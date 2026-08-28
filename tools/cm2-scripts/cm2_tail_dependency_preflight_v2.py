#!/usr/bin/env python3
"""CM2 tail dependency preflight v2 (read-only, zero-credit).

v2 preserves the v1 D02/D03/D04/Gate5 checks and adds the current v16r2
semantic-regeneration staging bundle.  It intentionally reports the expected
staging blockers (source-template checkers not run, 0/137 static attacks,
un-pinned contract/audit, and absent manifest/outer) as *passing observations*;
those observations mean the bundle is correctly fail-closed, not that it is
authorized.  Run with ``python3 -I -B``.  The only output is canonical JSON on
stdout and no file or runtime object is written.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
V1_REL = "scripts/cm2_tail_dependency_preflight_v1.py"
V1_SHA256 = "cad06b78813f1117425e62b71d0b1358b9bdb1e83bdd5bf745e00143d7ffa4ae"

BASE = "deliverables/cm2_round306c79g_true_global_no_producer_consumer"
V16R2_FILES = {
    "semantic_supersession": f"{BASE}_v16_semantic_rejection_supersession_receipt_v1.json",
    "schema": f"{BASE}_schema_v16r2.json",
    "contract": f"{BASE}_contract_v16r2.json",
    "producer": f"{BASE}_v16r2.py",
    "consumer": f"{BASE}_independent_verifier_assembler_authority_consumer_v16r2.py",
    "transition": f"{BASE}_v16_to_v16r2_static_launch_transition_receipt_v1.json",
    "static_audit": f"{BASE}_static_audit_v16r2.json",
}
V16R2_SHA256 = {
    "semantic_supersession": "4b05c7dcd7303311fed7b51ea878641e006e707b5fe413f2aefbc3146afddb3c",
    "schema": "903c27f627439abe7c3184f6b239df72e9a4fb3512d740020f504703d464ca07",
    "contract": "c2fe261645f14a9a02c5525a7351b5f9f34d04a7935ea5fb198d4ffccbf2bb6b",
    "producer": "07fbba12fa35270cfa046d2cb022afcf5007648f63b4aa5f918995b4478e2506",
    "consumer": "b33a214c735e802fdc6baaeb539d8fdc2a7d7fcb5b804f03bee554de6ff64bae",
    "transition": "f7960a12b0ba7db693ef1805daedeeb6d895dd859c1a937ba01d85c1cd56fe6d",
    "static_audit": "9be67d1cd9bc2f91c32d960ff0897d990b548d315407f7faae53f8531963cc90",
}
V16R2_MODE = {
    "semantic_supersession": "0444",
    "schema": "0664",
    "contract": "0664",
    "producer": "0664",
    "consumer": "0664",
    "transition": "0664",
    "static_audit": "0664",
}
V16R2_MANIFEST_REL = f"{BASE}_cold_launch_manifest_v16r2.sha256"
V16R2_OUTER_REL = f"{BASE}_cold_launch_outer_receipt_v16r2.json"


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_stable(path: Path) -> tuple[bytes, dict[str, Any]]:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise RuntimeError(f"not regular single-link: {path}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(fd, 1 << 20)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(fd)
        named = os.lstat(path)
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
        ) or (before.st_dev, before.st_ino) != (named.st_dev, named.st_ino):
            raise RuntimeError(f"identity drift: {path}")
        raw = b"".join(chunks)
        if len(raw) != before.st_size:
            raise RuntimeError(f"size drift: {path}")
        return raw, {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(raw),
            "mode_octal": format(stat.S_IMODE(before.st_mode), "04o"),
            "nlink": before.st_nlink,
            "bytes": len(raw),
        }
    finally:
        os.close(fd)


def json_doc(raw: bytes, rel: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            if key in out:
                raise ValueError(f"duplicate JSON key {key} in {rel}")
            out[key] = value
        return out

    def constant(value: str) -> None:
        raise ValueError(f"non-finite JSON constant {value} in {rel}")

    return json.loads(
        raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant
    )


def probe(root: Path, rel: str, expected: str | None = None) -> tuple[dict[str, Any], Any | None]:
    path = root / rel
    try:
        raw, meta = read_stable(path)
        if expected is not None:
            meta["expected_sha256"] = expected
            meta["sha256_match"] = meta["sha256"] == expected
        value = json_doc(raw, rel) if path.suffix == ".json" else None
        return meta, value
    except Exception as exc:
        return {"path": rel, "readable": False, "error": str(exc)}, None


def row(passed: bool, observed: Any = None, expected: Any = None, blocker: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"passed": bool(passed)}
    if observed is not None:
        out["observed"] = observed
    if expected is not None:
        out["expected"] = expected
    if blocker is not None:
        out["blocker"] = blocker
    return out


def get(value: Any, *keys: str, default: Any = None) -> Any:
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def path_absent(root: Path, rel: str) -> bool:
    """Return true only when even a dangling symlink is absent."""

    try:
        os.lstat(root / rel)
    except FileNotFoundError:
        return True
    except OSError:
        return False
    return False


def count_key(value: Any, wanted: str) -> int:
    if isinstance(value, dict):
        return sum((1 if key == wanted else 0) + count_key(child, wanted) for key, child in value.items())
    if isinstance(value, list):
        return sum(count_key(child, wanted) for child in value)
    return 0


def import_v1(root: Path) -> Any:
    path = root / V1_REL
    raw, meta = read_stable(path)
    if meta["sha256"] != V1_SHA256:
        raise RuntimeError(f"v1 source hash mismatch: {meta['sha256']} != {V1_SHA256}")
    spec = importlib.util.spec_from_file_location("cm2_tail_dependency_preflight_v1_pinned", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned v1 preflight")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_v16r2(root: Path) -> dict[str, Any]:
    files: dict[str, Any] = {}
    docs: dict[str, Any] = {}
    for role, rel in V16R2_FILES.items():
        meta, value = probe(root, rel, V16R2_SHA256[role])
        files[role] = meta
        if value is not None:
            docs[role] = value

    schema = docs.get("schema", {})
    contract = docs.get("contract", {})
    transition = docs.get("transition", {})
    audit = docs.get("static_audit", {})
    bundle = get(contract, "v16r2_bundle", default={})
    audit_bundle = get(audit, "audited_v16r2_bundle", default={})
    closure = get(audit, "schema_and_constructor_closure", default={})
    dual = get(audit, "dual_independent_static_checkers", default={})
    attacks = get(audit, "coherent_attack_static_census", default={})
    static_credit = get(audit, "static_credit_census", default={})
    no_run = get(audit, "static_no_run", default={})
    transition_bundle = get(transition, "successor_v16r2_static_bundle", default={})
    credit = get(contract, "credit_boundary", default={})
    exact_paths = get(contract, "exact_publication_paths", default={})
    manifest_rel = exact_paths.get("cold_launch_exact8_manifest", V16R2_MANIFEST_REL)
    outer_rel = exact_paths.get("cold_launch_outer_last", V16R2_OUTER_REL)

    schema_ref_count = count_key(schema, "$ref")
    schema_def_count = len(schema.get("$defs", {})) if isinstance(schema, dict) else 0
    checks = {
        "seven_file_hash_pins": row(
            all(files.get(role, {}).get("sha256_match") is True for role in V16R2_FILES),
            observed={role: files.get(role, {}).get("sha256") for role in V16R2_FILES},
            expected=V16R2_SHA256,
        ),
        "seven_file_staging_shape": row(
            all(
                files.get(role, {}).get("mode_octal") == V16R2_MODE[role]
                and files.get(role, {}).get("nlink") == 1
                for role in V16R2_FILES
            ),
            observed={role: {"mode": files.get(role, {}).get("mode_octal"), "nlink": files.get(role, {}).get("nlink")} for role in V16R2_FILES},
            expected=V16R2_MODE,
        ),
        "schema_46_defs_242_refs_52_closed": row(
            schema_def_count == 46
            and schema_ref_count == 242
            and closure.get("closed_object_count") == 52,
            observed={
                "schema_defs": schema_def_count,
                "schema_refs": schema_ref_count,
                "closed_objects": closure.get("closed_object_count"),
            },
            expected={"schema_defs": 46, "schema_refs": 242, "closed_objects": 52},
        ),
        "source_template_and_dual_checker_staging": row(
            audit.get("status") == "STAGING_V16R2_FULL_SHAPE_REBUILD__RUNTIME_NOT_AUTHORIZED"
            and dual.get("checker_A", {}).get("status") == "NOT_RUN_SOURCE_TEMPLATE_ONLY"
            and dual.get("checker_B", {}).get("status") == "NOT_RUN_SOURCE_TEMPLATE_ONLY"
            and dual.get("checker_A", {}).get("failed_static_check_count") == 1
            and dual.get("checker_B", {}).get("failed_static_check_count") == 1
            and dual.get("all_common_callsite_censuses_equal") is False
            and dual.get("all_pin_normalizers_equal") is False,
            observed={
                "audit_status": audit.get("status"),
                "checker_A": dual.get("checker_A"),
                "checker_B": dual.get("checker_B"),
                "all_common_callsite_censuses_equal": dual.get("all_common_callsite_censuses_equal"),
                "all_pin_normalizers_equal": dual.get("all_pin_normalizers_equal"),
            },
            blocker="Independent source review is not run; staging cannot enter cold freeze.",
        ),
        "attack_census_0_of_137_deferred": row(
            attacks.get("exact_unique_ordered_attack_count_observed") == 0
            and attacks.get("exact_unique_ordered_attack_count_required") == 137
            and attacks.get("attack_execution_deferred_to_cold_runtime") is True,
            observed={
                "observed": attacks.get("exact_unique_ordered_attack_count_observed"),
                "required": attacks.get("exact_unique_ordered_attack_count_required"),
                "deferred": attacks.get("attack_execution_deferred_to_cold_runtime"),
            },
            expected={"observed": 0, "required": 137, "deferred": True},
            blocker="Coherent attack set has not run in cold runtime.",
        ),
        "contract_and_audit_unpinned": row(
            bundle.get("pin_state") == "SOURCE_TEMPLATES_UNPINNED__STATIC_ONLY__NO_HASH_CYCLE__COLD_LAUNCHER_EXTERNAL_PIN_REQUIRED"
            and bundle.get("contract_file_sha256") == "UNPINNED_STATIC_CONTRACT"
            and bundle.get("contract_object_sha256") == "UNPINNED_STATIC_CONTRACT_OBJECT"
            and audit_bundle.get("audit_file_sha256") == "UNPINNED_STATIC_AUDIT",
            observed={
                "pin_state": bundle.get("pin_state"),
                "contract_file_sha256": bundle.get("contract_file_sha256"),
                "contract_object_sha256": bundle.get("contract_object_sha256"),
                "audit_file_sha256": audit_bundle.get("audit_file_sha256"),
            },
            blocker="Final core pins must be installed and independently replayed before manifest/outer.",
        ),
        "manifest_outer_absent": row(
            manifest_rel == V16R2_MANIFEST_REL
            and outer_rel == V16R2_OUTER_REL
            and path_absent(root, V16R2_MANIFEST_REL)
            and path_absent(root, V16R2_OUTER_REL)
            and transition_bundle.get("cold_launch_outer_closure", {}).get("manifest_or_outer_absent_in_this_static_phase") is True,
            observed={
                "manifest": manifest_rel,
                "outer": outer_rel,
                "transition_assertion": transition_bundle.get("cold_launch_outer_closure", {}).get("manifest_or_outer_absent_in_this_static_phase"),
            },
            blocker="Manifest is ninth and outer is tenth; neither may exist before dual static GO.",
        ),
        "transition_zero_credit": row(
            transition.get("status") == "STATIC_BYTES_CLOSED_V16_TO_V16R2__PHYSICAL_FREEZE_PENDING__RUNTIME_NOT_AUTHORIZED"
            and transition.get("D02_unlock") is False
            and transition.get("formal_global_closure_credit") == 0
            and transition.get("D02_task_credit") == 0
            and transition.get("C79_runtime_artifacts_created") == 0,
            observed={
                "status": transition.get("status"),
                "D02_unlock": transition.get("D02_unlock"),
                "formal_global_closure_credit": transition.get("formal_global_closure_credit"),
                "D02_task_credit": transition.get("D02_task_credit"),
                "C79_runtime_artifacts_created": transition.get("C79_runtime_artifacts_created"),
            },
        ),
        "credit_boundary_zero": row(
            credit.get("D02_formal_pending_task_count") == 33638
            and credit.get("D02_gate_credit") == 0
            and credit.get("D02_unlock") is False
            and credit.get("v16r2_runtime_authorized") is False
            and static_credit.get("all_persisted_v16r2_objects_formal_global_closure_credit") == 0
            and no_run.get("C79_entrypoint_executed") is False,
            observed={
                "D02_formal_pending_task_count": credit.get("D02_formal_pending_task_count"),
                "D02_gate_credit": credit.get("D02_gate_credit"),
                "D02_unlock": credit.get("D02_unlock"),
                "v16r2_runtime_authorized": credit.get("v16r2_runtime_authorized"),
                "persisted_credit": static_credit.get("all_persisted_v16r2_objects_formal_global_closure_credit"),
                "C79_entrypoint_executed": no_run.get("C79_entrypoint_executed"),
            },
        ),
    }
    return {
        "status": "V16R2_STAGING_PHYSICAL_FREEZE_PENDING",
        "files": files,
        "checks": checks,
        "schema_shape": {"defs": schema_def_count, "refs": schema_ref_count, "closed_objects": closure.get("closed_object_count")},
        "attack_census": {"observed": attacks.get("exact_unique_ordered_attack_count_observed"), "required": attacks.get("exact_unique_ordered_attack_count_required")},
        "formal_global_closure_credit": 0,
        "D02_unlock": False,
        "runtime_authorized": False,
        "ready_for_cold_freeze": False,
        "blocker": "Run independent source reviewer/CI to GO, pin contract/audit, then execute cold exact8 -> manifest -> outer-last.",
    }


def failures(value: Any, prefix: str = "") -> list[str]:
    out: list[str] = []
    if isinstance(value, dict):
        if value.get("passed") is False:
            out.append(prefix or "check")
        if value.get("sha256_match") is False:
            out.append(f"{prefix}.sha256_match" if prefix else "sha256_match")
        for key, child in value.items():
            if key in {"passed", "sha256_match"}:
                continue
            out.extend(failures(child, f"{prefix}.{key}" if prefix else key))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            out.extend(failures(child, f"{prefix}[{i}]"))
    return out


def main() -> int:
    try:
        root = ROOT
        v1 = import_v1(root)
        base_report, base_code = v1.run(root)
        v16r2 = check_v16r2(root)
        report: dict[str, Any] = {
            "schema": "cm2.tail-dependency-preflight.v2",
            "workspace_root": str(root),
            "invocation": {
                "sys_flag_B_seen": bool(sys.flags.dont_write_bytecode),
                "bytecode_disabled": bool(sys.dont_write_bytecode),
                "read_only": True,
                "runtime_write_attempted": False,
                "credit_attempted": False,
            },
            "base_v1": base_report,
            "v16r2_staging": v16r2,
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "cm2_ready": False,
            "tail_order": [
                "v16r2 source GO + physical exact8 freeze",
                "manifest ninth -> outer tenth",
                "C79g unresolved_zero consumer and positive wrapper",
                "D02-A 33638 -> D02-B 7463/14926 -> D02-C 862/76832",
                "D03 -> D04 -> Gate5 18/18 + complete block -> fresh clean-room",
            ],
        }
        failed = failures(report)
        report["failed_check_count"] = len(failed)
        report["failed_checks"] = failed
        ok = (
            base_code == 0
            and v16r2.get("status") == "V16R2_STAGING_PHYSICAL_FREEZE_PENDING"
            and not failed
            and bool(sys.flags.dont_write_bytecode)
        )
        report["status"] = "READ_ONLY_PREFLIGHT_V2_COMPLETE__CM2_NO_GO" if ok else "FAIL_CLOSED_PREFLIGHT_V2"
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0 if ok else 1
    except Exception as exc:
        print(json.dumps({
            "schema": "cm2.tail-dependency-preflight.v2.failure",
            "status": "FAIL_CLOSED_PREFLIGHT_V2",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "formal_global_closure_credit": 0,
            "D02_unlock": False,
            "cm2_ready": False,
            "read_only": True,
            "runtime_write_attempted": False,
            "credit_attempted": False,
        }, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
