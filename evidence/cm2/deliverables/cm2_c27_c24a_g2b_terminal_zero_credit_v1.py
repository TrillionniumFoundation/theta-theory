#!/usr/bin/env python3
"""Terminal diagnostic receipt for the C24A G2B route (zero formal credit)."""

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

AUTHORITIES = {
    "primary_producer": ("deliverables/cm2_c27_c24a_g2b_exact_factor_sign_disposition_v1_probe.py", "7ec20f13eecf83a3598f6298421658a197ddc2170215be91b3e8a2a8324550c1"),
    "comparator": ("deliverables/cm2_c27_c24a_g2b_dual_implementation_comparator_v1.py", "4eff31f89e85d7849e0d8e609950efb2dc234ac80168a511e90f8bddee992043"),
    "attacks": ("deliverables/cm2_c27_c24a_g2b_dual_implementation_comparator_attack_v1.py", "8d51356b50d4f466fdcddc38c9a42512996fab1ee3737bd7ab464a414284291f"),
    "priority_v2": ("deliverables/cm2_c27_c24a_priority_rank_closure_v2_producer.py", "89531c062acec52191b7036daeb8e9371e32073697ee7f4d57ce4666e984633d"),
    "primary_seed1_result": (".cm2-runtime/audit/c27-c24a-g2b-exact-factor-sign-disposition-v1-seed-30634101-clean-replay/payload/result.json", "4d8a556125f11a40b0c61ab289f747c1ec85ef38076e109e8d62dc0dc5da8918"),
    "primary_seed2_result": (".cm2-runtime/audit/c27-c24a-g2b-exact-factor-sign-disposition-v1-seed-30634991-attempt1/payload/result.json", "576ab450a2b71398d4a8280f64dfebec6ee4d87910858d18b06e366f26e9a3b6"),
    "primary_seed1_ledger": (".cm2-runtime/audit/c27-c24a-g2b-exact-factor-sign-disposition-v1-seed-30634101-clean-replay/payload/C24A_G2B_18800_exact_factor_sign_disposition.jsonl.gz", "c3dbfb3363af18dc79b27aeb4245266102914de5a8c2cab980c019337776d899"),
    "primary_seed2_ledger": (".cm2-runtime/audit/c27-c24a-g2b-exact-factor-sign-disposition-v1-seed-30634991-attempt1/payload/C24A_G2B_18800_exact_factor_sign_disposition.jsonl.gz", "c3dbfb3363af18dc79b27aeb4245266102914de5a8c2cab980c019337776d899"),
    "secondary_result": (".cm2-runtime/audit/c24a-c22a-exact-factor-sign-independent-v2/result.json", "e03ce26b6aab27fd047ad570ffd5313afc8c5f12dcc2eb250091818ea64855d7"),
    "secondary_ledger": (".cm2-runtime/audit/c24a-c22a-exact-factor-sign-independent-v2/C24A_18800_G2B_envelope_exact_factor_sign_disposition.jsonl.gz", "f72c792fdca47ba1e5b92498a43995d16d76b758647a8f444da9af349d3654c7"),
    "priority_seed1_result": (".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635101/payload/result.json", "5ad65f7228d8a2503f7ec6a0155f290f478efea7c70697b54d3d8036bc0752d2"),
    "priority_seed2_result": (".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635991/payload/result.json", "d8305325f6448f9433244c8e677291d949ad391fb7942d21a6db26ada3423e8c"),
    "priority_ledger": (".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635101/payload/C24A_9408_positive_pair_priority_disposition.jsonl.gz", "6a59b0822c8a27eb5f44609cd5edd33038dadf17aa8fe7841d2c7277c8c5ec95"),
    "cross_ledger": (".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635101/payload/C24A_596_cross_positive_member_to_component_edge.jsonl.gz", "0f3924d4a9f0b029d4c82879ec453bb280232c13d870ac28157b5a20dd5585c8"),
    "edge_ledger": (".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635101/payload/C24A_cross_positive_unique_component_edges.jsonl.gz", "d922bbf6d8f487df1e826271b0d65d2d9765432f6d4a02919fe1157b94c117ef"),
    "comparator_result": (".cm2-runtime/audit/c27-c24a-g2b-dual-implementation-comparator-v1-attempt4/payload/result.json", "863bf3deb221d2c9d2691ec4d38004f30bbe9272a1345a5437a1470720479f3c"),
    "attacks_result": (".cm2-runtime/audit/c27-c24a-g2b-dual-comparator-attacks-v1-seed-30636101-attempt1/payload/result.json", "9f437fa7901bd474784aea6aa8d9a5665b7996e9055cfff7df3610b697d48420"),
    "outer_result": (".cm2-runtime/audit/c27-three-terminal-current-full-support-totality-v3-seed-30633101-attempt5-envelope-blocker/payload/result.json", "4c2b3fda6165695153a1c21587de566e4a1efe34f1fbec8bb2ba888250e68440"),
    "G2A_open_ledger": (".cm2-runtime/audit/c27-three-terminal-current-full-support-totality-v3-seed-30633101-attempt5-envelope-blocker/payload/C24A_5264_G2A_relative_2D_open_routes.jsonl.gz", "0d62c8c11c6af1c427d8b373afcd3bfd21e024008e4a4ff391f658e4536e45d1"),
}

RUNS = {
    "primary_seed1": ".cm2-runtime/audit/c27-c24a-g2b-exact-factor-sign-disposition-v1-seed-30634101-clean-replay",
    "primary_seed2": ".cm2-runtime/audit/c27-c24a-g2b-exact-factor-sign-disposition-v1-seed-30634991-attempt1",
    "priority_seed1": ".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635101",
    "priority_seed2": ".cm2-runtime/audit/c27-c24a-priority-rank-closure-v2-seed-30635991",
    "comparator": ".cm2-runtime/audit/c27-c24a-g2b-dual-implementation-comparator-v1-attempt4",
    "attacks": ".cm2-runtime/audit/c27-c24a-g2b-dual-comparator-attacks-v1-seed-30636101-attempt1",
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


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


@dataclass
class Capture:
    label: str
    relative: str
    fd: int
    pre: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, relative: str, expected: str | None = None) -> "Capture":
        path = ROOT / relative
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
                need(observed == expected, label + ":sha256")
            need(fingerprint(os.fstat(fd)) == fingerprint(before), label + ":hash fstat")
            os.lseek(fd, 0, os.SEEK_SET)
            return cls(label, relative, fd, fingerprint(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        pieces: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            pieces.append(block)
        need(fingerprint(os.fstat(self.fd)) == self.pre, self.label + ":parse fstat")
        return b"".join(pieces)

    def document(self) -> dict[str, Any]:
        row = json.loads(self.raw())
        need(type(row) is dict, self.label + ":document")
        body = dict(row)
        claimed = body.pop("result_sha256", None)
        need(type(claimed) is str and claimed == digest(body), self.label + ":closure")
        return row

    def receipt(self) -> dict[str, Any]:
        need(fingerprint(os.fstat(self.fd)) == self.pre, self.label + ":final fstat")
        return {"path": self.relative, "sha256": self.sha256,
                "size": self.pre[2], "stat_fingerprint": list(self.pre),
                "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def build(out: Path) -> tuple[dict[str, Any], str]:
    need(not out.exists(), "fresh output directory")
    captures: dict[str, Capture] = {}
    try:
        for label, (relative, expected) in AUTHORITIES.items():
            captures[label] = Capture.open(label, relative, expected)
        producer_relative = str(Path(__file__).resolve().relative_to(ROOT))
        captures["terminal_producer"] = Capture.open(
            "terminal_producer", producer_relative
        )
        documents = {label: captures[label].document() for label in (
            "primary_seed1_result", "primary_seed2_result", "secondary_result",
            "priority_seed1_result", "priority_seed2_result", "comparator_result",
            "attacks_result", "outer_result")}

        p1, p2 = documents["primary_seed1_result"], documents["primary_seed2_result"]
        need([p1["invocation_seed"], p2["invocation_seed"]] == [30634101, 30634991]
             and p1["semantic_projection_sha256"] == p2["semantic_projection_sha256"]
                == "eac539a5c78280addd07f2acb099d97236c8958a7ee1cc8627e0dbd592b1c114"
             and p1["ledger"]["file_sha256"] == p2["ledger"]["file_sha256"]
                == "c3dbfb3363af18dc79b27aeb4245266102914de5a8c2cab980c019337776d899"
             and p1["disposition_census"] == p2["disposition_census"]
                == {"EXACT_EMPTY_INTERSECTION": 9392, "EXACT_POSITIVE_SUPPORT": 9408}
             and p1["current_C15_component_disposition_census"]["CROSS_C15|EXACT_POSITIVE_SUPPORT"] == 596,
             "primary dual-seed authority")
        s = documents["secondary_result"]
        need(s["status"] == "PASS_EXACT_FACTOR_SIGN_DISPOSITION_ZERO_UNRESOLVED"
             and s["disposition_census"] == {"SUPPORT_EMPTY": 9392, "SUPPORT_POSITIVE": 9408}
             and s["unresolved_reason_census"] == {}, "independent secondary authority")
        q1, q2 = documents["priority_seed1_result"], documents["priority_seed2_result"]
        need([q1["invocation_seed"], q2["invocation_seed"]] == [30635101, 30635991]
             and q1["semantic_projection_sha256"] == q2["semantic_projection_sha256"]
                == "57395377caa6ac87fbe6a4f79971afd0d2260974f74cbde7561e3b1be35abc50"
             and q1["raw_exact_pair_sets"] == q2["raw_exact_pair_sets"]
             and q1["C27R1D_comparison"] == q2["C27R1D_comparison"],
             "priority/rank dual-seed authority")
        comp = documents["comparator_result"]
        need(comp["status"].startswith("PASS_DUAL_IMPLEMENTATION_18800_EXACT")
             and comp["comparison"]["dual_semantic_mismatch_census"] == {}
             and comp["three_terminal_priority_union_count"] == 45548
             and comp["component_rank_diagnostic"]["novel_after_C27R1D"] == 0
             and comp["formal_credit"] == 0 and comp["manifest_authorized"] is False,
             "comparator authority")
        attacks = documents["attacks_result"]
        need(attacks["attack_count"] == attacks["rejected_attack_count"] == 37
             and attacks["accepted_attack_count"] == 0
             and attacks["formal_credit"] == 0, "attack authority")
        outer = documents["outer_result"]
        need(outer["C24A_exact_support_partition"]["G2A_relative_2D_route_status"] == "OPEN"
             and outer["C24A_exact_support_partition"]["family_census"]["G2A"] == 5264
             and outer["C24A_exact_support_partition"]["G2A_open_route_ledger_file_sha256"]
                == "0d62c8c11c6af1c427d8b373afcd3bfd21e024008e4a4ff391f658e4536e45d1",
             "G2A open authority")

        run_receipts: dict[str, Any] = {}
        for run_label, directory in RUNS.items():
            items: dict[str, Any] = {}
            for filename, expected in (("exit_code.txt", b"0\n"),
                                       ("signal.txt", b"null\n"),
                                       ("stderr.log", b"")):
                label = "run_" + run_label + "_" + filename
                captures[label] = Capture.open(label, directory + "/" + filename)
                need(captures[label].raw() == expected, label + ":content")
                items[filename] = captures[label].receipt()
            run_receipts[run_label] = items

        authority_receipts = {label: capture.receipt()
                              for label, capture in sorted(captures.items())
                              if not label.startswith("run_")}
        body = {
            "schema": "cm2.c27-independent.c24a-g2b-terminal-zero-credit.v1",
            "status": "PASS_TERMINAL_DIAGNOSTIC_C24A_G2B_EXACT_ROUTE__ZERO_FORMAL_CREDIT",
            "G2B_closed_diagnostic": {
                "candidate_pairs": 18800, "exact_positive": 9408,
                "exact_empty": 9392, "unresolved": 0,
                "cross_current_C15_positive_member_pairs": 596,
                "unique_old_C15_component_edges": 144,
                "edges_already_in_C27R1D": 144,
                "new_component_edges_after_C27R1D": 0,
                "incremental_rank_reduction_after_C27R1D": 0,
            },
            "three_terminal_priority": {
                "SIGNED": 25452, "COMPLETE_only": 10688,
                "C24A_G2B_positive": 9408, "union": 45548,
                "C24A_intersection_SIGNED": 0,
                "C24A_intersection_COMPLETE": 0,
            },
            "dual_implementation_exact_mismatch_count": 0,
            "coherent_attacks": {"rejected": 37, "accepted": 0},
            "open_blockers": [
                "C24A_G2A_5264_RELATIVE_2D_COMPLETE_OR_UNIQUE_DIMENSIONAL_ROUTE_OPEN",
                "THREE_TERMINAL_GLOBAL_CANDIDATE_TOTALITY_AND_UNIQUE_ASSIGNMENT_OPEN",
                "C27_C28_C29_FULL_REBUILD_MUST_UNION_ALL_EXISTING_STRICT_VOLUME_AND_C19_WITNESSES_WITH_C24A_BRANCH",
                "NO_PATCH_PROMOTION_AND_NO_PHYSICAL_MAXIMALITY_CLAIM",
            ],
            "formal_state_unchanged": {
                "latest_formal_seal": "Round306C30b",
                "Source_W_remaining": 80,
                "C27_transition_totality": 0,
                "C28_pair_routing": 0,
                "C29_physical_maximality": 0,
                "formal_credit": 0,
                "manifest_authorized": False,
                "CM2": "NO-GO_FOR_CLAIM",
            },
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "authorities": authority_receipts,
                "clean_run_receipts": run_receipts,
            },
        }
        receipt = dict(body)
        receipt["result_sha256"] = digest(receipt)
        out.mkdir(parents=True)
        receipt_path = out / "terminal_zero_credit_receipt.json"
        receipt_path.write_bytes(canonical(receipt) + b"\n")
        receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        manifest_entries = [(item["sha256"], item["path"])
                            for item in authority_receipts.values()]
        for run in run_receipts.values():
            for item in run.values():
                manifest_entries.append((item["sha256"], item["path"]))
        receipt_relative = str(receipt_path.resolve().relative_to(ROOT))
        manifest_entries.append((receipt_sha, receipt_relative))
        manifest = b"".join(f"{sha}  {path}\n".encode("ascii")
                            for sha, path in sorted(manifest_entries, key=lambda item: item[1]))
        manifest_path = out / "manifest.sha256"
        manifest_path.write_bytes(manifest)
        manifest_sha = hashlib.sha256(manifest).hexdigest()
        return receipt, manifest_sha
    finally:
        for capture in captures.values():
            capture.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        receipt, manifest_sha = build(Path(args.out_dir))
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": receipt["status"], "result_sha256": receipt["result_sha256"],
                     "manifest_file_sha256": manifest_sha}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
