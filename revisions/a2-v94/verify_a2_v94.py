#!/usr/bin/env python3
"""Finite regression and exact-source checks, not a formal proof verifier."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
REVIEW = '7d5e9d80a6033399afe633da21b44e4d6f435a2f'

def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def diagnostics() -> list[str]:
    z, r, c, x = sp.symbols('z r c x', real=True)
    f, g = z*(z-r)**2, (z-2*r/3)**3
    h = sp.expand((1-c)*f+c*g)
    check(sp.factor(sp.discriminant(h, z)+4*r**6*c*(1-c)**2/27) == 0,
          'isolated cubic pencil discriminant identity failed')
    check(sp.factor(h.subs(z, 0)+8*r**3*c/27) == 0,
          'endpoint sign identity failed')
    centered = z**3-r**2*(1-c)*z/3+2*r**3*(1-c)/27
    check(sp.expand(h.subs(z,z+2*r/3)-centered) == 0,
          'depressed cubic identity failed')
    out = ['cubic discriminant, endpoint and depressed coefficients: exact']
    b1,b2=sp.symbols('b1 b2')
    check(sp.factor(b1/(1-c)*h+(b2-c*b1/(1-c))*g-(b1*f+b2*g)) == 0,
          'ambient coefficient-kernel identity failed')
    out.append('ambient coefficient-kernel curve: exact')
    for m in (3,4,6):
        f0=z**m
        g0=sp.prod(z-sp.Rational(j, m+2) for j in range(1,m+1))
        for q in (3,5,9):
            B=sp.Matrix([[f0+x**2+x**q,x*g0],[x,g0]])
            tangent=sp.Matrix([[f0,x*g0],[x,g0]])
            check(sp.expand(B.det()-g0*(f0+x**q)) == 0,
                  'full composed determinant identity failed')
            check(sp.expand(tangent.det()-g0*(f0-x**2)) == 0,
                  'affine tangent determinant identity failed')
        check(sp.expand(sp.Matrix([[f0+x**2,x*g0],[x,g0]]).det()-f0*g0) == 0,
              'curved spectral-rigidity identity failed')
    out.append('composed jets versus affine tangents: 9 exact cases plus rigidity')
    p=sp.diag(10,sp.Rational(10,3),5,sp.Rational(5,2))
    T=sp.diag(2,1,2,1)
    J=sp.Matrix([[1,0],[0,1],[-1,0],[0,-1]])
    transported=T.inv().T*p*T.inv()
    check((T*J).T*transported*(T*J) == J.T*p*J,
          'transported Fisher form was not preserved')
    naive=sp.diag(5,sp.Rational(10,3),sp.Rational(5,2),sp.Rational(5,2))
    check((T*J).T*naive*(T*J) != J.T*p*J,
          'nonisometric left-right witness unexpectedly became an isometry')
    out.append('Fisher transport and failure of naive cell reinterpretation: exact')
    clocks=np.linspace(1.2,1.8,7)
    rv=.75; sv=.5; alpha=.4
    uv=np.array([.4,.6]); V=np.array([[.8,.3],[.2,.7]])
    def observation(split: float) -> np.ndarray:
        fs=clocks*(clocks-rv)**2
        gs=(clocks-sv)*((clocks-sv)**2-split**2)
        qv=alpha*fs+(1-alpha)*gs
        row=(alpha*fs[:,None]*V[:,0]+(1-alpha)*gs[:,None]*V[:,1])/qv[:,None]
        return uv[None,:,None]*row[:,None,:]
    P=observation(0)
    qv=alpha*clocks*(clocks-rv)**2+(1-alpha)*(clocks-sv)**3
    derivative=-(1-alpha)*(clocks-sv)[:,None,None]/qv[:,None,None]*(
        uv[None,:,None]*V[:,1][None,None,:]-P)
    gamma=.5*np.sqrt(np.mean(np.sum(derivative**2/P,axis=(1,2))))
    check(gamma>0 and np.all(P>0), 'positive-cell lower witness failed')
    ratios=[]
    for split in (.01,.005,.002,.001):
        P1=observation(split)
        hell=np.sqrt(np.mean(np.sum((np.sqrt(P1)-np.sqrt(P))**2,axis=(1,2))))
        ratios.append(float(hell/split**2/gamma))
    check(abs(ratios[-1]-1)<2e-5, 'stochastic Hellinger quadratic constant failed to converge')
    out.append('actual stochastic split: h/u^2 converges to positive Fisher coefficient; ratios='+repr(ratios))
    # The old diagnostic wording is not propagated: a pole would be a failure.
    gg=sp.prod(z-j for j in (1,2,3))
    check(sp.denom(sp.cancel((z+1)/gg)).subs(z,0) != 0,
          'expected analytic first variation at zero, but found a pole')
    out.append('invisible first variation: analytic at zero (correct failure wording)')
    return out

def active_graph(entry: str) -> set[str]:
    found: set[str]=set()
    def visit(name: str) -> None:
        if name in found: return
        path=PAPER/name
        check(path.is_file(), 'missing active TeX input: '+name)
        found.add(name)
        text=re.sub(r'(?m)(?<!\\)%.*$', '', path.read_text())
        for child in re.findall(r'\\(?:input|include)\{([^}]+)\}',text):
            child=child if child.endswith('.tex') else child+'.tex'
            visit(child)
    visit(entry)
    return found

def audit() -> dict:
    manifest=json.loads((ROOT/'revisions/a2-v94/SOURCE_MANIFEST.json').read_text())
    head=git('rev-parse','HEAD')
    if os.environ.get('GITHUB_SHA'):
        check(head == os.environ['GITHUB_SHA'], 'runtime HEAD differs from GITHUB_SHA')
    graph=active_graph(manifest['entrypoint'])
    check(graph == set(manifest['active_tex']), 'active TeX graph differs from manifest')
    old=json.loads((ROOT/'revisions/a2-v93/SOURCE_MANIFEST.json').read_text())
    expected=set(old['active_tex'])-{'article/v93/paper.tex','rigidity_v93.tex'}
    check(expected <= graph, 'an inherited proof or bibliography module was removed')
    # The base review must be available: a full checkout is part of the build contract.
    git('cat-file','-e',REVIEW+'^{commit}')
    preserved={}
    for name in sorted(set(old['active_tex'])):
        path='papers/A2-v17-boundary-information-coarsening/'+name
        baseline=subprocess.check_output(['git','show',REVIEW+':'+path],cwd=ROOT)
        actual=(ROOT/path).read_bytes()
        check(actual == baseline, 'inherited source modified: '+path)
        preserved[path]=hashlib.sha256(actual).hexdigest()
    for path, expected_hash in manifest['new_source_sha256'].items():
        check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected_hash,
              'new source hash mismatch: '+path)
    changes=git('diff','--name-status',REVIEW,head).splitlines()
    for change in changes:
        status,path=change.split('\t',1)
        check(status == 'A', 'revision must not modify or remove inherited paths: '+change)
        check(path.startswith(('papers/A2-v17-boundary-information-coarsening/article/v94/',
                               'revisions/a2-v94/')) or path in {
                                   'papers/A2-v17-boundary-information-coarsening/rigidity_v94.tex',
                                   '.github/workflows/a2-v94-native.yml','A2_REVISION_V94_REVIEW_READY.md'},
              'change outside declared A2 v94 scope: '+path)
    return {'revision_head':head,'revision_tree':git('rev-parse','HEAD^{tree}'),
            'controlling_review':REVIEW,'active_tex_count':len(graph),
            'active_tex':sorted(graph),'preserved_sha256':preserved,
            'diff_vs_review':changes}

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--diagnostics-only',action='store_true')
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    result={'qualification':'Finite symbolic/numerical regressions are not universal proof verification.',
            'diagnostics':diagnostics()}
    if not args.diagnostics_only:
        result.update(audit())
    else:
        result['source_audit']='not run: diagnostics-only mode'
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(text)
    print(text)

if __name__=='__main__':
    main()
