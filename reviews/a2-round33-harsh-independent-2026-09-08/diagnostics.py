#!/usr/bin/env python3
"""Independent referee diagnostics for the two pinned A2 source lines.
Finite exact checks and floating quadrature are not continuum proof certificates.
No repository code is imported, no network is used, and assertions survive -O.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
from typing import Any
import numpy as np
from scipy.integrate import quad
import sympy as sp

CHECKS: list[dict[str, Any]] = []

def check(name: str, condition: bool, detail: Any = None) -> None:
    CHECKS.append({'name': name, 'passed': bool(condition), 'detail': detail})
    if not condition:
        raise ArithmeticError(f'Diagnostic failed: {name}: {detail}')

def tail(roofs: tuple[F, ...], t: F, k: int) -> F:
    m = len(roofs)
    a = sum(max(F(0), t-sum(roofs[(i+j)%m] for j in range(k-1))) for i in range(m))
    b = sum(max(F(0), t-sum(roofs[(i+j)%m] for j in range(k))) for i in range(m))
    return (a-b)/sum(roofs)

def direct_tail(roofs: tuple[F, ...], t: F, k: int) -> F:
    m = len(roofs)
    lengths = [max(F(0), min(roofs[i], roofs[i]+t-sum(roofs[(i+j)%m] for j in range(k)))) for i in range(m)]
    return sum(lengths)/sum(roofs)

def law(roofs: tuple[F, ...], t: F) -> list[F]:
    ts = [F(1)] + [tail(roofs, t, k) for k in range(1, int(t/min(roofs))+3)]
    ps = [ts[i]-ts[i+1] for i in range(len(ts)-1)]
    while ps and ps[-1] == 0:
        ps.pop()
    return ps

def chord_integrals(R: float, T: float = .11) -> dict[str, float]:
    """Independent oriented-line coordinates, not the author's sector grid.

    theta is the line direction relative to one nearest-neighbour centre;
    c is the transverse offset centred between the two disks.  Section flux
    is dtheta dc/(4*pi*R).  The integral in c is performed analytically.
    """
    if not 0 < R < .5 or not 0 < T < 2*(1-2*R):
        raise ValueError('Requires a short window below two inter-disk gaps')
    g = 1-2*R
    if T <= g:
        return dict(R=R, T=T, J=0., Jp=0., bulk_Jpp=0., level_Jpp=0.)
    cmin = (1+T*T-4*R*R)/(2*T)
    if not 0 < cmin < 1:
        raise ValueError('This independent chart uses positive forward projection')
    theta_max = math.acos(cmin)
    def geometry(theta: float) -> tuple[float, float, float, float, float]:
        s, C = math.sin(theta), math.cos(theta)
        D = C-T
        U = 1-2*T*C+T*T
        a = s/2
        c = D/2*math.sqrt(max(0., (4*R*R-U)/U))
        return s, D, a, c, C
    def antiderivative(x: float) -> float:
        h = math.sqrt(max(0., R*R-x*x))
        return .5*(x*h+R*R*math.asin(max(-1., min(1., x/R))))
    def jtheta(theta: float) -> float:
        _, D, a, c, _ = geometry(theta)
        return -2*c*D + 2*(antiderivative(c+a)-antiderivative(-c+a))
    J = 3/(math.pi*R)*quad(jtheta, 0., theta_max, epsabs=2e-13, epsrel=2e-10, limit=150)[0]
    def jptheta(theta: float) -> float:
        _, _, a, c, _ = geometry(theta)
        return math.asin((c+a)/R)-math.asin((-c+a)/R)
    Jp = -J/R + 6/math.pi*quad(jptheta, 0., theta_max, epsabs=1e-12, epsrel=2e-10, limit=150)[0]
    def bulk(theta: float) -> float:
        s, _, a, c, _ = geometry(theta)
        def G(u: float) -> float:
            return u/(R*R*math.sqrt(R*R-u*u))
        return -3/(math.pi*R)*s*s*(G(c+a)-G(-c+a))
    bulk_pp = quad(bulk, 0., theta_max, epsabs=1e-11, epsrel=2e-10, limit=150)[0]
    def level_transformed(t: float) -> float:
        # theta=theta_max*sin(t) removes the inverse square-root endpoint.
        theta = theta_max*math.sin(t)
        s, _, a, c, _ = geometry(theta)
        total = 0.
        for cr in (-c, c):
            b, u = cr-a, cr+a
            h0, h1 = math.sqrt(R*R-b*b), math.sqrt(R*R-u*u)
            tau_prime_section = -(h0*h1+R*R-u*b)/(R*h1)
            derivative_c = b/h0+u/h1
            total += tau_prime_section**2/abs(derivative_c)
        return 3/(math.pi*R)*total*theta_max*math.cos(t)
    level_pp = quad(level_transformed, 0., math.pi/2, epsabs=2e-9, epsrel=2e-9, limit=150)[0]
    area = math.sqrt(3)/2-math.pi*R*R
    lam = 2*R/area
    lamp = 2*(math.sqrt(3)/2+math.pi*R*R)/area**2
    p2 = lam*J
    p1 = lam*T-2*p2
    return dict(R=R,T=T,J=J,Jp=Jp,bulk_Jpp=bulk_pp,level_Jpp=level_pp,
                Jpp=bulk_pp+level_pp,p0=1-p1-p2,p1=p1,p2=p2,p2p=lamp*J+lam*Jp)

def run() -> dict[str, Any]:
    # Algebraic norm: an exact identity, followed by finite nonzero examples.
    k,m,n = sp.symbols('k m n', integer=True)
    norm = sp.prod(k+sm*m*sp.sqrt(2)+sn*n*sp.sqrt(3) for sm in (-1,1) for sn in (-1,1))
    polynomial = (k*k+2*m*m-3*n*n)**2-8*k*k*m*m
    check('exact_biquadratic_norm_identity', sp.expand(norm-polynomial)==0)
    samples = [(a,b,c) for a in range(-5,6) for b in range(-4,5) for c in range(-4,5) if (b,c)!=(0,0)]
    vals = [(a*a+2*b*b-3*c*c)**2-8*a*a*b*b for a,b,c in samples]
    check('finite_nonzero_integer_norms', all(v != 0 for v in vals), {'triples':len(vals),'min_absolute_norm':min(map(abs,vals))})
    dZ,dC,v,M,A = 3,1,F(6),F(8),F(2)
    d = dZ+dC
    exp = v-A*(M-dC)
    check('strict_fourier_tail_budget', exp < -F(d,2)-1, {'tail_power':str(exp),'target_power':str(-F(d,2)-1)})
    boundary_A = (v+F(d,2)+1)/(M-dC)
    check('equality_budget_is_only_big_O_envelope', v-boundary_A*(M-dC)==-F(d,2)-1)
    check('cosine_margin_exact', (1-2*F(47,100)-F(11,100)**2)/(2*F(47,100)*F(11,100))==F(479,1034))
    check('window_and_witness_exact', F(1,10)<F(11,100)<2*F(3,50) and F(9,10)*F(9,1000)/4000000>F(1,10**9))
    roofs1 = tuple(map(F,(1,1,2,2)))
    roofs2 = tuple(map(F,(1,2,1,2)))
    pairs = [(rs,t,j) for rs in (roofs1,roofs2,(F(7,100),F(9,100),F(8,100))) for t in (F(3,2),F(5,2),F(11,100)) for j in range(1,38)]
    check('exact_tail_vs_direct_suspension_lengths', all(tail(rs,t,j)==direct_tail(rs,t,j) for rs,t,j in pairs), {'comparisons':len(pairs)})
    two_laws = [law(rs,F(3,2)) for rs in (roofs1,roofs2)]
    check('same_two_event_laws_with_different_dependence', two_laws[0]==two_laws[1]==[F(1,6),F(2,3),F(1,6)])
    tails3 = [tail(rs,F(5,2),3) for rs in (roofs1,roofs2)]
    check('different_three_event_tail_exact', tails3 == [F(1,12),F(0)], list(map(str,tails3)))
    # Algebraic identity at fixed angular section coordinates.
    R,b0,s0 = sp.symbols('R b0 s0', real=True)
    D = R*R-(b0-R*s0)**2
    hpp_numerator = sp.expand(sp.diff(D,R,2)*D/2-sp.diff(D,R)**2/4)
    check('roof_second_derivative_numerator_exact', sp.expand(hpp_numerator+b0*b0)==0)
    rows = []
    for r in (.45,.455,.46,.465,.47):
        row = chord_integrals(r)
        h = 2e-6
        lo,hi = chord_integrals(r-h),chord_integrals(r+h)
        fd1 = (hi['J']-lo['J'])/(2*h)
        fd2 = (hi['Jp']-lo['Jp'])/(2*h)
        row.update(finite_difference_Jp=fd1, finite_difference_Jpp=fd2)
        check(f'positive_probabilities_and_strict_response_R={r}', min(row[x] for x in ('p0','p1','p2','p2p'))>0 and row['p2']>1e-9)
        check(f'first_response_R={r}', abs(fd1-row['Jp'])<1e-7, abs(fd1-row['Jp']))
        check(f'second_response_with_coarea_R={r}', abs(fd2-row['Jpp'])<2e-5, {'fd':fd2,'bulk_plus_level':row['Jpp'],'absolute_error':abs(fd2-row['Jpp'])})
        check(f'level_term_not_optional_R={r}', row['bulk_Jpp']<0 < row['level_Jpp'] and abs(fd2-row['bulk_Jpp'])>1)
        rows.append(row)
    r=.46;g=1-2*r;target=3/(2*math.sqrt(g))
    threshold=[]
    for eps in (1e-3,3e-4,1e-4,3e-5):
        z=chord_integrals(r,g+eps)
        threshold.append({'epsilon':eps,'J_over_epsilon_squared':z['J']/eps**2,'leading_coefficient':target})
    check('onset_coefficient_convergence_floating', abs(threshold[-1]['J_over_epsilon_squared']/target-1)<5e-4, threshold)
    return {'reviewed_commits':{'revision_carrier':'7f1bc9a42ba27615aea61afb9a417ef076e2c6e1','a2_round33_last_change':'7bb555662a572bd400fbfb0d6011a812ad578593','two_collision_note':'e8d3b658ead4996dabfc9f31a07b812e070f5446'},
            'limits':'Finite exact diagnostics and floating non-interval quadrature; not proof assistance, full billiard simulation, author-test replay, PDF build, or remote CI.',
            'python':platform.python_version(),'numpy':np.__version__, 'sympy':sp.__version__,
            'checks':CHECKS,'passed':sum(x['passed'] for x in CHECKS),'total':len(CHECKS),
            'short_window_laws':[[str(x) for x in y] for y in two_laws], 'longer_window_third_tails':list(map(str,tails3)),
            'quadrature':rows,'threshold_asymptotics':threshold}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    out=run();out['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(f"{out['passed']}/{out['total']} independent diagnostics passed; output: {a.output}")
