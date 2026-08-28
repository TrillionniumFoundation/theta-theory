#!/usr/bin/env python3
"""Independent verifier for the K2G0 zero-credit G2 authority frontier.

The verifier does not import, execute, tokenize, or parse the producer.  It
uses an independently duplicated input allowlist, rechecks every byte pin and
selected upstream manifest, validates the frozen ordered-table commitments and
semantic/nonclaim frontier, and publishes verification last.  It does not
rederive the heavy B1G0 row streams and therefore cannot mint theorem credit.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from typing import Any, Final


class Blocked(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Blocked(label)


def type_strict_equal(actual: Any, expected: Any) -> bool:
    """Recursive equality that never admits Python bool/int aliases."""
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        if set(actual) != set(expected):
            return False
        return all(type_strict_equal(actual[key], expected[key]) for key in expected)
    if type(expected) is list:
        return len(actual) == len(expected) and all(
            type_strict_equal(left, right) for left, right in zip(actual, expected)
        )
    if type(expected) is tuple:
        return len(actual) == len(expected) and all(
            type_strict_equal(left, right) for left, right in zip(actual, expected)
        )
    return bool(actual == expected)


def strict_need(actual: Any, expected: Any, label: str) -> None:
    need(type_strict_equal(actual, expected), label)


HERE: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306b1af4k2g0_source_g_g2_semantic_authority_frontier_"
SCHEMA: Final = "cm2.round306b1af4k2g0.source-g-g2-semantic-authority-frontier.independent-verification.v1"
LEDGER_SCHEMA: Final = "cm2.round306b1af4k2g0.source-g-g2-semantic-authority-frontier.v1"
STATUS: Final = "PASS_INDEPENDENT_K2G0_EXACT_AUTHORITY_FRONTIER__ZERO_FORMAL_CREDIT"
ROW_CAP: Final = 8_388_608

PRODUCER: Final = PREFIX + "producer.py"
PRODUCER_SIZE: Final = 33_577
PRODUCER_SHA: Final = "dd788f526faf8a2179aa1b440309c75753a440caf30ae7834c20367704b0847b"
LEDGER: Final = PREFIX + "ledger.json"
LEDGER_SIZE: Final = 18_862
LEDGER_SHA: Final = "af0d3a52c916224826d766388d585b02e35a8ea20597fe78e72eb0e9fbfa9ccd"
RESULT: Final = PREFIX + "result.json"
RESULT_SIZE: Final = 1_523
RESULT_SHA: Final = "eb1e2fdf2985b142eb6c4c53a585757d74ce787f7b74d8ba95c652de80b291d1"
VERIFICATION: Final = PREFIX + "verification.json"
REPORT: Final = PREFIX + "report.md"
COLD: Final = PREFIX + "cold_replay.md"
MANIFEST: Final = PREFIX + "manifest.sha256"

# label, filename, exact size, SHA-256.  This is intentionally duplicated and
# not accepted from the candidate ledger.
PINS: Final = (
    ("AF2", "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py", 52_538, "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5"),
    ("G1", "cm2_round306b1af4g1_source_g_g2_exact_join_preflight.py", 92_288, "fce556387520b6e27af9ba5d6e816e91325a629750855af0fffae36dfdba765d"),
    ("B0_MEMBER", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af"),
    ("B1G0_PRODUCER", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py", 90_721, "97f1d0736a616071dbb0dba3bf533e3fae96091fc6b165395436216bb69c9321"),
    ("B1G0_VERIFIER", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_promotion_verifier.py", 128_011, "47d642bfd90c8f8040a7de97df88788f2295e60b50ad7c72bb8ae2e85d89004b"),
    ("B1G0_GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    ("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    ("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    ("B1G0_CORRECTION", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz", 140_958, "834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a"),
    ("B1G0_BACKBIND", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz", 32_731_854, "79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b"),
    ("B1G0_GAP", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809"),
    ("B1G0_RESULT", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json", 5_006, "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e"),
    ("B1G0_VERIFICATION", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json", 11_575, "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a"),
    ("B1G0_MANIFEST", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8"),
    ("R245_CERT", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json", 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1"),
    ("R245_VERIFICATION", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_verification.json", 1_016, "7b116fce6abfad827a19da4e6637bac50c784c0e53b84e9bfd9567abb35bef14"),
    ("R245_MANIFEST", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256", 897, "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac"),
    ("R248_CERT", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
    ("R248_VERIFICATION", "cm2_round248_source_g_wall_finite_key_retained_quotient_verification.json", 1_028, "5e20ada49b5bca2e7ebaf6b78835c4ca1a6051e24960b7d00b3ae9d596f11a10"),
    ("R248_MANIFEST", "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256", 885, "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07"),
    ("R300E_WITNESS", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_witness_ledger.json.gz", 17_175_071, "69f480da55e917b7b75bfe1efa823a9228d9b563f6f3aabd4e2a364c9e50eb9f"),
    ("R300E_RESULT", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_result.json", 5_168, "193c74535431789ba4fcdad598487916712d6ad1c04f191a083076e4a05f7e3e"),
    ("R300E_VERIFICATION", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_verification.json", 2_153, "313008d59a2d67b5ce4b7c8d62cd68a26a855a65c34396b5ae0176dda2096d4a"),
    ("R300E_MANIFEST", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_manifest.sha256", 1_571, "4e6c4eec1af04a907285d41395aeef63e911b3b5486db91b33a95fa62e45177a"),
    ("R302A_LEDGER", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_ledger.json.gz", 14_522, "f71feba87a6ae9e8524c2d86c7489ffe19c71dd08c9ebec75a90702f0e81b558"),
    ("R302A_RESULT", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_result.json", 4_897, "5fddf94222712385684c117d220a165934450a80a318ae3d26e26a81ef3cc160"),
    ("R302A_VERIFICATION", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_verification.json", 1_737, "28214c45a373365587087c21ee51c0e1eec7c4195afccb356b5b36b8ccbaeb71"),
    ("R302A_MANIFEST", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_manifest.sha256", 1_358, "b4a53c485da9fd889e3a9194c7e770f2a32eb14027e8bfd0f7c2370eab9eca71"),
    ("R302C_LEDGER", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_disposition_ledger.json.gz", 20_435_193, "c326d50f62a427c71e6f41b188b00b08baf6db7bf535ba082f23678239eebba6"),
    ("R302C_RESULT", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_result.json", 8_144, "d371d3d6ce01b0779717dc817216204cf0c142d0b95caf42ede3d1d243d5daa2"),
    ("R302C_VERIFICATION", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_verification.json", 1_945, "da663f790488e85c8973bd62c8af269abfd19e3e7ee19aa3f2335091a9dd81d9"),
    ("R302C_MANIFEST", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_manifest.sha256", 1_275, "42fa1ad2266e3bef38f034489085c325d656ff94ddf2f9710c7c68ab90646dc1"),
    ("K1_KERNEL", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py", 68_346, "17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae"),
    ("K1_RESULT", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_result.json", 2_787, "e9ff89a5d51f5e79864f10dc34dd4b5f12887c029f65c2196c60f50bd4c77b21"),
    ("K1_VERIFICATION", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_verification.json", 3_777, "4d1d5d20d7f61906262486582b9cb407935f6b883989165b7a7938994fedf0d8"),
    ("K1_MANIFEST", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_manifest.sha256", 933, "07a3f12e75c43fd459dfd4e86c918b349c09226c94735b1a6d16432f1caca939"),
    ("R288_RESULT", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json", 8_981, "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569"),
    ("R288_VERIFICATION", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json", 9_874, "f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23"),
    ("R288_MANIFEST", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_manifest.sha256", 1_203, "c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb"),
    ("R294_RESULT", "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json", 6_958, "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626"),
    ("R294_VERIFICATION", "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json", 6_529, "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245"),
    ("R294_MANIFEST", "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256", 1_275, "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131"),
)

PRIMARY: Final = (
    ("PRODUCER", PRODUCER, PRODUCER_SIZE, PRODUCER_SHA),
    ("LEDGER", LEDGER, LEDGER_SIZE, LEDGER_SHA),
    ("RESULT", RESULT, RESULT_SIZE, RESULT_SHA),
)

MANIFESTS: Final = {
    "B1G0_MANIFEST": ("B1G0_PRODUCER", "B1G0_VERIFIER", "B1G0_GRAPH", "B1G0_SHEET", "B1G0_SIDE", "B1G0_CORRECTION", "B1G0_BACKBIND", "B1G0_GAP", "B1G0_RESULT", "B1G0_VERIFICATION"),
    "R245_MANIFEST": ("R245_CERT", "R245_VERIFICATION"),
    "R248_MANIFEST": ("R248_CERT", "R248_VERIFICATION"),
    "R300E_MANIFEST": ("R300E_WITNESS", "R300E_RESULT", "R300E_VERIFICATION"),
    "R302A_MANIFEST": ("R302A_LEDGER", "R302A_RESULT", "R302A_VERIFICATION"),
    "R302C_MANIFEST": ("R302C_LEDGER", "R302C_RESULT", "R302C_VERIFICATION"),
    "K1_MANIFEST": ("K1_KERNEL", "K1_RESULT", "K1_VERIFICATION"),
    "R288_MANIFEST": ("R288_RESULT", "R288_VERIFICATION"),
    "R294_MANIFEST": ("R294_RESULT", "R294_VERIFICATION"),
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def dup_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate key:" + key)
        out[key] = value
    return out


def decode(raw: bytes, label: str) -> dict[str, Any]:
    need(len(raw) <= ROW_CAP, "selected bytes cap:" + label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=dup_reject,
                           parse_float=lambda token: (_ for _ in ()).throw(Blocked("float:" + token)),
                           parse_constant=lambda token: (_ for _ in ()).throw(Blocked("constant:" + token)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Blocked("decode:" + label) from exc
    need(type(value) is dict, "root object:" + label)
    need(len(canonical(value)) <= ROW_CAP, "final canonical cap:" + label)
    return value


def file_identity(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def dir_identity(st: os.stat_result) -> tuple[int, int, int]:
    return (st.st_dev, st.st_ino, st.st_mode)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dirstat: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.expected = {row[0]: row for row in (*PINS, *PRIMARY)}
        self.initial: dict[str, tuple[str, str]] = {}
        self.final: dict[str, str] = {}

    @staticmethod
    def _hash(fd: int) -> str:
        os.lseek(fd, 0, os.SEEK_SET)
        h = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                return h.hexdigest()
            h.update(chunk)

    def __enter__(self) -> "Snapshot":
        before = os.stat(HERE, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode), "deliverables dir")
        self.dirfd = os.open(HERE, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        held_dir = os.fstat(self.dirfd)
        need(dir_identity(before) == dir_identity(held_dir), "directory race")
        self.dirstat = held_dir
        try:
            for label, filename, size, sha256 in (*PINS, *PRIMARY):
                need(filename == os.path.basename(filename), "basename:" + label)
                path = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(path.st_mode) and path.st_nlink == 1, "regular/nlink:" + label)
                need(path.st_size == size, "size:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                held = os.fstat(fd)
                need(file_identity(path) == file_identity(held), "open race:" + label)
                self.fds[label] = fd
                h1, h2 = self._hash(fd), self._hash(fd)
                need(h1 == h2 == sha256, "two-pass SHA:" + label)
                need(file_identity(held) == file_identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)), "post-hash path:" + label)
                self.initial[label] = (h1, h2)
            return self
        except BaseException:
            self.__exit__()
            raise

    def bytes(self, label: str) -> bytes:
        fd = self.fds[label]
        os.lseek(fd, 0, os.SEEK_SET)
        out: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                return b"".join(out)
            total += len(chunk)
            need(total <= ROW_CAP, "selected cap:" + label)
            out.append(chunk)

    def check_manifests(self) -> None:
        for manifest_label, required in MANIFESTS.items():
            rows: dict[str, str] = {}
            for line in self.bytes(manifest_label).decode("ascii").splitlines():
                if not line.strip():
                    continue
                parts = line.split()
                need(len(parts) == 2 and len(parts[0]) == 64, "manifest grammar:" + manifest_label)
                name = os.path.basename(parts[1])
                need(name not in rows, "manifest duplicate:" + name)
                rows[name] = parts[0]
            for label in required:
                expected = self.expected[label]
                need(rows.get(expected[1]) == expected[3], "manifest binding:" + manifest_label + ":" + label)

    def final_revalidate(self) -> None:
        for label, filename, _size, sha256 in (*PINS, *PRIMARY):
            final = self._hash(self.fds[label])
            need(final == sha256, "final SHA:" + label)
            held = os.fstat(self.fds[label])
            path = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(file_identity(held) == file_identity(path), "final path/FD:" + label)
            need(stat.S_ISREG(held.st_mode) and held.st_nlink == 1, "final regular/nlink:" + label)
            self.final[label] = final
        need(self.dirstat is not None, "held dir")
        need(dir_identity(self.dirstat) == dir_identity(os.fstat(self.dirfd)) == dir_identity(os.stat(HERE, follow_symlinks=False)), "final directory")

    def __exit__(self, *_args: object) -> None:
        for fd in self.fds.values():
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds.clear()
        if self.dirfd >= 0:
            try:
                os.close(self.dirfd)
            except OSError:
                pass
            self.dirfd = -1


EXPECTED_TABLES: Final = {
    "graph": (38_624, "a684dad14281e44c9dc02a0f825af661ef152f86a436c827fc0b113d25b4d6a0", "beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f"),
    "sheet": (38_624, "3686f3b90a77195dbecd08750707a32f98e07f9fdff5f59d57f09c1178a48fda", "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f"),
    "side": (76_848, "108bdcbe1c124de15d8f48f82a3cdb7aa545f6f61294be34e3e5b07979d6670e", "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2"),
    "correction": (400, "a4af6f87737028981be9dccae9c2c28236408aa1f112f507418b6e4516eeb671", "a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67"),
    "member": (115_456, "65493ba72be6047b7c1c4ea64045460ad8160ab05440d02204393d3697a4d541", "35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6"),
    "gap": (154_096, "5324319ce7b3f90f67b3e12af6848f851008fd52c7cbd7c8d433cd0652c52f9e", "d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b"),
}


def validate(ledger: dict[str, Any], result: dict[str, Any]) -> None:
    strict_need(ledger["schema"], LEDGER_SCHEMA, "ledger schema")
    strict_need(ledger["status"], "PASS_EXACT_G2_AUTHORITY_FRONTIER__SEMANTIC_GAPS_NONZERO__ZERO_FORMAL_CREDIT", "ledger status")
    strict_need(result["schema"], LEDGER_SCHEMA + ".result.v1", "result schema")
    strict_need(result["status"], ledger["status"], "result status")
    strict_need(ledger["producer"], {"filename": PRODUCER, "size": PRODUCER_SIZE, "sha256": PRODUCER_SHA}, "producer binding")
    candidate_pins = ledger["snapshot"]["pins"]
    need(type(candidate_pins) is list and len(candidate_pins) == len(PINS), "pin count")
    strict_need([(row["label"], row["filename"], row["exact_size"], row["sha256"]) for row in candidate_pins], list(PINS), "independent pin allowlist")
    need(ledger["snapshot"]["held_fd_two_pass_and_final_sha"] is True, "held FD claim")
    need(ledger["snapshot"]["final_path_revalidated"] is True, "final path claim")
    need(ledger["snapshot"]["symlink_hardlink_TOCTOU_fail_closed"] is True, "filesystem claim")

    census = ledger["exact_census"]
    strict_need(census, {"G2_distinct_members": 115_456, "G2_representations_current_exact_index_candidate": 115_456,
                    "G2a_R245": 264, "G2a_R248": 38_360, "G2a_members": 38_624,
                    "G2b_R245_distinct_members": 528, "G2b_R245_references": 528,
                    "G2b_R248_distinct_members": 76_304, "G2b_R248_references": 76_320,
                    "G2b_distinct_members": 76_832, "G2b_references": 76_848,
                    "duplicate_side_reference_excess": 16}, "exact census")
    strict_need(result["exact_census"], census, "result census")

    for key, (count, ledger_sha, rows_sha) in EXPECTED_TABLES.items():
        row = ledger["ordered_table_commitments"][key]
        strict_need(row["row_count"], count, "ordered table count:" + key)
        strict_need(row["ledger_sha256"], ledger_sha, "ordered table ledger SHA:" + key)
        strict_need(row["rows_sha256"], rows_sha, "ordered table rows SHA:" + key)
        need(type(row["path"]) is list and len(row["path"]) == 1, "table path:" + key)
        need(len(row["row_ids_sha256"]) == 64 and len(row["row_hashes_sha256"]) == 64, "table row commitments:" + key)

    gaps = ledger["semantic_gaps"]
    strict_need(gaps, {"B1G0_explicit_gap_rows": 154_096, "distinct_member_full_support_equalities_pending": 115_456,
                  "graph_sheet_physical_incidence_pending": 38_624, "graph_side_physical_incidence_reference_pending": 76_848,
                  "physical_incidence_rows_pending": 115_472, "representation_pullback_theorems_pending": 115_456,
                  "source_free_graph_definition_pending": 38_624, "unresolved_semantic_gap_zero": False}, "exact gaps")
    strict_need(result["semantic_gaps"], gaps, "result gaps")
    need(len(ledger["authority_frontier"]) == 7, "authority classes")
    statuses = {row["source"]: row["status"] for row in ledger["authority_frontier"]}
    strict_need(statuses["B1G0/G1/B0"], "ENGINEERING_EXACT_IDENTITY_AND_ORDER_ONLY", "identity-only class")
    strict_need(statuses["R245"], "LOCAL_INPUT_BOUND_PHYSICAL_QUOTIENT_AUTHORITY", "R245 local authority")
    strict_need(statuses["R248"], "LOCAL_INPUT_BOUND_WALL_QUOTIENT_AUTHORITY", "R248 local authority")
    strict_need(statuses["R300E"], "NARROW_INPUT_BOUND_COMPONENT_CONNECTIVITY_AUTHORITY", "R300E narrow authority")
    strict_need(statuses["K1"], "CHECKER_FOUNDATION_ZERO_CREDIT", "K1 checker")
    strict_need(statuses["R288/R294"], "OPEN_3D_STAGE_A_IDENTITY_CONTEXT_NOT_G2_COVER", "R294 noncover")
    need(all(value is False for value in ledger["strict_nonclaims"].values()), "strict nonclaims")
    need(all(type(value) is int and value == 0 for value in ledger["formal_credit"].values()), "formal credit zero strict type")
    strict_need(result["formal_credit"], ledger["formal_credit"], "result credits")
    strict_need(ledger["downstream_state"], {"B1A": "BLOCKED", "B2": "NOT_AUTHORIZED_BY_THIS_FRONTIER", "CM2": "NO-GO_FOR_CLAIM", "D02": "BLOCKED"}, "ledger downstream state")
    strict_need(result["downstream_state"], ledger["downstream_state"], "result downstream state")
    resource = ledger["resource_boundary"]
    strict_need(resource["canonical_selected_row_cap_bytes"], ROW_CAP, "row cap")
    need(resource["final_canonical_cap_checked_after_successful_decode"] is True, "post-decode cap")
    strict_need(resource["temporary_directory"], "/tmp", "scratch root")
    need(resource["temporary_directory_resolved_outside_deliverables"] is True, "scratch boundary")
    need(resource["bounded_memory_claim"] is False and resource["resource_exhaustion_mints_credit"] is False, "availability boundary")
    strict_need(result["ledger"], {"filename": LEDGER, "object_sha256": object_sha(ledger), "sha256": LEDGER_SHA, "size": LEDGER_SIZE}, "ledger/result binding")


def attacks(ledger: dict[str, Any], result: dict[str, Any]) -> list[dict[str, Any]]:
    mutations: list[tuple[str, str, tuple[str, ...], Any]] = [
        ("ledger G2a count", "ledger", ("exact_census", "G2a_members"), 38_625),
        ("ledger G2b refs", "ledger", ("exact_census", "G2b_references"), 76_832),
        ("ledger G2b distinct", "ledger", ("exact_census", "G2b_distinct_members"), 76_848),
        ("ledger graph gap", "ledger", ("semantic_gaps", "source_free_graph_definition_pending"), 0),
        ("ledger incidence gap", "ledger", ("semantic_gaps", "physical_incidence_rows_pending"), 0),
        ("ledger support gap", "ledger", ("semantic_gaps", "distinct_member_full_support_equalities_pending"), 0),
        ("ledger representation gap", "ledger", ("semantic_gaps", "representation_pullback_theorems_pending"), 0),
        ("ledger support credit", "ledger", ("formal_credit", "normalized_support"), 1),
        ("ledger incidence credit", "ledger", ("formal_credit", "physical_incidence"), 1),
        ("ledger bool alias credit", "ledger", ("formal_credit", "physical_incidence"), False),
        ("ledger bool alias false gap", "ledger", ("semantic_gaps", "unresolved_semantic_gap_zero"), 0),
        ("ledger pin count bool alias", "ledger", ("snapshot", "pins", "0", "exact_size"), True),
        ("ledger table count bool alias", "ledger", ("ordered_table_commitments", "correction", "row_count"), True),
        ("ledger resource cap bool alias", "ledger", ("resource_boundary", "canonical_selected_row_cap_bytes"), True),
        ("ledger outer envelope", "ledger", ("strict_nonclaims", "outer_envelope_is_full_support"), True),
        ("ledger K1 theorem", "ledger", ("strict_nonclaims", "K1_checker_is_theorem_instance"), True),
        ("ledger R300E identity", "ledger", ("strict_nonclaims", "R300E_component_edge_is_occurrence_identity"), True),
        ("ledger R294 G2 cover", "ledger", ("strict_nonclaims", "R294_stage_A_registry_covers_G2"), True),
        ("ledger B1A open", "ledger", ("downstream_state", "B1A"), "GO"),
        ("ledger side order", "ledger", ("ordered_table_commitments", "side", "row_count"), 76_832),
        ("result formal credit false alias", "result", ("formal_credit", "physical_incidence"), False),
        ("result exact census bool alias", "result", ("exact_census", "G2a_members"), True),
        ("result integer gap false alias", "result", ("semantic_gaps", "source_free_graph_definition_pending"), False),
        ("result false gap integer alias", "result", ("semantic_gaps", "unresolved_semantic_gap_zero"), 0),
        ("result ledger size bool alias", "result", ("ledger", "size"), True),
    ]
    rows: list[dict[str, Any]] = []
    for name, target, path, value in mutations:
        candidate_ledger = copy.deepcopy(ledger)
        candidate_result = copy.deepcopy(result)
        node: Any = candidate_ledger if target == "ledger" else candidate_result
        for part in path[:-1]:
            if type(node) is list:
                node = node[int(part)]
            else:
                node = node[part]
        node[path[-1]] = value
        rejected = False
        try:
            validate(candidate_ledger, candidate_result)
        except (Blocked, KeyError, TypeError, ValueError):
            rejected = True
        need(rejected, "mutation rejected:" + name)
        rows.append({"name": name, "rejected": True})
    return rows


def safe_publish(name: str, payload: bytes) -> None:
    need(name == os.path.basename(name), "output basename")
    output_real = HERE.resolve()
    scratch = Path(tempfile.mkdtemp(prefix="cm2-k2g0-verify-", dir="/tmp"))
    try:
        scratch_real = scratch.resolve()
        need(output_real not in (scratch_real, *scratch_real.parents), "scratch outside deliverables")
        staged = scratch / name
        with staged.open("xb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        outfd = os.open(HERE, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        try:
            try:
                existing_stat = os.stat(name, dir_fd=outfd, follow_symlinks=False)
            except FileNotFoundError:
                existing_stat = None
            if existing_stat is not None:
                need(stat.S_ISREG(existing_stat.st_mode) and existing_stat.st_nlink == 1, "existing output regular/nlink:" + name)
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=outfd)
                try:
                    chunks: list[bytes] = []
                    while True:
                        chunk = os.read(fd, 1_048_576)
                        if not chunk:
                            break
                        chunks.append(chunk)
                    existing = b"".join(chunks)
                finally:
                    os.close(fd)
                if existing != payload:
                    need(name in {VERIFICATION, REPORT, COLD, MANIFEST}, "refuse unrelated overwrite:" + name)
                    os.replace(staged, name, dst_dir_fd=outfd)
                    os.fsync(outfd)
            else:
                os.rename(staged, name, dst_dir_fd=outfd)
                os.fsync(outfd)
        finally:
            os.close(outfd)
    finally:
        shutil.rmtree(scratch)


def self_bytes() -> tuple[int, str]:
    raw = Path(__file__).read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def report_text(verification: dict[str, Any]) -> str:
    return f"""# CM2 Round306B1AF4K2G0 — G2 semantic authority frontier

## Verdict

`{STATUS}`.  Exact construction identity/order is frozen, but full-support
theorem credit remains zero.  G2a is exactly `38,624`; G2b is `76,848`
references to `76,832` distinct members.  Together they backbind exactly
`115,456` B0 members and currently supply `115,456` mechanical representation
index candidates, not a proved representation cover.

## Authority boundary

- B1G0/G1/B0: engineering-exact joins and ordered commitments only.
- R245/R248: input-bound local quotient geometry only; it does not transfer to
  a source-free graph definition or full-support equality.
- R300E: exactly `12,992` one-sided R248 sheet-owner component edges; not
  occurrence identity and not support.
- R302A/R302C: `32 + 25,336` attachment exclusions; not support nonexistence.
- K1: independently receipt-checked checker mechanics, but no G2 certificate
  instances and no independent mathematical implementation.
- R288/R294: open-3D Stage-A identity context; no G2 lower-stratum cover.

The exact remaining gaps are `38,624` graph definitions, `115,472` physical
incidence rows, `115,456` distinct full-support equalities and `115,456`
representation pullbacks.  The B1G0 explicit gap ledger has `154,096` rows.

## Verification

The independent verifier pins `{len(PINS) + len(PRIMARY)}` files, performs two
same-FD SHA passes plus a final full SHA/path revalidation, rechecks nine
upstream manifests, validates all six ordered-table commitments, rejects
`{verification['attack_summary']['rejected']}/{verification['attack_summary']['total']}`
semantic/type overclaims, and enforces the post-decode 8 MiB canonical cap.

It does not independently reparse/rederive the heavy B1G0 rows; it verifies
their sealed file and ordered commitments.  Therefore its scope is a strict
authority-frontier receipt, not a theorem replay.  B1A remains BLOCKED, B2 is
not authorized by this frontier, D02 remains BLOCKED, and CM2 remains
NO-GO_FOR_CLAIM.
"""


def cold_text() -> str:
    return f"""# K2G0 cold replay

Two seed-distinct cacheless verifier commands are required and deterministic:

```text
PYTHONHASHSEED=3064201 python -I -B {Path(__file__).name} --verify --write
PYTHONHASHSEED=3064999 python -I -B {Path(__file__).name} --verify --no-write
```

The second run must accept only byte-identical verification/report/cold/manifest
artifacts.  Runtime and maximum RSS are execution observations, not theorem
claims.  Availability/resource exhaustion cannot mint credit.
"""


def manifest_bytes(names: list[str]) -> bytes:
    rows: list[str] = []
    for name in names:
        path = HERE / name
        before = os.stat(path, follow_symlinks=False)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "manifest target regular/nlink:" + name)
        raw = path.read_bytes()
        after = os.stat(path, follow_symlinks=False)
        need(file_identity(before) == file_identity(after), "manifest target stable:" + name)
        rows.append(hashlib.sha256(raw).hexdigest() + "  " + name)
    return ("\n".join(rows) + "\n").encode("ascii")


def verify(write: bool) -> dict[str, Any]:
    verifier_size, verifier_sha = self_bytes()
    with Snapshot() as snap:
        snap.check_manifests()
        ledger_raw = snap.bytes("LEDGER")
        result_raw = snap.bytes("RESULT")
        ledger = decode(ledger_raw, "ledger")
        result = decode(result_raw, "result")
        need(ledger_raw == canonical(ledger) + b"\n", "canonical ledger bytes")
        need(result_raw == canonical(result) + b"\n", "canonical result bytes")
        validate(ledger, result)
        attack_rows = attacks(ledger, result)
        snap.final_revalidate()

    verification: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "verifier": {"filename": Path(__file__).name, "size": verifier_size, "sha256": verifier_sha},
        "targets": {"producer": {"filename": PRODUCER, "size": PRODUCER_SIZE, "sha256": PRODUCER_SHA}, "ledger": {"filename": LEDGER, "size": LEDGER_SIZE, "sha256": LEDGER_SHA}, "result": {"filename": RESULT, "size": RESULT_SIZE, "sha256": RESULT_SHA}},
        "snapshot": {"pin_count": len(PINS) + len(PRIMARY), "input_bytes": sum(row[2] for row in PINS) + PRODUCER_SIZE + LEDGER_SIZE + RESULT_SIZE, "two_pass_same_fd_all": True, "final_sha_and_path_revalidated_all": True, "manifest_groups_rechecked": len(MANIFESTS), "symlink_hardlink_TOCTOU_fail_closed": True},
        "exact_census": ledger["exact_census"],
        "semantic_gaps": ledger["semantic_gaps"],
        "ordered_table_count": len(EXPECTED_TABLES),
        "authority_class_count": len(ledger["authority_frontier"]),
        "attack_summary": {"total": len(attack_rows), "rejected": sum(row["rejected"] for row in attack_rows), "rows": attack_rows},
        "scope": {"independent_byte_manifest_and_frontier_validation": True, "heavy_B1G0_rows_independently_reparsed_here": False, "independent_mathematical_theorem_implementation": False, "mints_formal_credit": False},
        "formal_credit": ledger["formal_credit"],
        "downstream_state": ledger["downstream_state"],
        "resource_boundary": {"canonical_selected_row_cap_bytes": ROW_CAP, "post_decode_cap_enforced": True, "scratch_root": "/tmp", "scratch_resolved_outside_deliverables": True, "bounded_memory_claim": False, "resource_exhaustion_mints_credit": False},
    }
    verification["object_sha256"] = object_sha(verification)
    verification_bytes = canonical(verification) + b"\n"
    need(len(verification_bytes) <= ROW_CAP, "verification cap")
    report = report_text(verification).encode("utf-8")
    cold = cold_text().encode("utf-8")
    if write:
        safe_publish(VERIFICATION, verification_bytes)
        safe_publish(REPORT, report)
        safe_publish(COLD, cold)
        safe_publish(MANIFEST, manifest_bytes([PRODUCER, LEDGER, RESULT, Path(__file__).name, VERIFICATION, REPORT, COLD]))
    else:
        expected = {VERIFICATION: verification_bytes, REPORT: report, COLD: cold}
        for name, payload in expected.items():
            path = HERE / name
            st = os.stat(path, follow_symlinks=False)
            need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, "existing receipt regular/nlink:" + name)
            need(path.read_bytes() == payload, "existing receipt exact bytes:" + name)
        need((HERE / MANIFEST).read_bytes() == manifest_bytes([PRODUCER, LEDGER, RESULT, Path(__file__).name, VERIFICATION, REPORT, COLD]), "manifest exact bytes")
    return verification


def self_test() -> None:
    need(len(PINS) == 42, "pin census")
    need(len({row[0] for row in PINS}) == len(PINS), "unique labels")
    need(len({row[1] for row in PINS}) == len(PINS), "unique filenames")
    need(sum((38_624, 76_832)) == 115_456, "member census")
    need(38_624 + 115_472 == 154_096, "gap census")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    need(args.self_test != args.verify, "choose self-test or verify")
    if args.self_test:
        need(not args.write and not args.no_write, "self-test inert")
        self_test()
        print("PASS_K2G0_INDEPENDENT_VERIFIER_SELF_TEST")
    else:
        need(args.write != args.no_write, "choose write or no-write")
        document = verify(args.write)
        print(canonical({"status": document["status"], "object_sha256": document["object_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Blocked as exc:
        print("BLOCKED:" + str(exc), file=os.sys.stderr)
        raise SystemExit(2)
