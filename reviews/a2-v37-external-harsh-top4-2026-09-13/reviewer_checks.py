#!/usr/bin/env python3
"""Finite independent A2-v37 review checks, NOT a native build or proof certificate.

Run with Python 3.10+ and the standard library only. The seventh family imports
an exact Git-blob-checked author build driver, but mocks TeX and pdfinfo. Its
expected finding is a provenance weakness, not a successful manuscript build.
"""
from __future__ import annotations
import argparse
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

REVIEWED_SHA = '6c311aa389e3af833f06f14ae98de7bfc28c1327'
DRIVER_BLOB = '029e9e96537df18a032d36de55e449e262be87c4'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def matmul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def inv2(a):
    det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    require(det != 0, 'Singular matrix')
    return [[a[1][1]/det, -a[0][1]/det], [-a[1][0]/det, a[0][0]/det]]


def signed_density():
    grid = [F(i, 12) for i in range(-4, 5)]
    anchor, d = F(1, 4), F(1)
    cases = 0
    for odd in [F(-1, 7), F(1, 5)]:
        S = lambda u: F(1,2)*u*u + odd*u**3 + F(1,9)*u**4
        for amp in [F(-1, 3), F(2, 5)]:
            B = lambda u: F(1)+amp*u+F(1,11)*u*u
            for Z in [F(3, 2), F(7)]:
                f = lambda u,v: B(u)*B(v)*(d-S(u)-S(v))/Z
                R = lambda u,v: f(u,v)*f(0,0)/(f(u,0)*f(0,v))
                t = lambda u: S(u)/(d-S(u))
                require(1-R(anchor,anchor)==t(anchor)**2, 'Anchor square')
                require(t(anchor)>0, 'Positive anchor')
                for u in grid:
                    require(S(u)<d/4 and B(u)>0, 'Interior margins')
                    T = (1-R(u,anchor))/t(anchor)
                    require(d*T/(1+T)==S(u), 'Signed action inversion')
                    require(f(u,0)/f(0,0)*(1+T)==B(u)/B(0), 'Amplitude inversion')
                    if u:
                        require(S(u)!=S(-u), 'Odd information erased')
                    for v in grid:
                        require(1-R(u,v)==t(u)*t(v), 'Rank-one defect')
                        cases += 1
    return {'status':'passed','exact_density_pairs':cases,'arithmetic':'Fraction',
            'scope':'Interior algebra; these functional examples are not asserted to be realized billiards.'}


def last_jet_blocks():
    cases = 0
    max_det = D(0)
    for g, k0, k1 in [(D('.7'),D('.4'),D('1.7')),
                      (D('1.3'),D('2.1'),D('.3')),
                      (D('.2'),D('.6'),D('.9'))]:
        c0,c1=1+g*k0,1+g*k1
        c=(c0*c1).sqrt()
        sh=(c*c-1).sqrt()
        gamma=(c+sh).ln()
        a0,a1=c*sh/(g*c1),c*sh/(g*c0)
        restored_sh=g*(a0*a1).sqrt()
        restored_c=(1+restored_sh**2).sqrt()
        restored_c0=restored_c*(a0/a1).sqrt()
        require(abs((restored_c0-1)/g-k0)<D('1e-60'),'Leading inversion')
        r0=(c0/c1).sqrt()
        for n in range(3,19):
            x=(-D(n)*gamma).exp()
            den=1-x*x
            diagonal=(1+x*x)/den
            cross0=2*(r0**n)*x/den
            cross1=2*(r0**(-n))*x/den
            error=abs(diagonal**2-cross0*cross1-1)
            max_det=max(max_det,error)
            require(error<D('1e-60'),'Determinant-one block')
            N=128
            finite_own=1+2*sum(x**(2*k) for k in range(1,N+1))
            exact_tail=2*x**(2*(N+1))/den
            require(abs(diagonal-finite_own-exact_tail)<D('1e-60'),'Own-site tail')
            finite_cross=2*r0**n*sum(x**(2*k+1) for k in range(N))
            cross_tail=2*r0**n*x**(2*N+1)/den
            require(abs(cross0-finite_cross-cross_tail)<D('1e-60'),'Cross-site tail')
            cases+=1
    return {'status':'passed','geometry_order_pairs':cases,
            'maximum_determinant_error':str(max_det),
            'scope':'Leading inversion, last-jet multiplicities and explicit geometric tails, not the nonlinear half-line theorem.'}


def lattice_gauge():
    L=[[F(3,2),F(1,3)],[F(1,4),F(5,4)]]
    M=[[F(2),F(1)],[F(0),F(3)]]
    V=matmul(L,M)
    recovered=matmul(V,inv2(M))
    require(recovered==L,'Non-unimodular reconstruction')
    G=matmul(transpose(L),L)
    R=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
    newL=matmul(R,L)
    require(matmul(transpose(newL),newL)==G,'Gram gauge invariance')
    I=[[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]]
    A=[[F(3,5),F(-4,5),F(2)],[F(4,5),F(3,5),F(-1)],[F(0),F(0),F(1)]]
    edges=[(0,1,A),(1,2,[[F(1),F(0),F(1)],[F(0),F(1),F(3)],[F(0),F(0),F(1)]]),
           (0,3,[[F(0),F(-1),F(-2)],[F(1),F(0),F(1)],[F(0),F(0),F(1)]])]
    def propagate(root):
        placed={0:root}
        for u,v,H in edges:
            require(u in placed, 'Unrooted edge order')
            placed[v]=matmul(placed[u],H)
        return placed
    base, transformed=propagate(I),propagate(A)
    for v in base:
        require(transformed[v]==matmul(A,base[v]),'One simultaneous gauge')
    require(set(base)=={0,1,2,3},'Spanning tree coverage')
    require(set(base)!={0,1,2,3,4},'Unreached orbit must not be certified')
    return {'status':'passed','deck_determinant':6,'placed_vertices':4,
            'unreached_fifth_vertex_detected':True,'arithmetic':'Fraction',
            'scope':'Algebra after unique transition congruences are given; no analytic matching or realizability test.'}


def pilot_grid():
    cases=0
    for j in [2,8,20]:
        for h in [F(1,50),F(1,73)]:
            gm,gp=F(7,10),F(13,10)
            ceil=lambda x: -((-x.numerator)//x.denominator)
            L=ceil(j*(gp-gm)/h)+2
            for k in range(31):
                g=gm+F(k,50)
                critical=ceil((j*g+h-j*gm)/h)
                excess=j*gm+critical*h-j*g
                require(0<=critical<=L and h<=excess<=2*h,'Critical pilot cell')
                good_times=[j*gm+l*h for l in range(critical+1) if j*gm+l*h>j*g]
                require(bool(good_times),'No above-onset grid point')
                for t0 in good_times:
                    for t1 in good_times:
                        estimate=(min(t0,t1)-h)/j
                        require(j*abs(estimate-g)<=h,'Midpoint gap error')
                        require(max(t0,t1)<=j*g+2*h,'Localization window')
                        cases+=1
    return {'status':'passed','exact_two_type_success_time_cases':cases,
            'scope':'Grid geometry and simultaneous midpoint bound. No sampled rare-event success or uncharged rejection.'}


def geometric_information():
    probabilities=[D('.000001'),D('.0007'),D('.03'),D('.2'),D('.6')]
    cases=0
    max_ratio=D(0)
    for p in probabilities:
        for q in probabilities:
            affinity=(p*q).sqrt()/(1-((1-p)*(1-q)).sqrt())
            h2=2*(1-affinity)
            pstar=(1+max(p,q))/2
            bound=(p.ln()-q.ln())**2/(4*(1-pstar))
            require(h2>=-D('1e-60') and h2<=bound+D('1e-60'),'Geometric Hellinger bound')
            if bound:
                max_ratio=max(max_ratio,h2/bound)
            cases+=1
    # Log-p derivatives of the NB likelihood, evaluated independently by differences.
    derivative_cases=0
    step=D('1e-18')
    for p in [D('.01'),D('.2'),D('.6')]:
        for k in [1,3,11]:
            for T in [k,k+7,10*k+4]:
                phi=p.ln()
                def ll(x):
                    px=x.exp()
                    return D(k)*x+D(T-k)*(1-px).ln()
                first=(ll(phi+step)-ll(phi-step))/(2*step)
                second=(ll(phi+step)-2*ll(phi)+ll(phi-step))/(step*step)
                score=(D(k)-p*T)/(1-p)
                curvature=-D(T-k)*p/(1-p)**2
                require(abs(first-score)<D('1e-28'),'NB log-p score')
                require(abs(second-curvature)<D('1e-26'),'NB log-p information curvature')
                derivative_cases+=1
    return {'status':'passed','geometric_probability_pairs':cases,
            'negative_binomial_derivative_cases':derivative_cases,
            'maximum_Hellinger_to_bound_ratio':str(max_ratio),
            'scope':'Exact affinity formula and finite-difference likelihood checks; not a CLT simulation or an asymptotic proof.'}


def compatible_rates():
    rows=[]
    previous=None
    for ell in [8,12,24,48,96]:
        ell=D(ell)
        delta=(-ell).exp()
        k=D(int(((2*ell).exp()/ell).to_integral_value(rounding='ROUND_CEILING')))
        logk=k.ln()
        j=D(2*int((2*logk).to_integral_value(rounding='ROUND_CEILING')))
        eta=1/(j*k.sqrt())
        fast_mark=(1+(j*k.sqrt()).ln())/(j*j)
        transfer=k*(-j*D(2).ln()).exp()
        remainder=k.sqrt()*(delta+eta+j*delta**2+j*delta*eta+j*eta**2)
        require(0 <= k*delta**2*ell-1 <= delta**2*ell+D('1e-60'),'Rounded critical budget')
        values=(j*delta,fast_mark,transfer,remainder)
        if previous:
            require(all(a<b for a,b in zip(values,previous)),'Displayed budgets did not decrease')
        previous=values
        rows.append({'ell':str(ell),'integer_k':str(k),'critical_budget':str(k*delta**2*ell),
                     'even_j':int(j),'j_delta':str(values[0]),
                     'fast_mark_budget':str(fast_mark),'transfer_budget_tau_half':str(transfer),
                     'sqrt_k_count_remainder_bound_terms':str(remainder)})
    return {'status':'passed','rows':rows,
            'scope':'Finite values of one compatible rate sequence; asymptotic conclusions are checked analytically in the report.'}


def provenance_fixture(driver: Path):
    data=driver.read_bytes()
    require(git_blob(data)==DRIVER_BLOB,'Driver bytes do not match the reviewed Git blob')
    spec=importlib.util.spec_from_file_location('a2_reviewed_build_driver',driver)
    require(spec is not None and spec.loader is not None,'Cannot load driver')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    records=[]
    for case,diverge,recorder in [('matched_control',False,True),
                                  ('divergent_compile_copy',True,True),
                                  ('missing_recorder',False,False)]:
        with tempfile.TemporaryDirectory(prefix='a2-v37-referee-fixture-') as td:
            root=Path(td)
            source,work,out=(root/name for name in ['source','work','output'])
            for path in [source,work,out]:
                path.mkdir()
            original=b'% fixture source A\n'
            consumed=b'% fixture source B: distinct build input\n' if diverge else original
            (source/'main.tex').write_bytes(original)
            (work/'main.tex').write_bytes(consumed)
            def fake_run(cmd,cwd,env,output):
                output.write_text('MOCK EXECUTION: no TeX process was invoked.\n')
                (work/'main.log').write_text('Mock successful engine log.\n')
                (work/'main.pdf').write_bytes(b'MOCK PRODUCT, NOT A PDF')
                if recorder:
                    (work/'main.fls').write_text('INPUT '+str(work/'main.tex')+'\n')
                return 0
            # Only external execution is mocked. build_entry and its recorder/hash logic
            # are exactly the upstream function, verified above by Git blob identity.
            with patch.object(module,'SOURCE',source), patch.object(module,'run',fake_run), \
                 patch.object(module.subprocess,'run',return_value=SimpleNamespace(stdout='Pages: 1\n')):
                result=module.build_entry('main',work,out,{})
            observed=json.loads((out/'main-recorder-source-inputs.json').read_text())
            require(result['status']=='passed','Expected current acceptance path was not reproduced')
            if recorder:
                require(observed=={'main.tex':digest(original)},'Unexpected recorder source hash')
                require((observed['main.tex']!=digest(consumed))==diverge,'Consumed-byte mismatch not demonstrated')
            else:
                require(observed=={},'Missing recorder did not produce an empty map')
            records.append({'case':case,'driver_status':result['status'],
                            'recorder_present':recorder,'original_sha256':digest(original),
                            'compile_copy_sha256':digest(consumed),'recorded_inputs':observed})
    return {'status':'expected_provenance_weaknesses_reproduced','driver_git_blob':DRIVER_BLOB,
            'driver_sha256':digest(data),'fixtures':records,
            'native_main_built':False,'native_companion_built':False,
            'scope':'Three isolated unit fixtures with mocked TeX/pdfinfo. No repository mutation and no manuscript PDF.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--driver',type=Path,default=Path(__file__).resolve().parent/'fixtures'/'build_submission.py')
    args=parser.parse_args()
    with localcontext() as ctx:
        ctx.prec=75
        output={'reviewed_submission':REVIEWED_SHA,'status':'review_checks_completed',
                'formal_proof_verification':False,'native_manuscript_build':False,
                'families':{'signed_density':signed_density(),
                            'last_jet_blocks':last_jet_blocks(),
                            'lattice_and_gauge':lattice_gauge(),
                            'pilot_grid':pilot_grid(),
                            'geometric_and_count_information':geometric_information(),
                            'compatible_rates':compatible_rates(),
                            'build_provenance':provenance_fixture(args.driver)}}
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('REFEREE CHECK FAILURE: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
