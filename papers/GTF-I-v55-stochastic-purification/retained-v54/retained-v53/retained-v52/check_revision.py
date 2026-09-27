"""Exact v52 finite regressions. Universal claims are proved in the manuscript."""
from __future__ import annotations
import itertools
import json
import math
from fractions import Fraction as F
from typing import Callable
import sympy as s
from certificate_verifier import check_sos, local_linear_system, require


def horizon_certificate(rho: F, n: int, degree: int = 20) -> bool:
    require(0 < rho < 1 and isinstance(n, int) and n >= 0, 'signal/horizon domain')
    require(1 <= degree <= 100, 'Taylor degree domain')
    x = rho**3 / 1024
    lower_log = n*x/(1+x)
    lower_exp = sum(lower_log**j/math.factorial(j) for j in range(degree+1))
    return lower_exp > 6/rho**3


def main() -> None:
    negatives: list[str] = []
    checks: dict[str, object] = {}
    def reject(name: str, f: Callable[[], object]) -> None:
        try:
            f()
        except ValueError:
            negatives.append(name)
        else:
            raise RuntimeError('negative control accepted: '+name)

    rho = F(1,10)
    n0 = 9*1024001
    require(n0 == 9216009 and horizon_certificate(rho,n0), 'effective horizon certificate')
    require(not horizon_certificate(rho,0), 'zero horizon incorrectly certified')
    require(F(72,2**22) <= F(1,32768), 'conditioned dilation constant')
    require(F(1,864) > F(1,1024), 'rational beta weakening')
    z=s.symbols('z', nonnegative=True)
    require(s.expand((1+4*z)-(1+2*z)*(1+z)) == z-2*z*z, 'noisy quotient identity')
    checks['effective_constants']={'rho':'1/10','sufficient_N':n0,
        'Taylor_degree':20,'beta3_coefficient_lower':'1/1024',
        'conditioned_TV_bound':'rho^4/(2^23*A)',
        'unconditional_noise_search_executed':False}
    reject('invalid_signal',lambda:horizon_certificate(F(0),n0))
    reject('negative_horizon',lambda:horizon_certificate(rho,-1))
    reject('unbounded_Taylor_request',lambda:horizon_certificate(rho,n0,1000))
    reject('zero_horizon_claim',lambda:require(horizon_certificate(rho,0),'not certified'))

    # Equality in the trace lemma for a centered simplex, with no numeric eigenvalues.
    for d in (2,3,4):
        m=d+1
        Z=s.eye(d).col_join(-s.ones(1,d))
        T=(s.ones(m)-s.eye(m))/d
        require(T*s.ones(m,1)==s.ones(m,1) and T*Z==-Z/d,'simplex antipodal extension')
        require(s.trace(T)==0 and m-d-s.Rational(d,d)==0,'trace equality')
        require(s.ones(m,1).row_join(Z).rank()==d+1,'affine independence')
    reject('central_case_strict_gap',lambda:require(3+3<2*3,'strict trace gap requires k<2D'))
    checks['trace_mechanism']={'simplex_dimensions':[2,3,4],'exact_equalities':True}

    # Height separation, fixed-axis obstruction and rational reflection.
    R=s.Matrix([[3,-4],[4,3]])/5
    Fm=s.diag(1,-1)
    require(R.T*R==s.eye(2) and Fm*R*Fm==R.inv() and Fm*R!=R*Fm,'rational group')
    pairchecks=0
    for k in range(1,9):
        points=[R**j*s.Matrix([1,0]) for j in range(2*k)]
        for u,v in itertools.combinations(points,2):
            require((u-v).dot(u-v)>=s.Rational(1,5)**(4*k),'height separation')
            pairchecks+=1
    R3=s.diag(R,s.ones(1));P=s.diag(1,1,0);axis=s.Matrix([0,0,1])
    require(R3*axis==axis and P*R3==R3*P,'moving-subspace reduction')
    require(s.trace(P)==2 and sum((P*s.eye(3)[:,i]).dot(P*s.eye(3)[:,i]) for i in range(3))==2,
            'projection calibration identity')
    checks['word_height']={'denominator':5,'K_values':list(range(1,9)),
                         'exact_pair_checks':pairchecks,'fixed_axis_removed':True}
    reject('fixed_axis_has_positive_distortion',lambda:require((R3*axis-axis).dot(R3*axis-axis)>0,'fixed axis'))
    reject('closed_noise_boundary',lambda:require(rho/3-2*(rho/6)>0,'strict calibration'))
    reject('nonorthogonal_command',lambda:require((2*R).T*(2*R)==s.eye(2),'orthogonality'))

    # Explicit range-invariance row in the complete local system.
    P2=s.diag(1,0); Z=s.zeros(2,1);Q=P2;Y=Z;U=s.eye(1)
    B,b=local_linear_system(P2,Z,Q,Y,U)
    swap=s.Matrix([[0,1],[1,0]])
    v=s.Matrix(list(swap))
    require(B.shape==(2+4+2,4) and b.shape==(8,1),'dual dimensions')
    require(swap*s.ones(2,1)==s.ones(2,1) and P2*(swap*Y-Z*U.T)==s.zeros(2,1),'weak equations pass')
    require(B*v!=b,'omitted-range counterexample absent')
    reject('omit_range_accepts_swap',lambda:require(B*v==b,'range invariance fails'))
    checks['complete_local_equations']={'rows':8,'columns':4,'range_omission_counterexample':True}

    x=s.symbols('x');zero=([],s.zeros(0));good=([s.Integer(1),x,x*x],s.diag(0,2,1))
    terms=[good,zero,zero]
    check_sos((x*x+1)**2,s.Rational(1),[x],[(-1,1)],terms)
    reject('SOS_identity_mutation',lambda:check_sos((x*x+1)**2+x,s.Rational(1),[x],[(-1,1)],terms))
    reject('SOS_negative_eigenvalue',lambda:check_sos((x*x+1)**2,s.Rational(1),[x],[(-1,1)],
                [([s.Integer(1),x,x*x],s.diag(0,-2,1)),zero,zero]))
    reject('SOS_float_margin',lambda:check_sos((x*x+1)**2,1.0,[x],[(-1,1)],terms))
    reject('SOS_zero_margin',lambda:check_sos((x*x+1)**2,s.Rational(0),[x],[(-1,1)],terms))
    reject('SOS_missing_generator',lambda:check_sos((x*x+1)**2,s.Rational(1),[x],[(-1,1)],terms[:2]))
    reject('SOS_nonrational_Gram',lambda:check_sos((x*x+1)**2,s.Rational(1),[x],[(-1,1)],
                [([s.Integer(1),x,x*x],s.diag(0,2.0,1)),zero,zero]))
    reject('SOS_undeclared_symbol',lambda:check_sos((x*x+1)**2+s.Symbol('y'),s.Rational(1),[x],[(-1,1)],terms))
    reject('SOS_bad_interval',lambda:check_sos((x*x+1)**2,s.Rational(1),[x],[(1,-1)],terms))
    checks['exact_SOS_certificate']={'q':'(x^2+1)^2','lambda':'1','Gram_diagonal':[0,2,1],
         'search_engine_implemented':False,'certificate_scope':'supplied rational identities'}

    # Exact fair-bit rejection probabilities; no pseudorandom simulation is used.
    compiler_cases=0
    for q in range(2,65):
        ell=(q-1).bit_length()
        require(F(q,2**ell)>F(1,2),'acceptance probability')
        require(F(ell*2**ell,q)<2*ell,'expected fair bits')
        for p in range(1,q):
            require(F(sum(y<p for y in range(q)),q)==F(p,q),'conditional Bernoulli law')
            compiler_cases+=1
    require(F(sum(y%5<3 for y in range(8)),8)!=F(3,5),'biased modulo negative control')
    reject('biased_modulo_sampler',lambda:require(F(sum(y%5<3 for y in range(8)),8)==F(3,5),'modulo is biased'))
    checks['uniform_rational_sampling']={'exact_probability_cases':compiler_cases,'max_denominator':64}

    print(json.dumps({'schema':'gtf52.exact-regressions/1','status':'success','checks':checks,
        'negative_controls_detected':negatives,
        'scope':'Finite exact arithmetic and supplied-certificate regressions, not a proof by sampling of Haar compactness, noisy rigidity, or universal asymmetry.'},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
