#!/usr/bin/env python3
"""Source and finite algebra diagnostics. These do not certify continuum proofs."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import verify_v8

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v8-referee-response'

def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)

def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def canonical(s: str) -> str:
    # The complementary projection was renamed, not changed mathematically.
    return s.replace(r'Q_R^\perp', 'E_R')

def environments(s: str) -> list[str]:
    names = 'theorem|lemma|proposition|corollary|definition|proof'
    return [canonical(m.group(0)) for m in re.finditer(
        r'\\begin\{(' + names + r')\}(?:\[[^\]]*\])?.*?\\end\{\1\}', s, re.S)]

def source_checks() -> dict:
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == 9, 'incorrect revision')
    preserved, edited, env_count = [], [], 0
    for old in sorted((BASE / 'core').glob('*.tex')):
        new = ROOT / 'core' / old.name
        require(new.exists(), 'lost inherited core: ' + old.name)
        require(environments(old.read_text()) == environments(new.read_text()),
                'altered inherited mathematical environment: ' + old.name)
        old_labels = set(re.findall(r'\\label\{([^}]+)\}', old.read_text()))
        new_labels = set(re.findall(r'\\label\{([^}]+)\}', new.read_text()))
        require(old_labels <= new_labels, 'lost inherited labels: ' + old.name)
        env_count += len(environments(old.read_text()))
        (preserved if old.read_bytes() == new.read_bytes() else edited).append(old.name)
        require(digest(old) == manifest['baseline_core_sha256'][old.name],
                'baseline differs from the pinned manifest: ' + old.name)
    require(len(preserved) + len(edited) == 21, 'incomplete baseline')
    require(edited == manifest['expository_updates'], 'unrecorded inherited edit')
    for old in sorted((BASE / 'tools').glob('*.py')):
        require(old.read_bytes() == (ROOT / 'tools' / old.name).read_bytes(),
                'changed historical diagnostic: ' + old.name)
    main = (ROOT / 'main.tex').read_text()
    require('A2-DYN, revision 9' in main, 'metadata does not say revision 9')
    inputs = re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs) == len(set(inputs)) == 24, 'complete unique core inclusion')
    text = main + '\n' + '\n'.join((ROOT / (name + '.tex')).read_text() for name in inputs)
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    require(len(labels) == len(set(labels)), 'duplicate labels')
    refs = re.findall(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}', text)
    require(not (set(refs) - set(labels)), 'unresolved reference: ' + str(set(refs)-set(labels)))
    require(text.count(r'\begin{proof}') == text.count(r'\end{proof}'), 'unbalanced proofs')
    cites = set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', text):
        cites.update(x.strip() for x in group.split(','))
    bib = set(re.findall(r'\\bibitem\{([^}]+)\}', (ROOT / 'references.tex').read_text()))
    require(cites <= bib, 'missing bibliography keys')
    required = ['thm:intro-gaussian', 'thm:collision-covariance',
                'thm:actual-record-gaussian', 'thm:gaussian-kernel-coboundary',
                'thm:collision-functional', 'thm:actual-return-functional',
                'cor:physical-functional-gaussian', 'thm:LLT',
                'thm:phase-resolvent-criterion', 'lem:raw-residual-sum']
    require(set(required) <= set(labels), 'missing principal statements')
    require(manifest['full_raw_LLT_proved'] is False, 'unsupported raw-LLT status')
    return {'byte_identical_inherited_core': preserved, 'expository_updates': edited,
            'inherited_mathematical_environments_preserved': env_count,
            'historical_scripts_preserved': len(list((BASE/'tools').glob('*.py'))),
            'included_core_files': len(inputs), 'labels': len(labels),
            'proof_environments': text.count(r'\begin{proof}'),
            'tex_sha256': {str(p.relative_to(ROOT)): digest(p)
                           for p in sorted(ROOT.rglob('*.tex'))}}

def finite_checks() -> dict:
    checks = 0
    # Deterministic cycles: no independent-renewal surrogate is being tested.
    for length, section in [(7, {0, 2, 5}), (9, {0, 1, 4, 7})]:
        record = [(F(i%3-1), F((i*i)%5-2), F(1), F(i+3, 7))
                  for i in range(length)]
        c = F(len(section), length)
        mean = [sum(row[k] for row in record) / len(section) for k in range(4)]
        h = [[row[k] - mean[k]*int(i in section) for k in range(4)]
             for i, row in enumerate(record)]
        require(all(sum(row[k] for row in h) == 0 for k in range(4)), 'centering')
        checks += 1
        for start in sorted(section):
            index, visits, collisions = start, 0, 0
            js, hs = [F(0)]*4, [F(0)]*4
            for n in range(1, 17):
                while True:
                    visits += int(index in section)
                    js = [a+b for a,b in zip(js, record[index])]
                    hs = [a+b for a,b in zip(hs, h[index])]
                    index = (index+1) % length
                    collisions += 1
                    if index in section:
                        break
                require(visits == n, 'exact visits before nth return')
                require(hs == [js[k]-n*mean[k] for k in range(4)], 'stopped compensation')
                require(collisions == js[2], 'collision record')
                checks += 3
        tau = sum(row[3] for row in record)/length
        require(mean[2]-mean[3]/tau == 0, 'physical-clock compensation')
        checks += 1
    # Exact scale inequalities used by the analytic proofs.
    scalar = F(1, 13)
    require(F(1, 2)-6*scalar == scalar/2 == F(1,26), 'one-time balance')
    functional = F(1, 32)
    require(F(1,2)-6*functional > 0, 'functional cubic remainder')
    require(F(1,2)-8*functional > 0, 'coarse interpolation error')
    require(F(1,2)-4*functional > 0, 'projection amplitude error')
    stop = F(3,5)
    require(2*stop-1 == (1-stop)/2 == F(1,5), 'stopping balance')
    checks += 5
    # Every prefix has a disjoint dyadic decomposition using at most one
    # interval at each scale, the combinatorial part of the maximal bound.
    for levels in range(1,9):
        for end in range(2**levels+1):
            cursor, widths = 0, []
            for k in reversed(range(levels+1)):
                width = 2**k
                if cursor+width <= end:
                    require(cursor % width == 0, 'unaligned dyadic interval')
                    widths.append(width)
                    cursor += width
            require(cursor == end and len(widths) == len(set(widths)), 'dyadic prefix')
            checks += 1
    return {'finite_exact_checks': checks,
            'one_time_scale': 'delta=(1/4)n^(-1/13)',
            'functional_scale': 'delta=(1/4)n^(-1/32)',
            'stopping_window': 'ceil(n^(3/5))',
            'inherited_renewal_diagnostics': verify_v8.model_check(),
            'scope': 'finite identities and exponent arithmetic, not continuum validation'}

def main() -> None:
    print(json.dumps({'revision': 9, 'source': source_checks(), 'finite': finite_checks(),
        'full_raw_LLT_certified': False, 'independent_human_review': False},
        indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
