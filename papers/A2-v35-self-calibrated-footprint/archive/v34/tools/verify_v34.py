#!/usr/bin/env python3
"""Finite exact/numerical diagnostics; not continuum proofs or apparatus tests."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import re
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
CHECKS: Counter[str] = Counter()

def require(ok: bool, group: str) -> None:
    if not ok:
        raise RuntimeError(group)
    CHECKS[group] += 1

def blob(path: Path) -> str:
    b = path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def cap_rectangles() -> None:
    # These inequalities put an explicit rectangle in the two rolling disks.
    for rc, rk, q in itertools.product([F(1,3),F(1,2),F(1),F(3)],
                                       [F(1,4),F(2,3),F(2)],
                                       [F(1,10),F(1,100),F(1,1000)]):
        d = min(rc,rk)*q
        u2 = min(rc,rk)*d/16
        for y in [-3*d/4,-d/4]:
            require(u2+(y+rc)**2 <= rc**2, 'rectangle_in_first_disk')
            require(u2+(y-rk+d)**2 <= rk**2, 'rectangle_in_second_disk')
        require(d-d/4 == 3*d/4, 'erosion_depth_reserve')
    for beta, gamma in itertools.product([F(1,4),F(1,2),F(1)],
                                         [F(0),F(1,2),F(1),F(2),F(5)]):
        s=6+beta; p=gamma+F(3,2)
        require(2*p==2*gamma+3, 'mean_cost_exponent')
        require((1+2*p*s)/(s-2)==((2*gamma+3)*s+1)/(s-2),
                'total_attempt_exponent')
        require((s-2)/(s*p)>0, 'inverse_modulus_positive')
        require(F(1,s)*(s-2)==1-2/s, 'support_interpolation_balance')
        require(3*min(s/3,s-2)>=s, 'finite_output_value_accuracy')


def killed_lattices() -> None:
    for side in [3,5]:
        half=side//2
        states=list(itertools.product(range(-half,half+1),repeat=2))
        indices={x:i for i,x in enumerate(states)}
        neighbors=[]
        for x,y in states:
            neighbors.append([indices[p] for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                              if p in indices])
        def transition(v):
            return [sum((v[j] for j in row),F(0))/4 for row in neighbors]
        # The finite state set is clipped, never wrapped or row-normalized.
        require(any(len(row)<4 for row in neighbors), 'killed_boundary_present')
        ones=[F(1)]*len(states); green=[F(0)]*len(states)
        tail=ones[:]; zero=[F(0)]*len(states)
        # One positive component is fully protected by a zero collar.
        v=[F(3+x*x+y*y,12) if abs(x)+abs(y)<=1 else F(0) for x,y in states]
        tv=transition(v); forcing=[a-b for a,b in zip(tv,v)]
        xi=F(1,1000); zeta=F(1,2000)
        exact=zero[:]; noisy=zero[:]
        for n in range(1,49):
            green=[a+b for a,b in zip(green,tail)]; tail=transition(tail)
            tx=transition(exact); tn=transition(noisy)
            exact=[max(F(0),a-g) for a,g in zip(tx,forcing)]
            errors=[xi*(-1)**(i+n) for i in range(len(states))]
            noisy=[min(F(1),max(F(0),a-g-d))+zeta*(-1)**i
                   for i,(a,g,d) in enumerate(zip(tn,forcing,errors))]
            noisy=[min(F(1),max(F(0),a)) for a in noisy]
            for i in range(len(states)):
                require(0<=exact[i]<=v[i], 'bellman_lower_occupation')
                require(abs(noisy[i]-exact[i]) <= (xi+zeta)*green[i],
                        'finite_green_perturbation_bound')
                # A deliberately larger rational bound than (diam W+1)^2.
                require(green[i] <= (2*side+1)**2, 'fixed_aperture_exit_bound')
            require(len(noisy)==side*side, 'state_count_independent_of_depth')
        require(max(abs(a-b) for a,b in zip(exact,v)) < F(1,10**8),
                'protected_occupation_convergence')
    for H,b in itertools.product([F(1),F(10),F(1000)],
                                 [F(1),F(1,16),F(1,1024)]):
        mean=b/(128*H); update=b/(64*H); tail=b/32
        error=tail+H*(2*mean+update)
        require(error < b/8, 'query_error_allocation')
        require(error < b/2 < b-error, 'positive_support_threshold')


def finite_supports() -> None:
    # Fourier arrays represent laboratory support functions. Degree one encodes
    # translation; n>=2 shape. All operations here are exact coefficient algebra.
    for seed in range(1,61):
        C=[F(2),F(seed,100),F(-seed,150),F(seed%7,500),F(seed%5,800),F(1,900)]
        K=[F(1,2),F(1,13),F(-1,17),F(1,400),F(-1,600),F(1,1100)]
        # Coefficient order: constant, cos1,sin1,cos2,sin2,cos3.
        degrees=[0,1,1,2,2,3]
        reflected=[(-1)**d*k for d,k in zip(degrees,K)]
        P=[c+k for c,k in zip(C,reflected)]
        require([p-k for p,k in zip(P,reflected)]==C, 'reflected_minkowski_subtraction')
        require(C[0]-sum((d*d-1)*abs(c) for d,c in zip(degrees[3:],C[3:]))>0,
                'strict_curvature_margin')
        centered=C[:]; centered[1:3]=[F(0),F(0)]
        zP=P[:]; zP[1:3]=[F(0),F(0)]
        zK=reflected[:]; zK[1:3]=[F(0),F(0)]
        require([p-k for p,k in zip(zP,zK)]==centered, 'centering_commutes_with_subtraction')
    # Midpoint perturbation creates a mesh floor, not a depth-linear error.
    for d in [F(1,100),F(1,1000)]:
        w=F(1)
        for n in range(1,41):
            w=w/2+d
            require(w==F(1,2**n)+2*d*(1-F(1,2**n)), 'rounded_bracket_exact_solution')
            require(w<=F(1,2**n)+2*d, 'rounded_bracket_mesh_floor')


def numerical_lenses() -> dict[str,str]:
    mp.mp.dps=60
    ratios=[]; errors=[]; biased=[]
    for r0,R0 in [(1,1),(2,1),(1,2)]:
        r=mp.mpf(r0); R=mp.mpf(R0)
        for depth in ['0.01','0.001','0.0001','0.00001']:
            d=mp.mpf(depth); x=r+R-d
            radical=(x*x+r*r-R*R)/(2*x)
            lo=max(-r,x-R); hi=min(r,x+R)
            def section(y):
                return 2*mp.sqrt(max(mp.mpf(0),min(r*r-y*y,R*R-(y-x)**2)))
            area=mp.quad(section,[lo,radical,hi])
            asym=(4*mp.sqrt(2)/3)*mp.sqrt(r*R/(r+R))*d**mp.mpf('1.5')
            ratio=area/asym; ratios.append(ratio)
            require(mp.mpf('.98')<ratio<mp.mpf('1.02'), 'lens_three_halves_asymptotic')
            for theta in [mp.mpf('-.4'),mp.mpf('.35')]:
                prob=mp.quad(lambda y:section(y)*(1+theta*(y-x)/R),[lo,radical,hi])/(mp.pi*R*R)
                base=area/(mp.pi*R*R)
                require((1-abs(theta))*base<=prob<=(1+abs(theta))*base,
                        'unknown_biased_density_lower_bound')
                biased.append(prob/base)
            errors.append(abs(1-ratio))
        # This law is normalized, biased, and has exactly the same footprint.
        for theta in [mp.mpf('-.4'),mp.mpf('.35')]:
            mass=mp.quad(lambda y:2*mp.sqrt(R*R-y*y)*(1+theta*y/R),[-R,0,R])/(mp.pi*R*R)
            moment=mp.quad(lambda y:y*2*mp.sqrt(R*R-y*y)*(1+theta*y/R),[-R,0,R])/(mp.pi*R*R)
            require(abs(mass-1)<mp.mpf('1e-50'), 'biased_disk_density_normalized')
            require(abs(moment-theta*R/4)<mp.mpf('1e-50'), 'nonzero_unknown_mean')
    return {'precision_decimal_digits':'60',
            'lens_asymptotic_ratio_min':mp.nstr(min(ratios),17),
            'lens_asymptotic_ratio_max':mp.nstr(max(ratios),17),
            'biased_probability_ratio_min':mp.nstr(min(biased),17),
            'biased_probability_ratio_max':mp.nstr(max(biased),17)}


def sources() -> None:
    old=ROOT/'archive/v33'
    unchanged=['01_local_queries.tex','02_adaptive_boundary.tex','03_period_recognition.tex',
               '04_information_bound.tex','06_finite_precision.tex','07_sequential_gauge.tex']
    for name in unchanged:
        require(blob(ROOT/'core'/name)==blob(old/'core'/name),'unchanged_active_proof_chapter')
    main=(ROOT/'main.tex').read_text()
    text=main
    for name in re.findall(r'\\input\{([^}]+)\}',main):
        path=ROOT/(name+'.tex')
        require(path.is_file(),'active_input_exists')
        require(not name.startswith('archive/'),'journal_does_not_input_archive')
        text+='\n'+path.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)),'unique_active_labels')
    for name in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text):
        require(name in labels,'resolved_reference')
    for path in (old/'core').glob('*.tex'):
        require((ROOT/'core'/path.name).is_file(),'every_reviewed_chapter_active')
        for label in re.findall(r'\\label\{([^}]+)\}',path.read_text()):
            require(label in labels,'every_reviewed_label_retained')
    for label in ['thm:stationary-jitter','prop:jitter-modulus','lem:cap-mass',
                  'lem:aperture-green','eq:calibration-quantifiers','cor:no-jitter-floor']:
        require(label in labels,'new_main_result_present')


def main() -> None:
    cap_rectangles(); killed_lattices(); finite_supports()
    numerical=numerical_lenses(); sources()
    print(json.dumps({'schema':'a2-v34-finite-diagnostics-1','status':'passed',
                      'finite_checks':sum(CHECKS.values()),
                      'checks':dict(sorted(CHECKS.items())), 'numerical_controls':numerical,
                      'physical_sensor_executed':False,'formal_proof_certificate':False},
                     indent=2,sort_keys=True))

if __name__=='__main__':
    main()
