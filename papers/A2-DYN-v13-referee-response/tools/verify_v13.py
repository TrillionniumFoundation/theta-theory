#!/usr/bin/env python3
"""Exact source checks and finite algebra; not continuum proof certification."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from math import comb
import hashlib
import json
import re
import verify_v11

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v12-referee-response'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks() -> dict:
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 13, 'wrong revision')
    old = sorted((BASE / 'core').glob('*.tex'))
    require(len(old) == 29, 'incomplete v12 baseline')
    repaired = '15_exponential_returns.tex'
    for path in old:
        source = path.read_bytes()
        target = (ROOT / 'core' / path.name).read_bytes()
        if path.name == repaired:
            require(source.count(b'\\end{proof}+') == 1, 'repair is not unique')
            require(target == source.replace(b'\\end{proof}+', b'\\end{proof}', 1),
                    'unexpected change in explicit one-character repair')
        else:
            require(target == source, 'changed inherited mathematics: ' + path.name)
    inherited = sorted((BASE / 'tools').glob('*.py'))
    for path in inherited:
        require(path.read_bytes() == (ROOT / 'tools' / path.name).read_bytes(),
                'changed inherited diagnostic: ' + path.name)
    require((ROOT / 'references.tex').read_bytes() == (BASE / 'references.tex').read_bytes(),
            'changed inherited bibliography')
    for rel, sha in manifest['source_sha256'].items():
        require(digest(ROOT / rel) == sha, 'source hash differs: ' + rel)
    main = (ROOT / 'main.tex').read_text()
    require('A2-DYN, revision 13' in main, 'stale revision metadata')
    inputs = re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs) == len(set(inputs)) == 31, 'missing or duplicate core inclusion')
    require(set(s + '.tex' for s in inputs) ==
            {str(p.relative_to(ROOT)) for p in (ROOT / 'core').glob('*.tex')},
            'unlisted mathematical source')
    tex = main + '\n' + '\n'.join((ROOT / (s + '.tex')).read_text() for s in inputs)
    require(not any(ord(c) < 32 and c not in '\n\t\r' for c in tex), 'control character')
    require(r'\nef{' not in tex and r'\end{proof}+' not in tex, 'known TeX defect')
    labels = re.findall(r'\\label\{([^}]+)\}', tex)
    require(len(labels) == len(set(labels)), 'duplicate mathematical label')
    refs = set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', tex))
    require(refs <= set(labels), 'unresolved references: ' + str(refs - set(labels)))
    old_tex = '\n'.join(p.read_text() for p in BASE.rglob('*.tex'))
    old_labels = set(re.findall(r'\\label\{([^}]+)\}', old_tex))
    require(old_labels <= set(labels), 'deleted inherited mathematical label')
    cites = set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', tex):
        cites.update(s.strip() for s in group.split(','))
    bib = set(re.findall(r'\\bibitem\{([^}]+)\}', (ROOT / 'references.tex').read_text()))
    require(cites <= bib, 'unresolved citation')
    for env in ['theorem', 'lemma', 'proposition', 'corollary', 'proof', 'maintheorem']:
        require(tex.count('\\begin{' + env + '}') == tex.count('\\end{' + env + '}'),
                'unbalanced environment: ' + env)
    expected = {'lem:bv-finite-product', 'prop:unsmoothed-fourth',
                'thm:marked-L2-stopping', 'thm:marked-quadratic-moments',
                'cor:induced-cesaro-covariance', 'cor:marked-conditional-moments',
                'cor:positive-count-variance',
                'thm:LLT', 'thm:marked-return-band', 'lem:raw-residual-sum'}
    require(expected <= set(labels), 'missing new or retained theorem')
    require(manifest['full_raw_LLT_proved'] is False, 'unsupported raw LLT flag')
    require(manifest['uniform_positive_definiteness_proved'] is False, 'unsupported positivity flag')
    return {'included_core_files': len(inputs), 'inherited_core_byte_identical': len(old)-1,
            'explicit_one_character_repairs': [repaired],
            'inherited_python_files_byte_identical': len(inherited),
            'retained_mathematical_labels': len(old_labels), 'total_labels': len(labels),
            'proof_environments': tex.count(r'\begin{proof}'),
            'source_sha256': manifest['source_sha256']}


def new_finite_checks() -> dict:
    # The exact eigenphase is 2*pi*c* = 91/5000, in (0, 6),
    # hence strictly between 0 and 2*pi since pi > 3.
    count_phase = F(91, 5000)
    require(0 < count_phase < 6, 'count eigenphase could equal zero modulo 2*pi')
    l2_window = F(2, 3)
    characteristic_window = F(5, 9)
    require(1-l2_window == 2*l2_window-1 == F(1, 3), 'L2 window imbalance')
    require((1-l2_window)/2 == F(1, 6), 'L2 norm exponent')
    require(4*characteristic_window-2 == (1-characteristic_window)/2 == F(2, 9),
            'characteristic window imbalance')
    losses = [F(2, 9)-F(4, 200), F(2, 9)-F(5, 200)]
    require(all(x > F(3, 280) for x in losses), 'stopping consumes central budget')
    require(F(3, 280) < F(1, 6) and F(9, 175) < F(1, 2),
            'old marked-event class not contained in moment class')
    for q in range(2, 5):
        a = F(1, 2*q+1)
        require(1-2*q*a == a and a >= F(1, 9), 'smoothing/gap exponent')
    # Exact Rademacher fourth moment, including repeated indices.
    for m in range(1, 65):
        fourth = F(sum(comb(m,k)*(2*k-m)**4 for k in range(m+1)), 2**m)
        require(fourth == 3*m*m-2*m, 'four-index moment count')
    # Both terms of the ordered-gap bound. For theta=1/2,
    # sum_{a,b,c>=0} theta^max(a,b,c) = 26 and sum theta^(a+c) = 4.
    gap_cases = 0
    for m in range(1, 25):
        pair = F(0)
        residual = F(0)
        for a in range(m):
            for b in range(m-a):
                for c in range(m-a-b):
                    starts = m-a-b-c
                    pair += starts*F(1, 2**(a+c))
                    residual += starts*F(1, 2**max(a,b,c))
                    gap_cases += 1
        require(pair <= 4*m*m, 'pair term exceeds quadratic bound')
        require(residual <= 26*m, 'connected term exceeds linear bound')
    # Every prefix of a finite dyadic grid decomposes into at most one
    # aligned interval per scale. This is a combinatorial, not dynamical, test.
    prefixes = 0
    for power in range(9):
        size = 2**power
        for stop in range(size+1):
            start = 0
            lengths = []
            for p in reversed(range(power+1)):
                length = 2**p
                if start+length <= stop:
                    require(start % length == 0, 'unaligned dyadic block')
                    lengths.append(length)
                    start += length
            require(start == stop and len(lengths) == len(set(lengths)), 'prefix decomposition')
            prefixes += 1
    # Negative controls: the wrong characteristic window and a linear
    # fourth-moment bound must be rejected by the same arithmetic checks.
    require(4*F(3,5)-2 != (1-F(3,5))/2, 'bad window escaped negative control')
    require(3*64**2-2*64 > 10*64, 'linear fourth-moment claim escaped control')
    return {'count_eigenphase': str(count_phase), 'L2_squared_rate': '1/3', 'L2_and_covariance_rate': '1/6',
            'characteristic_stopping_rate': '2/9',
            'integrated_stopping_rates': [str(x) for x in losses],
            'rademacher_moment_cases': 64, 'ordered_gap_cases': gap_cases,
            'dyadic_prefix_cases': prefixes, 'negative_controls': 2,
            'finite_models_are_not_continuum_proofs': True}


if __name__ == '__main__':
    print(json.dumps({'revision': 13, 'source': source_checks(),
                      'new_finite_checks': new_finite_checks(),
                      'inherited_finite_checks': verify_v11.finite_checks(),
                      'continuum_proof_certified': False,
                      'full_raw_LLT_certified': False}, indent=2, sort_keys=True))
