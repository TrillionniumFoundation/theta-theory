#!/usr/bin/env python3
"""Round301 legal expanded-registry component DSU application.

Until every R300-E/F/G/H channel is independently sealed this program runs
only in ``--preliminary`` mode and writes no deliverable.  The preliminary
path already performs the expensive independent reconstruction:

* 564,492 identity-preserved members;
* 367,964 pre-application component roots;
* complete sealed legal edge channels, with append-only channel registry;
* forward and exact-reverse DSU application with identical final partition.

R295-A/R300-D lower-witness incidence and R300-A closure-contact pairs are
never legal DSU inputs.  The obsolete Round298 scripts and every .tmp spike
are absent from this source boundary and are never imported, executed, or
parsed.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, Callable, Iterable, Iterator, TextIO


HERE = Path(__file__).resolve().parent
PREFIX = "cm2_round301_source_g_legal_component_dsu_application"
EDGE_APPLICATION_LEDGER = PREFIX + "_edge_application_ledger.json.gz"
MEMBER_COMPONENT_LEDGER = PREFIX + "_member_component_ledger.json.gz"
COMPONENT_KEY_INCIDENCE_LEDGER = (
    PREFIX + "_component_key_incidence_ledger.json.gz"
)
INELIGIBLE_SOURCE_LEDGER = (
    PREFIX + "_ineligible_source_consumption_ledger.json.gz"
)
RESULT_FILE = PREFIX + "_result.json"

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
R299A_MANIFEST = (
    "cm2_round299a_source_g_refined_occurrence_official_key_binding_closure_"
    "manifest.sha256"
)
R299A_LEDGER = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure_ledger.json.gz"
)
R299A_RESULT = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure_result.json"
)
R299A_VERIFICATION = (
    "cm2_round299a_source_g_refined_occurrence_"
    "official_key_binding_closure_verification.json"
)
R300A_PREFIX = (
    "cm2_round300a_source_g_r287_graph_zero_lower_frontier_exhaustion"
)
R300A_MANIFEST = R300A_PREFIX + "_manifest.sha256"
R300A_LEDGER = R300A_PREFIX + "_ledger.json.gz"
R300A_RESULT = R300A_PREFIX + "_result.json"
R300A_VERIFIER = R300A_PREFIX + "_verifier.py"
R300A_VERIFICATION = R300A_PREFIX + "_verification.json"
R300D_PREFIX = (
    "cm2_round300d_source_g_lower_physical_witness_"
    "component_edge_promotion"
)
R300D_MANIFEST = R300D_PREFIX + "_manifest.sha256"
R300D_LEDGER = R300D_PREFIX + "_ledger.json.gz"
R300D_RESULT = R300D_PREFIX + "_result.json"
R300D_VERIFIER = R300D_PREFIX + "_verifier.py"
R300D_VERIFICATION = R300D_PREFIX + "_verification.json"
R300E_WITNESS_LEDGER = (
    "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
    "promotion_witness_ledger.json.gz"
)
R300E_MANIFEST = (
    "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
    "promotion_manifest.sha256"
)
R300E_MANIFEST_PIN = (
    "4e6c4eec1af04a907285d41395aeef63e911b3b5486db91b33a95fa62e45177a"
)
R300E_WITNESS_LEDGER_PIN = (
    "69f480da55e917b7b75bfe1efa823a9228d9b563f6f3aabd4e2a364c9e50eb9f"
)
R300B_FACE_INVENTORY = (
    "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_"
    "inventory_closure_face_inventory.json.gz"
)
R300B_FACE_INVENTORY_PIN = (
    "443f26bdbed929d873972be0d2232809bf022feed1a5709001ee8f2dda49ac2d"
)
R300G_PREFIX = (
    "cm2_round300g_source_g_r300a_explicit_outgoing_seam_"
    "attachment_exclusion"
)
R300G_MANIFEST = R300G_PREFIX + "_manifest.sha256"
R300G_LEDGER = R300G_PREFIX + "_ledger.json.gz"
R300G_RESULT = R300G_PREFIX + "_result.json"
R300G_VERIFIER = R300G_PREFIX + "_verifier.py"
R300G_VERIFICATION = R300G_PREFIX + "_verification.json"
R300H_PREFIX = (
    "cm2_round300h_source_g_enriched_lower_witness_and_single_assignment_"
    "failclosed_closure"
)
R300H_PRODUCER = R300H_PREFIX + ".py"
R300H_MANIFEST = R300H_PREFIX + "_manifest.sha256"
R300H_PAIR_LEDGER = R300H_PREFIX + "_enriched_pair_disposition_ledger.json.gz"
R300H_SINGLE_LEDGER = R300H_PREFIX + "_single_target_disposition_ledger.json.gz"
R300H_ELIGIBLE_LEDGER = R300H_PREFIX + "_eligible_component_edge_ledger.json.gz"
R300H_RESULT = R300H_PREFIX + "_result.json"
R300H_VERIFIER = R300H_PREFIX + "_verifier.py"
R300H_ATTACKS = R300H_PREFIX + "_attack_suite.json"
R300H_VERIFICATION = R300H_PREFIX + "_verification.json"
R300H_REPORT = R300H_PREFIX + "_report.md"
R300H_COLD_REPLAY = R300H_PREFIX + "_cold_replay.md"

FOUNDATION_MANIFEST_PINS = {
    R266_MANIFEST:
        "63fb5b25d52ca5de579256499629d04d15f6a313e0a73f7e80fcb463385cbe09",
    R294_MANIFEST:
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    R299A_MANIFEST:
        "b1dfe718dd2b7477d9cc4067f1bade59d1589b3822eaf4b94b9dd721e61b468e",
}
FOUNDATION_FILE_PINS = {
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
    R299A_LEDGER:
        "ffea8120af2179990d5c9e7ff385193e2c5a08bed161cf5b570aa28b1f8b1ee0",
    R299A_RESULT:
        "4835bab4ebe7afc0da8d00395f83f881dd2aaf31e0697994fed54dc7d86302f5",
    R299A_VERIFICATION:
        "3a3ab65fdd6b5bd00062e1cebbd141e1c38bded7d920705a83a57ba24db0f27d",
}

INELIGIBLE_PACKAGE_PINS = {
    R300A_MANIFEST:
        "9f9e86d93aebe2b47e525af795a3a9e8331ab3b6f2d71ecafe69429238a1aee8",
    R300A_LEDGER:
        "ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d",
    R300A_RESULT:
        "b8f7c27f8761f1eb611f8fd57a0e773572f045963560f5d63b44baa1680e7ee4",
    R300A_VERIFIER:
        "b425a9836a474122a99cd76a0f4e81175c65c2f426ad7e38773cce46220c64d5",
    R300A_VERIFICATION:
        "e976fc2912c1d902029b8c4c7d4864bd8bb1cb6895bc09c215f2a5ac2400c696",
    R300D_MANIFEST:
        "8dd3907a363ae0c4fe7d524061a02b4c70944ce870ded941d5d617911ea1124e",
    R300D_LEDGER:
        "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7",
    R300D_RESULT:
        "59b7e788ed217ceb590a3e2125cc13aefbf447af236315ea607f4f631cb29c84",
    R300D_VERIFIER:
        "d7fbbeeb3f0959de54e55f20928f276a36df75100907b1af16bb2e46317ddc26",
    R300D_VERIFICATION:
        "a5bd12b10103b4785574bd4633e608c7fd5107369ba8f2343ebffe7e08eba1c7",
}

R300A_CANONICAL_PAIR_COMMITMENT = {
    "row_count": 3_232,
    "row_ids_sha256":
        "876617c3beda3cc50bcff712e6273786ba87a513d5422e875960353c6eb64332",
    "row_hashes_sha256":
        "2f34355d24534220e6cf42e636925d0f5adf9d7430b61563f20f2d4d928faac4",
    "rows_sha256":
        "7991da0c6f268cfb87628f1bee88f560ed319bec1028bee43e427c65ac8f6f16",
}
R300A_SOURCE_EXPANSION_COMMITMENT = {
    "row_count": 3_488,
    "row_ids_sha256":
        "22942899c9601c88f59014f4b9cd449b2758e60eaa803e949370b06fb58f0885",
    "row_hashes_sha256":
        "aeed60e7457dda5c1042f47198a223e5ad6cb4d1fa1a3d6b66187707f267cbe1",
    "rows_sha256":
        "99318f4f1c092a223448a5ccd2a70cbd6d9a8b9a9f2d5b9ee9fdb861c738cbcb",
}
R300D_INCIDENCE_COMMITMENT = {
    "row_count": 111_524,
    "row_ids_sha256":
        "19ce53e77604142bf0410e49b1f1c8bf921beb715538901776c517d098626c6b",
    "row_hashes_sha256":
        "97f5ae7ffde9c583bf0cc75e6ad685c4d22cdc487261576b8e904a69fcad17d2",
    "rows_sha256":
        "3623738c4a7a41980b6386d089f319d5149358e7e91fb422053289068eedbc8b",
}
R300D_SINGLE_COMMITMENT = {
    "row_count": 1_600,
    "row_ids_sha256":
        "74cedc49a8aa56c4520e56546390705e96faafae6c2d2547d8851ca123d9880c",
    "row_hashes_sha256":
        "96ff1c02ef4ea047a9b61bb0bfb806ced48e896cdf82000ba53a161a67e3ab24",
    "rows_sha256":
        "953522b88f21adb705505ec44ce121910fcdaa81dc13424068ec572733a28007",
}
R300E_WITNESS_COMMITMENT = {
    "row_count": 12_992,
    "row_ids_sha256":
        "8d4f4eb7e1a1058283c9c163eefe2516c01193e3d84a8ab8b0174faee3f9e9c8",
    "row_hashes_sha256":
        "71b8457998a7e5813d57b10197c2a8506111c7ec041f893bb177d8a01de5ab92",
    "rows_sha256":
        "6d2f26a0782e66fe01d440586c21846581a55944252e364909bb08600e09abaa",
}
R300B_FACE_INVENTORY_COMMITMENT = {
    "row_count": 62_548,
    "row_ids_sha256":
        "ec642912b4779fa7a19212ee34b3c2ff408b1e60f2d4862fb6a1a1d2127651f1",
    "row_hashes_sha256":
        "3ad41927e18ba1e527a091a3bb2536118810caed2659ec4f7e03134e4ba947d7",
    "rows_sha256":
        "4c8c0e4662f72301cc1c97fe71d2cdd2735bfce4bed1b5bb445bde9893876ee7",
}
R300G_COMMITMENT = {
    "row_count": 128,
    "row_ids_sha256":
        "77449ccec8ed05e1b1df63467c466225686eb5b73d1897708d406b671f3b14f9",
    "row_hashes_sha256":
        "fb36993227018ad0479e35bf6fae0b3f8ee8fbcaffbd38cf84e74f6822d5c22e",
    "rows_sha256":
        "cbf7483e4ad97570965dec413fa029053137316d702bb2f831d25f2472c737e9",
}
R300H_PAIR_COMMITMENT = {
    "row_count": 144,
    "row_ids_sha256":
        "1d077d69858a380df2c18923f73f0794a5a06b784ea6867431804bedc624f3cc",
    "row_hashes_sha256":
        "547baddd341f9177e43550c860b8965eb9ede290e1f8ce66fd488e98273afeaf",
    "rows_sha256":
        "9dd35a49e9c23e0228522d7a3c97ddaaa139a465e9a65f9cbacba9afada9a3cb",
}
R300H_SINGLE_COMMITMENT = {
    "row_count": 1_600,
    "row_ids_sha256":
        "23d05b1483c95be92b397eba7f4413eae03dbec9d0fd3a2e62d6586e8a585e44",
    "row_hashes_sha256":
        "6cb93443ba7653d8adc8151cccaf40752c99de924f5808e43d59f1e97c8f6e31",
    "rows_sha256":
        "f1ac5a8c3384bb33f2963ab0de73239834ff4b717bbb69da3621cfef882dc40b",
}
R300H_EMPTY_EDGE_COMMITMENT = {
    "row_count": 0,
    "row_ids_sha256":
        "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "row_hashes_sha256":
        "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
    "rows_sha256":
        "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
}

R266_MEMBER_COMMITMENT = {
    "row_count": 259_752,
    "row_ids_sha256":
        "f064d177c25985b38c899c651923b83ba47ee36b465902cca85a4c21e0c33ca6",
    "row_hashes_sha256":
        "1f28c84d14cf3fabb38d0f2d1fdf862ce8f6a4559552d68fd9c0a5bd0a3ed3ee",
    "rows_sha256":
        "28398acde446047ff4a210b2fa0831d2c44e3758f7e9239b5ec63cecc386b257",
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
R299A_COMMITMENT = {
    "row_count": 9_404,
    "row_ids_sha256":
        "a3786265b52feafd316cc81c71ab05ee32976b5ff7f1de091853d34a7b33e6e3",
    "row_hashes_sha256":
        "65e6f22b9085685b20a50dedfcb62cd08dd01e1ea70a61ee850d74450402b333",
    "rows_sha256":
        "6955fe1c36555c7aa492e4c5cfd1ab945fe16b824ea49bd3d72cea3bd3136c0f",
}

PRESERVED = "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
R288 = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
R292 = "CANDIDATE_NEW_ROUND292_REFINED_R287_SUPPORT_COMPONENT"
PIN_RE = re.compile(r"^[0-9a-f]{64}$")


class PreliminaryError(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise PreliminaryError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
)


def pieces(value: Any) -> Iterable[bytes]:
    for token in ENCODER.iterencode(value):
        yield token.encode("utf-8")


def canonical(value: Any) -> bytes:
    return b"".join(pieces(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for token in pieces(value):
        state.update(token)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def safe_file(path: Path, maximum: int = 3_000_000_000) -> None:
    need(path.parent.resolve() == HERE.resolve(), "HERE path")
    need(path.exists() and not path.is_symlink(), "existing non-symlink")
    info = os.lstat(path)
    need(
        stat.S_ISREG(info.st_mode)
        and info.st_nlink == 1
        and 0 < info.st_size <= maximum,
        "single-link regular bounded file:" + path.name,
    )


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw and not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
         "strict bytes:" + label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label + ":" + key)
            output[key] = value
        return output

    def reject(token: str) -> Any:
        raise PreliminaryError("noninteger JSON:" + label + ":" + token)

    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=unique,
            parse_float=reject,
            parse_constant=reject,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PreliminaryError("invalid JSON:" + label) from error
    need(type(value) is dict, "top-level object:" + label)
    return value


def read_json(name: str) -> dict[str, Any]:
    path = HERE / name
    safe_file(path)
    return strict_json(path.read_bytes(), name)


def validate_closed_row(row: dict[str, Any], label: str) -> None:
    payload = dict(row)
    claimed = payload.pop("row_sha256", None)
    need(
        type(claimed) is str and digest(payload) == claimed,
        "row self closure:" + label,
    )


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for token in pieces(value):
            self.state.update(token)
        self.count += 1

    def finish(self) -> str:
        state = self.state.copy()
        state.update(b"]")
        return state.hexdigest()


def iter_array(
    stream: TextIO,
    marker: str = '"rows":[',
    initial: str = "",
) -> Iterator[dict[str, Any]]:
    buffer = initial
    while marker not in buffer:
        block = stream.read(1 << 20)
        need(bool(block), "missing array marker:" + marker)
        buffer += block
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
            PreliminaryError("stream float:" + token)
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            PreliminaryError("stream constant:" + token)
        ),
    )
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated streamed array")
            buffer = block
            continue
        if buffer[0] == ",":
            buffer = buffer[1:]
            continue
        if buffer[0] == "]":
            return
        while True:
            try:
                row, end = decoder.raw_decode(buffer)
                break
            except json.JSONDecodeError:
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed row")
                buffer += block
        need(type(row) is dict, "stream row object")
        yield row
        buffer = buffer[end:]


def validated_gzip_rows(
    name: str,
    id_field: str,
    expected: dict[str, Any],
    table: str = "rows",
) -> Iterator[dict[str, Any]]:
    rows = ListHash()
    ids = ListHash()
    hashes = ListHash()
    occurrences = (
        ListHash() if "occurrence_ids_sha256" in expected else None
    )
    with gzip.open(
        HERE / name, "rt", encoding="utf-8", newline=""
    ) as stream:
        seen_ids: set[str] = set()
        for row in iter_array(stream, marker='"' + table + '":['):
            validate_closed_row(row, name)
            row_id = row[id_field]
            need(
                type(row_id) is str and row_id not in seen_ids,
                "unique string row ID:" + name,
            )
            seen_ids.add(row_id)
            rows.add(row)
            ids.add(row_id)
            hashes.add(row["row_sha256"])
            if occurrences is not None:
                occurrences.add(row["registry_occurrence_id"])
            yield row
    actual = {
        "row_count": rows.count,
        "row_ids_sha256": ids.finish(),
        "row_hashes_sha256": hashes.finish(),
        "rows_sha256": rows.finish(),
    }
    if occurrences is not None:
        actual["occurrence_ids_sha256"] = occurrences.finish()
    need(actual == expected, "complete gzip commitment:" + name + ":" + table)


def stream_gzip_rows(
    name: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
    table: str = "rows",
) -> None:
    for row in validated_gzip_rows(
        name, id_field, expected, table=table
    ):
        visit(row)


def pinned_gzip_rows_without_semantic_rehash(
    name: str,
    file_pin: str,
    id_field: str,
    expected_count: int,
    table: str = "rows",
) -> Iterator[dict[str, Any]]:
    """Stream an auxiliary sealed table under its exact package byte pin.

    This is used only for the enormous R300B face certificates.  Their
    independent upstream verifier already reclosed every algebraic payload;
    Round301 needs the exact endpoint/decision projection and pins the full
    immutable gzip bytes, but does not redundantly canonicalize every large
    certificate object again.
    """

    path = HERE / name
    safe_file(path)
    need(file_sha256(path) == file_pin, "auxiliary sealed byte pin:" + name)
    seen: set[str] = set()
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        for row in iter_array(stream, marker='"' + table + '":['):
            row_id = row.get(id_field)
            need(
                type(row_id) is str
                and row_id not in seen
                and PIN_RE.fullmatch(row.get("row_sha256", "")) is not None,
                "auxiliary sealed row boundary:" + name,
            )
            seen.add(row_id)
            yield row
    need(len(seen) == expected_count, "auxiliary sealed row count:" + name)


def stream_plain_table(
    name: str,
    table: str,
    id_field: str,
    expected: dict[str, Any],
    visit: Callable[[dict[str, Any]], None],
) -> None:
    marker = '"' + table + '":'
    carry = ""
    with (HERE / name).open("rt", encoding="utf-8", newline="") as stream:
        while True:
            block = stream.read(1 << 20)
            need(bool(block), "missing table:" + table)
            combined = carry + block
            if marker in combined:
                initial = combined.split(marker, 1)[1]
                break
            carry = combined[-len(marker):]
        rows = ListHash()
        ids = ListHash()
        hashes = ListHash()
        seen_ids: set[str] = set()
        for row in iter_array(stream, initial=initial):
            validate_closed_row(row, table)
            row_id = row[id_field]
            need(
                type(row_id) is str and row_id not in seen_ids,
                "unique string row ID:" + table,
            )
            seen_ids.add(row_id)
            rows.add(row)
            ids.add(row_id)
            hashes.add(row["row_sha256"])
            visit(row)
    need(
        {
            "row_count": rows.count,
            "row_ids_sha256": ids.finish(),
            "row_hashes_sha256": hashes.finish(),
            "rows_sha256": rows.finish(),
        } == expected,
        "complete plain-table commitment:" + table,
    )


def parse_manifest(name: str) -> dict[str, str]:
    path = HERE / name
    safe_file(path, 300_000)
    output: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        value, member = match.groups()
        need(Path(member).name == member and member not in output,
             "manifest member policy:" + name)
        output[member] = value
    need(bool(output), "nonempty manifest:" + name)
    return output


def validate_manifest_selection(
    name: str,
    manifest_pin: str,
    selected: dict[str, str],
) -> None:
    need(file_sha256(HERE / name) == manifest_pin, "manifest pin:" + name)
    entries = parse_manifest(name)
    for member, fixed_pin in selected.items():
        safe_file(HERE / member)
        need(
            entries.get(member) == fixed_pin
            and file_sha256(HERE / member) == fixed_pin,
            "selected package member:" + name + ":" + member,
        )


def check_result_self(document: dict[str, Any], label: str) -> None:
    payload = dict(document)
    claimed = payload.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(payload),
         "result self closure:" + label)


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "row closure field absent")
    row = dict(payload)
    row["row_sha256"] = digest(payload)
    return row


def measure_rows(
    factory: Callable[[], Iterator[dict[str, Any]]],
    id_field: str,
) -> dict[str, Any]:
    rows = ListHash()
    ids = ListHash()
    hashes = ListHash()
    seen: set[str] = set()
    for row in factory():
        validate_closed_row(row, id_field)
        row_id = row.get(id_field)
        need(
            type(row_id) is str and row_id not in seen,
            "generated unique row ID:" + id_field,
        )
        seen.add(row_id)
        rows.add(row)
        ids.add(row_id)
        hashes.add(row["row_sha256"])
    return {
        "row_count": rows.count,
        "row_ids_sha256": ids.finish(),
        "row_hashes_sha256": hashes.finish(),
        "rows_sha256": rows.finish(),
    }


def write_rows_ledger(
    name: str,
    schema: str,
    status: str,
    id_field: str,
    factory: Callable[[], Iterator[dict[str, Any]]],
) -> dict[str, Any]:
    """Write one deterministic, single-member gzip ledger in two passes."""

    commitment = measure_rows(factory, id_field)
    path = HERE / name
    work = HERE / (name + ".incomplete")
    need(path.parent.resolve() == HERE.resolve(), "output path boundary")
    if work.exists():
        info = os.lstat(work)
        need(
            not work.is_symlink()
            and stat.S_ISREG(info.st_mode)
            and info.st_nlink == 1,
            "safe incomplete output",
        )
        work.unlink()
    if path.exists():
        safe_file(path)
    try:
        with work.open("xb") as raw:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                fileobj=raw,
                compresslevel=9,
                mtime=0,
            ) as stream:
                prefix = (
                    b'{"every_row_closed_by_own_SHA256":true,'
                    + b'"row_count":'
                    + canonical(commitment["row_count"])
                    + b',"row_hashes_sha256":'
                    + canonical(commitment["row_hashes_sha256"])
                    + b',"row_ids_sha256":'
                    + canonical(commitment["row_ids_sha256"])
                    + b',"rows":['
                )
                stream.write(prefix)
                second_rows = ListHash()
                second_ids = ListHash()
                second_hashes = ListHash()
                count = 0
                for row in factory():
                    validate_closed_row(row, id_field)
                    if count:
                        stream.write(b",")
                    stream.write(canonical(row))
                    second_rows.add(row)
                    second_ids.add(row[id_field])
                    second_hashes.add(row["row_sha256"])
                    count += 1
                stream.write(
                    b'],"rows_sha256":'
                    + canonical(commitment["rows_sha256"])
                    + b',"schema":'
                    + canonical(schema)
                    + b',"status":'
                    + canonical(status)
                    + b"}"
                )
        second = {
            "row_count": count,
            "row_ids_sha256": second_ids.finish(),
            "row_hashes_sha256": second_hashes.finish(),
            "rows_sha256": second_rows.finish(),
        }
        need(second == commitment, "two-pass generated row equality:" + name)
        os.replace(work, path)
    except BaseException:
        if work.exists() and not work.is_symlink():
            work.unlink()
        raise
    safe_file(path)
    return {
        "filename": name,
        "file_sha256": file_sha256(path),
        **commitment,
        "schema": schema,
    }


def write_closed_result(
    name: str,
    payload: dict[str, Any],
) -> tuple[str, str]:
    need("result_sha256" not in payload, "result closure field absent")
    document = dict(payload)
    document["result_sha256"] = digest(payload)
    path = HERE / name
    work = HERE / (name + ".incomplete")
    if work.exists():
        info = os.lstat(work)
        need(
            not work.is_symlink()
            and stat.S_ISREG(info.st_mode)
            and info.st_nlink == 1,
            "safe incomplete result",
        )
        work.unlink()
    if path.exists():
        safe_file(path)
    try:
        with work.open("xb") as stream:
            stream.write(canonical(document))
        os.replace(work, path)
    except BaseException:
        if work.exists() and not work.is_symlink():
            work.unlink()
        raise
    safe_file(path)
    return file_sha256(path), document["result_sha256"]


@dataclass(frozen=True)
class Channel:
    name: str
    manifest: str
    manifest_sha256: str
    ledger: str
    ledger_sha256: str
    result: str
    verifier: str
    verification: str
    row_count: int
    row_id_field: str
    endpoint_field: str
    row_ids_sha256: str
    row_hashes_sha256: str
    rows_sha256: str
    required_values: tuple[tuple[str, Any], ...]

    @property
    def commitment(self) -> dict[str, Any]:
        return {
            "row_count": self.row_count,
            "row_ids_sha256": self.row_ids_sha256,
            "row_hashes_sha256": self.row_hashes_sha256,
            "rows_sha256": self.rows_sha256,
        }


# A gate package and its DSU-eligible edge subledgers are deliberately
# separate.  A sealed G/H audit may lawfully register zero eligible edge
# rows; its coverage/disposition ledger must still be pinned and reclosed,
# but must never be coerced into an edge Channel.
@dataclass(frozen=True)
class GateAuditCoverage:
    exact_occurrence_pair_references: dict[
        tuple[str, str], list[dict[str, Any]]
    ]
    exact_R300D_single_row_references: dict[
        str, list[dict[str, Any]]
    ]
    census: dict[str, Any]


@dataclass(frozen=True)
class GateRegistration:
    name: str
    manifest: str
    manifest_sha256: str
    required_members: tuple[tuple[str, str], ...]
    result: str
    verification: str
    eligible_edge_channels: tuple[Channel, ...]
    coverage_loader: Callable[[], GateAuditCoverage]


def load_R300G_gate_coverage() -> GateAuditCoverage:
    pair_references: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = {}
    for row in validated_gzip_rows(
        R300G_LEDGER,
        "Round300G_explicit_outgoing_seam_exclusion_row_id",
        R300G_COMMITMENT,
    ):
        pair = tuple(
            row["canonical_unordered_Round294_registry_occurrence_ids"]
        )
        need(
            len(pair) == 2
            and pair[0] < pair[1]
            and pair not in pair_references
            and row["attachment_exclusion_reason"]
            == (
                "NO_ROUND220_ANCESTOR_INTERFACE__"
                "NO_STRICT_VOLUME_INTERSECTION__"
                "CLOSED_CONTACT_INSUFFICIENT"
            )
            and row["included_one_sided_owner_attachment_proved"]
            is False
            and row["eligible_for_component_DSU_application"] is False
            and row["selected_leaf_Round220_interface_count"] == 0
            and row["selected_origin_Round220_interface_count"] == 0,
            "R300G exact fail-closed pair disposition",
        )
        for field in (
            "formal_DSU_rank_reduction_credit",
            "formal_component_edge_credit",
            "formal_component_union_credit",
            "formal_fibre_credit",
            "formal_global_disposition_credit",
            "formal_maximality_credit",
            "formal_occurrence_identity_collapse_credit",
            "formal_seam_edge_credit",
        ):
            need(row[field] == 0, "R300G strict zero:" + field)
        pair_references[pair] = [{
            "gate": "R300G",
            "provenance_kind": "AUDITED_FAIL_CLOSED_NO_EDGE",
            "gate_evidence_row_id":
                row[
                    "Round300G_explicit_outgoing_seam_exclusion_row_id"
                ],
            "gate_evidence_row_sha256": row["row_sha256"],
            "source_R300A_canonical_pair_row_id":
                row["source_Round300A_canonical_occurrence_pair_row_id"],
            "source_R300A_canonical_pair_row_sha256":
                row[
                    "source_Round300A_canonical_occurrence_pair_row_sha256"
                ],
            "source_R295A_physical_incidence_binding_row_id":
                row["source_Round295A_physical_incidence_binding_row_id"],
            "source_R295A_physical_incidence_binding_row_sha256":
                row[
                    "source_Round295A_physical_incidence_binding_row_sha256"
                ],
            "attachment_exclusion_reason":
                row["attachment_exclusion_reason"],
        }]
    need(len(pair_references) == 128, "R300G exact 128 pair coverage")
    return GateAuditCoverage(
        exact_occurrence_pair_references=pair_references,
        exact_R300D_single_row_references={},
        census={
            "exact_pair_count": len(pair_references),
            "eligible_edge_row_count": 0,
            "disposition": "AUDITED_FAIL_CLOSED_NO_EDGE",
        },
    )


def load_R300H_gate_coverage() -> GateAuditCoverage:
    pair_references: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = {}
    pair_tranches: Counter[str] = Counter()
    pair_source_rows: set[str] = set()
    for row in validated_gzip_rows(
        R300H_PAIR_LEDGER,
        "Round300H_enriched_pair_disposition_row_id",
        R300H_PAIR_COMMITMENT,
    ):
        pair = tuple(
            row["canonical_unordered_Round294_registry_occurrence_ids"]
        )
        tranche = row["disposition_tranche"]
        source_row_id = row["source_Round300D_pair_row_id"]
        need(
            len(pair) == 2
            and pair[0] < pair[1]
            and pair not in pair_references
            and tranche in {
                "GRAPH_TRANS_ANALYTIC_BOUNDARY_ONLY",
                "OWNER_POLICY_INCIDENCE_ONLY",
            }
            and source_row_id not in pair_source_rows
            and PIN_RE.fullmatch(
                row["source_Round300D_pair_row_sha256"]
            ) is not None
            and row["eligible_for_component_DSU_application"] is False
            and row["included_stratum_two_attachment_lemma_pinned"] is False
            and row["direct_formal_lineage_hit_count"] == 0
            and row[
                "owner_child_or_origin_to_Round266_root_lineage_count"
            ] == 0
            and row[
                "prior_Round300C_E_F_component_edge_endpoint_hit_count"
            ] == 0,
            "R300H exact fail-closed enriched-pair disposition",
        )
        for field in (
            "formal_DSU_rank_reduction_credit",
            "formal_component_edge_credit",
            "formal_component_quotient_credit",
            "formal_component_union_credit",
            "formal_fibre_credit",
            "formal_global_disposition_credit",
            "formal_maximality_credit",
            "formal_occurrence_identity_collapse_credit",
            "formal_official_key_merge_credit",
            "formal_seam_edge_credit",
        ):
            need(row[field] == 0, "R300H pair strict zero:" + field)
        if tranche == "GRAPH_TRANS_ANALYTIC_BOUNDARY_ONLY":
            need(
                row["transverse_analytic_boundary_present"] is True
                and row["transverse_owner_status"]
                == (
                    "ANALYTIC_BOUNDARY_STRATUM__"
                    "NO_ADJACENT_TUBE_DEDUP_CREDIT"
                )
                and row["t0_owner_policy_cells_present"] is False,
                "R300H graph/trans analytic-boundary exclusion",
            )
        else:
            need(
                row["t0_owner_policy_cells_present"] is True
                and row["owner_rectangles_exactly_cover_graph_leaf_base"]
                is True,
                "R300H owner-policy incidence-only exclusion",
            )
        pair_source_rows.add(source_row_id)
        pair_tranches[tranche] += 1
        pair_references[pair] = [{
            "gate": "R300H",
            "provenance_kind": "AUDITED_FAIL_CLOSED_NO_EDGE",
            "gate_evidence_row_id":
                row["Round300H_enriched_pair_disposition_row_id"],
            "gate_evidence_row_sha256": row["row_sha256"],
            "source_Round300D_pair_row_id": source_row_id,
            "source_Round300D_pair_row_sha256":
                row["source_Round300D_pair_row_sha256"],
            "disposition_tranche": tranche,
            "formal_disposition": row["formal_disposition"],
        }]
    need(
        len(pair_references) == 144
        and pair_tranches == {
            "GRAPH_TRANS_ANALYTIC_BOUNDARY_ONLY": 56,
            "OWNER_POLICY_INCIDENCE_ONLY": 88,
        },
        "R300H exact 56+88 pair coverage",
    )

    single_references: dict[str, list[dict[str, Any]]] = {}
    single_dispositions: Counter[str] = Counter()
    for row in validated_gzip_rows(
        R300H_SINGLE_LEDGER,
        "Round300H_single_target_disposition_row_id",
        R300H_SINGLE_COMMITMENT,
    ):
        source_row_id = row["source_Round300D_single_row_id"]
        source_row_sha256 = row["source_Round300D_single_row_sha256"]
        disposition = row["formal_disposition"]
        preserved = row["preserved_Round266_provenance"]
        need(
            source_row_id not in single_references
            and PIN_RE.fullmatch(source_row_sha256) is not None
            and row["canonical_two_target_incidence_edge_issued"] is False
            and row["eligible_for_component_DSU_application"] is False
            and row[
                "direct_formal_owner_root_attachment_lineage_count"
            ] == 0
            and row[
                "prior_Round300C_E_F_component_edge_endpoint_hit_count"
            ] == 0
            and type(row["target_Round294_registry_occurrence_id"]) is str
            and disposition in {
                "RECLOSED_EXISTING_ROUND266_OCCURRENCE_ROOT__ZERO_NEW_EDGE",
                (
                    "EXCLUDED__UNIQUE_TARGET_ASSIGNMENT_HAS_NO_FORMAL_"
                    "OWNER_ROOT_ATTACHMENT_LINEAGE"
                ),
            },
            "R300H exact single-target disposition",
        )
        for field in (
            "formal_DSU_rank_reduction_credit",
            "formal_component_edge_credit",
            "formal_component_quotient_credit",
            "formal_component_union_credit",
            "formal_fibre_credit",
            "formal_global_disposition_credit",
            "formal_maximality_credit",
            "formal_occurrence_identity_collapse_credit",
            "formal_official_key_merge_credit",
            "formal_seam_edge_credit",
        ):
            need(row[field] == 0, "R300H single strict zero:" + field)
        if disposition.startswith("RECLOSED_EXISTING_"):
            need(
                type(preserved) is dict
                and PIN_RE.fullmatch(
                    preserved[
                        "Round266_component_frontier_row_sha256"
                    ]
                ) is not None
                and PIN_RE.fullmatch(
                    preserved[
                        "Round266_expanded_occurrence_frontier_row_sha256"
                    ]
                ) is not None,
                "R300H preserved single exact Round266 provenance",
            )
        else:
            need(
                preserved is None,
                "R300H new single has no invented Round266 provenance",
            )
        single_dispositions[disposition] += 1
        single_references[source_row_id] = [{
            "gate": "R300H",
            "provenance_kind": "AUDITED_FAIL_CLOSED_NO_EDGE",
            "gate_evidence_row_id":
                row["Round300H_single_target_disposition_row_id"],
            "gate_evidence_row_sha256": row["row_sha256"],
            "source_Round300D_single_row_id": source_row_id,
            "source_Round300D_single_row_sha256": source_row_sha256,
            "target_Round294_registry_entry_kind":
                row["target_Round294_registry_entry_kind"],
            "target_Round294_registry_occurrence_id":
                row["target_Round294_registry_occurrence_id"],
            "witness_kind": row["witness_kind"],
            "formal_disposition": disposition,
            "preserved_Round266_provenance": preserved,
        }]
    need(
        len(single_references) == 1_600
        and single_dispositions == {
            "RECLOSED_EXISTING_ROUND266_OCCURRENCE_ROOT__ZERO_NEW_EDGE":
                1_408,
            (
                "EXCLUDED__UNIQUE_TARGET_ASSIGNMENT_HAS_NO_FORMAL_"
                "OWNER_ROOT_ATTACHMENT_LINEAGE"
            ): 192,
        },
        "R300H exact 1408+192 single-target coverage",
    )

    empty_rows = list(validated_gzip_rows(
        R300H_ELIGIBLE_LEDGER,
        "Round300H_eligible_component_edge_row_id",
        R300H_EMPTY_EDGE_COMMITMENT,
    ))
    need(not empty_rows, "R300H explicit empty eligible edge subledger")
    result = read_json(R300H_RESULT)
    need(
        result["status"]
        == (
            "PASS_ROUND300H_ZERO_ELIGIBLE_COMPONENT_EDGES__"
            "144_ENRICHED_PAIRS_AND_1600_SINGLES_EXHAUSTED"
        )
        and result["disposition_census"] == {
            "GRAPH_TRANS_ONLY_excluded_count": 56,
            "NEW_SINGLE_excluded_count": 192,
            "OWNER_POLICY_excluded_count": 88,
            "PRESERVED_SINGLE_reclosed_count": 1_408,
            "eligible_component_edge_count": 0,
        },
        "R300H result census agrees with exact ledgers",
    )
    return GateAuditCoverage(
        exact_occurrence_pair_references=pair_references,
        exact_R300D_single_row_references=single_references,
        census={
            "exact_pair_count": len(pair_references),
            "pair_disposition_tranche_histogram":
                dict(sorted(pair_tranches.items())),
            "exact_single_target_count": len(single_references),
            "single_formal_disposition_histogram":
                dict(sorted(single_dispositions.items())),
            "eligible_edge_row_count": 0,
        },
    )


# Every entry here is a formal, DSU-eligible edge ledger.  Package-level gate
# closure is tracked independently below.
CHANNELS: tuple[Channel, ...] = (
    Channel(
        "R297_ORDINARY_FACE",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
        "manifest.sha256",
        "1feecefa897c5320eadc006509ba6bde84cdbf692dfaddd024472b93c13c38c0",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
        "edge_ledger.json.gz",
        "18a20b4679a8a3e94ccaf1b511694220cad1bc92e1590ded4585ae3735547371",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
        "result.json",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
        "verifier.py",
        "cm2_round297_source_g_ordinary_face_occurrence_edge_promotion_"
        "verification.json",
        330_724,
        "Round297_ordinary_face_occurrence_edge_row_id",
        "exact_occurrence_endpoint_pair",
        "6ee71aba6c26953b7b368dc89d985468fb7410e6d5a47b0300c2962ceca045a6",
        "02586985662d453791f1461d71c15cca7e5e109b25025a8eec5f5c7c441c937d",
        "52a6ee955af86ac186824c23d27c0372d3c14792839f372620d311c9f144dbe0",
        (
            ("formal_ordinary_component_edge_witness_credit", 1),
            ("occurrence_endpoint_pair_is_nonself", True),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    Channel(
        "R296_TRUE_SEAM",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
        "manifest.sha256",
        "f7786b9cdec45cb381ec46489eb44b0365b8ee43d81ae9a9611cb2dcdee7fb59",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
        "edge_ledger.json.gz",
        "1b57b10fac9317e1609fb8858972011165bd95e5b1b687604edd6c8ad7139ef7",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
        "result.json",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
        "verifier.py",
        "cm2_round296_source_g_true_seam_occurrence_edge_ledger_closure_"
        "verification.json",
        48_444,
        "Round296_true_seam_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        "d6ad370122651272a384f4fc8f48ca8b3e6a6b3f2cd9c9f03a073c1d207f853a",
        "608bf8140bcb77b950f00628804c649e82ebdb1055816df2ae32f68b3e321a06",
        "e989828d774a08694404fe678c4ae74dc199f8f5cdf4d398dc755f5ff4b0561f",
        (
            ("formal_true_seam_edge_credit", 1),
            ("occurrence_identity_collapsed", False),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    Channel(
        "R299C_SIGNED_FACE",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_"
        "manifest.sha256",
        "62e04cdd7f9c3d2fb865be0a999e1ce5ed1de435151a1b7bb5bba0176709b9b3",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_"
        "canonical_occurrence_edge_pairs.json.gz",
        "e63f164bf9cc559ec8d3a2895e66493933b43b90f1ad3b163dfb41e12bb04df1",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_"
        "result.json",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_"
        "verifier.py",
        "cm2_round299c_source_g_r292_signed_support_face_edge_promotion_"
        "verification.json",
        25_452,
        "Round299C_canonical_signed_face_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        "56c09af202b36a867f1cc9893c968ab231a952fdea85cafdde999be4ebcba70d",
        "138395a9a63f16623f2df4ff3656d82c744a522de23f20fc728c925baa833dc6",
        "14c6f44ab989a075a46de4c842b14cad9dff211373b52d0be41c8083620c3c87",
        (
            ("formal_component_edge_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    Channel(
        "R300B_COMPLETE_FACE",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_"
        "inventory_closure_manifest.sha256",
        "6208c4bfd8b147f06ffb735d4b5621faff22585831b5f19d48e8125514ac4a6b",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_"
        "inventory_closure_canonical_novel_occurrence_edge_pairs.json.gz",
        "c3d1e604ed0e1256789c239b65d22546035fd3bd333dd11bfb907e221c3cec9e",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_"
        "inventory_closure_result.json",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_"
        "inventory_closure_verifier.py",
        "cm2_round300b_source_g_registry_boundary_and_complete_r275_face_"
        "inventory_closure_verification.json",
        10_416,
        "Round300B_canonical_novel_occurrence_edge_row_id",
        "unordered_formal_occurrence_endpoint_pair",
        "5b3c7f446db963d7b763ffebf5d596c1fda92e3d31e573fd3fd95b1c855b5119",
        "cbd960748bfed1d31e31cbad053c3a0c11d8264fe043e35fe85350c54bf8f648",
        "cbc1cf8de07559c50db2cd84920379c9e0bd839c22bf9be3267784adc801c808",
        (
            ("formal_component_edge_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
            ("all_prior_channel_memberships_false", True),
        ),
    ),
    Channel(
        "R300C_POSITIVE_VOLUME",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
        "volume_edge_promotion_manifest.sha256",
        "cd327de2702ac209b0b0a03d09b3744596a901c2d65794dd86231d31a0be3503",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
        "volume_edge_promotion_edge_ledger.json.gz",
        "8c9ed8b09e994a00ca3ca4906c35b454523383b7d488f66e7a082dbbd4b1fcec",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
        "volume_edge_promotion_result.json",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
        "volume_edge_promotion_verifier.py",
        "cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_"
        "volume_edge_promotion_verification.json",
        6_314,
        "Round300C_virtual_occurrence_positive_volume_edge_row_id",
        "canonical_component_edge_endpoint_pair",
        "f35b03655c3fb6986d4798b1b9a2858cba915d1279d393396315358ef0632c65",
        "2f4c62e37a58c457bdc22c3271bce1229acfda942f46ec38341a7fd693897efb",
        "41716c0e35152d8e735310a2efdb55cbe7cf5813c8f94dc0ee4f88525bcd0a5b",
        (
            ("formal_positive_volume_component_edge_witness_credit", 1),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    Channel(
        "R300E_HALF_OPEN_OWNER",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
        "promotion_manifest.sha256",
        "4e6c4eec1af04a907285d41395aeef63e911b3b5486db91b33a95fa62e45177a",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
        "promotion_all_edge_ledger.json.gz",
        "4aa7ae76d984d15b345d5d6805ec4f06a47e30a46fff1315f346e81f1f17122f",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
        "promotion_result.json",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
        "promotion_verifier.py",
        "cm2_round300e_source_g_r248_half_open_owner_lower_component_edge_"
        "promotion_verification.json",
        12_992,
        "Round300E_half_open_owner_component_edge_row_id",
        "canonical_component_edge_endpoint_pair",
        "d2a8a525bd593f1e9cedcd3306b84b87ba6ccc88a4878d18572c32dca43f2272",
        "de692835ee6333a65e554a4f1567186995b5d3c80adfd374227fc82e096fc4c7",
        "76bfbac5c9706416be4ed1e4df3104006dc26cb68cf5e8f23c5b482aa44ac20a",
        (
            ("formal_half_open_owner_component_edge_credit", 1),
            ("eligible_for_component_DSU_application", True),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
    Channel(
        "R300F_R245_HALF_OPEN_OWNER",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_"
        "manifest.sha256",
        "811656ed9160b622014a94901a1e08c7d3e6313db08f86d65ae01afefb49bbeb",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_"
        "ledger.json.gz",
        "1f958f9f3e3aff7327d897b39851f2d2d030d820e00859d302241702613cae1f",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_"
        "result.json",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_"
        "verifier.py",
        "cm2_round300f_source_g_r245_half_open_owner_sheet_attachment_"
        "verification.json",
        264,
        "Round300F_R245_half_open_owner_attachment_row_id",
        "canonical_component_edge_endpoint_pair",
        "e836f0e338cd43b19cebc718fe5ba60d8e5a313bcf8aac9eea72b8bfc8246c22",
        "58fc944871aaba4d49708359d59a6c996953068cef3d59e7a1d3719179944180",
        "6be4a94b83fb5b1b61a93bf84ca2b61fb1f9dfd9cbf4425b5dbb6a0dcdc9f6c2",
        (
            ("formal_half_open_owner_component_edge_witness_credit", 1),
            ("eligible_for_component_DSU_application", True),
            ("Round300A_prior_explicit_graph_zero_pair_present", False),
            ("Round300A_two_endpoint_union_credit", 0),
            ("shadow_component_edge_witness_credit", 0),
            ("formal_occurrence_identity_collapse_credit", 0),
            ("formal_DSU_rank_reduction_credit", 0),
        ),
    ),
)

# Append-only gate registry.  A final Round301 run is forbidden until every
# entry is replaced by a sealed GateRegistration.  The registered tuple of
# eligible edge channels may be empty, but the gate seal and its full
# coverage/disposition evidence may not be omitted.
PENDING_GATE_REGISTRATIONS: dict[str, GateRegistration | None] = {
    "R300G": GateRegistration(
        name="R300G",
        manifest=R300G_MANIFEST,
        manifest_sha256=
            "ce700bdc855406396ae89aa936d07c506057d7dfab806d064a91c0e08b0d8a4c",
        required_members=(
            (
                R300G_LEDGER,
                "84b4e855cd95867758cd87a88f0ef55b712218999166796712495d70602bb61b",
            ),
            (
                R300G_RESULT,
                "5693f64262623dccbdc0138edc7dc876b06b2822f552eee26ac580c27f861c1c",
            ),
            (
                R300G_VERIFIER,
                "2b3a241ed3769273113d17f3907007da57626f7eb3e5f7b75eb107b833b1f9a9",
            ),
            (
                R300G_VERIFICATION,
                "2416d2efe04935fddc615c5542b1f0f0c56411111152d5e27d1021c59d8782ff",
            ),
        ),
        result=R300G_RESULT,
        verification=R300G_VERIFICATION,
        eligible_edge_channels=(),
        coverage_loader=load_R300G_gate_coverage,
    ),
    "R300H": GateRegistration(
        name="R300H",
        manifest=R300H_MANIFEST,
        manifest_sha256=
            "7cb31452e1f22c22d3d5dd7552f49c86526e60dba6cdedeb13888f4ff41bf71e",
        required_members=(
            (
                R300H_PRODUCER,
                "3d93a3a13b494fbf136916827e63fb5861960cec9de8dcb4facceb16c5f0b952",
            ),
            (
                R300H_PAIR_LEDGER,
                "29261a9a6b366252492c703b01714236c3a80f759fa540412f291a3bf586c4c9",
            ),
            (
                R300H_SINGLE_LEDGER,
                "fba21c8297caca43eb1f9ff5dea5af258b7893550cc3d3dd97abf3be88acc8e7",
            ),
            (
                R300H_ELIGIBLE_LEDGER,
                "d3dc3a8fc94ea2f7c8bbf08b87eb663c102606e964e612334199e3bb32c8cdc2",
            ),
            (
                R300H_RESULT,
                "378546acee06a11dce5da9c41c5d15d739888e163e14bab5fb80ba8d92ffa56c",
            ),
            (
                R300H_VERIFIER,
                "eb545e912766993cb20a04a6ef2cfa8559a5a7ad474481bb3f55c8a036893c33",
            ),
            (
                R300H_ATTACKS,
                "aad9c2e077a4770aa16380d784fc1d6cb4e7d825d430000e58b9f1f97446cd15",
            ),
            (
                R300H_VERIFICATION,
                "7c06a189a642ba3068ea8e61a8170a7847fc4d5ae4260375af212773b18409bb",
            ),
            (
                R300H_REPORT,
                "77426faa4b9032be9604a4208782bd529c290acf6ac0633d3c47294236ca6dbb",
            ),
            (
                R300H_COLD_REPLAY,
                "1d1749ecf5d268b3a33088d7fd24af835cb7cf7fde99a670f849eb171d2d14fa",
            ),
        ),
        result=R300H_RESULT,
        verification=R300H_VERIFICATION,
        eligible_edge_channels=(),
        coverage_loader=load_R300H_gate_coverage,
    ),
}


@dataclass
class Member:
    member_id: str
    member_kind: str
    base_root: str
    official_key_id: str | None
    source_row_id: str
    source_row_sha256: str


@dataclass(frozen=True)
class Edge:
    channel: str
    source_row_id: str
    source_row_sha256: str
    left_endpoint: str
    right_endpoint: str
    left_base_root: str
    right_base_root: str


class DSU:
    def __init__(self, roots: Iterable[str]) -> None:
        self.parent = {root: root for root in roots}
        self.size = {root: 1 for root in self.parent}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        while parent != self.parent[parent]:
            parent = self.parent[parent]
        while item != parent:
            next_item = self.parent[item]
            self.parent[item] = parent
            item = next_item
        return parent

    def union(self, left: str, right: str) -> bool:
        a = self.find(left)
        b = self.find(right)
        if a == b:
            return False
        if (self.size[a], a) < (self.size[b], b):
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


def validate_foundation_boundary() -> None:
    for name, pin in FOUNDATION_MANIFEST_PINS.items():
        need(PIN_RE.fullmatch(pin) is not None, "manifest pin syntax")
        need(file_sha256(HERE / name) == pin, "foundation manifest pin")
    for name, pin in FOUNDATION_FILE_PINS.items():
        need(PIN_RE.fullmatch(pin) is not None, "file pin syntax")
        safe_file(HERE / name)
        need(file_sha256(HERE / name) == pin, "foundation file pin:" + name)
    selections = {
        R266_MANIFEST: [R266_CERTIFICATE, R266_VERIFICATION],
        R294_MANIFEST: [R294_REGISTRY, R294_RESULT, R294_VERIFICATION],
        R299A_MANIFEST: [R299A_LEDGER, R299A_RESULT, R299A_VERIFICATION],
    }
    for manifest, members in selections.items():
        entries = parse_manifest(manifest)
        for member in members:
            need(
                entries.get(member) == FOUNDATION_FILE_PINS[member],
                "foundation manifest selection:" + manifest + ":" + member,
            )
    for name, prefix in (
        (R266_VERIFICATION, "PASS"),
        (R294_VERIFICATION, "PASS_INDEPENDENT_CACHELESS_ROUND294"),
        (R299A_VERIFICATION, "PASS_INDEPENDENT_CACHELESS_ROUND299A"),
    ):
        need(read_json(name)["status"].startswith(prefix),
             "foundation verification:" + name)
    for name in (R294_RESULT, R299A_RESULT):
        check_result_self(read_json(name), name)


def validate_ineligible_source_boundary() -> None:
    packages = (
        (
            R300A_MANIFEST,
            (
                R300A_LEDGER,
                R300A_RESULT,
                R300A_VERIFIER,
                R300A_VERIFICATION,
            ),
        ),
        (
            R300D_MANIFEST,
            (
                R300D_LEDGER,
                R300D_RESULT,
                R300D_VERIFIER,
                R300D_VERIFICATION,
            ),
        ),
    )
    for manifest, members in packages:
        validate_manifest_selection(
            manifest,
            INELIGIBLE_PACKAGE_PINS[manifest],
            {
                member: INELIGIBLE_PACKAGE_PINS[member]
                for member in members
            },
        )
    for result_name, verification_name in (
        (R300A_RESULT, R300A_VERIFICATION),
        (R300D_RESULT, R300D_VERIFICATION),
    ):
        result = read_json(result_name)
        check_result_self(result, result_name)
        need(result["status"].startswith("PASS"), result_name + ":status")
        need(
            read_json(verification_name)["status"].startswith("PASS"),
            verification_name + ":status",
        )
    validate_manifest_selection(
        R300E_MANIFEST,
        R300E_MANIFEST_PIN,
        {R300E_WITNESS_LEDGER: R300E_WITNESS_LEDGER_PIN},
    )


def reconstruct_members() -> tuple[
    dict[str, Member], set[str], dict[str, Any]
]:
    members: dict[str, Member] = {}
    retained_roots: set[str] = set()
    kind_census: Counter[str] = Counter()

    def visit_member(row: dict[str, Any]) -> None:
        member_id = row["component_member_id"]
        root = row["post_Round266_quotient_component_id"]
        need(
            member_id not in members
            and row["member_identity_preserved"] is True
            and row["maximality_credit"] == 0
            and type(row["official_key_id"]) is str,
            "Round266 identity-preserved member",
        )
        members[member_id] = Member(
            member_id=member_id,
            member_kind=row["component_member_kind"],
            base_root=root,
            official_key_id=row["official_key_id"],
            source_row_id=
                row["post_Round266_component_member_frontier_row_id"],
            source_row_sha256=row["row_sha256"],
        )
        retained_roots.add(root)
        kind_census[row["component_member_kind"]] += 1

    stream_plain_table(
        R266_CERTIFICATE,
        "formal_post_Round266_component_member_frontier_ledger",
        "post_Round266_component_member_frontier_row_id",
        R266_MEMBER_COMMITMENT,
        visit_member,
    )
    need(
        len(members) == 259_752
        and len(retained_roots) == 63_224
        and kind_census == {
            "EXPANDED_OCCURRENCE": 126_468,
            "VALID_VIRTUAL_STRATUM": 133_284,
        },
        "Round266 complete member/root census",
    )

    root_keys: dict[str, str] = {}

    def visit_root(row: dict[str, Any]) -> None:
        root = row["post_Round266_quotient_component_id"]
        need(
            root in retained_roots
            and root not in root_keys
            and type(row["official_key_id"]) is str,
            "Round266 complete root row",
        )
        root_keys[root] = row["official_key_id"]

    stream_plain_table(
        R266_CERTIFICATE,
        "formal_post_Round266_component_frontier_ledger",
        "post_Round266_component_frontier_row_id",
        R266_ROOT_COMMITMENT,
        visit_root,
    )
    need(set(root_keys) == retained_roots, "Round266 root coverage")
    need(
        all(
            member.official_key_id == root_keys[member.base_root]
            for member in members.values()
        ),
        "Round266 member/root official-key consistency",
    )

    registry_kinds: Counter[str] = Counter()
    preserved_seen: set[str] = set()
    refined_sources: dict[str, tuple[str, str]] = {}
    new_roots: set[str] = set()
    old_keys = set(root_keys.values())

    def visit_registry(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        kind = row["registry_entry_kind"]
        registry_kinds[kind] += 1
        if kind == PRESERVED:
            member = members.get(occurrence)
            need(
                member is not None
                and member.member_kind == "EXPANDED_OCCURRENCE"
                and occurrence not in preserved_seen
                and member.official_key_id == row["official_key_id"],
                "Round294 exact preservation of Round266 occurrence member",
            )
            preserved_seen.add(occurrence)
            return
        need(occurrence not in members, "Round294 append-only new identity")
        if kind == R288:
            need(
                type(row["official_key_id"]) is str
                and type(row["official_key_ordinal"]) is int,
                "Round288 singleton key",
            )
            official_key: str | None = row["official_key_id"]
            old_keys.add(row["official_key_id"])
        else:
            need(
                kind == R292
                and row["official_key_id"] is None
                and row["official_key_ordinal"] is None,
                "Round292 prebinding key null",
            )
            official_key = None
            refined_sources[occurrence] = (
                row["Round294_occurrence_registry_row_id"],
                row["row_sha256"],
            )
        members[occurrence] = Member(
            member_id=occurrence,
            member_kind=kind,
            base_root=occurrence,
            official_key_id=official_key,
            source_row_id=row["Round294_occurrence_registry_row_id"],
            source_row_sha256=row["row_sha256"],
        )
        new_roots.add(occurrence)

    stream_gzip_rows(
        R294_REGISTRY,
        "Round294_occurrence_registry_row_id",
        R294_COMMITMENT,
        visit_registry,
    )
    need(
        len(preserved_seen) == 126_468
        and registry_kinds == {
            PRESERVED: 126_468,
            R288: 295_336,
            R292: 9_404,
        }
        and len(new_roots) == 304_740
        and len(old_keys) == 116,
        "Round294 append-only registry reconstruction",
    )

    binding_seen: set[str] = set()
    final_keys = set(old_keys)

    def visit_binding(row: dict[str, Any]) -> None:
        occurrence = row["registry_occurrence_id"]
        source = refined_sources.get(occurrence)
        member = members.get(occurrence)
        need(
            source is not None
            and member is not None
            and member.official_key_id is None
            and occurrence not in binding_seen
            and row["source_Round294_occurrence_registry_row_id"] == source[0]
            and row["source_Round294_occurrence_registry_row_sha256"]
            == source[1]
            and row["append_only_official_key_binding"] is True
            and row["occurrence_identity_preserved"] is True
            and row[
                "formal_refined_occurrence_official_key_binding_credit"
            ] == 1
            and row["raw_key_merge_credit"] == 0,
            "Round299A refined singleton final key",
        )
        member.official_key_id = row["official_key_id"]
        binding_seen.add(occurrence)
        final_keys.add(row["official_key_id"])

    stream_gzip_rows(
        R299A_LEDGER,
        "Round299A_refined_occurrence_official_key_binding_row_id",
        R299A_COMMITMENT,
        visit_binding,
    )
    base_roots = retained_roots | new_roots
    need(
        set(refined_sources) == binding_seen
        and len(members) == 564_492
        and len(base_roots) == 367_964
        and len(final_keys) == 124
        and all(member.official_key_id is not None for member in members.values()),
        "Round301 exact member/base-root/final-key universe",
    )
    return members, base_roots, {
        "member_count": len(members),
        "base_root_count": len(base_roots),
        "retained_Round266_member_count": 259_752,
        "retained_Round266_root_count": len(retained_roots),
        "new_Round294_singleton_member_and_root_count": len(new_roots),
        "final_official_key_count": len(final_keys),
        "unkeyed_member_count": 0,
        "member_kind_histogram": dict(sorted(
            Counter(member.member_kind for member in members.values()).items()
        )),
    }


def package_members(channel: Channel) -> dict[str, str]:
    entries = parse_manifest(channel.manifest)
    required = {
        channel.ledger: channel.ledger_sha256,
        channel.result: entries.get(channel.result, ""),
        channel.verifier: entries.get(channel.verifier, ""),
        channel.verification: entries.get(channel.verification, ""),
    }
    need(all(PIN_RE.fullmatch(value) is not None for value in required.values()),
         "channel manifest required members:" + channel.name)
    return required


def validate_channel_package(channel: Channel) -> None:
    selected = package_members(channel)
    validate_manifest_selection(
        channel.manifest, channel.manifest_sha256, selected
    )
    result = read_json(channel.result)
    check_result_self(result, channel.name)
    verification = read_json(channel.verification)
    need(result["status"].startswith("PASS"), "channel result:" + channel.name)
    need(
        verification["status"].startswith("PASS"),
        "channel verification:" + channel.name,
    )


def validate_gate_package(registration: GateRegistration) -> None:
    selected = dict(registration.required_members)
    need(
        registration.result in selected
        and registration.verification in selected,
        "gate result/verification explicitly pinned:" + registration.name,
    )
    validate_manifest_selection(
        registration.manifest,
        registration.manifest_sha256,
        selected,
    )
    result = read_json(registration.result)
    check_result_self(result, registration.name)
    verification = read_json(registration.verification)
    need(
        result["status"].startswith("PASS")
        and verification["status"].startswith("PASS"),
        "gate result and verification:" + registration.name,
    )


def collect_edges(
    channels: Iterable[Channel],
    members: dict[str, Member],
    base_roots: set[str],
) -> tuple[list[Edge], dict[str, Any]]:
    output: list[Edge] = []
    channel_rows: dict[str, int] = {}
    channel_unique_pairs: dict[str, int] = {}

    def project(endpoint: str) -> str:
        if endpoint in base_roots:
            return endpoint
        member = members.get(endpoint)
        need(member is not None, "edge endpoint in complete member universe")
        return member.base_root

    for channel in channels:
        validate_channel_package(channel)
        seen_pairs: set[tuple[str, str]] = set()
        before = len(output)

        def visit(row: dict[str, Any]) -> None:
            for field, expected in channel.required_values:
                need(
                    row.get(field) == expected,
                    channel.name + ":legal edge field:" + field,
                )
            endpoints = row[channel.endpoint_field]
            need(
                type(endpoints) is list
                and len(endpoints) == 2
                and endpoints == sorted(endpoints)
                and endpoints[0] != endpoints[1],
                channel.name + ":canonical nonself endpoint pair",
            )
            left_root = project(endpoints[0])
            right_root = project(endpoints[1])
            seen_pairs.add(tuple(endpoints))
            output.append(Edge(
                channel=channel.name,
                source_row_id=row[channel.row_id_field],
                source_row_sha256=row["row_sha256"],
                left_endpoint=endpoints[0],
                right_endpoint=endpoints[1],
                left_base_root=left_root,
                right_base_root=right_root,
            ))

        stream_gzip_rows(
            channel.ledger,
            channel.row_id_field,
            channel.commitment,
            visit,
        )
        channel_rows[channel.name] = len(output) - before
        channel_unique_pairs[channel.name] = len(seen_pairs)
        need(
            channel_rows[channel.name] == channel.row_count,
            "channel complete edge rows:" + channel.name,
        )
    return output, {
        "channel_edge_row_count": channel_rows,
        "channel_unique_endpoint_pair_count": channel_unique_pairs,
        "total_sealed_legal_edge_row_count": len(output),
    }


def exact_stronger_edge_provenance(
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    channel_by_name = {channel.name: channel for channel in CHANNELS}
    b_channel = channel_by_name["R300B_COMPLETE_FACE"]
    e_channel = channel_by_name["R300E_HALF_OPEN_OWNER"]
    f_channel = channel_by_name["R300F_R245_HALF_OPEN_OWNER"]
    for channel in (b_channel, e_channel, f_channel):
        validate_channel_package(channel)

    e_edge_by_witness: dict[str, dict[str, str]] = {}
    for row in validated_gzip_rows(
        e_channel.ledger,
        e_channel.row_id_field,
        e_channel.commitment,
    ):
        witness_id = row["source_half_open_owner_witness_row_id"]
        need(
            witness_id not in e_edge_by_witness,
            "R300E witness has one exact legal edge",
        )
        e_edge_by_witness[witness_id] = {
            "legal_edge_channel": e_channel.name,
            "legal_edge_source_row_id": row[e_channel.row_id_field],
            "legal_edge_source_row_sha256": row["row_sha256"],
        }

    output: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in validated_gzip_rows(
        b_channel.ledger,
        b_channel.row_id_field,
        b_channel.commitment,
    ):
        pair = tuple(row[b_channel.endpoint_field])
        need(
            len(pair) == 2 and pair[0] < pair[1],
            "R300B exact canonical occurrence edge pair",
        )
        output[pair].append({
            "gate": "R300B",
            "provenance_kind": "RECLOSED_BY_STRONGER_LEGAL_EDGE",
            "gate_evidence_row_id": row[b_channel.row_id_field],
            "gate_evidence_row_sha256": row["row_sha256"],
            "legal_edge_channel": b_channel.name,
            "legal_edge_source_row_id": row[b_channel.row_id_field],
            "legal_edge_source_row_sha256": row["row_sha256"],
        })

    seen_e_witnesses: set[str] = set()
    for row in validated_gzip_rows(
        R300E_WITNESS_LEDGER,
        "Round300E_half_open_owner_component_edge_witness_row_id",
        R300E_WITNESS_COMMITMENT,
    ):
        witness_id = row[
            "Round300E_half_open_owner_component_edge_witness_row_id"
        ]
        edge = e_edge_by_witness.get(witness_id)
        need(
            edge is not None
            and witness_id not in seen_e_witnesses
            and row["eligible_for_component_DSU_application"] is True
            and row[
                "formal_half_open_owner_component_edge_witness_credit"
            ] == 1,
            "R300E exact witness to legal edge closure",
        )
        seen_e_witnesses.add(witness_id)
        pair = tuple(sorted((
            row["owner_Round294_registry_occurrence_id"],
            row["excluded_present_side_Round294_registry_occurrence_id"],
        )))
        output[pair].append({
            "gate": "R300E",
            "provenance_kind": "RECLOSED_BY_STRONGER_LEGAL_EDGE",
            "gate_evidence_row_id": witness_id,
            "gate_evidence_row_sha256": row["row_sha256"],
            **edge,
        })
    need(
        seen_e_witnesses == set(e_edge_by_witness),
        "R300E complete witness-to-edge bijection",
    )

    for row in validated_gzip_rows(
        f_channel.ledger,
        f_channel.row_id_field,
        f_channel.commitment,
    ):
        pair = tuple(sorted((
            row["Round294_owner_occurrence_id"],
            row["Round294_shadow_occurrence_id"],
        )))
        output[pair].append({
            "gate": "R300F",
            "provenance_kind": "RECLOSED_BY_STRONGER_LEGAL_EDGE",
            "gate_evidence_row_id": row[f_channel.row_id_field],
            "gate_evidence_row_sha256": row["row_sha256"],
            "legal_edge_channel": f_channel.name,
            "legal_edge_source_row_id": row[f_channel.row_id_field],
            "legal_edge_source_row_sha256": row["row_sha256"],
        })

    for values in output.values():
        values.sort(key=lambda value: (
            value["gate"],
            value["gate_evidence_row_id"],
        ))
    return output


def complete_exact_gate_provenance() -> tuple[
    dict[tuple[str, str], list[dict[str, Any]]],
    dict[str, list[dict[str, Any]]],
    dict[str, Any],
]:
    pair_references = exact_stronger_edge_provenance()
    single_references: dict[str, list[dict[str, Any]]] = defaultdict(list)
    gate_census: dict[str, Any] = {}
    for name, registration in PENDING_GATE_REGISTRATIONS.items():
        if registration is None:
            continue
        validate_gate_package(registration)
        coverage = registration.coverage_loader()
        gate_census[name] = coverage.census
        for pair, references in (
            coverage.exact_occurrence_pair_references.items()
        ):
            need(
                type(pair) is tuple
                and len(pair) == 2
                and pair[0] < pair[1],
                "gate coverage canonical exact occurrence pair:" + name,
            )
            pair_references[pair].extend(references)
        for source_row_id, references in (
            coverage.exact_R300D_single_row_references.items()
        ):
            need(
                type(source_row_id) is str and references,
                "gate coverage exact R300D single row:" + name,
            )
            single_references[source_row_id].extend(references)
    for references in pair_references.values():
        references.sort(key=lambda value: (
            value["gate"],
            value["gate_evidence_row_id"],
        ))
    for references in single_references.values():
        references.sort(key=lambda value: (
            value["gate"],
            value["gate_evidence_row_id"],
        ))
    return pair_references, dict(single_references), gate_census


def exact_prior_channel_pair_sets(
    edges: list[Edge],
) -> dict[str, set[tuple[str, str]]]:
    names = {
        "R296_TRUE_SEAM",
        "R297_ORDINARY_FACE",
        "R299C_SIGNED_FACE",
        "R300C_POSITIVE_VOLUME",
    }
    output: dict[str, set[tuple[str, str]]] = {
        name: set() for name in names
    }
    if edges:
        for edge in edges:
            if edge.channel in names:
                output[edge.channel].add(
                    (edge.left_endpoint, edge.right_endpoint)
                )
        return output
    for channel in CHANNELS:
        if channel.name not in names:
            continue
        validate_channel_package(channel)
        for row in validated_gzip_rows(
            channel.ledger,
            channel.row_id_field,
            channel.commitment,
        ):
            pair = row[channel.endpoint_field]
            output[channel.name].add((pair[0], pair[1]))
    return output


def exact_R300A_pair_set() -> set[tuple[str, str]]:
    output: set[tuple[str, str]] = set()
    for row in validated_gzip_rows(
        R300A_LEDGER,
        "Round300A_canonical_occurrence_pair_row_id",
        R300A_CANONICAL_PAIR_COMMITMENT,
        table="canonical_occurrence_pair_rows",
    ):
        pair = tuple(
            row["canonical_unordered_Round294_registry_occurrence_ids"]
        )
        need(pair not in output, "R300A exact pair set uniqueness")
        output.add(pair)
    return output


def exact_R300B_face_coverage_for_pairs(
    target_pairs: set[tuple[str, str]],
) -> tuple[
    dict[tuple[str, str], list[dict[str, Any]]],
    dict[tuple[str, str], list[dict[str, Any]]],
]:
    b_channel = next(
        channel
        for channel in CHANNELS
        if channel.name == "R300B_COMPLETE_FACE"
    )
    validate_manifest_selection(
        b_channel.manifest,
        b_channel.manifest_sha256,
        {R300B_FACE_INVENTORY: R300B_FACE_INVENTORY_PIN},
    )
    accepted: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    rejected: dict[
        tuple[str, str], list[dict[str, Any]]
    ] = defaultdict(list)
    for row in pinned_gzip_rows_without_semantic_rehash(
        R300B_FACE_INVENTORY,
        R300B_FACE_INVENTORY_PIN,
        "Round300B_face_inventory_row_id",
        R300B_FACE_INVENTORY_COMMITMENT["row_count"],
    ):
        decision = row["decision"]
        need(
            decision.startswith("ACCEPT_")
            or decision.startswith("REJECT_"),
            "R300B complete face decision",
        )
        left = row["left_formal_occurrence_endpoints"]
        right = row["right_formal_occurrence_endpoints"]
        need(type(left) is list and type(right) is list,
             "R300B exact endpoint lists")
        pairs: set[tuple[str, str]] = set()
        if decision.startswith("ACCEPT_"):
            # A positive patch plus two corridors applies to every exact
            # endpoint cross-product on the accepted face.
            for first in left:
                for second in right:
                    if first != second:
                        pairs.add(tuple(sorted((first, second))))
            destination = accepted
            provenance_kind = (
                "FACE_ACCEPTED_WITH_EXACT_POSITIVE_PATCH_AND_TWO_CORRIDORS"
            )
        else:
            # A rejected multi-endpoint face does not exclude its raw source
            # cross-product.  Only the explicit exact pair field is a
            # pair-specific no-edge disposition.
            explicit = row[
                "unordered_nonself_formal_occurrence_endpoint_pair"
            ]
            if explicit is not None:
                pairs.add(tuple(explicit))
            destination = rejected
            provenance_kind = "AUDITED_FAIL_CLOSED_NO_EDGE"
        for pair in pairs & target_pairs:
            destination[pair].append({
                "gate": "R300B_FACE_INVENTORY",
                "provenance_kind": provenance_kind,
                "gate_evidence_row_id":
                    row["Round300B_face_inventory_row_id"],
                "gate_evidence_row_sha256": row["row_sha256"],
                "face_decision": decision,
            })
    for mapping in (accepted, rejected):
        for references in mapping.values():
            references.sort(key=lambda item: item["gate_evidence_row_id"])
    return dict(accepted), dict(rejected)


def audit_ineligible_sources(
    edges: list[Edge],
    members: dict[str, Member],
    base_roots: set[str],
    pending_gate_seals: list[str],
    exact_provenance_override: (
        dict[tuple[str, str], list[dict[str, Any]]] | None
    ) = None,
    single_provenance_override: (
        dict[str, list[dict[str, Any]]] | None
    ) = None,
    gate_census_override: dict[str, Any] | None = None,
    a_face_accepted_override: (
        dict[tuple[str, str], list[dict[str, Any]]] | None
    ) = None,
    a_face_rejected_override: (
        dict[tuple[str, str], list[dict[str, Any]]] | None
    ) = None,
) -> dict[str, Any]:
    """Reclose every R300-A/D row without ever feeding one to the DSU.

    A stronger E/F/G/H proof may happen to cover the same projected pair.
    That fact is recorded as provenance only: the legal edge remains the
    stronger channel's own pinned row, never the R300-A/D row.
    """

    validate_ineligible_source_boundary()

    del members, base_roots
    if (
        exact_provenance_override is None
        or single_provenance_override is None
        or gate_census_override is None
    ):
        exact_provenance, single_provenance, gate_census = (
            complete_exact_gate_provenance()
        )
    else:
        exact_provenance = exact_provenance_override
        single_provenance = single_provenance_override
        gate_census = gate_census_override
    prior_pair_sets = exact_prior_channel_pair_sets(edges)
    if (
        a_face_accepted_override is None
        or a_face_rejected_override is None
    ):
        a_target_pairs = exact_R300A_pair_set()
        a_face_accepted, a_face_rejected = (
            exact_R300B_face_coverage_for_pairs(a_target_pairs)
        )
    else:
        a_face_accepted = a_face_accepted_override
        a_face_rejected = a_face_rejected_override

    d_disposition: Counter[str] = Counter()
    d_seen_occurrence_pairs: set[tuple[str, str]] = set()

    def visit_d_incidence(row: dict[str, Any]) -> None:
        occurrence_pair = row[
            "canonical_unordered_Round294_registry_occurrence_ids"
        ]
        need(
            type(occurrence_pair) is list
            and len(occurrence_pair) == 2
            and occurrence_pair == sorted(occurrence_pair)
            and occurrence_pair[0] != occurrence_pair[1]
            and tuple(occurrence_pair) not in d_seen_occurrence_pairs,
            "R300D unique canonical occurrence pair",
        )
        d_seen_occurrence_pairs.add(tuple(occurrence_pair))
        for field in (
            "formal_DSU_rank_reduction_credit",
            "formal_Jx_Jy_same_point_glue_credit",
            "formal_component_edge_credit",
            "formal_component_quotient_credit",
            "formal_component_union_credit",
            "formal_fibre_credit",
            "formal_global_disposition_credit",
            "formal_maximality_credit",
            "formal_occurrence_identity_collapse_credit",
            "formal_official_key_merge_credit",
            "formal_seam_edge_credit",
        ):
            need(row[field] == 0, "R300D strict zero:" + field)
        need(
            row["eligible_for_component_DSU_application"] is False
            and row["topological_occurrence_union_connectivity_claimed"]
            is False,
            "R300D incidence-only ineligible boundary",
        )
        provenance = exact_provenance.get(tuple(occurrence_pair), [])
        for reference in provenance:
            if "source_Round300D_pair_row_id" in reference:
                need(
                    reference["source_Round300D_pair_row_id"]
                    == row[
                        "Round300D_lower_physical_witness_incidence_edge_row_id"
                    ]
                    and reference["source_Round300D_pair_row_sha256"]
                    == row["row_sha256"],
                    "later gate exact R300D pair source-row binding",
                )
        gates = sorted({item["gate"] for item in provenance})
        if not gates:
            d_disposition["NO_STRONGER_GATE_PROOF__INCIDENCE_ONLY"] += 1
        elif len(gates) == 1:
            kinds = sorted({
                item["provenance_kind"] for item in provenance
            })
            need(len(kinds) == 1, "one gate has one exact disposition")
            if kinds[0] == "RECLOSED_BY_STRONGER_LEGAL_EDGE":
                label = (
                    gates[0]
                    + "_STRONGER_PROOF__R300D_ROW_STILL_INELIGIBLE"
                )
            else:
                label = (
                    gates[0] + "_" + kinds[0]
                    + "__R300D_ROW_STILL_INELIGIBLE"
                )
            d_disposition[label] += 1
        else:
            d_disposition["MULTIPLE_STRONGER_GATE_PROOFS"] += 1

    stream_gzip_rows(
        R300D_LEDGER,
        "Round300D_lower_physical_witness_incidence_edge_row_id",
        R300D_INCIDENCE_COMMITMENT,
        visit_d_incidence,
        table="canonical_incidence_edge_rows",
    )

    d_single_kinds: Counter[str] = Counter()

    def visit_d_single(row: dict[str, Any]) -> None:
        need(
            row["canonical_two_target_incidence_edge_issued"] is False,
            "R300D single-target is not an edge",
        )
        for field in (
            "formal_DSU_rank_reduction_credit",
            "formal_Jx_Jy_same_point_glue_credit",
            "formal_component_edge_credit",
            "formal_component_quotient_credit",
            "formal_component_union_credit",
            "formal_fibre_credit",
            "formal_global_disposition_credit",
            "formal_maximality_credit",
            "formal_occurrence_identity_collapse_credit",
            "formal_official_key_merge_credit",
            "formal_seam_edge_credit",
        ):
            need(row[field] == 0, "R300D single strict zero:" + field)
        d_single_kinds[row["witness_kind"]] += 1
        references = single_provenance.get(
            row["Round300D_single_target_assignment_exclusion_row_id"],
            [],
        )
        for reference in references:
            need(
                reference["source_Round300D_single_row_id"]
                == row[
                    "Round300D_single_target_assignment_exclusion_row_id"
                ]
                and reference["source_Round300D_single_row_sha256"]
                == row["row_sha256"],
                "later gate exact R300D single source-row binding",
            )
            need(
                reference["target_Round294_registry_occurrence_id"]
                == row["target_Round294_registry_occurrence"][
                    "registry_occurrence_id"
                ]
                and reference["target_Round294_registry_entry_kind"]
                == row["target_Round294_registry_occurrence"][
                    "registry_entry_kind"
                ]
                and reference["witness_kind"] == row["witness_kind"],
                "later gate exact R300D single target/witness binding",
            )
        d_single_gate_coverage[
            "+".join(sorted({item["gate"] for item in references}))
            if references else "NO_LATER_GATE_AUDIT"
        ] += 1

    d_single_gate_coverage: Counter[str] = Counter()
    stream_gzip_rows(
        R300D_LEDGER,
        "Round300D_single_target_assignment_exclusion_row_id",
        R300D_SINGLE_COMMITMENT,
        visit_d_single,
        table="single_target_assignment_exclusion_rows",
    )

    a_prior = 0
    a_unresolved = 0
    a_stronger: Counter[str] = Counter()
    a_prior_channel_exact_intersections: Counter[str] = Counter()
    a_face_disposition: Counter[str] = Counter()
    a_primary_source_consumption_disposition: Counter[str] = Counter()
    a_seen_pairs: set[tuple[str, str]] = set()

    def visit_a_pair(row: dict[str, Any]) -> None:
        nonlocal a_prior, a_unresolved
        occurrence_pair = row[
            "canonical_unordered_Round294_registry_occurrence_ids"
        ]
        need(
            type(occurrence_pair) is list
            and len(occurrence_pair) == 2
            and occurrence_pair == sorted(occurrence_pair)
            and tuple(occurrence_pair) not in a_seen_pairs,
            "R300A unique canonical occurrence pair",
        )
        a_seen_pairs.add(tuple(occurrence_pair))
        for field in (
            "formal_DSU_rank_reduction_credit",
            "formal_component_edge_credit",
            "formal_maximality_credit",
            "formal_occurrence_identity_collapse_credit",
            "formal_seam_edge_credit",
        ):
            need(row[field] == 0, "R300A pair strict zero:" + field)
        need(
            row[
                "parent_regular_graph_zero_in_closure_is_not_itself_an_edge"
            ] is True
            and row["exact_positive_open_support_intersection"] is False,
            "R300A closure-contact nonedge boundary",
        )
        if row["R295A_explicit_lower_graph_sheet_witness_present"]:
            a_prior += 1
        else:
            a_unresolved += 1
        provenance = exact_provenance.get(tuple(occurrence_pair), [])
        stronger = sorted({
            item["gate"] + ":" + item["provenance_kind"]
            for item in provenance
        })
        a_stronger[
            "+".join(stronger) if stronger else "NO_STRONGER_GATE_PROOF"
        ] += 1
        for channel, pairs in prior_pair_sets.items():
            if tuple(occurrence_pair) in pairs:
                a_prior_channel_exact_intersections[channel] += 1
        face_accepted = a_face_accepted.get(tuple(occurrence_pair), [])
        face_rejected = a_face_rejected.get(tuple(occurrence_pair), [])
        if face_accepted:
            need(
                any(item["gate"] == "R300B" for item in provenance),
                "R300B accepted face exact pair has legal provenance",
            )
            a_face_disposition["R300B_ACCEPTED_FACE"] += 1
        elif face_rejected:
            a_face_disposition[
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE"
            ] += 1
        else:
            a_face_disposition[
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE"
            ] += 1
        provenance_gates = {item["gate"] for item in provenance}
        if "R300B" in provenance_gates:
            a_primary_source_consumption_disposition[
                "RECLOSED_BY_R300B_STRONGER_LEGAL_EDGE"
            ] += 1
        elif face_rejected:
            a_primary_source_consumption_disposition[
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE"
            ] += 1
        elif "R300G" in provenance_gates:
            a_primary_source_consumption_disposition[
                "R300G_AUDITED_FAIL_CLOSED_NO_EDGE"
            ] += 1
        else:
            a_primary_source_consumption_disposition[
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE__"
                "ROUND302_REOPEN"
            ] += 1

    stream_gzip_rows(
        R300A_LEDGER,
        "Round300A_canonical_occurrence_pair_row_id",
        R300A_CANONICAL_PAIR_COMMITMENT,
        visit_a_pair,
        table="canonical_occurrence_pair_rows",
    )

    a_expansion_references = 0

    def visit_a_expansion(row: dict[str, Any]) -> None:
        nonlocal a_expansion_references
        need(
            row["exact_positive_open_support_intersection"] is False
            and row["formal_DSU_rank_reduction_credit"] == 0
            and row["formal_component_edge_credit"] == 0
            and row["formal_occurrence_identity_collapse_credit"] == 0,
            "R300A source expansion closure-only",
        )
        references = row["canonical_occurrence_pair_row_ids"]
        need(
            type(references) is list and references,
            "R300A expansion canonical reference coverage",
        )
        a_expansion_references += len(references)

    stream_gzip_rows(
        R300A_LEDGER,
        "Round300A_R287_source_pair_expansion_row_id",
        R300A_SOURCE_EXPANSION_COMMITMENT,
        visit_a_expansion,
        table="source_pair_expansion_rows",
    )

    need(
        len(d_seen_occurrence_pairs) == 111_524
        and sum(d_disposition.values()) == 111_524
        and sum(d_single_kinds.values()) == 1_600
        and len(a_seen_pairs) == 3_232
        and a_prior == 128
        and a_unresolved == 3_104,
        "complete R300A/R300D ineligible source coverage",
    )
    if pending_gate_seals == ["R300G", "R300H"]:
        need(
            d_disposition == {
                "R300E_STRONGER_PROOF__R300D_ROW_STILL_INELIGIBLE": 472,
                "R300F_STRONGER_PROOF__R300D_ROW_STILL_INELIGIBLE": 264,
                "NO_STRONGER_GATE_PROOF__INCIDENCE_ONLY": 110_788,
            },
            "preliminary exact E/F provenance into R300D",
        )
        need(
            a_stronger == {
                "R300B:RECLOSED_BY_STRONGER_LEGAL_EDGE": 432,
                "NO_STRONGER_GATE_PROOF": 2_800,
            }
            and not a_prior_channel_exact_intersections,
            "preliminary exact R300A stronger-channel cross-check",
        )
        need(
            a_face_disposition == {
                "R300B_ACCEPTED_FACE": 432,
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE": 8,
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE": 2_792,
            },
            "preliminary complete R300B face disposition of R300A",
        )
        need(
            a_primary_source_consumption_disposition == {
                "RECLOSED_BY_R300B_STRONGER_LEGAL_EDGE": 432,
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE": 8,
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE__"
                "ROUND302_REOPEN": 2_792,
            },
            "preliminary R300A primary source consumption partition",
        )
    if pending_gate_seals == ["R300H"]:
        need(
            d_disposition == {
                "R300E_STRONGER_PROOF__R300D_ROW_STILL_INELIGIBLE": 472,
                "R300F_STRONGER_PROOF__R300D_ROW_STILL_INELIGIBLE": 264,
                "R300G_AUDITED_FAIL_CLOSED_NO_EDGE__"
                "R300D_ROW_STILL_INELIGIBLE": 128,
                "NO_STRONGER_GATE_PROOF__INCIDENCE_ONLY": 110_660,
            },
            "preliminary exact E/F/G provenance into R300D",
        )
        need(
            a_stronger == {
                "R300B:RECLOSED_BY_STRONGER_LEGAL_EDGE": 432,
                "R300G:AUDITED_FAIL_CLOSED_NO_EDGE": 128,
                "NO_STRONGER_GATE_PROOF": 2_672,
            }
            and not a_prior_channel_exact_intersections,
            "preliminary exact R300A B/G cross-check",
        )
        need(
            a_face_disposition == {
                "R300B_ACCEPTED_FACE": 432,
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE": 8,
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE": 2_792,
            }
            and a_primary_source_consumption_disposition == {
                "RECLOSED_BY_R300B_STRONGER_LEGAL_EDGE": 432,
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE": 8,
                "R300G_AUDITED_FAIL_CLOSED_NO_EDGE": 128,
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE__"
                "ROUND302_REOPEN": 2_664,
            },
            "preliminary G-sealed R300A 432/8/128/2664 partition",
        )
        need(
            d_single_gate_coverage == {"NO_LATER_GATE_AUDIT": 1_600},
            "R300H singles remain pending",
        )
    if not pending_gate_seals:
        need(
            d_disposition[
                "R300E_STRONGER_PROOF__R300D_ROW_STILL_INELIGIBLE"
            ] == 472
            and d_disposition[
                "R300F_STRONGER_PROOF__R300D_ROW_STILL_INELIGIBLE"
            ] == 264
            and d_disposition[
                "R300G_AUDITED_FAIL_CLOSED_NO_EDGE__"
                "R300D_ROW_STILL_INELIGIBLE"
            ] == 128
            and sum(
                count
                for label, count in d_disposition.items()
                if label.startswith("R300H_")
            ) == 144
            and d_disposition[
                "NO_STRONGER_GATE_PROOF__INCIDENCE_ONLY"
            ] == 110_516
            and "MULTIPLE_STRONGER_GATE_PROOFS" not in d_disposition,
            "final pairwise-disjoint R300D E/F/G/H source partition",
        )
        need(
            a_primary_source_consumption_disposition == {
                "RECLOSED_BY_R300B_STRONGER_LEGAL_EDGE": 432,
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE": 8,
                "R300G_AUDITED_FAIL_CLOSED_NO_EDGE": 128,
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE__"
                "ROUND302_REOPEN": 2_664,
            },
            "final R300A 432/8/128/2664 source partition",
        )
        need(
            d_single_gate_coverage == {"R300H": 1_600},
            "final R300H complete 1600 single-target coverage",
        )
    return {
        "R300D_canonical_incidence_pair_count": len(
            d_seen_occurrence_pairs
        ),
        "R300D_pair_source_consumption_disposition": dict(sorted(
            d_disposition.items()
        )),
        "R300D_single_target_assignment_exclusion_count":
            sum(d_single_kinds.values()),
        "R300D_single_target_witness_kind_histogram": dict(sorted(
            d_single_kinds.items()
        )),
        "R300D_single_target_later_gate_coverage": dict(sorted(
            d_single_gate_coverage.items()
        )),
        "R300A_canonical_closure_pair_count": len(a_seen_pairs),
        "R300A_prior_explicit_lower_witness_pair_count": a_prior,
        "R300A_unresolved_zero_trace_pair_count": a_unresolved,
        "R300A_pair_stronger_gate_projection": dict(sorted(
            a_stronger.items()
        )),
        "R300A_other_prior_channel_exact_pair_intersections": dict(sorted(
            a_prior_channel_exact_intersections.items()
        )),
        "R300A_complete_R300B_face_disposition": dict(sorted(
            a_face_disposition.items()
        )),
        "R300A_primary_source_consumption_disposition": dict(sorted(
            a_primary_source_consumption_disposition.items()
        )),
        "R300A_source_pair_expansion_count":
            R300A_SOURCE_EXPANSION_COMMITMENT["row_count"],
        "R300A_source_expansion_to_canonical_reference_count":
            a_expansion_references,
        "ineligible_source_rows_fed_to_DSU": 0,
        "registered_gate_coverage_census": gate_census,
    }


def canonical_partition(
    dsu: DSU,
    base_roots: set[str],
) -> tuple[dict[str, str], str, int]:
    groups: dict[str, list[str]] = defaultdict(list)
    for root in sorted(base_roots):
        groups[dsu.find(root)].append(root)
    root_to_component: dict[str, str] = {}
    component_root_sets: list[list[str]] = []
    for roots in groups.values():
        roots.sort()
        component_id = "round301-legal-component:" + digest(roots)
        component_root_sets.append(roots)
        for root in roots:
            root_to_component[root] = component_id
    component_root_sets.sort(key=lambda roots: roots[0])
    partition_pin = digest(component_root_sets)
    return root_to_component, partition_pin, len(component_root_sets)


def apply_edges(
    edges: Iterable[Edge],
    base_roots: set[str],
) -> tuple[dict[str, str], dict[str, Any]]:
    dsu = DSU(base_roots)
    per_channel: dict[str, Counter[str]] = defaultdict(Counter)
    total = 0
    for edge in edges:
        total += 1
        counter = per_channel[edge.channel]
        counter["edge_rows"] += 1
        if edge.left_base_root == edge.right_base_root:
            counter["same_base_root_before_application"] += 1
            counter["cycle_or_redundant"] += 1
        elif dsu.union(edge.left_base_root, edge.right_base_root):
            counter["rank_reduction"] += 1
        else:
            counter["cycle_or_redundant"] += 1
    root_to_component, partition_pin, component_count = canonical_partition(
        dsu, base_roots
    )
    rank = sum(counter["rank_reduction"] for counter in per_channel.values())
    need(
        rank == len(base_roots) - component_count,
        "rank-nullity component census",
    )
    return root_to_component, {
        "edge_rows_processed": total,
        "rank_reduction": rank,
        "component_count": component_count,
        "partition_sha256": partition_pin,
        "per_channel_application": {
            channel: dict(sorted(counter.items()))
            for channel, counter in sorted(per_channel.items())
        },
    }


def iter_edge_application_rows(
    edges: list[Edge],
    base_roots: set[str],
    final_root_to_component: dict[str, str],
) -> Iterator[dict[str, Any]]:
    dsu = DSU(base_roots)
    for ordinal, edge in enumerate(edges):
        left_before = dsu.find(edge.left_base_root)
        right_before = dsu.find(edge.right_base_root)
        rank_reduction = left_before != right_before
        if rank_reduction:
            need(
                dsu.union(edge.left_base_root, edge.right_base_root),
                "canonical application union succeeds",
            )
        final_component = final_root_to_component[edge.left_base_root]
        need(
            final_component
            == final_root_to_component[edge.right_base_root],
            "legal edge final component agreement",
        )
        payload = {
            "Round301_legal_component_edge_application_row_id":
                "round301-legal-component-edge-application:"
                + digest([edge.channel, edge.source_row_id]),
            "application_ordinal": ordinal,
            "canonical_projected_base_root_pair": sorted([
                edge.left_base_root,
                edge.right_base_root,
            ]),
            "cycle_or_redundant_after_prior_legal_edges":
                not rank_reduction,
            "eligible_for_component_DSU_application": True,
            "final_Round301_component_id": final_component,
            "formal_DSU_rank_reduction_credit":
                1 if rank_reduction else 0,
            "formal_component_edge_application_credit": 1,
            "formal_component_union_credit":
                1 if rank_reduction else 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "pre_application_DSU_representative_pair": sorted([
                left_before,
                right_before,
            ]),
            "rank_reduction_applied": rank_reduction,
            "same_pre_application_DSU_component":
                not rank_reduction,
            "source_canonical_endpoint_pair": [
                edge.left_endpoint,
                edge.right_endpoint,
            ],
            "source_channel": edge.channel,
            "source_edge_row_id": edge.source_row_id,
            "source_edge_row_sha256": edge.source_row_sha256,
            "source_occurrence_identities_preserved": True,
        }
        yield close_row(payload)


def iter_member_component_rows(
    members: dict[str, Member],
    final_root_to_component: dict[str, str],
) -> Iterator[dict[str, Any]]:
    for member_id in sorted(members):
        member = members[member_id]
        payload = {
            "Round301_member_to_component_row_id":
                "round301-member-to-component:" + digest(member_id),
            "base_component_root_id": member.base_root,
            "final_Round301_component_id":
                final_root_to_component[member.base_root],
            "formal_component_membership_credit": 1,
            "formal_occurrence_identity_collapse_credit": 0,
            "member_identity_preserved": True,
            "member_kind": member.member_kind,
            "official_key_id": member.official_key_id,
            "registry_or_frontier_member_id": member.member_id,
            "source_member_row_id": member.source_row_id,
            "source_member_row_sha256": member.source_row_sha256,
        }
        yield close_row(payload)


def build_component_key_incidence(
    members: dict[str, Member],
    base_roots: set[str],
    final_root_to_component: dict[str, str],
) -> tuple[
    dict[tuple[str, str], Counter[str]],
    dict[str, int],
    dict[str, str],
]:
    root_keys: dict[str, str] = {}
    incidence: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for member in members.values():
        key = member.official_key_id
        need(type(key) is str, "member final official key")
        prior = root_keys.setdefault(member.base_root, key)
        need(prior == key, "base root official-key purity before DSU")
        incidence[
            (final_root_to_component[member.base_root], key)
        ]["member_count"] += 1
    need(set(root_keys) == base_roots, "official key for every base root")
    for root in base_roots:
        incidence[
            (final_root_to_component[root], root_keys[root])
        ]["base_root_count"] += 1
    key_multiplicity: Counter[str] = Counter()
    for component, _key in incidence:
        key_multiplicity[component] += 1
    component_key_multiplicity = dict(key_multiplicity)
    return incidence, component_key_multiplicity, root_keys


def iter_component_key_incidence_rows(
    incidence: dict[tuple[str, str], Counter[str]],
    component_key_multiplicity: dict[str, int],
) -> Iterator[dict[str, Any]]:
    for component, key in sorted(incidence):
        counts = incidence[(component, key)]
        payload = {
            "Round301_component_key_incidence_row_id":
                "round301-component-key-incidence:"
                + digest([component, key]),
            "final_Round301_component_id": component,
            "formal_official_key_merge_credit": 0,
            "member_count": counts["member_count"],
            "official_key_id": key,
            "official_key_identity_preserved": True,
            "official_key_multiplicity_in_component":
                component_key_multiplicity[component],
            "pre_application_base_root_count":
                counts["base_root_count"],
        }
        yield close_row(payload)


def stronger_edge_reference_map(
    edges: list[Edge],
) -> dict[tuple[str, str], list[dict[str, str]]]:
    output: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for edge in edges:
        gate = edge.channel.split("_", 1)[0]
        if gate not in {"R300E", "R300F", "R300G", "R300H"}:
            continue
        pair = tuple(sorted((edge.left_base_root, edge.right_base_root)))
        output[pair].append({
            "legal_edge_channel": edge.channel,
            "legal_edge_source_row_id": edge.source_row_id,
            "legal_edge_source_row_sha256": edge.source_row_sha256,
        })
    for references in output.values():
        references.sort(key=lambda item: (
            item["legal_edge_channel"],
            item["legal_edge_source_row_id"],
        ))
    return output


def iter_ineligible_source_consumption_rows(
    edges: list[Edge],
    members: dict[str, Member],
    base_roots: set[str],
    exact_provenance_override: (
        dict[tuple[str, str], list[dict[str, Any]]] | None
    ) = None,
    single_provenance_override: (
        dict[str, list[dict[str, Any]]] | None
    ) = None,
    a_face_accepted_override: (
        dict[tuple[str, str], list[dict[str, Any]]] | None
    ) = None,
    a_face_rejected_override: (
        dict[tuple[str, str], list[dict[str, Any]]] | None
    ) = None,
) -> Iterator[dict[str, Any]]:
    del edges
    if (
        exact_provenance_override is None
        or single_provenance_override is None
    ):
        exact_provenance, single_provenance, _gate_census = (
            complete_exact_gate_provenance()
        )
    else:
        exact_provenance = exact_provenance_override
        single_provenance = single_provenance_override
    if (
        a_face_accepted_override is None
        or a_face_rejected_override is None
    ):
        a_target_pairs = exact_R300A_pair_set()
        a_face_accepted, a_face_rejected = (
            exact_R300B_face_coverage_for_pairs(a_target_pairs)
        )
    else:
        a_face_accepted = a_face_accepted_override
        a_face_rejected = a_face_rejected_override

    def project(endpoint: str) -> str:
        if endpoint in base_roots:
            return endpoint
        member = members.get(endpoint)
        need(member is not None, "consumption endpoint in member universe")
        return member.base_root

    def pair_projection(pair: list[str]) -> list[str]:
        return sorted((project(pair[0]), project(pair[1])))

    for row in validated_gzip_rows(
        R300D_LEDGER,
        "Round300D_lower_physical_witness_incidence_edge_row_id",
        R300D_INCIDENCE_COMMITMENT,
        table="canonical_incidence_edge_rows",
    ):
        pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
        projected = pair_projection(pair)
        provenance = exact_provenance.get(tuple(pair), [])
        gates = sorted({reference["gate"] for reference in provenance})
        stronger = [
            {
                "legal_edge_channel": reference[
                    "legal_edge_channel"
                ],
                "legal_edge_source_row_id": reference[
                    "legal_edge_source_row_id"
                ],
                "legal_edge_source_row_sha256": reference[
                    "legal_edge_source_row_sha256"
                ],
            }
            for reference in provenance
            if reference["provenance_kind"]
            == "RECLOSED_BY_STRONGER_LEGAL_EDGE"
        ]
        if stronger:
            disposition = (
                "INELIGIBLE_SOURCE_ROW_NOT_CONSUMED__"
                "PAIR_RECLOSED_BY_STRONGER_LEGAL_EDGE"
            )
        elif provenance:
            disposition = (
                "INELIGIBLE_SOURCE_ROW_NOT_CONSUMED__"
                "AUDITED_FAIL_CLOSED_NO_EDGE"
            )
        else:
            disposition = (
                "INELIGIBLE_INCIDENCE_ONLY__NO_STRONGER_GATE_PROOF"
            )
        payload = {
            "Round301_ineligible_source_consumption_row_id":
                "round301-ineligible-source-consumption:"
                + digest([
                    "R300D_CANONICAL_INCIDENCE_PAIR",
                    row[
                        "Round300D_lower_physical_witness_incidence_edge_row_id"
                    ],
                ]),
            "canonical_occurrence_endpoint_pair": pair,
            "canonical_projected_base_root_pair": projected,
            "disposition": disposition,
            "eligible_for_component_DSU_application": False,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_component_edge_application_credit": 0,
            "formal_component_union_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "legal_stronger_edge_references": stronger,
            "exact_gate_provenance_references": provenance,
            "source_relation":
                "R300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_"
                "INCIDENCE_EDGE",
            "source_row_fed_to_DSU": False,
            "source_row_id":
                row[
                    "Round300D_lower_physical_witness_incidence_edge_row_id"
                ],
            "source_row_sha256": row["row_sha256"],
            "stronger_gate_names": gates,
        }
        yield close_row(payload)

    for row in validated_gzip_rows(
        R300D_LEDGER,
        "Round300D_single_target_assignment_exclusion_row_id",
        R300D_SINGLE_COMMITMENT,
        table="single_target_assignment_exclusion_rows",
    ):
        target_record = row["target_Round294_registry_occurrence"]
        target = target_record["registry_occurrence_id"]
        source_row_id = row[
            "Round300D_single_target_assignment_exclusion_row_id"
        ]
        later_gate_references = single_provenance.get(source_row_id, [])
        later_gate_names = sorted({
            reference["gate"] for reference in later_gate_references
        })
        payload = {
            "Round301_ineligible_source_consumption_row_id":
                "round301-ineligible-source-consumption:"
                + digest([
                    "R300D_SINGLE_TARGET_ASSIGNMENT",
                    row[
                        "Round300D_single_target_assignment_exclusion_row_id"
                    ],
                ]),
            "canonical_occurrence_endpoint_pair": None,
            "canonical_projected_base_root_pair": None,
            "disposition":
                "INELIGIBLE_SINGLE_TARGET_ASSIGNMENT__NOT_AN_EDGE",
            "eligible_for_component_DSU_application": False,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_component_edge_application_credit": 0,
            "formal_component_union_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "legal_stronger_edge_references": [],
            "exact_gate_provenance_references":
                later_gate_references,
            "single_target_occurrence_id": target,
            "single_target_projected_base_root": project(target),
            "single_target_registry_entry_kind":
                target_record["registry_entry_kind"],
            "single_target_Round294_registry_row_id":
                target_record["Round294_occurrence_registry_row_id"],
            "single_target_Round294_registry_row_sha256":
                target_record["Round294_occurrence_registry_row_sha256"],
            "source_relation": "R300D_SINGLE_TARGET_ASSIGNMENT",
            "source_row_fed_to_DSU": False,
            "source_row_id":
                source_row_id,
            "source_row_sha256": row["row_sha256"],
            "stronger_gate_names": later_gate_names,
            "witness_kind": row["witness_kind"],
        }
        yield close_row(payload)

    for row in validated_gzip_rows(
        R300A_LEDGER,
        "Round300A_canonical_occurrence_pair_row_id",
        R300A_CANONICAL_PAIR_COMMITMENT,
        table="canonical_occurrence_pair_rows",
    ):
        pair = row["canonical_unordered_Round294_registry_occurrence_ids"]
        projected = pair_projection(pair)
        provenance = exact_provenance.get(tuple(pair), [])
        gates = sorted({reference["gate"] for reference in provenance})
        stronger = [
            {
                "legal_edge_channel": reference[
                    "legal_edge_channel"
                ],
                "legal_edge_source_row_id": reference[
                    "legal_edge_source_row_id"
                ],
                "legal_edge_source_row_sha256": reference[
                    "legal_edge_source_row_sha256"
                ],
            }
            for reference in provenance
            if reference["provenance_kind"]
            == "RECLOSED_BY_STRONGER_LEGAL_EDGE"
        ]
        face_accepted = a_face_accepted.get(tuple(pair), [])
        face_rejected = a_face_rejected.get(tuple(pair), [])
        provenance_gates = {reference["gate"] for reference in provenance}
        if "R300B" in provenance_gates:
            disposition = "RECLOSED_BY_R300B_STRONGER_LEGAL_EDGE"
        elif face_rejected:
            disposition = (
                "R300B_REJECTED_FACE__AUDITED_FAIL_CLOSED_NO_EDGE"
            )
        elif "R300G" in provenance_gates:
            disposition = "R300G_AUDITED_FAIL_CLOSED_NO_EDGE"
        else:
            disposition = (
                "R300B_COMPLETE_INVENTORY__NO_ENDPOINT_FACE__"
                "ROUND302_REOPEN"
            )
        payload = {
            "Round301_ineligible_source_consumption_row_id":
                "round301-ineligible-source-consumption:"
                + digest([
                    "R300A_CANONICAL_CLOSURE_PAIR",
                    row["Round300A_canonical_occurrence_pair_row_id"],
                ]),
            "canonical_occurrence_endpoint_pair": pair,
            "canonical_projected_base_root_pair": projected,
            "disposition": disposition,
            "eligible_for_component_DSU_application": False,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_component_edge_application_credit": 0,
            "formal_component_union_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "legal_stronger_edge_references": stronger,
            "exact_gate_provenance_references": provenance,
            "R300B_complete_face_inventory_references":
                face_accepted + face_rejected,
            "R300B_complete_face_inventory_rows_sha256":
                R300B_FACE_INVENTORY_COMMITMENT["rows_sha256"],
            "R300B_endpoint_face_present":
                bool(face_accepted or face_rejected),
            "R300B_no_endpoint_face_negative_set_difference_sha256":
                None if face_accepted or face_rejected
                else digest([
                    pair,
                    R300B_FACE_INVENTORY_COMMITMENT["rows_sha256"],
                    "NO_ENDPOINT_FACE_IN_COMPLETE_INVENTORY",
                ]),
            "prior_R295A_explicit_lower_graph_witness_present":
                row["R295A_explicit_lower_graph_sheet_witness_present"],
            "source_relation":
                "R300A_REGULAR_GRAPH_ZERO_CLOSURE_CONTACT",
            "source_row_fed_to_DSU": False,
            "source_row_id":
                row["Round300A_canonical_occurrence_pair_row_id"],
            "source_row_sha256": row["row_sha256"],
            "stronger_gate_names": gates,
        }
        yield close_row(payload)

    for row in validated_gzip_rows(
        R300A_LEDGER,
        "Round300A_R287_source_pair_expansion_row_id",
        R300A_SOURCE_EXPANSION_COMMITMENT,
        table="source_pair_expansion_rows",
    ):
        payload = {
            "Round301_ineligible_source_consumption_row_id":
                "round301-ineligible-source-consumption:"
                + digest([
                    "R300A_SOURCE_PAIR_EXPANSION",
                    row["Round300A_R287_source_pair_expansion_row_id"],
                ]),
            "canonical_occurrence_endpoint_pair": None,
            "canonical_projected_base_root_pair": None,
            "canonical_pair_reference_count":
                len(row["canonical_occurrence_pair_row_ids"]),
            "canonical_pair_reference_row_ids":
                row["canonical_occurrence_pair_row_ids"],
            "disposition":
                "INELIGIBLE_SOURCE_CROSS_PRODUCT_OR_CLOSURE_CONTACT__"
                "CANONICAL_DERIVATIONS_TRACKED_SEPARATELY",
            "eligible_for_component_DSU_application": False,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_component_edge_application_credit": 0,
            "formal_component_union_credit": 0,
            "formal_occurrence_identity_collapse_credit": 0,
            "legal_stronger_edge_references": [],
            "exact_gate_provenance_references": [],
            "source_relation": "R300A_R287_SOURCE_PAIR_EXPANSION",
            "source_row_fed_to_DSU": False,
            "source_row_id":
                row["Round300A_R287_source_pair_expansion_row_id"],
            "source_row_sha256": row["row_sha256"],
            "stronger_gate_names": [],
        }
        yield close_row(payload)


def preliminary() -> dict[str, Any]:
    validate_foundation_boundary()
    members, base_roots, member_census = reconstruct_members()
    active_channels = list(CHANNELS)
    for registration in PENDING_GATE_REGISTRATIONS.values():
        if registration is not None:
            validate_gate_package(registration)
            active_channels.extend(registration.eligible_edge_channels)
    edges, edge_census = collect_edges(
        active_channels, members, base_roots
    )
    forward_map, forward = apply_edges(edges, base_roots)
    reverse_map, reverse = apply_edges(reversed(edges), base_roots)
    need(
        forward_map == reverse_map
        and forward["partition_sha256"] == reverse["partition_sha256"]
        and forward["rank_reduction"] == reverse["rank_reduction"]
        and forward["component_count"] == reverse["component_count"],
        "forward/reverse exact partition equality",
    )
    pending = [
        name
        for name, registration in PENDING_GATE_REGISTRATIONS.items()
        if registration is None
    ]
    ineligible_census = audit_ineligible_sources(
        edges, members, base_roots, pending
    )
    # The known base+E+F diagnostic values are an assertion derived here, not
    # imported from any spike.
    if pending in (["R300G", "R300H"], ["R300H"]):
        need(
            forward["rank_reduction"] == 246_016
            and forward["component_count"] == 121_948,
            "independent base-five-plus-E-plus-F preliminary cross-check",
        )
    return {
        "schema":
            "cm2.round301.source-g-legal-component-dsu-application."
            "preliminary.v1",
        "status":
            "PRELIMINARY_ONLY__FINAL_QUOTIENT_AND_MANIFEST_FORBIDDEN_"
            "UNTIL_" + "_".join(pending) + "_SEALED",
        "final_artifact_written": False,
        "obsolete_Round298_or_tmp_spike_imported_executed_or_parsed": False,
        "member_universe": member_census,
        "active_sealed_channels": [
            channel.name for channel in active_channels
        ],
        "pending_gate_seals": pending,
        "edge_census": edge_census,
        "ineligible_source_consumption": ineligible_census,
        "forward_application": forward,
        "reverse_application": reverse,
        "forward_reverse_same_partition": True,
        "formal_Round301_quotient_issued": False,
    }


def final_package() -> dict[str, Any]:
    need(
        all(
            registration is not None
            for registration in PENDING_GATE_REGISTRATIONS.values()
        ),
        "every G/H gate package sealed before final Round301",
    )
    validate_foundation_boundary()
    members, base_roots, member_census = reconstruct_members()
    active_channels = list(CHANNELS)
    gate_census: dict[str, Any] = {}
    for name, registration in PENDING_GATE_REGISTRATIONS.items():
        need(registration is not None, "sealed registration:" + name)
        validate_gate_package(registration)
        coverage = registration.coverage_loader()
        gate_census[name] = coverage.census
        active_channels.extend(registration.eligible_edge_channels)
    edges, edge_census = collect_edges(
        active_channels, members, base_roots
    )
    forward_map, forward = apply_edges(edges, base_roots)
    reverse_map, reverse = apply_edges(reversed(edges), base_roots)
    need(
        forward_map == reverse_map
        and forward["partition_sha256"] == reverse["partition_sha256"]
        and forward["rank_reduction"] == reverse["rank_reduction"]
        and forward["component_count"] == reverse["component_count"],
        "final forward/reverse exact partition equality",
    )
    exact_provenance, single_provenance, coverage_census = (
        complete_exact_gate_provenance()
    )
    need(
        coverage_census == gate_census,
        "one exact sealed-gate coverage census",
    )
    a_target_pairs = exact_R300A_pair_set()
    a_face_accepted, a_face_rejected = (
        exact_R300B_face_coverage_for_pairs(a_target_pairs)
    )
    ineligible_census = audit_ineligible_sources(
        edges,
        members,
        base_roots,
        [],
        exact_provenance,
        single_provenance,
        coverage_census,
        a_face_accepted,
        a_face_rejected,
    )

    incidence, component_key_multiplicity, _root_keys = (
        build_component_key_incidence(members, base_roots, forward_map)
    )
    key_multiplicity_histogram = Counter(
        component_key_multiplicity.values()
    )
    component_key_census = {
        "component_key_incidence_row_count": len(incidence),
        "component_official_key_multiplicity_histogram": {
            str(key): value
            for key, value in sorted(key_multiplicity_histogram.items())
        },
        "cross_official_key_component_count": sum(
            1
            for value in component_key_multiplicity.values()
            if value > 1
        ),
        "maximum_official_key_multiplicity_in_one_component":
            max(component_key_multiplicity.values()),
        "official_key_identity_merge_count": 0,
    }

    edge_ledger = write_rows_ledger(
        EDGE_APPLICATION_LEDGER,
        (
            "cm2.round301.source-g-legal-component-dsu-application."
            "edge-application-ledger.v1"
        ),
        "PASS_COMPLETE_CANONICAL_FORWARD_LEGAL_EDGE_APPLICATION",
        "Round301_legal_component_edge_application_row_id",
        lambda: iter_edge_application_rows(
            edges, base_roots, forward_map
        ),
    )
    need(
        edge_ledger["row_count"] == len(edges),
        "complete final legal edge applications",
    )

    member_ledger = write_rows_ledger(
        MEMBER_COMPONENT_LEDGER,
        (
            "cm2.round301.source-g-legal-component-dsu-application."
            "member-component-ledger.v1"
        ),
        "PASS_COMPLETE_564492_MEMBER_TO_COMPONENT_MAPPING",
        "Round301_member_to_component_row_id",
        lambda: iter_member_component_rows(members, forward_map),
    )
    need(
        member_ledger["row_count"] == 564_492,
        "complete member-to-component mapping",
    )

    key_ledger = write_rows_ledger(
        COMPONENT_KEY_INCIDENCE_LEDGER,
        (
            "cm2.round301.source-g-legal-component-dsu-application."
            "component-key-incidence-ledger.v1"
        ),
        "PASS_COMPLETE_COMPONENT_KEY_INCIDENCE_WITHOUT_KEY_MERGE",
        "Round301_component_key_incidence_row_id",
        lambda: iter_component_key_incidence_rows(
            incidence, component_key_multiplicity
        ),
    )
    need(
        key_ledger["row_count"] == len(incidence),
        "complete component-key incidence mapping",
    )

    ineligible_ledger = write_rows_ledger(
        INELIGIBLE_SOURCE_LEDGER,
        (
            "cm2.round301.source-g-legal-component-dsu-application."
            "ineligible-source-consumption-ledger.v1"
        ),
        (
            "PASS_COMPLETE_R300A_R300D_SOURCE_CONSUMPTION__"
            "ZERO_INELIGIBLE_ROWS_FED_TO_DSU"
        ),
        "Round301_ineligible_source_consumption_row_id",
        lambda: iter_ineligible_source_consumption_rows(
            edges,
            members,
            base_roots,
            exact_provenance,
            single_provenance,
            a_face_accepted,
            a_face_rejected,
        ),
    )
    need(
        ineligible_ledger["row_count"] == 119_844,
        "complete 111524+1600+3232+3488 source consumption",
    )

    upstream_pins: dict[str, str] = {}
    upstream_pins.update(FOUNDATION_MANIFEST_PINS)
    upstream_pins.update(FOUNDATION_FILE_PINS)
    upstream_pins.update(INELIGIBLE_PACKAGE_PINS)
    upstream_pins[R300E_MANIFEST] = R300E_MANIFEST_PIN
    upstream_pins[R300E_WITNESS_LEDGER] = R300E_WITNESS_LEDGER_PIN
    upstream_pins[R300B_FACE_INVENTORY] = R300B_FACE_INVENTORY_PIN
    for channel in active_channels:
        upstream_pins[channel.manifest] = channel.manifest_sha256
        upstream_pins.update(package_members(channel))
    for registration in PENDING_GATE_REGISTRATIONS.values():
        need(registration is not None, "final registration")
        upstream_pins[registration.manifest] = registration.manifest_sha256
        upstream_pins.update(dict(registration.required_members))

    result_payload = {
        "schema":
            "cm2.round301.source-g-legal-component-dsu-application.v1",
        "status":
            "PASS_ROUND301_COMPLETE_LEGAL_COMPONENT_DSU__"
            + str(forward["rank_reduction"])
            + "_RANK_REDUCTIONS__"
            + str(forward["component_count"])
            + "_COMPONENTS__FORWARD_REVERSE_SAME_PARTITION",
        "producer_file_sha256": file_sha256(Path(__file__).resolve()),
        "input_file_and_manifest_pins": dict(sorted(
            upstream_pins.items()
        )),
        "member_universe": member_census,
        "legal_edge_census": edge_census,
        "sealed_gate_census": gate_census,
        "forward_application": forward,
        "reverse_application": reverse,
        "forward_reverse_same_partition": True,
        "component_key_incidence_census": component_key_census,
        "ineligible_source_consumption": ineligible_census,
        "output_ledgers": {
            "edge_application": edge_ledger,
            "member_to_component": member_ledger,
            "component_key_incidence": key_ledger,
            "ineligible_source_consumption": ineligible_ledger,
        },
        "formal_credit_transition": {
            "formal_legal_component_edge_application_credit":
                edge_ledger["row_count"],
            "formal_DSU_rank_reduction_credit":
                forward["rank_reduction"],
            "formal_component_union_credit":
                forward["rank_reduction"],
            "formal_component_quotient_credit": 1,
            "formal_post_Round301_component_count":
                forward["component_count"],
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_official_key_merge_credit": 0,
            "formal_maximality_credit": 0,
            "formal_fibre_credit": 0,
            "formal_global_disposition_credit": 0,
        },
        "strict_boundary": {
            "R295A_or_R300D_incidence_rows_fed_to_DSU": 0,
            "R300A_closure_contact_rows_fed_to_DSU": 0,
            "R300G_eligible_edge_row_count": 0,
            "R300H_eligible_edge_row_count": 0,
            "obsolete_Round298_or_tmp_spike_imported_executed_or_parsed":
                False,
            "rejected_multi_endpoint_face_raw_cross_product_used":
                False,
            "historical_29984_rank_number_used": False,
        },
        "required_next": [
            (
                "Use the sealed member-to-component and component-key "
                "incidence ledgers for downstream maximality, fibre, and "
                "global disposition gates."
            ),
            (
                "Reopen the exact 2664 R300A pairs with no endpoint face "
                "only under new positive-area/two-corridor or separately "
                "sealed gluing evidence."
            ),
        ],
        "seed_affects_output": False,
    }
    result_file_sha256, result_self_sha256 = write_closed_result(
        RESULT_FILE, result_payload
    )
    return {
        "schema":
            "cm2.round301.source-g-legal-component-dsu-application."
            "producer-run.v1",
        "status": "PASS_ROUND301_FINAL_PACKAGE_WRITTEN",
        "seed_affects_output": False,
        "output_file_pins": {
            EDGE_APPLICATION_LEDGER: edge_ledger["file_sha256"],
            MEMBER_COMPONENT_LEDGER: member_ledger["file_sha256"],
            COMPONENT_KEY_INCIDENCE_LEDGER: key_ledger["file_sha256"],
            INELIGIBLE_SOURCE_LEDGER:
                ineligible_ledger["file_sha256"],
            RESULT_FILE: result_file_sha256,
        },
        "result_sha256": result_self_sha256,
        "partition_sha256": forward["partition_sha256"],
        "rank_reduction": forward["rank_reduction"],
        "component_count": forward["component_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preliminary", action="store_true")
    parser.add_argument(
        "--preliminary-source-consumption-only",
        action="store_true",
    )
    parser.add_argument("--seed", default="301001")
    args = parser.parse_args()
    need(bool(args.seed), "nonempty seed bookkeeping")
    need(
        not (args.preliminary and args.preliminary_source_consumption_only),
        "one preliminary mode",
    )
    if args.preliminary_source_consumption_only:
        pending = [
            name
            for name, registration
            in PENDING_GATE_REGISTRATIONS.items()
            if registration is None
        ]
        print(canonical(audit_ineligible_sources(
            [], {}, set(), pending
        )).decode("utf-8"))
        return
    incomplete = any(
        registration is None
        for registration in PENDING_GATE_REGISTRATIONS.values()
    )
    if args.preliminary:
        need(incomplete, "preliminary mode is only for incomplete gate seals")
        print(canonical(preliminary()).decode("utf-8"))
        return
    need(not incomplete, "final mode disabled while gate seals remain pending")
    print(canonical(final_package()).decode("utf-8"))


if __name__ == "__main__":
    main()
