#!/usr/bin/env python3
"""Extract an auditable status map from large historical derivation documents.

GitHub's contents endpoint cannot return the multi-megabyte recursive volume,
but an Actions checkout with ``fetch-depth: 0`` contains the archived branch.
This program reads files materialized by ``git show``, records their exact
hashes, finds A1--A5/S1--S3 and referee-blocker vocabulary, and classifies only
the nearby *status language*.  It deliberately does not promote a historical
label to theorem credit; mathematical proof audit remains separate.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
from typing import Iterable

GATES = ["A1", "A2", "A3", "A4", "A5", "S1", "S2", "S3"]
BLOCKERS = {
    "source-dependent saddle": [r"source[- ]dependent", r"reoptimi[sz]", r"fixed[- ]saddle"],
    "vector/roof local limit": [r"vector.{0,20}roof", r"local[- ]limit", r"current.{0,20}clock"],
    "Young-code applicability": [r"Young tower", r"countable.{0,20}(shift|code)", r"finite primitiv"],
    "singularity shield": [r"singularit", r"shield", r"grazing"],
    "Palm/random clock": [r"Palm", r"random[- ]time", r"clock inversion", r"renewal"],
    "actual-contact recollision": [r"recollision", r"actual collision", r"contact measure"],
    "cotangent gauge": [r"gauge", r"coboundar", r"Delta p", r"representation kernel"],
    "nonlinear generator/comparison": [r"nonlinear generator", r"Hamilton.?Jacobi", r"comparison principle"],
    "control timing/Isaacs": [r"Isaacs", r"one[- ]time preparation", r"adaptive control"],
    "speed covariance normalization": [r"speed.{0,30}covariance", r"sqrt.{0,20}(speed|mu)", r"D\^?2.{0,20}Cov"],
}

POSITIVE = re.compile(
    r"\b(PROVED|PROOF|CLOSED|COMPLETE|PASS(?:ED)?|RESOLVED|ESTABLISHED|THEOREM)\b"
    r"|已证明|闭合|完成|通过",
    re.IGNORECASE,
)
NEGATIVE = re.compile(
    r"NO[_ -]?THEOREM[_ -]?CREDIT|NOT[_ -]?PROVED|UNPROVED|OPEN|PENDING|"
    r"CONDITIONAL|ASSUM(?:E|ED|PTION)|REQUIRED|MISSING|WITHDRAWN|REFUTED|GAP|"
    r"未证明|开放|待定|条件|缺失|撤回|反例|驳倒",
    re.IGNORECASE,
)
STRONG_NEGATIVE = re.compile(
    r"NO[_ -]?THEOREM[_ -]?CREDIT|NOT[_ -]?PROVED|UNPROVED|OPEN|PENDING|"
    r"WITHDRAWN|REFUTED|MISSING|GAP|未证明|开放|待定|缺失|撤回|反例|驳倒",
    re.IGNORECASE,
)
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")


def compact(text: str, limit: int = 520) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def status_of(context: str) -> str:
    positive = bool(POSITIVE.search(context))
    negative = bool(NEGATIVE.search(context))
    strong_negative = bool(STRONG_NEGATIVE.search(context))
    if strong_negative and positive:
        return "MIXED/CONFLICTING"
    if strong_negative:
        return "OPEN_OR_NEGATED"
    if negative and positive:
        return "CONDITIONAL_OR_ASSUMED"
    if negative:
        return "CONDITIONAL_OR_ASSUMED"
    if positive:
        return "POSITIVE_LANGUAGE"
    return "UNCLASSIFIED"


def heading_map(lines: list[str]) -> list[str]:
    current = "(document root)"
    result: list[str] = []
    for line in lines:
        match = HEADING.match(line)
        if match:
            current = compact(match.group(2), 180)
        result.append(current)
    return result


def contexts_for(patterns: Iterable[str], lines: list[str], headings: list[str], limit: int = 12):
    regex = re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)
    results = []
    for idx, line in enumerate(lines):
        if not regex.search(line):
            continue
        lo = max(0, idx - 2)
        hi = min(len(lines), idx + 3)
        context = " ".join(lines[lo:hi])
        results.append(
            {
                "line": idx + 1,
                "heading": headings[idx],
                "status": status_of(context),
                "excerpt": compact(context),
            }
        )
        if len(results) >= limit:
            break
    return results


def gate_patterns(gate: str) -> list[str]:
    # Avoid matching A1 inside a longer alphanumeric identifier.
    return [rf"(?<![A-Za-z0-9]){re.escape(gate)}(?![A-Za-z0-9])"]


def parse_source(spec: str) -> tuple[str, Path]:
    if "=" not in spec:
        raise argparse.ArgumentTypeError("source must be LABEL=PATH")
    label, raw_path = spec.split("=", 1)
    path = Path(raw_path)
    if not label or not path.is_file():
        raise argparse.ArgumentTypeError(f"invalid source: {spec}")
    return label, path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("sources", nargs="+", type=parse_source)
    args = parser.parse_args()

    source_data = []
    all_gate_rows: dict[str, list[dict[str, object]]] = {gate: [] for gate in GATES}
    all_blocker_rows: dict[str, list[dict[str, object]]] = {key: [] for key in BLOCKERS}

    for label, path in args.sources:
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        lines = text.splitlines()
        headings = heading_map(lines)
        source_data.append(
            {
                "label": label,
                "path": str(path),
                "bytes": len(raw),
                "lines": len(lines),
                "sha256": hashlib.sha256(raw).hexdigest(),
            }
        )
        for gate in GATES:
            matches = contexts_for(gate_patterns(gate), lines, headings, limit=20)
            for match in matches:
                match["source"] = label
            all_gate_rows[gate].extend(matches)
        for blocker, patterns in BLOCKERS.items():
            matches = contexts_for(patterns, lines, headings, limit=16)
            for match in matches:
                match["source"] = label
            all_blocker_rows[blocker].extend(matches)

    out: list[str] = []
    out.append("# Round-three historical derivation audit")
    out.append("")
    out.append("> This is an exact-text provenance and status-language audit. A historical")
    out.append("> occurrence of `PROVED`, `CLOSED`, or a gate label is not promoted to")
    out.append("> theorem credit unless the controlling manuscript contains the proof and")
    out.append("> its dependencies. Mixed, conditional, withdrawn, and no-credit language")
    out.append("> is reported fail-closed.")
    out.append("")
    out.append("## Exact sources")
    out.append("")
    out.append("| Label | Bytes | Lines | SHA-256 |")
    out.append("|---|---:|---:|---|")
    for item in source_data:
        out.append(
            f"| `{item['label']}` | {item['bytes']} | {item['lines']} | `{item['sha256']}` |"
        )
    out.append("")

    out.append("## A1--A5 / S1--S3 status-language map")
    out.append("")
    out.append("| Gate | Sampled matches | Positive | Conditional/assumed | Open/negated | Mixed |")
    out.append("|---|---:|---:|---:|---:|---:|")
    for gate, rows in all_gate_rows.items():
        counts = {key: 0 for key in (
            "POSITIVE_LANGUAGE", "CONDITIONAL_OR_ASSUMED", "OPEN_OR_NEGATED", "MIXED/CONFLICTING"
        )}
        for row in rows:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        out.append(
            f"| `{gate}` | {len(rows)} | {counts['POSITIVE_LANGUAGE']} | "
            f"{counts['CONDITIONAL_OR_ASSUMED']} | {counts['OPEN_OR_NEGATED']} | "
            f"{counts['MIXED/CONFLICTING']} |"
        )
    out.append("")

    for gate, rows in all_gate_rows.items():
        out.append(f"### {gate}")
        out.append("")
        if not rows:
            out.append("No exact token match was found in the audited sources.")
            out.append("")
            continue
        for row in rows[:12]:
            out.append(
                f"- `{row['source']}:L{row['line']}` — **{row['status']}** — "
                f"_{row['heading']}_ — {row['excerpt']}"
            )
        out.append("")

    out.append("## Referee-blocker vocabulary map")
    out.append("")
    out.append("| Blocker family | Sampled matches | Positive | Conditional/assumed | Open/negated | Mixed |")
    out.append("|---|---:|---:|---:|---:|---:|")
    for blocker, rows in all_blocker_rows.items():
        counts = {key: 0 for key in (
            "POSITIVE_LANGUAGE", "CONDITIONAL_OR_ASSUMED", "OPEN_OR_NEGATED", "MIXED/CONFLICTING"
        )}
        for row in rows:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        out.append(
            f"| {blocker} | {len(rows)} | {counts['POSITIVE_LANGUAGE']} | "
            f"{counts['CONDITIONAL_OR_ASSUMED']} | {counts['OPEN_OR_NEGATED']} | "
            f"{counts['MIXED/CONFLICTING']} |"
        )
    out.append("")

    for blocker, rows in all_blocker_rows.items():
        out.append(f"### {blocker}")
        out.append("")
        if not rows:
            out.append("No vocabulary match was found in the audited sources.")
            out.append("")
            continue
        for row in rows[:10]:
            out.append(
                f"- `{row['source']}:L{row['line']}` — **{row['status']}** — "
                f"_{row['heading']}_ — {row['excerpt']}"
            )
        out.append("")

    out.append("## Fail-closed interpretation rule")
    out.append("")
    out.append("1. `OPEN_OR_NEGATED`, `MIXED/CONFLICTING`, `NO_THEOREM_CREDIT`,")
    out.append("   withdrawn, refuted, assumed, or required-input language cannot close a")
    out.append("   referee blocker.")
    out.append("2. `POSITIVE_LANGUAGE` is only a candidate pointer. The exact proof must be")
    out.append("   compared with the referee objection and materialized into the controlling")
    out.append("   paper before credit is assigned.")
    out.append("3. The round-three modules therefore cite historical ideas only through")
    out.append("   independently stated and proved local packets; no historical status label")
    out.append("   is used as a substitute for proof.")
    out.append("")

    args.output.write_text("\n".join(out), encoding="utf-8")
    print(
        "ROUND3_HISTORICAL_AUDIT_PASS "
        f"sources={len(source_data)} output={args.output}"
    )


if __name__ == "__main__":
    main()
