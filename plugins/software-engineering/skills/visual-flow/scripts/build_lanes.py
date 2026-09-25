"""Render a visual-flow spec to a standalone SVG, and to a page around it.

    python build_lanes.py spec.json out.html [out.svg] [--pr | --scale N]
    python build_lanes.py --demo

--pr grows the type and the space around it without widening the columns, for
a diagram that will be scaled down to fit a pull-request comment.

Layout and text measurement happen here, not in a browser: the SVG carries its
own stylesheet and its motion is animateMotion in the markup, so the diagram
still draws and still moves where scripts are stripped, and a machine with no
fonts installed produces the same bytes as a laptop.

A card title or field line may open with a delta marker: "+ " for new, "~ " for
changed, "- " for removed. The marker is stripped and the delta travels as data,
so it can be counted and coloured rather than read as text.
"""

import copy
import html
import json
import pathlib
import re
import sys

ASSETS = pathlib.Path(__file__).resolve().parents[1] / "assets"

SCHEMA_VERSION = "1.0.0"
SUPPORTED_MAJOR = 1

PAD, ROW, HEAD, CARD_PAD = 20, 15, 24, 8
FILE_ROW, FILE_GAP = 13, 7
MIN_GAP, MIN_ROW_GAP, SLOT = 46, 34, 17
PULSE_SPEED, MIN_DUR = 110.0, 1.2
TITLE_SIZE, FIELD_SIZE, LABEL_SIZE, PILL_SIZE, FILE_SIZE = 11.5, 10.5, 9.5, 7.5, 9.0
LANE_SIZE, SUB_SIZE, GLYPH_SIZE, CHIP_SIZE = 15.0, 11.0, 8.0, 10.0
PILL_TRACKING = 0.4
GLYPH_W = 22
RAIL_H, CHIP, CHIP_GAP = 48, 17, 5
BEAT_SIZE, BODY_SIZE = 10.5, 10.0
SUB_CHARS = 22
MIN_STEPS, MAX_STEPS = 2, 12
PR_SCALE = 1.45

# Type and vertical rhythm scale together; column width does not. A diagram
# embedded in a fixed-width column is scaled to fit, so growing the columns
# with the type would cancel out. Holding width and letting cards grow taller
# is what actually makes the text bigger once the column has shrunk it.
SCALED = ("PAD", "ROW", "HEAD", "CARD_PAD", "FILE_ROW", "FILE_GAP", "MIN_GAP", "MIN_ROW_GAP",
          "SLOT", "TITLE_SIZE", "FIELD_SIZE", "LABEL_SIZE", "PILL_SIZE", "FILE_SIZE",
          "LANE_SIZE", "SUB_SIZE", "GLYPH_SIZE", "CHIP_SIZE", "PILL_TRACKING", "GLYPH_W",
          "RAIL_H", "CHIP", "CHIP_GAP", "BEAT_SIZE", "BODY_SIZE")
BASE = {}


def set_scale(scale):
    """Resize the type and the space around it. Kept as module state because
    every metric below is read from thirty-odd places."""
    if not BASE:
        BASE.update({name: globals()[name] for name in SCALED})
    globals().update({name: BASE[name] * scale for name in SCALED})
    globals()["SUB_CHARS"] = max(8, int(22 / scale))
    globals()["SCALE"] = scale


SCALE = 1.0

TYPE_VARS = (("lane", "LANE_SIZE"), ("sub", "SUB_SIZE"), ("title", "TITLE_SIZE"),
             ("field", "FIELD_SIZE"), ("pill", "PILL_SIZE"), ("glyph", "GLYPH_SIZE"),
             ("file", "FILE_SIZE"), ("label", "LABEL_SIZE"), ("chip", "CHIP_SIZE"),
             ("beat", "BEAT_SIZE"), ("body", "BODY_SIZE"))


def type_css():
    """The one place font sizes are declared, so measurement and drawing agree."""
    decls = " ".join(f"--fs-{name}: {globals()[const]:.2f}px;" for name, const in TYPE_VARS)
    return "svg.flow { " + decls + " }"

# Advance width of one character as a fraction of the font size, for the mono
# stack in diagram.css. Every card and route string is measured with this and
# pinned with textLength, so the drawn width does not move with the viewer's
# installed fonts.
MONO = 0.55

# Coarse on purpose: the glyph says what kind of thing a card is at a glance,
# and never drives anything else. Anything that does not fit is "other".
KIND_GLYPH = {
    "workbook": "WB",
    "function": "fn",
    "module": "{}",
    "table": "TBL",
    "query": "SQL",
    "task": "DAG",
    "endpoint": "API",
    "model": "MDL",
    "command": ">_",
    "grid": "GRD",
    "other": "*",
}
EMPHASIS = ("normal", "hero", "muted")

MARKERS = {"+ ": "new", "~ ": "changed", "- ": "removed"}
DELTA_ORDER = ("new", "changed", "removed")
DEFAULTS = {"colw": 214, "gut": 22, "laneLabelW": 150}

LANE_KEYS = {"id", "label", "sub", "color", "source"}
CARD_KEYS = {"id", "lane", "col", "title", "fields", "span", "y", "kind", "files"}
SPEC_KEYS = {"schemaVersion", "title", "lede", "layout", "lanes", "cards", "edges", "walkthrough", "views"}
VIEW_KEYS = {"id", "title", "summary", "lanes", "cards"}
MAX_VIEWS = 8
STEP_KEYS = {"heading", "body", "cards", "lanes", "routes"}
LAYOUT_KEYS = {"colw", "gut", "laneLabelW", "columns"}


def text_width(text, size):
    return len(text) * size * MONO


def split_long(word, size, max_px):
    """Break an over-long identifier or path at _ . / - so it can wrap. Names
    here are mostly one long token, and a token that cannot break is a token
    that gets cut."""
    if text_width(word, size) <= max_px:
        return [word]
    parts, cur = [], ""
    for piece in re.split(r"(?<=[_./-])", word):
        if cur and text_width(cur + piece, size) > max_px:
            parts.append(cur)
            cur = piece
        else:
            cur += piece
    if cur:
        parts.append(cur)
    return parts


def wrap_px(text, size, max_px):
    """Break on spaces to fit max_px, and inside a word when the word alone
    is too wide."""
    lines, line = [], ""
    words = [p for word in text.split(" ") for p in split_long(word, size, max_px)]
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and text_width(candidate, size) > max_px:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or [""]


def fit_text(text, size, room, floor=0.85):
    """Return (text, drawn width) for a string pinned into room. A slight
    overflow is squeezed; past the floor the text is cut instead, because a
    hard squeeze is unreadable."""
    natural = text_width(text, size)
    if natural <= room:
        return text, natural
    if room / natural >= floor:
        return text, room
    keep = max(1, int(room / (size * MONO * floor)) - 3)
    return text[:keep] + "...", room


def wrap_chars(text, width):
    lines, line = [], ""
    for word in text.split(" "):
        candidate = f"{line} {word}".strip()
        if line and len(candidate) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def split_delta(text):
    for marker, delta in MARKERS.items():
        if text.startswith(marker):
            return {"text": text[len(marker):].strip(), "delta": delta}
    return {"text": text}


def split_file(entry):
    """"path" or "path:42" -> (path, line or None)."""
    match = re.fullmatch(r"(.+?):(\d+)", entry)
    return (match.group(1), int(match.group(2))) if match else (entry, None)


def permalink(template, path, line):
    url = template.replace("{path}", path)
    if "{line}" in url:
        url = url.replace("{line}", str(line) if line else "1")
    return url


def normalize(spec):
    """Lift markers, kinds and file refs out of the prose and onto the card."""
    lanes = {lane["id"]: lane for lane in spec["lanes"]}
    for card in spec["cards"]:
        card["title"] = split_delta(card["title"])
        card["fields"] = [split_delta(f) for f in card["fields"]]
        card["delta"] = card["title"].get("delta")
        card["glyph"] = KIND_GLYPH.get(card.get("kind")) if card.get("kind") else None
        source = lanes[card["lane"]].get("source")
        refs = []
        for entry in card.get("files", []):
            path, line = split_file(entry)
            refs.append({"path": path, "line": line, "name": path.rsplit("/", 1)[-1],
                         "href": permalink(source, path, line) if source else None})
        card["refs"] = refs
    spec["edges"] = [list(edge) + ["normal"] if len(edge) == 3 else list(edge) for edge in spec["edges"]]

    # A step lights the cards it names, and any route whose two ends are both
    # lit, so the common case needs no route list at all.
    for i, step in enumerate(spec.get("walkthrough", []), start=1):
        step["n"] = i
        step["id"] = f"vfs{i}"
        focus = set(step["cards"])
        routes = {tuple(r.split(">")) for r in step.get("routes", [])}
        routes |= {(a, b) for a, b, *_ in spec["edges"] if a in focus and b in focus}
        step["focus_cards"], step["focus_routes"] = focus, routes
    return spec


def tally(spec):
    cards = [c["delta"] for c in spec["cards"] if c.get("delta")]
    fields = [f["delta"] for c in spec["cards"] for f in c["fields"] if f.get("delta")]
    parts = []
    for delta in DELTA_ORDER:
        if cards.count(delta):
            parts.append((delta, f"{cards.count(delta)} {delta} cards"))
    for delta in DELTA_ORDER:
        if fields.count(delta):
            parts.append((delta, f"{fields.count(delta)} {delta} fields"))
    linked = sum(len(c.get("files", [])) for c in spec["cards"])
    if linked:
        parts.append((None, f"{linked} linked files"))
    parts.append((None, f"{len(spec['cards'])} cards across {len(spec['lanes'])} lanes"))
    return '<span class="sep">&middot;</span>'.join(
        f'<span class="count{" delta-" + d if d else ""}">{html.escape(label)}</span>'
        for d, label in parts
    )


def validate(spec):
    """Reject a spec that could not draw, naming every problem at once."""
    problems = []

    version = spec.get("schemaVersion")
    if version is None:
        problems.append(f'no schemaVersion; this build speaks {SCHEMA_VERSION}')
    elif not re.fullmatch(r"\d+\.\d+\.\d+", str(version)):
        problems.append(f'schemaVersion {version!r} is not a semver string')
    elif int(str(version).split(".")[0]) != SUPPORTED_MAJOR:
        problems.append(f'schemaVersion {version} is not major {SUPPORTED_MAJOR}')

    for key in ("title", "lanes", "cards", "edges"):
        if key not in spec:
            problems.append(f"spec has no {key}")
    problems += [f"spec has unknown key {k!r}" for k in set(spec) - SPEC_KEYS]
    problems += [f"layout has unknown key {k!r}" for k in set(spec.get("layout", {})) - LAYOUT_KEYS]
    if problems:
        return problems

    lanes, seen = {}, set()
    for lane in spec["lanes"]:
        problems += [f"lane has unknown key {k!r}" for k in set(lane) - LANE_KEYS]
        if "id" not in lane or "label" not in lane:
            problems.append(f"lane {lane.get('id', '?')} needs an id and a label")
            continue
        if lane["id"] in seen:
            problems.append(f"duplicate lane id {lane['id']}")
        seen.add(lane["id"])
        source = lane.get("source")
        if source is not None and "{path}" not in source:
            problems.append(f"lane {lane['id']} source has no {{path}} placeholder")
        lanes[lane["id"]] = lane

    cards = set()
    for c in spec["cards"]:
        where = c.get("id", "?")
        problems += [f"card {where} has unknown key {k!r}" for k in set(c) - CARD_KEYS]
        if not all(k in c for k in ("id", "lane", "col", "title", "fields")):
            problems.append(f"card {where} needs id, lane, col, title and fields")
            continue
        if c["id"] in cards:
            problems.append(f"duplicate card id {c['id']}")
        cards.add(c["id"])
        if c["lane"] not in lanes:
            problems.append(f"card {c['id']} names unknown lane {c['lane']}")
        if not isinstance(c["col"], int) or c["col"] < 0:
            problems.append(f"card {c['id']} col must be a non-negative integer")
        if not isinstance(c.get("span", 1), int) or c.get("span", 1) < 1:
            problems.append(f"card {c['id']} span must be a positive integer")
        if not c["fields"]:
            problems.append(f"card {c['id']} has no fields")
        if c.get("kind") and c["kind"] not in KIND_GLYPH:
            problems.append(f"card {c['id']} kind {c['kind']!r} is not one of {sorted(KIND_GLYPH)}")
        for entry in c.get("files", []):
            if not isinstance(entry, str) or not entry.strip():
                problems.append(f"card {c['id']} has an empty file entry")
            elif c["lane"] in lanes and not lanes[c["lane"]].get("source"):
                problems.append(f"card {c['id']} lists files but lane {c['lane']} has no source")

    for edge in spec["edges"]:
        if not isinstance(edge, list) or len(edge) not in (3, 4):
            problems.append(f"edge {edge!r} must be [from, to, label] or [from, to, label, emphasis]")
            continue
        a, b = edge[0], edge[1]
        if a not in cards or b not in cards:
            problems.append(f"edge {a}->{b} names an unknown card")
        if len(edge) == 4 and edge[3] not in EMPHASIS:
            problems.append(f"edge {a}->{b} emphasis {edge[3]!r} is not one of {list(EMPHASIS)}")

    views = spec.get("views")
    if views is not None:
        if not isinstance(views, list) or not 1 <= len(views) <= MAX_VIEWS:
            problems.append(f"views must be 1 to {MAX_VIEWS} entries")
            return problems
        seen_views = set()
        for i, v in enumerate(views, start=1):
            problems += [f"view {i} has unknown key {k!r}" for k in set(v) - VIEW_KEYS]
            if not v.get("id") or not v.get("title"):
                problems.append(f"view {i} needs an id and a title")
                continue
            if v["id"] in seen_views:
                problems.append(f"duplicate view id {v['id']}")
            seen_views.add(v["id"])
            problems += [f"view {v['id']} names unknown card {c}" for c in v.get("cards", []) if c not in cards]
            problems += [f"view {v['id']} names unknown lane {l}" for l in v.get("lanes", []) if l not in lanes]
            in_scope = set(v.get("cards", [])) | {
                c["id"] for c in spec["cards"] if c["lane"] in set(v.get("lanes", []))}
            if not in_scope:
                problems.append(f"view {v['id']} scopes to no cards")

    steps = spec.get("walkthrough")
    if steps is not None:
        pairs = {f"{a}>{b}" for a, b, *_ in spec["edges"]}
        if not isinstance(steps, list) or not MIN_STEPS <= len(steps) <= MAX_STEPS:
            problems.append(f"walkthrough must be {MIN_STEPS} to {MAX_STEPS} steps; "
                            "one step is a caption, and a long tour loses the reader")
            return problems
        for i, step in enumerate(steps, start=1):
            problems += [f"step {i} has unknown key {k!r}" for k in set(step) - STEP_KEYS]
            if not step.get("heading") or not step.get("body"):
                problems.append(f"step {i} needs a heading and a body")
            if not step.get("cards"):
                problems.append(f"step {i} names no cards")
            problems += [f"step {i} names unknown card {c}" for c in step.get("cards", []) if c not in cards]
            problems += [f"step {i} names unknown lane {l}" for l in step.get("lanes", []) if l not in lanes]
            problems += [f"step {i} route {r!r} is not an edge" for r in step.get("routes", []) if r not in pairs]
    return problems


def warnings(spec):
    """Things worth saying that are not reasons to refuse to draw."""
    notes = []
    steps = spec.get("walkthrough")
    if steps:
        named = {card for step in steps for card in step.get("cards", [])}
        dark = [c["id"] for c in spec["cards"] if c["id"] not in named]
        if dark:
            notes.append(
                f"{len(dark)} of {len(spec['cards'])} cards are lit by no walkthrough step, "
                f"so they stay dimmed for the whole tour: {', '.join(dark)}"
            )
    return notes


def scoped(spec, view):
    """A spec holding only what a view names, laid out on its own.

    A view is drawn rather than dimmed: dropping the lanes and columns it does
    not use is what makes it smaller than the whole picture, which is the only
    reason to have one."""
    keep = set(view.get("cards", []))
    keep |= {c["id"] for c in spec["cards"] if c["lane"] in set(view.get("lanes", []))}
    cards = [copy.deepcopy(c) for c in spec["cards"] if c["id"] in keep]

    # Columns close up, so a view of two streams is two streams wide.
    used = sorted({col for c in cards for col in range(c["col"], c["col"] + c.get("span", 1))})
    shift = {col: i for i, col in enumerate(used)}
    for c in cards:
        c["col"] = shift[c["col"]]

    lanes = [copy.deepcopy(l) for l in spec["lanes"] if any(c["lane"] == l["id"] for c in cards)]
    edges = [list(e) for e in spec["edges"] if e[0] in keep and e[1] in keep]
    out = {k: spec[k] for k in ("schemaVersion", "layout") if k in spec}
    out.update({"title": view["title"], "lede": view.get("summary", ""),
                "lanes": lanes, "cards": cards, "edges": edges})
    return out


def nest(group):
    """Longest span nearest the source, so parallel runs sit inside each other."""
    group.sort(key=lambda r: -abs(r["x2"] - r["x1"]))
    for i, route in enumerate(group):
        route["slot"], route["slots"] = i + 1, len(group)
    return group


def layout(spec):
    L = {**DEFAULTS, **spec.get("layout", {})}
    L["laneLabelW"] = L["laneLabelW"] * SCALE
    lanes, cards, edges = spec["lanes"], spec["cards"], spec["edges"]
    columns = L.get("columns") or max(c["col"] + c.get("span", 1) for c in cards)

    for i, lane in enumerate(lanes):
        lane["index"] = i
        lane["tint"] = lane.get("color") or f"var(--l{i % 8})"
    lane_by_id = {lane["id"]: lane for lane in lanes}

    for c in cards:
        span = c.get("span", 1)
        c["w"] = L["colw"] * span + L["gut"] * (span - 1)
        c["x"] = L["laneLabelW"] + PAD + c["col"] * (L["colw"] + L["gut"])
        inner = c["w"] - 18
        c["lines"] = [
            {"text": line, "delta": f.get("delta")}
            for f in c["fields"]
            for line in wrap_px(f["text"], FIELD_SIZE, inner)
        ]
        # A bigger type scale leaves the title less room, so let it take a
        # second line rather than lose its ending to an ellipsis.
        c["pill_w"] = (len(c["delta"].upper()) * (PILL_SIZE * MONO + PILL_TRACKING) + 12 + 6
                       if c.get("delta") else 0)
        c["title_x"] = c["x"] + (6 + GLYPH_W + 6 if c["glyph"] else 9)
        room = c["x"] + c["w"] - c["pill_w"] - 9 - c["title_x"]
        c["title_room"] = room
        c["title_lines"] = wrap_px(c["title"]["text"], TITLE_SIZE, room)[:2]
        c["head_h"] = HEAD + (len(c["title_lines"]) - 1) * ROW
        c["h"] = c["head_h"] + CARD_PAD + len(c["lines"]) * ROW + CARD_PAD
        if c["refs"]:
            c["files_top"] = c["h"] - CARD_PAD + FILE_GAP
            c["h"] = c["files_top"] + len(c["refs"]) * FILE_ROW + CARD_PAD
    by_id = {c["id"]: c for c in cards}

    # Ports depend on x only, so routes can be shaped before lanes are placed.
    out_count, in_count = {}, {}
    for a, b, *_ in edges:
        out_count[a] = out_count.get(a, 0) + 1
        in_count[b] = in_count.get(b, 0) + 1
    out_idx, in_idx = {}, {}
    routes = []
    for a, b, label, emphasis in edges:
        s, t = by_id[a], by_id[b]
        out_idx[a] = out_idx.get(a, 0) + 1
        in_idx[b] = in_idx.get(b, 0) + 1
        x1 = s["x"] + s["w"] * out_idx[a] / (out_count[a] + 1)
        x2 = t["x"] + t["w"] * in_idx[b] / (in_count[b] + 1)
        routes.append({
            "s": s, "t": t, "from": lane_by_id[s["lane"]], "to": lane_by_id[t["lane"]],
            "label": label, "emphasis": emphasis, "x1": x1, "x2": x2,
            "intra": s["lane"] == t["lane"], "straight": abs(x1 - x2) < 2,
            "key": (a, b),
        })

    # Inside a lane, a card fed by another card in the same lane sits on its own
    # row below it, so every hop still reads downward. Rank is the longest path
    # over the lane's own edges; the sweep count caps any cycle.
    for lane in lanes:
        lane_cards = [c for c in cards if c["lane"] == lane["id"]]
        intra = [r for r in routes if r["intra"] and r["from"] is lane]
        for c in lane_cards:
            c["rank"] = 0
        for _ in range(len(lane_cards)):
            moved = False
            for r in intra:
                if r["s"]["rank"] + 1 > r["t"]["rank"]:
                    r["t"]["rank"] = r["s"]["rank"] + 1
                    moved = True
            if not moved:
                break

        dy = PAD
        for rank in sorted({c["rank"] for c in lane_cards}):
            stacks = {}
            for c in [c for c in lane_cards if c["rank"] == rank]:
                stacks.setdefault(c["col"], []).append(c)
            row_h = 0
            for col in stacks:
                cy = 0
                for c in sorted(stacks[col], key=lambda c: c.get("y", 0)):
                    c["dy"] = dy + cy
                    cy += c["h"] + 12
                row_h = max(row_h, cy - 12)
            crossing = nest([r for r in intra if r["s"]["rank"] == rank])
            gap = max(MIN_ROW_GAP, len(crossing) * SLOT + 16) if crossing else 0
            for r in crossing:
                r["row_bottom"], r["row_gap"] = dy + row_h, gap
            dy += row_h + gap
        lane["h"] = dy + PAD

    # Every route that leaves its lane gets a slot in the gap below that lane.
    gap_after = {lane["index"]: MIN_GAP for lane in lanes}
    by_gap = {}
    for r in routes:
        if not r["straight"] and not r["intra"]:
            by_gap.setdefault(r["from"]["index"], []).append(r)
    for index, group in by_gap.items():
        gap_after[index] = max(MIN_GAP, len(nest(group)) * SLOT + 24)

    rail = RAIL_H if spec.get("walkthrough") else 0
    y = 16 + rail
    for lane in lanes:
        lane["y"] = y
        y += lane["h"] + gap_after[lane["index"]]
    for c in cards:
        c["cy"] = lane_by_id[c["lane"]]["y"] + c["dy"]

    for r in routes:
        r["y1"] = r["s"]["cy"] + r["s"]["h"]
        r["y2"] = r["t"]["cy"]
        if r["straight"]:
            r["mid"] = None
            r["d"] = f'M{r["x1"]:.2f},{r["y1"]:.2f} L{r["x2"]:.2f},{r["y2"]:.2f}'
        else:
            if r["intra"]:
                mid = r["from"]["y"] + r["row_bottom"] + r["row_gap"] * r["slot"] / (r["slots"] + 1)
            else:
                top = r["from"]["y"] + r["from"]["h"]
                mid = top + gap_after[r["from"]["index"]] * r["slot"] / (r["slots"] + 1)
            r["mid"] = mid
            r["d"] = (f'M{r["x1"]:.2f},{r["y1"]:.2f} L{r["x1"]:.2f},{mid:.2f} '
                      f'L{r["x2"]:.2f},{mid:.2f} L{r["x2"]:.2f},{r["y2"]:.2f}')
        r["length"] = (abs(r["y2"] - r["y1"]) if r["straight"]
                       else abs(r["mid"] - r["y1"]) + abs(r["x2"] - r["x1"]) + abs(r["y2"] - r["mid"]))

    width = L["laneLabelW"] + PAD * 2 + columns * L["colw"] + (columns - 1) * L["gut"] + 4
    height = y - gap_after[lanes[-1]["index"]] + 16
    return {"routes": routes, "w": width, "h": height, "L": L, "rail": rail}


def esc(value):
    return html.escape(str(value), quote=True)


def attrs_str(attrs):
    return " ".join(f'{k}="{esc(v)}"' for k, v in attrs.items() if v is not None)


def open_tag(name, attrs):
    return f"<{name} {attrs_str(attrs)}>"


def tag(name, attrs, text=None):
    if text is None:
        return f"<{name} {attrs_str(attrs)}/>"
    return f"<{name} {attrs_str(attrs)}>{html.escape(text)}</{name}>"


def step_css(steps, cards, routes):
    """One rule set per step, driven from an empty target element that sits
    before every content group.

    Every element a step dims is named by id. The compact form,
    `#step:target ~ g .card:not([data-step~="n"])`, matches when asked and
    still does not repaint: on a hash change the browser never recomputes
    style for it, so clicking a step left the diagram untouched, while the
    id-keyed rules beside it worked. Ids give the invalidation something cheap
    to hang on, and the length costs nothing in generated output."""
    rules = []
    for step in steps:
        sid, n = step["id"], step["n"]
        dim = [c["vfid"] for c in cards if c["id"] not in step["focus_cards"]]
        dim += [r["vfid"] for r in routes if r["key"] not in step["focus_routes"]]
        dim += [r["pulse_id"] for r in routes if r["key"] not in step["focus_routes"]]
        if dim:
            rules.append(", ".join(f"#{sid}:target ~ g #{i}" for i in dim) + " { opacity: 0.08; }")
        rules.append(f'#{sid}:target ~ g #vfc{n} .chip {{ fill: var(--c); }}')
        rules.append(f'#{sid}:target ~ g #vfc{n} .chip-label {{ fill: var(--panel); }}')
        rules.append(f'#{sid}:target ~ g #vfh{n}, #{sid}:target ~ g #vfb{n} {{ opacity: 1; }}')
    return chr(10).join(rules)


def render_rail(spec, geo, out):
    steps = spec["walkthrough"]
    L = geo["L"]
    x = L["laneLabelW"] + PAD
    out.append(open_tag("g", {"class": "rail"}))
    for step in steps:
        cx = x + (step["n"] - 1) * (CHIP + CHIP_GAP)
        out.append(open_tag("a", {"href": f'#{step["id"]}'}))
        out.append(open_tag("g", {"id": f'vfc{step["n"]}'}))
        out.append(tag("rect", {"x": f"{cx:.2f}", "y": 14, "width": CHIP, "height": CHIP,
                                "rx": 3, "class": "chip"}))
        out.append(tag("text", {"x": f"{cx + CHIP / 2:.2f}", "y": 26, "class": "chip-label",
                                "text-anchor": "middle"}, str(step["n"])))
        out.append("</g></a>")
    end = x + len(steps) * (CHIP + CHIP_GAP)
    out.append(open_tag("a", {"href": "#"}))
    out.append(tag("rect", {"x": f"{end:.2f}", "y": 14, "width": CHIP, "height": CHIP,
                            "rx": 3, "class": "chip chip-reset"}))
    out.append(tag("text", {"x": f"{end + CHIP / 2:.2f}", "y": 26, "class": "chip-label",
                            "text-anchor": "middle"}, "x"))
    out.append("</a>")

    tx = end + CHIP + 14
    room = geo["w"] - tx - 10
    out.append(tag("text", {"x": f"{tx:.2f}", "y": 24, "class": "walk-hint"},
                   "Click a number to walk the change one step at a time."))
    for step in steps:
        head, drawn = fit_text(f'{step["n"]}. {step["heading"]}', BEAT_SIZE, room)
        out.append(tag("text", {"x": f"{tx:.2f}", "y": 24, "id": f'vfh{step["n"]}',
                                "class": "beat-head", "textLength": f"{drawn:.2f}",
                                "lengthAdjust": "spacingAndGlyphs"}, head))
        body, drawn = fit_text(step["body"], BODY_SIZE, room)
        out.append(tag("text", {"x": f"{tx:.2f}", "y": 39, "id": f'vfb{step["n"]}',
                                "class": "beat-body", "textLength": f"{drawn:.2f}",
                                "lengthAdjust": "spacingAndGlyphs"}, body))
    out.append("</g>")


def render_svg(spec, geo, css):
    lanes, cards = spec["lanes"], spec["cards"]
    lane_by_id = {lane["id"]: lane for lane in lanes}
    steps = spec.get("walkthrough", [])
    for i, c in enumerate(cards):
        c["vfid"] = f"vfk{i}"
    for i, r in enumerate(geo["routes"]):
        r["vfid"], r["pulse_id"] = f"vfe{i}", f"vfp{i}"

    def steps_for(key, bucket):
        hit = [str(s["n"]) for s in steps if key in s[f"focus_{bucket}"]]
        return " ".join(hit) if steps else None
    out = [
        f'<svg class="flow" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {geo["w"]:.0f} {geo["h"]:.0f}"',
        f' width="{geo["w"]:.0f}" height="{geo["h"]:.0f}" role="img"',
        f' aria-label="{esc(spec["title"])}">',
        "<style>", css, type_css(), step_css(steps, cards, geo["routes"]), "</style>",
        '<defs>',
        '<marker id="arrow" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="5" markerHeight="5"'
        ' orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 z" class="arrowhead"/></marker>',
        '<filter id="glow" x="-100%" y="-100%" width="300%" height="300%">'
        '<feGaussianBlur stdDeviation="2.6"/></filter>',
        "</defs>",
    ]

    if steps:
        # Empty, zero-sized, and ahead of every group the steps restyle.
        for step in steps:
            out.append(tag("g", {"id": step["id"], "class": "beat"}, ""))
        render_rail(spec, geo, out)

    out.append("<g>")
    for lane in lanes:
        out.append(open_tag("g", {"style": f'--c:{lane["tint"]}'}))
        out.append(tag("rect", {"x": 4, "y": f'{lane["y"]:.2f}', "width": f'{geo["w"] - 8:.0f}',
                                "height": f'{lane["h"]:.2f}', "class": "lane"}))
        out.append(tag("rect", {"x": 4, "y": f'{lane["y"]:.2f}', "width": 3,
                                "height": f'{lane["h"]:.2f}', "class": "lane-edge"}))
        out.append(tag("text", {"x": 18, "y": f'{lane["y"] + 24:.2f}', "class": "lane-title"}, lane["label"]))
        for i, line in enumerate(wrap_chars(lane.get("sub", ""), SUB_CHARS)):
            out.append(tag("text", {"x": 18, "y": f'{lane["y"] + 42 + i * 14:.2f}', "class": "lane-sub"}, line))
        out.append("</g>")
    out.append("</g>")

    # Pulses first: a travelling dot passes under the route chips rather than
    # blotting out the label it crosses.
    out.append("<g>")
    for n, r in enumerate(geo["routes"]):
        if r["emphasis"] == "muted":
            continue
        dur = max(MIN_DUR, r["length"] / PULSE_SPEED)
        out.append(open_tag("g", {"id": r["pulse_id"], "class": "pulse",
                                  "style": f'--c:{r["from"]["tint"]}',
                                  "data-step": steps_for(r["key"], "routes")}))
        out.append('<circle r="7" class="pulse-halo"/><circle r="2" class="pulse-core"/>')
        out.append(tag("animateMotion", {"dur": f"{dur:.2f}s", "begin": f"{(n % 7) * 0.45:.2f}s",
                                         "repeatCount": "indefinite", "path": r["d"]}))
        out.append("</g>")
    out.append("</g>")
    out.append("<g>")
    for r in geo["routes"]:
        style = f'--c:{r["from"]["tint"]}'
        out.append(open_tag("g", {"id": r["vfid"], "class": "edge",
                                  "data-step": steps_for(r["key"], "routes")}))
        classes = ["route"]
        if r["intra"]:
            classes.append("route-intra")
        if r["emphasis"] != "normal":
            classes.append(f'route-{r["emphasis"]}')
        out.append(tag("path", {"d": r["d"], "class": " ".join(classes),
                                "style": style, "marker-end": "url(#arrow)"}))
        if r["label"]:
            lx = r["x1"] + (r["x2"] - r["x1"]) * 0.35
            ly = (r["y1"] + r["y2"]) / 2 if r["straight"] else r["mid"]
            tw = text_width(r["label"], LABEL_SIZE)
            chip = "route-chip hero" if r["emphasis"] == "hero" else "route-chip"
            out.append(tag("rect", {"x": f"{lx - (tw + 10) / 2:.2f}", "y": f"{ly - 7:.2f}",
                                    "width": f"{tw + 10:.2f}", "height": 13, "rx": 6,
                                    "class": chip, "style": style}))
            out.append(tag("text", {"x": f"{lx:.2f}", "y": f"{ly + 3:.2f}", "class": "route-label",
                                    "text-anchor": "middle", "textLength": f"{tw:.2f}",
                                    "lengthAdjust": "spacingAndGlyphs", "style": style}, r["label"]))
        out.append("</g>")
    out.append("</g>")

    out.append("<g>")
    for c in cards:
        lane = lane_by_id[c["lane"]]
        attrs = {"id": c["vfid"], "class": "card", "style": f'--c:{lane["tint"]}',
                 "data-step": steps_for(c["id"], "cards")}
        if c.get("delta"):
            attrs["data-delta"] = c["delta"]
        out.append(open_tag("g", attrs))
        out.append(tag("rect", {"x": f'{c["x"]:.2f}', "y": f'{c["cy"]:.2f}', "width": c["w"],
                                "height": f'{c["h"]:.2f}', "rx": 4}))
        out.append(tag("rect", {"x": f'{c["x"]:.2f}', "y": f'{c["cy"]:.2f}', "width": c["w"],
                                "height": f'{c["head_h"]:.2f}', "rx": 4, "class": "head"}))
        out.append(tag("rect", {"x": f'{c["x"]:.2f}', "y": f'{c["cy"] + c["head_h"] - 1:.2f}',
                                "width": c["w"], "height": 1, "class": "head-rule"}))

        title_x = c["title_x"]
        if c["glyph"]:
            out.append(tag("rect", {"x": f'{c["x"] + 6:.2f}', "y": f'{c["cy"] + 6:.2f}',
                                    "width": GLYPH_W, "height": 13, "rx": 3, "class": "glyph"}))
            out.append(tag("text", {"x": f'{c["x"] + 6 + GLYPH_W / 2:.2f}', "y": f'{c["cy"] + 15.5:.2f}',
                                    "class": "glyph-label", "text-anchor": "middle"}, c["glyph"]))

        pill_w = 0
        if c.get("delta"):
            label = c["delta"].upper()
            pill_w = c["pill_w"] - 6
            out.append(tag("rect", {"x": f'{c["x"] + c["w"] - pill_w - 7:.2f}', "y": f'{c["cy"] + 6:.2f}',
                                    "width": f"{pill_w:.2f}", "height": 13, "rx": 6.5, "class": "pill"}))
            out.append(tag("text", {"x": f'{c["x"] + c["w"] - pill_w / 2 - 7:.2f}', "y": f'{c["cy"] + 15.5:.2f}',
                                    "class": "pill-label", "text-anchor": "middle"}, label))

        for n, raw in enumerate(c["title_lines"]):
            title, drawn = fit_text(raw, TITLE_SIZE, c["title_room"])
            out.append(tag("text", {"x": f"{title_x:.2f}",
                                    "y": f'{c["cy"] + HEAD * 0.667 + n * ROW:.2f}',
                                    "class": "card-title", "textLength": f"{drawn:.2f}",
                                    "lengthAdjust": "spacingAndGlyphs"}, title))
        for i, line in enumerate(c["lines"]):
            text, drawn = fit_text(line["text"], FIELD_SIZE, c["w"] - 18)
            attrs = {"x": f'{c["x"] + 9:.2f}',
                     "y": f'{c["cy"] + c["head_h"] + CARD_PAD + i * ROW + 11:.2f}',
                     "class": "card-field", "textLength": f"{drawn:.2f}",
                     "lengthAdjust": "spacingAndGlyphs"}
            if line["delta"]:
                attrs["data-delta"] = line["delta"]
            out.append(tag("text", attrs, text))

        if c["refs"]:
            top = c["cy"] + c["files_top"]
            out.append(tag("rect", {"x": f'{c["x"] + 9:.2f}', "y": f"{top - FILE_GAP + 1:.2f}",
                                    "width": c["w"] - 18, "height": 1, "class": "files-rule"}))
            for i, ref in enumerate(c["refs"]):
                name = ref["name"] + (f':{ref["line"]}' if ref["line"] else "")
                text, drawn = fit_text(name, FILE_SIZE, c["w"] - 18)
                node = tag("text", {"x": f'{c["x"] + 9:.2f}', "y": f"{top + i * FILE_ROW + 9:.2f}",
                                    "class": "card-file", "textLength": f"{drawn:.2f}",
                                    "lengthAdjust": "spacingAndGlyphs"}, text)
                if ref["href"]:
                    node = (open_tag("a", {"href": ref["href"], "target": "_blank"})
                            + node + "</a>")
                out.append(node)
        out.append("</g>")
    out.append("</g></svg>")
    return "".join(out)


def build(spec_path, out_html, out_svg=None, scale=1.0):
    set_scale(scale)
    spec = json.loads(pathlib.Path(spec_path).read_text(encoding="utf-8"))
    problems = validate(spec)
    if problems:
        sys.exit("\n".join(problems))
    for note in warnings(spec):
        print(f"warning: {note}", file=sys.stderr)
    css = (ASSETS / "diagram.css").read_text(encoding="utf-8")

    # Views are scoped from the spec as read, before the whole-diagram pass
    # rewrites it in place.
    views = []
    for view in spec.get("views", []):
        sub = scoped(spec, view)
        normalize(sub)
        views.append((view, sub, render_svg(sub, layout(sub), css)))

    normalize(spec)
    geo = layout(spec)
    svg = render_svg(spec, geo, css)

    drill = "".join(
        f'<details><summary>{html.escape(view["title"])}'
        f'<span class="scope">{len(sub["cards"])} cards, {len(sub["lanes"])} lanes</span></summary>'
        + (f'<p class="view-summary">{html.escape(view["summary"])}</p>' if view.get("summary") else "")
        + f'<div class="lanes">{sub_svg}</div></details>'
        for view, sub, sub_svg in views
    )

    page = (ASSETS / "page.html").read_text(encoding="utf-8")
    page = (
        page.replace("__CSS__", css)
        .replace("__TITLE__", html.escape(spec["title"]))
        .replace("__LEDE__", html.escape(spec.get("lede", "")))
        .replace("__COUNTS__", tally(spec))
        .replace("__SVG__", svg)
        .replace("__VIEWS__", drill)
    )
    pathlib.Path(out_html).write_text(page, encoding="utf-8")
    if out_svg:
        base = pathlib.Path(out_svg)
        base.write_text(svg, encoding="utf-8")
        for view, sub, sub_svg in views:
            side = base.with_name(f'{base.stem}.{view["id"]}{base.suffix}')
            side.write_text(sub_svg, encoding="utf-8")

    deltas = sum(1 for c in spec["cards"] if c.get("delta"))
    links = sum(len(c["refs"]) for c in spec["cards"])
    print(f"wrote {out_html}: {len(spec['lanes'])} lanes, {len(spec['cards'])} cards "
          f"({deltas} with a delta), {len(spec['edges'])} edges, {links} file links, "
          f"{geo['w']:.0f}x{geo['h']:.0f}"
          + (f" at scale {scale}" if scale != 1.0 else "")
          + (f", and {out_svg}" if out_svg else ""))
    for view, sub, sub_svg in views:
        print(f"  view {view['id']}: {len(sub['cards'])} cards, {len(sub['lanes'])} lanes, "
              f"{len(sub['edges'])} edges")


def demo():
    import copy
    import xml.etree.ElementTree as ET

    good = {
        "schemaVersion": SCHEMA_VERSION, "title": "demo", "lede": "",
        "lanes": [{"id": "a", "label": "A", "source": "https://host/{path}#L{line}"},
                  {"id": "b", "label": "B"}],
        "cards": [
            {"id": "c1", "lane": "a", "col": 0, "title": "+ new card", "kind": "query",
             "fields": ["+ added", "~ touched", "- gone", "untouched"],
             "files": ["src/deep/thing.sql:42", "src/other.sql"]},
            {"id": "c2", "lane": "a", "col": 1, "title": "sink", "fields": ["one"]},
            {"id": "c3", "lane": "b", "col": 0, "title": "plain", "kind": "table", "fields": ["two"]},
        ],
        "edges": [["c1", "c2", "in lane"], ["c2", "c3", "", "hero"], ["c1", "c3", "", "muted"]],
        "walkthrough": [
            {"heading": "First", "body": "c1 feeds c2.", "cards": ["c1", "c2"]},
            {"heading": "Second", "body": "c2 reaches c3.", "cards": ["c2", "c3"]},
        ],
    }
    assert validate(good) == [], validate(good)

    # Every rejection the contract promises.
    def broken(mutate):
        spec = copy.deepcopy(good)
        mutate(spec)
        return validate(spec)

    assert any("schemaVersion" in p for p in broken(lambda s: s.pop("schemaVersion")))
    assert any("not major" in p for p in broken(lambda s: s.update(schemaVersion="9.0.0")))
    assert any("unknown key" in p for p in broken(lambda s: s.update(colour="red")))
    assert any("unknown lane" in p for p in broken(lambda s: s["cards"][0].update(lane="zz")))
    assert any("duplicate card id" in p for p in broken(lambda s: s["cards"].append(dict(s["cards"][0]))))
    assert any("kind" in p for p in broken(lambda s: s["cards"][1].update(kind="banana")))
    assert any("emphasis" in p for p in broken(lambda s: s["edges"][1].__setitem__(3, "loud")))
    assert any("unknown card" in p for p in broken(lambda s: s["edges"][0].__setitem__(1, "nope")))
    assert any("no source" in p for p in broken(lambda s: s["cards"][2].update(files=["x.py"])))
    assert any("{path}" in p for p in broken(lambda s: s["lanes"][0].update(source="https://host/")))
    assert any("2 to 12 steps" in p for p in broken(lambda s: s.update(walkthrough=[s["walkthrough"][0]])))
    assert any("unknown card" in p for p in broken(lambda s: s["walkthrough"][0].update(cards=["ghost"])))
    assert any("heading" in p for p in broken(lambda s: s["walkthrough"][0].update(body="")))
    assert any("names no cards" in p for p in broken(lambda s: s["walkthrough"][1].update(cards=[])))
    assert any("is not an edge" in p for p in broken(lambda s: s["walkthrough"][0].update(routes=["c1>c9"])))
    assert any("unknown key" in p for p in broken(lambda s: s["walkthrough"][0].update(focus=["c1"])))

    spec = copy.deepcopy(good)
    normalize(spec)
    assert spec["cards"][0]["delta"] == "new"
    assert spec["cards"][0]["title"]["text"] == "new card"
    assert spec["cards"][1].get("delta") is None
    assert [f.get("delta") for f in spec["cards"][0]["fields"]] == ["new", "changed", "removed", None]
    assert split_delta("-- not a marker")["text"] == "-- not a marker"
    assert spec["cards"][0]["glyph"] == "SQL"
    refs = spec["cards"][0]["refs"]
    assert refs[0] == {"path": "src/deep/thing.sql", "line": 42, "name": "thing.sql",
                       "href": "https://host/src/deep/thing.sql#L42"}
    assert refs[1]["href"] == "https://host/src/other.sql#L1"
    assert [e[3] for e in spec["edges"]] == ["normal", "hero", "muted"]

    assert text_width("abcd", 10) == 4 * 10 * MONO
    assert wrap_px("aaa bbb ccc", 10, text_width("aaa bbb", 10)) == ["aaa bbb", "ccc"]
    assert split_long("short", 10, 500) == ["short"]
    assert split_long("a_b_c_d", 10, text_width("a_b_", 10)) == ["a_b_", "c_d"]
    assert wrap_px("lims_connect/src/x.py", 10, text_width("lims_connect/", 10)) == ["lims_connect/", "src/x.py"]
    assert fit_text("abc", 10, 100) == ("abc", text_width("abc", 10))
    assert fit_text("abcdefghij", 10, 40)[0].endswith("..."), "a hard squeeze is cut, not crushed"
    assert fit_text("abcdefghij", 10, 50) == ("abcdefghij", 50), "a slight overflow is squeezed"

    geo = layout(spec)
    # The in-lane edge puts its target on a lower row, and every route runs down.
    assert spec["cards"][0]["rank"] == 0 and spec["cards"][1]["rank"] == 1
    assert spec["cards"][1]["cy"] > spec["cards"][0]["cy"]
    for r in geo["routes"]:
        assert r["y2"] > r["y1"], "a route must arrive below where it left"
        assert r["length"] > 0
    for c in spec["cards"]:
        lane = next(l for l in spec["lanes"] if l["id"] == c["lane"])
        assert lane["y"] <= c["cy"] and c["cy"] + c["h"] <= lane["y"] + lane["h"]

    # The stylesheet is inlined into the SVG's own <style>, so anything that
    # parses as a tag in it breaks the document. A comment mentioning a tag
    # name is the easy way to do that by accident.
    sheet = (ASSETS / "diagram.css").read_text(encoding="utf-8")
    assert not re.search(r"<[A-Za-z/!]", sheet), "diagram.css contains tag-like text"

    svg = render_svg(spec, geo, sheet)
    root = ET.fromstring(svg)
    ns, xlink = "{http://www.w3.org/2000/svg}", "{http://www.w3.org/1999/xlink}"
    assert root.tag == ns + "svg"
    assert "<script" not in svg
    links = [a.get("href") or a.get(xlink + "href") for a in root.iter(ns + "a")]
    files = [l for l in links if l and l.startswith("http")]
    assert files == ["https://host/src/deep/thing.sql#L42", "https://host/src/other.sql#L1"]
    # The muted route draws but does not pulse.
    assert sum(1 for _ in root.iter(ns + "animateMotion")) == 2
    # Draw order: lanes, pulses, edges, cards. A pulse over a route chip hides
    # the label it is crossing, so the pulses go under the edge group.
    top = [g for g in root if g.tag == ns + "g"]
    kinds = ["".join(sorted({(x.get("class") or "").split(" ")[0] for x in g.iter() if x.get("class")}))
             for g in top]
    order = [i for i, k in enumerate(kinds) if "pulse" in k or "route" in k]
    assert len(order) >= 2 and "pulse" in kinds[order[0]] and "route" in kinds[order[1]], kinds
    assert sum(1 for p in root.iter(ns + "path") if "route-hero" in (p.get("class") or "")) == 1
    assert sum(1 for t in root.iter(ns + "text") if t.get("class") == "glyph-label") == 2

    # A wrapped title makes the header taller; the fields have to start below
    # it, or the first line lands on top of the title's second line.
    for card in (g for g in root.iter(ns + "g") if g.get("class") == "card"):
        head = next(r for r in card if r.get("class") == "head")
        first = next((x for x in card if x.get("class") == "card-field"), None)
        if first is None:
            continue
        top, tall = float(head.get("y")), float(head.get("height"))
        assert float(first.get("y")) > top + tall, "a field line sits inside the header"

    # Step 1 lights c1, c2 and the route between them; nothing else.
    step = spec["walkthrough"][0]
    assert step["focus_cards"] == {"c1", "c2"} and step["focus_routes"] == {("c1", "c2")}
    by_id = {c["id"]: c for c in spec["cards"]}
    assert [g.get("data-step") for g in root.iter(ns + "g") if g.get("class") == "card"] == ["1", "1 2", "2"]
    assert sum(1 for a in root.iter(ns + "a") if a.get("href", "").startswith("#vfs")) == 2
    rules = step_css(spec["walkthrough"], spec["cards"], geo["routes"])
    assert ":has(" not in rules
    # c3 is outside step 1, so step 1 must name its id in the dim list.
    c3 = next(c for c in spec["cards"] if c["id"] == "c3")
    assert f'#vfs1:target ~ g #{c3["vfid"]}' in rules
    assert ":not(" not in rules, "id-keyed dim lists repaint on a hash change; class-keyed ones did not"
    assert "<script" not in rules

    # A card no step lights is worth saying, and never a reason to refuse.
    assert warnings(good) == []
    lonely = copy.deepcopy(good)
    lonely["walkthrough"][1]["cards"] = ["c2"]
    note = warnings(lonely)
    assert len(note) == 1 and "c3" in note[0] and "1 of 3 cards" in note[0]
    assert validate(lonely) == [], "a coverage gap must not block the build"
    assert warnings({"cards": good["cards"]}) == [], "no walkthrough, nothing to say"

    # A view is scoped, re-columned, and laid out on its own.
    viewed = copy.deepcopy(good)
    viewed["views"] = [{"id": "spine", "title": "Just the spine", "cards": ["c1", "c3"]}]
    assert validate(viewed) == []
    sub = scoped(viewed, viewed["views"][0])
    assert [c["id"] for c in sub["cards"]] == ["c1", "c3"]
    assert [c["col"] for c in sub["cards"]] == [0, 0], "columns close up around what is left"
    assert [(e[0], e[1]) for e in sub["edges"]] == [("c1", "c3")], "an edge reaching outside the view is dropped"
    assert [l["id"] for l in sub["lanes"]] == ["a", "b"]
    assert "walkthrough" not in sub and "views" not in sub
    normalize(sub)
    sub_geo = layout(sub)
    assert sub_geo["w"] < geo["w"], "a scoped view is narrower than the whole diagram"
    assert "<script" not in render_svg(sub, sub_geo, sheet)

    broken_view = copy.deepcopy(viewed)
    broken_view["views"][0]["cards"] = ["ghost"]
    assert any("unknown card" in x for x in validate(broken_view))
    empty_view = copy.deepcopy(viewed)
    empty_view["views"][0]["cards"] = []
    assert any("scopes to no cards" in x for x in validate(empty_view))
    dupe = copy.deepcopy(viewed)
    dupe["views"].append(dict(viewed["views"][0]))
    assert any("duplicate view id" in x for x in validate(dupe))

    counts = tally(spec)
    assert "1 new cards" in counts and "2 linked files" in counts
    print("ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--demo"]:
        demo()
        sys.exit()
    scale = 1.0
    if "--pr" in args:
        args.remove("--pr")
        scale = PR_SCALE
    if "--scale" in args:
        i = args.index("--scale")
        scale = float(args[i + 1])
        del args[i:i + 2]
    if len(args) not in (2, 3):
        sys.exit(__doc__)
    build(*args, scale=scale)
