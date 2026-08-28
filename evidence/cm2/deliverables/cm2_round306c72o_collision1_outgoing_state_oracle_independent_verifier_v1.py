#!/usr/bin/env python3
"""Independent no-producer verifier for the staged C72o outgoing oracle.

Policy boundary: this verifier never opens, reads, parses, imports, executes, or
decodes the C72o producer source.  The producer is bound only by a hard-coded
SHA-256 declaration carried in the candidate result.  All upstream byte joins
and every numerical decision are reconstructed here at fresh 512-bit precision.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterator, Mapping
import zlib

from flint import arb, ctx

import cm2_round185_preconditioned_c1_residual_refinement as r185
import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139


ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"
SELF = Path(__file__).resolve()
SCHEMA = "cm2.round306c72o.collision1-outgoing-state-oracle.independent-verifier.v1"
PREFIX = "cm2_round306c72o_collision1_outgoing_state_oracle_v1"
LEDGER = PREFIX + ".jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
LOCK = "ZERO_CREDIT_STAGED_OUTGOING_ORACLE_ONLY.lock"
PRODUCER_SHA256_DECLARATION_ONLY = "c2aa5de01787784bad2d01fbf315cc83bba070c54a540752ad9f18cb673b2842"
EXPECTED_RESULT_OBJECT = "529d7081293b37111619d4dbf03c750be06da48105d46cc18e8c79eee10b48e7"
EXPECTED_LEDGER_SHA = "e3125863adcf3ef6489dce741337622b1d70b2ce7655d8d06237c1612ff19355"
PRECISION_BITS = 512
FROZEN_OWNER = "W[1,0]"
CORE_INDEX = {"W:E": 14, "W:N": 17, "W:S": 20, "W:W": 23}

C38_DIR = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C35_DIR = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C37_DIR = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38"

PINS = {
    "C72_RESULT": "55318b7c3ee778cb8a0e41d612c9c2caa44790e6fff816a6104116268258f01e",
    "C72_LEDGER": "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370",
    "C72_VERIFY": "63105e380d37d49bd655e094d41e15d3ed0d182380a44a4a16709ba3308edaf0",
    "C65_RESULT": "1ca46fb81cc104b727b31d3bb0adbb439ab8dae9123b8cbe05d3c60de0e75457",
    "C65_LEAVES": "4ff1c36a0a6331510da3afb988738f128a3cada04ddd297ac58584579115437d",
    "C69_RESULT": "607fc73ebe3333ca172eb15c0831b8c3d98192c86e20eec7a59a69c4ae4737d4",
    "C69_BLOCKERS": "69b3ec294f95cb5ce377e553ae875daab10a5bdb33e860363f6bae122022e606",
    "C38_RESULT": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_CHILDREN": "0347849c0368368430f5456b71cd4a4bce4e5912c8a3da33649cfac35b1708a2",
    "C35_RESULT": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_PATH": "cf24920309daad0f621dd5ed8b3bdb394727be377917cca34f92767d044f8e66",
    "C37_RESULT": "5b968d957cbca2a4f8aec855a44643f5add7fe0244d933401dfdef9ad7be61f3",
    "C37_PATH": "7c87829f6ef883b7928ff8a313d5bfcf240383c51a9040739de1cfe7e617bef5",
}
OBJECT_PINS = {
    "C72_RESULT": "a6aa0cfd8e1ee1b7a02d92af066acb23abffb22b0b7276b7e233d2ff7d92f9f4",
    "C72_VERIFY": "8ae20b71916ee1f6d1d28e633b1fbc080f4cb277eed7b6bb54937f8538ae7994",
    "C65_RESULT": "79185dbca48f0d228977a006583eb545525cff2d9418160fb190c1f9c5b6c393",
    "C69_RESULT": "e52904a7d8ba73c855e69e390cd3cf29c233ffe492e6fae74efdf0b6d4d0a6a5",
    "C38_RESULT": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C35_RESULT": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C37_RESULT": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
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
EXPECTED_CATEGORY = {"COLLISION1_OUTGOING_STATE": 423,
                     "REGULAR_BOUNDARY_ARRANGEMENT": 18_245}
EXPECTED_OUTCOME = {"STRICT_EXCLUSION_COLLISION1_WORD_MISMATCH": 8_321,
                    "STRICT_EXCLUSION_COLLISION2_OWNER_MISMATCH": 10_347}
EXPECTED_OWNER2 = {"W[1,-1]": 5_851, "W[1,1]": 4_496}
EXPECTED_REPORT = (
    "# C72o exact collision-one outgoing-state oracle\n\n"
    "- Selector: `child_route_witness == OUTGOING_STATE`.\n"
    "- Closed without subdivision: 18,668 / 18,668 children.\n"
    "- Strict exclusions: 8,321 collision-one official-word mismatches; "
    "10,347 collision-two strict-owner mismatches.\n"
    "- Source-category split: 423 outgoing-state category + 18,245 "
    "boundary-source children with the same child-level capability.\n"
    "- This staged object grants zero formal, whole-parent, D02, or CM2 credit.\n"
).encode()
EXPECTED_LOCK = b"STAGED ZERO-CREDIT ORACLE ONLY; NO AUTHORITY OR GLOBAL PROMOTION.\n"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate:" + key)
        result[key] = value
    return result


def parse(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"), label + ":framing")
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=unique,
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
    need(type(value) is dict and canonical(value) == raw, label + ":canonical")
    return value


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value)); claim = body.pop("row_sha256", None)
    need(claim == digest(body), label + ":row closure")


def close_object(value: Mapping[str, Any], expected: str | None, label: str) -> None:
    body = copy.deepcopy(dict(value)); claim = body.pop("object_sha256", None)
    need(type(claim) is str and claim == digest(body) and
         (expected is None or claim == expected), label + ":object closure")


@dataclass(frozen=True)
class Identity:
    dev: int; ino: int; mode: int; nlink: int; size: int; mtime_ns: int; ctime_ns: int


def ident(value: os.stat_result) -> Identity:
    return Identity(value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
                    value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def open_regular(path: Path) -> tuple[int, Identity]:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                 getattr(os, "O_NOFOLLOW", 0)); first = os.fstat(fd)
    need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "regular single-link:" + str(path))
    return fd, ident(first)


def secure_bytes(path: Path, expected: str | None = None,
                 maximum: int = 64 << 20) -> tuple[bytes, str]:
    fd, first = open_regular(path); data = bytearray(); h = hashlib.sha256()
    try:
        while True:
            block = os.read(fd, 1 << 20)
            if not block: break
            h.update(block); data.extend(block); need(len(data) <= maximum, "bound:" + str(path))
        observed = h.hexdigest()
        need(first == ident(os.fstat(fd)) == ident(os.stat(path, follow_symlinks=False)),
             "TOCTOU:" + str(path))
        need(expected is None or observed == expected, "pin:" + str(path))
        return bytes(data), observed
    finally:
        os.close(fd)


def secure_json(path: Path, file_pin: str | None, object_pin: str | None) -> tuple[dict[str, Any], str]:
    raw, observed = secure_bytes(path, file_pin)
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "JSON newline:" + str(path))
    value = parse(raw[:-1], str(path)); close_object(value, object_pin, str(path))
    return value, observed


def iter_jsonl(path: Path, file_pin: str, rows: int) -> Iterator[dict[str, Any]]:
    fd, first = open_regular(path); h = hashlib.sha256(); z = zlib.decompressobj(16 + zlib.MAX_WBITS)
    pending = bytearray(); count = 0; expanded = 0
    try:
        while True:
            block = os.read(fd, 1 << 20)
            if not block: break
            h.update(block); decoded = z.decompress(block); expanded += len(decoded)
            need(expanded <= 1 << 30, "gzip bound"); pending.extend(decoded)
            while True:
                n = pending.find(b"\n")
                if n < 0: break
                raw = bytes(pending[:n]); del pending[:n + 1]
                value = parse(raw, f"{path}:{count + 1}"); close_row(value, f"{path}:{count + 1}")
                count += 1; yield value
        pending.extend(z.flush())
        need(z.eof and not z.unused_data and not z.unconsumed_tail and not pending,
             "gzip closure:" + str(path))
        need(count == rows and h.hexdigest() == file_pin, "ledger closure:" + str(path))
        need(first == ident(os.fstat(fd)) == ident(os.stat(path, follow_symlinks=False)),
             "ledger TOCTOU:" + str(path))
    finally:
        os.close(fd)


def file_sha(path: Path) -> str:
    _raw, value = secure_bytes(path, maximum=128 << 20); return value


def numeric_pins() -> dict[str, str]:
    modules = {"r185": r185, "r178": r185.r178, "atlas": r185.atlas,
               "ge": r185.ge, "registry": r185.registry, "r139": r139,
               "lower": r139.lower, "round136": r139.lower.round136,
               "time3": r139.lower.time3, "time2": r139.lower.time3.time2_cert,
               "core": r139.lower.core_cert, "step1": r139.lower.step1}
    observed = {name: file_sha(Path(module.__file__).resolve()) for name, module in modules.items()}
    need(observed == NUMERIC_PINS and getattr(sys.modules["flint"], "__version__") == "0.9.0",
         "numeric pins")
    return observed


def aq(value: Q) -> arb:
    return r139.lower.step1.arbq(value)


def claim_margin(value: arb, depth: int, label: str) -> None:
    need(type(depth) is int and bool(value > aq(Q(1, 2 ** depth) if depth >= 0
                                               else Q(2 ** (-depth)))), label)


def box(row: Mapping[str, Any]) -> Any:
    b = row["exact_representative_box"]
    return r185.atlas.AtlasBox(Q(b["t"][0]), Q(b["t"][1]), Q(b["p"][0]), Q(b["p"][1]),
                               Q(b["s"][0]), Q(b["s"][1]), len(row["child_path"]), row["child_path"])


def reconstruct_outgoing(row: dict[str, Any], cores: tuple[Any, ...]) -> tuple[dict[str, Any],
                                                                                dict[str, arb],
                                                                                dict[str, Any]]:
    parent = row["parent_key"]; b = box(row); chart_id = ":".join(parent.split(":")[:2])
    atom = r139.lower.step1.Atom(CORE_INDEX[chart_id], cores[CORE_INDEX[chart_id]],
                                 b.t0, b.t1, b.p0, b.p1, Q(0), Q(0), "independent")
    initial = r139.lower.round136.initial_state(atom)
    raw = r185.ad_root(r185.ad_initial_geometry(parent, b), FROZEN_OWNER)
    delta = r185.centered_enclosure(r185.collision0_delta_ad, parent, b, FROZEN_OWNER, raw["Delta"])
    need(bool(delta > 0), "independent centered Delta")
    radius = raw["radius"].value; radical = delta.sqrt(); trans = raw["transverse"].value
    near = raw["ell"].value - radical
    tau = r139.lower.time3.time2_cert.step1.arbq(r139.lower.time3.time2_cert.first_hit.TAU_MAX)
    need(bool(near > 0) and bool(tau - near > 0), "independent collision1 root")
    nx = (-radical * initial["outgoing_x"] + trans * initial["outgoing_y"]) / radius
    ny = (-radical * initial["outgoing_y"] - trans * initial["outgoing_x"]) / radius
    p = trans / radius; radial = radical / radius
    full, adnx, _adny = r185.collision1_h1_ad(parent, b, FROZEN_OWNER)
    h1 = r185.centered_enclosure(r185.collision1_h1_ad, parent, b, FROZEN_OWNER, full)
    need(bool(h1 > 0) and bool(adnx.value < 0) and bool(radial > 0), "independent W chart")
    owner = {"selected_target_id": FROZEN_OWNER, "selected_root": near,
             "normal_x": nx, "normal_y": ny, "p": p, "cosine": radial}
    cx, cy = r139.lower.time3.time2_cert.target_center(FROZEN_OWNER, initial["s"])
    outgoing = {"contact_x": cx + radius * nx, "contact_y": cy + radius * ny,
                "outgoing_x": radial * nx - p * ny, "outgoing_y": radial * ny + p * nx,
                "s": initial["s"], "chart": "W", "normal_x": nx, "normal_y": ny, "p": p}
    margins = {"centered_Delta": delta, "radial_Delta_over_R2": delta / (radius * radius),
               "centered_H1": h1, "negative_nx": -adnx.value,
               "near_root": near, "tau_minus_near": tau - near}
    return {"initial": initial, "owner": owner, "outgoing": outgoing}, margins, {"atom": atom}


def reconstruct_owner2(state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, arb | None]]:
    time2 = r139.lower.time3.time2_cert; candidates = list(time2.translated_candidate_ids(FROZEN_OWNER, "W"))
    counts: Counter[str] = Counter(); future = []
    for identifier in candidates:
        item = time2.candidate_root(state["contact_x"], state["contact_y"],
                                    state["outgoing_x"], state["outgoing_y"], state["s"], identifier)
        need(item["classification"] in {"no_real_intersection", "intersection_strictly_behind",
                                        "strict_future_near_root"}, "independent owner2 competitor")
        counts[item["classification"]] += 1
        if item["classification"] == "strict_future_near_root": future.append((identifier, item))
    winners = [(identifier, item) for identifier, item in future if all(
        identifier == other or bool(item["near"] < other_item["near"])
        for other, other_item in future)]
    need(len(winners) == 1, "independent owner2 winner")
    selected_id, selected = winners[0]
    gaps = [other["near"] - selected["near"] for identifier, other in future if identifier != selected_id]
    need(all(bool(value > 0) for value in gaps), "independent owner2 gaps")
    tau = time2.step1.arq(time2.first_hit.TAU_MAX) if hasattr(time2.step1, "arq") else time2.step1.arbq(time2.first_hit.TAU_MAX)
    need(bool(tau - selected["near"] > 0), "independent owner2 tau")
    evidence = {"retained_candidate_count": len(candidates),
                "classification_census": dict(sorted(counts.items())),
                "strict_future_candidate_count": len(future)}
    margins: dict[str, arb | None] = {"selected_root_dyadic_depth": selected["near"],
                                     "selected_tau_margin_dyadic_depth": tau - selected["near"],
                                     "minimum_root_order_gap_dyadic_depth": min(gaps, key=lambda x: x.lower()) if gaps else None}
    return {"selected_target_id": selected_id}, evidence, margins


def candidate_pair_bytes(a: Path, b: Path) -> dict[str, str]:
    hashes = {}
    for name in (LEDGER, RESULT, REPORT, LOCK):
        raw_a, sha_a = secure_bytes(a / name, maximum=128 << 20)
        raw_b, sha_b = secure_bytes(b / name, maximum=128 << 20)
        need(raw_a == raw_b and sha_a == sha_b, "dual bytes:" + name)
        hashes[name] = sha_a
    return hashes


def policy(value: dict[str, Any]) -> None:
    need(value["status"] ==
         "PASS_18668_OF_18668_OUTGOING_STATE_WITNESS_CHILDREN_STRICTLY_EXCLUDED__ZERO_CREDIT",
         "policy status")
    need(value["producer_file_sha256"] == PRODUCER_SHA256_DECLARATION_ONLY,
         "producer declaration")
    scope = value["capability_scope"]
    need(scope["target_child_count"] == 18_668 and scope["same_capability_pending_child_count"] == 0 and
         scope["original_COLLISION1_OUTGOING_STATE_category_child_count"] == 423 and
         scope["same_capability_cross_category_child_count"] == 18_245 and
         scope["additional_dyadic_depth"] == 0, "policy scope")
    need(value["outcome_census"] == EXPECTED_OUTCOME and
         value["collision2_selected_owner_census"] == EXPECTED_OWNER2, "policy census")
    boundary = value["strict_boundary"]
    need(boundary["candidate_is_authority"] is False and
         boundary["global_consumption_ready"] is False and
         boundary["only_later_no_producer_global_consumer_may_promote"] is True and
         boundary["remaining_C72_atlas_children_outside_this_capability"] == 115_487 and
         all(boundary[name] == 0 for name in ("formal_credit", "whole_parent_credit",
                                               "D02_gate_credit", "CM2_credit")), "policy boundary")


def coherent_attacks(result: dict[str, Any], first_row: dict[str, Any]) -> dict[str, Any]:
    attacks: dict[str, bool] = {}
    mutations = [
        ("status", lambda x: x.__setitem__("status", "PASS")),
        ("producer", lambda x: x.__setitem__("producer_file_sha256", "0" * 64)),
        ("target", lambda x: x["capability_scope"].__setitem__("target_child_count", 18_667)),
        ("pending", lambda x: x["capability_scope"].__setitem__("same_capability_pending_child_count", 1)),
        ("category", lambda x: x["capability_scope"].__setitem__("original_COLLISION1_OUTGOING_STATE_category_child_count", 18_668)),
        ("cross", lambda x: x["capability_scope"].__setitem__("same_capability_cross_category_child_count", 0)),
        ("depth", lambda x: x["capability_scope"].__setitem__("additional_dyadic_depth", 1)),
        ("outcome", lambda x: x["outcome_census"].__setitem__("STRICT_EXCLUSION_COLLISION1_WORD_MISMATCH", 8_320)),
        ("owner", lambda x: x["collision2_selected_owner_census"].__setitem__("W[1,-1]", 5_850)),
        ("authority", lambda x: x["strict_boundary"].__setitem__("candidate_is_authority", True)),
        ("ready", lambda x: x["strict_boundary"].__setitem__("global_consumption_ready", True)),
        ("formal", lambda x: x["strict_boundary"].__setitem__("formal_credit", 1)),
        ("whole", lambda x: x["strict_boundary"].__setitem__("whole_parent_credit", 1)),
        ("D02", lambda x: x["strict_boundary"].__setitem__("D02_gate_credit", 1)),
        ("CM2", lambda x: x["strict_boundary"].__setitem__("CM2_credit", 1)),
        ("consumer", lambda x: x["strict_boundary"].__setitem__("only_later_no_producer_global_consumer_may_promote", False)),
        ("outside", lambda x: x["strict_boundary"].__setitem__("remaining_C72_atlas_children_outside_this_capability", 0)),
    ]
    for name, mutate in mutations:
        trial = copy.deepcopy(result); mutate(trial)
        try: policy(trial)
        except Reject: attacks[name] = True
        else: attacks[name] = False
    row_trials = {
        "row_exit": ("exit_class", "SEALED_COLLISION3_HANDOFF"),
        "row_credit": ("formal_credit", 1), "row_D02": ("D02_gate_credit", 1),
        "row_CM2": ("CM2_credit", 1), "row_depth": ("additional_dyadic_depth", 1),
        "row_chart": ("collision1_chart", "E"), "row_owner": ("collision1_owner", "G[0,0]"),
        "row_witness": ("child_route_witness", "OTHER"),
    }
    for name, (field, value) in row_trials.items():
        trial = copy.deepcopy(first_row); trial[field] = value
        good = (trial["exit_class"] == "STRICT_EXCLUSION" and trial["formal_credit"] == 0 and
                trial["D02_gate_credit"] == 0 and trial["CM2_credit"] == 0 and
                trial["additional_dyadic_depth"] == 0 and trial["collision1_chart"] == "W" and
                trial["collision1_owner"] == FROZEN_OWNER and trial["child_route_witness"] == "OUTGOING_STATE")
        attacks[name] = not good
    need(len(attacks) == 25 and all(attacks.values()), "coherent attacks")
    return {"attack_count": len(attacks), "attacks": dict(sorted(attacks.items())),
            "status": "PASS_25_OF_25_COHERENT_SCOPE_CREDIT_AND_ROUTE_ATTACKS_FAIL_CLOSED"}


def verify(c72: Path, candidate_a: Path, candidate_b: Path, output: Path) -> dict[str, Any]:
    need(not output.exists(), "verification output exists")
    dual_hashes = candidate_pair_bytes(candidate_a, candidate_b)
    need(dual_hashes[LEDGER] == EXPECTED_LEDGER_SHA, "candidate ledger pin")
    result, result_file = secure_json(candidate_a / RESULT, None, EXPECTED_RESULT_OBJECT)
    need(result_file == dual_hashes[RESULT] and result["ledger"]["sha256"] == EXPECTED_LEDGER_SHA and
         result["ledger"]["row_count"] == 18_668, "candidate result descriptor")
    policy(result)
    report, _ = secure_bytes(candidate_a / REPORT); lock, _ = secure_bytes(candidate_a / LOCK)
    need(report == EXPECTED_REPORT and lock == EXPECTED_LOCK, "report lock")
    numeric = numeric_pins(); ctx.prec = PRECISION_BITS
    pair_index, pattern_index, registry_sha = r139.lower.component_cert.key_index_tables()
    cores = tuple(r139.lower.core_cert.physical_cores())

    c72_result, _ = secure_json(c72 / "cm2_round306c72_structural_child_obligation_atlas_v1_result.json",
                                PINS["C72_RESULT"], OBJECT_PINS["C72_RESULT"])
    c72_verify, _ = secure_json(c72 / "cm2_round306c72_structural_child_obligation_atlas_independent_verification_v1.json",
                                PINS["C72_VERIFY"], OBJECT_PINS["C72_VERIFY"])
    need(c72_result["ledger"]["sha256"] == PINS["C72_LEDGER"] and
         c72_verify["candidate_object_sha256"] == OBJECT_PINS["C72_RESULT"], "C72 closure")
    atlas_rows = [row for row in iter_jsonl(
        c72 / "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz",
        PINS["C72_LEDGER"], 134_155) if row["child_route_witness"] == "OUTGOING_STATE"]
    output_rows = list(iter_jsonl(candidate_a / LEDGER, EXPECTED_LEDGER_SHA, 18_668))
    need(len(atlas_rows) == len(output_rows) == 18_668, "target/output count")

    by_c65 = {row["C65_aggregate_child_row_sha256"]: (atlas, row)
              for atlas, row in zip(atlas_rows, output_rows)}
    by_c69 = {row["C69c_blocker_row_sha256"]: (atlas, row)
              for atlas, row in zip(atlas_rows, output_rows)}
    found65 = set(); found69 = set()
    c65_result, _ = secure_json(DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_result_v1.json",
                                PINS["C65_RESULT"], OBJECT_PINS["C65_RESULT"])
    c69_result, _ = secure_json(DELIVERABLES / "cm2_round306c69c_descriptor_repair_supersession_v1_corrected_result.json",
                                PINS["C69_RESULT"], OBJECT_PINS["C69_RESULT"])
    need(c65_result["ledgers"]["aggregate_leaves"]["row_count"] == 358_919 and
         c69_result["ledgers"]["blockers"]["row_count"] == 18_523, "upstream descriptors")
    for source in iter_jsonl(DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz",
                             PINS["C65_LEAVES"], 358_919):
        item = by_c65.get(source["row_sha256"])
        if item is None: continue
        atlas, row = item
        need(source["path"] == row["child_path"] == atlas["child_path"] and
             source["source_path"] == row["source_path"] == atlas["source_path"] and
             source["pair_index"] == row["pair_index"] == atlas["pair_index"] and
             source["exact_representative_box"] == row["exact_representative_box"] == atlas["exact_representative_box"] and
             source["source_C61_aggregate_leaf_row_sha256"] == row["C61_aggregate_leaf_row_sha256"],
             "independent C65 lineage")
        continuation = source["continuation"]
        need(continuation["collision1_original_owner"] == FROZEN_OWNER and
             continuation["collision1_history_row_sha256"] == row["collision1_history_row_sha256"] and
             continuation["collision1_event_order"]["outgoing_chart"] == "W", "C65 event lineage")
        found65.add(source["row_sha256"])
    for source in iter_jsonl(DELIVERABLES / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz",
                             PINS["C69_BLOCKERS"], 18_523):
        item = by_c69.get(source["row_sha256"])
        if item is None: continue
        atlas, row = item
        need(source["C61_aggregate_leaf_row_sha256"] == row["C61_aggregate_leaf_row_sha256"] and
             source["path"] == row["source_path"] and source["pair_index"] == row["pair_index"] and
             source["structural_graph_kind"] == row["source_structural_category"] == atlas["structural_category"],
             "independent C69 lineage")
        found69.add(source["row_sha256"])
    need(found65 == set(by_c65) and found69 == set(by_c69), "upstream inventory")

    c38_result, _ = secure_json(C38_DIR / "result.json", PINS["C38_RESULT"], OBJECT_PINS["C38_RESULT"])
    origins: dict[int, tuple[str, str, str]] = {}
    target_pairs = {row["pair_index"] for row in output_rows}
    for source in iter_jsonl(C38_DIR / "collision1_2_child_pairs.jsonl.gz", PINS["C38_CHILDREN"], 10_486):
        if source["pair_index"] not in target_pairs: continue
        value = (source["representative_origin_key"], source["representative_cell_id"],
                 source["representative_parent_row_sha256"])
        need(source["pair_index"] not in origins or origins[source["pair_index"]] == value,
             "C38 origin consistency")
        origins[source["pair_index"]] = value
    need(len(origins) == 12, "C38 origin count")
    c35_result, _ = secure_json(C35_DIR / "result.json", PINS["C35_RESULT"], OBJECT_PINS["C35_RESULT"])
    c37_result, _ = secure_json(C37_DIR / "result.json", PINS["C37_RESULT"], OBJECT_PINS["C37_RESULT"])
    original = [row for index, row in enumerate(iter_jsonl(C35_DIR / "path_occurrences.jsonl.gz",
                                                            PINS["C35_PATH"], 1_648)) if index < 2]
    reflected = [row for index, row in enumerate(iter_jsonl(C37_DIR / "reflected_r1648_occurrences.jsonl.gz",
                                                             PINS["C37_PATH"], 1_648)) if index < 2]
    expected_word = original[0]["official_word_key_id"]
    expected_owner_set = sorted({original[1]["selected_absolute_owner_id"],
                                 reflected[1]["selected_absolute_owner_id"]})

    outcomes: Counter[str] = Counter(); categories: Counter[str] = Counter(); owners: Counter[str] = Counter()
    first_row = output_rows[0]
    for atlas, row in zip(atlas_rows, output_rows):
        need(row["C72_atlas_row_sha256"] == atlas["row_sha256"] and
             row["child_path"] == atlas["child_path"] and row["source_path"] == atlas["source_path"] and
             row["child_route_witness"] == "OUTGOING_STATE" and
             row["source_structural_category"] == atlas["structural_category"], "atlas output alignment")
        origin = origins[row["pair_index"]]
        need((row["parent_key"], row["C38_representative_cell_id"],
              row["C38_representative_parent_row_sha256"]) == origin, "origin binding")
        route, margins, _extra = reconstruct_outgoing(row, cores)
        for name, value in margins.items():
            claim_margin(value, row["collision1_margin_dyadic_depths"][name], "margin:" + name)
        word, error = r139.lower.round136.translation_normalized_official_word(
            route["initial"], "W[0,0]", route["owner"], pair_index, pattern_index)
        need(word is not None and error is None, "independent word")
        compact = r139.lower.round136.compact_key(word["key"])
        word_id = compact["official_word_key_id"]
        need(row["collision1_computed_official_word_key_id"] == word_id and
             row["collision1_expected_official_word_key_id"] == expected_word and
             row["collision1_registry_row_sha256"] == compact["registry_row_sha256"] and
             row["collision1_ordered_clean_wall_record"] == word["ordered_clean_wall_record"],
             "word evidence")
        if word_id != expected_word:
            outcome = "STRICT_EXCLUSION_COLLISION1_WORD_MISMATCH"; witness = word_id
            need(row["collision2_selected_owner"] is None and
                 row["collision2_owner_order_evidence"] is None, "no owner2 branch")
        else:
            owner2, evidence, owner_margins = reconstruct_owner2(route["outgoing"])
            selected = owner2["selected_target_id"]
            outcome = "STRICT_EXCLUSION_COLLISION2_OWNER_MISMATCH"; witness = selected
            need(selected not in expected_owner_set and row["collision2_selected_owner"] == selected and
                 row["collision2_expected_owner_set"] == expected_owner_set, "owner2 mismatch")
            stored = row["collision2_owner_order_evidence"]
            need({key: stored[key] for key in ("retained_candidate_count", "classification_census",
                                                "strict_future_candidate_count")} == evidence,
                 "owner2 census evidence")
            for key, value in owner_margins.items():
                if value is None: need(stored[key] is None, "owner2 null gap")
                else: claim_margin(value, stored[key], "owner2 margin:" + key)
            owners[selected] += 1
        need(row["exit_class"] == "STRICT_EXCLUSION" and
             row["strict_exclusion_reason"] == outcome and
             row["strict_exclusion_witness"] == witness and
             row["current_disposition"] == "STAGED_ZERO_CREDIT_STRICT_EXCLUSION_CANDIDATE" and
             row["additional_dyadic_depth"] == 0 and row["collision1_owner"] == FROZEN_OWNER and
             row["collision1_chart"] == "W" and
             all(row[name] == 0 for name in ("formal_credit", "whole_parent_credit",
                                              "D02_gate_credit", "CM2_credit")), "row policy")
        outcomes[outcome] += 1; categories[row["source_structural_category"]] += 1
    need(dict(outcomes) == EXPECTED_OUTCOME and dict(categories) == EXPECTED_CATEGORY and
         dict(owners) == EXPECTED_OWNER2, "independent final census")
    attacks = coherent_attacks(result, first_row)

    # Terminal-byte replay of both candidates and all direct upstream ledgers.
    terminal = {}
    for path, expected in [
        (candidate_a / LEDGER, EXPECTED_LEDGER_SHA), (candidate_a / RESULT, dual_hashes[RESULT]),
        (candidate_a / REPORT, dual_hashes[REPORT]), (candidate_a / LOCK, dual_hashes[LOCK]),
        (candidate_b / LEDGER, EXPECTED_LEDGER_SHA), (candidate_b / RESULT, dual_hashes[RESULT]),
        (candidate_b / REPORT, dual_hashes[REPORT]), (candidate_b / LOCK, dual_hashes[LOCK]),
        (c72 / "cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz", PINS["C72_LEDGER"]),
        (DELIVERABLES / "cm2_round306c65s18_depth18_64shard_aggregate_leaf_ledger_v1.jsonl.gz", PINS["C65_LEAVES"]),
        (DELIVERABLES / "cm2_round306c69b_singleton_h1_graph_slab_decider_v2_blockers.jsonl.gz", PINS["C69_BLOCKERS"]),
        (C38_DIR / "collision1_2_child_pairs.jsonl.gz", PINS["C38_CHILDREN"]),
        (C35_DIR / "path_occurrences.jsonl.gz", PINS["C35_PATH"]),
        (C37_DIR / "reflected_r1648_occurrences.jsonl.gz", PINS["C37_PATH"]),
    ]:
        observed = file_sha(path); need(observed == expected, "terminal replay:" + str(path)); terminal[str(path)] = observed
    verification: dict[str, Any] = {
        "schema": SCHEMA, "status": "PASS_INDEPENDENT_NO_PRODUCER_18668_OF_18668_RECONSTRUCTION",
        "verifier_file_sha256": file_sha(SELF),
        "producer_file_sha256_declaration_only": PRODUCER_SHA256_DECLARATION_ONLY,
        "producer_source_policy": {
            "opened": False, "read": False, "parsed": False, "imported": False,
            "executed": False, "decoded": False,
        },
        "precision_bits": PRECISION_BITS, "python_flint_version": "0.9.0",
        "numeric_source_sha256": numeric, "official_registry_sha256": registry_sha,
        "candidate_result_object_sha256": result["object_sha256"],
        "candidate_dual_byte_identity": True, "candidate_file_sha256": dual_hashes,
        "recomputed_target_child_count": 18_668,
        "recomputed_source_category_census": dict(sorted(categories.items())),
        "recomputed_outcome_census": dict(sorted(outcomes.items())),
        "recomputed_collision2_selected_owner_census": dict(sorted(owners.items())),
        "additional_dyadic_depth": 0, "same_capability_pending_child_count": 0,
        "coherent_attacks": attacks,
        "terminal_byte_replay_sha256": dict(sorted(terminal.items())),
        "strict_boundary": {"candidate_is_authority": False, "formal_credit": 0,
                            "whole_parent_credit": 0, "D02_gate_credit": 0,
                            "CM2_credit": 0, "global_consumption_ready": False},
    }
    verification["object_sha256"] = digest(verification)
    payload = canonical(verification) + b"\n"
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0), 0o644)
    try:
        view = memoryview(payload)
        while view:
            n = os.write(fd, view); need(n > 0, "verification write"); view = view[n:]
        os.fsync(fd)
    finally:
        os.close(fd)
    need(file_sha(output) == hashlib.sha256(payload).hexdigest(), "verification terminal replay")
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c72-dir", type=Path, required=True)
    parser.add_argument("--candidate-a", type=Path, required=True)
    parser.add_argument("--candidate-b", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    value = verify(args.c72_dir.resolve(), args.candidate_a.resolve(),
                   args.candidate_b.resolve(), args.output.resolve())
    print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"],
                      "attack_count": value["coherent_attacks"]["attack_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
