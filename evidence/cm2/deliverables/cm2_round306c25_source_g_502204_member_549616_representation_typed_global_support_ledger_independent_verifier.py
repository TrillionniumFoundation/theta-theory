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
PREFIX = "cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger"
MEMBER_LEDGER = PREFIX + "_member_ledger.jsonl.gz"
REPRESENTATION_LEDGER = PREFIX + "_representation_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
C15_BASE = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
C15_MEMBER = C15_BASE + "_member_component_ledger.jsonl.gz"
C16_BASE = "cm2_round306c16a_source_g_identity_representation_family_replay"
C16_MEMBER = C16_BASE + "_member_identity_family_ledger.jsonl.gz"
C16_REPRESENTATION = C16_BASE + "_representation_ledger.jsonl.gz"

SOURCES = (
    ("C15", C15_BASE, (C15_MEMBER,), "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4", "99ad5fb9f2f940155effdcb24ac076824f6436f2d92a66bd6d9ed196d0ac8f71"),
    ("C16A", C16_BASE, (C16_MEMBER, C16_REPRESENTATION), "597a9a402190989baa72f0e7955be376b3142850695096e2fdc6d651ce3ce7f4", "46150e0b5331b1f7c3a4591ad9072e6e987746944af6aa4ac0526c06322f8e44"),
    ("C19A", "cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel", ("cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz",), "c6d6a004aaa49c1e98223934afd325c23220ce0ce44f408b3f1c07c995791502", "dc2ebd8ca4b375d72086643b59325468811f436ce89320db59ce5c9207374f58"),
    ("C19B", "cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel", ("cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz",), "82fdf7d81f79727d326dcd6b92fe6c5d02228504047232a430c6e30767fb0bdf", "0139af153531fa482181431a04022b9cf89efc1393c75c29b7e3767fa73e13f6"),
    ("C19C", "cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel", ("cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz",), "021ae36b83178ee49c6e8bdf9b32b1a139660752c82aec311eebf2b7d5a10a92", "3482ebe2e9adfe9d6aa15236c689d9e81009c554022cd1269bcad28cb216308f"),
    ("C19D", "cm2_round306c19d_source_g_4432_retained_outer_envelope_sheet_support_kernel", ("cm2_round306c19d_source_g_4432_retained_outer_envelope_sheet_support_kernel_ledger.jsonl.gz",), "9dee4ba6e95d12716f58dd66927591562fb33f1e6f6166c801399f2282325602", "e85db00615e9719d3e8e7d4deea5fc25e945c3d8a141c3af02cc2817e7bbcbf3"),
    ("C20A", "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel", ("cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz",), "124771a897a37b0a6dffb933eaf9e9852c405514b584d16ba50e32ca5bb91158", "a1247449093af5695c11934911080f0c346c75d30647bbba7379bf18cfaf300e"),
    ("C20B", "cm2_round306c20b_source_g_36680_preserved_exact_equal_alias_support_kernel", ("cm2_round306c20b_source_g_36680_preserved_exact_equal_alias_support_kernel_ledger.jsonl.gz",), "a8919465e5252eba0d0c94a0831d8d3f94f040949caafb590c5c201ba3cd0a03", "e374987445c787050460be177b638dd7601401b45ddd1f15b0ba5ed58c67fd61"),
    ("C20C", "cm2_round306c20c_source_g_76_fixed_sign_t2ps_exact_alias_support_kernel", ("cm2_round306c20c_source_g_76_fixed_sign_t2ps_exact_alias_support_kernel_ledger.jsonl.gz",), "2849273cc639dee4cd776b0286bc2a8057dc9e49ca84b4892ed40dcd84455ef8", "2b8c5bb80aa4165e166c2daa2bde665be6df2e7cc4c5b57c17cae893d921fa97"),
    ("C20D", "cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel", ("cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel_ledger.jsonl.gz",), "e73ee2690a41c18a6110dc920eecb26c13766b26a814ea6fb38ad70a310ce0a8", "946bf9772c39efb6c9a39a8b518e8e830b96f42e429b6c629c53c031260451ab"),
    ("C22B", "cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel", ("cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_ledger.jsonl.gz",), "cd6ed594efe7cd24ddc5e267c564ad650f48f3289e06da658337743a1469399e", "2cde2eadbd150d5ff2cd6cb9412196228820bb77fea466e665a994f3fc08e55f"),
    ("C23B", "cm2_round306c23b_source_g_9404_r292_component_union_and_10252_representation_semantic_kernel", ("cm2_round306c23b_source_g_9404_r292_component_union_and_10252_representation_semantic_kernel_ledger.jsonl.gz",), "a9d8ecb93d719320894ef2520b697a67ef710a7c45339a72cc3f419461c802cf", "b7b4878f0e809417bed3be52c2ad0ca8949f24a51aeacb92408b83410e6903f3"),
    ("C24A", "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel", ("cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz",), "2e17d522cef9a32a971c28a7d0e6aaeab97e66da367fedf92c2bb6b418aaeacb", "c9cd71af703705ccf4862cb43052a80e55031c7e3226f2de9cba3b6668ea6107"),
    ("C24B", "cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel", ("cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_ledger.jsonl.gz",), "9a5b8dea2ed9093070c4434bbac7af9169691d02c2c5315974f597b6927b3d13", "9409bbf8f4f75b20d10ea468822af1b171b2dc96f186e0c9a3f88666f3a1ef62"),
)

MEMBER_FAMILIES = {"PRESERVED": 126468, "NON_GRAPH": 55604, "R2": 295336, "R292": 9404, "G2A": 5264, "G2B": 10128}
REPRESENTATION_FAMILIES = {"PRESERVED": 165744, "NON_GRAPH": 55604, "R2": 302624, "R292": 10252, "G2A": 5264, "G2B": 10128}
MEMBER_SOURCES = {"C19A": 5596, "C19B": 12232, "C19C": 33344, "C19D": 4432, "C20A": 126468, "C22B": 295336, "C23B": 9404, "C24A": 15224, "C24B": 168}
REPRESENTATION_SOURCES = {"C19A": 5596, "C19B": 12232, "C19C": 33344, "C19D": 4432, "C20A": 126468, "C20B": 36680, "C20C": 76, "C20D": 2520, "C22B": 302624, "C23B": 10252, "C24A": 15224, "C24B": 168}


class Failure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def wire(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(wire(value)).hexdigest()


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def checked_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as source:
        for line in source:
            require(line[-1:] == b"\n", "newline:" + path.name)
            raw = line[:-1]
            row = json.loads(raw)
            require(wire(row) == raw, "canonical row:" + path.name)
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            require(type(claimed) is str and claimed == object_hash(body), "row hash:" + path.name)
            yield row


def checked_result(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    value = json.loads(raw)
    require(wire(value) == raw, "canonical result:" + path.name)
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    require(type(claimed) is str and claimed == object_hash(body), "result hash:" + path.name)
    return value, claimed


def read_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        parts = line.split(None, 1)
        require(len(parts) == 2, "manifest syntax:" + path.name)
        result[Path(parts[1].strip()).name] = parts[0]
    return result


def seal_sources() -> tuple[dict[str, str], list[dict[str, str]]]:
    objects: dict[str, str] = {}
    pins: list[dict[str, str]] = []
    for tag, base, ledger_names, manifest_sha256, expected_object in SOURCES:
        manifest_name = base + "_manifest.sha256"
        result_name = base + "_result.json"
        verification_name = base + "_verification.json"
        require(sha256_file(ROOT / manifest_name) == manifest_sha256, "manifest pin:" + tag)
        listed = read_manifest(ROOT / manifest_name)
        for name in (*ledger_names, result_name, verification_name):
            require(name in listed and sha256_file(ROOT / name) == listed[name], "manifest member:" + tag + ":" + name)
        result, claimed = checked_result(ROOT / result_name)
        require(claimed == expected_object and result.get("status", "").startswith("PASS"), "sealed result:" + tag)
        verification = json.loads((ROOT / verification_name).read_bytes())
        direct = verification.get("status", "")
        nested = verification.get("independent_verifier", {}).get("status", "")
        require((isinstance(direct, str) and direct.startswith("PASS")) or (isinstance(nested, str) and nested.startswith("PASS")), "sealed verification:" + tag)
        objects[tag] = claimed
        for name in ledger_names:
            pins.append({"filename": name, "sha256": listed[name]})
        pins.extend(({"filename": result_name, "sha256": listed[result_name]}, {"filename": manifest_name, "sha256": manifest_sha256}))
    return objects, sorted(pins, key=lambda row: row["filename"])


def ledger_for(tag: str) -> str:
    matches = [ledgers[0] for current, _, ledgers, _, _ in SOURCES if current == tag]
    require(len(matches) == 1, "ledger lookup:" + tag)
    return matches[0]


def rebuild_indexes() -> tuple[dict[str, tuple[Any, ...]], dict[str, tuple[Any, ...]], Counter[str], Counter[str]]:
    member_index: dict[str, tuple[Any, ...]] = {}
    representation_index: dict[str, tuple[Any, ...]] = {}
    member_counts: Counter[str] = Counter()
    representation_counts: Counter[str] = Counter()

    def member(member_id: str, family: str, tag: str, row: dict[str, Any], support: str, certificate: str, kind: str) -> None:
        require(member_id not in member_index, "member collision")
        member_index[member_id] = (family, tag, row["row_sha256"], support, certificate, kind, row.get("fresh_component_id"), row.get("base_root_id"), row.get("official_key_id"))
        member_counts[tag] += 1

    def representation(representation_id: str, owner_id: str, family: str, tag: str, row: dict[str, Any], kind: str, equality: int, certificate: str, owner_support: str | None = None) -> None:
        require(representation_id not in representation_index, "representation collision")
        representation_index[representation_id] = (owner_id, family, tag, row["row_sha256"], kind, equality, certificate, owner_support, row.get("fresh_component_id"))
        representation_counts[tag] += 1

    for tag in ("C19A", "C19B", "C19C", "C19D"):
        for row in checked_rows(ROOT / ledger_for(tag)):
            certificate = object_hash(row["construction_certificate"])
            member(row["member_id"], "NON_GRAPH", tag, row, row["support_ast_sha256"], certificate, "EXACT_MEMBER_SUPPORT_EQUALITY")
            representation(row["representation_id"], row["member_id"], "NON_GRAPH", tag, row, "REPRESENTATION_SET_EQUALITY", 1, certificate, row["support_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C20A")):
        certificate = object_hash(row["construction_certificate"])
        member(row["member_id"], "PRESERVED", "C20A", row, row["support_ast_sha256"], certificate, "EXACT_MEMBER_SUPPORT_EQUALITY")
        representation(row["representation_id"], row["member_id"], "PRESERVED", "C20A", row, "REPRESENTATION_SET_EQUALITY", 1, certificate, row["support_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C20B")):
        representation(row["representation_id"], row["owner_member_id"], "PRESERVED", "C20B", row, "REPRESENTATION_SET_EQUALITY", 1, object_hash(row["set_equality_certificate"]), row["representation_support_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C20C")):
        representation(row["representation_id"], row["owner_member_id"], "PRESERVED", "C20C", row, "REPRESENTATION_SET_EQUALITY", 1, row["T2PS_bijection_theorem_sha256"], row["owner_support_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C20D")):
        representation(row["representation_id"], row["owner_member_id"], "PRESERVED", "C20D", row, "TYPED_NONFULL_REPRESENTATION_DISPOSITION", 0, object_hash(row["negative_disposition"]), row["owner_support_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C22B")):
        if row["row_kind"] == "R2_PRIMARY_MEMBER_NORMALIZED_SUPPORT_AND_REPRESENTATION_SET_EQUALITY":
            member(row["member_id"], "R2", "C22B", row, row["normalized_support_ast_sha256"], row["member_union_theorem_ast_sha256"], "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY")
            representation(row["representation_id"], row["member_id"], "R2", "C22B", row, "REPRESENTATION_SET_EQUALITY", 1, row["member_union_theorem_ast_sha256"], row["normalized_support_ast_sha256"])
        else:
            require(row["row_kind"] == "R2_R287_ALIAS_EXACT_SUBCOVER_INCLUSION_DISPOSITION", "R2 semantic type")
            representation(row["representation_id"], row["member_id"], "R2", "C22B", row, "EXACT_SUBCOVER_INCLUSION_DISPOSITION", 0, row["subcover_theorem_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C23B")):
        if row["row_kind"] == "R292_MEMBER_NORMALIZED_SUPPORT_SET_EQUALITY":
            member(row["member_id"], "R292", "C23B", row, row["normalized_support_ast_sha256"], row["member_union_theorem_ast_sha256"], "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY")
        else:
            require(row["row_kind"] in {"R292_SINGLE_CELL_REPRESENTATION_SET_EQUALITY", "R292_COMPONENT_CELL_EXACT_SUBCOVER_INCLUSION_DISPOSITION"}, "R292 semantic type")
            equality = int(row["formal_credit"]["representation_set_equality"])
            kind = "REPRESENTATION_SET_EQUALITY" if equality else "EXACT_SUBCOVER_INCLUSION_DISPOSITION"
            representation(row["representation_id"], row["member_id"], "R292", "C23B", row, kind, equality, row["representation_theorem_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C24A")):
        family = row["coarse_family"]
        member(row["member_id"], family, "C24A", row, row["normalized_support_ast_sha256"], row["semantic_theorem_ast_sha256"], "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY")
        representation(row["canonical_representation_id"], row["member_id"], family, "C24A", row, "REPRESENTATION_SET_EQUALITY", 1, row["semantic_theorem_ast_sha256"], row["normalized_support_ast_sha256"])
    for row in checked_rows(ROOT / ledger_for("C24B")):
        member(row["member_id"], "G2B", "C24B", row, row["normalized_support_ast_sha256"], row["semantic_theorem_ast_sha256"], "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY")
        representation(row["sole_registered_representation_id"], row["member_id"], "G2B", "C24B", row, "REPRESENTATION_SET_EQUALITY", 1, row["semantic_theorem_ast_sha256"], row["normalized_support_ast_sha256"])
    require(len(member_index) == 502204 and dict(member_counts) == MEMBER_SOURCES, "member index census")
    require(len(representation_index) == 549616 and dict(representation_counts) == REPRESENTATION_SOURCES, "representation index census")
    for representation_id, value in representation_index.items():
        owner_id, family, _, _, _, _, _, asserted_support, _ = value
        require(owner_id in member_index and member_index[owner_id][0] == family, "representation owner anti-join:" + representation_id)
        if asserted_support is not None:
            require(asserted_support == member_index[owner_id][3], "representation owner support:" + representation_id)
    return member_index, representation_index, member_counts, representation_counts


def expected_member(ordinal: int, c15: dict[str, Any], c16: dict[str, Any], source: tuple[Any, ...], result_objects: dict[str, str]) -> dict[str, Any]:
    family, tag, source_row, support, certificate, kind, source_component, source_root, source_key = source
    member_id = c16["member_id"]
    require((c15["member_ordinal"], c16["member_ordinal"]) == (ordinal, ordinal), "member ordinal")
    require(c15["registry_member_id"] == member_id, "member identity join")
    require((c15["fresh_component_id"], c15["base_root_id"], c15["official_key_id"]) == (c16["fresh_component_id"], c16["base_root_id"], c16["official_key_id"]), "member binding join")
    require(c16["C15_member_ref"][0] == ordinal and c16["C15_member_ref"][1] == c15["row_id"] and c16["C15_member_ref"][3] == c15["row_sha256"], "member ref")
    require(family == c16["coarse_family"], "member family")
    require(source_component is None or source_component == c16["fresh_component_id"], "source component")
    require(source_root is None or source_root == c16["base_root_id"], "source root")
    require(source_key is None or source_key == c16["official_key_id"], "source key")
    body = {
        "schema": "cm2.round306c25.source-g-typed-global-support-ledger.v1.member-row.v1",
        "member_ordinal": ordinal,
        "row_id": PREFIX + ":member:" + hashlib.sha256(member_id.encode("ascii")).hexdigest(),
        "member_id": member_id,
        "coarse_family": family,
        "fresh_component_id": c16["fresh_component_id"],
        "base_root_id": c16["base_root_id"],
        "official_key_id": c16["official_key_id"],
        "normalized_support_ast_sha256": support,
        "support_semantic_kind": kind,
        "support_semantic_certificate_sha256": certificate,
        "source_bindings": {"C15_member_row_sha256": c15["row_sha256"], "C16a_member_row_sha256": c16["row_sha256"], "support_kernel": tag, "support_kernel_ledger": ledger_for(tag), "support_kernel_row_sha256": source_row, "support_kernel_result_sha256": result_objects[tag]},
        "formal_credit": {"fresh_DSU_member_binding": 1, "typed_member_identity": 1, "member_normalized_support_set_equality": 1, "typed_global_support_ledger": 1},
        "strict_nonpromotion": {"B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
    }
    return {**body, "row_sha256": object_hash(body)}


def expected_representation(ordinal: int, c16: dict[str, Any], source: tuple[Any, ...], owner_support: tuple[Any, ...], result_objects: dict[str, str]) -> dict[str, Any]:
    owner_id, family, tag, source_row, kind, equality, certificate, _, source_component = source
    representation_id = c16["representation_id"]
    require(c16["representation_ordinal"] == ordinal, "representation ordinal")
    require((owner_id, family) == (c16["owner_member_id"], c16["coarse_family"]), "representation owner join")
    require(source_component is None or source_component == c16["fresh_component_id"], "representation component")
    require(owner_support[0] == family, "owner support family")
    body = {
        "schema": "cm2.round306c25.source-g-typed-global-support-ledger.v1.representation-row.v1",
        "representation_ordinal": ordinal,
        "row_id": PREFIX + ":representation:" + hashlib.sha256(representation_id.encode("ascii")).hexdigest(),
        "representation_id": representation_id,
        "owner_member_id": owner_id,
        "coarse_family": family,
        "fresh_component_id": c16["fresh_component_id"],
        "base_root_id": c16["base_root_id"],
        "official_key_id": c16["official_key_id"],
        "owner_normalized_support_ast_sha256": owner_support[3],
        "representation_semantic_kind": kind,
        "representation_semantic_certificate_sha256": certificate,
        "source_bindings": {"C16a_representation_row_sha256": c16["row_sha256"], "semantic_kernel": tag, "semantic_kernel_ledger": ledger_for(tag), "semantic_kernel_row_sha256": source_row, "semantic_kernel_result_sha256": result_objects[tag]},
        "formal_credit": {"typed_representation_identity_owner_binding": 1, "typed_representation_semantic_disposition": 1, "representation_set_equality": equality, "typed_nonfull_representation_disposition": 1 - equality, "typed_global_support_ledger": 1},
        "strict_nonpromotion": {"member_identity": 0, "DSU_edge": 0, "DSU_union": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
    }
    return {**body, "row_sha256": object_hash(body)}


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": count, "size": path.stat().st_size, "sha256": sha256_file(path), "row_sequence_sha256": sequence, "order": order}


def verify(candidate: Path) -> dict[str, Any]:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    preliminary, _ = checked_result(candidate / RESULT)
    require(preliminary.get("schema") == "cm2.round306c25.source-g-502204-member-549616-representation-typed-global-support-ledger.v1", "preflight schema")
    require(preliminary.get("status") == "PASS_502204_MEMBER_TYPED_GLOBAL_SUPPORT_AND_549616_REPRESENTATION_SEMANTIC_LEDGER_SEALED__B1A_REPLAY_AUTHORIZED", "preflight status")
    require(preliminary.get("corrected_universe_census") == {"members": 502204, "representations": 549616, "authorized_base_roots": 339036, "fresh_components": 57876, "cross_component_pair_denominator": 125616475670}, "preflight universe")
    require(preliminary.get("member_support_source_census") == MEMBER_SOURCES, "preflight member sources")
    require(preliminary.get("representation_semantic_source_census") == REPRESENTATION_SOURCES, "preflight representation sources")
    require(preliminary.get("global_credit") == {"typed_member_identity_and_fresh_DSU_binding": 502204, "member_normalized_support_set_equality": 502204, "typed_representation_identity_owner_binding": 549616, "typed_representation_semantic_disposition": 549616, "representation_set_equality": 538680, "typed_nonfull_representation_disposition": 10936, "typed_global_support_ledger": 1}, "preflight credit")
    require(preliminary.get("strict_nonpromotion") == {"new_DSU_edges": 0, "new_DSU_unions": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"}, "preflight boundary")
    result_objects, pins = seal_sources()
    member_index, representation_index, member_source_census, representation_source_census = rebuild_indexes()
    owner_supports = dict(member_index)
    c15_rows = checked_rows(ROOT / C15_MEMBER)
    c16_members = checked_rows(ROOT / C16_MEMBER)
    candidate_members = checked_rows(candidate / MEMBER_LEDGER)
    member_sequence = hashlib.sha256()
    member_families: Counter[str] = Counter()
    components: set[str] = set()
    roots: set[str] = set()
    for ordinal in range(502204):
        c15 = next(c15_rows, None)
        c16 = next(c16_members, None)
        actual = next(candidate_members, None)
        require(c15 is not None and c16 is not None and actual is not None, "member replay length")
        expected = expected_member(ordinal, c15, c16, member_index.pop(c16["member_id"]), result_objects)
        require(actual == expected, "member full reconstruction:" + str(ordinal))
        member_sequence.update(bytes.fromhex(actual["row_sha256"]))
        member_families[actual["coarse_family"]] += 1
        components.add(actual["fresh_component_id"])
        roots.add(actual["base_root_id"])
    require(next(c15_rows, None) is None and next(c16_members, None) is None and next(candidate_members, None) is None and not member_index, "member exhaustion")
    c16_representations = checked_rows(ROOT / C16_REPRESENTATION)
    candidate_representations = checked_rows(candidate / REPRESENTATION_LEDGER)
    representation_sequence = hashlib.sha256()
    representation_families: Counter[str] = Counter()
    semantic_census: Counter[str] = Counter()
    for ordinal in range(549616):
        c16 = next(c16_representations, None)
        actual = next(candidate_representations, None)
        require(c16 is not None and actual is not None, "representation replay length")
        source = representation_index.pop(c16["representation_id"])
        expected = expected_representation(ordinal, c16, source, owner_supports[source[0]], result_objects)
        require(actual == expected, "representation full reconstruction:" + str(ordinal))
        representation_sequence.update(bytes.fromhex(actual["row_sha256"]))
        representation_families[actual["coarse_family"]] += 1
        semantic_census[actual["representation_semantic_kind"]] += 1
    require(next(c16_representations, None) is None and next(candidate_representations, None) is None and not representation_index, "representation exhaustion")
    require(dict(member_families) == MEMBER_FAMILIES and len(components) == 57876 and len(roots) == 339036, "member census")
    require(dict(representation_families) == REPRESENTATION_FAMILIES, "representation family census")
    require(dict(semantic_census) == {"REPRESENTATION_SET_EQUALITY": 538680, "TYPED_NONFULL_REPRESENTATION_DISPOSITION": 2520, "EXACT_SUBCOVER_INCLUSION_DISPOSITION": 8416}, "representation semantic census")
    result, claimed = checked_result(candidate / RESULT)
    member_descriptor = descriptor(candidate / MEMBER_LEDGER, 502204, member_sequence.hexdigest(), "C16A_MEMBER_IDENTITY_FAMILY_LEDGER_ORDER")
    representation_descriptor = descriptor(candidate / REPRESENTATION_LEDGER, 549616, representation_sequence.hexdigest(), "C16A_REPRESENTATION_LEDGER_ORDER")
    body = {
        "schema": "cm2.round306c25.source-g-502204-member-549616-representation-typed-global-support-ledger.v1",
        "status": "PASS_502204_MEMBER_TYPED_GLOBAL_SUPPORT_AND_549616_REPRESENTATION_SEMANTIC_LEDGER_SEALED__B1A_REPLAY_AUTHORIZED",
        "corrected_universe_census": {"members": 502204, "representations": 549616, "authorized_base_roots": 339036, "fresh_components": 57876, "cross_component_pair_denominator": 125616475670},
        "member_family_census": dict(member_families),
        "representation_family_census": dict(representation_families),
        "member_support_source_census": dict(member_source_census),
        "representation_semantic_source_census": dict(representation_source_census),
        "representation_semantic_census": dict(semantic_census),
        "global_credit": {"typed_member_identity_and_fresh_DSU_binding": 502204, "member_normalized_support_set_equality": 502204, "typed_representation_identity_owner_binding": 549616, "typed_representation_semantic_disposition": 549616, "representation_set_equality": 538680, "typed_nonfull_representation_disposition": 10936, "typed_global_support_ledger": 1},
        "anti_join_census": {"member_support_missing": 0, "member_support_duplicate": 0, "representation_semantic_missing": 0, "representation_semantic_duplicate": 0, "representation_owner_missing": 0, "binding_mismatch": 0},
        "ledgers": {"member": member_descriptor, "representation": representation_descriptor},
        "input_pins": pins,
        "strict_nonpromotion": {"new_DSU_edges": 0, "new_DSU_unions": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "REPLAY_CORRECTED_B1A_FEATURE_DEFINITION_DEPENDENCY_AND_TRANSITION_READY_COVER_ON_C25",
    }
    expected_result = {**body, "result_sha256": object_hash(body)}
    require(result == expected_result and claimed == expected_result["result_sha256"], "result full reconstruction")
    return {"status": "PASS_INDEPENDENT_C25_1051820_ROW_FULL_RECONSTRUCTION__CORRECTED_B1A_REPLAY_AUTHORIZED", "result_sha256": claimed, "member_rows": 502204, "representation_rows": 549616, "total_rows": 1051820}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir")
    args = parser.parse_args()
    candidate = ROOT if args.candidate_dir is None else Path(args.candidate_dir).resolve()
    print(wire(verify(candidate)).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
