#!/usr/bin/env python3
"""Append-only correction and impact audit for the Round101 endpoint closure.

Round101 accidentally used the left endpoint of each Round94
``first_physical_terminal_event_parameter_bracket`` as the end of the
adjacent-chart continuation.  That endpoint is the chart-transfer seam, so
all 8 * 65 advertised adjacent-chart intervals collapse to a point.  This
certificate reconstructs the frozen computation, then replaces the collapsed
partition by the actual adjacent pre-root interval
``[seam_outer,grazing_inner]`` from Round94.

The last base interval on each ray approaches only ``grazing_inner``, the
lower endpoint of a separate tight algebraic grazing-root bracket.  We
certify a fixed dyadic prefix toward that lower endpoint; this is not a
root-centred exhaustion and says nothing by itself about source cosine at the
unknown root.  No positive-width (eta,c3) collar or Gate5 field is claimed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round91_rank3_exterior_source_exit_cert as round91
import cm2_round93_rank3_full_source_chart_exit_cert as round93
import cm2_round94_rank3_adjacent_chart_transfer_cert as round94
import cm2_round95_rank3_centered_reverse_interval_cert as round95
import cm2_round96_rank3_correlated_owner_interval_cert as round96
from cm2_round79_tangency_intersection_generator import aq, strict_sign


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round111.rank3-round101-zero-width-correction-impact-audit.v1"
PRECISION_BITS = 512
ENDPOINT_RING_PREFIX = 32

FILES = {
    "r87": "cm2-round87-rank3-port-event-continuation-2026-07-22.json",
    "r94": "cm2-round94-rank3-adjacent-chart-transfer-2026-07-22.json",
    "r99": "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json",
    "r100": "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json",
    "r101": "cm2-round101-rank3-eight-ray-source-grazing-closure-2026-07-22.json",
    "r102": "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json",
    "r103": "cm2-round103-rank3-rn-f1-f2-binding-2026-07-22.json",
    "r104": "cm2-round104-rank3-rn-f3-prefix-chart-2026-07-22.json",
    "r105": "cm2-round105-rank3-rn-f4-suffix-chart-2026-07-22.json",
    "r106": "cm2-round106-rank3-f5-adjacent-cell-scope-audit-2026-07-22.json",
    "r107": "cm2-round107-rank3-adjacent-smooth-cell-atlas-2026-07-22.json",
    "r108": "cm2-round108-rank3-official-word-crosswalk-2026-07-22.json",
    "r109": "cm2-round109-rank3-registered-arc-immutable-whole-tube-reaudit-2026-07-22.json",
    "r110": "cm2-round110-rank3-gap-tube-side-decomposition-2026-07-22.json",
}
PINS = {
    "cm2_gate25_physical_return_core_registry_cert.py": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate3_candidate_first_hit_cert.py": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate34_round26_q1_time2_frontier_cert.py": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "cm2_round79_tangency_intersection_generator.py": "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    FILES["r87"]: "f63f5d627def35f87dd3dfac075f8ecc0e8a5adfa725ddbe0eb692a39b54393b",
    FILES["r94"]: "915f7c18d896d92116ab3f4346a5853c09fef2d3226a1f5429a7c19bca948ee3",
    FILES["r99"]: "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    FILES["r100"]: "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
    FILES["r101"]: "df29ea8467c09351276a40b38424d6c9effc763f287815e7bac67829bca58172",
    FILES["r102"]: "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    FILES["r103"]: "76ac1099805e5fb3d9eac9984a078ed52f1f6ec706a5a12ec880de28a262c8e8",
    FILES["r104"]: "d6d47ac6b7cb03f70d483536a31ca031718f9aa96bd8adfce072866870bb9c5d",
    FILES["r105"]: "ef747bcd760bf8fe0a8bd8ac3bc65f9df4cf381898ffe98afcdb823f19c44b28",
    FILES["r106"]: "d3fbf85017f173e609a34b8b202d09d1fb0e5a664b922951c1c0730836d8f57e",
    FILES["r107"]: "bb6aeaa821174a1e1994eff2eb10046811b66dd7cf41c4e2d1c898b74d9dea74",
    FILES["r108"]: "96bf22d97f517d53cb360c4aae64a2d5a5a0bbfb7125610dc69b519629bd78ea",
    FILES["r109"]: "fa5231f91f71da8014f9ca606702e3a59499adf78ce86ce09954bb424dae540e",
    FILES["r110"]: "2b49f900e05a29fc65897b8ebf350882a310fa95ebcd0031f94214f87ded38a2",
    "cm2_round91_rank3_exterior_source_exit_cert.py": "d75eb3a9a6aeca2c45b5b9eaa487c32481d4a9cf7e3da04c5d45d6f9a79414da",
    "cm2_round93_rank3_full_source_chart_exit_cert.py": "cec3bc83ae2a9df015441ce72397c2d553a74baf2cab89946a220ee4debb1023",
    "cm2_round94_rank3_adjacent_chart_transfer_cert.py": "ecc5fae4bf35bb33408f10b8357b546d487be57329e2a798fc1ace95a3c0a24b",
    "cm2_round95_rank3_centered_reverse_interval_cert.py": "c7921f2e999df9f1fb9ac935f28093e830d036116dafaf18dc2b2090c5e7702b",
    "cm2_round96_rank3_correlated_owner_interval_cert.py": "5c0205e4756270d8f94ede4947c2b80f82ad655b37d81a6bc02aa8bade54c702",
    "cm2_round101_rank3_eight_ray_source_grazing_closure.py": "2e42513fdc6674200a3a6b29f7fa4182c938bf9b8e30facf43085a790f1b8a1f",
}
SCHEMAS = {
    "r87": "cm2.round87.rank3-port-event-continuation.v1",
    "r94": "cm2.round94.rank3-adjacent-chart-transfer.v1",
    "r99": "cm2.round99.rank3-registered-port-candidate-audit.v1",
    "r100": "cm2.round100.rank3-immutable-interior-gap-closure.v1",
    "r101": "cm2.round101.rank3-eight-ray-source-grazing-closure.v1",
    "r102": "cm2.round102.rank3-corrected-face-quotient.v1",
    "r103": "cm2.round103.rank3-rn-f1-f2-binding.v1",
    "r104": "cm2.round104.rank3-rn-f3-prefix-chart.v1",
    "r105": "cm2.round105.rank3-rn-f4-suffix-chart.v1",
    "r106": "cm2.round106.rank3-f5-adjacent-cell-scope-audit.v1",
    "r107": "cm2.round107.rank3-adjacent-smooth-cell-atlas.v1",
    "r108": "cm2.round108.rank3-official-word-crosswalk.v1",
    "r109": "cm2.round109.rank3-registered-arc-immutable-whole-tube-reaudit.v1",
    "r110": "cm2.round110.rank3-gap-tube-side-decomposition.v1",
}


def digest(value: Any) -> str:
    text = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(text.encode()).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(token: str) -> Any:
    raise ValueError(f"nonfinite JSON number: {token}")


def load_documents() -> dict[str, dict[str, Any]]:
    for name, expected in PINS.items():
        if sha256(HERE / name) != expected:
            raise RuntimeError(f"pin mismatch: {name}")
    documents: dict[str, dict[str, Any]] = {}
    for alias, name in FILES.items():
        value = json.loads(
            (HERE / name).read_text(encoding="utf-8"),
            object_pairs_hook=strict_pairs,
            parse_constant=reject_nonfinite,
        )
        if set(value) != {"schema", "result", "result_sha256"}:
            raise RuntimeError(f"open document schema: {name}")
        if value["schema"] != SCHEMAS[alias] or value["result_sha256"] != digest(value["result"]):
            raise RuntimeError(f"closed document mismatch: {name}")
        documents[alias] = value["result"]
    return documents


def certify_same_chart(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> dict[str, Any]:
    path, chart1, chart2, first_digest, second_digest, third_digest = round96.certify(
        source, branch, qa, qb
    )
    return {
        "reverse_path": list(path),
        "first_outgoing_chart": chart1,
        "second_outgoing_chart": chart2,
        "complete_first_competitor_rows_sha256": first_digest,
        "complete_second_competitor_rows_sha256": second_digest,
        "complete_third_competitor_rows_sha256": third_digest,
    }


def clear_before(point: Any, velocity: Any, target: str, terminal: Any) -> str:
    delta = round95.sub(round95.center(target), point)
    ell = round95.dot(velocity, delta)
    transverse = round95.cross(velocity, delta)
    radius = round95.radius(target)
    line_clear = transverse * transverse - radius * radius
    end_clear = (ell - terminal) * (ell - terminal) + transverse * transverse - radius * radius
    if strict_sign(line_clear.value) == 1:
        return "WHOLE_LINE_MISS"
    if bool(ell.value < 0):
        return "CLOSEST_BEHIND_START"
    if bool(ell.value > terminal.value) and strict_sign(end_clear.value) == 1:
        return "CLOSEST_AFTER_TERMINAL__END_CLEAR"
    raise RuntimeError(f"union-chart competitor unresolved: {target}")


def centered_state_with_source_normal(
    source: Any, branch: tuple[Any, ...], qa: Q, qb: Q,
) -> tuple[tuple[int, int, int], dict[str, Any]]:
    lo, hi = min(qa, qb), max(qa, qb)
    middle, radius = (lo + hi) / 2, (hi - lo) / 2
    path = round95.discover_path(source, branch, middle)
    q_value = round95.Centered.variable(
        aq(middle), round91.qball(lo, hi), arb(0, aq(radius).upper())
    )
    normal, direction, offset = round95.tangent(branch, q_value)
    hit2, normal2 = round95.line_hit(normal, direction, offset, branch[1], path[0])
    incoming2 = round95.reflect(direction, normal2)
    hit1, normal1, flight1 = round95.ray_hit(
        hit2, round95.scale(-1, incoming2), source.target_id, path[1]
    )
    initial = round95.reflect(incoming2, normal1)
    hit0, normal0, flight0 = round95.ray_hit(
        hit1, round95.scale(-1, initial), f"{source.source}[0,0]", path[2]
    )
    contact = round95.sub(
        round95.center(branch[2]),
        round95.scale(branch[3] * round95.radius(branch[2]), normal),
    )
    tangent_flight = round95.dot(direction, round95.sub(contact, hit2))
    state = {
        "hit0": hit0, "normal0": normal0, "initial": initial, "flight0": flight0,
        "hit1": hit1, "normal1": normal1, "outgoing1": incoming2, "flight1": flight1,
        "hit2": hit2, "normal2": normal2, "outgoing2": direction,
        "tangent_flight": tangent_flight,
    }
    for terminal in (flight0, flight1, tangent_flight):
        if not bool(terminal.value > 0) or not bool(terminal.value < aq(Q(3))):
            raise RuntimeError("selected flight is not strict")
    return path, state


def source_normal_chart(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> str:
    _path, state = centered_state_with_source_normal(source, branch, qa, qb)
    return round96.chart(state["normal0"])


def certify_source_normal_union_chart(
    source: Any, branch: tuple[Any, ...], qa: Q, qb: Q,
) -> dict[str, Any]:
    """Replay a source-normal seam against all four first-hit tables."""
    path, state = centered_state_with_source_normal(source, branch, qa, qb)
    first_ids: set[str] = set()
    for chart in ("E", "W", "N", "S"):
        first_ids.update(first_hit.candidate_ids(f"{source.source}:{chart}"))
    first_rows = [
        (target, clear_before(state["hit0"], state["initial"], target, state["flight0"]))
        for target in sorted(first_ids - {source.target_id, f"{source.source}[0,0]"})
    ]
    chart1 = round96.chart(state["normal1"])
    second_rows = []
    for target in time2.translated_candidate_ids(source.target_id, chart1):
        if target not in {branch[1], source.target_id}:
            second_rows.append((target, clear_before(state["hit1"], state["outgoing1"], target, state["flight1"])))
    chart2 = round96.chart(state["normal2"])
    third_rows = []
    for target in time2.translated_candidate_ids(branch[1], chart2):
        if target not in {branch[2], branch[1]}:
            third_rows.append((target, clear_before(state["hit2"], state["outgoing2"], target, state["tangent_flight"])))
    if len(first_rows) != 75:
        raise RuntimeError(f"source-normal four-chart union census changed: {len(first_rows)}")
    return {
        "reverse_path": list(path),
        "source_representation_seam_policy": "UNION_OF_E_W_N_S_FIRST_HIT_CANDIDATE_TABLES",
        "first_candidate_union_size": len(first_ids),
        "first_candidate_row_count": len(first_rows),
        "first_outgoing_chart": chart1,
        "second_outgoing_chart": chart2,
        "complete_first_union_competitor_rows_sha256": digest(first_rows),
        "complete_second_competitor_rows_sha256": digest(second_rows),
        "complete_third_competitor_rows_sha256": digest(third_rows),
    }


def certify_union_chart(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q) -> dict[str, Any]:
    """Replay a representation seam against the union of all four tables."""
    lo, hi = min(qa, qb), max(qa, qb)
    middle, radius = (lo + hi) / 2, (hi - lo) / 2
    path = round95.discover_path(source, branch, middle)
    q_value = round95.Centered.variable(
        aq(middle), round91.qball(lo, hi), arb(0, aq(radius).upper())
    )
    state = round96.state(source, branch, q_value, path)
    for terminal in (state["flight0"], state["flight1"], state["tangent_flight"]):
        if not bool(terminal.value > 0) or not bool(terminal.value < aq(Q(3))):
            raise RuntimeError("selected flight is not strict")

    first_rows = []
    for target in first_hit.candidate_ids(source.chart_id):
        if target not in {source.target_id, f"{source.source}[0,0]"}:
            first_rows.append((target, clear_before(state["hit0"], state["initial"], target, state["flight0"])))

    second_ids: set[str] = set()
    third_ids: set[str] = set()
    for chart in ("E", "W", "N", "S"):
        second_ids.update(time2.translated_candidate_ids(source.target_id, chart))
        third_ids.update(time2.translated_candidate_ids(branch[1], chart))
    second_rows = [
        (target, clear_before(state["hit1"], state["outgoing1"], target, state["flight1"]))
        for target in sorted(second_ids - {branch[1], source.target_id})
    ]
    third_rows = [
        (target, clear_before(state["hit2"], state["outgoing2"], target, state["tangent_flight"]))
        for target in sorted(third_ids - {branch[2], branch[1]})
    ]
    first_rows.sort()
    return {
        "reverse_path": list(path),
        "representation_seam_policy": "UNION_OF_E_W_N_S_IMMUTABLE_CANDIDATE_TABLES",
        "first_candidate_row_count": len(first_rows),
        "second_candidate_union_size": len(second_ids),
        "third_candidate_union_size": len(third_ids),
        "complete_first_competitor_rows_sha256": digest(first_rows),
        "complete_second_union_competitor_rows_sha256": digest(second_rows),
        "complete_third_union_competitor_rows_sha256": digest(third_rows),
    }


def frozen_segment(source: Any, branch: tuple[Any, ...], qa: Q, qb: Q, layer: str) -> dict[str, Any]:
    row = {
        "q_interval": [str(qa), str(qb)],
        "source_chart": source.chart_id,
        **certify_same_chart(source, branch, qa, qb),
        "layer": layer,
    }
    return row


def corrected_segment(
    source: Any, branch: tuple[Any, ...], q0: Q, direction: int,
    index: int, lower: Q, upper: Q,
) -> dict[str, Any]:
    qa, qb = q0 + direction * lower, q0 + direction * upper
    try:
        chart0 = source_normal_chart(source, branch, qa, qb)
    except RuntimeError as exc:
        if str(exc) != "correlated chart seam":
            raise
        evidence = certify_source_normal_union_chart(source, branch, qa, qb)
        mode = "SOURCE_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY"
    else:
        if chart0 != source.chart_id.split(":")[1]:
            raise RuntimeError("strict source normal does not lie in the selected adjacent chart")
        try:
            evidence = certify_same_chart(source, branch, qa, qb)
            mode = "SAME_CHART_CORRELATED_REPLAY"
        except RuntimeError as exc:
            if str(exc) != "correlated chart seam":
                raise
            evidence = certify_union_chart(source, branch, qa, qb)
            mode = "OUTGOING_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY"
    return {
        "segment_index": index,
        "parameter_interval": [str(lower), str(upper)],
        "q_interval": [str(qa), str(qb)],
        "strictly_positive_parameter_width": lower < upper,
        "replay_mode": mode,
        "evidence": evidence,
    }


def corrected_source_segment(
    source: Any, branch: tuple[Any, ...], q0: Q, direction: int,
    index: int, lower: Q, upper: Q,
) -> dict[str, Any]:
    """Repair the frozen source-table claim when the centered normal is a seam."""
    qa, qb = q0 + direction * lower, q0 + direction * upper
    try:
        chart0 = source_normal_chart(source, branch, qa, qb)
    except RuntimeError as exc:
        if str(exc) != "correlated chart seam":
            raise
        evidence = certify_source_normal_union_chart(source, branch, qa, qb)
        mode = "SOURCE_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY"
    else:
        if chart0 != source.chart_id.split(":")[1]:
            raise RuntimeError("strict source normal does not lie in the selected old chart")
        evidence = certify_same_chart(source, branch, qa, qb)
        mode = "SAME_CHART_CORRELATED_REPLAY"
    return {
        "segment_index": index,
        "parameter_interval": [str(lower), str(upper)],
        "q_interval": [str(qa), str(qb)],
        "source_chart": source.chart_id,
        "strictly_positive_parameter_width": lower < upper,
        "replay_mode": mode,
        "evidence": evidence,
    }


def impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "round": 101,
            "status": "CORRECTED__ADJACENT_WHOLE_INTERVAL_CLOSURE_WITHDRAWN",
            "preserved": "8 source-core exit chains plus 1,024 old-chart same-table segments and 8 newly recovered source-normal four-chart-union evidence rows",
            "affected": "the frozen same-table completeness claim fails on 8 source-chart terminal segments; all advertised 520 adjacent-chart rows are zero-width seam repetitions; remaining_open_exterior_ray_count=0 is not established",
        },
        {
            "round": 102,
            "status": "PARTIAL_COMBINATORIAL_FACE_LEDGER",
            "preserved": "12 face IDs, 120 registered ports, 108 internal links, and source-grazing event-type/candidate incidence",
            "affected": "the 8 broad terminal brackets, their endpoint IDs, endpoint completeness, whole-domain physical completeness, and zero-residual claims for the cap-to-grazing faces",
        },
        {
            "round": 103,
            "status": "FACE_LOCAL_METADATA_ONLY__ACTUAL_CHILD_F1_F2_WITHDRAWN",
            "preserved": "face/ID bookkeeping mechanisms and nonempty local registered-port evidence",
            "affected": "tangent faces are not homogeneous operator children and their three-owner tuple is not an official word; actual-child F1/F2 must be rebuilt",
        },
        {
            "round": 104,
            "status": "FACE_LOCAL_PREFIX_METADATA_ONLY__ACTUAL_CHILD_F3_WITHDRAWN",
            "preserved": "source-core collision chart metadata",
            "affected": "no official actual-child F3 slot survives without a homogeneous child and official word path",
        },
        {
            "round": 105,
            "status": "ALGEBRAIC_DIRECTION_METADATA_ONLY__ACTUAL_CHILD_F4_WITHDRAWN",
            "preserved": "strict q-direction component signs on the formal intervals",
            "affected": "no official actual-child F4 slot survives without a certified homogeneous child domain and official path",
        },
        {
            "round": 106,
            "status": "CONSERVATIVE_NO_GO_PRESERVED",
            "preserved": "no F5/F6 promotion and the requirement for side cells/collars",
            "affected": "none in the nonpromotion conclusion",
        },
        {
            "round": 107,
            "status": "LOCAL_WITNESS_ATLAS_PRESERVED__GLOBAL_EXTENSION_UNAVAILABLE",
            "preserved": "24 positive-area rational witness boxes and their immutable local candidate replays",
            "affected": "extension of the 16 germs incident to grazing-ended faces through the missing endpoint tails",
        },
        {
            "round": 108,
            "status": "LOCAL_FIXED_BOX_WORD_CROSSWALK_PRESERVED",
            "preserved": "24 local paths and 72 official legs on the Round107 boxes",
            "affected": "no whole-face or endpoint-collar word constancy may be inferred",
        },
        {
            "round": 109,
            "status": "REGISTERED_ARC_WHOLE_TUBE_REAUDIT_PRESERVED",
            "preserved": "52 internal registered arcs and 41,984 immutable-table strips",
            "affected": "none of its internal tube computations; it remains insufficient for exterior collars",
        },
        {
            "round": 110,
            "status": "INTERNAL_GAP_SIDE_LEDGER_PRESERVED__GLOBAL_FACE_EMBEDDING_QUALIFIED",
            "preserved": "56 gap pairs, 112 strict-D side ownership rows, and nonpromotion flags",
            "affected": "use of the ledger as part of an endpoint-complete 12-face physical quotient",
        },
    ]


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    if precision_bits < 384:
        raise RuntimeError("insufficient precision")
    ctx.prec = precision_bits
    documents = load_documents()
    r87 = documents["r87"]
    r94 = documents["r94"]
    r99 = documents["r99"]
    r101 = documents["r101"]
    by_port = {row["registered_port_id"]: row for row in r87["port_event_rows"]}
    physical = {
        port_id: by_port[port_id]
        for port_id in r99["corrected_locally_physical_registered_port_ids"]
    }
    transfers = {row["exterior_port_id"]: row for row in r94["transfer_rows"]}
    cores = core_cert.physical_cores()
    round91.round87.WORK_CORES = cores

    if len(r101["ray_rows"]) != 8 or len(transfers) != 28:
        raise RuntimeError("upstream ray census changed")
    rows = []
    all_source_corrections: list[dict[str, Any]] = []
    all_nonterminal: list[dict[str, Any]] = []
    all_rings: list[dict[str, Any]] = []
    source_mode_histogram: Counter[str] = Counter()
    mode_histogram: Counter[str] = Counter()

    for frozen in sorted(r101["ray_rows"], key=lambda row: row["ray_index"]):
        ray_index = frozen["ray_index"]
        port_id = frozen["exterior_port_id"]
        branch = tuple(frozen["branch_key"])
        side = frozen["projective_end"]
        transfer = transfers[port_id]
        if transfer["first_physical_terminal_event_type"] != "SOURCE_GRAZING":
            raise RuntimeError("Round101 ray is not a source-grazing transfer")
        q0, direction, cell_edge, inner, seam_outer, event_kind, _, _ = round93.isolate_event(
            branch, side, port_id, physical, cores
        )
        if event_kind != "SOURCE_CHART_SEAM":
            raise RuntimeError("Round101 ray lacks its advertised chart seam")
        source = cores[branch[0]]
        source_bounds = [
            cell_edge + (inner - cell_edge) * Q(index, round93.PROBE_COUNT + 1)
            for index in range(round93.PROBE_COUNT + 2)
        ]
        frozen_source_rows = [
            frozen_segment(source, branch, q0 + direction * left, q0 + direction * right, "SOURCE_CHART")
            for left, right in zip(source_bounds, source_bounds[1:])
        ]
        source_correction_rows = []
        for index, (left, right) in enumerate(zip(source_bounds, source_bounds[1:])):
            corrected = corrected_source_segment(
                source, branch, q0, direction, index, left, right
            )
            source_correction_rows.append(corrected)
            all_source_corrections.append({"ray_index": ray_index, **corrected})
            source_mode_histogram[corrected["replay_mode"]] += 1
        adjacent_source = replace(source, chart_id=f"{source.source}:{transfer['adjacent_source_chart']}")

        wrong_terminal = Q(transfer["first_physical_terminal_event_parameter_bracket"][0])
        if wrong_terminal != seam_outer:
            raise RuntimeError("the Round101 collapse is not exactly at the seam")
        wrong_bounds = [
            seam_outer + (wrong_terminal - seam_outer) * Q(index, round94.PROBE_COUNT + 1)
            for index in range(round94.PROBE_COUNT + 2)
        ]
        wrong_rows = [
            frozen_segment(
                adjacent_source, branch,
                q0 + direction * left, q0 + direction * right,
                "ADJACENT_CHART",
            )
            for left, right in zip(wrong_bounds, wrong_bounds[1:])
        ]
        frozen_rows = [*frozen_source_rows, *wrong_rows]
        if len(frozen_rows) != frozen["certified_segment_count"] or digest(frozen_rows) != frozen["certified_segment_rows_sha256"]:
            raise RuntimeError("Round101 frozen segment digest did not rebuild")
        if any(Q(row["q_interval"][0]) != Q(row["q_interval"][1]) for row in wrong_rows):
            raise RuntimeError("an advertised Round101 adjacent segment is unexpectedly positive-width")

        first_bracket = list(map(Q, transfer["first_physical_terminal_event_parameter_bracket"]))
        grazing_bracket = list(map(Q, transfer["transferred_grazing_parameter_bracket"]))
        real_terminal = grazing_bracket[0]
        if first_bracket[1] != real_terminal or not seam_outer < real_terminal < grazing_bracket[1]:
            raise RuntimeError("Round94 seam/grazing endpoint relation changed")
        real_bounds = [
            seam_outer + (real_terminal - seam_outer) * Q(index, round94.PROBE_COUNT + 1)
            for index in range(round94.PROBE_COUNT + 2)
        ]
        if len(real_bounds) != 66 or not all(a < b for a, b in zip(real_bounds, real_bounds[1:])):
            raise RuntimeError("corrected adjacent base partition is not positive-width")

        nonterminal_rows = []
        for index, (lower, upper) in enumerate(zip(real_bounds[:-2], real_bounds[1:-1])):
            row = corrected_segment(adjacent_source, branch, q0, direction, index, lower, upper)
            nonterminal_rows.append(row)
            all_nonterminal.append({"ray_index": ray_index, **row})
            mode_histogram[row["replay_mode"]] += 1
        if len(nonterminal_rows) != 64:
            raise RuntimeError("nonterminal base segment accounting")

        terminal_start = real_bounds[-2]
        terminal_width = real_terminal - terminal_start
        ring_rows = []
        for ring_index in range(ENDPOINT_RING_PREFIX):
            lower = real_terminal - terminal_width / Q(2 ** ring_index)
            upper = real_terminal - terminal_width / Q(2 ** (ring_index + 1))
            qa, qb = q0 + direction * lower, q0 + direction * upper
            if source_normal_chart(adjacent_source, branch, qa, qb) != transfer["adjacent_source_chart"]:
                raise RuntimeError("endpoint-ring source normal left the strict adjacent chart")
            evidence = certify_same_chart(adjacent_source, branch, qa, qb)
            ring = {
                "ring_index": ring_index,
                "parameter_interval": [str(lower), str(upper)],
                "q_interval": [str(qa), str(qb)],
                "strictly_positive_parameter_width": lower < upper,
                "replay_mode": "SAME_CHART_CORRELATED_REPLAY",
                "evidence": evidence,
            }
            ring_rows.append(ring)
            all_rings.append({"ray_index": ray_index, **ring})
        residual_start = real_terminal - terminal_width / Q(2 ** ENDPOINT_RING_PREFIX)
        rows.append({
            "ray_index": ray_index,
            "exterior_port_id": port_id,
            "branch_key": list(branch),
            "projective_end": side,
            "old_source_chart": transfer["old_source_chart"],
            "adjacent_source_chart": transfer["adjacent_source_chart"],
            "round101_stored_terminal_parameter_bracket": frozen["terminal_event_parameter_bracket"],
            "round94_first_physical_terminal_parameter_bracket": transfer["first_physical_terminal_event_parameter_bracket"],
            "round94_tight_grazing_parameter_bracket": transfer["transferred_grazing_parameter_bracket"],
            "wrong_terminal_equals_seam_outer": True,
            "first_physical_bracket_right_equals_tight_grazing_lower": True,
            "frozen_source_chart_segment_row_count": len(frozen_source_rows),
            "frozen_source_chart_same_table_complete_segment_count_revalidated": sum(
                row["replay_mode"] == "SAME_CHART_CORRELATED_REPLAY"
                for row in source_correction_rows
            ),
            "frozen_source_chart_old_table_completeness_revalidated": False,
            "corrected_source_chart_segment_count_certified": len(source_correction_rows),
            "corrected_source_chart_replay_mode_histogram": dict(sorted(Counter(
                row["replay_mode"] for row in source_correction_rows
            ).items())),
            "corrected_source_chart_segment_rows_sha256": digest(source_correction_rows),
            "frozen_adjacent_segment_row_count": len(wrong_rows),
            "frozen_positive_width_adjacent_segment_row_count": 0,
            "frozen_full_segment_digest_independently_rebuilt": True,
            "actual_adjacent_parameter_interval": [str(seam_outer), str(real_terminal)],
            "actual_adjacent_parameter_width": str(real_terminal - seam_outer),
            "unbridged_source_chart_transfer_seam_bracket": [str(inner), str(seam_outer)],
            "unbridged_source_chart_transfer_seam_bracket_width": str(seam_outer - inner),
            "source_chart_transfer_seam_whole_interval_bridged": False,
            "corrected_base_partition_count": 65,
            "certified_positive_width_nonterminal_base_segment_count": len(nonterminal_rows),
            "nonterminal_replay_mode_histogram": dict(sorted(Counter(row["replay_mode"] for row in nonterminal_rows).items())),
            "nonterminal_segment_rows_sha256": digest(nonterminal_rows),
            "terminal_base_segment_whole_closed": False,
            "certified_endpoint_dyadic_ring_prefix_count": len(ring_rows),
            "endpoint_dyadic_ring_strict_adjacent_source_normal_count": len(ring_rows),
            "endpoint_dyadic_ring_rows_sha256": digest(ring_rows),
            "remaining_pre_root_bracket_interval_tail_parameter_interval": [str(residual_start), str(real_terminal)],
            "remaining_pre_root_bracket_interval_tail_relative_width": str(Q(1, 2 ** ENDPOINT_RING_PREFIX)),
            "unresolved_tight_algebraic_source_grazing_root_bracket": [str(grazing_bracket[0]), str(grazing_bracket[1])],
            "source_grazing_corner_status": "PRE_ROOT_LOWER_END_TAIL_PLUS_SEPARATE_TIGHT_ALGEBRAIC_ROOT_BRACKET_OPEN__ROOT_CENTERED_ETA_C3_COLLAR_NOT_YET_CERTIFIED",
        })

    if source_mode_histogram != Counter({
        "SAME_CHART_CORRELATED_REPLAY": 1024,
        "SOURCE_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY": 8,
    }):
        raise RuntimeError(f"source correction replay mode census changed: {source_mode_histogram}")
    if mode_histogram != Counter({
        "SAME_CHART_CORRELATED_REPLAY": 496,
        "SOURCE_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY": 8,
        "OUTGOING_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY": 8,
    }):
        raise RuntimeError(f"corrected replay mode census changed: {mode_histogram}")
    if documents["r109"]["certified_registered_arc_whole_tube_count"] != 52:
        raise RuntimeError("Round109 preserved census changed")
    if documents["r110"]["complete_two_sided_gap_pair_count"] != 56:
        raise RuntimeError("Round110 preserved census changed")
    impacts = impact_rows()
    result = {
        "producer_precision_bits": precision_bits,
        "audited_round101_ray_count": len(rows),
        "round101_reported_source_chart_segment_count": r101["source_chart_segment_count"],
        "round101_frozen_source_chart_segment_row_count_rebuilt": sum(
            row["frozen_source_chart_segment_row_count"] for row in rows
        ),
        "round101_frozen_source_chart_old_table_completeness_revalidated": False,
        "corrected_source_chart_segment_count_certified": len(all_source_corrections),
        "corrected_source_chart_same_table_segment_count_certified": source_mode_histogram[
            "SAME_CHART_CORRELATED_REPLAY"
        ],
        "corrected_source_chart_source_normal_union_segment_count_certified": source_mode_histogram[
            "SOURCE_NORMAL_FOUR_CHART_UNION_CORRELATED_REPLAY"
        ],
        "corrected_source_chart_replay_mode_histogram": dict(sorted(source_mode_histogram.items())),
        "corrected_source_chart_segment_rows_sha256": digest(all_source_corrections),
        "round101_reported_adjacent_chart_segment_count": r101["adjacent_chart_segment_count"],
        "round101_frozen_adjacent_segment_row_count_rebuilt": sum(row["frozen_adjacent_segment_row_count"] for row in rows),
        "round101_frozen_positive_width_adjacent_segment_row_count": 0,
        "round101_remaining_open_exterior_ray_count_claim_revalidated": False,
        "corrected_actual_positive_width_adjacent_base_segment_count": 520,
        "corrected_positive_width_nonterminal_base_segment_count_certified": len(all_nonterminal),
        "corrected_nonterminal_replay_mode_histogram": dict(sorted(mode_histogram.items())),
        "corrected_nonterminal_segment_rows_sha256": digest(all_nonterminal),
        "terminal_base_segment_whole_closed_count": 0,
        "certified_endpoint_dyadic_ring_prefix_per_ray": ENDPOINT_RING_PREFIX,
        "certified_endpoint_dyadic_ring_count": len(all_rings),
        "endpoint_dyadic_ring_strict_adjacent_source_normal_count": len(all_rings),
        "endpoint_dyadic_ring_rows_sha256": digest(all_rings),
        "remaining_pre_root_bracket_interval_tail_count": len(rows),
        "remaining_pre_root_bracket_interval_tail_relative_width_per_ray": str(Q(1, 2 ** ENDPOINT_RING_PREFIX)),
        "unresolved_tight_algebraic_source_grazing_root_bracket_count": len(rows),
        "unbridged_source_chart_transfer_seam_bracket_count": len(rows),
        "end_to_end_source_grazing_ray_closure_count": 0,
        "positive_width_eta_c3_collar_count": 0,
        "whole_collar_complete_57_candidate_ordering_count": 0,
        "ray_correction_rows": rows,
        "ray_correction_rows_sha256": digest(rows),
        "downstream_impact_rows": impacts,
        "downstream_impact_rows_sha256": digest(impacts),
        "preserved_round109_registered_arc_whole_tube_count": 52,
        "preserved_round110_two_sided_gap_pair_count": 56,
        "rank3_face_local_maturity_after_correction": "FACE_METADATA_ONLY__ACTUAL_HOMOGENEOUS_CHILD_MATURITY_0/18",
        "new_immutable_F5_slot_count": 0,
        "new_immutable_F6_slot_count": 0,
        "complete_18_field_operator_block_count": 0,
        "global_Gate5": "10/18__BLOCKS_0__NO_PROMOTION",
        "CM2": "NO-GO_FOR_CLAIM",
        "strict_separator": (
            "Round101's frozen old-chart same-table claim fails on 8 terminal segments and its "
            "adjacent terminal was the transfer seam, producing 520 zero-width rows; corrected "
            "source rows have 1,024 same-table plus 8 four-chart-union replays, and the corrected "
            "open adjacent intervals have 512/520 positive-width base cells certified plus "
            "32 dyadic endpoint rings per ray, while 8 source-chart transfer seam brackets, 8 "
            "pre-root-bracket lower-end tails, 8 separate tight algebraic grazing-root brackets, and all "
            "positive-width (eta,c3) collars remain open"
        ),
        "strict_nonclaims": [
            "rebuilding all 1,032 frozen source rows does not preserve the old same-table completeness claim on its 8 source-normal-seam terminal enclosures",
            "the fixed dyadic ring prefix is not an infinite exhaustion proof",
            "the pre-root-bracket interval tail stops at grazing_inner and is not a root-centred exhaustion or evidence that source cosine tends to zero",
            "the Round93 old-chart inner to adjacent-chart seam-outer bracket is not whole-interval bridged",
            "end-to-end closure is therefore 0/8 even though 512 corrected nonterminal adjacent base cells replay",
            "no positive-width root-centred (eta,c3) collar is constructed",
            "no countable H_{sigma,k} ownership theorem, canonical recut, F5, or F6 slot is installed",
            "the preserved Round109/110 internal computations do not restore endpoint-complete faces",
        ],
        "upstream_and_executable_pins": PINS,
    }
    if result["round101_reported_adjacent_chart_segment_count"] != 520:
        raise RuntimeError("Round101 advertised adjacent census changed")
    if (
        len(all_source_corrections) != 1032
        or len(all_nonterminal) != 512
        or len(all_rings) != 8 * ENDPOINT_RING_PREFIX
    ):
        raise RuntimeError("corrected reconstruction accounting")
    result = json.loads(json.dumps(result, sort_keys=True, allow_nan=False))
    return {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build(args.precision_bits), sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
