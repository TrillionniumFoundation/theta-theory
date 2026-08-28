#!/usr/bin/env python3
"""Independent SQLite reconstruction of same-chart exact-equal-box witnesses.

This probe never opens the SAME_CHART census atom ledger, Round306C27, a
FAMILIES table, or a historical transition-edge ledger.  Its candidate
universe is rebuilt directly from the six primitive support-row sources and
the frozen chart-lineage/C15/C25 authorities.  SQLite supplies the independent
external grouping/sort implementation.  C23 t^2 branches are transported to
physical t with exact signed-square-root endpoints before grouping.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
import math
from pathlib import Path
import random
import sqlite3
import sys
from typing import Any, Iterable, Iterator


ROOT = Path(__file__).resolve().parent
LEDGER = "cm2_c27_same_chart_exact_equal_cross_component_witness_groups.jsonl.gz"
RESULT = "cm2_c27_same_chart_exact_equal_cross_component_sqlite_result.json"

FILES = {
    "C15": ("cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz", "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    "C25": ("cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz", "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6"),
    "C19A": ("cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz", "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3"),
    "C19B": ("cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz", "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798"),
    "C19C": ("cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz", "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84"),
    "C20A": ("cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz", "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"),
    "C22A": ("cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz", "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb"),
    "C23A": ("cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz", "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528"),
    "R179": ("cm2_round179_source_g_residual_tube_arrangement_rows.json", "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    "R234": ("cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    "R236": ("cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    "C5": ("cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz", "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
}
SOURCE_COUNTS = {
    "C19A": 5_596,
    "C19B": 12_232,
    "C19C": 33_344,
    "C20A": 126_468,
    "C22A": 295_340,
    "C23A": 10_252,
}
SOURCE_KERNEL = {
    "C19A": "C19A",
    "C19B": "C19B",
    "C19C": "C19C",
    "C20A": "C20A",
    "C22A": "C22B",
    "C23A": "C23B",
}


class Failure(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def qwire(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def closed_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path.name}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"canonical:{path.name}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body), f"closure:{path.name}:{ordinal}")
            yield row


def rational_endpoint(value: str) -> dict[str, Any]:
    return {"kind": "Q", "value": qwire(Fraction(value))}


def signed_sqrt_endpoint(value: str, sign: int) -> dict[str, Any]:
    q = Fraction(value)
    need(q >= 0 and sign in {-1, 1}, "signed sqrt domain")
    numerator_root = math.isqrt(q.numerator)
    denominator_root = math.isqrt(q.denominator)
    if numerator_root * numerator_root == q.numerator and denominator_root * denominator_root == q.denominator:
        return rational_endpoint(qwire(Fraction(sign * numerator_root, denominator_root)))
    return {"kind": "SIGNED_SQRT_Q", "radicand": qwire(q), "sign": sign}


def normalized_bounds(source: str, support: dict[str, Any]) -> list[dict[str, Any]]:
    raw = support.get("bounds")
    need(type(raw) is list and len(raw) == 6 and all(type(x) is str for x in raw), f"six exact bounds:{source}")
    if source != "C23A":
        need(support.get("coordinates") == ["t", "p", "s"], f"physical coordinates:{source}")
        return [rational_endpoint(value) for value in raw]
    need(
        support.get("kind") == "T2PS_BRANCH_OPEN_RATIONAL_BOX"
        and support.get("coordinates") == ["t_squared", "p", "s"],
        "C23 t2ps AST",
    )
    sign = support.get("physical_t_sign")
    need(sign in {-1, 1}, "C23 physical sign")
    t_squared_lower, t_squared_upper = raw[:2]
    need(Fraction(t_squared_lower) >= 0 and Fraction(t_squared_upper) > Fraction(t_squared_lower), "C23 positive t2 interval")
    if sign == 1:
        t_lower = signed_sqrt_endpoint(t_squared_lower, 1)
        t_upper = signed_sqrt_endpoint(t_squared_upper, 1)
    else:
        t_lower = signed_sqrt_endpoint(t_squared_upper, -1)
        t_upper = signed_sqrt_endpoint(t_squared_lower, -1)
    return [
        t_lower, t_upper,
        rational_endpoint(raw[2]), rational_endpoint(raw[3]),
        rational_endpoint(raw[4]), rational_endpoint(raw[5]),
    ]


def positive_width(lower: dict[str, Any], upper: dict[str, Any], axis: str) -> dict[str, Any]:
    if lower["kind"] == upper["kind"] == "Q":
        difference = Fraction(upper["value"]) - Fraction(lower["value"])
        need(difference > 0, f"strict rational width:{axis}")
        return {
            "axis": axis,
            "lower": lower,
            "upper": upper,
            "strict_relation": "UPPER_MINUS_LOWER_IS_POSITIVE_RATIONAL",
            "exact_positive_difference": qwire(difference),
        }
    lower_kind, upper_kind = lower.get("kind"), upper.get("kind")
    if lower_kind == upper_kind == "SIGNED_SQRT_Q":
        lower_q, upper_q = Fraction(lower["radicand"]), Fraction(upper["radicand"])
        lower_sign, upper_sign = lower.get("sign"), upper.get("sign")
        need(lower_sign in {-1, 1} and upper_sign in {-1, 1}, f"signed sqrt signs:{axis}")
        if lower_sign == upper_sign == 1:
            need(upper_q > lower_q, f"positive branch strict width:{axis}")
            margin = upper_q - lower_q
            relation = "SQRT_UPPER_RADICAND_GT_SQRT_LOWER_RADICAND"
        elif lower_sign == upper_sign == -1:
            need(lower_q > upper_q, f"negative branch strict width:{axis}")
            margin = lower_q - upper_q
            relation = "NEGATIVE_SQRT_ORDER_REVERSES_AND_WIDTH_IS_POSITIVE"
        else:
            need(lower_sign == -1 and upper_sign == 1, f"opposite signed sqrt order:{axis}")
            margin = lower_q + upper_q
            need(margin > 0, f"opposite signed sqrt strict width:{axis}")
            relation = "NEGATIVE_SQRT_IS_STRICTLY_BELOW_POSITIVE_SQRT"
        return {
            "axis": axis,
            "lower": lower,
            "upper": upper,
            "strict_relation": relation,
            "exact_positive_squared_comparison_margin": qwire(margin),
        }

    if lower_kind == "Q" and upper_kind == "SIGNED_SQRT_Q":
        rational = Fraction(lower["value"])
        radicand = Fraction(upper["radicand"])
        sign = upper.get("sign")
        need(sign in {-1, 1}, f"upper signed sqrt sign:{axis}")
        if sign == 1 and rational < 0:
            margin = -rational
            relation = "NEGATIVE_RATIONAL_IS_STRICTLY_BELOW_NONNEGATIVE_SQRT"
        elif sign == 1:
            margin = radicand - rational * rational
            need(margin > 0, f"rational below positive sqrt by squares:{axis}")
            relation = "NONNEGATIVE_RATIONAL_SQUARE_IS_STRICTLY_BELOW_UPPER_RADICAND"
        else:
            need(rational < 0, f"rational below negative sqrt sign:{axis}")
            margin = rational * rational - radicand
            need(margin > 0, f"rational below negative sqrt by squares:{axis}")
            relation = "LOWER_NEGATIVE_RATIONAL_ABSOLUTE_VALUE_EXCEEDS_SQRT_RADICAND"
        return {
            "axis": axis, "lower": lower, "upper": upper,
            "strict_relation": relation,
            "exact_positive_squared_comparison_margin": qwire(margin),
        }

    if lower_kind == "SIGNED_SQRT_Q" and upper_kind == "Q":
        radicand = Fraction(lower["radicand"])
        rational = Fraction(upper["value"])
        sign = lower.get("sign")
        need(sign in {-1, 1}, f"lower signed sqrt sign:{axis}")
        if sign == -1 and rational >= 0:
            margin = rational if rational > 0 else radicand
            need(margin > 0, f"negative sqrt below nonnegative rational strictly:{axis}")
            relation = "NEGATIVE_SQRT_IS_STRICTLY_BELOW_NONNEGATIVE_RATIONAL"
        elif sign == -1:
            margin = radicand - rational * rational
            need(margin > 0, f"negative sqrt below negative rational by squares:{axis}")
            relation = "LOWER_NEGATIVE_SQRT_ABSOLUTE_VALUE_EXCEEDS_UPPER_NEGATIVE_RATIONAL"
        else:
            need(rational > 0, f"positive sqrt below rational sign:{axis}")
            margin = rational * rational - radicand
            need(margin > 0, f"positive sqrt below rational by squares:{axis}")
            relation = "LOWER_RADICAND_IS_STRICTLY_BELOW_UPPER_POSITIVE_RATIONAL_SQUARE"
        return {
            "axis": axis, "lower": lower, "upper": upper,
            "strict_relation": relation,
            "exact_positive_squared_comparison_margin": qwire(margin),
        }

    raise Failure(f"comparable exact algebraic endpoints:{axis}")


def volume_proof(bounds: list[dict[str, Any]]) -> dict[str, Any]:
    factors = [positive_width(bounds[2 * i], bounds[2 * i + 1], axis) for i, axis in enumerate(("t", "p", "s"))]
    all_rational = all("exact_positive_difference" in row for row in factors)
    proof: dict[str, Any] = {
        "dimension": 3,
        "strict_positive_width_factors": factors,
        "theorem": "PRODUCT_OF_THREE_STRICTLY_POSITIVE_EXACT_WIDTHS_IS_STRICTLY_POSITIVE",
        "common_open_interior_nonempty": True,
        "endpoint_inclusion_bits_irrelevant_to_open_interior_intersection": True,
    }
    if all_rational:
        volume = Fraction(1)
        for row in factors:
            volume *= Fraction(row["exact_positive_difference"])
        proof["exact_positive_rational_volume"] = qwire(volume)
    else:
        proof["exact_volume_form"] = "ALGEBRAIC_PRODUCT_OF_PINNED_POSITIVE_WIDTH_FACTORS"
    return proof


def load_chart_lineage() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    r179 = json.loads((ROOT / FILES["R179"][0]).read_bytes())
    packed = r179["result"]["retained_3d_child_rows"]
    map_179 = {row[0]: row[3] for row in packed}
    need(len(map_179) == len(packed), "R179 lineage uniqueness")

    r234 = json.loads((ROOT / FILES["R234"][0]).read_bytes())
    values = r234["result"]["resolved_descendant_rows"]
    map_234 = {row["materialized_row_id"]: row["chart"] for row in values}
    need(len(map_234) == len(values), "R234 lineage uniqueness")

    r236 = json.loads((ROOT / FILES["R236"][0]).read_bytes())
    values = r236["result"]["crossing_dependency_discharge_rows"]
    map_236 = {
        row["crossing_dependency_discharge_row_id"]: row["local_return_signature"]["source_chart"]
        for row in values
    }
    need(len(map_236) == len(values) == 32, "R236 lineage uniqueness")

    map_c5: dict[str, str] = {}
    for row in closed_rows(ROOT / FILES["C5"][0]):
        semantic = row["semantic_classification"]
        if semantic["classification"] == "EMPTY_GRAPH":
            map_c5[row["row_sha256"]] = semantic["kernel_parameters"]["source_chart"]
    need(len(map_c5) == 33_344, "C5 empty graph lineage")
    return map_179, map_234, map_236, map_c5


def chart_for(source: str, row: dict[str, Any], lineage: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]]) -> str:
    map_179, map_234, map_236, map_c5 = lineage
    if source == "C19A":
        chart = map_179[row["construction_certificate"]["retained_child_row_id"]]
    elif source == "C19B":
        key = row["construction_certificate"]["source_partition_row_id"]
        chart = map_234[key] if key.startswith("round234-resolved:") else map_236[key]
    elif source == "C19C":
        chart = map_c5[row["construction_certificate"]["C5_row_sha256"]]
    elif source in {"C20A", "C22A"}:
        chart = row["support_ast"]["coordinate_chart"]
    else:
        need(source == "C23A", "known primitive source")
        chart = row["support_ast"]["recharted_target_chart"]
    need(chart in {"G:E", "G:N", "G:W", "G:S"}, "four-chart lineage")
    return chart


def owner_for(row: dict[str, Any]) -> str:
    owner = row.get("member_id") or row.get("owner_member_id")
    need(type(owner) is str and owner != "", "owner member id")
    return owner


def component_for(row: dict[str, Any]) -> str:
    component = row.get("fresh_component_id") or row.get("owner_fresh_component_id")
    need(type(component) is str and component != "", "source component id")
    return component


def atom_id(source: str, row: dict[str, Any]) -> str:
    return f"primitive-same-chart-atom:{source}:{row['row_sha256']}"


def shuffled_batches(rows: Iterable[tuple[Any, ...]], rng: random.Random, size: int = 4096) -> Iterator[list[tuple[Any, ...]]]:
    batch: list[tuple[Any, ...]] = []
    for row in rows:
        batch.append(row)
        if len(batch) == size:
            rng.shuffle(batch)
            yield batch
            batch = []
    if batch:
        rng.shuffle(batch)
        yield batch


def make_database(path: Path) -> sqlite3.Connection:
    if path.exists():
        path.unlink()
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=OFF")
    db.execute("PRAGMA synchronous=OFF")
    db.execute("PRAGMA temp_store=FILE")
    db.execute("PRAGMA cache_size=-131072")
    db.execute("CREATE TABLE c15(member TEXT PRIMARY KEY, component TEXT NOT NULL, row_sha TEXT NOT NULL) WITHOUT ROWID")
    db.execute("CREATE TABLE c25(member TEXT PRIMARY KEY, component TEXT NOT NULL, row_sha TEXT NOT NULL, kernel TEXT NOT NULL, semantic TEXT NOT NULL) WITHOUT ROWID")
    db.execute("""CREATE TABLE atom(
        atom_id TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        source_row_sha TEXT NOT NULL,
        owner TEXT NOT NULL,
        source_component TEXT NOT NULL,
        chart TEXT NOT NULL,
        support_kind TEXT NOT NULL,
        bounds_json BLOB NOT NULL,
        box_key BLOB NOT NULL
    ) WITHOUT ROWID""")
    return db


def load_authorities(db: sqlite3.Connection) -> None:
    c15_rows = (
        (row["registry_member_id"], row["fresh_component_id"], row["row_sha256"])
        for row in closed_rows(ROOT / FILES["C15"][0])
    )
    count = 0
    for batch in shuffled_batches(c15_rows, random.Random(15), 8192):
        db.executemany("INSERT INTO c15 VALUES(?,?,?)", batch)
        count += len(batch)
    need(count == 502_204, "C15 full authority")

    c25_rows = (
        (
            row["member_id"], row["fresh_component_id"], row["row_sha256"],
            row["source_bindings"]["support_kernel"], row["support_semantic_kind"],
        )
        for row in closed_rows(ROOT / FILES["C25"][0])
    )
    count = 0
    for batch in shuffled_batches(c25_rows, random.Random(25), 8192):
        db.executemany("INSERT INTO c25 VALUES(?,?,?,?,?)", batch)
        count += len(batch)
    need(count == 502_204, "C25 full authority")
    db.commit()


def primitive_tuples(
    source: str,
    lineage: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]],
    c23_normalization: Counter[str],
) -> Iterator[tuple[Any, ...]]:
    for row in closed_rows(ROOT / FILES[source][0]):
        chart = chart_for(source, row, lineage)
        bounds = normalized_bounds(source, row["support_ast"])
        if source == "C23A":
            sign = row["support_ast"]["physical_t_sign"]
            c23_normalization[f"physical_t_sign:{sign:+d}"] += 1
            c23_normalization[
                "physical_t_endpoint_form:" + bounds[0]["kind"] + "/" + bounds[1]["kind"]
            ] += 1
            positive_width(bounds[0], bounds[1], "t")
        box_key = canonical([chart, bounds])
        yield (
            atom_id(source, row), source, row["row_sha256"], owner_for(row),
            component_for(row), chart, row["support_ast"]["kind"],
            canonical(bounds), box_key,
        )


def load_atoms(
    db: sqlite3.Connection,
    seed: int,
    lineage: tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str]],
) -> tuple[Counter[str], Counter[str]]:
    rng = random.Random(seed)
    counts: Counter[str] = Counter()
    c23_normalization: Counter[str] = Counter()
    for source, expected in SOURCE_COUNTS.items():
        for batch in shuffled_batches(
            primitive_tuples(source, lineage, c23_normalization), rng,
        ):
            db.executemany("INSERT INTO atom VALUES(?,?,?,?,?,?,?,?,?)", batch)
            counts[source] += len(batch)
        need(counts[source] == expected, f"primitive census:{source}")
        db.commit()
    need(sum(counts.values()) == 483_232, "483232 direct primitive atoms")
    db.execute("CREATE INDEX atom_box_key ON atom(box_key)")
    db.execute("CREATE INDEX atom_owner ON atom(owner)")
    db.commit()
    need(sum(c23_normalization[key] for key in c23_normalization if key.startswith("physical_t_sign:")) == 10_252,
         "C23 signed branch census")
    need(sum(c23_normalization[key] for key in c23_normalization if key.startswith("physical_t_endpoint_form:")) == 10_252,
         "C23 endpoint normalization census")
    return counts, c23_normalization


def validate_joins(db: sqlite3.Connection) -> dict[str, int]:
    gap = db.execute("""SELECT COUNT(*) FROM atom a
        LEFT JOIN c15 ON c15.member=a.owner LEFT JOIN c25 ON c25.member=a.owner
        WHERE c15.member IS NULL OR c25.member IS NULL""").fetchone()[0]
    component_mismatch = db.execute("""SELECT COUNT(*) FROM atom a
        JOIN c15 ON c15.member=a.owner JOIN c25 ON c25.member=a.owner
        WHERE a.source_component<>c15.component OR c15.component<>c25.component""").fetchone()[0]
    kernel_mismatch = 0
    for source, kernel in SOURCE_KERNEL.items():
        kernel_mismatch += db.execute("""SELECT COUNT(*) FROM atom a JOIN c25 ON c25.member=a.owner
            WHERE a.source=? AND c25.kernel<>?""", (source, kernel)).fetchone()[0]
    need(gap == component_mismatch == kernel_mismatch == 0, "complete C15/C25 primitive authority joins")
    distinct_owners = db.execute("SELECT COUNT(DISTINCT owner) FROM atom").fetchone()[0]
    need(distinct_owners == 482_380, "distinct primitive owners")
    return {
        "authority_join_gap": gap,
        "component_mismatch": component_mismatch,
        "support_kernel_mismatch": kernel_mismatch,
        "distinct_owner_count": distinct_owners,
    }


def member_row(record: tuple[Any, ...]) -> dict[str, Any]:
    (
        aid, source, source_sha, owner, component, chart, support_kind,
        bounds_raw, c15_sha, c25_sha, c25_kernel, c25_semantic,
    ) = record
    body = {
        "atom_id": aid,
        "owner_member_id": owner,
        "fresh_component_id": component,
        "source_kernel": source,
        "support_kind": support_kind,
        "chart": chart,
        "physical_bounds": json.loads(bounds_raw),
        "source_row_sha256": source_sha,
        "C15_member_row_sha256": c15_sha,
        "C25_member_row_sha256": c25_sha,
        "C25_support_kernel": c25_kernel,
        "C25_support_semantic_kind": c25_semantic,
    }
    return {**body, "member_row_sha256": digest(body)}


def reconstruct_groups(db: sqlite3.Connection) -> tuple[list[dict[str, Any]], dict[str, int]]:
    duplicate_groups = db.execute("SELECT COUNT(*) FROM (SELECT box_key FROM atom GROUP BY box_key HAVING COUNT(*)>1)").fetchone()[0]
    keys = [row[0] for row in db.execute("SELECT box_key FROM atom GROUP BY box_key HAVING COUNT(DISTINCT source_component)>1 ORDER BY box_key")]
    need(len(keys) == 228, "independent 228 cross-component equal-box groups")
    output: list[dict[str, Any]] = []
    total_members = 0
    total_components = 0
    cross_component_pairs = 0
    for key in keys:
        records = db.execute("""SELECT
                a.atom_id,a.source,a.source_row_sha,a.owner,a.source_component,
                a.chart,a.support_kind,a.bounds_json,c15.row_sha,c25.row_sha,
                c25.kernel,c25.semantic
            FROM atom a JOIN c15 ON c15.member=a.owner JOIN c25 ON c25.member=a.owner
            WHERE a.box_key=? ORDER BY a.source,a.atom_id""", (key,)).fetchall()
        members = [member_row(row) for row in records]
        components = sorted({row["fresh_component_id"] for row in members}, key=lambda x: x.encode("ascii"))
        need(len(components) > 1, "cross-component group")
        chart, bounds = json.loads(key)
        proof = volume_proof(bounds)
        group_id = "same-chart-exact-equal-positive-volume:" + digest([chart, bounds])
        component_counts = Counter(row["fresh_component_id"] for row in members)
        pair_count = 0
        for i, left in enumerate(components):
            for right in components[i + 1:]:
                pair_count += component_counts[left] * component_counts[right]
        body = {
            "schema": "cm2.c27.same-chart-exact-equal-cross-component-witness-group.v1",
            "group_id": group_id,
            "chart": chart,
            "physical_bounds": bounds,
            "strict_positive_volume_proof": proof,
            "member_count": len(members),
            "component_count": len(components),
            "fresh_component_ids": components,
            "cross_component_member_pair_count": pair_count,
            "members": members,
            "member_row_hashes_sha256": digest([row["member_row_sha256"] for row in members]),
            "legal_cross_component_physical_witness": True,
            "witness_reason": "DISTINCT_C15_COMPONENTS_SHARE_THE_SAME_NONEMPTY_OPEN_3D_INTERIOR_IN_ONE_CHART",
            "formal_credit": 0,
        }
        output.append({**body, "group_row_sha256": digest(body)})
        total_members += len(members)
        total_components += len(components)
        cross_component_pairs += pair_count
    output.sort(key=lambda row: row["group_id"].encode("ascii"))
    return output, {
        "duplicate_exact_box_group_count": duplicate_groups,
        "witness_group_count": len(output),
        "witness_member_count": total_members,
        "witness_component_occurrence_count": total_components,
        "cross_component_member_pair_count": cross_component_pairs,
    }


def write_groups(path: Path, groups: list[dict[str, Any]]) -> dict[str, Any]:
    sequence = hashlib.sha256()
    member_sequence = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as packed:
            for ordinal, source in enumerate(groups):
                body = dict(source)
                body["ordinal"] = ordinal
                body.pop("group_row_sha256", None)
                row = {**body, "group_row_sha256": digest(body)}
                sequence.update(bytes.fromhex(row["group_row_sha256"]))
                for member in row["members"]:
                    member_sequence.update(bytes.fromhex(member["member_row_sha256"]))
                packed.write(canonical(row) + b"\n")
    return {
        "filename": path.name,
        "row_count": len(groups),
        "sha256": file_hash(path),
        "size": path.stat().st_size,
        "group_row_sequence_sha256": sequence.hexdigest(),
        "flattened_member_row_sequence_sha256": member_sequence.hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    observed = {name: file_hash(ROOT / filename) for name, (filename, _) in FILES.items()}
    need(all(observed[name] == expected for name, (_, expected) in FILES.items()), "all primitive input pins")

    db_path = output_dir / "scratch.sqlite3"
    db = make_database(db_path)
    try:
        load_authorities(db)
        lineage = load_chart_lineage()
        source_counts, c23_normalization = load_atoms(db, args.seed, lineage)
        joins = validate_joins(db)
        groups, census = reconstruct_groups(db)
    finally:
        db.close()
        if db_path.exists():
            db_path.unlink()

    ledger = write_groups(output_dir / LEDGER, groups)
    semantic_projection = {
        "schema": "cm2.c27.same-chart-exact-equal-cross-component.sqlite-reconstruction.v1",
        "status": "PASS_ZERO_CREDIT__228_SAME_CHART_EXACT_EQUAL_POSITIVE_VOLUME_CROSS_C15_COMPONENT_WITNESS_GROUPS",
        "implementation": "INDEPENDENT_SQLITE_EXTERNAL_GROUPING_OVER_DIRECT_PRIMITIVE_ROWS",
        "candidate_universe": "DIRECT_C19A_C19B_C19C_C20A_C22A_C23A_ROWS_WITH_R179_R234_R236_C5_CHART_LINEAGE",
        "forbidden_inputs": {
            "same_chart_census_atom_ledger_opened_or_used": False,
            "C27_source_or_FAMILIES_imported_or_read": False,
            "old_edge_ledger_used_as_candidate_universe": False,
        },
        "primitive_atom_count": sum(source_counts.values()),
        "primitive_source_census": dict(source_counts),
        "C23_signed_sqrt_physical_normalization_census": dict(sorted(c23_normalization.items())),
        "authority_joins": joins,
        "witness_census": census,
        "all_witness_groups_have_strict_positive_volume": True,
        "all_witness_groups_cross_C15_components": True,
        "endpoint_bits_needed_for_these_witnesses": False,
        "group_ids_sha256": digest([row["group_id"] for row in groups]),
        "group_rows_sha256": digest([row["group_row_sha256"] for row in groups]),
        "ledger_semantic_commitments": {
            "group_row_count": ledger["row_count"],
            "group_row_sequence_sha256": ledger["group_row_sequence_sha256"],
            "flattened_member_row_sequence_sha256": ledger["flattened_member_row_sequence_sha256"],
        },
        "input_sha256": {FILES[name][0]: observed[name] for name in sorted(FILES)},
        "legal_cross_component_witness_found": True,
        "required_governance_action": "REBUILD_C27_THROUGH_C29__PATCHING_OR_PRESERVING_C29_UNCONDITIONAL_AUTHORITY_IS_FORBIDDEN",
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    body = {
        **semantic_projection,
        "declared_seed": args.seed,
        "declared_seed_used_for_pre_sort_sqlite_insertion_order": True,
        "invocation": {
            "command_argv": [
                sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                "--output-dir", str(output_dir), "--seed", str(args.seed),
            ],
            "isolated_runtime": True,
            "dont_write_bytecode": True,
        },
        "semantic_projection_sha256": digest(semantic_projection),
        "ledger": ledger,
    }
    result = {**body, "result_sha256": digest(body)}
    (output_dir / RESULT).write_bytes(canonical(result) + b"\n")
    print(canonical(result).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, KeyError, OSError, TypeError, ValueError, json.JSONDecodeError, sqlite3.Error) as error:
        print("REJECT_SAME_CHART_EXACT_EQUAL_SQLITE_RECONSTRUCTION:" + str(error), file=sys.stderr)
        raise SystemExit(2)
