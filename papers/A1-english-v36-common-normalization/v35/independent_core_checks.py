#!/usr/bin/env python3
"""Independent exact diagnostics of A1 v34's collision spine.

No continuum quantization, global controller optimization, or general proof
verification is claimed. The pairing tests use the uniform prior on [0,1].
The Hermite basis spans the same complete flag as the selected Newton tests;
we test its rank, not a floating-point approximation to divided differences.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import factorial, prod, comb
from pathlib import Path
import hashlib
import json

CHECKS = 0

def require(ok, msg):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ArithmeticError(msg)


def rank(a):
    a = [list(row) for row in a]
    r = 0
    for col in range(len(a[0])):
        piv = next((i for i in range(r, len(a)) if a[i][col]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        v = a[r][col]
        a[r] = [x/v for x in a[r]]
        for i in range(r+1, len(a)):
            if a[i][col]:
                z = a[i][col]
                a[i] = [x-z*y for x,y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def det(a):
    a = [list(row) for row in a]
    result = F(1)
    for col in range(len(a)):
        piv = next((i for i in range(col, len(a)) if a[i][col]), None)
        if piv is None:
            return F(0)
        if piv != col:
            a[col], a[piv] = a[piv], a[col]
            result = -result
        v = a[col][col]
        result *= v
        for i in range(col+1, len(a)):
            z = a[i][col]/v
            for j in range(col+1, len(a)):
                a[i][j] -= z*a[col][j]
    return result


def formal_nodes(A, m):
    return [sum((A[i] for i in word), F(0))
            for word in combinations_with_replacement(range(len(A)), m)
            if any(i != 0 for i in word)]


def leja_order(nodes):
    remaining = set(range(len(nodes)))
    first = min(remaining, key=lambda j:(nodes[j], j))
    order = [first]
    remaining.remove(first)
    scales = [F(1)]
    while remaining:
        def pivot(j):
            return prod((abs(nodes[j]-nodes[i]) for i in order), start=F(1))
        j = max(remaining, key=lambda i:(pivot(i), -i))
        scales.append(pivot(j)); order.append(j); remaining.remove(j)
    return order, scales


def configurations():
    t = F(1,64)
    return [('intersection',F(0),F(0)), ('line_u_zero',F(0),F(1,32)),
            ('line_v_u',F(1,32),F(1,32)), ('line_v_2u',F(1,32),F(1,16)),
            ('generic_v_zero',F(1,32),F(0)), ('generic_signed',-F(1,32),F(1,32)),
            ('tangent_order_2',t,t+t*t), ('tangent_order_4',t,t+t**4)]


def volume_checks():
    rows = []
    for name,u,v in configurations():
        A = [F(0), F(1), F(2)+u, F(3)+v]
        nodes = [x/16 for x in formal_nodes(A,2)]
        order, scales = leja_order(nodes)
        V = []
        for ell in range(1,len(nodes)+1):
            best = max(prod((abs(nodes[i]-nodes[j]) for i,j in combinations(S,2)),start=F(1))
                       for S in combinations(range(len(nodes)),ell))
            left = prod(scales[:ell],start=F(1))
            require(left <= best <= factorial(ell)*left, 'Leja-volume comparison '+name)
            V.append(best)
        require(all(a>=b for a,b in zip(scales,scales[1:])), 'monotone scales '+name)
        expected = 6 if u==v==0 else 8 if u==0 or v==u or v==2*u else 9
        require(len(set(nodes))==expected, 'distinct positive exponents '+name)
        require(sum(x>0 for x in V)==expected, 'zero-volume convention '+name)
        s = expected
        L = [[prod((nodes[order[i]]-nodes[order[k]] for k in range(j)),start=F(1))/scales[j]
              for j in range(s)] for i in range(s)]
        require(all(abs(x)<=1 for row in L for x in row),'bounded Newton matrix '+name)
        require(all(abs(L[i][i])==1 for i in range(s)), 'unit diagonal '+name)
        rows.append({'configuration':name,'u':str(u),'v':str(v),
                     'distinct_positive_exponents':s,'all_nine_volume_comparisons_passed':True})
    return rows


def pairing_checks():
    rows=[]
    for name,u,v in configurations():
        A=[F(0),F(1),F(2)+u,F(3)+v]; D=A[-1]
        for n in range(1,5):
            m=5-n
            B=sorted({j*D for j in range(n+1)} |
                     {a+j*D for a in A[1:-1] for j in range(n)})
            require(len(B)==n*3+1, 'binomial tangent dimension')
            nodes=formal_nodes(A,m); p=min(3*n,len(nodes))
            leja,_=leja_order(nodes)
            for ordername,order in [('leja',leja),('reverse_formal',list(reversed(range(len(nodes)))) )]:
                counts=Counter(nodes[j] for j in order[:p])
                tests=[(F(0),0)]+[(lam,k) for lam,count in sorted(counts.items()) for k in range(count)]
                # Exact integral of t^(b+lambda) log(t)^k / k!, uniform prior.
                L=[[F((-1)**k)/(b+lam+1)**(k+1) for b in B] for lam,k in tests]
                minor=det([[L[j][i] for j in range(p+1)] for i in range(p+1)])
                require(minor>0,'strict complete confluent mixed minor')
                coeff={F(0):F(1)}
                for i in range(n):
                    nxt={}; c=F(1,16+i)
                    for b,x in coeff.items():
                        nxt[b]=nxt.get(b,F(0))+x/2
                        nxt[b+D]=nxt.get(b+D,F(0))+x*c/2
                    coeff=nxt
                LP=[sum((x*row[B.index(b)] for b,x in coeff.items()),F(0)) for row in L]
                Z=LP[0]
                differential=[[(L[j][i]*Z-LP[j]*L[0][i])/Z**2 for i in range(len(B))]
                              for j in range(1,p+1)]
                actual=rank(differential)
                require(actual==p,'normalization loses exactly one rank')
                rows.append({'configuration':name,'n':n,'m':m,'ordering':ordername,
                             'flag_dimension':p,'normalized_rank':actual,
                             'positive_mixed_minor':True})
    return rows


def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0:
        p.pop()
    return tuple(p)


def polyadd(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b)))])


def order_difference(a,b):
    return next(i for i in range(max(len(a),len(b)))
                if (a[i] if i<len(a) else 0)!=(b[i] if i<len(b) else 0))


def tree_table(nodes):
    size=len(nodes)
    w=[[0 if i==j else order_difference(nodes[i],nodes[j]) for j in range(size)] for i in range(size)]
    infinity=10**9
    def visit(indices,parent_height=0,is_root=False):
        if len(indices)==1:
            return [0,0]
        h=0 if is_root else min(w[i][j] for i,j in combinations(indices,2))
        groups=[]; unused=set(indices)
        while unused:
            i=min(unused)
            group={j for j in unused if j==i or w[i][j]>h}
            groups.append(sorted(group));unused-=group
        tab=[0]
        for group in groups:
            sub=visit(group,h)
            new=[infinity]*(len(tab)+len(sub)-1)
            for i,a in enumerate(tab):
                for j,b in enumerate(sub):
                    new[i+j]=min(new[i+j],a+b)
            tab=new
        return [value+(h-parent_height)*comb(k,2) for k,value in enumerate(tab)]
    dp=visit(list(range(size)),is_root=True)
    brute=[0]+[min(sum(w[i][j] for i,j in combinations(S,2))
                   for S in combinations(range(size),ell)) for ell in range(1,size+1)]
    require(dp==brute,'collision-tree dynamic program versus all subsets')
    return dp


def phase_checks():
    result=[]
    for k in range(2,7):
        a3=[3,1]+[0]*(k-2)+[1]
        A=[(0,),(1,),(2,1),tuple(a3)]
        nodes=sorted({polyadd(A[i],A[j]) for i,j in combinations_with_replacement(range(4),2) if i or j})
        beta=tree_table(nodes)
        require(beta==[0]*7+[1,2,k+2],'tangent energy profile')
        # On M=theta^-gamma: compare theta powers, not floating-point risks.
        def powers(gamma):
            return [F(gamma,3),F(1,2)+F(gamma,4),F(4+2*k+2*gamma,9)]
        c1=6; c2=8*k-2
        require(powers(c1)[0]==powers(c1)[1]==2,'first crossover and regret')
        require(powers(c2)[1]==powers(c2)[2]==2*k,'second crossover and regret')
        require(c2>c1,'separated three regimes')
        result.append({'contact_order':k,'beta':beta,'crossover_exponents':[c1,c2],
                       'regret_exponents':[2,2*k]})
    nested=[(0,),(0,0,0,1),(0,1,0,0,1),(0,1,0,0,0,-1),
            (1,),(1,0,1),(1,0,1,0,0,0,1)]
    result.append({'nonuniform_nested_cluster_beta':tree_table(nested)})
    return result


def pairing_summary(rows):
    return {'systems_tested':len(rows), 'configurations':len(configurations()),
            'orderings':['leja','reverse_formal'],
            'checkpoints_n_m_flag_dimension':[[1,4,3],[2,3,6],[3,2,9],[4,1,3]],
            'all_expected_normalized_ranks_attained':all(r['normalized_rank']==r['flag_dimension'] for r in rows),
            'all_tested_mixed_minors_positive':all(r['positive_mixed_minor'] for r in rows),
            'at_intersection_n3_m2':{'raw_future_nonconstant_dimension':6,
                                    'auxiliary_confluent_flag_rank':9}}


def main():
    result={'schema':'a1-v34-independent-collision-core-checks-v1',
            'reviewed_commit':'03a4788efb3cf643bc2cd60257c5ed290bb0570d',
            'arithmetic':'Python standard-library Fraction; exact integer collision orders',
            'volumes':volume_checks(),'complete_confluent_pairings':pairing_summary(pairing_checks()),
            'collision_trees_and_phases':phase_checks()}
    result['checks_passed']=CHECKS
    result['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['limits']=['No proof of a continuum entropy bound or uniform chart minorization.',
        'Pairing checks use a uniform latent prior, not a singular full-support prior.',
        'No global finite-memory optimization or proof-assistant verification.',
        'Exact rank tests do not certify lower bounds on singular values over a chamber.']
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
