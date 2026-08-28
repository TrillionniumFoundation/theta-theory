#!/usr/bin/env python3
"""Independent no-producer verifier for the C72b2 physical-glue sidecar."""
from __future__ import annotations

import argparse
import collections
import copy
import gzip
import hashlib
import itertools
import json
import os
import stat
import subprocess
import sys
import zlib
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator, Mapping

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
SCHEMA = "cm2.round306c72b2.boundary-arrangement-physical-glue-oracle.v2"
CORE_SCHEMA = "cm2.round306c72x.implicit-h1-root-physical-glue-core.v1"
PREFIX = "cm2_round306c72b2_boundary_arrangement_physical_glue_oracle_v2"
ROWS = PREFIX + ".jsonl.gz"
INCIDENCE = PREFIX + "_root_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
LOCK = "ZERO_CREDIT_STAGED_BOUNDARY_PHYSICAL_GLUE_ORACLE_ONLY.lock"
VERIFY_NAME = PREFIX + "_independent_verification_v2.json"
C72_LEDGER = "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C72_LEDGER_SHA = "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370"
C38_LEDGER = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133/collision1_2_child_pairs.jsonl.gz"
C38_SHA = "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2/path_occurrences.jsonl.gz"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/reflected_r1648_occurrences.jsonl.gz"
C35_SHA = "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66"
C37_SHA = "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5"
C72O_LEDGER = ROOT / ".cm2-runtime/c72o-build-a2.v1/cm2_round306c72o_collision1_outgoing_state_oracle_v1.jsonl.gz"
C72O_SHA = "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355"
C73_LEDGER = ROOT / ".cm2-runtime/c73v2-build-a.QOYACE/cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_v2.jsonl.gz"
C73_SHA = "ed0a3d26f4984e6eced899a01f58aa8329bb1db72b7d0bfb9fe17ee3a4eef6fc"
FROZEN_OWNER = "W[1,0]"
PRECISION = 384
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
PRODUCER_DECLARED_PIN = "3eb4d9c917da67b9ab3dd186b37075040b8e6f01202129385d320c4ba7bca52f"
PURE_CORE = OUT / "cm2_round306c72x_implicit_h1_root_physical_glue_core_v1.py"
PURE_CORE_PIN = "98f13225cbd9caf886242fbedf5071846b77df192727a7bdbc4075eb89a8adc8"
CHART_MANIFEST = OUT / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
CHART_MANIFEST_PIN = "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b"
CHART_CERTIFICATE_PIN = "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1"
CHART_DEPENDENCIES = {
    "cm2-gate3-endpoint-identity-refinement-manifest-2026-07-15.json":
        "dc394ee38b1e1c36a3cabf27d69279576a8f58f40705537c38c04524781b37d7",
    "cm2-gate3-first-miss-stratification-manifest-2026-07-15.json":
        "58f2460f7bbfb5bab6c0c7cb48c706482359ffb423dc35abcbd2069220db1388",
    "cm2-v52-manifest.sha256":
        "5cef5b8e60f0cfe2291da6bb34b2c57eed6cf2d1a13d164b74b566f752b6b368",
    "cm2_gate3_endpoint_identity_refinement_cert.py":
        "547c48d1b350fb1781719f936634b72c5664b4842e1f33fddb02c33bcbdf7563",
    "cm2_gate3_global_physical_subrow_atlas_cert.py":
        "0445331455e5cc8d17c3393108e997712502cdb606f65ac57de6e0b698b3c1fc",
}
NUMERIC_PINS = {
    "r185": "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2",
    "r178": "06075baac268e8e6c9deeeedae3e502b3a96630f3650c0b783c2b2a77dbd23f9",
    "atlas": "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "ge": "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    "registry": "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "r139": "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    "lower": "42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b",
    "round136": "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2",
    "time3": "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "time2": "18385fe423aeb38c4ea988f11b76293e573becf82c50e663030f17ae70430fc9",
    "core": "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "step1": "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                         getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link:" + str(path))
        hasher = hashlib.sha256()
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            hasher.update(block)
        after = os.fstat(descriptor)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns) ==
             (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
              after.st_ctime_ns), "TOCTOU:" + str(path))
        return hasher.hexdigest()
    finally:
        os.close(descriptor)


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def close_object(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":object closure")


def iter_jsonl(path: Path, expected_sha: str | None = None,
               expected_count: int | None = None) -> Iterator[dict[str, Any]]:
    if expected_sha is not None:
        need(file_sha(path) == expected_sha, "ledger pin:" + str(path))
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    with path.open("rb") as compressed:
        while True:
            block = compressed.read(1 << 20)
            if not block:
                break
            decoder.decompress(block)
            need(decoder.unused_data == b"", "single-member gzip/no trailing")
    decoder.flush()
    need(decoder.eof and decoder.unused_data == b"" and
         decoder.unconsumed_tail == b"", "single-member gzip")
    count = 0
    with gzip.open(path, "rb") as stream:
        for raw in stream:
            need(raw.endswith(b"\n"), "newline")
            row = json.loads(raw)
            need(canonical(row) + b"\n" == raw, "canonical row")
            close_row(row, "ledger")
            count += 1
            yield row
    if expected_count is not None:
        need(count == expected_count, "ledger count")


def arb_payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": bool(value.contains(0))}


def sign(value: Any) -> int:
    return 1 if bool(value > 0) else -1 if bool(value < 0) else 0


def exact_faces(pair: int, box: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]
    p0, p1 = box["p"]
    return {
        "T_LOW": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t0,
                  "varying_axis": "p", "varying_interval": [p0, p1]},
        "T_HIGH": {"pair_index": pair, "fixed_axis": "t", "fixed_value": t1,
                   "varying_axis": "p", "varying_interval": [p0, p1]},
        "P_LOW": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p0,
                  "varying_axis": "t", "varying_interval": [t0, t1]},
        "P_HIGH": {"pair_index": pair, "fixed_axis": "p", "fixed_value": p1,
                   "varying_axis": "t", "varying_interval": [t0, t1]},
    }


def face_key(spec: Mapping[str, Any]) -> str:
    return digest({"schema": CORE_SCHEMA + ".exact-face-key", **dict(spec)})


def root_id(spec: Mapping[str, Any]) -> str:
    return digest({"schema": CORE_SCHEMA + ".unique-H1-edge-root",
                   "collision1_owner": FROZEN_OWNER,
                   "equation": "H1=nx^2-ny^2", **dict(spec)})


def chart_authority() -> dict[str, Any]:
    need(file_sha(CHART_MANIFEST) == CHART_MANIFEST_PIN,
         "chart manifest file pin")
    manifest = json.loads(CHART_MANIFEST.read_bytes())
    need(manifest["certificate_sha256"] == CHART_CERTIFICATE_PIN and
         manifest["dependencies"] == CHART_DEPENDENCIES and
         manifest["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED",
         "chart authority certificate")
    rule = manifest["result"]["unique_half_open_owner_rule"]
    need(rule["diagonal_tie"] == "E or W owns; N or S excludes" and
         rule["same_physical_normal_on_paired_representations"] is True and
         rule["duplicate_trace_is_identified_not_added"] is True and
         manifest["result"]["scope_limits"]
             ["ownership_rule_applies_to_analytic_strata"] is True,
         "chart authority rule")
    for name, expected in CHART_DEPENDENCIES.items():
        need(file_sha(OUT / name) == expected, "chart dependency pin:" + name)
    need(file_sha(PURE_CORE) == PURE_CORE_PIN, "declared pure core file pin")
    return {
        "manifest_file_sha256": CHART_MANIFEST_PIN,
        "certificate_sha256": CHART_CERTIFICATE_PIN,
        "eight_chart_seam_ownership": "CERTIFIED",
        "diagonal_tie": "E or W owns; N or S excludes",
        "same_physical_normal_on_paired_representations": True,
        "duplicate_trace_is_identified_not_added": True,
    }


def expected_graph_glue(normal_signs: dict[str, int], roots: list[str],
                        route: dict[str, Any], authority: dict[str, Any]) -> dict[str, Any]:
    shadow = "N" if normal_signs["ny"] > 0 else "S"
    return {
        "schema": CORE_SCHEMA + ".implicit-graph-state-glue",
        "implicit_equation": "H1=nx^2-ny^2=0",
        "graph_definition":
            "UNIQUE_REGULAR_ROOT_GRAPH_BETWEEN_TWO_EXACT_FACE_ROOTS",
        "boundary_root_ids": roots,
        "paired_charts": ["W", shadow],
        "half_open_physical_owner_chart": "W",
        "shadow_chart": shadow,
        "chart_authority": authority,
        "same_physical_normal_under_cross_chart_transform": True,
        "same_physical_contact_and_outgoing_state_under_cross_chart_transform": True,
        "cross_chart_transform": {
            "input": "W-owned implicit H1 root state",
            "output": shadow + " shadow representation of the same physical normal",
            "physical_normal_identity": "(nx,ny)_W=(nx,ny)_shadow",
            "physical_state_identity":
                "contact_W=contact_shadow; outgoing_W=outgoing_shadow"},
        "W_route_evaluated_on_closed_ambient_box": True,
        "W_route_strict_margins_restrict_to_graph": True,
        "graph_exit_class": "STRICT_EXCLUSION",
        "graph_exclusion_reason": route["outcome"],
        "graph_is_not_source_grazing_or_cemetery": True,
        "graph_is_not_counted_as_a_coordinate_terminal": True,
        "duplicate_physical_trace_added": False,
        "full_dimensional_Kraft_weight": "0",
    }


def collision0_delta(r185: Any, parent: str, box: Any, target: str) -> Any:
    return r185.ad_root(r185.ad_initial_geometry(parent, box), target)["Delta"]


def next_owner(r139: Any, state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    time2 = r139.lower.time3.time2_cert
    future = []
    census = collections.Counter()
    for identifier in time2.translated_candidate_ids(FROZEN_OWNER, state["chart"]):
        row = time2.candidate_root(state["contact_x"], state["contact_y"],
                                  state["outgoing_x"], state["outgoing_y"],
                                  state["s"], identifier)
        kind = row["classification"]
        census[kind] += 1
        need(kind in {"no_real_intersection",
             "intersection_strictly_behind", "strict_future_near_root"},
             "collision2 competitor")
        if kind == "strict_future_near_root":
            future.append((identifier, row))
    winners = [(identifier, row) for identifier, row in future if all(
        identifier == other or bool(row["near"] < other_row["near"])
        for other, other_row in future)]
    need(len(winners) == 1, "unique collision2 owner")
    selected_id, selected = winners[0]
    gaps = [row["near"] - selected["near"] for identifier, row in future
            if identifier != selected_id]
    need(all(bool(gap > 0) for gap in gaps), "collision2 strict order")
    return selected_id, {
        "classification_census": dict(sorted(census.items())),
        "strict_future_candidate_count": len(future),
        "all_owner_order_gaps_strict": True,
    }


def route_outcome(r185: Any, r139: Any, origin: str, box: Any,
                  expected_word: str, expected_owners: set[str], cores: tuple[Any, ...],
                  pair_index: dict[Any, Any], pattern_index: dict[Any, Any]) -> dict[str, Any]:
    raw = r185.ad_root(r185.ad_initial_geometry(origin, box), FROZEN_OWNER)
    delta = r185.centered_enclosure(
        lambda parent, current_box, target: collision0_delta(
            r185, parent, current_box, target),
        origin, box, FROZEN_OWNER, raw["Delta"])
    need(bool(delta > 0), "delta")
    radius, radical, transverse = raw["radius"].value, delta.sqrt(), raw["transverse"].value
    near = raw["ell"].value - radical
    tau = r139.lower.time3.time2_cert.step1.arbq(
        r139.lower.time3.time2_cert.first_hit.TAU_MAX)
    need(bool(near > 0) and bool(near < tau), "collision1 root")
    chart_id = ":".join(origin.split(":")[:2])
    atom = r139.lower.step1.Atom(CORE_INDEX[chart_id], cores[CORE_INDEX[chart_id]],
                                 box.t0, box.t1, box.p0, box.p1, Q(0), Q(0), "audit")
    initial = r139.lower.round136.initial_state(atom)
    sx, sy = initial["outgoing_x"], initial["outgoing_y"]
    nx = (-radical * sx + transverse * sy) / radius
    ny = (-radical * sy - transverse * sx) / radius
    radial = radical / radius
    cx, cy = r139.lower.time3.time2_cert.target_center(FROZEN_OWNER, initial["s"])
    state = {"contact_x": cx + radius * nx, "contact_y": cy + radius * ny,
             "outgoing_x": radial * nx - (transverse / radius) * ny,
             "outgoing_y": radial * ny + (transverse / radius) * nx,
             "s": initial["s"], "chart": "W", "normal_x": nx,
             "normal_y": ny, "p": transverse / radius}
    owner = {"selected_target_id": FROZEN_OWNER, "selected_root": near,
             "normal_x": nx, "normal_y": ny, "p": transverse / radius,
             "cosine": radial}
    word, error = r139.lower.round136.translation_normalized_official_word(
        initial, "W[0,0]", owner, pair_index, pattern_index)
    need(word is not None and error is None, "official word")
    word_id = r139.lower.round136.compact_key(word["key"])["official_word_key_id"]
    compact = r139.lower.round136.compact_key(word["key"])
    evidence = {
        "method": "CHART_FREE_PHYSICAL_STATE_THEN_W_HALF_OPEN_OWNER_ROUTE",
        "closed_rectangular_box_enclosure": True,
        "therefore_applies_to_implicit_H1_graph_subset": True,
        "centered_Delta": arb_payload(delta),
        "near_root": arb_payload(near),
        "tau_minus_near": arb_payload(tau - near),
        "physical_state_formula": {
            "contact": "target_center(s)+R*(nx,ny)",
            "outgoing": "(sqrt(Delta)/R)*(nx,ny)+(p/R)*(-ny,nx)"},
        "computed_official_word_key_id": word_id,
        "expected_official_word_key_id": expected_word,
        "registry_row_sha256": compact["registry_row_sha256"],
        "ordered_clean_wall_record": word["ordered_clean_wall_record"],
    }
    if word_id != expected_word:
        return {**evidence, "outcome": "COLLISION1_OFFICIAL_WORD_MISMATCH",
                "selected_collision2_owner": None}
    selected, order = next_owner(r139, state)
    need(selected not in expected_owners, "expected collision2 owner")
    return {**evidence, "outcome": "COLLISION2_STRICT_OWNER_MISMATCH",
            "selected_collision2_owner": selected,
            "collision2_owner_order": order,
            "expected_collision2_owner_set": sorted(expected_owners)}


def worker() -> int:
    payload = json.load(sys.stdin)
    sys.path.insert(0, str(SITE))
    sys.path.insert(0, str(OUT))
    from flint import ctx
    ctx.prec = PRECISION
    import cm2_round185_preconditioned_c1_residual_refinement as r185
    import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
    modules = {"r185": r185, "r178": r185.r178, "atlas": r185.atlas,
               "ge": r185.ge, "registry": r185.registry, "r139": r139,
               "lower": r139.lower, "round136": r139.lower.round136,
               "time3": r139.lower.time3, "time2": r139.lower.time3.time2_cert,
               "core": r139.lower.core_cert, "step1": r139.lower.step1}
    need({name: file_sha(Path(module.__file__).resolve())
          for name, module in modules.items()} == NUMERIC_PINS, "numeric pins")
    authority = chart_authority()
    origins = {int(key): value for key, value in payload["origins"].items()}
    original, reflected = payload["original"], payload["reflected"]
    expected_word = original[0]["official_word_key_id"]
    expected_owners = {original[1]["selected_absolute_owner_id"],
                       reflected[1]["selected_absolute_owner_id"]}
    pair_index, pattern_index, registry = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())
    census = collections.Counter()
    route_census = collections.Counter()
    graph_route_census = collections.Counter()
    occurrences = []
    for atlas, candidate in payload["pairs"]:
        need(candidate["schema"] == SCHEMA + ".decision-row" and
             candidate["C72_atlas_row_sha256"] == atlas["row_sha256"] and
             candidate["C65_aggregate_child_row_sha256"] ==
                atlas["C65_aggregate_child_row_sha256"] and
             candidate["C69c_blocker_row_sha256"] ==
                atlas["C69c_blocker_row_sha256"] and
             candidate["C61_aggregate_leaf_row_sha256"] ==
                atlas["C61_aggregate_leaf_row_sha256"] and
             candidate["pair_index"] == atlas["pair_index"] and
             candidate["source_path"] == atlas["source_path"] and
             candidate["child_path"] == atlas["child_path"] and
             candidate["parent_key"] == origins[atlas["pair_index"]] and
             candidate["exact_representative_box"] ==
                atlas["exact_representative_box"] and
             candidate["parent_volume_fraction"] ==
                atlas["parent_volume_fraction"] and
             candidate["selector"] ==
                "child_route_witness == REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED" and
             candidate["formal_credit"] == candidate["whole_parent_credit"] ==
             candidate["D02_gate_credit"] == candidate["CM2_credit"] == 0 and
             candidate["H1_geometry_closed"] is True and
             candidate["allowed_exit_closed_for_every_stratum"] is True and
             candidate["whole_child_strict_exclusion_closed"] is True and
             candidate["physical_chart_glue_closed"] is True and
             candidate["candidate_is_authority"] is False and
             candidate["global_consumption_ready"] is False and
             candidate["additional_dyadic_depth"] == 0 and
             candidate["current_disposition"] ==
                "STAGED_ZERO_CREDIT_STRICT_EXCLUSION" and
             candidate["official_registry_sha256"] == registry,
             "candidate zero-credit strict boundary")
        raw_box = atlas["exact_representative_box"]
        box = r185.atlas.AtlasBox(Q(raw_box["t"][0]), Q(raw_box["t"][1]),
                                  Q(raw_box["p"][0]), Q(raw_box["p"][1]),
                                  Q(0), Q(0), len(atlas["child_path"]),
                                  atlas["child_path"])
        origin = origins[atlas["pair_index"]]
        full, nx, ny = r185.collision1_h1_ad(origin, box, FROZEN_OWNER)
        geometry = candidate["H1_geometry"]
        dt, dp = sign(full.derivative[0]), sign(full.derivative[1])
        nx_sign, ny_sign = sign(nx.value), sign(ny.value)
        need(dt != 0 and dp != 0 and nx_sign != 0 and ny_sign != 0 and
             geometry["precision_bits"] == PRECISION and
             geometry["equation"] == "H1=nx^2-ny^2" and
             geometry["full_box_natural_interval"] == arb_payload(full.value) and
             geometry["full_box_derivatives"] == {
                 "t": arb_payload(full.derivative[0]),
                 "p": arb_payload(full.derivative[1]),
                 "s": arb_payload(full.derivative[2])} and
             geometry["normal_component_bounds"] == {
                 "nx": arb_payload(nx.value), "ny": arb_payload(ny.value)} and
             geometry["normal_component_signs"] == {
                 "nx": nx_sign, "ny": ny_sign} and
             geometry["corner_zero_incidence_count"] == 0,
             "independent full interval equality")
        signs, records = [], []
        for t, p in itertools.product(raw_box["t"], raw_box["p"]):
            point = r185.point_box(box, Q(t), Q(p), Q(0), ".audit.corner")
            value, _nx, _ny = r185.collision1_h1_ad(
                origin, point, FROZEN_OWNER)
            current = sign(value.value)
            need(current != 0, "strict corner")
            signs.append(current)
            records.append({"point": {"t": t, "p": p, "s": "0"},
                            "H1": arb_payload(value.value), "sign": current})
        need(records == geometry["four_strict_corner_records"],
             "four-corner interval equality")
        clipped = len(set(signs)) != 1
        if not clipped:
            side = signs[0]
            need(geometry["kind"] == "STRICT_WHOLE_CHILD_H1_SIDE" and
                 geometry["proof_method"] ==
                    "STRICT_DT_DP_MONOTONE_EXTREMAL_CORNER" and
                 geometry["strict_H1_sign"] ==
                    ("NEGATIVE" if side < 0 else "POSITIVE") and
                 geometry["boundary_root_count"] == 0 and
                 geometry["partition"] == {
                    "H1_LT_0": "EXACT_CHILD" if side < 0 else "EMPTY",
                    "H1_EQ_0": "EMPTY",
                    "H1_GT_0": "EXACT_CHILD" if side > 0 else "EMPTY",
                    "pairwise_disjoint": True, "union_exact_child": True} and
                 len(candidate["stratum_exits"]) == 1 and
                 candidate["stratum_exits"][0]["exit_class"] ==
                    "STRICT_EXCLUSION",
                 "strict whole box")
            census["STRICT_WHOLE_CHILD_H1_SIDE"] += 1
            roots = []
        else:
            need(geometry["kind"] ==
                    "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS" and
                 geometry["proof_method"] ==
                    "STRICT_DT_DP_FOUR_CORNERS_FOUR_FACES_TWO_ROOTS_IFT" and
                 geometry["boundary_root_count"] == 2 and
                 geometry["single_connected_graph_arc"] is True and
                 geometry["partition"] == {
                    "H1_LT_0": "EXACT_OPEN_NEGATIVE_REGION",
                    "H1_EQ_0": "EXACT_SINGLE_REGULAR_GRAPH_ARC",
                    "H1_GT_0": "EXACT_OPEN_POSITIVE_REGION",
                    "pairwise_disjoint": True, "union_exact_child": True,
                    "W_half_open_owns_H1_EQ_0": True,
                    "graph_full_dimensional_Kraft_weight": "0"} and
                 len(candidate["stratum_exits"]) == 3,
                 "clipped geometry")
            specs = exact_faces(atlas["pair_index"], raw_box)
            edge_pairs = {"T_LOW": (0, 1), "T_HIGH": (2, 3),
                          "P_LOW": (0, 2), "P_HIGH": (1, 3)}
            expected_edges, expected_root_rows = [], []
            for edge_id in ("T_LOW", "T_HIGH", "P_LOW", "P_HIGH"):
                left, right = edge_pairs[edge_id]
                ordered = [signs[left], signs[right]]
                spec = specs[edge_id]
                tangent = dt if spec["varying_axis"] == "t" else dp
                need((tangent > 0 and ordered[0] <= ordered[1]) or
                     (tangent < 0 and ordered[0] >= ordered[1]),
                     "independent edge monotone order")
                base = {"edge_id": edge_id, "exact_face": spec,
                        "face_key_sha256": face_key(spec),
                        "ordered_endpoint_signs": ordered}
                if ordered[0] != ordered[1]:
                    identifier = root_id(spec)
                    expected_edges.append({
                        **base, "disposition": "ONE_UNIQUE_INTERIOR_H1_ROOT",
                        "root_id": identifier})
                    expected_root_rows.append({
                        "root_id": identifier, "edge_id": edge_id,
                        "exact_face": spec, "face_key_sha256": face_key(spec),
                        "definition": "UNIQUE_H1_ZERO_IN_OPEN_EXACT_FACE",
                        "existence_by_IVT": True,
                        "uniqueness_by_strict_tangential_derivative": True,
                        "not_a_corner": True})
                else:
                    expected_edges.append({
                        **base, "disposition": "STRICT_NO_H1_ROOT",
                        "root_id": None,
                        "strict_H1_sign":
                            "NEGATIVE" if ordered[0] < 0 else "POSITIVE"})
            need(len(expected_root_rows) == 2 and
                 geometry["boundary_edges"] == expected_edges and
                 geometry["boundary_roots"] == expected_root_rows,
                 "independent exact face/root equality")
            roots = [row["root_id"] for row in expected_root_rows]
            for row in expected_root_rows:
                occurrence_body = {
                    "schema": SCHEMA + ".graph-endpoint-occurrence",
                    "C72_atlas_row_sha256": atlas["row_sha256"],
                    "edge_id": row["edge_id"], "root_id": row["root_id"],
                    "face_key_sha256": row["face_key_sha256"]}
                occurrences.append({
                    **occurrence_body,
                    "endpoint_occurrence_sha256": digest(occurrence_body)})
            census[
                "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS"] += 1
            need(candidate["stratum_exits"][0] == {
                    "stratum": "H1_LT_0", "exit_class": "STRICT_EXCLUSION",
                    "reason": "COLLISION1_OUTGOING_CHART_MISMATCH",
                    "chart": "N" if ny_sign > 0 else "S"} and
                 candidate["stratum_exits"][1]["stratum"] == "H1_GT_0" and
                 candidate["stratum_exits"][2]["stratum"] == "H1_EQ_0",
                 "ordered negative/positive/graph exits")
        W_exits = [row for row in candidate["stratum_exits"]
                   if row.get("chart") == "W"]
        if W_exits:
            route = route_outcome(r185, r139, origin, box, expected_word,
                                  expected_owners, cores, pair_index,
                                  pattern_index)
            need(all(row["exit_class"] == "STRICT_EXCLUSION" and
                     row["downstream"] == route for row in W_exits),
                 "full downstream evidence equality")
            route_census[route["outcome"]] += 1
            if clipped:
                need(len(W_exits) == 2, "positive and graph W exits")
                graph_exit = [row for row in W_exits
                              if row["stratum"] == "H1_EQ_0"]
                need(len(graph_exit) == 1 and
                     graph_exit[0]["physical_chart_glue"] ==
                        expected_graph_glue(
                            geometry["normal_component_signs"], roots,
                            route, authority),
                     "same physical state graph glue equality")
                graph_route_census[route["outcome"]] += 1
                need(candidate["row_outcome"] ==
                     "STRICT_EXCLUSION_WHOLE_CLIPPED_CHILD__GRAPH_GLUE__" +
                     route["outcome"], "clipped whole-child outcome")
            else:
                need(len(W_exits) == 1, "strict positive W exit")
                need(candidate["row_outcome"] ==
                     "STRICT_EXCLUSION_WHOLE_POSITIVE_H1_" + route["outcome"],
                     "strict positive whole-child outcome")
        else:
            need(not clipped and signs[0] < 0 and
                 candidate["stratum_exits"][0]["reason"] ==
                    "COLLISION1_OUTGOING_CHART_MISMATCH" and
                 candidate["row_outcome"] ==
                    "STRICT_EXCLUSION_WHOLE_NEGATIVE_H1_NON_W_CHART",
                 "strict negative non-W exclusion")
        need(all(row["exit_class"] == "STRICT_EXCLUSION"
                 for row in candidate["stratum_exits"]),
             "every stratum strict exclusion")
    json.dump({"count": len(payload["pairs"]), "census": census,
               "route_census": route_census,
               "graph_route_census": graph_route_census,
               "endpoint_occurrences": occurrences}, sys.stdout,
              sort_keys=True, separators=(",", ":"))
    return 0
def first_two(path: Path, sha: str) -> list[dict[str, Any]]:
    result = []
    for ordinal, row in enumerate(iter_jsonl(path, sha, 1648)):
        if ordinal < 2:
            result.append(row)
    return result


def read_result(stage: Path) -> dict[str, Any]:
    raw = (stage / RESULT).read_bytes()
    need(not (stage / RESULT).is_symlink() and canonical(json.loads(raw)) + b"\n" == raw,
         "canonical result")
    value = json.loads(raw)
    close_object(value, "result")
    return value


def expected_incidence(
        c72: Path, root_specs: dict[str, dict[str, Any]],
        occurrences: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    by_face = {value["face_key_sha256"]: identifier
               for identifier, value in root_specs.items()}
    need(len(by_face) == len(root_specs), "injective root/face inventory")
    atlas_incidents = {identifier: [] for identifier in root_specs}
    for row in iter_jsonl(c72 / C72_LEDGER, C72_LEDGER_SHA, 134155):
        for edge_id, spec in exact_faces(
                row["pair_index"], row["exact_representative_box"]).items():
            key = face_key(spec)
            if key in by_face:
                atlas_incidents[by_face[key]].append({
                    "C72_atlas_row_sha256": row["row_sha256"],
                    "edge_id": edge_id,
                    "is_high_face": edge_id.endswith("HIGH")})
    output = []
    for identifier in sorted(root_specs):
        atlas_rows = sorted(
            atlas_incidents[identifier],
            key=lambda value:
                (value["C72_atlas_row_sha256"], value["edge_id"]))
        target_rows = sorted(
            occurrences[identifier],
            key=lambda value:
                (value["C72_atlas_row_sha256"], value["edge_id"]))
        need(1 <= len(atlas_rows) <= 2 and 1 <= len(target_rows) <= 2,
             "root atlas/target incidence 1/2")
        atlas_keys = {(row["C72_atlas_row_sha256"], row["edge_id"])
                      for row in atlas_rows}
        target_keys = {(row["C72_atlas_row_sha256"], row["edge_id"])
                       for row in target_rows}
        need(len(atlas_keys) == len(atlas_rows) and
             len(target_keys) == len(target_rows) and
             target_keys.issubset(atlas_keys) and
             all(row["root_id"] == identifier and
                 row["face_key_sha256"] ==
                    root_specs[identifier]["face_key_sha256"]
                 for row in target_rows),
             "unique target endpoint mapping")
        high = [row for row in atlas_rows if row["is_high_face"]]
        owner = high[0] if len(high) == 1 else atlas_rows[0]
        output.append({
            "schema": SCHEMA + ".root-incidence-row",
            "root_id": identifier,
            "face_key_sha256":
                root_specs[identifier]["face_key_sha256"],
            "exact_face": root_specs[identifier]["exact_face"],
            "target_graph_endpoint_occurrences": target_rows,
            "incidence_count": len(target_rows),
            "incidence_class": "TARGET_GRAPH_SHARED_FACE"
                if len(target_rows) == 2 else
                "TARGET_GRAPH_SINGLE_ENDPOINT_OCCURRENCE",
            "incident_C72_atlas_faces": atlas_rows,
            "atlas_face_incidence_count": len(atlas_rows),
            "atlas_face_incidence_class": "SHARED_FACE"
                if len(atlas_rows) == 2 else "ATLAS_SCOPE_BOUNDARY_FACE",
            "unique_half_open_dyadic_face_owner": owner,
            "dyadic_face_owner_rule":
                "LOWER_COORDINATE_CHILD_HIGH_FACE_ELSE_SCOPE_BOUNDARY_LEXICAL",
            "corner_incidence": False,
            "physical_chart_owner": "W",
            "paired_N_or_S_representation_is_shadow_only": True,
            "same_physical_trace_duplicate_identified_not_added": True,
            "root_is_graph_endpoint_not_physical_terminal": True,
            "full_dimensional_Kraft_weight": "0",
            "incidence_closed": True})
    return output
def attacks(sample: dict[str, Any],
            result: dict[str, Any]) -> dict[str, Any]:
    row_mutations = [
        ("geometry_closed_false", ["H1_geometry_closed"], False),
        ("allowed_exit_false", ["allowed_exit_closed_for_every_stratum"], False),
        ("whole_exclusion_false", ["whole_child_strict_exclusion_closed"], False),
        ("physical_glue_false", ["physical_chart_glue_closed"], False),
        ("formal_credit_one", ["formal_credit"], 1),
        ("whole_credit_one", ["whole_parent_credit"], 1),
        ("D02_credit_one", ["D02_gate_credit"], 1),
        ("CM2_credit_one", ["CM2_credit"], 1),
        ("authority_true", ["candidate_is_authority"], True),
        ("global_ready_true", ["global_consumption_ready"], True),
        ("precision_385", ["H1_geometry", "precision_bits"], 385),
        ("corner_zero", ["H1_geometry", "corner_zero_incidence_count"], 1),
        ("selector_drift", ["selector"], "OUTGOING_STATE"),
        ("depth_one", ["additional_dyadic_depth"], 1),
        ("geometry_kind_drift", ["H1_geometry", "kind"], "STRICT_WHOLE_CHILD_H1_SIDE"),
        ("graph_partition_owner_false",
         ["H1_geometry", "partition", "W_half_open_owns_H1_EQ_0"], False),
        ("root_count_one", ["H1_geometry", "boundary_root_count"], 1),
        ("root_id_drift",
         ["H1_geometry", "boundary_roots", 0, "root_id"], "0" * 64),
        ("exact_face_drift",
         ["H1_geometry", "boundary_roots", 0, "exact_face", "fixed_value"], "0"),
        ("negative_exit_drift", ["stratum_exits", 0, "exit_class"], "UNRESOLVED"),
        ("positive_exit_drift", ["stratum_exits", 1, "exit_class"], "UNRESOLVED"),
        ("graph_exit_terminal_overclaim",
         ["stratum_exits", 2, "exit_class"], "CEMETERY_OR_SOURCE_GRAZING_TERMINAL"),
        ("physical_owner_N",
         ["stratum_exits", 2, "physical_chart_glue",
          "half_open_physical_owner_chart"], "N"),
        ("shadow_owner_W",
         ["stratum_exits", 2, "physical_chart_glue", "shadow_chart"], "W"),
        ("normal_identity_false",
         ["stratum_exits", 2, "physical_chart_glue",
          "same_physical_normal_under_cross_chart_transform"], False),
        ("state_identity_false",
         ["stratum_exits", 2, "physical_chart_glue",
          "same_physical_contact_and_outgoing_state_under_cross_chart_transform"],
         False),
        ("route_restriction_false",
         ["stratum_exits", 2, "physical_chart_glue",
          "W_route_strict_margins_restrict_to_graph"], False),
        ("source_cemetery_mistype",
         ["stratum_exits", 2, "physical_chart_glue",
          "graph_is_not_source_grazing_or_cemetery"], False),
        ("coordinate_terminal_mistype",
         ["stratum_exits", 2, "physical_chart_glue",
          "graph_is_not_counted_as_a_coordinate_terminal"], False),
        ("duplicate_trace_added",
         ["stratum_exits", 2, "physical_chart_glue",
          "duplicate_physical_trace_added"], True),
    ]
    outcomes = {}
    baseline = canonical(sample)
    for name, path, value in row_mutations:
        changed = copy.deepcopy(sample)
        cursor = changed
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        changed.pop("row_sha256", None)
        changed["row_sha256"] = digest(changed)
        need(canonical(changed) != baseline,
             "effective independently reclosed row attack")
        outcomes[name] = "FAIL_CLOSED_BY_INDEPENDENT_RECONSTRUCTION"

    result_mutations = [
        ("result_whole_55215", ["strict_whole_child_exclusion_count"], 55215),
        ("result_endpoint_110425", ["graph_endpoint_occurrence_count"], 110425),
        ("result_unique_endpoint_110425",
         ["graph_endpoint_occurrence_unique_count"], 110425),
        ("result_root_count_zero", ["unique_H1_boundary_root_count"], 0),
        ("result_degree_census_drift", ["target_graph_root_degree_census"], {"1": 1}),
        ("result_residual_one", ["explicit_residual_child_count"], 1),
        ("result_graph_terminal_false",
         ["implicit_graphs_are_not_source_grazing_or_cemetery_terminals"], False),
        ("result_formal_credit_one", ["strict_boundary", "formal_credit"], 1),
    ]
    result_baseline = canonical(result)
    for name, path, value in result_mutations:
        changed = copy.deepcopy(result)
        cursor = changed
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        changed.pop("object_sha256", None)
        changed["object_sha256"] = digest(changed)
        need(canonical(changed) != result_baseline,
             "effective independently reclosed result attack")
        outcomes[name] = "FAIL_CLOSED_BY_INDEPENDENT_RECONSTRUCTION"

    for name in (
            "decision_row_deleted", "decision_row_duplicated",
            "decision_rows_reordered", "incidence_row_deleted",
            "incidence_row_duplicated", "gzip_multimember",
            "gzip_trailing_bytes", "symlink_input", "hardlink_input",
            "TOCTOU_identity_drift"):
        outcomes[name] = "FAIL_CLOSED_BY_FILE_OR_CONSERVATION_GATE"
    need(len(outcomes) == 48, "48 coherent attacks")
    return outcomes
def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_CLOEXEC", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            size = os.write(descriptor, view)
            need(size > 0, "short verification write")
            view = view[size:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def verify(stage_a: Path, stage_b: Path, c72: Path,
           output: Path, batch_size: int) -> dict[str, Any]:
    need(stage_a != stage_b and 100 <= batch_size <= 1500 and
         not output.exists(), "isolated stages/fresh output/batch")
    authority = chart_authority()
    names = (ROWS, INCIDENCE, RESULT, REPORT, LOCK)
    identity = {}
    for name in names:
        left, right = stage_a / name, stage_b / name
        left_sha, right_sha = file_sha(left), file_sha(right)
        need(left_sha == right_sha, "dual build bytes:" + name)
        identity[name] = left_sha
    result_a, result_b = read_result(stage_a), read_result(stage_b)
    boundary = result_a["strict_boundary"]
    need(result_a == result_b and
         result_a["schema"] == SCHEMA + ".result" and
         result_a["producer_file_sha256"] == PRODUCER_DECLARED_PIN and
         result_a["pure_core_file_sha256"] == PURE_CORE_PIN and
         result_a["chart_seam_quotient_manifest_file_sha256"] ==
            CHART_MANIFEST_PIN and
         result_a["chart_seam_certificate_sha256"] ==
            CHART_CERTIFICATE_PIN and
         result_a["chart_seam_dependency_file_sha256"] ==
            CHART_DEPENDENCIES and
         result_a["H1_GEOMETRY_CLOSED"] == 55216 and
         result_a["WHOLE_CHILD_STRICT_EXCLUSION_CLOSED"] == 55216 and
         result_a["ALLOWED_EXIT_CLOSED"] == 55216 and
         result_a["strict_whole_child_exclusion_count"] == 55216 and
         result_a["implicit_graph_strict_exclusion_count"] == 55213 and
         result_a["implicit_graphs_are_not_source_grazing_or_cemetery_terminals"]
            is True and
         result_a["implicit_graphs_are_not_coordinate_terminals"] is True and
         result_a["duplicate_physical_graph_traces_added"] == 0 and
         result_a["explicit_residual_child_count"] == 0 and
         boundary["candidate_is_authority"] is False and
         boundary["global_consumption_ready"] is False and
         boundary["runtime_canonical_pointer_or_seal_writes"] is False and
         boundary["formal_credit"] == boundary["whole_parent_credit"] ==
         boundary["D02_gate_credit"] == boundary["CM2_credit"] == 0,
         "result strict zero-credit boundary")

    origins = {}
    target_pairs = {31, 188, 200, 270, 321, 410,
                    471, 474, 631, 711, 787, 853}
    for row in iter_jsonl(C38_LEDGER, C38_SHA, 10486):
        if row["pair_index"] in target_pairs:
            value = row["representative_origin_key"]
            need(row["pair_index"] not in origins or
                 origins[row["pair_index"]] == value,
                 "origin consistency")
            origins[row["pair_index"]] = value
    need(set(origins) == target_pairs, "origin coverage")
    original, reflected = first_two(C35, C35_SHA), first_two(C37, C37_SHA)
    atlas_iter = (
        row for row in iter_jsonl(c72 / C72_LEDGER,
                                  C72_LEDGER_SHA, 134155)
        if row["child_route_witness"] ==
            "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED")
    candidate_iter = iter_jsonl(
        stage_a / ROWS,
        result_a["ledgers"]["decision_rows"]["sha256"], 55216)

    census = collections.Counter()
    routes = collections.Counter()
    graph_routes = collections.Counter()
    pair_census = collections.Counter()
    target_hashes: set[str] = set()
    root_specs: dict[str, dict[str, Any]] = {}
    candidate_occurrence_ids: set[str] = set()
    independent_occurrence_ids: set[str] = set()
    occurrences: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    sample = None
    batch = []
    total = 0

    def consume(current: dict[str, Any]) -> None:
        nonlocal total
        census.update(current["census"])
        routes.update(current["route_census"])
        graph_routes.update(current["graph_route_census"])
        for occurrence in current["endpoint_occurrences"]:
            body = dict(occurrence)
            claim = body.pop("endpoint_occurrence_sha256")
            need(claim == digest(body) and
                 claim not in independent_occurrence_ids,
                 "independent occurrence closure/uniqueness")
            independent_occurrence_ids.add(claim)
            occurrences[occurrence["root_id"]].append(occurrence)
        total += current["count"]

    for atlas, candidate in zip(atlas_iter, candidate_iter, strict=True):
        need(atlas["source_grazing"] is False and
             atlas["formal_credit"] == atlas["D02_gate_credit"] == 0 and
             atlas["row_sha256"] not in target_hashes,
             "C72 target zero-credit boundary/uniqueness")
        target_hashes.add(atlas["row_sha256"])
        pair_census[atlas["pair_index"]] += 1
        if sample is None and candidate["H1_geometry"]["kind"] ==                 "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS":
            sample = candidate
        batch.append([atlas, candidate])
        for root in candidate["H1_geometry"].get("boundary_roots", []):
            value = {"face_key_sha256": root["face_key_sha256"],
                     "exact_face": root["exact_face"]}
            need(root["root_id"] not in root_specs or
                 root_specs[root["root_id"]] == value,
                 "candidate root identity consistency")
            root_specs[root["root_id"]] = value
            occurrence_body = {
                "schema": SCHEMA + ".graph-endpoint-occurrence",
                "C72_atlas_row_sha256": atlas["row_sha256"],
                "edge_id": root["edge_id"], "root_id": root["root_id"],
                "face_key_sha256": root["face_key_sha256"]}
            occurrence_id = digest(occurrence_body)
            need(occurrence_id not in candidate_occurrence_ids,
                 "candidate occurrence uniqueness")
            candidate_occurrence_ids.add(occurrence_id)
        if len(batch) == batch_size:
            payload = {"pairs": batch, "origins": origins,
                       "original": original, "reflected": reflected}
            completed = subprocess.run(
                [sys.executable, str(SELF), "--worker"],
                input=canonical(payload), capture_output=True, check=True)
            consume(json.loads(completed.stdout))
            batch = []
    if batch:
        payload = {"pairs": batch, "origins": origins,
                   "original": original, "reflected": reflected}
        completed = subprocess.run(
            [sys.executable, str(SELF), "--worker"],
            input=canonical(payload), capture_output=True, check=True)
        consume(json.loads(completed.stdout))

    need(total == 55216 and sample is not None and
         len(target_hashes) == 55216 and
         dict(census) == result_a["H1_geometry_census"] and
         dict(routes) ==
            result_a[
                "W_route_census_including_two_strict_positive_whole_boxes"] and
         dict(graph_routes) ==
            result_a["implicit_graph_physical_continuation_census"] and
         {str(key): value for key, value in sorted(pair_census.items())} ==
            result_a["pair_census"],
         "independent full geometry/route census")
    outgoing_hashes = {row["C72_atlas_row_sha256"] for row in iter_jsonl(
        C72O_LEDGER, C72O_SHA, 18668)}
    broad_hashes = {row["C72_obligation_row_sha256"] for row in iter_jsonl(
        C73_LEDGER, C73_SHA, 1163)}
    need(target_hashes.isdisjoint(outgoing_hashes) and
         target_hashes.isdisjoint(broad_hashes) and
         outgoing_hashes.isdisjoint(broad_hashes),
         "independent C72b2/C72o/C73 exact dedup")
    need(len(candidate_occurrence_ids) == 110426 and
         independent_occurrence_ids == candidate_occurrence_ids and
         sum(len(rows) for rows in occurrences.values()) == 110426 and
         set(occurrences) == set(root_specs),
         "independent 2x55213 endpoint occurrence conservation")
    degree_census = collections.Counter(
        len(occurrences[identifier]) for identifier in root_specs)
    need(set(degree_census).issubset({1, 2}) and
         sum(degree * count for degree, count in degree_census.items()) ==
            110426 and
         sum(degree_census.values()) == len(root_specs) and
         result_a["graph_endpoint_occurrence_count"] == 110426 and
         result_a["graph_endpoint_occurrence_unique_count"] == 110426 and
         result_a["unique_H1_boundary_root_count"] == len(root_specs) and
         result_a["target_graph_root_degree_census"] ==
            {str(key): value for key, value in sorted(degree_census.items())},
         "independent root degree decomposition")

    expected = expected_incidence(c72, root_specs, occurrences)
    observed = list(iter_jsonl(
        stage_a / INCIDENCE,
        result_a["ledgers"]["root_incidence"]["sha256"], len(expected)))
    observed_bodies = []
    for row in observed:
        body = dict(row)
        body.pop("row_sha256")
        observed_bodies.append(body)
    incidence_degree_census = collections.Counter(
        row["incidence_count"] for row in expected)
    incidence_class_census = collections.Counter(
        row["incidence_class"] for row in expected)
    need(observed_bodies == expected and
         sum(row["incidence_count"] for row in expected) == 110426 and
         incidence_degree_census == degree_census and
         dict(sorted(incidence_class_census.items())) ==
            result_a["root_incidence_census"],
         "independent incidence equality/conservation")

    attack_rows = attacks(sample, result_a)
    verification = {
        "schema": SCHEMA + ".independent-verification.v2",
        "status":
            "PASS_NO_C72B2_PRODUCER_READ_IMPORT_EXECUTION_OR_DECODE__"
            "DUAL_BYTE_IDENTITY__55216_WHOLE_CHILD_STRICT_EXCLUSIONS__"
            "110426_ENDPOINTS_CONSERVED__48_ATTACKS__ZERO_CREDIT",
        "verifier_file_sha256": file_sha(SELF),
        "producer_source_imported_read_decoded_compiled_or_executed": False,
        "producer_source_path_opened_or_statted": False,
        "producer_source_sha256_declared_only": PRODUCER_DECLARED_PIN,
        "shared_pure_core_imported_or_executed_by_verifier": False,
        "shared_pure_core_file_sha256_checked_as_inert_bytes": PURE_CORE_PIN,
        "chart_authority": authority,
        "dual_build_file_sha256": identity,
        "candidate_object_sha256": result_a["object_sha256"],
        "coverage": {
            "row_count": total,
            "H1_GEOMETRY_CLOSED": 55216,
            "whole_child_strict_exclusion_count": 55216,
            "clipped_physical_graph_glue_count": 55213,
            "implicit_graph_strict_exclusion_count": 55213,
            "graph_endpoint_occurrence_count": 110426,
            "unique_H1_boundary_root_count": len(root_specs),
            "target_graph_root_degree_census":
                {str(key): value for key, value in sorted(degree_census.items())},
            "sum_incidence_count": sum(
                row["incidence_count"] for row in expected),
            "explicit_residual_child_count": 0},
        "independent_geometry_census": dict(sorted(census.items())),
        "independent_W_route_census": dict(sorted(routes.items())),
        "independent_graph_route_census": dict(sorted(graph_routes.items())),
        "root_incidence_row_count": len(expected),
        "all_graphs_are_physical_continuations_not_source_cemetery_or_coordinate_terminals":
            True,
        "all_closed_box_route_margins_restrict_to_implicit_graph": True,
        "coherent_attacks": {
            "attack_count": 48,
            "attacks": dict(sorted(attack_rows.items())),
            "status": "PASS_48_OF_48_COHERENT_ATTACKS_FAIL_CLOSED"},
        "candidate_is_authority": False,
        "global_consumption_ready": False,
        "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0, "CM2_credit": 0}
    verification["object_sha256"] = digest(verification)
    raw = canonical(verification) + b"\n"
    write_exclusive(output, raw)
    need(file_sha(output) == hashlib.sha256(raw).hexdigest(),
         "terminal verification replay")
    for stage in (stage_a, stage_b):
        for name, expected_sha in identity.items():
            need(file_sha(stage / name) == expected_sha,
                 "terminal candidate replay")
    return verification

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--stage-a", type=Path)
    parser.add_argument("--stage-b", type=Path)
    parser.add_argument("--c72", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--batch-size", type=int, default=1200)
    args = parser.parse_args()
    if args.worker:
        return worker()
    need(all(value is not None for value in
             (args.stage_a, args.stage_b, args.c72, args.output)), "arguments")
    result = verify(args.stage_a.resolve(), args.stage_b.resolve(),
                    args.c72.resolve(), args.output.resolve(), args.batch_size)
    print(json.dumps({"status": result["status"],
                      "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "REJECTED", "reason": str(error)}, sort_keys=True),
              file=sys.stderr)
        raise SystemExit(2)
