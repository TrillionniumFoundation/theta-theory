#!/usr/bin/env python3
"""Seal the scoped 101,080 pair-union chain as a zero-credit receipt."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


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
        resolved = path.resolve()
        fd = os.open(resolved, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            need(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            need(observed == expected, label + ":sha256")
            need(fp(os.fstat(fd)) == fp(before), label + ":hash fstat")
            return cls(label, resolved, fd, fp(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        need(fp(os.fstat(self.fd)) == self.pre, self.label + ":raw fstat")
        return b"".join(pieces)

    def document(self, closure_key: str) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        need(type(value) is dict and canonical(value) + b"\n" == raw,
             self.label + ":canonical")
        body = dict(value)
        claim = body.pop(closure_key)
        need(claim == digest(body), self.label + ":closure")
        return value

    def attestation(self) -> dict[str, Any]:
        need(fp(os.fstat(self.fd)) == self.pre, self.label + ":final fstat")
        try:
            rendered = str(self.path.relative_to(ROOT))
        except ValueError:
            rendered = str(self.path)
        return {"path": rendered, "sha256": self.sha256, "size": self.pre[2],
                "stat_fingerprint": list(self.pre), "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def build(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    output = Path(args.out_dir)
    need(not output.exists(), "fresh output directory")
    specs = {
        "comparator_source": (args.comparator_source, args.comparator_source_sha256),
        "verifier_source": (args.verifier_source, args.verifier_source_sha256),
        "attack_source": (args.attack_source, args.attack_source_sha256),
        "comparator_result": (args.comparator_result, args.comparator_result_sha256),
        "key_ledger": (args.key_ledger, args.key_ledger_sha256),
        "ownership_ledger": (args.ownership_ledger, args.ownership_ledger_sha256),
        "edge_ledger": (args.edge_ledger, args.edge_ledger_sha256),
        "verification": (args.verification, args.verification_sha256),
        "attacks": (args.attacks, args.attacks_sha256),
    }
    captures: dict[str, Capture] = {}
    try:
        for label, (path, sha) in specs.items():
            captures[label] = Capture.open(label, Path(path), sha)
        result = captures["comparator_result"].document("result_sha256")
        verification = captures["verification"].document("verification_sha256")
        attacks = captures["attacks"].document("attack_result_sha256")
        need(result["status"].endswith("GLOBAL_TOTALITY_FAIL_CLOSED__ZERO_CREDIT")
             and result["formal_credit"] == 0
             and result["scoped_candidate_union"]["union_pair_count"] == 101_080
             and result["scoped_candidate_union"]["scoped_unique_assignment_closed"] is True,
             "comparator scoped authority")
        ledger_map = {
            "C24A_key_comparison": "key_ledger",
            "unique_ownership": "ownership_ledger",
            "cross_C15_edge_union": "edge_ledger",
        }
        for result_key, capture_key in ledger_map.items():
            descriptor = result["ledgers"][result_key]
            capture = captures[capture_key]
            need(descriptor["file_sha256"] == capture.sha256
                 and descriptor["filename"] == capture.path.name,
                 result_key + ":ledger binding")
        need(verification["status"].startswith(
                 "PASS_NO_PRODUCER_IMPORT_INDEPENDENT_RECONSTRUCTION__")
             and verification["formal_credit"] == 0
             and verification["reconstructed"]["scoped_candidate_union"] == 101_080
             and verification["implementation_independence"]
                 ["comparator_or_producer_module_imported"] is False
             and verification["implementation_independence"]["verifier_source_sha256"]
                 == captures["verifier_source"].sha256,
             "independent verification authority")
        need(attacks["status"]
                 == "PASS_ALL_COHERENT_RESIGNED_ATTACKS_REJECTED__GLOBAL_FAIL_CLOSED__ZERO_CREDIT"
             and attacks["attack_count"] == attacks["rejected_attack_count"] == 18
             and attacks["accepted_attack_count"] == 0
             and attacks["formal_credit"] == 0
             and attacks["pins"]["verifier_source_sha256"]
                 == captures["verifier_source"].sha256
             and attacks["pins"]["baseline_result_file_sha256"]
                 == captures["comparator_result"].sha256,
             "coherent attack authority")
        body = {
            "schema": "cm2.c27-independent.c24a-current-primitive-three-terminal-union-terminal-receipt.v1",
            "status": "PASS_SCOPED_101080_PAIR_UNION_DUAL_SEED_NO_IMPORT_18_ATTACKS__GLOBAL_ATOM_TOTALITY_OPEN__ZERO_CREDIT",
            "authority_scope": {
                "candidate_pair_count": 101_080,
                "each_candidate_pair_exactly_one_terminal": True,
                "terminal_census": result["scoped_candidate_union"]["normalized_terminal_census"],
                "G2A_alias_counted_as_second_pair": False,
                "G2B_positive_terminal": "POSITIVE_VOLUME_CARRIERS",
                "current_seed1_seed2_priority_byte_identical": True,
            },
            "C24A_key_authority": result["C24A_G2A_G2B_key_by_key"],
            "edge_diagnostic": result["cross_C15_edge_overlap_and_rank"],
            "independent_verifier": {
                "verification_file_sha256": captures["verification"].sha256,
                "verification_sha256": verification["verification_sha256"],
                "no_producer_import": True,
            },
            "coherent_attacks": {
                "attack_file_sha256": captures["attacks"].sha256,
                "attack_result_sha256": attacks["attack_result_sha256"],
                "attack_count": 18,
                "rejected": 18,
                "accepted": 0,
            },
            "global_open_blockers": [
                "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_AUTHORITY_REQUIRED",
                "PRIMITIVE_TWENTY_FAMILY_TOTALITY_REQUIRES_SEPARATE_FAIL_CLOSED_GATE",
            ],
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": result["strict_nonpromotion"],
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {
                    label: capture.attestation()
                    for label, capture in sorted(captures.items())
                },
            },
        }
        receipt = dict(body)
        receipt["result_sha256"] = digest(receipt)
        output.mkdir(parents=True, exist_ok=False)
        receipt_path = output / "receipt.json"
        receipt_path.write_bytes(canonical(receipt) + b"\n")
        receipt_file_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        manifest_entries = [
            (capture.sha256, capture.attestation()["path"])
            for capture in captures.values()
        ]
        manifest_entries.append((receipt_file_sha, str(receipt_path.resolve().relative_to(ROOT))))
        manifest = b"".join(
            f"{sha}  {path}\n".encode("ascii")
            for sha, path in sorted(manifest_entries, key=lambda item: item[1])
        )
        manifest_path = output / "manifest.sha256"
        manifest_path.write_bytes(manifest)
        return receipt, hashlib.sha256(manifest).hexdigest()
    finally:
        for capture in captures.values():
            capture.close()


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "comparator-source", "verifier-source", "attack-source",
        "comparator-result", "key-ledger", "ownership-ledger", "edge-ledger",
        "verification", "attacks",
    ):
        add_input(parser, name)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        receipt, manifest_sha = build(args)
    except (Failure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": receipt["status"],
                     "result_sha256": receipt["result_sha256"],
                     "manifest_file_sha256": manifest_sha}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
