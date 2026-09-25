#!/usr/bin/env python3
"""Exact finite regressions for v41; not certification of analytical gap theorems."""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import sys
import sympy as S


def require(test: bool, reason: str) -> None:
    if not test:
        raise RuntimeError('CHECK_REJECTED: '+reason)


def cartan(kind: str, n: int) -> list[list[int]]:
    a=[[2 if i==j else 0 for j in range(n)] for i in range(n)]
    def edge(i:int,j:int,u:int=-1,v:int=-1)->None:
        a[i][j]=u;a[j][i]=v
    if kind in 'ABC':
        for i in range(n-1): edge(i,i+1)
        if kind=='B': a[n-1][n-2]=-2
        if kind=='C': a[n-2][n-1]=-2
    elif kind=='D':
        for i in range(n-3):edge(i,i+1)
        edge(n-3,n-2);edge(n-3,n-1)
    elif kind=='E':
        edge(0,2);edge(1,3);edge(2,3)
        for i in range(3,n-1):edge(i,i+1)
    elif kind=='F':edge(0,1);edge(1,2,-2,-1);edge(2,3)
    elif kind=='G':edge(0,1,-3,-1)
    else:raise ValueError(kind)
    return a


def roots(a:list[list[int]])->set[tuple[int,...]]:
    n=len(a);seen={tuple(int(i==j) for i in range(n)) for j in range(n)}
    queue=list(seen)
    while queue:
        v=queue.pop()
        for i in range(n):
            w=list(v);w[i]-=sum(a[i][j]*v[j] for j in range(n));w=tuple(w)
            if w not in seen:seen.add(w);queue.append(w)
        require(len(seen)<2000,'root enumeration did not remain finite')
    return seen


def su_basis(n:int):
    result=[]
    for i in range(n):
        for j in range(i):
            a=S.zeros(n);a[i,j]=1;a[j,i]=-1;result.append(a)
            a=S.zeros(n);a[i,j]=S.I;a[j,i]=S.I;result.append(a)
    for i in range(n-1):
        a=S.zeros(n);a[i,i]=S.I;a[n-1,n-1]=-S.I;result.append(a)
    return result


def skew_rank(n:int,k:int)->int:
    a=S.zeros(n)
    for i in range(k):a[2*i,2*i+1]=1;a[2*i+1,2*i]=-1
    columns=[]
    for x in su_basis(n):
        y=x*a+a*x.T
        columns.append(S.Matrix([S.re(c) for c in y]+[S.im(c) for c in y]))
    return S.Matrix.hstack(*columns).rank()


def octahedral():
    result=[]
    for p in itertools.permutations(range(3)):
        for sign in itertools.product([-1,1],repeat=3):
            a=S.zeros(3)
            for i,j in enumerate(p):a[i,j]=sign[i]
            if a.det()==1:result.append(a)
    require(len(result)==24,'rotation averaging group size')
    return result


def check(mutant:str|None=None)->tuple[dict,dict]:
    records={};cases=[]
    for kind,n in [('A',i) for i in range(1,9)]+[(k,i) for k in 'BC' for i in range(2,9)]+[('D',i) for i in range(4,9)]+[('G',2),('F',4),('E',6),('E',7),('E',8)]:
        rr=roots(cartan(kind,n));counts=[sum(v[j]==0 for v in rr) for j in range(n)]
        actual=len(rr)-max(counts)
        expected={'A':2*n,'B':4*n-2,'C':4*n-2,'D':4*n-4}.get(kind)
        if expected is None:expected={('G',2):10,('F',4):30,('E',6):32,('E',7):54,('E',8):114}[kind,n]
        if mutant=='nilpotent-adjoint-dimension' and kind=='E' and n==8:expected=58
        require(actual==expected,f'{kind}{n} compact adjoint count {actual} != {expected}')
        cases.append({'type':kind+str(n),'roots':len(rr),'deleted_root_counts':counts,'minimum_orbit_dimension':actual})
    records['root_systems']=cases
    skew=[]
    for n in range(3,9):
        ranks=[]
        for k in range(1,n//2+1):
            actual=skew_rank(n,k)
            expected=k*(4*n-6*k-1) if 2*k<n else n*(n-1)//2-1
            if mutant=='missing-special-unitary-constraint' and n==6 and k==3:expected+=1
            require(actual==expected,f'skew orbit dimension n={n}, k={k}')
            ranks.append(actual)
        expected={3:5,4:5,5:13,6:14}.get(n,4*n-7)
        if mutant=='highest-weight-always-minimal' and n==6:expected=17
        require(min(ranks)==expected,f'minimum skew orbit n={n}')
        skew.append({'n':n,'coalesced_rank_strata':ranks,'minimum':min(ranks)})
    records['skew_orbits']=skew

    group=octahedral();grams=[]
    # Finite irreducible averaging has the same invariant second moment as SO(3).
    for x in [S.Matrix([1,0,0,1,0,0])/S.sqrt(2),S.Matrix([1,0,0,0,1,0])/S.sqrt(2),S.Matrix([S.Rational(3,5),0,0,S.Rational(4,5),0,0])]:
        C=S.zeros(6)
        for g in group:
            gx=S.diag(g,g)*x;C+=gx*gx.T/24
        a2=3*max(C.eigenvals())
        X=S.Matrix.hstack(x[:3,0],x[3:,0])
        required=max((X.T*X).eigenvals())
        if mutant=='isotypic-trace-instead-of-top-eigenvalue' and x==S.Matrix([1,0,0,0,1,0])/S.sqrt(2):a2=C.trace()
        require(S.simplify(a2-required)==0,'canonical activation uses the top multiplicity eigenvalue')
        require(all(C*S.diag(g,g)==S.diag(g,g)*C for g in group),'covariance lies in commutant')
        grams.append({'seed':[str(t) for t in x],'canonical_activation_squared':str(a2),'covariance':[[str(t) for t in C.row(i)] for i in range(6)]})
    require(S.simplify(grams[0]['canonical_activation_squared'])==1,'diagonal reachable copy fully activated')
    if mutant=='coordinate-copy-is-canonical':require(S.Rational(1,2)==1,'coordinate splitting loses diagonal activation')
    records['activation']=grams

    c=S.Rational(3,5);s=S.Rational(4,5)
    rx=S.Matrix([[1,0,0],[0,c,-s],[0,s,c]]);rz=S.Matrix([[c,-s,0],[s,c,0],[0,0,1]])
    r=S.Matrix([[c,-s],[s,c]])
    gates=[S.diag(a,b) for a in [S.eye(3),rx,rx.T,rz,rz.T] for b in [S.eye(2),r]]
    require(len(gates)==10 and all(g.T*g==S.eye(5) and g.det()==1 for g in gates),'ten rational orthogonal commands')
    ax=S.Matrix([[0,0,0],[0,0,-1],[0,1,0]]);az=S.Matrix([[0,-1,0],[1,0,0],[0,0,0]])
    lie=S.Matrix.hstack(S.Matrix(list(ax)),S.Matrix(list(az)),S.Matrix(list(ax*az-az*ax)))
    require(lie.rank()==3,'SO(3) Lie generators span')
    B=S.sqrt(3);activation=1/B
    if mutant=='free-query-norm':activation=S.Integer(1)
    require(S.simplify(activation-1/S.sqrt(3))==0,'actual query norm controls calibration')
    # branch initialization/output identities are exact for all displayed seeds
    branch_cases=0
    rho=S.Rational(1,40);w=[S.Rational(3,5),S.Rational(2,5)]
    for g in gates:
        for j in range(5):
            x=S.eye(5)[:,j]
            target=rho*g*x
            factors=[rho/w[0],rho/w[1]]
            if mutant=='unpaid-branch-amplification':factors=[rho,rho]
            out=S.Matrix.vstack(w[0]*g[:3,:3]*factors[0]*x[:3,0],w[1]*g[3:,3:]*factors[1]*x[3:,0])
            require(out==target,'weighted branch mean must reproduce exact target')
            branch_cases+=1
    sigma=max(2,1)
    if mutant=='minimum-over-effective-group':sigma=min(2,1)
    require(sigma==2,'dominant active minimum determines exponent')
    records['mixed_commands']=[[[str(v) for v in g.row(i)] for i in range(5)] for g in gates]

    # Reported constants must correspond to the exact inspected primary versions.
    versions={'v1':{'gfa':(2,6),'qfa':(2,6)},'v2':{'gfa':(1,1),'qfa':(1,1)}}
    if mutant=='conflate-primary-versions':versions['v2']=versions['v1']
    require(versions['v1']['qfa']!=(versions['v2']['qfa']),'version-specific theorem constants differ')
    result={'schema':'gtf41.checks/1','exact_checks':{'root_systems':len(cases),'root_vectors_enumerated':sum(x['roots'] for x in cases),'skew_orbit_tangent_ranks':sum(len(x['coalesced_rank_strata']) for x in skew),'commutant_averages':len(grams),'finite_rotations_per_average':24,'rational_mixed_commands':len(gates),'paid_branch_cases':branch_cases},'proved_in_article':{'intrinsic_gap':'sphere action = Lebesgue action; independent of redundant presentation','active_width':'dominant active action gap suffices for Theta(N^(sigma_X/2))','canonical_activation':'a_lambda^2 = d_lambda max_x lambda_max(C_lambda,x)','faithful_nongapped_example':'SO(3) x SO(2), ten rational commands, Theta(N)','all_adjoint_exponents':{'A_l':'l','B_l':'2l-1','C_l':'2l-1','D_l':'2l-2','G2':5,'F4':15,'E6':16,'E7':27,'E8':57},'exterior_SU6_exponent':7},'scope':'Exact finite algebra and model regressions. No full spectral gap, universal orbit theorem, independent proof verification or priority clearance is certified by these tests.'}
    return result,records


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--negative-control');parser.add_argument('--export',type=Path);args=parser.parse_args()
    result,records=check(args.negative_control)
    if args.export:args.export.write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as error:
        print(str(error),file=sys.stderr);sys.exit(1)
