#!/usr/bin/env python3
"""Finite exact-arithmetic diagnostics for the A2 v70 review.
No author modules are imported. Run under Python and Python -O and compare JSON.
Requires SymPy. These checks do NOT certify infinite-dimensional or probability
limit theorems, billiard realizability, originality, or optimal sample complexity.
"""
from __future__ import annotations
import itertools, json, math
from collections import defaultdict
from fractions import Fraction as F
import sympy as sp

def require(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    counts=defaultdict(int)
    for r in (2,3,4):
        for seed in (1,2,3):
            k=[sp.Rational(seed+i+2,i+1) for i in range(r)]
            m=[sp.Rational(seed+i+1,seed+i+3) for i in range(r)]
            M=sp.eye(2)
            for i in range(r):
                M=sp.Matrix([[1+m[i]/k[i],1/k[i]],[m[i],1]])*M
            require(M.det()==1,'transfer determinant')
            a,b=sp.Integer(0),sp.Integer(1)
            for n in range(1,5):
                N=r*n; H=sp.zeros(N-1)
                for j in range(1,N):
                    H[j-1,j-1]=k[(j-1)%r]+k[j%r]+m[j%r]
                    if j<N-1:
                        H[j-1,j]=H[j,j-1]=-k[j%r]
                cofactor=sp.prod(k[j%r] for j in range(N))/H.det()
                require(cofactor==1/(M**n)[0,1],'cofactor/transfer mismatch')
                require((M**n)[0,1]==b*M[0,1],'Cayley-Hamilton offdiagonal')
                counts['cofactor_transfer_and_Cayley_Hamilton_cases']+=1
                a,b=b,sp.trace(M)*b-a
    for r in (2,3,4,5):
        for signs in ((1,)*r,(-1,)+(1,)*(r-1)):
            sig=[sp.Rational(signs[i]*(i+1),i+3) for i in range(r)]
            lam=sp.prod(sig); astar=max(abs(x) for x in sig)
            for n in range(2,9):
                T=sp.zeros(r)
                for i in range(r):T[i,(i+1)%r]=sig[i]**n
                require(T**r==lam**n*sp.eye(r),'signed cyclic power')
                C=(sp.eye(r)+T)*(sp.eye(r)-T).inv()
                require(C.det()==(1-(-1)**r*lam**n)/(1-lam**n),'signed determinant')
                inv=C.inv()
                require(max(sum(abs(x) for x in inv.row(i)) for i in range(r)) <= (1+astar**n)/(1-astar**n),'inverse norm')
                counts['signed_cyclic_matrix_cases']+=1
    for d1,d2 in ((F(2),F(5)),(F(1),F(3)),(F(3),F(4))):
        for h in (F(-1,3),F(1,7),F(2,5)):
            for z1,z2 in ((F(2),F(7)),(F(5,2),F(3,2))):
                for amp in (F(4,3),F(9,5)):
                    f1=amp*(d1-h)/z1; f2=amp*(d2-h)/z2
                    q=f1*(d2/z2)/(f2*(d1/z1))
                    H=d1*d2*(1-q)/(d2-d1*q)
                    require(H==h,'two-offset extraction')
                    badq=f1/f2
                    if d2-d1*badq:
                        badH=d1*d2*(1-badq)/(d2-d1*badq)
                        require(badH!=h,'unanchored-ratio control not detected')
                        counts['unanchored_normalizer_controls_detected']+=1
                    counts['two_offset_cases']+=1
    for m,s,omega,Gamma in itertools.product((3,5,8,20),(1,2,4,8),(F(1,3),F(1),F(2)),(F(1,2),F(1),F(4))):
        den=2*(m+s)+2; h_exp=F(1,den);alpha=F(s,den)
        gamma=F(s,m+s+3);t=alpha/(omega+alpha*Gamma);beta=omega*t
        require(F(1,2)-(m+1)*h_exp==alpha,'variance balance')
        require(1-(m+2)*h_exp>=alpha,'Bernstein linear term')
        require(1-F(m+3,m+s+3)==gamma,'readout balance')
        require(alpha*(1-Gamma*t)==beta and 0<beta<alpha,'rarity balance')
        wrong_h=F(1,2*(m+s)+1)
        require(s*wrong_h != F(1,2)-(m+1)*wrong_h,'wrong dimension undetected')
        require(alpha*(1-Gamma*alpha/omega)!=alpha,'omitted rarity undetected')
        counts['rate_cases']+=1;counts['dimension_and_rarity_controls_detected']+=2
    for p in (F(1,4),F(2,3)):
        probs=(1-p,p*F(2,5),p*F(3,5));total=F(0);marks=defaultdict(F)
        for record in itertools.product(range(3),repeat=5):
            weight=math.prod(probs[x] for x in record)
            success=tuple(x for x in record if x)
            if len(success)>=2:
                total+=weight;marks[success[:2]]+=weight
        expected=sum(F(math.comb(5,j))*p**j*(1-p)**(5-j) for j in range(2,6))
        require(total==expected,'binomial success probability')
        counts['exact_binomial_normalizations']+=1
        for pair,weight in marks.items():
            require(weight/total==math.prod(F(2,5) if x==1 else F(3,5) for x in pair),'conditional mark law')
            counts['conditional_first_success_mark_identities']+=1
    thresholds=[]
    for a in (F(1,2),F(2,3),F(9,10),F(99,100)):
        m=2
        while 6*a**m/(1-a**m)>=1:m+=1
        theta=6*a**m/(1-a**m)
        require(theta<1,'weighted threshold')
        require(6*(2*a)**m/(1-a**m)>=1,'constant-one distinction control')
        thresholds.append({'a':str(a),'first_admissible_m':m,'theta_less_than_one':True})
        counts['weighted_threshold_cases']+=1
    print(json.dumps({'status':'passed','counts':dict(counts),'weighted_thresholds':thresholds,
        'author_code_imported':False,'arithmetic':'exact rational',
        'scope':'Finite diagnostics and deliberate negative controls, not theorem or priority certificates.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
