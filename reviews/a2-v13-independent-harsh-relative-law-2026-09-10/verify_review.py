#!/usr/bin/env python3
"""Independent finite rational diagnostics for the pinned A2 v13 review.
No manuscript imports, floating-point quadrature, assertions, or external packages.
This is not a proof of any infinite-dimensional or statistical theorem.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import comb, factorial
from pathlib import Path
import json

checks = []

def check(category, label, condition, detail=''):
    if not condition:
        raise RuntimeError(f'{category}: {label}: {detail}')
    checks.append([category, label])

def matrix_inverse(a):
    det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
    if not det:
        raise ValueError('singular matrix')
    return [[a[1][1]/det, -a[0][1]/det],[-a[1][0]/det, a[0][0]/det]]

def product(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def finite_row(g, cb, co, m):
    h=[[ (cb-F(1,2)/co)/g, -F(1,2)/(co*g)],
       [-F(1,2)/(co*g), (cb-F(1,2)/co)/g]]
    c=matrix_inverse(h)
    @lru_cache(None)
    def gaussian(i,j):
        if min(i,j)<0 or (i+j)%2:
            return F(0)
        if i+j==0:
            return F(1)
        if i:
            return (i-1)*c[0][0]*gaussian(i-2,j)+j*c[0][1]*gaussian(i-1,j-1)
        return (j-1)*c[1][1]*gaussian(0,j-2)
    def ellipse(poly, weighted):
        result=F(0)
        for (i,j),coef in poly.items():
            if (i+j)%2:
                continue
            n=(i+j)//2
            factor=F(2, factorial(n)*(n+1)*(n+2 if weighted else 1))
            result+=coef*factor*gaussian(i,j)
        return result
    own={(2*m,0):F(1,factorial(2*m)),(0,2*m):F(1,factorial(2*m))}
    other={(i,2*m-i):F(2*comb(2*m,i),factorial(2*m))/(2*co)**(2*m) for i in range(2*m+1)}
    d0=F(1)/(2*g*co)
    def variation(poly):
        twist={(i-1,j-1):-coef*i*j/d0 for (i,j),coef in poly.items() if i and j}
        return -ellipse(poly,False)+ellipse(twist,True)
    return [variation(own),variation(other)],h,c

def run():
    for g in [F(1,2),F(1),F(3,2)]:
        for c0 in [F(3,2),F(2),F(5,2)]:
            for c1 in [F(4,3),F(2),F(3)]:
                z=c0*c1-1
                ls=[g/(2*c0*z),g/(2*c1*z)]
                for m in range(2,10):
                    k=F(4,2**m*(m+1)*factorial(m)**2)
                    u=(1+2*z)**m
                    v=1+2*m*z
                    key=f'g={g};c0={c0};c1={c1};m={m}'
                    matrix=[]
                    for b,cb,co in [(0,c0,c1),(1,c1,c0)]:
                        row,h,c=finite_row(g,cb,co,m)
                        expected=[-k*ls[b]**m*u,-k*ls[1-b]**m*v]
                        check('two_flight',key+f';orientation={b};action_twist_moments',row==expected)
                        check('two_flight',key+f';orientation={b};schur_inverse',product(h,c)==[[1,0],[0,1]])
                        check('two_flight',key+f';orientation={b};endpoint_variance',c[0][0]==ls[b]*(1+2*z))
                        middle=(c[0][0]+2*c[0][1]+c[1][1])/(4*co*co)
                        check('two_flight',key+f';orientation={b};middle_variance',middle==ls[1-b])
                        matrix.append(row if b==0 else list(reversed(row)))
                    check('two_flight',key+';positive_binomial_remainder',u-v==sum(F(comb(m,r))*(2*z)**r for r in range(2,m+1)) and u>v>0)
                    det=matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
                    check('two_flight',key+';determinant',det==k*k*(ls[0]*ls[1])**m*(u*u-v*v) and det>0)
                    check('two_flight',key+';block_inverse',product(matrix,matrix_inverse(matrix))==[[1,0],[0,1]])
    row,_,_=finite_row(F(1),F(2),F(2),2)
    check('two_flight','printed_quartic_example',row==[-F(49,1728),-F(13,1728)])
    check('two_flight','printed_antisymmetric_eigenvalue',row[1]-row[0]==F(1,48))
    for t in [F(1,9),F(1,4),F(1,2),F(3,4),F(9,10)]:
        for m in range(2,13):
            e=t**(2*(m-1))/(1-t**(2*(m-1)))-t**(2*m)/(1-t**(2*m))
            o=t**(m-1)/(1-t**(2*(m-1)))-t**m/(1-t**(2*m))
            p=(1+t**(2*m))/(1-t**(2*m))+2*m*e
            q=2*t**m/(1-t**(2*m))+2*m*o
            minus=m*(1-t**(m-1))/(1+t**(m-1))-(m-1)*(1-t**m)/(1+t**m)
            plus=(1+t**m)/(1-t**m)+2*m*(t**(m-1)/(1-t**(m-1))-t**m/(1-t**m))
            key=f't={t};m={m}'
            check('limiting_block',key+';minus_identity',p-q==minus)
            check('limiting_block',key+';plus_identity',p+q==plus)
            check('limiting_block',key+';positivity',p>q>0 and minus>0)
    def beta_coefficient(i,j):
        return F(2*factorial(2*i)*factorial(2*j),4**(i+j)*factorial(i)*factorial(j)*factorial(i+j+2))
    def forward(a,b):
        out=[F(0)]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):
                out[i+j]+=beta_coefficient(i,j)*x*y
        return out
    def kernel(law):
        return [F((n+1)*(n+2),2)*x for n,x in enumerate(law)]
    def convolve(a,b):
        out=[F(0)]*(len(a)+len(b))
        for i,x in enumerate(a):
            for j,y in enumerate(b):
                out[i+j+1]+=x*y*F(factorial(i)*factorial(j),factorial(i+j+1))
        return out
    for n in range(41):
        lam=2*beta_coefficient(n,0)
        closed=F(4*comb(2*n,n),4**n*(n+1)*(n+2))
        abel_over_2pi=F((n+1)*(n+2)*4**n*factorial(n)**2,4*factorial(2*n))
        check('abel_and_profiles',f'n={n};linearization',lam==closed)
        check('abel_and_profiles',f'n={n};abel_inverse_with_endpoint',lam*abel_over_2pi==1)
    for seed in range(1,11):
        a=[F(1)]+[F((-1)**(seed+i)*seed,100*(i+1)) for i in range(1,5)]
        b=[F(1)]+[F((-1)**i,70*(seed+i)) for i in range(1,4)]
        aa,ab,bb=forward(a,a),forward(a,b),forward(b,b)
        check('abel_and_profiles',f'profile_pair={seed};volterra_compatibility',convolve(kernel(ab),kernel(ab))==convolve(kernel(aa),kernel(bb)))
        recovered=[F(1)]
        for n in range(1,len(a)):
            lower=sum(beta_coefficient(i,n-i)*recovered[i]*recovered[n-i] for i in range(1,n))
            recovered.append((aa[n]-lower)/(2*beta_coefficient(n,0)))
            check('abel_and_profiles',f'profile_pair={seed};triangular_inverse={n}',recovered[n]==a[n])
    for m in range(4,31):
        nu=F(2*m-1,2)
        rate=2+6/nu
        pilot=2+F(2,m)
        modulus=nu/(m+2)
        check('sampling_algebra',f'm={m};pilot_power_gap',rate>pilot)
        check('sampling_algebra',f'm={m};mesh_noise_balance',1-F(5,2)/(m+2)==modulus)
        check('sampling_algebra',f'm={m};preparation_power',2+(1+5)/nu==rate)
    check('sampling_algebra','m=4;printed_power',2+6/F(7,2)==F(26,7))
    payload=json.dumps(checks,separators=(',',':'),ensure_ascii=True).encode()
    return {
        'schema':'a2-v13-independent-review-checks/1',
        'reviewed_commit':'0e54099f079232df233316ae6fe7986fc51b7ea1',
        'status':'PASS',
        'checks_total':len(checks),
        'checks_by_category':dict(sorted(Counter(c[0] for c in checks).items())),
        'ordered_check_ids_sha256':sha256(payload).hexdigest(),
        'quartic_example':{'g':'1','c0':'2','c1':'2','m':2,'row':['-49/1728','-13/1728'],'antisymmetric_magnitude':'1/48'},
        'limitations':['Finite exact algebra only; no theorem certification.','No author verification suite or manuscript code imported.','No nonlinear billiard simulation, native TeX build, PDF inspection, or remote CI.','No numerical experiment is used as proof of an all-order or statistical assertion.']
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    text=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')
    else:
        print(text,end='')
