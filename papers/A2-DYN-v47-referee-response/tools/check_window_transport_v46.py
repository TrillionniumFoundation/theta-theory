#!/usr/bin/env python3
"""Finite regressions for the transport proof; not continuum certification."""
from fractions import Fraction as F
import json
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    sigma=F(1,4)
    require(1-sigma==F(3,4), 'contact response exponent')
    require(1-2*sigma==F(1,2), 'guard derivative exponent')
    require(1-3*sigma==F(1,4), 'logarithmic distortion exponent')
    require(1-3*F(1,3)<=0, 'bad graded exponent escaped negative control')
    # q^(1/4) <= r, with r rational; endpoint-distance multiplicity is at most two.
    q=F(47,53); r=F(63,64)
    require(r**4>q and r<1, 'rational geometric majorant')
    count_cases=0
    for m in range(1,130):
        distances=[min(j,m-j) for j in range(m+1)]
        flights=[min(j,m-1-j) for j in range(m)]
        for ds in (distances,flights):
            require(max(ds.count(d) for d in set(ds))<=2, 'endpoint multiplicity')
            require(sum((r**d for d in ds),F(0))<=2/(1-r), 'geometric guard sum')
            count_cases+=1
    # Exact exponent balances in the admissible flow time and bandwidth.
    budget_cases=0
    for j in range(1,9):
        eps=F(1,2**j)
        for k in range(1,7):
            delta=eps**3/F(2**k)
            h=eps**3*delta**2
            require(h/delta<=eps**3 and h<=delta**2, 'flow first-exit budgets')
            require(h*(delta**-2+eps**-3*delta**-1)==eps**3+delta,
                    'weighted divergence times flow length')
            B=delta**-4
            require(B>=eps**-12, 'protection-bandwidth threshold')
            require(B**-1*delta**-2==delta**2, 'regular/critical bandwidth balance')
            require(eps**-3/B/delta<=delta**2, 'endpoint log term not absorbed')
            budget_cases+=1
    # The first admissible grazing-clearance angle is uniformly transverse.
    gap_squared=F(53,100)**2-(F(47,100)+F(1,100))**2
    require(gap_squared>0, 'clearance transversality')
    for j in range(1,101):
        s=F(j,101); y=1-s*s
        require(0<y<1 and y*y<=y, 'incidence strip inequality')
    # VF=1 and the exact divergence in a nonaffine roof model.
    u,v=sp.symbols('u v', real=True)
    roof=u+v*v/2
    V=sp.Matrix([1/(1+v*v),v/(1+v*v)])
    require(sp.simplify(V.dot(sp.Matrix([sp.diff(roof,u),sp.diff(roof,v)]))-1)==0,
            'roof translation identity')
    weight=sp.exp(u/5+v/7)
    weighted_div=sp.diff(weight*V[0],u)+sp.diff(weight*V[1],v)
    expected=(1-v*v)/(1+v*v)**2+sp.Rational(1,5)/(1+v*v)+v/sp.Integer(7)/(1+v*v)
    require(sp.simplify(weighted_div/weight-expected)==0, 'Liouville weighted divergence')
    # For F=u and a compactly supported polynomial cutoff, coarea and
    # divergence give exactly the same derivative (including its sign).
    a=(1-u*u)**2*(1-v*v)**2; w=1+u/8
    density=sp.integrate(a*w,(v,-1,1))
    push_div=sp.integrate(sp.diff(a*w,u),(v,-1,1))
    require(sp.expand(sp.diff(density,u)-push_div)==0, 'pushforward derivative sign')
    require(sp.simplify(a.subs(u,1))==0 and sp.simplify(a.subs(u,-1))==0,
            'cutoff boundary trace')
    require(sp.simplify(sp.diff(density,u).subs(u,0))!=0, 'sign negative control is vacuous')
    require(sp.simplify((sp.diff(density,u)+push_div).subs(u,0))!=0,
            'wrong derivative sign escaped negative control')
    # A sharp interval without the guard has a boundary contribution.
    require(sp.integrate(sp.diff(u,u),(u,-1,1))==2,
            'unguarded boundary negative control')
    # Disjoint affine flow boxes: total tube mass is exactly 2h times level mass.
    flow_cases=0
    for j in range(1,17):
        h=F(1,j+2); lengths=[F(1,i+2) for i in range(1,j+1)]
        level=sum(lengths,F(0)); tube=sum((2*h*x for x in lengths),F(0))
        require(tube==2*h*level, 'positive flow-box coarea factor')
        flow_cases+=1
    # Signed mass-one kernels: the ABSOLUTE first moment is indispensable.
    def tent(x): return max(F(0),1-abs(x))
    kernel_cases=0
    for B in range(1,25):
        shifts=[F(0),F(1,B),-F(1,B)]
        weights=[F(2),-F(1,2),-F(1,2)]
        require(sum(weights)==1, 'signed kernel mass')
        first=sum((abs(s)*abs(wt) for s,wt in zip(shifts,weights)),F(0))
        for j in range(-24,25):
            t=F(j,12)
            err=abs(tent(t)-sum((wt*tent(t-s) for s,wt in zip(shifts,weights)),F(0)))
            require(err<=first, 'signed approximate-identity Lipschitz bound')
            kernel_cases+=1
        signed_first=sum((s*wt for s,wt in zip(shifts,weights)),F(0))
        err0=abs(tent(F(0))-sum((wt*tent(-s) for s,wt in zip(shifts,weights)),F(0)))
        require(signed_first==0 and err0>0, 'signed-moment negative control')
    # Pointwise in epsilon is not uniform along every epsilon_m.
    for m in range(2,65):
        fast_eps=F(1,m)
        require(m<fast_eps**-2, 'fixed-parameter/diagonal negative control')
        fixed_eps=F(1,4)
        if m>=16: require(not (m<fixed_eps**-2), 'fixed-epsilon model convergence')
    return {'graded_exponents':['3/4','1/2','1/4'],
            'endpoint_distance_cases':count_cases,'flow_budget_cases':budget_cases,
            'clearance_transversality_squared':str(gap_squared),'incidence_cases':100,
            'symbolic_roof_translation':True,'symbolic_density_derivative':True,
            'affine_flow_box_cases':flow_cases,'signed_kernel_cases':kernel_cases,
            'negative_control_types':5,'bandwidth_modulus':'B^-1/2 after collision limsup',
            'protection_threshold':'B >= C epsilon^-12',
            'count_rate_certified':False,'continuum_proof_certified':False,
            'full_boundary_correction_certified':False}


if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
