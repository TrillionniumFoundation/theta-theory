#!/usr/bin/env python3
"""Cold independent verifier for C65s18 v3 shard 00.

The v3 executor is captured as pinned inert bytes and AST only.  It is never
imported or executed.  All 330 shard-0 assignments and their exact numeric
routes are rebuilt through the frozen C41 independent-auditor kernel.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Callable, Iterable
import zlib


sys.dont_write_bytecode = True
SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = SELF.parent
sys.path.insert(0, str(OUT))

import cm2_round306c41_d02_lower_strata_depth3_closure_independent_auditor_v1 as c41a  # noqa: E402


SCHEMA = "cm2.round306c65s18.shard00-independent-cold-verifier.v2"
CORE_SCHEMA = "cm2.round306c65s18.depth18-64shard.v3"
DOMAIN = "cm2.round306c65s18.depth18-64shard.v2.assignment"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SHARD = 0
SHARD_COUNT = 64
ADDITIONAL_DEPTH = 6

EXECUTOR = OUT / "cm2_round306c65s18_depth18_64shard_executor_v3.py"
PREEXEC_MANIFEST = OUT / "cm2_round306c65s18_preexecution_manifest_v3.sha256"
CONTRACT = OUT / "cm2_round306c65s18_independent_contract_v2.json"
ASSIGNMENT = OUT / "cm2_round306c65s18_depth18_64shard_assignment_result_v2.json"
INVENTORY = OUT / "cm2_round306c65s18_depth18_64shard_assignment_inventory_v2.jsonl.gz"
AUTHORIZATION = OUT / "cm2_round306c65s18_assignment_authorization_seal_v2.json"
C61_RESULT = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_result_v4.json"
C61_LEAVES = OUT / "cm2_round306c61s12_depth12_16shard_aggregate_leaf_ledger_v4.jsonl.gz"
C58_RESULT = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_result_v1.json"
C58_LEAVES = OUT / "cm2_round306c58s2_singleton_collision2_handoff_depth6_refinement_leaf_ledger_v1.jsonl.gz"
LEDGER = OUT / "cm2_round306c65s18_depth18_64shard_shard_00_leaf_ledger_v3.jsonl.gz"
RECEIPT = OUT / "cm2_round306c65s18_depth18_64shard_shard_00_receipt_v3.json"
C40 = ROOT / ".cm2-runtime/candidates/c40-h1-endpoint-c2-arrangement-20260810T234000Z-c2f144e29bc1172f"

CANONICAL = OUT / "CM2_LATEST_STATUS.md"
CANONICAL_COMPANION = OUT / "CM2_LATEST_STATUS.sha256"
GLOBAL_HEAD = ROOT / ".cm2-runtime/cm2-global-authority-heads/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.seal"
GLOBAL_CLAIM = ROOT / ".cm2-runtime/cm2-global-successor-claims/predecessor-10fb050d30c92b0f2bdcf85a30d28ff670d8efc0b48104b7f04a63c391967b41.claim"
C53_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-token"
C53_AUDIT_TOKEN = ROOT / ".cm2-runtime/c53-current-pair-successor-audit-token"

VERIFY_OUT = OUT / "cm2_round306c65s18_shard00_independent_cold_verification_v2.json"
SELFTEST_OUT = OUT / "cm2_round306c65s18_shard00_independent_cold_self_test_v2.json"

PIN = {
    "executor_file": "170df261ed9451fc3ecc1fca5e686c6f6d8eeb3d643126da09f30c634cda22ef",
    "preexec_manifest_file": "8882eb9b9eda1b1bb4c1e065c4c1d25b45de15b42af79804594c9e0887511423",
    "contract_file": "e320ac48b1cf3675a3c152d0cb9e6084ba750433722fef716e4a8ab534fab287",
    "contract_object": "5d8a39432c2b02e807c5624ea26f56a12b58f66601ab391b52fee89d0ca604a4",
    "assignment_file": "0306fd12de7d73988a45bac84acf70e4615e8e3aaef7c3c42a66fc39dbef4baa",
    "assignment_object": "c7671985713c8cfd8a496931f1b2686fa545448ce0a434c89e943b178000407f",
    "inventory_file": "e2c4714f1f1a8aa470a393d25ff03aaa3228f08979c30c90fd5f297469d6ad30",
    "authorization_file": "99788b913ee8b900c97e14b6b52d90b0ad83ef2c3fddda6d9f82ab0aacc39ca0",
    "authorization_object": "d1b508a54553b8944b50e926e895b35a589fe6aca3a03440e416571b339ca228",
    "C61_result_file": "06b4146185cb6ef0c8d908d523369008481f7df4e6a05ad5956c001267b07f5e",
    "C61_result_object": "05bcb4301ac74aefd6744db2e633c2479c423fab881b33609bf7234a5537e584",
    "C61_leaf_file": "2656bc4d1b99d37da3733338d85c8d6301621563a400d5db40380078c001b1c2",
    "C58_result_file": "ed4eb1e5ea64c61e4b85a710c1429a2f0b489048320badd4d9a8214bc38c05bc",
    "C58_result_object": "038503bd21505dacde4ce6dc59a320fa70a97cc0dccce33be210c60bbd7d0a30",
    "C58_leaf_file": "15a5b1c5c15f8528591bd80be040317590dadec70b4476d01eb3763ae64965df",
    "C40_result_file": "f721b08a4addb7c0369b27ea3af8546c9fad293b1a7808d015bbf783b3aa22d6",
    "C40_object": "397eda962e4bd20429d7cab1ffc53d82cccfdf59bdce8cd03b271a8ded0536ba",
    "C41_independent_auditor_file": "537f3dea94c3743235df8984ba4922d37f82999ff3d8abbac59e5171ef38b74c",
    "ledger_file": "c9da80d725d6b11f1e8a7e181dff6b02aa7b604b0aedbf35522e4fd3629de7af",
    "receipt_file": "8a932d0abc64761db4eda758122dca4665afea42cf5e6d97fcc303fb1b46018a",
    "receipt_object": "3f61e37aa9cf11e1c564f2585fdfea0c3ba0f1d8baa30828cf831dd19f72a4cc",
    "canonical_file": "922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57",
    "canonical_companion_file": "57d0c75a2dc774d312fc72a11c66e745cf9b7232531e469490bac492b0a91d6b",
    "global_head_file": "f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3",
    "global_claim_file": "3801e452f218e330bc16faed5986146202a7d7026e46924bf7bc00167b05f77b",
    "C53_token_file": "dcad8792bb4bede7f97f9996d10b43497b6286704dbc8f1b8a4170a9e2416846",
    "C53_audit_token_file": "c3a9a3248b2ec3cb0887b62f4edade7664f73f1746593be1b69897404ae42eba",
}

PREEXEC_MEMBERS = {
    "cm2_round306c65s18_independent_contract_v2.json": PIN["contract_file"],
    "cm2_round306c65s18_assignment_builder_final_v2.py": "700326aee68f423b8e03a9f8adda95a07b811bab60e95bd159c8e46cc290794b",
    "cm2_round306c65s18_depth18_64shard_assignment_inventory_v2.jsonl.gz": PIN["inventory_file"],
    "cm2_round306c65s18_depth18_64shard_assignment_result_v2.json": PIN["assignment_file"],
    "cm2_round306c65s18_assignment_authorization_sealer_v2.py": "ae122914853a234dfc8a44bd915700ab0fcec7823fab7e5c7f5061b50cb865df",
    "cm2_round306c65s18_assignment_authorization_seal_v2.json": PIN["authorization_file"],
    "cm2_round306c65s18_depth18_64shard_executor_v3.py": PIN["executor_file"],
    "cm2_round306c65s18_preexecution_smoke_v3.json": "a7f7c1f8ee4ed186f871d2981307a865ddc9a17d2e66868ef7f2d261e1a0128e",
    "cm2_round306c65s18_independent_preexecution_verifier_v3.py": "d85b0b0eb723b762ec116433e05555cd0c8286e5af6909349c8ba766959b173f",
    "cm2_round306c65s18_independent_preexecution_verification_v3.json": "f6c70cf56560d51a13916a1cb022e1a4ad1f68708469d7002f9606ca18a1029c",
    "cm2_round306c65s18_independent_preexecution_self_test_v3.json": "27a908491264a15ebdd3c72df60d381996a7d929ceeb4bcba47fa14b7aef5dff",
    "cm2_round306c65s18_executor_v2_REJECTED_AFTER_ZERO_WRITE_SHARD0_SCHEMA_KEY_FAIL.md": "49ed8c6dc5c37c5b987b7aea92d292407725955e2283c93c57a0ec9563c2c57b",
    "cm2_round306c65s18_preexecution_report_v3.md": "19b183c1045075bd5e711f1d5eee4b8f8cbec4f3f35860ad390102e504c33036",
}


class Rejected(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Rejected(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def close(value: dict[str, Any]) -> dict[str, Any]:
    answer = copy.deepcopy(value)
    need("object_sha256" not in answer, "already closed")
    answer["object_sha256"] = digest(answer)
    return answer


def parse(raw: bytes, label: str, canonical_required: bool = False) -> Any:
    need(bool(raw) and not raw.startswith(b"\xef\xbb\xbf"), label + " strict bytes")

    def hook(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            need(key not in result, label + " duplicate key:" + key)
            result[key] = value
        return result

    value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=hook,
                       parse_constant=lambda token: (_ for _ in ()).throw(
                           Rejected(label + " nonfinite:" + token)))
    if canonical_required:
        need(raw == canonical(value) + b"\n", label + " canonical bytes")
    return value


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns)


def capture(paths: Iterable[Path], maximum: int = 768 << 20,
            hook: Callable[[], None] | None = None) -> dict[Path, bytes]:
    ordered = tuple(paths)
    need(len(ordered) == len(set(ordered)), "duplicate capture path")
    descriptors: dict[Path, int] = {}
    before: dict[Path, os.stat_result] = {}
    try:
        for path in ordered:
            descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                                 getattr(os, "O_NOFOLLOW", 0))
            state = os.fstat(descriptor)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 0 < state.st_size <= maximum, "single-link frozen input:" + str(path))
            descriptors[path] = descriptor
            before[path] = state
        result: dict[Path, bytes] = {}
        for path in ordered:
            chunks: list[bytes] = []
            while block := os.read(descriptors[path], 4 << 20):
                chunks.append(block)
            result[path] = b"".join(chunks)
        if hook is not None:
            hook()
        for path in ordered:
            need(fingerprint(before[path]) == fingerprint(os.fstat(descriptors[path])) ==
                 fingerprint(os.stat(path, follow_symlinks=False)), "TOCTOU:" + str(path))
        return result
    finally:
        for descriptor in descriptors.values():
            os.close(descriptor)


def closed_result(raw: bytes, file_pin: str, object_pin: str, label: str) -> dict[str, Any]:
    need(hashlib.sha256(raw).hexdigest() == file_pin, label + " file pin")
    # The frozen chain contains both canonical compact JSON and pretty-printed
    # closed JSON.  Exact file pins bind the byte representation; the separate
    # object closure below binds the semantic representation.
    value = parse(raw, label, canonical_required=False)
    need(type(value) is dict and value.get("object_sha256") == object_pin,
         label + " object claim")
    body = copy.deepcopy(value)
    body.pop("object_sha256")
    need(digest(body) == object_pin, label + " object closure")
    return value


def ledger_rows(raw: bytes, descriptor: dict[str, Any], file_pin: str,
                label: str) -> list[dict[str, Any]]:
    need(hashlib.sha256(raw).hexdigest() == descriptor.get("sha256") == file_pin,
         label + " file pin")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    expanded = decoder.decompress(raw, 768 << 20) + decoder.flush()
    need(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
         label + " exactly one gzip member")
    lines = expanded.splitlines(keepends=True)
    need(len(lines) == descriptor.get("row_count"), label + " row count")
    sequence = hashlib.sha256()
    rows: list[dict[str, Any]] = []
    for line in lines:
        row = parse(line, label + " row", canonical_required=True)
        need(type(row) is dict and HEX64.fullmatch(str(row.get("row_sha256"))) is not None,
             label + " row claim")
        body = copy.deepcopy(row)
        claim = body.pop("row_sha256")
        need(digest(body) == claim, label + " row closure")
        sequence.update((claim + "\n").encode("ascii"))
        rows.append(row)
    need(sequence.hexdigest() == descriptor.get("row_hash_line_sequence_sha256"),
         label + " row sequence")
    return rows


def q(value: Any) -> Fraction:
    return Fraction(str(value))


def prefix_free(paths: list[str]) -> bool:
    ordered = sorted(paths, key=lambda value: (len(value), value))
    return all(not later.startswith(first) for index, first in enumerate(ordered)
               for later in ordered[index + 1:])


def assignment_preimage(source_sha: str, path: str) -> bytes:
    need(HEX64.fullmatch(source_sha) is not None and len(path) == 21 and
         set(path) <= {"0", "1"}, "assignment source/path")
    return canonical({"assignment_domain": DOMAIN, "path": path,
                      "source_C61_aggregate_leaf_row_sha256": source_sha})


def preexec_manifest(raw: bytes) -> None:
    need(hashlib.sha256(raw).hexdigest() == PIN["preexec_manifest_file"],
         "preexec manifest file pin")
    observed: dict[str, str] = {}
    for line in raw.decode("ascii", "strict").splitlines():
        fields = line.split("  ", 1)
        need(len(fields) == 2 and HEX64.fullmatch(fields[0]) is not None and
             fields[1] not in observed, "preexec manifest syntax/uniqueness")
        observed[fields[1]] = fields[0]
    need(observed == PREEXEC_MEMBERS, "preexec exact membership")
    for name, claim in observed.items():
        need(hashlib.sha256(capture((OUT / name,))[OUT / name]).hexdigest() == claim,
             "preexec member pin:" + name)


def executor_independence(raw: bytes) -> dict[str, Any]:
    need(hashlib.sha256(raw).hexdigest() == PIN["executor_file"], "executor source pin")
    tree = ast.parse(raw.decode("utf-8", "strict"), filename=EXECUTOR.name)
    functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    attributes = {node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)}
    calls = {node.func.attr if isinstance(node.func, ast.Attribute) else
             (node.func.id if isinstance(node.func, ast.Name) else "")
             for node in ast.walk(tree) if isinstance(node, ast.Call)}
    text = raw.decode("utf-8")
    need("write_bytes" not in attributes and "write_text" not in attributes and
         "exists" not in attributes and "is_symlink" not in attributes,
         "executor unsafe path APIs absent")
    need("make_inventory" not in functions and "contract_check" not in functions and
         "authorized_inputs" in functions and "smoke" in functions and "run_shard" in functions,
         "executor v3 function boundary")
    need("O_EXCL" in text and "O_NOFOLLOW" in text and "dir_fd=" in text and
         "fstat" in calls and "fsync" in calls and
         "_leaf_ledger_v3.jsonl.gz" in text and "_receipt_v3.json" in text,
         "executor atomic explicit-v3 output protocol")
    need(EXECUTOR.stem not in sys.modules, "executor not imported")
    return {"executor_file_sha256": PIN["executor_file"],
            "executor_consumed_as_pinned_inert_bytes_and_AST_only": True,
            "executor_imported": False, "executor_executed": False,
            "atomic_no_replace_AST": True}


def authority_snapshot(raw: dict[Path, bytes]) -> dict[str, str]:
    return {
        "C50d_global_claim": hashlib.sha256(raw[GLOBAL_CLAIM]).hexdigest(),
        "C50d_global_head": hashlib.sha256(raw[GLOBAL_HEAD]).hexdigest(),
        "C53_audit_token": hashlib.sha256(raw[C53_AUDIT_TOKEN]).hexdigest(),
        "C53_successor_token": hashlib.sha256(raw[C53_TOKEN]).hexdigest(),
        "CM2_LATEST_STATUS.md": hashlib.sha256(raw[CANONICAL]).hexdigest(),
        "CM2_LATEST_STATUS.sha256": hashlib.sha256(raw[CANONICAL_COMPANION]).hexdigest(),
    }


def numeric_context() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]],
                               dict[str, dict[str, Any]], dict[str, Any]]:
    need(hashlib.sha256(Path(c41a.__file__).read_bytes()).hexdigest() ==
         PIN["C41_independent_auditor_file"], "C41 independent auditor source pin")
    c41a.source_pins()
    need(hashlib.sha256((C40 / "result.json").read_bytes()).hexdigest() ==
         PIN["C40_result_file"], "C40 result file pin")
    c40_result = c41a.c40a.pinned_result(C40, PIN["C40_object"], "C40 result")
    authority = c40_result["C39_authority"]
    c39_path = (ROOT / authority["path"]).resolve()
    c39_audit = (ROOT / authority["independent_audit_path"]).resolve()
    c39_result, _audit, _rows, _parents = c41a.c40a.load_c39_authority(c39_path, c39_audit)
    c38_index, cells, config = c41a.c40a.load_geometry_authority(c39_result)
    config["cores"] = tuple(c41a.round139.lower.core_cert.physical_cores())
    sources = c41a.c40a.pinned_ledger(C40, c40_result, "routed_leaf_cells",
                                      "C40 routed leaves")
    need(len(sources) == 35009 and len({row["row_sha256"] for row in sources}) == 35009,
         "C40 source census/uniqueness")
    c41a.install_complete_cache()
    return sources, c38_index, cells, config


def reconstruct(assigned: list[dict[str, Any]], sources_by_hash: dict[str, dict[str, Any]],
                c58_by_hash: dict[str, dict[str, Any]]) -> tuple[
                    list[dict[str, Any]], Counter[str], int, list[dict[str, Any]], int
                ]:
    c40_rows, c38_index, cells, config = numeric_context()
    c40_index = {row["row_sha256"]: (ordinal, row)
                 for ordinal, row in enumerate(c40_rows)}
    expected: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    raw_census: Counter[str] = Counter()
    route_count = 0
    whole_terminal = 0
    for assignment in assigned:
        source = sources_by_hash[assignment["source_C61_aggregate_leaf_row_sha256"]]
        c58_source = c58_by_hash[source["source_C58_leaf_row_sha256"]]
        c40_ordinal, c40_source = c40_index[c58_source["C40_source_row_sha256"]]
        task = c41a.task_for_source(c40_ordinal, c40_source, c38_index, cells,
                                    config["source_chart_seams"])
        stack: list[tuple[str, int, Fraction]] = [
            (source["path"], 0, q(source["parent_volume_fraction"]))
        ]
        final: list[dict[str, Any]] = []
        while stack:
            path, depth, volume = stack.pop()
            route = c41a.independent_route_at_path(task, path, config)
            route_count += 1
            family = c41a.disposition_family(route["classification"])
            if family == "RESIDUAL_OUTER" and depth < ADDITIONAL_DEPTH:
                stack.append((path + "1", depth + 1, volume / 2))
                stack.append((path + "0", depth + 1, volume / 2))
                continue
            if family == "TERMINAL_EXCLUDED":
                disposition = "STRICT_TERMINAL"
                next_collision = None
            elif family == "COLLISION3_READY":
                disposition = "COLLISION3_READY"
                next_collision = 3
            else:
                disposition = "COLLISION2_HANDOFF"
                next_collision = 2
            raw_census[route["classification"]] += 1
            exact_box = c41a.box_payload(route["box"])
            reflected = c41a.reflected_box(
                task["c38_source"]["representative_origin_key"], route["box"])
            continuation: dict[str, Any] | None = None
            if next_collision is not None:
                continuation = {
                    "next_collision_index": next_collision,
                    "prior_C61_aggregate_leaf_row_sha256": source["row_sha256"],
                    "prior_C61_shard_row_sha256": source["source_shard_row_sha256"],
                    "prior_C61_continuation_object_sha256":
                        source["continuation"]["continuation_object_sha256"],
                    "prior_C58_leaf_row_sha256": c58_source["row_sha256"],
                    "prior_C58_handoff_object_sha256":
                        c58_source["collision2_handoff"]["handoff_object_sha256"],
                    "collision1_history_row_sha256":
                        source["continuation"]["collision1_history_row_sha256"],
                    "collision1_original_owner": source["continuation"]["collision1_original_owner"],
                    "collision1_event_order": source["continuation"]["collision1_event_order"],
                    "exact_representative_box": exact_box,
                    "exact_reflected_box": reflected,
                    "route_classification": route["classification"],
                    "route_witness": route["witness"],
                    "route_method": route["route_method"],
                    "continuation_credit": 0,
                }
                continuation["continuation_object_sha256"] = digest(continuation)
            body = {
                "schema": CORE_SCHEMA + ".shard-leaf-row", "shard_id": SHARD,
                "assignment_preimage_sha256": assignment["assignment_preimage_sha256"],
                "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
                "source_C61_shard_row_sha256": source["source_shard_row_sha256"],
                "source_C58_leaf_row_sha256": c58_source["row_sha256"],
                "source_handoff_ordinal": source["source_handoff_ordinal"],
                "C58_source_path": source["source_path"], "source_path": source["path"],
                "path": path, "additional_depth_from_C61": depth,
                "nominal_additional_depth_from_C58":
                    source["additional_depth_from_C58"] + depth,
                "pair_index": source["pair_index"], "parent_volume_fraction": str(volume),
                "exact_representative_box": exact_box, "exact_reflected_box": reflected,
                "route_classification": route["classification"],
                "route_witness": route["witness"], "route_method": route["route_method"],
                "disposition": disposition, "continuation": continuation,
                "local_terminal_credit": 1 if disposition == "STRICT_TERMINAL" else 0,
                "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
            }
            row = {**body, "row_sha256": digest(body)}
            final.append(row)
            expected.append(row)
        paths = [row["path"] for row in final]
        need(prefix_free(paths) and
             sum(q(row["parent_volume_fraction"]) for row in final) ==
             q(source["parent_volume_fraction"]), "per-source prefix/Kraft")
        if all(row["disposition"] == "STRICT_TERMINAL" for row in final):
            whole_terminal += 1
        summaries.append({
            "assignment_preimage_sha256": assignment["assignment_preimage_sha256"],
            "source_C61_aggregate_leaf_row_sha256": source["row_sha256"],
            "source_output_row_count": len(final),
            "source_output_row_hash_line_sequence_sha256": hashlib.sha256(
                "".join(row["row_sha256"] + "\n" for row in final).encode("ascii")).hexdigest(),
            "source_Kraft_conservation": source["parent_volume_fraction"],
            "source_prefix_free": True,
        })
    return expected, raw_census, route_count, summaries, whole_terminal


def core_paths() -> tuple[Path, ...]:
    return (EXECUTOR, PREEXEC_MANIFEST, CONTRACT, ASSIGNMENT, INVENTORY, AUTHORIZATION,
            C61_RESULT, C61_LEAVES, C58_RESULT, C58_LEAVES, LEDGER, RECEIPT,
            CANONICAL, CANONICAL_COMPANION, GLOBAL_HEAD, GLOBAL_CLAIM,
            C53_TOKEN, C53_AUDIT_TOKEN)


def verify() -> dict[str, Any]:
    raw = capture(core_paths())
    independence = executor_independence(raw[EXECUTOR])
    preexec_manifest(raw[PREEXEC_MANIFEST])
    contract = closed_result(raw[CONTRACT], PIN["contract_file"], PIN["contract_object"],
                             "contract")
    assignment = closed_result(raw[ASSIGNMENT], PIN["assignment_file"],
                               PIN["assignment_object"], "assignment")
    authorization = closed_result(raw[AUTHORIZATION], PIN["authorization_file"],
                                  PIN["authorization_object"], "authorization")
    receipt = closed_result(raw[RECEIPT], PIN["receipt_file"], PIN["receipt_object"],
                            "shard00 receipt")
    c61_result = closed_result(raw[C61_RESULT], PIN["C61_result_file"],
                               PIN["C61_result_object"], "C61 result")
    c61_rows = ledger_rows(raw[C61_LEAVES], c61_result["ledgers"]["aggregate_leaves"],
                           PIN["C61_leaf_file"], "C61 leaves")
    residuals = [row for row in c61_rows if row["disposition"] == "COLLISION2_HANDOFF"]
    residual_by_hash = {row["row_sha256"]: row for row in residuals}
    need(len(residuals) == len(residual_by_hash) == contract["selection"]["exact_count"] == 20879,
         "C61 exact residual census")
    inventory = ledger_rows(raw[INVENTORY], assignment["inventory"], PIN["inventory_file"],
                            "assignment inventory")
    need(len(inventory) == 20879 and assignment["per_shard_input_counts"]["0"] == 330 and
         authorization["assignment"]["per_shard_input_counts"]["0"] == 330,
         "assignment shard0 census")
    assigned = [row for row in inventory if row["shard_id"] == SHARD]
    need(len(assigned) == 330 and len({row["source_C61_aggregate_leaf_row_sha256"]
                                      for row in assigned}) == 330,
         "330 unique shard0 assignments")
    assignment_sequence = hashlib.sha256()
    for row in assigned:
        source = residual_by_hash[row["source_C61_aggregate_leaf_row_sha256"]]
        claim = hashlib.sha256(assignment_preimage(source["row_sha256"], source["path"])).hexdigest()
        need(int(claim, 16) % SHARD_COUNT == SHARD and
             row["assignment_preimage_sha256"] == claim and row["path"] == source["path"] and
             row["pair_index"] == source["pair_index"] and
             row["source_C61_continuation_object_sha256"] ==
             source["continuation"]["continuation_object_sha256"] and
             row["source_C61_next_collision_index"] == 2 and
             row["assignment_credit"] == row["formal_credit"] ==
             row["whole_parent_credit"] == row["D02_gate_credit"] == 0,
             "exact shard0 assignment/source binding")
        assignment_sequence.update((claim + "\n").encode("ascii"))
    c58_result = closed_result(raw[C58_RESULT], PIN["C58_result_file"],
                               PIN["C58_result_object"], "C58 result")
    c58_rows = ledger_rows(raw[C58_LEAVES], c58_result["ledgers"]["leaves"],
                           PIN["C58_leaf_file"], "C58 leaves")
    c58_by_hash = {row["row_sha256"]: row for row in c58_rows}
    need(len(c58_by_hash) == len(c58_rows), "C58 identities unique")

    expected, raw_census, route_count, summaries, whole_terminal = reconstruct(
        assigned, residual_by_hash, c58_by_hash)
    observed = ledger_rows(raw[LEDGER], receipt["output_ledger"], PIN["ledger_file"],
                           "shard00 output")
    need(expected == observed, "all exact independent shard00 output rows")
    dispositions = Counter(row["disposition"] for row in expected)
    need(receipt["schema"] == CORE_SCHEMA + ".shard-receipt" and
         receipt["status"] == "PASS_COMPLETE_NO_REPLACE_DEPTH18_SHARD__ZERO_CREDIT" and
         receipt["runner_file_sha256"] == PIN["executor_file"] and
         receipt["shard_id"] == SHARD and receipt["shard_count"] == SHARD_COUNT and
         receipt["additional_binary_depth"] == ADDITIONAL_DEPTH and
         receipt["assignment_contract_file_sha256"] == PIN["contract_file"] and
         receipt["assignment_contract_object_sha256"] == PIN["contract_object"] and
         receipt["assignment_authorization_file_sha256"] == PIN["authorization_file"] and
         receipt["assignment_authorization_object_sha256"] == PIN["authorization_object"] and
         receipt["assignment_result_file_sha256"] == PIN["assignment_file"] and
         receipt["assignment_result_object_sha256"] == PIN["assignment_object"] and
         receipt["assignment_inventory_sha256"] == PIN["inventory_file"] and
         receipt["assigned_input_count"] == 330 and
         receipt["ordered_assignment_preimage_sha256_line_sequence_sha256"] ==
         assignment_sequence.hexdigest() and receipt["input_assignment_rows"] == summaries and
         receipt["route_evaluation_count"] == route_count and
         receipt["output_disposition_census"] == {
             "STRICT_TERMINAL": dispositions["STRICT_TERMINAL"],
             "COLLISION3_READY": dispositions["COLLISION3_READY"],
             "COLLISION2_HANDOFF": dispositions["COLLISION2_HANDOFF"],
         } and receipt["raw_classification_census"] == dict(sorted(raw_census.items())) and
         receipt["shard_complete"] is True and
         receipt["partial_statistics_are_formal_credit"] is False and
         receipt["formal_credit"] == receipt["whole_parent_credit"] ==
         receipt["D02_gate_credit"] == 0 and
         receipt["runtime_canonical_pointer_or_seal_writes"] is False,
         "exact reconstructed receipt")

    expected_authority = {
        "C50d_global_claim": PIN["global_claim_file"],
        "C50d_global_head": PIN["global_head_file"],
        "C53_audit_token": PIN["C53_audit_token_file"],
        "C53_successor_token": PIN["C53_token_file"],
        "CM2_LATEST_STATUS.md": PIN["canonical_file"],
        "CM2_LATEST_STATUS.sha256": PIN["canonical_companion_file"],
    }
    current_authority = authority_snapshot(raw)
    need(current_authority == expected_authority and
         receipt["authority_snapshot_before"] == receipt["authority_snapshot_after"] ==
         current_authority and receipt["authority_snapshot_object_sha256"] ==
         digest(current_authority), "authority/canonical snapshot unchanged")
    need(all(row["formal_credit"] == row["whole_parent_credit"] ==
             row["D02_gate_credit"] == 0 for row in expected) and
         all(row["continuation"] is None or row["continuation"]["continuation_credit"] == 0
             for row in expected), "all output credit locks zero")

    return close({
        "schema": SCHEMA + ".verification",
        "status": "PASS_COLD_NO_EXECUTOR_IMPORT_EXACT_SHARD00_REPLAY__330_INPUTS__PREFIX_KRAFT__AUTHORITY_UNCHANGED__ZERO_CREDIT",
        "frozen_execution_chain": {
            "executor_file_sha256": PIN["executor_file"],
            "preexecution_manifest_sha256": PIN["preexec_manifest_file"],
            "assignment_result_object_sha256": PIN["assignment_object"],
            "assignment_inventory_sha256": PIN["inventory_file"],
            "authorization_object_sha256": PIN["authorization_object"],
            "receipt_file_sha256": PIN["receipt_file"],
            "receipt_object_sha256": PIN["receipt_object"],
            "output_ledger_sha256": PIN["ledger_file"],
        },
        "coverage": {
            "assigned_inputs": 330, "independent_route_evaluations": route_count,
            "output_leaf_rows": len(expected),
            "strict_terminal_leaves": dispositions["STRICT_TERMINAL"],
            "collision3_ready_leaves": dispositions["COLLISION3_READY"],
            "collision2_handoff_leaves": dispositions["COLLISION2_HANDOFF"],
            "whole_input_handoffs_terminal": whole_terminal,
            "source_partitions_prefix_free_and_Kraft_conserved": 330,
        },
        "raw_classification_census": dict(sorted(raw_census.items())),
        "reconstructed_invariants": {
            "all_330_assignment_source_bindings_exact": True,
            "all_numeric_routes_boxes_witnesses_methods_and_dispositions_exact": True,
            "all_output_row_hashes_and_line_sequence_exact": True,
            "all_330_source_partitions_prefix_free_and_Kraft_conserved": True,
            "receipt_object_and_all_census_fields_exact": True,
            "no_replace_output_protocol_AST_verified": True,
            "authority_and_canonical_snapshots_unchanged": True,
        },
        "partial_shard_is_aggregate": False, "candidate_is_authority": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
        "independence": independence,
    })


def synthetic(receipt: dict[str, Any]) -> dict[str, Any]:
    return close({
        "schema": "synthetic.c65s18.shard00", "shard": receipt["shard_id"],
        "inputs": receipt["assigned_input_count"],
        "routes": receipt["route_evaluation_count"],
        "outputs": receipt["output_ledger"]["row_count"],
        "terminal": receipt["output_disposition_census"]["STRICT_TERMINAL"],
        "C3": receipt["output_disposition_census"]["COLLISION3_READY"],
        "C2": receipt["output_disposition_census"]["COLLISION2_HANDOFF"],
        "prefix_free": True, "Kraft": True, "row_hashes": True,
        "receipt_closed": True, "executor_bound": True, "assignment_bound": True,
        "authority_unchanged": True, "partial_is_aggregate": False,
        "formal_credit": 0, "whole_parent_credit": 0, "D02_gate_credit": 0,
    })


def validate_synthetic(value: dict[str, Any], baseline: dict[str, Any]) -> None:
    need(type(value) is dict and set(value) == set(baseline), "synthetic closed schema")
    body = copy.deepcopy(value)
    claim = body.pop("object_sha256", None)
    need(claim == digest(body) and value == baseline, "synthetic exact baseline")


def self_test() -> dict[str, Any]:
    raw = capture((RECEIPT, EXECUTOR))
    receipt = closed_result(raw[RECEIPT], PIN["receipt_file"], PIN["receipt_object"],
                            "selftest receipt")
    executor_independence(raw[EXECUTOR])
    baseline = synthetic(receipt)
    validate_synthetic(baseline, baseline)
    tests: dict[str, bool] = {"baseline_valid": True}
    mutations: list[tuple[str, Any]] = [
        ("shard", 1), ("inputs", 329), ("routes", receipt["route_evaluation_count"] - 1),
        ("outputs", receipt["output_ledger"]["row_count"] - 1),
        ("terminal", receipt["output_disposition_census"]["STRICT_TERMINAL"] + 1),
        ("C3", receipt["output_disposition_census"]["COLLISION3_READY"] + 1),
        ("C2", receipt["output_disposition_census"]["COLLISION2_HANDOFF"] - 1),
        ("prefix_free", False), ("Kraft", False), ("row_hashes", False),
        ("receipt_closed", False), ("executor_bound", False), ("assignment_bound", False),
        ("authority_unchanged", False), ("partial_is_aggregate", True),
        ("formal_credit", 1), ("whole_parent_credit", 1), ("D02_gate_credit", 1),
    ]
    for field, replacement in mutations:
        attacked = copy.deepcopy(baseline)
        attacked.pop("object_sha256")
        attacked[field] = replacement
        attacked = close(attacked)
        try:
            validate_synthetic(attacked, baseline)
        except Rejected:
            tests["coherent_" + field + "_rejected"] = True
    malformed = (
        ("duplicate_key", b'{"a":1,"a":2}\n'),
        ("NaN", b'{"a":NaN}\n'),
        ("Infinity", b'{"a":Infinity}\n'),
        ("BOM", b'\xef\xbb\xbf{"a":1}\n'),
        ("trailing", b'{"a":1}\nX'),
    )
    for name, value in malformed:
        try:
            parse(value, name, canonical_required=True)
        except (Rejected, ValueError):
            tests[name + "_rejected"] = True
    try:
        ledger_rows(b"\x1f\x8b", {"sha256": hashlib.sha256(b"\x1f\x8b").hexdigest(),
                                   "row_count": 0, "row_hash_line_sequence_sha256": "0" * 64},
                    hashlib.sha256(b"\x1f\x8b").hexdigest(), "truncated")
    except (Rejected, zlib.error):
        tests["truncated_gzip_rejected"] = True
    with tempfile.TemporaryDirectory(prefix="cm2-c65-shard00-cold-") as temporary:
        root = Path(temporary)
        target = root / "target"
        target.write_bytes(canonical(baseline) + b"\n")
        link = root / "link"
        link.symlink_to(target.name)
        try:
            capture((link,))
        except OSError:
            tests["symlink_rejected"] = True
        hard = root / "hard"
        os.link(target, hard)
        try:
            capture((target,))
        except Rejected:
            tests["hardlink_rejected"] = True
        hard.unlink()
        replacement = root / "replacement"
        replacement.write_bytes(canonical(baseline) + b"\n")
        try:
            capture((target,), hook=lambda: os.replace(replacement, target))
        except Rejected:
            tests["TOCTOU_replacement_rejected"] = True
    tests["executor_not_imported_or_executed"] = not executor_independence(raw[EXECUTOR])[
        "executor_imported"]
    tests["receipt_and_ledger_pins_are_concrete"] = all(
        HEX64.fullmatch(PIN[key]) is not None
        for key in ("receipt_file", "receipt_object", "ledger_file")
    )
    need(len(tests) == 30 and all(tests.values()), "30/30 hostile tests")
    return close({
        "schema": SCHEMA + ".self-test",
        "status": "PASS_30_OF_30_EXECUTED_COHERENT_HOSTILE_TESTS",
        "tests": tests, "test_count": 30,
        "synthetic_is_authority": False, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0,
        "runtime_canonical_pointer_or_seal_writes": False,
    })


def publish(path: Path, value: dict[str, Any]) -> None:
    raw = canonical(value) + b"\n"
    directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path.name, flags, 0o644, dir_fd=directory)
        try:
            view = memoryview(raw)
            while view:
                count = os.write(descriptor, view)
                need(count > 0, "short output write")
                view = view[count:]
            os.fsync(descriptor)
            state = os.fstat(descriptor)
            need(stat.S_ISREG(state.st_mode) and state.st_nlink == 1 and
                 fingerprint(state) == fingerprint(os.stat(path.name, dir_fd=directory,
                                                            follow_symlinks=False)),
                 "output fd/path identity")
            os.lseek(descriptor, 0, os.SEEK_SET)
            replay = b""
            while block := os.read(descriptor, 1 << 20):
                replay += block
            need(replay == raw, "output byte replay")
            os.fsync(directory)
        finally:
            os.close(descriptor)
    finally:
        os.close(directory)


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        value = verify() if args.verify else self_test()
        publish(VERIFY_OUT if args.verify else SELFTEST_OUT, value)
        print(json.dumps({"status": value["status"], "object_sha256": value["object_sha256"]},
                         sort_keys=True, separators=(",", ":")))
        return 0
    except (Rejected, c41a.Reject, OSError, KeyError, TypeError, ValueError, zlib.error) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)},
                         sort_keys=True, separators=(",", ":")))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
