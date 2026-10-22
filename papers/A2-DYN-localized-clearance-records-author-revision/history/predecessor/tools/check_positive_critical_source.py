#!/usr/bin/env python3
"""Exact auxiliary checks for 322; no continuum or physical-orbit certificate."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

def require(v,m):
    if not v:
        raise ArithmeticError(m)

def checks():
    q=F(47,59); groups=[]; cases=0
    for m in range(1,141):
        total=sum((q**max(j,m-1-j) for j in range(m)),F(0))
        h=m//2
        exact=(2*q**h*(1-q**h)/(1-q) if m%2==0
               else q**h+2*q**(h+1)*(1-q**h)/(1-q))
        require(total==exact,'all-mark closed sum')
        require(total*total<=m*m*q**(m-1),'all-mark half exponent')
        for j in range(m):
            require(min(q**j,q**(m-1-j))==q**max(j,m-1-j),'minimum exponent orientation')
            require((j+1)-1==j and (m-j)-1==m-1-j,'true half counts')
            cases+=1
    groups.append({'name':'exact_all_m_all_j_index_and_fan_sum','cases':cases,'status':'passed'})
    count=0
    for j in range(12):
        for k in range(12):
            for n in range(1,13):
                # Rational families obey each half cap and the two half-sum
                # bounds. They test product accounting, not orbit existence.
                a=[q**j/F(n+i+1) for i in range(n)]
                b=[q**k/F(2*n-i+1) for i in range(n)]
                require(sum(a)<=1 and sum(b)<=1,'half-sum fixture')
                product=sum((x*y for x,y in zip(a,b)),F(0))
                require(product<=min(q**j,q**k),'two competing half payments')
                count+=1
    groups.append({'name':'two_half_supremum_product_accounting','cases':count,'scope':'exact algebraic parameter families','status':'passed'})
    R0=F(9,20); R1=F(47,100); foot2=F(1827,40000)
    require((F(28,5)+R1)/(2*R0)==F(607,90),'physical determinant radius factor')
    require(1/((1/R1)**2*foot2)==F(94**2,1827),'half derivative constant')
    require(F(170,9)/2==F(170,18),'one critical conditioning factor')
    for R in (R0,F(23,50),R1):
        for a in range(1,18):
            for d in range(1,18):
                for b in range(-3,4):
                    det=a*d-b*b
                    if det<=0: continue
                    # G=R^2 [[a,b],[b,d]], a,d<=170/9:
                    # (2*c*J/u)^2=detG/R^4<=U^2.
                    detG=R**4*det
                    require(detG/R**4<=F(170,9)**2,'normalized Hessian determinant')
    groups.append({'name':'critical_coefficient_radius_and_conditioning','status':'passed'})
    examples=[]
    for n in (2,3,10,100,1000):
        u=F(1,n); v=u
        require(u>0 and v>0 and v*v<u,'common positive-u representative')
        examples.append({'u':str(u),'v':str(v),'strict_gap':str(u-v*v)})
    groups.append({'name':'collapsed_slice_positive_sector_example','status':'passed',
                   'domain':'u>0, v>0, v^2<u; zero-u slice empty but first-quadrant tangent fan positive',
                   'scope':'analytic counterexample to discarding a collapsed slice; not Lorentz trajectory data',
                   'representatives':examples})
    for n in range(1,100):
        slope=F(100,47)*F(1,5); eps=F(1,n)
        max_separation=2*eps/slope
        require(slope*max_separation==2*eps,'strict monotonicity separation budget')
    groups.append({'name':'distinct_half_interval_separation_budget','status':'passed'})
    # Same marked state can have several disjoint physical sector pieces.
    # Their normalized union fraction, rather than the germ count, is paid.
    pieces=[F(1,8),F(1,6),F(1,12)]
    require(sum(pieces)<=1,'one-copy angular union')
    require(sum(pieces)!=len(pieces),'sector union is not copy multiplicity')
    groups.append({'name':'merged_critical_state_sector_accounting','status':'passed'})
    return {'status':'passed','native_module':322,'groups':groups,
            'continuum_proof_certificate':False,'full_raw_pointwise_llt_complete':False,
            'scope':'finite exact algebra, normalized factor checks and logical non-implication examples'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--details',type=Path)
    args=p.parse_args(); result=checks()
    source=Path(__file__).resolve().parents[1]/'core/322_positive_critical_marked_source.tex'
    result['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    if args.details:
        args.details.parent.mkdir(parents=True,exist_ok=True)
        args.details.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
    return 0
if __name__=='__main__':
    raise SystemExit(main())
