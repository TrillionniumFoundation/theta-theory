#!/usr/bin/env python3
"""C43B0: read-only adaptive pilot for five post-C42 sole-deficit parents.

This program never writes below ``.cm2-runtime`` and has no candidate,
authority, receipt, seal, output-path, or promotion mode.  It first validates
the installed C42 f1 authority transaction and the pinned C41 lineage.  It
then resumes C41 ``route_at_path`` at the unique residual descendant of pairs
97, 211, 592, 664, and 715.

Adaptive dyadic subdivision stops a branch only when it reaches a strict
``TERMINAL_EXCLUDED`` or ``COLLISION3_READY`` D02-A exit.  A branch that reaches
the finite pilot budget is reported only as a zero-credit checkpoint.  The
stdout JSON is exploratory evidence, never a candidate or authority object.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Callable


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
sys.path.insert(0, str(SELF.parent))

import cm2_round306c41_d02_lower_strata_depth3_closure_v1 as c41
import cm2_round306c42_f1_authority_transaction_independent_auditor_v1 as c42tx


RUNTIME = ROOT / ".cm2-runtime"
AUDIT_ROOT = RUNTIME / "audit"

SCHEMA = "cm2.round306c43b0.d02-sole-deficit-adaptive-pilot.v1"
TARGET_PAIRS = (97, 211, 592, 664, 715)
START_PARENT_VOLUME = Q(1, 512)

C41_TOKEN = "c41-lower-strata-depth3-20260811T023804Z-f997365c91559599"
C41_AUDIT_TOKEN = "c41-independent-audit-20260811T031547Z-ab94d420c43c94cd"
C42_TOKEN = "c42-p391-formal-producer-20260811T044500Z-f1"
C42_AUDIT_TOKEN = "c42-independent-audit-20260811T052900Z-p391-f1"
C42_RELEASE = "c42-f1-authority-install-a50914a266af-85a7cd719cee-v1"

C41_DIR = RUNTIME / "candidates" / C41_TOKEN
C42_DIR = RUNTIME / "candidates" / C42_TOKEN
C42_RECEIPT = AUDIT_ROOT / C42_RELEASE / "installation_receipt.json"

EXPECTED_C41_OBJECT = (
    "b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24"
)
EXPECTED_C42_OBJECT = (
    "a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2"
)
EXPECTED_C42_AUDIT_OBJECT = (
    "85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c"
)
EXPECTED_C42_SEAL_OBJECT = (
    "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460"
)
EXPECTED_C42_RECEIPT_OBJECT = (
    "c5f2eb78a0d9d717326bc57fb14df823ab3c5181e3e613a0327425c5e33e784e"
)
EXPECTED_C41_SOURCE_SHA256 = (
    "3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde"
)
EXPECTED_C42_TRANSACTION_AUDITOR_SHA256 = (
    "a37bf76da4674831c90d4e5839e7134b7ebfd9167a0a60840996a331039a06e2"
)

PINNED_FILES = {
    "c42_candidate_pointer": (
        ".cm2-runtime/c42-current-token",
        "fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07",
    ),
    "c42_audit_pointer": (
        ".cm2-runtime/c42-current-audit-token",
        "59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5",
    ),
    "c42_authority_seal": (
        ".cm2-runtime/c42-current-authority-seal",
        "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d",
    ),
    "c42_installation_receipt": (
        f".cm2-runtime/audit/{C42_RELEASE}/installation_receipt.json",
        "3599494ff330a367a6c27ee57c19c01e86626428871d014c9153f290fdfc407f",
    ),
    "c42_result": (
        f".cm2-runtime/candidates/{C42_TOKEN}/result.json",
        "f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0",
    ),
    "c42_independent_audit": (
        f".cm2-runtime/audit/{C42_AUDIT_TOKEN}/independent_audit.json",
        "d60bb3c8f79f989df776effa4616ec170097a018547b1f4c929ad068c11138d3",
    ),
    "c41_candidate_pointer": (
        ".cm2-runtime/c41-current-token",
        "9e4f2d9c02c1f3e56639d69c971ccc7846ba229f87723e878f101730df3dd1a9",
    ),
    "c41_audit_pointer": (
        ".cm2-runtime/c41-current-audit-token",
        "f8a9a0bf69169eba05ef3bec1db7e924de4b06b4ab61c97693b2919effd9c86c",
    ),
    "c41_result": (
        f".cm2-runtime/candidates/{C41_TOKEN}/result.json",
        "73fde0eee7eb06bb0f144ea98880c72bfea36e10db696731ae72393cd9b0a50f",
    ),
    "c41_manifest": (
        f".cm2-runtime/candidates/{C41_TOKEN}/root_manifest.sha256",
        "86e10532d63269cd0fdd58d541b1984522e9718f4613a5dc83211fe84eb258ba",
    ),
    "c41_independent_audit": (
        f".cm2-runtime/audit/{C41_AUDIT_TOKEN}/independent_audit.json",
        "6a800959a90c227d587b82c6246f60123483471f61dcf6a5de4da5381fee4b1e",
    ),
    "c41_source": (
        "deliverables/cm2_round306c41_d02_lower_strata_depth3_closure_v1.py",
        EXPECTED_C41_SOURCE_SHA256,
    ),
    "c42_transaction_auditor_source": (
        "deliverables/"
        "cm2_round306c42_f1_authority_transaction_independent_auditor_v1.py",
        EXPECTED_C42_TRANSACTION_AUDITOR_SHA256,
    ),
}

EXPECTED_TARGETS: dict[int, dict[str, str]] = {
    97: {
        "descendant_path": "111111111",
        "c40_leaf_id": "c40-leaf:d2f84a6eacae6bace954ddd09130d12687d4465ce89316827d35637e0d58febf",
        "c40_row_sha256": "f2e1f153deb87534f1cfa21e3131363c62dbb18eda2054b4991b4017d58b9510",
        "c41_ambient_row_sha256": "2db22144ca16f31dd528835a879e38bf4362c8c7a9b6397c0a29a5f8c92b5767",
        "c41_parent_row_sha256": "6e309c2576f5862630465bb81fa38af3bba0b650852ad111b7fbf0c1c7d67762",
        "c42_parent_row_sha256": "b0f74ff6812a75e9d69bf2e11cfc99ec1e9f8eb43c0ab527152ce4b658d9aa3e",
        "raw_classification": "UNRESOLVED_C40_COLLISION2_WALL_ENDPOINT",
        "residual_classification": "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER",
    },
    211: {
        "descendant_path": "111111111",
        "c40_leaf_id": "c40-leaf:7e0b721bd80687cd3bd1f8fffe0369f3c0ebc7273e3cf941178a9d7a8fc5edb3",
        "c40_row_sha256": "1f8a4094d17cd5f5f888116098c03f97ad62a4df71e44e024930a020df45432a",
        "c41_ambient_row_sha256": "ddc554f00da31c5c4b21ec51de3a49eb0f62ed984f2843ae673bf34ce3b06fc4",
        "c41_parent_row_sha256": "04b77d56f4e96466504972ed3730b7a9bf92364cd6b2f8b64acecdb92cc64600",
        "c42_parent_row_sha256": "bd464fa2e1cefd063860022026758026ba7cc8fbfb399fa323fb2f36f7762064",
        "raw_classification": "UNRESOLVED_C40_COLLISION2_WALL_ENDPOINT",
        "residual_classification": "UNRESOLVED_C41_COLLISION2_WALL_ENDPOINT_OUTER",
    },
    592: {
        "descendant_path": "000000000",
        "c40_leaf_id": "c40-leaf:e34e9616160fabac64fde47c92755efdc8f1f2d93e7ac798f2ff3eab2947f33b",
        "c40_row_sha256": "c804684bb3961f7b60134e7d168488ca0dc30f1fb49bec612b3e301e91d2ab89",
        "c41_ambient_row_sha256": "bf089245fa0f96196014cbd425b0b3d3e265b0350477779f731b32dc05f8985e",
        "c41_parent_row_sha256": "2ba14f7e7e8b89c548ffbafa81168770f53780d287eeeee2396938ceb8fa6e99",
        "c42_parent_row_sha256": "cbb5a195348f179a6e243af79faff1cb1abf7da0d05f76ec63a1b464ce5d3631",
        "raw_classification": "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE",
        "residual_classification": "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER",
    },
    664: {
        "descendant_path": "010101010",
        "c40_leaf_id": "c40-leaf:c2e98c22c8d0a87abbd19189d6262a9c81c8a88322ae18ff91ee8ceb73bca4a3",
        "c40_row_sha256": "498cdf8a6d00f7c2b9839eec811710643bf77615268023bf25cc57b7e2d1ea7e",
        "c41_ambient_row_sha256": "395f8ef977aece344cb2e9b6950c4cc5734e3795aa34a7ffdccc73c6616601ba",
        "c41_parent_row_sha256": "d93a77969d0452e5fdcba3e7a42cea4303725f3ba5333335828b7ad8bee05244",
        "c42_parent_row_sha256": "e992c0ff2e0a005bacf10de761ab6ea14b093932d3764353f378df1f71c81fc0",
        "raw_classification": "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE",
        "residual_classification": "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER",
    },
    715: {
        "descendant_path": "101010101",
        "c40_leaf_id": "c40-leaf:d2768eebbaf3c62ad68b42b636552586b60875f79121e40422e31bc595869459",
        "c40_row_sha256": "15796e01b7e552f453ae3e9ac4fe145ca1e35c393a9694a68a46aba3b2884c5a",
        "c41_ambient_row_sha256": "24b8a1114e0bda5b0ff4d88b8f7daddfd6b009724fb2e418ea9ac52de42df349",
        "c41_parent_row_sha256": "9c26d3272b8d541ac5856b7f674a44007fea3eb62ac881d8a7d1aa0653cf3354",
        "c42_parent_row_sha256": "dda2b4afca3fe326ac76c48b6e96ef68fda9c04da368d6a6b468fc2fab866920",
        "raw_classification": "UNRESOLVED_C39_C1_ENHANCED_W_SIDE_COLLISION1_OUTGOING_STATE",
        "residual_classification": "UNRESOLVED_C41_C1_OUTGOING_H1_FACTOR_OUTER",
    },
}


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def fingerprint(info: os.stat_result) -> list[int]:
    return [
        info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size,
        info.st_mtime_ns, info.st_ctime_ns, info.st_uid, info.st_gid,
    ]


def directory_fingerprint(path: Path) -> list[int]:
    info = os.stat(path, follow_symlinks=False)
    require(stat.S_ISDIR(info.st_mode), "runtime snapshot directory:" + str(path))
    return fingerprint(info)


def lexical_no_symlinks(path: Path, label: str) -> None:
    path = path.absolute()
    require(path == ROOT or ROOT in path.parents, label + ": workspace boundary")
    cursor = ROOT
    require(stat.S_ISDIR(os.lstat(cursor).st_mode), label + ": root directory")
    for part in path.relative_to(ROOT).parts:
        cursor /= part
        require(not stat.S_ISLNK(os.lstat(cursor).st_mode),
                label + ": no symlink component")


class Capture:
    """Hold one singleton input open and re-attest it after the pilot."""

    def __init__(self, path: Path, expected_sha256: str | None, label: str,
                 maximum: int = 1 << 30):
        self.path = path.absolute()
        self.label = label
        lexical_no_symlinks(self.path.parent, label + " parent")
        self.fd = os.open(
            self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
        )
        self.before = os.fstat(self.fd)
        require(
            stat.S_ISREG(self.before.st_mode)
            and self.before.st_nlink == 1
            and self.before.st_uid == os.getuid()
            and 0 <= self.before.st_size <= maximum,
            label + ": singleton owned bounded regular",
        )
        self.raw = self._read()
        self.sha256 = hashlib.sha256(self.raw).hexdigest()
        if expected_sha256 is not None:
            require(self.sha256 == expected_sha256, label + ": SHA256 pin")
        self.unchanged("initial")

    def _read(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        total = 0
        while block := os.read(self.fd, 1 << 20):
            chunks.append(block)
            total += len(block)
            require(total <= self.before.st_size, self.label + ": read bound")
        os.lseek(self.fd, 0, os.SEEK_SET)
        require(total == self.before.st_size, self.label + ": exact read size")
        return b"".join(chunks)

    def unchanged(self, phase: str) -> None:
        current = os.stat(self.path, follow_symlinks=False)
        require(
            fingerprint(current) == fingerprint(self.before)
            == fingerprint(os.fstat(self.fd)),
            self.label + ": " + phase + " stat identity",
        )
        require(hashlib.sha256(self._read()).hexdigest() == self.sha256,
                self.label + ": " + phase + " bytes")

    def close(self) -> None:
        os.close(self.fd)


Leaf = dict[str, Any]
ChildBuilder = Callable[[str, dict[str, Any]], tuple[list[tuple[str, dict[str, Any]]], str]]


def adaptive_traverse(
    start_path: str,
    initial_route: dict[str, Any],
    max_depth: int,
    max_routes: int,
    child_builder: ChildBuilder,
) -> dict[str, Any]:
    require(max_depth >= 0 and max_routes >= 1, "positive adaptive budget")
    stack: list[tuple[str, int, dict[str, Any]]] = [
        (start_path, 0, initial_route)
    ]
    leaves: list[Leaf] = []
    route_count = 1
    split_count = 0
    split_axes: Counter[str] = Counter()
    while stack:
        path, depth, route = stack.pop()
        classification = route["classification"]
        family = c41.disposition_family(classification)
        if family in {"TERMINAL_EXCLUDED", "COLLISION3_READY"}:
            stop = "D02_A_EXIT"
        elif depth >= max_depth:
            stop = "CHECKPOINT_MAX_DEPTH"
        elif route_count + 2 > max_routes:
            stop = "CHECKPOINT_ROUTE_BUDGET"
        else:
            children, axis = child_builder(path, route)
            require(
                len(children) == 2
                and children[0][0] == path + "0"
                and children[1][0] == path + "1",
                "exact binary child paths",
            )
            route_count += 2
            split_count += 1
            split_axes[axis] += 1
            stack.append((children[1][0], depth + 1, children[1][1]))
            stack.append((children[0][0], depth + 1, children[0][1]))
            continue
        leaves.append({
            "path": path,
            "additional_depth": depth,
            "family": family,
            "classification": classification,
            "stop": stop,
        })

    leaves.sort(key=lambda row: row["path"])
    paths = [row["path"] for row in leaves]
    require(
        len(paths) == len(set(paths))
        and all(
            not right.startswith(left)
            for index, left in enumerate(paths)
            for right in paths[index + 1:]
        ),
        "adaptive leaf prefix freedom",
    )
    relative_kraft = sum(Q(1, 2 ** row["additional_depth"]) for row in leaves)
    require(relative_kraft == 1, "adaptive relative Kraft conservation")
    return {
        "leaves": leaves,
        "route_evaluation_count": route_count,
        "split_count": split_count,
        "split_axis_census": dict(sorted(split_axes.items())),
        "relative_kraft_sum": qstr(relative_kraft),
    }


def summarize_traversal(pair_index: int, start_row: dict[str, Any],
                        traversal: dict[str, Any]) -> dict[str, Any]:
    leaves = traversal["leaves"]
    exits = [row for row in leaves if row["stop"] == "D02_A_EXIT"]
    checkpoints = [row for row in leaves if row["stop"] != "D02_A_EXIT"]

    def census(rows: list[Leaf], field: str) -> dict[str, int]:
        return dict(sorted(Counter(row[field] for row in rows).items()))

    def relative_volume(rows: list[Leaf]) -> Q:
        return sum(Q(1, 2 ** row["additional_depth"]) for row in rows)

    terminal = [row for row in exits if row["family"] == "TERMINAL_EXCLUDED"]
    ready = [row for row in exits if row["family"] == "COLLISION3_READY"]
    checkpoint_relative = relative_volume(checkpoints)
    exit_relative = relative_volume(exits)
    require(checkpoint_relative + exit_relative == 1,
            "pair exit/checkpoint conservation")
    return {
        "pair_index": pair_index,
        "C41_descendant_path": start_row["path"],
        "C41_start_raw_classification": start_row["raw_classification"],
        "C41_start_residual_classification": start_row["residual_classification"],
        "C41_start_parent_volume_fraction": start_row["parent_volume_fraction"],
        "route_evaluation_count": traversal["route_evaluation_count"],
        "split_count": traversal["split_count"],
        "split_axis_census": traversal["split_axis_census"],
        "leaf_count": len(leaves),
        "deepest_additional_depth": max(row["additional_depth"] for row in leaves),
        "leaf_path_sequence_sha256": digest([row["path"] for row in leaves]),
        "relative_Kraft_sum": traversal["relative_kraft_sum"],
        "D02_A_exit_leaf_count": len(exits),
        "D02_A_exit_family_census": census(exits, "family"),
        "D02_A_exit_classification_census": census(exits, "classification"),
        "terminal_excluded_exit_leaf_count": len(terminal),
        "collision3_ready_exit_leaf_count": len(ready),
        "checkpoint_leaf_count": len(checkpoints),
        "checkpoint_reason_census": census(checkpoints, "stop"),
        "checkpoint_classification_census": census(
            checkpoints, "classification"
        ),
        "relative_exit_volume": qstr(exit_relative),
        "relative_checkpoint_volume": qstr(checkpoint_relative),
        "absolute_parent_exit_volume": qstr(START_PARENT_VOLUME * exit_relative),
        "absolute_parent_checkpoint_volume": qstr(
            START_PARENT_VOLUME * checkpoint_relative
        ),
        "ambient_credit_issued": 0,
        "D02_gate_credit_issued": 0,
        "formal_credit_issued": False,
    }


def validate_target_rows(
    c41_result: dict[str, Any], c42_result: dict[str, Any]
) -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]]]:
    c41_rows: dict[int, dict[str, Any]] = {}
    for row in c41.iter_ledger(
        C41_DIR, c41_result["ledgers"]["routed_ambient_cells"]
    ):
        pair = row["pair_index"]
        if pair not in EXPECTED_TARGETS or row["disposition_family"] == "TERMINAL_EXCLUDED":
            continue
        require(pair not in c41_rows, "unique C41 sole residual:" + str(pair))
        c41_rows[pair] = row
    require(set(c41_rows) == set(TARGET_PAIRS), "five C41 sole residual rows")

    c42_parent_rows: dict[int, dict[str, Any]] = {}
    for row in c41.iter_ledger(
        C42_DIR, c42_result["ledgers"]["parent_conservation"]
    ):
        if row["pair_index"] in EXPECTED_TARGETS:
            c42_parent_rows[row["pair_index"]] = row
    require(set(c42_parent_rows) == set(TARGET_PAIRS), "five C42 parent rows")

    for pair in TARGET_PAIRS:
        expected = EXPECTED_TARGETS[pair]
        row = c41_rows[pair]
        require(
            row["path"] == expected["descendant_path"]
            and row["c40_source_leaf_id"] == expected["c40_leaf_id"]
            and row["c40_source_row_sha256"] == expected["c40_row_sha256"]
            and row["row_sha256"] == expected["c41_ambient_row_sha256"]
            and row["raw_classification"] == expected["raw_classification"]
            and row["residual_classification"]
            == expected["residual_classification"]
            and row["disposition_family"] == "RESIDUAL_OUTER"
            and Q(row["parent_volume_fraction"]) == START_PARENT_VOLUME
            and row["local_round144_terminal_credit"] == 0
            and row["lower_dimensional_ambient_credit"] == 0
            and row["D02_gate_credit"] == 0,
            "exact C41 sole residual binding:" + str(pair),
        )
        parent = c42_parent_rows[pair]
        require(
            parent["row_sha256"] == expected["c42_parent_row_sha256"]
            and parent["C41_parent_row_sha256"]
            == expected["c41_parent_row_sha256"]
            and parent["C41_unresolved_parent_volume"] == "1/512"
            and parent["unresolved_parent_volume"] == "1/512"
            and parent["terminal_excluded_parent_volume"] == "511/512"
            and parent["nonterminal_leaf_count"] == 1
            and parent["C42_terminal_gain"] == "0"
            and parent["newly_whole_terminal_vs_C41"] is False
            and parent["C34_common_refinement_credit"] == 0
            and parent["D02_gate_credit"] == 0,
            "exact post-C42 sole-deficit parent:" + str(pair),
        )
    return c41_rows, c42_parent_rows


def load_c40_tasks(
    context: dict[str, Any], c41_rows: dict[int, dict[str, Any]]
) -> dict[int, dict[str, Any]]:
    wanted = {
        EXPECTED_TARGETS[pair]["c40_leaf_id"]: pair for pair in TARGET_PAIRS
    }
    tasks: dict[int, dict[str, Any]] = {}
    # The context result is the pinned C40 result; its candidate directory is
    # supplied independently by the caller and retained in this private key.
    source_dir: Path = context["_C43B0_C40_directory"]
    for ordinal, source in enumerate(c41.iter_ledger(
        source_dir, context["result"]["ledgers"]["routed_leaf_cells"]
    )):
        pair = wanted.get(source["c40_leaf_id"])
        if pair is None:
            continue
        expected = EXPECTED_TARGETS[pair]
        require(
            pair not in tasks
            and source["pair_index"] == pair
            and source["row_sha256"] == expected["c40_row_sha256"]
            and source["c40_leaf_id"] == expected["c40_leaf_id"]
            and source["path"] == c41_rows[pair]["source_path"],
            "exact C40 task source:" + str(pair),
        )
        tasks[pair] = c41.task_for_row(ordinal, source, context)
    require(set(tasks) == set(TARGET_PAIRS), "five exact C40 tasks")
    return tasks


def pilot(max_depth: int, max_routes_per_pair: int) -> dict[str, Any]:
    require(0 <= max_depth <= 12, "pilot max depth range")
    require(1 <= max_routes_per_pair <= 8191,
            "pilot max routes per pair range")
    guards: dict[str, Capture] = {}
    watched_directories = (
        RUNTIME, RUNTIME / "candidates", AUDIT_ROOT,
        C41_DIR, C42_DIR, AUDIT_ROOT / C42_RELEASE,
    )
    directory_before = {
        str(path.relative_to(ROOT)): directory_fingerprint(path)
        for path in watched_directories
    }
    try:
        guards["self"] = Capture(SELF, None, "C43B0 source", 4 << 20)
        for label, (path, sha) in PINNED_FILES.items():
            guards[label] = Capture(ROOT / path, sha, label)

        installed_audit = c42tx.audit_installed(
            EXPECTED_C42_TRANSACTION_AUDITOR_SHA256
        )
        require(
            installed_audit["authority_installed"] is True
            and installed_audit["authority_seal_object_sha256"]
            == EXPECTED_C42_SEAL_OBJECT
            and installed_audit["installation_receipt_object_sha256"]
            == EXPECTED_C42_RECEIPT_OBJECT
            and installed_audit["candidate_object_sha256"] == EXPECTED_C42_OBJECT
            and installed_audit["independent_audit_object_sha256"]
            == EXPECTED_C42_AUDIT_OBJECT,
            "installed C42 authority audit",
        )

        c41_result = c41.strict_json(C41_DIR / "result.json")
        c41.validate_manifest(C41_DIR)
        c41.validate_object(c41_result, EXPECTED_C41_OBJECT, "C41")
        c42_result = c41.strict_json(C42_DIR / "result.json")
        c41.validate_manifest(C42_DIR)
        c41.validate_object(c42_result, EXPECTED_C42_OBJECT, "C42")
        require(
            file_sha256(Path(c41.__file__).resolve())
            == EXPECTED_C41_SOURCE_SHA256,
            "C41 route source SHA256",
        )

        c41_rows, _c42_parent_rows = validate_target_rows(
            c41_result, c42_result
        )
        c40_dir = (ROOT / c41_result["C40_authority"]["path"]).resolve()
        c40_audit = (
            ROOT / c41_result["C40_authority"]["independent_audit_path"]
        ).resolve()
        context = c41.load_context(c40_dir, c40_audit, formal=True)
        context["_C43B0_C40_directory"] = c40_dir
        tasks = load_c40_tasks(context, c41_rows)

        c41.ctx.prec = c41.PRECISION_BITS
        generated = c41.install_complete_immutable_cache()
        config = c41.decode_worker_config(context["config"])
        require(
            sum(len(rows) for rows in generated.values()) == 448,
            "complete immutable candidate cache",
        )

        pair_reports: list[dict[str, Any]] = []
        for pair in TARGET_PAIRS:
            task = tasks[pair]
            start_row = c41_rows[pair]
            start_path = start_row["path"]
            initial_route = c41.route_at_path(task, start_path, config)
            require(
                initial_route["classification"] == start_row["raw_classification"]
                and c41.box_payload(initial_route["box"])
                == start_row["closed_representative_box"],
                "C41 starting route replay:" + str(pair),
            )

            def children(path: str, route: dict[str, Any], *,
                         current_task: dict[str, Any] = task) \
                    -> tuple[list[tuple[str, dict[str, Any]]], str]:
                box = route["box"]
                require(box is not None, "adaptive rational parent box")
                axis = c41.c38.round166.longest_axis(box)
                require(axis in {0, 1}, "s=0 adaptive split uses t or p")
                exact_children = c41.c38.round166.split_axis(box, axis)
                routed: list[tuple[str, dict[str, Any]]] = []
                for bit in ("0", "1"):
                    child_path = path + bit
                    child_route = c41.route_at_path(
                        current_task, child_path, config
                    )
                    require(
                        c41.box_payload(child_route["box"])
                        == c41.box_payload(exact_children[int(bit)]),
                        "adaptive exact child reconstruction",
                    )
                    routed.append((child_path, child_route))
                return routed, ("t", "p", "s")[axis]

            traversal = adaptive_traverse(
                start_path, initial_route, max_depth,
                max_routes_per_pair, children,
            )
            pair_reports.append(summarize_traversal(pair, start_row, traversal))

        aggregate_exit_families: Counter[str] = Counter()
        aggregate_checkpoint_classifications: Counter[str] = Counter()
        for report in pair_reports:
            aggregate_exit_families.update(report["D02_A_exit_family_census"])
            aggregate_checkpoint_classifications.update(
                report["checkpoint_classification_census"]
            )
        semantic = {
            "schema": SCHEMA,
            "status": "PASS_READ_ONLY_C43B0_ADAPTIVE_PILOT__ZERO_CREDIT",
            "source_sha256": guards["self"].sha256,
            "authority_input": {
                "C42_authority_installed": True,
                "C42_candidate_object_sha256": EXPECTED_C42_OBJECT,
                "C42_independent_audit_object_sha256": EXPECTED_C42_AUDIT_OBJECT,
                "C42_installation_receipt_object_sha256":
                    EXPECTED_C42_RECEIPT_OBJECT,
                "C42_authority_seal_object_sha256": EXPECTED_C42_SEAL_OBJECT,
                "C41_candidate_object_sha256": EXPECTED_C41_OBJECT,
                "C41_route_source_sha256": EXPECTED_C41_SOURCE_SHA256,
            },
            "budget": {
                "maximum_additional_depth": max_depth,
                "maximum_route_evaluations_per_pair": max_routes_per_pair,
                "target_pair_count": len(TARGET_PAIRS),
            },
            "pair_reports": pair_reports,
            "aggregate": {
                "route_evaluation_count": sum(
                    row["route_evaluation_count"] for row in pair_reports
                ),
                "split_count": sum(row["split_count"] for row in pair_reports),
                "leaf_count": sum(row["leaf_count"] for row in pair_reports),
                "D02_A_exit_leaf_count": sum(
                    row["D02_A_exit_leaf_count"] for row in pair_reports
                ),
                "D02_A_exit_family_census": dict(
                    sorted(aggregate_exit_families.items())
                ),
                "checkpoint_leaf_count": sum(
                    row["checkpoint_leaf_count"] for row in pair_reports
                ),
                "checkpoint_classification_census": dict(
                    sorted(aggregate_checkpoint_classifications.items())
                ),
                "formal_credit_issued": False,
                "ambient_credit_issued": 0,
                "D02_gate_credit_issued": 0,
            },
            "nonpromotion": {
                "runtime_writes_performed": False,
                "candidate_created": False,
                "authority_minted": False,
                "pilot_stdout_is_authority": False,
                "D02": "BLOCKED",
                "CM2": "NO-GO_FOR_CLAIM",
            },
        }
        semantic["pilot_report_object_sha256"] = digest(semantic)
        for guard in guards.values():
            guard.unchanged("terminal pilot")
        directory_after = {
            str(path.relative_to(ROOT)): directory_fingerprint(path)
            for path in watched_directories
        }
        require(directory_after == directory_before,
                "runtime directory tree unchanged by pilot")
        return semantic
    finally:
        for guard in reversed(list(guards.values())):
            guard.close()


def self_test() -> dict[str, Any]:
    require(
        file_sha256(Path(c41.__file__).resolve()) == EXPECTED_C41_SOURCE_SHA256
        and file_sha256(Path(c42tx.__file__).resolve())
        == EXPECTED_C42_TRANSACTION_AUDITOR_SHA256,
        "self-test source pins",
    )

    def fake_route(path: str) -> dict[str, Any]:
        table = {
            "x": "UNRESOLVED_FAKE_OUTER",
            "x0": "EXCLUDED_FAKE_STRICT",
            "x1": "UNRESOLVED_FAKE_OUTER",
            "x10": "UNRESOLVED_FAKE_NEEDS_COLLISION3_1648",
            "x11": "UNRESOLVED_FAKE_OUTER",
        }
        return {"classification": table[path], "box": path}

    def fake_children(path: str, _route: dict[str, Any]) \
            -> tuple[list[tuple[str, dict[str, Any]]], str]:
        return [
            (path + "0", fake_route(path + "0")),
            (path + "1", fake_route(path + "1")),
        ], "t"

    traversal = adaptive_traverse(
        "x", fake_route("x"), max_depth=2, max_routes=7,
        child_builder=fake_children,
    )
    leaves = traversal["leaves"]
    require(
        traversal["route_evaluation_count"] == 5
        and traversal["relative_kraft_sum"] == "1"
        and [row["family"] for row in leaves]
        == ["TERMINAL_EXCLUDED", "COLLISION3_READY", "RESIDUAL_OUTER"]
        and leaves[-1]["stop"] == "CHECKPOINT_MAX_DEPTH",
        "adaptive traversal hostile fixture",
    )
    budget = adaptive_traverse(
        "x", fake_route("x"), max_depth=2, max_routes=1,
        child_builder=fake_children,
    )
    require(
        budget["route_evaluation_count"] == 1
        and budget["leaves"][0]["stop"] == "CHECKPOINT_ROUTE_BUDGET",
        "route budget fail-closed checkpoint",
    )
    return {
        "schema": SCHEMA + ".self-test",
        "status": "PASS_C43B0_READ_ONLY_ADAPTIVE_TRAVERSAL_SELF_TEST",
        "target_pairs": list(TARGET_PAIRS),
        "fixture_leaf_count": len(leaves),
        "fixture_relative_Kraft_sum": traversal["relative_kraft_sum"],
        "runtime_writes_performed": False,
        "candidate_created": False,
        "authority_minted": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--pilot", action="store_true")
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--max-routes-per-pair", type=int, default=127)
    arguments = parser.parse_args()
    if arguments.self_test:
        require(
            arguments.max_depth == 6 and arguments.max_routes_per_pair == 127,
            "self-test takes no pilot budget overrides",
        )
        value = self_test()
    else:
        value = pilot(arguments.max_depth, arguments.max_routes_per_pair)
    sys.stdout.buffer.write(canonical(value) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
