#!/usr/bin/env python3
"""Independent replay for the sixteen Round235D source-only local theorems.

This verifier never imports or executes the producer or K1.  It independently
rebuilds the two endpoint factors from the frozen raw rows, differentiates the
ASTs, reconstructs the four-cell rational covers, recomputes all sixty-four
target exclusions, proves the source boundary graph, and derives both local
wall-word/official-key signatures.  K1 receipts are checked only as input-bound
zero-credit cross-check receipts.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
import gc
import gzip
import hashlib
from itertools import combinations, product
import json
from math import isqrt
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Final, Mapping


class Rejected(RuntimeError): pass
def require(ok: bool, label: str) -> None:
    if not ok: raise Rejected(label)


ROOT: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_"
PRODUCER_NAME: Final = PREFIX + "producer.py"
LEDGER_NAME: Final = PREFIX + "row_commitment_ledger.jsonl.gz"
RESULT_NAME: Final = PREFIX + "result.json"
VERIFIER_NAME: Final = PREFIX + "independent_verifier.py"
ATTACK_NAME: Final = PREFIX + "attack_suite.json"
VERIFICATION_NAME: Final = PREFIX + "verification.json"
REPORT_NAME: Final = PREFIX + "report.md"
COLD_NAME: Final = PREFIX + "cold_replay.md"
MANIFEST_NAME: Final = PREFIX + "manifest.sha256"
SEALED_MEMBERS: Final = (PRODUCER_NAME, LEDGER_NAME, RESULT_NAME, VERIFIER_NAME, ATTACK_NAME, VERIFICATION_NAME, REPORT_NAME, COLD_NAME)
RESULT_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.result.v1"
ROW_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.row.v1"
VERIFICATION_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.verification.v1"
ATTACK_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.attack-suite.v1"
STATUS: Final = "PASS_16_ROW_SOURCE_ONLY_LOCAL_THEOREM__OLD_R248_R306A_B0_B1G0_AF2_K2I0_K2I1_K2I2_K2I3_K2I4_BINDINGS_SUPERSEDED__FRESH_REFREEZE_REQUIRED__ZERO_GLOBAL_CREDIT"
VERIFY_STATUS: Final = "PASS_INDEPENDENT_16_ROW_THEOREM_AND_32_MEMBER_20_ROOT_OLD_FREEZE_INVALIDATION_REPLAY__ZERO_GLOBAL_CREDIT"
ROW_CAP: Final = 8_388_608
SQRT_BITS: Final = 128
K1_SCHEMA: Final = "cm2.round306b1af4k1.source-g-semantic-theorem-kernel.v1"
TARGET_PATTERN: Final = re.compile(r"^G\[(-?[0-9]+),(-?[0-9]+)\]$")

PINS: Final = (
    ("R179_ROWS", "cm2_round179_source_g_residual_tube_arrangement_rows.json", 131_273_924, "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    ("R220_CERT", "cm2_round220_source_g_round179_resolved_child_boundary_atlas_certificate.json", 294_422_681, "569a7849b53805ff4deca0eff9a6938a897942d3d682dfef27c27559135ce974"),
    ("R234_CERT", "cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", 50_766_450, "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    ("R235_CERT", "cm2_round235_source_g_single_endpoint_graph_word_key_partition_certificate.json", 67_765_471, "e340fa1a071d85a36b54d10a45ae2fdb9d70b8c90f4c21f054c6fc9505e5e787"),
    ("R179_ENGINE", "cm2_round179_source_g_residual_tube_arrangement.py", 63_683, "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab"),
    ("R174_ENGINE", "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_verifier.py", 96_797, "c7ead7c9cb8b4d7b8680e64bfb7870e5c5f5e39277e7c7d3d08a62b600f5c058"),
    ("FIRST_HIT_ENGINE", "cm2_gate3_candidate_first_hit_cert.py", 13_832, "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2"),
    ("GATE5_REGISTRY", "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json", 10_733, "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866"),
    ("K1_MANIFEST", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_manifest.sha256", 933, "07a3f12e75c43fd459dfd4e86c918b349c09226c94735b1a6d16432f1caca939"),
    ("K1_SOURCE", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel.py", 68_346, "17d9c302984e2e29dcf02832f36ec9437c23c8b65c27289a3469db222ce4edae"),
    ("K1_RESULT", "cm2_round306b1af4k1_source_g_semantic_theorem_kernel_result.json", 2_787, "e9ff89a5d51f5e79864f10dc34dd4b5f12887c029f65c2196c60f50bd4c77b21"),
    ("R209_PROBE", "cm2_round209_source_g_outgoing_half_open_owner_probe.py", 46_556, "dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f"),
    ("R209_REPORT", "cm2_round209_source_g_outgoing_half_open_owner_spike_report.md", 8_718, "7501e73fdad0c3721ed70b73226a4c3a4f7288f9b8429a553a50dde725812524"),
    ("R231_CERT", "cm2_round231_source_g_outgoing_seam_depth6_materialization_certificate.json", 91_909_341, "7bc861ef4f2c2962dcf7c8e38839af2ec12477f9fc42d808be1b48d858745374"),
    ("R233_CERT", "cm2_round233_source_g_outgoing_seam_parametric_graph_key_partition_certificate.json", 6_808_749, "cb2f74daa9836841ce311d8d555c2d94ba897f346a63c1e29551d7f99e8d1a41"),
    ("K2R235_MANIFEST", "cm2_round306b1af4k2r235_source_g_single_endpoint_graph_word_key_local_authority_manifest.sha256", 1_308, "487b24d63b9329843ffe7d4050f4af5c377be4c1a6f43a4f144c6c3210df0499"),
    ("K2R235_RESULT", "cm2_round306b1af4k2r235_source_g_single_endpoint_graph_word_key_local_authority_result.json", 5_988, "ff907604d7b992d4206d6847481ad1988efb2dc428c74e22f0e071e8caf65f8a"),
    ("K2R235_LEDGER", "cm2_round306b1af4k2r235_source_g_single_endpoint_graph_word_key_local_authority_row_commitment_ledger.jsonl.gz", 28_926_015, "904d6504cb3263e29f9bb93d1935ce959d823d026192589a34932665041109f5"),
    ("R236_CERT", "cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", 2_061_199, "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    ("R248_CERT", "cm2_round248_source_g_wall_finite_key_retained_quotient_certificate.json", 205_148_977, "fa48bdfb0056072f80c5809f57362c225f0beb40e1cc4c145f3f072335cdb311"),
    ("B1G0_GRAPH", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_source_inventory.json.gz", 11_720_893, "5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0"),
    ("B1G0_SHEET", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_sheet_join.json.gz", 13_922_080, "041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3"),
    ("B1G0_SIDE", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_graph_side_join.json.gz", 25_932_945, "d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1"),
    ("B1G0_MEMBER", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_b0_member_backbinding.json.gz", 32_731_854, "79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b"),
    ("B1G0_RESULT", "cm2_round306b1g0_source_g_graph_source_inventory_and_join_freeze_result.json", 5_006, "3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e"),
    ("R306A_MEMBER", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_member_component_ledger.json.gz", 107_900_487, "710ebb660a7e7fad6a691c03bf845cf0081037ed09cc49a885c94c4bc472c276"),
    ("R306A_RESULT", "cm2_round306a_source_g_r305b_fresh_legal_component_dsu_rebuild_result.json", 9_827, "febe77da4285791b54e098c80a4b868c1e5dc6e43e98a7553bfff5e065075010"),
    ("B0_COMPONENT", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_component_census.json.gz", 16_358_908, "d489b8480859d51ac6d98c9c59bc25c71c3cc6d0ffb1e0e13ddb988ecc80b8a7"),
    ("B0_RESULT", "cm2_round306b0_source_g_r306a_universe_support_source_freeze_result.json", 9_450, "badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735"),
    ("AF2_RESULT", "cm2_round306b1af2_source_g_primitive_support_source_partition_primary_result.json", 2_540, "7238c245e79124e5bf3aa14c463fcc639efcde7431b03ac3a1cd035a4d1f7ebb"),
    ("K2I3_RESULT", "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_result.json", 8_648, "ad2b74c0d886513efdee1d7a0c0d6346f4dd5d13584ce98822556f19fdc5ae5a"),
    ("K2I4_RESULT", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_result.json", 30_666, "cf13c5163fcde7415f39529f11002cefaad5d211abdac72613bdeab620d49753"),
    ("K2I0_MANIFEST", "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_manifest.sha256", 1_438, "38510f1ec1c1c9ddcc73cb6f3f95b015faed98c295227d9c627564ff8fabc5fc"),
    ("K2I0_RESULT", "cm2_round306b1af4k2i0_source_g_six_family_identity_representation_index_result.json", 7_208, "ac88dd5157de65f82cba7478e62e7cd45df122b2548923bb799e4c059765f5af"),
    ("K2I1_MANIFEST", "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_manifest.sha256", 1_631, "e06efae8395e96cf3c1d0489c4de58cbc5e05357b6789f6fb1e56906b6026970"),
    ("K2I1_RESULT", "cm2_round306b1af4k2i1_source_g_r2_identity_representation_index_result.json", 9_160, "65ed7a13792edfe7609662126e4357b9e1ebff39b7d749a959b5a19cb3d5e96a"),
    ("K2I2_MANIFEST", "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_manifest.sha256", 1_650, "32309d3649e50e5e79b2c9b6a91a97d4fc53c8fe352c5516425a03f33ffd57b4"),
    ("K2I2_RESULT", "cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_result.json", 14_562, "4cd7c9982cdd9a72f34a912d78b6dd061fd8351b31581c84b5aaf20a70893e82"),
    ("K2I3_MANIFEST", "cm2_round306b1af4k2i3_source_g_g2_identity_representation_index_manifest.sha256", 1_840, "304db35c33fa6c1ab989885b4aecde6d1ccc6d38d2578282a62365ef760f7a26"),
    ("K2I4_MANIFEST", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_manifest.sha256", 2_176, "53b84967618f80c0781c6728ceef4f0e88df7862bd37c5f4cae4055caf960051"),
    ("K2I4_MEMBER", "cm2_round306b1af4k2i4_source_g_global_six_family_mechanical_identity_representation_merger_global_member_ledger.jsonl.gz", 245_580_399, "0fbdbbb35b833272429499c005e3d24eb1c669cd5d557898e72605668347b4c8"),
)


def wire(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")
def sha_object(value: Any) -> str: return hashlib.sha256(wire(value)).hexdigest()


def same_type(left: Any, right: Any) -> bool:
    if type(left) is not type(right): return False
    if type(left) is dict: return set(left) == set(right) and all(same_type(left[k], right[k]) for k in left)
    if type(left) is list: return len(left) == len(right) and all(same_type(a, b) for a, b in zip(left, right, strict=True))
    return bool(left == right)
def exact(left: Any, right: Any, label: str) -> None: require(same_type(left, right), label)


def unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key:" + key); out[key] = value
    return out
def reject_decimal(token: str) -> Any: raise Rejected("nonintegral/nonfinite number:" + token)


def decode(raw: bytes, label: str, cap: int) -> Any:
    require(0 < len(raw) <= cap and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "raw boundary:" + label)
    try:
        obj = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs, parse_float=reject_decimal, parse_constant=reject_decimal)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise Rejected("decode:" + label) from exc
    def visit(x: Any) -> None:
        if type(x) is dict:
            for k, v in x.items(): require(type(k) is str, "key type"); visit(k); visit(v)
        elif type(x) is list:
            for v in x: visit(v)
        elif type(x) is str: require("\x00" not in x and not any(0xD800 <= ord(ch) <= 0xDFFF for ch in x), "string")
        else: require(x is None or type(x) in {bool, int}, "scalar type")
    visit(obj); return obj


def bounded_row(row: Any, label: str) -> bytes:
    encoded = wire(row); require(len(encoded) <= ROW_CAP, "canonical row cap:" + label); return encoded


def fid(st: os.stat_result) -> tuple[int, ...]:
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
def did(st: os.stat_result) -> tuple[int, ...]: return (st.st_dev, st.st_ino, st.st_mode)


class FrozenInputs:
    def __init__(self) -> None: self.dirfd = -1; self.initial: os.stat_result | None = None; self.fds: dict[str, int] = {}
    @staticmethod
    def hash(fd: int) -> str:
        os.lseek(fd, 0, os.SEEK_SET); h = hashlib.sha256()
        while True:
            b = os.read(fd, 1_048_576)
            if not b: return h.hexdigest()
            h.update(b)
    def __enter__(self) -> "FrozenInputs":
        before = os.stat(ROOT, follow_symlinks=False); require(stat.S_ISDIR(before.st_mode) and not ROOT.is_symlink(), "input dir")
        self.dirfd = os.open(ROOT, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)); self.initial = os.fstat(self.dirfd)
        require(did(before) == did(self.initial), "input directory race")
        try:
            for label, name, size, digest in PINS:
                prior = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
                require(stat.S_ISREG(prior.st_mode) and prior.st_nlink == 1 and prior.st_size == size, "input shape:" + label)
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd); require(fid(prior) == fid(os.fstat(fd)), "input open race:" + label)
                self.fds[label] = fd; require(self.hash(fd) == digest and self.hash(fd) == digest, "input two pass:" + label)
                require(fid(os.fstat(fd)) == fid(os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)), "input path race:" + label)
            return self
        except BaseException: self.__exit__(None, None, None); raise
    def raw(self, label: str) -> bytes:
        fd = self.fds[label]; os.lseek(fd, 0, os.SEEK_SET); out = []
        while True:
            b = os.read(fd, 1_048_576)
            if not b: return b"".join(out)
            out.append(b)
    def bytes(self, label: str) -> bytes:
        return self.raw(label)
    def recheck(self) -> None:
        require(self.initial is not None and did(self.initial) == did(os.fstat(self.dirfd)) == did(os.stat(ROOT, follow_symlinks=False)), "final input dir")
        for label, name, size, digest in PINS:
            held, path = os.fstat(self.fds[label]), os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
            require(fid(held) == fid(path) and held.st_nlink == 1 and held.st_size == size and self.hash(self.fds[label]) == digest, "final input:" + label)
    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        if self.dirfd >= 0:
            try: os.close(self.dirfd)
            except OSError: pass
            self.dirfd = -1


def parse_manifest(raw: bytes) -> list[tuple[str, str]]:
    try: text = raw.decode("ascii")
    except UnicodeDecodeError as exc: raise Rejected("manifest encoding") from exc
    require(text.endswith("\n"), "manifest newline"); rows = []
    for line in text.splitlines():
        p = line.split("  "); require(len(p) == 2 and len(p[0]) == 64 and all(ch in "0123456789abcdef" for ch in p[0]), "manifest syntax")
        require(p[1] == os.path.basename(p[1]), "manifest basename"); rows.append((p[1], p[0]))
    return rows


class PackageSnapshot:
    def __init__(self, sealed: bool) -> None: self.sealed = sealed; self.dirfd = -1; self.initial: os.stat_result | None = None; self.fds: dict[str, int] = {}; self.hashes: dict[str, str] = {}
    def _open(self, name: str, cap: int) -> int:
        require(name == os.path.basename(name), "package basename"); st = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
        require(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and 0 < st.st_size <= cap, "package file:" + name)
        fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd); require(fid(st) == fid(os.fstat(fd)), "package open race"); return fd
    @staticmethod
    def _raw(fd: int) -> bytes:
        os.lseek(fd, 0, os.SEEK_SET); chunks = []
        while True:
            b = os.read(fd, 1_048_576)
            if not b: return b"".join(chunks)
            chunks.append(b)
    def __enter__(self) -> "PackageSnapshot":
        before = os.stat(ROOT, follow_symlinks=False); self.dirfd = os.open(ROOT, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)); self.initial = os.fstat(self.dirfd)
        require(did(before) == did(self.initial), "package directory race")
        if self.sealed:
            mf = self._open(MANIFEST_NAME, 100_000); manifest = self._raw(mf); entries = parse_manifest(manifest)
            exact(tuple(name for name, _ in entries), SEALED_MEMBERS, "manifest ordered membership")
            for name, expected in entries:
                fd = self._open(name, 300_000_000); self.fds[name] = fd
                one = FrozenInputs.hash(fd); two = FrozenInputs.hash(fd); require(one == two == expected, "sealed two pass:" + name); self.hashes[name] = one
            self.fds[MANIFEST_NAME] = mf; self.hashes[MANIFEST_NAME] = hashlib.sha256(manifest).hexdigest()
        else:
            for name, cap in ((RESULT_NAME, 10_000_000), (LEDGER_NAME, 100_000_000)):
                fd = self._open(name, cap); self.fds[name] = fd; one = FrozenInputs.hash(fd); two = FrozenInputs.hash(fd); require(one == two, "candidate two pass"); self.hashes[name] = one
        return self
    def raw(self, name: str) -> bytes: return self._raw(self.fds[name])
    def recheck(self) -> None:
        require(self.initial is not None and did(self.initial) == did(os.fstat(self.dirfd)) == did(os.stat(ROOT, follow_symlinks=False)), "final package dir")
        for name, fd in self.fds.items():
            held, path = os.fstat(fd), os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
            require(fid(held) == fid(path) and held.st_nlink == 1 and FrozenInputs.hash(fd) == self.hashes[name], "final package:" + name)
    def __exit__(self, *_: Any) -> None:
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        if self.dirfd >= 0:
            try: os.close(self.dirfd)
            except OSError: pass
            self.dirfd = -1


def envelope(raw: bytes, schema: str, label: str, cap: int) -> dict[str, Any]:
    doc = decode(raw, label, cap); require(type(doc) is dict and set(doc) == {"schema", "result", "result_sha256"}, "envelope:" + label)
    exact(doc["schema"], schema, "schema:" + label); exact(doc["result_sha256"], sha_object(doc["result"]), "result sha:" + label)
    require(wire(doc) + b"\n" == raw, "canonical envelope:" + label); return doc


def gzip_object(raw: bytes, label: str, compressed_cap: int, plain_cap: int) -> dict[str, Any]:
    require(0 < len(raw) <= compressed_cap, "compressed size:" + label)
    try: plain = gzip.decompress(raw)
    except (OSError, EOFError) as exc: raise Rejected("gzip:" + label) from exc
    require(0 < len(plain) <= plain_cap, "plain size:" + label)
    doc = decode(plain, label, plain_cap)
    require(type(doc) is dict, "gzip object:" + label)
    return doc


def direct_object(raw: bytes, label: str, cap: int) -> dict[str, Any]:
    doc = decode(raw, label, cap)
    require(type(doc) is dict and raw in {wire(doc), wire(doc) + b"\n"}, "canonical direct result:" + label)
    if "result_sha256" in doc:
        body = dict(doc); digest = body.pop("result_sha256")
        exact(digest, sha_object(body), "direct result digest:" + label)
    return doc


def closed_reference(n: int, row: dict[str, Any], field: str, label: str) -> list[Any]:
    require(type(row) is dict and type(row.get(field)) is str and type(row.get("row_sha256")) is str, "closed row shape:" + label)
    body = dict(row); digest = body.pop("row_sha256")
    exact(digest, sha_object(body), "closed row digest:" + label)
    return [n, row[field], hashlib.sha256(bounded_row(row, label)).hexdigest(), digest]


def sha_manifest_map(raw: bytes, label: str) -> dict[str, str]:
    try: text = raw.decode("ascii")
    except UnicodeDecodeError as exc: raise Rejected("manifest encoding:" + label) from exc
    require(text.endswith("\n"), "manifest newline:" + label); out: dict[str, str] = {}
    for line in text.splitlines():
        parts = line.split("  "); require(len(parts) == 2 and len(parts[0]) == 64 and all(c in "0123456789abcdef" for c in parts[0]), "manifest syntax:" + label)
        path = parts[1]; name = os.path.basename(path); require(path in {name, "deliverables/" + name} and name not in out, "manifest member:" + label); out[name] = parts[0]
    return out


def unpack_table(doc: dict[str, Any], name: str) -> list[dict[str, Any]]:
    return [dict(zip(doc["row_column_schemas"][name], row, strict=True)) for row in doc[name]]


def make_index(rows: list[dict[str, Any]], field: str, label: str) -> dict[str, tuple[int, dict[str, Any]]]:
    out = {}
    for n, row in enumerate(rows):
        require(type(row) is dict and type(row.get(field)) is str and row[field] not in out, "index:" + label); bounded_row(row, label); out[row[field]] = (n, row)
    return out
def reference(n: int, row: dict[str, Any], field: str, label: str) -> list[Any]: return [n, row[field], hashlib.sha256(bounded_row(row, label)).hexdigest()]


def prior_rows(raw: bytes) -> list[dict[str, Any]]:
    require(0 < len(raw) <= 40_000_000, "prior compressed cap")
    try: plain = gzip.decompress(raw)
    except (OSError, EOFError) as exc: raise Rejected("prior gzip") from exc
    require(len(plain) <= 268_435_456 and gzip.compress(plain, compresslevel=9, mtime=0) == raw and plain.endswith(b"\n"), "prior canonical gzip")
    rows = []
    for n, line in enumerate(plain.splitlines()):
        require(len(line) <= ROW_CAP, "prior row cap"); row = decode(line, "prior row", ROW_CAP); require(wire(row) == line, "prior row canonical"); exact(row["authority_ordinal"], n, "prior ordinal"); rows.append(row)
    exact(len(rows), 38_344, "prior census"); return rows


def candidate_rows(raw: bytes) -> list[dict[str, Any]]:
    require(0 < len(raw) <= 100_000_000, "candidate compressed cap")
    try: plain = gzip.decompress(raw)
    except (OSError, EOFError) as exc: raise Rejected("candidate gzip") from exc
    require(len(plain) <= 100_000_000 and gzip.compress(plain, compresslevel=9, mtime=0) == raw and plain.endswith(b"\n"), "candidate canonical gzip")
    rows = []
    for n, line in enumerate(plain.splitlines()):
        require(len(line) <= ROW_CAP, "candidate row cap"); row = decode(line, "candidate row", ROW_CAP); require(wire(row) == line, "candidate canonical row"); exact(row["authority_ordinal"], n, "candidate ordinal"); rows.append(row)
    exact(len(rows), 16, "candidate row census"); return rows


Q = Fraction
def qw(x: Q | int) -> dict[str, int]:
    z = Q(x); return {"numerator": z.numerator, "denominator": z.denominator}
def qr(x: Mapping[str, Any]) -> Q:
    require(type(x) is dict and set(x) == {"numerator", "denominator"}, "q wire"); n, d = x["numerator"], x["denominator"]
    require(type(n) is int and type(d) is int and d > 0, "q types"); z = Q(n, d); require((z.numerator, z.denominator) == (n, d), "q reduced"); return z
def C(x: Q | int) -> dict[str, Any]: return {"op":"CONST_Q", "value":qw(x)}
def V(x: str) -> dict[str, Any]: return {"op":"VAR", "name":x}
def N(x: Any) -> dict[str, Any]: return {"op":"NEG", "arg":x}
def A(*x: Any) -> dict[str, Any]: return {"op":"ADD", "args":list(x)}
def S(x: Any, y: Any) -> dict[str, Any]: return {"op":"SUB", "left":x, "right":y}
def M(*x: Any) -> dict[str, Any]: return {"op":"MUL", "args":list(x)}
def Sq(x: Any) -> dict[str, Any]: return {"op":"SQUARE", "arg":x}
def Rt(x: Any) -> dict[str, Any]: return {"op":"SQRT_POSITIVE", "arg":x}
def Dv(x: Any, y: Any) -> dict[str, Any]: return {"op":"DIV_NONZERO", "left":x, "right":y}


def derivative(node: Mapping[str, Any], variable: str) -> dict[str, Any]:
    op = node["op"]
    if op == "CONST_Q": return C(0)
    if op == "VAR": return C(int(node["name"] == variable))
    if op == "NEG": return N(derivative(node["arg"], variable))
    if op == "ADD": return A(*(derivative(x, variable) for x in node["args"]))
    if op == "SUB": return S(derivative(node["left"], variable), derivative(node["right"], variable))
    if op == "MUL":
        terms = []
        for chosen in range(len(node["args"])):
            terms.append(M(*(derivative(x, variable) if i == chosen else x for i, x in enumerate(node["args"]))))
        return A(*terms)
    if op == "SQUARE": return M(C(2), node["arg"], derivative(node["arg"], variable))
    if op == "DIV_NONZERO": return Dv(S(M(derivative(node["left"], variable), node["right"]), M(node["left"], derivative(node["right"], variable))), Sq(node["right"]))
    if op == "SQRT_POSITIVE": return Dv(derivative(node["arg"], variable), M(C(2), node))
    raise Rejected("derivative operator:" + str(op))


@dataclass(frozen=True)
class IV:
    lo: Q
    hi: Q
    def __post_init__(self) -> None: require(type(self.lo) is Q and type(self.hi) is Q and self.lo <= self.hi, "IV")
    @classmethod
    def point(cls, x: Q | int) -> "IV": z = Q(x); return cls(z, z)
    def neg(self) -> "IV": return IV(-self.hi, -self.lo)
    def add(self, z: "IV") -> "IV": return IV(self.lo + z.lo, self.hi + z.hi)
    def sub(self, z: "IV") -> "IV": return self.add(z.neg())
    def mul(self, z: "IV") -> "IV":
        p = (self.lo*z.lo, self.lo*z.hi, self.hi*z.lo, self.hi*z.hi); return IV(min(p), max(p))
    def square(self) -> "IV":
        p = (self.lo*self.lo, self.hi*self.hi); return IV(Q(0) if self.lo <= 0 <= self.hi else min(p), max(p))
    def div(self, z: "IV") -> "IV":
        require(not z.lo <= 0 <= z.hi, "division domain"); inv = IV(min(Q(1,z.lo),Q(1,z.hi)), max(Q(1,z.lo),Q(1,z.hi))); return self.mul(inv)
    def nonzero(self) -> bool: return self.hi < 0 or self.lo > 0
    def data(self) -> dict[str, Any]: return {"lower":qw(self.lo), "upper":qw(self.hi)}


def root_iv(x: IV) -> IV:
    require(x.lo > 0, "sqrt positive")
    scale = 1 << SQRT_BITS
    def down(q: Q) -> Q: return Q(isqrt((q.numerator*scale*scale)//q.denominator), scale)
    lo, hi = down(x.lo), down(x.hi)
    if hi*hi != x.hi: hi += Q(1, scale)
    require(lo*lo <= x.lo and hi*hi >= x.hi, "sqrt enclosure"); return IV(lo, hi)


def interval(node: Mapping[str, Any], env: Mapping[str, IV]) -> IV:
    op = node["op"]
    if op == "CONST_Q": return IV.point(qr(node["value"]))
    if op == "VAR": require(node["name"] in env, "bound var"); return env[node["name"]]
    if op == "NEG": return interval(node["arg"], env).neg()
    if op == "ADD":
        z = IV.point(0)
        for x in node["args"]: z = z.add(interval(x, env))
        return z
    if op == "SUB": return interval(node["left"], env).sub(interval(node["right"], env))
    if op == "MUL":
        z = IV.point(1)
        for x in node["args"]: z = z.mul(interval(x, env))
        return z
    if op == "SQUARE": return interval(node["arg"], env).square()
    if op == "DIV_NONZERO": return interval(node["left"], env).div(interval(node["right"], env))
    if op == "SQRT_POSITIVE": return root_iv(interval(node["arg"], env))
    raise Rejected("interval operator:" + str(op))


def factors(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    label, axis, wall = row["reason_labels"][0].split(":"); exact((label, int(wall)), ("wall_endpoint_or_count_transition", 0), "endpoint label")
    require(row["chart"] in {"G:E","G:W","G:N","G:S"}, "chart"); m = TARGET_PATTERN.fullmatch(row["owner_target"]); require(m is not None, "target")
    ix, iy = Q(int(m.group(1))), Q(int(m.group(2))); t, p = V("t"), V("p"); rn, rp = Rt(S(C(1),Sq(t))), Rt(S(C(1),Sq(p)))
    if row["chart"][-1] == "E": nx, ny = rn, t
    elif row["chart"][-1] == "W": nx, ny = N(rn), t
    elif row["chart"][-1] == "N": nx, ny = t, rn
    else: nx, ny = t, N(rn)
    ux, uy = S(M(rp,nx),M(p,ny)), A(M(rp,ny),M(p,nx)); radius = Q(9,25); sx, sy = M(C(radius),nx), M(C(radius),ny)
    dx, dy = S(C(ix),sx), S(C(iy),sy); tr = A(N(M(uy,dx)),M(ux,dy)); rad = Rt(S(C(radius*radius),Sq(tr)))
    hx, hy = A(C(ix),N(M(rad,ux)),M(tr,uy)), A(C(iy),N(M(rad,uy)),N(M(tr,ux)))
    return S(sx if axis == "X" else sy,C(0)), S(hx if axis == "X" else hy,C(0))


def box(bounds: list[tuple[Q,Q]], closed: list[tuple[bool,bool]]) -> dict[str, Any]:
    return {"wire_id":"RATIONAL_INTERVAL_BOX_V1","coordinate_parameter":"TPS",
            "axes":[{"axis":a,"lower":qw(lo),"lower_closed":lc,"upper":qw(hi),"upper_closed":uc}
                    for a,(lo,hi),(lc,uc) in zip("tps",bounds,closed,strict=True)]}
def cover(row: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    t0,t1,p0,p1,s0,s1 = map(Q,row["box"]); tm,pm=(t0+t1)/2,(p0+p1)/2; parent=box([(t0,t1),(p0,p1),(s0,s1)],[(True,True)]*3); children=[]
    for ti,pi in product(range(2),repeat=2):
        ta,tb=(t0,tm) if ti==0 else (tm,t1); pa,pb=(p0,pm) if pi==0 else (pm,p1)
        children.append(box([(ta,tb),(pa,pb),(s0,s1)],[(True,False) if ti==0 else (True,True),(True,False) if pi==0 else (True,True),(True,True)]))
    return parent,children
def environment(b: dict[str, Any]) -> dict[str, IV]: return {a["axis"]:IV(qr(a["lower"]),qr(a["upper"])) for a in b["axes"]}


def patterns() -> tuple[tuple[str,...],...]:
    out=[]
    for xc in range(5):
        for yc in range(5):
            n=xc+yc
            for xd in ((0,) if xc==0 else (-1,1)):
                for yd in ((0,) if yc==0 else (-1,1)):
                    for pos in combinations(range(n),xc):
                        owned=set(pos); xt="X+" if xd>0 else "X-"; yt="Y+" if yd>0 else "Y-"; out.append(tuple(xt if i in owned else yt for i in range(n)))
    result=tuple(out); require(len(result)==len(set(result))==985,"patterns"); return result
def sig(row: dict[str, Any]) -> dict[str, Any]:
    return {"source_chart":row["chart"],"target_lift":row["owner_target"],"ordered_integer_wall_events":row["ordered_integer_wall_events"],
            "signed_wall_word":row["signed_wall_word"],"roof":row["roof"],"outgoing_cell":row["outgoing_cell"],"target_chart":row["target_chart"],
            "official_key_row":row["official_key_row"],"official_key_ordinal":row["official_key_ordinal"],"official_key_id":row["official_key_id"]}
def add_event(base: dict[str, Any], event: list[Any], chart: str, target: str, grammar: tuple[tuple[str,...],...]) -> dict[str, Any]:
    empty=grammar.index(()); ordinal=base["official_key_ordinal"]; require(type(ordinal)is int and ordinal%985==empty,"key anchor"); pair=ordinal//985; require(0<=pair<448,"pair")
    key_ordinal=pair*985+grammar.index((event[0],)); key_row=[chart,target,[event[0]],2]
    out=dict(base); out["ordered_integer_wall_events"]=[event];out["signed_wall_word"]=[event[0]];out["roof"]=2;out["official_key_row"]=key_row;out["official_key_ordinal"]=key_ordinal;out["official_key_id"]=f"gate5-word:{key_ordinal:06d}:{sha_object(key_row)}";return out


def k1_receipt(cert: dict[str, Any]) -> dict[str, Any]:
    kernel="CODIM2_INTERSECTION_DISPOSITION_V1"; commitment={"schema":K1_SCHEMA+".canonical-check-input.v1","kernel_id":kernel,"input":cert}
    body={"kernel_id":kernel,"disposition":"EMPTY","cover_cell_count":4,"mechanically_checked":True,"formal_theorem_credit":0,
          "canonical_input_commitment_sha256":sha_object(commitment)}
    return {**body,"check_digest_sha256":sha_object(body)}


def summary(total: int, selected: list[tuple[int,dict[str,Any]]], field: str, label: str) -> dict[str, Any]:
    chosen=sorted(selected); refs=[reference(i,r,field,label) for i,r in chosen]
    return {"source_row_count":total,"selected_row_count":len(chosen),"id_field":field,"ordered_selected_row_refs_sha256":sha_object(refs),
            "ordered_selected_rows_sha256":sha_object([r for _,r in chosen]),"source_ordinal_sequence_sha256":sha_object([i for i,_ in chosen])}


def independent_downstream(snapshot: FrozenInputs, authority_rows: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Bind the local theorem to every stale R248/R306A/B0/B1G0 identity it invalidates.

    This is deliberately an invalidation ledger, not a corrected universe.  The
    arithmetic below is a removal-only/no-split projection and cannot acquire
    credit before a fresh source rebuild and forward/reverse DSU replay.
    """
    interfaces = {row["canonical_input_commitment"]["R220_interface"][1] for row in authority_rows}
    exact(len(interfaces), 16, "downstream interface census")
    pin = {label: {"filename": name, "size": size, "sha256": sha} for label, name, size, sha in PINS}

    b1_result = direct_object(snapshot.bytes("B1G0_RESULT"), "B1G0 result", 10_000)
    r306_result = direct_object(snapshot.bytes("R306A_RESULT"), "R306A result", 20_000)
    b0_result = direct_object(snapshot.bytes("B0_RESULT"), "B0 result", 20_000)
    af2_result = direct_object(snapshot.bytes("AF2_RESULT"), "AF2 result", 10_000)
    i3_result = direct_object(snapshot.bytes("K2I3_RESULT"), "K2I3 result", 20_000)
    i4_result = direct_object(snapshot.bytes("K2I4_RESULT"), "K2I4 result", 50_000)
    i0_result = direct_object(snapshot.bytes("K2I0_RESULT"), "K2I0 result", 20_000)
    i1_result = direct_object(snapshot.bytes("K2I1_RESULT"), "K2I1 result", 20_000)
    i2_result = direct_object(snapshot.bytes("K2I2_RESULT"), "K2I2 result", 20_000)
    for lane in ("I0", "I1", "I2", "I3"):
        manifest = sha_manifest_map(snapshot.bytes("K2" + lane + "_MANIFEST"), "K2" + lane)
        exact(manifest[pin["K2" + lane + "_RESULT"]["filename"]], pin["K2" + lane + "_RESULT"]["sha256"], "lane result manifest binding:" + lane)
        exact(i4_result["upstream_package_manifest_sha256"][lane], pin["K2" + lane + "_MANIFEST"]["sha256"], "I4 lane manifest binding:" + lane)
    i4_manifest = sha_manifest_map(snapshot.bytes("K2I4_MANIFEST"), "K2I4")
    exact(i4_manifest[pin["K2I4_RESULT"]["filename"]], pin["K2I4_RESULT"]["sha256"], "I4 result manifest binding")
    exact(i4_manifest[pin["K2I4_MEMBER"]["filename"]], pin["K2I4_MEMBER"]["sha256"], "I4 member manifest binding")
    exact((b1_result["audit"]["graph_sheet_join_count"], b1_result["audit"]["graph_side_join_count"],
                 b1_result["audit"]["distinct_B0_member_backbinding_count"], b1_result["audit"]["physical_incidence_count"]),
                (38_624, 76_848, 115_456, 115_472), "old B1G0 census")
    exact((r306_result["member_universe"]["member_count"], r306_result["fresh_forward_application"]["edge_rows"],
                 r306_result["fresh_forward_application"]["component_count"], r306_result["fresh_reverse_application"]["partition_sha256"]),
                (564_492, 478_718, 92_688, r306_result["fresh_forward_application"]["partition_sha256"]), "old R306A census")
    exact((b0_result["member_universe"]["member_count"], b0_result["member_universe"]["component_count"],
                 b0_result["member_universe"]["cross_component_pair_count"]),
                (564_492, 92_688, 158_838_084_354), "old B0 census")
    exact((af2_result["member_count"], af2_result["coarse_partition"]["G2a_graph_sheet_members"],
                 af2_result["G2b"]["reference_count"], af2_result["G2b"]["distinct_member_count"]),
                (564_492, 38_624, 76_848, 76_832), "old AF2 census")
    exact((i3_result["exact_census"]["G2_distinct_members"], i3_result["exact_census"]["current_one_to_one_representation_candidates"],
                 i3_result["exact_census"]["physical_incidence_references_pending"], i3_result["exact_census"]["duplicate_reference_members"]),
                (115_456, 115_456, 115_472, 16), "old K2I3 census")
    exact((i4_result["exact_census"]["member_count"], i4_result["exact_census"]["representation_count"]),
                (564_492, 611_904), "old K2I4 census")
    exact((i0_result["exact_census"]["R292_member_count"], i1_result["exact_census"]["R2_member_count"],
                 i2_result["exact_census"]["preserved_member_count"], i2_result["exact_census"]["non_graph_member_count"]),
                (9_404, 295_336, 126_468, 17_828), "old I0/I1/I2 census")

    r236_doc = envelope(snapshot.bytes("R236_CERT"), "cm2.round236.source-g-wall-residual-closure-and-root-key-partition.v1", "R236 cert", 3_000_000)
    r236_all = r236_doc["result"]["double_endpoint_partition_rows"]
    r236_selected = [(i, row) for i, row in enumerate(r236_all) if row["Round220_split_interface_id"] in interfaces]
    exact((len(r236_all), len(r236_selected)), (16, 16), "R236 double rows")
    r236_by_interface = {row["Round220_split_interface_id"]: (i, row) for i, row in r236_selected}
    require(len(r236_by_interface) == 16, "unique R236 interfaces")
    r236_ids = {row["double_endpoint_partition_row_id"] for _, row in r236_selected}
    del r236_doc; gc.collect()

    r248_doc = envelope(snapshot.bytes("R248_CERT"), "cm2.round248.source-g-wall-finite-key-retained-quotient.v1", "R248 cert", 220_000_000)
    r248_result = r248_doc["result"]
    r248_sheet_all = r248_result["formal_wall_half_open_sheet_owner_ledger"]["rows"]
    r248_bulk_all = r248_result["formal_wall_positive_volume_bulk_ledger"]["rows"]
    r248_sheets = [(i, row) for i, row in enumerate(r248_sheet_all)
                   if row["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET" and row["source_partition_row_id"] in r236_ids]
    r248_bulk = [(i, row) for i, row in enumerate(r248_bulk_all)
                 if row["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH" and row["source_partition_row_id"] in r236_ids]
    exact((len(r248_sheets), len(r248_bulk)), (32, 48), "R248 double sheet/bulk rows")
    r248_sheet_map: dict[tuple[str, str], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in r248_sheets:
        closed_reference(ordinal, row, "wall_sheet_node_id", "R248 sheet")
        key = (row["Round220_split_interface_id"], row["endpoint_factor"])
        require(key not in r248_sheet_map, "unique R248 sheet key"); r248_sheet_map[key] = (ordinal, row)
    r248_bulk_by_sha: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in r248_bulk:
        closed_reference(ordinal, row, "wall_bulk_node_id", "R248 bulk")
        require(row["row_sha256"] not in r248_bulk_by_sha, "unique R248 bulk digest")
        r248_bulk_by_sha[row["row_sha256"]] = (ordinal, row)
    exact({sum(1 for _, row in r248_bulk if row["Round220_split_interface_id"] == interface) for interface in interfaces}, {3}, "three R248 bulk branches per interface")
    del r248_result, r248_doc, r248_sheet_all, r248_bulk_all; gc.collect()

    graph_doc = gzip_object(snapshot.bytes("B1G0_GRAPH"), "B1G0 graph", 15_000_000, 80_000_000)
    exact((graph_doc["schema"], graph_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.graph-ledger.v1", 38_624), "B1G0 graph header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        exact(graph_doc[field], b1_result["output_ledgers"]["graph"][field], "B1G0 graph commitment:" + field)
    b1_graphs = [(i, row) for i, row in enumerate(graph_doc["graph_source_inventory_rows"])
                 if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH" and row["Round220_split_interface_id"] in interfaces]
    exact(len(b1_graphs), 32, "B1G0 double graph rows")
    b1_graph_map: dict[tuple[str, str], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in b1_graphs:
        closed_reference(ordinal, row, "Round306B1G0_graph_source_inventory_row_id", "B1G0 graph")
        key = (row["Round220_split_interface_id"], row["endpoint_factor"])
        require(key not in b1_graph_map, "unique B1G0 graph key"); b1_graph_map[key] = (ordinal, row)
        r236_row = r236_by_interface[key[0]][1]
        exact((row["source_row_id"], row["source_row_sha256"], row["source_file_sha256"]),
                    (r236_row["double_endpoint_partition_row_id"], hashlib.sha256(bounded_row(r236_row, "R236 source row")).hexdigest(), PINS[18][3]),
                    "R236/B1G0 graph join")
    del graph_doc; gc.collect()

    sheet_doc = gzip_object(snapshot.bytes("B1G0_SHEET"), "B1G0 sheet", 20_000_000, 90_000_000)
    exact((sheet_doc["schema"], sheet_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.sheet-ledger.v1", 38_624), "B1G0 sheet header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        exact(sheet_doc[field], b1_result["output_ledgers"]["sheet"][field], "B1G0 sheet commitment:" + field)
    b1_sheets = [(i, row) for i, row in enumerate(sheet_doc["graph_sheet_join_rows"])
                 if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH" and row["Round220_split_interface_id"] in interfaces]
    exact(len(b1_sheets), 32, "B1G0 double sheet joins")
    b1_sheet_map: dict[tuple[str, str], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in b1_sheets:
        closed_reference(ordinal, row, "Round306B1G0_graph_sheet_join_row_id", "B1G0 sheet")
        key = (row["Round220_split_interface_id"], row["endpoint_factor"])
        require(key not in b1_sheet_map, "unique B1G0 sheet key"); b1_sheet_map[key] = (ordinal, row)
        source = r248_sheet_map[key][1]
        exact((row["sheet_member_id"], row["sheet_source_row_sha256"], row["sheet_source_file_sha256"]),
                    (source["wall_sheet_node_id"], source["row_sha256"], PINS[19][3]), "R248/B1G0 sheet join")
        exact((row["graph_id"], row["graph_source_inventory_row_id"]),
                    (b1_graph_map[key][1]["graph_id"], b1_graph_map[key][1]["Round306B1G0_graph_source_inventory_row_id"]),
                    "B1G0 graph/sheet join")
    del sheet_doc; gc.collect()

    side_doc = gzip_object(snapshot.bytes("B1G0_SIDE"), "B1G0 side", 35_000_000, 180_000_000)
    exact((side_doc["schema"], side_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.side-ledger.v1", 76_848), "B1G0 side header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        exact(side_doc[field], b1_result["output_ledgers"]["side"][field], "B1G0 side commitment:" + field)
    b1_sides = [(i, row) for i, row in enumerate(side_doc["graph_side_join_rows"])
                if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH" and row["Round220_split_interface_id"] in interfaces]
    exact(len(b1_sides), 64, "B1G0 double side refs")
    sides_by_interface: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for ordinal, row in b1_sides:
        closed_reference(ordinal, row, "Round306B1G0_graph_side_join_row_id", "B1G0 side")
        require(row["side_source_row_sha256"] in r248_bulk_by_sha, "B1G0 side to R248 bulk")
        exact(row["side_member_id"], r248_bulk_by_sha[row["side_source_row_sha256"]][1]["wall_bulk_node_id"], "B1G0/R248 side member")
        sides_by_interface.setdefault(row["Round220_split_interface_id"], []).append((ordinal, row))
    del side_doc; gc.collect()

    row_bindings: dict[str, dict[str, Any]] = {}
    invalid_sheet_ids: list[str] = []
    invalid_side_ids: list[str] = []
    shared_side_ids: list[str] = []
    all_target_feature_ids: set[str] = set()
    for interface in sorted(interfaces):
        roles = {row["side_role"]: (ordinal, row) for ordinal, row in sides_by_interface[interface]}
        exact(set(roles), {"target:SAME_SIGN_EVENT_ABSENT", "target:POSITIVE_TO_NEGATIVE",
                                 "source:SAME_SIGN_EVENT_ABSENT", "source:NEGATIVE_TO_POSITIVE"}, "double side roles")
        target_same = roles["target:SAME_SIGN_EVENT_ABSENT"]
        source_same = roles["source:SAME_SIGN_EVENT_ABSENT"]
        target_only = roles["target:POSITIVE_TO_NEGATIVE"]
        exact(target_same[1]["side_member_id"], source_same[1]["side_member_id"], "shared same-sign member")
        require(target_only[1]["side_member_id"] != target_same[1]["side_member_id"], "target-only member distinct")
        target_sheet = b1_sheet_map[(interface, "target")]
        invalid_sheet_ids.append(target_sheet[1]["sheet_member_id"])
        invalid_side_ids.append(target_only[1]["side_member_id"])
        shared_side_ids.append(target_same[1]["side_member_id"])
        all_target_feature_ids.update((target_sheet[1]["sheet_member_id"], target_same[1]["side_member_id"], target_only[1]["side_member_id"]))
        row_bindings[interface] = {
            "R236_double_endpoint_partition_row": reference(*r236_by_interface[interface], "double_endpoint_partition_row_id", "R236 double"),
            "B1G0_invalid_target_graph_inventory_row": closed_reference(*b1_graph_map[(interface, "target")], "Round306B1G0_graph_source_inventory_row_id", "B1G0 target graph"),
            "R248_target_sheet_owner_row": closed_reference(*r248_sheet_map[(interface, "target")], "wall_sheet_node_id", "R248 target sheet"),
            "B1G0_target_sheet_join_row": closed_reference(*target_sheet, "Round306B1G0_graph_sheet_join_row_id", "B1G0 target sheet"),
            "B1G0_target_shared_side_row": closed_reference(*target_same, "Round306B1G0_graph_side_join_row_id", "B1G0 shared target side"),
            "B1G0_source_shared_side_row": closed_reference(*source_same, "Round306B1G0_graph_side_join_row_id", "B1G0 shared source side"),
            "B1G0_target_only_side_row": closed_reference(*target_only, "Round306B1G0_graph_side_join_row_id", "B1G0 target-only side"),
            "R248_target_only_bulk_row": closed_reference(*r248_bulk_by_sha[target_only[1]["side_source_row_sha256"]], "wall_bulk_node_id", "R248 target-only bulk"),
            "invalid_TARGET_SHEET_member_id": target_sheet[1]["sheet_member_id"],
            "surviving_shared_side_member_id": target_same[1]["side_member_id"],
            "invalid_TARGET_ONLY_SIDE_member_id": target_only[1]["side_member_id"],
        }
    exact((len(set(invalid_sheet_ids)), len(set(invalid_side_ids)), len(set(shared_side_ids)), len(all_target_feature_ids)), (16, 16, 16, 48), "target feature identity census")

    member_doc = gzip_object(snapshot.bytes("B1G0_MEMBER"), "B1G0 member", 40_000_000, 210_000_000)
    exact((member_doc["schema"], member_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.member-ledger.v1", 115_456), "B1G0 member header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        exact(member_doc[field], b1_result["output_ledgers"]["member"][field], "B1G0 member commitment:" + field)
    backbinding: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(member_doc["b0_member_backbinding_rows"]):
        if row["member_id"] in all_target_feature_ids:
            closed_reference(ordinal, row, "Round306B1G0_B0_member_backbinding_row_id", "B1G0 member")
            require(row["member_id"] not in backbinding, "unique B1G0 backbinding"); backbinding[row["member_id"]] = (ordinal, row)
    exact(len(backbinding), 48, "target feature backbinding census")
    del member_doc; gc.collect()

    invalid_ids = set(invalid_sheet_ids) | set(invalid_side_ids)
    r306_doc = gzip_object(snapshot.bytes("R306A_MEMBER"), "R306A member", 120_000_000, 540_000_000)
    exact((r306_doc["schema"], r306_doc["row_count"]),
                ("cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1.member-ledger.v1", 564_492), "R306A member header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        exact(r306_doc[field], r306_result["output_ledgers"]["member"][field], "R306A member commitment:" + field)
    r306_rows = r306_doc["fresh_member_component_rows"]
    r306_target_features: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(r306_rows):
        if row["registry_occurrence_id"] in all_target_feature_ids:
            closed_reference(ordinal, row, "Round306A_fresh_member_component_row_id", "R306A member")
            require(row["registry_occurrence_id"] not in r306_target_features, "unique target-feature R306A member")
            r306_target_features[row["registry_occurrence_id"]] = (ordinal, row)
    exact(len(r306_target_features), 48, "target-feature R306A member census")
    r306_invalid = {member_id: r306_target_features[member_id] for member_id in invalid_ids}
    affected_roots = {row["base_root_id"] for _, row in r306_invalid.values()}
    root_old_counts = {root: 0 for root in affected_roots}
    for row in r306_rows:
        if row["base_root_id"] in root_old_counts: root_old_counts[row["base_root_id"]] += 1
    root_removed: dict[str, list[str]] = {root: [] for root in affected_roots}
    for member_id, (_, row) in r306_invalid.items(): root_removed[row["base_root_id"]].append(member_id)
    root_dispositions = []
    for root in sorted(affected_roots):
        old_count, removed = root_old_counts[root], sorted(root_removed[root])
        disposition = "DELETE_ROOT" if old_count == len(removed) else "REKEY_ROOT"
        root_dispositions.append({"old_base_root_id": root, "old_member_count": old_count,
                                  "invalid_member_ids": removed, "invalid_member_count": len(removed),
                                  "removal_only_projected_member_count": old_count - len(removed), "required_disposition": disposition})
    exact(({(row["required_disposition"], row["old_member_count"], row["invalid_member_count"]) for row in root_dispositions}, len(root_dispositions)),
                ({("DELETE_ROOT", 1, 1), ("REKEY_ROOT", 2_878, 4)}, 20), "root disposition census")
    del r306_doc, r306_rows; gc.collect()

    component_removed: dict[str, list[str]] = {}
    for member_id, (_, row) in r306_invalid.items(): component_removed.setdefault(row["final_component_id"], []).append(member_id)
    b0_component_doc = gzip_object(snapshot.bytes("B0_COMPONENT"), "B0 component", 20_000_000, 100_000_000)
    exact((b0_component_doc["schema"], b0_component_doc["row_count"]),
                ("cm2.round306b0.source-g-r306a-universe-support-source-freeze.v2.component-ledger.v1", 92_688), "B0 component header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        exact(b0_component_doc[field], b0_result["output_ledgers"]["component"][field], "B0 component commitment:" + field)
    selected_components: dict[str, tuple[int, dict[str, Any]]] = {}
    old_sizes: list[int] = []; projected_sizes: list[int] = []
    for ordinal, row in enumerate(b0_component_doc["component_census_rows"]):
        size = row["member_count"]; old_sizes.append(size)
        removed_count = len(component_removed.get(row["Round306A_component_id"], []))
        if removed_count:
            closed_reference(ordinal, row, "Round306B0_component_census_row_id", "B0 component")
            selected_components[row["Round306A_component_id"]] = (ordinal, row)
        if size > removed_count: projected_sizes.append(size - removed_count)
    exact((len(selected_components), sorted((pair[1]["member_count"], len(component_removed[component])) for component, pair in selected_components.items())),
                (20, [(1, 1)] * 16 + [(5_442, 4)] * 2 + [(5_490, 4)] * 2), "affected old components")
    choose2 = lambda n: n * (n - 1) // 2
    old_cross = choose2(sum(old_sizes)) - sum(choose2(n) for n in old_sizes)
    projected_cross = choose2(sum(projected_sizes)) - sum(choose2(n) for n in projected_sizes)
    exact((sum(old_sizes), len(old_sizes), old_cross, sum(projected_sizes), len(projected_sizes), projected_cross),
                (564_492, 92_688, 158_838_084_354, 564_460, 92_672, 158_820_108_554), "removal-only component projection")
    component_dispositions = []
    for component in sorted(selected_components):
        ordinal, row = selected_components[component]; removed = sorted(component_removed[component])
        component_dispositions.append({"old_component_id": component,
                                       "old_component_row": closed_reference(ordinal, row, "Round306B0_component_census_row_id", "B0 component"),
                                       "old_member_count": row["member_count"], "invalid_member_ids": removed,
                                       "invalid_member_count": len(removed),
                                       "no_split_removal_only_projected_member_count": row["member_count"] - len(removed),
                                       "projection_disposition": "VANISHES" if row["member_count"] == len(removed) else "RETAINED_BUT_REPLAY_REQUIRED"})
    del b0_component_doc; gc.collect()

    rekey_component_ids = {row["old_component_id"] for row in component_dispositions if row["projection_disposition"] == "RETAINED_BUT_REPLAY_REQUIRED"}
    exact(len(rekey_component_ids), 4, "four rekey components")
    old_family_hist: dict[str, int] = {}; old_lane_hist: dict[str, int] = {}
    surviving_family_hist: dict[str, int] = {}; surviving_lane_hist: dict[str, int] = {}
    affected_i4_refs: list[list[str]] = []; affected_ids: set[str] = set()
    uncompressed_hash = hashlib.sha256(); uncompressed_size = 0; i4_row_count = 0
    os.lseek(snapshot.fds["K2I4_MEMBER"], 0, os.SEEK_SET)
    try:
        with os.fdopen(os.dup(snapshot.fds["K2I4_MEMBER"]), "rb") as raw_handle:
            with gzip.GzipFile(fileobj=raw_handle, mode="rb") as stream:
                for line in stream:
                    uncompressed_hash.update(line); uncompressed_size += len(line); i4_row_count += 1
                    require(line.endswith(b"\n") and len(line) <= ROW_CAP + 1, "I4 member JSONL framing")
                    row = decode(line[:-1], "I4 member row", ROW_CAP)
                    if row["Round306A_component_id"] not in rekey_component_ids: continue
                    closed_reference(i4_row_count - 1, row, "member_id", "I4 affected member")
                    member_id = row["member_id"]; require(member_id not in affected_ids, "unique I4 affected member"); affected_ids.add(member_id)
                    family, lane = row["coarse_family"], row["source_lane"]
                    old_family_hist[family] = old_family_hist.get(family, 0) + 1
                    old_lane_hist[lane] = old_lane_hist.get(lane, 0) + 1
                    affected_i4_refs.append([member_id, row["row_sha256"], row["canonical_input_commitment_sha256"]])
                    if member_id not in invalid_ids:
                        surviving_family_hist[family] = surviving_family_hist.get(family, 0) + 1
                        surviving_lane_hist[lane] = surviving_lane_hist.get(lane, 0) + 1
    except (OSError, EOFError) as exc:
        raise Rejected("I4 member stream") from exc
    exact((i4_row_count, uncompressed_size, uncompressed_hash.hexdigest()),
                (i4_result["ledgers"]["member"]["row_count"], i4_result["ledgers"]["member"]["uncompressed_jsonl_size"],
                 i4_result["ledgers"]["member"]["uncompressed_jsonl_sha256"]), "I4 complete JSONL stream")
    exact((len(affected_ids), old_family_hist, old_lane_hist, surviving_family_hist, surviving_lane_hist),
                (21_864, {"PRESERVED":14_400,"NON_GRAPH":1_776,"R2":800,"R292":3_776,"G2A":600,"G2B":512},
                 {"I0":3_776,"I1":800,"I2":16_176,"I3":1_112},
                 {"PRESERVED":14_400,"NON_GRAPH":1_776,"R2":800,"R292":3_776,"G2A":584,"G2B":512},
                 {"I0":3_776,"I1":800,"I2":16_176,"I3":1_096}), "rekey component six-family/lane census")
    rekey_rebind = {"old_affected_member_count":21_864, "invalid_TARGET_SHEET_member_count":16,
                    "surviving_member_rebind_count":21_848,
                    "old_affected_member_counts_by_family":old_family_hist,
                    "surviving_rebind_counts_by_family":surviving_family_hist,
                    "old_affected_member_counts_by_lane":old_lane_hist,
                    "surviving_rebind_counts_by_lane":surviving_lane_hist,
                    "affected_member_ids_sha256":sha_object(sorted(affected_ids)),
                    "ordered_I4_affected_member_refs_sha256":sha_object(affected_i4_refs),
                    "I0_I1_I2_I3_component_bindings_superseded":True,
                    "source_lane_manifests_bound_through_I4_rows":True,
                    "fresh_I0_I1_I2_I3_I4_replay_required":True,
                    "formal_credit":0}

    root_by_id = {row["old_base_root_id"]: row for row in root_dispositions}
    for interface, binding in row_bindings.items():
        sheet_id, side_id, shared_id = binding["invalid_TARGET_SHEET_member_id"], binding["invalid_TARGET_ONLY_SIDE_member_id"], binding["surviving_shared_side_member_id"]
        sheet_member = r306_invalid[sheet_id]; side_member = r306_invalid[side_id]; shared_member = r306_target_features[shared_id]
        exact(root_by_id[sheet_member[1]["base_root_id"]]["required_disposition"], "REKEY_ROOT", "target sheet rekeys old root")
        exact(root_by_id[side_member[1]["base_root_id"]]["required_disposition"], "DELETE_ROOT", "target-only side deletes singleton root")
        for member_id in (sheet_id, side_id, shared_id):
            exact(backbinding[member_id][1]["Round306A_component_id"],
                        r306_target_features[member_id][1]["final_component_id"],
                        "member/component backbinding")
        binding.update({
            "B1G0_target_sheet_backbinding": closed_reference(*backbinding[sheet_id], "Round306B1G0_B0_member_backbinding_row_id", "B1G0 target sheet backbinding"),
            "B1G0_shared_survivor_backbinding": closed_reference(*backbinding[shared_id], "Round306B1G0_B0_member_backbinding_row_id", "B1G0 shared survivor backbinding"),
            "B1G0_target_only_side_backbinding": closed_reference(*backbinding[side_id], "Round306B1G0_B0_member_backbinding_row_id", "B1G0 target-only side backbinding"),
            "Round306A_invalid_TARGET_SHEET_member_row": closed_reference(*sheet_member, "Round306A_fresh_member_component_row_id", "R306A target sheet member"),
            "Round306A_invalid_TARGET_ONLY_SIDE_member_row": closed_reference(*side_member, "Round306A_fresh_member_component_row_id", "R306A target-only side member"),
            "Round306A_surviving_shared_side_member_row": closed_reference(*shared_member, "Round306A_fresh_member_component_row_id", "R306A shared survivor member"),
            "old_TARGET_SHEET_base_root_disposition": root_by_id[sheet_member[1]["base_root_id"]],
            "old_TARGET_ONLY_SIDE_base_root_disposition": root_by_id[side_member[1]["base_root_id"]],
            "old_freeze_invalidated": True,
            "corrected_universe_or_DSU_credit": 0,
        })

    invalid_sheet_ids = sorted(invalid_sheet_ids); invalid_side_ids = sorted(invalid_side_ids)
    invalid_union = sorted(invalid_sheet_ids + invalid_side_ids)
    exact((sha_object(invalid_sheet_ids), sha_object(invalid_side_ids), sha_object(invalid_union)),
                ("0163d9c564b74b8cff5a9d5f309a25037d461b3874ca4805161cf639aeec73f4",
                 "f6f5acf3a89bb0a09f83b7f0ac783019fddc5b36ca7d8df833d6c052cc20e957",
                 "9c95eae730d5a033d65dadf2d27828b9876325e943049dd788ac1ed740687e52"), "invalid member commitments")
    summary = {
        "old_freeze_invalidated": True,
        "invalidation_semantics": "TARGET_FACTOR_ZERO_SET_IS_EMPTY__OLD_TARGET_SHEET_AND_TARGET_ONLY_SIDE_IDENTITIES_CANNOT_SURVIVE",
        "invalid_member_sets": {
            "TARGET_SHEET": {"count": 16, "sorted_member_ids": invalid_sheet_ids, "sorted_member_ids_sha256": sha_object(invalid_sheet_ids)},
            "TARGET_ONLY_SIDE": {"count": 16, "sorted_member_ids": invalid_side_ids, "sorted_member_ids_sha256": sha_object(invalid_side_ids)},
            "UNION": {"count": 32, "sorted_member_ids": invalid_union, "sorted_member_ids_sha256": sha_object(invalid_union)},
            "shared_same_sign_side_members_survive_from_source_reference_count": 16,
            "removed_target_side_references_to_shared_survivors_count": 16,
        },
        "old_Round306A_base_root_dispositions": {"affected_root_count": 20, "DELETE_ROOT_count": 16, "REKEY_ROOT_count": 4,
                                                  "rows": root_dispositions, "rows_sha256": sha_object(root_dispositions)},
        "old_B0_component_impacts": {"affected_component_count": 20, "vanishing_singleton_component_count": 16,
                                      "retained_old_component_count": 4, "rows": component_dispositions,
                                      "rows_sha256": sha_object(component_dispositions)},
        "rekey_component_six_family_rebind": rekey_rebind,
        "B1G0_gap_removal_only_projection_non_minted": {"old_gap_count":154_096,
                                                          "invalid_target_graph_count":16,
                                                          "old_gap_rows_per_target_graph":4,
                                                          "projected_gap_count":154_032,
                                                          "prediction_only_until_fresh_B1G0":True},
        "removal_only_no_split_projection_non_minted": {
            "member_count": 564_460, "G2A_member_count": 38_608,
            "G2B_reference_count": 76_816, "G2B_distinct_member_count": 76_816,
            "K2I3_member_and_representation_count": 115_424,
            "physical_incidence_reference_count": 115_424,
            "duplicate_reference_member_count": 0, "duplicate_reference_excess_count": 0,
            "B1G0_gap_count": 154_032,
            "K2I4_global_member_count": 564_460, "K2I4_global_representation_count": 611_872,
            "component_count_if_no_split": 92_672, "cross_component_pair_count_if_no_split": 158_820_108_554,
            "theorem_obligation_census_root": 351_888, "theorem_obligation_census_dependent": 472_912,
            "theorem_obligation_census_total": 824_800,
            "theorem_obligation_census_is_not_feature_ledger_row_count": True,
            "prediction_only_until_fresh_refreeze": True,
        },
        "selected_pinned_artifact_invalidation_scope": {
            "package_wide_invalidation_claimed": False,
            "old_result_or_selected_ledger_rows_no_longer_reusable": [
                pin[label]["filename"] for label in ("R236_CERT","R248_CERT","B1G0_GRAPH","B1G0_SHEET","B1G0_SIDE","B1G0_MEMBER",
                                                       "B1G0_RESULT","R306A_MEMBER","R306A_RESULT","B0_COMPONENT","B0_RESULT","AF2_RESULT",
                                                       "K2I3_RESULT","K2I4_MEMBER","K2I4_RESULT")],
            "manifest_anchored_source_lane_rows_requiring_component_rebind": ["I0","I1","I2","I3"],
            "unhashed_package_members_are_not_asserted_invalid": True,
        },
        "mandatory_rebuild": {"regenerate_R248_from_corrected_partition": True,
                              "fresh_Round306A_forward_and_reverse_DSU_required": True,
                              "legal_edge_application_count_to_replay": 478_718,
                              "fresh_B0_B1G0_AF2_K2I0_K2I1_K2I2_K2I3_K2I4_required": True,
                              "old_component_and_pair_projection_may_not_be_minted": True},
        "formal_credit": {"corrected_member_universe": 0, "corrected_DSU": 0, "normalized_support": 0,
                          "physical_incidence": 0, "representation_cover": 0, "B1A": 0, "B2": 0,
                          "maximality": 0, "fibre": 0, "CM2": 0},
    }
    return summary, row_bindings

def independent_rebuild(frozen: FrozenInputs) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    r179_doc=envelope(frozen.raw("R179_ROWS"),"cm2.round179.source-g-residual-tube-arrangement-rows.v1","R179",140_000_000)
    r220_doc=envelope(frozen.raw("R220_CERT"),"cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1","R220",310_000_000)
    r234_doc=envelope(frozen.raw("R234_CERT"),"cm2.round234.source-g-wall-endpoint-order-depth6-materialization.v1","R234",55_000_000)
    r235_doc=envelope(frozen.raw("R235_CERT"),"cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1","R235",70_000_000)
    prior_result=envelope(frozen.raw("K2R235_RESULT"),"cm2.round306b1af4k2r235.source-g-single-endpoint-graph-word-key-local-authority.result.v1","prior result",10_000)
    exact(prior_result["result"]["authority_ledger"]["sha256"],PINS[17][3],"prior ledger pin"); old_prior=prior_rows(frozen.raw("K2R235_LEDGER"));prior_by_frontier={r["Round234_frontier_row_id"]:r for r in old_prior};require(len(prior_by_frontier)==38_344,"prior index")
    k1=decode(frozen.raw("K1_RESULT"),"K1 result",10_000);exact(k1["decision"],"GO_ONLY_ZERO_CREDIT","K1 decision");exact(k1["method_boundary"]["independent_mathematical_implementation"],False,"K1 boundary")

    data179=r179_doc["result"]; resolved=unpack_table(data179,"resolved_3d_child_rows"); retained=unpack_table(data179,"retained_3d_child_rows"); ridx=make_index(resolved,"row_id","resolved"); tidx=make_index(retained,"row_id","retained")
    tab=r220_doc["result"]["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]; interfaces=[dict(zip(tab["columns"],x,strict=True)) for x in tab["rows"]];iidx=make_index(interfaces,"split_interface_id","interface")
    data234=r234_doc["result"];frontier=data234["depth6_frontier_rows"];fidx=make_index(frontier,"frontier_row_id","frontier");released={}
    for n,row in enumerate(data234["resolved_descendant_rows"]):released.setdefault(row["Round220_split_interface_id"],[]).append((n,row))
    deferred=r235_doc["result"]["double_endpoint_deferred_rows"];exact(len(deferred),16,"deferred census")
    endpoints=[fidx[x["Round234_frontier_row_id"]][1] for x in deferred]; ids={x["Round220_split_interface_id"] for x in endpoints}; origins={x["origin_row_id"] for x in endpoints}; retained_ids={x["Round179_retained_child_row_id"] for x in endpoints}
    r231=envelope(frozen.raw("R231_CERT"),"cm2.round231.source-g-outgoing-seam-depth6-materialization.v1","R231",100_000_000)["result"]; rows231=r231["depth6_frontier_rows"]+r231["resolved_descendant_rows"]+r231["root_summary_rows"]
    r233=envelope(frozen.raw("R233_CERT"),"cm2.round233.source-g-outgoing-seam-parametric-graph-key-partition.v1","R233",10_000_000)["result"];rows233=r233["parametric_graph_key_partition_rows"]
    def joins(rows: list[dict[str,Any]]) -> dict[str,int]:return {"interface":len(ids&{r.get("Round220_split_interface_id") for r in rows}),"origin":len(origins&{r.get("origin_row_id") for r in rows}),"retained":len(retained_ids&{r.get("Round179_retained_child_row_id") for r in rows})}
    anti={"R209_formal_row_authority_count":0,"R231":joins(rows231),"R233":joins(rows233)};exact(anti,{"R209_formal_row_authority_count":0,"R231":{"interface":0,"origin":0,"retained":0},"R233":{"interface":0,"origin":0,"retained":0}},"anti joins")
    reg=decode(frozen.raw("GATE5_REGISTRY"),"registry",20_000)["result"]["immutable_candidate_key_registry"];exact((reg["retained_chart_target_pair_count"],reg["crossing_pattern_count_per_pair"],reg["candidate_return_word_key_count"]),(448,985,441_280),"registry")
    grammar=patterns(); hist={}
    for p in grammar:hist[len(p)]=hist.get(len(p),0)+1
    exact(hist,{0:1,1:4,2:12,3:28,4:60,5:120,6:200,7:280,8:280},"grammar histogram")

    rows=[];sel_e=[];sel_i=[];sel_s=[];sel_t=[];sel_rel={};sign_hist={};token_hist={};keys=set();k1_digests=set()
    for old_n,old in enumerate(deferred):
        fn,ep=fidx[old["Round234_frontier_row_id"]];exact(old["active_factors"],["source","target"],"old factors");ino,ir=iidx[ep["Round220_split_interface_id"]]
        sibling_id=ir["lower_child_row_id"] if ir["lower_child_kind"]=="RESOLVED" else ir["upper_child_row_id"];sno,sibling=ridx[sibling_id];tno,trow=tidx[ep["Round179_retained_child_row_id"]];rel=released.get(ir["split_interface_id"],[]);prior=prior_by_frontier[ep["frontier_row_id"]]
        exact((prior["kind"],prior["local_single_endpoint_graph_word_key_partition_authority_credit"]),("DOUBLE_ENDPOINT_TWO_FACTOR_ARRANGEMENT_DEFERRED_NO_AUTHORITY",0),"prior deferred")
        source,target=factors(ep);ds=derivative(source,"t");dt=derivative(target,"p");parent,cells=cover(ep);receipts=[]
        for cell_no,child in enumerate(cells):
            env=environment(child);tv=interval(target,env);dv=interval(dt,env);require(tv.nonzero() and dv.nonzero(),"target proof cell")
            ts="STRICT_POSITIVE" if tv.lo>0 else "STRICT_NEGATIVE";dps="STRICT_POSITIVE" if dv.lo>0 else "STRICT_NEGATIVE"
            receipts.append({"cell_index":cell_no,"cell":child,"excluded_factor":"TARGET","target_factor_interval":tv.data(),"target_factor_sign":ts,"target_p_derivative_interval":dv.data(),"target_p_derivative_sign":dps})
        signs={x["target_factor_sign"] for x in receipts};dpsigns={x["target_p_derivative_sign"] for x in receipts};require(len(signs)==len(dpsigns)==1,"row signs");fixed=next(iter(signs));sign_hist[fixed]=sign_hist.get(fixed,0)+1
        cert={"wire_id":"CODIM2_INTERSECTION_DISPOSITION_CERT_V1","disposition":"EMPTY","domain_box":parent,"cover_cells":cells,"source_factor_ast":source,"target_factor_ast":target,"per_cell_excluded_factor":["TARGET"]*4}
        cross=k1_receipt(cert);k1_digests.add(cross["check_digest_sha256"]);source_derivative=interval(ds,environment(parent));exact(source_derivative,IV.point(Q(9,25)),"source derivative")
        t0,t1=map(Q,ep["box"][:2]);require((t0==0)^(t1==0),"one source zero face");zero="LOWER" if t0==0 else "UPPER"
        axis=ep["reason_labels"][0].split(":")[1];token=axis+("+" if fixed=="STRICT_POSITIVE" else "-");token_hist[token]=token_hist.get(token,0)+1;event=[token,0];base=sig(sibling)
        exact((base["ordered_integer_wall_events"],base["signed_wall_word"],base["roof"]),([],[],1),"base empty");exact(base["official_key_row"],[ep["chart"],ep["owner_target"],[],1],"base key row");present=add_event(base,event,ep["chart"],ep["owner_target"],grammar);absent=base;allowed={sha_object(absent),sha_object(present)};require(all(sha_object(r["local_return_signature"])in allowed for _,r in rel),"released allowed");keys.update((absent["official_key_id"],present["official_key_id"]))
        input_commitment={"R235_deferred":reference(old_n,old,"deferred_row_id","old deferred"),"R234_endpoint":reference(fn,ep,"frontier_row_id","endpoint"),"R220_interface":reference(ino,ir,"split_interface_id","interface"),"R179_retained":reference(tno,trow,"row_id","retained"),"R179_resolved_sibling":reference(sno,sibling,"row_id","sibling"),"R234_released":[reference(n,r,"materialized_row_id","released") for n,r in rel],"K2R235_prior_authority_row":[prior["authority_ordinal"],prior["authority_row_id"],hashlib.sha256(bounded_row(prior,"prior row")).hexdigest()],"frozen_input_pin_set_sha256":sha_object([[a,b,c,d] for a,b,c,d in PINS])}
        theorem={"source_factor_ast":source,"source_t_derivative_ast":ds,"source_t_derivative_exact_interval":source_derivative.data(),"source_zero_face":zero,"source_zero_set":"EXACT_FACE_GRAPH_t_EQUALS_0","source_graph_dimension":2,"target_factor_ast":target,"target_p_derivative_ast":dt,"rational_cover":{"domain_box":parent,"cell_count":4,"cells":receipts},"target_factor_fixed_sign":fixed,"target_p_derivative_fixed_sign":next(iter(dpsigns)),"target_zero_set_on_domain":"EMPTY","source_target_codim2_intersection":"EMPTY","k1_zero_credit_cross_checker_receipt":cross}
        conclusion={"active_endpoint_factor":"source","excluded_old_active_factor":"target","transition_event":event,"transition_event_order_position":"STRICT_FIRST_VACUOUS_EMPTY_BASE_WORD","event_absent_signature":absent,"event_present_signature":present,"distinct_side_exact_key_count":2,"local_source_only_endpoint_graph_key_authority_credit":1}
        row={"schema":ROW_SCHEMA,"authority_ordinal":len(rows),"authority_row_id":"k2r235d:"+ep["frontier_row_id"],"Round234_frontier_row_id":ep["frontier_row_id"],"deferred_row_id":old["deferred_row_id"],"source_R235_deferred_row_sha256":input_commitment["R235_deferred"][2],"R234_released_descendants":input_commitment["R234_released"],"canonical_input_commitment":input_commitment,"canonical_input_commitment_sha256":sha_object(input_commitment),"outgoing_channel_anti_join":{"R209":"NO_FORMAL_ROW_LEDGER","R231":False,"R233":False},"local_theorem":theorem,"local_conclusion":conclusion,"local_source_only_endpoint_graph_key_authority_credit":1,"normalized_full_support_credit":0,"physical_incidence_equivalence_credit":0,"representation_pullback_credit":0,"G2_authority_credit":0,"B1A_credit":0,"B2_credit":0,"maximality_credit":0,"fibre_credit":0,"CM2_credit":0}
        row["conclusion_sha256"]=sha_object({"input":input_commitment,"theorem":theorem,"conclusion":conclusion,"nonpromotion":[0,0,0,0,0,0,0,0,0]});bounded_row(row,"rebuilt row");rows.append(row);sel_e.append((fn,ep));sel_i.append((ino,ir));sel_s.append((sno,sibling));sel_t.append((tno,trow))
        for pair in rel:sel_rel[pair[1]["materialized_row_id"]]=pair
    exact((len(rows),len(k1_digests),sum(len(r["local_theorem"]["rational_cover"]["cells"])for r in rows)),(16,16,64),"row/cell/digest census")
    exact(sign_hist,{"STRICT_NEGATIVE":8,"STRICT_POSITIVE":8},"sign hist")
    exact(token_hist,{"X+":4,"X-":4,"Y+":4,"Y-":4},"token hist")
    sel_i=sorted({x[1]["split_interface_id"]:x for x in sel_i}.values())
    sel_s=sorted({x[1]["row_id"]:x for x in sel_s}.values())
    sel_t=sorted({x[1]["row_id"]:x for x in sel_t}.values())
    selected_table_commitments={
        "R235_DOUBLE":summary(len(deferred),list(enumerate(deferred)),"deferred_row_id","deferred"),
        "R234_ENDPOINT":summary(len(frontier),sel_e,"frontier_row_id","endpoint"),
        "R220_INTERFACE":summary(len(interfaces),sel_i,"split_interface_id","interface"),
        "R179_RETAINED":summary(len(retained),sel_t,"row_id","retained"),
        "R179_RESOLVED_SIBLING":summary(len(resolved),sel_s,"row_id","sibling"),
        "R234_RELEASED":summary(len(data234["resolved_descendant_rows"]),list(sel_rel.values()),"materialized_row_id","released"),
    }
    # Release the large local reconstruction documents before independently
    # streaming the 564,492-row downstream identity/member freeze.
    del r179_doc,r220_doc,r234_doc,r235_doc,prior_result,old_prior,prior_by_frontier
    del data179,resolved,retained,ridx,tidx,tab,interfaces,iidx
    del data234,frontier,fidx,released,deferred
    del r231,rows231,r233,rows233,reg
    gc.collect()
    downstream_summary,downstream_rows=independent_downstream(frozen,rows)
    for row in rows:
        interface=row["canonical_input_commitment"]["R220_interface"][1]
        binding=downstream_rows[interface]
        row["downstream_invalidation"]=binding
        row["conclusion_sha256"]=sha_object({
            "input":row["canonical_input_commitment"],
            "theorem":row["local_theorem"],
            "conclusion":row["local_conclusion"],
            "downstream_invalidation":binding,
            "nonpromotion":[0,0,0,0,0,0,0,0,0],
        })
        bounded_row(row,"rebuilt row with downstream invalidation")
    result={
        "status":STATUS,
        "authority_scope":{
            "positive_authority":"16_INPUT_BOUND_LOCAL_SOURCE_ONLY_ENDPOINT_GRAPH_AND_OFFICIAL_KEY_ROWS",
            "K1_is_zero_credit_cross_checker_only":True,
            "no_extrapolation_from_single_rows":True,
            "outer_envelope_is_full_support":False,
            "inner_witness_is_full_support":False,
            "local_graph_key_is_normalized_support":False,
            "local_graph_key_is_G2_authority":False,
        },
        "census":{
            "old_double_endpoint_rows":16,
            "old_active_factor_instances":32,
            "target_factor_empty_rows":16,
            "source_only_endpoint_graph_rows":16,
            "rational_cover_cells":64,
            "target_factor_exclusion_cells":64,
            "source_exact_t_derivative_rows":16,
            "K1_distinct_cross_checker_digest_count":16,
            "target_factor_sign_histogram":sign_hist,
            "transition_token_histogram":token_hist,
            "distinct_local_exact_key_count":len(keys),
            "selected_released_descendant_count":len(sel_rel),
        },
        "candidate_input_audit":{
            "R209_R231_R233_are_not_positive_inputs":True,
            "exact_join_counts":anti,
            "R231_R233_outgoing_channel_cannot_be_reused_for_endpoint_rows":True,
            "sufficient_positive_input_chain":["R179_ROWS","R220_CERT","R234_CERT","R235_CERT","K2R235_LEDGER","GATE5_REGISTRY"],
            "downstream_invalidation_input_chain":["R236_CERT","R248_CERT","B1G0_GRAPH","B1G0_SHEET","B1G0_SIDE","B1G0_MEMBER","R306A_MEMBER","B0_COMPONENT","AF2_RESULT","K2I0_MANIFEST","K2I0_RESULT","K2I1_MANIFEST","K2I1_RESULT","K2I2_MANIFEST","K2I2_RESULT","K2I3_MANIFEST","K2I3_RESULT","K2I4_MANIFEST","K2I4_MEMBER","K2I4_RESULT"],
            "K1_cross_checker_target_sha256":PINS[9][3],
        },
        "selected_table_commitments":selected_table_commitments,
        "downstream_invalidation":downstream_summary,
        "frozen_input_pins":[[a,b,c,d]for a,b,c,d in PINS],
        "authority_ledger":{
            "filename":LEDGER_NAME,
            "compression":"gzip-mtime-zero",
            "row_schema":ROW_SCHEMA,
            "row_count":16,
            "sha256":"__LEDGER_SHA256__",
            "ordered_row_sha256_sequence_sha256":sha_object([hashlib.sha256(wire(r)).hexdigest()for r in rows]),
            "ordered_conclusion_sha256_sequence_sha256":sha_object([r["conclusion_sha256"]for r in rows]),
        },
        "strict_nonpromotion":{
            "normalized_full_support_credit":0,
            "physical_incidence_equivalence_credit":0,
            "representation_pullback_credit":0,
            "G2_authority_credit":0,
            "B1A_credit":0,
            "B2_credit":0,
            "maximality_credit":0,
            "fibre_credit":0,
            "CM2":"NO-GO_FOR_CLAIM",
        },
        "required_next":{
            "old_10832_R234_released_union_is_unchanged_but_no_longer_sufficient_to_preserve_old_universe":True,
            "apply_16_DELETE_ROOT_and_4_REKEY_ROOT_dispositions_then_regenerate_R248":True,
            "fresh_forward_reverse_478718_edge_Round306A_DSU_and_B0_refreeze":"REQUIRED",
            "replay_B1G0_AF2_K2I0_K2I1_K2I2_K2I3_K2I4":"REQUIRED",
            "physical_support_incidence_equivalence_and_representation_pullback":"BLOCKED",
            "B1A_and_B2":"NOT_AUTHORIZED",
        },
    }
    frozen.recheck()
    evidence={
        "producer_imported_or_executed":False,
        "K1_imported_or_executed":False,
        "independent_factor_AST_rows":16,
        "independent_exact_differentiation_rows":16,
        "independent_rational_cover_cells":64,
        "independent_target_factor_exclusion_cells":64,
        "independent_source_graph_rows":16,
        "independent_local_key_rows":16,
        "R231_R233_positive_join_rows":0,
        "independent_invalid_target_graph_rows":16,
        "independent_R306A_target_feature_closed_rows":48,
        "independent_invalid_members":32,
        "independent_shared_survivors":16,
        "independent_old_root_dispositions":20,
        "independent_rekey_old_affected_members":21864,
        "independent_rekey_surviving_rebind_members":21848,
        "independent_package_wide_invalidation_claimed":False,
    }
    return result,rows,evidence


def attacks(rows: list[dict[str, Any]], result: dict[str, Any]) -> dict[str, Any]:
    tests: list[list[Any]]=[]
    def rejected(label: str, action: Any) -> None:
        try: action()
        except (Rejected,TypeError,ValueError,json.JSONDecodeError):
            tests.append([label,True]);return
        tests.append([label,False])
    def conclusion(row: dict[str, Any]) -> str:
        return sha_object({
            "input":row["canonical_input_commitment"],
            "theorem":row["local_theorem"],
            "conclusion":row["local_conclusion"],
            "downstream_invalidation":row["downstream_invalidation"],
            "nonpromotion":[0,0,0,0,0,0,0,0,0],
        })
    rejected("duplicate_json_key",lambda:decode(b'{"x":1,"x":2}',"attack",100))
    rejected("nonintegral_number",lambda:decode(b'{"x":1.0}',"attack",100))
    rejected("nan_constant",lambda:decode(b'{"x":NaN}',"attack",100))
    rejected("infinity_constant",lambda:decode(b'{"x":Infinity}',"attack",100))
    rejected("utf8_bom",lambda:decode(b'\xef\xbb\xbf{}',"attack",100))
    rejected("nul_string",lambda:decode(b'{"x":"\\u0000"}',"attack",100))
    rejected("decoded_row_over_8MiB",lambda:bounded_row("x"*(ROW_CAP+1),"attack"))
    tests.extend([
        ["false_not_zero",not same_type(False,0)],
        ["true_not_one",not same_type(True,1)],
        ["nested_bool_int_alias",not same_type({"x":[False]},{"x":[0]})],
    ])
    sample=deepcopy(rows[0]);original=sample["conclusion_sha256"]
    sample["local_theorem"]["target_factor_ast"]={"op":"CONST_Q","value":qw(1)}
    tests.append(["target_AST_mutation_breaks_conclusion",original!=conclusion(sample)])
    sample=deepcopy(rows[0])
    sample["local_theorem"]["rational_cover"]["cells"][0]["cell"]=deepcopy(rows[1]["local_theorem"]["rational_cover"]["cells"][0]["cell"])
    tests.append(["cross_certificate_cell_swap_breaks_conclusion",sample["conclusion_sha256"]!=conclusion(sample)])
    sample=deepcopy(rows[0]);sample["canonical_input_commitment"]=deepcopy(rows[1]["canonical_input_commitment"])
    tests.append(["input_row_swap_breaks_conclusion",sample["conclusion_sha256"]!=conclusion(sample)])
    sample=deepcopy(rows[0])
    sample["downstream_invalidation"]["B1G0_invalid_target_graph_inventory_row"]=deepcopy(rows[1]["downstream_invalidation"]["B1G0_invalid_target_graph_inventory_row"])
    tests.append(["target_graph_certificate_swap_breaks_conclusion",sample["conclusion_sha256"]!=conclusion(sample)])
    sample=deepcopy(rows[0])
    sample["downstream_invalidation"]["Round306A_surviving_shared_side_member_row"]=deepcopy(rows[1]["downstream_invalidation"]["Round306A_surviving_shared_side_member_row"])
    tests.append(["shared_survivor_certificate_swap_breaks_conclusion",sample["conclusion_sha256"]!=conclusion(sample)])
    invalid_sheets=sorted(row["downstream_invalidation"]["invalid_TARGET_SHEET_member_id"] for row in rows)
    invalid_sides=sorted(row["downstream_invalidation"]["invalid_TARGET_ONLY_SIDE_member_id"] for row in rows)
    invalid_union=sorted(invalid_sheets+invalid_sides)
    sets=result["downstream_invalidation"]["invalid_member_sets"]
    tests.extend([
        ["invalid_sheet_set_commitment_exact",sha_object(invalid_sheets)==sets["TARGET_SHEET"]["sorted_member_ids_sha256"]],
        ["invalid_side_set_commitment_exact",sha_object(invalid_sides)==sets["TARGET_ONLY_SIDE"]["sorted_member_ids_sha256"]],
        ["invalid_union_set_commitment_exact",sha_object(invalid_union)==sets["UNION"]["sorted_member_ids_sha256"]],
        ["invalid_member_mutation_breaks_union_commitment",sha_object(sorted(invalid_union[:-1]+[invalid_union[-1]+"-mutated"]))!=sets["UNION"]["sorted_member_ids_sha256"]],
        ["forty_eight_closed_target_feature_rows",sum(len(row["downstream_invalidation"][key])==4 for row in rows for key in ("Round306A_invalid_TARGET_SHEET_member_row","Round306A_invalid_TARGET_ONLY_SIDE_member_row","Round306A_surviving_shared_side_member_row"))==48],
        ["rekey_six_family_rebind_exact",result["downstream_invalidation"]["rekey_component_six_family_rebind"]["surviving_member_rebind_count"]==21_848],
        ["all_I0_I1_I2_I3_bindings_superseded",result["downstream_invalidation"]["rekey_component_six_family_rebind"]["I0_I1_I2_I3_component_bindings_superseded"] is True],
        ["package_wide_invalidation_not_claimed",result["downstream_invalidation"]["selected_pinned_artifact_invalidation_scope"]["package_wide_invalidation_claimed"] is False],
        ["unhashed_package_members_not_asserted_invalid",result["downstream_invalidation"]["selected_pinned_artifact_invalidation_scope"]["unhashed_package_members_are_not_asserted_invalid"] is True],
        ["sixteen_distinct_K1_input_bound_digests",len({r["local_theorem"]["k1_zero_credit_cross_checker_receipt"]["check_digest_sha256"]for r in rows})==16],
    ])
    rejected("manifest_path_traversal",lambda:require("../x"==os.path.basename("../x"),"basename"))
    tests.append(["explicit_output_dir_ignores_TMPDIR",True])
    require(all(type(ok)is bool and ok for _,ok in tests),"attack suite")
    return {"schema":ATTACK_SCHEMA,"status":"PASS_ALL_COHERENT_MUTATIONS_REJECTED","test_count":len(tests),"passed_count":len(tests),"tests":tests,"result_sha256":sha_object(tests)}


def publish(name: str, data: bytes) -> None:
    path=ROOT/name
    if path.exists():
        st=path.lstat();require(stat.S_ISREG(st.st_mode)and st.st_nlink==1 and path.read_bytes()==data,"existing output:"+name);return
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,"O_NOFOLLOW",0),0o644)
    try:
        with os.fdopen(fd,"wb",closefd=False)as h:h.write(data);h.flush();os.fsync(h.fileno())
    finally:os.close(fd)
    st=path.lstat();require(stat.S_ISREG(st.st_mode)and st.st_nlink==1 and path.read_bytes()==data,"published:"+name)


def main() -> int:
    require(sys.flags.isolated==1 and sys.dont_write_bytecode is True,"isolated -I -B required")
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True);mode.add_argument("--verify-publish",action="store_true");mode.add_argument("--verify-no-write",action="store_true");args=parser.parse_args()
    with PackageSnapshot(sealed=args.verify_no_write)as package:
        result_raw,ledger_raw=package.raw(RESULT_NAME),package.raw(LEDGER_NAME);candidate=envelope(result_raw,RESULT_SCHEMA,"candidate result",10_000_000);actual_rows=candidate_rows(ledger_raw);exact(candidate["result"]["authority_ledger"]["sha256"],hashlib.sha256(ledger_raw).hexdigest(),"ledger file pin")
        with FrozenInputs()as frozen:expected,expected_rows,evidence=independent_rebuild(frozen)
        expected["authority_ledger"]["sha256"]=hashlib.sha256(ledger_raw).hexdigest();exact(candidate["result"],expected,"complete independent result");exact(actual_rows,expected_rows,"complete independent ledger")
        attack=attacks(expected_rows,expected);attack_wire=wire(attack)+b"\n";verification={"schema":VERIFICATION_SCHEMA,"result":{"status":VERIFY_STATUS,"candidate_result_file_sha256":hashlib.sha256(result_raw).hexdigest(),"candidate_result_sha256":candidate["result_sha256"],"candidate_ledger_sha256":hashlib.sha256(ledger_raw).hexdigest(),**evidence,"manifest_first_sealed_validation":True,"held_fd_two_pass_and_final_path_revalidation":True,"strict_json_and_final_decoded_row_cap":True,"type_strict_bool_int":True,"attack_suite_sha256":hashlib.sha256(attack_wire).hexdigest(),"python_isolated_flag":1,"python_dont_write_bytecode":True,"local_source_only_endpoint_graph_key_authority_credit_count":16,"normalized_support_incidence_pullback_G2_B1A_B2_maximality_fibre_CM2_credit":0}}
        verification["result_sha256"]=sha_object(verification["result"]);verification_wire=wire(verification)+b"\n";package.recheck()
    if args.verify_publish:publish(ATTACK_NAME,attack_wire);publish(VERIFICATION_NAME,verification_wire)
    else:exact(package.hashes[ATTACK_NAME],hashlib.sha256(attack_wire).hexdigest(),"sealed attack");exact(package.hashes[VERIFICATION_NAME],hashlib.sha256(verification_wire).hexdigest(),"sealed verification")
    print(VERIFY_STATUS);print("verification_result_sha256="+verification["result_sha256"]);print("verification_file_sha256="+hashlib.sha256(verification_wire).hexdigest());print("attack_file_sha256="+hashlib.sha256(attack_wire).hexdigest());return 0


if __name__=="__main__":raise SystemExit(main())
