#!/usr/bin/env python3
"""Independent diagnostics for A1 v4 at e4b10bf (not a proof assistant).
No author code is imported. Exact Fraction interval arithmetic and SymPy.
Run: python referee_checks.py ; output: DIAGNOSTICS.json next to this file.
Finite diagnostics do not certify the general theorems or journal novelty.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from math import isqrt
from pathlib import Path
import hashlib
import json
import sys
import sympy as sp

@dataclass(frozen=True)
class Box:
    low: Q
    high: Q
    def __post_init__(self):
        if self.low > self.high:
            raise ValueError('Reversed interval')
    @staticmethod
    def make(value):
        return value if isinstance(value, Box) else Box(Q(value), Q(value))
    def __add__(self, other):
        b = Box.make(other)
        return Box(self.low + b.low, self.high + b.high)
    __radd__ = __add__
    def __neg__(self):
        return Box(-self.high, -self.low)
    def __sub__(self, other):
        return self + (-Box.make(other))
    def __rsub__(self, other):
        return Box.make(other) - self
    def __mul__(self, other):
        b = Box.make(other)
        ends = [a*c for a in (self.low, self.high) for c in (b.low, b.high)]
        return Box(min(ends), max(ends))
    __rmul__ = __mul__
    def __truediv__(self, other):
        b = Box.make(other)
        if b.low <= 0 <= b.high:
            raise ZeroDivisionError('Interval includes zero')
        return self * Box(1/b.high, 1/b.low)
    def __rtruediv__(self, other):
        return Box.make(other)/self
    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError('Nonnegative integer power required')
        answer = Box.make(1)
        for _ in range(n):
            answer = answer*self
        return answer

def maximum(items):
    v = list(items)
    return Box(max(a.low for a in v), max(a.high for a in v))

def enclosure(x, digits=18):
    scale = 10**digits
    def dec(n):
        sign = '-' if n < 0 else ''
        n = abs(n)
        return f'{sign}{n//scale}.{n%scale:0{digits}d}'
    return {'lower': dec((x.low*scale).__floor__()),
            'upper': dec((x.high*scale).__ceil__())}

def atan_remainder(den, count):
    partial = sum((Q((-1)**j, (2*j+1)*den**(2*j+1)) for j in range(count)), Q(0))
    following = Q((-1)**count, (2*count+1)*den**(2*count+1))
    return Box(min(partial, partial+following), max(partial, partial+following))

def check_within(interval, lo, hi):
    return Q(lo) < interval.low and interval.high < Q(hi)

checks = []
def record(name, condition, evidence=None):
    ok = bool(condition)
    checks.append({'name': name, 'passed': ok, 'kind': 'exact rational / symbolic finite diagnostic',
                   'evidence': evidence})
    if not ok:
        raise AssertionError(name)

# Different truncation lengths and precision from the submitted program.
pi = 16*atan_remainder(5, 60)-4*atan_remainder(239, 15)
scale = 10**55
root = isqrt(3*scale*scale)
sqrt3 = Box(Q(root, scale), Q(root+1, scale))
record('independent_Machin_enclosure', check_within(pi,
       '3.1415926535897932384626433832795028841971',
       '3.1415926535897932384626433832795028841972'), enclosure(pi, 40))
record('independent_sqrt3_squared_bounds', sqrt3.low**2 < 3 < sqrt3.high**2,
       enclosure(sqrt3, 40))
a0 = sqrt3/2
radii = [Q(9,20), Q(47,100)]
T, S = Q(1,20), Q(99,100)
raw = [[pi*r*r/a0, 1-pi*r*r/a0-2*T*r/a0, 2*T*r/a0] for r in radii]
record('nominal_probabilities_positive_normalized',
       all(all(v.low > 0 for v in row) and sum(row).low <= 1 <= sum(row).high for row in raw))
prior = [Box.make(Q(2,5)), Box.make(Q(3,5))]

def bayes_payoff(z):
    return maximum([2*z[0]+z[1], z[0]+2*z[1]])

def solve_finite(prob):
    count = len(prob[0])
    gates = list(product((0,1), repeat=count))
    def outcomes(z, gate):
        values = []
        for j in range(count):
            if gate[j]:
                values.append(([z[i]*prob[i][j] for i in range(2)], S, j))
        failure = [sum((prob[i][j] for j in range(count) if not gate[j]), Box.make(0)) for i in range(2)]
        values.append(([z[i]*failure[i] for i in range(2)], Q(1), count))
        return values
    def last(z, gate):
        return sum((w*bayes_payoff(next_z) for next_z,w,_ in outcomes(z,gate)), Box.make(0))
    fixed = {(g,h):sum((w*last(z,h) for z,w,_ in outcomes(prior,g)), Box.make(0))
             for g in gates for h in gates}
    adaptive = {g:sum((w*maximum(last(z,h) for h in gates) for z,w,_ in outcomes(prior,g)), Box.make(0))
                for g in gates}
    return gates, outcomes, last, fixed, adaptive

gates, outcomes, last, fixed, adaptive = solve_finite(raw)
A, O = (0,1,0), (0,0,0)
na, ad = fixed[(A,A)], adaptive[A]
record('all_64_nonadaptive_pairs_unique_winner_AA',
       len(fixed)==64 and all(na.low > v.high for k,v in fixed.items() if k!=(A,A)))
record('all_8_adaptive_first_gates_unique_winner_A',
       len(adaptive)==8 and all(ad.low > v.high for k,v in adaptive.items() if k!=A))
continuations=[]
for z,w,tag in outcomes(prior,A):
    chosen = A if tag==1 else O
    values = {g:last(z,g) for g in gates}
    record('continuation_'+str(tag)+'_strict_choice',
           all(values[chosen].low > v.high for k,v in values.items() if k!=chosen),
           {'choice':chosen,'weighted_value':enclosure(w*values[chosen])})
    continuations.append({'tag':tag,'chosen':chosen,'all_values':[
        {'gate':g,**enclosure(w*v)} for g,v in values.items()]})
record('printed_nonadaptive_value', check_within(na,'1.600432377967011','1.600432377967012'),enclosure(na))
record('printed_adaptive_value', check_within(ad,'1.602586453549804','1.602586453549805'),enclosure(ad))
gap=ad-na
record('printed_nominal_gap',check_within(gap,'0.002154075582792','0.002154075582793'),enclosure(gap))
q=[row[1] for row in raw]
signs={}
for bits in product((0,1),repeat=2):
    z=[prior[i] for i in range(2)]
    for b in bits:
        z=[z[i]*(q[i] if b else 1-q[i]) for i in range(2)]
    difference=z[0]-z[1]
    signs[str(bits)]=enclosure(difference)
    record('terminal_sign_'+''.join(map(str,bits)),
           difference.low>0 if bits==(1,1) else difference.high<0,enclosure(difference))
# Check every printed nonadaptive table entry independently, not only the maximum.
upper_rows=[
[1,-859097,-2586509,-3445606,-12554393,-13413490,-15140902,-15999999],
[-859097,-1717732,-3444222,-4302858,-13406745,-14265381,-15991870,-16850506],
[-2586509,-3444222,432378,-425335,-9725764,-10320810,-12101858,-12959572],
[-3445606,-4302858,-425335,-1282586,-10578116,-11172701,-12952826,-13810078],
[-12554393,-13406745,-9725764,-10578116,-20513189,-20413020,-22181516,-23033868],
[-13413490,-14265381,-10320810,-11172701,-20413020,-20999591,-22769817,-23621707],
[-15140902,-15991870,-12101858,-12952826,-22181516,-22769817,-24537454,-25388421],
[-15999999,-16850506,-12959572,-13810078,-23033868,-23621707,-25388421,-26238928]]
record('all_64_printed_table_upper_bounds',all(
    fixed[(g,h)].high <= Q(8,5)+Q(upper_rows[i][j],10**9)
    for i,g in enumerate(gates) for j,h in enumerate(gates)))
first_upper=[1,-859097,2586454,1727357,-7730246,-8188276,-9967940,-10827037]
record('all_8_printed_adaptive_upper_bounds',all(
    adaptive[g].high <= Q(8,5)+Q(first_upper[i],10**9) for i,g in enumerate(gates)))
e0=(2*T*radii[1]/a0)*(Q(1,20)*radii[1]**2)/pi
e2=1-(1-e0)**2
omega=2-S*S
transferred=gap-2*omega*(e2+Q(1,10000))
record('full_cubic_transfer_gt_11_over_10000', transferred.low>Q(11,10000),enclosure(transferred))
record('printed_transfer_enclosure',check_within(transferred,'0.001171773732645','0.001171773732646'))
# Referee ablation: the same optimum and gap in a binary, non-mechanical experiment.
binary=[[1-row[1],row[1]] for row in raw]
bg,bo,bl,bfixed,bad=solve_finite(binary)
BA=(0,1)
bna,badvalue=bfixed[(BA,BA)],bad[BA]
record('binary_ablation_unique_nonadaptive_winner',all(bna.low>v.high for k,v in bfixed.items() if k!=(BA,BA)))
record('binary_ablation_unique_adaptive_winner',all(badvalue.low>v.high for k,v in bad.items() if k!=BA))
record('binary_ablation_same_values_within_1e_minus_45',
       all((x-y).low > -Q(1,10**45) and (x-y).high < Q(1,10**45)
           for x,y in ((bna,na),(badvalue,ad))),
       {'nonadaptive':enclosure(bna),'adaptive':enclosure(badvalue),
        'meaning':'Exact equality follows analytically from the common selected-policy formulas; this bounds recomputation differences.'})
# Symbolic closed gap, independent of pi, sqrt3, mechanics, or polynomial degree.
z0,z1,q0,q1,s=sp.symbols('z0 z1 q0 q1 s')
mixed=z0*q0*(1-q0)+2*z1*q1*(1-q1)
full11=2*z0*q0*q0+z1*q1*q1
vna=s*s*full11+2*s*mixed+z0*(1-q0)**2+2*z1*(1-q1)**2
vad=s*s*full11+s*mixed+z0*(1-q0)+2*z1*(1-q1)
record('binary_gap_symbolic_identity',sp.expand(vad-vna-(1-s)*mixed)==0)
y,eps,R=sp.symbols('y eps R',real=True)
record('tag_only_witness_independent_of_cubic_mark',sp.integrate(1+eps*R**2*sp.cos(y),(y,0,2*sp.pi))==2*sp.pi)
# Gram right inverse in a finite positive degree-three experiment.
t=sp.symbols('t')
coeff=sp.Matrix([[1,x,x*x,x*x*x] for x in (1,2,3,4)])
Gamma=coeff.T*coeff/4
increment=sp.Matrix([sp.Rational(1,1000000),0,0,0])
g=sp.ones(4,1)/2-coeff*Gamma.inv()*increment
f=coeff.T*(sp.ones(4,1)-g)/4
record('Gram_right_inverse_exact',Gamma.det()>0 and
       f-coeff.T*sp.ones(4,1)/8==increment and all(0<x<1 for x in g),
       {'determinant':str(Gamma.det()),'gates':[str(x) for x in g]})
# Referee dimension lemma: finite algebra diagnostics, not an all-n proof.
cases=[('full_cubic',[1,t,t*t,t**3],1),
       ('sparse_rank_three',[1,t*t,t**5],1),
       ('common_factor_rank_three',[1,t,t*t],1+t*t)]
rank_evidence=[]
for title,basis,common in cases:
    d=max(sp.degree(x,t) for x in basis)
    actual=[sp.expand(common*x) for x in basis]
    for n in (1,2,3,4):
        factors=[sp.expand(common*(i+2+t**d)) for i in range(n)]
        variations=[]
        for i in range(n):
            other=sp.prod(factors[j] for j in range(n) if j!=i)
            variations.extend(sp.Poly(sp.expand(v*other),t) for v in actual)
        degree=max(p.degree() for p in variations)
        matrix=sp.Matrix([[p.nth(k) for p in variations] for k in range(degree+1)])
        rank=matrix.rank()
        expected=n*(len(basis)-1)+1
        record(title+'_product_rank_n_'+str(n),rank==expected,{'rank':rank,'normalized_rank':rank-1})
        rank_evidence.append({'case':title,'n':n,'rank':rank,'normalized_rank':rank-1})
# Elementary identities used in positive Bernstein approximation.
for m in (1,2,7):
    B=[sp.binomial(m,i)*t**i*(1-t)**(m-i) for i in range(m+1)]
    norm=sp.expand(sum(B))
    variance=sp.expand(sum((sp.Rational(i,m)-t)**2*B[i] for i in range(m+1)))
    record('Bernstein_normalization_variance_m_'+str(m),norm==1 and sp.expand(variance-t*(1-t)/m)==0)

result={
 'reviewed_commit':'e4b10bf7acebf38dbcfb466b3ee4cf30bb77b381',
 'review_date':'2026-09-06',
 'status':'PASS','checks_passed':len(checks),'checks_total':len(checks),
 'method':'Independent script; exact rational interval decisions and symbolic identities/ranks; no imported author code.',
 'limits':['Not proof-assistant verification','Not an exhaustive priority search','No LaTeX compilation or PDF inspection',
           'Author 24-check suite not rerun','No complete historical-foundation or eleven-paper audit',
           'Finite ranks do not prove the all-budget dimension lemma; its analytic proof is in the report',
           'All-Borel coverage is an analytic argument, not a conclusion from a finite enumeration'],
 'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'values':{'nominal_nonadaptive':enclosure(na),'nominal_adaptive':enclosure(ad),'nominal_gap':enclosure(gap),
           'one_step_error':enclosure(e0),'two_step_error':enclosure(e2),'transferred_gap_lower_bound_expression':enclosure(transferred),
           'binary_nonadaptive':enclosure(bna),'binary_adaptive':enclosure(badvalue)},
 'checks':checks,
 'all_nonadaptive_values':[{'first':g,'second':h,**enclosure(v)} for (g,h),v in fixed.items()],
 'all_adaptive_first_gate_values':[{'first':g,**enclosure(v)} for g,v in adaptive.items()],
 'continuations':continuations,
 'rank_evidence':rank_evidence}
target=Path(__file__).with_name('DIAGNOSTICS.json')
target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','checks_passed','checks_total','values','script_sha256')},indent=2))
