#!/usr/bin/env node
// Global PostToolUse hook: strip em dashes (U+2014) from any file written via Write/Edit.
// Reads the hook payload JSON on stdin, finds the edited file, replaces every em dash with a
// hyphen, and writes it back. Designed to never fail the originating tool.
import { readFileSync, writeFileSync, existsSync, statSync } from "node:fs";

let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  try {
    const payload = JSON.parse(input || "{}");
    const file =
      (payload.tool_input && payload.tool_input.file_path) ||
      (payload.tool_response && payload.tool_response.filePath);
    if (!file || !existsSync(file)) return;

    const stat = statSync(file);
    if (!stat.isFile() || stat.size > 5_000_000) return; // skip dirs and huge files

    const original = readFileSync(file, "utf8");
    if (original.includes("\0")) return; // skip binary

    const cleaned = original.split("—").join("-");
    if (cleaned !== original) writeFileSync(file, cleaned);
  } catch {
    // Never block or fail the tool that triggered this hook.
  }
});
