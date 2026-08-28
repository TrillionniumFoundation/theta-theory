#!/usr/bin/env python3
"""Independent verifier for the Round-56 terminal J_pair closure leaf."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import cm2_gate34_round56_terminal_j_pair_kac_mesh_closure_cert as cert


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = cert.DEFAULT_MANIFEST
EXPECTED_SCHEMA = cert.MANIFEST_SCHEMA


class DuplicateKeyError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(key)
        value[key] = item
    return value


def strict_load(raw: bytes) -> dict[str, Any]:
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant: {token}")
        ),
    )
    require(isinstance(value, dict), "manifest root")
    return value


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def qstr(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def check_json_tree(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, str, int)):
        return
    if isinstance(value, float):
        require(math.isfinite(value), f"non-finite float: {path}")
        raise RuntimeError(f"floating JSON number forbidden: {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            check_json_tree(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            require(isinstance(key, str), f"non-string key: {path}")
            check_json_tree(item, f"{path}.{key}")
        return
    raise RuntimeError(f"unsupported JSON type: {path}")


def safe_manifest_path(path: Path) -> Path:
    resolved = path.resolve()
    require(path.is_file(), "manifest missing")
    require(not path.is_symlink(), "manifest symlink")
    require(resolved.parent == HERE, "manifest outside deliverables")
    return resolved


def expected_path_rows() -> list[dict[str, Any]]:
    paths = ([14], [14, 15], [20, 14, 17], [64, 65, 14], [100, 99, 100])
    rows: list[dict[str, Any]] = []
    for ranks in paths:
        b_max = max(ranks)
        inv_max = 1 << ((3 * (b_max + 1) + 1) // 2)
        inv_sum = sum(1 << ((3 * (B + 1) + 1) // 2) for B in ranks)
        require(inv_max <= inv_sum, "sample path max")
        for B in ranks:
            inv = 1 << ((3 * (B + 1) + 1) // 2)
            require(inv * inv <= 16 * 2 ** (3 * B), "sample mesh square")
        rows.append(
            {
                "path_ranks": list(ranks),
                "B_max": b_max,
                "delta_Bmax_inverse": str(inv_max),
                "sum_delta_Bi_inverse": str(inv_sum),
                "max_is_one_path_term": True,
                "squared_rank_bound_each_i": "delta_Bi^-2<=16*2^(3B_i)",
            }
        )
    return rows


def expected_tower_rows() -> list[dict[str, Any]]:
    return [
        {
            "return_depth_n": n,
            "tower_levels": [f"T^{i}(R_{n})" for i in range(n)],
            "rank_indices": [f"B_{i + 1}=B_inc(T^{i}x)" for i in range(n)],
            "level_count": n,
            "last_level_before_return": f"T^{n - 1}(R_{n})",
        }
        for n in range(1, 6)
    ]


def independent_arithmetic(result: dict[str, Any]) -> None:
    mesh = result["path_max_mesh_and_Kac_tower"]
    rows = expected_path_rows()
    require(mesh["sample_path_rows"] == rows, "path rows")
    require(mesh["sample_path_rows_sha256"] == digest(rows), "path row digest")
    towers = expected_tower_rows()
    require(mesh["tower_sample_rows"] == towers, "tower rows")
    require(mesh["tower_sample_rows_sha256"] == digest(towers), "tower digest")
    rank_moment = Q(134217735, 64)
    delta_charge = 4 * rank_moment
    adapted_charge = Q(27, 5) * delta_charge
    require(delta_charge == Q(134217735, 16), "delta charge arithmetic")
    require(adapted_charge == Q(724775769, 16), "adapted charge arithmetic")
    require(
        Q(mesh["physical_rank_moment_strict_upper"]) == rank_moment,
        "rank moment field",
    )
    require(
        Q(mesh["physical_delta_charge_strict_upper"]) == delta_charge,
        "delta charge field",
    )
    require(mesh["ergodicity_used"] is False, "ergodicity guard")
    require(
        mesh["saturation_replaced_by_full_space_only_as_upper_bound"] is True,
        "saturation guard",
    )
    require(
        mesh["off_by_one_guard"]
        == "R_1 has exactly the level x itself and rank B_1=B_inc(x)",
        "tower off-by-one",
    )

    source = result["finite_static_source_natural_Z"]
    require(
        Q(source["numeric_Kac_full_cell_strict_upper"]) == adapted_charge,
        "source full-cell constant",
    )
    require(
        source["proof_only_prechop_bound"]
        == "Z_src,pre,*<=mu_s(C_s)/delta_open+(4000/1999)*Z_src,coarse<infinity",
        "source prechop bound",
    )
    require(
        source["rank_grid_global_bound"]
        == "Z_src,rank,*<724775769/16+(4000/1999)*Z_src,pre,*<infinity",
        "source additive rank-grid bound",
    )
    require(
        source["full_cell_bound"]
        == "sum_full p_j/ell_*(A_j)<=(27/5)*p/delta_(B_max)",
        "full-cell ledger",
    )
    require(
        source["clipped_endpoint_bound"]
        == "sum_at_most_two_endpoints p_j/ell_*(A_j)<=(4000/1999)*p/ell_*(A)",
        "endpoint ledger",
    )
    require(
        source["source_short_refinement_bound"]
        == "Z_src,short,*<=(4000/1999)*Z_src,rank,*<infinity",
        "source short-recut ledger",
    )
    require(
        "delta_open<10^-90" in source["source_short_two_cell_reason"],
        "source short two-cell reason",
    )
    require(source["static_not_moving"] is True, "static replay")
    require(len(source["controlled_initial_family_checks"]) == 5, "input checks")

    final = result["hereditary_replay_and_image_recut_join"]
    n_img = 2397 * 10**90 + 1
    ratio = Q(2000, 1999)
    require(int(final["image_recut_count_upper"]) == n_img, "image count")
    require(Q(final["image_recut_density_ratio"]) == ratio, "image ratio")
    require(
        Q(final["image_refinement_multiplier"]) == ratio * n_img,
        "image multiplier",
    )
    require(final["same_ID_once_charge"] is True, "final once charge")
    require(final["physical_J_pair"] == "CERTIFIED_FINITE", "Jpair result")

    defect = result["physical_defect_moment_join"]
    require(
        Q(defect["coefficient"]) == Q(35, 99 * 2**309),
        "defect coefficient",
    )
    require(defect["same_measure"] is True, "defect same measure")
    require(defect["physical_I_D"] == "CERTIFIED_FINITE", "I_D result")


def independent_typing(result: dict[str, Any]) -> None:
    paired = result["paired_leafwise_reverse_replay"]
    require(
        paired["round35_kernel"]
        == (
            "Psi_s(b,r)=(r,phi=4r+b), p=sin(4r+b), with collision-SRB "
            "conditional density cp/sqrt(17) against slope-four arclength"
        ),
        "exact Round35 kernel",
    )
    require(
        "dphi/dr=4" in paired["exact_leaf_type"]
        and "invariant unstable cone" in paired["exact_leaf_type"],
        "exact slope-four leaf type",
    )
    require(
        "covering only the 24 compact central-homogeneity cores"
        in paired["safe_core_envelope_preparation"]
        and "closure stays in abs(p)<3/10"
        in paired["safe_core_envelope_preparation"]
        and paired["core_nongrazing_bound"]
        == (
            "on every retained parent abs(p)<3/10, hence "
            "cp=sqrt(1-p^2)>sqrt(91)/10>19/20"
        )
        and "abs(d_r log cp)=4*abs(p)/cp<24/19"
        in paired["base_density_cone"]
        and "strictly below 2000/1999" in paired["base_density_cone"]
        and Q(paired["base_log_density_oscillation_strict_upper"])
        == Q(648, 95 * 10**90)
        and Q(paired["base_log_density_oscillation_strict_upper"])
        < Q(1, 2000)
        and paired["base_density_ratio_arithmetic"]
        == "x=648/(95*10^90)<1/2000 and exp(x)<1/(1-x)<2000/1999"
        and paired["no_full_grazing_parent"] is True,
        "safe non-grazing slope-four base",
    )
    require(
        paired["core_restriction"].endswith("norm at most 2000/1999")
        and "Z(G_A0)<infinity" in paired["forward_initial_family"],
        "finite-Z exact forward source",
    )
    require(
        paired["forward_terminal_exact_inclusion"]
        == (
            "every forward terminal proof curve is B'=T_s^n(A') subset "
            "B=T_s^n(A), where A' is a subinterval of the exact Round35 "
            "slope-four A subset R_n leaf"
        ),
        "forward exact B inclusion",
    )
    require(
        paired["cuts_only_split"].endswith(
            "they never transversely redisintegrate"
        ),
        "no transverse redisintegration",
    )
    require(
        "(T_C_s)_#(mu_s|C_s)=mu_s|C_s exactly once"
        in paired["induced_return_once_coverage"]
        and paired["normalization_used"] is False,
        "induced once coverage",
    )
    require(
        paired["reverse_start"].startswith(
            "G_IB=I_#E_fw,total is exactly mu_s|I(C_s)"
        )
        and "Z(G_IB)=Z(E_fw,total)<infinity" in paired["reverse_start"],
        "exact finite-Z I(B) reverse start",
    )
    require(
        paired["reverse_path_identity"]
        == (
            "for the tag B=T_s^n(A), T_s^k(I(B))=I(T_s^(n-k)(A)) "
            "for 0<=k<=n"
        )
        and "first returns to I(C_s) at exactly n"
        in paired["reverse_first_return"],
        "paired reverse first-return identity",
    )
    require(
        paired["reverse_terminal_exact_inclusion"].startswith(
            "every paired reverse terminal proof curve is I(A'') subset I(A)"
        )
        and paired["source_recovery"].endswith(
            "subinterval of the exact Round35 slope-four A leaf"
        ),
        "reverse I(A) and recovered A inclusion",
    )
    require(
        paired["source_measure_and_Z"]
        == (
            "G_src,coarse represents mu_s|C_s exactly once and "
            "Z_src,coarse=Z(E_rev,paired,total)<infinity"
        )
        and paired["no_same_measure_shortcut"] is True
        and "later B_max/source-short ledger is not used"
        in paired["no_circularity"],
        "paired source measure, nonshortcut, and noncircularity",
    )
    require(
        paired["status"]
        == (
            "CERTIFIED_EXACT_ROUND35_SLOPE4_SOURCE_LEAF_REFINEMENT_BY_"
            "PAIRED_REVERSE_REPLAY"
        ),
        "paired replay status",
    )

    ledger = result["metric_and_once_charge_terminal_source_join"]
    require(ledger["forward_view"] == "A -> B", "forward typing")
    require(ledger["reverse_view"] == "I(B) -> I(A)", "reverse typing")
    require(
        ledger["coarse_terminal_outputs"]
        == {
            "forward": "exact tagged B subcurves from the paired forward replay",
            "reverse": "exact tagged I(A) subcurves from the paired reverse replay",
        },
        "terminal outputs",
    )
    require(
        ledger["source_recovery_from_reverse_terminal"].startswith(
            "apply I once to the paired reverse terminal output I(A'') subset I(A)"
        ),
        "I(A) source join",
    )
    require(
        "exactly once" in ledger["coarse_source_family"],
        "source exactly once",
    )
    require(
        ledger["coarse_source_Z"]
        == (
            "Z_src,coarse=Z(E_rev,paired,total)<infinity by the paired reverse "
            "hereditary terminal replay"
        ),
        "paired coarse source Z",
    )
    require(
        "never two physical masses" in ledger["charge_policy"],
        "no double charge",
    )
    require(
        ledger["length_functionals"]
        == {
            "ell_fw_c": "adapted carrier length ell_*(A_c)",
            "ell_rev_c": "adapted carrier length ell_*(I(B_c))=ell_*(B_c)",
            "natural_delta_metric": "Euclidean carrier arclength ell_E on A",
            "image_recut_metric": "adapted carrier arclength ell_* on B",
        },
        "metric ledger",
    )
    require(
        ledger["metric_conversion"].startswith(
            "ell_E<=27/5*ell_*, equivalently ell_*>=5/27*ell_E"
        ),
        "metric conversion",
    )
    require(
        "proof-only canonical chop code forgotten" in ledger["same_ID_final_cell"],
        "proof projection",
    )

    replay = result["hereditary_replay_and_image_recut_join"]
    require("static finite-Z" in replay["replay_input"], "finite-Z replay")
    require("no arbitrary moving sequence" in replay["replay_scope"], "map scope")
    require(
        replay["mass_tail_unchanged"].startswith(
            "the refinement changes only the representation"
        ),
        "same mass replay",
    )
    require(
        replay["hereditary_output"].endswith("is finite"),
        "hereditary output",
    )
    require(
        replay["physical_image_relation"].endswith(
            "Z_image,physical,short<=Z_img,short,*"
        ),
        "physical coarsening",
    )


def nonpromotion_guard(result: dict[str, Any]) -> None:
    required = {
        "natural_mesh_path_rule": "CERTIFIED_BMAX",
        "natural_mesh_Kac_tower_charge": "CERTIFIED_PHYSICAL_L1",
        "exact_round35_slope4_source_leaf_inclusion": (
            "CERTIFIED_BY_PAIRED_REVERSE_REPLAY"
        ),
        "natural_mesh_metric_alignment": "CERTIFIED_ADAPTED_TWO_VIEW_LEDGER",
        "natural_mesh_same_ID_terminal_join": "CERTIFIED_ONCE_CHARGED_WITH_PROOF_REFINEMENT",
        "finite_static_source_natural_Z": "CERTIFIED",
        "hereditary_terminal_replay_on_refined_source": "CERTIFIED",
        "global_connected_image_recut_count_cap": "CERTIFIED_PINNED_ROUND55",
        "terminal_cell_refinement_to_J_pair": "CERTIFIED",
        "physical_J_pair": "CERTIFIED_FINITE",
        "physical_defect_moment_I_D": "CERTIFIED_FINITE",
        "physical_common_refinement_J_cap_total": "NOT_CERTIFIED",
        "physical_proper_same_ID_first_return": "NOT_CERTIFIED",
        "intermediate_C24_avoidance_after_properisation": "NOT_CERTIFIED",
        "later_and_repeated_recovery_clock_moments": "NOT_CERTIFIED",
        "physical_collision_time_q_L6over5": "NOT_CERTIFIED",
        "strong_singular_current_cemetery": "NOT_CERTIFIED",
        "full_numeric_C_fw_C_rev_q": "NOT_CERTIFIED",
        "Gate4": "NOT_CERTIFIED",
        "complete_composite_gates": "0/5",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    require(result["strict_nonpromotion"] == required, "strict frontier map")


def ast_guard() -> None:
    source = Path(cert.__file__).resolve().read_text(encoding="utf-8")
    tree = ast.parse(source)
    strings = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }
    required = {
        "physical_common_refinement_J_cap_total",
        "physical_proper_same_ID_first_return",
        "strong_singular_current_cemetery",
        "NOT_CERTIFIED",
        "NO-GO_FOR_CLAIM",
    }
    require(required.issubset(strings), "AST nonpromotion literals")
    forbidden = {"CERTIFIED_GATE4", "CM2_CERTIFIED", "CERTIFIED_PHYSICAL_Q"}
    require(not strings.intersection(forbidden), "AST forbidden promotion")


def verify_value(value: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(value)
        == {
            "schema",
            "certificate_sha256",
            "verifier_sha256",
            "dependencies",
            "result",
            "verdict",
        },
        "top-level keys",
    )
    require(value["schema"] == EXPECTED_SCHEMA, "schema")
    require(
        value["certificate_sha256"] == sha256_path(Path(cert.__file__).resolve()),
        "certificate hash",
    )
    require(
        value["verifier_sha256"] == sha256_path(Path(__file__).resolve()),
        "verifier hash",
    )
    require(value["dependencies"] == cert.DEPENDENCIES, "dependency map")
    for name, expected_hash in cert.DEPENDENCIES.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"dependency safety: {name}")
        require(path.resolve().parent == HERE, f"dependency parent: {name}")
        require(sha256_path(path) == expected_hash, f"dependency hash: {name}")
    result = value["result"]
    require(isinstance(result, dict), "result root")
    require(
        result["provenance"]["dependency_sha256"] == value["dependencies"],
        "provenance parity",
    )
    require(result["provenance"]["old_artifacts_modified"] is False, "append only")
    require(result["provenance"]["external_source_promoted"] is False, "source scope")
    independent_arithmetic(result)
    independent_typing(result)
    nonpromotion_guard(result)
    digest_copy = copy.deepcopy(result)
    embedded = digest_copy.pop("internal_replay_digest")
    require(embedded == digest(digest_copy), "internal digest")
    require(value["verdict"] == result["strict_nonpromotion"], "verdict parity")
    require(value == expected, "deterministic semantic replay")
    ast_guard()


def verify_manifest(path: Path) -> tuple[dict[str, Any], bytes, bytes]:
    resolved = safe_manifest_path(path)
    raw = resolved.read_bytes()
    value = strict_load(raw)
    check_json_tree(value)
    expected = cert.build_manifest(Path(__file__).resolve())
    verify_value(value, expected)
    reemitted = json.dumps(expected, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    require(raw == reemitted, "manifest is not byte-canonical")
    return value, raw, reemitted


def hostile_mutations(base: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[dict[str, Any]] = []

    def changed(path: tuple[str, ...], replacement: Any) -> None:
        item = copy.deepcopy(base)
        cursor: Any = item
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        mutations.append(item)

    changed(("schema",), EXPECTED_SCHEMA + ".promoted")
    changed(("certificate_sha256",), "0" * 64)
    changed(("verifier_sha256",), "f" * 64)
    bad_deps = copy.deepcopy(base["dependencies"])
    bad_deps[next(iter(bad_deps))] = "1" * 64
    changed(("dependencies",), bad_deps)
    changed(("result", "provenance", "old_artifacts_modified"), True)
    changed(("result", "provenance", "external_source_promoted"), True)
    changed(("result", "path_max_mesh_and_Kac_tower", "ergodicity_used"), True)
    changed(
        ("result", "path_max_mesh_and_Kac_tower", "physical_delta_charge_strict_upper"),
        "1",
    )
    changed(
        ("result", "path_max_mesh_and_Kac_tower", "saturation_replaced_by_full_space_only_as_upper_bound"),
        False,
    )
    changed(
        ("result", "path_max_mesh_and_Kac_tower", "sample_path_rows_sha256"),
        "2" * 64,
    )
    changed(
        ("result", "path_max_mesh_and_Kac_tower", "tower_sample_rows_sha256"),
        "3" * 64,
    )
    changed(
        ("result", "paired_leafwise_reverse_replay", "round35_kernel"),
        "different foliation",
    )
    changed(
        (
            "result",
            "paired_leafwise_reverse_replay",
            "safe_core_envelope_preparation",
        ),
        "full collision section including grazing",
    )
    changed(
        ("result", "paired_leafwise_reverse_replay", "core_nongrazing_bound"),
        "cp can vanish",
    )
    changed(
        ("result", "paired_leafwise_reverse_replay", "no_full_grazing_parent"),
        False,
    )
    changed(
        (
            "result",
            "paired_leafwise_reverse_replay",
            "forward_terminal_exact_inclusion",
        ),
        "same measure only",
    )
    changed(
        (
            "result",
            "paired_leafwise_reverse_replay",
            "induced_return_once_coverage",
        ),
        "double charged",
    )
    changed(
        ("result", "paired_leafwise_reverse_replay", "reverse_path_identity"),
        "untyped reverse path",
    )
    changed(
        (
            "result",
            "paired_leafwise_reverse_replay",
            "reverse_terminal_exact_inclusion",
        ),
        "generic I(A)",
    )
    changed(
        ("result", "paired_leafwise_reverse_replay", "no_same_measure_shortcut"),
        False,
    )
    changed(
        ("result", "paired_leafwise_reverse_replay", "status"),
        "NOT_CERTIFIED",
    )
    changed(
        ("result", "metric_and_once_charge_terminal_source_join", "reverse_view"),
        "A -> B",
    )
    changed(
        ("result", "metric_and_once_charge_terminal_source_join", "charge_policy"),
        "two masses",
    )
    changed(
        ("result", "metric_and_once_charge_terminal_source_join", "coarse_source_Z"),
        "generic reverse terminal Z",
    )
    changed(
        ("result", "metric_and_once_charge_terminal_source_join", "metric_conversion"),
        "no conversion",
    )
    changed(
        ("result", "metric_and_once_charge_terminal_source_join", "length_functionals", "ell_fw_c"),
        "Euclidean",
    )
    changed(
        ("result", "finite_static_source_natural_Z", "rank_grid_global_bound"),
        "product of two L1 quantities",
    )
    changed(
        ("result", "finite_static_source_natural_Z", "full_cell_bound"),
        "false",
    )
    changed(
        ("result", "finite_static_source_natural_Z", "clipped_endpoint_bound"),
        "false",
    )
    changed(
        ("result", "finite_static_source_natural_Z", "source_short_refinement_bound"),
        "false",
    )
    changed(("result", "finite_static_source_natural_Z", "static_not_moving"), False)
    changed(
        ("result", "hereditary_replay_and_image_recut_join", "replay_scope"),
        "arbitrary moving sequence",
    )
    changed(
        ("result", "hereditary_replay_and_image_recut_join", "image_recut_count_upper"),
        "1",
    )
    changed(
        ("result", "hereditary_replay_and_image_recut_join", "image_refinement_multiplier"),
        "1",
    )
    changed(
        ("result", "hereditary_replay_and_image_recut_join", "same_ID_once_charge"),
        False,
    )
    changed(
        ("result", "hereditary_replay_and_image_recut_join", "physical_J_pair"),
        "NOT_CERTIFIED",
    )
    changed(("result", "physical_defect_moment_join", "coefficient"), "1")
    changed(("result", "physical_defect_moment_join", "same_measure"), False)
    changed(
        ("result", "physical_defect_moment_join", "physical_I_D"),
        "NOT_CERTIFIED",
    )
    changed(("result", "strict_nonpromotion", "physical_J_pair"), "NOT_CERTIFIED")
    changed(
        (
            "result",
            "strict_nonpromotion",
            "exact_round35_slope4_source_leaf_inclusion",
        ),
        "NOT_CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "physical_defect_moment_I_D"),
        "NOT_CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "physical_common_refinement_J_cap_total"),
        "CERTIFIED",
    )
    changed(
        ("result", "strict_nonpromotion", "physical_proper_same_ID_first_return"),
        "CERTIFIED",
    )
    changed(("result", "strict_nonpromotion", "physical_collision_time_q_L6over5"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "Gate4"), "CERTIFIED")
    changed(("result", "strict_nonpromotion", "complete_composite_gates"), "1/5")
    changed(("result", "strict_nonpromotion", "CM2"), "GO")
    changed(("result", "internal_replay_digest"), "4" * 64)
    changed(("verdict", "Gate4"), "CERTIFIED")
    item = copy.deepcopy(base)
    item["unexpected"] = True
    mutations.append(item)
    return mutations


def run_self_test(path: Path) -> int:
    base, raw, _ = verify_manifest(path)
    expected = cert.build_manifest(Path(__file__).resolve())
    rejected = 0
    mutations = hostile_mutations(base)
    for index, item in enumerate(mutations):
        try:
            verify_value(item, expected)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"hostile mutation accepted: {index}")
    raw_cases = [
        b'{"schema":"a","schema":"b"}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
    ]
    duplicate = raw.replace(
        b'{\n  "certificate_sha256"',
        b'{\n  "schema": "duplicate",\n  "certificate_sha256"',
        1,
    )
    raw_cases.append(duplicate)
    for item in raw_cases:
        try:
            strict_load(item)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("hostile raw JSON accepted")
    total = len(mutations) + len(raw_cases)
    require(rejected == total, "hostile rejection count")
    print(f"HOSTILE_MUTATIONS_REJECTED: {rejected}/{total}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reemit", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test(args.manifest)
    manifest, raw, reemitted = verify_manifest(args.manifest)
    if args.reemit:
        require(raw == reemitted, "re-emission mismatch")
        print("REEMIT_BYTE_IDENTICAL: PASS")
        return 0
    print("AUDIT_MODE: PASS")
    print("PHYSICAL_J_PAIR:", manifest["verdict"]["physical_J_pair"])
    print("PHYSICAL_I_D:", manifest["verdict"]["physical_defect_moment_I_D"])
    print("GATE4:", manifest["verdict"]["Gate4"])
    print("CM2:", manifest["verdict"]["CM2"])
    return 0 if args.audit else 2


if __name__ == "__main__":
    raise SystemExit(main())
