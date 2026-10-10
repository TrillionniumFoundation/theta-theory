#!/usr/bin/env python3
"""Finite arithmetic regression tests; no continuum or spectral certificate."""
from fractions import Fraction as F
from itertools import product
import sympy as S

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def rejected(fn):
    try:
        fn()
    except RuntimeError:
        return True
    raise RuntimeError('negative control was not rejected')

def finite_checks():
    p, q, v, gamma, zeta = F(1,12), F(1,24), F(1,8), F(1,100), F(1,4)
    require(0<q<p<F(1,6), 'test exponents')
    require(v<1-F(2,3), 'Jacobian summability')
    require(gamma<min(v,p-q,F(1,3)-q,1-q), 'unstable errors')
    require(max(p,gamma/(1-gamma))<zeta<F(1,2), 'multiplier closure')
    require(v-q>0, 'trimmed test error')
    cases=0; sheet_cases=0
    for prime in (2,3,5):
        vec=list(product(range(prime),repeat=2))
        for a0,a1,c in product(range(prime),repeat=3):
            if (a0,a1,c)==(0,0,0):
                continue
            if c==0:
                residues=[(a0*l0+a1*l1)%prime for l0,l1 in vec]
                require(all(residues.count(r)==prime for r in range(prime)), 'nonzero sheet character')
                sheet_cases+=1
            else:
                require(c%prime!=0, 'nontrivial eigenvalue')
            for l0,l1 in vec:
                for k0,k1 in vec:
                    h=(l1,k0,c)
                    chi=a0*h[0]+a1*h[1]+c*h[2]
                    chi_next=a0*(h[0]+k0)+a1*(h[1]+k1)+c*(h[2]+1)
                    old=a0*l0+a1*l1-chi
                    new=a0*(l0+k0)+a1*(l1+k1)-chi_next
                    require((new-old+c)%prime==0, 'space-count cover eigenphase')
                    cases+=1
    # Algebra of the preceding ellipse entry root, not an orbit enumeration.
    A,B,C=S.symbols('A B C',positive=True)
    root=(-B-S.sqrt(B**2-A*C))/A
    require(S.simplify(A*root**2+2*B*root+C)==0, 'quadratic entry identity')
    r,area,tau=S.symbols('r area tau',positive=True)
    require(S.simplify(S.pi*area/(2*S.pi*r)-area/(2*r))==0, 'circular mean roof')
    require(1-2*F(47,100)==F(3,50), 'ellipse gap')
    area_lower=F(17,20)-F(22,7)*F(47,100)**2
    require(area_lower>0, 'positive free area via sqrt(3)>1.7 and pi<22/7')
    lo=F(9,20)**2/F(47,100)**3
    hi=F(47,100)**2/F(9,20)**3
    require(0<lo<hi, 'curvature envelope')
    # Clock determinant and Gaussian quadratic form at exact rational matrices.
    Sigma=S.Matrix([[3,1,0],[1,4,1],[0,1,5]])
    clock_cases=0
    for t in (S.Rational(1,5),S.Rational(2,7),S.Rational(3,4)):
        D=S.diag(1,1,-1/t);V=D*Sigma*D.T/t
        require(S.simplify(V.det()-Sigma.det()/t**5)==0, 'clock determinant')
        x=S.Matrix([1,-2,3]);z=S.sqrt(t)*S.diag(1,1,-t)*x
        require(S.simplify((x.T*V.inv()*x-z.T*Sigma.inv()*z)[0])==0, 'Gaussian exponent')
        clock_cases+=1
    # A finite model checks the order of equivalent-norm choices only.
    norm_cases=0
    for band in (1,2,8,32):
        CB=F(3*band+1);theta=F(3,4);N=1
        while CB*(theta**N+F(4,5)**N)>=F(1,4) or CB*F(9,10)**N>=F(1,4):
            N+=1
        cB=F(1,8)/(CB*3**N)
        require(CB*(theta**N+F(4,5)**N)+cB*CB*3**N<F(1,2), 'stable absorption')
        require(CB*F(9,10)**N<F(1,4), 'unstable leading factor')
        norm_cases+=1
    negative=0
    negative+=rejected(lambda:require(F(1,10)<p-q,'wrong unstable exponent'))
    negative+=rejected(lambda:require(F(1,2)<F(1,2),'forbidden Holder endpoint'))
    negative+=rejected(lambda:require(S.Rational(1,4)**-3==S.Rational(1,4)**-5,'missing clock determinant'))
    negative+=rejected(lambda:require((-1)%3==0,'collision step omitted from character'))
    # The source topology condition is genuinely stronger than small open mass:
    # delta_(1/n) converges to delta_0, but an open union around 1/n avoiding 0
    # has zero limiting open mass while its closure has limiting mass one.
    return {'cover_phase_cases':cases,'zero_mean_sheet_characters':sheet_cases,
        'exact_quadratic_root_checked':True,'clock_matrix_cases':clock_cases,
        'equivalent_norm_cases':norm_cases,'negative_controls':negative,
        'exponents':{'p':str(p),'q':str(q),'varsigma':str(v),'gamma':str(gamma),'zeta':str(zeta)},
        'ellipse_gap':str(F(3,50)),'free_area_rational_lower_bound':str(area_lower),
        'curvature_envelope':[str(lo),str(hi)],
        'continuum_partition_verified_by_tests':False,'mixing_verified_by_tests':False,
        'operator_spectrum_verified_by_tests':False,'full_raw_return_LLT_verified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
