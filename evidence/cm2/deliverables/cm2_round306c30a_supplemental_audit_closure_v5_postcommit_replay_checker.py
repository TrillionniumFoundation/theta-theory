#!/usr/bin/env python3
"""Additive post-publication semantic replay and final-commit-v2 checker.

The original v5 preflight correctly required all official publication targets
to be absent at stage 10.  That historical fact cannot also be required after
publication.  This checker validates the retained stage-10 bytes as the
historical freshness witness, requires the official targets to exist now, and
then independently recomputes the complete core and stages 95--101.

It never modifies the original v5 payload, six publication targets, or first
final commit.  Two separate Docker-network-none invocations must emit the same
post-publication replay bytes before an additive manifest and final-commit-v2
can be minted.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Any, Iterable

_BOOTSTRAP = os.path.dirname(os.path.abspath(__file__))
if _BOOTSTRAP not in sys.path:
    sys.path.insert(0, _BOOTSTRAP)

import cm2_round306c30a_supplemental_audit_closure_v5_common as common
import cm2_round306c30a_supplemental_audit_closure_v5_release_checker as release
import cm2_round306c30a_supplemental_audit_closure_v5_trace_lib as traces


sys.dont_write_bytecode = True

PREFIX = "cm2_round306c30a_supplemental_audit_closure"
SCRIPT = common.DELIVERABLES / (PREFIX + "_v5_postcommit_replay_checker.py")
ADDENDUM = common.DELIVERABLES / (PREFIX + "_v5_postcommit_addendum.md")
OFFICIAL_REPLAY = common.DELIVERABLES / (PREFIX + "_postcommit_replay_receipt.json")
OFFICIAL_MANIFEST = common.DELIVERABLES / (PREFIX + "_postcommit_replay_manifest.sha256")
OFFICIAL_COMMIT_V2 = common.DELIVERABLES / (PREFIX + "_final_commit_v2_receipt.json")
STAGED_REPLAY_NAMES = {
    PREFIX + "_postcommit_replay_a.json",
    PREFIX + "_postcommit_replay_b.json",
}
STAGED_MANIFEST_NAME = PREFIX + "_postcommit_replay_manifest.sha256"
STAGED_COMMIT_V2_NAME = PREFIX + "_final_commit_v2_receipt.json"
REPLAY_STAGES = ("110_postcommit_replay_a", "111_postcommit_replay_b")
MANIFEST_STAGE = "112_postcommit_manifest"
COMMIT_V2_STAGE = "113_final_commit_v2"


def _publication(root: Path) -> Path:
    path = root / "publication"
    status = path.lstat()
    common.require(
        stat.S_ISDIR(status.st_mode) and not path.is_symlink(),
        "postcommit publication staging directory",
    )
    return path


def _json_stage(root: Path, name: str, label: str) -> tuple[dict[str, Any], dict[str, Any]]:
    stage = common.validate_stage(root, name)
    common.require(
        stage["stdout"].raw is not None and stage["stderr"].size == 0,
        "postcommit stage raw streams:" + label,
    )
    return stage, common.strict_json(stage["stdout"].raw, label)


def _historical_preflight(root: Path) -> dict[str, Any]:
    """Validate stage-10 absence as retained history, not present-day state."""

    stage, reported = _json_stage(root, "10_preflight", "historical v5 preflight")
    common.validate_closed(reported, "historical v5 preflight")
    body = dict(reported)
    digest = body.pop("payload_sha256", None)
    expected = {
        "schema": "cm2.round306c30a.supplemental-preflight.v5",
        "status": "READY_FOR_FRESH_P0B_V5_CHAIN__ZERO_AUTHORITY",
        "run_root": common.workspace_rel(root),
        "base_manifest_sha256": common.BASE_MANIFEST_SHA256,
        "static_tools": release._static_table(),
        "prohibited_evidence": {
            "v4_bundle_authority": "PERMANENTLY_DISABLED",
            "retrospective_raw_stream_derivation": "FORBIDDEN",
        },
        "conclusion": common.fixed_conclusion(),
    }
    expected_inner_argv = [
        "/usr/bin/env", "-i",
        "HOME=/nonexistent",
        "LANG=C.UTF-8",
        "LC_ALL=C.UTF-8",
        "PATH=/usr/bin:/bin",
        "TZ=UTC",
        os.fspath(common.LOCKED_PYTHON), "-I", "-B",
        os.fspath(
            common.DELIVERABLES
            / (PREFIX + "_v5_release_checker.py")
        ),
        "preflight", "--run-root", common.workspace_rel(root),
    ]
    expected_container_cmd = [
        "/usr/bin/time", "-v", "-o",
        os.fspath(root / "stages/10_preflight/time.txt"),
        "--", *expected_inner_argv,
    ]
    _, inspect_pre = common.json_capture(
        root / "stages/10_preflight/docker_inspect_pre.json",
        "historical preflight Docker inspect pre",
    )
    _, inspect_post = common.json_capture(
        root / "stages/10_preflight/docker_inspect_post.json",
        "historical preflight Docker inspect post",
    )
    for inspected in (inspect_pre, inspect_post):
        config = inspected.get("Config", {})
        common.require(
            config.get("Cmd") == expected_container_cmd
            and config.get("WorkingDir") == os.fspath(common.WORKSPACE)
            and inspected.get("Path") == "/usr/bin/time"
            and inspected.get("Args") == expected_container_cmd[1:],
            "historical preflight exact inspected command",
        )
    common.require(
        body == expected
        and digest == common.sha256(common.canonical(body))
        and stage["receipt"].get("inner_argv") == expected_inner_argv
        and stage["receipt"].get("working_directory")
        == os.fspath(common.WORKSPACE)
        and stage["receipt"]["ended_wall_time_ns"]
        < common.validate_stage(root, "20_runtime_rebuild")["receipt"]["started_wall_time_ns"],
        "historical stage10 freshness/static identity",
    )
    return reported


def _core_replay(root: Path) -> dict[str, Any]:
    common.validate_base_manifest()
    release._validate_precheck(root, "00_base_precheck")
    preflight = _historical_preflight(root)
    release._validate_runtime(root)
    for seed in common.SEEDS:
        common.validate_stage(root, traces.PRODUCER_STAGES[seed])
        traces.exact_candidate(root, seed)
    release._validate_comparator(root)
    trace = release._validate_trace_audit(root)
    release._validate_precheck(root, "90_base_postcheck")
    release._phase_order(root, release.CORE_GROUPS)
    common.require(
        trace.get("status")
        == (
            "PASS_FOUR_FULL_TRACES_RECOMPUTED__TEN_ATTACKS_REJECTED__"
            "KERNEL_NETWORK_NONE"
        )
        and trace.get("conclusion") == common.fixed_conclusion(),
        "postpublication full core semantic replay",
    )
    return {"preflight": preflight, "trace": trace}


def _expected_mint_outputs(
    root: Path, payload: common.Capture, cold: common.Capture,
    outer: common.Capture, root_manifest: common.Capture,
    terminal: common.Capture,
) -> dict[str, dict[str, Any]]:
    publication = root / "publication"
    payload_rows = common.parse_manifest(payload.raw or b"", "official payload")
    return {
        "95_assemble_payload": {
            "schema": "cm2.round306c30a.supplemental-assembly-result.v5",
            "status": "PASS_STAGED_SEALED_EVIDENCE_AND_PAYLOAD__NOT_YET_AUTHORITY",
            "sealed_staging": common.workspace_rel(publication / release.OFFICIAL_SEALED.name),
            "payload_staging": common.workspace_rel(publication / release.OFFICIAL_PAYLOAD.name),
            "payload_manifest_sha256": payload.sha256,
            "payload_member_count": len(payload_rows),
            "conclusion": common.fixed_conclusion(),
        },
        "96_mint_cold": {
            "status": "COLD_RECEIPT_STAGED__NOT_YET_AUTHORITY",
            "sha256": cold.sha256,
        },
        "97_mint_outer": {
            "status": "OUTER_VERIFICATION_STAGED__NOT_YET_AUTHORITY",
            "sha256": outer.sha256,
        },
        "98_build_root": {
            "status": "ROOT_MANIFEST_STAGED__NOT_YET_AUTHORITY",
            "sha256": root_manifest.sha256,
        },
    }


def _base_stage_names() -> list[str]:
    return [
        *(name for group in release.CORE_GROUPS for name in group),
        *release.MINT_STAGES,
        release.FINAL_COMMIT_STAGE,
    ]


def _stage_artifacts(stage: dict[str, Any]) -> dict[str, Any]:
    captures = {
        "exit": stage["receipt_capture"],
        "start": stage["start_capture"],
        "stdout": stage["stdout"],
        "stderr": stage["stderr"],
        "time": stage["time"],
        "docker_inspect_pre": stage["inspect_pre"],
        "docker_inspect_post": stage["inspect_post"],
        "docker_inspect_pre_raw": stage["inspect_pre_raw"],
        "docker_inspect_post_raw": stage["inspect_post_raw"],
        "docker_create_stdout": stage["create_stdout"],
        "docker_create_stderr": stage["create_stderr"],
    }
    return {
        key: {"sha256": cap.sha256, "size": cap.size}
        for key, cap in sorted(captures.items())
    }


def _validate_complete_chain(
    root: Path, *, allowed_extra_stages: Iterable[str] = (),
) -> dict[str, Any]:
    core = _core_replay(root)
    payload = common.capture(release.OFFICIAL_PAYLOAD)
    cold = common.capture(release.OFFICIAL_COLD)
    outer = common.capture(release.OFFICIAL_OUTER)
    root_manifest = common.capture(release.OFFICIAL_ROOT)
    terminal = common.capture(release.OFFICIAL_TERMINAL)
    original_commit = common.capture(release.OFFICIAL_COMMIT)
    common.require(
        all(cap.raw is not None for cap in (
            payload, cold, outer, root_manifest, terminal, original_commit
        )),
        "retained official publication bytes",
    )
    release.validate_payload(payload.sha256)
    replay = release.check_terminal(
        root, payload.sha256, cold.sha256, root_manifest.sha256, terminal.sha256
    )
    expected_outputs = _expected_mint_outputs(
        root, payload, cold, outer, root_manifest, terminal
    )
    stage_records: dict[str, Any] = {}
    for name, expected in expected_outputs.items():
        stage, value = _json_stage(root, name, "postcommit " + name)
        common.require(value == expected, "mint stage exact output:" + name)
        stage_records[name] = {
            "exit_sha256": stage["receipt_capture"].sha256,
            "stdout_sha256": stage["stdout"].sha256,
        }
    stage99, value99 = _json_stage(root, "99_mint_terminal", "postcommit terminal mint")
    common.validate_closed(value99, "postcommit terminal mint")
    common.require(
        stage99["stdout"].raw == terminal.raw,
        "stage99/official terminal byte identity",
    )
    stage100, value100 = _json_stage(root, "100_terminal_replay", "postcommit stage100")
    common.validate_closed(value100, "postcommit stage100")
    common.require(value100 == replay, "stage100 exact semantic replay")
    receipt_cap, pipeline_receipt = release._closed_file(
        root / release.PIPELINE_RECEIPT_NAME, "pipeline precommit receipt"
    )
    recomputed_pipeline = release.build_pipeline_receipt(
        root, payload.sha256, cold.sha256, root_manifest.sha256, terminal.sha256
    )
    common.require(
        pipeline_receipt == recomputed_pipeline,
        "pipeline receipt postpublication recomputation",
    )
    commit = common.strict_json(original_commit.raw or b"", "original final commit")
    common.validate_closed(commit, "original final commit")
    stage101, value101 = _json_stage(root, release.FINAL_COMMIT_STAGE, "original commit stage")
    common.validate_closed(value101, "original commit stage")
    common.require(
        value101 == commit
        and stage101["stdout"].raw == original_commit.raw
        and commit.get("status")
        == "PASS_FINAL_COMMIT_AFTER_POST_PUBLICATION_REPLAY__ZERO_ADDITIONAL_CREDIT"
        and commit.get("pipeline_precommit_receipt_sha256") == receipt_cap.sha256
        and commit.get("pipeline_precommit_receipt") == pipeline_receipt
        and commit.get("official_targets") == release._official_target_table()
        and commit.get("conclusion") == common.fixed_conclusion(),
        "original commit exact closure",
    )
    release._phase_order(
        root,
        release.CORE_GROUPS
        + tuple((name,) for name in release.MINT_STAGES)
        + ((release.FINAL_COMMIT_STAGE,),),
    )
    base_names = _base_stage_names()
    allowed = set(allowed_extra_stages)
    actual = {path.name for path in (root / "stages").iterdir() if path.is_dir()}
    common.require(
        actual == set(base_names) | allowed,
        "postcommit exact stage census",
    )
    base_stage_table: dict[str, Any] = {}
    for name in base_names:
        stage = common.validate_stage(root, name)
        base_stage_table[name] = {
            "exit_sha256": stage["receipt_capture"].sha256,
            "stdout_sha256": stage["stdout"].sha256,
            "stderr_sha256": stage["stderr"].sha256,
            "time_sha256": stage["time"].sha256,
        }
    return {
        "core_trace_audit_payload_sha256": core["trace"]["payload_sha256"],
        "historical_preflight_payload_sha256": core["preflight"]["payload_sha256"],
        "base_stages": base_stage_table,
        "official_targets": release._official_target_table(),
        "payload_manifest_sha256": payload.sha256,
        "cold_replay_receipt_sha256": cold.sha256,
        "outer_verification_sha256": outer.sha256,
        "root_manifest_sha256": root_manifest.sha256,
        "terminal_receipt_sha256": terminal.sha256,
        "original_final_commit_sha256": original_commit.sha256,
        "pipeline_precommit_receipt_sha256": receipt_cap.sha256,
        "stage99_exit_sha256": stage99["receipt_capture"].sha256,
        "stage100_exit_sha256": stage100["receipt_capture"].sha256,
        "stage101_exit_sha256": stage101["receipt_capture"].sha256,
    }


def build_replay(root: Path, *, allowed_extra_stages: Iterable[str] = ()) -> dict[str, Any]:
    chain = _validate_complete_chain(root, allowed_extra_stages=allowed_extra_stages)
    script = common.capture(SCRIPT, retain=False)
    addendum = common.capture(ADDENDUM, retain=False)
    return common.close_object({
        "schema": "cm2.round306c30a.supplemental-postpublication-semantic-replay.v1",
        "status": (
            "PASS_POSTPUBLICATION_FULL_CORE_AND_STAGE95_TO_101_REPLAY__"
            "ZERO_ADDITIONAL_CREDIT"
        ),
        "run_root": common.workspace_rel(root),
        "historical_stage10_fact": "OFFICIAL_TARGETS_ABSENT_AT_RETAINED_PREFLIGHT",
        "present_day_fact": "SIX_OFFICIAL_TARGETS_AND_ORIGINAL_COMMIT_EXIST_AND_MATCH",
        "checker_sha256": script.sha256,
        "addendum_sha256": addendum.sha256,
        **chain,
        "conclusion": common.fixed_conclusion(),
    })


def _manifest_sources(root: Path) -> dict[str, Path]:
    sources: dict[str, Path] = {
        common.workspace_rel(SCRIPT): SCRIPT,
        common.workspace_rel(ADDENDUM): ADDENDUM,
        common.workspace_rel(OFFICIAL_REPLAY): OFFICIAL_REPLAY,
        common.workspace_rel(release.OFFICIAL_PAYLOAD): release.OFFICIAL_PAYLOAD,
        common.workspace_rel(release.OFFICIAL_COLD): release.OFFICIAL_COLD,
        common.workspace_rel(release.OFFICIAL_OUTER): release.OFFICIAL_OUTER,
        common.workspace_rel(release.OFFICIAL_ROOT): release.OFFICIAL_ROOT,
        common.workspace_rel(release.OFFICIAL_TERMINAL): release.OFFICIAL_TERMINAL,
        common.workspace_rel(release.OFFICIAL_COMMIT): release.OFFICIAL_COMMIT,
        common.workspace_rel(root / release.PIPELINE_RECEIPT_NAME):
            root / release.PIPELINE_RECEIPT_NAME,
    }
    for stage_name in REPLAY_STAGES:
        stage_root = root / "stages" / stage_name
        status = stage_root.lstat()
        common.require(
            stat.S_ISDIR(status.st_mode) and not stage_root.is_symlink(),
            "replay stage evidence directory",
        )
        for entry in os.scandir(stage_root):
            common.require(
                entry.is_file(follow_symlinks=False) and not entry.is_symlink(),
                "replay stage exact regular evidence",
            )
            path = stage_root / entry.name
            sources[common.workspace_rel(path)] = path
    return sources


def build_manifest(root: Path, expected_replay_sha256: str) -> dict[str, Any]:
    common.require(
        common.HEX64.fullmatch(expected_replay_sha256) is not None,
        "external replay receipt pin",
    )
    replay_cap, replay = release._closed_file(OFFICIAL_REPLAY, "official replay")
    common.require(
        replay_cap.sha256 == expected_replay_sha256
        and replay == build_replay(
            root, allowed_extra_stages=(*REPLAY_STAGES, MANIFEST_STAGE)
        ),
        "two-replay official semantic receipt",
    )
    for stage_name in REPLAY_STAGES:
        stage = common.validate_stage(root, stage_name)
        common.require(
            stage["stdout"].raw == replay_cap.raw and stage["stderr"].size == 0,
            "double replay byte identity:" + stage_name,
        )
    release._phase_order(
        root,
        release.CORE_GROUPS
        + tuple((name,) for name in release.MINT_STAGES)
        + ((release.FINAL_COMMIT_STAGE,),)
        + tuple((name,) for name in REPLAY_STAGES),
    )
    sources = _manifest_sources(root)
    rows = {
        name: common.capture(path, retain=False).sha256
        for name, path in sources.items()
    }
    raw = b"".join(
        rows[name].encode("ascii") + b"  " + name.encode("ascii") + b"\n"
        for name in sorted(rows, key=os.fsencode)
    )
    output = _publication(root) / STAGED_MANIFEST_NAME
    common.write_exclusive(output, raw)
    return common.close_object({
        "schema": "cm2.round306c30a.supplemental-postcommit-manifest-mint.v1",
        "status": "PASS_DOUBLE_REPLAY_MANIFEST_STAGED__NOT_YET_V2_AUTHORITY",
        "manifest_sha256": common.sha256(raw),
        "member_count": len(rows),
        "replay_receipt_sha256": replay_cap.sha256,
        "conclusion": common.fixed_conclusion(),
    })


def _validate_manifest(root: Path, expected_manifest_sha256: str) -> dict[str, str]:
    common.require(
        common.HEX64.fullmatch(expected_manifest_sha256) is not None,
        "external postcommit manifest pin",
    )
    cap = common.capture(OFFICIAL_MANIFEST)
    common.require(
        cap.raw is not None and cap.sha256 == expected_manifest_sha256,
        "official postcommit manifest external pin",
    )
    rows = common.parse_manifest(cap.raw, "postcommit replay manifest")
    sources = _manifest_sources(root)
    common.require(set(rows) == set(sources), "postcommit manifest exact map")
    for name, path in sources.items():
        common.require(
            common.capture(path, retain=False).sha256 == rows[name],
            "postcommit manifest member:" + name,
        )
    return rows


def build_commit_v2(
    root: Path, expected_replay_sha256: str, expected_manifest_sha256: str,
) -> dict[str, Any]:
    allowed = (*REPLAY_STAGES, MANIFEST_STAGE, COMMIT_V2_STAGE)
    replay_cap, replay = release._closed_file(OFFICIAL_REPLAY, "official replay")
    common.require(
        replay_cap.sha256 == expected_replay_sha256
        and replay == build_replay(root, allowed_extra_stages=allowed),
        "v2 replay semantic recomputation",
    )
    replay_stage_records: dict[str, Any] = {}
    for stage_name in REPLAY_STAGES:
        stage = common.validate_stage(root, stage_name)
        common.require(
            stage["stdout"].raw == replay_cap.raw and stage["stderr"].size == 0,
            "v2 double replay bytes:" + stage_name,
        )
        replay_stage_records[stage_name] = {
            "exit_sha256": stage["receipt_capture"].sha256,
            "artifacts": _stage_artifacts(stage),
        }
    rows = _validate_manifest(root, expected_manifest_sha256)
    manifest_stage, manifest_result = _json_stage(
        root, MANIFEST_STAGE, "postcommit manifest stage"
    )
    common.validate_closed(manifest_result, "postcommit manifest stage")
    common.require(
        manifest_result.get("status")
        == "PASS_DOUBLE_REPLAY_MANIFEST_STAGED__NOT_YET_V2_AUTHORITY"
        and manifest_result.get("manifest_sha256") == expected_manifest_sha256
        and manifest_result.get("member_count") == len(rows)
        and manifest_result.get("replay_receipt_sha256") == replay_cap.sha256,
        "postcommit manifest stage exact result",
    )
    release._phase_order(
        root,
        release.CORE_GROUPS
        + tuple((name,) for name in release.MINT_STAGES)
        + ((release.FINAL_COMMIT_STAGE,),)
        + tuple((name,) for name in REPLAY_STAGES)
        + ((MANIFEST_STAGE,),),
    )
    script = common.capture(SCRIPT, retain=False)
    addendum = common.capture(ADDENDUM, retain=False)
    original_commit = common.capture(release.OFFICIAL_COMMIT, retain=False)
    return common.close_object({
        "schema": "cm2.round306c30a.supplemental-final-commit-v2.v1",
        "status": (
            "PASS_ADDITIVE_FINAL_COMMIT_V2_AFTER_DOUBLE_POSTPUBLICATION_REPLAY__"
            "ZERO_ADDITIONAL_CREDIT"
        ),
        "run_root": common.workspace_rel(root),
        "checker_sha256": script.sha256,
        "addendum_sha256": addendum.sha256,
        "postcommit_replay_receipt_sha256": replay_cap.sha256,
        "postcommit_manifest_sha256": expected_manifest_sha256,
        "postcommit_manifest_member_count": len(rows),
        "original_final_commit_sha256": original_commit.sha256,
        "original_commit_authority": "SUPERSEDED_BY_THIS_ADDITIVE_V2_COMMIT",
        "double_replay_stages": replay_stage_records,
        "manifest_stage_exit_sha256": manifest_stage["receipt_capture"].sha256,
        "official_targets": release._official_target_table(),
        "conclusion": common.fixed_conclusion(),
    })


def _write_output(root: Path, name: str, value: dict[str, Any]) -> None:
    common.require(
        name in STAGED_REPLAY_NAMES | {STAGED_COMMIT_V2_NAME},
        "known postcommit JSON output",
    )
    path = _publication(root) / name
    common.require(not path.exists() and not path.is_symlink(), "fresh postcommit output")
    common.write_json(path, value)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("mode", choices=("replay", "mint-manifest", "mint-v2"))
    value.add_argument("--run-root", required=True)
    value.add_argument("--output-name")
    value.add_argument("--expected-replay-sha256")
    value.add_argument("--expected-manifest-sha256")
    return value


def main() -> int:
    try:
        args = parser().parse_args()
        root = common.run_root(args.run_root)
        if args.mode == "replay":
            common.require(args.output_name in STAGED_REPLAY_NAMES, "replay output name")
            allowed = (
                (REPLAY_STAGES[0],)
                if args.output_name.endswith("_a.json")
                else REPLAY_STAGES
            )
            result = build_replay(root, allowed_extra_stages=allowed)
            _write_output(root, args.output_name, result)
        elif args.mode == "mint-manifest":
            common.require(args.output_name is None, "manifest has fixed output")
            result = build_manifest(root, args.expected_replay_sha256 or "")
        else:
            common.require(args.output_name == STAGED_COMMIT_V2_NAME, "v2 output name")
            result = build_commit_v2(
                root,
                args.expected_replay_sha256 or "",
                args.expected_manifest_sha256 or "",
            )
            _write_output(root, args.output_name, result)
    except Exception as error:
        print(
            "C30A_SUPPLEMENTAL_POSTCOMMIT_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    sys.stdout.buffer.write(common.canonical(result) + b"\n")
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
