#!/usr/bin/env python3
"""Independent verifier for the Round-53 Gate-4 fractional-Z leaf."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERT = HERE / "cm2_gate34_round53_fractional_z_common_return_frontier_cert.py"
MANIFEST = (
    HERE
    / "cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json"
)
RESULT_SCHEMA = "cm2.gate34.round53-fractional-z-common-return-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
EXPECTED_DEPENDENCIES = {
    "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json": (
        "7ddecb544fa5a2b243882eaf2028159c22f8437fc3fbb49fda4eb487ab181798"
    ),
    "cm2-gate34-round51-two-proper-view-common-law-manifest-2026-07-20.json": (
        "028c5a8f59a6efffa9df93cfba841f3844d244988dc235038183eef222d21abc"
    ),
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json": (
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73"
    ),
    "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json": (
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c"
    ),
    "cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json": (
        "7980e90ce45edfd3012b265315e6877e38eb4604ab0219205ec966ad43a8cd75"
    ),
    "cm2-gate45-round36-aggregate-z-route-manifest-2026-07-19.json": (
        "8b6bd9a1b72e1d222ea0b370f046defbf90b10935c55271d4f5bf81a36835ba5"
    ),
    "cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json": (
        "ca623e4c350b75f0fec889d0909b052bb0493613ff2f983ac71fd2fca40e016b"
    ),
    "cm2-gate45-round28-weighted-tail-transfer-frontier-manifest-2026-07-18.json": (
        "eef1071c1f4973892bf5e450421f3b91de7a2b426165e6a8c6f8bb4404eeac57"
    ),
}

CLOSED_A = Q(360134800, 360493663)
CLOSED_B = 2 * 10**90
C_P = Q(4 * 10**90 * 360493663, 358863)
COEFFICIENT = Q(35, 99 * 2**309)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"non-finite JSON constant: {token}")


def strict_load(path: Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
        raise RuntimeError(f"unsafe input: {path}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError("manifest root is not an object")
    return value


def parse_q(value: str | int) -> Q:
    return Q(value)


def get_path(root: Any, path: tuple[str | int, ...]) -> Any:
    value = root
    for key in path:
        value = value[key]
    return value


def set_path(root: Any, path: tuple[str | int, ...], value: Any) -> None:
    target = root
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


REQUIRED_FIELDS: list[tuple[tuple[str | int, ...], Any]] = [
    (("schema",), RESULT_SCHEMA),
    (("provenance", "old_artifacts_modified"), False),
    (("provenance", "external_theorem_promoted"), False),
    (
        ("fractional_cell_Z_to_defect_moment", "status"),
        "CERTIFIED_EXACT_SAME_MEASURE_CELL_Z_TO_DEFECT_MOMENT_BRIDGE__PHYSICAL_J_PAIR_OPEN",
    ),
    (
        ("fractional_cell_Z_to_defect_moment", "pair_boundary_numerator"),
        "J_pair=integral sum_c p_c*(ell_fw,c^-1+ell_rev,c^-1) dlambda",
    ),
    (
        ("fractional_cell_Z_to_defect_moment", "strict_event_identity"),
        "for every integer m>=0, {M_c>m}={min(ell_fw,c,ell_rev,c)<2^-m}",
    ),
    (("fractional_cell_Z_to_defect_moment", "no_rounding_loss"), True),
    (
        ("fractional_cell_Z_to_defect_moment", "direct_linear_tail_coefficient"),
        str(COEFFICIENT),
    ),
    (
        ("fractional_cell_Z_to_defect_moment", "equivalent_coefficient_form"),
        "(70/99)*2^-310",
    ),
    (("fractional_cell_Z_to_defect_moment", "physical_J_pair_certified"), False),
    (("fractional_cell_Z_to_defect_moment", "physical_I_D_certified"), False),
    (
        ("aggregate_Z_cross_gate_bridge", "status"),
        "CERTIFIED_ABSTRACT_L1_RESOLVENT_TO_GATE4_DEFECT_BRIDGE__PHYSICAL_MASS_NORMALIZATION_FACE_TOWER_AND_EXTRACTION_OPEN",
    ),
    (("aggregate_Z_cross_gate_bridge", "a"), "360134800/360493663"),
    (("aggregate_Z_cross_gate_bridge", "b"), str(CLOSED_B)),
    (("aggregate_Z_cross_gate_bridge", "exact_l1_resolvent"), "360493663/358863"),
    (("aggregate_Z_cross_gate_bridge", "return_tail_constants", "A"), "550000/147"),
    (
        ("aggregate_Z_cross_gate_bridge", "return_tail_constants", "r"),
        "111718729/111718750",
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "collision_mass_term"),
        "conditional only: if a same-ID level/normalization theorem identifies the Round36 unnormalised m_n with mu_s(C_s)*S_n (or gives an explicit fixed index shift and domination by it), then the Round28 tail gives sum_n m_n<mu_s(C_s)*A*N_open/(1-r)<infinity",
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "round28_Qn_to_round36_mn_same_ID_normalization_join"),
        "NOT_CERTIFIED",
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "round28_tail_supplies_join_1_without_typing"),
        False,
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "fixed_insertion_owner_tail_supplies_join_2"),
        False,
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "abstract_growth_recurrence_supplies_join_3"),
        False,
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "required_physical_join_1"),
        "a same-ID level-index and normalization theorem from Round28 S_n=mu_s(Q_n)/mu_s(C_s) to the Round36 unnormalised recurrence mass m_n",
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "required_physical_join_2"),
        "an all-insertion-time same-ID face-tower L1 bound for the full F_n, including cemetery",
    ),
    (
        ("aggregate_Z_cross_gate_bridge", "required_physical_join_3"),
        "a terminal-extraction inequality on the same cell law which bounds J_pair by the evolved aggregate Z plus terminal face injection",
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "status"),
        "CERTIFIED_CONDITIONAL_COMMON_REFINEMENT_Z_TO_TWO_VIEW_PROPERISATION_AND_CLOCK_MOMENT__PHYSICAL_J_CAP_OPEN",
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "component_registry_hypothesis"),
        "both orientation decompositions of the common raw restriction are standard-Borel regular connected-component kernels with exact outer disintegration and no duplicate charge",
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "physical_common_refinement_J_cap_certified"),
        False,
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "physical_proper_same_ID_return_certified"),
        False,
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "minimality_inequality"),
        "for D_cap>0, minimality gives 2^D_cap<=4*z_cap/C_p",
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "physical_kernel_typing_boundary"),
        "two proper orientation-specific pushforwards of one common raw restriction give a proper two-view reference carrier; they are not thereby one physical first-return kernel",
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "what_this_does_not_certify", 0),
        "intermediate C24 avoidance or the physical first-return interpretation",
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "what_this_does_not_certify", 2),
        "the Round28 physical collision-time q",
    ),
    (
        ("common_refinement_Z_to_proper_return_clock", "what_this_does_not_certify", 3),
        "the strong singular/current cemetery",
    ),
    (
        ("two_Z_and_cemetery_nonimplication_audit", "status"),
        "CERTIFIED_SEPARATION_OF_D1_FIXED_TIME_OWNER_MARGINAL_Z_AND_STRONG_CEMETERY_FROM_THE_TWO_TARGET_Z_QUANTITIES",
    ),
    (
        ("two_Z_and_cemetery_nonimplication_audit", "physical_J_pair_or_J_cap_disproved"),
        False,
    ),
    (("compressed_physical_frontier", "physical_J_pair"), "NOT_CERTIFIED"),
    (("compressed_physical_frontier", "physical_I_D"), "NOT_CERTIFIED"),
    (
        ("compressed_physical_frontier", "round28_Qn_to_round36_mn_same_ID_normalization_join"),
        "NOT_CERTIFIED",
    ),
    (
        ("compressed_physical_frontier", "proper_same_ID_physical_return"),
        "NOT_CERTIFIED",
    ),
    (
        ("compressed_physical_frontier", "physical_collision_time_q_L6over5"),
        "NOT_CERTIFIED",
    ),
    (
        ("compressed_physical_frontier", "strong_singular_current_cemetery"),
        "NOT_CERTIFIED",
    ),
    (("strict_nonpromotion", "same_measure_cell_Z_to_defect_bridge"), "CERTIFIED_CONDITIONAL_THEOREM"),
    (("strict_nonpromotion", "abstract_aggregate_Z_l1_resolvent"), "CERTIFIED"),
    (
        ("strict_nonpromotion", "common_refinement_Z_to_extra_clock_bridge"),
        "CERTIFIED_CONDITIONAL_THEOREM",
    ),
    (("strict_nonpromotion", "physical_J_pair"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "physical_defect_moment_I_D"), "NOT_CERTIFIED"),
    (
        ("strict_nonpromotion", "round28_Qn_to_round36_mn_same_ID_normalization_join"),
        "NOT_CERTIFIED",
    ),
    (
        ("strict_nonpromotion", "physical_all_time_face_tower_and_terminal_extraction"),
        "NOT_CERTIFIED",
    ),
    (("strict_nonpromotion", "physical_common_refinement_J_cap"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "proper_same_ID_geometric_return"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "physical_collision_time_q_L6over5"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "strong_singular_current_cemetery"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "Gate4"), "NOT_CERTIFIED"),
    (("strict_nonpromotion", "complete_composite_gates"), "0/5"),
    (("strict_nonpromotion", "CM2"), "NO-GO_FOR_CLAIM"),
]


def validate_required_fields(result: dict[str, Any]) -> None:
    for path, expected in REQUIRED_FIELDS:
        actual = get_path(result, path)
        if actual != expected:
            raise RuntimeError(f"required field mismatch: {path}: {actual!r}")


def independent_arithmetic(result: dict[str, Any]) -> None:
    # exp(1/6)<13/11 with a rational series remainder.
    tail = Q(1, 72) / (1 - Q(1, 18))
    upper_series = 1 + Q(1, 6) + tail
    if tail != Q(1, 68) or upper_series != Q(241, 204):
        raise RuntimeError("exponential series remainder")
    if 13 * 204 - 241 * 11 != 1 or not upper_series < Q(13, 11):
        raise RuntimeError("exponential rational bracket")

    r = Q(13, 11)
    head = (r**2 - 1) / Q(2**310)
    tail_coeff = (r - 1) / Q(2**309) * ((r / 2) ** 2 / (1 - r / 2))
    if head + tail_coeff != COEFFICIENT:
        raise RuntimeError("linear-tail layer-cake coefficient")
    bridge = result["fractional_cell_Z_to_defect_moment"]
    if parse_q(bridge["direct_linear_tail_coefficient"]) != COEFFICIENT:
        raise RuntimeError("manifest coefficient")

    rows = bridge["rows"]
    if digest(rows) != bridge["rows_sha256"]:
        raise RuntimeError("cell rows digest")
    expected_M = [14, 310, 311, 400, 576]
    expected_powers = [3, 7, 11, 20, 24]
    for row, M, power in zip(rows, expected_M, expected_powers, strict=True):
        p = Q(1, 2**power)
        ell_fw = Q(1, 2**M)
        ell_rev = Q(1, 2 ** max(0, M - 3))
        pair_z = p / ell_fw + p / ell_rev
        if row["M"] != M or parse_q(row["mass"]) != p:
            raise RuntimeError("cell row mass/rank")
        if parse_q(row["ell_fw"]) != ell_fw or parse_q(row["ell_rev"]) != ell_rev:
            raise RuntimeError("cell row lengths")
        if parse_q(row["pair_boundary_contribution"]) != pair_z:
            raise RuntimeError("cell row pair Z")
        expected_d = 0 if M <= 310 else M - 309
        if row["safe_defect_Dbar"] != expected_d:
            raise RuntimeError("cell row defect")
        # At m=M-1, min ell=2^-M is strictly less than 2^-(M-1),
        # while p/min ell is one summand in J_pair.
        if M > 0 and not p < Q(1, 2 ** (M - 1)) * pair_z:
            raise RuntimeError("strict cell tail event")

    agg = result["aggregate_Z_cross_gate_bridge"]
    if Q(1, 1) / (1 - CLOSED_A) != Q(360493663, 358863):
        raise RuntimeError("aggregate resolvent")
    if Q(111718750 - 111718729, 111718750) != Q(21, 111718750):
        raise RuntimeError("return-tail gap")
    agg_rows = agg["rows"]
    if digest(agg_rows) != agg["rows_sha256"]:
        raise RuntimeError("aggregate rows digest")
    z = Q(7, 5)
    for n, row in enumerate(agg_rows):
        mass = Q(1, 2 ** (n + 1))
        forcing = Q(1, 3 ** (n + 1))
        z_next = CLOSED_A * z + CLOSED_B * mass + forcing
        if row["n"] != n or parse_q(row["Z_n"]) != z:
            raise RuntimeError("aggregate Z row")
        if parse_q(row["m_n"]) != mass or parse_q(row["face_forcing_F_n"]) != forcing:
            raise RuntimeError("aggregate forcing row")
        if parse_q(row["equality_model_Z_next"]) != z_next:
            raise RuntimeError("aggregate recurrence row")
        z = z_next

    common = result["common_refinement_Z_to_proper_return_clock"]
    if not 2 * CLOSED_A.numerator**696 < CLOSED_A.denominator**696:
        raise RuntimeError("696 half-block")
    common_rows = common["rows"]
    if digest(common_rows) != common["rows_sha256"]:
        raise RuntimeError("common rows digest")
    expected_k = [-1, 0, 1, 4, 12, 32]
    for row, k in zip(common_rows, expected_k, strict=True):
        z_norm = C_P / 2 if k == -1 else C_P * 2**k
        if z_norm < C_P:
            d = 0
        else:
            d = 1
            while Q(1, 2**d) * z_norm >= C_P / 2:
                d += 1
        if row["extra_block_defect_D_cap"] != d:
            raise RuntimeError("common defect row")
        if row["extra_clock_696_D_cap"] != 696 * d:
            raise RuntimeError("common clock row")
        if d and not Q(2**d) <= 4 * z_norm / C_P:
            raise RuntimeError("common minimality inequality")
        if row["two_power_relation"] is not True:
            raise RuntimeError("common relation flag")
        # Pure rational fourth-power check for
        # (13/11)^d < (13/11)^3*2^(d/4).
        if not Q(13, 11) ** (4 * d) < Q(13, 11) ** 12 * 2**d:
            raise RuntimeError("common quarter-power bound")

    sep = result["two_Z_and_cemetery_nonimplication_audit"]
    sep_rows = sep["rows"]
    if digest(sep_rows) != sep["rows_sha256"]:
        raise RuntimeError("separator rows digest")
    for row, n in zip(sep_rows, [18, 19, 20, 24], strict=True):
        M = n * n
        d = M - 309
        lower = Q(1, 2**n) * Q(7, 6) ** d
        ratio = Q(1, 2) * Q(7, 6) ** (2 * n + 1)
        if row["band_n"] != n or row["Dbar"] != d:
            raise RuntimeError("separator rank row")
        if parse_q(row["defect_moment_rational_lower"]) != lower:
            raise RuntimeError("separator moment row")
        if parse_q(row["next_lower_term_ratio"]) != ratio or not ratio > 1:
            raise RuntimeError("separator ratio row")


def validate_result(result: dict[str, Any]) -> None:
    expected_keys = {
        "schema",
        "provenance",
        "fractional_cell_Z_to_defect_moment",
        "aggregate_Z_cross_gate_bridge",
        "common_refinement_Z_to_proper_return_clock",
        "two_Z_and_cemetery_nonimplication_audit",
        "compressed_physical_frontier",
        "strict_nonpromotion",
        "internal_replay_digest",
    }
    if set(result) != expected_keys:
        raise RuntimeError("result top-level key set")
    validate_required_fields(result)
    independent_arithmetic(result)
    payload = copy.deepcopy(result)
    stored = payload.pop("internal_replay_digest")
    if digest(payload) != stored:
        raise RuntimeError("internal replay digest")


def audit_integrity(manifest: dict[str, Any]) -> None:
    if set(manifest) != {
        "schema",
        "certificate_sha256",
        "verifier_sha256",
        "dependencies",
        "result",
        "verdict",
    }:
        raise RuntimeError("manifest top-level key set")
    if manifest["schema"] != MANIFEST_SCHEMA:
        raise RuntimeError("manifest schema")
    if manifest["certificate_sha256"] != sha(CERT):
        raise RuntimeError("certificate SHA")
    if manifest["verifier_sha256"] != sha(Path(__file__).resolve()):
        raise RuntimeError("verifier SHA")
    if manifest["dependencies"] != EXPECTED_DEPENDENCIES:
        raise RuntimeError("dependency map")
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = HERE / name
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise RuntimeError(f"unsafe dependency: {name}")
        if sha(path) != expected:
            raise RuntimeError(f"dependency SHA: {name}")
    validate_result(manifest["result"])
    if manifest["verdict"] != manifest["result"]["strict_nonpromotion"]:
        raise RuntimeError("verdict/result mismatch")


def load_certificate_module() -> Any:
    spec = importlib.util.spec_from_file_location("cm2_round53_fractional_z_cert", CERT)
    if spec is None or spec.loader is None:
        raise RuntimeError("certificate import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(manifest: dict[str, Any]) -> None:
    module = load_certificate_module()
    if module.RESULT_SCHEMA != RESULT_SCHEMA or module.MANIFEST_SCHEMA != MANIFEST_SCHEMA:
        raise RuntimeError("certificate schema constants")
    if module.DEPENDENCIES != EXPECTED_DEPENDENCIES:
        raise RuntimeError("certificate dependencies")
    expected = module.build_result()
    if expected != manifest["result"]:
        raise RuntimeError("certificate replay mismatch")


def mutation_value(value: Any, variant: int) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + variant + 1
    if isinstance(value, str):
        return value + f"__MUT{variant}"
    if isinstance(value, list):
        return value + [f"MUT{variant}"]
    if value is None:
        return f"MUT{variant}"
    raise RuntimeError(f"unsupported hostile target type: {type(value)}")


def hostile_tests(manifest: dict[str, Any]) -> tuple[int, int]:
    rejected = 0
    total = 0
    # Three independently digested mutations for every substantive field.
    for path, _expected in REQUIRED_FIELDS:
        for variant in range(3):
            total += 1
            bad = copy.deepcopy(manifest)
            old = get_path(bad["result"], path)
            set_path(bad["result"], path, mutation_value(old, variant))
            payload = copy.deepcopy(bad["result"])
            payload.pop("internal_replay_digest")
            bad["result"]["internal_replay_digest"] = digest(payload)
            if path and path[0] == "strict_nonpromotion":
                bad["verdict"] = copy.deepcopy(bad["result"]["strict_nonpromotion"])
            try:
                validate_result(bad["result"])
                if bad["verdict"] != bad["result"]["strict_nonpromotion"]:
                    raise RuntimeError("verdict mismatch")
            except Exception:
                rejected += 1

    # Strict parser rejects duplicate keys and non-finite constants.
    parser_cases = [
        '{"a":1,"a":2}',
        '{"x":NaN}',
        '{"x":Infinity}',
        '{"x":-Infinity}',
    ]
    for raw in parser_cases:
        total += 1
        try:
            json.loads(raw, object_pairs_hook=strict_object, parse_constant=reject_constant)
        except Exception:
            rejected += 1
    return rejected, total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit-manifest", type=Path)
    args = parser.parse_args()

    manifest = strict_load(args.manifest)
    audit_integrity(manifest)
    if args.integrity_only:
        print("AUDIT_MODE: PASS")
        return 0

    replay(manifest)
    if args.reemit_manifest:
        module = load_certificate_module()
        module.write_manifest(args.reemit_manifest, Path(__file__).resolve())
        print(f"REEMITTED: {args.reemit_manifest}")
        return 0
    if args.replay:
        print("AUDIT_MODE: PASS")
        return 0
    if args.self_test:
        rejected, total = hostile_tests(manifest)
        if rejected != total:
            print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
            return 1
        print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
        return 0

    strict = manifest["result"]["strict_nonpromotion"]
    print("AUDIT_MODE: PASS")
    print("PHYSICAL_J_PAIR:", strict["physical_J_pair"])
    print("PHYSICAL_J_CAP:", strict["physical_common_refinement_J_cap"])
    print("PHYSICAL_Q:", strict["physical_collision_time_q_L6over5"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
