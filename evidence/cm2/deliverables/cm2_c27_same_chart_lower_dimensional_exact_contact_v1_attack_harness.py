#!/usr/bin/env python3
"""Coherent re-signed attacks for the lower-dimensional contact subgate."""

from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
VERIFY_SOURCE = ROOT / "cm2_c27_same_chart_lower_dimensional_exact_contact_v1_independent_verifier.py"
PREFIX = "cm2_c27_same_chart_lower_dimensional_exact_contact_v1"


class Rejected(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def need(flag: bool, label: str) -> None:
    if type(flag) is not bool or not flag:
        raise Rejected(label)


def load_verifier():
    spec = importlib.util.spec_from_file_location("lower_contact_independent", VERIFY_SOURCE)
    need(spec is not None and spec.loader is not None, "verifier module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def flip(text: str) -> str:
    return ("0" if text[0] != "0" else "1") + text[1:]


def sequence_sha(values: list[dict[str, Any]]) -> str:
    state = hashlib.sha256()
    for value in values:
        body = dict(value)
        body.pop("ordinal", None)
        body.pop("row_sha256", None)
        state.update(canonical(body))
    return state.hexdigest()


def authority_projection(module, audit: dict[str, Any]) -> dict[str, Any]:
    buckets = audit["buckets"]
    bucket_rows = []
    global_state = hashlib.sha256()
    sorted_lists = []
    for key in sorted(buckets):
        dimension, source_pair, relation = key
        values = sorted(buckets[key])
        sorted_lists.append(values)
        bucket_rows.append({
            "dimension": dimension,
            "source_pair": source_pair,
            "component_relation": relation,
            "count": len(values),
            "pair_sequence_sha256": hashlib.sha256(b"".join(values)).hexdigest(),
            "policy": "C19C" if source_pair == "C19C__C19C" else "FULLY_OPEN",
        })
    import heapq
    for value in heapq.merge(*sorted_lists):
        global_state.update(value)
    contacts = sorted(audit["c19c_contacts"], key=lambda row: row["contact_pair_digest"])
    patterns = Counter()
    for row in contacts:
        patterns[(row["intersection_dimension"], tuple((item["left_closed"], item["right_closed"]) for item in row["zero_width_axis_endpoint_checks"]))] += 1
    return {
        "dimension_census": dict(sorted(audit["dimension_counts"].items())),
        "relation_census": {str(key): value for key, value in sorted(audit["relation_counts"].items())},
        "source_dimension_census": {str(key): value for key, value in sorted(audit["source_dimension_counts"].items())},
        "bucket_rows_sha256": sha(bucket_rows),
        "bucket_count": len(bucket_rows),
        "global_pair_commitment": global_state.hexdigest(),
        "lower_candidate_count": 5783708,
        "strict_dim3_crosscheck": 187132,
        "C19C_contact_count": len(contacts),
        "C19C_contact_semantics_sha256": sequence_sha(contacts),
        "C19C_pattern_census": {str(key): value for key, value in sorted(patterns.items(), key=lambda item: str(item[0]))},
        "C19C_cross_count": sum(row["component_relation"] == "CROSS_C15_COMPONENT" for row in contacts),
        "C19C_legal_count": sum(row["legal_cross_component_lower_dimensional_witness"] for row in contacts),
        "C19C_double_include_count": sum(row["all_zero_axes_double_included"] for row in contacts),
        "fully_open_uniform_rejection_count": 5707708,
        "C26_contact_owner_coverage_count": len(audit["c26_covered"]),
        "C26_contact_owner_gap_count": len(audit["contact_owners"] - audit["c26_covered"]),
        "forbidden_C27_read": False,
        "forbidden_old_edge_read": False,
        "forbidden_old_same_chart_read": False,
        "formal_credit": 0,
        "C27_C28_C29": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
        "source_W_transition_authorized": False,
    }


def candidate_projection(module, candidate_dir: Path) -> dict[str, Any]:
    result = module.closed_json(candidate_dir / module.RESULT, "result_sha256")
    bucket_rows = list(module.rows(candidate_dir / module.BUCKET_LEDGER))
    contacts = list(module.rows(candidate_dir / module.C19C_LEDGER))
    bucket_semantics = []
    for row in bucket_rows:
        bucket_semantics.append({
            "dimension": row["intersection_dimension"],
            "source_pair": "__".join(row["source_pair"]),
            "component_relation": row["component_relation"],
            "count": row["candidate_pair_count"],
            "pair_sequence_sha256": row["canonical_sorted_pair_digest_sequence_sha256"],
            "policy": "C19C" if row["endpoint_policy"] == "C19C_V3_PRODUCT_AUTHORITY_ROW_MATERIALIZATION" else "FULLY_OPEN",
        })
    patterns = Counter()
    for row in contacts:
        patterns[(row["intersection_dimension"], tuple((item["left_closed"], item["right_closed"]) for item in row["zero_width_axis_endpoint_checks"]))] += 1
    census = result["census"]
    source_dimension_census = {}
    for key, value in census["source_dimension_component_census"].items():
        parts = key.split("__")
        dimension = int(parts[0][3:])
        source_pair = "__".join(parts[1:-1])
        relation = parts[-1]
        source_dimension_census[str((dimension, source_pair, relation))] = value
    return {
        "dimension_census": {int(key): value for key, value in census["dimension_census"].items()},
        "relation_census": {str((int(key.split("__")[0][3:]), key.split("__")[1])): value for key, value in census["component_relation_census"].items()},
        "source_dimension_census": source_dimension_census,
        "bucket_rows_sha256": sha(bucket_semantics),
        "bucket_count": len(bucket_rows),
        "global_pair_commitment": census["global_canonical_sorted_pair_digest_sequence_sha256"],
        "lower_candidate_count": census["lower_dimensional_candidate_pair_count"],
        "strict_dim3_crosscheck": census["strict_dimension3_pair_count_crosscheck"],
        "C19C_contact_count": len(contacts),
        "C19C_contact_semantics_sha256": sequence_sha(contacts),
        "C19C_pattern_census": {str(key): value for key, value in sorted(patterns.items(), key=lambda item: str(item[0]))},
        "C19C_cross_count": sum(row["component_relation"] == "CROSS_C15_COMPONENT" for row in contacts),
        "C19C_legal_count": sum(row["legal_cross_component_lower_dimensional_witness"] for row in contacts),
        "C19C_double_include_count": sum(row["all_zero_axes_double_included"] for row in contacts),
        "fully_open_uniform_rejection_count": census["open_kernel_uniform_rejection_candidate_count"],
        "C26_contact_owner_coverage_count": census["C26_contact_owner_coverage_count"],
        "C26_contact_owner_gap_count": census["C26_contact_owner_gap_count"],
        "forbidden_C27_read": result["forbidden_inputs"]["C27_FAMILIES_read"],
        "forbidden_old_edge_read": result["forbidden_inputs"]["historical_edge_universe_read"],
        "forbidden_old_same_chart_read": result["forbidden_inputs"]["older_same_chart_candidate_ledger_read"],
        "formal_credit": result["formal_credit"],
        "C27_C28_C29": result["C27_C28_C29"],
        "CM2": result["CM2"],
        "source_W_transition_authorized": result["source_W_transition_authorized"],
    }


def seal(model: dict[str, Any]) -> dict[str, Any]:
    return {**model, "projection_sha256": sha(model)}


def validate(candidate: dict[str, Any], authority: dict[str, Any]) -> None:
    body = dict(candidate)
    claimed = body.pop("projection_sha256", None)
    need(claimed == sha(body), "coherent projection closure")
    need(candidate == authority, "primitive-sweep anchored projection equality")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    candidate_dir = Path(args.candidate_dir).resolve()
    module = load_verifier()
    _, audit = module.rebuild(args.seed)
    authority = seal(authority_projection(module, audit))
    candidate = seal(candidate_projection(module, candidate_dir))
    validate(candidate, authority)
    candidate_result = module.closed_json(candidate_dir / module.RESULT, "result_sha256")

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("drop_lower_candidate", lambda x: x.__setitem__("lower_candidate_count", x["lower_candidate_count"] - 1)),
        ("alter_dimension_census", lambda x: x["dimension_census"].__setitem__(1, x["dimension_census"][1] - 1)),
        ("alter_component_relation", lambda x: x.__setitem__("relation_census", {**x["relation_census"], "(1, 'CROSS_C15_COMPONENT')": x["relation_census"]["(1, 'CROSS_C15_COMPONENT')"] - 1})),
        ("alter_source_bucket", lambda x: x.__setitem__("source_dimension_census", {**x["source_dimension_census"], next(iter(x["source_dimension_census"])): 0})),
        ("mutate_bucket_commitment", lambda x: x.__setitem__("bucket_rows_sha256", flip(x["bucket_rows_sha256"]))),
        ("mutate_global_pair_commitment", lambda x: x.__setitem__("global_pair_commitment", flip(x["global_pair_commitment"]))),
        ("drop_C19C_contact", lambda x: x.__setitem__("C19C_contact_count", x["C19C_contact_count"] - 1)),
        ("flip_C19C_endpoint_semantics", lambda x: x.__setitem__("C19C_contact_semantics_sha256", flip(x["C19C_contact_semantics_sha256"]))),
        ("claim_double_included_endpoint", lambda x: x.__setitem__("C19C_double_include_count", 1)),
        ("claim_legal_cross_component_witness", lambda x: x.__setitem__("C19C_legal_count", 1)),
        ("remove_fully_open_rejection", lambda x: x.__setitem__("fully_open_uniform_rejection_count", x["fully_open_uniform_rejection_count"] - 1)),
        ("claim_C26_negative_geometry_gap", lambda x: x.__setitem__("C26_contact_owner_gap_count", x["C26_contact_owner_gap_count"] + 1)),
        ("claim_C27_FAMILIES_read", lambda x: x.__setitem__("forbidden_C27_read", True)),
        ("claim_old_edge_universe_read", lambda x: x.__setitem__("forbidden_old_edge_read", True)),
        ("grant_formal_credit", lambda x: x.__setitem__("formal_credit", 1)),
        ("authorize_C27_without_rebuild", lambda x: x.__setitem__("C27_C28_C29", "AUTHORIZED")),
        ("claim_CM2", lambda x: x.__setitem__("CM2", "GO_FOR_CLAIM")),
        ("authorize_Source_W_transition", lambda x: x.__setitem__("source_W_transition_authorized", True)),
    ]
    attacks = []
    for ordinal, (name, mutate) in enumerate(mutations):
        body = copy.deepcopy(candidate)
        body.pop("projection_sha256")
        mutate(body)
        attacked = seal(body)
        rejected = False
        reason = None
        try:
            validate(attacked, authority)
        except Rejected as exc:
            rejected = True
            reason = str(exc)
        need(rejected, "mutation must reject:" + name)
        attacks.append({"ordinal": ordinal, "attack": name, "coherent_projection_closure_recomputed": True, "rejected": True, "reason": reason})
    body = {
        "schema": "cm2.c27.same-chart-lower-dimensional-exact-contact.v1.attack-result.v1",
        "status": f"PASS_ALL_{len(attacks)}_COHERENT_RESIGNED_MUTATIONS_REJECTED",
        "seed": args.seed,
        "candidate_result_sha256": candidate_result["result_sha256"],
        "candidate_semantic_projection_sha256": candidate_result["semantic_projection_sha256"],
        "candidate_bucket_ledger_sha256": candidate_result["census"]["ledgers"]["candidate_buckets"]["sha256"],
        "candidate_C19C_ledger_sha256": candidate_result["census"]["ledgers"]["C19C_contacts"]["sha256"],
        "independent_verifier_sha256": module.hash_file(VERIFY_SOURCE),
        "authority_projection_sha256": authority["projection_sha256"],
        "candidate_projection_sha256": candidate["projection_sha256"],
        "attack_count": len(attacks), "rejected_count": len(attacks), "attacks": attacks,
        "formal_credit": 0, "C27_C28_C29": "REBUILD_REQUIRED_AND_NOT_AUTHORIZED", "CM2": "NO-GO_FOR_CLAIM", "source_W_transition_authorized": False,
    }
    result = {**body, "result_sha256": sha(body)}
    Path(args.output).resolve().write_bytes(canonical(result))
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
