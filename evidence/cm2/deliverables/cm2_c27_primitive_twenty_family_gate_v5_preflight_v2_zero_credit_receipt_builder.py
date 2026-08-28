#!/usr/bin/env python3
"""Seal the immutable truthful-reject primitive v5 preflight v2 chain."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


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


def disk_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        need(type(expected) is str and len(expected) == 64, label + ":expected sha")
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

    def stable(self, phase: str) -> None:
        need(fp(os.fstat(self.fd)) == self.initial,
             self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        self.stable("raw")
        return b"".join(pieces)

    def document(self, closure_key: str,
                 canonical_file: bool = True) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        need(type(value) is dict, self.label + ":document")
        if canonical_file:
            need(canonical(value) + b"\n" == raw, self.label + ":canonical")
        body = dict(value)
        claim = body.pop(closure_key, None)
        need(type(claim) is str and claim == digest(body), self.label + ":closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    need(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    need(type(row) is dict and canonical(row) == payload,
                         f"{self.label}:{ordinal}:canonical")
                    body = dict(row)
                    claim = body.pop("row_sha256", None)
                    need(type(claim) is str and claim == digest(body),
                         f"{self.label}:{ordinal}:closure")
                    yield row
        self.stable("rows")

    def rendered_path(self) -> str:
        try:
            return str(self.path.relative_to(ROOT))
        except ValueError:
            return str(self.path)

    def attestation(self) -> dict[str, Any]:
        self.stable("attestation")
        return {"path": self.rendered_path(), "sha256": self.sha256,
                "size": self.initial[2], "stat_fingerprint": list(self.initial),
                "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def resolve(path: str) -> Path:
    value = Path(path)
    return value.resolve() if value.is_absolute() else (ROOT / value).resolve()


def add(captures: dict[str, Capture], label: str, path: Path, sha: str) -> None:
    need(label not in captures, label + ":unique label")
    view = Capture.open(label, path, sha)
    need(all(view.path != existing.path for existing in captures.values()),
         label + ":unique path")
    captures[label] = view


def build(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_dir)
    need(not output.exists(), "fresh receipt directory")
    need(args.producer_observed_exit_code == 2, "observed preflight exit code 2")
    captures: dict[str, Capture] = {}
    try:
        own = Path(__file__).resolve()
        add(captures, "receipt_builder_source", own, disk_sha(own))
        for label in (
            "terminal_replay_source", "preflight_source",
            "independent_verifier_source", "attack_harness_source",
            "preflight_result", "gap_ledger", "independent_verification",
            "coherent_attacks",
        ):
            add(captures, label, Path(getattr(args, label)),
                getattr(args, label + "_sha256"))

        preflight = captures["preflight_result"].document("result_sha256")
        verification = captures["independent_verification"].document(
            "verification_sha256")
        attacks = captures["coherent_attacks"].document("attack_result_sha256")
        expected_authorities = {
            "correction_v2", "strict_volume_receipt", "lower_contact_receipt",
            "c19c_receipt", "g2a_final_receipt", "g2a_payload_manifest",
            "g2a_root_manifest", "g2a_terminal_replay", "g2a_invalidation_notice",
            "g2b_receipt", "pair_union_receipt", "pair_union_manifest",
            "pair_ownership",
        }
        source_attestations = preflight["root_input_capture"]["attestations"]
        need(set(source_attestations) == expected_authorities,
             "exact preflight authority set")
        for label in sorted(expected_authorities):
            item = source_attestations[label]
            add(captures, label, resolve(item["path"]), item["sha256"])
        need(len(captures) == 22, "22 payload captures")

        expected_blockers = {
            "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT",
            "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT",
        }
        need(preflight["schema"]
                == "cm2.c27-independent.primitive-twenty-family-gate-v5-fail-closed-preflight.v2"
             and preflight["status"]
                == "REJECT_MISSING_FULL_ATOM_AND_OR_C26_FORMAL_RECEIPT__ZERO_CREDIT"
             and preflight["decision"] == "REJECT"
             and preflight["intended_process_exit_code"] == 2
             and set(preflight["blocking_authority_slots"]) == expected_blockers
             and preflight["authority_slot_census"]
                == {"total": 9, "present": 7, "missing_or_blocking": 2}
             and preflight["formal_credit"] == 0
             and preflight["manifest_authorized"] is False
             and preflight["global_gate"]["primitive_twenty_family_totality_proved"]
                is False
             and preflight["global_gate"]["decision"] == "FAIL_CLOSED_REJECT",
             "truthful preflight reject")
        need(preflight["authority_hardening"]["G2A_final_v2_receipt_bound"] is True
             and preflight["authority_hardening"]
                ["G2A_payload_and_root_manifests_bound"] is True
             and preflight["authority_hardening"]["G2A_terminal_replay_bound"]
                is True
             and preflight["authority_hardening"]
                ["G2A_old_invalidated_seal_rejected"] is True
             and preflight["authority_hardening"]
                ["pair_union_terminal_receipt_bound"] is True
             and preflight["authority_hardening"]
                ["pair_union_no_import_verification_bound"] is True
             and preflight["authority_hardening"]
                ["pair_union_18_of_18_attacks_bound"] is True
             and preflight["authority_hardening"]
                ["full_atom_seed_result_alone_is_authority"] is False,
             "strong authority bindings")
        need(preflight["corrected_contract"]["atom_multi_pair_allowed"] is True
             and preflight["corrected_contract"]["atom_multi_terminal_allowed"]
                is True
             and preflight["corrected_contract"]
                ["atom_single_pair_or_terminal_constraint_imposed"] is False
             and preflight["forbidden_input_governance"]
                ["legacy_coarse_current_atom_contract_accepted"] is False,
             "corrected atom contract")

        sequence = hashlib.sha256()
        blockers: set[str] = set()
        gap_count = 0
        for row in captures["gap_ledger"].rows():
            gap_count += 1
            sequence.update(bytes.fromhex(row["row_sha256"]))
            if row["gate_blocking"]:
                need(row["authority_status"] == "MISSING_FORMAL_AUTHORITY",
                     "blocking gap status")
                blockers.add(row["authority_slot"])
        need(gap_count == 9 and blockers == expected_blockers
             and preflight["gap_ledger"]["file_sha256"]
                == captures["gap_ledger"].sha256
             and preflight["gap_ledger"]["row_sequence_sha256"]
                == sequence.hexdigest(), "gap replay")
        need(verification["status"]
                == "PASS_INDEPENDENT_AUTHORITY_BOUND_TRUTHFUL_REJECT__ZERO_CREDIT"
             and verification["decision"] == "VERIFY_REJECT"
             and verification["formal_credit"] == 0
             and verification["manifest_authorized"] is False
             and verification["implementation_independence"]
                ["preflight_or_workspace_module_imported"] is False
             and verification["implementation_independence"]
                ["verifier_source_sha256"]
                == captures["independent_verifier_source"].sha256,
             "independent verification")
        verifier_inputs = verification["root_input_capture"]["attestations"]
        need(set(verifier_inputs) == expected_authorities | {
                 "preflight_result", "gap_ledger"}
             and verifier_inputs["preflight_result"]["sha256"]
                == captures["preflight_result"].sha256
             and verifier_inputs["gap_ledger"]["sha256"]
                == captures["gap_ledger"].sha256,
             "verification input binding")
        need(attacks["status"]
                == "PASS_CONTROL_AND_18_OF_18_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT"
             and attacks["attack_count"] == 18
             and attacks["rejected_attack_count"] == 18
             and attacks["accepted_attack_count"] == 0
             and attacks["control"]["verifier_exit_code"] == 0
             and attacks["control"]["verification_output_created"] is True
             and attacks["formal_credit"] == 0
             and attacks["manifest_authorized"] is False
             and attacks["pins"] == {
                "baseline_gap_file_sha256": captures["gap_ledger"].sha256,
                "baseline_result_file_sha256": captures["preflight_result"].sha256,
                "verifier_source_sha256": captures["independent_verifier_source"].sha256,
             }, "18 coherent attacks")
        need(captures["preflight_source"].sha256
                == args.preflight_source_sha256
             and captures["attack_harness_source"].sha256
                == args.attack_harness_source_sha256
             and captures["terminal_replay_source"].sha256
                == args.terminal_replay_source_sha256,
             "source pins")

        output.mkdir(parents=True, exist_ok=False)
        payload_lines = [f"{capture.sha256}  {capture.rendered_path()}\n"
                         for capture in sorted(captures.values(),
                                               key=lambda item: item.rendered_path())]
        payload_path = output / "payload_manifest.sha256"
        payload_path.write_text("".join(payload_lines), encoding="ascii")
        payload_sha = disk_sha(payload_path)
        def sealed(label: str, object_key: str | None = None) -> dict[str, Any]:
            item = {"path": captures[label].rendered_path(),
                    "file_sha256": captures[label].sha256}
            if object_key is not None:
                document = {"result_sha256": preflight,
                            "verification_sha256": verification,
                            "attack_result_sha256": attacks}[object_key]
                item["object_sha256"] = document[object_key]
            return item

        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-v2-zero-credit-receipt.v1",
            "status": "PASS_SEALED_TRUTHFUL_REJECT_PREFLIGHT_VERIFIER_AND_18_ATTACKS__ZERO_CREDIT",
            "preflight_execution": {
                "decision": "REJECT", "intended_exit_code": 2,
                "observed_exit_code": args.producer_observed_exit_code,
                "observed_matches_intended": True, "truthful_reject": True,
            },
            "sealed_artifacts": {
                "preflight_result": sealed("preflight_result", "result_sha256"),
                "gap_ledger": sealed("gap_ledger"),
                "independent_verification": sealed(
                    "independent_verification", "verification_sha256"),
                "coherent_attacks": sealed("coherent_attacks", "attack_result_sha256"),
            },
            "authority_chain": {
                "G2A_final_v2_receipt_payload_root_manifests_and_replay_bound": True,
                "old_invalidated_G2A_seal_rejected": True,
                "pair_union_terminal_receipt_manifest_no_import_and_18_attacks_bound": True,
                "pair_ownership_rows_reconstructed": 101_080,
                "full_atom_seed_result_not_accepted_as_formal": True,
                "legacy_coarse_atom_contract_rejected": True,
                "C26_lower_receipt_not_promoted_to_absence_theorem": True,
            },
            "blocking_authority_slots": sorted(expected_blockers),
            "global_gate": {
                "decision": "FAIL_CLOSED_REJECT",
                "primitive_twenty_family_totality_proved": False,
                "full_atom_formal_receipt_present": False,
                "C26_formal_receipt_present": False,
                "future_closure_requires_fresh_actual_gate_run": True,
                "sealed_preflight_may_not_be_rewritten": True,
            },
            "independent_verification": {
                "verification_sha256": verification["verification_sha256"],
                "no_preflight_or_workspace_import": True,
            },
            "coherent_attacks": {"control_passed": True, "attack_count": 18,
                                 "rejected": 18, "accepted": 0},
            "payload_manifest": {"filename": payload_path.name,
                                 "entry_count": len(captures),
                                 "file_sha256": payload_sha},
            "formal_credit": 0,
            "manifest_authorized": False,
            "strict_nonpromotion": preflight["strict_nonpromotion"],
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(captures.items())},
            },
        }
        receipt = dict(body)
        receipt["result_sha256"] = digest(receipt)
        receipt_path = output / "receipt.json"
        receipt_path.write_bytes(canonical(receipt) + b"\n")
        root_path = output / "root_manifest.sha256"
        root_path.write_text(
            f"{payload_sha}  payload_manifest.sha256\n"
            f"{disk_sha(receipt_path)}  receipt.json\n", encoding="ascii")
        return receipt
    finally:
        for capture in captures.values():
            capture.close()


def add_input(parser: argparse.ArgumentParser, name: str) -> None:
    parser.add_argument("--" + name, required=True)
    parser.add_argument("--" + name + "-sha256", required=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    for name in (
        "terminal-replay-source", "preflight-source",
        "independent-verifier-source", "attack-harness-source",
        "preflight-result", "gap-ledger", "independent-verification",
        "coherent-attacks",
    ):
        add_input(parser, name)
    parser.add_argument("--producer-observed-exit-code", type=int, required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        receipt = build(args)
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(canonical({"status": receipt["status"],
                     "result_sha256": receipt["result_sha256"],
                     "blocking_authority_slots":
                         receipt["blocking_authority_slots"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
