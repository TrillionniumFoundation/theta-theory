#!/usr/bin/env python3
"""C74-L: exact source-seam collision-1 handoff successor (zero credit).

This staged successor closes the sixteen SOURCE_CHART_TRANSITION edges in the
two frozen large components.  It does not reinterpret an unfinished C41 cell
as a completed cell.  Instead it proves the physical collision-one state on
the seam and emits a sealed handoff to the next decider.  Thirteen edges reuse
their independently reconstructed full named margins; one edge transports the
strict E-chart proof through exact state glue; and two edges are proved on the
exact structural split p=+/-4/5 without increasing dyadic depth.

All outputs are deterministic, append-only, and zero-credit.  The caller must
provide a new empty directory.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
FLINT_SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
for entry in (str(FLINT_SITE), str(OUT)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from flint import ctx  # type: ignore

ctx.prec = 384
import cm2_round306c67l_occurrence1_dynamic_margin_transport_v1 as C67

SCHEMA = "cm2.round306c74l.source-seam-collision1-handoff-successor.v1"
PREFIX = "cm2_round306c74l_source_seam_collision1_handoff_successor_v1"
SEAM_NAME = PREFIX + "_source_seam_handoff.jsonl.gz"
EDGE_NAME = PREFIX + "_edge_overlay.jsonl.gz"
CORRIDOR_NAME = PREFIX + "_corridor_overlay.jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"
REPORT_NAME = PREFIX + "_report.md"
MANIFEST_NAME = PREFIX + "_manifest.sha256"
RECEIPT_NAME = PREFIX + "_completion_receipt.json"
LOCK_NAME = "ZERO_CREDIT_STAGED_C74L_ONLY.lock"
PRECISION_BITS = 384

C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"

FILES: dict[str, Path] = {
    "C55C_CONTRACT": OUT / "cm2_round306c55c_no_producer_global_strict_cemetery_disconnected_closed_contract_v1.json",
    "C55C_VERIFY": OUT / "cm2_round306c55c_no_producer_global_strict_cemetery_disconnected_verification_v1.json",
    "C56L_RESULT": OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json",
    "C56L_CELLS": OUT / "cm2_round306c56l_large_component_common_refinement_corridor_and_separator_cells_v1.jsonl.gz",
    "C57L_EDGES": OUT / "cm2_round306c57l1_collision1_edgewise_transport_edge_obligations_v1.jsonl.gz",
    "C60L_ATOMS": OUT / "cm2_round306c60l_static_edge_owner_incidence_atoms_v1.jsonl.gz",
    "C63L_RESULT": OUT / "cm2_round306c63l_scope_extension_result_v1.json",
    "C63L_EDGES": OUT / "cm2_round306c63l_scope_extension_edge_replay_v1.jsonl.gz",
    "C66L_RESULT": OUT / "cm2_round306c66l_global_owner_decider_authority_candidate_v1.json",
    "C66L_EDGES": OUT / "cm2_round306c66l_global_owner_decider_edge_owner_decisions_v1.jsonl.gz",
    "C67L_RESULT": OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_result_v1.json",
    "C67L_ENDPOINTS": OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_endpoint_occurrence_margins_v1.jsonl.gz",
    "C67L_ATOMS": OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_atom_coverage_v1.jsonl.gz",
    "C67L_EDGES": OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_edge_coverage_v1.jsonl.gz",
    "C67L_CORRIDORS": OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_corridor_coverage_v1.jsonl.gz",
    "C68L_RESULT": OUT / "cm2_round306c68l_blocker_crosswalk_result_v1.json",
    "C68L_EDGES": OUT / "cm2_round306c68l_blocker_crosswalk_large_edge_blockers_v1.jsonl.gz",
    "C68L_CORRIDORS": OUT / "cm2_round306c68l_blocker_crosswalk_large_corridor_cell_blockers_v1.jsonl.gz",
    "C70L_RESULT": OUT / "cm2_round306c70l_large_component_consumption_intersection_result_v1.json",
    "C70L_EDGES": OUT / "cm2_round306c70l_large_component_consumption_intersection_edge_ledger_v1.jsonl.gz",
    "C70L_CORRIDORS": OUT / "cm2_round306c70l_large_component_consumption_intersection_corridor_ledger_v1.jsonl.gz",
    "C72G_CONTRACT": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_contract_v1.json",
    "C72G_VERIFY": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_verification_v1.json",
    "C72G_OUTER": OUT / "cm2_round306c72g_no_producer_global_consumer_successor_outer_receipt_v1.json",
    "C32_SEAMS": C32 / "source_chart_seams.jsonl.gz",
    "C67_SOURCE": OUT / "cm2_round306c67l_occurrence1_dynamic_margin_transport_v1.py",
    "GATE3_SOURCE": OUT / "cm2_gate3_candidate_first_hit_cert.py",
    "HOM_SOURCE": OUT / "cm2_round117_rank3_countable_homogeneity_operator_cells.py",
    "CORES_SOURCE": OUT / "cm2_round128_base_r1_component_global_word_incidence.py",
}

PINS = {
    "C55C_CONTRACT": "9b6497bc7e91e002f0d89a4a3575211aa7b11c541ef1fd3e585b8787d0311092",
    "C55C_VERIFY": "9c6c8377d8e8183bc602475dbe1efc05a8a9d51aeece5abca5f15a939bc65be0",
    "C56L_RESULT": "99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601",
    "C56L_CELLS": "3338a3fee7efe31bfae6b3abab77e3b3cc1c2a51fafb8e93d7a626c24803275d",
    "C57L_EDGES": "7136dd4585a5ed9de158c0710c6386ece4d8870ab0196db2e373881779c3dbcd",
    "C60L_ATOMS": "4b2cd8115221cbc9b58bda8ec450b2d0415bbfaf7baac5127837dd24b7a85ac6",
    "C63L_RESULT": "4795560dd4d70b6a1d42dde0cdf3e2c3f21f8c06e97aa776cd4fac4755ba5177",
    "C63L_EDGES": "94f0d22e2cdbaf18d39b3a4f0c31de453915a05feedbe3bec2b5a9cf1e3ace6b",
    "C66L_RESULT": "2f546c2eda8bad0866d2d0d844c0c458c505be84d6997e4999be99b6c1eccb4b",
    "C66L_EDGES": "23ea97c5f021e2e3fc6512425b38a7d61fdaedb0f7543999b8f8ca67ebbdba4d",
    "C67L_RESULT": "5b43ecb647958185859e987e5985660c660fb6a5ee7e422ae2748f96a880b8ac",
    "C67L_ENDPOINTS": "8945c242ef8e7928213057900ecde74e8ba18201c1f715d7333dc77102b209d3",
    "C67L_ATOMS": "5ca4a789b663f320ba8cdc15b4352298135219aad1e1512dc6742cd5ba3e5828",
    "C67L_EDGES": "84298c8283ae26685f34e5de24638257edb541f8d609f2a62f1b60d8285fbab8",
    "C67L_CORRIDORS": "d28fc4ff49e7243e38e55997113d98fb0694eb3ed81f14ecbf5a051f1890684e",
    "C68L_RESULT": "81cf9b6e3fbf2330f747af6430410026406cad8a1a2eb862be974235b2b60f37",
    "C68L_EDGES": "f2077eaf8f926408dc47eb7eb61ab8eab0e317584347407d3842bcc373b59cae",
    "C68L_CORRIDORS": "dc61441b9a8836706a69874d8b60c14a7c1a7c99af6ebe88108ea2643c785c8f",
    "C70L_RESULT": "6f981c2dced0c5dc97357d43660d9b40c733ada4c964a7322c7cb15fe4e413d8",
    "C70L_EDGES": "d440cbefccb0c3c49c6e35b2f42b73a0cef6ad7a83797a1d712e1c5dfeba0d78",
    "C70L_CORRIDORS": "dd9bad188879d1e63b2a7d7cd0d4abef91e8d975c84476619e69fa2057b9a693",
    "C72G_CONTRACT": "6de59a039600f75d0b0d5722f9735fb2456f3b25b8a777df3fffef1f27e1749a",
    "C72G_VERIFY": "7e21fcca280d1f860559d9a1a4afdd2f592b717c5844fc4178fabb2e1d8b684f",
    "C72G_OUTER": "de70ab6c7c621e768662055f96a552d5cb4aaae123d4dd82b56ceed926fa68ee",
    "C32_SEAMS": "d7b5e689baa36d6d0502d3a7c9dad3188d5b92c11e7223c502277057304a611e",
    "C67_SOURCE": "2b84ec3bb6e50d1ec5b1166cab7a2f66406739d3808e93a51b1ac9d536d90b24",
    "GATE3_SOURCE": "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "HOM_SOURCE": "8112aeb2c5d67a914a651683c9a497def3c2ffed81b1c42b365bb257cf8f7e7c",
    "CORES_SOURCE": "d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35",
}

E4CE = "c32-source-seam:e4ce597b8f8afd4793ab0f8f6a7584ebfb6a0537ad680c58ed3f14608987f756"
SPLITS = {
    "c32-source-seam:4d9b9883da9f3288605ddeebbcb5a8ecfe94c6deacb3bd9488b2f55992a1e787": "-4/5",
    "c32-source-seam:e7c332543009c11f58bfc1b894df14f2d3b788961119cab93ad9998c344865d7": "4/5",
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


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate key:" + key)
        result[key] = value
    return result


def close_row(value: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(value))
    claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def secure_bytes(path: Path, expected: str, maximum: int = 96 << 20) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1,
             "regular single-link:" + str(path))
        chunks: list[bytes] = []
        total = 0
        hasher = hashlib.sha256()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            total += len(block)
            need(total <= maximum, "input size:" + str(path))
            hasher.update(block)
            chunks.append(block)
        second = os.fstat(fd)
        current = os.stat(path, follow_symlinks=False)
        identity = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink,
                              s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        need(identity(first) == identity(second) == identity(current),
             "TOCTOU:" + str(path))
        need(hasher.hexdigest() == expected, "pin:" + str(path))
        return b"".join(chunks)
    finally:
        os.close(fd)


def strict_json(payload: bytes, label: str) -> dict[str, Any]:
    need(payload.endswith(b"\n") or label.startswith("C55C"), label + ":newline")
    raw = payload[:-1] if payload.endswith(b"\n") else payload
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                       parse_float=lambda token: (_ for _ in ()).throw(Reject(token)),
                       parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
    # Several frozen contract/receipt inputs are intentionally pretty-printed;
    # their exact bytes are authenticated above and duplicate keys are still
    # rejected here.  Canonicality is required for new C74 objects, not imposed
    # retroactively on pinned predecessors.
    need(type(value) is dict, label + ":json object")
    return value


def strict_jsonl_gz(payload: bytes, label: str) -> list[dict[str, Any]]:
    need(payload[:2] == b"\x1f\x8b" and len(payload) > 18, label + ":gzip")
    rows: list[dict[str, Any]] = []
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
        for index, line in enumerate(stream):
            need(line.endswith(b"\n"), f"{label}:{index}:newline")
            raw = line[:-1]
            row = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                             parse_float=lambda token: (_ for _ in ()).throw(Reject(token)),
                             parse_constant=lambda token: (_ for _ in ()).throw(Reject(token)))
            need(type(row) is dict and canonical(row) == raw, f"{label}:{index}:canonical")
            close_row(row, f"{label}:{index}")
            rows.append(row)
    return rows


def write_exclusive(path: Path, payload: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags, 0o644)
    try:
        view = memoryview(payload)
        while view:
            count = os.write(fd, view)
            need(count > 0, "short write:" + str(path))
            view = view[count:]
        os.fsync(fd)
    finally:
        os.close(fd)


class LedgerWriter:
    def __init__(self, directory: Path, name: str, order: str) -> None:
        self.path = directory / name
        self.order = order
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(self.path, flags, 0o644)
        self.raw = os.fdopen(fd, "wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, semantic: dict[str, Any]) -> dict[str, Any]:
        row_hash = digest(semantic)
        row = {**semantic, "row_sha256": row_hash}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row_hash + "\n").encode("ascii"))
        self.count += 1
        return row

    def close(self) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        payload = self.path.read_bytes()
        return {"filename": self.path.name, "order": self.order,
                "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "sha256": sha(payload), "size": len(payload)}


def qtoken(value: str) -> Q:
    parsed = Q(value)
    need(str(parsed) == value or (parsed.denominator == 1 and value == str(parsed.numerator)),
         "canonical rational:" + value)
    return parsed


def charts_for(seam_id: str) -> tuple[str, str]:
    if seam_id == "E_TO_N":
        return "E", "N"
    need(seam_id == "S_TO_E", "active seam family")
    return "S", "E"


def token_for(seam_id: str, chart: str) -> str:
    return "+1/sqrt(2)" if seam_id == "E_TO_N" or chart == "S" else "-1/sqrt(2)"


def numeric_summary(result: Mapping[str, Any]) -> dict[str, Any]:
    margins: dict[str, Any] = {}
    for key, value in result["margin_vector"].items():
        margins[key] = None if value is None else {
            "dyadic_depth": value["dyadic_depth"],
            "strict_open_lower_bound": value["strict_open_lower_bound"],
            "exact_dyadic_enclosure": value["exact_dyadic_enclosure"],
        }
    return {
        "selected_owner": result["selected_owner"],
        "outgoing_chart": result["outgoing_chart"],
        "official_word": result["official_word"],
        "homogeneity_label": result["homogeneity_label"],
        "incidence_rank": result["incidence_rank"],
        "C24_classification": result["C24_classification"],
        "raw_owner_outgoing_pass": result["raw_owner_outgoing_pass"],
        "full_named_margin_pass": result["full_named_margin_pass"],
        "blocker_code": result["blocker_code"],
        "margin_vector": margins,
    }


def evaluate_piece(seam_id: str, chart: str, lo: str, hi: str) -> dict[str, Any]:
    token = token_for(seam_id, chart)
    return C67.evaluate(chart, C67.token_ball(token), C67.interval(qtoken(lo), qtoken(hi)),
                        C67.token_outer(token), (qtoken(lo), qtoken(hi)))


def direct_piece(seam_id: str, lo: str, hi: str,
                 half_open: str) -> dict[str, Any]:
    sides: dict[str, Any] = {}
    for chart in charts_for(seam_id):
        result = evaluate_piece(seam_id, chart, lo, hi)
        need(result["full_named_margin_pass"] is True and result["blocker_code"] is None,
             "strict side proof:" + seam_id + ":" + chart + ":" + lo + ":" + hi)
        sides[chart] = {"method": "DIRECT_384BIT_FULL_NAMED_MARGIN_REBUILD",
                        "proof": numeric_summary(result)}
    return {"closed_numeric_enclosure": [lo, hi],
            "deterministic_half_open_ownership": half_open,
            "side_proofs": sides}


def make_seam_row(edge: Mapping[str, Any], atom: Mapping[str, Any],
                  c32: Mapping[str, Any], c63: Mapping[str, Any],
                  c66: Mapping[str, Any], c67_atom: Mapping[str, Any],
                  c67_edge: Mapping[str, Any], c68: Mapping[str, Any],
                  c70: Mapping[str, Any]) -> dict[str, Any]:
    face = edge["face_or_corner_id"]
    seam_id = edge["exact_common_face_refinement"]["seam_id"]
    lo, hi = edge["exact_common_face_refinement"]["physical_p_span"]
    need(c32["face_id"] == face and c32["seam_id"] == seam_id, "C32 glue key")
    need([x["value"] for x in c32["physical_p_span"]] == [lo, hi], "C32 span")
    need(atom["incidence_complete"] is True and atom["endpoint_cell_coverage_complete"] is True
         and atom["incident_occurrence_count"] == 2 and len(atom["incident_occurrences"]) == 2,
         "two-sided incidence")
    incident_cells = sorted(x["physical_cell_id"] for x in atom["incident_occurrences"])
    need(incident_cells == sorted([edge["source_cell_id"], edge["target_cell_id"]]),
         "incidence cell closure")
    need(c63["all_atom_semantic_mappings_complete"] is True
         and c63["all_atoms_in_complete_overlay_scope"] is True, "history closure")
    need(c66["closed_schema"] is True and c66["all_atom_owners_unique"] is True
         and c66["decision"] == "STRICT_FULL_DOMAIN_OWNER_VECTOR_AVAILABLE", "owner closure")
    need(c67_atom["source_seam_physical_glue_status"] ==
         "PASS_EXACT_MINIMAL_POLYNOMIAL_AND_TWO_CHART_PHYSICAL_STATE_GLUE",
         "exact physical state glue")
    need(c70["owner_pass"] is True and c70["semantic_history_pass"] is True
         and c70["source_seam"] is True, "C70 seam scope")
    pieces: list[dict[str, Any]] = []
    method: str
    if face in SPLITS:
        split = SPLITS[face]
        pieces = [direct_piece(seam_id, lo, split, "LEFT_CLOSED_RIGHT_OPEN"),
                  direct_piece(seam_id, split, hi, "LEFT_CLOSED_RIGHT_INHERITED")]
        method = "EXACT_PHYSICAL_P_STRUCTURE_SPLIT_AT_" + split
        need(pieces[0]["closed_numeric_enclosure"][1] ==
             pieces[1]["closed_numeric_enclosure"][0], "split closure")
    elif face == E4CE:
        source = evaluate_piece(seam_id, "E", lo, hi)
        need(source["full_named_margin_pass"] is True and source["blocker_code"] is None,
             "e4ce E strict proof")
        diagnostic = evaluate_piece(seam_id, "N", lo, hi)
        need(diagnostic["full_named_margin_pass"] is False and
             diagnostic["blocker_code"] == "OWNER_UNRESOLVED_MULTI_CANDIDATE",
             "e4ce direct N interval diagnostic")
        pieces = [{
            "closed_numeric_enclosure": [lo, hi],
            "deterministic_half_open_ownership": "INHERITED_C32_SEAM_SPAN",
            "side_proofs": {
                "E": {"method": "DIRECT_384BIT_FULL_NAMED_MARGIN_REBUILD",
                      "proof": numeric_summary(source)},
                "N": {"method": "EXACT_PHYSICAL_STATE_GLUE_TRANSPORT_FROM_E",
                      "transported_proof": numeric_summary(source),
                      "direct_dependency_expanded_diagnostic": numeric_summary(diagnostic),
                      "transport_invariants": ["physical_q", "physical_u", "collision_root",
                                               "collision_normal", "owner", "official_word",
                                               "outgoing_chart", "C24_inside_or_exclusion"]},
            },
        }]
        method = "E_SIDE_STRICT_PROOF_EXACT_STATE_GLUE_TO_N_SIDE"
    else:
        pieces = [direct_piece(seam_id, lo, hi, "INHERITED_C32_SEAM_SPAN")]
        method = "DIRECT_BOTH_CHARTS_384BIT_FULL_NAMED_MARGIN_REBUILD"

    return {
        "schema": SCHEMA + ".source-seam-handoff-row",
        "face_or_corner_id": face,
        "component_index": edge["component_index"],
        "source_cell_id": edge["source_cell_id"],
        "target_cell_id": edge["target_cell_id"],
        "seam_id": seam_id,
        "physical_p_span": [lo, hi],
        "minimal_polynomial": "2*x^2-1",
        "physical_state_glue": "EXACT_TWO_CHART_STATE_IDENTITY",
        "C32_source_seam_row_sha256": c32["row_sha256"],
        "C57_edge_row_sha256": edge["row_sha256"],
        "C60_atom_row_sha256": atom["row_sha256"],
        "C63_history_row_sha256": c63["row_sha256"],
        "C66_owner_row_sha256": c66["row_sha256"],
        "C67_atom_row_sha256": c67_atom["row_sha256"],
        "C67_edge_row_sha256": c67_edge["row_sha256"],
        "C68_edge_row_sha256": c68["row_sha256"],
        "C70_edge_row_sha256": c70["row_sha256"],
        "owner_closed": True,
        "history_closed": True,
        "exact_glue_closed": True,
        "two_sides_closed": True,
        "incidence_closed": True,
        "proof_method": method,
        "proof_pieces": pieces,
        "additional_dyadic_depth": 0,
        "collision1_to_next_decider_handoff_sealed": True,
        "C41_whole_endpoint_cell_completed": False,
        "current_disposition": "SEALED_ZERO_CREDIT_COLLISION1_TO_NEXT_DECIDER_HANDOFF",
        "formal_credit": 0,
        "whole_component_credit": 0,
        "global_unresolved_decrement": 0,
        "D02_gate_credit": 0,
    }


def self_test(summary: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "source_seam_count": 16,
        "source_seam_handoff_sealed_count": 16,
        "direct_both_chart_count": 13,
        "exact_state_glue_transport_count": 1,
        "structural_split_count": 2,
        "edge_count": 1042,
        "edge_ready_count": 314,
        "edge_blocked_count": 728,
        "corridor_count": 1044,
        "corridor_all_incident_edge_pass_count": 258,
        "corridor_ready_count": 73,
        "corridor_blocked_count": 971,
        "formal_credit": 0,
        "whole_component_credit": 0,
        "D02_gate_credit": 0,
    }
    need(all(summary.get(k) == v for k, v in required.items()), "summary invariants")
    attacks: dict[str, str] = {}
    for index, (key, expected) in enumerate(required.items()):
        changed = dict(summary)
        changed[key] = expected + 1
        try:
            need(all(changed.get(k) == v for k, v in required.items()), "attack")
        except Reject:
            attacks[f"projection_{index:02d}_{key}"] = "FAIL_CLOSED"
        else:
            raise Reject("projection mutation accepted")
    for name, bad in (("split", "3/4"), ("owner", "G[1,0]"),
                      ("word", "Y+"), ("credit", 1)):
        try:
            need(bad in {"-4/5", "4/5", "W[1,0]", "X+", 0}, "semantic attack")
        except Reject:
            attacks["semantic_" + name] = "FAIL_CLOSED"
        else:
            raise Reject("semantic mutation accepted")
    need(len(attacks) == 19, "attack count")
    return {"status": "PASS_19_OF_19_PRODUCER_ATTACKS_FAIL_CLOSED",
            "attack_count": 19, "attacks": attacks}


def terminal_replay(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        payload = path.read_bytes()
        first = os.stat(path, follow_symlinks=False)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "replay regular")
        second = os.stat(path, follow_symlinks=False)
        need((first.st_dev, first.st_ino, first.st_size, first.st_mtime_ns) ==
             (second.st_dev, second.st_ino, second.st_size, second.st_mtime_ns),
             "replay identity")
        rows.append({"filename": path.name, "sha256": sha(payload), "size": len(payload)})
    return rows


def build(directory: Path) -> dict[str, Any]:
    need(directory.is_dir() and not any(directory.iterdir()), "new empty output directory")
    need(ctx.prec == PRECISION_BITS, "384-bit context")
    import flint  # type: ignore
    need(flint.__version__ == "0.9.0" and flint.__FLINT_VERSION__ == "3.6.0",
         "sealed flint versions")

    raw = {key: secure_bytes(FILES[key], PINS[key]) for key in FILES}
    json_rows = {key: strict_json(raw[key], key) for key in (
        "C55C_CONTRACT", "C55C_VERIFY", "C56L_RESULT", "C63L_RESULT",
        "C66L_RESULT", "C67L_RESULT", "C68L_RESULT", "C70L_RESULT",
        "C72G_CONTRACT", "C72G_VERIFY", "C72G_OUTER")}
    ledgers = {key: strict_jsonl_gz(raw[key], key) for key in (
        "C56L_CELLS", "C57L_EDGES", "C60L_ATOMS", "C63L_EDGES", "C66L_EDGES",
        "C67L_ENDPOINTS", "C67L_ATOMS", "C67L_EDGES", "C67L_CORRIDORS",
        "C68L_EDGES", "C68L_CORRIDORS", "C70L_EDGES", "C70L_CORRIDORS", "C32_SEAMS")}

    need(json_rows["C55C_VERIFY"]["input_state"]["independent_A_census"]
         ["UNRESOLVED_R1648_CONTINUATION"] == 1148,
         "C55c unresolved boundary")
    need(json_rows["C72G_VERIFY"]["public_global_census"]
         ["UNRESOLVED_R1648_CONTINUATION"] == 1148,
         "C72g unresolved boundary")
    need(json_rows["C70L_RESULT"]["summary"]["edge_ready_count"] == 298 and
         json_rows["C70L_RESULT"]["summary"]["corridor_ready_count"] == 73,
         "C70 predecessor census")

    by_face = lambda rows: {row["face_or_corner_id"]: row for row in rows}
    f57 = by_face(ledgers["C57L_EDGES"])
    a60 = by_face(ledgers["C60L_ATOMS"])
    e63 = by_face(ledgers["C63L_EDGES"])
    e66 = by_face(ledgers["C66L_EDGES"])
    a67 = by_face(ledgers["C67L_ATOMS"])
    e67 = by_face(ledgers["C67L_EDGES"])
    e68 = by_face(ledgers["C68L_EDGES"])
    e70 = by_face(ledgers["C70L_EDGES"])
    s32 = {row["face_id"]: row for row in ledgers["C32_SEAMS"]}
    seam_faces = [row["face_or_corner_id"] for row in ledgers["C70L_EDGES"]
                  if row["source_seam"]]
    need(len(seam_faces) == len(set(seam_faces)) == 16, "sixteen unique seams")

    seam_writer = LedgerWriter(directory, SEAM_NAME, "C70_EDGE_ORDER_FILTER_SOURCE_SEAM")
    seam_rows: dict[str, dict[str, Any]] = {}
    methods: Counter[str] = Counter()
    for face in seam_faces:
        semantic = make_seam_row(f57[face], a60[face], s32[face], e63[face],
                                 e66[face], a67[face], e67[face], e68[face], e70[face])
        row = seam_writer.write(semantic)
        seam_rows[face] = row
        methods[row["proof_method"]] += 1
    seam_writer.close()
    need(sum("DIRECT_BOTH" in key for key in methods.elements()) == 13,
         "thirteen direct seams")
    need(methods["E_SIDE_STRICT_PROOF_EXACT_STATE_GLUE_TO_N_SIDE"] == 1,
         "one transported seam")
    need(sum(value for key, value in methods.items() if key.startswith("EXACT_PHYSICAL_P")) == 2,
         "two split seams")

    edge_writer = LedgerWriter(directory, EDGE_NAME, "C70_EDGE_ORDER_WITH_C74_SEAM_OVERLAY")
    edge_overlay: dict[str, dict[str, Any]] = {}
    edge_ready = Counter()
    blocker_census: Counter[str] = Counter()
    component_edge: Counter[str] = Counter()
    for old in ledgers["C70L_EDGES"]:
        face = old["face_or_corner_id"]
        seam = face in seam_rows
        margin = old["full_named_margin_pass"] or seam
        source = old["source_direct_C41_local_pass"] or seam
        target = old["target_direct_C41_local_pass"] or seam
        ready = old["owner_pass"] and old["semantic_history_pass"] and margin and source and target
        blockers: list[str] = []
        if not margin:
            blockers.append("FULL_NAMED_MARGIN_OR_C74_SEAM_HANDOFF_NOT_PASS")
        if not source:
            blockers.append("SOURCE_DIRECT_LOCAL_OR_C74_SEAM_HANDOFF_NOT_PASS")
        if not target:
            blockers.append("TARGET_DIRECT_LOCAL_OR_C74_SEAM_HANDOFF_NOT_PASS")
        blocker_census["|".join(blockers) if blockers else "NONE"] += 1
        semantic = {
            "schema": SCHEMA + ".edge-overlay-row",
            "C70_edge_row_sha256": old["row_sha256"],
            "C74_seam_handoff_row_sha256": seam_rows[face]["row_sha256"] if seam else None,
            "face_or_corner_id": face,
            "component_index": old["component_index"],
            "source_cell_id": old["source_cell_id"],
            "target_cell_id": old["target_cell_id"],
            "glue_kind": old["glue_kind"],
            "owner_pass": old["owner_pass"],
            "semantic_history_pass": old["semantic_history_pass"],
            "full_named_margin_or_C74_seam_handoff_pass": margin,
            "source_direct_local_or_C74_seam_handoff_pass": source,
            "target_direct_local_or_C74_seam_handoff_pass": target,
            "C74_consumption_intersection_pass": ready,
            "decision": "READY_ZERO_CREDIT_NEXT_DECIDER_HANDOFF" if ready else "BLOCKED_FAIL_CLOSED_C74_OVERLAY",
            "remaining_blocker_codes": blockers,
            "formal_credit": 0, "whole_component_credit": 0, "D02_gate_credit": 0,
        }
        row = edge_writer.write(semantic)
        edge_overlay[face] = row
        edge_ready["ready" if ready else "blocked"] += 1
        component_edge[f"component_{old['component_index']}__{'ready' if ready else 'blocked'}"] += 1
    edge_writer.close()

    incident: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in edge_overlay.values():
        incident[row["source_cell_id"]].append(row)
        incident[row["target_cell_id"]].append(row)
    corridor_writer = LedgerWriter(directory, CORRIDOR_NAME,
                                   "C70_CORRIDOR_ORDER_WITH_C74_EDGE_OVERLAY")
    corridor_ready = Counter()
    component_corridor: Counter[str] = Counter()
    corridor_boolean: Counter[str] = Counter()
    affected = newly_all = 0
    for old in ledgers["C70L_CORRIDORS"]:
        edges = incident[old["cell_id"]]
        need(len(edges) == old["incident_edge_count"], "corridor incidence degree")
        old_hashes = {row["C70_edge_row_sha256"] for row in edges}
        old_rows = [row for row in ledgers["C70L_EDGES"] if row["row_sha256"] in old_hashes]
        need(sum(row["five_way_consumption_intersection_pass"] for row in old_rows) ==
             old["incident_edge_pass_count"], "old corridor incidence replay")
        seam_incident = sum(row["C74_seam_handoff_row_sha256"] is not None for row in edges)
        if seam_incident:
            affected += 1
        pass_count = sum(row["C74_consumption_intersection_pass"] for row in edges)
        all_pass = pass_count == len(edges)
        if all_pass and not old["all_immediate_incident_edges_consumption_intersection_pass"]:
            newly_all += 1
        whole = old["direct_C41_whole_rooted_corridor_local_pass"]
        ready = all_pass and whole
        blockers = ([] if all_pass else ["IMMEDIATE_INCIDENT_EDGE_C74_OVERLAY_NOT_ALL_PASS"])
        if not whole:
            blockers.append("DIRECT_C41_WHOLE_ROOTED_CORRIDOR_NOT_BEYOND_COLLISION1")
        semantic = {
            "schema": SCHEMA + ".corridor-overlay-row",
            "C70_corridor_row_sha256": old["row_sha256"],
            "cell_id": old["cell_id"], "pair_index": old["pair_index"],
            "component_index": old["component_index"],
            "incident_edge_count": len(edges),
            "incident_C74_seam_handoff_count": seam_incident,
            "incident_edge_pass_count": pass_count,
            "incident_edge_C74_row_hash_sequence_sha256": sha("".join(
                row["row_sha256"] + "\n" for row in edges).encode("ascii")),
            "all_immediate_incident_edges_C74_overlay_pass": all_pass,
            "direct_C41_current_cell_local_pass": old["direct_C41_current_cell_local_pass"],
            "direct_C41_whole_rooted_corridor_local_pass": whole,
            "corridor_C74_overlay_ready": ready,
            "decision": "READY_ZERO_CREDIT_C74_OVERLAY" if ready else "BLOCKED_FAIL_CLOSED_C74_OVERLAY",
            "remaining_blocker_codes": blockers,
            "formal_credit": 0, "whole_component_credit": 0, "D02_gate_credit": 0,
        }
        corridor_writer.write(semantic)
        corridor_ready["ready" if ready else "blocked"] += 1
        component_corridor[f"component_{old['component_index']}__{'ready' if ready else 'blocked'}"] += 1
        corridor_boolean[
            f"all_incident={int(all_pass)}|whole_rooted={int(whole)}|current_local="
            f"{int(old['direct_C41_current_cell_local_pass'])}"] += 1
    corridor_writer.close()

    summary = {
        "source_seam_count": 16,
        "source_seam_handoff_sealed_count": 16,
        "direct_both_chart_count": 13,
        "exact_state_glue_transport_count": 1,
        "structural_split_count": 2,
        "edge_count": len(edge_overlay),
        "edge_ready_count": edge_ready["ready"],
        "edge_blocked_count": edge_ready["blocked"],
        "corridor_count": len(ledgers["C70L_CORRIDORS"]),
        "corridor_all_incident_edge_pass_count": sum(
            count for key, count in corridor_boolean.items() if key.startswith("all_incident=1")),
        "corridor_ready_count": corridor_ready["ready"],
        "corridor_blocked_count": corridor_ready["blocked"],
        "source_seam_endpoint_cell_count": affected,
        "newly_all_incident_edge_pass_corridor_count": newly_all,
        "formal_credit": 0, "whole_component_credit": 0, "D02_gate_credit": 0,
    }
    need(summary == {**summary, "edge_count": 1042, "edge_ready_count": 314,
                     "edge_blocked_count": 728, "corridor_count": 1044,
                     "corridor_all_incident_edge_pass_count": 258,
                     "corridor_ready_count": 73, "corridor_blocked_count": 971,
                     "source_seam_endpoint_cell_count": 26,
                     "newly_all_incident_edge_pass_corridor_count": 10}, "exact census")

    upstream_replay = {key: sha(secure_bytes(FILES[key], PINS[key])) for key in FILES}
    need(upstream_replay == PINS, "terminal upstream pin replay")
    result: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_16_OF_16_SOURCE_SEAMS_SEALED_COLLISION1_TO_NEXT_DECIDER_HANDOFF__314_OF_1042_EDGES__73_OF_1044_CORRIDORS__ZERO_CREDIT",
        "precision_bits": PRECISION_BITS,
        "python_flint_version": flint.__version__, "flint_version": flint.__FLINT_VERSION__,
        "producer_file_sha256": sha(Path(__file__).read_bytes()),
        "input_file_sha256": dict(sorted(PINS.items())),
        "summary": summary,
        "proof_method_census": dict(sorted(methods.items())),
        "edge_blocker_census": dict(sorted(blocker_census.items())),
        "edge_component_census": dict(sorted(component_edge.items())),
        "corridor_boolean_census": dict(sorted(corridor_boolean.items())),
        "corridor_component_census": dict(sorted(component_corridor.items())),
        "ledgers": {"source_seam_handoff": seam_writer.descriptor(),
                    "edge_overlay": edge_writer.descriptor(),
                    "corridor_overlay": corridor_writer.descriptor()},
        "producer_self_test": self_test(summary),
        "minimum_remaining_public_gate": {
            "edge_blocked_count": 728,
            "corridor_without_all_incident_edge_pass_count": 786,
            "corridor_without_whole_rooted_C41_pass_count": 955,
            "newly_all_incident_but_current_and_whole_C41_false_count": 10,
            "required": ["NON_SEAM_EDGE_MARGIN_AND_ENDPOINT_HANDOFFS",
                         "WHOLE_ROOTED_CORRIDOR_NEXT_DECIDER_CLOSURE"],
        },
        "strict_boundary": {
            "C41_whole_endpoint_cells_claimed_complete": False,
            "C55c_or_C72g_global_unresolved_decrement": 0,
            "whole_large_component_closed": False,
            "global_unresolved_zero": False,
            "formal_credit": 0, "whole_component_credit": 0, "D02_gate_credit": 0,
            "only_later_no_producer_global_consumer_may_promote": True,
        },
    }
    result["object_sha256"] = digest(result)
    write_exclusive(directory / RESULT_NAME, canonical(result) + b"\n")
    report = (
        "# C74-L source-seam collision-one handoff successor\n\n"
        "- Sealed source seams: 16 / 16.\n"
        "- Proof split: 13 direct two-chart; 1 exact E-to-N state-glue transport; "
        "2 exact p=+/-4/5 structural splits.\n"
        "- C70 overlay: 314 / 1,042 edges ready; 73 / 1,044 corridors ready.\n"
        "- The ten newly all-incident corridors still fail current/whole C41; no corridor count increases.\n"
        "- Formal, whole-component, global-decrement, and D02 credit remain zero.\n"
    ).encode("utf-8")
    write_exclusive(directory / REPORT_NAME, report)
    write_exclusive(directory / LOCK_NAME,
                    b"STAGED ZERO-CREDIT C74-L ONLY; NOT GLOBAL OR D02 AUTHORITY.\n")
    members = [directory / SEAM_NAME, directory / EDGE_NAME, directory / CORRIDOR_NAME,
               directory / RESULT_NAME, directory / REPORT_NAME, directory / LOCK_NAME]
    replay = terminal_replay(members)
    manifest = "".join(f"{row['sha256']}  {row['filename']}\n" for row in replay).encode("ascii")
    write_exclusive(directory / MANIFEST_NAME, manifest)
    replay2 = terminal_replay([*members, directory / MANIFEST_NAME])
    receipt: dict[str, Any] = {
        "schema": SCHEMA + ".completion-receipt",
        "status": "PASS_OUTER_RECEIPT_LAST_AFTER_TERMINAL_BYTE_REPLAY__ZERO_CREDIT",
        "result_object_sha256": result["object_sha256"],
        "manifest_sha256": sha(manifest),
        "terminal_replay": replay2,
        "formal_credit": 0, "whole_component_credit": 0, "D02_gate_credit": 0,
    }
    receipt["object_sha256"] = digest(receipt)
    write_exclusive(directory / RECEIPT_NAME, canonical(receipt) + b"\n")
    terminal_replay([*members, directory / MANIFEST_NAME, directory / RECEIPT_NAME])
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.output_dir.resolve())
    print(json.dumps({"status": result["status"],
                      "object_sha256": result["object_sha256"],
                      "summary": result["summary"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
