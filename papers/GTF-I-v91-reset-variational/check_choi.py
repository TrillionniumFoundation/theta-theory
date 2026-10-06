#!/usr/bin/env python3
"""Exact finite tests of v66. No universal proof, gap or novelty certification."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import copy
import hashlib
import io
import json
import random
import subprocess
import sys
import tempfile
import choi_streaming as c
import instrument_streaming as old

ROOT=Path(__file__).resolve().parent
COUNT=0; NEG=[]

def require(ok,message):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)

def rejects(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,IndexError):NEG.append(name)
    else:raise RuntimeError('negative control escaped: '+name)

def outer(v):return [[c.mul(x,c.conj(y)) for y in v] for x in v]

def sqrt_upper(x):
    if x==0:return F(0)
    unit=1<<96;n=isqrt(x.numerator*unit*unit//x.denominator)
    if n*n*x.denominator<x.numerator*unit*unit:n+=1
    return F(n,unit)

def norm_upper(a,wa,b,wb):
    vals=[wa*x-wb*y for ar,br in zip(a,b) for az,bz in zip(ar,br) for x,y in zip(az,bz)]
    # All callers supply positive matrices and nonnegative block weights.
    # The trace-of-positive-parts bound avoids a loose Frobenius overestimate.
    return min(sum(abs(x) for x in vals),sqrt_upper(len(a)*sum(x*x for x in vals)),
               wa*c.trace(a)+wb*c.trace(b))

def choi_difference_upper(original, compiled, B):
    # Independent exact enclosure using both the direct difference and its
    # trace-correction/buffer decomposition. Q itself need not be positive.
    C,_=c.constants(original.d,original.n,len(original.outcomes))
    dn=original.d*original.n;m=len(original.outcomes);answer=F(0)
    for x,y in zip(original.outcomes,compiled.outcomes):
        values=[]
        for i in range(dn):
            for j in range(dn):
                for part in [0,1]:
                    values.append(F(y[i][j][part])-F(C if i==j and part==0 else 0)
                                  -F(B*x[i][j][part],original.denominator))
        perturb=min(sum(abs(v) for v in values),sqrt_upper(dn*sum(v*v for v in values)))
        decomposed=(perturb+C*dn+F(m*original.n*C*c.trace(x),original.denominator))/compiled.denominator
        direct=norm_upper(x,F(1,original.denominator),y,F(1,compiled.denominator))
        answer+=min(direct,decomposed)
    return answer

def from_kraus(spec):
    data={}
    for a,ys in spec.commands.items():
        blocks=[]
        for ks in ys:
            z=c.zero(spec.d**2)
            for k in ks:
                v=[k[alpha][i] for i in range(spec.d) for alpha in range(spec.d)]
                z=c.plus(z,outer(v))
            blocks.append(z)
        inst=c.Instrument(spec.d,spec.d,spec.q**2,blocks);inst.validate();data[a]=inst
    return c.Description(spec.d,spec.initial,data)

def description_dict(desc):
    return {'schema':'gtf66.choi-stream/1','dimension':desc.d,'initial_numerator':[[list(x) for x in row] for row in desc.initial],
            'commands':{a:x.to_dict() for a,x in desc.commands.items()}}

def prep_instrument(d,n):
    # Two preparation outcomes with a nontrivial rational state, and a zero one.
    v=[(i+1,(-1)**i) for i in range(n)];p=outer(v);z=c.trace(p)
    blocks=[]
    for weight in [2,1,0]:
        block=c.zero(d*n)
        for i in range(d):
            for alpha in range(n):
                for beta in range(n):
                    block[i*n+alpha][i*n+beta]=old.scale(p[alpha][beta],weight)
        blocks.append(block)
    inst=c.Instrument(d,n,3*z,blocks);inst.validate();return inst

def apply_reference(inst,p,r,y):
    # Registers use system-first/reference-second indices. Returns integer numerator.
    d,n=inst.d,inst.n;out=c.zero(n*r);mat=inst.outcomes[y]
    for alpha in range(n):
        for beta in range(n):
            for k in range(r):
                for l in range(r):
                    val=c.ZERO
                    for i in range(d):
                        for j in range(d):
                            val=c.add(val,c.mul(mat[i*n+alpha][j*n+beta],p[i*r+k][j*r+l]))
                    out[alpha*r+k][beta*r+l]=val
    return out

def compilation_checks():
    rng=random.Random(6601);cases=0
    examples=[prep_instrument(d,n) for d,n in [(1,1),(1,3),(2,1),(2,2),(2,3),(3,2)]]
    for path in sorted((ROOT/'inputs').glob('*-instrument.json')):
        desc=from_kraus(old.Specification.read(path))
        examples+=list(desc.commands.values())
    for inst in examples:
        for B in [1,3,16,1024,1<<18]:
            cert=c.compile_exact(inst,B);out=c.Instrument.from_dict(cert['instrument'])
            require(c.verify_compilation(inst,cert),'recomputed certificate')
            C,K=c.constants(inst.d,inst.n,len(inst.outcomes))
            require(out.denominator==B+len(inst.outcomes)*inst.n*C,'fixed channel denominator')
            upper=F(cert['diamond_error_upper'])
            total=choi_difference_upper(inst,out,B)
            require(total<=upper,'rigorous Choi trace bound')
            require(all(c.rational_psd(x) for x in out.outcomes),'compiled CP')
            require(all(abs(q).bit_length()<=out.denominator.bit_length()
                        for a in out.outcomes for row in a for z in row for q in z),'entry bit bound')
            require(F(K,out.denominator)==upper,'rational explicit constant')
            # Deliberate calibrated perturbations with additional diagonal grid errors.
            grid=[[[ (old.toward_zero(B*x,inst.denominator),old.toward_zero(B*y,inst.denominator))
                       for x,y in row] for row in a] for a in inst.outcomes]
            # Use a perturbation only when the original coordinate is exact on this grid.
            for yi,a in enumerate(inst.outcomes):
                for i in range(len(a)):
                    if B*a[i][i][0]%inst.denominator==0:
                        grid[yi][i][i]=c.add(grid[yi][i][i],(rng.choice([-1,1]),0))
            noisy=c.repair_grid(grid,inst.d,inst.n,B)
            require(choi_difference_upper(inst,noisy,B)<=upper,'calibrated noisy grid repair')
            cases+=1
    inst=prep_instrument(2,2);cert=c.compile_exact(inst,32)
    for key,value in [('diamond_error_upper','0'),('grid',16),('convention','output-first')]:
        bad=copy.deepcopy(cert);bad[key]=value
        require(not c.verify_compilation(inst,bad),'tampered '+key);NEG.append('tampered-'+key)
    bad=copy.deepcopy(cert);bad['instrument']['denominator']+=1
    require(not c.verify_compilation(inst,bad),'tampered denominator');NEG.append('tampered-denominator')
    bad=copy.deepcopy(cert);bad['instrument']['outcomes'][0][0][0]=(0,0)
    require(not c.verify_compilation(inst,bad),'tampered Choi entry');NEG.append('tampered-Choi-entry')
    rejects('zero-grid',lambda:c.compile_exact(inst,0))
    rejects('negative-dimension',lambda:c.constants(-1,2,1))
    return cases

def algebra_checks():
    cases=0
    for path in sorted((ROOT/'inputs').glob('*-instrument.json')):
        spec=old.Specification.read(path);desc=from_kraus(spec)
        rng=random.Random(6600+spec.d)
        for _ in range(12):
            p=outer([(rng.randrange(-4,5),rng.randrange(-4,5)) for i in range(spec.d)])
            if c.trace(p)==0:p=c.identity(spec.d)
            require(c.rational_psd(p),'rational Schur input')
            for a,inst in desc.commands.items():
                branches=spec.branches(p,a)
                for y,z in enumerate(branches):
                    got=inst.branch(p,y)
                    require(got==z,'input-first Choi contraction agrees with Kraus update')
                    require(c.rational_psd(got),'branch PSD');cases+=1
                require(sum(c.trace(z) for z in branches)==inst.denominator*c.trace(p),'mass identity')
            for B in [1,2,7,64]:
                rounded=c.round_density(p,B)
                # Referee's suggested scalar out-of-range claim is false on promised PSD inputs.
                qlast=rounded[-1][-1][0]-2*spec.d
                require(0<=qlast<=B,'last unrepaired diagonal remains in [0,1]')
    for a in [ [[(0,0),(1,0)],[(1,0),(1,0)]], [[(1,0),(2,0)],[(2,0),(1,0)]] ]:
        require(not c.rational_psd(a),'PSD negative control')
    NEG.extend(['zero-pivot-nonzero-row','indefinite-Hermitian-input'])
    # Full variable-dimension Schur examples with rank deficiency.
    for d in range(2,14):
        v=[(i+1,(-1)**i) for i in range(d)]
        require(c.rational_psd(outer(v)),'rank-one variable-dimension validation')
        require(c.rational_psd(c.plus(outer(v),c.identity(d))),'full-rank variable-dimension validation')
    # Ordinary transposition is positive and TP but fails complete positivity.
    swap=c.zero(4)
    for i in range(2):
        for j in range(2):swap[i*2+j][j*2+i]=(1,0)
    require(c.partial_trace(swap,2,2)==c.identity(2),'transpose is TP')
    require(not c.rational_psd(swap),'transpose Choi not positive')
    NEG.append('positive-TP-is-not-completely-positive')
    return cases

def reference_checks():
    desc=from_kraus(old.Specification.read(ROOT/'inputs/qubit-instrument.json'))
    # A maximally entangled state and an unbalanced entangled state; no separable restriction.
    vectors=[[(1,0),(0,0),(0,0),(1,0)],[(3,0),(0,0),(0,0),(0,4)]]
    cases=0
    for v in vectors:
        p=outer(v);z=c.trace(p)
        for a,inst in desc.commands.items():
            approx=c.Instrument.from_dict(c.compile_exact(inst,1<<18)['instrument'])
            delta=F(c.constants(2,2,len(inst.outcomes))[1],approx.denominator)
            err=F(0)
            for y in range(len(inst.outcomes)):
                u=apply_reference(inst,p,2,y);w=apply_reference(approx,p,2,y)
                require(c.rational_psd(u) and c.rational_psd(w),'entangled output PSD')
                err+=norm_upper(u,F(1,z*inst.denominator),w,F(1,z*approx.denominator));cases+=1
            require(err<=delta,'arbitrary-reference norm test')
    # Adaptive history with retained reference and genuine joint tester interventions.
    keys=list(desc.commands);insts={a:desc.commands[a] for a in keys}
    approximations={a:c.Instrument.from_dict(c.compile_exact(x,1<<20)['instrument']) for a,x in insts.items()}
    nodes=[((),outer(vectors[0]),F(1,2),outer(vectors[0]),F(1,2))]
    budget=F(0);stopped=[]
    for t in range(4):
        fresh=[];step_delta=F(0)
        for hist,p,wp,q,wq in nodes:
            a='a' if t==0 else ('m' if t==1 or sum(hist)%2 else 'v')
            inst=insts[a];approx=approximations[a]
            # The reference controls a system bit flip; a recorded outcome also
            # controls an imaginary phase. Both experiments use this same tester.
            tester=c.zero(4)
            for col,row in enumerate([0,3,2,1]):
                tester[row][col]=(0,1) if sum(hist)%2 and col==3 else (1,0)
            require(old.product(old.adjoint(tester),tester)==c.identity(4),'joint tester unitary')
            p=old.product(old.product(tester,p),old.adjoint(tester))
            q=old.product(old.product(tester,q),old.adjoint(tester))
            step_delta=max(step_delta,F(c.constants(2,2,len(inst.outcomes))[1],approx.denominator))
            for y in range(len(inst.outcomes)):
                u=apply_reference(inst,p,2,y);v=apply_reference(approx,q,2,y)
                node=(hist+(y,),u,wp/inst.denominator,v,wq/approx.denominator)
                # The same public stopping rule freezes selected paths.
                if t==1 and y==0:stopped.append(node)
                else:fresh.append(node)
        budget+=step_delta;nodes=fresh
        live=nodes+stopped
        error=sum(norm_upper(p,wp,q,wq) for _,p,wp,q,wq in live)
        require(sum(c.trace(p)*wp for _,p,wp,_,_ in live)==1,'true stopped mass')
        require(sum(c.trace(q)*wq for _,_,_,q,wq in live)==1,'compiled stopped mass')
        require(error<=budget,'common adaptive stopped hybrid bound')
        tv=sum(abs(c.trace(p)*wp-c.trace(q)*wq) for _,p,wp,q,wq in live)/2
        require(tv<=error/2,'TV normalization');cases+=len(live)
    # Sharp warning against pointwise rare-posterior inference, and valid weighted bound.
    rare=F(1,1024);p=c.identity(2);rho=[[(1,0),(0,0)],[(0,0),(0,0)]]
    sig=[[(0,0),(0,0)],[(0,0),(1,0)]]
    e=norm_upper(rho,rare,sig,rare)
    require(e==2*rare and norm_upper(rho,F(1),sig,F(1))==2,'rare posterior witness')
    require(rare*2<=2*e,'weighted posterior inequality')
    NEG.append('small-global-error-does-not-bound-every-rare-posterior')
    # Exact joint-instrument restriction tests do not exhaust all testers.
    require(len(stopped)>0 and len(nodes)>0,'nontrivial stopped and continuing branches')
    return cases

def numerical_history_checks():
    base=from_kraus(old.Specification.read(ROOT/'inputs/qubit-instrument.json'))
    insts={a:c.Instrument.from_dict(c.compile_exact(x,4096)['instrument']) for a,x in base.commands.items()}
    desc=c.Description(2,base.initial,insts);sim=c.ChoiStreamer(desc,80,2)
    require(sim.B is not None,'compiled-Choi trajectory uses positive grid')
    delta=F(24,sim.B)
    nodes=[((),base.initial,F(1,c.trace(base.initial)),sim.p,F(1,c.trace(sim.p)))];stopped=[];cases=0
    for t in range(3):
        fresh=[]
        for hist,p,wp,q,wq in nodes:
            a='a' if t==0 else ('m' if sum(hist)%2==0 else 'v');inst=insts[a]
            for y in range(len(inst.outcomes)):
                a1=inst.branch(p,y);b1=inst.branch(q,y);mass=c.trace(b1)
                q1=c.round_density(b1,sim.B) if mass else c.round_density(c.identity(2),sim.B)
                node=(hist+(y,),a1,wp/inst.denominator,q1,wq*mass/(inst.denominator*c.trace(q1)))
                if t==1 and y==0:stopped.append(node)
                else:fresh.append(node)
        nodes=fresh;allnodes=nodes+stopped;cases+=len(allnodes)
        require(sum(c.trace(p)*wp for _,p,wp,_,_ in allnodes)==1,'numerical true stopped mass')
        require(sum(c.trace(q)*wq for _,_,_,q,wq in allnodes)==1,'numerical simulated stopped mass')
        error=sum(norm_upper(p,wp,q,wq) for _,p,wp,q,wq in allnodes)
        require(error<=(t+2)*delta,'compiled-Choi numerical stopped error')
    return cases

def streaming_checks():
    cases=0;modes=set()
    for path in sorted((ROOT/'inputs').glob('*-instrument.json')):
        desc=from_kraus(old.Specification.read(path));raw=description_dict(desc)
        loaded=c.Description.from_dict(json.loads(json.dumps(raw)))
        rng=random.Random(6610+desc.d)
        for N,L in [(2,2),(9,2),(24,2),(24,200),(64,3)]:
            sim=c.ChoiStreamer(loaded,N,L);modes.add(sim.mode)
            p=[row[:] for row in desc.initial];wp=F(1,c.trace(p));wq=F(1,c.trace(sim.p))
            keys=list(desc.commands)
            for t in range(N):
                a=keys[t%len(keys)];inst=desc.commands[a]
                previous=[row[:] for row in sim.p]
                y=sim.step(a,lambda:rng.randrange(2))
                want=inst.branch(previous,y)
                require(c.rational_psd(sim.p),'streamed state PSD')
                require(c.trace(want)>0,'zero branch never sampled')
                require(sim.p==(want if sim.B is None else c.round_density(want,sim.B)), 'same recurrence')
                if sim.B is not None:require(c.trace(sim.p)==sim.B+2*desc.d**2,'fixed state denominator')
                else:require(c.trace(sim.p).bit_length()<=desc.exact_cap(N),'exact bit envelope')
                cases+=1
            require(sim.finish()['dimension']==desc.d,'finish dimension')
            rejects('too-many-commands-'+str(desc.d)+'-'+str(N)+'-'+str(L),lambda:sim.step(keys[0],lambda:0))
        bad=copy.deepcopy(raw);bad['commands'][keys[0]]['denominator']+=1
        rejects('invalid-partial-trace-'+str(desc.d),lambda:c.Description.from_dict(bad))
    require(modes=={'exact','positive-grid'},'both modes exercised')
    # Check the real compile CLI and deterministic single-outcome streaming CLI.
    inst=prep_instrument(2,3)
    target=ROOT/'inputs/rectangular-choi.json'
    require(c.Instrument.from_dict(json.loads(target.read_text())).to_dict()==inst.to_dict(),'committed rectangular input')
    proc=subprocess.run([sys.executable,str(ROOT/'choi_streaming.py'),'compile','--input',str(target),'--grid','4096'],capture_output=True,check=True,timeout=30)
    require(c.verify_compilation(inst,json.loads(proc.stdout)),'real compiler CLI')
    streamfile=ROOT/'inputs/choi-channel-stream.json'
    proc2=subprocess.run([sys.executable,str(ROOT/'choi_streaming.py'),'stream','--input',str(streamfile)],
                         input=b'8\n2\nxxxxxxxx\n',capture_output=True,check=True,timeout=30)
    lines=[json.loads(x) for x in proc2.stdout.splitlines()]
    require(len(lines)==9 and all(x['outcome']==0 for x in lines[:-1]),'immediate outputs CLI')
    for text in [b'1\n2\nxx\n',b'2\n1\nxx\n',b'2\n2\nx\n',b'2\n2\nxxx\n',b'2\n2\nx?\n']:
        p=subprocess.run([sys.executable,str(ROOT/'choi_streaming.py'),'stream','--input',str(streamfile)],input=text,capture_output=True,timeout=30)
        require(p.returncode==2,'malformed stream rejected');NEG.append('stream-input-'+hashlib.sha256(text).hexdigest()[:8])
    tokenraw=json.loads(streamfile.read_text());tokenraw['commands']={'command-001':tokenraw['commands']['x']}
    named=c.Description.from_dict(tokenraw)
    m=c.ChoiStreamer(named,2,2);m.step('command-001',lambda:0);m.step('command-001',lambda:0)
    require(m.finish()['dimension']==2,'unbounded command-identifier syntax at library interface')
    with tempfile.TemporaryDirectory(prefix='gtf66-token-test-') as tmp:
        tokenfile=Path(tmp)/'description.json';tokenfile.write_text(json.dumps(tokenraw))
        cmd=[sys.executable,str(ROOT/'choi_streaming.py'),'stream','--tokens','--input',str(tokenfile)]
        p=subprocess.run(cmd,input=b'2\n2\ncommand-001 command-001\n',capture_output=True,check=True,timeout=30)
        data=[json.loads(x) for x in p.stdout.splitlines()]
        require(len(data)==3 and data[0]['outcome']==0 and data[1]['outcome']==0,'multi-character actual CLI')
        require(data[-1]==m.finish(),'token CLI and integer recurrence agree')
        for token in [b'command-001-too-long',b'command-00?',b'command-\xff01']:
            p=subprocess.run(cmd,input=b'2\n2\n'+token+b'\n',capture_output=True,timeout=30)
            require(p.returncode==2,'invalid token rejected')
        NEG.append('malformed-token-stream')
    bad=copy.deepcopy(tokenraw);bad['commands']['command-001']['convention']='output-first'
    rejects('wrong-input-tensor-convention',lambda:c.Description.from_dict(bad))
    cap=desc.exact_cap(8)
    require(c.read_decimal_line(io.BytesIO(b'9'*10000+b'\n'),cap)==cap,'large precision saturated')
    return cases,hashlib.sha256(proc.stdout).hexdigest(),hashlib.sha256(proc2.stdout).hexdigest()

def main():
    comp=compilation_checks();alg=algebra_checks();ref=reference_checks();nh=numerical_history_checks();st,cc,sc=streaming_checks()
    print(json.dumps({'schema':'gtf66.regression/1','status':'success','exact_assertions':COUNT,
      'compilation_cases':comp,'algebraic_branch_cases':alg,'entangled_or_stopped_blocks':ref,
      'sampled_prefixes':st,'numerical_history_blocks':nh,'negative_controls':NEG,'compile_cli_sha256':cc,'stream_cli_sha256':sc,
      'floating_point_decisions':False,
      'scope':'Exact finite regression only. Not universal proof, formal bit-space verification, full Koopman certification, independent priority, or OS entropy certification.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
