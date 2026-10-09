"""Check a built visual-flow diagram against its spec and its sources.

    python check_spec.py spec.json [--repo-root DIR]

Everything here should hold after any rebuild, so it is worth running whenever
the spec or the renderer moves. Claims about the code a diagram describes live
beside the spec in `<spec>.claims.json`, not here: they belong to the diagram,
not to the renderer.

    [{"repo": "ancera-platform", "path": "biodata/models.py",
      "contains": "is_control = models.BooleanField(default=False)"},
     {"repo": "dataEngineering_airflow", "path": "dags/old_dag.py", "absent": true}]

Exits non-zero if anything fails.
"""

import contextlib
import io
import json
import pathlib
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_lanes as B  # noqa: E402

NS = "{http://www.w3.org/2000/svg}"
# No leading word boundary: Azure DevOps writes the commit as version=GC<sha>,
# and there is no boundary between the C and the hex that follows it.
SHA = re.compile(r"([0-9a-f]{40})(?![0-9a-f])")
REPO = re.compile(r"_git/([^/?&]+)|github\.com/[^/]+/([^/]+)/blob")


class Report:
    def __init__(self):
        self.failures = []

    def check(self, label, ok, detail=""):
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
        if not ok:
            self.failures.append(label)
        return ok


def render(spec_path, out_dir):
    """Build into out_dir and return {name: text} for every SVG written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    svg = out_dir / "d.svg"
    with contextlib.redirect_stdout(io.StringIO()):
        B.build(str(spec_path), str(out_dir / "d.html"), str(svg))
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(out_dir.glob("*.svg"))}


def parsed(text):
    root = ET.fromstring(text)
    groups = []
    for top in root:
        if top.tag != NS + "g":
            continue
        classes = {(x.get("class") or "").split(" ")[0] for x in top.iter() if x.get("class")}
        for kind in ("pulse", "route", "card", "lane"):
            if kind in classes:
                groups.append(kind)
                break
    by = lambda c: [x for x in root.iter(NS + "g") if x.get("class") == c]  # noqa: E731
    box = re.search(r'viewBox="0 0 (\d+) (\d+)"', text)
    return {
        "root": root, "order": groups, "w": int(box.group(1)), "h": int(box.group(2)),
        "cards": by("card"), "edges": by("edge"), "beats": by("beat"),
        "cut": [x.text for x in root.iter(NS + "text")
                if x.get("class") in ("card-title", "card-field") and x.text.endswith("...")],
        "links": [a.get("href") for a in root.iter(NS + "a")
                  if (a.get("href") or "").startswith("http")],
    }


def check_sources(spec, repo_root, report):
    """Every lane source must pin a commit its repository is actually on, and
    every linked path must exist there."""
    import subprocess

    for lane in spec["lanes"]:
        source = lane.get("source")
        if not source:
            continue
        sha = SHA.search(source)
        found = REPO.search(source)
        name = found and (found.group(1) or found.group(2))
        repo = repo_root / name if name else None
        if not sha or not repo or not repo.exists():
            print(f"  --    lane {lane['id']}: no pinned commit to check")
            continue
        head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
        report.check(f"lane {lane['id']} pins {name} at HEAD", sha.group(1) == head,
                     "" if sha.group(1) == head else f"pinned {sha.group(1)[:9]}, HEAD {head[:9]}")

    lanes = {lane["id"]: lane for lane in spec["lanes"]}
    missing = []
    total = 0
    for card in spec["cards"]:
        source = lanes[card["lane"]].get("source") or ""
        found = REPO.search(source)
        name = found and (found.group(1) or found.group(2))
        for entry in card.get("files", []):
            total += 1
            path = entry.split(":")[0]
            if name and not (repo_root / name / path).exists():
                missing.append(f"{card['id']}:{path}")
    report.check(f"all {total} linked files exist", not missing, "; ".join(missing[:4]))


def check_claims(spec_path, repo_root, report):
    claims_path = spec_path.with_suffix(spec_path.suffix + ".claims.json")
    if not claims_path.exists():
        print(f"  --    no {claims_path.name}; skipping source claims")
        return
    claims = json.loads(claims_path.read_text(encoding="utf-8"))
    bad = []
    for claim in claims:
        path = repo_root / claim["repo"] / claim["path"]
        if claim.get("absent"):
            if path.exists():
                bad.append(f"still present: {claim['repo']}/{claim['path']}")
        elif not path.exists():
            bad.append(f"gone: {claim['repo']}/{claim['path']}")
        elif claim["contains"] not in path.read_text(encoding="utf-8", errors="replace"):
            bad.append(f"{claim['repo']}/{claim['path']} :: {claim['contains'][:44]}")
    report.check(f"all {len(claims)} source claims hold", not bad, "; ".join(bad[:4]))


def main(spec_path, repo_root):
    spec_path = pathlib.Path(spec_path)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    report = Report()

    print("spec")
    problems = B.validate(spec)
    report.check("validates", not problems, "; ".join(problems[:3]))
    if problems:
        return 1
    for note in B.warnings(spec):
        print(f"  warn  {note}")

    print("render")
    with tempfile.TemporaryDirectory() as tmp:
        one = render(spec_path, pathlib.Path(tmp) / "a")
        two = render(spec_path, pathlib.Path(tmp) / "b")
    report.check(f"deterministic across {len(one)} svg files", one == two)

    main_svg = parsed(one["d.svg"])
    for name, text in one.items():
        got = parsed(text)
        report.check(f"{name}: parses, no script, ascii, nothing truncated",
                     "<script" not in text and text.isascii() and not got["cut"],
                     "" if not got["cut"] else f"cut: {got['cut'][:2]}")
        routed = "route" in got["order"]
        want = ["lane", "pulse", "route", "card"] if routed else ["lane", "card"]
        report.check(f"{name}: draw order puts pulses under the labels",
                     got["order"] == want, f"got {got['order']}")

    print("walkthrough")
    steps = spec.get("walkthrough", [])
    if not steps:
        print("  --    none")
    for i, step in enumerate(steps, start=1):
        lit = [c for c in main_svg["cards"] if str(i) in (c.get("data-step") or "").split()]
        report.check(f"step {i} lights the {len(step['cards'])} cards it names",
                     len(lit) == len(step["cards"]), f"lit {len(lit)}")

    print("views")
    if not spec.get("views"):
        print("  --    none")
    for view in spec.get("views", []):
        got = parsed(one[f"d.{view['id']}.svg"])
        scope = set(view.get("cards", [])) | {
            c["id"] for c in spec["cards"] if c["lane"] in set(view.get("lanes", []))}
        edges = [e for e in spec["edges"] if e[0] in scope and e[1] in scope]
        report.check(
            f"view {view['id']} holds {len(scope)} cards, {len(edges)} edges, no walkthrough, "
            f"and fits inside the whole",
            len(got["cards"]) == len(scope) and len(got["edges"]) == len(edges)
            and not got["beats"] and got["w"] <= main_svg["w"] and got["h"] <= main_svg["h"],
            f'{len(got["cards"])} cards, {len(got["edges"])} edges, {got["w"]}x{got["h"]}')

    print("sources")
    check_sources(spec, repo_root, report)
    check_claims(spec_path, repo_root, report)

    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    root = pathlib.Path.cwd()
    if "--repo-root" in args:
        i = args.index("--repo-root")
        root = pathlib.Path(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    sys.exit(main(args[0], root))
