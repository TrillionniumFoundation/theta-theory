#!/usr/bin/env python3
"""Coherent fail-closed attacks for the C27R2 authority-v2 core.

The harness never edits the authoritative candidate or actual-v2 inputs.  It
first obtains a clean independent-verifier PASS, then creates one private
candidate clone (Linux reflink when available, byte copy otherwise).  Each
attack mutates only that clone and restores it before the next case.

The attacks cover coherently reclosed result lies, inventory/link/gzip faults,
and external authority-pin substitution.  PASS here is still zero-credit and
does not replace release-only TOCTOU, manifest, outer-verifier, cold-replay or
terminal-seal plumbing.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PYTHON = Path("/usr/bin/python3.12")
VERIFIER = ROOT / (
    "deliverables/"
    "cm2_round306c27r2_source_g_actual_v2_fresh_quotient_rebuild_v2_"
    "independent_verifier_v4.py"
)
FILES = {
    "old": "old_c15_component_to_post_component.jsonl.gz",
    "member": "member_to_post_component.jsonl.gz",
    "census": "post_component_census.jsonl.gz",
    "result": "result.json",
}
RESULT_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "producer-result.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "independent-verification.v1"
)
VERIFICATION_PASS_PREFIX = (
    "PASS_NO_IMPORT_ACTUAL_V2_SEED2_INDEPENDENT_QUOTIENT_AND_"
    "BYTE_EXACT_CANDIDATE_REPLAY__ZERO_CREDIT"
)
HARNESS_SCHEMA = (
    "cm2.round306c27r2.source-g-actual-v2-fresh-quotient-rebuild.v2."
    "coherent-attack-harness.v1"
)
FICLONE = 0x40049409


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def valid_sha(value: Any) -> bool:
    return (
        type(value) is str and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def file_sha(path: Path) -> str:
    descriptor = os.open(
        path,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
             "regular single-link file:" + str(path))
        state = hashlib.sha256()
        while block := os.read(descriptor, 4 << 20):
            state.update(block)
        after = os.fstat(descriptor)
        need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
              before.st_ctime_ns, before.st_mode, before.st_nlink)
             == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
                 after.st_ctime_ns, after.st_mode, after.st_nlink),
             "stable hash:" + str(path))
        return state.hexdigest()
    finally:
        os.close(descriptor)


def inside(raw: str | Path, *, absent: bool = False) -> Path:
    value = Path(raw)
    path = (ROOT / value if not value.is_absolute() else value).absolute()
    try:
        relative = path.relative_to(ROOT)
    except ValueError as error:
        raise Failure("path outside workspace:" + str(raw)) from error
    need(all(part not in {"", ".", ".."} for part in relative.parts),
         "canonical workspace path:" + str(raw))
    current = ROOT
    for part in relative.parts:
        current = current / part
        if not current.exists():
            need(absent, "missing path component:" + str(current))
            break
        need(not current.is_symlink(), "symlink path component:" + str(current))
    return path


def strict_document(path: Path, closure: str | None = None) -> Any:
    payload = path.read_bytes()
    need(payload.endswith(b"\n"), "JSON newline:" + str(path))
    value = json.loads(payload)
    need(canonical(value) == payload[:-1], "canonical JSON:" + str(path))
    if closure is not None:
        body = dict(value)
        claim = body.pop(closure, None)
        need(valid_sha(claim) and claim == digest(body),
             "JSON closure:" + str(path))
    return value


def write_once(path: Path, payload: bytes) -> None:
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def clone_file(source: Path, target: Path) -> str:
    need(not target.exists() and not target.is_symlink(),
         "fresh clone target:" + str(target))
    source_fd = os.open(
        source,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    target_fd = os.open(
        target,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    method = "REFLINK"
    try:
        source_info = os.fstat(source_fd)
        need(stat.S_ISREG(source_info.st_mode) and source_info.st_nlink == 1,
             "clone source regular single-link")
        try:
            fcntl.ioctl(target_fd, FICLONE, source_fd)
        except OSError:
            method = "BYTE_COPY"
            os.lseek(source_fd, 0, os.SEEK_SET)
            while block := os.read(source_fd, 4 << 20):
                offset = 0
                while offset < len(block):
                    offset += os.write(target_fd, block[offset:])
        os.fsync(target_fd)
    except BaseException:
        os.close(target_fd)
        os.close(source_fd)
        target.unlink(missing_ok=True)
        raise
    os.close(target_fd)
    os.close(source_fd)
    need(file_sha(source) == file_sha(target), "clone byte identity")
    return method


def clone_candidate(source: Path, target: Path) -> dict[str, str]:
    need(not target.exists(), "fresh private candidate clone")
    target.mkdir(mode=0o700)
    methods: dict[str, str] = {}
    for name in sorted(FILES.values()):
        methods[name] = clone_file(source / name, target / name)
    return methods


def reclose_result(path: Path, mutation: Callable[[dict[str, Any]], None]) -> None:
    value = strict_document(path, "result_sha256")
    body = dict(value)
    body.pop("result_sha256")
    mutation(body)
    body["result_sha256"] = digest(body)
    path.unlink()
    write_once(path, canonical(body) + b"\n")


def flip_hash(value: str) -> str:
    need(valid_sha(value), "hash to flip")
    return ("0" if value[0] != "0" else "1") + value[1:]


def verifier_command(args: argparse.Namespace, candidate: Path,
                     output: Path, *, terminal_dir: str | None = None,
                     base_dir: str | None = None,
                     terminal_root: str | None = None,
                     terminal_file: str | None = None,
                     terminal_object: str | None = None) -> list[str]:
    return [
        str(PYTHON), "-I", "-B", str(VERIFIER),
        "--terminal-dir", terminal_dir or args.terminal_dir,
        "--base-seal-dir", base_dir or args.base_seal_dir,
        "--expect-terminal-root-sha256",
        terminal_root or args.expect_terminal_root_sha256,
        "--expect-terminal-receipt-file-sha256",
        terminal_file or args.expect_terminal_receipt_file_sha256,
        "--expect-terminal-receipt-object-sha256",
        terminal_object or args.expect_terminal_receipt_object_sha256,
        "--candidate-dir", str(candidate),
        "--out-file", str(output),
    ]


def run(command: list[str]) -> subprocess.CompletedProcess[bytes]:
    environment = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "LC_ALL": "C",
        "PYTHONHASHSEED": "30662712",
    }
    return subprocess.run(
        command, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )


def save_transcript(directory: Path, label: str,
                    completed: subprocess.CompletedProcess[bytes]) -> None:
    write_once(directory / (label + ".stdout"), completed.stdout)
    write_once(directory / (label + ".stderr"), completed.stderr)
    write_once(directory / (label + ".exit_code.txt"),
               (str(completed.returncode) + "\n").encode("ascii"))


def reject_record(label: str, completed: subprocess.CompletedProcess[bytes],
                  output: Path) -> dict[str, Any]:
    rejected = (
        completed.returncode == 2
        and completed.stdout == b""
        and completed.stderr.startswith(b"REJECT:")
        and completed.stderr.endswith(b"\n")
        and not output.exists()
    )
    return {
        "attack": label,
        "numeric_exit_code": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
        "stderr_prefix": completed.stderr[:160].decode("ascii", "replace"),
        "verification_output_created": output.exists(),
        "rejected_fail_closed": rejected,
    }


def replace_with_bytes(candidate: Path, saved: Path, name: str,
                       payload: bytes) -> Callable[[], None]:
    path = candidate / name
    backup = saved / name
    os.replace(path, backup)
    write_once(path, payload)

    def restore() -> None:
        path.unlink(missing_ok=True)
        os.replace(backup, path)

    return restore


def replace_with_link(candidate: Path, saved: Path, name: str,
                      hard: bool) -> Callable[[], None]:
    path = candidate / name
    backup = saved / name
    os.replace(path, backup)
    if hard:
        os.link(backup, path)
    else:
        os.symlink(backup, path)

    def restore() -> None:
        path.unlink(missing_ok=True)
        os.replace(backup, path)

    return restore


def execute(args: argparse.Namespace) -> dict[str, Any]:
    candidate_source = inside(args.candidate_dir)
    work = inside(args.work_dir, absent=True)
    out_file = inside(args.out_file, absent=True)
    need(candidate_source.is_dir() and not work.exists() and not out_file.exists(),
         "candidate exists/fresh work and result")
    need(out_file.parent == work or out_file.parent.is_dir(),
         "attack result parent exists or is fresh work directory")
    need(valid_sha(args.expect_verifier_sha256)
         and valid_sha(args.expect_python_sha256)
         and file_sha(VERIFIER) == args.expect_verifier_sha256
         and file_sha(PYTHON) == args.expect_python_sha256,
         "verifier/Python source pins")
    need(file_sha(SELF) == args.expect_harness_sha256,
         "attack harness self pin")
    need({entry.name for entry in candidate_source.iterdir()}
         == set(FILES.values()), "source candidate exact inventory")
    source_before = {name: file_sha(candidate_source / name)
                     for name in sorted(FILES.values())}

    work.mkdir(parents=True, mode=0o700)
    transcripts = work / "transcripts"
    transcripts.mkdir()
    saved = work / "saved"
    saved.mkdir()
    clone = work / "candidate-clone"
    clone_methods = clone_candidate(candidate_source, clone)
    baseline_output = work / "baseline_verification.json"
    baseline = run(verifier_command(args, candidate_source, baseline_output))
    save_transcript(transcripts, "baseline", baseline)
    need(baseline.returncode == 0 and baseline.stderr == b""
         and baseline.stdout.endswith(b"\n") and baseline_output.is_file(),
         "baseline independent verifier clean PASS")
    baseline_document = strict_document(baseline_output, "verification_sha256")
    need(baseline_document.get("schema") == VERIFICATION_SCHEMA
         and baseline_document.get("status", "").startswith(
             VERIFICATION_PASS_PREFIX)
         and baseline_document.get("formal_credit") == 0,
         "baseline verification semantics")

    records: list[dict[str, Any]] = []
    attack_index = 0

    def perform(label: str, mutation: Callable[[], Callable[[], None] | None],
                command_change: dict[str, str] | None = None) -> None:
        nonlocal attack_index
        output = work / f"attack-{attack_index:02d}-{label}.verification.json"
        restore: Callable[[], None] | None = None
        try:
            restore = mutation()
            completed = run(verifier_command(
                args, clone, output, **(command_change or {})))
            save_transcript(transcripts, f"attack-{attack_index:02d}-{label}",
                            completed)
            records.append(reject_record(label, completed, output))
        finally:
            if restore is not None:
                restore()
        attack_index += 1

    def result_mutation(change: Callable[[dict[str, Any]], None]) \
            -> Callable[[], Callable[[], None]]:
        def apply() -> Callable[[], None]:
            path = clone / FILES["result"]
            backup = saved / FILES["result"]
            os.replace(path, backup)
            clone_file(backup, path)
            reclose_result(path, change)

            def restore() -> None:
                path.unlink(missing_ok=True)
                os.replace(backup, path)

            return restore
        return apply

    perform("missing-result", lambda: move_out(clone, saved, FILES["result"]))
    perform("extra-inventory", lambda: add_extra(clone))
    perform("result-noncanonical", lambda: replace_with_bytes(
        clone, saved, FILES["result"], b'{"z":0, "a":1}\n'))
    perform("result-duplicate-key", lambda: replace_with_bytes(
        clone, saved, FILES["result"], b'{"schema":"x","schema":"y"}\n'))
    perform("result-stale-closure", lambda: replace_with_bytes(
        clone, saved, FILES["result"],
        (clone / FILES["result"]).read_bytes().replace(
            b'"formal_credit":0', b'"formal_credit":1', 1)))
    perform("coherent-formal-credit", result_mutation(
        lambda value: value.__setitem__("formal_credit", 1)))
    perform("coherent-manifest-authorized", result_mutation(
        lambda value: value.__setitem__("manifest_authorized", True)))
    perform("coherent-status-lie", result_mutation(
        lambda value: value.__setitem__("status", "PASS_FORMAL_C27R2")))
    perform("coherent-census-lie", result_mutation(
        lambda value: value["exact_census"].__setitem__(
            "post_C27R2_components", 43_683)))
    perform("coherent-dsu-root-id-formula", result_mutation(
        lambda value: value.__setitem__(
            "canonical_post_component_id_formula", "DSU_INTERNAL_ROOT")))
    perform("coherent-seed-label-swap", result_mutation(
        lambda value: value["authority"].__setitem__(
            "actual_v2_seed_label", "seed2")))
    perform("coherent-ledger-sha-lie", result_mutation(
        lambda value: value["ledgers"]["member_to_post_component"].__setitem__(
            "sha256", flip_hash(
                value["ledgers"]["member_to_post_component"]["sha256"]))))
    perform("result-symlink", lambda: replace_with_link(
        clone, saved, FILES["result"], False))
    perform("old-map-hardlink", lambda: replace_with_link(
        clone, saved, FILES["old"], True))
    perform("old-map-truncated-gzip", lambda: replace_with_bytes(
        clone, saved, FILES["old"],
        (clone / FILES["old"]).read_bytes()[:37]))
    perform("member-map-bad-gzip", lambda: replace_with_bytes(
        clone, saved, FILES["member"], b"not-a-gzip-stream\n"))
    perform("post-census-empty-gzip", lambda: replace_with_bytes(
        clone, saved, FILES["census"], b"\x1f\x8b\x08\x00"))
    perform("wrong-terminal-root-pin", lambda: None, {
        "terminal_root": flip_hash(args.expect_terminal_root_sha256)})
    perform("wrong-terminal-file-pin", lambda: None, {
        "terminal_file": flip_hash(args.expect_terminal_receipt_file_sha256)})
    perform("wrong-terminal-object-pin", lambda: None, {
        "terminal_object": flip_hash(
            args.expect_terminal_receipt_object_sha256)})
    perform("terminal-base-directory-swap", lambda: None, {
        "terminal_dir": args.base_seal_dir, "base_dir": args.terminal_dir})

    need(len(records) == 21
         and all(record["rejected_fail_closed"] for record in records),
         "all 21 coherent attacks rejected")
    need({name: file_sha(candidate_source / name)
          for name in sorted(FILES.values())} == source_before,
         "authoritative candidate pre/post SHA unchanged")
    need({entry.name for entry in clone.iterdir()} == set(FILES.values()),
         "private clone restored exact inventory")
    body = {
        "schema": HARNESS_SCHEMA,
        "status": (
            "PASS_BASELINE_AND_21_OF_21_COHERENT_ATTACKS_REJECTED_"
            "FAIL_CLOSED__ZERO_CREDIT_PENDING_RELEASE_CHAIN"
        ),
        "harness_source_sha256": args.expect_harness_sha256,
        "independent_verifier_source_sha256": args.expect_verifier_sha256,
        "python_sha256": args.expect_python_sha256,
        "baseline_verification_file_sha256": file_sha(baseline_output),
        "baseline_verification_object_sha256":
            baseline_document["verification_sha256"],
        "clone_methods": clone_methods,
        "attack_count": len(records),
        "rejected": sum(record["rejected_fail_closed"] for record in records),
        "accepted": sum(not record["rejected_fail_closed"] for record in records),
        "attacks": records,
        "authoritative_candidate_pre_post_sha256_identical": True,
        "scope": {
            "candidate_coherent_reclosure_attacks": True,
            "inventory_link_and_gzip_attacks": True,
            "external_terminal_pin_substitution_attacks": True,
            "release_TOCTOU_manifest_outer_cold_terminal_attacks":
                "REQUIRED_LATER_NOT_CLAIMED_BY_THIS_CORE_HARNESS",
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "C27R2": "UNAUTHORIZED_PENDING_RELEASE_CHAIN",
        "C28_C29": "UNAUTHORIZED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["attack_harness_sha256"] = digest(result)
    write_once(out_file, canonical(result) + b"\n")
    return result


def move_out(candidate: Path, saved: Path,
             name: str) -> Callable[[], None]:
    path = candidate / name
    backup = saved / name
    os.replace(path, backup)

    def restore() -> None:
        os.replace(backup, path)

    return restore


def add_extra(candidate: Path) -> Callable[[], None]:
    extra = candidate / "unexpected.extra"
    write_once(extra, b"attack\n")

    def restore() -> None:
        extra.unlink()

    return restore


def self_test() -> dict[str, Any]:
    value = {"schema": RESULT_SCHEMA, "formal_credit": 0}
    closed = {**value, "result_sha256": digest(value)}
    need(closed["result_sha256"] == digest(value), "fixture closure")
    need(flip_hash("0" * 64) == "1" + "0" * 63,
         "fixture hash substitution")
    with tempfile.TemporaryDirectory(prefix="cm2-c27r2-v2-attacks-selftest-") as raw:
        directory = Path(raw)
        source = directory / "source"
        target = directory / "target"
        source.write_bytes(b"fixture\n")
        method = clone_file_unrestricted(source, target)
        need(source.read_bytes() == target.read_bytes()
             and method in {"REFLINK", "BYTE_COPY"}, "fixture private clone")
    return {
        "schema": HARNESS_SCHEMA + ".self-test",
        "status": "PASS_SMALL_FIXTURE_CLOSURE_HASH_AND_PRIVATE_CLONE_TESTS",
        "formal_credit": 0,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def clone_file_unrestricted(source: Path, target: Path) -> str:
    method = "REFLINK"
    source_fd = os.open(source, os.O_RDONLY)
    target_fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        try:
            fcntl.ioctl(target_fd, FICLONE, source_fd)
        except OSError:
            method = "BYTE_COPY"
            os.lseek(source_fd, 0, os.SEEK_SET)
            while block := os.read(source_fd, 4096):
                os.write(target_fd, block)
        os.fsync(target_fd)
    finally:
        os.close(source_fd)
        os.close(target_fd)
    return method


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--terminal-dir")
    value.add_argument("--base-seal-dir")
    value.add_argument("--expect-terminal-root-sha256")
    value.add_argument("--expect-terminal-receipt-file-sha256")
    value.add_argument("--expect-terminal-receipt-object-sha256")
    value.add_argument("--candidate-dir")
    value.add_argument("--work-dir")
    value.add_argument("--out-file")
    value.add_argument("--expect-verifier-sha256")
    value.add_argument("--expect-python-sha256")
    value.add_argument("--expect-harness-sha256")
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "terminal_dir", "base_seal_dir", "expect_terminal_root_sha256",
        "expect_terminal_receipt_file_sha256",
        "expect_terminal_receipt_object_sha256", "candidate_dir", "work_dir",
        "out_file", "expect_verifier_sha256", "expect_python_sha256",
        "expect_harness_sha256",
    )
    try:
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields),
                 "self-test accepts no run arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields),
                 "all authority/candidate/source pins and fresh paths required")
            result = execute(args)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())



