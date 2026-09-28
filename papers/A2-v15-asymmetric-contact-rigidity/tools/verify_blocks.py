#!/usr/bin/env python3
"""Exact finite diagnostics for A2 v15; not a mathematical proof certificate.

Reconstruct the homogeneous action variation as a polynomial, differentiate
it for the twist, and integrate monomials by Gaussian pairings on the ellipse.
This does not import manuscript formulas as the integration implementation.
Uses only the Python standard library; checks survive python -O.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import factorial, comb
import json

checks = {}
def require(ok, category, message):
    checks[category] = checks.get(category, 0) + 1
    if not ok:
        raise ArithmeticError(f'{category}: {message}')

def add(a, b):
    result = a.copy()
    for key, value in b.items():
        result[key] = result.get(key, F(0)) + value
    return {k:v for k,v in result.items() if v}

def scale(p, a):
    return {k:v*a for k,v in p.items() if v*a}

def multiply(p, q):
    result = {}
    for (i,j), a in p.items():
        for (k,l), b in q.items():
            key=(i+k,j+l)
            result[key]=result.get(key,F(0))+a*b
    return result

def derivative(p, axis):
    result={}
    for (i,j),a in p.items():
        degree=(i,j)[axis]
        if degree:
            result[(i-(axis==0),j-(axis==1))]=a*degree
    return result

def power_linear(a,b,n):
    return {(i,n-i):F(comb(n,i))*a**i*b**(n-i) for i in range(n+1)}

def ellipse_integral(p, covariance, weighted):
    """Integral / I0 at d=1, via Wick pairings and radial integration."""
    c00,c01,c11=covariance
    @lru_cache(None)
    def pairing(i,j):
        if (i+j)%2: return F(0)
        if i+j==0: return F(1)
        if i:
            return ((i-1)*c00*pairing(i-2,j) if i>=2 else F(0)) + \
                   (j*c01*pairing(i-1,j-1) if j else F(0))
        return (j-1)*c11*pairing(0,j-2)
    total=F(0)
    for (i,j),value in p.items():
        if (i+j)%2==0:
            r=(i+j)//2
            total+=value*pairing(i,j)*F(2,factorial(r+2 if weighted else r+1))
    return total

def direct_block(g,c0,c1,degree):
    cs=(c0,c1); z=c0*c1-1; mark={(1,0):F(1),(0,1):F(1)}
    result=[]
    for b in (0,1):
        cb,co=cs[b],cs[1-b]; L=g/(2*cb*z)
        covariance=(L*(1+2*z),L,L*(1+2*z))
        row=[]
        for contact in (0,1):
            if contact==b:
                action={(degree,0):F(1,factorial(degree)),
                        (0,degree):F(1,factorial(degree))}
            else:
                action=scale(power_linear(1/(2*co),1/(2*co),degree),
                             F(2,factorial(degree)))
            twist=scale(derivative(derivative(action,0),1), -2*g*co)
            if degree%2:
                action=multiply(mark,action); twist=multiply(mark,twist)
            row.append(-ellipse_integral(action,covariance,False)
                       +ellipse_integral(twist,covariance,True))
        result.append(row)
    return result

def formula_block(g,c0,c1,degree):
    z=c0*c1-1; R=1+2*z; cs=(c0,c1)
    L=[g/(2*c*z) for c in cs]
    m=degree//2; V=1+2*m*z
    if degree%2:
        C=F(2)**(2-m)/((m+1)*(m+2)*factorial(m)**2)
        return [[-(cs[1-b]*R**m if b==j else V)
                 *2*cs[j]*C*L[j]**(m+1) for j in (0,1)] for b in (0,1)]
    k=F(4,2**m*(m+1)*factorial(m)**2)
    return [[-(R**m if b==j else V)*k*L[j]**m for j in (0,1)] for b in (0,1)]

def determinant(matrix):
    a=[list(map(F,row)) for row in matrix]; n=len(a); value=F(1)
    for k in range(n):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None: return F(0)
        if pivot!=k: a[k],a[pivot]=a[pivot],a[k]; value=-value
        d=a[k][k]; value*=d
        for i in range(k+1,n):
            ratio=a[i][k]/d
            for j in range(k+1,n): a[i][j]-=ratio*a[k][j]
    return value

def run():
    for g in (F(1,2),F(1),F(3,2)):
        for c0 in (F(101,100),F(3,2),F(2)):
            for c1 in (F(101,100),F(4,3),F(2)):
                z=c0*c1-1
                for degree in range(3,19):
                    direct=direct_block(g,c0,c1,degree)
                    predicted=formula_block(g,c0,c1,degree)
                    for b in (0,1):
                        for j in (0,1):
                            require(direct[b][j]==predicted[b][j],
                                    'polynomial_moment_entries',str((g,c0,c1,degree,b,j)))
                    require(determinant(direct)>0,'block_determinants',str(degree))
                    m=degree//2
                    if degree%2:
                        require((1+z)*(1+2*z)**(2*m)-(1+2*m*z)**2
                                >=z*(1+2*m*z)**2>0,'odd_separation',str(m))
                    else:
                        require((1+2*z)**m-(1+2*m*z)
                                ==sum(F(comb(m,r))*(2*z)**r for r in range(2,m+1))>0,
                                'even_separation',str(m))
    require(direct_block(F(1),F(2),F(2),3)==
            [[-F(7,54),-F(7,108)],[-F(7,108),-F(7,54)]],
            'reference_blocks','cubic')
    require(direct_block(F(1),F(2),F(2),4)==
            [[-F(49,1728),-F(13,1728)],[-F(13,1728),-F(49,1728)]],
            'reference_blocks','quartic')
    for K in range(3,17):
        ne=K//2-1; no=(K-1)//2
        require(ne+no==K-2,'window_dimensions',str(K))
        for h in (F(1),F(1,3),F(1,17)):
            count=[]
            for b,n in ((0,ne+1),(1,ne)):
                for i in range(1,n+1):
                    count.append([F(1)]+[(i*h)**k if b==j else F(0)
                                          for j in (0,1) for k in range(1,ne+1)])
            require(determinant(count)!=0,'shared_intercept_windows',str((K,h)))
            # Repeated nodes are genuinely singular whenever a block has two rows.
            if len(count)>1:
                bad=[r[:] for r in count]; bad[1]=bad[0][:]
                require(determinant(bad)==0,'singular_window_controls',str(K))
            moment=[[(i*h)**k for k in range(1,no+1)] for i in range(1,no+1)]
            require(determinant(moment)!=0,'moment_windows',str((K,h)))
    require(ellipse_integral({(3,0):F(1)},(F(2),F(1),F(3)),False)==0,
            'reflection','odd action count')
    require(ellipse_integral({(3,0):F(1)},(F(2),F(1),F(3)),True)==0,
            'reflection','odd density count')
    for K in range(3,17):
        # Integral of sin^(2K+2) divided by 2pi; area derivative is negative at disk.
        normalized=F(comb(2*K+2,K+1),4**(K+1))
        require(normalized>0,'area_direction',str(K))
    return {'schema':'a2-v15-exact-diagnostics-1','arithmetic':'fractions.Fraction',
            'checks':checks,'total_checks':sum(checks.values()),'status':'passed',
            'proof_certificate':False,
            'scope':'Finite leading homogeneous action/twist moments, determinants, nodal designs and controls; not a full proof or physical simulation.'}
if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
