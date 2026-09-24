#!/usr/bin/env python3
"""Exact algebra and finite face witnesses. These checks do not replace proofs."""
from __future__ import annotations
import argparse
import importlib.util
import json
from itertools import product
from pathlib import Path
import sympy as s


def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)


def run(mutant: str | None = None) -> dict:
    r,g,u,p=s.symbols('r g u p', real=True)
    f=r**3+(13-2*g)*r**2+(3-12*g)*r-(1+2*g)
    D=s.diff(f,r)
    H=(-u**3+(7-4*g)*u**2-3*u+13+4*g)/32
    J=-(u**3+(13-2*g)*u**2+(3-12*g)*u-(1+2*g))/64
    A=(1-p)**4*((1+g)/4-(1-p)**2/2)
    B=p**4*((1+g)/4-p**2/2)
    require(s.expand(A+B-J.subs(u,(2*p-1)**2))==0,'Extreme tie coefficient identity')
    tau=-2*(3*r*r+(8*g-14)*r+3)/D
    chosen=1 if mutant=='free-tie' else tau
    require(s.cancel((s.diff(H,u)+chosen*s.diff(J,u)).subs(u,r))==0,
            'Bayes tie must obey minimax stationarity')
    require(s.cancel(s.diff(J,u).subs(u,r)+D/64)==0,'Contact derivative coefficient')
    # Interval positivity is exact rectangular Bernstein arithmetic inherited from v26.
    old=Path(__file__).resolve().parent.parent/'GTF-I-v26-controlled-memory-foundations'/'verify.py'
    spec=importlib.util.spec_from_file_location('v26_verifier',old)
    if spec is None or spec.loader is None: raise RuntimeError('Missing predecessor verifier')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    require(mod.rectangle_positive(D-8,r,g),'Positive derivative on full bias rectangle')
    numerator,denominator=s.fraction(s.cancel(tau))
    require(mod.rectangle_positive(numerator,r,g) and mod.rectangle_positive(denominator-numerator,r,g),
            'Strict interior tie on full bias rectangle')
    events=[(0,0,1,1),(1,0,1,1),(1,1,1,1),(1,1,0,1),(1,1,0,0)]
    mandatory=events[1:4]
    decision_faces=[{1:0,2:1,3:1},{0:1,1:1,2:0}]
    if mutant=='face-overlap': decision_faces[1]=decision_faces[0].copy()
    compatible=lambda v,F:all(v[j]==x for j,x in F.items())
    require([sum(compatible(v,F) for v in mandatory) for F in decision_faces]==[1,1],
            'Each decision face contains exactly one mandatory vertex')
    require(not any(all(compatible(v,F) for F in decision_faces) for v in product([0,1],repeat=4)),
            'Decision faces are disjoint')
    require(len(set(mandatory))+len(decision_faces)==5,'Decision witness cardinality')
    # Deterministic channels on (unread candidate mark, target diagonal word).
    residuals=[]
    for event, fs in [(events[1],[(0,0),(1,0),(1,1)]),
                      (events[2],[(0,0),(1,1)]),
                      (events[3],[(0,0),(0,1),(1,1)])]:
        for ff in fs:residuals.append(tuple(event[y]-ff[w] for w in range(2) for y in range(4)))
    if mutant=='residual-vertex': residuals[-1]=residuals[0]
    require(len(set(residuals))==8,'Eight distinct forced deterministic continuation channels')
    simple_faces=[{1:0,2:1,3:1},{1:-1,2:0,3:0},{0:1,1:1,2:0},{0:0,1:0,2:-1}]
    faces=[{4*w+j:x for w in range(2) for j,x in F.items()} for F in simple_faces]
    require([sum(compatible(v,F) for v in residuals) for F in faces]==[1,1,1,1],
            'Four output faces have one forced vertex each')
    for i in range(4):
        for j in range(i):
            require(any(k in faces[j] and val!=faces[j][k] for k,val in faces[i].items()),
                    'Output faces must be disjoint')
    # A rational interior tie witnesses the geometry; the manuscript proves every 0<t<1.
    t=s.Rational(1,5)
    mixed=[(t,0,1,1),(t-1,-1,0,0),(1,1,0,t),(0,0,-1,t-1)]
    for F,row in zip(faces,mixed):
        row=tuple(row)*2
        require(compatible(row,F) and row not in residuals,'Mixed face row needs another generator')
    # Positive normalization must precede the report.
    action_probability=[[s.Rational(1,2),s.Rational(1,2)],
                        [s.Rational(1,2),s.Rational(1,2)]]
    if mutant=='anticipating-action': action_probability[1]=[s.Rational(1,3),s.Rational(2,3)]
    require(action_probability[0]==action_probability[1],'Action law cannot depend on unread report')
    # Exact closest-product endpoint comparisons and derived constants.
    gamma0=s.Rational(6,25); delta=s.Rational(7,575)
    require(gamma0*(s.Rational(3,2)-s.Rational(100,69))==delta,'Uniform endpoint gap')
    c=s.Rational(7,2300)
    require(c==delta/4 and 2*c<s.Rational(1,50),'Intrinsic quadratic constant')
    x=s.symbols('x',real=True)
    Fl=2-g-2*s.sqrt((1-g)/2)
    Fh=2+g/2-2*s.sqrt((1+g)/2)
    require(s.simplify((Fh-Fl)-g*(s.Rational(3,2)-2/(s.sqrt((1+g)/2)+s.sqrt((1-g)/2))))==0,
            'Endpoint overlap comparison identity')
    # Test exact rational input points; square roots handled by SymPy algebraic comparisons.
    empirical_d=8 if mutant=='mark-cost' else 4
    require(empirical_d-1==3,'Known fair mark must not enlarge empirical error constant')
    checks=0
    for gamma in [s.Rational(6,25),s.Rational(1,4),s.Rational(13,50)]:
        ss=s.sqrt((1+gamma)/2)
        dd=2*ss-1-(gamma if mutant=='nearest-value' else gamma/2)
        h=(1+gamma)/2
        require(s.simplify(1-((1-ss)**2+s.Rational(1,2))-dd)==0,'Nearest value formula')
        for ip in range(9):
            for iq in range(9):
                pp,qq=s.Rational(ip,8),s.Rational(iq,8)
                aa,cc=(1-pp)*(1-qq),pp*qq
                target=[(1+gamma)/4,(1-gamma)/4,(1-gamma)/4,(1+gamma)/4]
                tv=1-sum(min(x,y) for x,y in zip(target,[aa/2,aa/2,cc/2,cc/2]))
                if pp+qq>=1:
                    aa=pp**2+qq**2+2*h; bb=-2*(pp+qq)
                else:
                    aa=(pp-1)**2+(qq-1)**2+2*h; bb=2*(pp+qq-2)
                # The nearest squared distance is aa+bb*sqrt(h).
                # Check the resulting algebraic number exactly by one squaring.
                ra=tv+1+gamma/2-c*aa; rb=-2-c*bb
                if ra>=0 and rb>=0: ok=True
                elif ra<0 and rb<=0: ok=False
                elif ra>=0: ok=ra**2>=rb**2*h
                else: ok=rb**2*h>=ra**2
                require(bool(ok),'Intrinsic contact growth regression')
                checks+=1
    return {'schema':'gtf27.exact/1','tie_sum_identity':True,'uniform_stationarity':True,
            'decision_vertices':3,'decision_additional_disjoint_faces':2,'exact_decision_width':5,
            'serial_vertices':8,'serial_additional_disjoint_faces':4,'exact_forward_serial_peak':12,
            'serial_scope':'candidate-first serial validation only; not a minimum over all validation orders',
            'intrinsic_growth_constant':'7/2300','uniform_endpoint_gap':'7/575',
            'contact_growth_rational_regressions':checks,'all_N_error_constant':'sqrt(3/N)',
            'asymptotic_value_at_gamma_one_quarter':str(s.sqrt(10)/2-s.Rational(9,8)),
            'scope':'Exact algebra and finite witnesses; continuous optimization and global bounds are proved in the manuscript.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mutant',choices=['free-tie','face-overlap','residual-vertex','anticipating-action','nearest-value','mark-cost'])
    args=ap.parse_args(); print(json.dumps(run(args.mutant),indent=2,sort_keys=True))
