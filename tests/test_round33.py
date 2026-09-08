#!/usr/bin/env python3
"""Finite algebraic/numerical regression examples, not a proof assistant.
Run directly to write an actual result record, or with unittest.
Only Python's standard library is required.
"""
from __future__ import annotations
import cmath
import json
import math
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path

class Round33Examples(unittest.TestCase):
    def test_01_factorial_majorant(self):
        for n in range(1, 150):
            self.assertLessEqual(n*math.log(n)-math.lgamma(n+1), n+1e-12)
    def test_02_equal_radius_allocation(self):
        M,T,delta=0.7,0.4,3.0
        for n in range(1,30):
            term=(M*n/delta)**n*T**n/math.factorial(n)
            self.assertLessEqual(term,(math.e*M*T/delta)**n*(1+1e-12))
    def test_03_geometric_tail(self):
        q,K=0.42,8
        partial=sum(q**n for n in range(K+1,200))
        self.assertAlmostEqual(partial,q**(K+1)/(1-q),places=14)
    def test_04_independent_endpoint_margin(self):
        a0,lam,T,astar=10,4,1,3
        self.assertGreater(a0-lam*T,astar)
        self.assertFalse(a0>(a0-lam*T)+lam*T)
    def test_05_time_diagonal_is_not_integrable(self):
        truncated=[-math.log(eps) for eps in (1e-2,1e-4,1e-8)]
        self.assertGreater(truncated[2],2*truncated[0])
        self.assertEqual(F(2,1)**3/F(math.factorial(3)), F(4,3))
    def test_06_translation_has_finite_radius(self):
        R,a,t=2.0,1.0,0.3
        series=sum(t**n/(R-a)**(n+1) for n in range(100))
        self.assertAlmostEqual(series,1/(R-a-t),places=12)
        self.assertGreater(1.1/(R-a),1)
    def test_07_tree_tangency_does_not_give_surplus_rank(self):
        # DF=DG=[1,0], R=[1,0]^T, tangent projection diag(0,1).
        projected_surplus=[1*0+0*0,1*0+0*1]
        self.assertEqual(projected_surplus,[0,0])
    def test_08_exact_edge_divergence(self):
        R=[2,3,1]; marks=[1,-2,4]; N=6
        h=[0]; s=[F(0)]
        for r,m in zip(R,marks): h.append(h[-1]+m); s.append(s[-1]+F(r,N))
        phi=lambda t,x:t*t+2*t*x+x*x
        dt=sum((s[k]**2-s[k-1]**2)+2*h[k-1]*(s[k]-s[k-1]) for k in range(1,4))
        div=sum(phi(s[k],h[k-1])-phi(s[k],h[k]) for k in range(1,4))
        self.assertEqual(-dt+div,phi(s[0],h[0])-phi(s[-1],h[-1]))
    def test_09_chronological_only_test(self):
        s=[F(0),F(1,3),F(5,6),F(1)]
        integral=sum(b*b-a*a for a,b in zip(s,s[1:]))
        self.assertEqual(integral,1)
    def test_10_transition_entropy_clock(self):
        p,q,r=0.4,0.7,3
        H=q*math.log(q/p)+(1-q)*math.log((1-q)/(1-p))
        N=300; count=N//r
        self.assertAlmostEqual(count*H/N,H/r)
        self.assertNotAlmostEqual(count*H/N,H)
    def test_11_local_amplitudes_do_not_cancel(self):
        a,b,N=2.0,5.0,1000
        self.assertNotEqual(a/b,1)
        self.assertAlmostEqual(math.log(a/b)/N,(math.log(a)-math.log(b))/N)
    def test_12_ancestry_support(self):
        n=4
        for q in range(-10,11):
            contains_origin=(q-n<=0<=q+n)
            self.assertEqual(contains_origin,abs(q)<=n)
    def test_13_covariance_trace(self):
        vectors=[(1.0,2.0),(-2.0,0.5)]
        diag=[sum(v[i]**2 for v in vectors)/2 for i in range(2)]
        self.assertEqual(sum(diag),sum(sum(x*x for x in v) for v in vectors)/2)
    def test_14_algebraic_norm_is_nonzero(self):
        for k in range(-5,6):
            for m in range(-5,6):
                for n in range(-5,6):
                    if (k,m,n)==(0,0,0): continue
                    norm=(k*k+2*m*m-3*n*n)**2-8*k*k*m*m
                    self.assertNotEqual(norm,0)
    def test_15_arithmetic_excludes_small_frequency_claim(self):
        t=1e-8; lhs=t*math.sqrt(1+2)
        rhs=0.01/(1+t)**3
        self.assertLess(lhs,rhs)
    def test_16_fourier_tail_budget(self):
        dz,dc,M,v,A=3,2,12,4,2
        self.assertLess(v-A*(M-dc),-(dz+dc)/2-1)
        # The obsolete exponential-width majorant has exploding log volume.
        N=10000; kappa=0.1
        self.assertGreater(kappa*dc*N-N/(1+kappa*N),0)
    def test_17_resolvent_fourth_order_remainder(self):
        c=0.7
        for b in (10,100,1000):
            z=1+1j*b
            exact=-c*c/(z+2)
            approx=-c*c/z+2*c*c/z**2-4*c*c/z**3
            self.assertLess(abs(exact-approx)*abs(z)**4,9*c*c)
    def test_18_compression_example_dissipative(self):
        c=0.7
        for x,y in ((1,0),(0,1),(2,-3)):
            quadratic=x*(-x+c*y)+y*(-c*x-2*y)
            self.assertEqual(quadratic,-x*x-2*y*y)
    def test_19_gaussian_anchor_characteristic_normalized(self):
        d,m=3,10
        def cf(u,t):
            return (1-1j*t)**(-d*m/2)*cmath.exp(-m*u*u/(2*(1-1j*t)))
        self.assertEqual(cf(0,0),1)
        u,t=0.7,2.0
        modulus=(1+t*t)**(-d*m/4)*math.exp(-m*u*u/(2*(1+t*t)))
        self.assertAlmostEqual(abs(cf(u,t)),modulus,places=14)
    def test_20_equal_velocity_energy_row_dependent(self):
        v=(F(1),F(2),F(3))
        momentum_rows=[[F(int(i%3==j)) for i in range(6)] for j in range(3)]
        energy=[v[i%3] for i in range(6)]
        combo=[sum(v[j]*momentum_rows[j][i] for j in range(3)) for i in range(6)]
        self.assertEqual(energy,combo)
    def test_21_anchor_size_budget(self):
        d,s,m=3,8,10
        self.assertGreater(m,2*(d+s+1)/d)
        self.assertGreater(d*(m-1)/2,s)
    def test_22_entropy_energy_does_not_control_tail(self):
        for R in (10,100,1000):
            p=1/(R*R)
            self.assertAlmostEqual(p*R*R,1)
            self.assertAlmostEqual(p*R*R/2,0.5)
    def test_23_hilbert_schmidt_gap(self):
        D=12
        self.assertGreaterEqual(D-2*2,0)
        self.assertLess(D-2*7,0)
    def test_24_finite_grid_residual(self):
        values=[]
        for mu in (100,1000,10000):
            p,gamma,r,delta=8,1/8,mu**(-0.5),1/mu
            val=r**p*delta**(-(1+p*gamma))
            self.assertAlmostEqual(val*mu**2,1)
            values.append(val)
        self.assertGreater(values[0],values[-1])
    def test_25_small_jumps_do_not_control_cell_spike(self):
        spike=lambda t:max(0.0,1-abs(2*t-1))
        self.assertEqual((spike(0),spike(1)),(0,0))
        self.assertEqual(spike(0.5),1)
    def test_26_static_entropy_quadratic(self):
        hs=[-1.3,0.0,2.0]; eta=1e-5
        val=sum(((1+eta*h)*math.log1p(eta*h)-eta*h)/eta**2 for h in hs)
        self.assertAlmostEqual(val,0.5*sum(h*h for h in hs),delta=2e-5)
    def test_27_cycle_cost_retained(self):
        normal,cycle=F(3),F(4)
        self.assertEqual((normal**2+cycle**2)/2,F(25,2))
        self.assertGreater(cycle**2/2,0)
    def test_28_stratum_normalization(self):
        alpha=[F(1,2),F(1,3),F(1,6)]
        prob=[F(1,5),F(3,10),F(1,2)]
        self.assertEqual(sum(a*(p/a) for a,p in zip(alpha,prob)),1)
        self.assertEqual(sum(a*(1/a) for a in alpha),3)
    def test_29_projective_bonding(self):
        joint={(0,0):F(1,10),(0,1):F(2,10),(1,0):F(3,10),(1,1):F(4,10)}
        marginal={x:sum(joint[x,y] for y in (0,1)) for x in (0,1)}
        self.assertEqual(marginal,{0:F(3,10),1:F(7,10)})
        self.assertEqual(sum(marginal.values()),1)
    def test_30_adaptive_gaussian_posterior(self):
        prior_mean,prior_var,noise_var=1.0,2.0,1.0
        ys=[0.3,1.4,-0.1]; T=len(ys)
        var=1/(1/prior_var+T/noise_var)
        mean=var*(prior_mean/prior_var+sum(ys)/noise_var)
        self.assertAlmostEqual(mean,0.6)
        self.assertAlmostEqual(var,2/7)
    def test_31_parameter_specific_filters(self):
        p,p0=F(4,5),F(3,5)
        likelihood=(p*p+(1-p)**2)/(p0*p0+(1-p0)**2)
        correct=(p*p+(1-p)**2)/(p0*p0+(1-p0)**2)
        wrong=(p*p0+(1-p)*(1-p0))/(p0*p0+(1-p0)**2)
        self.assertEqual(likelihood,F(17,13))
        self.assertEqual(likelihood,correct)
        self.assertNotEqual(likelihood,wrong)
    def test_32_policy_factors_must_match(self):
        self.assertEqual(F(3,4)/F(1,2),F(3,2))
    def test_33_evidence_weighted_bound(self):
        # Two hidden states coupled identically, two observations.
        g=[[0.9,0.1],[0.2,0.8]]; gn=[[0.8,0.2],[0.25,0.75]]; fs=[-1,2]
        eps=sum(abs(g[i][y]-gn[i][y])/2 for i in range(2) for y in range(2))
        lhs=0
        for y in range(2):
            r=sum(g[i][y] for i in range(2))/2
            rn=sum(gn[i][y] for i in range(2))/2
            a=sum(fs[i]*g[i][y] for i in range(2))/2
            an=sum(fs[i]*gn[i][y] for i in range(2))/2
            lhs+=rn*abs(an/rn-a/r)
        self.assertLessEqual(lhs,2*max(map(abs,fs))*eps)
    def test_34_weak_convergence_not_second_moment(self):
        for n in (10,100):
            self.assertEqual(F(1,n*n)*n*n,1)
            self.assertLess(F(1,n*n),F(1,n))
    def test_35_normalized_gaussian_density(self):
        N=64
        true_density=math.sqrt(N/(2*math.pi))
        missing_density=1/math.sqrt(2*math.pi)
        self.assertEqual(true_density/missing_density,8)
    def test_36_lattice_cell_sum(self):
        N=40
        self.assertEqual(sum(math.comb(N,k) for k in range(N+1)),2**N)
        point=math.comb(N,N//2)/2**N
        self.assertAlmostEqual(point*math.sqrt(N),math.sqrt(2/math.pi),delta=0.01)
    def test_37_fibre_cell_powers(self):
        dz,dr,r=2,3,0; lam=dr/2
        fib=dz/2-lam+(dr-r)/2; cell=-lam+(dr-r)/2
        self.assertEqual(fib,dz/2);self.assertEqual(cell,0)
    def test_38_common_policy_constant(self):
        N=40
        vals=[0.5*math.exp(-N*(a-1)**2)+0.5*math.exp(-N*(a+1)**2)
              for a in [k/1000 for k in range(-1000,1001)]]
        self.assertAlmostEqual(max(vals),0.5,places=12)
        self.assertNotEqual(max(vals),1)
    def test_39_near_maximizer_polynomial_deficit(self):
        vals=[math.log(N)*(math.log(N)/N)**0.5 for N in (10**4,10**8,10**12)]
        self.assertGreater(vals[0],vals[-1])
        self.assertLess(vals[-1],0.001)
    def test_40_memory_chart_growth(self):
        lam,gamma,eta=2.0,0.5,1.0
        for N in (100,10000):
            m=(1+eta)*math.log(N)/lam
            self.assertAlmostEqual(N*math.exp(-lam*m),1/N)
            self.assertAlmostEqual(math.log(math.exp(gamma*m))/math.log(N),0.5)
    def test_41_spatial_collision_product_counterexample(self):
        a=0.6; n=7; grid=1000
        avg=sum((1+a*math.sin(2*math.pi*n*k/grid))**2 for k in range(grid))/grid
        self.assertAlmostEqual(avg,1+a*a/2,places=12)
    def test_42_recession_probability_mass_vanishes(self):
        e,m,R=F(5),F(3),F(100)
        p=(e-m)/(R*R-m)
        self.assertEqual((1-p)*m+p*R*R,e)
        self.assertLess(p,F(1,1000))

class RecordingResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs): super().__init__(*args,**kwargs);self.records=[]
    def addSuccess(self,test): super().addSuccess(test);self.records.append({'id':test.id().split('.')[-1],'ok':True})
    def addFailure(self,test,err): super().addFailure(test,err);self.records.append({'id':test.id().split('.')[-1],'ok':False,'error':str(err[1])})
    def addError(self,test,err): super().addError(test,err);self.records.append({'id':test.id().split('.')[-1],'ok':False,'error':str(err[1])})

if __name__=='__main__':
    runner=unittest.TextTestRunner(verbosity=2,resultclass=RecordingResult)
    result=runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(Round33Examples))
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'build/ROUND33_REGRESSION_RESULTS.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'scope':'finite algebraic/numerical examples; not formal verification of the mechanical applications',
        'passed':len(result.records)-len(result.failures)-len(result.errors),
        'failed':len(result.failures)+len(result.errors),'checks':result.records},indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
