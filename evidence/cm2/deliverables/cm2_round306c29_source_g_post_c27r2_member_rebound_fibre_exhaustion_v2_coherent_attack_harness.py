#!/usr/bin/env python3
"""Coherent corruption harness for the append-only C29-v2 candidate.

The harness never edits its input candidate.  Each case uses Linux reflinks in
a fresh append-only work directory, recloses every directly affected row,
ledger descriptor, theorem hash, and result object, then requires the
no-import verifier to reject with exit 2 and without producing a verification
file.  Release-only process/TOCTOU/cold-history attacks remain the job of the
future transaction and terminal-seal layer.
"""

from __future__ import annotations

import argparse
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
PREFIX = "cm2_round306c29_source_g_post_c27r2_member_rebound_fibre_exhaustion_v2"
COMPONENT_LEDGER = PREFIX + "_post_component_official_key_assignment_ledger.jsonl.gz"
FIBRE_LEDGER = PREFIX + "_official_key_fibre_exhaustion_ledger.jsonl.gz"
DISPOSITION_LEDGER = PREFIX + "_global_member_disposition_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"
FILES = {COMPONENT_LEDGER, FIBRE_LEDGER, DISPOSITION_LEDGER, RESULT}
RESULT_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
    "producer-result.v1"
)
HARNESS_SCHEMA = (
    "cm2.round306c29.source-g-post-c27r2-member-rebound-fibre-exhaustion.v2."
    "coherent-attacks.v1"
)
FICLONE = 0x40049409


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def pair_object(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        need(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def constant(value: str) -> None:
    raise Failure("JSON constant:" + value)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1 << 20):
            state.update(chunk)
    return state.hexdigest()


def decode(raw: bytes, label: str, newline: bool = True) -> Any:
    if newline:
        need(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), label + ":newline")
        raw = raw[:-1]
    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pair_object,
            parse_constant=constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Failure(label + ":JSON") from error
    need(canonical(value) == raw, label + ":canonical")
    return value


def closed_result(path: Path) -> dict[str, Any]:
    value = decode(path.read_bytes(), path.name)
    need(type(value) is dict and value.get("schema") == RESULT_SCHEMA,
         "candidate result schema")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == object_sha(body), "candidate result closure")
    return value


def write_result(path: Path, value: dict[str, Any]) -> None:
    body = dict(value)
    body.pop("result_sha256", None)
    body["result_sha256"] = object_sha(body)
    path.write_bytes(canonical(body) + b"\n")


def close_row(value: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    body.pop("row_sha256", None)
    body["row_sha256"] = object_sha(body)
    return body


def clone_file(source: Path, target: Path) -> None:
    source_fd = os.open(source, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
    try:
        target_fd = os.open(
            target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC,
            stat.S_IMODE(source.stat().st_mode),
        )
        try:
            fcntl.ioctl(target_fd, FICLONE, source_fd)
            os.fsync(target_fd)
        except OSError as error:
            os.close(target_fd)
            target_fd = -1
            target.unlink(missing_ok=True)
            raise Failure("reflink required for immutable full-candidate attacks") from error
        finally:
            if target_fd >= 0:
                os.close(target_fd)
    finally:
        os.close(source_fd)


def clone_candidate(source: Path, target: Path) -> None:
    target.mkdir(mode=0o700)
    for name in sorted(FILES):
        clone_file(source / name, target / name)


def read_gzip_rows(path: Path) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    try:
        with gzip.open(path, "rb") as source:
            for ordinal, line in enumerate(source):
                need(line.endswith(b"\n"), path.name + ":row newline")
                value = decode(line[:-1], path.name + ":" + str(ordinal), False)
                need(type(value) is dict, path.name + ":row object")
                body = dict(value)
                claimed = body.pop("row_sha256", None)
                need(type(claimed) is str and claimed == object_sha(body),
                     path.name + ":row closure")
                output.append(value)
    except (gzip.BadGzipFile, EOFError) as error:
        raise Failure(path.name + ":gzip") from error
    return output


def write_gzip_rows(path: Path, rows: list[dict[str, Any]]) -> tuple[int, str]:
    sequence = hashlib.sha256()
    temporary = path.with_name(path.name + ".attack-new")
    with temporary.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as output:
            for row in rows:
                output.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
    os.replace(temporary, path)
    return len(rows), sequence.hexdigest()


def reclose_descriptor(candidate: Path, ledger: str, result_key: str) -> None:
    rows = read_gzip_rows(candidate / ledger)
    count = len(rows)
    sequence = hashlib.sha256()
    for row in rows:
        sequence.update(bytes.fromhex(row["row_sha256"]))
    result = closed_result(candidate / RESULT)
    descriptor = result["ledgers"][result_key]
    descriptor.update({
        "filename": ledger,
        "row_count": count,
        "size": (candidate / ledger).stat().st_size,
        "sha256": file_sha(candidate / ledger),
        "row_sequence_sha256": sequence.hexdigest(),
    })
    write_result(candidate / RESULT, result)


def result_mutator(action: Callable[[dict[str, Any]], None]) -> Callable[[Path], None]:
    def mutate(candidate: Path) -> None:
        value = closed_result(candidate / RESULT)
        action(value)
        write_result(candidate / RESULT, value)
    return mutate


def theorem_flag(candidate: Path) -> None:
    value = closed_result(candidate / RESULT)
    value["theorem"]["component_key_incidences_recomputed_not_imported"] = False
    value["theorem_sha256"] = object_sha(value["theorem"])
    write_result(candidate / RESULT, value)


def ledger_mutator(
    ledger: str, result_key: str, action: Callable[[dict[str, Any]], None],
) -> Callable[[Path], None]:
    def mutate(candidate: Path) -> None:
        values = read_gzip_rows(candidate / ledger)
        need(len(values) > 0, ledger + ":nonempty")
        action(values[0])
        values[0] = close_row(values[0])
        write_gzip_rows(candidate / ledger, values)
        reclose_descriptor(candidate, ledger, result_key)
    return mutate


def truncate_gzip(candidate: Path) -> None:
    path = candidate / DISPOSITION_LEDGER
    raw = path.read_bytes()
    need(len(raw) > 32, "truncate source")
    path.write_bytes(raw[:-17])
    result = closed_result(candidate / RESULT)
    descriptor = result["ledgers"]["global_member_disposition"]
    descriptor["size"] = path.stat().st_size
    descriptor["sha256"] = file_sha(path)
    write_result(candidate / RESULT, result)


def extra_file(candidate: Path) -> None:
    (candidate / "EXTRA.json").write_bytes(b"{}\n")


def symlink_member(candidate: Path) -> None:
    path = candidate / COMPONENT_LEDGER
    path.unlink()
    path.symlink_to(FIBRE_LEDGER)


def hardlink_extra(candidate: Path) -> None:
    os.link(candidate / RESULT, candidate / "HARDLINKED_RESULT.json")


def attacks() -> list[tuple[str, Callable[[Path], None], str]]:
    return [
        ("result_formal_credit", result_mutator(lambda x: x.__setitem__("formal_credit", 1)), "normal"),
        ("result_manifest_authorized", result_mutator(lambda x: x.__setitem__("manifest_authorized", True)), "normal"),
        ("result_C29_authorized", result_mutator(lambda x: x.__setitem__("C29", "AUTHORIZED")), "normal"),
        ("result_Source_W_numeric", result_mutator(lambda x: x.__setitem__("Source_W", 0)), "normal"),
        ("result_D02_unblocked", result_mutator(lambda x: x.__setitem__("D02", "PASS")), "normal"),
        ("result_Gate5_18", result_mutator(lambda x: x.__setitem__("Gate5", "18/18")), "normal"),
        ("result_incidence_plus_one", result_mutator(lambda x: x["recomputed_census"].__setitem__("component_key_incidences", x["recomputed_census"]["component_key_incidences"] + 1)), "normal"),
        ("result_multiplicity_false", result_mutator(lambda x: x["recomputed_census"].__setitem__("component_key_multiplicity_census", {"1": 43684})), "normal"),
        ("theorem_imported_instead_recomputed", theorem_flag, "normal"),
        ("result_C27R2_root_substitution", result_mutator(lambda x: x["source_authority"].__setitem__("C27R2_terminal_root_manifest_sha256", "0" * 64)), "normal"),
        ("result_C28_root_substitution", result_mutator(lambda x: x["source_authority"].__setitem__("C28_v2_terminal_root_manifest_sha256", "f" * 64)), "normal"),
        ("component_row_credit", ledger_mutator(COMPONENT_LEDGER, "post_component_official_key_assignment", lambda x: x.__setitem__("formal_credit", 1)), "normal"),
        ("component_historical_role", ledger_mutator(COMPONENT_LEDGER, "post_component_official_key_assignment", lambda x: x.__setitem__("C25_fresh_component_id_role", "CURRENT_AUTHORITY")), "normal"),
        ("component_key_count", ledger_mutator(COMPONENT_LEDGER, "post_component_official_key_assignment", lambda x: x.__setitem__("official_key_count", x["official_key_count"] + 1)), "normal"),
        ("component_post_id", ledger_mutator(COMPONENT_LEDGER, "post_component_official_key_assignment", lambda x: x.__setitem__("post_C27R2_component_id", "round306c27r2-source-g-post-component:" + "0" * 64)), "normal"),
        ("fibre_row_credit", ledger_mutator(FIBRE_LEDGER, "official_key_fibre_exhaustion", lambda x: x.__setitem__("formal_credit", 1)), "normal"),
        ("fibre_residual", ledger_mutator(FIBRE_LEDGER, "official_key_fibre_exhaustion", lambda x: x.__setitem__("global_transition_residual_count", 1)), "normal"),
        ("fibre_incidence", ledger_mutator(FIBRE_LEDGER, "official_key_fibre_exhaustion", lambda x: x.__setitem__("post_C27R2_component_incidence_count", x["post_C27R2_component_incidence_count"] + 1)), "normal"),
        ("disposition_row_credit", ledger_mutator(DISPOSITION_LEDGER, "global_member_disposition", lambda x: x.__setitem__("formal_credit", 1)), "normal"),
        ("disposition_post_id", ledger_mutator(DISPOSITION_LEDGER, "global_member_disposition", lambda x: x.__setitem__("post_C27R2_component_id", "round306c27r2-source-g-post-component:" + "f" * 64)), "normal"),
        ("disposition_historical_role", ledger_mutator(DISPOSITION_LEDGER, "global_member_disposition", lambda x: x.__setitem__("historical_component_binding_role", "CURRENT_AUTHORITY")), "normal"),
        ("gzip_truncation_reclosed_descriptor", truncate_gzip, "normal"),
        ("extra_inventory", extra_file, "normal"),
        ("symlink_substitution", symlink_member, "normal"),
        ("hardlink_extra_inventory", hardlink_extra, "normal"),
        ("wrong_C27R2_external_root_pin", lambda _x: None, "wrong_c27_pin"),
        ("wrong_C28_external_root_pin", lambda _x: None, "wrong_c28_pin"),
        ("terminal_role_swap", lambda _x: None, "swap_terminals"),
    ]


def verifier_command(args: argparse.Namespace, candidate: Path, output: Path, mode: str) -> list[str]:
    c27_dir = args.c27r2_terminal_dir
    c28_dir = args.c28_terminal_dir
    c27_root = args.expect_c27r2_root_sha256
    c28_root = args.expect_c28_root_sha256
    if mode == "wrong_c27_pin":
        c27_root = "0" * 64 if c27_root != "0" * 64 else "1" * 64
    elif mode == "wrong_c28_pin":
        c28_root = "f" * 64 if c28_root != "f" * 64 else "e" * 64
    elif mode == "swap_terminals":
        c27_dir, c28_dir = c28_dir, c27_dir
    return [
        args.python, "-I", "-B", args.verifier,
        "--c27r2-terminal-dir", c27_dir,
        "--expect-c27r2-root-sha256", c27_root,
        "--expect-c27r2-receipt-file-sha256", args.expect_c27r2_receipt_file_sha256,
        "--expect-c27r2-receipt-object-sha256", args.expect_c27r2_receipt_object_sha256,
        "--c28-terminal-dir", c28_dir,
        "--expect-c28-root-sha256", c28_root,
        "--expect-c28-receipt-file-sha256", args.expect_c28_receipt_file_sha256,
        "--expect-c28-receipt-object-sha256", args.expect_c28_receipt_object_sha256,
        "--candidate-dir", str(candidate), "--out-file", str(output),
    ]


def regular(path: Path, label: str) -> Path:
    lexical = path.absolute()
    actual = lexical.resolve(strict=True)
    need(lexical == actual and actual.is_file() and not actual.is_symlink(), label)
    return actual


def run(args: argparse.Namespace) -> dict[str, Any]:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True,
         "isolated Python -I -B runtime")
    verifier = regular(Path(args.verifier), "verifier source")
    python = regular(Path(args.python), "Python binary")
    harness = regular(SELF, "harness source")
    need(file_sha(verifier) == args.expect_verifier_sha256,
         "verifier source external pin")
    need(file_sha(python) == args.expect_python_sha256, "Python external pin")
    need(file_sha(harness) == args.expect_harness_sha256, "harness self external pin")
    candidate = Path(args.candidate_dir).absolute()
    need(candidate.resolve(strict=True) == candidate and candidate.is_relative_to(ROOT)
         and candidate.is_dir() and {entry.name for entry in candidate.iterdir()} == FILES,
         "immutable source candidate exact inventory")
    before = {name: file_sha(candidate / name) for name in sorted(FILES)}
    work = Path(args.work_dir).absolute()
    result_file = Path(args.result_file).absolute()
    need(work.is_relative_to(ROOT) and result_file.is_relative_to(ROOT)
         and not work.exists() and not result_file.exists(), "fresh harness outputs")
    work.mkdir(parents=True, mode=0o700)

    receipts: list[dict[str, Any]] = []
    for ordinal, (name, mutate, mode) in enumerate(attacks()):
        case = work / f"attack-{ordinal:02d}-{name}"
        clone_candidate(candidate, case)
        mutate(case)
        output = case / "verification.json"
        command = verifier_command(args, case, output, mode)
        environment = {
            "HOME": str(work), "LANG": "C", "LC_ALL": "C",
            "PATH": "/usr/bin:/bin", "PYTHONHASHSEED": str(730001 + ordinal),
        }
        process = subprocess.run(
            command, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout_seconds,
            check=False,
        )
        need(process.returncode == 2 and process.stdout == b""
             and process.stderr.startswith(b"REJECT:")
             and not output.exists(), "attack rejected fail-closed:" + name)
        receipts.append({
            "ordinal": ordinal, "attack": name, "mode": mode,
            "exit_code": process.returncode,
            "stdout_sha256": hashlib.sha256(process.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(process.stderr).hexdigest(),
            "verification_output_created": False,
            "rejected": True,
        })
    after = {name: file_sha(candidate / name) for name in sorted(FILES)}
    need(before == after, "source candidate pre/post SHA identical")
    body = {
        "schema": HARNESS_SCHEMA,
        "status": "PASS_28_OF_28_C29_V2_COHERENT_CANDIDATE_AND_AUTHORITY_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_census": {"required": 28, "rejected": len(receipts), "accepted": 0},
        "attacks": receipts,
        "source_candidate_pre_sha256": before,
        "source_candidate_post_sha256": after,
        "source_candidate_unchanged": True,
        "verifier_sha256": args.expect_verifier_sha256,
        "python_sha256": args.expect_python_sha256,
        "harness_sha256": args.expect_harness_sha256,
        "formal_credit": 0,
        "manifest_authorized": False,
        "C29": "UNAUTHORIZED_PENDING_RELEASE_ONLY_ATTACKS_AND_TERMINAL_SEAL",
        "Source_W": "UNCHANGED_BY_SOURCE_G_C29_V2_ATTACKS",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    result = dict(body)
    result["attacks_sha256"] = object_sha(result)
    result_file.parent.mkdir(parents=True, exist_ok=True)
    with result_file.open("xb") as output:
        output.write(canonical(result) + b"\n")
        output.flush()
        os.fsync(output.fileno())
    return result


def self_test() -> dict[str, Any]:
    need(len(attacks()) == 28 and len({name for name, _action, _mode in attacks()}) == 28,
         "self-test attack catalog")
    with tempfile.TemporaryDirectory(prefix="cm2-c29-v2-attacks-") as name:
        path = Path(name) / "result.json"
        body = {
            "schema": RESULT_SCHEMA, "formal_credit": 0,
            "theorem": {"component_key_incidences_recomputed_not_imported": True},
            "theorem_sha256": object_sha({
                "component_key_incidences_recomputed_not_imported": True,
            }),
        }
        value = dict(body)
        value["result_sha256"] = object_sha(value)
        path.write_bytes(canonical(value) + b"\n")
        need(closed_result(path)["formal_credit"] == 0, "self-test initial closure")
        value["formal_credit"] = 1
        write_result(path, value)
        need(closed_result(path)["formal_credit"] == 1, "self-test coherent reclosure")
    return {
        "schema": HARNESS_SCHEMA + ".self-test",
        "status": "PASS_C29_V2_28_ATTACK_CATALOG_AND_RECLOSURE_FIXTURE",
        "attack_count": 28, "formal_credit": 0,
        "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--self-test", action="store_true")
    value.add_argument("--python")
    value.add_argument("--expect-python-sha256")
    value.add_argument("--verifier")
    value.add_argument("--expect-verifier-sha256")
    value.add_argument("--expect-harness-sha256")
    value.add_argument("--c27r2-terminal-dir")
    value.add_argument("--expect-c27r2-root-sha256")
    value.add_argument("--expect-c27r2-receipt-file-sha256")
    value.add_argument("--expect-c27r2-receipt-object-sha256")
    value.add_argument("--c28-terminal-dir")
    value.add_argument("--expect-c28-root-sha256")
    value.add_argument("--expect-c28-receipt-file-sha256")
    value.add_argument("--expect-c28-receipt-object-sha256")
    value.add_argument("--candidate-dir")
    value.add_argument("--work-dir")
    value.add_argument("--result-file")
    value.add_argument("--timeout-seconds", type=int, default=7200)
    return value


def main() -> int:
    args = parser().parse_args()
    fields = (
        "python", "expect_python_sha256", "verifier", "expect_verifier_sha256",
        "expect_harness_sha256", "c27r2_terminal_dir",
        "expect_c27r2_root_sha256", "expect_c27r2_receipt_file_sha256",
        "expect_c27r2_receipt_object_sha256", "c28_terminal_dir",
        "expect_c28_root_sha256", "expect_c28_receipt_file_sha256",
        "expect_c28_receipt_object_sha256", "candidate_dir", "work_dir", "result_file",
    )
    try:
        if args.self_test:
            need(all(getattr(args, field) is None for field in fields),
                 "self-test has no authority/candidate arguments")
            result = self_test()
        else:
            need(all(getattr(args, field) is not None for field in fields)
                 and type(args.timeout_seconds) is int and args.timeout_seconds > 0,
                 "all pinned authority/candidate/harness arguments required")
            result = run(args)
        sys.stdout.buffer.write(canonical({
            "status": result["status"], "formal_credit": 0,
            "C29": result.get("C29", "UNAUTHORIZED"), "CM2": "NO-GO_FOR_CLAIM",
        }) + b"\n")
        return 0
    except (Failure, OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
