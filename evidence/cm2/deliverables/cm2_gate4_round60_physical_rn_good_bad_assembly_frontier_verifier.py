#!/usr/bin/env python3
"""Independent verifier for the Round-60 Gate-4 RN/good-bad frontier."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULT_SCHEMA = "cm2.gate4.round60-physical-rn-good-bad-assembly-frontier.v1"
MANIFEST_SCHEMA = RESULT_SCHEMA + ".manifest.v1"
PREFIX = "cm2-gate4-round60-physical-rn-good-bad-assembly-frontier"
MANIFEST = HERE / f"{PREFIX}-manifest-2026-07-20.json"
REPORT = HERE / f"{PREFIX}-assault-2026-07-20.md"
CERT = HERE / "cm2_gate4_round60_physical_rn_good_bad_assembly_frontier_cert.py"
VERIFIER = Path(__file__).resolve()

DEPENDENCIES = {
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json":
        "e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5",
    "cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json":
        "d335ea6b9bfdc68c13fa0c44f5f2893af7399546f5951d0cfc156be8b5236ffb",
    "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json":
        "1600a3e060e7ae9601a55d425fbce5a27612300e26e01c77f53158b93010a424",
    "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json":
        "cf907c3e980f77fdb19a7bf38db3a647b0be76f0e1a3b5355d5cf3e64452a0f8",
    "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json":
        "7c9d089219ef00234b7e7bdafaea706bd4c91a46990d6f14d0837ea360406414",
    "cm2-gate2-round25-product-base-manifest-2026-07-18.json":
        "8045c36fb14c69a145be4ebf4cd33ae11d55fd77f4591b91782f13516c80679b",
    "cm2-gate34-round49-incidence-safe-long-leaf-atlas-manifest-2026-07-19.json":
        "f8117b4d6b91c85597953366bc1eee26652a6ff7c3bd5486d3a3a38694550c18",
}

BASELINE = {
    "cm2-fifty-ninth-direct-assault-2026-07-20.md":
        "ec0623ec2fd6138c74d3707fd1c6f5e385b98187dcbd616cadee3b19e39dd5ef",
    "cm2-fifty-ninth-direct-assault-manifest-2026-07-20.sha256":
        "c013b5aa22db44308c7aa4cbe2b0800da14f709bcc80250464478b047cfc0712",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-assault-2026-07-20.md":
        "2f66b1aff6551e97729d27f06c87a32957ab21404c0fb0ee3cc0210fa578b468",
    "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.sha256":
        "967421bc83b283510cdb25013f2e723e5761337e56471fad64a9ef74b35536c0",
}

C_P = Q(4 * 10**90 * 360493663, 358863)
SHORT_L = Q(2, 1) / (3 * C_P)
SHORT_Z = Q(1, 1) / SHORT_L
H = Q(999, 1000)
N = C_P.numerator // C_P.denominator + 1
FRAGMENTED_Z = Q(N, 1) / H

EXPECTED_FRONTIER = {
    "actual_landing_RN_marker": "CERTIFIED",
    "same_measure_conditional_Bayes_formula": "CERTIFIED_ON_ANY_SUPPLIED_PHYSICAL_DISINTEGRATION",
    "seven_field_physical_landing_join": "1/7_ACTUAL_COMPLETE__FIELD4_AND_FIELD7_PARTIAL_ONLY",
    "fibrewise_J_land_min_below_Cp_h": "NOT_CERTIFIED",
    "good_original_time_proper_landing_subkernel": "CERTIFIED_POSSIBLY_ZERO__SOURCE_PROPERNESS_NOT_INFERRED",
    "good_subkernel_positive_mass": "NOT_CERTIFIED",
    "bad_landing_mass_zero": "NOT_CERTIFIED",
    "positive_bad_defect_cemetery_route": "CONDITIONAL_FIVE_INTERFACES_MISSING",
    "physical_proper_same_ID_first_return_landing_kernel": "NOT_CERTIFIED",
    "physical_proper_same_ID_first_return_kernel": "NOT_CERTIFIED",
    "original_Rn_intermediate_C24_avoidance": "CERTIFIED_PINNED_ROUND57",
    "full_proper_graph_killed_C24_join": "CERTIFIED_CONDITIONAL",
    "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
    "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
    "strong_singular_current_cemetery": "NOT_CERTIFIED",
    "Gate4": "NOT_CERTIFIED",
    "complete_composite_gates": "0/5",
    "CM2": "NO-GO_FOR_CLAIM",
}


class DuplicateKeyError(ValueError):
    pass


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(key)
        out[key] = value
    return out


def strict_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def defect_depth(z: Q) -> int:
    if z < C_P:
        return 0
    d = 1
    while Q(1, 2**d) * z >= C_P / 2:
        d += 1
    return d


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.is_file() or MANIFEST.is_symlink() or MANIFEST.resolve().parent != HERE:
        raise ValueError("manifest path")
    data = strict_json(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root")
    return data


def check_pinned_files() -> None:
    for mapping in (DEPENDENCIES, BASELINE):
        for name, expected in mapping.items():
            path = HERE / name
            if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
                raise ValueError(f"pinned path: {name}")
            if sha256_path(path) != expected:
                raise ValueError(f"pinned hash: {name}")
    for path in (CERT, VERIFIER, REPORT):
        if not path.is_file() or path.is_symlink() or path.resolve().parent != HERE:
            raise ValueError(f"artifact path: {path.name}")


def replay_dependency_domination_chain() -> None:
    def load(name: str) -> dict[str, Any]:
        path = HERE / name
        data = strict_json(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("result"), dict):
            raise ValueError(f"dependency semantic root: {name}")
        return data["result"]

    raw = load(
        "cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json"
    )["raw_common_first_return_typing"]
    if "exact positive common restriction" not in raw["raw_domain"]:
        raise ValueError("dependency positive source restriction")
    if raw["physical_map"] != "Q_cap(y,x)=T_s^n(x) in B_c subset C_s":
        raise ValueError("dependency physical landing map")
    if "charged exactly once" not in raw["charge"]:
        raise ValueError("dependency once charge")

    r56 = load(
        "cm2-gate34-round56-terminal-j-pair-kac-mesh-closure-manifest-2026-07-20.json"
    )
    induced = r56["paired_leafwise_reverse_replay"]["induced_return_once_coverage"]
    if "(T_C_s)_#(mu_s|C_s)=mu_s|C_s exactly once" not in induced:
        raise ValueError("dependency induced invariance")
    domination = r56["finite_static_source_natural_Z"]["controlled_initial_family_checks"][-1]
    if "dominated as the same positive measure by the admissible mu_s|C_s base source" not in domination:
        raise ValueError("dependency base domination")

    pal = load(
        "cm2-gate34-round57-exact-slope4-cross-endpoint-frontier-manifest-2026-07-20.json"
    )
    if "identical raw point restriction" not in pal["physical_common_refinement_closure"]["same_raw_restriction"]:
        raise ValueError("dependency same raw marker")
    if "positive interval restriction" not in pal["palindromic_stopped_cut_replay"]["density_and_domination"]:
        raise ValueError("dependency interval domination")

    r59 = load(
        "cm2-gate4-round59-cross-fibre-rokhlin-threshold-frontier-manifest-2026-07-20.json"
    )
    weak = r59["same_graph_rokhlin_reconditioning"]
    if weak["status"] != "CERTIFIED_WEAK_SAME_GRAPH_ROKHLIN_RECONDITIONING_AND_TAGGED_BOREL_BRANCH_INVERSE":
        raise ValueError("dependency weak graph theorem")
    if "eta-almost everywhere" not in weak["disintegration_identity"]:
        raise ValueError("dependency eta typing")
    if "Gamma_u-almost surely" not in weak["conditional_support"]:
        raise ValueError("dependency conditional support")


def integrity_check(data: dict[str, Any], *, files: bool = True) -> None:
    if files:
        check_pinned_files()
    if data.get("schema") != MANIFEST_SCHEMA:
        raise ValueError("manifest schema")
    if data.get("dependencies") != DEPENDENCIES:
        raise ValueError("dependencies")
    if data.get("baseline_files") != BASELINE:
        raise ValueError("baseline files")
    if data.get("certificate_sha256") != sha256_path(CERT):
        raise ValueError("certificate hash")
    if data.get("verifier_sha256") != sha256_path(VERIFIER):
        raise ValueError("verifier hash")
    if data.get("report_sha256") != sha256_path(REPORT):
        raise ValueError("report hash")
    for key in ("certificate_sha256", "verifier_sha256", "report_sha256"):
        value = data.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError(key)
    result = data.get("result")
    if not isinstance(result, dict):
        raise ValueError("result root")
    replay = dict(result)
    recorded = replay.pop("internal_replay_digest", None)
    if not isinstance(recorded, str) or digest(replay) != recorded:
        raise ValueError("internal replay digest")
    if data.get("verdict") != result.get("strict_nonpromotion"):
        raise ValueError("verdict alias")


def replay_separators(result: dict[str, Any]) -> None:
    section = result["perfect_product_fields_1_to_4_nonimplication"]
    rows = section["rows"]
    if len(rows) != 2 or digest(rows) != section["rows_sha256"]:
        raise ValueError("separator rows")
    if SHORT_Z != Q(3, 2) * C_P or not C_P < SHORT_Z < 2 * C_P:
        raise ValueError("short arithmetic")
    if defect_depth(SHORT_Z) != 2:
        raise ValueError("short D")
    short = rows[0]
    expected_short = {
        "model": "short_full_plaque",
        "rectangle_count": 1,
        "unstable_plaque_length_L": qstr(SHORT_L),
        "stable_projection": "vertical identity-coordinate projection",
        "two_sided_holonomy_RN_Jacobian": "1",
        "F": 1,
        "theta": "1",
        "R": "1",
        "density": "constant 1/L, log distortion 0",
        "h": "1",
        "J": qstr(SHORT_Z),
        "normalized_boundary": qstr(SHORT_Z),
        "F_R_over_theta_L": qstr(SHORT_Z),
        "D_land": 2,
        "good_fibre": False,
    }
    if short != expected_short:
        raise ValueError("short row")
    short_h = Q(short["h"])
    short_j = Q(short["J"])
    short_z = Q(short["normalized_boundary"])
    if short_h != 1 or short_j != 1 / SHORT_L or short_z != short_j / short_h:
        raise ValueError("short h/J/z")
    if not Q(N - 1) <= C_P < Q(N) or not C_P < FRAGMENTED_Z < 2 * C_P:
        raise ValueError("fragmented arithmetic")
    if defect_depth(FRAGMENTED_Z) != 2:
        raise ValueError("fragmented D")
    fragmented = rows[1]
    expected_fragmented = {
        "model": "unit_plaque_many_gaps",
        "rectangle_count": 1,
        "unstable_plaque_length_L": "1",
        "stable_projection": "vertical identity-coordinate projection",
        "two_sided_holonomy_RN_Jacobian": "1",
        "F": str(N),
        "theta": qstr(H),
        "R": "1",
        "density": "constant 1 on the retained components, log distortion 0",
        "h": qstr(H),
        "J": str(N),
        "normalized_boundary": qstr(FRAGMENTED_Z),
        "F_R_over_theta_L": qstr(FRAGMENTED_Z),
        "D_land": 2,
        "good_fibre": False,
    }
    if fragmented != expected_fragmented:
        raise ValueError("fragmented row")
    fragmented_h = Q(fragmented["h"])
    fragmented_j = Q(fragmented["J"])
    fragmented_z = Q(fragmented["normalized_boundary"])
    if fragmented_h != H or fragmented_j != N or fragmented_z != fragmented_j / fragmented_h:
        raise ValueError("fragmented h/J/z")
    if section["status"] != "CERTIFIED_FIELDS_1_TO_4_QUALITATIVELY_PERFECT_DO_NOT_IMPLY_PHYSICAL_BOUNDARY_THRESHOLD":
        raise ValueError("separator status")
    if "independent quantitative debts" not in section["conclusion"]:
        raise ValueError("separator conclusion")


def replay_field_audit(result: dict[str, Any]) -> None:
    audit = result["seven_field_materialization_audit"]
    rows = audit["rows"]
    if len(rows) != 7 or [r["field"] for r in rows] != list(range(1, 8)):
        raise ValueError("field numbers")
    if digest(rows) != audit["rows_sha256"]:
        raise ValueError("field digest")
    if audit["actual_complete_rows"] != "1/7" or audit["partial_rows"] != [4, 7]:
        raise ValueError("field counts")
    if rows[0]["actual"] != "NOT_CERTIFIED" or rows[1]["actual"] != "NOT_CERTIFIED":
        raise ValueError("physical fields 1/2")
    if rows[2]["actual"] != "NOT_CERTIFIED":
        raise ValueError("field3")
    if not rows[3]["actual"].startswith("PARTIAL_RN_MARKER"):
        raise ValueError("field4")
    if rows[4]["actual"] != "NOT_CERTIFIED":
        raise ValueError("field5")
    if rows[5]["actual"] != "CERTIFIED_ROUND59":
        raise ValueError("field6")
    if not rows[6]["actual"].startswith("NOT_CERTIFIED"):
        raise ValueError("field7")
    if audit["official_Gate2_fields_unchanged"] != "0/17":
        raise ValueError("Gate2 score")


def replay_rn_bridge(result: dict[str, Any]) -> None:
    rn = result["actual_landing_RN_marker_bridge"]
    if rn["status"] != "CERTIFIED_ACTUAL_RN_MARKER_AND_CONDITIONAL_SAME_MEASURE_BAYES_FORMULA__FIELD4_PARTIAL_ONLY":
        raise ValueError("RN status")
    if (
        "kappa_B(A)=kappa_A(T_C_s^(-1)A)" not in rn["positive_domination"]
        or "<=mu_C(T_C_s^(-1)A)=mu_C(A)" not in rn["positive_domination"]
        or "0<=kappa_B<=mu_C" not in rn["positive_domination"]
    ):
        raise ValueError("RN domination")
    if "0<=g_B<=1" not in rn["RN_marker"]:
        raise ValueError("RN range")
    if "tilde_kappa_u=g_B*mu_u" not in rn["unnormalized_same_measure_formula"]:
        raise ValueError("unnormalized formula")
    if "eta_B=m*eta" not in rn["normalized_formula"]:
        raise ValueError("outer formula")
    if "d tilde_kappa_u/ds=g_B*rho_u" not in rn["density_formula"]:
        raise ValueError("density formula")
    if "only eta_B-almost everywhere" not in rn["zero_fibre_policy"]:
        raise ValueError("zero fibre")
    if "never eta({u})" not in rn["singleton_guard"]:
        raise ValueError("singleton guard")
    if "Gamma_u-almost surely" not in rn["graph_semantics"]:
        raise ValueError("conditional graph type")


def replay_good_bad(result: dict[str, Any]) -> None:
    split = result["good_bad_original_time_graph_split"]
    if split["status"] != "CERTIFIED_EXACT_GOOD_BAD_GRAPH_SPLIT_AND_POSSIBLY_ZERO_PROPER_GOOD_LANDING_SUBKERNEL__SOURCE_AND_BAD_PART_UNPAID":
        raise ValueError("split status")
    if "G={y:h(y)>0 and z_land(y)<C_p}" not in split["sets"]:
        raise ValueError("good set")
    if "possibly-zero proper" not in split["good_subkernel"] or "source properness" not in split["good_subkernel"]:
        raise ValueError("good subkernel")
    if "notin C_s" not in split["good_killed_semantics"]:
        raise ValueError("killed semantics")
    if "Gamma_u-almost surely" not in split["measure_typing"] or "eta-almost every" not in split["measure_typing"]:
        raise ValueError("split measure typing")
    if split["good_mass_positive"] != "NOT_CERTIFIED; finite J_land,min,total alone permits G to be empty":
        raise ValueError("good mass")
    if split["bad_mass_zero"] != "NOT_CERTIFIED; the k=0 Markov estimate is finite, not zero":
        raise ValueError("bad mass")
    if "D_land=2" not in split["all_bad_separator"] or "=4" not in split["all_bad_separator"]:
        raise ValueError("all bad model")

    defect = result["positive_bad_defect_cemetery_interface"]
    rows = defect["rows"]
    if len(rows) != 5 or digest(rows) != defect["rows_sha256"]:
        raise ValueError("defect rows")
    if [r["index"] for r in rows] != [1, 2, 3, 4, 5]:
        raise ValueError("defect indices")
    if defect["status"] != "CERTIFIED_CONDITIONAL_POSITIVE_DEFECT_ROUTE_WITH_FIVE_MISSING_INTERFACES__NO_CURRENT_HYBRID_CLOSURE":
        raise ValueError("defect status")
    if "positive ordinary collision-SRB mass" not in defect["collision_null_guard"]:
        raise ValueError("positive mass guard")
    if "all-bad separator" not in defect["exactness_guard"]:
        raise ValueError("exactness guard")


def replay_literature_and_downstream(result: dict[str, Any]) -> None:
    literature = result["latest_field7_literature_audit"]
    if literature["official_pdf_sha256_checked"] != "fc00f45a8ec6513763665bf8fa34569a95ca5d6d6b9fa5d90b7e1089fabd9004":
        raise ValueError("literature hash")
    if "arXiv:2604.19671v2" not in literature["official_source"]:
        raise ValueError("literature source")
    if literature["external_theorem_promoted"] is not False:
        raise ValueError("external promotion")
    if "B2 is qualitative" not in literature["quantitative_guard"]:
        raise ValueError("B2 guard")
    if "divides" not in literature["conditioning_guard"]:
        raise ValueError("conditioning guard")
    if "no known Banach spaces" not in literature["strong_space_guard"]:
        raise ValueError("Banach guard")
    if literature["status"] != "AUDITED_CONDITIONAL_STANDARD_FAMILY_CATEGORY_SUBINTERFACE__FIELD7_ACTUAL_STRONG_ASSEMBLY_NOT_SUPPLIED":
        raise ValueError("literature status")

    downstream = result["downstream_original_killed_join"]
    if downstream["status"] != "CERTIFIED_CONDITIONAL_ORIGINAL_RN_KILLED_JOIN__LATER_CLOCK_Q_AND_STRONG_CEMETERY_REMAIN_SEPARATE":
        raise ValueError("downstream status")
    if "product_{j=1}^{n-1}" not in downstream["killed_C24_join"]:
        raise ValueError("killed product")
    if "Gamma_u-almost sure" not in downstream["typing"] or "eta-almost every" not in downstream["typing"]:
        raise ValueError("downstream typing")
    if "possibly-zero good landing subgraph" not in downstream["current_actual_scope"] or "source properness is not inferred" not in downstream["current_actual_scope"]:
        raise ValueError("downstream actual scope")
    if "same-ID numerical C_fw/C_rev" not in downstream["physical_q"]:
        raise ValueError("q guard")


def semantic_replay(data: dict[str, Any]) -> None:
    result = data["result"]
    if result.get("schema") != RESULT_SCHEMA:
        raise ValueError("result schema")
    provenance = result["provenance"]
    if provenance["dependency_sha256"] != DEPENDENCIES or provenance["baseline_file_sha256"] != BASELINE:
        raise ValueError("provenance pins")
    if provenance["old_artifacts_modified"] is not False or provenance["external_theorem_promoted"] is not False:
        raise ValueError("provenance promotion")
    pinned = result["pinned_round59_type_audit"]
    if pinned["status"] != "CERTIFIED_FROZEN_ROUND59_TYPE_BASELINE":
        raise ValueError("pinned status")
    if "eta-almost every" not in pinned["Round59_measure_typing"] or "no singleton normalization" not in pinned["Round59_measure_typing"]:
        raise ValueError("pinned measure typing")
    replay_dependency_domination_chain()
    replay_rn_bridge(result)
    replay_separators(result)
    replay_field_audit(result)
    replay_good_bad(result)
    replay_literature_and_downstream(result)
    if result["strict_nonpromotion"] != EXPECTED_FRONTIER:
        raise ValueError("strict frontier")


def source_guard() -> None:
    tree = ast.parse(CERT.read_text(encoding="utf-8"), filename=str(CERT))
    strings = [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)]
    joined = "\n".join(strings)
    for token in (
        "NO-GO_FOR_CLAIM",
        "physical_proper_same_ID_first_return_kernel",
        "NOT_CERTIFIED",
        "eta_B-almost everywhere",
        "never eta({u})",
    ):
        if token not in joined:
            raise ValueError(f"source guard: {token}")


def validate(data: dict[str, Any], *, files: bool = True) -> None:
    integrity_check(data, files=files)
    semantic_replay(data)
    if files:
        source_guard()


def assign_path(data: Any, path: tuple[Any, ...], value: Any) -> None:
    target = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def hostile_self_test() -> tuple[int, int]:
    original = load_manifest()
    mutations: list[tuple[tuple[Any, ...], Any, bool]] = [
        (("schema",), "bad", False),
        (("certificate_sha256",), "0" * 64, False),
        (("verifier_sha256",), "0" * 64, False),
        (("report_sha256",), "0" * 64, False),
        (("dependencies", next(iter(DEPENDENCIES))), "0" * 64, False),
        (("baseline_files", next(iter(BASELINE))), "0" * 64, False),
        (("result", "schema"), "bad", True),
        (("result", "provenance", "old_artifacts_modified"), True, True),
        (("result", "provenance", "external_theorem_promoted"), True, True),
        (("result", "pinned_round59_type_audit", "status"), "NOT_CERTIFIED", True),
        (("result", "pinned_round59_type_audit", "Round59_measure_typing"), "pointwise", True),
        (("result", "actual_landing_RN_marker_bridge", "status"), "CERTIFIED_FIELD4", True),
        (("result", "actual_landing_RN_marker_bridge", "positive_domination"), "kappa=mu", True),
        (("result", "actual_landing_RN_marker_bridge", "RN_marker"), "g=2", True),
        (("result", "actual_landing_RN_marker_bridge", "zero_fibre_policy"), "all fibres", True),
        (("result", "actual_landing_RN_marker_bridge", "singleton_guard"), "divide eta singleton", True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "status"), "CERTIFIED_PROPER", True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "rows", 0, "F"), 2, True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "rows", 0, "theta"), "1/2", True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "rows", 0, "R"), "2", True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "rows", 0, "D_land"), 0, True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "rows", 0, "good_fibre"), True, True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "rows", 1, "F"), "1", True),
        (("result", "perfect_product_fields_1_to_4_nonimplication", "rows", 1, "D_land"), 0, True),
        (("result", "seven_field_materialization_audit", "actual_complete_rows"), "2/7", True),
        (("result", "seven_field_materialization_audit", "partial_rows"), [4], True),
        (("result", "seven_field_materialization_audit", "official_Gate2_fields_unchanged"), "1/17", True),
        (("result", "seven_field_materialization_audit", "rows", 0, "actual"), "CERTIFIED", True),
        (("result", "seven_field_materialization_audit", "rows", 1, "actual"), "CERTIFIED", True),
        (("result", "seven_field_materialization_audit", "rows", 2, "actual"), "CERTIFIED", True),
        (("result", "seven_field_materialization_audit", "rows", 3, "actual"), "CERTIFIED", True),
        (("result", "seven_field_materialization_audit", "rows", 4, "actual"), "CERTIFIED", True),
        (("result", "seven_field_materialization_audit", "rows", 5, "actual"), "NOT_CERTIFIED", True),
        (("result", "seven_field_materialization_audit", "rows", 6, "actual"), "CERTIFIED", True),
        (("result", "good_bad_original_time_graph_split", "status"), "CERTIFIED_FULL_KERNEL", True),
        (("result", "good_bad_original_time_graph_split", "good_mass_positive"), "CERTIFIED", True),
        (("result", "good_bad_original_time_graph_split", "bad_mass_zero"), "CERTIFIED", True),
        (("result", "good_bad_original_time_graph_split", "measure_typing"), "pointwise all u", True),
        (("result", "positive_bad_defect_cemetery_interface", "status"), "CERTIFIED_CEMETERY", True),
        (("result", "positive_bad_defect_cemetery_interface", "rows", 0, "current"), "CERTIFIED", True),
        (("result", "positive_bad_defect_cemetery_interface", "rows", 2, "current"), "CERTIFIED", True),
        (("result", "positive_bad_defect_cemetery_interface", "collision_null_guard"), "collision null", True),
        (("result", "latest_field7_literature_audit", "external_theorem_promoted"), True, True),
        (("result", "latest_field7_literature_audit", "official_pdf_sha256_checked"), "0" * 64, True),
        (("result", "latest_field7_literature_audit", "quantitative_guard"), "B2<Cp", True),
        (("result", "latest_field7_literature_audit", "strong_space_guard"), "strong Banach assembly", True),
        (("result", "downstream_original_killed_join", "status"), "CERTIFIED_ALL_DOWNSTREAM", True),
        (("result", "downstream_original_killed_join", "typing"), "pointwise", True),
        (("result", "downstream_original_killed_join", "current_actual_scope"), "full graph", True),
        (("result", "strict_nonpromotion", "Gate4"), "CERTIFIED", True),
        (("result", "strict_nonpromotion", "CM2"), "GO", True),
        (("result", "strict_nonpromotion", "complete_composite_gates"), "1/5", True),
        (("result", "strict_nonpromotion", "fibrewise_J_land_min_below_Cp_h"), "CERTIFIED", True),
        (("result", "strict_nonpromotion", "good_subkernel_positive_mass"), "CERTIFIED", True),
        (("result", "strict_nonpromotion", "bad_landing_mass_zero"), "CERTIFIED", True),
        (("result", "strict_nonpromotion", "physical_proper_same_ID_first_return_kernel"), "CERTIFIED", True),
        (("result", "strict_nonpromotion", "later_and_repeated_recovery_clock_moments"), "CERTIFIED", True),
        (("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED", True),
        (("result", "strict_nonpromotion", "strong_singular_current_cemetery"), "CERTIFIED", True),
        (("verdict", "Gate4"), "CERTIFIED", False),
        (("verdict", "CM2"), "GO", False),
    ]
    rejected = 0
    for path, value, rehash in mutations:
        candidate = copy.deepcopy(original)
        assign_path(candidate, path, value)
        if rehash and path[:1] == ("result",):
            replay = dict(candidate["result"])
            replay.pop("internal_replay_digest", None)
            candidate["result"]["internal_replay_digest"] = digest(replay)
            candidate["verdict"] = candidate["result"]["strict_nonpromotion"]
        try:
            validate(candidate, files=False)
        except (ValueError, KeyError, TypeError, IndexError):
            rejected += 1
        else:
            raise AssertionError(f"hostile mutation accepted: {path}")

    malformed = [
        '{"x":1,"x":2}',
        '{"x":NaN}',
        '{"x":Infinity}',
        '{"x":-Infinity}',
        '{"x":',
    ]
    for payload in malformed:
        try:
            strict_json(payload)
        except (ValueError, json.JSONDecodeError, DuplicateKeyError):
            rejected += 1
        else:
            raise AssertionError("malformed JSON accepted")
    return rejected, len(mutations) + len(malformed)


def deterministic_reemit() -> None:
    proc = subprocess.run(
        [sys.executable, str(CERT), "--manifest-json"],
        cwd=str(HERE),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise ValueError(f"certificate reemit exit {proc.returncode}: {proc.stderr}{proc.stdout}")
    if proc.stdout != MANIFEST.read_text(encoding="utf-8"):
        raise ValueError("manifest reemit differs")


def default_exit_audit() -> None:
    cert = subprocess.run([sys.executable, str(CERT)], cwd=str(HERE), capture_output=True, text=True, check=False)
    if cert.returncode != 2 or "NO-GO_FOR_CLAIM" not in cert.stdout:
        raise ValueError("certificate default")
    verifier = subprocess.run([sys.executable, str(VERIFIER), "--default-child"], cwd=str(HERE), capture_output=True, text=True, check=False)
    if verifier.returncode != 2 or "NO-GO_FOR_CLAIM" not in verifier.stdout:
        raise ValueError("verifier default")


def run_default_child() -> int:
    data = load_manifest()
    validate(data)
    strict = data["result"]["strict_nonpromotion"]
    print("GATE4:", strict["Gate4"])
    print("CM2:", strict["CM2"])
    return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integrity-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", action="store_true")
    parser.add_argument("--check-defaults", action="store_true")
    parser.add_argument("--default-child", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.default_child:
            return run_default_child()
        data = load_manifest()
        if args.integrity_only:
            integrity_check(data)
            source_guard()
            print("AUDIT_MODE: PASS")
            return 0
        if args.replay:
            validate(data)
            print("AUDIT_MODE: PASS")
            return 0
        if args.self_test:
            validate(data)
            passed, total = hostile_self_test()
            print(f"HOSTILE_TESTS: {passed}/{total} PASS")
            return 0
        if args.reemit:
            validate(data)
            deterministic_reemit()
            print("REEMIT: BYTE_IDENTICAL PASS")
            return 0
        if args.check_defaults:
            validate(data)
            default_exit_audit()
            print("DEFAULT_EXITS: 2/2 PASS")
            return 0
        validate(data)
        strict = data["result"]["strict_nonpromotion"]
        print("ACTUAL_RN_MARKER:", strict["actual_landing_RN_marker"])
        print("SEVEN_FIELD_JOIN:", strict["seven_field_physical_landing_join"])
        print("PROPER_KERNEL:", strict["physical_proper_same_ID_first_return_kernel"])
        print("GATE4:", strict["Gate4"])
        print("CM2:", strict["CM2"])
        return 2
    except (OSError, ValueError, KeyError, TypeError, IndexError, AssertionError) as exc:
        print(f"ROUND60_GATE4_RN_VERIFY_FAILURE: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
