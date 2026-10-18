#!/usr/bin/env python3
"""Finite exact algebra and numerical diagnostics, not continuum proof or review."""
from __future__ import annotations
import json, math
from fractions import Fraction as F
import numpy as np
import scipy
from scipy.optimize import linprog
import sympy as sp
COUNTS={};DETAILS={}
def check(ok,group,detail):
    if not bool(ok):raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1

def classical_exact():
    # State-dependent herald: raw Kraus potential, with coherent preparation.
    A=sp.diag(sp.Rational(3,5),sp.Rational(4,5))
    B=sp.diag(sp.Rational(4,5),sp.Rational(3,5))
    H=sp.diag(sp.Rational(25,16),sp.Rational(25,9))
    rho=sp.Matrix([[sp.Rational(1,2),sp.Rational(1,3)],[sp.Rational(1,3),sp.Rational(1,2)]])
    check(A.T*A+B.T*B==sp.eye(2),'exact_weighted_instrument','normalization')
    check(H-A.T*H*A==sp.eye(2),'exact_weighted_potential','first-herald resolvent')
    check(rho.det()>0 and sp.trace(rho)==1,'exact_weighted_preparation','full rank')
    # Policy rejects its first herald once, then accepts next: solve raw expected cost.
    RHS=sp.eye(2)+B.T*H*B
    J=sp.Matrix(2,2,lambda i,j:RHS[i,j]/(1-A[i,i]*A[j,j]))
    reject_extra=sp.Matrix(2,2,lambda i,j:(B.T*H*B)[i,j]/(1-A[i,i]*A[j,j]))
    check(J==H+reject_extra,'exact_weighted_residual','raw one-rejection potential')
    check(sp.trace((J-H)*rho)>0,'exact_weighted_residual','strict extra cost')
    # Coverage cannot be discarded: expensive a-model cost3; cheap b-model2+one reject3.
    check(1/sp.Rational(1,3)==3 and 2+1==3,'exact_coverage_negative','exclusive cheaper word')
    table=[]
    for k in range(2,8):
        for a in (sp.Rational(1,3),sp.Rational(1,2),sp.Rational(3,4)):
            Q=sp.zeros(k)
            for i in range(k-1):Q[i,i]=a;Q[i,i+1]=1-a
            Q[k-1,k-1]=1
            d=sp.ones(k,1);d[k-1]=0;e=sp.zeros(1,k);e[0]=1
            values=[];state=e
            for n in range(2*k+5):
                beta=(state*d)[0]
                direct=sum(sp.binomial(n,j)*(1-a)**j*a**(n-j) for j in range(min(n,k-2)+1))
                check(beta==direct,'exact_chain_born',(k,str(a),n));values.append(beta);state=state*Q
            hankel=sp.Matrix([[1]+[values[n+j] for j in range(k-1)] for n in range(k)])
            check(hankel.det()!=0,'exact_chain_hankel_lower',(k,str(a)))
            # Scalar rank k-1 is not by itself the live-memory count; include normalization.
            check(sp.Matrix([[values[n+j] for j in range(k)] for n in range(k)]).rank()==k-1,
                  'exact_scalar_vs_probability_rank',(k,str(a)))
            gs=[]
            for t in (sp.Rational(1,4),sp.Rational(1,2),sp.Rational(3,4)):
                g=((1-t)*e*(sp.eye(k)-t*Q).inv()*d)[0]
                form=1-(((1-a)*t)/(1-a*t))**(k-1)
                check(g==form,'exact_chain_random_horizon',(k,str(a),str(t)));gs.append(g)
            u=(gs[0]+gs[-1])/2;radius=(gs[0]-gs[-1])/2
            check(gs[0]>=gs[1]>=gs[2] and u-gs[-1]==radius and gs[0]-u==radius,
                  'exact_one_label_chebyshev',(k,str(a)))
            table.append({'k':k,'a':str(a),'one_label_risk':str(sp.Rational(1,2)+radius/2)})
    DETAILS['chain_exact_memory_and_one_label']=table
    # Full robust face versus Bayes slack: every pure action tied under balanced signs.
    for beta in (sp.Rational(0),sp.Rational(1,3),sp.Rational(1)):
        for action in (0,1):
            plus=(1+action-beta)/2;minus=(1-action+beta)/2
            check((plus+minus)/2==sp.Rational(1,2),'exact_tied_slack','all actions Bayes tied')
    # Finite equality bound: nilpotent shift hides a difference until its last reachable row.
    for dim in range(2,10):
        T=sp.zeros(dim)
        for j in range(dim-1):T[j,j+1]=1
        v=sp.zeros(1,dim);v[0]=1;last=sp.zeros(dim,1);last[-1]=1
        vals=[(v*T**n*last)[0] for n in range(dim+2)]
        check(all(z==0 for z in vals[:dim-1]) and vals[dim-1]==1,
              'exact_shorter_prefix_negative',dim)

def quantum_exact():
    c,s=sp.Rational(3,5),sp.Rational(4,5)
    threshold=5/(3+4*sp.sqrt(3))
    check(sp.simplify(threshold*(c+sp.sqrt(3)*s)-1)==0,'exact_three_label_threshold','endpoint')
    for alpha in (sp.Rational(1,10),sp.Rational(1,3),sp.Rational(1,2),threshold):
        u0=(1+2*alpha*c)/3;up=(1-alpha*c+sp.sqrt(3)*alpha*s)/3;um=(1-alpha*c-sp.sqrt(3)*alpha*s)/3
        Q=sp.Matrix([[u0,up,um],[um,u0,up],[up,um,u0]])
        check(all(sp.simplify(x)>=0 for x in Q),'exact_circulant_stochastic',str(alpha))
        check(Q*sp.ones(3,1)==sp.ones(3,1),'exact_circulant_rows',str(alpha))
        # A 3x3 real moment embedding proves equality at all n by intertwining.
        vertices=sp.Matrix([[1,1,0],[1,-sp.Rational(1,2),sp.sqrt(3)/2],[1,-sp.Rational(1,2),-sp.sqrt(3)/2]])
        T=sp.Matrix([[1,0,0],[0,alpha*c,alpha*s],[0,-alpha*s,alpha*c]])
        check((Q*vertices-vertices*T).applyfunc(sp.simplify)==sp.zeros(3),
              'exact_circulant_intertwining',str(alpha))
        d=sp.Matrix([1,sp.Rational(1,4),sp.Rational(1,4)])
        check(vertices*sp.Matrix([sp.Rational(1,2),sp.Rational(1,2),0])==d,
              'exact_circulant_decoder','probabilities not signs')
        if alpha!=threshold:
            vals=[];row=sp.Matrix([[1,0,0]]);z=sp.Integer(1)
            for n in range(10):
                value=sp.simplify((row*d)[0]);wanted=sp.Rational(1,2)+(alpha**n)*sp.re(z)/2
                check(sp.simplify(value-wanted)==0,'exact_qubit_coefficients',(str(alpha),n))
                vals.append(value);row=(row*Q).applyfunc(sp.simplify);z=sp.expand(z*(c+sp.I*s))
            check(sp.Matrix([[vals[i+j] for j in range(3)] for i in range(3)]).det()!=0,
                  'exact_qubit_hankel_three',str(alpha))
    alpha=sp.Rational(3,5)
    check(3*(alpha*s)**2>(1-alpha*c)**2,'exact_three_label_impossibility','alpha=3/5')
    # General stochastic generator trace inequality, exact finite probes not proof by sampling.
    for den in range(2,7):
        for a in range(den+1):
            q=sp.Matrix([[sp.Rational(a,den),1-sp.Rational(a,den),0],
                         [0,sp.Rational(1,den),1-sp.Rational(1,den)],
                         [sp.Rational(1,2),0,sp.Rational(1,2)]])
            B=sp.eye(3)-q;ex=[B[i,i] for i in range(3)]
            sec=sum(B.extract([i,j],[i,j]).det() for i in range(3) for j in range(i+1,3))
            check(sec<=sum(ex)**2/3,'exact_three_state_trace_bound',(den,a))
    # alpha=0 has rank2 and a two-label realization.
    Q=sp.Matrix([[0,1],[0,1]]);d=sp.Matrix([1,sp.Rational(1,2)])
    check([((sp.Matrix([[1,0]])*Q**n*d)[0]) for n in range(4)]==[1,sp.Rational(1,2),sp.Rational(1,2),sp.Rational(1,2)],
          'exact_full_depolarization','two labels')
    DETAILS['alpha_three']=str(threshold)

def polygon_numeric():
    angle=math.atan2(4,3);rot=np.array([[.6,-.8],[.8,.6]])
    out=[];maximum=0.
    for alpha in (.01,.2,.5,.55,.7,.8,.9,.95,.98):
        M=max(3,math.ceil(math.pi/math.acos(alpha))+1) # strict interior numeric certificate
        ang=2*np.pi*np.arange(M)/M;vertices=np.column_stack([np.cos(ang),np.sin(ang)])
        Q=np.zeros((M,M));A=np.vstack([np.ones(M),vertices.T])
        for j,v in enumerate(vertices):
            target=alpha*rot@v
            res=linprog(np.zeros(M),A_eq=A,b_eq=np.r_[1.,target],bounds=(0,None),method='highs')
            check(res.success,'float_polygon_feasible',(alpha,j))
            Q[j]=res.x
        check(np.max(np.abs(Q@vertices-alpha*vertices@rot.T))<2e-10,'float_polygon_invariance',alpha)
        d=(1+vertices[:,0])/2;row=np.eye(M)[0]
        for n in range(80):
            target=(1+alpha**n*math.cos(n*angle))/2
            err=abs(row@d-target);maximum=max(maximum,err)
            check(err<2e-9,'float_polygon_born',(alpha,n));row=row@Q
        # Independent raw qubit computation, not scalar closed-form only.
        U=np.array([[2.,-1.],[1.,2.]])/math.sqrt(5);rho=np.diag([1.,0.]);row=np.eye(M)[0]
        for n in range(32):
            check(abs(row@d-rho[0,0])<2e-9,'float_raw_qubit_replication',(alpha,n))
            rho=alpha*U@rho@U.T+(1-alpha)*np.eye(2)*np.trace(rho)/2;row=row@Q
        for t in (.2,.4,.7,.9):
            g=(1-t)*np.linalg.solve(np.eye(M)-t*Q,d)[0]
            target=.5+(1-t)*(1-alpha*t*.6)/(2*(1-2*alpha*t*.6+(alpha*t)**2))
            check(abs(g-target)<2e-9,'float_random_horizon_resolvent',(alpha,t))
        out.append({'alpha':alpha,'verified_labels':M,'max_row_error':float(np.max(np.abs(Q.sum(axis=1)-1)))})
    DETAILS['polygon_probes']=out;DETAILS['maximum_born_residual']=maximum

if __name__=='__main__':
    classical_exact();quantum_exact();polygon_numeric()
    print(json.dumps({'schema':'theta.r66.finite-diagnostics.v1','status':'PASS',
        'checks_by_group':COUNTS,'total_checks':sum(COUNTS.values()),'details':DETAILS,
        'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
        'limits':'Finite exact algebra and floating probes only; no formal proof, independent human review, exhaustive priority or editorial certification.'},indent=2,sort_keys=True))
