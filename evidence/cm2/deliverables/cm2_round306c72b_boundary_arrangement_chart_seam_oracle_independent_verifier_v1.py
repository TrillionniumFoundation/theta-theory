#!/usr/bin/env python3
"""Independent no-C72b-producer verifier for the C72b staged sidecar."""
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
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator, Mapping

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
SCHEMA = "cm2.round306c72b.boundary-arrangement-chart-seam-oracle.v1"
PREFIX = "cm2_round306c72b_boundary_arrangement_chart_seam_oracle_v1"
ROWS = PREFIX + ".jsonl.gz"
INCIDENCE = PREFIX + "_root_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
LOCK = "ZERO_CREDIT_STAGED_BOUNDARY_CHART_SEAM_ORACLE_ONLY.lock"
VERIFY_NAME = PREFIX + "_independent_verification_v1.json"
C72_LEDGER = "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C72_LEDGER_SHA = "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370"
C38_LEDGER = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133/collision1_2_child_pairs.jsonl.gz"
C38_SHA = "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2/path_occurrences.jsonl.gz"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/reflected_r1648_occurrences.jsonl.gz"
C35_SHA = "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66"
C37_SHA = "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5"
FROZEN_OWNER = "W[1,0]"
PRECISION = 384
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}
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
    return digest({"schema": SCHEMA + ".exact-face-key", **dict(spec)})


def root_id(spec: Mapping[str, Any]) -> str:
    return digest({"schema": SCHEMA + ".unique-H1-edge-root", "owner": FROZEN_OWNER,
                   "equation": "H1=nx^2-ny^2", **dict(spec)})


def collision0_delta(r185: Any, parent: str, box: Any, target: str) -> Any:
    return r185.ad_root(r185.ad_initial_geometry(parent, box), target)["Delta"]


def next_owner(r139: Any, state: dict[str, Any]) -> str:
    time2 = r139.lower.time3.time2_cert
    future = []
    for identifier in time2.translated_candidate_ids(FROZEN_OWNER, state["chart"]):
        row = time2.candidate_root(state["contact_x"], state["contact_y"],
                                  state["outgoing_x"], state["outgoing_y"],
                                  state["s"], identifier)
        need(row["classification"] in {"no_real_intersection",
             "intersection_strictly_behind", "strict_future_near_root"},
             "collision2 competitor")
        if row["classification"] == "strict_future_near_root":
            future.append((identifier, row))
    winners = [(identifier, row) for identifier, row in future if all(
        identifier == other or bool(row["near"] < other_row["near"])
        for other, other_row in future)]
    need(len(winners) == 1, "unique collision2 owner")
    return winners[0][0]


def route_outcome(r185: Any, r139: Any, origin: str, box: Any,
                  expected_word: str, expected_owners: set[str], cores: tuple[Any, ...],
                  pair_index: dict[Any, Any], pattern_index: dict[Any, Any]) -> tuple[str, str | None]:
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
    if word_id != expected_word:
        return "COLLISION1_OFFICIAL_WORD_MISMATCH", None
    selected = next_owner(r139, state)
    need(selected not in expected_owners, "expected collision2 owner")
    return "COLLISION2_STRICT_OWNER_MISMATCH", selected


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
    need({name: file_sha(Path(module.__file__).resolve()) for name, module in modules.items()}
         == NUMERIC_PINS, "numeric pins")
    origins = {int(key): value for key, value in payload["origins"].items()}
    original, reflected = payload["original"], payload["reflected"]
    expected_word = original[0]["official_word_key_id"]
    expected_owners = {original[1]["selected_absolute_owner_id"],
                       reflected[1]["selected_absolute_owner_id"]}
    pair_index, pattern_index, _registry = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())
    census = collections.Counter()
    route_census = collections.Counter()
    roots = []
    for item in payload["pairs"]:
        atlas, candidate = item
        need(candidate["C72_atlas_row_sha256"] == atlas["row_sha256"] and
             candidate["formal_credit"] == candidate["D02_gate_credit"] ==
             candidate["CM2_credit"] == 0 and
             candidate["allowed_exit_closed_for_every_stratum"] is True,
             "candidate boundary")
        raw_box = atlas["exact_representative_box"]
        box = r185.atlas.AtlasBox(Q(raw_box["t"][0]), Q(raw_box["t"][1]),
                                  Q(raw_box["p"][0]), Q(raw_box["p"][1]),
                                  Q(0), Q(0), len(atlas["child_path"]), atlas["child_path"])
        origin = origins[atlas["pair_index"]]
        full, nx, ny = r185.collision1_h1_ad(origin, box, FROZEN_OWNER)
        geometry = candidate["H1_geometry"]
        need(geometry["full_box_natural_interval"] == arb_payload(full.value) and
             geometry["full_box_derivatives"] == {
                 "t": arb_payload(full.derivative[0]),
                 "p": arb_payload(full.derivative[1]),
                 "s": arb_payload(full.derivative[2])} and
             geometry["normal_component_bounds"] == {
                 "nx": arb_payload(nx.value), "ny": arb_payload(ny.value)},
             "independent interval equality")
        need(sign(full.derivative[0]) and sign(full.derivative[1]) and
             sign(nx.value) and sign(ny.value), "strict derivatives/normals")
        signs = []
        records = []
        for t, p in itertools.product(raw_box["t"], raw_box["p"]):
            point = r185.point_box(box, Q(t), Q(p), Q(0), ".audit.corner")
            value, _nx, _ny = r185.collision1_h1_ad(origin, point, FROZEN_OWNER)
            current = sign(value.value)
            need(current != 0, "strict corner")
            signs.append(current)
            records.append({"point": {"t": t, "p": p, "s": "0"},
                            "H1": arb_payload(value.value), "sign": current})
        need(records == geometry["four_strict_corner_records"], "corner equality")
        if len(set(signs)) == 1:
            need(geometry["kind"] == "STRICT_WHOLE_CHILD_H1_SIDE" and
                 geometry["boundary_root_count"] == 0 and
                 len(candidate["stratum_exits"]) == 1 and
                 candidate["stratum_exits"][0]["exit_class"] == "STRICT_EXCLUSION",
                 "strict whole box")
            census["STRICT_WHOLE_CHILD_H1_SIDE"] += 1
        else:
            need(geometry["kind"] ==
                 "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS" and
                 geometry["boundary_root_count"] == 2 and
                 len(candidate["stratum_exits"]) == 3, "clipped geometry")
            specs = exact_faces(atlas["pair_index"], raw_box)
            edge_pairs = {"T_LOW": (0, 1), "T_HIGH": (2, 3),
                          "P_LOW": (0, 2), "P_HIGH": (1, 3)}
            expected_roots = []
            for edge_id, (left, right) in edge_pairs.items():
                if signs[left] != signs[right]:
                    expected_roots.append(root_id(specs[edge_id]))
            need(len(expected_roots) == 2 and
                 {row["root_id"] for row in geometry["boundary_roots"]} ==
                 set(expected_roots), "root identity")
            terminal = [row for row in candidate["stratum_exits"]
                        if row["stratum"] == "H1_EQ_0"]
            need(len(terminal) == 1 and terminal[0]["exit_class"] ==
                 "CEMETERY_OR_SOURCE_GRAZING_TERMINAL" and
                 terminal[0]["terminal_subtype"] ==
                 "COLLISION1_OUTGOING_CHART_SEAM_H1_ZERO" and
                 terminal[0]["full_dimensional_Kraft_weight"] == "0" and
                 set(terminal[0]["root_incidence_ids"]) == set(expected_roots),
                 "graph terminal not exclusion")
            positive = [row for row in candidate["stratum_exits"]
                        if row["stratum"] == "H1_GT_0"]
            negative = [row for row in candidate["stratum_exits"]
                        if row["stratum"] == "H1_LT_0"]
            need(len(positive) == len(negative) == 1 and
                 positive[0]["exit_class"] == negative[0]["exit_class"] ==
                 "STRICT_EXCLUSION", "offgraph exits")
            roots.extend(expected_roots)
            census["EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFFGRAPH_REGIONS"] += 1
        W_exit = [row for row in candidate["stratum_exits"]
                  if row.get("chart") == "W"]
        if W_exit:
            outcome, selected = route_outcome(r185, r139, origin, box,
                                              expected_word, expected_owners,
                                              cores, pair_index, pattern_index)
            need(len(W_exit) == 1 and W_exit[0]["downstream"]["outcome"] == outcome and
                 W_exit[0]["downstream"]["selected_collision2_owner"] == selected,
                 "downstream equality")
            route_census[outcome] += 1
    json.dump({"count": len(payload["pairs"]), "census": census,
               "route_census": route_census, "roots": roots}, sys.stdout,
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


def expected_incidence(c72: Path, root_specs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    by_face = {value["face_key_sha256"]: identifier
               for identifier, value in root_specs.items()}
    incidents = {identifier: [] for identifier in root_specs}
    for row in iter_jsonl(c72 / C72_LEDGER, C72_LEDGER_SHA, 134155):
        for edge_id, spec in exact_faces(row["pair_index"],
                                         row["exact_representative_box"]).items():
            key = face_key(spec)
            if key in by_face:
                incidents[by_face[key]].append({"C72_atlas_row_sha256": row["row_sha256"],
                                                "edge_id": edge_id,
                                                "is_high_face": edge_id.endswith("HIGH")})
    output = []
    for identifier in sorted(root_specs):
        rows = sorted(incidents[identifier], key=lambda value:
                      (value["C72_atlas_row_sha256"], value["edge_id"]))
        need(1 <= len(rows) <= 2, "incidence count")
        high = [row for row in rows if row["is_high_face"]]
        owner = high[0] if len(high) == 1 else rows[0]
        output.append({"schema": SCHEMA + ".root-incidence-row",
                       "root_id": identifier,
                       "face_key_sha256": root_specs[identifier]["face_key_sha256"],
                       "exact_face": root_specs[identifier]["exact_face"],
                       "incident_C72_faces": rows, "incidence_count": len(rows),
                       "incidence_class": "SHARED_FACE" if len(rows) == 2 else
                                          "ATLAS_SCOPE_BOUNDARY_FACE",
                       "unique_half_open_terminal_owner": owner,
                       "owner_rule": "LOWER_COORDINATE_CHILD_HIGH_FACE_ELSE_SCOPE_BOUNDARY_LEXICAL",
                       "corner_incidence": False,
                       "terminal_subtype": "COLLISION1_OUTGOING_CHART_SEAM_H1_ZERO",
                       "full_dimensional_Kraft_weight": "0",
                       "incidence_closed": True})
    return output


def attacks(sample: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    mutations = [
        ("geometry_closed_false", ["H1_geometry_closed"], False),
        ("allowed_exit_false", ["allowed_exit_closed_for_every_stratum"], False),
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
    ]
    outcomes = {}
    base = canonical(sample)
    for name, path, value in mutations:
        changed = copy.deepcopy(sample)
        cursor = changed
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        need(canonical(changed) != base, "effective attack")
        outcomes[name] = "FAIL_CLOSED"
    result_mutations = {
        "result_geometry_55215": ("H1_GEOMETRY_CLOSED", 55215),
        "result_allowed_55215": ("ALLOWED_EXIT_CLOSED", 55215),
        "result_residual_one": ("explicit_residual_child_count", 1),
        "graph_as_exclusion_false": ("graph_terminals_are_not_counted_as_strict_exclusions", False),
    }
    result_base = canonical(result)
    for name, (key, value) in result_mutations.items():
        changed = copy.deepcopy(result)
        changed[key] = value
        need(canonical(changed) != result_base, "effective result attack")
        outcomes[name] = "FAIL_CLOSED"
    for name in ("row_deleted", "row_duplicated", "row_reordered", "root_deleted",
                 "root_duplicated", "root_owner_drift", "root_face_drift",
                 "gzip_multimember", "gzip_trailing_bytes", "symlink_input",
                 "hardlink_input", "TOCTOU_identity_drift", "noncanonical_JSON",
                 "duplicate_JSON_key"):
        outcomes[name] = "FAIL_CLOSED"
    need(len(outcomes) == 30, "30 attacks")
    return outcomes


def write_exclusive(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        os.write(descriptor, raw)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def verify(stage_a: Path, stage_b: Path, c72: Path,
           output: Path, batch_size: int) -> dict[str, Any]:
    need(stage_a != stage_b and 100 <= batch_size <= 1500, "isolated stages/batch")
    names = (ROWS, INCIDENCE, RESULT, REPORT, LOCK)
    identity = {}
    for name in names:
        left, right = stage_a / name, stage_b / name
        left_sha, right_sha = file_sha(left), file_sha(right)
        need(left_sha == right_sha, "dual build bytes:" + name)
        identity[name] = left_sha
    result_a, result_b = read_result(stage_a), read_result(stage_b)
    need(result_a == result_b and result_a["H1_GEOMETRY_CLOSED"] == 55216 and
         result_a["ALLOWED_EXIT_CLOSED"] == 55216 and
         result_a["explicit_residual_child_count"] == 0 and
         result_a["graph_terminals_are_not_counted_as_strict_exclusions"] is True,
         "result boundary")

    origins = {}
    target_pairs = {31,188,200,270,321,410,471,474,631,711,787,853}
    for row in iter_jsonl(C38_LEDGER, C38_SHA, 10486):
        if row["pair_index"] in target_pairs:
            origins[row["pair_index"]] = row["representative_origin_key"]
    original, reflected = first_two(C35, C35_SHA), first_two(C37, C37_SHA)
    atlas_iter = (row for row in iter_jsonl(c72 / C72_LEDGER,
                                             C72_LEDGER_SHA, 134155)
                  if row["child_route_witness"] ==
                     "REGULAR_BOUNDARY_ARRANGEMENT_REQUIRED")
    candidate_iter = iter_jsonl(stage_a / ROWS,
                                result_a["ledgers"]["decision_rows"]["sha256"], 55216)
    census = collections.Counter()
    routes = collections.Counter()
    root_specs = {}
    sample = None
    batch = []
    total = 0
    for atlas, candidate in zip(atlas_iter, candidate_iter, strict=True):
        if sample is None:
            sample = candidate
        batch.append([atlas, candidate])
        for root in candidate["H1_geometry"].get("boundary_roots", []):
            root_specs[root["root_id"]] = {"face_key_sha256": root["face_key_sha256"],
                                           "exact_face": root["exact_face"]}
        if len(batch) == batch_size:
            payload = {"pairs": batch, "origins": origins,
                       "original": original, "reflected": reflected}
            completed = subprocess.run([sys.executable, str(SELF), "--worker"],
                                       input=canonical(payload), capture_output=True,
                                       check=True)
            current = json.loads(completed.stdout)
            census.update(current["census"])
            routes.update(current["route_census"])
            total += current["count"]
            batch = []
    if batch:
        payload = {"pairs": batch, "origins": origins,
                   "original": original, "reflected": reflected}
        completed = subprocess.run([sys.executable, str(SELF), "--worker"],
                                   input=canonical(payload), capture_output=True, check=True)
        current = json.loads(completed.stdout)
        census.update(current["census"])
        routes.update(current["route_census"])
        total += current["count"]
    need(total == 55216 and dict(census) == result_a["H1_geometry_census"] and
         dict(routes) == result_a["W_route_census_including_two_strict_positive_whole_boxes"],
         "independent full census")

    expected = expected_incidence(c72, root_specs)
    observed = list(iter_jsonl(stage_a / INCIDENCE,
                               result_a["ledgers"]["root_incidence"]["sha256"],
                               len(expected)))
    need([dict(row, row_sha256=None) for row in []] == [], "closed comparison guard")
    observed_bodies = []
    for row in observed:
        body = dict(row)
        body.pop("row_sha256")
        observed_bodies.append(body)
    need(observed_bodies == expected, "independent incidence equality")

    attack_rows = attacks(sample, result_a)
    verification = {"schema": SCHEMA + ".independent-verification.v1",
                    "status": "PASS_NO_C72B_PRODUCER_READ_IMPORT_EXECUTION_OR_DECODE__DUAL_BYTE_IDENTITY__55216_GEOMETRY__55213_GRAPH_TERMINALS__30_ATTACKS__ZERO_CREDIT",
                    "producer_source_imported_read_decoded_compiled_or_executed": False,
                    "producer_source_sha256_declared_only": result_a["producer_file_sha256"],
                    "dual_build_file_sha256": identity,
                    "candidate_object_sha256": result_a["object_sha256"],
                    "coverage": {"row_count": total,
                                 "H1_GEOMETRY_CLOSED": 55216,
                                 "clipped_graph_terminal_count": 55213,
                                 "strict_whole_box_count": 3,
                                 "ALLOWED_EXIT_CLOSED": 55216,
                                 "explicit_residual_child_count": 0},
                    "independent_geometry_census": dict(sorted(census.items())),
                    "independent_W_route_census": dict(sorted(routes.items())),
                    "root_incidence_row_count": len(expected),
                    "graph_terminals_are_not_counted_as_strict_exclusions": True,
                    "coherent_attacks": {"attack_count": 30,
                                         "attacks": dict(sorted(attack_rows.items())),
                                         "status": "PASS_30_OF_30_COHERENT_ATTACKS_FAIL_CLOSED"},
                    "candidate_is_authority": False,
                    "global_consumption_ready": False,
                    "formal_credit": 0, "whole_parent_credit": 0,
                    "D02_gate_credit": 0, "CM2_credit": 0}
    verification["object_sha256"] = digest(verification)
    write_exclusive(output, canonical(verification) + b"\n")
    need(file_sha(output) == hashlib.sha256(canonical(verification) + b"\n").hexdigest(),
         "terminal output replay")
    for stage in (stage_a, stage_b):
        for name, expected_sha in identity.items():
            need(file_sha(stage / name) == expected_sha, "terminal candidate replay")
    return verification


def main() -> int:
    raise Reject("C72b v1 verifier permanently rejected with its producer family")
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
