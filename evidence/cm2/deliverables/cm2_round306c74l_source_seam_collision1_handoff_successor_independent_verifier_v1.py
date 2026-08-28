#!/usr/bin/env python3
"""Independent no-C74-producer verifier for the C74-L seam successor.

The C74 producer is neither opened, read, decoded, compiled, imported, nor
executed.  Candidate bytes are reconstructed from frozen upstream ledgers and
the pinned C67 numerical certificate kernel at 384-bit precision.
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
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
SELF = Path(__file__).resolve()
FLINT_SITE = ROOT / ".cm2-runtime/python-flint-0.9.0/lib/python3.12/site-packages"
for entry in (str(FLINT_SITE), str(OUT)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from flint import ctx  # type: ignore
ctx.prec = 384
import cm2_round306c67l_occurrence1_dynamic_margin_transport_v1 as C67

SCHEMA = "cm2.round306c74l.source-seam-collision1-handoff-successor.v1"
PREFIX = "cm2_round306c74l_source_seam_collision1_handoff_successor_v1"
NAMES = {
    "seam": PREFIX + "_source_seam_handoff.jsonl.gz",
    "edge": PREFIX + "_edge_overlay.jsonl.gz",
    "corridor": PREFIX + "_corridor_overlay.jsonl.gz",
    "result": PREFIX + "_result.json",
    "report": PREFIX + "_report.md",
    "manifest": PREFIX + "_manifest.sha256",
    "receipt": PREFIX + "_completion_receipt.json",
    "lock": "ZERO_CREDIT_STAGED_C74L_ONLY.lock",
}
CANDIDATE_PINS = {
    "seam": "394c59426fa47151452829b514ad84c6377e5ea2e7aabf80343a0bb9c5d02dc0",
    "edge": "ef24f61383f6fa63f45c45a323043391402e4fa3d4c36cceca5f4083dd9625c4",
    "corridor": "741e5afae56ad96bc8471a81dceaae8e4766d0bf475b2d99c10e465284749d9f",
    "result": "53732dbd4d3be61f26a4aba74952c2aef40684c9d2fb23bd9bd6692917fc5b8d",
    "report": "924d5f8e2e398e1ce3a1faff082fe1d95e2f5ec64893974bf11f88b74c277b93",
    "manifest": "6b02a113c1e21392bad6b2f6070629ed7a29b18bcca527db4f3e47145b461a06",
    "receipt": "48ea30873a5ce8f8cc8ee970f43bc9886030ff58bc67f1ebf7af24d6a06fca2d",
    "lock": "96bc25952f0f542de585ef7eae0504e0f06f543df12631d21b105112e4f22e32",
}
EXPECTED_RESULT_OBJECT = "cd5f924ff0ef3a776480aeba508ba6136791d161a650a098baeb8f025e3c7833"
EXPECTED_C74_PRODUCER_SHA256_DECLARATION_ONLY = "fda9ed711bd61f867f0ccd055ea8699b963c859635b4f71db900e47b04fb2cb4"
VERIFICATION_STEM = "cm2_round306c74l_source_seam_collision1_handoff_successor"
OLD_VERIFICATION_NAME = VERIFICATION_STEM + "_independent_verification_v1.json"
CORRECTED_VERIFICATION_NAME = VERIFICATION_STEM + "_independent_verification_v1_1.json"
MISNAMED_SELF_BOUND_VERIFICATION_NAME = PREFIX + "_independent_verification_v1_1.json"
SUPERSESSION_NAME = VERIFICATION_STEM + "_independent_verification_v1_SUPERSEDED_BY_v1_1.json"
DUAL_RECEIPT_NAME = VERIFICATION_STEM + "_dual_completion_receipt_v1.json"
OLD_VERIFICATION_SHA256 = "748dfb2be626bc1920a0d21bd936c708e35356813a5eb38a6263ecca79518d37"
OLD_VERIFICATION_OBJECT_SHA256 = "7fdab7f412f9cbcea4ff7d5809c62ca47d5663c7ad0ac4b772a144fbeda617aa"
MISNAMED_SELF_BOUND_VERIFICATION_SHA256 = "f0ee22df980db6886dd73e014796418512925d28dce37d1be0caf04d293310e5"
MISNAMED_SELF_BOUND_VERIFICATION_OBJECT_SHA256 = "5b80f45be05a9cf9aabd333e1d678e1183eae1b95306b31ef9dbfa03aceb78bb"
REJECTED_BUILD_MARKER = ROOT / ".cm2-runtime/c74l-build-a.AhIq8h/REJECTED_SUPERSEDED_INCOMPLETE.txt"
REJECTED_BUILD_MARKER_SHA256 = "adf6dd2e84bc7a313960835bea215f2c6cb8e5a130ad69dc234a5b1eb3ee73d0"

C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9"
FILES = {
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


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate:" + key)
        result[key] = value
    return result


def secure(path: Path, expected: str, maximum: int = 96 << 20) -> bytes:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1, "regular:" + str(path))
        data = bytearray()
        h = hashlib.sha256()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            data.extend(block); h.update(block)
            need(len(data) <= maximum, "size:" + str(path))
        second = os.fstat(fd); third = os.stat(path, follow_symlinks=False)
        ident = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
                           s.st_mtime_ns, s.st_ctime_ns)
        need(ident(first) == ident(second) == ident(third), "TOCTOU:" + str(path))
        need(h.hexdigest() == expected, "pin:" + str(path))
        return bytes(data)
    finally:
        os.close(fd)


def secure_capture(path: Path, maximum: int = 8 << 20) -> tuple[bytes, str]:
    """Capture an unpinned new source/output with the same TOCTOU rules."""
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        first = os.fstat(fd)
        need(stat.S_ISREG(first.st_mode) and first.st_nlink == 1,
             "capture regular:" + str(path))
        data = bytearray(); h = hashlib.sha256()
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            data.extend(block); h.update(block)
            need(len(data) <= maximum, "capture size:" + str(path))
        second = os.fstat(fd); third = os.stat(path, follow_symlinks=False)
        ident = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
                           s.st_mtime_ns, s.st_ctime_ns)
        need(ident(first) == ident(second) == ident(third),
             "capture TOCTOU:" + str(path))
        return bytes(data), h.hexdigest()
    finally:
        os.close(fd)


def parse_json(payload: bytes, label: str, canonical_required: bool = True) -> dict[str, Any]:
    raw = payload[:-1] if payload.endswith(b"\n") else payload
    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates,
                       parse_float=lambda x: (_ for _ in ()).throw(Reject(x)),
                       parse_constant=lambda x: (_ for _ in ()).throw(Reject(x)))
    need(type(value) is dict, label + ":object")
    if canonical_required:
        need(canonical(value) == raw, label + ":canonical")
    return value


def close_row(row: Mapping[str, Any], label: str) -> None:
    body = copy.deepcopy(dict(row)); claim = body.pop("row_sha256", None)
    need(type(claim) is str and claim == digest(body), label + ":row closure")


def parse_gz(payload: bytes, label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with gzip.GzipFile(fileobj=io.BytesIO(payload), mode="rb") as stream:
        for index, line in enumerate(stream):
            need(line.endswith(b"\n"), label + ":newline")
            row = parse_json(line, f"{label}:{index}")
            close_row(row, f"{label}:{index}")
            rows.append(row)
    return rows


def qtoken(token: str) -> Q:
    value = Q(token)
    need(str(value) == token, "rational token")
    return value


def token_for(seam: str, chart: str) -> str:
    return "+1/sqrt(2)" if seam == "E_TO_N" or chart == "S" else "-1/sqrt(2)"


def charts(seam: str) -> tuple[str, str]:
    need(seam in {"E_TO_N", "S_TO_E"}, "seam family")
    return ("E", "N") if seam == "E_TO_N" else ("S", "E")


def summarize(result: Mapping[str, Any]) -> dict[str, Any]:
    vector: dict[str, Any] = {}
    for key, value in result["margin_vector"].items():
        vector[key] = None if value is None else {
            "dyadic_depth": value["dyadic_depth"],
            "strict_open_lower_bound": value["strict_open_lower_bound"],
            "exact_dyadic_enclosure": value["exact_dyadic_enclosure"],
        }
    return {"selected_owner": result["selected_owner"],
            "outgoing_chart": result["outgoing_chart"],
            "official_word": result["official_word"],
            "homogeneity_label": result["homogeneity_label"],
            "incidence_rank": result["incidence_rank"],
            "C24_classification": result["C24_classification"],
            "raw_owner_outgoing_pass": result["raw_owner_outgoing_pass"],
            "full_named_margin_pass": result["full_named_margin_pass"],
            "blocker_code": result["blocker_code"], "margin_vector": vector}


def evaluate(seam: str, chart: str, lo: str, hi: str) -> dict[str, Any]:
    token = token_for(seam, chart)
    return C67.evaluate(chart, C67.token_ball(token), C67.interval(qtoken(lo), qtoken(hi)),
                        C67.token_outer(token), (qtoken(lo), qtoken(hi)))


def verify_seam_numeric(row: Mapping[str, Any]) -> None:
    face = row["face_or_corner_id"]; seam = row["seam_id"]
    lo, hi = row["physical_p_span"]
    pieces = row["proof_pieces"]
    if face in SPLITS:
        split = SPLITS[face]
        need(len(pieces) == 2 and pieces[0]["closed_numeric_enclosure"] == [lo, split]
             and pieces[1]["closed_numeric_enclosure"] == [split, hi], "split partition")
        expected_owners = ["LEFT_CLOSED_RIGHT_OPEN", "LEFT_CLOSED_RIGHT_INHERITED"]
        for piece, ownership in zip(pieces, expected_owners):
            need(piece["deterministic_half_open_ownership"] == ownership, "half-open owner")
            a, b = piece["closed_numeric_enclosure"]
            for chart in charts(seam):
                rebuilt = evaluate(seam, chart, a, b)
                need(rebuilt["full_named_margin_pass"] is True and rebuilt["blocker_code"] is None,
                     "split numeric strict")
                need(piece["side_proofs"][chart]["method"] ==
                     "DIRECT_384BIT_FULL_NAMED_MARGIN_REBUILD" and
                     piece["side_proofs"][chart]["proof"] == summarize(rebuilt),
                     "split numeric bytes")
    elif face == E4CE:
        need(len(pieces) == 1, "e4ce piece count")
        direct = evaluate(seam, "E", lo, hi); diagnostic = evaluate(seam, "N", lo, hi)
        need(direct["full_named_margin_pass"] is True and direct["blocker_code"] is None,
             "e4ce direct strict")
        need(diagnostic["full_named_margin_pass"] is False and
             diagnostic["blocker_code"] == "OWNER_UNRESOLVED_MULTI_CANDIDATE",
             "e4ce diagnostic")
        sides = pieces[0]["side_proofs"]
        need(sides["E"]["proof"] == summarize(direct) and
             sides["N"]["transported_proof"] == summarize(direct) and
             sides["N"]["direct_dependency_expanded_diagnostic"] == summarize(diagnostic),
             "e4ce exact transport")
    else:
        need(len(pieces) == 1, "direct piece count")
        for chart in charts(seam):
            rebuilt = evaluate(seam, chart, lo, hi)
            need(rebuilt["full_named_margin_pass"] is True and rebuilt["blocker_code"] is None,
                 "direct numeric strict")
            need(pieces[0]["side_proofs"][chart]["proof"] == summarize(rebuilt),
                 "direct numeric bytes")


def validate_projection(summary: Mapping[str, Any], seam: Mapping[str, Any]) -> None:
    required = {"source_seam_count": 16, "source_seam_handoff_sealed_count": 16,
                "direct_both_chart_count": 13, "exact_state_glue_transport_count": 1,
                "structural_split_count": 2, "edge_count": 1042,
                "edge_ready_count": 314, "edge_blocked_count": 728,
                "corridor_count": 1044, "corridor_all_incident_edge_pass_count": 258,
                "corridor_ready_count": 73, "corridor_blocked_count": 971,
                "formal_credit": 0, "whole_component_credit": 0, "D02_gate_credit": 0}
    need(all(summary.get(k) == v for k, v in required.items()), "projection summary")
    for key in ("owner_closed", "history_closed", "exact_glue_closed", "two_sides_closed",
                "incidence_closed", "collision1_to_next_decider_handoff_sealed"):
        need(seam.get(key) is True, "projection seam:" + key)
    need(seam.get("C41_whole_endpoint_cell_completed") is False and
         seam.get("formal_credit") == seam.get("whole_component_credit") ==
         seam.get("global_unresolved_decrement") == seam.get("D02_gate_credit") == 0,
         "projection zero boundary")


def coherent_attacks(summary: Mapping[str, Any], seam: Mapping[str, Any]) -> dict[str, Any]:
    attacks: dict[str, str] = {}
    summary_keys = ["source_seam_count", "source_seam_handoff_sealed_count",
                    "direct_both_chart_count", "exact_state_glue_transport_count",
                    "structural_split_count", "edge_count", "edge_ready_count",
                    "edge_blocked_count", "corridor_count",
                    "corridor_all_incident_edge_pass_count", "corridor_ready_count",
                    "corridor_blocked_count", "formal_credit", "whole_component_credit",
                    "D02_gate_credit"]
    for key in summary_keys:
        bad = copy.deepcopy(dict(summary)); bad[key] += 1
        try:
            validate_projection(bad, seam)
        except Reject:
            attacks["summary_" + key] = "FAIL_CLOSED"
        else:
            raise Reject("summary attack accepted")
    seam_mutations = ["owner_closed", "history_closed", "exact_glue_closed",
                      "two_sides_closed", "incidence_closed",
                      "collision1_to_next_decider_handoff_sealed"]
    for key in seam_mutations:
        bad = copy.deepcopy(dict(seam)); bad[key] = False
        try:
            validate_projection(summary, bad)
        except Reject:
            attacks["seam_" + key] = "FAIL_CLOSED"
        else:
            raise Reject("seam attack accepted")
    for key in ("formal_credit", "whole_component_credit", "global_unresolved_decrement",
                "D02_gate_credit"):
        bad = copy.deepcopy(dict(seam)); bad[key] = 1
        try:
            validate_projection(summary, bad)
        except Reject:
            attacks["seam_" + key] = "FAIL_CLOSED"
        else:
            raise Reject("credit attack accepted")
    need(len(attacks) == 25, "25 attacks")
    return {"status": "PASS_25_OF_25_COHERENT_ATTACKS_FAIL_CLOSED",
            "attack_count": 25, "attacks": attacks}


def write_exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        view = memoryview(payload)
        while view:
            count = os.write(fd, view); need(count > 0, "write")
            view = view[count:]
        os.fsync(fd)
    finally:
        os.close(fd)


def verify(candidate: Path, output: Path) -> dict[str, Any]:
    import flint  # type: ignore
    need(ctx.prec == 384 and flint.__version__ == "0.9.0" and
         flint.__FLINT_VERSION__ == "3.6.0", "numeric environment")
    need(output.name == CORRECTED_VERIFICATION_NAME,
         "corrected append-only verification filename")
    verifier_source_before, verifier_file_sha256 = secure_capture(SELF)

    upstream = {key: secure(path, PINS[key]) for key, path in FILES.items()}
    candidate_raw = {key: secure(candidate / name, CANDIDATE_PINS[key])
                     for key, name in NAMES.items()}
    seams = parse_gz(candidate_raw["seam"], "candidate seam")
    edges = parse_gz(candidate_raw["edge"], "candidate edge")
    corridors = parse_gz(candidate_raw["corridor"], "candidate corridor")
    result = parse_json(candidate_raw["result"], "candidate result")
    receipt = parse_json(candidate_raw["receipt"], "candidate receipt")
    body = copy.deepcopy(result); claim = body.pop("object_sha256")
    need(claim == EXPECTED_RESULT_OBJECT == digest(body), "result object closure")
    body = copy.deepcopy(receipt); rclaim = body.pop("object_sha256")
    need(rclaim == digest(body), "receipt closure")
    need(receipt["result_object_sha256"] == EXPECTED_RESULT_OBJECT and
         receipt["manifest_sha256"] == CANDIDATE_PINS["manifest"], "receipt binding")
    need(result["producer_file_sha256"] == EXPECTED_C74_PRODUCER_SHA256_DECLARATION_ONLY,
         "declared producer hash")
    need(result["input_file_sha256"] == dict(sorted(PINS.items())), "upstream pin map")
    need(result["strict_boundary"]["formal_credit"] == 0 and
         result["strict_boundary"]["whole_component_credit"] == 0 and
         result["strict_boundary"]["D02_gate_credit"] == 0 and
         result["strict_boundary"]["global_unresolved_zero"] is False,
         "result zero boundary")

    def ledger(key: str) -> list[dict[str, Any]]:
        return parse_gz(upstream[key], key)
    f57 = {x["face_or_corner_id"]: x for x in ledger("C57L_EDGES")}
    a60 = {x["face_or_corner_id"]: x for x in ledger("C60L_ATOMS")}
    e63 = {x["face_or_corner_id"]: x for x in ledger("C63L_EDGES")}
    e66 = {x["face_or_corner_id"]: x for x in ledger("C66L_EDGES")}
    a67 = {x["face_or_corner_id"]: x for x in ledger("C67L_ATOMS")}
    e67 = {x["face_or_corner_id"]: x for x in ledger("C67L_EDGES")}
    e68 = {x["face_or_corner_id"]: x for x in ledger("C68L_EDGES")}
    old_edges = ledger("C70L_EDGES")
    old_corridors = ledger("C70L_CORRIDORS")
    e70 = {x["face_or_corner_id"]: x for x in old_edges}
    s32 = {x["face_id"]: x for x in ledger("C32_SEAMS")}
    need(len(seams) == 16 and len(edges) == 1042 and len(corridors) == 1044,
         "candidate row counts")

    seam_map = {x["face_or_corner_id"]: x for x in seams}
    need(len(seam_map) == 16, "seam keys")
    for face, row in seam_map.items():
        old = f57[face]; atom = a60[face]
        need(row["C32_source_seam_row_sha256"] == s32[face]["row_sha256"] and
             row["C57_edge_row_sha256"] == old["row_sha256"] and
             row["C60_atom_row_sha256"] == atom["row_sha256"] and
             row["C63_history_row_sha256"] == e63[face]["row_sha256"] and
             row["C66_owner_row_sha256"] == e66[face]["row_sha256"] and
             row["C67_atom_row_sha256"] == a67[face]["row_sha256"] and
             row["C67_edge_row_sha256"] == e67[face]["row_sha256"] and
             row["C68_edge_row_sha256"] == e68[face]["row_sha256"] and
             row["C70_edge_row_sha256"] == e70[face]["row_sha256"], "seam joins")
        need(atom["incidence_complete"] is True and atom["incident_occurrence_count"] == 2 and
             sorted(x["physical_cell_id"] for x in atom["incident_occurrences"]) ==
             sorted([row["source_cell_id"], row["target_cell_id"]]), "seam incidence")
        need(e63[face]["all_atom_semantic_mappings_complete"] is True and
             e63[face]["all_atoms_in_complete_overlay_scope"] is True and
             e66[face]["closed_schema"] is True and
             e66[face]["all_atom_owners_unique"] is True and
             a67[face]["source_seam_physical_glue_status"] ==
             "PASS_EXACT_MINIMAL_POLYNOMIAL_AND_TWO_CHART_PHYSICAL_STATE_GLUE",
             "owner history glue")
        validate_projection(result["summary"], row)
        verify_seam_numeric(row)

    edge_map = {x["face_or_corner_id"]: x for x in edges}
    need(len(edge_map) == 1042, "edge keys")
    ready_count = 0
    for old in old_edges:
        row = edge_map[old["face_or_corner_id"]]
        seam = old["face_or_corner_id"] in seam_map
        expected = old["five_way_consumption_intersection_pass"] or seam
        need(row["C70_edge_row_sha256"] == old["row_sha256"] and
             (row["C74_seam_handoff_row_sha256"] is not None) == seam and
             row["owner_pass"] == old["owner_pass"] and
             row["semantic_history_pass"] == old["semantic_history_pass"] and
             row["full_named_margin_or_C74_seam_handoff_pass"] ==
             (old["full_named_margin_pass"] or seam) and
             row["source_direct_local_or_C74_seam_handoff_pass"] ==
             (old["source_direct_C41_local_pass"] or seam) and
             row["target_direct_local_or_C74_seam_handoff_pass"] ==
             (old["target_direct_C41_local_pass"] or seam) and
             row["C74_consumption_intersection_pass"] == expected, "edge rebuild")
        ready_count += expected
    need(ready_count == 314, "edge census")

    incident: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in edges:
        incident[row["source_cell_id"]].append(row)
        incident[row["target_cell_id"]].append(row)
    corridor_map = {x["cell_id"]: x for x in corridors}
    ready_corridor = all_incident = newly_all = affected = 0
    for old in old_corridors:
        row = corridor_map[old["cell_id"]]; joined = incident[old["cell_id"]]
        need(len(joined) == old["incident_edge_count"], "corridor degree")
        count = sum(x["C74_consumption_intersection_pass"] for x in joined)
        all_pass = count == len(joined)
        ready = all_pass and old["direct_C41_whole_rooted_corridor_local_pass"]
        seam_count = sum(x["C74_seam_handoff_row_sha256"] is not None for x in joined)
        need(row["C70_corridor_row_sha256"] == old["row_sha256"] and
             row["incident_edge_count"] == len(joined) and
             row["incident_C74_seam_handoff_count"] == seam_count and
             row["incident_edge_pass_count"] == count and
             row["all_immediate_incident_edges_C74_overlay_pass"] == all_pass and
             row["direct_C41_current_cell_local_pass"] ==
             old["direct_C41_current_cell_local_pass"] and
             row["direct_C41_whole_rooted_corridor_local_pass"] ==
             old["direct_C41_whole_rooted_corridor_local_pass"] and
             row["corridor_C74_overlay_ready"] == ready, "corridor rebuild")
        ready_corridor += ready; all_incident += all_pass; affected += seam_count > 0
        newly_all += all_pass and not old["all_immediate_incident_edges_consumption_intersection_pass"]
    need((ready_corridor, all_incident, affected, newly_all) == (73, 258, 26, 10),
         "corridor census")

    attacks = coherent_attacks(result["summary"], seams[0])
    # Fresh terminal-byte and identity recapture of every candidate member.
    recaptured = {key: hashlib.sha256(secure(candidate / NAMES[key], CANDIDATE_PINS[key])).hexdigest()
                  for key in NAMES}
    need(recaptured == CANDIDATE_PINS, "candidate terminal recapture")
    need({key: hashlib.sha256(secure(FILES[key], PINS[key])).hexdigest() for key in FILES} == PINS,
         "upstream terminal recapture")

    verification: dict[str, Any] = {
        "schema": SCHEMA + ".independent-verification",
        "status": "PASS_NO_C74_PRODUCER_REBUILD__16_OF_16_SEAMS__1042_EDGES__1044_CORRIDORS__25_OF_25_ATTACKS__ZERO_CREDIT",
        "candidate_result_file_sha256": CANDIDATE_PINS["result"],
        "candidate_result_object_sha256": EXPECTED_RESULT_OBJECT,
        "candidate_file_sha256": dict(sorted(CANDIDATE_PINS.items())),
        "declared_C74_producer_sha256": EXPECTED_C74_PRODUCER_SHA256_DECLARATION_ONLY,
        "verifier_file_sha256": verifier_file_sha256,
        "verifier_source_terminal_replay": {
            "before_verification_publish": True,
            "after_verification_publish": True,
            "byte_identical": True,
            "sha256": verifier_file_sha256,
        },
        "C74_producer_opened_read_decoded_compiled_imported_or_executed": False,
        "upstream_C67_numeric_certificate_kernel_imported": True,
        "precision_bits": 384, "python_flint_version": flint.__version__,
        "numeric_rebuild": {"source_seam_count": 16,
                            "source_seam_handoff_sealed_count": 16,
                            "edge_ready_count": ready_count,
                            "edge_blocked_count": 1042 - ready_count,
                            "corridor_all_incident_edge_pass_count": all_incident,
                            "corridor_ready_count": ready_corridor,
                            "corridor_blocked_count": 1044 - ready_corridor,
                            "affected_endpoint_cell_count": affected,
                            "newly_all_incident_but_not_whole_count": newly_all},
        "closure": {"owner": True, "history": True, "exact_glue": True,
                    "two_sides": True, "incidence": True,
                    "terminal_byte_replay": True},
        "coherent_attacks": attacks,
        "strict_boundary": {"whole_large_component_closed": False,
                            "global_unresolved_decrement": 0,
                            "formal_credit": 0, "whole_component_credit": 0,
                            "D02_gate_credit": 0},
    }
    verification["object_sha256"] = digest(verification)
    payload = canonical(verification) + b"\n"
    write_exclusive(output, payload)
    need(secure(output, hashlib.sha256(payload).hexdigest()) == payload,
         "verification terminal replay")
    verifier_source_after, verifier_file_sha256_after = secure_capture(SELF)
    need(verifier_source_after == verifier_source_before and
         verifier_file_sha256_after == verifier_file_sha256,
         "verifier source terminal replay")
    return verification


def finalize_dual(stage_a: Path, stage_b: Path) -> dict[str, Any]:
    """Append identical supersession markers and outer dual receipts."""
    source_before, verifier_hash = secure_capture(SELF)
    rejected_marker = secure(REJECTED_BUILD_MARKER, REJECTED_BUILD_MARKER_SHA256)
    need(rejected_marker.endswith(b"A corrected run must use a fresh output directory.\n"),
         "rejected build marker semantics")

    # Bind the eight producer members and the rejected first verification in
    # both stages before publishing any new finalization bytes.
    for stage in (stage_a, stage_b):
        need(stage.is_dir(), "dual stage directory")
        for key, name in NAMES.items():
            secure(stage / name, CANDIDATE_PINS[key])
        secure(stage / OLD_VERIFICATION_NAME, OLD_VERIFICATION_SHA256)
        secure(stage / MISNAMED_SELF_BOUND_VERIFICATION_NAME,
               MISNAMED_SELF_BOUND_VERIFICATION_SHA256)
        need(not (stage / SUPERSESSION_NAME).exists() and
             not (stage / DUAL_RECEIPT_NAME).exists(), "append-only final targets")

    corrected_a, corrected_hash_a = secure_capture(stage_a / CORRECTED_VERIFICATION_NAME)
    corrected_b, corrected_hash_b = secure_capture(stage_b / CORRECTED_VERIFICATION_NAME)
    need(corrected_a == corrected_b and corrected_hash_a == corrected_hash_b,
         "corrected dual verification bytes")
    corrected = parse_json(corrected_a, "corrected verification")
    corrected_body = copy.deepcopy(corrected)
    corrected_object = corrected_body.pop("object_sha256", None)
    need(corrected_object == digest(corrected_body), "corrected object closure")
    need(corrected["verifier_file_sha256"] == verifier_hash and
         corrected["verifier_source_terminal_replay"] == {
             "before_verification_publish": True,
             "after_verification_publish": True,
             "byte_identical": True,
             "sha256": verifier_hash,
         }, "corrected verifier self binding")
    need(corrected["C74_producer_opened_read_decoded_compiled_imported_or_executed"] is False,
         "no C74 producer")

    marker: dict[str, Any] = {
        "schema": SCHEMA + ".verification-supersession",
        "status": "OLD_V1_VERIFICATION_REJECTED_SUPERSEDED_BY_SELF_BOUND_V1_1",
        "old_verification_filename": OLD_VERIFICATION_NAME,
        "old_verification_file_sha256": OLD_VERIFICATION_SHA256,
        "old_verification_object_sha256": OLD_VERIFICATION_OBJECT_SHA256,
        "old_verification_rejection_reason":
            "MISSING_VERIFIER_FILE_SHA256_AND_SOURCE_TERMINAL_RECAPTURE",
        "misnamed_self_bound_verification_filename": MISNAMED_SELF_BOUND_VERIFICATION_NAME,
        "misnamed_self_bound_verification_file_sha256":
            MISNAMED_SELF_BOUND_VERIFICATION_SHA256,
        "misnamed_self_bound_verification_object_sha256":
            MISNAMED_SELF_BOUND_VERIFICATION_OBJECT_SHA256,
        "misnamed_self_bound_verification_rejection_reason":
            "NONCANONICAL_BASENAME_WITH_DUPLICATED_V1_SEGMENT",
        "corrected_verification_filename": CORRECTED_VERIFICATION_NAME,
        "corrected_verification_file_sha256": corrected_hash_a,
        "corrected_verification_object_sha256": corrected_object,
        "verifier_file_sha256": verifier_hash,
        "earlier_incomplete_build_rejection_marker_sha256": REJECTED_BUILD_MARKER_SHA256,
        "formal_credit": 0, "whole_component_credit": 0,
        "global_unresolved_decrement": 0, "D02_gate_credit": 0,
    }
    marker["object_sha256"] = digest(marker)
    marker_payload = canonical(marker) + b"\n"
    marker_hash = hashlib.sha256(marker_payload).hexdigest()
    for stage in (stage_a, stage_b):
        write_exclusive(stage / SUPERSESSION_NAME, marker_payload)
        need(secure(stage / SUPERSESSION_NAME, marker_hash) == marker_payload,
             "marker terminal replay")

    producer_members = [
        {"role": key, "filename": NAMES[key], "sha256": CANDIDATE_PINS[key]}
        for key in sorted(NAMES)
    ]
    member_sequence = hashlib.sha256("".join(
        row["sha256"] + "  " + row["filename"] + "\n" for row in producer_members
    ).encode("ascii")).hexdigest()
    receipt: dict[str, Any] = {
        "schema": SCHEMA + ".dual-completion-receipt",
        "status": "PASS_DUAL_STAGE_BYTE_IDENTICAL_SELF_BOUND_VERIFICATION_AND_SUPERSESSION__ZERO_CREDIT",
        "producer_member_count_per_stage": 8,
        "producer_members": producer_members,
        "producer_member_sequence_sha256": member_sequence,
        "corrected_verification": {
            "filename": CORRECTED_VERIFICATION_NAME,
            "sha256": corrected_hash_a,
            "object_sha256": corrected_object,
        },
        "supersession_marker": {"filename": SUPERSESSION_NAME,
                                "sha256": marker_hash,
                                "object_sha256": marker["object_sha256"]},
        "old_verification": {"filename": OLD_VERIFICATION_NAME,
                             "sha256": OLD_VERIFICATION_SHA256,
                             "object_sha256": OLD_VERIFICATION_OBJECT_SHA256,
                             "consumable": False},
        "misnamed_self_bound_verification": {
            "filename": MISNAMED_SELF_BOUND_VERIFICATION_NAME,
            "sha256": MISNAMED_SELF_BOUND_VERIFICATION_SHA256,
            "object_sha256": MISNAMED_SELF_BOUND_VERIFICATION_OBJECT_SHA256,
            "consumable": False,
        },
        "earlier_incomplete_build_rejection_marker_sha256": REJECTED_BUILD_MARKER_SHA256,
        "dual_stage_byte_identical": True,
        "verifier_file_sha256": verifier_hash,
        "C74_producer_opened_read_decoded_compiled_imported_or_executed": False,
        "terminal_replay": {
            "source_after_receipt": True,
            "all_stage_members_after_receipt": True,
            "member_count_per_stage_including_rejected_verifications_marker_and_receipt": 13,
        },
        "strict_boundary": {"whole_large_component_closed": False,
                            "global_unresolved_decrement": 0,
                            "formal_credit": 0, "whole_component_credit": 0,
                            "D02_gate_credit": 0},
    }
    receipt["object_sha256"] = digest(receipt)
    receipt_payload = canonical(receipt) + b"\n"
    receipt_hash = hashlib.sha256(receipt_payload).hexdigest()
    for stage in (stage_a, stage_b):
        write_exclusive(stage / DUAL_RECEIPT_NAME, receipt_payload)

    # Outer receipt is last.  Freshly recapture source and every stage member;
    # compare the two complete byte sets without recording random stage paths.
    source_after, verifier_hash_after = secure_capture(SELF)
    need(source_after == source_before and verifier_hash_after == verifier_hash,
         "finalizer source terminal replay")
    complete_names = [NAMES[key] for key in sorted(NAMES)] + [
        OLD_VERIFICATION_NAME, MISNAMED_SELF_BOUND_VERIFICATION_NAME,
        CORRECTED_VERIFICATION_NAME,
        SUPERSESSION_NAME, DUAL_RECEIPT_NAME,
    ]
    complete_a: list[tuple[str, bytes]] = []
    complete_b: list[tuple[str, bytes]] = []
    for name in complete_names:
        payload_a, _ = secure_capture(stage_a / name, 96 << 20)
        payload_b, _ = secure_capture(stage_b / name, 96 << 20)
        complete_a.append((name, payload_a)); complete_b.append((name, payload_b))
    need(complete_a == complete_b and len(complete_a) == 13,
         "complete dual terminal replay")
    need(hashlib.sha256(complete_a[-1][1]).hexdigest() == receipt_hash,
         "outer receipt replay")
    return {"status": receipt["status"], "object_sha256": receipt["object_sha256"],
            "file_sha256": receipt_hash, "corrected_verification_sha256": corrected_hash_a,
            "supersession_marker_sha256": marker_hash}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--finalize-dual", action="store_true")
    parser.add_argument("--stage-a", type=Path)
    parser.add_argument("--stage-b", type=Path)
    args = parser.parse_args()
    if args.finalize_dual:
        need(args.stage_a is not None and args.stage_b is not None and
             args.candidate_dir is None and args.output is None, "finalize arguments")
        result = finalize_dual(args.stage_a.resolve(), args.stage_b.resolve())
    else:
        need(args.candidate_dir is not None and args.output is not None and
             args.stage_a is None and args.stage_b is None, "verify arguments")
        result = verify(args.candidate_dir.resolve(), args.output.resolve())
    print(json.dumps({"status": result["status"],
                      "object_sha256": result["object_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
