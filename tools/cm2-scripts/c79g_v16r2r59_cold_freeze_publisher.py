#!/usr/bin/env python3
"""One-shot r59 exact8 -> manifest -> outer-last publisher.

This process is the only writer in the static phase.  It first runs the
read-only r59 guard, then holds every exact8 descriptor while changing the
three source members to 0444, creates the manifest and outer receipt with
O_EXCL/O_RDWR, and terminally replays the same descriptors.  It never imports
or executes a candidate and never writes credit, runtime, or C53 authority.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r59"
PREV = "v16r2r58"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
GUARD = ROOT / "scripts/c79g_v16r2r59_cold_freeze_guard.py"
MANIFEST_REL = f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER_REL = f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json"
MANIFEST = ROOT / MANIFEST_REL
OUTER = ROOT / OUTER_REL
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_FILE_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT_SHA = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"


@dataclass(frozen=True)
class Pin:
    relative: str
    file_sha: str
    object_sha: str | None
    mode: int


EXACT8: tuple[Pin, ...] = (
    Pin(f"deliverables/{BASE}_v14_runtime_registry_shape_drift_rejection_supersession_receipt_v1.json",
        "aa4323027e2313f8a2eda0d6ffc039a537afe342d496d1f75cd73fcd47446c01",
        "93689e62ae36f405f045a769f4dc6f6e6fd83a16605d08299d5c3397ad657e2e", 0o444),
    Pin(f"deliverables/{BASE}_schema_{TAG}.json",
        "f10bd33759b184c0695f9beb710914635fbda779bbc27037b6703dc0a808a676", None, 0o444),
    Pin(f"deliverables/{BASE}_contract_{TAG}.json",
        "e93ca9b5e2e64d48de6d77e698756ed4afee749501ffdf651aaee57b9ee50c7d",
        "a28dbb0dcf703f72e9a60d7295efea7c7b0acfdf11d676de664d6c67fc088c60", 0o444),
    Pin(f"deliverables/{BASE}_{TAG}_semantic_source.py",
        "1a8d3b17aab88351890992fe45a6b17c2194d8a5dc4f3ad25f8ecd894538dc32", None, 0o664),
    Pin(f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "2f0452b1dd4cb24ed058285802f6bd6f3854798a79289832cbef03b1789473cd", None, 0o664),
    Pin(f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "2c8b9d20c4af440a58837b05404be5a0a8e3f665a1a06e6aa7260a1a2ee21d2f",
        "91c4f18aa4aed1e40d5f22c055515dc16d01d232cd9819418f64a021dcec8ca2", 0o444),
    Pin(f"deliverables/{BASE}_static_audit_{TAG}.json",
        "41b0c0f0a6b40df1f2688c56fcf5222e0cebe87e46157c93b45fe4b4bffe3093",
        "61d42e9291c8e10e186d8fc3c95583e7776744dc9c910ddc3318ae5827f1fd36", 0o444),
    Pin(f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
        "323bced6d33ec437b8a175f82c557bcbd9ce1831411d698643b1dce1537ade80", None, 0o664),
)

OUTER_KEYS = frozenset({
    "schema", "status", "effective_checkpoint_object_sha256",
    "exact8_ordered_entries", "cold_launch_manifest", "cold_launcher",
    "all_exact8_regular_0444_nlink1_and_held_for_runtime",
    "outer_published_after_exact8_manifest", "runtime_entry_must_be_cold_launcher",
    "sole_external_static_file_anchor_is_launcher_sha256", "declared_external_tcb",
    "formal_global_closure_credit", "D02_unlock", "runtime_executed_during_static_freeze",
    "object_sha256",
})


@dataclass
class Held:
    pin: Pin
    path: Path
    fd: int
    raw: bytes
    initial: os.stat_result
    final: os.stat_result | None = None


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def ident(st: os.stat_result) -> tuple[int, int, int, int]:
    return st.st_dev, st.st_ino, st.st_size, st.st_nlink


def fail(message: str) -> None:
    raise RuntimeError(message)


def absent(path: Path) -> None:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return
    fail(f"append-only target already exists:{path.relative_to(ROOT)}")


def stable_fd(fd: int, path: Path) -> tuple[bytes, os.stat_result]:
    before = os.fstat(fd)
    named = os.lstat(path)
    if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
            ident(before) != ident(named)):
        fail(f"unstable:{path}")
    os.lseek(fd, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    while True:
        block = os.read(fd, 1 << 20)
        if not block:
            break
        chunks.append(block)
    os.lseek(fd, 0, os.SEEK_SET)
    after = os.fstat(fd)
    named_after = os.lstat(path)
    raw = b"".join(chunks)
    if (ident(before) != ident(after) or ident(before) != ident(named_after) or
            len(raw) != before.st_size):
        fail(f"identity drift:{path}")
    return raw, after


def strict_json(raw: bytes, label: str) -> Any:
    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                fail(f"duplicate JSON key:{label}:{key}")
            out[key] = value
        return out
    return json.loads(raw.decode("utf-8"), object_pairs_hook=hook,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def c53_snapshot() -> tuple[bytes, str]:
    fd = os.open(C53, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
    try:
        raw, st = stable_fd(fd, C53)
    finally:
        os.close(fd)
    value = strict_json(raw, "C53")
    if (st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o444 or
            sha(raw) != C53_FILE_SHA or not isinstance(value, dict) or
            value.get("authority_seal_object_sha256") != C53_OBJECT_SHA):
        fail("C53 pin/mode/object")
    return raw, sha(raw)


def tagged_pyc() -> list[str]:
    return [str(p.relative_to(ROOT)) for p in ROOT.rglob("*.pyc") if TAG in str(p)]


def tagged_runtime() -> list[str]:
    runtime = ROOT / ".cm2-runtime"
    if not runtime.exists():
        return []
    return [str(p.relative_to(ROOT)) for p in runtime.rglob("*") if TAG in str(p)]


def run_guard() -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": "1"})
    proc = subprocess.run(["/usr/bin/python3", "-I", "-B", "-S", str(GUARD)],
                          cwd=str(ROOT), env=env, capture_output=True, check=False,
                          timeout=240)
    if proc.returncode != 0:
        fail(f"guard rc={proc.returncode}:{proc.stderr.decode('utf-8','replace')[-600:]}")
    value = strict_json(proc.stdout, "guard")
    if (not isinstance(value, dict) or
            value.get("status") != "PREFLIGHT_PASS_R59_PINS_PENDING_MANIFEST_OUTER_ABSENT__ZERO_CREDIT" or
            value.get("check_count") != 9 or value.get("failed_check_count") != 0 or
            value.get("read_only") is not True or value.get("formal_global_closure_credit") != 0 or
            value.get("D02_unlock") is not False or value.get("runtime_authorized") is not False or
            value.get("manifest_created") is not False or value.get("outer_created") is not False):
        fail("guard predicate")
    expected = [{"path": p.relative, "file_sha256": p.file_sha,
                 "object_sha256": p.object_sha, "mode": p.mode} for p in EXACT8]
    if value.get("exact8") != expected:
        fail("guard exact8 mismatch")
    return value, proc.stdout


def open_exact8() -> list[Held]:
    held: list[Held] = []
    try:
        for pin in EXACT8:
            path = ROOT / pin.relative
            fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0))
            try:
                raw, st = stable_fd(fd, path)
                if (sha(raw) != pin.file_sha or stat.S_IMODE(st.st_mode) != pin.mode or
                        st.st_nlink != 1):
                    fail(f"exact8 pin/mode:{pin.relative}")
                if pin.object_sha is not None:
                    value = strict_json(raw, pin.relative)
                    body = dict(value); claim = body.pop("object_sha256", None)
                    if claim != pin.object_sha or sha(canonical(body)) != claim:
                        fail(f"exact8 object closure:{pin.relative}")
                held.append(Held(pin, path, fd, raw, st))
            except BaseException:
                os.close(fd)
                raise
        if len({ident(x.initial) for x in held}) != len(EXACT8):
            fail("exact8 identity collision")
        if len({x.initial.st_dev for x in held}) != 1:
            fail("exact8 device split")
        return held
    except BaseException:
        for item in reversed(held):
            os.close(item.fd)
        raise


def freeze_exact8(held: list[Held], out_fd: int) -> None:
    changed = 0
    for item in held:
        os.fsync(item.fd)
        current = os.fstat(item.fd)
        mode = stat.S_IMODE(current.st_mode)
        if mode == 0o664:
            os.fchmod(item.fd, 0o444)
            changed += 1
        elif mode != 0o444:
            fail(f"unexpected initial mode:{item.pin.relative}")
        os.fsync(item.fd)
        os.fsync(out_fd)
        raw, final = stable_fd(item.fd, item.path)
        if raw != item.raw or sha(raw) != item.pin.file_sha or stat.S_IMODE(final.st_mode) != 0o444:
            fail(f"byte/mode drift during freeze:{item.pin.relative}")
        item.final = final
    if changed != 3:
        fail(f"expected three source freezes, got {changed}")
    if any(item.final is None or item.final.st_nlink != 1 for item in held):
        fail("terminal exact8 mode/nlink")


def publication_bytes(held: list[Held]) -> tuple[bytes, bytes, str, str, list[dict[str, str]]]:
    entries = [{"path": item.pin.relative, "file_sha256": item.pin.file_sha} for item in held]
    manifest = b"".join(f"{e['file_sha256']}  {e['path']}\n".encode("ascii") for e in entries)
    manifest_sha = sha(manifest)
    body: dict[str, Any] = {
        "schema": "cm2.round306c79g.true-global-no-producer-consumer.cold-launch-outer-receipt.v16r2",
        "status": "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__RUNTIME_DEFERRED",
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {"path": MANIFEST_REL, "file_sha256": manifest_sha, "ordered_entry_count": 8},
        "cold_launcher": {"path": EXACT8[-1].relative, "file_sha256": EXACT8[-1].file_sha},
        "all_exact8_regular_0444_nlink1_and_held_for_runtime": True,
        "outer_published_after_exact8_manifest": True,
        "runtime_entry_must_be_cold_launcher": True,
        "sole_external_static_file_anchor_is_launcher_sha256": True,
        "declared_external_tcb": ["EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
                                   "PYTHON3_ISOLATED_INTERPRETER",
                                   "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS"],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_executed_during_static_freeze": False,
    }
    if frozenset(body) != OUTER_KEYS - {"object_sha256"}:
        fail("launcher-native outer key set")
    body["object_sha256"] = sha(canonical(body))
    outer = canonical(body) + b"\n"
    return manifest, outer, manifest_sha, body["object_sha256"], entries


def create_exclusive(out_fd: int, relative: str, raw: bytes) -> tuple[int, os.stat_result]:
    if Path(relative).parent.as_posix() != "deliverables":
        fail("publication path not direct deliverables")
    name = Path(relative).name
    fd = os.open(name, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0), 0o444, dir_fd=out_fd)
    try:
        view = memoryview(raw)
        pos = 0
        while pos < len(view):
            n = os.write(fd, view[pos:])
            if n <= 0:
                fail(f"short write:{relative}")
            pos += n
        os.fsync(fd)
        os.fchmod(fd, 0o444)
        os.fsync(fd)
        os.fsync(out_fd)
        state = os.fstat(fd)
        named = os.stat(name, dir_fd=out_fd, follow_symlinks=False)
        if (not stat.S_ISREG(state.st_mode) or state.st_nlink != 1 or
                stat.S_IMODE(state.st_mode) != 0o444 or ident(state) != ident(named)):
            fail(f"published identity:{relative}")
        # O_RDWR is deliberate: replay the exact same open file description.
        os.lseek(fd, 0, os.SEEK_SET)
        if os.read(fd, len(raw) + 1) != raw:
            fail(f"published byte replay:{relative}")
        os.lseek(fd, 0, os.SEEK_SET)
        return fd, state
    except BaseException:
        os.close(fd)
        raise


def chronology(held: list[Held], manifest: os.stat_result, outer: os.stat_result) -> dict[str, bool]:
    exact = [x.final for x in held if x.final is not None]
    exact_internal = all(x.st_mtime_ns <= x.st_ctime_ns for x in exact)
    manifest_internal = manifest.st_mtime_ns <= manifest.st_ctime_ns
    outer_internal = outer.st_mtime_ns <= outer.st_ctime_ns
    exact_before_manifest = max(max(x.st_mtime_ns, x.st_ctime_ns) for x in exact) < manifest.st_mtime_ns
    manifest_before_outer = manifest.st_ctime_ns < outer.st_mtime_ns
    return {
        "all_exact8_mtime_not_after_final_ctime": exact_internal,
        "manifest_mtime_not_after_final_ctime": manifest_internal,
        "outer_mtime_not_after_final_ctime": outer_internal,
        "max_exact8_final_mtime_ctime_before_manifest_mtime": exact_before_manifest,
        "manifest_final_ctime_before_outer_mtime": manifest_before_outer,
        "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology": (
            exact_internal and manifest_internal and outer_internal and
            exact_before_manifest and manifest_before_outer),
    }


def terminal_replay(held: list[Held], manifest_fd: int, outer_fd: int,
                    manifest_raw: bytes, outer_raw: bytes,
                    manifest_state: os.stat_result, outer_state: os.stat_result,
                    entries: list[dict[str, str]]) -> None:
    for item in held:
        raw, state = stable_fd(item.fd, item.path)
        if (raw != item.raw or sha(raw) != item.pin.file_sha or
                stat.S_IMODE(state.st_mode) != 0o444 or state.st_nlink != 1 or
                item.final is None or ident(state) != ident(item.final)):
            fail(f"exact8 terminal replay:{item.pin.relative}")
    for fd, path, expected, expected_state in ((manifest_fd, MANIFEST, manifest_raw, manifest_state),
                                                (outer_fd, OUTER, outer_raw, outer_state)):
        raw, state = stable_fd(fd, path)
        if (raw != expected or stat.S_IMODE(state.st_mode) != 0o444 or
                state.st_nlink != 1 or ident(state) != ident(expected_state)):
            fail(f"publication terminal replay:{path.name}")
    if manifest_raw.decode("ascii").splitlines() != [f"{e['file_sha256']}  {e['path']}" for e in entries]:
        fail("manifest ordered replay")
    value = strict_json(outer_raw, "r59 outer")
    if not isinstance(value, dict) or frozenset(value) != OUTER_KEYS:
        fail("outer key replay")
    body = dict(value)
    claim = body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canonical(body)) != claim:
        fail("outer object closure replay")
    if (value.get("effective_checkpoint_object_sha256") != CHECKPOINT or
            value.get("formal_global_closure_credit") != 0 or
            value.get("D02_unlock") is not False or
            value.get("runtime_executed_during_static_freeze") is not False or
            "successor_checkpoint_object_sha256" in value):
        fail("outer zero-credit/current-checkpoint replay")


def main() -> int:
    held: list[Held] = []
    manifest_fd = -1
    outer_fd = -1
    manifest_created = False
    outer_created = False
    try:
        guard, guard_raw = run_guard()
        absent(MANIFEST); absent(OUTER)
        if tagged_pyc() or tagged_runtime():
            fail("r59 pyc/runtime residue before freeze")
        c53_before, c53_before_sha = c53_snapshot()
        out_fd = os.open(OUT, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
                         getattr(os, "O_NOFOLLOW", 0))
        try:
            held = open_exact8()
            freeze_exact8(held, out_fd)
            absent(MANIFEST); absent(OUTER)
            c53_now, c53_now_sha = c53_snapshot()
            if c53_now != c53_before or c53_now_sha != c53_before_sha:
                fail("C53 changed before namespace publication")
            manifest_raw, outer_raw, manifest_sha, outer_object_sha, entries = publication_bytes(held)
            manifest_fd, manifest_state = create_exclusive(out_fd, MANIFEST_REL, manifest_raw)
            manifest_created = True
            absent(OUTER)
            outer_fd, outer_state = create_exclusive(out_fd, OUTER_REL, outer_raw)
            outer_created = True
            chrono = chronology(held, manifest_state, outer_state)
            if not all(chrono.values()):
                fail("physical publication chronology")
            terminal_replay(held, manifest_fd, outer_fd, manifest_raw, outer_raw,
                            manifest_state, outer_state, entries)
            c53_after, c53_after_sha = c53_snapshot()
            if c53_after != c53_before or c53_after_sha != c53_before_sha:
                fail("C53 changed after publication")
            if tagged_pyc() or tagged_runtime():
                fail("r59 pyc/runtime residue after freeze")
            report: dict[str, Any] = {
                "schema": f"cm2.c79g.{TAG}.cold-freeze-publisher.v1",
                "status": "TERMINAL_EXACT10_HELD_REPLAY_PASS__FROZEN_MANIFEST_OUTER_LAST__RUNTIME_NOT_EXECUTED",
                "successor_suffix": TAG, "predecessor_suffix": PREV,
                "ordered_exact10": [x.pin.relative for x in held] + [MANIFEST_REL, OUTER_REL],
                "exact8_file_sha256": {x.pin.relative: x.pin.file_sha for x in held},
                "exact8_terminal_mode": "0444", "source_freeze_count": 3,
                "manifest_file_sha256": manifest_sha, "outer_file_sha256": sha(outer_raw),
                "outer_object_sha256": outer_object_sha,
                "guard_report_sha256": sha(guard_raw), "guard_status": guard.get("status"),
                "guard_check_count": guard.get("check_count"),
                "guard_failed_check_count": guard.get("failed_check_count"),
                "C53_authority_head_sha256_before_after": c53_before_sha, "C53_unchanged": True,
                "chronology": chrono, "manifest_O_EXCL_outer_last_O_EXCL": True,
                "manifest_created": True, "outer_created": True,
                "runtime_authority_writes": False, "candidate_execution_count": 0,
                "formal_global_closure_credit": 0, "D02_unlock": False,
                "runtime_authorized": False, "normative_137_runtime_execution_observed": False,
                "pyc_absent": True,
            }
            report["object_sha256"] = sha(canonical(report))
            print(json.dumps(report, sort_keys=True, separators=(",", ":")))
            return 0
        finally:
            if outer_fd >= 0:
                os.close(outer_fd)
            if manifest_fd >= 0:
                os.close(manifest_fd)
            for item in reversed(held):
                os.close(item.fd)
            os.close(out_fd)
    except Exception as exc:
        report = {
            "schema": f"cm2.c79g.{TAG}.cold-freeze-publisher.v1",
            "status": "FAIL_CLOSED_R59_COLD_FREEZE_PUBLISHER",
            "error": f"{type(exc).__name__}: {exc}",
            "manifest_created": manifest_created, "outer_created": outer_created,
            "runtime_authority_writes": False, "formal_global_closure_credit": 0,
            "D02_unlock": False, "runtime_authorized": False,
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
