#!/usr/bin/env python3
"""Coherent negative harness for the independent C30q0 verifier.

The expensive upstream reconstruction is performed once.  Each semantic
attack then re-closes the candidate result digest before validation so that
rejection occurs at the intended mathematical layer.  Encoding and path
attacks exercise the verifier's byte-capture boundary directly.  No attack or
baseline pass grants formal credit.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import copy
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import types
from typing import Any, Callable


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
AUDIT_ROOT = WORKSPACE / ".cm2-runtime" / "audit"
VERIFIER = (
    HERE
    / "cm2_round306c30q0_compact_q_representative_origin_analytic_"
      "independent_verifier.py"
)
VERIFIER_SHA256 = (
    "f6008cc943845b54b7f6833d2f7e6a24d6f2340db0c7ef696dc37e792d65910b"
)
CANDIDATE = (
    AUDIT_ROOT
    / "c30q0-representative-analytic-v2-20260807T1021"
    / "stdout.json"
)
CANDIDATE_SHA256 = (
    "bca0c9882db0fefe5fad65617c73418218330e8cdb651dbe04f8c64ff3725968"
)
PRODUCER_STEM = (
    "cm2_round306c30q0_compact_q_representative_origin_analytic_probe"
)
SCHEMA = (
    "cm2.round306c30q0.compact-q-representative-origin-analytic-"
    "coherent-negative-harness.v1"
)


class HarnessFailure(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise HarnessFailure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def identity(value: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def capture_verifier() -> tuple[bytes, tuple[int, int, int, int, int, int, int]]:
    absolute = Path(os.path.abspath(os.fspath(VERIFIER)))
    require(absolute.resolve(strict=True) == absolute, "verifier canonical path")
    before_path = absolute.lstat()
    require(
        stat.S_ISREG(before_path.st_mode)
        and before_path.st_nlink == 1
        and before_path.st_size < 4 << 20,
        "verifier regular singleton",
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        before = os.fstat(descriptor)
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    current = absolute.lstat()
    require(
        identity(before_path) == identity(before) == identity(after) == identity(current),
        "verifier stable capture",
    )
    raw = b"".join(chunks)
    require(
        len(raw) == before.st_size and hashlib.sha256(raw).hexdigest() == VERIFIER_SHA256,
        "verifier byte pin",
    )
    return raw, identity(before)


def load_verifier() -> tuple[types.ModuleType, bytes]:
    raw, captured = capture_verifier()
    name = "cm2_c30q0_independent_verifier_pinned_for_negative_harness"
    module = types.ModuleType(name)
    module.__file__ = os.fspath(VERIFIER)
    module.__package__ = ""
    exec(compile(raw, os.fspath(VERIFIER), "exec", dont_inherit=True), module.__dict__)
    require(capture_verifier()[1] == captured, "verifier stable after load")
    require(
        callable(module.reconstruct_reference)
        and callable(module.validate_candidate)
        and callable(module.verify_candidate_path)
        and callable(module.decode_candidate),
        "verifier callable surface",
    )
    return module, raw


def reclose(document: dict[str, Any]) -> bytes:
    document["result_sha256"] = digest(document["result"])
    return canonical(document) + b"\n"


def mutate_frozen_target(document: dict[str, Any]) -> bytes:
    frozen = document["result"]["analytic_whole_origin_certificate"][
        "frozen_target_strictly_behind"
    ]
    frozen["target"] = "W[0,1]"
    frozen["center_displacement"] = "(0,1)-(4/25)*n"
    return reclose(document)


def mutate_k(document: dict[str, Any]) -> bytes:
    analytic = document["result"]["analytic_whole_origin_certificate"]
    analytic["coarse_radical_witnesses"]["q_squared_exact_maximum"] = "1/256"
    analytic["coarse_radical_witnesses"]["q_squared_upper_gap"] = "0"
    analytic["coordinate_definitions"]["q"] = "sqrt(1/256)*r, 0<=r<=1"
    return reclose(document)


def mutate_t_domain(document: dict[str, Any]) -> bytes:
    domain = document["result"]["analytic_whole_origin_certificate"]["exact_domain"]
    domain["t"][0] = "-1/10"
    return reclose(document)


def mutate_s_domain(document: dict[str, Any]) -> bytes:
    domain = document["result"]["analytic_whole_origin_certificate"]["exact_domain"]
    domain["s"][0] = "-1/500"
    return reclose(document)


def mutate_root_box(document: dict[str, Any]) -> bytes:
    partition = document["result"]["root_box_partition"]
    partition["root_box_rows"][0]["t"][0] = "-1/10"
    partition["root_box_rows_sha256"] = digest(partition["root_box_rows"])
    return reclose(document)


def recensus_owner_partition(partition: dict[str, Any]) -> None:
    rows = partition["owner_assignment_rows"]
    dimensions = Counter(row["ambient_dimension"] for row in rows)
    multiplicities = Counter(row["incident_root_count"] for row in rows)
    partition["atomic_stratum_count"] = len(rows)
    partition["atomic_stratum_count_by_dimension"] = {
        str(key): dimensions[key] for key in sorted(dimensions, reverse=True)
    }
    partition["incident_root_multiplicity_count"] = {
        str(key): multiplicities[key] for key in sorted(multiplicities)
    }
    partition["owner_root_count"] = len({row["owner_root_key"] for row in rows})
    partition["owner_assignment_rows_sha256"] = digest(rows)


def mutate_boundary_atom_drop(document: dict[str, Any]) -> bytes:
    partition = document["result"]["cross_root_half_open_owner_partition"]
    index = next(
        index
        for index, row in enumerate(partition["owner_assignment_rows"])
        if row["ambient_dimension"] < 3
    )
    partition["owner_assignment_rows"].pop(index)
    recensus_owner_partition(partition)
    return reclose(document)


def mutate_owner_rule(document: dict[str, Any]) -> bytes:
    partition = document["result"]["cross_root_half_open_owner_partition"]
    partition["rule"] = "lexicographically greatest incident root"
    return reclose(document)


def mutate_boundary_owner(document: dict[str, Any]) -> bytes:
    partition = document["result"]["cross_root_half_open_owner_partition"]
    row = next(
        row for row in partition["owner_assignment_rows"]
        if row["incident_root_count"] > 1
    )
    row["owner_root_key"] = row["incident_root_keys"][-1]
    recensus_owner_partition(partition)
    return reclose(document)


def mutate_future_margin(document: dict[str, Any]) -> bytes:
    future = document["result"]["analytic_whole_origin_certificate"][
        "certified_nonfrozen_strict_future_root"
    ]
    future["absolute_transverse_strict_upper"] = "3/20"
    future["radius_minus_absolute_transverse_strict_lower"] = "1/100"
    return reclose(document)


def mutate_frozen_bound(document: dict[str, Any]) -> bytes:
    frozen = document["result"]["analytic_whole_origin_certificate"][
        "frozen_target_strictly_behind"
    ]
    frozen["uniform_strict_upper"] = "0"
    frozen["future_root_possible"] = True
    return reclose(document)


def mutate_full_r_bridge(document: dict[str, Any]) -> bytes:
    replay = document["result"]["targeted_upstream_complement_replay"]
    replay["Round176_source_grazing_p_interval"] = ["255/256", "1"]
    replay["Round176_source_grazing_q_parameterization"] = (
        "q=sqrt(511/65536)*r, r in [0,1]"
    )
    return reclose(document)


def mutate_complement_count(document: dict[str, Any]) -> bytes:
    replay = document["result"]["targeted_upstream_complement_replay"]
    replay["exact_behind_closed_child_count"] = 326
    replay["exact_behind_residual_child_count"] = 2
    return reclose(document)


def mutate_residual_child(document: dict[str, Any]) -> bytes:
    replay = document["result"]["targeted_upstream_complement_replay"]
    replay["exact_behind_residual_child"]["active_targets"].append("W[1,0]")
    return reclose(document)


def mutate_formal_credit(document: dict[str, Any]) -> bytes:
    boundary = document["result"]["strict_nonpromotion"]
    boundary["formal_credit"] = 1
    boundary["compact_q_formal_remaining_origins"] = 53
    return reclose(document)


def mutate_overextension(document: dict[str, Any]) -> bytes:
    conclusion = document["result"]["representative_conclusion"]
    conclusion["conditional_research_transition"] = "54 -> 0"
    conclusion["scope"] = "all compact-q origins"
    return reclose(document)


@dataclass(frozen=True)
class Attack:
    name: str
    expected_prefix: str
    mode: str
    mutate: Callable[[dict[str, Any]], bytes] | None = None


ATTACKS = (
    Attack("frozen_target_rebind", "candidate frozen target", "semantic", mutate_frozen_target),
    Attack("compact_K_rewrite", "candidate compact K", "semantic", mutate_k),
    Attack("t_domain_cut_shift", "candidate domain cuts", "semantic", mutate_t_domain),
    Attack("s_domain_cut_shift", "candidate domain cuts", "semantic", mutate_s_domain),
    Attack("root_box_boundary_shift", "candidate dynamic root boxes", "semantic", mutate_root_box),
    Attack("boundary_atom_drop", "candidate atomic owner rows", "semantic", mutate_boundary_atom_drop),
    Attack("owner_rule_max_instead_of_min", "candidate owner rule", "semantic", mutate_owner_rule),
    Attack("boundary_owner_retarget", "candidate atomic owner rows", "semantic", mutate_boundary_owner),
    Attack("future_root_margin_shrink", "candidate future-root margin", "semantic", mutate_future_margin),
    Attack("frozen_projection_bound_clear", "candidate frozen-behind inequality", "semantic", mutate_frozen_bound),
    Attack("full_r_bridge_reparameterize", "candidate full-r bridge", "semantic", mutate_full_r_bridge),
    Attack("complement_327_plus_1_recount", "candidate complement counts", "semantic", mutate_complement_count),
    Attack("residual_child_add_frozen_target", "candidate exact upstream complement", "semantic", mutate_residual_child),
    Attack("formal_credit_pregrant", "candidate formal credit", "semantic", mutate_formal_credit),
    Attack("representative_to_global_overextension", "candidate representative conclusion", "semantic", mutate_overextension),
    Attack("candidate_noncanonical_space", "candidate canonical bytes", "noncanonical"),
    Attack("candidate_duplicate_schema_key", "duplicate JSON key:schema", "duplicate"),
    Attack("candidate_trailing_document", "strict JSON:candidate", "trailing"),
    Attack("candidate_symlink", "canonical path:candidate stdout", "symlink"),
    Attack("candidate_atomic_replace_during_read", "stable capture:candidate stdout", "toctou"),
)


def expect_reject(verifier: types.ModuleType, callback: Callable[[], None], attack: Attack) -> str:
    try:
        callback()
    except verifier.Reject as error:
        reason = str(error)
        require(
            reason.startswith(attack.expected_prefix),
            "wrong rejection reason:" + attack.name + ":" + reason,
        )
        return type(error).__name__ + ":" + reason
    except BaseException as error:
        raise HarnessFailure(
            "unexpected exception:" + attack.name + ":"
            + type(error).__name__ + ":" + str(error)
        ) from error
    raise HarnessFailure("attack accepted:" + attack.name)


def run_attack(
    verifier: types.ModuleType,
    baseline: dict[str, Any],
    baseline_raw: bytes,
    reference: dict[str, Any],
    temporary: Path,
    attack: Attack,
) -> str:
    if attack.mode == "semantic":
        require(attack.mutate is not None, "semantic mutator:" + attack.name)
        document = copy.deepcopy(baseline)
        raw = attack.mutate(document)
        require(raw != baseline_raw, "semantic attack changes bytes:" + attack.name)
        return expect_reject(
            verifier,
            lambda: verifier.validate_candidate(verifier.decode_candidate(raw), reference),
            attack,
        )
    if attack.mode == "noncanonical":
        raw = b" " + baseline_raw
        return expect_reject(verifier, lambda: verifier.decode_candidate(raw), attack)
    if attack.mode == "duplicate":
        raw = b'{"schema":"forged",' + baseline_raw[1:]
        return expect_reject(verifier, lambda: verifier.decode_candidate(raw), attack)
    if attack.mode == "trailing":
        raw = baseline_raw + b"{}\n"
        return expect_reject(verifier, lambda: verifier.decode_candidate(raw), attack)
    if attack.mode == "symlink":
        target = temporary / "symlink-target.json"
        alias = temporary / "candidate-symlink.json"
        target.write_bytes(baseline_raw)
        alias.symlink_to(target.name)
        return expect_reject(
            verifier,
            lambda: verifier.verify_candidate_path(alias, reference, False),
            attack,
        )
    if attack.mode == "toctou":
        target = temporary / "candidate-race.json"
        replacement = temporary / "candidate-race-replacement.json"
        target.write_bytes(baseline_raw)
        replacement.write_bytes(baseline_raw)
        original_read = verifier.os.read
        fired = False

        def racing_read(descriptor: int, size: int) -> bytes:
            nonlocal fired
            block = original_read(descriptor, size)
            if not fired:
                fired = True
                os.replace(replacement, target)
            return block

        verifier.os.read = racing_read
        try:
            reason = expect_reject(
                verifier,
                lambda: verifier.verify_candidate_path(target, reference, False),
                attack,
            )
        finally:
            verifier.os.read = original_read
        require(fired, "TOCTOU attack fired")
        return reason
    raise HarnessFailure("unknown attack mode:" + attack.mode)


def smoke(verifier: types.ModuleType, verifier_raw: bytes) -> dict[str, Any]:
    tree = ast.parse(verifier_raw, filename=os.fspath(VERIFIER))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    require(
        PRODUCER_STEM not in imports
        and "T_CUTS" not in names
        and PRODUCER_STEM.encode("ascii") in verifier_raw,
        "verifier producer-byte-only and dynamic-cut AST",
    )
    rejected: list[str] = []
    for label, raw in (
        ("duplicate", b'{"x":1,"x":2}\n'),
        ("trailing", b'{"x":1}\n{}\n'),
        ("space", b' {"x":1}\n'),
        ("float", b'{"x":1.0}\n'),
    ):
        try:
            verifier.decode_candidate(raw)
        except verifier.Reject:
            rejected.append(label)
        else:
            raise HarnessFailure("smoke accepted:" + label)
    return {
        "schema": SCHEMA + ".smoke.v1",
        "status": "PASS_AST_AND_4_OF_4_NEGATIVE_SMOKE_CASES",
        "attack_count": len(ATTACKS),
        "negative_smoke_rejected": rejected,
        "formal_credit": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    verifier, verifier_raw = load_verifier()
    if arguments.smoke:
        print(canonical(smoke(verifier, verifier_raw)).decode("utf-8"))
        return 0

    baseline_raw = verifier.capture_regular(CANDIDATE, "harness baseline candidate", 2 << 20)[0]
    require(hashlib.sha256(baseline_raw).hexdigest() == CANDIDATE_SHA256, "baseline candidate pin")
    baseline = verifier.decode_candidate(baseline_raw)
    reference = verifier.reconstruct_reference()
    verified, verified_hash = verifier.verify_candidate_path(CANDIDATE, reference, True)
    require(
        verified_hash == CANDIDATE_SHA256
        and canonical(verified) + b"\n" == baseline_raw,
        "baseline exact accepted bytes",
    )
    before = file_sha256(CANDIDATE)
    outcomes: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="c30q0-attacks-", dir=AUDIT_ROOT) as name:
        temporary = Path(name)
        for attack in ATTACKS:
            reason = run_attack(
                verifier, baseline, baseline_raw, reference, temporary, attack
            )
            outcomes.append({
                "attack": attack.name,
                "expected_reason_prefix": attack.expected_prefix,
                "rejection": reason,
            })
    require(
        len(outcomes) == len(ATTACKS)
        and len({row["attack"] for row in outcomes}) == len(ATTACKS)
        and file_sha256(CANDIDATE) == before == CANDIDATE_SHA256,
        "all attacks exact and baseline immutable",
    )
    self_hash = file_sha256(Path(__file__).resolve())
    output = {
        "schema": SCHEMA,
        "status": (
            "PASS_" + str(len(outcomes)) + "_OF_" + str(len(ATTACKS))
            + "_COHERENT_NEGATIVE_ATTACKS_REJECTED_WITH_EXACT_REASONS__"
              "ZERO_FORMAL_CREDIT"
        ),
        "harness_sha256": self_hash,
        "verifier_sha256": VERIFIER_SHA256,
        "candidate_sha256": CANDIDATE_SHA256,
        "attack_count": len(outcomes),
        "rejected_count": len(outcomes),
        "skipped_count": 0,
        "attacks": outcomes,
        "formal_credit": 0,
        "formal_remaining_origins": 80,
        "compact_q_formal_remaining_origins": 54,
        "CM2": "NO-GO_FOR_CLAIM",
    }
    print(canonical(output).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
