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

PACKAGE_SPECS = (
    ("C15", C15_BASE, ((C15_MEMBER, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),), "851d047d92b8ded8949e6182837ac93fc390aabb9bc7b325aba7ea14889dc333", "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4", "99ad5fb9f2f940155effdcb24ac076824f6436f2d92a66bd6d9ed196d0ac8f71"),
    ("C16A", C16_BASE, ((C16_MEMBER, "0686f987c6f7ab2ef247914fba45c94663f73fe7dcefc3bdb2ecbe43ea89166a"), (C16_REPRESENTATION, "47cc45de91a9d42be3d6b982cc044b39445d9db3682a8a9390be1ca9d1ffdfc1")), "85e692b6e6889ab8fe3c74ede8e11d48aae664988ed93da7a139d3d9137599f8", "597a9a402190989baa72f0e7955be376b3142850695096e2fdc6d651ce3ce7f4", "46150e0b5331b1f7c3a4591ad9072e6e987746944af6aa4ac0526c06322f8e44"),
    ("C19A", "cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel", (("cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz", "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3"),), "b6cc66d793dccfa90176f130c7fd2842326535cf53480f03229a236327d65f37", "c6d6a004aaa49c1e98223934afd325c23220ce0ce44f408b3f1c07c995791502", "dc2ebd8ca4b375d72086643b59325468811f436ce89320db59ce5c9207374f58"),
    ("C19B", "cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel", (("cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz", "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798"),), "71a3e11c0e6291e7e147fa77747cf29970ef1e4548768ea1114e75ccfda184bd", "82fdf7d81f79727d326dcd6b92fe6c5d02228504047232a430c6e30767fb0bdf", "0139af153531fa482181431a04022b9cf89efc1393c75c29b7e3767fa73e13f6"),
    ("C19C", "cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel", (("cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz", "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84"),), "65151daf86e3e4edafc98a7b091f3a7fa494b1b167792b224518d7afd0cca1d1", "021ae36b83178ee49c6e8bdf9b32b1a139660752c82aec311eebf2b7d5a10a92", "3482ebe2e9adfe9d6aa15236c689d9e81009c554022cd1269bcad28cb216308f"),
    ("C19D", "cm2_round306c19d_source_g_4432_retained_outer_envelope_sheet_support_kernel", (("cm2_round306c19d_source_g_4432_retained_outer_envelope_sheet_support_kernel_ledger.jsonl.gz", "23cf730404d3f405ad202ddedb475ae32b65a7abefa8a338cf6071c4b58eaa5c"),), "b491b7860aa38f94a9c3829e4f1e40858bc651a55c9e7fa840a2523ff04db5a9", "9dee4ba6e95d12716f58dd66927591562fb33f1e6f6166c801399f2282325602", "e85db00615e9719d3e8e7d4deea5fc25e945c3d8a141c3af02cc2817e7bbcbf3"),
    ("C20A", "cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel", (("cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz", "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"),), "f025b632f27eaab2cb8ecaeb47392f67ddfdfe883a0f9ff495d5540f1b073b2a", "124771a897a37b0a6dffb933eaf9e9852c405514b584d16ba50e32ca5bb91158", "a1247449093af5695c11934911080f0c346c75d30647bbba7379bf18cfaf300e"),
    ("C20B", "cm2_round306c20b_source_g_36680_preserved_exact_equal_alias_support_kernel", (("cm2_round306c20b_source_g_36680_preserved_exact_equal_alias_support_kernel_ledger.jsonl.gz", "6c6e27516497da4a30cb8d11b0825221d8ceac5ca36c182f486c0db22a51d0ef"),), "bdc7f1814caa1edb70383ac622373129480118ec533dce8ea02e5c8d7db93a75", "a8919465e5252eba0d0c94a0831d8d3f94f040949caafb590c5c201ba3cd0a03", "e374987445c787050460be177b638dd7601401b45ddd1f15b0ba5ed58c67fd61"),
    ("C20C", "cm2_round306c20c_source_g_76_fixed_sign_t2ps_exact_alias_support_kernel", (("cm2_round306c20c_source_g_76_fixed_sign_t2ps_exact_alias_support_kernel_ledger.jsonl.gz", "6acf090a2dd5d88a120b02b4dd5d32f6c64b0d9ff570a10373d83fdabdcedf32"),), "cf5e3636ebcb640a94b45bc8b34affb8b9cf655b2a364f5849bbb613c112811a", "2849273cc639dee4cd776b0286bc2a8057dc9e49ca84b4892ed40dcd84455ef8", "2b8c5bb80aa4165e166c2daa2bde665be6df2e7cc4c5b57c17cae893d921fa97"),
    ("C20D", "cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel", (("cm2_round306c20d_source_g_2520_preserved_nonfull_alias_negative_disposition_kernel_ledger.jsonl.gz", "0b3177691d8822a6cad5a73650f612980ee2999ba7b646783604ef084b5c6078"),), "f0c765559d947f3d716ebc10969ad96e018eeb7c1682af2df34f68746da87762", "e73ee2690a41c18a6110dc920eecb26c13766b26a814ea6fb38ad70a310ce0a8", "946bf9772c39efb6c9a39a8b518e8e830b96f42e429b6c629c53c031260451ab"),
    ("C22B", "cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel", (("cm2_round306c22b_source_g_295336_r2_member_union_and_302624_representation_semantic_kernel_ledger.jsonl.gz", "c0f3d3a9fc6002f0af23271f7483aeff7eac0b0cc92399fc3785b0a5b9291f97"),), "218a64732da853bf426f4882c84633f8421511a3490b2f0b830bed5484d83506", "cd6ed594efe7cd24ddc5e267c564ad650f48f3289e06da658337743a1469399e", "2cde2eadbd150d5ff2cd6cb9412196228820bb77fea466e665a994f3fc08e55f"),
    ("C23B", "cm2_round306c23b_source_g_9404_r292_component_union_and_10252_representation_semantic_kernel", (("cm2_round306c23b_source_g_9404_r292_component_union_and_10252_representation_semantic_kernel_ledger.jsonl.gz", "ab313cb8cd2f272af62e316ecde1c068f0830e420b12009e21b850745125ab5b"),), "22eade6a1f152c4576d0f60d3515901e73b8fa6e7dae7a9a7bd4869b987da8a3", "a9d8ecb93d719320894ef2520b697a67ef710a7c45339a72cc3f419461c802cf", "b7b4878f0e809417bed3be52c2ad0ca8949f24a51aeacb92408b83410e6903f3"),
    ("C24A", "cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel", (("cm2_round306c24a_source_g_15224_relation_backed_graph_family_support_and_representation_kernel_ledger.jsonl.gz", "ef3554ecb7b38fa689a1dbd21d2d4d7eb0b68b5f5e2f794034d895b8afe6ef58"),), "23d0b07fd34a3c231e85c734e6f159725abeb0a9f2cd1f7c86cb92de891761f2", "2e17d522cef9a32a971c28a7d0e6aaeab97e66da367fedf92c2bb6b418aaeacb", "c9cd71af703705ccf4862cb43052a80e55031c7e3226f2de9cba3b6668ea6107"),
    ("C24B", "cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel", (("cm2_round306c24b_source_g_168_negative_nonincidence_empty_support_and_representation_kernel_ledger.jsonl.gz", "788f16cf6c8e67cdd5c1f3bcdb89e6cde00047bda19531a9a42c56339a31e380"),), "0fec5aa198e94f3f06e24006c628eb5b5b66952106097c2c80e2190b2a80818e", "9a5b8dea2ed9093070c4434bbac7af9169691d02c2c5315974f597b6927b3d13", "9409bbf8f4f75b20d10ea468822af1b171b2dc96f186e0c9a3f88666f3a1ef62"),
)

FAMILY_COUNTS = {"PRESERVED": 126468, "NON_GRAPH": 55604, "R2": 295336, "R292": 9404, "G2A": 5264, "G2B": 10128}
REPRESENTATION_FAMILY_COUNTS = {"PRESERVED": 165744, "NON_GRAPH": 55604, "R2": 302624, "R292": 10252, "G2A": 5264, "G2B": 10128}
MEMBER_SOURCE_COUNTS = {"C19A": 5596, "C19B": 12232, "C19C": 33344, "C19D": 4432, "C20A": 126468, "C22B": 295336, "C23B": 9404, "C24A": 15224, "C24B": 168}
REPRESENTATION_SOURCE_COUNTS = {"C19A": 5596, "C19B": 12232, "C19C": 33344, "C19D": 4432, "C20A": 126468, "C20B": 36680, "C20C": 76, "C20D": 2520, "C22B": 302624, "C23B": 10252, "C24A": 15224, "C24B": 168}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1048576):
            state.update(block)
    return state.hexdigest()


def check_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label)


def check_result(result: dict[str, Any], label: str) -> str:
    body = dict(result)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label)
    return claimed


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for line in stream:
            need(line.endswith(b"\n"), "source newline:" + path.name)
            raw = line[:-1]
            row = json.loads(raw)
            need(canonical(row) == raw, "source canonical:" + path.name)
            check_row(row, "source row closure:" + path.name)
            yield row


def manifest_map(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in path.read_text().splitlines():
        parts = line.split(None, 1)
        need(len(parts) == 2, "manifest line:" + path.name)
        output[Path(parts[1].strip()).name] = parts[0]
    return output


def verification_pass(value: dict[str, Any]) -> None:
    direct = value.get("status", "")
    nested = value.get("independent_verifier", {}).get("status", "")
    need((type(direct) is str and direct.startswith("PASS")) or (type(nested) is str and nested.startswith("PASS")), "source verification")


def input_pins() -> list[dict[str, str]]:
    pins: list[dict[str, str]] = []
    for _, base, ledgers, result_hash, manifest_hash, _ in PACKAGE_SPECS:
        pins.extend({"filename": name, "sha256": sha256} for name, sha256 in ledgers)
        pins.append({"filename": base + "_result.json", "sha256": result_hash})
        pins.append({"filename": base + "_manifest.sha256", "sha256": manifest_hash})
    return sorted(pins, key=lambda row: row["filename"])


def validate_sources() -> dict[str, str]:
    result_objects: dict[str, str] = {}
    for tag, base, ledgers, result_hash, manifest_hash, expected_object in PACKAGE_SPECS:
        result_name = base + "_result.json"
        verification_name = base + "_verification.json"
        manifest_name = base + "_manifest.sha256"
        need(file_hash(ROOT / result_name) == result_hash, "result pin:" + tag)
        need(file_hash(ROOT / manifest_name) == manifest_hash, "manifest pin:" + tag)
        listed = manifest_map(ROOT / manifest_name)
        for name, sha256 in ledgers:
            need(file_hash(ROOT / name) == sha256, "ledger pin:" + tag)
            need(listed.get(name) == sha256, "manifest ledger:" + tag)
        need(listed.get(result_name) == result_hash, "manifest result:" + tag)
        need(verification_name in listed and file_hash(ROOT / verification_name) == listed[verification_name], "manifest verification:" + tag)
        result = json.loads((ROOT / result_name).read_bytes())
        claimed = check_result(result, "result closure:" + tag)
        need(claimed == expected_object and result.get("status", "").startswith("PASS"), "result object:" + tag)
        verification_pass(json.loads((ROOT / verification_name).read_bytes()))
        result_objects[tag] = claimed
    c15 = json.loads((ROOT / (C15_BASE + "_result.json")).read_bytes())
    c16 = json.loads((ROOT / (C16_BASE + "_result.json")).read_bytes())
    c24b = json.loads((ROOT / (PACKAGE_SPECS[-1][1] + "_result.json")).read_bytes())
    need(c15["fresh_universe_census"] == {"base_roots": 339036, "members": 502204, "new_C14c_members": 4432, "old_C6_members": 497772}, "C15 universe")
    need(c15["fresh_DSU_census"]["components"] == 57876 and c15["fresh_DSU_census"]["cross_component_pair_denominator"] == 125616475670, "C15 partition")
    need(c16["member_census"]["family_counts"] == FAMILY_COUNTS and c16["representation_census"]["family_counts"] == REPRESENTATION_FAMILY_COUNTS, "C16 census")
    need(c24b["cumulative_global_member_support_credit"] == 502204 and c24b["remaining_global_member_support_debt"] == 0, "C24b boundary")
    return result_objects


def package_ledger(tag: str) -> str:
    for current, _, ledgers, _, _, _ in PACKAGE_SPECS:
        if current == tag:
            need(len(ledgers) == 1, "single family ledger:" + tag)
            return ledgers[0][0]
    raise Failure("unknown package:" + tag)


def source_indexes() -> tuple[dict[str, tuple[Any, ...]], dict[str, tuple[Any, ...]], Counter[str], Counter[str]]:
    members: dict[str, tuple[Any, ...]] = {}
    representations: dict[str, tuple[Any, ...]] = {}
    member_counts: Counter[str] = Counter()
    representation_counts: Counter[str] = Counter()

    def add_member(member_id: str, family: str, tag: str, row: dict[str, Any], support_sha256: str, certificate_sha256: str, semantic_kind: str) -> None:
        need(member_id not in members, "duplicate member support:" + member_id)
        members[member_id] = (family, tag, row["row_sha256"], support_sha256, certificate_sha256, semantic_kind, row.get("fresh_component_id"), row.get("base_root_id"), row.get("official_key_id"))
        member_counts[tag] += 1

    def add_representation(representation_id: str, owner_member_id: str, family: str, tag: str, row: dict[str, Any], semantic_kind: str, set_equality: int, certificate_sha256: str, claimed_owner_support_sha256: str | None = None) -> None:
        need(representation_id not in representations, "duplicate representation semantic:" + representation_id)
        representations[representation_id] = (owner_member_id, family, tag, row["row_sha256"], semantic_kind, set_equality, certificate_sha256, claimed_owner_support_sha256, row.get("fresh_component_id"))
        representation_counts[tag] += 1

    for tag in ("C19A", "C19B", "C19C", "C19D"):
        for row in rows(ROOT / package_ledger(tag)):
            certificate_sha256 = digest(row["construction_certificate"])
            add_member(row["member_id"], "NON_GRAPH", tag, row, row["support_ast_sha256"], certificate_sha256, "EXACT_MEMBER_SUPPORT_EQUALITY")
            add_representation(row["representation_id"], row["member_id"], "NON_GRAPH", tag, row, "REPRESENTATION_SET_EQUALITY", 1, certificate_sha256, row["support_ast_sha256"])

    for row in rows(ROOT / package_ledger("C20A")):
        certificate_sha256 = digest(row["construction_certificate"])
        add_member(row["member_id"], "PRESERVED", "C20A", row, row["support_ast_sha256"], certificate_sha256, "EXACT_MEMBER_SUPPORT_EQUALITY")
        add_representation(row["representation_id"], row["member_id"], "PRESERVED", "C20A", row, "REPRESENTATION_SET_EQUALITY", 1, certificate_sha256, row["support_ast_sha256"])

    for row in rows(ROOT / package_ledger("C20B")):
        add_representation(row["representation_id"], row["owner_member_id"], "PRESERVED", "C20B", row, "REPRESENTATION_SET_EQUALITY", 1, digest(row["set_equality_certificate"]), row["representation_support_ast_sha256"])

    for row in rows(ROOT / package_ledger("C20C")):
        add_representation(row["representation_id"], row["owner_member_id"], "PRESERVED", "C20C", row, "REPRESENTATION_SET_EQUALITY", 1, row["T2PS_bijection_theorem_sha256"], row["owner_support_ast_sha256"])

    for row in rows(ROOT / package_ledger("C20D")):
        add_representation(row["representation_id"], row["owner_member_id"], "PRESERVED", "C20D", row, "TYPED_NONFULL_REPRESENTATION_DISPOSITION", 0, digest(row["negative_disposition"]), row["owner_support_ast_sha256"])

    for row in rows(ROOT / package_ledger("C22B")):
        if row["row_kind"] == "R2_PRIMARY_MEMBER_NORMALIZED_SUPPORT_AND_REPRESENTATION_SET_EQUALITY":
            add_member(row["member_id"], "R2", "C22B", row, row["normalized_support_ast_sha256"], row["member_union_theorem_ast_sha256"], "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY")
            add_representation(row["representation_id"], row["member_id"], "R2", "C22B", row, "REPRESENTATION_SET_EQUALITY", 1, row["member_union_theorem_ast_sha256"], row["normalized_support_ast_sha256"])
        else:
            need(row["row_kind"] == "R2_R287_ALIAS_EXACT_SUBCOVER_INCLUSION_DISPOSITION", "C22b row kind")
            add_representation(row["representation_id"], row["member_id"], "R2", "C22B", row, "EXACT_SUBCOVER_INCLUSION_DISPOSITION", 0, row["subcover_theorem_ast_sha256"])

    for row in rows(ROOT / package_ledger("C23B")):
        if row["row_kind"] == "R292_MEMBER_NORMALIZED_SUPPORT_SET_EQUALITY":
            add_member(row["member_id"], "R292", "C23B", row, row["normalized_support_ast_sha256"], row["member_union_theorem_ast_sha256"], "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY")
        else:
            need(row["row_kind"] in {"R292_SINGLE_CELL_REPRESENTATION_SET_EQUALITY", "R292_COMPONENT_CELL_EXACT_SUBCOVER_INCLUSION_DISPOSITION"}, "C23b row kind")
            set_equality = int(row["formal_credit"]["representation_set_equality"])
            semantic_kind = "REPRESENTATION_SET_EQUALITY" if set_equality else "EXACT_SUBCOVER_INCLUSION_DISPOSITION"
            add_representation(row["representation_id"], row["member_id"], "R292", "C23B", row, semantic_kind, set_equality, row["representation_theorem_ast_sha256"])

    for row in rows(ROOT / package_ledger("C24A")):
        family = row["coarse_family"]
        add_member(row["member_id"], family, "C24A", row, row["normalized_support_ast_sha256"], row["semantic_theorem_ast_sha256"], "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY")
        add_representation(row["canonical_representation_id"], row["member_id"], family, "C24A", row, "REPRESENTATION_SET_EQUALITY", 1, row["semantic_theorem_ast_sha256"], row["normalized_support_ast_sha256"])

    for row in rows(ROOT / package_ledger("C24B")):
        add_member(row["member_id"], "G2B", "C24B", row, row["normalized_support_ast_sha256"], row["semantic_theorem_ast_sha256"], "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY")
        add_representation(row["sole_registered_representation_id"], row["member_id"], "G2B", "C24B", row, "REPRESENTATION_SET_EQUALITY", 1, row["semantic_theorem_ast_sha256"], row["normalized_support_ast_sha256"])

    need(len(members) == 502204 and dict(member_counts) == MEMBER_SOURCE_COUNTS, "member source census")
    need(len(representations) == 549616 and dict(representation_counts) == REPRESENTATION_SOURCE_COUNTS, "representation source census")
    for representation_id, source in representations.items():
        owner_member_id, family, _, _, _, _, _, claimed_owner_support_sha256, _ = source
        need(owner_member_id in members, "representation owner gap:" + representation_id)
        owner = members[owner_member_id]
        need(owner[0] == family, "representation family mismatch:" + representation_id)
        if claimed_owner_support_sha256 is not None:
            need(claimed_owner_support_sha256 == owner[3], "owner support mismatch:" + representation_id)
    return members, representations, member_counts, representation_counts


def write_gzip_rows(path: Path, iterator: Iterator[dict[str, Any]]) -> tuple[int, str]:
    sequence = hashlib.sha256()
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as output:
            for row in iterator:
                output.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    return count, sequence.hexdigest()


def member_output_rows(members: dict[str, tuple[Any, ...]], result_objects: dict[str, str], census: Counter[str], components: set[str], roots: set[str]) -> Iterator[dict[str, Any]]:
    c15_iterator = rows(ROOT / C15_MEMBER)
    c16_iterator = rows(ROOT / C16_MEMBER)
    for ordinal in range(502204):
        c15 = next(c15_iterator, None)
        c16 = next(c16_iterator, None)
        need(c15 is not None and c16 is not None, "member source length")
        member_id = c16["member_id"]
        need((c15["member_ordinal"], c16["member_ordinal"]) == (ordinal, ordinal), "member ordinal")
        need(c15["registry_member_id"] == member_id, "C15/C16 member join")
        need((c15["fresh_component_id"], c15["base_root_id"], c15["official_key_id"]) == (c16["fresh_component_id"], c16["base_root_id"], c16["official_key_id"]), "C15/C16 binding")
        need(c16["C15_member_ref"][0] == ordinal and c16["C15_member_ref"][1] == c15["row_id"] and c16["C15_member_ref"][3] == c15["row_sha256"], "C16 C15 ref")
        family, tag, source_row_sha256, support_sha256, certificate_sha256, semantic_kind, source_component, source_root, source_key = members.pop(member_id)
        need(family == c16["coarse_family"], "member family")
        need(source_component is None or source_component == c16["fresh_component_id"], "member source component")
        need(source_root is None or source_root == c16["base_root_id"], "member source root")
        need(source_key is None or source_key == c16["official_key_id"], "member source key")
        census[family] += 1
        components.add(c16["fresh_component_id"])
        roots.add(c16["base_root_id"])
        row_id = PREFIX + ":member:" + hashlib.sha256(member_id.encode("ascii")).hexdigest()
        body = {
            "schema": "cm2.round306c25.source-g-typed-global-support-ledger.v1.member-row.v1",
            "member_ordinal": ordinal,
            "row_id": row_id,
            "member_id": member_id,
            "coarse_family": family,
            "fresh_component_id": c16["fresh_component_id"],
            "base_root_id": c16["base_root_id"],
            "official_key_id": c16["official_key_id"],
            "normalized_support_ast_sha256": support_sha256,
            "support_semantic_kind": semantic_kind,
            "support_semantic_certificate_sha256": certificate_sha256,
            "source_bindings": {
                "C15_member_row_sha256": c15["row_sha256"],
                "C16a_member_row_sha256": c16["row_sha256"],
                "support_kernel": tag,
                "support_kernel_ledger": package_ledger(tag),
                "support_kernel_row_sha256": source_row_sha256,
                "support_kernel_result_sha256": result_objects[tag],
            },
            "formal_credit": {"fresh_DSU_member_binding": 1, "typed_member_identity": 1, "member_normalized_support_set_equality": 1, "typed_global_support_ledger": 1},
            "strict_nonpromotion": {"B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
        }
        yield {**body, "row_sha256": digest(body)}
    need(next(c15_iterator, None) is None and next(c16_iterator, None) is None and not members, "member exhaustion")


def representation_output_rows(representations: dict[str, tuple[Any, ...]], member_supports: dict[str, tuple[Any, ...]], result_objects: dict[str, str], family_census: Counter[str], semantic_census: Counter[str]) -> Iterator[dict[str, Any]]:
    c16_iterator = rows(ROOT / C16_REPRESENTATION)
    for ordinal in range(549616):
        c16 = next(c16_iterator, None)
        need(c16 is not None and c16["representation_ordinal"] == ordinal, "representation ordinal")
        representation_id = c16["representation_id"]
        owner_member_id, family, tag, source_row_sha256, semantic_kind, set_equality, certificate_sha256, _, source_component = representations.pop(representation_id)
        need((owner_member_id, family) == (c16["owner_member_id"], c16["coarse_family"]), "representation owner/family")
        need(source_component is None or source_component == c16["fresh_component_id"], "representation source component")
        owner_support = member_supports[owner_member_id]
        need(owner_support[0] == family, "owner support family")
        family_census[family] += 1
        semantic_census[semantic_kind] += 1
        row_id = PREFIX + ":representation:" + hashlib.sha256(representation_id.encode("ascii")).hexdigest()
        body = {
            "schema": "cm2.round306c25.source-g-typed-global-support-ledger.v1.representation-row.v1",
            "representation_ordinal": ordinal,
            "row_id": row_id,
            "representation_id": representation_id,
            "owner_member_id": owner_member_id,
            "coarse_family": family,
            "fresh_component_id": c16["fresh_component_id"],
            "base_root_id": c16["base_root_id"],
            "official_key_id": c16["official_key_id"],
            "owner_normalized_support_ast_sha256": owner_support[3],
            "representation_semantic_kind": semantic_kind,
            "representation_semantic_certificate_sha256": certificate_sha256,
            "source_bindings": {
                "C16a_representation_row_sha256": c16["row_sha256"],
                "semantic_kernel": tag,
                "semantic_kernel_ledger": package_ledger(tag),
                "semantic_kernel_row_sha256": source_row_sha256,
                "semantic_kernel_result_sha256": result_objects[tag],
            },
            "formal_credit": {"typed_representation_identity_owner_binding": 1, "typed_representation_semantic_disposition": 1, "representation_set_equality": set_equality, "typed_nonfull_representation_disposition": 1 - set_equality, "typed_global_support_ledger": 1},
            "strict_nonpromotion": {"member_identity": 0, "DSU_edge": 0, "DSU_union": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": 0},
        }
        yield {**body, "row_sha256": digest(body)}
    need(next(c16_iterator, None) is None and not representations, "representation exhaustion")


def descriptor(path: Path, row_count: int, row_sequence_sha256: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": row_count, "size": path.stat().st_size, "sha256": file_hash(path), "row_sequence_sha256": row_sequence_sha256, "order": order}


def build(candidate: Path) -> dict[str, Any]:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    result_objects = validate_sources()
    members, representations, member_source_census, representation_source_census = source_indexes()
    member_supports = dict(members)
    candidate.mkdir(parents=True, exist_ok=True)
    member_family_census: Counter[str] = Counter()
    components: set[str] = set()
    roots: set[str] = set()
    member_count, member_sequence = write_gzip_rows(candidate / MEMBER_LEDGER, member_output_rows(members, result_objects, member_family_census, components, roots))
    representation_family_census: Counter[str] = Counter()
    representation_semantic_census: Counter[str] = Counter()
    representation_count, representation_sequence = write_gzip_rows(candidate / REPRESENTATION_LEDGER, representation_output_rows(representations, member_supports, result_objects, representation_family_census, representation_semantic_census))
    need(member_count == 502204 and dict(member_family_census) == FAMILY_COUNTS, "global member census")
    need(len(components) == 57876 and len(roots) == 339036, "global partition census")
    need(representation_count == 549616 and dict(representation_family_census) == REPRESENTATION_FAMILY_COUNTS, "global representation census")
    need(dict(representation_semantic_census) == {"REPRESENTATION_SET_EQUALITY": 538680, "TYPED_NONFULL_REPRESENTATION_DISPOSITION": 2520, "EXACT_SUBCOVER_INCLUSION_DISPOSITION": 8416}, "global semantic census")
    member_descriptor = descriptor(candidate / MEMBER_LEDGER, member_count, member_sequence, "C16A_MEMBER_IDENTITY_FAMILY_LEDGER_ORDER")
    representation_descriptor = descriptor(candidate / REPRESENTATION_LEDGER, representation_count, representation_sequence, "C16A_REPRESENTATION_LEDGER_ORDER")
    body = {
        "schema": "cm2.round306c25.source-g-502204-member-549616-representation-typed-global-support-ledger.v1",
        "status": "PASS_502204_MEMBER_TYPED_GLOBAL_SUPPORT_AND_549616_REPRESENTATION_SEMANTIC_LEDGER_SEALED__B1A_REPLAY_AUTHORIZED",
        "corrected_universe_census": {"members": 502204, "representations": 549616, "authorized_base_roots": 339036, "fresh_components": 57876, "cross_component_pair_denominator": 125616475670},
        "member_family_census": dict(member_family_census),
        "representation_family_census": dict(representation_family_census),
        "member_support_source_census": dict(member_source_census),
        "representation_semantic_source_census": dict(representation_source_census),
        "representation_semantic_census": dict(representation_semantic_census),
        "global_credit": {"typed_member_identity_and_fresh_DSU_binding": 502204, "member_normalized_support_set_equality": 502204, "typed_representation_identity_owner_binding": 549616, "typed_representation_semantic_disposition": 549616, "representation_set_equality": 538680, "typed_nonfull_representation_disposition": 10936, "typed_global_support_ledger": 1},
        "anti_join_census": {"member_support_missing": 0, "member_support_duplicate": 0, "representation_semantic_missing": 0, "representation_semantic_duplicate": 0, "representation_owner_missing": 0, "binding_mismatch": 0},
        "ledgers": {"member": member_descriptor, "representation": representation_descriptor},
        "input_pins": input_pins(),
        "strict_nonpromotion": {"new_DSU_edges": 0, "new_DSU_unions": 0, "B1A": 0, "B2": 0, "maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "REPLAY_CORRECTED_B1A_FEATURE_DEFINITION_DEPENDENCY_AND_TRANSITION_READY_COVER_ON_C25",
    }
    result = {**body, "result_sha256": digest(body)}
    (candidate / RESULT).write_bytes(canonical(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve())
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
