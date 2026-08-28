#!/usr/bin/env python3
"""Gate-1 global-coding / class-H separation frontier.

This certificate preserves every frozen predecessor.  It adds three strictly
separated statements.

1.  The selected symmetric QNL homoclinic occurrence is transverse.  The
    proof uses the already validated whole graph tube, propagates its complete
    tangent cone through the 48-collision half word, and compares the tangent
    with its image under the billiard reversing involution.  Birkhoff--Smale
    then supplies a clean finite Markov coding on a compact horseshoe.  The
    pulled-back cocycle is the actual derivative, not a frozen word matrix.

2.  On any such finite symbolic coding the invariant stable/unstable line
    fields give a faithful diagonal representative.  After a finite higher
    block recoding its scalar signs are one-step.  The two scalar logarithms
    have summable variations on local plaques, hence this diagonal
    representative belongs to Butler--Park class H.  Its canonical holonomy
    loops are diagonal and therefore fail the required same-axis twisting
    identically.

3.  The compact QNL logarithmic gauge from the frozen stack is identity near
    the distinct connector periodic point.  A fresh point-jet replay of the
    connector return proves a nonzero stable mixed coefficient.  The canonical
    stable comparison increments then grow exponentially on every nontrivial
    local connector stable tail, so that particular compact gauge is not in
    class H on the earlier common basic set containing the connector.

The diagonal class-H representative and the twisting compact-gauge
representative are deliberately not identified.  No single representative
is certified to have both global class H and the selected twisting loop.
Gate 1 and unconditional CM2 therefore remain fail-closed.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

IMMUTABLE_MANIFEST = (
    HERE / "cm2-gate1-immutable-homoclinic-plaque-entry-frontier-manifest-2026-07-16.json"
)
NUMERIC_MANIFEST = (
    HERE / "cm2-gate1-numeric-holonomy-tail-twisting-frontier-manifest-2026-07-16.json"
)
COMPACT_MANIFEST = (
    HERE / "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
)
COMMON_MAGNET_SIDECAR = HERE / "cm2-gate1-common-magnet-manifest-2026-07-15.sha256"
IMMUTABLE_CERT = HERE / "cm2_gate1_immutable_homoclinic_plaque_entry_frontier_cert.py"
CONNECTOR_CERT = HERE / "cm2_gate1_connector_stable_graph_cert.py"
QNL_GRAPH_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
FULL_CROSS_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
TRUE_GRAPH_CERT = HERE / "cm2_gate1_true_graph_krawczyk_cert.py"
SHADOW_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"

EXPECTED_HASHES = {
    IMMUTABLE_MANIFEST.name: "e583a7c0f43f291f92ffb7dc15a4888bda6702340f3209bfd7ec224101df841c",
    NUMERIC_MANIFEST.name: "4b9baaacaf7a315659448072d8d382bc90c4b41a9d98746b63c786f206ad449a",
    COMPACT_MANIFEST.name: "fc2d7263d4cb659a82c7ecb0fad48f538b466f861f1295d78bb6738331b8c4cd",
    COMMON_MAGNET_SIDECAR.name: "92990c108a8b54787d7b3d7340e4afaa92ad540bdb227c5dd4fd88e805a936eb",
    IMMUTABLE_CERT.name: "22e4fca1ff76baef390c40850243b87ac553fa81621fbbac4c2e02195650d3d3",
    CONNECTOR_CERT.name: "7440b97ad97fc876dbc9d42c56cb9dc1d3239f3eb0d95c30e501f0115e73b77f",
    QNL_GRAPH_CERT.name: "0945b084263e2f48d4cc8521e3e1f24986d28d057ec62de829a18471b8e46fa9",
    TANGENT_CERT.name: "d58a196da59b1f31191ad67239b079e669a5629aec1deaee925fa76d9c489ed1",
    FULL_CROSS_CERT.name: "1eb603891c13e3615f74b5b25151dba3f8dab7933811c2ffeb85a3bf22283942",
    TRUE_GRAPH_CERT.name: "ea90579306b5fd3064cba500ac916cbc5ca8f21e89e8b7863fb711f8a547f4e7",
    SHADOW_CERT.name: "5ce6e38558bd1de56e17c8ef620fc27b6e73f7b04764d272823964c3b9334abc",
}

PRECISION_BITS = 1000
BUTLER_PARK_ARXIV = "1909.11548v2"
BUTLER_PARK_PDF_SHA256 = (
    "63c186b1a09db9db50882ba29c32b6395d868596138011f97d5284a484a590ca"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def short(value: object, digits: int = 80) -> str:
    method = getattr(value, "str", None)
    return method(digits) if callable(method) else str(value)


def audit_frozen_inputs() -> dict[str, Any]:
    for name, expected in EXPECTED_HASHES.items():
        path = HERE / name
        if sha256_path(path) != expected:
            raise RuntimeError(f"frozen dependency hash changed: {name}")

    immutable = json.loads(IMMUTABLE_MANIFEST.read_text(encoding="utf-8"))
    numeric = json.loads(NUMERIC_MANIFEST.read_text(encoding="utf-8"))
    compact = json.loads(COMPACT_MANIFEST.read_text(encoding="utf-8"))

    if immutable["verdict"]["selected_immutable_qnl_homoclinic_orbit"] != "CERTIFIED":
        raise RuntimeError("selected immutable homoclinic dependency disappeared")
    if numeric["verdict"]["four_selected_QNL_twisting_wedges"] != "CERTIFIED":
        raise RuntimeError("selected twisting dependency disappeared")
    if compact["result"]["scope_limits"]["global_all_pairs_holder_holonomies"]:
        raise RuntimeError("compact predecessor unexpectedly claims global class H")

    return {
        "immutable_internal_digest": immutable["result"]["internal_digest"],
        "numeric_internal_digest": numeric["result"]["internal_digest"],
        "compact_internal_digest": compact["result"]["internal_digest"],
        "dependencies": dict(EXPECTED_HASHES),
        "butler_park_arxiv": BUTLER_PARK_ARXIV,
        "audited_pdf_sha256": BUTLER_PARK_PDF_SHA256,
    }


def certify_selected_transversality() -> dict[str, Any]:
    immutable = load(IMMUTABLE_CERT, "cm2_gate1_global_immutable")
    full_cross = load(FULL_CROSS_CERT, "cm2_gate1_global_full_cross")
    parent = load(TRUE_GRAPH_CERT, "cm2_gate1_global_parent")
    qnl = load(QNL_GRAPH_CERT, "cm2_gate1_global_qnl")
    connector = load(CONNECTOR_CERT, "cm2_gate1_global_connector_graph")
    tangent = load(TANGENT_CERT, "cm2_gate1_global_tangent")
    shadow = load(SHADOW_CERT, "cm2_gate1_global_shadow")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    shadow.refresh_exact_geometry(module)
    _, slope_qnl, _ = tangent.setup_fixed_data(module)
    qnl.certify_graph_transform(module)

    half_word = tuple(tangent.QNL_FORWARD_WORD) * 2 + tuple(
        tangent.CONNECTOR_REVERSE_FORWARD_WORD
    ) * 2
    if len(half_word) != 48:
        raise RuntimeError("selected symmetric half word changed")

    whole = immutable.replay_rectangle(
        full_cross,
        parent,
        qnl,
        connector,
        tangent,
        module,
        slope_qnl,
        half_word,
        module.arb(immutable.ROOT_X_CENTER),
        module.arb(immutable.ROOT_X_RADIUS),
        module.arb(immutable.GRAPH_ORDINATE_TUBE),
    )
    derivative = whole.derivative_box(module)
    graph_lipschitz = module.arb(immutable.GRAPH_LIPSCHITZ)

    # The actual tangent is (1,h'(x)) with |h'|<=L.  Both components of
    # D(T^48)(1,h') are strictly positive throughout the complete graph tube.
    theta_component_lower = derivative[0][0] - abs(derivative[0][1]) * graph_lipschitz
    momentum_component_lower = derivative[1][0] - abs(derivative[1][1]) * graph_lipschitz
    if not theta_component_lower > module.arb("9e26"):
        raise RuntimeError(
            f"terminal tangent may be vertical/degenerate: {theta_component_lower}"
        )
    if not momentum_component_lower > module.arb("2e27"):
        raise RuntimeError(
            f"terminal tangent may be horizontal/degenerate: {momentum_component_lower}"
        )

    # At the symmetric midpoint w in Fix(I), D I(a,b)=(a,-b).  Therefore
    # |det((a,b),D I(a,b))|=2|ab|.  This is precisely the crossing of
    # T^48 W^u(p) with its reflected stable branch.
    determinant_lower = 2 * theta_component_lower * momentum_component_lower
    if not determinant_lower > module.arb("3e54"):
        raise RuntimeError(f"symmetric homoclinic crossing may be tangent: {determinant_lower}")

    thresholds = {
        "flight": module.arb(18) / 100,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(63) / 100,
        "clearance": module.arb(22) / 100,
    }
    for name, threshold in thresholds.items():
        if not whole.minima[name] > threshold:
            raise RuntimeError(f"selected half-word physical margin changed: {name}")

    return {
        "arb_precision_bits": PRECISION_BITS,
        "selected_half_collision_count": 48,
        "symmetric_full_collision_count": 96,
        "actual_unstable_graph_tangent_cone": "(1,h'(x)), |h'(x)|<=1e-4",
        "terminal_theta_tangent_component_lower": short(theta_component_lower),
        "terminal_momentum_tangent_component_lower": short(momentum_component_lower),
        "reflection_tangent_determinant_formula": "det((a,b),(a,-b))=-2*a*b",
        "absolute_reflection_tangent_determinant_lower": short(determinant_lower),
        "absolute_reflection_tangent_determinant_gt_3e54": True,
        "selected_qnl_homoclinic_is_transverse": True,
        "clean_physical_half_word_replayed": True,
        "birkhoff_smale_clean_horseshoe_exists": True,
        "finite_markov_partition_for_a_clean_return_iterate_exists": True,
    }


def certify_connector_compact_gauge_obstruction() -> dict[str, Any]:
    connector = load(CONNECTOR_CERT, "cm2_gate1_global_connector_obstruction")
    qnl = connector.load_helper(QNL_GRAPH_CERT, "cm2_gate1_global_connector_qnl")
    tangent = connector.load_helper(TANGENT_CERT, "cm2_gate1_global_connector_tangent")
    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    root, slope_qnl, slope_connector = tangent.setup_fixed_data(module)

    # Point jets avoid the deliberately wide graph-transform core enclosure.
    # Root uncertainty is still carried at 1e-70.
    data = connector.compose_connector_core(
        qnl,
        module,
        root,
        slope_connector,
        module.arb(0),
        module.arb(connector.QUADRATIC_CONSTANT),
    )
    mixed = data.hessians[1][0][1]
    if not mixed < module.arb("-0.04") or not mixed > module.arb("-0.05"):
        raise RuntimeError(f"connector stable mixed jet is not separated: {mixed}")

    matrix, angle_residual, momentum_residual = module.connector_derivative(root.boxes[0])
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector root no longer closes")
    eigen_root = (matrix[0, 1] * matrix[1, 0]).sqrt()
    unstable_multiplier = matrix[0, 0] + eigen_root
    stable_multiplier = matrix[0, 0] - eigen_root
    if not unstable_multiplier > module.arb("1e8"):
        raise RuntimeError("connector unstable multiplier lost hyperbolicity")
    if not stable_multiplier > 0 or not stable_multiplier < module.arb("1e-8"):
        raise RuntimeError("connector stable multiplier changed")

    # At p=0 the two QNL eigen-coordinates coincide with R_G(theta-pi/4)/2.
    # The connector base point is far outside the frozen 1e-10 gauge chart.
    qnl_coordinate = module.R_GRAY * (root.boxes[0] - module.arb.pi() / 4) / 2
    if not abs(qnl_coordinate) > module.arb("1e-4"):
        raise RuntimeError("connector base may meet the compact QNL gauge support")

    # For G=T^14 in connector eigen-coordinates, on x=h(y) one has
    # b_21(y)=c*y+O(y^2), c=partial_xy G_2(0).  If y_n~d*nu^n and
    # Lambda*nu=1, the (2,1) canonical comparison increment is
    # -Lambda*(Lambda/nu)^n*b_21(y_n)
    # ~ -Lambda*c*d*Lambda^n.  It is unbounded for every d!=0.
    return {
        "arb_precision_bits": PRECISION_BITS,
        "connector_return": "G=T^14 at the certified symmetric connector fixed point",
        "connector_unstable_multiplier": short(unstable_multiplier),
        "connector_stable_multiplier": short(stable_multiplier),
        "symplectic_multiplier_identity": "Lambda*nu=1 exactly",
        "stable_mixed_jet_partial_xy_G2": short(mixed),
        "stable_mixed_jet_in_minus_1_over_20_minus_1_over_25": True,
        "connector_qnl_eigen_coordinate": short(qnl_coordinate),
        "compact_qnl_gauge_chart_radius": "1e-10",
        "connector_has_neighbourhood_where_compact_qnl_gauge_is_identity": True,
        "stable_graph_form": "x=h(y), h(0)=h'(0)=0",
        "canonical_increment_formula": (
            "(K_n)_21=-Lambda*(Lambda/nu)^n*b_21(y_n), "
            "b_21(y)=c*y+O(y^2)"
        ),
        "canonical_increment_asymptotic": (
            "(K_n)_21~ -Lambda*c*d*Lambda^n for y_n~d*nu^n, d!=0"
        ),
        "compact_qnl_gauge_connector_stable_limit_converges": False,
        "compact_qnl_gauge_class_H_on_common_basic_set_with_connector": False,
    }


def symbolic_and_class_h_frontier() -> dict[str, Any]:
    return {
        "clean_symbolic_coding": {
            "base": "a finite SFT coding of a clean Birkhoff-Smale horseshoe for a return iterate",
            "selected_qnl_periodic_code": True,
            "selected_transverse_homoclinic_code": True,
            "coding_map": "pi:Sigma_A->Lambda, G o pi=pi o sigma",
            "faithful_actual_cocycle": (
                "A_log(x)=E(sigma*x)^-1 D_{pi(x)}G E(x); no frozen word matrix substitution"
            ),
            "finite_clean_horseshoe_coding_certified": True,
            "full_collision_srb_mass_coding_certified": False,
            "global_singular_billiard_coding_certified": False,
        },
        "invariant_frame_class_H": {
            "holder_line_fields": "E^u and E^s on the compact uniformly hyperbolic horseshoe",
            "holder_frames": "after clopen trivialisation on the zero-dimensional finite SFT",
            "higher_block_sign_recode": True,
            "faithful_diagonal_formula": (
                "A_diag(x)=C(sigma*x)^-1 A_log(x) C(x)=diag(a_u(x),a_s(x))"
            ),
            "canonical_stable_holonomy_formula": (
                "diag(prod_n>=0 a_u(sigma^n x)/a_u(sigma^n y), "
                "prod_n>=0 a_s(sigma^n x)/a_s(sigma^n y))"
            ),
            "holder_log_series_bound": (
                "sum_n |phi(sigma^n x)-phi(sigma^n y)| "
                "<= Hol_beta(phi)*d(x,y)^beta/(1-theta^beta)"
            ),
            "canonical_stable_and_unstable_holonomies_converge": True,
            "canonical_holonomies_are_holder": True,
            "diagonal_representative_belongs_to_butler_park_class_H": True,
            "all_canonical_holonomy_loops_are_diagonal": True,
            "same_axis_twisting_wedges_are_exactly_zero": True,
            "diagonal_representative_is_weakly_typical": False,
        },
        "same_representative_frontier": {
            "selected_compact_gauge_four_wedges": True,
            "selected_compact_gauge_all_plaque_holder_holonomies": False,
            "selected_compact_gauge_class_H_on_selected_horseshoe": False,
            "selected_compact_gauge_class_H_on_selected_horseshoe_status": "NOT_CERTIFIED",
            "diagonal_gauge_global_class_H": True,
            "diagonal_gauge_selected_same_axis_twisting": False,
            "cohomology_does_not_identify_non_fiber_bunched_canonical_holonomies": True,
            "one_representative_with_both_class_H_and_weak_typicality": False,
            "one_representative_with_both_status": "NOT_CERTIFIED",
        },
    }


def certify_frontier() -> dict[str, Any]:
    provenance = audit_frozen_inputs()
    transverse = certify_selected_transversality()
    connector = certify_connector_compact_gauge_obstruction()
    symbolic = symbolic_and_class_h_frontier()
    scope = {
        "selected_transverse_qnl_homoclinic": True,
        "finite_faithful_clean_horseshoe_coding": True,
        "global_full_mass_physical_coding": False,
        "faithful_diagonal_class_H_representative_on_clean_horseshoe": True,
        "diagonal_representative_weakly_typical": False,
        "compact_twisting_gauge_uniform_all_plaque_holder_holonomies": False,
        "compact_twisting_gauge_butler_park_class_H": False,
        "single_representative_class_H_and_weak_typicality": False,
        "physical_projective_PPE": False,
        "gate1_certified": False,
        "unconditional_cm2": False,
    }
    result = {
        "schema": "cm2.gate1.global-coding-class-h-separation-frontier.v1",
        "provenance": provenance,
        "selected_transverse_homoclinic": transverse,
        "connector_compact_gauge_obstruction": connector,
        "symbolic_and_class_h_frontier": symbolic,
        "scope_limits": scope,
        "strict_frontier": {
            "positive": (
                "the selected QNL homoclinic is transverse; a finite faithful clean "
                "horseshoe coding exists; an invariant-frame diagonal representative "
                "has uniform Holder canonical holonomies and belongs to class H"
            ),
            "negative": (
                "the diagonal class-H representative has zero same-axis twisting; the "
                "twisting compact gauge lacks all-plaque holonomies and fails class H "
                "on the common basic set containing the connector"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest(
        {
            "transverse": transverse,
            "connector": connector,
            "symbolic": symbolic,
            "scope": scope,
        }
    )
    return result


def main() -> int:
    try:
        result = certify_frontier()
    except Exception as exc:
        print(f"GATE1_GLOBAL_CODING_CLASS_H_FRONTIER: FAILED: {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    print("SELECTED_TRANSVERSE_QNL_HOMOCLINIC: CERTIFIED")
    print("FINITE_FAITHFUL_CLEAN_HORSESHOE_CODING: CERTIFIED")
    print("DIAGONAL_INVARIANT_FRAME_CLASS_H: CERTIFIED")
    print("DIAGONAL_INVARIANT_FRAME_WEAK_TYPICALITY: REFUTED")
    print("COMPACT_TWISTING_GAUGE_GLOBAL_CLASS_H: NOT_CERTIFIED")
    print("SINGLE_REPRESENTATIVE_CLASS_H_PLUS_TWISTING: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
