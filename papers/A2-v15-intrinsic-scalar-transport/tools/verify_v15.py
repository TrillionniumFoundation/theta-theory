#!/usr/bin/env python3
"""A2 v15 exact diagnostics and explicit source-retention checks.

Use --scope edited for the pinned revision-source subset; use --scope full
in a complete repository checkout. Neither mode is a formal proof checker.
All checks use explicit exceptions and remain active under Python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()
PINS = {
    'main.tex': 'cf90db9a5d217de54c3389f409de034e0f7330e5',
    'preamble.tex': '7e0de97c08dd2e12187193aff89f3ca4712f430f',
    'article/01_introduction.tex': '907daec5fbc1478423e46a75d311719aa8dfc4db',
    'article/16_hyperbolic_coordinates.tex': '14210a28d78baadb7e6d750c813c4e4aa31a0eee',
    'article/23_two_contact_rigidity.tex': '49d0468658a5b219d5a51720714ffb3194e1110a',
    'v5/references.tex': '16bdda298381063b94de8fba0f7d355337fd5ca3',
}
MATH_EDITED = ['article/01_introduction.tex', 'article/16_hyperbolic_coordinates.tex',
               'article/23_two_contact_rigidity.tex']
ACTIVE_EDITED = {'main.tex', 'v5/references.tex', *MATH_EDITED}
BLOCK = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}', re.S)
INPUT = re.compile(r'\\input\{([^}]+)\}')


def check(category: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError('Verification failed: ' + category)
    COUNTS[category] += 1


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def old_text(rel: str) -> str:
    return (ROOT / 'history/v14-reviewed' / rel).read_text(encoding='utf-8')


def reverse_notation(text: str) -> str:
    return text.replace('\\varrho', '\\lambda').replace('\\mathfrak r_b', 'r_b')


def edited_retention() -> dict:
    for rel, sha in PINS.items():
        check('source:pinned_original', git_blob((ROOT/'history/v14-reviewed'/rel).read_bytes()) == sha)
    old_inputs = INPUT.findall(old_text('main.tex'))
    new_inputs = INPUT.findall((ROOT/'main.tex').read_text())
    check('source:all_top_level_inputs_in_order', old_inputs == new_inputs)
    check('source:top_level_input_count', len(old_inputs) == 52)
    blocks = 0
    for rel in MATH_EDITED:
        before, after = old_text(rel), (ROOT/rel).read_text()
        if rel.endswith('23_two_contact_rigidity.tex'):
            after = reverse_notation(after)
            check('source:entire_contact_section_alpha_equivalent', before == after)
        for match in BLOCK.finditer(before):
            check('source:inherited_formal_block_retained', match.group() in after)
            blocks += 1
        old_labels = set(re.findall(r'\\label\{([^}]+)\}', before))
        new_labels = set(re.findall(r'\\label\{([^}]+)\}', after))
        check('source:inherited_labels_retained', old_labels <= new_labels)
    section = (ROOT/'article/16_hyperbolic_coordinates.tex').read_text()
    check('source:new_scalar_proof_active', '\\input{article/16a_scalar_linearization}' in section)
    check('source:new_physical_identity_active', '\\input{article/16b_determinant_transport}' in section)
    combined = '\n'.join((ROOT/rel).read_text() for rel in [*PINS,
        'article/16a_scalar_linearization.tex', 'article/16b_determinant_transport.tex'])
    labels = re.findall(r'\\label\{([^}]+)\}', combined)
    check('source:edited_labels_unique', len(labels) == len(set(labels)))
    check('source:no_control_characters', all(ord(c) >= 32 or c in '\r\n\t' for c in combined))
    old_bib = set(re.findall(r'\\bibitem\{([^}]+)\}', old_text('v5/references.tex')))
    new_bib = set(re.findall(r'\\bibitem\{([^}]+)\}', (ROOT/'v5/references.tex').read_text()))
    check('source:all_bibliography_items_retained', old_bib <= new_bib)
    check('source:scalar_attribution', {'Sternberg', 'EN', 'A2ReviewV14'} <= new_bib)
    check('source:preamble_unchanged', git_blob((ROOT/'preamble.tex').read_bytes()) == PINS['preamble.tex'])
    return {'pinned_original_files': len(PINS), 'main_input_commands': len(old_inputs),
            'inherited_formal_blocks_in_edited_math_files': blocks,
            'preservation': 'Exact blocks, allowing only the explicitly reversed alpha-renaming in the contact section.'}


def walk_inputs(root: Path, rel: str = 'main.tex', stack: tuple[str, ...] = ()) -> list[tuple[str, str]]:
    if rel in stack:
        raise RuntimeError('TeX input cycle: ' + rel)
    text = (root/rel).read_text(encoding='utf-8')
    result = [(rel, text)]
    for item in INPUT.findall(text):
        result += walk_inputs(root, item + '.tex', stack + (rel,))
    return result


def full_retention() -> dict:
    base = ROOT.parent/'A2-v14-intrinsic-boundary-normal-form'
    if not base.is_dir():
        raise RuntimeError('Full mode requires the frozen sibling v14 native manuscript directory.')
    for rel, sha in PINS.items():
        check('full:frozen_base', git_blob((base/rel).read_bytes()) == sha)
    old, new = walk_inputs(base), walk_inputs(ROOT)
    old_names = {p for p, _ in old}; new_names = [p for p, _ in new]
    check('full:every_old_input_active', old_names <= set(new_names))
    check('full:no_duplicate_input', len(new_names) == len(set(new_names)))
    old_blocks = new_blocks = 0
    for rel, text in old:
        current = (ROOT/rel).read_text()
        if rel.endswith('23_two_contact_rigidity.tex'):
            current = reverse_notation(current)
        if rel not in ACTIVE_EDITED:
            check('full:unchanged_active_file', current == text)
        for match in BLOCK.finditer(text):
            check('full:inherited_formal_block', match.group() in current)
            old_blocks += 1
    for _, text in new:
        new_blocks += len(list(BLOCK.finditer(text)))
    joined = '\n'.join(t for _, t in new)
    labels = re.findall(r'\\label\{([^}]+)\}', joined)
    refs = re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', joined)
    keys = set(re.findall(r'\\bibitem\{([^}]+)\}', joined))
    cited = {k.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', joined) for k in group.split(',')}
    check('full:labels_unique', len(labels) == len(set(labels)))
    check('full:references_resolved', all(r in labels or r.startswith('TC-') for r in refs))
    check('full:citations_resolved', cited <= keys)
    excluded = ACTIVE_EDITED | {'README.md', 'RESPONSE_TO_REFEREES.md', 'PROOF_LEDGER.md',
        'HISTORICAL_DERIVATION_AUDIT.md', 'LITERATURE_VERIFICATION.md', 'SOURCE_PINS.json', 'VERIFICATION.json'}
    files = 0
    generated = {'.aux', '.log', '.out', '.toc', '.fls', '.fdb_latexmk', '.synctex.gz', '.pyc'}
    for path in sorted(base.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or path.suffix in generated:
            continue
        rel = path.relative_to(base).as_posix()
        check('full:every_native_file_present', (ROOT/rel).is_file())
        if rel not in excluded:
            check('full:unchanged_native_file', path.read_bytes() == (ROOT/rel).read_bytes())
        else:
            check('full:overridden_original_archived', path.read_bytes() == (ROOT/'history/v14-reviewed'/rel).read_bytes())
        files += 1
    return {'active_inputs': len(new), 'inherited_formal_blocks': old_blocks,
            'current_formal_blocks': new_blocks, 'native_files_checked': files}


def sh(rho: Q, k: int) -> Q:
    return (rho**(-k)-rho**k)/2


def coth(rho: Q, k: int) -> Q:
    return (1+rho**(2*k))/(1-rho**(2*k))


def tanh(rho: Q, k: int) -> Q:
    return (1-rho**(2*k))/(1+rho**(2*k))


def exact_geometry() -> dict:
    cases = 0
    for rho in (Q(1,4), Q(1,3), Q(1,2), Q(2,3), Q(3,4)):
        c, sinh = (rho+1/rho)/2, sh(rho, 1)
        for ratio in (Q(1), (1+c)/2, 2/(1+c)):
            for g in (Q(1,2), Q(1), Q(3,2)):
                curv = [c*ratio, c/ratio]
                a = [ratio*sinh/g, sinh/(ratio*g)]
                r = [ratio*rho, rho/ratio]
                lam = rho*rho
                check('geometry:positive_margin', all(x > 1 for x in curv) and all(0 < x < 1 for x in r))
                check('geometry:return_multiplier', r[0]*r[1] == lam)
                check('geometry:curvature_ratio', a[0]/a[1] == ratio*ratio)
                for b in (0, 1):
                    o = 1-b
                    check('geometry:first_hit_Riccati', 1/(curv[o]+g*a[o]) == r[b])
                    for n in range(1, 10):
                        check('normalization:flight_return_conversion', a[b]/sh(rho, 2*n) == 2*a[b]*lam**n/(1-lam**(2*n)))
                        check('negative_control:wrong_return_multiplier', a[b]/sh(rho, 2*n) != 2*a[b]*rho**n/(1-rho**(2*n)))
                        j = n; terminal = (o+j)%2
                        tail = a[o] if terminal == o else sinh/g
                        full = a[b] if terminal == b else sinh/g
                        check('normalization:both_parities', r[b]*(tail/sh(rho,j))/(full/sh(rho,j+1)) == (1-rho**(2*j+2))/(1-rho**(2*j)))
                for m in range(2, 13):
                    em = rho**(4*(m-1))/(1-rho**(4*(m-1))) - rho**(4*m)/(1-rho**(4*m))
                    om = 1/(2*sh(rho,2*(m-1))) - 1/(2*sh(rho,2*m))
                    p = coth(rho,2*m)+2*m*em
                    q = 1/sh(rho,2*m)+2*m*om
                    plus = coth(rho,m)+2*m*(rho**(2*(m-1))/(1-rho**(2*(m-1))) - rho**(2*m)/(1-rho**(2*m)))
                    minus = m*tanh(rho,m-1)-(m-1)*tanh(rho,m)
                    check('contact:P_plus_Q', p+q == plus and plus > 0)
                    check('contact:P_minus_Q', p-q == minus and minus > 0)
                    k = [Q(4,2**m*(m+1)*math.factorial(m)**2)/x**m for x in a]
                    check('contact:curvature_ratio_normalization', k[0]*ratio**(2*m) == k[1])
                    x,y=Q(m,3),Q(1-m,5)
                    f0,f1=-p*k[0]*x-q*k[1]*y,-q*k[0]*x-p*k[1]*y
                    check('contact:block_inverse_first', -(p*f0-q*f1)/((p*p-q*q)*k[0]) == x)
                    check('contact:block_inverse_second', -(-q*f0+p*f1)/((p*p-q*q)*k[1]) == y)
                cases += 1
    return {'positive_rational_geometries': cases, 'includes_equal_curvatures': True}


def exact_scalar_products() -> dict:
    cases = 0
    for lam in (Q(1,9), Q(1,4), Q(4,9), Q(9,16)):
        for alpha in (Q(-1,2), Q(0), Q(1,3), Q(3,5)):
            for u in (Q(-1,5), Q(-1,11), Q(0), Q(1,13), Q(1,4)):
                b = lambda x: 1/(1-alpha*x)**2
                z = lambda x: x/(1-alpha*x)
                x, product = u, Q(1)
                for n in range(1, 13):
                    derivative = lam/(1-alpha*(1-lam)*x)**2
                    product *= derivative/lam
                    x = lam*x/(1-alpha*(1-lam)*x)
                    closed = lam**n*u/(1-alpha*(1-lam**n)*u)
                    check('scalar:actual_iterated_point', x == closed)
                    check('scalar:finite_derivative_product', product == 1/(1-alpha*(1-lam**n)*u)**2)
                    check('scalar:exact_product_tail', product*b(x) == b(u))
                    check('scalar:normalized_coordinate', z(x) == lam**n*z(u))
                    check('scalar:exact_value_remainder', x/lam**n-z(u) == -alpha*lam**n*z(u)**2/(1+alpha*lam**n*z(u)))
                    if alpha and u:
                        check('negative_control:finite_product_not_limit', product != b(u))
                    cases += 1
    for coefficients in ([Q(1),Q(1,2),Q(-1,7)], [Q(1),Q(-1,4),Q(2,9),Q(1,11)]):
        for t in (Q(1,100),Q(1,20),Q(1,5)):
            profile = sum(v*t**(2*i) for i,v in enumerate(coefficients))
            width_dt = sum(2*v*t**(2*i) for i,v in enumerate(coefficients))
            check('width:weighted_derivative_inverse', width_dt/2 == profile)
            check('width:normalized_initial_coefficient', coefficients[0] == 1)
    return {'finite_product_cases': cases,
            'scope': 'Exact scalar conjugacy models and polynomial width identity; not physical realization or uniform estimates.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=('edited','full'), default='full')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = {'schema': 'a2-v15-verification-v1', 'status': 'pass', 'source_scope': args.scope,
              'edited_retention': edited_retention(), 'geometry': exact_geometry(),
              'scalar_products': exact_scalar_products()}
    result['full_retention'] = full_retention() if args.scope == 'full' else None
    result['checks_by_category'] = dict(sorted(COUNTS.items()))
    result['total_explicit_checks'] = sum(COUNTS.values())
    result['limitations'] = [
        'Exact finite algebra does not prove uniform infinite-dimensional estimates.',
        'The scalar models do not assert Euclidean billiard realization.',
        'Edited mode does not claim the full native TeX input graph was locally materialized.',
        'No journal significance or acceptance follows from a diagnostic count.']
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(json.dumps({'status':result['status'], 'source_scope':args.scope,
                      'total_explicit_checks':result['total_explicit_checks']}, sort_keys=True))


if __name__ == '__main__':
    main()
