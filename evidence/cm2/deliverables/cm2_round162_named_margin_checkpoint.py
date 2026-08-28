#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_round162_named_margin_checkpoint_engine as engine


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round162-named-margin-checkpoint-2026-07-25.json"
SCHEMA = "cm2.round162.named-margin-checkpoint.v1"
PRIOR_CERTIFICATE = (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-2026-07-25.json"
)
PRIOR_VERIFICATION = (
    "cm2-round161-dyadic-sheared-recentering-to-"
    "2500000000000000h-verification-2026-07-25.json"
)
PINS = {
    PRIOR_CERTIFICATE:
        "317ee6a43cd6db687f9ac4b089940c436817b4bfec7449ab778b462cff35e0cd",
    PRIOR_VERIFICATION:
        "01da56a79ec34736946c047784de75aa773e61822ffd45fa8a3fe5cc339832db",
}
PRIOR_CERTIFICATE_RESULT_SHA256 = (
    "842ef791a414e85b5f2eeb458f876d837d269a284f26ae8317059bd4e0fb2f12"
)
PRIOR_VERIFICATION_RESULT_SHA256 = (
    "5c1a78555644f4fb424e8e164e3088fd24a1d393252a6214d4b8829815571e07"
)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    value = json.loads(
        path.read_bytes().decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )
    require(type(value) is dict, "top object")
    return value


def check_prior() -> tuple[dict[str, Any], dict[str, Any]]:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    prior = strict_load(HERE / PRIOR_CERTIFICATE)
    verification = strict_load(HERE / PRIOR_VERIFICATION)
    require(
        set(prior) == {"schema", "result", "result_sha256"}
        and prior["schema"]
        == (
            "cm2.round161.dyadic-sheared-recentering-to-"
            "2500000000000000h.v1"
        )
        and prior["result_sha256"]
        == PRIOR_CERTIFICATE_RESULT_SHA256
        == digest(prior["result"])
        and prior["result"]["status"]
        == (
            "CERTIFIED_DYADIC_SHEARED_RECENTERING_TO_"
            "2500000000000000H__D02_STILL_BLOCKED"
        ),
        "prior certificate",
    )
    require(
        set(verification) == {"schema", "result", "result_sha256"}
        and verification["schema"]
        == (
            "cm2.round161.dyadic-sheared-recentering-to-"
            "2500000000000000h.verification.v1"
        )
        and verification["result_sha256"]
        == PRIOR_VERIFICATION_RESULT_SHA256
        == digest(verification["result"])
        and verification["result"]["status"] == "PASS"
        and verification["result"]["certificate_result_sha256"]
        == prior["result_sha256"],
        "prior verification",
    )
    return prior, verification


def build() -> dict[str, Any]:
    engine.check_pins()
    prior, verification = check_prior()
    checkpoint = engine.build_checkpoint()
    result = {
        **checkpoint,
        "inherited_round161_result_sha256": prior["result_sha256"],
        "inherited_round161_verification_result_sha256":
            verification["result_sha256"],
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    document = build()
    arguments.output.write_text(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
