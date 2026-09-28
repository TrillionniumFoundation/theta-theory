#!/usr/bin/env python3
"""Fail-closed preservation and exact finite controls for A2 revision 63.

No removable assertions; output is identical under ordinary and optimized
Python. Finite arithmetic controls and source hashes are not proof certificates.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import re
from source_provenance import graph, strip_comments, INPUT, require

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'history/v62-review-baseline'
MODIFIED = {
    'README.md', 'main.tex', 'rigidity.tex',
    'article/00_structural_introduction_v48.tex',
    'journal/00_principal_introduction_v61.tex',
    'article/23f2_finite_experiment_analytic_inverse_v62.tex',
    'journal/references_v56.tex', 'v5/references_v43.tex',
}

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def base_bytes(name: str) -> bytes:
    return ((ARCHIVE if name in MODIFIED else ROOT) / name).read_bytes()

def base_graph(name: str, seen: set[str] | None = None) -> set[str]:
    seen = set() if seen is None else seen
    if name in seen:
        return seen
    seen.add(name)
    for raw in INPUT.findall(strip_comments(base_bytes(name).decode('utf-8'))):
        require(re.fullmatch(r'[A-Za-z0-9_./-]+', raw) is not None, 'Dynamic baseline input')
        base_graph(raw if raw.endswith('.tex') else raw + '.tex', seen)
    return seen

def main() -> None:
    manifest = json.loads((ARCHIVE / 'SOURCE_MANIFEST.json').read_text())
    require(manifest['source_commit'] == '037c80dc44d8191e6f808591ea0651e813234d06', 'Wrong baseline')
    require(manifest['source_tree'] == '160735632f3977d47dcf708fb2292699ab79fafd', 'Wrong baseline tree')
    require(len(manifest['files']) == 767, 'Unexpected baseline inventory')
    changed, unchanged = [], []
    for name, meta in manifest['files'].items():
        p = ROOT / name
        require(p.is_file() and not p.is_symlink(), 'Inherited path missing/nonregular: ' + name)
        require(bool(p.stat().st_mode & 0o111) == (meta['mode'] == '100755'), 'Inherited executable mode changed: ' + name)
        original = base_bytes(name)
        require((len(original), hashlib.sha256(original).hexdigest(), blob(original)) ==
                (meta['bytes'], meta['sha256'], meta['git_blob']), 'Baseline bytes mismatch: ' + name)
        if p.read_bytes() != original:
            require(name in MODIFIED, 'Unapproved inherited change: ' + name)
            changed.append(name)
        else:
            unchanged.append(name)
    require(set(changed) == MODIFIED, 'Changed-path authorization mismatch')
    old_active, new_active = set(), set()
    for stem in ('two_collision', 'main', 'rigidity'):
        old_active |= base_graph(stem + '.tex')
        new_active |= graph(ROOT, stem + '.tex')
    require(len(old_active) == 126 and old_active <= new_active, 'Inherited active proof path lost')
    require(new_active - old_active == {'article/00d_orbit_local_comparison_v63.tex'}, 'Unexpected active additions')
    proof = 'article/23f2_finite_experiment_analytic_inverse_v62.tex'
    old, new = base_bytes(proof).decode(), (ROOT / proof).read_text()
    pattern = re.compile(r'\\begin\{(lemma|theorem|corollary|proposition)\}.*?\\end\{\1\}', re.S)
    old_blocks = [m.group() for m in pattern.finditer(old)]
    new_blocks = [m.group() for m in pattern.finditer(new)]
    require(len(old_blocks) == 5 and old_blocks == new_blocks, 'Finite-experiment statement changed')
    require(r'\label{eq:v63-pilot-time}' in new and r'jg_++3\varepsilon' in new, 'Grid correction missing')
    require(r'A failed scan may reach $t_{L_{\mathrm{grid}}}$.' in new, 'All-history distinction missing')
    bib_counts = {}
    for name in ('journal/references_v56.tex', 'v5/references_v43.tex'):
        original = base_bytes(name).decode()
        current = (ROOT / name).read_text()
        cleaned = re.sub(r'\\bibitem\{Zelditch2009\}.*?(?=\\end\{thebibliography\})', '', current, flags=re.S)
        require(original == cleaned, 'Inherited bibliography changed: ' + name)
        require(current.count(r'\bibitem{Zelditch2009}') == 1, 'Missing/duplicate Zelditch item')
        bib_counts[name] = len(re.findall(r'\\bibitem\{', original))
    for name in ('main.tex', 'rigidity.tex'):
        require((ROOT / name).read_text().replace('revision 63', 'revision 62').replace('A2 v63', 'A2 v62') ==
                base_bytes(name).decode(), 'Entry change exceeds metadata: ' + name)
    comparison = (ROOT / 'article/00d_orbit_local_comparison_v63.tex').read_text()
    require(r'\cite{Zelditch2009}' in comparison and r'\ref{thm:v4-factorization}' in comparison,
            'Comparison not anchored to literature/mechanism')
    for name in ('journal/00_principal_introduction_v61.tex', 'article/00_structural_introduction_v48.tex'):
        current = (ROOT / name).read_text()
        require(current.replace('\\input{article/00d_orbit_local_comparison_v63}\n\n', '') == base_bytes(name).decode(),
                'Inherited introduction altered beyond shared insertion')

    # Direct rational grid computation, including integral and fractional q.
    grid_cases = fractional = 0
    for j in range(2, 18, 2):
        for gm in (Q(1, 3), Q(1), Q(5, 2)):
            for width in (Q(0), Q(1, 7), Q(1, 2), Q(3, 5), Q(4, 3)):
                for epsilon in (Q(1, 1000), Q(2, 101), Q(3, 77), Q(1, 4), Q(2, 3), Q(1)):
                    gp = gm + width
                    q = j * width / epsilon
                    ceil = -((-q.numerator) // q.denominator)
                    L = ceil + 2
                    last = j * gm + L * epsilon
                    gap = last - j * gp
                    require(gap == (ceil - q + 2) * epsilon, 'Grid identity failed')
                    require(2 * epsilon <= gap < 3 * epsilon, 'All-history bound failed')
                    require(L + 1 == ceil + 3, 'Cap point count changed')
                    if q.denominator != 1:
                        require(gap > 2 * epsilon, 'Fractional old-bound counterexample missing')
                        fractional += 1
                    grid_cases += 1
    j, gm, gp, eps = 2, Q(1), Q(3, 2), Q(2, 101)
    q = j * (gp - gm) / eps
    L = -((-q.numerator) // q.denominator) + 2
    require(j * gm + L * eps == Q(308, 101), 'Referee final-grid control failed')
    require(j * gp + 2 * eps == Q(307, 101), 'Referee former bound control failed')
    # Algebraic exponent and pilot power controls; not lower bounds or minimax checks.
    rate_cases = 0
    for omega in (Q(1, 7), Q(1, 2), Q(2), Q(5, 2)):
        for gamma in (Q(0), Q(1, 3), Q(1), Q(3)):
            for theta in (Q(1, 5), Q(1, 2), Q(1)):
                z = omega / (4 * omega + gamma)
                require((1 - gamma / (4 * omega + gamma) - 2 * z) / 2 == z, 'Calibrated variance balance')
                zc = omega / (12 * omega + gamma)
                require(12 * zc + gamma / (12 * omega + gamma) == 1, 'Complete-cap exponent balance')
                require(theta * z > 0 and theta * zc > 0 and theta * zc < theta * z, 'Rate distinction')
                require(4 * 3 == 12 and 4 * Q(1, 2) - 1 == 1, 'Pilot coordinate/cost powers')
                rate_cases += 1
    report = {
        'schema': 'a2-v63-preservation-and-finite-controls-1',
        'status': 'passed',
        'baseline_source_commit': manifest['source_commit'],
        'baseline_source_files': len(manifest['files']),
        'inherited_paths_retained': len(changed) + len(unchanged),
        'byte_identical_inherited_paths': len(unchanged),
        'modified_inherited_paths': sorted(changed),
        'byte_exact_archived_originals': len(changed),
        'baseline_active_inputs': len(old_active),
        'current_active_inputs': len(new_active),
        'added_active_inputs': sorted(new_active - old_active),
        'unchanged_finite_experiment_statement_bodies': len(old_blocks),
        'inherited_bibliography_items_retained': bib_counts,
        'exact_grid_cases': grid_cases,
        'fractional_grid_old_bound_counterexamples': fractional,
        'referee_example': {'last_time': '308/101', 'former_bound': '307/101'},
        'rational_rate_balance_cases': rate_cases,
        'scope': 'Source preservation and finite arithmetic controls, not a full proof or significance certificate',
    }
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
