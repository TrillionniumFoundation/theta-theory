#!/usr/bin/env python3
"""Exact source preservation and finite diagnostics; not continuum certification."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import verify_v9

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v9-referee-response'

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_checks() -> dict:
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 10, 'wrong revision')
    old = sorted((BASE / 'core').glob('*.tex'))
    require(len(old) == 24, 'incomplete v9 baseline')
    for p in old:
        require(p.read_bytes() == (ROOT / 'core' / p.name).read_bytes(),
                'changed inherited mathematical source: ' + p.name)
        require(digest(p) == manifest['baseline_core_sha256'][p.name],
                'baseline differs from the frozen source: ' + p.name)
    for p in sorted((BASE / 'tools').glob('*.py')):
        require(p.read_bytes() == (ROOT / 'tools' / p.name).read_bytes(),
                'changed historical diagnostic: ' + p.name)
    for name, sha in manifest['new_core_sha256'].items():
        require(digest(ROOT / 'core' / name) == sha, 'new source hash mismatch: ' + name)
    main = (ROOT / 'main.tex').read_text()
    require('A2-DYN, revision 10' in main, 'stale manuscript metadata')
    inputs = re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs) == len(set(inputs)) == 27, 'missing or duplicate inclusion')
    text = main + '\n' + '\n'.join((ROOT / (s + '.tex')).read_text() for s in inputs)
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    require(len(labels) == len(set(labels)), 'duplicate labels')
    refs = set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', text))
    require(refs <= set(labels), 'unresolved references: ' + str(refs - set(labels)))
    cites = set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', text):
        cites.update(s.strip() for s in group.split(','))
    bib = set(re.findall(r'\\bibitem\{([^}]+)\}', (ROOT / 'references.tex').read_text()))
    require(cites <= bib, 'unresolved citations')
    for env in ['theorem', 'lemma', 'proposition', 'corollary', 'proof', 'maintheorem']:
        require(text.count('\\begin{' + env + '}') == text.count('\\end{' + env + '}'),
                'unbalanced ' + env)
    expected = {'thm:intro-gaussian', 'thm:intro-major-arc', 'thm:growing-major-arc',
                'cor:raw-from-growing-arc', 'thm:LLT', 'lem:splice',
                'thm:phase-resolvent-criterion', 'lem:raw-residual-sum',
                'prop:semialgebraic-slicing', 'lem:density-norm-details',
                'lem:chronological-product', 'prop:coarse-interpolation'}
    require(expected <= set(labels), 'missing required mathematical statements')
    require(not manifest['full_raw_LLT_proved'], 'unsupported full raw LLT claim')
    require(not manifest['uniform_positive_definiteness_proved'], 'unsupported positivity claim')
    return {'byte_identical_baseline_core_files': len(old), 'included_core_files': len(inputs),
            'labels': len(labels), 'proof_environments': text.count(r'\begin{proof}'),
            'tex_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sorted(ROOT.rglob('*.tex'))}}

def finite_checks() -> dict:
    eps, theta = F(1, 200), F(1, 14)
    require(0 < eps < F(1, 134), 'band exponent range')
    require(10 * eps < theta < (F(1, 2) - 7 * eps) / 6, 'empty scale interval')
    margins = {
        'initial_smoothing': theta - 4 * eps,
        'observable_smoothing': theta / 2 - 5 * eps,
        'covariance_smoothing': theta - 6 * eps,
        'projector_amplitude': F(1, 2) - 4 * theta - 5 * eps,
        'cubic_remainder': F(1, 2) - 6 * theta - 7 * eps,
        'clock_exception': F(1, 5) - 4 * eps,
        'clock_window': F(1, 5) - 5 * eps,
        'clock_rounding': 1 - 6 * eps}
    require(min(margins.values()) == F(3, 280), 'wrong integrated rate')
    require(margins['cubic_remainder'] == F(51, 1400), 'cubic arithmetic')
    require(margins['clock_window'] == F(7, 40), 'clock arithmetic')
    require(sum(x == F(3, 280) for x in margins.values()) == 1, 'logarithmic dominance')
    require(F(1, 2) - 2 * theta - eps > 0, 'analytic radius')
    require(F(1, 2) - 6 * theta - 3 * eps > 0, 'pointwise cubic smallness')
    require(-F(1, 2) + eps < -F(2, 5), 'new band is not smaller than old cutoff')
    # Endpoint of the feasibility interval is obtained by exact linear algebra.
    require(10 * F(1, 134) == (F(1, 2) - 7 * F(1, 134)) / 6,
            'incorrect feasibility threshold')
    # The interpolation inequalities are elementary finite diagnostics, not
    # a verification of probabilistic hypotheses or of the continuum theorem.
    cases = 0
    for denominator in range(1, 41):
        for numerator in range(denominator + 1):
            ratio = F(numerator, denominator)
            require(ratio ** 4 <= ratio ** 2, 'fractional-block fourth moment')
            cases += 1
    return {'band_exponent': str(eps), 'smoothing_exponent': str(theta),
            'integrated_error_margins': {k: str(v) for k, v in margins.items()},
            'interpolation_cases': cases, 'inherited': verify_v9.finite_checks(),
            'scope': 'source, rational exponents and finite identities only'}

if __name__ == '__main__':
    print(json.dumps({'revision': 10, 'source': source_checks(), 'finite': finite_checks(),
                      'full_raw_LLT_certified': False, 'independent_human_review': False},
                     indent=2, sort_keys=True))
