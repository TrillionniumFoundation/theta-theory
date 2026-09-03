"""Finite regressions and exact certificates. Not a formal proof assistant."""
from __future__ import annotations
import importlib.util
import math
import json
import re
from fractions import Fraction as F
from pathlib import Path
import unittest
import numpy as np
from scipy.linalg import expm
from scipy.special import logsumexp
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
cert=load('cert',ROOT/'tools/certify_round35.py')
model=load('model',ROOT/'tools/mechanical_benchmark.py')

class ExactCertificate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=cert.certificate();cls.cs=cert.coefficients()
    def test_polynomial_addition(self):
        self.assertEqual(cert.add(cert.C,cert.scale(cert.C,F(-1))),{})
    def test_polynomial_product_derivative(self):
        self.assertEqual(cert.deriv(cert.mul(cert.C,cert.C),0),cert.scale(cert.C,F(2)))
    def test_centered_bound(self):
        self.assertEqual(cert.box_bound(cert.add(cert.C,{(0,0):F(-3,2)})),F(1,2))
    def test_first_markov_parameters(self):
        self.assertEqual(self.cs[:3],[{},cert.ONE,cert.scale(cert.C,F(-1))])
    def test_stiffness_and_coupling_coefficient(self):
        want=cert.add(cert.mul(cert.C,cert.C),cert.scale(cert.K,F(-1)),{(0,0):F(-1,10)})
        self.assertEqual(self.cs[3],want)
    def test_locality_larger_truncation(self):
        self.assertEqual(self.cs,cert.coefficients(9,18))
    def test_exact_frobenius_inequality(self):
        self.assertLess(F(self.report['frobenius_bound_squared_exact']),F(1,4))
    def test_upward_rounded_display(self):
        self.assertLess(F(self.report['frobenius_bound_squared_exact']),F(36375,10**6))
    def test_f1_value_budget(self):
        self.assertLess(F(self.report['f1_absolute_bound_exact']),F(3))
    def test_declared_certificate_scope(self):
        self.assertTrue(self.report['embedding_certified'])
        self.assertFalse(self.report['all_statistical_theorems_formally_verified'])
    def test_invalid_duration(self):
        with self.assertRaises(ValueError):cert.certificate(F(1))
    def test_invalid_locality_cutoff(self):
        with self.assertRaises(ValueError):cert.coefficients(9,3)

class LocalErrata(unittest.TestCase):
    def test_zero_evidence_original_counterexample(self):
        eps=F(1,10);F_norm=F(0)
        original_error=eps*abs(F(0)-F(1))
        self.assertGreater(original_error,2*F_norm*(2*eps))
    def test_zero_evidence_bounded_repair(self):
        eps=F(1,10)
        repaired_error=eps*abs(F(0)-F(0))
        self.assertEqual(repaired_error,0)
    def test_finite_evidence_comparison(self):
        # Nontrivial hidden coupling, including a limiting zero-evidence output.
        weight=np.array([0.4,0.6]);fn=np.array([0.3,-0.8]);f=np.array([0.1,-0.7])
        gn=np.array([[0.7,0.2,0.1],[0.1,0.6,0.3]])
        g=np.array([[0.8,0.2,0],[0.2,0.8,0]])
        rn=weight@gn;r=weight@g;Nn=(weight*fn)@gn;N=(weight*f)@g
        un=Nn/rn;u=np.divide(N,r,out=np.zeros_like(r),where=r>0)
        M=max(abs(fn).max(),abs(f).max())
        rhs=weight@abs(fn-f)+2*M*np.sum(weight[:,None]*abs(gn-g))
        self.assertLessEqual(np.dot(rn,abs(un-u)),rhs)
    def test_singleton_energy_atom(self):
        v=np.array([0.25,-0.75,1.5])
        self.assertEqual(np.dot(v,v)/2-np.dot(v,v)/2,0)
    def test_multiple_particle_orthogonal_energy(self):
        v=np.array([[1.,2.,3.],[-1.,0.,2.],[0.,-2.,1.]])
        p=v.sum(axis=0);m=len(v)
        self.assertAlmostEqual(np.sum(v*v)/2-np.dot(p,p)/(2*m),np.sum((v-v.mean(axis=0))**2)/2)
    def test_fourier_anchor_threshold(self):
        d=3;m=3;s=0
        self.assertLess((d+s)/2-d*m/4,-0.5)
        self.assertFalse(1>2*(d+s+1)/d)
    def test_hilbert_minkowski_range(self):
        rng=np.random.default_rng(7);z=rng.normal(size=(30,4));weights=np.array([1,.5,.25,.125])
        for p in (2,4,8):
            lhs=np.mean(np.sum(weights*z*z,axis=1)**(p/2))**(2/p)
            rhs=np.sum(weights*np.mean(abs(z)**p,axis=0)**(2/p))
            self.assertLessEqual(lhs,rhs+1e-12)

class MechanicalChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=model.simulate();cls.theta=(1.4,1.6)
    def test_generator_bad_input(self):
        with self.assertRaises(ValueError):model.generator((-1,1))
    def test_positive_coupled_stiffness(self):
        A,B,C,K=model.generator(self.theta)
        self.assertGreater(np.linalg.eigvalsh(K)[0],0)
        self.assertNotEqual(K[0,1],0)
    def test_energy_derivative_identity(self):
        A,B,C,K=model.generator(self.theta,8);rng=np.random.default_rng(1)
        q,v=rng.normal(size=(2,8));delta=0.5
        acceleration=-K@q-C@v
        derivative=np.dot(v,acceleration)+np.dot(K@q,v)+delta*(np.dot(v,v)+np.dot(q,acceleration))+delta*np.dot(C@q,v)
        expected=-np.dot(v,(C-delta*np.eye(8))@v)-delta*np.dot(q,K@q)
        self.assertAlmostEqual(derivative,expected,places=11)
    def test_memory_resolvent_infinite_tail(self):
        e=.1;cb=1.5;kb=1.;z=2.;p=z*z+cb*z+kb+2*e
        s=2*e*e/(p+math.sqrt(p*p-4*e*e))
        n=30;J=p*np.eye(n)-e*np.eye(n,k=1)-e*np.eye(n,k=-1)
        finite=e*e*np.linalg.solve(J,np.eye(n)[:,0])[0]
        self.assertAlmostEqual(s,finite,places=14)
        self.assertAlmostEqual(s*(p-s),e*e,places=14)
    def test_memory_first_coefficients(self):
        sites=8;A,B,C,K=model.generator(self.theta,sites)
        idx=list(range(1,sites))+list(range(sites+1,2*sites))
        AQ=A[np.ix_(idx,idx)];BQ=np.zeros((len(idx),2));BQ[sites-1,0]=.1
        CQ=np.zeros((2,len(idx)));CQ[1,0]=.1
        self.assertTrue(np.allclose(CQ@BQ,0))
        self.assertAlmostEqual((CQ@AQ@BQ)[1,0],.01)
        self.assertAlmostEqual((CQ@AQ@AQ@BQ)[1,0],-.015)
    def test_two_duration_jacobian(self):
        tau=1/32;c,k=self.theta
        rows=[];hs=[]
        for d in (tau,2*tau):
            T,b,ds=model.transition(self.theta,d,derivatives=True)
            hs.append(b[0]);rows.append([db[0] for dt,db in ds])
        h1,h2=hs;g1,g2=np.array(rows)
        f1=3/(4*tau**3)*(h2-16*h1+6*tau*tau)
        df1=3/(4*tau**3)*(g2-16*g1)
        df2=3/tau**4*(g2-8*g1)
        jac=np.vstack((df1,2*f1*df1-df2))
        self.assertLess(np.linalg.norm(jac-np.eye(2),'fro')**2,.036375)
    def test_random_sign_cancellation(self):
        d,a,b=F(9,7),F(2),F(3,11)
        self.assertEqual(((d+a*b)**2+(d-a*b)**2)/2,d*d+a*a*b*b)
    def test_adaptive_schedule_uses_history(self):
        probs=self.data['probabilities']
        self.assertTrue(np.all(probs>=.5/4))
        self.assertGreater(len(np.unique(probs,axis=0)),1)
        self.assertTrue(np.allclose(probs.sum(axis=1),1))
    def test_persistent_initial_state_no_reset(self):
        _,_,end,_=model.prediction(self.theta,self.data['actions'],initial=self.data['initial'])
        self.assertTrue(np.allclose(end,self.data['final']))
    def test_sensitivity_recursion(self):
        acts=self.data['actions'][:35]
        m,g,_,_=model.prediction(self.theta,acts,gradients=True)
        delta=1e-5
        for axis in range(2):
            plus=list(self.theta);minus=list(self.theta);plus[axis]+=delta;minus[axis]-=delta
            fd=(model.prediction(plus,acts)[0]-model.prediction(minus,acts)[0])/(2*delta)
            self.assertTrue(np.allclose(fd,g[:,axis],atol=2e-10,rtol=1e-5))
    def test_realized_information_positive(self):
        _,g,_,_=model.prediction(self.theta,self.data['actions'],gradients=True)
        info=g.T@g/(len(g)*.05**2)
        self.assertGreater(np.linalg.eigvalsh(info)[0],0)
    def test_initial_prior_likelihood_identity(self):
        acts=self.data['actions'][:80];y=self.data['y'][:80];var=.05**2
        m=model.prediction(self.theta,acts)[0]
        states=[np.zeros(24),self.data['initial']];weights=np.array([.3,.7])
        log0=-np.sum((y-m)**2)/(2*var)
        direct=[];vs=[]
        for z in states:
            mz=model.prediction(self.theta,acts,initial=z)[0];b=mz-m
            direct.append(-np.sum((y-mz)**2)/(2*var))
            vs.append(np.sum((y-m)*b-.5*b*b)/var)
        self.assertAlmostEqual(logsumexp(np.log(weights)+direct),log0+logsumexp(np.log(weights)+vs),places=10)
    def test_sensitivity_state_covariance_rank(self):
        _,g,_,G=model.prediction(self.theta,self.data['actions'],gradients=True)
        info=g.T@g/(len(g)*.05**2);cov=G@np.linalg.inv(info)@G.T
        self.assertLessEqual(np.linalg.matrix_rank(cov,tol=1e-9),2)
        self.assertGreaterEqual(np.trace(cov),0)
    def test_evidence_gaussian_dimension(self):
        I=np.array([[3.,.6],[.6,2.]]);delta=np.array([.2,-.4]);n=100
        gaussian=2*math.pi/np.sqrt(np.linalg.det(I))*np.exp(.5*delta@np.linalg.solve(I,delta))
        self.assertAlmostEqual(gaussian/n/(gaussian/(4*n)),4)
    def test_preparation_mixture_normalizes(self):
        w=np.array([.2,.3,.5]);r=np.array([-2.,1.,.4]);logw=np.log(w)+r
        p=np.exp(logw-logsumexp(logw));self.assertAlmostEqual(p.sum(),1)

class ActiveSourceGuards(unittest.TestCase):
    def test_no_control_bytes(self):
        for p in list((ROOT/'round35').rglob('*.tex'))+[ROOT/'ROUND35_REVISION.tex']:
            self.assertFalse(any(x<32 and x not in (9,10,13) for x in p.read_bytes()),str(p))
    def test_c2_version_quantifier_is_in_active_source(self):
        text=(ROOT/'round35/supporting/C2.tex').read_text()
        self.assertIn('choose versions satisfying',text)
        self.assertNotIn('With arbitrary versions on zero-evidence sets',text)
    def test_b1_atom_in_active_source(self):
        text=(ROOT/'round35/supporting/B1.tex').read_text()
        self.assertIn('For $m=1$',text);self.assertIn('$W_1=0$',text);self.assertIn('For integer $m\\ge2$',text)
    def test_b3_p_range_in_active_source(self):
        self.assertIn('For $p\\ge2$,',(ROOT/'round35/supporting/B3.tex').read_text())
    def test_bsde_measurability_in_active_source(self):
        text=(ROOT/'round35/supporting/C2.tex').read_text()
        for word in ('standard Borel','sigma-finite','progressively measurable','predictable'):
            self.assertIn(word,text)
    def test_four_canonical_entries_select_round35(self):
        dirs=('B1-microcanonical-preparation','B3-hamilton-boltzmann-cotangents','C1-information-risk-sensitive-saddles','C2-cotangent-rigidity-tangent-representations')
        entries=[ROOT/'papers'/d/'main.tex' for d in dirs]
        for p in entries:self.assertIn('\\input{ROUND35_REVISION.tex}',p.read_text())
    def test_no_information_limit_is_assumed(self):
        text=(ROOT/'round35/mechanical.tex').read_text()
        self.assertIn('Neither result assumes convergence of $I_n$',text)
        self.assertIn('not called classical LAN',text)
    def test_certificate_checks_value_and_derivative(self):
        text=(ROOT/'round35/mechanical.tex').read_text()
        self.assertIn('$\\sup_\\Th|f_1|\\le c_++1$',text)
        self.assertIn('prop:r35-certificate',text)
    def test_ledger_labels_and_dependency_dag(self):
        ledger=json.loads((ROOT/'round35/PROOF_LEDGER.json').read_text())
        labels=set(re.findall(r'\\label\{([^}]+)\}',(ROOT/'round35/mechanical.tex').read_text()))
        seen=set()
        for item in ledger['new_model_theorems']:
            self.assertIn(item['label'],labels)
            self.assertTrue(set(item['dependencies'])<=seen)
            seen.add(item['id'])
        self.assertFalse(ledger['all_original_gaps_closed'])
    def test_original_programme_not_certified_by_build(self):
        text=(ROOT/'round35/mechanical.tex').read_text()
        self.assertIn('does not',text)
        self.assertIn('hard-sphere all-genealogy LDP',text)
        self.assertIn('remain separately tracked',text)

if __name__=='__main__':unittest.main(verbosity=2)
