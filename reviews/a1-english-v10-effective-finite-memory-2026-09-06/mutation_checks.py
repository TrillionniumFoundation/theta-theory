#!/usr/bin/env python3
"""Referee mutation control for A1 v10; never modifies the author files.

Usage: python mutation_checks.py PAPER_DIR OUTPUT_DIR
PAPER_DIR must contain the exact pinned finite_compiler.py and tests/test_v10.py.
The mutation zeros the returned program's dyadic output tables while retaining
its transitions, state counts, output precision, and the real Machine class.
A passed mutated suite exposes a test-coverage gap, not an author-code defect.
"""
import contextlib
import dataclasses
import hashlib
import importlib.util
import io
import json
from fractions import Fraction
from pathlib import Path
import sys

EXPECTED = {
    'finite_compiler.py': '286c956da1e8b4845d8457488e56845cf15c352b',
    'tests/test_v10.py': 'dc3d6b4632d69e0eab2894645d6d203342d1a4a0',
}


def git_blob(path: Path) -> str:
    b = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    paper, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    hashes = {name: git_blob(paper / name) for name in EXPECTED}
    if hashes != EXPECTED:
        raise RuntimeError(f'Author-source identity mismatch: {hashes}')
    spec = importlib.util.spec_from_file_location('a1_author_tests_mutation', paper / 'tests/test_v10.py')
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    original_compile = module.compile_tables
    mutated_program_count = 0
    original_outputs_checked = 0
    corrupted_outputs_detected = 0

    def compile_with_zero_outputs(*args, **kwargs):
        nonlocal mutated_program_count, original_outputs_checked, corrupted_outputs_detected
        program, audit = original_compile(*args, **kwargs)
        predict = args[6] if len(args) > 6 else kwargs['predict']
        scale = 1 << program.output_bits
        for stage, histories in enumerate(audit.representatives):
            for i, hist in enumerate(histories):
                for q, truth in enumerate(predict(hist)):
                    stored = Fraction(program.outputs[stage][i][q], scale)
                    assert abs(stored-truth) <= Fraction(1, 2*scale)
                    original_outputs_checked += 1
                    if abs(truth) > Fraction(1, 2*scale):
                        corrupted_outputs_detected += 1
        zero_outputs = tuple(tuple(tuple(0 for _ in query_row) for query_row in stage)
                             for stage in program.outputs)
        mutated_program_count += 1
        return dataclasses.replace(program, outputs=zero_outputs), audit

    module.compile_tables = compile_with_zero_outputs
    old_argv = sys.argv[:]
    stdout = io.StringIO()
    try:
        sys.argv = [str(paper / 'tests/test_v10.py'), str(out / 'MUTATED_AUTHOR_TESTS.json')]
        with contextlib.redirect_stdout(stdout):
            module.main()
    finally:
        sys.argv = old_argv
    mutated = json.loads((out / 'MUTATED_AUTHOR_TESTS.json').read_text())
    assert mutated['status'] == 'passed' and mutated['assertions'] == 7904
    assert mutated_program_count == 9
    # At n=2, N=3, query 0 is the single constant factor 1/2.
    # Thus the corrupt table has squared error 1/4, not dyadic-rounding error.
    model = module.Model(Fraction(0), 'uniform')
    true_prediction = model.predictions(((0, 3), (7, 3)))[0]
    assert true_prediction == Fraction(1, 2)
    squared_error = true_prediction ** 2
    assert squared_error == Fraction(1, 4)
    minimum_test_bound = 192 * Fraction(1, 4)
    assert minimum_test_bound == 48 and minimum_test_bound > 1
    result = {
        'submission_sha': 'd9f48fe08fd694e636c287be7646ae7d723ce3b8',
        'author_git_blob_hashes': hashes,
        'mutation': 'Replace every returned Program.outputs entry by integer zero; all other fields unchanged.',
        'mutated_programs': mutated_program_count,
        'additional_referee_output_checks_on_unmodified_tables': original_outputs_checked,
        'zeroed_entries_detected_by_referee_output_checks': corrupted_outputs_detected,
        'author_suite_after_mutation': {'status': mutated['status'], 'assertions': mutated['assertions']},
        'constant_query_truth_at_n2': str(true_prediction),
        'mutated_prediction': '0',
        'constant_query_squared_error': str(squared_error),
        'accumulated_offgrid_assertions': mutated['categories']['accumulated_offgrid_error'],
        'minimum_offgrid_test_rhs': str(minimum_test_bound),
        'maximum_possible_raw_infinity_error': '1',
        'interpretation': 'Undetected intentional corruption demonstrates coverage weakness, not a defect in the unmodified compiler or a counterexample to the theorem.'
    }
    (out / 'MUTATION_DIAGNOSTICS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
