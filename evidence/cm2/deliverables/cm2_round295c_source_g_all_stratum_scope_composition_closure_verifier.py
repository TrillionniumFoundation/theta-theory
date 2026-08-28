#!/usr/bin/env python3
"""Independent cacheless verifier for the Round295-C scope composition.

The Round295-C producer is inert evidence: this verifier never imports or
executes it.  It reconstructs the canonical Round289 relation table and the
eight-row all-stratum inventory from the sealed Round294, Round295-A, and
Round295-B inputs before opening either candidate output.
"""

from __future__ import annotations

import argparse
from collections import Counter
import copy
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round295c_source_g_all_stratum_scope_composition_closure"
PRODUCER = HERE / f"{PREFIX}.py"
CANDIDATE_LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
CANDIDATE_RESULT = HERE / f"{PREFIX}_result.json"
DEFAULT_OUTPUT = HERE / f"{PREFIX}_verification.json"
DEFAULT_ATTACK_OUTPUT = HERE / f"{PREFIX}_attack_suite.json"

R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R294_BINDINGS = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "representation_binding_ledger.json.gz"
)
R294_RESULT = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
)
R294_VERIFICATION = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "verification.json"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "manifest.sha256"
)
A_ALIASES = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "representation_alias_ledger.json.gz"
)
A_PHYSICAL = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
A_ABSENCE = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "absence_no_binding_ledger.json.gz"
)
A_RESULT = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "result.json"
)
A_VERIFICATION = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "verification.json"
)
A_ATTACKS = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "attack_suite.json"
)
A_MANIFEST = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "manifest.sha256"
)
B_LEDGER = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_ledger.json.gz"
)
B_RESULT = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_result.json"
)
B_VERIFICATION = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_"
    "verification.json"
)
B_MANIFEST = (
    "cm2_round295b_source_g_r289_terminal_face_absence_closure_"
    "manifest.sha256"
)

INPUT_PINS = {
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R294_BINDINGS:
        "f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833",
    R294_RESULT:
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    R294_VERIFICATION:
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    A_ALIASES:
        "5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f",
    A_PHYSICAL:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    A_ABSENCE:
        "9e28ee87b5a031a7f1c457d3fa26601925dbdf07dd5857c8e2108891891243b0",
    A_RESULT:
        "0deb8b9c88595762df3844b988af777a6b5f55347acbb8b9e8784308c2d4381d",
    A_VERIFICATION:
        "1b5c3423ea3854a8ae206677c740f31f5f9133edf66926271a10eec96b052349",
    A_ATTACKS:
        "ecf3da6b5be1d6e790d39240ee93f5457651f7e3605c6388e05a69c9027ece16",
    A_MANIFEST:
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    B_LEDGER:
        "1714945c470607a68c9fb5e323319899faabd187ecbccd00d266ea6f9361007c",
    B_RESULT:
        "b10c5caf9813887b06f2ed49796e02befc8abdc048e6909c2146bfc120e6334a",
    B_VERIFICATION:
        "f823fd7c7a34d39163bc887d6544ea670915e9ecb93fc2a94947f4ee777180a1",
    B_MANIFEST:
        "09cec800efc3c7dd21bebab4a226d384f51ec1273040c548bfa54834a25c8331",
}

SCHEMA = "cm2.round295c.source-g-all-stratum-scope-composition-closure.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"
ATTACK_SCHEMA = SCHEMA + ".attack-suite.v1"
ZERO_FIELDS = (
    "formal_new_occurrence_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)
EXPECTED_MULTIPLICITY = {
    1: 2388, 2: 632, 3: 312, 4: 40, 5: 32, 6: 16, 8: 72,
    9: 4, 10: 4, 11: 8, 12: 64, 14: 4, 16: 84, 18: 72,
    20: 8, 24: 8, 32: 8, 56: 8, 65: 8, 83: 8,
}


class VerificationError(RuntimeError):
    """Fail-closed verification error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)


def chunks(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode()


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for piece in chunks(value):
        state.update(piece)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1 << 20), b""):
            state.update(piece)
    return state.hexdigest()


def guard_path(
    path: Path,
    maximum: int = 2_000_000_000,
    allowed_parent: Path = HERE,
) -> bytes:
    need(
        path.parent == allowed_parent
        and path.parent.resolve() == allowed_parent.resolve(),
        f"path parent:{path}",
    )
    need(path.exists() and not path.is_symlink(), f"path exists:{path}")
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        f"path regular/link/size:{path}",
    )
    return path.read_bytes()


def strict_decode(raw: bytes, label: str) -> dict[str, Any]:
    need(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"strict bytes:{label}",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, f"duplicate key:{label}:{key}")
            result[key] = value
        return result

    def reject(token: str) -> Any:
        raise VerificationError(f"bad JSON token:{label}:{token}")

    value = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_float=reject,
        parse_constant=reject,
    )
    need(type(value) is dict, f"top object:{label}")
    return value


def read_json(name: str) -> dict[str, Any]:
    return strict_decode(guard_path(HERE / name), name)


def read_gzip_json(name: str) -> dict[str, Any]:
    try:
        raw = gzip.decompress(guard_path(HERE / name))
    except Exception as error:
        raise VerificationError(f"gzip:{name}") from error
    return strict_decode(raw, name)


def verify_self(value: dict[str, Any], field: str, label: str) -> None:
    claimed = value.get(field)
    payload = dict(value)
    payload.pop(field, None)
    need(claimed == digest(payload), f"self hash:{label}")


def validate_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(claimed == digest(payload), f"row hash:{label}")


def close_row(
    prefix: str, domain: str, id_field: str, payload: dict[str, Any]
) -> dict[str, Any]:
    row = {id_field: prefix + digest([domain, payload]), **payload}
    row["row_sha256"] = digest(row)
    return row


class ListCommitment:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for piece in chunks(value):
            self.state.update(piece)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def rows_commitment(
    rows: list[dict[str, Any]], id_field: str
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), f"unique ids:{id_field}")
    return {
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": digest(rows),
    }


def nested(
    table: dict[str, Any], id_field: str, count: int, label: str
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = table["rows"]
    need(len(rows) == table["row_count"] == count, f"count:{label}")
    for row in rows:
        validate_row(row, label)
    commitment = rows_commitment(rows, id_field)
    need(
        all(table[key] == commitment[key] for key in commitment),
        f"commitment:{label}",
    )
    return rows, commitment


def scan_rows(
    name: str, visit: Callable[[dict[str, Any]], None]
) -> dict[str, Any]:
    path = HERE / name
    guard_path(path)
    decoder = json.JSONDecoder(
        object_pairs_hook=lambda pairs: dict(pairs),
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    marker = '"rows":['
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        prefix = ""
        while marker not in prefix:
            piece = stream.read(1 << 20)
            need(bool(piece), f"marker:{name}")
            prefix += piece
        before, buffer = prefix.split(marker, 1)
        count = 0
        while True:
            buffer = buffer.lstrip()
            if buffer.startswith(","):
                buffer = buffer[1:].lstrip()
            if buffer.startswith("]"):
                buffer = buffer[1:]
                break
            while True:
                try:
                    row, end = decoder.raw_decode(buffer)
                    break
                except json.JSONDecodeError:
                    piece = stream.read(1 << 20)
                    need(bool(piece), f"truncated:{name}:{count}")
                    buffer += piece
            need(type(row) is dict, f"row object:{name}:{count}")
            visit(row)
            count += 1
            buffer = buffer[end:]
        suffix = buffer + stream.read()
    metadata = strict_decode(
        (before + '"rows":[]' + suffix).encode(), f"{name}:metadata"
    )
    need(metadata["rows"] == [], f"metadata rows:{name}")
    metadata["streamed_row_count"] = count
    return metadata


def parse_manifest(name: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in guard_path(HERE / name, 100_000).decode().splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{name}")
        sha256, filename = match.groups()
        need(filename not in result, f"manifest duplicate:{name}")
        result[filename] = sha256
    return result


def rectangle_area(values: list[str]) -> Q:
    need(len(values) == 4, "rectangle arity")
    p0, p1, s0, s1 = map(Q, values)
    need(p0 < p1 and s0 < s1, "positive rectangle")
    return (p1 - p0) * (s1 - s0)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", fileobj=buffer, mode="wb", mtime=0, compresslevel=9
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return buffer.getvalue()


def safe_write(path: Path, payload: bytes) -> None:
    need(path.parent.resolve() == HERE.resolve(), f"output parent:{path}")
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=HERE, prefix=f".{path.name}.", delete=False
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def validate_frozen_inputs() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], str
]:
    producer_sha256 = file_sha256(PRODUCER)
    for name, expected in INPUT_PINS.items():
        need(file_sha256(HERE / name) == expected, f"pin:{name}")
    for manifest_name, members in (
        (
            R294_MANIFEST,
            (R294_REGISTRY, R294_BINDINGS, R294_RESULT, R294_VERIFICATION),
        ),
        (
            A_MANIFEST,
            (
                A_ALIASES, A_PHYSICAL, A_ABSENCE, A_RESULT,
                A_VERIFICATION, A_ATTACKS,
            ),
        ),
        (B_MANIFEST, (B_LEDGER, B_RESULT, B_VERIFICATION)),
    ):
        manifest = parse_manifest(manifest_name)
        for member in members:
            need(
                manifest.get(member) == INPUT_PINS[member],
                f"manifest:{manifest_name}:{member}",
            )
    r294 = read_json(R294_RESULT)
    ra = read_json(A_RESULT)
    rb = read_json(B_RESULT)
    v294 = read_json(R294_VERIFICATION)
    va = read_json(A_VERIFICATION)
    vb = read_json(B_VERIFICATION)
    verify_self(r294, "result_sha256", "R294")
    verify_self(ra, "result_sha256", "R295A")
    verify_self(rb, "result_sha256", "R295B")
    verify_self(v294, "verification_sha256", "R294 verification")
    verify_self(va, "verification_sha256", "R295A verification")
    verify_self(vb, "verification_sha256", "R295B verification")
    need(
        r294["census"]["formal_occurrence_registry_row_count"] == 431_208
        and r294["census"]["formal_representation_binding_count"] == 46_288
        and ra["formal_credit_transition"][
            "formal_representation_binding_count_after"
        ] == 46_564
        and ra["atomic_R291_binding_census"][
            "formal_unresolved_physical_witness_count"
        ] == 0
        and rb["corrected_relation_census"][
            "remaining_R289_terminal_face_frontier_count"
        ] == 0
        and rb["strict_nonpromotion"][
            "true_seam_directed_endpoint_cell_count"
        ] == 152
        and rb["strict_nonpromotion"]["formal_true_seam_edge_count"] == 0
        and v294["status"].startswith("PASS_INDEPENDENT_CACHELESS_ROUND294")
        and va["status"].startswith("PASS_INDEPENDENT_CACHELESS_ROUND295A")
        and vb["status"].startswith("PASS_INDEPENDENT_CACHELESS_ROUND295B"),
        "sealed input semantics",
    )
    return r294, ra, rb, producer_sha256


def independently_reconstruct_expected() -> dict[str, Any]:
    r294, _ra, _rb, producer_sha256 = validate_frozen_inputs()

    alias_doc = read_gzip_json(A_ALIASES)
    aliases, alias_commitment = nested(
        alias_doc,
        "Round295A_retained_continuation_alias_row_id",
        276,
        "A aliases",
    )
    aphysical_doc = read_gzip_json(A_PHYSICAL)
    aphysical, aphysical_commitment = nested(
        aphysical_doc,
        "Round295A_R291_physical_incidence_binding_row_id",
        113_452,
        "A physical",
    )
    need(
        sum(
            row["target_Round294_registry_reference_count"]
            for row in aphysical
        ) == 225_304
        and Counter(
            row["target_Round294_registry_reference_count"]
            for row in aphysical
        ) == {1: 1_600, 2: 111_852},
        "independent A physical census",
    )
    del aphysical, aphysical_doc
    aabsence_doc = read_gzip_json(A_ABSENCE)
    aabsence, aabsence_commitment = nested(
        aabsence_doc,
        "Round295A_R291_absence_no_binding_row_id",
        28_016,
        "A absence",
    )
    need(
        all(
            row["target_Round294_registry_reference_count"] == 0
            for row in aabsence
        ),
        "independent A absence census",
    )
    del aabsence, aabsence_doc

    bdoc = read_gzip_json(B_LEDGER)
    brelations, brelation_commitment = nested(
        bdoc["corrected_relation_disposition_ledger"],
        "Round295B_corrected_relation_disposition_row_id",
        9_528,
        "B relations",
    )
    bphysical, bphysical_commitment = nested(
        bdoc["physical_incidence_binding_ledger"],
        "Round295B_physical_incidence_binding_row_id",
        11_448,
        "B physical",
    )
    bwrong, bwrong_commitment = nested(
        bdoc["wrong_signed_empty_no_binding_ledger"],
        "Round295B_wrong_signed_empty_no_binding_row_id",
        468,
        "B wrong",
    )
    bgraph, bgraph_commitment = nested(
        bdoc["graph_separated_no_binding_ledger"],
        "Round295B_graph_separated_no_binding_row_id",
        288,
        "B graph",
    )

    raw_by_child = {
        row["Round295B_physical_incidence_binding_row_id"]:
            row["formal_Round294_occurrence_id"]
        for row in bphysical
    }
    raw_values = set(raw_by_child.values())
    need(len(raw_values) == 3_780, "raw B target count")

    registry_ids: set[str] = set()
    by_source: dict[str, list[str]] = {}
    target_metadata: dict[str, dict[str, Any]] = {}
    occurrence_commitment = ListCommitment()
    registry_id_commitment = ListCommitment()
    registry_hash_commitment = ListCommitment()
    registry_rows_commitment = ListCommitment()

    def registry_visit(row: dict[str, Any]) -> None:
        validate_row(row, "R294 registry")
        occurrence = row["registry_occurrence_id"]
        source = row["source_row_id"]
        need(occurrence not in registry_ids, "registry occurrence injective")
        registry_ids.add(occurrence)
        occurrence_commitment.add(occurrence)
        registry_id_commitment.add(row["Round294_occurrence_registry_row_id"])
        registry_hash_commitment.add(row["row_sha256"])
        registry_rows_commitment.add(row)
        if occurrence in raw_values or source in raw_values:
            target_metadata[occurrence] = {
                "registry_occurrence_id": occurrence,
                "Round294_occurrence_registry_row_id":
                    row["Round294_occurrence_registry_row_id"],
                "Round294_occurrence_registry_row_sha256":
                    row["row_sha256"],
                "registry_entry_kind": row["registry_entry_kind"],
                "source_occurrence_class": row["source_occurrence_class"],
                "source_row_id": source,
            }
        if source in raw_values:
            by_source.setdefault(source, []).append(occurrence)

    registry_meta = scan_rows(R294_REGISTRY, registry_visit)
    expected_registry = r294["registry_ledger"]
    registry_commitment = {
        "row_count": registry_meta["streamed_row_count"],
        "occurrence_ids_sha256": occurrence_commitment.finish(),
        "row_ids_sha256": registry_id_commitment.finish(),
        "row_hashes_sha256": registry_hash_commitment.finish(),
        "rows_sha256": registry_rows_commitment.finish(),
    }
    need(
        registry_meta["streamed_row_count"]
        == registry_meta["row_count"] == 431_208
        and all(
            registry_commitment[key] == expected_registry[key]
            for key in registry_commitment
        ),
        "independent full registry commitment",
    )
    direct_values = raw_values & registry_ids
    indirect_values = raw_values - registry_ids
    need(
        len(direct_values) == 356
        and len(indirect_values) == 3_424
        and set(by_source) == indirect_values
        and all(len(by_source[source]) == 1 for source in indirect_values),
        "independent source-row normalization function",
    )
    normalized_by_raw = {
        raw: raw if raw in direct_values else by_source[raw][0]
        for raw in raw_values
    }
    converted_targets = {
        normalized_by_raw[raw] for raw in indirect_values
    }
    direct_targets = set(direct_values)
    normalized_targets = converted_targets | direct_targets
    need(
        len(converted_targets) == 3_424
        and len(direct_targets) == 356
        and not converted_targets & direct_targets
        and len(normalized_targets) == 3_780
        and normalized_targets <= registry_ids
        and normalized_targets <= set(target_metadata),
        "independent normalized target universe",
    )
    normalized_by_child = {
        child: normalized_by_raw[raw]
        for child, raw in raw_by_child.items()
    }
    converted_rows = sum(raw in indirect_values for raw in raw_by_child.values())
    direct_rows = len(raw_by_child) - converted_rows
    target_uses = Counter(normalized_by_child.values())
    multiplicity = Counter(target_uses.values())
    prefix_histogram = Counter(
        target.split(":", 1)[0] for target in normalized_targets
    )
    need(
        converted_rows == 5_292
        and direct_rows == 6_156
        and multiplicity == EXPECTED_MULTIPLICITY
        and prefix_histogram == {
            "source-g-expanded-occurrence": 3_728,
            "round182-collar-leaf": 32,
            "round179-resolved-child": 20,
        },
        "independent target normalization census",
    )

    # Independently recommit the prior representation table and append the
    # already verified A alias rows in their sealed order.
    prior_ids = ListCommitment()
    prior_hashes = ListCommitment()
    prior_rows = ListCommitment()
    composed_ids = ListCommitment()
    composed_hashes = ListCommitment()
    composed_rows = ListCommitment()

    def binding_visit(row: dict[str, Any]) -> None:
        validate_row(row, "R294 binding")
        row_id = row[
            "Round294_occurrence_representation_binding_row_id"
        ]
        prior_ids.add(row_id)
        prior_hashes.add(row["row_sha256"])
        prior_rows.add(row)
        composed_ids.add(row_id)
        composed_hashes.add(row["row_sha256"])
        composed_rows.add(row)

    binding_meta = scan_rows(R294_BINDINGS, binding_visit)
    sealed_binding = r294["representation_binding_ledger"]
    need(
        binding_meta["streamed_row_count"]
        == binding_meta["row_count"] == 46_288
        and prior_ids.finish() == sealed_binding["row_ids_sha256"]
        and prior_hashes.finish() == sealed_binding["row_hashes_sha256"]
        and prior_rows.finish() == sealed_binding["rows_sha256"],
        "independent prior representation commitment",
    )
    for row in aliases:
        composed_ids.add(row["Round295A_retained_continuation_alias_row_id"])
        composed_hashes.add(row["row_sha256"])
        composed_rows.add(row)
    representation_commitment = {
        "row_count": 46_564,
        "row_ids_sha256": composed_ids.finish(),
        "row_hashes_sha256": composed_hashes.finish(),
        "rows_sha256": composed_rows.finish(),
    }

    physical_by_id = {
        row["Round295B_physical_incidence_binding_row_id"]: row
        for row in bphysical
    }
    wrong_by_id = {
        row["Round295B_wrong_signed_empty_no_binding_row_id"]: row
        for row in bwrong
    }
    graph_by_id = {
        row["Round295B_graph_separated_no_binding_row_id"]: row
        for row in bgraph
    }
    relation_output: list[dict[str, Any]] = []
    used_physical: set[str] = set()
    used_wrong: set[str] = set()
    used_graph: set[str] = set()
    patch_ids: set[str] = set()
    patch_sides: set[tuple[str, int]] = set()
    disposition_histogram: Counter[str] = Counter()
    assignments: list[list[str]] = []

    for source in sorted(
        brelations,
        key=lambda row: row["Round289_region_cell_relation_id"],
    ):
        relation_id = source["Round289_region_cell_relation_id"]
        patch = source["Round268_true_seam_patch_row_id"]
        side = source["side_index"]
        patch_ids.add(patch)
        patch_sides.add((patch, side))
        physical_ids = source["physical_row_ids"]
        wrong_ids = source["wrong_signed_empty_no_binding_row_ids"]
        graph_ids = source["graph_no_binding_proof_ids"]
        need(
            len(physical_ids)
            == source["physical_incidence_binding_row_count"]
            and len(wrong_ids)
            == source["wrong_signed_empty_no_binding_row_count"]
            and len(graph_ids)
            == source["graph_separated_no_binding_row_count"]
            and len(physical_ids) == len(set(physical_ids))
            and len(wrong_ids) == len(set(wrong_ids))
            and len(graph_ids) == len(set(graph_ids)),
            f"independent relation child arity:{relation_id}",
        )

        physical_children: list[dict[str, Any]] = []
        physical_area = Q(0)
        for child_id in physical_ids:
            child = physical_by_id[child_id]
            need(
                child_id not in used_physical
                and child["Round289_region_cell_relation_id"] == relation_id,
                f"independent physical ownership:{child_id}",
            )
            used_physical.add(child_id)
            area = rectangle_area(child["exact_physical_ps_subcell"])
            need(
                area == Q(child["exact_physical_ps_area"]),
                f"independent physical area:{child_id}",
            )
            physical_area += area
            raw_target = child["formal_Round294_occurrence_id"]
            canonical_target = normalized_by_raw[raw_target]
            assignments.append([child_id, canonical_target])
            target = target_metadata[canonical_target]
            physical_children.append({
                "source_Round295B_physical_incidence_binding_row_id":
                    child_id,
                "source_Round295B_row_sha256": child["row_sha256"],
                "source_field_formal_Round294_occurrence_id": raw_target,
                "target_normalization_classification": (
                    "CONVERTED_FROM_ROUND294_SOURCE_ROW_ID"
                    if raw_target in indirect_values
                    else "ALREADY_CANONICAL_ROUND294_REGISTRY_OCCURRENCE_ID"
                ),
                "canonical_Round294_registry_occurrence_id":
                    canonical_target,
                "Round294_occurrence_registry_row_id":
                    target["Round294_occurrence_registry_row_id"],
                "Round294_occurrence_registry_row_sha256":
                    target["Round294_occurrence_registry_row_sha256"],
                "Round294_registry_entry_kind":
                    target["registry_entry_kind"],
                "exact_physical_ps_subcell":
                    child["exact_physical_ps_subcell"],
                "exact_physical_ps_area": child["exact_physical_ps_area"],
            })

        wrong_children: list[dict[str, Any]] = []
        wrong_area = Q(0)
        for child_id in wrong_ids:
            child = wrong_by_id[child_id]
            need(
                child_id not in used_wrong
                and child["Round289_region_cell_relation_id"] == relation_id
                and child["terminal_registry_target_reference_count"] == 0,
                f"independent wrong ownership:{child_id}",
            )
            used_wrong.add(child_id)
            area = rectangle_area(
                child["exact_empty_intersection_ps_rectangle"]
            )
            need(
                area == Q(child["exact_empty_intersection_ps_area"]),
                f"independent wrong area:{child_id}",
            )
            wrong_area += area
            wrong_children.append({
                "source_Round295B_wrong_signed_empty_no_binding_row_id":
                    child_id,
                "source_Round295B_row_sha256": child["row_sha256"],
                "exact_empty_intersection_ps_rectangle":
                    child["exact_empty_intersection_ps_rectangle"],
                "exact_empty_intersection_ps_area":
                    child["exact_empty_intersection_ps_area"],
                "no_binding_classification":
                    child["no_binding_classification"],
            })

        graph_children: list[dict[str, Any]] = []
        graph_area = Q(0)
        for child_id in graph_ids:
            child = graph_by_id[child_id]
            need(
                child_id not in used_graph
                and child["Round289_region_cell_relation_id"] == relation_id
                and child["terminal_registry_target_reference_count"] == 0,
                f"independent graph ownership:{child_id}",
            )
            used_graph.add(child_id)
            area = rectangle_area(child["exact_relation_ps_rectangle"])
            need(
                area == Q(child["exact_relation_ps_area"]),
                f"independent graph area:{child_id}",
            )
            graph_area += area
            graph_children.append({
                "source_Round295B_graph_separated_no_binding_row_id":
                    child_id,
                "source_Round295B_row_sha256": child["row_sha256"],
                "exact_graph_separated_ps_rectangle":
                    child["exact_relation_ps_rectangle"],
                "exact_graph_separated_ps_area":
                    child["exact_relation_ps_area"],
                "no_binding_classification":
                    child["no_binding_classification"],
            })

        relation_area = rectangle_area(source["exact_relation_ps_rectangle"])
        need(
            relation_area == Q(source["exact_relation_ps_area"])
            and physical_area == Q(source["exact_physical_ps_area"])
            and wrong_area == Q(source["exact_wrong_signed_empty_ps_area"])
            and graph_area == Q(source["exact_graph_separated_ps_area"])
            and relation_area == physical_area + wrong_area + graph_area
            and source["remaining_terminal_face_frontier_cell_count"] == 0
            and source["remaining_terminal_face_frontier_ps_area"] == "0",
            f"independent relation conservation:{relation_id}",
        )
        disposition = source["corrected_relation_disposition"]
        disposition_histogram[disposition] += 1
        payload = {
            "source_Round295B_corrected_relation_disposition_row_id":
                source["Round295B_corrected_relation_disposition_row_id"],
            "source_Round295B_row_sha256": source["row_sha256"],
            "Round289_region_cell_relation_id": relation_id,
            "Round268_true_seam_patch_row_id": patch,
            "Round275_region_id": source["Round275_region_id"],
            "side_index": side,
            "source_relation_classification":
                source["source_relation_classification"],
            "canonical_relation_disposition": disposition,
            "exact_relation_ps_rectangle":
                source["exact_relation_ps_rectangle"],
            "exact_relation_ps_area": qstr(relation_area),
            "exact_physical_ps_area": qstr(physical_area),
            "exact_wrong_signed_empty_ps_area": qstr(wrong_area),
            "exact_graph_separated_ps_area": qstr(graph_area),
            "physical_children": physical_children,
            "wrong_signed_empty_children": wrong_children,
            "graph_separated_children": graph_children,
            "physical_child_count": len(physical_children),
            "wrong_signed_empty_child_count": len(wrong_children),
            "graph_separated_child_count": len(graph_children),
            "canonical_Round294_target_reference_count":
                len(physical_children),
            "canonical_Round294_target_occurrence_ids": [
                child["canonical_Round294_registry_occurrence_id"]
                for child in physical_children
            ],
            "per_relation_child_lists_complete": True,
            "per_relation_exact_ps_area_conserved": True,
            "remaining_relation_scope_frontier_count": 0,
            "formal_existing_occurrence_physical_incidence_binding_credit":
                len(physical_children),
            **{field: 0 for field in ZERO_FIELDS},
        }
        relation_output.append(close_row(
            "round295c-canonical-r289-relation:",
            "ROUND295C_CANONICAL_R289_RELATION_V1",
            "Round295C_canonical_R289_relation_disposition_row_id",
            payload,
        ))

    relation_output.sort(
        key=lambda row: row[
            "Round295C_canonical_R289_relation_disposition_row_id"
        ]
    )
    need(
        used_physical == set(physical_by_id)
        and used_wrong == set(wrong_by_id)
        and used_graph == set(graph_by_id)
        and len(patch_ids) == 24
        and len(patch_sides) == 40
        and len(assignments) == 11_448
        and disposition_histogram == {
            "WHOLE_PHYSICAL_EXISTING_OCCURRENCE_INCIDENCE": 8_844,
            "MIXED_PHYSICAL_EXISTING_OCCURRENCE_AND_WRONG_SIGNED_EMPTY_"
            "ABSENCE": 392,
            "WHOLE_WRONG_SIGNED_EMPTY_ABSENCE__NO_BINDING": 4,
            "GRAPH_SEPARATED_ABSENCE__NO_BINDING": 288,
        },
        "independent complete relation partition",
    )
    relation_commitment = rows_commitment(
        relation_output,
        "Round295C_canonical_R289_relation_disposition_row_id",
    )
    assignments.sort()

    def inventory(
        slot: int, table_name: str, fields: dict[str, Any]
    ) -> dict[str, Any]:
        return close_row(
            "round295c-all-stratum-inventory:",
            "ROUND295C_ALL_STRATUM_SCOPE_INVENTORY_V1",
            "Round295C_all_stratum_scope_inventory_row_id",
            {
                "scope_slot": slot,
                "scope_table_name": table_name,
                **fields,
                "unresolved_scope_row_count": 0,
                **{field: 0 for field in ZERO_FIELDS},
            },
        )

    inventory_rows = [
        inventory(1, "ROUND294_OCCURRENCE_REGISTRY", {
            **registry_commitment,
            "channel_provenance": "SEALED_ROUND294_OCCURRENCE_IDENTITY",
            "source_artifact": R294_REGISTRY,
            "formal_target_reference_count": 0,
        }),
        inventory(2, "COMPOSED_REPRESENTATION_BINDINGS_AND_ALIASES", {
            **representation_commitment,
            "channel_provenance":
                "ROUND294_46288_BINDINGS_PLUS_ROUND295A_276_ALIASES",
            "source_artifacts": [R294_BINDINGS, A_ALIASES],
            "formal_prior_representation_binding_count": 46_288,
            "formal_Round295A_alias_delta": 276,
            "formal_target_reference_count": 0,
        }),
        inventory(3, "ROUND291_PHYSICAL_INCIDENCE", {
            **aphysical_commitment,
            "channel_provenance":
                "ROUND295A_COMPLETE_R291_PHYSICAL_INCIDENCE",
            "source_artifact": A_PHYSICAL,
            "formal_target_reference_count": 225_304,
            "unique_target_witness_row_count": 1_600,
            "multi_target_witness_row_count": 111_852,
        }),
        inventory(4, "ROUND291_ABSENCE_NO_BINDING", {
            **aabsence_commitment,
            "channel_provenance":
                "ROUND295A_COMPLETE_R291_ABSENCE_EVIDENCE",
            "source_artifact": A_ABSENCE,
            "formal_target_reference_count": 0,
        }),
        inventory(5, "CANONICAL_ROUND289_RELATIONS", {
            **relation_commitment,
            "source_Round295B_row_ids_sha256":
                brelation_commitment["row_ids_sha256"],
            "source_Round295B_row_hashes_sha256":
                brelation_commitment["row_hashes_sha256"],
            "source_Round295B_rows_sha256":
                brelation_commitment["rows_sha256"],
            "channel_provenance":
                "ROUND295C_CANONICAL_RELATION_COMPOSITION",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 11_448,
        }),
        inventory(6, "NORMALIZED_ROUND289_PHYSICAL_INCIDENCE", {
            **bphysical_commitment,
            "channel_provenance":
                "ROUND295B_PHYSICAL_WITH_ROUND295C_CANONICAL_TARGETS",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 11_448,
            "canonical_target_assignments_sha256": digest(assignments),
            "canonical_unique_target_ids_sha256":
                digest(sorted(normalized_targets)),
            "canonical_unique_target_count": 3_780,
        }),
        inventory(7, "ROUND289_WRONG_SIGNED_ABSENCE", {
            **bwrong_commitment,
            "channel_provenance":
                "ROUND295B_WRONG_SIGNED_EMPTY_NO_BINDING_EVIDENCE",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 0,
        }),
        inventory(8, "ROUND289_GRAPH_SEPARATED_ABSENCE", {
            **bgraph_commitment,
            "channel_provenance":
                "ROUND295B_GRAPH_SEPARATED_NO_BINDING_EVIDENCE",
            "source_artifact": B_LEDGER,
            "formal_target_reference_count": 0,
        }),
    ]
    inventory_rows.sort(key=lambda row: row["scope_slot"])
    inventory_commitment = rows_commitment(
        inventory_rows,
        "Round295C_all_stratum_scope_inventory_row_id",
    )
    need(
        len(inventory_rows) == 8
        and [row["row_count"] for row in inventory_rows]
        == [431_208, 46_564, 113_452, 28_016, 9_528, 11_448, 468, 288],
        "independent eight-row inventory",
    )

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status":
            "PASS_ROUND295C_CANONICAL_R289_RELATIONS_AND_ALL_STRATUM_"
            "SCOPE_INVENTORY__9528_RELATIONS__8_INVENTORY_ROWS__"
            "ALL_TARGETS_CANONICAL_ROUND294_IDS__UNRESOLVED_SCOPE_ZERO",
        "canonical_R289_relation_disposition_ledger": {
            **relation_commitment,
            "rows": relation_output,
        },
        "all_stratum_scope_inventory_ledger": {
            **inventory_commitment,
            "rows": inventory_rows,
        },
    }
    ledger_bytes = deterministic_gzip(ledger)

    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND295C_ALL_STRATUM_SCOPE_COMPOSITION_CLOSURE__"
            "R291_576_TO_ZERO__R289_396_TO_ZERO__"
            "NORMALIZED_R289_TARGETS_3780__UNRESOLVED_SCOPE_ZERO__"
            "NO_SEAM_COMPONENT_OR_DSU_PROMOTION",
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "sealed_package_consumption": {
            "Round294_registry_row_count": 431_208,
            "Round294_representation_binding_count": 46_288,
            "Round295A_alias_delta": 276,
            "post_Round295A_representation_binding_count": 46_564,
            "Round295A_manifest_sha256": INPUT_PINS[A_MANIFEST],
            "Round295B_manifest_sha256": INPUT_PINS[B_MANIFEST],
            "complete_Round294_registry_streamed_and_recommitted": True,
            "complete_Round294_binding_ledger_streamed_and_recommitted":
                True,
        },
        "Round289_target_normalization": {
            "physical_row_count": 11_448,
            "converted_from_Round294_source_row_id_count": 5_292,
            "converted_unique_source_row_id_count": 3_424,
            "already_canonical_registry_occurrence_id_count": 6_156,
            "already_canonical_unique_target_count": 356,
            "converted_and_already_canonical_target_set_overlap_count": 0,
            "canonical_unique_Round294_target_count": 3_780,
            "all_canonical_targets_present_in_complete_Round294_registry":
                True,
            "canonical_target_prefix_histogram": {
                key: value for key, value in sorted(prefix_histogram.items())
            },
            "canonical_target_use_multiplicity_histogram": {
                str(key): value for key, value in sorted(multiplicity.items())
            },
            "misnamed_source_field_copied_as_occurrence_ID": False,
            "normalization_source":
                "INDEPENDENT_COMPLETE_ROUND294_SOURCE_ROW_TO_"
                "REGISTRY_OCCURRENCE_ID_MAP",
            "number_5784_belongs_only_to":
                "ROUND296_COMBINED_STRICT_PLUS_B_SEAM_ENDPOINT_UNIVERSE",
            "number_5784_used_as_Round295C_B_target_count": False,
        },
        "canonical_R289_relation_census": {
            "relation_count": 9_528,
            "physical_relation_count": 9_236,
            "whole_physical_relation_count": 8_844,
            "mixed_physical_and_empty_relation_count": 392,
            "absent_relation_count": 292,
            "whole_wrong_signed_empty_relation_count": 4,
            "graph_separated_absent_relation_count": 288,
            "physical_child_count": 11_448,
            "wrong_signed_empty_child_count": 468,
            "graph_separated_child_count": 288,
            "all_child_IDs_covered_exactly_once": True,
            "all_relations_exact_ps_area_conserved": True,
            "remaining_R289_relation_scope_frontier_count": 0,
        },
        "all_stratum_scope_census": {
            "inventory_row_count": 8,
            "formal_occurrence_registry_row_count": 431_208,
            "formal_representation_binding_and_alias_count": 46_564,
            "Round291_physical_incidence_row_count": 113_452,
            "Round291_target_reference_count": 225_304,
            "Round291_absence_no_binding_row_count": 28_016,
            "Round289_relation_row_count": 9_528,
            "Round289_physical_incidence_row_count": 11_448,
            "Round289_wrong_signed_no_binding_row_count": 468,
            "Round289_graph_no_binding_row_count": 288,
            "formal_physical_incidence_channel_total": 124_900,
            "formal_no_binding_evidence_channel_total": 28_772,
            "physical_channels_merged_as_identity_aliases": False,
            "no_binding_channels_merged_as_occurrences": False,
            "Round291_gap_before": 576,
            "Round291_gap_after": 0,
            "Round289_gap_before": 396,
            "Round289_gap_after": 0,
            "unresolved_all_stratum_scope_count": 0,
        },
        "strict_nonpromotion": {
            "formal_registry_delta": 0,
            "formal_alias_delta_from_Round294": 276,
            "formal_new_occurrence_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_seam_edge_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "distinct_Round268_true_seam_patch_IDs_in_relation_scope": 24,
            "distinct_Round268_patch_side_pairs_in_relation_scope": 40,
            "true_seam_directed_endpoint_cell_relation_scope_count": 152,
            "directed_endpoint_cell_count_source":
                "SEALED_ROUND295B_RESULT_STRICT_NONPROMOTION",
            "directed_endpoint_cells_are_seam_edges": False,
            "all_152_true_seam_patch_edge_pairing_status":
                "DEFERRED_TO_INDEPENDENT_ROUND296",
            "true_seam_endpoint_pairing_status":
                "DEFERRED_TO_INDEPENDENT_ROUND296",
            "post_Round294_expanded_registry_component_DSU_status":
                "NOT_REBUILT",
            "post_Round295C_quotient_component_count": None,
            "legacy_pre_Round294_quotient_component_count": 63_224,
            "legacy_count_is_current_post_Round294_quotient": False,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "ledger": {
            "filename": CANDIDATE_LEDGER.name,
            "schema": LEDGER_SCHEMA,
            "canonical_R289_relation_row_count": 9_528,
            "canonical_R289_relation_rows_sha256":
                relation_commitment["rows_sha256"],
            "all_stratum_scope_inventory_row_count": 8,
            "all_stratum_scope_inventory_rows_sha256":
                inventory_commitment["rows_sha256"],
            "file_sha256": hashlib.sha256(ledger_bytes).hexdigest(),
        },
        "required_next": [
            "Independently verify the complete Round295-C composition and "
            "target normalization before consuming it.",
            "Pair all 152 true-seam patches/edges only in the independent "
            "Round296 seam-edge closure; do not reinterpret the separate "
            "Round295-B 152 directed endpoint-cell census as edges.",
            "Build the expanded all-stratum component/DSU edge ledger only "
            "after the seam pairing is sealed.",
        ],
        "provenance": {
            "producer_sha256": producer_sha256,
            "seed_affects_output": False,
            "Round295A_or_Round295B_producer_imported_or_executed": False,
            "Round296_input_used": False,
        },
        "seed_affects_output": False,
    }
    result["result_sha256"] = digest(result)
    result_bytes = canonical(result)
    return {
        "ledger": ledger,
        "result": result,
        "ledger_bytes": ledger_bytes,
        "result_bytes": result_bytes,
        "normalization_audit": {
            "converted_rows": converted_rows,
            "converted_unique": len(converted_targets),
            "already_rows": direct_rows,
            "already_unique": len(direct_targets),
            "set_overlap": len(converted_targets & direct_targets),
            "normalized_unique": len(normalized_targets),
            "prefix_histogram":
                dict(sorted(prefix_histogram.items())),
            "multiplicity_histogram": {
                str(key): value for key, value in sorted(multiplicity.items())
            },
        },
    }


def resign_relation(row: dict[str, Any]) -> dict[str, Any]:
    id_field = "Round295C_canonical_R289_relation_disposition_row_id"
    payload = {
        key: value for key, value in row.items()
        if key not in {id_field, "row_sha256"}
    }
    return close_row(
        "round295c-canonical-r289-relation:",
        "ROUND295C_CANONICAL_R289_RELATION_V1",
        id_field,
        payload,
    )


def resign_inventory(row: dict[str, Any]) -> dict[str, Any]:
    id_field = "Round295C_all_stratum_scope_inventory_row_id"
    payload = {
        key: value for key, value in row.items()
        if key not in {id_field, "row_sha256"}
    }
    return close_row(
        "round295c-all-stratum-inventory:",
        "ROUND295C_ALL_STRATUM_SCOPE_INVENTORY_V1",
        id_field,
        payload,
    )


def validate_relation_attack(
    row: dict[str, Any], expected: dict[str, Any]
) -> None:
    validate_row(row, "attack relation")
    need(row == expected, "relation exact independent expectation")
    need(
        row["per_relation_child_lists_complete"] is True
        and row["per_relation_exact_ps_area_conserved"] is True
        and row["remaining_relation_scope_frontier_count"] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS)
        and all(
            child["canonical_Round294_registry_occurrence_id"]
            != child["source_field_formal_Round294_occurrence_id"]
            for child in row["physical_children"]
            if child["target_normalization_classification"]
            == "CONVERTED_FROM_ROUND294_SOURCE_ROW_ID"
        ),
        "relation semantic contract",
    )


def validate_inventory_attack(
    row: dict[str, Any], expected: dict[str, Any]
) -> None:
    validate_row(row, "attack inventory")
    need(row == expected, "inventory exact independent expectation")
    need(
        row["unresolved_scope_row_count"] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS),
        "inventory semantic contract",
    )


def validate_result_attack(
    value: dict[str, Any], expected: dict[str, Any]
) -> None:
    verify_self(value, "result_sha256", "attack result")
    need(value == expected, "result exact independent expectation")
    need(
        value["Round289_target_normalization"][
            "canonical_unique_Round294_target_count"
        ] == 3_780
        and value["all_stratum_scope_census"][
            "unresolved_all_stratum_scope_count"
        ] == 0
        and value["strict_nonpromotion"]["formal_seam_edge_credit"] == 0
        and value["strict_nonpromotion"][
            "post_Round295C_quotient_component_count"
        ] is None,
        "result semantic contract",
    )


def run_attacks(expected: dict[str, Any]) -> dict[str, Any]:
    labels: list[str] = []

    def reject(label: str, action: Callable[[], None]) -> None:
        try:
            action()
        except Exception:
            labels.append(label)
            return
        raise VerificationError(f"attack accepted:{label}")

    relations = expected["ledger"][
        "canonical_R289_relation_disposition_ledger"
    ]["rows"]
    relation_expected = next(
        row for row in relations
        if any(
            child["target_normalization_classification"]
            == "CONVERTED_FROM_ROUND294_SOURCE_ROW_ID"
            for child in row["physical_children"]
        )
    )
    converted_child_index = next(
        index
        for index, child in enumerate(relation_expected["physical_children"])
        if child["target_normalization_classification"]
        == "CONVERTED_FROM_ROUND294_SOURCE_ROW_ID"
    )

    def relation_mutation(
        label: str, mutate: Callable[[dict[str, Any]], None]
    ) -> None:
        def action() -> None:
            value = copy.deepcopy(relation_expected)
            mutate(value)
            validate_relation_attack(resign_relation(value), relation_expected)
        reject(label, action)

    relation_mutation(
        "copy_misnamed_source_as_occurrence",
        lambda row: row["physical_children"][
            converted_child_index
        ].__setitem__(
            "canonical_Round294_registry_occurrence_id",
            row["physical_children"][converted_child_index][
                "source_field_formal_Round294_occurrence_id"
            ],
        ),
    )
    relation_mutation(
        "forge_normalization_classification",
        lambda row: row["physical_children"][
            converted_child_index
        ].__setitem__(
            "target_normalization_classification",
            "ALREADY_CANONICAL_ROUND294_REGISTRY_OCCURRENCE_ID",
        ),
    )
    relation_mutation(
        "erase_physical_child",
        lambda row: row["physical_children"].pop(),
    )
    relation_mutation(
        "duplicate_physical_child",
        lambda row: row["physical_children"].append(
            copy.deepcopy(row["physical_children"][0])
        ),
    )
    relation_mutation(
        "forge_relation_area",
        lambda row: row.__setitem__("exact_relation_ps_area", "1"),
    )
    relation_mutation(
        "forge_relation_disposition",
        lambda row: row.__setitem__(
            "canonical_relation_disposition", "WHOLE_PHYSICAL"
        ),
    )
    relation_mutation(
        "restore_relation_frontier",
        lambda row: row.__setitem__(
            "remaining_relation_scope_frontier_count", 1
        ),
    )
    relation_mutation(
        "grant_relation_seam_credit",
        lambda row: row.__setitem__("formal_seam_edge_credit", 1),
    )
    relation_mutation(
        "grant_relation_component_credit",
        lambda row: row.__setitem__("formal_component_union_credit", 1),
    )
    relation_mutation(
        "grant_relation_DSU_credit",
        lambda row: row.__setitem__("formal_DSU_rank_reduction_credit", 1),
    )
    relation_mutation(
        "issue_relation_occurrence",
        lambda row: row.__setitem__("formal_new_occurrence_credit", 1),
    )
    relation_mutation(
        "inflate_physical_incidence_credit",
        lambda row: row.__setitem__(
            "formal_existing_occurrence_physical_incidence_binding_credit",
            row[
                "formal_existing_occurrence_physical_incidence_binding_credit"
            ] + 1,
        ),
    )

    inventory_rows = expected["ledger"][
        "all_stratum_scope_inventory_ledger"
    ]["rows"]

    def inventory_mutation(
        slot: int,
        label: str,
        mutate: Callable[[dict[str, Any]], None],
    ) -> None:
        source = next(row for row in inventory_rows if row["scope_slot"] == slot)

        def action() -> None:
            value = copy.deepcopy(source)
            mutate(value)
            validate_inventory_attack(resign_inventory(value), source)
        reject(label, action)

    inventory_mutation(
        1, "forge_registry_inventory_count",
        lambda row: row.__setitem__("row_count", 431_209),
    )
    inventory_mutation(
        2, "forge_representation_inventory_count",
        lambda row: row.__setitem__("row_count", 46_565),
    )
    inventory_mutation(
        3, "forge_R291_target_reference_count",
        lambda row: row.__setitem__("formal_target_reference_count", 225_305),
    )
    inventory_mutation(
        5, "restore_relation_inventory_unresolved",
        lambda row: row.__setitem__("unresolved_scope_row_count", 1),
    )
    inventory_mutation(
        6, "use_R296_5784_as_B_target_count",
        lambda row: row.__setitem__("canonical_unique_target_count", 5_784),
    )
    inventory_mutation(
        6, "forge_target_assignment_commitment",
        lambda row: row.__setitem__(
            "canonical_target_assignments_sha256", "0" * 64
        ),
    )
    inventory_mutation(
        2, "grant_inventory_alias_as_component",
        lambda row: row.__setitem__("formal_component_union_credit", 1),
    )

    result_expected = expected["result"]

    def result_mutation(
        label: str, mutate: Callable[[dict[str, Any]], None]
    ) -> None:
        def action() -> None:
            value = copy.deepcopy(result_expected)
            value.pop("result_sha256")
            mutate(value)
            value["result_sha256"] = digest(value)
            validate_result_attack(value, result_expected)
        reject(label, action)

    result_mutation(
        "result_target_count_5784",
        lambda row: row["Round289_target_normalization"].__setitem__(
            "canonical_unique_Round294_target_count", 5_784
        ),
    )
    result_mutation(
        "result_converted_count_forged",
        lambda row: row["Round289_target_normalization"].__setitem__(
            "converted_from_Round294_source_row_id_count", 5_291
        ),
    )
    result_mutation(
        "result_restore_scope_unresolved",
        lambda row: row["all_stratum_scope_census"].__setitem__(
            "unresolved_all_stratum_scope_count", 1
        ),
    )
    result_mutation(
        "result_registry_delta",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "formal_registry_delta", 1
        ),
    )
    result_mutation(
        "result_grant_seam_credit",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "formal_seam_edge_credit", 152
        ),
    )
    result_mutation(
        "result_rebuild_DSU",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "post_Round294_expanded_registry_component_DSU_status",
            "REBUILT",
        ),
    )
    result_mutation(
        "result_reuse_legacy_quotient",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "post_Round295C_quotient_component_count", 63_224
        ),
    )
    result_mutation(
        "result_claim_CM2",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "CM2", "CERTIFIED"
        ),
    )
    result_mutation(
        "result_reinterpret_endpoint_cells_as_edges",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "directed_endpoint_cells_are_seam_edges", True
        ),
    )
    result_mutation(
        "result_claim_R296_input_used",
        lambda row: row["provenance"].__setitem__(
            "Round296_input_used", True
        ),
    )

    reject(
        "duplicate_json_key",
        lambda: strict_decode(b'{"a":1,"a":2}', "duplicate"),
    )
    reject(
        "nonfinite_json",
        lambda: strict_decode(b'{"a":NaN}', "nonfinite"),
    )
    reject(
        "nul_json",
        lambda: strict_decode(b'{"a":1}\x00', "nul"),
    )
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        regular = root / "regular"
        regular.write_bytes(b"x")
        symlink = root / "symlink"
        symlink.symlink_to(regular)
        hardlink = root / "hardlink"
        hardlink.hardlink_to(regular)
        reject(
            "symlink_input",
            lambda: guard_path(symlink, allowed_parent=root),
        )
        reject(
            "hardlink_input",
            lambda: guard_path(hardlink, allowed_parent=root),
        )
        reject(
            "path_traversal_input",
            lambda: guard_path(HERE / ".." / HERE.name / B_RESULT),
        )
        malformed = root / "bad.gz"
        malformed.write_bytes(b"not gzip")

        def bad_gzip() -> None:
            with gzip.open(malformed, "rb") as stream:
                stream.read()
        reject("malformed_gzip", bad_gzip)

    return {
        "attack_count": len(labels),
        "rejected_count": len(labels),
        "resigned_semantic_attack_count": 29,
        "malformed_or_path_attack_count": 7,
        "attack_labels": labels,
        "all_attacks_rejected": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--attack-output", type=Path, default=DEFAULT_ATTACK_OUTPUT
    )
    parser.add_argument("--seed", default="295371")
    arguments = parser.parse_args()

    # This call completes before either candidate file is opened.
    expected = independently_reconstruct_expected()
    expected_completed_before_candidate_open = True

    ledger_raw = guard_path(CANDIDATE_LEDGER)
    result_raw = guard_path(CANDIDATE_RESULT)
    need(
        ledger_raw == expected["ledger_bytes"]
        and result_raw == expected["result_bytes"],
        "candidate exact deterministic bytes",
    )
    candidate_ledger = strict_decode(
        gzip.decompress(ledger_raw), CANDIDATE_LEDGER.name
    )
    candidate_result = strict_decode(result_raw, CANDIDATE_RESULT.name)
    need(
        candidate_ledger == expected["ledger"]
        and candidate_result == expected["result"],
        "candidate exact independently reconstructed objects",
    )
    validate_result_attack(candidate_result, expected["result"])
    attacks = run_attacks(expected)
    need(
        attacks["attack_count"] == attacks["rejected_count"] == 36
        and attacks["resigned_semantic_attack_count"] == 29
        and attacks["malformed_or_path_attack_count"] == 7,
        "complete attack census",
    )

    attack_suite = {
        "schema": ATTACK_SCHEMA,
        "status":
            "PASS_ROUND295C_36_OF_36_RECLOSED_SEMANTIC_MALFORMED_"
            "AND_PATH_ATTACKS_REJECTED",
        "candidate_basis": {
            "ledger_file_sha256": hashlib.sha256(ledger_raw).hexdigest(),
            "result_file_sha256": hashlib.sha256(result_raw).hexdigest(),
            "result_sha256": candidate_result["result_sha256"],
            "candidate_bytes_first_matched_independent_expectation": True,
        },
        "attacks": attacks,
        "seed_affects_output": False,
    }
    attack_suite["attack_suite_sha256"] = digest(attack_suite)
    attack_bytes = canonical(attack_suite)

    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND295C_ALL_STRATUM_SCOPE_"
            "COMPOSITION__9528_CANONICAL_RELATIONS__8_SCOPE_ROWS__"
            "5292_TARGETS_CONVERTED__6156_ALREADY_CANONICAL__"
            "3780_UNIQUE_TARGETS__UNRESOLVED_SCOPE_ZERO__"
            "NO_SEAM_COMPONENT_OR_DSU_PROMOTION",
        "seed_affects_output": False,
        "independence_contract": {
            "Round295C_producer_imported_or_executed": False,
            "Round295C_candidate_opened_before_expected_reconstruction":
                False,
            "expected_completed_before_candidate_open":
                expected_completed_before_candidate_open,
            "Round295A_or_Round295B_producer_imported_or_executed": False,
            "Round296_input_used": False,
            "complete_431208_registry_streamed_and_recommitted": True,
            "complete_46288_binding_table_streamed_and_recommitted": True,
            "all_input_and_candidate_rows_reclosed": True,
        },
        "normalization_audit": expected["normalization_audit"],
        "relation_audit": {
            "relation_count": 9_528,
            "physical_child_count": 11_448,
            "wrong_signed_child_count": 468,
            "graph_child_count": 288,
            "distinct_Round268_patch_ID_count": 24,
            "distinct_Round268_patch_side_pair_count": 40,
            "sealed_Round295B_directed_endpoint_cell_count": 152,
            "all_children_covered_exactly_once": True,
            "all_relations_exact_rational_area_conserved": True,
        },
        "scope_inventory_audit": {
            "inventory_row_count": 8,
            "inventory_table_row_counts":
                [431_208, 46_564, 113_452, 28_016,
                 9_528, 11_448, 468, 288],
            "physical_incidence_channel_total": 124_900,
            "no_binding_evidence_channel_total": 28_772,
            "unresolved_scope_count": 0,
            "channels_kept_distinct": True,
        },
        "candidate_file_audit": {
            "producer_file_sha256": file_sha256(PRODUCER),
            "ledger_file_sha256": hashlib.sha256(ledger_raw).hexdigest(),
            "result_file_sha256": hashlib.sha256(result_raw).hexdigest(),
            "result_sha256": candidate_result["result_sha256"],
            "both_candidate_files_exact_expected_bytes": True,
            "both_candidate_objects_exact_expected_values": True,
        },
        "targeted_reclosed_attacks": attacks,
        "attack_suite_audit": {
            "filename": DEFAULT_ATTACK_OUTPUT.name,
            "file_sha256": hashlib.sha256(attack_bytes).hexdigest(),
            "attack_suite_sha256": attack_suite["attack_suite_sha256"],
            "attack_count": 36,
            "rejected_count": 36,
        },
        "strict_nonpromotion": {
            "registry_delta": 0,
            "alias_delta_from_Round294": 276,
            "seam_edge_credit": 0,
            "component_union_credit": 0,
            "DSU_rank_reduction_credit": 0,
            "post_Round295C_quotient_component_count": None,
            "expanded_registry_DSU_status": "NOT_REBUILT",
            "directed_endpoint_cells_are_seam_edges": False,
            "all_152_true_seam_patch_edge_pairing":
                "DEFERRED_TO_ROUND296",
            "legacy_63224_used_as_current": False,
            "Gate5": "10/18",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    verification["verification_sha256"] = digest(verification)
    verification_bytes = canonical(verification)
    safe_write(arguments.attack_output, attack_bytes)
    safe_write(arguments.output, verification_bytes)
    print(json.dumps({
        "status": verification["status"],
        "seed": arguments.seed,
        "seed_affects_output": False,
        "verification_file_sha256":
            hashlib.sha256(verification_bytes).hexdigest(),
        "verification_sha256": verification["verification_sha256"],
        "attack_suite_file_sha256":
            hashlib.sha256(attack_bytes).hexdigest(),
        "attack_suite_sha256": attack_suite["attack_suite_sha256"],
        "attack_count": attacks["attack_count"],
        "normalization_audit": verification["normalization_audit"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
