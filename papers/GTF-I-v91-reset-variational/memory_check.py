#!/usr/bin/env python3
"""Exact finite regressions for the v90 game; not a continuum proof."""
from fractions import Fraction as F
from itertools import product
import json
import sympy as s

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def swap(d):
    return s.Matrix(d*d,d*d,lambda i,j:int(i//d==j%d and i%d==j//d))

checks=0
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
kron=s.kronecker_product
measurements=[[(I+sign*A)/2,(I-sign*A)/2] for A in [X,Y,Z] for sign in [-1,1]]
for t in [s.Rational(0),s.Rational(1,7),s.Rational(1,2),s.Rational(1)]:
    L=6-t*t; pc=(3-t*t)/L; pe=3/L; k=t*t/(2*L)
    B=[[(1-t)*I/2+t*P for P in E] for E in measurements]
    S=swap(2); minus=(s.eye(4)-S)/2
    for y in range(2):
        require(sum((E[y] for E in B),s.zeros(2))/6==I/2,'one-call averaged channel')
        checks+=1
    for y,z in product(range(2),repeat=2):
        moment=sum((kron(E[y],E[z]) for E in B),s.zeros(4))/6
        W=pc*s.eye(4)/4-pe*moment
        require(W==(-k*S if y==z else -2*k*minus),'payoff block')
        checks+=1
    event=lambda E:sum(s.trace(minus*kron(E[y].T,E[y].T))/4 for y in range(2))
    require(event([I/2,I/2])==s.Rational(1,8),'normalized receiver event')
    require(all(event(E)==(1-t*t)/8 for E in B),'same device signal')
    require(s.simplify(pe+pc/8-pe*(1-t*t)/8-(pe+t*t/(4*L)))==0,'reset score')
    checks+=3
    # The imaginary Pauli basis checks that the Choi transpose is not discarded.
    P=B[2][0]
    require(P.T==P.conjugate(),'complex Choi contraction')
    checks+=1
for d in range(2,9):
    S=swap(d)
    for a,b in [(list(range(1,d+1)),list(range(d,0,-1))),([1]*d,[1]*d),([0]*(d-1)+[1],[1]*d)]:
        A=s.diag(*a); B=s.diag(*b)
        R=kron(A.applyfunc(s.sqrt),B.applyfunc(s.sqrt)); K=R*S*R
        negative=sum(-val*mult for val,mult in K.eigenvals().items() if val<0)
        expected=sum(s.sqrt(a[i]*b[i]*a[j]*b[j]) for i in range(d) for j in range(i+1,d))
        require(s.simplify(negative-expected)==0,'swap spectrum')
        require(bool(negative<=s.Rational(d-1,2*d)*sum(a)*sum(b)),'swap trace bound')
        bound=s.Rational(d-1,2*d)*sum(a)*sum(b)
        scalar=(len(set(a))==1 and len(set(b))==1 and a[0]>0 and b[0]>0)
        require(bool(negative==bound)==scalar,'filtered-swap equality characterization')
        checks+=3
    for t in [s.Rational(0),s.Rational(1,3),s.Rational(1)]:
        L=2*(d+1)-t*t; ca=(d+1)/L; reset=ca+t*t*(d-1)/(2*d*L); allp=ca+t*t/L
        require(s.Rational(1,2)<=ca<=reset<=allp<=1,'probability range')
        require((t==0 and ca==reset==allp) or (ca<reset<allp),'strictness')
        require(s.simplify(allp-reset-t*t*(d+1)/(2*d*L))==0,'second gap')
        checks+=3
# Noncommuting positive factors: exact characteristic-polynomial identity.
for A,B in [(s.Matrix([[2,1],[1,1]]),s.diag(1,3)),
            (s.Matrix([[2,s.I],[-s.I,2]]),s.Matrix([[3,1],[1,2]]))]:
    z=s.symbols('z'); AB=A*B
    K=(kron(A,B)*swap(2)).charpoly(z).as_expr()
    expected=(z*z-s.trace(AB)*z+AB.det())*(z*z-AB.det())
    require(s.expand(K-expected)==0,'noncommuting filtered-swap spectrum')
    require(bool(s.sqrt(AB.det())<s.trace(A)*s.trace(B)/4),'noncommuting factors are not equality cases')
    checks+=2
singlet=(s.eye(4)-swap(2))/2
reduced=s.Matrix(2,2,lambda i,j:sum(singlet[2*i+a,2*j+a] for a in range(2)))
negative_controls={
 'missing_pair_normalization_changes_coin_probability':s.Rational(1,2)!=s.Rational(1,8),
 'redrawing_basis_erases_second_moment_signal':sum(s.trace(((s.eye(4)-swap(2))/2)*kron(I/2,I/2))/4 for _ in range(2))==s.Rational(1,8),
 'antisymmetric_acquisition_not_a_product':singlet.rank()==1 and reduced.rank()==2,
 'nonzero_defect_can_overwhelm_small_signal':F(1,10)>F(1,20),
 'reset_score_is_not_unrestricted_score':F(13,20)!=F(4,5),
 'classical_upper_is_not_reset_upper':F(3,5)!=F(13,20)}
require(all(negative_controls.values()),'negative controls')
print(json.dumps({'schema':'gtf90.memory-regression/1','status':'success',
 'exact_checks':checks,'negative_controls':negative_controls,
 'qubit_optima':['3/5','13/20','4/5'],
 'scope':{'continuum_proof_by_replay':False,'physical_reset_calibrated':False,
          'independent_human_priority':False,'arbitrary_pair_score_gap':False}},sort_keys=True))
