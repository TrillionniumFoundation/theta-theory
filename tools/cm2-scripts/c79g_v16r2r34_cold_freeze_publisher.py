#!/usr/bin/env python3
"""One-shot r34 exact8 -> manifest -> outer-last cold-freeze publisher.

This publisher is intentionally a fresh append-only implementation.  It does
not import or execute any candidate protocol, does not open an authority or
credit surface for writing, and never creates a runtime object.  The existing
r34 read-only preflight guard is run first.  Only after a 7/7 pass are the
three source members changed from 0664 to 0444 on held file descriptors.  The
manifest and the launcher-native outer receipt are then created with O_EXCL,
fsynced, and terminally replayed while the held descriptors remain open.

The launcher source is the authority for the outer shape: its native
publication reconstruction has no successor-checkpoint field.  The successor
DD9 pin remains in the nested static contract/transition/audit evidence and is
deliberately not copied into this outer object.
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
TAG = "v16r2r34"
PREV = "v16r2r33"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR_CHECKPOINT = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"

GUARD = ROOT / "scripts/c79g_v16r2r34_cold_freeze_guard.py"
MANIFEST_REL = f"deliverables/{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER_REL = f"deliverables/{BASE}_cold_launch_outer_receipt_{TAG}.json"
MANIFEST = ROOT / MANIFEST_REL
OUTER = ROOT / OUTER_REL

C53_REL = Path(
    ".cm2-runtime/cm2-global-authority-heads/"
    "predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
)
C53 = ROOT / C53_REL
C53_FILE_SHA256 = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT_SHA256 = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"


@dataclass(frozen=True)
class Pin:
    relative: str
    file_sha256: str
    object_sha256: str | None
    initial_mode: int


EXACT8: tuple[Pin, ...] = (
    Pin(
        f"deliverables/{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json",
        "b0a47e3ea586aa9bca2fb647ace2086651c318b0676369e09b59d8b705ef7a89",
        "9047ba11c82743b18731818044755b7dedf591cf4bc1e3982921871521c78b0e",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_schema_{TAG}.json",
        "faa68634c03eda0818f970c1963436bcc446a83695c5f20da36f6c632de9192d",
        None,
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_contract_{TAG}.json",
        "3c1e109fbb6a80b83e623131b549bf5007d8c9e3f3676087133714aa5f554b71",
        "98477ae1718cd6ad1a87cbe86a2099725e80bf1c2a4c16eed1d9271a2813f780",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_{TAG}_semantic_source.py",
        "e83a718c0a480e4deaa44fc091b18d3438f87519efe7db27f4204cf99a3596ed",
        None,
        0o664,
    ),
    Pin(
        f"deliverables/{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
        "877f4a6ba6475ee27ffca8e030302d9af7c5309fcefb689b37be4049682a1e9b",
        None,
        0o664,
    ),
    Pin(
        f"deliverables/{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
        "86ccf4e8543a095105958981804b1531a48b4da89f0dc9f1f363bf0c396c7933",
        "29d32e73855644d56d28d58345eeaf25ebc4ddc6a5c6a2ea2800f5a19faa13a3",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_static_audit_{TAG}.json",
        "b924ecbc71ef8e280d1fa15bba22ba0af682711217713b2c7217b475c629e187",
        "c9c8ef2cbdfc0098e9c307ab360d5275bd4efe97f1038d24298b5684fbb5bf9a",
        0o444,
    ),
    Pin(
        f"deliverables/{BASE}_cold_launch_{TAG}_semantic_source.py",
        "24f9686462f47c009118887d1cdfd0f1b22791eeef335bcb64252d3ade931c0a",
        None,
        0o664,
    ),
)

SOURCE_PATHS = frozenset(pin.relative for pin in EXACT8 if pin.relative.endswith(".py"))
OUTER_KEYS = frozenset(
    {
        "schema",
        "status",
        "effective_checkpoint_object_sha256",
        "exact8_ordered_entries",
        "cold_launch_manifest",
        "cold_launcher",
        "all_exact8_regular_0444_nlink1_and_held_for_runtime",
        "outer_published_after_exact8_manifest",
        "runtime_entry_must_be_cold_launcher",
        "sole_external_static_file_anchor_is_launcher_sha256",
        "declared_external_tcb",
        "formal_global_closure_credit",
        "D02_unlock",
        "runtime_executed_during_static_freeze",
        "object_sha256",
    }
)


def canonical(value: Any) -> bytes:
    # This is byte-for-byte the launcher canonicalizer.
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def identity(st: os.stat_result) -> tuple[int, int, int, int]:
    return (st.st_dev, st.st_ino, st.st_size, st.st_nlink)


def reject(message: str) -> None:
    raise RuntimeError(message)


def assert_absent(path: Path) -> None:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return
    raise RuntimeError(f"append-only target already exists:{path.relative_to(ROOT)}")


def strict_json(raw: bytes, label: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise RuntimeError(f"duplicate JSON key:{label}:{key}")
            result[key] = value
        return result

    return json.loads(
        raw.decode("utf-8"), object_pairs_hook=pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            RuntimeError(f"non-finite JSON constant:{label}:{token}")),
    )


def stable_fd(fd: int, path: Path) -> tuple[bytes, os.stat_result]:
    """Read a held descriptor and prove path identity did not drift."""
    before = os.fstat(fd)
    named = os.lstat(path)
    if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
            identity(before) != identity(named)):
        reject(f"unstable input:{path}")
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
    if (identity(before) != identity(after) or
            identity(before) != identity(named_after)):
        reject(f"identity drift:{path}")
    raw = b"".join(chunks)
    if len(raw) != before.st_size:
        reject(f"size drift:{path}")
    return raw, after


def stable_path(path: Path) -> tuple[bytes, os.stat_result]:
    fd = os.open(
        path,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        return stable_fd(fd, path)
    finally:
        os.close(fd)


def verify_json_pin(pin: Pin, raw: bytes) -> None:
    if not pin.relative.endswith(".json"):
        return
    value = strict_json(raw, pin.relative)
    if not isinstance(value, dict):
        reject(f"JSON object required:{pin.relative}")
    if pin.object_sha256 is not None:
        claim = value.get("object_sha256")
        body = dict(value)
        body.pop("object_sha256", None)
        if claim != pin.object_sha256 or sha(canonical(body)) != claim:
            reject(f"JSON object pin mismatch:{pin.relative}")


def assert_no_tagged_pyc() -> list[str]:
    found: list[str] = []
    for path in ROOT.rglob("*.pyc"):
        try:
            if TAG in str(path.relative_to(ROOT)):
                found.append(str(path.relative_to(ROOT)))
        except ValueError:
            continue
    if found:
        reject("r34 pyc present:" + ",".join(found))
    return found


def runtime_tagged_paths() -> list[str]:
    runtime = ROOT / ".cm2-runtime"
    if not runtime.exists():
        return []
    found: list[str] = []
    for path in runtime.rglob("*"):
        try:
            rel = str(path.relative_to(ROOT))
        except ValueError:
            continue
        if TAG in rel:
            found.append(rel)
    return found


def c53_snapshot() -> tuple[bytes, str, str]:
    raw, st = stable_path(C53)
    if st.st_nlink != 1 or stat.S_IMODE(st.st_mode) != 0o444:
        reject("C53 mode/nlink")
    if sha(raw) != C53_FILE_SHA256:
        reject("C53 file pin")
    value = strict_json(raw, "C53")
    if (not isinstance(value, dict) or
            value.get("authority_seal_object_sha256") != C53_OBJECT_SHA256):
        reject("C53 object pin")
    return raw, sha(raw), C53_OBJECT_SHA256


def run_guard() -> tuple[dict[str, Any], bytes]:
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1",
                "PYTHONHASHSEED": "1"})
    proc = subprocess.run(
        ["/usr/bin/python3", "-I", "-B", str(GUARD)],
        cwd=str(ROOT), env=env, capture_output=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"r34 guard rc={proc.returncode}:{proc.stderr[-600:]!r}")
    try:
        report = json.loads(proc.stdout.decode("utf-8"))
    except Exception as exc:
        raise RuntimeError("r34 guard did not emit one JSON object") from exc
    if not isinstance(report, dict):
        raise RuntimeError("r34 guard report object required")
    if (report.get("status") !=
            "PREFLIGHT_PASS_R34_PINS_PENDING_MANIFEST_OUTER_ABSENT__ZERO_CREDIT" or
            report.get("check_count") != 7 or
            report.get("failed_check_count") != 0 or
            report.get("read_only") is not True or
            report.get("formal_global_closure_credit") != 0 or
            report.get("D02_unlock") is not False or
            report.get("runtime_authorized") is not False or
            report.get("manifest_created") is not False or
            report.get("outer_created") is not False):
        raise RuntimeError("r34 guard predicate failed")
    rows = report.get("exact8")
    expected = [
        {"path": p.relative, "file_sha256": p.file_sha256,
         "object_sha256": p.object_sha256, "mode": p.initial_mode}
        for p in EXACT8
    ]
    if rows != expected:
        raise RuntimeError("r34 guard exact8 report mismatch")
    return report, proc.stdout


@dataclass
class Held:
    pin: Pin
    path: Path
    fd: int
    raw: bytes
    initial: os.stat_result
    final: os.stat_result | None = None


def open_exact8() -> list[Held]:
    opened: list[Held] = []
    try:
        for pin in EXACT8:
            path = ROOT / pin.relative
            fd = os.open(
                path,
                os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
            )
            try:
                raw, st = stable_fd(fd, path)
                if sha(raw) != pin.file_sha256:
                    reject(f"exact8 byte pin:{pin.relative}")
                if stat.S_IMODE(st.st_mode) != pin.initial_mode:
                    reject(f"exact8 initial mode:{pin.relative}")
                verify_json_pin(pin, raw)
                opened.append(Held(pin, path, fd, raw, st))
            except BaseException:
                os.close(fd)
                raise
        ids = {identity(item.initial) for item in opened}
        if len(ids) != len(EXACT8):
            reject("exact8 identity collision")
        if len({item.initial.st_dev for item in opened}) != 1:
            reject("exact8 device split")
        return opened
    except BaseException:
        for item in reversed(opened):
            os.close(item.fd)
        raise


def freeze_exact8(held: list[Held], out_fd: int) -> None:
    source_freeze_count = 0
    for item in held:
        # The descriptor is held from the preflight byte check through the
        # metadata transition; no pathname is reopened for the chmod.
        os.fsync(item.fd)
        current = os.fstat(item.fd)
        if stat.S_IMODE(current.st_mode) == 0o664:
            os.fchmod(item.fd, 0o444)
            source_freeze_count += 1
        elif stat.S_IMODE(current.st_mode) != 0o444:
            reject(f"unexpected freeze mode:{item.pin.relative}")
        os.fsync(item.fd)
        raw, final = stable_fd(item.fd, item.path)
        if raw != item.raw or sha(raw) != item.pin.file_sha256:
            reject(f"byte drift during freeze:{item.pin.relative}")
        if stat.S_IMODE(final.st_mode) != 0o444:
            reject(f"not terminal 0444:{item.pin.relative}")
        item.final = final
        os.fsync(out_fd)
    if source_freeze_count != 3:
        reject(f"expected three source freezes, observed {source_freeze_count}")
    for item in held:
        if item.final is None:
            reject("missing final exact8 state")
        if stat.S_IMODE(item.final.st_mode) != 0o444 or item.final.st_nlink != 1:
            reject(f"exact8 terminal mode/nlink:{item.pin.relative}")


def publication_bytes(held: list[Held]) -> tuple[bytes, bytes, str, str]:
    entries = [
        {"path": item.pin.relative, "file_sha256": item.pin.file_sha256}
        for item in held
    ]
    manifest = b"".join(
        f"{entry['file_sha256']}  {entry['path']}\n".encode("ascii")
        for entry in entries
    )
    manifest_sha = sha(manifest)
    body: dict[str, Any] = {
        "schema": (
            "cm2.round306c79g.true-global-no-producer-consumer."
            "cold-launch-outer-receipt.v16r2"),
        "status": (
            "FROZEN_COLD_LAUNCH_OUTER_LAST__EXACT8_MANIFEST_CLOSED__"
            "RUNTIME_DEFERRED"),
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "exact8_ordered_entries": entries,
        "cold_launch_manifest": {
            "path": MANIFEST_REL,
            "file_sha256": manifest_sha,
            "ordered_entry_count": 8,
        },
        "cold_launcher": {
            "path": EXACT8[-1].relative,
            "file_sha256": EXACT8[-1].file_sha256,
        },
        "all_exact8_regular_0444_nlink1_and_held_for_runtime": True,
        "outer_published_after_exact8_manifest": True,
        "runtime_entry_must_be_cold_launcher": True,
        "sole_external_static_file_anchor_is_launcher_sha256": True,
        "declared_external_tcb": [
            "EXTERNAL_HELD_FD_SEALED_MEMFD_BOOTSTRAP",
            "PYTHON3_ISOLATED_INTERPRETER",
            "LINUX_KERNEL_OPENAT2_STATX_MEMFD_PROCFS",
        ],
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_executed_during_static_freeze": False,
    }
    if frozenset(body) != OUTER_KEYS - {"object_sha256"}:
        reject("launcher-native outer key shape")
    body["object_sha256"] = sha(canonical(body))
    outer = canonical(body) + b"\n"
    return manifest, outer, manifest_sha, body["object_sha256"]


def create_exclusive(out_fd: int, relative: str, raw: bytes) -> tuple[int, os.stat_result]:
    name = Path(relative).name
    if Path(relative).parent.as_posix() != "deliverables":
        reject("publication path is not direct deliverables member")
    fd = os.open(
        name,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC |
        getattr(os, "O_NOFOLLOW", 0),
        0o444,
        dir_fd=out_fd,
    )
    try:
        view = memoryview(raw)
        offset = 0
        while offset < len(view):
            count = os.write(fd, view[offset:])
            if count <= 0:
                reject(f"short write:{relative}")
            offset += count
        os.fsync(fd)
        os.fchmod(fd, 0o444)
        os.fsync(fd)
        os.fsync(out_fd)
        state = os.fstat(fd)
        named = os.stat(name, dir_fd=out_fd, follow_symlinks=False)
        if (not stat.S_ISREG(state.st_mode) or state.st_nlink != 1 or
                stat.S_IMODE(state.st_mode) != 0o444 or
                identity(state) != identity(named) or
                os.lseek(fd, 0, os.SEEK_CUR) < 0):
            reject(f"published identity:{relative}")
        os.lseek(fd, 0, os.SEEK_SET)
        if os.read(fd, len(raw) + 1) != raw:
            reject(f"published bytes:{relative}")
        os.lseek(fd, 0, os.SEEK_SET)
        return fd, state
    except BaseException:
        os.close(fd)
        raise


def chronology(exact: list[os.stat_result], manifest: os.stat_result,
               outer: os.stat_result) -> dict[str, bool]:
    exact_ok = all(s.st_mtime_ns <= s.st_ctime_ns for s in exact)
    manifest_ok = manifest.st_mtime_ns <= manifest.st_ctime_ns
    outer_ok = outer.st_mtime_ns <= outer.st_ctime_ns
    exact_before_manifest = max(
        max(s.st_mtime_ns, s.st_ctime_ns) for s in exact
    ) < manifest.st_mtime_ns
    manifest_before_outer = manifest.st_ctime_ns < outer.st_mtime_ns
    return {
        "all_exact8_mtime_not_after_final_ctime": exact_ok,
        "manifest_mtime_not_after_final_ctime": manifest_ok,
        "outer_mtime_not_after_final_ctime": outer_ok,
        "max_exact8_final_mtime_ctime_before_manifest_mtime": exact_before_manifest,
        "manifest_final_ctime_before_outer_mtime": manifest_before_outer,
        "physical_exact8_freeze_then_manifest_freeze_then_outer_freeze_chronology": (
            exact_ok and manifest_ok and outer_ok and exact_before_manifest and
            manifest_before_outer
        ),
    }


def terminal_replay(
    held: list[Held], manifest_fd: int, outer_fd: int,
    manifest_raw: bytes, outer_raw: bytes,
    manifest_state: os.stat_result, outer_state: os.stat_result,
    entries: list[dict[str, str]],
) -> None:
    for item in held:
        raw, state = stable_fd(item.fd, item.path)
        if raw != item.raw or sha(raw) != item.pin.file_sha256:
            reject(f"exact8 terminal replay bytes:{item.pin.relative}")
        if (stat.S_IMODE(state.st_mode) != 0o444 or state.st_nlink != 1 or
                identity(state) != identity(item.final)):
            reject(f"exact8 terminal replay identity:{item.pin.relative}")
    for fd, path, expected, state in (
        (manifest_fd, MANIFEST, manifest_raw, manifest_state),
        (outer_fd, OUTER, outer_raw, outer_state),
    ):
        raw, current = stable_fd(fd, path)
        if raw != expected or stat.S_IMODE(current.st_mode) != 0o444 or current.st_nlink != 1:
            reject(f"publication terminal replay:{path.name}")
        if identity(current) != identity(state):
            reject(f"publication identity drift:{path.name}")
    parsed_manifest = manifest_raw.decode("ascii").splitlines()
    expected_lines = [f"{e['file_sha256']}  {e['path']}" for e in entries]
    if parsed_manifest != expected_lines:
        reject("manifest exact ordered replay")
    outer_value = strict_json(outer_raw, "r34 outer")
    if not isinstance(outer_value, dict) or frozenset(outer_value) != OUTER_KEYS:
        reject("outer exact key replay")
    body = dict(outer_value)
    claim = body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canonical(body)) != claim:
        reject("outer object closure replay")
    if "successor_checkpoint_object_sha256" in outer_value:
        reject("outer successor field forbidden by launcher-native shape")
    if (outer_value.get("effective_checkpoint_object_sha256") != CHECKPOINT or
            outer_value.get("formal_global_closure_credit") != 0 or
            outer_value.get("D02_unlock") is not False or
            outer_value.get("runtime_executed_during_static_freeze") is not False):
        reject("outer zero-credit/effective checkpoint replay")


def main() -> int:
    held: list[Held] = []
    manifest_fd = -1
    outer_fd = -1
    guard_report: dict[str, Any] | None = None
    guard_raw = b""
    manifest_created = False
    outer_created = False
    try:
        # This is the only subprocess and it is read-only.  It must pass before
        # any source mode transition or publication target is touched.
        guard_report, guard_raw = run_guard()
        assert_absent(MANIFEST)
        assert_absent(OUTER)
        assert_no_tagged_pyc()
        if runtime_tagged_paths():
            reject("r34 runtime surface already present")
        c53_before_raw, c53_before_sha, _ = c53_snapshot()
        out_fd = os.open(
            OUT,
            os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC |
            getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            held = open_exact8()
            freeze_exact8(held, out_fd)
            # Recheck append-only targets and the upstream authority head just
            # before the first namespace write.
            assert_absent(MANIFEST)
            assert_absent(OUTER)
            c53_now_raw, c53_now_sha, _ = c53_snapshot()
            if c53_now_raw != c53_before_raw or c53_now_sha != c53_before_sha:
                reject("C53 changed before publication")
            manifest_raw, outer_raw, manifest_sha, outer_object_sha = publication_bytes(held)
            entries = [
                {"path": item.pin.relative, "file_sha256": item.pin.file_sha256}
                for item in held
            ]
            manifest_fd, manifest_state = create_exclusive(out_fd, MANIFEST_REL, manifest_raw)
            manifest_created = True
            # Outer is deliberately the tenth and last namespace creation.
            assert_absent(OUTER)
            outer_fd, outer_state = create_exclusive(out_fd, OUTER_REL, outer_raw)
            outer_created = True
            chrono = chronology(
                [item.final for item in held if item.final is not None],
                manifest_state, outer_state,
            )
            if not all(chrono.values()):
                reject("physical publication chronology")
            terminal_replay(
                held, manifest_fd, outer_fd, manifest_raw, outer_raw,
                manifest_state, outer_state, entries,
            )
            c53_after_raw, c53_after_sha, _ = c53_snapshot()
            if c53_after_raw != c53_before_raw or c53_after_sha != c53_before_sha:
                reject("C53 changed after publication")
            assert_no_tagged_pyc()
            if runtime_tagged_paths():
                reject("r34 runtime surface appeared")
            report: dict[str, Any] = {
                "schema": f"cm2.c79g.{TAG}.cold-freeze-publisher.v1",
                "status": (
                    "TERMINAL_EXACT10_HELD_REPLAY_PASS__FROZEN_MANIFEST_OUTER_LAST__"
                    "RUNTIME_NOT_EXECUTED"),
                "successor_suffix": TAG,
                "predecessor_suffix": PREV,
                "ordered_exact10": [item.pin.relative for item in held] +
                [MANIFEST_REL, OUTER_REL],
                "exact8_file_sha256": {
                    item.pin.relative: item.pin.file_sha256 for item in held
                },
                "exact8_terminal_mode": "0444",
                "source_freeze_count": 3,
                "manifest_file_sha256": manifest_sha,
                "outer_file_sha256": sha(outer_raw),
                "outer_object_sha256": outer_object_sha,
                "guard_report_sha256": sha(guard_raw),
                "guard_status": guard_report.get("status"),
                "guard_check_count": guard_report.get("check_count"),
                "guard_failed_check_count": guard_report.get("failed_check_count"),
                "C53_authority_head_sha256_before_after": c53_before_sha,
                "C53_unchanged": True,
                "chronology": chrono,
                "manifest_O_EXCL_outer_last_O_EXCL": True,
                "manifest_created": True,
                "outer_created": True,
                "runtime_authority_writes": False,
                "candidate_execution_count": 0,
                "formal_global_closure_credit": 0,
                "D02_unlock": False,
                "runtime_authorized": False,
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
            "status": "FAIL_CLOSED_R34_COLD_FREEZE_PUBLISHER",
            "error": f"{type(exc).__name__}: {exc}",
            "manifest_created": manifest_created,
            "outer_created": outer_created,
            "runtime_authority_writes": False,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "runtime_authorized": False,
        }
        report["object_sha256"] = sha(canonical(report))
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
