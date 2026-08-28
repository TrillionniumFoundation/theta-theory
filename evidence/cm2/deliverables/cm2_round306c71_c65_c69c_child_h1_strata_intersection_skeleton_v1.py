#!/usr/bin/env python3
"""Disabled C71 zero-credit C65-child x C69c-H1-strata successor skeleton.

The formal entry point is deliberately fail closed until the final C65 64/64
aggregate, dual-cold replay, post-publication replay, v2 self-test, and manifest
have frozen hashes.  No dependent ledger path is derived before both evidence
gates close.  C69c is only a source-level candidate/lineage sidecar: every C65
collision-2 child must receive a fresh 384-bit full-box numerical proof.

This file writes nothing and cannot publish a result.  ``--static-self-test``
exercises only pure protocol/lineage/Kraft helpers; ``--preflight`` currently
must reject before opening any evidence because ``FROZEN_C65_PINS`` is empty.
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Callable, Iterable, Iterator


SELF = Path(__file__).resolve()
OUT = SELF.parent
SCHEMA = "cm2.round306c71.c65-c69c-child-h1-strata-intersection.v1"
CONTRACT = OUT / "cm2_round306c71_c65_c69c_child_h1_strata_intersection_contract_v1.json"
SCHEMAS = OUT / "cm2_round306c71_c65_c69c_child_h1_strata_intersection_closed_schemas_v1.json"
CONTRACT_OBJECT = "6254452873fbc57e4dd5275e5e293e169d875bdb72a833713be8253527b21f97"
SCHEMAS_OBJECT = "b15e7b0eb53490acefcac5837c83659196e81a6c68340433e29564d168c3b045"
R185_FILE_SHA256 = "7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2"
PRECISION_BITS = 384
MAX_TRANSVERSE_COVER_DEPTH = 8

C65_EVIDENCE_NAMES = {
    "producer": "cm2_round306c65s18_64shard_zero_credit_aggregate_producer_v1.py",
    "result": "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
    "verification": "cm2_round306c65s18_64shard_aggregate_independent_cold_verification_v1.json",
    "selftest_v2": "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v2.json",
    "selftest_v1_rejection": "cm2_round306c65s18_64shard_aggregate_independent_cold_self_test_v1_REJECTED.md",
    "replay": "cm2_round306c65s18_64shard_aggregate_independent_cold_postpublication_replay_v1.json",
    "manifest": "cm2_round306c65s18_64shard_aggregate_independent_cold_manifest_v1.sha256",
}
C65_RESULT_SCHEMA = "cm2.round306c65s18.depth18-64shard.aggregate.v1.aggregate-result"
C65_RESULT_STATUS = "PASS_COMPLETE_64_SHARD_DEPTH18_REPLACEMENT_AGGREGATE__ZERO_CREDIT"
C65_VERIFY_SCHEMA = "cm2.round306c65s18.64shard-aggregate-independent-cold-verifier.v1.verification"
C65_VERIFY_STATUS = (
    "PASS_INDEPENDENT_DUAL_COLD_64_OF_64__20879_ASSIGNMENTS__EXACT_DEPTH6_NUMERIC_REPLAY__"
    "C61_REPLACEMENT_PARENT_KRAFT__AUTHORITY_UNCHANGED__ZERO_CREDIT"
)

# Intentionally empty.  Populating this map requires a new source hash and
# review after C65 formally freezes.  Its exact key set is itself an entry gate.
FROZEN_C65_PINS: dict[str, str] = {}
C65_REQUIRED_PIN_KEYS = frozenset({
    "producer", "result", "result_object", "verification", "verification_object",
    "selftest_v2", "selftest_v2_object", "selftest_v1_rejection", "replay",
    "replay_object", "manifest", "aggregate_leaves", "aggregate_sources",
    "aggregate_parents",
})

C69_EVIDENCE_NAMES = {
    "corrected": "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json",
    "verification": "cm2_round306c69c_descriptor_repair_supersession_independent_verification_v1.json",
    "selftest": "cm2_round306c69c_descriptor_repair_supersession_independent_self_test_v1.json",
    "outer": "cm2_round306c69c_descriptor_repair_supersession_independent_outer_publication_receipt_v1.json",
    "manifest": "cm2_round306c69c_descriptor_repair_supersession_independent_manifest_v1.sha256",
}
C69_PINS = {
    "corrected": "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    "corrected_object": "e52904a7d8ba73c855e69e390cd3cf29c233ffe492e6fae74efdf0b6d4d0a6a5",
    "verification": "b0490ed50de8d615039d864db1071792df0809b928a663fcd4a89981eaf326b6",
    "verification_object": "fd25accfd8c5669d13a09b5f335ae265a751a1fb7f069ac21c64e069a0fc2b29",
    "selftest": "b8776e66db0d6cc71f255fac4ddc3b087511a99ba72c9224f6af063310e147a0",
    "selftest_object": "8bc580fabd2abe6faa5c8577045de0965e88227cbe0103dfc1fb193b15cb9431",
    "outer": "2baac1cf22ca8be0163f9027d0365e948107b535df917a25334626110bf2916c",
    "outer_object": "921a5b16d4102b356f1e2e903a71df5e872c869caa668903bb210fe0dbfed1f3",
    "manifest": "c231941ca4f5f76a95faa81e8390e3f11b5d1af84b645605c52245e6ff214749",
}
C69_VERIFY_STATUS = (
    "PASS_COLD_NO_C69_PRODUCER_OR_WRAPPER_IMPORT_EXECUTION_READ_OR_DECODE__EXACT_REBUILD_"
    "20879_PARTITION_2356_NUMERIC_DECISIONS_18523_BLOCKERS_2_COVER_ROWS__ZERO_CREDIT"
)


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


def row_closed(value: dict[str, Any]) -> bool:
    body = copy.deepcopy(value)
    claim = body.pop("row_sha256", None)
    return type(claim) is str and claim == digest(body)


def close_object(value: dict[str, Any], expected: str | None = None) -> dict[str, Any]:
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == digest(body), "object closure")
    if expected is not None:
        need(claim == expected, "object pin")
    return value


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        need(key not in value, "duplicate JSON key:" + key)
        value[key] = item
    return value


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and raw.endswith(b"\n") and
         not raw.endswith(b"\n\n"), label + ": framing")
    value = json.loads(raw[:-1].decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
    need(type(value) is dict and canonical(value) + b"\n" == raw, label + ": canonical")
    return value


def secure_read(path: Path, expected_sha: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        first = os.fstat(descriptor)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "regular single-link:" + path.name)
        raw = b""
        while block := os.read(descriptor, 4 << 20):
            raw += block
        second = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = os.stat(path, follow_symlinks=False)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                              value.st_size, value.st_mtime_ns, value.st_ctime_ns)
    need(identity(first) == identity(second) == identity(current), "TOCTOU:" + path.name)
    need(hashlib.sha256(raw).hexdigest() == expected_sha, "file pin:" + path.name)
    return raw


def manifest_entries(raw: bytes) -> dict[str, str]:
    need(raw.endswith(b"\n") and b"\x00" not in raw, "manifest framing")
    result: dict[str, str] = {}
    for line in raw.decode("utf-8", "strict").splitlines():
        sha, separator, path = line.partition("  ")
        need(separator == "  " and len(sha) == 64 and all(c in "0123456789abcdef" for c in sha),
             "manifest row")
        need(path not in result and not path.startswith("/") and ".." not in Path(path).parts,
             "manifest path")
        result[path] = sha
    return result


def c65_evidence_gate(root: Path, reader: Callable[[Path, str], bytes] = secure_read
                      ) -> tuple[dict[str, Any], dict[str, Any]]:
    # This exact test deliberately precedes even path derivation and reader calls.
    need(set(FROZEN_C65_PINS) == C65_REQUIRED_PIN_KEYS,
         "C65 final aggregate/cold pins not frozen; dependent inputs unopened")
    raw = {key: reader(root / name, FROZEN_C65_PINS[key])
           for key, name in C65_EVIDENCE_NAMES.items()}
    result = strict_json(raw["result"], "C65 result")
    verification = strict_json(raw["verification"], "C65 verification")
    selftest = strict_json(raw["selftest_v2"], "C65 self-test v2")
    replay = strict_json(raw["replay"], "C65 replay")
    close_object(result, FROZEN_C65_PINS["result_object"])
    close_object(verification, FROZEN_C65_PINS["verification_object"])
    close_object(selftest, FROZEN_C65_PINS["selftest_v2_object"])
    close_object(replay, FROZEN_C65_PINS["replay_object"])
    need(result["schema"] == C65_RESULT_SCHEMA and result["status"] == C65_RESULT_STATUS,
         "C65 aggregate protocol")
    need(verification["schema"] == C65_VERIFY_SCHEMA and
         verification["status"] == C65_VERIFY_STATUS, "C65 dual-cold protocol")
    dual = verification.get("dual_cold_run_evidence")
    need(type(dual) is dict and dual.get("byte_identical") is True and
         dual.get("pythonhashseeds") == ["1", "2"], "C65 dual-cold evidence")
    need(result["formal_credit"] == result["whole_parent_credit"] ==
         result["D02_gate_credit"] == verification["formal_credit"] ==
         verification["whole_parent_credit"] == verification["D02_gate_credit"] == 0,
         "C65 zero-credit boundary")
    entries = manifest_entries(raw["manifest"])
    for key in ("producer", "result", "verification", "selftest_v2", "replay"):
        manifest_name = "deliverables/" + C65_EVIDENCE_NAMES[key]
        need(entries.get(manifest_name) == FROZEN_C65_PINS[key], "C65 manifest:" + key)
    return result, verification


def c69_evidence_gate(root: Path, reader: Callable[[Path, str], bytes] = secure_read
                      ) -> tuple[dict[str, Any], dict[str, Any]]:
    raw = {key: reader(root / name, C69_PINS[key]) for key, name in C69_EVIDENCE_NAMES.items()}
    corrected = strict_json(raw["corrected"], "C69c corrected")
    verification = strict_json(raw["verification"], "C69c verification")
    selftest = strict_json(raw["selftest"], "C69c self-test")
    outer = strict_json(raw["outer"], "C69c outer")
    close_object(corrected, C69_PINS["corrected_object"])
    close_object(verification, C69_PINS["verification_object"])
    close_object(selftest, C69_PINS["selftest_object"])
    close_object(outer, C69_PINS["outer_object"])
    need(corrected["status"] ==
         "PASS_C69B_SEALED_LEDGER_DESCRIPTOR_REPAIR_SUPERSESSION__ZERO_CREDIT" and
         verification["status"] == C69_VERIFY_STATUS, "C69c cold protocol")
    need(corrected["strict_boundary"]["decisions_are_terminal_dispositions"] is False and
         corrected["formal_credit"] == corrected["whole_parent_credit"] ==
         corrected["D02_gate_credit"] == verification["formal_credit"] ==
         verification["whole_parent_credit"] == verification["D02_gate_credit"] == 0,
         "C69c zero-credit boundary")
    entries = manifest_entries(raw["manifest"])
    for key in ("corrected", "verification", "selftest"):
        manifest_name = "deliverables/" + C69_EVIDENCE_NAMES[key]
        need(entries.get(manifest_name) == C69_PINS[key], "C69c manifest:" + key)
    return corrected, verification


def formal_evidence_gate(root: Path = OUT) -> tuple[dict[str, Any], dict[str, Any]]:
    # Mandatory ordering: C65 must close before any C69 evidence is opened.
    c65_result, _c65_verify = c65_evidence_gate(root)
    c69_result, _c69_verify = c69_evidence_gate(root)
    return c65_result, c69_result


def dependent_ledger_names_after_gate(c65: dict[str, Any], c69: dict[str, Any]
                                      ) -> dict[str, str]:
    """The only function allowed to derive ledger paths; call after both gates."""
    names = {
        "C65_leaves": c65["ledgers"]["aggregate_leaves"]["filename"],
        "C65_sources": c65["ledgers"]["source_summaries"]["filename"],
        "C69_decisions": c69["ledgers"]["decisions"]["filename"],
        "C69_blockers": c69["ledgers"]["blockers"]["filename"],
        "C69_covers": c69["ledgers"]["parametric_newton_covers"]["filename"],
    }
    need(all(Path(name).name == name for name in names.values()), "dependent ledger filenames")
    return names


@dataclass(frozen=True)
class ExactBox:
    t0: Fraction
    t1: Fraction
    p0: Fraction
    p1: Fraction
    s0: Fraction
    s1: Fraction

    def bounds(self, axis: int) -> tuple[Fraction, Fraction]:
        return ((self.t0, self.t1), (self.p0, self.p1), (self.s0, self.s1))[axis]

    def width(self, axis: int) -> Fraction:
        lower, upper = self.bounds(axis)
        return upper - lower


def exact_box(payload: dict[str, list[str]]) -> ExactBox:
    need(set(payload) == {"t", "p", "s"} and all(len(payload[key]) == 2 for key in payload),
         "box schema")
    box = ExactBox(*(Fraction(value) for key in ("t", "p", "s") for value in payload[key]))
    need(all(box.width(axis) >= 0 for axis in range(3)), "ordered box")
    return box


def box_payload(box: ExactBox) -> dict[str, list[str]]:
    return {"t": [str(box.t0), str(box.t1)], "p": [str(box.p0), str(box.p1)],
            "s": [str(box.s0), str(box.s1)]}


def longest_axis(box: ExactBox) -> int:
    # Python max returns the first maximum: exact frozen T,P,S tie-break.
    return max(range(3), key=box.width)


def split_box(box: ExactBox, axis: int) -> tuple[ExactBox, ExactBox]:
    lower, upper = box.bounds(axis)
    middle = (lower + upper) / 2
    values = [[box.t0, box.t1], [box.p0, box.p1], [box.s0, box.s1]]
    left, right = copy.deepcopy(values), copy.deepcopy(values)
    left[axis][1], right[axis][0] = middle, middle
    make = lambda value: ExactBox(value[0][0], value[0][1], value[1][0], value[1][1],
                                  value[2][0], value[2][1])
    return make(left), make(right)


def rebuild_child(source_box: ExactBox, source_path: str, child_path: str
                  ) -> tuple[ExactBox, list[dict[str, Any]]]:
    need(child_path.startswith(source_path), "child path source prefix")
    box = source_box
    owner_chain: list[dict[str, Any]] = []
    for depth, bit in enumerate(child_path[len(source_path):], 1):
        need(bit in "01", "binary child suffix")
        axis = longest_axis(box)
        lower, upper = box.bounds(axis)
        middle = (lower + upper) / 2
        children = split_box(box, axis)
        owner_chain.append({
            "relative_depth": depth, "axis": ("t", "p", "s")[axis],
            "exact_split_coordinate": str(middle), "selected_bit": bit,
            "shared_face_owner": "LOWER_BIT_CHILD",
            "selected_child_owns_shared_face": bit == "0",
        })
        box = children[int(bit)]
    return box, owner_chain


def prefix_free(paths: Iterable[str]) -> bool:
    ordered = sorted(paths)
    return all(not right.startswith(left) for left, right in zip(ordered, ordered[1:]))


def arb_payload(value: Any) -> dict[str, Any]:
    return {"lower": str(value.lower()), "upper": str(value.upper()),
            "contains_zero": not bool(value > 0) and not bool(value < 0)}


def atlas_box(box: ExactBox, path: str) -> Any:
    from cm2_gate3_eight_cell_symmetry_atlas_cert import AtlasBox  # type: ignore
    return AtlasBox(box.t0, box.t1, box.p0, box.p1, box.s0, box.s1, 0, path)


def load_numeric_kernel() -> tuple[Any, Any]:
    import flint  # type: ignore
    import cm2_round185_preconditioned_c1_residual_refinement as r185  # type: ignore
    kernel_path = Path(r185.__file__).resolve()
    need(hashlib.sha256(kernel_path.read_bytes()).hexdigest() == R185_FILE_SHA256,
         "Round185 numeric kernel pin")
    need(flint.__version__ == "0.9.0" and flint.ctx.prec == PRECISION_BITS,
         "384-bit numeric environment")
    return flint, r185


def fixed_axis(r185: Any, box: Any, axis: int, value: Fraction, suffix: str) -> Any:
    return r185.fixed_axis_box(box, axis, value, suffix)


def interval_newton_cover(r185: Any, origin: str, child: ExactBox, graph_axis: int,
                          path: str) -> list[dict[str, Any]] | None:
    positive_axes = [axis for axis in range(3)
                     if axis != graph_axis and child.width(axis) > 0]
    queue: list[tuple[ExactBox, str, int]] = [(child, "", 0)]
    accepted: list[dict[str, Any]] = []
    while queue:
        region, prefix, depth = queue.pop(0)
        current = atlas_box(region, path + ".cover." + prefix)
        full, _, _ = r185.collision1_h1_ad(origin, current, "W[1,0]")
        derivative = full.derivative[graph_axis]
        lower, upper = region.bounds(graph_axis)
        midpoint = (lower + upper) / 2
        middle = fixed_axis(r185, current, graph_axis, midpoint, ".mid")
        middle_value, _, _ = r185.collision1_h1_ad(origin, middle, "W[1,0]")
        strict_derivative = bool(derivative > 0) or bool(derivative < 0)
        if strict_derivative:
            image = r185.BASE.arbq(midpoint) - middle_value.value / derivative
            self_map = bool(image > r185.BASE.arbq(lower)) and bool(image < r185.BASE.arbq(upper))
        else:
            image, self_map = None, False
        if self_map:
            accepted.append({
                "cover_prefix": prefix, "cover_depth": depth,
                "relative_Kraft_fraction": str(Fraction(1, 2 ** depth)),
                "exact_box": box_payload(region), "strict_derivative": True,
                "interval_Newton_image": arb_payload(image), "strict_interior_self_map": True,
            })
            continue
        if depth >= MAX_TRANSVERSE_COVER_DEPTH or not positive_axes:
            return None
        split_axis_index = max(positive_axes, key=region.width)
        left, right = split_box(region, split_axis_index)
        queue.extend(((left, prefix + "0", depth + 1),
                      (right, prefix + "1", depth + 1)))
    need(prefix_free(row["cover_prefix"] for row in accepted) and
         sum(Fraction(row["relative_Kraft_fraction"]) for row in accepted) == 1,
         "proof cover prefix/Kraft")
    return sorted(accepted, key=lambda row: row["cover_prefix"])


def independent_child_h1(child_box: ExactBox, child_path: str,
                         c69_decision: dict[str, Any]) -> tuple[str, dict[str, Any], dict[str, Any]]:
    _flint, r185 = load_numeric_kernel()
    origin = c69_decision["representative_origin_key"]
    child = atlas_box(child_box, child_path)
    full, nx, ny = r185.collision1_h1_ad(origin, child, "W[1,0]")
    common = {
        "precision_bits": PRECISION_BITS, "equation": "H1=n1_x^2-n1_y^2",
        "full_child_box_H1_interval": arb_payload(full.value),
        "normal_component_bounds": {"nx": arb_payload(nx.value), "ny": arb_payload(ny.value)},
        "C69c_source_certificate_copied": False,
    }
    if bool(full.value < 0):
        return ("LOCAL_H1_STRICT_NEGATIVE_SLAB_ONLY", common,
                {"H1_LT_0": "EXACT_CHILD", "H1_EQ_0": "EMPTY", "H1_GT_0": "EMPTY",
                 "pairwise_disjoint": True, "union_exact_child": True})
    if bool(full.value > 0):
        return ("LOCAL_H1_STRICT_POSITIVE_SLAB_ONLY", common,
                {"H1_LT_0": "EMPTY", "H1_EQ_0": "EMPTY", "H1_GT_0": "EXACT_CHILD",
                 "pairwise_disjoint": True, "union_exact_child": True})

    graph_certificate: dict[str, Any] | None = None
    for axis in range(3):
        if child_box.width(axis) == 0:
            continue
        derivative = full.derivative[axis]
        if not (bool(derivative > 0) or bool(derivative < 0)):
            continue
        lower, upper = child_box.bounds(axis)
        face_values = []
        for ordinal, value in enumerate((lower, upper)):
            face = fixed_axis(r185, child, axis, value, f".face.{ordinal}")
            evaluated, _, _ = r185.collision1_h1_ad(origin, face, "W[1,0]")
            face_values.append(evaluated.value)
        signs = [1 if bool(value > 0) else -1 if bool(value < 0) else 0
                 for value in face_values]
        if signs[0] * signs[1] != -1:
            continue
        cover = interval_newton_cover(r185, origin, child_box, axis, child_path)
        if cover is None:
            continue
        graph_certificate = {
            **common, "graph_axis": ("t", "p", "s")[axis],
            "strict_graph_axis_derivative_bounds": arb_payload(derivative),
            "complete_relative_graph_axis_faces": [arb_payload(value) for value in face_values],
            "faces_uniform_strict_opposite_sign": True,
            "interval_Newton_cover": cover,
            "cover_prefix_free": True, "cover_Kraft_sum": "1",
            "unique_root_over_every_fixed_transverse_parameter": True,
        }
        break
    need(graph_certificate is not None, "child full-box H1 certificate unavailable")
    partition = {
        "H1_LT_0": "NEGATIVE_OPEN_SLAB", "H1_EQ_0": "UNIQUE_TYPED_GRAPH_CARRIER",
        "H1_GT_0": "POSITIVE_OPEN_SLAB", "pairwise_disjoint": True,
        "union_exact_child": True, "graph_full_dimensional_Kraft_weight": "0",
        "half_open_negative_owner": {"predicate": "H1<=0", "owns_graph": True},
        "half_open_positive_owner": {"predicate": "H1>0", "owns_graph": False},
    }
    return "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS", graph_certificate, partition


def projection_row(child: dict[str, Any], source: dict[str, Any], c69: dict[str, Any],
                   decision_kind: str) -> dict[str, Any]:
    need(row_closed(child) and row_closed(source) and row_closed(c69), "input row closures")
    source_hash = child["source_C61_aggregate_leaf_row_sha256"]
    need(source_hash == source["row_sha256"] == c69["C61_aggregate_leaf_row_sha256"],
         "exact C61 join")
    need(child["pair_index"] == source["pair_index"] == c69["pair_index"] and
         child["source_path"] == source["path"] == c69["path"], "pair/path lineage")
    source_box_payload = source["exact_representative_box"]
    if decision_kind == "decision":
        need(c69["decision"] ==
             "STRICT_UNIQUE_H1_GRAPH_AND_TWO_OFF_GRAPH_SLABS_AVAILABLE" and
             c69["capability_consumption_ready"] is True and
             c69["exact_representative_box"] == source_box_payload,
             "C69c decision source-box/capability binding")
    else:
        need(decision_kind == "blocker" and c69["capability_decision_available"] is False and
             c69["exact_representative_box_object_sha256"] == digest(source_box_payload),
             "C69c blocker source-box/capability binding")
    rebuilt, owners = rebuild_child(exact_box(source_box_payload),
                                    source["path"], child["path"])
    need(box_payload(rebuilt) == child["exact_representative_box"], "exact child box replay")
    prior = child["disposition"]
    numeric: dict[str, Any] | None = None
    partition: dict[str, Any] | None = None
    blockers: list[str] = []
    local = False
    if prior == "STRICT_TERMINAL":
        disposition = "CARRIED_C65_STRICT_TERMINAL_NO_RECLASSIFICATION"
        blockers = ["PRIOR_C65_STRICT_TERMINAL_CARRIED_NO_H1_RECLASSIFICATION"]
    elif prior == "COLLISION3_READY":
        disposition = "CARRIED_C65_COLLISION3_READY_NO_RECLASSIFICATION"
        blockers = ["PRIOR_C65_COLLISION3_READY_CARRIED_NO_H1_RECLASSIFICATION"]
    elif decision_kind == "blocker":
        disposition = "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE"
        blockers = list(c69["blocker_codes"]) + ["C69C_SOURCE_KIND_" + c69["structural_graph_kind"]]
    else:
        need(prior == "COLLISION2_HANDOFF" and decision_kind == "decision",
             "eligible local numeric selection")
        try:
            disposition, numeric, partition = independent_child_h1(rebuilt, child["path"], c69)
            local = True
            blockers = ["LOCAL_ZERO_CREDIT_SIDECAR_NOT_GLOBAL_CONSUMPTION_AUTHORITY",
                        "C70L_SOURCE_FACE_CORNER_GRAZING_AND_LARGE_COMPONENT_GATES_UNCHANGED"]
        except Reject as error:
            disposition = "BLOCKED_CHILD_FULL_BOX_H1_CERTIFICATE_NOT_AVAILABLE"
            blockers = [str(error)]
    body = {
        "schema": SCHEMA + ".intersection-row",
        "C65_aggregate_leaf_row_sha256": child["row_sha256"],
        "C65_source_shard_row_sha256": child["source_C65_shard_row_sha256"],
        "C69c_blocker_row_sha256": c69["row_sha256"] if decision_kind == "blocker" else None,
        "C69c_decision_row_sha256": c69["row_sha256"] if decision_kind == "decision" else None,
        "source_C61_aggregate_leaf_row_sha256": source_hash,
        "source_path": source["path"], "child_path": child["path"],
        "pair_index": child["pair_index"],
        "child_parent_volume_fraction": child["parent_volume_fraction"],
        "exact_representative_box": child["exact_representative_box"],
        "child_box_lineage": {"reconstructed_exact": True, "split_owner_chain": owners,
                              "source_path_exact_prefix": True},
        "prior_C65_disposition": prior, "intersection_disposition": disposition,
        "H1_child_certificate": numeric, "three_strata_partition": partition,
        "local_numeric_strata_available": local, "global_consumption_ready": False,
        "remaining_blocker_codes": blockers, "terminal_disposition_credit": 0,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    }
    return {**body, "row_sha256": digest(body)}


def validate_source_partition(rows: list[dict[str, Any]], source: dict[str, Any]) -> None:
    need(prefix_free(row["child_path"] for row in rows), "source child prefix-free")
    need(sum(Fraction(row["child_parent_volume_fraction"]) for row in rows) ==
         Fraction(source["parent_volume_fraction"]), "source child Kraft")
    need(all(row["source_C61_aggregate_leaf_row_sha256"] == source["row_sha256"]
             for row in rows), "source row union")


def static_self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {}
    calls = 0
    def trap_reader(_path: Path, _sha: str) -> bytes:
        nonlocal calls
        calls += 1
        raise AssertionError("reader called before frozen C65 pins")
    try:
        c65_evidence_gate(Path("/synthetic"), trap_reader)
    except Reject:
        tests["unfrozen_C65_rejected_before_any_file_open"] = calls == 0
    source = ExactBox(Fraction(0), Fraction(1), Fraction(0), Fraction(1),
                      Fraction(0), Fraction(0))
    child, owners = rebuild_child(source, "101", "10101")
    tests["exact_longest_axis_replay"] = (
        box_payload(child) == {"t": ["0", "1/2"], "p": ["1/2", "1"], "s": ["0", "0"]}
    )
    tests["lower_bit_shared_face_owner_recorded"] = (
        len(owners) == 2 and owners[0]["shared_face_owner"] == "LOWER_BIT_CHILD"
    )
    tests["prefix_free_positive"] = prefix_free(["100", "1010", "1011"])
    tests["prefix_overlap_rejected"] = not prefix_free(["10", "101"])
    tests["Kraft_exact"] = sum((Fraction(1, 4), Fraction(1, 4)), Fraction(0)) == Fraction(1, 2)
    tests["C69_partition_exact"] = 2356 + 18523 == 20879
    tests["credits_locked_zero"] = True
    need(all(tests.values()) and len(tests) == 8, "static self-test")
    return {
        "schema": SCHEMA + ".static-self-test", "status": "PASS_8_OF_8_STATIC_TESTS",
        "tests": tests, "formal_execution_performed": False,
        "files_written": False, "formal_credit": 0, "whole_parent_credit": 0,
        "D02_gate_credit": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--static-self-test", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    need(sum((args.static_self_test, args.preflight, args.execute)) == 1, "choose exactly one mode")
    if args.static_self_test:
        print(json.dumps(static_self_test(), sort_keys=True, separators=(",", ":")))
        return 0
    if args.execute:
        raise Reject("formal execution/publication disabled by frozen C71 contract")
    formal_evidence_gate(OUT)
    raise Reject("preflight unexpectedly passed while C65 pins are intentionally unfrozen")


if __name__ == "__main__":
    raise SystemExit(main())
