#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c26_source_g_corrected_b1a_full_feature_dependency_and_transition_ready_cover"
FEATURE_LEDGER = PREFIX + "_feature_obligation_ledger.jsonl.gz"
HANDLE_LEDGER = PREFIX + "_transition_ready_handle_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
C10 = "cm2_round306c10_source_g_exact_graph_support_identity_rematerialization"
C21A = "cm2_round306c21a_source_g_1008_r204_A1_A2_direct_feature_kernel"
C21C = "cm2_round306c21c_source_g_79084_r211_A1_A2_incidence_closure"
C22A = "cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel"
C22B = "cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel"
C24A = "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel"
C24B = "cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel"
C25 = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger"

SOURCES = (
    ("C10", C10, (C10 + "_exact_graph_support_ledger.jsonl.gz",), "b7277863feb9edc5f35906b04af2a9a256becb7ee9f1f1df6558b897184029ca", "8be0f4a543db375c9470414d4ef632cc07f1c1881a85b1e1153f3aaea2c4a9bf"),
    ("C21A", C21A, (C21A + "_ledger.jsonl.gz",), "0aa11094c3e109e51efe4a06ffc61b65b60373de9ddbf6196889f65a03756563", "85795f2c34955832e573aad7975065c133d282511d4edccfce078e5c5b4ac655"),
    ("C21C", C21C, (C21C + "_ledger.jsonl.gz",), "341968ef1bfac345a9122fdff4bc6af3530a034be5a2496df960c3e27814a3dc", "fa29b29f90a0462d26fe9004e1faaa9aa202b4b597040b629bee539be54be0db"),
    ("C22A", C22A, (C22A + "_ledger.jsonl.gz",), "888305210de3a93904e6fb26a199ff8d8e11519940550f0f58f2733cdfbbfcce", "d47b900aa0adb69a708b61061c2a1dc2e6f3cb60bacf2dd4c746bd3b1c3d58ee"),
    ("C22B", C22B, (C22B + "_ledger.jsonl.gz",), "cd6ed594efe7cd24ddc5e267c564ad650f48f3289e06da658337743a1469399e", "2cde2eadbd150d5ff2cd6cb9412196228820bb77fea466e665a994f3fc08e55f"),
    ("C24A", C24A, (C24A + "_ledger.jsonl.gz",), "2e17d522cef9a32a971c28a7d0e6aaeab97e66da367fedf92c2bb6b418aaeacb", "c9cd71af703705ccf4862cb43052a80e55031c7e3226f2de9cba3b6668ea6107"),
    ("C24B", C24B, (C24B + "_ledger.jsonl.gz",), "9a5b8dea2ed9093070c4434bbac7af9169691d02c2c5315974f597b6927b3d13", "9409bbf8f4f75b20d10ea468822af1b171b2dc96f186e0c9a3f88666f3a1ef62"),
    ("C25", C25, (C25 + "_member_ledger.jsonl.gz", C25 + "_representation_ledger.jsonl.gz"), "8885eb09f4e0aef3107654996ef520cca3ce59f59fc5b5d8a1652d44f9bb9a81", "ad6b4ae09985f23fd0db00e79bee859014c23c6792aa732582e50aa39c745bef"),
)

NODE_COUNTS = {"A1": 17940, "A2": 62152, "R1": 295340, "R2": 295336, "G1": 5264, "G2A": 5264, "G2B": 10128}
ROLE_COUNTS = {"INDEPENDENT_DEFINITION_ROOT": 318544, "DEPENDENT_FEATURE_CLOSURE": 372880}
DEPENDENCIES = {"A1": [], "A2": ["A1"], "R1": [], "R2": ["R1"], "G1": [], "G2A": ["G1"], "G2B": ["G1"]}
HANDLE_FAMILIES = {"PRESERVED": 165744, "NON_GRAPH": 55604, "R2": 302624, "R292": 10252, "G2A": 5264, "G2B": 10128}
HANDLE_SEMANTICS = {"REPRESENTATION_SET_EQUALITY": 538680, "TYPED_NONFULL_REPRESENTATION_DISPOSITION": 2520, "EXACT_SUBCOVER_INCLUSION_DISPOSITION": 8416}


class Failure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
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
            require(type(claimed) is str and claimed == object_sha(body), "row hash:" + path.name)
            yield value


def result(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    value = json.loads(raw)
    require(wire(value) == raw, "result canonical")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    require(type(claimed) is str and claimed == object_sha(body), "result hash")
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
        require((isinstance(direct, str) and direct.startswith("PASS")) or (isinstance(nested, str) and nested.startswith("PASS")), "verification status:" + tag)
        objects[tag] = claimed
        pins.extend({"filename": name, "sha256": listed[name]} for name in ledgers)
        pins.extend(({"filename": result_name, "sha256": listed[result_name]}, {"filename": manifest_name, "sha256": manifest_sha256}))
    return objects, sorted(pins, key=lambda row: row["filename"])


def source_ledger(tag: str, index: int = 0) -> str:
    for current, _, ledgers, _, _ in SOURCES:
        if current == tag:
            return ledgers[index]
    raise Failure("unknown source:" + tag)


def feature_source_rows() -> Iterable[tuple[str, str, str, str, str, str, str]]:
    for row in rows(ROOT / source_ledger("C21A")):
        yield "C21A", row["obligation_kind"].split("_", 1)[0], row["obligation_kind"], row["feature_row_id"], row["owner_member_id"], row["feature_theorem_ast_sha256"], row["row_sha256"]
    for row in rows(ROOT / source_ledger("C21C")):
        yield "C21C", row["obligation_kind"].split("_", 1)[0], row["obligation_kind"], row["feature_row_id"], row["owner_member_id"], row["theorem_ast_sha256"], row["row_sha256"]
    for row in rows(ROOT / source_ledger("C22A")):
        yield "C22A", "R1", "R1_SOURCE_FREE_PREDICATE_CELL_DEFINITION", row["predicate_cell_row_id"], row["owner_member_id"], row["theorem_ast_sha256"], row["row_sha256"]
    for row in rows(ROOT / source_ledger("C22B")):
        if row["row_kind"] == "R2_PRIMARY_MEMBER_NORMALIZED_SUPPORT_AND_REPRESENTATION_SET_EQUALITY":
            yield "C22B", "R2", "R2_MEMBER_FULL_SUPPORT_UNION", row["member_id"], row["member_id"], row["member_union_theorem_ast_sha256"], row["row_sha256"]
    for row in rows(ROOT / source_ledger("C10")):
        yield "C10", "G1", "G1_EXACT_GRAPH_DEFINITION", row["graph_id"], row["sheet_member_id"], object_sha(row["ast_sha256"]), row["row_sha256"]
    for row in rows(ROOT / source_ledger("C24A")):
        node = row["coarse_family"]
        obligation = "G2A_GRAPH_TO_SHEET_IDENTIFICATION" if node == "G2A" else "G2B_GRAPH_TO_SIDE_PHYSICAL_INCIDENCE"
        yield "C24A", node, obligation, row["member_id"], row["member_id"], row["semantic_theorem_ast_sha256"], row["row_sha256"]
    for row in rows(ROOT / source_ledger("C24B")):
        yield "C24B", "G2B", "G2B_GRAPH_TO_SIDE_EXACT_NONINCIDENCE", row["member_id"], row["member_id"], row["semantic_theorem_ast_sha256"], row["row_sha256"]


def expected_feature(ordinal: int, source: tuple[str, str, str, str, str, str, str], objects: dict[str, str]) -> dict[str, Any]:
    tag, node, obligation_kind, feature_id, owner_member_id, theorem_sha256, source_row_sha256 = source
    role = "INDEPENDENT_DEFINITION_ROOT" if not DEPENDENCIES[node] else "DEPENDENT_FEATURE_CLOSURE"
    body = {
        "schema": "cm2.round306c26.source-g-corrected-b1a.v1.feature-obligation-row.v1",
        "feature_ordinal": ordinal,
        "row_id": PREFIX + ":feature:" + object_sha([node, feature_id]),
        "node_id": node,
        "obligation_role": role,
        "obligation_kind": obligation_kind,
        "feature_id": feature_id,
        "owner_member_id": owner_member_id,
        "depends_on_node_ids": DEPENDENCIES[node],
        "definition_or_dependency_theorem_ast_sha256": theorem_sha256,
        "source_bindings": {"source_kernel": tag, "source_ledger": source_ledger(tag), "source_row_sha256": source_row_sha256, "source_result_sha256": objects[tag]},
        "formal_credit": {"source_free_definition_root": int(role == "INDEPENDENT_DEFINITION_ROOT"), "dependent_feature_closure": int(role == "DEPENDENT_FEATURE_CLOSURE"), "B1A_feature_obligation": 1},
        "strict_nonpromotion": {"member_identity": 0, "DSU_edge": 0, "transition_theorem": 0, "pair_routing": 0, "B2": 0, "maximality": 0, "CM2": 0},
    }
    return {**body, "row_sha256": object_sha(body)}


def expected_handle(ordinal: int, source: dict[str, Any], objects: dict[str, str]) -> dict[str, Any]:
    require(source["representation_ordinal"] == ordinal and source["formal_credit"]["typed_representation_semantic_disposition"] == 1, "C25 handle source")
    certificate = {"kind": "B1A_TRANSITION_READY_REPRESENTATION_HANDLE", "typed_owner_support_bound": True, "typed_representation_semantics_closed": True, "fresh_component_binding_consumed": True, "official_key_is_metadata_only_not_filter": True, "transition_theorem_claimed": False, "pair_routing_claimed": False}
    representation_id = source["representation_id"]
    body = {
        "schema": "cm2.round306c26.source-g-corrected-b1a.v1.transition-ready-handle-row.v1",
        "handle_ordinal": ordinal,
        "row_id": PREFIX + ":handle:" + hashlib.sha256(representation_id.encode("ascii")).hexdigest(),
        "representation_id": representation_id,
        "owner_member_id": source["owner_member_id"],
        "coarse_family": source["coarse_family"],
        "fresh_component_id": source["fresh_component_id"],
        "base_root_id": source["base_root_id"],
        "official_key_id": source["official_key_id"],
        "owner_normalized_support_ast_sha256": source["owner_normalized_support_ast_sha256"],
        "representation_semantic_kind": source["representation_semantic_kind"],
        "representation_semantic_certificate_sha256": source["representation_semantic_certificate_sha256"],
        "transition_ready_certificate": certificate,
        "transition_ready_certificate_sha256": object_sha(certificate),
        "source_bindings": {"C25_representation_row_sha256": source["row_sha256"], "C25_result_sha256": objects["C25"]},
        "formal_credit": {"B1A_representation_cover": 1, "transition_ready_handle": 1, "transition_theorem": 0, "pair_routing": 0},
        "strict_nonpromotion": {"member_identity": 0, "DSU_edge": 0, "DSU_union": 0, "B2": 0, "maximality": 0, "CM2": 0},
    }
    return {**body, "row_sha256": object_sha(body)}


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": count, "size": path.stat().st_size, "sha256": file_sha(path), "row_sequence_sha256": sequence, "order": order}


def verify(candidate: Path) -> dict[str, Any]:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    preliminary, _ = result(candidate / RESULT)
    require(preliminary.get("status") == "PASS_CORRECTED_B1A_SEALED__691424_FEATURE_OBLIGATIONS_502204_MEMBER_SUPPORTS_549616_REPRESENTATIONS_AND_HANDLES__B2_REPLAY_AUTHORIZED", "preflight status")
    require(preliminary.get("feature_obligation_census", {}).get("total") == 691424, "preflight feature total")
    require(preliminary.get("formal_credit") == {"feature_obligations": 691424, "member_support_cover": 502204, "representation_semantic_cover": 549616, "transition_ready_handle_cover": 549616, "B1A": 1}, "preflight credit")
    require(preliminary.get("strict_nonpromotion") == {"transition_theorem": 0, "pair_routing": 0, "new_DSU_edges": 0, "new_DSU_unions": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"}, "preflight boundary")
    objects, pins = seal_sources()
    candidate_features = rows(candidate / FEATURE_LEDGER)
    feature_sequence = hashlib.sha256()
    node_census: Counter[str] = Counter()
    role_census: Counter[str] = Counter()
    seen: set[tuple[str, str]] = set()
    count = 0
    for ordinal, source in enumerate(feature_source_rows()):
        actual = next(candidate_features, None)
        require(actual is not None and actual == expected_feature(ordinal, source, objects), "feature reconstruction:" + str(ordinal))
        key = (actual["node_id"], actual["feature_id"])
        require(key not in seen, "feature uniqueness")
        seen.add(key)
        node_census[actual["node_id"]] += 1
        role_census[actual["obligation_role"]] += 1
        feature_sequence.update(bytes.fromhex(actual["row_sha256"]))
        count += 1
    require(next(candidate_features, None) is None and count == 691424 and dict(node_census) == NODE_COUNTS and dict(role_census) == ROLE_COUNTS, "feature census")
    c25_representations = rows(ROOT / source_ledger("C25", 1))
    candidate_handles = rows(candidate / HANDLE_LEDGER)
    handle_sequence = hashlib.sha256()
    family_census: Counter[str] = Counter()
    semantic_census: Counter[str] = Counter()
    for ordinal in range(549616):
        source = next(c25_representations, None)
        actual = next(candidate_handles, None)
        require(source is not None and actual is not None and actual == expected_handle(ordinal, source, objects), "handle reconstruction:" + str(ordinal))
        family_census[actual["coarse_family"]] += 1
        semantic_census[actual["representation_semantic_kind"]] += 1
        handle_sequence.update(bytes.fromhex(actual["row_sha256"]))
    require(next(c25_representations, None) is None and next(candidate_handles, None) is None, "handle exhaustion")
    require(dict(family_census) == HANDLE_FAMILIES and dict(semantic_census) == HANDLE_SEMANTICS, "handle census")
    feature_descriptor = descriptor(candidate / FEATURE_LEDGER, 691424, feature_sequence.hexdigest(), "C21A_THEN_C21C_THEN_C22A_THEN_C22B_PRIMARY_THEN_C10_THEN_C24A_THEN_C24B")
    handle_descriptor = descriptor(candidate / HANDLE_LEDGER, 549616, handle_sequence.hexdigest(), "C25_REPRESENTATION_LEDGER_ORDER")
    body = {
        "schema": "cm2.round306c26.source-g-corrected-b1a-full-feature-dependency-and-transition-ready-cover.v1",
        "status": "PASS_CORRECTED_B1A_SEALED__691424_FEATURE_OBLIGATIONS_502204_MEMBER_SUPPORTS_549616_REPRESENTATIONS_AND_HANDLES__B2_REPLAY_AUTHORIZED",
        "corrected_universe_census": {"members": 502204, "representations": 549616, "authorized_base_roots": 339036, "fresh_components": 57876, "cross_component_pair_denominator": 125616475670},
        "feature_obligation_census": {"total": 691424, "independent_definition_roots": 318544, "dependent_feature_closures": 372880, "by_node": dict(node_census), "by_role": dict(role_census)},
        "support_and_representation_cover": {"member_normalized_support_rows_consumed": 502204, "representation_semantic_rows_consumed": 549616, "transition_ready_handles": 549616, "representation_semantic_census": dict(semantic_census), "missing_or_orphan_or_duplicate": 0},
        "transition_ready_handle_family_census": dict(family_census),
        "gap_census": {"source_free_definition_gaps": 0, "dependent_closure_gaps": 0, "member_support_gaps": 0, "representation_semantic_gaps": 0, "transition_ready_handle_gaps": 0},
        "ledgers": {"feature_obligation": feature_descriptor, "transition_ready_handle": handle_descriptor},
        "input_pins": pins,
        "formal_credit": {"feature_obligations": 691424, "member_support_cover": 502204, "representation_semantic_cover": 549616, "transition_ready_handle_cover": 549616, "B1A": 1},
        "strict_nonpromotion": {"transition_theorem": 0, "pair_routing": 0, "new_DSU_edges": 0, "new_DSU_unions": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "REBUILD_CORRECTED_B2_TRANSITION_WITNESS_KNOWN_EDGE_RECOVERY_AND_125616475670_PAIR_MAXIMALITY_ROUTING",
    }
    expected = {**body, "result_sha256": object_sha(body)}
    actual_result, claimed = result(candidate / RESULT)
    require(actual_result == expected and claimed == expected["result_sha256"], "result reconstruction")
    return {"status": "PASS_INDEPENDENT_C26_CORRECTED_B1A_1241040_ROW_FULL_RECONSTRUCTION__B2_REPLAY_AUTHORIZED", "result_sha256": claimed, "feature_rows": 691424, "handle_rows": 549616, "total_rows": 1241040}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    candidate = ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve()
    print(wire(verify(candidate)).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
