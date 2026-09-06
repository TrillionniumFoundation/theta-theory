#!/usr/bin/env python3
"""Independent exact-rational A1 v12 review diagnostics.

Run from the repository (no network and no source-file mutations):
  python3 reviews/a1-english-v12-certified-memory-2026-09-06/reproduce_review.py
Use --source-root PATH for a separate, byte-verified source copy.
The expected outcomes include accepted deliberately faulty compiler results.
These are certification-interface counterexamples, not counterexamples to the
printed mathematical theorems with their rounding and horizon hypotheses.
"""
from __future__ import annotations
import argparse
from dataclasses import replace
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import sys

SUBMISSION = '71907d83ba4eb235949e2a929b4b7f85349e96e5'
BLOBS = {
    'finite_compiler.py': '286c956da1e8b4845d8457488e56845cf15c352b',
    'certified_compiler.py': '205bf39543f81eab85eb22425572206c810f598e',
    'construction_contracts.py': 'ec778394962114c3ad9a0e6bef0fb7796c65c266',
}


def identities(root: Path) -> dict:
    result = {}
    for name, expected in BLOBS.items():
        data = (root / name).read_bytes()
        git_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if git_blob != expected:
            raise RuntimeError(f'Pinned source mismatch: {name}: {git_blob}')
        result[name] = {'git_blob': git_blob, 'sha256': hashlib.sha256(data).hexdigest(),
                        'bytes': len(data)}
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path,
                        default=Path(__file__).resolve().parents[2] / 'papers/A1-english-v12')
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('EXECUTION.json'))
    args = parser.parse_args()
    before = identities(args.source_root)
    sys.path.insert(0, str(args.source_root.resolve()))
    import certified_compiler as cc
    import finite_compiler as fc
    from construction_contracts import inspect_construction, ContractError
    original = cc.compile_tables
    rows = []

    def interval_factory(b, h, tau=None):
        # U=[1/4,3/4]; this grid's command covering radius is at most h.
        segments = max(1, 1 << max(0, b - 2))
        grid = tuple(F(1, 4) + F(j, 2 * segments) for j in range(segments + 1))
        def state(hist):
            s = F(1, 2)
            for u, _ in hist:
                s = (s + grid[u]) / 2
            return (s,)
        return len(grid), state, state, grid

    def force_zero_bits(*a, **kw):
        a = list(a)
        a[4] = 0  # Only the returned compiler precision is changed.
        return original(*a, **kw)

    try:
        for routine in ('adaptive', 'robust'):
            for M in (1, 2):
                for fault in ('none', 'zero_output_bits'):
                    cc.compile_tables = original if fault == 'none' else force_zero_bits
                    if routine == 'adaptive':
                        p, audit, trace, grid = cc.adaptive_compile(
                            1, 1, M, F(1, 2), interval_factory,
                            absolute_tolerance=F(1, 128), max_bits=12)
                    else:
                        p, audit, trace, grid = cc.robust_adaptive_compile(
                            1, 1, M, F(1, 2), interval_factory,
                            F(1, 128), max_bits=12)
                    last = trace[-1]
                    count, state, predict, _ = interval_factory(last['b'], last['h'])
                    certificate = inspect_construction(p, audit, count, 1, M, state, predict)
                    e = F(1, 8 * M)  # Exact continuum radius; elementary interval proof.
                    valid = all(t['lower'] <= e <= t['upper'] for t in trace)
                    errors = []
                    for u in range(len(grid)):
                        machine = fc.Machine()
                        machine.step(p, 0, u, 0)
                        errors.append(abs(machine.output(p, 1, 0) - state(((u, 0),))[0]))
                    assert certificate.accepted
                    assert valid == (fault == 'none')
                    assert (p.output_bits == last['b'] + 2) == (fault == 'none')
                    rows.append({'routine': routine, 'M': M, 'fault': fault,
                                 'true_continuum_radius': e, 'returned_bits': p.output_bits,
                                 'requested_bits': last['b'] + 2,
                                 'accepted': certificate.accepted,
                                 'all_returned_brackets_valid': valid,
                                 'maximum_grid_query_error': max(errors),
                                 'first_invalid_bracket': next((t for t in trace
                                     if not t['lower'] <= e <= t['upper']), None),
                                 'last_stage': last})
        cc.compile_tables = original
        # Positive control: the old transition-collapse fault is rejected.
        count, state, predict, _ = interval_factory(6, F(1, 64))
        p, audit = original(1, count, 1, 2, 8, state, predict)
        collapsed = replace(p, transitions=tuple(
            tuple(tuple(tuple(0 for _ in reports) for reports in commands)
                  for commands in stage) for stage in p.transitions))
        rejected = not inspect_construction(collapsed, audit, count, 1, 2, state, predict).accepted
        assert rejected

        # A separate dimension-contract counterexample: a two-stage request
        # receives a self-consistent one-stage program and audit.
        def finite_factory(b, h, tau=None):
            grid = (F(1,4), F(1,2), F(3,4))
            def state(hist):
                s = F(1,2)
                for u, _ in hist:
                    s = (s+grid[u])/2
                return (s,)
            return len(grid), state, state, grid
        def shorten_horizon(*a, **kw):
            a = list(a)
            a[0] = 1
            return original(*a, **kw)
        horizon_rows = []
        for routine in ('adaptive', 'robust'):
            cc.compile_tables = shorten_horizon
            if routine == 'adaptive':
                p, audit, trace, _ = cc.adaptive_compile(2, 1, 2, F(0), finite_factory, max_bits=12)
            else:
                p, audit, trace, _ = cc.robust_adaptive_compile(
                    2, 1, 2, F(0), finite_factory, F(1,128), max_bits=12)
            assert len(p.transitions) == 1 and all(t['construction_accepted'] for t in trace)
            machine = fc.Machine()
            machine.step(p, 0, 0, 0)
            try:
                machine.step(p, 1, 0, 0)
            except IndexError:
                runtime = 'IndexError on required second transition'
            else:
                raise AssertionError('shortened program unexpectedly executed two stages')
            horizon_rows.append({'routine': routine, 'requested_horizon': 2,
                                 'returned_horizon': len(p.transitions),
                                 'all_construction_gates_accepted': True, 'runtime': runtime,
                                 'last_stage': trace[-1]})
    finally:
        cc.compile_tables = original

    # Positive exact checks for the new rank-two lower-bound calculation.
    advice = []
    for delta in (F(1,128), F(1,256), F(1,1024)):
        eps = 6*delta
        def moment(k, sign):
            return F(1,k+1)+sign*eps*F(k,(k+1)*(k+2))
        assert all(abs(moment(k,sgn)-F(1,k+1)) <= delta
                   for k in range(33) for sgn in (-1,1))
        gap = (moment(1,1)-moment(1,-1))/32
        assert gap == delta/16 and (gap/2)**2 == delta**2/1024
        advice.append({'delta':delta,'query_gap':gap,'conditional_two_point_floor':(gap/2)**2})
    after = identities(args.source_root)
    assert before == after
    result = {
        'reviewed_commit':SUBMISSION, 'python':platform.python_version(),
        'source_identity':before, 'source_files_unchanged':True,
        'scope':'Executed independent exact-rational review diagnostics on three blob-verified modules; not the complete author suite, TeX build, or a formal proof check.',
        'nominal_runs':4, 'coarse_precision_mutations_accepted_with_false_brackets':4,
        'horizon_truncation_mutations_accepted':2,
        'old_transition_collapse_rejected':rejected,
        'precision_experiments':rows, 'horizon_experiments':horizon_rows,
        'positive_advice_floor_checks':advice,
        'status':'All expected diagnostic outcomes reproduced.'}
    args.output.write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ('precision_experiments','source_identity')},indent=2,default=str))


if __name__ == '__main__':
    main()
