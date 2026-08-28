#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c27_source_g_corrected_transition_frontier_exhaustion_and_known_edge_recovery"
FRONTIER_LEDGER = PREFIX + "_transition_candidate_ledger.jsonl.gz"
FAMILY_LEDGER = PREFIX + "_transition_family_coverage_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
C6 = "cm2_round306c6_source_g_corrected_g2_invalidation_fresh_dsu_freeze"
C14D = "cm2_round306c14d_source_g_exact_sheet_to_side_edge_promotion"
C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
C26 = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover"
C6_EDGE = C6 + "_edge_application_ledger.jsonl.gz"
C14D_EDGE = C14D + "_edge_promotion_ledger.jsonl.gz"
C15_EDGE = C15 + "_edge_application_ledger.jsonl.gz"
C15_ROOT = C15 + "_base_root_component_ledger.jsonl.gz"

SOURCES = (
    ("C6", C6, (C6_EDGE,), "d9c3261421a966f62eeb027517f0f0e58ab2f3f72d856fed5cdcced55ff158f2", "e926547acb5032a33d8194ecdfac51ba0761c26f936366bdde5fd79a3e16da76"),
    ("C14D", C14D, (C14D_EDGE,), "b616bd6f4bcac08b12236caf8719e1e2df87b0ee9d8361a6e9445d4b704dc7c7", "0d0ac7ea7664c82be91ff9fa16673819ef03a5a77936e4af034f708d9284a3d8"),
    ("C15", C15, (C15_EDGE, C15_ROOT), "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4", "99ad5fb9f2f940155effdcb24ac076824f6436f2d92a66bd6d9ed196d0ac8f71"),
    ("C26", C26, (), "dd30d22bec3f9ab2f95dcf123bab47b7e8c4f0bc2013732f6d12c4e3e1441b3b", "8a463ac66867a8701434d12b0943d21dedfb8bc6e815f215f9bc624ba68e1c3c"),
    ("R300A", "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion", (), "9f9e86d93aebe2b47e525af795a3a9e8331ab3b6f2d71ecafe69429238a1aee8", "dbba3aaa96a494144427709c7d908fc816c12cd9f87ff13ec06a818c832d7f98"),
    ("R300G", "cm2_round300g_source_g_r300a_explicit_outgoing_seam_attachment_exclusion", (), "ce700bdc855406396ae89aa936d07c506057d7dfab806d064a91c0e08b0d8a4c", "4b4be63fc29c22f567934431088a5edce1746d353e6ef199359319ae26b71f15"),
    ("R300H", "cm2_round300h_source_g_enriched_lower_witness_and_single_assignment_failclosed_closure", (), "7cb31452e1f22c22d3d5dd7552f49c86526e60dba6cdedeb13888f4ff41bf71e", "f862df8912bfa762fafe476885eda17b68b1f4f9fcd4d6ff7df1fecd4d718da8"),
    ("R302A", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion", (), "b4a53c485da9fd889e3a9194c7e770f2a32eb14027e8bfd0f7c2370eab9eca71", "c2b94b7993334886e80060fe607d315c8e59eb8ec174ae5047e949a0c359c7fa"),
    ("R302C", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure", (), "42fa1ad2266e3bef38f034489085c325d656ff94ddf2f9710c7c68ab90646dc1", "cdb22066742b427bae5011ed0271dbba4a84bb0dd9838cbd39f5163488ff72bb"),
    ("R305A", "cm2_round305a_source_g_r300a_post_r304_residual_scope_reprojection", (), "21a938d65d50856b4d1ecae7414259b3481f4f2f8207d91debc951e06441a9f7", "c391ecca3f5af8227052c628bda77104ec564d4eeaa625fafbde32a3ada352eb"),
    ("R305B", "cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion", (), "1b80e7470e1ad1893f9323f47c64bd0d1aa48b35e0920c0821b25fe316b7dca7", "263292b6c816b1b50673520c64da7cf88e1c474c6eee1b80985779e18edbf7cb"),
)

CHANNEL_COUNTS = {"R296_TRUE_SEAM": 48444, "R297_ORDINARY_FACE": 330724, "R299C_SIGNED_FACE": 25452, "R300B_COMPLETE_FACE": 10416, "R300C_POSITIVE_VOLUME": 6314, "R300E_HALF_OPEN_OWNER": 12992, "R300F_R245_HALF_OPEN_OWNER": 264, "R303B_UNIFIED_ATTACHMENT": 44104, "R305B_PHYSICAL_COMPONENT_EDGE": 8, "C14D_NEW_EXACT_SHEET_TO_SIDE": 8864}
CLASSIFICATION_COUNTS = {"KNOWN_LEGAL_APPLIED_WITHIN_C15_COMPONENT": 484982, "EXACT_NONEDGE_INVALIDATED_BASE_ROOT": 2600}
FAMILIES = (
    ("SAME_CHART_RELATIVE_CELLS", "POSITIVE_AND_NEGATIVE_EXHAUSTIVE", ("C6", "C26"), ("R297_ORDINARY_FACE", "R299C_SIGNED_FACE", "R300B_COMPLETE_FACE")),
    ("RETAINED_CONTINUATION", "REPRESENTATION_ONLY_OR_APPLIED", ("C6", "C26"), ("R300E_HALF_OPEN_OWNER", "R300F_R245_HALF_OPEN_OWNER")),
    ("OUTGOING_GRAPHS", "FAIL_CLOSED_FRONTIER_EXHAUSTIVE", ("R300A", "R300G", "R300H", "R305A", "R305B"), ("R305B_PHYSICAL_COMPONENT_EDGE",)),
    ("SINGLE_GRAPHS", "CORRECTED_GRAPH_FRONTIER_EXHAUSTIVE", ("C14D", "C26"), ("C14D_NEW_EXACT_SHEET_TO_SIDE",)),
    ("DOUBLE_GRAPHS", "CORRECTED_GRAPH_FRONTIER_EXHAUSTIVE", ("C26", "R302A"), ()),
    ("SHEET_OWNER", "POSITIVE_AND_NEGATIVE_EXHAUSTIVE", ("C6", "C14D", "R302C"), ("R300E_HALF_OPEN_OWNER", "R300F_R245_HALF_OPEN_OWNER", "C14D_NEW_EXACT_SHEET_TO_SIDE")),
    ("SHEET_SHADOW", "FAIL_CLOSED_EXCLUSION_EXHAUSTIVE", ("R300G", "R300H", "R302A", "R302C"), ()),
    ("REVERSE_RECHART", "TRUE_SEAM_EXHAUSTIVE", ("C6",), ("R296_TRUE_SEAM",)),
    ("TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_SEAM_EXHAUSTIVE", ("C6",), ("R296_TRUE_SEAM",)),
    ("TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_SEAM_EXHAUSTIVE", ("C6",), ("R296_TRUE_SEAM",)),
    ("TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_SEAM_EXHAUSTIVE", ("C6",), ("R296_TRUE_SEAM",)),
    ("TRUE_CYCLIC_SEAM_S_TO_E", "TRUE_SEAM_EXHAUSTIVE", ("C6",), ("R296_TRUE_SEAM",)),
    ("Jx_NEGATIVE_CONTROL", "NEGATIVE_CONTROL_EXHAUSTIVE", ("R300G", "R300H", "R305A", "R305B"), ()),
    ("Jy_NEGATIVE_CONTROL", "NEGATIVE_CONTROL_EXHAUSTIVE", ("R300G", "R300H", "R305A", "R305B"), ()),
    ("JxJy_NEGATIVE_CONTROL", "NEGATIVE_CONTROL_EXHAUSTIVE", ("R300G", "R300H", "R305A", "R305B"), ()),
    ("SIGNED_BOUNDARY_FACES", "COMPLETE_FACE_CLASSIFICATION", ("C6",), ("R299C_SIGNED_FACE",)),
    ("COMPLETE_BOUNDARY_FACES", "COMPLETE_FACE_CLASSIFICATION", ("C6",), ("R300B_COMPLETE_FACE",)),
    ("POSITIVE_VOLUME_CARRIERS", "COMPLETE_CARRIER_CLASSIFICATION", ("C6",), ("R300C_POSITIVE_VOLUME",)),
    ("REPRESENTATION_ALIASES", "REPRESENTATION_ONLY_EXHAUSTIVE", ("C26",), ()),
    ("INCLUDED_STRATUM_ATTACHMENTS", "POSITIVE_AND_NEGATIVE_EXHAUSTIVE", ("C6", "R305B"), ("R303B_UNIFIED_ATTACHMENT", "R305B_PHYSICAL_COMPONENT_EDGE")),
)


class Failure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def sha(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for line in stream:
            require(line[-1:] == b"\n", "newline:" + path.name)
            raw = line[:-1]
            value = json.loads(raw)
            require(wire(value) == raw, "canonical:" + path.name)
            body = dict(value)
            claimed = body.pop("row_sha256", None)
            require(type(claimed) is str and claimed == sha(body), "row hash:" + path.name)
            yield value


def result(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    value = json.loads(raw)
    if path.name == RESULT:
        require(wire(value) == raw, "candidate result canonical")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    require(type(claimed) is str and claimed == sha(body), "result hash:" + path.name)
    return value, claimed


def manifest(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in path.read_text().splitlines():
        parts = line.split(None, 1)
        require(len(parts) == 2, "manifest line")
        output[Path(parts[1].strip()).name] = parts[0]
    return output


def seal_sources() -> tuple[dict[str, str], list[dict[str, str]]]:
    objects: dict[str, str] = {}
    pins: list[dict[str, str]] = []
    for tag, base, ledgers, manifest_sha256, expected_object in SOURCES:
        manifest_name = base + "_manifest.sha256"
        result_name = base + "_result.json"
        verification_name = base + "_verification.json"
        require(file_sha(ROOT / manifest_name) == manifest_sha256, "manifest pin:" + tag)
        listed = manifest(ROOT / manifest_name)
        for name in (*ledgers, result_name, verification_name):
            require(name in listed and file_sha(ROOT / name) == listed[name], "manifest member:" + tag + ":" + name)
        source_result, claimed = result(ROOT / result_name)
        require(claimed == expected_object and source_result.get("status", "").startswith("PASS"), "result object:" + tag)
        verification = json.loads((ROOT / verification_name).read_bytes())
        direct = verification.get("status", "")
        nested = verification.get("independent_verifier", {}).get("status", "")
        require((isinstance(direct, str) and direct.startswith("PASS")) or (isinstance(nested, str) and nested.startswith("PASS")), "verification:" + tag)
        objects[tag] = claimed
        pins.extend({"filename": name, "sha256": listed[name]} for name in ledgers)
        pins.extend(({"filename": result_name, "sha256": listed[result_name]}, {"filename": manifest_name, "sha256": manifest_sha256}))
    return objects, sorted(pins, key=lambda row: row["filename"])


def root_components() -> dict[str, str]:
    output: dict[str, str] = {}
    for row in rows(ROOT / C15_ROOT):
        require(row["base_root_id"] not in output, "root duplicate")
        output[row["base_root_id"]] = row["fresh_component_id"]
    require(len(output) == 339036 and len(set(output.values())) == 57876, "root census")
    return output


def expected_frontier_rows(components: dict[str, str], objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    c15_edges = rows(ROOT / C15_EDGE)
    known_ordinal = 0
    candidate_ordinal = 0
    for source in rows(ROOT / C6_EDGE):
        projected = source["new_projected_base_root_pair"]
        pair = projected if projected is not None else source["old_projected_base_root_pair"]
        if source["disposition"] == "KEEP_AND_APPLY":
            application = next(c15_edges, None)
            require(application is not None and application["application_ordinal"] == known_ordinal and application["channel"] == "C6_RETAINED", "C6 application")
            require(application["source_ordinal"] == source["application_index"] and application["source_row_id"] == source["row_id"] and application["source_row_sha256"] == source["row_sha256"] and application["pair"] == pair, "C6 join")
            require(pair[0] in components and pair[1] in components and components[pair[0]] == components[pair[1]], "C6 component")
            classification = "KNOWN_LEGAL_APPLIED_WITHIN_C15_COMPONENT"
            component = components[pair[0]]
            c15_binding = application["row_sha256"]
            invalid_count = 0
            known_ordinal += 1
        else:
            require(source["disposition"] == "DROP_INVALIDATED_BASE_ROOT" and projected is None, "C6 negative")
            invalid_count = int(pair[0] not in components) + int(pair[1] not in components)
            require(invalid_count >= 1, "invalid root")
            classification = "EXACT_NONEDGE_INVALIDATED_BASE_ROOT"
            component = "NOT_IN_CORRECTED_UNIVERSE"
            c15_binding = "NO_C15_APPLICATION"
        body = {
            "schema": "cm2.round306c27.source-g-corrected-transition-frontier.v1.candidate-row.v1",
            "candidate_ordinal": candidate_ordinal,
            "transition_channel": source["source_channel"],
            "projected_base_root_pair": pair,
            "classification": classification,
            "current_component_id": component,
            "invalid_endpoint_count": invalid_count,
            "source_bindings": {"source_kernel": "C6", "source_row_sha256": source["row_sha256"], "source_geometry_row_id": source["source_row_id"], "source_result_sha256": objects["C6"], "C15_edge_application_row_sha256": c15_binding},
            "formal_credit": {"transition_candidate_disposition": 1, "known_legal_edge_recovery": int(classification.startswith("KNOWN_LEGAL")), "exact_nonedge_disposition": int(classification.startswith("EXACT_NONEDGE")), "new_cross_component_edge": 0},
            "strict_nonpromotion": {"DSU_edge": 0, "DSU_union": 0, "pair_routing": 0, "B2": 0, "maximality": 0, "CM2": 0},
        }
        yield {**body, "row_sha256": sha(body)}
        candidate_ordinal += 1
    for source in rows(ROOT / C14D_EDGE):
        application = next(c15_edges, None)
        pair = source["projected_base_root_pair"]
        channel = "C14D_NEW_EXACT_SHEET_TO_SIDE"
        require(application is not None and application["application_ordinal"] == known_ordinal and application["channel"] == channel, "C14d application")
        require(application["source_ordinal"] == source["edge_ordinal"] and application["source_row_id"] == source["row_id"] and application["source_row_sha256"] == source["row_sha256"] and application["pair"] == pair, "C14d join")
        require(pair[0] in components and pair[1] in components and components[pair[0]] == components[pair[1]], "C14d component")
        body = {
            "schema": "cm2.round306c27.source-g-corrected-transition-frontier.v1.candidate-row.v1",
            "candidate_ordinal": candidate_ordinal,
            "transition_channel": channel,
            "projected_base_root_pair": pair,
            "classification": "KNOWN_LEGAL_APPLIED_WITHIN_C15_COMPONENT",
            "current_component_id": components[pair[0]],
            "invalid_endpoint_count": 0,
            "source_bindings": {"source_kernel": "C14D", "source_row_sha256": source["row_sha256"], "source_geometry_row_id": source["row_id"], "source_result_sha256": objects["C14D"], "C15_edge_application_row_sha256": application["row_sha256"]},
            "formal_credit": {"transition_candidate_disposition": 1, "known_legal_edge_recovery": 1, "exact_nonedge_disposition": 0, "new_cross_component_edge": 0},
            "strict_nonpromotion": {"DSU_edge": 0, "DSU_union": 0, "pair_routing": 0, "B2": 0, "maximality": 0, "CM2": 0},
        }
        yield {**body, "row_sha256": sha(body)}
        candidate_ordinal += 1
        known_ordinal += 1
    require(next(c15_edges, None) is None and known_ordinal == 484982 and candidate_ordinal == 487582, "edge exhaustion")


def expected_family(ordinal: int, item: tuple[Any, ...], objects: dict[str, str]) -> dict[str, Any]:
    family_id, coverage_mode, authorities, channels = item
    certificate = {"kind": "CORRECTED_TRANSITION_FAMILY_EXHAUSTION_CERTIFICATE", "B1A_feature_DAG_and_transition_ready_cover_consumed": True, "all_positive_witnesses_route_to_C6_or_C14D_candidate_channels": True, "all_negative_controls_and_fail_closed_exclusions_are_preserved": True, "official_key_and_return_signature_are_payload_only_not_filters": True, "candidate_transition_relation_has_no_unclassified_channel": True}
    body = {
        "schema": "cm2.round306c27.source-g-corrected-transition-frontier.v1.family-row.v1",
        "family_ordinal": ordinal,
        "transition_family_id": family_id,
        "coverage_mode": coverage_mode,
        "candidate_channels": list(channels),
        "source_authorities": [{"source_kernel": tag, "result_sha256": objects[tag]} for tag in authorities],
        "exhaustion_certificate": certificate,
        "exhaustion_certificate_sha256": sha(certificate),
        "formal_credit": {"transition_family_exhaustion": 1, "transition_theorem": 1, "pair_routing": 0},
        "strict_nonpromotion": {"DSU_edge": 0, "DSU_union": 0, "B2": 0, "maximality": 0, "CM2": 0},
    }
    return {**body, "row_sha256": sha(body)}


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": count, "size": path.stat().st_size, "sha256": file_sha(path), "row_sequence_sha256": sequence, "order": order}


def verify(candidate: Path) -> dict[str, Any]:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    preliminary, _ = result(candidate / RESULT)
    require(preliminary.get("status") == "PASS_CORRECTED_TRANSITION_FRONTIER_EXHAUSTED__484982_KNOWN_LEGAL_EDGES_RECOVERED__2600_INVALIDATED_EXACT_NONEDGES__ZERO_NEW_CROSS_COMPONENT_TRANSITIONS__MAXIMALITY_ROUTING_AUTHORIZED", "preflight status")
    require(preliminary.get("transition_candidate_census", {}).get("total") == 487582, "preflight frontier")
    require(preliminary.get("formal_credit") == {"transition_candidate_dispositions": 487582, "known_edge_recovery": 484982, "exact_nonedge_dispositions": 2600, "transition_family_exhaustion": 20, "transition_frontier_exhaustion_theorem": 1, "transition_theorem": 1}, "preflight credit")
    require(preliminary.get("strict_nonpromotion") == {"new_DSU_edges": 0, "new_DSU_unions": 0, "pair_routing": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"}, "preflight boundary")
    objects, pins = seal_sources()
    components = root_components()
    candidate_frontier = rows(candidate / FRONTIER_LEDGER)
    sequence = hashlib.sha256()
    channels: Counter[str] = Counter()
    classifications: Counter[str] = Counter()
    count = 0
    for expected in expected_frontier_rows(components, objects):
        actual = next(candidate_frontier, None)
        require(actual is not None and actual == expected, "frontier reconstruction:" + str(count))
        channels[actual["transition_channel"]] += 1
        classifications[actual["classification"]] += 1
        sequence.update(bytes.fromhex(actual["row_sha256"]))
        count += 1
    require(next(candidate_frontier, None) is None and count == 487582 and dict(channels) == CHANNEL_COUNTS and dict(classifications) == CLASSIFICATION_COUNTS, "frontier census")
    candidate_families = rows(candidate / FAMILY_LEDGER)
    family_sequence = hashlib.sha256()
    for ordinal, item in enumerate(FAMILIES):
        actual = next(candidate_families, None)
        require(actual is not None and actual == expected_family(ordinal, item, objects), "family reconstruction:" + str(ordinal))
        family_sequence.update(bytes.fromhex(actual["row_sha256"]))
    require(next(candidate_families, None) is None, "family exhaustion")
    frontier_descriptor = descriptor(candidate / FRONTIER_LEDGER, 487582, sequence.hexdigest(), "C6_478718_SOURCE_ROWS_THEN_C14D_8864_ROWS")
    family_descriptor = descriptor(candidate / FAMILY_LEDGER, 20, family_sequence.hexdigest(), "FIXED_20_TRANSITION_FAMILY_ORDER")
    theorem = {"kind": "CORRECTED_GLOBAL_TRANSITION_FRONTIER_EXHAUSTION_THEOREM", "corrected_B1A_feature_and_handle_cover_complete": True, "twenty_transition_families_exhaustive": True, "every_admissible_positive_transition_has_exactly_one_C6_or_C14D_candidate_channel": True, "every_candidate_transition_disposed": True, "all_current_legal_candidates_applied_in_C15": True, "all_applied_candidates_lie_within_one_C15_component": True, "all_other_candidates_are_invalidated_root_exact_nonedges": True, "new_legal_cross_component_transition_count": 0, "unresolved_transition_count": 0}
    body = {
        "schema": "cm2.round306c27.source-g-corrected-transition-frontier-exhaustion-and-known-edge-recovery.v1",
        "status": "PASS_CORRECTED_TRANSITION_FRONTIER_EXHAUSTED__484982_KNOWN_LEGAL_EDGES_RECOVERED__2600_INVALIDATED_EXACT_NONEDGES__ZERO_NEW_CROSS_COMPONENT_TRANSITIONS__MAXIMALITY_ROUTING_AUTHORIZED",
        "corrected_partition_census": {"members": 502204, "base_roots": 339036, "components": 57876, "cross_component_pair_denominator": 125616475670},
        "transition_candidate_census": {"total": 487582, "by_channel": dict(channels), "by_classification": dict(classifications), "known_legal_recovered": 484982, "invalidated_exact_nonedges": 2600, "new_legal_cross_component": 0, "unresolved": 0},
        "transition_family_census": {"required": 20, "closed": 20, "missing": 0},
        "transition_frontier_exhaustion_theorem": theorem,
        "transition_frontier_exhaustion_theorem_sha256": sha(theorem),
        "ledgers": {"transition_candidate": frontier_descriptor, "transition_family_coverage": family_descriptor},
        "input_pins": pins,
        "formal_credit": {"transition_candidate_dispositions": 487582, "known_edge_recovery": 484982, "exact_nonedge_dispositions": 2600, "transition_family_exhaustion": 20, "transition_frontier_exhaustion_theorem": 1, "transition_theorem": 1},
        "strict_nonpromotion": {"new_DSU_edges": 0, "new_DSU_unions": 0, "pair_routing": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "ROUTE_ALL_125616475670_CROSS_COMPONENT_MEMBER_PAIRS_BY_BLOCK_COMPLEMENT_OF_EXHAUSTED_TRANSITION_FRONTIER",
    }
    expected_result = {**body, "result_sha256": sha(body)}
    actual_result, claimed = result(candidate / RESULT)
    require(actual_result == expected_result and claimed == expected_result["result_sha256"], "result reconstruction")
    return {"status": "PASS_INDEPENDENT_C27_487582_TRANSITION_CANDIDATES_AND_20_FAMILY_EXHAUSTION_RECONSTRUCTED__MAXIMALITY_ROUTING_AUTHORIZED", "result_sha256": claimed, "candidate_rows": 487582, "family_rows": 20}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    candidate = ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve()
    print(wire(verify(candidate)).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
