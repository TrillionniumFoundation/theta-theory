#!/usr/bin/env python3
"""C57-L1: collision-one-only edgewise transport over C56-L corridors.

This producer is intentionally fail-closed.  It reconstructs the exact
C38->C39->C40->C41 lineage of every post-C53 pending task in the two large
components and checks the 1,042 rooted-corridor faces.  C36 occurrence 1 and
the frozen C50a owner capability are bound, but their existing scopes do not
prove a dynamic margin/owner/history transport across those C32 faces.
Consequently no collision-two-ready handoff is emitted.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
PREFIX = "cm2_round306c57l1_collision1_edgewise_transport"
SCHEMA = "cm2.round306c57l1.collision1-edgewise-transport.v1"
CHAIN_SCHEMA = SCHEMA + ".upstream-task-chain-row"
LOCAL_SCHEMA = SCHEMA + ".local-collision1-cell-status-row"
EDGE_SCHEMA = SCHEMA + ".edge-transport-row"
CELL_SCHEMA = SCHEMA + ".corridor-cell-transport-row"
HANDOFF_SCHEMA = SCHEMA + ".collision2-ready-handoff-row"

CHAIN_FILE = PREFIX + "_upstream_task_chains_v1.jsonl.gz"
LOCAL_FILE = PREFIX + "_local_collision1_cell_status_v1.jsonl.gz"
EDGE_FILE = PREFIX + "_edge_obligations_v1.jsonl.gz"
CELL_FILE = PREFIX + "_corridor_cell_transport_v1.jsonl.gz"
HANDOFF_FILE = PREFIX + "_collision2_ready_handoff_v1.jsonl.gz"
RESULT_FILE = PREFIX + "_result_v1.json"

C56_RESULT = OUT / "cm2_round306c56l_large_component_common_refinement_result_v1.json"
C56_VERIFY = OUT / "cm2_round306c56l_large_component_common_refinement_independent_verification_v1.json"
C55B_RESULT = OUT / "cm2_round306c55b_global_component_adjacency_known_sheet_result_v1.json"
C35 = ROOT / ".cm2-runtime/candidates/c35-transition-registry-20260810T145204Z-43f2cb35f9817ae2"
C36 = ROOT / ".cm2-runtime/candidates/c36-template-margin-atlas-20260810T153254Z-f37f908cf93d924c"
C38 = ROOT / ".cm2-runtime/candidates/c38-collision1-2-child-atlas-20260810T180156Z-0d5047fe3a316133"
C39 = ROOT / ".cm2-runtime/candidates/c39-h1-c1-graph-router-20260810T185014Z-e004fadaadcd5559"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"
C41 = ROOT / ".cm2-runtime/candidates/c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C50A_MANIFEST = OUT / "cm2_round306c50a_global_codimension_owner_oracle_manifest_v1.sha256"
C50A_PRODUCER = OUT / "cm2_round306c50a_global_codimension_owner_oracle_v1.py"
C50A_VERIFIER = OUT / "cm2_round306c50a_global_codimension_owner_oracle_independent_verifier_v1.py"
C53_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
CANONICAL = OUT / "CM2_LATEST_STATUS.md"

EXPECTED = {
    "C56_RESULT_FILE": "99e5fc0019ae21e7bc68d0c2b997ed62e9c47b28fd47d366237b0c06b1d82601",
    "C56_RESULT_OBJECT": "0ab2c1ea9086db7f05d9b0c7f96d4348b0b2d8c9f54b47bd8e57aa570133a637",
    "C56_VERIFY_FILE": "4a3d90843ee1401b32ef02af3eb5eb9ffdee773c4abeb0d096b9bcfe6e3ae6f2",
    "C56_VERIFY_OBJECT": "c793495f11962757a1e1ac55539ee7260d59d7e084662eb954a8a973466a70a5",
    "C55B_RESULT_FILE": "6bf9cae7b4b422c5c2121f95828e1508700fe1a5d1b1128598c8617f65032a93",
    "C55B_RESULT_OBJECT": "1ce396e9746d3c0364325e8308e94c9dcd4a3bfbba8c17a9c9961915e807cc56",
    "C35_RESULT_FILE": "3122c977e47c1b1f685f7c97f3b9d68e9ff79d477916cb8bd4556f4b518c17ad",
    "C35_OBJECT": "cb524ae587390a578683c88d933125e041ab2a906f0351370d58f3b0d67aa752",
    "C36_RESULT_FILE": "7922139708dc486232ec79b29d6339bdca7e00999bddf63d5b9a83b3f4cfbbd1",
    "C36_OBJECT": "9251693da7d6cc0ff6011fb965276ac64be2b79be8f245ab8954291a43fb4167",
    "C38_RESULT_FILE": "094eb7cf3fca64451aaad80bdd970a8a39a58244e492ed3d2c69f63c70ed3501",
    "C38_OBJECT": "fba83cdd6eb0eb7d0b71989189ad61ba099e0c440b1f31c3c5aa01b9fbc4f434",
    "C39_RESULT_FILE": "f9bfacbdaaf5263ba16397e70fe56b4f31149087c2434b7c163ff284b40cfd7e",
    "C39_OBJECT": "821c84d3793bcd941e0a574302bf6c5a0835b46f852156a56fde6ec0353d7e02",
    "C40_RESULT_FILE": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_OBJECT": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C41_RESULT_FILE": "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    "C41_OBJECT": "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24",
    "C50A_MANIFEST_FILE": "07444544362d8b25d7d5d735e17ad08057dfc459d166ade868a073c2ce4c50f6",
    "C50A_PRODUCER_FILE": "43147808a94e14df20d902db6d7d383f8d230c6685401684bfb9ea697f7e9ed7",
    "C50A_VERIFIER_FILE": "2ae76868e0320563cafbc4a472f3ad1bf292817491d97da1fe68ca9d8e8bd3b4",
    "C53_HEAD_FILE": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "CANONICAL_FILE": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
}

COLLISION2_PREFIX = "UNRESOLVED_C41_COLLISION2_"
SEED_SCOPE = "DUAL_R139_SEED_COLLARS_ONLY"
EDGE_REASON_CODES = [
    "C36_OCCURRENCE1_MARGIN_SCOPE_DUAL_R139_SEED_COLLARS_ONLY",
    "C36_NO_C32_FACE_LIPSCHITZ_OR_VARIATION_BOUND",
    "C50A_NO_FROZEN_C57L1_EDGE_OWNER_REQUEST_OR_AUDIT",
    "NO_C41_SPLIT_HISTORY_COMMON_FACE_CROSSWALK",
]


class FailClosed(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise FailClosed(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key:{path}:{key}")
            result[key] = value
        return result
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream, object_pairs_hook=hook)
    require(type(value) is dict, f"top object:{path}")
    return value


def close_object(value: dict[str, Any], expected: str, label: str, field: str = "object_sha256") -> None:
    semantic = dict(value)
    claim = semantic.pop(field, None)
    require(claim == expected == digest(semantic), f"object closure:{label}")


def close_row(row: dict[str, Any], label: str) -> None:
    semantic = dict(row)
    claim = semantic.pop("row_sha256", None)
    require(type(claim) is str and claim == digest(semantic), f"row closure:{label}")


def sequence_sha(values: Iterable[str]) -> str:
    state = hashlib.sha256()
    for value in values:
        state.update((value + "\n").encode("ascii"))
    return state.hexdigest()


def read_ledger(base: Path, descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    path = base / descriptor["filename"]
    require(path.stat().st_size == descriptor["size"] and file_sha(path) == descriptor["sha256"], f"ledger bytes:{path}")
    rows: list[dict[str, Any]] = []
    sequence = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for index, line in enumerate(stream):
            row = json.loads(line)
            close_row(row, f"{path}:{index}")
            rows.append(row)
            sequence.update((row["row_sha256"] + "\n").encode("ascii"))
    require(len(rows) == descriptor["row_count"], f"ledger count:{path}")
    require(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"], f"ledger sequence:{path}")
    return rows


class Writer:
    def __init__(self, path: Path, order: str) -> None:
        self.path, self.order = path, order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: Any = None
        self.gz: Any = None

    def __enter__(self) -> "Writer":
        self.raw = self.path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        return self

    def write(self, semantic: dict[str, Any]) -> dict[str, Any]:
        require("row_sha256" not in semantic, "writer open row")
        row_hash = digest(semantic)
        row = {**semantic, "row_sha256": row_hash}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row_hash + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args: Any) -> None:
        self.gz.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha(self.path),
            "size": self.path.stat().st_size,
        }


ALGEBRAIC_BOUNDARIES = {"-1/sqrt(2)", "+1/sqrt(2)"}


def exact_token(value: Any) -> str:
    token = value["value"] if isinstance(value, dict) else value
    require(isinstance(token, str), f"exact scalar token:{token!r}")
    if token in ALGEBRAIC_BOUNDARIES:
        return token
    result = Fraction(token)
    require(str(result) == token, f"canonical rational:{token}")
    return token


def exact_compare(left: str, right: str) -> int:
    """Compare the only exact scalar field used by the frozen C32 atlas.

    Besides canonical rationals the atlas has exactly the two source-chart
    boundary tokens +/-1/sqrt(2).  Comparisons with those tokens are reduced
    to a rational comparison against 1/2 after a sign check.
    """
    if left == right:
        return 0
    if left not in ALGEBRAIC_BOUNDARIES and right not in ALGEBRAIC_BOUNDARIES:
        a, b = Fraction(left), Fraction(right)
        return -1 if a < b else 1
    if left in ALGEBRAIC_BOUNDARIES and right in ALGEBRAIC_BOUNDARIES:
        return -1 if left.startswith("-") else 1
    if left in ALGEBRAIC_BOUNDARIES:
        return -exact_compare(right, left)
    rational = Fraction(left)
    if right == "+1/sqrt(2)":
        if rational <= 0:
            return -1
        square = rational * rational
        require(square != Fraction(1, 2), "rational cannot equal +1/sqrt(2)")
        return -1 if square < Fraction(1, 2) else 1
    require(right == "-1/sqrt(2)", "known algebraic boundary")
    if rational >= 0:
        return 1
    square = rational * rational
    require(square != Fraction(1, 2), "rational cannot equal -1/sqrt(2)")
    return -1 if square > Fraction(1, 2) else 1


def exact_min(left: str, right: str) -> str:
    return left if exact_compare(left, right) <= 0 else right


def exact_max(left: str, right: str) -> str:
    return left if exact_compare(left, right) >= 0 else right


def qstr(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def compact_interval(row: dict[str, Any], axis: str) -> tuple[str, str]:
    if axis == "p":
        values = row["physical_p_interval"]
    else:
        values = row["physical_t_interval"]
    low, high = exact_token(values[0]), exact_token(values[1])
    require(exact_compare(low, high) < 0, f"positive {axis} interval:{row['cell_id']}")
    return low, high


def exact_face_check(step: dict[str, Any], left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    require({step["from_cell_id"], step["to_cell_id"]} == {left["cell_id"], right["cell_id"]}, "face endpoints")
    geometry = step["exact_geometry"]
    if step["glue_kind"] == "INTRA_CHART_FACE":
        require(left["compact_chart"] == right["compact_chart"] == geometry["compact_chart"], "intra chart")
        axis = geometry["axis"]
        other = "p" if axis == "t" else "t"
        a0, a1 = compact_interval(left, axis)
        b0, b1 = compact_interval(right, axis)
        shared = a1 if a1 == b0 else b1 if b1 == a0 else None
        require(shared is not None, "shared fixed boundary")
        c0, c1 = compact_interval(left, other)
        d0, d1 = compact_interval(right, other)
        overlap = (exact_max(c0, d0), exact_min(c1, d1))
        require(exact_compare(overlap[0], overlap[1]) < 0, "positive face overlap")
        span = tuple(exact_token(item) for item in geometry["span"])
        require(exact_token(geometry["coordinate"]) == shared and span == overlap, "exact intra face geometry")
        return {
            "kind": "EXACT_INTRA_CHART_COMMON_FACE",
            "axis": axis,
            "fixed_coordinate": shared,
            "span": list(overlap),
            "source_geometry_sha256": digest(geometry),
        }
    require(step["glue_kind"] == "SOURCE_CHART_TRANSITION", "supported corridor glue")
    require(geometry["exact_state_gluing_inherited_from_round162"] is True, "seam state glue")
    require({left["compact_chart"], right["compact_chart"]} == {geometry["left_chart"], geometry["right_chart"]}, "seam charts")
    a0, a1 = compact_interval(left, "p")
    b0, b1 = compact_interval(right, "p")
    overlap = (exact_max(a0, b0), exact_min(a1, b1))
    span = tuple(exact_token(item) for item in geometry["physical_p_span"])
    require(exact_compare(overlap[0], overlap[1]) < 0 and span == overlap, "exact seam span")
    return {
        "kind": "EXACT_SOURCE_CHART_SEAM_COMMON_FACE",
        "seam_id": geometry["seam_id"],
        "physical_p_span": list(overlap),
        "source_geometry_sha256": digest(geometry),
    }


def margin_intervals(margin: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for collar, vector in sorted(margin["collar_margin_vectors"].items()):
        result[collar] = {}
        for field, depth in sorted(vector.items()):
            result[collar][field] = (
                {"applicable": False, "strict_open_lower_bound": None, "upper_bound": None}
                if depth is None
                else {
                    "applicable": True,
                    "dyadic_depth": depth,
                    "strict_open_lower_bound": qstr(Fraction(1, 2**depth)),
                    "upper_bound": None,
                }
            )
    return result


def validate_c50a_manifest() -> list[dict[str, str]]:
    require(file_sha(C50A_MANIFEST) == EXPECTED["C50A_MANIFEST_FILE"], "C50a manifest pin")
    members: list[dict[str, str]] = []
    for line in C50A_MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        path = ROOT / name
        require(path.is_file() and file_sha(path) == expected, f"C50a manifest member:{name}")
        members.append({"filename": name, "sha256": expected})
    require(len(members) == 8, "C50a frozen member count")
    require(file_sha(C50A_PRODUCER) == EXPECTED["C50A_PRODUCER_FILE"], "C50a producer pin")
    require(file_sha(C50A_VERIFIER) == EXPECTED["C50A_VERIFIER_FILE"], "C50a verifier pin")
    require(not any("c57l1" in row["filename"].lower() or "edge" in row["filename"].lower() for row in members), "C50a frozen manifest has unexpected edge request")
    return members


def self_test(summary: dict[str, Any]) -> dict[str, Any]:
    expected = {
        "corridor_cell_count": 1044,
        "unique_rooted_edge_count": 1042,
        "intra_chart_edge_count": 1026,
        "source_seam_edge_count": 16,
        "post_C53_task_chain_count": 33319,
        "local_all_pending_beyond_collision1_cell_count": 350,
        "all_nodes_local_beyond_collision1_corridor_cell_count": 89,
        "edge_transport_pass_count": 0,
        "collision2_ready_handoff_cell_count": 0,
        "collision2_ready_handoff_row_count": 0,
    }
    def guard(value: dict[str, Any]) -> None:
        require(all(value.get(key) == expected_value for key, expected_value in expected.items()), "self-test exact projection")
    guard(summary)
    attacks = {}
    for index, (key, value) in enumerate(expected.items()):
        altered = dict(summary)
        altered[key] = value + 1
        try:
            guard(altered)
        except FailClosed:
            attacks[f"projection_{index}_{key}"] = "FAIL_CLOSED"
        else:
            raise FailClosed(f"attack accepted:{key}")
    return {"status": "PASS_10_OF_10_PRODUCER_ATTACKS_FAIL_CLOSED", "attack_count": 10, "attacks": attacks}


def build() -> dict[str, Any]:
    # Frozen authority/result validation.
    paths = [
        (C56_RESULT, "C56_RESULT_FILE"), (C56_VERIFY, "C56_VERIFY_FILE"),
        (C55B_RESULT, "C55B_RESULT_FILE"), (C35 / "result.json", "C35_RESULT_FILE"),
        (C36 / "result.json", "C36_RESULT_FILE"), (C38 / "result.json", "C38_RESULT_FILE"),
        (C39 / "result.json", "C39_RESULT_FILE"), (C40 / "result.json", "C40_RESULT_FILE"),
        (C41 / "result.json", "C41_RESULT_FILE"),
    ]
    for path, key in paths:
        require(file_sha(path) == EXPECTED[key], f"file pin:{key}")
    c56 = strict_json(C56_RESULT); close_object(c56, EXPECTED["C56_RESULT_OBJECT"], "C56")
    c56_verify = strict_json(C56_VERIFY); close_object(c56_verify, EXPECTED["C56_VERIFY_OBJECT"], "C56 verify")
    c55b = strict_json(C55B_RESULT); close_object(c55b, EXPECTED["C55B_RESULT_OBJECT"], "C55B")
    c35 = strict_json(C35 / "result.json"); close_object(c35, EXPECTED["C35_OBJECT"], "C35")
    c36 = strict_json(C36 / "result.json"); close_object(c36, EXPECTED["C36_OBJECT"], "C36")
    c38 = strict_json(C38 / "result.json"); close_object(c38, EXPECTED["C38_OBJECT"], "C38")
    c39 = strict_json(C39 / "result.json"); close_object(c39, EXPECTED["C39_OBJECT"], "C39")
    c40 = strict_json(C40 / "result.json"); close_object(c40, EXPECTED["C40_OBJECT"], "C40")
    c41 = strict_json(C41 / "result.json"); close_object(c41, EXPECTED["C41_OBJECT"], "C41")
    require(file_sha(C53_HEAD) == EXPECTED["C53_HEAD_FILE"] and file_sha(CANONICAL) == EXPECTED["CANONICAL_FILE"], "installed authority snapshot pins")
    c50a_members = validate_c50a_manifest()

    c56_cells_all = read_ledger(OUT, c56["ledgers"]["corridor_and_separator_cells"])
    c56_cells = [row for row in c56_cells_all if row["witness_kind"] == "EXPLICIT_TOPOLOGICAL_CORRIDOR_TO_STRICT_OPEN_ANCHOR"]
    c56_tasks = read_ledger(OUT, c56["ledgers"]["post_C53_pending_logical_tasks"])
    crosswalk_rows = read_ledger(OUT, c55b["ledgers"]["cell_component_crosswalk"])
    crosswalk = {row["cell_id"]: row for row in crosswalk_rows}
    require(len(c56_cells) == 1044 and len(c56_tasks) == 33319 and len(crosswalk) == 1724, "input scope counts")
    cell_by_id = {row["cell_id"]: row for row in c56_cells}

    occurrences = read_ledger(C35, c35["ledgers"]["path_occurrences"])
    margins = read_ledger(C36, c36["ledgers"]["occurrence_margin_bindings"])
    occurrence1, margin1 = occurrences[0], margins[0]
    require(occurrence1["collision_index"] == margin1["collision_index"] == 1, "occurrence1 index")
    require(occurrence1["row_sha256"] == "815af4b7fd77b884f70178c9a706de9be94be219b66488c9da48fe7b470b8250", "C35 occurrence1 row pin")
    require(margin1["row_sha256"] == "b9238fdb52bf7e3979b7bfdc1beabe5e1d0f2adf10e949f7eeaf13f6a4a7a169", "C36 occurrence1 row pin")
    require(margin1["selected_absolute_owner_id"] == "W[1,0]" and margin1["outgoing_chart"] == "W", "occurrence1 owner/chart")
    require(c36["map_stage_census"]["scope"] == SEED_SCOPE, "C36 scope")
    seed_intervals = margin_intervals(margin1)

    c38_rows = read_ledger(C38, c38["ledgers"]["collision1_2_child_pairs"])
    c39_rows = read_ledger(C39, c39["ledgers"]["routed_child_pairs"])
    c40_rows = read_ledger(C40, c40["ledgers"]["routed_leaf_cells"])
    c38_map = {row["row_sha256"]: row for row in c38_rows}
    c39_map = {row["row_sha256"]: row for row in c39_rows}
    c40_map = {row["row_sha256"]: row for row in c40_rows}
    require(len(c38_map) == 10486 and len(c39_map) == 10486 and len(c40_map) == 35009, "C38-C40 unique rows")

    wanted = {row["C41_routed_ambient_row_sha256"] for row in c56_tasks}
    require(len(wanted) == 33319, "unique C41 wanted hashes")
    c41_selected: dict[str, dict[str, Any]] = {}
    desc = c41["ledgers"]["routed_ambient_cells"]
    c41_path = C41 / desc["filename"]
    require(file_sha(c41_path) == desc["sha256"], "C41 routed file")
    sequence = hashlib.sha256(); count = 0
    with gzip.open(c41_path, "rt", encoding="utf-8") as stream:
        for count, line in enumerate(stream, start=1):
            row = json.loads(line); close_row(row, f"C41 routed:{count}")
            sequence.update((row["row_sha256"] + "\n").encode("ascii"))
            if row["row_sha256"] in wanted:
                c41_selected[row["row_sha256"]] = row
    require(count == desc["row_count"] and sequence.hexdigest() == desc["row_hash_line_sequence_sha256"], "C41 full ledger closure")
    require(set(c41_selected) == wanted, "selected C41 completeness")

    chain_rows_by_blocker: dict[str, list[dict[str, Any]]] = defaultdict(list)
    chain_class_census = Counter()
    with Writer(OUT / CHAIN_FILE, "C56L_POST_C53_TASK_ORDER") as chain_writer:
        for task in c56_tasks:
            c41_row = c41_selected[task["C41_routed_ambient_row_sha256"]]
            c40_row = c40_map[c41_row["c40_source_row_sha256"]]
            c39_row = c39_map[c40_row["c39_source_row_sha256"]]
            c38_row = c38_map[c40_row["c38_source_row_sha256"]]
            require(c39_row["c38_child_row_sha256"] == c38_row["row_sha256"], "C39/C38 chain")
            require(c40_row["c39_source_row_sha256"] == c39_row["row_sha256"] and c40_row["c38_source_row_sha256"] == c38_row["row_sha256"], "C40 chain")
            require(c41_row["pair_index"] == c40_row["pair_index"] == c39_row["pair_index"] == c38_row["pair_index"] == task["pair_index"], "chain pair")
            require(c39_row["path"] == c38_row["path"] and c40_row["source_path"] == c39_row["path"] and c41_row["source_path"] == c40_row["path"], "chain path lineage")
            past_c1 = c41_row["residual_classification"].startswith(COLLISION2_PREFIX)
            semantic = {
                "schema": CHAIN_SCHEMA,
                "pair_index": task["pair_index"],
                "C55A_blocker_row_sha256": task["C55A_blocker_row_sha256"],
                "C56L_task_row_sha256": task["row_sha256"],
                "C41_row_sha256": c41_row["row_sha256"],
                "C41_residual_classification": c41_row["residual_classification"],
                "C41_path": c41_row["path"],
                "C41_split_axis_history": c41_row["split_axis_history"],
                "C40_row_sha256": c40_row["row_sha256"],
                "C40_classification": c40_row["classification"],
                "C40_path": c40_row["path"],
                "C39_row_sha256": c39_row["row_sha256"],
                "C39_classification": c39_row["classification"],
                "C39_route_method": c39_row["route_method"],
                "C39_path": c39_row["path"],
                "C38_row_sha256": c38_row["row_sha256"],
                "C38_classification": c38_row["classification"],
                "C38_first_decision_collision": c38_row["first_decision_collision"],
                "C38_path": c38_row["path"],
                "within_cell_upstream_lineage_exact": True,
                "current_pending_task_beyond_collision1": past_c1,
                "cross_C32_face_occurrence1_history_compatibility_proved": False,
                "formal_credit": 0,
                "D02_gate_credit": 0,
            }
            written = chain_writer.write(semantic)
            chain_rows_by_blocker[task["C55A_blocker_row_sha256"]].append(written)
            chain_class_census[c41_row["residual_classification"]] += 1
    chain_desc = chain_writer.descriptor()

    local_by_cell: dict[str, dict[str, Any]] = {}
    local_class = Counter()
    with Writer(OUT / LOCAL_FILE, "COMPONENT_INDEX_THEN_CELL_ID") as local_writer:
        for cell in c56_cells:
            chains = chain_rows_by_blocker[cell["C55A_blocker_row_sha256"]]
            require(len(chains) == cell["post_C53_pending_logical_task_count_for_pair"], "cell chain count")
            residual = Counter(row["C41_residual_classification"] for row in chains)
            past = all(row["current_pending_task_beyond_collision1"] for row in chains)
            local_class[cell["primary_residual_classification"], past] += 1
            semantic = {
                "schema": LOCAL_SCHEMA,
                "component_index": cell["component_index"],
                "cell_id": cell["cell_id"],
                "pair_index": cell["pair_index"],
                "C56L_cell_row_sha256": cell["row_sha256"],
                "C55A_blocker_row_sha256": cell["C55A_blocker_row_sha256"],
                "primary_residual_classification": cell["primary_residual_classification"],
                "current_pending_task_count": len(chains),
                "C57L1_upstream_chain_row_hash_sequence_sha256": sequence_sha(row["row_sha256"] for row in chains),
                "C41_residual_classification_census": dict(sorted(residual.items())),
                "all_current_pending_tasks_beyond_collision1": past,
                "within_cell_C38_C41_lineage_complete": True,
                "occurrence1_common_face_history_crosswalk_present": False,
                "local_status": "LOCAL_PENDING_FRONTIER_ALL_BEYOND_COLLISION1" if past else "LOCAL_PENDING_FRONTIER_RETAINS_COLLISION1_OR_LOWER_STRATA",
                "collision2_ready_edgewise_handoff_credit": 0,
                "D02_gate_credit": 0,
            }
            local_by_cell[cell["cell_id"]] = local_writer.write(semantic)
    local_desc = local_writer.descriptor()
    require(sum(row["all_current_pending_tasks_beyond_collision1"] for row in local_by_cell.values()) == 350, "350 local-beyond-C1 cells")

    # Each non-anchor cell owns the first edge in its rooted C56-L corridor.
    edge_by_source: dict[str, dict[str, Any]] = {}
    edge_kind = Counter(); endpoint_state = Counter()
    with Writer(OUT / EDGE_FILE, "COMPONENT_INDEX_THEN_SOURCE_CELL_ID") as edge_writer:
        for cell in c56_cells:
            if cell["corridor_step_count"] == 0:
                continue
            step = cell["corridor_steps"][0]
            require(step["from_cell_id"] == cell["cell_id"], "rooted first step source")
            source, target = crosswalk[step["from_cell_id"]], crosswalk[step["to_cell_id"]]
            face = exact_face_check(step, source, target)
            source_local, target_local = local_by_cell[source["cell_id"]], local_by_cell[target["cell_id"]]
            both_local = source_local["all_current_pending_tasks_beyond_collision1"] and target_local["all_current_pending_tasks_beyond_collision1"]
            reasons = list(EDGE_REASON_CODES)
            if step["glue_kind"] == "SOURCE_CHART_TRANSITION":
                reasons.append("SOURCE_SEAM_DYNAMIC_OCCURRENCE1_GLUE_NOT_MATERIALIZED")
            if not both_local:
                reasons.append("EDGE_ENDPOINT_LOCAL_COLLISION1_FRONTIER_NOT_BOTH_COMPLETE")
            edge_kind[step["glue_kind"]] += 1
            endpoint_state[(source_local["all_current_pending_tasks_beyond_collision1"], target_local["all_current_pending_tasks_beyond_collision1"], step["glue_kind"])] += 1
            semantic = {
                "schema": EDGE_SCHEMA,
                "component_index": cell["component_index"],
                "source_cell_id": source["cell_id"],
                "target_cell_id": target["cell_id"],
                "C56L_source_cell_row_sha256": cell["row_sha256"],
                "C55B_edge_row_sha256": step["C55B_edge_row_sha256"],
                "upstream_face_or_seam_row_sha256": step["upstream_row_sha256"],
                "face_or_corner_id": step["face_or_corner_id"],
                "glue_kind": step["glue_kind"],
                "exact_common_face_refinement": face,
                "exact_common_face_refinement_materialized": True,
                "source_local_status_row_sha256": source_local["row_sha256"],
                "target_local_status_row_sha256": target_local["row_sha256"],
                "both_endpoint_pending_frontiers_beyond_collision1": both_local,
                "C35_occurrence1_row_sha256": occurrence1["row_sha256"],
                "C36_occurrence1_margin_row_sha256": margin1["row_sha256"],
                "C36_seed_collar_scope": SEED_SCOPE,
                "C36_seed_collar_named_strict_margin_intervals": seed_intervals,
                "transported_edge_strict_margin_intervals": None,
                "C36_C32_face_Lipschitz_or_variation_bound_present": False,
                "C50a_owner_protocol": "CM2_FULL_UNIVERSE_FACE_CORNER_OWNER_V1",
                "C50a_frozen_edge_request_present": False,
                "C50a_frozen_edge_independent_audit_present": False,
                "endpoint_occurrence1_owner_compatibility_proved": False,
                "endpoint_occurrence1_owner_compatibility_disproved": False,
                "endpoint_split_history_common_face_compatibility_proved": False,
                "endpoint_split_history_common_face_compatibility_disproved": False,
                "edge_transport_pass": False,
                "reason_codes": reasons,
                "collision2_ready_handoff_credit": 0,
                "D02_gate_credit": 0,
            }
            written = edge_writer.write(semantic)
            require(source["cell_id"] not in edge_by_source, "unique rooted source edge")
            edge_by_source[source["cell_id"]] = written
    edge_desc = edge_writer.descriptor()
    require(edge_desc["row_count"] == 1042 and edge_kind == Counter({"INTRA_CHART_FACE": 1026, "SOURCE_CHART_TRANSITION": 16}), "edge census")

    # Whole-corridor cell decision.  Even the two anchors remain blocked: the
    # C36 collar has not been promoted to a whole C32-cell variation theorem.
    all_nodes_count = 0
    class_accounting: dict[str, Counter[str]] = defaultdict(Counter)
    cell_transport_rows: list[dict[str, Any]] = []
    with Writer(OUT / CELL_FILE, "COMPONENT_INDEX_THEN_CELL_ID") as cell_writer:
        for cell in c56_cells:
            node_ids = [cell["cell_id"]] + [step["to_cell_id"] for step in cell["corridor_steps"]]
            all_nodes = all(local_by_cell[node]["all_current_pending_tasks_beyond_collision1"] for node in node_ids)
            all_nodes_count += int(all_nodes)
            path_edge_rows = [edge_by_source[step["from_cell_id"]] for step in cell["corridor_steps"]]
            require(all(row["C55B_edge_row_sha256"] == step["C55B_edge_row_sha256"] for row, step in zip(path_edge_rows, cell["corridor_steps"], strict=True)), "path edge binding")
            local = local_by_cell[cell["cell_id"]]
            reasons = []
            if not local["all_current_pending_tasks_beyond_collision1"]:
                reasons.append("LOCAL_CELL_RETAINS_COLLISION1_OR_LOWER_STRATA_PENDING_TASK")
            if not all_nodes:
                reasons.append("CORRIDOR_CONTAINS_NODE_WITH_INCOMPLETE_LOCAL_COLLISION1_FRONTIER")
            if cell["corridor_step_count"] == 0:
                reasons.append("ANCHOR_C36_SEED_COLLAR_NOT_PROMOTED_TO_WHOLE_C32_CELL")
            else:
                reasons.extend([
                    "PATH_EDGE_C36_LIPSCHITZ_OR_VARIATION_TRANSPORT_MISSING",
                    "PATH_EDGE_C50A_OWNER_REQUESTS_AND_AUDITS_MISSING",
                    "PATH_EDGE_SPLIT_HISTORY_COMMON_FACE_COMPATIBILITY_MISSING",
                ])
            primary = cell["primary_residual_classification"]
            class_accounting[primary]["corridor_cells"] += 1
            class_accounting[primary]["local_beyond_C1_cells"] += int(local["all_current_pending_tasks_beyond_collision1"])
            class_accounting[primary]["all_nodes_beyond_C1_cells"] += int(all_nodes)
            class_accounting[primary]["transport_pass_cells"] += 0
            semantic = {
                "schema": CELL_SCHEMA,
                "component_index": cell["component_index"],
                "cell_id": cell["cell_id"],
                "pair_index": cell["pair_index"],
                "primary_residual_classification": primary,
                "C56L_cell_row_sha256": cell["row_sha256"],
                "local_collision1_status_row_sha256": local["row_sha256"],
                "corridor_step_count": cell["corridor_step_count"],
                "corridor_edge_transport_row_hash_sequence_sha256": sequence_sha(row["row_sha256"] for row in path_edge_rows),
                "all_current_cell_pending_tasks_beyond_collision1": local["all_current_pending_tasks_beyond_collision1"],
                "all_corridor_nodes_local_pending_frontiers_beyond_collision1": all_nodes,
                "all_corridor_exact_common_faces_materialized": True,
                "all_corridor_edge_margin_transports_proved": False,
                "all_corridor_edge_owner_compatibilities_proved": False,
                "all_corridor_edge_history_compatibilities_proved": False,
                "collision1_edgewise_transport_pass": False,
                "failure_reason_codes": reasons,
                "collision2_ready_handoff": False,
                "collision2_ready_handoff_credit": 0,
                "formal_credit": 0,
                "D02_gate_credit": 0,
            }
            cell_transport_rows.append(cell_writer.write(semantic))
    cell_desc = cell_writer.descriptor()
    require(all_nodes_count == 89, "89 all-nodes local condition")

    # A deterministic empty handoff is semantically significant.
    with Writer(OUT / HANDOFF_FILE, "EMPTY_NO_COLLISION2_READY_HANDOFFS") as handoff_writer:
        pass
    handoff_desc = handoff_writer.descriptor()
    require(handoff_desc["row_count"] == 0, "zero handoff rows")

    class_rows = []
    for primary in sorted(class_accounting):
        counts = class_accounting[primary]
        class_rows.append({
            "primary_residual_classification": primary,
            "corridor_cell_count": counts["corridor_cells"],
            "local_all_pending_beyond_collision1_cell_count": counts["local_beyond_C1_cells"],
            "all_nodes_local_beyond_collision1_corridor_cell_count": counts["all_nodes_beyond_C1_cells"],
            "edgewise_transport_pass_cell_count": 0,
            "collision2_ready_handoff_cell_count": 0,
            "remaining_cell_count": counts["corridor_cells"],
        })

    summary = {
        "corridor_cell_count": 1044,
        "unique_rooted_edge_count": 1042,
        "intra_chart_edge_count": 1026,
        "source_seam_edge_count": 16,
        "post_C53_task_chain_count": 33319,
        "local_all_pending_beyond_collision1_cell_count": 350,
        "all_nodes_local_beyond_collision1_corridor_cell_count": 89,
        "edge_transport_pass_count": 0,
        "collision2_ready_handoff_cell_count": 0,
        "collision2_ready_handoff_row_count": 0,
    }
    test = self_test(summary)
    result: dict[str, Any] = {
        "schema": SCHEMA + ".result",
        "status": "PASS_EXACT_COLLISION1_EDGE_OBLIGATION_MATERIALIZATION__1042_OF_1042_COMMON_FACES__FAIL_CLOSED_0_OF_1044_TRANSPORTED__NO_COLLISION2_READY_HANDOFF",
        "authority_binding": {
            "C56L_result_file_sha256": EXPECTED["C56_RESULT_FILE"],
            "C56L_result_object_sha256": EXPECTED["C56_RESULT_OBJECT"],
            "C56L_independent_verification_file_sha256": EXPECTED["C56_VERIFY_FILE"],
            "C56L_independent_verification_object_sha256": EXPECTED["C56_VERIFY_OBJECT"],
            "C35_object_sha256": EXPECTED["C35_OBJECT"],
            "C36_object_sha256": EXPECTED["C36_OBJECT"],
            "C38_object_sha256": EXPECTED["C38_OBJECT"],
            "C39_object_sha256": EXPECTED["C39_OBJECT"],
            "C40_object_sha256": EXPECTED["C40_OBJECT"],
            "C41_object_sha256": EXPECTED["C41_OBJECT"],
            "C50a_manifest_file_sha256": EXPECTED["C50A_MANIFEST_FILE"],
            "C50a_producer_file_sha256": EXPECTED["C50A_PRODUCER_FILE"],
            "C50a_independent_verifier_file_sha256": EXPECTED["C50A_VERIFIER_FILE"],
            "C50a_frozen_manifest_members": c50a_members,
            "C53_head_file_sha256": EXPECTED["C53_HEAD_FILE"],
            "canonical_file_sha256": EXPECTED["CANONICAL_FILE"],
        },
        "occurrence1_binding": {
            "C35_occurrence1_row_sha256": occurrence1["row_sha256"],
            "C36_occurrence1_margin_row_sha256": margin1["row_sha256"],
            "selected_absolute_owner_id": margin1["selected_absolute_owner_id"],
            "incoming_chart": margin1["incoming_chart"],
            "outgoing_chart": margin1["outgoing_chart"],
            "C36_atlas_scope": SEED_SCOPE,
            "seed_collar_named_strict_margin_intervals": seed_intervals,
            "whole_C32_face_variation_transport_proved": False,
        },
        "scope": summary,
        "edge_endpoint_local_status_census": {
            f"source_{str(source).lower()}__target_{str(target).lower()}__{kind}": value
            for (source, target, kind), value in sorted(endpoint_state.items(), key=lambda item: str(item[0]))
        },
        "primary_residual_classification_accounting": class_rows,
        "C41_selected_task_residual_classification_census": dict(sorted(chain_class_census.items())),
        "proof_boundary": {
            "exact_C32_common_face_or_source_seam_geometry_materialized": True,
            "within_cell_C38_C41_lineage_materialized": True,
            "C36_occurrence1_seed_collar_margin_bound": True,
            "C36_edge_Lipschitz_or_variation_transport": False,
            "C50a_frozen_C57L1_edge_owner_requests_and_audits": False,
            "cross_edge_C41_split_history_compatibility": False,
            "atlas_adjacency_promoted_to_dynamic_transport": False,
        },
        "formal_effect": {
            "collision2_ready_handoff_credit": 0,
            "whole_cell_CONNECTED_TO_KNOWN_credit": 0,
            "formal_credit": 0,
            "D02_gate_credit": 0,
            "installed_four_class_census_unchanged": True,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "ledgers": {
            "upstream_task_chains": chain_desc,
            "local_collision1_cell_status": local_desc,
            "edge_obligations": edge_desc,
            "corridor_cell_transport": cell_desc,
            "collision2_ready_handoff": handoff_desc,
        },
        "self_test": test,
        "required_next": [
            "FREEZE_1042_C50A_STYLE_EDGE_OWNER_REQUESTS_AND_INDEPENDENT_AUDITS",
            "PROVE_C36_OCCURRENCE1_LIPSCHITZ_OR_VARIATION_MARGIN_TRANSPORT_ON_1026_INTRA_FACES_AND_16_SOURCE_SEAMS",
            "MATERIALIZE_C38_C41_SPLIT_HISTORY_COMMON_FACE_COMPATIBILITY_FOR_BOTH_ENDPOINTS_OF_EACH_EDGE",
            "REPLAY_THE_1044_CELL_CORRIDORS_AND_EMIT_COLLISION2_READY_HANDOFF_ONLY_WHEN_EVERY_EDGE_PASSES_ALL_THREE_GATES",
        ],
    }
    result["object_sha256"] = digest(result)
    (OUT / RESULT_FILE).write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    result = build()
    print(json.dumps({"status": result["status"], "object_sha256": result["object_sha256"], "scope": result["scope"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FailClosed, OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"FAIL_CLOSED:{type(exc).__name__}:{exc}", file=sys.stderr)
        raise SystemExit(2)
