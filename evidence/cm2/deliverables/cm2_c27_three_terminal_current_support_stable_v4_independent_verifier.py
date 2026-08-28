#!/usr/bin/env python3
"""Independent sweep-line verifier for the stable 91,672 current universe.

This verifier does not import the producer or its pinned geometry engine.  It
reconstructs every physical C19×C22 and transformed C19×C23 overlap using an
event sweep, rebuilds SIGNED and COMPLETE pair sets, and verifies both seeded
priority ledgers row by row.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "C15": ("deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz", "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    "C25": ("deliverables/cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz", "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6"),
    "C22A": ("deliverables/cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz", "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb"),
    "C23A": ("deliverables/cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz", "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528"),
    "SIGNED": ("deliverables/cm2_round299_source_g_r292_signed_support_face_classifier_independent_probe_ledger.json.gz", "9797d486eaf96ce8352883093c24637b5eb9cb27af60fd79e5ee03a6585d27a9"),
    "COMPLETE": ("deliverables/cm2_round300b_source_g_registry_boundary_and_complete_r275_face_inventory_closure_face_inventory.json.gz", "443f26bdbed929d873972be0d2232809bf022feed1a5709001ee8f2dda49ac2d"),
    "crosswalk": (".cm2-runtime/audit/c27-three-terminal-current-support-crosswalk-v3-seed-30632101-retry6/payload/current_C19_51172_chart_sign_identity_crosswalk.jsonl.gz", "958a71b578089f4a9c2a31d77a65795130902fd2af0626135b264fc1da55f56b"),
}

# Exact leaf whitelist for run-local/non-semantic differences between the two
# primary materializations.  The producer's older semantic_projection_sha256
# included several of these leaves, so it is verified as a closed result field
# but deliberately superseded by this independently normalized projection.
RUN_LOCAL_DIFFERENCE_WHITELIST = (
    "/fresh_positive_primitive_scan/inner_result_file_sha256",
    "/fresh_positive_primitive_scan/inner_result_sha256",
    "/invocation_seed",
    "/result_sha256",
    "/root_input_capture/attestations/self_produced_inner_result/path",
    "/root_input_capture/attestations/self_produced_inner_result/sha256",
    "/root_input_capture/attestations/self_produced_inner_result/stat_fingerprint/1",
    "/root_input_capture/attestations/self_produced_inner_result/stat_fingerprint/3",
    "/root_input_capture/attestations/self_produced_inner_result/stat_fingerprint/4",
    "/root_input_capture/attestations/self_produced_positive_ledger/path",
    "/root_input_capture/attestations/self_produced_positive_ledger/stat_fingerprint/1",
    "/root_input_capture/attestations/self_produced_positive_ledger/stat_fingerprint/3",
    "/root_input_capture/attestations/self_produced_positive_ledger/stat_fingerprint/4",
    "/semantic_projection_sha256",
)


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


def difference_paths(left: Any, right: Any, path: str = "") -> set[str]:
    if type(left) is not type(right):
        return {path or "/"}
    if isinstance(left, dict):
        if set(left) != set(right):
            return {path or "/"}
        result: set[str] = set()
        for key in sorted(left):
            result |= difference_paths(left[key], right[key], path + "/" + key)
        return result
    if isinstance(left, list):
        if len(left) != len(right):
            return {path or "/"}
        result = set()
        for index, (a, b) in enumerate(zip(left, right)):
            result |= difference_paths(a, b, path + "/" + str(index))
        return result
    return set() if left == right else {path or "/"}


def normalized_result(value: dict[str, Any]) -> dict[str, Any]:
    copy = json.loads(canonical(value))
    for pointer in RUN_LOCAL_DIFFERENCE_WHITELIST:
        parts = pointer.strip("/").split("/")
        cursor: Any = copy
        for part in parts[:-1]:
            cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
        last = parts[-1]
        if isinstance(cursor, list):
            cursor[int(last)] = "__WHITELISTED_RUN_LOCAL_LEAF__"
        else:
            cursor[last] = "__WHITELISTED_RUN_LOCAL_LEAF__"
    return copy


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
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
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
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        self.unchanged("raw")
        return b"".join(chunks)

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
                import io
                with io.TextIOWrapper(zipped, encoding="utf-8") as stream:
                    marker = '"rows":['
                    buffer = ""
                    while marker not in buffer:
                        piece = stream.read(1 << 20)
                        need(bool(piece), self.label + ":rows marker")
                        buffer += piece
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


@dataclass(frozen=True, slots=True)
class Atom:
    atom_id: str
    member_id: str
    source: str
    chart: str
    box: tuple[Fraction, ...]
    sign: int | None


def qbox(values: list[str]) -> tuple[Fraction, ...]:
    box = tuple(Fraction(value) for value in values)
    need(len(box) == 6 and all(box[2*i] < box[2*i+1] for i in range(3)), "box")
    return box


def qtext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def box_text(box: tuple[Fraction, ...]) -> list[str]:
    return [qtext(value) for value in box]


def unordered(left: str, right: str) -> tuple[str, str]:
    need(left != right, "nonself")
    return (left, right) if left < right else (right, left)


def physical_overlap(left: Atom, right: Atom) -> tuple[Fraction, ...] | None:
    result: list[Fraction] = []
    for axis in range(3):
        lower = max(left.box[2*axis], right.box[2*axis])
        upper = min(left.box[2*axis+1], right.box[2*axis+1])
        if lower >= upper:
            return None
        result.extend((lower, upper))
    return tuple(result)


def transformed_overlap(cell: Atom, carrier: Atom) -> tuple[Fraction, ...] | None:
    need(cell.sign in {-1, 1}, "T2 sign")
    p0, p1 = max(cell.box[2], carrier.box[2]), min(cell.box[3], carrier.box[3])
    s0, s1 = max(cell.box[4], carrier.box[4]), min(cell.box[5], carrier.box[5])
    if p0 >= p1 or s0 >= s1:
        return None
    if cell.sign == 1:
        if carrier.box[1] <= 0:
            return None
        lower, upper = max(carrier.box[0], Fraction(0)) ** 2, carrier.box[1] ** 2
    else:
        if carrier.box[0] >= 0:
            return None
        lower, upper = min(carrier.box[1], Fraction(0)) ** 2, carrier.box[0] ** 2
    t0, t1 = max(cell.box[0], lower), min(cell.box[1], upper)
    if t0 >= t1:
        return None
    return (t0, t1, p0, p1, s0, s1)


def sweep(left: list[Atom], right: list[Atom], left_axis: int, right_axis: int) -> Iterator[tuple[Atom, Atom]]:
    events: list[tuple[Fraction, int, int, int]] = []
    for index, atom in enumerate(left):
        events.append((atom.box[2*left_axis], 1, 0, index))
        events.append((atom.box[2*left_axis+1], 0, 0, index))
    for index, atom in enumerate(right):
        events.append((atom.box[2*right_axis], 1, 1, index))
        events.append((atom.box[2*right_axis+1], 0, 1, index))
    events.sort()
    active_left: set[int] = set()
    active_right: set[int] = set()
    for _, start, side, index in events:
        if start == 0:
            (active_left if side == 0 else active_right).discard(index)
        elif side == 0:
            for other in active_right:
                yield left[index], right[other]
            active_left.add(index)
        else:
            for other in active_left:
                yield left[other], right[index]
            active_right.add(index)


def verify(args: argparse.Namespace) -> dict[str, Any]:
    specs = dict(FILES)
    for prefix in ("seed1", "seed2"):
        for kind in ("result", "priority", "positive"):
            specs[prefix + "_" + kind] = (
                getattr(args, prefix + "_" + kind),
                getattr(args, prefix + "_" + kind + "_sha256"),
            )
    captures: dict[str, Capture] = {}
    try:
        for label, (path, expected) in specs.items():
            captures[label] = Capture.open(label, ROOT / path, expected)

        results: list[dict[str, Any]] = []
        for prefix, seed in (("seed1", 30637101), ("seed2", 30637991)):
            raw = captures[prefix + "_result"].raw()
            result = json.loads(raw)
            body = dict(result)
            claimed = body.pop("result_sha256")
            need(claimed == digest(body) and result["invocation_seed"] == seed
                 and result["root_input_capture"]["all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat"] is True,
                 prefix + ":result authority")
            results.append(result)
        raw_differences = difference_paths(results[0], results[1])
        need(raw_differences == set(RUN_LOCAL_DIFFERENCE_WHITELIST),
             "dual seed exact run-local difference whitelist")
        normalized = [normalized_result(result) for result in results]
        need(normalized[0] == normalized[1]
             and results[0]["priority_ledger"]["file_sha256"]
                == results[1]["priority_ledger"]["file_sha256"],
             "dual seed independently normalized equality")
        normalized_projection_sha256 = digest(normalized[0])

        component: dict[str, str] = {}
        for row in captures["C15"].jsonl():
            component[row["registry_member_id"]] = row["fresh_component_id"]
        kernel: dict[str, str] = {}
        for row in captures["C25"].jsonl():
            kernel[row["member_id"]] = row["source_bindings"]["support_kernel"]
        need(len(component) == len(kernel) == 502_204, "member authority")

        carriers: dict[str, list[Atom]] = {}
        carrier_count = 0
        for row in captures["crosswalk"].jsonl():
            atom = Atom(row["current_C19_source"] + ":" + row["current_C19_support_row_sha256"],
                        row["member_id"], row["current_C19_source"], row["source_chart"],
                        qbox(row["support_bounds_t_p_s"]), None)
            carriers.setdefault(atom.chart, []).append(atom)
            carrier_count += 1
        physical_targets: dict[str, list[Atom]] = {}
        for row in captures["C22A"].jsonl():
            support = row["support_ast"]
            atom = Atom("C22A:" + row["row_sha256"], row["owner_member_id"], "C22A",
                        support["coordinate_chart"], qbox(support["bounds"]), None)
            physical_targets.setdefault(atom.chart, []).append(atom)
        t2_targets: dict[str, list[Atom]] = {}
        for row in captures["C23A"].jsonl():
            support = row["support_ast"]
            atom = Atom("C23A:" + row["row_sha256"], row["owner_member_id"], "C23A",
                        support["recharted_target_chart"], qbox(support["bounds"]),
                        support["physical_t_sign"])
            t2_targets.setdefault(atom.chart, []).append(atom)
        need(carrier_count == 51_172
             and sum(map(len, physical_targets.values())) == 295_340
             and sum(map(len, t2_targets.values())) == 10_252, "atom census")

        expected: dict[tuple[str, str], dict[tuple[str, str], tuple[str, list[str]]]] = {}
        comparison = {"PHYSICAL_PHYSICAL": 0, "T2_PHYSICAL": 0}

        def record(carrier: Atom, target: Atom, system: str, overlap: tuple[Fraction, ...]) -> None:
            if carrier.member_id == target.member_id:
                return
            pair = unordered(carrier.member_id, target.member_id)
            atoms = ((carrier.atom_id, target.atom_id) if carrier.member_id < target.member_id
                     else (target.atom_id, carrier.atom_id))
            witness = expected.setdefault(pair, {})
            need(atoms not in witness, "duplicate atom witness")
            witness[atoms] = (system, box_text(overlap))

        for chart in sorted(carriers):
            left = carriers[chart]
            for carrier, target in sweep(left, physical_targets.get(chart, []), 0, 0):
                comparison["PHYSICAL_PHYSICAL"] += 1
                overlap = physical_overlap(carrier, target)
                if overlap is not None:
                    record(carrier, target, "(t,p,s)", overlap)
            for carrier, target in sweep(left, t2_targets.get(chart, []), 1, 1):
                comparison["T2_PHYSICAL"] += 1
                overlap = transformed_overlap(target, carrier)
                if overlap is not None:
                    record(carrier, target, "(t_squared,p,s)", overlap)
        need(len(expected) == 55_532, "independent positive pair census")

        positive_rows: list[dict[tuple[str, str], dict[str, Any]]] = []
        for prefix in ("seed1", "seed2"):
            rows: dict[tuple[str, str], dict[str, Any]] = {}
            for row in captures[prefix + "_positive"].jsonl():
                pair = unordered(row["left_member_id"], row["right_member_id"])
                need(pair not in rows and pair in expected, prefix + ":positive pair")
                witnesses = expected[pair]
                atoms = tuple(row["representative_atom_ids"])
                need(atoms in witnesses and row["atom_overlap_witness_count"] == len(witnesses)
                     and (row["intersection_coordinate_system"], row["exact_positive_intersection_box"])
                        == witnesses[atoms]
                     and row["current_C15_components"] == [component[pair[0]], component[pair[1]]]
                     and row["current_C25_support_kernels"] == [kernel[pair[0]], kernel[pair[1]]]
                     and row["same_current_C15_component"]
                        == (component[pair[0]] == component[pair[1]])
                     and row["positive_volume_physical_overlap"] is True,
                     prefix + ":positive row semantics")
                rows[pair] = row
            need(set(rows) == set(expected), prefix + ":positive exact totality")
            positive_rows.append(rows)

        signed: set[tuple[str, str]] = set()
        signed_self = signed_count = 0
        for row in captures["SIGNED"].document_rows():
            signed_count += 1
            if row["decision"].startswith("ACCEPT_"):
                left, right = row["left_formal_occurrence_id"], row["right_formal_occurrence_id"]
                if left == right:
                    signed_self += 1
                else:
                    signed.add(unordered(left, right))
        complete: set[tuple[str, str]] = set()
        complete_count = complete_self = complete_raw = 0
        for row in captures["COMPLETE"].document_rows():
            complete_count += 1
            if row["decision"].startswith("ACCEPT_"):
                for left in row["left_formal_occurrence_endpoints"]:
                    for right in row["right_formal_occurrence_endpoints"]:
                        if left == right:
                            complete_self += 1
                        else:
                            complete_raw += 1
                            complete.add(unordered(left, right))
        need(signed_count == 43_092 and signed_self == 2_092 and len(signed) == 25_452
             and complete_count == 62_548 and complete_self == 15_056
             and complete_raw == 91_760 and len(complete) == 36_140
             and signed <= complete and not (set(expected) & complete), "face pair sets")
        universe = complete | set(expected)
        need(len(universe) == 91_672, "independent 91,672 union")

        for prefix, positives in zip(("seed1", "seed2"), positive_rows):
            routes: set[tuple[str, str]] = set()
            census: dict[str, int] = {}
            for row in captures[prefix + "_priority"].jsonl():
                pair = unordered(row["left_member_id"], row["right_member_id"])
                need(pair not in routes and pair in universe, prefix + ":route pair")
                terminal = ("SIGNED_BOUNDARY_FACES" if pair in signed else
                            "COMPLETE_BOUNDARY_FACES" if pair in complete else
                            "POSITIVE_VOLUME_CARRIERS")
                need(row["assigned_terminal"] == terminal
                     and row["raw_signed_face_evidence"] == (pair in signed)
                     and row["raw_complete_face_evidence"] == (pair in complete)
                     and row["raw_positive_C19_physical_support_evidence"] == (pair in expected)
                     and row["positive_primitive_row_sha256"]
                        == (positives[pair]["row_sha256"] if pair in positives else None)
                     and row["current_C15_components"] == [component[pair[0]], component[pair[1]]]
                     and row["current_C25_support_kernels"] == [kernel[pair[0]], kernel[pair[1]]],
                     prefix + ":route semantics")
                census[terminal] = census.get(terminal, 0) + 1
                routes.add(pair)
            need(routes == universe and census == {
                "SIGNED_BOUNDARY_FACES": 25_452,
                "COMPLETE_BOUNDARY_FACES": 10_688,
                "POSITIVE_VOLUME_CARRIERS": 55_532,
            }, prefix + ":route exact totality")

        body = {
            "schema": "cm2.c27-independent.current-support-91672-sweep-verification.v1",
            "status": "PASS_INDEPENDENT_SWEEP_55532_AND_PRIORITY_91672_DUAL_SEED__ZERO_CREDIT",
            "independent_algorithm": "OPEN_INTERVAL_EVENT_SWEEP_THEN_EXACT_RATIONAL_3D_OR_T_SQUARED_INTERSECTION",
            "candidate_comparison_census": comparison,
            "positive_pair_count": len(expected),
            "SIGNED_pair_count": len(signed),
            "COMPLETE_pair_count": len(complete),
            "total_priority_pair_count": len(universe),
            "dual_seed_primary_ledger_bytes_identical": True,
            "independent_normalized_projection_sha256": normalized_projection_sha256,
            "run_local_difference_whitelist": list(RUN_LOCAL_DIFFERENCE_WHITELIST),
            "observed_run_local_difference_paths": sorted(raw_differences),
            "producer_semantic_projection_field": "SUPERSEDED_FOR_CROSS_SEED_COMPARISON__CLOSED_INSIDE_EACH_RESULT_BUT_INCLUDED_RUN_LOCAL_FIELDS",
            "root_input_capture": {"all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                                   "attestations": {label: cap.receipt()
                                                    for label, cap in sorted(captures.items())}},
            "R300C_used_as_candidate_universe": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        result = dict(body)
        result["result_sha256"] = digest(result)
        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=False)
        (out / "verification.json").write_bytes(canonical(result) + b"\n")
        return result
    finally:
        for capture in captures.values():
            capture.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    for prefix in ("seed1", "seed2"):
        for kind in ("result", "priority", "positive"):
            parser.add_argument("--" + prefix + "-" + kind, required=True)
            parser.add_argument("--" + prefix + "-" + kind + "-sha256", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        result = verify(args)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
