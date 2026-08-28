#!/usr/bin/env python3
"""Coherent mutation attacks for the independent same-chart witness bundle."""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable


LEDGER = "cm2_c27_same_chart_exact_equal_cross_component_witness_groups.jsonl.gz"
RESULT = "cm2_c27_same_chart_exact_equal_cross_component_sqlite_result.json"


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def parse_bundle(directory: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw = (directory / RESULT).read_bytes()
    need(raw.endswith(b"\n") and b"\n" not in raw[:-1], "single result object")
    result = json.loads(raw[:-1])
    need(canonical(result) + b"\n" == raw, "canonical result")
    body = dict(result)
    need(body.pop("result_sha256", None) == digest(body), "result closure")
    groups = []
    with gzip.open(directory / LEDGER, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), "group newline")
            row = json.loads(line[:-1])
            need(canonical(row) + b"\n" == line, "canonical group")
            need(row.get("ordinal") == ordinal, "group ordinal")
            groups.append(row)
    return result, groups


def endpoint_positive(lower: dict[str, Any], upper: dict[str, Any]) -> bool:
    if lower.get("kind") == upper.get("kind") == "Q":
        return Fraction(upper["value"]) > Fraction(lower["value"])
    if lower.get("kind") != "SIGNED_SQRT_Q" or upper.get("kind") != "SIGNED_SQRT_Q":
        return False
    if lower.get("sign") != upper.get("sign") or lower["sign"] not in {-1, 1}:
        return False
    lq, uq = Fraction(lower["radicand"]), Fraction(upper["radicand"])
    return uq > lq if lower["sign"] == 1 else lq > uq


def semantic_commitments(groups: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "group_ids_sha256": digest([row["group_id"] for row in groups]),
        "group_rows_without_ordinal_sha256": digest([
            digest({key: value for key, value in row.items() if key not in {"ordinal", "group_row_sha256"}})
            for row in groups
        ]),
        "full_group_projection_sha256": digest([
            {key: value for key, value in row.items() if key != "group_row_sha256"}
            for row in groups
        ]),
    }


def result_semantic_projection(result: dict[str, Any]) -> dict[str, Any]:
    excluded = {
        "declared_seed", "declared_seed_used_for_pre_sort_sqlite_insertion_order",
        "invocation", "semantic_projection_sha256", "ledger", "result_sha256",
    }
    return {key: value for key, value in result.items() if key not in excluded}


def validate(
    result: dict[str, Any], groups: list[dict[str, Any]],
    expected: dict[str, Any], ledger_path: Path | None,
) -> None:
    body = dict(result)
    need(body.pop("result_sha256", None) == digest(body), "result closure")
    need(
        result.get("status") == "PASS_ZERO_CREDIT__228_SAME_CHART_EXACT_EQUAL_POSITIVE_VOLUME_CROSS_C15_COMPONENT_WITNESS_GROUPS"
        and result.get("formal_credit") == 0
        and result.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED"
        and result.get("CM2") == "NO-GO_FOR_CLAIM"
        and result.get("legal_cross_component_witness_found") is True
        and result.get("endpoint_bits_needed_for_these_witnesses") is False
        and result.get("required_governance_action") == "REBUILD_C27_THROUGH_C29__PATCHING_OR_PRESERVING_C29_UNCONDITIONAL_AUTHORITY_IS_FORBIDDEN",
        "truthful nonpromotion and rebuild action",
    )
    forbidden = result.get("forbidden_inputs", {})
    need(forbidden == {
        "same_chart_census_atom_ledger_opened_or_used": False,
        "C27_source_or_FAMILIES_imported_or_read": False,
        "old_edge_ledger_used_as_candidate_universe": False,
    }, "forbidden input contract")
    need(
        result.get("declared_seed") == expected["declared_seed"]
        and result.get("declared_seed_used_for_pre_sort_sqlite_insertion_order") is True
        and result.get("invocation") == expected["invocation"],
        "actual seed and invocation authority",
    )
    projection = result_semantic_projection(result)
    need(
        result.get("semantic_projection_sha256") == digest(projection)
        and result["semantic_projection_sha256"] == expected["semantic_projection_sha256"],
        "cross-seed semantic projection commitment",
    )
    need(len(groups) == result["witness_census"]["witness_group_count"] == 228, "228 groups")
    need([row["ordinal"] for row in groups] == list(range(228)), "ordinal cover")
    group_ids: set[str] = set()
    for row in groups:
        group_body = dict(row)
        claimed = group_body.pop("group_row_sha256", None)
        need(claimed == digest(group_body), "group closure")
        need(row["group_id"] not in group_ids, "unique group id")
        group_ids.add(row["group_id"])
        expected_id = "same-chart-exact-equal-positive-volume:" + digest([row["chart"], row["physical_bounds"]])
        need(row["group_id"] == expected_id, "geometry-derived group id")
        need(row["member_count"] == len(row["members"]), "member count")
        components = sorted({member["fresh_component_id"] for member in row["members"]}, key=lambda x: x.encode("ascii"))
        need(len(components) > 1 and row["fresh_component_ids"] == components, "cross C15 components")
        need(row["component_count"] == len(components), "component count")
        need(row["legal_cross_component_physical_witness"] is True, "legal witness flag")
        bounds = row["physical_bounds"]
        need(len(bounds) == 6 and all(endpoint_positive(bounds[2*i], bounds[2*i+1]) for i in range(3)), "strict positive 3D widths")
        proof = row["strict_positive_volume_proof"]
        need(
            proof["dimension"] == 3
            and proof["common_open_interior_nonempty"] is True
            and proof["endpoint_inclusion_bits_irrelevant_to_open_interior_intersection"] is True,
            "strict positive volume proof",
        )
        hashes = []
        for member in row["members"]:
            member_body = dict(member)
            member_claimed = member_body.pop("member_row_sha256", None)
            need(member_claimed == digest(member_body), "member closure")
            need(member["chart"] == row["chart"] and member["physical_bounds"] == bounds, "member equal box")
            hashes.append(member_claimed)
        need(row["member_row_hashes_sha256"] == digest(hashes), "member sequence commitment")
    commitments = semantic_commitments(groups)
    need(
        commitments == {key: expected[key] for key in commitments},
        "primitive baseline semantic commitments",
    )
    need(result["group_ids_sha256"] == commitments["group_ids_sha256"], "result group ids commitment")
    need(result["group_rows_sha256"] == commitments["group_rows_without_ordinal_sha256"], "result group rows commitment")
    if ledger_path is not None:
        need(result["ledger"]["sha256"] == file_hash(ledger_path), "ledger file commitment")


def reclose(result: dict[str, Any], groups: list[dict[str, Any]]) -> None:
    for ordinal, row in enumerate(groups):
        row["ordinal"] = ordinal
        for member in row.get("members", []):
            member_body = dict(member)
            member_body.pop("member_row_sha256", None)
            member["member_row_sha256"] = digest(member_body)
        row["member_count"] = len(row.get("members", []))
        if "members" in row:
            row["member_row_hashes_sha256"] = digest([member["member_row_sha256"] for member in row["members"]])
        row_body = dict(row)
        row_body.pop("group_row_sha256", None)
        row["group_row_sha256"] = digest(row_body)
    result["witness_census"]["witness_group_count"] = len(groups)
    result["group_ids_sha256"] = digest([row["group_id"] for row in groups])
    result["group_rows_sha256"] = digest([
        digest({key: value for key, value in row.items() if key not in {"ordinal", "group_row_sha256"}})
        for row in groups
    ])
    result["semantic_projection_sha256"] = digest(result_semantic_projection(result))
    body = dict(result)
    body.pop("result_sha256", None)
    result["result_sha256"] = digest(body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")
    directory = Path(args.candidate_dir).resolve()
    baseline_result, baseline_groups = parse_bundle(directory)
    expected = semantic_commitments(baseline_groups)
    expected["declared_seed"] = baseline_result["declared_seed"]
    expected["invocation"] = baseline_result["invocation"]
    expected["semantic_projection_sha256"] = baseline_result["semantic_projection_sha256"]
    validate(baseline_result, baseline_groups, expected, directory / LEDGER)

    attacks: list[tuple[str, Callable[[dict[str, Any], list[dict[str, Any]]], None]]] = []
    attacks.append(("drop_witness_group", lambda r, g: g.pop()))
    attacks.append(("duplicate_witness_group", lambda r, g: g.append(copy.deepcopy(g[-1]))))
    attacks.append(("promote_c27", lambda r, g: r.__setitem__("C27_C28_C29", "PASS")))
    attacks.append(("mint_formal_credit", lambda r, g: r.__setitem__("formal_credit", 1)))
    attacks.append(("clear_legal_witness", lambda r, g: r.__setitem__("legal_cross_component_witness_found", False)))
    attacks.append(("preserve_c29_patch_action", lambda r, g: r.__setitem__("required_governance_action", "PATCH_C29")))
    attacks.append(("claim_census_ledger_used", lambda r, g: r["forbidden_inputs"].__setitem__("same_chart_census_atom_ledger_opened_or_used", True)))
    attacks.append(("claim_c27_families_read", lambda r, g: r["forbidden_inputs"].__setitem__("C27_source_or_FAMILIES_imported_or_read", True)))
    attacks.append(("claim_edge_ledger_used", lambda r, g: r["forbidden_inputs"].__setitem__("old_edge_ledger_used_as_candidate_universe", True)))
    attacks.append(("change_group_chart", lambda r, g: g[0].__setitem__("chart", "G:FAKE")))
    attacks.append(("change_group_lower_bound", lambda r, g: g[0]["physical_bounds"][0].__setitem__("value", "-999999")))
    attacks.append(("collapse_group_component", lambda r, g: g[0]["members"][0].__setitem__("fresh_component_id", g[0]["members"][1]["fresh_component_id"])))
    attacks.append(("change_member_owner", lambda r, g: g[0]["members"][0].__setitem__("owner_member_id", "forged-owner")))
    attacks.append(("change_member_source", lambda r, g: g[0]["members"][0].__setitem__("source_kernel", "C27")))
    attacks.append(("change_support_kind", lambda r, g: g[0]["members"][0].__setitem__("support_kind", "CLOSED_BOX")))
    attacks.append(("change_C15_row_pin", lambda r, g: g[0]["members"][0].__setitem__("C15_member_row_sha256", "0" * 64)))
    attacks.append(("change_C25_row_pin", lambda r, g: g[0]["members"][0].__setitem__("C25_member_row_sha256", "0" * 64)))
    attacks.append(("drop_group_member", lambda r, g: g[0]["members"].pop()))
    attacks.append(("forge_group_id", lambda r, g: g[0].__setitem__("group_id", "forged-group")))
    attacks.append(("zero_width_t", lambda r, g: g[0]["physical_bounds"].__setitem__(1, copy.deepcopy(g[0]["physical_bounds"][0]))))
    attacks.append(("deny_open_interior", lambda r, g: g[0]["strict_positive_volume_proof"].__setitem__("common_open_interior_nonempty", False)))
    attacks.append(("require_endpoint_bits", lambda r, g: r.__setitem__("endpoint_bits_needed_for_these_witnesses", True)))
    attacks.append(("forge_cross_component_pair_count", lambda r, g: g[0].__setitem__("cross_component_member_pair_count", 0)))
    attacks.append(("promote_cm2", lambda r, g: r.__setitem__("CM2", "GO_FOR_CLAIM")))
    attacks.append(("change_declared_seed", lambda r, g: r.__setitem__("declared_seed", r["declared_seed"] + 1)))
    attacks.append(("change_invocation_seed", lambda r, g: r["invocation"]["command_argv"].__setitem__(-1, "0")))
    attacks.append(("forge_C23_normalization_census", lambda r, g: r["C23_signed_sqrt_physical_normalization_census"].__setitem__("physical_t_sign:+1", 0)))

    rejected = []
    for name, mutate in attacks:
        result = copy.deepcopy(baseline_result)
        groups = copy.deepcopy(baseline_groups)
        mutate(result, groups)
        reclose(result, groups)
        try:
            validate(result, groups, expected, None)
        except Exception:
            rejected.append(name)
        else:
            raise Failure("accepted coherent attack:" + name)
    body = {
        "status": f"PASS_{len(attacks)}_OF_{len(attacks)}_COHERENT_SAME_CHART_WITNESS_ATTACKS_REJECTED__ZERO_CREDIT",
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "rejected_attacks": rejected,
        "baseline_result_sha256": baseline_result["result_sha256"],
        "baseline_group_ids_sha256": expected["group_ids_sha256"],
        "baseline_group_projection_sha256": expected["full_group_projection_sha256"],
        "baseline_declared_seed": baseline_result["declared_seed"],
        "baseline_semantic_projection_sha256": baseline_result["semantic_projection_sha256"],
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    print(canonical({**body, "result_sha256": digest(body)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print("REJECT_SAME_CHART_WITNESS_ATTACK_HARNESS:" + str(error), file=sys.stderr)
        raise SystemExit(2)
