#!/usr/bin/env python3
"""Stable-FD primitive rebuild of the 91,672 current-support pair universe.

The pinned v3 geometry engine is executed from primitive inputs while every
root input is held on one O_NOFOLLOW descriptor.  Its path-oriented input
entrypoints are replaced by same-descriptor hash/parse/fstat readers.  The
55,532 freshly reconstructed positive pairs are then joined to raw SIGNED and
COMPLETE primitive pair sets and assigned by exact priority.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import redirect_stdout
from dataclasses import dataclass
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import sys
import types
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "deliverables/cm2_c27_three_terminal_current_full_support_totality_v3_probe.py"
ENGINE_SHA256 = "57f41d9d35157801078f1dc75aa53dd10f7c4e6ad223bd164840a27a4b9145f0"


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


def closed(body: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in body, "fresh row")
    return {**body, "row_sha256": digest(body)}


def check_closed(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claimed = body.pop("row_sha256", None)
    need(type(claimed) is str and claimed == digest(body), label + ":closure")


def fp(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    pre: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str | None) -> "Capture":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            if expected is not None:
                need(observed == expected, label + ":pin")
            need(fp(os.fstat(fd)) == fp(before), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, path.resolve(), fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def unchanged(self, phase: str) -> None:
        need(fp(os.fstat(self.fd)) == self.pre, self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.unchanged("raw")
        return b"".join(pieces)

    def jsonl(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:newline:{ordinal}")
                    encoded = line[:-1]
                    row = json.loads(encoded)
                    need(type(row) is dict and canonical(row) == encoded,
                         f"{self.label}:canonical:{ordinal}")
                    check_closed(row, f"{self.label}:{ordinal}")
                    yield row
        self.unchanged("jsonl")

    def document_rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as zipped:
                stream = io.TextIOWrapper(zipped, encoding="utf-8")
                marker = '"rows":['
                buffer = ""
                while marker not in buffer:
                    piece = stream.read(1 << 20)
                    need(bool(piece), self.label + ":rows marker")
                    buffer += piece
                    if len(buffer) > (6 << 20):
                        buffer = buffer[-(3 << 20):]
                buffer = buffer.split(marker, 1)[1]
                decoder = json.JSONDecoder()
                ordinal = 0
                while True:
                    buffer = buffer.lstrip()
                    if not buffer:
                        piece = stream.read(1 << 20)
                        need(bool(piece), self.label + ":EOF")
                        buffer = piece
                        continue
                    if buffer[0] == ",":
                        buffer = buffer[1:]
                        continue
                    if buffer[0] == "]":
                        break
                    try:
                        row, end = decoder.raw_decode(buffer)
                    except json.JSONDecodeError:
                        piece = stream.read(1 << 20)
                        need(bool(piece), self.label + ":malformed")
                        buffer += piece
                        continue
                    need(type(row) is dict, self.label + ":row object")
                    check_closed(row, f"{self.label}:{ordinal}")
                    yield row
                    ordinal += 1
                    buffer = buffer[end:]
        self.unchanged("document rows")

    def receipt(self) -> dict[str, Any]:
        self.unchanged("final")
        return {"path": str(self.path.relative_to(ROOT)), "sha256": self.sha256,
                "stat_fingerprint": list(self.pre), "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def unordered(left: str, right: str) -> tuple[str, str]:
    need(type(left) is str and type(right) is str and left != right, "nonself pair")
    return (left, right) if left < right else (right, left)


def write_rows(path: Path, rows: Iterator[dict[str, Any]]) -> tuple[int, str, str]:
    count = 0
    sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
            for row in rows:
                stream.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                count += 1
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return count, state.hexdigest(), sequence.hexdigest()


def run(args: argparse.Namespace) -> dict[str, Any]:
    need(not Path(args.out_dir).exists(), "fresh output directory")
    need(not Path(args.scratch_dir).exists(), "fresh scratch directory")
    captures: dict[str, Capture] = {}
    try:
        captures["primitive_engine_source"] = Capture.open(
            "primitive_engine_source", ENGINE, ENGINE_SHA256
        )
        engine_bytes = captures["primitive_engine_source"].raw()
        module_name = "cm2_current_support_v3_pinned_stable_fd"
        module = types.ModuleType(module_name)
        module.__file__ = str(ENGINE)
        sys.modules[module_name] = module
        exec(compile(engine_bytes, str(ENGINE), "exec"), module.__dict__)
        captures["primitive_engine_source"].unchanged("post compile/exec")
        for name, expected in module.PINS.items():
            captures[name] = Capture.open(name, module.ROOT / name, expected)
        crosswalk = Path(args.crosswalk).resolve()
        identity_result = Path(args.identity_result).resolve()
        captures["v3_crosswalk"] = Capture.open(
            "v3_crosswalk", crosswalk, args.crosswalk_sha256
        )
        captures["v3_identity_result"] = Capture.open(
            "v3_identity_result", identity_result, args.identity_result_sha256
        )
        by_path = {str(capture.path): capture for capture in captures.values()}

        def lookup(path: Path) -> Capture | None:
            return by_path.get(str(Path(path).resolve()))

        original_file_hash = module.file_hash
        original_stat = module.stat_fingerprint
        original_read_bytes = Path.read_bytes

        def stable_file_hash(path: Path) -> str:
            capture = lookup(path)
            if capture is None:
                return original_file_hash(path)
            capture.unchanged("file_hash")
            return capture.sha256

        def stable_stat(path: Path) -> tuple[int, ...]:
            capture = lookup(path)
            return capture.pre if capture is not None else original_stat(path)

        def stable_jsonl(path: Path) -> Iterator[dict[str, Any]]:
            capture = lookup(path)
            need(capture is not None, "registered jsonl root:" + str(path))
            yield from capture.jsonl()

        def stable_document_rows(path: Path) -> Iterator[dict[str, Any]]:
            capture = lookup(path)
            need(capture is not None, "registered document root:" + str(path))
            yield from capture.document_rows()

        def stable_result_object(name: str) -> dict[str, Any]:
            capture = captures[name]
            raw = capture.raw()
            value = json.loads(raw)
            need(type(value) is dict and canonical(value) + b"\n" == raw,
                 name + ":canonical result")
            body = dict(value)
            claimed = body.pop("result_sha256", None)
            need(type(claimed) is str and claimed == digest(body), name + ":result closure")
            return value

        def stable_certificate_result(name: str) -> dict[str, Any]:
            document = json.loads(captures[name].raw())
            need(type(document) is dict
                 and set(document) == {"schema", "result", "result_sha256"}
                 and document["result_sha256"] == digest(document["result"]),
                 name + ":certificate closure")
            return document["result"]

        def stable_read_bytes(path: Path) -> bytes:
            capture = lookup(path)
            return capture.raw() if capture is not None else original_read_bytes(path)

        module.file_hash = stable_file_hash
        module.stat_fingerprint = stable_stat
        module.jsonl = stable_jsonl
        module.document_rows = stable_document_rows
        module.result_object = stable_result_object
        module.certificate_result = stable_certificate_result
        Path.read_bytes = stable_read_bytes
        old_argv = sys.argv
        output = Path(args.out_dir)
        inner = output / "primitive_scan"
        try:
            sys.argv = [str(ENGINE), "--out-dir", str(inner),
                        "--scratch-dir", args.scratch_dir,
                        "--crosswalk", str(crosswalk),
                        "--crosswalk-sha256", args.crosswalk_sha256,
                        "--identity-result", str(identity_result),
                        "--identity-result-sha256", args.identity_result_sha256,
                        "--seed", str(args.seed)]
            captured_stdout = io.StringIO()
            with redirect_stdout(captured_stdout):
                status = module.main()
        finally:
            sys.argv = old_argv
            Path.read_bytes = original_read_bytes
        need(status == 0, "primitive engine execution")

        inner_result_path = inner / "result.json"
        captures["self_produced_inner_result"] = Capture.open(
            "self_produced_inner_result", inner_result_path, None
        )
        inner_result_raw = captures["self_produced_inner_result"].raw()
        inner_result = json.loads(inner_result_raw)
        body = dict(inner_result)
        claimed = body.pop("result_sha256")
        need(claimed == digest(body)
             and inner_result["independent_current_C19_scan"]["distinct_member_positive_pair_count"] == 55_532,
             "primitive positive scan result")

        positive_path = inner / "current_new_C19_carrier_exact_positive_pair_universe.jsonl.gz"
        captures["self_produced_positive_ledger"] = Capture.open(
            "self_produced_positive_ledger", positive_path, None
        )
        positive: dict[tuple[str, str], dict[str, Any]] = {}
        for row in captures["self_produced_positive_ledger"].jsonl():
            pair = unordered(row["left_member_id"], row["right_member_id"])
            need(pair not in positive, "positive unique pair")
            positive[pair] = row
        need(len(positive) == 55_532, "positive pair census")
        positive_file_sha = captures["self_produced_positive_ledger"].sha256
        need(positive_file_sha == inner_result["independent_current_C19_scan"]["pair_ledger_file_sha256"],
             "positive ledger/result binding")

        signed: set[tuple[str, str]] = set()
        signed_self = signed_rows = 0
        for row in captures[module.SIGNED].document_rows():
            signed_rows += 1
            if row["decision"].startswith("ACCEPT_"):
                left, right = row["left_formal_occurrence_id"], row["right_formal_occurrence_id"]
                if left == right:
                    signed_self += 1
                else:
                    signed.add(unordered(left, right))
        need(signed_rows == 43_092 and signed_self == 2_092 and len(signed) == 25_452,
             "SIGNED primitive pair census")

        complete: set[tuple[str, str]] = set()
        complete_rows = complete_self = complete_raw_nonself = 0
        for row in captures[module.COMPLETE].document_rows():
            complete_rows += 1
            if row["decision"].startswith("ACCEPT_"):
                for left in row["left_formal_occurrence_endpoints"]:
                    for right in row["right_formal_occurrence_endpoints"]:
                        if left == right:
                            complete_self += 1
                        else:
                            complete_raw_nonself += 1
                            complete.add(unordered(left, right))
        need(complete_rows == 62_548 and complete_self == 15_056
             and complete_raw_nonself == 91_760 and len(complete) == 36_140
             and signed <= complete, "COMPLETE primitive pair census")
        need(not (set(positive) & signed) and not (set(positive) & complete),
             "positive disjoint from SIGNED and COMPLETE")

        c15: dict[str, str] = {}
        for row in captures[module.C15].jsonl():
            c15[row["registry_member_id"]] = row["fresh_component_id"]
        c25: dict[str, str] = {}
        for row in captures[module.C25].jsonl():
            c25[row["member_id"]] = row["source_bindings"]["support_kernel"]
        need(len(c15) == len(c25) == 502_204, "current member authority census")

        universe = complete | set(positive)
        need(len(universe) == 91_672, "91,672 exact union")
        assignment = Counter()

        def route_rows() -> Iterator[dict[str, Any]]:
            for left, right in sorted(universe):
                terminal = ("SIGNED_BOUNDARY_FACES" if (left, right) in signed else
                            "COMPLETE_BOUNDARY_FACES" if (left, right) in complete else
                            "POSITIVE_VOLUME_CARRIERS")
                assignment[terminal] += 1
                need(left in c15 and right in c15 and left in c25 and right in c25,
                     "current endpoint authority")
                yield closed({
                    "assigned_terminal": terminal,
                    "current_C15_components": [c15[left], c15[right]],
                    "current_C25_support_kernels": [c25[left], c25[right]],
                    "formal_credit": 0,
                    "left_member_id": left,
                    "pair_assignment_rule": "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE",
                    "positive_source_branch": (
                        "CURRENT_C19_PHYSICAL_SUPPORT" if (left, right) in positive else None
                    ),
                    "positive_primitive_row_sha256": (
                        positive[(left, right)]["row_sha256"] if (left, right) in positive else None
                    ),
                    "raw_complete_face_evidence": (left, right) in complete,
                    "raw_positive_C19_physical_support_evidence": (left, right) in positive,
                    "raw_signed_face_evidence": (left, right) in signed,
                    "right_member_id": right,
                    "same_current_C15_component": c15[left] == c15[right],
                    "schema": "cm2.c27-independent.current-support-91672-priority.row.v1",
                })

        route_path = output / "current_support_91672_unique_priority_routes.jsonl.gz"
        route_count, route_sha, route_sequence = write_rows(route_path, route_rows())
        need(route_count == 91_672 and assignment == {
            "SIGNED_BOUNDARY_FACES": 25_452,
            "COMPLETE_BOUNDARY_FACES": 10_688,
            "POSITIVE_VOLUME_CARRIERS": 55_532,
        }, "unique priority assignment census")

        result_body = {
            "schema": "cm2.c27-independent.current-support-91672-stable-fd.v4",
            "status": "PASS_PRIMITIVE_CURRENT_SUPPORT_91672_UNIQUE_PRIORITY__CROSS_COMPONENT_WITNESS_FULL_REBUILD_REQUIRED__ZERO_CREDIT",
            "invocation_seed": args.seed,
            "primitive_pair_sets": {
                "SIGNED": 25_452,
                "COMPLETE": 36_140,
                "COMPLETE_only": 10_688,
                "POSITIVE_C19": 55_532,
                "SIGNED_subset_COMPLETE": True,
                "POSITIVE_intersection_SIGNED": 0,
                "POSITIVE_intersection_COMPLETE": 0,
                "union": 91_672,
            },
            "unique_priority_assignment_census": dict(sorted(assignment.items())),
            "priority_ledger": {"filename": route_path.name, "row_count": route_count,
                                "file_sha256": route_sha,
                                "row_sequence_sha256": route_sequence},
            "fresh_positive_primitive_scan": {
                "engine_source_sha256": ENGINE_SHA256,
                "positive_pair_count": 55_532,
                "same_current_C15_component_pair_count": 23_520,
                "cross_current_C15_component_pair_count": 32_012,
                "positive_ledger_path": str(positive_path.relative_to(output)),
                "positive_ledger_file_sha256": positive_file_sha,
                "inner_result_file_sha256": hashlib.sha256(inner_result_raw).hexdigest(),
                "inner_result_sha256": claimed,
                "legacy_path_capture_warning_superseded_by_outer_stable_fd_adapter": True,
            },
            "candidate_governance": {
                "C27_FAMILIES_imported_or_read": False,
                "edge_ledger_used_as_candidate_universe": False,
                "R300C_used_only_as_validation": True,
                "R300C_used_as_candidate_universe": False,
                "candidate_prefilter": "PHYSICAL_CHART_ONLY_FOR_POSITIVE_C19_PRIMITIVE_SCAN",
            },
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "entrypoints_replaced": ["file_hash", "stat_fingerprint", "jsonl",
                                          "document_rows", "result_object",
                                          "certificate_result", "Path.read_bytes"],
                "attestations": {label: capture.receipt()
                                 for label, capture in sorted(captures.items())},
            },
            "C27_C28_C29": "FULL_REBUILD_REQUIRED__UNION_ALL_LEGAL_WITNESS_BRANCHES__NO_PATCH_PROMOTION",
            "formal_credit": 0,
            "manifest_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = dict(result_body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in result_body.items()
            if key not in {"invocation_seed", "root_input_capture"}
        })
        result["result_sha256"] = digest(result)
        (output / "result.json").write_bytes(canonical(result) + b"\n")
        return result
    finally:
        for capture in captures.values():
            capture.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--scratch-dir", required=True)
    parser.add_argument("--crosswalk", required=True)
    parser.add_argument("--crosswalk-sha256", required=True)
    parser.add_argument("--identity-result", required=True)
    parser.add_argument("--identity-result-sha256", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result = run(args)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "semantic_projection_sha256": result["semantic_projection_sha256"],
                     "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
