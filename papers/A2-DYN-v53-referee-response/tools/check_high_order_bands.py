#!/usr/bin/env python3
"""Finite algebra and chronology checks only; no continuum proof certification."""
from __future__ import annotations
from fractions import Fraction as F
from math import comb
import numpy as np


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def nonsingleton_partitions(limit: int = 32) -> list[list[int]]:
    a = [[0] * (limit + 1) for _ in range(limit + 1)]
    a[0][0] = 1
    for n in range(1, limit + 1):
        for b in range(1, n // 2 + 1):
            a[n][b] = sum(comb(n-1, k-1) * a[n-k][b-1]
                          for k in range(2, n+1))
    return a


def exact_moment_checks() -> tuple[int, int]:
    a = nonsingleton_partitions()
    require((a[4][1], a[4][2]) == (1, 3), 'fourth moment partition recovery')
    require((a[6][1], a[6][2], a[6][3]) == (1, 25, 15), 'sixth moment partition recovery')
    for p in range(1, 17):
        require(all(a[2*p][b] == 0 for b in range(p+1, 33)), 'too many nonsingleton blocks')
        require(a[2*p][1] == 1, 'missing connected residual term')
        require(a[2*p][p] == int(np.prod(np.arange(1, 2*p, 2), dtype=object)),
                'pair partition number')
    cases = 0
    for delta in (F(1, 3), F(1, 5), F(1, 20)):
        moments = [F(1)] + [delta if j % 2 == 0 else F(0) for j in range(1, 33)]
        cumulants = [F(0)] * 33
        for n in range(1, 33):
            cumulants[n] = moments[n] - sum(F(comb(n-1, k-1))*cumulants[k]*moments[n-k]
                                            for k in range(1, n))
        law = {0: F(1)}
        for m in range(1, 6):
            next_law: dict[int, F] = {}
            for x, prob in law.items():
                for y, mass in ((-1, delta/2), (0, 1-delta), (1, delta/2)):
                    next_law[x+y] = next_law.get(x+y, F(0)) + prob*mass
            law = next_law
            reconstructed = [F(1)] + [F(0)]*32
            for n in range(1, 33):
                reconstructed[n] = sum(F(comb(n-1,k-1))*m*cumulants[k]*reconstructed[n-k]
                                       for k in range(1,n+1))
                direct = sum(prob*x**n for x,prob in law.items())
                require(reconstructed[n] == direct, 'exact iid cumulant-moment identity')
                cases += 1
    return cases, a[32][16]


def heterogeneous_checks() -> int:
    for e in (F(0), F(1,4), F(1,2), F(-1,3)):
        samples = [((F(x), F(2*x), F(y), F(3*y)), (1+e*x*y)/4)
                   for x in (-1,1) for y in (-1,1)]
        def moment(indices: tuple[int, ...]) -> F:
            result = F(0)
            for values, prob in samples:
                product = F(1)
                for i in indices: product *= values[i]
                result += prob*product
            return result
        require(all(moment((i,)) == 0 for i in range(4)), 'heterogeneous centering')
        k4 = moment((0,1,2,3))-moment((0,1))*moment((2,3)) \
             -moment((0,2))*moment((1,3))-moment((0,3))*moment((1,2))
        require(k4 == -12*e*e, 'heterogeneous partition subtraction')
    return 4


def chronological_checks() -> int:
    d = 5
    transfer = np.zeros((d,d), dtype=complex)
    for i in range(d): transfer[(i+1)%d, i] = 1
    phase = np.exp(0.17j * np.array([-0.8, 0.1, 0.4, 0.9, -0.6]))
    residual = np.array([0.2, -0.3, 0.4, -0.1, 0.6])
    mark = np.array([0.2+0.1j, -0.4+0.3j, 0.7-0.2j, 0.5+0.4j, -0.1-0.5j])
    twist = transfer @ np.diag(phase)
    cases = 0
    for m in (1, 3, 7, 11):
        powers = [np.linalg.matrix_power(twist, k) for k in range(m+1)]
        for j in range(32):
            for pattern in range(3):
                times = [0 if pattern == 0 else m-1 if pattern == 1 else (2*i+1)%m
                         for i in range(j)]
                for mark_time in (0, m//2, m):
                    events = sorted([(t, residual) for t in times] + [(mark_time, mark)], key=lambda x:x[0])
                    state = np.ones(d, dtype=complex)/d
                    prev = 0
                    lengths = []
                    for time, multiplier in events:
                        lengths.append(time-prev)
                        state = multiplier * (powers[time-prev] @ state)
                        prev = time
                    lengths.append(m-prev)
                    actual = np.sum(powers[m-prev] @ state)
                    direct = 0j
                    for x in range(d):
                        term = mark[(x+mark_time)%d]
                        for t in range(m): term *= phase[(x+t)%d]
                        for t in times: term *= residual[(x+t)%d]
                        direct += term/d
                    require(sum(lengths) == m and min(lengths) >= 0, 'lost chronological length')
                    require(2*len(events) <= 64, 'wrong multiplier exponent at P=16')
                    require(abs(actual-direct) < 5e-13, 'chronological pairing differs from orbit product')
                    cases += 1
    return cases


def feasible_orders(theta: tuple[F, F, F, F], eta: F) -> tuple[F, int, int, int]:
    t, vol = max(theta), sum(theta)
    require(min(theta) >= F(1,200), 'box omits inherited small ball')
    require(t < F(1,10), 'no strict coarse-scale interval')
    require(0 < eta <= F(1,4)-vol-t, 'no stopping rate budget')
    alpha = (2*t + F(1,4)-t/2)/2
    p = int((vol+eta)//(alpha-2*t)) + 1
    s = F(1,2)-t
    q = max(3, int((s+2*alpha)//(s-2*alpha))+1)
    beta = int((vol+(2*p-1)*(F(1,2)+t)+eta)//1)+1
    require(2*t < alpha < F(1,4)-t/2, 'bad coarse-scale choice')
    require(p*(alpha-2*t) > vol+eta, 'nonpositive residual margin')
    require((q-1)*s > 2*alpha*(q+1), 'nonpositive Taylor-domain margin')
    return alpha,p,q,beta


def finite_checks() -> dict:
    cases, pair32 = exact_moment_checks()
    heterogeneous = heterogeneous_checks()
    words = chronological_checks()
    theta = (F(1,100),F(1,100),F(1,100),F(9,100))
    t, vol, alpha, p, q, beta = max(theta), sum(theta), F(19,100), 16, 29, F(20)
    eta = F(1,40)
    ledger = {
        'analytic_disk': F(1,2)-t-2*alpha,
        'spectral_Taylor_domain': (q-1)*(F(1,2)-t)-2*alpha*(q+1),
        'fine_insertion': beta-vol,
        'fine_residual': beta-vol-(2*p-1)*(F(1,2)+t),
        'paired_residual': p*(alpha-2*t)-vol,
        'actual_stopping': F(1,4)-vol-t,
    }
    require(list(ledger.values()) == [F(3,100),F(2,25),F(497,25),F(159,100),F(1,25),F(1,25)],
            'concrete exponent ledger differs')
    residuals = []
    for b in range(1,p+1):
        decay = p-2*p*t-vol-(1-alpha)*b
        require(decay > eta, 'a residual/log term cannot be absorbed')
        residuals.append({'blocks':b,'decay':str(decay),'log_power':2*p-b,'slack':str(decay-eta)})
    require(eta > F(3,280) and ledger['fine_insertion'] > F(9,175), 'central rate lost')
    require(F(9,100) > F(67,1400) and F(9,100) < F(1,10), 'extension misidentified')
    # Volume is the sum of four separate exponents, not four times the largest.
    require(vol == F(3,25) and vol != 4*t, 'anisotropic volume accounting')
    count_power = F(1,2)+theta[2]
    require(count_power == F(51,100) and count_power != F(1,2)+theta[3], 'wrong count-kernel coordinate')
    require(2*min(theta) == F(1,50), 'Gaussian complement scale')
    for requested in (1,3,10,50):
        J = int((vol+requested)//count_power)+1
        require(vol-count_power*J < -requested, 'Schwartz count separation failed')
    width_cases = [
        theta,
        (F(67,1400),)*4,
        (F(1,100),F(1,100),F(7,100),F(7,100)),
        (F(1,200),F(1,200),F(1,200),F(99,1000)),
    ]
    orders = []
    for widths in width_cases:
        e = (F(1,4)-sum(widths)-max(widths))/2
        order = feasible_orders(widths,e)
        orders.append({'widths':[str(x) for x in widths],'eta':str(e),
                       'alpha':str(order[0]),'P':order[1],'Q':order[2],'beta':order[3]})
    invalid = [
        ((F(1,100),F(1,100),F(1,100),F(1,10)), F(1,100)),
        ((F(7,100),)*4, F(1,100)),
        ((F(1,1000),F(1,100),F(1,100),F(9,100)), F(1,100)),
    ]
    for widths,e in invalid:
        try: feasible_orders(widths,e)
        except RuntimeError: pass
        else: raise RuntimeError('invalid width budget escaped rejection')
    # Neither the box nor its union with the old ball covers the full target ball.
    uncovered_axis = F(2,25)
    require(theta[0] < uncovered_axis and F(67,1400) < uncovered_axis < F(1,10),
            'unsupported full annulus claim')
    # Cubic remainder cannot establish this concrete extension at any permitted alpha.
    require(2*(F(1,4)-t/2-2*t)-vol < 0, 'negative control for residual order two')
    return {'residual_moment_order':32,'residual_Taylor_degree':31,'spectral_degree':29,
            'partition_orders_checked':16,'pair_partitions_at_order_32':pair32,
            'exact_iid_moment_cases':cases,'heterogeneous_cases':heterogeneous,
            'finite_chronological_words':words,
            'concrete_exponents':{k:str(v) for k,v in ledger.items()},
            'all_residual_powers':residuals,'feasible_width_examples':orders,
            'invalid_width_negative_controls':len(invalid),
            'additional_negative_controls':['cubic order insufficient in concrete box','wrong roof versus count coordinate','union is not full isotropic ball'],
            'raw_jacobian':'dv = n^2 dz','kernel_volume_power':str(vol),
            'kernel_count_separation_power':str(count_power),'Gaussian_tail_power':'1/50',
            'finite_models_are_not_continuum_proofs':True}


if __name__ == '__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
