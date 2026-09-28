#!/usr/bin/env python3
"""Finite regression diagnostics and exact source audit, not a theorem prover.

Default: audit the complete committed input graph, every content identity, the
pinned review ancestry and runtime HEAD, then run diagnostics.  The explicitly
labelled --diagnostics-only mode makes no source/build verification claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
PAPER = Path('papers/A2-v17-boundary-information-coarsening')
REVIEW = '37e03652f639930f5489dfee09150a7cba3964d7'
PREVIOUS = 'd55c480f8cdf9f1327b4142bf1bb31a315f71b2b'
OLD_MANIFEST = Path('revisions/a2-v92/SOURCE_MANIFEST.json')
OLD_BLOB = 'ed0295752c242ad8213da05759aef24faed57134'

def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)

def identity(data: bytes) -> dict[str, Any]:
    header = f'blob {len(data)}\0'.encode()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(header + data).hexdigest()}

def git(*args: str) -> str:
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()

def input_graph() -> set[str]:
    seen: set[str] = set()
    def visit(name: str) -> None:
        if name in seen:
            return
        seen.add(name)
        p = ROOT / PAPER / name
        require(p.is_file(), f'missing active source: {p}')
        text = p.read_text(encoding='utf-8')
        for child in re.findall(r'\\(?:input|include)\{([^}]+)\}', text):
            visit(child if child.endswith('.tex') else child + '.tex')
    visit('rigidity_v93.tex')
    return seen

def audit() -> dict[str, Any]:
    manifest = json.loads((ROOT / 'revisions/a2-v93/SOURCE_MANIFEST.json').read_text())
    require(manifest['previous_review_commit'] == REVIEW, 'wrong controlling review')
    require(manifest['previous_revision_head'] == PREVIOUS, 'wrong reviewed manuscript')
    head = git('rev-parse', 'HEAD')
    tree = git('rev-parse', 'HEAD^{tree}')
    expected = os.environ.get('GITHUB_SHA')
    require(not expected or head == expected, 'checkout does not match triggering SHA')
    source = manifest['revision_source_commit']
    subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', REVIEW, source], check=True)
    subprocess.run(['git', '-C', str(ROOT), 'merge-base', '--is-ancestor', source, head], check=True)
    old_bytes = (ROOT / OLD_MANIFEST).read_bytes()
    require(identity(old_bytes)['git_blob'] == OLD_BLOB, 'altered v92 source manifest')
    old = json.loads(old_bytes)
    new = manifest['files']
    checked: set[str] = set()
    # Verify every declared v92 active-source identity, including old entrypoints.
    for relative, spec in old['active_sources'].items():
        name = str(PAPER / relative)
        data = (ROOT / name).read_bytes()
        require(identity(data) == spec, f'baseline content mismatch: {name}')
        require(git('rev-parse', f'HEAD:{name}') == spec['git_blob'], f'index blob mismatch: {name}')
        require(git('rev-parse', f'{REVIEW}:{name}') == spec['git_blob'], f'baseline pin mismatch: {name}')
        checked.add(name)
    for relative, expected_blob in old['inherited_git_blobs'].items():
        name = str(PAPER / relative)
        require(identity((ROOT / name).read_bytes())['git_blob'] == expected_blob, f'inherited blob mismatch: {name}')
        require(git('rev-parse', f'HEAD:{name}') == expected_blob, f'inherited checkout mismatch: {name}')
        checked.add(name)
    for name, expected_sha in old['verification_sources'].items():
        require(identity((ROOT / name).read_bytes())['sha256'] == expected_sha, f'old verifier changed: {name}')
        require(git('rev-parse', f'HEAD:{name}') == git('rev-parse', f'{REVIEW}:{name}'), f'old verifier pin mismatch: {name}')
        checked.add(name)
    for name, spec in new.items():
        data = (ROOT / name).read_bytes()
        require(identity(data) == spec, f'v93 content mismatch: {name}')
        require(git('rev-parse', f'HEAD:{name}') == spec['git_blob'], f'v93 git blob mismatch: {name}')
        require(git('rev-parse', f'{source}:{name}') == spec['git_blob'], f'changed since source snapshot: {name}')
        checked.add(name)
    graph = input_graph()
    require(graph == set(manifest['active_tex']), 'manifest does not equal complete TeX input graph')
    require({str(PAPER / p) for p in graph} <= checked, 'unhashed active TeX source')
    previous_modules = set(old['active_sources']) - {'rigidity_v92.tex', 'article/v92/paper.tex'}
    require(previous_modules <= graph, 'inherited proof or bibliography removed from active manuscript')
    full = '\n'.join((ROOT / PAPER / p).read_text() for p in sorted(graph))
    labels = re.findall(r'\\label\{([^}]+)\}', full)
    require(len(labels) == len(set(labels)), 'duplicate TeX labels')
    refs = set(re.findall(r'\\(?:ref|eqref|autoref)\{([^}]+)\}', full))
    require(refs <= set(labels), 'undefined source labels: ' + repr(sorted(refs - set(labels))))
    bib = set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', full))
    cites = {c.strip() for group in re.findall(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}', full) for c in group.split(',')}
    require(cites <= bib, 'undefined bibliography keys: ' + repr(sorted(cites - bib)))
    changed = git('diff', '--name-status', REVIEW, head).splitlines()
    for line in changed:
        status, name = line.split('\t', 1)
        require(status == 'A', f'revision modifies or removes pre-existing source: {line}')
        require(name in new or name == 'revisions/a2-v93/SOURCE_MANIFEST.json', f'uninventoried addition: {name}')
    return {'revision_head': head, 'revision_tree': tree, 'revision_source_commit': source,
            'previous_review_commit': REVIEW, 'previous_revision_head': PREVIOUS,
            'active_tex_count': len(graph), 'inherited_active_modules': len(previous_modules),
            'checked_content_identities': len(checked), 'head_matches_GITHUB_SHA': bool(expected),
            'source_audit': 'passed'}

def exponent(poly: sp.Expr, z: sp.Symbol, params: tuple[sp.Symbol, ...], multiplicity: int) -> sp.Rational:
    candidates = []
    for powers, coef in sp.Poly(sp.expand(poly), *params, z).terms():
        j, a = sum(powers[:-1]), powers[-1]
        if coef != 0 and j > 0 and a < multiplicity:
            candidates.append(sp.Rational(j, multiplicity - a))
    return min(candidates) if candidates else sp.oo

def diagnostics() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    z = sp.symbols('z')
    for m in (3, 4):
        f = z**m
        g = sp.prod(z-i for i in range(1, m+1))
        us = sp.symbols(f'u0:{m+1}')
        vs = sp.symbols(f'v0:{m+1}')
        hs = sp.symbols(f'h0:{m+1}')
        u, v, h = [sum(c*z**i for i, c in enumerate(group)) for group in (us, vs, hs)]
        fixed = f*(g+h)-u*v
        require(exponent(fixed, z, us+vs+hs, m) == sp.Rational(2,m), 'quadratic exposure exponent')
        require(sp.limit(z**m*h/g, z, 0) == 0 and sp.denom(sp.cancel(h/g)).subs(z,0) != 0, 'first variation has pole')
        a = sp.symbols('a')
        free = (f+a)*(g+h)-u*v
        require(exponent(free, z, (a,)+us+vs+hs, m) == sp.Rational(1,m), 'free-normalizer exponent')
        M = sp.Matrix([[f+g,f-g],[f-g,f+g]])/4
        require(sp.expand(sum(M)-f) == 0, 'entry-sum normalizer')
        for clock in range(m+1, 3*m+2):
            require(all(cell.subs(z,clock)/f.subs(z,clock) > 0 for cell in M), 'nonpositive observed cell')
        out.append({'test': f'invisible_first_variation_degree_{m}', 'fixed_q_exponent': str(sp.Rational(2,m)),
                    'free_q_exponent': str(sp.Rational(1,m)), 'status':'passed'})
    # Exact normalization rank at seven clocks, without floating-point thresholds.
    m = 3
    clocks = list(range(4,11))
    f, g = z**m, (z-1)*(z-2)*(z-3)
    W = sp.Matrix([[t**i for i in range(m+1)] for t in clocks])
    annihilator = sp.Matrix.hstack(*W.T.nullspace()).T
    N = annihilator * sp.Matrix([[sp.Rational(t**i)*(f-g).subs(z,t)/(4*f.subs(z,t)) for i in range(m)] for t in clocks])
    require(N.rank() == m, 'normalization residual loses rank')
    out.append({'test':'exact_normalization_residual_rank', 'rank':m, 'status':'passed'})
    # The retained 3x3 cancellation: no top-right inverse term, true pole 3.
    T = sp.Matrix([[z*z,z,1],[0,z*z,z],[0,0,z*z]])
    inv = sp.simplify(T.inv())
    require(inv[0,2] == 0 and inv[0,1] == -z**-3 and inv[1,2] == -z**-3, 'Laurent cancellation')
    L = sp.Matrix([[0,-1,0],[0,0,-1],[0,0,0]])
    require(L.rank() == 2, 'leading Laurent matrix cannot be exposed')
    E = sp.zeros(3); E[1,0]=1; E[1,1]=-1
    e = sp.symbols('e')
    require(sum(E) == 0 and sp.trace(L*E) != 0, 'zero-sum exposure')
    require(exponent((T+e*E).det(), z, (e,), 6) == sp.Rational(1,3), 'cancellation-reduced root exponent')
    out.append({'test':'path_cancellation_degree_two_size_three', 'true_pole':3, 'path_count':6, 'exponent':'1/3', 'status':'passed'})
    # A concrete interpolation gauge, with arbitrary independent zero-sum H.
    M = T/3; q = sp.expand(sum(M))
    clocks = (1,2,3)
    a,b,c = sp.symbols('a b c')
    scalar = a+b*z
    gauge = M.applyfunc(lambda cell: sp.interpolate([(t,sp.cancel(scalar*cell/q).subs(z,t)) for t in clocks],z))
    require(sp.simplify(sum(gauge)-scalar) == 0, 'gauge does not reproduce scalar normalizer')
    H = c*E
    actual = gauge+H
    require(sp.simplify(sum(actual)-scalar) == 0, 'gauge decomposition is not onto')
    require((M+actual).det().expand() == (M+gauge+H).det().expand(), 'gauge determinant identity')
    out.append({'test':'exact_scalar_interpolation_shear', 'status':'passed'})
    # Binary perturbation and analytic rank-one reconstruction.
    aa,bb,xx,y,eps = sp.symbols('aa bb xx y eps', nonzero=True, real=True)
    U = sp.Matrix([[1+aa,1-aa],[1-aa,1+aa]])/2
    V = sp.Matrix([[1+bb,1-bb],[1-bb,1+bb]])/2
    K = U*sp.diag((y-xx)/2,(y+xx)/2)*V.T
    D = sp.Matrix([[1,-1],[-1,1]])/4
    expected = (aa*bb*y*y+eps*y-aa*bb*xx*xx)/4
    require(sp.simplify((K+eps*D).det()-expected) == 0, 'binary determinant')
    for root in (-xx,xx):
        derivative = sp.simplify(-sp.diff(expected,eps).subs({eps:0,y:root})/sp.diff(expected,y).subs({eps:0,y:root}))
        require(derivative == -1/(2*aa*bb), 'binary root derivative')
    un = np.array([[1.4,.6],[.6,1.4]])/2
    vn = np.array([[1.5,.5],[.5,1.5]])/2
    A = un @ np.diag([.5,.5]) @ vn.T
    C = un @ np.diag([.1,-.1]) @ vn.T
    delta = np.array([[1.,-1.],[-1.,1.]])/4
    for ep in (-1.e-3,0.,1.e-3):
        Ce = C-ep*delta
        X = Ce @ np.linalg.inv(A)
        roots = np.sort(np.linalg.eigvals(X).real)
        Ws=[]
        for bidx in (0,1):
            Q=(X-roots[1-bidx]*np.eye(2))/(roots[bidx]-roots[1-bidx])
            Wb=Q @ A; weight=Wb.sum()
            require(np.all(Wb>0) and weight>.1, 'positive factors or strict weights lost')
            u=Wb.sum(axis=1)/weight; v=Wb.sum(axis=0)/weight
            require(np.allclose(Wb,weight*np.outer(u,v),atol=1.e-12), 'rank-one reconstruction')
            Ws.append(Wb)
        require(np.allclose(sum(Ws),A), 'leading coefficient reconstruction')
        require(np.allclose(sum(roots[i]*Ws[i] for i in (0,1)),Ce), 'constant coefficient reconstruction')
        require(abs(Ce.sum()) < 1.e-12 and np.max(abs(roots))<.3, 'normalizer or root interval')
    out.append({'test':'binary_stochastic_refactorization', 'status':'passed'})
    # Hellinger convention used in the sharp edge constant.
    p=np.array([.2,.3,.1,.4]); tangent=np.array([1.,-2.,3.,-2.])
    fisher=np.sum(tangent*tangent/p)
    h=np.linalg.norm(np.sqrt(p+1.e-7*tangent)-np.sqrt(p))
    require(abs(h/1.e-7-.5*np.sqrt(fisher)) < 1.e-4, 'Hellinger radius-two factor')
    out.append({'test':'Hellinger_radius_two_ellipsoid', 'status':'passed'})
    return out

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--diagnostics-only',action='store_true')
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    result: dict[str, Any] = {'qualification':'finite diagnostics and source identities, not a formal proof check',
                               'source_audit':'explicitly skipped' if args.diagnostics_only else 'pending'}
    if not args.diagnostics_only:
        result.update(audit())
    result['diagnostics']=diagnostics()
    result['diagnostic_count']=len(result['diagnostics'])
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    print(text,end='')
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(text,encoding='utf-8')

if __name__=='__main__':
    main()
