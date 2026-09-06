#!/usr/bin/env python3
"""Executable finite diagnostics for A1 revision 3, not formal theorem proofs.
Run from any directory: python tests/test_revision.py --output validation/revision_checks.json
Requires Python 3.10+, NumPy, SymPy. No network or repository writes.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import platform
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp

A0 = math.sqrt(3) / 2
L, UPPER = .45, .47
METRICS: dict[str, object] = {}


def raw_coeff(T: float, eps: float, theta: float, tag: str, y: float = 0.) -> np.ndarray:
    """Positive cubic Bernstein coefficients of the unnormalized raw density."""
    if not (0 < T < .06 and 0 <= eps < 1 / UPPER**2):
        raise ValueError('Mode outside the proved compact-interval regime')
    j = np.arange(4, dtype=float)
    delta = UPPER - L
    r = L + delta*j/3
    s = L**2 + 2*L*delta*j/3 + delta**2*j*(j-1)/6
    d = np.array([L**(3-k)*UPPER**k for k in range(4)])
    if tag == 'placement':
        return math.pi*s
    if tag == 'nohit':
        return A0 - math.pi*s - 2*T*r
    if tag == 'hit':
        return 2*T*(r + eps*math.cos(y-theta)*d)
    raise ValueError('Unknown raw tag')


def multiply(c: np.ndarray, h: np.ndarray, normalize: bool = True) -> np.ndarray:
    """Positive Bernstein convolution; optional normalization is by coefficient sum."""
    c, h = np.asarray(c, float), np.asarray(h, float)
    if c.ndim != 1 or h.ndim != 1 or not np.all(c > 0) or not np.all(h > 0):
        raise ValueError('Strictly positive one-dimensional coefficient vectors required')
    d, m = len(c)-1, len(h)-1
    ans = np.zeros(d+m+1)
    for i, ci in enumerate(c):
        for j, hj in enumerate(h):
            ans[i+j] += math.comb(d,i)*math.comb(m,j)/math.comb(d+m,i+j)*ci*hj
    return ans/ans.sum() if normalize else ans


def evaluate(c: np.ndarray, t: np.ndarray | float) -> np.ndarray:
    t = np.asarray(t, float)
    if np.any((t < 0) | (t > 1)):
        raise ValueError('Bernstein coordinate must lie in [0,1]')
    d = len(c)-1
    return sum(ci*math.comb(d,i)*t**i*(1-t)**(d-i) for i,ci in enumerate(c))


def invert_cdf(u: np.ndarray, c: np.ndarray | float, theta: float) -> np.ndarray:
    u, c = np.broadcast_arrays(np.asarray(u,float), np.asarray(c,float))
    if np.any((u < 0) | (u > 1)) or np.any(np.abs(c) >= 1):
        raise ValueError('Invalid uniform seed or detector amplitude')
    lo, hi = np.zeros_like(u), np.full_like(u,2*math.pi)
    for _ in range(48):
        mid=(lo+hi)/2
        val=(mid+c*(np.sin(mid-theta)+math.sin(theta)))/(2*math.pi)
        lo=np.where(val<u,mid,lo); hi=np.where(val>=u,mid,hi)
    return (lo+hi)/2


def fail_coeff(T: float, eps: float, moments: np.ndarray) -> np.ndarray:
    mp, m0, m1, m2 = moments
    j=np.arange(4,dtype=float); delta=UPPER-L
    r=L+delta*j/3
    s=L**2+2*L*delta*j/3+delta**2*j*(j-1)/6
    d=np.array([L**(3-k)*UPPER**k for k in range(4)])
    return math.pi*s*(1-mp)+(A0-math.pi*s-2*T*r)*(1-m0)+2*T*r*(1-m1)-2*T*eps*d*m2


class RevisionChecks(unittest.TestCase):
    def test_01_raw_normalization(self):
        R,T,a=sp.symbols('R T a',positive=True)
        masses=[sp.pi*R**2,a-sp.pi*R**2-2*T*R,2*T*R]
        self.assertEqual(sp.expand(sum(masses)/a),1)

    def test_02_conditional_equilibrium(self):
        R,T,a=sp.symbols('R T a',positive=True)
        success=(a-sp.pi*R**2)/a
        self.assertEqual(sp.simplify((2*T*R/a)/success-2*T*R/(a-sp.pi*R**2)),0)

    def test_03_detector_cdf_and_inverse(self):
        seeds=np.linspace(0,1,257)
        for c in (0.,.4,.88):
            y=invert_cdf(seeds,c,1.2)
            recovered=(y+c*(np.sin(y-1.2)+math.sin(1.2)))/(2*math.pi)
            self.assertLess(np.max(np.abs(recovered-seeds)),8e-15)
            self.assertTrue(np.all(np.diff(y)>0))

    def test_04_elementary_bernstein_identities(self):
        t=sp.symbols('t');l=sp.Rational(9,20);u=sp.Rational(47,100);d=u-l
        basis=[sp.binomial(3,j)*t**j*(1-t)**(3-j) for j in range(4)]
        rows=[[l+d*j/3 for j in range(4)],
              [l*l+2*l*d*j/3+d*d*j*(j-1)/6 for j in range(4)],
              [l**(3-j)*u**j for j in range(4)]]
        for power,row in enumerate(rows,1):
            self.assertEqual(sp.expand(sum(x*b for x,b in zip(row,basis))-(l+d*t)**power),0)

    def test_05_coefficient_lower_margin(self):
        tmin,tmax,E=.02,.05,2.
        hmin=min(math.pi*L**2,A0-math.pi*UPPER**2-2*tmax*UPPER,2*tmin*L*(1-E*UPPER**2))
        minima=[]
        for T,eps,theta,y in itertools.product((tmin,tmax),(0.,E),(0.,.7),(0.,.7,math.pi,4.)):
            for tag in ('placement','nohit','hit'):
                h=raw_coeff(T,eps,theta,tag,y)
                self.assertGreaterEqual(h.min()+1e-15,hmin)
                minima.append(float(h.min()))
        METRICS['coefficient_margin']={'T_interval':[tmin,tmax],'E':E,'proved_lower_bound':hmin,'sampled_min':min(minima)}

    def test_06_bernstein_product_rational(self):
        t=sp.symbols('t');c=[sp.Rational(i+1,7) for i in range(5)];h=[sp.Rational(i+2,9) for i in range(4)]
        out=[0]*8
        for i,ci in enumerate(c):
            for j,hj in enumerate(h):
                out[i+j]+=sp.binomial(4,i)*sp.binomial(3,j)/sp.binomial(7,i+j)*ci*hj
        poly=lambda v:sum(x*sp.binomial(len(v)-1,i)*t**i*(1-t)**(len(v)-1-i) for i,x in enumerate(v))
        self.assertEqual(sp.expand(poly(c)*poly(h)-poly(out)),0)

    def test_07_sequence_filter_including_failures(self):
        t=np.linspace(0,1,181);c=np.ones(1);direct=np.ones_like(t)
        factors=[raw_coeff(.04,1.5,.7,'hit',1.1),raw_coeff(.03,.4,1.,'placement'),
                 fail_coeff(.05,2.,np.array([.3,.6,.5,.12])),raw_coeff(.02,0.,0.,'nohit')]
        for h in factors:
            c=multiply(c,h);direct*=evaluate(h,t)
        ratio=evaluate(c,t)/direct
        self.assertLess(np.max(np.abs(ratio/ratio[0]-1)),3e-14)
        self.assertEqual(len(c),13)
        self.assertTrue(np.all(c>0))

    def test_08_beta_mixture_moments(self):
        rng=np.random.default_rng(19);c=rng.uniform(.1,1,13);c/=c.sum();d=len(c)-1
        nodes,weights=np.polynomial.legendre.leggauss(40);t=(nodes+1)/2;weights/=2
        for q in range(7):
            exact=sum(c[i]*math.prod(range(i+1,i+q+1))/math.prod(range(d+2,d+q+2)) for i in range(d+1))
            quadrature=np.sum(weights*t**q*(d+1)*evaluate(c,t))
            self.assertAlmostEqual(exact,quadrature,places=13)

    def test_09_failure_moment_formula(self):
        y=2*math.pi*np.arange(4096)/4096;theta=.7;T=.04;eps=1.5
        gp=.3;g0=.6+.1*np.sin(y);g1=.5+.2*np.cos(y-theta)
        m=np.array([gp,g0.mean(),g1.mean(),np.mean(g1*np.cos(y-theta))])
        h=fail_coeff(T,eps,m)
        for R in np.linspace(L,UPPER,5):
            direct=(1-gp)*math.pi*R**2+np.mean(1-g0)*(A0-math.pi*R**2-2*T*R)
            direct+=np.mean((1-g1)*2*T*R*(1+eps*R**2*np.cos(y-theta)))
            self.assertAlmostEqual(float(evaluate(h,(R-L)/(UPPER-L))),direct,places=14)

    def test_10_failure_is_informative(self):
        h=fail_coeff(.04,1.,np.array([.2,.8,.8,0.]))
        self.assertGreater(abs(h[-1]-h[0]),.01)
        self.assertGreater(h.min(),0)

    def test_11_same_gate_across_radii(self):
        g=.37;y=.9
        for R in (L,.46,UPPER):
            k=float(evaluate(raw_coeff(.04,1.2,.3,'hit',y),(R-L)/(UPPER-L)))/A0
            self.assertAlmostEqual((g*k)/k,g)
        proposed=[]
        for R in (L,UPPER):
            k=float(evaluate(raw_coeff(.04,1.2,.3,'hit',y),(R-L)/(UPPER-L)))/A0
            proposed.append((.3+20*(R-L))*k/k)
        self.assertGreater(abs(proposed[1]-proposed[0]),.39)
        self.assertTrue(all(.2 <= ratio <= .8 for ratio in proposed))

    def test_12_body_support_discrete_exhaustion(self):
        rng=np.random.default_rng(48);Fmat=rng.normal(size=(7,5));weight=np.array([.1,.2,.3,.4,.5,.6,.9]);eta=.2
        for direction in rng.normal(size=(5,5)):
            scalars=Fmat@direction
            formula=eta*np.sum(weight*scalars)+(1-2*eta)*np.sum(weight*np.maximum(scalars,0))
            brute=max(np.sum(weight*scalars*np.array(g)) for g in itertools.product((eta,1-eta),repeat=7))
            self.assertAlmostEqual(formula,brute,places=13)

    def test_13_finite_gate_weak_moment_approximation(self):
        y=2*math.pi*(np.arange(8192)+.5)/8192
        g=.5+.3*np.sin(37*y+.2);test=np.cos(y)+.4*np.sin(2*y)
        errors=[]
        for bins in (16,64,256,1024):
            width=len(y)//bins;gj=np.repeat(g.reshape(bins,width).mean(axis=1),width)
            err=abs(np.mean((g-gj)*test));conditional=np.repeat(test.reshape(bins,width).mean(axis=1),width)
            bound=.8*np.mean(np.abs(test-conditional))
            self.assertLessEqual(err,bound+1e-14);errors.append(err)
        METRICS['finite_gate_moment_errors']=errors

    def test_14_gate_to_cubic_full_rank(self):
        ap,a0g,a1,a2=sp.symbols('ap a0g a1 a2');a,b,e,p=sp.symbols('a b e p',positive=True)
        coeff=sp.Matrix([a*(sp.Rational(1,2)-a0g),b*(a0g-a1),p*(a0g-ap),-b*e*a2/2])
        det=sp.factor(coeff.jacobian([ap,a0g,a1,a2]).det())
        self.assertNotEqual(det,0)
        METRICS['gate_to_cubic_jacobian_determinant']=str(det)

    def test_15_product_rank_matches_dimension_bound(self):
        x=sp.symbols('x');ranks=[]
        for n in (1,2,3):
            polys=[1+sp.Rational(i+1,100)*x**3 for i in range(n)]
            prod=sp.prod(polys);columns=[];normalized=[]
            for i in range(n):
                other=sp.prod(polys[j] for j in range(n) if j!=i)
                for j in range(4):
                    v=sp.expand(x**j*other)
                    columns.append([v.coeff(x,k) for k in range(3*n+1)])
                    vn=sp.expand(v-prod*v.subs(x,0))
                    normalized.append([vn.coeff(x,k) for k in range(3*n+1)])
            rank=sp.Matrix(columns).T.rank();nr=sp.Matrix(normalized).T.rank()
            self.assertEqual(rank,3*n+1);self.assertEqual(nr,3*n);ranks.append([n,rank,nr])
        METRICS['finite_product_jacobian_ranks']=ranks

    def test_16_degree_elevation_positivity(self):
        m=201;a=[F(26,100),F(-1),F(1)]
        values=[];errors=[]
        for k in range(m+1):
            b=a[0]+a[1]*F(k,m)+a[2]*F(k*(k-1),m*(m-1))
            value=(F(k,m)-F(1,2))**2+F(1,100)
            values.append(b);errors.append(abs(b-value))
        self.assertGreater(min(values),0);self.assertLessEqual(max(errors),F(1,m))

    def test_17_capped_tilt_with_counted_failure(self):
        masses=[F(3,5),F(1,5),F(1,5)];g=[F(1,4),F(1,2),F(3,4)]
        success=sum(p*a for p,a in zip(masses,g));f=1-success;cap=5
        output=[sum(f**j*p*a for j in range(cap)) for p,a in zip(masses,g)]
        self.assertEqual(sum(output)+f**cap,1)
        self.assertEqual([x/sum(output) for x in output],[p*a/success for p,a in zip(masses,g)])
        self.assertEqual(sum(f**j for j in range(cap)),(1-f**cap)/(1-f))

    def test_18_fisher_mark_formula(self):
        R=.46;eps=2.;c=eps*R**2;y=2*math.pi*np.arange(65536)/65536
        numeric=np.mean((2*eps*R*np.cos(y))**2/(1+c*np.cos(y)))
        exact=4/R**2*(1/math.sqrt(1-c*c)-1)
        self.assertAlmostEqual(numeric,exact,places=12)

    def test_19_raw_fisher_and_censoring_information(self):
        R=.46;T=.04;eps=1.5;y=2*math.pi*np.arange(32768)/32768
        s=math.pi*R**2/A0;sd=2*math.pi*R/A0
        A=A0-math.pi*R**2;p=2*T*R/A;pd=2*T*(A0+math.pi*R**2)/A**2
        J=4/R**2*(1/math.sqrt(1-eps**2*R**4)-1)
        formula=sd**2/(s*(1-s))+(1-s)*(pd**2/(p*(1-p))+p*J)
        k0=(A-2*T*R)/A0;dk0=(-2*math.pi*R-2*T)/A0
        k1=2*T*R*(1+eps*R**2*np.cos(y))/A0;dk1=2*T*(1+3*eps*R**2*np.cos(y))/A0
        direct=sd**2/s+dk0**2/k0+np.mean(dk1**2/k1)
        self.assertAlmostEqual(formula,direct,places=11)
        gp=.3;g0=.6;g1=.5+.2*np.cos(y)
        f=(1-gp)*s+(1-g0)*k0+np.mean((1-g1)*k1)
        df=(1-gp)*sd+(1-g0)*dk0+np.mean((1-g1)*dk1)
        gated=gp*sd**2/s+g0*dk0**2/k0+np.mean(g1*dk1**2/k1)+df**2/f
        self.assertLessEqual(gated,direct+1e-12)
        METRICS['information_example']={'raw':direct,'gated':gated,'failure_information':df**2/f,'mark_conditional':J}

    def test_20_fixed_adaptive_polynomial_normalization(self):
        R=sp.symbols('R');a=sp.sqrt(3)/2
        def probs(T,g):
            raw=[sp.pi*R**2/a,(a-sp.pi*R**2-2*T*R)/a,2*T*R/a]
            return [gi*p for gi,p in zip(g,raw)]+[1-sum(gi*p for gi,p in zip(g,raw))]
        commands=[probs(sp.Rational(1,50),[sp.Rational(1,3),sp.Rational(2,3),sp.Rational(1,2)]),
                  probs(sp.Rational(1,20),[sp.Rational(3,4),sp.Rational(1,4),sp.Rational(2,3)])]
        histories=[]
        for z1 in range(4):
            for z2 in range(4):
                poly=sp.expand(commands[0][z1]*commands[z1%2][z2]);histories.append(poly)
                self.assertEqual(sp.diff(poly,R,7),0)
        self.assertEqual(sp.simplify(sum(histories)),1)
        self.assertEqual(sp.simplify(sum(sp.diff(x,R) for x in histories)),0)

    def test_21_two_step_full_history_vs_reduced_control(self):
        radii=np.array([L,.46,UPPER]);t=(radii-L)/(UPPER-L);prior=np.array([.3,.4,.3]);lam=.4
        # Exact flag coarsening; no claim that this enumerates continuous detector policies.
        options=[(.02,np.array([.7,.3,.8])),(.05,np.array([.3,.8,.4]))]
        kernels=[];coeff=[]
        for T,g in options:
            raw=[raw_coeff(T,0,0,tag) for tag in ('placement','nohit','hit')]
            gated=[g[i]*h/A0 for i,h in enumerate(raw)]
            gated.append(np.ones(4)-sum(gated))
            coeff.append(gated);kernels.append(np.stack([evaluate(h,t) for h in gated],axis=1))
        reward=np.array([-.2,0.,.4,-.35]);G=np.stack([2+np.cos(math.pi*(radii-d)/(UPPER-L)) for d in (L,UPPER)],axis=1)
        values=[]
        for first in range(2):
            for second in itertools.product(range(2),repeat=4):
                total=0.
                for z1 in range(4):
                    for z2 in range(4):
                        weights=prior*kernels[first][:,z1]*kernels[second[z1]][:,z2]
                        total+=math.exp(lam*(reward[z1]+reward[z2]))*np.max(weights@G)
                values.append(total)
        def dp(c,b):
            weights=prior*evaluate(c,t);post=weights/weights.sum()
            if b==0:return float(np.max(post@G))
            return max(sum(float(post@kernels[a][:,z])*math.exp(lam*reward[z])*dp(multiply(c,coeff[a][z]),b-1) for z in range(4)) for a in range(2))
        reduced=dp(np.ones(1),2);brute=max(values)
        self.assertAlmostEqual(reduced,brute,places=12)
        METRICS['two_step_control']={'policies_enumerated':32,'raw_flag_outcomes':3,'censoring_atom':True,'brute_value':brute,'reduced_value':reduced}

    def test_22_positive_roundoff_posterior_bound(self):
        rng=np.random.default_rng(74);c=rng.uniform(.1,1,16);delta=.03;ct=c*(1+rng.uniform(-delta,delta,len(c)))
        nodes,w=np.polynomial.legendre.leggauss(160);t=(nodes+1)/2;w=w/2
        p=evaluate(c,t);p/=np.sum(w*p);pt=evaluate(ct,t);pt/=np.sum(w*pt)
        tv=.5*np.sum(w*np.abs(p-pt));self.assertLessEqual(tv,delta/(1-delta))

    def test_23_general_bias_identity(self):
        p=np.array([.2,.3,.5]);C=np.array([0.,1.,2.]);B=np.array([.3,-.1,.7]);xi=.4;q=np.array([.4,.4,.2])
        Z=np.sum(p*np.exp(xi*C+B));star=p*np.exp(xi*C+B)/Z
        kl=lambda x,y:np.sum(x*np.log(x/y))
        self.assertAlmostEqual(kl(q,p)-q@B,kl(q,star)+xi*(q@C)-math.log(Z),places=14)

    def test_24_two_trace_formula(self):
        x,a=sp.symbols('x a');rho1=1+x;rho2=2-x;Ftest=1+x*x
        J=sp.integrate(rho1*Ftest,(x,0,a))+sp.integrate(rho2*Ftest,(x,a,1))
        two=(rho1-rho2).subs(x,a)*Ftest.subs(x,a)
        self.assertEqual(sp.expand(sp.diff(J,a)-two),0)

    def test_25_weight_transport_normalization(self):
        a=sp.symbols('a');weights=[1+a,2-a];X=[a,1+2*a];Z=sum(weights)
        J=sum(w*x*x for w,x in zip(weights,X))
        dJ=sum(sp.diff(w,a)*x*x+w*2*x*sp.diff(x,a) for w,x in zip(weights,X))
        self.assertEqual(sp.simplify(sp.diff(J/Z,a)-(dJ-(J/Z)*sp.diff(Z,a))/Z),0)

    def test_27_boundary_gate_normalization_and_zero_failure(self):
        base=np.array([.3,.6,.5,.12]);c0=fail_coeff(.04,1.5,base);c0/=c0.sum()
        for delta in (1.,1e-3,1e-6):
            # g_delta=1-delta*(1-g_base); its normalized failure factor is unchanged.
            m=np.array([1.,1.,1.,0.])+delta*(base-np.array([1.,1.,1.,0.]))
            h=fail_coeff(.04,1.5,m)
            self.assertTrue(np.all(h>0))
            self.assertLess(np.max(np.abs(h/h.sum()-c0)),2e-10)
        self.assertTrue(np.all(fail_coeff(.04,1.5,np.array([1.,1.,1.,0.]))==0))
        all_censored=fail_coeff(.04,1.5,np.zeros(4))
        self.assertTrue(np.allclose(all_censored,A0))

    def test_26_independent_counted_geometry_and_detector(self):
        rng=np.random.default_rng(202609053);draws=300000;R=.46;T=.04;eps=1.5;theta=.7
        uv=rng.random((draws,2));q=np.column_stack((uv[:,0]+.5*uv[:,1],math.sqrt(3)/2*uv[:,1]))
        centers=np.array([(i+.5*j,math.sqrt(3)/2*j) for i in range(-2,4) for j in range(-2,4)])
        outside=np.ones(draws,dtype=bool)
        for center in centers:outside &= np.sum((q-center)**2,axis=1)>R*R
        qv=q[outside];angle=rng.uniform(0,2*math.pi,len(qv));v=np.column_stack((np.cos(angle),np.sin(angle)))
        first=np.full(len(qv),np.inf);hitcenter=np.zeros_like(qv)
        for center in centers:
            delta=qv-center;along=np.sum(delta*v,axis=1);disc=along*along-(np.sum(delta*delta,axis=1)-R*R)
            cand=-along-np.sqrt(np.maximum(disc,0));ok=(disc>=0)&(cand>0)&(cand<T)&(cand<first)
            first[ok]=cand[ok];hitcenter[ok]=center
        hit=np.isfinite(first);z=qv[hit]+first[hit,None]*v[hit]-hitcenter[hit]
        amplitude=eps*np.sum(z*z,axis=1);y=invert_cdf(rng.random(hit.sum()),amplitude,theta)
        hit_values=np.zeros(draws);hit_values[np.flatnonzero(outside)[hit]]=1
        mark_values=np.zeros(draws);mark_values[np.flatnonzero(outside)[hit]]=np.cos(y-theta)
        specs=[('placement_failure',(~outside).astype(float),math.pi*R**2/A0),
               ('collision_per_attempt',hit_values,2*T*R/A0),
               ('collision_weighted_mark',mark_values,(2*T*R/A0)*(eps*R**2)/2)]
        checks=[]
        for name,values,target in specs:
            estimate=float(np.mean(values));se=float(np.std(values,ddof=1)/math.sqrt(draws))
            self.assertLess(abs(estimate-target),7*se+1e-13)
            checks.append({'observable':name,'estimate':estimate,'target':target,'standard_error':se,'z_score':(estimate-target)/se})
        METRICS['counted_geometry']={'seed':202609053,'attempts':draws,'placed':int(outside.sum()),'collisions':int(hit.sum()),'checks':checks,'scope':'one radius and horizon; finite stochastic diagnostic only'}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=Path('revision_checks.json'));args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RevisionChecks))
    content=Path(__file__).read_bytes()
    receipt={'suite':'A1 revision 3 finite diagnostics','tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'passed':result.wasSuccessful(),
             'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__,'script_sha256':hashlib.sha256(content).hexdigest(),
             'script_git_blob':hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest(),'metrics':METRICS,
             'limitations':['Finite diagnostics, not theorem or proof-assistant certification.','Rank checked at n=1,2,3; the arbitrary-n proof is in the manuscript.','Control enumeration is a two-command two-step flag coarsening, not a certification of the full continuous optimum.','Stochastic geometry checks one radius, horizon and seed.']}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':sys.exit(main())
