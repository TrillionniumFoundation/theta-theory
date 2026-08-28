#!/usr/bin/env python3
"""Execute the fresh Docker-network-none C30a supplemental P0-B v5 chain."""

from __future__ import annotations

import argparse
import concurrent.futures
import ctypes
import datetime
import errno
import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

_DELIVERABLES_BOOTSTRAP = os.path.dirname(os.path.abspath(__file__))
if _DELIVERABLES_BOOTSTRAP not in sys.path:
    sys.path.insert(0, _DELIVERABLES_BOOTSTRAP)

import cm2_round306c30a_supplemental_audit_closure_v5_common as common
import cm2_round306c30a_supplemental_audit_closure_v5_release_checker as checker
import cm2_round306c30a_supplemental_audit_closure_v5_trace_lib as traces


sys.dont_write_bytecode = True

DOCKER = "/usr/bin/docker"
TIME = "/usr/bin/time"
STRACE = "/usr/bin/strace"
ENV = "/usr/bin/env"
IMAGE_REFERENCE = "alpine:3.20"
IMAGE_ID = "sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc"
RUNTIME_ALIAS = (
    common.WORKSPACE / ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807"
)
REBUILD = common.DELIVERABLES / "cm2_round306c30a_python_flint_fresh_runtime_rebuild.py"
ATTESTOR = common.DELIVERABLES / "cm2_round306c30a_python_flint_fresh_runtime_attestor.py"
LAUNCHER = common.DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_controlled_replay_launcher.py"
)
COMPARATOR = common.DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_v5_comparator.py"
)
VERIFIER = common.DELIVERABLES / (common.BASE_PREFIX + "_independent_verifier.py")
ATTACK_HARNESS = common.DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_coherent_attack_harness.py"
)
TRACE_AUDITOR = common.DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_v5_trace_auditor.py"
)
RELEASE_CHECKER = common.DELIVERABLES / (
    "cm2_round306c30a_supplemental_audit_closure_v5_release_checker.py"
)
UID = os.getuid()
GID = os.getgid()
DOCKER_USER = f"{UID}:{GID}"


def env_i(assignments: dict[str, str], argv: list[str]) -> list[str]:
    return [
        ENV, "-i",
        *(key + "=" + assignments[key] for key in sorted(assignments)),
        *argv,
    ]


BASE_ENV = {
    "HOME": "/nonexistent",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "TZ": "UTC",
}


def _subprocess_raw(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _inspect(container: str) -> tuple[bytes, dict[str, Any]]:
    completed = _subprocess_raw([
        DOCKER, "inspect", "--format", "{{json .}}", container,
    ])
    common.require(completed.returncode == 0 and completed.stderr == b"",
                   "Docker inspect success:" + container)
    try:
        value = json.loads(completed.stdout.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise common.Reject("Docker inspect JSON:" + container) from error
    common.require(type(value) is dict, "Docker inspect object:" + container)
    return completed.stdout, value


def _write_raw(path: Path, raw: bytes) -> common.Capture:
    common.write_exclusive(path, raw, 0o444)
    return common.capture(path)


def _artifact(cap: common.Capture) -> dict[str, Any]:
    return {"path": cap.relpath, "sha256": cap.sha256, "size": cap.size}


def _container_name(root: Path, stage: str) -> str:
    prefix = hashlib.sha256(common.workspace_rel(root).encode("ascii")).hexdigest()[:10]
    safe = re.sub(r"[^A-Za-z0-9_.-]", "-", stage)
    return "cm2-c30a-v5-" + prefix + "-" + safe


def _docker_create_argv(
    root: Path,
    stage: str,
    inner_argv: list[str],
    *,
    working_directory: Path,
    extra_mounts: tuple[tuple[Path, Path, str], ...],
) -> tuple[str, list[str]]:
    container = _container_name(root, stage)
    time_path = root / "stages" / stage / "time.txt"
    mounts = [
        (Path("/usr"), Path("/usr"), "ro"),
        (Path("/lib"), Path("/lib"), "ro"),
        (Path("/lib64"), Path("/lib64"), "ro"),
        (Path("/etc/ld.so.cache"), Path("/etc/ld.so.cache"), "ro"),
        (common.WORKSPACE, common.WORKSPACE, "ro"),
        (root, root, "rw"),
        *extra_mounts,
    ]
    argv = [
        DOCKER, "create", "--name", container,
        "--network", "none",
        "--read-only",
        "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--ipc", "none",
        "--pids-limit", "1024",
        "--user", DOCKER_USER,
        "--workdir", os.fspath(working_directory),
        "--tmpfs", "/tmp:rw,nosuid,nodev,noexec,size=128m",
    ]
    for source, destination, mode in mounts:
        argv.extend(["--volume", f"{source}:{destination}:{mode}"])
    argv.extend([
        IMAGE_ID,
        TIME, "-v", "-o", os.fspath(time_path), "--",
        *inner_argv,
    ])
    return container, argv


def run_stage(
    root: Path,
    stage: str,
    inner_argv: list[str],
    *,
    working_directory: Path = common.WORKSPACE,
    extra_mounts: tuple[tuple[Path, Path, str], ...] = (),
) -> dict[str, Any]:
    common.require(common.SAFE_COMPONENT.fullmatch(stage) is not None,
                   "safe stage component")
    stage_dir = root / "stages" / stage
    stage_dir.mkdir(mode=0o755)
    started_wall_ns = time.time_ns()
    start = {
        "schema": "cm2.round306c30a.supplemental-stage-start.v5",
        "stage": stage,
        "wall_time_ns": started_wall_ns,
    }
    common.write_json(stage_dir / "start.json", start)
    start_cap = common.capture(stage_dir / "start.json")
    container, create_argv = _docker_create_argv(
        root,
        stage,
        inner_argv,
        working_directory=working_directory,
        extra_mounts=extra_mounts,
    )
    create = _subprocess_raw(create_argv)
    create_stdout = _write_raw(stage_dir / "docker_create.stdout.raw", create.stdout)
    create_stderr = _write_raw(stage_dir / "docker_create.stderr.raw", create.stderr)
    common.require(
        create.returncode == 0 and create.stderr == b""
        and bool(create.stdout.strip().decode("ascii", "strict")),
        "Docker create:" + stage,
    )
    pre_raw, pre = _inspect(container)
    pre_raw_cap = _write_raw(stage_dir / "docker_inspect_pre.raw.json", pre_raw)
    common.write_json(stage_dir / "docker_inspect_pre.json", pre)
    pre_cap = common.capture(stage_dir / "docker_inspect_pre.json")
    stdout_path = stage_dir / "stdout.raw"
    stderr_path = stage_dir / "stderr.raw"
    stdout_fd = os.open(
        stdout_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o444,
    )
    stderr_fd = os.open(
        stderr_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o444,
    )
    try:
        attached = subprocess.run(
            [DOCKER, "start", "--attach", container],
            stdin=subprocess.DEVNULL,
            stdout=stdout_fd,
            stderr=stderr_fd,
            check=False,
        )
    finally:
        os.close(stdout_fd)
        os.close(stderr_fd)
    post_raw, post = _inspect(container)
    post_raw_cap = _write_raw(stage_dir / "docker_inspect_post.raw.json", post_raw)
    common.write_json(stage_dir / "docker_inspect_post.json", post)
    post_cap = common.capture(stage_dir / "docker_inspect_post.json")
    stdout_cap = common.capture(stdout_path)
    stderr_cap = common.capture(stderr_path)
    time_cap = common.capture(stage_dir / "time.txt")
    state = post.get("State", {})
    signals = []
    if time_cap.raw is not None:
        try:
            timing_text = time_cap.raw.decode("utf-8", "strict")
            signals = common.TIME_SIGNAL.findall(timing_text)
        except UnicodeDecodeError:
            signals = ["NON_UTF8_TIME_REPORT"]
    attach_signal = -attached.returncode if attached.returncode < 0 else None
    signal_value: int | str | None = (
        attach_signal if attach_signal is not None
        else signals[0] if signals else None
    )
    ended_wall_ns = time.time_ns()
    passed = (
        attached.returncode == 0
        and state.get("ExitCode") == 0
        and state.get("OOMKilled") is False
        and state.get("Error") == ""
        and signal_value is None
    )
    receipt_body = {
        "schema": "cm2.round306c30a.supplemental-timed-process-exit.v5",
        "status": (
            "PASS_SAME_INVOCATION_ZERO_EXIT_NO_SIGNAL"
            if passed else "FAIL_CLOSED_SAME_INVOCATION_PROCESS"
        ),
        "stage": stage,
        "working_directory": os.fspath(working_directory),
        "started_wall_time_ns": started_wall_ns,
        "ended_wall_time_ns": ended_wall_ns,
        "attach_returncode": attached.returncode,
        "container_exit_code": state.get("ExitCode"),
        "signal": signal_value,
        "oom_killed": state.get("OOMKilled"),
        "docker_error": state.get("Error"),
        "docker_user": DOCKER_USER,
        "image_id": IMAGE_ID,
        "container_id": pre.get("Id"),
        "container_name": container,
        "inner_argv": inner_argv,
        "docker_create_argv": create_argv,
        "start": _artifact(start_cap),
        "stdout": _artifact(stdout_cap),
        "stderr": _artifact(stderr_cap),
        "time": _artifact(time_cap),
        "docker_create_stdout": _artifact(create_stdout),
        "docker_create_stderr": _artifact(create_stderr),
        "docker_inspect_pre": _artifact(pre_cap),
        "docker_inspect_post": _artifact(post_cap),
        "docker_inspect_pre_raw": _artifact(pre_raw_cap),
        "docker_inspect_post_raw": _artifact(post_raw_cap),
    }
    receipt = common.close_object(receipt_body)
    common.write_json(stage_dir / "exit.json", receipt)
    removed = _subprocess_raw([DOCKER, "rm", container])
    common.require(removed.returncode == 0, "Docker temporary cleanup:" + stage)
    common.require(passed, "stage failed closed:" + stage)
    return common.validate_stage(root, stage)


def parallel_stages(calls: list[tuple[Any, ...]]) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as executor:
        futures = [executor.submit(run_stage, *call) for call in calls]
        for future in futures:
            future.result()


def _checker_argv(root: Path, mode: str, *extra: str) -> list[str]:
    return env_i(BASE_ENV, [
        os.fspath(common.LOCKED_PYTHON), "-I", "-B",
        os.fspath(RELEASE_CHECKER), mode,
        "--run-root", common.workspace_rel(root),
        *extra,
    ])


def _sha(path: Path) -> str:
    return common.capture(path, retain=False).sha256


def _rename_noreplace(source: Path, destination: Path) -> None:
    common.require(source.exists() and not source.is_symlink(), "publish source")
    common.require(not destination.exists() and not destination.is_symlink(),
                   "publish destination absent")
    common.require(source.parent.stat().st_dev == destination.parent.stat().st_dev,
                   "publish same filesystem")
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameat2", None)
    common.require(function is not None, "renameat2 available")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p,
                         ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    result = function(
        -100, os.fsencode(source), -100, os.fsencode(destination), 1
    )
    if result != 0:
        code = ctypes.get_errno()
        raise common.Reject(
            "renameat2 noreplace:" + os.strerror(code)
        )
    common.require(destination.exists() and not source.exists(),
                   "published destination identity")


def _publish_all(root: Path) -> dict[str, str]:
    publication = root / "publication"
    pairs = (
        (publication / checker.OFFICIAL_SEALED.name, checker.OFFICIAL_SEALED),
        (publication / checker.OFFICIAL_PAYLOAD.name, checker.OFFICIAL_PAYLOAD),
        (publication / checker.OFFICIAL_COLD.name, checker.OFFICIAL_COLD),
        (publication / checker.OFFICIAL_OUTER.name, checker.OFFICIAL_OUTER),
        (publication / checker.OFFICIAL_ROOT.name, checker.OFFICIAL_ROOT),
        (publication / checker.OFFICIAL_TERMINAL.name, checker.OFFICIAL_TERMINAL),
    )
    for source, destination in pairs:
        common.require(source.exists() and not source.is_symlink(),
                       "all staged publication inputs present")
        common.require(not destination.exists() and not destination.is_symlink(),
                       "all official publication targets absent")
    for source, destination in pairs:
        _rename_noreplace(source, destination)
    return {
        "payload_manifest_sha256": _sha(checker.OFFICIAL_PAYLOAD),
        "cold_replay_receipt_sha256": _sha(checker.OFFICIAL_COLD),
        "outer_verification_sha256": _sha(checker.OFFICIAL_OUTER),
        "root_manifest_sha256": _sha(checker.OFFICIAL_ROOT),
        "terminal_receipt_sha256": _sha(checker.OFFICIAL_TERMINAL),
        "sealed_tree_sha256": checker._sealed_tree_record()["sha256"],
    }


def execute(root: Path) -> dict[str, Any]:
    manifest_name = Path(common.BASE_MANIFEST_REL).name
    precheck = ["/usr/bin/sha256sum", "-c", manifest_name]
    run_stage(
        root, "00_base_precheck", precheck,
        working_directory=common.DELIVERABLES,
    )
    run_stage(root, "10_preflight", _checker_argv(root, "preflight"))
    runtime_mount = ((root / "runtime", RUNTIME_ALIAS, "rw"),)
    run_stage(
        root,
        "20_runtime_rebuild",
        env_i(
            {"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
            ["/usr/bin/python3.12", "-I", "-B", os.fspath(REBUILD)],
        ),
        extra_mounts=runtime_mount,
    )
    fresh_python = RUNTIME_ALIAS / "fresh-python-flint-0.9.0/bin/python"
    run_stage(
        root,
        "21_runtime_recheck",
        env_i(
            {"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"},
            [os.fspath(fresh_python), "-I", "-B", os.fspath(ATTESTOR)],
        ),
        extra_mounts=runtime_mount,
    )

    producer_calls: list[tuple[Any, ...]] = []
    for seed in common.SEEDS:
        stage = traces.PRODUCER_STAGES[seed]
        trace_path = root / "stages" / stage / "trace.raw"
        candidate = traces.candidate_dir(root, seed)
        provenance = traces.provenance_path(root, seed)
        pycache = root / "pycache" / ("seed" + seed)
        environment = {
            **BASE_ENV,
            "PYTHONHASHSEED": seed,
            "PYTHONPYCACHEPREFIX": os.fspath(pycache),
        }
        command = [
            STRACE, "-qq", "-f", "-yy", "-s", "4096",
            "-e", "trace=all", "-o", os.fspath(trace_path),
            *env_i(environment, [
                os.fspath(common.LOCKED_PYTHON), "-P", "-s", "-B",
                os.fspath(LAUNCHER),
                "--expected-hash-seed", seed,
                "--expected-pycache-prefix", os.fspath(pycache),
                "--candidate-dir", os.fspath(candidate),
                "--provenance", os.fspath(provenance),
            ]),
        ]
        producer_calls.append((root, stage, command))
    parallel_stages(producer_calls)

    run_stage(
        root,
        "50_comparator",
        env_i(BASE_ENV, [
            os.fspath(common.LOCKED_PYTHON), "-I", "-B",
            os.fspath(COMPARATOR), "--run-root", common.workspace_rel(root),
        ]),
    )

    for seed in common.SEEDS:
        run_stage(
            root, "55_verifier_manifest_pre_seed" + seed, precheck,
            working_directory=common.DELIVERABLES,
        )

    verifier_calls: list[tuple[Any, ...]] = []
    for seed in common.SEEDS:
        stage = traces.VERIFIER_STAGES[seed]
        trace_path = root / "stages" / stage / "trace.raw"
        command = [
            STRACE, "-qq", "-f", "-yy", "-s", "4096",
            "-e", "trace=all", "-o", os.fspath(trace_path),
            *env_i(BASE_ENV, [
                os.fspath(common.LOCKED_PYTHON), "-I", "-B",
                os.fspath(VERIFIER),
                "--candidate-dir", os.fspath(traces.candidate_dir(root, seed)),
            ]),
        ]
        verifier_calls.append((root, stage, command))
    parallel_stages(verifier_calls)

    for seed in common.SEEDS:
        run_stage(
            root, "65_verifier_manifest_post_seed" + seed, precheck,
            working_directory=common.DELIVERABLES,
        )

    attacks = root / "attacks"
    run_stage(
        root,
        "70_attacks",
        env_i(BASE_ENV, [
            os.fspath(common.LOCKED_PYTHON), "-I", "-B",
            os.fspath(ATTACK_HARNESS),
            "--candidate-dir", os.fspath(traces.candidate_dir(root, common.SEEDS[0])),
            "--evidence-dir", os.fspath(attacks),
        ]),
    )
    run_stage(
        root,
        "80_trace_audit",
        env_i(BASE_ENV, [
            os.fspath(common.LOCKED_PYTHON), "-I", "-B",
            os.fspath(TRACE_AUDITOR), "--run-root", common.workspace_rel(root),
        ]),
    )
    run_stage(
        root, "90_base_postcheck", precheck,
        working_directory=common.DELIVERABLES,
    )

    run_stage(root, "95_assemble_payload", _checker_argv(root, "assemble"))
    publication = root / "publication"
    payload_sha = _sha(publication / checker.OFFICIAL_PAYLOAD.name)
    run_stage(
        root, "96_mint_cold",
        _checker_argv(
            root, "mint-cold", "--expected-payload-sha256", payload_sha,
        ),
    )
    cold_sha = _sha(publication / checker.OFFICIAL_COLD.name)
    run_stage(
        root, "97_mint_outer",
        _checker_argv(
            root, "mint-outer", "--expected-payload-sha256", payload_sha,
            "--expected-cold-sha256", cold_sha,
        ),
    )
    run_stage(
        root, "98_build_root",
        _checker_argv(
            root, "build-root", "--expected-payload-sha256", payload_sha,
            "--expected-cold-sha256", cold_sha,
        ),
    )
    root_sha = _sha(publication / checker.OFFICIAL_ROOT.name)
    run_stage(
        root, "99_mint_terminal",
        _checker_argv(
            root, "mint-terminal", "--expected-payload-sha256", payload_sha,
            "--expected-cold-sha256", cold_sha,
            "--expected-root-sha256", root_sha,
        ),
    )
    terminal_sha = _sha(publication / checker.OFFICIAL_TERMINAL.name)
    published = _publish_all(root)
    common.require(
        published["payload_manifest_sha256"] == payload_sha
        and published["cold_replay_receipt_sha256"] == cold_sha
        and published["root_manifest_sha256"] == root_sha
        and published["terminal_receipt_sha256"] == terminal_sha,
        "staging/published byte identity",
    )
    run_stage(
        root, "100_terminal_replay",
        _checker_argv(
            root, "check-terminal", "--expected-payload-sha256", payload_sha,
            "--expected-cold-sha256", cold_sha,
            "--expected-root-sha256", root_sha,
            "--expected-terminal-sha256", terminal_sha,
        ),
    )
    replay = common.validate_stage(root, "100_terminal_replay")
    common.require(replay["stdout"].raw is not None, "terminal replay stdout")
    replay_object = common.strict_json(replay["stdout"].raw, "terminal replay")
    common.validate_closed(replay_object, "terminal replay")
    common.require(
        replay_object.get("status")
        == "PASS_FULL_FIVE_LAYER_TERMINAL_REPLAY__252_TO_92_ONLY",
        "terminal replay final PASS",
    )
    pipeline_receipt = checker.build_pipeline_receipt(
        root, payload_sha, cold_sha, root_sha, terminal_sha
    )
    pipeline_receipt_path = root / checker.PIPELINE_RECEIPT_NAME
    common.write_json(pipeline_receipt_path, pipeline_receipt)
    pipeline_receipt_sha = _sha(pipeline_receipt_path)
    run_stage(
        root, checker.FINAL_COMMIT_STAGE,
        _checker_argv(
            root, "mint-final-commit",
            "--expected-payload-sha256", payload_sha,
            "--expected-cold-sha256", cold_sha,
            "--expected-root-sha256", root_sha,
            "--expected-terminal-sha256", terminal_sha,
            "--expected-pipeline-receipt-sha256", pipeline_receipt_sha,
        ),
    )
    final_stage = common.validate_stage(root, checker.FINAL_COMMIT_STAGE)
    staged_commit = publication / checker.OFFICIAL_COMMIT.name
    staged_commit_cap = common.capture(staged_commit)
    common.require(
        staged_commit_cap.raw is not None
        and final_stage["stdout"].raw == staged_commit_cap.raw
        and final_stage["stderr"].size == 0,
        "final commit same-invocation bytes",
    )
    final_commit = common.strict_json(staged_commit_cap.raw, "final commit")
    common.validate_closed(final_commit, "final commit")
    common.require(
        final_commit.get("status")
        == "PASS_FINAL_COMMIT_AFTER_POST_PUBLICATION_REPLAY__ZERO_ADDITIONAL_CREDIT"
        and final_commit.get("pipeline_precommit_receipt_sha256")
        == pipeline_receipt_sha,
        "final commit semantics",
    )
    _rename_noreplace(staged_commit, checker.OFFICIAL_COMMIT)
    official_commit_sha = _sha(checker.OFFICIAL_COMMIT)
    common.require(
        official_commit_sha == staged_commit_cap.sha256,
        "final commit O_EXCL publication identity",
    )
    published["final_commit_receipt_sha256"] = official_commit_sha
    return common.close_object({
        "schema": "cm2.round306c30a.supplemental-p0b-pipeline.v5",
        "status": (
            "PASS_FRESH_V5_FIVE_LAYER_CLOSURE_AND_FINAL_COMMIT__"
            "252_TO_92_ONLY"
        ),
        "run_root": common.workspace_rel(root),
        **published,
        "terminal_replay_payload_sha256": replay_object["payload_sha256"],
        "pipeline_precommit_receipt_sha256": pipeline_receipt_sha,
        "conclusion": common.fixed_conclusion(),
    })


def initialize(name: str) -> Path:
    common.require(common.RUN_NAME.fullmatch(name) is not None, "run name policy")
    root = common.AUDIT / name
    root.mkdir(mode=0o755)
    for child in (
        "stages", "runtime", "candidates", "provenance", "pycache", "publication"
    ):
        (root / child).mkdir(mode=0o755)
    image = _subprocess_raw([DOCKER, "image", "inspect", "--format", "{{.Id}}",
                             IMAGE_REFERENCE])
    common.require(
        image.returncode == 0
        and image.stderr == b""
        and image.stdout.decode("ascii", "strict").strip() == IMAGE_ID,
        "locally installed Docker image digest pin",
    )
    descriptor = common.close_object({
        "schema": "cm2.round306c30a.supplemental-p0b-run.v5",
        "status": "INITIALIZED_ZERO_AUTHORITY",
        "run_root": common.workspace_rel(root),
        "docker": {
            "binary": DOCKER,
            "image_reference": IMAGE_REFERENCE,
            "image_id": IMAGE_ID,
            "network": "none",
            "read_only_rootfs": True,
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges"],
            "ipc": "none",
            "user": DOCKER_USER,
        },
        "prohibited_inputs": [
            "ANY_C30A_SUPPLEMENTAL_V4_BUNDLE",
            "DERIVED_OR_RETROSPECTIVE_RAW_STDERR_OR_EXIT",
            "POSTPROCESSED_COMPARATOR_STDOUT",
        ],
        "conclusion": common.fixed_conclusion(),
    })
    common.write_json(root / "run_descriptor.json", descriptor)
    return root


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--run-name", required=True)
    return value


def main() -> int:
    try:
        root = initialize(parser().parse_args().run_name)
        result = execute(root)
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_V5_PIPELINE_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    sys.stdout.buffer.write(common.canonical(result) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
