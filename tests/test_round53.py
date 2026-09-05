"""Adversarial contract and exact arithmetic regressions; not formal proofs."""
from __future__ import annotations
import argparse
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import round53_certificates as c
from tools import round51_certificates as old

BOX = c.ModelBox((1,2),(F(1,2),1),(3,4),1)
SPEC = c.CertificateSpec(BOX,0,F(1,8),F(1,2048),F(1,2),F(1,4096))
CERT = c.certificate(SPEC)
GRID = c.pulse_grid(CERT)


def broad_bands(n):
    return [((-F(100),F(100)),(-F(100),F(100)),F(0)) for _ in range(n)]


def run_outer(grid=GRID, bands=None, cert=CERT, box=BOX, J=0, **kw):
    return c.certify_outer(box,J,1,F(1),2,grid,
                           broad_bands(len(grid)) if bands is None else bands,
                           cert,max_boxes=kw.pop('max_boxes',1),**kw)


class ContractTests(unittest.TestCase):
    def test_clock_improvement_and_minimality(self):
        legacy = old.certificate(BOX,0,SPEC.delta,SPEC.t0,SPEC.rho,SPEC.w)
        self.assertEqual((legacy['N'],CERT.N,CERT.m,CERT.tau),(60,41,42,F(18,1015)))
        self.assertLessEqual(CERT.L*CERT.E,SPEC.delta/2)
        self.assertGreater(CERT.L*CERT.E/CERT.tau,SPEC.delta/2)
        self.assertGreater(CERT.kappa,legacy['kappa'])

    def test_weighted_certificate(self):
        cert = c.certificate(SPEC,weighted=True)
        c.validate_certificate(cert)
        self.assertGreater(cert.W,0)
        self.assertLessEqual(cert.W,cert.A**2)
        self.assertGreaterEqual(cert.kappa_weighted,cert.kappa)

    def test_canonical_zero_time_and_split_terms(self):
        grid = [[(F(2)*a,t),(-a,t),(F(17),F(0)),(F(0),F(99))] 
                if len(row)==1 else list(row)+[(F(17),F(0))]
                for row in GRID for a,t in [row[-1]]]
        self.assertEqual(c.validate_grid(grid,CERT),tuple(range(CERT.m)))

    def test_reordering_keeps_bands_bound(self):
        bands = [((-F(100+i),F(100+i)),(-F(100+i),F(100+i)),F(0))
                 for i in range(CERT.m)]
        out = run_outer(GRID[::-1],bands[::-1])
        self.assertEqual(out.grid,GRID)
        self.assertEqual(out.statistical_radii,tuple(F(100+i) for i in range(CERT.m)))

    def test_complete_grid_wide_box_not_certified(self):
        out = run_outer()
        self.assertTrue(out.complete)
        self.assertEqual(out.status,'enclosed')
        self.assertFalse(out.diameter_certified)
        self.assertEqual(out.boxes_requested,1)
        self.assertEqual(len(out.full_boxes),1)
        self.assertEqual(len(out.prefix_boxes[0]),3)
        self.assertGreater(out.diameter_upper_bound,SPEC.delta)
        self.assertEqual(dict(out.base_errors).keys(),{'tail','mesh','taylor'})
        for a,b,e,r in zip(out.statistical_radii,out.representation_radii,
                           out.observable_errors,out.outer_radii):
            self.assertEqual(r,a+b+2*e)

    def test_immutable_result(self):
        out = run_outer()
        with self.assertRaises(FrozenInstanceError):
            out.status = 'certified'
        self.assertIsInstance(out.full_boxes,tuple)
        self.assertIsInstance(out.full_boxes[0],tuple)

    def test_empty_not_identification(self):
        bands = [((F(100),F(101)),(F(100),F(101)),F(0))]*CERT.m
        out = run_outer(bands=bands)
        self.assertEqual(out.status,'empty')
        self.assertTrue(out.complete)
        self.assertFalse(out.diameter_certified)

    def test_model_substitution_rejected(self):
        with self.assertRaises(c.ContractError):
            run_outer(box=c.ModelBox((1,3),(F(1,2),1),(3,4),1))

    def test_depth_substitution_rejected(self):
        with self.assertRaises(c.ContractError):
            run_outer(J=1)

    def test_unbound_dictionary_rejected(self):
        with self.assertRaises(c.ContractError):
            run_outer(cert={'L':F(1),'A':F(1),'E':F(0)})

    def test_atomless_exploration(self):
        cert = c.certificate(replace(SPEC,w=F(0)))
        self.assertEqual(cert.p,F(1,2))
        self.assertGreater(cert.kappa,0)

    def test_no_exploration_needed(self):
        self.assertEqual(c.certificate(replace(SPEC,rho=F(0),w=F(0))).p,1)

    def test_zero_fast_probability_rejected(self):
        with self.assertRaises(ValueError):
            replace(SPEC,rho=F(1),w=F(0))

    def test_invalid_clock(self):
        with self.assertRaises(ValueError):
            replace(SPEC,t0=F(1,10))

    def test_order_cap(self):
        with self.assertRaises(c.ResourceLimit):
            c.certificate(SPEC,max_order=8)
        with self.assertRaises(c.ResourceLimit):
            c.certificate(replace(SPEC,J=10000),max_order=8)

    def test_enumeration_cap(self):
        with self.assertRaises(c.ResourceLimit):
            c.certify_outer(BOX,0,1,F(1,100),2,GRID,broad_bands(CERT.m),CERT,max_boxes=1)

    def test_false_representation_budget_rejected(self):
        bands = broad_bands(CERT.m)
        bands[0] = ((-F(1,10**7),F(1,10**7)),(-F(1),F(1)),F(0))
        with self.assertRaises(old.RepresentationError):
            run_outer(bands=bands)

    def test_missing_band_rejected(self):
        with self.assertRaises(c.ContractError):
            run_outer(bands=broad_bands(CERT.m-1))

    def test_conditional_helper_is_not_a_grid_validator(self):
        self.assertTrue(c.radius_budget_satisfied([F(0)]*CERT.m,CERT))
        with self.assertRaises(c.ContractError):
            c.radius_budget_satisfied([F(0)],CERT)
        with self.assertRaises(c.ContractError):
            c.radius_budget_satisfied([-F(1)]*CERT.m,CERT)
        # The certifying endpoint has no parameter accepting precomputed radii.
        with self.assertRaises(TypeError):
            run_outer(radii=[F(0)]*CERT.m)

    def test_positive_nonempty_end_to_end_certificate(self):
        # A deliberately narrow exact box is a positive interface fixture,
        # not a claim of computational efficiency for the broad model box.
        h = F(1,10**180)
        box = c.ModelBox((1-h,1+h),(F(1,2)-h,F(1,2)+h),(3-h,3+h),1)
        cert = c.certificate(replace(SPEC,box=box))
        grid = c.pulse_grid(cert)
        K=P=80
        errors = old.outer_errors(box,max(t for row in grid for _,t in row),K,h,P)
        jets = old.boundary_jets(F(1),[F(3)]*(K+1),[F(1,2)]*K,P+1)
        from math import factorial
        def val(t):
            return sum(jets[k+1]*t**(k+1)/factorial(k+1) for k in range(P+1))
        bands = []
        for row in grid:
            center = sum(a*val(t) for a,t in row)
            error = sum(abs(a) for a,_ in row)*sum(errors.values())
            band = (center-error,center+error)
            bands.append((band,band,F(0)))
        out = c.certify_outer(box,0,K,h,P,grid,bands,cert,max_boxes=1)
        self.assertTrue(out.complete)
        self.assertEqual(len(out.full_boxes),1)
        self.assertTrue(out.diameter_certified)
        self.assertLessEqual(out.diameter_upper_bound,SPEC.delta)

    def test_drift_posterior_constants(self):
        self.assertEqual(-F(3,8)*F(15,32)+F(1,64),-F(41,256))
        self.assertEqual(-F(5,8)*F(1,16)-F(1,64),-F(7,128))
        self.assertEqual(-F(41,256)+F(7,128),-F(27,256))
        self.assertEqual(-F(27,256)+F(8,1024)+F(2,64),-F(17,256))
        self.assertLessEqual(-F(17,256),-F(1,16))
        for d in (F(-7),F(-1,3),F(0),F(2,5)):
            for f in (F(-9),F(-1,2),F(0),F(3)):
                self.assertLessEqual(abs(d*f),f*f/16+4*d*d)

    def test_clock_tail_prefactor(self):
        for den in (128,1024,4096):
            Delta=F(1,den)
            x=min(Delta*BOX.Lambda,F(1,64))
            tau=2*x/(1-x)
            self.assertLessEqual(tau,F(2,63))
            self.assertLessEqual(12*Delta*tau/(1-tau),1)


def add(name,body):
    setattr(ContractTests,'test_'+name,body)


def malformed_grid_case(kind):
    def run(self):
        grid = [list(row) for row in GRID]
        if kind=='missing': grid.pop()
        elif kind=='extra': grid.append(grid[0])
        elif kind=='duplicate': grid[-1]=grid[0]
        elif kind=='scale': grid[-1]=[(2*a,t) for a,t in grid[-1]]
        elif kind=='sign': grid[-1]=[(-a,t) for a,t in grid[-1]]
        elif kind=='clock': grid[-1]=[(a,t+F(1,100000)) for a,t in grid[-1]]
        elif kind=='negative': grid[-1]=[(F(1),-F(1))]
        elif kind=='zero': grid=[[(F(0),F(1,100))]]*CERT.m
        elif kind=='wrong_lag': grid[-1]=[(F(1),CERT.m*CERT.Delta+SPEC.t0),(-F(1),CERT.m*CERT.Delta)]
        with self.assertRaises(c.ContractError):
            run_outer(grid)
    return run

for kind in ('missing','extra','duplicate','scale','sign','clock','negative','zero','wrong_lag'):
    add('grid_reject_'+kind,malformed_grid_case(kind))


def modified_cert_case(field):
    def run(self):
        with self.assertRaises(c.ContractError):
            run_outer(cert=replace(CERT,**{field:getattr(CERT,field)+1}))
    return run

for field in ('R','N','Delta','tau','p','L','A','E','kappa'):
    add('certificate_reject_'+field,modified_cert_case(field))


def old_witness_case(kind):
    def run(self):
        cert = old.certificate(BOX,0,SPEC.delta,SPEC.t0,SPEC.rho,SPEC.w)
        tiny = F(1,10**100)
        if kind=='zero':
            grid,bands=[[(F(0),F(1,100))]],[((F(0),F(0)),(F(0),F(0)),F(0))]
        else:
            count=cert['m'] if kind=='repeated61' else CERT.m if kind=='repeated42' else 1
            radius=F(27,2)*tiny*tiny
            grid=[[(F(1),tiny)]]*count
            bands=[((-radius,radius),(-radius,radius),F(0))]*count
        out=old.outer_boxes(BOX,0,1,F(1),2,grid,bands,max_boxes=1)
        self.assertEqual(len(out['retained']),1)
        self.assertEqual(max(b-a for a,b in out['retained'][0]['prefix']),1)
        self.assertTrue(old.diameter_certified(out['outer_radii'],cert,SPEC.delta))
        with self.assertRaises(c.ContractError):
            run_outer(grid,bands)
    return run

for kind in ('zero','nonzero','repeated61','repeated42'):
    add('round52_witness_'+kind,old_witness_case(kind))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--json-out',type=Path)
    args=parser.parse_args()
    start=time.monotonic()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests))
    receipt=dict(python=platform.python_version(),tests_run=result.testsRun,
                 failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),
                 success=result.wasSuccessful(),elapsed_seconds=round(time.monotonic()-start,3),
                 scope='Finite rational regression; three original witnesses plus repeated42; not formal proof',
                 test_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                 implementation_sha256=hashlib.sha256((ROOT/'tools/round53_certificates.py').read_bytes()).hexdigest())
    if args.json_out:
        args.json_out.parent.mkdir(parents=True,exist_ok=True)
        args.json_out.write_text(json.dumps(receipt,indent=2)+'\n')
    sys.exit(0 if result.wasSuccessful() else 1)
