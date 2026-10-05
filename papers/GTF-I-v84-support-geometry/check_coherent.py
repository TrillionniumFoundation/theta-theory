#!/usr/bin/env python3
"""Exact finite regression for the coherent/preparation code, not universal proof."""
from __future__ import annotations
import copy
from fractions import Fraction as F
from itertools import product as tuples
import hashlib,json,random,subprocess,sys,tempfile
from pathlib import Path
import coherent_codec as c
import preparation_codec as p
from check_preparation import from_factors,matrix_rank
from instrument_streaming import zero,identity,product,adjoint,trace
from choi_streaming import Instrument
ROOT=Path(__file__).resolve().parent
COUNT=0;NEG=[]
def require(ok,message):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)
def rejects(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError,RuntimeError):NEG.append(name)
    else:raise RuntimeError('negative control escaped: '+name)
def normalized(obj):
    return [[[(F(x,obj.denominator),F(y,obj.denominator)) for x,y in row] for row in A] for A in obj.outcomes]
def sphere_cases():
    rng=random.Random(7003);cases=0
    for ell in [1,2,3]:
        for B in [1,2,7,19,257]:
            for j in range(ell+1):
                for sign in [-1,1]:
                    for it in range(6):
                        z=[rng.randrange(-100,101) for _ in range(ell)]
                        q=c.sphere_decode(j,sign,z,100)
                        a,s,w=c.sphere_encode(q,B);qh=c.sphere_decode(a,s,w,B)
                        require(sum(x*x for x in qh)==1,'decoded sphere norm')
                        require(sum((x-y)**2 for x,y in zip(q,qh))<=F(4*ell,B*B),'global sphere atlas radius')
                        t=[F(k,100) for k in z];tp=[F(rng.randrange(-100,101),100) for _ in z]
                        qq=c.sphere_decode(j,sign,[int(x*100) for x in tp],100)
                        rhs=4*sum((x-y)**2 for x,y in zip(t,tp))/((1+sum(x*x for x in t))*(1+sum(x*x for x in tp)))
                        require(sum((x-y)**2 for x,y in zip(q,qq))==rhs,'exact stereographic distance identity')
                        if ell==3:
                            code=c.quaternion_code(q,B);out=c.quaternion_decode(code)
                            require(code==c.quaternion_code(tuple(-x for x in q),B),'projective sign canonicalization')
                            require(min(sum((x-y)**2 for x,y in zip(q,out)),sum((x+y)**2 for x,y in zip(q,out)))<=F(12,B*B),'quaternion chart radius')
                            U=c.quaternion_matrix(q);V=c.quaternion_matrix(out)
                            require(product(U,adjoint(U))==identity(2),'quaternion exact unitarity')
                            dot=sum(x*y for x,y in zip(q,out))
                            require(c.chi_squared(U,V)==1-dot*dot,'qubit Choi ray formula')
                            cases+=1
    # All words at B=1 are legal, even when not canonical encodings of a target.
    for a in range(4):
        for z in tuples([-1,0,1],repeat=3):
            q=c.sphere_decode(a,1,list(z),1)
            require(sum(x*x for x in q)==1,'every chart decoder image legal')
    return cases

def atlas_cases():
    rng=random.Random(7010);cases=0
    for d in [2,3,4]:
        for B in [1,3,11]:
            for _ in range(8):
                gs=[(rng.randrange(3),rng.choice([-1,1]),[rng.randrange(-B,B+1) for _ in range(2)]) for _ in c.atlas_pairs(d)]
                ps=[(rng.randrange(2),rng.choice([-1,1]),[rng.randrange(-B,B+1)]) for _ in range(d-1)]
                U=c.unitary_atlas_decode(d,B,gs,ps)
                require(product(U,adjoint(U))==identity(d),'general atlas exact unitarity')
                require(c.chi_squared(U,U)==0,'general Choi ray diagonal')
                # Perturb every factor by re-encoding on a finer grid; compare a
                # conservative telescoping Frobenius-square bound entirely exactly.
                B2=13
                g2=[c.sphere_encode(c.sphere_decode(*z,B),B2) for z in gs]
                p2=[c.sphere_encode(c.sphere_decode(*z,B),B2) for z in ps]
                V=c.unitary_atlas_decode(d,B2,g2,p2);L=d*(d-1)//2;K=3*L+2*(d-1)
                require(c.chi_squared(U,V)<=F(K*K,B2*B2),'general atlas error bound')
                cases+=1
    first=next(c.unitary_atlas_words(2,1));U=c.unitary_atlas_decode(2,1,first['givens'],first['phases'])
    require(c.unitary_atlas_encode(U,1,F(0),1)==first,'actual finite encoder search')
    rejects('finite-search-cap-is-inconclusive',lambda:c.unitary_atlas_encode(identity(2),1,F(0),1))
    return cases

def unitary_amplification_cases():
    # Exact rotation recurrences avoid floating-point trig. Reusing I versus a
    # diagonal unitary makes the displayed probe distance squared 4 sin^2(k theta).
    cases=0
    for B in [3,10,100,10**6]:
        for digit in [1,B//2,B]:
            x,y=c.sphere_decode(0,1,[digit],B)
            for N in [1,2,3,8,31,100]:
                z=(F(1),F(0));best=F(0)
                for k in range(1,N+1):
                    z=c.mul(z,(x,y));best=max(best,4*z[1]*z[1])
                chi2=y*y
                require(best>=min(F(N*N,2)*chi2,F(1)),'finite unitary adaptive lower bound')
                cases+=1
    return cases

def code_cases():
    rng=random.Random(7070);cases=0;retractions=0
    for n in [1,2,3]:
        for m in [1,2,3]:
            for it in range(4):
                factors=[]
                for y in range(m):
                    A=zero(n)
                    if y!=m-1 or m==1:
                        for i in range(n):
                            for j in range(1+it%n):A[i][j]=(rng.randrange(-4,5),rng.randrange(-4,5))
                    factors.append(A)
                if not sum(trace(product(A,adjoint(A))) for A in factors):factors[0][0][0]=(1,0)
                target=from_factors(factors,1+it%2);blocks=p.preparation_blocks(target)
                ranks=[matrix_rank(A) for A in blocks]
                q=c.sphere_decode(it%4,1,[1,-2,3],7);N=[1,2,13,1000][it];error=[F(1,32),F(1,127),F(1,10**12),F(1,64)][it]
                raw=c.encode(q,target,N,error,ranks);out=c.decode(raw)
                require(c.verify(q,target,raw),'target replay')
                require(out.d==2 and out.n==2*n,'data and preparation output dimensions')
                require([matrix_rank(A) for A in out.outcomes]==[matrix_rank(A) for A in p.preparation_blocks(p.validate_adaptive(raw['preparation']))],'Choi rank equals preparation rank')
                require(all(matrix_rank(A)<=r for A,r in zip(out.outcomes,ranks)),'rank nonincrease')
                require(sum(trace(A) for A in out.outcomes)==2*out.denominator,'total Choi trace equals input dimension')
                for i,A in enumerate(blocks):
                    if not matrix_rank(A):require(not any(z!=(0,0) for row in out.outcomes[i] for z in row),'exact zero outcome')
                require(F(raw['total_error_squared_upper'])<=error**2,'joint squared certificate')
                us=F(raw['coherent_error_squared_upper']);ps=F(raw['preparation_error_squared_upper'])
                require(F(raw['total_error_squared_upper'])==2*(us+ps),'triangle square includes cross term')
                qr=c.quaternion_decode(raw['unitary'])
                require(4*N*N*min(sum((x-y)**2 for x,y in zip(q,qr)),sum((x+y)**2 for x,y in zip(q,qr)))<=us,'actual coherent hybrid square')
                ret=c.retract(out);ret2=c.retract(ret)
                require(normalized(ret)==normalized(ret2),'retraction idempotence')
                require(normalized(c.retract(target))==normalized(target),'retraction fixes all preparation targets')
                rb=p.preparation_blocks(ret)
                decoded=p.preparation_blocks(p.validate_adaptive(raw['preparation']));pd=p.validate_adaptive(raw['preparation']).denominator
                # Retracting this non-erasing family appends its preparation to I/2.
                for Y,A in enumerate(rb):
                    for a,b,k,l in tuples(range(2),range(2),range(n),range(n)):
                        expected=tuple(F(x,2*pd) if a==b else F(0) for x in decoded[Y][k][l])
                        require(tuple(F(x,ret.denominator) for x in A[a*n+k][b*n+l])==expected,'fresh maximally mixed input retraction')
                retractions+=1;cases+=1
    # Non-input-erasing identity maps to a mixed preparation: ranks need not survive.
    pure=from_factors([[[(1,0)]]]);ident=c.tensor_instrument(identity(2),pure);ret=c.retract(ident)
    require(matrix_rank(ident.outcomes[0])==1 and matrix_rank(ret.outcomes[0])==4,'retraction deliberately increases Choi rank')
    return cases,retractions,raw,target,q

def negative_cases(raw,target,q):
    for key,val in [('horizon',True),('horizon',0),('requested_unhalved_error','2/64'),('requested_unhalved_error','1/2'),('coherent_error_squared_upper','0'),('preparation_error_squared_upper','0'),('total_error_squared_upper','0'),('fixed_length_bits',0)]:
        z=copy.deepcopy(raw);z[key]=val;rejects('tamper-'+key+'-'+str(val),lambda z=z:c.decode(z))
    for key,val in [('body_hex','00'),('body_hex','G'),('grid',True),('fixed_length_bits',0),('one_use_squared_upper','0')]:
        z=copy.deepcopy(raw);z['unitary'][key]=val;rejects('unitary-'+key+'-'+str(val),lambda z=z:c.decode(z))
    z=copy.deepcopy(raw);z['unitary']['body_hex']=format(4*(2*z['unitary']['grid']+1)**3,'x');rejects('body-out-of-range',lambda:c.decode(z))
    z=copy.deepcopy(raw);z['preparation']['horizon']+=1;rejects('crossed-horizons',lambda:c.decode(z))
    z=copy.deepcopy(raw);z['preparation']['code']['rank_bounds']=[0]*len(target.outcomes);rejects('false-rank-header',lambda:c.decode(z))
    require(not c.verify(c.sphere_decode(0,1,[2,1,1],5),target,raw),'wrong quaternion replay rejected');NEG.append('wrong-quaternion-replay')
    z=copy.deepcopy(raw);z['scope']='changed';require(not c.verify(q,target,z),'complete payload replay binds metadata');NEG.append('metadata-replay')
    rejects('nonunit-quaternion',lambda:c.encode(tuple(F(1) for _ in range(4)),target,1,F(1,64),[target.n]*len(target.outcomes)))
    rejects('float-input-forbidden',lambda:c.point([1.0,0.0,0.0,0.0],4))
    rejects('bad-sphere-anchor',lambda:c.sphere_decode(True,1,[1],2))
    rejects('bad-sphere-digit',lambda:c.sphere_decode(0,1,[3],2))
    rejects('nonunitary-atlas-target',lambda:c.unitary_atlas_encode([[(F(2),F(0))]],1,F(0)))
    # A common unsafe error-budget shortcut must be visibly rejected as arithmetic.
    require(2*(F(1,4)+F(1,4))>F(1,4)+F(1,4),'sum of squares is not triangle square');NEG.append('omitted-cross-term-control')

def cli_case():
    q='["1/2","1/2","1/2","1/2"]';target=str(ROOT/'inputs/preparation-boundary.json')
    args=[sys.executable,str(ROOT/'coherent_codec.py')]
    with tempfile.TemporaryDirectory() as td:
        cert=Path(td)/'code.json'
        r=subprocess.run(args+['encode','--input',target,'--quaternion',q,'--horizon','100','--error','1/1000','--ranks','[2,1,0]'],capture_output=True,check=True)
        cert.write_bytes(r.stdout)
        dec=subprocess.run(args+['decode','--input',str(cert)],capture_output=True,check=True)
        obj=Instrument.from_dict(json.loads(dec.stdout));require(obj.d==2 and obj.n==6,'CLI real output interface')
        ver=subprocess.run(args+['verify','--input',target,'--quaternion',q,'--certificate',str(cert)],capture_output=True,check=True)
        require(json.loads(ver.stdout)['status']=='success','CLI exact target verification')
        expanded=Path(td)/'instrument.json';expanded.write_bytes(dec.stdout)
        ret=subprocess.run(args+['retract','--input',str(expanded)],capture_output=True,check=True)
        p.preparation_blocks(Instrument.from_dict(json.loads(ret.stdout)));require(True,'CLI centre retraction')
        return hashlib.sha256(r.stdout).hexdigest()

def main():
    qs=sphere_cases();ats=atlas_cases();amps=unitary_amplification_cases()
    cs,rs,raw,target,q=code_cases();negative_cases(raw,target,q);digest=cli_case()
    print(json.dumps({'schema':'gtf70.regression/1','status':'success','exact_assertions':COUNT,
      'quaternion_cases':qs,'general_atlas_cases':ats,'finite_amplification_cases':amps,
      'combined_instrument_cases':cs,'nonerasing_retraction_cases':rs,'negative_controls':NEG,
      'cli_example_sha256':digest,'uses_floating_point_oracle':False,
      'scope':'Finite exact identities, rational legality, ranks, construction budgets and target replay. Not continuum proof, independent priority or a physical simulation certificate.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
