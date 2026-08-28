#!/usr/bin/env python3
"""Independent cacheless verifier for the Round303-A anchor/side bridge.

The Round303-A producer is an inert byte-pinned artifact.  It is never
imported, executed, parsed, tokenized, or used as an expected-output oracle.
This verifier reconstructs the exact Round301-cross-component Round300-D
scope from sealed inputs, then independently binds every new Round288-issued
occurrence anchor to its unique formal connected source-side region.

The bridge is deliberately weaker than a full-support equality claim:

    positive inner anchor B0  is contained in  connected formal side A.

It does not assert that B0 is the whole occurrence support.  Four W-tail
canonical atoms account for eight endpoint occurrences and twelve source-row
references; those rows lack the required connected-side extension and remain
fail-closed.  This gate grants no component edge, identity, key, DSU,
maximality, fibre, global-disposition, seam, or Jx/Jy credit.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction as Q
import gzip
import hashlib
import io
import json
import mmap
import os
from pathlib import Path
import re
import stat
from typing import Any, Callable, Iterable, Iterator, TextIO
import zlib

from flint import arb, ctx, __version__ as FLINT_VERSION


HERE = Path(__file__).resolve().parent
PREFIX = (
    "cm2_round303a_source_g_occurrence_anchor_connected_side_bridge"
)
PRODUCER = HERE / f"{PREFIX}.py"
MATERIALIZED_LEDGER = HERE / f"{PREFIX}_bridge_ledger.json.gz"
UNRESOLVED_LEDGER = HERE / f"{PREFIX}_unresolved_bridge_ledger.json.gz"
RESULT = HERE / f"{PREFIX}_result.json"
ATTACKS = HERE / f"{PREFIX}_attack_suite.json"
VERIFICATION = HERE / f"{PREFIX}_verification.json"

SCHEMA = "cm2.round303a.source-g-occurrence-anchor-connected-side-bridge.v1"
MATERIALIZED_SCHEMA = SCHEMA + ".materialized-bridge-ledger.v1"
UNRESOLVED_SCHEMA = SCHEMA + ".unresolved-bridge-ledger.v1"
ATTACK_SCHEMA = SCHEMA + ".independent-attack-suite.v1"
VERIFICATION_SCHEMA = SCHEMA + ".independent-verification.v1"

MATERIALIZED_ID = "Round303A_occurrence_anchor_source_side_bridge_row_id"
UNRESOLVED_ID = "Round303A_unresolved_occurrence_anchor_bridge_row_id"
THEOREM_ID = (
    "ROUND294_CANONICAL_ATOM_OCCURRENCE_"
    "ANCHOR_TO_CONNECTED_SOURCE_SIDE_BRIDGE_V1"
)
UNRESOLVED_DISPOSITION = (
    "UNRESOLVED__W_TAIL_CONNECTED_SOURCE_SIDE_EXTENSION_MISSING"
)

THEOREM = {
    "conclusion": (
        "A nonempty strict rational subbox B0 of the issued Round294 "
        "occurrence inner support is contained in the uniquely bound formal "
        "connected source signed region A; B0 may be consumed only as an "
        "occurrence anchor for a later separately proved attachment theorem."
    ),
    "credit_boundary": {
        "formal_DSU_rank_reduction_credit": 0,
        "formal_Jx_Jy_same_point_glue_credit": 0,
        "formal_component_edge_credit": 0,
        "formal_component_union_credit": 0,
        "formal_fibre_credit": 0,
        "formal_global_disposition_credit": 0,
        "formal_maximality_credit": 0,
        "formal_occurrence_anchor_connected_side_bridge_credit": 1,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_official_key_merge_credit": 0,
    },
    "hypotheses": {
        "A0_exact_provenance_pins_and_row_closures": (
            "The cross-Round301 Round300D scope, Round294 occurrence row, "
            "Round288 disposition, Round279 atom, source-side rows, leaf, "
            "active equation, support-source row, and interval kernel are "
            "all exactly content pinned and row closed."
        ),
        "A1_Round294_issued_occurrence_has_nonempty_inner_anchor": (
            "The formally issued Round294 occurrence carries an exact "
            "positive-volume rational inner-support box B."
        ),
        "A2_strict_anchor_subbox_inside_issued_inner_support": (
            "Independent interval replay constructs a positive-volume "
            "rational B0 contained in B on which the exact active scalar has "
            "the strict sign bound by the source signed-region row."
        ),
        "A3_occurrence_atom_source_side_provenance_exactly_closed": (
            "The Round294 occurrence ID, Round288 disposition, Round279 "
            "canonical atom, leaf, chart, signature, and source-side row all "
            "close to one exact signed-region provenance chain."
        ),
        "A4_unique_formal_connected_source_signed_region_materialized": (
            "The non-W-tail source row materializes the complete connected "
            "active-factor sign side A in the pinned leaf, and B0 has that "
            "same exact active-factor sign."
        ),
    },
    "nonclaims": {
        "DSU_rank_or_quotient_change": False,
        "component_connectivity_edge": False,
        "full_occurrence_support_equals_connected_source_side": False,
        "maximality_fibre_or_global_disposition": False,
        "occurrence_identity_or_official_key_merge": False,
    },
    "theorem_id": THEOREM_ID,
}
THEOREM_SHA256 = (
    "41141dbd0fbc9d501c5714ab61b7907711f1a6fdcee1796a6cbc602e9aab138f"
)

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

# The producer is an inert byte-pinned input only.  It is never imported,
# executed, parsed, or tokenized by this verifier.
PRODUCER_SHA256 = (
    "b85d6a8f33e81feb613b2cdb04de648376a10c94635b23119bd7f70439ba461a"
)

R301_MEMBER = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "member_component_ledger.json.gz"
)
R301_INELIGIBLE = (
    "cm2_round301_source_g_legal_component_dsu_application_"
    "ineligible_source_consumption_ledger.json.gz"
)
R300D_LEDGER = (
    "cm2_round300d_source_g_lower_physical_witness_component_"
    "edge_promotion_ledger.json.gz"
)
R294_REGISTRY = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "registry_ledger.json.gz"
)
R288_DISPOSITIONS = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "atom_dispositions.json.gz"
)
R288_OVERLAPS = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "existing_overlap_relations.json.gz"
)
R279_ATOMS = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_atoms.json.gz"
)
R279_EDGES = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_edges.json.gz"
)
R290_SUPPORT = (
    "cm2_round290_source_g_isolated_atom_inner_support_closure_"
    "inner_support_ledger.json.gz"
)
R269_CERT = (
    "cm2_round269_source_g_closed_collar_direct_signature_"
    "materialization_certificate.json"
)
R270_CERT = (
    "cm2_round270_source_g_outgoing_g_factor_signature_"
    "materialization_certificate.json"
)
R271_CERT = (
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_"
    "materialization_certificate.json"
)
R272_CERT = (
    "cm2_round272_source_g_boundary_dual_factor_wall_"
    "closure_certificate.json"
)
R179_KERNEL = "cm2_round179_source_g_residual_tube_arrangement.py"
R179_ROWS = "cm2_round179_source_g_residual_tube_arrangement_rows.json"
R182_ROWS = (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
)
R179_VERIFICATION = (
    "cm2_round179_source_g_residual_tube_arrangement_verification.json"
)
R182_VERIFICATION = (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json"
)
R269_VERIFICATION = (
    "cm2_round269_source_g_closed_collar_direct_signature_"
    "materialization_verification.json"
)
R270_VERIFICATION = (
    "cm2_round270_source_g_outgoing_g_factor_signature_"
    "materialization_verification.json"
)
R271_VERIFICATION = (
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_"
    "materialization_verification.json"
)
R272_VERIFICATION = (
    "cm2_round272_source_g_boundary_dual_factor_wall_"
    "closure_verification.json"
)
R279_VERIFICATION = (
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_"
    "verification.json"
)
R288_VERIFICATION = (
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "verification.json"
)
R290_VERIFICATION = (
    "cm2_round290_source_g_isolated_atom_inner_support_closure_"
    "verification.json"
)
R294_VERIFICATION = (
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_"
    "verification.json"
)
R300D_VERIFICATION = (
    "cm2_round300d_source_g_lower_physical_witness_component_edge_"
    "promotion_verification.json"
)
R301_VERIFICATION = (
    "cm2_round301_source_g_legal_component_dsu_application_verification.json"
)
GATE5_MANIFEST = (
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
GATE3_FIRST_HIT_SPEC = "cm2_gate3_candidate_first_hit_cert.py"
GATE3_ATLAS_SPEC = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GATE3_INTERVAL_SPEC = "cm2_gate3_ge_interval_atlas_cert.py"

FILE_PINS = {
    R179_KERNEL:
        "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R301_MEMBER:
        "88adb1ac6c9ee447fddb2ccd8e657a238827e9b31712d974a2a9abd2a3591b93",
    R301_INELIGIBLE:
        "5fbc5a409eccd4e04954c7b63dab6739897efd8d9e327c47045cbfbbbaf7633e",
    R300D_LEDGER:
        "287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7",
    R294_REGISTRY:
        "c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb",
    R288_DISPOSITIONS:
        "6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a",
    R288_OVERLAPS:
        "d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e",
    R279_ATOMS:
        "283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe",
    R279_EDGES:
        "bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695",
    R290_SUPPORT:
        "9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025",
    R269_CERT:
        "472df3ac65c490b79924beaabb382435f5b74ea8ac6c13d71b1d0ab54ffe01d3",
    R270_CERT:
        "72a47e53ff601660cb63fe8062403e41a54450fa4a432638faf18a2c76b3efea",
    R271_CERT:
        "c2a6b66c6fc6ac0b353b36254339a90b91f18c52246c324307ee49569bd7b747",
    R272_CERT:
        "16050c7087deb546d39b2c7922274ccae7cec24a799ecafd9a8304ae1186d8f2",
    R179_ROWS:
        "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42",
    R182_ROWS:
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    R179_VERIFICATION:
        "37eaa14cd870df64a12c2434deafe5fdead5cec303f5530208f07c11836736bc",
    R182_VERIFICATION:
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    R269_VERIFICATION:
        "3435ad2ad0d76f881e7b49fd052fb64035776a991b0f92a542b054f224860982",
    R270_VERIFICATION:
        "6af01780481224f8c9fd690c46886321be4f5b294c33e3f6515cf20dc7cb0513",
    R271_VERIFICATION:
        "26eed04f887f8b6a4ec8fcc88f1112f7382e079d9c53a33dd37a53f7417a29f9",
    R272_VERIFICATION:
        "a40f79823dcf07155eec1ecd12cc367dae6b7bdc7a6e8e7cf8680d29d4dade10",
    R279_VERIFICATION:
        "a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21",
    R288_VERIFICATION:
        "f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23",
    R290_VERIFICATION:
        "94a8b1a3a0274bfb14d6f9e9b00d896673792548220e309b0211f2f2e3367b51",
    R294_VERIFICATION:
        "13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245",
    R300D_VERIFICATION:
        "a5bd12b10103b4785574bd4633e608c7fd5107369ba8f2343ebffe7e08eba1c7",
    R301_VERIFICATION:
        "31db1fd416c12a384bcfc7dd08d0a6ecf1cba5a9390b47227847f5c7852f376a",
    GATE5_MANIFEST:
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    GATE3_FIRST_HIT_SPEC:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    GATE3_ATLAS_SPEC:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    GATE3_INTERVAL_SPEC:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
}

MANIFEST_PINS = {
    "cm2_round179_source_g_residual_tube_arrangement_manifest.sha256":
        "8fd5ae3a0cdd0c3321c0f8ffe6183ab57d31088b96523fa41ce0ebbe10d78b76",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256":
        "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5",
    "cm2_round269_source_g_closed_collar_direct_signature_"
    "materialization_manifest.sha256":
        "99d8eb8260775b3f2e00bfb51790a6db45a1307753183d61173a2307033c407d",
    "cm2_round270_source_g_outgoing_g_factor_signature_"
    "materialization_manifest.sha256":
        "a23fc6c40b6a29314a9ed7eded86e10242d88a657a321df0c6cfd1b081a8e851",
    "cm2_round271_source_g_wall_and_outgoing_tail_signature_"
    "materialization_manifest.sha256":
        "6c6b710b3d04c24f962ecb00399ea7d2bccf64650b5e78af36a59c2a754f0697",
    "cm2_round272_source_g_boundary_dual_factor_wall_"
    "closure_manifest.sha256":
        "82124ccbc3fa88fadb1f2a3239634dca332ccc959f7338c44cd27908e4957e5a",
    "cm2_round279_source_g_collar_atom_and_face_edge_freeze_manifest.sha256":
        "dc726fde4395c23bd528ef4fc674289bb224c42e023520487676c3deafca12ac",
    "cm2_round288_source_g_canonical_atom_occurrence_identity_gate_audit_"
    "manifest.sha256":
        "c15e4657051318f1a4e6aadcf80fa679840969c7f2c776e65460ac05cc2eb1eb",
    "cm2_round290_source_g_isolated_atom_inner_support_closure_manifest.sha256":
        "e4e4b0614d810bb0516902e173ea7c816f1cecdea162d202ff058200b3d83189",
    "cm2_round294_source_g_occurrence_registry_atomic_promotion_manifest.sha256":
        "90d5cda0271610bf95a72f94e9bae8e192425580019dd3c823b5a69d20e52131",
    "cm2_round300d_source_g_lower_physical_witness_component_edge_promotion_"
    "manifest.sha256":
        "8dd3907a363ae0c4fe7d524061a02b4c70944ce870ded941d5d617911ea1124e",
    "cm2_round301_source_g_legal_component_dsu_application_manifest.sha256":
        "5789b23e74b6e0db9a1b4e311fb22ebe5e3612e4972d2fc3547957230fda214c",
}

# Exact pin map serialized by the producer result.  The four Gate3/Gate5
# formula artifacts and the Round288 overlap ledger are additional
# verifier-only evidence and deliberately do not alter the producer schema.
RESULT_INPUT_PINS = {
    name: pin
    for name, pin in {**FILE_PINS, **MANIFEST_PINS}.items()
    if name not in {
        R288_OVERLAPS,
        GATE5_MANIFEST,
        GATE3_FIRST_HIT_SPEC,
        GATE3_ATLAS_SPEC,
        GATE3_INTERVAL_SPEC,
    }
}

# The caps are per artifact, not a shared permissive default.
FILE_SIZE_CAPS = {
    R179_KERNEL: 4 << 20,
    R269_CERT: 384 << 20,
    R301_MEMBER: 192 << 20,
    R182_ROWS: 192 << 20,
    R179_ROWS: 160 << 20,
    R288_DISPOSITIONS: 160 << 20,
    R279_ATOMS: 128 << 20,
    R271_CERT: 128 << 20,
    R279_EDGES: 128 << 20,
    R294_REGISTRY: 320 << 20,
    R300D_LEDGER: 96 << 20,
    R290_SUPPORT: 32 << 20,
    R301_INELIGIBLE: 48 << 20,
    R270_CERT: 64 << 20,
    R288_OVERLAPS: 32 << 20,
    R272_CERT: 4 << 20,
    R179_VERIFICATION: 8 << 20,
    R182_VERIFICATION: 8 << 20,
    R269_VERIFICATION: 8 << 20,
    R270_VERIFICATION: 8 << 20,
    R271_VERIFICATION: 8 << 20,
    R272_VERIFICATION: 8 << 20,
    R279_VERIFICATION: 8 << 20,
    R288_VERIFICATION: 8 << 20,
    R290_VERIFICATION: 8 << 20,
    R294_VERIFICATION: 8 << 20,
    R300D_VERIFICATION: 8 << 20,
    R301_VERIFICATION: 8 << 20,
    GATE5_MANIFEST: 1 << 20,
    GATE3_FIRST_HIT_SPEC: 4 << 20,
    GATE3_ATLAS_SPEC: 4 << 20,
    GATE3_INTERVAL_SPEC: 4 << 20,
}

PIN_RE = re.compile(r"^[0-9a-f]{64}$")
STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
NEW288 = "CANDIDATE_NEW_ROUND288_CANONICAL_ATOM"
R301_RELATION = (
    "R300D_CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE"
)
R301_RESIDUAL = "INELIGIBLE_INCIDENCE_ONLY__NO_STRONGER_GATE_PROOF"
NEW_PAIR = f"{NEW288}|{NEW288}"
W_TAIL_PREFIX = "round271-W-tail-side:"
W_TAIL_CLASS = (
    "ROUND271_OUTGOING_W_TAIL_FACTOR_SIDE__ENVELOPE_NOT_INNER_BOX"
)

MAX_ANCHOR_SIGN_SPLIT_DEPTH = 18
MAX_ANCHOR_SIGN_SEARCH_NODES = 4_096
MAX_DECOMPRESSED_CANDIDATE_BYTES = 2_000_000_000
MAX_STREAM_ROW_BYTES = 8 << 20
PRECISION_BITS = 256

EXPECTED_SUPPORT_KIND_HISTOGRAM = {
    "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT": 72_712,
    "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT": 15_120,
}
EXPECTED_CONNECTED_CONTRACT_HISTOGRAM = {
    "ROUND269_DIRECT_WHOLE_LEAF_F_SIGN_SIDE": 12_864,
    "ROUND270_DIRECT_WHOLE_LEAF_F_SIGN_SIDE": 26_144,
    "ROUND271_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_WHOLE_F_SIGN_SIDE":
        48_752,
    "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_WHOLE_F_SIGN_SIDE":
        64,
}
EXPECTED_SOURCE_REFERENCE_HISTOGRAM = {
    "269": 12_864,
    "270": 26_144,
    "271": 48_764,
    "272": 64,
}


class VerificationError(RuntimeError):
    """A fail-closed verification failure."""


def need(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


ENCODER = json.JSONEncoder(
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=True,
    allow_nan=False,
)


def canonical_chunks(value: Any) -> Iterable[bytes]:
    for token in ENCODER.iterencode(value):
        yield token.encode("ascii")


def canonical(value: Any) -> bytes:
    return b"".join(canonical_chunks(value))


def digest(value: Any) -> str:
    state = hashlib.sha256()
    for chunk in canonical_chunks(value):
        state.update(chunk)
    return state.hexdigest()


def file_sha256(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in output, "duplicate JSON key:" + key)
        output[key] = value
    return output


def reject_float(token: str) -> Any:
    raise VerificationError("forbidden noninteger JSON number:" + token)


def reject_large_int(token: str) -> int:
    need(
        len(token.lstrip("-")) <= 20,
        "oversized JSON integer token",
    )
    return int(token)


def strict_decoder() -> json.JSONDecoder:
    return json.JSONDecoder(
        object_pairs_hook=strict_object,
        parse_int=reject_large_int,
        parse_float=reject_float,
        parse_constant=reject_float,
    )


def validate_tree(value: Any, *, depth: int = 0) -> None:
    need(depth <= 64, "JSON nesting depth")
    if type(value) is str:
        need(
            len(value) <= (1 << 20)
            and "\x00" not in value
            and not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            "JSON string boundary",
        )
    elif type(value) is list:
        for item in value:
            validate_tree(item, depth=depth + 1)
    elif type(value) is dict:
        for key, item in value.items():
            validate_tree(key, depth=depth + 1)
            validate_tree(item, depth=depth + 1)
    else:
        need(
            value is None or type(value) in {bool, int},
            "JSON scalar type",
        )


def strict_json_bytes(
    raw: bytes,
    label: str,
    *,
    exact_bytes: bytes | None = None,
) -> dict[str, Any]:
    need(
        raw
        and not raw.startswith(b"\xef\xbb\xbf")
        and b"\x00" not in raw,
        "strict JSON byte prefix:" + label,
    )
    try:
        text = raw.decode("utf-8")
        value = strict_decoder().decode(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("strict JSON decode:" + label) from error
    need(type(value) is dict, "JSON top-level object:" + label)
    validate_tree(value)
    if exact_bytes is not None:
        need(
            raw == exact_bytes == canonical(value),
            "canonical JSON bytes:" + label,
        )
    return value


def safe_regular(path: Path, cap: int) -> os.stat_result:
    need(path.parent.resolve() == HERE.resolve(), "HERE-only path")
    info = os.lstat(path)
    need(
        stat.S_ISREG(info.st_mode)
        and not path.is_symlink()
        and info.st_nlink == 1
        and 0 < info.st_size <= cap,
        "regular single-link bounded path:" + path.name,
    )
    return info


def parse_manifest(name: str) -> dict[str, str]:
    path = HERE / name
    safe_regular(path, 512 << 10)
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
        need(match is not None, "manifest syntax:" + name)
        pin, member = match.groups()
        need(
            member not in entries
            and not Path(member).is_absolute()
            and ".." not in Path(member).parts,
            "manifest member policy:" + name,
        )
        entries[member] = pin
    need(bool(entries), "nonempty manifest:" + name)
    return entries


def validate_input_boundary() -> None:
    for name, expected in FILE_PINS.items():
        need(PIN_RE.fullmatch(expected) is not None, "file pin shape:" + name)
        path = HERE / name
        safe_regular(path, FILE_SIZE_CAPS[name])
        need(file_sha256(path) == expected, "file pin:" + name)
    for name, expected in MANIFEST_PINS.items():
        need(
            PIN_RE.fullmatch(expected) is not None,
            "manifest pin shape:" + name,
        )
        path = HERE / name
        safe_regular(path, 512 << 10)
        need(file_sha256(path) == expected, "manifest pin:" + name)
        entries = parse_manifest(name)
        basename_members = {
            Path(member).name: pin for member, pin in entries.items()
        }
        relevant = [
            member
            for member in FILE_PINS
            if member in basename_members
        ]
        for member in relevant:
            need(
                basename_members[member] == FILE_PINS[member],
                "manifest selected member:" + member,
            )


def verify_closed_row(row: dict[str, Any], label: str) -> None:
    claimed = row.get("row_sha256")
    need(
        isinstance(claimed, str) and PIN_RE.fullmatch(claimed) is not None,
        "row SHA shape:" + label,
    )
    payload = dict(row)
    payload.pop("row_sha256")
    need(digest(payload) == claimed, "row SHA closure:" + label)


def close_row(payload: dict[str, Any]) -> dict[str, Any]:
    need("row_sha256" not in payload, "fresh row payload")
    output = dict(payload)
    output["row_sha256"] = digest(payload)
    return output


class ListHash:
    def __init__(self) -> None:
        self.state = hashlib.sha256(b"[")
        self.count = 0

    def add(self, value: Any) -> None:
        if self.count:
            self.state.update(b",")
        for token in canonical_chunks(value):
            self.state.update(token)
        self.count += 1

    def finish(self) -> str:
        result = self.state.copy()
        result.update(b"]")
        return result.hexdigest()


def iter_array_stream(stream: TextIO, marker: str) -> Iterator[Any]:
    if marker:
        buffer = ""
        while marker not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "missing array marker:" + marker)
            buffer = (buffer + block)[-(len(marker) + (2 << 20)) :]
        buffer = buffer.split(marker, 1)[1]
    else:
        buffer = stream.read(1 << 20)
        need(bool(buffer), "empty streamed array tail")
    decoder = strict_decoder()
    while True:
        buffer = buffer.lstrip()
        if not buffer:
            block = stream.read(1 << 20)
            need(bool(block), "truncated streamed array:" + marker)
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
                need(
                    len(buffer.encode("utf-8")) <= MAX_STREAM_ROW_BYTES,
                    "streamed row byte cap:" + marker,
                )
                block = stream.read(1 << 20)
                need(bool(block), "truncated streamed row:" + marker)
                buffer += block
        validate_tree(value)
        yield value
        buffer = buffer[end:]


def iter_named_array(name: str, table: str) -> Iterator[Any]:
    path = HERE / name
    opener: Callable[..., Any] = gzip.open if name.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", newline="") as stream:
        yield from iter_array_stream(
            stream,
            json.dumps(table, ensure_ascii=True) + ":[",
        )


def matching_container_end(
    data: mmap.mmap,
    start: int,
) -> int:
    opening = data[start]
    need(opening in {ord("{"), ord("[")}, "container opening")
    closing = ord("}") if opening == ord("{") else ord("]")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(data)):
        byte = data[index]
        if in_string:
            if escaped:
                escaped = False
            elif byte == ord("\\"):
                escaped = True
            elif byte == ord('"'):
                in_string = False
            continue
        if byte == ord('"'):
            in_string = True
        elif byte == opening:
            depth += 1
        elif byte == closing:
            depth -= 1
            if depth == 0:
                return index
    raise VerificationError("unterminated JSON container")


PACKED_RESULT_SCHEMAS = {
    R179_ROWS:
        "cm2.round179.source-g-residual-tube-arrangement-rows.v1",
    R182_ROWS:
        "cm2.round182.source-g-clipped-graph-and-pair-arrangement-rows.v1",
}


def locate_actual_packed_array(
    name: str,
    table: str,
    columns: tuple[str, ...],
) -> int:
    """Locate a direct result table, excluding its schema-name duplicate."""

    path = HERE / name
    marker = canonical(table) + b":["
    schema_object_marker = b'"row_column_schemas":{'
    expected_suffix = (
        b',"schema":'
        + canonical(PACKED_RESULT_SCHEMAS[name])
        + b"}\n"
    )
    with path.open("rb") as stream:
        with mmap.mmap(
            stream.fileno(), length=0, access=mmap.ACCESS_READ
        ) as data:
            need(
                data[:11] == b'{"result":{'
                and data[-len(expected_suffix):] == expected_suffix,
                "packed result exact wrapper:" + name,
            )
            schema_marker_positions: list[int] = []
            cursor = 0
            while True:
                position = data.find(schema_object_marker, cursor)
                if position < 0:
                    break
                schema_marker_positions.append(position)
                cursor = position + 1
            need(
                len(schema_marker_positions) == 1,
                "unique row_column_schemas object:" + name,
            )
            schema_open = (
                schema_marker_positions[0]
                + len(schema_object_marker) - 1
            )
            schema_close = matching_container_end(data, schema_open)

            positions: list[int] = []
            cursor = 0
            while True:
                position = data.find(marker, cursor)
                if position < 0:
                    break
                positions.append(position)
                cursor = position + 1
                need(
                    len(positions) <= 2,
                    "ambiguous packed table marker:" + table,
                )
            schema_positions = [
                position for position in positions
                if schema_open < position < schema_close
            ]
            actual_positions = [
                position for position in positions
                if not (schema_open < position < schema_close)
            ]
            result_close = data.rfind(b'},"result_sha256":"')
            need(
                len(positions) == 2
                and len(schema_positions) == 1
                and len(actual_positions) == 1
                and 11 <= actual_positions[0] < result_close
                and schema_close < result_close,
                "unique direct result packed table:" + table,
            )

            schema_array_open = schema_positions[0] + len(marker) - 1
            schema_array_close = matching_container_end(
                data, schema_array_open
            )
            schema_columns = strict_decoder().decode(
                data[schema_array_open:schema_array_close + 1].decode(
                    "ascii"
                )
            )
            need(
                schema_columns == list(columns),
                "packed table declared column schema:" + table,
            )
            return actual_positions[0] + len(marker)


def iter_actual_packed_array(
    name: str,
    table: str,
    columns: tuple[str, ...],
) -> Iterator[Any]:
    offset = locate_actual_packed_array(name, table, columns)
    with (HERE / name).open("rb") as raw:
        raw.seek(offset)
        with io.TextIOWrapper(
            raw, encoding="utf-8", newline=""
        ) as stream:
            yield from iter_array_stream(stream, "")


@dataclass(frozen=True)
class Commitment:
    count: int
    ids: str
    hashes: str
    rows: str


COMMITMENTS = {
    "R301_MEMBER": Commitment(
        564_492,
        "1aeef7c94cd785385b03aa8cd6e29ed16eee3056e499fb135c66c300ccb1ebbd",
        "ec2a3d4a192d49d9f4e1466b46acae06a34fc748c3838e2539c5eccdc1d5cc92",
        "d38fb616d7d6416c2933932a4d1779836946b98f0dbe1fa45eb1939dc2e0e5d7",
    ),
    "R301_INELIGIBLE": Commitment(
        119_844,
        "676926e533c6dd33d6a5b799717d4cf218ebf9cc512012d123de1fb314e3e3d5",
        "dbcb0fd5bb4d107df220bad633f526a69f0d3e3a54732e79304055cd0df773f0",
        "6b3d484c44b9d5b60919f209633d712a6fdd5e309282bf29318b8498a19ca7f4",
    ),
    "R300D": Commitment(
        111_524,
        "19ce53e77604142bf0410e49b1f1c8bf921beb715538901776c517d098626c6b",
        "97f5ae7ffde9c583bf0cc75e6ad685c4d22cdc487261576b8e904a69fcad17d2",
        "3623738c4a7a41980b6386d089f319d5149358e7e91fb422053289068eedbc8b",
    ),
    "R294": Commitment(
        431_208,
        "bbaca3ecbb804a87fd509aac2b8bd9f505d0c008e7bddbeb1a2ecb2a966f5509",
        "ea98de3dab7e6f308f5a07d04bc29ca0d9dcd265a5323d8ecdb728cc501eed56",
        "33936ecd04cbce9f9a308b0da10381bd854b45028db53db5d3cbb9aa8b264044",
    ),
    "R288": Commitment(
        332_016,
        "09a0039e5d9e82413c949823697c794fc65095c1f71d2e6c2f576df0699ec13b",
        "30a167baab36fab7e3e37fd0014c35b9fd94b5491494d21c83dc39080e191f50",
        "8007b0c96e44c76bea6038fed8430134f9f424c7a81508f843d72d473f768849",
    ),
    "R279_ATOMS": Commitment(
        332_016,
        "a685a017d5ae1a4d735a84142b3a2f2c3ed1b3cd2be3c41ad3dca3297f0acbe3",
        "52aed35a8b1b423da27c7b6f05bc6f6721398c606ebe7ec3239770ada9f8887f",
        "d2680baed100e4e1a236aa929999c7d93be5eeddabb2cc0660fca5e756882105",
    ),
    "R279_EDGES": Commitment(
        330_724,
        "5ef215767717f96cab2f4efb29851f41f2efbe8f5aec1c63e4ddef486abe8e92",
        "29efd6ba3b9b1a04580cf2a2593496bd5c1ddabffdb0eab9eaea9f0ac2762b78",
        "bfcb9979545b6abb2e85d54e0200f4394b6e967dbb888e3bcda7ee726cdc6bf7",
    ),
    "R290": Commitment(
        21_160,
        "90364fbc92c8ec21100eba1d7ba5cb8ceeb616506f138dfdc21315e63709edb1",
        "925b4c51ea0c6ee2142a4b4fdf4c20cedb351fb24044c953fa5faf3652cefc81",
        "3ab9344c1fa492d87eee4937d11659872ea848c6ff9bf02419c10ae77a0636cd",
    ),
}


def committed_rows(
    name: str,
    table: str,
    id_field: str,
    expected: Commitment,
) -> Iterator[dict[str, Any]]:
    row_hash = ListHash()
    id_hash = ListHash()
    sha_hash = ListHash()
    seen: set[str] = set()
    for value in iter_named_array(name, table):
        need(type(value) is dict, "streamed row object:" + name)
        row = value
        verify_closed_row(row, name)
        row_id = row.get(id_field)
        need(
            isinstance(row_id, str) and row_id not in seen,
            "unique row ID:" + name,
        )
        seen.add(row_id)
        row_hash.add(row)
        id_hash.add(row_id)
        sha_hash.add(row["row_sha256"])
        yield row
    need(
        Commitment(
            row_hash.count,
            id_hash.finish(),
            sha_hash.finish(),
            row_hash.finish(),
        )
        == expected,
        "complete table commitment:" + name,
    )


def exact_pair(value: Any, label: str) -> tuple[str, str]:
    need(
        type(value) is list
        and len(value) == 2
        and all(type(item) is str for item in value),
        "endpoint pair shape:" + label,
    )
    left, right = value
    need(left < right, "canonical endpoint order:" + label)
    return left, right


@dataclass(frozen=True)
class CrossEndpoint:
    occurrence_id: str
    source_R300D_row_id: str
    source_R300D_row_sha256: str
    source_Round301_ineligible_row_id: str
    source_Round301_ineligible_row_sha256: str
    peer_occurrence_id: str
    Round301_component_id: str
    peer_Round301_component_id: str
    Round301_member_row_id: str
    Round301_member_row_sha256: str
    expected_registry_row_id: str
    expected_registry_row_sha256: str


def collect_cross_component_new_endpoints() -> dict[str, CrossEndpoint]:
    residual: dict[
        str, tuple[tuple[str, str], str, str, str]
    ] = {}
    all_endpoints: set[str] = set()
    for row in committed_rows(
        R301_INELIGIBLE,
        "rows",
        "Round301_ineligible_source_consumption_row_id",
        COMMITMENTS["R301_INELIGIBLE"],
    ):
        if (
            row["source_relation"] != R301_RELATION
            or row["disposition"] != R301_RESIDUAL
        ):
            continue
        source_id = row["source_row_id"]
        pair = exact_pair(
            row["canonical_occurrence_endpoint_pair"],
            source_id,
        )
        need(
            source_id not in residual
            and row["source_row_fed_to_DSU"] is False
            and row["eligible_for_component_DSU_application"] is False
            and row["formal_component_edge_application_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "Round301 residual fail-closed contract:" + source_id,
        )
        residual[source_id] = (
            pair,
            row["source_row_sha256"],
            row["Round301_ineligible_source_consumption_row_id"],
            row["row_sha256"],
        )
        all_endpoints.update(pair)
    need(
        len(residual) == 110_516 and len(all_endpoints) == 221_032,
        "complete Round300D residual source scope",
    )

    components: dict[str, tuple[str, str, str]] = {}
    for row in committed_rows(
        R301_MEMBER,
        "rows",
        "Round301_member_to_component_row_id",
        COMMITMENTS["R301_MEMBER"],
    ):
        endpoint = row["registry_or_frontier_member_id"]
        if endpoint not in all_endpoints:
            continue
        need(
            endpoint not in components
            and row["member_identity_preserved"] is True
            and row["formal_occurrence_identity_collapse_credit"] == 0,
            "Round301 member projection:" + endpoint,
        )
        components[endpoint] = (
            row["final_Round301_component_id"],
            row["Round301_member_to_component_row_id"],
            row["row_sha256"],
        )
    need(set(components) == all_endpoints, "Round301 endpoint coverage")

    cross_sources = {
        source_id
        for source_id, (pair, _sha, _ineligible_id, _ineligible_sha)
        in residual.items()
        if components[pair[0]][0] != components[pair[1]][0]
    }
    need(len(cross_sources) == 44_108, "Round301 cross-component census")

    selected: dict[str, CrossEndpoint] = {}
    new_pair_count = 0
    preserved_pair_count = 0
    seen_sources: set[str] = set()
    for row in committed_rows(
        R300D_LEDGER,
        "canonical_incidence_edge_rows",
        "Round300D_lower_physical_witness_incidence_edge_row_id",
        COMMITMENTS["R300D"],
    ):
        source_id = row["Round300D_lower_physical_witness_incidence_edge_row_id"]
        if source_id not in cross_sources:
            continue
        seen_sources.add(source_id)
        pair = exact_pair(
            row["canonical_unordered_Round294_registry_occurrence_ids"],
            source_id,
        )
        need(
            pair == residual[source_id][0]
            and row["row_sha256"] == residual[source_id][1],
            "Round300D/Round301 exact source binding:" + source_id,
        )
        if row["endpoint_tranche_relation"] != NEW_PAIR:
            need(
                row["endpoint_tranche_relation"]
                == (
                    "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE|"
                    "PRESERVED_ROUND266_EXISTING_LOCAL_OCCURRENCE"
                ),
                "known cross-component tranche:" + source_id,
            )
            preserved_pair_count += 1
            continue
        new_pair_count += 1
        endpoint_rows = {
            row["left_endpoint"]["registry_occurrence_id"]:
                row["left_endpoint"],
            row["right_endpoint"]["registry_occurrence_id"]:
                row["right_endpoint"],
        }
        need(
            set(endpoint_rows) == set(pair),
            "Round300D endpoint object coverage:" + source_id,
        )
        for endpoint in pair:
            peer = pair[1] if endpoint == pair[0] else pair[0]
            item = endpoint_rows[endpoint]
            need(
                endpoint not in selected
                and item["registry_entry_kind"] == NEW288
                and item["preserved_Round266_provenance"] is None,
                "unique new Round288 endpoint:" + endpoint,
            )
            selected[endpoint] = CrossEndpoint(
                occurrence_id=endpoint,
                source_R300D_row_id=source_id,
                source_R300D_row_sha256=row["row_sha256"],
                source_Round301_ineligible_row_id=
                    residual[source_id][2],
                source_Round301_ineligible_row_sha256=
                    residual[source_id][3],
                peer_occurrence_id=peer,
                Round301_component_id=components[endpoint][0],
                peer_Round301_component_id=components[peer][0],
                Round301_member_row_id=components[endpoint][1],
                Round301_member_row_sha256=components[endpoint][2],
                expected_registry_row_id=item[
                    "Round294_occurrence_registry_row_id"
                ],
                expected_registry_row_sha256=item[
                    "Round294_occurrence_registry_row_sha256"
                ],
            )
    need(
        seen_sources == cross_sources
        and new_pair_count == 43_916
        and preserved_pair_count == 192
        and len(selected) == 87_832,
        "exact Round303A cross-scope partition",
    )
    return selected


@dataclass
class EndpointEvidence:
    scope: CrossEndpoint
    registry: dict[str, Any]
    disposition: dict[str, Any] | None = None
    atom: dict[str, Any] | None = None
    support: dict[str, Any] | None = None
    source_rows: list[tuple[int, dict[str, Any]]] | None = None
    leaf: dict[str, Any] | None = None
    occurrence: dict[str, Any] | None = None
    origin: dict[str, Any] | None = None
    normal_form: dict[str, Any] | None = None


def collect_registry(
    scope: dict[str, CrossEndpoint],
) -> dict[str, EndpointEvidence]:
    output: dict[str, EndpointEvidence] = {}
    for row in committed_rows(
        R294_REGISTRY,
        "rows",
        "Round294_occurrence_registry_row_id",
        COMMITMENTS["R294"],
    ):
        occurrence_id = row["registry_occurrence_id"]
        requirement = scope.get(occurrence_id)
        if requirement is None:
            continue
        need(
            occurrence_id not in output
            and row["Round294_occurrence_registry_row_id"]
            == requirement.expected_registry_row_id
            and row["row_sha256"]
            == requirement.expected_registry_row_sha256
            and row["registry_entry_kind"] == NEW288
            and row["registry_identity_status"]
            == "FORMALLY_ISSUED_ROUND294_ATOMIC_OCCURRENCE_ID"
            and row["registry_promotion_status"]
            == "FORMALLY_PROMOTED_ROUND294_ATOMIC_OCCURRENCE_REGISTRY"
            and row["formal_new_expanded_occurrence_credit"] == 1
            and row["formal_occurrence_alias_credit"] == 0
            and row["formal_DSU_rank_reduction_credit"] == 0,
            "Round294 issued occurrence contract:" + occurrence_id,
        )
        need(
            row["registry_source_identity"]
            == "ROUND288_CANONICAL_ATOM::" + row["canonical_atom_id"]
            and occurrence_id
            == "source-g-expanded-occurrence:"
            + row["occurrence_id_content_preimage_sha256"],
            "Round294 content identity:" + occurrence_id,
        )
        output[occurrence_id] = EndpointEvidence(requirement, row)
    need(set(output) == set(scope), "Round294 selected registry coverage")
    return output


def collect_dispositions(
    endpoints: dict[str, EndpointEvidence],
) -> None:
    by_source = {
        item.registry["source_row_id"]: occurrence_id
        for occurrence_id, item in endpoints.items()
    }
    need(len(by_source) == len(endpoints), "unique Round288 source rows")
    seen: set[str] = set()
    for row in committed_rows(
        R288_DISPOSITIONS,
        "rows",
        "Round288_atom_disposition_row_id",
        COMMITMENTS["R288"],
    ):
        occurrence_id = by_source.get(row["Round288_atom_disposition_row_id"])
        if occurrence_id is None:
            continue
        item = endpoints[occurrence_id]
        registry = item.registry
        need(
            occurrence_id not in seen
            and row["row_sha256"] == registry["source_row_sha256"]
            and row["canonical_atom_id"] == registry["canonical_atom_id"]
            and row["reserved_candidate_occurrence_id__not_issued"]
            == occurrence_id
            and row["existing_local_occurrence_row_id"] is None
            and row["positive_volume_existing_overlap_count"] == 0
            and row["formal_new_occurrence_credit"] == 0
            and row["formal_component_credit"] == 0
            and row["formal_maximality_credit"] == 0
            and row["Round182_leaf_row_id"]
            == registry["Round182_leaf_row_id"]
            and row["complete_10_field_return_signature_sha256"]
            == registry["complete_10_field_return_signature_sha256"]
            and row["source_signature_row_ids"]
            == registry["source_signature_row_ids"],
            "Round288/Round294 exact disposition binding:" + occurrence_id,
        )
        item.disposition = row
        seen.add(occurrence_id)
    need(seen == set(endpoints), "Round288 selected disposition coverage")


def collect_atoms(endpoints: dict[str, EndpointEvidence]) -> None:
    by_atom = {
        item.registry["canonical_atom_id"]: occurrence_id
        for occurrence_id, item in endpoints.items()
    }
    need(len(by_atom) == len(endpoints), "unique selected canonical atoms")
    seen: set[str] = set()
    for row in committed_rows(
        R279_ATOMS,
        "rows",
        "canonical_atom_id",
        COMMITMENTS["R279_ATOMS"],
    ):
        occurrence_id = by_atom.get(row["canonical_atom_id"])
        if occurrence_id is None:
            continue
        item = endpoints[occurrence_id]
        disposition = item.disposition
        need(disposition is not None, "Round288 join order")
        need(
            occurrence_id not in seen
            and row["new_occurrence_region_atom_candidate"] is True
            and row["existing_Round208_occurrence_row_ids"] == []
            and row["expanded_occurrence_credit"] == 0
            and row["component_credit"] == 0
            and row["maximality_credit"] == 0
            and row["Round182_leaf_row_id"]
            == disposition["Round182_leaf_row_id"]
            and row["complete_10_field_return_signature_sha256"]
            == disposition["complete_10_field_return_signature_sha256"]
            and row["source_signature_row_ids"]
            == disposition["source_signature_row_ids"]
            and row["source_rounds"] == disposition["source_rounds"],
            "Round279/Round288 canonical atom binding:" + occurrence_id,
        )
        need(
            row["canonical_atom_id"]
            == "round279-collar-atom:"
            + digest([
                row["Round182_leaf_row_id"],
                row["complete_10_field_return_signature_sha256"],
            ]),
            "independent canonical atom ID:" + occurrence_id,
        )
        item.atom = row
        seen.add(occurrence_id)
    need(seen == set(endpoints), "Round279 selected atom coverage")


def collect_support_rows(endpoints: dict[str, EndpointEvidence]) -> None:
    by_r290: dict[str, str] = {}
    by_r279_edge: dict[str, list[str]] = defaultdict(list)
    for occurrence_id, item in endpoints.items():
        registry = item.registry
        kind = registry["support_representation_kind"]
        if kind == "ROUND290_ISOLATED_ATOM_RATIONAL_INNER_SUPPORT":
            source_id = registry["source_Round290_inner_support_row_id"]
            need(
                isinstance(source_id, str)
                and registry["source_Round279_formal_face_edge_witness_row_id"]
                is None,
                "Round290 support selector:" + occurrence_id,
            )
            by_r290[source_id] = occurrence_id
        else:
            need(
                kind
                == "ROUND279_DYNAMIC_STRICT_INWARD_CORRIDOR_INNER_SUPPORT",
                "known support representation:" + occurrence_id,
            )
            source_id = registry[
                "source_Round279_formal_face_edge_witness_row_id"
            ]
            need(
                isinstance(source_id, str)
                and registry["source_Round290_inner_support_row_id"] is None,
                "Round279 support selector:" + occurrence_id,
            )
            by_r279_edge[source_id].append(occurrence_id)
    need(
        len(by_r290)
        + sum(len(values) for values in by_r279_edge.values())
        == len(endpoints),
        "complete support source endpoint references",
    )

    seen_r290: set[str] = set()
    for row in committed_rows(
        R290_SUPPORT,
        "rows",
        "Round290_inner_support_row_id",
        COMMITMENTS["R290"],
    ):
        occurrence_id = by_r290.get(row["Round290_inner_support_row_id"])
        if occurrence_id is None:
            continue
        item = endpoints[occurrence_id]
        registry = item.registry
        disposition = item.disposition
        need(disposition is not None, "Round290 join order")
        need(
            occurrence_id not in seen_r290
            and row["row_sha256"]
            == registry["source_Round290_inner_support_row_sha256"]
            == registry["support_source_row_sha256"]
            and row["canonical_atom_id"] == registry["canonical_atom_id"]
            and row["Round288_atom_disposition_row_id"]
            == disposition["Round288_atom_disposition_row_id"]
            and row["exact_positive_volume_rational_inner_support_box"]
            == registry["positive_volume_rational_inner_support_box"]
            and row["exact_inner_support_volume"]
            == registry["exact_inner_support_volume"]
            and row["dynamic_signature_constant_on_whole_inner_box"] is True
            and row["whole_leaf_envelope_used_as_inner_support"] is False
            and row["point_witness_used_as_inner_support"] is False,
            "Round290 exact support binding:" + occurrence_id,
        )
        item.support = {
            "support_source_kind": "ROUND290_ISOLATED_INNER_SUPPORT",
            "support_source_row_id": row["Round290_inner_support_row_id"],
            "support_source_row_sha256": row["row_sha256"],
            "source_signature_row_id": row["source_signature_row_id"],
            "source_round": row["source_round"],
        }
        seen_r290.add(occurrence_id)
    need(
        seen_r290 == set(by_r290.values()),
        "Round290 selected support coverage",
    )

    seen_edges: set[str] = set()
    for row in committed_rows(
        R279_EDGES,
        "rows",
        "formal_face_edge_witness_row_id",
        COMMITMENTS["R279_EDGES"],
    ):
        occurrence_ids = by_r279_edge.get(
            row["formal_face_edge_witness_row_id"]
        )
        if occurrence_ids is None:
            continue
        for occurrence_id in occurrence_ids:
            item = endpoints[occurrence_id]
            registry = item.registry
            disposition = item.disposition
            atom = item.atom
            need(
                disposition is not None and atom is not None,
                "Round279 edge join order",
            )
            selected = disposition[
                "selected_Round279_strict_inner_corridor"
            ]
            need(
                occurrence_id not in seen_edges
                and selected is not None
                and selected["formal_face_edge_witness_row_id"]
                == row["formal_face_edge_witness_row_id"]
                and selected["witness_partition"]
                == row["witness_partition"],
                "Round279 selected edge binding:" + occurrence_id,
            )
            matching_atoms = [
                endpoint
                for endpoint in row["endpoint_atoms"]
                if endpoint["canonical_atom_id"]
                == registry["canonical_atom_id"]
            ]
            matching = [
                corridor
                for corridor in row["two_inward_corridors"]
                if corridor["leaf_row_id"]
                == registry["Round182_leaf_row_id"]
            ]
            need(
                len(matching_atoms) == len(matching) == 1
                and row["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and row["source_chart"] == atom["source_chart"]
                and row["owner_target"] == atom["owner_target"]
                and matching[0]["exact_corridor_box"]
                == registry["positive_volume_rational_inner_support_box"]
                == selected[
                    "exact_positive_volume_rational_inner_support_box"
                ],
                "Round279 exact inward corridor:" + occurrence_id,
            )
            item.support = {
                "support_source_kind":
                    "ROUND279_DYNAMIC_CORRIDOR",
                "support_source_row_id": row[
                    "formal_face_edge_witness_row_id"
                ],
                "support_source_row_sha256": row["row_sha256"],
                "corridor_leaf_row_id": matching[0]["leaf_row_id"],
                "corridor_geometric_side":
                    matching[0]["geometric_side"],
                "corridor_dyadic_normal_depth":
                    matching[0]["dyadic_normal_depth"],
            }
            seen_edges.add(occurrence_id)
    need(
        seen_edges
        == {
            occurrence_id
            for occurrence_ids in by_r279_edge.values()
            for occurrence_id in occurrence_ids
        },
        "Round279 selected support coverage",
    )


SOURCE_SPECS = {
    269: (
        R269_CERT,
        "formal_direct_side_signature_ledger",
        "signed_region_row_id",
        187_128,
        "992392cc52465cd5ea427e7776fc16fd889048553950b5338042581c14d98755",
    ),
    270: (
        R270_CERT,
        "formal_direct_side_signature_ledger",
        "signed_region_row_id",
        37_712,
        "6f23d7d545ff8c3add454fe01da64d095f237222228c1dd382ca9b19420d746e",
    ),
    271: (
        R271_CERT,
        "formal_side_signature_ledger",
        "signed_region_row_id",
        70_420,
        "cec8a0318385127d8ee5d7968c016f8f6b7ee103596fbce5258cc3b25c4930b8",
    ),
    272: (
        R272_CERT,
        "formal_side_signature_ledger",
        "signed_region_row_id",
        720,
        "f23f389e39a9715f67fa827026072db638aee34c6f1e539b5ec36bf225e075da",
    ),
}


def iter_certificate_ledger_rows(
    name: str,
    ledger_name: str,
) -> Iterator[dict[str, Any]]:
    path = HERE / name
    with path.open("rt", encoding="utf-8", newline="") as stream:
        buffer = ""
        marker = json.dumps(ledger_name) + ":{"
        while marker not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "missing certificate ledger:" + ledger_name)
            buffer = (buffer + block)[-(len(marker) + (2 << 20)) :]
        buffer = buffer.split(marker, 1)[1]
        rows_marker = '"rows":['
        while rows_marker not in buffer:
            block = stream.read(1 << 20)
            need(bool(block), "missing certificate rows:" + ledger_name)
            buffer += block
            need(
                len(buffer.encode("utf-8")) <= (4 << 20),
                "certificate ledger header cap:" + ledger_name,
            )
        buffer = buffer.split(rows_marker, 1)[1]

        # Feed the already-read tail and the remaining stream through the
        # same strict streaming decoder without seeking or reparsing.
        class Prefixed:
            def __init__(self, prefix: str, source: TextIO) -> None:
                self.prefix = prefix
                self.source = source

            def read(self, size: int = -1) -> str:
                if self.prefix:
                    if size < 0:
                        value = self.prefix + self.source.read()
                        self.prefix = ""
                        return value
                    value = self.prefix[:size]
                    self.prefix = self.prefix[size:]
                    if len(value) < size:
                        value += self.source.read(size - len(value))
                    return value
                return self.source.read(size)

        prefixed = Prefixed(buffer, stream)
        yield from iter_array_stream(prefixed, "")


def source_round_from_id(row_id: str) -> int:
    for round_number in SOURCE_SPECS:
        if row_id.startswith(f"round{round_number}-"):
            return round_number
    raise VerificationError("unknown source signature row ID:" + row_id)


def collect_source_rows(endpoints: dict[str, EndpointEvidence]) -> None:
    required: dict[int, set[str]] = defaultdict(set)
    for item in endpoints.values():
        atom = item.atom
        need(atom is not None, "Round279 atom join order")
        for source_id in atom["source_signature_row_ids"]:
            required[source_round_from_id(source_id)].add(source_id)

    selected: dict[str, tuple[int, dict[str, Any]]] = {}
    for round_number, spec in SOURCE_SPECS.items():
        name, ledger_name, id_field, expected_count, expected_rows_sha = spec
        rows_hash = ListHash()
        seen_ids: set[str] = set()
        for row in iter_certificate_ledger_rows(name, ledger_name):
            need(type(row) is dict, "source row object")
            row_id = row[id_field]
            verify_closed_row(row, row_id)
            need(row_id not in seen_ids, "unique source row:" + row_id)
            seen_ids.add(row_id)
            rows_hash.add(row)
            if row_id in required.get(round_number, set()):
                need(
                    row_id not in selected,
                    "selected source row uniqueness:" + row_id,
                )
                selected[row_id] = (round_number, row)
        need(
            rows_hash.count == expected_count
            and rows_hash.finish() == expected_rows_sha,
            f"complete Round{round_number} source ledger commitment",
        )
        need(
            set(source_id for source_id in selected
                if source_round_from_id(source_id) == round_number)
            == required.get(round_number, set()),
            f"selected Round{round_number} source coverage",
        )

    source_reference_count = 0
    for occurrence_id, item in endpoints.items():
        atom = item.atom
        disposition = item.disposition
        need(atom is not None and disposition is not None, "source join order")
        rows = [selected[source_id] for source_id in atom[
            "source_signature_row_ids"
        ]]
        source_reference_count += len(rows)
        for round_number, row in rows:
            need(
                row["Round182_leaf_row_id"]
                == atom["Round182_leaf_row_id"]
                and row["complete_10_field_return_signature_sha256"]
                == atom["complete_10_field_return_signature_sha256"]
                and digest(row["local_return_signature"])
                == row["complete_10_field_return_signature_sha256"]
                and row["expanded_occurrence_credit"] == 0
                and row["component_edge_credit"] == 0
                and row["maximality_credit"] == 0,
                "source row/canonical atom binding:" + occurrence_id,
            )
            need(
                round_number in disposition["source_rounds"],
                "source round/disposition binding:" + occurrence_id,
            )
        item.source_rows = rows
    need(
        source_reference_count == 87_836,
        "selected source signature reference census",
    )


R182_LEAF_COLUMNS = (
    "row_id",
    "occurrence_row_id",
    "retained_child_row_id",
    "base_refinement_path",
    "box",
    "coordinate_volume",
    "base_coordinate_area",
    "lower_t_face_status",
    "upper_t_face_status",
    "graph_classification",
    "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "closed_3d_side_union_volume",
    "residual_3d_collar_volume",
)
R182_OCCURRENCE_COLUMNS = (
    "row_id",
    "Round179_occurrence_row_id",
    "origin_row_id",
    "parent_id",
    "chart",
    "owner_target",
    "kind",
    "reason_label",
    "equation",
    "target_obstacle",
    "strict_t_derivative_sign",
    "Round179_origin_already_fully_replaced",
    "Round179_retained_child_count",
    "Round179_retained_coordinate_volume",
    "bounded_base_split_axis",
    "bounded_base_split_depth",
    "closed_leaf_count",
    "closed_coordinate_volume",
    "residual_leaf_count",
    "residual_coordinate_volume",
    "full_base_graph_leaf_count",
    "absent_graph_leaf_count",
    "clipped_graph_leaf_count",
    "two_dimensional_graph_sheet_count",
    "one_dimensional_clipping_curve_segment_count",
    "zero_dimensional_boundary_endpoint_incidence_count",
    "fully_clipped_over_Round179_retained_children",
    "leaf_rows_sha256",
    "whole_original_tube_credit",
    "global_exact_key_disposition_credit",
    "provenance",
)
R179_ORIGIN_COLUMNS = (
    "origin_row_id",
    "parent_id",
    "chart",
    "owner_target",
    "original_refinement_path",
    "original_box",
    "original_coordinate_volume",
    "original_reason_labels",
    "reason_count",
    "chosen_split_axis",
    "resolved_child_count",
    "resolved_child_coordinate_volume",
    "guard_child_count",
    "guard_child_coordinate_volume",
    "retained_child_count",
    "retained_child_coordinate_volume",
    "fully_replaced_by_bounded_children",
    "released_exact_key_count",
    "released_exact_key_ordinals_sha256",
    "provenance",
)
R179_OUTGOING_COLUMNS = (
    "row_id",
    "origin_row_id",
    "parent_id",
    "chart",
    "equation",
    "gradient_axis",
    "gradient_sign",
    "regularity_certification",
    "lower_t_face_sign",
    "upper_t_face_sign",
    "face_classification",
    "zero_set_dimension_account",
    "existence_over_full_base",
    "two_open_3d_sides_retained",
    "whole_origin_credit",
    "global_geometric_disposition_credit",
    "provenance",
)
R179_WALL_COLUMNS = (
    "row_id",
    "origin_row_id",
    "parent_id",
    "chart",
    "reason_label",
    "axis",
    "integer_wall",
    "zero_equation",
    "source_factor_classification",
    "source_gradient_axis",
    "source_gradient_sign",
    "target_factor_classification",
    "target_gradient_axis",
    "target_gradient_sign",
    "target_lower_face_sign",
    "target_upper_face_sign",
    "target_face_classification",
    "zero_set_dimension_account",
    "crossing_time_dependency_overwrap_discharged",
    "whole_origin_credit",
    "global_geometric_disposition_credit",
    "provenance",
)


def select_packed_rows(
    name: str,
    table: str,
    columns: tuple[str, ...],
    id_field: str,
    wanted: set[str],
) -> dict[str, dict[str, Any]]:
    id_index = columns.index(id_field)
    output: dict[str, dict[str, Any]] = {}
    for packed in iter_actual_packed_array(name, table, columns):
        need(
            type(packed) is list and len(packed) == len(columns),
            "packed row width:" + table,
        )
        row_id = packed[id_index]
        if row_id not in wanted:
            continue
        need(row_id not in output, "unique packed row:" + row_id)
        output[row_id] = dict(zip(columns, packed, strict=True))
    need(set(output) == wanted, "packed selected coverage:" + table)
    return output


def collect_geometry_rows(endpoints: dict[str, EndpointEvidence]) -> None:
    leaf_ids = {
        item.atom["Round182_leaf_row_id"]
        for item in endpoints.values()
        if item.atom is not None
    }
    leaves = select_packed_rows(
        R182_ROWS,
        "collar_leaf_rows",
        R182_LEAF_COLUMNS,
        "row_id",
        leaf_ids,
    )
    occurrence_ids = {
        leaf["occurrence_row_id"] for leaf in leaves.values()
    }
    occurrences = select_packed_rows(
        R182_ROWS,
        "collar_occurrence_rows",
        R182_OCCURRENCE_COLUMNS,
        "Round179_occurrence_row_id",
        occurrence_ids,
    )
    origin_ids = {
        row["origin_row_id"] for row in occurrences.values()
    }
    origins = select_packed_rows(
        R179_ROWS,
        "origin_tube_rows",
        R179_ORIGIN_COLUMNS,
        "origin_row_id",
        origin_ids,
    )
    outgoing_ids = {
        occurrence_id
        for occurrence_id, row in occurrences.items()
        if row["kind"] == "OUTGOING"
    }
    wall_ids = occurrence_ids - outgoing_ids
    outgoing = (
        select_packed_rows(
            R179_ROWS,
            "outgoing_normal_form_rows",
            R179_OUTGOING_COLUMNS,
            "row_id",
            outgoing_ids,
        )
        if outgoing_ids else {}
    )
    walls = (
        select_packed_rows(
            R179_ROWS,
            "wall_normal_form_rows",
            R179_WALL_COLUMNS,
            "row_id",
            wall_ids,
        )
        if wall_ids else {}
    )
    normal_forms = {**outgoing, **walls}
    need(set(normal_forms) == occurrence_ids, "normal-form coverage")

    for occurrence_id, item in endpoints.items():
        atom = item.atom
        source_rows = item.source_rows
        need(atom is not None and source_rows is not None, "geometry join order")
        leaf = leaves[atom["Round182_leaf_row_id"]]
        occurrence = occurrences[leaf["occurrence_row_id"]]
        origin = origins[occurrence["origin_row_id"]]
        normal_form = normal_forms[leaf["occurrence_row_id"]]
        need(
            atom["Round182_occurrence_row_id"]
            == leaf["occurrence_row_id"]
            and atom["origin_row_id"] == occurrence["origin_row_id"]
            and occurrence["chart"] == origin["chart"]
            == atom["source_chart"]
            == item.registry["physical_support_chart"]
            and occurrence["owner_target"] == origin["owner_target"]
            == atom["owner_target"] == item.registry["owner_target"],
            "chart/owner geometry chain:" + occurrence_id,
        )
        for round_number, source in source_rows:
            need(
                source["Round182_leaf_row_id"] == leaf["row_id"]
                and source["local_return_signature"]["source_chart"]
                == occurrence["chart"]
                and (
                    source.get("occurrence_row_id") is None
                    or source["occurrence_row_id"]
                    == leaf["occurrence_row_id"]
                )
                and (
                    source.get("retained_child_row_id") is None
                    or source["retained_child_row_id"]
                    == leaf["retained_child_row_id"]
                )
                and (
                    source.get("equation") is None
                    or source["equation"] == occurrence["equation"]
                ),
                "source/leaf/occurrence binding:" + occurrence_id,
            )
            if round_number in {269, 270}:
                need(
                    source["retained_child_row_id"]
                    == leaf["retained_child_row_id"],
                    "source retained-child binding:" + occurrence_id,
                )
        item.leaf = leaf
        item.occurrence = occurrence
        item.origin = origin
        item.normal_form = normal_form


@dataclass(frozen=True)
class Box:
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    s0: Q
    s1: Q

    @classmethod
    def from_values(cls, values: Any, label: str) -> "Box":
        need(
            type(values) is list
            and len(values) == 6
            and all(type(value) is str for value in values),
            "box shape:" + label,
        )
        try:
            box = cls(*(Q(value) for value in values))
        except (ValueError, ZeroDivisionError) as error:
            raise VerificationError("rational box:" + label) from error
        need(
            box.t0 <= box.t1
            and box.p0 <= box.p1
            and box.s0 <= box.s1,
            "ordered box:" + label,
        )
        return box

    def values(self) -> list[str]:
        return [
            qstr(self.t0),
            qstr(self.t1),
            qstr(self.p0),
            qstr(self.p1),
            qstr(self.s0),
            qstr(self.s1),
        ]

    def volume(self) -> Q:
        return (
            (self.t1 - self.t0)
            * (self.p1 - self.p0)
            * (self.s1 - self.s0)
        )

    def contains(self, other: "Box") -> bool:
        return (
            self.t0 <= other.t0 <= other.t1 <= self.t1
            and self.p0 <= other.p0 <= other.p1 <= self.p1
            and self.s0 <= other.s0 <= other.s1 <= self.s1
        )

    def split(self, axis: int) -> tuple["Box", "Box"]:
        need(axis in {0, 1, 2}, "split axis")
        values = [
            self.t0, self.t1,
            self.p0, self.p1,
            self.s0, self.s1,
        ]
        low = 2 * axis
        middle = (values[low] + values[low + 1]) / 2
        left = list(values)
        right = list(values)
        left[low + 1] = middle
        right[low] = middle
        return Box(*left), Box(*right)


def arbq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def arb_interval(lower: Q, upper: Q) -> arb:
    need(lower <= upper, "arb interval order")
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return arbq(middle) + arb(0, arbq(radius).upper())


def arb_hull(lower: arb, upper: arb) -> arb:
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return middle + arb(0, radius.upper())


def sqrt_one_minus_square(lower: Q, upper: Q) -> arb:
    need(Q(-1) <= lower <= upper <= Q(1), "sqrt interval domain")
    maximum_abs = max(abs(lower), abs(upper))
    minimum_abs = (
        Q(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))
    )
    value_lower = arbq(1 - maximum_abs * maximum_abs).sqrt()
    value_upper = arbq(1 - minimum_abs * minimum_abs).sqrt()
    return arb_hull(value_lower.lower(), value_upper.upper())


Dual = tuple[arb, tuple[arb | None, arb | None, arb | None]]


def dconstant(value: arb) -> Dual:
    return value, (arb(0), arb(0), arb(0))


def dneg(value: Dual) -> Dual:
    return (
        -value[0],
        tuple(None if item is None else -item for item in value[1]),
    )  # type: ignore[return-value]


def dadd(left: Dual, right: Dual) -> Dual:
    derivatives: list[arb | None] = []
    for a, b in zip(left[1], right[1], strict=True):
        derivatives.append(None if a is None or b is None else a + b)
    return left[0] + right[0], tuple(derivatives)  # type: ignore[return-value]


def dsub(left: Dual, right: Dual) -> Dual:
    return dadd(left, dneg(right))


def dmul(left: Dual, right: Dual) -> Dual:
    derivatives: list[arb | None] = []
    for a, b in zip(left[1], right[1], strict=True):
        derivatives.append(
            None
            if a is None or b is None
            else a * right[0] + left[0] * b
        )
    return left[0] * right[0], tuple(derivatives)  # type: ignore[return-value]


def dscale(value: Dual, factor: arb) -> Dual:
    return (
        value[0] * factor,
        tuple(
            None if derivative is None else derivative * factor
            for derivative in value[1]
        ),
    )  # type: ignore[return-value]


TARGET_RE = re.compile(r"^([GW])\[(-?[0-9]+),(-?[0-9]+)\]$")


def interval_geometry(chart: str, target_id: str, box: Box) -> dict[str, Dual]:
    target_match = TARGET_RE.fullmatch(target_id)
    need(target_match is not None, "target ID syntax:" + target_id)
    obstacle, ix_text, iy_text = target_match.groups()
    ix, iy = int(ix_text), int(iy_text)

    t: Dual = (
        arb_interval(box.t0, box.t1),
        (arb(1), arb(0), arb(0)),
    )
    p: Dual = (
        arb_interval(box.p0, box.p1),
        (arb(0), arb(1), arb(0)),
    )
    s: Dual = (
        arb_interval(box.s0, box.s1),
        (arb(0), arb(0), arb(1)),
    )
    rt_value = sqrt_one_minus_square(box.t0, box.t1)
    rp_value = sqrt_one_minus_square(box.p0, box.p1)
    rt: Dual = (
        rt_value,
        (-t[0] / rt_value, arb(0), arb(0)),
    )
    rp: Dual = (
        rp_value,
        (
            arb(0),
            None if not bool(rp_value > 0) else -p[0] / rp_value,
            arb(0),
        ),
    )

    need(chart.startswith("G:"), "Source-G chart")
    cell = chart.split(":", 1)[1]
    if cell == "E":
        nx, ny = rt, t
    elif cell == "W":
        nx, ny = dneg(rt), t
    elif cell == "N":
        nx, ny = t, rt
    else:
        need(cell == "S", "known chart cell")
        nx, ny = t, dneg(rt)

    ux = dsub(dmul(rp, nx), dmul(p, ny))
    uy = dadd(dmul(rp, ny), dmul(p, nx))
    source_x = dscale(nx, arb(9) / 25)
    source_y = dscale(ny, arb(9) / 25)
    if obstacle == "G":
        cx = dconstant(arb(ix))
        cy = dconstant(arb(iy))
        radius = arb(9) / 25
    else:
        cx = dadd(dconstant(arb(ix) + arb(1) / 2), s)
        cy = dconstant(arb(iy) + arb(1) / 2)
        radius = arb(4) / 25
    dx = dsub(cx, source_x)
    dy = dsub(cy, source_y)
    transverse = dadd(dneg(dmul(uy, dx)), dmul(ux, dy))
    discriminant = dsub(
        dconstant(radius * radius),
        dmul(transverse, transverse),
    )
    need(bool(discriminant[0] > 0), "strict first-hit discriminant")
    radical_value = discriminant[0].sqrt()
    radical: Dual = (
        radical_value,
        tuple(
            None
            if derivative is None
            else derivative / (2 * radical_value)
            for derivative in discriminant[1]
        ),
    )  # type: ignore[assignment]
    out_x = dscale(
        dadd(dneg(dmul(radical, ux)), dmul(transverse, uy)),
        1 / radius,
    )
    out_y = dscale(
        dsub(dneg(dmul(radical, uy)), dmul(transverse, ux)),
        1 / radius,
    )
    return {
        "source_x": source_x,
        "source_y": source_y,
        "hit_x": dadd(cx, dscale(out_x, radius)),
        "hit_y": dadd(cy, dscale(out_y, radius)),
        "outgoing_equality": dsub(
            dmul(out_x, out_x),
            dmul(out_y, out_y),
        ),
    }


def arb_sign(value: arb) -> str:
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    if bool(value > 0):
        return "STRICT_POSITIVE"
    return "OVERWRAP"


def active_scalar(
    evidence: EndpointEvidence,
    box: Box,
) -> tuple[Dual, Dual | None]:
    origin = evidence.origin
    occurrence = evidence.occurrence
    normal_form = evidence.normal_form
    need(
        origin is not None and occurrence is not None
        and normal_form is not None,
        "active scalar geometry join",
    )
    geometry = interval_geometry(
        origin["chart"],
        origin["owner_target"],
        box,
    )
    if occurrence["kind"] == "OUTGOING":
        return geometry["outgoing_equality"], None
    need(occurrence["kind"] == "WALL", "known collar kind")
    axis = normal_form["axis"]
    need(axis in {"X", "Y"}, "wall axis")
    integer_wall = arb(normal_form["integer_wall"])
    target = geometry["hit_x" if axis == "X" else "hit_y"]
    source = geometry["source_x" if axis == "X" else "source_y"]
    return (
        dsub(target, dconstant(integer_wall)),
        dsub(source, dconstant(integer_wall)),
    )


def find_strict_anchor_subbox(
    evidence: EndpointEvidence,
    issued_inner_box: Box,
    expected_active_sign: str,
) -> tuple[Box, int, int]:
    """Find the first strict rational anchor under an independent BFS replay."""

    need(expected_active_sign in STRICT_SIGNS, "expected active sign")
    queue: deque[tuple[Box, int]] = deque([(issued_inner_box, 0)])
    visited = 0
    while queue:
        candidate, depth = queue.popleft()
        visited += 1
        need(
            visited <= MAX_ANCHOR_SIGN_SEARCH_NODES,
            "anchor sign search node cap",
        )
        active, _source = active_scalar(evidence, candidate)
        observed = arb_sign(active[0])
        if observed == expected_active_sign:
            need(candidate.volume() > 0, "positive strict anchor")
            return candidate, depth, visited
        need(
            observed == "OVERWRAP",
            "anchor active-factor sign contradiction",
        )
        if depth == MAX_ANCHOR_SIGN_SPLIT_DEPTH:
            continue
        widths = (
            candidate.t1 - candidate.t0,
            candidate.p1 - candidate.p0,
            candidate.s1 - candidate.s0,
        )
        axis = max(range(3), key=lambda index: (widths[index], -index))
        queue.extend(
            (child, depth + 1) for child in candidate.split(axis)
        )
    raise VerificationError("strict anchor subbox search cap")


def source_side_contract(
    round_number: int,
    row: dict[str, Any],
) -> dict[str, Any]:
    """Independently normalize one sealed source row to the bridge schema."""

    row_id = row["signed_region_row_id"]
    common = {
        "source_round": round_number,
        "source_signature_row_id": row_id,
        "source_signature_row_sha256": row["row_sha256"],
        "Round182_leaf_row_id": row["Round182_leaf_row_id"],
        "source_chart": row["local_return_signature"]["source_chart"],
        "complete_10_field_return_signature_sha256":
            row["complete_10_field_return_signature_sha256"],
        "occurrence_row_id": row.get("occurrence_row_id"),
        "retained_child_row_id": row.get("retained_child_row_id"),
        "equation": row.get("equation"),
    }
    if round_number in {269, 270}:
        sign = row["region_factor_sign"]
        region_id = row["Round182_leaf_row_id"] + ":" + sign
        need(
            row["direct_whole_leaf_base_certified"] is True
            and row["side_specific_signature_credit"] == 1
            and sign in STRICT_SIGNS
            and row["HPLUS_sign"] in STRICT_SIGNS
            and row["HMINUS_sign"] in STRICT_SIGNS
            and row["candidate_region_id"] == region_id,
            f"Round{round_number} formal connected factor side",
        )
        return {
            **common,
            "active_factor_strict_sign": sign,
            "connected_contract":
                f"ROUND{round_number}_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
            "formal_connected_source_signed_region_id": region_id,
            "formal_connected_source_signed_region_definition":
                "{x in exact pinned Round182 leaf: active_F(x) has "
                + sign + "}",
            "connected_side_extension_materialized": True,
            "relative_open_excluded_face": None,
            "W_tail_connected_extension_missing": False,
        }

    if round_number == 271:
        need(row["side_signature_credit"] == 1, "Round271 side credit")
        if row["collar_kind"] == "OUTGOING":
            sign = row["region_product_sign"]
            child = Box.from_values(row["t_child_box"], row_id)
            need(
                row_id.startswith(W_TAIL_PREFIX)
                and sign in STRICT_SIGNS
                and child.volume() > 0,
                "Round271 W-tail signed child",
            )
            return {
                **common,
                "active_factor_strict_sign": sign,
                "connected_contract":
                    "MISSING__ROUND271_W_TAIL_SIGNED_CHILD_ONLY",
                "formal_connected_source_signed_region_id": None,
                "formal_connected_source_signed_region_definition": None,
                "connected_side_extension_materialized": False,
                "relative_open_excluded_face":
                    row.get("excluded_transition_face"),
                "W_tail_connected_extension_missing": True,
            }
        sign = row["witness_target_factor_sign"]
        need(
            row["collar_kind"] == "WALL"
            and row["connected_side_extension"]
            == "ROUND182_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_GRAPH_SIDE"
            and row["region_product_sign"] in STRICT_SIGNS
            and row["witness_source_factor_sign"] in STRICT_SIGNS
            and sign in STRICT_SIGNS,
            "Round271 formal connected wall side",
        )
        return {
            **common,
            "active_factor_strict_sign": sign,
            "connected_contract":
                "ROUND271_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_"
                "WHOLE_F_SIGN_SIDE",
            "formal_connected_source_signed_region_id":
                row["Round182_leaf_row_id"] + ":TARGET_F:" + sign,
            "formal_connected_source_signed_region_definition":
                "{x in exact pinned Round182 wall leaf: active target_F(x) "
                "has " + sign + "}",
            "connected_side_extension_materialized": True,
            "relative_open_excluded_face": None,
            "W_tail_connected_extension_missing": False,
        }

    need(round_number == 272, "known source round")
    sign = row["witness_target_factor_sign"]
    need(
        row["collar_kind"] == "WALL"
        and row["side_signature_credit"] == 1
        and row["connected_side_extension"]
        == (
            "ONE_SIDED_SOURCE_FACTOR_STRICT_ON_OPEN_INTERIOR__"
            "TARGET_FACTOR_IS_THE_ONLY_ACTIVE_GRAPH"
        )
        and row["exact_source_factor_identity"]
        == (
            "source transverse wall factor = (9/25)*t "
            "with chart-dependent sign"
        )
        and row["excluded_zero_face"] == "t=0"
        and row["closed_leaf_source_factor_sign"] == "OVERWRAP"
        and row["witness_source_factor_sign"] in STRICT_SIGNS
        and sign in STRICT_SIGNS,
        "Round272 relative-open connected boundary side",
    )
    return {
        **common,
        "active_factor_strict_sign": sign,
        "connected_contract":
            "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_"
            "WHOLE_F_SIGN_SIDE",
        "formal_connected_source_signed_region_id":
            row["Round182_leaf_row_id"]
            + ":RELATIVE_OPEN_TARGET_F:" + sign,
        "formal_connected_source_signed_region_definition":
            "{x in relative-open pinned Round182 wall leaf excluding t=0: "
            "active target_F(x) has " + sign + "}",
        "connected_side_extension_materialized": True,
        "relative_open_excluded_face": "t=0",
        "W_tail_connected_extension_missing": False,
    }


def close_output_row(
    id_field: str,
    prefix: str,
    domain: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    need(
        id_field not in payload and "row_sha256" not in payload,
        "fresh Round303A row payload",
    )
    row = {id_field: prefix + digest([domain, payload]), **payload}
    row["row_sha256"] = digest(row)
    return row


def build_bridge_proofs(
    endpoints: dict[str, EndpointEvidence],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    materialized: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    source_reference_histogram: Counter[str] = Counter()
    support_kind_histogram: Counter[str] = Counter()
    connected_contract_histogram: Counter[str] = Counter()
    split_depth_histogram: Counter[str] = Counter()
    unresolved_alias_histogram: Counter[str] = Counter()

    for occurrence_id in sorted(endpoints):
        item = endpoints[occurrence_id]
        registry = item.registry
        disposition = item.disposition
        atom = item.atom
        support = item.support
        source_rows = item.source_rows
        leaf = item.leaf
        occurrence = item.occurrence
        need(
            disposition is not None and atom is not None
            and support is not None and source_rows is not None
            and leaf is not None and occurrence is not None,
            "complete endpoint evidence",
        )
        anchor = Box.from_values(
            registry["positive_volume_rational_inner_support_box"],
            occurrence_id,
        )
        leaf_box = Box.from_values(leaf["box"], leaf["row_id"])
        need(
            anchor.volume() > 0
            and qstr(anchor.volume()) == registry["exact_inner_support_volume"]
            and leaf_box.contains(anchor)
            and registry["outer_envelope_used_as_inner_support"] is False,
            "positive contained non-envelope anchor:" + occurrence_id,
        )
        support_kind_histogram[registry["support_representation_kind"]] += 1

        contracts = [
            source_side_contract(round_number, row)
            for round_number, row in source_rows
        ]
        for contract in contracts:
            source_reference_histogram[str(contract["source_round"])] += 1
        signs = {
            contract["active_factor_strict_sign"] for contract in contracts
        }
        need(len(signs) == 1, "source alias active-sign agreement")
        active_sign = next(iter(signs))
        strict_anchor, split_depth, visited_nodes = (
            find_strict_anchor_subbox(item, anchor, active_sign)
        )
        need(
            anchor.contains(strict_anchor)
            and strict_anchor.volume() > 0,
            "strict B0 contained in issued B",
        )
        split_depth_histogram[str(split_depth)] += 1

        if any(contract["source_round"] == 272 for contract in contracts):
            need(
                (leaf_box.t0 == 0) ^ (leaf_box.t1 == 0)
                and not (anchor.t0 <= 0 <= anchor.t1)
                and not (strict_anchor.t0 <= 0 <= strict_anchor.t1),
                "Round272 relative-open anchor excludes unique t=0 face",
            )

        source_references = [
            {
                "source_round": contract["source_round"],
                "source_signature_row_id":
                    contract["source_signature_row_id"],
                "source_signature_row_sha256":
                    contract["source_signature_row_sha256"],
                "connected_contract": contract["connected_contract"],
                "active_factor_strict_sign":
                    contract["active_factor_strict_sign"],
                "formal_connected_source_signed_region_id":
                    contract["formal_connected_source_signed_region_id"],
                "connected_side_extension_materialized":
                    contract["connected_side_extension_materialized"],
                "relative_open_excluded_face":
                    contract["relative_open_excluded_face"],
            }
            for contract in contracts
        ]
        scope = item.scope
        common = {
            "A0_exact_provenance_pins_and_row_closures": True,
            "A1_Round294_issued_occurrence_has_nonempty_inner_anchor": True,
            "A2_strict_anchor_subbox_inside_issued_inner_support": True,
            "A3_occurrence_atom_source_side_provenance_exactly_closed": True,
            "Round179_active_geometry_reference": {
                "Round179_origin_row_id": item.origin["origin_row_id"],
                "Round179_active_normal_form_row_id":
                    item.normal_form["row_id"],
                "active_collar_kind": occurrence["kind"],
                "active_factor_equation": occurrence["equation"],
                "source_chart": occurrence["chart"],
                "owner_target": occurrence["owner_target"],
                "interval_kernel_filename": R179_KERNEL,
                "interval_kernel_sha256": FILE_PINS[R179_KERNEL],
                "python_flint_version": "0.9.0",
                "interval_precision_bits": PRECISION_BITS,
            },
            "Round182_leaf_reference": {
                "Round182_leaf_row_id": leaf["row_id"],
                "Round182_occurrence_row_id": leaf["occurrence_row_id"],
                "retained_child_row_id": leaf["retained_child_row_id"],
                "exact_leaf_box": leaf["box"],
                "graph_classification": leaf["graph_classification"],
            },
            "Round279_atom_reference": {
                "canonical_atom_id": atom["canonical_atom_id"],
                "row_sha256": atom["row_sha256"],
                "Round182_leaf_row_id": atom["Round182_leaf_row_id"],
                "complete_10_field_return_signature_sha256":
                    atom["complete_10_field_return_signature_sha256"],
                "source_signature_row_ids":
                    atom["source_signature_row_ids"],
                "support_classification": atom["support_classification"],
                "frozen_true_support_boxes":
                    atom["frozen_true_support_boxes"],
            },
            "Round288_disposition_reference": {
                "Round288_atom_disposition_row_id":
                    disposition["Round288_atom_disposition_row_id"],
                "row_sha256": disposition["row_sha256"],
                "occurrence_identity_disposition":
                    disposition["occurrence_identity_disposition"],
                "reserved_candidate_occurrence_id__not_issued":
                    disposition[
                        "reserved_candidate_occurrence_id__not_issued"
                    ],
                "source_proof_classes": disposition["source_proof_classes"],
            },
            "Round294_registry_reference": {
                "Round294_occurrence_registry_row_id":
                    registry["Round294_occurrence_registry_row_id"],
                "row_sha256": registry["row_sha256"],
                "registry_identity_status":
                    registry["registry_identity_status"],
                "registry_promotion_status":
                    registry["registry_promotion_status"],
                "registry_source_identity":
                    registry["registry_source_identity"],
            },
            "Round300D_Round301_scope_reference": {
                "source_Round300D_row_id": scope.source_R300D_row_id,
                "source_Round300D_row_sha256":
                    scope.source_R300D_row_sha256,
                "source_Round301_ineligible_row_id":
                    scope.source_Round301_ineligible_row_id,
                "source_Round301_ineligible_row_sha256":
                    scope.source_Round301_ineligible_row_sha256,
                "opposite_endpoint": scope.peer_occurrence_id,
                "this_Round301_member_row": {
                    "row_id": scope.Round301_member_row_id,
                    "row_sha256": scope.Round301_member_row_sha256,
                    "component_id": scope.Round301_component_id,
                },
            },
            "active_factor_equation": occurrence["equation"],
            "active_factor_strict_sign": active_sign,
            "canonical_atom_id": atom["canonical_atom_id"],
            "exact_issued_inner_support_box": anchor.values(),
            "exact_strict_anchor_subbox": strict_anchor.values(),
            "full_occurrence_support_equality_claimed": False,
            "registry_occurrence_id": occurrence_id,
            "source_side_row_references": source_references,
            "strict_anchor_search": {
                "algorithm":
                    "DETERMINISTIC_BREADTH_FIRST_LONGEST_AXIS_"
                    "RATIONAL_BISECTION",
                "configured_max_split_depth": MAX_ANCHOR_SIGN_SPLIT_DEPTH,
                "configured_max_search_nodes": MAX_ANCHOR_SIGN_SEARCH_NODES,
                "selected_split_depth": split_depth,
                "visited_node_count": visited_nodes,
                "strict_active_factor_sign": active_sign,
                "subbox_contained_in_issued_inner_support": True,
                "subbox_exact_positive_volume":
                    qstr(strict_anchor.volume()),
            },
            "support_representation_kind":
                registry["support_representation_kind"],
            "support_source_reference": support,
            "theorem_id": THEOREM_ID,
            "theorem_sha256": THEOREM_SHA256,
        }

        missing = [
            contract for contract in contracts
            if not contract["connected_side_extension_materialized"]
        ]
        if missing:
            need(
                len(source_rows) in {1, 2}
                and len(missing) == len(source_rows)
                and all(
                    row["signed_region_row_id"].startswith(W_TAIL_PREFIX)
                    for _round, row in source_rows
                ),
                "exact W-tail unresolved source class:" + occurrence_id,
            )
            unresolved_alias_histogram[str(len(source_rows))] += 1
            payload = {
                **common,
                "A4_unique_formal_connected_source_signed_region_materialized":
                    False,
                "disposition": UNRESOLVED_DISPOSITION,
                "eligible_as_R303B_G1_bridge_input": False,
                "formal_occurrence_anchor_connected_side_bridge_credit": 0,
                "missing_obligation":
                    "ROUND271_W_TAIL_ROW_HAS_STRICT_SIGNED_CHILD_BUT_NO_"
                    "FORMAL_CONNECTED_SOURCE_SIDE_EXTENSION",
                "nonedge_or_exclusion_claimed": False,
                **{field: 0 for field in ZERO_FIELDS},
            }
            unresolved.append(close_output_row(
                UNRESOLVED_ID,
                "round303a-unresolved-anchor-bridge:",
                "ROUND303A_W_TAIL_CONNECTED_SIDE_UNRESOLVED_V1",
                payload,
            ))
            continue

        need(
            len(contracts) == 1,
            "unique non-W-tail source row:" + occurrence_id,
        )
        contract = contracts[0]
        connected_contract_histogram[contract["connected_contract"]] += 1
        payload = {
            **common,
            "A4_unique_formal_connected_source_signed_region_materialized":
                True,
            "anchor_bridge_semantics":
                "STRICT_ISSUED_OCCURRENCE_ANCHOR_SUBBOX_B0_IS_"
                "CONTAINED_IN_UNIQUELY_BOUND_FORMAL_CONNECTED_"
                "SOURCE_SIGNED_REGION_A__NO_FULL_SUPPORT_EQUALITY",
            "connected_source_side_witness": {
                "formal_connected_source_signed_region_id":
                    contract["formal_connected_source_signed_region_id"],
                "formal_connected_source_signed_region_definition":
                    contract[
                        "formal_connected_source_signed_region_definition"
                    ],
                "connected_contract": contract["connected_contract"],
                "relative_open_excluded_face":
                    contract["relative_open_excluded_face"],
                "connected": True,
                "strict_anchor_subbox_has_same_active_factor_sign": True,
            },
            "eligible_as_R303B_G1_bridge_input": True,
            "formal_occurrence_anchor_connected_side_bridge_credit": 1,
            **{field: 0 for field in ZERO_FIELDS},
        }
        materialized.append(close_output_row(
            MATERIALIZED_ID,
            "round303a-occurrence-anchor-source-side-bridge:",
            "ROUND303A_OCCURRENCE_ANCHOR_CONNECTED_SIDE_BRIDGE_V1",
            payload,
        ))

    need(
        len(materialized) == 87_824
        and len(unresolved) == 8
        and source_reference_histogram == EXPECTED_SOURCE_REFERENCE_HISTOGRAM
        and support_kind_histogram == EXPECTED_SUPPORT_KIND_HISTOGRAM
        and connected_contract_histogram
        == EXPECTED_CONNECTED_CONTRACT_HISTOGRAM
        and unresolved_alias_histogram == {"1": 4, "2": 4},
        "Round303A proof census",
    )
    return materialized, unresolved, {
        "bridge_count": len(materialized),
        "unresolved_count": len(unresolved),
        "connected_contract_histogram":
            dict(sorted(connected_contract_histogram.items())),
        "support_representation_kind_histogram":
            dict(sorted(support_kind_histogram.items())),
        "source_round_reference_histogram":
            dict(sorted(source_reference_histogram.items())),
        "strict_anchor_split_depth_histogram":
            dict(sorted(split_depth_histogram.items())),
    }


def rows_commitment(
    rows: list[dict[str, Any]],
    id_field: str,
) -> dict[str, Any]:
    rows_hash = ListHash()
    ids_hash = ListHash()
    hashes_hash = ListHash()
    seen: set[str] = set()
    for row in rows:
        validate_output_row(row, id_field)
        row_id = row[id_field]
        need(row_id not in seen, "unique Round303A output row ID")
        seen.add(row_id)
        rows_hash.add(row)
        ids_hash.add(row_id)
        hashes_hash.add(row["row_sha256"])
    return {
        "row_count": len(rows),
        "row_ids_sha256": ids_hash.finish(),
        "row_hashes_sha256": hashes_hash.finish(),
        "rows_sha256": rows_hash.finish(),
    }


COMMON_OUTPUT_KEYS = {
    "A0_exact_provenance_pins_and_row_closures",
    "A1_Round294_issued_occurrence_has_nonempty_inner_anchor",
    "A2_strict_anchor_subbox_inside_issued_inner_support",
    "A3_occurrence_atom_source_side_provenance_exactly_closed",
    "A4_unique_formal_connected_source_signed_region_materialized",
    "Round179_active_geometry_reference",
    "Round182_leaf_reference",
    "Round279_atom_reference",
    "Round288_disposition_reference",
    "Round294_registry_reference",
    "Round300D_Round301_scope_reference",
    "active_factor_equation",
    "active_factor_strict_sign",
    "canonical_atom_id",
    "eligible_as_R303B_G1_bridge_input",
    "exact_issued_inner_support_box",
    "exact_strict_anchor_subbox",
    "formal_occurrence_anchor_connected_side_bridge_credit",
    "full_occurrence_support_equality_claimed",
    "registry_occurrence_id",
    "row_sha256",
    "source_side_row_references",
    "strict_anchor_search",
    "support_representation_kind",
    "support_source_reference",
    "theorem_id",
    "theorem_sha256",
    *ZERO_FIELDS,
}
MATERIALIZED_OUTPUT_KEYS = COMMON_OUTPUT_KEYS | {
    MATERIALIZED_ID,
    "anchor_bridge_semantics",
    "connected_source_side_witness",
}
UNRESOLVED_OUTPUT_KEYS = COMMON_OUTPUT_KEYS | {
    UNRESOLVED_ID,
    "disposition",
    "missing_obligation",
    "nonedge_or_exclusion_claimed",
}
SOURCE_REFERENCE_KEYS = {
    "source_round",
    "source_signature_row_id",
    "source_signature_row_sha256",
    "connected_contract",
    "active_factor_strict_sign",
    "formal_connected_source_signed_region_id",
    "connected_side_extension_materialized",
    "relative_open_excluded_face",
}
CONNECTED_WITNESS_KEYS = {
    "formal_connected_source_signed_region_id",
    "formal_connected_source_signed_region_definition",
    "connected_contract",
    "relative_open_excluded_face",
    "connected",
    "strict_anchor_subbox_has_same_active_factor_sign",
}


def validate_output_row(row: dict[str, Any], id_field: str) -> None:
    expected_keys = (
        MATERIALIZED_OUTPUT_KEYS
        if id_field == MATERIALIZED_ID
        else UNRESOLVED_OUTPUT_KEYS
    )
    need(set(row) == expected_keys, "exact Round303A output row schema")
    verify_closed_row(row, row[id_field])
    payload = dict(row)
    row_hash = payload.pop("row_sha256")
    row_id = payload.pop(id_field)
    prefix, domain = (
        (
            "round303a-occurrence-anchor-source-side-bridge:",
            "ROUND303A_OCCURRENCE_ANCHOR_CONNECTED_SIDE_BRIDGE_V1",
        )
        if id_field == MATERIALIZED_ID
        else (
            "round303a-unresolved-anchor-bridge:",
            "ROUND303A_W_TAIL_CONNECTED_SIDE_UNRESOLVED_V1",
        )
    )
    need(
        row_id == prefix + digest([domain, payload]),
        "Round303A content-derived row ID",
    )
    need(
        row_hash == digest({id_field: row_id, **payload}),
        "Round303A row re-sign closure",
    )
    need(
        all(
            row[f"A{index}_" + suffix] is True
            for index, suffix in (
                (0, "exact_provenance_pins_and_row_closures"),
                (1, "Round294_issued_occurrence_has_nonempty_inner_anchor"),
                (2, "strict_anchor_subbox_inside_issued_inner_support"),
                (3, "occurrence_atom_source_side_provenance_exactly_closed"),
            )
        ),
        "Round303A A0-A3 predicates",
    )
    need(
        row["theorem_id"] == THEOREM_ID
        and row["theorem_sha256"] == THEOREM_SHA256
        and row["full_occurrence_support_equality_claimed"] is False
        and row["active_factor_strict_sign"] in STRICT_SIGNS
        and all(row[field] == 0 for field in ZERO_FIELDS),
        "Round303A theorem/noncredit boundary",
    )
    issued = Box.from_values(
        row["exact_issued_inner_support_box"], "issued output box"
    )
    strict = Box.from_values(
        row["exact_strict_anchor_subbox"], "strict output box"
    )
    need(
        issued.contains(strict)
        and strict.volume() > 0
        and row["strict_anchor_search"][
            "subbox_contained_in_issued_inner_support"
        ] is True
        and row["strict_anchor_search"]["subbox_exact_positive_volume"]
        == qstr(strict.volume()),
        "Round303A serialized anchor containment",
    )
    references = row["source_side_row_references"]
    need(
        type(references) is list and len(references) in {1, 2},
        "Round303A source reference shape",
    )
    need(
        all(
            type(reference) is dict
            and set(reference) == SOURCE_REFERENCE_KEYS
            and reference["source_round"] in {269, 270, 271, 272}
            and reference["active_factor_strict_sign"]
            == row["active_factor_strict_sign"]
            and PIN_RE.fullmatch(
                reference["source_signature_row_sha256"]
            ) is not None
            for reference in references
        ),
        "Round303A exact source reference schema",
    )
    if id_field == MATERIALIZED_ID:
        witness = row["connected_source_side_witness"]
        expected_contracts = {
            269: "ROUND269_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
            270: "ROUND270_DIRECT_WHOLE_LEAF_F_SIGN_SIDE",
            271:
                "ROUND271_SINGLE_ACTIVE_FACTOR_STRICT_T_MONOTONE_"
                "WHOLE_F_SIGN_SIDE",
            272:
                "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_"
                "WHOLE_F_SIGN_SIDE",
        }
        need(
            row[
                "A4_unique_formal_connected_source_signed_region_materialized"
            ] is True
            and row["eligible_as_R303B_G1_bridge_input"] is True
            and row[
                "formal_occurrence_anchor_connected_side_bridge_credit"
            ] == 1
            and row["anchor_bridge_semantics"]
            == (
                "STRICT_ISSUED_OCCURRENCE_ANCHOR_SUBBOX_B0_IS_"
                "CONTAINED_IN_UNIQUELY_BOUND_FORMAL_CONNECTED_"
                "SOURCE_SIGNED_REGION_A__NO_FULL_SUPPORT_EQUALITY"
            )
            and type(witness) is dict
            and set(witness) == CONNECTED_WITNESS_KEYS
            and witness["connected"] is True
            and witness[
                "strict_anchor_subbox_has_same_active_factor_sign"
            ] is True
            and all(
                reference["connected_side_extension_materialized"] is True
                for reference in references
            ),
            "materialized Round303A bridge semantics",
        )
        reference = references[0]
        need(
            len(references) == 1
            and reference["connected_contract"]
            == expected_contracts[reference["source_round"]]
            and isinstance(
                reference["formal_connected_source_signed_region_id"], str
            )
            and bool(
                reference["formal_connected_source_signed_region_id"]
            )
            and isinstance(
                witness[
                    "formal_connected_source_signed_region_definition"
                ],
                str,
            )
            and bool(
                witness[
                    "formal_connected_source_signed_region_definition"
                ]
            )
            and witness["connected_contract"]
            == reference["connected_contract"]
            and witness["formal_connected_source_signed_region_id"]
            == reference["formal_connected_source_signed_region_id"]
            and witness["relative_open_excluded_face"]
            == reference["relative_open_excluded_face"],
            "materialized bridge/source witness identity",
        )
        if reference["source_round"] == 272:
            leaf = Box.from_values(
                row["Round182_leaf_reference"]["exact_leaf_box"],
                "Round272 exact leaf",
            )
            need(
                reference["connected_contract"]
                == (
                    "ROUND272_ONE_SIDED_SOURCE_FACTOR_TARGET_ONLY_ACTIVE_"
                    "WHOLE_F_SIGN_SIDE"
                )
                and reference["relative_open_excluded_face"] == "t=0"
                and (leaf.t0 == 0) ^ (leaf.t1 == 0)
                and not (issued.t0 <= 0 <= issued.t1)
                and not (strict.t0 <= 0 <= strict.t1),
                "Round272 relative-open unique excluded-zero-face semantics",
            )
        else:
            need(
                reference["relative_open_excluded_face"] is None,
                "non-Round272 has no excluded face",
            )
    else:
        need(
            row[
                "A4_unique_formal_connected_source_signed_region_materialized"
            ] is False
            and row["eligible_as_R303B_G1_bridge_input"] is False
            and row[
                "formal_occurrence_anchor_connected_side_bridge_credit"
            ] == 0
            and row["disposition"] == UNRESOLVED_DISPOSITION
            and row["missing_obligation"]
            == (
                "ROUND271_W_TAIL_ROW_HAS_STRICT_SIGNED_CHILD_BUT_NO_"
                "FORMAL_CONNECTED_SOURCE_SIDE_EXTENSION"
            )
            and row["nonedge_or_exclusion_claimed"] is False
            and all(
                reference["connected_side_extension_materialized"] is False
                and reference["formal_connected_source_signed_region_id"]
                is None
                for reference in references
            ),
            "unresolved Round303A W-tail fail-closed semantics",
        )
        need(
            all(
                reference["source_round"] == 271
                and reference["connected_contract"]
                == "MISSING__ROUND271_W_TAIL_SIGNED_CHILD_ONLY"
                for reference in references
            ),
            "unresolved exact Round271 W-tail class",
        )


def ledger_value(
    rows: list[dict[str, Any]],
    table: str,
    schema: str,
    status: str,
    commitment: dict[str, Any],
) -> dict[str, Any]:
    prefix = (
        "materialized_bridge"
        if table == "materialized_bridge_rows"
        else "unresolved_bridge"
    )
    return {
        "every_row_closed_by_own_SHA256": True,
        f"{prefix}_row_count": commitment["row_count"],
        f"{prefix}_row_hashes_sha256":
            commitment["row_hashes_sha256"],
        f"{prefix}_row_ids_sha256": commitment["row_ids_sha256"],
        table: rows,
        f"{prefix}_rows_sha256": commitment["rows_sha256"],
        "schema": schema,
        "status": status,
    }


def deterministic_gzip(payload: bytes) -> bytes:
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=output,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        stream.write(payload)
    return output.getvalue()


def deterministic_ledger_gzip(
    rows: list[dict[str, Any]],
    table: str,
    schema: str,
    status: str,
    commitment: dict[str, Any],
) -> bytes:
    value = ledger_value(rows, table, schema, status, commitment)
    header = dict(value)
    header[table] = None
    output = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        fileobj=output,
        mode="wb",
        mtime=0,
        compresslevel=9,
    ) as stream:
        stream.write(b"{")
        first_key = True
        for key in sorted(header):
            if not first_key:
                stream.write(b",")
            first_key = False
            stream.write(canonical(key) + b":")
            if key != table:
                stream.write(canonical(header[key]))
                continue
            stream.write(b"[")
            for index, row in enumerate(rows):
                if index:
                    stream.write(b",")
                stream.write(canonical(row))
            stream.write(b"]")
        stream.write(b"}")
    return output.getvalue()


def strict_gzip_payload(
    raw: bytes,
    expected_payload: bytes,
    label: str,
) -> dict[str, Any]:
    need(
        len(raw) >= 18
        and raw[:10] == b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff",
        "deterministic gzip header:" + label,
    )
    decoder = zlib.decompressobj(wbits=31)
    plain = decoder.decompress(
        raw, MAX_DECOMPRESSED_CANDIDATE_BYTES + 1
    )
    need(
        len(plain) <= MAX_DECOMPRESSED_CANDIDATE_BYTES
        and decoder.eof
        and not decoder.unused_data
        and not decoder.unconsumed_tail,
        "single-member bounded gzip:" + label,
    )
    plain += decoder.flush()
    need(plain == expected_payload, "exact gzip payload:" + label)
    return strict_json_bytes(
        plain,
        label,
        exact_bytes=expected_payload,
    )


def finalize_result(value: dict[str, Any]) -> bytes:
    result = dict(value)
    result["result_sha256"] = digest(result)
    return canonical(result) + b"\n"


def expected_result(
    statistics: dict[str, Any],
    bridge_commitment: dict[str, Any],
    unresolved_commitment: dict[str, Any],
    bridge_file_sha256: str,
    unresolved_file_sha256: str,
) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status":
            "PASS_ROUND303A_87824_OCCURRENCE_ANCHOR_CONNECTED_SIDE_"
            "BRIDGES__8_W_TAIL_ENDPOINTS_UNRESOLVED__"
            "ZERO_COMPONENT_EDGE_AND_DOWNSTREAM_CREDIT",
        "producer_sha256": PRODUCER_SHA256,
        "seed_affects_output": False,
        "complete_formal_run": True,
        "input_file_pins": dict(sorted(RESULT_INPUT_PINS.items())),
        "theorem": THEOREM,
        "theorem_sha256": THEOREM_SHA256,
        "scope_reconstruction": {
            "complete_Round300D_incidence_edge_count": 111_524,
            "residual_Round301_ineligible_Round300D_pair_count": 110_516,
            "cross_Round301_Round300D_pair_count": 44_108,
            "selected_R288_R288_cross_pair_count": 43_916,
            "selected_distinct_Round294_occurrence_endpoint_count": 87_832,
            "sample_endpoint_count": None,
            "old_63224_component_result_reused": False,
            "Round301_partition_reopened_exactly": True,
        },
        "bridge_census": {
            **statistics,
            "materialized_bridge_row_count":
                bridge_commitment["row_count"],
            "unresolved_bridge_row_count":
                unresolved_commitment["row_count"],
            "full_occurrence_support_equality_claim_count": 0,
            "component_edge_credit_count": 0,
            "W_tail_nonedge_or_exclusion_count": 0,
        },
        "predicate_contract": {
            "all_materialized_rows_A0_through_A4_true": True,
            "all_unresolved_rows_fail_only_A4_connected_extension": True,
            "Round272_relative_open_t0_excluded_face_contract_used": True,
            "Round272_closed_box_source_factor_strictness_required": False,
            "inner_support_is_anchor_not_full_support_definition": True,
        },
        "materialized_bridge_ledger": {
            "filename": MATERIALIZED_LEDGER.name,
            "schema": MATERIALIZED_SCHEMA,
            **bridge_commitment,
            "file_sha256": bridge_file_sha256,
        },
        "unresolved_bridge_ledger": {
            "filename": UNRESOLVED_LEDGER.name,
            "schema": UNRESOLVED_SCHEMA,
            **unresolved_commitment,
            "file_sha256": unresolved_file_sha256,
        },
        "formal_credit_transition": {
            "formal_occurrence_anchor_connected_side_bridge_credit": 87_824,
            **{field: 0 for field in ZERO_FIELDS},
        },
        "strict_nonclaims": {
            "full_occurrence_support_equality_claimed": False,
            "component_connectivity_edge_promoted": False,
            "occurrence_identity_collapsed": False,
            "official_key_identity_merged": False,
            "Round301_DSU_mutated_or_reused": False,
            "maximality_rebuilt": False,
            "fibre_exhaustion_claimed": False,
            "global_disposition_claimed": False,
            "W_tail_unresolved_rows_are_nonedges_or_exclusions": False,
        },
        "atomicity_contract": {
            "both_ledgers_staged_before_any_replacement": True,
            "result_replaced_last_as_atomic_commit_point": True,
            "partial_formal_promotion_permitted": False,
            "any_row_or_numerical_replay_failure_aborts_before_commit": True,
        },
        "required_next": [
            "Seal this producer with an independent cacheless verifier, "
            "targeted re-signed attacks, dual-seed replay, cold replay, "
            "and a manifest.",
            "Only a later Round303-B edge gate may combine a sealed "
            "Round303-A bridge with an independently included connected "
            "graph patch and two closure attachments.",
            "Keep the eight W-tail endpoints unresolved until a dedicated "
            "connected-side extension is proved.",
        ],
    }


def resign_output_row(
    row: dict[str, Any],
    id_field: str,
) -> dict[str, Any]:
    payload = deepcopy(row)
    payload.pop(id_field)
    payload.pop("row_sha256")
    prefix, domain = (
        (
            "round303a-occurrence-anchor-source-side-bridge:",
            "ROUND303A_OCCURRENCE_ANCHOR_CONNECTED_SIDE_BRIDGE_V1",
        )
        if id_field == MATERIALIZED_ID
        else (
            "round303a-unresolved-anchor-bridge:",
            "ROUND303A_W_TAIL_CONNECTED_SIDE_UNRESOLVED_V1",
        )
    )
    return close_output_row(id_field, prefix, domain, payload)


def expect_rejection(label: str, action: Callable[[], Any]) -> str:
    try:
        action()
    except (VerificationError, ValueError, KeyError, zlib.error, OSError):
        return label
    raise VerificationError("attack unexpectedly accepted:" + label)


RESULT_KEYS = {
    "schema",
    "status",
    "producer_sha256",
    "seed_affects_output",
    "complete_formal_run",
    "input_file_pins",
    "theorem",
    "theorem_sha256",
    "scope_reconstruction",
    "bridge_census",
    "predicate_contract",
    "materialized_bridge_ledger",
    "unresolved_bridge_ledger",
    "formal_credit_transition",
    "strict_nonclaims",
    "atomicity_contract",
    "required_next",
    "result_sha256",
}


def validate_result_contract(result: dict[str, Any]) -> None:
    need(set(result) == RESULT_KEYS, "exact formal result top-level schema")
    payload = dict(result)
    claimed = payload.pop("result_sha256")
    need(
        isinstance(claimed, str)
        and PIN_RE.fullmatch(claimed) is not None
        and digest(payload) == claimed,
        "formal result SHA closure",
    )
    need(
        result["schema"] == SCHEMA
        and result["producer_sha256"] == PRODUCER_SHA256
        and result["seed_affects_output"] is False
        and "seed" not in result
        and result["complete_formal_run"] is True
        and result["input_file_pins"]
        == dict(sorted(RESULT_INPUT_PINS.items()))
        and result["theorem"] == THEOREM
        and result["theorem_sha256"] == THEOREM_SHA256,
        "formal result frozen header",
    )
    need(
        result["bridge_census"]["bridge_count"] == 87_824
        and result["bridge_census"]["unresolved_count"] == 8
        and result["bridge_census"][
            "full_occurrence_support_equality_claim_count"
        ] == 0
        and result["bridge_census"]["component_edge_credit_count"] == 0
        and result["formal_credit_transition"][
            "formal_occurrence_anchor_connected_side_bridge_credit"
        ] == 87_824
        and all(
            result["formal_credit_transition"][field] == 0
            for field in ZERO_FIELDS
        ),
        "formal result census/noncredit boundary",
    )
    need(
        result["materialized_bridge_ledger"]["filename"]
        == MATERIALIZED_LEDGER.name
        and result["unresolved_bridge_ledger"]["filename"]
        == UNRESOLVED_LEDGER.name,
        "formal result exact ledger filenames",
    )


def resign_result(result: dict[str, Any]) -> dict[str, Any]:
    output = deepcopy(result)
    output.pop("result_sha256", None)
    output["result_sha256"] = digest(output)
    return output


def run_attack_suite(
    materialized: list[dict[str, Any]],
    unresolved: list[dict[str, Any]],
    formal_result: dict[str, Any],
) -> dict[str, Any]:
    need(materialized and unresolved, "attack representatives")
    accepted: list[str] = []

    def row_attack(
        label: str,
        base: dict[str, Any],
        id_field: str,
        mutate: Callable[[dict[str, Any]], None],
    ) -> None:
        forged = deepcopy(base)
        mutate(forged)
        forged = resign_output_row(forged, id_field)
        accepted.append(expect_rejection(
            label,
            lambda: validate_output_row(forged, id_field),
        ))

    bridge = materialized[0]
    row_attack(
        "resign_bridge_A4_false", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__(
            "A4_unique_formal_connected_source_signed_region_materialized",
            False,
        ),
    )
    row_attack(
        "resign_bridge_credit_zero", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__(
            "formal_occurrence_anchor_connected_side_bridge_credit", 0
        ),
    )
    row_attack(
        "resign_bridge_component_edge_credit", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__("formal_component_edge_credit", 1),
    )
    row_attack(
        "resign_bridge_full_support_equality", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__(
            "full_occurrence_support_equality_claimed", True
        ),
    )
    row_attack(
        "resign_bridge_ineligible", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__(
            "eligible_as_R303B_G1_bridge_input", False
        ),
    )
    row_attack(
        "resign_bridge_disconnected_witness", bridge, MATERIALIZED_ID,
        lambda row: row["connected_source_side_witness"].__setitem__(
            "connected", False
        ),
    )
    row_attack(
        "resign_bridge_source_extension_false", bridge, MATERIALIZED_ID,
        lambda row: row["source_side_row_references"][0].__setitem__(
            "connected_side_extension_materialized", False
        ),
    )
    row_attack(
        "resign_bridge_theorem_hash", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__("theorem_sha256", "0" * 64),
    )
    row_attack(
        "resign_bridge_anchor_not_contained", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__(
            "exact_strict_anchor_subbox",
            ["-2", "2", "-2", "2", "-2", "2"],
        ),
    )
    row_attack(
        "resign_bridge_extra_field", bridge, MATERIALIZED_ID,
        lambda row: row.__setitem__("forged_claim", True),
    )
    round272 = next(
        row for row in materialized
        if row["source_side_row_references"][0]["source_round"] == 272
    )

    def erase_relative_open_semantics(row: dict[str, Any]) -> None:
        row["source_side_row_references"][0][
            "relative_open_excluded_face"
        ] = None
        row["connected_source_side_witness"][
            "relative_open_excluded_face"
        ] = None

    row_attack(
        "resign_Round272_as_generic_closed_box",
        round272,
        MATERIALIZED_ID,
        erase_relative_open_semantics,
    )

    blocked = unresolved[0]
    row_attack(
        "resign_W_tail_A4_true", blocked, UNRESOLVED_ID,
        lambda row: row.__setitem__(
            "A4_unique_formal_connected_source_signed_region_materialized",
            True,
        ),
    )
    row_attack(
        "resign_W_tail_bridge_credit", blocked, UNRESOLVED_ID,
        lambda row: row.__setitem__(
            "formal_occurrence_anchor_connected_side_bridge_credit", 1
        ),
    )
    row_attack(
        "resign_W_tail_eligible", blocked, UNRESOLVED_ID,
        lambda row: row.__setitem__(
            "eligible_as_R303B_G1_bridge_input", True
        ),
    )
    row_attack(
        "resign_W_tail_nonedge", blocked, UNRESOLVED_ID,
        lambda row: row.__setitem__("nonedge_or_exclusion_claimed", True),
    )
    row_attack(
        "resign_W_tail_fake_region", blocked, UNRESOLVED_ID,
        lambda row: row["source_side_row_references"][0].__setitem__(
            "formal_connected_source_signed_region_id", "forged-region"
        ),
    )
    row_attack(
        "resign_W_tail_wrong_disposition", blocked, UNRESOLVED_ID,
        lambda row: row.__setitem__("disposition", "FORMAL_NONEDGE"),
    )

    forged_seed_effect = deepcopy(formal_result)
    forged_seed_effect["seed_affects_output"] = True
    forged_seed_effect = resign_result(forged_seed_effect)
    accepted.append(expect_rejection(
        "resign_result_seed_affects_output_true",
        lambda: validate_result_contract(forged_seed_effect),
    ))
    forged_seed_field = deepcopy(formal_result)
    forged_seed_field["seed"] = "forged-invocation-state"
    forged_seed_field = resign_result(forged_seed_field)
    accepted.append(expect_rejection(
        "resign_result_seed_field_injected",
        lambda: validate_result_contract(forged_seed_field),
    ))

    valid_small = canonical({"x": 1})
    accepted.append(expect_rejection(
        "json_duplicate_key",
        lambda: strict_json_bytes(b'{"x":1,"x":1}', "attack"),
    ))
    accepted.append(expect_rejection(
        "json_float",
        lambda: strict_json_bytes(b'{"x":1.0}', "attack"),
    ))
    accepted.append(expect_rejection(
        "json_nan",
        lambda: strict_json_bytes(b'{"x":NaN}', "attack"),
    ))
    accepted.append(expect_rejection(
        "json_bom",
        lambda: strict_json_bytes(
            b"\xef\xbb\xbf" + valid_small, "attack"
        ),
    ))
    accepted.append(expect_rejection(
        "json_nul",
        lambda: strict_json_bytes(b'{"x":"\\u0000"}', "attack"),
    ))

    valid_gzip = deterministic_gzip(valid_small)
    accepted.append(expect_rejection(
        "gzip_truncated",
        lambda: strict_gzip_payload(
            valid_gzip[:-3], valid_small, "attack"
        ),
    ))
    accepted.append(expect_rejection(
        "gzip_trailing_member",
        lambda: strict_gzip_payload(
            valid_gzip + valid_gzip, valid_small, "attack"
        ),
    ))
    changed_header = bytearray(valid_gzip)
    changed_header[4] = 1
    accepted.append(expect_rejection(
        "gzip_nonzero_mtime",
        lambda: strict_gzip_payload(
            bytes(changed_header), valid_small, "attack"
        ),
    ))
    accepted.append(expect_rejection(
        "gzip_payload_change",
        lambda: strict_gzip_payload(
            deterministic_gzip(canonical({"x": 2})),
            valid_small,
            "attack",
        ),
    ))
    need(len(accepted) == 28, "attack suite census")
    return {
        "schema": ATTACK_SCHEMA,
        "status": "PASS_28_OF_28_TARGETED_ATTACKS_REJECTED",
        "attack_count": len(accepted),
        "rejected_attack_ids": accepted,
        "semantic_resigning_attacks_rejected": 19,
        "strict_json_attacks_rejected": 5,
        "strict_gzip_attacks_rejected": 4,
    }


def compare_candidate_file(
    path: Path,
    expected: bytes,
    cap: int,
    label: str,
) -> bytes:
    safe_regular(path, cap)
    raw = path.read_bytes()
    need(raw == expected, "exact candidate bytes:" + label)
    return raw


def write_atomic(path: Path, payload: bytes) -> None:
    need(path.parent.resolve() == HERE.resolve(), "output HERE confinement")
    temporary = HERE / ("." + path.name + ".tmp")
    need(not temporary.exists(), "clean verifier staging path")
    try:
        with temporary.open("xb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def reconstruct_expected() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    scope = collect_cross_component_new_endpoints()
    endpoints = collect_registry(scope)
    collect_dispositions(endpoints)
    collect_atoms(endpoints)
    collect_support_rows(endpoints)
    collect_source_rows(endpoints)
    collect_geometry_rows(endpoints)
    return build_bridge_proofs(endpoints)


def run(*, no_write: bool) -> dict[str, Any]:
    need(
        digest(THEOREM) == THEOREM_SHA256,
        "frozen theorem SHA",
    )
    need(
        PIN_RE.fullmatch(PRODUCER_SHA256) is not None,
        "frozen producer SHA required",
    )
    need(
        str(FLINT_VERSION) == "0.9.0",
        "python-flint version 0.9.0",
    )
    ctx.prec = PRECISION_BITS
    need(ctx.prec == PRECISION_BITS, "independent Arb precision")
    validate_input_boundary()
    safe_regular(PRODUCER, 4 << 20)
    need(
        file_sha256(PRODUCER) == PRODUCER_SHA256,
        "inert producer byte pin",
    )

    # No candidate file is opened before the complete independent expected
    # state has been reconstructed and byte-serialized.
    materialized, unresolved, statistics = reconstruct_expected()
    bridge_commitment = rows_commitment(
        materialized, MATERIALIZED_ID
    )
    unresolved_commitment = rows_commitment(
        unresolved, UNRESOLVED_ID
    )
    bridge_status = (
        "FORMAL_87824_ROUND294_OCCURRENCE_ANCHORS_BOUND_TO_"
        "CONNECTED_SOURCE_SIGNED_REGIONS__NO_SUPPORT_EQUALITY_"
        "OR_COMPONENT_EDGE_CREDIT"
    )
    unresolved_status = (
        "EIGHT_ROUND271_W_TAIL_ENDPOINTS_UNRESOLVED__"
        "CONNECTED_SOURCE_SIDE_EXTENSION_MISSING__"
        "NOT_NONEDGES_OR_EXCLUSIONS"
    )
    bridge_value = ledger_value(
        materialized,
        "materialized_bridge_rows",
        MATERIALIZED_SCHEMA,
        bridge_status,
        bridge_commitment,
    )
    unresolved_value = ledger_value(
        unresolved,
        "unresolved_bridge_rows",
        UNRESOLVED_SCHEMA,
        unresolved_status,
        unresolved_commitment,
    )
    bridge_plain = canonical(bridge_value)
    unresolved_plain = canonical(unresolved_value)
    bridge_expected = deterministic_ledger_gzip(
        materialized,
        "materialized_bridge_rows",
        MATERIALIZED_SCHEMA,
        bridge_status,
        bridge_commitment,
    )
    unresolved_expected = deterministic_ledger_gzip(
        unresolved,
        "unresolved_bridge_rows",
        UNRESOLVED_SCHEMA,
        unresolved_status,
        unresolved_commitment,
    )
    result_value = expected_result(
        statistics,
        bridge_commitment,
        unresolved_commitment,
        hashlib.sha256(bridge_expected).hexdigest(),
        hashlib.sha256(unresolved_expected).hexdigest(),
    )
    result_expected = finalize_result(result_value)

    bridge_raw = compare_candidate_file(
        MATERIALIZED_LEDGER,
        bridge_expected,
        MAX_DECOMPRESSED_CANDIDATE_BYTES,
        MATERIALIZED_LEDGER.name,
    )
    unresolved_raw = compare_candidate_file(
        UNRESOLVED_LEDGER,
        unresolved_expected,
        64 << 20,
        UNRESOLVED_LEDGER.name,
    )
    result_raw = compare_candidate_file(
        RESULT,
        result_expected,
        8 << 20,
        RESULT.name,
    )
    strict_gzip_payload(
        bridge_raw, bridge_plain, MATERIALIZED_LEDGER.name
    )
    strict_gzip_payload(
        unresolved_raw, unresolved_plain, UNRESOLVED_LEDGER.name
    )
    formal_result = strict_json_bytes(
        result_raw[:-1],
        RESULT.name,
        exact_bytes=result_expected[:-1],
    )
    need(
        result_raw.endswith(b"\n")
        and not result_raw.endswith(b"\n\n"),
        "result single trailing newline",
    )
    validate_result_contract(formal_result)

    attacks = run_attack_suite(
        materialized, unresolved, formal_result
    )
    attacks_bytes = canonical(attacks) + b"\n"
    verification = {
        "schema": VERIFICATION_SCHEMA,
        "status":
            "PASS_INDEPENDENT_CACHELESS_EXACT_RECONSTRUCTION_87824_"
            "BRIDGES_8_W_TAIL_UNRESOLVED",
        "producer_sha256": PRODUCER_SHA256,
        "producer_treatment":
            "INERT_BYTE_PIN_ONLY__NEVER_IMPORTED_EXECUTED_PARSED_OR_TOKENIZED",
        "candidate_artifact_pins": {
            MATERIALIZED_LEDGER.name:
                hashlib.sha256(bridge_raw).hexdigest(),
            UNRESOLVED_LEDGER.name:
                hashlib.sha256(unresolved_raw).hexdigest(),
            RESULT.name: hashlib.sha256(result_raw).hexdigest(),
        },
        "materialized_bridge_row_count": len(materialized),
        "unresolved_bridge_row_count": len(unresolved),
        "theorem_id": THEOREM_ID,
        "theorem_sha256": THEOREM_SHA256,
        "exact_candidate_bytes_verified": True,
        "cacheless_reconstruction": True,
        "candidate_opened_only_after_expected_state_complete": True,
        "strict_json_gzip_path_boundary_verified": True,
        "targeted_attack_suite": {
            "filename": ATTACKS.name,
            "file_sha256": hashlib.sha256(attacks_bytes).hexdigest(),
            "attack_count": attacks["attack_count"],
            "all_rejected": True,
        },
        "formal_component_edge_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_Jx_Jy_same_point_glue_credit": 0,
    }
    verification_bytes = canonical(verification) + b"\n"
    if not no_write:
        write_atomic(ATTACKS, attacks_bytes)
        write_atomic(VERIFICATION, verification_bytes)
    printed = dict(verification)
    printed["verification_file_sha256"] = hashlib.sha256(
        verification_bytes
    ).hexdigest()
    return printed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    arguments = parser.parse_args()
    result = run(no_write=arguments.no_write)
    print(result["status"])
    print("producer_sha256=" + result["producer_sha256"])
    print(
        "verification_file_sha256="
        + result["verification_file_sha256"]
    )


if __name__ == "__main__":
    main()
