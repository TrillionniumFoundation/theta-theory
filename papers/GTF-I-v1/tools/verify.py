#!/usr/bin/env python3
"""Finite reproducibility diagnostics, not formal verification of theorems."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import itertools
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS: dict[str, int] = {}

def require(ok: bool, group: str, message: str) -> None:
    if not ok:
        raise RuntimeError(f"{group}: {message}")
    CHECKS[group] = CHECKS.get(group, 0) + 1

def determinant(a: list[list[F]]) -> F:
    b = [row[:] for row in a]
    result = F(1)
    for k in range(len(b)):
        pivot = next((i for i in range(k, len(b)) if b[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            b[k], b[pivot] = b[pivot], b[k]
            result = -result
        p = b[k][k]
        result *= p
        for j in range(k, len(b)):
            b[k][j] /= p
        for i in range(k + 1, len(b)):
            mult = b[i][k]
            for j in range(k, len(b)):
                b[i][j] -= mult * b[k][j]
    return result

def update(p: list[F], gamma: F, eps: F, v: list[F], y: int):
    d = len(p) - 1
    q = [(1 - gamma)*x + gamma/F(d+1) for x in p]
    r = [F(1)] + [1 + y*eps*x for x in v]
    z = sum(qi*ri for qi, ri in zip(q, r))
    return [qi*ri/z for qi, ri in zip(q, r)], q, r, z

def l1(p, q):
    return sum(abs(x-y) for x,y in zip(p,q))

def structural_checks() -> None:
    sources = [ROOT/'main.tex', ROOT/'preamble.tex', ROOT/'references.tex']
    sources += sorted((ROOT/'sections').glob('*.tex'))
    text = '\n'.join(p.read_text() for p in sources)
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', text)
    require(len(set(labels)) == len(labels), 'source', 'duplicate labels')
    require(not (set(refs)-set(labels)), 'source', 'missing labels')
    bib = set(re.findall(r'\\bibitem\{([^}]+)\}', text))
    cites = set()
    for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', text):
        cites.update(x.strip() for x in group.split(','))
    require(not (cites-bib), 'source', 'missing bibliography entries')
    for name in re.findall(r'\\input\{([^}]+)\}', text):
        require((ROOT/(name+'.tex')).is_file(), 'source', f'missing input {name}')
    for token in ['TODO', 'PLACEHOLDER', 'TBD', 'proof omitted']:
        require(token not in text, 'source', f'unfinished marker {token}')
    for env in ['theorem','lemma','proposition','corollary','proof','definition','example','remark']:
        require(text.count('\\begin{'+env+'}') == text.count('\\end{'+env+'}'),
                'source', f'unbalanced {env}')

def exact_diagnostics(mutant: str | None) -> None:
    for d in range(1, 6):
        uniform = [F(1,d+1)]*(d+1)
        tilts = [uniform, [F(i+1, (d+1)*(d+2)//2) for i in range(d+1)]]
        for gamma, eps, y in itertools.product([F(4,5), F(9,10),F(1)],
                                              [F(0),F(1,8),F(1,4)], [-1,1]):
            v = [F((-1)**i, i+2) for i in range(d)]
            fp, q, r, z = update(tilts[0],gamma,eps,v,y)
            ft, _, _, _ = update(tilts[1],gamma,eps,v,y)
            require(sum(fp)==1 and min(fp)>=0,'Bayes','normalization')
            require(1-eps<=z<=1+eps,'Bayes','evidence range')
            rho = 2*(1+eps)/(1-eps)*(1-gamma)
            require(rho<=F(2,3),'contraction','uniform factor')
            require(l1(fp,ft)<=rho*l1(*tilts),'contraction','sample difference')
            if eps:
                inv = [(fp[i+1]*q[0]/(fp[0]*q[i+1])-1)/(y*eps)
                       for i in range(d)]
                require(inv==v,'odds','inverse')
                # Derivative is in v=tanh(u), hence no sech factor in this matrix.
                jac = [[(q[i+1]*y*eps/z if i==j else F(0))
                        -(q[i+1]*r[i+1]/z)*(q[j+1]*y*eps/z)
                        for j in range(d)] for i in range(d)]
                formula = q[0]*math.prod(q[1:])*(y*eps)**d/z**(d+1)
                if mutant=='omit-jacobian-q0':
                    formula /= q[0]
                require(determinant(jac)==formula,'Jacobian','exact determinant')
            pa,_,_,za=update(uniform,gamma,eps,v,1)
            pb,_,_,zb=update(uniform,gamma,eps,v,-1)
            require(za/2+zb/2==1,'Bayes','both reports counted')
            require([za/2*x+zb/2*y for x,y in zip(pa,pb)]==uniform,
                    'Bayes','posterior barycentre')
        # Reachable-domain invariance along a finite, deterministic legal sequence.
        for gamma,eps in itertools.product([F(4,5),F(1)],[F(0),F(1,4)]):
            p=uniform[:]
            radius=2*eps/(gamma*(1-eps))
            for t in range(12):
                v=[F((-1)**(i+t),i+2) for i in range(d)]
                p,_,_,_=update(p,gamma,eps,v,(-1)**t)
                require(l1(p,uniform)<=radius,'invariant-domain','sample path')
    # Printed appendix example.
    pa,_,_,za=update([F(1,2)]*2,F(4,5),F(1,4),[F(1,2)],1)
    pb,_,_,zb=update([F(1,2)]*2,F(4,5),F(1,4),[F(1,2)],-1)
    require((za/2,zb/2,pa[1],pb[1])==(F(17,32),F(15,32),F(9,17),F(7,15)),
            'printed-example','probabilities')
    require(F(1,2)+pa[1]/4==F(43,68),'printed-example','positive probe')
    require(F(1,2)+pb[1]/4==F(37,60),'printed-example','negative probe')
    for M in range(1,41):
        error=sum(F(1,12*M**3) for _ in range(M))
        require(error==F(1,12*M*M),'quantization','uniform cells')
    # A finite positive binary channel: exact score projection and variance gap.
    p=[F(1,3),F(2,3)]; dp=[F(1),F(-1)]
    channel=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]]
    q=[sum(p[i]*channel[i][j] for i in range(2)) for j in range(2)]
    dq=[sum(dp[i]*channel[i][j] for i in range(2)) for j in range(2)]
    info=sum(dp[i]**2/p[i] for i in range(2))
    coarse=sum(dq[j]**2/q[j] for j in range(2))
    residual=sum(p[i]*channel[i][j]*(dp[i]/p[i]-dq[j]/q[j])**2
                 for i,j in itertools.product(range(2),repeat=2))
    require(info-coarse==residual and residual>=0,'information','conditional variance')
    # Pressure Hessian at zero is beta times the variance.
    beta=F(3); values=[F(-1),F(2)]; weights=[F(1,3),F(2,3)]
    mean=sum(p*x for p,x in zip(weights,values))
    var=sum(p*(x-mean)**2 for p,x in zip(weights,values))
    numerator_second=beta**2*sum(p*x*x for p,x in zip(weights,values))
    log_second=(numerator_second-(beta*mean)**2)/beta
    claimed=var if mutant=='omit-pressure-beta' else beta*var
    require(log_second==claimed,'pressure','normalization factor')
    # Exact telescoping bound for two adaptive report laws.
    P={(0,0):F(3,8),(0,1):F(1,8),(1,0):F(1,8),(1,1):F(3,8)}
    Q={(0,0):F(2,5)*F(2,3),(0,1):F(2,5)*F(1,3),
       (1,0):F(3,5)*F(1,3),(1,1):F(3,5)*F(2,3)}
    tv=sum(abs(P[h]-Q[h]) for h in P)/2
    budget=F(1,10)+F(1,2)*abs(F(3,4)-F(2,3))+F(1,2)*abs(F(1,4)-F(1,3))
    require(tv<=budget,'path-comparison','predictable budget')

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant',choices=['omit-jacobian-q0','omit-pressure-beta'])
    args=parser.parse_args()
    structural_checks()
    exact_diagnostics(args.mutant)
    print(json.dumps({'status':'passed','checks':CHECKS,'total':sum(CHECKS.values()),
          'scope':'finite diagnostics and source consistency; not formal proof verification'},
          indent=2,sort_keys=True))

if __name__=='__main__':
    main()
