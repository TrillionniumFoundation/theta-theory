#!/usr/bin/env python3
"""Independent finite checks for A1 v33. Not a general theorem verifier.

Standard library only. Every logical check remains active under python -O.
The three-stage test uses a uniform continuous latent prior and a prescribed
atomic command law (allowed in Section 8), not the principal uniform cube law.
The exact paper instance is separately checked by a different series formula.
"""
from __future__ import annotations
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json

COUNT = 0

def check(ok: bool, message: str) -> None:
    global COUNT
    COUNT += 1
    if not ok:
        raise ArithmeticError(message)

def trim(p):
    p = list(p)
    while len(p)>1 and p[-1] == 0:
        p.pop()
    return p

def add(a,b):
    return trim([(a[i] if i<len(a) else F(0)) + (b[i] if i<len(b) else F(0))
                 for i in range(max(len(a),len(b)))])

def scale(a,s):
    return trim([x*s for x in a])

def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    return trim(out)

def integral(p):
    return sum((c/F(i+1) for i,c in enumerate(p)),F(0))

def kernel(n,i,c,x):
    v=F(1+(3*n+2*i+5*c+4*x)%10,12)
    return [1-v,v]

CELLS=[[F(1,4),F(1,2)],[F(3,4),-F(1,2)]]
COMMANDS=[(F(1,4),F(2,3)),(F(3,4),F(1,3))]
PROBS=[F(2,5),F(3,5)]

def likelihood(c,x):
    g=COMMANDS[c]
    if x<2:
        return scale(CELLS[x],g[x])
    return add(scale(CELLS[0],1-g[0]),scale(CELLS[1],1-g[1]))

def row(n,i):
    return [[sum((PROBS[c]*(COMMANDS[c][k]*kernel(n,i,c,k)[j]
             +(1-COMMANDS[c][k])*kernel(n,i,c,2)[j]) for c in range(2)),F(0))
             for j in range(2)] for k in range(2)]

def query_menu(m):
    # Failure factors at (.5,.5) and (.35,.55), both in [.2,.8]^2.
    basis=[[F(1,2)],[F(1,2),F(1,10)]]
    result=[]
    for word in product(range(2),repeat=m):
        p=[F(1)]
        for k in word:
            p=mul(p,basis[k])
        result.append(p)
    return result

def three_stage():
    histories=[([F(1)],[F(1),F(0)],F(1))]
    q=[[F(1)],[F(0)]]
    records=[]
    for n in range(1,4):
        A=[row(n,i) for i in range(2)]
        qnew=[[F(0)],[F(0)]]
        for i,k,j in product(range(2),repeat=3):
            qnew[j]=add(qnew[j],scale(mul(q[i],CELLS[k]),A[i][k][j]))
        new=[]
        for L,z,pc in histories:
            for c,x in product(range(2),range(3)):
                zz=[sum((z[i]*kernel(n,i,c,x)[j] for i in range(2)),F(0))
                    for j in range(2)]
                new.append((mul(L,likelihood(c,x)),zz,pc*PROBS[c]))
        histories=new
        direct=[[F(0)],[F(0)]]
        for L,z,pc in histories:
            for i in range(2):
                direct[i]=add(direct[i],scale(L,pc*z[i]))
        check(qnew==direct,f'occupancy polynomial identity n={n}')
        check(add(*qnew)==[F(1)],f'occupancy conservation n={n}')
        H=query_menu(4-n)
        w=[integral(x) for x in qnew]
        b=[[integral(mul(qnew[i],h)) for h in H] for i in range(2)]
        d=[[v/w[i] for v in b[i]] for i in range(2)]
        B=F(0); R=F(0); cross=F(0)
        for L,z,pc in histories:
            evidence=integral(L)
            for l,h in enumerate(H):
                p=integral(mul(L,h))/evidence
                B += pc*evidence*p*p/len(H)
                for i in range(2):
                    R += pc*evidence*z[i]*(p-d[i][l])**2/len(H)
                    cross += pc*evidence*z[i]*p*d[i][l]/len(H)
        explained=sum((b[i][l]**2/w[i]/len(H)
                        for i in range(2) for l in range(len(H))),F(0))
        check(cross==explained,f'cross-term factorization n={n}')
        check(R==B-explained,f'exact mean-risk identity n={n}')
        check(R>=0,f'nonnegative regret n={n}')
        records.append({'checkpoint':n,'histories':len(histories),
                        'query_count':len(H),'risk':str(R),'risk_decimal':float(R)})
        q=qnew
    return records

def body_checks():
    matrices=[]
    for choices in product(range(2),repeat=6):
        A=[[F(0),F(0)],[F(0),F(0)]]
        for c,k in product(range(2),repeat=2):
            A[k][choices[3*c+k]] += PROBS[c]*COMMANDS[c][k]
            A[k][choices[3*c+2]] += PROBS[c]*(1-COMMANDS[c][k])
        matrices.append(A)
    overlaps=[sum((min(A[0][j],A[1][j]) for j in range(2)),F(0)) for A in matrices]
    floor=sum((PROBS[c]*min(1-COMMANDS[c][0],1-COMMANDS[c][1]) for c in range(2)),F(0))
    check(min(overlaps)==floor,'common-failure overlap is attained in finite example')
    for Cflat in product((-2,0,3),repeat=4):
        C=[Cflat[:2],Cflat[2:]]
        brute=max(sum((C[k][j]*A[k][j] for k,j in product(range(2),repeat=2)),F(0)) for A in matrices)
        formula=sum((sum((PROBS[c]*COMMANDS[c][k] for c in range(2)),F(0))*max(C[k])
                     for k in range(2)),F(0))
        formula+=sum((PROBS[c]*max(sum(((1-COMMANDS[c][k])*C[k][j] for k in range(2)),F(0))
                                             for j in range(2)) for c in range(2)),F(0))
        check(brute==formula,'support-function identity')
    return {'deterministic_rules_enumerated':len(matrices),'linear_functionals_tested':81,
            'minimum_row_overlap':str(floor),'arbitrary_row_identity_excluded':floor>0}

def independent_certificate():
    # Integrate each polynomial via a direct multinomial expansion rather than
    # multiplying (X-Z)^2 by a separate binomial expansion as in the author code.
    def moment(p):
        return F(0) if p%2 else F(1,20**p*(p+1))
    terms=[]
    for k in range(6):
        value=F(0)
        for p in range(2*k+3):
            coef=sum(((-1)**r*comb(2,r)*comb(2*k,p-r)
                      for r in range(3) if 0<=p-r<=2*k),0)
            value+=coef*moment(p)*moment(2*k+2-p)
        terms.append(value)
    lo=F(1,240)**2*(F(1,12)+sum(terms,F(0))/4)
    width=F(1,136857600000000000000)
    hi=lo+width
    check(lo==F(18108150189130829,12454041600000000000000),'paper lower endpoint')
    check(hi==F(150901251576091,103783680000000000000),'paper upper endpoint')
    check(F(1,2)-F(3,20)/1-(1+3*F(1,10)**2)/4==F(37,400),'all-encoder margin')
    # Independent sum-and-difference integration of J, with a decimal log check.
    # J = (100/3) [int_.9^1 (s-.9)^3/s ds + int_1^1.1 (1.1-s)^3/s ds].
    with localcontext() as ctx:
        ctx.prec=90
        c=Decimal(9)/10; d=Decimal(11)/10; one=Decimal(1)
        def P(s): return s**3/3-3*c*s*s/2+3*c*c*s-c**3*s.ln()
        def Q(s): return d**3*s.ln()-3*d*d*s+3*d*s*s/2-s**3/3
        J=Decimal(100)/3*(P(one)-P(c)+Q(d)-Q(one))
        risk=(one/Decimal(240))**2*(one/12+J/4)
        lower=Decimal(lo.numerator)/lo.denominator
        upper=Decimal(hi.numerator)/hi.denominator
        check(lower<risk<upper,'independent logarithmic integral inside certificate')
        numeric=str(risk)
    return {'lower':str(lo),'upper':str(hi),'width':str(width),
            'risk_log_integral_90_digit_diagnostic':numeric,
            'log_integral_is_formally_directed_enclosure':False}

def main():
    result={'schema':'theta-v33-independent-referee-checks-v1',
            'reviewed_commit':'e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c',
            'arithmetic':'Fraction; Decimal only for explicitly noncertified logarithmic cross-check',
            'three_stage':three_stage(),'implementability_body':body_checks(),
            'continuum_certificate':independent_certificate()}
    result['checks_passed']=COUNT
    result['scope_limits']=['No exhaustive optimization of the multistage controller.',
        'Atomic command test does not verify atomless purification.',
        'No full TeX build or visual inspection was performed by this referee.',
        'Finite diagnostics are not a proof of the general theorems.']
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
