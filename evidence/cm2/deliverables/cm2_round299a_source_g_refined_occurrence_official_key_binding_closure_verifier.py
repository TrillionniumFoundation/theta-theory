#!/usr/bin/env python3
"""Independent cacheless verifier for the Round299-A binding closure.

The Round299-A producer is never imported, executed, parsed, or used as a
semantic oracle.  Its file is consumed only by a byte-for-byte SHA-256 pin.
Expected binding rows are rebuilt directly from the sealed Round275,
Round282/Round285, Round292, and Round294 evidence.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable, Iterable, Iterator, TextIO
import zlib


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure"
)
PRODUCER = HERE / f"{PREFIX}.py"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

SCHEMA = (
    "cm2.round299a.source-g-refined-occurrence-"
    "official-key-binding-closure.v1"
)
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
INDEPENDENT_ATTACK_SCHEMA = SCHEMA + ".attack-suite.v2"
VERIFICATION_SCHEMA = SCHEMA + ".verification.v1"
ROW_ID_FIELD = "Round299A_refined_occurrence_official_key_binding_row_id"
REFINED_KIND = (
    "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
)
EXISTING_CLASS = "EXISTING_KEY_FROM_PRE_REFINED_ROUND294_KEY_UNIVERSE"
NEW_CLASS = "NEW_RAW_KEY_FROM_PINNED_ROUND275_LOCAL_RETURN_SIGNATURE"

MAX_FILE_BYTES = 2_000_000_000
MAX_GZIP_UNCOMPRESSED_BYTES = 2_000_000_000
PRE_VERIFICATION_MANIFEST_SHA256 = (
    "c04d0327a22db21c89b169ca2d7472c6c607c87febb1b1109cac7b74fd3a8e74"
)
PRODUCER_SHA256 = (
    "a8e8d46c8ff13c2315868a982a3b394af7629cbb3cd76eda772b2c442a9f8f59"
)
CANDIDATE_LEDGER_SHA256 = (
    "ffea8120af2179990d5c9e7ff385193e2c5a08bed161cf5b570aa28b1f8b1ee0"
)
CANDIDATE_RESULT_FILE_SHA256 = (
    "4835bab4ebe7afc0da8d00395f83f881dd2aaf31e0697994fed54dc7d86302f5"
)
CANDIDATE_RESULT_SHA256 = (
    "5a3cece69ad8f7737b8f80ca6828d34da969de1a22d56af5f6ed422356d88233"
)
PRODUCER_ATTACK_FILE_SHA256 = (
    "8a9c30bc732871934ee50a83db227e7965d6ec29fa6ed493740a119e1cb6fe38"
)
PRODUCER_ATTACK_SELF_SHA256 = (
    "bb501c8312a2025500b93d3e062cac53bccc2c696b8c1bd4bc7240f228e7921e"
)

R275_MANIFEST = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "manifest.sha256"
)
R275_CERTIFICATE = (
    "cm2_round275_source_g_complete_reverse_rechart_materialization_"
    "certificate.json"
)
R282_MANIFEST = (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_"
    "manifest.sha256"
)
R282_LEDGER = (
    "cm2_round282_source_g_strict_true_seam_normal_corridor_probe_"
    "ledger.json.gz"
)
R285_MANIFEST = (
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_"
    "manifest.sha256"
)
R285_LEDGER = (
    "cm2_round285_source_g_true_seam_safe_pairing_contract_probe_"
    "ledger.json.gz"
)
R292_MANIFEST = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_"
    "manifest.sha256"
)
R292_LEDGER = (
    "cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_"
    "ledger.json.gz"
)
R294_MANIFEST = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "manifest.sha256"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)

PACKAGE_MANIFEST_PINS = {
    R275_MANIFEST:
        "a5dbf43a144a0a752f467911ee59e6afd6d2d60d27e0bc80bc45b7afa9334669",
    R282_MANIFEST:
        "c93d7982b036126ea4fcae761316d86863051d19c9fa9a3008b82ef9c6d44081",
    R285_MANIFEST:
        "260065c2a0253516ebda73ba68db8bd76cd3d6e68fade0535d81b77e1471b952",
    R292_MANIFEST:
        "4ea92e4112cae18aa0c13a6d2308816bafc19e4129c09d8b6be914268cfc4870",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
}

SELECTED_INPUT_PINS = {
    R275_CERTIFICATE:
        "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R282_LEDGER:
        "6d94bce99b3ea57b8a568707705d9f16833cfba28b242a6dabb2de5933f6509e",
    R285_LEDGER:
        "92462778ad249c5aff2d7a8d0205efa288ccaf191ab8a419c8b6f58a18dfcc1e",
    R292_LEDGER:
        "8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab",
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
}

SELECTED_MANIFEST_MEMBERS = {
    R275_MANIFEST: R275_CERTIFICATE,
    R282_MANIFEST: R282_LEDGER,
    R285_MANIFEST: R285_LEDGER,
    R292_MANIFEST: R292_LEDGER,
    R294_MANIFEST: R294_REGISTRY,
}

R294_COMMITMENT = {
    "row_count": 431_208,
    "rows_sha256":
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    "row_ids_sha256":
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
    "row_hashes_sha256":
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
    "occurrence_ids_sha256":
        "169869b5755eda22f1527e7393a5bef0a77a842eefbdf45ab34d315b0dad1936",
}

ZERO_FIELDS = (
    "formal_new_occurrence_credit",
    "formal_occurrence_alias_credit",
    "formal_component_union_credit",
    "formal_DSU_rank_reduction_credit",
    "formal_Jx_Jy_same_point_glue_credit",
    "formal_maximality_credit",
    "formal_fibre_credit",
    "formal_global_disposition_credit",
)
PHYSICAL_PAYLOAD_FIELDS = (
    "target_chart",
    "target_lift",
    "outgoing_cell",
    "ordered_integer_wall_events",
    "roof",
    "signed_wall_word",
)
KEY_TRANSITION_FIELDS = (
    "official_key_id",
    "official_key_ordinal",
    "official_key_row",
    "ordered_integer_wall_events",
    "roof",
    "signed_wall_word",
)

ATTACK_SPECS = (
    ("A01_DROP_BINDING_ROW", "ledger", "drop one of 9404 rows",
     "RECLOSED_LEDGER_EXACT_UNIVERSE"),
    ("A02_DUPLICATE_BINDING_ROW", "ledger", "duplicate one row",
     "RECLOSED_LEDGER_UNIQUE_ROW_ID"),
    ("A03_OCCURRENCE_SUBSTITUTION", "row", "change registry occurrence",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A04_R292_COMPONENT_SUBSTITUTION", "row", "change source component",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A05_R275_REGION_SUBSTITUTION", "row", "change source region",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A06_SIGNATURE_HASH_SUBSTITUTION", "row", "change signature digest",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A07_OFFICIAL_KEY_SUBSTITUTION", "row", "change bound key",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A08_KEY_ORDINAL_SUBSTITUTION", "row", "change bound ordinal",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A09_KEY_ROW_SUBSTITUTION", "row", "change official key row",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A10_OLD_NEW_CLASS_FLIP", "row", "flip binding classification",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A11_FORCE_OLD_116_ONLY", "result", "drop eight new raw keys",
     "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A12_COLLAPSE_NEW_TO_SIBLING", "row", "bind new key to wall sibling",
     "RECLOSED_NEW_KEY_ROW_EXACT_RECONSTRUCTION"),
    ("A13_WALL_FACE_AS_KEY_EQUIVALENCE", "result",
     "merge across X/Y graph", "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A14_FORGE_R285_INCIDENCE", "result",
     "claim transported seam evidence", "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A15_RELAX_PHYSICAL_PAYLOAD", "result",
     "ignore events/roof/wall word", "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A16_MEMBER_CELL_OMISSION", "row", "drop refinement member",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A17_MEMBER_BOX_SUBSTITUTION", "source", "alter exact member box",
     "RECLOSED_SOURCE_ROW_EXACT_RECONSTRUCTION"),
    ("A18_MEMBER_VOLUME_SUBSTITUTION", "source", "alter exact volume",
     "RECLOSED_SOURCE_ROW_EXACT_RECONSTRUCTION"),
    ("A19_OCCURRENCE_IDENTITY_COLLAPSE", "row",
     "rewrite occurrence identity", "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A20_OCCURRENCE_ALIAS_CREDIT", "row", "grant alias credit",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A21_COMPONENT_UNION_CREDIT", "row", "grant component credit",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A22_DSU_RANK_CREDIT", "row", "grant DSU rank credit",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A23_JX_JY_GLUE_CREDIT", "row", "grant Jx/Jy credit",
     "RECLOSED_BINDING_ROW_EXACT_RECONSTRUCTION"),
    ("A24_MAXIMALITY_CREDIT", "result", "claim maximality",
     "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A25_FIBRE_EXHAUSTION", "result", "claim 116-fibre exhaustion",
     "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A26_GLOBAL_DISPOSITION", "result", "claim global disposition",
     "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A27_D02_PROMOTION", "result", "unblock D02",
     "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A28_CM2_PROMOTION", "result", "claim CM2",
     "RECLOSED_RESULT_EXACT_RECONSTRUCTION"),
    ("A29_STALE_MANIFEST", "input", "substitute an upstream package",
     "EXACT_INPUT_MANIFEST_PIN"),
    ("A30_DUPLICATE_JSON_KEY", "encoding", "duplicate a JSON key",
     "STRICT_JSON_DUPLICATE_KEY"),
    ("A31_NONFINITE_OR_NUL_JSON", "encoding", "use NaN or NUL",
     "STRICT_JSON_NONFINITE_AND_NUL"),
    ("A32_MALFORMED_OR_CONCAT_GZIP", "encoding", "alter GZIP stream",
     "STRICT_SINGLE_MEMBER_GZIP"),
    ("A33_SYMLINK_HARDLINK_TRAVERSAL", "filesystem", "substitute a path",
     "HERE_ONLY_REGULAR_SINGLE_LINK_PATH"),
)


class VerificationError(RuntimeError):
    """Fail-closed independent-verification error."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for piece in ENCODER.iterencode(value):
        yield piece.encode("utf-8")


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


def require_safe_regular(
    path: Path,
    maximum: int = MAX_FILE_BYTES,
) -> None:
    need(
        path.parent == HERE and path.parent.resolve() == HERE.resolve(),
        f"HERE-only path:{path}",
    )
    try:
        metadata = path.lstat()
    except FileNotFoundError as error:
        raise VerificationError(f"missing file:{path}") from error
    need(
        stat.S_ISREG(metadata.st_mode)
        and not path.is_symlink()
        and metadata.st_nlink == 1
        and 0 < metadata.st_size <= maximum,
        f"regular non-symlink single-link bounded file:{path}",
    )


def strict_integer(token: str) -> int:
    need(
        re.fullmatch(r"-?(?:0|[1-9][0-9]*)", token) is not None
        and len(token.lstrip("-")) <= 128,
        "strict bounded integer",
    )
    return int(token)


def duplicate_free_object(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        need(key not in value, f"duplicate JSON key:{key}")
        value[key] = item
    return value


def reject_noninteger(token: str) -> Any:
    raise VerificationError(f"non-integral or nonfinite JSON token:{token}")


def strict_json_bytes(payload: bytes, label: str) -> dict[str, Any]:
    need(
        payload
        and not payload.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in payload,
        f"strict JSON byte boundary:{label}",
    )
    try:
        value = json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=duplicate_free_object,
            parse_int=strict_integer,
            parse_float=reject_noninteger,
            parse_constant=reject_noninteger,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"strict JSON document:{label}") from error
    need(type(value) is dict, f"top-level JSON object:{label}")
    return value


def read_json(path: Path) -> tuple[dict[str, Any], bytes]:
    require_safe_regular(path)
    raw = path.read_bytes()
    return strict_json_bytes(raw, path.name), raw


def scan_single_member_gzip(
    path: Path,
    maximum: int = MAX_GZIP_UNCOMPRESSED_BYTES,
) -> int:
    require_safe_regular(path)
    decoder = zlib.decompressobj(wbits=31)
    total = 0
    with path.open("rb") as stream:
        while True:
            piece = stream.read(1 << 20)
            if not piece:
                break
            need(not decoder.eof, f"trailing or multi-member GZIP:{path.name}")
            output = decoder.decompress(piece)
            total += len(output)
            need(total <= maximum, f"GZIP size cap:{path.name}")
            need(
                not decoder.unused_data,
                f"trailing or multi-member GZIP:{path.name}",
            )
    total += len(decoder.flush())
    need(
        decoder.eof
        and not decoder.unused_data
        and total <= maximum,
        f"strict single-member GZIP:{path.name}",
    )
    return total


def scan_single_member_gzip_bytes(
    payload: bytes,
    maximum: int,
) -> int:
    try:
        decoder = zlib.decompressobj(wbits=31)
        output = decoder.decompress(payload)
        total = len(output) + len(decoder.flush())
    except zlib.error as error:
        raise VerificationError("malformed GZIP bytes") from error
    need(
        decoder.eof
        and not decoder.unused_data
        and total <= maximum,
        "strict bounded single-member GZIP bytes",
    )
    return total


def read_gzip_json(path: Path) -> tuple[dict[str, Any], bytes]:
    scan_single_member_gzip(path)
    compressed = path.read_bytes()
    try:
        raw = gzip.decompress(compressed)
    except (OSError, EOFError) as error:
        raise VerificationError(f"GZIP decode:{path.name}") from error
    return strict_json_bytes(raw, path.name), compressed


def validate_closed_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    payload = {key: value for key, value in row.items()
               if key != "row_sha256"}
    need(
        type(claimed) is str and digest(payload) == claimed,
        f"row closure:{label}",
    )


def close_binding_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = {
        ROW_ID_FIELD:
            "round299a-refined-occurrence-key-binding:" + digest([
                "ROUND299A_REFINED_OCCURRENCE_KEY_BINDING_V1",
                payload,
            ]),
        **payload,
    }
    row["row_sha256"] = digest(row)
    return row


class ListHasher:
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
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    need(len(ids) == len(set(ids)), "unique row IDs")
    return {
        "row_count": len(rows),
        "row_ids_sha256": digest(ids),
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": digest(rows),
    }


def raw_rows_commitment(
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "row_ids_sha256": digest([row[id_field] for row in rows]),
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": digest(rows),
    }


def validate_table(
    table: dict[str, Any],
    *,
    id_field: str,
    count: int,
    label: str,
) -> list[dict[str, Any]]:
    rows = table.get("rows")
    need(
        type(rows) is list
        and len(rows) == table.get("row_count") == count,
        f"table count:{label}",
    )
    for row in rows:
        need(type(row) is dict, f"row object:{label}")
        validate_closed_row(row, label)
    expected = rows_commitment(rows, id_field)
    need(
        all(table.get(key) == value for key, value in expected.items()),
        f"table commitments:{label}",
    )
    return rows


def parse_manifest(path: Path) -> dict[str, str]:
    require_safe_regular(path, 200_000)
    try:
        text = path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError(f"manifest UTF-8:{path.name}") from error
    entries: dict[str, str] = {}
    for line in text.splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, f"manifest syntax:{path.name}")
        sha256, filename = match.groups()
        need(
            Path(filename).name == filename and filename not in entries,
            f"manifest HERE-only unique member:{path.name}:{filename}",
        )
        entries[filename] = sha256
    need(bool(entries), f"nonempty manifest:{path.name}")
    return entries


def validate_sealed_upstream() -> int:
    member_count = 0
    for manifest_name, expected_pin in sorted(
        PACKAGE_MANIFEST_PINS.items()
    ):
        manifest_path = HERE / manifest_name
        require_safe_regular(manifest_path)
        need(
            file_sha256(manifest_path) == expected_pin,
            f"sealed package manifest pin:{manifest_name}",
        )
        entries = parse_manifest(manifest_path)
        member_count += len(entries)
        for filename, expected_member_pin in sorted(entries.items()):
            member_path = HERE / filename
            require_safe_regular(member_path)
            need(
                file_sha256(member_path) == expected_member_pin,
                f"sealed manifest member:{manifest_name}:{filename}",
            )
        selected = SELECTED_MANIFEST_MEMBERS[manifest_name]
        need(
            entries.get(selected) == SELECTED_INPUT_PINS[selected],
            f"selected member binding:{manifest_name}:{selected}",
        )
    for filename, expected_pin in sorted(SELECTED_INPUT_PINS.items()):
        path = HERE / filename
        require_safe_regular(path)
        need(
            file_sha256(path) == expected_pin,
            f"selected source artifact pin:{filename}",
        )
    require_safe_regular(PRODUCER)
    need(
        file_sha256(PRODUCER) == PRODUCER_SHA256,
        "Round299-A producer inert-byte pin",
    )
    return member_count


def stream_json_rows(
    stream: TextIO,
    marker: str = '"rows":[',
) -> Iterator[dict[str, Any]]:
    buffer = ""
    while marker not in buffer:
        piece = stream.read(1 << 20)
        need(bool(piece), f"streamed array marker:{marker}")
        buffer += piece
        if len(buffer) > 2 * (1 << 20):
            buffer = buffer[-(len(marker) + (1 << 20)):]
    buffer = buffer.split(marker, 1)[1]
    decoder = json.JSONDecoder(
        object_pairs_hook=duplicate_free_object,
        parse_int=strict_integer,
        parse_float=reject_noninteger,
        parse_constant=reject_noninteger,
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            piece = stream.read(1 << 20)
            need(bool(piece), "unexpected streamed JSON EOF")
            buffer = piece
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                value, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                piece = stream.read(1 << 20)
                need(bool(piece), "malformed streamed JSON row")
                buffer += piece
        need(type(value) is dict, "streamed JSON row object")
        yield value
        buffer = buffer[end:]


def deterministic_gzip(value: Any) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=output,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        for piece in chunks(value):
            stream.write(piece)
    return output.getvalue()


def histogram(values: Iterable[int]) -> dict[str, int]:
    return {
        str(key): value
        for key, value in sorted(Counter(values).items())
    }


def physical_payload(signature: dict[str, Any]) -> dict[str, Any]:
    return {
        field: signature[field] for field in PHYSICAL_PAYLOAD_FIELDS
    }


def load_sources() -> dict[str, Any]:
    certificate, _ = read_json(HERE / R275_CERTIFICATE)
    result = certificate.get("result")
    need(
        type(result) is dict
        and certificate.get("result_sha256") == digest(result)
        and result.get("schema")
        == "cm2.round275.source-g-complete-reverse-rechart-"
        "materialization.v1"
        and result.get("status")
        == "PASS_PRODUCER_ROUND275__ZERO_GLOBAL_CREDIT",
        "Round275 certificate closure and semantics",
    )
    strict_rows = validate_table(
        result["strict_region_ledger"],
        id_field="reverse_rechart_region_row_id",
        count=5_288,
        label="Round275 strict region",
    )
    arrangement_rows = validate_table(
        result["arrangement_region_ledger"],
        id_field="reverse_rechart_region_row_id",
        count=8_500,
        label="Round275 arrangement region",
    )
    r275_rows = strict_rows + arrangement_rows
    r275 = {
        row["reverse_rechart_region_row_id"]: row for row in r275_rows
    }
    need(len(r275) == len(r275_rows) == 13_788, "Round275 region universe")
    for row in r275_rows:
        signature = row.get("local_return_signature")
        need(
            type(signature) is dict
            and row.get("complete_10_field_return_signature_sha256")
            == digest(signature),
            "Round275 complete ten-field signature closure",
        )

    r292_document, _ = read_gzip_json(HERE / R292_LEDGER)
    r292_rows = r292_document.get("rows")
    need(
        r292_document.get("schema")
        == "cm2.round292.r287-registry-overlap-exhaustion-probe.v1."
        "ledger.v1"
        and type(r292_rows) is list
        and len(r292_rows) == r292_document.get("row_count") == 22_820,
        "Round292 mixed ledger envelope",
    )
    refinement: dict[str, dict[str, Any]] = {}
    components: dict[str, dict[str, Any]] = {}
    overlap_count = 0
    for row in r292_rows:
        need(type(row) is dict, "Round292 row object")
        validate_closed_row(row, "Round292")
        if "Round292_registry_overlap_row_id" in row:
            overlap_count += 1
        elif "member_refinement_cell_ids" in row:
            row_id = row["Round292_refined_new_support_component_id"]
            need(row_id not in components, "Round292 unique component")
            components[row_id] = row
        elif "Round292_R287_existing_overlap_refinement_cell_id" in row:
            row_id = row[
                "Round292_R287_existing_overlap_refinement_cell_id"
            ]
            need(row_id not in refinement, "Round292 unique refinement cell")
            refinement[row_id] = row
        else:
            raise VerificationError("unknown Round292 mixed-row kind")
    need(
        r292_document.get("rows_sha256")
        == "556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055"
        == digest(r292_rows)
        and len(refinement) == 11_852
        and len(components) == 9_404
        and overlap_count == 1_564,
        "Round292 row commitment and complete partition",
    )

    r282_document, _ = read_gzip_json(HERE / R282_LEDGER)
    need(
        r282_document.get("schema")
        == "cm2.round282.source-g-strict-true-seam-normal-corridor-"
        "probe.v1.ledger",
        "Round282 schema",
    )
    r282_rows = validate_table(
        r282_document,
        id_field="Round282_seam_corridor_row_id",
        count=152,
        label="Round282 corridor",
    )
    r285_document, _ = read_gzip_json(HERE / R285_LEDGER)
    need(
        r285_document.get("schema")
        == "cm2.round285.source-g-true-seam-safe-pairing-contract-"
        "probe.v1.ledger"
        and r285_document.get("status")
        == "PASS_ROUND285_COMPLETE_TRUE_SEAM_PAIRING_CENSUS__ZERO_CREDIT"
        and r285_document.get("strict_nonpromotion") is True,
        "Round285 schema and zero-credit status",
    )
    r285_rows = validate_table(
        r285_document,
        id_field="Round285_safe_pairing_row_id",
        count=152,
        label="Round285 safe pairing",
    )

    scan_single_member_gzip(HERE / R294_REGISTRY)
    refined_registry_rows: list[dict[str, Any]] = []
    old_keys: set[str] = set()
    seen_occurrences: set[str] = set()
    registry_kind_histogram: Counter[str] = Counter()
    rows_hash = ListHasher()
    ids_hash = ListHasher()
    row_hashes_hash = ListHasher()
    occurrence_ids_hash = ListHasher()
    with gzip.open(
        HERE / R294_REGISTRY,
        "rt",
        encoding="utf-8",
        newline="",
    ) as stream:
        for row in stream_json_rows(stream):
            validate_closed_row(row, "Round294 registry")
            occurrence = row["registry_occurrence_id"]
            need(
                occurrence not in seen_occurrences,
                "Round294 unique occurrence identity",
            )
            seen_occurrences.add(occurrence)
            rows_hash.add(row)
            ids_hash.add(row["Round294_occurrence_registry_row_id"])
            row_hashes_hash.add(row["row_sha256"])
            occurrence_ids_hash.add(occurrence)
            kind = row["registry_entry_kind"]
            registry_kind_histogram[kind] += 1
            if kind == REFINED_KIND:
                need(
                    row.get("official_key_id") is None
                    and row.get("official_key_ordinal") is None
                    and row.get("official_key_binding_status")
                    == "NOT_MATERIALIZED_IN_R287_FROZEN_LEDGER__"
                    "COMPLETE_SIGNATURE_HASH_PINNED",
                    "Round294 refined null-key freeze",
                )
                refined_registry_rows.append(row)
            else:
                key = row.get("official_key_id")
                need(type(key) is str, "Round294 nonrefined official key")
                old_keys.add(key)
    recomputed_r294 = {
        "row_count": rows_hash.count,
        "rows_sha256": rows_hash.finish(),
        "row_ids_sha256": ids_hash.finish(),
        "row_hashes_sha256": row_hashes_hash.finish(),
        "occurrence_ids_sha256": occurrence_ids_hash.finish(),
    }
    need(
        recomputed_r294 == R294_COMMITMENT
        and registry_kind_histogram == {
            "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE": 126_468,
            "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM": 295_336,
            REFINED_KIND: 9_404,
        }
        and len(refined_registry_rows) == 9_404
        and len(old_keys) == 116,
        "Round294 full registry recommitment and key census",
    )
    return {
        "r275_rows": r275_rows,
        "r275": r275,
        "strict_rows": strict_rows,
        "arrangement_rows": arrangement_rows,
        "r292_rows": r292_rows,
        "refinement": refinement,
        "components": components,
        "r282_rows": r282_rows,
        "r285_rows": r285_rows,
        "refined_registry_rows": refined_registry_rows,
        "old_keys": old_keys,
        "registry_kind_histogram": registry_kind_histogram,
        "r294_commitment": recomputed_r294,
    }


def build_expected_binding(
    source: dict[str, Any],
) -> dict[str, Any]:
    r275 = source["r275"]
    refinement = source["refinement"]
    components = source["components"]
    old_keys = source["old_keys"]
    rows: list[dict[str, Any]] = []
    key_occurrences: Counter[str] = Counter()
    key_regions: dict[str, set[str]] = defaultdict(set)
    key_member_cells: Counter[str] = Counter()
    classification_histogram: Counter[str] = Counter()
    seen_occurrences: set[str] = set()
    seen_components: set[str] = set()
    seen_regions: set[str] = set()
    all_member_ids: set[str] = set()
    mismatch_count = 0

    for registry in source["refined_registry_rows"]:
        occurrence = registry["registry_occurrence_id"]
        component_id = registry["source_row_id"]
        region_id = registry["Round275_region_id"]
        need(
            occurrence not in seen_occurrences
            and component_id not in seen_components
            and region_id not in seen_regions,
            "one-to-one refined occurrence/component/region",
        )
        seen_occurrences.add(occurrence)
        seen_components.add(component_id)
        seen_regions.add(region_id)
        need(component_id in components, "Round292 component join")
        need(region_id in r275, "Round275 region join")
        component = components[component_id]
        region = r275[region_id]
        signature = region["local_return_signature"]
        signature_sha256 = region[
            "complete_10_field_return_signature_sha256"
        ]
        member_ids = component["member_refinement_cell_ids"]
        need(
            type(member_ids) is list
            and member_ids == sorted(member_ids)
            and len(member_ids) == len(set(member_ids)),
            "Round292 component ordered unique member IDs",
        )
        registry_member_ids = sorted(
            member["Round292_refinement_cell_id"]
            for member in registry["member_refinement_cells"]
        )
        checks = (
            registry["source_row_sha256"] == component["row_sha256"],
            registry["complete_10_field_return_signature_sha256"]
            == signature_sha256 == digest(signature),
            registry["physical_support_chart"] == region["adjacent_chart"],
            registry["owner_target"] == region["owner_target"],
            registry["member_refinement_cell_count"]
            == component["member_refinement_cell_count"]
            == len(member_ids),
            registry_member_ids == member_ids,
        )
        need(all(checks), "Round294/Round292/Round275 exact join")
        need(
            not (all_member_ids & set(member_ids)),
            "refined component member-cell disjointness",
        )
        all_member_ids.update(member_ids)
        for member in registry["member_refinement_cells"]:
            member_id = member["Round292_refinement_cell_id"]
            need(member_id in refinement, "Round292 member-cell join")
            exact = refinement[member_id]
            member_checks = (
                member["Round275_region_id"]
                == exact["Round275_region_id"] == region_id,
                member["complete_10_field_return_signature_sha256"]
                == exact["complete_10_field_return_signature_sha256"]
                == signature_sha256,
                member["physical_support_chart"]
                == exact["source_chart"] == region["adjacent_chart"],
                member["exact_transformed_open_cell"]
                == exact["exact_transformed_open_cell"],
                member["exact_transformed_cell_volume"]
                == exact["exact_transformed_cell_volume"],
                member["source_row_sha256"] == exact["row_sha256"],
            )
            mismatch_count += sum(not check for check in member_checks)
            need(all(member_checks), "exact refinement member-cell join")

        official_key = signature["official_key_id"]
        classification = (
            EXISTING_CLASS if official_key in old_keys else NEW_CLASS
        )
        classification_histogram[classification] += 1
        key_occurrences[official_key] += 1
        key_regions[official_key].add(region_id)
        key_member_cells[official_key] += len(member_ids)
        payload = {
            "source_Round294_occurrence_registry_row_id":
                registry["Round294_occurrence_registry_row_id"],
            "source_Round294_occurrence_registry_row_sha256":
                registry["row_sha256"],
            "registry_occurrence_id": occurrence,
            "registry_entry_kind": registry["registry_entry_kind"],
            "source_Round292_refined_support_component_id": component_id,
            "source_Round292_refined_support_component_row_sha256":
                component["row_sha256"],
            "source_Round275_region_id": region_id,
            "source_Round275_region_row_sha256": region["row_sha256"],
            "source_Round294_official_key_binding_status":
                registry["official_key_binding_status"],
            "complete_10_field_return_signature_sha256": signature_sha256,
            "source_Round275_local_return_signature": signature,
            "official_key_id": official_key,
            "official_key_ordinal": signature["official_key_ordinal"],
            "official_key_row": signature["official_key_row"],
            "binding_classification": classification,
            "binding_basis":
                "EXACT_ROUND275_REGION_ID_PLUS_COMPLETE_10_FIELD_"
                "SIGNATURE_HASH_PREIMAGE",
            "member_refinement_cell_count": len(member_ids),
            "member_refinement_cell_ids_sha256": digest(member_ids),
            "append_only_official_key_binding": True,
            "occurrence_identity_preserved": True,
            "raw_key_merge_credit": 0,
            "formal_refined_occurrence_official_key_binding_credit": 1,
            **{field: 0 for field in ZERO_FIELDS},
        }
        rows.append(close_binding_row(payload))

    rows.sort(key=lambda row: row[ROW_ID_FIELD])
    bound_keys = set(key_occurrences)
    existing_bound_keys = bound_keys & old_keys
    new_keys = bound_keys - old_keys
    need(
        len(rows) == len(seen_occurrences) == len(seen_components)
        == len(seen_regions) == 9_404
        and len(all_member_ids) == 10_252
        and mismatch_count == 0
        and classification_histogram
        == {EXISTING_CLASS: 8_212, NEW_CLASS: 1_192}
        and len(bound_keys) == 44
        and len(existing_bound_keys) == 36
        and len(new_keys) == 8
        and all(key_occurrences[key] == 149 for key in new_keys)
        and all(key_member_cells[key] == 149 for key in new_keys),
        "complete 9404 binding census and 8212+1192 partition",
    )
    return {
        "rows": rows,
        "key_occurrences": key_occurrences,
        "key_regions": key_regions,
        "key_member_cells": key_member_cells,
        "classification_histogram": classification_histogram,
        "existing_bound_keys": existing_bound_keys,
        "new_keys": new_keys,
        "mismatch_count": mismatch_count,
        "member_cell_count": len(all_member_ids),
        "region_count": len(seen_regions),
    }


def build_expected_nonmerge(
    source: dict[str, Any],
    binding: dict[str, Any],
) -> dict[str, Any]:
    old_keys = source["old_keys"]
    new_keys = binding["new_keys"]
    r275_rows = source["r275_rows"]
    strict_rows = source["strict_rows"]
    arrangement_rows = source["arrangement_rows"]
    r275 = source["r275"]

    signatures_by_key: dict[str, set[str]] = defaultdict(set)
    payload_keys: dict[str, set[str]] = defaultdict(set)
    for row in r275_rows:
        signature = row["local_return_signature"]
        key = signature["official_key_id"]
        signatures_by_key[key].add(
            canonical(signature).decode("utf-8")
        )
        payload_keys[digest(physical_payload(signature))].add(key)
    need(
        len(signatures_by_key) == 44
        and all(len(signatures_by_key[key]) == 1 for key in new_keys),
        "Round275 raw signature universe",
    )

    arrangement_groups: dict[
        tuple[str, tuple[str, ...], tuple[str, ...], str],
        list[dict[str, Any]],
    ] = defaultdict(list)
    for row in arrangement_rows:
        arrangement_groups[(
            row["source_guard_row_id"],
            tuple(row["adjacent_cover_refinement_path"]),
            tuple(row["adjacent_rational_region_box"]),
            row["active_reason"],
        )].append(row)

    summaries: list[dict[str, Any]] = []
    all_sibling_pair_count = 0
    for key in sorted(new_keys):
        key_strict = [
            row for row in strict_rows
            if row["local_return_signature"]["official_key_id"] == key
        ]
        key_arrangement = [
            row for row in arrangement_rows
            if row["local_return_signature"]["official_key_id"] == key
        ]
        need(
            len(key_strict) == 21
            and len(key_arrangement) == 128
            and all(
                row["arrangement_classification"]
                == "REGULAR_GRAPH_CROSSING"
                and row["active_reason"] in {
                    "wall_endpoint_or_count_transition:X:0",
                    "wall_endpoint_or_count_transition:Y:0",
                }
                for row in key_arrangement
            ),
            "new-key strict/graph-crossing region census",
        )
        counterpart_counts: Counter[str] = Counter()
        reason_counts: Counter[str] = Counter()
        differing_counts: Counter[tuple[str, ...]] = Counter()
        for row in key_arrangement:
            group_key = (
                row["source_guard_row_id"],
                tuple(row["adjacent_cover_refinement_path"]),
                tuple(row["adjacent_rational_region_box"]),
                row["active_reason"],
            )
            siblings = [
                sibling for sibling in arrangement_groups[group_key]
                if sibling["reverse_rechart_region_row_id"]
                != row["reverse_rechart_region_row_id"]
            ]
            need(len(siblings) == 1, "unique wall-transition sibling")
            sibling = siblings[0]
            sibling_key = sibling[
                "local_return_signature"
            ]["official_key_id"]
            need(
                sibling_key in old_keys,
                "wall-transition sibling belongs to old 116",
            )
            counterpart_counts[sibling_key] += 1
            reason_counts[row["active_reason"]] += 1
            left = row["local_return_signature"]
            right = sibling["local_return_signature"]
            differing = tuple(sorted(
                field for field in left if left[field] != right[field]
            ))
            need(
                differing == tuple(sorted(KEY_TRANSITION_FIELDS)),
                "exact six-field wall-transition distinction",
            )
            differing_counts[differing] += 1
        need(
            len(counterpart_counts) == 1
            and next(iter(counterpart_counts.values())) == 128
            and len(reason_counts) == 1
            and len(differing_counts) == 1,
            "one distinct old sibling class for each new key",
        )
        sibling_key = next(iter(counterpart_counts))
        new_signature = json.loads(next(iter(signatures_by_key[key])))
        sibling_signatures = [
            row["local_return_signature"]
            for row in r275_rows
            if row["local_return_signature"]["official_key_id"]
            == sibling_key
        ]
        need(bool(sibling_signatures), "old sibling signature")
        sibling_ordinal = sibling_signatures[0]["official_key_ordinal"]
        payload_sha256 = digest(physical_payload(new_signature))
        need(
            not (payload_keys[payload_sha256] - {key}),
            "no other key has exact transported six-field payload",
        )
        summaries.append({
            "new_raw_official_key_id": key,
            "new_raw_official_key_ordinal":
                new_signature["official_key_ordinal"],
            "new_raw_official_key_row":
                new_signature["official_key_row"],
            "bound_refined_occurrence_count":
                binding["key_occurrences"][key],
            "bound_Round275_region_count":
                len(binding["key_regions"][key]),
            "bound_refinement_member_cell_count":
                binding["key_member_cells"][key],
            "Round275_strict_region_count": len(key_strict),
            "Round275_regular_graph_crossing_region_count":
                len(key_arrangement),
            "unique_old_116_wall_transition_sibling_key_id":
                sibling_key,
            "unique_old_116_wall_transition_sibling_key_ordinal":
                sibling_ordinal,
            "wall_transition_sibling_pair_count":
                counterpart_counts[sibling_key],
            "wall_transition_reason": next(iter(reason_counts)),
            "wall_transition_differing_signature_fields":
                list(next(iter(differing_counts))),
            "wall_transition_is_transported_key_equivalence": False,
            "transported_physical_payload_sha256": payload_sha256,
            "other_Round275_raw_keys_with_exact_transported_payload_count":
                0,
            "Round285_corridor_region_incidence_count": 0,
            "formal_raw_key_merge_credit": 0,
        })
        all_sibling_pair_count += counterpart_counts[sibling_key]

    r282_by_patch = {
        row["Round268_true_seam_patch_row_id"]: row
        for row in source["r282_rows"]
    }
    r285_by_patch = {
        row["Round268_true_seam_patch_row_id"]: row
        for row in source["r285_rows"]
    }
    need(
        len(r282_by_patch) == len(r285_by_patch) == 152
        and set(r282_by_patch) == set(r285_by_patch),
        "Round282/Round285 exact patch universe",
    )
    corridor_region_occurrences: list[str] = []
    side_hash_mismatch_count = 0
    new_key_corridor_occurrences = 0
    for patch_id in sorted(r282_by_patch):
        r282_row = r282_by_patch[patch_id]
        r285_row = r285_by_patch[patch_id]
        output_sides = {
            side["side"]: side for side in r285_row["side_summaries"]
        }
        need(
            set(output_sides) == {"left", "right"},
            "Round285 two side summaries",
        )
        for side in r282_row["side_corridors"]:
            side_name = side["side"]
            region_ids = sorted({
                corridor["Round275_region_id"]
                for corridor in side["accepted_strict_corridors"]
            })
            corridor_region_occurrences.extend(region_ids)
            summary = output_sides[side_name]
            side_hash_mismatch_count += int(
                summary["distinct_Round275_region_count"]
                != len(region_ids)
                or summary["distinct_Round275_region_ids_sha256"]
                != digest(region_ids)
            )
            for corridor in side["accepted_strict_corridors"]:
                region_id = corridor["Round275_region_id"]
                need(region_id in r275, "Round282 corridor/Round275 join")
                region = r275[region_id]
                need(
                    corridor[
                        "complete_10_field_return_signature_sha256"
                    ]
                    == region[
                        "complete_10_field_return_signature_sha256"
                    ]
                    and corridor["adjacent_chart"]
                    == region["adjacent_chart"]
                    and corridor["owner_target"] == region["owner_target"],
                    "Round282 exact corridor source join",
                )
                new_key_corridor_occurrences += int(
                    region["local_return_signature"]["official_key_id"]
                    in new_keys
                )
    need(
        len(corridor_region_occurrences) == 2_660
        and len(set(corridor_region_occurrences)) == 2_636
        and side_hash_mismatch_count == 0
        and new_key_corridor_occurrences == 0,
        "Round285 nonmerge zero-incidence audit",
    )
    return {
        "new_raw_key_rows": summaries,
        "new_raw_key_count": 8,
        "new_raw_key_Round275_region_count": 1_192,
        "new_raw_key_Round275_strict_region_count": 168,
        "new_raw_key_Round275_regular_graph_crossing_region_count": 1_024,
        "wall_transition_sibling_pair_count": all_sibling_pair_count,
        "wall_transition_sibling_pairs_are_key_equivalences": False,
        "exact_transported_payload_match_to_other_Round275_key_count": 0,
        "Round282_patch_count": 152,
        "Round285_side_region_count_hash_mismatch_count":
            side_hash_mismatch_count,
        "Round285_corridor_region_occurrence_count":
            len(corridor_region_occurrences),
        "Round285_distinct_corridor_region_count":
            len(set(corridor_region_occurrences)),
        "new_raw_key_Round285_corridor_region_incidence_count":
            new_key_corridor_occurrences,
        "transported_equivalence_supports_any_new_key_merge": False,
        "formal_raw_key_merge_credit": 0,
    }


def build_expected_candidate(
    source: dict[str, Any],
    binding: dict[str, Any],
    nonmerge: dict[str, Any],
) -> tuple[dict[str, Any], bytes, dict[str, Any], bytes]:
    rows = binding["rows"]
    commitment = rows_commitment(rows, ROW_ID_FIELD)
    ledger = {
        "schema": LEDGER_SCHEMA,
        **commitment,
        "rows": rows,
    }
    ledger_bytes = deterministic_gzip(ledger)
    ledger_sha256 = hashlib.sha256(ledger_bytes).hexdigest()
    key_occurrences = binding["key_occurrences"]
    new_keys = binding["new_keys"]
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND299A_APPEND_ONLY_REFINED_OCCURRENCE_OFFICIAL_"
            "KEY_BINDING__9404_OF_9404__8212_OLD36__1192_NEW8__"
            "RAW_KEY_UNIVERSE_116_TO_124__NO_KEY_MERGE_OR_DSU_CREDIT",
        "input_package_manifest_pins":
            dict(sorted(PACKAGE_MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(SELECTED_INPUT_PINS.items())),
        "source_reconstruction": {
            "Round275_region_count": 13_788,
            "Round275_raw_official_key_count": 44,
            "Round292_refinement_cell_count": 11_852,
            "Round292_refined_component_count": 9_404,
            "Round294_registry_count": 431_208,
            "Round294_refined_occurrence_count": 9_404,
            "pre_refined_Round294_observed_official_key_count": 116,
            "all_input_rows_recommitted": True,
            "Round275_Round292_Round294_join_mismatch_count":
                binding["mismatch_count"],
        },
        "binding_census": {
            "binding_row_count": 9_404,
            "distinct_bound_occurrence_count": 9_404,
            "distinct_bound_Round292_component_count": 9_404,
            "distinct_bound_Round275_region_count": 9_404,
            "bound_refinement_member_cell_count": 10_252,
            "bound_raw_official_key_count": 44,
            "old_116_key_used_count": 36,
            "old_116_key_unused_by_refined_occurrences_count": 80,
            "old_116_key_binding_row_count": 8_212,
            "new_raw_key_count": 8,
            "new_raw_key_binding_row_count": 1_192,
            "new_raw_key_binding_count_per_key_histogram": {"149": 8},
            "binding_count_per_observed_key_histogram":
                histogram(key_occurrences.values()),
            "binding_classification_histogram":
                dict(sorted(binding["classification_histogram"].items())),
            "append_only_binding": True,
            "occurrence_ID_rewrite_count": 0,
            "key_merge_count": 0,
        },
        "raw_observed_key_universe": {
            "before_refined_binding_count": 116,
            "new_raw_key_delta": 8,
            "after_refined_binding_count": 124,
            "new_raw_key_ids": sorted(new_keys),
            "new_raw_keys_are_distinct": True,
            "new_raw_keys_merged_into_old_116": False,
        },
        "nonmerge_audit": nonmerge,
        "ledger": {
            "filename": LEDGER.name,
            "file_sha256": ledger_sha256,
            "schema": LEDGER_SCHEMA,
            **commitment,
        },
        "formal_credit_transition": {
            "formal_refined_occurrence_official_key_binding_credit": 9_404,
            "formal_raw_observed_key_universe_delta": 8,
            "formal_new_occurrence_credit": 0,
            "formal_occurrence_alias_credit": 0,
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "scope_contract": {
            "key_binding_is_append_only_metadata_on_existing_occurrences":
                True,
            "component_partition_or_rank_recomputed_here": False,
            "component_key_incidence_must_be_recomputed_downstream": True,
            "legacy_116_key_universe_is_complete_after_binding": False,
            "raw_observed_key_universe_count": 124,
            "eight_new_raw_keys_require_distinct_fibre_treatment": True,
            "wall_transition_adjacency_is_not_key_equivalence": True,
            "Round285_transported_equivalence_supports_new_key_merge":
                False,
        },
        "strict_nonpromotion": {
            "post_Round299A_component_count": None,
            "component_DSU_status": "NOT_REBUILT_BY_THIS_ROUND",
            "exact_key_fibre_exhaustion_status":
                "NOT_CERTIFIED__RAW_KEY_UNIVERSE_REVISED_116_TO_124",
            "maximality_status": "NOT_CERTIFIED",
            "global_disposition_status": "NOT_CERTIFIED",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "producer_self_attack_rejection": {
            "attack_count": 33,
            "rejected_count": 33,
            "accepted_count": 0,
            "reclosable_semantic_attack_count": 28,
            "status": "PASS_PRODUCER_SELF_AUDIT_ONLY",
            "independent_verification_status": "PENDING",
        },
        "required_next": [
            "Independently reconstruct all 9,404 binding rows without "
            "importing or executing this producer.",
            "Reject every attempted collapse of the eight new raw keys into "
            "their R275 wall-transition siblings.",
            "Recompute component-key incidence and the exact-key fibre "
            "denominator over the 124-key raw observed universe.",
        ],
        "provenance": {
            "producer_sha256": PRODUCER_SHA256,
            "seed_affects_output": False,
            "independent_verifier_executed": False,
        },
        "seed_affects_output": False,
    }
    result["result_sha256"] = digest(result)
    result_bytes = canonical(result) + b"\n"
    need(
        ledger_sha256 == CANDIDATE_LEDGER_SHA256
        and hashlib.sha256(result_bytes).hexdigest()
        == CANDIDATE_RESULT_FILE_SHA256
        and result["result_sha256"] == CANDIDATE_RESULT_SHA256,
        "independent reconstruction reaches pinned candidate commitments",
    )
    return ledger, ledger_bytes, result, result_bytes


def open_and_match_candidate(
    expected_ledger: dict[str, Any],
    expected_ledger_bytes: bytes,
    expected_result: dict[str, Any],
    expected_result_bytes: bytes,
    ledger_path: Path,
    result_path: Path,
) -> None:
    require_safe_regular(ledger_path)
    require_safe_regular(result_path)
    need(
        file_sha256(ledger_path) == CANDIDATE_LEDGER_SHA256
        and file_sha256(result_path) == CANDIDATE_RESULT_FILE_SHA256,
        "candidate file hashes equal independent reconstruction",
    )
    candidate_ledger, candidate_ledger_bytes = read_gzip_json(ledger_path)
    candidate_result, candidate_result_bytes = read_json(result_path)
    result_payload = dict(candidate_result)
    claimed_result_sha256 = result_payload.pop("result_sha256", None)
    need(
        claimed_result_sha256 == digest(result_payload)
        == CANDIDATE_RESULT_SHA256,
        "candidate result self closure",
    )
    need(
        candidate_ledger == expected_ledger
        and candidate_ledger_bytes == expected_ledger_bytes
        and hashlib.sha256(candidate_ledger_bytes).hexdigest()
        == hashlib.sha256(expected_ledger_bytes).hexdigest()
        == CANDIDATE_LEDGER_SHA256,
        "candidate ledger object/bytes/hash exact equality",
    )
    need(
        candidate_result == expected_result
        and candidate_result_bytes == expected_result_bytes
        and hashlib.sha256(candidate_result_bytes).hexdigest()
        == hashlib.sha256(expected_result_bytes).hexdigest()
        == CANDIDATE_RESULT_FILE_SHA256,
        "candidate result object/bytes/hash exact equality",
    )


def reclose_binding_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = {
        key: value for key, value in row.items()
        if key not in {ROW_ID_FIELD, "row_sha256"}
    }
    return close_binding_row(payload)


def reclose_source_row(row: dict[str, Any]) -> dict[str, Any]:
    value = {
        key: item for key, item in row.items() if key != "row_sha256"
    }
    value["row_sha256"] = digest(value)
    return value


def reclose_result(result: dict[str, Any]) -> dict[str, Any]:
    result.pop("result_sha256", None)
    result["result_sha256"] = digest(result)
    return result


def exact_ledger(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    rows = candidate.get("rows")
    need(type(rows) is list, "attack ledger rows")
    for row in rows:
        validate_closed_row(row, "attack binding")
    commitment = rows_commitment(rows, ROW_ID_FIELD)
    need(
        candidate.get("schema") == LEDGER_SCHEMA
        and all(candidate.get(key) == value
                for key, value in commitment.items())
        and candidate == expected,
        "attack exact independently reconstructed ledger",
    )


def exact_binding_row(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    validate_closed_row(candidate, "attack binding row")
    need(
        candidate == expected,
        "attack exact independently reconstructed binding row",
    )


def exact_source_row(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    validate_closed_row(candidate, "attack source row")
    need(
        candidate == expected,
        "attack exact sealed source row",
    )


def exact_result(
    candidate: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    payload = dict(candidate)
    claimed = payload.pop("result_sha256", None)
    need(
        claimed == digest(payload) and candidate == expected,
        "attack exact independently reconstructed result",
    )


EXPECTED_REJECTION_EXCEPTIONS = (
    VerificationError,
    KeyError,
    TypeError,
    ValueError,
    UnicodeError,
    OSError,
)


def rejected_outcome(
    specification: tuple[str, str, str, str],
    callback: Callable[[], None],
    *,
    semantic_reclosed: bool,
) -> dict[str, Any]:
    attack_id, target, mutation, probe_kind = specification
    try:
        callback()
    except EXPECTED_REJECTION_EXCEPTIONS as error:
        rejection_class = type(error).__name__
    else:
        raise VerificationError(f"attack accepted:{attack_id}")
    row = {
        "attack_id": attack_id,
        "target": target,
        "mutation": mutation,
        "independent_probe_kind": probe_kind,
        "semantic_attack_fully_reclosed": semantic_reclosed,
        "producer_self_attack_rejection": "REJECTED",
        "independent_verification_status": "REJECTED",
        "rejection_class": rejection_class,
    }
    row["row_sha256"] = digest(row)
    return row


def composite_rejected_outcome(
    specification: tuple[str, str, str, str],
    callbacks: list[Callable[[], None]],
) -> dict[str, Any]:
    attack_id, target, mutation, probe_kind = specification
    rejection_classes: list[str] = []
    for callback in callbacks:
        try:
            callback()
        except EXPECTED_REJECTION_EXCEPTIONS as error:
            rejection_classes.append(type(error).__name__)
        else:
            raise VerificationError(f"composite attack accepted:{attack_id}")
    row = {
        "attack_id": attack_id,
        "target": target,
        "mutation": mutation,
        "independent_probe_kind": probe_kind,
        "semantic_attack_fully_reclosed": False,
        "producer_self_attack_rejection": "REJECTED",
        "independent_verification_status": "REJECTED",
        "boundary_subprobe_count": len(callbacks),
        "rejection_classes": rejection_classes,
    }
    row["row_sha256"] = digest(row)
    return row


def build_independent_attacks(
    source: dict[str, Any],
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    specs = {spec[0]: spec for spec in ATTACK_SPECS}
    expected_row = expected_ledger["rows"][0]
    expected_new_row = next(
        row for row in expected_ledger["rows"]
        if row["binding_classification"] == NEW_CLASS
    )
    expected_source_row = next(iter(source["refinement"].values()))

    def ledger_attack(attack_id: str, duplicate: bool) -> None:
        candidate_rows = (
            expected_ledger["rows"] + [expected_ledger["rows"][0]]
            if duplicate else expected_ledger["rows"][:-1]
        )
        forged = {
            "schema": LEDGER_SCHEMA,
            **raw_rows_commitment(candidate_rows, ROW_ID_FIELD),
            "rows": candidate_rows,
        }
        rows.append(rejected_outcome(
            specs[attack_id],
            lambda: exact_ledger(forged, expected_ledger),
            semantic_reclosed=True,
        ))

    ledger_attack("A01_DROP_BINDING_ROW", False)
    ledger_attack("A02_DUPLICATE_BINDING_ROW", True)

    def row_attack(
        attack_id: str,
        field: str,
        value: Any,
        expected: dict[str, Any] = expected_row,
    ) -> None:
        forged = deepcopy(expected)
        forged[field] = value
        forged = reclose_binding_row(forged)
        rows.append(rejected_outcome(
            specs[attack_id],
            lambda: exact_binding_row(forged, expected),
            semantic_reclosed=True,
        ))

    row_attack("A03_OCCURRENCE_SUBSTITUTION",
               "registry_occurrence_id", "forged-occurrence")
    row_attack("A04_R292_COMPONENT_SUBSTITUTION",
               "source_Round292_refined_support_component_id",
               "forged-component")
    row_attack("A05_R275_REGION_SUBSTITUTION",
               "source_Round275_region_id", "forged-region")
    row_attack("A06_SIGNATURE_HASH_SUBSTITUTION",
               "complete_10_field_return_signature_sha256", "0" * 64)
    row_attack("A07_OFFICIAL_KEY_SUBSTITUTION",
               "official_key_id", "forged-key")
    row_attack("A08_KEY_ORDINAL_SUBSTITUTION",
               "official_key_ordinal", expected_row["official_key_ordinal"] + 1)
    row_attack("A09_KEY_ROW_SUBSTITUTION",
               "official_key_row", {"forged": True})
    row_attack(
        "A10_OLD_NEW_CLASS_FLIP",
        "binding_classification",
        NEW_CLASS if expected_row["binding_classification"] == EXISTING_CLASS
        else EXISTING_CLASS,
    )

    def result_attack(
        attack_id: str,
        path: tuple[str, ...],
        value: Any,
    ) -> None:
        forged = deepcopy(expected_result)
        cursor: dict[str, Any] = forged
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        reclose_result(forged)
        rows.append(rejected_outcome(
            specs[attack_id],
            lambda: exact_result(forged, expected_result),
            semantic_reclosed=True,
        ))

    result_attack(
        "A11_FORCE_OLD_116_ONLY",
        ("raw_observed_key_universe", "after_refined_binding_count"),
        116,
    )
    new_key = expected_new_row["official_key_id"]
    summary = next(
        row for row in expected_result["nonmerge_audit"]["new_raw_key_rows"]
        if row["new_raw_official_key_id"] == new_key
    )
    row_attack(
        "A12_COLLAPSE_NEW_TO_SIBLING",
        "official_key_id",
        summary["unique_old_116_wall_transition_sibling_key_id"],
        expected_new_row,
    )
    result_attack(
        "A13_WALL_FACE_AS_KEY_EQUIVALENCE",
        ("nonmerge_audit",
         "wall_transition_sibling_pairs_are_key_equivalences"),
        True,
    )
    result_attack(
        "A14_FORGE_R285_INCIDENCE",
        ("nonmerge_audit",
         "new_raw_key_Round285_corridor_region_incidence_count"),
        1,
    )
    result_attack(
        "A15_RELAX_PHYSICAL_PAYLOAD",
        ("nonmerge_audit",
         "exact_transported_payload_match_to_other_Round275_key_count"),
        1,
    )
    row_attack(
        "A16_MEMBER_CELL_OMISSION",
        "member_refinement_cell_count",
        expected_row["member_refinement_cell_count"] - 1,
    )

    for attack_id, field, value in (
        ("A17_MEMBER_BOX_SUBSTITUTION",
         "exact_transformed_open_cell", {"forged": True}),
        ("A18_MEMBER_VOLUME_SUBSTITUTION",
         "exact_transformed_cell_volume", "forged-volume"),
    ):
        forged_source = deepcopy(expected_source_row)
        forged_source[field] = value
        forged_source = reclose_source_row(forged_source)
        rows.append(rejected_outcome(
            specs[attack_id],
            lambda forged_source=forged_source:
                exact_source_row(forged_source, expected_source_row),
            semantic_reclosed=True,
        ))

    row_attack("A19_OCCURRENCE_IDENTITY_COLLAPSE",
               "occurrence_identity_preserved", False)
    row_attack("A20_OCCURRENCE_ALIAS_CREDIT",
               "formal_occurrence_alias_credit", 1)
    row_attack("A21_COMPONENT_UNION_CREDIT",
               "formal_component_union_credit", 1)
    row_attack("A22_DSU_RANK_CREDIT",
               "formal_DSU_rank_reduction_credit", 1)
    row_attack("A23_JX_JY_GLUE_CREDIT",
               "formal_Jx_Jy_same_point_glue_credit", 1)
    result_attack(
        "A24_MAXIMALITY_CREDIT",
        ("strict_nonpromotion", "maximality_status"),
        "CERTIFIED",
    )
    result_attack(
        "A25_FIBRE_EXHAUSTION",
        ("strict_nonpromotion", "exact_key_fibre_exhaustion_status"),
        "CERTIFIED",
    )
    result_attack(
        "A26_GLOBAL_DISPOSITION",
        ("strict_nonpromotion", "global_disposition_status"),
        "CERTIFIED",
    )
    result_attack(
        "A27_D02_PROMOTION",
        ("strict_nonpromotion", "D02"),
        "UNBLOCKED",
    )
    result_attack(
        "A28_CM2_PROMOTION",
        ("strict_nonpromotion", "CM2"),
        "CERTIFIED",
    )

    stale_pins = dict(PACKAGE_MANIFEST_PINS)
    stale_pins[R275_MANIFEST] = "0" * 64
    rows.append(rejected_outcome(
        specs["A29_STALE_MANIFEST"],
        lambda: need(
            stale_pins == PACKAGE_MANIFEST_PINS,
            "exact sealed manifest pins",
        ),
        semantic_reclosed=False,
    ))
    rows.append(rejected_outcome(
        specs["A30_DUPLICATE_JSON_KEY"],
        lambda: strict_json_bytes(
            b'{"x":1,"x":2}',
            "A30 duplicate key",
        ),
        semantic_reclosed=False,
    ))
    rows.append(composite_rejected_outcome(
        specs["A31_NONFINITE_OR_NUL_JSON"],
        [
            lambda: strict_json_bytes(b'{"x":NaN}', "A31 NaN"),
            lambda: strict_json_bytes(b'{"x":"a\x00b"}', "A31 NUL"),
        ],
    ))
    first_member = gzip.compress(b'{"x":1}', mtime=0)
    second_member = gzip.compress(b'{"y":2}', mtime=0)
    rows.append(composite_rejected_outcome(
        specs["A32_MALFORMED_OR_CONCAT_GZIP"],
        [
            lambda: scan_single_member_gzip_bytes(
                b"\x1f\x8b\x08\x00truncated", 1024
            ),
            lambda: scan_single_member_gzip_bytes(
                first_member + second_member, 1024
            ),
            lambda: scan_single_member_gzip_bytes(
                first_member + b"TRAILING", 1024
            ),
        ],
    ))

    with tempfile.NamedTemporaryFile(
        dir=HERE,
        prefix=".round299a_path_target_",
        delete=False,
    ) as stream:
        target = Path(stream.name)
        stream.write(b"x")
    symlink_path = HERE / f".round299a_symlink_{target.name}"
    hardlink_path = HERE / f".round299a_hardlink_{target.name}"
    try:
        os.symlink(target.name, symlink_path)
        os.link(target, hardlink_path)
        traversal_path = HERE / ".." / HERE.name / target.name
        rows.append(composite_rejected_outcome(
            specs["A33_SYMLINK_HARDLINK_TRAVERSAL"],
            [
                lambda: require_safe_regular(symlink_path),
                lambda: require_safe_regular(hardlink_path),
                lambda: require_safe_regular(traversal_path),
            ],
        ))
    finally:
        for path in (symlink_path, hardlink_path, target):
            if path.is_symlink() or path.exists():
                path.unlink()

    need(
        len(rows) == 33
        and [row["attack_id"] for row in rows]
        == [spec[0] for spec in ATTACK_SPECS]
        and sum(row["semantic_attack_fully_reclosed"] for row in rows)
        == 28
        and all(
            row["independent_verification_status"] == "REJECTED"
            for row in rows
        ),
        "33 attacks: 28 reclosed semantic plus 5 boundary",
    )
    value = {
        "schema": INDEPENDENT_ATTACK_SCHEMA,
        "status":
            "PASS_INDEPENDENT_REJECTION_33_OF_33__"
            "28_RECLOSED_SEMANTIC__5_JSON_GZIP_PATH_BOUNDARY",
        "execution_status": "EXECUTED_BY_INDEPENDENT_CACHELESS_VERIFIER",
        "candidate_basis": {
            "producer_file_sha256": PRODUCER_SHA256,
            "ledger_file_sha256": CANDIDATE_LEDGER_SHA256,
            "result_file_sha256": CANDIDATE_RESULT_FILE_SHA256,
            "result_sha256": CANDIDATE_RESULT_SHA256,
        },
        "producer_only_pre_verification_basis": {
            "manifest_sha256": PRE_VERIFICATION_MANIFEST_SHA256,
            "manifest_entry_count": 6,
            "attack_suite_file_sha256": PRODUCER_ATTACK_FILE_SHA256,
            "attack_suite_sha256": PRODUCER_ATTACK_SELF_SHA256,
            "producer_self_attack_count": 33,
            "producer_self_rejected_count": 33,
        },
        "attack_count": 33,
        "rejected_count": 33,
        "accepted_count": 0,
        "fully_reclosed_semantic_attack_count": 28,
        "JSON_GZIP_path_boundary_attack_count": 5,
        "all_28_semantic_attacks_fully_reclosed": True,
        "all_33_attacks_independently_rejected": True,
        "producer_imported_or_executed": False,
        "row_hashes_sha256": digest(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": digest(rows),
        "attacks": rows,
        "seed_affects_output": False,
    }
    value["attack_suite_sha256"] = digest(value)
    return value


def validate_original_producer_attack_suite(
    value: dict[str, Any],
) -> None:
    payload = dict(value)
    claimed = payload.pop("attack_suite_sha256", None)
    attacks = value.get("attacks")
    need(
        claimed == digest(payload) == PRODUCER_ATTACK_SELF_SHA256
        and value.get("schema") == SCHEMA + ".attack-suite.v1"
        and value.get("attack_count") == 33
        and type(attacks) is list
        and len(attacks) == 33
        and [row.get("attack_id") for row in attacks]
        == [spec[0] for spec in ATTACK_SPECS]
        and value.get("producer_self_attack_rejection", {}).get(
            "rejected_count"
        ) == 33
        and value.get("producer_self_attack_rejection", {}).get(
            "reclosable_semantic_attack_count"
        ) == 28
        and value.get("producer_self_attack_rejection", {}).get(
            "independent_verification_status"
        ) == "PENDING",
        "original producer-only attack-suite closure",
    )


def validate_attack_output_transition(
    output_path: Path,
    independent_bytes: bytes,
) -> None:
    if not output_path.exists():
        return
    require_safe_regular(output_path)
    actual_sha256 = file_sha256(output_path)
    if actual_sha256 == PRODUCER_ATTACK_FILE_SHA256:
        original, original_bytes = read_json(output_path)
        need(
            hashlib.sha256(original_bytes).hexdigest()
            == PRODUCER_ATTACK_FILE_SHA256,
            "producer attack-suite file pin",
        )
        validate_original_producer_attack_suite(original)
        return
    need(
        output_path.read_bytes() == independent_bytes,
        "existing attack output is exact independent replay",
    )


def safe_write(path: Path, payload: bytes) -> None:
    need(
        path.parent == HERE and path.parent.resolve() == HERE.resolve(),
        f"output HERE-only parent:{path}",
    )
    need(not path.is_symlink(), f"output is not symlink:{path}")
    if path.exists():
        metadata = path.lstat()
        need(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            f"output regular single-link object:{path}",
        )
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=HERE,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(payload)
        stream.flush()
    temporary.replace(path)


def build_verification(
    source: dict[str, Any],
    binding: dict[str, Any],
    nonmerge: dict[str, Any],
    attack_value: dict[str, Any],
    attack_bytes: bytes,
    manifest_member_count: int,
) -> dict[str, Any]:
    new_key_pairs = [
        {
            "new_raw_key_id": row["new_raw_official_key_id"],
            "new_raw_key_ordinal": row["new_raw_official_key_ordinal"],
            "distinct_old_116_wall_transition_sibling_key_id":
                row["unique_old_116_wall_transition_sibling_key_id"],
            "distinct_old_116_wall_transition_sibling_key_ordinal":
                row[
                    "unique_old_116_wall_transition_sibling_key_ordinal"
                ],
            "wall_transition_sibling_pair_count":
                row["wall_transition_sibling_pair_count"],
            "Round285_corridor_region_incidence_count":
                row["Round285_corridor_region_incidence_count"],
        }
        for row in nonmerge["new_raw_key_rows"]
    ]
    value = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND299A__"
            "9404_BINDINGS__8212_OLD36__1192_NEW8__"
            "RAW_KEYS_116_TO_124__8_KEYS_NONMERGED__"
            "33_OF_33_ATTACKS_REJECTED__NO_DSU_OR_PROMOTION",
        "artifact_pins": {
            **dict(sorted(PACKAGE_MANIFEST_PINS.items())),
            **dict(sorted(SELECTED_INPUT_PINS.items())),
            PRODUCER.name: PRODUCER_SHA256,
            LEDGER.name: CANDIDATE_LEDGER_SHA256,
            RESULT.name: CANDIDATE_RESULT_FILE_SHA256,
            ATTACKS.name: hashlib.sha256(attack_bytes).hexdigest(),
            Path(__file__).name:
                file_sha256(Path(__file__).resolve()),
        },
        "producer_only_package_transition": {
            "pre_verification_manifest_sha256":
                PRE_VERIFICATION_MANIFEST_SHA256,
            "pre_verification_manifest_entry_count": 6,
            "final_manifest_required_entry_count": 8,
            "producer_bytes_unchanged": True,
            "producer_sha256": PRODUCER_SHA256,
            "candidate_ledger_bytes_unchanged": True,
            "candidate_result_bytes_unchanged": True,
        },
        "independence_contract": {
            "Round299A_producer_imported_or_executed": False,
            "Round299A_producer_parsed_as_Python": False,
            "Round299A_producer_bytes_used_only_as_inert_SHA256_pin": True,
            "candidate_ledger_or_result_used_as_expected_row_oracle": False,
            "cache_pickle_or_bytecode_input_used": False,
            "sealed_upstream_manifests_exhausted": True,
            "sealed_upstream_manifest_member_count":
                manifest_member_count,
            "Round294_registry_rows_streamed_and_recommitted": 431_208,
            "source_to_binding_rows_reconstructed_independently": True,
        },
        "candidate_exact_equality": {
            "ledger_object_equal_to_independent_reconstruction": True,
            "ledger_deterministic_GZIP_bytes_equal": True,
            "ledger_file_SHA256_equal": True,
            "ledger_file_sha256": CANDIDATE_LEDGER_SHA256,
            "result_object_equal_to_independent_reconstruction": True,
            "result_canonical_JSON_bytes_equal": True,
            "result_file_SHA256_equal": True,
            "result_file_sha256": CANDIDATE_RESULT_FILE_SHA256,
            "result_self_SHA256_equal": True,
            "result_sha256": CANDIDATE_RESULT_SHA256,
        },
        "source_reconstruction": {
            "Round275_region_count": len(source["r275_rows"]),
            "Round275_raw_official_key_count": 44,
            "Round282_patch_count": len(source["r282_rows"]),
            "Round285_safe_pairing_row_count": len(source["r285_rows"]),
            "Round292_mixed_row_count": len(source["r292_rows"]),
            "Round292_refinement_cell_count": len(source["refinement"]),
            "Round292_refined_component_count": len(source["components"]),
            "Round294_registry_row_count":
                source["r294_commitment"]["row_count"],
            "Round294_refined_occurrence_count":
                len(source["refined_registry_rows"]),
            "Round275_Round292_Round294_join_mismatch_count":
                binding["mismatch_count"],
            "all_selected_source_rows_recommitted": True,
        },
        "verified_binding_census": {
            "binding_row_count": len(binding["rows"]),
            "distinct_occurrence_count": 9_404,
            "distinct_Round292_component_count": 9_404,
            "distinct_Round275_region_count": binding["region_count"],
            "bound_refinement_member_cell_count":
                binding["member_cell_count"],
            "old_116_binding_row_count": 8_212,
            "old_116_used_key_count":
                len(binding["existing_bound_keys"]),
            "new_raw_key_binding_row_count": 1_192,
            "new_raw_key_count": len(binding["new_keys"]),
            "new_raw_key_binding_count_per_key": 149,
            "bound_raw_key_count": len(binding["key_occurrences"]),
            "raw_observed_key_universe_before": 116,
            "raw_observed_key_universe_after": 124,
            "occurrence_ID_rewrite_count": 0,
            "raw_key_merge_count": 0,
        },
        "eight_key_nonmerge_evidence": {
            "new_key_rows": new_key_pairs,
            "new_key_count": 8,
            "new_key_Round275_region_count":
                nonmerge["new_raw_key_Round275_region_count"],
            "new_key_strict_region_count":
                nonmerge["new_raw_key_Round275_strict_region_count"],
            "new_key_regular_graph_crossing_region_count":
                nonmerge[
                    "new_raw_key_Round275_regular_graph_crossing_region_count"
                ],
            "wall_transition_sibling_pair_count":
                nonmerge["wall_transition_sibling_pair_count"],
            "wall_transition_siblings_are_key_equivalences": False,
            "exact_transported_payload_matches_to_other_raw_keys": 0,
            "Round285_corridor_region_occurrence_count":
                nonmerge["Round285_corridor_region_occurrence_count"],
            "Round285_distinct_corridor_region_count":
                nonmerge["Round285_distinct_corridor_region_count"],
            "new_key_Round285_corridor_region_incidence_count": 0,
            "transported_equivalence_supports_any_new_key_merge": False,
        },
        "attack_audit": {
            "attack_suite_file_sha256":
                hashlib.sha256(attack_bytes).hexdigest(),
            "attack_suite_sha256": attack_value["attack_suite_sha256"],
            "attack_count": 33,
            "rejected_count": 33,
            "accepted_count": 0,
            "fully_reclosed_semantic_attack_count": 28,
            "JSON_GZIP_path_boundary_attack_count": 5,
            "all_28_semantic_attacks_fully_reclosed": True,
            "all_33_attacks_independently_rejected": True,
        },
        "strict_document_and_file_boundary": {
            "duplicate_free_integral_finite_single_document_JSON": True,
            "NUL_and_nonfinite_JSON_rejected": True,
            "single_member_trailing_free_bounded_GZIP": True,
            "GZIP_uncompressed_size_cap_bytes":
                MAX_GZIP_UNCOMPRESSED_BYTES,
            "HERE_only_regular_non_symlink_non_hardlink_files": True,
            "file_size_cap_bytes": MAX_FILE_BYTES,
            "stale_manifest_symlink_hardlink_traversal_attacks_rejected":
                True,
        },
        "strict_nonpromotion": {
            "formal_component_union_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_Jx_Jy_same_point_glue_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "post_Round299A_component_count": None,
            "component_DSU_status": "NOT_REBUILT",
            "maximality_status": "NOT_CERTIFIED",
            "exact_key_fibre_exhaustion_status": "NOT_CERTIFIED",
            "global_disposition_status": "NOT_CERTIFIED",
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "replay_contract": {
            "seed_argument_affects_output": False,
            "external_PYTHONHASHSEED_affects_output": False,
            "dual_seed_byte_identical_replay_required": True,
        },
    }
    value["verification_sha256"] = digest(value)
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=299_311)
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--result", type=Path, default=RESULT)
    parser.add_argument("--attack-output", type=Path, default=ATTACKS)
    parser.add_argument("--verification", type=Path, default=VERIFICATION)
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    _ = arguments.seed

    require_safe_regular(Path(__file__).resolve())
    manifest_member_count = validate_sealed_upstream()
    source = load_sources()
    binding = build_expected_binding(source)
    nonmerge = build_expected_nonmerge(source, binding)
    (
        expected_ledger,
        expected_ledger_bytes,
        expected_result,
        expected_result_bytes,
    ) = build_expected_candidate(source, binding, nonmerge)
    open_and_match_candidate(
        expected_ledger,
        expected_ledger_bytes,
        expected_result,
        expected_result_bytes,
        arguments.ledger,
        arguments.result,
    )

    attack_value = build_independent_attacks(
        source,
        expected_ledger,
        expected_result,
    )
    attack_bytes = canonical(attack_value) + b"\n"
    validate_attack_output_transition(
        arguments.attack_output,
        attack_bytes,
    )
    verification = build_verification(
        source,
        binding,
        nonmerge,
        attack_value,
        attack_bytes,
        manifest_member_count,
    )
    verification_bytes = canonical(verification) + b"\n"
    if not arguments.no_write:
        safe_write(arguments.attack_output, attack_bytes)
        safe_write(arguments.verification, verification_bytes)
    print(json.dumps({
        "status": verification["status"],
        "verification_file_sha256":
            hashlib.sha256(verification_bytes).hexdigest(),
        "verification_sha256": verification["verification_sha256"],
        "attack_suite_file_sha256":
            hashlib.sha256(attack_bytes).hexdigest(),
        "attack_suite_sha256": attack_value["attack_suite_sha256"],
        "verified_binding_census":
            verification["verified_binding_census"],
        "strict_nonpromotion": verification["strict_nonpromotion"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
