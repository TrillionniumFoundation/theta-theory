#!/usr/bin/env python3
"""Coherent candidate attacks for the zero-credit C30q8 audit."""

from __future__ import annotations

import copy
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


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
ROOT = HERE.parent
PRODUCER = (
    HERE
    / "cm2_round306c30q8_compact_q_54_origin_global_template_audit_zero_credit_gate_v1.py"
)
VERIFIER = (
    HERE
    / "cm2_round306c30q8_compact_q_54_origin_global_template_audit_zero_credit_independent_verifier_v1.py"
)
PRODUCER_SHA256 = "d82e72b4063147810fbb2dbce9d8589c39dbf213ad8327e72613ef5f501dfdcb"
VERIFIER_SHA256 = "71dfc7dd056f8691e5870a5cbae837613b4dc9ad115309a9eb32b41f82a23bbd"
EXPECTED_RESULT_SHA256 = "e04b1f73a898b8408062f5feee2618dc51171dc59c14bce15c38ccd1cbb0aab5"


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_capture(path: Path) -> bytes:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical file:" + str(path))
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular single-link file:" + str(path))
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    fields = (
        "st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
        "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid",
    )
    need(all(getattr(before, key) == getattr(after, key) for key in fields),
         "stable file:" + str(path))
    return raw


def close(document: dict[str, Any]) -> None:
    document["result_sha256"] = sha(canonical(document["result"]))


def set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def delete_path(document: dict[str, Any], path: tuple[Any, ...]) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    del cursor[path[-1]]


def mutation(path: tuple[Any, ...], value: Any,
             coherent: bool = True) -> Callable[[dict[str, Any]], None]:
    def apply(document: dict[str, Any]) -> None:
        set_path(document, path, value)
        if coherent:
            close(document)
    return apply


def deletion(path: tuple[Any, ...]) -> Callable[[dict[str, Any]], None]:
    def apply(document: dict[str, Any]) -> None:
        delete_path(document, path)
        close(document)
    return apply


def duplicate_first_cohort_origin(document: dict[str, Any]) -> None:
    row = document["result"]["full_disjoint_cohort_ledger"][0]
    row["origin_keys"][1] = row["origin_keys"][0]
    close(document)


def remove_theorem(document: dict[str, Any]) -> None:
    document["result"]["whole_origin_theorem_candidates"].pop()
    document["result"]["classification_closure"]["research_EXCLUDED_candidates"] = 35
    close(document)


def remove_blocker(document: dict[str, Any]) -> None:
    document["result"]["explicit_blockers"].pop()
    document["result"]["classification_closure"]["undecided_global_miss_origins"] = 5
    close(document)


def alter_first_piecewise_switch(document: dict[str, Any]) -> None:
    row = next(row for row in document["result"]["whole_origin_theorem_candidates"]
               if row["template_id"].startswith("T3_"))
    row["switch"] = "3/4"
    close(document)


def alter_first_piecewise_seam(document: dict[str, Any]) -> None:
    row = next(row for row in document["result"]["whole_origin_theorem_candidates"]
               if row["template_id"].startswith("T3_"))
    row["switch_seam"]["assigned_domains_have_overlap"] = True
    close(document)


def erase_physical_bridge(document: dict[str, Any]) -> None:
    row = next(row for row in document["result"]["whole_origin_theorem_candidates"]
               if row["physical_target_completeness_bridge_required"] is True)
    row["physical_target_completeness_bridge_required"] = False
    close(document)


def alter_first_blocker(document: dict[str, Any], blocker_class: str,
                        key: str, value: Any) -> None:
    row = next(row for row in document["result"]["explicit_blockers"]
               if row["blocker_class"] == blocker_class)
    row[key] = value
    close(document)


def erase_strict_frozen_hit(document: dict[str, Any]) -> None:
    alter_first_blocker(document, "B1_STRICT_INTERIOR_FROZEN_HIT",
                        "whole_origin_EXCLUDED_falsified", False)


def fake_mixed_completion(document: dict[str, Any]) -> None:
    alter_first_blocker(document, "B1_STRICT_INTERIOR_FROZEN_HIT",
                        "RESOLVED_MIXED_exhaustive_partition_proved", True)


def fake_global_miss_exclusion(document: dict[str, Any]) -> None:
    alter_first_blocker(document, "B2_GLOBAL_FROZEN_DISCRIMINANT_NEGATIVE",
                        "proposed_route", "EXCLUDED")


ATTACKS: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
    ("stale_result_closure", mutation(("result", "verdict"), "FORGED", False)),
    ("schema_substitution", mutation(("schema",), "forged.schema")),
    ("pass_status_substitution", mutation(("result", "status"), "PASS_FORGED")),
    ("formal_credit_one", mutation(("result", "formal_boundary", "formal_credit"), 1)),
    ("ledger_changed_lie", mutation(("result", "formal_boundary", "ledger_unchanged"), False)),
    ("source_W_80_to_78_lie", mutation(("result", "formal_boundary", "source_W_formal_remaining"), 78)),
    ("compact_q_54_to_52_lie", mutation(("result", "formal_boundary", "compact_q_formal_remaining_origins"), 52)),
    ("formal_54_to_0_authorized_lie", mutation(("result", "formal_boundary", "formal_54_to_0_authorized"), True)),
    ("terminal_gate_present_lie", mutation(("result", "formal_boundary", "terminal_gate_present"), True)),
    ("CM2_go_lie", mutation(("result", "formal_boundary", "CM2"), "GO_FOR_CLAIM")),
    ("cohort_origin_deletion", deletion(("result", "full_disjoint_cohort_ledger", 0, "origin_keys", 0))),
    ("cohort_origin_duplication", duplicate_first_cohort_origin),
    ("theorem_row_deletion_with_count_reclosure", remove_theorem),
    ("blocker_row_deletion_with_count_reclosure", remove_blocker),
    ("template_substitution", mutation(("result", "whole_origin_theorem_candidates", 0, "template_id"), "T0_FORGED")),
    ("piecewise_switch_substitution", alter_first_piecewise_switch),
    ("half_open_seam_overlap_lie", alter_first_piecewise_seam),
    ("witness_bound_substitution", mutation(("result", "whole_origin_theorem_candidates", 0, "witnesses", 0, "interval_bounds", "tau_minus", "lower"), "[-1]")),
    ("formal_disposition_minted_lie", mutation(("result", "whole_origin_theorem_candidates", 0, "formal_disposition_minted"), True)),
    ("physical_bridge_erasure", erase_physical_bridge),
    ("strict_frozen_hit_erasure", erase_strict_frozen_hit),
    ("mixed_partition_fake_completion", fake_mixed_completion),
    ("global_miss_fake_exclusion", fake_global_miss_exclusion),
    ("future_adapter_fake_presence", mutation(("result", "future_C30f_terminal_adapter_contract", "adapter_exists_now"), True)),
    ("symbolic_certificate_fake_presence", mutation(("result", "proof_boundary", "independent_per_origin_polynomial_or_SOS_certificate_present"), True)),
]


def run_verifier(candidate_path: Path, seed: int) -> subprocess.CompletedProcess[bytes]:
    environment = {
        "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": str(seed),
    }
    return subprocess.run(
        [sys.executable, "-B", "-s", str(VERIFIER), str(candidate_path)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=ROOT, env=environment, timeout=60, check=False,
    )


def rejected(process: subprocess.CompletedProcess[bytes]) -> bool:
    return (process.returncode == 2 and process.stdout == b""
            and process.stderr.startswith(b"REJECT_C30Q8_VERIFY:"))


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage: attack_harness CANDIDATE")
        candidate_path = Path(argv[1]).absolute()
        need(sha(safe_capture(PRODUCER)) == PRODUCER_SHA256, "producer pin")
        need(sha(safe_capture(VERIFIER)) == VERIFIER_SHA256, "verifier pin")
        raw = safe_capture(candidate_path)
        original = json.loads(raw.decode("utf-8", "strict"))
        need(type(original) is dict and raw == canonical(original) + b"\n"
             and original["result_sha256"] == EXPECTED_RESULT_SHA256,
             "canonical frozen baseline")
        records: list[dict[str, Any]] = []
        with tempfile.TemporaryDirectory(prefix="c30q8-attacks-",
                                         dir=candidate_path.parent) as directory:
            work = Path(directory)
            for index, (name, mutate) in enumerate(ATTACKS):
                attacked = copy.deepcopy(original)
                mutate(attacked)
                attack_path = work / f"attack-{index:02d}.json"
                attack_path.write_bytes(canonical(attacked) + b"\n")
                process = run_verifier(attack_path, 30880000 + index)
                need(rejected(process), "attack accepted:" + name)
                records.append({
                    "name": name, "numeric_exit_code": 2, "signal": None,
                    "stdout_empty": True, "rejected": True,
                })

            extra = copy.deepcopy(original)
            extra["unexpected_envelope_member"] = True
            extra_path = work / "attack-extra-envelope.json"
            extra_path.write_bytes(canonical(extra) + b"\n")
            process = run_verifier(extra_path, 30880100)
            need(rejected(process), "extra envelope accepted")
            records.append({"name": "extra_envelope_member", "numeric_exit_code": 2,
                            "signal": None, "stdout_empty": True, "rejected": True})

            symlink_path = work / "attack-symlink.json"
            symlink_path.symlink_to(candidate_path)
            process = run_verifier(symlink_path, 30880101)
            need(rejected(process), "symlink accepted")
            records.append({"name": "candidate_symlink", "numeric_exit_code": 2,
                            "signal": None, "stdout_empty": True, "rejected": True})

            hardlink_path = work / "attack-hardlink.json"
            os.link(candidate_path, hardlink_path)
            try:
                process = run_verifier(hardlink_path, 30880102)
                need(rejected(process), "hardlink accepted")
            finally:
                hardlink_path.unlink(missing_ok=True)
            records.append({"name": "candidate_hardlink", "numeric_exit_code": 2,
                            "signal": None, "stdout_empty": True, "rejected": True})

        need(len(records) == 28 and all(row["rejected"] for row in records),
             "28/28 attacks")
        output = {
            "schema": "cm2.round306c30q8.coherent-attacks.zero-credit.v1",
            "status": "PASS_28_OF_28_COHERENT_C30Q8_ATTACKS_REJECTED",
            "attack_count": len(records), "rejected": len(records),
            "candidate_result_sha256": EXPECTED_RESULT_SHA256,
            "producer_sha256": PRODUCER_SHA256,
            "verifier_sha256": VERIFIER_SHA256,
            "mandatory_coverage": {
                "authority_and_status_substitution": True,
                "formal_credit_and_remaining_lies": True,
                "cohort_partition_and_count_reclosure": True,
                "template_switch_seam_and_bound_substitution": True,
                "EXCLUDED_RESOLVED_MIXED_and_global_miss_lies": True,
                "future_terminal_adapter_and_symbolic_certificate_lies": True,
                "extra_envelope_symlink_and_hardlink": True,
            },
            "records": records,
            "formal_credit": 0, "source_W_formal_remaining": 80,
            "compact_q_formal_remaining": 54,
            "formal_54_to_0_authorized": False,
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, Reject,
            subprocess.SubprocessError, subprocess.TimeoutExpired) as error:
        sys.stderr.write("REJECT_C30Q8_ATTACKS:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
