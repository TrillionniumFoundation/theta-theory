#!/usr/bin/env python3
"""Exact finite checks. These are NOT certificates of the continuum proofs."""
from __future__ import annotations
import argparse,csv,json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

CHECKS=0

def require(ok: bool, message: str) -> None:
    global CHECKS
    CHECKS+=1
    if not ok:
        raise RuntimeError(message)

def cell_loss(d:F,p:F,c:int)->F:
    return (d*d-d+F(1,2))/2+(1 if c else -1)*p*(1-2*d)/8

def risk(ds:tuple[F,F], rows:tuple[F,F,F,F], p:F, beta:F=F(1,2))->F:
    T=[]; r=[]
    for i in range(2):
        q=(rows[2*i]+rows[2*i+1])/2
        T.append((q,1-q))
        r.append(sum(rows[2*i+c]*cell_loss(ds[0],p,c)+(1-rows[2*i+c])*cell_loss(ds[1],p,c) for c in range(2)))
    a=1-beta*T[0][0]; b=-beta*T[0][1]
    c=-beta*T[1][0]; d=1-beta*T[1][1]
    det=a*d-b*c
    if det<=0:
        raise RuntimeError('stochastic discounted resolvent is not invertible')
    return (1-beta)*(d*r[0]-b*r[1])/det

def round_simplex(row:tuple[F,...],Q:int)->tuple[F,...]:
    floors=[int(Q*x) for x in row]
    missing=Q-sum(floors)
    indices=sorted(range(len(row)),key=lambda j:(-(Q*row[j]-floors[j]),j))
    for j in indices[:missing]: floors[j]+=1
    return tuple(F(x,Q) for x in floors)

def run(output:Path|None=None)->dict:
    decisions=(F(7,16),F(1,2),F(9,16)); grid=(F(0),F(1,2),F(1))
    records=[]
    for ds in product(decisions,repeat=2):
        for rows in product(grid,repeat=4):
            r0,r1=risk(ds,rows,F(1,4)),risk(ds,rows,F(1,2))
            require(0<=r0<=1 and 0<=r1<=1,'risk outside probability bounds')
            for p in (F(5,16),F(3,8),F(7,16)):
                lam=(p-F(1,4))/F(1,4)
                require(risk(ds,rows,p)==(1-lam)*r0+lam*r1,'affine parameter reduction failed')
            records.append({'readouts':list(map(str,ds)),'row_prob_label1':list(map(str,rows)),'risk_p0':str(r0),'risk_p1':str(r1),'worst':str(max(r0,r1))})
    value=min(F(x['worst']) for x in records)
    require(len(records)==729,'enumeration incomplete')
    require(value==F(63,256),'unexpected robust optimum')
    selected=(F(1),F(0),F(1),F(0)); ds=(F(7,16),F(9,16))
    require(max(risk(ds,selected,p) for p in (F(1,4),F(1,2)))==value,'selected table not optimal')
    require(value-F(1,64)==F(59,256),'certificate lower')
    # Exact continuous-family formula and dyadic readout symmetry.
    for M in range(1,17):
        p0=F(1,4); mids=[-1+F(2*j+1,M) for j in range(M)]
        second=sum(z*z for z in mids)/M
        require(second==(1-F(1,M*M))/3,'uniform cell second moment')
        vv=F(1,4)-p0*p0*second/4
        require(vv==F(1,4)-p0*p0/12*(1-F(1,M*M)),'continuous risk formula')
    rounding_cases=0
    for den in (3,5,7):
        for a in range(den+1):
            for b in range(den-a+1):
                row=(F(a,den),F(b,den),F(den-a-b,den))
                for Q in (1,2,4,8,16):
                    rr=round_simplex(row,Q); rounding_cases+=1
                    require(sum(rr)==1 and min(rr)>=0,'rounded row invalid')
                    require(sum(abs(x-y) for x,y in zip(row,rr))/2<=F(len(row),Q),'TV rounding bound')
    # Diagonal multiplication and separate product-coordinate calculations.
    for m in range(1,9):
        bins=2**m; ones=bins//2
        require(F(ones,bins)==F(1,2),'dyadic mean')
        require(F(ones*ones,bins*bins)==F(1,4),'separate product coordinates')
        require(F(ones,bins)!=F(1,4),'diagonal counterexample')
    # Discount accumulation and sharp expansion regimes: exact finite sums plus tails.
    for beta in (F(1,4),F(1,2),F(3,4)):
        for k in range(1,9):
            s=F(1,2**k)
            exact=(1-beta)*sum(beta**(t-1)*2**t*s for t in range(1,k))+beta**(k-1)
            partial=(1-beta)*sum(beta**(t-1)*min(1,2**t*s) for t in range(1,k+20))
            require(exact-partial==beta**(k+19),'discount expansion tail')
    for beta,e in product((F(1,4),F(1,2),F(3,4)),(F(0),F(1,8),F(1,2),F(1))):
        exact=e/(4*(1-beta+beta*e))
        # Infinite geometric sum computed in closed rational form independently.
        series=(1-(1-beta)*(1-e)/(1-beta*(1-e)))/4
        require(exact==series,'erasure resolvent')
        require(exact<=min(F(1,4),e/(4*(1-beta))),'erasure Lipschitz allowance')
    report={'component':'R22 exact finite regression','assertions':CHECKS,'continuous_family_tables':len(records),'endpoint_evaluations':2*len(records),'interior_affinity_checks':3*len(records),'simplex_rounding_cases':rounding_cases,'optimal_value':str(value),'generic_report_error':'1/64','instance_value_rounding_error':'0','parameter_error':'0','evaluation_error':'0','interval':['59/256','63/256'],'analytic_tightened_interval':['63/256','63/256'],'selected_readouts':list(map(str,ds)),'selected_rows_label1':list(map(str,selected)),'limits':'Finite identities and complete stated 729-table search only. No continuum, priority, or general-complexity certification.'}
    if output:
        output.mkdir(parents=True,exist_ok=True)
        (output/'CONTINUOUS_CERTIFICATE.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        with (output/'CONTINUOUS_TABLES.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    print(json.dumps(run(args.output),sort_keys=True,indent=2))
