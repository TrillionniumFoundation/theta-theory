#!/usr/bin/env python3
"""Finite exact checks and source preservation, not a proof certificate.

The nonlinear model below is a point-coordinate pullback of a quadratic
symplectic generating action. It tests the cocycle and Hessian identities;
it is explicitly not a Euclidean billiard simulation or a realization theorem.
Only the standard library is used. Every check survives Python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()

def check(category: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError('Verification failed: ' + category)
    COUNTS[category] += 1

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def sources(rel: str = 'main.tex', stack: tuple[str, ...] = ()) -> list[tuple[str, str]]:
    if rel in stack:
        raise RuntimeError('TeX input cycle: ' + rel)
    text = (ROOT / rel).read_text(encoding='utf-8')
    out = [(rel, text)]
    for item in re.findall(r'\\input\{([^}]+)\}', text):
        out += sources(item + '.tex', stack + (rel,))
    return out

BLOCK = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}', re.S)

def preservation() -> dict:
    active = sources()
    names = [name for name, _ in active]
    joined = '\n'.join(text for _, text in active)
    baseline = json.loads((ROOT / 'history/v13-active-blocks.json').read_text())
    current = Counter(digest(m.group().encode()) for _, text in active for m in BLOCK.finditer(text))
    old = sorted(digest(m.group().encode()) for name, text in active if name in baseline['inputs'] for m in BLOCK.finditer(text))
    check('source:every_reviewed_input_active', set(baseline['inputs']) <= set(names))
    check('source:unique_active_inputs', len(names) == len(set(names)))
    check('source:reviewed_formal_block_multiset_retained', digest(('\n'.join(old)+'\n').encode()) == baseline['sorted_block_multiset_sha256'])
    check('source:reviewed_block_count', len(old) == baseline['block_count'] == 218)
    edited = {'main.tex', 'article/01_introduction.tex', 'article/29_two_flight_benchmark.tex', 'v5/references.tex'}
    for name, sha in baseline['active_file_git_blobs'].items():
        if name in edited:
            check('source:edited_input_archived_exactly', git_blob((ROOT / 'history/v13-reviewed' / name).read_bytes()) == sha)
        else:
            check('source:unchanged_active_input', git_blob((ROOT / name).read_bytes()) == sha)
    labels = re.findall(r'\\label\{([^}]+)\}', joined)
    refs = re.findall(r'\\(?:ref|eqref)\{([^}]+)\}', joined)
    keys = set(re.findall(r'\\bibitem\{([^}]+)\}', joined))
    cited = {k.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', joined) for k in group.split(',')}
    check('source:labels_unique', len(labels) == len(set(labels)))
    check('source:internal_references_resolved', all(r in labels or r.startswith('TC-') for r in refs))
    check('source:bibliography_resolved', cited <= keys)
    check('source:control_characters', all(ord(c) >= 32 or c in '\r\n\t' for c in joined))
    check('source:universal_abstract_repaired', 'every fixed finite-dimensional family' not in (ROOT/'main.tex').read_text())
    check('source:new_results_active', {'prop:v14-normal-form','thm:v14-intrinsic-density','cor:v14-width'} <= set(labels))
    return {'reviewed_commit': baseline['commit'], 'reviewed_blocks': len(old),
            'current_blocks': sum(current.values()), 'active_inputs': len(names),
            'all_reviewed_formal_blocks_retained_byte_identically': True,
            'edited_active_inputs_archived': sorted(edited)}

def sh(lam: F, n: int) -> F:
    return (lam**(-n)-lam**n)/2

def zeta(u: F, alpha: F) -> F:
    return u/(1-alpha*u)

def inverse_zeta(z: F, alpha: F) -> F:
    return z/(1+alpha*z)

def B(u: F, alpha: F) -> F:
    return 1/(1-alpha*u)**2

def Bprime(u: F, alpha: F) -> F:
    return 2*alpha/(1-alpha*u)**3

def exact_models() -> dict:
    geometries = cases = 0
    for ell in (F(1,3), F(1,2), F(2,3), F(4,5)):
        c, sinh = (ell+1/ell)/2, sh(ell,1)
        for ratio in (F(1), (1+c)/2, 2/(1+c)):
            for g in (F(1,2), F(1), F(3,2)):
                curv = [c*ratio, c/ratio]
                a = [ratio*sinh/g, sinh/(ratio*g)]
                r = [ratio*ell, ell/ratio]
                lam = ell**2
                check('geometry:positive_margin', all(x>1 for x in curv) and all(0<x<1 for x in r))
                check('geometry:return_multiplier', r[0]*r[1] == lam)
                geometries += 1
                for b in (0,1):
                    o=1-b
                    check('geometry:Riccati_first_hit', 1/(curv[o]+g*a[o]) == r[b])
                    check('geometry:stable_Hessian', (curv[b]-r[b])/g == a[b])
                    for n in range(1,13):
                        # The factor two converts the return number to flights.
                        direct = 2*a[b]*lam**n/(1-lam**(2*n))
                        check('normalization:exact_csch', direct == a[b]/sh(ell,2*n))
                        j=n
                        terminal=(o+j)%2
                        root_tail=a[o] if o==terminal else sinh/g
                        root_full=a[b] if b==terminal else sinh/g
                        finite_ratio=(root_tail/sh(ell,j))/(root_full/sh(ell,j+1))
                        expected=(1/r[b])*(1-ell**(2*j+2))/(1-ell**(2*j))
                        check('normalization:finite_reference_ratio', finite_ratio==expected)
                    for alpha_b,alpha_o in ((F(0),F(1,3)),(F(1,4),F(-1,5)),(F(-1,2),F(2,5))):
                        for u in (F(-1,8),F(-1,20),F(0),F(1,20),F(1,8)):
                            z=zeta(u,alpha_b)
                            w=inverse_zeta(r[b]*z,alpha_o)
                            zw=zeta(w,alpha_o)
                            bw=B(w,alpha_o)
                            phi_prime=r[b]*B(u,alpha_b)/(1+alpha_o*r[b]*z)**2
                            check('cocycle:exact_one_flight', bw*phi_prime == r[b]*B(u,alpha_b))
                            check('linearizer:exact_first_flight', zw==r[b]*z)
                            ell2=(curv[o]*zw-z)*bw/g
                            tail1=a[o]*zw*bw
                            check('action:stationary_middle', ell2+tail1==0)
                            cost=(curv[b]*z*z+curv[o]*zw*zw-2*z*zw)/(2*g)
                            check('action:Bellman_identity', cost+a[o]*zw*zw/2==a[b]*z*z/2)
                            ell22=curv[o]*bw*bw/g+(curv[o]*zw-z)*Bprime(w,alpha_o)/g
                            tail2=a[o]*(bw*bw+zw*Bprime(w,alpha_o))
                            negell12=B(u,alpha_b)*bw/g
                            check('action:physical_implicit_derivative', negell12/(ell22+tail2)==phi_prime)
                            if alpha_o and w:
                                check('negative_control:nonlinear_Hessian_term_matters',
                                      negell12/(curv[o]*bw*bw/g+tail2)!=phi_prime)
                            second=inverse_zeta(r[o]*zeta(w,alpha_o),alpha_b)
                            check('linearizer:two_type_return', second==inverse_zeta(lam*z,alpha_b))
                            for n in (1,2,4,8,12):
                                rn=inverse_zeta(lam**n*z,alpha_b)
                                norm_derivative=B(u,alpha_b)/(1+alpha_b*lam**n*z)**2
                                check('iteration:normalized_value_remainder',
                                      rn/lam**n-z == -alpha_b*lam**n*z*z/(1+alpha_b*lam**n*z))
                                check('iteration:normalized_derivative_remainder',
                                      norm_derivative-B(u,alpha_b) == B(u,alpha_b)*
                                      (-2*alpha_b*lam**n*z-(alpha_b*lam**n*z)**2)/(1+alpha_b*lam**n*z)**2)
                            # Stable action S=(a/2) zeta^2: exact sublevel width.
                            radius=F(1,10)
                            uminus, uplus=inverse_zeta(-radius,alpha_b),inverse_zeta(radius,alpha_b)
                            check('width:exact_pushforward', zeta(uplus,alpha_b)-zeta(uminus,alpha_b)==2*radius)
                            cases += 1
    return {'positive_rational_geometries':geometries,'nonlinear_endpoint_cases':cases,
            'model':'point-coordinate pullback of a quadratic generating action; not a Euclidean billiard'}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    retained=preservation(); models=exact_models()
    result={'schema':'a2-v14-verification-v1','status':'pass','total_explicit_checks':sum(COUNTS.values()),
            'checks_by_category':dict(sorted(COUNTS.items())),'retention':retained,'exact_models':models,
            'limitations':['Finite rational diagnostics do not certify continuum estimates or constitute formal proof.',
            'The nonlinear test action is not asserted to be a Euclidean billiard realization.',
            'All-order and parameter-uniform assertions are justified by the manuscript proofs, not by the grid.',
            'No remote CI, nonlinear trajectory simulation, or full-profile minimax result is claimed.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','total_explicit_checks','retention')},sort_keys=True))

if __name__=='__main__':
    main()
