#!/usr/bin/env python3
"""Gate-1 immutable QNL homoclinic orbit and plaque-entry frontier.

This certificate does not modify any frozen predecessor.  It combines the
validated QNL unstable graph with the correlation-preserving Taylor replay
used by the frozen full-cross certificate.

On the exact local unstable graph ``y=h_u(x)`` we solve a reversible scalar
shooting problem.  The declared 48-collision half word is ``Q5^2 B^2``.
The endpoint momentum has opposite strict signs on the two faces of a tiny
``x`` interval, uniformly for the full certified graph-ordinate tube, and
its derivative along every admissible graph is strictly positive.  Hence
the actual invariant graph contains one and only one point whose half-word
endpoint belongs to ``Fix(I)={p=0}``.  Exact billiard reversibility then
gives

    T^96 z_h = I z_h,

so the point has QNL tails in both directions.  For ``F=T^2`` its local
unstable and stable plaque-entry times are respectively 0 and 48 returns.

The selected point makes the repaired homoclinic loop well typed.  The
frozen compact logarithmic-gauge certificate, however, contains qualitative
summability orders rather than numerical tail-majorant constants or a
matrix enclosure for either local holonomy.  Consequently this certificate
does not identify the loop with the 96-collision periodic-shadow matrix and
does not certify any twisting wedge or global class-H statement.

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

WORD_MANIFEST = (
    HERE / "cm2-gate1-word-gauge-homoclinic-loop-frontier-manifest-2026-07-16.json"
)
COMPACT_MANIFEST = (
    HERE / "cm2-gate1-compact-log-gauge-plaque-holonomy-frontier-manifest-2026-07-16.json"
)
FULL_CROSS_CERT = HERE / "cm2_gate1_full_cross_transport_cert.py"
TRUE_GRAPH_CERT = HERE / "cm2_gate1_true_graph_krawczyk_cert.py"
QNL_GRAPH_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
CONNECTOR_GRAPH_CERT = HERE / "cm2_gate1_connector_stable_graph_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
SHADOW_CERT = HERE / "cm2_gate1_closed_shadow_twisting_cert.py"

EXPECTED_HASHES = {
    WORD_MANIFEST.name: "84bfec08376ed49f0fb3432261c1100bf3e0d4e46e1760d960ceb3960963d1e8",
    COMPACT_MANIFEST.name: "fc2d7263d4cb659a82c7ecb0fad48f538b466f861f1295d78bb6738331b8c4cd",
    FULL_CROSS_CERT.name: "1eb603891c13e3615f74b5b25151dba3f8dab7933811c2ffeb85a3bf22283942",
    TRUE_GRAPH_CERT.name: "ea90579306b5fd3064cba500ac916cbc5ca8f21e89e8b7863fb711f8a547f4e7",
    QNL_GRAPH_CERT.name: "0945b084263e2f48d4cc8521e3e1f24986d28d057ec62de829a18471b8e46fa9",
    CONNECTOR_GRAPH_CERT.name: "7440b97ad97fc876dbc9d42c56cb9dc1d3239f3eb0d95c30e501f0115e73b77f",
    TANGENT_CERT.name: "d58a196da59b1f31191ad67239b079e669a5629aec1deaee925fa76d9c489ed1",
    SHADOW_CERT.name: "5ce6e38558bd1de56e17c8ef620fc27b6e73f7b04764d272823964c3b9334abc",
}

PRECISION_BITS = 1000

# Discovery used Newton iteration only to choose this rational decimal
# centre.  Acceptance below is the face-sign/monotonicity argument on the
# actual unknown invariant graph; the centre itself is never trusted as a
# root.
ROOT_X_CENTER = (
    "-8.293762194329601963437426816426218129136992992541213302685879950938746933679495882046154825340036010743174892558684126391544694649846885859088067348205641235289978138183961800037966087993611724941297924070080341715788907910727582613670011086480203974435489036750325333647236440100451527329092540147809133409697742230321803864868331258410153702375806605390149768919195276305867418145849332101778666361e-15"
)
ROOT_X_RADIUS = "1e-50"
GRAPH_ORDINATE_TUBE = "7e-29"
GRAPH_QUADRATIC = "1"
GRAPH_LIPSCHITZ = "1e-4"

# This pass freezes explicit nested QNL boxes for the compact logarithmic
# gauge.  The bump is one on the core disk and zero outside the chart disk.
GAUGE_CORE_RADIUS = "1e-12"
GAUGE_CHART_RADIUS = "1e-10"


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


def audit_frozen_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in EXPECTED_HASHES.items():
        path = HERE / name
        if sha256_path(path) != expected:
            raise RuntimeError(f"frozen dependency hash changed: {name}")

    word = json.loads(WORD_MANIFEST.read_text(encoding="utf-8"))
    compact = json.loads(COMPACT_MANIFEST.read_text(encoding="utf-8"))
    if word["schema"] != (
        "cm2.gate1.word-gauge-homoclinic-loop-frontier.manifest.v1"
    ):
        raise RuntimeError("word-gauge dependency schema changed")
    if compact["schema"] != (
        "cm2.gate1.compact-log-gauge-plaque-holonomy-frontier.manifest.v1"
    ):
        raise RuntimeError("compact-gauge dependency schema changed")
    if word["result"]["homoclinic_tail_extension"][
        "existential_qnl_homoclinic_holonomy_endomorphism"
    ] is not True:
        raise RuntimeError("frozen typed-tail result disappeared")
    if word["result"]["scope_limits"]["specific_typed_qnl_twisting_loop"]:
        raise RuntimeError("frozen word frontier unexpectedly claims twisting")
    compact_scope = compact["result"]["scope_limits"]
    if not compact_scope["stable_all_pairs_on_one_local_qnl_plaque"]:
        raise RuntimeError("frozen stable local plaque holonomies disappeared")
    if not compact_scope["unstable_all_pairs_on_one_local_qnl_plaque"]:
        raise RuntimeError("frozen unstable local plaque holonomies disappeared")
    if compact_scope["global_all_pairs_holder_holonomies"]:
        raise RuntimeError("frozen compact frontier unexpectedly claims global H")
    return word, compact


def replay_rectangle(
    full_cross,
    parent,
    qnl,
    connector,
    tangent,
    module,
    slope,
    word,
    parameter_center,
    parameter_radius,
    transverse_radius,
):
    return full_cross.replay_rectangle(
        parent,
        qnl,
        connector,
        tangent,
        module,
        parameter_center=parameter_center,
        parameter_radius=parameter_radius,
        transverse_radius=transverse_radius,
        base_angle=module.arb.pi() / 4,
        slope=slope,
        word=word,
    )


def certify_geometry() -> dict[str, Any]:
    full_cross = load(FULL_CROSS_CERT, "cm2_gate1_immutable_full_cross")
    parent = load(TRUE_GRAPH_CERT, "cm2_gate1_immutable_parent")
    qnl = load(QNL_GRAPH_CERT, "cm2_gate1_immutable_qnl")
    connector = load(CONNECTOR_GRAPH_CERT, "cm2_gate1_immutable_connector")
    tangent = load(TANGENT_CERT, "cm2_gate1_immutable_tangent")
    shadow = load(SHADOW_CERT, "cm2_gate1_immutable_shadow")

    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    shadow.refresh_exact_geometry(module)
    _, slope_qnl, _ = tangent.setup_fixed_data(module)

    # Replay the predecessor's actual invariant-graph theorem, including the
    # strict unstable projection expansion used to keep the backward QNL tail
    # inside the explicit core.  The stable statement follows by the frozen
    # billiard involution.
    graph_radius, graph_quadratic, graph_lipschitz = (
        qnl.certify_graph_transform(module)
    )

    if qnl.RADIUS != "2e-9":
        raise RuntimeError("QNL invariant-graph radius changed")
    if qnl.QUADRATIC_CONSTANT != GRAPH_QUADRATIC:
        raise RuntimeError("QNL graph quadratic bound changed")
    if qnl.LIPSCHITZ_CONSTANT != GRAPH_LIPSCHITZ:
        raise RuntimeError("QNL graph Lipschitz bound changed")
    if graph_radius != module.arb(qnl.RADIUS):
        raise RuntimeError("replayed QNL graph radius changed")
    if graph_quadratic != module.arb(GRAPH_QUADRATIC):
        raise RuntimeError("replayed QNL graph quadratic bound changed")
    if graph_lipschitz != module.arb(GRAPH_LIPSCHITZ):
        raise RuntimeError("replayed QNL graph Lipschitz bound changed")

    q5_word = tuple(tangent.QNL_FORWARD_WORD)
    b_word = tuple(tangent.CONNECTOR_REVERSE_FORWARD_WORD)
    half_word = q5_word * 2 + b_word * 2
    reflected_half_word = b_word * 2 + q5_word * 2
    full_word = half_word + reflected_half_word
    if len(q5_word) != 10 or len(b_word) != 14:
        raise RuntimeError("frozen block collision counts changed")
    if len(half_word) != 48 or len(full_word) != 96:
        raise RuntimeError("homoclinic word collision count changed")
    if full_word != q5_word * 2 + b_word * 4 + q5_word * 2:
        raise RuntimeError("reflected full word factorisation changed")
    if module.FULL_KEYS[1:] != tuple(reversed(module.FULL_KEYS[1:])):
        raise RuntimeError("connector block lost the frozen reversibility audit")

    center = module.arb(ROOT_X_CENTER)
    radius = module.arb(ROOT_X_RADIUS)
    transverse = module.arb(GRAPH_ORDINATE_TUBE)
    graph_bound = module.arb(GRAPH_QUADRATIC) * (abs(center) + radius) ** 2
    if not graph_bound < transverse:
        raise RuntimeError("declared graph-ordinate tube does not cover h_u(x)")
    if not abs(center) + radius < module.arb(qnl.RADIUS):
        raise RuntimeError("root interval leaves the invariant-graph domain")

    zero = module.arb(0)
    left = replay_rectangle(
        full_cross,
        parent,
        qnl,
        connector,
        tangent,
        module,
        slope_qnl,
        half_word,
        center - radius,
        zero,
        transverse,
    )
    right = replay_rectangle(
        full_cross,
        parent,
        qnl,
        connector,
        tangent,
        module,
        slope_qnl,
        half_word,
        center + radius,
        zero,
        transverse,
    )
    whole = replay_rectangle(
        full_cross,
        parent,
        qnl,
        connector,
        tangent,
        module,
        slope_qnl,
        half_word,
        center,
        radius,
        transverse,
    )

    left_momentum = left.value_box(module)[1]
    right_momentum = right.value_box(module)[1]
    if not left_momentum < -module.arb("1e-23"):
        raise RuntimeError(f"left shooting face is not negative: {left_momentum}")
    if not right_momentum > module.arb("1e-23"):
        raise RuntimeError(f"right shooting face is not positive: {right_momentum}")

    derivative = whole.derivative_box(module)[1]
    graph_slope = module.arb(GRAPH_LIPSCHITZ)
    derivative_along_graph = derivative[0] - abs(derivative[1]) * graph_slope
    if not derivative[0] > module.arb("2e27"):
        raise RuntimeError(f"shooting x derivative is too small: {derivative[0]}")
    if not abs(derivative[1]) < module.arb(100):
        raise RuntimeError(f"shooting transverse derivative is too large: {derivative[1]}")
    if not derivative_along_graph > module.arb("1e27"):
        raise RuntimeError(
            f"shooting derivative along every admissible graph may vanish: "
            f"{derivative_along_graph}"
        )

    thresholds = {
        "flight": module.arb(18) / 100,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(63) / 100,
        "clearance": module.arb(22) / 100,
    }
    for name, threshold in thresholds.items():
        if not whole.minima[name] > threshold:
            raise RuntimeError(
                f"homoclinic half-word physical margin {name} fails: "
                f"{whole.minima[name]}"
            )
    module.certify_lattice_exhaustion(module.arb(1) / 5)
    if whole.cumulative_lifts[-1] != (0, 0):
        raise RuntimeError("homoclinic half word changes the terminal lift")

    # Freeze a genuinely numerical compact-gauge chart.  The complete square
    # containing the chart disk stays on the same regular QNL return branch.
    chart_radius = module.arb(GAUGE_CHART_RADIUS)
    core_radius = module.arb(GAUGE_CORE_RADIUS)
    chart = qnl.qnl_return(
        module,
        module.arb(0, GAUGE_CHART_RADIUS),
        module.arb(0, GAUGE_CHART_RADIUS),
    )
    chart_thresholds = {
        "flight": (chart.minimum_flight, module.arb(18) / 100),
        "discriminant": (chart.minimum_discriminant, module.arb(2) / 100),
        "incidence": (chart.minimum_incidence, module.arb(99) / 100),
        "clearance": (chart.minimum_clearance, module.arb(3) / 10),
    }
    for name, (value, threshold) in chart_thresholds.items():
        if not value > threshold:
            raise RuntimeError(f"explicit gauge chart margin {name} fails: {value}")
    if not core_radius < chart_radius:
        raise RuntimeError("gauge core is not compactly inside the chart")
    if not abs(center) + radius + transverse < core_radius:
        raise RuntimeError("selected unstable/stable endpoints leave gauge core")

    return {
        "arb_precision_bits": PRECISION_BITS,
        "root_x_center": ROOT_X_CENTER,
        "root_x_radius": ROOT_X_RADIUS,
        "root_interval_excludes_qnl_point": True,
        "actual_graph_ordinate_bound": "|h_u(x)|<7e-29 on the root interval",
        "actual_graph_derivative_bound": "|h_u'(x)|<=1e-4",
        "half_word_left_face_momentum": "strictly less than -1e-23",
        "half_word_right_face_momentum": "strictly greater than 1e-23",
        "shooting_derivative_along_actual_graph": "strictly greater than 1e27",
        "unique_actual_graph_root": True,
        "q5_block_collision_keys": [list(item) for item in q5_word],
        "connector_block_collision_keys": [list(item) for item in b_word],
        "half_word_factorisation": "Q5^2 B^2",
        "full_word_factorisation": "Q5^2 B^4 Q5^2",
        "half_word_collision_count": 48,
        "full_word_collision_count": 96,
        "half_word_sha256": digest([list(item) for item in half_word]),
        "full_word_sha256": digest([list(item) for item in full_word]),
        "half_word_terminal_lift": [0, 0],
        "half_lift_ledger_sha256": digest(
            [list(item) for item in whole.cumulative_lifts]
        ),
        "half_word_uniform_physical_margins": {
            "flight": ">18/100",
            "discriminant": ">1/100",
            "incidence": ">63/100",
            "clearance": ">22/100",
        },
        "reversibility_fixed_line": "Fix(I)={p=0}",
        "exact_reflection_identity": "T^96 z_h=I z_h",
        "phase_aligned_return": "F=T^2",
        "F_unstable_plaque_entry_time": 0,
        "F_stable_plaque_entry_time": 48,
        "bi_infinite_itinerary": "... QNL | Q5^2 B^4 Q5^2 | QNL ...",
        "selected_point_definition": (
            "z_h=(x_h,h_u(x_h)), where x_h is the unique root in the frozen "
            "x interval of momentum(T^48(x,h_u(x)))=0"
        ),
        "selected_point_is_regular": True,
        "selected_point_is_nonperiodic_qnl_homoclinic": True,
        "explicit_gauge_core_radius": GAUGE_CORE_RADIUS,
        "explicit_gauge_chart_radius": GAUGE_CHART_RADIUS,
        "explicit_gauge_cutoff": (
            "chi(x,y)=sigma(((x^2+y^2)-r_core^2)/(r_chart^2-r_core^2)); "
            "sigma(t)=beta(1-t)/(beta(1-t)+beta(t)), beta(t)=0 for t<=0 "
            "and exp(-1/t) for t>0"
        ),
        "gauge_is_one_on_selected_local_tails": True,
        "gauge_is_zero_outside_chart_disk": True,
        "gauge_chart_qnl_return_is_regular": True,
    }


def typed_loop_frontier() -> dict[str, Any]:
    return {
        "selected_loop_fiber": "E_p",
        "selected_homoclinic_endomorphism": (
            "psi_z=H_hat^s_{z_h,p} o H_hat^u_{p,z_h}:E_p->E_p"
        ),
        "finite_entry_formula": (
            "psi_z=A_hat^48(p)^-1 H_hat^s_{I z_h,p} "
            "A_hat^48(z_h) H_hat^u_{p,z_h}:E_p->E_p"
        ),
        "formula_is_well_typed": True,
        "local_unstable_holonomy_exists": True,
        "local_stable_holonomy_exists": True,
        "selected_immutable_qnl_homoclinic_loop": "CERTIFIED_AS_A_TYPED_LIMIT",
        "numeric_matrix_enclosure_for_Hu": False,
        "numeric_matrix_enclosure_for_Hs": False,
        "numeric_matrix_enclosure_for_psi_z": False,
        "frozen_tail_data_are_qualitative": (
            "the source records O(n*mu^n), O(n*mu^(2n)), O(mu^(4n)) "
            "without numerical majorant constants or a truncation error"
        ),
        "periodic_shadow_matrix_fiber": "E_{z_*}",
        "gauge_covariant_transport_J_from_shadow_to_p": False,
        "psi_z_vs_J_L_J_inverse_error_bound": False,
        "raw_common_chart_finite_excursion_equals_psi_z": False,
        "four_qnl_fiber_twisting_wedges": False,
        "global_uniform_holder_holonomies": False,
        "butler_park_class_H": False,
        "first_missing_numeric_interface": (
            "EXPLICIT_LOCAL_HOLONOMY_TAIL_MAJORANTS_AND_MATRIX_ENCLOSURES"
        ),
    }


def certify() -> dict[str, Any]:
    word, compact = audit_frozen_inputs()
    geometry = certify_geometry()
    loop = typed_loop_frontier()
    result = {
        "schema": "cm2.gate1.immutable-homoclinic-plaque-entry-frontier.v1",
        "provenance": {
            "dependencies": EXPECTED_HASHES,
            "word_frontier_internal_digest": word["result"]["internal_digest"],
            "compact_frontier_internal_digest": compact["result"][
                "internal_digest"
            ],
        },
        "immutable_homoclinic_orbit": geometry,
        "typed_loop_and_numeric_frontier": loop,
        "scope_limits": {
            "selected_immutable_regular_phase_aligned_qnl_homoclinic_orbit": True,
            "physical_plaque_entry_times_certified": True,
            "selected_typed_qnl_homoclinic_limit_loop": True,
            "direct_numeric_psi_z": False,
            "shadow_transport_and_error_bound": False,
            "four_twisting_wedges": False,
            "global_faithful_coding": False,
            "uniform_all_plaque_holder_holonomies": False,
            "butler_park_class_H": False,
            "gate1_certified": False,
            "unconditional_cm2": False,
        },
        "strict_frontier": {
            "positive": (
                "one unique immutable physical QNL homoclinic itinerary with "
                "explicit F-plaque entry times 0 and 48, plus a selected typed "
                "homoclinic holonomy-limit endomorphism"
            ),
            "negative": (
                "no numerical local-holonomy matrices, no typed comparison with "
                "the periodic shadow, no twisting wedges, and no global class H"
            ),
            "gate1": "NOT_CERTIFIED",
        },
    }
    result["internal_digest"] = digest(
        {
            "orbit": geometry,
            "loop": loop,
            "scope": result["scope_limits"],
        }
    )
    return result


def main() -> int:
    try:
        result = certify()
    except Exception as exc:
        print(f"GATE1_IMMUTABLE_HOMOCLINIC_PLAQUE_ENTRY: FAILED: {exc}")
        print("SELECTED_IMMUTABLE_QNL_HOMOCLINIC_ORBIT: NOT_CERTIFIED")
        print("SELECTED_TYPED_QNL_HOMOCLINIC_LOOP: NOT_CERTIFIED")
        print("GATE1: NOT_CERTIFIED")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    print("SELECTED_IMMUTABLE_QNL_HOMOCLINIC_ORBIT: CERTIFIED")
    print("PHYSICAL_F_PLAQUE_ENTRY_TIMES_0_AND_48: CERTIFIED")
    print("SELECTED_TYPED_QNL_HOMOCLINIC_LIMIT_LOOP: CERTIFIED")
    print("NUMERIC_PSI_Z_AND_FOUR_TWISTING_WEDGES: NOT_CERTIFIED")
    print("BUTLER_PARK_CLASS_H: NOT_CERTIFIED")
    print("GATE1: NOT_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
