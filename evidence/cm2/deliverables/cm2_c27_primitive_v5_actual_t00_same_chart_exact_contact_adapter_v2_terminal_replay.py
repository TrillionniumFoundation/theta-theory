#!/usr/bin/env python3
"""Cold terminal replay for the corrected T00 v2 zero-credit seal."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
RECEIPT_PIN = "38e48470d487d65e6a70433bebc67f3e2068715aaf4bd4e008ca89d1ed128dc7"
RECEIPT_OBJECT = "8c13783792d9b9cd1752ef2f89f3cb7ac74499c92d33fc68c9cde64bab6b011e"
PAYLOAD_PIN = "9b043a567323366dccbd5b4acd7b6dac09655822493bf0a38437bc7925a9eb82"
ROOT_PIN = "18ea6e69afe11e14ef26318a411048b3ab606b42ed3d2eebac2b26d2056b5c8f"
PYTHON = Path("/usr/bin/python3.12")
PYTHON_SHA = "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
SEED2_RECEIPT = ROOT / ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647991-attempt1/adapter_receipt.json"
RUN_DIRS = {
    "seed1": ROOT / ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647101-attempt2-run",
    "seed2": ROOT / ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-seed30647991-attempt1-run",
    "verifier": ROOT / ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-independent-verifier-run",
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def stat_wire(path: Path) -> list[int]:
    info = path.stat()
    return [info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid]


def root_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    need(ROOT in path.parents, "payload path inside workspace")
    return path


def byte_identical(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as a, right.open("rb") as b:
        while True:
            x, y = a.read(4 << 20), b.read(4 << 20)
            if x != y:
                return False
            if not x:
                return True


def parse_manifest(path: Path) -> list[tuple[str, str]]:
    rows = []
    previous = None
    for ordinal, line in enumerate(path.read_text("ascii").splitlines()):
        pieces = line.split("  ", 1)
        need(len(pieces) == 2 and len(pieces[0]) == 64,
             f"manifest row:{ordinal}")
        need(previous is None or previous < line, "manifest strict ordering")
        previous = line
        rows.append((pieces[0], pieces[1]))
    return rows


def closed_document(path: Path, closure: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claim = body.pop(closure, None)
    need(type(claim) is str and claim == digest(body),
         "document closure:" + path.name)
    return value


def verify_descriptor(desc: dict[str, Any]) -> dict[str, Any]:
    path = root_path(desc["path"])
    need(path.is_file() and path.stat().st_size == desc["size"]
         and fsha(path) == desc["sha256"], "descriptor file:" + path.name)
    count = 0
    sequence = hashlib.sha256()
    previous = None
    with gzip.open(path, "rb") as stream:
        for line in stream:
            need(line.endswith(b"\n"), "ledger newline:" + path.name)
            payload = line[:-1]
            row = json.loads(payload)
            need(canonical(row) == payload and row["schema"] == desc["row_schema"],
                 "ledger canonical/schema:" + path.name)
            body = dict(row)
            claim = body.pop("row_sha256", None)
            need(type(claim) is str and claim == digest(body),
                 "ledger closure:" + path.name)
            need(row["ordinal"] == count, "ledger ordinal:" + path.name)
            key = row["candidate_key"]
            need(previous is None or previous < key,
                 "candidate ordering:" + path.name)
            previous = key
            sequence.update(claim.encode("ascii") + b"\n")
            count += 1
    need(count == desc["row_count"]
         and sequence.hexdigest() == desc["row_sequence_sha256"],
         "descriptor census/sequence:" + path.name)
    return {"path": desc["path"], "rows": count,
            "sha256": desc["sha256"]}


def verify_run_files(label: str, expected: dict[str, Any]) -> None:
    directory = RUN_DIRS[label]
    paths = {"command_file_sha256": directory / "command.json",
             "stdout_file_sha256": directory / "stdout.log",
             "stderr_file_sha256": directory / "stderr.log",
             "exit_code_file_sha256": directory / "exit_code.txt"}
    need(all(path.is_file() and fsha(path) == expected[key]
             for key, path in paths.items()), "run file pins:" + label)
    need(json.loads(paths["command_file_sha256"].read_bytes())
         == expected["argv"], "run argv:" + label)
    need(paths["stderr_file_sha256"].read_bytes() == b""
         and paths["exit_code_file_sha256"].read_bytes() == b"0\n"
         and len(paths["stdout_file_sha256"].read_bytes().splitlines()) == 1,
         "run exit/stderr/stdout:" + label)


def replay(seal: Path) -> dict[str, Any]:
    need(all(pin != "PENDING" for pin in
             (RECEIPT_PIN, RECEIPT_OBJECT, PAYLOAD_PIN, ROOT_PIN)),
         "seal pins finalized")
    receipt_path = seal / "receipt.json"
    payload_path = seal / "payload_manifest.sha256"
    root_manifest = seal / "root_manifest.sha256"
    need(fsha(receipt_path) == RECEIPT_PIN
         and fsha(payload_path) == PAYLOAD_PIN
         and fsha(root_manifest) == ROOT_PIN, "seal file pins")
    receipt = closed_document(receipt_path, "receipt_sha256")
    need(receipt["receipt_sha256"] == RECEIPT_OBJECT
         and receipt["formal_credit"] == 0
         and receipt["manifest_authorized"] is False
         and receipt["dual_seed"]["all_ledgers_byte_identical"] is True
         and receipt["dual_seed"]["ledger_pair_count"] == 3
         and receipt["coherent_attacks"]["attacks"]
             == receipt["coherent_attacks"]["rejected"] == 22,
         "receipt closure/governance")
    exact = receipt["exact_census"]
    need(exact["candidate_count"] == 5_970_840
         and exact["lower_cross_component_candidate_count"] == 2_598_666
         and exact["lower_same_component_candidate_count"] == 3_185_042
         and exact["strict_cross_component_physical_proof_count"] == 32_240
         and exact["unique_component_edge_count"] == 14_772,
         "receipt exact census")
    payload_rows = parse_manifest(payload_path)
    need(len(payload_rows) == receipt["payload_manifest"]["entry_count"]
         and receipt["payload_manifest"]["file_sha256"] == PAYLOAD_PIN,
         "payload receipt binding")
    root_expected = "".join(sorted((
        f"{PAYLOAD_PIN}  {payload_path.relative_to(ROOT)}\n",
        f"{RECEIPT_PIN}  {receipt_path.relative_to(ROOT)}\n",
    ))).encode("ascii")
    need(root_manifest.read_bytes() == root_expected, "exact root manifest")
    pre = {}
    for pin, relative in payload_rows:
        path = root_path(relative)
        need(path.is_file() and fsha(path) == pin,
             "payload member:" + relative)
        pre[relative] = {"sha256": pin, "stat": stat_wire(path)}
    need(PYTHON.is_file() and fsha(PYTHON) == PYTHON_SHA
         and Path(shutil.which("python") or "").resolve() == PYTHON
         and receipt["runtime_and_argv_closure"]["resolved_runtime"]
             == str(PYTHON)
         and receipt["runtime_and_argv_closure"]["runtime_sha256"]
             == PYTHON_SHA,
         "runtime binding")
    for label, expected in (receipt["runtime_and_argv_closure"]
                            ["run_evidence"].items()):
        verify_run_files(label, expected)

    second = closed_document(SEED2_RECEIPT, "receipt_sha256")
    need(fsha(SEED2_RECEIPT) == receipt["dual_seed"]
                                  ["seed2_receipt_file_sha256"]
         and second["receipt_sha256"] == receipt["dual_seed"]
                                         ["seed2_receipt_object_sha256"],
         "seed2 receipt binding")
    verified = []
    for key in ("primitive_authority_ledger", "candidate_ownership_ledger",
                "materialized_physical_proof_fragment_ledger"):
        left = receipt["terminal_adapter"][key]
        right = second["terminal_adapter"][key]
        need({k: left[k] for k in left if k != "path"}
             == {k: right[k] for k in right if k != "path"}
             and byte_identical(root_path(left["path"]),
                                root_path(right["path"])),
             "dual ledger identity:" + key)
        verified.append(verify_descriptor(left))
    post = {}
    for pin, relative in payload_rows:
        path = root_path(relative)
        post[relative] = {"sha256": fsha(path), "stat": stat_wire(path)}
        need(post[relative] == pre[relative],
             "pre/post identity:" + relative)
    stable = {"payload_entry_count": len(payload_rows),
              "replayed_ledger_count": len(verified),
              "replayed_row_count": sum(item["rows"] for item in verified),
              "dual_seed_byte_identical_ledger_count": 3,
              "pre_post_sha256_identical": True,
              "pre_post_stat_identical": True}
    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-terminal-replay.v1",
        "status": "PASS_COLD_ROOT_PAYLOAD_RUNTIME_ARGV_AND_THREE_LEDGER_REPLAY__PRE_POST_IDENTICAL__ZERO_CREDIT",
        "receipt_file_sha256": RECEIPT_PIN,
        "receipt_sha256": RECEIPT_OBJECT,
        "payload_manifest_file_sha256": PAYLOAD_PIN,
        "root_manifest_file_sha256": ROOT_PIN,
        "exact_census": stable, "verified_ledgers": verified,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "replay_source_sha256": fsha(Path(__file__).resolve()),
    }
    result = dict(body)
    result["result_sha256"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    try:
        need(not output.exists(), "fresh replay output")
        result = replay(Path(args.seal_dir).resolve())
        output.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                     | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(fd, canonical(result) + b"\n")
            os.fsync(fd)
        finally:
            os.close(fd)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "exact_census": result["exact_census"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
