"""Emit a pull-request description for a diagram, for hosts that will not
render the SVG itself.

    python to_markdown.py spec.json --images <prefix> [--svg <url>]

A raster loses the two things the SVG carries that a reviewer actually uses:
the links from each card to its source, and the walkthrough. The links come
back here as markdown, which every host renders; the walkthrough does not, so
`--svg` adds one line pointing at the file that still steps.

`--images` is where the PNGs will live: a repository path, a raw URL, or the
attachment URL the host gives you after you drag the file in.
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_lanes as B  # noqa: E402


def counts(spec):
    cards = [c["delta"] for c in spec["cards"] if c.get("delta")]
    fields = [f["delta"] for c in spec["cards"] for f in c["fields"] if f.get("delta")]
    bits = []
    for delta in B.DELTA_ORDER:
        if cards.count(delta):
            bits.append(f"**{cards.count(delta)}** {delta} cards")
    for delta in B.DELTA_ORDER:
        if fields.count(delta):
            bits.append(f"**{fields.count(delta)}** {delta} fields")
    bits.append(f"{len(spec['cards'])} cards across {len(spec['lanes'])} lanes")
    return " &middot; ".join(bits)


def index(spec):
    """One line per card that names files, with its lane and its links."""
    lanes = {lane["id"]: lane for lane in spec["lanes"]}
    rows = []
    for card in spec["cards"]:
        if not card["refs"]:
            continue
        mark = {"new": "NEW", "changed": "CHANGED", "removed": "REMOVED"}.get(card.get("delta"), "")
        links = ", ".join(
            f"[{ref['name']}]({ref['href']})" if ref["href"] else f"`{ref['name']}`"
            for ref in card["refs"])
        rows.append(f"| {lanes[card['lane']]['label']} | {card['title']['text']}"
                    f"{' **' + mark + '**' if mark else ''} | {links} |")
    if not rows:
        return ""
    return ("\n| Lane | Card | Source |\n|---|---|---|\n" + "\n".join(rows) + "\n")


def main(spec_path, images, svg_url):
    spec = json.loads(pathlib.Path(spec_path).read_text(encoding="utf-8"))
    problems = B.validate(spec)
    if problems:
        sys.exit("\n".join(problems))
    B.normalize(spec)
    stem = pathlib.Path(spec_path).stem.replace("_spec", "")

    out = [f"## {spec['title']}", "", spec.get("lede", ""), "", counts(spec), ""]
    if svg_url:
        out += [f"The [SVG]({svg_url}) is the live one: it animates, and the numbered rail "
                f"steps through the change. The images below are stills of it.", ""]
    out += [f"![{spec['title']}]({images}/{stem}.png)", ""]

    for view in spec.get("views", []):
        out += [f"<details><summary><b>{view['title']}</b></summary>", ""]
        if view.get("summary"):
            out += [view["summary"], ""]
        out += [f"![{view['title']}]({images}/{stem}.{view['id']}.png)", "", "</details>", ""]

    files = index(spec)
    if files:
        out += ["<details><summary><b>Where each card comes from</b></summary>", files,
                "</details>", ""]
    print("\n".join(out))


if __name__ == "__main__":
    args = sys.argv[1:]
    images, svg_url = ".", None
    for flag in ("--images", "--svg"):
        if flag in args:
            i = args.index(flag)
            value = args[i + 1]
            del args[i:i + 2]
            if flag == "--images":
                images = value.rstrip("/")
            else:
                svg_url = value
    if len(args) != 1:
        sys.exit(__doc__)
    main(args[0], images, svg_url)
