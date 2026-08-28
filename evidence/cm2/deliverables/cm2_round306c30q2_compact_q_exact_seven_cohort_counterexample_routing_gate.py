#!/usr/bin/env python3
"""Route the frozen C30q1-v3 census into seven exact zero-credit cohorts.

This gate rebuilds the complete 54-origin/844-root C30q1-v3 result, requires
byte equality with its frozen two-seed audit output, and derives an exhaustive
disjoint routing ledger.  It is diagnostic research only: a routing PASS does
not prove a whole-origin theorem, establish a first owner, mint formal credit,
or authorize a seal.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


sys.dont_write_bytecode = True

from flint import ctx


HERE = Path(__file__).absolute().parent
WORKSPACE = HERE.parent
Q1_SOURCE = (
    HERE
    / "cm2_round306c30q1_compact_q_54_origin_analytic_cohort_"
      "counterexample_gate_v3.py"
)
Q1_SOURCE_SHA256 = (
    "fe737101dfc88c115e5bed5298e640bc3995bcdf52510c0c25202c252fbe10ef"
)
Q1_RESULT_SHA256 = (
    "be0f4505f333e35aa3148c9ddccabc5e41fe145b790eb67b57add82ec65e54c3"
)
Q1_STDOUT_SHA256 = (
    "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574"
)
Q1_NORMALIZED_SEMANTIC_SHA256 = (
    "b489ab6ff6d09c4422059eb1ca11e023325389bec5a0592e831ac9ae8f5a2ee5"
)
Q1_FROZEN_DIRECT_INPUT_CAPTURE_SHA256 = (
    "23dc229aaeeb7dcf3a8572744ec73b4dfbc86e2952a160735087cb1160d25a9b"
)
Q1_AUDIT = (
    WORKSPACE / ".cm2-runtime/audit/"
    "c30q1-cohort-counterexample-v3-20260807T1205"
)
SCHEMA = "cm2.round306c30q2.compact-q-exact-seven-cohort-routing-gate.v1"

SEED_FINGERPRINTS = {
    "30630071": -3086663661018055712,
    "30630929": 1060284294658223278,
}

AUDIT_FILES = {
    "commands.txt": (308, "5f40d2fe240ed3dcf8b031cee9451bd807ceac071414db59249f665d29c0c52b"),
    "compare.txt": (20, "a1235d92f43e199b661c2ce2df82c1701b0bc3b41c65dcd32529bfc8e6a2e3ff"),
    "end_utc.txt": (21, "6d9f5576cb384dd4183585c9dae678cfe743e7e8996065e8afee9ebe0426e123"),
    "post.sha256": (3263, "bd7688625d0e05e60e7380811044ae6c737b2423b298db94d52c04879fd3f00f"),
    "post.stat": (3559, "98da954a25ea604a0d4e23e2ac71de8d3f8bc177dfb06e7d85a9901956cff877"),
    "pre.sha256": (3263, "bd7688625d0e05e60e7380811044ae6c737b2423b298db94d52c04879fd3f00f"),
    "pre.stat": (3559, "98da954a25ea604a0d4e23e2ac71de8d3f8bc177dfb06e7d85a9901956cff877"),
    "provenance.json": (333, "63ee3a96b85ea0466991a263040340e9ad6ad7772a025654f8e25088867d708b"),
    "run.sh": (3505, "13d1d76ea128bbae19f4191b9c07619289985f2e26317da864984e5adf2ee877"),
    "seed30630071_exit_code.txt": (2, "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"),
    "seed30630071_stderr.log": (362, "91b2592bdb84c39a0fde3fadc2bea4ce734e617170956375cfab989b4dc092c6"),
    "seed30630071_stdout.json": (14806441, Q1_STDOUT_SHA256),
    "seed30630071_time.txt": (1062, "407f474002bea901f98ec6c743d1d093d962e7d0a423cfda25589496bd12818c"),
    "seed30630929_exit_code.txt": (2, "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"),
    "seed30630929_stderr.log": (362, "91b2592bdb84c39a0fde3fadc2bea4ce734e617170956375cfab989b4dc092c6"),
    "seed30630929_stdout.json": (14806441, Q1_STDOUT_SHA256),
    "seed30630929_time.txt": (1062, "3f6c897c412cbcefc4302cb431602b272fca65f622e4813f60ece3b7ecd67a61"),
    "start_utc.txt": (21, "a391f734e53e8c41279769e73adb3a76d5e0c37fed5c12851867f91bcdbab57e"),
    "wrapper_exit_code.txt": (2, "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa"),
    "wrapper_pid.txt": (8, "c6f812017e03b2912eb58cdbad77ea798552d42b3b69846021cdbedcb935c166"),
}

EXPECTED_PATTERNS = {
    (10, 0, 10, 0): (
        2, "900e03a37037f5a8864341a38474747d3d11ecf4d34daa2df46f6f375b96d95f",
        20, "dc3901a9d50e9197a6abe77489e34333358d5fc8371fa0710b75db3bea0af144",
        "937492ee04af0f9f6f8db623ee51ff654d529c2cceefa7d65ecfbe76db105c31",
        "9f7408c68cdd0c66312882a5fcd610c1c6b1a877f14850e4c71560bca30d0795",
    ),
    (14, 0, 0, 0): (
        2, "27b37c7dfc3fce5f1960694f001a7bdbf2ef273a23973fe1ca074ebc9a9a3193",
        28, "698fdde5ce818786ef7a22cef255e0a96d1d7c3299aa7b04c92d882f7f0570ac",
        "3dc6e2bf410569f0b5ad562fec067d5458865f35c471dc73b5afdea73db9fe78",
        "8dff270cc3dc906635b873db7962014ae43e8b6b232a62801976fa04f1da63da",
    ),
    (14, 0, 14, 0): (
        2, "a997196fcca01fd7cc8cbcd5b8e31456533ee4df99f644fed14d878acf97b1c2",
        28, "1000d988e06ed213fe823e88e00742db19da7e274ed553f96b1a685baf8e6dd4",
        "06b8f1cddfa49a98cdb21733a5ad2cee12d33b6bc77e11ecc30c9d936591b2c2",
        "ca32fb0ed7eb3f655e15b7c901702112b459b471c56147879ae9d78cf889f491",
    ),
    (16, 0, 0, 0): (
        16, "2edd9793b369ddf69e40950ec5fc7b50766002f1b3ee6dd4795db82a87378c45",
        256, "3ac1897b85df13e893da9beb78969affdd365227348716ad6817e8e428035294",
        "a7df6dad3241ff66b63799dad5b848294243d35ecfa625d8fe98daad0b8b5a97",
        "e18b99a31c32f52b4b201e1d2fb2fe317f8d28b53c9801b2e046627fe14d6c57",
    ),
    (16, 0, 16, 0): (
        24, "32d3d5e6e6f88b187e41a99df7027ccaa6ab4b0e1b4ba25c997f2e87e2baed76",
        384, "c0c8dffa49c735cc36695f776d5366d525117046a1d2397242439949e41a1295",
        "ccc2f8ae9ec61e4cc7f15095a0a34eb48c5f50dacdd5d8fcc2ea191c84da7072",
        "0d079767dc3e2f488f7dbca6b63c980dd5b08d9105cdef850af9350db48eac27",
    ),
    (16, 4, 16, 4): (
        2, "496c22785e4af067171438642e5d22a5d41b02a8b979eed3cc26f3d6c5e655d4",
        32, "d52d478c4c98df72b1751052a647e8bab867b63d55ee39492606cf32b7e21739",
        "9ddbef83c7f5298c4444589359f9a4f3cc2d2264fd14b64cbfd7e358f8c60420",
        "d9adc361cbd293aaacbb60f4a03a2d800614580e0602569ba01638f10cd89010",
    ),
    (16, 16, 16, 16): (
        6, "1683d39992ca9a2bd2fb85bb8ed9ff1a58453cb5442522a0e943da07bd0ed491",
        96, "4f8583b19fa18a89ff69fa66f93c239f01e890f33ded574c349367b07e375149",
        "c1f0384a4e4a2185d344c4769419e661c31d347edc819ec4884958e3414ba09f",
        "3708fd9d187b7511cacc2cd0ca0dbbd647fe69a9b6012897f1eb1afe36905c93",
    ),
}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label)
            output[key] = value
        return output

    try:
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=unique,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    need(raw in {canonical(value), canonical(value) + b"\n"}, "canonical JSON:" + label)
    return value


def capture_no_follow(path: Path, label: str) -> tuple[bytes, tuple[int, ...]]:
    descriptor = os.open(
        path, os.O_RDONLY | os.O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        before = os.fstat(descriptor)
        need(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            "regular singleton:" + label,
        )
        chunks: list[bytes] = []
        while block := os.read(descriptor, 1 << 20):
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity = (
        before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
        before.st_size, before.st_mtime_ns, before.st_ctime_ns,
    )
    need(
        identity == (
            after.st_dev, after.st_ino, after.st_mode, after.st_nlink,
            after.st_size, after.st_mtime_ns, after.st_ctime_ns,
        ),
        "stable capture:" + label,
    )
    raw = b"".join(chunks)
    need(len(raw) == before.st_size, "complete capture:" + label)
    return raw, identity


def validate_seed_runtime() -> None:
    seed = os.environ.get("PYTHONHASHSEED")
    need(seed in SEED_FINGERPRINTS, "true seed selected")
    need(
        sys.flags.isolated == 0
        and sys.flags.ignore_environment == 0
        and sys.flags.hash_randomization == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.no_user_site == 1
        and sys.dont_write_bytecode is True,
        "clean non-isolated seed runtime",
    )
    need(
        hash("cm2-q2-seed-fingerprint") == SEED_FINGERPRINTS[seed],
        "active PYTHONHASHSEED fingerprint",
    )


def frozen_q1_audit() -> tuple[dict[str, Any], dict[str, str]]:
    root_status = Q1_AUDIT.lstat()
    need(
        stat.S_ISDIR(root_status.st_mode) and not Q1_AUDIT.is_symlink(),
        "frozen Q1 audit directory",
    )
    actual = {path.name for path in Q1_AUDIT.iterdir()}
    need(actual == set(AUDIT_FILES), "frozen Q1 audit exact tree")
    raws: dict[str, bytes] = {}
    identities: dict[str, tuple[int, ...]] = {}
    for name, (size, expected_hash) in AUDIT_FILES.items():
        raw, identity = capture_no_follow(Q1_AUDIT / name, "Q1 audit:" + name)
        need(
            len(raw) == size and hashlib.sha256(raw).hexdigest() == expected_hash,
            "frozen Q1 audit byte pin:" + name,
        )
        raws[name] = raw
        identities[name] = identity
    need(
        raws["pre.sha256"] == raws["post.sha256"]
        and raws["pre.stat"] == raws["post.stat"],
        "Q1 audit pre/post byte stability",
    )
    need(
        raws["compare.txt"] == b"byte_identical=true\n"
        and raws["wrapper_exit_code.txt"] == b"0\n",
        "Q1 audit wrapper success",
    )
    outputs: list[bytes] = []
    for seed in SEED_FINGERPRINTS:
        prefix = "seed" + seed
        need(raws[prefix + "_exit_code.txt"] == b"0\n", "Q1 seed exit:" + seed)
        timing = raws[prefix + "_time.txt"]
        need(
            b"Command terminated by signal" not in timing
            and timing.decode("utf-8").splitlines()[-1] == "\tExit status: 0",
            "Q1 seed unsignalled GNU time success:" + seed,
        )
        outputs.append(raws[prefix + "_stdout.json"])
    need(outputs[0] == outputs[1], "Q1 true-seed byte equality")
    document = strict_json(outputs[0], "Q1 v3 frozen output")
    need(
        document.get("schema")
        == "cm2.round306c30q1.compact-q-54-origin-analytic-cohort-counterexample-gate.v3"
        and set(document) == {"schema", "result", "result_sha256"}
        and type(document.get("result")) is dict
        and document.get("result_sha256") == Q1_RESULT_SHA256
        and digest(document["result"]) == Q1_RESULT_SHA256,
        "Q1 v3 frozen result closure",
    )
    for name, identity in identities.items():
        current = (Q1_AUDIT / name).lstat()
        need(
            identity == (
                current.st_dev, current.st_ino, current.st_mode, current.st_nlink,
                current.st_size, current.st_mtime_ns, current.st_ctime_ns,
            ),
            "Q1 audit stable after parse:" + name,
        )
    return document, {
        name: expected_hash for name, (_size, expected_hash) in sorted(AUDIT_FILES.items())
    }


def normalize_q1_result(
    value: dict[str, Any], label: str,
) -> tuple[dict[str, Any], str]:
    copied = strict_json(canonical(value), label)
    frozen_inputs = copied.get("frozen_inputs")
    need(type(frozen_inputs) is dict, "Q1 frozen inputs:" + label)
    volatile = frozen_inputs.pop("direct_input_capture_sha256", None)
    need(
        type(volatile) is str and len(volatile) == 64
        and all(character in "0123456789abcdef" for character in volatile)
        and frozen_inputs.get(
            "all_direct_inputs_single_capture_and_ancestor_chain_stable"
        ) is True,
        "Q1 direct capture provenance:" + label,
    )
    return copied, volatile


def load_and_rebuild_q1() -> tuple[dict[str, Any], str, str]:
    source_before, identity_before = capture_no_follow(Q1_SOURCE, "Q1 v3 source")
    need(
        hashlib.sha256(source_before).hexdigest() == Q1_SOURCE_SHA256,
        "Q1 v3 source hash pin",
    )
    if os.fspath(HERE) not in sys.path:
        sys.path.insert(0, os.fspath(HERE))
    module_name = "cm2_c30q1_v3_frozen_for_q2"
    specification = importlib.util.spec_from_file_location(module_name, Q1_SOURCE)
    need(
        specification is not None and specification.loader is not None,
        "Q1 v3 module specification",
    )
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    need(Path(module.__file__).absolute() == Q1_SOURCE, "Q1 v3 module identity")
    rebuilt = module.rebuild()
    source_after, identity_after = capture_no_follow(Q1_SOURCE, "Q1 v3 source post")
    need(
        source_before == source_after
        and identity_before == identity_after
        and hashlib.sha256(source_after).hexdigest() == Q1_SOURCE_SHA256,
        "Q1 v3 source stable",
    )
    need(type(rebuilt) is dict, "Q1 rebuilt result object")
    rebuilt_hash = digest(rebuilt)
    v2 = importlib.import_module(module.V2_SOURCE.stem)
    v1 = importlib.import_module(v2.V1_SOURCE.stem)
    need(Path(v1.__file__).absolute() == v2.V1_SOURCE, "Q1 v1 module identity")
    recaptured_direct = v1.digest(v1.capture_direct_pins())
    need(
        rebuilt["frozen_inputs"]["direct_input_capture_sha256"]
        == recaptured_direct,
        "Q1 rebuilt direct capture independently recaptured",
    )
    return rebuilt, rebuilt_hash, recaptured_direct


def pattern_of(origin: dict[str, Any]) -> tuple[int, int, int, int]:
    analytic = origin["analytic"]
    return (
        analytic["analytic_root_count"], analytic["applicable_root_count"],
        analytic["frozen_behind_root_count"], analytic["future_witness_root_count"],
    )


def route_name(pattern: tuple[int, int, int, int]) -> str:
    if pattern in {(14, 0, 0, 0), (16, 0, 0, 0)}:
        return "FROZEN_BEHIND_CERTIFICATE_REVERSAL_ROUTE"
    if pattern in {
        (10, 0, 10, 0), (14, 0, 14, 0),
        (16, 0, 16, 0), (16, 4, 16, 4),
    }:
        return "FUTURE_WITNESS_CERTIFICATE_GAP_ROUTE"
    need(pattern == (16, 16, 16, 16), "known routing pattern")
    return "ANALYTIC_FULL_THEN_COMPLEMENT_RESIDUAL_ROUTE"


def build_ledger(result: dict[str, Any]) -> dict[str, Any]:
    census = result["analytic_cohort_census"]
    combined = result["combined_origin_gate"]
    origin_rows = combined["origin_rows"]
    root_rows = census["root_results"]
    need(
        len(origin_rows) == combined["origin_count"] == 54
        and len(root_rows) == census["analytic_root_count"] == 844
        and census["applicable_root_count"] == 104
        and census["fully_applicable_origin_count"] == 6
        and combined["conditionally_applicable_origin_count"] == 2
        and combined["rejected_origin_count"] == 52,
        "Q1 rebuilt global census counts",
    )
    origin_by_key = {row["origin_key"]: row for row in origin_rows}
    root_by_key = {row["root_key"]: row for row in root_rows}
    need(
        len(origin_by_key) == 54 and len(root_by_key) == 844
        and {row["origin_key"] for row in root_rows} == set(origin_by_key),
        "Q1 unique origin/root keys",
    )
    grouped: dict[tuple[int, int, int, int], list[str]] = {}
    for key, row in origin_by_key.items():
        grouped.setdefault(pattern_of(row), []).append(key)
    need(set(grouped) == set(EXPECTED_PATTERNS), "seven exhaustive patterns")

    ledger: list[dict[str, Any]] = []
    all_routed_origins: list[str] = []
    all_routed_roots: list[str] = []
    for index, pattern in enumerate(sorted(grouped), 1):
        expected = EXPECTED_PATTERNS[pattern]
        origin_keys = sorted(grouped[pattern])
        origin_set = set(origin_keys)
        selected_roots = sorted(
            (row for row in root_rows if row["origin_key"] in origin_set),
            key=lambda row: row["root_key"],
        )
        root_keys = [row["root_key"] for row in selected_roots]
        parameter_hashes = sorted({digest(row["cohort_parameters"]) for row in selected_roots})
        root_bound_parameters = [
            {"root_key": row["root_key"],
             "parameters_sha256": digest(row["cohort_parameters"])}
            for row in selected_roots
        ]
        need(
            len(origin_keys) == expected[0] and digest(origin_keys) == expected[1]
            and len(root_keys) == expected[2] and digest(root_keys) == expected[3]
            and digest(parameter_hashes) == expected[4]
            and digest(root_bound_parameters) == expected[5],
            "exact cohort ledger pattern:" + repr(pattern),
        )
        analytic_count, applicable_count, frozen_count, future_count = pattern
        conditional_pass = sum(
            origin_by_key[key]["conditional_origin_applicable"] is True
            for key in origin_keys
        )
        residual_counts = sorted(
            origin_by_key[key]["complement"]["P215_residual_child_count"]
            for key in origin_keys
        )
        ledger.append({
            "cohort_index": index,
            "pattern": {
                "analytic_root_count_per_origin": analytic_count,
                "applicable_root_count_per_origin": applicable_count,
                "frozen_behind_root_count_per_origin": frozen_count,
                "future_witness_root_count_per_origin": future_count,
            },
            "route": route_name(pattern),
            "origin_count": len(origin_keys),
            "origin_keys": origin_keys,
            "origin_keys_sha256": digest(origin_keys),
            "root_count": len(root_keys),
            "root_keys": root_keys,
            "root_keys_sha256": digest(root_keys),
            "parameter_signature_count": len(parameter_hashes),
            "parameter_signature_set_sha256": digest(parameter_hashes),
            "root_bound_parameter_signatures_sha256": digest(root_bound_parameters),
            "root_failure_summary": {
                "applicability_gap_root_count": len(root_keys) - applicable_count * len(origin_keys),
                "frozen_behind_gap_root_count": len(root_keys) - frozen_count * len(origin_keys),
                "future_witness_gap_root_count": len(root_keys) - future_count * len(origin_keys),
            },
            "complement_summary": {
                "conditionally_applicable_origin_count": conditional_pass,
                "blocked_origin_count": len(origin_keys) - conditional_pass,
                "P215_residual_child_counts_sorted": residual_counts,
                "P215_residual_child_count_total": sum(residual_counts),
            },
        })
        all_routed_origins.extend(origin_keys)
        all_routed_roots.extend(root_keys)
    need(
        len(all_routed_origins) == len(set(all_routed_origins)) == 54
        and sorted(all_routed_origins) == sorted(origin_by_key)
        and len(all_routed_roots) == len(set(all_routed_roots)) == 844
        and sorted(all_routed_roots) == sorted(root_by_key),
        "seven patterns exhaustive and disjoint",
    )

    reversal = [row for row in ledger if row["route"].startswith("FROZEN")]
    future_gap = [row for row in ledger if row["route"].startswith("FUTURE")]
    analytic_full = [row for row in ledger if row["route"].startswith("ANALYTIC")]
    need(
        sum(row["origin_count"] for row in reversal) == 18
        and sum(row["root_count"] for row in reversal) == 284
        and sum(row["origin_count"] for row in future_gap) == 30
        and sum(row["root_count"] for row in future_gap) == 464
        and sum(
            row["root_count"] - row["root_failure_summary"]["future_witness_gap_root_count"]
            for row in future_gap
        ) == 8
        and sum(row["root_failure_summary"]["future_witness_gap_root_count"]
                for row in future_gap) == 456
        and len(analytic_full) == 1
        and analytic_full[0]["origin_count"] == 6
        and analytic_full[0]["root_count"] == 96
        and analytic_full[0]["complement_summary"]["conditionally_applicable_origin_count"] == 2
        and analytic_full[0]["complement_summary"]["blocked_origin_count"] == 4
        and analytic_full[0]["complement_summary"]["P215_residual_child_counts_sorted"]
        == [1, 1, 128, 128, 136, 136]
        and analytic_full[0]["complement_summary"]["P215_residual_child_count_total"] == 530,
        "primary disjoint routing totals",
    )

    north = {
        key.removeprefix("W:N:"): key for key in origin_by_key if key.startswith("W:N:")
    }
    south = {
        key.removeprefix("W:S:H."): key
        for key in origin_by_key if key.startswith("W:S:H.")
    }
    need(len(north) == len(south) == 27 and set(north) == set(south),
         "observed exact north/south key pairing")
    mirror_pairs = [
        {"suffix": suffix, "north_origin_key": north[suffix],
         "south_origin_key": south[suffix]}
        for suffix in sorted(north)
    ]
    for pair in mirror_pairs:
        need(
            pattern_of(origin_by_key[pair["north_origin_key"]])
            == pattern_of(origin_by_key[pair["south_origin_key"]]),
            "observed paired pattern equality",
        )

    boolean_counts: dict[tuple[bool, bool, bool, bool, bool], int] = {}
    for row in origin_rows:
        analytic = row["analytic"]
        complement = row["complement"]
        boolean_key = (
            analytic["frozen_behind_root_count"] == analytic["analytic_root_count"],
            analytic["future_witness_root_count"] == analytic["analytic_root_count"],
            analytic["future_witness_root_count"] > 0,
            complement["P215_residual_child_count"] > 0,
            complement["unique_compact_residual_in_exactly_one_root_box"],
        )
        boolean_counts[boolean_key] = boolean_counts.get(boolean_key, 0) + 1
    expected_boolean_counts = {
        (True, True, True, True, True): 2,
        (True, True, True, True, False): 4,
        (True, False, True, True, False): 2,
        (True, False, False, True, False): 4,
        (True, False, False, False, False): 24,
        (False, False, False, True, False): 14,
        (False, False, False, False, False): 4,
    }
    need(boolean_counts == expected_boolean_counts, "exact seven-class boolean census")
    boolean_census = [
        {
            "all_frozen": key[0], "all_future": key[1],
            "any_future": key[2], "P215_residual_positive": key[3],
            "unique_compact_residual": key[4], "origin_count": count,
        }
        for key, count in sorted(boolean_counts.items(), reverse=True)
    ]

    witness = result["exact_strict_interior_frozen_behind_reverse_parameter_witness"]
    need(
        witness["origin_key"] in origin_by_key
        and pattern_of(origin_by_key[witness["origin_key"]]) == (16, 0, 0, 0)
        and witness["root_key"] in root_by_key
        and witness["exact_parameters"]["t"] == "8673/256000"
        and witness["exact_parameters"]["s"] == "-1/800"
        and witness["exact_parameters"]["r"] == "1/2"
        and witness["exact_parameters"]["q_squared"] == "1023/1048576"
        and witness["exact_parameters"]["p_squared"] == "1047553/1048576"
        and witness["exact_frozen_forward_projection_sign_proof"]
            ["positive_term_square_minus_negative_term_square"]
        == "4185337467739/4194304000000"
        and witness["exact_frozen_forward_projection_sign_proof"]["ell_sign"]
        == "STRICT_POSITIVE"
        and witness["boundary_ownership_dependency"] is False
        and witness["scope"]
        == ("exact strict-interior parameter counterexample to the C30q0 "
            "frozen-behind sufficient subclaim only; not a CM2 counterexample "
            "and not a first-owner classification"),
        "exact frozen-behind exemplar",
    )
    return {
        "pattern_count": 7,
        "patterns": ledger,
        "totals": {
            "origin_count": 54,
            "root_count": 844,
            "applicable_root_count": 104,
            "fully_analytic_origin_count": 6,
            "final_combined_pass_origin_count": 2,
        },
        "primary_disjoint_routing": {
            "frozen_behind_certificate_reversal": {
                "origin_count": 18, "root_count": 284,
                "whole_box_arb_failures_are_physical_counterexamples": False,
                "exact_subclaim_counterexample_exemplar_count": 1,
            },
            "future_root_certificate_gap": {
                "origin_count": 30, "root_count": 464,
                "certified_root_count": 8, "gap_root_count": 456,
                "partial_pattern": [16, 4, 16, 4],
            },
            "analytic_full_then_complement_residual": {
                "origin_count": 6, "root_count": 96,
                "final_combined_pass_origin_count": 2,
                "residual_nonunique_blocked_origin_count": 4,
                "residual_child_count_total": 530,
            },
        },
        "observed_key_pairing_only": {
            "pair_count": 27,
            "pairs": mirror_pairs,
            "pairs_sha256": digest(mirror_pairs),
            "used_to_infer_unchecked_geometry": False,
        },
        "exact_boolean_census": boolean_census,
        "exact_subclaim_counterexample_exemplar": witness,
    }


def rebuild() -> dict[str, Any]:
    validate_seed_runtime()
    frozen_document, audit_hashes = frozen_q1_audit()
    rebuilt, rebuilt_hash, recaptured_direct = load_and_rebuild_q1()
    frozen_normalized, frozen_direct = normalize_q1_result(
        frozen_document["result"], "frozen Q1 result normalization"
    )
    rebuilt_normalized, rebuilt_direct = normalize_q1_result(
        rebuilt, "rebuilt Q1 result normalization"
    )
    need(
        frozen_direct == Q1_FROZEN_DIRECT_INPUT_CAPTURE_SHA256
        and rebuilt_direct == recaptured_direct
        and digest(frozen_normalized) == Q1_NORMALIZED_SEMANTIC_SHA256
        and digest(rebuilt_normalized) == Q1_NORMALIZED_SEMANTIC_SHA256
        and canonical(rebuilt_normalized) == canonical(frozen_normalized),
        "Q1 exact semantic replay after one-path provenance normalization",
    )
    ledger = build_ledger(rebuilt)
    return {
        "status": (
            "PASS_EXACT_SEVEN_COHORT_ROUTING_LEDGER__"
            "REJECT_AUTOMATIC_EXTENSION__ZERO_FORMAL_CREDIT"
        ),
        "verdict": "ROUTING_PASS__AUTOMATIC_EXTENSION_REJECTED",
        "scope": (
            "exhaustive disjoint routing of the frozen 54-origin C30q1-v3 "
            "research census; no whole-origin analytic theorem"
        ),
        "frozen_inputs": {
            "C30q1_v3_source_sha256": Q1_SOURCE_SHA256,
            "C30q1_v3_result_sha256": Q1_RESULT_SHA256,
            "C30q1_v3_current_rebuild_result_sha256": rebuilt_hash,
            "C30q1_v3_two_seed_stdout_sha256": Q1_STDOUT_SHA256,
            "C30q1_v3_audit_member_sha256": audit_hashes,
            "one_allowed_volatile_provenance_path":
                "$.frozen_inputs.direct_input_capture_sha256",
            "frozen_direct_input_capture_sha256": frozen_direct,
            "current_direct_input_capture_sha256": rebuilt_direct,
            "current_direct_input_independent_recapture_sha256": recaptured_direct,
            "normalized_semantic_result_sha256": Q1_NORMALIZED_SEMANTIC_SHA256,
            "normalized_semantic_results_byte_identical": True,
            "arbitrary_outer_digest_normalization_forbidden": True,
        },
        "runtime_seed_contract": {
            "invocation_must_not_use_python_I": True,
            "PYTHONHASHSEED_is_observed_by_runtime": True,
            "accepted_true_seed_values": sorted(SEED_FINGERPRINTS),
            "active_seed_intentionally_omitted_for_byte_identical_outputs": True,
        },
        "exact_seven_cohort_ledger": ledger,
        "certificate_logic": {
            "arb_whole_box_failure_is_only_a_coverage_obstruction": True,
            "exact_interior_witness_refutes_only_frozen_behind_sufficient_subclaim": True,
            "does_not_refute_CM2": True,
            "does_not_establish_alternative_first_owner": True,
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "source_W_formal_remaining_before": 80,
            "source_W_formal_remaining_after": 80,
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
            "seal_or_release_authority": False,
        },
        "next_falsifiable_work": (
            "prove one exact whole-origin route, including cross-root "
            "3D/2D/1D/0D half-open ownership, before extending to its cohort"
        ),
    }


def main() -> int:
    ctx.prec = 192
    try:
        result = rebuild()
        document = {"schema": SCHEMA, "result": result}
        document["result_sha256"] = digest(result)
        sys.stdout.buffer.write(canonical(document) + b"\n")
        return 0
    except (Reject, RuntimeError, OSError, ValueError, KeyError, StopIteration) as error:
        print("REJECT_C30Q2_ROUTING_INTEGRITY:" + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
