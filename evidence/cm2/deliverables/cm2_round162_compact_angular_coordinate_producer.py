#!/usr/bin/env python3
"""Produce the nonpromotional Round162 compact-coordinate certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_round162_compact_angular_coordinate_engine as engine


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round162_compact_angular_coordinate_infrastructure_2026_07_25.json"
)
SCHEMA = "cm2.round162.compact-angular-coordinate-infrastructure.v1"
ENGINE = "cm2_round162_compact_angular_coordinate_engine.py"
ROUND161_CERTIFICATE = (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-2026-07-25.json"
)
ROUND161_VERIFICATION = (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-verification-2026-07-25.json"
)
PINS = {
    ENGINE:
        "f8ec6e2760ff19c6fdd65689ed134cd925b5c382778699e16e0e2f933ae162ed",
    ROUND161_CERTIFICATE:
        "317ee6a43cd6db687f9ac4b089940c436817b4bfec7449ab778b462cff35e0cd",
    ROUND161_VERIFICATION:
        "01da56a79ec34736946c047784de75aa773e61822ffd45fa8a3fe5cc339832db",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError(value)

    def reject_float(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    raw = path.read_bytes()
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "strict JSON encoding",
    )
    result = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject_float,
    )

    def strings(value: Any) -> None:
        if type(value) is str:
            require(
                "\x00" not in value
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in value
                ),
                "decoded string encoding",
            )
        elif type(value) is list:
            for item in value:
                strings(item)
        elif type(value) is dict:
            for key, item in value.items():
                strings(key)
                strings(item)

    strings(result)
    require(type(result) is dict, "top-level object")
    return result


def check_pins() -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        Path(engine.__file__).resolve() == (HERE / ENGINE).resolve(),
        "engine module identity",
    )
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, "pin:" + name)
    engine.check_pins()
    certificate = strict_load(HERE / ROUND161_CERTIFICATE)
    verification = strict_load(HERE / ROUND161_VERIFICATION)
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"]
        == (
            "cm2.round161.dyadic-sheared-recentering-to-"
            "2500000000000000h.v1"
        )
        and certificate["result_sha256"] == digest(certificate["result"])
        and certificate["result_sha256"]
        == "842ef791a414e85b5f2eeb458f876d837d269a284f26ae8317059bd4e0fb2f12",
        "Round161 certificate wrapper",
    )
    require(
        set(verification) == {"schema", "result", "result_sha256"}
        and verification["schema"]
        == (
            "cm2.round161.dyadic-sheared-recentering-to-"
            "2500000000000000h.verification.v1"
        )
        and verification["result_sha256"] == digest(verification["result"])
        and verification["result_sha256"]
        == "5c1a78555644f4fb424e8e164e3088fd24a1d393252a6214d4b8829815571e07"
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == certificate["result_sha256"],
        "Round161 verification wrapper",
    )
    prior = certificate["result"]
    require(
        prior["status"]
        == (
            "CERTIFIED_DYADIC_SHEARED_RECENTERING_TO_"
            "2500000000000000H__D02_STILL_BLOCKED"
        )
        and prior["certified_abs_delta_x_corridor_in_h_units"]
        == ["0", "2500000000000000"]
        and prior["combined_typed_atlas"]
        == {
            "connected": True,
            "interior_untyped_event_cell_count": 0,
            "lower_symmetry_axis_terminal": True,
            "slab_count": 75,
            "typed_box_count": 225,
            "upper_endpoint_in_h_units": "2500000000000000",
            "upper_endpoint_terminal": False,
        }
        and prior["strict_nonpromotion"]
        == {
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "Round161 strict state",
    )
    terminal_macro = prior["new_dyadic_sheared_recentering"][
        "new_macro_slabs"
    ][-1]
    require(
        terminal_macro["u_in_h_units"]
        == ["100000", "2500000000000000"]
        and terminal_macro["coordinate_map"]
        == {
            "coordinate_system": "SHEARED_COMPACT_ANGLE_LIFT",
            "slope_s": "1403486916994043/500000000000000",
            "u_definition": "u=abs(delta_x)/h=-delta_x/h",
            "w_definition": "w=delta_beta/h-s*u",
        }
        and terminal_macro["w_typed_box_chain"]
        == [
            {
                "kind": "C24_EVENT",
                "w_in_h_units": ["-430", "-405"],
            },
            {
                "kind": "STRICT_RETURN_BRIDGE",
                "w_in_h_units": ["-405", "-350"],
            },
            {
                "kind": "D3_EVENT",
                "w_in_h_units": ["-350", "134111000000"],
            },
        ],
        "Round161 endpoint typed faces",
    )
    return certificate, verification


def build() -> dict[str, Any]:
    certificate, verification = check_pins()
    infrastructure = engine.build_infrastructure()
    strict = infrastructure["strict_scope"]
    require(
        strict["D02_status"] == "BLOCKED"
        and strict["D03_authorized"] is False
        and strict["CM2"] == "NO-GO_FOR_CLAIM"
        and infrastructure["round161_endpoint_compact_lift"][
            "this_is_a_coordinate_lift_not_a_new_continuation_slab"
        ],
        "nonpromotion invariant",
    )
    result = {
        "status": infrastructure["status"],
        "inheritance": {
            "round161_certificate": ROUND161_CERTIFICATE,
            "round161_certificate_file_sha256": PINS[ROUND161_CERTIFICATE],
            "round161_certificate_result_sha256":
                certificate["result_sha256"],
            "round161_verification": ROUND161_VERIFICATION,
            "round161_verification_file_sha256": PINS[ROUND161_VERIFICATION],
            "round161_verification_result_sha256":
                verification["result_sha256"],
            "round161_verification_status": "PASS",
            "inherited_certified_abs_delta_x_corridor_in_h_units":
                ["0", "2500000000000000"],
            "inherited_combined_typed_atlas":
                certificate["result"]["combined_typed_atlas"],
        },
        "engine_source": {
            "file": ENGINE,
            "sha256": PINS[ENGINE],
        },
        "compact_angular_coordinate_infrastructure": infrastructure,
        "strict_nonpromotion": {
            "certified_abs_delta_x_corridor_extended": False,
            "combined_typed_atlas_changed": False,
            "D02_status": "BLOCKED",
            "D03_authorized": False,
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": infrastructure["next_core_gate"],
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = build()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    arguments.output.write_text(
        canonical(document) + "\n",
        encoding="utf-8",
    )
    print(canonical(document))


if __name__ == "__main__":
    main()
