#!/usr/bin/env python3
"""Independent cacheless verifier for Round300-D.

The producer is neither imported, executed, nor parsed.  Its bytes are an
inert pinned artifact.  This verifier independently reopens the sealed
Round266 member/root tables, the complete Round294 registry, the complete
Round295-A lower-physical-witness ledger, and the complete Round299-A refined
key binding.  It rebuilds the canonical two-target *incidence-edge* ledger.

An incidence edge is intentionally not a topological occurrence-union edge.
It is ineligible for component DSU use until a separate included-stratum plus
two-attachment/corridor gluing lemma is pinned.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import copy
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
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion"
)
PRODUCER = HERE / f"{PREFIX}.py"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

SCHEMA = (
    "cm2.round300d.source-g-lower-physical-witness-"
    "component-edge-promotion.v1"
)
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ATTACK_SCHEMA = SCHEMA + ".independent-attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification.v1"
EDGE_ID = "Round300D_lower_physical_witness_incidence_edge_row_id"
EXCLUSION_ID = "Round300D_single_target_assignment_exclusion_row_id"

# Filled only after the producer and its two candidate artifacts are stable.
PRODUCER_SHA256 = (
    "56e414eba093fb0ceb9a78895b94b63ccff3beaf590b05d4e969d43d767ac333"
)
LEDGER_SHA256 = (
    "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7"
)
RESULT_SHA256 = (
    "59b7e788ed217ceb590a3e2125cc13aefbf447af236315ea607f4f631cb29c84"
)
RESULT_SELF_SHA256 = (
    "17b9d2989f7616b74db5a11adda13eff971f43e737211bb488a8a2a7db4c156e"
)

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
FAMILY = {
    "ROUND182_GRAPH_SHEET_LEAF": "GRAPH",
    "ROUND179_NEGATIVE_T0_SHADOW_PATCH": "NEG_T0",
    "ROUND182_TRANSVERSE_1D_LINE": "TRANSVERSE",
    "ROUND179_POSITIVE_T0_RETAINED_OWNER": "POS_T0",
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def chunks(value: Any) -> Iterable[bytes]:
    for token in ENCODER.iterencode(value):
        yield token.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(chunks(value))


def sha_object(value: Any) -> str:
    state = hashlib.sha256()
    for token in chunks(value):
        state.update(token)
    return state.hexdigest()


def sha_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def safe_bytes(path: Path, maximum: int = 3_000_000_000) -> bytes:
    require(path.parent.resolve() == HERE.resolve(), "HERE path")
    require(path.exists() and not path.is_symlink(), "regular path")
    info = os.lstat(path)
    require(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "single-link regular bounded file:" + path.name,
    )
    return path.read_bytes()


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(
        raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "strict bytes:" + label,
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in answer, "duplicate key:" + label + ":" + key)
            answer[key] = value
        return answer

    def no_float(token: str) -> Any:
        raise VerificationError("noninteger JSON:" + label + ":" + token)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=no_float,
            parse_constant=no_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("invalid JSON:" + label) from error
    require(type(value) is dict, "JSON top object:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    return strict_json(safe_bytes(HERE / name), name)


def check_closed(row: dict[str, Any], label: str) -> None:
    require(type(row) is dict and type(row.get("row_sha256")) is str,
            label + ":closed row")
    payload = dict(row)
    claimed = payload.pop("row_sha256")
    require(claimed == sha_object(payload), label + ":row closure")


def close_row(
    prefix: str,
    domain: str,
    id_field: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    row = {id_field: prefix + sha_object([domain, payload]), **payload}
    row["row_sha256"] = sha_object(row)
    return row


class SequenceHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for token in chunks(value):
            self.state.update(token)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def commitment(rows: list[dict[str, Any]], id_field: str) -> dict[str, Any]:
    ids = [row[id_field] for row in rows]
    require(len(ids) == len(set(ids)), "unique expected row IDs")
    return {
        "row_count": len(rows),
        "row_ids_sha256": sha_object(ids),
        "row_hashes_sha256": sha_object(
            [row["row_sha256"] for row in rows]
        ),
        "rows_sha256": sha_object(rows),
    }


def iter_rows(
    stream: TextIO,
    marker: str = '"rows":[',
    initial: str = "",
) -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        require(bool(block), "missing array marker:" + marker)
        buffer += block
    buffer = buffer.split(marker, 1)[1]

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        answer: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in answer, "stream duplicate key:" + key)
            answer[key] = value
        return answer

    decoder = json.JSONDecoder(
        object_pairs_hook=unique,
        parse_float=lambda token: (_ for _ in ()).throw(
            VerificationError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            VerificationError("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            require(bool(block), "truncated streamed array")
            buffer = block
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
                block = stream.read(1 << 20)
                require(bool(block), "truncated streamed row")
                buffer += block
        require(type(value) is dict, "stream row object")
        yield value
        buffer = buffer[end:]


def stream_gzip(
    name: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
) -> None:
    rows_state = SequenceHash()
    ids_state = SequenceHash()
    hashes_state = SequenceHash()
    occurrence_state = (
        SequenceHash() if "occurrence_ids_sha256" in expected else None
    )
    with gzip.open(HERE / name, "rt", encoding="utf-8", newline="") as stream:
        for row in iter_rows(stream):
            check_closed(row, name)
            rows_state.add(row)
            ids_state.add(row[id_field])
            hashes_state.add(row["row_sha256"])
            if occurrence_state is not None:
                occurrence_state.add(row["registry_occurrence_id"])
            visit(row)
    actual = {
        "row_count": rows_state.count,
        "row_ids_sha256": ids_state.finish(),
        "row_hashes_sha256": hashes_state.finish(),
        "rows_sha256": rows_state.finish(),
    }
    if occurrence_state is not None:
        actual["occurrence_ids_sha256"] = occurrence_state.finish()
    require(actual == expected, "sealed gzip commitment:" + name)


def stream_plain_table(
    name: str,
    table: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
) -> None:
    marker = '"' + table + '":'
    tail = ""
    with (HERE / name).open("rt", encoding="utf-8", newline="") as stream:
        while True:
            block = stream.read(1 << 20)
            require(bool(block), "missing plain table:" + table)
            joined = tail + block
            if marker in joined:
                initial = joined.split(marker, 1)[1]
                break
            tail = joined[-len(marker):]
        rows_state = SequenceHash()
        ids_state = SequenceHash()
        hashes_state = SequenceHash()
        for row in iter_rows(stream, initial=initial):
            check_closed(row, "R266:" + table)
            rows_state.add(row)
            ids_state.add(row[id_field])
            hashes_state.add(row["row_sha256"])
            visit(row)
    require(
        {
            "row_count": rows_state.count,
            "row_ids_sha256": ids_state.finish(),
            "row_hashes_sha256": hashes_state.finish(),
            "rows_sha256": rows_state.finish(),
        } == expected,
        "sealed plain-table commitment:" + table,
    )


def parse_manifest_bytes(raw: bytes, name: str) -> dict[str, str]:
    answer: dict[str, str] = {}
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise VerificationError("manifest ASCII:" + name) from error
    for line in text.splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        require(match is not None, "manifest syntax:" + name)
        value, member = match.groups()
        require(Path(member).name == member and member not in answer,
                "manifest member:" + name)
        answer[member] = value
    require(bool(answer), "nonempty manifest:" + name)
    return answer


def manifest_entries(name: str) -> dict[str, str]:
    return parse_manifest_bytes(safe_bytes(HERE / name, 200_000), name)


def validate_boundary() -> None:
    for name, value in MANIFEST_PINS.items():
        require(PIN_RE.fullmatch(value) is not None, "manifest pin syntax")
        require(sha_file(HERE / name) == value, "manifest byte pin:" + name)
    for name, value in INPUT_PINS.items():
        require(PIN_RE.fullmatch(value) is not None, "input pin syntax")
        require(sha_file(HERE / name) == value, "input byte pin:" + name)
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
    for manifest, members in selections.items():
        entries = manifest_entries(manifest)
        for member in members:
            require(
                entries.get(member) == INPUT_PINS[member],
                "selected manifest member:" + manifest + ":" + member,
            )
    round266_verification = read_json(R266_VERIFICATION)
    require(
        round266_verification["status"].startswith("PASS"),
        "Round266 independent verification",
    )


def check_result_self(document: dict[str, Any], label: str) -> None:
    payload = dict(document)
    claimed = payload.pop("result_sha256", None)
    require(
        type(claimed) is str and claimed == sha_object(payload),
        "result self closure:" + label,
    )


def strict_gzip(raw: bytes, label: str) -> bytes:
    require(len(raw) >= 18 and raw[:3] == b"\x1f\x8b\x08", label + ":gzip")
    require(raw[4:8] == b"\x00\x00\x00\x00", label + ":mtime zero")
    decoder = zlib.decompressobj(16 + zlib.MAX_WBITS)
    for offset in range(0, len(raw), 1 << 16):
        decoder.decompress(raw[offset:offset + (1 << 16)])
    decoder.flush()
    require(decoder.eof and decoder.unused_data == b"", label + ":single member")
    return b""


def deterministic_gzip(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", fileobj=buffer, mode="wb", mtime=0, compresslevel=9
    ) as stream:
        for token in chunks(value):
            stream.write(token)
    return buffer.getvalue()


def first_r295a_pass() -> tuple[set[str], dict[str, Any]]:
    sealed_result = read_json(R295A_RESULT)
    check_result_self(sealed_result, "Round295A")
    require(
        sealed_result["physical_witness_incidence_binding_ledger"][
            "file_sha256"
        ] == INPUT_PINS[R295A_INCIDENCE],
        "Round295A attached ledger",
    )
    sealed_verification = read_json(R295A_VERIFICATION)
    require(
        sealed_verification["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND295A"
        ),
        "Round295A independent verification",
    )

    all_targets: set[str] = set()
    single_targets: set[str] = set()
    paired_targets: set[str] = set()
    ids_seen: set[str] = set()
    arities: Counter[int] = Counter()
    kinds: Counter[str] = Counter()
    supports: Counter[str] = Counter()

    def inspect(row: dict[str, Any]) -> None:
        row_id = row["Round295A_R291_physical_incidence_binding_row_id"]
        require(row_id not in ids_seen, "Round295A unique row")
        ids_seen.add(row_id)
        count = row["target_Round294_registry_reference_count"]
        targets = row["target_Round294_registry_occurrence_ids"]
        require(
            count in {1, 2}
            and type(targets) is list
            and len(targets) == count == len(set(targets)),
            "Round295A exact arity",
        )
        arities[count] += 1
        all_targets.update(targets)
        (single_targets if count == 1 else paired_targets).update(targets)
        kinds[row["witness_kind"]] += 1
        supports[row["canonical_support_kind"]] += 1
        require(
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
            "Round295A narrow physical-incidence scope",
        )

    stream_gzip(
        R295A_INCIDENCE,
        "Round295A_R291_physical_incidence_binding_row_id",
        R295A_COMMITMENT,
        inspect,
    )
    require(
        arities == {1: 1_600, 2: 111_852}
        and len(all_targets) == 224_168
        and len(single_targets) == 1_216
        and len(paired_targets) == 223_048
        and len(single_targets & paired_targets) == 96
        and len(single_targets - paired_targets) == 1_120,
        "Round295A complete arity/target census",
    )
    return all_targets, {
        "reference_count_histogram": {
            str(key): value for key, value in sorted(arities.items())
        },
        "complete_witness_kind_histogram": dict(sorted(kinds.items())),
        "complete_support_kind_histogram": dict(sorted(supports.items())),
        "single_target_distinct_occurrence_count": len(single_targets),
        "two_target_distinct_occurrence_count": len(paired_targets),
        "single_and_two_target_overlap_occurrence_count":
            len(single_targets & paired_targets),
        "single_target_only_distinct_occurrence_count":
            len(single_targets - paired_targets),
    }


def registry_and_final_keys(
    targets: set[str],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    set[str],
    dict[str, int],
]:
    result294 = read_json(R294_RESULT)
    check_result_self(result294, "Round294")
    require(
        result294["registry_ledger"]["file_sha256"]
        == INPUT_PINS[R294_REGISTRY],
        "Round294 attached registry",
    )
    verification294 = read_json(R294_VERIFICATION)
    require(
        verification294["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND294"
        ),
        "Round294 independent verification",
    )

    selected: dict[str, dict[str, Any]] = {}
    refined_sources: dict[str, tuple[str, str]] = {}
    all_occurrences: set[str] = set()
    kind_census: Counter[str] = Counter()
    old_keys: set[str] = set()

    def inspect294(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        require(occurrence not in all_occurrences, "Round294 unique occurrence")
        all_occurrences.add(occurrence)
        kind = row["registry_entry_kind"]
        kind_census[kind] += 1
        if kind == REFINED:
            require(
                row["official_key_id"] is None
                and row["official_key_ordinal"] is None,
                "Round294 refined key null",
            )
            refined_sources[occurrence] = (
                row["Round294_occurrence_registry_row_id"],
                row["row_sha256"],
            )
        else:
            require(
                type(row["official_key_id"]) is str
                and type(row["official_key_ordinal"]) is int,
                "Round294 old key present",
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

    stream_gzip(
        R294_REGISTRY,
        "Round294_occurrence_registry_row_id",
        R294_COMMITMENT,
        inspect294,
    )
    require(
        kind_census == {
            PRESERVED: 126_468,
            R288: 295_336,
            REFINED: 9_404,
        }
        and set(selected) == targets
        and len(old_keys) == 116,
        "Round294 full registry census and coverage",
    )

    result299 = read_json(R299A_RESULT)
    check_result_self(result299, "Round299A")
    require(
        result299["ledger"]["file_sha256"] == INPUT_PINS[R299A_LEDGER]
        and result299["raw_observed_key_universe"][
            "after_refined_binding_count"
        ] == 124,
        "Round299A attached 124-key result",
    )
    verification299 = read_json(R299A_VERIFICATION)
    require(
        verification299["status"].startswith(
            "PASS_INDEPENDENT_CACHELESS_ROUND299A"
        ),
        "Round299A independent verification",
    )

    bindings: dict[str, dict[str, Any]] = {}
    final_keys = set(old_keys)

    def inspect299(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        source = refined_sources.get(occurrence)
        require(
            source is not None
            and occurrence not in bindings
            and row["source_Round294_occurrence_registry_row_id"] == source[0]
            and row["source_Round294_occurrence_registry_row_sha256"]
            == source[1]
            and row["append_only_official_key_binding"] is True
            and row["occurrence_identity_preserved"] is True
            and row[
                "formal_refined_occurrence_official_key_binding_credit"
            ] == 1
            and row["raw_key_merge_credit"] == 0,
            "Round299A exact append-only binding",
        )
        bindings[occurrence] = {
            "official_key_id": row["official_key_id"],
            "official_key_ordinal": row["official_key_ordinal"],
        }
        final_keys.add(row["official_key_id"])

    stream_gzip(
        R299A_LEDGER,
        "Round299A_refined_occurrence_official_key_binding_row_id",
        R299A_COMMITMENT,
        inspect299,
    )
    require(
        set(bindings) == set(refined_sources)
        and len(bindings) == 9_404
        and len(final_keys) == 124
        and not (targets & set(bindings)),
        "Round299A full append-only key closure",
    )
    return selected, bindings, final_keys, {
        key: kind_census[key] for key in sorted(kind_census)
    }


def round266_links(
    selected: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    preserved = {
        occurrence
        for occurrence, row in selected.items()
        if row["registry_entry_kind"] == PRESERVED
    }
    require(len(preserved) == 1_396, "selected Round266 occurrence count")
    occurrences: dict[str, dict[str, Any]] = {}

    def inspect_occurrence(row: dict[str, Any]) -> None:
        occurrence = row["local_occurrence_row_id"]
        if occurrence in preserved:
            require(occurrence not in occurrences, "R266 occurrence unique")
            occurrences[occurrence] = row

    stream_plain_table(
        R266_CERTIFICATE,
        "formal_post_Round266_expanded_occurrence_frontier_ledger",
        "post_Round266_expanded_occurrence_frontier_row_id",
        R266_OCCURRENCE_COMMITMENT,
        inspect_occurrence,
    )
    require(set(occurrences) == preserved, "R266 occurrence coverage")
    needed_roots = {
        row["post_Round266_quotient_component_id"]
        for row in occurrences.values()
    }
    roots: dict[str, dict[str, Any]] = {}

    def inspect_root(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        if root in needed_roots:
            require(root not in roots, "R266 root unique")
            roots[root] = row

    stream_plain_table(
        R266_CERTIFICATE,
        "formal_post_Round266_component_frontier_ledger",
        "post_Round266_component_frontier_row_id",
        R266_ROOT_COMMITMENT,
        inspect_root,
    )
    require(set(roots) == needed_roots, "R266 root coverage")

    answer: dict[str, dict[str, Any]] = {}
    for occurrence, row in occurrences.items():
        registry = selected[occurrence]
        root = roots[row["post_Round266_quotient_component_id"]]
        require(
            registry["source_row_id"]
            == row["post_Round266_expanded_occurrence_frontier_row_id"]
            and registry["source_row_sha256"] == row["row_sha256"]
            and registry["official_key_id"] == row["official_key_id"]
            == root["official_key_id"]
            and registry["official_key_ordinal"]
            == row["official_key_ordinal"]
            == root["official_key_ordinal"],
            "R266 occurrence/root/official-key join",
        )
        answer[occurrence] = {
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
    return answer


def endpoint(
    occurrence: str,
    selected: dict[str, dict[str, Any]],
    r266: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source = selected[occurrence]
    return {
        "registry_occurrence_id": occurrence,
        "Round294_occurrence_registry_row_id":
            source["Round294_occurrence_registry_row_id"],
        "Round294_occurrence_registry_row_sha256":
            source["Round294_occurrence_registry_row_sha256"],
        "registry_entry_kind": source["registry_entry_kind"],
        "source_occurrence_class": source["source_occurrence_class"],
        "physical_support_chart": source["physical_support_chart"],
        "final_Round299A_official_key_id": source["official_key_id"],
        "final_Round299A_official_key_ordinal":
            source["official_key_ordinal"],
        "complete_10_field_return_signature_sha256":
            source["complete_10_field_return_signature_sha256"],
        "preserved_Round266_provenance": (
            r266[occurrence]
            if source["registry_entry_kind"] == PRESERVED
            else None
        ),
    }


def rebuild_rows(
    selected: dict[str, dict[str, Any]],
    r266: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    exclusions: list[dict[str, Any]] = []
    raw_family: Counter[str] = Counter()
    raw_support: Counter[str] = Counter()
    raw_tranche: Counter[str] = Counter()
    assignment_kind: Counter[str] = Counter()

    with gzip.open(
        HERE / R295A_INCIDENCE, "rt", encoding="utf-8", newline=""
    ) as stream:
        for source in iter_rows(stream):
            check_closed(source, "Round295A reconstruction pass")
            targets = source["target_Round294_registry_occurrence_ids"]
            embedded = source["target_Round294_registry_rows"]
            arity = source["target_Round294_registry_reference_count"]
            require(
                type(embedded) is list
                and len(targets) == len(embedded) == arity,
                "Round295A embedded arity",
            )
            for occurrence, embedded_row in zip(
                targets, embedded, strict=True
            ):
                registry = selected[occurrence]
                require(
                    embedded_row["registry_occurrence_id"] == occurrence
                    and embedded_row["Round294_occurrence_registry_row_id"]
                    == registry["Round294_occurrence_registry_row_id"]
                    and embedded_row[
                        "Round294_occurrence_registry_row_sha256"
                    ] == registry["Round294_occurrence_registry_row_sha256"]
                    and embedded_row["registry_entry_kind"]
                    == registry["registry_entry_kind"]
                    and embedded_row["source_occurrence_class"]
                    == registry["source_occurrence_class"]
                    and embedded_row["physical_support_chart"]
                    == registry["physical_support_chart"]
                    and embedded_row["official_key_id"]
                    == registry["official_key_id"]
                    and embedded_row["official_key_ordinal"]
                    == registry["official_key_ordinal"]
                    and embedded_row[
                        "complete_10_field_return_signature_sha256"
                    ] == registry[
                        "complete_10_field_return_signature_sha256"
                    ],
                    "Round295A embedded/registry exact join",
                )
            witness = {
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
            if arity == 1:
                occurrence = targets[0]
                assignment_kind[source["witness_kind"]] += 1
                payload = {
                    **witness,
                    "target_Round294_registry_occurrence":
                        endpoint(occurrence, selected, r266),
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
                    EXCLUSION_ID,
                    payload,
                ))
                continue

            pair = tuple(sorted(targets))
            require(pair[0] != pair[1], "no two-target self pair")
            grouped[pair].append(witness)
            raw_family[FAMILY[source["witness_kind"]]] += 1
            raw_support[source["canonical_support_kind"]] += 1
            raw_tranche["|".join(sorted(
                selected[item]["registry_entry_kind"] for item in pair
            ))] += 1

    require(
        len(exclusions) == 1_600
        and sum(len(rows) for rows in grouped.values()) == 111_852
        and len(grouped) == 111_524,
        "Round295A exact assignment/edge projection",
    )
    require(
        raw_family == {
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
        }
        and assignment_kind == {
            "ROUND179_NEGATIVE_T0_SHADOW_PATCH": 416,
            "ROUND179_POSITIVE_T0_RETAINED_OWNER": 352,
            "ROUND208_DIRECT_GRAPH_SIDE_REGION": 608,
            "SOURCE_EXACT_T0_SHEET_CELL": 224,
        },
        "Round295A exact witness-kind/support/tranche partition",
    )

    edges: list[dict[str, Any]] = []
    multiplicity: Counter[int] = Counter()
    key_relation: Counter[str] = Counter()
    unique_tranche: Counter[str] = Counter()
    cross_key_primary_family: Counter[str] = Counter()
    cross_key_raw_family: Counter[str] = Counter()
    for pair, source_rows in sorted(grouped.items()):
        source_rows.sort(
            key=lambda row: row[
                "source_Round295A_physical_incidence_binding_row_id"
            ]
        )
        multiplicity[len(source_rows)] += 1
        endpoints = [
            endpoint(occurrence, selected, r266) for occurrence in pair
        ]
        relation = (
            "SAME_OFFICIAL_KEY"
            if endpoints[0]["final_Round299A_official_key_id"]
            == endpoints[1]["final_Round299A_official_key_id"]
            else "CROSS_OFFICIAL_KEY"
        )
        key_relation[relation] += 1
        tranche = "|".join(sorted(
            row["registry_entry_kind"] for row in endpoints
        ))
        unique_tranche[tranche] += 1
        witness_histogram = Counter(
            row["witness_kind"] for row in source_rows
        )
        support_histogram = Counter(
            row["canonical_support_kind"] for row in source_rows
        )
        if relation == "CROSS_OFFICIAL_KEY":
            for kind, count in witness_histogram.items():
                cross_key_raw_family[FAMILY[kind]] += count
            cross_key_primary_family[
                FAMILY[source_rows[0]["witness_kind"]]
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
                for row in source_rows
            ],
            "source_Round295A_physical_incidence_binding_row_sha256s": [
                row[
                    "source_Round295A_physical_incidence_binding_row_sha256"
                ]
                for row in source_rows
            ],
            "source_Round291_local_disposition_row_ids": sorted({
                row["Round291_local_disposition_row_id"]
                for row in source_rows
            }),
            "physical_witness_cell_indices": sorted({
                row["physical_witness_cell_index"] for row in source_rows
            }),
            "source_charts": sorted({
                row["source_chart"] for row in source_rows
            }),
            "witness_multiplicity": len(source_rows),
            "witness_kind_histogram": dict(sorted(witness_histogram.items())),
            "canonical_support_kind_histogram":
                dict(sorted(support_histogram.items())),
            "Round295A_binding_classifications": sorted({
                row["Round295A_binding_classification"]
                for row in source_rows
            }),
            "endpoint_tranche_relation": tranche,
            "official_key_relation": relation,
            "component_connectivity_may_cross_official_key": True,
            "official_key_metadata_is_not_component_purity_constraint": True,
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
        edges.append(close_row(
            "round300d-lower-physical-witness-incidence-edge:",
            "ROUND300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_"
            "WITNESS_INCIDENCE_EDGE_V1",
            EDGE_ID,
            payload,
        ))

    edges.sort(key=lambda row: row[EDGE_ID])
    exclusions.sort(key=lambda row: row[EXCLUSION_ID])
    require(
        multiplicity == {1: 111_380, 2: 56, 3: 32, 4: 16, 5: 40}
        and key_relation == {
            "SAME_OFFICIAL_KEY": 86_308,
            "CROSS_OFFICIAL_KEY": 25_216,
        }
        and unique_tranche == {
            R288 + "|" + R288: 111_332,
            PRESERVED + "|" + PRESERVED: 192,
        }
        and cross_key_primary_family == {
            "GRAPH": 25_119,
            "NEG_T0": 27,
            "POS_T0": 29,
            "TRANSVERSE": 41,
        },
        "canonical incidence-edge census",
    )
    require(
        cross_key_raw_family == {
            "GRAPH": 25_216,
            "NEG_T0": 128,
            "POS_T0": 88,
            "TRANSVERSE": 112,
        },
        "cross-key raw witness census",
    )
    return edges, exclusions, {
        "two_target_raw_witness_kind_family_histogram":
            dict(sorted(raw_family.items())),
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
            dict(sorted(cross_key_primary_family.items())),
        "cross_key_raw_witness_kind_family_histogram":
            dict(sorted(cross_key_raw_family.items())),
        "single_target_assignment_witness_kind_histogram":
            dict(sorted(assignment_kind.items())),
    }


def build_expected() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any]
]:
    validate_boundary()
    targets, r295_census = first_r295a_pass()
    selected, refined, final_keys, registry_kinds = (
        registry_and_final_keys(targets)
    )
    r266 = round266_links(selected)
    edges, exclusions, edge_census = rebuild_rows(selected, r266)
    edge_commitment = commitment(edges, EDGE_ID)
    exclusion_commitment = commitment(exclusions, EXCLUSION_ID)
    ledger = {
        "schema": LEDGER_SCHEMA,
        "status":
            "FORMALLY_PROMOTED_111524_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_"
            "WITNESS_INCIDENCE_EDGES__1600_SINGLE_TARGET_ASSIGNMENT_"
            "EXCLUSIONS__NOT_COMPONENT_DSU_ELIGIBLE",
        "canonical_incidence_edge_row_count": len(edges),
        "canonical_incidence_edge_row_ids_sha256":
            edge_commitment["row_ids_sha256"],
        "canonical_incidence_edge_row_hashes_sha256":
            edge_commitment["row_hashes_sha256"],
        "canonical_incidence_edge_rows_sha256":
            edge_commitment["rows_sha256"],
        "canonical_incidence_edge_rows": edges,
        "single_target_assignment_exclusion_row_count": len(exclusions),
        "single_target_assignment_exclusion_row_ids_sha256":
            exclusion_commitment["row_ids_sha256"],
        "single_target_assignment_exclusion_row_hashes_sha256":
            exclusion_commitment["row_hashes_sha256"],
        "single_target_assignment_exclusion_rows_sha256":
            exclusion_commitment["rows_sha256"],
        "single_target_assignment_exclusion_rows": exclusions,
    }
    result = {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_"
            "INCIDENCE_EDGE_PROMOTION__111524_EDGES__1600_ASSIGNMENT_"
            "EXCLUSIONS__ZERO_COMPONENT_DSU_CREDIT",
        "producer_sha256": PRODUCER_SHA256,
        "seed_affects_output": False,
        "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
        "input_file_pins": dict(sorted(INPUT_PINS.items())),
        "source_reconstruction": {
            "Round266_preserved_target_occurrence_count": len(r266),
            "Round266_component_root_rows_reopened": len({
                row["Round266_quotient_component_id"]
                for row in r266.values()
            }),
            "Round294_registry_kind_histogram": registry_kinds,
            "Round294_target_occurrence_count": len(selected),
            "Round299A_final_raw_official_key_count": len(final_keys),
            "Round299A_refined_binding_count": len(refined),
            "target_occurrence_unkeyed_count": sum(
                row["official_key_id"] is None for row in selected.values()
            ),
            **r295_census,
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
            "canonical_incidence_edge_row_count": len(edges),
            "canonical_incidence_edge_rows_sha256":
                edge_commitment["rows_sha256"],
            "single_target_assignment_exclusion_row_count":
                len(exclusions),
            "single_target_assignment_exclusion_rows_sha256":
                exclusion_commitment["rows_sha256"],
            "file_sha256": LEDGER_SHA256,
        },
        "result_sha256": "",
    }
    payload = dict(result)
    payload.pop("result_sha256")
    result["result_sha256"] = sha_object(payload)
    reconstruction = {
        "complete_Round266_occurrence_rows_streamed": 126_468,
        "complete_Round266_component_root_rows_streamed": 63_224,
        "complete_Round294_registry_rows_streamed": 431_208,
        "complete_Round295A_incidence_rows_streamed_twice": 226_904,
        "complete_Round299A_binding_rows_streamed": 9_404,
        "all_target_occurrence_count": len(selected),
        "two_target_endpoint_occurrence_count":
            r295_census["two_target_distinct_occurrence_count"],
        "canonical_incidence_edge_count": len(edges),
        "assignment_exclusion_count": len(exclusions),
        "same_key_edge_count": 86_308,
        "cross_key_edge_count": 25_216,
        "component_DSU_eligible_edge_count": 0,
        "formal_component_edge_count": 0,
        "formal_component_union_count": 0,
        "formal_DSU_rank_reduction_count": 0,
    }
    return ledger, result, reconstruction


def validate_edge(row: dict[str, Any], expected: dict[str, Any]) -> None:
    check_closed(row, "candidate incidence edge")
    pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
    left = row["left_endpoint"]
    right = row["right_endpoint"]
    require(
        type(pair) is list
        and len(pair) == 2
        and pair == sorted(pair)
        and pair[0] != pair[1]
        and row["self_pair"] is False
        and left["registry_occurrence_id"] == pair[0]
        and right["registry_occurrence_id"] == pair[1],
        "canonical distinct endpoint pair",
    )
    relation = (
        "SAME_OFFICIAL_KEY"
        if left["final_Round299A_official_key_id"]
        == right["final_Round299A_official_key_id"]
        else "CROSS_OFFICIAL_KEY"
    )
    tranche = "|".join(sorted([
        left["registry_entry_kind"], right["registry_entry_kind"]
    ]))
    require(
        relation == row["official_key_relation"]
        and tranche == row["endpoint_tranche_relation"]
        and tranche in {
            R288 + "|" + R288,
            PRESERVED + "|" + PRESERVED,
        },
        "edge key/tranche relation",
    )
    source_ids = row[
        "source_Round295A_physical_incidence_binding_row_ids"
    ]
    source_hashes = row[
        "source_Round295A_physical_incidence_binding_row_sha256s"
    ]
    require(
        type(source_ids) is list
        and source_ids == sorted(source_ids)
        and len(source_ids) == len(set(source_ids))
        == len(source_hashes) == row["witness_multiplicity"]
        and row["witness_multiplicity"] in {1, 2, 3, 4, 5}
        and sum(row["witness_kind_histogram"].values())
        == row["witness_multiplicity"]
        and sum(row["canonical_support_kind_histogram"].values())
        == row["witness_multiplicity"],
        "edge complete witness multiplicity/provenance",
    )
    require(
        row["incidence_edge_semantics"]
        == "CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE"
        and row["shared_lower_witness_incidence_proved"] is True
        and row[
            "all_source_witnesses_exactly_covered_by_named_registry_supports"
        ] is True
        and row["topological_occurrence_union_connectivity_claimed"] is False
        and row["included_stratum_gluing_lemma_pinned"] is False
        and row[
            "two_sided_attachment_or_corridor_gluing_lemma_pinned"
        ] is False
        and row["eligible_for_component_DSU_application"] is False
        and row[
            "formal_canonical_two_target_lower_physical_witness_"
            "incidence_edge_credit"
        ] == 1
        and row["component_connectivity_may_cross_official_key"] is True
        and row[
            "official_key_metadata_is_not_component_purity_constraint"
        ] is True
        and row[
            "same_official_key_is_not_an_identity_or_connectivity_shortcut"
        ] is True
        and all(row[field] == 0 for field in ZERO_FIELDS),
        "incidence-only non-DSU semantic boundary",
    )
    for endpoint_row in (left, right):
        require(
            type(endpoint_row["final_Round299A_official_key_id"]) is str
            and type(endpoint_row[
                "final_Round299A_official_key_ordinal"
            ]) is int,
            "endpoint official-key completeness",
        )
        if endpoint_row["registry_entry_kind"] == PRESERVED:
            provenance = endpoint_row["preserved_Round266_provenance"]
            require(
                type(provenance) is dict
                and type(provenance["Round266_quotient_component_id"]) is str
                and type(provenance[
                    "Round266_component_frontier_row_sha256"
                ]) is str,
                "preserved endpoint member/root provenance",
            )
        else:
            require(
                endpoint_row["registry_entry_kind"] == R288
                and endpoint_row["preserved_Round266_provenance"] is None,
                "new endpoint excludes Round266 provenance",
            )
    require(row == expected, "edge exact source reconstruction")


def validate_exclusion(
    row: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    check_closed(row, "candidate assignment exclusion")
    require(
        row["target_registry_reference_count"] == 1
        and row["assignment_only_reason"]
        == "ONE_TARGET_PHYSICAL_INCIDENCE_ASSIGNMENT__"
        "CANNOT_FORM_UNORDERED_OCCURRENCE_PAIR"
        and row["canonical_two_target_incidence_edge_issued"] is False
        and row[
            "formal_canonical_two_target_lower_physical_witness_"
            "incidence_edge_credit"
        ] == 0
        and all(row[field] == 0 for field in ZERO_FIELDS),
        "single-target assignment non-edge boundary",
    )
    endpoint_row = row["target_Round294_registry_occurrence"]
    require(
        type(endpoint_row["registry_occurrence_id"]) is str,
        "assignment endpoint",
    )
    require(row == expected, "assignment exact source reconstruction")


def validate_result(
    result: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    check_result_self(result, "Round300D candidate")
    require(
        result["schema"] == SCHEMA
        and result["producer_sha256"] == PRODUCER_SHA256
        and result["result_sha256"] == RESULT_SELF_SHA256
        and result["seed_affects_output"] is False
        and result["ledger"]["file_sha256"] == LEDGER_SHA256
        and result["promotion_census"][
            "canonical_unordered_incidence_edge_count"
        ] == 111_524
        and result["promotion_census"][
            "single_target_assignment_exclusion_count"
        ] == 1_600
        and result["semantic_scope"][
            "eligible_for_component_DSU_application"
        ] is False
        and result["semantic_scope"][
            "incidence_edge_is_topological_occurrence_union_claim"
        ] is False
        and result["semantic_scope"][
            "incidence_edge_is_occurrence_identity_collapse"
        ] is False
        and result["strict_nonpromotion"]["formal_component_edge_count"] == 0
        and result["strict_nonpromotion"]["formal_component_union_count"] == 0
        and result["strict_nonpromotion"][
            "formal_official_key_merge_count"
        ] == 0
        and result["strict_nonpromotion"][
            "formal_component_quotient_credit"
        ] == 0
        and result["strict_nonpromotion"][
            "formal_DSU_rank_reduction_count"
        ] == 0
        and result["strict_nonpromotion"][
            "post_Round300D_quotient_component_count"
        ] is None
        and "DIAGNOSTIC_HYPOTHESIS_ONLY" in result["strict_nonpromotion"][
            "historical_29984_rank_reduction_number_status"
        ]
        and all(
            result["formal_credit_transition"][field] == 0
            for field in ZERO_FIELDS
        ),
        "Round300D result incidence-only boundary",
    )
    require(result == expected, "result exact independent reconstruction")


def validate_ledger(
    ledger: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    require(ledger["schema"] == LEDGER_SCHEMA, "ledger schema")
    edges = ledger["canonical_incidence_edge_rows"]
    exclusions = ledger["single_target_assignment_exclusion_rows"]
    require(
        type(edges) is list
        and len(edges)
        == ledger["canonical_incidence_edge_row_count"] == 111_524
        and type(exclusions) is list
        and len(exclusions)
        == ledger["single_target_assignment_exclusion_row_count"] == 1_600,
        "ledger row counts",
    )
    require(
        [row[EDGE_ID] for row in edges]
        == sorted(row[EDGE_ID] for row in edges)
        and [row[EXCLUSION_ID] for row in exclusions]
        == sorted(row[EXCLUSION_ID] for row in exclusions),
        "ledger canonical ordering",
    )
    for row, expected_row in zip(
        edges, expected["canonical_incidence_edge_rows"], strict=True
    ):
        validate_edge(row, expected_row)
    for row, expected_row in zip(
        exclusions,
        expected["single_target_assignment_exclusion_rows"],
        strict=True,
    ):
        validate_exclusion(row, expected_row)
    edge_commitment = commitment(edges, EDGE_ID)
    exclusion_commitment = commitment(exclusions, EXCLUSION_ID)
    require(
        ledger["canonical_incidence_edge_row_ids_sha256"]
        == edge_commitment["row_ids_sha256"]
        and ledger["canonical_incidence_edge_row_hashes_sha256"]
        == edge_commitment["row_hashes_sha256"]
        and ledger["canonical_incidence_edge_rows_sha256"]
        == edge_commitment["rows_sha256"]
        and ledger["single_target_assignment_exclusion_row_ids_sha256"]
        == exclusion_commitment["row_ids_sha256"]
        and ledger["single_target_assignment_exclusion_row_hashes_sha256"]
        == exclusion_commitment["row_hashes_sha256"]
        and ledger["single_target_assignment_exclusion_rows_sha256"]
        == exclusion_commitment["rows_sha256"],
        "ledger internal commitments",
    )
    require(ledger == expected, "ledger exact independent reconstruction")


def reclose_row(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = sha_object(row)


def reclose_result(result: dict[str, Any]) -> None:
    result.pop("result_sha256", None)
    result["result_sha256"] = sha_object(result)


def attack_suite(
    expected_ledger: dict[str, Any],
    expected_result: dict[str, Any],
    candidate_ledger_raw: bytes,
) -> dict[str, Any]:
    edges = expected_ledger["canonical_incidence_edge_rows"]
    exclusions = expected_ledger["single_target_assignment_exclusion_rows"]
    same = next(row for row in edges
                if row["official_key_relation"] == "SAME_OFFICIAL_KEY")
    cross = next(row for row in edges
                 if row["official_key_relation"] == "CROSS_OFFICIAL_KEY")
    multi = next(row for row in edges if row["witness_multiplicity"] > 1)
    preserved = next(
        row for row in edges
        if row["endpoint_tranche_relation"]
        == PRESERVED + "|" + PRESERVED
    )

    records: list[dict[str, Any]] = []

    def record(
        label: str,
        attack_class: str,
        semantic_reclosed: bool,
        action: Callable[[], None],
    ) -> None:
        rejected = False
        reason = ""
        try:
            action()
        except (
            VerificationError, KeyError, IndexError, TypeError,
            ValueError, zlib.error,
        ) as error:
            rejected = True
            reason = type(error).__name__ + ":" + str(error)
        require(rejected, "attack accepted:" + label)
        payload = {
            "attack_label": label,
            "attack_class": attack_class,
            "semantic_payload_reclosed": semantic_reclosed,
            "rejected": True,
            "rejection_reason": reason,
        }
        records.append(close_row(
            "round300d-independent-attack:",
            "ROUND300D_INDEPENDENT_ATTACK_CASE_V1",
            "Round300D_independent_attack_case_id",
            payload,
        ))

    def edge_case(
        label: str,
        base: dict[str, Any],
        mutate: Callable[[dict[str, Any]], None],
        reclosed: bool = True,
    ) -> None:
        def action() -> None:
            candidate = copy.deepcopy(base)
            mutate(candidate)
            if reclosed:
                reclose_row(candidate)
            validate_edge(candidate, base)
        record(label, "EDGE_ROW", reclosed, action)

    def exclusion_case(
        label: str,
        mutate: Callable[[dict[str, Any]], None],
    ) -> None:
        base = exclusions[0]

        def action() -> None:
            candidate = copy.deepcopy(base)
            mutate(candidate)
            reclose_row(candidate)
            validate_exclusion(candidate, base)
        record(label, "ASSIGNMENT_EXCLUSION_ROW", True, action)

    def result_case(
        label: str,
        mutate: Callable[[dict[str, Any]], None],
        reclosed: bool = True,
    ) -> None:
        def action() -> None:
            candidate = copy.deepcopy(expected_result)
            mutate(candidate)
            if reclosed:
                reclose_result(candidate)
            validate_result(candidate, expected_result)
        record(label, "RESULT", reclosed, action)

    edge_case(
        "FORGE_COMPONENT_DSU_ELIGIBILITY", cross,
        lambda row: row.__setitem__(
            "eligible_for_component_DSU_application", True
        ),
    )
    edge_case(
        "FORGE_FORMAL_COMPONENT_EDGE", cross,
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
    )
    edge_case(
        "FORGE_FORMAL_COMPONENT_UNION", cross,
        lambda row: row.__setitem__("formal_component_union_credit", 1),
    )
    edge_case(
        "FORGE_FORMAL_OFFICIAL_KEY_MERGE", cross,
        lambda row: row.__setitem__("formal_official_key_merge_credit", 1),
    )
    edge_case(
        "FORGE_FORMAL_COMPONENT_QUOTIENT", cross,
        lambda row: row.__setitem__(
            "formal_component_quotient_credit", 1
        ),
    )
    edge_case(
        "FORGE_DSU_RANK_REDUCTION", cross,
        lambda row: row.__setitem__("formal_DSU_rank_reduction_credit", 1),
    )
    edge_case(
        "FORGE_TOPOLOGICAL_UNION_CONNECTIVITY", cross,
        lambda row: row.__setitem__(
            "topological_occurrence_union_connectivity_claimed", True
        ),
    )
    edge_case(
        "FORGE_INCLUDED_STRATUM_GLUING_LEMMA", cross,
        lambda row: row.__setitem__(
            "included_stratum_gluing_lemma_pinned", True
        ),
    )
    edge_case(
        "FORGE_TWO_ATTACHMENT_CORRIDOR_LEMMA", cross,
        lambda row: row.__setitem__(
            "two_sided_attachment_or_corridor_gluing_lemma_pinned", True
        ),
    )
    edge_case(
        "FORGE_OCCURRENCE_IDENTITY_COLLAPSE", same,
        lambda row: row.__setitem__(
            "formal_occurrence_identity_collapse_credit", 1
        ),
    )
    edge_case(
        "FORGE_MAXIMALITY", same,
        lambda row: row.__setitem__("formal_maximality_credit", 1),
    )
    edge_case(
        "FORGE_FIBRE", same,
        lambda row: row.__setitem__("formal_fibre_credit", 1),
    )
    edge_case(
        "FORGE_GLOBAL_DISPOSITION", same,
        lambda row: row.__setitem__(
            "formal_global_disposition_credit", 1
        ),
    )
    edge_case(
        "FORGE_SEAM_EDGE", same,
        lambda row: row.__setitem__("formal_seam_edge_credit", 1),
    )
    edge_case(
        "FORGE_JX_JY_GLUE", same,
        lambda row: row.__setitem__(
            "formal_Jx_Jy_same_point_glue_credit", 1
        ),
    )
    edge_case(
        "ERASE_SHARED_INCIDENCE_PROOF", cross,
        lambda row: row.__setitem__(
            "shared_lower_witness_incidence_proved", False
        ),
    )
    edge_case(
        "ZERO_INCIDENCE_EDGE_CREDIT", cross,
        lambda row: row.__setitem__(
            "formal_canonical_two_target_lower_physical_witness_"
            "incidence_edge_credit", 0
        ),
    )
    edge_case(
        "DOUBLE_INCIDENCE_EDGE_CREDIT", cross,
        lambda row: row.__setitem__(
            "formal_canonical_two_target_lower_physical_witness_"
            "incidence_edge_credit", 2
        ),
    )
    edge_case(
        "FORGE_SELF_PAIR_FLAG", same,
        lambda row: row.__setitem__("self_pair", True),
    )
    edge_case(
        "SWAP_CANONICAL_ENDPOINT_ORDER", cross,
        lambda row: row[
            "canonical_unordered_Round294_registry_occurrence_ids"
        ].reverse(),
    )

    def duplicate_endpoint(row: dict[str, Any]) -> None:
        pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
        pair[1] = pair[0]
        row["right_endpoint"] = copy.deepcopy(row["left_endpoint"])

    edge_case("FORGE_DUPLICATE_ENDPOINT_SELF_PAIR", cross, duplicate_endpoint)
    edge_case(
        "DELETE_CANONICAL_ENDPOINT", cross,
        lambda row: row[
            "canonical_unordered_Round294_registry_occurrence_ids"
        ].pop(),
    )
    edge_case(
        "TAMPER_LEFT_REGISTRY_ROW_HASH", cross,
        lambda row: row["left_endpoint"].__setitem__(
            "Round294_occurrence_registry_row_sha256", "0" * 64
        ),
    )
    edge_case(
        "TAMPER_LEFT_REGISTRY_ROW_ID", cross,
        lambda row: row["left_endpoint"].__setitem__(
            "Round294_occurrence_registry_row_id", "forged"
        ),
    )
    edge_case(
        "CROSS_KEY_WRONGLY_REJECTED", cross,
        lambda row: (
            row.__setitem__("official_key_relation", "REJECTED_CROSS_KEY"),
            row.__setitem__(
                "formal_canonical_two_target_lower_physical_witness_"
                "incidence_edge_credit", 0
            ),
        ),
    )
    edge_case(
        "SAME_KEY_IDENTITY_SHORTCUT", same,
        lambda row: row.__setitem__(
            "formal_occurrence_identity_collapse_credit", 1
        ),
    )
    edge_case(
        "CROSS_KEY_KEY_MERGE", cross,
        lambda row: row["right_endpoint"].__setitem__(
            "final_Round299A_official_key_id",
            row["left_endpoint"]["final_Round299A_official_key_id"],
        ),
    )
    edge_case(
        "FORGE_WITNESS_MULTIPLICITY", multi,
        lambda row: row.__setitem__(
            "witness_multiplicity", row["witness_multiplicity"] + 1
        ),
    )

    def witness_histogram(row: dict[str, Any]) -> None:
        key = next(iter(row["witness_kind_histogram"]))
        row["witness_kind_histogram"][key] += 1

    edge_case("FORGE_WITNESS_KIND_HISTOGRAM", multi, witness_histogram)
    edge_case(
        "DELETE_SOURCE_WITNESS_ID", multi,
        lambda row: row[
            "source_Round295A_physical_incidence_binding_row_ids"
        ].pop(),
    )
    edge_case(
        "TAMPER_SOURCE_WITNESS_HASH", multi,
        lambda row: row[
            "source_Round295A_physical_incidence_binding_row_sha256s"
        ].__setitem__(0, "f" * 64),
    )
    edge_case(
        "FORGE_MIXED_TRANCHE", cross,
        lambda row: row.__setitem__(
            "endpoint_tranche_relation", PRESERVED + "|" + R288
        ),
    )
    edge_case(
        "TRANCHE_SUBSTITUTION", cross,
        lambda row: row["left_endpoint"].__setitem__(
            "registry_entry_kind",
            (
                PRESERVED
                if row["left_endpoint"]["registry_entry_kind"] == R288
                else R288
            ),
        ),
    )
    edge_case(
        "TAMPER_ROUND266_COMPONENT_ROOT", preserved,
        lambda row: row["left_endpoint"][
            "preserved_Round266_provenance"
        ].__setitem__("Round266_quotient_component_id", "forged-root"),
    )
    edge_case(
        "TAMPER_ROUND266_ROOT_ROW_HASH", preserved,
        lambda row: row["left_endpoint"][
            "preserved_Round266_provenance"
        ].__setitem__("Round266_component_frontier_row_sha256", "0" * 64),
    )
    exclusion_case(
        "PROMOTE_SINGLE_TARGET_ASSIGNMENT_TO_EDGE",
        lambda row: (
            row.__setitem__("canonical_two_target_incidence_edge_issued", True),
            row.__setitem__(
                "formal_canonical_two_target_lower_physical_witness_"
                "incidence_edge_credit", 1
            ),
        ),
    )
    exclusion_case(
        "GRANT_ASSIGNMENT_COMPONENT_EDGE",
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
    )
    exclusion_case(
        "GRANT_ASSIGNMENT_DSU_RANK",
        lambda row: row.__setitem__(
            "formal_DSU_rank_reduction_credit", 1
        ),
    )
    result_case(
        "RESULT_FORGE_EDGE_COUNT",
        lambda row: row["promotion_census"].__setitem__(
            "canonical_unordered_incidence_edge_count", 111_525
        ),
    )
    result_case(
        "RESULT_GRANT_COMPONENT_UNION",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "formal_component_union_count", 111_524
        ),
    )
    result_case(
        "RESULT_GRANT_DSU_RANK_29984",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "formal_DSU_rank_reduction_count", 29_984
        ),
    )
    result_case(
        "RESULT_FORGE_QUOTIENT_COUNT",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "post_Round300D_quotient_component_count", 33_240
        ),
    )
    result_case(
        "RESULT_PROMOTE_DIAGNOSTIC_29984_TO_FORMAL",
        lambda row: row["strict_nonpromotion"].__setitem__(
            "historical_29984_rank_reduction_number_status",
            "FORMAL_DSU_RANK_REDUCTION_CREDIT",
        ),
    )
    result_case(
        "RESULT_FORGE_DSU_ELIGIBILITY",
        lambda row: row["semantic_scope"].__setitem__(
            "eligible_for_component_DSU_application", True
        ),
    )
    result_case(
        "RESULT_FORGE_TOPOLOGICAL_UNION",
        lambda row: row["semantic_scope"].__setitem__(
            "incidence_edge_is_topological_occurrence_union_claim", True
        ),
    )
    result_case(
        "RESULT_FORGE_PRODUCER_PIN",
        lambda row: row.__setitem__("producer_sha256", "0" * 64),
    )
    result_case(
        "RESULT_FORGE_UPSTREAM_PIN",
        lambda row: row["input_file_pins"].__setitem__(
            R295A_INCIDENCE, "0" * 64
        ),
    )
    result_case(
        "RESULT_FORGE_LEDGER_ATTACHMENT",
        lambda row: row["ledger"].__setitem__("file_sha256", "f" * 64),
    )
    result_case(
        "RESULT_BREAK_SELF_CLOSURE",
        lambda row: row.__setitem__("result_sha256", "0" * 64),
        reclosed=False,
    )

    def metadata_case(label: str, field: str, value: Any) -> None:
        expected = {
            "canonical_incidence_edge_row_count": 111_524,
            "canonical_incidence_edge_row_ids_sha256":
                expected_ledger[
                    "canonical_incidence_edge_row_ids_sha256"
                ],
            "canonical_incidence_edge_rows_sha256":
                expected_ledger["canonical_incidence_edge_rows_sha256"],
            "single_target_assignment_exclusion_row_count": 1_600,
            "single_target_assignment_exclusion_rows_sha256":
                expected_ledger[
                    "single_target_assignment_exclusion_rows_sha256"
                ],
        }

        def action() -> None:
            candidate = dict(expected)
            candidate[field] = value
            require(candidate == expected, "ledger metadata reconstruction")
        record(label, "LEDGER_STRUCTURE", False, action)

    metadata_case(
        "DROP_EDGE_ROW_RECOMMIT",
        "canonical_incidence_edge_row_count", 111_523,
    )
    metadata_case(
        "ADD_EDGE_ROW_RECOMMIT",
        "canonical_incidence_edge_row_count", 111_525,
    )
    metadata_case(
        "REORDER_EDGE_ROWS_RECOMMIT",
        "canonical_incidence_edge_rows_sha256", "0" * 64,
    )
    metadata_case(
        "DROP_ASSIGNMENT_EXCLUSION_RECOMMIT",
        "single_target_assignment_exclusion_row_count", 1_599,
    )

    def raw_pin_case(label: str, mutate: Callable[[bytearray], None]) -> None:
        def action() -> None:
            candidate = bytearray(candidate_ledger_raw)
            mutate(candidate)
            require(
                hashlib.sha256(candidate).hexdigest() == LEDGER_SHA256,
                "candidate ledger byte pin",
            )
            strict_gzip(bytes(candidate), "attacked ledger")
        record(label, "BYTE_TRANSPORT", False, action)

    raw_pin_case(
        "GZIP_MTIME_TAMPER",
        lambda raw: raw.__setitem__(4, (raw[4] + 1) % 256),
    )
    raw_pin_case(
        "GZIP_PAYLOAD_BIT_FLIP",
        lambda raw: raw.__setitem__(20, raw[20] ^ 1),
    )

    def concatenated_member() -> None:
        candidate = candidate_ledger_raw + gzip.compress(
            b"{}", compresslevel=9, mtime=0
        )
        require(
            hashlib.sha256(candidate).hexdigest() == LEDGER_SHA256,
            "candidate ledger concatenated-member pin",
        )
        strict_gzip(candidate, "concatenated ledger")

    record(
        "GZIP_CONCATENATED_MEMBER",
        "BYTE_TRANSPORT",
        False,
        concatenated_member,
    )
    record(
        "OUTPUT_PATH_TRAVERSAL",
        "PATH_POLICY",
        False,
        lambda: validate_output_pair(
            Path("/tmp/round300d-attacks.json"),
            HERE / f"{PREFIX}_verification.json",
        ),
    )
    record(
        "OUTPUT_PATH_COLLISION",
        "PATH_POLICY",
        False,
        lambda: validate_output_pair(
            HERE / f"{PREFIX}_attack_suite.json",
            HERE / f"{PREFIX}_attack_suite.json",
        ),
    )
    record(
        "MANIFEST_PATH_TRAVERSAL_MEMBER",
        "MANIFEST_POLICY",
        False,
        lambda: parse_manifest_bytes(
            (("0" * 64) + "  ../escape.json\n").encode("ascii"),
            "attacked-manifest",
        ),
    )
    record(
        "MANIFEST_DUPLICATE_MEMBER",
        "MANIFEST_POLICY",
        False,
        lambda: parse_manifest_bytes(
            (
                (("0" * 64) + "  member.json\n")
                + (("f" * 64) + "  member.json\n")
            ).encode("ascii"),
            "attacked-manifest",
        ),
    )

    require(len(records) == 60, "independent attack census")
    require(all(row["rejected"] is True for row in records),
            "all attacks rejected")
    semantic_count = sum(
        row["semantic_payload_reclosed"] is True for row in records
    )
    require(semantic_count == 48, "semantic reclosed attack census")
    suite = {
        "schema": ATTACK_SCHEMA,
        "status":
            "PASS_ALL_60_INDEPENDENT_ATTACKS_REJECTED__"
            "INCIDENCE_ONLY_DSU_OVERREACH_FAILS_CLOSED",
        "attack_count": len(records),
        "rejected_count": len(records),
        "semantic_reclosed_attack_count": semantic_count,
        "all_attacks_rejected": True,
        "producer_attack_suite_imported_or_trusted": False,
        "attacks": records,
        "attack_suite_sha256": "",
    }
    payload = dict(suite)
    payload.pop("attack_suite_sha256")
    suite["attack_suite_sha256"] = sha_object(payload)
    return suite


def atomic_write(path: Path, raw: bytes) -> None:
    require(
        path.parent.resolve() == HERE.resolve()
        and path.name.startswith(PREFIX + "_"),
        "output HERE/prefix confinement",
    )
    require(not path.is_symlink(), "output symlink")
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=HERE,
        prefix="." + path.name + ".",
        delete=False,
    ) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
    temporary.replace(path)


def validate_output_pair(attacks: Path, verification: Path) -> None:
    require(attacks != verification, "distinct verifier output paths")
    for path in (attacks, verification):
        require(
            path.parent.resolve() == HERE.resolve()
            and path.name.startswith(PREFIX + "_")
            and not path.is_symlink(),
            "verifier output path policy",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", default="300411")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--attacks", type=Path, default=ATTACKS)
    parser.add_argument("--verification", type=Path, default=VERIFICATION)
    args = parser.parse_args()
    require(bool(args.seed), "nonempty seed bookkeeping")
    validate_output_pair(args.attacks, args.verification)
    require(
        PIN_RE.fullmatch(PRODUCER_SHA256) is not None
        and PIN_RE.fullmatch(LEDGER_SHA256) is not None
        and PIN_RE.fullmatch(RESULT_SHA256) is not None
        and PIN_RE.fullmatch(RESULT_SELF_SHA256) is not None,
        "fixed Round300D candidate pins installed",
    )

    # The producer is touched only here, as inert bytes for a direct pin.
    require(
        sha_file(PRODUCER) == PRODUCER_SHA256,
        "producer inert-byte pin",
    )
    candidate_ledger_raw = safe_bytes(LEDGER)
    candidate_result_raw = safe_bytes(RESULT, 20_000_000)
    require(
        hashlib.sha256(candidate_ledger_raw).hexdigest() == LEDGER_SHA256,
        "candidate ledger byte pin",
    )
    require(
        hashlib.sha256(candidate_result_raw).hexdigest() == RESULT_SHA256,
        "candidate result byte pin",
    )
    strict_gzip(candidate_ledger_raw, "candidate ledger")

    # Reconstruction is complete before candidate JSON objects are trusted.
    expected_ledger, expected_result, reconstruction = build_expected()
    validate_ledger(expected_ledger, expected_ledger)
    validate_result(expected_result, expected_result)
    expected_ledger_raw = deterministic_gzip(expected_ledger)
    expected_result_raw = canonical(expected_result) + b"\n"
    require(
        candidate_ledger_raw == expected_ledger_raw,
        "candidate/independent deterministic gzip byte equality",
    )
    require(
        candidate_result_raw == expected_result_raw,
        "candidate/independent result byte equality",
    )
    candidate_result = strict_json(candidate_result_raw, RESULT.name)
    validate_result(candidate_result, expected_result)

    attacks = attack_suite(
        expected_ledger, expected_result, candidate_ledger_raw
    )
    attack_bytes = canonical(attacks) + b"\n"
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_ROUND300D__111524_CANONICAL_"
            "TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGES__"
            "1600_ASSIGNMENT_EXCLUSIONS__ZERO_COMPONENT_DSU_CREDIT__"
            "ALL_60_ATTACKS_REJECTED",
        "seed_affects_verdict_or_artifacts": False,
        "verifier_sha256": sha_file(Path(__file__).resolve()),
        "producer_source_imported_executed_or_parsed": False,
        "producer_used_only_as_inert_fixed_bytes": True,
        "producer_sha256": PRODUCER_SHA256,
        "candidate_artifacts": {
            "ledger_filename": LEDGER.name,
            "ledger_file_sha256": LEDGER_SHA256,
            "result_filename": RESULT.name,
            "result_file_sha256": RESULT_SHA256,
            "result_sha256": RESULT_SELF_SHA256,
            "candidate_object_and_byte_equality": True,
            "deterministic_single_member_gzip_byte_equality": True,
        },
        "sealed_upstream_boundary": {
            "input_manifest_pins": dict(sorted(MANIFEST_PINS.items())),
            "input_file_pins": dict(sorted(INPUT_PINS.items())),
            "all_manifest_members_directly_reconciled": True,
            "all_named_source_tables_reopened_and_recommitted": True,
        },
        "independent_reconstruction": reconstruction,
        "semantic_conclusion": {
            "promoted_relation":
                "CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE",
            "formal_incidence_edge_credit": 111_524,
            "eligible_for_component_DSU_application": False,
            "topological_occurrence_union_connectivity_proved": False,
            "included_stratum_plus_two_attachment_or_corridor_lemma_pinned":
                False,
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_official_key_merge_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_component_union_credit": 0,
            "formal_component_quotient_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
            "historical_29984_is_diagnostic_only": True,
            "official_key_is_not_component_purity_constraint": True,
            "same_key_is_not_connectivity_or_identity_shortcut": True,
            "cross_key_incidence_edge_count_preserved": 25_216,
        },
        "independent_attack_suite": {
            "attack_count": attacks["attack_count"],
            "rejected_count": attacks["rejected_count"],
            "semantic_reclosed_attack_count":
                attacks["semantic_reclosed_attack_count"],
            "all_attacks_rejected": True,
            "attack_suite_filename": ATTACKS.name,
            "attack_suite_file_sha256":
                hashlib.sha256(attack_bytes).hexdigest(),
            "attack_suite_sha256": attacks["attack_suite_sha256"],
        },
        "verification_sha256": "",
    }
    payload = dict(verification)
    payload.pop("verification_sha256")
    verification["verification_sha256"] = sha_object(payload)
    verification_bytes = canonical(verification) + b"\n"
    if not args.no_write:
        atomic_write(args.attacks, attack_bytes)
        atomic_write(args.verification, verification_bytes)
    print(verification["status"])
    print(json.dumps(reconstruction, sort_keys=True))
    print("attack_suite_file_sha256="
          + hashlib.sha256(attack_bytes).hexdigest())
    print("attack_suite_sha256=" + attacks["attack_suite_sha256"])
    print("verification_file_sha256="
          + hashlib.sha256(verification_bytes).hexdigest())
    print("verification_sha256=" + verification["verification_sha256"])


if __name__ == "__main__":
    main()
