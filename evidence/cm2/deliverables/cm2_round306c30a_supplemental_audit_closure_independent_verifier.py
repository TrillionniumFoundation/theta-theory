#!/usr/bin/env python3
"""Independent, additive preflight for a C30a supplemental audit closure.

The original 13-member C30a manifest is a trust root and is read before any
other workspace evidence.  This verifier does not import or execute the C30a
producer/verifier/harness.  It checks the original seal, the two retained
candidate copies, and a fresh offline runtime attestation.  The attestation
verifies the machine interpreter, sealed wheel, glibc/manylinux compatibility,
and every hashed wheel/installed RECORD row.

Success here means *only* that the additive closure is ready for its expensive
controlled-seed, independent-verifier, syscall-trace, and attack replays.  It
does not mint a final closure and can never authorize ``252 -> 90``.

Required invocation::

    .cm2-runtime/python-flint-0.9.0/bin/python -I -B \
      deliverables/cm2_round306c30a_supplemental_audit_closure_independent_verifier.py
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


sys.dont_write_bytecode = True

SCRIPT = Path(__file__).resolve(strict=True)
DELIVERABLES = SCRIPT.parent
WORKSPACE = DELIVERABLES.parent

BASE_PREFIX = (
    "cm2_round306c30a_source_w_162_reduced_clipped_delta_"
    "whole_origin_promotion"
)
BASE_MANIFEST = DELIVERABLES / (BASE_PREFIX + "_manifest.sha256")
BASE_MANIFEST_SHA256 = (
    "0f3e80d54d4307eccf509435470213e19fd4eefffc43b95e01cec0d3b8a094bc"
)
BASE_MEMBERS = {
    "cm2_round306c30a_python_flint_requirements.lock":
        "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c",
    "cm2_round306c30a_python_flint_runtime_lock.json":
        "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79",
    (
        "cm2_round306c30a_runtime/"
        "python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64."
        "manylinux_2_17_x86_64.whl"
    ): "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76",
    BASE_PREFIX + "_attack_harness.py":
        "debdb1ac9d3b840660600cec66dd2b6b1d45eb5847d366c989a652f893bb3c17",
    BASE_PREFIX + "_cold_replay.md":
        "6bac45a8150603370380afca729220fc2c6da9e3d3580ea3b535b9d2b37a94c5",
    BASE_PREFIX + "_independent_verifier.py":
        "5af75a97e9c306cc47a514e4c87ae875a8388bb75d9274d106b64e2ceee87c7c",
    BASE_PREFIX + "_producer.py":
        "41a3f11c3e44bdbbfcf95edf88902669365186e6fb6394aaee15a6846dc91714",
    BASE_PREFIX + "_report.md":
        "e2811b8c9a676e08e1e3014a10ca693ee651f4d143b38540a1ac53195f4b8562",
    BASE_PREFIX + "_verification.json":
        "f02f7e3144541284819947c549ce91d8f1d6e9df24c0bdb4b981077f1e358d07",
    "cm2_round306c30a_sealed/" + BASE_PREFIX + "_cell_ledger.jsonl.gz":
        "c4c0061a08983471428b2e5113aff60bbeccc67530cac691658a6bbad1ce9904",
    (
        "cm2_round306c30a_sealed/" + BASE_PREFIX
        + "_inherited_h_obstruction_ledger.jsonl.gz"
    ): "f86c6c3d90a4a87c7d4366b86a0e8119d019cbf86f5b5ab781140605ddc1e80e",
    "cm2_round306c30a_sealed/" + BASE_PREFIX + "_result.json":
        "521be2aefebea96d6a3d2ce1bcf0234753ef69af7182a4e47a0d22d686df6c48",
    (
        "cm2_round306c30a_sealed/" + BASE_PREFIX
        + "_whole_origin_ledger.jsonl.gz"
    ): "778995522629a362183159420860b65d60c8719bc1453c4fc2657e8e8fba9649",
}

RUNTIME_AUDITOR_NAME = (
    "cm2_round306c30b_python_flint_runtime_attestation_auditor.py"
)
RUNTIME_AUDITOR = DELIVERABLES / RUNTIME_AUDITOR_NAME
RUNTIME_AUDITOR_SHA256 = (
    "0309dc5710421a5e56b0d1b7b04ef2c5ccf971d054943dc6baf7765e512b76f8"
)
CONTROLLED_LAUNCHER_NAME = (
    "cm2_round306c30a_supplemental_audit_closure_"
    "controlled_replay_launcher.py"
)
CONTROLLED_LAUNCHER = DELIVERABLES / CONTROLLED_LAUNCHER_NAME
CONTROLLED_LAUNCHER_SHA256 = (
    "1437e60dd0b49e213b50615a3d5a7991c5bee1199edfda8b7495424d35a767cf"
)
ATTACK_HARNESS_NAME = (
    "cm2_round306c30a_supplemental_audit_closure_"
    "coherent_attack_harness.py"
)
ATTACK_HARNESS = DELIVERABLES / ATTACK_HARNESS_NAME
ATTACK_HARNESS_SHA256 = (
    "2fbeed7dad99e7d71076cc82cb9449d647153e11b563ecf87bdba1c3a0d32034"
)

RESULT_NAME = BASE_PREFIX + "_result.json"
OUTPUT_NAMES = (
    BASE_PREFIX + "_cell_ledger.jsonl.gz",
    BASE_PREFIX + "_inherited_h_obstruction_ledger.jsonl.gz",
    RESULT_NAME,
    BASE_PREFIX + "_whole_origin_ledger.jsonl.gz",
)
CANDIDATES = (
    ".cm2-runtime/candidates/c30a-final-seed30630071",
    ".cm2-runtime/candidates/c30a-final-seed30630929",
)

SHA_LINE = re.compile(r"([0-9a-f]{64})  ([!-~]+)\n")
EXPECTED_RESULT_OBJECT_SHA256 = (
    "32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09"
)
EXPECTED_TRANSFORMED_PRODUCER_SHA256 = (
    "6105ad2e3aeffbd2a27063a7e9b56cdadaeb22e8e96f8daf987f0a5763ac923e"
)


class Reject(RuntimeError):
    """A fail-closed preflight check rejected the evidence."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_regular(
    path: Path,
    *,
    maximum: int = 512 * 1024 * 1024,
    allow_empty: bool = False,
) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and (allow_empty or status.st_size > 0)
        and 0 <= status.st_size <= maximum,
        "regular singleton:" + os.fspath(path),
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino, opened.st_size)
            == (status.st_dev, status.st_ino, status.st_size),
            "opened identity:" + os.fspath(path),
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1 << 20, remaining))
            require(bool(block), "short read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing input:" + os.fspath(path))
        final = os.fstat(descriptor)
        require(
            (final.st_dev, final.st_ino, final.st_size)
            == (opened.st_dev, opened.st_ino, opened.st_size),
            "changed input:" + os.fspath(path),
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(raw and b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"),
            "JSON encoding:" + label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(type(key) is str and key not in output,
                    "JSON duplicate:" + label)
            output[key] = value
        return output

    def reject_constant(token: str) -> None:
        raise ValueError(token)

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique,
            parse_constant=reject_constant,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    require(type(value) is dict, "JSON top object:" + label)
    return value


def manifest_first() -> dict[str, str]:
    """Read and close the original 13-member seal before all other evidence."""

    raw = read_regular(BASE_MANIFEST, maximum=64 * 1024)
    require(sha256(raw) == BASE_MANIFEST_SHA256, "base manifest trust-root sha256")
    cursor = 0
    members: dict[str, str] = {}
    text = raw.decode("ascii", "strict")
    for match in SHA_LINE.finditer(text):
        require(match.start() == cursor, "base manifest canonical lines")
        cursor = match.end()
        digest, name = match.groups()
        pure = PurePosixPath(name)
        require(
            not pure.is_absolute()
            and all(part not in {"", ".", ".."} for part in pure.parts)
            and pure.as_posix() == name
            and name not in members,
            "base manifest safe unique path",
        )
        members[name] = digest
    require(cursor == len(text), "base manifest complete parse")
    require(members == BASE_MEMBERS and len(members) == 13,
            "base manifest exact 13 members")
    for name in sorted(members):
        path = DELIVERABLES / name
        require(path.resolve(strict=True).is_relative_to(DELIVERABLES),
                "base member containment:" + name)
        require(sha256(read_regular(path)) == members[name],
                "base member sha256:" + name)
    return members


def validate_fixed_transition() -> dict[str, Any]:
    result_path = DELIVERABLES / "cm2_round306c30a_sealed" / RESULT_NAME
    raw = read_regular(result_path, maximum=1024 * 1024)
    result = strict_json(raw, RESULT_NAME)
    require(canonical(result) == raw, "base result canonical bytes")
    transition = result["source_W_ledger_transition"]
    before = transition["before"]
    after = transition["after"]
    census = result["whole_origin_census"]
    held = census["Round306C30A_inherited_H_held"]
    require(
        result["result_sha256"] == EXPECTED_RESULT_OBJECT_SHA256
        and before["remaining"] == 252
        and after["remaining"] == 92
        and transition["new_whole_origin_exclusion_credit"] == 160
        and census["Round306C30A_new_promoted"] == 160
        and held == 2
        and result["formal_credit"]["whole_source_W_origin_exclusions"] == 160
        and result["strict_nonpromotion"]["D02"]
        == "BLOCKED_BY_92_REMAINING_SOURCE_W_ORIGINS"
        and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "fixed fail-closed 252-to-92 transition",
    )
    require(after["remaining"] != 90, "forbidden 252-to-90 overclaim")
    return {
        "before": 252,
        "after": 92,
        "new_whole_origin_exclusions": 160,
        "held_origins": 2,
        "result_object_sha256": result["result_sha256"],
    }


def validate_candidate_copies() -> dict[str, Any]:
    sealed = DELIVERABLES / "cm2_round306c30a_sealed"
    tables: dict[str, dict[str, str]] = {}
    for candidate_relpath in CANDIDATES:
        candidate = WORKSPACE / candidate_relpath
        require(candidate.is_dir() and not candidate.is_symlink(),
                "candidate directory:" + candidate_relpath)
        names = sorted(entry.name for entry in candidate.iterdir())
        require(names == sorted(OUTPUT_NAMES),
                "candidate exact output set:" + candidate_relpath)
        table: dict[str, str] = {}
        for name in OUTPUT_NAMES:
            candidate_raw = read_regular(candidate / name)
            sealed_raw = read_regular(sealed / name)
            require(candidate_raw == sealed_raw,
                    "candidate/seal bytes:" + candidate_relpath + ":" + name)
            table[name] = sha256(candidate_raw)
        tables[candidate_relpath] = table
    require(len({canonical(table) for table in tables.values()}) == 1,
            "historical candidate copies byte-identical")
    return {
        "historical_runs_only_not_controlled_seed_evidence": True,
        "candidate_count": len(tables),
        "file_count_per_candidate": len(OUTPUT_NAMES),
        "file_table": next(iter(tables.values())),
    }


def run_runtime_attestation() -> dict[str, Any]:
    auditor_raw = read_regular(RUNTIME_AUDITOR, maximum=4 * 1024 * 1024)
    require(sha256(auditor_raw) == RUNTIME_AUDITOR_SHA256,
            "runtime auditor pin")
    run = subprocess.run(
        [sys.executable, "-I", "-B", os.fspath(RUNTIME_AUDITOR)],
        cwd=WORKSPACE,
        env={
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PATH": "/usr/bin:/bin",
            "TZ": "UTC",
        },
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(run.returncode == 0 and run.stderr == b"",
            "fresh runtime auditor exit/stderr")
    require(run.stdout.endswith(b"\n") and run.stdout.count(b"\n") == 1,
            "fresh runtime auditor one stdout document")
    raw = run.stdout[:-1]
    attestation = strict_json(raw, "fresh runtime attestation")
    require(canonical(attestation) == raw,
            "fresh runtime attestation canonical bytes")
    wheel = attestation["sealed_wheel"]
    interpreter = attestation["interpreter"]
    installed = attestation["installed_distribution"]
    imported = attestation["imported_flint"]
    require(
        attestation["verdict"] == "PASS"
        and attestation["offline"] is True
        and attestation["trust_roots"]["p0_runtime_lock"]["sha256"]
        == BASE_MEMBERS["cm2_round306c30a_python_flint_runtime_lock.json"]
        and attestation["trust_roots"]["requirements_lock"]["sha256"]
        == BASE_MEMBERS["cm2_round306c30a_python_flint_requirements.lock"]
        and interpreter["resolved_executable_sha256"]
        == "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
        and interpreter["python_version"] == "3.12.3"
        and interpreter["cache_tag"] == "cpython-312"
        and interpreter["architecture"] == "x86_64"
        and interpreter["glibc"] == "2.39"
        and wheel["sha256"]
        == "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76"
        and wheel["compatibility_tags"] == [
            "cp310-abi3-manylinux2014_x86_64",
            "cp310-abi3-manylinux_2_17_x86_64",
        ]
        and wheel["record_verification"] == {
            "entry_count": 113,
            "hashed_entry_count": 112,
            "unhashed_entry_count": 1,
            "unhashed_paths": ["python_flint-0.9.0.dist-info/RECORD"],
        }
        and installed["record_verification"]["entry_count"] == 139
        and installed["record_verification"]["hashed_entry_count"] == 114
        and installed["record_verification"]["unhashed_entry_count"] == 25
        and installed["sealed_wheel_member_match_count"] == 112
        and imported["python_flint_version"] == "0.9.0"
        and imported["flint_version"] == "3.6.0"
        and imported["flint_release"] == 30600,
        "runtime lock/machine/wheel/glibc/RECORD closure",
    )
    return {
        "auditor_path": "deliverables/" + RUNTIME_AUDITOR_NAME,
        "auditor_sha256": sha256(auditor_raw),
        "fresh_attestation_sha256": sha256(raw),
        "machine_python_sha256": interpreter["resolved_executable_sha256"],
        "glibc": interpreter["glibc"],
        "manylinux_floor": "manylinux_2_17_x86_64",
        "wheel_sha256": wheel["sha256"],
        "wheel_record_hashed_rows_verified": 112,
        "installed_record_hashed_rows_verified": 114,
        "python_flint": imported["python_flint_version"],
        "flint": imported["flint_version"],
    }


def validate_supplemental_tools() -> dict[str, Any]:
    launcher_raw = read_regular(CONTROLLED_LAUNCHER, maximum=4 * 1024 * 1024)
    require(sha256(launcher_raw) == CONTROLLED_LAUNCHER_SHA256,
            "controlled replay launcher pin")
    attack_raw = read_regular(ATTACK_HARNESS, maximum=4 * 1024 * 1024)
    require(sha256(attack_raw) == ATTACK_HARNESS_SHA256,
            "persistent coherent attack harness pin")
    return {
        "controlled_replay_launcher": {
            "path": "deliverables/" + CONTROLLED_LAUNCHER_NAME,
            "sha256": sha256(launcher_raw),
            "permitted_seeds": [30630071, 30630929],
            "python_flags": ["-P", "-s", "-B"],
            "isolated_mode_forbidden": True,
            "one_byte_transformed_producer_sha256":
                EXPECTED_TRANSFORMED_PRODUCER_SHA256,
        },
        "persistent_coherent_attack_harness": {
            "path": "deliverables/" + ATTACK_HARNESS_NAME,
            "sha256": sha256(attack_raw),
            "attack_count": 10,
            "retains_each_forged_candidate_stdout_stderr_and_exit": True,
            "held_to_promoted_162_overclaim_full_reclosure_included": True,
        },
        "frozen_rebuild_recipe": [
            "/usr/bin/python3.12 -m venv --clear .cm2-runtime/python-flint-0.9.0",
            (
                ".cm2-runtime/python-flint-0.9.0/bin/python -I -B -m pip "
                "install --no-index --no-deps --only-binary=:all: "
                "--require-hashes --find-links "
                "deliverables/cm2_round306c30a_runtime -r "
                "deliverables/cm2_round306c30a_python_flint_requirements.lock"
            ),
        ],
        "rebuild_recipe_is_reconstruction_not_original_creation_provenance": True,
    }


def build() -> dict[str, Any]:
    require(
        sys.flags.isolated == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.dont_write_bytecode is True
        and sys.prefix != sys.base_prefix
        and Path(sys.prefix).resolve(strict=True)
        == (WORKSPACE / ".cm2-runtime/python-flint-0.9.0").resolve(strict=True),
        "locked isolated verifier runtime",
    )
    members = manifest_first()
    transition = validate_fixed_transition()
    candidates = validate_candidate_copies()
    runtime = run_runtime_attestation()
    tools = validate_supplemental_tools()
    body: dict[str, Any] = {
        "schema": "cm2.round306c30a.supplemental-audit-closure-preflight.v1",
        "status": (
            "READY_FOR_EXPENSIVE_SUPPLEMENTAL_REPLAYS__"
            "NOT_A_C30A_AUDIT_CLOSURE_PASS"
        ),
        "formal_credit": {
            "additional_whole_origin_exclusions": 0,
            "source_W_transition": "252_TO_92_ONLY",
            "source_W_252_to_90": "FORBIDDEN",
        },
        "manifest_first": {
            "path": "deliverables/" + BASE_MANIFEST.name,
            "sha256": BASE_MANIFEST_SHA256,
            "member_count": len(members),
            "all_members_verified": True,
        },
        "fixed_transition": transition,
        "historical_candidates": candidates,
        "runtime_identity": runtime,
        "supplemental_tools": tools,
        "still_required_before_closure": [
            "TWO_TRUE_CONTROLLED_HASH_SEED_PRODUCER_REPLAYS",
            "BOTH_REPLAYS_BYTE_IDENTICAL_TO_THE_ORIGINAL_13_MEMBER_SEAL",
            "SCRUBBED_FRESH_CANDIDATE_REPLAY_WITH_RAW_SYSCALL_TRACE",
            "INDEPENDENT_VERIFIER_RAW_STDOUT_STDERR_EXIT_AND_SYSCALL_TRACE",
            "TEN_COHERENT_ATTACKS_WITH_PER_ATTACK_RAW_OUTPUTS",
            "HELD_TO_PROMOTED_FULL_RECLOSURE_ATTACK_INCLUDED",
            "SUPPLEMENTAL_MANIFEST_AND_EXTERNAL_SHA256_PIN",
        ],
    }
    body["payload_sha256"] = sha256(canonical(body))
    return body


def main() -> int:
    try:
        result = build()
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_PREFLIGHT_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    sys.stdout.buffer.write(canonical(result) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
