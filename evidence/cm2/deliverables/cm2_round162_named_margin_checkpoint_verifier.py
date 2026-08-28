#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import cm2_round162_named_margin_checkpoint_engine as engine


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2-round162-named-margin-checkpoint-2026-07-25.json"
OUTPUT = (
    HERE
    / "cm2-round162-named-margin-checkpoint-verification-2026-07-25.json"
)
CERTIFICATE_SCHEMA = "cm2.round162.named-margin-checkpoint.v1"
SCHEMA = "cm2.round162.named-margin-checkpoint.verification.v1"
ENGINE = "cm2_round162_named_margin_checkpoint_engine.py"
PRODUCER = "cm2_round162_named_margin_checkpoint.py"
PINS = {
    ENGINE: "4fa2c5c6c01acdaa807a2fb4499f9816a1fcd0094520d408c0d9c8bdf19190a9",
    PRODUCER: "e939b35584251ba512daf91ef98fe4d666efe7766950e416fee80eae69d3fd98",
}
PRIOR_RESULT_SHA256 = (
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


def strict_load_raw(raw: bytes) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "raw encoding",
    )
    value = json.loads(
        raw.decode(),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string encoding",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, "top object")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes())


def check_pins() -> None:
    require(
        Path(engine.__file__).resolve() == (HERE / ENGINE).resolve(),
        "engine module identity",
    )
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    engine.check_pins()


def expected_result() -> dict[str, Any]:
    return {
        **engine.build_checkpoint(),
        "inherited_round161_result_sha256": PRIOR_RESULT_SHA256,
        "inherited_round161_verification_result_sha256":
            PRIOR_VERIFICATION_RESULT_SHA256,
    }


def validate(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        type(document) is dict
        and set(document) == {"schema", "result", "result_sha256"}
        and document["schema"] == CERTIFICATE_SCHEMA
        and type(document["result"]) is dict
        and type(document["result_sha256"]) is str
        and document["result_sha256"] == digest(document["result"])
        and canonical(document["result"]) == canonical(expected),
        "certificate exact reconstruction",
    )


def semantic_attacks(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> dict[str, Any]:
    margin_name = "round161_collision3_anchor_correlated_miss"
    require(
        margin_name
        in document["result"]["unrelated_non_event_named_margins"],
        "attack margin",
    )
    mutations: list[tuple[str, Any]] = []

    def add(label: str, function: Any) -> None:
        candidate = copy.deepcopy(document)
        function(candidate)
        candidate["result_sha256"] = digest(candidate["result"])
        mutations.append((label, candidate))

    add(
        "status",
        lambda d: d["result"].__setitem__("status", "PASS"),
    )
    add(
        "u upper",
        lambda d: d["result"]["checkpoint"]["specification"].__setitem__(
            "u_upper_h", "2500000000000002"
        ),
    )
    add(
        "event role",
        lambda d: d["result"]["intentional_typed_event_graph_zeros"][0]
        .__setitem__("role", "UNRELATED_NON_EVENT_STRICT_MARGIN"),
    )
    add(
        "margin family",
        lambda d: d["result"]["unrelated_non_event_named_margins"][
            margin_name
        ].__setitem__("family", "TERMINAL"),
    )
    add(
        "margin interval",
        lambda d: d["result"]["unrelated_non_event_named_margins"][
            margin_name
        ]["minimum_observed_interval_exact_rational"].__setitem__(0, "0"),
    )
    add(
        "margin count",
        lambda d: d["result"]["unrelated_non_event_named_margins"][
            margin_name
        ].__setitem__("observation_count", 0),
    )
    add(
        "margin witness",
        lambda d: d["result"]["unrelated_non_event_named_margins"][
            margin_name
        ].__setitem__("minimum_observed_witness", None),
    )
    add(
        "derivative status",
        lambda d: d["result"]["unrelated_non_event_named_margins"][
            margin_name
        ].__setitem__(
            "parameter_derivative_status",
            "EXPORTED_VALIDATED_OUTERS",
        ),
    )
    add(
        "weakest depth",
        lambda d: d["result"].__setitem__(
            "weakest_unrelated_non_event_margin_depth", 0
        ),
    )
    add(
        "family census",
        lambda d: d["result"]["named_margin_family_census"].__setitem__(
            "all_unrelated_non_event_margins_strict", False
        ),
    )
    add(
        "nonclaim removal",
        lambda d: d["result"]["strict_nonclaims"].pop(),
    )
    add(
        "D02 promotion",
        lambda d: d["result"]["strict_nonpromotion"].__setitem__(
            "D02_status", "READY"
        ),
    )
    add(
        "prior digest",
        lambda d: d["result"].__setitem__(
            "inherited_round161_result_sha256", "0" * 64
        ),
    )
    add(
        "extra field",
        lambda d: d["result"].__setitem__("extra", True),
    )
    rejected = 0
    for label, candidate in mutations:
        try:
            validate(candidate, expected)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError(f"semantic attack accepted:{label}")
    return {
        "attack_count": len(mutations),
        "rejected_count": rejected,
        "all_rejected": rejected == len(mutations),
    }


def strict_json_attacks() -> dict[str, Any]:
    attacks = [
        b'{"schema":"x","schema":"y"}',
        b'{"x":1.0}',
        b'{"x":NaN}',
        b'\xef\xbb\xbf{"x":1}',
        b'{"x":"\\u0000"}',
        b'{"x":"\\ud800"}',
        b'{"x":1}\x00',
    ]
    rejected = 0
    for raw in attacks:
        try:
            strict_load_raw(raw)
        except Exception:
            rejected += 1
        else:
            raise RuntimeError("strict JSON attack accepted")
    return {
        "attack_count": len(attacks),
        "rejected_count": rejected,
        "all_rejected": rejected == len(attacks),
    }


def build() -> dict[str, Any]:
    check_pins()
    document = strict_load(CERTIFICATE)
    expected = expected_result()
    validate(document, expected)
    semantic = semantic_attacks(document, expected)
    strict_attacks = strict_json_attacks()
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": document["result_sha256"],
        "independent_full_R1648_recomputation": True,
        "independent_named_margin_exact_interval_recomputation": True,
        "intentional_event_zero_separation_recomputed": True,
        "parameter_derivative_coverage_statement_recomputed": True,
        "semantic_attack_suite": semantic,
        "strict_json_attack_suite": strict_attacks,
        "strict_nonpromotion_recomputed": True,
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
