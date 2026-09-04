#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SCHEMA = JSON.parse(
  readFileSync(resolve(HERE, "../schema/schema.json"), "utf8"),
);

export const DELTA = {
  new: { fill: "#e8f6ee", stroke: "#6fbe86", ink: "#3d8f58" },
  changed: { fill: "#fff6df", stroke: "#d2b36a", ink: "#9a7a2e" },
  removed: { fill: "#fdeeee", stroke: "#d48a8a", ink: "#b15a5a" },
  unchanged: { fill: "#f4f6f8", stroke: "#a8b3be", ink: "#6b7682" },
};

const FLOW_COLOR = "#7eb8a0";
export const EDGE_STROKE = 1.8;
const CHEVRON_COUNT = 2;
const PAD = 24;
const TITLE_H = 36;
const HEADER_H = 34;
const COL_PAD = 16;
const COL_GAP = 28;
const CARD_W = 200;
const CARD_H = 96;
const CARD_GAP_Y = 18;
const BADGE = { new: "NEW", changed: "CHANGED", removed: "REMOVED" };

function escapeXml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function typeOf(value) {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value;
}

function resolveRef(schema, root) {
  if (!schema || !schema.$ref) return schema;
  const path = schema.$ref;
  if (!path.startsWith("#/")) {
    throw new Error(`unsupported $ref: ${path}`);
  }
  let cur = root;
  for (const part of path.slice(2).split("/")) {
    cur = cur?.[part];
  }
  if (!cur) throw new Error(`unresolved $ref: ${path}`);
  return cur;
}

function validateSchema(schema, value, path, root, errors) {
  const node = resolveRef(schema, root);
  if (Object.hasOwn(node, "const") && value !== node.const) {
    errors.push(`${path}: expected ${JSON.stringify(node.const)}`);
    return;
  }
  const actual = typeOf(value);
  if (node.type === "integer") {
    if (!Number.isInteger(value)) {
      errors.push(`${path}: expected integer`);
      return;
    }
  } else if (node.type && actual !== node.type) {
    errors.push(`${path}: expected ${node.type}`);
    return;
  }
  if (node.enum && !node.enum.includes(value)) {
    errors.push(`${path}: expected one of ${node.enum.join(", ")}`);
  }
  if (node.pattern && typeof value === "string" && !new RegExp(node.pattern).test(value)) {
    errors.push(`${path}: does not match ${node.pattern}`);
  }
  if (typeof value === "string" && node.minLength && value.length < node.minLength) {
    errors.push(`${path}: shorter than ${node.minLength}`);
  }
  if (typeof value === "number" && node.minimum != null && value < node.minimum) {
    errors.push(`${path}: below ${node.minimum}`);
  }
  if (node.type === "array") {
    if (node.minItems && value.length < node.minItems) {
      errors.push(`${path}: fewer than ${node.minItems} items`);
    }
    value.forEach((item, i) => {
      validateSchema(node.items, item, `${path}[${i}]`, root, errors);
    });
    return;
  }
  if (node.type !== "object" || typeOf(value) !== "object") return;
  const required = node.required || [];
  for (const key of required) {
    if (value[key] === undefined) errors.push(`${path}: missing ${key}`);
  }
  const props = node.properties || {};
  for (const [key, child] of Object.entries(value)) {
    if (!props[key]) {
      if (node.additionalProperties === false) {
        errors.push(`${path}: unexpected ${key}`);
      }
      continue;
    }
    validateSchema(props[key], child, `${path}.${key}`, root, errors);
  }
}

export function validate(doc) {
  const errors = [];
  validateSchema(SCHEMA, doc, "$", SCHEMA, errors);
  if (errors.length) return errors;
  if (!doc.lenses.includes("architecture")) {
    errors.push("lenses: architecture is required");
  }
  if (new Set(doc.lenses).size !== doc.lenses.length) {
    errors.push("lenses: duplicate entry");
  }
  const lanes = new Map(doc.lanes.map((lane) => [lane.id, lane]));
  if (lanes.size !== doc.lanes.length) errors.push("duplicate lane id");
  const nodes = new Map(doc.nodes.map((node) => [node.id, node]));
  if (nodes.size !== doc.nodes.length) errors.push("duplicate node id");
  for (const node of doc.nodes) {
    if (!lanes.has(node.lane)) errors.push(`node ${node.id}: unknown lane ${node.lane}`);
    if (node.evidence === "fact" && !String(node.cite || "").trim()) {
      errors.push(`node ${node.id}: fact requires cite`);
    }
  }
  for (const [i, edge] of doc.edges.entries()) {
    if (!nodes.has(edge.from)) errors.push(`edges[${i}]: unknown from ${edge.from}`);
    if (!nodes.has(edge.to)) errors.push(`edges[${i}]: unknown to ${edge.to}`);
    if (edge.evidence === "fact" && !String(edge.cite || "").trim()) {
      errors.push(`edges[${i}]: fact requires cite`);
    }
  }
  const flows = doc.flows || [];
  if (doc.lenses.includes("data-flow") && flows.length < 1) {
    errors.push("flows: data-flow lens requires at least one flow");
  }
  const views = doc.views || [];
  const viewIds = new Set();
  for (const view of views) {
    if (viewIds.has(view.id)) errors.push(`duplicate view id ${view.id}`);
    viewIds.add(view.id);
    for (const [i, nodeId] of view.nodeIds.entries()) {
      if (!nodes.has(nodeId)) {
        errors.push(`view ${view.id} nodeIds[${i}]: unknown ${nodeId}`);
      }
    }
  }
  const flowIds = new Set();
  for (const flow of flows) {
    if (flowIds.has(flow.id)) errors.push(`duplicate flow id ${flow.id}`);
    flowIds.add(flow.id);
    for (const [i, step] of flow.steps.entries()) {
      if (!nodes.has(step.from)) {
        errors.push(`flow ${flow.id} step ${i}: unknown from ${step.from}`);
      }
      if (!nodes.has(step.to)) {
        errors.push(`flow ${flow.id} step ${i}: unknown to ${step.to}`);
      }
    }
  }
  return errors;
}

function clip(text, max) {
  const value = String(text);
  return value.length <= max ? value : `${value.slice(0, max - 1)}…`;
}

function hasLens(doc, name) {
  return (doc.lenses || []).includes(name);
}

function layout(doc) {
  const byLane = new Map(doc.lanes.map((lane) => [lane.id, []]));
  for (const node of doc.nodes) {
    byLane.get(node.lane)?.push(node);
  }
  const colW = COL_PAD + CARD_W + COL_PAD;
  const rows = Math.max(1, ...[...byLane.values()].map((list) => list.length));
  const width = PAD + doc.lanes.length * colW + Math.max(0, doc.lanes.length - 1) * COL_GAP + PAD;
  const flowH = hasLens(doc, "data-flow") && (doc.flows || []).length ? 22 : 0;
  const viewH = (doc.views || []).length ? 8 + (doc.views || []).length * 16 : 0;
  const height = PAD + TITLE_H + HEADER_H + rows * (CARD_H + CARD_GAP_Y) + PAD + flowH + viewH;
  const cards = new Map();
  const columns = [];
  doc.lanes.forEach((lane, i) => {
    const x = PAD + i * (colW + COL_GAP);
    columns.push({ lane, x, width: colW });
    (byLane.get(lane.id) || []).forEach((node, row) => {
      const cx = x + COL_PAD;
      const cy = PAD + TITLE_H + HEADER_H + row * (CARD_H + CARD_GAP_Y);
      cards.set(node.id, {
        node,
        x: cx,
        y: cy,
        cx: cx + CARD_W / 2,
        cy: cy + CARD_H / 2,
        right: cx + CARD_W,
        left: cx,
      });
    });
  });
  return { width, height, cards, columns };
}

function cardPath(a, b) {
  const x1 = a.right;
  const y1 = a.cy;
  const x2 = b.left;
  const y2 = b.cy;
  const mid = (x1 + x2) / 2;
  return `M ${x1} ${y1} C ${mid} ${y1}, ${mid} ${y2}, ${x2} ${y2}`;
}

function flowPath(cards, steps) {
  const ids = [];
  for (const step of steps) {
    if (!ids.length) ids.push(step.from);
    ids.push(step.to);
  }
  const pts = ids.map((id) => cards.get(id)).filter(Boolean);
  if (pts.length < 2) return "";
  let d = `M ${pts[0].cx} ${pts[0].cy}`;
  for (let i = 1; i < pts.length; i += 1) {
    const prev = pts[i - 1];
    const cur = pts[i];
    const midX = (prev.cx + cur.cx) / 2;
    d += ` C ${midX} ${prev.cy}, ${midX} ${cur.cy}, ${cur.cx} ${cur.cy}`;
  }
  return d;
}

function cubicPoint(p0, p1, p2, p3, t) {
  const u = 1 - t;
  return {
    x: u * u * u * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t * t * t * p3.x,
    y: u * u * u * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t * t * t * p3.y,
  };
}

function cubicTan(p0, p1, p2, p3, t) {
  const u = 1 - t;
  return {
    x: 3 * u * u * (p1.x - p0.x) + 6 * u * t * (p2.x - p1.x) + 3 * t * t * (p3.x - p2.x),
    y: 3 * u * u * (p1.y - p0.y) + 6 * u * t * (p2.y - p1.y) + 3 * t * t * (p3.y - p2.y),
  };
}

function controlPoints(a, b) {
  const mid = (a.right + b.left) / 2;
  return [
    { x: a.right, y: a.cy },
    { x: mid, y: a.cy },
    { x: mid, y: b.cy },
    { x: b.left, y: b.cy },
  ];
}

function chevronAt(x, y, angle, color, pulse, delay) {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  const half = EDGE_STROKE / 2;
  const along = EDGE_STROKE * 2.2;
  const map = (lx, ly) => `${x + lx * c - ly * s},${y + lx * s + ly * c}`;
  const anim = pulse
    ? `<animate attributeName="opacity" values="0.35;1;0.35" dur="1.4s" begin="${delay}s" repeatCount="indefinite"/>`
    : "";
  return `<polyline class="chevron" points="${map(-along, -half)} ${map(along * 0.35, 0)} ${map(-along, half)}" fill="none" stroke="${color}" stroke-width="${EDGE_STROKE}" stroke-linecap="butt" stroke-linejoin="miter">${anim}</polyline>`;
}

function cubicSamples(p0, p1, p2, p3, steps = 32) {
  const samples = [{ t: 0, s: 0, p: p0 }];
  let prev = p0;
  let acc = 0;
  for (let i = 1; i <= steps; i += 1) {
    const t = i / steps;
    const p = cubicPoint(p0, p1, p2, p3, t);
    acc += Math.hypot(p.x - prev.x, p.y - prev.y);
    samples.push({ t, s: acc, p });
    prev = p;
  }
  return samples;
}

function tAtLength(samples, target) {
  for (let i = 1; i < samples.length; i += 1) {
    if (samples[i].s >= target) {
      const a = samples[i - 1];
      const b = samples[i];
      const span = b.s - a.s || 1;
      return a.t + ((target - a.s) / span) * (b.t - a.t);
    }
  }
  return 1;
}

function edgeChevrons(a, b, stroke, light, pulse) {
  const [p0, p1, p2, p3] = controlPoints(a, b);
  const samples = cubicSamples(p0, p1, p2, p3);
  const total = samples[samples.length - 1].s;
  const gap = total / (CHEVRON_COUNT + 1);
  const marks = [];
  for (let i = 1; i <= CHEVRON_COUNT; i += 1) {
    const t = tAtLength(samples, gap * i);
    const p = cubicPoint(p0, p1, p2, p3, t);
    const d = cubicTan(p0, p1, p2, p3, t);
    const color = i % 2 === 0 ? light : stroke;
    marks.push(chevronAt(p.x, p.y, Math.atan2(d.y, d.x), color, pulse, (i - 1) * 0.28));
  }
  return marks.join("\n");
}

function mixHex(hex, toward, amount) {
  const parse = (value) => [
    parseInt(value.slice(1, 3), 16),
    parseInt(value.slice(3, 5), 16),
    parseInt(value.slice(5, 7), 16),
  ];
  const a = parse(hex);
  const b = parse(toward);
  const ch = a.map((n, i) => Math.round(n + (b[i] - n) * amount));
  return `#${ch.map((n) => n.toString(16).padStart(2, "0")).join("")}`;
}

function laneColumn(column, height) {
  const { lane, x, width } = column;
  const top = PAD + TITLE_H;
  const bandH = height - top - PAD;
  return `<g class="lane" data-lane="${escapeXml(lane.id)}">
  <rect class="lane-band" x="${x}" y="${top}" width="${width}" height="${bandH}" rx="12" fill="var(--lane-a)"/>
  <text class="lane-header" x="${x + 14}" y="${top + 22}">${escapeXml(lane.label)}</text>
</g>`;
}

function card(box, views) {
  const { node, x, y } = box;
  const colors = DELTA[node.delta];
  const removed = node.delta === "removed";
  const dash = removed ? ' stroke-dasharray="5 4"' : "";
  const ghost = removed ? ' opacity="0.55"' : "";
  const strike = removed ? ' text-decoration="line-through"' : "";
  const subtitle = node.subtitle || node.kind || "";
  const cite = node.cite ? clip(node.cite, 28) : "";
  const viewIds = views
    .filter((view) => view.nodeIds.includes(node.id))
    .map((view) => view.id)
    .join(" ");
  const viewAttr = viewIds ? ` data-view="${escapeXml(viewIds)}"` : "";
  const badge = BADGE[node.delta]
    ? `<g class="delta-badge" data-badge="${node.delta}">
  <rect x="${x + CARD_W - 78}" y="${y + 8}" width="70" height="16" rx="8" fill="${colors.fill}" stroke="${colors.stroke}"/>
  <text class="badge-text" x="${x + CARD_W - 43}" y="${y + 20}" fill="${colors.ink}">${BADGE[node.delta]}</text>
</g>`
    : "";
  return `<g class="card" data-node="${escapeXml(node.id)}" data-delta="${node.delta}"${viewAttr}${ghost}>
  <rect class="card-body" x="${x}" y="${y}" width="${CARD_W}" height="${CARD_H}" rx="10" fill="${colors.fill}" stroke="${colors.stroke}" stroke-width="1.2"${dash}/>
  <rect class="card-accent" x="${x}" y="${y}" width="5" height="${CARD_H}" rx="3" fill="${colors.stroke}"/>
  ${badge}
  <text class="card-title" x="${x + 16}" y="${y + 42}"${strike}>${escapeXml(clip(node.label, 18))}</text>
  ${subtitle ? `<text class="card-meta" x="${x + 16}" y="${y + 62}">${escapeXml(clip(subtitle, 22))}</text>` : ""}
  ${cite ? `<text class="card-cite" x="${x + 16}" y="${y + 80}">${escapeXml(cite)}</text>` : ""}
</g>`;
}

export function renderSvg(doc) {
  const errors = validate(doc);
  if (errors.length) {
    const err = new Error(errors.join("\n"));
    err.errors = errors;
    throw err;
  }
  const { width, height, cards, columns } = layout(doc);
  const lanes = columns.map((column) => laneColumn(column, height)).join("\n");
  const nodeCards = [...cards.values()].map((box) => card(box, doc.views || [])).join("\n");
  const chain = hasLens(doc, "data-flow") && (doc.flows || [])[0]
    ? (doc.flows[0].steps || []).map((step) => ({
        from: step.from,
        to: step.to,
        label: step.label,
        delta: (doc.edges.find((edge) => edge.from === step.from && edge.to === step.to) || {}).delta || "unchanged",
        evidence: (doc.edges.find((edge) => edge.from === step.from && edge.to === step.to) || {}).evidence,
      }))
    : doc.edges;
  const nHops = Math.max(1, chain.length);
  const hopDur = 1.5;
  const cycle = nHops * hopDur;
  const edges = chain
    .map((edge, hop) => {
      const a = cards.get(edge.from);
      const b = cards.get(edge.to);
      if (!a || !b) return "";
      const delta = edge.delta || "unchanged";
      const stroke = DELTA[delta]?.stroke || "#a8b3be";
      const light = mixHex(stroke, "#ffffff", 0.45);
      const dash = delta === "removed" || edge.evidence === "assumption" ? ' stroke-dasharray="3 5"' : "";
      const label = edge.label
        ? `<text class="edge-label" x="${(a.right + b.left) / 2}" y="${(a.cy + b.cy) / 2 - 10}">${escapeXml(edge.label)}</text>`
        : "";
      const pulse = hasLens(doc, "data-flow") && delta === "new";
      return `<g class="edge" data-from="${escapeXml(edge.from)}" data-to="${escapeXml(edge.to)}" data-order="${hop + 1}">
  <path class="flow-route" d="${cardPath(a, b)}" fill="none" stroke="${stroke}" stroke-width="${EDGE_STROKE}"${dash}/>
  ${edgeChevrons(a, b, stroke, light, pulse)}
  ${label}
</g>`;
    })
    .join("\n");
  const spine = hasLens(doc, "data-flow") && (doc.flows || [])[0]
    ? flowPath(cards, doc.flows[0].steps)
    : "";
  const flows = spine
    ? `<g class="flow" data-flow="${escapeXml(doc.flows[0].id)}">
  <path id="flow-${doc.flows[0].id}" class="flow-spine" d="${spine}" fill="none" stroke="${FLOW_COLOR}" stroke-width="0.8" stroke-opacity="0.35"/>
  <polyline class="flow-token chevron" points="${-EDGE_STROKE * 2.2},${-EDGE_STROKE / 2} ${EDGE_STROKE * 0.77},0 ${-EDGE_STROKE * 2.2},${EDGE_STROKE / 2}" fill="none" stroke="${FLOW_COLOR}" stroke-width="${EDGE_STROKE}" stroke-linecap="butt" stroke-linejoin="miter">
    <animateMotion dur="${cycle}s" repeatCount="indefinite" rotate="auto" path="${spine}"/>
  </polyline>
  <text class="flow-caption" x="${PAD}" y="${height - 14 - (doc.views || []).length * 16}">${escapeXml(doc.flows[0].label || "data-flow")}</text>
</g>`
    : "";
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" role="img">
  <title>${escapeXml(doc.title)}</title>
  <desc>Blast-radius lanes and ordered data-flow for ${escapeXml(doc.title)}</desc>
  <style>
    :root { --bg: #fff; --ink: #0f172a; --muted: #334155; --lane-a: #f1f5f9; --lane-b: #e2e8f0; }
    @media (prefers-color-scheme: dark) {
      :root { --bg: #0f172a; --ink: #e2e8f0; --muted: #cbd5e1; --lane-a: #1e293b; --lane-b: #334155; }
    }
    .title { font: 700 18px ui-sans-serif, system-ui, sans-serif; fill: var(--ink); }
    .lane-header { font: 700 11px ui-sans-serif, system-ui, sans-serif; fill: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
    .card-meta, .card-cite, .edge-label, .flow-caption { font: 12px ui-sans-serif, system-ui, sans-serif; fill: var(--muted); }
    .card-title { font: 700 14px ui-sans-serif, system-ui, sans-serif; fill: var(--ink); }
    .badge-text { font: 700 9px ui-sans-serif, system-ui, sans-serif; text-anchor: middle; }
  </style>
  <rect width="${width}" height="${height}" fill="var(--bg)"/>
  <text class="title" x="${PAD}" y="${PAD + 18}">${escapeXml(doc.title)}</text>
  ${lanes}
  ${edges}
  ${flows}
  ${nodeCards}
  ${(doc.views || [])
    .map((view, i) => {
      const y = height - 12 - ((doc.views || []).length - 1 - i) * 16;
      return `<g class="view" data-view="${escapeXml(view.id)}">
  <text class="flow-caption" x="${PAD}" y="${y}">View: ${escapeXml(view.title)}</text>
</g>`;
    })
    .join("\n")}
</svg>
`;
}

function main(argv) {
  const input = argv[0];
  const output = argv[1];
  if (!input) {
    console.error("usage: render.mjs <document.json> [output.svg]");
    process.exit(2);
  }
  const doc = JSON.parse(readFileSync(resolve(input), "utf8"));
  const errors = validate(doc);
  if (errors.length) {
    for (const error of errors) console.error(error);
    process.exit(1);
  }
  const svg = renderSvg(doc);
  if (output) writeFileSync(resolve(output), svg, "utf8");
  else process.stdout.write(svg);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2));
}
