#!/usr/bin/env python3
"""Reproduce the A1-v11 referee diagnostics without changing author sources.

Run from the repository root:
  python3 reviews/a1-english-v11-certified-memory-2026-09-06/reproduce_review.py
The three imported author files must match the reviewed submission exactly.
Receipts are written under --out, never over the manuscript's validation files.
This is finite diagnostic work, not an automated proof or journal assessment.
"""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import importlib.util
import json
import platform
import sys
from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path

SUBMISSION = 'f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0'
EXPECTED = {
    'finite_compiler.py': '5e6335160cec538c13f7b0fbfb3d6ad89ec55946734ee7d527dae564ac654fda',
    'certified_compiler.py': '6965862f93bd2ef8f107eca30fd53fb3c8ce52e696f99c893a343aad980a226c',
    'tests/test_v11.py': '4cfe2c0a6a492cdff3ca87053ce2de541c6ce90fe97f51fa3238122a6019b2b6',
}


def load_tests(source: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, source / 'tests/test_v11.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load the pinned author suite')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def suite_run(source: Path, out: Path, mutate: bool, fc, cc) -> dict:
    name = 'ZERO_TRANSITION_MUTATION' if mutate else 'AUTHOR_V11_RERUN'
    tests = load_tests(source, 'referee_' + name.lower())
    original = fc.compile_tables
    old_cc = cc.compile_tables
    counters = {'programs': 0, 'changed_entries': 0, 'total_entries': 0}

    def instrumented(*args, **kwargs):
        program, audit = original(*args, **kwargs)
        counters['programs'] += 1
        for stage in program.transitions:
            for row in stage:
                for reports in row:
                    for target in reports:
                        counters['total_entries'] += 1
                        counters['changed_entries'] += int(mutate and target != 0)
        if mutate:
            transitions = tuple(tuple(tuple(tuple(0 for _ in reports)
                               for reports in row) for row in stage)
                               for stage in program.transitions)
            program = replace(program, transitions=transitions)
        return program, audit

    tests.compile_tables = instrumented
    cc.compile_tables = instrumented
    old_argv = sys.argv[:]
    sys.argv = [name, str(out / (name + '.json'))]
    try:
        with (out / (name + '.stdout')).open('w', encoding='utf-8') as stream:
            with contextlib.redirect_stdout(stream):
                tests.main()
    finally:
        sys.argv = old_argv
        cc.compile_tables = old_cc
    receipt = json.loads((out / (name + '.json')).read_text())
    return {'suite_passed': receipt['status'] == 'passed',
            'assertions': receipt['assertions'], **counters,
            'categories': receipt['categories'],
            'max_physical_query_bound': receipt['measurements']['max_physical_query_bound'],
            'max_physical_actual_query_error': receipt['measurements']['max_physical_actual_query_error']}


def interval_witness(fc) -> list[dict]:
    """Exact one-step compact system; its continuum radius is 1/(8M).

    U=[1/4,3/4], s0=1/2, T(s,u)=(s+u)/2, Q(s)=s.
    S1=[3/8,5/8]. The h-net has 8M segments and h=1/(32M).
    Equal-length interval covering gives e=1/(8M), independently of code.
    Collapsing transitions to the first representative fixes output at 3/8.
    """
    rows = []
    for M in (1, 2, 4, 8, 16, 32):
        segments = 8 * M
        grid = tuple(F(1, 4) + F(j, 2 * segments) for j in range(segments + 1))
        bits = (32 * M).bit_length()

        def evaluate(history):
            state = F(1, 2)
            for u, _ in history:
                state = (state + grid[u]) / 2
            return (state,)

        p, audit = fc.compile_tables(1, len(grid), 1, M, bits, evaluate, evaluate)
        collapsed = replace(p, transitions=tuple(tuple(tuple((0,) for _ in row)
                                   for row in stage) for stage in p.transitions))
        raw_error = collapsed_error = F(0)
        wrong_targets = 0
        for u in range(len(grid)):
            target = evaluate(((u, 0),))
            centers = [fc.dyadic(evaluate(hist), bits) for hist in audit.representatives[1]]
            approximate_target = fc.dyadic(target, bits)
            ideal = min(range(len(centers)), key=lambda j: (fc.distance(approximate_target, centers[j]), j))
            assert p.transitions[0][0][u][0] == ideal
            wrong_targets += int(collapsed.transitions[0][0][u][0] != ideal)
            for program, original_flag in ((p, True), (collapsed, False)):
                machine = fc.Machine()
                machine.step(program, 0, u, 0)
                error = abs(machine.output(program, 1, 0) - target[0])
                if original_flag:
                    raw_error = max(raw_error, error)
                else:
                    collapsed_error = max(collapsed_error, error)
        e = F(1, 8 * M)
        assert collapsed_error == F(1, 4)
        assert raw_error <= 2 * e
        assert wrong_targets > 0 if M > 1 else wrong_targets == 0
        rows.append({'M': M, 'true_continuum_radius': str(e),
                     'command_net_radius': str(F(1, 32 * M)),
                     'original_max_grid_error': str(raw_error),
                     'collapsed_max_grid_error': str(collapsed_error),
                     'collapsed_error_over_optimal_radius': str(collapsed_error / e),
                     'independent_transition_contract_failures': wrong_targets})
    return rows


def precision_witness() -> list[dict]:
    rows = []
    for b in (4, 8, 16, 32):
        for degree in (2, 3, 5):
            value = F((1 << b) - 1, 1 << b) ** degree
            assert value.denominator == 1 << (degree * b)
            rows.append({'input_binary_places': b, 'degree': degree,
                         'exact_product_binary_places': value.denominator.bit_length() - 1})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('papers/A1-english-v11'))
    parser.add_argument('--out', type=Path, default=Path('a1-v11-referee-reproduction'))
    args = parser.parse_args()
    source, out = args.source.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name, expected in EXPECTED.items():
        actual = hashlib.sha256((source / name).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f'Refusing unreviewed source {name}: {actual}')
        hashes[name] = actual
    sys.path.insert(0, str(source))
    import finite_compiler as fc
    import certified_compiler as cc
    baseline = suite_run(source, out, False, fc, cc)
    mutation = suite_run(source, out, True, fc, cc)
    assert baseline['assertions'] == mutation['assertions'] == 8207
    assert baseline['suite_passed'] and mutation['suite_passed']
    assert mutation['changed_entries'] == 775 and mutation['total_entries'] == 1389
    assert mutation['programs'] == 52
    result = {
        'reviewed_submission': SUBMISSION,
        'python': platform.python_version(), 'platform': platform.platform(),
        'source_sha256': hashes,
        'baseline': baseline, 'zero_transition_mutation': mutation,
        'independent_interval_witness': interval_witness(fc),
        'exact_intermediate_precision_witness': precision_witness(),
        'interpretation': 'The unmodified suite passes but does not reject collapsed transitions. '
                          'The residual theorem remains valid for corrupted tables with larger bounds. '
                          'These are finite diagnostics, not a counterexample to the unmodified compiler '
                          'or the continuum classification theorem. Exact rational bit lengths must be '
                          'distinguished from sufficient rounded input/output precision.',
        'not_executed': ['legacy v10 suite', 'legacy independent referee suite', 'LaTeX build',
                         'PDF visual inspection', 'full historical proof-preservation audit', 'GitHub Actions'],
    }
    # Check that neither baseline nor mutation changed any author source bytes.
    for name, expected in EXPECTED.items():
        assert hashlib.sha256((source / name).read_bytes()).hexdigest() == expected
    (out / 'EXECUTION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'baseline_checks': baseline['assertions'],
                      'mutation_checks_passed': mutation['assertions'],
                      'changed_transition_entries': mutation['changed_entries'],
                      'interval_budgets': [r['M'] for r in result['independent_interval_witness']],
                      'receipt': str(out / 'EXECUTION.json')}, indent=2))


if __name__ == '__main__':
    main()
