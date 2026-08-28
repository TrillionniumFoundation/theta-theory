#!/usr/bin/env python3
"""Coherent semantic mutation attacks for the scoped C26 theorem."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
LEDGER = "c26_691424_scoped_exact_contact_source_factorization.jsonl.gz"


class Failure(RuntimeError):
    pass


def need(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 << 20), b""):
            state.update(block)
    return state.hexdigest()


def close_result(value: dict[str, Any], census_changed: bool = False) -> dict[str, Any]:
    out = copy.deepcopy(value)
    out.pop("result_sha256", None)
    if census_changed:
        out["semantic_projection_sha256"] = digest(out["census"])
    out["result_sha256"] = digest(out)
    return out


def run(verifier: Path, candidate: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, str(verifier), "--candidate-dir", str(candidate), "--front-gate-only"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    candidate = Path(args.candidate_dir).resolve()
    output = Path(args.output_dir).resolve()
    need(not output.exists(), "new output dir")
    output.mkdir(parents=True)
    verifier = ROOT / "deliverables/cm2_c26_exact_contact_source_factorization_scoped_v1_independent_verifier.py"
    control = run(verifier, candidate)
    need(control.returncode == 0, "control must pass")
    original = json.loads((candidate / "result.json").read_bytes())

    Mutation = tuple[str, Callable[[dict[str, Any]], None], bool]
    attacks: list[Mutation] = [
        ("C26_denominator_decrement", lambda r: r["census"].__setitem__("C26_feature_rows", 691_423), True),
        ("direct_C26_carrier_injected", lambda r: r["census"].__setitem__("C26_direct_support_carrier_rows", 1), True),
        ("source_factorization_gap", lambda r: r["census"].__setitem__("C26_source_factorized_rows", 691_423), True),
        ("scoped_unresolved_injected", lambda r: r["census"].__setitem__("scoped_unresolved_rows", 1), True),
        ("G1_bucket_erased", lambda r: r["census"]["graph_feature_row_disjoint_bucket_census"].__setitem__("G1_C10_definition_handoff_by_graph_id", 0), True),
        ("G2A_bucket_double_count", lambda r: r["census"]["graph_feature_row_disjoint_bucket_census"].__setitem__("G2A_C24A_scoped_route", 10_528), True),
        ("G2B_positive_count_flip", lambda r: r["census"].__setitem__("C24A_G2B_positive_priority_pairs", 9_407), True),
        ("C24B_empty_count_flip", lambda r: r["census"].__setitem__("C24B_exact_empty_members", 167), True),
        ("C26_absence_promoted_to_negative_geometry", lambda r: r["candidate_governance"].__setitem__("C26_absence_used_as_negative_geometry_theorem", True), False),
        ("global_totality_fabricated", lambda r: r["theorem_scope"].__setitem__("global_three_terminal_totality_and_unique_assignment", True), False),
        ("scoped_conclusion_negated", lambda r: r["conclusion"].__setitem__("NO_NEW_GEOMETRY_FROM_C26_FEATURE_ROWS", False), False),
        ("formal_credit_fabricated", lambda r: r.__setitem__("formal_credit", 1), False),
        ("manifest_authorization_fabricated", lambda r: r.__setitem__("manifest_authorized", True), False),
        ("C27_transition_credit_fabricated", lambda r: r["strict_nonpromotion"].__setitem__("C27_transition_totality", 1), False),
        ("global_blocker_removed", lambda r: r.__setitem__("open_blockers", r["open_blockers"][:-1]), False),
    ]
    records: list[dict[str, Any]] = []
    rejected = 0
    for ordinal, (name, mutate, census_changed) in enumerate(attacks, 1):
        attack_dir = output / f"attack_{ordinal:02d}_{name}"
        attack_dir.mkdir()
        os.link(candidate / LEDGER, attack_dir / LEDGER)
        mutated = copy.deepcopy(original)
        mutate(mutated)
        mutated = close_result(mutated, census_changed)
        (attack_dir / "result.json").write_bytes(canonical(mutated) + b"\n")
        completed = run(verifier, attack_dir)
        accepted = completed.returncode == 0
        if not accepted:
            rejected += 1
        (attack_dir / "stdout.log").write_bytes(completed.stdout)
        (attack_dir / "stderr.log").write_bytes(completed.stderr)
        (attack_dir / "exit_code.txt").write_text(str(completed.returncode) + "\n", encoding="ascii")
        records.append({"ordinal": ordinal, "attack": name, "coherent_result_closure_recomputed": True, "semantic_projection_recomputed_when_census_changed": census_changed, "accepted": accepted, "exit_code": completed.returncode, "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest()})
    need(rejected == len(attacks), "all attacks rejected")
    body = {
        "schema": "cm2.c26-independent.exact-contact-source-factorization-coherent-attacks.v1",
        "status": "PASS_CONTROL_AND_REJECT_15_OF_15_COHERENT_MUTATIONS__ZERO_CREDIT",
        "control_pass": True,
        "control_stdout_sha256": hashlib.sha256(control.stdout).hexdigest(),
        "verifier_sha256": file_sha(verifier),
        "candidate_result_sha256": original["result_sha256"],
        "candidate_ledger_sha256": file_sha(candidate / LEDGER),
        "attack_count": len(attacks),
        "accepted": 0,
        "rejected": rejected,
        "attacks": records,
        "formal_credit": 0,
    }
    receipt = dict(body)
    receipt["result_sha256"] = digest(body)
    (output / "attack_receipt.json").write_bytes(canonical(receipt) + b"\n")
    print(canonical({"status": receipt["status"], "result_sha256": receipt["result_sha256"]}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
