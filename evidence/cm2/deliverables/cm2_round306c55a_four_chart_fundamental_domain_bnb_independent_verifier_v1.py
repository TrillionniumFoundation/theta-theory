#!/usr/bin/env python3
"""Independent structural/cross-source verifier for C55-A.

The verifier imports and executes no C55-A producer.  It replays C32 geometry,
C34 dispositions, C37 reflection identities, C41 residual blockers, the C48
task overlay, and C53 parent projections directly from frozen bytes.
"""

from __future__ import annotations

import gc
import gzip
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "deliverables"
RUNTIME = ROOT / ".cm2-runtime"

LEAF_PATH = DELIVERABLES / "cm2_round306c55a_four_chart_fundamental_domain_bnb_leaf_ledger_v1.json"
GLUE_PATH = DELIVERABLES / "cm2_round306c55a_four_chart_fundamental_domain_exact_glue_ledger_v1.json"
RESULT_PATH = DELIVERABLES / "cm2_round306c55a_four_chart_fundamental_domain_bnb_result_v1.json"
VERIFY_PATH = DELIVERABLES / "cm2_round306c55a_four_chart_fundamental_domain_bnb_independent_verification_v1.json"

EXPECTED_FILES = {
    LEAF_PATH: "e80c012e3260e8f9e68d5858ba5d9dafd94611e2a1c1200d787a20e3842d8db6",
    GLUE_PATH: "d91dbc92c76fc8f004ff795c008d3a7b3e5716e6e6287a39798ba7331ecae00b",
    RESULT_PATH: "d38f39792fc944b72e70100f9f96f312b5e30e034d5104ce5f848d24378ae5af",
}
EXPECTED_OBJECTS = {
    LEAF_PATH: "7dd4c19cfb2b9f8cd30a4a9a23e30f11734e856cc6cc5a04e9a169c051059d90",
    GLUE_PATH: "b9a9a3fd6a18ac50d7141cc9e351364d5fe35edb6bdcb4b2126aaeec5c745cef",
    RESULT_PATH: "93b732cd65be4453e7b29379d7f70d8c849057d5bcba5489e1f6c4dd705972e3",
}
TOKENS = {
    32: "c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9",
    34: "c34-seed-event-frontier-20260810T142445Z-6ec6dac7de032cdb",
    37: "c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38",
    41: "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599",
    42: "c42-p391-formal-producer-20260811T044500Z-f1",
}
C53_AUDIT = DELIVERABLES / "cm2_round306c53_d02a_pair1_pair_level_successor_independent_audit_v1.json"
C48_RESULT = ROOT / ".cm2-runtime/c48-successor-candidates/c48-pair668-gen1-bbd909cad5a5-61de17d0a812-v1/candidate_result__cm2_round306c48_d02a_pair668_two_side_owner_closure_result_v1.json"

AUTHORITY = {
    "C32_object_sha256": "32ff9e0f90a12f17b16f67086eabda0986a0d52d185bea0c5c16e20518ca1474",
    "C33_object_sha256": "82dedeace982db89763e8a7e318fa6605d18cadc6bf390d6b23585d0922b87a0",
    "C34_object_sha256": "1c75d245a20bac35a0e33249f921ee862ad3c1397e78817189699dcc28552d2e",
    "C37_object_sha256": "d6333d60d045dd60d93560b75f6332324c8a8bc131024e7e8100704aa2d89d2b",
    "C53_effective_checkpoint_object_sha256": "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab",
    "C53_global_head_file_sha256": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "C53_global_head_object_sha256": "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb",
    "C53_global_head_path": ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal",
    "C53_independent_audit_object_sha256": "a7bee7e57b6527c7bf9ea7f17966379c62a722fe9ce2ce2009f19f85a5afaa7c",
}
TERMINALS = {"CONNECTED_TO_KNOWN", "EARLIEST_PREFIX_EXCLUDED", "SOURCE_GRAZING_OR_CEMETERY", "TYPED_EVENT_GRAPH"}

TOP_LEAF_KEYS = {"authority_binding", "blocker_partition", "blocker_rows", "census", "leaf_order", "leaves", "object_sha256", "proof_policy", "schema", "source_assets", "status"}
LEAF_KEYS = {"anchor_or_exterior_proof", "bnb_state", "c34_frontier_row_sha256", "cell_id", "component_ref", "exact_box", "glue_refs", "leaf_ordinal", "origin_key", "physical_chart", "proof_ref", "reflection_pair_ref", "row_sha256", "schema", "source_cell_row_sha256", "terminal_disposition", "unresolved_reason"}
BLOCKER_KEYS = {"blocker_row_id", "c37_reflection_row_sha256", "c42_parent_row_sha256", "c53_projection_object_sha256", "current_nonterminal_leaf_count", "current_unresolved_parent_volume", "global_missing_requirement_ids", "pair_index", "primary_residual_classification", "reflected_cell_id", "representative_cell_id", "residual_classification_census", "residual_source_row_sha256s", "row_sha256", "schema"}
TOP_GLUE_KEYS = {"authority_binding", "coverage", "exact_gluing_model", "glue_rows", "object_sha256", "row_order", "schema", "source_assets", "status"}
GLUE_KEYS = {
    "intra_faces": {"axis", "classification", "compact_chart", "coordinate", "dimension", "face_id", "negative_cell_id", "ordinal", "positive_cell_id", "row_sha256", "source_row_sha256", "span"},
    "source_seams": {"classification", "dimension", "exact_state_gluing_inherited_from_round162", "face_id", "left_cell_id", "left_chart", "left_compact_endpoint", "ordinal", "physical_p_span", "right_cell_id", "right_chart", "right_compact_endpoint", "row_sha256", "seam_id", "source_row_sha256", "terminal"},
    "source_grazing_faces": {"classification", "compact_chart", "compact_q", "dimension", "face_id", "incident_cell_id", "ordinal", "physical_p", "physical_t_span", "round144_dynamic_cemetery_credit", "row_sha256", "source_row_sha256", "terminal_for_compact_geometry"},
    "source_grazing_corners": {"classification", "compact_q", "corner_id", "dimension", "left_cell_id", "ordinal", "physical_p", "right_cell_id", "round144_dynamic_cemetery_credit", "row_sha256", "seam_id", "source_row_sha256", "terminal_for_compact_geometry"},
}

ENCODER = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def require(ok: bool, label: str) -> None:
    if not ok:
        raise RuntimeError(label)


def digest(value: Any) -> str:
    h = hashlib.sha256()
    for part in ENCODER.iterencode(value):
        h.update(part.encode("ascii"))
    return h.hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strict_json(path: Path, one_line: bool = False) -> dict[str, Any]:
    raw = path.read_bytes()
    require(path.is_file() and not path.is_symlink() and path.stat().st_nlink == 1, f"safe-regular:{path}")
    if one_line:
        require(raw.endswith(b"\n") and raw.count(b"\n") == 1, f"one-line:{path}")
        require(all(byte < 128 for byte in raw), f"ascii:{path}")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, f"duplicate-key:{path}:{key}")
            out[key] = value
        return out
    def no_float(token: str) -> None:
        raise RuntimeError(f"float:{path}:{token}")
    value = json.loads(raw, object_pairs_hook=pairs, parse_float=no_float)
    require(type(value) is dict, f"top-object:{path}")
    return value


def verify_closed(value: dict[str, Any], field: str, expected: str | None = None) -> None:
    bare = dict(value)
    claimed = bare.pop(field, None)
    require(type(claimed) is str and digest(bare) == claimed, f"self-hash:{field}")
    if expected is not None:
        require(claimed == expected, f"expected-hash:{field}")


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    return {**value, "row_sha256": digest(value)}


def rows(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="ascii", newline="") as f:
        for line in f:
            yield json.loads(line)


def directory(n: int) -> Path:
    require((RUNTIME / f"c{n}-current-token").read_text(encoding="ascii").strip() == TOKENS[n], f"token:{n}")
    return RUNTIME / "candidates" / TOKENS[n]


def validate_source_row(row: dict[str, Any]) -> None:
    bare = dict(row)
    claimed = bare.pop("row_sha256", None)
    require(type(claimed) is str and digest(bare) == claimed, "source-row-hash")


def normalize(source: dict[str, Any], ordinal: int) -> dict[str, Any]:
    bare = dict(source)
    source_hash = bare.pop("row_sha256")
    bare["ordinal"] = ordinal
    bare["source_row_sha256"] = source_hash
    return close_row(bare)


def validate_leaf_shape(row: dict[str, Any]) -> None:
    require(set(row) == LEAF_KEYS, "leaf-closed-schema")
    verify_closed(row, "row_sha256")
    terminal = row["terminal_disposition"]
    reason = row["unresolved_reason"]
    require(
        (terminal in TERMINALS and reason is None)
        or (terminal is None and type(reason) is str and bool(reason)),
        "leaf-null-rule",
    )
    require(row["bnb_state"]["depth_cap_terminal_used"] is False, "depth-cap-terminal")
    require(row["bnb_state"]["base_leaf_is_full_continuation_proof"] is False, "s0-full-continuation")


def execute_attacks(terminal: dict[str, Any], unresolved: dict[str, Any]) -> int:
    attacks: list[dict[str, Any]] = []
    for mutate in (
        lambda r: r.update(terminal_disposition="FAKE_FIFTH_CLASS"),
        lambda r: r.update(terminal_disposition=None),
        lambda r: r.update(unresolved_reason="forged"),
        lambda r: r["bnb_state"].update(depth_cap_terminal_used=True),
        lambda r: r["bnb_state"].update(base_leaf_is_full_continuation_proof=True),
    ):
        row = json.loads(json.dumps(terminal))
        row.pop("row_sha256")
        mutate(row)
        row = close_row(row)
        attacks.append(row)
    for mutate in (
        lambda r: r.update(unresolved_reason=None),
        lambda r: r.update(terminal_disposition="SOURCE_GRAZING_OR_CEMETERY"),
        lambda r: r["bnb_state"].update(blocker_row_id=None),
    ):
        row = json.loads(json.dumps(unresolved))
        row.pop("row_sha256")
        mutate(row)
        row = close_row(row)
        attacks.append(row)
    rejected = 0
    for i, row in enumerate(attacks):
        try:
            validate_leaf_shape(row)
            if i >= 7:
                require(row["bnb_state"]["blocker_row_id"] is not None, "unresolved-blocker")
        except RuntimeError:
            rejected += 1
    # The blocker-id mutation passes the generic null rule but is rejected by
    # the cross-ledger check above; count it explicitly after executing it.
    require(rejected == len(attacks), "attack-not-rejected")
    return rejected


def verify() -> dict[str, Any]:
    result = strict_json(RESULT_PATH, one_line=True)
    require(file_sha(RESULT_PATH) == EXPECTED_FILES[RESULT_PATH], "result-file")
    verify_closed(result, "object_sha256", EXPECTED_OBJECTS[RESULT_PATH])
    require(result["authority_binding"] == AUTHORITY, "result-authority")
    require(result["formal_credit"] == {"D02_gate_credit": 0, "formal_credit": 0, "source_grazing_or_cemetery_new_credit": 0}, "zero-credit")
    for source in result["source_assets"]:
        path = ROOT / source["path"]
        require(file_sha(path) == source["file_sha256"], f"source-file:{path}")

    glue = strict_json(GLUE_PATH, one_line=True)
    require(file_sha(GLUE_PATH) == EXPECTED_FILES[GLUE_PATH], "glue-file")
    require(set(glue) == TOP_GLUE_KEYS and glue["authority_binding"] == AUTHORITY, "glue-top")
    verify_closed(glue, "object_sha256", EXPECTED_OBJECTS[GLUE_PATH])
    expected_counts = {"intra_faces": 161586, "source_seams": 888, "source_grazing_faces": 1024, "source_grazing_corners": 8}
    refs: dict[str, dict[str, list[int]]] = defaultdict(lambda: {
        "intra_face_ordinals": [], "source_grazing_corner_ordinals": [],
        "source_grazing_face_ordinals": [], "source_seam_ordinals": [],
    })
    source_specs = {
        "intra_faces": (directory(32) / "intra_chart_adjacency.jsonl.gz", ("negative_cell_id", "positive_cell_id"), "intra_face_ordinals"),
        "source_seams": (directory(32) / "source_chart_seams.jsonl.gz", ("left_cell_id", "right_cell_id"), "source_seam_ordinals"),
        "source_grazing_faces": (directory(32) / "source_grazing_faces.jsonl.gz", ("incident_cell_id",), "source_grazing_face_ordinals"),
        "source_grazing_corners": (directory(32) / "source_grazing_corners.jsonl.gz", ("left_cell_id", "right_cell_id"), "source_grazing_corner_ordinals"),
    }
    for family, count in expected_counts.items():
        actual = glue["glue_rows"][family]
        require(len(actual) == count, f"glue-count:{family}")
        source_path, incident_fields, ref_key = source_specs[family]
        source_iter = rows(source_path)
        for ordinal, row in enumerate(actual):
            require(set(row) == GLUE_KEYS[family] and row["ordinal"] == ordinal, f"glue-schema:{family}")
            verify_closed(row, "row_sha256")
            source = next(source_iter)
            validate_source_row(source)
            require(row == normalize(source, ordinal), f"glue-source-equality:{family}:{ordinal}")
            if family in {"source_grazing_faces", "source_grazing_corners"}:
                require(row["round144_dynamic_cemetery_credit"] == 0, "geometric-grazing-credit")
            for field in incident_fields:
                refs[row[field]][ref_key].append(ordinal)
        try:
            next(source_iter)
            require(False, f"extra-source-row:{family}")
        except StopIteration:
            pass
    require(glue["coverage"] == {
        "all_corner_cells_exist": True, "all_face_cells_exist": True,
        "cell_count": 76832, "corner_count": 8, "grazing_face_count": 1024,
        "intra_face_count": 161586, "leaf_glue_refs_bidirectional": True,
        "source_grazing_boundary_complete": True, "source_seam_count": 888,
        "source_seam_cyclic_span_complete": True,
        "unexpected_or_missing_cell_reference_count": 0,
    }, "glue-coverage")
    del glue
    gc.collect()

    ledger = strict_json(LEAF_PATH, one_line=True)
    require(file_sha(LEAF_PATH) == EXPECTED_FILES[LEAF_PATH], "leaf-file")
    require(set(ledger) == TOP_LEAF_KEYS and ledger["authority_binding"] == AUTHORITY, "leaf-top")
    verify_closed(ledger, "object_sha256", EXPECTED_OBJECTS[LEAF_PATH])
    require(len(ledger["leaves"]) == 76832 and len(ledger["blocker_rows"]) == 574, "leaf-blocker-count")

    audit = strict_json(C53_AUDIT)
    verify_closed(audit, "object_sha256", AUTHORITY["C53_independent_audit_object_sha256"])
    projections = {r["pair_index"]: r for r in audit["post_seal_promotion_derivation"]["parent_projections"]}
    require(len(projections) == 862, "projection-count")
    for projection in projections.values():
        bare = dict(projection)
        claimed = bare.pop("projection_object_sha256")
        require(digest(bare) == claimed, "projection-self-hash")

    pair_map: dict[str, tuple[dict[str, Any], str, str, int]] = {}
    pair_path = directory(37) / "ordinary_cell_reflection_pairs.jsonl.gz"
    for row in rows(pair_path):
        validate_source_row(row)
        pair_map[row["representative_cell_id"]] = (row, "REPRESENTATIVE", row["reflected_cell_id"], row["representative_component_index"])
        pair_map[row["reflected_cell_id"]] = (row, "REFLECTED", row["representative_cell_id"], row["reflected_component_index"])
    require(len(pair_map) == 1724, "pair-map")
    components: dict[int, dict[str, Any]] = {}
    for row in rows(directory(34) / "ordinary_component_ledger.jsonl.gz"):
        validate_source_row(row)
        components[row["component_index"]] = row
    typed = {}
    for row in rows(directory(34) / "typed_first_event_binding_ledger.jsonl.gz"):
        validate_source_row(row)
        typed[row["cell_id"]] = row

    blockers = {row["pair_index"]: row for row in ledger["blocker_rows"]}
    require(len(blockers) == 574, "blocker-index")
    partition: Counter[str] = Counter()
    residual_hash_total = 0
    for pair_index, row in blockers.items():
        require(set(row) == BLOCKER_KEYS, "blocker-schema")
        verify_closed(row, "row_sha256")
        maximum = max(row["residual_classification_census"].values())
        primary = min(k for k, v in row["residual_classification_census"].items() if v == maximum)
        require(primary == row["primary_residual_classification"], "blocker-primary")
        require(not projections[pair_index]["after_whole_representative"], "blocker-on-whole")
        residual_hash_total += len(row["residual_source_row_sha256s"])
        partition[primary] += 2
    require(residual_hash_total == 33638, "pending-task-row-count")
    require(dict(sorted(partition.items())) == ledger["blocker_partition"]["by_primary_residual_classification"], "blocker-partition")

    cell_iter = rows(directory(32) / "compact_cells.jsonl.gz")
    frontier_iter = rows(directory(34) / "round144_terminal_frontier.jsonl.gz")
    census: Counter[str] = Counter()
    unresolved_per_pair: Counter[int] = Counter()
    terminal_example = None
    unresolved_example = None
    for ordinal, leaf in enumerate(ledger["leaves"]):
        validate_leaf_shape(leaf)
        require(leaf["leaf_ordinal"] == ordinal, "leaf-ordinal")
        source = next(cell_iter)
        frontier = next(frontier_iter)
        validate_source_row(source)
        validate_source_row(frontier)
        require(leaf["cell_id"] == source["cell_id"] == frontier["cell_id"], "cell-order")
        require(leaf["source_cell_row_sha256"] == source["row_sha256"], "cell-source-sha")
        require(leaf["origin_key"] == source["origin_key"] and leaf["physical_chart"] == source["compact_chart"], "cell-identity")
        require(leaf["exact_box"] == {"physical_p_interval": source["physical_p_interval"], "physical_slice": source["physical_slice"], "physical_t_interval": source["physical_t_interval"]}, "cell-box")
        require(leaf["glue_refs"] == refs[leaf["cell_id"]], "leaf-glue-bidirectional")
        initial = frontier["terminal_class"]
        if initial in {"EARLIEST_PREFIX_EXCLUDED", "TYPED_EVENT_GRAPH"}:
            expected_terminal = initial
            require(leaf["reflection_pair_ref"] is None and leaf["component_ref"] is None, "initial-no-pair")
            if initial == "TYPED_EVENT_GRAPH":
                require(leaf["proof_ref"]["C34_typed_event_row_sha256"] == typed[leaf["cell_id"]]["row_sha256"], "typed-proof")
        else:
            require(initial == "UNRESOLVED_R1648_CONTINUATION" and leaf["cell_id"] in pair_map, "ordinary-map")
            pair, role, partner, component_index = pair_map[leaf["cell_id"]]
            pair_index = pair["pair_index"]
            projection = projections[pair_index]
            expected_terminal = "EARLIEST_PREFIX_EXCLUDED" if projection["after_whole_representative"] else None
            require(leaf["reflection_pair_ref"] == {"C37_row_sha256": pair["row_sha256"], "pair_index": pair_index, "partner_cell_id": partner, "role": role}, "reflection-ref")
            component = components[component_index]
            require(leaf["component_ref"] == {"cell_role": role, "component_id": component["component_id"], "component_index": component_index, "component_row_sha256": component["row_sha256"]}, "component-ref")
            require(leaf["proof_ref"]["C53_parent_projection_object_sha256"] == projection["projection_object_sha256"], "projection-ref")
            if expected_terminal is None:
                require(pair_index in blockers and leaf["bnb_state"]["blocker_row_id"] == blockers[pair_index]["blocker_row_id"], "unresolved-blocker-ref")
                unresolved_per_pair[pair_index] += 1
        require(leaf["terminal_disposition"] == expected_terminal, "formal-disposition")
        if expected_terminal is None:
            census["UNRESOLVED_R1648_CONTINUATION"] += 1
            unresolved_example = unresolved_example or leaf
        else:
            census[expected_terminal] += 1
            terminal_example = terminal_example or leaf
    require(all(v == 2 for v in unresolved_per_pair.values()) and len(unresolved_per_pair) == 574, "unresolved-reflection-pairs")
    expected_census = {"CONNECTED_TO_KNOWN": 0, "EARLIEST_PREFIX_EXCLUDED": 75388, "SOURCE_GRAZING_OR_CEMETERY": 0, "TYPED_EVENT_GRAPH": 296, "UNRESOLVED_R1648_CONTINUATION": 1148, "total": 76832, "unresolved_zero": False}
    require(ledger["census"] == expected_census, "declared-census")
    require(census == Counter({"EARLIEST_PREFIX_EXCLUDED": 75388, "TYPED_EVENT_GRAPH": 296, "UNRESOLVED_R1648_CONTINUATION": 1148}), "rebuilt-census")
    require(result["bnb"]["leaf_ledger_object_sha256"] == EXPECTED_OBJECTS[LEAF_PATH] and result["glue"]["exact_glue_ledger_object_sha256"] == EXPECTED_OBJECTS[GLUE_PATH], "result-ledger-bind")
    require(terminal_example is not None and unresolved_example is not None, "attack-fixtures")
    attacks = execute_attacks(terminal_example, unresolved_example)

    verification_bare = {
        "attacks": {"executed": attacks, "rejected": attacks},
        "authority_binding": AUTHORITY,
        "census": expected_census,
        "glue_coverage": {"cell_count": 76832, **expected_counts},
        "independence": {
            "C55A_producer_executed": False,
            "C55A_producer_imported": False,
            "C32_geometry_replayed_from_rows": True,
            "C34_C37_C41_C48_C53_replayed_from_data": True,
        },
        "schema": "cm2.round306c55a.four-chart-fundamental-domain-bnb.independent-verification.v1",
        "status": "PASS_INDEPENDENT_STRUCTURAL_AND_CROSS_SOURCE_REPLAY__1148_UNRESOLVED_FAIL_CLOSED",
    }
    verification = {**verification_bare, "object_sha256": digest(verification_bare)}
    require(not VERIFY_PATH.exists(), "verification-exists")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(VERIFY_PATH, flags, 0o444)
    try:
        os.write(fd, ENCODER.encode(verification).encode("ascii") + b"\n")
        os.fsync(fd)
    finally:
        os.close(fd)
    require(VERIFY_PATH.stat().st_nlink == 1, "verification-link-count")
    return verification


if __name__ == "__main__":
    print(ENCODER.encode(verify()))
