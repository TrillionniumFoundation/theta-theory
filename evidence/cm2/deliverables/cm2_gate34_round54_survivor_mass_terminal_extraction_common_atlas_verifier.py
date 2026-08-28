#!/usr/bin/env python3
"""Independent verifier for the Round-54 survivor/terminal atlas leaf."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

import cm2_gate34_round54_survivor_mass_terminal_extraction_common_atlas_cert as cert


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = cert.DEFAULT_MANIFEST


def fail(message: str) -> None:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else (
        f"{value.numerator}/{value.denominator}"
    )


def load_manifest(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing manifest: {path.name}")
    require(not path.is_symlink(), "manifest symlink")
    require(path.resolve().parent == HERE, "unsafe manifest path")
    value = cert.parse_json_text(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "manifest root")
    return value


def check_literal_dict_keys(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[Any] = set()
        for key in node.keys:
            if key is None:
                continue
            if isinstance(key, ast.Constant) and isinstance(
                key.value, (str, int, float, bytes, bool, type(None))
            ):
                if key.value in seen:
                    fail(f"duplicate literal dict key in {path.name}: {key.value!r}")
                seen.add(key.value)


def check_dependencies_independently() -> None:
    for name, expected in cert.DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file(), f"missing dependency {name}")
        require(not path.is_symlink(), f"dependency symlink {name}")
        require(path.resolve().parent == HERE, f"unsafe dependency {name}")
        require(sha256_path(path) == expected, f"dependency SHA {name}")
        value = cert.parse_json_text(path.read_text(encoding="utf-8"))
        require(isinstance(value, dict), f"dependency root {name}")

    round27 = cert.parse_json_text(
        (
            HERE
            / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
        ).read_text(encoding="utf-8")
    )["result"]["arbitrary_n_Rn_Qn_level_and_mass_schema"]
    require(round27["Q_0"] == "C_s", "independent Q0")
    require(
        round27["level_identity_mod_null"]
        == "Q_(n-1)=R_n disjoint_union Q_n",
        "independent level split",
    )
    physical = round27["symbolic_physical_mass"]
    require(physical["sum_k_qmass_s_n_k"] == "mu_s(Q_n)", "independent Q mass")
    require(physical["sum_k_m_s_n_k"] == "mu_s(R_n)", "independent R mass")
    require(
        round27["normalized_core_mass_interval"]
        == ["147/550000_strict_lower", "29021/75000000_strict_upper"],
        "independent core mass upper",
    )

    round37 = cert.parse_json_text(
        (
            HERE
            / "cm2-gate45-round37-typed-forcing-correction-manifest-2026-07-19.json"
        ).read_text(encoding="utf-8")
    )["result"]["typed_forcing_correction"]
    require(
        round37["fixed_s_base_standard_family_recurrence"]
        == "Z_(n+1)<=a*Z_n+b*m_n+J_C24,n",
        "independent corrected recurrence",
    )
    require(
        "repeated characteristic restriction" in round37["C24_complement_role"],
        "independent C24 type",
    )

    inner = cert.parse_json_text(
        (
            HERE
            / "cm2-gate4-inner-core-strong-product-bridge-frontier-manifest-2026-07-16.json"
        ).read_text(encoding="utf-8")
    )
    require(
        inner["replay_summary"]["source_multiplier_norm_upper"] == "2000/1999",
        "independent core multiplier",
    )

    round35 = cert.parse_json_text(
        (
            HERE
            / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
        ).read_text(encoding="utf-8")
    )["result"]["common_forward_reverse_carrier_pair"]
    require(
        round35["reverse_oriented_branch"] == "I(B) -> I(A) by T_s^n",
        "independent reverse return branch",
    )
    require(
        round35["forward_and_reverse_share_identical_component_and_restriction"]
        is True,
        "independent same restriction",
    )

    round52 = cert.parse_json_text(
        (
            HERE
            / "cm2-gate34-round52-defect-threshold-same-id-return-frontier-manifest-2026-07-20.json"
        ).read_text(encoding="utf-8")
    )["result"]
    require(
        round52["uniform_outer_majorant_terminal_join"][
            "same_ID_once_charged_common_terminal_survivor_fraction_strict_lower"
        ]
        == "249/250",
        "independent common mass",
    )
    require(
        round52["large_common_mass_geometric_nonpromotion"][
            "common_standard_family_proper"
        ]
        is False,
        "independent common geometry scope",
    )


def independent_arithmetic(result: dict[str, Any]) -> None:
    A = Q(550000, 147)
    r = Q(111718729, 111718750)
    gap = 1 - r
    require(gap == Q(21, 111718750), "tail gap arithmetic")
    coefficient = A / gap
    require(coefficient == Q(61445312500000, 3087), "tail coefficient arithmetic")
    uniform = Q(29021, 75000000) * coefficient
    require(uniform == Q(142656353125, 18522), "uniform tail coefficient")

    killed = result["killed_survivor_mass_join"]
    require(killed["tail_constants"]["A_over_one_minus_r"] == qstr(coefficient), "tail field")
    require(
        killed["strict_sum"]
        == "sum_{n>=0}m_n<mu_s(C_s)*(61445312500000/3087)*N_open",
        "strict sum field",
    )
    require(
        killed["uniform_relaxed_sum"]
        == "sum_{n>=0}m_n<(142656353125/18522)*N_open",
        "uniform sum field",
    )
    require(
        killed["mass_identity"]
        == "m_n=mass(F_n)=mu_s(Q_n)=mu_s(C_s)*S_n",
        "mass identity field",
    )
    require(
        killed["R_n_state_rejected"]["using_R_n_mass_in_the_Q_n_killed_recurrence"]
        is False,
        "R_n rejection",
    )
    require("not the next return-level law" in killed["R_n_state_rejected"]["why_not_this_recurrence_state"], "R_n dynamics")

    expected_rows: list[dict[str, Any]] = []
    for n in range(10):
        expected_rows.append(
            {
                "n": n,
                "toy_N_open": 3,
                "block_index": n // 3,
                "strict_S_n_upper": qstr(A * r ** (n // 3)),
                "state_ID": f"survivor-prefix:(source-core,Q_{n},prefix-key)",
                "next_terminal_ID": f"return-path:(source-core,R_{n + 1},path-key)",
            }
        )
    require(killed["sample_rows"] == expected_rows, "tail rows")
    require(killed["sample_rows_sha256"] == canonical_digest(expected_rows), "tail rows digest")

    a = Q(360134800, 360493663)
    b = Q(2 * 10**90)
    c = Q(2000, 1999)
    margin = 1 - a
    resolvent = 1 / margin
    require(margin == Q(358863, 360493663), "growth margin")
    require(resolvent == Q(360493663, 358863), "growth resolvent")
    c_resolvent = c * resolvent
    require(c_resolvent == Q(720987326000, 717367137), "terminal multiplier")
    terminal = result["two_orientation_terminal_extraction"]
    coeff = terminal["coefficients"]
    require(coeff["terminal_resolvent_multiplier"] == qstr(c_resolvent), "terminal field")
    require(coeff["Z_pair_0_coefficient"] == qstr(c_resolvent * a), "Z0 coefficient")
    require(coeff["M_coefficient"] == qstr(c_resolvent * 2 * b), "mass coefficient")
    require(coeff["Phi_pair_coefficient"] == qstr(c_resolvent * a), "face coefficient")
    require(
        terminal["exact_coarse_extraction_bound"]
        == "Z_term,coarse,pair<=(2000/1999)/(1-a)*[a*Z_pair,0+2*b*M+a*Phi_pair]",
        "coarse extraction formula",
    )
    require("not included" in terminal["forcing_index_contract"], "terminal/forcing separation")
    require(terminal["first_level_check"].startswith("n=0"), "terminal off-by-one")
    cores = terminal["orientation_specific_cores"]
    require(cores["forward_terminal_core"] == "C_fw=C_s", "forward core")
    require(cores["reverse_terminal_core"] == "C_rev=I(C_s)", "reverse core")
    require(cores["no_time_reversal_invariance_of_the_literal_core_asserted"] is True, "core invariance scope")
    require("preserves collision-SRB measure" in cores["same_multiplier_reason"], "reverse measure")
    require("arclength" in cores["same_multiplier_reason"], "reverse arclength")

    refinement_rows: list[dict[str, Any]] = []
    for cells in [1, 2, 4, 8, 32, 128]:
        refinement_rows.append(
            {
                "natural_or_image_cell_count_N": cells,
                "coarse_interval": "[0,1]",
                "coarse_mass": "1",
                "coarse_length": "1",
                "coarse_boundary_Z": "1",
                "each_refined_cell_mass": qstr(Q(1, cells)),
                "each_refined_cell_length": qstr(Q(1, cells)),
                "each_cell_boundary_contribution": "1",
                "refined_cell_boundary_Z": str(cells),
            }
        )
    refinement = terminal["cell_refinement_separator"]
    require(refinement["rows"] == refinement_rows, "refinement rows")
    require(refinement["rows_sha256"] == canonical_digest(refinement_rows), "refinement digest")
    require(
        terminal["terminal_cell_refinement_to_J_pair_same_ID_Z_join"]
        == "NOT_CERTIFIED",
        "cell refinement scope",
    )

    separator = result["summable_mass_nonsummable_face_separator"]
    expected_sep: list[dict[str, Any]] = []
    mass_partial = Q(0)
    force_partial = Q(0)
    for n in range(9):
        mass = r**n
        mass_partial += mass
        force_partial += 1
        expected_sep.append(
            {
                "n": n,
                "survivor_interval": f"W_{n}=(0,r^{n})",
                "survivor_mass_m_n": qstr(mass),
                "new_cut_location": f"r^{n + 1}",
                "new_endpoint_boundary_charge_Phi_n": "1",
                "mass_partial_sum": qstr(mass_partial),
                "forcing_partial_sum": qstr(force_partial),
            }
        )
    require(separator["rows"] == expected_sep, "separator rows")
    require(separator["rows_sha256"] == canonical_digest(expected_sep), "separator digest")
    require(mass_partial < 1 / gap and force_partial == 9, "separator arithmetic")

    atlas = result["physical_common_refinement_atlas"]
    require(atlas["status"] == "CERTIFIED_PHYSICAL_BOREL_COUNTABLE_COMMON_REFINEMENT_ATLAS_ONLY", "atlas status")
    require(atlas["sample_rows_sha256"] == canonical_digest(atlas["sample_rows"]), "atlas rows digest")
    require(sum(row["component_count"] for row in atlas["sample_rows"]) == 3, "atlas row count")
    require("countably many" in atlas["whole_record_cardinality"], "atlas countable scope")
    require(atlas["recordwise_J_cap"].endswith("NOT_CERTIFIED"), "atlas recordwise Jcap")
    require(atlas["recordwise_D_cap"].endswith("NOT_CERTIFIED"), "atlas recordwise Dcap")
    require(atlas["recordwise_two_view_properisation"] == "NOT_CERTIFIED", "atlas properisation")
    require(atlas["global_integrability"].endswith("NOT_CERTIFIED"), "atlas global scope")
    require("not yet a proper two-view carrier" in atlas["typing_boundary"], "atlas return scope")

    countable_rows: list[dict[str, Any]] = []
    for k in range(1, 9):
        length = Q(1, 2**k)
        countable_rows.append(
            {
                "compact_regular_substratum_k": k,
                "component_count_on_this_substratum": 1,
                "component_mass_p_k": qstr(length),
                "forward_length_ell_k": qstr(length),
                "reverse_length_ell_k": qstr(length),
                "forward_boundary_contribution": "1",
                "reverse_boundary_contribution": "1",
                "pair_boundary_contribution": "2",
            }
        )
    countable = atlas["countable_stratum_separator"]
    require(countable["rows"] == countable_rows, "countable separator rows")
    require(countable["rows_sha256"] == canonical_digest(countable_rows), "countable separator digest")
    require(sum(Q(row["component_mass_p_k"]) for row in countable_rows) < 1, "finite separator sample mass")
    require(sum(int(row["pair_boundary_contribution"]) for row in countable_rows) == 16, "separator sample Z")

    strict = result["strict_nonpromotion"]
    expected_status = {
        "round28_Qn_to_round36_mn_same_ID_normalization_join": "CERTIFIED",
        "all_insertion_time_C24_complement_face_forcing_l1": "NOT_CERTIFIED",
        "coarse_terminal_Z_extraction_inequality": "CERTIFIED",
        "terminal_cell_refinement_to_J_pair_same_ID_Z_join": "NOT_CERTIFIED",
        "terminal_extraction_to_J_pair_join": "NOT_CERTIFIED",
        "physical_J_pair": "NOT_CERTIFIED",
        "physical_common_refinement_atlas": "CERTIFIED_BOREL_COUNTABLE_ONLY",
        "recordwise_common_refinement_J_cap": "NOT_CERTIFIED",
        "physical_common_refinement_J_cap_total": "NOT_CERTIFIED",
        "recordwise_common_two_view_properisation": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    for key, value in expected_status.items():
        require(strict[key] == value, f"strict status {key}")


def verify_manifest(value: dict[str, Any]) -> None:
    expected = cert.build_manifest(Path(__file__).resolve())
    require(value.get("schema") == cert.MANIFEST_SCHEMA, "manifest schema")
    require(set(value) == set(expected), "manifest root keys")
    require(value["certificate_sha256"] == sha256_path(Path(cert.__file__).resolve()), "certificate SHA")
    require(value["verifier_sha256"] == sha256_path(Path(__file__).resolve()), "verifier SHA")
    require(value["dependencies"] == cert.DEPENDENCIES, "dependency ledger")
    require(value["result"]["schema"] == cert.RESULT_SCHEMA, "result schema")
    replay = copy.deepcopy(value["result"])
    digest_value = replay.pop("internal_replay_digest", None)
    require(digest_value == canonical_digest(replay), "internal replay digest")
    require(value["verdict"] == value["result"]["strict_nonpromotion"], "verdict alias")
    require(canonical_json(value) == canonical_json(expected), "deterministic replay")
    independent_arithmetic(value["result"])


def scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterable[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key in sorted(value):
            yield from scalar_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from scalar_paths(item, prefix + (index,))
    else:
        yield prefix


def mutate_scalar(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 0.5
    if value is None:
        return "MUTATED_NULL"
    if isinstance(value, str):
        return value + "__MUTATED"
    fail(f"unsupported scalar type: {type(value)}")


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    cursor = value
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = replacement


def get_path(value: Any, path: tuple[Any, ...]) -> Any:
    cursor = value
    for part in path:
        cursor = cursor[part]
    return cursor


def rejection_test(value: dict[str, Any]) -> tuple[int, int]:
    paths = list(scalar_paths(value))
    selected = paths[:180]
    rejected = 0
    total = 0
    for path in selected:
        bad = copy.deepcopy(value)
        set_path(bad, path, mutate_scalar(get_path(bad, path)))
        total += 1
        try:
            verify_manifest(bad)
        except Exception:
            rejected += 1

    structural_mutations: list[dict[str, Any]] = []
    bad = copy.deepcopy(value)
    bad["result"].pop("killed_survivor_mass_join")
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["result"]["strict_nonpromotion"]["physical_J_pair"] = "CERTIFIED"
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["result"]["killed_survivor_mass_join"]["mass_identity"] = "m_n=mu_s(R_n)"
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["result"]["two_orientation_terminal_extraction"]["first_level_check"] = "n=1 starts R_1"
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["result"]["two_orientation_terminal_extraction"]["forcing_index_contract"] = "terminal included in Phi"
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["result"]["two_orientation_terminal_extraction"][
        "terminal_cell_refinement_to_J_pair_same_ID_Z_join"
    ] = "CERTIFIED"
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["result"]["summable_mass_nonsummable_face_separator"]["rows"][0][
        "new_endpoint_boundary_charge_Phi_n"
    ] = "0"
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["result"]["physical_common_refinement_atlas"]["recordwise_J_cap"] = "CERTIFIED"
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["verdict"] = {}
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["dependencies"] = {}
    structural_mutations.append(bad)
    bad = copy.deepcopy(value)
    bad["schema"] = cert.RESULT_SCHEMA
    structural_mutations.append(bad)

    for bad in structural_mutations:
        total += 1
        try:
            verify_manifest(bad)
        except Exception:
            rejected += 1

    malformed = [
        '{"a":1,"a":2}',
        '{"x":NaN}',
        '{"x":Infinity}',
        '{"x":-Infinity}',
        '[1,2,',
        'null trailing',
    ]
    for raw in malformed:
        total += 1
        try:
            cert.parse_json_text(raw)
        except Exception:
            rejected += 1
    return rejected, total


def deterministic_reemit(value: dict[str, Any]) -> None:
    with tempfile.TemporaryDirectory(prefix="cm2-r54-return-") as tmp:
        p1 = Path(tmp) / "one.json"
        p2 = Path(tmp) / "two.json"
        text = json.dumps(value, indent=2, sort_keys=True) + "\n"
        p1.write_text(text, encoding="utf-8")
        p2.write_text(
            json.dumps(cert.build_manifest(Path(__file__).resolve()), indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        require(p1.read_bytes() == p2.read_bytes(), "deterministic re-emission")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit-manifest", type=Path)
    args = parser.parse_args()

    check_literal_dict_keys(Path(cert.__file__).resolve())
    check_literal_dict_keys(Path(__file__).resolve())
    check_dependencies_independently()
    value = load_manifest(args.manifest)
    verify_manifest(value)

    if args.reemit_manifest is not None:
        target = args.reemit_manifest
        require(not target.exists() or (target.is_file() and not target.is_symlink()), "unsafe reemit target")
        target.write_text(
            json.dumps(cert.build_manifest(Path(__file__).resolve()), indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
        )
        print("REEMIT: PASS")
        return 0

    if args.self_test:
        rejected, total = rejection_test(value)
        require(rejected == total, "hostile mutation rejection")
        print(f"HOSTILE_TESTS: {rejected}/{total} PASS")
        return 0

    if args.integrity_only:
        print("DEPENDENCY_SHA:", f"{len(cert.DEPENDENCIES)}/{len(cert.DEPENDENCIES)} PASS")
        print("AUDIT_MODE: PASS")
        return 0

    if args.replay:
        deterministic_reemit(value)
        print("INDEPENDENT_ARITHMETIC: PASS")
        print("DETERMINISTIC_REEMISSION: PASS")
        print("AUDIT_MODE: PASS")
        return 0

    strict = value["verdict"]
    print("AUDIT_MODE: PASS")
    print("SURVIVOR_MASS_JOIN:", strict["round28_Qn_to_round36_mn_same_ID_normalization_join"])
    print("COARSE_TERMINAL_Z:", strict["coarse_terminal_Z_extraction_inequality"])
    print("TERMINAL_TO_J_PAIR_JOIN:", strict["terminal_extraction_to_J_pair_join"])
    print("ALL_TIME_FACE_FORCING:", strict["all_insertion_time_C24_complement_face_forcing_l1"])
    print("PHYSICAL_J_PAIR:", strict["physical_J_pair"])
    print("CM2:", strict["CM2"])
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"AUDIT_MODE: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
