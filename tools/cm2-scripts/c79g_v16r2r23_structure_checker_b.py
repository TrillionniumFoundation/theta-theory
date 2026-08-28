#!/usr/bin/env python3
"""Independent checker B for the r23 static DAG (read-only).

This implementation intentionally does not import checker A or any protocol
source.  It reconstructs the path/hash graph from the filesystem and emits a
small, separately named report; a failure is nonzero and never writes state.
"""
from __future__ import annotations
import ast, hashlib, json, os, re, stat, sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
BASE = "cm2_round306c79g_true_global_no_producer_consumer"
SUFFIX = os.environ.get("CM2_SUCCESSOR_SUFFIX", "v16r2r23")
PREV = os.environ.get("CM2_PREDECESSOR_SUFFIX", "v16r2r22")
HEX = re.compile(r"^[0-9a-f]{64}$")


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def walk(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def read(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(fd); named = os.lstat(path)
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or
                (before.st_dev, before.st_ino, before.st_size) !=
                (named.st_dev, named.st_ino, named.st_size)):
            raise RuntimeError(f"identity:{path}")
        chunks = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(fd); named_after = os.lstat(path)
        if ((before.st_dev, before.st_ino, before.st_size) !=
                (after.st_dev, after.st_ino, after.st_size) or
                (before.st_dev, before.st_ino) !=
                (named_after.st_dev, named_after.st_ino)):
            raise RuntimeError(f"drift:{path}")
        return b"".join(chunks)
    finally:
        os.close(fd)


def load(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = read(path)
    seen: set[str] = set()
    def hook(items):
        result = {}
        for key, value in items:
            if key in seen:
                raise ValueError("duplicate key:" + key)
            seen.add(key); result[key] = value
        seen.clear()
        return result
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=hook,
                       parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    if not isinstance(value, dict):
        raise ValueError("object required")
    return value, raw


def closed(value: dict[str, Any]) -> bool:
    claim = value.get("object_sha256")
    if not isinstance(claim, str) or not HEX.fullmatch(claim):
        return False
    body = dict(value); body.pop("object_sha256", None)
    return sha(canon(body)) == claim


def main() -> int:
    sources = {
        "producer": OUT / f"{BASE}_{SUFFIX}_semantic_source.py",
        "consumer": OUT / f"{BASE}_independent_verifier_assembler_authority_consumer_{SUFFIX}_semantic_source.py",
        "launcher": OUT / f"{BASE}_cold_launch_{SUFFIX}_semantic_source.py",
    }
    receipts = {
        "anchor": OUT / f"{BASE}_{SUFFIX}_active_predecessor_supersession_receipt_v1.json",
        "rejection": OUT / f"{BASE}_{PREV}_static_bundle_rejection_receipt_v1.json",
        "supersession": OUT / f"{BASE}_{PREV}_to_{SUFFIX}_static_bundle_rejection_supersession_receipt_v1.json",
        "schema": OUT / f"{BASE}_schema_{SUFFIX}.json",
        "contract": OUT / f"{BASE}_contract_{SUFFIX}.json",
        "transition": OUT / f"{BASE}_{PREV}_to_{SUFFIX}_static_launch_transition_receipt_v1.json",
        "audit": OUT / f"{BASE}_static_audit_{SUFFIX}.json",
    }
    checks: list[dict[str, Any]] = []
    def check(name: str, ok: bool, detail: Any = None) -> None:
        row = {"name": name, "passed": bool(ok)}
        if detail is not None: row["detail"] = detail
        checks.append(row)
    try:
        all_paths = {**sources, **receipts}
        check("all_paths", all(p.is_file() for p in all_paths.values()))
        raw = {k: read(p) for k, p in all_paths.items()}
        vals = {k: load(p)[0] for k, p in receipts.items()}
        # Sources are 0664/0644 while draft/static bytes are being reviewed,
        # and are chmod-frozen to 0444 for exact8 publication.  JSON receipts
        # remain 0444 throughout.  Never relax regular-file or nlink checks.
        check("modes_and_identity", all(stat.S_IMODE(p.stat().st_mode) in ({0o444, 0o644, 0o664} if k in sources else {0o444}) and p.stat().st_nlink == 1 for k, p in all_paths.items()))
        trees = {}
        for k, p in sources.items():
            text = raw[k].decode("utf-8"); trees[k] = ast.parse(text, str(p)); compile(trees[k], str(p), "exec")
        check("ast_compile", len(trees) == 3)
        check("namespace_literals", all(SUFFIX.encode() in raw[k] and f"{SUFFIX}_semantic_source" in raw[k].decode() for k in sources))
        check("no_old_tokens", all(x not in raw[k].lower() for k in sources for x in (b"v16r2r15", b"v16r2r16", b"v15")))
        # Schema definitions describe the eventual positive authority shape
        # (including const=1/true); they are not persisted credit.  Exclude
        # ``$defs`` and inspect only the live instance roots/receipts.
        zero_values = [v for k, v in vals.items() if k != "schema"]
        zero_values.append({k: v for k, v in vals["schema"].items() if k != "$defs"})
        check("zero_credit", all(node.get("formal_global_closure_credit", 0) in (0, False, None) and node.get("D02_unlock") is not True and node.get("runtime_authorized") is not True for v in zero_values for node in walk(v) if isinstance(node, dict)))
        check("receipt_closure", all(closed(vals[k]) for k in ("anchor", "rejection", "supersession", "contract", "transition", "audit")))
        schema = vals["schema"]; check("schema_shape", (len(schema.get("$defs", {})), sum(isinstance(n, dict) and "$ref" in n for n in walk(schema)), sum(isinstance(n, dict) and n.get("additionalProperties") is False for n in walk(schema))) == (46, 242, 52))
        check("instance_shapes", (len(vals["contract"]), len(vals["transition"]), len(vals["audit"])) == (30, 31, 30))
        anchor, rej, sup = vals["anchor"], vals["rejection"], vals["supersession"]
        check("chain_direction", anchor.get("predecessor_namespace") == PREV and anchor.get("successor_namespace") == f"{SUFFIX}_semantic_source" and sup.get("predecessor_namespace") == PREV and sup.get("successor_namespace") == SUFFIX and rej.get("failed_namespace") == PREV)
        check("chain_hash_links", sha(raw["rejection"]) == sup.get("predecessor_rejection_file_sha256") and rej.get("object_sha256") == sup.get("predecessor_rejection_object_sha256") and sha(raw["supersession"]) == anchor.get("predecessor_supersession_file_sha256") and sup.get("object_sha256") == anchor.get("predecessor_supersession_object_sha256"))
        expected8 = [str(receipts["anchor"].relative_to(ROOT)), str(receipts["schema"].relative_to(ROOT)), str(receipts["contract"].relative_to(ROOT)), str(sources["producer"].relative_to(ROOT)), str(sources["consumer"].relative_to(ROOT)), str(receipts["transition"].relative_to(ROOT)), str(receipts["audit"].relative_to(ROOT)), str(sources["launcher"].relative_to(ROOT))]
        cb = vals["contract"].get("v16r2_bundle", {}); tr = vals["transition"]; succ = tr.get("successor_v16r2_static_bundle", {})
        check("exact8_and_boundary", cb.get("exact8_ordered_paths") == expected8 and cb.get("base7_ordered_paths") == expected8[:-1] and tr.get("cold_launch_boundary", {}).get("base7_order") == expected8[:-1])
        expected11 = {"all_four_core_file_pins_final", "build_only_producer", "closed_schema", "cold_launcher_v16r2_path", "contract", "draft_pin_sentinels_remain_present", "final_consumer_pin_installed", "independent_verifier_assembler_authority_consumer", "static_audit_v16r2_path", "transition_receipt_bytes_are_closed_around_final_core_pins", "transition_receipt_physical_freeze_completed"}
        check("exact11", set(succ) == expected11 and not any(isinstance(n, dict) and "source_hashes" in n for v in vals.values() for n in walk(v)))
        hashes = {k: sha(raw[k]) for k in all_paths}
        check("cross_pins", cb.get("schema_file_sha256") == hashes["schema"] and cb.get("predecessor_semantic_supersession", {}).get("file_sha256") == hashes["anchor"] and succ.get("build_only_producer", {}).get("file_sha256") == hashes["producer"] and succ.get("independent_verifier_assembler_authority_consumer", {}).get("file_sha256") == hashes["consumer"] and succ.get("contract", {}).get("file_sha256") == hashes["contract"] and vals["audit"].get("audited_v16r2_bundle", {}).get("transition_file_sha256") == hashes["transition"])
        check("source_constants", all(f"ACTIVE_PREDECESSOR_SUPERSESSION_FILE_PIN = \"{hashes['anchor']}\"" in raw[k].decode() for k in ("producer", "consumer", "launcher")))
        check("no_cold_surfaces", not (OUT / f"{BASE}_cold_launch_manifest_{SUFFIX}.sha256").exists() and not (OUT / f"{BASE}_cold_launch_outer_receipt_{SUFFIX}.json").exists() and not any(SUFFIX in str(p) for p in ROOT.rglob("*.pyc")))
        passed = all(row["passed"] for row in checks)
        report = {"schema": f"cm2.c79g.{SUFFIX}.independent-checker-b.v1", "status": "PASS_INDEPENDENT_CHECKER_B__ZERO_CREDIT" if passed else "FAIL_CLOSED_INDEPENDENT_CHECKER_B", "successor_suffix": SUFFIX, "predecessor_suffix": PREV, "check_count": len(checks), "failed_check_count": sum(not row["passed"] for row in checks), "checks": checks, "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False, "read_only": True}
        report["object_sha256"] = sha(canon(report)); print(json.dumps(report, sort_keys=True)); return 0 if passed else 1
    except Exception as exc:
        print(json.dumps({"schema": f"cm2.c79g.{SUFFIX}.independent-checker-b.v1", "status": "FAIL_CLOSED_INDEPENDENT_CHECKER_B_EXCEPTION", "error": f"{type(exc).__name__}: {exc}", "formal_global_closure_credit": 0, "D02_unlock": False, "runtime_authorized": False, "read_only": True}, sort_keys=True)); return 1


if __name__ == "__main__":
    raise SystemExit(main())
