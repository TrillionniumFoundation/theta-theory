#!/usr/bin/env python3
"""Finite diagnostics for A2 v102; these checks are not universal proofs."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sympy as sp
import mpmath as mp


def exact_checks() -> dict:
    results = {}
    ranks = []
    for k in range(1, 9):
        basis = [sp.eye(k)[:, i] for i in range(k)]
        probes = basis + [basis[i] + basis[j] for i in range(k) for j in range(i+1, k)]
        entries = [(i, j) for i in range(k) for j in range(i, k)]
        A = sp.Matrix([[v[i]*v[j]*(1 if i == j else 2) for i, j in entries] for v in probes])
        assert A.rank() == k*(k+1)//2
        assert A[:-1, :].rank() == k*(k+1)//2-1
        ranks.append({'k': k, 'full_rank': A.rank(), 'one_probe_removed_rank': A[:-1, :].rank()})
    results['probe_ranks'] = ranks
    Qplus = sp.Matrix([[1, sp.Rational(1,4)], [sp.Rational(1,4), 1]])
    Qminus = sp.Matrix([[1, -sp.Rational(1,4)], [-sp.Rational(1,4), 1]])
    assert Qplus.is_positive_definite and Qminus.is_positive_definite
    assert list(Qplus.diagonal()) == list(Qminus.diagonal())
    assert (sp.ones(2,1).T * Qplus * sp.ones(2,1))[0] != (sp.ones(2,1).T * Qminus * sp.ones(2,1))[0]
    results['indistinguishable_diagonal_probes'] = 'passed; mixed ray distinguishes'
    x, z, b = sp.symbols('x z b', real=True)
    assert sp.expand(x*x + 2*b*x*(-b*x)+(-b*x)**2 - (1-b*b)*x*x) == 0
    results['endpoint_active_face'] = {'b_nonnegative': 'G(x)=x^2 for x>=0', 'b_negative': 'G(x)=(1-b^2)x^2 for x>=0'}
    for m in range(1, 5):
        for n in range(m+1, m+7):
            B = sp.cancel((x**n-z**n)/(x**m-z**m))
            assert sp.cancel(x**n-z**n-(x**m-z**m)*B) == 0
            assert sp.simplify(sp.limit(B, x, z) - sp.Rational(n,m)*z**(n-m)) == 0
    results['divided_difference_identities'] = 24
    a, c = sp.symbols('a c')
    assert sp.expand((-b*z**2+c*z**5)*z**3+b*z**5) == c*z**8
    assert sp.expand((-b*z**2)*z**3+b*z**5) == 0
    results['moving_wall_cancellation'] = 'm=2,n=3,q=5; exact wall and order 4 opening verified'
    h11,h12,h22,u = sp.symbols('h11 h12 h22 u', nonzero=True)
    expr = h11*u*u+2*h12*u*c+h22*c*c
    assert sp.simplify(expr.subs(u,-h12*c/h11)-c*c*(h22-h12*h12/h11)) == 0
    results['metric_schur_complement'] = 'passed'
    P0=sp.Matrix([sp.Rational(1,3)]*3)
    A=sp.Matrix([1,-1,0])/20
    B=sp.Matrix([1,0,-1])/20
    W=sp.diag(*[1/q for q in P0])
    fisher=sp.Matrix.hstack(A,B).T*W*sp.Matrix.hstack(A,B)/4
    assert fisher == sp.Matrix([[sp.Rational(3,800),sp.Rational(3,1600)], [sp.Rational(3,1600),sp.Rational(3,800)]])
    kappa2=sp.simplify(fisher[1,1]-fisher[0,1]**2/fisher[0,0])
    assert kappa2 == sp.Rational(9,3200)
    # On 0<=x,s<=1/4 and |a_i|<=1, the coordinate perturbation is <1/30.
    upper=sp.Rational(1,20)*(sp.Rational(1,4)**2+sp.Rational(1,4)**3+sp.Rational(1,4)**5)
    assert upper < sp.Rational(1,30)
    results['positive_probability_example'] = {'H0': str(fisher), 'kappa_squared': str(kappa2), 'probability_lower_bound': '1/3-1/30 > 0'}
    return results


def numerical_checks() -> list:
    mp.mp.dps=80
    H=(mp.mpf(2),mp.mpf('0.7'),mp.mpf(3))
    kappa=mp.sqrt(H[2]-H[1]**2/H[0])
    records=[]
    # Optimize in U/C coordinates, not x, to avoid losing tiny cancellation gaps.
    for delta in [mp.mpf('1e-3'),mp.mpf('1e-5'),mp.mpf('1e-7')]:
        z=mp.sqrt(delta)
        for tag,a1,a2 in [('generic',mp.mpf('0.4'),mp.mpf('0.8')),
                           ('crossover',-mp.mpf('0.7')*delta,mp.mpf('0.8')),
                           ('high_cancellation',-mp.mpf('0.8')*delta+mp.mpf('0.3')*delta**mp.mpf('2.5'),mp.mpf('0.8'))]:
            C=a1*z**3+a2*z**5
            assert C != 0
            def normalized_sq(v):
                xp=mp.sqrt(delta+v*C)
                G=(a1*xp**3+a2*xp**5)/C
                return H[0]*v*v+2*H[1]*v*G+H[2]*G*G
            v0=-H[1]/H[0]
            vstar=mp.findroot(lambda v: mp.diff(normalized_sq,v),(v0-mp.mpf('.1'),v0+mp.mpf('.1')))
            ratio=mp.sqrt(normalized_sq(vstar))/kappa
            assert abs(ratio-1) < 20*z
            # This local stationary check is not a certified global root isolation.
            records.append({'delta': str(delta), 'case': tag, 'distance_over_predicted': mp.nstr(ratio,22), 'normalized_stationary_point': mp.nstr(vstar,22)})
    return records


def binary_score_checks() -> list:
    """Exact score profiling in simple, repeated, and mixed endpoint patterns."""
    z=sp.symbols('z')
    alpha=sp.Rational(2,5)
    U=sp.Matrix([[sp.Rational(2,3),sp.Rational(1,4)],[sp.Rational(1,3),sp.Rational(3,4)]])
    V=sp.Matrix([[sp.Rational(3,4),sp.Rational(1,5)],[sp.Rational(1,4),sp.Rational(4,5)]])
    u=[U[:,i] for i in range(2)];v=[V[:,i] for i in range(2)]
    weights=[alpha,1-alpha]
    R=sp.Rational
    cases=[('linear_simple', [[(R(1,3),1)],[(R(2,3),1)]],False),
           ('interior_repeated', [[(R(1,3),2)],[(R(2,3),2)]],True),
           ('mixed_endpoint_repeated', [[(R(0),1),(R(1,3),2)],[(R(2,3),3)]],True)]
    records=[]
    for name,clusters,repeated in cases:
        f=[sp.prod((z-r)**m for r,m in ca) for ca in clusters]
        degree=int(sp.degree(f[0],z));ell=2*degree+1
        clocks=list(range(2,2+ell))
        K=sum((weights[a]*f[a]*u[a]*v[a].T for a in range(2)),sp.zeros(2))
        q=sp.expand(weights[0]*f[0]+weights[1]*f[1])
        probs=[K.subs(z,T)/q.subs(z,T) for T in clocks]
        def col(dK,dq):
            values=[]
            for T,P in zip(clocks,probs):
                S=(dK.subs(z,T)-P*sp.sympify(dq).subs(z,T))/q.subs(z,T)
                values.extend(list(S))
            return sp.Matrix(values)
        free=[];retained=[]
        for a in range(2):
            for r,m in clusters[a]:
                p=sp.cancel(-f[a]/(z-r))
                score=col(weights[a]*p*u[a]*v[a].T,weights[a]*p)
                (free if repeated and 0<r<1 else retained).append(score)
                if repeated and 0<r<1 and m>=2:
                    p=sp.cancel(-f[a]/(z-r)**2)
                    retained.append(col(weights[a]*p*u[a]*v[a].T,weights[a]*p))
        free.append(col(f[0]*u[0]*v[0].T-f[1]*u[1]*v[1].T,f[0]-f[1]))
        direction=sp.Matrix([1,-1])
        for a in range(2):
            free.append(col(weights[a]*f[a]*direction*v[a].T,0))
        for a in range(2):
            free.append(col(weights[a]*f[a]*u[a]*direction.T,0))
        L=sp.Matrix.hstack(*free);D=sp.Matrix.hstack(*retained)
        W=sp.diag(*[1/(ell*p) for P in probs for p in P])
        gram=L.T*W*L
        Q=D.T*W*D-D.T*W*L*gram.inv()*L.T*W*D
        assert gram.det()>0
        for j in range(1,Q.rows+1):
            assert Q[:j,:j].det()>0
        probe=sp.ones(Q.rows,1)
        astar=-gram.inv()*L.T*W*D*probe
        residual=L*astar+D*probe
        assert sp.simplify((residual.T*W*residual)[0]-(probe.T*Q*probe)[0])==0
        assert L.row_join(D).rank()==L.cols+D.cols
        records.append({'case':name,'degree':degree,'free_columns':L.cols,'retained_columns':D.cols,
                        'combined_rank':L.cols+D.cols,'profile_positive_definite':True,
                        'all_ones_probe_cost':str((probe.T*Q*probe)[0])})
    return records


def main() -> None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    record={'status':'finite_diagnostics_passed','exact':exact_checks(),'binary_score_checks':binary_score_checks(),'numerical_local_stationary_checks':numerical_checks(),
            'scope':'Finite exact identities and 80-digit local stationary checks. Not a proof of universal theorems, adaptive complexity, or a certified global numerical minimum.',
            'sympy_version':sp.__version__,'mpmath_version':mp.__version__,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(record,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text)


if __name__=='__main__':
    main()
