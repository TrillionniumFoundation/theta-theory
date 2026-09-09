#!/usr/bin/env python3
"""Independent finite diagnostics for A2 v4; no repository imports or network.
Run: python independent_diagnostics.py > DIAGNOSTICS.json
Finite floating tests are NOT interval certificates or continuum proofs.
Failures use explicit exceptions and remain active under python -O.
"""
import json
import math
import platform
from fractions import Fraction

import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import solve_banded
from scipy.optimize import brentq
import sympy as sp

CHECKS = []


def check(name, condition, kind):
    ok = bool(condition)
    CHECKS.append({"name": name, "kind": kind, "passed": ok})
    if not ok:
        raise RuntimeError("Diagnostic failed: " + name)


def exact_checks():
    h = sp.Matrix([[2, -1], [-1, 2]])
    m = h.inv()
    dq = -(m[0, 0] ** 2 + m[1, 1] ** 2) / 24
    check("one_flight_quartic_derivative", dq == -sp.Rational(1, 27), "exact")
    check("one_flight_shape_derivative", -24 * dq == sp.Rational(8, 9), "exact")
    gamma = sp.acosh(2)
    dinf = -24 * (-(sp.cosh(2*gamma)+2)/(36*sp.sinh(2*gamma)))
    check("half_line_shape_derivative", sp.simplify(sp.expand_trig(dinf)-sp.sqrt(3)/2) == 0, "exact")
    r, g = sp.symbols("r g", positive=True)
    phi = r/sp.sqrt(g*(g+2*r))
    third = sp.factor(sp.diff(phi, r, 3))
    check("radius_third_derivative", sp.simplify(third-3*(3*g+r)/(sp.sqrt(g)*(g+2*r)**sp.Rational(7,2))) == 0, "exact")
    for order in range(1, 11):
        w = [(-1)**(l-1)*math.comb(order, l) for l in range(1, order+1)]
        check(f"richardson_moments_m{order}", all(sum(w[l-1]*l**k for l in range(1, order+1)) == int(k == 0) for k in range(order)), "exact")
        check(f"timing_harmonic_m{order}", sum((Fraction(w[l-1], l) for l in range(1, order+1)), Fraction()) == sum((Fraction(1, l) for l in range(1, order+1)), Fraction()), "exact")
    # Direct rational Schur complements, independent of the hyperbolic formula.
    schur_cases = []
    for c0, c1 in [(sp.Rational(2), sp.Rational(2)), (sp.Rational(7,5), sp.Rational(12,5)), (sp.Rational(3), sp.Rational(5,4))]:
        for j in range(1, 10):
            cs = [c0 if i % 2 == 0 else c1 for i in range(j+1)]
            hfull = sp.zeros(j+1)
            for i in range(j):
                hfull[i,i] += cs[i]
                hfull[i+1,i+1] += cs[i+1]
                hfull[i,i+1] = hfull[i+1,i] = -1
            ends = [0,j]
            hj = hfull.extract(ends, ends)
            detint = sp.Integer(1)
            if j > 1:
                ints = list(range(1,j))
                hi = hfull.extract(ints, ints)
                detint = hi.det()
                hj -= hfull.extract(ends,ints)*hi.inv()*hfull.extract(ints,ends)
            c = sp.sqrt(c0*c1)
            sig0 = sp.sqrt(c1)
            sigj = sp.sqrt(c1 if j % 2 == 0 else c0)
            u = sp.chebyshevu(j-1,c)
            t = sp.chebyshevt(j,c)
            expected = sp.diag(1/sig0,1/sigj)*sp.Matrix([[c*t/u,-c/u],[-c/u,c*t/u]])*sp.diag(1/sig0,1/sigj)
            check(f"schur_{c0}_{c1}_j{j}", all(sp.simplify(x)==0 for x in hj-expected) and sp.simplify(-hj[0,1]*detint-1)==0, "exact")
            schur_cases.append(j)
    x = sp.symbols("x")
    f = x*x/(4-x*x)
    check("jensen_second_derivative", sp.factor(sp.diff(f,x,2)-8*(4+3*x*x)/(4-x*x)**3)==0, "exact")
    return {"dR1_dq":"-1/27", "dR1_ds":"8/9", "dRinf_ds":"sqrt(3)/2", "Phi1_third_derivative":str(third), "timing_factor":"H_m = sum(1/l, l=1..m)"}


def graphs(y, k, cubic, quartic):
    return (k*y*y/2+cubic*y**3/6+quartic*y**4/24,
            k*y+cubic*y*y/2+quartic*y**3/6,
            k+cubic*y+quartic*y*y/2)


def edge(u,v,g,left,right):
    p, pu, puu = graphs(u,*left)
    q, qv, qvv = graphs(v,*right)
    X, D = g+p+q, v-u
    L = np.hypot(X,D)
    U, V = X*pu-D, X*qv+D
    excess = ((p+q)*(X+g)+D*D)/(L+g)
    return excess, U/L, V/L, (pu*pu+X*puu+1)/L-U*U/L**3, (qv*qv+X*qvv+1)/L-V*V/L**3, (pu*qv-1)/L-U*V/L**3


def ldlog(diag,off):
    if not len(diag):
        return 0.0
    piv = float(diag[0])
    if piv <= 0:
        raise RuntimeError("Nonpositive LDL pivot")
    result = math.log(piv)
    for i in range(1,len(diag)):
        piv = float(diag[i])-float(off[i-1])**2/piv
        if piv <= 0:
            raise RuntimeError("Nonpositive LDL pivot")
        result += math.log(piv)
    return result


def bridge(j,u,v,g,pars,start=0):
    n = j-1
    types = [(start+i)%2 for i in range(j+1)]
    y = np.zeros(j+1)
    y[0],y[-1] = u,v
    if n:
        diag0 = np.array([2*(1+g*pars[types[i]][0])/g for i in range(1,j)])
        off0 = np.full(max(0,n-1),-1/g)
        band = np.zeros((3,n))
        band[1] = diag0
        band[0,1:] = off0
        band[2,:-1] = off0
        rhs = np.zeros(n)
        rhs[0] += u/g
        rhs[-1] += v/g
        y[1:-1] = solve_banded((1,1),band,rhs)
    for _ in range(20):
        ed = np.array([edge(y[i],y[i+1],g,pars[types[i]],pars[types[i+1]]) for i in range(j)])
        grad = ed[:-1,2]+ed[1:,1]
        residual = float(np.max(np.abs(grad))) if n else 0.0
        if residual < 2e-15:
            break
        diag = ed[:-1,4]+ed[1:,3]
        off = ed[1:-1,5]
        band[1] = diag
        band[0,1:] = off
        band[2,:-1] = off
        y[1:-1] -= solve_banded((1,1),band,grad)
    if residual >= 3e-12:
        raise RuntimeError("Newton did not converge")
    if n:
        logdet_ratio = ldlog(ed[:-1,4]+ed[1:,3],ed[1:-1,5])-ldlog(diag0,off0)
    else:
        logdet_ratio = 0.0
    logb = float(np.sum(np.log(-g*ed[:,5]))-logdet_ratio)
    return float(np.sum(ed[:,0])), logb, residual


def bridge_checks():
    table=[]
    cases=[("asymmetric",0.4,[(1.3,0.7,3.0),(2.1,-0.9,4.0)]), ("even",1.0,[(1.0,0.0,3.0),(1.0,0.0,3.0)])]
    for name,g,pars in cases:
        u,v=0.035,-0.027
        left=bridge(160,u,0,g,pars,0)
        for j in [4,5,8,9,12,13,20,21,32,33]:
            right=bridge(160,v,0,g,pars,j%2)
            finite=bridge(j,u,v,g,pars)
            ae=abs(finite[0]-left[0]-right[0])
            be=abs(finite[1]-left[1]-right[1])
            check(f"nonlinear_factorization_{name}_j{j}", max(ae,be) < 0.1*math.exp(-0.3*j)+5e-11, "floating_noninterval")
            table.append({"case":name,"j":j,"action_error":ae,"log_relative_twist_error":be,"stationarity_residual":finite[2]})
    # Independent finite Green sum for the quartic coefficient.
    gamma=math.acosh(2)
    a=math.sqrt(3)
    quart=[]
    for j in [1,2,3,4,8,16,32,64]:
        L=np.array([[math.sinh((j-i)*gamma),math.sinh(i*gamma)] for i in range(j+1)])/math.sinh(j*gamma)
        M=np.array([[1/math.tanh(j*gamma),1/math.sinh(j*gamma)],[1/math.sinh(j*gamma),1/math.tanh(j*gamma)]])/a
        vv=np.einsum("ni,ij,nj->n",L,M,L)
        Gii=np.array([math.sinh(i*gamma)*math.sinh((j-i)*gamma)/(a*math.sinh(j*gamma)) for i in range(1,j)])
        dq=-float(Gii@vv[1:-1])/3-(vv[0]**2+vv[-1]**2+2*float(vv[1:-1]@vv[1:-1]))/24
        quart.append({"j":j,"dRj_ds":-24*dq})
    check("finite_quartic_to_limit",abs(quart[-1]["dRj_ds"]-math.sqrt(3)/2)<2e-13,"floating_noninterval")
    return {"half_line_cutoff":160,"factorization":table,"quartic":quart}


def one_flight_F(d,s,angles=96,radial=32):
    nodes,weights=np.polynomial.legendre.leggauss(radial)
    nodes=(nodes+1)/2
    weights=weights/2
    pars=(1.0,0.0,3.0-24*s)
    total=0.0
    for i in range(angles):
        theta=2*math.pi*(i+0.5)/angles
        co,si=math.cos(theta),math.sin(theta)
        root=brentq(lambda r:edge(r*co,r*si,1.0,pars,pars)[0]-d,0.0,3*math.sqrt(d),xtol=1e-15)
        rr=root*nodes
        ed=edge(rr*co,rr*si,1.0,pars,pars)
        total+=float(np.sum(weights*root*(d-ed[0])*(-ed[5])*rr))
    return math.sqrt(3)/(math.pi*d*d)*total*2*math.pi/angles


def quadrature_checks():
    table=[]
    for d in [0.002,0.001,0.0005]:
        step=0.0001
        val=(one_flight_F(d,step)-one_flight_F(d,-step))/(2*step*d)
        check(f"physical_quartic_quadrature_d{d}",abs(val-8/9)<5*d,"floating_noninterval")
        table.append({"d":d,"shape_derivative_of_first_coefficient":val})
    d=0.001
    f0=one_flight_F(d,0)
    f1=one_flight_F(d,0,192,48)
    check("quadrature_refinement",abs(f0-f1)<3e-12,"floating_noninterval")
    return {"local_graph":"psi_s(y)=y^2/2+(3-24s)y^4/24; a local diagnostic, not the global support family", "symmetric_difference_step":0.0001,"table":table,"refinement_difference":abs(f0-f1)}


def coalescence_checks():
    mp.mp.dps=70
    R=mp.mpf(1)/4
    gap=1-2*R
    a=mp.mpf("0.4")
    A0=mp.sqrt(3)/2-mp.pi*R*R
    def amplitude(s,j):
        area=A0+45*mp.pi*s*s/4
        return (1/mp.sinh(j*mp.acosh(1+gap/(R+36*s)))+2/mp.sinh(j*mp.acosh(1+gap/(R-18*s))))/area
    table=[]
    for st in ["0.0001","0.00003","0.00001"]:
        s=mp.mpf(st)
        diff=max(mp.exp(a*j)*abs(amplitude(s,j)-amplitude(-s,j)) for j in range(1,129))
        kp=sorted([1/(R+36*s),1/(R-18*s),1/(R-18*s)])
        km=sorted([1/(R-36*s),1/(R+18*s),1/(R+18*s)])
        dist=max(abs(x-y) for x,y in zip(kp,km))
        check("pairwise_cubic_prefix_s"+st, diff/s**3<mp.mpf("1000000") and dist/s>500,"highprecision_noninterval")
        table.append({"s":st,"weighted_prefix_difference_over_s3":mp.nstr(diff/s**3,22),"matching_curvature_distance_over_s":mp.nstr(dist/s,22)})
    radii=[mp.mpf("0.249"),mp.mpf("0.25"),mp.mpf("0.251")]
    gammas=[mp.acosh(1+gap/r) for r in radii]
    Cs=[sum(1/mp.sinh(j*t) for t in gammas) for j in [1,2,3]]
    mean=2*Cs[1]/Cs[0]
    f=lambda x:x*x/(4-x*x)
    J=Cs[2]/Cs[0]-f(mean)
    xs=[1/mp.cosh(t) for t in gammas]
    ps=[(1/mp.sinh(t))/Cs[0] for t in gammas]
    check("jensen_identity_and_positive_gap",abs(mean-sum(p*x for p,x in zip(ps,xs)))<mp.mpf("1e-65") and J>0 and abs(J-(sum(p*f(x) for p,x in zip(ps,xs))-f(mean)))<mp.mpf("1e-65"),"highprecision_noninterval")
    return {"R":"1/4","sequence_weight":"0.4","prefix_length":128,"precision_decimal_digits":70,"pairwise_table":table,"infinite_norm_status":"The report proves the infinite bound analytically; this test observes only 128 coefficients."}


def main():
    exact=exact_checks()
    nonlinear=bridge_checks()
    quadrature=quadrature_checks()
    coalescence=coalescence_checks()
    kinds=sorted({c["kind"] for c in CHECKS})
    result={"reviewed_commit":"68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f","environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__,"mpmath":mp.__version__},"counts":{"total":len(CHECKS),"passed":sum(c["passed"] for c in CHECKS),"by_kind":{k:sum(c["kind"]==k for c in CHECKS) for k in kinds}},"exact":exact,"nonlinear":nonlinear,"quadrature":quadrature,"coalescence":coalescence,"checks":CHECKS,"limitations":["No repository code imported or author test suite replayed.","No interval arithmetic, formal proof assistant, global equilibrium simulation, PDF rebuild, or remote CI.","Finite nonlinear cutoffs and sampled parameters cannot certify a uniform continuum theorem.","Exact symbolic identities are distinguished from floating and high-precision non-interval diagnostics."]}
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))


if __name__ == "__main__":
    main()
