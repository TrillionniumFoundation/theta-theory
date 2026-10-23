#!/usr/bin/env python3
"""Independent finite diagnostic of the proposed five-character obstruction.

This exhausts quotient-action families in the finite four-bit group. It does
not establish the general finite-group structural theorem or novelty.
"""
import collections
import itertools
import json
from fractions import Fraction as Q

checks=0
def require(test, message):
    global checks
    checks+=1
    if not test:raise RuntimeError(message)

S=frozenset((1,2,4,8,15))
spaces={frozenset((0,))}
pending=list(spaces)
while pending:
    H=pending.pop()
    for x in range(16):
        K=H|frozenset(h^x for h in H)
        if K not in spaces:spaces.add(K);pending.append(K)
require(len(spaces)==67,'four-bit vector-space lattice')
for H in spaces:
    require(0 in H and all(a^b in H for a in H for b in H),'subspace closure')
for size in range(1,5):
    for subset in itertools.combinations(S,size):
        require(__import__('functools').reduce(int.__xor__,subset,0)!=0,'proper circuit relation')
require(__import__('functools').reduce(int.__xor__,S,0)==0,'five-character circuit')

options=sorted((H for H in spaces if len(H)<=11),key=lambda H:(len(H),tuple(sorted(H))))
families=[];all_families=0
def search(start,cost,chosen,cover):
    global all_families
    all_families+=1
    if S<=cover:families.append(tuple(chosen))
    for i in range(start,len(options)):
        H=options[i]
        if cost+len(H)>11:continue
        search(i+1,cost+len(H),chosen+[H],cover|(H&S))
search(0,0,[],frozenset())
require(len(families)==52,'all budget-eleven target-cover families')
patterns=collections.Counter()
for fam in families:
    patterns[tuple(sorted(len(H) for H in fam))]+=1
    nontrivial=[H for H in fam if len(H)>1]
    require(all(len(H) in (2,4) for H in nontrivial),'no degree-eight target cover')
    require(sum(len(H) for H in nontrivial)==10,'target-carrying degree')
    for chi in S:
        require(sum(chi in H for H in fam)==1,'target character assigned once')
    for H in nontrivial:
        active=H&S
        require(len(active)==len(H)//2,'optimal character density')
        for chi in H-{0}-S:
            require(sum(chi in K for K in fam)==1,'auxiliary character cannot cancel')
    require(sum(len(H&S) for H in nontrivial)==5,'mass lower coefficient')

def chi(a,g):return 1 if (a&g).bit_count()%2==0 else -1

# Verify the separate orbit decoders and the exact cancellation on all 16 inputs.
for g in range(16):
    signs=[chi(a,g) for a in (1,2,4,8,15)]
    require(__import__('functools').reduce(int.__mul__,signs,1)==1,'circuit character product')
    indicator=Q((signs[0]==1 and signs[1]==1))
    majority=Q(sum(x==1 for x in signs[2:])>=2)
    target=Q(3,8)+sum(map(Q,signs))/8
    require((indicator+majority)/2==target,'degree-four plus degree-eight cancellation')
    require(target in (Q(0),Q(1,2),Q(1)),'probability boundary values')
    for t in (Q(0),Q(1,7),Q(3,5),Q(4,5),Q(1)):
        mixed=Q(3,8)+t*sum(map(Q,signs))/8
        require(0<=mixed<=1,'contrast probability')
        decoder_a=(1-t)*Q(3,8)+t*indicator
        decoder_b=(1-t)*Q(3,8)+t*majority
        require(0<=decoder_a<=1 and 0<=decoder_b<=1,'upper realization decoder bounds')
        require((decoder_a+decoder_b)/2==mixed,'all-word contrast realization')
        if t<=Q(3,5):
            small=[Q(3,8)+Q(5,8)*t*s for s in signs]
            require(all(0<=x<=1 for x in small),'degree-ten decoder bounds')
            require(sum(small)/5==mixed,'degree-ten response equality')

# Module rank and residual cardinality from character independence / direct tables.
matrix=[[chi(a,g) for a in (0,1,2,4,8,15)] for g in range(16)]
for i in range(6):
    for j in range(6):
        require(sum(row[i]*row[j] for row in matrix)==(16 if i==j else 0),'character orthogonality')
residuals={tuple(Q(3,8)+sum(Q(chi(a,g^h),8) for a in S) for h in range(16)) for g in range(16)}
require(len(residuals)==16,'six-dimensional response has sixteen residuals')

# Independently reconstruct the family-specific signed scores used in the
# robust corollary. W is an annihilator (a space of characters); its primal
# stabilizer consists of group elements on which every character in W is one.
expected_histograms={
    0:{-4:1,0:10,4:5},
    1:{-3:1,-1:6,1:4,3:2,5:3},
    2:{-2:5,0:4,2:2,4:4,6:1},
}
expected_norms={0:Q(3,2),1:Q(17,8),2:Q(9,4)}
distinct_partitions=set()
for fam in families:
    pairs=tuple(sorted(tuple(sorted(W&S)) for W in fam if len(W)==4))
    distinct_partitions.add(pairs)
    z={g:1-sum(chi(a,g) for a in S)
         +sum(chi(a^b,g) for a,b in pairs) for g in range(16)}
    require(dict(collections.Counter(z.values()))==expected_histograms[len(pairs)],
            'robust score histogram')
    score_norm=sum(Q(abs(value),16) for value in z.values())
    require(score_norm==expected_norms[len(pairs)] and score_norm<=Q(9,4),
            'robust score exact l1 norm')
    for W in fam:
        stabilizer=[h for h in range(16) if all(chi(a,h)==1 for a in W)]
        block=tuple(sorted(W&S))
        for g in range(16):
            average=sum(Q(z[g^h],len(stabilizer)) for h in stabilizer)
            expected=__import__('functools').reduce(int.__mul__,(1-chi(a,g) for a in block),1)
            require(average==expected and average>=0,'score nonnegative on quotient fibers')
    for t in (Q(0),Q(3,5),Q(2,3),Q(4,5),Q(1)):
        pairing=sum(Q(z[g],16)*(Q(3,8)+t*sum(chi(a,g) for a in S)/8) for g in range(16))
        require(pairing==(3-5*t)/8,'score exact target margin')
        if t>Q(3,5):
            radius=(5*t-3)/18
            require(0<radius<t/8,'robust radius preserves five active coefficients')
            eta=radius*Q(99,100)
            require(pairing+score_norm*eta<0,'strict robust finite-table certificate')
require(len(distinct_partitions)==26,'all singleton/pair robust witnesses')
print(json.dumps({'status':'PASS','role':'Independent author-team finite diagnostic, not human referee or formal proof',
                  'total_checks':checks,'exact_checks':checks,'floating_checks':0,
                  'checks_by_group':{'exact-finite-enumeration':checks},
                  'robust_witness_partitions':len(distinct_partitions),
                  'subspaces':len(spaces),'all_quotient_families_with_cost_at_most_11':all_families,
                  'target_cover_families':len(families),'patterns':{str(k):v for k,v in sorted(patterns.items())}},sort_keys=True))
