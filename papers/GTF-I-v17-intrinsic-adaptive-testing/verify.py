#!/usr/bin/env python3
"""Exact finite certificates and diagnostic counterchecks; not an analytic proof verifier."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from math import comb,isqrt,factorial
from pathlib import Path
import sys
import sympy as s

HERE=Path(__file__).resolve().parent
MUTANTS=('negative_coefficient','wrong_adaptive_weight','convexify_private','hide_visible_seed','drop_actual_mark','erase_collision','omit_bayes_denominator','halve_presentation_error')

class Checker:
    def __init__(self,mutant:str|None=None): self.count=0;self.mutant=mutant
    def need(self,ok:bool,message:str)->None:
        self.count+=1
        if not ok: raise RuntimeError('FAILED: '+message)

def tv(p:dict,q:dict)->Q:return sum((abs(p.get(k,Q(0))-q.get(k,Q(0)))for k in set(p)|set(q)),Q(0))/2

def sqrt_interval(x:Q,digits:int=25)->tuple[Q,Q]:
    scale=10**digits;k=isqrt(x.numerator*scale*scale//x.denominator)
    return Q(k,scale),Q(k+1,scale)

def push(p:dict,g:tuple[int,int])->dict:
    r={}
    for(w,b,c),z in p.items():
        k=(w,b,g[b],g[b]*c);r[k]=r.get(k,Q(0))+z
    return r

def bernstein(poly:s.Poly,n:int)->list[Q]:
    return [sum((Q(int(c.p),int(c.q))*Q(comb(k,i),comb(n,i))for(i,),c in poly.terms()if k>=i),Q(0))for k in range(n+1)]

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=MUTANTS);parser.add_argument('--write-certificates',type=Path);args=parser.parse_args();ck=Checker(args.mutant)
    p,q,a,b,c,t=s.symbols('p q a b c t');u=p*q;v=(1-p)*(1-q);J=lambda z:3*z*z-2*z*z*z
    ck.need(s.expand(J(t)+J(1-t)-1)==0,'majority-complement identity')
    ck.need(s.expand(s.diff(J(t),t)-6*t*(1-t))==0,'majority monotonicity identity')
    weights=[J(v),J(u),1-J(u)-J(v)]
    if args.mutant=='wrong_adaptive_weight':weights[2]+=1
    ck.need(s.expand(sum(weights)-1)==0,'adaptive weights must sum to one')
    G=s.expand(sum(w*f for w,f in zip(weights,[s.Rational(1,2)-u,s.Rational(1,2)-v,1-u-v])))
    Ga=(27-12*a+38*a*a-20*a**3-a**4+36*b-60*a*b+36*a*a*b+4*a**3*b+6*b*b-12*a*b*b-6*a*a*b*b-4*b**3+4*a*b**3-b**4)/64
    ck.need(s.expand(G-Ga.subs({a:(p+q-1)**2,b:(p-q)**2}))==0,'behavior-to-square chart identity')
    H=4*a**3+6*a*a*c+12*a*b*b+24*a*b*c+12*a*c*c+8*b**3+30*b*b*c+30*b*c*c+9*c**3
    ck.need(s.expand(16*s.diff(Ga,b)-H.subs(c,1-a-b))==0,'nonnegative derivative identity')
    for coeff in s.Poly(H,a,b,c).coeffs():ck.need(coeff>0,'derivative coefficient positive')
    diag=s.Poly(Ga.subs(b,0)-s.Rational(2,5),a);nums=[7644,3549,1183,351,855,2494,5064,8358,12166,16275,20469,24529,28233,31356,33670,34944,34944];den=349440
    if args.mutant=='negative_coefficient':nums[3]=-351
    coeffs=bernstein(diag,16)
    for i,z in enumerate(nums):ck.need(Q(z,den)==coeffs[i] and z>0,'exact positive univariate coefficient '+str(i))
    expansion=sum(s.Rational(z,den)*comb(16,k)*a**k*(1-a)**(16-k)for k,z in enumerate(nums))
    ck.need(s.expand(expansion-diag.as_expr())==0,'exact elevated Bernstein identity')
    ck.need(min(coeffs)==Q(9,8960),'uniform certified margin')
    affine=s.expand(v*(s.Rational(1,2)-u)+u*(s.Rational(1,2)-v)+(1-u-v)**2-s.Rational(3,8))
    ck.need(s.expand(affine-((p-q)**2/2+2*(p-s.Rational(1,2))**2*(q-s.Rational(1,2))**2))==0,'two-square affine certificate')
    # Quantitative hierarchy constants: binomial variances and exact degree elevation.
    for n in (1,2,4,8):
        for x in (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)):
            law=[Q(comb(n,k))*x**k*(1-x)**(n-k)for k in range(n+1)]
            ck.need(sum(law)==1,'binomial normalization')
            ck.need(sum(law[k]*(Q(k,n)-x)**2 for k in range(n+1))==x*(1-x)/n,'binomial variance identity')
    # Marked target and exact rational upper tables close to algebraic optimum.
    target={(w,b,b):Q(5 if w==b else 3,16)for w,b in itertools.product(range(2),repeat=2)}
    ck.need(sum(target.values())==1,'marked target normalization')
    rlo,rhi=sqrt_interval(Q(5,8));dlo,dhi=sqrt_interval(Q(5,2));dlo-=Q(9,8);dhi-=Q(9,8)
    par=(rlo+rhi)/2
    private={(w,b,c):Q(1,2)*(par if b else 1-par)*(par if c else 1-par)for w,b,c in itertools.product(range(2),repeat=3)}
    hidden={(w,b,b):Q(1,4)for w,b in itertools.product(range(2),repeat=2)}
    if args.mutant=='convexify_private':private=hidden
    ck.need(dlo-Q(1,10**23)<tv(private,target)<dhi+Q(1,10**23),'private nonconvex all-on optimum')
    hidden_value=tv(hidden,target)
    if args.mutant=='drop_actual_mark':hidden_value=Q(0)
    ck.need(hidden_value==Q(1,8),'actual mark remains in the hidden comparison')
    for gate in itertools.product(range(2),repeat=2):
        ck.need(tv(push(private,gate),push(target,gate))<=tv(private,target),'private feedback contraction '+str(gate))
        ck.need(tv(push(hidden,gate),push(target,gate))<=Q(1,8),'hidden feedback contraction '+str(gate))
    # A visible fair selector choosing constant paths has joint, not marginalized, error 1/2.
    vt={(j,w,b,b):z/2 for j in range(2)for(w,b,_),z in target.items()}
    vs={(j,w,j,j):Q(1,4)for j,w in itertools.product(range(2),repeat=2)}
    visible_value=tv(vs,vt)
    if args.mutant=='hide_visible_seed':visible_value=tv(hidden,target)
    ck.need(visible_value==Q(1,2),'visible selector target law is joint and independent')
    # Uniform geometric inequalities in the proof, with rational arithmetic only.
    ck.need(Q(61,50)>Q(11,10),'pre-contact separation')
    ck.need(Q(1,4)**2+Q(113,200)**2+Q(1,40)**2<Q(9,10)**2,'entry before 3/2')
    ck.need((Q(11,20)+Q(31,1900))**2+(Q(1,100)+Q(31,1900))**2<Q(9,10)**2,'entry before free x-zero')
    ck.need(1-(Q(113,200)**2+Q(1,40)**2)/Q(9,10)**2>Q(77,100)**2,'normal x-margin')
    ck.need((Q(9,20)-Q(3,200))/Q(11,10)==Q(87,220),'normal y-margin')
    ck.need(Q(19,10)*Q(77,100)-Q(2,100)==Q(1443,1000),'incoming flux margin')
    lower=-Q(3,200)+Q(1443,1000)*Q(87,220)
    if args.mutant=='erase_collision':lower=-Q(3,200)
    ck.need(lower>Q(1,2),'scattering creates detector signal')
    ck.need(Q(9,20)-Q(3,100)>Q(2,5),'small-diameter no-collision regime')
    ck.need(Q(3,200)<Q(1,4),'incoming detector is zero')
    expsum=sum((Q(9,2)**k/Q(factorial(k))for k in range(14)),Q(0));ck.need(expsum>80,'positive Taylor lower bound exp(9/2)>80')
    # Machin identity with rational alternating-series enclosure for pi.
    def atan_bounds(x:Q,N:int)->tuple[Q,Q]:
        partial=sum(((-1)**k*x**(2*k+1)/Q(2*k+1)for k in range(N)),Q(0));tail=x**(2*N+1)/Q(2*N+1)
        return (partial,partial+tail) if N%2==0 else (partial-tail,partial)
    a5,b5=atan_bounds(Q(1,5),8);a239,b239=atan_bounds(Q(1,239),4);pi_lower=16*a5-4*b239
    ck.need(pi_lower>Q(25,8),'Machin enclosure supplies sqrt(2pi)>5/2')
    ck.need(Q(1,80)/3/Q(5,2)==Q(1,600),'one-report Gaussian bound')
    ck.need(dlo-Q(1,300)>Q(9,20),'physical private lower > .45')
    ck.need(Q(1,8)+Q(1,300)<Q(13,100),'physical hidden upper < .13')
    # A finite posterior tree: Bayes denominator and full-time estimate.
    P={(0,0,0):Q(1,5),(0,0,1):Q(1,10),(0,1,0):Q(1,10),(0,1,1):Q(1,10),
       (1,0,0):Q(1,10),(1,0,1):Q(1,10),(1,1,0):Q(3,20),(1,1,1):Q(3,20)}
    QQ={k:Q(1,8)for k in P};eps=tv(P,QQ)
    ck.need(all(sum(z for k,z in P.items()if k[0]==w)==Q(1,2)for w in range(2)),'common latent marginal')
    maxdiff={}
    for path in itertools.product(range(2),repeat=2):
        differences=[]
        for time in range(3):
            keys=[k for k in QQ if k[1:1+time]==path[:time]];qm=sum(QQ[k]for k in keys);pm=sum(P[k]for k in keys)
            mf=lambda k:2*k[0]-1
            mp=sum(P[k]*mf(k)for k in keys)/pm;mq=sum(QQ[k]*mf(k)for k in keys)/qm
            A=sum((P[k]-QQ[k])*mf(k)for k in keys)/qm;B=pm/qm-1
            denominator=1 if args.mutant=='omit_bayes_denominator' else 1+B
            ck.need(mp-mq==(A-B*mq)/denominator,'Bayes posterior difference identity')
            differences.append((mp-mq)**2)
        maxdiff[path]=max(differences)
    expected=sum(sum(QQ[k]for k in QQ if k[1:]==path)*val for path,val in maxdiff.items())
    ck.need(expected<=80*eps,'finite whole-posterior diagnostic')
    # Common output transformation cannot cost only half a sharp total variation error.
    err=Q(1,10);claimed=err/2 if args.mutant=='halve_presentation_error' else err
    ck.need(tv({0:Q(1)},{0:1-err,1:err})<=claimed,'stateless presentation error must be paid')
    # Degree-zero constant mixtures cannot witness the fair target against both constant paths.
    for lam in (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)):
        left=lam*Q(1,2)+(1-lam)*(-Q(1,2));right=-left
        ck.need(min(left,right)<=0,'constant-test barycenter obstruction')
    if args.mutant:raise RuntimeError('designated mutant survived')
    payload={'weight_polynomial':'J(t)=3t^2-2t^3','behavior_weights':['J(v)','J(u)','1-J(u)-J(v)'],
      'lower_level':'2/5','margin':'9/8960','univariate_degree':16,'denominator':den,'numerators':nums,
      'derivative_monomials':[{'powers':list(k),'coefficient':int(z)}for k,z in s.Poly(H,a,b,c).terms()],
      'raw_row_dimension':2,'full_law_affine_dimension':3,'selected_test_observable_dimension':2,'occupied_test_weights':3,'test_degree_in_behavior':3,
      'univariate_positive_coefficients':17,'derivative_nonnegative_terms':9,
      'largest_integer_bit_length':max(den.bit_length(),*(x.bit_length()for x in nums)),
      'boundary_claim':'strict lower bound only; not the optimal value'}
    geometric={'mark_same':'5/16','mark_different':'3/16','private_interval':[str(dlo),str(dhi)],'private_formula':'sqrt(5/2)-9/8','hidden_value':'1/8','diameter_interval':['9/10','11/10'],'noise_upper':'1/12','physical_error_upper':'1/300','no_collision_diameter_upper':'2/5','incoming_flux_lower':'1443/1000','outgoing_signed_velocity_lower':str(lower),'scope':'Exact rational bounds for the specified two-sphere boxes. No particle-uniform or kinetic claim.'}
    if args.write_certificates:
        args.write_certificates.mkdir(parents=True,exist_ok=True)
        for name,obj in [('ADAPTIVE_CERTIFICATE.json',payload),('COLLISION_CERTIFICATE.json',geometric)]:
            (args.write_certificates/name).write_text(json.dumps(obj,indent=2)+'\n')
    encoded=(json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode()
    print(json.dumps({'status':'passed','checks':ck.count,'adaptive':payload,'adaptive_compact_json_bytes':len(encoded),'adaptive_compact_json_sha256':hashlib.sha256(encoded).hexdigest(),'collision':geometric,'posterior_tree':{'joint_TV':str(eps),'expected_squared_uniform_difference':str(expected)},'scope':'Exact polynomial/rational instance checks and finite diagnostics, not verification of analytic theorems.'},indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print(str(e),file=sys.stderr);sys.exit(1)
