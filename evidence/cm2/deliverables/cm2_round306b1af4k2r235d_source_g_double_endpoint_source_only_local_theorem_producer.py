#!/usr/bin/env python3
"""Produce sixteen input-bound source-only endpoint graph/key theorem rows.

Round235 conservatively deferred sixteen rows because dependency-heavy whole-box
interval evaluation made both endpoint factors overwrap.  This producer does
not extrapolate from the already-certified single rows.  It rebuilds both
factors for each deferred row, differentiates them exactly, partitions that
row into four rational (t,p) cells, and proves on every cell that the target
factor excludes zero.  The remaining source factor is the exact boundary
graph (9/25)t=0.  K1 is used only as a zero-credit cross checker; the positive
local conclusion is bound to the explicit finite proof data written here.
"""

from __future__ import annotations

import argparse
import gc
from dataclasses import dataclass
from fractions import Fraction as Q
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
import types
from typing import Any, Final, Mapping


class Blocked(RuntimeError):
    pass


def need(ok: bool, label: str) -> None:
    if not ok:
        raise Blocked(label)


HERE: Final = Path(__file__).parent
PREFIX: Final = "cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_"
LEDGER_NAME: Final = PREFIX + "row_commitment_ledger.jsonl.gz"
RESULT_NAME: Final = PREFIX + "result.json"
RESULT_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.result.v1"
ROW_SCHEMA: Final = "cm2.round306b1af4k2r235d.source-g-double-endpoint-source-only-local-theorem.row.v1"
STATUS: Final = "PASS_16_ROW_SOURCE_ONLY_LOCAL_THEOREM__OLD_R248_R306A_B0_B1G0_AF2_K2I0_K2I1_K2I2_K2I3_K2I4_BINDINGS_SUPERSEDED__FRESH_REFREEZE_REQUIRED__ZERO_GLOBAL_CREDIT"
ROW_CAP: Final = 8_388_608
SQRT_BITS: Final = 128
K1_SCHEMA: Final = "cm2.round306b1af4k1.source-g-semantic-theorem-kernel.v1"
OWNER_RE: Final = re.compile(r"^G\[(-?[0-9]+),(-?[0-9]+)\]$")

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


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def type_strict_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(type_strict_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(type_strict_equal(a, b) for a, b in zip(left, right, strict=True))
    return bool(left == right)


def strict_need(left: Any, right: Any, label: str) -> None:
    need(type_strict_equal(left, right), label)


def duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_number(token: str) -> Any:
    raise Blocked("nonintegral/nonfinite JSON number:" + token)


def strict_decode(raw: bytes, label: str, maximum: int) -> Any:
    need(0 < len(raw) <= maximum, "raw size:" + label)
    need(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "raw encoding:" + label)
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=duplicate_reject,
                           parse_float=reject_number, parse_constant=reject_number)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Blocked("JSON decode:" + label) from exc
    def walk(item: Any) -> None:
        if type(item) is dict:
            for key, child in item.items():
                need(type(key) is str, "key type:" + label); walk(key); walk(child)
        elif type(item) is list:
            for child in item: walk(child)
        elif type(item) is str:
            need("\x00" not in item and not any(0xD800 <= ord(c) <= 0xDFFF for c in item), "string:" + label)
        else:
            need(item is None or type(item) in {bool, int}, "scalar:" + label)
    walk(value)
    return value


def row_wire(row: Any, label: str) -> bytes:
    wire = canonical(row)
    need(len(wire) <= ROW_CAP, "final canonical row cap:" + label)
    return wire


def identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


class HeldPins:
    def __init__(self) -> None:
        self.dirfd = -1
        self.dirstat: os.stat_result | None = None
        self.fds: dict[str, int] = {}

    @staticmethod
    def hash_fd(fd: int) -> str:
        os.lseek(fd, 0, os.SEEK_SET); state = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                return state.hexdigest()
            state.update(chunk)

    def __enter__(self) -> "HeldPins":
        before = os.stat(HERE, follow_symlinks=False)
        need(stat.S_ISDIR(before.st_mode) and not HERE.is_symlink(), "deliverables directory")
        self.dirfd = os.open(HERE, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0))
        self.dirstat = os.fstat(self.dirfd)
        need((before.st_dev, before.st_ino, before.st_mode) == (self.dirstat.st_dev, self.dirstat.st_ino, self.dirstat.st_mode), "directory race")
        try:
            for label, name, size, sha in PINS:
                before_file = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
                need(stat.S_ISREG(before_file.st_mode) and before_file.st_nlink == 1 and before_file.st_size == size, "regular/size/nlink:" + label)
                fd = os.open(name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=self.dirfd)
                opened = os.fstat(fd); need(identity(before_file) == identity(opened), "open race:" + label)
                self.fds[label] = fd
                need(self.hash_fd(fd) == sha and self.hash_fd(fd) == sha, "two-pass pin:" + label)
                need(identity(opened) == identity(os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)), "post-hash path:" + label)
            return self
        except BaseException:
            self.__exit__(None, None, None); raise

    def bytes(self, label: str) -> bytes:
        fd = self.fds[label]; os.lseek(fd, 0, os.SEEK_SET); chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1_048_576)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)

    def load_k1(self) -> types.ModuleType:
        source = self.bytes("K1_SOURCE")
        module = types.ModuleType("_sealed_k1_cross_checker")
        module.__file__ = str(HERE / PINS[9][1]); module.__package__ = ""
        old = sys.modules.get(module.__name__); sys.modules[module.__name__] = module
        try:
            exec(compile(source, module.__file__, "exec"), module.__dict__)
        finally:
            if old is None: sys.modules.pop(module.__name__, None)
            else: sys.modules[module.__name__] = old
        return module

    def final_revalidate(self) -> None:
        need(self.dirstat is not None, "snapshot active")
        now = os.stat(HERE, follow_symlinks=False)
        need((self.dirstat.st_dev, self.dirstat.st_ino, self.dirstat.st_mode) == (now.st_dev, now.st_ino, now.st_mode), "final directory")
        for label, name, size, sha in PINS:
            held = os.fstat(self.fds[label]); path = os.stat(name, dir_fd=self.dirfd, follow_symlinks=False)
            need(identity(held) == identity(path) and held.st_nlink == 1 and held.st_size == size, "final FD/path:" + label)
            need(self.hash_fd(self.fds[label]) == sha, "final hash:" + label)

    def __exit__(self, *_args: Any) -> None:
        for fd in self.fds.values():
            try: os.close(fd)
            except OSError: pass
        self.fds.clear()
        if self.dirfd >= 0:
            try: os.close(self.dirfd)
            except OSError: pass
            self.dirfd = -1


def load_envelope(raw: bytes, schema: str, label: str, maximum: int) -> dict[str, Any]:
    doc = strict_decode(raw, label, maximum)
    need(type(doc) is dict and set(doc) == {"schema", "result", "result_sha256"}, "envelope:" + label)
    strict_need(doc["schema"], schema, "schema:" + label)
    strict_need(doc["result_sha256"], object_sha(doc["result"]), "result digest:" + label)
    need(canonical(doc) + b"\n" == raw, "canonical envelope:" + label)
    return doc


def load_gzip_object(raw: bytes, label: str, compressed_cap: int, plain_cap: int) -> dict[str, Any]:
    need(0 < len(raw) <= compressed_cap, "compressed size:" + label)
    try:
        plain = gzip.decompress(raw)
    except (OSError, EOFError) as exc:
        raise Blocked("gzip:" + label) from exc
    need(0 < len(plain) <= plain_cap, "uncompressed size:" + label)
    doc = strict_decode(plain, label, plain_cap)
    # Exact compressed bytes are held-FD pinned; upstream ledgers use their own
    # frozen serialization rather than this package's canonical JSON encoder.
    need(type(doc) is dict, "gzip object:" + label)
    return doc


def load_direct_object(raw: bytes, label: str, maximum: int) -> dict[str, Any]:
    doc = strict_decode(raw, label, maximum)
    need(type(doc) is dict and raw in {canonical(doc), canonical(doc) + b"\n"}, "canonical direct result:" + label)
    if "result_sha256" in doc:
        body = dict(doc); digest = body.pop("result_sha256")
        strict_need(digest, object_sha(body), "direct result digest:" + label)
    return doc


def closed_row_ref(ordinal: int, row: dict[str, Any], identifier_field: str, label: str) -> list[Any]:
    need(type(row) is dict and type(row.get(identifier_field)) is str and type(row.get("row_sha256")) is str, "closed row shape:" + label)
    body = dict(row); internal = body.pop("row_sha256")
    strict_need(internal, object_sha(body), "closed row digest:" + label)
    return [ordinal, row[identifier_field], hashlib.sha256(row_wire(row, label)).hexdigest(), internal]


def sha_manifest_entries(raw: bytes, label: str) -> dict[str, str]:
    try: text = raw.decode("ascii")
    except UnicodeDecodeError as exc: raise Blocked("manifest encoding:" + label) from exc
    need(text.endswith("\n"), "manifest newline:" + label); out: dict[str, str] = {}
    for line in text.splitlines():
        parts = line.split("  ")
        need(len(parts) == 2 and len(parts[0]) == 64 and all(c in "0123456789abcdef" for c in parts[0]), "manifest syntax:" + label)
        path = parts[1]; name = os.path.basename(path)
        need(path in {name, "deliverables/" + name} and name not in out, "manifest member:" + label)
        out[name] = parts[0]
    return out


def unpack(document: dict[str, Any], table: str) -> list[dict[str, Any]]:
    columns = document["row_column_schemas"][table]
    return [dict(zip(columns, packed, strict=True)) for packed in document[table]]


def index_rows(rows: list[dict[str, Any]], field: str, label: str) -> dict[str, tuple[int, dict[str, Any]]]:
    out: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(rows):
        need(type(row) is dict and type(row.get(field)) is str and row[field] not in out, "row index:" + label)
        row_wire(row, label); out[row[field]] = (ordinal, row)
    return out


def row_ref(ordinal: int, row: dict[str, Any], field: str, label: str) -> list[Any]:
    return [ordinal, row[field], hashlib.sha256(row_wire(row, label)).hexdigest()]


def load_prior_ledger(raw: bytes) -> list[dict[str, Any]]:
    need(0 < len(raw) <= 40_000_000, "prior ledger compressed size")
    try: data = gzip.decompress(raw)
    except (OSError, EOFError) as exc: raise Blocked("prior ledger gzip") from exc
    need(len(data) <= 268_435_456 and gzip.compress(data, compresslevel=9, mtime=0) == raw, "prior canonical gzip")
    need(data.endswith(b"\n"), "prior ledger newline")
    rows = []
    for i, line in enumerate(data.splitlines()):
        need(len(line) <= ROW_CAP, "prior row cap")
        row = strict_decode(line, "prior row", ROW_CAP); need(canonical(row) == line, "prior row canonical")
        strict_need(row["authority_ordinal"], i, "prior ordinal"); rows.append(row)
    strict_need(len(rows), 38_344, "prior row census")
    return rows


def qwire(value: Q | int) -> dict[str, int]:
    q = Q(value)
    return {"numerator": q.numerator, "denominator": q.denominator}


def qread(value: Mapping[str, Any]) -> Q:
    need(type(value) is dict and set(value) == {"numerator", "denominator"}, "rational wire")
    n, d = value["numerator"], value["denominator"]
    need(type(n) is int and type(d) is int and d > 0, "rational types")
    q = Q(n, d); need((q.numerator, q.denominator) == (n, d), "reduced rational")
    return q


def c(value: Q | int) -> dict[str, Any]: return {"op": "CONST_Q", "value": qwire(value)}
def v(name: str) -> dict[str, Any]: return {"op": "VAR", "name": name}
def neg(a: Any) -> dict[str, Any]: return {"op": "NEG", "arg": a}
def add(*args: Any) -> dict[str, Any]: return {"op": "ADD", "args": list(args)}
def sub(a: Any, b: Any) -> dict[str, Any]: return {"op": "SUB", "left": a, "right": b}
def mul(*args: Any) -> dict[str, Any]: return {"op": "MUL", "args": list(args)}
def square(a: Any) -> dict[str, Any]: return {"op": "SQUARE", "arg": a}
def sqrt_positive(a: Any) -> dict[str, Any]: return {"op": "SQRT_POSITIVE", "arg": a}
def div_nonzero(a: Any, b: Any) -> dict[str, Any]: return {"op": "DIV_NONZERO", "left": a, "right": b}


def differentiate(node: Mapping[str, Any], variable: str) -> dict[str, Any]:
    op = node["op"]
    if op == "CONST_Q": return c(0)
    if op == "VAR": return c(1 if node["name"] == variable else 0)
    if op == "NEG": return neg(differentiate(node["arg"], variable))
    if op == "ADD": return add(*(differentiate(a, variable) for a in node["args"]))
    if op == "SUB": return sub(differentiate(node["left"], variable), differentiate(node["right"], variable))
    if op == "MUL":
        return add(*(mul(*(differentiate(a, variable) if i == j else a for j, a in enumerate(node["args"]))) for i in range(len(node["args"]))))
    if op == "SQUARE": return mul(c(2), node["arg"], differentiate(node["arg"], variable))
    if op == "DIV_NONZERO":
        return div_nonzero(sub(mul(differentiate(node["left"], variable), node["right"]),
                               mul(node["left"], differentiate(node["right"], variable))), square(node["right"]))
    if op == "SQRT_POSITIVE": return div_nonzero(differentiate(node["arg"], variable), mul(c(2), node))
    raise Blocked("unsupported derivative op:" + str(op))


@dataclass(frozen=True)
class Interval:
    lower: Q
    upper: Q
    def __post_init__(self) -> None: need(type(self.lower) is Q and type(self.upper) is Q and self.lower <= self.upper, "interval")
    @classmethod
    def point(cls, value: Q | int) -> "Interval":
        q = Q(value); return cls(q, q)
    def neg(self) -> "Interval": return Interval(-self.upper, -self.lower)
    def add(self, other: "Interval") -> "Interval": return Interval(self.lower + other.lower, self.upper + other.upper)
    def sub(self, other: "Interval") -> "Interval": return self.add(other.neg())
    def mul(self, other: "Interval") -> "Interval":
        p = (self.lower * other.lower, self.lower * other.upper, self.upper * other.lower, self.upper * other.upper)
        return Interval(min(p), max(p))
    def square(self) -> "Interval":
        p = (self.lower * self.lower, self.upper * self.upper)
        return Interval(Q(0) if self.lower <= 0 <= self.upper else min(p), max(p))
    def div(self, other: "Interval") -> "Interval":
        need(not other.lower <= 0 <= other.upper, "interval division zero")
        reciprocal = Interval(min(Q(1, other.lower), Q(1, other.upper)), max(Q(1, other.lower), Q(1, other.upper)))
        return self.mul(reciprocal)
    def excludes_zero(self) -> bool: return self.upper < 0 or self.lower > 0
    def wire(self) -> dict[str, Any]: return {"lower": qwire(self.lower), "upper": qwire(self.upper)}


def sqrt_interval(value: Interval) -> Interval:
    need(value.lower > 0, "sqrt domain positive")
    scale = 1 << SQRT_BITS
    def floor(q: Q) -> Q: return Q(isqrt((q.numerator * scale * scale) // q.denominator), scale)
    lo, hi = floor(value.lower), floor(value.upper)
    if hi * hi != value.upper: hi += Q(1, scale)
    need(lo * lo <= value.lower and hi * hi >= value.upper, "sqrt outward")
    return Interval(lo, hi)


def eval_interval(node: Mapping[str, Any], env: Mapping[str, Interval]) -> Interval:
    op = node["op"]
    if op == "CONST_Q": return Interval.point(qread(node["value"]))
    if op == "VAR": need(node["name"] in env, "bound variable"); return env[node["name"]]
    if op == "NEG": return eval_interval(node["arg"], env).neg()
    if op == "ADD":
        out = Interval.point(0)
        for a in node["args"]: out = out.add(eval_interval(a, env))
        return out
    if op == "SUB": return eval_interval(node["left"], env).sub(eval_interval(node["right"], env))
    if op == "MUL":
        out = Interval.point(1)
        for a in node["args"]: out = out.mul(eval_interval(a, env))
        return out
    if op == "SQUARE": return eval_interval(node["arg"], env).square()
    if op == "DIV_NONZERO": return eval_interval(node["left"], env).div(eval_interval(node["right"], env))
    if op == "SQRT_POSITIVE": return sqrt_interval(eval_interval(node["arg"], env))
    raise Blocked("unsupported interval op:" + str(op))


def factor_asts(endpoint: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    reason = endpoint["reason_labels"][0]; kind, axis, wall_text = reason.split(":")
    strict_need(kind, "wall_endpoint_or_count_transition", "endpoint reason kind")
    wall = int(wall_text); strict_need(wall, 0, "only wall zero")
    chart = endpoint["chart"]; need(chart in {"G:E", "G:W", "G:N", "G:S"}, "source chart")
    owner_match = OWNER_RE.fullmatch(endpoint["owner_target"]); need(owner_match is not None, "G owner target")
    ix, iy = Q(int(owner_match.group(1))), Q(int(owner_match.group(2)))
    t, p = v("t"), v("p"); rn = sqrt_positive(sub(c(1), square(t))); rp = sqrt_positive(sub(c(1), square(p)))
    cell = chart[-1]
    if cell == "E": nx, ny = rn, t
    elif cell == "W": nx, ny = neg(rn), t
    elif cell == "N": nx, ny = t, rn
    else: nx, ny = t, neg(rn)
    ux = sub(mul(rp, nx), mul(p, ny)); uy = add(mul(rp, ny), mul(p, nx))
    radius = Q(9, 25); sx, sy = mul(c(radius), nx), mul(c(radius), ny)
    dx, dy = sub(c(ix), sx), sub(c(iy), sy)
    transverse = add(neg(mul(uy, dx)), mul(ux, dy))
    radical = sqrt_positive(sub(c(radius * radius), square(transverse)))
    hit_x = add(c(ix), neg(mul(radical, ux)), mul(transverse, uy))
    hit_y = add(c(iy), neg(mul(radical, uy)), neg(mul(transverse, ux)))
    return sub(sx if axis == "X" else sy, c(wall)), sub(hit_x if axis == "X" else hit_y, c(wall))


def box_wire(bounds: list[tuple[Q, Q]], closures: list[tuple[bool, bool]]) -> dict[str, Any]:
    return {"wire_id": "RATIONAL_INTERVAL_BOX_V1", "coordinate_parameter": "TPS",
            "axes": [{"axis": axis, "lower": qwire(lo), "lower_closed": lc,
                      "upper": qwire(hi), "upper_closed": uc}
                     for axis, (lo, hi), (lc, uc) in zip("tps", bounds, closures, strict=True)]}


def proof_boxes(endpoint: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    t0, t1, p0, p1, s0, s1 = map(Q, endpoint["box"]); tm, pm = (t0 + t1) / 2, (p0 + p1) / 2
    parent = box_wire([(t0, t1), (p0, p1), (s0, s1)], [(True, True)] * 3)
    cells = []
    for ti, pi in product(range(2), repeat=2):
        ta, tb = (t0, tm) if ti == 0 else (tm, t1); pa, pb = (p0, pm) if pi == 0 else (pm, p1)
        cells.append(box_wire([(ta, tb), (pa, pb), (s0, s1)],
                              [(True, False) if ti == 0 else (True, True),
                               (True, False) if pi == 0 else (True, True), (True, True)]))
    return parent, cells


def box_env(wire: dict[str, Any]) -> dict[str, Interval]:
    return {row["axis"]: Interval(qread(row["lower"]), qread(row["upper"])) for row in wire["axes"]}


def enumerate_patterns() -> tuple[tuple[str, ...], ...]:
    output: list[tuple[str, ...]] = []
    for xc in range(5):
        for yc in range(5):
            total = xc + yc
            for xd in ((0,) if xc == 0 else (-1, 1)):
                for yd in ((0,) if yc == 0 else (-1, 1)):
                    for positions in combinations(range(total), xc):
                        xset = set(positions); xt = "X+" if xd > 0 else "X-"; yt = "Y+" if yd > 0 else "Y-"
                        output.append(tuple(xt if i in xset else yt for i in range(total)))
    patterns = tuple(output)
    need(len(patterns) == len(set(patterns)) == 985, "pattern census")
    return patterns


def signature(row: dict[str, Any]) -> dict[str, Any]:
    return {"source_chart": row["chart"], "target_lift": row["owner_target"],
            "ordered_integer_wall_events": row["ordered_integer_wall_events"], "signed_wall_word": row["signed_wall_word"],
            "roof": row["roof"], "outgoing_cell": row["outgoing_cell"], "target_chart": row["target_chart"],
            "official_key_row": row["official_key_row"], "official_key_ordinal": row["official_key_ordinal"], "official_key_id": row["official_key_id"]}


def exact_key_from_base(chart: str, owner: str, pattern: tuple[str, ...], base: dict[str, Any], patterns: tuple[tuple[str, ...], ...]) -> dict[str, Any]:
    empty_index = patterns.index(()); base_ordinal = base["official_key_ordinal"]
    need(type(base_ordinal) is int and base_ordinal % 985 == empty_index, "base key pair anchor")
    pair_index = base_ordinal // 985; need(0 <= pair_index < 448, "pair index")
    ordinal = pair_index * 985 + patterns.index(pattern); row = [chart, owner, list(pattern), len(pattern) + 1]
    return {"row": row, "ordinal": ordinal, "identifier": f"gate5-word:{ordinal:06d}:{object_sha(row)}"}


def with_event(base: dict[str, Any], event: list[Any], chart: str, owner: str, patterns: tuple[tuple[str, ...], ...]) -> dict[str, Any]:
    out = dict(base); out["ordered_integer_wall_events"] = [event]; out["signed_wall_word"] = [event[0]]; out["roof"] = 2
    key = exact_key_from_base(chart, owner, (event[0],), base, patterns)
    out["official_key_row"], out["official_key_ordinal"], out["official_key_id"] = key["row"], key["ordinal"], key["identifier"]
    return out


def gzip_rows(rows: list[dict[str, Any]]) -> bytes:
    return gzip.compress(b"".join(canonical(row) + b"\n" for row in rows), compresslevel=9, mtime=0)


def table_summary(total: int, selected: list[tuple[int, dict[str, Any]]], field: str, label: str) -> dict[str, Any]:
    selected = sorted(selected); refs = [row_ref(i, row, field, label) for i, row in selected]
    return {"source_row_count": total, "selected_row_count": len(selected), "id_field": field,
            "ordered_selected_row_refs_sha256": object_sha(refs), "ordered_selected_rows_sha256": object_sha([row for _, row in selected]),
            "source_ordinal_sequence_sha256": object_sha([i for i, _ in selected])}


def downstream_invalidation(snapshot: HeldPins, authority_rows: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """Bind the local theorem to every stale R248/R306A/B0/B1G0 identity it invalidates.

    This is deliberately an invalidation ledger, not a corrected universe.  The
    arithmetic below is a removal-only/no-split projection and cannot acquire
    credit before a fresh source rebuild and forward/reverse DSU replay.
    """
    interfaces = {row["canonical_input_commitment"]["R220_interface"][1] for row in authority_rows}
    strict_need(len(interfaces), 16, "downstream interface census")
    pin = {label: {"filename": name, "size": size, "sha256": sha} for label, name, size, sha in PINS}

    b1_result = load_direct_object(snapshot.bytes("B1G0_RESULT"), "B1G0 result", 10_000)
    r306_result = load_direct_object(snapshot.bytes("R306A_RESULT"), "R306A result", 20_000)
    b0_result = load_direct_object(snapshot.bytes("B0_RESULT"), "B0 result", 20_000)
    af2_result = load_direct_object(snapshot.bytes("AF2_RESULT"), "AF2 result", 10_000)
    i3_result = load_direct_object(snapshot.bytes("K2I3_RESULT"), "K2I3 result", 20_000)
    i4_result = load_direct_object(snapshot.bytes("K2I4_RESULT"), "K2I4 result", 50_000)
    i0_result = load_direct_object(snapshot.bytes("K2I0_RESULT"), "K2I0 result", 20_000)
    i1_result = load_direct_object(snapshot.bytes("K2I1_RESULT"), "K2I1 result", 20_000)
    i2_result = load_direct_object(snapshot.bytes("K2I2_RESULT"), "K2I2 result", 20_000)
    for lane in ("I0", "I1", "I2", "I3"):
        manifest = sha_manifest_entries(snapshot.bytes("K2" + lane + "_MANIFEST"), "K2" + lane)
        strict_need(manifest[pin["K2" + lane + "_RESULT"]["filename"]], pin["K2" + lane + "_RESULT"]["sha256"], "lane result manifest binding:" + lane)
        strict_need(i4_result["upstream_package_manifest_sha256"][lane], pin["K2" + lane + "_MANIFEST"]["sha256"], "I4 lane manifest binding:" + lane)
    i4_manifest = sha_manifest_entries(snapshot.bytes("K2I4_MANIFEST"), "K2I4")
    strict_need(i4_manifest[pin["K2I4_RESULT"]["filename"]], pin["K2I4_RESULT"]["sha256"], "I4 result manifest binding")
    strict_need(i4_manifest[pin["K2I4_MEMBER"]["filename"]], pin["K2I4_MEMBER"]["sha256"], "I4 member manifest binding")
    strict_need((b1_result["audit"]["graph_sheet_join_count"], b1_result["audit"]["graph_side_join_count"],
                 b1_result["audit"]["distinct_B0_member_backbinding_count"], b1_result["audit"]["physical_incidence_count"]),
                (38_624, 76_848, 115_456, 115_472), "old B1G0 census")
    strict_need((r306_result["member_universe"]["member_count"], r306_result["fresh_forward_application"]["edge_rows"],
                 r306_result["fresh_forward_application"]["component_count"], r306_result["fresh_reverse_application"]["partition_sha256"]),
                (564_492, 478_718, 92_688, r306_result["fresh_forward_application"]["partition_sha256"]), "old R306A census")
    strict_need((b0_result["member_universe"]["member_count"], b0_result["member_universe"]["component_count"],
                 b0_result["member_universe"]["cross_component_pair_count"]),
                (564_492, 92_688, 158_838_084_354), "old B0 census")
    strict_need((af2_result["member_count"], af2_result["coarse_partition"]["G2a_graph_sheet_members"],
                 af2_result["G2b"]["reference_count"], af2_result["G2b"]["distinct_member_count"]),
                (564_492, 38_624, 76_848, 76_832), "old AF2 census")
    strict_need((i3_result["exact_census"]["G2_distinct_members"], i3_result["exact_census"]["current_one_to_one_representation_candidates"],
                 i3_result["exact_census"]["physical_incidence_references_pending"], i3_result["exact_census"]["duplicate_reference_members"]),
                (115_456, 115_456, 115_472, 16), "old K2I3 census")
    strict_need((i4_result["exact_census"]["member_count"], i4_result["exact_census"]["representation_count"]),
                (564_492, 611_904), "old K2I4 census")
    strict_need((i0_result["exact_census"]["R292_member_count"], i1_result["exact_census"]["R2_member_count"],
                 i2_result["exact_census"]["preserved_member_count"], i2_result["exact_census"]["non_graph_member_count"]),
                (9_404, 295_336, 126_468, 17_828), "old I0/I1/I2 census")

    r236_doc = load_envelope(snapshot.bytes("R236_CERT"), "cm2.round236.source-g-wall-residual-closure-and-root-key-partition.v1", "R236 cert", 3_000_000)
    r236_all = r236_doc["result"]["double_endpoint_partition_rows"]
    r236_selected = [(i, row) for i, row in enumerate(r236_all) if row["Round220_split_interface_id"] in interfaces]
    strict_need((len(r236_all), len(r236_selected)), (16, 16), "R236 double rows")
    r236_by_interface = {row["Round220_split_interface_id"]: (i, row) for i, row in r236_selected}
    need(len(r236_by_interface) == 16, "unique R236 interfaces")
    r236_ids = {row["double_endpoint_partition_row_id"] for _, row in r236_selected}
    del r236_doc; gc.collect()

    r248_doc = load_envelope(snapshot.bytes("R248_CERT"), "cm2.round248.source-g-wall-finite-key-retained-quotient.v1", "R248 cert", 220_000_000)
    r248_result = r248_doc["result"]
    r248_sheet_all = r248_result["formal_wall_half_open_sheet_owner_ledger"]["rows"]
    r248_bulk_all = r248_result["formal_wall_positive_volume_bulk_ledger"]["rows"]
    r248_sheets = [(i, row) for i, row in enumerate(r248_sheet_all)
                   if row["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_GRAPH_SHEET" and row["source_partition_row_id"] in r236_ids]
    r248_bulk = [(i, row) for i, row in enumerate(r248_bulk_all)
                 if row["source_partition_kind"] == "ROUND236_DOUBLE_ENDPOINT_ARRANGEMENT_BRANCH" and row["source_partition_row_id"] in r236_ids]
    strict_need((len(r248_sheets), len(r248_bulk)), (32, 48), "R248 double sheet/bulk rows")
    r248_sheet_map: dict[tuple[str, str], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in r248_sheets:
        closed_row_ref(ordinal, row, "wall_sheet_node_id", "R248 sheet")
        key = (row["Round220_split_interface_id"], row["endpoint_factor"])
        need(key not in r248_sheet_map, "unique R248 sheet key"); r248_sheet_map[key] = (ordinal, row)
    r248_bulk_by_sha: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in r248_bulk:
        closed_row_ref(ordinal, row, "wall_bulk_node_id", "R248 bulk")
        need(row["row_sha256"] not in r248_bulk_by_sha, "unique R248 bulk digest")
        r248_bulk_by_sha[row["row_sha256"]] = (ordinal, row)
    strict_need({sum(1 for _, row in r248_bulk if row["Round220_split_interface_id"] == interface) for interface in interfaces}, {3}, "three R248 bulk branches per interface")
    del r248_result, r248_doc, r248_sheet_all, r248_bulk_all; gc.collect()

    graph_doc = load_gzip_object(snapshot.bytes("B1G0_GRAPH"), "B1G0 graph", 15_000_000, 80_000_000)
    strict_need((graph_doc["schema"], graph_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.graph-ledger.v1", 38_624), "B1G0 graph header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        strict_need(graph_doc[field], b1_result["output_ledgers"]["graph"][field], "B1G0 graph commitment:" + field)
    b1_graphs = [(i, row) for i, row in enumerate(graph_doc["graph_source_inventory_rows"])
                 if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH" and row["Round220_split_interface_id"] in interfaces]
    strict_need(len(b1_graphs), 32, "B1G0 double graph rows")
    b1_graph_map: dict[tuple[str, str], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in b1_graphs:
        closed_row_ref(ordinal, row, "Round306B1G0_graph_source_inventory_row_id", "B1G0 graph")
        key = (row["Round220_split_interface_id"], row["endpoint_factor"])
        need(key not in b1_graph_map, "unique B1G0 graph key"); b1_graph_map[key] = (ordinal, row)
        r236_row = r236_by_interface[key[0]][1]
        strict_need((row["source_row_id"], row["source_row_sha256"], row["source_file_sha256"]),
                    (r236_row["double_endpoint_partition_row_id"], hashlib.sha256(row_wire(r236_row, "R236 source row")).hexdigest(), PINS[18][3]),
                    "R236/B1G0 graph join")
    del graph_doc; gc.collect()

    sheet_doc = load_gzip_object(snapshot.bytes("B1G0_SHEET"), "B1G0 sheet", 20_000_000, 90_000_000)
    strict_need((sheet_doc["schema"], sheet_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.sheet-ledger.v1", 38_624), "B1G0 sheet header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        strict_need(sheet_doc[field], b1_result["output_ledgers"]["sheet"][field], "B1G0 sheet commitment:" + field)
    b1_sheets = [(i, row) for i, row in enumerate(sheet_doc["graph_sheet_join_rows"])
                 if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH" and row["Round220_split_interface_id"] in interfaces]
    strict_need(len(b1_sheets), 32, "B1G0 double sheet joins")
    b1_sheet_map: dict[tuple[str, str], tuple[int, dict[str, Any]]] = {}
    for ordinal, row in b1_sheets:
        closed_row_ref(ordinal, row, "Round306B1G0_graph_sheet_join_row_id", "B1G0 sheet")
        key = (row["Round220_split_interface_id"], row["endpoint_factor"])
        need(key not in b1_sheet_map, "unique B1G0 sheet key"); b1_sheet_map[key] = (ordinal, row)
        source = r248_sheet_map[key][1]
        strict_need((row["sheet_member_id"], row["sheet_source_row_sha256"], row["sheet_source_file_sha256"]),
                    (source["wall_sheet_node_id"], source["row_sha256"], PINS[19][3]), "R248/B1G0 sheet join")
        strict_need((row["graph_id"], row["graph_source_inventory_row_id"]),
                    (b1_graph_map[key][1]["graph_id"], b1_graph_map[key][1]["Round306B1G0_graph_source_inventory_row_id"]),
                    "B1G0 graph/sheet join")
    del sheet_doc; gc.collect()

    side_doc = load_gzip_object(snapshot.bytes("B1G0_SIDE"), "B1G0 side", 35_000_000, 180_000_000)
    strict_need((side_doc["schema"], side_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.side-ledger.v1", 76_848), "B1G0 side header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        strict_need(side_doc[field], b1_result["output_ledgers"]["side"][field], "B1G0 side commitment:" + field)
    b1_sides = [(i, row) for i, row in enumerate(side_doc["graph_side_join_rows"])
                if row["graph_family"] == "R236_DOUBLE_ENDPOINT_GRAPH" and row["Round220_split_interface_id"] in interfaces]
    strict_need(len(b1_sides), 64, "B1G0 double side refs")
    sides_by_interface: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for ordinal, row in b1_sides:
        closed_row_ref(ordinal, row, "Round306B1G0_graph_side_join_row_id", "B1G0 side")
        need(row["side_source_row_sha256"] in r248_bulk_by_sha, "B1G0 side to R248 bulk")
        strict_need(row["side_member_id"], r248_bulk_by_sha[row["side_source_row_sha256"]][1]["wall_bulk_node_id"], "B1G0/R248 side member")
        sides_by_interface.setdefault(row["Round220_split_interface_id"], []).append((ordinal, row))
    del side_doc; gc.collect()

    row_bindings: dict[str, dict[str, Any]] = {}
    invalid_sheet_ids: list[str] = []
    invalid_side_ids: list[str] = []
    shared_side_ids: list[str] = []
    all_target_feature_ids: set[str] = set()
    for interface in sorted(interfaces):
        roles = {row["side_role"]: (ordinal, row) for ordinal, row in sides_by_interface[interface]}
        strict_need(set(roles), {"target:SAME_SIGN_EVENT_ABSENT", "target:POSITIVE_TO_NEGATIVE",
                                 "source:SAME_SIGN_EVENT_ABSENT", "source:NEGATIVE_TO_POSITIVE"}, "double side roles")
        target_same = roles["target:SAME_SIGN_EVENT_ABSENT"]
        source_same = roles["source:SAME_SIGN_EVENT_ABSENT"]
        target_only = roles["target:POSITIVE_TO_NEGATIVE"]
        strict_need(target_same[1]["side_member_id"], source_same[1]["side_member_id"], "shared same-sign member")
        need(target_only[1]["side_member_id"] != target_same[1]["side_member_id"], "target-only member distinct")
        target_sheet = b1_sheet_map[(interface, "target")]
        invalid_sheet_ids.append(target_sheet[1]["sheet_member_id"])
        invalid_side_ids.append(target_only[1]["side_member_id"])
        shared_side_ids.append(target_same[1]["side_member_id"])
        all_target_feature_ids.update((target_sheet[1]["sheet_member_id"], target_same[1]["side_member_id"], target_only[1]["side_member_id"]))
        row_bindings[interface] = {
            "R236_double_endpoint_partition_row": row_ref(*r236_by_interface[interface], "double_endpoint_partition_row_id", "R236 double"),
            "B1G0_invalid_target_graph_inventory_row": closed_row_ref(*b1_graph_map[(interface, "target")], "Round306B1G0_graph_source_inventory_row_id", "B1G0 target graph"),
            "R248_target_sheet_owner_row": closed_row_ref(*r248_sheet_map[(interface, "target")], "wall_sheet_node_id", "R248 target sheet"),
            "B1G0_target_sheet_join_row": closed_row_ref(*target_sheet, "Round306B1G0_graph_sheet_join_row_id", "B1G0 target sheet"),
            "B1G0_target_shared_side_row": closed_row_ref(*target_same, "Round306B1G0_graph_side_join_row_id", "B1G0 shared target side"),
            "B1G0_source_shared_side_row": closed_row_ref(*source_same, "Round306B1G0_graph_side_join_row_id", "B1G0 shared source side"),
            "B1G0_target_only_side_row": closed_row_ref(*target_only, "Round306B1G0_graph_side_join_row_id", "B1G0 target-only side"),
            "R248_target_only_bulk_row": closed_row_ref(*r248_bulk_by_sha[target_only[1]["side_source_row_sha256"]], "wall_bulk_node_id", "R248 target-only bulk"),
            "invalid_TARGET_SHEET_member_id": target_sheet[1]["sheet_member_id"],
            "surviving_shared_side_member_id": target_same[1]["side_member_id"],
            "invalid_TARGET_ONLY_SIDE_member_id": target_only[1]["side_member_id"],
        }
    strict_need((len(set(invalid_sheet_ids)), len(set(invalid_side_ids)), len(set(shared_side_ids)), len(all_target_feature_ids)), (16, 16, 16, 48), "target feature identity census")

    member_doc = load_gzip_object(snapshot.bytes("B1G0_MEMBER"), "B1G0 member", 40_000_000, 210_000_000)
    strict_need((member_doc["schema"], member_doc["row_count"]),
                ("cm2.round306b1g0.source-g-graph-source-inventory-and-join-freeze.v1.member-ledger.v1", 115_456), "B1G0 member header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        strict_need(member_doc[field], b1_result["output_ledgers"]["member"][field], "B1G0 member commitment:" + field)
    backbinding: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(member_doc["b0_member_backbinding_rows"]):
        if row["member_id"] in all_target_feature_ids:
            closed_row_ref(ordinal, row, "Round306B1G0_B0_member_backbinding_row_id", "B1G0 member")
            need(row["member_id"] not in backbinding, "unique B1G0 backbinding"); backbinding[row["member_id"]] = (ordinal, row)
    strict_need(len(backbinding), 48, "target feature backbinding census")
    del member_doc; gc.collect()

    invalid_ids = set(invalid_sheet_ids) | set(invalid_side_ids)
    r306_doc = load_gzip_object(snapshot.bytes("R306A_MEMBER"), "R306A member", 120_000_000, 540_000_000)
    strict_need((r306_doc["schema"], r306_doc["row_count"]),
                ("cm2.round306a.source-g-r305b-fresh-legal-component-dsu-rebuild.v1.member-ledger.v1", 564_492), "R306A member header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        strict_need(r306_doc[field], r306_result["output_ledgers"]["member"][field], "R306A member commitment:" + field)
    r306_rows = r306_doc["fresh_member_component_rows"]
    r306_target_features: dict[str, tuple[int, dict[str, Any]]] = {}
    for ordinal, row in enumerate(r306_rows):
        if row["registry_occurrence_id"] in all_target_feature_ids:
            closed_row_ref(ordinal, row, "Round306A_fresh_member_component_row_id", "R306A member")
            need(row["registry_occurrence_id"] not in r306_target_features, "unique target-feature R306A member")
            r306_target_features[row["registry_occurrence_id"]] = (ordinal, row)
    strict_need(len(r306_target_features), 48, "target-feature R306A member census")
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
    strict_need(({(row["required_disposition"], row["old_member_count"], row["invalid_member_count"]) for row in root_dispositions}, len(root_dispositions)),
                ({("DELETE_ROOT", 1, 1), ("REKEY_ROOT", 2_878, 4)}, 20), "root disposition census")
    del r306_doc, r306_rows; gc.collect()

    component_removed: dict[str, list[str]] = {}
    for member_id, (_, row) in r306_invalid.items(): component_removed.setdefault(row["final_component_id"], []).append(member_id)
    b0_component_doc = load_gzip_object(snapshot.bytes("B0_COMPONENT"), "B0 component", 20_000_000, 100_000_000)
    strict_need((b0_component_doc["schema"], b0_component_doc["row_count"]),
                ("cm2.round306b0.source-g-r306a-universe-support-source-freeze.v2.component-ledger.v1", 92_688), "B0 component header")
    for field in ("ledger_sha256", "row_hashes_sha256", "row_ids_sha256", "rows_sha256"):
        strict_need(b0_component_doc[field], b0_result["output_ledgers"]["component"][field], "B0 component commitment:" + field)
    selected_components: dict[str, tuple[int, dict[str, Any]]] = {}
    old_sizes: list[int] = []; projected_sizes: list[int] = []
    for ordinal, row in enumerate(b0_component_doc["component_census_rows"]):
        size = row["member_count"]; old_sizes.append(size)
        removed_count = len(component_removed.get(row["Round306A_component_id"], []))
        if removed_count:
            closed_row_ref(ordinal, row, "Round306B0_component_census_row_id", "B0 component")
            selected_components[row["Round306A_component_id"]] = (ordinal, row)
        if size > removed_count: projected_sizes.append(size - removed_count)
    strict_need((len(selected_components), sorted((pair[1]["member_count"], len(component_removed[component])) for component, pair in selected_components.items())),
                (20, [(1, 1)] * 16 + [(5_442, 4)] * 2 + [(5_490, 4)] * 2), "affected old components")
    choose2 = lambda n: n * (n - 1) // 2
    old_cross = choose2(sum(old_sizes)) - sum(choose2(n) for n in old_sizes)
    projected_cross = choose2(sum(projected_sizes)) - sum(choose2(n) for n in projected_sizes)
    strict_need((sum(old_sizes), len(old_sizes), old_cross, sum(projected_sizes), len(projected_sizes), projected_cross),
                (564_492, 92_688, 158_838_084_354, 564_460, 92_672, 158_820_108_554), "removal-only component projection")
    component_dispositions = []
    for component in sorted(selected_components):
        ordinal, row = selected_components[component]; removed = sorted(component_removed[component])
        component_dispositions.append({"old_component_id": component,
                                       "old_component_row": closed_row_ref(ordinal, row, "Round306B0_component_census_row_id", "B0 component"),
                                       "old_member_count": row["member_count"], "invalid_member_ids": removed,
                                       "invalid_member_count": len(removed),
                                       "no_split_removal_only_projected_member_count": row["member_count"] - len(removed),
                                       "projection_disposition": "VANISHES" if row["member_count"] == len(removed) else "RETAINED_BUT_REPLAY_REQUIRED"})
    del b0_component_doc; gc.collect()

    rekey_component_ids = {row["old_component_id"] for row in component_dispositions if row["projection_disposition"] == "RETAINED_BUT_REPLAY_REQUIRED"}
    strict_need(len(rekey_component_ids), 4, "four rekey components")
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
                    need(line.endswith(b"\n") and len(line) <= ROW_CAP + 1, "I4 member JSONL framing")
                    row = strict_decode(line[:-1], "I4 member row", ROW_CAP)
                    if row["Round306A_component_id"] not in rekey_component_ids: continue
                    closed_row_ref(i4_row_count - 1, row, "member_id", "I4 affected member")
                    member_id = row["member_id"]; need(member_id not in affected_ids, "unique I4 affected member"); affected_ids.add(member_id)
                    family, lane = row["coarse_family"], row["source_lane"]
                    old_family_hist[family] = old_family_hist.get(family, 0) + 1
                    old_lane_hist[lane] = old_lane_hist.get(lane, 0) + 1
                    affected_i4_refs.append([member_id, row["row_sha256"], row["canonical_input_commitment_sha256"]])
                    if member_id not in invalid_ids:
                        surviving_family_hist[family] = surviving_family_hist.get(family, 0) + 1
                        surviving_lane_hist[lane] = surviving_lane_hist.get(lane, 0) + 1
    except (OSError, EOFError) as exc:
        raise Blocked("I4 member stream") from exc
    strict_need((i4_row_count, uncompressed_size, uncompressed_hash.hexdigest()),
                (i4_result["ledgers"]["member"]["row_count"], i4_result["ledgers"]["member"]["uncompressed_jsonl_size"],
                 i4_result["ledgers"]["member"]["uncompressed_jsonl_sha256"]), "I4 complete JSONL stream")
    strict_need((len(affected_ids), old_family_hist, old_lane_hist, surviving_family_hist, surviving_lane_hist),
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
                    "affected_member_ids_sha256":object_sha(sorted(affected_ids)),
                    "ordered_I4_affected_member_refs_sha256":object_sha(affected_i4_refs),
                    "I0_I1_I2_I3_component_bindings_superseded":True,
                    "source_lane_manifests_bound_through_I4_rows":True,
                    "fresh_I0_I1_I2_I3_I4_replay_required":True,
                    "formal_credit":0}

    root_by_id = {row["old_base_root_id"]: row for row in root_dispositions}
    for interface, binding in row_bindings.items():
        sheet_id, side_id, shared_id = binding["invalid_TARGET_SHEET_member_id"], binding["invalid_TARGET_ONLY_SIDE_member_id"], binding["surviving_shared_side_member_id"]
        sheet_member = r306_invalid[sheet_id]; side_member = r306_invalid[side_id]; shared_member = r306_target_features[shared_id]
        strict_need(root_by_id[sheet_member[1]["base_root_id"]]["required_disposition"], "REKEY_ROOT", "target sheet rekeys old root")
        strict_need(root_by_id[side_member[1]["base_root_id"]]["required_disposition"], "DELETE_ROOT", "target-only side deletes singleton root")
        for member_id in (sheet_id, side_id, shared_id):
            strict_need(backbinding[member_id][1]["Round306A_component_id"],
                        r306_target_features[member_id][1]["final_component_id"],
                        "member/component backbinding")
        binding.update({
            "B1G0_target_sheet_backbinding": closed_row_ref(*backbinding[sheet_id], "Round306B1G0_B0_member_backbinding_row_id", "B1G0 target sheet backbinding"),
            "B1G0_shared_survivor_backbinding": closed_row_ref(*backbinding[shared_id], "Round306B1G0_B0_member_backbinding_row_id", "B1G0 shared survivor backbinding"),
            "B1G0_target_only_side_backbinding": closed_row_ref(*backbinding[side_id], "Round306B1G0_B0_member_backbinding_row_id", "B1G0 target-only side backbinding"),
            "Round306A_invalid_TARGET_SHEET_member_row": closed_row_ref(*sheet_member, "Round306A_fresh_member_component_row_id", "R306A target sheet member"),
            "Round306A_invalid_TARGET_ONLY_SIDE_member_row": closed_row_ref(*side_member, "Round306A_fresh_member_component_row_id", "R306A target-only side member"),
            "Round306A_surviving_shared_side_member_row": closed_row_ref(*shared_member, "Round306A_fresh_member_component_row_id", "R306A shared survivor member"),
            "old_TARGET_SHEET_base_root_disposition": root_by_id[sheet_member[1]["base_root_id"]],
            "old_TARGET_ONLY_SIDE_base_root_disposition": root_by_id[side_member[1]["base_root_id"]],
            "old_freeze_invalidated": True,
            "corrected_universe_or_DSU_credit": 0,
        })

    invalid_sheet_ids = sorted(invalid_sheet_ids); invalid_side_ids = sorted(invalid_side_ids)
    invalid_union = sorted(invalid_sheet_ids + invalid_side_ids)
    strict_need((object_sha(invalid_sheet_ids), object_sha(invalid_side_ids), object_sha(invalid_union)),
                ("0163d9c564b74b8cff5a9d5f309a25037d461b3874ca4805161cf639aeec73f4",
                 "f6f5acf3a89bb0a09f83b7f0ac783019fddc5b36ca7d8df833d6c052cc20e957",
                 "9c95eae730d5a033d65dadf2d27828b9876325e943049dd788ac1ed740687e52"), "invalid member commitments")
    summary = {
        "old_freeze_invalidated": True,
        "invalidation_semantics": "TARGET_FACTOR_ZERO_SET_IS_EMPTY__OLD_TARGET_SHEET_AND_TARGET_ONLY_SIDE_IDENTITIES_CANNOT_SURVIVE",
        "invalid_member_sets": {
            "TARGET_SHEET": {"count": 16, "sorted_member_ids": invalid_sheet_ids, "sorted_member_ids_sha256": object_sha(invalid_sheet_ids)},
            "TARGET_ONLY_SIDE": {"count": 16, "sorted_member_ids": invalid_side_ids, "sorted_member_ids_sha256": object_sha(invalid_side_ids)},
            "UNION": {"count": 32, "sorted_member_ids": invalid_union, "sorted_member_ids_sha256": object_sha(invalid_union)},
            "shared_same_sign_side_members_survive_from_source_reference_count": 16,
            "removed_target_side_references_to_shared_survivors_count": 16,
        },
        "old_Round306A_base_root_dispositions": {"affected_root_count": 20, "DELETE_ROOT_count": 16, "REKEY_ROOT_count": 4,
                                                  "rows": root_dispositions, "rows_sha256": object_sha(root_dispositions)},
        "old_B0_component_impacts": {"affected_component_count": 20, "vanishing_singleton_component_count": 16,
                                      "retained_old_component_count": 4, "rows": component_dispositions,
                                      "rows_sha256": object_sha(component_dispositions)},
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


def build(snapshot: HeldPins) -> tuple[dict[str, Any], bytes]:
    r179_doc = load_envelope(snapshot.bytes("R179_ROWS"), "cm2.round179.source-g-residual-tube-arrangement-rows.v1", "R179 rows", 140_000_000)
    r220_doc = load_envelope(snapshot.bytes("R220_CERT"), "cm2.round220.source-g-round179-resolved-child-boundary-atlas.v1", "R220 cert", 310_000_000)
    r234_doc = load_envelope(snapshot.bytes("R234_CERT"), "cm2.round234.source-g-wall-endpoint-order-depth6-materialization.v1", "R234 cert", 55_000_000)
    r235_doc = load_envelope(snapshot.bytes("R235_CERT"), "cm2.round235.source-g-single-endpoint-graph-word-key-partition.v1", "R235 cert", 70_000_000)
    prior_result = load_envelope(snapshot.bytes("K2R235_RESULT"), "cm2.round306b1af4k2r235.source-g-single-endpoint-graph-word-key-local-authority.result.v1", "K2R235 result", 10_000)
    strict_need(prior_result["result"]["authority_ledger"]["sha256"], PINS[17][3], "prior ledger result pin")
    prior_rows = load_prior_ledger(snapshot.bytes("K2R235_LEDGER")); prior_index = {row["Round234_frontier_row_id"]: row for row in prior_rows}
    need(len(prior_index) == 38_344, "prior frontier index")

    k1_result = strict_decode(snapshot.bytes("K1_RESULT"), "K1 result", 10_000)
    strict_need(k1_result["decision"], "GO_ONLY_ZERO_CREDIT", "K1 decision")
    strict_need(k1_result["method_boundary"]["independent_mathematical_implementation"], False, "K1 is cross checker only")
    strict_need(k1_result["formal_credit"], {"B1A":0,"B2":0,"CM2":0,"D02":0,"fibre":0,"global_disposition":0,"maximality":0,"normalized_support":0,"pair_routing":0,"physical_incidence":0,"representation_cover":0,"transition":0}, "K1 zero credit")
    k1 = snapshot.load_k1()

    r179 = r179_doc["result"]; resolved = unpack(r179, "resolved_3d_child_rows"); retained = unpack(r179, "retained_3d_child_rows")
    resolved_index = index_rows(resolved, "row_id", "R179 resolved"); retained_index = index_rows(retained, "row_id", "R179 retained")
    t220 = r220_doc["result"]["coordinate_boundary_atlas"]["tables"]["one_step_split_interface_rows"]
    interfaces = [dict(zip(t220["columns"], packed, strict=True)) for packed in t220["rows"]]
    interface_index = index_rows(interfaces, "split_interface_id", "R220 interface")
    r234 = r234_doc["result"]; frontier = r234["depth6_frontier_rows"]; frontier_index = index_rows(frontier, "frontier_row_id", "R234 frontier")
    released_by_interface: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for ordinal, row in enumerate(r234["resolved_descendant_rows"]):
        released_by_interface.setdefault(row["Round220_split_interface_id"], []).append((ordinal, row))
    old_double = r235_doc["result"]["double_endpoint_deferred_rows"]
    strict_need(len(old_double), 16, "double endpoint census")

    double_frontier_ids = {row["Round234_frontier_row_id"] for row in old_double}
    double_endpoints = [frontier_index[i][1] for i in double_frontier_ids]
    ids = {row["Round220_split_interface_id"] for row in double_endpoints}; origins = {row["origin_row_id"] for row in double_endpoints}; retained_ids = {row["Round179_retained_child_row_id"] for row in double_endpoints}
    r231 = load_envelope(snapshot.bytes("R231_CERT"), "cm2.round231.source-g-outgoing-seam-depth6-materialization.v1", "R231 cert", 100_000_000)["result"]
    r231_rows = r231["depth6_frontier_rows"] + r231["resolved_descendant_rows"] + r231["root_summary_rows"]
    r233 = load_envelope(snapshot.bytes("R233_CERT"), "cm2.round233.source-g-outgoing-seam-parametric-graph-key-partition.v1", "R233 cert", 10_000_000)["result"]
    r233_rows = r233["parametric_graph_key_partition_rows"]
    def joins(rows: list[dict[str, Any]]) -> dict[str, int]:
        return {"interface": len(ids & {row.get("Round220_split_interface_id") for row in rows}),
                "origin": len(origins & {row.get("origin_row_id") for row in rows}),
                "retained": len(retained_ids & {row.get("Round179_retained_child_row_id") for row in rows})}
    anti_join = {"R209_formal_row_authority_count": 0, "R231": joins(r231_rows), "R233": joins(r233_rows)}
    strict_need(anti_join, {"R209_formal_row_authority_count":0,"R231":{"interface":0,"origin":0,"retained":0},"R233":{"interface":0,"origin":0,"retained":0}}, "outgoing-channel anti-joins")

    registry = strict_decode(snapshot.bytes("GATE5_REGISTRY"), "Gate5 registry", 20_000)
    immutable = registry["result"]["immutable_candidate_key_registry"]
    strict_need((immutable["retained_chart_target_pair_count"], immutable["crossing_pattern_count_per_pair"], immutable["candidate_return_word_key_count"]), (448, 985, 441_280), "Gate5 registry census")
    patterns = enumerate_patterns(); pattern_hist: dict[int, int] = {}
    for pat in patterns: pattern_hist[len(pat)] = pattern_hist.get(len(pat), 0) + 1
    strict_need(pattern_hist, {0:1,1:4,2:12,3:28,4:60,5:120,6:200,7:280,8:280}, "pattern histogram")

    authority_rows: list[dict[str, Any]] = []; selected_endpoints = []; selected_interfaces = []; selected_siblings = []; selected_retained = []; selected_released: dict[str, tuple[int, dict[str, Any]]] = {}
    target_sign_hist: dict[str, int] = {}; token_hist: dict[str, int] = {}; key_ids: set[str] = set(); k1_digests: set[str] = set()
    for old_ordinal, deferred in enumerate(old_double):
        frontier_ordinal, endpoint = frontier_index[deferred["Round234_frontier_row_id"]]
        strict_need(deferred["active_factors"], ["source", "target"], "old double active factors")
        interface_ordinal, interface = interface_index[endpoint["Round220_split_interface_id"]]
        sibling_id = interface["lower_child_row_id"] if interface["lower_child_kind"] == "RESOLVED" else interface["upper_child_row_id"]
        sibling_ordinal, sibling = resolved_index[sibling_id]; retained_ordinal, retained_row = retained_index[endpoint["Round179_retained_child_row_id"]]
        released = released_by_interface.get(interface["split_interface_id"], [])
        prior = prior_index[endpoint["frontier_row_id"]]
        strict_need((prior["kind"], prior["local_single_endpoint_graph_word_key_partition_authority_credit"]), ("DOUBLE_ENDPOINT_TWO_FACTOR_ARRANGEMENT_DEFERRED_NO_AUTHORITY", 0), "prior double zero")

        source_ast, target_ast = factor_asts(endpoint); source_dt = differentiate(source_ast, "t"); target_dp = differentiate(target_ast, "p")
        parent, cells = proof_boxes(endpoint); cell_receipts = []
        for cell_index, cell in enumerate(cells):
            env = box_env(cell); target_iv = eval_interval(target_ast, env); dp_iv = eval_interval(target_dp, env)
            need(target_iv.excludes_zero() and dp_iv.excludes_zero(), "target/derivative exclusion")
            target_sign = "STRICT_POSITIVE" if target_iv.lower > 0 else "STRICT_NEGATIVE"
            dp_sign = "STRICT_POSITIVE" if dp_iv.lower > 0 else "STRICT_NEGATIVE"
            cell_receipts.append({"cell_index": cell_index, "cell": cell, "excluded_factor": "TARGET",
                                  "target_factor_interval": target_iv.wire(), "target_factor_sign": target_sign,
                                  "target_p_derivative_interval": dp_iv.wire(), "target_p_derivative_sign": dp_sign})
        row_signs = {item["target_factor_sign"] for item in cell_receipts}; need(len(row_signs) == 1, "one target sign per row")
        fixed_sign = next(iter(row_signs)); target_sign_hist[fixed_sign] = target_sign_hist.get(fixed_sign, 0) + 1
        dp_signs = {item["target_p_derivative_sign"] for item in cell_receipts}; need(len(dp_signs) == 1, "one target derivative sign")

        cert = {"wire_id":"CODIM2_INTERSECTION_DISPOSITION_CERT_V1", "disposition":"EMPTY", "domain_box":parent,
                "cover_cells":cells, "source_factor_ast":source_ast, "target_factor_ast":target_ast,
                "per_cell_excluded_factor":["TARGET"] * 4}
        k1_receipt = k1.check_codim2_empty(cert)
        strict_need(k1_receipt["formal_theorem_credit"], 0, "K1 no theorem credit")
        k1_digests.add(k1_receipt["check_digest_sha256"])
        source_env = box_env(parent); dt_iv = eval_interval(source_dt, source_env)
        strict_need(dt_iv, Interval.point(Q(9, 25)), "exact source t derivative")
        t0, t1 = map(Q, endpoint["box"][:2]); need((t0 == 0) ^ (t1 == 0), "source zero is exactly one t face")
        zero_face = "LOWER" if t0 == 0 else "UPPER"

        reason = endpoint["reason_labels"][0]; axis = reason.split(":")[1]
        token = axis + ("+" if fixed_sign == "STRICT_POSITIVE" else "-"); token_hist[token] = token_hist.get(token, 0) + 1
        event = [token, 0]; base = signature(sibling)
        strict_need((base["ordered_integer_wall_events"], base["signed_wall_word"], base["roof"]), ([], [], 1), "empty base signature")
        strict_need(base["official_key_row"], [endpoint["chart"], endpoint["owner_target"], [], 1], "base official row")
        absent, present = base, with_event(base, event, endpoint["chart"], endpoint["owner_target"], patterns)
        allowed = {object_sha(absent), object_sha(present)}
        need(all(object_sha(row["local_return_signature"]) in allowed for _, row in released), "released signature allowed")
        key_ids.update((absent["official_key_id"], present["official_key_id"]))

        input_commitment = {
            "R235_deferred": row_ref(old_ordinal, deferred, "deferred_row_id", "R235 deferred"),
            "R234_endpoint": row_ref(frontier_ordinal, endpoint, "frontier_row_id", "R234 endpoint"),
            "R220_interface": row_ref(interface_ordinal, interface, "split_interface_id", "R220 interface"),
            "R179_retained": row_ref(retained_ordinal, retained_row, "row_id", "R179 retained"),
            "R179_resolved_sibling": row_ref(sibling_ordinal, sibling, "row_id", "R179 sibling"),
            "R234_released": [row_ref(i, row, "materialized_row_id", "R234 released") for i, row in released],
            "K2R235_prior_authority_row": [prior["authority_ordinal"], prior["authority_row_id"], hashlib.sha256(row_wire(prior, "K2R235 prior row")).hexdigest()],
            "frozen_input_pin_set_sha256": object_sha([[label, name, size, sha] for label, name, size, sha in PINS]),
        }
        theorem = {
            "source_factor_ast": source_ast, "source_t_derivative_ast": source_dt,
            "source_t_derivative_exact_interval": dt_iv.wire(), "source_zero_face": zero_face,
            "source_zero_set": "EXACT_FACE_GRAPH_t_EQUALS_0", "source_graph_dimension": 2,
            "target_factor_ast": target_ast, "target_p_derivative_ast": target_dp,
            "rational_cover": {"domain_box": parent, "cell_count": 4, "cells": cell_receipts},
            "target_factor_fixed_sign": fixed_sign, "target_p_derivative_fixed_sign": next(iter(dp_signs)),
            "target_zero_set_on_domain": "EMPTY", "source_target_codim2_intersection": "EMPTY",
            "k1_zero_credit_cross_checker_receipt": k1_receipt,
        }
        conclusion = {
            "active_endpoint_factor": "source", "excluded_old_active_factor": "target",
            "transition_event": event, "transition_event_order_position": "STRICT_FIRST_VACUOUS_EMPTY_BASE_WORD",
            "event_absent_signature": absent, "event_present_signature": present,
            "distinct_side_exact_key_count": 2, "local_source_only_endpoint_graph_key_authority_credit": 1,
        }
        core = {
            "schema": ROW_SCHEMA, "authority_ordinal": len(authority_rows),
            "authority_row_id": "k2r235d:" + endpoint["frontier_row_id"], "Round234_frontier_row_id": endpoint["frontier_row_id"],
            "deferred_row_id": deferred["deferred_row_id"],
            "source_R235_deferred_row_sha256": input_commitment["R235_deferred"][2],
            "R234_released_descendants": input_commitment["R234_released"],
            "canonical_input_commitment": input_commitment, "canonical_input_commitment_sha256": object_sha(input_commitment),
            "outgoing_channel_anti_join": {"R209":"NO_FORMAL_ROW_LEDGER", "R231":False, "R233":False},
            "local_theorem": theorem, "local_conclusion": conclusion,
            "local_source_only_endpoint_graph_key_authority_credit": 1,
            "normalized_full_support_credit":0, "physical_incidence_equivalence_credit":0, "representation_pullback_credit":0,
            "G2_authority_credit":0, "B1A_credit":0, "B2_credit":0, "maximality_credit":0, "fibre_credit":0, "CM2_credit":0,
        }
        core["conclusion_sha256"] = object_sha({"input": input_commitment, "theorem": theorem, "conclusion": conclusion,
                                                  "nonpromotion": [0,0,0,0,0,0,0,0,0]})
        row_wire(core, "authority row"); authority_rows.append(core)
        selected_endpoints.append((frontier_ordinal, endpoint)); selected_interfaces.append((interface_ordinal, interface)); selected_siblings.append((sibling_ordinal, sibling)); selected_retained.append((retained_ordinal, retained_row))
        for item in released: selected_released[item[1]["materialized_row_id"]] = item

    strict_need((len(authority_rows), len(k1_digests), sum(len(row["local_theorem"]["rational_cover"]["cells"]) for row in authority_rows)), (16, 16, 64), "theorem row/cell/digest census")
    strict_need(target_sign_hist, {"STRICT_NEGATIVE":8,"STRICT_POSITIVE":8}, "target sign histogram")
    strict_need(token_hist, {"X+":4,"X-":4,"Y+":4,"Y-":4}, "token histogram")
    selected_interfaces = sorted({row[1]["split_interface_id"]: row for row in selected_interfaces}.values())
    selected_siblings = sorted({row[1]["row_id"]: row for row in selected_siblings}.values())
    selected_retained = sorted({row[1]["row_id"]: row for row in selected_retained}.values())
    selected_table_commitments = {
        "R235_DOUBLE": table_summary(len(old_double), list(enumerate(old_double)), "deferred_row_id", "R235 deferred"),
        "R234_ENDPOINT": table_summary(len(frontier), selected_endpoints, "frontier_row_id", "R234 endpoint"),
        "R220_INTERFACE": table_summary(len(interfaces), selected_interfaces, "split_interface_id", "R220 interface"),
        "R179_RETAINED": table_summary(len(retained), selected_retained, "row_id", "R179 retained"),
        "R179_RESOLVED_SIBLING": table_summary(len(resolved), selected_siblings, "row_id", "R179 sibling"),
        "R234_RELEASED": table_summary(len(r234["resolved_descendant_rows"]), list(selected_released.values()), "materialized_row_id", "R234 released"),
    }
    # The downstream joins include a 564,492-row ledger.  Release the large
    # local reconstruction documents before loading that independent freeze.
    del r179_doc, r220_doc, r234_doc, r235_doc, prior_result, prior_rows, prior_index
    del r179, resolved, retained, resolved_index, retained_index, t220, interfaces, interface_index
    del r234, frontier, frontier_index, released_by_interface, old_double
    del r231, r231_rows, r233, r233_rows, registry, immutable
    gc.collect()
    downstream_summary, downstream_rows = downstream_invalidation(snapshot, authority_rows)
    for row in authority_rows:
        interface = row["canonical_input_commitment"]["R220_interface"][1]
        binding = downstream_rows[interface]
        row["downstream_invalidation"] = binding
        row["conclusion_sha256"] = object_sha({"input": row["canonical_input_commitment"],
                                                  "theorem": row["local_theorem"],
                                                  "conclusion": row["local_conclusion"],
                                                  "downstream_invalidation": binding,
                                                  "nonpromotion": [0,0,0,0,0,0,0,0,0]})
        row_wire(row, "authority row with downstream invalidation")
    ledger_wire = gzip_rows(authority_rows); ledger_sha = hashlib.sha256(ledger_wire).hexdigest()
    result = {
        "status": STATUS,
        "authority_scope": {"positive_authority":"16_INPUT_BOUND_LOCAL_SOURCE_ONLY_ENDPOINT_GRAPH_AND_OFFICIAL_KEY_ROWS",
                            "K1_is_zero_credit_cross_checker_only":True, "no_extrapolation_from_single_rows":True,
                            "outer_envelope_is_full_support":False, "inner_witness_is_full_support":False,
                            "local_graph_key_is_normalized_support":False, "local_graph_key_is_G2_authority":False},
        "census": {"old_double_endpoint_rows":16, "old_active_factor_instances":32, "target_factor_empty_rows":16,
                   "source_only_endpoint_graph_rows":16, "rational_cover_cells":64, "target_factor_exclusion_cells":64,
                   "source_exact_t_derivative_rows":16, "K1_distinct_cross_checker_digest_count":16,
                   "target_factor_sign_histogram":target_sign_hist, "transition_token_histogram":token_hist,
                   "distinct_local_exact_key_count":len(key_ids), "selected_released_descendant_count":len(selected_released)},
        "candidate_input_audit": {"R209_R231_R233_are_not_positive_inputs":True, "exact_join_counts":anti_join,
                                  "R231_R233_outgoing_channel_cannot_be_reused_for_endpoint_rows":True,
                                  "sufficient_positive_input_chain":["R179_ROWS","R220_CERT","R234_CERT","R235_CERT","K2R235_LEDGER","GATE5_REGISTRY"],
                                  "downstream_invalidation_input_chain":["R236_CERT","R248_CERT","B1G0_GRAPH","B1G0_SHEET","B1G0_SIDE","B1G0_MEMBER","R306A_MEMBER","B0_COMPONENT","AF2_RESULT","K2I0_MANIFEST","K2I0_RESULT","K2I1_MANIFEST","K2I1_RESULT","K2I2_MANIFEST","K2I2_RESULT","K2I3_MANIFEST","K2I3_RESULT","K2I4_MANIFEST","K2I4_MEMBER","K2I4_RESULT"],
                                  "K1_cross_checker_target_sha256":PINS[9][3]},
        "selected_table_commitments": selected_table_commitments,
        "downstream_invalidation": downstream_summary,
        "frozen_input_pins": [[label, name, size, sha] for label, name, size, sha in PINS],
        "authority_ledger": {"filename":LEDGER_NAME, "compression":"gzip-mtime-zero", "row_schema":ROW_SCHEMA,
                             "row_count":16, "sha256":ledger_sha,
                             "ordered_row_sha256_sequence_sha256":object_sha([hashlib.sha256(canonical(row)).hexdigest() for row in authority_rows]),
                             "ordered_conclusion_sha256_sequence_sha256":object_sha([row["conclusion_sha256"] for row in authority_rows])},
        "strict_nonpromotion": {"normalized_full_support_credit":0,"physical_incidence_equivalence_credit":0,
                                "representation_pullback_credit":0,"G2_authority_credit":0,"B1A_credit":0,"B2_credit":0,
                                "maximality_credit":0,"fibre_credit":0,"CM2":"NO-GO_FOR_CLAIM"},
        "required_next": {"old_10832_R234_released_union_is_unchanged_but_no_longer_sufficient_to_preserve_old_universe":True,
                          "apply_16_DELETE_ROOT_and_4_REKEY_ROOT_dispositions_then_regenerate_R248":True,
                          "fresh_forward_reverse_478718_edge_Round306A_DSU_and_B0_refreeze":"REQUIRED",
                          "replay_B1G0_AF2_K2I0_K2I1_K2I2_K2I3_K2I4":"REQUIRED",
                          "physical_support_incidence_equivalence_and_representation_pullback":"BLOCKED",
                          "B1A_and_B2":"NOT_AUTHORIZED"},
    }
    snapshot.final_revalidate()
    return result, ledger_wire


def write_once(directory: Path, name: str, data: bytes) -> None:
    resolved = directory.resolve(strict=True); info = os.stat(resolved, follow_symlinks=False)
    need(stat.S_ISDIR(info.st_mode) and not directory.is_symlink(), "output directory")
    path = resolved / name
    if path.exists():
        st = path.lstat(); need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and path.read_bytes() == data, "existing output mismatch:" + name); return
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
    finally: os.close(fd)
    st = path.lstat(); need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1 and path.read_bytes() == data, "published output:" + name)


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B execution required")
    parser = argparse.ArgumentParser(description=__doc__); mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--produce", action="store_true"); mode.add_argument("--no-write", action="store_true")
    parser.add_argument("--output-directory", type=Path, default=HERE); args = parser.parse_args()
    with HeldPins() as snapshot: result, ledger_wire = build(snapshot)
    document = {"schema":RESULT_SCHEMA, "result":result, "result_sha256":object_sha(result)}; result_wire = canonical(document) + b"\n"
    if args.produce:
        write_once(args.output_directory, LEDGER_NAME, ledger_wire); write_once(args.output_directory, RESULT_NAME, result_wire)
    print(STATUS); print("result_sha256=" + document["result_sha256"]); print("result_file_sha256=" + hashlib.sha256(result_wire).hexdigest()); print("ledger_sha256=" + hashlib.sha256(ledger_wire).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
