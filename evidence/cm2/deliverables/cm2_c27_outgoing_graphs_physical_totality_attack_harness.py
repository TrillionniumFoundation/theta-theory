#!/usr/bin/env python3
"""Coherent mutation attacks for the OUTGOING_GRAPHS physical-totality gate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
VERIFIER = ROOT / "cm2_c27_outgoing_graphs_physical_totality_sqlite_verifier.py"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load_verifier():
    spec = importlib.util.spec_from_file_location("outgoing_sqlite_verifier", VERIFIER)
    need(spec is not None and spec.loader is not None, "verifier import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reclose(row: dict[str, Any]) -> None:
    body = dict(row)
    body.pop("candidate_digest", None)
    row["candidate_digest"] = digest(body)


def mutate_field(path: tuple[Any, ...], value: Any) -> Callable[[list[dict[str, Any]]], None]:
    def apply(rows: list[dict[str, Any]]) -> None:
        target: Any = rows[0]
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        reclose(rows[0])
    return apply


def attacks() -> list[tuple[str, Callable[[list[dict[str, Any]]], None]]]:
    def drop_root(rows):
        rows.pop(0)

    def duplicate_root(rows):
        rows.insert(1, copy.deepcopy(rows[0]))

    def reorder_roots(rows):
        rows[0], rows[1] = rows[1], rows[0]

    def drop_g2a(rows):
        rows[0]["dispositions"] = [x for x in rows[0]["dispositions"] if x["role"] != "G2A_SHEET"]
        reclose(rows[0])

    def duplicate_g2a(rows):
        sheet = next(x for x in rows[0]["dispositions"] if x["role"] == "G2A_SHEET")
        rows[0]["dispositions"].append(copy.deepcopy(sheet))
        rows[0]["dispositions"].sort(key=lambda x: (x["role"], x["member_id"]))
        reclose(rows[0])

    def drop_g2b(rows):
        for index, value in enumerate(rows[0]["dispositions"]):
            if value["role"] == "G2B_SIDE":
                rows[0]["dispositions"].pop(index)
                break
        reclose(rows[0])

    out: list[tuple[str, Callable[[list[dict[str, Any]]], None]]] = [
        ("drop_root", drop_root),
        ("duplicate_root", duplicate_root),
        ("reorder_roots", reorder_roots),
        ("flip_graph_id", mutate_field(("graph_id",), "round242-positive-2d-transition-sheet-patch:" + "f" * 64)),
        ("flip_graph_class", mutate_field(("graph_class",), "R235_TARGET_POSITIVE_PARTIAL_BASE")),
        ("flip_terminal", mutate_field(("terminal",), "SINGLE_GRAPHS")),
        ("flip_geometry_root", mutate_field(("geometry_root_sha256",), "0" * 64)),
        ("flip_base_ast", mutate_field(("base_domain_ast_sha256",), "1" * 64)),
        ("flip_carrier_ast", mutate_field(("carrier_domain_ast_sha256",), "2" * 64)),
        ("flip_equation_ast", mutate_field(("equation_ast_sha256",), "3" * 64)),
        ("flip_exact_support_ast", mutate_field(("exact_support_ast_sha256",), "4" * 64)),
        ("flip_C10_binding", mutate_field(("C10_row_sha256",), "5" * 64)),
        ("flip_C26_G1_binding", mutate_field(("C26_G1_row_sha256",), "6" * 64)),
        ("drop_G2A", drop_g2a),
        ("duplicate_G2A", duplicate_g2a),
        ("drop_G2B", drop_g2b),
        ("flip_G2A_role", mutate_field(("dispositions", 0, "role"), "G2B_SIDE")),
        ("flip_member_id", mutate_field(("dispositions", 0, "member_id"), "round245-retained-stratum:" + "7" * 64)),
        ("flip_component", mutate_field(("dispositions", 0, "fresh_component_id"), "round306c15-source-g-component:" + "8" * 64)),
        ("flip_base_root", mutate_field(("dispositions", 0, "base_root_id"), "round266-curved-face-component:" + "9" * 64)),
        ("flip_official_key", mutate_field(("dispositions", 0, "official_key_id"), "gate5-word:000000:" + "a" * 64)),
        ("flip_support_sha", mutate_field(("dispositions", 0, "normalized_support_ast_sha256"), "b" * 64)),
        ("flip_theorem_sha", mutate_field(("dispositions", 0, "semantic_theorem_ast_sha256"), "c" * 64)),
        ("flip_C15_binding", mutate_field(("dispositions", 0, "C15_row_sha256"), "d" * 64)),
        ("flip_C24_binding", mutate_field(("dispositions", 0, "C24A_row_sha256"), "e" * 64)),
        ("flip_C25_binding", mutate_field(("dispositions", 0, "C25_row_sha256"), "f" * 64)),
        ("flip_C26_G2_binding", mutate_field(("dispositions", 0, "C26_row_sha256"), "0" * 64)),
        ("flip_one_sheet_certificate", mutate_field(("physical_totality_certificate", "exactly_one_G2A_sheet"), False)),
        ("flip_two_side_certificate", mutate_field(("physical_totality_certificate", "exactly_two_G2B_sides"), False)),
        ("inject_unresolved", mutate_field(("physical_totality_certificate", "unresolved"), 1)),
        ("inject_formal_credit", mutate_field(("formal_credit",), 1)),
    ]
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output-tag", required=True)
    args = parser.parse_args()
    module = load_verifier()
    reference, reference_result = module.reconstruct_sqlite()
    supplied, supplied_result = module.read_candidate(Path(args.candidate_dir).resolve())
    module.validate_candidate_rows(supplied, reference)
    need(canonical(supplied_result) == canonical(reference_result), "baseline exact result")
    rejected: list[str] = []
    unexpected_accepts: list[str] = []
    for name, mutation in attacks():
        candidate = copy.deepcopy(supplied)
        mutation(candidate)
        try:
            module.validate_candidate_rows(candidate, reference)
        except module.Failure:
            rejected.append(name)
        else:
            unexpected_accepts.append(name)
    need(not unexpected_accepts and len(rejected) == len(attacks()) and len(rejected) >= 15, "all coherent attacks rejected")
    body = {
        "schema": "cm2.c27.outgoing-graphs-physical-totality-zero-credit.v1.attack-harness.v1",
        "status": "PASS_31_COHERENT_OUTGOING_GRAPH_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": len(attacks()),
        "rejected_count": len(rejected),
        "unexpected_accept_count": 0,
        "rejected_attacks": rejected,
        "baseline_candidate_count": 264,
        "baseline_result_sha256": supplied_result["result_sha256"],
        "reference_result_sha256": reference_result["result_sha256"],
        "formal_credit": 0,
        "unconditional_C27_C28_C29": "REJECT_REMAINS_PENDING_FULL_TWENTY_FAMILY_GATE",
    }
    result = {**body, "result_sha256": digest(body)}
    target = AUDIT / args.output_tag
    need(not target.exists() and target.parent.resolve() == AUDIT.resolve(), "new direct-child output")
    target.mkdir(mode=0o700)
    (target / "attack_result.json").write_bytes(canonical(result))
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print("GATE_FAILURE:" + str(exc))
        raise SystemExit(2)
