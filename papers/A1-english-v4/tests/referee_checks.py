#!/usr/bin/env python3
"""Independent finite diagnostics for the A1 English-v2 referee report.

These are referee-written checks, NOT a rerun of the author's test suite and
NOT a proof of the manuscript. The three scope counterexamples test broad
readings of printed hypotheses; the report states the narrower valid repairs.
Run: python referee_checks.py --output CHECK_RESULTS.json
Dependencies: Python >=3.10, NumPy, SymPy. No network, file deletion, or shell.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import platform
import sys
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

METRICS: dict[str, object] = {}

class RefereeChecks(unittest.TestCase):
    def test_01_inherited_bias_breaks_bare_entropy_minimum(self):
        p = [sp.Rational(1, 2)] * 2
        q = [sp.Rational(1, 4), sp.Rational(3, 4)]
        divergence = sum(qi * sp.log(qi / pi) for qi, pi in zip(q, p))
        reverse = sum(pi * sp.log(pi / qi) for pi, qi in zip(p, q))
        self.assertGreater(float(divergence), 0)
        self.assertGreater(float(reverse), 0)
        self.assertEqual(sum(qi * 0 for qi in q), 0)
        METRICS['bias_counterexample'] = {
            'P': ['1/2', '1/2'], 'Q_xi_B': ['1/4', '3/4'],
            'C': [0, 0], 'B': ['0', 'log(3)'], 'xi': 0,
            'D_Q_P': float(divergence), 'D_P_Q': float(reverse)}

    def test_02_corrected_bias_identity(self):
        p = [sp.Rational(1, 2)] * 2
        star = [sp.Rational(1, 4), sp.Rational(3, 4)]
        q = [sp.Rational(2, 5), sp.Rational(3, 5)]
        b = [0, sp.log(3)]
        kl = lambda a, c: sum(x * sp.log(x / y) for x, y in zip(a, c))
        residual = kl(q, p) - kl(q, star) - sum(x*y for x,y in zip(q,b)) + sp.log(2)
        self.assertEqual(sp.expand_log(residual, force=True).simplify(), 0)

    def test_03_two_density_traces_are_needed(self):
        x, a = sp.symbols('x a', real=True)
        # psi is this polynomial on [1/4,3/4], and zero outside. It is C^1.
        psi = 256 * (x-sp.Rational(1,4))**2 * (sp.Rational(3,4)-x)**2
        # rho_minus=psi, rho_plus=2psi, V=0, F=psi.
        integral = sp.integrate(psi**2, (x, sp.Rational(1,4), a))
        integral += 2 * sp.integrate(psi**2, (x, a, sp.Rational(3,4)))
        actual = sp.diff(integral, a).subs(a, sp.Rational(1,2))
        printed_common_trace_term = sp.Integer(0)  # F_minus-F_plus=0
        self.assertEqual(actual, -1)
        self.assertNotEqual(actual, printed_common_trace_term)
        METRICS['shape_counterexample'] = {'actual_derivative_at_half': -1,
            'printed_formula_under_branchwise_density_reading': 0,
            'repair': 'use rho_minus and rho_plus, or assume a common trace'}

    def test_04_preparation_cusp_survives_smooth_dynamics(self):
        h = Fraction(1, 1000)
        expectation = lambda a: Fraction(1,2) - abs(a)
        right = (expectation(h)-expectation(Fraction(0))) / h
        left = (expectation(-h)-expectation(Fraction(0))) / (-h)
        self.assertEqual(right, -1)
        self.assertEqual(left, 1)
        METRICS['preparation_counterexample'] = {
            'fixed_support': [0, 1], 'flow': 'identity',
            'right_difference_quotient': -1, 'left_difference_quotient': 1}

    def test_05_incoming_tube_jacobian(self):
        R, alpha, phi, s = sp.symbols('R alpha phi s', real=True)
        n = sp.Matrix([sp.cos(alpha), sp.sin(alpha)])
        t = sp.Matrix([-sp.sin(alpha), sp.cos(alpha)])
        v = -sp.cos(phi)*n + sp.sin(phi)*t
        q = R*n-s*v
        coordinates = sp.Matrix([q[0],q[1],alpha+sp.pi-phi])
        det = sp.trigsimp(coordinates.jacobian([alpha,phi,s]).det())
        self.assertEqual(sp.trigsimp(det**2-R**2*sp.cos(phi)**2), 0)

    def test_06_flux_normalization_and_domain_derivative(self):
        R,T,A = sp.symbols('R T A', positive=True)
        z = 2*sp.pi*(A-sp.pi*R**2)
        hit = 4*sp.pi*R*T
        no_hit = z-hit
        self.assertEqual(sp.simplify(hit/z-2*R*T/(A-sp.pi*R**2)), 0)
        self.assertEqual(sp.diff(hit,R)+sp.diff(no_hit,R)-sp.diff(z,R), 0)

    def test_07_equilibrium_derivatives_through_eight(self):
        R,T,A = sp.symbols('R T A', positive=True)
        d = A-sp.pi*R**2
        p = 2*R*T/d
        self.assertEqual(sp.simplify(sp.diff(p,R)-2*T*(A+sp.pi*R**2)/d**2), 0)
        for j in range(2,9):
            rhs = (2*j*sp.pi*R*sp.diff(p,R,j-1)+j*(j-1)*sp.pi*sp.diff(p,R,j-2))/d
            self.assertEqual(sp.simplify(sp.diff(p,R,j)-rhs), 0)

    def test_08_nonconstant_collision_observable_integrals(self):
        phi = sp.symbols('phi', real=True)
        mass = sp.integrate(sp.cos(phi),(phi,-sp.pi/2,sp.pi/2))
        dot = sp.integrate(sp.cos(phi)*(1-2*sp.cos(phi)**2),(phi,-sp.pi/2,sp.pi/2))
        self.assertEqual(mass,2)
        self.assertEqual(dot/mass,-sp.Rational(1,3))
        METRICS['exact_observable_identities'] = {
            'E_hit_times_incoming_dot_outgoing': '-p/3',
            'E_hit_times_collision_time': 'p*T/2'}

    def test_09_exact_record_recovers_radius(self):
        R = Fraction(23,50)
        s = Fraction(1,50)
        q0 = R+s
        endpoint = q0-s
        self.assertEqual(endpoint,R)
        self.assertNotEqual(endpoint,Fraction(461,1000))
        # Other angles, including near grazing, check the same coordinate identity.
        errors=[]
        for alpha in (0.,.7,2.3):
            for phi in (-1.56,-.3,0.,1.56):
                n=np.array([math.cos(alpha),math.sin(alpha)])
                t=np.array([-math.sin(alpha),math.cos(alpha)])
                v=-math.cos(phi)*n+math.sin(phi)*t
                initial=float(R)*n-float(s)*v
                errors.append(abs(np.linalg.norm(initial+float(s)*v)-float(R)))
        self.assertLess(max(errors),1e-14)
        METRICS['tagged_record_radius_recovery_max_error']=max(errors)

    def test_10_geometric_margins(self):
        rmin,rmax,T=Fraction(9,20),Fraction(47,100),Fraction(1,25)
        self.assertGreater(rmin*rmin,Fraction(3,16))
        self.assertLess(rmax,Fraction(1,2))
        self.assertEqual(1-2*rmax,Fraction(3,50))
        self.assertLess(T,1-2*rmax)

    def test_11_independent_equilibrium_geometric_sampling(self):
        # Sample the cell and solve line-circle roots directly. This does not
        # sample the collision-tube coordinates used in the manuscript proof.
        rng=np.random.default_rng(20260905)
        draws=400000
        R,T=.46,.04
        uv=rng.random((draws,2))
        q=np.column_stack((uv[:,0]+.5*uv[:,1],math.sqrt(3)/2*uv[:,1]))
        centers=np.array([(i+.5*j,math.sqrt(3)/2*j) for i in range(-2,4) for j in range(-2,4)])
        outside=np.ones(draws,dtype=bool)
        for center in centers:
            outside &= np.sum((q-center)**2,axis=1)>R*R
        q=q[outside]
        theta=rng.uniform(0,2*math.pi,len(q))
        v=np.column_stack((np.cos(theta),np.sin(theta)))
        first=np.full(len(q),np.inf)
        hit_center=np.zeros_like(q)
        for center in centers:
            delta=q-center
            along=np.sum(delta*v,axis=1)
            disc=along*along-(np.sum(delta*delta,axis=1)-R*R)
            candidate=-along-np.sqrt(np.maximum(disc,0))
            valid=(disc>=0)&(candidate>0)&(candidate<=T)&(candidate<first)
            first[valid]=candidate[valid]
            hit_center[valid]=center
        hit=np.isfinite(first)
        normals=(q[hit]+first[hit,None]*v[hit]-hit_center[hit])/R
        incidence=np.sum(v[hit]*normals,axis=1)
        self.assertTrue(np.all(incidence<0))
        weighted_dot=np.zeros(len(q))
        weighted_dot[hit]=1-2*incidence**2
        weighted_time=np.zeros(len(q))
        weighted_time[hit]=first[hit]
        p=2*R*T/(math.sqrt(3)/2-math.pi*R*R)
        checks=[]
        for name,values,target in [('hit_probability',hit.astype(float),p),
            ('hit_weighted_velocity_dot',weighted_dot,-p/3),
            ('hit_weighted_collision_time',weighted_time,p*T/2)]:
            estimate=float(np.mean(values))
            se=float(np.std(values,ddof=1)/math.sqrt(len(values)))
            self.assertLess(abs(estimate-target),7*se+1e-13)
            checks.append({'observable':name,'estimate':estimate,'target':target,
                'standard_error':se,'z_score':(estimate-target)/se})
        METRICS['independent_geometry_sampling']={'seed':20260905,
            'cell_draws':draws,'accepted_equilibrium_states':len(q),
            'R':R,'T':T,'tolerance':'7 estimated standard errors',
            'checks':checks,'limitation':'finite stochastic regression, not uniform geometry proof'}

    def test_12_capped_trial_output_retains_failure(self):
        p=[Fraction(1,3),Fraction(2,3)]
        accept=[Fraction(1,2),Fraction(1)]
        success=sum(x*y for x,y in zip(p,accept))
        budget=4
        output=[sum((1-success)**j*p[i]*accept[i] for j in range(budget)) for i in range(2)]
        failure=(1-success)**budget
        self.assertEqual(sum(output)+failure,1)
        self.assertGreater(failure,0)
        self.assertEqual([x/sum(output) for x in output],[p[i]*accept[i]/success for i in range(2)])


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('CHECK_RESULTS.json'))
    args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(RefereeChecks)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    content=Path(__file__).read_bytes()
    receipt={'review_date':'2026-09-05','suite':'independent referee finite diagnostics',
        'author_test_suite_rerun':False,'pdf_built_or_inspected':False,
        'formal_verification':False,'tests_run':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'passed':result.wasSuccessful(),'python':platform.python_version(),
        'numpy':np.__version__,'sympy':sp.__version__,
        'script_sha256':hashlib.sha256(content).hexdigest(),
        'script_git_blob':hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest(),
        'metrics':METRICS,
        'limitations':['Finite tests are not theorem proofs.',
        'Three scope diagnostics apply to broad readings explicitly qualified in the report.',
        'The geometric simulation uses one radius, one horizon and a fixed finite sample.',
        'No claim of all-order, long-time, or full-suite numerical certification.']}
    args.output.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':
    sys.exit(main())
