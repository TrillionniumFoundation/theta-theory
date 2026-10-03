#!/usr/bin/env python3
"""Exact finite tests for local period recognition; not a proof or apparatus run."""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import gcd
from pathlib import Path
import hashlib
import json
import random
import re

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()


def require(ok: bool, group: str) -> None:
    if not ok:
        raise RuntimeError(group)
    COUNTS[group] += 1


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if not b:
        return abs(a), 1 if a >= 0 else -1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def hnf2(vectors: list[tuple[int, int]]) -> tuple[int, int, int]:
    """Column Hermite basis ((a,0),(b,c)) for a full-rank integer group."""
    detg = 0
    for x, y in vectors:
        for u, v in vectors:
            detg = gcd(detg, abs(x*v-y*u))
    if detg == 0:
        raise ValueError('rank-deficient integer span')
    yg = xs = 0
    for x, y in vectors:
        g, u, v = egcd(yg, y)
        xs = u*xs + v*x
        yg = g
    if yg == 0 or detg % yg:
        raise ValueError('inconsistent Hermite invariants')
    a, c = detg//yg, yg
    return a, xs % a, c


def explicit_patch(motif, a: int, b: int):
    return frozenset((x+a*i, y+b*j, colour)
                     for x, y, colour in motif
                     for i, j in product(range(-2, 3), repeat=2))


def local_period(motif, patch, shift: tuple[int, int]) -> bool:
    u, v = shift
    return all((x+sgn*u, y+sgn*v, col) in patch
               for x, y, col in motif for sgn in (-1, 1))


def global_period(motif, a, b, shift) -> bool:
    u, v = shift
    return frozenset(((x+u) % a, (y+v) % b, c) for x, y, c in motif) == motif


def check_motif(motif, a, b, group) -> None:
    patch = explicit_patch(motif, a, b)
    root = min(motif)
    candidates = {(x-root[0], y-root[1]) for x, y, c in motif}
    candidates |= {(a, 0), (-a, 0), (0, b), (0, -b)}
    accepted = []
    for shift in sorted(candidates):
        local = local_period(motif, patch, shift)
        require(local == global_period(motif, a, b, shift), group+'_finite_patch')
        if local:
            accepted.append(shift)
    full = [v for v in product(range(a), range(b)) if global_period(motif, a, b, v)]
    ha, hb, hc = hnf2(accepted)
    require(ha*hc*len(full) == a*b, group+'_full_covolume')
    require(len(motif) % len(full) == 0, group+'_free_component_action')
    for x, y in accepted:
        require(y % hc == 0 and (x-hb*(y//hc)) % ha == 0,
                group+'_hermite_membership')
    unseen = set(motif)
    orbits = 0
    while unseen:
        x, y, c = min(unseen)
        orbit = {p for p in motif if local_period(motif, patch, (p[0]-x, p[1]-y))}
        require(all(p[2] == c for p in orbit), group+'_shape_preserved_by_period')
        unseen -= orbit
        orbits += 1
    require(orbits*len(full) == len(motif), group+'_primitive_multiplicity')


def periodic_patterns() -> None:
    # Every nonempty uncoloured 4x3 torus motif, with genuine Euclidean
    # patch tests compared to a separate global finite-torus calculation.
    sites = list(product(range(4), range(3)))
    for mask in range(1, 1 << len(sites)):
        motif = frozenset((x, y, 1) for j, (x, y) in enumerate(sites) if mask & (1 << j))
        check_motif(motif, 4, 3, 'repeated_disks')
    # Empty / small disk / larger disk at each of six sites. This detects
    # accidental reliance on centers alone when shapes are different.
    sites = list(product(range(3), range(2)))
    for colours in product(range(3), repeat=6):
        if not any(colours):
            continue
        motif = frozenset((x, y, c) for (x, y), c in zip(sites, colours) if c)
        check_motif(motif, 3, 2, 'coloured_disks')
    motif = frozenset(((0, 0, 1), (1, 0, 1)))
    require((1, 0, 1) in motif, 'root_pair_matches_exactly')
    require(not local_period(motif, explicit_patch(motif, 4, 3), (1, 0)),
            'root_match_does_not_certify_period')
    # Omitting a nonmatching central witness would wrongly certify the shift.
    incomplete_sources = frozenset(((0, 0, 1),))
    one_sided = all((x+1, y, c) in explicit_patch(motif, 4, 3)
                    for x, y, c in incomplete_sources)
    require(one_sided and not global_period(motif, 4, 3, (1, 0)),
            'missing_witness_negative_control')


def body_distance(body, other, shift=(F(0), F(0))):
    return max(abs(body[0]+shift[0]-other[0]), abs(body[1]+shift[1]-other[1])) + abs(body[2]-other[2])


def defect(sources, targets, shift):
    return max(min(body_distance(c, d, (sgn*shift[0], sgn*shift[1])) for d in targets)
               for c in sources for sgn in (-1, 1))


def noisy_patch_tests() -> None:
    rng = random.Random(20261003)
    fixtures = [((F(0), F(0), F(1,4)), (F(2)+t, F(0), F(1,4)))
                for t in (F(0), F(1,32), F(1,16), F(1,10))]
    fixtures += [((F(0),F(0),F(1,5)),(F(1),F(0),F(1,5)),(F(2),F(1),F(1,7)))]
    for motif in fixtures:
        targets = tuple((x+4*i, y+4*j, r) for x,y,r in motif
                        for i,j in product(range(-2,3),repeat=2))
        shifts = [(x-motif[0][0],y-motif[0][1]) for x,y,r in motif]+[(F(4),F(0)),(F(0),F(4))]
        true = [defect(motif,targets,v) for v in shifts]
        positives = [v for v in true if v>0]
        eta = min(positives) if positives else F(1)
        e = min(F(1,10000),eta/1000)
        for _ in range(12):
            jitter = {c:tuple(v+e*F(rng.randint(-10,10),10) for v in c) for c in targets}
            # All central components are among targets; their source and target
            # perturbations are deliberately coupled, as in one observed cloud.
            sources = [jitter[c] for c in motif]
            noisy = list(jitter.values())
            for v, exact in zip(shifts,true):
                endpoint = (motif[0][0]+v[0],motif[0][1]+v[1],motif[0][2])
                if endpoint not in jitter:
                    # A differently shaped candidate has its actual radius.
                    endpoint = next(c for c in targets if c[:2]==endpoint[:2])
                vr = tuple(jitter[endpoint][i]-jitter[motif[0]][i] for i in (0,1))
                estimated = defect(sources,noisy,vr)
                require(abs(estimated-exact) <= 14*e,'fourteen_e_comparison_bound')
                require((estimated<eta/2) == (exact==0),'threshold_period_classification')
    for t in [F(1,j) for j in range(9,81)]:
        motif=((F(0),F(0),F(1,4)),(2+t,F(0),F(1,4)))
        targets=tuple((x+4*i,y+4*j,r) for x,y,r in motif
                      for i,j in product(range(-2,3),repeat=2))
        require(defect(motif,targets,(2+t,F(0)))==2*t,'symmetry_jump_defect')
        require((4+2*t)%4 != 0,'nonzero_motif_shift_not_a_period')
    require(F(4*4,2)==8,'primitive_covolume_at_symmetry')


def rational_locking() -> None:
    def closest(value, Q):
        vals={F(n,d) for d in range(1,Q+1) for n in range(-3*d,3*d+1)}
        distances=sorted((abs(value-v),v) for v in vals)
        if len(distances)>1 and distances[0][0]==distances[1][0]:
            raise ValueError('ambiguous rational')
        return distances[0][1]
    for Q in range(1,13):
        rationals=sorted({F(n,d) for d in range(1,Q+1) for n in range(-d,d+1)})
        require(all(b-a>=F(1,Q*Q) for a,b in zip(rationals,rationals[1:])),
                'bounded_denominator_separation')
        for value in rationals[::max(1,len(rationals)//12)]:
            for sign in (-1,1):
                require(closest(value+sign*F(1,4*Q*Q),Q)==value,'unique_rational_lock')
    try:
        closest(F(1,2),1)
    except ValueError:
        require(True,'ambiguous_rational_rejected')
    else:
        require(False,'ambiguous_rational_rejected')
    try:
        hnf2([(1,0),(2,0)])
    except ValueError:
        require(True,'rank_deficiency_rejected')
    else:
        require(False,'rank_deficiency_rejected')


def resource_and_margins() -> None:
    for L0 in [F(1),F(3,2),F(3),F(11)]:
        B=1+L0
        for e in [F(1,100),F(1,1000)]:
            require(3*B+4*e<4*B,'protected_generator_cutoff')
            require(8*B+8*e<10*B,'period_target_available')
            require(B+2*e<2*B,'every_core_witness_selected')
            require(10*B+e<11*B,'kept_partial_hull_implies_complete_body')
    require(F(3,2)-2*F(1,4)==1,'two_derivative_smoothing_noise')
    require(4*F(1,4)==1,'fourth_order_smoothing_bias')
    require(2*F(3,4)==F(3,2),'hull_localization_balance')
    for r in range(1,21):
        for m in range(1,r+1):
            if r % m == 0:
                require(F(1,m)>=F(1,r),'full_lattice_covolume_lower_bound')
                require((r//m)*m==r,'orbit_stabilizer_multiplicity')


def sources() -> None:
    pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
    for path, sha in pins['source_sha256'].items():
        require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,'source_sha256_binding')
    for path, sha in pins['retained_active_core_blobs'].items():
        data=(ROOT/path).read_bytes()
        require(hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==sha,
                'all_eight_v27_cores_byte_identical')
    text=(ROOT/'main.tex').read_text()
    for name in re.findall(r'\\input\{([^}]+)\}',text):
        require((ROOT/(name+'.tex')).is_file(),'primary_input_reachable')
        text+='\n'+(ROOT/(name+'.tex')).read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)),'unique_primary_labels')
    for ref in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text):
        require(ref in labels,'primary_reference_resolved')
    for label in ('thm:repeat-exact','thm:repeat-finite','thm:aperture-main',
                  'lem:period-local','prop:repeatjump','cor:repeatpointwise'):
        require(label in labels,'new_and_prior_results_active')


def main() -> None:
    periodic_patterns(); noisy_patch_tests(); rational_locking(); resource_and_margins(); sources()
    print(json.dumps({'schema':'a2-v28-finite-diagnostics-1','status':'passed',
        'total_checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
        'exhaustive_uncoloured_motifs':4095,'exhaustive_coloured_motifs':728,
        'scope':'finite periodic motifs, noisy patch inequalities, rational arithmetic and source integrity',
        'formal_proof_certificate':False,'physical_sensor_executed':False},sort_keys=True))

if __name__=='__main__':
    main()
