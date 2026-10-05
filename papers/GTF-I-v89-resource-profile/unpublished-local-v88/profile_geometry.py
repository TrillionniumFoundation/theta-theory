#!/usr/bin/env python3
"""Exact allocation bookkeeping for the proved local profile law.

This routine computes integer resource invariants, not an operational distance,
channel classification, recovery circuit, or the theorem's local scale interval.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA = 'gtf88.allocation/1'
MAX_INPUT_BYTES = 4_000_000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical_fraction(value: Any) -> Fraction:
    require(type(value) is str, 'a rational must be a canonical string')
    try:
        x = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    require(str(x) == value, 'noncanonical rational')
    return x


def integer(value: Any, name: str) -> int:
    require(type(value) is int and value > 0, name + ' must be a positive integer')
    return value


def allocation(parts: Any, max_groups: int = 100_000) -> tuple[int, ...]:
    integer(max_groups, 'max_groups')
    require(type(parts) is list and len(parts) > 0, 'allocation must be a nonempty list')
    require(len(parts) <= max_groups, 'complete allocation exceeds group cap')
    return tuple(integer(n, 'group size') for n in parts)


def maximum_profile(calls: int, width: int) -> tuple[list[int], int]:
    integer(calls, 'calls'); integer(width, 'width')
    require(width <= calls, 'width exceeds calls')
    q, r = divmod(calls, width)
    # A run-length representation avoids O(calls) memory for a large binary integer.
    return [q, width, r], q * width * width + r * r


def make_certificate(payload: dict[str, Any], max_groups: int = 100_000) -> dict[str, Any]:
    require(type(payload) is dict and set(payload) <= {'allocation', 'phase_per_call'},
            'unsupported input fields')
    require('allocation' in payload, 'missing allocation')
    parts = allocation(payload['allocation'], max_groups)
    n, v, b = sum(parts), sum(x*x for x in parts), max(parts)
    packed, vmax = maximum_profile(n, b)
    out: dict[str, Any] = {
        'schema': SCHEMA, 'status': 'success',
        'input_sha256': hashlib.sha256(json.dumps(payload, sort_keys=True,
                                                   separators=(',', ':')).encode()).hexdigest(),
        'allocation': list(parts), 'groups': len(parts), 'calls': n,
        'second_moment': v, 'largest_group': b, 'effective_width': str(Fraction(v, n)),
        'maximum_second_moment_at_same_budget': vmax,
        'maximizer_run_length': {'full_groups': packed[0], 'full_size': packed[1],
                                 'residual_size': packed[2]},
        'local_rate_formulas': {'regular': 'min(1,s*sqrt(calls))',
                                'coherent': 'min(1,s*sqrt(second_moment))',
                                'opening': 'min(1,s*calls)'},
        'resource_model': 'independent complete probe-reference groups; no input feedback',
        'exact_distance_computed': False, 'measurement_or_tangent_classified': False,
        'discrimination_interval_computed': False, 'recovery_synthesized': False,
        'physical_protocol_executed': False, 'continuum_proof_by_replay': False,
        'firstness_or_priority_certified': False}
    if 'phase_per_call' in payload:
        z = canonical_fraction(payload['phase_per_call'])
        require(0 < z <= Fraction(1, 4), 'phase_per_call must be in (0,1/4]')
        threshold = int(1/(2*z))
        used = [min(p, threshold) for p in parts]
        x = [z*m for m in used]
        require(threshold >= 2 and all(0 < a <= Fraction(1, 2) for a in x),
                'internal clipping invariant failed')
        out['public_clipping'] = {'phase_per_call': str(z), 'integer_cap': threshold,
                                  'used_allocation': used, 'used_calls': sum(used),
                                  'used_second_moment': sum(m*m for m in used),
                                  'signal_scales': [str(a) for a in x],
                                  'quadratic_error_condition_checked': False}
    return out


def verify(payload: dict[str, Any], certificate: Any, max_groups: int = 100_000) -> dict[str, Any]:
    expected = make_certificate(payload, max_groups)
    # Typed JSON comparison prevents bool/int substitution from passing equality.
    require(json.dumps(certificate, sort_keys=True, separators=(',', ':')) ==
            json.dumps(expected, sort_keys=True, separators=(',', ':')),
            'certificate differs from complete exact reconstruction')
    return expected


def load_json(path: Path) -> Any:
    raw = path.read_bytes()
    require(len(raw) <= MAX_INPUT_BYTES, 'input file exceeds byte cap')
    def distinct(pairs):
        out = {}
        for k, v in pairs:
            require(k not in out, 'duplicate JSON key')
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=distinct)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path); p.add_argument('--verify', type=Path)
    p.add_argument('--max-groups', type=int, default=100_000)
    a = p.parse_args()
    try:
        payload = load_json(a.input)
        result = verify(payload, load_json(a.verify), a.max_groups) if a.verify else make_certificate(payload, a.max_groups)
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        p.exit(2, 'allocation certificate rejected: '+str(exc)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
