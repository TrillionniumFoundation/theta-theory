#!/usr/bin/env python3
"""Exact finite regression only: not a verification of a continuum or adaptive supremum."""
from __future__ import annotations
from fractions import Fraction as F
from math import comb
import copy
import json
import coupled_codec as c

count = 0
controls = []
cases = {'binomial':0,'monotonicity':0,'codec':0,'legal_words':0,'algebraic_comparisons':0}


def check(ok, message):
    global count
    count += 1
    if not ok: raise RuntimeError(message)


def reject(name, fn):
    try: fn()
    except (ValueError, TypeError, KeyError):
        controls.append(name); return
    raise RuntimeError('negative control accepted: '+name)


def bino(n,p):
    return [F(comb(n,j))*p**j*(1-p)**(n-j) for j in range(n+1)]


def distance(n,p,q):
    return sum(abs(a-b) for a,b in zip(bino(n,p),bino(n,q)))


def run():
    for N in [1,2,3,7,16,31]:
        for q in [F(1,2),F(1,3),F(1,10),F(1,100),F(1,10000)]:
            prev = F(0)
            for ratio in [F(1),F(99,100),F(3,4),F(1,2),F(0)]:
                p=q*ratio; s=1-2*q; r=1-2*p
                tv=distance(N,p,q); R2=F(N)*(r-s)**2/(1-s*s+F(1,N))
                check(tv*tv >= min(F(1),R2)/4096,'finite radial lower')
                check(tv*tv <= min(F(4),9*R2),'finite radial upper')
                check(tv >= prev,'binomial monotonicity with decreasing p'); prev=tv
                cases['binomial'] += 1
                k=min(N,(1/(2*q)).numerator//(1/(2*q)).denominator)
                ep=(1-p)**k; eq=(1-q)**k
                cc=1/max(ep+eq,2-ep-eq); bb=(1-cc*(ep+eq))/2
                check(bb>=0 and bb+cc<=1 and cc>=F(1,2),'common processing kernel')
                check(ep-eq >= k*(q-p)/2,'block probability gap')
                check(bb+cc*ep == (1+cc*(ep-eq))/2,'opposite biases')
                for qp in [q,(q+1)/2,F(1)]:
                    check(distance(N,p,qp)>=tv,'binomial monotonicity through high q')
                    cases['monotonicity'] += 1
    # Algebraic comparisons against perfect-square Q provide independent exact values.
    for r in [F(1,5),F(1,2),F(4,5),F(1)]:
        for a in [F(0),r/2,r]:
            for b in [F(0),r/3,r]:
                for v in [F(0),F(1,7),F(1,2),F(1),F(2)]:
                    check(c.ratio_compare(b,a,r*r,v)==c.sign(b/(r+a)-v),'signed radical comparison')
                    cases['algebraic_comparisons']+=1
    check(c.nearest_algebraic(lambda v:c.sign(F(1,2)-v),1)==0,'tie toward zero')
    check(c.nearest_algebraic(lambda v:c.sign(F(3,4)-v),2)==1,'interior tie toward zero')
    vectors2=[('0','0'),('1','0'),('-1','0'),('0','1'),('3/5','4/5'),('1/2','1/3'),('-1/3','1/2'),('1/100000','-1/200000')]
    vectors3=[('0','0','0'),('1','0','0'),('0','0','-1'),('2/3','2/3','1/3'),('1/2','1/3','1/5'),('-1/2','1/3','-1/5'),('1/4','1/4','1/4')]
    for N,error in [(1,F(1,4)),(2,F(1,8)),(7,F(1,16)),(31,F(1,64))]:
        for d,vs in [(2,vectors2),(3,vectors3)]:
            B,grids,starts=c.layers(N,error,d)
            check(F(B*B)>=64*N/error**2,'radial precision')
            check(B>=1 and starts[1]==1,'erased layer')
            for i in [1,max(1,B//2),max(1,B-1),B]:
                r=F(2*i*B,B*B+i*i); A=grids[i]
                check(F(A*A)>=64*(d-1)*c.scale_squared(N,r)/error**2,'angular precision')
                for body in [starts[i],starts[i]+(starts[i+1]-starts[i])//2,starts[i+1]-1]:
                    obj=c.header(N,error,d,body); y=c.decode_vector(obj); inst=c.decode(obj)
                    check(sum(q*q for q in y)==r*r,'exact norm of decoded layer')
                    check(inst.d==2 and inst.n==1 and len(inst.outcomes)==2,'interface')
                    for mat in inst.outcomes:
                        a=F(mat[0][0][0],inst.denominator); b=F(mat[1][1][0],inst.denominator)
                        z=mat[0][1]
                        det=a*b-F(z[0]**2+z[1]**2,inst.denominator**2)
                        check(det==(1-r*r)/4,'effect determinant')
                    cases['legal_words']+=1
            for vs0 in vs:
                raw={'schema':c.TARGET,'bloch_vector':list(vs0)}; x=c.target(raw)
                obj=c.encode(raw,N,error); y=c.decode_vector(obj)
                check(c.verify(raw,obj),'target replay')
                check(sum(q*q for q in y)<=1,'legality')
                check(obj['fixed_length_bits']==(int(obj['codeword_count'])-1).bit_length(),'payload capacity')
                check(F(obj['adaptive_error_upper'])==error/4,'theorem certificate budget')
                # A separate rational consequence of the new metric upper bound.
                D2=F(N)*sum((a-b)**2 for a,b in zip(x,y))/(1-min(sum(a*a for a in x),sum(b*b for b in y))+F(1,N))
                check(36*D2<=error*error,'independent finite metric error check')
                cases['codec']+=1
    raw={'schema':c.TARGET,'bloch_vector':['1/2','1/3','1/5']}
    obj=c.encode(raw,3,F(1,8))
    for key,value in [('schema','bad'),('dimension',True),('horizon',False),('horizon',0),
                      ('requested_unhalved_error','2/16'),('requested_unhalved_error','0'),
                      ('requested_unhalved_error','1'),('radial_grid',1),('fixed_length_bits',False),
                      ('fixed_length_bits',0),('codeword_count','01'),('body_hex','00'),('body_hex','AB'),
                      ('body_hex','-1'),('body_hex',''),('body_hex',format(int(obj['codeword_count']),'x')),
                      ('adaptive_error_upper','0'),('scope','fabricated')]:
        bad=copy.deepcopy(obj);bad[key]=value
        reject('code-'+key+'-'+str(value),lambda bad=bad:c.decode(bad))
    bad=copy.deepcopy(obj);bad['visibility']='1/2'
    reject('free-visibility-header',lambda:c.decode(bad))
    bad=copy.deepcopy(obj);del bad['body_hex']
    reject('missing-payload',lambda:c.decode(bad))
    for label,v in [('outside',['1','1']),('decimal',['0.5','0']),('noncanonical',['2/4','0']),
                    ('bool',[True,'0']),('wrong-dimension',['0']),('not-rational',['nan','0'])]:
        reject(label,lambda v=v:c.encode({'schema':c.TARGET,'bloch_vector':v},3,F(1,8)))
    reject('extra-target-field',lambda:c.target({**raw,'visibility':'1'}))
    reject('duplicate-json',lambda:c.loads('{"schema":1,"schema":2}'))
    reject('invalid-chart-sign',lambda:c.chart(0,0,(0,),1,2))
    reject('invalid-chart-digit',lambda:c.chart(0,1,(2,),1,2))
    changed={'schema':c.TARGET,'bloch_vector':['-1/2','1/3','1/5']}
    check(not c.verify(changed,obj),'valid code for a different target rejected')
    controls.append('other-target-replay')
    c.layers(1,F(1,8),3)  # Populate the colliding integer-key cache entry.
    reject('boolean-horizon-cached',lambda:c.encode(raw,True,F(1,8)))
    reject('nonfraction-error-cached',lambda:c.layers(1,0.125,3))
    return {'schema':'gtf74.finite-regression/1','status':'success','exact_assertions':count,
            'cases':cases,'negative_controls':controls,'floating_point_decisions':False,
            'scope':'Finite exact binomial, algebraic, payload, legal-Choi and canonical-replay regression. Not a proof of the adaptive supremum, continuum covering, or priority.'}


if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
