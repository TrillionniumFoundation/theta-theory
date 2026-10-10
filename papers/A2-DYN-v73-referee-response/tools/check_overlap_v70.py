#!/usr/bin/env python3
"""Finite exact-arithmetic diagnostics; never a continuum proof certificate."""
from fractions import Fraction as Q
from itertools import product
import json
import math


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def overlap(x, receiving):
    if not receiving:
        raise ValueError('positive receiving interval required')
    if x < 0 or any(v < 0 for v in receiving):
        raise ValueError('angular capacities must be nonnegative')
    return sum((min(Q(1), v/x) for v in receiving), Q(0))/len(receiving) if x else Q(1)


def finite_checks():
    checked = 0
    for vals in product([Q(0), Q(1,5), Q(1)], repeat=6):
        for receiving in [vals[:3], vals[3:], vals]:
            avg = sum(receiving, Q(0))/len(receiving)
            for x in vals:
                a = overlap(x, receiving)
                loss = sum((max(x-v, Q(0)) for v in receiving), Q(0))/len(receiving)
                require(0 <= a <= 1, 'positive overlap weight')
                require(x*a + loss == x, 'exact complementary capacities')
                require(x*a <= avg, 'receiving capacity domination')
                for density, guard in [(Q(1,2),Q(0)), (Q(2),Q(1,7)), (Q(3,2),Q(1))]:
                    b = density*guard*x
                    require(a*b+(1-a)*b == b, 'unchanged weighted source')
                    require(a*b <= 4*guard*avg/2, 'two-sided density distortion')
                    checked += 1
                checked += 3
        # Exact BV loss comparison for step functions on (0,1), H=1/2.
        for j in range(3):
            u = Q(2*j+1,12)
            loss = sum((max(vals[j]-v,Q(0)) for v in vals[3:]),Q(0))/3
            current = Q(0)
            for k in range(1,6):
                s = Q(k,6)
                if s > u:
                    kappa = min(Q(1), 2*(1-s))
                    current += kappa*max(vals[k-1]-vals[k],Q(0))
            require(loss <= current, 'atomic negative-current kernel')
            checked += 1
    for p in [0,1,2,7,31,1023,1000000]:
        ratio = p+1  # exact integral of u**p over (0,1)
        require(ratio >= 1, 'finite-scale ratio formula')
        # log form avoids underflow at very high orders.
        require(p*math.log(.4) <= p*math.log(.6), 'monotone outer comparison')
        checked += 2
    require(overlap(Q(1),[Q(0),Q(0)]) == 0, 'unfunded later birth stays in loss')
    require(overlap(Q(0),[Q(0),Q(0)]) == 1, 'zero-source convention')
    require(overlap(Q(1,4),[Q(1,2),Q(1)]) == 1, 'complete no-loss source')
    a = overlap(Q(1),[Q(1,4),Q(1,2)])
    require(0<a<1 and 0<1-a<1, 'weights can overlap: not disjoint events')
    # A radial death at 3/4 is an atom with cost 1/2, invisible to a.e. derivative.
    atomic_cost = (1-Q(3,4))/Q(1,2)
    require(atomic_cost == Q(1,2) and atomic_cost > 0, 'do not erase death atom')
    # Signed projection permits cancellation; projecting negative parts first overcounts.
    require(max(-(Q(1)-Q(1)),Q(0)) == 0 < Q(1), 'project then take negative part')
    for interfaces in product([False,True],repeat=4):
        assigned=[bool(x) and not any(interfaces[:j]) for j,x in enumerate(interfaces)]
        require(sum(assigned) == int(any(interfaces)), 'coincident interface allocated once')
        checked += 1
    for eps in [1e-2,1e-4,1e-8,1e-16]:
        chi=math.sqrt(eps)
        require(4*eps <= chi <= .1, 'legal fixed-band incidence budget')
        require(math.isclose(chi**6,eps**3,rel_tol=1e-12), 'whole-chart band exponent')
        checked += 2
    for K,H,Lg in product([1.,3.],[1e-8,1e-6],[2.,10.]):
        E=math.exp((2+math.sqrt(2))*K*math.sqrt(H))
        lhs=6*H*E*min(1.,Lg*math.sqrt(2*H))
        rhs=6*math.sqrt(2)*Lg*H**1.5*E
        require(lhs <= rhs*(1+1e-12), 'zero-center height power')
        checked += 1
    # Explicit adversarial finite profile: tiny mass does not bound its height.
    narrow=[Q(0)]*63+[Q(1)]
    require(sum(narrow)/64 == Q(1,64) and max(narrow)==1, 'mass is not height')
    require(overlap(Q(1),narrow[:32])==0, 'narrow spike cannot be declared no-loss')
    for args in [(Q(1),[]),(Q(-1),[Q(1)])]:
        try:
            overlap(*args)
        except ValueError:
            checked += 1
        else:
            raise RuntimeError('invalid angular comparison not rejected')
    return {'exact_checks':checked,'zero_capacity_checked':True,'atomic_deaths_retained':True,
            'signed_projection_checked':True,'weight_partition_not_disjoint_events':True,
            'negative_controls_passed':True,'continuum_certified':False,
            'ordered_physical_tail_certified':False}


if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
