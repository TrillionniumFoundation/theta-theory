#!/usr/bin/env python3
"""Freeze the exact G2 construction/semantic authority frontier.

This producer is deliberately zero-credit.  It pins the complete inputs used
to classify G2a/G2b authority, preserves the already sealed B1G0 ordered-table
commitments, and records the exact semantic gaps.  It does not import or
execute any upstream producer/checker and it does not turn local quotient
contacts, occurrence attachment, an outer envelope, or an inner witness into
normalized full support.
"""

from __future__ import annotations

import argparse
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


HERE: Final = Path(__file__).parent
SCHEMA: Final = "cm2.round306b1af4k2g0.source-g-g2-semantic-authority-frontier.v1"
STATUS: Final = "PASS_EXACT_G2_AUTHORITY_FRONTIER__SEMANTIC_GAPS_NONZERO__ZERO_FORMAL_CREDIT"
ROW_CAP: Final = 8_388_608
LEDGER_NAME: Final = "cm2_round306b1af4k2g0_source_g_g2_semantic_authority_frontier_ledger.json"
RESULT_NAME: Final = "cm2_round306b1af4k2g0_source_g_g2_semantic_authority_frontier_result.json"


# label, family, filename, exact size, SHA-256, role
PINS: Final = (
    ("AF2", "ANCHOR", "cm2_round306b1af2_source_g_primitive_support_source_partition_freeze_contract.py", 52_538, "a91578a8bef1c4a72f940f7ebc71aea4c0ebc1ddac08ddbb3889a2da6cdd00f5", "SIX_FAMILY_PARTITION_ANCHOR"),
    ("G1", "ANCHOR", "cm2_round306b1af4g1_source_g_g2_exact_join_preflight.py", 92_288, "fce556387520b6e27af9ba5d6e816e91325a629750855af0fffae36dfdba765d", "ZERO_CREDIT_EXACT_JOIN_REPLAY"),
    ("B0_MEMBER", "B0", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_member_support_source_index.json.gz", 162_499_140, "c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af", "FROZEN_MEMBER_SOURCE_INDEX"),
    ("B1G0_PRODUCER", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze.py", 90_721, "97f1d0736a616071dbb0dba3bf533e3fae96091fc6b165395436216bb69c9321", "INERT_PRODUCER_BYTES"),
    ("B1G0_VERIFIER", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_promotion_verifier.py", 128_011, "47d642bfd90c8f8040a7de97df88788f2295e60b50ad7c72bb8ae2e85d89004b", "INDEPENDENT_VERIFIER_BYTES"),
    ("B1G0_GRAPH", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0", "ORDERED_GRAPH_INVENTORY"),
    ("B1G0_SHEET", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3", "ORDERED_G2A_JOIN"),
    ("B1G0_SIDE", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1", "ORDERED_G2B_REF_JOIN"),
    ("B1G0_CORRECTION", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_r264_correction_disposition.json.gz", 140_958, "834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a", "ORDERED_R264_CORRECTIONS"),
    ("B1G0_BACKBIND", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz", 32_731_854, "79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b", "ORDERED_DISTINCT_MEMBER_BACKBINDING"),
    ("B1G0_GAP", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_gap.json.gz", 23_240_985, "2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809", "ORDERED_EXPLICIT_SEMANTIC_GAPS"),
    ("B1G0_RESULT", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json", 5_006, "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e", "RESULT"),
    ("B1G0_VERIFICATION", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_verification.json", 11_575, "65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a", "VERIFICATION_RECEIPT"),
    ("B1G0_MANIFEST", "B1G0", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_manifest.sha256", 1_959, "6f79385d0eed9c13bcc1501c8a189e947f1194d28e198290e6a4b2b2a376a9b8", "MANIFEST"),
    ("R245_CERT", "R245", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_certificate.json", 20_683_081, "c76662f7cb068127f3612a3655ae720662eead9b9210b5757d771693149883c1", "LOCAL_GRAPH_SHEET_SIDE_QUOTIENT_AUTHORITY"),
    ("R245_VERIFICATION", "R245", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_verification.json", 1_016, "7b116fce6abfad827a19da4e6637bac50c784c0e53b84e9bfd9567abb35bef14", "VERIFICATION_RECEIPT"),
    ("R245_MANIFEST", "R245", "cm2_round245_source_g_retained_graph_mixed_sheet_quotient_manifest.sha256", 897, "1aff29f3a42b618ca85e5a1d3c537307e32326f8d5092b82d4253a5bf6e1c4ac", "MANIFEST"),
    ("R248_CERT", "R248", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311", "LOCAL_WALL_SHEET_SIDE_QUOTIENT_AUTHORITY"),
    ("R248_VERIFICATION", "R248", "cm2_round248_source_g_wall_finite_key_retained_quotient_verification.json", 1_028, "5e20ada49b5bca2e7ebaf6b78835c4ca1a6051e24960b7d00b3ae9d596f11a10", "VERIFICATION_RECEIPT"),
    ("R248_MANIFEST", "R248", "cm2_round248_source_g_wall_finite_key_retained_quotient_manifest.sha256", 885, "b1ddedd01041e71b5c12fa4989726815c8685e6df77f54d9dbddda64aaf89e07", "MANIFEST"),
    ("R300E_WITNESS", "R300E", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_witness_ledger.json.gz", 17_175_071, "69f480da55e917b7b75bfe1efa823a9228d9b563f6f3aabd4e2a364c9e50eb9f", "NARROW_INPUT_BOUND_OWNER_EDGE_WITNESS"),
    ("R300E_RESULT", "R300E", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_result.json", 5_168, "193c74535431789ba4fcdad598487916712d6ad1c04f191a083076e4a05f7e3e", "RESULT"),
    ("R300E_VERIFICATION", "R300E", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_verification.json", 2_153, "313008d59a2d67b5ce4b7c8d62cd68a26a855a65c34396b5ae0176dda2096d4a", "VERIFICATION_RECEIPT"),
    ("R300E_MANIFEST", "R300E", "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_promotion_manifest.sha256", 1_571, "4e6c4eec1af04a907285d41395aeef63e911b3b5486db91b33a95fa62e45177a", "MANIFEST"),
    ("R302A_LEDGER", "R302A", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_ledger.json.gz", 14_522, "f71feba87a6ae9e8524c2d86c7489ffe19c71dd08c9ebec75a90702f0e81b558", "DOUBLE_ENDPOINT_ATTACHMENT_EXCLUSION"),
    ("R302A_RESULT", "R302A", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_result.json", 4_897, "5fddf94222712385684c117d220a165934450a80a318ae3d26e26a81ef3cc160", "RESULT"),
    ("R302A_VERIFICATION", "R302A", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_verification.json", 1_737, "28214c45a373365587087c21ee51c0e1eec7c4195afccb356b5b36b8ccbaeb71", "VERIFICATION_RECEIPT"),
    ("R302A_MANIFEST", "R302A", "cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_manifest.sha256", 1_358, "b4a53c485da9fd889e3a9194c7e770f2a32eb14027e8bfd0f7c2370eab9eca71", "MANIFEST"),
    ("R302C_LEDGER", "R302C", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_disposition_ledger.json.gz", 20_435_193, "c326d50f62a427c71e6f41b188b00b08baf6db7bf535ba082f23678239eebba6", "RESIDUAL_SINGLE_ENDPOINT_ATTACHMENT_EXCLUSION"),
    ("R302C_RESULT", "R302C", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_result.json", 8_144, "d371d3d6ce01b0779717dc817216204cf0c142d0b95caf42ede3d1d243d5daa2", "RESULT"),
    ("R302C_VERIFICATION", "R302C", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_verification.json", 1_945, "da663f790488e85c8973bd62c8af269abfd19e3e7ee19aa3f2335091a9dd81d9", "VERIFICATION_RECEIPT"),
    ("R302C_MANIFEST", "R302C", "cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_manifest.sha256", 1_275, "42fa1ad2266e3bef38f034489085c325d656ff94ddf2f9710c7c68ab90646dc1", "MANIFEST"),
    ("K1_KERNEL", "K1", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py", 68_346, "17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae", "ZERO_CREDIT_CHECKER_ONLY"),
    ("K1_RESULT", "K1", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_result.json", 2_787, "e9ff89a5d51f5e79864f10dc34dd4b5f12887c029f65c2196c60f50bd4c77b21", "ZERO_CREDIT_RESULT"),
    ("K1_VERIFICATION", "K1", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_verification.json", 3_777, "4d1d5d20d7f61906262486582b9cb407935f6b883989165b7a7938994fedf0d8", "VERIFICATION_RECEIPT"),
    ("K1_MANIFEST", "K1", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_manifest.sha256", 933, "07a3f12e75c43fd459dfd4e86c918b349c09226c94735b1a6d16432f1caca939", "MANIFEST"),
    ("R288_RESULT", "R288", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_result.json", 8_981, "9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569", "OPEN_3D_IDENTITY_NONCOVERAGE_CONTEXT"),
    ("R288_VERIFICATION", "R288", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_verification.json", 9_874, "f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23", "VERIFICATION_RECEIPT"),
    ("R288_MANIFEST", "R288", "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_manifest.sha256", 1_203, "c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb", "MANIFEST"),
    ("R294_RESULT", "R294", "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json", 6_958, "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626", "STAGE_A_REGISTRY_NONCOVERAGE_CONTEXT"),
    ("R294_VERIFICATION", "R294", "cm2_round294_source_g_occurrence_registry_atomic_promotion_verification.json", 6_529, "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245", "VERIFICATION_RECEIPT"),
    ("R294_MANIFEST", "R294", "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256", 1_275, "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131", "MANIFEST"),
)

TABLES: Final = {
    "graph": {"source_label": "B1G0_GRAPH", "path": ["graph_source_inventory_rows"], "row_count": 38_624, "ledger_sha256": "a684dad14281e44c9dc02a0f825af661ef152f86a436c827fc0b113d25b4d6a0", "rows_sha256": "beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f", "row_ids_sha256": "982ee86845f92368cee72b74c52e401eecfb6dd225a4b198910b89ce34a8a7dc", "row_hashes_sha256": "7fde3bb652a469eb3b04fe31a80c365d010d914700348954c5d917ac1162dace"},
    "sheet": {"source_label": "B1G0_SHEET", "path": ["graph_sheet_join_rows"], "row_count": 38_624, "ledger_sha256": "3686f3b90a77195dbecd08750707a32f98e07f9fdff5f59d57f09c1178a48fda", "rows_sha256": "9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f", "row_ids_sha256": "b36ca314b15b8b8297dfeda9cb4fe37360ff20339e7603a6388ac172cfb87300", "row_hashes_sha256": "a3c606a9ba302ced5593d941529946729da5d160a32384ca37060b20011a01f5"},
    "side": {"source_label": "B1G0_SIDE", "path": ["graph_side_join_rows"], "row_count": 76_848, "ledger_sha256": "108bdcbe1c124de15d8f48f82a3cdb7aa545f6f61294be34e3e5b07979d6670e", "rows_sha256": "43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2", "row_ids_sha256": "9e2a2c015372aa22e5f2cfa1f11ae268496831b3118da5bd5087fc6d7f403f53", "row_hashes_sha256": "2090d073d45f0097df68a60b36085786de0db51d76219b562734465bbf6daff6"},
    "correction": {"source_label": "B1G0_CORRECTION", "path": ["r264_correction_disposition_rows"], "row_count": 400, "ledger_sha256": "a4af6f87737028981be9dccae9c2c28236408aa1f112f507418b6e4516eeb671", "rows_sha256": "a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67", "row_ids_sha256": "b3dec2b9ef34fd5ebc3701201593ca90146f6d6150e5b593284a2a974a1d8caf", "row_hashes_sha256": "f172394acdc909f6bc58f59fd1f361c4a4c5b00d06b2a8e8369b7638a6e6c592"},
    "member": {"source_label": "B1G0_BACKBIND", "path": ["b0_member_backbinding_rows"], "row_count": 115_456, "ledger_sha256": "65493ba72be6047b7c1c4ea64045460ad8160ab05440d02204393d3697a4d541", "rows_sha256": "35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6", "row_ids_sha256": "ff6c659209636eec5235a375e8f8ba1cd5bf69c39df6630e6dfaeb95b0945d72", "row_hashes_sha256": "88026547b175b4ee968f738fe1276163d364b4482d164dbc2e84377039088eae"},
    "gap": {"source_label": "B1G0_GAP", "path": ["gap_rows"], "row_count": 154_096, "ledger_sha256": "5324319ce7b3f90f67b3e12af6848f851008fd52c7cbd7c8d433cd0652c52f9e", "rows_sha256": "d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b", "row_ids_sha256": "f1c3bf0bb9991f1298a3bc8ce90d55871122ef81b679f32fca21b81087ee1421", "row_hashes_sha256": "ca9e836b8ca114ba2843a9196748128b6194adb3bd801bb9a28dfff44d28af35"},
}

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


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def dup_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_float(token: str) -> Any:
    raise Blocked("nonintegral JSON number:" + token)


def decode(raw: bytes, label: str) -> dict[str, Any]:
    need(len(raw) <= ROW_CAP, "selected document cap:" + label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=dup_reject,
                           parse_float=reject_float,
                           parse_constant=lambda token: (_ for _ in ()).throw(Blocked("constant:" + token)))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Blocked("JSON decode:" + label) from exc
    need(type(value) is dict, "JSON root object:" + label)
    need(len(canonical(value)) <= ROW_CAP, "final canonical selected document cap:" + label)
    return value


def file_identity(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns)


def dir_identity(st: os.stat_result) -> tuple[int, int, int]:
    return (st.st_dev, st.st_ino, st.st_mode)


class Snapshot:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dirstat: os.stat_result | None = None
        self.fds: dict[str, int] = {}
        self.initial: dict[str, tuple[str, str]] = {}
        self.final: dict[str, str] = {}
        self.by_label = {row[0]: row for row in PINS}

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
        need(stat.S_ISDIR(before.st_mode), "deliverables directory")
        self.dirfd = os.open(HERE, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        held = os.fstat(self.dirfd)
        need(dir_identity(before) == dir_identity(held), "directory open race")
        self.dirstat = held
        try:
            for label, _family, filename, size, sha256, _role in PINS:
                need(filename == os.path.basename(filename), "basename:" + label)
                path = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(path.st_mode) and path.st_nlink == 1, "regular nlink=1:" + label)
                need(path.st_size == size, "size:" + label)
                fd = os.open(filename, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd)
                need(file_identity(path) == file_identity(opened), "open race:" + label)
                self.fds[label] = fd
                h1, h2 = self._hash(fd), self._hash(fd)
                need(h1 == h2 == sha256, "two-pass SHA:" + label)
                need(file_identity(opened) == file_identity(os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)), "post-hash path:" + label)
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
            need(total <= ROW_CAP, "selected bytes cap:" + label)
            out.append(chunk)

    def check_manifests(self) -> None:
        for manifest_label, required in MANIFESTS.items():
            text = self.bytes(manifest_label).decode("ascii")
            rows: dict[str, str] = {}
            for line in text.splitlines():
                if not line.strip():
                    continue
                parts = line.split()
                need(len(parts) == 2 and len(parts[0]) == 64, "manifest grammar:" + manifest_label)
                basename = os.path.basename(parts[1])
                need(basename not in rows, "manifest duplicate basename:" + basename)
                rows[basename] = parts[0]
            for label in required:
                pin = self.by_label[label]
                need(rows.get(pin[2]) == pin[4], "manifest binding:" + manifest_label + ":" + label)

    def final_revalidate(self) -> None:
        for label, _family, filename, _size, sha256, _role in PINS:
            final = self._hash(self.fds[label])
            need(final == sha256, "final SHA:" + label)
            held = os.fstat(self.fds[label])
            path = os.stat(filename, dir_fd=self.dirfd, follow_symlinks=False)
            need(file_identity(held) == file_identity(path), "final path/FD:" + label)
            need(stat.S_ISREG(held.st_mode) and held.st_nlink == 1, "final regular/nlink:" + label)
            self.final[label] = final
        need(self.dirstat is not None, "directory snapshot")
        need(dir_identity(self.dirstat) == dir_identity(os.fstat(self.dirfd)) == dir_identity(os.stat(HERE, follow_symlinks=False)), "final directory identity")

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


def assert_source_documents(snap: Snapshot) -> None:
    b1 = decode(snap.bytes("B1G0_RESULT"), "B1G0_RESULT")
    need(b1["audit"] == {
        "R264_correction_count": 400,
        "all_output_formal_credit_zero": True,
        "distinct_B0_member_backbinding_count": 115_456,
        "gap_count": 154_096,
        "graph_count": 38_624,
        "graph_family_histogram": {"R235_SINGLE_ENDPOINT_GRAPH": 38_328, "R236_DOUBLE_ENDPOINT_GRAPH": 32, "R242_UNIQUE_TRANSITION_GRAPH": 264},
        "graph_sheet_join_count": 38_624,
        "graph_side_join_count": 76_848,
        "incidence_family_histogram": {"R235_SINGLE_ENDPOINT_GRAPH:SHEET": 38_328, "R235_SINGLE_ENDPOINT_GRAPH:SIDE": 76_256, "R236_DOUBLE_ENDPOINT_GRAPH:SHEET": 32, "R236_DOUBLE_ENDPOINT_GRAPH:SIDE": 64, "R242_UNIQUE_TRANSITION_GRAPH:SHEET": 264, "R242_UNIQUE_TRANSITION_GRAPH:SIDE": 528},
        "official_key_used_as_join_or_routing_filter": False,
        "physical_incidence_count": 115_472,
        "physical_incidence_theorem_complete": False,
        "source_free_graph_definition_complete": False,
    }, "B1G0 exact audit")
    need(b1["strict_boundary"]["formal_full_support_credit"] == 0, "B1G0 zero support")
    need(b1["strict_boundary"]["formal_physical_incidence_credit"] == 0, "B1G0 zero incidence")
    for key, spec in TABLES.items():
        source = b1["output_ledgers"][key]
        need(source["row_count"] == spec["row_count"], "B1G0 table count:" + key)
        for field in ("ledger_sha256", "rows_sha256", "row_ids_sha256", "row_hashes_sha256"):
            need(source[field] == spec[field], "B1G0 table commitment:" + key + ":" + field)

    r300e = decode(snap.bytes("R300E_RESULT"), "R300E_RESULT")
    need(r300e["source_audit"]["distinct_R248_matched_sheet_count"] == 12_992, "R300E sheet count")
    need(r300e["scope_contract"]["edge_means_component_connectivity_not_occurrence_identity"] is True, "R300E narrow edge")
    need(r300e["scope_contract"]["mere_two_sided_graph_incidence_is_not_an_edge"] is True, "R300E incidence nontransfer")
    need(all(value in (0, None) for value in r300e["strict_nonpromotion"].values()), "R300E nonpromotion")

    r302a = decode(snap.bytes("R302A_RESULT"), "R302A_RESULT")
    need(r302a["complete_frontier_census"]["Round248_double_endpoint_sheet_count"] == 32, "R302A 32")
    need(r302a["complete_frontier_census"]["unresolved_sheet_count"] == 0, "R302A disposition complete")
    need(all(value == 0 for value in r302a["formal_credit_transition"].values()), "R302A zero credit")

    r302c = decode(snap.bytes("R302C_RESULT"), "R302C_RESULT")
    partition = r302c["sealed_attachment_disposition_partition"]
    need(partition["Round300E_positive_single_endpoint_sheet_count"] == 12_992, "R302C positive")
    need(partition["Round302A_excluded_double_endpoint_sheet_count"] == 32, "R302C double")
    need(partition["Round302C_excluded_single_endpoint_sheet_count"] == 25_336, "R302C residual")
    need(partition["complete_R248_sheet_count"] == 38_360, "R302C total")

    k1 = decode(snap.bytes("K1_RESULT"), "K1_RESULT")
    need(k1["decision"] == "GO_ONLY_ZERO_CREDIT", "K1 checker only")
    need(k1["method_boundary"]["independent_mathematical_implementation"] is False, "K1 no independent math")
    need(all(value == 0 for value in k1["formal_credit"].values()), "K1 zero credit")

    r294 = decode(snap.bytes("R294_RESULT"), "R294_RESULT")
    need(r294["scope_contract"]["final_exhaustive_all_stratum_registry_claimed"] is False, "R294 not exhaustive")
    need(r294["scope_contract"]["registry_scope"] == "CURRENT_FORMAL_STAGE_A_OPEN_3D_PLUS_R287_REFINED_FRONTIER", "R294 stage A scope")


def pin_rows() -> list[dict[str, Any]]:
    return [{"label": label, "family": family, "filename": filename, "exact_size": size,
             "sha256": sha256, "role": role, "authority_priority": {
                 "ANCHOR": 1, "B0": 2, "B1G0": 3, "R245": 4, "R248": 4,
                 "R300E": 5, "R302A": 6, "R302C": 6, "K1": 7,
                 "R288": 8, "R294": 8,
             }[family]} for label, family, filename, size, sha256, role in PINS]


def expected_ledger(producer_size: int, producer_sha: str) -> dict[str, Any]:
    document: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "producer": {"filename": Path(__file__).name, "size": producer_size, "sha256": producer_sha},
        "snapshot": {"pin_count": len(PINS), "total_bytes": sum(row[3] for row in PINS), "pins": pin_rows(), "held_fd_two_pass_and_final_sha": True, "final_path_revalidated": True, "symlink_hardlink_TOCTOU_fail_closed": True},
        "ordered_table_commitments": TABLES,
        "exact_census": {
            "G2a_members": 38_624,
            "G2a_R245": 264,
            "G2a_R248": 38_360,
            "G2b_references": 76_848,
            "G2b_distinct_members": 76_832,
            "G2b_R245_references": 528,
            "G2b_R245_distinct_members": 528,
            "G2b_R248_references": 76_320,
            "G2b_R248_distinct_members": 76_304,
            "G2_distinct_members": 115_456,
            "G2_representations_current_exact_index_candidate": 115_456,
            "duplicate_side_reference_excess": 16,
        },
        "authority_frontier": [
            {"rank": 1, "source": "B1G0/G1/B0", "status": "ENGINEERING_EXACT_IDENTITY_AND_ORDER_ONLY", "covers": "38,624 graphs; 38,624 G2a joins; 76,848 G2b refs -> 76,832 distinct members; 115,456 B0 backbindings", "does_not_cover": "source-free graph definition, physical incidence, normalized support, representation pullback theorem"},
            {"rank": 2, "source": "R245", "status": "LOCAL_INPUT_BOUND_PHYSICAL_QUOTIENT_AUTHORITY", "covers": "264 transition sheets, 528 side members and their local owner/shadow corridor/quotient contacts", "does_not_cover": "the later B1G0 source-free graph definition or full-support equality for those members"},
            {"rank": 2, "source": "R248", "status": "LOCAL_INPUT_BOUND_WALL_QUOTIENT_AUTHORITY", "covers": "38,360 half-open wall sheets; 76,320 side refs -> 76,304 distinct side members; local wall-root contacts/ownership", "does_not_cover": "all graph-to-sheet/side incidence or member full-support equality"},
            {"rank": 3, "source": "R300E", "status": "NARROW_INPUT_BOUND_COMPONENT_CONNECTIVITY_AUTHORITY", "covers": "12,992 R248 sheet -> event-absent owner edges", "does_not_cover": "occurrence identity, side support, all 38,360 sheets, graph incidence, normalized support"},
            {"rank": 4, "source": "R302A/R302C", "status": "ATTACHMENT_DISPOSITION_EXCLUSION_ONLY", "covers": "32 double-endpoint plus 25,336 residual single-endpoint R248 sheet attachment exclusions", "does_not_cover": "support nonexistence, support equality, physical incidence or maximality"},
            {"rank": 5, "source": "K1", "status": "CHECKER_FOUNDATION_ZERO_CREDIT", "covers": "input-bound certificate checking grammar and mechanics", "does_not_cover": "any G2 theorem instance; no independent mathematical implementation"},
            {"rank": 6, "source": "R288/R294", "status": "OPEN_3D_STAGE_A_IDENTITY_CONTEXT_NOT_G2_COVER", "covers": "preserved/R2/R292 occurrence identity and bindings", "does_not_cover": "G2a/G2b lower-dimensional full support or their representation pullbacks"},
        ],
        "semantic_gaps": {
            "source_free_graph_definition_pending": 38_624,
            "graph_sheet_physical_incidence_pending": 38_624,
            "graph_side_physical_incidence_reference_pending": 76_848,
            "physical_incidence_rows_pending": 115_472,
            "distinct_member_full_support_equalities_pending": 115_456,
            "representation_pullback_theorems_pending": 115_456,
            "B1G0_explicit_gap_rows": 154_096,
            "unresolved_semantic_gap_zero": False,
        },
        "strict_nonclaims": {
            "outer_envelope_is_full_support": False,
            "inner_witness_is_full_support": False,
            "graph_occurrence_is_full_support": False,
            "K1_checker_is_theorem_instance": False,
            "local_quotient_contact_transfers_to_global_support": False,
            "R300E_component_edge_is_occurrence_identity": False,
            "R302_attachment_exclusion_is_support_nonexistence": False,
            "R294_stage_A_registry_covers_G2": False,
            "normalized_support_constructed": False,
            "representation_cover_constructed": False,
        },
        "formal_credit": {"graph_definition": 0, "physical_incidence": 0, "normalized_support": 0, "representation_cover": 0, "B1A": 0, "transition": 0, "pair_routing": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "D02": 0, "CM2": 0},
        "downstream_state": {"B1A": "BLOCKED", "B2": "NOT_AUTHORIZED_BY_THIS_FRONTIER", "D02": "BLOCKED", "CM2": "NO-GO_FOR_CLAIM"},
        "resource_boundary": {"canonical_selected_row_cap_bytes": ROW_CAP, "final_canonical_cap_checked_after_successful_decode": True, "temporary_directory": "/tmp", "temporary_directory_resolved_outside_deliverables": True, "bounded_memory_claim": False, "resource_exhaustion_mints_credit": False},
    }
    need(len(canonical(document)) <= ROW_CAP, "final canonical ledger cap")
    return document


def hash_self() -> tuple[int, str]:
    path = Path(__file__)
    raw = path.read_bytes()
    return len(raw), hashlib.sha256(raw).hexdigest()


def publish(name: str, payload: bytes) -> None:
    need(name == os.path.basename(name), "output basename")
    output_real = HERE.resolve()
    scratch = Path(tempfile.mkdtemp(prefix="cm2-k2g0-", dir="/tmp"))
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
                before = os.stat(name, dir_fd=outfd, follow_symlinks=False)
            except FileNotFoundError:
                before = None
            if before is not None:
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "existing output regular/nlink")
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=outfd)
                try:
                    existing = b""
                    while True:
                        chunk = os.read(fd, 1_048_576)
                        if not chunk:
                            break
                        existing += chunk
                    need(existing == payload, "existing output differs:" + name)
                finally:
                    os.close(fd)
            else:
                os.rename(staged, name, dst_dir_fd=outfd)
                os.fsync(outfd)
        finally:
            os.close(outfd)
    finally:
        shutil.rmtree(scratch)


def replay(write: bool) -> tuple[dict[str, Any], dict[str, Any]]:
    producer_size, producer_sha = hash_self()
    with Snapshot() as snap:
        snap.check_manifests()
        assert_source_documents(snap)
        ledger = expected_ledger(producer_size, producer_sha)
        snap.final_revalidate()
    ledger_bytes = canonical(ledger) + b"\n"
    ledger_sha = hashlib.sha256(ledger_bytes).hexdigest()
    result = {
        "schema": SCHEMA + ".result.v1",
        "status": STATUS,
        "ledger": {"filename": LEDGER_NAME, "size": len(ledger_bytes), "sha256": ledger_sha, "object_sha256": digest(ledger)},
        "exact_census": ledger["exact_census"],
        "semantic_gaps": ledger["semantic_gaps"],
        "formal_credit": ledger["formal_credit"],
        "downstream_state": ledger["downstream_state"],
    }
    need(len(canonical(result)) <= ROW_CAP, "final result canonical cap")
    if write:
        publish(LEDGER_NAME, ledger_bytes)
        publish(RESULT_NAME, canonical(result) + b"\n")
    return ledger, result


def self_test() -> None:
    need(sum((38_624, 76_832)) == 115_456, "member sum")
    need(76_848 - 76_832 == 16, "reference excess")
    need(264 + 38_360 == 38_624, "G2a split")
    need(528 + 76_320 == 76_848, "G2b ref split")
    need(528 + 76_304 == 76_832, "G2b member split")
    need(38_624 + 115_472 == 154_096, "gap split")
    need(len({row[0] for row in PINS}) == len(PINS), "unique labels")
    need(len({row[2] for row in PINS}) == len(PINS), "unique files")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--full-replay", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    need(sum((args.self_test, args.print_contract, args.full_replay)) == 1, "choose exactly one mode")
    need(not args.write or args.full_replay, "write only with full replay")
    if args.self_test:
        self_test()
        print("PASS_K2G0_SELF_TEST")
    elif args.print_contract:
        print(canonical({"schema": SCHEMA, "status": STATUS, "pin_count": len(PINS), "row_cap": ROW_CAP, "writes_only_with_explicit_full_replay": True}).decode("ascii"))
    else:
        ledger, result = replay(args.write)
        print(canonical({"status": result["status"], "ledger_object_sha256": digest(ledger), "result_object_sha256": digest(result)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Blocked as exc:
        print("BLOCKED:" + str(exc), file=os.sys.stderr)
        raise SystemExit(2)
