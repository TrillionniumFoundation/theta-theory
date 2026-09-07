#!/usr/bin/env python3
"""Independent exact diagnostics for A1 v22; finite tests, not a proof certificate.

No manuscript/author-test imports. Python standard library only. Optional JSON
output path: python independent_diagnostics.py DIAGNOSTICS.json
The same checks run under python -O: checks deliberately do not use assert.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

COUNTS: Counter[str] = Counter()
MODELS = HISTORIES = PREFIXES = NONASSOCIATIVE = 0

def check(group: str, condition: bool) -> None:
    COUNTS[group] += 1
    if not condition:
        raise RuntimeError(f"Diagnostic failed: {group} #{COUNTS[group]}")

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def add(a, b):
    return tuple(x+y for x, y in zip(a, b))

def scale(a, s):
    return tuple(s*x for x in a)

def unit(n, i):
    return tuple(F(j == i) for j in range(n))

def mul(a, b, table):
    d = len(a)-1
    out = [a[0]*b[0]] + [a[0]*b[k]+b[0]*a[k] for k in range(1,d+1)]
    for i in range(d):
        for j in range(d):
            for k in range(d+1):
                out[k] += a[i+1]*b[j+1]*table[i][j][k]
    return tuple(out)

def rank(rows):
    a = [list(row) for row in rows]
    r = 0
    for j in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(r,len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        t = a[r][j]
        a[r] = [x/t for x in a[r]]
        for i in range(len(a)):
            if i != r:
                t = a[i][j]
                a[i] = [x-t*y for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r

def audit_model(values, prior, table):
    global MODELS, HISTORIES, PREFIXES, NONASSOCIATIVE
    MODELS += 1
    d, q = len(values[0]), len(values)
    delta = F(1,12)
    check('admissibility', sum(prior) == 1 and min(prior) >= 0)
    check('admissibility', all(abs(x) <= 1 for row in values for x in row))
    check('admissibility', delta <= F(1,4*d))
    check('admissibility', max(abs(x) for row in table for cell in row for x in cell) <= 2)
    ev = [(F(1),)+tuple(row) for row in values]
    for i,j,z in product(range(d), range(d), range(q)):
        check('multiplication', dot(table[i][j],ev[z]) == values[z][i]*values[z][j])
    units = [unit(d+1,i) for i in range(d+1)]
    seen_nonassoc = False
    for a,b,c in product(units, repeat=3):
        diff = add(mul(mul(a,b,table),c,table),scale(mul(a,mul(b,c,table),table),-1))
        if any(diff):
            seen_nonassoc = True
        check('represented_associativity', all(dot(diff,row)==0 for row in ev))
    NONASSOCIATIVE += int(seen_nonassoc)
    mean = tuple(sum(prior[z]*values[z][i] for z in range(q)) for i in range(d))
    cov = tuple(tuple(sum(prior[z]*(values[z][i]-mean[i])*(values[z][j]-mean[j])
                          for z in range(q)) for j in range(d)) for i in range(d))
    active = [values[z] for z in range(q) if prior[z]>0]
    differences = [tuple(x-y for x,y in zip(row,active[0])) for row in active]
    check('support_affine_rank', rank(cov) == rank(differences))
    commands = [tuple(delta*F((j+1)*((-1)**(i+j)), d*(i+2)) for j in range(d))
                for i in range(3)]
    word_mass = F(0)
    for word in product((-1,1), repeat=3):
        HISTORIES += 1
        coeff = units[0]
        density = [F(1)]*q
        old = mean
        for n,(u,y) in enumerate(zip(commands,word),start=1):
            PREFIXES += 1
            factors = [1+y*dot(u,row) for row in values]
            check('positive_likelihood', all(F(3,4)<=x<=F(5,4) for x in factors))
            density = [a*b for a,b in zip(density,factors)]
            coeff = mul(coeff,(F(1),)+scale(u,y),table)
            evidence = dot(prior,density)
            check('evidence', F(3,4)**n <= evidence <= F(5,4)**n)
            check('product_chart', all(dot(coeff,row)==density[z] for z,row in enumerate(ev)))
            check('product_chart', coeff[0]+dot(coeff[1:],mean)==evidence)
            post = tuple(sum(prior[z]*density[z]*values[z][i] for z in range(q))/evidence
                         for i in range(d))
            theta = scale(coeff[1:],1/evidence)
            chart = tuple(mean[i]+dot(cov[i],theta) for i in range(d))
            check('posterior_chart', chart==post)
            denominator = 1+y*dot(u,old)
            update = tuple((old[i]+y*sum(u[j]*(table[i][j][0]+dot(table[i][j][1:],old))
                                               for j in range(d)))/denominator for i in range(d))
            check('raw_update', update==post)
            if rank(cov)==0:
                check('zero_rank', post==mean)
            for s in (1,3):
                differences_q = [F(0)]+[F(1,2)**s*delta*(post[i]-mean[i]) for i in range(d)]
                physical = dot(differences_q,differences_q)/F(d+1)
                check('physical_metric', physical==(F(1,2)**s*delta)**2*
                      sum((post[i]-mean[i])**2 for i in range(d))/F(d+1))
            old = post
        word_mass += evidence/F(8)
    check('unconditional_word_partition', word_mass==1)

# A redundant affine presentation, with two equal generators and a constant.
# Null relations are added to the multiplication table deliberately. Evaluation
# is associative; coefficient multiplication need not be. B=2 works throughout.
for tau,c,p in product((F(0),F(1,13),F(1)),(F(0),F(1,5)),
                       (F(0),F(1,10**6),F(1,4),F(1,2),F(1))):
    e = [unit(4,i) for i in range(4)]
    n1, n2 = add(e[1],scale(e[2],-1)), add(e[0],scale(e[3],-1))
    table = [[None]*3 for _ in range(3)]
    table[0][0] = add(scale(e[1],tau),scale(n2,c))
    table[0][1] = table[1][0] = add(scale(e[2],tau),scale(n1,c))
    table[1][1] = add(scale(e[1],tau),scale(n2,-c))
    table[0][2] = table[2][0] = add(e[1],scale(n1,c))
    table[1][2] = table[2][1] = add(e[2],scale(n1,-c))
    table[2][2] = add(e[0],scale(n2,c))
    audit_model(((F(0),F(0),F(1)),(tau,tau,F(1))),(1-p,p),table)

# Three observable atoms: positive, boundary, rare-atom and Dirac priors.
priors = ((F(1,3),)*3,(F(0),F(1,2),F(1,2)),(F(1),F(0),F(0)),
          (F(0),F(1),F(0)),(F(999998,10**6),F(1,10**6),F(1,10**6)))
for (t1,t2),prior in product(((F(1),F(1)),(F(1),F(1,31)),
                             (F(0),F(1)),(F(0),F(0))),priors):
    zero = (F(0),)*3
    table = [[(F(0),t1,F(0)),zero],[zero,(F(0),F(0),t2)]]
    audit_model(((F(0),F(0)),(t1,F(0)),(F(0),t2)),prior,table)

# Exact Jacobian identity at selected first-command anchor coordinates.
# With later commands zero, theta=z/(1+m.z), independently of the table.
for m in ((F(0),F(1)),(F(1,4),F(-1,3)),(F(1),F(1))):
    for z in ((F(1,100),F(-1,200)),(F(0),F(1,120))):
        denom = 1+dot(m,z)
        jac = [[F(i==j)/denom-z[i]*m[j]/denom**2 for j in range(2)] for i in range(2)]
        determinant = jac[0][0]*jac[1][1]-jac[0][1]*jac[1][0]
        check('first_command_jacobian', determinant==denom**-3)

# Integer witness for each nonzero exterior-product branch. Avoid roots:
# e(M)^2 <= lambda_l^2 is equivalent to V_j/M <= lambda_l^j for every j.
for scales in ((F(1),),(F(1),F(1,7)),(F(3),F(1),F(1,99)),
               (F(1,10**6),F(1,10**6)),(F(1),F(0)),(F(0),F(0))):
    products=[]
    value=F(1)
    for x in scales:
        value*=x
        products.append(value)
    for l,lam in enumerate(scales,start=1):
        if lam==0:
            continue
        real_budget=products[l-1]/lam**l
        integer_budget=(real_budget.numerator+real_budget.denominator-1)//real_budget.denominator
        check('integer_profile_witness', 1<=real_budget<=integer_budget<=2*real_budget)
        for j,V in enumerate(products,start=1):
            check('integer_profile_witness', V/F(integer_budget)<=lam**j)
        check('integer_profile_witness', integer_budget*lam**l<=2*products[l-1])

# Adversarial controls: deliberately incorrect alternatives are distinguishable.
check('negative_controls', NONASSOCIATIVE>0)
p,tau,u=F(1,3),F(1,5),F(1,12)
m=p*tau
sigma=p*(1-p)*tau**2
post=m+sigma*u/(1+m*u)
check('negative_controls', post!=m+sigma*u)  # omission of evidence normalization
check('negative_controls', post!=m+(p*tau**2)*u/(1+m*u))  # second moment instead of covariance
check('negative_controls', sigma**2!=sigma)  # variance, not std deviation, is an axis

payload={
    'target_commit':'5f745a863dac637496bd5eb20341f12cecb71ab1',
    'status':'PASS', 'models':MODELS, 'full_histories':HISTORIES,
    'checked_prefixes':PREFIXES, 'models_with_nonassociative_coefficient_rule':NONASSOCIATIVE,
    'checks':sum(COUNTS.values()), 'groups':dict(sorted(COUNTS.items())),
    'arithmetic':'fractions.Fraction; exact rational arithmetic; Python standard library',
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'limitations':'Finite identity and adversarial tests only; not a proof of uniform density, entropy bounds, optimal coding risk, or the full manuscript.'
}
text=json.dumps(payload,indent=2,sort_keys=True)+'\n'
if len(sys.argv)>2:
    raise SystemExit('Usage: independent_diagnostics.py [output.json]')
if len(sys.argv)==2:
    Path(sys.argv[1]).write_text(text,encoding='utf-8')
print(text,end='')
