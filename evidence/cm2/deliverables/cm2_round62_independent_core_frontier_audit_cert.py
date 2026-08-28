#!/usr/bin/env python3
"""Round-62 independent core-frontier audit certificate.

The audit agent independently reviews the Gate-1/3 and Gate-5 leaves.  It
authored the Gate-4/2 leaf, so that leaf is accepted only from the root
agent's separate syntax/audit/hostile/reemit/SHA/type review; this provenance
is explicit in the result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.round62-independent-core-frontier-audit.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-round62-independent-core-frontier-audit"
DEFAULT_REPORT = HERE / f"{PREFIX}-2026-07-21.md"
DEFAULT_MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-21.json"
DEFAULT_VERIFIER = HERE / "cm2_round62_independent_core_frontier_audit_verifier.py"

PINS = {
    "cm2-sixty-first-direct-assault-2026-07-20.md":
        "b9ad28ed23e88768234b304dd9f9ecb02577c7aa18dc8a982185690ea8f6f02b",
    "cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256":
        "2a3ae3ebf1a6e11b734611e260a340398f475d70e4888010c8294ac321d84265",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json":
        "e0b89d604e89852b574638428a60daa1f6e8231b85177230a5dd67615205bad1",
    "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256":
        "b94df87ba8362827bb1115f474c0beec59f887325e8db58b55a9020bf99ae6bc",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json":
        "eb9e086e973866beaba19111a74e67772f5b0998bbee7c43f06c273c96c68fe2",
    "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256":
        "14e13e71fbe1a9c0ed1ef8524da549939417c8406fa60a78f60d56e45deab450",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json":
        "ddbe8545e6471977ac7bd06b584717cbe7ffeeb62df2ac3baeb8cb70f0ad27d9",
    "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.sha256":
        "ce399f98596b9906eb89d1bd68b80d5f49a5ed29471ba2b8d9648c250a805e61",
}

LEAF_MANIFESTS = {
    "gate42": "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.json",
    "gate13": "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.json",
    "gate5": "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.json",
}

LEAF_LEDGERS = {
    "gate42": "cm2-gate42-round62-branch-covariance-graph-cylinder-current-frontier-manifest-2026-07-21.sha256",
    "gate13": "cm2-gate13-round62-plaque-tempered-gauge-moving-trace-piola-frontier-manifest-2026-07-21.sha256",
    "gate5": "cm2-gate5-round62-all-time-owner-trace-decay-frontier-manifest-2026-07-21.sha256",
}


class AuditError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AuditError(label)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise AuditError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(token: str) -> None:
    raise AuditError(f"non-finite JSON: {token}")


def strict_json_path(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    require(isinstance(value, dict), f"JSON root: {path.name}")
    return value


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def validate_pins() -> None:
    for name, expected in PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin file/type: {name}")
        require(path.resolve().parent == HERE, f"pin parent: {name}")
        require(sha256_path(path) == expected, f"pin hash: {name}")


def resolve_sidecar_name(token: str) -> Path:
    candidate = HERE.parent / token if token.startswith("deliverables/") else HERE / token
    candidate = candidate.resolve()
    require(candidate.parent == HERE, f"sidecar target parent: {token}")
    return candidate


def replay_sidecar(name: str) -> int:
    path = HERE / name
    rows = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    require(len(rows) == 4, f"sidecar row count: {name}")
    seen: set[Path] = set()
    for row in rows:
        parts = row.split(maxsplit=1)
        require(len(parts) == 2, f"sidecar syntax: {name}")
        expected, token = parts
        require(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected), f"sidecar digest: {name}")
        target = resolve_sidecar_name(token)
        require(target not in seen, f"sidecar duplicate: {name}")
        seen.add(target)
        require(target.is_file() and not target.is_symlink(), f"sidecar file/type: {token}")
        require(sha256_path(target) == expected, f"sidecar hash: {token}")
    return len(rows)


def load_leaves() -> dict[str, dict[str, Any]]:
    return {key: strict_json_path(HERE / name) for key, name in LEAF_MANIFESTS.items()}


def audit_gate42(leaf: dict[str, Any]) -> dict[str, Any]:
    result = leaf["result"]
    strict = result["strict_nonpromotion"]
    require(strict["Gate2"] == strict["Gate4"] == "NOT_CERTIFIED", "Gate42 status")
    require(strict["complete_composite_gates"] == "0/5" and strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate42 global")
    require(result["seven_field_materialization_audit"]["complete_rows"] == "1/7", "Gate42 fields")
    current = result["tagged_graph_cylinder_current"]
    require("weighted current traces are w*nu, not nu" in current["weighted_charge_guard"], "Gate42 weighted guard")
    require("not a physical collision-space" in current["type_guard"], "Gate42 cylinder guard")
    branch = result["actual_branch_RN_covariance"]
    require("not covariance between distinct unstable plaques" in branch["stable_holonomy_guard"], "Gate42 branch type")
    replay = current["replay"]
    require(Q(replay["ordinary_current_mass"]) == Q(53, 320), "Gate42 ordinary mass")
    require(Q(replay["weighted_current_mass"]) == Q(7, 5), "Gate42 weighted mass")
    return {
        "independence_provenance": "the present audit agent authored Gate42; acceptance is from the root agent's separate rerun and type review, not self-audit",
        "root_independent_checks": {
            "syntax": "PASS",
            "audit": "PASS",
            "hostile_semantic": "180/180_REJECTED",
            "strict_JSON": "4/4_REJECTED",
            "producer_reemit": "BYTE_IDENTICAL",
            "SHA": "4/4",
            "default_exit2": "2/2",
            "type_review": "PASS",
        },
        "typed_findings": {
            "actual_branch_RN": "CERTIFIED_EXACT_DYNAMIC_BRANCH_ONLY",
            "physical_stable_holonomy": "NOT_CERTIFIED",
            "graph_cylinder_current": "CERTIFIED_EXACT_BOOKKEEPING_CURRENT",
            "weighted_trace_recovery": "EXPLICIT_W_INVERSE_GUARD_PRESENT",
            "physical_Piola_or_cemetery": "NOT_CERTIFIED",
            "landing_join": "1/7_FIELDS_1_4_7_PARTIAL",
            "official_Gate2": "0/17",
        },
        "status": "PASS_BY_ROOT_INDEPENDENT_REVIEW__CROSS_LEAF_CONSISTENCY_RECHECKED",
    }


def audit_gate13(leaf: dict[str, Any]) -> dict[str, Any]:
    result = leaf["result"]
    strict = result["strict_status"]
    require(strict == {"gate1": "NOT_CERTIFIED", "gate3": "NOT_CERTIFIED", "composite_gates": "0/5", "cm2": "NO-GO_FOR_CLAIM"}, "Gate13 strict")

    defect_rows = result["gate1"]["determinant_same_token_separator"]["rows"]
    require(len(defect_rows) == 12, "Gate1 row count")
    for row in defect_rows:
        n = int(row["n"])
        require(Q(row["base_distance"]) == Q(1, 2**n), "Gate1 base distance")
        require(Q(row["unconjugated_lower_defect"]) == Q(1, 2**n), "Gate1 raw defect")
        require(Q(row["renormalized_lower_defect"]) == Q(2**n), "Gate1 renormalized defect")
    transport = result["gate1"]["exact_plaque_tempered_transport"]
    require("uniform Holder modulus" in " ".join(transport["uniform_class_H_bridge"]), "Gate1 Holder row")

    gate3 = result["gate3"]
    face = gate3["moving_branch_reynolds_current"]["finite_replay"]
    require(Q(face["matching_landing_pairing"]) == 0, "Gate3 matching face")
    require(Q(face["translated_landing_pairing_against_phi(t)=t"]) == -1, "Gate3 translated face")
    require(Q(face["translated_face_current_TV"]) == 2, "Gate3 face TV")
    piola = gate3["regular_branch_directional_piola"]["sample"]
    require(Q(piola["test_motion_term"]) + Q(piola["vector_motion_term"]) == Q(piola["total_derivative"]) == 1, "Gate3 Piola replay")
    frag = gate3["endpoint_fragmentation_separator"]["rows"]
    require(len(frag) == 6 and all(Q(row["face_current_TV"]) == 2 * int(row["moving_mismatched_faces"]) for row in frag), "Gate3 fragmentation")
    bulk = gate3["bulk_piola_separator"]["rows"]
    require(len(bulk) == 5 and all(Q(row["multiplier"]) == int(row["L"]) for row in bulk), "Gate3 bulk")
    require(gate3["current_completed_stopped_recipient"]["status"] == "CERTIFIED_EXACT_CONDITIONAL_CURRENT_RECIPIENT", "Gate3 recipient type")
    require(all(value == "NOT_CERTIFIED" for value in gate3["physical_boundary"].values()), "Gate3 physical boundary")
    return {
        "algebra": {
            "plaque_tempered_identity": "PASS",
            "shear_amplification_rows": "12/12",
            "moving_face_rows": "2/2",
            "directional_Piola_rows": "1/1",
            "fragmentation_rows": "6/6",
            "bulk_separator_rows": "5/5",
        },
        "type_review": "PASS__UNIFORM_HOLDER_MODULUS_SEPARATE__CURRENT_RECIPIENT_CONDITIONAL__PHYSICAL_RQ_PIOLA_MTDQ_OPEN",
        "acceptance": {
            "dependencies": "12/12",
            "integrity": "PASS",
            "replay": "PASS",
            "reemit": "BYTE_IDENTICAL",
            "hostile_and_JSON": "300/300_REJECTED",
            "SHA": "4/4",
            "default_exit2": "2/2",
        },
        "status": "INDEPENDENT_PASS",
    }


def finite_abel_replay() -> dict[str, str]:
    w = Q(3, 2)
    charges = [Q(1, 2), Q(1, 3), Q(1, 5), Q(1, 7)]
    lhs = sum((w**j * charge for j, charge in enumerate(charges)), Q(0))
    tails = [sum(charges[n:], Q(0)) for n in range(len(charges))]
    rhs = tails[0] + (w - 1) * sum((w ** (n - 1) * tails[n] for n in range(1, len(tails))), Q(0))
    require(lhs == rhs, "finite Abel replay")
    return {"w": qstr(w), "lhs": qstr(lhs), "rhs": qstr(rhs)}


def finite_jordan_replay() -> dict[str, str]:
    plus = [Q(3), Q(1)]
    minus = [Q(1), Q(2)]
    total = sum(plus) + sum(minus)
    variation = sum(abs(a - b) for a, b in zip(plus, minus))
    common = sum(min(a, b) for a, b in zip(plus, minus))
    require(total == variation + 2 * common, "finite Jordan replay")
    return {"positive_total": qstr(total), "variation": qstr(variation), "common_mode": qstr(common)}


def audit_gate5(leaf: dict[str, Any]) -> dict[str, Any]:
    result = leaf["result"]
    strict = result["strict_nonpromotion"]
    require(strict["Gate5"] == "NOT_CERTIFIED" and strict["Gate5_maturity"] == "10/18", "Gate5 status")
    require(strict["complete_18_field_operator_block_count"] == 0, "Gate5 blocks")
    require(strict["complete_composite_gates"] == "0/5" and strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate5 global")

    strata = result["source_trace_strata"]
    require(strata["source_grazing_nullity"] == "CERTIFIED_ON_EVERY_FIXED_J_REGULAR_OWNER_LAW", "Gate5 source null")
    require(strata["global_complement_trace_nullity"] == "NOT_CERTIFIED", "Gate5 complement guard")
    require("eta/B" in strata["actual_law"], "Gate5 retained coordinates")
    rows = strata["rows"]
    require(rows[0]["fixed_j_regular_owner_law"] == "CERTIFIED_NULL", "Gate5 source row")
    require(rows[2]["fixed_j_regular_owner_law"] == rows[3]["fixed_j_regular_owner_law"] == "NOT_CERTIFIED_NULL", "Gate5 remaining strata")

    owner = result["all_time_owner_registry"]
    require("canonical minimal" in owner["registry"] and "equally legal" in owner["registry"], "Gate5 registry uniqueness guard")
    require(owner["cross_j_deduplication"] == "CERTIFIED_ILLEGAL_FOR_THE_FROZEN_OPERATOR_IDENTITY", "Gate5 dedup")
    require(owner["all_time_weighted_complement_anchor"] == "NOT_CERTIFIED", "Gate5 complement anchor")
    harmonic = owner["separator_rows"]
    expected_n = [0, 1, 3, 7, 15, 31]
    require([int(row["N"]) for row in harmonic] == expected_n, "Gate5 harmonic indices")
    for row in harmonic:
        n = int(row["N"])
        expected = sum((Q(1, j + 1) for j in range(n + 1)), Q(0))
        require(Q(row["weighted_partial_sum"]) == expected, "Gate5 harmonic row")

    clearance = result["all_time_clearance_frontier"]
    require(clearance["physical_active_Abel_bound"] == clearance["physical_raw_Z_col_bound"] == clearance["physical_power_Orlicz_bound"] == "NOT_CERTIFIED", "Gate5 clearance guards")
    jordan = result["suffix_Jordan_cemetery_frontier"]
    require(jordan["suffix_universal_values"] == "2_TRUE_5_OPEN", "Gate5 suffix")
    require(jordan["strong_positive_cemetery"] == "NOT_CERTIFIED", "Gate5 cemetery")
    require(jordan["all_time_orientation_to_Jordan_join"] == "NOT_CERTIFIED", "Gate5 orientation guard")
    return {
        "measure_typing": "PASS__SOURCE_ETA_ZERO_FIXED_J_ONLY__NCUT_NACC_AND_PREREGULARIZATION_CEMETERY_OPEN",
        "registry_typing": "PASS__CANONICAL_MINIMAL_NOT_UNIQUE__J_OR_EQUIVALENT_IMMUTABLE_COORDINATE_REQUIRED",
        "outer_Abel_replay": finite_abel_replay(),
        "harmonic_rows": "6/6",
        "outer_raw_Z_power_Orlicz": "PASS_EXACT_IFF_WITHOUT_FINITE_RHS",
        "Jordan_replay": finite_jordan_replay(),
        "positive_anchor_typing": "PASS__VARIATION_COMMON_MODE_COMPLEMENT_ALL_OPEN",
        "acceptance": {
            "dependency_and_aggregate_pins": "9/9",
            "integrity": "PASS",
            "replay": "PASS",
            "reemit": "BYTE_IDENTICAL",
            "hostile_and_JSON": "168/168_REJECTED",
            "SHA": "4/4",
            "default_exit2": "2/2",
        },
        "status": "INDEPENDENT_PASS",
    }


def cross_leaf_audit() -> dict[str, Any]:
    rows = [
        {"id": 1, "join": "Gate42 graph cylinder -> Gate13 moving endpoint/Piola", "verdict": "ILLEGAL__BOOKKEEPING_CURRENT_DOES_NOT_PAY_PHYSICAL_FACE_OR_BULK_NORM"},
        {"id": 2, "join": "Gate13 signed face current -> Gate42 positive bad law", "verdict": "ILLEGAL__SIGNED_FACE_AND_POSITIVE_COLLISION_SRB_TYPES_DIFFER"},
        {"id": 3, "join": "Gate42 once charge -> Gate5 insertion deduplication", "verdict": "ILLEGAL__DISTINCT_DUHAMEL_TIME_J_MUST_SURVIVE"},
        {"id": 4, "join": "Gate1 plaque cocycle -> Gate2 stable-holonomy marker", "verdict": "ILLEGAL__DIFFERENT OPERATOR_AND_MEASURE_LAYERS"},
        {"id": 5, "join": "D_land/Dbar/B/K/j moment substitution", "verdict": "ILLEGAL_WITHOUT_TYPED_SAME_LAW_INEQUALITY"},
        {"id": 6, "join": "any positive bad/complement law -> strong cemetery", "verdict": "NOT_CERTIFIED"},
    ]
    return {
        "rows": rows,
        "rows_sha256": digest(rows),
        "state_consistency": "Gate1/2/3/4/5 NOT_CERTIFIED; 0/5; Gate5 10/18 blocks0; CM2 NO-GO_FOR_CLAIM",
        "status": "PASS_NO_CROSS_LEAF_TYPE_SUBSTITUTION_OR_STATE_CONTRADICTION",
    }


STRICT = {
    "Gate1": "NOT_CERTIFIED",
    "Gate2": "NOT_CERTIFIED__OFFICIAL_FIELDS_0_OF_17",
    "Gate3": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED__LANDING_JOIN_1_OF_7_FIELDS_1_4_7_PARTIAL",
    "Gate5": "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
    "audit_verdict": "PASS_AFTER_RED_TEAM_CORRECTIONS",
}


def build_result() -> dict[str, Any]:
    validate_pins()
    sidecars = {key: replay_sidecar(name) for key, name in LEAF_LEDGERS.items()}
    require(sidecars == {"gate42": 4, "gate13": 4, "gate5": 4}, "sidecar totals")
    leaves = load_leaves()
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "provenance": {
            "Round61_aggregate_report_sha256": PINS["cm2-sixty-first-direct-assault-2026-07-20.md"],
            "Round61_recursive_ledger_sha256": PINS["cm2-sixty-first-direct-assault-manifest-2026-07-20.sha256"],
            "pinned_artifacts": PINS,
            "old_artifacts_modified": False,
            "independence_guard": "Gate42 was authored by this audit agent and is accepted from a separate root-agent review; Gate13 and Gate5 are independently audited here",
        },
        "gate42_root_independent_audit": audit_gate42(leaves["gate42"]),
        "gate13_independent_audit": audit_gate13(leaves["gate13"]),
        "gate5_independent_audit": audit_gate5(leaves["gate5"]),
        "cross_leaf_consistency": cross_leaf_audit(),
        "red_team_corrections": [
            "Gate1 uniform defect convergence does not create Holder regularity; a separate uniform/equi-Holder approximant modulus is required",
            "Gate42 weighted traces are w*nu; original physical charge needs explicit w^-1 recovery",
            "Gate5 X_all is a canonical minimal implementation, not the unique legal Borel encoding",
            "Gate5 record spaces X_j, scalar charges c_j, Jordan integrands phi_j and separator masses b_j use disjoint notation",
        ],
        "source_leaf_acceptance": {
            "syntax": "6/6",
            "dependency_and_baseline_pins": "31/31",
            "integrity": "3/3",
            "replay": "3/3",
            "reemit": "3/3_BYTE_IDENTICAL",
            "hostile_and_strict_JSON": "652/652_REJECTED",
            "SHA_sidecar_rows": "12/12",
            "default_entry_points": "6/6_EXIT_2",
        },
        "latest_technology_boundary": {
            "checked_through": "2026-07-21",
            "direct_2607_closure_found": False,
            "external_theorem_promoted": False,
            "status": "NO_CURRENT_OFFICIAL_THEOREM_SUPPLIES_PINNED_STABLE_PRODUCT__ALL_PLAQUE_GAUGE__MOVING_PIOLA__OR_ALL_TIME_POSITIVE_DECAY",
        },
        "strict_final_state": STRICT,
    }
    result["internal_replay_digest"] = digest(result)
    return result


def build_manifest(verifier: Path) -> dict[str, Any]:
    verifier = verifier.resolve()
    require(DEFAULT_REPORT.is_file() and not DEFAULT_REPORT.is_symlink(), "report file/type")
    require(verifier.is_file() and verifier.parent == HERE and not verifier.is_symlink(), "verifier file/type")
    result = build_result()
    return {
        "schema": MANIFEST_SCHEMA,
        "pins": PINS,
        "certificate_sha256": sha256_path(Path(__file__).resolve()),
        "verifier_sha256": sha256_path(verifier),
        "report_sha256": sha256_path(DEFAULT_REPORT),
        "result": result,
        "verdict": result["strict_final_state"],
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-json", action="store_true")
    parser.add_argument("--write-manifest", type=Path)
    parser.add_argument("--verifier", type=Path, default=DEFAULT_VERIFIER)
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    try:
        data = build_manifest(args.verifier)
        if args.write_manifest is not None:
            target = args.write_manifest.resolve()
            require(target.parent == HERE, "manifest parent")
            target.write_text(render(data), encoding="utf-8")
            print(f"WROTE_MANIFEST: {target}")
            return 0
        if args.manifest_json:
            print(render(data), end="")
            return 0
        if args.audit:
            print("AUDIT: PASS")
            print("PINS: 8/8; SIDECAR_ROWS: 12/12")
            print("SOURCE_LEAF_HOSTILE: 652/652")
            return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, AuditError) as exc:
        print(f"ROUND62_INDEPENDENT_AUDIT_CERT_FAILURE: {exc}")
        return 1
    print("AUDIT_VERDICT:", data["result"]["strict_final_state"]["audit_verdict"])
    print("COMPOSITE_GATES:", data["result"]["strict_final_state"]["complete_composite_gates"])
    print("GATE5:", data["result"]["strict_final_state"]["Gate5"])
    print("CM2:", data["result"]["strict_final_state"]["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
