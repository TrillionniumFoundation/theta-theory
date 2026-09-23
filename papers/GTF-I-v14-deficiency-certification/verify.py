#!/usr/bin/env python3
"""Finite exact certificate checks and floating-point operator diagnostics.

This is not an analytic proof verifier or a physical Gram-integral validator.
Negative controls alter a designated claim/data and must fail at that check.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from certify import Problem, make_certificate, check_certificate, row_cells, row_vertices

MUTANTS=('missing_cell','false_lower','false_upper','repeated_row',
         'visible_selector_modulus','omit_graph_residual','omit_kick_residual',
         'reverse_word','drop_reset_tail')
HERE=Path(__file__).resolve().parent
count=0; groups={}; group='initial'
def need(ok: bool, message: str) -> None:
    global count
    count+=1;groups[group]=groups.get(group,0)+1
    if not ok:raise RuntimeError('FAILED: '+message)

def test(label: str, *terms):return {'label':label,'terms':list(terms)}
def identity_problem(n: int)->Problem:
    # The input symbol is consumed before a blank delayed query; at private
    # width one only one n-valued decoder row remains. TV(delta_i,p)=1-p_i.
    return Problem.load({'model':'delayed_identity_private_width_one','input_symbols':n,'persistent_width':1,
                         'row_sizes':[n,1],
                         'tests':[test('empty',('0',[]))]+[test('row_'+str(i),('1',[]),('-1',[[0,i]])) for i in range(n)]})

def expect_rejected(problem,cert,mutant):
    try:check_certificate(problem,cert)
    except ValueError as exc:return str(exc)
    raise RuntimeError('FAILED: invalid '+mutant+' certificate accepted')

def run(mutant: str|None = None)->dict:
    global group
    artifacts={}; group='rational_vertex_geometry'
    for d in (1,2,3,4):
        for mesh in (1,2,4):
            cs=row_cells(d,mesh)
            need(bool(cs),'nonempty simplex cover')
            for box,vertices in cs:
                for v in vertices:
                    need(sum(v)==1 and all(Q(b,mesh)<=x<=Q(b+1,mesh) for b,x in zip(box,v)),'invalid clipped-simplex vertex')
            # Rational test points must occur in at least one generated cell.
            for weights in product(range(3),repeat=d):
                s=sum(weights)
                if not s:continue
                p=tuple(Q(w,s) for w in weights)
                need(any(all(Q(b,mesh)<=x<=Q(b+1,mesh) for b,x in zip(box,p)) for box,_ in cs),'simplex point not covered')
    group='exact_private_identity_certificates'
    results={}
    for n in (2,3,4):
        p=identity_problem(n);prior_lo=Q(-1);prior_up=Q(2); seq=[]
        for mesh in (1,2,4):
            c=make_certificate(p,mesh);checked=check_certificate(p,c)
            lo,up=Q(c['lower']),Q(c['upper']);truth=1-Q(1,n)
            need(lo<=truth<=up,'identity optimum excluded')
            need(prior_lo<=lo and up<=prior_up,'dyadic monotonicity')
            need(up-lo<=min(Q(1),Q(n,2*mesh)),'private row coupling modulus')
            need(checked['resource_enlargement'] is False,'original width not preserved')
            prior_lo,prior_up=lo,up
            seq.append([mesh,str(lo),str(up)])
        results[str(n)]=seq
        artifacts['identity'+str(n)]={'input':p.raw,'certificate':c,'verification':checked}
    p=identity_problem(2);c=make_certificate(p,2)
    need(Q(c['lower'])==Q(c['upper'])==Q(1,2),'binary private exact interval')
    if mutant in ('missing_cell','false_lower','false_upper'):
        bad=deepcopy(c)
        if mutant=='missing_cell':bad['cells'].pop()
        elif mutant=='false_lower':bad['lower']='3/4';bad['upper']='1'
        else:bad['upper']='1/4';bad['lower']='0'
        # Mutant intentionally adopts the false claim that the bad cert is valid.
        try:check_certificate(p,bad)
        except ValueError as exc:need(False,mutant+': '+str(exc))
        need(False,'designated mutant survived')
    for kind in ('coverage','lower','upper','hash','row_simplex','cell_minimum'):
        bad=deepcopy(c)
        if kind=='coverage':bad['cells'].pop()
        elif kind=='lower':bad['lower']='3/4';bad['upper']='1'
        elif kind=='upper':bad['upper']='1/4';bad['lower']='0'
        elif kind=='hash':bad['problem_sha256']='0'*64
        elif kind=='row_simplex':bad['upper_rows'][0]=['3/4','3/4']
        else:bad['cells'][0]['vertex_min']='99'
        reason=expect_rejected(p,bad,kind)
        need(bool(reason),'missing rejection reason')
    group='multiaffine_two_stage'
    p=Problem.load({'model':'two_independent_rows_Bernoulli_product_target_one_third', 'row_sizes':[2,2],
                    'tests':[test('empty',('0',[])),test('plus',('-1/3',[]),('1',[[0,0],[1,0]])),
                             test('minus',('1/3',[]),('-1',[[0,0],[1,0]]))]})
    prev_lo=Q(-1);prev_up=Q(2);seq=[]
    for mesh in (1,2,4,8):
        c=make_certificate(p,mesh);checked=check_certificate(p,c)
        lo,up=Q(c['lower']),Q(c['upper'])
        need(lo==0 and up>=0,'bilinear attainable zero lower')
        need(lo>=prev_lo and up<=prev_up,'bilinear monotonicity')
        need(up-lo<=1-(1-Q(1,mesh))**2,'depth coupling bound')
        prev_lo,prev_up=lo,up;seq.append([mesh,str(lo),str(up)])
    artifacts['product']={'input':p.raw,'certificate':c,'verification':checked}
    invalid={'row_sizes':[2], 'tests':[test('bad',('1',[[0,0],[0,1]]))]}
    try:Problem.load(invalid)
    except ValueError as exc:
        if mutant=='repeated_row':need(False,str(exc))
        need('repeat a row' in str(exc),'multiaffinity validation')
    else:need(False,'non-multiaffine input was accepted')
    group='selector_and_mark_moduli'
    # Revealed selectors compare TWO changing joint laws. Opposite event
    # fibers give f(lambda)=lambda_0-lambda_1, with oscillation 2 TV(lambda).
    for denominator in (4,8,16):
        u=Q(1,2);v=u+Q(1,denominator);tv=v-u;osc=abs((2*v-1)-(2*u-1))
        bound=tv if mutant=='visible_selector_modulus' else 2*tv
        need(osc<=bound,'visible selector fixed-test needs both target and simulated selector variation')
        need(osc==2*tv,'sharp signed-event selector oscillation')
    for depth in range(1,9):
        for mesh in (2,4,8,16):
            rho=Q(1,mesh);gap=1-(1-rho)**depth
            need(0<=gap<=min(1,depth*rho),'causal union/product modulus')
    group='finite_graph_residuals'
    L=np.array([[0.,-1.,0.],[1.,0.,-2.],[0.,2.,0.]])
    C=[np.eye(3),np.array([[0.,0.,1.],[0.,1.,0.],[1.,0.,0.]])]
    delta=0.19;f=np.array([0.4,-0.6,0.3]);max_error=0.;max_bound=0.
    for dim in (1,2,3):
        iota=np.eye(3)[:,:dim];P=iota@iota.T;J=iota.T@L@iota
        R=(L@iota).T@(L@iota)-J.T@J
        need(np.max(np.abs(R-((np.eye(3)-P)@L@iota).T@((np.eye(3)-P)@L@iota)))<1e-12,'graph Gram factorization')
        need(np.min(np.linalg.eigvalsh(R))>=-1e-12,'graph Gram positivity')
        Bs=[iota.T@ca@iota for ca in C];Ss=[np.eye(dim)-b.T@b for b in Bs]
        Ms=[b@expm(delta*J) for b in Bs];Ts=[ca@expm(delta*L) for ca in C]
        for ca,S in zip(C,Ss):
            need(np.max(np.abs(S-((np.eye(3)-P)@ca@iota).T@((np.eye(3)-P)@ca@iota)))<1e-12,'intervention Gram factorization')
            need(np.min(np.linalg.eigvalsh(S))>=-1e-12,'intervention residual positivity')
        def defect(a,c):
            if np.linalg.norm(R)<1e-14:drift=0.
            else:drift=quad(lambda s: float(np.linalg.norm((np.eye(3)-P)@L@iota@expm(s*J)@c)),0,delta,epsabs=1e-11)[0]
            kick=float(np.linalg.norm((np.eye(3)-P)@C[a]@iota@expm(delta*J)@c))
            return drift+kick
        for length in range(1,5):
            for word in product(range(2),repeat=length):
                exact=f.copy();approx=iota.T@f;bound=float(np.linalg.norm(f-P@f))
                for a in reversed(word):
                    bound+=defect(a,approx);approx=Ms[a]@approx;exact=Ts[a]@exact
                err=float(np.linalg.norm(exact-iota@approx))
                need(err<=bound+2e-10,'controlled-word residual bound')
                max_error=max(max_error,err);max_bound=max(max_bound,bound)
        if dim==3:
            word=(0,1);correct=Ts[0]@Ts[1]@f
            approx=(Ms[1]@Ms[0] if mutant=='reverse_word' else Ms[0]@Ms[1])@f
            need(np.linalg.norm(correct-approx)<1e-12,'Koopman controlled-word order')
    # Separate examples isolate missing residual terms; not just changed labels.
    angle=.3;rot=expm(angle*np.array([[0.,-1.],[1.,0.]]));e1=np.array([1.,0.])
    error=np.linalg.norm(rot@e1-e1)
    graph_bound=0. if mutant=='omit_graph_residual' else angle
    need(error<=graph_bound+1e-12,'nonzero unresolved generator residual')
    swap=np.array([[0.,1.],[1.,0.]]);err=np.linalg.norm(swap@e1)
    kick_bound=0. if mutant=='omit_kick_residual' else 1.
    need(err<=kick_bound+1e-12,'nonzero intervention projection residual')
    group='reset_and_stability'
    for eta in (Q(1,5),Q(2,5),Q(1,2),Q(1)):
        rho=1-eta
        for h in range(8):
            prefix=sum(eta*rho**k for k in range(h+1));tail=rho**(h+1)
            need(prefix+tail==1,'exact cycle-tail mass')
            reported=Q(0) if mutant=='drop_reset_tail' else tail
            # An error confined to the untested ages has exactly the tail mass.
            need(tail<=reported,'finite-age certificate must include remaining ages')
    for lo,up,a,b in [(Q(1,3),Q(1,2),Q(1,20),Q(1,30)),(Q(0),Q(1,4),Q(1,2),Q(1,3))]:
        lower=max(0,lo-a-b);upper=min(1,up+a+b)
        need(lower<=lo<=up<=upper,'stateless presentation interval')
    for norms in product((Q(0),Q(1,4),Q(1,2)),repeat=4):
        need(sum(x*x for x in norms)<=sum(norms)**2,'root sum square no worse than sum')
    if mutant is not None:raise RuntimeError('FAILED: designated mutant survived')
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
    (evidence/'LOCAL_CERTIFICATES.json').write_text(json.dumps(artifacts,indent=2)+'\n')
    return {'status':'passed','finite_checks':count,'groups':groups,
            'identity_intervals':results,'bilinear_intervals':seq,
            'certificates_generated':len(artifacts),'operator_examples_max_error':max_error,
            'operator_examples_max_bound':max_bound,'mutants':MUTANTS,
            'scope':'Exact rational examples and floating-point finite-operator diagnostics; not proof-level certification of the general theorems, physical Gram data, or scholarly priority.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mutant',choices=MUTANTS);args=p.parse_args()
    try:print(json.dumps(run(args.mutant),indent=2))
    except (RuntimeError,ValueError) as exc:
        print(str(exc));raise SystemExit(1)
