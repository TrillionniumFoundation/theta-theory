#!/usr/bin/env python3
"""Exact finite data used by the physical-certificate examples.

This module performs rational tree normalization, finite feedback enumeration,
polynomial Gram integrations and the sign-table certificate. It does not
implement the general collision-chart exhaustion or real quantifier elimination.
The analytic proofs identify the physical meaning of its exact inputs.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from typing import Sequence
import argparse
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent

def need(ok: bool, message: str) -> None:
    if not ok: raise ValueError(message)

def normalize(values: Sequence[Q]) -> tuple[Q,...]:
    need(bool(values) and all(x>=0 for x in values),'Nonnegative nonempty vector required')
    s=sum(values)
    return tuple(x/s for x in values) if s else tuple(Q(1,len(values)) for _ in values)

def tv(p: Sequence[Q], q: Sequence[Q]) -> Q:
    need(len(p)==len(q),'TV dimensions differ')
    return sum(abs(x-y) for x,y in zip(p,q))/2

def floor_rational(x: Q, denominator: int) -> Q:
    need(type(denominator) is int and denominator>0,'Positive denominator required')
    need(x>=0,'Negative mass')
    return Q((x*denominator).numerator//(x*denominator).denominator,denominator)

def finite_tree(denominator: int, horizon: int=2) -> dict:
    """An explicit two-mark two-action binary-report source and rounded tree.

Node keys (w, previous_actions, previous_reports, next_action) are latent
instrument nodes. No mark is exposed to the simulator. Original joint child
masses are rounded BEFORE normalization. A positive rare prefix is included.
"""
    need(horizon in (1,2),'This enumerated example supports horizons one or two')
    prior=(Q(1,3),Q(2,3))
    emission={(0,0):(Q(1,10**7),1-Q(1,10**7)),(0,1):(Q(1),Q(0)),
              (1,0):(Q(2,5),Q(3,5)),(1,1):(Q(0),Q(1))}
    tprior=tuple(floor_rational(x,denominator) for x in prior)
    rounded_prior=normalize(tprior)
    original={};rounded={};joint={};rounded_joint={}
    error=sum(abs(x-y) for x,y in zip(prior,tprior))
    for k in range(1,horizon+1):
        for w,aa,yy,a in product(range(2),product(range(2),repeat=k-1),
                                product(range(2),repeat=k-1),range(2)):
            prefix=prior[w]
            for ap,yp in zip(aa,yy): prefix*=emission[w,ap][yp]
            key=(w,aa,yy,a); child=tuple(prefix*x for x in emission[w,a])
            rounded_child=tuple(floor_rational(x,denominator) for x in child)
            original[key]=emission[w,a];rounded[key]=normalize(rounded_child)
            joint[key]=child;rounded_joint[key]=rounded_child
            error+=sum(abs(x-y) for x,y in zip(child,rounded_child))
    return dict(prior=prior,rounded_prior=rounded_prior,original=original,rounded=rounded,
                joint=joint,rounded_joint=rounded_joint,rho=min(Q(1),error),horizon=horizon,
                denominator=denominator)

def feedback_law(tree: dict, policy: tuple[int,...], rounded: bool=False) -> tuple[Q,...]:
    prior=tree['rounded_prior' if rounded else 'prior']
    rows=tree['rounded' if rounded else 'original'];horizon=tree['horizon']
    need(len(policy)==(1 if horizon==1 else 3),'Wrong feedback table length')
    law=[]
    for w in range(2):
        for ys in product(range(2),repeat=horizon):
            mass=prior[w];aa=();yy=()
            for k,y in enumerate(ys):
                a=policy[0] if k==0 else policy[1+ys[0]]
                mass*=rows[w,aa,yy,a][y];aa+=(a,);yy+=(y,)
            law.append(mass)
    return tuple(law)

def load_checker():
    path=HERE.parent/'GTF-I-v14-deficiency-certification/certify.py'
    spec=importlib.util.spec_from_file_location('gtf_v14_exact_checker',path)
    need(spec is not None and spec.loader is not None,'Cannot load pinned predecessor checker')
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module

def sign_problem() -> dict:
    """All marked-event tests for two externally chosen physical actions.

Each action has its own output simplex row; source mark is independent fair.
The target joint table follows Theorem thm:v15-quarter, not a floating fit.
"""
    tests=[]
    for ai,a in enumerate((-1,1)):
        outcomes=list(product((-1,1),repeat=2))
        masses=[Q(3,8) if z==a*w else Q(1,8) for w,z in outcomes]
        for mask in range(16):
            subset=[j for j in range(4) if mask>>j&1]
            terms=[[str(sum(masses[j] for j in subset)),[]]]
            for j in subset:
                _,z=outcomes[j];terms.append(['-1/2',[[ai,0 if z==-1 else 1]]])
            tests.append({'name':f'a={a},event={mask}','terms':terms})
    return {'row_sizes':[2,2],'tests':tests,
            'model':'Physical marked sign acquisition; each row is an independent output law at the same stateless budget.'}

def physical_sign_certificate() -> dict:
    checker=load_checker();raw=sign_problem();p=checker.Problem.load(raw)
    c=checker.make_certificate(p,2);checked=checker.check_certificate(p,c)
    need(Q(c['lower'])==Q(1,4)==Q(c['upper']),'Physical sign certificate not one quarter')
    return {'input':raw,'certificate':c,'independent_check':checked,
            'continuous_result':{'value':'1/4','lower_event':'W=sign(aY)',
             'upper_simulator':'Independent N(0,2); analytic density calculation in thm:v15-quarter',
             'warning':'Sign coarsening is not a two-sided exact reconstruction of a continuous report.'}}

def multiply(p: Sequence[Q],q: Sequence[Q]) -> tuple[Q,...]:
    out=[Q(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return tuple(out)

def integrate_symmetric(p: Sequence[Q]) -> Q:
    return sum(Q(2)*c/Q(i+1) for i,c in enumerate(p) if i%2==0)

def bump_gram() -> dict:
    b=(Q(1),Q(0),Q(-2),Q(0),Q(1))
    db=tuple(Q(i)*b[i] for i in range(1,len(b)))
    i0=integrate_symmetric(multiply(b,b));i1=integrate_symmetric(multiply(db,db))
    h=Q(1,4);r=4*i1/(h*h*i0);numerator=2*h**4*i0**4
    norm_lo=numerator/Q(9700);norm_hi=numerator/Q(9600)
    alpha_sq_hi=Q(1,1000)**2*Q(384)*norm_hi/Q(6)
    need(i0==Q(256,315) and i1==Q(256,105) and r==192,'Polynomial Gram integration error')
    need(alpha_sq_hi<Q(1,100000)**2,'Claimed physical error not certified')
    return {'model':'Two diameter-one spheres on side-ten two-dimensional torus; standard Gaussian velocities',
            'b_polynomial':[str(x) for x in b],'I0':str(i0),'I1':str(i1),
            'J':'0','R':str(r),'B_minus':'1','B_plus':'1','S_minus':'0','S_plus':'0',
            'norm_squared_interval':[str(norm_lo),str(norm_hi)],'pi_enclosure':['3','4'],
            'flight_time':'1/1000','noise_scale':'1','preparation_L2_bound':'1',
            'alpha_squared_upper':str(alpha_sq_hi),'alpha_upper':'1/100000',
            'interpretation':'Rigorous analytic equilibrium Gram data, not sampled matrices.'}

def export_examples() -> dict:
    tree_results=[]
    for denominator in (8,32,128,512):
        t=finite_tree(denominator)
        errors=[]
        for policy in product(range(2),repeat=3):
            p=feedback_law(t,policy);q=feedback_law(t,policy,True)
            need(sum(p)==sum(q)==1,'Incoherent causal law')
            errors.append(tv(p,q))
            need(errors[-1]<=t['rho'],'Joint marked feedback error exceeds rho')
        tree_results.append({'denominator':denominator,'rho':str(t['rho']),
                             'max_marked_feedback_TV':str(max(errors)),
                             'policies_enumerated':len(errors),
                             'zero_rounded_positive_nodes':sum(sum(t['joint'][key])>0 and sum(t['rounded_joint'][key])==0 for key in t['joint'])})
    return {'physical_sign':physical_sign_certificate(),'nonzero_physical_gram':bump_gram(),
            'finite_rationalization_regressions':tree_results,
            'scope':'Exact finite checks and analytic-example arithmetic. Not a general collision integrator, quantifier-elimination engine or analytic proof certificate.'}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=export_examples();text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
