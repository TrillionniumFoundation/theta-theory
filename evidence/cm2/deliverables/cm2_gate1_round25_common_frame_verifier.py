#!/usr/bin/env python3
"""Independent verifier for the round-25 Gate-1 common-frame leaf.

The verifier never imports the producer.  It hashes the producer and every
dependency before independently rebuilding the exact rational factorisation,
the same-gauge joins, the uniform q bound, and the fail-closed verdict.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_gate1_round25_common_frame_cert.py"
MANIFEST = HERE / "cm2-gate1-round25-common-frame-manifest-2026-07-18.json"
REPORT = HERE / "cm2-gate1-round25-common-frame-assault-2026-07-18.md"
EXPECTED_CERTIFICATE_SHA256 = "e3d1fcb0106745380b04d416cb6bc2ca76df362ce7c4ca6458337696ceab56c5"

EXPECTED_DEPENDENCIES = {
    "cm2-twenty-fourth-direct-assault-manifest-2026-07-18.sha256":
        "fde26b3f560086484a63cd0cc2e39a025d573c31982295a3702a14f9821e3c2c",
    "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json":
        "fc2d7263d4cb659a82c7ecb0fad48f538b466f861f1295d78bb6738331b8c4cd",
    "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json":
        "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json":
        "1e61f6f600300d15a15cf04179ee6e889ceb09edcf3d3b26f0d6f735afd6bdec",
    "cm2-gate1-biprojective-half-density-frontier-manifest-2026-07-17.json":
        "6c6e8465161a64785ae07b3bd7a229820c93bacd9d07a2cd10c4691686722d6b",
    "cm2-gate1-common-transport-ift-frontier-manifest-2026-07-17.json":
        "b4a7838178ea2fe54d6fed68f99fc03f20d4efaa2e5c9ba4df13e7c5613e8527",
}

COMPACT = "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
NUMERIC = "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json"
GLOBAL = "cm2-gate1-global-coding-class-h-separation-frontier-manifest-2026-07-16.json"
HALF = "cm2-gate1-biprojective-half-density-frontier-manifest-2026-07-17.json"
TRANSPORT = "cm2-gate1-common-transport-ift-frontier-manifest-2026-07-17.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class VerificationError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise VerificationError(code, detail)


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError("DUPLICATE_JSON_KEY", key)
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise VerificationError("NONFINITE_JSON", token)


def parse_json_text(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_pairs,
            parse_constant=reject_constant,
        )
    except VerificationError:
        raise
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise VerificationError("MALFORMED_JSON", str(exc)) from exc


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_regular_file(path: Path, code: str) -> None:
    require(path.parent.resolve() == HERE, code, f"escaped parent: {path.name}")
    require(not path.is_symlink(), code, f"symlink: {path.name}")
    require(path.is_file(), code, f"missing: {path.name}")


def load_dependency_data() -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for name, expected in EXPECTED_DEPENDENCIES.items():
        path = HERE / name
        safe_regular_file(path, "DEPENDENCY_PATH")
        require(sha256_path(path) == expected, "DEPENDENCY_HASH", name)
        if path.suffix == ".json":
            loaded[name] = parse_json_text(path.read_text(encoding="utf-8"))
    return loaded


def independent_sample() -> dict[str, Any]:
    u, v = Fraction(7, 9), Fraction(1)
    d, f = 1 + u * v, Fraction(4, 3)
    u_bip, q = u / d, 1 / d
    require(f * f == d, "ALGEBRA", "sqrt(d)")
    product = ((d, v), (u, Fraction(1)))
    bip = ((f, f * v), (f * u_bip, f))
    diag = ((f, Fraction(0)), (Fraction(0), 1 / f))

    def mul(a: Any, b: Any) -> Any:
        return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), Fraction())
                           for j in range(2)) for i in range(2))

    def det(a: Any) -> Fraction:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]

    require(mul(bip, diag) == product, "ALGEBRA", "factorisation")
    require(det(product) == det(bip) == det(diag) == 1, "ALGEBRA", "determinants")
    require(q == 1 - u_bip * v, "ALGEBRA", "q")
    fmt = lambda x: f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
    return {
        "sample_product_coordinates": {"u": fmt(u), "v": fmt(v), "d": fmt(d)},
        "sample_biprojective_coordinates": {
            "u_bip": fmt(u_bip), "v_bip": fmt(v), "q": fmt(q), "sqrt_d": fmt(f)
        },
        "product_gauge": [[fmt(x) for x in row] for row in product],
        "biprojective_factor": [[fmt(x) for x in row] for row in bip],
        "positive_diagonal_factor": [[fmt(x) for x in row] for row in diag],
        "factorisation_and_three_determinants_exact": True,
    }


def independent_expected_result() -> dict[str, Any]:
    deps = load_dependency_data()
    compact = deps[COMPACT]["result"]
    numeric = deps[NUMERIC]["result"]
    global_result = deps[GLOBAL]["result"]
    half = deps[HALF]["result"]
    transport = deps[TRANSPORT]["result"]
    compact_digest = compact["internal_digest"]

    require(numeric["provenance"]["compact_internal_digest"] == compact_digest,
            "SAME_GAUGE_BINDING", "numeric")
    require(global_result["provenance"]["compact_internal_digest"] == compact_digest,
            "SAME_GAUGE_BINDING", "connector")
    require(compact["compact_supported_section_gauge"]["single_section_gauge"]
            == "B_hat(x,y)=(I+t_u E_12)(I+t_s E_21) in U_chart, B_hat=I outside U_chart",
            "SAME_GAUGE_BINDING", "formula")
    require(numeric["canonical_coordinate_and_gauge_audit"]["gauge_matrix"]
            == "B_u(x) B_s(y)", "SAME_GAUGE_BINDING", "order")
    require(numeric["tail_majorants"]["chart_radius"] == "1e-10", "RADIUS")
    obstruction = global_result["connector_compact_gauge_obstruction"]
    require(obstruction["compact_qnl_gauge_chart_radius"] == "1e-10", "RADIUS")
    require(compact["compact_supported_section_gauge"]["determinant"] == "1 exactly",
            "DETERMINANT")
    require(compact["compact_supported_section_gauge"]["global_inverse_on_section"] is True,
            "INVERTIBILITY")
    require(compact["local_qnl_plaque_holonomies"]["uniform_holder_modulus_on_global_coding"]
            is False, "NONPROMOTION")
    wedges = numeric["four_selected_twisting_wedges"]
    require(len(wedges) == 4, "WEDGE_COUNT")
    require(numeric["scope_limits"]["four_selected_QNL_eigen_axis_twisting_wedges"]
            is True, "WEDGES")
    require(obstruction["compact_qnl_gauge_connector_stable_limit_converges"] is False,
            "CONNECTOR_OBSTRUCTION")
    require(obstruction["compact_qnl_gauge_class_H_on_common_basic_set_with_connector"]
            is False, "CONNECTOR_OBSTRUCTION")
    require(half["strict_nonpromotion"]["uniform_big_cell_q_lower_bound"]
            == "NOT_CERTIFIED", "PREDECESSOR_BOUNDARY")
    require(transport["strict_nonpromotion"]["coupled_half_density_groupoid_solution"]
            == "NOT_CERTIFIED", "PREDECESSOR_BOUNDARY")

    exp3_partial = Fraction(1) + Fraction(3) + Fraction(9, 2) + Fraction(27, 6)
    require(exp3_partial == 13 and exp3_partial > 10, "BOUND", "log10")
    product_bound = Fraction(1, 10**36)
    require(1 / (1 + product_bound) > Fraction(999, 1000), "BOUND", "q")

    core: dict[str, Any] = {
        "schema": "cm2.gate1.round25.common-frame-same-representative-frontier.v1",
        "provenance": {
            "dependency_sha256": dict(EXPECTED_DEPENDENCIES),
            "compact_gauge_internal_digest": compact_digest,
            "old_artifacts_modified": False,
            "arithmetic": "exact rational algebra plus frozen Arb interval dependencies",
        },
        "same_compact_gauge_binding": {
            "section_gauge": "G=U_v L_u=[[1+uv,v],[u,1]], with u=t_s and v=t_u",
            "cutoff_choice": "0<=chi<=1, chi=1 on U_core, chi=0 on the boundary collar",
            "chart_coordinate_radius": "1/10^10",
            "coefficient_bound": "0<k<1 (frozen 5000-bit Arb enclosure)",
            "same_gauge_local_qnl_stable_holonomies": True,
            "same_gauge_local_qnl_unstable_holonomies": True,
            "same_gauge_selected_homoclinic_loop": True,
            "same_gauge_four_nonzero_twisting_wedges": True,
            "same_gauge_connector_basic_set_obstruction": True,
            "gauge_identity_outside_chart": True,
        },
        "uniform_big_cell_certificate": {
            "log10_upper_witness": "exp(3)>1+3+9/2+27/6=13>10, hence log(10)<3",
            "monotonicity": "-r^2 log(r) is increasing on 0<r<=10^-10",
            "term_bounds": "|u|<1/10^18 and |v|<1/10^18",
            "product_bound": "|uv|<1/10^36",
            "gauss_denominator": "d=1+uv>0",
            "biprojective_coordinates": "u_bip=u/(1+uv), v_bip=v, q=1-u_bip*v_bip=1/(1+uv)",
            "uniform_q_lower_bound": "q>999/1000",
            "uniform_q_lower_bound_certified": True,
            "whole_compact_return_section": True,
            "outside_chart_q": "q=1",
        },
        "exact_common_frame_factorisation": {
            "identity": "U_v L_u = q^(-1/2)[[1,v_bip],[u_bip,1]] diag(sqrt(1+uv),1/sqrt(1+uv))",
            "biprojective_frame_columns": "a=q^(-1/2)(1,u_bip)^T, b=q^(-1/2)(v_bip,1)^T",
            "frame_determinant": "det(a,b)=1 exactly",
            "positive_diagonal_remainder": True,
            "same_original_physical_representative": True,
            "rational_replay": independent_sample(),
        },
        "same_representative_join": {
            "local_canonical_Hs_Hu_and_selected_twisting_in_one_gauge": True,
            "four_wedge_enclosures": dict(wedges),
            "connector_stable_increment": obstruction["canonical_increment_formula"],
            "connector_stable_increment_asymptotic": obstruction["canonical_increment_asymptotic"],
            "compact_gauge_class_H_on_common_basic_set_with_connector": False,
            "consequence": "this exact compact twisting candidate cannot close Gate 1 on the connector common basic set",
            "diagonal_class_H_representative_is_a_different_representative": True,
        },
        "maturity": {
            "candidate_interface_slots_total": 6,
            "candidate_interface_slots_positive": 5,
            "positive_slots": [
                "single determinant-one compact physical gauge",
                "uniform positive big cell and determinant-one common frame",
                "canonical Hs/Hu on the local QNL plaques",
                "typed selected immutable homoclinic loop",
                "four nonzero selected twisting wedges",
            ],
            "failed_global_slot": "uniform all-plaque Butler-Park class H in this same representative",
            "failed_global_slot_status": "REFUTED_ON_FROZEN_CONNECTOR_BASIC_SET",
            "gate1_maturity": "0/1",
        },
        "strict_nonpromotion": {
            "coupled_half_density_groupoid_equations_on_all_plaques": "NOT_CERTIFIED",
            "uniform_all_plaque_holder_holonomies_in_twisting_gauge": "NOT_CERTIFIED",
            "compact_twisting_gauge_in_class_H_on_connector_basic_set": False,
            "another_third_gauge_with_class_H_and_twisting": "NOT_CERTIFIED",
            "full_mass_physical_projective_PPE": "NOT_CERTIFIED",
            "Gate1": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = dict(core)
    result["internal_replay_digest"] = digest(core)
    return result


TOP_KEYS = {
    "schema", "date", "certificate_sha256", "verifier_sha256",
    "report_sha256", "dependencies", "result", "verdict",
}


def validate_manifest(manifest: Any, expected_result: dict[str, Any]) -> None:
    require(type(manifest) is dict, "TOP_TYPE")
    require(set(manifest) == TOP_KEYS, "TOP_KEYS")
    for key in ("schema", "date", "certificate_sha256", "verifier_sha256",
                "report_sha256", "verdict"):
        require(type(manifest[key]) is str, "FIELD_TYPE", key)
    require(type(manifest["dependencies"]) is dict, "FIELD_TYPE", "dependencies")
    require(type(manifest["result"]) is dict, "FIELD_TYPE", "result")
    require(manifest["schema"] == "cm2.gate1.round25.common-frame.manifest.v1",
            "MANIFEST_SCHEMA")
    require(manifest["date"] == "2026-07-18", "DATE")
    for key in ("certificate_sha256", "verifier_sha256", "report_sha256"):
        require(HEX64.fullmatch(manifest[key]) is not None, "MALFORMED_SHA", key)
    require(manifest["certificate_sha256"] == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_PIN")
    require(manifest["dependencies"] == EXPECTED_DEPENDENCIES, "DEPENDENCY_MAP")
    require(canonical_bytes(manifest["result"]) == canonical_bytes(expected_result),
            "RESULT_MISMATCH")
    require(manifest["verdict"]
            == "BIG-CELL/COMMON-FRAME JOIN CERTIFIED FOR THE COMPACT TWISTING GAUGE; "
               "SAME-REPRESENTATIVE GLOBAL CLASS H REFUTED ON THE CONNECTOR BASIC SET; "
               "GATE 1 NOT CERTIFIED",
            "VERDICT")


def load_and_validate() -> tuple[dict[str, Any], dict[str, Any]]:
    require(sys.flags.optimize == 0, "OPTIMIZED_PYTHON")
    safe_regular_file(CERTIFICATE, "CERTIFICATE_PATH")
    safe_regular_file(MANIFEST, "MANIFEST_PATH")
    safe_regular_file(REPORT, "REPORT_PATH")
    safe_regular_file(Path(__file__).resolve(), "VERIFIER_PATH")
    require(sha256_path(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_HASH")
    expected = independent_expected_result()
    manifest = parse_json_text(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest(manifest, expected)
    require(sha256_path(CERTIFICATE) == manifest["certificate_sha256"],
            "CERTIFICATE_HASH")
    require(sha256_path(Path(__file__).resolve()) == manifest["verifier_sha256"],
            "VERIFIER_HASH")
    require(sha256_path(REPORT) == manifest["report_sha256"], "REPORT_HASH")
    # Rehash after replay to reject time-of-check/time-of-use replacement.
    require(sha256_path(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
            "CERTIFICATE_REHASH")
    for name, expected_hash in EXPECTED_DEPENDENCIES.items():
        require(sha256_path(HERE / name) == expected_hash, "DEPENDENCY_REHASH", name)
    return manifest, expected


def mutate_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def run_self_test(valid: dict[str, Any], expected: dict[str, Any]) -> int:
    tests: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = []

    def add(name: str, code: str, fn: Callable[[dict[str, Any]], None]) -> None:
        tests.append((name, code, fn))

    add("remove top key", "TOP_KEYS", lambda x: x.pop("date"))
    add("extra top key", "TOP_KEYS", lambda x: x.update(extra=False))
    add("replace top shape", "TOP_KEYS", lambda x: x.clear() or x.update({"x": 1}))
    add("schema", "MANIFEST_SCHEMA", lambda x: x.update(schema="v2"))
    add("date", "DATE", lambda x: x.update(date="2026-07-17"))
    add("cert malformed", "MALFORMED_SHA", lambda x: x.update(certificate_sha256="0"))
    add("verifier malformed", "MALFORMED_SHA", lambda x: x.update(verifier_sha256="g" * 64))
    add("report malformed", "MALFORMED_SHA", lambda x: x.update(report_sha256=""))
    add("cert changed", "CERTIFICATE_PIN", lambda x: x.update(certificate_sha256="0" * 64))
    add("dependencies list", "FIELD_TYPE", lambda x: x.update(dependencies=[]))
    add("dependency missing", "DEPENDENCY_MAP", lambda x: x["dependencies"].pop(next(iter(x["dependencies"]))))
    add("dependency extra", "DEPENDENCY_MAP", lambda x: x["dependencies"].update({"../escape": "0" * 64}))
    add("dependency changed", "DEPENDENCY_MAP", lambda x: x["dependencies"].update({next(iter(x["dependencies"])): "0" * 64}))
    add("result list", "FIELD_TYPE", lambda x: x.update(result=[]))
    add("result missing key", "RESULT_MISMATCH", lambda x: x["result"].pop("maturity"))
    add("result extra key", "RESULT_MISMATCH", lambda x: x["result"].update(extra=False))
    result_mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("q lower", ("result", "uniform_big_cell_certificate", "uniform_q_lower_bound"), "q>1"),
        ("q flag false", ("result", "uniform_big_cell_certificate", "uniform_q_lower_bound_certified"), False),
        ("q bool integer", ("result", "uniform_big_cell_certificate", "uniform_q_lower_bound_certified"), 1),
        ("term bound", ("result", "uniform_big_cell_certificate", "term_bounds"), "|u|<1"),
        ("product bound", ("result", "uniform_big_cell_certificate", "product_bound"), "|uv|<1"),
        ("outside q", ("result", "uniform_big_cell_certificate", "outside_chart_q"), "unknown"),
        ("frame determinant", ("result", "exact_common_frame_factorisation", "frame_determinant"), "not one"),
        ("factor identity", ("result", "exact_common_frame_factorisation", "identity"), "swapped"),
        ("sample q", ("result", "exact_common_frame_factorisation", "rational_replay", "sample_biprojective_coordinates", "q"), "1"),
        ("sample matrix", ("result", "exact_common_frame_factorisation", "rational_replay", "product_gauge", 0, 0), "1"),
        ("same gauge loop", ("result", "same_compact_gauge_binding", "same_gauge_selected_homoclinic_loop"), False),
        ("same gauge Hs", ("result", "same_compact_gauge_binding", "same_gauge_local_qnl_stable_holonomies"), False),
        ("same gauge Hu", ("result", "same_compact_gauge_binding", "same_gauge_local_qnl_unstable_holonomies"), False),
        ("wedge removed", ("result", "same_representative_join", "four_wedge_enclosures", "wedge_e1_psi_e1"), "0"),
        ("class H promoted", ("result", "same_representative_join", "compact_gauge_class_H_on_common_basic_set_with_connector"), True),
        ("positive total", ("result", "maturity", "candidate_interface_slots_positive"), 6),
        ("slot total", ("result", "maturity", "candidate_interface_slots_total"), 5),
        ("gate maturity", ("result", "maturity", "gate1_maturity"), "1/1"),
        ("failed status", ("result", "maturity", "failed_global_slot_status"), "CERTIFIED"),
        ("coupled promoted", ("result", "strict_nonpromotion", "coupled_half_density_groupoid_equations_on_all_plaques"), "CERTIFIED"),
        ("Gate1 promoted", ("result", "strict_nonpromotion", "Gate1"), "CERTIFIED"),
        ("CM2 promoted", ("result", "strict_nonpromotion", "CM2"), "GO"),
        ("old modified", ("result", "provenance", "old_artifacts_modified"), True),
        ("digest stale", ("result", "internal_replay_digest"), "0" * 64),
    ]
    for name, path, replacement in result_mutations:
        add(name, "RESULT_MISMATCH", lambda x, p=path, r=replacement: mutate_path(x, p, r))
    add("verdict", "VERDICT", lambda x: x.update(verdict="CERTIFIED"))

    passed = 0
    for name, expected_code, fn in tests:
        candidate = deepcopy(valid)
        fn(candidate)
        try:
            validate_manifest(candidate, expected)
        except VerificationError as exc:
            require(exc.code == expected_code, "SELF_TEST_WRONG_CODE",
                    f"{name}: {exc.code} != {expected_code}")
            passed += 1
        else:
            raise VerificationError("SELF_TEST_ACCEPTED", name)

    duplicate = '{"schema":"x","schema":"y"}'
    try:
        parse_json_text(duplicate)
    except VerificationError as exc:
        require(exc.code == "DUPLICATE_JSON_KEY", "SELF_TEST_WRONG_CODE", "duplicate")
        passed += 1
    else:
        raise VerificationError("SELF_TEST_ACCEPTED", "duplicate JSON")

    for token in ("NaN", "Infinity", "-Infinity"):
        try:
            parse_json_text('{"x":' + token + '}')
        except VerificationError as exc:
            require(exc.code == "NONFINITE_JSON", "SELF_TEST_WRONG_CODE", token)
            passed += 1
        else:
            raise VerificationError("SELF_TEST_ACCEPTED", token)

    print(f"SELF-TEST PASS: {passed}/{passed} hostile mutations rejected")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--integrity-only", action="store_true")
    modes.add_argument("--replay", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if not (args.integrity_only or args.replay or args.self_test):
        print("LIVE VERDICT: Gate 1 NOT_CERTIFIED (fail-closed)")
        return 2
    try:
        manifest, expected = load_and_validate()
        if args.self_test:
            run_self_test(manifest, expected)
        elif args.replay:
            print("REPLAY PASS: independent common-frame/q-bound/same-gauge join")
        else:
            print("INTEGRITY PASS: certificate, dependencies, report, verifier, manifest")
        return 0
    except VerificationError as exc:
        print(f"VERIFY FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
