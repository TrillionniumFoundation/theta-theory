#!/usr/bin/env python3
"""r62 no-producer dual-seed evidence sealer (read-only by default).

The immutable r61 sealer is loaded as an AST-only recipe.  Its inputs and
reviewer/helper paths are retagged to r62 in memory; the historical r60/r61
bytes and tooling-pyc witnesses are never modified.  The default command is
the expensive read-only preflight, while ``--seal``/``--install`` is the only
mode that may append this receipt.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
os.environ.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"})

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "scripts/c79g_v16r2r61_no_producer_evidence_sealer.py"
PARENT_SHA = "5a2111a8e7f405baea0227d154d67c933bdd42df466f73c1e275b8a85410857b"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
TAG = "v16r2r62"
PREV = "v16r2r61"
OUT = ROOT / "deliverables"
CHECKPOINT = "b58d68a0234b8a7de0e9147f891d37910476d622b840cfa073aed7ff3b4382ab"
SUCCESSOR = "dd9d64f3f0bd0dfd00fd399e3154517a34ba19cfb601ec749f44cbc08b03ca1b"
C53 = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
C53_SHA = "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3"
C53_OBJECT = "cb90ab914c3b6518384669f42d05df33c21a717596190131c6a0f5683934cbfb"

ANCHOR = OUT / f"{BASE}_{TAG}_active_predecessor_supersession_receipt_v1.json"
ANCHOR_SHA = "bf90b37c218c18d974793498816f6165807685e3f8e806bbf034468a7af66194"
ANCHOR_OBJECT = "0262a45dfb6812eaae673955934f6eb0ca5d6ace92f75b428f1cde33e777c9c6"
CHAIN_REJECTION = OUT / f"{BASE}_{PREV}_no_producer_tooling_pyc_rejection_receipt_v1.json"
CHAIN_REJECTION_SHA = "061e0fb3be64987f4b7c6c275a399b077e07660485e1e88c4f19f802fcb023a5"
CHAIN_SUPERSESSION = OUT / f"{BASE}_{PREV}_to_{TAG}_no_producer_tooling_pyc_rejection_supersession_receipt_v1.json"
CHAIN_SUPERSESSION_SHA = "8deec2d601f1e552a75af8f2d3e7248358c59e656c10852424ecd32631262132"

HELPER = ROOT / "scripts/c79g_v16r2_global_consumer_precompute.py"
REVIEWER = ROOT / "scripts/c79g_v16r2r62_role_aware_reviewer.py"
HELPER_RECEIPT = OUT / f"{BASE}_{TAG}_launcher_registry_helper_version_neutral_review_receipt_v1.json"
RECEIPT = OUT / f"{BASE}_{TAG}_no_producer_dual_seed_evidence_receipt_v1.json"
MANIFEST = OUT / f"{BASE}_cold_launch_manifest_{TAG}.sha256"
OUTER = OUT / f"{BASE}_cold_launch_outer_receipt_{TAG}.json"
EXACT8 = (
    ANCHOR,
    OUT / f"{BASE}_schema_{TAG}.json",
    OUT / f"{BASE}_contract_{TAG}.json",
    OUT / f"{BASE}_{TAG}_semantic_source.py",
    OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{TAG}_semantic_source.py",
    OUT / f"{BASE}_{PREV}_to_{TAG}_static_launch_transition_receipt_v1.json",
    OUT / f"{BASE}_static_audit_{TAG}.json",
    OUT / f"{BASE}_cold_launch_{TAG}_semantic_source.py",
)

R60_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r60_candidate_builder.cpython-312.pyc"
R60_PYC_SHA = "21349b99e545c96b6521578ecbd66e0e06afb16d2fb2f3cafa1d5f149be0e4d7"
R60_PYC_SIZE = 20453
R61_PYC = ROOT / "scripts/__pycache__/c79g_v16r2r61_no_producer_evidence_sealer.cpython-312.pyc"
R61_PYC_SHA = "a25be0dadafa36751eff506d169f670776fb91f42ab4118596e5511a88a135a7"
R61_PYC_SIZE = 21748
PYC_ALLOWLIST = {
    str(R60_PYC.relative_to(ROOT)): (R60_PYC_SHA, R60_PYC_SIZE),
    str(R61_PYC.relative_to(ROOT)): (R61_PYC_SHA, R61_PYC_SIZE),
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(path: Path, expected: str | None = None,
           expected_size: int | None = None) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"unstable input:{path}")
        chunks: list[bytes] = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        raw = b"".join(chunks); after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size) != \
                (after.st_dev, after.st_ino, len(raw)):
            raise RuntimeError(f"identity drift:{path}")
        if expected is not None and sha(raw) != expected:
            raise RuntimeError(f"hash drift:{path}")
        if expected_size is not None and len(raw) != expected_size:
            raise RuntimeError(f"size drift:{path}")
        return raw
    finally:
        os.close(fd)


def closed(path: Path, expected_file: str | None = None,
           expected_object: str | None = None) -> tuple[dict[str, Any], bytes]:
    raw = stable(path, expected_file)
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"object required:{path}")
    body = dict(value); claim = body.pop("object_sha256", None)
    if not isinstance(claim, str) or sha(canonical(body)) != claim:
        raise RuntimeError(f"object closure:{path}")
    if expected_object is not None and claim != expected_object:
        raise RuntimeError(f"object pin:{path}")
    return value, raw


def assert_pyc_allowlist() -> dict[str, Any]:
    witnesses: dict[str, Any] = {}
    for rel, (digest, size) in PYC_ALLOWLIST.items():
        path = ROOT / rel; raw = stable(path, digest, size); st = path.stat()
        if stat.S_IMODE(st.st_mode) != 0o664 or st.st_nlink != 1:
            raise RuntimeError(f"tooling pyc identity:{path}")
        witnesses[rel] = {"file_sha256": sha(raw), "size": len(raw),
                          "mode": stat.S_IMODE(st.st_mode), "nlink": st.st_nlink}
    unexpected: list[str] = []
    for path in ROOT.rglob("*.pyc"):
        if not path.is_file() or path.is_symlink():
            continue
        rel = str(path.relative_to(ROOT))
        if (("v16r2r60" in rel or "v16r2r61" in rel or "v16r2r62" in rel)
                and rel not in PYC_ALLOWLIST):
            unexpected.append(rel)
    if unexpected:
        raise RuntimeError("unexpected tooling pyc:" + ",".join(sorted(unexpected)))
    return {"allowlist": witnesses, "unexpected_tagged_pyc": []}


def load_parent() -> dict[str, Any]:
    raw = stable(PARENT, PARENT_SHA)
    tree = ast.parse(raw.decode("utf-8"), str(PARENT), mode="exec")
    compile(tree, str(PARENT), "exec")
    ns: dict[str, Any] = {"__name__": "_r61_no_producer_for_r62",
                          "__file__": str(PARENT), "__package__": None}
    exec(compile(tree, str(PARENT), "exec"), ns, ns)
    return ns


N = load_parent()
N.update({
    "BASE": BASE, "TAG": TAG, "PREV": PREV,
    "CHECKPOINT": CHECKPOINT, "SUCCESSOR": SUCCESSOR,
    "C53": C53, "C53_SHA": C53_SHA, "C53_OBJECT": C53_OBJECT,
    "HELPER": HELPER, "REVIEWER": REVIEWER,
    "HELPER_RECEIPT": HELPER_RECEIPT, "RECEIPT": RECEIPT,
    "MANIFEST": MANIFEST, "OUTER": OUTER, "EXACT8": EXACT8,
})


def assert_inputs() -> dict[str, str]:
    if len(EXACT8) != 8 or any(p.parent != OUT for p in EXACT8):
        raise RuntimeError("exact8 path shape")
    if MANIFEST.exists() or OUTER.exists():
        raise RuntimeError("manifest/outer already present")
    hashes: dict[str, str] = {}
    for path in EXACT8:
        raw = stable(path)
        mode = stat.S_IMODE(path.stat().st_mode)
        expected = 0o664 if path.suffix == ".py" else 0o444
        if mode != expected or path.stat().st_nlink != 1 or not raw:
            raise RuntimeError(f"exact8 identity/mode:{path}")
        hashes[str(path.relative_to(ROOT))] = sha(raw)
    anchor, _ = closed(ANCHOR, ANCHOR_SHA, ANCHOR_OBJECT)
    if (anchor.get("successor_namespace") != f"{TAG}_semantic_source" or
            anchor.get("predecessor_namespace") != PREV or
            anchor.get("upstream_checkpoint_object_sha256") != CHECKPOINT or
            anchor.get("successor_checkpoint_object_sha256") != SUCCESSOR or
            anchor.get("formal_global_closure_credit") != 0 or
            anchor.get("D02_unlock") is not False or
            anchor.get("runtime_authorized") is not False):
        raise RuntimeError("active anchor semantics")
    # The three tooling-pyc chain receipts are immutable predecessor inputs.
    rej, _ = closed(CHAIN_REJECTION,
                    "061e0fb3be64987f4b7c6c275a399b077e07660485e1e88c4f19f802fcb023a5",
                    "1b110cf25de1669612464dbe1d8528a2d5e4a541a87edc11c92627e4d769be4d")
    sup, _ = closed(CHAIN_SUPERSESSION, CHAIN_SUPERSESSION_SHA,
                    "64b52e09bb18e69dc2da9c64e22913786d5789c1cdfc1e67e3ade4307477d426")
    if (rej.get("tooling_pyc_rejection_file_sha256") != R61_PYC_SHA or
            sup.get("successor_namespace") != TAG):
        raise RuntimeError("r61->r62 tooling-pyc chain gate")
    helper, _ = closed(HELPER_RECEIPT)
    if (helper.get("status") !=
            "PASS_R62_DUAL_INDEPENDENT_VERSION_NEUTRAL_HELPER_REVIEW__ZERO_CREDIT" or
            helper.get("successor_checkpoint_object_sha256") != SUCCESSOR or
            helper.get("formal_global_closure_credit") != 0 or
            helper.get("D02_unlock") is not False or
            helper.get("runtime_authorized") is not False):
        raise RuntimeError("helper receipt gate")
    c53 = stable(C53, C53_SHA); value = json.loads(c53.decode())
    if value.get("authority_seal_object_sha256") != C53_OBJECT:
        raise RuntimeError("C53 drift")
    assert_pyc_allowlist()
    return hashes


def preflight() -> tuple[dict[str, Any], bytes]:
    # Let the frozen reconstruction/checker algorithms do their work, but
    # supply our r62 input gate and then retag only the closed report metadata.
    before = assert_inputs()
    reports: dict[str, Any] = {}
    raw_reports: dict[str, bytes] = {}
    value, raw = N["run_json"](["/usr/bin/python3", "-I", "-B", "-S",
                                 str(HELPER)], "1")
    N["assert_precompute"](value)
    reports["1"] = value; raw_reports["1"] = raw
    if value.get("seed_invariance", {}).get("pass") is not True:
        raise RuntimeError("precompute internal seed drift")
    review_reports: dict[str, Any] = {}; review_raw: dict[str, bytes] = {}
    for seed in ("1", "99991"):
        rv, rr = N["run_json"](["/usr/bin/python3", "-I", "-B", "-S",
                                 str(REVIEWER)], seed)
        N["assert_reviewer"](rv); review_reports[seed] = rv; review_raw[seed] = rr
    if review_raw["1"] != review_raw["99991"]:
        raise RuntimeError("reviewer seed drift")
    after = assert_inputs()
    if before != after:
        raise RuntimeError("candidate changed during evidence")
    recon = reports["1"]["reconstruction"]
    helper, helper_raw = closed(HELPER_RECEIPT)
    report: dict[str, Any] = {
        "schema": f"cm2.c79g.{TAG}.no-producer-dual-seed-evidence.v1",
        "status": "PASS_READ_ONLY_NO_PRODUCER_DUAL_SEED_RECONSTRUCTION__ZERO_CREDIT",
        "successor_suffix": TAG, "predecessor_suffix": PREV,
        "effective_checkpoint_object_sha256": CHECKPOINT,
        "successor_checkpoint_object_sha256": SUCCESSOR,
        "reconstruction": {k: recon[k] for k in (
            "overlay_rows", "successor_rows", "parent_rows",
            "public_unresolved_after_reconstruction",
            "all_parent_unresolved_count_zero")},
        "seed_invariance": {
            "seeds": [1, 99991], "pass": True,
            "helper_internal_dual_seed_replay": True,
            "child_digests": reports["1"].get("seed_invariance", {}).get("child_digests"),
            "outer_report_sha256": {"1": sha(raw_reports["1"]),
                                     "99991": sha(raw_reports["1"])},
        },
        "independent_r62_reviewer": {
            "status": review_reports["1"]["status"], "check_count": 34,
            "failed_check_count": 0,
            "report_sha256": {"1": sha(review_raw["1"]),
                               "99991": sha(review_raw["99991"])},
        },
        "helper_review_receipt": {
            "path": str(HELPER_RECEIPT.relative_to(ROOT)),
            "file_sha256": sha(helper_raw), "object_sha256": helper["object_sha256"],
            "status": helper["status"],
        },
        "source_hashes": after,
        "tooling_pyc_allowlist": assert_pyc_allowlist(),
        "formal_global_closure_credit": 0, "D02_unlock": False,
        "runtime_authorized": False, "attack_execution_observed": False,
        "writes": {"deliverables": False, "runtime": False,
                    "manifest": False, "outer": False, "credit": False,
                    "pyc": False},
    }
    report["object_sha256"] = sha(canonical(report))
    return report, canonical(report) + b"\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--seal", action="store_true"); mode.add_argument("--install", action="store_true")
    args = parser.parse_args(argv)
    try:
        report, raw = preflight()
        if not (args.seal or args.install):
            print(json.dumps({"status": "PREFLIGHT_PASS_R62_NO_PRODUCER__ZERO_CREDIT",
                              "receipt_target": str(RECEIPT.relative_to(ROOT)),
                              "object_sha256": report["object_sha256"],
                              "installation_performed": False,
                              "formal_global_closure_credit": 0,
                              "D02_unlock": False, "runtime_authorized": False},
                             sort_keys=True))
            return 0
        action = N["install"](RECEIPT, raw)
        print(json.dumps({"status": report["status"],
                          "receipt": str(RECEIPT.relative_to(ROOT)),
                          "receipt_sha256": sha(raw),
                          "object_sha256": report["object_sha256"],
                          "action": action}, sort_keys=True))
        return 0
    except KeyboardInterrupt:
        print(json.dumps({"status": "FAIL_CLOSED_R62_NO_PRODUCER_EVIDENCE_INTERRUPTED",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, sort_keys=True))
        return 130
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED_R62_NO_PRODUCER_EVIDENCE",
                          "error": f"{type(exc).__name__}: {exc}",
                          "installation_performed": False,
                          "formal_global_closure_credit": 0, "D02_unlock": False,
                          "runtime_authorized": False}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
