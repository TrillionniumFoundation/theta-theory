#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent
PREFIX = "cm2_round306c28_source_g_125616475670_cross_component_pair_block_routing_and_maximality"
BLOCK_LEDGER = PREFIX + "_member_home_block_census_ledger.jsonl.gz"
ROUTE_LEDGER = PREFIX + "_cross_component_pair_route_shard_ledger.jsonl.gz"
RESULT = PREFIX + "_result.json"

C15 = "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze"
C27 = "cm2_round306c27_source_g_corrected_transition_frontier_exhaustion_and_known_edge_recovery"
C15_MEMBER = C15 + "_member_component_ledger.jsonl.gz"
C15_COMPONENT = C15 + "_component_census_ledger.jsonl.gz"
C27_FRONTIER = C27 + "_transition_candidate_ledger.jsonl.gz"
C27_FAMILY = C27 + "_transition_family_coverage_ledger.jsonl.gz"

SOURCE_SPECS = (
    (
        "C15",
        C15,
        "a1eea2c41123d2ff7f7d3e1f35f1deabc5bae9d93b24f825b4831f6324c1e2c4",
        "99ad5fb9f2f940155effdcb24ac076824f6436f2d92a66bd6d9ed196d0ac8f71",
        (C15_MEMBER, C15_COMPONENT),
    ),
    (
        "C27",
        C27,
        "26c0f7e5364630a5aafae690fc50cefd2091fe458432735b8bc2c0c3e13b631b",
        "3c547d24d602c751212c0c2e8fb15ef80413d2700093cfab5dd07f4e8d59235f",
        (C27_FRONTIER, C27_FAMILY),
    ),
)

MEMBER_COUNT = 502204
COMPONENT_COUNT = 57876
BLOCK_COUNT = 256
SHARD_COUNT = 32896
TOTAL_UNORDERED_PAIRS = 126104177706
WITHIN_COMPONENT_PAIRS = 487702036
CROSS_COMPONENT_PAIRS = 125616475670


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            state.update(block)
    return state.hexdigest()


def reject_constant(value: str) -> None:
    raise Failure("nonfinite:" + value)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate key:" + key)
        output[key] = value
    return output


def decode(raw: bytes, label: str) -> Any:
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(not payload.endswith(b"\n"), "multiple trailing newlines:" + label)
    try:
        text = payload.decode("ascii")
        value = json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Failure("JSON:" + label) from error
    need(canonical(value) == payload, "canonical:" + label)
    return value


def rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line[-1:] == b"\n", "newline:" + path.name)
            value = decode(line[:-1], path.name + ":" + str(ordinal))
            need(type(value) is dict, "row object:" + path.name)
            body = dict(value)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body), "row closure:" + path.name + ":" + str(ordinal))
            yield value


def result_object(path: Path) -> tuple[dict[str, Any], str]:
    value = decode(path.read_bytes(), path.name)
    need(type(value) is dict, "result object:" + path.name)
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "result closure:" + path.name)
    return value, claimed


def manifest(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        fields = line.split(None, 1)
        need(len(fields) == 2 and len(fields[0]) == 64, "manifest line:" + path.name)
        name = Path(fields[1].strip()).name
        need(name == fields[1].strip() and name not in output, "manifest filename:" + path.name)
        output[name] = fields[0]
    return output


def validate_sources() -> tuple[dict[str, str], list[dict[str, str]]]:
    objects: dict[str, str] = {}
    pins: list[dict[str, str]] = []
    for tag, base, expected_manifest, expected_object, ledgers in SOURCE_SPECS:
        manifest_name = base + "_manifest.sha256"
        result_name = base + "_result.json"
        verification_name = base + "_verification.json"
        need(file_hash(ROOT / manifest_name) == expected_manifest, "manifest pin:" + tag)
        listed = manifest(ROOT / manifest_name)
        for name in (*ledgers, result_name, verification_name):
            need(name in listed and file_hash(ROOT / name) == listed[name], "manifest member:" + tag + ":" + name)
        source_result, claimed = result_object(ROOT / result_name)
        need(claimed == expected_object and str(source_result.get("status", "")).startswith("PASS"), "result pin:" + tag)
        verification = decode((ROOT / verification_name).read_bytes(), verification_name)
        need(str(verification.get("status", "")).startswith("PASS"), "verification pin:" + tag)
        objects[tag] = claimed
        pins.append({"filename": manifest_name, "sha256": expected_manifest})
        for name in (*ledgers, result_name, verification_name):
            pins.append({"filename": name, "sha256": listed[name]})
    c15_result, _ = result_object(ROOT / (C15 + "_result.json"))
    c27_result, _ = result_object(ROOT / (C27 + "_result.json"))
    need(c15_result["fresh_universe_census"]["members"] == MEMBER_COUNT, "C15 members")
    need(c15_result["fresh_DSU_census"]["components"] == COMPONENT_COUNT, "C15 components")
    need(c15_result["fresh_DSU_census"]["cross_component_pair_denominator"] == CROSS_COMPONENT_PAIRS, "C15 denominator")
    need(c27_result["formal_credit"]["transition_frontier_exhaustion_theorem"] == 1, "C27 theorem")
    need(c27_result["transition_candidate_census"]["new_legal_cross_component"] == 0, "C27 new edges")
    need(c27_result["transition_candidate_census"]["unresolved"] == 0, "C27 unresolved")
    need(c27_result["strict_nonpromotion"]["pair_routing"] == 0, "C27 pair boundary")
    return objects, sorted(pins, key=lambda item: item["filename"])


def choose_two(value: int) -> int:
    return value * (value - 1) // 2


def home_block(member_id: str) -> int:
    return hashlib.sha256(member_id.encode("ascii")).digest()[0]


def reconstruct_partition() -> tuple[list[int], list[int], list[list[int]], dict[str, str]]:
    block_members = [0] * BLOCK_COUNT
    component_blocks: dict[str, dict[int, int]] = defaultdict(dict)
    member_ids: set[str] = set()
    member_sequence = hashlib.sha256()
    member_rows = 0
    for ordinal, row in enumerate(rows(ROOT / C15_MEMBER)):
        need(row["member_ordinal"] == ordinal, "member ordinal")
        member_id = row["registry_member_id"]
        component_id = row["fresh_component_id"]
        need(member_id not in member_ids, "duplicate member")
        member_ids.add(member_id)
        block = home_block(member_id)
        block_members[block] += 1
        counts = component_blocks[component_id]
        counts[block] = counts.get(block, 0) + 1
        member_sequence.update(member_id.encode("ascii") + b"\n")
        member_rows += 1
    need(member_rows == MEMBER_COUNT and len(member_ids) == MEMBER_COUNT, "member census")
    expected_components: dict[str, int] = {}
    for ordinal, row in enumerate(rows(ROOT / C15_COMPONENT)):
        need(row["component_ordinal"] == ordinal, "component ordinal")
        component_id = row["fresh_component_id"]
        need(component_id not in expected_components, "duplicate component")
        expected_components[component_id] = row["member_count"]
    need(len(expected_components) == COMPONENT_COUNT and set(expected_components) == set(component_blocks), "component set")
    need(all(sum(component_blocks[component].values()) == count for component, count in expected_components.items()), "component member census")

    block_component_presence = [0] * BLOCK_COUNT
    within = [[0] * BLOCK_COUNT for _ in range(BLOCK_COUNT)]
    component_block_vector = hashlib.sha256()
    within_total_from_components = 0
    for component_id in sorted(component_blocks):
        items = sorted(component_blocks[component_id].items())
        component_block_vector.update(canonical([component_id, items]) + b"\n")
        component_size = sum(count for _, count in items)
        within_total_from_components += choose_two(component_size)
        for left_index, (left_block, left_count) in enumerate(items):
            block_component_presence[left_block] += 1
            within[left_block][left_block] += choose_two(left_count)
            for right_block, right_count in items[left_index + 1:]:
                within[left_block][right_block] += left_count * right_count
    need(sum(block_members) == MEMBER_COUNT and all(count > 0 for count in block_members), "block coverage")
    need(within_total_from_components == WITHIN_COMPONENT_PAIRS, "within component denominator")
    commitments = {
        "member_id_sequence_sha256": member_sequence.hexdigest(),
        "block_member_count_vector_sha256": digest(block_members),
        "component_block_count_vector_sha256": component_block_vector.hexdigest(),
    }
    return block_members, block_component_presence, within, commitments


def close(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "row_sha256": digest(body)}


def block_rows(block_members: list[int], presence: list[int], within: list[list[int]], objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    for block in range(BLOCK_COUNT):
        total_pairs = choose_two(block_members[block])
        within_pairs = within[block][block]
        body = {
            "schema": "cm2.round306c28.source-g-member-home-block-census.v1.row.v1",
            "home_block_ordinal": block,
            "home_block_hex": f"{block:02x}",
            "home_block_definition": "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID",
            "member_count": block_members[block],
            "component_presence_count": presence[block],
            "same_block_total_unordered_pairs": total_pairs,
            "same_block_within_component_pairs": within_pairs,
            "same_block_cross_component_pairs": total_pairs - within_pairs,
            "source_binding": {"C15_result_sha256": objects["C15"]},
            "formal_credit": {"member_home_assignments": block_members[block]},
            "strict_nonpromotion": {"pair_routing": 0, "B2": 0, "maximality": 0, "fibre": 0, "global_disposition": 0, "CM2": 0},
        }
        yield close(body)


def route_rows(block_members: list[int], within: list[list[int]], objects: dict[str, str]) -> Iterator[dict[str, Any]]:
    ordinal = 0
    for left in range(BLOCK_COUNT):
        for right in range(left, BLOCK_COUNT):
            total_pairs = choose_two(block_members[left]) if left == right else block_members[left] * block_members[right]
            within_pairs = within[left][right]
            cross_pairs = total_pairs - within_pairs
            need(cross_pairs >= 0, "negative cross shard")
            body = {
                "schema": "cm2.round306c28.source-g-cross-component-pair-route-shard.v1.row.v1",
                "shard_ordinal": ordinal,
                "canonical_home_block_pair": [f"{left:02x}", f"{right:02x}"],
                "left_member_count": block_members[left],
                "right_member_count": block_members[right],
                "same_home_block": left == right,
                "total_unordered_member_pairs": total_pairs,
                "within_component_member_pairs_excluded": within_pairs,
                "cross_component_member_pairs_routed": cross_pairs,
                "pair_classification": {
                    "EXACT_NONEDGE_BY_EXHAUSTED_C27_TRANSITION_COMPLEMENT": cross_pairs,
                    "KNOWN_LEGAL_CROSS_COMPONENT": 0,
                    "NEW_LEGAL_CROSS_COMPONENT": 0,
                    "UNRESOLVED": 0,
                },
                "proof_binding": {
                    "C15_partition_result_sha256": objects["C15"],
                    "C27_transition_frontier_theorem_result_sha256": objects["C27"],
                    "canonical_pair_home_rule": "SORTED_FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID",
                    "all_within_component_pairs_excluded_by_component_block_convolution": True,
                    "all_remaining_pairs_are_cross_component": True,
                    "C27_proves_no_admissible_legal_cross_component_transition": True,
                },
                "formal_credit": {"pair_routes": cross_pairs, "exact_nonedge_classifications": cross_pairs},
                "strict_nonpromotion": {"new_DSU_edge": 0, "new_DSU_union": 0, "fibre": 0, "global_disposition": 0, "CM2": 0},
            }
            yield close(body)
            ordinal += 1
    need(ordinal == SHARD_COUNT, "shard count")


def write_rows(path: Path, source: Iterator[dict[str, Any]]) -> tuple[int, str, dict[str, int]]:
    sequence = hashlib.sha256()
    totals = {"total": 0, "within": 0, "cross": 0}
    count = 0
    with path.open("xb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as output:
            for row in source:
                output.write(canonical(row) + b"\n")
                sequence.update(bytes.fromhex(row["row_sha256"]))
                if "total_unordered_member_pairs" in row:
                    totals["total"] += row["total_unordered_member_pairs"]
                    totals["within"] += row["within_component_member_pairs_excluded"]
                    totals["cross"] += row["cross_component_member_pairs_routed"]
                count += 1
    return count, sequence.hexdigest(), totals


def descriptor(path: Path, count: int, sequence: str, order: str) -> dict[str, Any]:
    return {"filename": path.name, "row_count": count, "size": path.stat().st_size, "sha256": file_hash(path), "row_sequence_sha256": sequence, "order": order}


def build(candidate: Path) -> dict[str, Any]:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated runtime")
    objects, pins = validate_sources()
    candidate.mkdir(parents=True, exist_ok=True)
    need(not any(candidate.iterdir()), "candidate directory not empty")
    block_members, presence, within, commitments = reconstruct_partition()
    block_count, block_sequence, _ = write_rows(candidate / BLOCK_LEDGER, block_rows(block_members, presence, within, objects))
    route_count, route_sequence, totals = write_rows(candidate / ROUTE_LEDGER, route_rows(block_members, within, objects))
    need(block_count == BLOCK_COUNT and route_count == SHARD_COUNT, "ledger counts")
    need(totals == {"total": TOTAL_UNORDERED_PAIRS, "within": WITHIN_COMPONENT_PAIRS, "cross": CROSS_COMPONENT_PAIRS}, "pair totals")
    block_descriptor = descriptor(candidate / BLOCK_LEDGER, block_count, block_sequence, "HOME_BLOCK_00_THROUGH_FF")
    route_descriptor = descriptor(candidate / ROUTE_LEDGER, route_count, route_sequence, "LEXICOGRAPHIC_UNORDERED_BLOCK_PAIRS_00_00_THROUGH_FF_FF")
    theorem = {
        "kind": "CORRECTED_B2_GLOBAL_PAIR_ROUTING_AND_COMPONENT_MAXIMALITY_THEOREM",
        "every_C15_member_has_exactly_one_deterministic_home_block": True,
        "every_canonical_unordered_member_pair_has_exactly_one_unordered_block_pair_shard": True,
        "all_32896_shards_are_disjoint_and_exhaustive": True,
        "within_component_pairs_are_removed_by_exact_component_block_convolution": True,
        "cross_component_pair_denominator_is_exact": CROSS_COMPONENT_PAIRS,
        "C27_transition_frontier_is_exhaustive": True,
        "C27_has_zero_legal_cross_component_transitions": True,
        "every_cross_component_pair_is_an_exact_nonedge": True,
        "new_legal_cross_component_pair_count": 0,
        "unresolved_pair_count": 0,
        "C15_components_are_maximal_under_the_corrected_transition_relation": True,
    }
    body = {
        "schema": "cm2.round306c28.source-g-125616475670-cross-component-pair-block-routing-and-maximality.v1",
        "status": "PASS_ALL_125616475670_CROSS_COMPONENT_MEMBER_PAIRS_EXACTLY_ROUTED_AS_NONEDGES__B2_AND_MAXIMALITY_SEALED__FINAL_FIBRE_AUDIT_REQUIRED",
        "corrected_partition_census": {"members": MEMBER_COUNT, "components": COMPONENT_COUNT, "total_unordered_member_pairs": TOTAL_UNORDERED_PAIRS, "within_component_member_pairs": WITHIN_COMPONENT_PAIRS, "cross_component_member_pairs": CROSS_COMPONENT_PAIRS},
        "home_block_census": {"definition": "FIRST_BYTE_SHA256_ASCII_REGISTRY_MEMBER_ID", "blocks": BLOCK_COUNT, "nonempty_blocks": sum(count > 0 for count in block_members), "members_assigned": sum(block_members), **commitments},
        "pair_route_census": {"unordered_block_pair_shards": SHARD_COUNT, "closed_shards": route_count, "cross_component_pairs_routed": totals["cross"], "exact_nonedge_pairs": totals["cross"], "known_legal_cross_component_pairs": 0, "new_legal_cross_component_pairs": 0, "unresolved_pairs": 0},
        "B2_and_maximality_theorem": theorem,
        "B2_and_maximality_theorem_sha256": digest(theorem),
        "ledgers": {"member_home_block_census": block_descriptor, "cross_component_pair_route_shard": route_descriptor},
        "input_pins": pins,
        "formal_credit": {"B1A_consumed": 1, "transition_theorem_consumed": 1, "member_home_assignments": MEMBER_COUNT, "pair_route_shards": SHARD_COUNT, "pair_routing": CROSS_COMPONENT_PAIRS, "pair_classification": CROSS_COMPONENT_PAIRS, "exact_nonedges": CROSS_COMPONENT_PAIRS, "B2": 1, "maximality": 1},
        "strict_nonpromotion": {"new_DSU_edges": 0, "new_DSU_unions": 0, "fibre": 0, "global_disposition": 0, "D02": "BLOCKED_PENDING_FINAL_FIBRE_AND_GLOBAL_DISPOSITION_AUDIT", "D03": "NOT_REACHED", "D04": "NOT_MINTED", "CM2": "NO-GO_FOR_CLAIM"},
        "required_next": "RECONSTRUCT_57876_COMPONENT_FIBRES_AND_ISSUE_GLOBAL_EXACT_KEY_DISPOSITIONS_THEN_AUDIT_D02_D03_D04_CM2_GATES",
    }
    result = {**body, "result_sha256": digest(body)}
    (candidate / RESULT).write_bytes(canonical(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", required=True)
    args = parser.parse_args()
    result = build(Path(args.candidate_dir).resolve())
    print(canonical({"status": result["status"], "result_sha256": result["result_sha256"]}).decode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
