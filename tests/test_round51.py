"""Finite exact-arithmetic regression tests, not an infinite-theorem certificate."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import sys
import time
import unittest
from fractions import Fraction as F
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import round51_certificates as c

BOX = c.ModelBox((F(1), F(2)), (F(1,2), F(1)), (F(3), F(4)), F(1))


class ExactTests(unittest.TestCase):
    def test_box_constants(self):
        self.assertEqual((BOX.Lambda,BOX.Q), (F(9),F(72)))

    def test_invalid_box(self):
        with self.assertRaises(ValueError):
            c.ModelBox((F(1),F(2)),(F(1),F(2)),(F(3),F(4)),F(1))

    def test_float_rejected(self):
        with self.assertRaises(TypeError):
            c.rat(0.1)

    def test_invalid_clock(self):
        with self.assertRaises(ValueError):
            c.certificate(BOX,0,F(1,2),F(1,10),F(1,2),F(1,4))

    def test_resource_order_preflight(self):
        with self.assertRaises(c.ResourceLimit):
            c.certificate(BOX,100000,F(1,2),F(1,2048),F(1,2),F(1,4096))

    def test_certificate_exact_remainder_and_minimality(self):
        d = c.certificate(BOX,0,F(1,8),F(1,2048),F(1,2),F(1,4096))
        self.assertLessEqual(d['L']*d['E'],F(1,16))
        if d['N'] > d['R']:
            self.assertGreater(d['L']*d['E']*16,F(1,16))
        self.assertEqual(d['p'],F(4097,8192))
        self.assertEqual(d['m'],d['N']+1)
        self.assertGreater(d['kappa'],0)
        self.assertTrue(c.diameter_certified([F(1,8)/(4*d['L']*d['A'])],d,F(1,8)))

    def test_weighted_physical_certificate(self):
        d = c.certificate(BOX,0,F(1),F(1,2048),F(1,2),F(1,4096),weighted=True)
        self.assertGreaterEqual(d['kappa_weighted'],d['kappa'])
        self.assertGreater(d['W'],0)

    def test_single_atom(self):
        for rho in (F(1,100),F(1,2),F(1)):
            self.assertEqual(c.success_probability(rho,F(1)),1)

    def test_representation_counterexample(self):
        tiny = F(1,10**7)
        with self.assertRaises(c.RepresentationError):
            c.validate_band((-tiny,tiny),(-F(1),F(1)),F(0))
        self.assertEqual(c.validate_band((-tiny,tiny),(-F(1),F(1)),1-tiny)[2],1-tiny)

    def test_non_enclosing_representation(self):
        with self.assertRaises(c.RepresentationError):
            c.validate_band((-F(1),F(1)),(F(0),F(1)),F(2))

    def test_negative_representation_budget(self):
        with self.assertRaises(c.RepresentationError):
            c.validate_band((F(0),F(1)),(F(0),F(1)),-F(1))

    def test_outer_preflight(self):
        with self.assertRaises(c.ResourceLimit):
            c.outer_boxes(BOX,0,2,F(1,1000),4,[[(F(1),F(1,100))]],
                          [((-F(1),F(1)),(-F(1),F(1)),F(0))],max_boxes=10)

    def test_outer_complete_witness_and_budgets(self):
        out = c.outer_boxes(BOX,0,1,F(1),8,[[(F(1),F(1,100))]],
                            [((-F(100),F(100)),(-F(100),F(100)),F(0))],max_boxes=2)
        self.assertTrue(out['complete'])
        self.assertEqual(out['boxes_requested'],out['boxes_visited'])
        self.assertEqual(len(out['retained']),1)
        self.assertEqual(len(out['retained'][0]['full']),4)
        self.assertEqual(len(out['retained'][0]['prefix']),3)
        self.assertEqual(set(out['errors']),{'tail','mesh','taylor'})
        self.assertEqual(out['outer_radii'][0],100+2*out['observable_errors'][0])

    def test_outer_pulse_absolute_weights(self):
        out = c.outer_boxes(BOX,0,1,F(1),4,[[(F(1),F(1,100)),(-F(1),F(1,200))]],
                            [((-F(100),F(100)),(-F(101),F(101)),F(1))],max_boxes=2)
        self.assertEqual(out['observable_errors'][0],2*sum(out['errors'].values()))
        self.assertEqual(out['outer_radii'][0],101+2*out['observable_errors'][0])

    def test_invalid_prefix_cut(self):
        with self.assertRaises(ValueError):
            c.outer_boxes(BOX,1,1,F(1),2,[[(F(1),F(1))]],
                          [((-F(1),F(1)),(-F(1),F(1)),F(0))])

    def test_empty_outer_data(self):
        with self.assertRaises(ValueError):
            c.outer_boxes(BOX,0,1,F(1),2,[],[])

    def test_step_first_coefficients(self):
        diag, edges, damping, t = [F(3),F(4)],[F(1,2)],F(3,2),F(1,100)
        self.assertEqual(c.step_taylor(damping,diag,edges,t,2),t*t/2-damping*t**3/6)

    def test_posterior_arithmetic(self):
        self.assertEqual(-F(97,512)+F(13,256)+F(1,32),-F(55,512))
        self.assertLessEqual(-F(55,512),-F(1,16))

    def test_sharp_tail_arithmetic(self):
        self.assertEqual(12*F(1,16)/(1-F(1,16)),F(4,5))
        for Delta in (F(1,128),F(1,1024)):
            self.assertLessEqual(F(4,5)*Delta,1)

    def test_fir_transfer_arithmetic(self):
        # Dividing by the target delta: 3 LA e <= delta/2, LE <= delta/2.
        self.assertEqual(3*F(1,6)+F(1,2),1)
        self.assertEqual(2*F(1,4)+F(1,2),1)

    def test_singular_gram_rejected(self):
        with self.assertRaises(ValueError):
            c.recover_jacobi([F(1)]*5,1)


def add(name, body):
    setattr(ExactTests, 'test_'+name, body)


def sign_case(m):
    def run(self):
        d = [F((-1)**k,k+1) for k in range(m)]
        intercept = [F(k+1,m+1) for k in range(m)]
        amp = F(2,3)
        lhs = sum(sum((intercept[k]+amp*sum(sign[j]*d[k-j] for j in range(k+1)))**2
                      for k in range(m)) for sign in product((-1,1),repeat=m))/2**m
        rhs = sum(x*x for x in intercept)+amp**2*sum((m-k)*d[k]**2 for k in range(m))
        self.assertEqual(lhs,rhs)
    return run


for m in range(1,9):
    add(f'all_signs_m{m}',sign_case(m))


def series_case(r,Delta):
    def run(self):
        N = 12
        cs, rows = c.sampled_coefficients(Delta,r,N)
        lg, sq = c.log_sqrt_series(N+2)
        H = [Delta*x for x in c.series_div(sq[1:],lg[1:],N)]
        lhs = c.series_mul(cs[-1],H,N)
        rhs = [F(1)]+[F(0)]*N
        for _ in range(r-1):
            rhs = c.series_mul(rhs,[x/Delta for x in lg],N)
        self.assertEqual(lhs,rhs)
        # Independent binomial evaluation of T_l U^l versus c_k (U-1)^k.
        for U in (F(0),F(1),F(3,2)):
            self.assertEqual(sum(x*U**l for l,x in enumerate(rows[-1])),
                             sum(x*(U-1)**k for k,x in enumerate(cs[-1])))
    return run


for r in range(1,7):
    for den in (128,1024):
        add(f'sampled_identity_r{r}_d{den}',series_case(r,F(1,den)))


def weighted_case(R):
    def run(self):
        Delta,N = F(1,128),12
        _, rows = c.sampled_coefficients(Delta,R,N)
        W = max(sum(x*x/F(N+1-l) for l,x in enumerate(row)) for row in rows)
        A = 8*Delta**(-R)*4**N
        self.assertGreater(W,0)
        self.assertLessEqual(W,A*A)
        for row in rows:
            self.assertLessEqual(sum(abs(x) for x in row),A)
    return run


for R in range(1,5):
    add(f'weighted_budget_R{R}',weighted_case(R))


def moment_case(J,damping):
    def run(self):
        n = J+3
        diag = [F(3)+F(i,n+1) for i in range(n)]
        edges = [F(1,2)+F(i,4*n) for i in range(n-1)]
        order = 2*J+2
        mu = c.jacobi_moments(diag,edges,order)
        jets = c.boundary_jets(damping,diag,edges,2*order+2)
        self.assertEqual(c.moments_from_jets(jets,order),mu)
        b, a2 = c.recover_jacobi(mu,J)
        self.assertEqual(b,diag[:J+1])
        self.assertEqual(a2,[a*a for a in edges[:J+1]])
    return run


for J in range(4):
    for d in (F(1),F(3,2)):
        add(f'moment_inverse_J{J}_c{d.numerator}_{d.denominator}',moment_case(J,d))


def changed_jet_case(J):
    def run(self):
        n = J+2
        diag, edges = [F(3)]*n,[F(1,2)]*(n-1)
        other = list(diag)
        delta = F(1,7)
        other[J] += delta
        order = 4*J+4
        a = c.boundary_jets(F(3,2),diag,edges,order)
        b = c.boundary_jets(F(3,2),other,edges,order)
        self.assertEqual(a[:order],b[:order])
        self.assertEqual(b[order]-a[order],-delta*F(1,4)**J)
    return run


for J in range(4):
    add(f'first_changed_jet_J{J}',changed_jet_case(J))


def success_case(rho,w):
    def run(self):
        p = c.success_probability(rho,w)
        for m in (1,2,7):
            self.assertGreaterEqual(p**m,(rho*w)**m)
        if rho < 1:
            self.assertGreater(p,rho*w)
    return run


for i,(rho,w) in enumerate(product((F(1,100),F(1,2),F(1)),(F(1,4096),F(1,3),F(1)))):
    add(f'success_probability_{i}',success_case(rho,w))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json-out',type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ExactTests))
    receipt = dict(python=platform.python_version(),tests_run=result.testsRun,
                   failures=len(result.failures),errors=len(result.errors),
                   skipped=len(result.skipped),success=result.wasSuccessful(),
                   elapsed_seconds=round(time.monotonic()-start,3),
                   arithmetic='Fraction exact rational; finite regression only',
                   test_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(json.dumps(receipt,indent=2)+'\n')
    sys.exit(0 if result.wasSuccessful() else 1)
