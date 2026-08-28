#!/usr/bin/env python3
"""Independently verify the Round225 known-connectivity rebuild.

The Round222 partition is the frozen union-find boundary.  Only exact local
TRACE glues certified by Round223 and Round224 are added.  Proved ABSENT rows
and the still-missing Round220 transition identities remain non-edges.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import Any, Iterable


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round225_source_g_certified_connectivity_rebuild"
VERIFIER_PREFIX = f"{PREFIX}_verifier"
OUTPUT = HERE / f"{PREFIX}_verification.json"
SCHEMA = "cm2.round225.source-g-certified-connectivity-rebuild.v1"
VERIFICATION_SCHEMA = f"{SCHEMA}.verification.v1"
STATUS = "PASS_PARTIAL_FORMAL_ROUND225"
CERTIFICATE_STATUS = (
    "CERTIFIED_CONNECTIVITY_QUOTIENT_REBUILT__7404_KNOWN_BLOCKS__"
    "PHYSICAL_COMPONENT_EQUIVALENCE_STILL_INCOMPLETE"
)
SOURCE_G_KEYS = 224_580
MAX_INPUT_BYTES = 180_000_000
CANDIDATE = f"{PREFIX}_certificate.json"
CANDIDATE_SHA256 = (
    "0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841"
)
CANDIDATE_RESULT_SHA256 = (
    "0aedfdcc43e45810d97cc0699562a4d1e9faefb0ca3f3e055c84b1ad3ec77512"
)
PRODUCER = f"{PREFIX}.py"
PRODUCER_SHA256 = (
    "1c6637751c398ff26faceee0419421ffdab1616d17bab9ad99fa3c24a9b3d9f2"
)

R222_SOURCE = (
    "cm2_round222_source_g_certified_known_connectivity_union_find.py"
)
R222_CERTIFICATE = (
    "cm2_round222_source_g_certified_known_connectivity_union_find_"
    "certificate.json"
)
R223_CERTIFICATE = (
    "cm2_round223_source_g_analytic_endpoint_root_stratification_"
    "certificate.json"
)
R224_SOURCE = (
    "cm2_round224_source_g_partial_face_analytic_root_stratification.py"
)
R224_CERTIFICATE = (
    "cm2_round224_source_g_partial_face_analytic_root_stratification_"
    "certificate.json"
)

R222_SOURCE_SHA256 = (
    "58b5b63dc25a44c7d2279d54b1eb842d88cc61e3abd6c31f889688d3d2801a22"
)
R222_CERTIFICATE_SHA256 = (
    "700174fc3bdfa57805ce8a2a97630fd9e6183ce5aee443c430f14db6184e9e9e"
)
R222_RESULT_SHA256 = (
    "1b80b806fa6716135480a500ff1248cc8dfabb37af7b3802ba50ba1bf62b493e"
)
R223_CERTIFICATE_SHA256 = (
    "3d28f097419e11bde6733462736fcb70cd0164b18ac06a793a34b5dc26113168"
)
R223_RESULT_SHA256 = (
    "db012bb2e68176c8a5c144455bac9ff780521bbfa3c03110694390c70a3343d9"
)
R224_SOURCE_SHA256 = (
    "8bb6bd227be21d2c2c6e34394e4f83257f502bb9ab621355a306d5a20757336b"
)
R224_CERTIFICATE_SHA256 = (
    "9ff49f0a55c0048f8dc7b636b1ddcc7291e01545e9775d95cb9738f4b3f237c7"
)
R224_RESULT_SHA256 = (
    "2015369b8f5eef92da2245981157bf4dbacc55a69939b087d893f954f3374ab8"
)

R222_SCHEMA = "cm2.round222.source-g-certified-known-connectivity-union-find.v1"
R223_SCHEMA = "cm2.round223.source-g-analytic-endpoint-root-stratification.v1"
R224_SCHEMA = (
    "cm2.round224.source-g-partial-face-analytic-root-stratification.v1"
)
R222_MEMBERSHIP_SHA256 = (
    "715008789165502798276611bd763a8f6cf3160d9c74d8559a63c3cf7e467cd9"
)
R225_MEMBERSHIP_SHA256 = (
    "28a2fdc438c5c58096afd5e714ba0451d480072bafafd8158b6b39f4c9fd7018"
)


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for chunk in ENCODER.iterencode(value):
        yield chunk.encode()


def canonical_bytes(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in chunks(value):
        state.update(chunk)
    return state.hexdigest()


def make_id(label: str, value: Any) -> str:
    return f"round225-{label}:{digest(value)}"


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def verify_row(row: dict[str, Any], label: str) -> None:
    require(
        row.get("row_sha256")
        == digest(
            {
                key: value
                for key, value in row.items()
                if key != "row_sha256"
            }
        ),
        f"row closure:{label}",
    )


def histogram(values: Iterable[Any]) -> dict[str, int]:
    return dict(sorted(Counter(str(value) for value in values).items()))


def regular_bytes(path: Path, maximum: int = MAX_INPUT_BYTES) -> bytes:
    before = path.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not path.is_symlink()
        and before.st_nlink == 1,
        f"single-link regular:{path.name}",
    )
    require(0 < before.st_size <= maximum, f"bounded:{path.name}")
    descriptor = os.open(
        path,
        os.O_RDONLY
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            )
            == (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ),
            f"stable open:{path.name}",
        )
        parts: list[bytes] = []
        size = 0
        while True:
            part = os.read(descriptor, 1024 * 1024)
            if not part:
                break
            size += len(part)
            require(size <= maximum, f"bounded read:{path.name}")
            parts.append(part)
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
            == (
                opened.st_dev,
                opened.st_ino,
                opened.st_size,
                opened.st_mtime_ns,
            ),
            f"stable read:{path.name}",
        )
        return b"".join(parts)
    finally:
        os.close(descriptor)


def pinned(
    path: Path, expected: str, maximum: int = MAX_INPUT_BYTES
) -> bytes:
    raw = regular_bytes(path, maximum)
    require(
        hashlib.sha256(raw).hexdigest() == expected,
        f"SHA256:{path.name}",
    )
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result, f"duplicate key:{label}:{key}")
            result[key] = value
        return result

    def reject(token: str) -> None:
        raise VerificationError(f"non-integral JSON number:{label}:{token}")

    result = json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_float=reject,
        parse_constant=reject,
    )
    require(isinstance(result, dict), f"object:{label}")
    try:
        canonical_bytes(result).decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError) as error:
        raise VerificationError(f"invalid Unicode:{label}") from error
    return result


def load_envelope(
    name: str,
    file_sha256: str,
    result_sha256: str,
    schema: str,
) -> dict[str, Any]:
    envelope = strict_json(
        pinned(HERE / name, file_sha256),
        name,
    )
    require(
        set(envelope) == {"result", "result_sha256", "schema"},
        f"envelope keys:{name}",
    )
    require(envelope["schema"] == schema, f"schema:{name}")
    require(
        envelope["result_sha256"] == result_sha256
        and digest(envelope["result"]) == result_sha256,
        f"result closure:{name}",
    )
    return envelope["result"]


def verify_ledger(
    value: dict[str, Any],
    id_key: str,
    label: str,
) -> list[dict[str, Any]]:
    require(
        set(value)
        == {
            "every_row_closed_by_own_SHA256",
            "row_count",
            "row_hashes_sha256",
            "row_ids_sha256",
            "rows",
            "rows_sha256",
        },
        f"ledger keys:{label}",
    )
    rows = value["rows"]
    require(isinstance(rows, list), f"rows list:{label}")
    require(value["every_row_closed_by_own_SHA256"] is True, label)
    require(value["row_count"] == len(rows), f"count:{label}")
    require(value["rows_sha256"] == digest(rows), f"rows:{label}")
    require(
        value["row_ids_sha256"] == digest([row[id_key] for row in rows]),
        f"ids:{label}",
    )
    require(
        value["row_hashes_sha256"]
        == digest([row["row_sha256"] for row in rows]),
        f"hashes:{label}",
    )
    require(
        len({row[id_key] for row in rows}) == len(rows),
        f"unique ids:{label}",
    )
    for row in rows:
        verify_row(row, f"{label}:{row[id_key]}")
    return rows


def ledger(
    rows: list[dict[str, Any]],
    id_key: str,
) -> dict[str, Any]:
    require(
        len({row[id_key] for row in rows}) == len(rows),
        f"unique:{id_key}",
    )
    return {
        "row_count": len(rows),
        "every_row_closed_by_own_SHA256": True,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest([row[id_key] for row in rows]),
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows": rows,
    }


class UF:
    """The Round222 union-find implementation and deterministic tie-break."""

    def __init__(self, nodes: Iterable[str]) -> None:
        self.parent = {node: node for node in nodes}
        self.size = {node: 1 for node in self.parent}

    def find(self, node: str) -> str:
        root = node
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[node] != node:
            following = self.parent[node]
            self.parent[node] = root
            node = following
        return root

    def join(self, left: str, right: str) -> bool:
        left, right = self.find(left), self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right] or (
            self.size[left] == self.size[right] and left > right
        ):
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True

    def groups(self) -> list[list[str]]:
        groups: dict[str, list[str]] = defaultdict(list)
        for node in self.parent:
            groups[self.find(node)].append(node)
        return sorted(sorted(group) for group in groups.values())


def zero_promotion(row: dict[str, Any], label: str) -> None:
    for key in (
        "formal_component_deduplication_credit",
        "global_component_credit",
        "global_exact_key_disposition_credit",
        "global_fibre_credit",
        "whole_leaf_credit",
        "whole_origin_credit",
        "whole_original_tube_credit",
    ):
        if key in row:
            require(row[key] == 0, f"{label}:{key}")


def pair_from_leaves(
    row: dict[str, Any],
    leaf_to_sheet: dict[str, str],
) -> tuple[str, str]:
    negative_key = (
        "negative_side_leaf_row_id"
        if "negative_side_leaf_row_id" in row
        else "negative_leaf_row_id"
    )
    positive_key = (
        "positive_side_leaf_row_id"
        if "positive_side_leaf_row_id" in row
        else "positive_leaf_row_id"
    )
    require(
        row[negative_key] in leaf_to_sheet
        and row[positive_key] in leaf_to_sheet,
        "leaf-to-sheet mapping",
    )
    pair = tuple(
        sorted(
            (
                leaf_to_sheet[row[negative_key]],
                leaf_to_sheet[row[positive_key]],
            )
        )
    )
    require(pair[0] != pair[1], "self-loop")
    return pair


def new_evidence() -> dict[str, Any]:
    return {
        "glue_ids": [],
        "stratum_ids": [],
        "contact_ids": set(),
        "completion_ids": set(),
        "join_ids": [],
    }


def build_result(producer_sha256: str) -> dict[str, Any]:
    pinned(HERE / R222_SOURCE, R222_SOURCE_SHA256, 5_000_000)
    pinned(HERE / R224_SOURCE, R224_SOURCE_SHA256, 5_000_000)

    round222 = load_envelope(
        R222_CERTIFICATE,
        R222_CERTIFICATE_SHA256,
        R222_RESULT_SHA256,
        R222_SCHEMA,
    )
    require(
        round222["provenance"]["producer_sha256"] == R222_SOURCE_SHA256,
        "Round222 producer binding",
    )
    assignments222 = verify_ledger(
        round222["formal_Round211_sheet_assignment_ledger"],
        "sheet_assignment_row_id",
        "Round222 assignments",
    )
    blocks222 = verify_ledger(
        round222["formal_certified_known_connectivity_block_ledger"],
        "known_connectivity_block_id",
        "Round222 blocks",
    )
    edges222 = verify_ledger(
        round222[
            "formal_Round217_Round219_current_quotient_edge_ledger"
        ],
        "current_quotient_edge_row_id",
        "Round222 edges",
    )
    frontier222 = verify_ledger(
        round222[
            "formal_unresolved_and_nonedge_frontier_account_ledger"
        ],
        "frontier_account_row_id",
        "Round222 frontier",
    )
    require(
        len(assignments222) == 17_716
        and len(blocks222) == 7_640
        and len(edges222) == 7_036
        and len(frontier222) == 7_280,
        "Round222 ledger census",
    )

    sheet_by_id = {
        row["Round211_sheet_row_id"]: row for row in assignments222
    }
    leaf_to_sheet = {
        row["leaf_row_id"]: row["Round211_sheet_row_id"]
        for row in assignments222
    }
    require(
        len(sheet_by_id) == len(leaf_to_sheet) == 17_716,
        "Round222 assignment bijection",
    )

    old_block_by_sheet: dict[str, str] = {}
    old_members_by_block: dict[str, list[str]] = {}
    for block in blocks222:
        members = block["member_Round211_sheet_row_ids"]
        require(
            members == sorted(members)
            and block["member_Round211_sheet_row_count"] == len(members)
            and block["member_Round211_sheet_row_ids_sha256"]
            == digest(members)
            and block["certified_known_connectivity"] is True
            and block["maximal_physical_component_claimed"] is False
            and block["component_exhaustion_credit"] == 0
            and block["global_exact_key_disposition_credit"] == 0,
            "Round222 block boundary",
        )
        old_members_by_block[block["known_connectivity_block_id"]] = members
        for member in members:
            require(
                member in sheet_by_id and member not in old_block_by_sheet,
                "Round222 block partition",
            )
            old_block_by_sheet[member] = block[
                "known_connectivity_block_id"
            ]
    require(
        set(old_block_by_sheet) == set(sheet_by_id),
        "Round222 complete block partition",
    )
    for assignment in assignments222:
        require(
            old_block_by_sheet[assignment["Round211_sheet_row_id"]]
            == assignment["known_connectivity_block_id"],
            "Round222 assignment/block agreement",
        )
    groups222 = sorted(old_members_by_block.values())
    require(
        digest(groups222) == R222_MEMBERSHIP_SHA256,
        "Round222 membership boundary",
    )

    old_literal_pairs: set[tuple[str, str]] = set()
    for edge in edges222:
        pair = tuple(
            sorted(
                (
                    edge["left_Round211_sheet_row_id"],
                    edge["right_Round211_sheet_row_id"],
                )
            )
        )
        require(
            pair[0] != pair[1]
            and pair[0] in sheet_by_id
            and pair[1] in sheet_by_id
            and sheet_by_id[pair[0]]["leaf_row_id"]
            == edge["left_leaf_row_id"]
            and sheet_by_id[pair[1]]["leaf_row_id"]
            == edge["right_leaf_row_id"]
            and edge["current_quotient_lower_bound_edge_credit"] == 1
            and edge["maximal_physical_component_edge_credit"] == 0
            and edge["global_exact_key_disposition_credit"] == 0
            and edge["accepted_from_signature_hash_or_box_touch_alone"]
            is False,
            "Round222 edge boundary",
        )
        old_literal_pairs.add(pair)
    require(len(old_literal_pairs) == 7_036, "Round222 pair census")

    frontier_kind_count = Counter(
        row["frontier_kind"] for row in frontier222
    )
    require(
        frontier_kind_count
        == Counter(
            {
                "ROUND219_INCOMPLETE_EXACT_CONTACT": 7_016,
                "ROUND219_PARTIAL_UNRESOLVED": 236,
                "ROUND219_PARTIAL_ABSENT": 28,
            }
        ),
        "Round222 frontier kinds",
    )

    union_find = UF(sheet_by_id)
    seeded_merges = 0
    for members in groups222:
        for member in members[1:]:
            seeded_merges += union_find.join(members[0], member)
    require(
        seeded_merges == 10_076
        and union_find.groups() == groups222,
        "Round222 union-find seed",
    )

    round223 = load_envelope(
        R223_CERTIFICATE,
        R223_CERTIFICATE_SHA256,
        R223_RESULT_SHA256,
        R223_SCHEMA,
    )
    scope223 = round223["formal_exact_contact_scope"]
    require(
        scope223["total_exact_p_s_contact_count"] == 7_932
        and scope223["cumulative_complete_exact_p_s_contact_count"]
        == 7_932
        and scope223["remaining_incomplete_exact_p_s_contact_count"] == 0
        and scope223["physical_component_equivalence_relation_complete"]
        is False,
        "Round223 exact p/s closure",
    )
    completed223 = verify_ledger(
        round223["formal_completed_exact_contact_ledger"],
        "completed_contact_row_id",
        "Round223 completed contacts",
    )
    strata223 = verify_ledger(
        round223["formal_symbolic_stratum_ledger"],
        "symbolic_stratum_row_id",
        "Round223 symbolic strata",
    )
    joins223 = verify_ledger(
        round223["formal_endpoint_to_curve_join_ledger"],
        "endpoint_to_curve_join_row_id",
        "Round223 endpoint joins",
    )
    completed223_by_contact: dict[str, dict[str, Any]] = {}
    for row in completed223:
        zero_promotion(row, "Round223 completion")
        require(
            row[
                "formal_exact_contact_symbolic_stratification_complete_credit"
            ]
            == 1
            and row["all_old_UNRESOLVED_subfaces_exactly_replaced"]
            is True
            and row["replacement_partition_exact_union_of_old_subfaces"]
            is True
            and row["replacement_partition_has_no_gap"] is True
            and row["replacement_partition_has_no_owned_overlap"] is True,
            "Round223 completed-contact predicate",
        )
        contact_id = row["Round219_exact_contact_row_id"]
        require(
            contact_id not in completed223_by_contact,
            "Round223 unique completed contact",
        )
        completed223_by_contact[contact_id] = row
    require(
        len(completed223_by_contact) == 7_016,
        "Round223 completed-contact census",
    )

    evidence223: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        new_evidence
    )
    contact_pair223: dict[str, tuple[str, str]] = {}
    trace_count223 = 0
    for row in strata223:
        if row.get("classification") == "TRACE":
            zero_promotion(row, "Round223 TRACE")
            require(
                row["topological_dimension"] == 2
                and row["formal_local_glue_credit"] == 1
                and row["formal_local_incidence_credit"] == 2
                and row["formal_two_dimensional_trace_stratum_credit"]
                == 1
                and row["formal_two_dimensional_zero_absence_stratum_credit"]
                == 0
                and row["exact_common_refinement_glue_row_id"] is not None
                and row["negative_side_incidence_row_id"] is not None
                and row["positive_side_incidence_row_id"] is not None,
                "Round223 TRACE edge predicate",
            )
            contact_id = row["contact_row_id"]
            require(
                contact_id in completed223_by_contact,
                "Round223 TRACE completion binding",
            )
            pair = pair_from_leaves(row, leaf_to_sheet)
            if contact_id in contact_pair223:
                require(
                    contact_pair223[contact_id] == pair,
                    "Round223 contact pair consistency",
                )
            contact_pair223[contact_id] = pair
            bucket = evidence223[pair]
            bucket["glue_ids"].append(
                row["exact_common_refinement_glue_row_id"]
            )
            bucket["stratum_ids"].append(row["symbolic_stratum_row_id"])
            bucket["contact_ids"].add(contact_id)
            trace_count223 += 1
        else:
            require(
                row.get("formal_local_glue_credit", 0) != 1,
                "Round223 non-TRACE nonedge",
            )
    require(
        trace_count223 == 7_236
        and len(evidence223) == 7_016
        and set(contact_pair223) == set(completed223_by_contact)
        and histogram(
            len(bucket["glue_ids"]) for bucket in evidence223.values()
        )
        == {"1": 6_796, "2": 220},
        "Round223 exact-glue census",
    )
    for contact_id, row in completed223_by_contact.items():
        evidence223[contact_pair223[contact_id]]["completion_ids"].add(
            row["completed_contact_row_id"]
        )
    for row in joins223:
        zero_promotion(row, "Round223 endpoint join")
        require(
            row["formal_endpoint_to_curve_join_credit"] == 1
            and row["exact_restricted_evaluator_identity"] is True
            and row["joined_from_numeric_root_approximation"] is False
            and row["contact_row_id"] in contact_pair223,
            "Round223 endpoint-join predicate",
        )
        pair = pair_from_leaves(row, leaf_to_sheet)
        require(
            pair == contact_pair223[row["contact_row_id"]],
            "Round223 endpoint-join pair",
        )
        evidence223[pair]["join_ids"].append(
            row["endpoint_to_curve_join_row_id"]
        )
    require(len(joins223) == 7_232, "Round223 endpoint-join census")

    reduction223: dict[tuple[str, str], bool] = {}
    same_before223 = 0
    for pair in sorted(evidence223):
        same_before223 += union_find.find(pair[0]) == union_find.find(
            pair[1]
        )
        reduction223[pair] = union_find.join(*pair)
    require(
        same_before223 == 7_016
        and sum(reduction223.values()) == 0
        and len(union_find.groups()) == 7_640
        and len(set(evidence223) & old_literal_pairs) == 6_120,
        "Round223 rank-redundant union census",
    )

    round224 = load_envelope(
        R224_CERTIFICATE,
        R224_CERTIFICATE_SHA256,
        R224_RESULT_SHA256,
        R224_SCHEMA,
    )
    require(
        round224["provenance"]["producer_sha256"] == R224_SOURCE_SHA256,
        "Round224 producer binding",
    )
    scope224 = round224["formal_partial_contact_scope"]
    require(
        scope224["total_partial_contact_count"] == 264
        and scope224["Round219_inherited_complete_zero_absence_contact_count"]
        == 28
        and scope224[
            "new_symbolic_stratification_complete_partial_contact_count"
        ]
        == 236
        and scope224["remaining_incomplete_partial_contact_count"] == 0
        and scope224["physical_component_equivalence_relation_complete"]
        is False,
        "Round224 partial closure",
    )
    completed224 = verify_ledger(
        round224["formal_completed_partial_contact_ledger"],
        "completed_partial_contact_row_id",
        "Round224 completed contacts",
    )
    strata224 = verify_ledger(
        round224["formal_partial_symbolic_stratum_ledger"],
        "partial_symbolic_stratum_row_id",
        "Round224 symbolic strata",
    )
    joins224 = verify_ledger(
        round224["formal_partial_endpoint_to_curve_join_ledger"],
        "partial_endpoint_to_curve_join_row_id",
        "Round224 endpoint joins",
    )
    completed224_by_contact: dict[str, dict[str, Any]] = {}
    contact_pair224: dict[str, tuple[str, str]] = {}
    for row in completed224:
        zero_promotion(row, "Round224 completion")
        require(
            row[
                "formal_partial_contact_symbolic_stratification_complete_credit"
            ]
            == 1
            and row["old_UNRESOLVED_partial_contact_exactly_replaced"]
            is True
            and row[
                "replacement_partition_exact_union_of_old_partial_overlap"
            ]
            is True
            and row["replacement_partition_has_no_gap"] is True
            and row["replacement_partition_has_no_owned_overlap"] is True,
            "Round224 completed-contact predicate",
        )
        contact_id = row["Round219_partial_contact_row_id"]
        require(
            contact_id not in completed224_by_contact,
            "Round224 unique completed contact",
        )
        completed224_by_contact[contact_id] = row
        contact_pair224[contact_id] = pair_from_leaves(
            row, leaf_to_sheet
        )
    require(
        len(completed224_by_contact) == 236,
        "Round224 completed-contact census",
    )

    evidence224: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        new_evidence
    )
    trace_count224 = 0
    for row in strata224:
        if row.get("classification") == "TRACE":
            zero_promotion(row, "Round224 TRACE")
            require(
                row["topological_dimension"] == 2
                and row["formal_local_partial_glue_credit"] == 1
                and row["formal_local_partial_incidence_credit"] == 2
                and row[
                    "formal_two_dimensional_partial_trace_stratum_credit"
                ]
                == 1
                and row[
                    "formal_two_dimensional_partial_zero_absence_stratum_credit"
                ]
                == 0
                and row["exact_partial_common_refinement_glue_row_id"]
                is not None
                and row["negative_side_incidence_row_id"] is not None
                and row["positive_side_incidence_row_id"] is not None,
                "Round224 TRACE edge predicate",
            )
            contact_id = row["Round219_partial_contact_row_id"]
            require(
                contact_id in contact_pair224,
                "Round224 TRACE completion binding",
            )
            pair = pair_from_leaves(row, leaf_to_sheet)
            require(
                pair == contact_pair224[contact_id],
                "Round224 contact pair consistency",
            )
            bucket = evidence224[pair]
            bucket["glue_ids"].append(
                row["exact_partial_common_refinement_glue_row_id"]
            )
            bucket["stratum_ids"].append(
                row["partial_symbolic_stratum_row_id"]
            )
            bucket["contact_ids"].add(contact_id)
            trace_count224 += 1
        else:
            require(
                row.get("formal_local_partial_glue_credit", 0) != 1,
                "Round224 non-TRACE nonedge",
            )
    require(
        trace_count224 == 236
        and len(evidence224) == 236
        and set().union(
            *(bucket["contact_ids"] for bucket in evidence224.values())
        )
        == set(completed224_by_contact),
        "Round224 exact partial-glue census",
    )
    for contact_id, row in completed224_by_contact.items():
        evidence224[contact_pair224[contact_id]]["completion_ids"].add(
            row["completed_partial_contact_row_id"]
        )
    for row in joins224:
        zero_promotion(row, "Round224 endpoint join")
        require(
            row["formal_partial_endpoint_to_curve_join_credit"] == 1
            and row["exact_restricted_evaluator_identity"] is True
            and row["joined_from_numeric_root_approximation"] is False
            and row["Round219_partial_contact_row_id"] in contact_pair224,
            "Round224 endpoint-join predicate",
        )
        pair = pair_from_leaves(row, leaf_to_sheet)
        require(
            pair
            == contact_pair224[row["Round219_partial_contact_row_id"]],
            "Round224 endpoint-join pair",
        )
        evidence224[pair]["join_ids"].append(
            row["partial_endpoint_to_curve_join_row_id"]
        )
    require(len(joins224) == 236, "Round224 endpoint-join census")
    require(
        not (set(evidence224) & set(evidence223))
        and not (set(evidence224) & old_literal_pairs),
        "Round224 pair disjointness",
    )

    reduction224: dict[tuple[str, str], bool] = {}
    cross_before224 = 0
    for pair in sorted(evidence224):
        cross_before224 += union_find.find(pair[0]) != union_find.find(
            pair[1]
        )
        reduction224[pair] = union_find.join(*pair)
    require(
        cross_before224 == 236
        and sum(reduction224.values()) == 236
        and len(union_find.groups()) == 7_404,
        "Round224 rank-reduction census",
    )

    edge_rows: list[dict[str, Any]] = []
    edge_id_by_source_pair: dict[tuple[str, tuple[str, str]], str] = {}
    for source, evidence, reductions in (
        ("ROUND223_EXACT_P_S_TRACE_GLUE", evidence223, reduction223),
        (
            "ROUND224_EXACT_PARTIAL_CONTACT_TRACE_GLUE",
            evidence224,
            reduction224,
        ),
    ):
        for pair in sorted(evidence):
            bucket = evidence[pair]
            glue_ids = sorted(bucket["glue_ids"])
            stratum_ids = sorted(bucket["stratum_ids"])
            contact_ids = sorted(bucket["contact_ids"])
            completion_ids = sorted(bucket["completion_ids"])
            join_ids = sorted(bucket["join_ids"])
            edge_id = make_id(
                "current-quotient-edge", [source, *pair]
            )
            edge_id_by_source_pair[(source, pair)] = edge_id
            edge_rows.append(
                closed(
                    {
                        "current_quotient_edge_row_id": edge_id,
                        "source_layer": source,
                        "left_Round211_sheet_row_id": pair[0],
                        "right_Round211_sheet_row_id": pair[1],
                        "left_leaf_row_id": sheet_by_id[pair[0]][
                            "leaf_row_id"
                        ],
                        "right_leaf_row_id": sheet_by_id[pair[1]][
                            "leaf_row_id"
                        ],
                        "upstream_exact_glue_row_count": len(glue_ids),
                        "upstream_exact_glue_row_ids": glue_ids,
                        "upstream_exact_glue_row_ids_sha256": digest(
                            glue_ids
                        ),
                        "upstream_symbolic_stratum_row_ids_sha256":
                            digest(stratum_ids),
                        "upstream_completed_contact_row_ids_sha256":
                            digest(completion_ids),
                        "upstream_endpoint_to_curve_join_row_count":
                            len(join_ids),
                        "upstream_endpoint_to_curve_join_row_ids_sha256":
                            digest(join_ids),
                        "already_literal_Round222_edge":
                            pair in old_literal_pairs,
                        "same_Round222_known_connectivity_block":
                            old_block_by_sheet[pair[0]]
                            == old_block_by_sheet[pair[1]],
                        "union_rank_reduction_credit":
                            int(reductions[pair]),
                        "rank_redundant_under_preceding_sources":
                            not reductions[pair],
                        "accepted_from_signature_hash_or_box_touch_alone":
                            False,
                        "current_quotient_lower_bound_edge_credit": 1,
                        "maximal_physical_component_edge_credit": 0,
                        "global_exact_key_disposition_credit": 0,
                    }
                )
            )
    edge_rows.sort(key=lambda row: row["current_quotient_edge_row_id"])
    require(len(edge_rows) == 7_252, "Round225 edge ledger census")

    final_groups = union_find.groups()
    require(
        len(final_groups) == 7_404
        and digest(final_groups) == R225_MEMBERSHIP_SHA256
        and histogram(len(group) for group in final_groups)
        == {
            "1": 2_140,
            "2": 3_184,
            "3": 296,
            "4": 1_452,
            "5": 48,
            "6": 32,
            "7": 208,
            "8": 12,
            "9": 12,
            "10": 12,
            "11": 4,
            "64": 4,
        },
        "Round225 final membership census",
    )

    sheet_to_block225: dict[str, str] = {}
    block_rows: list[dict[str, Any]] = []
    old_block_multiplicity = Counter()
    for members in final_groups:
        old_block_ids = sorted(
            {old_block_by_sheet[member] for member in members}
        )
        old_block_multiplicity[len(old_block_ids)] += 1
        block_id = make_id("known-connectivity-block", members)
        for member in members:
            sheet_to_block225[member] = block_id
        block_rows.append(
            closed(
                {
                    "known_connectivity_block_id": block_id,
                    "canonical_member_Round211_sheet_row_id": members[0],
                    "member_Round211_sheet_row_count": len(members),
                    "member_Round211_sheet_row_ids": members,
                    "member_Round211_sheet_row_ids_sha256": digest(members),
                    "member_leaf_row_ids_sha256": digest(
                        sorted(
                            sheet_by_id[member]["leaf_row_id"]
                            for member in members
                        )
                    ),
                    "inherited_Round222_known_connectivity_block_count":
                        len(old_block_ids),
                    "inherited_Round222_known_connectivity_block_ids_sha256":
                        digest(old_block_ids),
                    "certified_known_connectivity": True,
                    "maximal_physical_component_claimed": False,
                    "component_exhaustion_credit": 0,
                    "global_exact_key_disposition_credit": 0,
                }
            )
        )
    block_rows.sort(key=lambda row: row["known_connectivity_block_id"])
    require(
        old_block_multiplicity
        == Counter({1: 7_228, 2: 116, 3: 60}),
        "Round225 old-block multiplicity",
    )

    incidence223: Counter[str] = Counter()
    incidence224: Counter[str] = Counter()
    for left, right in evidence223:
        incidence223[left] += 1
        incidence223[right] += 1
    for left, right in evidence224:
        incidence224[left] += 1
        incidence224[right] += 1
    assignment_rows: list[dict[str, Any]] = []
    for old in assignments222:
        sheet_id = old["Round211_sheet_row_id"]
        isolated = (
            old["isolated_under_current_proved_edge_set"]
            and incidence223[sheet_id] == 0
            and incidence224[sheet_id] == 0
        )
        assignment_rows.append(
            closed(
                {
                    "sheet_assignment_row_id": make_id(
                        "sheet-assignment", sheet_id
                    ),
                    "Round211_sheet_row_id": sheet_id,
                    "Round211_sheet_row_sha256": old[
                        "Round211_sheet_row_sha256"
                    ],
                    "leaf_row_id": old["leaf_row_id"],
                    "Round222_sheet_assignment_row_id": old[
                        "sheet_assignment_row_id"
                    ],
                    "Round222_sheet_assignment_row_sha256": old[
                        "row_sha256"
                    ],
                    "Round222_known_connectivity_block_id": old[
                        "known_connectivity_block_id"
                    ],
                    "known_connectivity_block_id":
                        sheet_to_block225[sheet_id],
                    "Round222_unique_proved_edge_incidence_count": old[
                        "current_unique_proved_edge_incidence_count"
                    ],
                    "Round223_exact_glue_pair_incidence_count":
                        incidence223[sheet_id],
                    "Round224_partial_glue_pair_incidence_count":
                        incidence224[sheet_id],
                    "isolated_under_Round222_proved_edge_set": old[
                        "isolated_under_current_proved_edge_set"
                    ],
                    "isolated_under_rebuilt_proved_edge_set": isolated,
                    "maximal_physical_component_assignment_claimed": False,
                    "global_exact_key_disposition_credit": 0,
                }
            )
        )
    require(
        sum(
            row["isolated_under_rebuilt_proved_edge_set"]
            for row in assignment_rows
        )
        == 2_140,
        "Round225 isolated-sheet census",
    )

    frontier_rows: list[dict[str, Any]] = []
    remaining_rows: list[dict[str, Any]] = []
    disposition_count: Counter[str] = Counter()
    cross_block_account_count = 0
    cross_block_proved_absence_count = 0
    for old in frontier222:
        pair = tuple(
            sorted(
                (
                    old["left_Round211_sheet_row_id"],
                    old["right_Round211_sheet_row_id"],
                )
            )
        )
        kind = old["frontier_kind"]
        edge_id: str | None
        if kind == "ROUND219_INCOMPLETE_EXACT_CONTACT":
            require(
                old["upstream_row_id"] in contact_pair223
                and contact_pair223[old["upstream_row_id"]] == pair,
                "Round223 frontier disposition binding",
            )
            disposition = "RESOLVED_BY_ROUND223_EXACT_TRACE_GLUE"
            source = "ROUND223_EXACT_P_S_TRACE_GLUE"
            edge_id = edge_id_by_source_pair[(source, pair)]
            proved_nonedge = False
            missing = False
        elif kind == "ROUND219_PARTIAL_UNRESOLVED":
            require(
                old["upstream_row_id"] in contact_pair224
                and contact_pair224[old["upstream_row_id"]] == pair,
                "Round224 frontier disposition binding",
            )
            disposition = "RESOLVED_BY_ROUND224_EXACT_PARTIAL_TRACE_GLUE"
            source = "ROUND224_EXACT_PARTIAL_CONTACT_TRACE_GLUE"
            edge_id = edge_id_by_source_pair[(source, pair)]
            proved_nonedge = False
            missing = False
        else:
            require(
                kind == "ROUND219_PARTIAL_ABSENT"
                and old["formal_partial_zero_absence_credit"] == 1
                and old["exact_trace_or_absence_proof_missing"] is False,
                "Round219 proved-absence disposition",
            )
            disposition = "CLOSED_PROVED_ABSENCE_NONEDGE"
            source = None
            edge_id = None
            proved_nonedge = True
            missing = False
        same_final = (
            sheet_to_block225[pair[0]] == sheet_to_block225[pair[1]]
        )
        cross_block_account_count += not same_final
        cross_block_proved_absence_count += proved_nonedge and not same_final
        row = closed(
            {
                "frontier_disposition_row_id": make_id(
                    "frontier-disposition",
                    old["frontier_account_row_id"],
                ),
                "Round222_frontier_account_row_id": old[
                    "frontier_account_row_id"
                ],
                "Round222_frontier_account_row_sha256": old["row_sha256"],
                "frontier_kind": kind,
                "upstream_row_id": old["upstream_row_id"],
                "upstream_row_sha256": old["upstream_row_sha256"],
                "left_Round211_sheet_row_id": pair[0],
                "right_Round211_sheet_row_id": pair[1],
                "disposition": disposition,
                "certified_edge_source_layer": source,
                "Round225_current_quotient_edge_row_id": edge_id,
                "same_Round222_known_connectivity_block":
                    old_block_by_sheet[pair[0]]
                    == old_block_by_sheet[pair[1]],
                "same_rebuilt_known_connectivity_block": same_final,
                "proved_absence_nonedge": proved_nonedge,
                "remaining_missing_equivalence_proof": missing,
                "remaining_cross_block_frontier":
                    missing and not same_final,
                "maximal_physical_component_credit": 0,
                "global_exact_key_disposition_credit": 0,
            }
        )
        disposition_count[disposition] += 1
        frontier_rows.append(row)
        if row["remaining_cross_block_frontier"]:
            remaining_rows.append(row)
    frontier_rows.sort(
        key=lambda row: row["frontier_disposition_row_id"]
    )
    require(
        disposition_count
        == Counter(
            {
                "RESOLVED_BY_ROUND223_EXACT_TRACE_GLUE": 7_016,
                "RESOLVED_BY_ROUND224_EXACT_PARTIAL_TRACE_GLUE": 236,
                "CLOSED_PROVED_ABSENCE_NONEDGE": 28,
            }
        )
        and cross_block_account_count == 28
        and cross_block_proved_absence_count == 28
        and len(remaining_rows) == 0,
        "Round225 rebuilt frontier census",
    )

    boundary222 = round222["Round216_Round220_boundary_and_nonedge_audit"]
    require(
        boundary222["Round220_coordinate_adjacency_nonedge_count"]
        == 10_384
        and boundary222[
            "Round220_rejected_coordinate_coincidence_nonedge_count"
        ]
        == 9_830
        and boundary222[
            "Round220_cross_parent_cross_chart_physical_glue_missing"
        ]
        is True
        and boundary222["Round220_physical_glue_blocker_closed"] is False,
        "Round222 Round220 boundary",
    )

    return {
        "status": CERTIFICATE_STATUS,
        "verdict": (
            "ROUND222_QUOTIENT_REBUILT_WITH_ALL_ROUND223_AND_ROUND224_"
            "CERTIFIED_TRACE_GLUES__7404_KNOWN_CONNECTIVITY_BLOCKS__"
            "NO_COMPONENT_WHOLE_OR_GLOBAL_PROMOTION"
        ),
        "formal_input_binding": {
            "Round222_producer_sha256": R222_SOURCE_SHA256,
            "Round222_certificate_sha256": R222_CERTIFICATE_SHA256,
            "Round222_result_sha256": R222_RESULT_SHA256,
            "Round223_certificate_sha256": R223_CERTIFICATE_SHA256,
            "Round223_result_sha256": R223_RESULT_SHA256,
            "Round224_producer_sha256": R224_SOURCE_SHA256,
            "Round224_certificate_sha256": R224_CERTIFICATE_SHA256,
            "Round224_result_sha256": R224_RESULT_SHA256,
            "Round222_union_find_implementation_reused": True,
            "Round222_sheet_assignment_and_block_boundary_reused": True,
            "producer_outcome_or_oracle_dependency": False,
        },
        "terminology_and_scope_contract": {
            "allowed_block_term": "CERTIFIED_KNOWN_CONNECTIVITY_BLOCK",
            "allowed_edge_term": "CURRENT_QUOTIENT_LOWER_BOUND_EDGE",
            "known_connectivity_block_count_is_not_a_component_count": True,
            "maximal_physical_component_term_forbidden": True,
            "proved_ABSENT_row_is_not_an_edge": True,
            "Round220_coordinate_adjacency_is_not_event_trace_glue": True,
        },
        "source_layered_edge_audit": {
            "fixed_source_precedence": [
                "ROUND222_CERTIFIED_KNOWN_CONNECTIVITY_PARTITION",
                "ROUND223_EXACT_P_S_TRACE_GLUE",
                "ROUND224_EXACT_PARTIAL_CONTACT_TRACE_GLUE",
            ],
            "Round222_known_connectivity_block_count": 7_640,
            "Round223_TRACE_evidence_row_count": 7_236,
            "Round223_unique_sheet_pair_count": 7_016,
            "Round223_literal_Round222_edge_overlap_count": 6_120,
            "Round223_nonliteral_but_same_Round222_block_pair_count": 896,
            "Round223_union_rank_reduction": 0,
            "Round223_rank_redundant_unique_pair_count": 7_016,
            "Round224_TRACE_evidence_row_count": 236,
            "Round224_unique_sheet_pair_count": 236,
            "Round224_pair_overlap_with_Round222_literal_edges": 0,
            "Round224_pair_overlap_with_Round223_pairs": 0,
            "Round224_union_rank_reduction": 236,
            "Round224_rank_redundant_unique_pair_count": 0,
            "Round223_unique_sheet_pairs_sha256": digest(
                sorted([list(pair) for pair in evidence223])
            ),
            "Round224_unique_sheet_pairs_sha256": digest(
                sorted([list(pair) for pair in evidence224])
            ),
        },
        "known_connectivity_delta": {
            "raw_Round211_sheet_row_count": 17_716,
            "Round222_known_connectivity_block_count": 7_640,
            "block_count_after_Round223": 7_640,
            "Round223_block_reduction": 0,
            "block_count_after_Round224": 7_404,
            "Round224_block_reduction": 236,
            "Round222_to_Round225_block_reduction": 236,
            "total_union_rank_reduction_from_raw_sheets": 10_312,
            "Round222_old_block_multiplicity_in_rebuilt_blocks": {
                "1": 7_228,
                "2": 116,
                "3": 60,
            },
            "rebuilt_known_connectivity_block_size_histogram":
                histogram(len(group) for group in final_groups),
            "rebuilt_known_connectivity_membership_sha256":
                digest(final_groups),
            "rebuilt_edge_isolated_sheet_count": 2_140,
            "maximal_physical_component_count_claimed": False,
            "component_exhaustion_credit": 0,
        },
        "formal_Round223_Round224_current_quotient_edge_ledger":
            ledger(edge_rows, "current_quotient_edge_row_id"),
        "formal_certified_known_connectivity_block_ledger":
            ledger(block_rows, "known_connectivity_block_id"),
        "formal_Round211_sheet_assignment_ledger":
            ledger(assignment_rows, "sheet_assignment_row_id"),
        "formal_Round222_frontier_disposition_ledger":
            ledger(frontier_rows, "frontier_disposition_row_id"),
        "formal_remaining_cross_block_frontier_ledger":
            ledger(remaining_rows, "frontier_disposition_row_id"),
        "rebuilt_frontier_audit": {
            "Round222_frontier_account_count": 7_280,
            "Round223_resolved_exact_contact_count": 7_016,
            "Round224_resolved_partial_contact_count": 236,
            "Round219_proved_ABSENT_nonedge_count": 28,
            "cross_block_account_count_after_rebuild": 28,
            "cross_block_proved_ABSENT_nonedge_count": 28,
            "remaining_missing_contact_frontier_count": 0,
            "remaining_cross_block_missing_contact_frontier_count": 0,
            "all_exact_p_s_and_partial_contact_proof_gaps_closed": True,
        },
        "first_missing_gate": {
            "gate": "ROUND220_CROSS_PARENT_CROSS_CHART_TRANSITION_GLUE",
            "Round220_coordinate_adjacency_nonedge_count": 10_384,
            "Round220_rejected_coordinate_coincidence_nonedge_count": 9_830,
            "first_missing_proof": (
                "EXPLICIT_CROSS_PARENT_CROSS_CHART_TRANSITION_IDENTITY_"
                "AND_EXACT_EVENT_TRACE_RESTRICTION"
            ),
            "Round220_candidate_to_Round211_sheet_pair_map_materialized":
                False,
            "Round220_exact_cross_block_sheet_pair_count_claimed": False,
            "physical_component_equivalence_relation_complete": False,
        },
        "strict_nonpromotion": {
            "formal_component_deduplication_credit": 0,
            "maximal_physical_component_credit": 0,
            "component_exhaustion_credit": 0,
            "whole_leaf_credit": 0,
            "whole_origin_credit": 0,
            "whole_original_tube_credit": 0,
            "global_component_credit": 0,
            "global_fibre_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator":
                SOURCE_G_KEYS,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize explicit Round220 cross-parent/cross-chart "
            "transition identities and exact event-trace restrictions, map "
            "them to Round211 sheet pairs, and rebuild again; do not grant "
            "component, whole, or global credit before the equivalence "
            "relation and occurrence fibres are genuinely complete"
        ),
        "provenance": {
            "schema": SCHEMA,
            "producer_sha256": producer_sha256,
            "python_version": sys.version.split()[0],
            "producer_outcome_blind": True,
            "formal_upstream_files_modified": False,
            "independent_verifier_must_not_import_or_execute_producer": True,
        },
    }


def validate_output(path: Path) -> Path:
    require(not any(part == ".." for part in path.parts), "output alias")
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(
        absolute.parent == HERE
        and absolute.parent.resolve() == HERE
        and (
            absolute.name == OUTPUT.name
            or (
                absolute.name.startswith(f".{PREFIX}_replay_")
                and absolute.name.endswith(".json")
            )
        ),
        "output allowlist",
    )
    protected = {
        Path(__file__).resolve(),
        (HERE / R222_SOURCE).resolve(),
        (HERE / R222_CERTIFICATE).resolve(),
        (HERE / R223_CERTIFICATE).resolve(),
        (HERE / R224_SOURCE).resolve(),
        (HERE / R224_CERTIFICATE).resolve(),
    }
    require(
        absolute.resolve(strict=False) not in protected,
        "protected output",
    )
    if absolute.exists() or absolute.is_symlink():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and not absolute.is_symlink()
            and metadata.st_nlink == 1,
            "existing output type",
        )
    return absolute


def safe_write(path: Path, data: bytes) -> None:
    destination = validate_output(path)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        directory = os.open(
            os.fspath(destination.parent),
            os.O_RDONLY
            | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_CLOEXEC", 0),
        )
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except BaseException:
        if descriptor >= 0:
            os.close(descriptor)
        raise
    finally:
        if temporary.exists() or temporary.is_symlink():
            temporary.unlink()


def candidate_accepts(candidate: dict[str, Any], expected: dict[str, Any]) -> bool:
    try:
        require(set(candidate) == {"result", "result_sha256", "schema"}, "candidate envelope")
        require(candidate["schema"] == SCHEMA, "candidate schema")
        require(candidate["result_sha256"] == digest(candidate["result"]), "candidate closure")
        require(candidate["result_sha256"] == CANDIDATE_RESULT_SHA256, "candidate pinned result")
        require(candidate["result"] == expected, "complete independent result equality")
        return True
    except (VerificationError, KeyError, TypeError):
        return False


def semantic_attack_suite(candidate: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    paths = [
        ("known_connectivity_delta", "Round222_to_Round225_block_reduction"),
        ("known_connectivity_delta", "block_count_after_Round224"),
        ("known_connectivity_delta", "maximal_physical_component_count_claimed"),
        ("rebuilt_frontier_audit", "remaining_cross_block_missing_contact_frontier_count"),
        ("rebuilt_frontier_audit", "Round219_proved_ABSENT_nonedge_count"),
        ("strict_nonpromotion", "component_exhaustion_credit"),
        ("strict_nonpromotion", "global_exact_key_disposition_credit"),
        ("strict_nonpromotion", "whole_origin_credit"),
        ("strict_nonpromotion", "D02"),
        ("strict_nonpromotion", "CM2"),
        ("terminology_and_scope_contract", "maximal_physical_component_term_forbidden"),
        ("provenance", "producer_outcome_blind"),
    ]
    rejected = 0
    for outer, inner in paths:
        original = candidate["result"][outer][inner]
        if isinstance(original, bool):
            altered = not original
        elif isinstance(original, int):
            altered = original + 1
        else:
            altered = f"FORGED::{original}"
        candidate["result"][outer][inner] = altered
        candidate["result_sha256"] = digest(candidate["result"])
        rejected += not candidate_accepts(candidate, expected)
        candidate["result"][outer][inner] = original
        candidate["result_sha256"] = digest(candidate["result"])
    require(rejected == len(paths), "semantic attacks")
    return {
        "attempted": len(paths),
        "rejected": rejected,
        "all_attacks_reclosed_with_fresh_result_SHA256": True,
        "classes": [f"{a}.{b}" for a, b in paths],
    }


def strict_json_attack_suite() -> dict[str, Any]:
    attacks = [
        b'{"a":1,"a":2}', b'{"a":1.0}', b'{"a":NaN}', b'{"a":Infinity}',
        b'{"a":-Infinity}', b'[]', b'null', b'true', b'{"a":1} trailing',
        b'{"a":01}', b'{"a":1e0}', b'{"a":0.0}', b'{"a":"\\ud800"}',
        b'{"a":"\\udfff"}', b'{"a":}', b'{"a":1,}',
    ]
    rejected = 0
    for index, raw in enumerate(attacks):
        try:
            strict_json(raw, f"attack-{index}")
        except (VerificationError, json.JSONDecodeError, UnicodeError):
            rejected += 1
    require(rejected == len(attacks), "strict JSON attacks")
    return {"attempted": len(attacks), "rejected": rejected}


def path_and_file_attack_suite() -> dict[str, Any]:
    rejected = 0
    attempted = 0

    def must_reject(action: Any) -> None:
        nonlocal rejected, attempted
        attempted += 1
        try:
            action()
        except (VerificationError, FileNotFoundError, IsADirectoryError):
            rejected += 1

    with tempfile.TemporaryDirectory(prefix=".round225-file-attacks-", dir=HERE) as directory:
        root = Path(directory)
        regular = root / "regular"
        regular.write_bytes(b"abcd")
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        hardlink = root / "hardlink"
        os.link(regular, hardlink)
        fifo = root / "fifo"
        os.mkfifo(fifo)
        empty = root / "empty"
        empty.touch()
        must_reject(lambda: regular_bytes(symlink, 10))
        must_reject(lambda: regular_bytes(hardlink, 10))
        must_reject(lambda: regular_bytes(fifo, 10))
        must_reject(lambda: regular_bytes(root, 10))
        must_reject(lambda: regular_bytes(root / "missing", 10))
        must_reject(lambda: regular_bytes(empty, 10))
        must_reject(lambda: regular_bytes(regular, 3))
        must_reject(lambda: validate_output(HERE / ".." / HERE.name / OUTPUT.name))
        must_reject(lambda: validate_output(HERE / CANDIDATE))
        replay = HERE / f".{PREFIX}_replay_attack.json"
        try:
            replay.symlink_to(regular)
            must_reject(lambda: validate_output(replay))
        finally:
            if replay.is_symlink():
                replay.unlink()
    require(rejected == attempted == 10, "path/file attacks")
    return {
        "attempted": attempted,
        "rejected": rejected,
        "classes": [
            "symlink", "hardlink", "FIFO", "directory", "missing",
            "empty", "bounded-size", "parent-alias", "protected-output",
            "output-symlink",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()

    require(hashlib.sha256(regular_bytes(HERE / PRODUCER, 5_000_000)).hexdigest() == PRODUCER_SHA256, "producer pin")
    candidate = strict_json(pinned(HERE / CANDIDATE, CANDIDATE_SHA256), CANDIDATE)
    expected = build_result(PRODUCER_SHA256)
    require(candidate_accepts(candidate, expected), "candidate semantics")
    semantic_attacks = semantic_attack_suite(candidate, expected)
    json_attacks = strict_json_attack_suite()
    file_attacks = path_and_file_attack_suite()
    verifier_sha256 = hashlib.sha256(regular_bytes(Path(__file__), 5_000_000)).hexdigest()
    result = {
        "status": STATUS,
        "candidate_file_sha256": CANDIDATE_SHA256,
        "candidate_result_sha256": CANDIDATE_RESULT_SHA256,
        "candidate_schema": SCHEMA,
        "producer_sha256": PRODUCER_SHA256,
        "verifier_sha256": verifier_sha256,
        "producer_imported_or_executed": False,
        "independent_reconstruction": {
            "Round222_known_connectivity_blocks": 7640,
            "Round223_unique_sheet_pairs": 7016,
            "Round223_union_rank_reduction": 0,
            "Round224_unique_sheet_pairs": 236,
            "Round224_union_rank_reduction": 236,
            "rebuilt_known_connectivity_blocks": 7404,
            "membership_sha256": R225_MEMBERSHIP_SHA256,
            "remaining_cross_block_missing_contact_frontier": 0,
            "proved_ABSENT_nonedges": 28,
            "all_semantically_material_fields_and_formal_rows_checked": True,
        },
        "attack_suite": {
            "truly_resigned_semantic": semantic_attacks,
            "strict_JSON": json_attacks,
            "path_and_file_object": file_attacks,
        },
        "strict_nonpromotion_reconfirmed": {
            "known_connectivity_blocks_are_maximal_physical_components": False,
            "physical_component_credit": 0,
            "whole_origin_credit": 0,
            "global_exact_key_disposition_credit": 0,
            "source_G_global_exact_key_dispositions": "0/224580",
            "D02": "BLOCKED",
            "global_Gate5_fields": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    envelope = {"schema": VERIFICATION_SCHEMA, "result": result, "result_sha256": digest(result)}
    encoded = canonical_bytes(envelope) + b"\n"
    if not arguments.no_write:
        safe_write(arguments.output, encoded)
    print(STATUS)
    print(f"result_sha256={envelope['result_sha256']}")
    print(f"verification_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("semantic_attacks=12/12_rejected")
    print("strict_JSON_attacks=16/16_rejected")
    print("path_and_file_attacks=10/10_rejected")
    print("producer_imported_or_executed=false")
    print("blocks=7640->7404")
    print("maximal_physical_component_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
