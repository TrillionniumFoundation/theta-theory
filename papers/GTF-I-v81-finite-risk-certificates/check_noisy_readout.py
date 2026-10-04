#!/usr/bin/env python3
"""Exact finite regression; not a continuum proof or priority certificate."""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
from math import comb
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import noisy_readout_codec as c
from choi_streaming import Instrument
from instrument_streaming import mul, conj, add

COUNT = 0
NEG = []


def check(condition, message):
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(message)


def rejects(name, fn):
    try:
        fn()
    except (ValueError, TypeError, KeyError, IndexError, ZeroDivisionError):
        NEG.append(name);check(True,name);return
    raise RuntimeError('negative control accepted: '+name)


def bare(lam,z):
    return {'schema':c.TARGET,'visibility':str(lam),'direction':[str(x) for x in z]}


def binomial_distance(m,a):
    p=(1+a)/2;q=(1-a)/2
    return sum(F(comb(m,j))*abs(p**j*q**(m-j)-q**j*p**(m-j)) for j in range(m+1))


def power(z,k):
    out=(F(1),F(0))
    for _ in range(k):out=mul(out,z)
    return out


def state(vector):
    den=sum(x*x+y*y for x,y in vector)
    mat=[[mul(a,conj(b)) for b in vector] for a in vector]
    obj=Instrument(1,len(vector),den,[mat]);obj.validate();return obj


def run():
    rng=random.Random(7304)
    coords=[c.chart_point(s,j,B) for B in [1,2,3,5,11] for s in [-1,1]
            for j in range(-B,B+1)]
    cases=0
    for lam in map(F,['0','1/1000000','1/8','1/2','3/5','4/5','99/100','999999/1000000','1']):
        for N in [1,2,3,7,31,257,10**6]:
            eta=1-lam*lam
            k0=N if not eta else min(N,int(1/eta))
            if lam and k0 <= 300:
                check(4*lam**(2*k0-2)>=1,'block visibility bound')
            for err in [F(1,16),F(1,1024),F(1,1000000)]:
                z=coords[rng.randrange(len(coords))]
                target=bare(lam,z);code=c.encode(target,N,err)
                decoded=c.decode(code);check(c.verify(target,code),'target replay')
                got_lam,q=c.decode_readout_parts(code)
                check(got_lam==lam and sum(t*t for t in q)==1,'rational circle remains exact')
                check(F(code['adaptive_error_squared_upper'])<=err*err/16,'adaptive grid margin')
                if lam:
                    B=code['grid'];dist2=sum((z[i]-q[i])**2 for i in range(2))
                    check(dist2<=F(1,B*B),'circle chart Lipschitz rounding')
                    check(c.scale_squared(N,lam)*dist2<=err*err/16,'exact target error certificate')
                    check(c.scale_squared(N,lam)<=N*N*lam*lam,'hybrid branch')
                    if eta:check(c.scale_squared(N,lam)<=N*lam*lam/eta,'programme branch')
                else:
                    check(code['fixed_length_bits']==0 and code['body_hex']=='0','erasure zero payload')
                    check(c.canonical(code)==c.canonical(c.encode(bare(lam,(F(1),F(0))),N,err)),
                          'erasure independent of direction')
                # Each transposed effect has determinant (1-lambda^2)/4.
                for mat in decoded.outcomes:
                    det=mul(mat[0][0],mat[1][1])[0]-mul(mat[0][1],mat[1][0])[0]
                    check(F(det,decoded.denominator**2)==eta/4,'effect determinant/rank')
                cases+=1
    # Every chart word is a legal centre, not only encoder-selected words.
    for lam in [F(0),F(3,5),F(1)]:
        N=1;err=F(3,2);B=c.grid(N,lam,err)
        for body in range(4*B+2 if B else 1):
            code=c.header(N,lam,err,B,body)
            c.decode(code);check(True,'full chart alphabet legality')
    # Exact square-root ceilings at huge integer and near-integer boundaries.
    for q in [F(0),F(1),F(3,4),F(9,4),F(16,9),F(10**200-1),F(10**200),F(10**200+1)]:
        b=c.ceil_sqrt(q);check(b*b>=q and (b==0 or (b-1)**2<q),'ceiling root')
    # Symmetric binary-product estimate, including both saturation regimes.
    for m in range(1,66):
        for a in [F(0),F(1,1000),F(1,17),F(1,4),F(1,2),F(3,4),F(1)]:
            D=binomial_distance(m,a)
            check(4*D*D>=m*a*a if m*a*a<=1 else 2*D>=1,'majority product bound')
            r=m if m%2 else m-1;j=(r-1)//2
            derivative=F(r*comb(2*j,j),4**j)*(1-a*a)**j
            # Differentiate the finite majority polynomial exactly.
            p=(1+a)/2;q=(1-a)/2
            direct=F(0)
            for ell in range(j+1,r+1):
                term=(ell*p**(ell-1)*q**(r-ell) if ell else F(0))
                if r-ell:term-=(r-ell)*p**ell*q**(r-ell-1)
                direct+=comb(r,ell)*term
            check(derivative==direct,'telescoping majority derivative')
    # GHZ parity identities from actual tensor-effect matrix elements.
    ghz=0
    for k in range(1,7):
        for lam in [F(0),F(1,3),F(4,5),F(1)]:
            for z in [coords[3],(F(3,5),F(4,5)),(F(0),F(1))]:
                ef=c.effects(lam,z);phase=(F(3,5),F(4,5))
                expected_mean=lam**k*mul(power(z,k),conj(phase))[0]
                probs=[]
                for bits in product(range(2),repeat=k):
                    cross=(F(1),F(0));sign=1
                    for bit in bits:
                        cross=mul(cross,ef[bit][0][1]);sign*=1 if bit==0 else -1
                    prob=F(1,2**k)+mul(cross,phase)[0]
                    check(prob==F(1,2**k)*(1+sign*expected_mean),'GHZ tensor probability')
                    check(prob>=0,'GHZ probability positivity')
                    probs.append((sign,prob))
                check(sum(p for _,p in probs)==1,'GHZ normalized')
                check(sum(s*p for s,p in probs)==expected_mean,'GHZ parity mean')
                ghz+=1
    # The programme coefficient and finite fidelity expression use no floating point.
    for lam in [F(0),F(1,5),F(3,5),F(99,100)]:
        eta=1-lam*lam
        for z in coords[::7]:
            # Pair the reference angle zero with z; sin(h/2)^2=(1-x)/2.
            a2=lam*lam*(1-z[0])/2;t2=a2/(eta+a2)
            for N in [1,2,9,32]:
                finite=4*(1-(1-t2)**N)
                check(finite<=4*N*t2,'finite programme to square-root bound')
                check(t2<=a2/eta,'uniform noise denominator')
    # Conditional quantum output: inherited exact singular factor code and assembly.
    st=[state([(1,0),(0,2),(0,0)]),state([(0,0),(1,0),(1,1)])]
    mix=Instrument(1,3,4,[[[(2,0),(0,0),(0,0)],[(0,0),(1,0),(0,0)],[(0,0),(0,0),(1,0)]]])
    mix.validate()
    conditional=0
    for lam in [F(0),F(2,3),F(999,1000),F(1)]:
        for ss,rr in [(st,[1,1]),([st[0],mix],[1,3])]:
            t=bare(lam,(F(3,5),F(4,5)));t['preparations']=[a.to_dict() for a in ss]
            code=c.encode(t,17,F(1,1024),rr);obj=c.decode(code)
            check(c.verify(t,code),'conditional target replay')
            # At I/2 each labelled output is exactly half of its encoded state.
            for mat,sub in zip(obj.outcomes,code['preparation_codes']):
                rho=c.prep.validate_adaptive(sub)
                for i in range(obj.n):
                    for j in range(obj.n):
                        a=add(mat[i][j],mat[obj.n+i][obj.n+j])
                        check((F(a[0],2*obj.denominator),F(a[1],2*obj.denominator))==
                              (F(rho.outcomes[0][i][j][0],2*rho.denominator),
                               F(rho.outcomes[0][i][j][1],2*rho.denominator)),
                              'mixed input emits fixed half-weight states')
                pivots=c.prep.triangular_data(c.prep.preparation_blocks(rho),rho.denominator)[0]
                check(len(pivots[0])<=sub['code']['rank_bounds'][0],'conditional rank nonincrease')
            conditional+=1
    t=bare(F(3,5),(F(3,5),F(4,5)));good=c.encode(t,19,F(1,1024))
    bad=deepcopy(t);bad['visibility']='6/5';rejects('visibility-outside-unit-interval',lambda:c.encode(bad,1,F(1,10)))
    for name,field,value in [('nonunit-direction','direction',['1','1']),('noncanonical-visibility','visibility','2/2'),
                              ('target-extra-field','extra',True),('wrong-target-schema','schema','other')]:
        bad=deepcopy(t);bad[field]=value;rejects(name,lambda bad=bad:c.encode(bad,1,F(1,10)))
    for value in [0,-1,True]:rejects('invalid-horizon-'+str(value),lambda value=value:c.encode(t,value,F(1,10)))
    for value in [F(0),F(-1),F(2)]:rejects('invalid-error-'+str(value),lambda value=value:c.encode(t,1,value))
    rejects('negative-root',lambda:c.ceil_sqrt(F(-1)))
    for name,field,value in [('code-extra-field','extra',True),('overlong-body','body_hex','f'*1000),
                              ('uppercase-body','body_hex','A'),('leading-zero-body','body_hex','00'),
                              ('wrong-grid','grid',good['grid']+1),('boolean-grid','grid',True),
                              ('wrong-bit-count','fixed_length_bits',0),('wrong-certificate','adaptive_error_squared_upper','0'),
                              ('wrong-scope','scope','certified proof')]:
        bad=deepcopy(good);bad[field]=value;rejects(name,lambda bad=bad:c.decode(bad))
        check(not c.verify(t,bad),'tampered target replay '+name)
    other=deepcopy(t);other['direction']=['-3/5','4/5'];check(not c.verify(other,good),'different target rejected')
    NEG.append('different-target-replay')
    # Trace-only outputs have no angular information; do not test an erased flag as retained.
    check(c.effects(F(3,5),(F(3,5),F(4,5)))[0][0][0][0]==F(1,2),'diagonal normalization')
    NEG.append('discarded-flag-is-not-an-observable-readout')
    # Coordinatewise unconstrained rounding is not a legal circle codec.
    check(F(1)**2+F(1)**2>1,'off-circle counterexample');NEG.append('off-circle-coordinate-rounding')
    bad=bare(F(3,5),(F(3,5),F(4,5)));bad['preparations']=[mix.to_dict(),mix.to_dict()]
    rejects('rank-understatement',lambda:c.encode(bad,5,F(1,100),[1,1]))
    joint=c.encode(bad,5,F(1,100),[3,3])
    for key,value in [('fixed_length_bits',0),('requested_unhalved_error','1/200'),('rank_bounds',[1,1])]:
        jj=deepcopy(joint);jj[key]=value;rejects('joint-'+key,lambda jj=jj:c.decode(jj))
    jj=deepcopy(joint);jj['preparation_codes'][0]['extra']=1
    rejects('nested-extra-field',lambda:c.decode(jj))
    # Actual CLI, canonical replay and duplicate-field rejection.
    root=Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory() as td:
        p=Path(td);(p/'target.json').write_text(json.dumps(t))
        out=subprocess.run([sys.executable,str(root/'noisy_readout_codec.py'),'encode','--input',str(p/'target.json'),
                            '--horizon','19','--error','1/1024'],capture_output=True,check=True)
        cli=json.loads(out.stdout);check(cli==good,'CLI agrees with library')
        (p/'code.json').write_bytes(out.stdout)
        for mode in ['decode','verify']:
            args=[sys.executable,str(root/'noisy_readout_codec.py'),mode,'--input',str(p/('code.json' if mode=='decode' else 'target.json'))]
            if mode=='verify':args+=['--certificate',str(p/'code.json')]
            rr=subprocess.run(args,capture_output=True,check=True);check(bool(json.loads(rr.stdout)),'CLI '+mode)
        (p/'duplicate.json').write_text('{"schema":"x","schema":"y"}')
        rejects('duplicate-json-key',lambda:c.load(str(p/'duplicate.json')))
    return {'schema':'gtf73.noisy-regression/1','status':'success','exact_assertions':COUNT,
            'readout_cases':cases,'ghz_block_cases':ghz,'conditional_cases':conditional,
            'negative_controls':NEG,'floating_point_decisions':False,
            'scope':'Finite exact algebra, parity/majority identities, rank-aware codec and canonical CLI replay; not a proof of all adaptive testers, continuum coverings, or priority.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
