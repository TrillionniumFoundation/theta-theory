#!/usr/bin/env python3
"""Exact finite algebra and separate numerical diagnostics; not a proof certificate."""
from __future__ import annotations
import itertools,json,math
from functools import lru_cache
import numpy as np
import scipy
from scipy.optimize import linprog
import sympy as sp
COUNTS={};DETAILS={};MAXIMUM={}
def check(ok,group,detail):
    if not bool(ok):raise RuntimeError(f'{group}: {detail}')
    COUNTS[group]=COUNTS.get(group,0)+1
def close(actual,expected,group,detail,tol=2e-9):
    gap=float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    MAXIMUM[group]=max(MAXIMUM.get(group,0.),gap)
    check(gap<tol,group,(detail,gap))
def partitions(items):
    if not items:yield ();return
    first,*rest=items
    for p in partitions(rest):
        yield ((first,),)+p
        for j in range(len(p)):yield p[:j]+((first,)+p[j],)+p[j+1:]
def partition_value(orders,blocks):
    return sum(math.lcm(*(orders[j] for j in B)) for B in blocks)+(len(blocks)>1)
def subset_solver(orders):
    r=len(orders);full=(1<<r)-1;lcms=[1]*(1<<r)
    for mask in range(1,1<<r):
        bit=mask&-mask;lcms[mask]=math.lcm(lcms[mask^bit],orders[bit.bit_length()-1])
    @lru_cache(None)
    def additive(mask):
        if not mask:return (0,())
        first=mask&-mask;sub=mask;best=(10**100,())
        while sub:
            if sub&first:
                tail,bs=additive(mask^sub);trial=(lcms[sub]+tail,(sub,)+bs)
                if trial[0]<best[0]:best=trial
            sub=(sub-1)&mask
        return best
    best=(lcms[full],(full,));sub=(full-1)&full
    while sub:
        tail,bs=additive(full^sub);trial=(1+lcms[sub]+tail,(sub,)+bs)
        if trial[0]<best[0]:best=trial
        sub=(sub-1)&full
    return best[0],tuple(tuple(i for i in range(r) if mask>>i&1) for mask in best[1])
def partition_exact():
    cases=list(itertools.combinations_with_replacement(range(3,10),3))
    cases += [(3,),(3,6),(4,6),(3,5,7),(3,5,7,11),(4,6,8,9),(5,5,7,7),(3,4,5,6,7)]
    for orders in cases:
        exhaustive=min(partition_value(orders,p) for p in partitions(list(range(len(orders)))))
        value,blocks=subset_solver(orders)
        check(value==exhaustive,'exact_partition_dp_vs_bell',orders)
        check(partition_value(orders,blocks)==value,'exact_partition_witness',orders)
        check(value<=math.lcm(*orders),'exact_partition_deterministic_upper',orders)
    for orders,wanted in [((3,5,7),16),((4,6),11),((3,6),6),((3,5,7,11),27)]:
        check(subset_solver(orders)[0]==wanted,'exact_named_memory_counts',orders)
    check(4+6<subset_solver((4,6))[0],'exact_negative_uncharged_initialization','a mixed initial distribution is not the prescribed pure start')
    DETAILS['partition_cases']=len(cases)
    DETAILS['period_3_5_7']={'stochastic':16,'deterministic_transitions':105,'leaky':17}
def exact_periodic_machine(orders,weights):
    size,blocks=subset_solver(orders);Gamma=sum(weights)
    lengths=[math.lcm(*(orders[j] for j in B)) for B in blocks]
    extra=int(len(blocks)>1);Q=sp.zeros(size);d=sp.zeros(size,1)
    direct=lambda n:sp.simplify((1+sum(weights[j]*sp.cos(2*sp.pi*n/orders[j]) for j in range(len(orders))))/2)
    if not extra:
        for k in range(size):Q[k,(k+1)%size]=1;d[k]=direct(k)
    else:
        d[0]=direct(0);offset=1
        for B,L in zip(blocks,lengths):
            W=sum(weights[j] for j in B);Q[0,offset+1%L]=W/Gamma
            for k in range(L):
                Q[offset+k,offset+(k+1)%L]=1
                d[offset+k]=sp.simplify((1+Gamma/W*sum(weights[j]*sp.cos(2*sp.pi*k/orders[j]) for j in B))/2)
            offset+=L
    return Q,d,direct,extra,lengths
def periodic_exact():
    for orders in [(3,),(4,),(3,4),(3,6),(4,6),(3,4,6)]:
        weights=[sp.Rational(1,len(orders)+1)]*len(orders)
        Q,d,direct,extra,lengths=exact_periodic_machine(orders,weights);M=Q.rows
        check(Q*sp.ones(M,1)==sp.ones(M,1),'exact_periodic_stochastic',orders)
        check(all(z>=0 for z in Q) and all(0<=z<=1 for z in d),'exact_periodic_probability_bounds',orders)
        row=sp.zeros(1,M);row[0]=1
        for n in range(2*math.lcm(*orders)+3):
            check(sp.simplify((row*d)[0]-direct(n))==0,'exact_periodic_coefficient',(orders,n));row=row*Q
        pi=sp.zeros(1,M);offset=extra
        for k in range(lengths[0]):pi[offset+k]=sp.Rational(1,lengths[0])
        check(pi*Q==pi and (pi*d)[0]==sp.Rational(1,2),'exact_periodic_stationary_decoder',orders)
        for alpha in (sp.Rational(1,3),sp.Rational(3,4)):
            Qa=alpha*Q+(1-alpha)*sp.ones(M,1)*pi;row=sp.zeros(1,M);row[0]=1
            for n in range(7):
                want=sp.Rational(1,2)+alpha**n*(direct(n)-sp.Rational(1,2))
                check(sp.simplify((row*d)[0]-want)==0,'exact_damped_mixture',(orders,str(alpha),n));row=row*Qa
        lam=sp.Rational(2,3);Ql=sp.zeros(M+1);Ql[:M,:M]=lam*Q
        for i in range(M):Ql[i,M]=1-lam
        Ql[M,M]=1;dl=d.col_join(sp.zeros(1,1));row=sp.zeros(1,M+1);row[0]=1
        check(Ql*sp.ones(M+1,1)==sp.ones(M+1,1),'exact_leakage_rows',orders)
        for n in range(10):
            check(sp.simplify((row*dl)[0]-lam**n*direct(n))==0,'exact_leakage_mixture',(orders,n));row=row*Ql
        for t in (sp.Rational(1,5),sp.Rational(1,2)):
            e=sp.zeros(1,M);e[0]=1
            actual=((1-t)*e*(sp.eye(M)-t*Q).inv()*d)[0]
            expected=sp.Rational(1,2)+(1-t)/2*sum(weights[j]*(1-t*sp.cos(2*sp.pi/orders[j]))/(1-2*t*sp.cos(2*sp.pi/orders[j])+t*t) for j in range(len(orders)))
            check(sp.simplify(actual-expected)==0,'exact_mixture_horizon_resolvent',(orders,str(t)))
    S=sp.Matrix([[sp.Rational(1,2),sp.Rational(1,4)],[0,sp.Rational(1,2)]]);A=2*S
    for n in range(1,20):
        check(A**n==sp.Matrix([[1,sp.Rational(n,2)],[0,1]]),'exact_critical_chain_negative',n)
    check(all(z<=1 for z in S*sp.ones(2,1)),'exact_critical_chain_negative','substochastic but rescaled powers unbounded')
def reversible_exact():
    c,s=sp.Rational(3,5),sp.Rational(4,5)
    U0=sp.diag(1,-1);U1=sp.Matrix([[2,1],[1,-2]])/sp.sqrt(5)
    check(U0*U0==sp.eye(2) and U1*U1==sp.eye(2),'exact_involutions','both reversible')
    check(U0*U1!=U1*U0,'exact_involutions','noncommuting')
    V=sp.Matrix([[1,1,0],[1,-sp.Rational(1,2),sp.sqrt(3)/2],[1,-sp.Rational(1,2),-sp.sqrt(3)/2]])
    alpha=sp.Rational(1,3);T0=sp.diag(1,alpha,-alpha)
    T1=sp.Matrix([[1,0,0],[0,alpha*c,alpha*s],[0,alpha*s,-alpha*c]])
    rows=[(V*T*V.inv()).applyfunc(sp.simplify) for T in (T0,T1)]
    for a,Q in enumerate(rows):
        check(Q*sp.ones(3,1)==sp.ones(3,1) and all(x>=0 for x in Q),'exact_common_command_rows',a)
        check((Q*V-V*(T0,T1)[a]).applyfunc(sp.simplify)==sp.zeros(3),'exact_common_intertwining',a)
    d=V*sp.Matrix([sp.Rational(1,2),sp.Rational(1,2),0])
    for n in range(6):
        for word in itertools.product((0,1),repeat=n):
            row=sp.Matrix([[1,0,0]]);rho=sp.diag(1,0)
            for a in word:
                row=(row*rows[a]).applyfunc(sp.simplify)
                U=(U0,U1)[a];rho=(alpha*U*rho*U.T+(1-alpha)*sp.eye(2)*sp.trace(rho)/2).applyfunc(sp.simplify)
            check(sp.simplify((row*d)[0]-rho[0,0])==0,'exact_mixed_word_raw_qubit',word)
    R=sp.Matrix([[c,-s],[s,c]])
    check((T1*T0)[1:,1:]==alpha**2*R,'exact_product_restriction','orientation convention')
    check(2*c==sp.Rational(6,5) and (2*c).q!=1,'exact_non_root_certificate','rational noninteger algebraic-integer obstruction')
    for U in (U0,U1,U1*U0):
        rho=U*sp.diag(1,0)*U.T
        check(sp.trace(sp.eye(2)*rho/2)==sp.Rational(1,2),'exact_observable_quotient','constant effect')
def numeric_periodic():
    examples=[((3,5,7),(.2,.3,.1),(.3,-.5,.7)),((4,6),(.3,.4),(.2,-.7)),((3,6),(.3,.5),(.4,.2)),((5,8,9),(.1,.2,.3),(.1,.2,.3))]
    records=[]
    for orders,weights,phases in examples:
        M,blocks=subset_solver(orders);Gamma=sum(weights);Q=np.zeros((M,M));d=np.zeros(M)
        direct=lambda n:.5*(1+sum(w*math.cos(2*math.pi*n/q+ph) for q,w,ph in zip(orders,weights,phases)))
        offset=int(len(blocks)>1)
        if not offset:
            for k in range(M):Q[k,(k+1)%M]=1;d[k]=direct(k)
        else:
            d[0]=direct(0)
            for B in blocks:
                L=math.lcm(*(orders[j] for j in B));W=sum(weights[j] for j in B)
                Q[0,offset+1%L]=W/Gamma
                for k in range(L):
                    Q[offset+k,offset+(k+1)%L]=1
                    d[offset+k]=.5*(1+Gamma/W*sum(weights[j]*math.cos(2*math.pi*k/orders[j]+phases[j]) for j in B))
                offset+=L
        check(d.min()>-1e-13 and d.max()<1+1e-13,'float_phase_decoder_bounds',orders)
        close(Q.sum(axis=1),np.ones(M),'float_mixture_row_sum',orders)
        row=np.eye(M)[0]
        for n in range(250):close(row@d,direct(n),'float_phased_mixture_coefficients',(orders,n));row=row@Q
        records.append({'orders':orders,'minimal_labels':M,'deterministic_period':math.lcm(*orders)})
    DETAILS['phased_mixture_examples']=records
def numeric_controls():
    c,s=.6,.8;S0=np.diag([1.,-1.]);S1=np.array([[c,s],[s,-c]])
    U0=np.diag([1.,-1.]);U1=np.array([[2.,1.],[1.,-2.]])/math.sqrt(5);records=[]
    for alpha in (.1,.4,.7,.9,.97):
        M=max(3,math.ceil(math.pi/math.acos(alpha))+1)
        angles=2*np.pi*np.arange(M)/M;V=np.column_stack([np.cos(angles),np.sin(angles)])
        A=np.vstack([np.ones(M),V.T]);matrices=[]
        for a,S in enumerate((S0,S1)):
            Q=np.zeros((M,M))
            for i,v in enumerate(V):
                result=linprog(np.zeros(M),A_eq=A,b_eq=np.r_[1.,alpha*S@v],bounds=(0,None),method='highs')
                check(result.success,'float_shared_polygon_feasibility',(alpha,a,i));Q[i]=result.x
            close(Q@V,alpha*V@S.T,'float_shared_intertwining',(alpha,a));matrices.append(Q)
        d=(1+V[:,0])/2
        for n in range(8):
            for word in itertools.product((0,1),repeat=n):
                row=np.eye(M)[0];rho=np.diag([1.,0.]);bloch=np.array([1.,0.])
                for a in word:
                    row=row@matrices[a];U=(U0,U1)[a]
                    rho=alpha*U@rho@U.T+(1-alpha)*np.eye(2)*np.trace(rho)/2
                    bloch=alpha*(S0,S1)[a]@bloch
                close(row@d,rho[0,0],'float_mixed_commands_raw_qubit',(alpha,word))
                close(row@V,bloch,'float_mixed_commands_bloch',(alpha,word))
        pair=matrices[0]@matrices[1];row=np.eye(M)[0]
        for n in range(40):
            close(row@d,(1+alpha**(2*n)*math.cos(n*math.atan2(s,c)))/2,'float_product_unary_restriction',(alpha,n));row=row@pair
        records.append({'alpha':alpha,'verified_common_labels':M,'all_binary_words_through':7})
    DETAILS['noncommuting_common_machines']=records
if __name__=='__main__':
    partition_exact();periodic_exact();reversible_exact();numeric_periodic();numeric_controls()
    print(json.dumps({'schema':'theta.r72.finite-diagnostics.v1','status':'PASS','checks_by_group':COUNTS,'total_checks':sum(COUNTS.values()),
      'details':DETAILS,'maximum_numeric_residuals':MAXIMUM,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,
      'limits':'Exact finite examples and floating probes; not proof by sampling, independent human review, exhaustive priority or editorial certification.'},indent=2,sort_keys=True))
