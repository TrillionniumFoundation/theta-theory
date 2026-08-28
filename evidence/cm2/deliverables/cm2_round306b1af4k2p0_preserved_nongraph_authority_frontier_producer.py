#!/usr/bin/env python3
"""Round306B1AF4K2P0 preserved/non-graph direct authority frontier.

This is a read-only, zero-credit source-discovery and byte/row commitment
producer.  It does not import or execute upstream producers.  ``--full-replay``
opens only the exact pinned files, through held descriptors, and emits one
canonical JSON authority ledger to stdout.  It does not construct normalized
support, prove any support equivalence/incidence theorem, or mint B1A/CM2
credit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Final, Iterable


class FrontierBlocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise FrontierBlocked(label)


SCHEMA: Final = "cm2.round306b1af4k2p0.preserved-nongraph-authority-frontier.v1"
STATUS: Final = (
    "PASS_DIRECT_SOURCE_DISCOVERY_AND_ORDER_COMMITMENTS__"
    "ZERO_NORMALIZED_SUPPORT_THEOREM_B1A_OR_CM2_CREDIT"
)
HERE: Final = Path(__file__).parent
CANONICAL_SELECTED_ROW_CAP: Final = 8_388_608


# label, source family, filename, exact size, exact SHA-256, byte role
PINS: Final = (
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


# label, certificate, schema, result digest, selected result-relative path,
# exact row count, exact ordered-list digest, optional declared metadata path.
TABLES: Final = (
    ("R230_ABSENCE", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_resolved_child_event_zero_set_absence_ledger", "rows"), 8_976, "9e5451b5f808ff80b1bc25dcad1746a78cb8fa7ae3f77483a0fc3e47f2345626", ("formal_resolved_child_event_zero_set_absence_ledger", "rows_sha256")),
    ("R230_FACE_CANDIDATE", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_exact_face_candidate_ledger", "rows"), 1_512, "421dd9039658c7e8bcb17f434b9d80515e65188083a8905f11c249814bbc18ad", ("formal_exact_face_candidate_ledger", "rows_sha256")),
    ("R230_EDGE", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_certified_local_bulk_continuation_edge_ledger", "rows"), 784, "7a63ba5416a34ad1fcf5084dc0a5ee4b135816358c7a02b69e258bd9f924f6e3", ("formal_certified_local_bulk_continuation_edge_ledger", "rows_sha256")),
    ("R230_REJECT", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_rejected_local_bulk_candidate_ledger", "rows"), 740, "a1ca4f398d1202da6a504ffc977eac25cd68867b280f83eea76651dd257bd773", ("formal_rejected_local_bulk_candidate_ledger", "rows_sha256")),
    ("R230_STAR", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_certified_local_bulk_bridge_star_ledger", "rows"), 448, "2d3348cac30d52bf97a1fb62c342bbf317bf388d09b256f186485f11c3cf3152", ("formal_certified_local_bulk_bridge_star_ledger", "rows_sha256")),
    ("R230_INCIDENCE_DELTA", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_occurrence_known_block_incidence_delta_ledger", "rows"), 464, "e0663279b21bdd6e983907ef228bfe5ef88a606cb881de981f1d3b9d732869c0", ("formal_occurrence_known_block_incidence_delta_ledger", "rows_sha256")),
    ("R230_POST_OCCURRENCE", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_post_Round230_occurrence_known_block_frontier_ledger", "rows"), 53_968, "dcceb9f3ce4f210e3d16ea262b87678d061defd7e333fb4a963483feba0bca95", ("formal_post_Round230_occurrence_known_block_frontier_ledger", "rows_sha256")),
    ("R230_POST_KEY", "R230_CERT", "cm2.round230.source-g-resolved-retained-bulk-continuation.v1", "325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e", ("formal_post_Round230_key_frontier_ledger", "rows"), 116, "345678761e03efb721acc9d5e7ac3405371c4de383d671a7dfd8c6b3cbaf4be9", ("formal_post_Round230_key_frontier_ledger", "rows_sha256")),
    ("R231_RESOLVED", "R231_CERT", "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1", "83381b3ba9bd22e1616f3b77006113b88486e13ad81e3c9745cb89fd7798f06a", ("resolved_descendant_rows",), 22_348, "dcc8cdfb71e566a18cd512be31964b0e395b844443440e78924f479fc67cb0b5", ("resolved_descendant_rows_sha256",)),
    ("R231_GUARD", "R231_CERT", "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1", "83381b3ba9bd22e1616f3b77006113b88486e13ad81e3c9745cb89fd7798f06a", ("guard_descendant_rows",), 0, "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945", ("guard_descendant_rows_sha256",)),
    ("R231_FRONTIER", "R231_CERT", "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1", "83381b3ba9bd22e1616f3b77006113b88486e13ad81e3c9745cb89fd7798f06a", ("depth6_frontier_rows",), 67_924, "17fc58fcd194ed00ba2509e4fec1173b3bfdc1c5ae4586f24ecf8e7dd95d5fd3", ("depth6_frontier_rows_sha256",)),
    ("R231_ROOT", "R231_CERT", "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1", "83381b3ba9bd22e1616f3b77006113b88486e13ad81e3c9745cb89fd7798f06a", ("root_summary_rows",), 5_368, "2a67e24ed3dbedaa6a1615245cf7075dd7ecde4929bdcf3b36e92376e3f42d03", ("root_summary_rows_sha256",)),
    ("R233_PARTITION", "R233_CERT", "cm2.round233.source-g-outgoing-seam-parametric-graph-key-partition.v1", "6be5b81be350a7d575fb34dd80fce53046fb017096d497070a218c04f92a88fc", ("parametric_graph_key_partition_rows",), 3_148, "9b44e5120168e008bea5d0e621511d9e375f0422b97292817b6bb8bd35443356", ("parametric_graph_key_partition_rows_sha256",)),
    ("R235_SINGLE", "R235_CERT", "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1", "5bbcf6780338c9a40fa9c131b0270e4fb934de022cf597d2f82d6b85af68dca2", ("single_endpoint_graph_partition_rows",), 38_328, "e9a3794540170bf013160fb713acfbb1a65d42afedfb7b972cbfdad290549731", ("single_endpoint_graph_partition_rows_sha256",)),
    ("R235_DOUBLE_DEFERRED", "R235_CERT", "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1", "5bbcf6780338c9a40fa9c131b0270e4fb934de022cf597d2f82d6b85af68dca2", ("double_endpoint_deferred_rows",), 16, "52e01cc83edcd02f9746701201508e0851fe8df6d44cee77c1aa23301d964572", ("double_endpoint_deferred_rows_sha256",)),
    ("R147_GATE5_FIELDS", "R147_CERT", "cm2.round147.gate5-strict-reaudit-upgrade-frontier.v1", "00649a259ff69590eed6a9f4e828b6a622c0c03deb3ca07a70526446b827e922", ("gate5_field_rows",), 18, "36de71e5bf06200fa689ad8cb3b26e2d1589f868a38cd2c8dd83df7b232edcc6", ("gate5_field_rows_sha256",)),
    ("R147_EXECUTABLE_FRONTIER", "R147_CERT", "cm2.round147.gate5-strict-reaudit-upgrade-frontier.v1", "00649a259ff69590eed6a9f4e828b6a622c0c03deb3ca07a70526446b827e922", ("executable_upgrade_frontier",), 4, "6cdf91412fde699ea2bb9ed1b939de70ecee361875c8b526b943209ad0cf6d18", ()),
)


MANIFESTS: Final = {
    "R230_MANIFEST": ("R230_SOURCE", "R230_CERT", "R230_VERIFIER", "R230_VERIFICATION"),
    "R233_MANIFEST": ("R233_SOURCE", "R233_CERT", "R233_VERIFIER", "R233_VERIFICATION"),
    "R235_MANIFEST": ("R235_SOURCE", "R235_CERT", "R235_VERIFIER", "R235_VERIFICATION"),
    "R147_MANIFEST": ("R147_SOURCE", "R147_CERT", "R147_VERIFIER", "R147_VERIFICATION", "R147_REPORT", "R147_COLD", "R147_ATTACK"),
}


def canonical_bytes(value: Any, *, ascii_only: bool = True) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=ascii_only, allow_nan=False).encode("ascii" if ascii_only else "utf-8")


def sha(value: Any, *, ascii_only: bool = True) -> str:
    return hashlib.sha256(canonical_bytes(value, ascii_only=ascii_only)).hexdigest()


def duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_float(token: str) -> Any:
    raise FrontierBlocked("nonintegral JSON number:" + token)


def reject_constant(token: str) -> Any:
    raise FrontierBlocked("nonstandard JSON constant:" + token)


def decode_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=duplicate_reject,
                           parse_float=reject_float, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise FrontierBlocked("JSON decode:" + label) from exc
    need(isinstance(value, dict), "JSON root object:" + label)
    return value


def identity(st: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size,
        st.st_mtime_ns, st.st_ctime_ns,
    )


def directory_identity(st: os.stat_result) -> tuple[int, int, int]:
    # Directory timestamps legitimately change when unrelated deliverables are
    # created concurrently.  Path replacement is bound by dev/inode/mode.
    return (st.st_dev, st.st_ino, st.st_mode)


class HeldPins:
    def __init__(self) -> None:
        self.directory_fd = -1
        self.directory_before: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.by_label = {row[0]: row for row in PINS}
        self.hash_passes: dict[str, tuple[str, str]] = {}
        self.final_hashes: dict[str, str] = {}

    def __enter__(self) -> "HeldPins":
        root = os.fspath(HERE)
        before = os.stat(root, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "input directory regular")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.directory_fd = os.open(root, flags)
        held = os.fstat(self.directory_fd)
        need(directory_identity(before) == directory_identity(held), "directory open race")
        self.directory_before = held
        try:
            for label, _family, filename, exact_size, expected_sha, _role in PINS:
                need(filename == os.path.basename(filename) and filename not in {".", ".."}, "pin basename")
                path_before = os.stat(filename, dir_fd=self.directory_fd, follow_symlinks=False)
                need(stat.S_ISREG(path_before.st_mode), "regular file:" + label)
                need(path_before.st_nlink == 1, "nlink=1:" + label)
                need(path_before.st_size == exact_size, "exact size:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.directory_fd)
                opened = os.fstat(fd)
                need(identity(path_before) == identity(opened), "open race:" + label)
                need(stat.S_ISREG(opened.st_mode) and opened.st_nlink == 1, "held regular/nlink:" + label)
                self.fds[label] = fd
                h1 = self._hash(fd)
                h2 = self._hash(fd)
                need(h1 == expected_sha and h2 == expected_sha, "two-pass SHA:" + label)
                path_after = os.stat(filename, dir_fd=self.directory_fd, follow_symlinks=False)
                need(identity(path_after) == identity(opened), "path/FD after hash:" + label)
                self.hash_passes[label] = (h1, h2)
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

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
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)

    def final_revalidate(self) -> None:
        need(self.directory_fd >= 0 and self.directory_before is not None, "held set active")
        for label, _family, filename, _size, expected_sha, _role in PINS:
            final_sha = self._hash(self.fds[label])
            need(final_sha == expected_sha, "final full SHA:" + label)
            self.final_hashes[label] = final_sha
            held = os.fstat(self.fds[label])
            path = os.stat(filename, dir_fd=self.directory_fd, follow_symlinks=False)
            need(identity(held) == identity(path), "final path/FD:" + label)
            need(stat.S_ISREG(held.st_mode) and held.st_nlink == 1, "final regular/nlink:" + label)
        held_dir = os.fstat(self.directory_fd)
        path_dir = os.stat(os.fspath(HERE), follow_symlinks=False)
        need(
            directory_identity(self.directory_before)
            == directory_identity(held_dir)
            == directory_identity(path_dir),
            "final directory path",
        )

    def __exit__(self, *_args: object) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds.clear()
        if self.directory_fd >= 0:
            try:
                os.close(self.directory_fd)
            except OSError:
                pass
            self.directory_fd = -1


def get_path(root: Any, path: Iterable[str], label: str) -> Any:
    node = root
    for part in path:
        need(isinstance(node, dict) and part in node, "exact path:" + label + ":" + part)
        node = node[part]
    return node


def streaming_digest(value: Any, *, cap: int | None = None) -> str:
    encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False, allow_nan=False)
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
    ordered_hashes: list[str] = []
    closed = 0
    for row in rows:
        need(isinstance(row, dict), "selected row object")
        ordered_hashes.append(streaming_digest(row, cap=CANONICAL_SELECTED_ROW_CAP))
        if "row_sha256" in row:
            expected = row["row_sha256"]
            need(isinstance(expected, str) and len(expected) == 64, "row SHA format")
            body = dict(row)
            del body["row_sha256"]
            need(streaming_digest(body, cap=CANONICAL_SELECTED_ROW_CAP) == expected, "row SHA closure")
            closed += 1
    return {
        "row_count": len(rows),
        "ordered_rows_sha256": streaming_digest(rows),
        "ordered_row_digest_sequence_sha256": sha(ordered_hashes),
        "unordered_row_digest_multiset_sha256": sha(sorted(ordered_hashes)),
        "first_row_sha256": ordered_hashes[0] if ordered_hashes else None,
        "last_row_sha256": ordered_hashes[-1] if ordered_hashes else None,
        "upstream_row_sha256_closed_count": closed,
        "upstream_row_sha256_missing_count": len(rows) - closed,
    }


def validate_manifest(raw: bytes, expected_labels: tuple[str, ...], by_label: dict[str, tuple[Any, ...]]) -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for line in raw.decode("ascii").splitlines():
        parts = line.split("  ", 1)
        need(len(parts) == 2 and len(parts[0]) == 64, "manifest syntax")
        digest_text, filename = parts
        need(filename not in seen, "manifest duplicate filename")
        seen.add(filename)
        rows.append({"filename": filename, "sha256": digest_text})
    expected = []
    for label in expected_labels:
        pin = by_label[label]
        expected.append({"filename": pin[2], "sha256": pin[4]})
    need(rows == expected, "manifest exact ordered membership")
    return {"entry_count": len(rows), "ordered_entries_sha256": sha(rows), "exact_membership": True}


def source_statuses(table_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in table_rows:
        grouped.setdefault(row["source_family"], []).append(row)
    return [
        {
            "source_family": "R209",
            "row_materialization_status": "BLOCKED_MISSING_AUTHORITY",
            "authority_status": "BLOCKED_MISSING_AUTHORITY",
            "reason": "nonformal probe emits only compact summary hashes; no sealed direct row payload, formal certificate, independent verifier, verification receipt, or manifest",
            "candidate_summary_only": {"sheet_rows": 17_716, "curve_rows": 20_456, "endpoint_rows": 40_912},
            "selected_table_commitment_count": 0,
        },
        {
            "source_family": "R230",
            "row_materialization_status": "ENGINEERING_READY",
            "authority_status": "BLOCKED_MISSING_AUTHORITY",
            "reason": "direct rows and a receipt package are pinned, but local bulk/incidence rows explicitly issue zero normalized-full-support, membership, maximality, fibre, and global credit",
            "selected_table_commitment_count": len(grouped.get("R230", [])),
        },
        {
            "source_family": "R231",
            "row_materialization_status": "ENGINEERING_READY",
            "receipt_package_status": "BLOCKED_MISSING_AUTHORITY",
            "authority_status": "BLOCKED_MISSING_AUTHORITY",
            "reason": "certificate rows are pinned and order-committed, but no independent verifier, verification receipt, report, cold replay, or manifest exists in the authority root; upstream rows also lack per-row SHA closure",
            "selected_table_commitment_count": len(grouped.get("R231", [])),
        },
        {
            "source_family": "R233",
            "row_materialization_status": "ENGINEERING_READY",
            "authority_status": "BLOCKED_MISSING_AUTHORITY",
            "reason": "direct graph-key partition rows are pinned, but lack per-row SHA closure and certify only local key dispositions with zero full-support/global credit",
            "selected_table_commitment_count": len(grouped.get("R233", [])),
        },
        {
            "source_family": "R235_PRESERVED_NONGRAPH",
            "row_materialization_status": "ENGINEERING_READY",
            "authority_status": "BLOCKED_MISSING_AUTHORITY",
            "reason": "this is the preserved/non-graph single-endpoint graph-word partition, not a G2 authority; 16 double-endpoint factors remain deferred, rows lack per-row SHA closure, and global credit is zero",
            "selected_table_commitment_count": len(grouped.get("R235_PRESERVED_NONGRAPH", [])),
        },
        {
            "source_family": "GATE5_R147",
            "row_materialization_status": "ENGINEERING_READY",
            "authority_status": "BLOCKED_MISSING_AUTHORITY",
            "reason": "latest strict frontier receipt only: 10/18 fields satisfied, 8/18 strictly blocked, zero upgrades and zero complete 18-field global blocks; it is not automatic row-level theorem authority",
            "selected_table_commitment_count": len(grouped.get("GATE5_R147", [])),
        },
    ]


def full_replay() -> dict[str, Any]:
    pin_by_label = {row[0]: row for row in PINS}
    cert_cache: dict[str, dict[str, Any]] = {}
    table_rows: list[dict[str, Any]] = []
    with HeldPins() as held:
        for table_label, cert_label, schema, result_sha, path, count, ordered_sha, declared_path in TABLES:
            if cert_label not in cert_cache:
                cert_cache[cert_label] = decode_json(held.bytes(cert_label), cert_label)
            doc = cert_cache[cert_label]
            need(doc.get("schema") == schema, "certificate schema:" + cert_label)
            need(doc.get("result_sha256") == result_sha, "certificate result pin:" + cert_label)
            result = doc.get("result")
            need(isinstance(result, dict), "certificate result object:" + cert_label)
            need(streaming_digest(result) == result_sha, "certificate result recompute:" + cert_label)
            rows = get_path(result, path, table_label)
            need(isinstance(rows, list), "selected table array:" + table_label)
            commitment = table_commitment(rows)
            need(commitment["row_count"] == count, "table count:" + table_label)
            need(commitment["ordered_rows_sha256"] == ordered_sha, "table ordered digest:" + table_label)
            if declared_path:
                need(get_path(result, declared_path, table_label) == ordered_sha, "declared table digest:" + table_label)
            family = pin_by_label[cert_label][1]
            table_rows.append({
                "table_label": table_label,
                "source_family": family,
                "certificate_label": cert_label,
                "exact_result_property_path": ["result", *path],
                "declared_digest_property_path": ["result", *declared_path] if declared_path else None,
                **commitment,
            })
        manifests = {
            manifest_label: validate_manifest(held.bytes(manifest_label), member_labels, pin_by_label)
            for manifest_label, member_labels in MANIFESTS.items()
        }
        held.final_revalidate()
        pin_rows = [
            {
                "label": label, "source_family": family, "filename": filename,
                "exact_size": size, "sha256": digest_text, "role": role,
                "two_pass_held_fd_sha256": list(held.hash_passes[label]),
                "final_post_parse_held_fd_sha256": held.final_hashes[label],
            }
            for label, family, filename, size, digest_text, role in PINS
        ]
    statuses = source_statuses(table_rows)
    total_rows = sum(row["row_count"] for row in table_rows)
    closed_rows = sum(row["upstream_row_sha256_closed_count"] for row in table_rows)
    ledger = {
        "schema": SCHEMA,
        "status": STATUS,
        "artifact_kind": "ZERO_CREDIT_DIRECT_SOURCE_AUTHORITY_FRONTIER",
        "scope": {
            "included": ["PRESERVED", "NON_GRAPH_BULK", "P1_B06_DIRECT_EVIDENCE_FRONTIER"],
            "excluded": ["R2", "R292", "G2A", "G2B", "NORMALIZED_SUPPORT_CONSTRUCTION", "B1A", "B2"],
            "formal_credit": 0,
            "normalized_full_support_credit": 0,
            "representation_cover_credit": 0,
            "B1A_credit": 0,
            "CM2_credit": 0,
        },
        "authority_priority": [
            "DIRECT_CERTIFICATE_ROW_WITH_EXACT_PATH_AND_ORDER_COMMITMENT",
            "SOURCE_CODE_REPLAY_PLUS_INDEPENDENT_VERIFICATION_RECEIPT",
            "SEALED_FRONTIER_RECEIPT",
            "REPORT_OR_MANIFEST",
            "NONFORMAL_PROBE_SUMMARY",
        ],
        "priority_nonpromotion": "no priority tier is a semantic/full-support theorem without a separate input-bound semantic checker and source-exhaustion proof",
        "input_security": {
            "pin_count": len(pin_rows),
            "total_pinned_bytes": sum(row["exact_size"] for row in pin_rows),
            "regular_file_required": True,
            "nlink_must_equal_one": True,
            "O_NOFOLLOW": True,
            "held_directory_descriptor": True,
            "two_full_sha256_passes_per_held_fd": True,
            "final_full_sha256_pass_after_all_parsing": True,
            "path_fd_identity_before_after_and_final": True,
            "directory_path_identity_final": True,
            "symlink_hardlink_TOCTOU": "FAIL_CLOSED",
            "upstream_python_imported_or_executed": False,
            "temporary_files_or_spill": False,
            "canonical_selected_row_cap_bytes": CANONICAL_SELECTED_ROW_CAP,
            "whole_certificate_JSON_loaded_in_memory": True,
            "bounded_memory_claim": False,
            "availability_limitation": "whole pinned certificate documents and selected row arrays are decoded in memory; exact input sizes are pinned, but no runtime/RSS bound is claimed",
        },
        "exact_pins": pin_rows,
        "selected_tables": table_rows,
        "selected_table_summary": {
            "table_count": len(table_rows),
            "row_count": total_rows,
            "upstream_row_sha256_closed_count": closed_rows,
            "upstream_row_sha256_missing_count": total_rows - closed_rows,
            "table_commitments_sha256": sha(table_rows),
        },
        "manifest_replay": manifests,
        "source_authority_status": statuses,
        "frontier_summary": {
            "engineering_ready_row_sources": 5,
            "blocked_missing_semantic_or_full_support_authority_sources": 6,
            "R209_direct_row_payload_available": False,
            "R231_independent_receipt_package_available": False,
            "Gate5_latest_strict_frontier_maturity": "10/18",
            "Gate5_strictly_blocked_fields": 8,
            "Gate5_complete_18_field_global_blocks": 0,
            "formal_credit": 0,
        },
        "required_next": [
            "mint a sealed row-bearing R209 formal certificate and independent receipt package",
            "mint an independent R231 verifier/verification/report/cold-replay/manifest package",
            "supply input-bound semantic theorem certificates for every consumed direct row",
            "prove exact construction-source exhaustion, representation backbinding, incidence/equivalence, and full-support equality",
            "keep the eight Gate5 fields blocked until independent global evidence exists",
        ],
    }
    return {"schema": SCHEMA + ".envelope", "ledger": ledger, "ledger_sha256": sha(ledger)}


def contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "READY_FOR_EXPLICIT_FULL_REPLAY__ZERO_CREDIT",
        "pin_count": len(PINS),
        "pinned_bytes": sum(row[3] for row in PINS),
        "selected_table_count": len(TABLES),
        "candidate_and_production_modes": "FAIL_BEFORE_FILESYSTEM",
        "formal_credit": 0,
    }


def self_test() -> dict[str, Any]:
    need(len({row[0] for row in PINS}) == len(PINS), "pin labels unique")
    need(len({row[2] for row in PINS}) == len(PINS), "pin filenames unique")
    need(len({row[0] for row in TABLES}) == len(TABLES), "table labels unique")
    need(all(len(row[4]) == 64 for row in PINS), "pin SHA format")
    need(all(isinstance(row[5], int) and row[5] >= 0 and len(row[6]) == 64 for row in TABLES), "table count/SHA format")
    sample = b'{"a":1,"a":2}'
    duplicate_rejected = False
    try:
        decode_json(sample, "self-test")
    except FrontierBlocked:
        duplicate_rejected = True
    need(duplicate_rejected, "duplicate key rejected")
    return {"schema": SCHEMA + ".self-test", "status": "PASS", "checks": 6, "formal_credit": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-replay", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--produce", action="store_true")
    args = parser.parse_args()
    if args.candidate or args.produce:
        raise FrontierBlocked("candidate/production blocked before filesystem")
    if args.full_replay:
        out = full_replay()
    elif args.self_test:
        out = self_test()
    else:
        out = contract()
    os.write(1, canonical_bytes(out) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
