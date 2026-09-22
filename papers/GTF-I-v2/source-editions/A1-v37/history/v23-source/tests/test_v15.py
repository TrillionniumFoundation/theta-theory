#!/usr/bin/env python3
"""Exact author diagnostics for the circular application; no author helper imports.

Gaussian rational Laurent arithmetic checks identities and finite rank samples.
These tests are not a proof of continuum uniformity, minimax optimality or novelty.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib
import json
import sys

@dataclass(frozen=True)
class G:
    re: F = F(0)
    im: F = F(0)
    def __add__(self, other):
        o = gauss(other)
        return G(self.re + o.re, self.im + o.im)
    __radd__ = __add__
    def __neg__(self):
        return G(-self.re, -self.im)
    def __sub__(self, other):
        return self + (-gauss(other))
    def __rsub__(self, other):
        return gauss(other) + (-self)
    def __mul__(self, other):
        o = gauss(other)
        return G(self.re*o.re-self.im*o.im, self.re*o.im+self.im*o.re)
    __rmul__ = __mul__
    def conj(self):
        return G(self.re, -self.im)
    def norm2(self):
        return self.re*self.re+self.im*self.im
    def __truediv__(self, other):
        o = gauss(other)
        d = o.norm2()
        if not d:
            raise ZeroDivisionError('zero Gaussian rational')
        p = self*o.conj()
        return G(p.re/d, p.im/d)
    def __pow__(self, n: int):
        if n < 0:
            return (G(F(1))/self)**(-n)
        result, base = G(F(1)), self
        while n:
            if n & 1:
                result = result*base
            base = base*base
            n //= 2
        return result

def gauss(x):
    return x if isinstance(x, G) else G(F(x))

ZERO, ONE, II = G(), G(F(1)), G(F(0), F(1))

def mul(p: dict[int,G], q: dict[int,G], modulus: int|None = None):
    out: dict[int,G] = {}
    for i, a in p.items():
        for j, b in q.items():
            k = i+j if modulus is None else (i+j) % modulus
            out[k] = out.get(k, ZERO)+a*b
    return {k:v for k,v in out.items() if v != ZERO}

def factor(z: G, tau: F):
    return {0:ONE, 1:tau*z, -1:tau*z.conj()}

def product(zs, tau):
    out = {0:ONE}
    for z in zs:
        out = mul(out, factor(z,tau))
    return out

def elementary(zs):
    e = [ONE]
    for z in zs:
        e.append(ZERO)
        for j in range(len(e)-1,0,-1):
            e[j] = e[j]+z*e[j-1]
    return e

def normalized(zs, tau):
    if not tau:
        return elementary(zs)[1:]
    p = product(zs,tau)
    return [p.get(j,ZERO)/(tau**j*p[0]) for j in range(1,len(zs)+1)]

def state(zs, tau, length):
    p = product(zs,tau)
    return {j:tau**j*p.get(j,ZERO)/p[0] for j in range(1,length+1)}

def jacobian(zs, tau):
    n = len(zs)
    p = product(zs,tau)
    columns = []
    for i in range(n):
        others = zs[:i]+zs[i+1:]
        for direction in (ONE,II):
            if not tau:
                column = [direction*e for e in elementary(others)]
            else:
                dp = mul(product(others,tau),
                         {1:tau*direction,-1:tau*direction.conj()})
                column = [(dp.get(j,ZERO)*p[0]-p.get(j,ZERO)*dp.get(0,ZERO)) /
                          (tau**j*p[0]*p[0]) for j in range(1,n+1)]
            columns.append([v for c in column for v in (c.re,c.im)])
    return [list(row) for row in zip(*columns)]

def det(matrix):
    a = [list(row) for row in matrix]
    result = F(1)
    for i in range(len(a)):
        pivot = next((k for k in range(i,len(a)) if a[k][i]),None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[pivot],a[i] = a[i],a[pivot]
            result = -result
        value = a[i][i]
        result *= value
        for k in range(i+1,len(a)):
            ratio = a[k][i]/value
            for j in range(i+1,len(a)):
                a[k][j] -= ratio*a[i][j]
    return result

def B(m, j, tau, rho):
    return sum((F(factorial(m),factorial(j+h)*factorial(h)*factorial(m-j-2*h)) *
                rho**(j+2*h)*tau**(2*h) for h in range((m-j)//2+1)),F(0))

def query_direct(zs, tau, m, rho, phase):
    p = product(zs,tau)
    q = product([rho*phase.conj()]*m,tau)
    return mul(p,q).get(0,ZERO)/(2**m*p[0])

def query_formula(zs, tau, m, rho, phase):
    y = state(zs,tau,m)
    value = G(B(m,0,tau,rho))
    for j in range(1,m+1):
        value += B(m,j,tau,rho)*(y[j]*phase**j+(y[j]*phase**j).conj())
    return value/(2**m)

COUNTS: dict[str,int] = {}
def check(condition, category):
    COUNTS[category] = COUNTS.get(category,0)+1
    if not condition:
        raise AssertionError(f'{category} check {COUNTS[category]} failed')

def main():
    rho = F(1,64)
    samples = 0
    for n in range(1,7):
        for seed in range(3):
            zs = [G(F(i+1+seed,128), F(i%3-1,96)) for i in range(n)]
            for tau in (F(0),F(1,2),F(1,8),F(1,64)):
                samples += 1
                p = product(zs,tau)
                check(p[0].im == 0 and p[0].re >= (1-tau)**n,'positive_evidence')
                for j in range(n+1):
                    check(p.get(-j,ZERO)==p.get(j,ZERO).conj(),'hermitian_coefficients')
                s = normalized(zs,tau)
                y = state(zs,tau,n+2)
                for j in range(1,n+1):
                    check(y[j]==tau**(2*j)*s[j-1],'double_attenuation')
                check(y[n+1]==ZERO and y[n+2]==ZERO,'exact_high_mode_zeros')
                for m in range(1,5):
                    for j in range(m+1):
                        check(B(m,j,tau,rho)>=F(factorial(m),factorial(j)*factorial(m-j))*rho**j,
                              'positive_query_coefficients')
                    for phase in (ONE,II,-ONE,-II):
                        direct = query_direct(zs,tau,m,rho,phase)
                        check(direct==query_formula(zs,tau,m,rho,phase),'physical_query_identity')
                        check(direct.im==0 and 0<=direct.re<=1,'physical_probability')
                    yy = state(zs,tau,m)
                    other = state([G(F(1,256))]*n,tau,m)
                    phase_poly = {}
                    expected = F(0)
                    for j in range(1,m+1):
                        delta = yy[j]-other[j]
                        coeff = B(m,j,tau,rho)*delta/(2**m)
                        phase_poly[j],phase_poly[-j] = coeff,coeff.conj()
                        expected += F(2,2**(2*m))*B(m,j,tau,rho)**2*delta.norm2()
                    average = mul(phase_poly,phase_poly,2*m+1).get(0,ZERO)
                    check(average==G(expected),'exact_cyclic_parseval')
                for new_z in (G(F(1,32),F(-1,40)),G(F(1,2)),G(F(0),F(-1,2))):
                    before = state(zs,tau,n+2); before[0]=ONE
                    after = state(zs+[new_z],tau,n+1)
                    denominator = ONE+new_z*before[1].conj()+new_z.conj()*before[1]
                    check(denominator.im==0 and denominator.re>=1-tau,'update_evidence_bound')
                    for j in range(1,n+2):
                        updated = (before[j]+tau**2*new_z*before[j-1]+new_z.conj()*before[j+1])/denominator
                        check(updated==after[j],'causal_update_identity')
                    if tau:
                        wrong = (before[1]+new_z+new_z.conj()*before[2])/denominator
                        check(wrong!=after[1],'negative_control_missing_tau_squared')
                if tau and n>=2:
                    check(p[0]!=ONE,'nontrivial_normalization')
                    check(p.get(1,ZERO)!=p.get(1,ZERO)/p[0],'negative_control_missing_evidence')
    rank_samples = []
    for n in range(1,6):
        zs = [G(F(i+1,128)) for i in range(n)]
        for tau in (F(0),F(1,4),F(1,32)):
            J = jacobian(zs,tau)
            determinant = det(J)
            check(determinant!=0,'full_real_jacobian_rank')
            for k in range(1,n+1):
                block = J[:2*k]
                gram = [[sum((a*b for a,b in zip(row,col)),F(0)) for col in block] for row in block]
                check(det(gram)>0,'all_initial_harmonic_flags')
            rank_samples.append({'n':n,'tau':str(tau),'determinant_nonzero':True,
                                 'determinant_sha256':hashlib.sha256(str(determinant).encode()).hexdigest()})
    for tau in (F(1,2),F(1,3),F(1,8)):
        for j in range(1,5):
            M = tau**(-2*j*(j+1))
            left_power = tau**(2*j*(j+1))/M
            right_power = tau**(2*(j+1)*(j+2))/M
            check(left_power**(j+1)==right_power**j,'adjacent_phase_crossings')
        for n in range(1,5):
            a = [tau**(2*j) for j in range(1,n+1) for _ in range(2)]
            volume = F(1)
            for index,x in enumerate(a,1):
                volume *= x
                if index%2==0:
                    j=index//2
                    check(volume==tau**(2*j*(j+1)),'paired_exterior_volumes')
    # At one trial each side contributes tau; using only future contrast is false.
    for tau in (F(1,2),F(1,8),F(1,64)):
        z = G(F(1,32))
        delta = query_direct([z],tau,1,rho,ONE)-query_direct([ZERO],tau,1,rho,ONE)
        check(delta==G(tau**2*rho*z.re),'one_trial_double_attenuation')
        check(delta!=G(tau*rho*z.re),'negative_control_future_only_scale')
    report={'version':15,'passed':True,'assertions':sum(COUNTS.values()),
            'categories':COUNTS,'history_configurations':samples,'rank_configurations':rank_samples,
            'arithmetic':'Exact fractions and Gaussian rational Laurent coefficients; cyclic Fourier identities.',
            'scope':'Author-designed finite diagnostics, not independent referee review, continuum proof or novelty certification.'}
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parents[1]/'validation/V15_CIRCULAR_DIAGNOSTICS.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
