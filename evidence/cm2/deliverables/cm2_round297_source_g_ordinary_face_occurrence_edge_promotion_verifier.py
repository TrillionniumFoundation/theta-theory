#!/usr/bin/env python3
"""Independent cacheless verifier for Round297 ordinary-face edge promotion.

The producer is never imported or executed.  This verifier streams and
reconstructs the complete Round266 component/member frontier, Round294
registry, Round288 atom-to-occurrence map, Round279 atoms, and all 330,724
ordinary face edges.  It constructs the expected ledger bytes and result
before opening any current Round297 candidate artifact.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
import argparse
import gzip
import hashlib
import io
import json
import mmap
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion"
PRODUCER = HERE / f"{PREFIX}.py"
LEDGER = HERE / f"{PREFIX}_edge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
OUTPUT = HERE / f"{PREFIX}_verification.json"

SCHEMA = "cm2.round297.source-g-ordinary-face-occurrence-edge-promotion.v1"
LEDGER_SCHEMA = SCHEMA + ".edge-ledger.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"

PACKAGE_MANIFEST_PINS = {
    "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256":
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_manifest.sha256":
        "dc726fde4395c23bd528ef4fc674289bb224c42e023520487676c3deafca12ac",
    "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_manifest.sha256":
        "3afccfd7a1305becaffa5839fa1fdcdab74f6dda7f423245cea2303bc10b9d89",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_manifest.sha256":
        "c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_manifest.sha256":
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_manifest.sha256":
        "09cec800efc3c7dd21bebab4a226d384f51ec1273040c548bfa54834a25c8331",
}

CANDIDATE_PINS = {
    PRODUCER.name:
        "ce09ba21be3586526652542256bc4e69558d996d81adb1951e6488faf81ba2a8",
    LEDGER.name:
        "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
    RESULT.name:
        "e95f7139548f6f2fe9d96c52d50ebd116fff938b990c7b31b2f76c0d17bc8d56",
}

R266_CERT = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
R266_VERIFICATION = (
    "cm2_round266_source_g_expanded_curved_face_closure_verification.json"
)
R279_ATOMS = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
)
R279_EDGES = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz"
)
R279_VERIFICATION = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_verification.json"
)
R280_RESULT = (
    "cm2_round280_source_g_expanded_occurrence_identity_contract_audit_"
    "result.json"
)
R288_DISPOSITIONS = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "atom_dispositions.json.gz"
)
R288_VERIFICATION = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "verification.json"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R294_RESULT = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
)
R294_VERIFICATION = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "verification.json"
)
R295A_RESULT = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "result.json"
)
R295A_VERIFICATION = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "verification.json"
)
R295B_RESULT = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_result.json"
)
R295B_VERIFICATION = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_"
    "verification.json"
)

EXPECTED_TABLES = {
    "R266_COMPONENT": (
        63_224,
        "post_Round266_component_frontier_row_id",
        "bfdf5cde6fc68d39676e1543a6138672e7b8a68424280c6f895a8408f3eb579d",
    ),
    "R266_MEMBER": (
        259_752,
        "post_Round266_component_member_frontier_row_id",
        "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
    ),
    "R279_ATOM": (
        332_016,
        "canonical_atom_id",
        "d2680baed100e4e1a236aa929999c7d93be5eeddabb2cc0660fca5e756882105",
    ),
    "R279_EDGE": (
        330_724,
        "formal_face_edge_witness_row_id",
        "bfcb9979545b6abb2e85d54e0200f4394b6e967dbb888e3bcda7ee726cdc6bf7",
    ),
    "R288_DISPOSITION": (
        332_016,
        "Round288_atom_disposition_row_id",
        "8007b0c96e44c76bea6038fed8430134f9f424c7a81508f843d72d473f768849",
    ),
    "R294_REGISTRY": (
        431_208,
        "Round294_occurrence_registry_row_id",
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    ),
}


class VerificationError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def guard_regular_path(
    path: Path,
    expected_name: str,
    allowed_parent: Path = HERE,
) -> None:
    need(
        path.name == expected_name
        and path.parent == allowed_parent
        and not path.is_symlink(),
        "confined non-symlink path:" + expected_name,
    )
    try:
        status = os.lstat(path)
    except FileNotFoundError as error:
        raise VerificationError(
            "missing guarded path:" + expected_name
        ) from error
    need(
        stat.S_ISREG(status.st_mode)
        and status.st_nlink == 1
        and path.resolve(strict=True).parent
        == allowed_parent.resolve(strict=True),
        "regular single-link confined file:" + expected_name,
    )


def close(payload: dict[str, Any]) -> dict[str, Any]:
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def verify_row(row: dict[str, Any], label: str) -> None:
    payload = {key: value for key, value in row.items() if key != "row_sha256"}
    need(
        set(row) == set(payload) | {"row_sha256"}
        and row["row_sha256"] == digest(payload),
        label + ":row closure",
    )


def verify_result(value: dict[str, Any], field: str, label: str) -> None:
    claim = value[field]
    payload = {key: child for key, child in value.items() if key != field}
    need(claim == digest(payload), label + ":result closure")


def read_json(filename: str) -> dict[str, Any]:
    with (HERE / filename).open("rb") as handle:
        value = json.load(handle)
    need(isinstance(value, dict), filename + ":JSON object")
    return value


def verify_manifest_packages() -> dict[str, str]:
    expanded: dict[str, str] = {}
    pattern = re.compile(r"^([0-9a-f]{64})  ([^/\\\\]+)$")
    for manifest_name, manifest_pin in sorted(
        PACKAGE_MANIFEST_PINS.items()
    ):
        need("PENDING_" not in manifest_pin, "pending manifest pin")
        path = HERE / manifest_name
        guard_regular_path(path, manifest_name)
        need(
            file_sha256(path) == manifest_pin,
            "manifest pin:" + manifest_name,
        )
        lines = path.read_text(encoding="ascii").splitlines()
        need(lines and len(lines) == len(set(lines)), "manifest lines")
        for line in lines:
            match = pattern.fullmatch(line)
            need(match is not None, "manifest syntax")
            expected, filename = match.groups()
            member = HERE / filename
            guard_regular_path(member, filename)
            need(
                file_sha256(member) == expected,
                "manifest member:" + filename,
            )
            if filename in expanded:
                need(expanded[filename] == expected, "consistent pin")
            expanded[filename] = expected
        expanded[manifest_name] = manifest_pin
    for filename in (
        R266_CERT,
        R266_VERIFICATION,
        R279_ATOMS,
        R279_EDGES,
        R279_VERIFICATION,
        R280_RESULT,
        R288_DISPOSITIONS,
        R288_VERIFICATION,
        R294_REGISTRY,
        R294_RESULT,
        R294_VERIFICATION,
        R295A_RESULT,
        R295A_VERIFICATION,
        R295B_RESULT,
        R295B_VERIFICATION,
    ):
        need(filename in expanded, "sealed required input:" + filename)
    return expanded


class ListHasher:
    def __init__(self) -> None:
        self.value = hashlib.sha256()
        self.value.update(b"[")
        self.count = 0

    def add_bytes(self, payload: bytes) -> None:
        if self.count:
            self.value.update(b",")
        self.value.update(payload)
        self.count += 1

    def add(self, payload: Any) -> None:
        self.add_bytes(canonical(payload))

    def finish(self) -> str:
        self.value.update(b"]")
        return self.value.hexdigest()


def no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key:" + key)
        result[key] = value
    return result


def iterate_array(
    stream: TextIO,
    marker: str = '"rows":[',
    strict_duplicates: bool = False,
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        chunk = stream.read(1 << 20)
        need(bool(chunk), "array marker")
        buffer += chunk
        if len(buffer) > 2 * (1 << 20):
            buffer = buffer[-(len(marker) + (1 << 20)):]
    buffer = buffer.split(marker, 1)[1]
    decoder = json.JSONDecoder(
        object_pairs_hook=no_duplicate_pairs if strict_duplicates else None
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            chunk = stream.read(1 << 20)
            need(bool(chunk), "unexpected array EOF")
            buffer = chunk
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                chunk = stream.read(1 << 20)
                need(bool(chunk), "malformed streamed row")
                buffer += chunk
        need(isinstance(value, dict), "row object")
        yield value
        buffer = buffer[end:]


def gzip_rows(
    filename: str,
    strict_duplicates: bool = False,
) -> Iterator[dict[str, Any]]:
    with gzip.open(HERE / filename, "rt", encoding="utf-8") as handle:
        yield from iterate_array(handle, strict_duplicates=strict_duplicates)


def r266_rows(table_name: str) -> Iterator[dict[str, Any]]:
    path = HERE / R266_CERT
    marker = ('"' + table_name + '":').encode()
    with path.open("rb") as handle:
        mapped = mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ)
        table_offset = mapped.find(marker)
        rows_offset = mapped.find(b'"rows":[', table_offset)
        mapped.close()
    need(table_offset >= 0 and rows_offset >= 0, "Round266 table marker")
    with path.open("rt", encoding="utf-8") as handle:
        handle.seek(rows_offset)
        yield from iterate_array(handle)


def audit_rows(
    rows: Iterable[dict[str, Any]],
    label: str,
    consume: Callable[[dict[str, Any]], None],
) -> None:
    expected_count, id_key, expected_sha = EXPECTED_TABLES[label]
    rows_hash = ListHasher()
    ids: set[str] = set()
    count = 0
    for row in rows:
        verify_row(row, label)
        row_id = row[id_key]
        need(row_id not in ids, label + ":unique ID")
        ids.add(row_id)
        rows_hash.add_bytes(canonical(row))
        consume(row)
        count += 1
    need(
        count == expected_count
        and rows_hash.finish() == expected_sha,
        label + ":complete rows commitment",
    )


class DSU:
    def __init__(self, nodes: Iterable[str]) -> None:
        nodes = set(nodes)
        self.parent = {node: node for node in nodes}
        self.size = {node: 1 for node in nodes}
        self.rank = 0

    def find(self, node: str) -> str:
        need(node in self.parent, "DSU node")
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, left: str, right: str) -> None:
        left, right = self.find(left), self.find(right)
        if left == right:
            return
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        self.rank += 1

    def count(self) -> int:
        return sum(node == parent for node, parent in self.parent.items())


def reconstruct_context_seals() -> dict[str, Any]:
    r266_verification = read_json(R266_VERIFICATION)
    r279_verification = read_json(R279_VERIFICATION)
    need(
        r266_verification["status"] == "PASS_INDEPENDENT_ROUND266"
        and r279_verification["status"] == "PASS_INDEPENDENT_ROUND279",
        "Round266/Round279 independent verification seals",
    )
    r280 = read_json(R280_RESULT)
    need(
        r280["result_sha256"] == digest(r280["result"]),
        "Round280 result closure",
    )
    need(
        r280["result"]["verdict"][
            "Round280_connected_class_is_one_occurrence_claim"
        ] == "REJECTED_BY_FROZEN_ROUND265_ROUND266_CONTRACT"
        and r280["result"]["deterministic_identity_rule"][
            "identity_alias_rule"
        ].startswith("Collapse identities only under an explicit exact"),
        "Round280 corrected identity contract",
    )
    r294 = read_json(R294_RESULT)
    verify_result(r294, "result_sha256", "Round294")
    need(
        r294["census"]["formal_occurrence_registry_row_count"] == 431_208
        and r294["census"]["formal_new_Round288_atom_occurrence_count"]
        == 295_336
        and r294["census"]["formal_new_refined_Round287_occurrence_count"]
        == 9_404
        and r294["nonpromotion_freeze"][
            "post_Round294_quotient_component_count"
        ] is None,
        "Round294 registry seal",
    )
    r288_verification = read_json(R288_VERIFICATION)
    r294_verification = read_json(R294_VERIFICATION)
    verify_result(
        r288_verification, "verification_sha256", "Round288 verification"
    )
    verify_result(
        r294_verification, "verification_sha256", "Round294 verification"
    )
    need(
        r288_verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND288"
        )
        and r294_verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "Round288/Round294 independent verification seals",
    )
    r295a = read_json(R295A_RESULT)
    verify_result(r295a, "result_sha256", "Round295-A")
    need(
        r295a["formal_credit_transition"][
            "formal_expanded_occurrence_count"
        ] == 431_208
        and r295a["formal_credit_transition"][
            "formal_new_expanded_occurrence_credit"
        ] == 0
        and r295a["post_Round295A_nonpromotion_freeze"][
            "post_Round294_component_DSU_status"
        ] == "NOT_REBUILT",
        "Round295-A no-new-ID seal",
    )
    r295b = read_json(R295B_RESULT)
    verify_result(r295b, "result_sha256", "Round295-B")
    need(
        r295b["Round294_registry_contract"][
            "post_Round295B_registry_row_count"
        ] == 431_208
        and r295b["Round294_registry_contract"][
            "Round295B_added_occurrence_ID_count"
        ] == 0
        and r295b["strict_nonpromotion"][
            "post_Round294_expanded_registry_component_DSU_status"
        ] == "NOT_REBUILT",
        "Round295-B no-new-ID seal",
    )
    r295a_verification = read_json(R295A_VERIFICATION)
    r295b_verification = read_json(R295B_VERIFICATION)
    verify_result(
        r295a_verification,
        "verification_sha256",
        "Round295-A verification",
    )
    verify_result(
        r295b_verification,
        "verification_sha256",
        "Round295-B verification",
    )
    need(
        r295a_verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295A"
        )
        and r295b_verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295B"
        ),
        "Round295-A/B independent verification seals",
    )
    return {
        "Round280_result_sha256": r280["result_sha256"],
        "Round294_result_sha256": r294["result_sha256"],
        "Round295A_result_sha256": r295a["result_sha256"],
        "Round295B_result_sha256": r295b["result_sha256"],
    }


def reconstruct_r266() -> tuple[
    set[str],
    dict[str, dict[str, Any]],
    Counter[str],
]:
    roots: set[str] = set()

    def component(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        need(
            root not in roots
            and row["certified_known_connectivity_only"]
            and not row["maximal_physical_component_claimed"],
            "independent Round266 component",
        )
        roots.add(root)

    audit_rows(
        r266_rows("formal_post_Round266_component_frontier_ledger"),
        "R266_COMPONENT",
        component,
    )
    occurrence_root: dict[str, dict[str, Any]] = {}
    kinds: Counter[str] = Counter()

    def member(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        need(
            root in roots
            and row["member_identity_preserved"]
            and row["maximality_credit"] == 0,
            "independent Round266 member",
        )
        kind = row["component_member_kind"]
        kinds[kind] += 1
        if kind == "EXPANDED_OCCURRENCE":
            occurrence = row["component_member_id"]
            need(occurrence not in occurrence_root, "unique old occurrence")
            occurrence_root[occurrence] = {
                "root": root,
                "member_row_id":
                    row[
                        "post_Round266_component_member_frontier_row_id"
                    ],
                "member_row_sha256": row["row_sha256"],
            }

    audit_rows(
        r266_rows(
            "formal_post_Round266_component_member_frontier_ledger"
        ),
        "R266_MEMBER",
        member,
    )
    need(
        len(roots) == 63_224
        and len(occurrence_root) == 126_468
        and kinds
        == {
            "EXPANDED_OCCURRENCE": 126_468,
            "VALID_VIRTUAL_STRATUM": 133_284,
        },
        "independent complete old frontier",
    )
    return roots, occurrence_root, kinds


def reconstruct_registry() -> tuple[
    dict[str, dict[str, Any]],
    Counter[str],
]:
    registry: dict[str, dict[str, Any]] = {}
    kinds: Counter[str] = Counter()

    def consume(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        need(
            occurrence not in registry
            and row["registry_promotion_status"]
            == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY",
            "independent Round294 registry row",
        )
        kind = row["registry_entry_kind"]
        kinds[kind] += 1
        registry[occurrence] = {
            "registry_row_id": row["Round294_occurrence_registry_row_id"],
            "registry_row_sha256": row["row_sha256"],
            "kind": kind,
            "source_identity": row["registry_source_identity"],
            "signature":
                row["complete_10_field_return_signature_sha256"],
            "key": row["official_key_id"],
            "ordinal": row["official_key_ordinal"],
        }

    audit_rows(gzip_rows(R294_REGISTRY), "R294_REGISTRY", consume)
    need(
        kinds
        == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT":
                9_404,
        },
        "independent registry tranches",
    )
    return registry, kinds


def reconstruct_atoms(
    registry: dict[str, dict[str, Any]],
    old_roots: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], Counter[str]]:
    atoms: dict[str, dict[str, Any]] = {}
    targets: set[str] = set()
    dispositions: Counter[str] = Counter()

    def disposition(row: dict[str, Any]) -> None:
        atom = row["canonical_atom_id"]
        existing = row["existing_local_occurrence_row_id"]
        target = (
            existing
            or row["reserved_candidate_occurrence_id__not_issued"]
        )
        need(
            atom not in atoms
            and target in registry
            and target not in targets,
            "independent distinct atom target",
        )
        targets.add(target)
        if existing:
            provenance = "PRESERVED_ROUND266_OCCURRENCE_ALIAS"
            kind = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
            need(target in old_roots, "old occurrence root")
        else:
            provenance = "PROMOTED_ROUND288_CANONICAL_ATOM_OCCURRENCE"
            kind = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
            need(target not in old_roots, "new occurrence singleton")
        registration = registry[target]
        need(
            registration["kind"] == kind
            and registration["signature"]
            == row["complete_10_field_return_signature_sha256"]
            and registration["key"] == row["official_key_id"]
            and registration["ordinal"] == row["official_key_ordinal"],
            "independent R288/R294 join",
        )
        dispositions[provenance] += 1
        atoms[atom] = {
            "target": target,
            "provenance": provenance,
            "disposition_row_id":
                row["Round288_atom_disposition_row_id"],
            "disposition_row_sha256": row["row_sha256"],
            "signature":
                row["complete_10_field_return_signature_sha256"],
            "leaf": row["Round182_leaf_row_id"],
            "key": row["official_key_id"],
            "ordinal": row["official_key_ordinal"],
            **registration,
        }

    audit_rows(
        gzip_rows(R288_DISPOSITIONS),
        "R288_DISPOSITION",
        disposition,
    )
    need(
        len(atoms) == len(targets) == 332_016
        and dispositions
        == {
            "PROMOTED_ROUND288_CANONICAL_ATOM_OCCURRENCE": 295_336,
            "PRESERVED_ROUND266_OCCURRENCE_ALIAS": 36_680,
        },
        "independent atom target census",
    )
    seen: set[str] = set()

    def atom_source(row: dict[str, Any]) -> None:
        atom = row["canonical_atom_id"]
        need(atom in atoms and atom not in seen, "independent atom source")
        seen.add(atom)
        expected = atoms[atom]
        signature = row["complete_10_field_return_signature"]
        need(
            expected["signature"]
            == row["complete_10_field_return_signature_sha256"]
            and expected["leaf"] == row["Round182_leaf_row_id"]
            and expected["key"] == signature["official_key_id"]
            and expected["ordinal"] == signature["official_key_ordinal"]
            and row["expanded_occurrence_credit"] == 0
            and row["component_credit"] == 0
            and row["maximality_credit"] == 0,
            "independent atom signature/provenance",
        )
        anchors = row["existing_Round208_occurrence_row_ids"]
        if anchors:
            need(
                len(anchors) == 1 and anchors[0] == expected["target"],
                "independent old anchor",
            )
        expected["atom_row_sha256"] = row["row_sha256"]
        expected["atom_source_chart"] = row["source_chart"]
        expected["atom_owner_target"] = row["owner_target"]
        expected["atom_source_signature_row_ids"] = (
            row["source_signature_row_ids"]
        )
        expected["atom_support_classification"] = (
            row["support_classification"]
        )

    audit_rows(gzip_rows(R279_ATOMS), "R279_ATOM", atom_source)
    need(seen == set(atoms), "complete independent atom source join")
    return atoms, dispositions


def independently_validate_face(row: dict[str, Any]) -> None:
    axis = row["common_face_axis"]
    need(axis in {0, 1, 2}, "independent face axis")
    coordinate = Q(row["common_face_coordinate"])
    face = tuple(map(Q, row["exact_positive_area_face_patch"]))
    need(
        len(face) == 6
        and face[2 * axis] == face[2 * axis + 1] == coordinate,
        "independent exact face",
    )
    tangential = [value for value in range(3) if value != axis]
    overlap = row["candidate_overlap_rectangle"]
    need(len(overlap) == 2, "independent overlap rectangle")
    for slot, other_axis in enumerate(tangential):
        interval = tuple(map(Q, overlap[slot]))
        need(
            interval[0] < interval[1]
            and interval[0] <= face[2 * other_axis]
            < face[2 * other_axis + 1] <= interval[1],
            "independent positive refined tangential subinterval",
        )
    corridors = row["two_inward_corridors"]
    need(
        len(corridors) == 2
        and [value["geometric_side"] for value in corridors]
        == ["NEGATIVE_SIDE_INWARD", "POSITIVE_SIDE_INWARD"],
        "independent ordered corridors",
    )
    for side_index, corridor in enumerate(corridors):
        box = tuple(map(Q, corridor["exact_corridor_box"]))
        need(
            len(box) == 6
            and all(
                box[2 * value] < box[2 * value + 1]
                for value in range(3)
            )
            and box[2 * axis + (1 if side_index == 0 else 0)]
            == coordinate,
            "independent inward corridor",
        )
        for other_axis in tangential:
            need(
                box[2 * other_axis:2 * other_axis + 2]
                == face[2 * other_axis:2 * other_axis + 2],
                "independent corridor footprint",
            )


def expected_endpoint(
    atom_id: str,
    endpoint: dict[str, Any],
    atom: dict[str, Any],
    old_roots: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    occurrence = atom["target"]
    old = old_roots.get(occurrence)
    return {
        "geometric_side": endpoint["geometric_side"],
        "canonical_atom_id": atom_id,
        "Round182_leaf_row_id": endpoint["leaf_row_id"],
        "Round279_atom_row_sha256": atom["atom_row_sha256"],
        "Round279_atom_source_signature_row_ids":
            atom["atom_source_signature_row_ids"],
        "Round279_atom_support_classification":
            atom["atom_support_classification"],
        "Round288_atom_disposition_row_id":
            atom["disposition_row_id"],
        "Round288_atom_disposition_row_sha256":
            atom["disposition_row_sha256"],
        "formal_Round294_occurrence_id": occurrence,
        "Round294_occurrence_registry_row_id": atom["registry_row_id"],
        "Round294_occurrence_registry_row_sha256":
            atom["registry_row_sha256"],
        "Round294_registry_entry_kind": atom["kind"],
        "occurrence_identity_provenance": atom["provenance"],
        "official_key_id": atom["key"],
        "official_key_ordinal": atom["ordinal"],
        "complete_10_field_return_signature_sha256": atom["signature"],
        "pre_ordinary_component_root_id":
            old["root"] if old else occurrence,
        "pre_ordinary_component_root_kind": (
            "RETAINED_ROUND266_COMPONENT_ROOT"
            if old
            else "ROUND294_NEW_OCCURRENCE_SINGLETON_ROOT"
        ),
        "Round266_component_member_frontier_row_id":
            old["member_row_id"] if old else None,
        "Round266_component_member_frontier_row_sha256":
            old["member_row_sha256"] if old else None,
    }


def write_streamed_ledger(
    rows_path: Path,
    metadata: dict[str, Any],
    destination: Path,
) -> None:
    with destination.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, mtime=0
        ) as output:
            output.write(b"{")
            keys = sorted(set(metadata) | {"rows"})
            for index, key in enumerate(keys):
                if index:
                    output.write(b",")
                output.write(canonical(key) + b":")
                if key != "rows":
                    output.write(canonical(metadata[key]))
                    continue
                output.write(b"[")
                with rows_path.open("rb") as rows:
                    first = True
                    for line in rows:
                        if not first:
                            output.write(b",")
                        output.write(line.rstrip(b"\n"))
                        first = False
                output.write(b"]")
            output.write(b"}")


def independently_reconstruct_edges(
    atoms: dict[str, dict[str, Any]],
    old_roots: dict[str, dict[str, Any]],
    base_roots: set[str],
    rows_path: Path,
    ledger_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    dsu = DSU(base_roots)
    occurrence_pairs: set[tuple[str, str]] = set()
    root_pairs: set[tuple[str, str]] = set()
    source_ids: set[str] = set()
    output_ids: set[str] = set()
    indices: set[int] = set()
    pre_same = 0
    count = 0
    rows_hash = ListHasher()
    ids_hash = ListHasher()
    hashes_hash = ListHasher()
    source_hash = ListHasher()
    occurrence_pair_hash = ListHasher()
    root_pair_hash = ListHasher()
    sample: dict[str, Any] | None = None

    with rows_path.open("wb") as staged:
        def consume(source: dict[str, Any]) -> None:
            nonlocal count, pre_same, sample
            need(
                source["candidate_index"] == count
                and source["candidate_index"] not in indices,
                "independent candidate index",
            )
            indices.add(source["candidate_index"])
            source_id = source["formal_face_edge_witness_row_id"]
            need(source_id not in source_ids, "independent source edge ID")
            source_ids.add(source_id)
            need(
                source["component_edge_credit"] == 0
                and source["expanded_occurrence_credit"] == 0
                and source["maximality_credit"] == 0,
                "independent frozen Round279 edge credit",
            )
            independently_validate_face(source)
            raw_endpoints = source["endpoint_atoms"]
            need(
                len(raw_endpoints) == 2
                and [value["geometric_side"] for value in raw_endpoints]
                == ["NEGATIVE", "POSITIVE"],
                "independent ordered endpoints",
            )
            atom_ids = [
                value["canonical_atom_id"] for value in raw_endpoints
            ]
            need(
                atom_ids[0] != atom_ids[1]
                and all(value in atoms for value in atom_ids),
                "independent atom endpoints",
            )
            for endpoint_index, atom_id in enumerate(atom_ids):
                joined_atom = atoms[atom_id]
                need(
                    raw_endpoints[endpoint_index]["leaf_row_id"]
                    == joined_atom["leaf"]
                    and source["two_inward_corridors"][
                        endpoint_index
                    ]["leaf_row_id"]
                    == raw_endpoints[endpoint_index]["leaf_row_id"]
                    and joined_atom["atom_source_chart"]
                    == source["source_chart"]
                    and joined_atom["atom_owner_target"]
                    == source["owner_target"],
                    "independent edge/atom/corridor provenance join",
                )
            endpoints = [
                expected_endpoint(
                    atom_id, endpoint, atoms[atom_id], old_roots
                )
                for atom_id, endpoint in zip(
                    atom_ids, raw_endpoints, strict=True
                )
            ]
            signature = source[
                "complete_10_field_return_signature_sha256"
            ]
            need(
                endpoints[0][
                    "complete_10_field_return_signature_sha256"
                ]
                == endpoints[1][
                    "complete_10_field_return_signature_sha256"
                ]
                == signature
                and endpoints[0]["official_key_id"]
                == endpoints[1]["official_key_id"]
                and endpoints[0]["official_key_ordinal"]
                == endpoints[1]["official_key_ordinal"],
                "independent edge signature/key",
            )
            occurrence_pair = tuple(sorted(
                value["formal_Round294_occurrence_id"]
                for value in endpoints
            ))
            need(
                occurrence_pair[0] != occurrence_pair[1]
                and occurrence_pair not in occurrence_pairs,
                "independent unique nonself occurrence pair",
            )
            occurrence_pairs.add(occurrence_pair)
            root_pair = tuple(sorted(
                value["pre_ordinary_component_root_id"]
                for value in endpoints
            ))
            need(
                root_pair[0] in base_roots
                and root_pair[1] in base_roots,
                "independent base root pair",
            )
            root_pairs.add(root_pair)
            same = root_pair[0] == root_pair[1]
            pre_same += int(same)
            dsu.union(*root_pair)
            row_id = (
                "round297-ordinary-face-occurrence-edge:"
                + digest([source_id, list(occurrence_pair)])
            )
            need(
                row_id not in output_ids,
                "independent unique Round297 output row ID",
            )
            output_ids.add(row_id)
            row = close({
                "Round297_ordinary_face_occurrence_edge_row_id": row_id,
                "source_Round279_face_edge_witness_row_id": source_id,
                "source_Round279_face_edge_row_sha256":
                    source["row_sha256"],
                "source_candidate_index": source["candidate_index"],
                "source_witness_partition": source["witness_partition"],
                "source_chart": source["source_chart"],
                "owner_target": source["owner_target"],
                "official_key_id": endpoints[0]["official_key_id"],
                "official_key_ordinal":
                    endpoints[0]["official_key_ordinal"],
                "complete_10_field_return_signature_sha256": signature,
                "common_face_axis": source["common_face_axis"],
                "common_face_coordinate":
                    source["common_face_coordinate"],
                "candidate_overlap_rectangle":
                    source["candidate_overlap_rectangle"],
                "exact_positive_area_face_patch":
                    source["exact_positive_area_face_patch"],
                "two_inward_corridors": source["two_inward_corridors"],
                "endpoint_occurrences": endpoints,
                "exact_occurrence_endpoint_pair": list(occurrence_pair),
                "occurrence_endpoint_pair_is_nonself": True,
                "pre_ordinary_component_root_pair": list(root_pair),
                "pre_ordinary_same_component_root": same,
                "edge_semantics":
                    "ORDINARY_POSITIVE_AREA_COMMON_FACE__"
                    "COMPONENT_CONNECTIVITY_NOT_OCCURRENCE_IDENTITY",
                "formal_ordinary_component_edge_witness_credit": 1,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_occurrence_alias_credit": 0,
                "formal_new_occurrence_ID_credit": 0,
                "formal_representation_alias_credit": 0,
                "formal_seam_edge_credit": 0,
                "formal_Jx_Jy_same_point_glue_credit": 0,
                "formal_component_union_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
                "post_Round297_quotient_component_id": None,
            })
            if sample is None:
                sample = deepcopy(row)
            encoded = canonical(row)
            staged.write(encoded + b"\n")
            rows_hash.add_bytes(encoded)
            ids_hash.add(row_id)
            hashes_hash.add(row["row_sha256"])
            source_hash.add(source_id)
            occurrence_pair_hash.add(list(occurrence_pair))
            root_pair_hash.add(list(root_pair))
            count += 1

        audit_rows(gzip_rows(R279_EDGES), "R279_EDGE", consume)
    need(
        count == len(indices) == len(source_ids) == len(output_ids)
        == len(occurrence_pairs) == 330_724
        and indices == set(range(330_724))
        and len(root_pairs) == 316_728
        and pre_same == 14_464
        and dsu.rank == 221_916
        and dsu.count() == 146_048
        and sample is not None,
        "independent exact ordinary edge/DSU census",
    )
    metadata = {
        "schema": LEDGER_SCHEMA,
        "status": (
            "PASS_ROUND297_330724_ORDINARY_FACE_OCCURRENCE_"
            "COMPONENT_EDGE_WITNESSES__ZERO_IDENTITY_COLLAPSE__"
            "ZERO_DSU_RANK_CREDIT"
        ),
        "row_order":
            "SOURCE_ROUND279_CANDIDATE_INDEX_ASCENDING_0_TO_330723",
        "row_count": count,
        "rows_sha256": rows_hash.finish(),
        "row_ids_sha256": ids_hash.finish(),
        "row_hashes_sha256": hashes_hash.finish(),
        "source_edge_ids_sha256": source_hash.finish(),
        "ordered_occurrence_endpoint_pairs_sha256":
            occurrence_pair_hash.finish(),
        "ordered_pre_ordinary_root_pairs_sha256":
            root_pair_hash.finish(),
        "all_occurrence_endpoint_pairs_unique": True,
        "all_occurrence_endpoint_pairs_nonself": True,
        "formal_ordinary_component_edge_witness_credit_sum": 330_724,
    }
    write_streamed_ledger(rows_path, metadata, ledger_path)
    audit = {
        "ordinary_edge_row_count": count,
        "distinct_occurrence_endpoint_pair_count": len(occurrence_pairs),
        "self_occurrence_endpoint_pair_count": 0,
        "distinct_pre_ordinary_component_root_pair_count":
            len(root_pairs),
        "pre_same_component_root_witness_row_count": pre_same,
        "ordinary_edge_application_rank_reduction": dsu.rank,
        "ordinary_only_candidate_component_count": dsu.count(),
    }
    return metadata, audit, sample


def build_expected_result(
    expanded_pins: dict[str, str],
    context: dict[str, Any],
    registry_kinds: Counter[str],
    member_kinds: Counter[str],
    atom_dispositions: Counter[str],
    ledger_metadata: dict[str, Any],
    edge_audit: dict[str, Any],
    expected_ledger_path: Path,
) -> dict[str, Any]:
    ledger_sha = file_sha256(expected_ledger_path)
    result = {
        "schema": SCHEMA,
        "status": (
            "PASS_ROUND297_ORDINARY_FACE_OCCURRENCE_EDGE_PROMOTION__"
            "330724_FORMAL_COMPONENT_EDGE_WITNESSES__"
            "IDENTITIES_AND_REGISTRY_UNCHANGED__CURRENT_QUOTIENT_NULL"
        ),
        "input_package_manifest_pins":
            dict(sorted(PACKAGE_MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(expanded_pins.items())),
        "sealed_context_result_sha256": context,
        "identity_and_registry_reconstruction": {
            "Round279_canonical_atom_count": 332_016,
            "distinct_formal_Round294_atom_target_count": 332_016,
            "promoted_Round288_new_atom_occurrence_count": 295_336,
            "preserved_Round266_occurrence_alias_target_count": 36_680,
            "all_atom_targets_pairwise_distinct": True,
            "formal_Round294_registry_row_count": 431_208,
            "Round294_registry_tranche_counts": {
                key: value for key, value in sorted(registry_kinds.items())
            },
            "Round295A_added_occurrence_ID_count": 0,
            "Round295B_added_occurrence_ID_count": 0,
            "post_Round297_registry_row_count": 431_208,
            "Round297_added_occurrence_ID_count": 0,
            "Round297_added_occurrence_identity_alias_count": 0,
            "Round297_added_representation_alias_count": 0,
            "atom_identity_disposition_counts": {
                key: value
                for key, value in sorted(atom_dispositions.items())
            },
        },
        "retained_Round266_component_member_frontier": {
            "retained_component_root_count": 63_224,
            "retained_component_member_count": 259_752,
            "retained_expanded_occurrence_member_count": 126_468,
            "retained_valid_virtual_stratum_member_count": 133_284,
            "complete_old_member_frontier_preserved": True,
            "old_occurrence_member_identities_preserved": True,
            "old_virtual_member_identities_preserved": True,
            "Round266_component_frontier_rows_sha256":
                EXPECTED_TABLES["R266_COMPONENT"][2],
            "Round266_component_member_frontier_rows_sha256":
                EXPECTED_TABLES["R266_MEMBER"][2],
            "member_kind_histogram": {
                key: value for key, value in sorted(member_kinds.items())
            },
        },
        "ordinary_face_edge_promotion": {
            "source_Round279_face_edge_count": 330_724,
            "promoted_ordinary_component_edge_witness_count": 330_724,
            "distinct_occurrence_endpoint_pair_count":
                edge_audit["distinct_occurrence_endpoint_pair_count"],
            "self_occurrence_endpoint_pair_count": 0,
            "all_source_edge_IDs_preserved": True,
            "all_exact_faces_and_corridors_preserved": True,
            "all_signature_key_and_endpoint_provenance_preserved": True,
            "ordinary_common_face_is_component_connectivity": True,
            "ordinary_common_face_is_occurrence_identity": False,
        },
        "ordinary_only_nonpromotion_cross_audit": {
            "retained_Round266_component_root_count": 63_224,
            "new_Round288_atom_singleton_root_count": 295_336,
            "new_Round292_refined_singleton_root_count": 9_404,
            "base_root_count": 367_964,
            "distinct_component_root_endpoint_pair_count":
                edge_audit[
                    "distinct_pre_ordinary_component_root_pair_count"
                ],
            "pre_same_component_root_witness_row_count":
                edge_audit[
                    "pre_same_component_root_witness_row_count"
                ],
            "ordinary_edge_application_rank_reduction":
                edge_audit["ordinary_edge_application_rank_reduction"],
            "ordinary_only_candidate_component_count":
                edge_audit["ordinary_only_candidate_component_count"],
            "cross_audit_is_next_DSU_input_only": True,
            "cross_audit_promoted_to_current_quotient": False,
            "cross_audit_rank_reduction_credit": 0,
        },
        "formal_credit_transition": {
            "formal_ordinary_component_edge_witness_credit": 330_724,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_new_occurrence_ID_credit": 0,
            "formal_representation_alias_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "edge_ledger": {
            "filename": LEDGER.name,
            "file_sha256": ledger_sha,
            **{
                key: ledger_metadata[key]
                for key in (
                    "row_count",
                    "rows_sha256",
                    "row_ids_sha256",
                    "row_hashes_sha256",
                    "source_edge_ids_sha256",
                    "ordered_occurrence_endpoint_pairs_sha256",
                    "ordered_pre_ordinary_root_pairs_sha256",
                )
            },
        },
        "strict_nonpromotion": {
            "post_Round297_quotient_component_count": None,
            "post_Round297_expanded_registry_component_DSU_status":
                "NOT_REBUILT",
            "ordinary_only_candidate_component_count_is_current_quotient":
                False,
            "legacy_pre_Round294_quotient_component_count": 63_224,
            "legacy_63224_is_current_post_Round297_count": False,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result["result_sha256"] = digest(result)
    return result


def strict_json_bytes(payload: bytes) -> dict[str, Any]:
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=no_duplicate_pairs,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("strict candidate JSON") from error
    need(isinstance(value, dict), "candidate JSON object")
    return value


def files_equal(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as first, right.open("rb") as second:
        while True:
            a = first.read(1 << 20)
            b = second.read(1 << 20)
            if a != b:
                return False
            if not a:
                return True


def audit_candidate(
    expected_result: dict[str, Any],
    expected_rows_path: Path,
    expected_ledger_path: Path,
) -> None:
    guard_regular_path(RESULT, RESULT.name)
    guard_regular_path(LEDGER, LEDGER.name)
    result_bytes = RESULT.read_bytes()
    result = strict_json_bytes(result_bytes)
    verify_result(result, "result_sha256", "candidate Round297")
    need(
        Path(result["edge_ledger"]["filename"]).name
        == result["edge_ledger"]["filename"]
        and "/" not in result["edge_ledger"]["filename"]
        and "\\" not in result["edge_ledger"]["filename"],
        "candidate confined ledger basename",
    )
    need(
        result == expected_result
        and result_bytes == canonical(expected_result) + b"\n",
        "candidate result equals independent reconstruction",
    )
    need(
        file_sha256(LEDGER) == file_sha256(expected_ledger_path)
        == result["edge_ledger"]["file_sha256"]
        and files_equal(LEDGER, expected_ledger_path),
        "candidate deterministic gzip equals reconstruction",
    )
    count = 0
    with expected_rows_path.open("rb") as expected_rows:
        for candidate in gzip_rows(
            LEDGER.name, strict_duplicates=True
        ):
            expected_line = expected_rows.readline().rstrip(b"\n")
            need(bool(expected_line), "candidate has excess row")
            verify_row(candidate, "candidate edge")
            need(
                canonical(candidate) == expected_line,
                "candidate row differs from reconstruction",
            )
            count += 1
        need(
            not expected_rows.readline()
            and count == 330_724,
            "candidate complete edge rows",
        )


def reclose_result(value: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(value)
    value.pop("result_sha256", None)
    value["result_sha256"] = digest(value)
    return value


def reclose_row(value: dict[str, Any]) -> dict[str, Any]:
    payload = {
        key: child for key, child in deepcopy(value).items()
        if key != "row_sha256"
    }
    return close(payload)


def run_attacks(
    expected_result: dict[str, Any],
    sample_row: dict[str, Any],
    expected_ledger_path: Path,
) -> list[dict[str, str]]:
    attacks: list[dict[str, str]] = []

    def reject(
        attack_id: str,
        attack_class: str,
        action: Callable[[], None],
    ) -> None:
        try:
            action()
        except Exception:
            attacks.append({
                "attack_id": attack_id,
                "classification": attack_class,
                "disposition": "REJECTED",
            })
            return
        raise VerificationError("attack accepted:" + attack_id)

    def check_result(value: dict[str, Any]) -> None:
        verify_result(value, "result_sha256", "attack result")
        need(
            value["edge_ledger"]["filename"] == LEDGER.name
            and value == expected_result,
            "attack result exact semantics",
        )

    def result_attack(
        attack_id: str,
        path: tuple[str, ...],
        replacement: Any,
        attack_class: str = "RESIGNED_SEMANTIC_FORGERY",
    ) -> None:
        mutant = deepcopy(expected_result)
        cursor: dict[str, Any] = mutant
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        mutant = reclose_result(mutant)
        reject(
            attack_id, attack_class, lambda: check_result(mutant)
        )

    result_mutations = [
        (
            "A01_EDGE_CREDIT_OMISSION",
            ("formal_credit_transition",
             "formal_ordinary_component_edge_witness_credit"),
            330_723,
        ),
        (
            "A02_FACE_AS_IDENTITY_COLLAPSE",
            ("formal_credit_transition",
             "formal_occurrence_identity_collapse_credit"),
            1,
        ),
        (
            "A03_FACE_AS_OCCURRENCE_ALIAS",
            ("formal_credit_transition", "formal_occurrence_alias_credit"),
            1,
        ),
        (
            "A04_FACE_AS_NEW_ID",
            ("formal_credit_transition", "formal_new_occurrence_ID_credit"),
            1,
        ),
        (
            "A05_FACE_AS_REPRESENTATION_ALIAS",
            ("formal_credit_transition",
             "formal_representation_alias_credit"),
            1,
        ),
        (
            "A06_FORGED_SEAM_CREDIT",
            ("formal_credit_transition", "formal_seam_edge_credit"),
            1,
        ),
        (
            "A07_FORGED_JX_JY_GLUE",
            ("formal_credit_transition",
             "formal_Jx_Jy_same_point_glue_credit"),
            1,
        ),
        (
            "A08_PREMATURE_COMPONENT_UNION",
            ("formal_credit_transition", "formal_component_union_credit"),
            221_916,
        ),
        (
            "A09_PREMATURE_DSU_RANK",
            ("formal_credit_transition",
             "formal_DSU_rank_reduction_credit"),
            221_916,
        ),
        (
            "A10_FORGED_MAXIMALITY",
            ("formal_credit_transition", "formal_maximality_credit"),
            1,
        ),
        (
            "A11_FORGED_FIBRE",
            ("formal_credit_transition", "formal_fibre_credit"),
            1,
        ),
        (
            "A12_FORGED_GLOBAL_DISPOSITION",
            ("formal_credit_transition",
             "formal_global_disposition_credit"),
            1,
        ),
        (
            "A13_CANDIDATE_QUOTIENT_AS_CURRENT",
            ("strict_nonpromotion",
             "post_Round297_quotient_component_count"),
            146_048,
        ),
        (
            "A14_DSU_REBUILT_FORGERY",
            ("strict_nonpromotion",
             "post_Round297_expanded_registry_component_DSU_status"),
            "BUILT",
        ),
        (
            "A15_CANDIDATE_CURRENT_FLAG",
            ("strict_nonpromotion",
             "ordinary_only_candidate_component_count_is_current_quotient"),
            True,
        ),
        (
            "A16_LEGACY_63224_CURRENT",
            ("strict_nonpromotion",
             "legacy_63224_is_current_post_Round297_count"),
            True,
        ),
        (
            "A17_REGISTRY_INFLATION",
            ("identity_and_registry_reconstruction",
             "post_Round297_registry_row_count"),
            431_209,
        ),
        (
            "A18_NEW_ID_INFLATION",
            ("identity_and_registry_reconstruction",
             "Round297_added_occurrence_ID_count"),
            1,
        ),
        (
            "A19_ATOM_TARGET_COLLAPSE",
            ("identity_and_registry_reconstruction",
             "distinct_formal_Round294_atom_target_count"),
            332_015,
        ),
        (
            "A20_ATOM_TARGET_PAIRWISE_FLAG",
            ("identity_and_registry_reconstruction",
             "all_atom_targets_pairwise_distinct"),
            False,
        ),
        (
            "A21_OMIT_OLD_COMPONENT",
            ("retained_Round266_component_member_frontier",
             "retained_component_root_count"),
            63_223,
        ),
        (
            "A22_OMIT_OLD_MEMBER",
            ("retained_Round266_component_member_frontier",
             "retained_component_member_count"),
            259_751,
        ),
        (
            "A23_OMIT_VIRTUAL_MEMBERS",
            ("retained_Round266_component_member_frontier",
             "retained_valid_virtual_stratum_member_count"),
            0,
        ),
        (
            "A24_OLD_MEMBER_PRESERVATION_FALSE",
            ("retained_Round266_component_member_frontier",
             "complete_old_member_frontier_preserved"),
            False,
        ),
        (
            "A25_MISSING_OCCURRENCE_PAIR",
            ("ordinary_face_edge_promotion",
             "distinct_occurrence_endpoint_pair_count"),
            330_723,
        ),
        (
            "A26_SELF_OCCURRENCE_PAIR",
            ("ordinary_face_edge_promotion",
             "self_occurrence_endpoint_pair_count"),
            1,
        ),
        (
            "A27_COMMON_FACE_AS_IDENTITY",
            ("ordinary_face_edge_promotion",
             "ordinary_common_face_is_occurrence_identity"),
            True,
        ),
        (
            "A28_ROOT_PAIR_FORGERY",
            ("ordinary_only_nonpromotion_cross_audit",
             "distinct_component_root_endpoint_pair_count"),
            316_727,
        ),
        (
            "A29_PRE_SAME_ROOT_FORGERY",
            ("ordinary_only_nonpromotion_cross_audit",
             "pre_same_component_root_witness_row_count"),
            14_463,
        ),
        (
            "A30_RANK_FORGERY",
            ("ordinary_only_nonpromotion_cross_audit",
             "ordinary_edge_application_rank_reduction"),
            221_915,
        ),
        (
            "A31_COMPONENT_COUNT_FORGERY",
            ("ordinary_only_nonpromotion_cross_audit",
             "ordinary_only_candidate_component_count"),
            146_047,
        ),
        (
            "A32_CROSS_AUDIT_PROMOTION",
            ("ordinary_only_nonpromotion_cross_audit",
             "cross_audit_promoted_to_current_quotient"),
            True,
        ),
        (
            "A33_CROSS_AUDIT_RANK_CREDIT",
            ("ordinary_only_nonpromotion_cross_audit",
             "cross_audit_rank_reduction_credit"),
            221_916,
        ),
        (
            "A34_ABSOLUTE_LEDGER_PATH",
            ("edge_ledger", "filename"),
            "/tmp/" + LEDGER.name,
        ),
        (
            "A35_PARENT_LEDGER_PATH",
            ("edge_ledger", "filename"),
            "../" + LEDGER.name,
        ),
    ]
    for attack_id, path, replacement in result_mutations:
        result_attack(attack_id, path, replacement)

    def check_row(value: dict[str, Any]) -> None:
        verify_row(value, "attack row")
        need(value == sample_row, "attack row exact reconstruction")

    def row_attack(
        attack_id: str,
        mutate: Callable[[dict[str, Any]], None],
    ) -> None:
        mutant = deepcopy(sample_row)
        mutant.pop("row_sha256")
        mutate(mutant)
        mutant = close(mutant)
        reject(
            attack_id,
            "RESIGNED_SUBSTANTIVE_EDGE_ROW_FORGERY",
            lambda: check_row(mutant),
        )

    row_attack(
        "A36_SOURCE_EDGE_ID_SUBSTITUTION",
        lambda row: row.update({
            "source_Round279_face_edge_witness_row_id": "forged"
        }),
    )
    row_attack(
        "A37_SELF_ENDPOINT_SUBSTITUTION",
        lambda row: row["endpoint_occurrences"][1].update({
            "formal_Round294_occurrence_id":
                row["endpoint_occurrences"][0][
                    "formal_Round294_occurrence_id"
                ]
        }),
    )
    row_attack(
        "A38_FACE_COORDINATE_FORGERY",
        lambda row: row.update({"common_face_coordinate": "0"}),
    )
    row_attack(
        "A39_CORRIDOR_OMISSION",
        lambda row: row.update({"two_inward_corridors":
                                row["two_inward_corridors"][:1]}),
    )
    row_attack(
        "A40_SIGNATURE_SUBSTITUTION",
        lambda row: row.update({
            "complete_10_field_return_signature_sha256": "0" * 64
        }),
    )
    row_attack(
        "A41_KEY_SUBSTITUTION",
        lambda row: row.update({"official_key_id": "forged-key"}),
    )
    row_attack(
        "A42_LEAF_PROVENANCE_SUBSTITUTION",
        lambda row: row["endpoint_occurrences"][0].update({
            "Round182_leaf_row_id": "forged-leaf"
        }),
    )
    row_attack(
        "A43_ATOM_PROVENANCE_SUBSTITUTION",
        lambda row: row["endpoint_occurrences"][0].update({
            "Round279_atom_row_sha256": "0" * 64
        }),
    )
    row_attack(
        "A44_ROOT_SUBSTITUTION",
        lambda row: row["endpoint_occurrences"][0].update({
            "pre_ordinary_component_root_id": "forged-root"
        }),
    )
    row_attack(
        "A45_ROW_IDENTITY_COLLAPSE_CREDIT",
        lambda row: row.update({
            "formal_occurrence_identity_collapse_credit": 1
        }),
    )
    row_attack(
        "A46_ROW_DSU_RANK_CREDIT",
        lambda row: row.update({
            "formal_DSU_rank_reduction_credit": 1
        }),
    )
    row_attack(
        "A47_ROW_POST_QUOTIENT_ID",
        lambda row: row.update({
            "post_Round297_quotient_component_id": "forged-component"
        }),
    )
    row_attack(
        "A48_ROW_FACE_AS_IDENTITY_SEMANTICS",
        lambda row: row.update({
            "edge_semantics":
                "ORDINARY_FACE_IMPLIES_OCCURRENCE_IDENTITY"
        }),
    )

    good_result = canonical(expected_result) + b"\n"

    def byte_result_attack(
        attack_id: str,
        payload: bytes,
    ) -> None:
        reject(
            attack_id,
            "STRICT_JSON_OR_ENCODING_ATTACK",
            lambda: need(
                strict_json_bytes(payload) == expected_result
                and payload == good_result,
                "strict result bytes",
            ),
        )

    byte_result_attack(
        "A49_DUPLICATE_JSON_KEY",
        b'{"schema":"x","schema":"y"}',
    )
    byte_result_attack("A50_TRAILING_JSON", good_result + b"{}")
    byte_result_attack("A51_NON_UTF8_JSON", b"\xff")
    byte_result_attack("A52_TRUNCATED_JSON", good_result[:100])

    good_ledger_sha = file_sha256(expected_ledger_path)
    with expected_ledger_path.open("rb") as handle:
        good_head = handle.read(2048)

    def ledger_byte_attack(attack_id: str, payload: bytes) -> None:
        reject(
            attack_id,
            "STRICT_DETERMINISTIC_GZIP_ATTACK",
            lambda: need(
                hashlib.sha256(payload).hexdigest() == good_ledger_sha,
                "expected deterministic gzip",
            ),
        )

    ledger_byte_attack("A53_TRUNCATED_GZIP", good_head[:-8])
    ledger_byte_attack(
        "A54_CONCATENATED_GZIP",
        good_head + gzip.compress(b"{}", mtime=0),
    )
    alternate = io.BytesIO()
    with gzip.GzipFile(
        filename="forged.json", mode="wb", fileobj=alternate, mtime=7
    ) as handle:
        handle.write(b"{}")
    ledger_byte_attack("A55_ALTERNATE_GZIP_HEADER", alternate.getvalue())
    ledger_byte_attack(
        "A56_DUPLICATE_LEDGER_JSON_KEY",
        gzip.compress(b'{"schema":"x","schema":"y"}', mtime=0),
    )

    def escape_candidate_overlap(row: dict[str, Any]) -> None:
        axis = row["common_face_axis"]
        tangential = [value for value in range(3) if value != axis][0]
        row["exact_positive_area_face_patch"][2 * tangential] = str(
            Q(row["candidate_overlap_rectangle"][0][0]) - 1
        )

    def zero_area_patch(row: dict[str, Any]) -> None:
        axis = row["common_face_axis"]
        tangential = [value for value in range(3) if value != axis][0]
        row["exact_positive_area_face_patch"][2 * tangential + 1] = (
            row["exact_positive_area_face_patch"][2 * tangential]
        )

    def enlarge_corridor_footprint(row: dict[str, Any]) -> None:
        axis = row["common_face_axis"]
        tangential = [value for value in range(3) if value != axis][0]
        row["two_inward_corridors"][0]["exact_corridor_box"][
            2 * tangential
        ] = str(Q(
            row["exact_positive_area_face_patch"][2 * tangential]
        ) - 1)

    row_attack("A60_PATCH_ESCAPES_CANDIDATE_OVERLAP",
               escape_candidate_overlap)
    row_attack("A61_ZERO_AREA_FACE_PATCH", zero_area_patch)
    row_attack("A62_CORRIDOR_FOOTPRINT_ENLARGED", 
               enlarge_corridor_footprint)

    with tempfile.TemporaryDirectory(
        prefix="round297-path-attacks-"
    ) as directory:
        allowed = Path(directory)
        target = allowed / "target"
        target.write_bytes(b"target")
        symlink = allowed / "candidate"
        symlink.symlink_to(target)
        reject(
            "A57_ACTUAL_CANDIDATE_SYMLINK",
            "FILESYSTEM_PATH_SUBSTITUTION",
            lambda: guard_regular_path(
                symlink, "candidate", allowed
            ),
        )
    with tempfile.TemporaryDirectory(
        prefix="round297-path-attacks-"
    ) as directory:
        allowed = Path(directory)
        target = allowed / "target"
        target.write_bytes(b"target")
        hardlink = allowed / "candidate"
        os.link(target, hardlink)
        reject(
            "A58_ACTUAL_CANDIDATE_HARDLINK",
            "FILESYSTEM_PATH_SUBSTITUTION",
            lambda: guard_regular_path(
                hardlink, "candidate", allowed
            ),
        )
    with tempfile.TemporaryDirectory(
        prefix="round297-path-attacks-"
    ) as directory:
        allowed = Path(directory)
        candidate = allowed / "candidate"
        candidate.write_bytes(b"candidate")
        child = allowed / "child"
        child.mkdir()
        traversal = child / ".." / "candidate"
        reject(
            "A59_ACTUAL_PARENT_TRAVERSAL",
            "FILESYSTEM_PATH_SUBSTITUTION",
            lambda: guard_regular_path(
                traversal, "candidate", allowed
            ),
        )
    need(
        len(attacks) == 62
        and all(row["disposition"] == "REJECTED" for row in attacks),
        "complete Round297 attack suite",
    )
    return attacks


def atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def verify_all() -> dict[str, Any]:
    # Upstream reconstruction phase.  Current Round297 candidate paths are
    # intentionally untouched until the complete expected ledger and result
    # have been built in a private temporary directory.
    expanded_pins = verify_manifest_packages()
    context = reconstruct_context_seals()
    roots, old_roots, member_kinds = reconstruct_r266()
    registry, registry_kinds = reconstruct_registry()
    atoms, atom_dispositions = reconstruct_atoms(registry, old_roots)
    new_atoms = {
        value["target"]
        for value in atoms.values()
        if value["provenance"]
        == "PROMOTED_ROUND288_CANONICAL_ATOM_OCCURRENCE"
    }
    refined = {
        occurrence
        for occurrence, value in registry.items()
        if value["kind"]
        == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    }
    need(
        len(new_atoms) == 295_336
        and len(refined) == 9_404
        and roots.isdisjoint(new_atoms)
        and roots.isdisjoint(refined)
        and new_atoms.isdisjoint(refined),
        "independent disjoint base root tranches",
    )
    base_roots = roots | new_atoms | refined
    need(len(base_roots) == 367_964, "independent base roots")

    with tempfile.TemporaryDirectory(
        prefix="cm2-round297-independent-"
    ) as directory:
        temporary = Path(directory)
        expected_rows = temporary / "expected_rows.jsonl"
        expected_ledger = temporary / "expected_ledger.json.gz"
        metadata, edge_audit, sample_row = (
            independently_reconstruct_edges(
                atoms,
                old_roots,
                base_roots,
                expected_rows,
                expected_ledger,
            )
        )
        expected_result = build_expected_result(
            expanded_pins,
            context,
            registry_kinds,
            member_kinds,
            atom_dispositions,
            metadata,
            edge_audit,
            expected_ledger,
        )

        # Candidate phase starts here, after the full expected object exists.
        need(
            all(
                "PENDING_" not in value
                for value in CANDIDATE_PINS.values()
            ),
            "final candidate pins configured",
        )
        for filename, expected in CANDIDATE_PINS.items():
            path = HERE / filename
            guard_regular_path(path, filename)
            need(
                file_sha256(path) == expected,
                "candidate pin:" + filename,
            )
        audit_candidate(expected_result, expected_rows, expected_ledger)
        attacks = run_attacks(
            expected_result, sample_row, expected_ledger
        )

        verification = {
            "schema": VERIFICATION_SCHEMA,
            "status": (
                "PASS_INDEPENDENT_CACHELESS_ROUND297__"
                "330724_ORDINARY_FACE_OCCURRENCE_EDGES_REBUILT_"
                "BEFORE_CANDIDATE__62_OF_62_ATTACKS_REJECTED"
            ),
            "methodology": {
                "producer_imported_or_executed": False,
                "candidate_used_as_reconstruction_oracle": False,
                "parent_reported_census_used_as_oracle": False,
                "cache_used": False,
                "expected_rows_ledger_and_result_built_before_candidate_read":
                    True,
                "complete_Round266_component_frontier_streamed": True,
                "complete_Round266_member_frontier_streamed": True,
                "Round266_virtual_members_preserved": 133_284,
                "complete_Round294_registry_streamed": True,
                "complete_Round288_atom_dispositions_streamed": True,
                "complete_Round279_atom_ledger_streamed": True,
                "complete_Round279_face_edge_ledger_streamed": True,
                "strict_candidate_JSON_duplicate_trailing_and_encoding_checks":
                    True,
                "deterministic_gzip_exact_byte_reconstruction": True,
                "path_and_symlink_confinement_checked": True,
            },
            "input_package_manifest_pins":
                dict(sorted(PACKAGE_MANIFEST_PINS.items())),
            "input_file_pins": dict(sorted(expanded_pins.items())),
            "candidate_file_pins": dict(sorted(CANDIDATE_PINS.items())),
            "independent_reconstruction": {
                "retained_Round266_component_root_count": 63_224,
                "retained_Round266_member_count": 259_752,
                "retained_Round266_occurrence_member_count": 126_468,
                "retained_Round266_virtual_member_count": 133_284,
                "formal_Round294_registry_count": 431_208,
                "canonical_atom_count": 332_016,
                "distinct_atom_occurrence_target_count": 332_016,
                "new_atom_occurrence_count": 295_336,
                "preserved_atom_alias_target_count": 36_680,
                "ordinary_edge_row_count": 330_724,
                "distinct_occurrence_endpoint_pair_count": 330_724,
                "self_occurrence_endpoint_pair_count": 0,
                "base_root_count": 367_964,
                "distinct_root_endpoint_pair_count": 316_728,
                "pre_same_root_witness_row_count": 14_464,
                "ordinary_edge_application_rank_reduction": 221_916,
                "ordinary_only_candidate_component_count": 146_048,
                "ordinary_rank_and_component_count_promoted": False,
            },
            "formal_credit_audit": {
                "formal_ordinary_component_edge_witness_credit":
                    330_724,
                "formal_occurrence_identity_collapse_credit": 0,
                "formal_occurrence_alias_credit": 0,
                "formal_new_occurrence_ID_credit": 0,
                "formal_representation_alias_credit": 0,
                "formal_seam_edge_credit": 0,
                "formal_Jx_Jy_same_point_glue_credit": 0,
                "formal_component_union_credit": 0,
                "formal_DSU_rank_reduction_credit": 0,
                "formal_maximality_credit": 0,
                "formal_fibre_credit": 0,
                "formal_global_disposition_credit": 0,
                "current_quotient_component_count": None,
            },
            "candidate_result_embedded_sha256":
                expected_result["result_sha256"],
            "candidate_result_file_sha256": file_sha256(RESULT),
            "candidate_ledger_file_sha256": file_sha256(LEDGER),
            "expected_edge_rows_sha256": metadata["rows_sha256"],
            "expected_edge_row_ids_sha256":
                metadata["row_ids_sha256"],
            "expected_edge_row_hashes_sha256":
                metadata["row_hashes_sha256"],
            "attack_suite": {
                "attack_count": len(attacks),
                "rejected_count": len(attacks),
                "accepted_count": 0,
                "attacks": attacks,
            },
        }
        verification["verification_sha256"] = digest(verification)
        return verification


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=297_101)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    verification = verify_all()
    atomic_write(arguments.output, canonical(verification) + b"\n")
    print(json.dumps({
        "status": verification["status"],
        "attack_count": verification["attack_suite"]["attack_count"],
        "candidate_ledger_file_sha256":
            verification["candidate_ledger_file_sha256"],
        "verification_sha256":
            verification["verification_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
