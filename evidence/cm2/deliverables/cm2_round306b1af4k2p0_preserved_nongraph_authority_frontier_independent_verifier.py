#!/usr/bin/env python3
"""Independent cold verifier for the K2P0 authority-frontier ledger.

The verifier does not import or execute the producer.  It pins the producer,
the frozen ledger, and every ledger-declared upstream artifact; independently
recomputes all selected table/path/order commitments; and preserves zero
formal credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterable, Final


class VerifyBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerifyBlocked(label)


def typed_equal(left: Any, right: Any) -> bool:
    """Recursive equality that never aliases bool with int."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(
            typed_equal(left[key], right[key]) for key in left
        )
    if isinstance(left, (list, tuple)):
        return len(left) == len(right) and all(
            typed_equal(a, b) for a, b in zip(left, right)
        )
    return bool(left == right)


SCHEMA: Final = "cm2.round306b1af4k2p0.preserved-nongraph-authority-frontier.independent-verification.v1"
LEDGER_SCHEMA: Final = "cm2.round306b1af4k2p0.preserved-nongraph-authority-frontier.v1"
HERE: Final = Path(__file__).parent
PRODUCER_FILE: Final = "cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_producer.py"
PRODUCER_SIZE: Final = 34_110
PRODUCER_SHA256: Final = "c4625c23b3e752951015682139898b83f1761a9784fa89cb168437993abcbafd"
LEDGER_FILE: Final = "cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_ledger.json"
LEDGER_SIZE: Final = 35_521
LEDGER_SHA256: Final = "e56a50b1ce88f0ae45eb09a194a15d3c26804c6e5baac803a1f5f4a19231ed3d"
ROW_CAP: Final = 8_388_608
EXPECTED_CERT_SCHEMAS: Final = {
    "R230_CERT": "cm2.round230.source-g-resolved-retained-bulk-continuation.v1",
    "R231_CERT": "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1",
    "R233_CERT": "cm2.round233.source-g-outgoing-seam-parametric-graph-key-partition.v1",
    "R235_CERT": "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1",
    "R147_CERT": "cm2.round147.gate5-strict-reaudit-upgrade-frontier.v1",
}
MANIFESTS: Final = {
    "R230_MANIFEST": ("R230_SOURCE", "R230_CERT", "R230_VERIFIER", "R230_VERIFICATION"),
    "R233_MANIFEST": ("R233_SOURCE", "R233_CERT", "R233_VERIFIER", "R233_VERIFICATION"),
    "R235_MANIFEST": ("R235_SOURCE", "R235_CERT", "R235_VERIFIER", "R235_VERIFICATION"),
    "R147_MANIFEST": ("R147_SOURCE", "R147_CERT", "R147_VERIFIER", "R147_VERIFICATION", "R147_REPORT", "R147_COLD", "R147_ATTACK"),
}

# Independent exact allowlists.  These are deliberately duplicated rather
# than imported from the producer or accepted from the ledger.
EXPECTED_PINS: Final = (
    ("P1", "ANCHOR", "cm2_round306b1af4p1_source_g_preserved_non_graph_exact_join_preflight.py", 112_834, "34098cfd5c5e8d1ff73b4a172ecd0a1375a74a4e51a12c6e89b7984474062dfd", "B06_FRONTIER_ANCHOR"),
    ("R209_SOURCE", "R209", "cm2_round209_source_g_outgoing_half_open_owner_probe.py", 46_556, "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f", "NONFORMAL_PROBE_SOURCE"),
    ("R209_REPORT", "R209", "cm2_round209_source_g_outgoing_half_open_owner_spike_report.md", 8_718, "7501e73fdad0c3721ed70b73226a4c3a4f7288f9b8429a553a50dde725812524", "NONFORMAL_PROBE_REPORT"),
    ("R230_SOURCE", "R230", "cm2_round230_source_g_resolved_retained_bulk_continuation.py", 63_598, "6b9bac3fd7da301bffb73b0545cc16505df84f69c4f496075cbb146157377cbb", "PRODUCER_SOURCE"),
    ("R230_CERT", "R230", "cm2_round230_source_g_resolved_retained_bulk_continuation_certificate.json", 67_327_799, "88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73", "ROW_CERTIFICATE"),
    ("R230_VERIFIER", "R230", "cm2_round230_source_g_resolved_retained_bulk_continuation_verifier.py", 54_481, "e2fdd802ab5d2ccb0d99483da4aed5cff96004c4c6c04518ac9a80cbafe79d72", "INDEPENDENT_VERIFIER"),
    ("R230_VERIFICATION", "R230", "cm2_round230_source_g_resolved_retained_bulk_continuation_verification.json", 763, "a48df50b6ffd38f096dbbeece6e6f1707a69ce08313ae302c993aac5d34fca0c", "VERIFICATION_RECEIPT"),
    ("R230_REPORT", "R230", "cm2_round230_source_g_resolved_retained_bulk_continuation_report.md", 3_051, "f18571ff53c9c8a057db7078bf6ba99a364a93b19062b4b6bf6fa2622b95da8f", "REPORT"),
    ("R230_COLD", "R230", "cm2_round230_source_g_resolved_retained_bulk_continuation_cold_replay.md", 823, "b6df942715e2df93d032528a8310af28a4823a0fef790d7d6b80f41b5811e56f", "COLD_REPLAY_RECEIPT"),
    ("R230_MANIFEST", "R230", "cm2_round230_source_g_resolved_retained_bulk_continuation_manifest.sha256", 546, "54a6a7f91aa9f7bd2caebd5778e8522fa072d5621da2b4015f425fb7f9d67229", "MANIFEST"),
    ("R231_SOURCE", "R231", "cm2_round231_source_g_outgoing_seam_depth6_materialization.py", 12_984, "5afa1bc6fc6faec4c9b13be707c93714acdf5dbd09f2fafeefff07c445c517ad", "PRODUCER_SOURCE"),
    ("R231_CERT", "R231", "cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json", 91_909_341, "7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374", "ROW_CERTIFICATE_WITHOUT_RECEIPT_PACKAGE"),
    ("R233_SOURCE", "R233", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition.py", 13_285, "820085392577265eabcbdfea19f095e942736c0fe938554b811b04f1bd1f3546", "PRODUCER_SOURCE"),
    ("R233_CERT", "R233", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json", 6_808_749, "cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41", "ROW_CERTIFICATE"),
    ("R233_VERIFIER", "R233", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_verifier.py", 14_492, "6c2eb0729a90866c4d98743462f5e379764c7ce8bbfe330680b18d49965b516d", "INDEPENDENT_VERIFIER"),
    ("R233_VERIFICATION", "R233", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_verification.json", 871, "184121d738cfcac44f06e65d14cf8581bc82c215ecf6f6bfb1ac2f2baf97bc63", "VERIFICATION_RECEIPT"),
    ("R233_MANIFEST", "R233", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_manifest.sha256", 582, "6e5d8babad93fbfad5a6656891f8600a3cc831c0f1d02085f8abe1c46a978459", "MANIFEST"),
    ("R235_SOURCE", "R235_PRESERVED_NONGRAPH", "cm2_round235_source_g_single_endpoint_graph_word_key_partition.py", 13_043, "8e5f807dfc43632d59cc9c994fd58907080a52bedc7789f8bb507b002ce8641a", "PRODUCER_SOURCE"),
    ("R235_CERT", "R235_PRESERVED_NONGRAPH", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787", "SINGLE_ENDPOINT_GRAPH_WORD_ROW_CERTIFICATE_NOT_G2"),
    ("R235_VERIFIER", "R235_PRESERVED_NONGRAPH", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_verifier.py", 10_882, "4ce8c9d516dd95f27bea0f951ea2644705af9b50b63362004e3d3e5d7221dc4d", "INDEPENDENT_VERIFIER"),
    ("R235_VERIFICATION", "R235_PRESERVED_NONGRAPH", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_verification.json", 643, "8009f857b45aa05848b84258f2081bd6de54ff04643387ea3e8fd9c74bdb0e2a", "VERIFICATION_RECEIPT"),
    ("R235_MANIFEST", "R235_PRESERVED_NONGRAPH", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_manifest.sha256", 566, "cf58b7d2f419ea252c3398665302fe6f5ff06436af20a56beaaa47e5ef822ea0", "MANIFEST"),
    ("R147_SOURCE", "GATE5_R147", "cm2_round147_gate5_strict_reaudit_upgrade_frontier.py", 30_689, "0f66021bb4691e8c9b9765f3025df4b052cb9323db1a8fa94e9d0ea5b3f63619", "LATEST_STRICT_FRONTIER_PRODUCER"),
    ("R147_CERT", "GATE5_R147", "cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json", 25_025, "db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee", "LATEST_STRICT_FRONTIER_RECEIPT_NOT_AUTOMATIC_THEOREM_AUTHORITY"),
    ("R147_VERIFIER", "GATE5_R147", "cm2_round147_gate5_strict_reaudit_upgrade_frontier_verifier.py", 23_265, "250e6e9335d638a8b37346b06c03c292c1c46e94a95255c27d24ad21314e5a7c", "INDEPENDENT_VERIFIER"),
    ("R147_VERIFICATION", "GATE5_R147", "cm2-round147-gate5-strict-reaudit-upgrade-frontier-verification-2026-07-24.json", 2_256, "8302642619f66a4a47ec79d8fefb0230378331b578a363f12ad1b64dffebbd3d", "VERIFICATION_RECEIPT"),
    ("R147_REPORT", "GATE5_R147", "cm2-round147-gate5-strict-reaudit-upgrade-frontier-report-2026-07-24.md", 4_192, "f12dde7dd10e6f86327bdd24b1c6462e839bb15a2daff509b44ab561a30c8441", "REPORT"),
    ("R147_COLD", "GATE5_R147", "cm2-round147-gate5-strict-reaudit-upgrade-frontier-cold-replay-2026-07-24.md", 775, "a2aae06ae6057ad7311b168f481366da6071db77e77a0ef8d8cbdd2e5baa7baf", "COLD_REPLAY_RECEIPT"),
    ("R147_ATTACK", "GATE5_R147", "cm2-round147-gate5-strict-reaudit-upgrade-frontier-direct-assault-2026-07-24.md", 1_008, "a413ca7f1f34950680835331a17180019c395e5b875bd5d0edbc55e236cb3ea8", "DIRECT_ASSAULT_RECEIPT"),
    ("R147_MANIFEST", "GATE5_R147", "cm2-round147-gate5-strict-reaudit-upgrade-frontier-manifest-2026-07-24.sha256", 955, "a961a4c53814272056f4b317cf8467e6965d798362be8efc2e9393314b994ac4", "MANIFEST"),
)

EXPECTED_TABLES: Final = (
    ("R230_ABSENCE", "R230_CERT", ("result", "formal_resolved_child_event_zero_set_absence_ledger", "rows"), 8_976, "9e5451b5f808ff80b1bc25dcad1746a78cb8fa7ae3f77483a0fc3e47f2345626", ("result", "formal_resolved_child_event_zero_set_absence_ledger", "rows_sha256")),
    ("R230_FACE_CANDIDATE", "R230_CERT", ("result", "formal_exact_face_candidate_ledger", "rows"), 1_512, "421dd9039658c7e8bcb17f434b9d80515e65188083a8905f11c249814bbc18ad", ("result", "formal_exact_face_candidate_ledger", "rows_sha256")),
    ("R230_EDGE", "R230_CERT", ("result", "formal_certified_local_bulk_continuation_edge_ledger", "rows"), 784, "7a63ba5416a34ad1fcf5084dc0a5ee4b135816358c7a02b69e258bd9f924f6e3", ("result", "formal_certified_local_bulk_continuation_edge_ledger", "rows_sha256")),
    ("R230_REJECT", "R230_CERT", ("result", "formal_rejected_local_bulk_candidate_ledger", "rows"), 740, "a1ca4f398d1202da6a504ffc977eac25cd68867b280f83eea76651dd257bd773", ("result", "formal_rejected_local_bulk_candidate_ledger", "rows_sha256")),
    ("R230_STAR", "R230_CERT", ("result", "formal_certified_local_bulk_bridge_star_ledger", "rows"), 448, "2d3348cac30d52bf97a1fb62c342bbf317bf388d09b256f186485f11c3cf3152", ("result", "formal_certified_local_bulk_bridge_star_ledger", "rows_sha256")),
    ("R230_INCIDENCE_DELTA", "R230_CERT", ("result", "formal_occurrence_known_block_incidence_delta_ledger", "rows"), 464, "e0663279b21bdd6e983907ef228bfe5ef88a606cb881de981f1d3b9d732869c0", ("result", "formal_occurrence_known_block_incidence_delta_ledger", "rows_sha256")),
    ("R230_POST_OCCURRENCE", "R230_CERT", ("result", "formal_post_Round230_occurrence_known_block_frontier_ledger", "rows"), 53_968, "dcceb9f3ce4f210e3d16ea262b87678d061defd7e333fb4a963483feba0bca95", ("result", "formal_post_Round230_occurrence_known_block_frontier_ledger", "rows_sha256")),
    ("R230_POST_KEY", "R230_CERT", ("result", "formal_post_Round230_key_frontier_ledger", "rows"), 116, "345678761e03efb721acc9d5e7ac3405371c4de383d671a7dfd8c6b3cbaf4be9", ("result", "formal_post_Round230_key_frontier_ledger", "rows_sha256")),
    ("R231_RESOLVED", "R231_CERT", ("result", "resolved_descendant_rows"), 22_348, "dcc8cdfb71e566a18cd512be31964b0e395b844443440e78924f479fc67cb0b5", ("result", "resolved_descendant_rows_sha256")),
    ("R231_GUARD", "R231_CERT", ("result", "guard_descendant_rows"), 0, "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945", ("result", "guard_descendant_rows_sha256")),
    ("R231_FRONTIER", "R231_CERT", ("result", "depth6_frontier_rows"), 67_924, "17fc58fcd194ed00ba2509e4fec1173b3bfdc1c5ae4586f24ecf8e7dd95d5fd3", ("result", "depth6_frontier_rows_sha256")),
    ("R231_ROOT", "R231_CERT", ("result", "root_summary_rows"), 5_368, "2a67e24ed3dbedaa6a1615245cf7075dd7ecde4929bdcf3b36e92376e3f42d03", ("result", "root_summary_rows_sha256")),
    ("R233_PARTITION", "R233_CERT", ("result", "parametric_graph_key_partition_rows"), 3_148, "9b44e5120168e008bea5d0e621511d9e375f0422b97292817b6bb8bd35443356", ("result", "parametric_graph_key_partition_rows_sha256")),
    ("R235_SINGLE", "R235_CERT", ("result", "single_endpoint_graph_partition_rows"), 38_328, "e9a3794540170bf013160fb713acfbb1a65d42afedfb7b972cbfdad290549731", ("result", "single_endpoint_graph_partition_rows_sha256")),
    ("R235_DOUBLE_DEFERRED", "R235_CERT", ("result", "double_endpoint_deferred_rows"), 16, "52e01cc83edcd02f9746701201508e0851fe8df6d44cee77c1aa23301d964572", ("result", "double_endpoint_deferred_rows_sha256")),
    ("R147_GATE5_FIELDS", "R147_CERT", ("result", "gate5_field_rows"), 18, "36de71e5bf06200fa689ad8cb3b26e2d1589f868a38cd2c8dd83df7b232edcc6", ("result", "gate5_field_rows_sha256")),
    ("R147_EXECUTABLE_FRONTIER", "R147_CERT", ("result", "executable_upgrade_frontier"), 4, "6cdf91412fde699ea2bb9ed1b939de70ecee361875c8b526b943209ad0cf6d18", None),
)


def canonical_bytes(value: Any, *, ascii_only: bool = True) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=ascii_only, allow_nan=False).encode("ascii" if ascii_only else "utf-8")


def sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate key:" + key)
        out[key] = value
    return out


def reject_float(token: str) -> Any:
    raise VerifyBlocked("nonintegral JSON number:" + token)


def reject_constant(token: str) -> Any:
    raise VerifyBlocked("nonstandard JSON constant:" + token)


def decode(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=duplicate_reject,
                           parse_float=reject_float, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerifyBlocked("decode:" + label) from exc
    need(isinstance(value, dict), "root object:" + label)
    return value


def file_identity(st: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns)


def dir_identity(st: os.stat_result) -> tuple[int, int, int]:
    return (st.st_dev, st.st_ino, st.st_mode)


class HeldSet:
    def __init__(self) -> None:
        self.dir_fd = -1
        self.dir_before: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.pins: dict[str, dict[str, Any]] = {}
        self.initial_hashes: dict[str, tuple[str, str]] = {}
        self.final_hashes: dict[str, str] = {}

    def __enter__(self) -> "HeldSet":
        root = os.fspath(HERE)
        before = os.stat(root, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "deliverables directory")
        self.dir_fd = os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        held = os.fstat(self.dir_fd)
        need(dir_identity(before) == dir_identity(held), "directory open race")
        self.dir_before = held
        return self

    def add(self, label: str, filename: str, size: int, expected: str) -> None:
        need(label not in self.fds, "duplicate pin label")
        need(filename == os.path.basename(filename) and filename not in {".", ".."}, "pin basename")
        before = os.stat(filename, dir_fd=self.dir_fd, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular/nlink:" + label)
        need(before.st_size == size, "size:" + label)
        fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dir_fd)
        opened = os.fstat(fd)
        need(file_identity(before) == file_identity(opened), "open race:" + label)
        self.fds[label] = fd
        self.pins[label] = {"filename": filename, "exact_size": size, "sha256": expected}
        h1, h2 = self._hash(fd), self._hash(fd)
        need(h1 == expected and h2 == expected, "two-pass SHA:" + label)
        after = os.stat(filename, dir_fd=self.dir_fd, follow_symlinks=False)
        need(file_identity(opened) == file_identity(after), "post-hash path:" + label)
        self.initial_hashes[label] = (h1, h2)

    @staticmethod
    def _hash(fd: int) -> str:
        os.lseek(fd, 0, os.SEEK_SET)
        state = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                break
            state.update(chunk)
        return state.hexdigest()

    def bytes(self, label: str) -> bytes:
        fd = self.fds[label]
        os.lseek(fd, 0, os.SEEK_SET)
        out: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                break
            out.append(chunk)
        return b"".join(out)

    def final(self) -> None:
        for label, pin in self.pins.items():
            digest_text = self._hash(self.fds[label])
            need(digest_text == pin["sha256"], "final SHA:" + label)
            self.final_hashes[label] = digest_text
            held = os.fstat(self.fds[label])
            path = os.stat(pin["filename"], dir_fd=self.dir_fd, follow_symlinks=False)
            need(file_identity(held) == file_identity(path), "final path/FD:" + label)
            need(stat.S_ISREG(held.st_mode) and held.st_nlink == 1, "final regular/nlink:" + label)
        need(self.dir_before is not None, "directory state")
        need(dir_identity(self.dir_before) == dir_identity(os.fstat(self.dir_fd)) == dir_identity(os.stat(os.fspath(HERE), follow_symlinks=False)), "final directory path")

    def __exit__(self, *_args: object) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        if self.dir_fd >= 0:
            try:
                os.close(self.dir_fd)
            except OSError:
                pass


def get_path(root: Any, path: Iterable[str], label: str) -> Any:
    node = root
    for key in path:
        need(isinstance(node, dict) and key in node, "exact path:" + label + ":" + key)
        node = node[key]
    return node


def streaming_digest(value: Any, *, cap: int | None = None) -> str:
    encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    state = hashlib.sha256()
    total = 0
    for chunk in encoder.iterencode(value):
        raw = chunk.encode("utf-8")
        total += len(raw)
        if cap is not None:
            need(total <= cap, "canonical selected row cap")
        state.update(raw)
    return state.hexdigest()


def table_commitment(rows: list[Any]) -> dict[str, Any]:
    hashes: list[str] = []
    closed = 0
    for row in rows:
        need(isinstance(row, dict), "row object")
        hashes.append(streaming_digest(row, cap=ROW_CAP))
        if "row_sha256" in row:
            expected = row["row_sha256"]
            need(isinstance(expected, str) and len(expected) == 64, "row SHA format")
            body = dict(row)
            del body["row_sha256"]
            need(streaming_digest(body, cap=ROW_CAP) == expected, "row SHA closure")
            closed += 1
    return {
        "row_count": len(rows),
        "ordered_rows_sha256": streaming_digest(rows),
        "ordered_row_digest_sequence_sha256": sha(hashes),
        "unordered_row_digest_multiset_sha256": sha(sorted(hashes)),
        "first_row_sha256": hashes[0] if hashes else None,
        "last_row_sha256": hashes[-1] if hashes else None,
        "upstream_row_sha256_closed_count": closed,
        "upstream_row_sha256_missing_count": len(rows) - closed,
    }


def validate_manifest(raw: bytes, labels: tuple[str, ...], pins: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64, "manifest syntax")
        rows.append({"filename": parts[1], "sha256": parts[0]})
    expected = [{"filename": pins[label]["filename"], "sha256": pins[label]["sha256"]} for label in labels]
    need(typed_equal(rows, expected), "manifest exact ordered membership")
    return {"entry_count": len(rows), "ordered_entries_sha256": sha(rows), "exact_membership": True}


def verify() -> dict[str, Any]:
    need(LEDGER_SIZE > 0 and len(LEDGER_SHA256) == 64, "verifier ledger pin frozen")
    with HeldSet() as held:
        held.add("K2P0_PRODUCER", PRODUCER_FILE, PRODUCER_SIZE, PRODUCER_SHA256)
        held.add("K2P0_LEDGER", LEDGER_FILE, LEDGER_SIZE, LEDGER_SHA256)
        envelope = decode(held.bytes("K2P0_LEDGER"), "ledger")
        need(envelope.get("schema") == LEDGER_SCHEMA + ".envelope", "ledger envelope schema")
        ledger = envelope.get("ledger")
        need(isinstance(ledger, dict) and envelope.get("ledger_sha256") == sha(ledger), "ledger internal digest")
        need(ledger.get("schema") == LEDGER_SCHEMA, "ledger schema")
        need(ledger.get("status") == "PASS_DIRECT_SOURCE_DISCOVERY_AND_ORDER_COMMITMENTS__ZERO_NORMALIZED_SUPPORT_THEOREM_B1A_OR_CM2_CREDIT", "ledger status")
        need(ledger.get("artifact_kind") == "ZERO_CREDIT_DIRECT_SOURCE_AUTHORITY_FRONTIER", "artifact kind")
        need(ledger.get("authority_priority") == [
            "DIRECT_CERTIFICATE_ROW_WITH_EXACT_PATH_AND_ORDER_COMMITMENT",
            "SOURCE_CODE_REPLAY_PLUS_INDEPENDENT_VERIFICATION_RECEIPT",
            "SEALED_FRONTIER_RECEIPT", "REPORT_OR_MANIFEST",
            "NONFORMAL_PROBE_SUMMARY",
        ], "authority priority")
        need(ledger.get("priority_nonpromotion") == "no priority tier is a semantic/full-support theorem without a separate input-bound semantic checker and source-exhaustion proof", "priority nonpromotion")
        need(typed_equal(ledger.get("scope"), {
            "included": ["PRESERVED", "NON_GRAPH_BULK", "P1_B06_DIRECT_EVIDENCE_FRONTIER"],
            "excluded": ["R2", "R292", "G2A", "G2B", "NORMALIZED_SUPPORT_CONSTRUCTION", "B1A", "B2"],
            "formal_credit": 0, "normalized_full_support_credit": 0,
            "representation_cover_credit": 0, "B1A_credit": 0,
            "CM2_credit": 0,
        }), "exact zero-credit scope")
        need(typed_equal(ledger.get("input_security"), {
            "O_NOFOLLOW": True,
            "availability_limitation": "whole pinned certificate documents and selected row arrays are decoded in memory; exact input sizes are pinned, but no runtime/RSS bound is claimed",
            "bounded_memory_claim": False,
            "canonical_selected_row_cap_bytes": ROW_CAP,
            "directory_path_identity_final": True,
            "final_full_sha256_pass_after_all_parsing": True,
            "held_directory_descriptor": True,
            "nlink_must_equal_one": True,
            "path_fd_identity_before_after_and_final": True,
            "pin_count": 30,
            "regular_file_required": True,
            "symlink_hardlink_TOCTOU": "FAIL_CLOSED",
            "temporary_files_or_spill": False,
            "total_pinned_bytes": 234_258_243,
            "two_full_sha256_passes_per_held_fd": True,
            "upstream_python_imported_or_executed": False,
            "whole_certificate_JSON_loaded_in_memory": True,
        }), "exact input-security/nonclaim contract")
        pins = ledger.get("exact_pins")
        need(isinstance(pins, list) and len(pins) == 30, "upstream pin count")
        actual_pin_allowlist = tuple(
            (pin.get("label"), pin.get("source_family"), pin.get("filename"),
             pin.get("exact_size"), pin.get("sha256"), pin.get("role"))
            for pin in pins if isinstance(pin, dict)
        )
        need(typed_equal(actual_pin_allowlist, EXPECTED_PINS), "exact independent pin allowlist")
        pin_map: dict[str, dict[str, Any]] = {}
        for pin in pins:
            need(isinstance(pin, dict), "pin row")
            label = pin.get("label")
            need(isinstance(label, str) and label not in pin_map, "pin label")
            need(pin.get("two_pass_held_fd_sha256") == [pin.get("sha256"), pin.get("sha256")], "producer two-pass receipt")
            need(pin.get("final_post_parse_held_fd_sha256") == pin.get("sha256"), "producer final SHA receipt")
            pin_map[label] = pin
            held.add(label, pin["filename"], pin["exact_size"], pin["sha256"])
        docs: dict[str, dict[str, Any]] = {}
        replayed_tables: list[dict[str, Any]] = []
        selected = ledger.get("selected_tables")
        need(isinstance(selected, list) and len(selected) == 17, "selected table count")
        actual_table_allowlist = tuple(
            (row.get("table_label"), row.get("certificate_label"),
             tuple(row.get("exact_result_property_path", [])), row.get("row_count"),
             row.get("ordered_rows_sha256"),
             tuple(row["declared_digest_property_path"])
             if row.get("declared_digest_property_path") is not None else None)
            for row in selected if isinstance(row, dict)
        )
        need(typed_equal(actual_table_allowlist, EXPECTED_TABLES), "exact independent table/path/order allowlist")
        for expected in selected:
            need(isinstance(expected, dict), "selected table row")
            cert_label = expected.get("certificate_label")
            need(cert_label in EXPECTED_CERT_SCHEMAS, "certificate allowlist")
            if cert_label not in docs:
                docs[cert_label] = decode(held.bytes(cert_label), cert_label)
            doc = docs[cert_label]
            need(doc.get("schema") == EXPECTED_CERT_SCHEMAS[cert_label], "certificate schema")
            result = doc.get("result")
            need(isinstance(result, dict) and doc.get("result_sha256") == streaming_digest(result), "certificate result digest")
            exact_path = expected.get("exact_result_property_path")
            need(isinstance(exact_path, list) and exact_path[:1] == ["result"], "selected exact path")
            rows = get_path(doc, exact_path, expected["table_label"])
            need(isinstance(rows, list), "selected table array")
            commitment = table_commitment(rows)
            for key, value in commitment.items():
                need(typed_equal(expected.get(key), value), "commitment mismatch:" + expected["table_label"] + ":" + key)
            declared = expected.get("declared_digest_property_path")
            if declared is not None:
                need(isinstance(declared, list) and declared[:1] == ["result"], "declared path")
                need(get_path(doc, declared, expected["table_label"]) == commitment["ordered_rows_sha256"], "declared digest mismatch")
            replayed_tables.append({"table_label": expected["table_label"], **commitment})
        manifests = {
            label: validate_manifest(held.bytes(label), members, pin_map)
            for label, members in MANIFESTS.items()
        }
        need(typed_equal(manifests, ledger.get("manifest_replay")), "manifest replay receipt")
        summary = ledger.get("selected_table_summary")
        need(typed_equal(summary, {
            "table_count": 17, "row_count": 204_162,
            "upstream_row_sha256_closed_count": 67_026,
            "upstream_row_sha256_missing_count": 137_136,
            "table_commitments_sha256": "75f21679adb6e9cbf20b87ed74872d35e199916104fa0cbcc66af3ba6f0e8938",
        }), "exact table summary")
        need(type(summary.get("row_count")) is int and sum(row["row_count"] for row in replayed_tables) == summary.get("row_count") == 204_162, "row census")
        need(type(summary.get("upstream_row_sha256_closed_count")) is int and sum(row["upstream_row_sha256_closed_count"] for row in replayed_tables) == summary.get("upstream_row_sha256_closed_count") == 67_026, "closed row census")
        need(type(summary.get("upstream_row_sha256_missing_count")) is int and sum(row["upstream_row_sha256_missing_count"] for row in replayed_tables) == summary.get("upstream_row_sha256_missing_count") == 137_136, "missing row SHA census")
        statuses = ledger.get("source_authority_status")
        need(isinstance(statuses, list) and len(statuses) == 6, "source status count")
        need(all(row.get("authority_status") == "BLOCKED_MISSING_AUTHORITY" for row in statuses), "all semantic authority blocked")
        status_core = tuple(
            (row.get("source_family"), row.get("row_materialization_status"),
             row.get("authority_status"), row.get("receipt_package_status"),
             row.get("selected_table_commitment_count"))
            for row in statuses
        )
        need(typed_equal(status_core, (
            ("R209", "BLOCKED_MISSING_AUTHORITY", "BLOCKED_MISSING_AUTHORITY", None, 0),
            ("R230", "ENGINEERING_READY", "BLOCKED_MISSING_AUTHORITY", None, 8),
            ("R231", "ENGINEERING_READY", "BLOCKED_MISSING_AUTHORITY", "BLOCKED_MISSING_AUTHORITY", 4),
            ("R233", "ENGINEERING_READY", "BLOCKED_MISSING_AUTHORITY", None, 1),
            ("R235_PRESERVED_NONGRAPH", "ENGINEERING_READY", "BLOCKED_MISSING_AUTHORITY", None, 2),
            ("GATE5_R147", "ENGINEERING_READY", "BLOCKED_MISSING_AUTHORITY", None, 2),
        )), "exact source authority statuses")
        frontier = ledger.get("frontier_summary")
        need(typed_equal(frontier, {
            "Gate5_complete_18_field_global_blocks": 0,
            "Gate5_latest_strict_frontier_maturity": "10/18",
            "Gate5_strictly_blocked_fields": 8,
            "R209_direct_row_payload_available": False,
            "R231_independent_receipt_package_available": False,
            "blocked_missing_semantic_or_full_support_authority_sources": 6,
            "engineering_ready_row_sources": 5,
            "formal_credit": 0,
        }), "exact frontier zero credit")
        held.final()
        final_count = len(held.final_hashes)
    result = {
        "schema": SCHEMA,
        "status": "PASS_INDEPENDENT_BYTE_PATH_ORDER_AND_ZERO_CREDIT_REPLAY",
        "producer_sha256": PRODUCER_SHA256,
        "ledger_file_sha256": LEDGER_SHA256,
        "ledger_payload_sha256": envelope["ledger_sha256"],
        "upstream_pin_count": 30,
        "all_held_pin_count_including_producer_and_ledger": final_count,
        "selected_table_count": 17,
        "selected_row_count": 204_162,
        "upstream_row_sha256_closed_count": 67_026,
        "upstream_row_sha256_missing_count": 137_136,
        "manifest_count": 4,
        "source_authority_blocked_count": 6,
        "canonical_selected_row_cap_bytes": ROW_CAP,
        "bounded_memory_claim": False,
        "availability_limitation": "whole pinned certificate documents and selected row arrays are decoded in memory; no runtime/RSS bound is claimed",
        "formal_credit": 0,
        "normalized_full_support_credit": 0,
        "B1A_credit": 0,
        "CM2_credit": 0,
    }
    return {"schema": SCHEMA + ".envelope", "result": result, "result_sha256": sha(result)}


def self_test() -> dict[str, Any]:
    duplicate_ok = False
    try:
        decode(b'{"x":1,"x":2}', "duplicate")
    except VerifyBlocked:
        duplicate_ok = True
    need(duplicate_ok, "duplicate rejected")
    cap_ok = False
    try:
        streaming_digest({"x": "a" * ROW_CAP}, cap=ROW_CAP)
    except VerifyBlocked:
        cap_ok = True
    need(cap_ok, "post-encode row cap")
    need(not typed_equal({"formal_credit": False}, {"formal_credit": 0}), "false must not alias zero credit")
    need(not typed_equal({"row_count": True}, {"row_count": 1}), "true must not alias count one")
    return {"schema": SCHEMA + ".self-test", "status": "PASS", "checks": 4, "formal_credit": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    out = self_test() if args.self_test else verify()
    os.write(1, canonical_bytes(out) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
