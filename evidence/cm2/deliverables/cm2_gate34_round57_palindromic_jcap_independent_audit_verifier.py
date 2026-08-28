#!/usr/bin/env python3
"""Fail-closed verifier for the independent Round-57 J_cap audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round57_palindromic_jcap_independent_audit_cert as cert


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE
    / "cm2-gate34-round57-palindromic-jcap-independent-audit-manifest-2026-07-20.json"
)

CLOSED_A = Q(360134800, 360493663)
C_P = Q(4 * 10**90 * 360493663, 358863)
CUT_Z1 = Q(18367592526, 360493663)
PAL_MASS_COEFF = (CUT_Z1 + 1) * C_P / 2


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_q(text: str) -> Q:
    return Q(text)


def strict_load_bytes(raw: bytes) -> dict[str, Any]:
    text = raw.decode("utf-8")
    value = json.loads(
        text,
        object_pairs_hook=cert.strict_object,
        parse_constant=cert.reject_constant,
    )
    require(isinstance(value, dict), "manifest root")
    return value


def safe_local(path: Path) -> Path:
    path = path.resolve()
    require(path.is_file() and not path.is_symlink(), "manifest path")
    require(path.parent == HERE, "manifest scope")
    return path


def expected_direction_rows() -> list[dict[str, str]]:
    return [
        {"step": "0", "operation": "start", "point": "x"},
        {"step": "1", "operation": "T_s^(K-1)", "point": "T_s^(K-1)x"},
        {"step": "2", "operation": "O_s transfer then kill", "point": "T_s^K x on survivors"},
        {"step": "3", "operation": "I", "point": "I T_s^K x"},
        {"step": "4", "operation": "T_s^K", "point": "I x"},
        {"step": "5", "operation": "I", "point": "x"},
    ]


def expected_growth_rows() -> list[dict[str, str]]:
    qstr = cert.qstr
    return [
        {"stage": "input_x", "A_on_Z_in": "1", "B_on_mass_in": "0"},
        {"stage": "closed_T_power_K_minus_1", "A_on_Z_in": "1", "B_on_mass_in": qstr(C_P / 2)},
        {"stage": "O_supplies_collision_K", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(CUT_Z1 * C_P / 2)},
        {"stage": "time_reversal_I", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(CUT_Z1 * C_P / 2)},
        {"stage": "closed_reverse_T_power_K", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(PAL_MASS_COEFF)},
        {"stage": "final_I_returns_x", "A_on_Z_in": qstr(CUT_Z1), "B_on_mass_in": qstr(PAL_MASS_COEFF)},
    ]


def expected_strict() -> dict[str, Any]:
    return {
        "physical_common_refinement_J_cap_total": "CERTIFIED_FINITE_AUDIT_PASS",
        "single_common_properisation_clock_D_cap_moment": "CERTIFIED_FINITE_AUDIT_PASS",
        "physical_full_dyadic_D_cap_first_moment": "CERTIFIED_FINITE_AUDIT_PASS",
        "proper_common_terminal_two_view_carrier": "CERTIFIED_AUDIT_PASS",
        "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_properisation": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
        "audit_verdict": "PASS_NO_REMAINING_BLOCKER_FOR_CLAIMED_SCOPE",
    }


def independent_checks(manifest: dict[str, Any]) -> None:
    require(manifest["schema"] == cert.MANIFEST_SCHEMA, "manifest schema")
    require(manifest["dependencies"] == cert.PINNED_FILES, "dependency ledger")
    result = manifest["result"]
    require(result["schema"] == cert.RESULT_SCHEMA, "result schema")
    require(result["provenance"]["audited_artifacts_modified"] is False, "read-only audit")
    require(result["provenance"]["pinned_sha256"] == cert.PINNED_FILES, "provenance pins")
    require(
        result["internal_replay_digest"]
        == cert.digest({k: v for k, v in result.items() if k != "internal_replay_digest"}),
        "result digest",
    )

    freeze = result["artifact_freeze_audit"]
    require(freeze["frozen_main_manifest"] == cert.MAIN_MANIFEST, "main filename")
    require(freeze["frozen_main_manifest_sha256"] == cert.PINNED_FILES[cert.MAIN_MANIFEST], "main SHA")
    require(freeze["audited_files_modified"] is False, "artifact immutability")

    direction = result["reversible_operator_audit"]
    require(direction["rows"] == expected_direction_rows(), "direction replay")
    require(direction["rows_sha256"] == cert.digest(direction["rows"]), "direction digest")
    require(direction["rows"][2]["point"] == "T_s^K x on survivors", "O lands at K")
    require(direction["rows"][4]["point"] == "I x", "reverse closed leg")
    require(direction["rows"][-1]["point"] == "x", "palindrome returns")

    clock = result["tagged_clock_Borel_audit"]
    require(clock["clock"] == "K(c)=696*Dbar(c)+H_joint>=1", "clock formula")
    require("never recomputed" in clock["tag_constancy"], "immutable K")
    require("countable disjoint finite-K strata" in clock["Borel_reason"], "Borel strata")
    require("parent y, not at proof cell c" in clock["mass_index_layer"], "mass index")

    growth = result["affine_Growth_audit"]
    require(growth["rows"] == expected_growth_rows(), "Growth rows")
    require(growth["rows_sha256"] == cert.digest(growth["rows"]), "Growth digest")
    require(CLOSED_A < 1 and CUT_Z1 > 1, "Growth constants")
    require(parse_q(growth["rows"][-1]["A_on_Z_in"]) == CUT_Z1, "final A")
    require(parse_q(growth["rows"][-1]["B_on_mass_in"]) == PAL_MASS_COEFF, "final B")
    require("arbitrarily thin and nonproper" in growth["second_input"], "nonproper second input")
    require("exactly one Z1 multiplier" in growth["mass_multiplier_is_single_cut"], "single cut multiplier")
    require("Round47 P*mass" in growth["marginal_separation"], "proper envelope excluded")

    replay = result["paired_first_return_replay_audit"]
    require(replay["forward"] == "A -> B=T_s^n(A) -> I(B)", "forward direction")
    require(replay["reverse"].startswith("I(B) -> I(A)"), "reverse direction")
    require("no transverse redisintegration" in replay["forbidden_shortcuts"], "no transverse shortcut")
    require("no" in replay["forbidden_shortcuts"] and "duplicate charge" in replay["forbidden_shortcuts"], "once charge")
    require(replay["common_raw_set"].endswith("S_fw intersect S_rev"), "same raw set")

    component = result["component_global_join_audit"]
    require("actual-union connected" in component["physical_merge_rule"], "actual connected merge")
    require("never merge across an omitted" in component["puncture_rule"], "puncture split")
    require("J_cap,physical<=Z_cap,proof" in component["coarsening"], "coarsening")
    require(component["global_result"].endswith("<infinity"), "global Jcap")
    require("exp(D_cap/6)" in component["Round53_result"], "Dcap exp moment")
    require("full dyadic first moment" in component["Round53_result"], "Dcap dyadic moment")

    strict = result["strict_scope_audit"]
    require(strict == expected_strict(), "strict scope")
    require(manifest["verdict"] == strict, "verdict parity")


def verify_value(value: dict[str, Any], expected: dict[str, Any]) -> None:
    require(set(value) == set(expected), "top-level keys")
    require(value == expected, "deterministic manifest mismatch")
    require(value["certificate_sha256"] == sha256_path(HERE / "cm2_gate34_round57_palindromic_jcap_independent_audit_cert.py"), "certificate hash")
    require(value["verifier_sha256"] == sha256_path(Path(__file__).resolve()), "verifier hash")
    independent_checks(value)


def verify_manifest(path: Path) -> tuple[dict[str, Any], bytes, bytes]:
    path = safe_local(path)
    raw = path.read_bytes()
    value = strict_load_bytes(raw)
    expected = cert.build_manifest(Path(__file__).resolve())
    verify_value(value, expected)
    for name, expected_hash in cert.PINNED_FILES.items():
        dependency = HERE / name
        require(dependency.is_file() and not dependency.is_symlink(), f"dependency path: {name}")
        require(dependency.resolve().parent == HERE, f"dependency scope: {name}")
        require(sha256_path(dependency) == expected_hash, f"dependency hash: {name}")
    reemitted = (json.dumps(expected, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return value, raw, reemitted


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    node: Any = value
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = replacement


def hostile_mutations(base: dict[str, Any]) -> list[dict[str, Any]]:
    specs: list[tuple[tuple[Any, ...], Any]] = [
        (("schema",), "wrong.schema"),
        (("certificate_sha256",), "0" * 64),
        (("verifier_sha256",), "1" * 64),
        (("dependencies", cert.MAIN_MANIFEST), "2" * 64),
        (("result", "schema"), "wrong.result"),
        (("result", "provenance", "audited_artifacts_modified"), True),
        (("result", "provenance", "parameter_scope"), "moving sequence"),
        (("result", "artifact_freeze_audit", "frozen_main_manifest_sha256"), "3" * 64),
        (("result", "artifact_freeze_audit", "audited_files_modified"), True),
        (("result", "artifact_freeze_audit", "status"), "FAIL"),
        (("result", "reversible_operator_audit", "reversibility_identity"), "false"),
        (("result", "reversible_operator_audit", "off_by_one"), "first leg K"),
        (("result", "reversible_operator_audit", "return_direction"), "T^K returns x directly"),
        (("result", "reversible_operator_audit", "rows", 1, "operation"), "T_s^K"),
        (("result", "reversible_operator_audit", "rows", 2, "point"), "T_s^(K+1)x"),
        (("result", "reversible_operator_audit", "rows", 4, "point"), "x"),
        (("result", "reversible_operator_audit", "rows", 5, "point"), "I x"),
        (("result", "reversible_operator_audit", "rows_sha256"), "4" * 64),
        (("result", "tagged_clock_Borel_audit", "clock"), "K=H"),
        (("result", "tagged_clock_Borel_audit", "tag_constancy"), "recompute after I"),
        (("result", "tagged_clock_Borel_audit", "Borel_reason"), "uncountable union"),
        (("result", "tagged_clock_Borel_audit", "mass_index_layer"), "cellwise 249/250"),
        (("result", "tagged_clock_Borel_audit", "terminal_scope"), "all intermediate collisions"),
        (("result", "affine_Growth_audit", "closed_recurrence"), "no additive mass"),
        (("result", "affine_Growth_audit", "one_cut"), "proper inputs only"),
        (("result", "affine_Growth_audit", "second_input"), "original Dbar makes it proper"),
        (("result", "affine_Growth_audit", "uniform_final_bound"), "infinite"),
        (("result", "affine_Growth_audit", "mass_multiplier_is_single_cut"), "two cuts"),
        (("result", "affine_Growth_audit", "marginal_separation"), "rerun SYZ conditionally"),
        (("result", "affine_Growth_audit", "rows", 1, "stage"), "closed_T_power_K"),
        (("result", "affine_Growth_audit", "rows", 2, "A_on_Z_in"), "1"),
        (("result", "affine_Growth_audit", "rows", 4, "B_on_mass_in"), "0"),
        (("result", "affine_Growth_audit", "rows_sha256"), "5" * 64),
        (("result", "paired_first_return_replay_audit", "forward"), "A -> I(B) directly"),
        (("result", "paired_first_return_replay_audit", "reverse"), "I(B) -> A"),
        (("result", "paired_first_return_replay_audit", "reverse_identity"), "wrong direction"),
        (("result", "paired_first_return_replay_audit", "first_return_scope"), "new proper first return certified"),
        (("result", "paired_first_return_replay_audit", "refinement_policy"), "transverse redisintegration"),
        (("result", "paired_first_return_replay_audit", "forbidden_shortcuts"), "normalize twice"),
        (("result", "paired_first_return_replay_audit", "common_raw_set"), "two raw charges"),
        (("result", "component_global_join_audit", "proof_kernel"), "non-Borel"),
        (("result", "component_global_join_audit", "physical_merge_rule"), "merge whenever closures touch"),
        (("result", "component_global_join_audit", "puncture_rule"), "merge across cemetery punctures"),
        (("result", "component_global_join_audit", "Borel_registry"), "no owner"),
        (("result", "component_global_join_audit", "coarsening"), "Jcap physical is larger"),
        (("result", "component_global_join_audit", "global_result"), "J_cap=infinity"),
        (("result", "component_global_join_audit", "Round53_result"), "physical q certified"),
        (("result", "strict_scope_audit", "physical_common_refinement_J_cap_total"), "NOT_CERTIFIED"),
        (("result", "strict_scope_audit", "single_common_properisation_clock_D_cap_moment"), "NOT_CERTIFIED"),
        (("result", "strict_scope_audit", "physical_full_dyadic_D_cap_first_moment"), "NOT_CERTIFIED"),
        (("result", "strict_scope_audit", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED"),
        (("result", "strict_scope_audit", "intermediate_C24_avoidance_after_properisation"), "CERTIFIED"),
        (("result", "strict_scope_audit", "later_and_repeated_recovery_clock_moments"), "CERTIFIED"),
        (("result", "strict_scope_audit", "physical_collision_time_q_L6over5"), "CERTIFIED"),
        (("result", "strict_scope_audit", "strong_singular_current_cemetery"), "CERTIFIED"),
        (("result", "strict_scope_audit", "Gate4"), "CERTIFIED"),
        (("result", "strict_scope_audit", "CM2"), "CERTIFIED"),
        (("result", "strict_scope_audit", "audit_verdict"), "FAIL"),
        (("result", "internal_replay_digest"), "6" * 64),
        (("verdict", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED"),
        (("verdict", "physical_collision_time_q_L6over5"), "CERTIFIED"),
    ]
    out: list[dict[str, Any]] = []
    for path, replacement in specs:
        mutated = copy.deepcopy(base)
        set_path(mutated, path, replacement)
        out.append(mutated)
    removed = copy.deepcopy(base)
    del removed["result"]["component_global_join_audit"]
    out.append(removed)
    added = copy.deepcopy(base)
    added["unexpected"] = True
    out.append(added)
    return out


def self_test(expected: dict[str, Any]) -> int:
    rejected = 0
    for mutated in hostile_mutations(expected):
        try:
            verify_value(mutated, expected)
        except Exception:
            rejected += 1
    require(rejected == len(hostile_mutations(expected)), "hostile mutation escaped")
    for raw in (
        b'{"x":1,"x":2}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
    ):
        try:
            strict_load_bytes(raw)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("strict parser probe escaped")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", action="store_true")
    args = parser.parse_args()

    manifest, raw, reemitted = verify_manifest(args.manifest)
    if args.self_test:
        rejected = self_test(manifest)
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{len(hostile_mutations(manifest)) + 3}")
        return 0
    if args.reemit:
        require(raw == reemitted, "reemit mismatch")
        print("REEMIT_BYTE_IDENTICAL: PASS")
        return 0
    strict = manifest["result"]["strict_scope_audit"]
    if args.audit:
        print("INDEPENDENT_AUDIT: PASS")
        print("MAIN_MANIFEST_SHA256:", cert.PINNED_FILES[cert.MAIN_MANIFEST])
        print("PHYSICAL_J_CAP:", strict["physical_common_refinement_J_cap_total"])
        print("D_CAP_MOMENT:", strict["single_common_properisation_clock_D_cap_moment"])
        print("PHYSICAL_FIRST_RETURN:", strict["physical_proper_same_ID_first_return_kernel"])
        print("PHYSICAL_Q:", strict["physical_collision_time_q_L6over5"])
        print("GATE4:", strict["Gate4"])
        print("CM2:", strict["CM2"])
        return 0
    print("INDEPENDENT_AUDIT:", strict["audit_verdict"])
    print("PHYSICAL_J_CAP:", strict["physical_common_refinement_J_cap_total"])
    print("PHYSICAL_FIRST_RETURN:", strict["physical_proper_same_ID_first_return_kernel"])
    print("PHYSICAL_Q:", strict["physical_collision_time_q_L6over5"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
