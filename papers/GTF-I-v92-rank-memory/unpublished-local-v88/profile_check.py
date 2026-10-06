#!/usr/bin/env python3
"""Finite exact tests; neither continuum proof nor physical learner execution."""
from fractions import Fraction as F
from itertools import product
from math import prod, factorial, isqrt
from pathlib import Path
import copy
import json
import tempfile
from profile_geometry import make_certificate, verify, maximum_profile, load_json

count=0;negative=0;bernoulli=0;quantumlaws=0

def check(ok):
    global count
    if not ok:raise RuntimeError('profile regression failed at check '+str(count+1))
    count+=1

def reject(fn):
    global negative
    try:fn()
    except (ValueError,TypeError,OverflowError):negative+=1;return
    raise RuntimeError('negative control was accepted')

def compositions(n):
    if n==0:yield ();return
    for a in range(1,n+1):
        for tail in compositions(n-a):yield (a,)+tail

def sign_law(biases):
    return {bits:prod(F(1,2)+(u if b else -u) for b,u in zip(bits,biases))
            for bits in product((0,1),repeat=len(biases))}

def pair_power(re,im,n):
    a,b=F(1),F(0)
    for _ in range(n):a,b=a*re-b*im,a*im+b*re
    return a,b

def ghz_law(m,s):
    re,im=(1-s*s)/(1+s*s),2*s/(1+s*s)
    phase=pair_power(re,im,m)[1]
    return {z:(1+(-1)**sum(z)*phase)/2**m for z in product((0,1),repeat=m)},phase

for n in range(1,11):
    groupings=list(compositions(n))
    for parts in groupings:
        cert=make_certificate({'allocation':list(parts)})
        v=sum(x*x for x in parts)
        check(cert['calls']==n and cert['second_moment']==v)
        check(n<=v<=max(parts)*n and F(cert['effective_width'])==F(v,n))
        for i in range(len(parts)-1):
            merged=parts[:i]+(parts[i]+parts[i+1],)+parts[i+2:]
            check(sum(x*x for x in merged)-v==2*parts[i]*parts[i+1])
    for b in range(1,n+1):
        pack,v=maximum_profile(n,b)
        check(v==max(sum(x*x for x in p) for p in groupings if max(p)<=b))
        check(F(n*b,2)<=v<=n*b and pack==[n//b,b,n%b])

for parts in [(1,),(2,),(1,2),(2,5,1),(8,1,1),(1,4,19,2),(10**30,1)]:
    for phase in [F(1,4),F(1,5),F(1,8),F(1,17),F(1,1000)]:
        payload={'allocation':list(parts),'phase_per_call':str(phase)}
        c=make_certificate(payload);p=c['public_clipping'];used=p['used_allocation']
        check(verify(payload,c)==c)
        check(all(m<=n and m>=1 for m,n in zip(used,parts)))
        check(sum(used)<=sum(parts))
        for m,n in zip(used,parts):
            check(0<m*phase<=F(1,2))
            if m<n:check(m*phase>=F(1,4))

# The lower inequality is compared exactly after squaring the nonnegative terms.
for xs in [(F(1,8),),(F(1,8),F(1,4)),(F(1,20),F(1,7),F(1,3)),
           (F(1,2),)*5,(F(1,30),F(1,40),F(1,20),F(1,10)),(F(0),F(1,6))]:
    for alpha in (F(1,8),F(1,3),F(1)):
        for choices in product((0,1),repeat=len(xs)):
            us=[x*(alpha if bit else 1) for bit,x in zip(choices,xs)]
            law=sign_law(us);base=F(1,2**len(xs));dist=sum(abs(v-base) for v in law.values())
            check(sum(law.values())==1 and all(v>=0 for v in law.values()))
            check(dist*dist>=alpha*alpha/F(4096)*min(1,sum(x*x for x in xs)))
            bernoulli+=1

# Direct interval evaluation of the common weighted sine readout.
# For these examples S is a rational square, so every weight is rational.
weighted_readouts=0
for xs in [(F(3,10),F(2,5)),(F(3,20),F(1,5)),(F(1,4),)*4,(F(1,2),)*4,
           (F(0),F(3,20),F(1,5))]:
    ss=sum(x*x for x in xs)
    root=F(isqrt(ss.numerator),isqrt(ss.denominator))
    check(root*root==ss)
    aa=max(root,ss);tt=[x/(16*aa) for x in xs]
    check(max(tt)<=F(1,16) and sum(t*t for t in tt)<=F(1,256))
    for alpha in [F(1,8),F(1,3),F(1)]:
        for choose in product((0,1),repeat=len(xs)):
            us=[x*(alpha if bit else 1) for x,bit in zip(xs,choose)]
            law=sign_law(us);low=F(0)
            for bits,p in law.items():
                yy=sum(t*(1 if b else -1) for t,b in zip(tt,bits))
                # Taylor degree 7 with a global 9th-derivative remainder bound.
                poly=yy-yy**3/factorial(3)+yy**5/factorial(5)-yy**7/factorial(7)
                err=abs(yy)**9/factorial(9)
                low+=p*(poly-err)
            check(low>=alpha*min(1,root)/64)
            weighted_readouts+=1

# Complete qubit GHZ laws and their unequal independent tensor products.
for parts in [(1,2),(1,3),(2,3),(1,1,2),(1,2,3)]:
    for s in (F(1,20),F(1,10),F(1,7)):
        laws=[ghz_law(m,s) for m in parts]
        for law,signal in laws:
            check(sum(law.values())==1 and all(p>=0 for p in law.values()))
            check(sum(abs(p-F(1,len(law))) for p in law.values())==abs(signal))
        full={};parity={bits:F(0) for bits in product((0,1),repeat=len(parts))}
        for records in product(*[tuple(law) for law,_ in laws]):
            prob=prod(law[r] for (law,_),r in zip(laws,records))
            full[records]=prob;parity[tuple(sum(r)%2 for r in records)]+=prob
        base=F(1,2**sum(parts));d=sum(abs(p-base) for p in full.values())
        dp=sum(abs(p-F(1,2**len(parts))) for p in parity.values())
        check(sum(full.values())==1 and d==dp)
        for bits,p in parity.items():
            check(p==prod((1+(-1)**bit*sig)/2 for bit,(_,sig) in zip(bits,laws)))
        # With these fixed small positive angles, signal gaps dominate m*s/4.
        check(all(sig/2>=m*s/4 for m,(_,sig) in zip(parts,laws)))
        ss=sum((m*s/4)**2 for m in parts)
        check(d*d>=min(1,ss)/4096)
        quantumlaws+=1

payload={'allocation':[1,2,7,3],'phase_per_call':'1/20'}
c=make_certificate(payload)
for bad in [[],[0],[-1],[True],[1.0],['1'],None]:
    reject(lambda bad=bad:make_certificate({'allocation':bad}))
for phase in ['0','-1/10','1/3','2/40',True,0.05]:
    reject(lambda phase=phase:make_certificate({'allocation':[2],'phase_per_call':phase}))
reject(lambda:make_certificate({'allocation':[1,2]},max_groups=1))
reject(lambda:make_certificate({'allocation':[1],'unknown':0}))
reject(lambda:maximum_profile(3,4))
for key in ['calls','second_moment','groups','maximum_second_moment_at_same_budget']:
    bad=copy.deepcopy(c);bad[key]+=1;reject(lambda bad=bad:verify(payload,bad))
bad=copy.deepcopy(c);bad['public_clipping']['used_allocation'][0]+=1;reject(lambda:verify(payload,bad))
bad=copy.deepcopy(c);bad['physical_protocol_executed']=0;reject(lambda:verify(payload,bad))
bad=copy.deepcopy(c);bad.pop('resource_model');reject(lambda:verify(payload,bad))
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/'duplicate.json';p.write_text('{"allocation":[1],"allocation":[2]}')
    reject(lambda:load_json(p))

print(json.dumps({'schema':'gtf88.profile-regression/1','status':'success','positive_checks':count,
 'negative_controls':negative,'exact_unequal_bernoulli_laws':bernoulli,
 'complete_unequal_GHZ_product_laws':quantumlaws,'certified_common_readout_examples':weighted_readouts,'integer_compositions_through':10,
 'continuum_proof_by_replay':False,'physical_protocol_executed':False,
 'general_recovery_synthesized':False,'independent_priority_certified':False},sort_keys=True,indent=2))
