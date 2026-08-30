#!/usr/bin/env python3
"""Create a concise Markdown report from persisted per-paper build logs."""
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "ROUND3_BUILD_SUMMARY.json"
OUTPUT = ROOT / "ROUND3_BUILD_FAILURES.md"
MARKER = re.compile(
    r"(^! |LaTeX Error:|Package .* Error:|Undefined control sequence|"
    r"Emergency stop|Fatal error|^.*\.tex:\d+:|There were undefined references|"
    r"There were undefined citations|Citation .* undefined|Reference .* undefined)",
    re.IGNORECASE,
)


def extract(text: str, radius: int = 7, limit: int = 6) -> list[str]:
    lines = text.splitlines()
    hits = [i for i, line in enumerate(lines) if MARKER.search(line)]
    if not hits:
        return ["\n".join(lines[-60:])]
    blocks: list[str] = []
    last_hi = -1
    for index in hits:
        lo = max(0, index - radius)
        hi = min(len(lines), index + radius + 1)
        if lo <= last_hi:
            continue
        blocks.append("\n".join(lines[lo:hi]))
        last_hi = hi
        if len(blocks) >= limit:
            break
    return blocks


def main() -> None:
    if not SUMMARY.is_file():
        OUTPUT.write_text("# Round-three build failures\n\nBuild summary was not produced.\n", encoding="utf-8")
        return
    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    out = [
        "# Round-three build failures",
        "",
        f"- Overall status: **{data.get('status', 'UNKNOWN')}**",
        f"- Passed: **{data.get('passed', 0)}/11**",
        f"- Failed papers: `{', '.join(data.get('failed', [])) or 'none'}`",
        "",
    ]
    for name in data.get("failed", []):
        item = data.get("papers", {}).get(name, {})
        log = ROOT / str(item.get("log", ""))
        out.extend([f"## {name}", "", f"Return code: `{item.get('returncode')}`", ""])
        if not log.is_file():
            out.extend(["No persisted log was found.", ""])
            continue
        text = log.read_text(encoding="utf-8", errors="replace")
        for block in extract(text):
            out.extend(["```text", block, "```", ""])
    OUTPUT.write_text("\n".join(out), encoding="utf-8")
    print(f"ROUND3_BUILD_FAILURE_REPORT_WRITTEN {OUTPUT}")


if __name__ == "__main__":
    main()
