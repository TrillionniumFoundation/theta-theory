#!/usr/bin/env python3
"""Promote Round279 ordinary-face witnesses to occurrence component edges.

This round promotes only formal ordinary component-edge *witness* credit.
Occurrence identities were frozen by Round294 and remain pairwise distinct.
The Round266-root DSU calculation is emitted solely as a nonpromoted,
next-round cross-audit; no quotient or DSU-rank credit is issued here.

Large upstream ledgers are consumed as bounded-memory JSON streams.  The
330,724 output rows are staged as canonical lines and then written as one
deterministic gzip JSON ledger without retaining the complete ledger in RAM.
"""

from __future__ import annotations

from collections import Counter
import argparse
from fractions import Fraction as Q
import gzip
import hashlib
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
LEDGER = HERE / f"{PREFIX}_edge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

SCHEMA = "cm2.round297.source-g-ordinary-face-occurrence-edge-promotion.v1"
LEDGER_SCHEMA = SCHEMA + ".edge-ledger.v1"

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


class BuildError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


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
        raise BuildError("missing guarded path:" + expected_name) from error
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
    line_pattern = re.compile(r"^([0-9a-f]{64})  ([^/\\\\]+)$")
    for manifest_name, manifest_pin in sorted(
        PACKAGE_MANIFEST_PINS.items()
    ):
        need(
            "PENDING_" not in manifest_pin,
            "final package pin pending:" + manifest_name,
        )
        manifest_path = HERE / manifest_name
        guard_regular_path(manifest_path, manifest_name)
        need(
            file_sha256(manifest_path) == manifest_pin,
            "manifest byte pin:" + manifest_name,
        )
        lines = manifest_path.read_text(encoding="ascii").splitlines()
        need(lines and len(lines) == len(set(lines)), "manifest lines")
        for line in lines:
            match = line_pattern.fullmatch(line)
            need(match is not None, "strict manifest line:" + line)
            expected, filename = match.groups()
            path = HERE / filename
            guard_regular_path(path, filename)
            need(
                file_sha256(path) == expected,
                "package member byte pin:" + filename,
            )
            if filename in expanded:
                need(expanded[filename] == expected, "consistent package pin")
            expanded[filename] = expected
        expanded[manifest_name] = manifest_pin
    for required in (
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
        need(required in expanded, "required sealed input:" + required)
    return expanded


class ListHasher:
    def __init__(self) -> None:
        self._hash = hashlib.sha256()
        self._hash.update(b"[")
        self.count = 0

    def add_bytes(self, payload: bytes) -> None:
        if self.count:
            self._hash.update(b",")
        self._hash.update(payload)
        self.count += 1

    def add(self, value: Any) -> None:
        self.add_bytes(canonical(value))

    def finish(self) -> str:
        self._hash.update(b"]")
        return self._hash.hexdigest()


def iterate_array(
    stream: TextIO,
    marker: str = '"rows":[',
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        chunk = stream.read(1 << 20)
        need(bool(chunk), "JSON array marker:" + marker)
        buffer += chunk
        if len(buffer) > 2 * (1 << 20):
            buffer = buffer[-(len(marker) + (1 << 20)):]
    buffer = buffer.split(marker, 1)[1]
    decoder = json.JSONDecoder()
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            chunk = stream.read(1 << 20)
            need(bool(chunk), "unexpected JSON array EOF")
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
                need(bool(chunk), "malformed streamed JSON row")
                buffer += chunk
        need(isinstance(value, dict), "streamed row object")
        yield value
        buffer = buffer[end:]


def gzip_rows(filename: str) -> Iterator[dict[str, Any]]:
    with gzip.open(HERE / filename, "rt", encoding="utf-8") as handle:
        yield from iterate_array(handle)


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
    consumer: Callable[[dict[str, Any]], None],
) -> None:
    expected_count, id_key, expected_rows_sha = EXPECTED_TABLES[label]
    rows_hash = ListHasher()
    ids: set[str] = set()
    count = 0
    for row in rows:
        verify_row(row, label)
        row_id = row[id_key]
        need(row_id not in ids, label + ":unique row ID")
        ids.add(row_id)
        rows_hash.add_bytes(canonical(row))
        consumer(row)
        count += 1
    need(
        count == expected_count
        and rows_hash.count == expected_count
        and rows_hash.finish() == expected_rows_sha,
        label + ":complete rows commitment",
    )


class DSU:
    def __init__(self, nodes: Iterable[str]) -> None:
        materialized = set(nodes)
        self.parent = {node: node for node in materialized}
        self.size = {node: 1 for node in materialized}
        self.rank_reduction = 0

    def find(self, node: str) -> str:
        need(node in self.parent, "DSU node")
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, left: str, right: str) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        self.rank_reduction += 1
        return True

    def component_count(self) -> int:
        return sum(node == parent for node, parent in self.parent.items())


def verify_context_results() -> dict[str, Any]:
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
        "Round280 identity correction result closure",
    )
    contract = r280["result"]
    need(
        contract["status"].startswith(
            "PASS_ZERO_CREDIT_IDENTITY_CONTRACT_AUDIT"
        )
        and contract["deterministic_identity_rule"]["identity_alias_rule"]
        .startswith("Collapse identities only under an explicit exact")
        and contract["verdict"][
            "Round280_connected_class_is_one_occurrence_claim"
        ] == "REJECTED_BY_FROZEN_ROUND265_ROUND266_CONTRACT",
        "Round280 face-connectivity-not-identity contract",
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
        ] is None
        and r294["nonpromotion_freeze"][
            "post_Round294_expanded_registry_component_DSU_status"
        ] == "NOT_REBUILT",
        "Round294 registry scope/non-DSU contract",
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
        "Round295-A lower-stratum no-new-ID contract",
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
        "Round295-B lower-stratum no-new-ID contract",
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


def load_r266_frontier() -> tuple[
    set[str],
    dict[str, dict[str, Any]],
    Counter[str],
]:
    roots: set[str] = set()

    def consume_component(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        need(root not in roots, "unique Round266 component root")
        need(
            row["certified_known_connectivity_only"]
            and not row["maximal_physical_component_claimed"],
            "Round266 component scope",
        )
        roots.add(root)

    audit_rows(
        r266_rows("formal_post_Round266_component_frontier_ledger"),
        "R266_COMPONENT",
        consume_component,
    )

    occurrence_root: dict[str, dict[str, Any]] = {}
    member_kinds: Counter[str] = Counter()

    def consume_member(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        need(
            root in roots
            and row["member_identity_preserved"]
            and row["maximality_credit"] == 0,
            "Round266 member/root scope",
        )
        kind = row["component_member_kind"]
        member_kinds[kind] += 1
        if kind == "EXPANDED_OCCURRENCE":
            occurrence_id = row["component_member_id"]
            need(
                occurrence_id not in occurrence_root,
                "unique existing occurrence root",
            )
            occurrence_root[occurrence_id] = {
                "Round266_component_root_id": root,
                "Round266_component_member_frontier_row_id":
                    row[
                        "post_Round266_component_member_frontier_row_id"
                    ],
                "Round266_component_member_frontier_row_sha256":
                    row["row_sha256"],
                "Round266_component_member_source_kind":
                    row["component_member_source_kind"],
            }

    audit_rows(
        r266_rows(
            "formal_post_Round266_component_member_frontier_ledger"
        ),
        "R266_MEMBER",
        consume_member,
    )
    need(
        len(roots) == 63_224
        and len(occurrence_root) == 126_468
        and member_kinds
        == {
            "EXPANDED_OCCURRENCE": 126_468,
            "VALID_VIRTUAL_STRATUM": 133_284,
        },
        "complete retained Round266 component/member frontier",
    )
    return roots, occurrence_root, member_kinds


def load_r294_registry() -> tuple[
    dict[str, dict[str, Any]],
    Counter[str],
]:
    registry: dict[str, dict[str, Any]] = {}
    kinds: Counter[str] = Counter()

    def consume(row: dict[str, Any]) -> None:
        occurrence_id = row["registry_occurrence_id"]
        need(
            occurrence_id not in registry
            and row["registry_promotion_status"]
            == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY",
            "unique formal Round294 registry occurrence",
        )
        kind = row["registry_entry_kind"]
        kinds[kind] += 1
        registry[occurrence_id] = {
            "Round294_occurrence_registry_row_id":
                row["Round294_occurrence_registry_row_id"],
            "Round294_occurrence_registry_row_sha256": row["row_sha256"],
            "Round294_registry_entry_kind": kind,
            "Round294_registry_source_identity":
                row["registry_source_identity"],
            "complete_10_field_return_signature_sha256":
                row["complete_10_field_return_signature_sha256"],
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "physical_support_chart": row["physical_support_chart"],
            "owner_target": row["owner_target"],
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
        "Round294 registry tranche census",
    )
    return registry, kinds


def load_atom_occurrence_map(
    registry: dict[str, dict[str, Any]],
    occurrence_root: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], Counter[str]]:
    atoms: dict[str, dict[str, Any]] = {}
    target_ids: set[str] = set()
    dispositions: Counter[str] = Counter()

    def consume_disposition(row: dict[str, Any]) -> None:
        atom_id = row["canonical_atom_id"]
        need(atom_id not in atoms, "unique Round288 atom")
        existing = row["existing_local_occurrence_row_id"]
        target = (
            existing
            or row["reserved_candidate_occurrence_id__not_issued"]
        )
        need(
            target is not None
            and target in registry
            and target not in target_ids,
            "unique formal target per canonical atom",
        )
        target_ids.add(target)
        if existing is not None:
            disposition = "PRESERVED_ROUND266_OCCURRENCE_ALIAS"
            expected_kind = (
                "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
            )
            need(target in occurrence_root, "existing atom Round266 root")
        else:
            disposition = "PROMOTED_ROUND288_CANONICAL_ATOM_OCCURRENCE"
            expected_kind = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
            need(target not in occurrence_root, "new atom singleton root")
        registration = registry[target]
        need(
            registration["Round294_registry_entry_kind"] == expected_kind
            and registration[
                "complete_10_field_return_signature_sha256"
            ] == row["complete_10_field_return_signature_sha256"]
            and registration["official_key_id"] == row["official_key_id"]
            and registration["official_key_ordinal"]
            == row["official_key_ordinal"],
            "Round288/Round294 identity-key-signature join",
        )
        dispositions[disposition] += 1
        atoms[atom_id] = {
            "formal_Round294_occurrence_id": target,
            "occurrence_identity_provenance": disposition,
            "Round288_atom_disposition_row_id":
                row["Round288_atom_disposition_row_id"],
            "Round288_atom_disposition_row_sha256": row["row_sha256"],
            "complete_10_field_return_signature_sha256":
                row["complete_10_field_return_signature_sha256"],
            "Round182_leaf_row_id": row["Round182_leaf_row_id"],
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            **registration,
        }

    audit_rows(
        gzip_rows(R288_DISPOSITIONS),
        "R288_DISPOSITION",
        consume_disposition,
    )
    need(
        len(atoms) == len(target_ids) == 332_016
        and dispositions
        == {
            "PROMOTED_ROUND288_CANONICAL_ATOM_OCCURRENCE": 295_336,
            "PRESERVED_ROUND266_OCCURRENCE_ALIAS": 36_680,
        },
        "332016 distinct formal atom occurrence targets",
    )

    seen: set[str] = set()

    def consume_atom(row: dict[str, Any]) -> None:
        atom_id = row["canonical_atom_id"]
        need(
            atom_id in atoms and atom_id not in seen,
            "Round279/Round288 atom universe",
        )
        seen.add(atom_id)
        target = atoms[atom_id]
        signature = row["complete_10_field_return_signature"]
        need(
            target["complete_10_field_return_signature_sha256"]
            == row["complete_10_field_return_signature_sha256"]
            and target["Round182_leaf_row_id"]
            == row["Round182_leaf_row_id"]
            and target["official_key_id"] == signature["official_key_id"]
            and target["official_key_ordinal"]
            == signature["official_key_ordinal"]
            and row["expanded_occurrence_credit"] == 0
            and row["component_credit"] == 0
            and row["maximality_credit"] == 0,
            "Round279 atom provenance/signature/nonpromotion",
        )
        anchors = row["existing_Round208_occurrence_row_ids"]
        if anchors:
            need(
                len(anchors) == 1
                and anchors[0] == target["formal_Round294_occurrence_id"],
                "Round208 anchor preservation",
            )
        target.update({
            "Round279_atom_row_sha256": row["row_sha256"],
            "Round279_atom_source_signature_row_ids":
                row["source_signature_row_ids"],
            "Round279_atom_support_classification":
                row["support_classification"],
            "Round279_atom_source_chart": row["source_chart"],
            "Round279_atom_owner_target": row["owner_target"],
        })

    audit_rows(gzip_rows(R279_ATOMS), "R279_ATOM", consume_atom)
    need(seen == set(atoms), "complete Round279 atom join")
    return atoms, dispositions


def validate_face_geometry(row: dict[str, Any]) -> None:
    axis = row["common_face_axis"]
    need(axis in {0, 1, 2}, "face axis")
    coordinate = Q(row["common_face_coordinate"])
    face = tuple(map(Q, row["exact_positive_area_face_patch"]))
    need(
        len(face) == 6
        and face[2 * axis] == face[2 * axis + 1] == coordinate,
        "exact face coordinate",
    )
    tangential_axes = [value for value in range(3) if value != axis]
    overlap = row["candidate_overlap_rectangle"]
    need(len(overlap) == 2, "face overlap rectangle")
    for slot, other_axis in enumerate(tangential_axes):
        interval = tuple(map(Q, overlap[slot]))
        need(
            len(interval) == 2
            and interval[0] < interval[1]
            and interval[0] <= face[2 * other_axis]
            < face[2 * other_axis + 1] <= interval[1],
            "positive exact refined tangential face subinterval",
        )
    corridors = row["two_inward_corridors"]
    need(
        len(corridors) == 2
        and corridors[0]["geometric_side"]
        == "NEGATIVE_SIDE_INWARD"
        and corridors[1]["geometric_side"]
        == "POSITIVE_SIDE_INWARD",
        "two ordered inward corridors",
    )
    for side_index, corridor in enumerate(corridors):
        box = tuple(map(Q, corridor["exact_corridor_box"]))
        need(
            len(box) == 6
            and all(
                box[2 * value] < box[2 * value + 1]
                for value in range(3)
            ),
            "positive exact inward corridor",
        )
        normal_endpoint = box[2 * axis + (1 if side_index == 0 else 0)]
        need(normal_endpoint == coordinate, "corridor reaches common face")
        for other_axis in tangential_axes:
            need(
                box[2 * other_axis:2 * other_axis + 2]
                == face[2 * other_axis:2 * other_axis + 2],
                "corridor exact tangential footprint",
            )


def endpoint_payload(
    atom_id: str,
    endpoint: dict[str, Any],
    atom: dict[str, Any],
    occurrence_root: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    occurrence_id = atom["formal_Round294_occurrence_id"]
    root_provenance = occurrence_root.get(occurrence_id)
    if root_provenance is None:
        root_id = occurrence_id
        root_kind = "ROUND294_NEW_OCCURRENCE_SINGLETON_ROOT"
        member_row_id = None
        member_row_sha = None
    else:
        root_id = root_provenance["Round266_component_root_id"]
        root_kind = "RETAINED_ROUND266_COMPONENT_ROOT"
        member_row_id = root_provenance[
            "Round266_component_member_frontier_row_id"
        ]
        member_row_sha = root_provenance[
            "Round266_component_member_frontier_row_sha256"
        ]
    return {
        "geometric_side": endpoint["geometric_side"],
        "canonical_atom_id": atom_id,
        "Round182_leaf_row_id": endpoint["leaf_row_id"],
        "Round279_atom_row_sha256": atom["Round279_atom_row_sha256"],
        "Round279_atom_source_signature_row_ids":
            atom["Round279_atom_source_signature_row_ids"],
        "Round279_atom_support_classification":
            atom["Round279_atom_support_classification"],
        "Round288_atom_disposition_row_id":
            atom["Round288_atom_disposition_row_id"],
        "Round288_atom_disposition_row_sha256":
            atom["Round288_atom_disposition_row_sha256"],
        "formal_Round294_occurrence_id": occurrence_id,
        "Round294_occurrence_registry_row_id":
            atom["Round294_occurrence_registry_row_id"],
        "Round294_occurrence_registry_row_sha256":
            atom["Round294_occurrence_registry_row_sha256"],
        "Round294_registry_entry_kind":
            atom["Round294_registry_entry_kind"],
        "occurrence_identity_provenance":
            atom["occurrence_identity_provenance"],
        "official_key_id": atom["official_key_id"],
        "official_key_ordinal": atom["official_key_ordinal"],
        "complete_10_field_return_signature_sha256":
            atom["complete_10_field_return_signature_sha256"],
        "pre_ordinary_component_root_id": root_id,
        "pre_ordinary_component_root_kind": root_kind,
        "Round266_component_member_frontier_row_id": member_row_id,
        "Round266_component_member_frontier_row_sha256": member_row_sha,
    }


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


def write_streamed_ledger(
    rows_path: Path,
    metadata: dict[str, Any],
    destination: Path,
) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + destination.name + ".", dir=destination.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as raw:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw, mtime=0
            ) as output:
                output.write(b"{")
                keys = sorted(set(metadata) | {"rows"})
                for key_index, key in enumerate(keys):
                    if key_index:
                        output.write(b",")
                    output.write(canonical(key))
                    output.write(b":")
                    if key != "rows":
                        output.write(canonical(metadata[key]))
                        continue
                    output.write(b"[")
                    with rows_path.open("rb") as rows:
                        first = True
                        for line in rows:
                            value = line.rstrip(b"\n")
                            need(bool(value), "nonempty staged row")
                            if not first:
                                output.write(b",")
                            output.write(value)
                            first = False
                    output.write(b"]")
                output.write(b"}")
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def promote_edges(
    atoms: dict[str, dict[str, Any]],
    occurrence_root: dict[str, dict[str, Any]],
    base_roots: set[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    dsu = DSU(base_roots)
    occurrence_pairs: set[tuple[str, str]] = set()
    root_pairs: set[tuple[str, str]] = set()
    source_edge_ids: set[str] = set()
    output_row_ids: set[str] = set()
    source_candidate_indices: set[int] = set()
    pre_same_root_count = 0
    row_count = 0
    rows_hash = ListHasher()
    row_ids_hash = ListHasher()
    row_hashes_hash = ListHasher()
    occurrence_pairs_hash = ListHasher()
    source_edge_ids_hash = ListHasher()
    root_pairs_hash = ListHasher()

    descriptor, rows_name = tempfile.mkstemp(
        prefix="round297-edge-rows.", suffix=".jsonl"
    )
    rows_path = Path(rows_name)
    try:
        with os.fdopen(descriptor, "wb") as staged:
            def consume_edge(source: dict[str, Any]) -> None:
                nonlocal pre_same_root_count, row_count
                verify_row(source, "Round279 edge")
                need(
                    source["candidate_index"] == row_count
                    and source["candidate_index"]
                    not in source_candidate_indices,
                    "complete source candidate-index order",
                )
                source_candidate_indices.add(source["candidate_index"])
                source_edge_id = source[
                    "formal_face_edge_witness_row_id"
                ]
                need(
                    source_edge_id not in source_edge_ids,
                    "unique source face-edge ID",
                )
                source_edge_ids.add(source_edge_id)
                need(
                    source["component_edge_credit"] == 0
                    and source["expanded_occurrence_credit"] == 0
                    and source["maximality_credit"] == 0,
                    "Round279 source edge frozen zero-credit state",
                )
                validate_face_geometry(source)
                endpoint_sources = source["endpoint_atoms"]
                need(
                    len(endpoint_sources) == 2
                    and endpoint_sources[0]["geometric_side"] == "NEGATIVE"
                    and endpoint_sources[1]["geometric_side"] == "POSITIVE",
                    "ordered source endpoints",
                )
                atom_ids = [
                    endpoint["canonical_atom_id"]
                    for endpoint in endpoint_sources
                ]
                need(
                    atom_ids[0] != atom_ids[1]
                    and all(atom_id in atoms for atom_id in atom_ids),
                    "two distinct formal atoms",
                )
                for endpoint_index, atom_id in enumerate(atom_ids):
                    joined_atom = atoms[atom_id]
                    need(
                        endpoint_sources[endpoint_index]["leaf_row_id"]
                        == joined_atom["Round182_leaf_row_id"]
                        and source["two_inward_corridors"][
                            endpoint_index
                        ]["leaf_row_id"]
                        == endpoint_sources[endpoint_index]["leaf_row_id"]
                        and joined_atom["Round279_atom_source_chart"]
                        == source["source_chart"]
                        and joined_atom["Round279_atom_owner_target"]
                        == source["owner_target"],
                        "edge/atom/endpoint/corridor provenance join",
                    )
                endpoint_rows = [
                    endpoint_payload(
                        atom_id,
                        endpoint,
                        atoms[atom_id],
                        occurrence_root,
                    )
                    for atom_id, endpoint in zip(
                        atom_ids, endpoint_sources, strict=True
                    )
                ]
                signature = source[
                    "complete_10_field_return_signature_sha256"
                ]
                need(
                    endpoint_rows[0][
                        "complete_10_field_return_signature_sha256"
                    ]
                    == endpoint_rows[1][
                        "complete_10_field_return_signature_sha256"
                    ]
                    == signature
                    and endpoint_rows[0]["official_key_id"]
                    == endpoint_rows[1]["official_key_id"]
                    and endpoint_rows[0]["official_key_ordinal"]
                    == endpoint_rows[1]["official_key_ordinal"],
                    "edge endpoint signature/key purity",
                )
                occurrence_pair = tuple(sorted(
                    endpoint[
                        "formal_Round294_occurrence_id"
                    ]
                    for endpoint in endpoint_rows
                ))
                need(
                    occurrence_pair[0] != occurrence_pair[1]
                    and occurrence_pair not in occurrence_pairs,
                    "unique nonself occurrence endpoint pair",
                )
                occurrence_pairs.add(occurrence_pair)
                root_pair = tuple(sorted(
                    endpoint["pre_ordinary_component_root_id"]
                    for endpoint in endpoint_rows
                ))
                need(
                    root_pair[0] in base_roots
                    and root_pair[1] in base_roots,
                    "ordinary edge root universe",
                )
                same_root = root_pair[0] == root_pair[1]
                pre_same_root_count += int(same_root)
                root_pairs.add(root_pair)
                dsu.union(*root_pair)

                row_id = (
                    "round297-ordinary-face-occurrence-edge:"
                    + digest([
                        source_edge_id,
                        list(occurrence_pair),
                    ])
                )
                need(
                    row_id not in output_row_ids,
                    "unique Round297 output row ID",
                )
                output_row_ids.add(row_id)
                promoted = close({
                    "Round297_ordinary_face_occurrence_edge_row_id":
                        row_id,
                    "source_Round279_face_edge_witness_row_id":
                        source_edge_id,
                    "source_Round279_face_edge_row_sha256":
                        source["row_sha256"],
                    "source_candidate_index": source["candidate_index"],
                    "source_witness_partition":
                        source["witness_partition"],
                    "source_chart": source["source_chart"],
                    "owner_target": source["owner_target"],
                    "official_key_id":
                        endpoint_rows[0]["official_key_id"],
                    "official_key_ordinal":
                        endpoint_rows[0]["official_key_ordinal"],
                    "complete_10_field_return_signature_sha256":
                        signature,
                    "common_face_axis": source["common_face_axis"],
                    "common_face_coordinate":
                        source["common_face_coordinate"],
                    "candidate_overlap_rectangle":
                        source["candidate_overlap_rectangle"],
                    "exact_positive_area_face_patch":
                        source["exact_positive_area_face_patch"],
                    "two_inward_corridors":
                        source["two_inward_corridors"],
                    "endpoint_occurrences": endpoint_rows,
                    "exact_occurrence_endpoint_pair":
                        list(occurrence_pair),
                    "occurrence_endpoint_pair_is_nonself": True,
                    "pre_ordinary_component_root_pair":
                        list(root_pair),
                    "pre_ordinary_same_component_root": same_root,
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
                encoded = canonical(promoted)
                staged.write(encoded + b"\n")
                rows_hash.add_bytes(encoded)
                row_ids_hash.add(row_id)
                row_hashes_hash.add(promoted["row_sha256"])
                occurrence_pairs_hash.add(list(occurrence_pair))
                source_edge_ids_hash.add(source_edge_id)
                root_pairs_hash.add(list(root_pair))
                row_count += 1

            audit_rows(gzip_rows(R279_EDGES), "R279_EDGE", consume_edge)
            staged.flush()
            os.fsync(staged.fileno())

        need(
            row_count == len(source_candidate_indices)
            == len(source_edge_ids) == len(output_row_ids)
            == len(occurrence_pairs) == 330_724
            and source_candidate_indices == set(range(330_724)),
            "complete unique ordinary edge universe",
        )
        need(
            len(root_pairs) == 316_728
            and pre_same_root_count == 14_464
            and dsu.rank_reduction == 221_916
            and dsu.component_count() == 146_048,
            "ordinary-only nonpromoted root/DSU cross-audit",
        )
        rows_sha = rows_hash.finish()
        row_ids_sha = row_ids_hash.finish()
        row_hashes_sha = row_hashes_hash.finish()
        occurrence_pairs_sha = occurrence_pairs_hash.finish()
        source_edge_ids_sha = source_edge_ids_hash.finish()
        ordered_root_pairs_sha = root_pairs_hash.finish()
        metadata = {
            "schema": LEDGER_SCHEMA,
            "status": (
                "PASS_ROUND297_330724_ORDINARY_FACE_OCCURRENCE_"
                "COMPONENT_EDGE_WITNESSES__ZERO_IDENTITY_COLLAPSE__"
                "ZERO_DSU_RANK_CREDIT"
            ),
            "row_order":
                "SOURCE_ROUND279_CANDIDATE_INDEX_ASCENDING_0_TO_330723",
            "row_count": row_count,
            "rows_sha256": rows_sha,
            "row_ids_sha256": row_ids_sha,
            "row_hashes_sha256": row_hashes_sha,
            "source_edge_ids_sha256": source_edge_ids_sha,
            "ordered_occurrence_endpoint_pairs_sha256":
                occurrence_pairs_sha,
            "ordered_pre_ordinary_root_pairs_sha256":
                ordered_root_pairs_sha,
            "all_occurrence_endpoint_pairs_unique": True,
            "all_occurrence_endpoint_pairs_nonself": True,
            "formal_ordinary_component_edge_witness_credit_sum":
                330_724,
        }
        write_streamed_ledger(rows_path, metadata, LEDGER)
        guard_regular_path(LEDGER, LEDGER.name)
        audit = {
            "ordinary_edge_row_count": row_count,
            "distinct_occurrence_endpoint_pair_count":
                len(occurrence_pairs),
            "self_occurrence_endpoint_pair_count": 0,
            "distinct_pre_ordinary_component_root_pair_count":
                len(root_pairs),
            "pre_same_component_root_witness_row_count":
                pre_same_root_count,
            "ordinary_edge_application_rank_reduction":
                dsu.rank_reduction,
            "ordinary_only_candidate_component_count":
                dsu.component_count(),
            "rows_sha256": rows_sha,
            "row_ids_sha256": row_ids_sha,
            "row_hashes_sha256": row_hashes_sha,
            "source_edge_ids_sha256": source_edge_ids_sha,
            "ordered_occurrence_endpoint_pairs_sha256":
                occurrence_pairs_sha,
            "ordered_pre_ordinary_root_pairs_sha256":
                ordered_root_pairs_sha,
        }
        return metadata, audit
    finally:
        if rows_path.exists():
            rows_path.unlink()


def build() -> dict[str, Any]:
    expanded_pins = verify_manifest_packages()
    context = verify_context_results()
    roots, occurrence_root, member_kinds = load_r266_frontier()
    registry, registry_kinds = load_r294_registry()
    atoms, atom_dispositions = load_atom_occurrence_map(
        registry, occurrence_root
    )

    new_atom_occurrences = {
        atom["formal_Round294_occurrence_id"]
        for atom in atoms.values()
        if atom["occurrence_identity_provenance"]
        == "PROMOTED_ROUND288_CANONICAL_ATOM_OCCURRENCE"
    }
    refined_occurrences = {
        occurrence_id
        for occurrence_id, row in registry.items()
        if row["Round294_registry_entry_kind"]
        == "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
    }
    need(
        len(new_atom_occurrences) == 295_336
        and len(refined_occurrences) == 9_404
        and roots.isdisjoint(new_atom_occurrences)
        and roots.isdisjoint(refined_occurrences)
        and new_atom_occurrences.isdisjoint(refined_occurrences),
        "disjoint ordinary-DSU base root tranches",
    )
    base_roots = roots | new_atom_occurrences | refined_occurrences
    need(len(base_roots) == 367_964, "ordinary-DSU base root count")

    ledger_metadata, edge_audit = promote_edges(
        atoms, occurrence_root, base_roots
    )
    ledger_sha = file_sha256(LEDGER)
    summary = {
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
    summary["result_sha256"] = digest(summary)
    atomic_write(RESULT, canonical(summary) + b"\n")
    guard_regular_path(RESULT, RESULT.name)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=297_001)
    parser.parse_args()
    result = build()
    print(json.dumps({
        "status": result["status"],
        "edge_row_count":
            result["edge_ledger"]["row_count"],
        "formal_ordinary_component_edge_witness_credit":
            result["formal_credit_transition"][
                "formal_ordinary_component_edge_witness_credit"
            ],
        "current_quotient":
            result["strict_nonpromotion"][
                "post_Round297_quotient_component_count"
            ],
        "ledger_file_sha256":
            result["edge_ledger"]["file_sha256"],
        "result_sha256": result["result_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
