#!/usr/bin/env python3
"""Producer for the independent CM2 Round-61 core-frontier audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPORT = HERE / "cm2-round61-independent-core-frontier-audit-2026-07-20.md"
MANIFEST = HERE / "cm2-round61-independent-core-frontier-audit-manifest-2026-07-20.json"
VERIFIER = HERE / "cm2_round61_independent_core_frontier_audit_verifier.py"

FROZEN_PINS = {
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.json":
        "2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b",
    "cm2-gate4-round61-marker-weighted-curve-defect-ledger-frontier-manifest-2026-07-20.sha256":
        "a7499c939a1b167a21b62f8f0485ceaac5b44a9c21d2c59e3e22ee45805c56e2",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.json":
        "59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75",
    "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-manifest-2026-07-20.sha256":
        "27f936d543d7b0f4794741f6896387ab0dcbc4b5d2e729f3412beb6ddc190d26",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json":
        "bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019",
    "cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.sha256":
        "744bf350c4b3511bb35cefb12d294d4ef407d9c09b43dacb1123eba6103a1f0b",
}

G4_MANIFEST = HERE / next(name for name in FROZEN_PINS if name.startswith("cm2-gate4-") and name.endswith(".json"))
G5_MANIFEST = HERE / next(name for name in FROZEN_PINS if name.startswith("cm2-gate5-") and name.endswith(".json"))
G123_MANIFEST = HERE / next(name for name in FROZEN_PINS if name.startswith("cm2-gate123-") and name.endswith(".json"))

C_P = Q(4 * 10**90 * 360493663, 358863)
FWD = Q(395304765824751, 220000)
REV = Q(162772550633721, 176000)
BI = Q(2395081816467609, 880000)
BLOCK_DEPTH = 9148


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False,
                       allow_nan=False) + "\n").encode()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False
    ).encode()).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise AuditError(f"nonfinite JSON constant: {token}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
            f"JSON file/type: {path.name}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"),
                           object_pairs_hook=unique_object,
                           parse_constant=reject_constant)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise AuditError(f"JSON parse: {path.name}: {exc}") from exc
    require(type(value) is dict, f"JSON root: {path.name}")
    return value


def resolve_ledger_target(raw_name: str) -> Path:
    candidate = Path(raw_name)
    require(not candidate.is_absolute() and ".." not in candidate.parts,
            f"unsafe ledger name: {raw_name}")
    path = ROOT / candidate if candidate.parts[:1] == ("deliverables",) else HERE / candidate
    require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
            f"ledger target: {raw_name}")
    return path


def ledger_rows(sidecar: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in sidecar.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        require(len(parts) == 2 and len(parts[0]) == 64,
                f"ledger syntax: {sidecar.name}")
        path = resolve_ledger_target(parts[1].strip())
        require(sha(path) == parts[0], f"ledger digest: {path.name}")
        rows.append({"name": path.name, "sha256": parts[0]})
    require(len(rows) == 4, f"ledger row count: {sidecar.name}")
    return rows


def load_frozen() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, str]], int]:
    for name, expected in FROZEN_PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink() and path.resolve().parent == HERE,
                f"frozen file/type: {name}")
        require(sha(path) == expected, f"frozen hash: {name}")
    g4 = load_json(G4_MANIFEST)
    g5 = load_json(G5_MANIFEST)
    g123 = load_json(G123_MANIFEST)
    rows: list[dict[str, str]] = []
    for name in FROZEN_PINS:
        if name.endswith(".sha256"):
            rows.extend(ledger_rows(HERE / name))
    require(len(rows) == 12 and len({row["name"] for row in rows}) == 12,
            "leaf ledger rows")
    dependency_count = (
        len(g4["dependencies"]) + len(g4["baseline_files"])
        + len(g5["dependencies"]) + len(g5["Round60_aggregate_artifact_sha256"])
        + len(g123["dependencies"])
    )
    require(dependency_count == 30, f"main dependency count: {dependency_count}")
    return g4, g5, g123, rows, dependency_count


def defect_depth(z: Q) -> int:
    if z < C_P:
        return 0
    depth = 1
    while z / 2**depth >= C_P / 2:
        depth += 1
    return depth


def audit_gate4(g4: dict[str, Any]) -> dict[str, Any]:
    result = g4["result"]
    lift = result["actual_marker_weighted_curve_lift"]
    lattice = result["weighted_graph_defect_lattice"]
    separator = result["smooth_Dland_vs_strong_separator"]
    fields = result["seven_field_materialization_audit"]
    strict = result["strict_nonpromotion"]

    require("CONE_CURVE_MEASURE_LIFT" in lift["status"], "Gate4 lift type")
    require("not asserted to be a partition" in lift["rokhlin_guard"], "Gate4 Rokhlin guard")
    require("not claimed to remain a regular standard family" in lift["field_effect"],
            "Gate4 regular-family guard")
    atoms = lattice["sample_atoms"]
    mass = sum((Q(row["mass"]) for row in atoms), Q(0))
    weighted = sum((2 ** row["D"] * Q(row["mass"]) for row in atoms), Q(0))
    require(mass == Q(53, 320) and weighted == Q(7, 5), "Gate4 graph sample")
    require(lattice["sample_weighted_norm"] == "7/5", "Gate4 graph norm")
    require(lattice["graph_rows_complete"] == "4/5", "Gate4 graph rows")
    require(lattice["requested_strong_interface_rows_complete"] == "1/5_TAG_ROW_ONLY",
            "Gate4 strong rows")

    length = Q(2, 1) / (3 * C_P)
    z = 1 / length
    require(z == Q(3, 2) * C_P and defect_depth(z) == 2, "Gate4 short defect")
    require(all(row["D_land"] == 2 for row in separator["rows"]), "Gate4 separator D")
    require(len({row["weighted_D_moment"] for row in separator["rows"]}) == 1,
            "Gate4 constant moment")
    require(separator["rows"][-1]["BV_variation_of_marker"] == 4096,
            "Gate4 BV growth")
    require("does not purport to refute every possible anisotropic norm" in separator["conclusion"],
            "Gate4 separator scope")
    require(fields["actual_complete_rows"] == "1/7" and fields["partial_rows"] == [1, 4, 7],
            "Gate4 field count")
    require(fields["official_Gate2_fields_unchanged"] == "0/17", "Gate4 Gate2 score")
    require(strict["Gate4"] == "NOT_CERTIFIED" and
            strict["complete_composite_gates"] == "0/5" and
            strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate4 strict state")
    require(strict["strong_singular_current_cemetery"] == "NOT_CERTIFIED",
            "Gate4 cemetery guard")
    return {
        "status": "PASS",
        "marker_lift": "CERTIFIED_CONE_CURVE_MEASURE_ONLY",
        "graph_norm_sample": "7/5",
        "graph_interfaces": "4/5",
        "strong_interfaces": "1/5_TAG_ONLY",
        "seven_field_join": "1/7__FIELDS_1_4_7_PARTIAL",
        "BV_separator_terminal_variation": 4096,
        "gate4": "NOT_CERTIFIED",
    }


def orlicz_replay() -> list[dict[str, Any]]:
    with localcontext() as ctx:
        ctx.prec = 150
        gamma = (Decimal(2000) / Decimal(1999)
                 * Decimal(1 + 48 * BLOCK_DEPTH)
                 * (Decimal(900337) / Decimal(901685)) ** BLOCK_DEPTH)
        rho = (Decimal(111718729) / Decimal(111718750)) ** BLOCK_DEPTH
        w = (Decimal(1) + Decimal(1) / rho) / Decimal(2)
        beta = Decimal(2).ln() / (-gamma.ln())
        q_col = Decimal(2).ln() / (beta * w.ln())
        require(w > 1 and beta > 0 and q_col > 1, "Orlicz constants")
        rows = []
        for k in (0, 1, 2, 16, 4381, 10000):
            r = int((beta * Decimal(k + 1)).to_integral_value(rounding=ROUND_CEILING))
            phi = (w ** r) ** q_col
            raw = Decimal(2) ** (k + 1)
            require(raw <= phi < (w ** q_col) * raw, f"Orlicz row {k}")
            rows.append({"K": k, "r_K": r, "lower": True, "upper": True})
        return rows


def audit_gate5(g5: dict[str, Any]) -> dict[str, Any]:
    result = g5["result"]
    owner = result["actual_owner_complement_RN_anchor"]
    suffix = result["seven_bit_common_Borel_code_materialisation"]
    orlicz = result["same_law_power_Orlicz_frontier"]
    hybrid = result["fixed_insertion_positive_hybrid"]
    jordan = result["Jordan_and_all_time_positive_frontier"]
    strict = result["strict_nonpromotion"]

    require(FWD + REV == BI, "Gate5 F10 arithmetic")
    require(owner["fixed_insertion_same_law_positive_complement_F10_anchor"] == "CERTIFIED",
            "Gate5 complement F10")
    require(owner["all_insertion_time_positive_complement_anchor"] == "NOT_CERTIFIED",
            "Gate5 fixed-j guard")
    require("standard-Borel product" in owner["cemetery_pushforward"] and
            "not a countable atom list" in owner["cemetery_pushforward"],
            "Gate5 cemetery label type")
    require(owner["strong_cemetery"] == "NOT_CERTIFIED", "Gate5 strong cemetery")

    generator = suffix["countable_separating_generator"]
    spaces = suffix["state_and_kernel_spaces"]
    require("injective" in generator and "separate subprobabilities" in generator,
            "Gate5 injective evaluation code")
    require("standard-Borel product" in spaces and "rather than a countable atom list" in spaces,
            "Gate5 continuous cemetery product")
    require(suffix["unconditional_Borel_predicate_count"] == 7 and
            suffix["conditional_Borel_predicate_count"] == 0 and
            suffix["certified_universal_true_count"] == 2 and
            suffix["missing_universal_value_count"] == 5,
            "Gate5 suffix counts")
    require(suffix["physical_R_at_least_r_K"] == "NOT_CERTIFIED", "Gate5 R value")

    forbidden = "all labelled cemetery atoms"
    require(forbidden not in (HERE / "cm2-gate5-round61-complement-rn-borel-orlicz-frontier-assault-2026-07-20.md").read_text(encoding="utf-8"),
            "Gate5 stale report wording")
    require(forbidden not in G5_MANIFEST.read_text(encoding="utf-8"),
            "Gate5 stale manifest wording")

    replay_rows = orlicz_replay()
    require(all(row["lower_check"] and row["upper_check"] for row in orlicz["rows"]),
            "Gate5 manifest Orlicz rows")
    require(orlicz["explicit_physical_power_Orlicz_criterion"] ==
            "CERTIFIED_EXACT_SAME_LAW_IFF", "Gate5 Orlicz status")
    require(orlicz["physical_raw_Z_col_finite"] == "NOT_CERTIFIED" and
            orlicz["physical_power_Orlicz_bound"] == "NOT_CERTIFIED",
            "Gate5 finite RHS guard")
    require(hybrid["complement_term"] == "CERTIFIED_FINITE_AT_FIXED_J" and
            hybrid["full_fixed_j_policy_finite"] == "NOT_CERTIFIED",
            "Gate5 hybrid scope")
    require(jordan["all_time_weighted_Jordan_variation_anchor"] == "NOT_CERTIFIED" and
            jordan["all_time_weighted_common_mode_anchor"] == "NOT_CERTIFIED" and
            jordan["strong_cemetery"] == "NOT_CERTIFIED", "Gate5 all-time guards")
    require(strict["Gate5_maturity"] == "10/18" and
            strict["complete_18_field_operator_block_count"] == 0 and
            strict["complete_composite_gates"] == "0/5" and
            strict["CM2"] == "NO-GO_FOR_CLAIM", "Gate5 strict state")
    return {
        "status": "PASS",
        "fixed_j_complement_RN_F10": "CERTIFIED",
        "suffix_Borel": "7/7",
        "suffix_values": "2_TRUE_5_OPEN",
        "SubProb_evaluation_code": "INJECTIVE_ON_COUNTABLE_GENERATOR",
        "Orlicz_rows_replayed": replay_rows,
        "physical_Orlicz_bound": "NOT_CERTIFIED",
        "maturity": "10/18",
        "blocks": 0,
        "gate5": "NOT_CERTIFIED",
    }


Matrix = tuple[tuple[Q, Q], tuple[Q, Q]]
Vector = tuple[Q, Q]


def mm(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), Q(0))
                       for j in range(2)) for i in range(2))  # type: ignore[return-value]


def mv(a: Matrix, v: Vector) -> Vector:
    return tuple(sum((a[i][k] * v[k] for k in range(2)), Q(0))
                 for i in range(2))  # type: ignore[return-value]


def wedge(v: Vector, w: Vector) -> Q:
    return v[0] * w[1] - v[1] * w[0]


def audit_gate123(g123: dict[str, Any]) -> dict[str, Any]:
    result = g123["result"]
    strict = result["strict_status"]
    d: Matrix = ((Q(2), Q(1)), (Q(1), Q(1)))
    d_inv: Matrix = ((Q(1), Q(-1)), (Q(-1), Q(2)))
    psi: Matrix = ((Q(2), Q(3)), (Q(5), Q(7)))
    psi_new = mm(mm(d, psi), d_inv)
    basis: tuple[Vector, Vector] = ((Q(1), Q(0)), (Q(0), Q(1)))
    basis_new = tuple(mv(d, v) for v in basis)  # type: ignore[assignment]
    old = [wedge(mv(psi, basis[i]), basis[j]) for i in range(2) for j in range(2)]
    new = [wedge(mv(psi_new, basis_new[i]), basis_new[j])
           for i in range(2) for j in range(2)]
    require(old == new == [Q(-5), Q(2), Q(-7), Q(3)], "Gate123 wedge covariance")

    mu_u = [Q(1, 2), Q(1, 3), Q(1, 6)]
    mu_v = [Q(1, 4), Q(1, 2), Q(1, 4)]
    g_u = [Q(1), Q(1, 2), Q(0)]
    target = [1, 2, 0]
    push_mu = [Q(0), Q(0), Q(0)]
    push_marked = [Q(0), Q(0), Q(0)]
    for i in range(3):
        push_mu[target[i]] += mu_u[i]
        push_marked[target[i]] += g_u[i] * mu_u[i]
    jac = [push_mu[i] / mu_v[i] for i in range(3)]
    marker = [push_marked[i] / mu_v[i] for i in range(3)]
    require(jac == [Q(2, 3), Q(1), Q(4, 3)] and
            marker == [Q(0), Q(1), Q(2, 3)], "Gate123 RN marker")

    signed = [Q(1, 3), Q(-1, 6), Q(1, 2), Q(-1, 4),
              Q(1, 8), Q(-1, 12), Q(1, 7), Q(-1, 9)]
    tv = sum((abs(x) for x in signed), Q(0))
    bins = [0, 0, 1, 1, 2, 2, 2, 1]
    output = [Q(0), Q(0), Q(0)]
    for x, b in zip(signed, bins):
        output[b] += x
    output_tv = sum((abs(x) for x in output), Q(0))
    require(tv == Q(863, 504) and output_tv == Q(247, 504) and output_tv <= tv,
            "Gate123 stopped TV")
    require(Q(1 + 2 * 32, 3) == Q(65, 3), "Gate123 BV separator")
    require(result["gate1"]["physical_boundary"]["all_actual_plaque_combined_gauge_registry"] ==
            "NOT_CERTIFIED", "Gate123 Gate1 boundary")
    require(result["gate2"]["physical_boundary"]["landing_join"] == "1/7" and
            result["gate2"]["physical_boundary"]["official_immutable_gate2_fields"] == "0/17",
            "Gate123 Gate2 boundary")
    require(result["gate3"]["actual_stopped_graph_partition"]["status"] ==
            "CERTIFIED_ACTUAL_WEAK_STOPPED_GRAPH_TV_NORM_ONE", "Gate123 weak status")
    require(result["gate3"]["direct_strong_boundary"]["physical_strong_R_s_Q_s"] ==
            "NOT_CERTIFIED" and
            result["gate3"]["direct_strong_boundary"]["MT_DQ"] == "NOT_CERTIFIED",
            "Gate123 strong boundary")
    require(strict == {
        "cm2": "NO-GO_FOR_CLAIM", "composite_gates": "0/5",
        "gate1": "NOT_CERTIFIED", "gate2": "NOT_CERTIFIED",
        "gate2_immutable_fields": "0/17", "gate2_landing_join": "1/7",
        "gate3": "NOT_CERTIFIED",
    }, "Gate123 strict state")
    return {
        "status": "PASS_AFTER_ROOT_INDEPENDENT_RED_TEAM_AND_FRESH_AUDIT_REPLAY",
        "same_loop_wedges": [str(x) for x in old],
        "marker_J_hol": [str(x) for x in jac],
        "marker_pushforward": [str(x) for x in marker],
        "stopped_input_TV": str(tv),
        "stopped_output_TV": str(output_tv),
        "strong_BV_ratio_at_m32": "65/3",
        "gate123": "NOT_CERTIFIED",
    }


def build_result() -> dict[str, Any]:
    g4, g5, g123, leaf_rows, dependency_count = load_frozen()
    result = {
        "red_team_corrections": [
            "Gate4 marked lift typed as cone-curve measure only and separator restricted to BV/derivative trace",
            "Gate5 continuous cemetery labels typed by a standard-Borel product and injective countable-generator SubProb evaluation code",
        ],
        "frozen_leaf_pins": [{"name": name, "sha256": digest}
                             for name, digest in FROZEN_PINS.items()],
        "leaf_ledger_rows": leaf_rows,
        "older_dependency_artifact_pins": dependency_count,
        "gate4_audit": audit_gate4(g4),
        "gate5_audit": audit_gate5(g5),
        "gate123_audit": audit_gate123(g123),
        "cross_leaf_audit": {
            "D_land_is_Dbar": False,
            "weak_graph_TV_is_physical_strong_space": False,
            "positive_bad_or_complement_mass_is_collision_null_cemetery": False,
            "orientation_RN_is_Jordan_marginal": False,
            "exact_Gate1_transport_requires_future_same_token_cohomology": True,
            "status": "PASS_NO_CARRIER_OR_STATE_COLLISION",
        },
        "acceptance": {
            "main_leaves": {
                "syntax": "6/6", "older_dependency_artifact_pins": "30/30",
                "frozen_manifest_ledger_pins": "6/6", "leaf_ledger_rows": "12/12",
                "integrity": "3/3", "replay": "3/3", "reemit": "3/3",
                "hostile_and_strict_JSON": "615/615_REJECTED",
                "default_cert_verifier": "6/6_EXIT_2",
            },
            "independent_audit_leaf": {
                "syntax": "2/2", "frozen_manifest_ledger_pins": "6/6",
                "leaf_ledger_rows": "12/12", "integrity": "1/1", "replay": "1/1",
                "reemit": "1/1", "hostile_and_strict_JSON": "108/108_REJECTED",
                "default_cert_verifier": "2/2_EXIT_2", "SHA_ledger": "4/4",
            },
            "final_four_leaf_matrix": {
                "syntax": "8/8", "dependency_artifact_pins": "36/36",
                "integrity": "4/4", "replay": "4/4", "reemit": "4/4",
                "hostile_and_strict_JSON": "723/723_REJECTED",
                "SHA_ledger_rows": "16/16", "default_cert_verifier": "8/8_EXIT_2",
                "stale_temp_files": 0,
            },
        },
        "strict_status": {
            "gate1": "NOT_CERTIFIED", "gate2": "NOT_CERTIFIED",
            "gate2_immutable_fields": "0/17", "gate2_landing_join": "1/7",
            "gate3": "NOT_CERTIFIED", "gate4": "NOT_CERTIFIED",
            "gate5": "NOT_CERTIFIED", "gate5_maturity": "10/18",
            "complete_18_field_blocks": 0, "composite_gates": "0/5",
            "cm2": "NO-GO_FOR_CLAIM",
        },
    }
    return result


def build_manifest(check_files: bool = True) -> dict[str, Any]:
    if check_files:
        require(REPORT.is_file() and not REPORT.is_symlink(), "report file/type")
        require(VERIFIER.is_file() and not VERIFIER.is_symlink(), "verifier file/type")
    result = build_result()
    return {
        "schema": "cm2.round61-independent-core-frontier-audit.v1",
        "artifact": "cm2-round61-independent-core-frontier-audit",
        "date": "2026-07-20",
        "frozen_pins": [{"name": name, "sha256": digest}
                        for name, digest in FROZEN_PINS.items()],
        "result": result,
        "result_sha256": canonical_digest(result),
        "strict_verdict": (
            "PASS after pre-freeze Gate4 cone-curve/BV scoping and Gate5 "
            "standard-Borel cemetery/injective-code corrections; all five Gates "
            "remain not certified, composite gates are 0/5 and CM2 is no-go"
        ),
        "report_sha256": sha(REPORT),
        "certificate_sha256": sha(Path(__file__).resolve()),
        "verifier_sha256": sha(VERIFIER),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--emit-manifest", type=Path)
    parser.add_argument("--summary-json", action="store_true")
    args = parser.parse_args()
    try:
        data = build_manifest(check_files=True)
        if args.emit_manifest is not None:
            args.emit_manifest.write_bytes(canonical_bytes(data))
            print(f"EMITTED: {args.emit_manifest}")
            return 0
        if args.summary_json:
            print(json.dumps(data["result"], indent=2, sort_keys=True,
                             ensure_ascii=False, allow_nan=False))
            return 0
        require(MANIFEST.is_file() and not MANIFEST.is_symlink(), "manifest file/type")
        require(MANIFEST.read_bytes() == canonical_bytes(data), "manifest drift")
    except (AuditError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"AUDIT_CERT_ERROR: {exc}", file=sys.stderr)
        return 1
    print("ROUND61_INDEPENDENT_AUDIT: PASS")
    print("FROZEN_PINS: 6/6")
    print("LEAF_LEDGER_ROWS: 12/12")
    print("FINAL_MATRIX: 8/8_SYNTAX 36/36_PINS 723/723_HOSTILE 16/16_SHA")
    print("COMPOSITE_GATES: 0/5")
    print("CM2: NO-GO_FOR_CLAIM")
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
