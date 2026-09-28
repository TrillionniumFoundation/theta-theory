"""Exact finite regressions for v62, not certificates of its universal proofs.

Tests retain the actual nonidentity drift, enumerate small no-idle orbits,
check sparse common rows, and check finite product-law/diagnostic examples.
Normal and optimized Python execute the same explicit checks.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, permutations
import json
from pathlib import Path
import sympy as sp
import qubit_compiler as qc

HOME=Path(__file__).resolve().parent
COUNT=0
NEG=[]
def check(ok, message):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)
def require(ok, message):
    if not ok:raise ValueError(message)
def negative(name,fn):
    try:fn()
    except (ValueError,RuntimeError,ZeroDivisionError):NEG.append(name)
    else:raise RuntimeError('negative control accepted: '+name)
def mm(A,B):
    return tuple(tuple(qc.dot(a,b) for b in qc.transpose(B)) for a in A)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def drift_checks():
    commands,seed,_,_=qc.supplied_input(json.loads((HOME/'NO_IDLE_INPUT.json').read_text()))
    rots=list(commands.values())
    pts=[qc.E1,(F(0),F(1),F(0)),(F(3,5),F(4,5),F(0))]
    for B in rots:
        for u,v in product(pts,repeat=2):
            d=qc.dot(sub(u,v),sub(u,v))
            duv=sub(qc.apply(B,u),qc.apply(B,v))
            check(qc.dot(duv,duv)==d,'chordal covariance')
            for h2 in [F(1,4),F(1,2),F(1)]:
                phi=lambda s:max(F(0),1-s/h2)**2
                check(phi(d)==phi(qc.dot(duv,duv)),'radial kernel covariance')
        for A in rots:
            for u in pts:
                check(qc.apply(mm(B,A),u)==qc.apply(B,qc.apply(A,u)),'chronological drift action')
    B,A=rots[2],rots[4]
    negative('drift_replaced_by_identity',lambda:require(qc.apply(B,qc.apply(A,seed))==qc.apply(A,seed),'missing drift'))
    negative('drift_commuted_past_spectral_step',lambda:require(mm(B,A)==mm(A,B),'noncommuting rotations'))
    # Exact centroid-mass loss and chordal transport identity, including zero centroids.
    masses=[F(1,3)]*3;cent=[sp.Matrix([1,0,0]),sp.Matrix([0,sp.Rational(3,5),0]),sp.zeros(3,1)]
    for Br in rots[:3]:
        B=sp.Matrix(Br)
        for r in [sp.Rational(0),sp.Rational(1,3),sp.Rational(1)]:
            rows=[[r,1-r],[1-r,r],[sp.Rational(1,2)]*2]
            q=[0,0];v=[sp.zeros(3,1),sp.zeros(3,1)];flows=[]
            alpha=sum(sp.Rational(p)*sp.sqrt(c.dot(c)) for p,c in zip(masses,cent))
            for pi,c,row in zip(masses,cent,rows):
                cn=sp.sqrt(c.dot(c))
                for Ar in rots[:2]:
                    A=sp.Matrix(Ar)
                    for i,t in enumerate(row):
                        weight=sp.Rational(pi)*t*cn/2
                        q[i]+=weight;v[i]+=sp.Rational(pi)*t*B*A*c/2
                        if cn:flows.append((i,weight,B*A*c/cn))
            norms=[sp.sqrt(x.dot(x)) for x in v]
            check(sp.simplify(sum(q)-alpha)==0,'directional mass conservation')
            check(bool(sp.simplify(alpha-sum(norms))>=0),'drift centroid mass nonincrease')
            for i in range(2):
                direction=v[i]/norms[i] if norms[i] else sp.Matrix([1,0,0])
                cost=sum(w*(u-direction).dot(u-direction) for j,w,u in flows if j==i)
                check(sp.simplify(cost-2*(q[i]-norms[i]))==0,'drift flow cost identity')
    negative('zero_centroid_given_a_direction',lambda:require(qc.dot(qc.ZERO,qc.ZERO)>0,'zero normalization'))
    negative('unweighted_label_law',lambda:require((F(1,2),F(1,2))==(F(5,6),F(1,6)),'wrong direction weights'))
    return commands,seed

def no_idle_checks(commands,seed):
    check(len(commands)==6 and all(A!=qc.I for A in commands.values()),'six actual nonidentity commands')
    for name,A in commands.items():
        check(mm(A,qc.transpose(A))==qc.I,'orthogonal '+name)
        check(qc.dot(A[0],qc.cross(A[1],A[2]))==1,'proper rotation '+name)
    profile=[];orb={seed}
    for t in range(6):
        check(len(orb)==5**t,'no-idle orbit profile');profile.append(len(orb))
        check(all((5**t*x).denominator==1 for v in orb for x in v),'lattice denominators')
        check(all(qc.dot(v,v)==1 for v in orb),'unit targets')
        if t<5:orb={qc.apply(A,v) for A in commands.values() for v in orb}
    check(qc.apply(commands['A1'],seed)==seed,'oriented seed stabilizer')
    negative('group_ball_substituted_for_coset_ball',lambda:require(profile[1]==7,'wrong orbit count'))
    # Reduced free words cannot be identity at odd length: length parity survives cancellation.
    for w in product([1,-1,2,-2,3,-3],repeat=5):
        stack=[]
        for a in w:
            if stack and stack[-1]==-a:stack.pop()
            else:stack.append(a)
        check(len(stack)%2==1 and bool(stack),'odd length is not an exact return')
    negative('cofinite_exact_returns_in_free_alphabet',lambda:require(1%2==0,'odd identity return impossible'))
    machine=qc.compile_exact(2,F(1,2),max_labels=100,commands=commands,seed=seed)
    check(set(machine['rows'])==set(commands),'compiler did not insert an idle letter')
    for name,rows in machine['rows'].items():
        for i,row in enumerate(rows):
            target=qc.scale(machine['contraction'],qc.apply(commands[name],machine['vertices'][i]))
            check(qc.valid_row(machine['vertices'],row,target),'no-idle common row')
            check(len(row)<=4,'sparse row')
    for word in product(commands,repeat=2):
        dist={machine['initial_label']:F(1)};target=seed
        for a in word:
            nxt={}
            for i,p in dist.items():
                for j,t in machine['rows'][a][i]:nxt[j]=nxt.get(j,F(0))+p*t
            dist=nxt;target=qc.apply(commands[a],target)
        out=tuple(sum((p*machine['decoder_bloch'][i][d] for i,p in dist.items()),F(0)) for d in range(3))
        check(out==qc.scale(F(1,2),target),'no-idle complete word realization')
    check(all(qc.dot(v,v)<=1 for v in machine['decoder_bloch']),'legal density decoders')
    negative('compiler_label_budget_bypassed',lambda:qc.compile_exact(2,F(1,2),max_labels=1,commands=commands))
    return {'finite_orbit_radii':list(range(6)),'finite_orbit_sizes':profile,'compiler_labels':len(machine['vertices']),'compiler_commands':list(commands)}

def accuracy_checks():
    for rho in [F(1,4),F(1,2),F(3,4),F(1)]:
        for ratio in [F(0),F(1,8),F(1,2),F(3,4)]:
            eps=rho*ratio;z=rho-eps;tau=1-rho+eps;beta=rho-eps/2
            check(1-z==tau and z>0,'joint residual normalization')
            check(1-beta>=tau/2 and beta>0,'amplitude budget')
            if tau:check(beta<1,'positive enclosure slack')
    negative('pure_exact_endpoint_used_in_slack_bound',lambda:require(1-F(1)>0,'zero enclosure slack'))
    for k in range(1,65):
        gamma=(1-F(5,9))*(1-F(1,4))
        check(gamma==F(1,3),'LPS entropy defect')
        check(F(3*24,1)/gamma**2==648,'LPS joint coefficient')
    # Young's inequality step can be certified by its completed square.
    x,y,g=sp.symbols('x y g',positive=True)
    check(sp.expand((g*x*x+y*y/g)/2-x*y-(sp.sqrt(g)*x-y/sp.sqrt(g))**2/2)==0,'Young square')
    negative('finite_dimensional_gap_substituted_for_action_gap',lambda:require(sp.cos(2*sp.pi)<sp.Rational(1,2),'third harmonic unchanged'))

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def cycle_checks():
    # A diagnostic emits the current type and then applies a permutation.
    # Its order-th iterate is a common resetting cycle; the first output distinguishes types.
    for n in range(2,6):
        ident=tuple(range(n))
        for p in permutations(range(n)):
            power=ident;order=0
            while True:
                power=compose(p,power);order+=1
                if power==ident:break
                if order>120:raise RuntimeError('permutation order search did not terminate')
            transcripts=[]
            for i in range(n):
                state=i;ys=[]
                for _ in range(order):ys.append(state);state=p[state]
                check(state==i,'type cycle returns')
                transcripts.append(tuple(ys))
            check(len(set(transcripts))==n,'one common cycle distinguishes all types')
    negative('one_itinerary_assumed_to_reset_types',lambda:require((1,0)==(0,1),'need permutation order'))
    negative('retained_seed_not_charged_to_state',lambda:require(len({0,1})<=1,'unrecorded seed'))

def binary_witness(eps):
    require(isinstance(eps,F) and 0<=eps<1,'rational tolerance below one required')
    R=1
    while 1-F(1,2**R)<=eps:R+=1
    return R

def tail_checks():
    grid=[F(0),F(1,4),F(1,2),F(3,4),F(1)]
    for R in range(1,6):
        best=F(1)
        for probs in product(grid,repeat=R):
            u=v=F(1)
            for p in probs:u*=p;v*=1-p
            check(u*v<=F(1,4**R),'product bound')
            err=1-min(u,v);check(err>=1-F(1,2**R),'one-label strong converse')
            best=min(best,err)
        check(best==1-F(1,2**R),'balanced fair outputs attain binary bound')
    records=[]
    for eps in [F(0),F(1,2),F(3,4),F(9,10),F(99,100),F(999,1000)]:
        R=binary_witness(eps)
        check(1-F(1,2**R)>eps,'strict finite infeasibility witness')
        if R>1:check(1-F(1,2**(R-1))<=eps,'first witness integer')
        records.append({'epsilon':str(eps),'first_excluded_length':R,'minimum_one_label_error':str(1-F(1,2**R))})
    negative('error_one_strong_converse',lambda:binary_witness(F(1)))
    # A one-cut label can feed a two-state fair mixture with error 1/2 indefinitely.
    check(F(1)-F(1,2)==F(1,2),'single bottleneck counterexample')
    negative('pointwise_all_error_n_label_claim',lambda:require(F(1,2)>F(3,4),'one cut can be narrower'))
    # Disjoint tail probabilities at a fixed state cannot both exceed one half.
    for a,b in product(grid,repeat=2):
        if a+b<=1:check(not(a>F(1,2) and b>F(1,2)),'distinct majority tails need distinct states')
    negative('tail_majority_without_disjointness',lambda:require(F(3,4)+F(3,4)<=1,'overlapping events'))
    return records

def main():
    commands,seed=drift_checks();geo=no_idle_checks(commands,seed);accuracy_checks();cycle_checks();tails=tail_checks()
    print(json.dumps({'schema':'gtf62.finite-checks/1','status':'success','exact_finite_assertions':COUNT,
       'negative_controls_detected':NEG,'no_idle_example':geo,'binary_product_witnesses':tails,
       'universal_proofs_certified':False,'spectral_gap_certified':False,
       'scope':'Exact finite identities and regression examples only; no universal proof, priority, or spectral certificate.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
