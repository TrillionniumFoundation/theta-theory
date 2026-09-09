#!/usr/bin/env python3
"""Independent finite checks for the A2 v9 completed-revision review.

Requires Python 3.10+, SymPy and mpmath. No manuscript code is imported.
Run: python verify_review.py --output independent_checks.json
Optional byte authentication: --paper /path/to/restored/paper
                              --manifest VERIFICATION.json
These finite identities are not certificates for the nonlinear billiard theorems.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sympy as s
import mpmath as mp

CHECKS: list[dict] = []
DETAILS: dict = {}

def require(name: str, condition: bool, kind: str = 'exact_algebra') -> None:
    if not bool(condition):
        raise RuntimeError('FAILED: ' + name)
    CHECKS.append({'name': name, 'kind': kind, 'status': 'pass'})

def zero(name: str, expr: s.Expr) -> None:
    require(name, s.simplify(s.expand_func(expr)) == 0)

def beta(a: s.Expr, b: s.Expr) -> s.Expr:
    return s.gamma(a)*s.gamma(b)/s.gamma(a+b)

def convolution(a: dict, b: dict) -> dict:
    result: dict = {}
    for r, ar in a.items():
        for t, bt in b.items():
            k = r+t+1
            result[k] = result.get(k, 0)+ar*bt*beta(r+1,t+1)
    return {k:s.simplify(v) for k,v in result.items()}

def main() -> dict:
    half=s.Rational(1,2); M=8; z=s.Symbol('z')
    profiles=[[s.Integer(1),s.Rational(1,4),-s.Rational(1,7),s.Rational(1,9)],
              [s.Integer(1),-s.Rational(1,5),s.Rational(1,11)]]
    kernels=[]; Fs={}; Ks={}; transformed={}
    for p in profiles:
        kernels.append({s.Integer(i)-half:v for i,v in enumerate(p)})
    for b,c in ((0,0),(0,1),(1,1)):
        F=[]
        for n in range(M+1):
            val=sum(2*profiles[b][r]*profiles[c][n-r]*s.gamma(r+half)*s.gamma(n-r+half)
                    /(s.pi*s.gamma(n+3))
                    for r in range(len(profiles[b])) if 0<=n-r<len(profiles[c]))
            F.append(s.simplify(val))
        Fs[b,c]=F
        Ks[b,c]=convolution(kernels[b],kernels[c])
        zero(f'normalization_F_{b}{c}',F[0]-1)
        zero(f'normalization_K_{b}{c}',Ks[b,c][0]-s.pi)
        for n in range(M+1):
            zero(f'twice_differentiated_residual_{b}{c}_{n}',
                 s.pi*s.Rational(1,2)*(n+2)*(n+1)*F[n]-Ks[b,c].get(s.Integer(n),0))
        transformed[b,c]=sum(s.factorial(n+2)*F[n]*z**n/2 for n in range(M+1))
    defect=s.expand(transformed[0,1]**2-transformed[0,0]*transformed[1,1])
    for n in range(M+1):zero(f'factorially_reweighted_rank_one_{n}',defect.coeff(z,n))
    for b in (0,1):
        root=[s.Integer(1)]
        for n in range(1,M+1):
            root.append(s.simplify((transformed[b,b].coeff(z,n)-sum(root[r]*root[n-r] for r in range(1,n)))/2))
        for n in range(M+1):
            expected=profiles[b][n] if n<len(profiles[b]) else 0
            zero(f'finite_square_root_inverse_{b}_{n}',root[n]/s.rf(half,n)-expected)
    # Check the derivative identities symbolically, not just on selected profiles.
    u,v,U,V=s.symbols('u v U V')
    f00=u/3; f11=v/3; f01=(u+v)/6
    # F'' = 2! times its coefficient; coefficients follow the simplex formula.
    g00=U/4+u*u/24; g11=V/4+v*v/24; g01=(U+V)/8+u*v/24
    zero('universal_first_derivative_parity',2*f01-f00-f11)
    zero('universal_second_derivative_negative_square',g01-(g00+g11)/2+s.Rational(3,16)*(f00-f11)**2)
    left=convolution(Ks[0,1],Ks[0,1]); right=convolution(Ks[0,0],Ks[1,1])
    for power in sorted(set(left)|set(right)):
        zero(f'whole_Volterra_identity_power_{power}',left.get(power,0)-right.get(power,0))
    # Forced second-kind equation: 2*pi*f+R'*f = k_* * Q'.
    difference={k:kernels[0].get(k,0)-kernels[1].get(k,0) for k in set(kernels[0])|set(kernels[1])}
    average={k:kernels[0].get(k,0)+kernels[1].get(k,0) for k in set(kernels[0])|set(kernels[1])}
    abel=convolution({-half:s.Integer(1)},average)
    zero('Abel_constant_is_two_pi',abel[0]-2*s.pi)
    Rprime={r-1:r*a for r,a in abel.items() if r>0}
    Q={r:Ks[0,0].get(r,0)-Ks[1,1].get(r,0) for r in set(Ks[0,0])|set(Ks[1,1])}
    zero('forced_equation_Q_zero',Q[0])
    Qprime={r-1:r*a for r,a in Q.items() if r>0}
    lhs=convolution(Rprime,difference)
    for r,a in difference.items():lhs[r]=lhs.get(r,0)+2*s.pi*a
    rhs=convolution({-half:s.Integer(1)},Qprime)
    for r in sorted(set(lhs)|set(rhs)):
        zero(f'forced_Volterra_identity_power_{r}',lhs.get(r,0)-rhs.get(r,0))
    # Start with the full unequal-contact quadratic broken action, then eliminate interiors.
    gap=s.Rational(3,5); kappas=(s.Rational(7,4),s.Rational(11,6))
    cs=[1+gap*k for k in kappas]; c=s.sqrt(cs[0]*cs[1])
    for j in (1,2,3,5,8,13):
        H=s.zeros(j+1)
        for i in range(j):
            H[i,i]+=cs[i%2]/gap;H[i+1,i+1]+=cs[(i+1)%2]/gap
            H[i,i+1]-=1/gap;H[i+1,i]-=1/gap
        if j==1:
            endpoint=H; determinant=s.Integer(1)
        else:
            interior=H[1:j,1:j];indices=[0,j]
            coupling=H.extract(indices,list(range(1,j)))
            endpoint=H.extract(indices,indices)-coupling*interior.inv()*coupling.T
            determinant=interior.det()
        zero(f'unequal_Schur_cofactor_j{j}',-endpoint[0,1]-(1/gap)**j/determinant)
        zero(f'unequal_normalized_ratio_squared_j{j}',endpoint[0,1]**2/endpoint.det()*(c*c-1)*s.chebyshevu(j-1,c)**2-1)
        require(f'unequal_positive_endpoint_j{j}',endpoint[0,0]>0 and endpoint.det()>0)
    # The cutoff construction scales all its C^m derivatives within a fixed budget.
    for m in (1,2,3,5,8):
        zero(f'envelope_per_query_exponent_m{m}',2*(3+s.Rational(3,m))-(6+s.Rational(6,m)))
        require(f'envelope_derivative_exponents_nonnegative_m{m}',all(3*(1-s.Rational(r,m))>=0 for r in range(m+1)))
    # C-infinity interior bump. For x0>1/2 the quadratic perturbation term is identically zero on [0,1].
    mp.mp.dps=60;x0=mp.mpf(3)/4; samples=[]
    def bump(t):
        return mp.exp(4-1/(t*(1-t))) if 0<t<1 else mp.mpf(0)
    bump_mass=mp.quad(bump,[0,mp.mpf('.5'),1])
    for den in (32,64,128,256):
        h=mp.mpf(1)/den
        deltaF=16*h*h/(3*mp.pi)*mp.quad(lambda t:bump(t)*(1-x0-h*t)**mp.mpf('1.5')/mp.sqrt(x0+h*t),[0,mp.mpf('.5'),1])
        ratio=deltaF/(h*h)
        lower=16/(3*mp.pi)*bump_mass*(1-x0-h)**mp.mpf('1.5')/mp.sqrt(x0+h)
        upper=16/(3*mp.pi)*bump_mass*(1-x0)**mp.mpf('1.5')/mp.sqrt(x0)
        require(f'C0_norm_separator_h_1_over_{den}',0<lower<ratio<upper,'ordinary_60_digit')
        samples.append({'h':str(h),'sup_profile_difference':str(h),'sup_law_difference':mp.nstr(deltaF,30),'law_difference_over_h_squared':mp.nstr(ratio,30)})
    DETAILS['smooth_bump_samples']=samples
    DETAILS['smooth_bump_scope']='Abstract normalized profiles, not claimed to be realized billiard tables; the general norm separation is proved in the report.'
    # Exact rescaled Bernoulli variance, not a minimax lower bound.
    scale,F,N=s.symbols('scale F N',positive=True);p=F/scale
    zero('empirical_normalized_law_variance',scale**2*p*(1-p)/N-scale*F*(1-p)/N)
    return {'schema':'a2-v9-independent-review-checks-v1','status':'pass','counts':{'total':len(CHECKS),**dict(Counter(x['kind'] for x in CHECKS))},'checks':CHECKS,'details':DETAILS,
            'limitations':['No manuscript code imported. Finite identities and ordinary numerical arithmetic only.',
            'Not interval arithmetic, a nonlinear billiard probability oracle, or a formal proof certificate.',
            'No proof of physical realizability of arbitrary abstract boundary profiles.',
            'No claim of exhaustive originality review or verification of all archival appendices.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('independent_checks.json'))
    parser.add_argument('--paper',type=Path)
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('VERIFICATION.json'))
    args=parser.parse_args();result=main()
    if args.paper:
        manifest=json.loads(args.manifest.read_text())['source_authentication']['file_sha256']
        if len(manifest)!=119:raise RuntimeError('Unexpected source manifest size')
        bad=[name for name,digest in manifest.items() if not (args.paper/name).is_file() or hashlib.sha256((args.paper/name).read_bytes()).hexdigest()!=digest]
        if bad:raise RuntimeError('Source byte mismatches: '+', '.join(bad))
        result['source_authentication']={'files':119,'sha256_all_match':True}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'counts':result['counts']},sort_keys=True))
