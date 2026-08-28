#!/usr/bin/env python3
"""Independent verifier for the Round147 Gate5 strict re-audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any, Callable


BASE = Path(__file__).resolve().parent
CERT_NAME = "cm2-round147-gate5-strict-reaudit-upgrade-frontier-2026-07-24.json"
DEFAULT_CERT = BASE / CERT_NAME
DEFAULT_OUTPUT = (
    BASE
    / "cm2-round147-gate5-strict-reaudit-upgrade-frontier-verification-2026-07-24.json"
)
CERT_SCHEMA = "cm2.round147.gate5-strict-reaudit-upgrade-frontier.v1"
VERIFY_SCHEMA = "cm2.round147.gate5-strict-reaudit-upgrade-frontier.verification.v1"
PRODUCER_NAME = "cm2_round147_gate5_strict_reaudit_upgrade_frontier.py"
PRODUCER_SHA256 = "0f66021bb4691e8c9b9765f3025df4b052cb9323db1a8fa94e9d0ea5b3f63619"
EXPECTED_CERT_SHA256 = "db7f1a01f36c56dc537a4873dcd232808c337298a0998608a2c34aeaaa7531ee"
EXPECTED_RESULT_SHA256 = "00649a259ff69590eed6a9f4e828b6a622c0c03deb3ca07a70526446b827e922"
EXPECTED_PINS_SHA256 = "5ae2d426643ef1f141911aec5d8491f178a6c28dd6e0eddc353bd798b5e41af9"
MAX_CERT_BYTES = 1_000_000

FIELD_NAMES = {
    1: "nonempty_or_empty_domain_proof",
    2: "physical_homogeneity_subbranch_table",
    3: "homogeneous_prefix_chart",
    4: "homogeneous_suffix_chart",
    5: "inverse_Jacobian_bound",
    6: "log_Jacobian_distortion_sum",
    7: "one_step_cut_growth_Z_sum",
    8: "face_transversality_lower",
    9: "face_C2_atlas_bound",
    10: "coarea_density_regular_bound",
    11: "dynamic_Holder_test_pullback_bound",
    12: "C1_face_trace_pullback_bound",
    13: "moving_boundary_DQ_current_and_two_traces",
    14: "regular_density_operator_cost",
    15: "standard_family_operator_cost",
    16: "flux_face_operator_cost",
    17: "dynamic_test_operator_cost",
    18: "operator_phase_block",
}
OPEN = [5, 6, 10, 11, 14, 15, 17, 18]
SATISFIED = [1, 2, 3, 4, 7, 8, 9, 12, 13, 16]
TOKEN_PATTERNS = {
    "historical_parent_W_shaped": re.compile(rb"rn-parent-W:[0-9a-f]{64}"),
    "historical_restriction_shaped": re.compile(rb"rn-restriction:[0-9a-f]{64}"),
    "v1_parent_W_shaped": re.compile(rb"rn-v1-parent-W:[0-9a-f]{64}"),
    "v1_restriction_shaped": re.compile(rb"rn-v1-restriction:[0-9a-f]{64}"),
    "round50_owner_shaped": re.compile(
        rb"(?:round50(?:-v1)?-owner|round50-owner-key):[0-9a-f]{64}"
    ),
    "round54_t54_shaped": re.compile(rb"round54(?:-v1)?-t54:[0-9a-f]{64}"),
    "round67_qj_shaped": re.compile(rb"round67(?:-v1)?-qj:[0-9a-f]{64}"),
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode), "certificate must be regular")
    require(not stat.S_ISLNK(info.st_mode), "certificate symlink forbidden")
    require(0 < info.st_size <= MAX_CERT_BYTES, "certificate size")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        raw = b""
        while True:
            chunk = os.read(fd, 65536)
            if not chunk:
                break
            raw += chunk
            require(len(raw) <= MAX_CERT_BYTES, "certificate read bound")
    finally:
        os.close(fd)
    require(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), "canonical newline")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError("UTF-8") from exc
    decoder = json.JSONDecoder()
    try:
        value, end = decoder.raw_decode(text)
    except json.JSONDecodeError as exc:
        raise VerificationError("JSON") from exc
    require(text[end:] == "\n", "trailing bytes")
    require(isinstance(value, dict), "envelope object")
    require(raw == canonical_bytes(value) + b"\n", "canonical JSON bytes")
    return value


def include_snapshot(path: Path) -> bool:
    name = path.name
    if not path.is_file() or name.startswith("."):
        return False
    if path.suffix.lower() not in {".json", ".py", ".md", ".sha256"}:
        return False
    lower = name.lower()
    if "round147" in lower:
        return False
    match = re.search(r"round(\d+)", lower)
    if match and int(match.group(1)) >= 145:
        return False
    if "one-hundred-forty-" in lower:
        return False
    return True


def independent_snapshot() -> dict[str, Any]:
    entries: list[list[Any]] = []
    hits: dict[str, dict[str, set[str]]] = {
        label: {} for label in TOKEN_PATTERNS
    }
    total = 0
    for path in sorted(BASE.iterdir(), key=lambda item: item.name):
        if not include_snapshot(path):
            continue
        raw = path.read_bytes()
        total += len(raw)
        entries.append([path.name, hashlib.sha256(raw).hexdigest(), len(raw)])
        for label, pattern in TOKEN_PATTERNS.items():
            for found in pattern.finditer(raw):
                token = found.group(0).decode("ascii")
                hits[label].setdefault(token, set()).add(path.name)
    rows = []
    for label in sorted(hits):
        for token in sorted(hits[label]):
            rows.append({
                "pattern_class": label,
                "token": token,
                "source_files": sorted(hits[label][token]),
            })
    return {
        "scope": (
            "top-level .json/.py/.md/.sha256 sealed snapshot through Round144; "
            "Round145+, Round147, dot-temporaries, and ambiguous concurrent "
            "one-hundred-forty-* prose assault files excluded"
        ),
        "file_count": len(entries),
        "total_bytes": total,
        "path_sha_size_rows_sha256": digest(entries),
        "identifier_pattern_hit_rows": rows,
        "identifier_pattern_hit_rows_sha256": digest(rows),
    }


def verify_external_inputs(result: dict[str, Any]) -> int:
    require(file_sha256(BASE / PRODUCER_NAME) == PRODUCER_SHA256, "producer pin")
    pins = result["provenance"]["strict_byte_pins"]
    require(digest(pins) == EXPECTED_PINS_SHA256, "pin-map digest")
    for name, expected in sorted(pins.items()):
        path = BASE / name
        require(path.is_file(), f"missing pinned input:{name}")
        require(file_sha256(path) == expected, f"input pin:{name}")

    snapshot = independent_snapshot()
    require(
        result["sealed_repository_search_snapshot"] == snapshot,
        "sealed repository snapshot replay",
    )

    def j(name: str) -> dict[str, Any]:
        return json.loads((BASE / name).read_text(encoding="utf-8"))["result"]

    g67 = j(
        "cm2-gate5-round67-direct-positive-potential-attenuation-frontier-"
        "manifest-2026-07-21.json"
    )
    require(
        [row["field"] for row in g67["remaining_eight_fields"]["rows"]]
        == [f"F{i}" for i in OPEN],
        "independent open-eight replay",
    )
    require(g67["strict_status"]["Gate5_maturity"] == "10/18", "input maturity")
    require(g67["strict_status"]["complete_18_field_blocks"] == 0, "input blocks")

    r130 = j(
        "cm2-round130-rank3-positive-borel-local-18-field-completion-"
        "2026-07-24.json"
    )
    require("LOCAL_18_OF_18__NO_GLOBAL_PROMOTION" in r130["status"], "R130 local")
    require(r130["global_complete_18_field_block_count"] == 0, "R130 block")

    r133 = j("cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json")
    require(r133["count_ledger"]["owner_key_count"] == 0, "R133 owner count")
    require(r133["count_ledger"]["q_j_recordwise_output_count"] == 0, "R133 qj count")

    r144 = j(
        "cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json"
    )
    require(all(x is None for x in r144["current_identifier_values"].values()), "R144 IDs")
    require(r144["first_exact_blocker"]["node_id"] == "D02", "R144 D02")
    return len(pins)


def verify_semantics(value: dict[str, Any], *, exact_hash: bool = True) -> int:
    checks = 0

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        require(condition, label)
        checks += 1

    check(set(value) == {"schema", "result", "result_sha256"}, "envelope keys")
    check(value["schema"] == CERT_SCHEMA, "schema")
    check(digest(value["result"]) == value["result_sha256"], "result digest")
    if exact_hash:
        check(value["result_sha256"] == EXPECTED_RESULT_SHA256, "sealed result hash")
    result = value["result"]
    expected_keys = {
        "status",
        "audit_date",
        "provenance",
        "sealed_repository_search_snapshot",
        "gate5_field_rows",
        "gate5_field_rows_sha256",
        "gate5_global_ledger",
        "historical_identifier_and_map_census",
        "Round142_underdetermination_pin",
        "Round144_atomic_migration_frontier",
        "executable_upgrade_frontier",
        "strict_nonclaims",
    }
    check(set(result) == expected_keys, "result keys")
    check(
        result["status"]
        == "CERTIFIED_GATE5_18_FIELD_STRICT_REAUDIT__"
        "10_SATISFIED__8_PROSPECTIVE_LOCAL_ONLY_AND_STRICTLY_BLOCKED__0_UPGRADES",
        "status",
    )
    rows = result["gate5_field_rows"]
    check(len(rows) == 18, "18 rows")
    check(result["gate5_field_rows_sha256"] == digest(rows), "row list digest")
    for offset, row in enumerate(rows, 1):
        check(row["field_index"] == offset, f"F{offset} index")
        check(row["field"] == f"F{offset}", f"F{offset} label")
        check(row["field_name"] == FIELD_NAMES[offset], f"F{offset} name")
        check(row["row_sha256"] == digest({k: v for k, v in row.items() if k != "row_sha256"}), f"F{offset} row digest")
        if offset in OPEN:
            check(row["global_credit_classification"] == "STRICTLY_BLOCKED", f"F{offset} blocked")
            check(row["global_field_credit"] is False, f"F{offset} no credit")
            check(
                row["best_available_non_global_evidence"]
                == "PROSPECTIVE_LOCAL_V1_ONLY__ROUND130_EVERY_EXACT_FIBRE",
                f"F{offset} prospective",
            )
            check(row["strict_blocker"] is not None, f"F{offset} blocker")
            check(row["minimum_closing_evidence"] is not None, f"F{offset} closer")
        else:
            check(row["global_credit_classification"] == "STRICTLY_SATISFIED", f"F{offset} satisfied")
            check(row["global_field_credit"] is True, f"F{offset} credit")
            check(row["strict_blocker"] is None, f"F{offset} no blocker")
        check(row["upgrade_credit_now"] is False, f"F{offset} no new upgrade")

    ledger = result["gate5_global_ledger"]
    check(ledger["strictly_satisfied_field_indices"] == SATISFIED, "satisfied set")
    check(ledger["strictly_blocked_field_indices"] == OPEN, "blocked set")
    check(ledger["prospective_local_v1_only_field_indices"] == OPEN, "prospective set")
    check(ledger["newly_promoted_field_indices"] == [], "no promotion")
    check(ledger["global_maturity_before"] == ledger["global_maturity_after"] == "10/18", "maturity")
    check(
        ledger["global_complete_18_field_block_count_before"]
        == ledger["global_complete_18_field_block_count_after"]
        == 0,
        "block count",
    )
    check(ledger["Gate5"] == "NOT_CERTIFIED", "Gate5")
    check(ledger["CM2"] == "NO-GO_FOR_CLAIM", "CM2")

    census = result["historical_identifier_and_map_census"]
    check(census["Round35"]["historical_parent_W_materialized_count"] == 0, "R35 W")
    check(
        census["Round35"]["historical_schema_compatible_restriction_materialized_count"]
        == 0,
        "R35 restriction",
    )
    check(
        census["Round35"]["namespace_shaped_restriction_false_positive_count"] == 1,
        "R35 false positive",
    )
    check(
        census["Round35"]["false_positive"]["identifier"]
        == "rn-restriction:8bc002c75e6ffb86a82f75a2543c3bb4dbd43feb881e3f4619d49095486918c8",
        "R70 ID",
    )
    check(census["Round50"]["recordwise_owner_key_count"] == 0, "R50 owner")
    check(census["Round50"]["complete_candidate_fibre_count"] == 0, "R50 fibre")
    check(census["Round54"]["token_schema_field_count"] == 7, "R54 schema")
    check(
        census["Round54"]["pi50_projection_schema_status"]
        == "CERTIFIED_EXACT_BOREL_PROJECTION",
        "R54 map",
    )
    check(census["Round54"]["materialized_owner_t54_token_count"] == 0, "R54 token")
    check(census["Round67"]["materialized_owned_Omega_j_record_count"] == 0, "R67 Omega")
    check(census["Round67"]["materialized_q_j_output_count"] == 0, "R67 qj")

    r142 = result["Round142_underdetermination_pin"]
    check(r142["historical_component_rank_identified"] is False, "R142 rank")
    check(r142["historical_component_ID_identified"] is False, "R142 ID")
    check(r142["absent_executable_enumeration_field_count"] == 9, "R142 fields")

    migration = result["Round144_atomic_migration_frontier"]
    check(migration["first_exact_blocker"]["node_id"] == "D02", "D02")
    check(migration["ready_DAG_nodes"] == ["D00", "D01"], "ready nodes")
    check(all(x is None for x in migration["current_identifier_values"].values()), "null IDs")
    slots = migration["future_input_slots"]
    check(len(slots) == 2, "future slots")
    check(migration["future_input_slots_sha256"] == digest(slots), "slot digest")
    for slot in slots:
        check(slot["status"] == "UNBOUND_NULL_FUTURE_INPUT", "slot status")
        check(
            all(
                slot[key] is None
                for key in (
                    "source_sha256",
                    "certificate_sha256",
                    "verifier_sha256",
                    "verification_sha256",
                    "verification_result_sha256",
                )
            ),
            "slot null pins",
        )
        check(
            slot["row_sha256"]
            == digest({k: v for k, v in slot.items() if k != "row_sha256"}),
            "slot row digest",
        )
    check(
        result["provenance"]["round145_or_round146_dependency_bytes_in_certificate"]
        is False,
        "future dependency exclusion",
    )
    check(
        result["provenance"]["sealed_snapshot_excludes_round145_and_round146"]
        is True,
        "future snapshot exclusion",
    )
    check(result["provenance"]["historical_identity_guessing_used"] is False, "no guessing")
    check(len(result["executable_upgrade_frontier"]) == 4, "upgrade rows")
    check(len(result["strict_nonclaims"]) == 8, "nonclaims")
    return checks


def semantic_hostile_tests(value: dict[str, Any]) -> list[dict[str, str]]:
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("promote_F5", lambda x: x["result"]["gate5_field_rows"][4].__setitem__("global_field_credit", True)),
        ("maturity_11", lambda x: x["result"]["gate5_global_ledger"].__setitem__("global_maturity_after", "11/18")),
        ("block_count_1", lambda x: x["result"]["gate5_global_ledger"].__setitem__("global_complete_18_field_block_count_after", 1)),
        ("invent_parent_W", lambda x: x["result"]["historical_identifier_and_map_census"]["Round35"].__setitem__("historical_parent_W_materialized_count", 1)),
        ("promote_R70", lambda x: x["result"]["historical_identifier_and_map_census"]["Round35"].__setitem__("historical_schema_compatible_restriction_materialized_count", 1)),
        ("invent_owner", lambda x: x["result"]["historical_identifier_and_map_census"]["Round50"].__setitem__("recordwise_owner_key_count", 1)),
        ("invent_t54", lambda x: x["result"]["historical_identifier_and_map_census"]["Round54"].__setitem__("materialized_owner_t54_token_count", 1)),
        ("invent_Omega", lambda x: x["result"]["historical_identifier_and_map_census"]["Round67"].__setitem__("materialized_owned_Omega_j_record_count", 1)),
        ("invent_qj", lambda x: x["result"]["historical_identifier_and_map_census"]["Round67"].__setitem__("materialized_q_j_output_count", 1)),
        ("bind_R145_partial", lambda x: x["result"]["Round144_atomic_migration_frontier"]["future_input_slots"][0].__setitem__("certificate_sha256", "0" * 64)),
        ("drop_field", lambda x: x["result"]["gate5_field_rows"].pop()),
        ("reorder_fields", lambda x: x["result"]["gate5_field_rows"].reverse()),
        ("erase_D02", lambda x: x["result"]["Round144_atomic_migration_frontier"]["first_exact_blocker"].__setitem__("node_id", "D03")),
        ("claim_gate5", lambda x: x["result"]["gate5_global_ledger"].__setitem__("Gate5", "CERTIFIED")),
        ("claim_CM2", lambda x: x["result"]["gate5_global_ledger"].__setitem__("CM2", "GO")),
        ("remove_nonclaim", lambda x: x["result"]["strict_nonclaims"].pop()),
    ]
    rows = []
    for name, mutate in attacks:
        mutant = copy.deepcopy(value)
        mutate(mutant)
        # Give the attacker the ability to recompute all top-level digests that
        # are easy to discover.  The sealed semantic pin must still reject it.
        mutant["result"]["gate5_field_rows_sha256"] = digest(
            mutant["result"]["gate5_field_rows"]
        )
        mutant["result"]["Round144_atomic_migration_frontier"][
            "future_input_slots_sha256"
        ] = digest(
            mutant["result"]["Round144_atomic_migration_frontier"][
                "future_input_slots"
            ]
        )
        mutant["result_sha256"] = digest(mutant["result"])
        rejected = False
        try:
            verify_semantics(mutant, exact_hash=True)
        except VerificationError:
            rejected = True
        require(rejected, f"hostile mutation accepted:{name}")
        rows.append({"attack": name, "status": "REJECTED"})
    return rows


def io_hostile_tests(valid: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    canonical = canonical_bytes(valid) + b"\n"

    def expect_reject(name: str, make: Callable[[Path], None]) -> None:
        with tempfile.TemporaryDirectory(prefix="round147-io-") as tmp:
            path = Path(tmp) / "candidate.json"
            make(path)
            rejected = False
            try:
                strict_load(path)
            except (VerificationError, OSError, UnicodeError, json.JSONDecodeError):
                rejected = True
            require(rejected, f"I/O attack accepted:{name}")
        rows.append({"attack": name, "status": "REJECTED"})

    expect_reject("invalid_utf8", lambda p: p.write_bytes(b"\xff\n"))
    expect_reject("trailing_json", lambda p: p.write_bytes(canonical + b"{}\n"))
    expect_reject("double_newline", lambda p: p.write_bytes(canonical + b"\n"))
    expect_reject("noncanonical_pretty", lambda p: p.write_text(json.dumps(valid, indent=2) + "\n", encoding="utf-8"))
    expect_reject("missing_newline", lambda p: p.write_bytes(canonical[:-1]))
    expect_reject("utf8_bom", lambda p: p.write_bytes(b"\xef\xbb\xbf" + canonical))
    expect_reject("directory", lambda p: p.mkdir())
    expect_reject("fifo", lambda p: os.mkfifo(p))

    with tempfile.TemporaryDirectory(prefix="round147-io-") as tmp:
        target = Path(tmp) / "target.json"
        target.write_bytes(canonical)
        link = Path(tmp) / "candidate.json"
        link.symlink_to(target)
        rejected = False
        try:
            strict_load(link)
        except (VerificationError, OSError):
            rejected = True
        require(rejected, "symlink accepted")
        rows.append({"attack": "symlink", "status": "REJECTED"})

    def oversized(path: Path) -> None:
        with path.open("wb") as handle:
            handle.truncate(MAX_CERT_BYTES + 1)

    expect_reject("oversized_sparse", oversized)
    return rows


def atomic_write(path: Path, payload: bytes) -> None:
    resolved = path.resolve()
    require(
        resolved.parent in {BASE, Path(tempfile.gettempdir()).resolve()},
        "output parent",
    )
    require(not resolved.exists() or resolved.is_file(), "output type")
    fd, temp_name = tempfile.mkstemp(prefix=f".{resolved.name}.", dir=resolved.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, resolved)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=DEFAULT_CERT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--skip-hostile-tests", action="store_true")
    args = parser.parse_args()

    cert = strict_load(args.certificate)
    semantic_checks = verify_semantics(cert)
    pin_count = verify_external_inputs(cert["result"])
    require(file_sha256(args.certificate) == EXPECTED_CERT_SHA256, "certificate pin")

    semantic_attacks = []
    io_attacks = []
    if not args.skip_hostile_tests:
        semantic_attacks = semantic_hostile_tests(cert)
        io_attacks = io_hostile_tests(cert)

    result = {
        "status": "PASS",
        "certificate": args.certificate.name,
        "certificate_sha256": file_sha256(args.certificate),
        "certificate_result_sha256": cert["result_sha256"],
        "producer": PRODUCER_NAME,
        "producer_sha256": PRODUCER_SHA256,
        "verified_input_pin_count": pin_count,
        "independent_semantic_check_count": semantic_checks,
        "sealed_snapshot_file_count": cert["result"][
            "sealed_repository_search_snapshot"
        ]["file_count"],
        "sealed_snapshot_total_bytes": cert["result"][
            "sealed_repository_search_snapshot"
        ]["total_bytes"],
        "semantic_hostile_attack_rows": semantic_attacks,
        "semantic_hostile_attack_count": len(semantic_attacks),
        "io_hostile_attack_rows": io_attacks,
        "io_hostile_attack_count": len(io_attacks),
        "gate5_global_maturity": "10/18",
        "global_complete_18_field_block_count": 0,
        "new_Gate5_field_credit_count": 0,
        "Round145_or_Round146_admitted": False,
        "Gate5": "NOT_CERTIFIED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    envelope = {
        "schema": VERIFY_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    atomic_write(args.output, canonical_bytes(envelope) + b"\n")
    print(json.dumps({
        "status": "PASS",
        "verification": str(args.output),
        "result_sha256": envelope["result_sha256"],
        "verification_sha256": file_sha256(args.output),
        "semantic_hostile_attack_count": len(semantic_attacks),
        "io_hostile_attack_count": len(io_attacks),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
