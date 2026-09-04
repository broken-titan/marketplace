#!/usr/bin/env node
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import { DELTA, EDGE_STROKE, renderSvg, validate } from "./render.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const fixture = JSON.parse(
  readFileSync(resolve(HERE, "fixtures/tiny.json"), "utf8"),
);

test("tiny fixture is schema-valid", () => {
  assert.deepEqual(validate(fixture), []);
});

test("renderer emits lanes, cards, delta colors, and SMIL", () => {
  const svg = renderSvg(fixture);
  assert.match(svg, /<svg xmlns="http:\/\/www.w3.org\/2000\/svg"/);
  assert.match(svg, /data-lane="edge"/);
  assert.match(svg, /data-lane="app"/);
  assert.match(svg, /data-lane="store"/);
  assert.match(svg, /class="lane-header"[^>]*>Edge</);
  assert.match(svg, /class="card"/);
  assert.match(svg, /data-badge="new"/);
  assert.match(svg, /data-badge="changed"/);
  assert.match(svg, /data-badge="removed"/);
  assert.match(svg, />NEW</);
  assert.match(svg, />CHANGED</);
  assert.match(svg, />REMOVED</);
  assert.match(svg, /text-decoration="line-through"/);
  assert.match(svg, new RegExp(DELTA.new.fill));
  assert.match(svg, new RegExp(DELTA.changed.fill));
  assert.match(svg, new RegExp(DELTA.removed.fill));
  assert.match(svg, /<animateMotion /);
  assert.match(svg, /class="flow-route"/);
  assert.match(svg, /class="chevron"/);
  assert.match(svg, new RegExp(`stroke-width="${EDGE_STROKE}"`));
  for (const block of svg.matchAll(/<g class="edge"[^>]*>[\s\S]*?<\/g>/g)) {
    const marks = [...block[0].matchAll(/<polyline class="chevron" points="([^"]+)"/g)];
    assert.equal(marks.length, 2);
    assert.equal([...block[0].matchAll(new RegExp(`stroke-width="${EDGE_STROKE}"`, "g"))].length, 3);
    const xs = [];
    for (const mark of marks) {
      const pts = mark[1].split(/\s+/).map((pair) => pair.split(",").map(Number));
      const ys = pts.map((pt) => pt[1]);
      assert.ok(Math.abs(Math.max(...ys) - Math.min(...ys) - EDGE_STROKE) < 0.05);
      xs.push(pts[1][0]);
    }
    const path = block[0].match(/class="flow-route" d="M ([-\d.]+) ([-\d.]+) C[^,]*,[^,]*, ([-\d.]+) /);
    assert.ok(path);
    const start = Number(path[1]);
    const end = Number(path[3]);
    const marksX = xs.slice().sort((a, b) => a - b);
    const stations = [start, ...marksX, end];
    const gaps = stations.slice(1).map((x, i) => x - stations[i]);
    const mean = gaps.reduce((sum, g) => sum + g, 0) / gaps.length;
    for (const gap of gaps) assert.ok(Math.abs(gap - mean) < 1.5);
  }
  assert.match(svg, /prefers-color-scheme: dark/);
  assert.match(svg, /data-view="writePath"/);
  assert.match(svg, /class="view"/);
  assert.doesNotMatch(svg, /data-legend=/);
  assert.doesNotMatch(svg, /class="flow-num"/);
  assert.doesNotMatch(svg, / · fact/);
  assert.doesNotMatch(svg, /mermaid/i);
  assert.doesNotMatch(svg, /marker-end/);
  assert.doesNotMatch(svg, /class="flow-arrow"/);
  assert.doesNotMatch(svg, /stroke-width="2\.4"/);
  assert.doesNotMatch(svg, /stroke-width="4"/);
});

test("view nodeIds must exist", () => {
  const bad = structuredClone(fixture);
  bad.views[0].nodeIds.push("missing");
  assert.ok(validate(bad).some((error) => error.includes("unknown missing")));
});

test("fact without cite is rejected", () => {
  const bad = structuredClone(fixture);
  delete bad.nodes[0].cite;
  assert.ok(validate(bad).some((error) => error.includes("fact requires cite")));
});
