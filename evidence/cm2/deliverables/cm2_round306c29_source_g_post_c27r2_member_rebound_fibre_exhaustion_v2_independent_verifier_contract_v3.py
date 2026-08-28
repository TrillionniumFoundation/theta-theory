#!/usr/bin/env python3
"""No-import independent verifier for the append-only C29-v2 candidate.

This file neither imports nor executes the producer.  It independently opens
the two terminal adapters, the pinned C25 ledgers, and every candidate row;
rebuilds the member-id join, component/key incidences, multiplicity, and
representation-owner rebinding; then requires byte-semantic equality with all
four candidate files.  PASS remains conditional and carries zero credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
COMPONENT_LEDGER = PREFIX + "_post_component_official_key_assignment_ledger.jsonl.gz"
FIBRE_LEDGER = PREFIX + "_official_key_fibre_exhaustion_ledger.jsonl.gz"
DISPOSITION_LEDGER = PREFIX + "_global_member_disposition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
OUTPUT_NAMES = {COMPONENT_LEDGER, FIBRE_LEDGER, DISPOSITION_LEDGER, RESULT}

C25_PREFIX = (
    "cm2_round306c25_source_g_502204_member_549616_representation_"
    "typed_global_support_ledger"
)
C25_MEMBER = C25_PREFIX + "_member_ledger.jsonl.gz"
C25_REPRESENTATION = C25_PREFIX + "_representation_ledger.jsonl.gz"
C25_RESULT = C25_PREFIX + "_result.json"
C25_VERIFICATION = C25_PREFIX + "_verification.json"
C25_MANIFEST = C25_PREFIX + "_manifest.sha256"
C25_PINS = {
    C25_MANIFEST: "8885eb09f4e0aef3107654996ef520cca3ce59f59fc5b5d8a1652d44f9bb9a81",
    C25_MEMBER: "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6",
    C25_REPRESENTATION: "3259f665e323cde3d56d8eaf6703744bca795208e733f3ac14663ea4882df45d",
    C25_RESULT: "6f3d46b460b6a03a1a461bbcf7b44dfc389d63a15fa26a6263a6150fc483d701",
    C25_VERIFICATION: "3907d3baa0f26593514422ea69df365f50c3daa2e2190ccf130bfdc1991f238e",
}
C25_RESULT_OBJECT = "ad6b4ae09985f23fd0db00e79bee859014c23c6792aa732582e50aa39c745bef"
C25_MEMBER_SCHEMA = "cm2.round306c25.source-g-typed-global-support-ledger.v1.member-row.v1"
C25_REPRESENTATION_SCHEMA = (
    "cm2.round306c25.source-g-typed-global-support-ledger.v1.representation-row.v1"
)
C27R2_MEMBER_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "member-to-post-component-row.v1"
)
C27R2_CENSUS_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "post-component-census-row.v1"
)
PROJECTION_FILE = "c29_consumer_projection.json"
C27R2_PROJECTION_SCHEMA = "cm2.round306c27r2.c29-consumer-projection.v1"
C28_PROJECTION_SCHEMA = "cm2.round306c28-v2.c29-consumer-projection.v1"
ADAPTER_RECEIPT_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion."
    "v2.terminal-consumer-adapter-receipt.v3"
)
COMPONENT_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
    "post-component-row.v1"
)
FIBRE_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
    "official-key-fibre-row.v1"
)
DISPOSITION_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
    "global-member-disposition-row.v1"
)
RESULT_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
    "producer-result.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
    "independent-verification.v1"
)

MEMBERS = 502_204
REPRESENTATIONS = 549_616
COMPONENTS = 43_684
OFFICIAL_KEYS = 124
TOTAL_PAIRS = 126_104_177_706
WITHIN_PAIRS = 542_179_508
CROSS_PAIRS = 125_561_998_198
FAMILIES = {
    "PRESERVED": 126_468, "NON_GRAPH": 55_604, "R2": 295_336,
    "R292": 9_404, "G2A": 5_264, "G2B": 10_128,
}
SUPPORT_KINDS = {
    "EXACT_MEMBER_SUPPORT_EQUALITY",
    "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY",
    "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY",
    "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY",
}


class Failure(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def object_pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in values:
        require(type(key) is str and key not in result, "duplicate key:" + str(key))
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise Failure("JSON constant:" + value)


def encode(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def string_sequence(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def hash_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1 << 20):
            state.update(chunk)
    return state.hexdigest()


def decode(raw: bytes, label: str, trailing_newline: bool = True) -> Any:
    if trailing_newline:
        require(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
        raw = raw[:-1]
    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=object_pairs,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Failure(label + ":JSON") from error
    require(encode(value) == raw, label + ":canonical")
    return value


def document(
    path: Path, closure: str, trailing_newline: bool = True,
) -> dict[str, Any]:
    value = decode(path.read_bytes(), path.name, trailing_newline)
    require(type(value) is dict, path.name + ":object")
    body = dict(value)
    claimed = body.pop(closure, None)
    require(type(claimed) is str and claimed == object_sha(body), path.name + ":closure")
    return value


def closed_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": object_sha(body)}


def path_in_workspace(text: str) -> Path:
    require(type(text) is str and text != "", "payload path")
    pure = PurePosixPath(text)
    require(not pure.is_absolute() and ".." not in pure.parts and "." not in pure.parts,
            "safe payload path")
    lexical = ROOT.joinpath(*pure.parts)
    actual = lexical.resolve(strict=True)
    require(lexical == actual and actual.is_relative_to(ROOT)
            and actual.is_file() and not actual.is_symlink(), "payload regular file")
    return actual


def directory_in_workspace(text: str, label: str) -> Path:
    lexical = Path(text).absolute()
    actual = lexical.resolve(strict=True)
    require(lexical == actual and actual.is_relative_to(ROOT)
            and actual.is_dir() and not actual.is_symlink(), label)
    return actual


def manifest(path: Path) -> dict[str, str]:
    raw = path.read_bytes()
    require(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), path.name + ":newline")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Failure(path.name + ":ASCII") from error
    result: dict[str, str] = {}
    for line in lines:
        fields = line.split("  ", 1)
        require(len(fields) == 2 and len(fields[0]) == 64
                and all(char in "0123456789abcdef" for char in fields[0]),
                path.name + ":line")
        require(fields[1] != "" and fields[1] not in result,
                path.name + ":unique member")
        result[fields[1]] = fields[0]
    require(len(result) > 0, path.name + ":nonempty")
    return result


def manifest_binds(entries: dict[str, str], path: Path) -> None:
    relative = path.relative_to(ROOT).as_posix()
    options = [relative, path.name]
    present = [name for name in options if name in entries]
    require(len(present) == 1 and entries[present[0]] == hash_file(path),
            "manifest binding:" + relative)


def rows(path: Path, schema: str) -> Iterator[dict[str, Any]]:
    try:
        with gzip.open(path, "rb") as source:
            for ordinal, line in enumerate(source):
                require(line.endswith(b"\n") and not line.endswith(b"\n\n"),
                        path.name + ":newline")
                value = decode(line[:-1], path.name + ":" + str(ordinal), False)
                require(type(value) is dict and value.get("schema") == schema,
                        path.name + ":schema")
                body = dict(value)
                claimed = body.pop("row_sha256", None)
                require(type(claimed) is str and claimed == object_sha(body),
                        path.name + ":closure")
                yield value
    except (gzip.BadGzipFile, EOFError) as error:
        raise Failure(path.name + ":gzip") from error


def terminal(
    text: str, kind: str, root_pin: str, receipt_file_pin: str,
    receipt_object_pin: str,
) -> dict[str, Any]:
    base = directory_in_workspace(text, kind + ":terminal directory")
    root_path = base / "root_manifest.sha256"
    payload_path = base / "payload_manifest.sha256"
    receipt_path = base / "terminal_receipt.json"
    pass_path = base / "PASS.lock"
    projection_path = base / PROJECTION_FILE
    require(all(path.is_file() and not path.is_symlink() for path in (
        root_path, payload_path, receipt_path, pass_path, projection_path,
    )), kind + ":dynamic adapter complete")
    require(all(type(item) is str and len(item) == 64
                and all(char in "0123456789abcdef" for char in item)
                for item in (root_pin, receipt_file_pin, receipt_object_pin)),
            kind + ":external pins")
    require(hash_file(root_path) == root_pin
            and hash_file(receipt_path) == receipt_file_pin,
            kind + ":external file pins")
    root = manifest(root_path)
    require(root == {
        "payload_manifest.sha256": hash_file(payload_path),
        "terminal_receipt.json": receipt_file_pin,
    }, kind + ":root closure")
    payload = manifest(payload_path)
    manifest_binds(payload, projection_path)
    receipt = document(receipt_path, "terminal_receipt_sha256")
    adapter_status = (
        "PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT"
        if kind == "C27R2" else
        "PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT"
    )
    require(receipt["terminal_receipt_sha256"] == receipt_object_pin
            and receipt.get("schema") == ADAPTER_RECEIPT_SCHEMA
            and receipt.get("status") == adapter_status
            and receipt.get("authority_kind") == kind
            and receipt.get("terminal_replay_passed") is True
            and receipt.get("authority_minted") is True
            and receipt.get("formal_credit") == 0,
            kind + ":receipt semantics")
    projection = document(projection_path, "projection_sha256")
    expected_schema = C27R2_PROJECTION_SCHEMA if kind == "C27R2" else C28_PROJECTION_SCHEMA
    expected_status = (
        "PASS_C27R2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"
        if kind == "C27R2" else "PASS_C28_V2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"
    )
    source_pins = (
        projection.get("terminal_root_manifest_sha256"),
        projection.get("terminal_receipt_file_sha256"),
        projection.get("terminal_receipt_object_sha256"),
        projection.get("terminal_replay_file_sha256"),
        projection.get("terminal_replay_object_sha256"),
    )
    require(all(type(item) is str and len(item) == 64
                and all(char in "0123456789abcdef" for char in item)
                for item in source_pins), kind + ":source terminal pins")
    require(projection.get("schema") == expected_schema
            and projection.get("status") == expected_status
            and projection.get("terminal_replay_passed") is True
            and projection.get("authority_minted") is True
            and receipt.get("source_terminal_root_manifest_sha256") == source_pins[0]
            and receipt.get("source_terminal_receipt_file_sha256") == source_pins[1]
            and receipt.get("source_terminal_receipt_object_sha256") == source_pins[2]
            and receipt.get("source_terminal_replay_file_sha256") == source_pins[3]
            and receipt.get("source_terminal_replay_object_sha256") == source_pins[4]
            and receipt.get("source_terminal_status") == projection.get("terminal_status")
            and projection.get("PASS_lock_sha256") == hash_file(pass_path),
            kind + ":projection terminal closure")
    pass_bytes = pass_path.read_bytes()
    expected_pass = (
        b"PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
        if kind == "C27R2" else
        b"PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
    )
    require(pass_bytes == expected_pass, kind + ":PASS lock")
    members = projection.get("payload_members")
    required = (
        {"producer_result", "member_to_post_component", "post_component_census"}
        if kind == "C27R2" else {"producer_result"}
    )
    require(type(members) is dict and set(members) == required,
            kind + ":projection members")
    captures: dict[str, dict[str, Any]] = {}
    for name in sorted(required):
        item = members[name]
        require(type(item) is dict and set(item) >= {"path", "file_sha256"},
                kind + ":descriptor")
        path = path_in_workspace(item["path"])
        require(hash_file(path) == item["file_sha256"], kind + ":payload SHA")
        manifest_binds(payload, path)
        captures[name] = {**item, "path_object": path}
    census = projection.get("exact_census")
    require(type(census) is dict, kind + ":census")
    if kind == "C27R2":
        require(census.get("members") == MEMBERS
                and census.get("post_C27R2_components") == COMPONENTS
                and census.get("within_post_component_member_pairs") == WITHIN_PAIRS
                and census.get("cross_post_component_member_pairs") == CROSS_PAIRS,
                "C27R2:census")
    else:
        require(census.get("post_C27R2_components") == COMPONENTS
                and census.get("cross_post_component_member_pairs") == CROSS_PAIRS
                and projection.get("B2_pair_routing_complete") is True
                and projection.get("component_maximality_complete") is True
                and projection.get("new_legal_cross_component_pairs") == 0
                and projection.get("unresolved_pairs") == 0,
                "C28:B2/maximality")
    return {
        "root": source_pins[0], "receipt_file": source_pins[1],
        "receipt_object": source_pins[2],
        "replay_file": source_pins[3], "replay_object": source_pins[4],
        "adapter_root": root_pin, "adapter_receipt_file": receipt_file_pin,
        "adapter_receipt_object": receipt_object_pin,
        "projection_object": projection["projection_sha256"],
        "projection": projection, "members": captures,
    }


def c25_authority() -> dict[str, Any]:
    base = ROOT / "deliverables"
    for name, expected in C25_PINS.items():
        path = base / name
        require(path.is_file() and not path.is_symlink()
                and hash_file(path) == expected, "C25 pin:" + name)
    listed = manifest(base / C25_MANIFEST)
    for name in (C25_MEMBER, C25_REPRESENTATION, C25_RESULT, C25_VERIFICATION):
        require(listed.get(name) == C25_PINS[name], "C25 manifest:" + name)
    result = document(base / C25_RESULT, "result_sha256", False)
    verification = decode((base / C25_VERIFICATION).read_bytes(), C25_VERIFICATION)
    require(result["result_sha256"] == C25_RESULT_OBJECT
            and result.get("global_credit", {}).get(
                "member_normalized_support_set_equality") == MEMBERS
            and result.get("global_credit", {}).get(
                "typed_representation_semantic_disposition") == REPRESENTATIONS,
            "C25 result semantics")
    require(type(verification) is dict
            and verification.get("result_object_sha256") == C25_RESULT_OBJECT
            and str(verification.get("status", "")).startswith("PASS_"),
            "C25 verification")
    return {
        "member": base / C25_MEMBER,
        "representation": base / C25_REPRESENTATION,
        "result_object": C25_RESULT_OBJECT,
        "manifest": C25_PINS[C25_MANIFEST],
    }


def source_result(authority: dict[str, Any], label: str) -> dict[str, Any]:
    member = authority["members"]["producer_result"]
    value = document(member["path_object"], "result_sha256")
    require(member.get("object_sha256") == value["result_sha256"],
            label + ":result object")
    return value


def match_descriptor(path: Path, value: Any, count: int) -> None:
    require(type(value) is dict and value.get("filename") == path.name
            and value.get("sha256") == hash_file(path)
            and value.get("row_count") == count, "source ledger descriptor")


def fresh_accumulator() -> dict[str, Any]:
    return {
        "members": 0, "representations": 0,
        "keys": Counter(), "families": Counter(),
        "old": set(), "post": set(),
        "member_sequence": hashlib.sha256(),
        "support_sequence": hashlib.sha256(),
        "representation_sequence": hashlib.sha256(),
        "semantic_sequence": hashlib.sha256(),
    }


def rebuild(c27: dict[str, Any], c25: dict[str, Any]) -> dict[str, Any]:
    member_path = c27["members"]["member_to_post_component"]["path_object"]
    census_path = c27["members"]["post_component_census"]["path_object"]
    c27_result = source_result(c27, "C27R2")
    ledgers = c27_result.get("ledgers")
    require(type(ledgers) is dict, "C27R2 result ledgers")
    match_descriptor(member_path, ledgers.get("member_to_post_component"), MEMBERS)
    match_descriptor(census_path, ledgers.get("post_component_census"), COMPONENTS)

    binding: dict[str, tuple[str, str, str]] = {}
    comps: dict[str, dict[str, Any]] = defaultdict(fresh_accumulator)
    fibres: dict[str, dict[str, Any]] = defaultdict(fresh_accumulator)
    families: Counter[str] = Counter()
    count = 0
    for ordinal, (quotient, support) in enumerate(zip(
        rows(member_path, C27R2_MEMBER_SCHEMA),
        rows(c25["member"], C25_MEMBER_SCHEMA), strict=True,
    )):
        require(quotient.get("ordinal") == ordinal
                and quotient.get("member_ordinal") == ordinal
                and support.get("member_ordinal") == ordinal,
                "member ordinal")
        member = support.get("member_id")
        old = support.get("fresh_component_id")
        post = quotient.get("post_C27R2_component_id")
        key = support.get("official_key_id")
        family = support.get("coarse_family")
        require(type(member) is str and member not in binding
                and quotient.get("registry_member_id") == member
                and quotient.get("old_C15_component_id") == old,
                "member-id/historical-component join")
        require(type(post) is str
                and post.startswith("round306c27r2-source-g-post-component:")
                and type(key) is str and type(family) is str
                and support.get("support_semantic_kind") in SUPPORT_KINDS,
                "joined member semantics")
        binding[member] = (post, old, key)
        comp = comps[post]
        fibre = fibres[key]
        for target in (comp, fibre):
            target["members"] += 1
            target["keys"][key] += 1
            target["families"][family] += 1
            target["old"].add(old)
            target["post"].add(post)
            target["member_sequence"].update(member.encode("ascii") + b"\n")
            target["support_sequence"].update(bytes.fromhex(
                support["support_semantic_certificate_sha256"]))
        families[family] += 1
        count += 1
    require(count == MEMBERS and len(binding) == MEMBERS
            and dict(families) == FAMILIES, "member/family exhaustion")

    representations: set[str] = set()
    for ordinal, row in enumerate(rows(c25["representation"], C25_REPRESENTATION_SCHEMA)):
        require(row.get("representation_ordinal") == ordinal,
                "representation ordinal")
        owner = row.get("owner_member_id")
        require(type(owner) is str and owner in binding,
                "representation owner join")
        post, old, key = binding[owner]
        require(row.get("fresh_component_id") == old
                and row.get("official_key_id") == key,
                "representation historical binding")
        identity = row.get("representation_id")
        semantic = row.get("representation_semantic_certificate_sha256")
        require(type(identity) is str and identity not in representations
                and type(semantic) is str and len(semantic) == 64,
                "representation identity/semantic")
        representations.add(identity)
        for target in (comps[post], fibres[key]):
            target["representations"] += 1
            target["representation_sequence"].update(identity.encode("ascii") + b"\n")
            target["semantic_sequence"].update(bytes.fromhex(semantic))
    require(len(representations) == REPRESENTATIONS,
            "representation exhaustion")

    census: dict[str, dict[str, Any]] = {}
    within = 0
    for ordinal, row in enumerate(rows(census_path, C27R2_CENSUS_SCHEMA)):
        post = row.get("post_C27R2_component_id")
        require(row.get("ordinal") == ordinal and type(post) is str
                and post not in census and post in comps,
                "post census set")
        require(row.get("member_count") == comps[post]["members"]
                and row.get("old_C15_component_count") == len(comps[post]["old"])
                and row.get("old_C15_component_ids_sha256")
                    == string_sequence(sorted(comps[post]["old"]))
                and row.get("within_member_pair_count")
                    == comps[post]["members"] * (comps[post]["members"] - 1) // 2,
                "post census closure")
        within += row["within_member_pair_count"]
        census[post] = row
    require(len(census) == COMPONENTS and set(census) == set(comps)
            and within == WITHIN_PAIRS and len(fibres) == OFFICIAL_KEYS,
            "post component/key exhaustion")
    multiplicity = Counter(len(value["keys"]) for value in comps.values())
    incidence_a = sum(len(value["keys"]) for value in comps.values())
    incidence_b = sum(len(value["post"]) for value in fibres.values())
    require(incidence_a == incidence_b
            and sum(multiplicity.values()) == COMPONENTS
            and sum(key * value for key, value in multiplicity.items()) == incidence_a,
            "incidence/multiplicity identities")
    return {
        "binding": binding, "components": dict(comps), "fibres": dict(fibres),
        "families": dict(families), "census": census,
        "incidences": incidence_a, "multiplicity": dict(sorted(multiplicity.items())),
        "c27_result": c27_result,
    }


def candidate_directory(text: str) -> Path:
    base = directory_in_workspace(text, "candidate directory")
    require({entry.name for entry in base.iterdir()} == OUTPUT_NAMES,
            "candidate exact four-file inventory")
    for entry in base.iterdir():
        require(entry.is_file() and not entry.is_symlink()
                and entry.stat().st_nlink == 1, "candidate regular single-link file")
    return base


def ledger_descriptor(path: Path, count: int, sequence: hashlib._Hash, order: str) -> dict[str, Any]:
    return {
        "filename": path.name, "row_count": count, "size": path.stat().st_size,
        "sha256": hash_file(path), "row_sequence_sha256": sequence.hexdigest(),
        "order": order,
    }


def verify_candidate(
    base: Path, state: dict[str, Any], c27: dict[str, Any], c28: dict[str, Any],
    c25: dict[str, Any], c28_result: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    c27_object = state["c27_result"]["result_sha256"]
    c28_object = c28_result["result_sha256"]
    source_objects = {"C25": C25_RESULT_OBJECT, "C27R2": c27_object, "C28": c28_object}

    component_hashes: dict[str, str] = {}
    component_sequence = hashlib.sha256()
    component_count = 0
    posts = sorted(state["components"])
    for ordinal, row in enumerate(rows(base / COMPONENT_LEDGER, COMPONENT_SCHEMA)):
        require(ordinal < len(posts), "extra component row")
        post = posts[ordinal]
        value = state["components"][post]
        census = state["census"][post]
        body = {
            "schema": COMPONENT_SCHEMA, "ordinal": ordinal,
            "post_C27R2_component_id": post,
            "member_count": value["members"],
            "representation_count": value["representations"],
            "historical_C15_component_count": len(value["old"]),
            "historical_C15_component_ids_sha256": census["old_C15_component_ids_sha256"],
            "official_key_count": len(value["keys"]),
            "official_key_member_census": dict(sorted(value["keys"].items())),
            "family_member_census": dict(sorted(value["families"].items())),
            "member_id_sequence_sha256": value["member_sequence"].hexdigest(),
            "support_certificate_sequence_sha256": value["support_sequence"].hexdigest(),
            "representation_id_sequence_sha256": value["representation_sequence"].hexdigest(),
            "representation_semantic_sequence_sha256": value["semantic_sequence"].hexdigest(),
            "C25_fresh_component_id_role": "HISTORICAL_BINDING_ONLY__NOT_CURRENT_COMPONENT_AUTHORITY",
            "source_bindings": {
                "C27R2_post_component_census_row_sha256": census["row_sha256"],
                "C25_result_object_sha256": source_objects["C25"],
                "C28_v2_result_object_sha256": source_objects["C28"],
            },
            "formal_credit": 0,
            "C29": "UNAUTHORIZED_PENDING_FULL_RELEASE_TERMINAL",
        }
        expected = closed_row(body)
        require(row == expected, "component row independent equality:" + str(ordinal))
        component_hashes[post] = row["row_sha256"]
        component_sequence.update(bytes.fromhex(row["row_sha256"]))
        component_count += 1
    require(component_count == COMPONENTS, "component row count")
    component_descriptor = ledger_descriptor(
        base / COMPONENT_LEDGER, component_count, component_sequence,
        "LEXICOGRAPHIC_POST_C27R2_COMPONENT_ID",
    )

    fibre_hashes: dict[str, str] = {}
    fibre_sequence = hashlib.sha256()
    fibre_count = 0
    fibre_keys = sorted(state["fibres"])
    for ordinal, row in enumerate(rows(base / FIBRE_LEDGER, FIBRE_SCHEMA)):
        require(ordinal < len(fibre_keys), "extra fibre row")
        key = fibre_keys[ordinal]
        value = state["fibres"][key]
        post_ids = sorted(value["post"])
        post_rows = hashlib.sha256()
        for post in post_ids:
            post_rows.update(bytes.fromhex(component_hashes[post]))
        body = {
            "schema": FIBRE_SCHEMA, "ordinal": ordinal,
            "official_key_id": key,
            "member_count": value["members"],
            "representation_count": value["representations"],
            "post_C27R2_component_incidence_count": len(post_ids),
            "post_C27R2_component_ids_sha256": object_sha(post_ids),
            "post_component_row_sequence_sha256": post_rows.hexdigest(),
            "family_member_census": dict(sorted(value["families"].items())),
            "member_id_sequence_sha256": value["member_sequence"].hexdigest(),
            "support_certificate_sequence_sha256": value["support_sequence"].hexdigest(),
            "representation_id_sequence_sha256": value["representation_sequence"].hexdigest(),
            "representation_semantic_sequence_sha256": value["semantic_sequence"].hexdigest(),
            "fibre_inventory_complete": True,
            "global_transition_residual_count": 0,
            "source_bindings": {
                "C25_result_object_sha256": source_objects["C25"],
                "C27R2_result_object_sha256": source_objects["C27R2"],
                "C28_v2_result_object_sha256": source_objects["C28"],
            },
            "formal_credit": 0,
            "C29": "UNAUTHORIZED_PENDING_FULL_RELEASE_TERMINAL",
        }
        expected = closed_row(body)
        require(row == expected, "fibre row independent equality:" + str(ordinal))
        fibre_hashes[key] = row["row_sha256"]
        fibre_sequence.update(bytes.fromhex(row["row_sha256"]))
        fibre_count += 1
    require(fibre_count == OFFICIAL_KEYS, "fibre row count")
    fibre_descriptor = ledger_descriptor(
        base / FIBRE_LEDGER, fibre_count, fibre_sequence,
        "LEXICOGRAPHIC_OFFICIAL_KEY_ID",
    )

    disposition_sequence = hashlib.sha256()
    disposition_count = 0
    quotient_rows = rows(
        c27["members"]["member_to_post_component"]["path_object"],
        C27R2_MEMBER_SCHEMA,
    )
    supports = rows(c25["member"], C25_MEMBER_SCHEMA)
    candidates = rows(base / DISPOSITION_LEDGER, DISPOSITION_SCHEMA)
    for ordinal, triple in enumerate(zip(quotient_rows, supports, candidates, strict=True)):
        quotient, support, row = triple
        post = quotient["post_C27R2_component_id"]
        key = support["official_key_id"]
        body = {
            "schema": DISPOSITION_SCHEMA, "ordinal": ordinal,
            "member_id": support["member_id"], "official_key_id": key,
            "post_C27R2_component_id": post,
            "historical_C25_fresh_component_id": support["fresh_component_id"],
            "historical_component_binding_role": "CHECKED_JOIN_ONLY__NOT_CURRENT_AUTHORITY",
            "coarse_family": support["coarse_family"],
            "normalized_support_ast_sha256": support["normalized_support_ast_sha256"],
            "support_semantic_certificate_sha256": support["support_semantic_certificate_sha256"],
            "global_disposition": "ASSIGNED_TO_C28_V2_MAXIMAL_POST_C27R2_COMPONENT_IN_EXHAUSTED_OFFICIAL_KEY_FIBRE",
            "source_bindings": {
                "C25_member_row_sha256": support["row_sha256"],
                "C27R2_member_to_post_row_sha256": quotient["row_sha256"],
                "C29_v2_post_component_row_sha256": component_hashes[post],
                "C29_v2_fibre_row_sha256": fibre_hashes[key],
                "C28_v2_result_object_sha256": source_objects["C28"],
            },
            "formal_credit": 0,
            "C29": "UNAUTHORIZED_PENDING_FULL_RELEASE_TERMINAL",
        }
        require(row == closed_row(body),
                "disposition row independent equality:" + str(ordinal))
        disposition_sequence.update(bytes.fromhex(row["row_sha256"]))
        disposition_count += 1
    require(disposition_count == MEMBERS, "disposition row count")
    disposition_descriptor = ledger_descriptor(
        base / DISPOSITION_LEDGER, disposition_count, disposition_sequence,
        "C25_MEMBER_ORDINAL",
    )

    theorem = {
        "kind": "POST_C27R2_MEMBER_ID_REBOUND_OFFICIAL_KEY_FIBRE_EXHAUSTION_CANDIDATE",
        "C25_member_support_semantics_pinned": True,
        "C25_representation_semantics_pinned_and_owner_rebound": True,
        "C25_fresh_component_id_used_only_as_historical_join_check": True,
        "all_members_joined_by_member_id_to_post_C27R2_component": True,
        "C27R2_partition_terminal_pinned": True,
        "C28_v2_B2_pair_routing_and_maximality_terminal_pinned": True,
        "component_key_incidences_recomputed_not_imported": True,
        "component_key_multiplicity_recomputed_not_imported": True,
        "every_official_key_fibre_inventory_complete": True,
        "source_G_fibre_or_disposition_gap_count": 0,
    }
    body = {
        "schema": RESULT_SCHEMA,
        "status": (
            "PASS_C29_V2_MATHEMATICAL_CANDIDATE__POST_C27R2_MEMBER_REBIND_"
            "AND_FIBRE_EXHAUSTION_RECOMPUTED__ZERO_CREDIT_PENDING_FULL_RELEASE_TERMINAL"
        ),
        "source_authority": {
            "C25_manifest_sha256": c25["manifest"],
            "C25_result_object_sha256": C25_RESULT_OBJECT,
            "C27R2_terminal_root_manifest_sha256": c27["root"],
            "C27R2_terminal_receipt_file_sha256": c27["receipt_file"],
            "C27R2_terminal_receipt_object_sha256": c27["receipt_object"],
            "C27R2_terminal_replay_file_sha256": c27["replay_file"],
            "C27R2_terminal_replay_object_sha256": c27["replay_object"],
            "C27R2_C29_adapter_root_manifest_sha256": c27["adapter_root"],
            "C27R2_C29_adapter_receipt_file_sha256": c27["adapter_receipt_file"],
            "C27R2_C29_adapter_receipt_object_sha256": c27["adapter_receipt_object"],
            "C27R2_consumer_projection_sha256": c27["projection_object"],
            "C27R2_result_object_sha256": c27_object,
            "C28_v2_terminal_root_manifest_sha256": c28["root"],
            "C28_v2_terminal_receipt_file_sha256": c28["receipt_file"],
            "C28_v2_terminal_receipt_object_sha256": c28["receipt_object"],
            "C28_v2_terminal_replay_file_sha256": c28["replay_file"],
            "C28_v2_terminal_replay_object_sha256": c28["replay_object"],
            "C28_v2_C29_adapter_root_manifest_sha256": c28["adapter_root"],
            "C28_v2_C29_adapter_receipt_file_sha256": c28["adapter_receipt_file"],
            "C28_v2_C29_adapter_receipt_object_sha256": c28["adapter_receipt_object"],
            "C28_v2_consumer_projection_sha256": c28["projection_object"],
            "C28_v2_result_object_sha256": c28_object,
        },
        "recomputed_census": {
            "members": MEMBERS, "representations": REPRESENTATIONS,
            "post_C27R2_components": COMPONENTS, "official_keys": OFFICIAL_KEYS,
            "component_key_incidences": state["incidences"],
            "component_key_multiplicity_census": {
                str(key): value for key, value in state["multiplicity"].items()
            },
            "family_member_census": state["families"],
            "total_unordered_member_pairs": TOTAL_PAIRS,
            "within_post_component_member_pairs": WITHIN_PAIRS,
            "cross_post_component_member_pairs": CROSS_PAIRS,
        },
        "theorem": theorem, "theorem_sha256": object_sha(theorem),
        "ledgers": {
            "post_component_official_key_assignment": component_descriptor,
            "official_key_fibre_exhaustion": fibre_descriptor,
            "global_member_disposition": disposition_descriptor,
        },
        "formal_credit": 0, "manifest_authorized": False,
        "C29": "UNAUTHORIZED_PENDING_DUAL_SEED_NO_IMPORT_VERIFIER_ATTACKS_COLD_TOCTOU_MANIFESTS_OUTER_SEAL_TERMINAL_REPLAY",
        "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_MATHEMATICAL_CANDIDATE",
        "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED", "Gate5": "10/18", "CM2": "NO-GO_FOR_CLAIM",
    }
    expected_result = dict(body)
    expected_result["result_sha256"] = object_sha(expected_result)
    candidate_result = document(base / RESULT, "result_sha256")
    require(candidate_result == expected_result, "candidate result independent equality")
    return candidate_result, {
        "component": component_descriptor, "fibre": fibre_descriptor,
        "disposition": disposition_descriptor,
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode is True,
            "isolated Python -I -B runtime")
    output = Path(args.out_file).absolute()
    require(output.is_relative_to(ROOT) and not output.exists(), "fresh verifier output")
    c27 = terminal(
        args.c27r2_terminal_dir, "C27R2", args.expect_c27r2_root_sha256,
        args.expect_c27r2_receipt_file_sha256,
        args.expect_c27r2_receipt_object_sha256,
    )
    c28 = terminal(
        args.c28_terminal_dir, "C28", args.expect_c28_root_sha256,
        args.expect_c28_receipt_file_sha256,
        args.expect_c28_receipt_object_sha256,
    )
    require(c28["projection"].get("C27R2_terminal_root_manifest_sha256")
            == c27["root"], "C28 exact C27R2 predecessor root")
    c25 = c25_authority()
    c28_result = source_result(c28, "C28")
    state = rebuild(c27, c25)
    candidate = candidate_directory(args.candidate_dir)
    result, descriptors = verify_candidate(candidate, state, c27, c28, c25, c28_result)
    body = {
        "schema": VERIFICATION_SCHEMA,
        "status": (
            "PASS_NO_IMPORT_INDEPENDENT_C29_V2_FULL_RECONSTRUCTION__"
            "CONDITIONAL_ZERO_CREDIT_PENDING_ATTACKS_AND_RELEASE_TERMINAL"
        ),
        "candidate_result_file_sha256": hash_file(candidate / RESULT),
        "candidate_result_object_sha256": result["result_sha256"],
        "candidate_ledger_descriptors": descriptors,
        "independent_recomputed_census": result["recomputed_census"],
        "no_import_or_execution_of_producer": True,
        "C25_historical_component_binding_only": True,
        "member_id_rebind_complete": True,
        "representation_owner_rebind_complete": True,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C29": "UNAUTHORIZED_PENDING_FULL_RELEASE_TERMINAL",
        "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_VERIFICATION",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    verification = dict(body)
    verification["verification_sha256"] = object_sha(verification)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        stream.write(encode(verification) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    return verification


def self_test() -> dict[str, Any]:
    member_to_post = {"m0": "p0", "m1": "p0", "m2": "p1", "m3": "p2"}
    member_to_key = {"m0": "k0", "m1": "k1", "m2": "k1", "m3": "k2"}
    component_keys: dict[str, set[str]] = defaultdict(set)
    fibres: dict[str, set[str]] = defaultdict(set)
    for member in sorted(member_to_post):
        post = member_to_post[member]
        key = member_to_key[member]
        component_keys[post].add(key)
        fibres[key].add(post)
    left = sum(len(value) for value in component_keys.values())
    right = sum(len(value) for value in fibres.values())
    multiplicity = Counter(len(value) for value in component_keys.values())
    require(left == right == 4 and dict(multiplicity) == {1: 2, 2: 1},
            "self-test independent incidence identity")
    return {
        "schema": VERIFICATION_SCHEMA + ".self-test",
        "status": "PASS_NO_IMPORT_C29_V2_INDEPENDENT_JOIN_FIXTURE",
        "fixture_incidences": left,
        "formal_credit": 0, "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--c27r2-terminal-dir")
    value.add_argument("--expect-c27r2-root-sha256")
    value.add_argument("--expect-c27r2-receipt-file-sha256")
    value.add_argument("--expect-c27r2-receipt-object-sha256")
    value.add_argument("--c28-terminal-dir")
    value.add_argument("--expect-c28-root-sha256")
    value.add_argument("--expect-c28-receipt-file-sha256")
    value.add_argument("--expect-c28-receipt-object-sha256")
    value.add_argument("--candidate-dir")
    value.add_argument("--out-file")
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "c27r2_terminal_dir", "expect_c27r2_root_sha256",
        "expect_c27r2_receipt_file_sha256", "expect_c27r2_receipt_object_sha256",
        "c28_terminal_dir", "expect_c28_root_sha256",
        "expect_c28_receipt_file_sha256", "expect_c28_receipt_object_sha256",
        "candidate_dir", "out_file",
    )
    try:
        if args.self_test:
            require(all(getattr(args, field) is None for field in fields),
                    "self-test has no authority/candidate arguments")
            result = self_test()
        else:
            require(all(getattr(args, field) is not None for field in fields),
                    "all authority/candidate/output arguments required")
            result = run(args)
        sys.stdout.buffer.write(encode({
            "status": result["status"], "formal_credit": 0,
            "C29": result.get("C29", "UNAUTHORIZED"), "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
