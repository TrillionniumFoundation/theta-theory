#!/usr/bin/env python3
"""Finite regression tests for formulas, not a proof of continuum estimates."""
from fractions import Fraction as F
from itertools import product
import cmath, math
import sympy as sp

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def multiply(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def collision(c, cp, v):
    return [[(v+c)/cp,v/(c*cp)],[v+c+cp,(v+cp)/c]]

def finite_checks():
    matrix_cases=0
    for m in range(1,7):
        for cs in product((F(1),F(1,2)),repeat=m-1):
            c=(F(1),)+cs+(F(1),)
            for v in (F(6,47),F(1),F(7,3)):
                mat=[[F(1),F(0)],[F(0),F(1)]]
                for j in range(m):
                    p=collision(c[j],c[j+1],v)
                    require(p[0][0]*p[1][1]-p[0][1]*p[1][0]==1,'one-flight determinant')
                    mat=multiply(p,mat)
                A,B=mat[0];C,D=mat[1]
                require(A*D-B*C==1 and min(A,B,C,D)>0,'positive symplectic product')
                require((A*C)*(B*D)-(B*C)**2==B*C,'critical Hessian determinant')
                require(A*C>0 and B*C>0,'critical Hessian definiteness')
                require(min(A,B,C,D)>=F(6,47)**m,'crude inverse-chart lower bound')
                matrix_cases+=1
    s=sp.symbols('s',real=True)
    a0,a1=sp.symbols('a0 a1',real=True)
    edge=sp.exp(-s)*(a0+(a0+a1)*s)
    require(sp.simplify(edge.subs(s,0)-a0)==0,'edge value')
    require(sp.simplify(sp.diff(edge,s).subs(s,0)-a1)==0,'edge first derivative')
    # Angular average, divided by pi, for a quartic source polynomial.
    radial_cases=0
    for c0,a,c,d,e,f in ((1,2,3,4,5,6),(2,-1,3,0,2,-1),(0,1,0,3,0,2)):
        average=2*c0+2*(a+c)*s+(3*d+e+3*f)*s*s
        require(average.subs(s,0)==2*c0,'radial constant')
        require(sp.diff(average,s).subs(s,0)==2*(a+c),'radial Laplacian coefficient')
        candidate=sp.exp(-s)*(2*c0+(2*c0+2*(a+c))*s)
        difference=average-candidate
        require(sp.simplify(difference.subs(s,0))==0 and sp.simplify(sp.diff(difference,s).subs(s,0))==0,'two-jet matching')
        radial_cases+=1
    phase_cases=0
    for d in range(1,10):
        for weights in ([F((i+1)**2) for i in range(d)],
                        [F(0 if i%3==1 else i+1) for i in range(d)]):
            omega=cmath.exp(2j*math.pi/d)
            for r in range(d):
                total=sum(weights[l]*weights[(l+r)%d] for l in range(d))
                if total:
                    require(sum(weights[l]*weights[(l+r)%d]/total for l in range(d))==1,'posterior normalization')
                for l in range(d):
                    dft=sum(omega**(-j*r)*float(weights[l])*omega**(-j*l)*
                            sum(float(weights[h])*omega**(j*h) for h in range(d)) for j in range(d))
                    expected=float(d*weights[l]*weights[(l+r)%d])
                    require(abs(dft-expected)<1e-7*(1+abs(expected)),'phase orientation or residue coefficient')
                    phase_cases+=1
    stopping_cases=0
    for length in range(2,7):
        for eta in product((0,1),repeat=length):
            for start in range(length):
                if not eta[start]: continue
                for n in range(1,4):
                    hits=[j for j in range(1,n*length+1) if eta[(start+j)%length]]
                    m=hits[n-1]
                    require(sum(eta[(start+j)%length] for j in range(m))==n,'actual stopped occupation')
                    require(eta[(start+m)%length]==1,'terminal section')
                    # A bad guard strictly after m must not alter the stopped product.
                    guards=[1]*(m+2);guards[m+1]=0
                    require(math.prod(guards[:m+1])==1 and math.prod(guards)==0,'post-terminal guard leaked into source')
                    stopping_cases+=1
    rejected=0
    def must_reject(check):
        try: check()
        except RuntimeError: return 1
        raise RuntimeError('negative control not rejected')
    rejected+=must_reject(lambda:require(-F(2)==F(3),'a single exponential must not be mistaken for two-jet subtraction'))
    w=(F(1),F(2),F(4))
    rejected+=must_reject(lambda:require(w[0]*w[1]==w[0]*w[-1],'reversed residue orientation'))
    rejected+=must_reject(lambda:require(F(1)==F(2),'missing factor two in integral of b^-2 on both tails'))
    return {'positive_matrix_cases':matrix_cases,'quartic_radial_cases':radial_cases,
            'finite_phase_cases':phase_cases,'actual_stopping_cases':stopping_cases,
            'negative_controls_rejected':rejected,'tail_constant':'1/pi',
            'new_uniform_raw_LLT_claimed':False,'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),sort_keys=True,indent=2))
