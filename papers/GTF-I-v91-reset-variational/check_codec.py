#!/usr/bin/env python3
"""Exact finite regression; not universal proof, priority or spectral certification."""
from __future__ import annotations
import copy
from fractions import Fraction as F
from itertools import product
from math import comb, isqrt
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import tempfile
import sympy as sp
import instrument_codec as c
import choi_streaming as old
import instrument_streaming as arithmetic
import check_choi as inherited

ROOT=Path(__file__).resolve().parent
COUNT=0
NEG=[]

def require(ok:bool, message:str):
    global COUNT
    COUNT+=1
    if not ok:
        raise RuntimeError(message)

def rejects(name, fn):
    try:
        fn()
    except (ValueError,TypeError,KeyError,IndexError):
        NEG.append(name)
    else:
        raise RuntimeError('negative control escaped: '+name)

def f2(a,b):
    return sum((F(x,a.denominator)-F(y,b.denominator))**2
        for aa,bb in zip(a.outcomes,b.outcomes)
        for ar,br in zip(aa,bb) for az,bz in zip(ar,br) for x,y in zip(az,bz))

def scalar_mixture(a,b,num,den):
    require(a.d==b.d and a.n==b.n and len(a.outcomes)==len(b.outcomes),'mixture shape')
    mats=[]
    for x,y in zip(a.outcomes,b.outcomes):
        mats.append([[tuple(num*b.denominator*xc+(den-num)*a.denominator*yc
                          for xc,yc in zip(xz,yz)) for xz,yz in zip(xr,yr)]
                     for xr,yr in zip(x,y)])
    ans=old.Instrument(a.d,a.n,den*a.denominator*b.denominator,mats);ans.validate();return ans

def centre(d,n,m):
    return old.Instrument(d,n,m*n,[old.identity(d*n) for _ in range(m)])

def code_cases():
    examples=[inherited.prep_instrument(d,n) for d,n in [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,2)]]
    examples += [centre(d,n,m) for d,n,m in [(1,1,1),(3,1,1),(2,2,1),(2,3,2),(3,2,3)]]
    for file in sorted((ROOT/'inputs').glob('*-instrument.json')):
        examples += list(inherited.from_kraus(arithmetic.Specification.read(file)).commands.values())
    cases=0
    for inst in examples:
        d,n,m=inst.d,inst.n,len(inst.outcomes)
        for ay in sorted({0,m-1}):
            for ao in sorted({0,n-1}):
                coords=list(c.coordinates(d,n,m,ay,ao))
                require(len(coords)==c.intrinsic_dimension(d,n,m),'intrinsic affine count')
                require(len(coords)==len(set(coords)),'no duplicated coordinate')
                for B in [1,7,64,4096]:
                    cert=c.encode(inst,B,ay,ao);got=c.decode(cert)
                    require(c.verify(inst,cert),'target-bound exact certificate')
                    require(got.denominator==B+m*n*old.constants(d,n,m)[0],'common denominator')
                    ds=c.unpack_digits(int(cert['payload_hex'],16),B,len(coords))
                    require(c.pack_digits(ds,B)==int(cert['payload_hex'],16),'mixed-radix round trip')
                    raw=c.fill_affine(ds,d,n,m,B,ay,ao)
                    marginal=old.zero(d)
                    for block in raw:
                        marginal=old.plus(marginal,old.partial_trace(block,d,n))
                    require(marginal==old.identity(d,B),'exact unbuffered marginal')
                    for y,mat in enumerate(raw):
                        require(mat==old.adjoint(mat),'unbuffered Hermitian')
                        for u in range(d*n):
                            for v in range(d*n):
                                for comp in [0,1]:
                                    er=abs(F(mat[u][v][comp],B)-F(inst.outcomes[y][u][v][comp],inst.denominator))
                                    omitted=(y==ay and u%n==ao and v%n==ao)
                                    require(er<=F(max(1,m*n-1) if omitted else 1,B),'coordinate reconstruction error')
                    upper=F(0)
                    for x,y in zip(inst.outcomes,got.outcomes):
                        upper += inherited.norm_upper(x,F(1,inst.denominator),y,F(1,got.denominator))
                    # A direct Frobenius enclosure of the final difference can be
                    # too loose for low-rank targets. Independently enclose the
                    # exact affine-error/buffer decomposition as well.
                    upper=min(upper,inherited.choi_difference_upper(inst,got,B))
                    require(upper<=F(cert['diamond_error_upper']),'independent block trace enclosure')
                    require(f2(inst,got)<=F(cert['diamond_error_upper'])**2,'tuple-Frobenius error')
                    for mat in got.outcomes:
                        require(old.rational_psd(mat),'exact CP')
                        require(all(x*x+y*y<=got.denominator**2 for row in mat for x,y in row),'Gaussian entry modulus bound')
                    cases+=1
        if any(all(z==old.ZERO for row in mat for z in row) for mat in inst.outcomes):
            cert=c.encode(inst,128,preserve_zeros=True);got=c.decode(cert)
            active=cert['active_outcomes'];require(len(active)<m,'zero mask reduces count')
            require(cert['intrinsic_dimension']==d*d*(len(active)*n*n-1),'zero face dimension')
            require(all(got.outcomes[y]==old.zero(d*n) for y in range(m) if y not in active),'zeros restored exactly')
    for d in range(1,7):
        cert=c.encode(centre(d,1,1),11)
        require(cert['fixed_length_payload_bits']==0 and cert['payload_hex']=='0','singleton zero-bit code')
        require(c.decode(cert).outcomes[0]==old.identity(d,c.decode(cert).denominator),'singleton trace channel')
    return cases

def negative_cases():
    inst=inherited.prep_instrument(2,2);good=c.encode(inst,128)
    for name,key,value in [('dimension','intrinsic_dimension',0),('bits','fixed_length_payload_bits',0),
        ('bound','diamond_error_upper','0'),('convention','convention','output-first'),
        ('negative-payload','payload_hex','-1'),('noncanonical-payload','payload_hex','00'),
        ('overlong-payload','payload_hex','f'*10000),('bool-grid','grid',True),
        ('zero-grid','grid',0),('bad-anchor','anchor_output',2),
        ('duplicate-mask','active_outcomes',[0,0,2]),('unordered-mask','active_outcomes',[1,0,2]),
        ('empty-mask','active_outcomes',[])]:
        bad=copy.deepcopy(good);bad[key]=value
        rejects('reject-'+name,lambda b=bad:c.decode(b))
        require(not c.verify(inst,bad),'tampered target verification '+name)
    rejects('out-of-alphabet',lambda:c.unpack_digits(5**4,2,4))
    rejects('out-of-range-digit',lambda:c.pack_digits([3],2))
    rejects('wrong-digit-count',lambda:c.fill_affine([],2,2,1,2))
    # Legal affine constraints alone do not guarantee CP; a malicious in-range
    # digit word with a large grid defeats a fixed buffer and must be rejected.
    B=100000;coords=list(c.coordinates(2,2,1));ds=[B]*len(coords)
    rejects('affine-word-not-CP',lambda:c.decode_digits(ds,2,2,1,B))
    # Removing a nonzero outcome cannot certify the original target.
    bad=copy.deepcopy(good);bad['active_outcomes']=[0];bad['preserve_zeros']=True
    require(not c.verify(inst,bad),'false zero mask rejected');NEG.append('false-zero-mask')
    pure=inherited.prep_instrument(2,2)
    require(not c.has_margin(pure,F(1,100)),'rank-deficient target not interior')
    rejects('false-margin',lambda:c.encode_adaptive(pure,10,F(1,100),F(1,4)))
    rejects('zero-margin',lambda:c.adaptive_grid(2,2,1,10,F(0),F(1,4)))
    rejects('empty-interior',lambda:c.adaptive_grid(2,2,1,10,F(1,2),F(1,4)))
    rejects('supercritical-tolerance',lambda:c.adaptive_grid(2,2,1,10,F(1,4),F(1)))
    rejects('zero-horizon',lambda:c.adaptive_grid(2,2,1,0,F(1,4),F(1,4)))

def programme_cases():
    # These diagonal instruments give rational endpoints, mixture weights and
    # exact product distances. No sampled or floating-point decisions are used.
    cases=0
    for d,n,m in [(1,1,2),(1,2,1),(2,2,2),(2,3,2)]:
        mid=centre(d,n,m)
        dim=d*n; lam=F(1,2*m*n)
        U=[old.zero(dim) for _ in range(m)]
        if n>1:
            U[0][0][0]=(F(3,5),F(0));U[0][1][1]=(F(-3,5),F(0))
            # Norm need not be one: rational bound ||U||F<=1 is sufficient
            # for the tested mixture and its conservative estimate.
        else:
            U[0][0][0]=(F(3,5),F(0));U[1][0][0]=(F(-3,5),F(0))
        def endpoints(sign):
            mats=[[[tuple(F(z,mid.denominator)+sign*lam*u for z,u in zip(zz,uu))
                    for zz,uu in zip(zr,ur)] for zr,ur in zip(zm,um)] for zm,um in zip(mid.outcomes,U)]
            require(all(old.rational_psd(mat) for mat in mats),'common programme vertices legal')
            marginal=old.zero(d)
            for mat in mats:marginal=old.plus(marginal,old.partial_trace(mat,d,n))
            require(marginal==old.identity(d),'programme joint TP')
            return mats
        kp,km=endpoints(1),endpoints(-1)
        for ratio in [F(0),F(1,16),F(1,4),F(1)]:
            p=F(1,2)+ratio/4;q=F(1,2)-ratio/4
            require(q>=F(1,4),'classical weight floor')
            chi=(p-q)**2/q+(p-q)**2/(1-q)
            require(chi<=2*ratio**2,'two-point relative entropy upper proxy')
            # Mixture difference is ratio*lambda*U, with no index transpose.
            for yp,ym,uu in zip(kp,km,U):
                for rp,rm,ru in zip(yp,ym,uu):
                    for xp,xm,xu in zip(rp,rm,ru):
                        for vp,vm,vu in zip(xp,xm,xu):
                            require((p-q)*(vp-vm)==ratio*lam*vu,'exact two-vertex mixture difference')
            for N in [1,2,5,12,32]:
                tv=sum(F(comb(N,j))*abs(p**j*(1-p)**(N-j)-q**j*(1-q)**(N-j)) for j in range(N+1))/2
                require((2*tv)**2<=4*N*ratio**2,'exact product TV obeys root-N envelope')
                require((2*tv)<=2,'unhalved trace convention')
                cases+=1
    # Factor two cannot be discarded: for disjoint classical laws trace norm=2.
    require(sum(abs(x-y) for x,y in zip([F(1),F(0)],[F(0),F(1)]))==2,'TV versus block trace')
    NEG.append('TV-is-half-block-trace')
    return cases

def adaptive_cases():
    cases=0
    for d,n,m in [(1,2,2),(2,2,1),(2,3,2),(3,2,2)]:
        pure=inherited.prep_instrument(d,n)
        # A direct strictly positive central perturbation by a diagonal tangent.
        target=centre(d,n,m)
        # Put all entries over a common denominator and perturb in one block.
        mat=copy.deepcopy(target.outcomes)
        mat=[[[tuple(8*x for x in z) for z in row] for row in a] for a in mat]
        mat[0][0][0]=old.add(mat[0][0][0],(1,0));mat[0][1][1]=old.add(mat[0][1][1],(-1,0))
        target=old.Instrument(d,n,8*m*n,mat);target.validate();a=F(1,2*m*n)
        require(c.has_margin(target,a),'certified input Choi margin')
        for N in [1,2,9,100,10000]:
            for delta in [F(1,4),F(1,2)]:
                cert=c.encode_adaptive(target,N,a,delta);out=c.decode(cert['code'])
                B=cert['code']['grid'];K=old.constants(d,n,m)[1]
                require(c.has_margin(out,a/2),'decoded margin at least half')
                require(F(K,B)<=a/2,'root-N local applicability')
                require(16*N*F(K,B)**2<=a*a*delta*delta,'exact adaptive error budget')
                require(16*N*f2(target,out)<=a*a*delta*delta,'independent tuple error budget')
                cases+=1
        # Dyadic horizons make ceil(sqrt N) exact. Constants aside, payload
        # grows with half the logarithm of the horizon, not the whole log.
        grids=[c.adaptive_grid(d,n,m,4**j,a,F(1,4)) for j in range(1,9)]
        require(all(grids[j+1]<=2*grids[j] for j in range(len(grids)-1)),'grid scales as square root')
    # Rational boundary unitary U_N=((N^2-1)+2Ni)/(N^2+1) gives finite
    # exact tests against any naive N-independent root-N Lipschitz proxy.
    for N in [8,32,128]:
        z=(N*N-1,2*N);den=N*N+1
        w=(1,0)
        for _ in range(N):w=old.mul(w,z)
        wden=den**N
        # Trace distance squared after N uses on |+> equals |1-U_N^N|^2.
        trace2=F((wden-w[0])**2+w[1]**2,wden*wden)
        choif2=F(8,N*N+1)  # 2sqrt2 sin(theta/2) squared.
        require(trace2>2,'rational boundary remains distinguishable')
        require(choif2*N<F(8,N),'one-use root-N input tends to zero')
    NEG.append('no-uniform-rootN-continuity-on-unitary-boundary')
    return cases

def schur_cases():
    rng=random.Random(6703);cases=0
    for q in range(2,7):
        for sample in range(3):
            X=sp.Matrix(q,q,lambda i,j:sp.Integer(rng.randrange(-3,4))+sp.I*rng.randrange(-2,3))
            A=(X*X.conjugate().T+sp.eye(q)).applyfunc(sp.expand)
            state=A.copy()
            for k in range(q):
                I=list(range(k));principal=A.extract(I,I).det() if I else sp.Integer(1)
                for i in range(k,q):
                    for j in range(k,q):
                        bordered=sp.expand(A.extract(I+[i],I+[j]).det(method="domain-ge"))
                        require(sp.cancel(state[i-k,j-k]-bordered/principal)==0,'ordered bordered-minor Schur identity')
                        for part in [sp.re(bordered),sp.im(bordered)]:
                            require(part.is_Integer is True,'Gaussian-integer bordered determinant')
                        cases+=1
                if state.rows>1:
                    state=state[1:,1:]-state[1:,0]*state[0,1:]/state[0,0]
                    state=state.applyfunc(sp.cancel)
    # Zero-pivot test: valid zero row skips without a permutation; an off-diagonal
    # nonzero at a zero diagonal is incompatible with positive semidefiniteness.
    z=old.identity(4);z[0][0]=(0,0)
    require(old.rational_psd(z),'leading zero row valid')
    z[0][1]=(0,1);z[1][0]=(0,-1)
    require(not old.rational_psd(z),'zero row obstruction')
    NEG.append('zero-pivot-nonzero-row-no-permutation-fix')
    return cases

def cli_cases():
    with tempfile.TemporaryDirectory(prefix='gtf67-codec-') as td:
        path=Path(td)/'target.json';target=centre(2,2,2)
        path.write_text(json.dumps(target.to_dict()))
        first=subprocess.run([sys.executable,str(ROOT/'instrument_codec.py'),'encode','--input',str(path),'--grid','128'],capture_output=True,check=True)
        cert=Path(td)/'code.json';cert.write_bytes(first.stdout)
        dec=subprocess.run([sys.executable,str(ROOT/'instrument_codec.py'),'decode','--input',str(cert)],capture_output=True,check=True)
        old.Instrument.from_dict(json.loads(dec.stdout))
        ver=subprocess.run([sys.executable,str(ROOT/'instrument_codec.py'),'verify','--input',str(path),'--certificate',str(cert)],capture_output=True,check=True)
        require(json.loads(ver.stdout)['verified'],'CLI target-bound verification')
        return hashlib.sha256(first.stdout).hexdigest()

def main():
    cases=code_cases();negative_cases();programmes=programme_cases();adaptive=adaptive_cases();schur=schur_cases();cli=cli_cases()
    print(json.dumps({'schema':'gtf67.codec-regression/1','status':'success',
        'exact_assertions':COUNT,'codec_cases':cases,'programme_product_cases':programmes,
        'adaptive_grid_cases':adaptive,'bordered_minor_cases':schur,'negative_controls':NEG,
        'cli_code_sha256':cli,'floating_point_decisions':False,
        'scope':'Finite exact arithmetic, input rejection, CP/TP repair, code round trips, programme identities, product tests and Schur minors. Not a universal proof, formal complexity certificate, independent priority clearance or physical simulation.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
