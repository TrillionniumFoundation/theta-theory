#!/usr/bin/env python3
"""Independent exact finite diagnostics for the A2 v28 referee report.

Standard library only. No assertion is removed by python -O. These tests
are not proofs of half-line convergence, physical realizability, full
native compilation, analytic continuation, or statistical equivalence.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

REVIEWED_COMMIT = 'f5fcd5e319cb4a37bdcbf8d9f9d190786ec7fc7d'
COUNTS: Counter[str] = Counter()


def check(condition: bool, group: str) -> None:
    if not condition:
        raise RuntimeError('Independent diagnostic failed: ' + group)
    COUNTS[group] += 1


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def mv(a, x):
    return tuple(sum(row[j] * x[j] for j in range(len(x))) for row in a)


def transpose(a):
    return tuple(zip(*a))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse(a):
    d = det(a)
    if not d:
        raise ValueError('Singular matrix')
    return ((a[1][1]/d, -a[0][1]/d), (-a[1][0]/d, a[0][0]/d))


def affine(t, shift):
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    return ((c, -s, shift[0]), (s, c, shift[1]), (Q(0), Q(0), Q(1)))


def run():
    I2 = ((Q(1), Q(0)), (Q(0), Q(1)))
    J2 = ((Q(1), Q(0)), (Q(0), Q(-1)))
    J3 = ((Q(1), Q(0), Q(0)), (Q(0), Q(-1), Q(0)),
          (Q(0), Q(0), Q(1)))
    motions = [affine(t, shift) for t in (Q(0), Q(1,3), Q(-2,5))
               for shift in ((Q(0), Q(0)), (Q(2,7), Q(-3,5)))]
    for A, B in product(motions, repeat=2):
        Ar, Br = mm(mm(J3, A), J3), mm(mm(J3, B), J3)
        check(mm(Br, Ar) == mm(mm(J3, mm(B, A)), J3),
              'affine_root_change_and_composition_equivariance')
        check(mm(mm(J3, Ar), J3) == A, 'affine_reflection_involution')
        check(det(tuple(row[:2] for row in Ar[:2])) == 1,
              'proper_affine_placement')
    for L in (((Q(2), Q(1,3)), (Q(0), Q(3))),
              ((Q(3), Q(-1,2)), (Q(1,4), Q(2)))):
        for M in (((Q(1), Q(0)), (Q(0), Q(1))),
                  ((Q(2), Q(1)), (Q(0), Q(3))),
                  ((Q(1), Q(3)), (Q(2), Q(1)))):
            V = mm(L, M)
            Lr = mm(mm(J2, V), inverse(M))
            check(Lr == mm(J2, L), 'nonprimitive_rank_two_reflection')
            check(mm(transpose(Lr), Lr) == mm(transpose(L), L),
                  'gram_and_scale_preserved')
            check(det(Lr) == -det(L), 'lattice_character_transported')
    # Local densities: normalization cancels, and every denominator is positive.
    d, a, Z = Q(3,2), Q(1,5), Q(7,3)
    S = lambda u: u*u/2 + u**3/7 + u**4/11
    B = lambda u: 1 + u/10 + u*u/9
    f = lambda u,v: B(u)*B(v)*(d-S(u)-S(v))/Z
    def ratio(fun,u,v):
        return fun(u,v)*fun(Q(0),Q(0))/(fun(u,Q(0))*fun(Q(0),v))
    for u,v in product((Q(i,20) for i in range(-5,6)), repeat=2):
        t, z = S(u)/(d-S(u)), S(v)/(d-S(v))
        check(1-ratio(f,u,v) == t*z, 'asymmetric_four_density_identity')
        qa = S(a)/(d-S(a))
        check(qa > 0 and qa*qa == 1-ratio(f,a,a), 'positive_scalar_anchor')
        T = (1-ratio(f,u,a))/qa
        check(d*T/(1+T) == S(u), 'exact_action_inverse')
        check(f(u,Q(0))/f(Q(0),Q(0))*(1+T) == B(u)/B(Q(0)),
              'normalized_amplitude_inverse')
        fr = lambda x,y: f(-x,-y)
        qar = S(-a)/(d-S(-a))
        Tr = (1-ratio(fr,u,a))/qar
        check(d*Tr/(1+Tr) == S(-u), 'exact_inverse_reflection_covariance')
    # Determinant-one blocks, restricting leading parameters to positive curvatures.
    for q,r,g in product((Q(1,4),Q(1,3),Q(1,2)),
                         (Q(3,4),Q(1),Q(4,3)), (Q(1,2),Q(1),Q(2))):
        c,h = (q+1/q)/2, (1/q-q)/2
        if c*r <= 1 or c/r <= 1:
            continue
        a0,a1 = r*h/g,h/(r*g)
        check(c*c-h*h == 1 and g*g*a0*a1 == h*h,
              'positive_leading_geometry_identity')
        for n in range(3,16):
            z = q**n
            co,cs = (1+z*z)/(1-z*z), 2*z/(1-z*z)
            Mn = ((co,r**n*cs),(r**(-n)*cs,co))
            Ni = ((co,-r**n*cs),(-r**(-n)*cs,co))
            check(det(Mn) == 1 and mm(Mn,Ni) == I2, 'last_jet_block_inverse')
            vec = (Q(2,7),Q(-3,11))
            reflected = tuple((-1)**n*x for x in vec)
            check(mv(Mn,reflected) == tuple((-1)**n*x for x in mv(Mn,vec)),
                  'homogeneous_last_jet_parity')
    # Functional-density examples, explicitly not physical-table counterexamples.
    for alpha in (Q(1,20),Q(1,10),Q(1,5)):
        for u,v in product((Q(i,6) for i in range(1,6)), repeat=2):
            ff = lambda x,y,k: (1+k*alpha*(x+y))/4
            check(1-4*alpha > 0, 'folded_example_positive')
            for k in (1,2):
                check(sum(ff(s*u,t*v,k) for s,t in product((-1,1),repeat=2)) == 1,
                      'folded_example_same_density')
                check(ff(u,v,k)+ff(-u,-v,k) == Q(1,2),
                      'samplewise_common_orbit_also_coarsens')
            check(ff(u,v,2) not in (ff(u,v,1),ff(-u,-v,1)),
                  'different_law_orbits')
    # New boundary of application: a fixed-anchor off-model extension is not
    # equivariant. On the disk, f_e = (2/pi)(1-u^2-v^2)_+
    # * (1+e*u*v*(u+v)) is normalized (the perturbation is odd under reversal).
    # Normalization cancels below. D=t(a)^2, h=2e*a^3 R0(a,a).
    witnesses = []
    for anchor,e in product((Q(1,5),Q(1,4)), (Q(1,200),Q(1,100),Q(1,50))):
        D = (anchor*anchor/(1-anchor*anchor))**2
        R0 = 1-D
        h = 2*e*anchor**3*R0
        check(D-h > 0 and h != 0, 'noisy_anchor_domain')
        left_sq = D+h
        right_sq = D*D/(D-h)
        check(left_sq-right_sq == -h*h/(D-h) and left_sq != right_sq,
              'fixed_anchor_off_model_nonequivariance_witness')
        if anchor == Q(1,4) and e == Q(1,100):
            witnesses.append({'anchor':str(anchor),'epsilon':str(e),
                              'D':str(D),'h':str(h),
                              'T_a_reflected_density_at_a_squared':str(left_sq),
                              'reflected_T_a_density_at_a_squared':str(right_sq),
                              'difference':str(left_sq-right_sq)})
        fe = lambda u,v: (1-u*u-v*v)*(1+e*u*v*(u+v))
        fre = lambda u,v: fe(-u,-v)
        for u in (Q(-1,6),Q(0),Q(1,7)):
            # Squared T equality, plus numerator signs, checks anchor transport
            # without numerical square roots: F_-a(r*f) = r*F_a(f).
            lhs = (1-ratio(fre,u,-anchor))**2/(1-ratio(fre,-anchor,-anchor))
            rhs = (1-ratio(fe,-u,anchor))**2/(1-ratio(fe,anchor,anchor))
            check(lhs == rhs and 1-ratio(fre,u,-anchor) == 1-ratio(fe,-u,anchor),
                  'transported_anchor_restores_covariance')
    # Tagged common orbits meet either orientation sector exactly once,
    # including reversal-invariant laws. This is not an untagged sign erasure.
    for x in ((Q(0),Q(0)),(Q(1,3),Q(-1,5)),(Q(2),Q(3))):
        for eps in (-1,1):
            orbit = {(eps,x),(-eps,tuple(-z for z in x))}
            check(len(orbit)==2 and sum(e==1 for e,_ in orbit)==1,
                  'tagged_orbit_and_symmetric_law_edge_case')
    return {'reviewed_commit':REVIEWED_COMMIT,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'Exact finite diagnostics, not a physical inverse or native-build certificate.',
            'arithmetic':'fractions.Fraction; no floating point',
            'checks':dict(sorted(COUNTS.items())),
            'total_checks':sum(COUNTS.values()),
            'fixed_anchor_witness':witnesses, 'status':'passed'}


if __name__ == '__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
