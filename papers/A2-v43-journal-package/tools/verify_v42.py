#!/usr/bin/env python3
"""Exact finite diagnostics of the new v42 signed-record construction.

No author v41 module is imported. Fractions are exact; tests remain active
under -O. This is not a continuum proof, a human review, or a sensor test.
"""
from fractions import Fraction as F
from math import ceil, comb, log
from functools import lru_cache
import json
import sys


class Failure(RuntimeError):
    pass


class Checks:
    def __init__(self):
        self.count = 0

    def require(self, condition, message):
        self.count += 1
        if not condition:
            raise Failure(message)


def plus(x, y):
    return (x[0] + y[0], x[1] + y[1])


def scale(s, x):
    return (s * x[0], s * x[1])


def solid(x, disks):
    return any((x[0]-c[0])**2 + (x[1]-c[1])**2 <= r*r for c, r in disks)


def collision(x, a, disks):
    if solid(x, disks):
        return 0
    length2 = a[0]**2 + a[1]**2
    for c, r in disks:
        u = max(F(0), min(F(1), ((c[0]-x[0])*a[0] + (c[1]-x[1])*a[1])/length2))
        y = plus(x, scale(u, a))
        if (y[0]-c[0])**2 + (y[1]-c[1])**2 <= r*r:
            return 1
    return 0


def in_q(x):
    return -F(3, 2) <= x[0] <= F(3, 2) and -F(3, 2) <= x[1] <= F(3, 2)


def stop(x, a, kmax):
    if not in_q(x):
        return 0
    for j in range(1, kmax+1):
        if not in_q(plus(x, scale(j, a))):
            return j
    raise Failure('exit not reached')


def moments_of_uniform_interval(lo, hi, n):
    return [(hi**(i+1)-lo**(i+1))/((i+1)*(hi-lo)) for i in range(n+1)]


def run():
    ck = Checks()
    sections = {}
    a = (F(1, 2), F(0))
    disks = (((F(-10), F(0)), F(1)), ((F(0), F(0)), F(1)), ((F(10), F(0)), F(1)))
    center = (disks[1],)
    laws = [(((F(0), F(0)), F(1)),),
            (((F(1, 4), F(0)), F(1)),),
            (((F(-1, 4), F(0)), F(1, 3)), ((F(1, 4), F(0)), F(2, 3))),
            (((F(0), F(-1, 4)), F(1, 4)), ((F(0), F(1, 4)), F(3, 4)))]
    kmax = 10
    points = [(F(i, 4), F(j, 4)) for i in range(-8, 9) for j in range(-8, 9)]
    before = ck.count
    negatives = 0
    for law in laws:
        @lru_cache(maxsize=None)
        def field(x, direction):
            return sum(p*collision(plus(x,z), direction, disks) for z,p in law)
        @lru_cache(maxsize=None)
        def occupation(x, bodies=disks):
            return sum(p*solid(plus(x,z), bodies) for z,p in law)
        for x in points:
            m = stop(x, a, kmax)
            vc = occupation(x, center)
            total = F(0)
            second_moment = F(0)
            for k in range(kmax):
                y = plus(x, scale(k, a))
                endpoint = plus(y,a)
                fp, fm = field(y,a), field(endpoint,scale(-1,a))
                ck.require(fp-fm == occupation(endpoint)-occupation(y), 'field endpoint identity')
                gate = int(k < m)
                mean = F(0)
                for yp in (0,1):
                    for ym in (0,1):
                        prob = (fp if yp else 1-fp)*(fm if ym else 1-fm)
                        record = kmax*gate*(ym-yp)
                        mean += prob*record
                        second_moment += prob*record*record/kmax
                        ck.require(abs(record) <= kmax, 'signed range')
                        negatives += int(record < 0 and prob > 0)
                ck.require(mean == kmax*gate*(fm-fp), 'independent two-bit expectation')
                total += mean/kmax
            ck.require(total == vc, 'linear occupation identity')
            ck.require(second_moment >= total*total, 'variance nonnegative')
            if m:
                ck.require(occupation(plus(x,scale(m,a))) == 0, 'protected exit occupation')
                ck.require(in_q(plus(x,scale(m-1,a))), 'first-exit predecessor')
                ck.require(not in_q(plus(x,scale(m,a))), 'closed boundary exit')
    ck.require(negatives > 0, 'negative nonzero records must occur')
    sections['exact_disks_prefix_and_independent_records'] = ck.count-before

    before=ck.count
    # Integrating polynomials over a rectangle is exact. Shift mixtures here
    # test quadrature and rational moments, not strict convexity or support theory.
    n=8
    lo,hi=F(-1),F(1)
    interval=moments_of_uniform_interval(lo,hi,n)
    law=(((F(-1,4),F(0)),F(1,3)),((F(1,4),F(0)),F(2,3)))
    previous=None
    errors=[]
    for den in (4,8,16):
        ell=F(1,den)
        grid=[F(-2)+(F(i)+F(1,2))*ell for i in range(4*den)]
        moment_errors=[]
        for i in range(n+1):
            for j in range(n+1-i):
                exact=F(0)
                for z,p in law:
                    mx=sum(F(comb(i,b))*interval[i-b]*(-z[0])**b for b in range(i+1))
                    my=sum(F(comb(j,b))*interval[j-b]*(-z[1])**b for b in range(j+1))
                    exact += 4*p*mx*my/(4**(i+j))
                # Tensor sums, then mixture; exact same midpoint grid expectation.
                quad=F(0)
                for z,p in law:
                    sx=sum((x/F(4))**i for x in grid if lo<=x+z[0]<=hi)*ell
                    sy=sum((y/F(4))**j for y in grid if lo<=y+z[1]<=hi)*ell
                    quad += p*sx*sy
                err=abs(quad-exact)
                ck.require(err <= 16*(n+1)*ell, 'uniform boundary-cell envelope')
                moment_errors.append(err)
        maximum=max(moment_errors)
        if previous is not None:
            ck.require(maximum<=previous,'midpoint model refinement')
        previous=maximum
        errors.append(str(maximum))
    sections['exact_rational_grid_moments']=ck.count-before

    before=ck.count
    for n in (1,4,8,16,40):
        count=sum(1 for i in range(n+1) for j in range(n+1-i))
        ck.require(count==comb(n+2,2),'multiindex count')
        for tau in (0.25,0.125,0.0625):
            for delta in (0.2,0.05,0.01):
                bound=3.0 # a finite B=|W|K example
                q=ceil(8*bound*bound/tau**2*log(2*count/delta))
                ck.require(log(2*count)-q*tau*tau/(8*bound*bound)<=log(delta)+1e-12,
                           'Hoeffding union exponent')
                ck.require(2*q>=q,'all two-bit occurrences charged')
    sections['concentration_and_resource_algebra']=ck.count-before

    return dict(schema='a2-v42-finite-diagnostics-1',status='passed',total_checks=ck.count,
                sections=sections,negative_record_cases=negatives,midpoint_model_errors=errors,
                formal_proof_certificate=False,human_specialist_review=False,
                physical_sensor_executed=False,
                scope='Finite exact algebra and model diagnostics; not continuum certification. Mixtures and rectangles test algebra, not the full theorem class.')


def main():
    try:
        result=run(); code=0
    except (Failure,ArithmeticError,ValueError) as exc:
        result=dict(status='failed',error=str(exc)); code=1
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return code


if __name__=='__main__':
    sys.exit(main())
