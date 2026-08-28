#!/usr/bin/env python3
"""Build the append-only C29-v2 mathematical candidate.

This producer deliberately has no legacy C29/C28/C27 input.  It joins the
terminal-pinned C27R2 member-to-post-component ledger to the pinned C25
member semantics by ``member_id``.  C25 ``fresh_component_id`` is checked
only as a historical C15 binding and is never used as the current component
authority.

The C27R2 and C28 release formats were not final when this file was frozen.
Consequently each terminal must publish a root-manifest-bound
``c29_consumer_projection.json`` matching the small adapter contract below.
Absent or incomplete terminal contracts reject before an output directory is
created.  A successful producer result is still zero-credit and cannot mint
C29; independent replay, attacks, cold/TOCTOU checks, manifests, an outer
verifier, a seal, and terminal byte replay remain mandatory.
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
import tempfile
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()

PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
COMPONENT_LEDGER = PREFIX + "_post_component_official_key_assignment_ledger.jsonl.gz"
FIBRE_LEDGER = PREFIX + "_official_key_fibre_exhaustion_ledger.jsonl.gz"
DISPOSITION_LEDGER = PREFIX + "_global_member_disposition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
OUTPUT_NAMES = (COMPONENT_LEDGER, FIBRE_LEDGER, DISPOSITION_LEDGER, RESULT)

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
C25_MEMBER_SCHEMA = (
    "cm2.round306c25.source-g-typed-global-support-ledger.v1.member-row.v1"
)
C25_REPRESENTATION_SCHEMA = (
    "cm2.round306c25.source-g-typed-global-support-ledger.v1."
    "representation-row.v1"
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

EXPECTED_MEMBERS = 502_204
EXPECTED_REPRESENTATIONS = 549_616
EXPECTED_COMPONENTS = 43_684
EXPECTED_OFFICIAL_KEYS = 124
EXPECTED_TOTAL_PAIRS = 126_104_177_706
EXPECTED_WITHIN_PAIRS = 542_179_508
EXPECTED_CROSS_PAIRS = 125_561_998_198
EXPECTED_FAMILIES = {
    "PRESERVED": 126_468,
    "NON_GRAPH": 55_604,
    "R2": 295_336,
    "R292": 9_404,
    "G2A": 5_264,
    "G2B": 10_128,
}
SUPPORT_KINDS = {
    "EXACT_MEMBER_SUPPORT_EQUALITY",
    "FINITE_CELL_UNION_MEMBER_SUPPORT_EQUALITY",
    "RELATION_BACKED_MEMBER_SUPPORT_EQUALITY",
    "EXACT_EMPTY_MEMBER_SUPPORT_EQUALITY",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in items:
        need(type(key) is str and key not in out, "duplicate JSON key:" + str(key))
        out[key] = value
    return out


def constant(value: str) -> None:
    raise Failure("non-finite JSON constant:" + value)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def string_sequence(values: list[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update(value.encode("ascii") + b"\n")
    return state.hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1 << 20):
            state.update(chunk)
    return state.hexdigest()


def strict_json_bytes(raw: bytes, label: str, newline: bool = True) -> Any:
    if newline:
        need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
        raw = raw[:-1]
    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs, parse_constant=constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Failure(label + ":JSON") from error
    need(canonical(value) == raw, label + ":canonical")
    return value


def closed_document(
    path: Path, closure_field: str, newline: bool = True,
) -> dict[str, Any]:
    value = strict_json_bytes(path.read_bytes(), path.name, newline)
    need(type(value) is dict, path.name + ":object")
    body = dict(value)
    claimed = body.pop(closure_field, None)
    need(type(claimed) is str and claimed == digest(body), path.name + ":closure")
    return value


def close_row(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def safe_workspace_path(text: str) -> Path:
    need(type(text) is str and text != "", "workspace relative path")
    pure = PurePosixPath(text)
    need(not pure.is_absolute() and ".." not in pure.parts and "." not in pure.parts,
         "safe workspace relative path:" + text)
    path = ROOT.joinpath(*pure.parts)
    resolved = path.resolve(strict=True)
    need(resolved.is_relative_to(ROOT) and path == resolved,
         "workspace path lexical/no-symlink:" + text)
    need(path.is_file() and not path.is_symlink(), "workspace regular file:" + text)
    return path


def safe_directory(path: Path, label: str) -> Path:
    path = path.absolute()
    resolved = path.resolve(strict=True)
    need(path == resolved and resolved.is_relative_to(ROOT), label + ":inside workspace")
    need(path.is_dir() and not path.is_symlink(), label + ":regular directory")
    return path


def parse_manifest(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), path.name + ":newline")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise Failure(path.name + ":ASCII") from error
    for line in lines:
        fields = line.split("  ", 1)
        need(len(fields) == 2 and len(fields[0]) == 64
             and all(char in "0123456789abcdef" for char in fields[0]),
             path.name + ":manifest line")
        name = fields[1]
        need(name != "" and name not in rows, path.name + ":manifest unique name")
        rows[name] = fields[0]
    need(len(rows) > 0, path.name + ":nonempty")
    return rows


def manifest_member(entries: dict[str, str], path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    candidates = [relative, path.name]
    found = [(name, entries[name]) for name in candidates if name in entries]
    need(len(found) == 1, "manifest exact member:" + relative)
    need(found[0][1] == file_sha(path), "manifest member SHA:" + relative)
    return found[0][0]


def iter_rows(path: Path, expected_schema: str) -> Iterator[dict[str, Any]]:
    try:
        with gzip.open(path, "rb") as source:
            for ordinal, line in enumerate(source):
                need(line.endswith(b"\n") and not line.endswith(b"\n\n"),
                     path.name + ":row newline")
                value = strict_json_bytes(line[:-1], path.name + ":" + str(ordinal), False)
                need(type(value) is dict and value.get("schema") == expected_schema,
                     path.name + ":row schema")
                body = dict(value)
                claimed = body.pop("row_sha256", None)
                need(type(claimed) is str and claimed == digest(body),
                     path.name + ":row closure:" + str(ordinal))
                yield value
    except (gzip.BadGzipFile, EOFError) as error:
        raise Failure(path.name + ":gzip") from error


def validate_terminal(
    terminal_arg: str, kind: str, expected_root: str,
    expected_receipt_file: str, expected_receipt_object: str,
) -> dict[str, Any]:
    terminal = safe_directory(Path(terminal_arg), kind + " terminal")
    root_path = terminal / "root_manifest.sha256"
    payload_path = terminal / "payload_manifest.sha256"
    receipt_path = terminal / "terminal_receipt.json"
    pass_path = terminal / "PASS.lock"
    projection_path = terminal / PROJECTION_FILE
    need(all(path.is_file() and not path.is_symlink() for path in (
        root_path, payload_path, receipt_path, pass_path, projection_path,
    )), kind + ":complete dynamic terminal adapter")
    need(all(type(item) is str and len(item) == 64
             and all(char in "0123456789abcdef" for char in item)
             for item in (expected_root, expected_receipt_file,
                          expected_receipt_object)), kind + ":external SHA pins")
    need(file_sha(root_path) == expected_root, kind + ":root external pin")
    need(file_sha(receipt_path) == expected_receipt_file,
         kind + ":receipt external file pin")
    root = parse_manifest(root_path)
    need(root == {
        "payload_manifest.sha256": file_sha(payload_path),
        "terminal_receipt.json": expected_receipt_file,
    }, kind + ":exact two-member terminal root")
    payload = parse_manifest(payload_path)
    manifest_member(payload, projection_path)
    receipt = closed_document(receipt_path, "terminal_receipt_sha256")
    need(receipt["terminal_receipt_sha256"] == expected_receipt_object,
         kind + ":receipt external object pin")
    adapter_status = (
        "PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT"
        if kind == "C27R2" else
        "PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT"
    )
    need(receipt.get("schema") == ADAPTER_RECEIPT_SCHEMA
         and receipt.get("status") == adapter_status
         and receipt.get("authority_kind") == kind
         and receipt.get("terminal_replay_passed") is True
         and receipt.get("authority_minted") is True
         and receipt.get("formal_credit") == 0,
         kind + ":terminal replay semantics")
    projection = closed_document(projection_path, "projection_sha256")
    schema = C27R2_PROJECTION_SCHEMA if kind == "C27R2" else C28_PROJECTION_SCHEMA
    status = (
        "PASS_C27R2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"
        if kind == "C27R2"
        else "PASS_C28_V2_TERMINAL_AUTHORITY_FOR_C29_CONSUMER"
    )
    need(projection.get("schema") == schema and projection.get("status") == status,
         kind + ":projection schema/status")
    source_pins = (
        projection.get("terminal_root_manifest_sha256"),
        projection.get("terminal_receipt_file_sha256"),
        projection.get("terminal_receipt_object_sha256"),
        projection.get("terminal_replay_file_sha256"),
        projection.get("terminal_replay_object_sha256"),
    )
    need(all(type(item) is str and len(item) == 64
             and all(char in "0123456789abcdef" for char in item)
             for item in source_pins), kind + ":source terminal pins")
    need(projection.get("terminal_replay_passed") is True
         and projection.get("authority_minted") is True
         and receipt.get("source_terminal_root_manifest_sha256") == source_pins[0]
         and receipt.get("source_terminal_receipt_file_sha256") == source_pins[1]
         and receipt.get("source_terminal_receipt_object_sha256") == source_pins[2]
         and receipt.get("source_terminal_replay_file_sha256") == source_pins[3]
         and receipt.get("source_terminal_replay_object_sha256") == source_pins[4]
         and receipt.get("source_terminal_status") == projection.get("terminal_status")
         and projection.get("PASS_lock_sha256") == file_sha(pass_path),
         kind + ":projection terminal binding")
    pass_bytes = pass_path.read_bytes()
    expected_pass = (
        b"PASS_C29_V2_C27R2_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
        if kind == "C27R2" else
        b"PASS_C29_V2_C28_TERMINAL_CONSUMER_ADAPTER__ZERO_CREDIT\n"
    )
    need(pass_bytes == expected_pass, kind + ":exact adapter PASS")
    members = projection.get("payload_members")
    need(type(members) is dict, kind + ":projection payload members")
    required = (
        {"producer_result", "member_to_post_component", "post_component_census"}
        if kind == "C27R2" else {"producer_result"}
    )
    need(set(members) == required, kind + ":exact projection payload keys")
    captures: dict[str, dict[str, Any]] = {}
    for name in sorted(required):
        item = members[name]
        need(type(item) is dict and set(item) >= {"path", "file_sha256"},
             kind + ":payload descriptor:" + name)
        path = safe_workspace_path(item["path"])
        need(file_sha(path) == item["file_sha256"], kind + ":payload file pin:" + name)
        manifest_member(payload, path)
        captures[name] = {**item, "resolved_path": path}
    census = projection.get("exact_census")
    need(type(census) is dict, kind + ":projection census")
    if kind == "C27R2":
        need(census.get("frozen_C15_members") == EXPECTED_MEMBERS
             and census.get("post_C27R2_components") == EXPECTED_COMPONENTS
             and census.get("within_post_component_member_pairs") == EXPECTED_WITHIN_PAIRS
             and census.get("cross_post_component_member_pairs") == EXPECTED_CROSS_PAIRS,
             "C27R2:projection exact census")
    else:
        need(census.get("post_C27R2_components") == EXPECTED_COMPONENTS
             and census.get("cross_post_component_member_pairs") == EXPECTED_CROSS_PAIRS
             and projection.get("B2_pair_routing_complete") is True
             and projection.get("component_maximality_complete") is True
             and projection.get("new_legal_cross_component_pairs") == 0
             and projection.get("unresolved_pairs") == 0,
             "C28:projection B2/maximality census")
    return {
        "terminal_dir": terminal,
        "root_sha256": source_pins[0],
        "receipt_file_sha256": source_pins[1],
        "receipt_object_sha256": source_pins[2],
        "replay_file_sha256": source_pins[3],
        "replay_object_sha256": source_pins[4],
        "adapter_root_sha256": expected_root,
        "adapter_receipt_file_sha256": expected_receipt_file,
        "adapter_receipt_object_sha256": expected_receipt_object,
        "projection_sha256": projection["projection_sha256"],
        "payload_manifest_sha256": file_sha(payload_path),
        "members": captures,
        "projection": projection,
    }


def validate_c25() -> dict[str, Any]:
    base = ROOT / "deliverables"
    for name, expected in C25_PINS.items():
        path = base / name
        need(path.is_file() and not path.is_symlink() and file_sha(path) == expected,
             "C25 static pin:" + name)
    entries = parse_manifest(base / C25_MANIFEST)
    for name in (C25_MEMBER, C25_REPRESENTATION, C25_RESULT, C25_VERIFICATION):
        need(entries.get(name) == C25_PINS[name], "C25 manifest member:" + name)
    result = closed_document(base / C25_RESULT, "result_sha256", False)
    verification = strict_json_bytes(
        (base / C25_VERIFICATION).read_bytes(), C25_VERIFICATION,
    )
    need(result["result_sha256"] == C25_RESULT_OBJECT
         and result.get("status") == (
             "PASS_502204_MEMBER_TYPED_GLOBAL_SUPPORT_AND_549616_"
             "REPRESENTATION_SEMANTIC_LEDGER_SEALED__B1A_REPLAY_AUTHORIZED"
         ), "C25 result authority")
    need(type(verification) is dict
         and verification.get("status") == (
             "PASS_INDEPENDENT_C25_1051820_ROW_RECONSTRUCTION__8_OF_8_"
             "ATTACKS_REJECTED__DOUBLE_SEED_BYTE_IDENTICAL__MANIFEST_FIRST_STDOUT_ONLY"
         ) and verification.get("result_object_sha256") == C25_RESULT_OBJECT,
         "C25 verification authority")
    credit = result.get("global_credit")
    need(type(credit) is dict
         and credit.get("member_normalized_support_set_equality") == EXPECTED_MEMBERS
         and credit.get("typed_representation_semantic_disposition") == EXPECTED_REPRESENTATIONS,
         "C25 semantic census")
    return {
        "member_path": base / C25_MEMBER,
        "representation_path": base / C25_REPRESENTATION,
        "result_object_sha256": C25_RESULT_OBJECT,
        "manifest_sha256": C25_PINS[C25_MANIFEST],
    }


def validate_result_descriptor(result_path: Path, member: dict[str, Any], label: str) -> dict[str, Any]:
    result = closed_document(result_path, "result_sha256")
    need(member.get("object_sha256") == result["result_sha256"],
         label + ":projection result object pin")
    return result


def descriptor_matches(path: Path, descriptor: dict[str, Any], rows_expected: int) -> None:
    need(type(descriptor) is dict and descriptor.get("filename") == path.name
         and descriptor.get("sha256") == file_sha(path)
         and descriptor.get("row_count") == rows_expected,
         "ledger descriptor:" + path.name)


def accumulator() -> dict[str, Any]:
    return {
        "members": 0,
        "representations": 0,
        "keys": Counter(),
        "families": Counter(),
        "old_components": set(),
        "post_components": set(),
        "member_ids": hashlib.sha256(),
        "supports": hashlib.sha256(),
        "representation_ids": hashlib.sha256(),
        "representation_semantics": hashlib.sha256(),
    }


def reconstruct(c27: dict[str, Any], c25: dict[str, Any]) -> dict[str, Any]:
    member_path = c27["members"]["member_to_post_component"]["resolved_path"]
    census_path = c27["members"]["post_component_census"]["resolved_path"]
    result_path = c27["members"]["producer_result"]["resolved_path"]
    c27_result = validate_result_descriptor(
        result_path, c27["members"]["producer_result"], "C27R2",
    )
    ledgers = c27_result.get("ledgers")
    need(type(ledgers) is dict, "C27R2 result ledgers")
    descriptor_matches(member_path, ledgers.get("member_to_post_component"), EXPECTED_MEMBERS)
    descriptor_matches(census_path, ledgers.get("post_component_census"), EXPECTED_COMPONENTS)

    bindings: dict[str, tuple[str, str, str]] = {}
    components: dict[str, dict[str, Any]] = defaultdict(accumulator)
    fibres: dict[str, dict[str, Any]] = defaultdict(accumulator)
    families: Counter[str] = Counter()
    c27_rows = iter_rows(member_path, C27R2_MEMBER_SCHEMA)
    c25_rows = iter_rows(c25["member_path"], C25_MEMBER_SCHEMA)
    member_count = 0
    for ordinal, pair in enumerate(zip(c27_rows, c25_rows, strict=True)):
        c27_row, support = pair
        need(c27_row.get("ordinal") == ordinal
             and c27_row.get("member_ordinal") == ordinal
             and support.get("member_ordinal") == ordinal,
             "member ordinal lockstep")
        member_id = support.get("member_id")
        old = support.get("fresh_component_id")
        post = c27_row.get("post_C27R2_component_id")
        key = support.get("official_key_id")
        family = support.get("coarse_family")
        need(type(member_id) is str and c27_row.get("registry_member_id") == member_id
             and c27_row.get("old_C15_component_id") == old,
             "member_id join and historical C15 binding")
        need(type(post) is str and post.startswith("round306c27r2-source-g-post-component:")
             and type(key) is str and type(family) is str,
             "post component/key/family types")
        need(support.get("support_semantic_kind") in SUPPORT_KINDS,
             "C25 member support semantic kind")
        need(member_id not in bindings, "unique member_id")
        bindings[member_id] = (post, old, key)
        comp = components[post]
        fibre = fibres[key]
        for target in (comp, fibre):
            target["members"] += 1
            target["keys"][key] += 1
            target["families"][family] += 1
            target["old_components"].add(old)
            target["member_ids"].update(member_id.encode("ascii") + b"\n")
            target["supports"].update(bytes.fromhex(support["support_semantic_certificate_sha256"]))
        fibre["post_components"].add(post)
        comp["post_components"].add(post)
        families[family] += 1
        member_count += 1
    need(member_count == EXPECTED_MEMBERS and len(bindings) == EXPECTED_MEMBERS,
         "502204 member exhaustion")
    need(dict(families) == EXPECTED_FAMILIES, "C25 family census")

    representation_count = 0
    representation_ids: set[str] = set()
    for ordinal, row in enumerate(iter_rows(c25["representation_path"], C25_REPRESENTATION_SCHEMA)):
        need(row.get("representation_ordinal") == ordinal,
             "representation ordinal")
        owner = row.get("owner_member_id")
        need(type(owner) is str and owner in bindings, "representation owner member join")
        post, old, key = bindings[owner]
        need(row.get("fresh_component_id") == old
             and row.get("official_key_id") == key,
             "representation historical component/key binding")
        representation_id = row.get("representation_id")
        semantic = row.get("representation_semantic_certificate_sha256")
        need(type(representation_id) is str and representation_id not in representation_ids
             and type(semantic) is str and len(semantic) == 64,
             "representation identity/semantic")
        representation_ids.add(representation_id)
        for target in (components[post], fibres[key]):
            target["representations"] += 1
            target["representation_ids"].update(representation_id.encode("ascii") + b"\n")
            target["representation_semantics"].update(bytes.fromhex(semantic))
        representation_count += 1
    need(representation_count == EXPECTED_REPRESENTATIONS
         and len(representation_ids) == EXPECTED_REPRESENTATIONS,
         "549616 representation exhaustion")

    census_source: dict[str, dict[str, Any]] = {}
    within = 0
    for ordinal, row in enumerate(iter_rows(census_path, C27R2_CENSUS_SCHEMA)):
        need(row.get("ordinal") == ordinal, "C27R2 census ordinal")
        post = row.get("post_C27R2_component_id")
        need(type(post) is str and post not in census_source and post in components,
             "C27R2 census post component set")
        need(row.get("member_count") == components[post]["members"]
             and row.get("old_C15_component_count") == len(components[post]["old_components"])
             and row.get("old_C15_component_ids_sha256")
                 == string_sequence(sorted(components[post]["old_components"]))
             and row.get("within_member_pair_count")
                 == components[post]["members"] * (components[post]["members"] - 1) // 2,
             "C27R2 census member/old-component closure")
        within += row["within_member_pair_count"]
        census_source[post] = row
    need(len(census_source) == EXPECTED_COMPONENTS
         and set(census_source) == set(components), "43684 post component exhaustion")
    need(within == EXPECTED_WITHIN_PAIRS, "within pair closure")
    need(len(fibres) == EXPECTED_OFFICIAL_KEYS, "124 official key exhaustion")
    multiplicity = Counter(len(value["keys"]) for value in components.values())
    incidences_by_components = sum(len(value["keys"]) for value in components.values())
    incidences_by_fibres = sum(
        len(value["post_components"]) for value in fibres.values()
    )
    need(incidences_by_components == incidences_by_fibres,
         "component-key incidence two-way identity")
    need(sum(multiplicity.values()) == EXPECTED_COMPONENTS
         and sum(count * multiplicity_value
                 for count, multiplicity_value in multiplicity.items())
             == incidences_by_components,
         "component-key multiplicity identity")
    return {
        "bindings": bindings,
        "components": dict(components),
        "fibres": dict(fibres),
        "families": dict(families),
        "census_source": census_source,
        "component_key_incidences": incidences_by_components,
        "component_key_multiplicity": dict(sorted(multiplicity.items())),
    }


class LedgerWriter:
    def __init__(self, path: Path, schema: str):
        self.path = path
        self.schema = schema
        self.raw = path.open("xb")
        self.output = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, row: dict[str, Any]) -> None:
        need(row.get("schema") == self.schema and row.get("ordinal") == self.count,
             self.path.name + ":output schema/ordinal")
        self.output.write(canonical(row) + b"\n")
        self.sequence.update(bytes.fromhex(row["row_sha256"]))
        self.count += 1

    def finish(self, order: str) -> dict[str, Any]:
        self.output.close()
        self.raw.close()
        return {
            "filename": self.path.name,
            "row_count": self.count,
            "size": self.path.stat().st_size,
            "sha256": file_sha(self.path),
            "row_sequence_sha256": self.sequence.hexdigest(),
            "order": order,
        }


def component_rows(state: dict[str, Any], source_objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    for ordinal, post in enumerate(sorted(state["components"])):
        value = state["components"][post]
        census = state["census_source"][post]
        body = {
            "schema": COMPONENT_SCHEMA,
            "ordinal": ordinal,
            "post_C27R2_component_id": post,
            "member_count": value["members"],
            "representation_count": value["representations"],
            "historical_C15_component_count": len(value["old_components"]),
            "historical_C15_component_ids_sha256": census["old_C15_component_ids_sha256"],
            "official_key_count": len(value["keys"]),
            "official_key_member_census": dict(sorted(value["keys"].items())),
            "family_member_census": dict(sorted(value["families"].items())),
            "member_id_sequence_sha256": value["member_ids"].hexdigest(),
            "support_certificate_sequence_sha256": value["supports"].hexdigest(),
            "representation_id_sequence_sha256": value["representation_ids"].hexdigest(),
            "representation_semantic_sequence_sha256": value["representation_semantics"].hexdigest(),
            "C25_fresh_component_id_role": "HISTORICAL_BINDING_ONLY__NOT_CURRENT_COMPONENT_AUTHORITY",
            "source_bindings": {
                "C27R2_post_component_census_row_sha256": census["row_sha256"],
                "C25_result_object_sha256": source_objects["C25"],
                "C28_v2_result_object_sha256": source_objects["C28"],
            },
            "formal_credit": 0,
            "C29": "UNAUTHORIZED_PENDING_FULL_RELEASE_TERMINAL",
        }
        yield close_row(body)


def fibre_rows(state: dict[str, Any], component_hashes: dict[str, str], source_objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    for ordinal, key in enumerate(sorted(state["fibres"])):
        value = state["fibres"][key]
        post_ids = sorted(value["post_components"])
        row_sequence = hashlib.sha256()
        for post in post_ids:
            row_sequence.update(bytes.fromhex(component_hashes[post]))
        body = {
            "schema": FIBRE_SCHEMA,
            "ordinal": ordinal,
            "official_key_id": key,
            "member_count": value["members"],
            "representation_count": value["representations"],
            "post_C27R2_component_incidence_count": len(post_ids),
            "post_C27R2_component_ids_sha256": digest(post_ids),
            "post_component_row_sequence_sha256": row_sequence.hexdigest(),
            "family_member_census": dict(sorted(value["families"].items())),
            "member_id_sequence_sha256": value["member_ids"].hexdigest(),
            "support_certificate_sequence_sha256": value["supports"].hexdigest(),
            "representation_id_sequence_sha256": value["representation_ids"].hexdigest(),
            "representation_semantic_sequence_sha256": value["representation_semantics"].hexdigest(),
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
        yield close_row(body)


def write_json_exclusive(path: Path, value: dict[str, Any]) -> None:
    with path.open("xb") as output:
        output.write(canonical(value) + b"\n")
        output.flush()
        os.fsync(output.fileno())


def build(args: argparse.Namespace) -> dict[str, Any]:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True,
         "isolated Python -I -B runtime")
    out_dir = Path(args.out_dir).absolute()
    need(out_dir.is_relative_to(ROOT) and not out_dir.exists(), "fresh output directory")
    c27 = validate_terminal(
        args.c27r2_terminal_dir, "C27R2", args.expect_c27r2_root_sha256,
        args.expect_c27r2_receipt_file_sha256,
        args.expect_c27r2_receipt_object_sha256,
    )
    c28 = validate_terminal(
        args.c28_terminal_dir, "C28", args.expect_c28_root_sha256,
        args.expect_c28_receipt_file_sha256,
        args.expect_c28_receipt_object_sha256,
    )
    need(c28["projection"].get("C27R2_terminal_root_manifest_sha256")
         == c27["root_sha256"], "C28 terminal binds exact C27R2 terminal root")
    c25 = validate_c25()
    c28_result = validate_result_descriptor(
        c28["members"]["producer_result"]["resolved_path"],
        c28["members"]["producer_result"], "C28",
    )
    state = reconstruct(c27, c25)
    c27_result = validate_result_descriptor(
        c27["members"]["producer_result"]["resolved_path"],
        c27["members"]["producer_result"], "C27R2",
    )
    source_objects = {
        "C25": c25["result_object_sha256"],
        "C27R2": c27_result["result_sha256"],
        "C28": c28_result["result_sha256"],
    }

    out_dir.mkdir(parents=True, mode=0o700)
    component_writer = LedgerWriter(out_dir / COMPONENT_LEDGER, COMPONENT_SCHEMA)
    component_hashes: dict[str, str] = {}
    for row in component_rows(state, source_objects):
        component_writer.write(row)
        component_hashes[row["post_C27R2_component_id"]] = row["row_sha256"]
    component_descriptor = component_writer.finish("LEXICOGRAPHIC_POST_C27R2_COMPONENT_ID")

    fibre_writer = LedgerWriter(out_dir / FIBRE_LEDGER, FIBRE_SCHEMA)
    fibre_hashes: dict[str, str] = {}
    for row in fibre_rows(state, component_hashes, source_objects):
        fibre_writer.write(row)
        fibre_hashes[row["official_key_id"]] = row["row_sha256"]
    fibre_descriptor = fibre_writer.finish("LEXICOGRAPHIC_OFFICIAL_KEY_ID")

    disposition_writer = LedgerWriter(out_dir / DISPOSITION_LEDGER, DISPOSITION_SCHEMA)
    c27_rows = iter_rows(
        c27["members"]["member_to_post_component"]["resolved_path"],
        C27R2_MEMBER_SCHEMA,
    )
    for ordinal, pair in enumerate(zip(
        c27_rows, iter_rows(c25["member_path"], C25_MEMBER_SCHEMA), strict=True,
    )):
        c27_row, support = pair
        post = c27_row["post_C27R2_component_id"]
        key = support["official_key_id"]
        body = {
            "schema": DISPOSITION_SCHEMA,
            "ordinal": ordinal,
            "member_id": support["member_id"],
            "official_key_id": key,
            "post_C27R2_component_id": post,
            "historical_C25_fresh_component_id": support["fresh_component_id"],
            "historical_component_binding_role": "CHECKED_JOIN_ONLY__NOT_CURRENT_AUTHORITY",
            "coarse_family": support["coarse_family"],
            "normalized_support_ast_sha256": support["normalized_support_ast_sha256"],
            "support_semantic_certificate_sha256": support["support_semantic_certificate_sha256"],
            "global_disposition": "ASSIGNED_TO_C28_V2_MAXIMAL_POST_C27R2_COMPONENT_IN_EXHAUSTED_OFFICIAL_KEY_FIBRE",
            "source_bindings": {
                "C25_member_row_sha256": support["row_sha256"],
                "C27R2_member_to_post_row_sha256": c27_row["row_sha256"],
                "C29_v2_post_component_row_sha256": component_hashes[post],
                "C29_v2_fibre_row_sha256": fibre_hashes[key],
                "C28_v2_result_object_sha256": source_objects["C28"],
            },
            "formal_credit": 0,
            "C29": "UNAUTHORIZED_PENDING_FULL_RELEASE_TERMINAL",
        }
        disposition_writer.write(close_row(body))
    disposition_descriptor = disposition_writer.finish("C25_MEMBER_ORDINAL")
    need(component_descriptor["row_count"] == EXPECTED_COMPONENTS
         and fibre_descriptor["row_count"] == EXPECTED_OFFICIAL_KEYS
         and disposition_descriptor["row_count"] == EXPECTED_MEMBERS,
         "output row census")

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
            "C25_manifest_sha256": c25["manifest_sha256"],
            "C25_result_object_sha256": source_objects["C25"],
            "C27R2_terminal_root_manifest_sha256": c27["root_sha256"],
            "C27R2_terminal_receipt_file_sha256": c27["receipt_file_sha256"],
            "C27R2_terminal_receipt_object_sha256": c27["receipt_object_sha256"],
            "C27R2_terminal_replay_file_sha256": c27["replay_file_sha256"],
            "C27R2_terminal_replay_object_sha256": c27["replay_object_sha256"],
            "C27R2_C29_adapter_root_manifest_sha256": c27["adapter_root_sha256"],
            "C27R2_C29_adapter_receipt_file_sha256": c27["adapter_receipt_file_sha256"],
            "C27R2_C29_adapter_receipt_object_sha256": c27["adapter_receipt_object_sha256"],
            "C27R2_consumer_projection_sha256": c27["projection_sha256"],
            "C27R2_result_object_sha256": source_objects["C27R2"],
            "C28_v2_terminal_root_manifest_sha256": c28["root_sha256"],
            "C28_v2_terminal_receipt_file_sha256": c28["receipt_file_sha256"],
            "C28_v2_terminal_receipt_object_sha256": c28["receipt_object_sha256"],
            "C28_v2_terminal_replay_file_sha256": c28["replay_file_sha256"],
            "C28_v2_terminal_replay_object_sha256": c28["replay_object_sha256"],
            "C28_v2_C29_adapter_root_manifest_sha256": c28["adapter_root_sha256"],
            "C28_v2_C29_adapter_receipt_file_sha256": c28["adapter_receipt_file_sha256"],
            "C28_v2_C29_adapter_receipt_object_sha256": c28["adapter_receipt_object_sha256"],
            "C28_v2_consumer_projection_sha256": c28["projection_sha256"],
            "C28_v2_result_object_sha256": source_objects["C28"],
        },
        "recomputed_census": {
            "members": EXPECTED_MEMBERS,
            "representations": EXPECTED_REPRESENTATIONS,
            "post_C27R2_components": EXPECTED_COMPONENTS,
            "official_keys": EXPECTED_OFFICIAL_KEYS,
            "component_key_incidences": state["component_key_incidences"],
            "component_key_multiplicity_census": {
                str(key): value for key, value in state["component_key_multiplicity"].items()
            },
            "family_member_census": state["families"],
            "total_unordered_member_pairs": EXPECTED_TOTAL_PAIRS,
            "within_post_component_member_pairs": EXPECTED_WITHIN_PAIRS,
            "cross_post_component_member_pairs": EXPECTED_CROSS_PAIRS,
        },
        "theorem": theorem,
        "theorem_sha256": digest(theorem),
        "ledgers": {
            "post_component_official_key_assignment": component_descriptor,
            "official_key_fibre_exhaustion": fibre_descriptor,
            "global_member_disposition": disposition_descriptor,
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "C29": "UNAUTHORIZED_PENDING_DUAL_SEED_NO_IMPORT_VERIFIER_ATTACKS_COLD_TOCTOU_MANIFESTS_OUTER_SEAL_TERMINAL_REPLAY",
        "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_MATHEMATICAL_CANDIDATE",
        "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED",
        "D04": "NOT_MINTED",
        "Gate5": "10/18",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["result_sha256"] = digest(result)
    write_json_exclusive(out_dir / RESULT, result)
    return result


def self_test() -> dict[str, Any]:
    # The fixture proves the key invariant: merging historical components can
    # change component-key multiplicity, and the value is derived from joined
    # member IDs rather than copied from a predecessor census.
    joined = [
        ("m0", "old0", "postA", "k0"),
        ("m1", "old1", "postA", "k1"),
        ("m2", "old2", "postB", "k1"),
        ("m3", "old3", "postC", "k2"),
        ("m4", "old4", "postC", "k2"),
    ]
    keys: dict[str, set[str]] = defaultdict(set)
    for member, old, post, key in joined:
        need(all(type(value) is str and value for value in (member, old, post, key)),
             "self-test tuple")
        keys[post].add(key)
    incidence = sum(len(value) for value in keys.values())
    multiplicity = Counter(len(value) for value in keys.values())
    need(incidence == 4 and dict(multiplicity) == {1: 2, 2: 1},
         "self-test recomputed incidence/multiplicity")
    with tempfile.TemporaryDirectory(prefix="cm2-c29-v2-self-test-") as name:
        path = Path(name) / "rows.jsonl.gz"
        writer = LedgerWriter(path, "fixture")
        for ordinal, post in enumerate(sorted(keys)):
            writer.write(close_row({
                "schema": "fixture", "ordinal": ordinal,
                "post_C27R2_component_id": post,
                "official_key_count": len(keys[post]), "formal_credit": 0,
            }))
        descriptor = writer.finish("LEXICOGRAPHIC_POST")
        replay = list(iter_rows(path, "fixture"))
        need(len(replay) == 3 and descriptor["row_count"] == 3,
             "self-test deterministic ledger replay")
    return {
        "schema": RESULT_SCHEMA + ".self-test",
        "status": "PASS_C29_V2_MEMBER_ID_REBIND_MATH_AND_GZIP_FIXTURE",
        "fixture_component_key_incidences": incidence,
        "fixture_component_key_multiplicity": {
            str(key): value for key, value in sorted(multiplicity.items())
        },
        "formal_credit": 0,
        "C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
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
    value.add_argument("--out-dir")
    return value


def main() -> int:
    args = parser().parse_args()
    names = (
        "c27r2_terminal_dir", "expect_c27r2_root_sha256",
        "expect_c27r2_receipt_file_sha256", "expect_c27r2_receipt_object_sha256",
        "c28_terminal_dir", "expect_c28_root_sha256",
        "expect_c28_receipt_file_sha256", "expect_c28_receipt_object_sha256",
        "out_dir",
    )
    try:
        if args.self_test:
            need(all(getattr(args, name) is None for name in names),
                 "self-test accepts no authority/output arguments")
            result = self_test()
        else:
            need(all(getattr(args, name) is not None for name in names),
                 "all terminal pins and fresh output directory are required")
            result = build(args)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "C29": result.get("C29", "UNAUTHORIZED"),
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
