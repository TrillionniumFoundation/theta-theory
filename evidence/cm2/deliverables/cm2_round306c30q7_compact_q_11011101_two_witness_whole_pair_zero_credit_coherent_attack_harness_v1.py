#!/usr/bin/env python3
"""Coherent negative attacks for the append-only Q7 two-witness theorem."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from typing import Any, Callable


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
VERIFIER = (
    HERE
    / "cm2_round306c30q7_compact_q_11011101_two_witness_whole_pair_"
      "zero_credit_independent_verifier_v1.py"
)
VERIFIER_SHA256 = "80b4ad775aa931451d4f7096d91ba84633c346193544fbc3acc95007407420a9"
PYTHON = Path(sys.executable).absolute()


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def capture(path: Path) -> bytes:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical candidate")
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular single-link candidate")
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    need((before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
          before.st_size, before.st_mtime_ns, before.st_ctime_ns,
          before.st_uid, before.st_gid) ==
         (after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
          after.st_size, after.st_mtime_ns, after.st_ctime_ns,
          after.st_uid, after.st_gid), "stable candidate")
    return raw


def close(document: dict[str, Any]) -> bytes:
    document["result_sha256"] = digest(document["result"])
    return canonical(document) + b"\n"


def invoke(candidate: Path) -> subprocess.CompletedProcess[bytes]:
    environment = {
        "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "30770073",
    }
    return subprocess.run(
        [str(PYTHON), "-B", "-s", str(VERIFIER), str(candidate)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=HERE.parent, env=environment, timeout=30, check=False,
    )


def set_path(document: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    current: Any = document
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage: attack_harness CANDIDATE")
        need(hashlib.sha256(VERIFIER.read_bytes()).hexdigest() == VERIFIER_SHA256,
             "verifier pin")
        original_raw = capture(Path(argv[1]).absolute())
        original = json.loads(original_raw)
        need(original_raw == canonical(original) + b"\n", "canonical baseline")

        Attack = tuple[str, Callable[[dict[str, Any]], None]]
        attacks: list[Attack] = [
            ("wrong_single_witness_kind", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "witness_language", "kind"
            ), "SINGLE_UNIFORM_WITNESS")),
            ("wrong_single_witness_claim", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "witness_language",
                "single_uniform_witness_claimed"
            ), True)),
            ("collapse_right_to_left_target", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "right_witness", "targets"
            ), {"W:N:03.15.11011101": "W[-1,0]",
                "W:S:H.03.15.11011101": "W[-1,0]"})),
            ("switch_drift_12_over_16", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "switch_seam", "r"
            ), "3/4")),
            ("left_closed_switch_drift", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "left_witness",
                "closed_proof_domain"
            ), ["0", "3/4"])),
            ("right_closed_switch_drift", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "right_witness",
                "closed_proof_domain"
            ), ["7/8", "1"])),
            ("half_open_left_closes_seam", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "left_witness",
                "assigned_half_open_domain"
            ), "[0,13/16]")),
            ("half_open_right_drops_seam", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "right_witness",
                "assigned_half_open_domain"
            ), "(13/16,1]")),
            ("boundary_gap_forge", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "switch_seam",
                "assigned_domains_have_gap"
            ), True)),
            ("boundary_overlap_forge", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "switch_seam",
                "assigned_domains_have_overlap"
            ), True)),
            ("seam_left_not_strict", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "switch_seam",
                "left_closed_proof_strict_at_seam"
            ), False)),
            ("seam_right_not_strict", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "switch_seam",
                "right_closed_proof_strict_at_seam"
            ), False)),
            ("north_target_flipped", lambda d: d["result"]
             ["two_witness_analytic_theorem"]["right_witness"]["targets"]
             .__setitem__("W:N:03.15.11011101", "G[0,0]")),
            ("south_target_flipped", lambda d: d["result"]
             ["two_witness_analytic_theorem"]["right_witness"]["targets"]
             .__setitem__("W:S:H.03.15.11011101", "G[0,1]")),
            ("north_south_reflection_false", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "witness_language",
                "north_south_target_reflection_verified"
            ), False)),
            ("forge_old_f1_negative_sign", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "right_witness",
                "strict_f_at_1_sign"
            ), "NEGATIVE")),
            ("forge_old_f1_condition_satisfied", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "right_witness",
                "old_f_at_1_negative_sufficient_condition_satisfied"
            ), True)),
            ("deny_f1_condition_is_unnecessary", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "right_witness",
                "old_f_at_1_negative_condition_is_not_necessary"
            ), False)),
            ("replace_chord_with_old_condition", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "right_witness", "criterion"
            ), "f_at_1_negative_required")),
            ("finite_12_gap_root_subdivision", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem",
                "finite_old_gap_root_subdivision_count"
            ), 12)),
            ("wrong_global_box_count", lambda d: set_path(d, (
                "result", "two_witness_analytic_theorem", "global_witness_interval_box_count"
            ), 14)),
            ("root_count_31", lambda d: set_path(d, (
                "result", "exact_root_and_old_gap_audit", "pair_root_count"
            ), 31)),
            ("old_gap_11", lambda d: set_path(d, (
                "result", "exact_root_and_old_gap_audit", "old_gap_roots_per_origin"
            ), 11)),
            ("root_digest_drift", lambda d: set_path(d, (
                "result", "exact_root_and_old_gap_audit", "pair_root_keys_sha256"
            ), "0" * 64)),
            ("residual_count_127", lambda d: set_path(d, (
                "result", "whole_pair_research_conclusion",
                "per_origin_compact_q_residual_children_covered_by_global_theorem"
            ), 127)),
            ("formal_credit_2", lambda d: set_path(d, (
                "result", "formal_boundary", "formal_credit"
            ), 2)),
            ("formal_remaining_52", lambda d: set_path(d, (
                "result", "formal_boundary", "compact_q_formal_remaining_origins"
            ), 52)),
            ("authorize_transition", lambda d: set_path(d, (
                "result", "formal_boundary", "diagnostic_transition_authorized"
            ), True)),
            ("forge_terminal_gate", lambda d: set_path(d, (
                "result", "formal_boundary", "terminal_gate_present"
            ), True)),
            ("forge_formal_predecessor", lambda d: set_path(d, (
                "result", "formal_boundary", "can_serve_as_compact_q_cohort_formal_predecessor"
            ), True)),
            ("mint_formal_disposition", lambda d: set_path(d, (
                "result", "whole_pair_research_conclusion", "formal_disposition_minted"
            ), True)),
            ("c30b_manifest_rebind", lambda d: set_path(d, (
                "result", "authority_binding", "c30b_manifest_sha256"
            ), "0" * 64)),
            ("q6_receipt_rebind", lambda d: set_path(d, (
                "result", "authority_binding", "q6_zero_credit_receipt_sha256"
            ), "0" * 64)),
            ("ledger_changed", lambda d: set_path(d, (
                "result", "formal_boundary", "ledger_unchanged"
            ), False)),
            ("CM2_go", lambda d: set_path(d, (
                "result", "formal_boundary", "CM2"
            ), "GO_FOR_CLAIM")),
        ]

        rejected: list[dict[str, str]] = []
        with tempfile.TemporaryDirectory(prefix="cm2-c30q7-attacks-") as directory:
            work = Path(directory)
            valid = work / "valid.json"
            valid.write_bytes(original_raw)
            baseline = invoke(valid)
            need(baseline.returncode == 0 and baseline.stderr == b"",
                 "valid baseline rejected")
            for index, (name, mutate) in enumerate(attacks):
                attacked = copy.deepcopy(original)
                mutate(attacked)
                path = work / f"attack-{index:02d}.json"
                path.write_bytes(close(attacked))
                process = invoke(path)
                need(process.returncode == 2 and process.stdout == b""
                     and process.stderr.startswith(b"REJECT_C30Q7_VERIFY:"),
                     "coherent attack accepted:" + name)
                rejected.append({"attack": name,
                                 "rejection": process.stderr.decode().strip()})

            malformed = [
                ("duplicate_schema", original_raw.replace(
                    b'{"result":', b'{"schema":"duplicate","result":', 1)),
                ("trailing_document", original_raw + b"{}\n"),
                ("noncanonical_whitespace", b" " + original_raw),
            ]
            for offset, (name, raw) in enumerate(malformed, len(attacks)):
                path = work / f"attack-{offset:02d}.json"
                path.write_bytes(raw)
                process = invoke(path)
                need(process.returncode == 2 and process.stdout == b""
                     and process.stderr.startswith(b"REJECT_C30Q7_VERIFY:"),
                     "malformed accepted:" + name)
                rejected.append({"attack": name,
                                 "rejection": process.stderr.decode().strip()})

            symlink_target = work / "symlink-target.json"
            symlink_target.write_bytes(original_raw)
            symlink_path = work / "candidate-symlink.json"
            symlink_path.symlink_to(symlink_target)
            process = invoke(symlink_path)
            need(process.returncode == 2 and process.stdout == b"",
                 "candidate symlink accepted")
            rejected.append({"attack": "candidate_symlink",
                             "rejection": process.stderr.decode().strip()})

            hard_source = work / "hard-source.json"
            hard_source.write_bytes(original_raw)
            hard_path = work / "candidate-hardlink.json"
            os.link(hard_source, hard_path)
            process = invoke(hard_path)
            need(process.returncode == 2 and process.stdout == b"",
                 "candidate hardlink accepted")
            rejected.append({"attack": "candidate_hardlink",
                             "rejection": process.stderr.decode().strip()})

        total = len(rejected)
        output = {
            "schema": "cm2.round306c30q7.two-witness-coherent-attacks.v1",
            "status": f"PASS_{total}_OF_{total}_COHERENT_ATTACKS_REJECTED",
            "attack_count": total, "rejected": total,
            "valid_baseline_passed": True,
            "mandatory_coverage": {
                "wrong_single_witness_language": True,
                "switch_drift": True,
                "north_south_target_flip": True,
                "boundary_gap_or_overlap": True,
                "old_f_at_1_negative_condition_forgery": True,
            },
            "attacks": rejected,
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, Reject,
            subprocess.SubprocessError) as error:
        sys.stderr.write("REJECT_C30Q7_ATTACKS:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
