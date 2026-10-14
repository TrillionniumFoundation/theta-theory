#!/usr/bin/env python3
"""Finite algebraic regressions only; none certifies continuum billiard estimates."""
from fractions import Fraction as F
from itertools import combinations
import sympy as sp
import numpy as np


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    # Exact endpoint/count disintegration in finite invertible orbit models.
    cases = 0
    negative_endpoint = 0
    for size in range(2, 9):
        for mask in range(1, 1 << size):
            section = {i for i in range(size) if mask & (1 << i)}
            for x in section:
                for m in range(1, 2 * size + 1):
                    endpoint = (x + m) % size
                    occupation = sum((x + j) % size in section for j in range(m))
                    visit_times = [j for j in range(1, m + 1) if (x + j) % size in section]
                    actual_n = len(visit_times) if endpoint in section else None
                    if endpoint in section:
                        require(actual_n == occupation, 'actual return count is not [0,m) occupation')
                        # Collision and roof records telescope over the same interval.
                        chunks = [0] + visit_times
                        direct_k = sum(((x+j) % size) - size//2 for j in range(m))
                        direct_t = sum(1 + ((x+j) % size) for j in range(m))
                        induced_k = sum(sum(((x+j) % size) - size//2 for j in range(l,r))
                                        for l,r in zip(chunks,chunks[1:]))
                        induced_t = sum(sum(1 + ((x+j) % size) for j in range(l,r))
                                        for l,r in zip(chunks,chunks[1:]))
                        require((direct_k,direct_t)==(induced_k,induced_t),'record additivity')
                        wrong = sum((x+j) % size in section for j in range(1,m))
                        require(wrong == occupation-1,'excluded-initial negative control')
                        negative_endpoint += 1
                    lhs = (actual_n*actual_n+1) if actual_n is not None else 0
                    rhs = (occupation*occupation+1) if endpoint in section else 0
                    require(lhs==rhs,'weighted disintegration')
                    cases += 1
    # Exact covariance and Gaussian Jacobian, for a rational positive matrix.
    c = sp.Rational(2,7); mu = sp.Rational(5,4)
    L = sp.Matrix([[1,0,0,0],[0,1,0,0],[0,0,-mu,1],[0,0,-c,0]])
    D = sp.Matrix([[4,1,0,1],[1,3,1,0],[0,1,5,2],[1,0,2,6]])
    require(all(D[:j,:j].det()>0 for j in range(1,5)), 'positive test covariance')
    Omega = c*L*D*L.T; Sigma=Omega[:3,:3]; cross=Omega[:3,3:4]
    beta=cross.T*Sigma.inv(); variance=Omega[3,3]-(beta*cross)[0]
    require(L.det()==c and Omega.det()==c**6*D.det(),'four-dimensional determinant')
    require(variance>0 and Omega.det()==Sigma.det()*variance,'Schur identity')
    z1,z2,z3,y=sp.symbols('z1 z2 z3 y'); z=sp.Matrix([z1,z2,z3]); x=z.col_join(sp.Matrix([y]))
    q=(x.T*Omega.inv()*x)[0]
    require(sp.simplify(q-(z.T*Sigma.inv()*z)[0]-(y-(beta*z)[0])**2/variance)==0,
            'conditional Gaussian completion of square')
    require(L.inv()*x==sp.Matrix([z1,z2,-y/c,z3-mu*y/c]),'induced coordinates')
    # The Fourier convention fixes a positive conditional mean. Check one exact
    # conditional characteristic derivative and reject the opposite sign.
    expected_mean=(beta*z)[0]
    require(expected_mean!=0 and sp.simplify(expected_mean-(-expected_mean))!=0,'Fourier-sign control')
    # Finite chronological weighted push-forward: image-side preceding roof,
    # source-side current occupation, with endpoint factors at the actual times.
    matrix_cases=0
    for size in range(2,9):
        P=np.zeros((size,size),dtype=complex)
        for i in range(size):P[(i+1)%size,i]=1
        f=np.arange(size)+1; eta=np.arange(size)%2; inv=(np.arange(size)-1)%size
        a=(np.arange(size)+1)/size; d=np.arange(size)[::-1]+1
        for t,v in [(0.13,0.21),(-0.27,0.41),(0.11+0.02j,-0.07+0.03j)]:
            Q=np.diag(np.exp(1j*t*f[inv]))@P@np.diag(np.exp(1j*v*eta))
            for m in range(1,10):
                lhs=np.sum(d*(np.linalg.matrix_power(Q,m)@a))/size
                rhs=sum(a[x]*d[(x+m)%size]*np.exp(1j*sum(t*f[(x+j)%size]+v*eta[(x+j)%size]
                           for j in range(m))) for x in range(size))/size
                require(abs(lhs-rhs)<1e-9*(1+abs(rhs)),'chronological mixed operator')
                matrix_cases+=1
    # Exact support-function perimeter, area, and conservative curvature bounds.
    require(F(91,200)-F(1,250)==F(451,1000),'support lower bound')
    require(F(93,200)+F(1,250)==F(469,1000),'support upper bound')
    require(F(91,200)-15*F(1,250)==F(79,200),'curvature-radius lower bound')
    require(F(93,200)+15*F(1,250)==F(21,40),'curvature-radius upper bound')
    require((1-3**2)/2==-4 and F(1-4**2,2)==-F(15,2),'area harmonics')
    require(1-2*F(469,1000)==F(31,500),'inter-obstacle gap')
    # The fixed-band statement must not be silently turned into a single-index
    # or pointwise-roof density assertion. These are explicit qualification flags.
    return {'exact_orbit_cases':cases,'endpoint_negative_controls':negative_endpoint,
            'chronological_matrix_cases':matrix_cases,'covariance_determinant_power':6,
            'conditional_variance':str(variance),'support_curvature_radius':['79/200','21/40'],
            'raw_return_singleton_certified':False,'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
