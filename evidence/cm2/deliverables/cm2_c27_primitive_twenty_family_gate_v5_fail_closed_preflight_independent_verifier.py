#!/usr/bin/env python3
"""No-import independent verifier for the v5 fail-closed preflight."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent


class Reject(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def verify_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    claim = body.pop("row_sha256", None)
    require(type(claim) is str and claim == object_hash(body), label + ":row closure")


def fp(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
        value.st_mode,
        value.st_uid,
        value.st_gid,
    )


@dataclass
class View:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "View":
        require(type(expected) is str and len(expected) == 64, label + ":expected sha")
        resolved = path.resolve()
        fd = os.open(
            resolved,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            before = os.fstat(fd)
            require(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            require(observed == expected, label + ":sha256")
            require(fp(os.fstat(fd)) == fp(before), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, resolved, fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        require(fp(os.fstat(self.fd)) == self.initial,
                self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.stable("raw")
        return b"".join(pieces)

    def document(self, canonical_file: bool = False) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        require(type(value) is dict, self.label + ":document")
        if canonical_file:
            require(encode(value) + b"\n" == raw, self.label + ":canonical")
        keys = [key for key in (
            "result_sha256", "receipt_sha256", "design_sha256", "verification_sha256"
        ) if key in value]
        require(len(keys) == 1, self.label + ":closure key")
        body = dict(value)
        claim = body.pop(keys[0])
        require(type(claim) is str and claim == object_hash(body),
                self.label + ":document closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    require(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    require(type(row) is dict and encode(row) == payload,
                            f"{self.label}:{ordinal}:canonical")
                    verify_row(row, f"{self.label}:{ordinal}")
                    yield row
        self.stable("rows")

    def attestation(self) -> dict[str, Any]:
        self.stable("attestation")
        try:
            rendered = str(self.path.relative_to(ROOT))
        except ValueError:
            rendered = str(self.path)
        return {
            "path": rendered,
            "sha256": self.sha256,
            "size": self.initial[2],
            "stat_fingerprint": list(self.initial),
            "O_NOFOLLOW": True,
            "single_open_file_description_hash_parse_fstat": True,
        }

    def close(self) -> None:
        os.close(self.fd)


def pair(values: Any, label: str) -> tuple[str, str]:
    require(type(values) is list and len(values) == 2
            and all(type(item) is str for item in values)
            and values[0] != values[1], label + ":pair")
    return tuple(sorted(values))


def disk_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def acquire(args: argparse.Namespace) -> dict[str, View]:
    specifications = {
        "correction_v2": (args.correction_v2, args.correction_v2_sha256),
        "strict_volume_receipt": (
            args.strict_volume_receipt, args.strict_volume_receipt_sha256
        ),
        "lower_contact_receipt": (
            args.lower_contact_receipt, args.lower_contact_receipt_sha256
        ),
        "c19c_receipt": (args.c19c_receipt, args.c19c_receipt_sha256),
        "g2a_result": (args.g2a_result, args.g2a_result_sha256),
        "g2b_receipt": (args.g2b_receipt, args.g2b_receipt_sha256),
        "pair_union_result": (args.pair_union_result, args.pair_union_result_sha256),
        "pair_ownership": (args.pair_ownership, args.pair_ownership_sha256),
        "preflight_result": (args.preflight_result, args.preflight_result_sha256),
        "gap_ledger": (args.gap_ledger, args.gap_ledger_sha256),
    }
    return {
        label: View.open(label, Path(path), sha)
        for label, (path, sha) in specifications.items()
    }


def verify(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_file)
    require(not output.exists(), "fresh verifier output")
    views = acquire(args)
    try:
        correction = views["correction_v2"].document(canonical_file=True)
        levels = correction["corrected_uniqueness_levels"]
        require(levels["candidate_pair"]["each_pair_has_exactly_one_assigned_terminal"]
                    is True
                and levels["atom_pair_incidence"]["duplicate_incidence_key_forbidden"]
                    is True
                and levels["atom_pair_incidence"]["one_atom_may_have_multiple_distinct_pair_incidences"]
                    is True
                and levels["atom_pair_incidence"]["one_atom_may_therefore_observe_multiple_distinct_terminals"]
                    is True
                and levels["atom"]["atom_terminal_uniqueness_required"] is False,
                "correction-v2 many-to-many contract")

        strict = views["strict_volume_receipt"].document()
        lower = views["lower_contact_receipt"].document()
        c19c = views["c19c_receipt"].document()
        g2a = views["g2a_result"].document()
        g2b = views["g2b_receipt"].document()
        union = views["pair_union_result"].document(canonical_file=True)
        require(strict["exact_census"]["all_component_strict_intersection_pair_count"]
                    == 187_132
                and strict["formal_credit"] == 0, "strict authority")
        require(lower["lower_dimensional_candidate_pair_count"] == 5_783_708
                and lower["C26_role"]["full_rows_read"] == 691_424
                and lower["C26_role"]["absence_used_as_negative_geometry_theorem"]
                    is False
                and lower["formal_credit"] == 0, "lower/C26 insufficiency")
        require(c19c["authority"]["direct_rule"]
                    == "oriented [lower,upper) on internal faces"
                and c19c["formal_credit"] == 0, "C19C authority")
        require(g2a["ledgers"]["contacts"]["row_count"] == 9_408
                and g2a["global_three_terminal_unique_assignment"] is False,
                "G2A scoped authority")
        require(g2b["G2B_closed_diagnostic"]["exact_positive"] == 9_408
                and g2b["G2B_closed_diagnostic"]["exact_empty"] == 9_392,
                "G2B authority")
        require(union["scoped_candidate_union"]["union_pair_count"] == 101_080
                and union["formal_credit"] == 0, "pair union authority")

        seen: set[tuple[str, str]] = set()
        terminal = Counter()
        source = Counter()
        branch = Counter()
        sequence = hashlib.sha256()
        for ordinal, row in enumerate(views["pair_ownership"].rows()):
            key = pair(row["pair_key"], f"ownership:{ordinal}")
            require(key not in seen, f"ownership:{ordinal}:unique")
            seen.add(key)
            assigned = row["assigned_terminal"]
            require(assigned in {
                "SIGNED_BOUNDARY_FACES",
                "COMPLETE_BOUNDARY_FACES",
                "POSITIVE_VOLUME_CARRIERS",
            } and row["formal_credit"] == 0, f"ownership:{ordinal}:terminal")
            authority = row["source_authority"]
            if authority == "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER":
                require(assigned == "POSITIVE_VOLUME_CARRIERS"
                        and row["G2A_diagnostic_alias_row_sha256"] is not None,
                        f"ownership:{ordinal}:C24A normalization")
            terminal[assigned] += 1
            source[authority] += 1
            if row["positive_support_branch"] is not None:
                branch[row["positive_support_branch"]] += 1
            sequence.update(bytes.fromhex(row["row_sha256"]))
        descriptor = union["ledgers"]["unique_ownership"]
        require(len(seen) == 101_080
                and views["pair_ownership"].sha256 == descriptor["file_sha256"]
                and sequence.hexdigest() == descriptor["row_sequence_sha256"]
                and terminal == {
                    "SIGNED_BOUNDARY_FACES": 25_452,
                    "COMPLETE_BOUNDARY_FACES": 10_688,
                    "POSITIVE_VOLUME_CARRIERS": 64_940,
                }
                and source == {
                    "CURRENT_SUPPORT_V4B_SEED1_PRIORITY_LEDGER": 91_672,
                    "C24A_G2B_TERMINAL_AUTHORIZED_PRIORITY_LEDGER": 9_408,
                }, "pair ownership independent reconstruction")

        preflight = views["preflight_result"].document(canonical_file=True)
        projection = {key: value for key, value in preflight.items()
                      if key not in {"invocation_seed", "root_input_capture",
                                     "semantic_projection_sha256", "result_sha256"}}
        require(preflight["semantic_projection_sha256"] == object_hash(projection),
                "preflight semantic projection")
        for label, view in views.items():
            if label in {"preflight_result", "gap_ledger"}:
                continue
            item = preflight["root_input_capture"]["attestations"][label]
            require(item["sha256"] == view.sha256, label + ":preflight binding")

        gaps: dict[str, dict[str, Any]] = {}
        sequence = hashlib.sha256()
        for ordinal, row in enumerate(views["gap_ledger"].rows()):
            require(row["schema"]
                    == "cm2.c27-independent.primitive-twenty-family-v5-authority-gap.row.v1"
                    and row["formal_credit"] == 0,
                    f"gap:{ordinal}:schema")
            slot = row["authority_slot"]
            require(slot not in gaps, f"gap:{ordinal}:unique")
            gaps[slot] = row
            sequence.update(bytes.fromhex(row["row_sha256"]))
        expected_present = {
            "CORRECTION_V2_MANY_TO_MANY_ATOM_CONTRACT",
            "SAME_CHART_STRICT_VOLUME_187132",
            "SAME_CHART_LOWER_EXACT_CONTACT_5783708",
            "C19C_ENDPOINT_V3_HALF_OPEN",
            "FORMAL_SCOPED_G2A_ROUTE",
            "G2B_TERMINAL_AUTHORITY",
            "SCOPED_PAIR_UNION_101080",
        }
        expected_missing = {
            "FULL_101080_TO_483232_ATOM_INCIDENCE",
            "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_THEOREM",
        }
        require(set(gaps) == expected_present | expected_missing
                and all(gaps[slot]["gate_blocking"] is False
                        for slot in expected_present)
                and all(gaps[slot]["gate_blocking"] is True
                        and gaps[slot]["authority_status"] == "MISSING_FORMAL_AUTHORITY"
                        for slot in expected_missing),
                "exact authority-gap partition")
        require(gaps["CORRECTION_V2_MANY_TO_MANY_ATOM_CONTRACT"]["evidence"]
                    == {"design_sha256": correction["design_sha256"]}
                and gaps["SAME_CHART_STRICT_VOLUME_187132"]["evidence"]
                    == {"primitive_row_count": 187_132}
                and gaps["SCOPED_PAIR_UNION_101080"]["evidence"]
                    == preflight["pair_authority_reconstruction"]
                and gaps["FULL_101080_TO_483232_ATOM_INCIDENCE"]["evidence"] == {
                    "required_pair_authority_rows": 101_080,
                    "required_atom_denominator": 483_232,
                    "required_contract": "EXACT_DUPLICATE_FREE_INCIDENCE_SET_OR_EMPTY_COMPLEMENT",
                    "current_only_complement_420992_is_not_global": True,
                }
                and gaps["C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_THEOREM"]["evidence"] == {
                    "C26_rows_known_in_lower_authority": 691_424,
                    "absence_may_not_be_inferred_from_missing_rows_or_volume": True,
                    "explicit_primitive_exact_contact_theorem_required": True,
                }, "gap evidence bindings")
        gap_descriptor = preflight["gap_ledger"]
        require(views["gap_ledger"].sha256 == gap_descriptor["file_sha256"]
                and gap_descriptor["row_count"] == 9
                and sequence.hexdigest() == gap_descriptor["row_sequence_sha256"],
                "gap descriptor")

        contract = preflight["corrected_contract"]
        require(contract == {
            "each_candidate_pair_exactly_one_terminal": True,
            "atom_pair_incidence_key_unique": True,
            "atom_exact_incidence_set_or_empty_complement": True,
            "atom_multi_pair_allowed": True,
            "atom_multi_terminal_allowed": True,
            "atom_single_pair_or_terminal_constraint_imposed": False,
        }, "preflight corrected contract")
        require(preflight["status"]
                    == "REJECT_MISSING_FULL_ATOM_JOIN_AND_OR_C26_EXACT_ABSENCE__ZERO_CREDIT"
                and preflight["decision"] == "REJECT"
                and preflight["intended_process_exit_code"] == 2
                and set(preflight["blocking_authority_slots"]) == expected_missing
                and preflight["authority_slot_census"]
                    == {"total": 9, "present": 7, "missing_or_blocking": 2}
                and preflight["global_gate"]["primitive_twenty_family_totality_proved"]
                    is False
                and preflight["global_gate"]["decision"] == "FAIL_CLOSED_REJECT"
                and preflight["formal_credit"] == 0
                and preflight["manifest_authorized"] is False,
                "truthful reject result")
        forbidden = preflight["forbidden_input_governance"]
        require(all(value is False for value in forbidden.values()),
                "forbidden inputs absent")

        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-verification.v1",
            "status": "PASS_INDEPENDENT_TRUTHFUL_REJECT_RECONSTRUCTION__ZERO_CREDIT",
            "verification_seed": args.seed,
            "reconstructed": {
                "candidate_pair_count": len(seen),
                "terminal_census": dict(sorted(terminal.items())),
                "source_census": dict(sorted(source.items())),
                "blocking_authority_slots": sorted(expected_missing),
                "present_authority_slots": sorted(expected_present),
                "atom_multi_pair_allowed": True,
                "atom_multi_terminal_allowed": True,
                "atom_single_terminal_uniqueness_imposed": False,
                "expected_preflight_exit_code": 2,
            },
            "implementation_independence": {
                "preflight_or_producer_module_imported": False,
                "workspace_module_imported": False,
                "stdlib_only": True,
                "verifier_source_sha256": disk_hash(Path(__file__).resolve()),
            },
            "decision": "VERIFY_REJECT",
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": preflight["strict_nonpromotion"],
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {
                    label: view.attestation() for label, view in sorted(views.items())
                },
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = object_hash({
            key: value for key, value in body.items()
            if key not in {"verification_seed", "root_input_capture"}
        })
        result["verification_sha256"] = object_hash(result)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(encode(result) + b"\n")
        return result
    finally:
        for view in views.values():
            view.close()


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "correction-v2",
        "strict-volume-receipt",
        "lower-contact-receipt",
        "c19c-receipt",
        "g2a-result",
        "g2b-receipt",
        "pair-union-result",
        "pair-ownership",
        "preflight-result",
        "gap-ledger",
    ):
        add_input(parser, name)
    parser.add_argument("--out-file", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result = verify(args)
    except (Reject, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({
        "status": result["status"],
        "verification_sha256": result["verification_sha256"],
        "semantic_projection_sha256": result["semantic_projection_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
