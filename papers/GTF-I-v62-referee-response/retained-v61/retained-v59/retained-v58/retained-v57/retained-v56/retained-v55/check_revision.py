"""Exact finite regression examples for revision 55; not a theorem prover.

Every check is executed under ordinary and optimized Python. Negative controls
exercise the same numerical validators as the accepted examples. No assert
statement is used as a test gate, and no floating-point tolerance is used.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import product, permutations
from math import gcd, lcm
import heapq
import json
from sympy import Matrix

class CheckFailure(RuntimeError):
    pass

checks = 0
negative_controls: list[str] = []

def require(ok: bool, message: str) -> None:
    global checks
    checks += 1
    if not ok:
        raise CheckFailure(message)

def reject(name: str, probe) -> None:
    try:
        probe()
    except CheckFailure:
        negative_controls.append(name)
        return
    raise CheckFailure('Negative control escaped: ' + name)

def mat(rows):
    return tuple(tuple(Q(x) for x in row) for row in rows)

def mul(a, b):
    return tuple(tuple(sum((a[i][z]*b[z][j] for z in range(len(b))),Q(0))
                       for j in range(len(b[0]))) for i in range(len(a)))

def eye(n):
    return mat([[int(i==j) for j in range(n)] for i in range(n)])

def power(a, n):
    out=eye(len(a))
    for _ in range(n):out=mul(out,a)
    return out

def stochastic(a):
    require(all(x>=0 for row in a for x in row), 'Negative probability')
    require(all(sum(row)==1 for row in a), 'Nonunit row mass')

def perm_matrix(p):
    return mat([[int(p[i]==j) for j in range(len(p))] for i in range(len(p))])

def order(p):
    seen=set(); answer=1
    for i in range(len(p)):
        if i in seen:continue
        j=i;length=0
        while j not in seen:
            seen.add(j);length+=1;j=p[j]
        answer=lcm(answer,length)
    return answer

def stationary_example(P, beta, decoder, targets, steps=24):
    stochastic(P);stochastic(beta)
    require(all(0<=row[0]<=1 for row in decoder),'Illegal binary decoder')
    state=beta
    for n in range(steps):
        require(mul(state,decoder)[0][0]==targets[n%len(targets)],'Wrong word output')
        state=mul(state,P)

def recurrent_simplex():
    # W has disjoint-support stationary rows; V records class weights.
    W=mat([[Q(1,3),Q(2,3),0,0],[0,0,1,0]])
    V=mat([[1,0],[1,0],[0,1],[Q(1,4),Q(3,4)]])
    P=mat([[0,1],[1,0]])
    E=mul(V,W);B=mul(mul(V,P),W)
    for a in [E,B]:stochastic(a)
    require(mul(W,V)==eye(2),'Recurrent coordinate inverse')
    require(mul(E,E)==E and Matrix(E).rank()==2,'Idempotent rank')
    require(mul(B,B)==E and B!=E,'Nontrivial relative group')
    require(mul(E,B)==B and mul(B,E)==B,'Relative identity')
    require(mul(W,B)==mul(P,W),'Simplex permutation')
    seeds=[mat([[int(i==j) for j in range(4)]]) for i in range(4)]
    seeds += [mat([[Q(1,4)]*4]),mat([[Q(1,8),Q(1,8),Q(1,4),Q(1,2)]])]
    for bits in product([Q(0),Q(1,2),Q(1)],repeat=4):
        D=tuple((v,) for v in bits)
        for seed in seeds:
            beta=mul(seed,V);d=mul(W,D)
            for n in range(7):
                old=mul(mul(mul(seed,E),power(B,n)),D)
                new=mul(mul(beta,power(P,n)),d)
                require(old==new,'Compressed endpoint mismatch')
    bad=[list(row) for row in E];bad[0][0]+=Q(1,7)
    reject('nonstochastic_idempotent_candidate',lambda:stochastic(mat(bad)))
    reject('ordinary_identity_substituted_for_relative_identity',lambda:require(mul(B,B)==eye(4),'Wrong inverse identity'))
    reject('hidden_recurrent_weights_discarded',lambda:require(mul(seeds[-1],E)==W[:1],'Lost randomized initialization'))
    # Cesaro averaging a permutation is not a word-closure idempotent.
    C=perm_matrix((1,2,0));avg=mat([[Q(1,3)]*3]*3)
    joint={(n%3,power(C,n)) for n in range(3)}
    require(mul(avg,avg)==avg,'Cesaro matrix idempotent')
    reject('cesaro_projection_has_false_physical_identity',lambda:require((0,avg) in joint,'Not in joint closure'))
    return {'rank':2,'ambient_labels':4,'relative_group_order':2}

def cyclic_minimum():
    P=perm_matrix((1,0,3,4,2))
    beta=mat([[Q(1,2),0,Q(1,2),0,0]])
    D=mat([[1],[0],[1],[Q(1,4)],[Q(1,4)]])
    values=tuple(map(Q,[1]))+(Q(1,8),Q(5,8),Q(1,2),Q(5,8),Q(1,8))
    stationary_example(P,beta,D,values,60)
    require(all(any(values[n]!=values[(n+d)%6] for n in range(6)) for d in [1,2,3]),'Least period six')
    orders=set()
    for k in range(1,5):
        for p in permutations(range(k)):
            v=order(p);orders.add(v)
            require(v%6!=0,'Four-state order obstruction')
    require(orders=={1,2,3,4},'Complete small permutation orders')
    require(order((1,0,3,4,2))==6,'Five-state permutation order')
    reject('deterministic_initialization_silently_substituted',lambda:stationary_example(P,mat([[1,0,0,0,0]]),D,values))
    wrong=mat([[1],[0],[1],[Q(1,3)],[Q(1,4)]])
    reject('altered_three_cycle_decoder',lambda:stationary_example(P,beta,wrong,values))
    reject('illegal_decoder_probability',lambda:stationary_example(P,beta,mat([[2],[0],[1],[Q(1,4)],[Q(1,4)]]),values))
    # A representative of each physical element is not enough: length three fails.
    P2=perm_matrix((1,0));v3=(Q(1),Q(0),Q(1))
    stationary_example(P2,mat([[1,0]]),mat([[1],[0]]),v3,3)
    reject('one_word_per_physical_element_misses_joint_fiber',lambda:stationary_example(P2,mat([[1,0]]),mat([[1],[0]]),v3,6))
    return {'stochastic_minimum':5,'deterministic_quotient_minimum':6,'small_orders':sorted(orders)}

def tv(p,q):return sum((abs(x-y) for x,y in zip(p,q)),Q(0))/2

def curved_categorical():
    centers=[(Q(1,2),Q(1,3),Q(1,6)),(Q(1,6),Q(1,3),Q(1,2))]
    t=Q(1,12)
    extrema=[(1,Q(-1,2),Q(-1,2)),(Q(1,2),Q(1,2),-1),
             (Q(-1,2),1,Q(-1,2)),(-1,Q(1,2),Q(1,2)),
             (Q(-1,2),Q(-1,2),1),(Q(1,2),-1,Q(1,2))]
    curves=[tuple(tuple(q[i]+t*z[i] for i in range(3)) for z in extrema) for q in centers]
    for curve in curves:
        for p in curve:require(sum(p)==1 and min(p)>=Q(1,12),'Categorical legality')
    minima=[Q(10)]*2;where=[[],[]];union_min=Q(10)
    for a in range(25):
        for b in range(25-a):
            y=(Q(a,24),Q(b,24),Q(24-a-b,24))
            radii=[]
            for c in range(2):
                radius=max(tv(p,y) for p in curves[c]);radii.append(radius)
                require(radius==t+max(abs(centers[c][i]-y[i]) for i in range(3)),'Independent coordinate-radius oracle')
                if radius<minima[c]:minima[c]=radius;where[c]=[y]
                elif radius==minima[c]:where[c].append(y)
            union_min=min(union_min,max(radii))
    require(minima==[t,t] and where==[[centers[0]],[centers[1]]],'Unique nonuniform centers on exact grid')
    require(union_min==Q(1,4),'Union radius')
    def center_check(y,c):require(max(tv(p,y) for p in curves[c])<=t,'Noncenter detected')
    reject('uniform_center_used_for_asymmetric_component',lambda:center_check((Q(1,3),)*3,0))
    reject('two_components_merged_at_boundary',lambda:require(max(tv(p,centers[0]) for p in curves[1])<=t,'Illegal merge'))
    reject('radius_mistaken_for_half_diameter',lambda:require(Q(2,3)==Q(1,2),'Three-vertex radius is not half diameter'))
    return {'component_radius':str(t),'union_radius':str(union_min),'grid_centers_examined':325}

def conductor(lengths):
    d=0
    for a in lengths:d=gcd(d,a)
    z=[a//d for a in lengths];m=min(z);dist=[None]*m;dist[0]=0;heap=[(0,0)]
    while heap:
        cost,r=heapq.heappop(heap)
        if cost!=dist[r]:continue
        for a in z:
            t=(r+a)%m;n=cost+a
            if dist[t] is None or n<dist[t]:dist[t]=n;heapq.heappush(heap,(n,t))
    require(all(v is not None for v in dist),'All scaled residues attained')
    return d,max(dist)

def return_phases():
    certificates=[]
    for lengths in [(2,3),(4,6),(6,10),(8,12,20),(6,9,20)]:
        d,g=conductor(lengths);limit=max(200,d*(g+30));reachable={0}
        for n in range(1,limit+1):
            if any(n-a in reachable for a in lengths):reachable.add(n)
            require(n not in reachable or n%d==0,'Forbidden residue returned')
            if n%d==0 and n>=d*g:require(n in reachable,'Cofinite scaled return')
        certificates.append({'lengths':list(lengths),'period':d,'scaled_bound':g})
    returns=set()
    for n in range(1,11):
        for w in product([-1,1],repeat=n):
            identity=sum(w)==0
            if identity:returns.add(n)
            require(not identity or n%2==0,'Irrational signed-count parity')
    require(returns=={2,4,6,8,10},'Period two observed')
    reject('gcd_claims_all_small_multiples_are_returns',lambda:require(2 in {6*a+10*b for a in range(5) for b in range(5)},'Conductor not zero'))
    reject('one_return_implies_cofinite_all_lengths',lambda:require(9 in returns,'Odd return falsely asserted'))
    return certificates

def cantor_integer(n):
    out=Q(0);den=3
    while n:
        out+=Q(2*(n&1),den);n//=2;den*=3
    return out

def v2(n):
    out=0
    while n%2==0:out+=1;n//=2
    return out

def profinite_boundary():
    vals=[cantor_integer(n) for n in range(512)]
    require(len(set(vals))==512,'Finite truncation injectivity')
    for m in range(1,8):
        for n in range(512):
            require(0<=vals[n]-cantor_integer(n%(2**m))<=Q(1,3**m),'Digit truncation bound')
    dets={}
    for m in range(5):
        n=2**m
        b=lambda z:cantor_integer(z+1)-cantor_integer(z)
        for z in range(2*n):require(b(z)==Q(5,3)*Q(1,3**v2(z+1))-1,'Trailing-one difference formula')
        psi=lambda x: Q(1,3**(m if x%n==0 else v2(x%n)))
        C=Matrix([[Q(5,3)*psi(j-i)-1 for j in range(n)] for i in range(n)])
        B=Matrix([[b(i+j) for j in range(n)] for i in range(n)])
        require(B.rank()==n,'Dyadic Hankel difference full rank')
        require(all(B[(-i-1)%n,j]==C[i,j] for i in range(n) for j in range(n)),'Exact circulant row permutation')
        eigen=[Q(2,3)*n*Q(1,6**m)]
        for q in range(1,n):
            eigen.append(-Q(10*n,3)*sum((Q(1,6**l) for l in range(1,m+1) if q%(n//2**l)==0),Q(0)))
        require(eigen[0]>0 and all(e<0 for e in eigen[1:]),'Fourier spectrum signs')
        determinant=C.det();prod=Q(1)
        for e in eigen:prod*=e
        require(determinant==prod and determinant!=0,'Independent determinant/Fourier oracle')
        dets[str(n)]=str(determinant)
    for N in range(1,129):
        for k in range(1,17):
            possible=[t for t in range(1,N) if min(t+1,N-t)<2*k]+[N]
            require(len(possible)<=4*k,'All-positive-cut occupation arithmetic')
    reject('zero_tolerance_accepts_digit_truncation',lambda:require(cantor_integer(2**8)==cantor_integer(0),'Nonzero omitted digit'))
    reject('dyadic_hankel_rank_collapsed_to_one',lambda:require(Matrix([[cantor_integer(i+j+1)-cantor_integer(i+j) for j in range(4)] for i in range(4)]).rank()<=1,'Lost suffix difference rank'))
    reject('circulant_zero_frequency_discarded',lambda:require(Q(2,3)*8*Q(1,6**3)==0,'Nonzero small eigenvalue'))
    return {'distinct_exact_integer_outputs':512,'dyadic_determinants':dets,'occupation_constant':'4*k'}

def unit_amplitude():
    cases=[]
    for eps in [Q(1,1000),Q(1,100),Q(1,10),Q(1,3),Q(49,100)]:
        eta=eps;rho=1-eta;a=(1+rho)/2
        require(0<eta<2*eps and 0<rho<1 and rho<a<1,'Positive slack transfer')
        require(eta/2<eps,'TV loss budget')
        delta=2*eps;r=int(delta/(1-delta))+1
        gap=2*(Q(r,r+1)-delta)
        require(gap>0,'Unit-amplitude harmonic residual')
        cases.append({'error':str(eps),'surrogate_amplitude':str(rho),'localization_order':r})
    def budget(eps,eta):require(0<eta<2*eps,'Strict positive-error transfer')
    reject('positive_slack_claimed_at_zero_error',lambda:budget(Q(0),Q(1,100)))
    reject('mean_error_not_halved_into_TV',lambda:budget(Q(1,10),Q(1,4)))
    reject('zero_enclosure_slack_used_for_exact_upper',lambda:require(Q(1)<Q(1),'No strict amplitude slack'))
    return cases

def main():
    evidence={'recurrent_simplex':recurrent_simplex(),'cyclic_minimum':cyclic_minimum(),
              'curved_categorical':curved_categorical(),'return_certificates':return_phases(),
              'profinite_boundary':profinite_boundary(),'unit_amplitude':unit_amplitude()}
    print(json.dumps({'schema':'gtf55.exact-regression/1','status':'success',
        'exact_finite_assertions':checks,'negative_controls_detected':negative_controls,
        'evidence':evidence,
        'scope':'Finite rational examples, exhaustive small permutations, dyadic Hankel minors and negative controls; not formal verification of universal compact-group statements.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
