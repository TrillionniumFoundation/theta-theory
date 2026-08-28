#!/usr/bin/env python3
"""Independent fail-close verifier for the primitive 20-terminal gate.

This verifier intentionally has no dependency on the C27 producer, its family
table, or an edge ledger.  It streams the frozen C15/C25/C26 primitive inputs,
reconstructs their censuses and joins, derives the four physical chart labels
from the primitive atlas source, and then reconstructs the only admissible
zero-credit result.  A truthful REJECT is a verifier PASS; physical promotion
is impossible while six support-stratum totality proofs remain open.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import gc
import gzip
import hashlib
from itertools import zip_longest
import json
from pathlib import Path
import sys
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover_feature_obligation_ledger.jsonl.gz"
ATLAS = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
ATTACHMENT_RECEIPT = "cm2_c27_included_stratum_attachments_subgate_receipt.json"
OUTGOING_RECEIPT = "cm2_c27_outgoing_graphs_physical_totality_subgate_receipt.json"
RETAINED_RECEIPT = "cm2_c27_retained_continuation_subgate_receipt.json"
SINGLE_RECEIPT = "cm2_c27_single_graphs_subgate_receipt.json"
OWNER_SHADOW_RECEIPT = "cm2_c27_sheet_owner_shadow_physical_totality_subgate_receipt.json"
SAME_CHART_DIRECT_RECEIPT = "cm2_c27_same_chart_exact_equal_cross_component_final_receipt_v2.json"
BOUNDARY_BLOCKER_RECEIPT = "cm2_c27_boundary_volume_primitive_totality_unresolved_receipt.json"
SAME_CHART_CROSS_RECEIPT = AUDIT / "c27-same-chart-witness-cross-implementation-comparator-20260807T2319" / "cm2_c27_same_chart_witness_cross_implementation_zero_credit_receipt.json"
PROVISIONAL_OVERLAY_RECEIPT = AUDIT / "c27r1bc-provisional-overlay-v2-final-receipt.json"

FILE_PINS = {
    C15: "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    C25: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C26: "fc6d1a31e9e7c476bde73336c18d7ad4fb92deed71c3f7b7c58638c0ffc8e88e",
    ATLAS: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    ATTACHMENT_RECEIPT: "d66d8aacb517a642684f3ddbe184e270936346726b73fa518c76f29076c184f5",
    OUTGOING_RECEIPT: "39fc442c396038dfcfd9ca01a99c1188c87015b778bc8d15795a0336a8bbd5e9",
    RETAINED_RECEIPT: "08b760876914406e2fbe4e897609afd6ffc6f3667acaf6a1b4a7a9df58f6e263",
    SINGLE_RECEIPT: "40435bf43d9bab01b54f9bc0a8c283930228e84a33f95d2af14783a2eb1d6ad5",
    OWNER_SHADOW_RECEIPT: "2833cc5f1c9d35eeca36722dfb348ad16e9d09e8d44d8983e63b61f390a93d0f",
    SAME_CHART_DIRECT_RECEIPT: "bb58cfb7a8929e322c81b8be617a184f523da862cb4d3f4c260acd80a4ba9969",
    BOUNDARY_BLOCKER_RECEIPT: "772bdcc750a44400342005c14230e2ea26fdf01c2d92244611ba6f66817689b7",
}
SAME_CHART_CROSS_RECEIPT_FILE_SHA256 = "e4bdb0ca3f594602b61efa218ef3efe62ef048638ba618a443110c66c905eaf1"
PROVISIONAL_OVERLAY_RECEIPT_FILE_SHA256 = "cd05b9c1260bc037f38ff5edde22c635a1dc40fe5dff3d10a632b453361ac6de"

EXPECTED_C25_KERNELS = {
    "C19A": 5_596,
    "C19B": 12_232,
    "C19C": 33_344,
    "C19D": 4_432,
    "C20A": 126_468,
    "C22B": 295_336,
    "C23B": 9_404,
    "C24A": 15_224,
    "C24B": 168,
}
EXPECTED_C25_SEMANTICS = {
    "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY": 168,
    "EXACT_MEMBER_SUPPORT_EQUALITY": 182_072,
    "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY": 304_740,
    "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY": 15_224,
}

# obligation kind -> (node, role, dependencies, source kernel, exact count)
C26_RULES = {
    "A1_R204_TARGET_SHEET": ("A1", "INDEPENDENT_DEFINITION_ROOT", (), "C21A", 224),
    "A1_R211_OWNER_SHEET": ("A1", "INDEPENDENT_DEFINITION_ROOT", (), "C21C", 17_716),
    "A2_R204_SOURCE_TARGET_CURVE": ("A2", "DEPENDENT_FEATURE_CLOSURE", ("A1",), "C21A", 504),
    "A2_R204_SOURCE_TARGET_ENDPOINT": ("A2", "DEPENDENT_FEATURE_CLOSURE", ("A1",), "C21A", 280),
    "A2_R211_OWNER_CURVE": ("A2", "DEPENDENT_FEATURE_CLOSURE", ("A1",), "C21C", 20_456),
    "A2_R211_OWNER_ENDPOINT": ("A2", "DEPENDENT_FEATURE_CLOSURE", ("A1",), "C21C", 40_912),
    "G1_EXACT_GRAPH_DEFINITION": ("G1", "INDEPENDENT_DEFINITION_ROOT", (), "C10", 5_264),
    "G2A_GRAPH_TO_SHEET_IDENTIFICATION": ("G2A", "DEPENDENT_FEATURE_CLOSURE", ("G1",), "C24A", 5_264),
    "G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE": ("G2B", "DEPENDENT_FEATURE_CLOSURE", ("G1",), "C24B", 168),
    "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE": ("G2B", "DEPENDENT_FEATURE_CLOSURE", ("G1",), "C24A", 9_960),
    "R1_SOURCE_FREE_PREDICATE_CELL_DEFINITION": ("R1", "INDEPENDENT_DEFINITION_ROOT", (), "C22A", 295_340),
    "R2_MEMBER_FULL_SUPPORT_UNION": ("R2", "DEPENDENT_FEATURE_CLOSURE", ("R1",), "C22B", 295_336),
}
EXPECTED_C26_NODES = {
    "A1": 17_940,
    "A2": 62_152,
    "G1": 5_264,
    "G2A": 5_264,
    "G2B": 10_128,
    "R1": 295_340,
    "R2": 295_336,
}

SUPPORT_TERMINALS = (
    "SAME_CHART_RELATIVE_CELLS",
    "RETAINED_CONTINUATION",
    "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS",
    "DOUBLE_GRAPHS",
    "SHEET_OWNER",
    "SHEET_SHADOW",
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
    "INCLUDED_STRATUM_ATTACHMENTS",
)
CLOSED_ZERO_CREDIT = frozenset({
    "DOUBLE_GRAPHS",
    "REPRESENTATION_ALIASES",
    "REVERSE_RECHART",
    "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W",
    "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E",
    "Jx_NEGATIVE_CONTROL",
    "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL",
    "OUTGOING_GRAPHS",
    "RETAINED_CONTINUATION",
    "SINGLE_GRAPHS",
    "INCLUDED_STRATUM_ATTACHMENTS",
    "SHEET_OWNER",
    "SHEET_SHADOW",
})


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def canonical_object(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(payload != b"" and b"\n" not in payload, f"single JSON object:{path}")
    value = json.loads(payload)
    need(type(value) is dict and canonical(value) == payload, f"canonical JSON:{path}")
    return value


def closed_object(path: Path, field: str = "result_sha256") -> dict[str, Any]:
    value = canonical_object(path)
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), f"object closure:{path}")
    return value


def independently_checked_receipt(
    path: Path, expected_file_sha256: str, closure_field: str
) -> dict[str, Any]:
    raw = path.read_bytes()
    need(file_hash(path) == expected_file_sha256, f"independent receipt pin:{path}")
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(payload != b"" and b"\n" not in payload, f"independent single receipt object:{path}")
    value = json.loads(payload)
    need(type(value) is dict and canonical(value) == payload, f"independent canonical receipt:{path}")
    body = dict(value)
    claimed = body.pop(closure_field, None)
    need(type(claimed) is str and claimed == digest(body), f"independent receipt closure:{path}")
    return value


def checked_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for line_number, line in enumerate(stream, 1):
            need(line.endswith(b"\n"), f"{path.name}:{line_number}:newline")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"{path.name}:{line_number}:canonical")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body), f"{path.name}:{line_number}:row closure")
            yield row


def atlas_cycle() -> tuple[str, ...]:
    """Derive the physical cycle from independently checked normal formulas."""
    tree = ast.parse((ROOT / ATLAS).read_text(encoding="utf-8"), filename=ATLAS)
    geometry = next(
        (node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "geometry"),
        None,
    )
    need(geometry is not None, "primitive atlas geometry function")
    signatures: dict[str, str] = {}
    for node in ast.walk(geometry):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        test = node.test
        if (
            not isinstance(test.left, ast.Name)
            or test.left.id != "cell"
            or len(test.ops) != 1
            or not isinstance(test.ops[0], ast.Eq)
            or len(test.comparators) != 1
            or not isinstance(test.comparators[0], ast.Constant)
            or test.comparators[0].value not in {"E", "N", "W", "S"}
        ):
            continue
        cell = str(test.comparators[0].value)
        assignment = next(
            (
                item
                for item in node.body
                if isinstance(item, ast.Assign)
                and len(item.targets) == 1
                and isinstance(item.targets[0], ast.Tuple)
                and [ast.unparse(x) for x in item.targets[0].elts] == ["nx", "ny"]
            ),
            None,
        )
        need(assignment is not None, f"primitive normal assignment:{cell}")
        signatures[cell] = ast.unparse(assignment.value)
    need(signatures == {
        "E": "(radical_n, t)",
        "N": "(t, radical_n)",
        "W": "(-radical_n, t)",
        "S": "(t, -radical_n)",
    }, "primitive four-chart physical normal signatures")
    return ("E", "N", "W", "S")


def attachment_receipt() -> dict[str, Any]:
    raw = (ROOT / ATTACHMENT_RECEIPT).read_bytes()
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         "included-stratum canonical receipt")
    need(
        value.get("status")
        == "PASS_LOCAL_ZERO_CREDIT__INCLUDED_STRATUM_ATTACHMENTS_10660__276_EXCLUDED_AND_RESERVED_FOR_OPEN_RETAINED_CONTINUATION"
        and value.get("candidate_commitment", {}).get("candidate_count") == 10_660
        and value.get("candidate_commitment", {}).get("C20D_adjacent_positive_t_excluded_and_reserved_for_open_retained_continuation") == 276
        and value.get("candidate_commitment", {}).get("candidate_excluded_intersection_count") == 0
        and value.get("candidate_commitment", {}).get("candidate_plus_excluded_union_count") == 10_936
        and value.get("candidate_commitment", {}).get("candidate_representation_ids_sha256") == "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511"
        and value.get("candidate_commitment", {}).get("excluded_adjacent_representation_ids_sha256") == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
        and value.get("cross_implementation_exact_commitments_identical") is True
        and value.get("attack_harness", {}).get("attack_count") == 29
        and value.get("attack_harness", {}).get("all_rejected") is True
        and value.get("retained_continuation_terminal_closed") is False
        and value.get("terminal_credit_withheld_until_retained_continuation_joint_boundary") is True
        and value.get("formal_credit") == 0
        and value.get("C27_C28_C29") == "REJECT_PENDING_REMAINING_TERMINALS"
        and value.get("CM2") == "NO-GO_FOR_CLAIM",
        "included-stratum truthful zero-credit closure",
    )
    scripts = {
        "cm2_c27_included_stratum_attachments_stream_probe.py": value["stream_implementation"]["script_sha256"],
        "cm2_c27_included_stratum_attachments_sqlite_probe.py": value["sqlite_implementation"]["script_sha256"],
        "cm2_c27_included_stratum_attachments_attack_harness.py": value["attack_harness"]["script_sha256"],
    }
    for name, expected in scripts.items():
        need(file_hash(ROOT / name) == expected, f"included-stratum script pin:{name}")
    stream_paths = tuple(
        AUDIT / f"c27-included-stratum-c20d-split-v2b-stream-seed-{seed}" / "result.json"
        for seed in (101, 909)
    )
    sqlite_paths = tuple(
        AUDIT / f"c27-included-stratum-c20d-split-v2b-sqlite-seed-{seed}" / "result.json"
        for seed in (101, 909)
    )
    attack_path = AUDIT / "c27-included-stratum-c20d-split-v2b-attacks-101" / "result.json"
    need(stream_paths[0].read_bytes() == stream_paths[1].read_bytes(), "included-stratum stream double-seed")
    need(sqlite_paths[0].read_bytes() == sqlite_paths[1].read_bytes(), "included-stratum sqlite double-seed")
    stream_result = closed_object(stream_paths[0])
    sqlite_result = closed_object(sqlite_paths[0])
    attack_result = closed_object(attack_path)
    need(file_hash(stream_paths[0]) == value["stream_implementation"]["result_file_sha256"], "included stream runtime pin")
    need(file_hash(sqlite_paths[0]) == value["sqlite_implementation"]["result_file_sha256"], "included sqlite runtime pin")
    need(file_hash(attack_path) == value["attack_harness"]["result_file_sha256"], "included attack runtime pin")
    need(stream_result["result_sha256"] == value["stream_implementation"]["result_sha256"], "included stream object pin")
    need(sqlite_result["result_sha256"] == value["sqlite_implementation"]["result_sha256"], "included sqlite object pin")
    need(attack_result["result_sha256"] == value["attack_harness"]["result_sha256"], "included attack object pin")
    for result in (stream_result, sqlite_result):
        universe = result["candidate_universe"]
        need(
            universe["candidate_count"] == 10_660
            and universe["candidate_excluded_intersection_count"] == 0
            and universe["candidate_plus_excluded_union_count"] == 10_936
            and universe["candidate_representation_ids_sha256"]
            == "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511"
            and universe["excluded_adjacent_representation_ids_sha256"]
            == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
            and universe["candidate_plus_excluded_union_ids_sha256"]
            == "e2ffc75d183889b90eee29d15e0c0783976d8290ebde977c3081a82bf57c602f"
            and all(count == 0 for count in result["join_gap_census"].values()),
            "included-stratum runtime boundary",
        )
    need(
        attack_result["attack_count"] == attack_result["rejected_count"] == 29
        and attack_result["all_rejected"] is True,
        "included-stratum runtime attacks",
    )
    return {
        "terminal": "INCLUDED_STRATUM_ATTACHMENTS",
        "receipt_filename": ATTACHMENT_RECEIPT,
        "receipt_sha256": FILE_PINS[ATTACHMENT_RECEIPT],
        "candidate_count": 10_660,
        "candidate_representation_ids_sha256": "3c18dda4883dcc9a357d898ffa7c0f126b7a1ffde985bc77a879369b2978c511",
        "excluded_adjacent_count": 276,
        "excluded_adjacent_representation_ids_sha256": "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd",
        "candidate_plus_excluded_union_count": 10_936,
        "candidate_plus_excluded_union_ids_sha256": "e2ffc75d183889b90eee29d15e0c0783976d8290ebde977c3081a82bf57c602f",
        "terminal_credit_counted_after_joint_boundary": True,
        "paired_terminal": "RETAINED_CONTINUATION",
        "formal_credit": 0,
    }


def outgoing_receipt() -> dict[str, Any]:
    raw = (ROOT / OUTGOING_RECEIPT).read_bytes()
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         "outgoing-graphs canonical receipt")
    body = dict(value)
    claimed = body.pop("receipt_sha256", None)
    need(type(claimed) is str and claimed == digest(body),
         "outgoing-graphs receipt closure")
    need(
        value.get("status")
        == "PASS_OUTGOING_GRAPHS_DUAL_SEMANTICS_DOUBLE_SEED_31_ATTACKS__ZERO_CREDIT"
        and value.get("fresh_G1_partition") == {"DOUBLE": 16, "OUTGOING": 264, "SINGLE": 4_984}
        and value.get("outgoing_roots") == 264
        and value.get("G2A_sheet_dispositions") == 264
        and value.get("G2B_side_dispositions") == 528
        and value.get("unresolved") == 0
        and value.get("stream_double_seed_byte_identical") is True
        and value.get("sqlite_double_seed_byte_identical") is True
        and value.get("cross_implementation_per_candidate_digest_mismatch") == 0
        and value.get("coherent_attacks_rejected") == 31
        and value.get("C27_FAMILIES_imported_or_read") is False
        and value.get("edge_ledger_used_as_candidate_universe") is False
        and value.get("formal_credit") == 0
        and value.get("strict_nonpromotion") == {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "outgoing-graphs truthful zero-credit closure",
    )
    return {
        "terminal": "OUTGOING_GRAPHS",
        "receipt_filename": OUTGOING_RECEIPT,
        "receipt_sha256": FILE_PINS[OUTGOING_RECEIPT],
        "candidate_count": 264,
        "formal_credit": 0,
    }


def retained_receipt() -> dict[str, Any]:
    value = canonical_object(ROOT / RETAINED_RECEIPT)
    need(
        value.get("status")
        == "PASS_LOCAL_ZERO_CREDIT__RETAINED_CONTINUATION_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT"
        and value.get("terminal") == "RETAINED_CONTINUATION"
        and value.get("candidate_commitment", {}).get("candidate_count") == 276
        and value.get("candidate_commitment", {}).get("candidate_representation_ids_sha256")
        == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
        and value.get("candidate_commitment", {}).get("candidate_row_sequence_sha256")
        == "73c46567074bb302e7e16e61742445da1365a7d778cf31843ec95f6c5d5fa0aa"
        and value.get("primitive_identity_route", {}).get("C20D_relation_census")
        == {
            "ADJACENT_CONTINUATION_DISJOINT_INTERIOR_SHARED_FULL_FACE": 276,
            "STRICT_SUBCOVER_OF_OWNER_SUPPORT": 2_244,
        }
        and value.get("primitive_identity_route", {}).get("unresolved") == 0
        and value.get("cross_implementation_exact_commitments_identical") is True
        and value.get("attack_harness", {}).get("attack_count") == 38
        and value.get("attack_harness", {}).get("all_rejected") is True
        and value.get("formal_credit") == 0
        and value.get("C27_C28_C29") == "REJECT_PENDING_REMAINING_TERMINALS"
        and value.get("CM2") == "NO-GO_FOR_CLAIM",
        "retained-continuation truthful zero-credit closure",
    )
    scripts = {
        "cm2_c27_retained_continuation_stream_probe.py": value["script_pins"]["stream_probe"],
        "cm2_c27_retained_continuation_sqlite_verifier.py": value["script_pins"]["sqlite_verifier"],
        "cm2_c27_retained_continuation_attack_harness.py": value["script_pins"]["attack_harness"],
    }
    for name, expected in scripts.items():
        need(file_hash(ROOT / name) == expected, f"retained script pin:{name}")
    stream_paths = (
        AUDIT / "c27-retained-continuation-stream-v4-seed-30627401" / "result.json",
        AUDIT / "c27-retained-continuation-stream-v4-seed-30627941" / "result.json",
    )
    sqlite_paths = (
        AUDIT / "c27-retained-continuation-sqlite-v2-seed-30627402" / "result.json",
        AUDIT / "c27-retained-continuation-sqlite-v2-seed-30627942" / "result.json",
    )
    attack_path = AUDIT / "c27-retained-continuation-attacks-v2" / "result.json"
    need(stream_paths[0].read_bytes() == stream_paths[1].read_bytes(), "retained stream double-seed")
    need(sqlite_paths[0].read_bytes() == sqlite_paths[1].read_bytes(), "retained sqlite double-seed")
    for path in stream_paths + sqlite_paths:
        need((path.parent / "stderr.txt").read_bytes() == b"", f"retained empty stderr:{path.parent.name}")
    stream_result = closed_object(stream_paths[0])
    sqlite_result = closed_object(sqlite_paths[0])
    attack_result = closed_object(attack_path)
    need(file_hash(stream_paths[0]) == value["implementation_runs"]["stream"]["result_sha256"], "retained stream runtime pin")
    need(file_hash(sqlite_paths[0]) == value["implementation_runs"]["sqlite"]["result_sha256"], "retained sqlite runtime pin")
    need(file_hash(attack_path) == value["attack_harness"]["result_sha256"], "retained attack runtime pin")
    need(stream_result["result_sha256"] == value["implementation_runs"]["stream"]["result_object_sha256"], "retained stream object pin")
    need(sqlite_result["result_sha256"] == value["implementation_runs"]["sqlite"]["result_object_sha256"], "retained sqlite object pin")
    need(attack_result["result_sha256"] == value["attack_harness"]["result_object_sha256"], "retained attack object pin")
    for result in (stream_result, sqlite_result):
        universe = result["candidate_universe"]
        need(
            universe["candidate_count"] == 276
            and universe["candidate_representation_ids_sha256"]
            == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
            and universe["candidate_row_sequence_sha256"]
            == "73c46567074bb302e7e16e61742445da1365a7d778cf31843ec95f6c5d5fa0aa"
            and result["attachment_terminal_overlap_after_required_C20D_SOURCE_SPLIT"] == 0
            and all(count == 0 for count in result["join_gap_census"].values()),
            "retained runtime boundary",
        )
    need(
        attack_result["attack_count"] == attack_result["rejected_count"] == 38
        and attack_result["baseline_candidate_representation_ids_sha256"]
        == "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd",
        "retained runtime attacks",
    )
    return {
        "terminal": "RETAINED_CONTINUATION",
        "receipt_filename": RETAINED_RECEIPT,
        "receipt_sha256": FILE_PINS[RETAINED_RECEIPT],
        "candidate_count": 276,
        "candidate_representation_ids_sha256": "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd",
        "candidate_row_sequence_sha256": "73c46567074bb302e7e16e61742445da1365a7d778cf31843ec95f6c5d5fa0aa",
        "terminal_credit_counted_after_joint_boundary": True,
        "paired_terminal": "INCLUDED_STRATUM_ATTACHMENTS",
        "formal_credit": 0,
    }


def single_receipt() -> dict[str, Any]:
    value = canonical_object(ROOT / SINGLE_RECEIPT)
    allocation = {
        "C24A": {
            "DOUBLE_GRAPHS": {"G2A": 16, "G2B": 16},
            "OUTGOING_GRAPHS": {"G2A": 264, "G2B": 528},
            "SINGLE_GRAPHS": {"G2A": 4_984, "G2B": 9_416},
        },
        "C24B": {
            "DOUBLE_GRAPHS": {"G2B": 16},
            "OUTGOING_GRAPHS": {},
            "SINGLE_GRAPHS": {"G2B": 152},
        },
    }
    need(
        value.get("status") == "PASS_LOCAL_ZERO_CREDIT__SINGLE_GRAPHS_PHYSICAL_TOTALITY_AND_UNIQUE_ASSIGNMENT"
        and value.get("terminal") == "SINGLE_GRAPHS"
        and value.get("single_roots") == 4_984
        and value.get("single_graph_class_partition")
        == {"R235_SOURCE_EXACT_FACE_FULL_BASE": 552, "R235_TARGET_POSITIVE_PARTIAL_BASE": 4_432}
        and value.get("C24_full_terminal_allocation") == allocation
        and value.get("materialized_C15_C24_C25_C26_proof_rows") == 14_552
        and value.get("unresolved") == 0
        and value.get("stream_double_seed_byte_identical") is True
        and value.get("sqlite_double_seed_byte_identical") is True
        and value.get("cross_implementation_per_candidate_digest_mismatch") == 0
        and value.get("attack_harness")
        == {"all_rejected": True, "attack_count": 48, "result_sha256": "0beedda9f87830355755504533e718d2043e0500f0dd514399cc84e79a5bc9a7"}
        and value.get("formal_credit") == 0
        and value.get("C27_C28_C29") == "REJECT_PENDING_REMAINING_TERMINALS"
        and value.get("CM2") == "NO-GO_FOR_CLAIM",
        "single-graphs truthful zero-credit closure",
    )
    script_names = {
        "stream_probe": "cm2_c27_single_graphs_physical_totality_stream_probe.py",
        "sqlite_verifier": "cm2_c27_single_graphs_physical_totality_sqlite_verifier.py",
        "attack_harness": "cm2_c27_single_graphs_physical_totality_attack_harness.py",
        "final_receipt_builder": "cm2_c27_single_graphs_physical_totality_final_receipt_builder.py",
    }
    for key, name in script_names.items():
        need(file_hash(ROOT / name) == value["script_pins"][key], f"single script pin:{name}")
    final_path = ROOT.parent / value["runtime_receipt"]["path"]
    need(file_hash(final_path) == value["runtime_receipt"]["file_sha256"], "single final receipt file pin")
    final = closed_object(final_path, "receipt_sha256")
    need(final["receipt_sha256"] == value["runtime_receipt"]["internal_receipt_sha256"], "single final receipt object pin")
    need(
        final["status"] == "PASS_SINGLE_GRAPHS_DUAL_SEMANTICS_DOUBLE_SEED_48_ATTACKS__ZERO_CREDIT"
        and final["single_roots"] == 4_984
        and final["C24_full_terminal_allocation"] == allocation
        and final["G2A_sheet_dispositions"] == 4_984
        and final["G2B_positive_side_dispositions"] == 9_416
        and final["G2B_exact_empty_side_dispositions"] == 152
        and final["unresolved"] == 0
        and final["coherent_attacks_rejected"] == 48
        and final["formal_credit"] == 0,
        "single final runtime semantics",
    )
    paths = {
        "stream_seed_A": AUDIT / "c27-single-graphs-stream-seed-30628101",
        "stream_seed_B": AUDIT / "c27-single-graphs-stream-seed-30628901",
        "sqlite_seed_A": AUDIT / "c27-single-graphs-sqlite-verify-seed-30628201",
        "sqlite_seed_B": AUDIT / "c27-single-graphs-sqlite-verify-seed-30628902",
        "attacks": AUDIT / "c27-single-graphs-attacks-30628301",
    }
    for group, members in final["evidence"].items():
        for name, expected in members.items():
            need(file_hash(paths[group] / name) == expected, f"single runtime evidence:{group}/{name}")
    for name in ("ledger.jsonl.gz", "result.json", "manifest.json"):
        need((paths["stream_seed_A"] / name).read_bytes() == (paths["stream_seed_B"] / name).read_bytes(), f"single stream double-seed:{name}")
    need(
        (paths["sqlite_seed_A"] / "verification.json").read_bytes()
        == (paths["sqlite_seed_B"] / "verification.json").read_bytes(),
        "single sqlite double-seed",
    )
    stream_result = closed_object(paths["stream_seed_A"] / "result.json")
    sqlite_result = closed_object(paths["sqlite_seed_A"] / "verification.json", "verification_sha256")
    attack_result = closed_object(paths["attacks"] / "attack_result.json")
    need(
        stream_result["single_root_count"] == 4_984
        and stream_result["unresolved_count"] == 0
        and sqlite_result["candidate_count"] == 4_984
        and sqlite_result["per_candidate_digest_mismatch_count"] == 0
        and attack_result["attack_count"] == attack_result["rejected_count"] == 48
        and attack_result["unexpected_accept_count"] == 0,
        "single runtime evidence semantics",
    )
    return {
        "terminal": "SINGLE_GRAPHS",
        "receipt_filename": SINGLE_RECEIPT,
        "receipt_sha256": FILE_PINS[SINGLE_RECEIPT],
        "candidate_count": 4_984,
        "materialized_proof_row_count": 14_552,
        "terminal_credit_counted": True,
        "formal_credit": 0,
    }


def retained_attachment_joint_boundary(
    attachment: dict[str, Any], retained: dict[str, Any]
) -> dict[str, Any]:
    retained_digest = "2c7624bf0ef1666f2d2b22186422361a5021acdea8548dccb8c3e85dac1effcd"
    need(attachment["candidate_count"] == 10_660, "joint attachment count")
    need(retained["candidate_count"] == 276, "joint retained count")
    need(attachment["excluded_adjacent_count"] == retained["candidate_count"], "joint cardinality")
    need(attachment["excluded_adjacent_representation_ids_sha256"] == retained_digest, "joint excluded digest")
    need(retained["candidate_representation_ids_sha256"] == retained_digest, "joint retained digest")
    need(attachment["candidate_plus_excluded_union_count"] == 10_936 == 10_660 + 276, "joint union count")
    return {
        "terminals": ["INCLUDED_STRATUM_ATTACHMENTS", "RETAINED_CONTINUATION"],
        "status": "PASS_EXACT_DISJOINT_JOINT_BOUNDARY__10660_ATTACHMENTS_PLUS_276_RETAINED_EQUALS_10936",
        "attachment_candidate_count": 10_660,
        "retained_candidate_count": 276,
        "intersection_count": 0,
        "union_count": 10_936,
        "attachment_candidate_representation_ids_sha256": attachment["candidate_representation_ids_sha256"],
        "retained_candidate_representation_ids_sha256": retained_digest,
        "attachment_excluded_adjacent_representation_ids_sha256": retained_digest,
        "union_representation_ids_sha256": attachment["candidate_plus_excluded_union_ids_sha256"],
        "both_terminal_credits_counted": True,
        "formal_credit": 0,
    }


def independently_reconstruct_new_evidence() -> dict[str, Any]:
    owner = independently_checked_receipt(
        ROOT / OWNER_SHADOW_RECEIPT,
        "2833cc5f1c9d35eeca36722dfb348ad16e9d09e8d44d8983e63b61f390a93d0f",
        "receipt_sha256",
    )
    owner_ok = (
        owner.get("schema") == "cm2.c27.sheet-owner-shadow-physical-totality.zero-credit.v1.final-receipt.v1"
        and owner.get("receipt_sha256") == "1e8216806e7efcf3f19d7fbe7de61879f6cd8ca1e970cfb592f237370fa95c2c"
        and owner.get("terminal_census", {}).get("SHEET_OWNER") == 17_940
        and owner.get("terminal_census", {}).get("SHEET_SHADOW") == 17_940
        and owner.get("primitive_candidate_generation", {}).get("total") == 17_940
        and owner.get("role_rows") == 35_880
        and owner.get("materialized_shadow_companions") == 17_940
        and owner.get("unresolved") == 0
        and owner.get("legal_cross_component_witness") == 0
        and owner.get("cross_implementation_role_row_mismatch") == 0
        and owner.get("cross_implementation_shadow_row_mismatch") == 0
        and owner.get("stream_double_seed_ledger_byte_identical") is True
        and owner.get("sqlite_cross_seed_semantic_projection_identical") is True
        and owner.get("coherent_attacks_rejected") == 50
        and owner.get("formal_credit") == 0
    )
    need(owner_ok, "independent owner/shadow evidence reconstruction")

    direct = independently_checked_receipt(
        ROOT / SAME_CHART_DIRECT_RECEIPT,
        "bb58cfb7a8929e322c81b8be617a184f523da862cb4d3f4c260acd80a4ba9969",
        "receipt_sha256",
    )
    cross = independently_checked_receipt(
        SAME_CHART_CROSS_RECEIPT,
        SAME_CHART_CROSS_RECEIPT_FILE_SHA256,
        "receipt_sha256",
    )
    direct_census = direct.get("witness_census", {})
    cross_exact = cross.get("cross_implementation_exact_match", {})
    need(
        direct.get("legal_cross_component_witness_found") is True
        and direct_census.get("witness_group_count") == 228
        and direct_census.get("cross_component_member_pair_count") == 228
        and direct_census.get("witness_component_occurrence_count") == 456
        and direct.get("observed_witness_structure", {}).get("strict_positive_volume_groups") == 228
        and direct.get("endpoint_bits_needed_for_these_witnesses") is False
        and direct.get("double_seed_ledger_byte_identical") is True
        and direct.get("cross_seed_semantic_projection_identical") is True
        and direct.get("attack_count") == 27
        and direct.get("formal_credit") == 0,
        "independent direct-source same-chart evidence reconstruction",
    )
    need(
        cross.get("legal_cross_component_witness_found") is True
        and cross_exact.get("group_count") == 228
        and cross_exact.get("projection_count") == 456
        and cross_exact.get("unique_component_edge_count") == 192
        and cross_exact.get("affected_component_vertex_count") == 312
        and cross_exact.get("connected_component_count_on_affected_vertices") == 120
        and cross_exact.get("DSU_rank_reduction") == 192
        and cross_exact.get("group_ids_sha256") == direct.get("group_ids_sha256")
        and cross.get("attack_count") == 20
        and cross.get("formal_credit") == 0,
        "independent cross-implementation same-chart evidence reconstruction",
    )

    overlay = independently_checked_receipt(
        PROVISIONAL_OVERLAY_RECEIPT,
        PROVISIONAL_OVERLAY_RECEIPT_FILE_SHA256,
        "receipt_object_sha256",
    )
    overlay_census = overlay.get("census", {})
    overlay_qualification = overlay.get("qualification", {})
    need(
        overlay.get("authority_limit") == "WITNESS_ONLY_PROVISIONAL_OVERLAY__NOT_A_FORMAL_C27R1_C28R1_OR_C29R1_SEAL"
        and overlay_census.get("old_components") == 57_876
        and overlay_census.get("certain_component_edges") == 192
        and overlay_census.get("forced_rank_reduction") == 192
        and overlay_census.get("affected_vertices") == 312
        and overlay_census.get("affected_clusters") == 120
        and overlay_census.get("provisional_components") == 57_684
        and overlay_census.get("newly_internalized_pairs") == 691_416
        and overlay_census.get("provisional_cross_denominator") == 125_615_784_254
        and overlay_qualification.get("partition") == "PROVISIONAL_UPPER_BOUND_ONLY"
        and overlay_qualification.get("twenty_family_totality") == "OPEN"
        and overlay_qualification.get("C28") == "REJECT"
        and overlay_qualification.get("C29") == "REJECT"
        and overlay.get("formal_credit") == 0,
        "independent provisional-overlay authority reconstruction",
    )

    boundary = independently_checked_receipt(
        ROOT / BOUNDARY_BLOCKER_RECEIPT,
        "772bdcc750a44400342005c14230e2ea26fdf01c2d92244611ba6f66817689b7",
        "receipt_sha256",
    )
    boundary_missing = boundary.get("minimal_missing_authority", {})
    need(
        boundary.get("status") == "PASS_EXACT_BLOCKER_MATERIALIZATION__SIGNED_COMPLETE_POSITIVE_TERMINALS_REMAIN_OPEN__ZERO_CREDIT"
        and boundary.get("double_seed", {}).get("ledger_byte_identical") is True
        and boundary.get("double_seed", {}).get("result_byte_identical") is True
        and boundary.get("double_seed", {}).get("seeds") == [30628111, 30628991]
        and boundary.get("attack_harness", {}).get("attack_count") == 27
        and boundary.get("attack_harness", {}).get("all_rejected") is True
        and boundary_missing.get("C19C_half_open_atom_count") == 33_344
        and boundary_missing.get("endpoint_ownership_bit_count") == 200_064
        and boundary_missing.get("C26_direct_three_terminal_assignment_row_count") == 0
        and boundary_missing.get("three_terminal_unassigned_atom_count") == 483_232
        and set(boundary.get("terminal_credit_counted", {})) == {
            "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS"
        }
        and all(x is False for x in boundary.get("terminal_credit_counted", {}).values())
        and boundary.get("formal_credit") == 0,
        "independent boundary blocker reconstruction",
    )

    owner_summary = {
        "terminals": ["SHEET_OWNER", "SHEET_SHADOW"],
        "receipt_filename": OWNER_SHADOW_RECEIPT,
        "receipt_file_sha256": FILE_PINS[OWNER_SHADOW_RECEIPT],
        "receipt_object_sha256": owner["receipt_sha256"],
        "candidate_count_per_terminal": 17_940,
        "unresolved": 0,
        "legal_cross_component_witness": 0,
        "dual_semantics_double_seed": True,
        "coherent_attacks_rejected": 50,
        "formal_credit": 0,
    }
    same_summary = {
        "terminal": "SAME_CHART_RELATIVE_CELLS",
        "terminal_state": "OPEN_TOTALITY_WITH_CONFIRMED_LEGAL_WITNESSES",
        "source_direct_receipt_filename": SAME_CHART_DIRECT_RECEIPT,
        "source_direct_receipt_file_sha256": FILE_PINS[SAME_CHART_DIRECT_RECEIPT],
        "source_direct_receipt_object_sha256": direct["receipt_sha256"],
        "cross_implementation_receipt_path": str(SAME_CHART_CROSS_RECEIPT.relative_to(ROOT.parent)),
        "cross_implementation_receipt_file_sha256": SAME_CHART_CROSS_RECEIPT_FILE_SHA256,
        "cross_implementation_receipt_object_sha256": cross["receipt_sha256"],
        "witness_group_count": 228,
        "witness_projection_count": 456,
        "unique_component_edge_count": 192,
        "affected_component_vertex_count": 312,
        "forced_DSU_rank_reduction": 192,
        "legal_cross_component_witness_found": True,
        "same_chart_totality_proved": False,
        "required_governance_action": "REBUILD_C27_THROUGH_C29__PATCHING_OR_PRESERVING_C29_UNCONDITIONAL_AUTHORITY_IS_FORBIDDEN",
        "formal_credit": 0,
    }
    overlay_summary = {
        "receipt_path": str(PROVISIONAL_OVERLAY_RECEIPT.relative_to(ROOT.parent)),
        "receipt_file_sha256": PROVISIONAL_OVERLAY_RECEIPT_FILE_SHA256,
        "receipt_object_sha256": overlay["receipt_object_sha256"],
        "authority": "PROVISIONAL_UPPER_BOUND_ONLY__NOT_MAXIMALITY__NOT_FORMAL_C27R1_C28R1_C29R1",
        "old_component_count": 57_876,
        "provisional_component_count": 57_684,
        "forced_rank_reduction": 192,
        "newly_internalized_pairs": 691_416,
        "formal_credit": 0,
    }
    blocker_summary = {
        "terminals": ["SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES", "POSITIVE_VOLUME_CARRIERS"],
        "terminal_state": "OPEN_EXACT_BLOCKERS_MATERIALIZED",
        "receipt_filename": BOUNDARY_BLOCKER_RECEIPT,
        "receipt_file_sha256": FILE_PINS[BOUNDARY_BLOCKER_RECEIPT],
        "receipt_object_sha256": boundary["receipt_sha256"],
        "C19C_half_open_atom_count": 33_344,
        "missing_endpoint_ownership_bit_count": 200_064,
        "C26_direct_three_terminal_assignment_row_count": 0,
        "three_terminal_unassigned_atom_count": 483_232,
        "double_seed_byte_identical": True,
        "coherent_attacks_rejected": 27,
        "formal_credit": 0,
    }
    return {
        "owner_summary": owner_summary,
        "same_summary": same_summary,
        "overlay_summary": overlay_summary,
        "blocker_summary": blocker_summary,
    }


def collect_source_evidence() -> dict[str, Any]:
    for name, expected in FILE_PINS.items():
        need(file_hash(ROOT / name) == expected, f"frozen input pin:{name}")

    cycle = atlas_cycle()
    included_stratum_receipt = attachment_receipt()
    outgoing_graphs_receipt = outgoing_receipt()
    retained_continuation_receipt = retained_receipt()
    single_graphs_receipt = single_receipt()
    newly_reconstructed = independently_reconstruct_new_evidence()
    joint_boundary = retained_attachment_joint_boundary(
        included_stratum_receipt, retained_continuation_receipt
    )
    c25_kernels: Counter[str] = Counter()
    c25_semantics: Counter[str] = Counter()
    c15_sequence = hashlib.sha256()
    c25_sequence = hashlib.sha256()
    seen_members: set[str] = set()
    sentinel = object()
    c15_stream = checked_rows(ROOT / C15)
    c25_stream = checked_rows(ROOT / C25)
    count = 0
    for ordinal, pair in enumerate(zip_longest(c15_stream, c25_stream, fillvalue=sentinel)):
        c15_row, c25_row = pair
        need(c15_row is not sentinel and c25_row is not sentinel, "C15/C25 exact universe anti-join")
        need(c15_row["schema"] == "cm2.round306c15.source-g-502204-member-fresh-dsu-freeze.v1.member-component-row.v1", "C15 schema")
        need(c25_row["schema"] == "cm2.round306c25.source-g-typed-global-support-ledger.v1.member-row.v1", "C25 schema")
        need(c15_row["member_ordinal"] == ordinal == c25_row["member_ordinal"], "C15/C25 ordinal join")
        member_id = c15_row["registry_member_id"]
        need(type(member_id) is str and member_id not in seen_members, "C15 unique member identity")
        seen_members.add(member_id)
        need(c25_row["member_id"] == member_id, "C15/C25 member identity join")
        need(c25_row["source_bindings"]["C15_member_row_sha256"] == c15_row["row_sha256"], "C15/C25 row-hash join")
        for field in ("fresh_component_id", "base_root_id", "official_key_id"):
            need(c25_row[field] == c15_row[field], f"C15/C25 {field} join")
        need(c25_row["strict_nonpromotion"] == {"B1A": 0, "B2": 0, "CM2": 0, "maximality": 0}, "C25 strict nonpromotion")
        c25_kernels[c25_row["source_bindings"]["support_kernel"]] += 1
        c25_semantics[c25_row["support_semantic_kind"]] += 1
        c15_sequence.update(bytes.fromhex(c15_row["row_sha256"]))
        c25_sequence.update(bytes.fromhex(c25_row["row_sha256"]))
        count += 1
    need(count == 502_204 and len(seen_members) == count, "C15/C25 502204-member universe")
    need(dict(c25_kernels) == EXPECTED_C25_KERNELS, "C25 support-kernel census")
    need(dict(c25_semantics) == EXPECTED_C25_SEMANTICS, "C25 support-semantic census")
    del seen_members
    gc.collect()

    c26_kinds: Counter[str] = Counter()
    c26_nodes: Counter[str] = Counter()
    c26_sequence = hashlib.sha256()
    seen_features: set[str] = set()
    c26_count = 0
    for ordinal, row in enumerate(checked_rows(ROOT / C26)):
        need(row["schema"] == "cm2.round306c26.source-g-corrected-b1a.v1.feature-obligation-row.v1", "C26 schema")
        need(row["feature_ordinal"] == ordinal, "C26 total order")
        feature_id = row["feature_id"]
        need(type(feature_id) is str and feature_id not in seen_features, "C26 unique feature identity")
        seen_features.add(feature_id)
        kind = row["obligation_kind"]
        need(kind in C26_RULES, "C26 primitive obligation grammar")
        node, role, dependencies, source_kernel, _ = C26_RULES[kind]
        need(row["node_id"] == node, "C26 node/kind assignment")
        need(row["obligation_role"] == role, "C26 role/kind assignment")
        need(tuple(row["depends_on_node_ids"]) == dependencies, "C26 dependency/kind assignment")
        need(row["source_bindings"]["source_kernel"] == source_kernel, "C26 source-kernel/kind assignment")
        expected_credit = {
            "B1A_feature_obligation": 1,
            "dependent_feature_closure": int(role == "DEPENDENT_FEATURE_CLOSURE"),
            "source_free_definition_root": int(role == "INDEPENDENT_DEFINITION_ROOT"),
        }
        need(row["formal_credit"] == expected_credit, "C26 role credit")
        need(row["strict_nonpromotion"] == {
            "B2": 0,
            "CM2": 0,
            "DSU_edge": 0,
            "maximality": 0,
            "member_identity": 0,
            "pair_routing": 0,
            "transition_theorem": 0,
        }, "C26 strict nonpromotion")
        c26_kinds[kind] += 1
        c26_nodes[node] += 1
        c26_sequence.update(bytes.fromhex(row["row_sha256"]))
        c26_count += 1
    expected_kinds = {kind: rule[4] for kind, rule in C26_RULES.items()}
    need(c26_count == 691_424 and len(seen_features) == c26_count, "C26 691424-feature universe")
    need(dict(c26_kinds) == expected_kinds, "C26 obligation-kind census")
    need(dict(c26_nodes) == EXPECTED_C26_NODES, "C26 node census")
    del seen_features
    gc.collect()

    primitive_universes = {
        "C15_member_count": count,
        "C25_support_kernel_census": dict(sorted(c25_kernels.items())),
        "C25_support_semantic_census": dict(sorted(c25_semantics.items())),
        "C26_feature_count": c26_count,
        "C26_node_census": dict(sorted(c26_nodes.items())),
        "C26_obligation_kind_census": dict(sorted(c26_kinds.items())),
    }
    return {
        "cycle": cycle,
        "primitive_universes": primitive_universes,
        "closed_subgate_receipts": [
            retained_continuation_receipt,
            outgoing_graphs_receipt,
            single_graphs_receipt,
            included_stratum_receipt,
            newly_reconstructed["owner_summary"],
        ],
        "same_chart_legal_witness_evidence": newly_reconstructed["same_summary"],
        "boundary_volume_unresolved_evidence": newly_reconstructed["blocker_summary"],
        "C27R1BC_provisional_overlay": newly_reconstructed["overlay_summary"],
        "joint_boundary_bindings": [joint_boundary],
        "withheld_joint_boundary_receipts": [],
        "source_row_sequence_sha256": {
            "C15": c15_sequence.hexdigest(),
            "C25": c25_sequence.hexdigest(),
            "C26": c26_sequence.hexdigest(),
        },
    }


def expected_terminals(cycle: tuple[str, ...]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {"branch": "SUPPORT_STRATUM", "terminal": terminal}
        for terminal in SUPPORT_TERMINALS
    ]
    rows.append({"branch": "ATLAS_MAP", "terminal": "REVERSE_RECHART"})
    for index, chart in enumerate(cycle):
        rows.append({
            "branch": "ATLAS_MAP",
            "terminal": f"TRUE_CYCLIC_SEAM_{chart}_TO_{cycle[(index + 1) % len(cycle)]}",
        })
    for terminal in ("Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL", "JxJy_NEGATIVE_CONTROL"):
        rows.append({"branch": "PHYSICAL_ACTION_NEGATIVE_CONTROL", "terminal": terminal})
    rows.append({"branch": "REPRESENTATION_MAP", "terminal": "REPRESENTATION_ALIASES"})
    need(len(rows) == 20 and len({row["terminal"] for row in rows}) == 20, "independent 20-terminal grammar")
    output = []
    for ordinal, row in enumerate(rows):
        body = {**row, "ordinal": ordinal}
        output.append({**body, "row_sha256": digest(body)})
    return output


def expected_candidate(evidence: dict[str, Any]) -> dict[str, Any]:
    cycle = evidence["cycle"]
    terminals = expected_terminals(cycle)
    obligations = []
    for terminal in terminals:
        name = terminal["terminal"]
        obligations.append({
            "terminal": name,
            "state": (
                "LOCAL_SUBGATE_CLOSED_ZERO_CREDIT"
                if name in CLOSED_ZERO_CREDIT
                else "INDEPENDENT_TOTALITY_PROOF_REQUIRED"
            ),
            "must_prove_candidate_generation_from_primitive_geometry": True,
            "must_prove_unique_terminal_assignment": True,
            "must_reject_or_route_every_cross_component_witness": True,
        })
    result = {
        "status": "REJECT_ZERO_CREDIT__16_OF_20_TERMINALS_EVIDENCE_CLOSED__228_LEGAL_SAME_CHART_WITNESS_GROUPS_FORCE_C27_C28_C29_REBUILD__4_TOTALITY_PROOFS_REMAIN",
        "C27_source_or_FAMILIES_imported_or_read": False,
        "edge_ledger_used_as_candidate_universe": False,
        "primitive_chart_cycle": list(cycle),
        "grammar": {
            "support_stratum_terminal_count": 11,
            "atlas_or_action_or_representation_terminal_count": 9,
            "terminal_count": 20,
            "terminals": terminals,
            "syntactic_coverage": "PASS",
            "syntactic_mutual_exclusivity": "PASS",
            "physical_totality": "REJECT__LEGAL_CROSS_COMPONENT_WITNESSES_FOUND__4_TERMINALS_OPEN",
        },
        "primitive_universes": evidence["primitive_universes"],
        "terminal_obligations": obligations,
        "closed_subgate_receipts": evidence["closed_subgate_receipts"],
        "same_chart_legal_witness_evidence": evidence["same_chart_legal_witness_evidence"],
        "boundary_volume_unresolved_evidence": evidence["boundary_volume_unresolved_evidence"],
        "C27R1BC_provisional_overlay": evidence["C27R1BC_provisional_overlay"],
        "joint_boundary_bindings": evidence["joint_boundary_bindings"],
        "withheld_joint_boundary_receipts": evidence["withheld_joint_boundary_receipts"],
        "closed_zero_credit_terminal_count": 16,
        "remaining_terminal_totality_proof_count": 4,
        "remaining_terminal_totality_proofs": [
            "SAME_CHART_RELATIVE_CELLS",
            "SIGNED_BOUNDARY_FACES",
            "COMPLETE_BOUNDARY_FACES",
            "POSITIVE_VOLUME_CARRIERS",
        ],
        "legal_cross_component_witness_found": True,
        "legal_same_chart_witness_group_count": 228,
        "unique_witness_component_edge_count": 192,
        "prior_C27_C28_C29_authority": "INVALIDATED__REBUILD_REQUIRED",
        "C29_patch_or_preservation_permitted": False,
        "provisional_overlay_is_maximality_authority": False,
        "rebuild_required": True,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    return {**result, "result_sha256": digest(result)}


def parse_candidate_bytes(raw: bytes) -> dict[str, Any]:
    if raw.endswith(b"\n"):
        raw = raw[:-1]
    need(raw != b"" and b"\n" not in raw, "single canonical candidate object")
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) == raw, "candidate canonical JSON")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "candidate result closure")
    return value


def verify_candidate_dict(candidate: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    expected = expected_candidate(evidence)
    need(candidate == expected, "candidate differs from independent primitive reconstruction")
    return {
        "status": "PASS_INDEPENDENT_PRIMITIVE_20_TERMINAL_RECONSTRUCTION__TRUTHFUL_REJECT_WITH_228_WITNESS_GROUPS_AND_4_TOTALITY_PROOFS_REMAINING__REBUILD_REQUIRED__ZERO_CREDIT",
        "candidate_result_sha256": candidate["result_sha256"],
        "closed_zero_credit_terminal_count": 16,
        "remaining_terminal_totality_proof_count": 4,
        "physical_totality": "REJECT__LEGAL_CROSS_COMPONENT_WITNESSES_FOUND__4_TERMINALS_OPEN",
        "legal_same_chart_witness_group_count": 228,
        "unique_witness_component_edge_count": 192,
        "prior_C27_C28_C29_authority": "INVALIDATED__REBUILD_REQUIRED",
        "provisional_overlay_authority": "PROVISIONAL_UPPER_BOUND_ONLY",
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
        "source_file_pins": dict(sorted(FILE_PINS.items())),
        "source_row_sequence_sha256": evidence["source_row_sequence_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-json", required=True, help="canonical producer stdout saved as a file, or - for stdin")
    args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")
    raw = sys.stdin.buffer.read() if args.candidate_json == "-" else Path(args.candidate_json).read_bytes()
    candidate = parse_candidate_bytes(raw)
    evidence = collect_source_evidence()
    print(canonical(verify_candidate_dict(candidate, evidence)).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print(canonical({
            "status": "REJECT_INDEPENDENT_PRIMITIVE_20_TERMINAL_VERIFICATION",
            "reason": str(exc),
            "formal_credit": 0,
            "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
            "CM2": "NO-GO_FOR_CLAIM",
        }).decode("ascii"))
        raise SystemExit(2)
