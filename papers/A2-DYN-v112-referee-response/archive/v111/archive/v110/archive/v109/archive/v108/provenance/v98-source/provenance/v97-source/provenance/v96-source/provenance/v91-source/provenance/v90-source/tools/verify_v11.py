#!/usr/bin/env python3
"""Source identity and finite diagnostics, not continuum proof certification."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import cmath
import hashlib
import json
import re
import verify_v10

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v10-referee-response'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks() -> dict:
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 11, 'wrong revision')
    old = sorted((BASE / 'core').glob('*.tex'))
    require(len(old) == 27, 'incomplete reviewed baseline')
    for p in old:
        require(p.read_bytes() == (ROOT / 'core' / p.name).read_bytes(),
                'changed inherited mathematics: ' + p.name)
        require(digest(p) == manifest['baseline_core_sha256'][p.name],
                'baseline hash differs: ' + p.name)
    inherited_scripts = sorted((BASE / 'tools').glob('*.py'))
    for p in inherited_scripts:
        require(p.read_bytes() == (ROOT / 'tools' / p.name).read_bytes(),
                'changed inherited diagnostic: ' + p.name)
    for name, sha in manifest['new_core_sha256'].items():
        require(digest(ROOT / 'core' / name) == sha, 'new hash differs: ' + name)
    main = (ROOT / 'main.tex').read_text()
    require('A2-DYN, revision 11' in main, 'stale manuscript version')
    inputs = re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs) == len(set(inputs)) == 29, 'missing or duplicate inclusion')
    require(set(s + '.tex' for s in inputs) ==
            set(str(p.relative_to(ROOT)) for p in (ROOT / 'core').glob('*.tex')),
            'some mathematical source is not in the article')
    tex = main + '\n' + '\n'.join((ROOT / (s + '.tex')).read_text() for s in inputs)
    require(not any(ord(c) < 32 and c not in '\n\t\r' for c in tex), 'control character in TeX')
    labels = re.findall(r'\\label\{([^}]+)\}', tex)
    require(len(labels) == len(set(labels)), 'duplicate mathematical label')
    refs = set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', tex))
    require(refs <= set(labels), 'unresolved references: ' + str(refs - set(labels)))
    cites = set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', tex):
        cites.update(s.strip() for s in group.split(','))
    bibliography = set(re.findall(r'\\bibitem\{([^}]+)\}', (ROOT / 'references.tex').read_text()))
    require(cites <= bibliography, 'unresolved source citation')
    for env in ['theorem', 'lemma', 'proposition', 'corollary', 'proof', 'maintheorem']:
        require(tex.count('\\begin{' + env + '}') == tex.count('\\end{' + env + '}'),
                'unbalanced environment ' + env)
    expected = {'thm:intro-marked-return', 'thm:marked-return-band',
                'lem:marked-compensation', 'lem:two-sided-clock-window',
                'lem:marked-spectral', 'cor:marked-state-conditioning',
                'thm:LLT', 'cor:raw-from-growing-arc', 'lem:raw-residual-sum'}
    require(expected <= set(labels), 'missing claimed or retained statement')
    require(manifest['full_raw_LLT_proved'] is False, 'unsupported raw LLT completion claim')
    require(manifest['uniform_positive_definiteness_proved'] is False, 'unsupported positivity claim')
    return {'inherited_core_files_byte_identical': len(old),
            'inherited_diagnostic_scripts_byte_identical': len(inherited_scripts),
            'included_core_files': len(inputs), 'labels': len(labels),
            'proof_environments': tex.count(r'\begin{proof}'),
            'tex_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sorted(ROOT.rglob('*.tex'))}}


def visit_times(state: int, section: set[int], size: int, count: int, direction: int) -> list[int]:
    times = [0]
    step = 0
    while len(times) <= count:
        step += 1
        if (state + direction * step) % size in section:
            times.append(step)
    return times


def marked_compensation_cases() -> int:
    """Exhaustive finite-cycle identities including k=0 and k=n."""
    cases = 0
    for size in range(2, 8):
        records = [(i % 3 - 1, i % 5 - 2, 1, i + 2) for i in range(size)]
        total = tuple(sum(row[j] for row in records) for j in range(4))
        for mask in range(1, 1 << size):
            section = {i for i in range(size) if mask & (1 << i)}
            card = len(section)
            h = [tuple(card * records[i][j] - (total[j] if i in section else 0)
                       for j in range(4)) for i in range(size)]
            for x in section:
                forward = visit_times(x, section, size, 7, 1)
                for n in range(1, 8):
                    centered = tuple(card * sum(records[(x + t) % size][j] for t in range(forward[n]))
                                     - n * total[j] for j in range(4))
                    for k in range(n + 1):
                        y = (x + forward[k]) % size
                        left = visit_times(y, section, size, k, -1)[-1]
                        right = visit_times(y, section, size, n-k, 1)[-1]
                        require(left + right == forward[n], 'wrong total collision interval')
                        require((y-left) % size == x, 'wrong recentered initial state')
                        require(sum((y+t) % size in section for t in range(-left, right)) == n,
                                'incorrect endpoint convention in section visit count')
                        two_sided = tuple(sum(h[(y+t) % size][j] for t in range(-left, right))
                                          for j in range(4))
                        require(two_sided == centered, 'marked compensation identity failed')
                        cases += 1
    return cases


def chronological_pairings() -> dict:
    size = 7
    nu = [1 / size] * size
    h = [0.3, -0.8, 0.2, 1.1, -0.5, 0.4, -0.7]
    a = [complex(1 + j % 3, (-1)**j / 3) for j in range(size)]
    cases, negative_controls = 0, 0
    for z in [0.19, 0.71, -1.3]:
        phase = [cmath.exp(1j * z * x) for x in h]
        def advance(vector: list[complex], count: int) -> list[complex]:
            result = list(vector)
            for _ in range(count):
                result = [phase[(j-1) % size] * result[(j-1) % size] for j in range(size)]
            return result
        for r in range(9):
            for s in range(9):
                past = advance(nu, r)
                actual = sum(advance([a[j] * past[j] for j in range(size)], s))
                direct = sum(a[y] * cmath.exp(1j*z*sum(h[(y+t) % size] for t in range(-r, s)))
                             for y in range(size)) / size
                require(abs(actual-direct) < 2e-12, 'chronological pairing failed')
                wrong = sum(a[j]*advance(nu, r+s)[j] for j in range(size))
                if abs(wrong-direct) > 1e-6:
                    negative_controls += 1
                cases += 1
    require(negative_controls > 0, 'pairing test failed to distinguish misplaced mark')
    return {'cases': cases, 'misplaced_mark_negative_controls': negative_controls}


def finite_checks() -> dict:
    eps, theta = F(1, 200), F(1, 14)
    margins = {
        'variation_smoothing': theta - 4*eps,
        'observable_smoothing': theta/2 - 5*eps,
        'covariance_smoothing': theta - 6*eps,
        'principal_amplitude': F(1,2) - 4*theta - 5*eps,
        'cubic_remainder': F(1,2) - 6*theta - 7*eps,
        'clock_exception': F(1,5) - 4*eps,
        'clock_window': F(1,5) - 5*eps,
        'short_block': F(1,2) - 5*eps,
        'time_coefficient': 1 - 6*eps,
        'complementary_power_at_logarithmic_cutoff': 4 - 2*theta - 4*eps}
    expected = {'variation_smoothing': F(9,175), 'observable_smoothing': F(3,280),
                'covariance_smoothing': F(29,700), 'principal_amplitude': F(53,280),
                'cubic_remainder': F(51,1400), 'clock_exception': F(9,50),
                'clock_window': F(7,40), 'short_block': F(19,40),
                'time_coefficient': F(97,100)}
    for key, value in expected.items():
        require(margins[key] == value, 'incorrect exponent: ' + key)
    require(min(margins.values()) == F(3,280), 'incorrect leading rate')
    require(F(1,2)-2*theta-eps > 0 and F(1,2)-6*theta-3*eps > 0, 'analytic restriction fails')
    require(-F(1,2)+eps == -F(99,200), 'physical cutoff mismatch')
    # Illustrative conditioning regime within the theorem, not a measured billiard constant.
    beta, kappa = F(1,200), F(1,50)
    require(beta < F(3,280) and beta+kappa < F(9,175), 'conditioning example outside the range')
    return {'margins': {key: str(value) for key, value in margins.items()},
            'marked_compensation_cases': marked_compensation_cases(),
            'chronological_pairings': chronological_pairings(),
            'inherited': verify_v10.finite_checks(),
            'scope': 'finite exact identities, rational exponents and source preservation only'}


if __name__ == '__main__':
    print(json.dumps({'revision': 11, 'source': source_checks(), 'finite': finite_checks(),
                     'continuum_proof_certified': False, 'full_raw_LLT_certified': False,
                     'independent_human_review': False}, indent=2, sort_keys=True))
