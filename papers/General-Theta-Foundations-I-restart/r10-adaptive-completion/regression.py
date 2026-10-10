#!/usr/bin/env python3
"""Exact finite checks for adaptive completion; not proofs of continuum theorems."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json, subprocess, sys

COUNTS=Counter()
def check(ok, group):
    if not ok:
        raise RuntimeError('finite regression failed: '+group)
    COUNTS[group]+=1

def solve(a,b):
    a=[list(row)+[rhs] for row,rhs in zip(a,b)]
    for j in range(len(a)):
        pivot=next(i for i in range(j,len(a)) if a[i][j])
        a[j],a[pivot]=a[pivot],a[j]
        q=a[j][j];a[j]=[x/q for x in a[j]]
        for i in range(len(a)):
            if i!=j:
                q=a[i][j];a[i]=[x-q*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]

R=F(1,100)
Q=((F(1,2),F(1,10)),(F(1,10),F(1,2)))
DIGITS=list(product((0,1),repeat=2))
def prob(i,z):
    return (Q[i][0] if z[0] else 1-Q[i][0])*(Q[i][1] if z[1] else 1-Q[i][1])
def parity(z): return z[0]^z[1]
P=[[sum(prob(i,z) for z in DIGITS if parity(z)==j) for j in range(2)] for i in range(2)]
means=[]
for c in range(2):
    means.append(solve([[F(i==j)-R*P[i][j] for j in range(2)] for i in range(2)],
                       [(1-R)*Q[i][c] for i in range(2)]))
MEAN=[[means[c][i] for c in range(2)] for i in range(2)]
b=[]
for i in range(2):
    b.append(sum(prob(i,z)*((1-R)**2*sum(x*x for x in z)+2*R*(1-R)*sum(z[c]*MEAN[parity(z)][c] for c in range(2))) for z in DIGITS))
SECOND=solve([[F(i==j)-R*R*P[i][j] for j in range(2)] for i in range(2)],b)
VAR=[SECOND[i]-sum(x*x for x in MEAN[i]) for i in range(2)]

def conditional(i,j,value):
    pp=Q[i][j] if value else 1-Q[i][j]
    mu=[F(0),F(0)];ss=F(0)
    for z in DIGITS:
        if z[j]!=value: continue
        weight=prob(i,z)/pp
        cm=[(1-R)*z[c]+R*MEAN[parity(z)][c] for c in range(2)]
        cs=(1-R)**2*sum(x*x for x in z)+2*R*(1-R)*sum(z[c]*MEAN[parity(z)][c] for c in range(2))+R*R*SECOND[parity(z)]
        mu=[x+weight*y for x,y in zip(mu,cm)];ss+=weight*cs
    return mu,ss-sum(x*x for x in mu)
DELTA=[]
for i in range(2):
    row=[]
    for j in range(2):
        m0,_=conditional(i,j,0);m1,_=conditional(i,j,1)
        row.append(Q[i][j]*(1-Q[i][j])*sum((x-y)**2 for x,y in zip(m0,m1)))
    DELTA.append(row)
W=[VAR[i]-max(DELTA[i]) for i in range(2)]

# A node is (word, mass, scalar full-pair scale, Markov state, pending tuple).
def children(node,budget):
    h,mass,scale,i,pending=node
    if pending is None:
        j=i if budget-len(h)==1 else 0
        return [(h+(v,),mass*(Q[i][j] if v else 1-Q[i][j]),scale,i,(j,v)) for v in (0,1)]
    j,v=pending;other=1-j;out=[]
    for w in (0,1):
        z=(v,w) if j==0 else (w,v)
        out.append((h+(w,),mass*(Q[i][other] if w else 1-Q[i][other]),scale*R,parity(z),None))
    return out

def energy(node):
    h,mass,scale,i,pending=node
    return mass*scale*scale*(2 if pending is None else 1+R*R)/4

def variance(node):
    h,mass,scale,i,pending=node
    vv=VAR[i] if pending is None else conditional(i,*pending)[1]
    return scale*scale*vv/4

def greedy(L,budget,limit=None):
    frontier={(): ((),F(1),F(1),0,None)};splits=[]
    while len(frontier)<L:
        eligible=[v for v in frontier.values() if limit is None or len(v[0])<limit]
        if not eligible: break
        node=min(eligible,key=lambda x:(-energy(x),x[0]));del frontier[node[0]];splits.append(node[0])
        for child in children(node,budget): frontier[child[0]]=child
    return frontier,splits

@lru_cache(None)
def full_variance(i,pending,k):
    if not k:
        return VAR[i] if pending is None else conditional(i,*pending)[1]
    if pending is None:
        return min(sum((Q[i][j] if v else 1-Q[i][j])*full_variance(i,(j,v),k-1) for v in (0,1)) for j in (0,1))
    j,v=pending;other=1-j
    return R*R*sum((Q[i][other] if w else 1-Q[i][other])*full_variance(v^w,None,k-1) for w in (0,1))

def main():
    for i,j in product(range(2),repeat=2):
        check(P[i][j]==F(1,2),'actual_markov_transition')
    for i in range(2):
        check(VAR[i]>0 and W[i]>0,'positive_remaining_variance')
        check(DELTA[i][i]>DELTA[i][1-i],'strict_observation_dependent_choice')
        check(DELTA[i][i]>=F(1,4)*(1-2*R)**2,'high_variance_lower')
        check(DELTA[i][1-i]<=F(9,100)*(1+R*R),'low_variance_upper')
        for j in range(2):
            cv=sum((Q[i][j] if v else 1-Q[i][j])*conditional(i,j,v)[1] for v in (0,1))
            check(cv+DELTA[i][j]==VAR[i],'conditional_variance_identity')
    for k in range(12):
        expected=R**(2*(k//2))*((VAR if k%2==0 else W)[0] if k<2 else sum(VAR if k%2==0 else W)/2)
        check(full_variance(0,None,k)==expected,'feedback_Bellman_closed_formula')
    gap=R*R*sum(DELTA[i][i]-DELTA[i][0] for i in range(2))/8
    check(gap>0,'strict_three_call_advantage')
    eta=F(1,10)*R*R
    for n in range(0,8):
        for L in range(1,31):
            frontier,splits=greedy(L,n)
            double,_=greedy(2*L,n)
            G=sum(map(energy,frontier.values()));G2=sum(map(energy,double.values()))
            t=max(map(energy,frontier.values()))
            check(all(energy(v)>=eta*t for v in frontier.values()),'balanced_actual_energy')
            check(G2<=G and G2>=2*eta**3*G,'profile_cardinality_stability')
            cut,cs=greedy(L,n,n)
            shallow={h for h in splits if len(h)<n}
            check(shallow.issubset(set(cs)),'depth_truncated_splits_retained')
            risk=sum(v[1]*variance(v) for v in cut.values())
            check(risk<=full_variance(0,None,n)/4+G,'finite_horizon_pruning_bound')
            check(all(len(h)<=n for h in cut),'paid_depth_budget')
            check(2*len(cut)-1<=2*L-1,'complete_binary_controller_count')
            check(sum(v[1] for v in cut.values())==1,'actual_stopped_mass_not_renormalized')
    for M in range(1,257):
        m=(M+1)//2
        check(2*m-1<=M,'autonomous_all_nodes_fit')
        check(M<=2*m,'constant_cardinality_conversion')
        if M>=7:
            L=(M-1)//3
            check(1+3*L<=M and L>=2,'erasure_controller_product_count')
            check(M<=5*L,'joint_cardinality_comparison')
    for e in (F(0),F(1,100),F(1,4),F(1,2)):
        check(2*e*F(1,4)==e/2,'attained_erasure_task_risk')
        check(1-(1-2*e)==2*e,'complete_bit_deficiency_lower')
    check(F(1,4)*(1-2*R)**2>F(9,100)*(1+R*R),'symbolic_feedback_gap_positive')
    check(2*4-1>4,'negative:leaf_count_is_not_controller_count')
    check(VAR[0]!=0,'negative:preparation_not_finite_acquired_law')
    check(Q[0][0]!=Q[1][0],'negative:unread_tails_not_independent_fair')
    cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).with_name('regression_r9.py'))]
    result=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if result.returncode: raise RuntimeError(result.stdout)
    inherited=json.loads(result.stdout);check(inherited['status']=='PASS','retained_R9_R8_R7_R6_suites')
    print(json.dumps({'status':'PASS','native_checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
                     'exact_moments':{'means':[[str(x) for x in row] for row in MEAN],'variance':[str(x) for x in VAR],
                                      'one_observation_variance':[str(x) for x in W],'three_call_feedback_gain':str(gap)},
                     'retained_R9':inherited,'scope':'finite exact checks only; the manuscript contains the general proofs'},sort_keys=True,indent=2))
if __name__=='__main__': main()
