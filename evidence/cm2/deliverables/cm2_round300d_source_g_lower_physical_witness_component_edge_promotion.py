#!/usr/bin/env python3
"""Round300-D: canonical two-target lower-physical-witness incidence edges.

This producer projects the complete sealed Round295-A physical-incidence
ledger into a canonical unordered-pair ledger:

* 111,852 two-target witness rows -> 111,524 canonical incidence edges;
* 1,600 one-target witness rows -> assignment-only exclusions.

The promoted object is deliberately narrow.  It is an incidence edge saying
that two distinct Round294 registry names occur in one or more sealed physical
lower-stratum witness rows.  It is not an occurrence-identity collapse, not a
topological occurrence-union claim, and is not eligible for component-DSU
application without a separately pinned included-stratum plus two-attachment
or corridor gluing lemma.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion"
)
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"

R266_MANIFEST = (
    "cm2_round266_source_g_expanded_curved_face_closure_manifest.sha256"
)
R266_CERTIFICATE = (
    "cm2_round266_source_g_expanded_curved_face_closure_certificate.json"
)
R266_VERIFICATION = (
    "cm2_round266_source_g_expanded_curved_face_closure_verification.json"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "manifest.sha256"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R294_RESULT = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_result.json"
)
R294_VERIFICATION = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "verification.json"
)
R295A_MANIFEST = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "manifest.sha256"
)
R295A_PRODUCER = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure.py"
)
R295A_INCIDENCE = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)
R295A_RESULT = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "result.json"
)
R295A_VERIFIER = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "verifier.py"
)
R295A_VERIFICATION = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "verification.json"
)
R299A_MANIFEST = (
    "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_"
    "manifest.sha256"
)
R299A_PRODUCER = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure.py"
)
R299A_LEDGER = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure_ledger.json.gz"
)
R299A_RESULT = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure_result.json"
)
R299A_VERIFIER = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure_verifier.py"
)
R299A_VERIFICATION = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure_verification.json"
)

MANIFEST_PINS = {
    R266_MANIFEST:
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    R295A_MANIFEST:
        "b25f11c0090c56d2ad2d3b2cd0b172e7c089f044ae5722eb9e82ae04b129094a",
    R299A_MANIFEST:
        "b1dfe718dd2b7477d9cc4067f1bade59d1589b3822eaf4b94b9dd721e61b468e",
}
INPUT_PINS = {
    R266_CERTIFICATE:
        "2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf",
    R266_VERIFICATION:
        "a6436c716cbbe74f0195e2d87f4084a28ca2a2e27b9fe5eeb98b6835df92b75b",
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R294_RESULT:
        "dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626",
    R294_VERIFICATION:
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    R295A_PRODUCER:
        "d147b6299a5e37b0e2ec104af64920e9b61f8a00491eb616b6a0e0eed66d6d08",
    R295A_INCIDENCE:
        "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
    R295A_RESULT:
        "0deb8b9c88595762df3844b988af777a6b5f55347acbb8b9e8784308c2d4381d",
    R295A_VERIFIER:
        "fabfb91c8aa1245716066594e5cf3c7e09fe43bdd199f662022eeda38eafb55a",
    R295A_VERIFICATION:
        "1b5c3423ea3854a8ae206677c740f31f5f9133edf66926271a10eec96b052349",
    R299A_PRODUCER:
        "a8e8d46c8ff13c2315868a982a3b394af7629cbb3cd76eda772b2c442a9f8f59",
    R299A_LEDGER:
        "ffea8120af2179990d5c9e7ff385193e2c5a08bed161cf5b570aa28b1f8b1ee0",
    R299A_RESULT:
        "4835bab4ebe7afc0da8d00395f83f881dd2aaf31e0697994fed54dc7d86302f5",
    R299A_VERIFIER:
        "8284650153f6dd933f493249f6af1c778fc1622639d465202ce752ea8935b215",
    R299A_VERIFICATION:
        "3a3ab65fdd6b5bd00062e1cebbd141e1c38bded7d920705a83a57ba24db0f27d",
}

R294_COMMITMENT = {
    "row_count": 431_208,
    "row_ids_sha256":
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
    "row_hashes_sha256":
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    "rows_sha256":
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    "occurrence_ids_sha256":
        "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936",
}
R295A_COMMITMENT = {
    "row_count": 113_452,
    "row_ids_sha256":
        "a0f471c84148d57eba4511efd8b343eb152c9378a24e018b9f0be10e41525805",
    "row_hashes_sha256":
        "7eab57334f6f5170ffaef60316250078cd6774cdabdb7279d3585267345e5258",
    "rows_sha256":
        "e8b00ffa431d7609d97e7e3cae00f656d2386643acc22d49bdc4a018ed295946",
}
R299A_COMMITMENT = {
    "row_count": 9_404,
    "row_ids_sha256":
        "a3786265b52feafd316cc81c71ab05ee32976b5ff7f1de091853d34a7b33e6e3",
    "row_hashes_sha256":
        "65e6f22b9085685b20a50dedfcb62cd08dd01e1ea70a61ee850d74450402b333",
    "rows_sha256":
        "6955fe1c36555c7aa492e4c5cfd1ab945fe16b824ea49bd3d72cea3bd3136c0f",
}
R266_OCCURRENCE_COMMITMENT = {
    "row_count": 126_468,
    "row_ids_sha256":
        "db01addd10a5112d56109695684d64994b927ce009e71b5e39dc95de2846acce",
    "row_hashes_sha256":
        "08fa74d62a0673cb02339bae0df05007e7f4cb9d452d69feef79a958ceaa5ad9",
    "rows_sha256":
        "441cde017675dc279a55d52f47c24c31721309ad1cb03e1ea831e6984569f351",
}
R266_ROOT_COMMITMENT = {
    "row_count": 63_224,
    "row_ids_sha256":
        "46889c11f7b1870bfe39faab0625054233c1c48b2cba2bd87cc9232b0405520a",
    "row_hashes_sha256":
        "a32bce700a94c39886a0d837e371e48562ae8380b71959e7326b0c4afef5e3b2",
    "rows_sha256":
        "bfdf5cde6fc68d39676e1543a6138672e7b8a68424280c6f895a8408f3eb579d",
}

SCHEMA = (
    "cm2.round300d.source-g-lower-physical-witness-"
    "component-edge-promotion.v1"
)
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
EDGE_ROW_ID = "Round300D_lower_physical_witness_incidence_edge_row_id"
EXCLUSION_ROW_ID = "Round300D_single_target_assignment_exclusion_row_id"
PRESERVED = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
R288 = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
REFINED = "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
PIN_RE = re.compile(r"^[0-9a-f]{64}$")
ZERO_FIELDS = (
    "formal_occurrence_identity_collapse_credit",
    "formal_official_key_merge_credit",
    "formal_component_edge_credit",
    "formal_component_union_credit",
    "formal_component_quotient_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_seam_edge_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)
WITNESS_KIND_FAMILY = {
    "ROUND182_GRAPH_SHEET_LEAF": "GRAPH",
    "ROUND179_NEGATIVE_T0_SHADOW_PATCH": "NEG_T0",
    "ROUND182_TRANSVERSE_1D_LINE": "TRANSVERSE",
    "ROUND179_POSITIVE_T0_RETAINED_OWNER": "POS_T0",
}


class PromotionError(RuntimeError):
    """Fail-closed producer error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PromotionError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def pieces(value: Any) -> Iterable[bytes]:
    for part in ENCODER.iterencode(value):
        yield part.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(pieces(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for part in pieces(value):
        state.update(part)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1 << 20), b""):
            state.update(part)
    return state.hexdigest()


def regular_bytes(path: Path, maximum: int = 3_000_000_000) -> bytes:
    need(path.parent.resolve() == HERE.resolve(), "path parent:" + path.name)
    need(path.exists() and not path.is_symlink(), "path exists:" + path.name)
    info = path.stat()
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "regular/link/size:" + path.name,
    )
    return path.read_bytes()


def strict_decode(raw: bytes, label: str) -> dict[str, Any]:
    need(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "strict bytes:" + label,
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate key:" + label + ":" + key)
            output[key] = value
        return output

    def reject(token: str) -> Any:
        raise PromotionError("noninteger JSON:" + label + ":" + token)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PromotionError("strict JSON:" + label) from error
    need(type(value) is dict, "top object:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    return strict_decode(regular_bytes(HERE / name), name)


def validate_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = dict(row)
    payload.pop("row_sha256", None)
    need(
        type(claimed) is str and digest(payload) == claimed,
        "row closure:" + label,
    )


def close_row(
    prefix: str,
    domain: str,
    id_field: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    row = {id_field: prefix + digest([domain, payload]), **payload}
    row["row_sha256"] = digest(row)
    return row


class ListHasher:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for part in pieces(value):
            self.state.update(part)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def rows_commitment(
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), "unique output IDs:" + id_field)
    return {
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "rows_sha256": digest(rows),
    }


def parse_manifest(name: str) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in regular_bytes(HERE / name, 200_000).decode().splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        sha256, filename = match.groups()
        need(
            Path(filename).name == filename and filename not in output,
            "manifest member:" + name,
        )
        output[filename] = sha256
    need(bool(output), "empty manifest:" + name)
    return output


def validate_input_boundary() -> None:
    for name, expected in MANIFEST_PINS.items():
        need(PIN_RE.fullmatch(expected) is not None, "manifest pin syntax")
        need(file_sha256(HERE / name) == expected, "manifest pin:" + name)
    for name, expected in INPUT_PINS.items():
        need(PIN_RE.fullmatch(expected) is not None, "input pin syntax")
        need(file_sha256(HERE / name) == expected, "input pin:" + name)
    selections = {
        R266_MANIFEST: [R266_CERTIFICATE, R266_VERIFICATION],
        R294_MANIFEST: [R294_REGISTRY, R294_RESULT, R294_VERIFICATION],
        R295A_MANIFEST: [
            R295A_PRODUCER, R295A_INCIDENCE, R295A_RESULT,
            R295A_VERIFIER, R295A_VERIFICATION,
        ],
        R299A_MANIFEST: [
            R299A_PRODUCER, R299A_LEDGER, R299A_RESULT,
            R299A_VERIFIER, R299A_VERIFICATION,
        ],
    }
    for manifest_name, members in selections.items():
        manifest = parse_manifest(manifest_name)
        for member in members:
            need(
                manifest.get(member) == INPUT_PINS[member],
                "manifest selection:" + manifest_name + ":" + member,
            )


def iter_array(
    stream: TextIO,
    marker: str = '"rows":[',
    initial: str = "",
) -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        part = stream.read(1 << 20)
        need(bool(part), "array marker:" + marker)
        buffer += part
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "stream duplicate key:" + key)
            output[key] = value
        return output

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(
            PromotionError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            PromotionError("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            part = stream.read(1 << 20)
            need(bool(part), "stream EOF")
            buffer = part
            continue
        if buffer.startswith(","):
            buffer = buffer[1:]
            continue
        if buffer.startswith("]"):
            return
        while True:
            try:
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                part = stream.read(1 << 20)
                need(bool(part), "truncated streamed row")
                buffer += part
        need(type(row) is dict, "stream row object")
        yield row
        buffer = buffer[end:]


def stream_gzip_rows(
    name: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
) -> None:
    rows_hash = ListHasher()
    ids_hash = ListHasher()
    hashes_hash = ListHasher()
    occurrence_ids_hash = (
        ListHasher() if "occurrence_ids_sha256" in expected else None
    )
    with gzip.open(
        HERE / name, "rt", encoding="utf-8", newline=""
    ) as stream:
        for row in iter_array(stream):
            validate_row(row, name)
            rows_hash.add(row)
            ids_hash.add(row[id_field])
            hashes_hash.add(row["row_sha256"])
            if occurrence_ids_hash is not None:
                occurrence_ids_hash.add(row["registry_occurrence_id"])
            visit(row)
    actual = {
        "row_count": rows_hash.count,
        "row_ids_sha256": ids_hash.finish(),
        "row_hashes_sha256": hashes_hash.finish(),
        "rows_sha256": rows_hash.finish(),
    }
    if occurrence_ids_hash is not None:
        actual["occurrence_ids_sha256"] = occurrence_ids_hash.finish()
    need(actual == expected, "gzip stream commitment:" + name)


def stream_named_plain_rows(
    name: str,
    table_name: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
) -> None:
    table_marker = '"' + table_name + '":'
    carry = ""
    with (HERE / name).open("rt", encoding="utf-8", newline="") as stream:
        while True:
            part = stream.read(1 << 20)
            need(bool(part), "plain table marker:" + table_name)
            joined = carry + part
            if table_marker in joined:
                initial = joined.split(table_marker, 1)[1]
                break
            carry = joined[-len(table_marker):]
        rows_hash = ListHasher()
        ids_hash = ListHasher()
        hashes_hash = ListHasher()
        for row in iter_array(stream, initial=initial):
            validate_row(row, "R266:" + table_name)
            rows_hash.add(row)
            ids_hash.add(row[id_field])
            hashes_hash.add(row["row_sha256"])
            visit(row)
    actual = {
        "row_count": rows_hash.count,
        "row_ids_sha256": ids_hash.finish(),
        "row_hashes_sha256": hashes_hash.finish(),
        "rows_sha256": rows_hash.finish(),
    }
    need(actual == expected, "plain stream commitment:" + table_name)


def validate_result_self(document: dict[str, Any], label: str) -> None:
    claimed = document.get("result_sha256")
    payload = dict(document)
    payload.pop("result_sha256", None)
    need(
        type(claimed) is str and digest(payload) == claimed,
        "result self closure:" + label,
    )


def first_pass_r295a() -> tuple[set[str], dict[str, Any]]:
    result = read_json(R295A_RESULT)
    validate_result_self(result, "Round295A")
    need(
        result["physical_witness_incidence_binding_ledger"]["file_sha256"]
        == INPUT_PINS[R295A_INCIDENCE],
        "Round295A result attachment",
    )
    verification = read_json(R295A_VERIFICATION)
    need(
        verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295A"
        ),
        "Round295A independent seal",
    )
    targets: set[str] = set()
    one_target_occurrences: set[str] = set()
    two_target_occurrences: set[str] = set()
    arities: Counter[int] = Counter()
    witness_kinds: Counter[str] = Counter()
    support_kinds: Counter[str] = Counter()
    row_ids: set[str] = set()

    def visit(row: dict[str, Any]) -> None:
        row_id = row["Round295A_R291_physical_incidence_binding_row_id"]
        need(row_id not in row_ids, "Round295A unique row ID")
        row_ids.add(row_id)
        count = row["target_Round294_registry_reference_count"]
        ids = row["target_Round294_registry_occurrence_ids"]
        need(
            count in {1, 2}
            and len(ids) == count
            and len(ids) == len(set(ids)),
            "Round295A target arity",
        )
        arities[count] += 1
        targets.update(ids)
        (one_target_occurrences if count == 1 else two_target_occurrences).update(
            ids
        )
        witness_kinds[row["witness_kind"]] += 1
        support_kinds[row["canonical_support_kind"]] += 1
        need(
            row["exact_witness_covered_by_named_registry_supports"] is True
            and row["formal_physical_witness_incidence_binding_credit"] == 1
            and row["formal_target_reference_credit"] == count
            and all(row.get(field, 0) == 0 for field in (
                "formal_new_expanded_occurrence_credit",
                "formal_occurrence_alias_credit",
                "formal_component_union_credit",
                "formal_DSU_rank_reduction_credit",
                "formal_seam_edge_credit",
                "formal_Jx_Jy_same_point_glue_credit",
                "formal_maximality_credit",
                "formal_fibre_credit",
                "formal_global_disposition_credit",
            )),
            "Round295A physical binding scope",
        )

    stream_gzip_rows(
        R295A_INCIDENCE,
        "Round295A_R291_physical_incidence_binding_row_id",
        R295A_COMMITMENT,
        visit,
    )
    need(
        arities == {1: 1_600, 2: 111_852}
        and len(targets) == 224_168,
        "Round295A complete target census",
    )
    need(
        len(one_target_occurrences) == 1_216
        and len(two_target_occurrences) == 223_048
        and len(one_target_occurrences & two_target_occurrences) == 96
        and len(one_target_occurrences - two_target_occurrences) == 1_120,
        "Round295A target-set overlap census",
    )
    return targets, {
        "reference_count_histogram": {
            str(key): value for key, value in sorted(arities.items())
        },
        "complete_witness_kind_histogram": dict(sorted(witness_kinds.items())),
        "complete_support_kind_histogram": dict(sorted(support_kinds.items())),
        "single_target_distinct_occurrence_count":
            len(one_target_occurrences),
        "two_target_distinct_occurrence_count":
            len(two_target_occurrences),
        "single_and_two_target_overlap_occurrence_count":
            len(one_target_occurrences & two_target_occurrences),
        "single_target_only_distinct_occurrence_count":
            len(one_target_occurrences - two_target_occurrences),
    }


def reconstruct_registry_and_keys(
    targets: set[str],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    set[str],
    dict[str, int],
]:
    result = read_json(R294_RESULT)
    validate_result_self(result, "Round294")
    need(
        result["registry_ledger"]["file_sha256"] == INPUT_PINS[R294_REGISTRY],
        "Round294 registry attachment",
    )
    verification = read_json(R294_VERIFICATION)
    need(
        verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "Round294 independent seal",
    )
    selected: dict[str, dict[str, Any]] = {}
    refined_rows: dict[str, dict[str, Any]] = {}
    occurrences: set[str] = set()
    registry_kinds: Counter[str] = Counter()
    old_keys: set[str] = set()

    def visit(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        need(occurrence not in occurrences, "Round294 unique occurrence")
        occurrences.add(occurrence)
        kind = row["registry_entry_kind"]
        registry_kinds[kind] += 1
        if kind == REFINED:
            need(
                row["official_key_id"] is None
                and row["official_key_ordinal"] is None,
                "Round294 refined key-null frontier",
            )
            refined_rows[occurrence] = {
                "row_id": row["Round294_occurrence_registry_row_id"],
                "row_sha256": row["row_sha256"],
            }
        else:
            need(
                type(row["official_key_id"]) is str
                and type(row["official_key_ordinal"]) is int,
                "Round294 nonrefined official key",
            )
            old_keys.add(row["official_key_id"])
        if occurrence in targets:
            selected[occurrence] = {
                "registry_occurrence_id": occurrence,
                "Round294_occurrence_registry_row_id":
                    row["Round294_occurrence_registry_row_id"],
                "Round294_occurrence_registry_row_sha256":
                    row["row_sha256"],
                "registry_entry_kind": kind,
                "source_occurrence_class": row["source_occurrence_class"],
                "physical_support_chart": row["physical_support_chart"],
                "official_key_id": row["official_key_id"],
                "official_key_ordinal": row["official_key_ordinal"],
                "complete_10_field_return_signature_sha256":
                    row["complete_10_field_return_signature_sha256"],
                "source_row_id": row["source_row_id"],
                "source_row_sha256": row["source_row_sha256"],
            }

    stream_gzip_rows(
        R294_REGISTRY,
        "Round294_occurrence_registry_row_id",
        R294_COMMITMENT,
        visit,
    )
    need(
        registry_kinds == {
            PRESERVED: 126_468,
            R288: 295_336,
            REFINED: 9_404,
        }
        and set(selected) == targets
        and len(old_keys) == 116,
        "Round294 complete registry/target census",
    )

    result299 = read_json(R299A_RESULT)
    validate_result_self(result299, "Round299A")
    need(
        result299["ledger"]["file_sha256"] == INPUT_PINS[R299A_LEDGER]
        and result299["raw_observed_key_universe"][
            "after_refined_binding_count"
        ] == 124,
        "Round299A result contract",
    )
    verification299 = read_json(R299A_VERIFICATION)
    need(
        verification299["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND299A"
        ),
        "Round299A independent seal",
    )
    refined_key_map: dict[str, dict[str, Any]] = {}
    final_keys = set(old_keys)

    def visit299(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        need(
            occurrence in refined_rows
            and occurrence not in refined_key_map
            and row["source_Round294_occurrence_registry_row_id"]
            == refined_rows[occurrence]["row_id"]
            and row["source_Round294_occurrence_registry_row_sha256"]
            == refined_rows[occurrence]["row_sha256"]
            and row["append_only_official_key_binding"] is True
            and row["occurrence_identity_preserved"] is True
            and row["formal_refined_occurrence_official_key_binding_credit"]
            == 1
            and row["raw_key_merge_credit"] == 0,
            "Round299A exact refined binding",
        )
        refined_key_map[occurrence] = {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
            "Round299A_binding_row_id":
                row[
                    "Round299A_refined_occurrence_official_key_binding_row_id"
                ],
            "Round299A_binding_row_sha256": row["row_sha256"],
        }
        final_keys.add(row["official_key_id"])

    stream_gzip_rows(
        R299A_LEDGER,
        "Round299A_refined_occurrence_official_key_binding_row_id",
        R299A_COMMITMENT,
        visit299,
    )
    need(
        set(refined_key_map) == set(refined_rows)
        and len(final_keys) == 124
        and not (targets & set(refined_key_map)),
        "Round299A complete 124-key extension and target exclusion",
    )
    return selected, refined_key_map, final_keys, {
        key: registry_kinds[key] for key in sorted(registry_kinds)
    }


def reconstruct_r266_provenance(
    selected: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    preserved_targets = {
        occurrence
        for occurrence, row in selected.items()
        if row["registry_entry_kind"] == PRESERVED
    }
    need(len(preserved_targets) == 1_396, "preserved target endpoint census")
    occurrence_rows: dict[str, dict[str, Any]] = {}

    def visit_occurrence(row: dict[str, Any]) -> None:
        occurrence = row["local_occurrence_row_id"]
        if occurrence in preserved_targets:
            need(
                occurrence not in occurrence_rows,
                "R266 selected occurrence uniqueness",
            )
            occurrence_rows[occurrence] = row

    stream_named_plain_rows(
        R266_CERTIFICATE,
        "formal_post_Round266_expanded_occurrence_frontier_ledger",
        "post_Round266_expanded_occurrence_frontier_row_id",
        R266_OCCURRENCE_COMMITMENT,
        visit_occurrence,
    )
    need(
        set(occurrence_rows) == preserved_targets,
        "R266 selected occurrence coverage",
    )
    needed_roots = {
        row["post_Round266_quotient_component_id"]
        for row in occurrence_rows.values()
    }
    root_rows: dict[str, dict[str, Any]] = {}

    def visit_root(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        if root in needed_roots:
            need(root not in root_rows, "R266 selected root uniqueness")
            root_rows[root] = row

    stream_named_plain_rows(
        R266_CERTIFICATE,
        "formal_post_Round266_component_frontier_ledger",
        "post_Round266_component_frontier_row_id",
        R266_ROOT_COMMITMENT,
        visit_root,
    )
    need(set(root_rows) == needed_roots, "R266 selected root coverage")

    output: dict[str, dict[str, Any]] = {}
    for occurrence, row in occurrence_rows.items():
        registry = selected[occurrence]
        root = root_rows[row["post_Round266_quotient_component_id"]]
        need(
            registry["source_row_id"]
            == row["post_Round266_expanded_occurrence_frontier_row_id"]
            and registry["source_row_sha256"] == row["row_sha256"]
            and registry["official_key_id"] == row["official_key_id"]
            == root["official_key_id"]
            and registry["official_key_ordinal"]
            == row["official_key_ordinal"]
            == root["official_key_ordinal"],
            "R266/R294 occurrence-root-key join",
        )
        output[occurrence] = {
            "Round266_expanded_occurrence_frontier_row_id":
                row["post_Round266_expanded_occurrence_frontier_row_id"],
            "Round266_expanded_occurrence_frontier_row_sha256":
                row["row_sha256"],
            "Round266_quotient_component_id":
                row["post_Round266_quotient_component_id"],
            "Round266_component_frontier_row_id":
                root["post_Round266_component_frontier_row_id"],
            "Round266_component_frontier_row_sha256": root["row_sha256"],
        }
    return output


def endpoint_payload(
    occurrence: str,
    selected: dict[str, dict[str, Any]],
    r266: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    registry = selected[occurrence]
    preserved = registry["registry_entry_kind"] == PRESERVED
    return {
        "registry_occurrence_id": occurrence,
        "Round294_occurrence_registry_row_id":
            registry["Round294_occurrence_registry_row_id"],
        "Round294_occurrence_registry_row_sha256":
            registry["Round294_occurrence_registry_row_sha256"],
        "registry_entry_kind": registry["registry_entry_kind"],
        "source_occurrence_class": registry["source_occurrence_class"],
        "physical_support_chart": registry["physical_support_chart"],
        "final_Round299A_official_key_id": registry["official_key_id"],
        "final_Round299A_official_key_ordinal":
            registry["official_key_ordinal"],
        "complete_10_field_return_signature_sha256":
            registry["complete_10_field_return_signature_sha256"],
        "preserved_Round266_provenance": (
            r266[occurrence] if preserved else None
        ),
    }


def reconstruct_rows(
    selected: dict[str, dict[str, Any]],
    r266: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    exclusions: list[dict[str, Any]] = []
    raw_kind: Counter[str] = Counter()
    raw_support: Counter[str] = Counter()
    raw_tranche: Counter[str] = Counter()
    assignment_kinds: Counter[str] = Counter()

    with gzip.open(
        HERE / R295A_INCIDENCE, "rt", encoding="utf-8", newline=""
    ) as stream:
        for source in iter_array(stream):
            validate_row(source, "Round295A second pass")
            ids = source["target_Round294_registry_occurrence_ids"]
            count = source["target_Round294_registry_reference_count"]
            embedded = source["target_Round294_registry_rows"]
            need(
                len(ids) == len(embedded) == count,
                "Round295A embedded target arity",
            )
            for occurrence, target in zip(ids, embedded, strict=True):
                expected = selected[occurrence]
                need(
                    target["registry_occurrence_id"] == occurrence
                    and target["Round294_occurrence_registry_row_id"]
                    == expected["Round294_occurrence_registry_row_id"]
                    and target["Round294_occurrence_registry_row_sha256"]
                    == expected["Round294_occurrence_registry_row_sha256"]
                    and target["registry_entry_kind"]
                    == expected["registry_entry_kind"]
                    and target["source_occurrence_class"]
                    == expected["source_occurrence_class"]
                    and target["physical_support_chart"]
                    == expected["physical_support_chart"]
                    and target["official_key_id"]
                    == expected["official_key_id"]
                    and target["official_key_ordinal"]
                    == expected["official_key_ordinal"]
                    and target[
                        "complete_10_field_return_signature_sha256"
                    ]
                    == expected[
                        "complete_10_field_return_signature_sha256"
                    ],
                    "Round295A embedded Round294 target join",
                )
            summary = {
                "source_Round295A_physical_incidence_binding_row_id":
                    source[
                        "Round295A_R291_physical_incidence_binding_row_id"
                    ],
                "source_Round295A_physical_incidence_binding_row_sha256":
                    source["row_sha256"],
                "Round291_local_disposition_row_id":
                    source["Round291_local_disposition_row_id"],
                "physical_witness_cell_index":
                    source["physical_witness_cell_index"],
                "source_chart": source["source_chart"],
                "canonical_support_kind":
                    source["canonical_support_kind"],
                "local_disposition": source["local_disposition"],
                "witness_kind": source["witness_kind"],
                "Round295A_binding_classification":
                    source["Round295A_binding_classification"],
            }
            if count == 1:
                occurrence = ids[0]
                assignment_kinds[source["witness_kind"]] += 1
                payload = {
                    **summary,
                    "target_Round294_registry_occurrence":
                        endpoint_payload(occurrence, selected, r266),
                    "target_registry_reference_count": 1,
                    "assignment_only_reason":
                        "ONE_TARGET_PHYSICAL_INCIDENCE_ASSIGNMENT__"
                        "CANNOT_FORM_UNORDERED_OCCURRENCE_PAIR",
                    "canonical_two_target_incidence_edge_issued": False,
                    "formal_canonical_two_target_lower_physical_witness_"
                    "incidence_edge_credit": 0,
                    **{field: 0 for field in ZERO_FIELDS},
                }
                exclusions.append(close_row(
                    "round300d-single-target-assignment-exclusion:",
                    "ROUND300D_SINGLE_TARGET_ASSIGNMENT_EXCLUSION_V1",
                    EXCLUSION_ROW_ID,
                    payload,
                ))
                continue

            pair = tuple(sorted(ids))
            need(pair[0] != pair[1], "Round295A two-target self pair")
            groups[pair].append(summary)
            raw_kind[WITNESS_KIND_FAMILY[source["witness_kind"]]] += 1
            raw_support[source["canonical_support_kind"]] += 1
            tranche = "|".join(sorted(
                selected[occurrence]["registry_entry_kind"]
                for occurrence in pair
            ))
            raw_tranche[tranche] += 1

    need(
        len(exclusions) == 1_600
        and sum(map(len, groups.values())) == 111_852
        and len(groups) == 111_524,
        "Round295A second-pass partition",
    )
    need(
        raw_kind == {
            "GRAPH": 111_524,
            "NEG_T0": 128,
            "TRANSVERSE": 112,
            "POS_T0": 88,
        }
        and raw_support == {
            "NOMINAL_REGULAR_ZERO_SET_IF_PRESENT": 86_308,
            "NOMINAL_REGULAR_FACTOR_UNION_IF_PRESENT": 25_432,
            "NOMINAL_PAIR_CANDIDATE_IF_TRANSVERSE": 112,
        }
        and raw_tranche == {
            R288 + "|" + R288: 111_660,
            PRESERVED + "|" + PRESERVED: 192,
        },
        "two-target kind/support/tranche census",
    )
    need(
        assignment_kinds == {
            "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 416,
            "ROUND179_POSITIVE_T0_RETAINED_OWNER": 352,
            "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
            "SOURCE_EXACT_T0_SHEET_CELL": 224,
        },
        "single-target assignment kind census",
    )

    edge_rows: list[dict[str, Any]] = []
    multiplicity: Counter[int] = Counter()
    key_relation: Counter[str] = Counter()
    unique_tranche: Counter[str] = Counter()
    cross_key_detail: Counter[str] = Counter()
    cross_key_raw: Counter[str] = Counter()
    for pair in sorted(groups):
        witnesses = sorted(
            groups[pair],
            key=lambda row: row[
                "source_Round295A_physical_incidence_binding_row_id"
            ],
        )
        multiplicity[len(witnesses)] += 1
        endpoints = [
            endpoint_payload(occurrence, selected, r266)
            for occurrence in pair
        ]
        keys = [
            endpoint["final_Round299A_official_key_id"]
            for endpoint in endpoints
        ]
        relation = "SAME_OFFICIAL_KEY" if keys[0] == keys[1] else (
            "CROSS_OFFICIAL_KEY"
        )
        key_relation[relation] += 1
        tranche = "|".join(sorted(
            endpoint["registry_entry_kind"] for endpoint in endpoints
        ))
        unique_tranche[tranche] += 1
        witness_kind_histogram = Counter(
            row["witness_kind"] for row in witnesses
        )
        support_kind_histogram = Counter(
            row["canonical_support_kind"] for row in witnesses
        )
        if relation == "CROSS_OFFICIAL_KEY":
            for kind, count in witness_kind_histogram.items():
                cross_key_raw[WITNESS_KIND_FAMILY[kind]] += count
            cross_key_detail[
                WITNESS_KIND_FAMILY[witnesses[0]["witness_kind"]]
            ] += 1
        payload = {
            "canonical_unordered_Round294_registry_occurrence_ids":
                list(pair),
            "left_endpoint": endpoints[0],
            "right_endpoint": endpoints[1],
            "self_pair": False,
            "source_Round295A_physical_incidence_binding_row_ids": [
                row[
                    "source_Round295A_physical_incidence_binding_row_id"
                ]
                for row in witnesses
            ],
            "source_Round295A_physical_incidence_binding_row_sha256s": [
                row[
                    "source_Round295A_physical_incidence_binding_row_sha256"
                ]
                for row in witnesses
            ],
            "source_Round291_local_disposition_row_ids": sorted({
                row["Round291_local_disposition_row_id"]
                for row in witnesses
            }),
            "physical_witness_cell_indices": sorted({
                row["physical_witness_cell_index"] for row in witnesses
            }),
            "source_charts": sorted({
                row["source_chart"] for row in witnesses
            }),
            "witness_multiplicity": len(witnesses),
            "witness_kind_histogram":
                dict(sorted(witness_kind_histogram.items())),
            "canonical_support_kind_histogram":
                dict(sorted(support_kind_histogram.items())),
            "Round295A_binding_classifications": sorted({
                row["Round295A_binding_classification"]
                for row in witnesses
            }),
            "endpoint_tranche_relation": tranche,
            "official_key_relation": relation,
            "component_connectivity_may_cross_official_key": True,
            "official_key_metadata_is_not_component_purity_constraint":
                True,
            "same_official_key_is_not_an_identity_or_connectivity_shortcut":
                True,
            "all_source_witnesses_exactly_covered_by_named_registry_supports":
                True,
            "incidence_edge_semantics":
                "CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE",
            "shared_lower_witness_incidence_proved": True,
            "topological_occurrence_union_connectivity_claimed": False,
            "included_stratum_gluing_lemma_pinned": False,
            "two_sided_attachment_or_corridor_gluing_lemma_pinned": False,
            "eligible_for_component_DSU_application": False,
            "formal_canonical_two_target_lower_physical_witness_"
            "incidence_edge_credit": 1,
            **{field: 0 for field in ZERO_FIELDS},
        }
        edge_rows.append(close_row(
            "round300d-lower-physical-witness-incidence-edge:",
            "ROUND300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_"
            "WITNESS_INCIDENCE_EDGE_V1",
            EDGE_ROW_ID,
            payload,
        ))
    edge_rows.sort(key=lambda row: row[EDGE_ROW_ID])
    exclusions.sort(key=lambda row: row[EXCLUSION_ROW_ID])
    need(
        multiplicity == {1: 111_380, 2: 56, 3: 32, 4: 16, 5: 40}
        and key_relation == {
            "SAME_OFFICIAL_KEY": 86_308,
            "CROSS_OFFICIAL_KEY": 25_216,
        }
        and unique_tranche == {
            R288 + "|" + R288: 111_332,
            PRESERVED + "|" + PRESERVED: 192,
        }
        and cross_key_detail == {
            "GRAPH": 25_119,
            "NEG_T0": 27,
            "POS_T0": 29,
            "TRANSVERSE": 41,
        },
        "canonical edge multiplicity/key/tranche census",
    )
    need(
        cross_key_raw == {
            "GRAPH": 25_216,
            "NEG_T0": 128,
            "POS_T0": 88,
            "TRANSVERSE": 112,
        },
        "cross-key raw witness census",
    )
    return edge_rows, exclusions, {
        "two_target_raw_witness_kind_family_histogram":
            dict(sorted(raw_kind.items())),
        "two_target_raw_support_kind_histogram":
            dict(sorted(raw_support.items())),
        "two_target_raw_endpoint_tranche_histogram":
            dict(sorted(raw_tranche.items())),
        "canonical_edge_witness_multiplicity_histogram": {
            str(key): value for key, value in sorted(multiplicity.items())
        },
        "canonical_edge_official_key_relation_histogram":
            dict(sorted(key_relation.items())),
        "canonical_edge_endpoint_tranche_histogram":
            dict(sorted(unique_tranche.items())),
        "cross_key_canonical_primary_witness_kind_family_histogram":
            dict(sorted(cross_key_detail.items())),
        "cross_key_raw_witness_kind_family_histogram":
            dict(sorted(cross_key_raw.items())),
        "single_target_assignment_witness_kind_histogram":
            dict(sorted(assignment_kinds.items())),
    }


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=buffer,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        for part in pieces(value):
            stream.write(part)
    return buffer.getvalue()


def atomic_write(path: Path, raw: bytes) -> None:
    need(
        path.parent.resolve() == HERE.resolve()
        and path.name.startswith(PREFIX + "_"),
        "output HERE/prefix confinement:" + str(path),
    )
    need(not path.is_symlink(), "output symlink:" + str(path))
    parent = path.parent.resolve()
    need(parent.is_dir(), "output parent:" + str(path))
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=parent,
        prefix="." + path.name + ".",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
    temporary.replace(path)


def build(
    producer_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_input_boundary()
    targets, r295_complete = first_pass_r295a()
    selected, refined_keys, final_keys, registry_kinds = (
        reconstruct_registry_and_keys(targets)
    )
    r266 = reconstruct_r266_provenance(selected)
    edge_rows, exclusion_rows, edge_census = reconstruct_rows(selected, r266)
    need(
        len(refined_keys) == 9_404
        and len(final_keys) == 124
        and all(
            row["official_key_id"] is not None for row in selected.values()
        ),
        "final key completeness",
    )
    edge_commitment = rows_commitment(edge_rows, EDGE_ROW_ID)
    exclusion_commitment = rows_commitment(
        exclusion_rows, EXCLUSION_ROW_ID
    )
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status":
            "FORMALLY_PROMOTED_111524_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_"
            "WITNESS_INCIDENCE_EDGES__1600_SINGLE_TARGET_ASSIGNMENT_"
            "EXCLUSIONS__NOT_COMPONENT_DSU_ELIGIBLE",
        "canonical_incidence_edge_row_count": len(edge_rows),
        "canonical_incidence_edge_row_ids_sha256":
            edge_commitment["row_ids_sha256"],
        "canonical_incidence_edge_row_hashes_sha256":
            edge_commitment["row_hashes_sha256"],
        "canonical_incidence_edge_rows_sha256":
            edge_commitment["rows_sha256"],
        "canonical_incidence_edge_rows": edge_rows,
        "single_target_assignment_exclusion_row_count":
            len(exclusion_rows),
        "single_target_assignment_exclusion_row_ids_sha256":
            exclusion_commitment["row_ids_sha256"],
        "single_target_assignment_exclusion_row_hashes_sha256":
            exclusion_commitment["row_hashes_sha256"],
        "single_target_assignment_exclusion_rows_sha256":
            exclusion_commitment["rows_sha256"],
        "single_target_assignment_exclusion_rows": exclusion_rows,
    }
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_"
            "INCIDENCE_EDGE_PROMOTION__111524_EDGES__1600_ASSIGNMENT_"
            "EXCLUSIONS__ZERO_COMPONENT_DSU_CREDIT",
        "producer_sha256": producer_sha256,
        "seed_affects_output": False,
        "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "source_reconstruction": {
            "Round266_preserved_target_occurrence_count": len(r266),
            "Round266_component_root_rows_reopened":
                len({
                    row["Round266_quotient_component_id"]
                    for row in r266.values()
                }),
            "Round294_registry_kind_histogram": registry_kinds,
            "Round294_target_occurrence_count": len(selected),
            "Round299A_final_raw_official_key_count": len(final_keys),
            "Round299A_refined_binding_count": len(refined_keys),
            "target_occurrence_unkeyed_count": sum(
                row["official_key_id"] is None for row in selected.values()
            ),
            **r295_complete,
        },
        "promotion_census": {
            "Round295A_complete_physical_incidence_row_count": 113_452,
            "single_target_assignment_exclusion_count": 1_600,
            "two_target_raw_physical_witness_row_count": 111_852,
            "canonical_unordered_incidence_edge_count": 111_524,
            "duplicate_two_target_witness_row_count": 328,
            "self_pair_count": 0,
            **edge_census,
        },
        "semantic_scope": {
            "promoted_relation":
                "CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE",
            "incidence_edge_is_occurrence_identity_collapse": False,
            "incidence_edge_is_topological_occurrence_union_claim": False,
            "eligible_for_component_DSU_application": False,
            "required_before_component_DSU_application":
                "PINNED_INCLUDED_STRATUM_PLUS_TWO_ATTACHMENT_OR_"
                "POSITIVE_VOLUME_CORRIDOR_GLUING_LEMMA",
            "component_connectivity_may_cross_official_key": True,
            "official_key_is_component_purity_constraint": False,
            "same_key_is_automatic_connectivity": False,
            "cross_key_is_automatic_exclusion": False,
            "cross_key_edge_count_preserved": 25_216,
            "same_key_edge_count_preserved": 86_308,
            "single_target_assignment_is_edge": False,
        },
        "formal_credit_transition": {
            "formal_canonical_two_target_lower_physical_witness_"
            "incidence_edge_credit": 111_524,
            "source_Round295A_physical_witness_binding_credit_reissued": 0,
            **{field: 0 for field in ZERO_FIELDS},
        },
        "strict_nonpromotion": {
            "formal_official_key_merge_count": 0,
            "formal_component_edge_count": 0,
            "formal_component_union_count": 0,
            "formal_component_quotient_credit": 0,
            "formal_DSU_rank_reduction_count": 0,
            "post_Round300D_quotient_component_count": None,
            "maximality_status": "NOT_REBUILT",
            "fibre_status": "NOT_REBUILT",
            "global_disposition_status": "NOT_REBUILT",
            "historical_29984_rank_reduction_number_status":
                "DIAGNOSTIC_HYPOTHESIS_ONLY__NOT_RECOMPUTED__"
                "NOT_FORMAL_CREDIT",
        },
        "required_next": [
            "Prove an included lower stratum and two endpoint attachments or "
            "strict positive-volume corridors for each incidence-edge class.",
            "Only a later gate may decide DSU eligibility, rank reduction, "
            "quotient count, maximality, fibres, or dispositions.",
            "Never merge occurrence identities or official key identities "
            "from this incidence-edge ledger.",
        ],
        "ledger": {
            "filename": LEDGER.name,
            "schema": LEDGER_SCHEMA,
            "canonical_incidence_edge_row_count": len(edge_rows),
            "canonical_incidence_edge_rows_sha256":
                edge_commitment["rows_sha256"],
            "single_target_assignment_exclusion_row_count":
                len(exclusion_rows),
            "single_target_assignment_exclusion_rows_sha256":
                exclusion_commitment["rows_sha256"],
            "file_sha256": "",
        },
        "result_sha256": "",
    }
    return ledger, result


def finalize_result(
    result: dict[str, Any],
    ledger_file_sha256: str,
) -> dict[str, Any]:
    output = json.loads(canonical(result))
    output["ledger"]["file_sha256"] = ledger_file_sha256
    output["result_sha256"] = ""
    payload = dict(output)
    payload.pop("result_sha256")
    output["result_sha256"] = digest(payload)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="300401")
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--result", type=Path, default=RESULT)
    args = parser.parse_args()
    need(bool(args.seed), "nonempty seed bookkeeping")
    need(args.ledger != args.result, "distinct ledger/result output paths")
    producer_sha256 = file_sha256(Path(__file__).resolve())
    ledger, result = build(producer_sha256)
    ledger_bytes = deterministic_gzip(ledger)
    result = finalize_result(result, hashlib.sha256(ledger_bytes).hexdigest())
    result_bytes = canonical(result) + b"\n"
    atomic_write(args.ledger, ledger_bytes)
    atomic_write(args.result, result_bytes)
    print(result["status"])
    print(json.dumps(result["promotion_census"], sort_keys=True))
    print("producer_sha256=" + producer_sha256)
    print("ledger_file_sha256=" + hashlib.sha256(ledger_bytes).hexdigest())
    print("result_file_sha256=" + hashlib.sha256(result_bytes).hexdigest())
    print("result_sha256=" + result["result_sha256"])


if __name__ == "__main__":
    main()
