#!/usr/bin/env python3
"""Finite exact regressions and separately labelled high-precision diagnostics.
Universal width bounds and external gaps are proved/cited in the article, not certified here.
"""
from __future__ import annotations
import argparse
import itertools as it
import json
import random
import sys
from pathlib import Path
import mpmath as mp
import sympy as sp

NEGATIVES=['one-step-is-expanding','drop-packet-commands','merge-packet-products',
           'free-query-norm','drop-copy-rank','unpaid-component','omit-polygon-dilation','duplicate-query-gain']

def check(ok:bool,msg:str)->None:
    if not bool(ok): raise RuntimeError('CHECK_REJECTED: '+msg)

def max_sign_quadratic(P:sp.Matrix)->sp.Expr:
    return max((sp.Matrix(s).T*P*sp.Matrix(s))[0] for s in it.product([-1,1],repeat=P.rows))

def main()->None:
    ap=argparse.ArgumentParser();ap.add_argument('--negative-control',choices=NEGATIVES);ap.add_argument('--export')
    args=ap.parse_args();mut=args.negative_control
    mp.mp.dps=80
    counts={};diags={};export={}
    a=sp.Matrix([[1,0,0],[0,sp.Rational(3,5),-sp.Rational(4,5)],[0,sp.Rational(4,5),sp.Rational(3,5)]])
    b=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5),0],[sp.Rational(4,5),sp.Rational(3,5),0],[0,0,1]])
    c=a.T*b*a;I=sp.eye(3);z=sp.Matrix([0,0,1])
    for M in [a,b,c,a*b]:check(M.T*M==I and M.det()==1,'rational rotation')
    for j in range(21):
        p=sp.Rational(j,20);P=a*((1-p)*I+p*b)
        claimed=sp.Rational(9,10) if mut=='one-step-is-expanding' else 1
        check((P*z).dot(P*z)==claimed,'one-step invariant vector has unit norm')
    U=[I,b,c,c*b];B=sum(U,sp.zeros(3))/4
    P=(a+a*b)/2
    check(P**2==a**2*B,'two-step word factorization')
    var=sum(((U[i]-U[j]).T*(U[i]-U[j]) for i in range(4) for j in range(i+1,4)),sp.zeros(3))/16
    check(I-B.T*B==var,'four-unitary variance identity')
    Q=(b+b.T+c+c.T)/4
    check(((I-b).T*(I-b)+(I-c).T*(I-c))/16==(I-Q)/4,'qualitative gap coefficient')
    counts['rational_rotation_identities']=8;counts['one_step_norm_witnesses']=21
    export['binary_SO3']={'a':a.tolist(),'b':b.tolist(),'c':c.tolist(),'external_gap':'qualitative Benoist-de Saxce; not tested'}

    signs=list(it.product([-1,1],repeat=6))
    P=sp.BlockMatrix([[I/2,I/2],[I/2,I/2]]).as_explicit()
    if mut=='drop-copy-rank':P=sp.eye(6)
    check(P**2==P and P.T==P and sp.trace(P)==3,'copy projection has rank three')
    maxB=max_sign_quadratic(P)
    Bused=1 if mut=='free-query-norm' else 6
    check(maxB==Bused,'query norm of a diagonal copy')
    x=sp.Matrix([1,0,0,1,0,0])/sp.sqrt(2);sig=sp.ones(6,1)
    groups=[]
    for perm in it.permutations(range(3)):
        for sg in it.product([-1,1],repeat=3):
            R=sp.zeros(3)
            for i,j in enumerate(perm):R[i,j]=sg[i]
            if R.det()==1:groups.append(sp.diag(R,R))
    check(len(groups)==24,'finite covariance-design count')
    def twirl(M):return sum((G*M*G.T for G in groups),sp.zeros(6))/24
    check(twirl(x*x.T)==twirl(sig*sig.T)/6,'exact dual calibration certificate')
    primal=P/6
    check((x.T*primal*x)[0]==sp.Rational(1,6) and max_sign_quadratic(primal)==1,'primal calibration witness')
    for d in range(2,9):check(max_sign_quadratic(sp.eye(d))==d,'standard coordinate query norm')
    multiplicity=0
    for u,v in it.product(range(-2,3),repeat=2):
        if not u and not v:continue
        aa=sp.Matrix([u,v])/sp.sqrt(u*u+v*v)
        PP=sp.kronecker_product(aa*aa.T,I)
        expected=3*(abs(u)+abs(v))**2/sp.Integer(u*u+v*v)
        check(max_sign_quadratic(PP)==expected,'real multiplicity sign norm');multiplicity+=1
    counts['multiplicity_sign_norm_cases']=multiplicity
    counts['calibration_sign_vectors']=len(signs);counts['dual_twirl_elements']=len(groups)
    export['calibration']={'copy_projection':P.tolist(),'primal':primal.tolist(),'dual_sign':list(sig),'dual_weight':'1/6','exact_c_squared':'1/6'}

    F=sp.Matrix([[1,0],[sp.Rational(3,5),sp.Rational(4,5)]])
    L=F.inv();Fd=sp.Matrix.vstack(F,F[0,:]);Ld=L.row_join(sp.zeros(2,1))
    beta2=max_sign_quadratic(L.T*L);betad2=max_sign_quadratic(Ld.T*Ld)
    claimed_dup=beta2/2 if mut=='duplicate-query-gain' else beta2
    check(Ld*Fd==sp.eye(2) and betad2==claimed_dup,'duplicated query cannot improve calibration')
    Fp=sp.Matrix([[1,0],[sp.Rational(1,10),sp.Rational(9,10)]])
    Lp=L-L*(Fp-F)*Fp.inv()
    check(Lp*Fp==sp.eye(2),'perturbed frame reconstruction identity')
    check(Lp==Fp.inv(),'unique square-frame solution')
    counts['frame_identities']=4
    export['frame']={'F':F.tolist(),'L':L.tolist(),'beta_squared':str(beta2)}

    packet_count=words_count=0
    for r in range(1,4):
        for k in range(1,9):
            LL=1
            while LL**r<2*k:LL+=1
            B=r*(LL-1)
            if mut=='drop-packet-commands' and r>1:B=LL-1
            count_vectors=[]
            for js in it.product(range(LL),repeat=r):
                word=tuple(a for i,J in enumerate(js,1) for a in ([i]*J+[0]*(LL-1-J)))
                check(len(word)==B,'all packet command slots are charged')
                cv=tuple(word.count(i) for i in range(1,r+1))
                check(cv==js,'packet count equals chosen coordinate vector')
                count_vectors.append((0,)*r if mut=='merge-packet-products' else cv);words_count+=1
            check(len(set(count_vectors))==LL**r and LL**r>=2*k,'packet products have distinct count vectors')
            packet_count+=1
    counts['packet_configurations']=packet_count;counts['packet_words']=words_count

    T=sp.Symbol('T');norms=0;separations=0
    for r in range(1,5):
        xi=mp.root(2,r+1);alph=[xi**i for i in range(1,r+1)];bb=mp.mpf(2)**r/mp.mpf(9)**r
        for m in it.product([-1,0,1],repeat=r):
            HH=sum(abs(x) for x in m)
            if HH==0:continue
            value=sum(mp.mpf(m[i])*alph[i] for i in range(r));m0=-int(mp.nint(value))
            poly=m0+sum(m[i]*T**(i+1) for i in range(r))
            resultant=sp.resultant(T**(r+1)-2,poly,T)
            check(resultant.is_Integer and abs(resultant)>=1,'nonzero integer algebraic norm');norms+=1
            check(abs(value+m0)>=bb/(mp.mpf(HH)**r),'finite algebraic-angle separation diagnostic');separations+=1
    counts['exact_nonzero_algebraic_norms']=norms;diags['algebraic_separation_cases']=separations
    denominator_cases=0
    for r in range(1,4):
        xi=mp.root(2,r+1);alpha=[xi**i for i in range(1,r+1)]
        bb=(mp.mpf(2)/9)**r;c0=(bb/r**(r+1))**r
        for QQ in range(2,10):
            qq=next(q for q in range(1,QQ**r+1) if max(abs(q*t-mp.nint(q*t)) for t in alpha)<1/mp.mpf(QQ))
            check(c0*QQ**r<=qq<=QQ**r,'comparable denominator diagnostic');denominator_cases+=1
    diags['simultaneous_denominator_cases']=denominator_cases

    # Explicit exact-geometry row formulas, evaluated at 80 digits; not rational proofs.
    row_cases=word_cases=0;examples=[];rng=random.Random(42027)
    for r,N,reflection in [(1,8,False),(2,8,False),(3,8,False),(2,8,True)]:
        xi=mp.root(2,r+1);alpha=[xi**i for i in range(1,r+1)]
        for q in range(4,300):
            deltas=[2*mp.pi*(t-mp.nint(q*t)/q) for t in alpha]
            lam=max([mp.mpf(1)]+[mp.cos(mp.pi/q-abs(d))/mp.cos(mp.pi/q) for d in deltas])
            if lam**N<=2:break
        else:raise RuntimeError('CHECK_REJECTED: diagnostic polygon search exhausted')
        if mut=='omit-polygon-dilation':lam=mp.mpf(1)
        verts=[mp.e**(2j*mp.pi*j/q) for j in range(q)]
        def weights(z):
            theta=mp.arg(z)%(2*mp.pi);idx=int(mp.floor(theta*q/(2*mp.pi)))%q
            step=2*mp.pi/q;d=theta-idx*step;rad=abs(z)
            w1=rad*mp.sin(step-d)/mp.sin(step);w2=rad*mp.sin(d)/mp.sin(step)
            rest=1-w1-w2
            check(rest>-mp.mpf('1e-65'),'rotated label lies in dilated polygon')
            row=[rest/q for _ in range(q)];row[idx]+=w1;row[(idx+1)%q]+=w2
            check(abs(sum(row)-1)<mp.mpf('1e-65'),'polygon row normalized')
            check(abs(sum(row[j]*verts[j] for j in range(q))-z)<mp.mpf('1e-65'),'polygon row barycenter')
            return row
        acts=[lambda z:z]+[(lambda z,t=t:z*mp.e**(2j*mp.pi*t)) for t in alpha]
        if reflection:acts.append(lambda z:mp.conj(z))
        rows=[[weights(act(z)/lam) for z in verts] for act in acts];row_cases+=q*len(acts)
        for _ in range(40):
            seed=rng.choice([1,-1,1j,-1j]);law=weights(mp.mpc(seed)/2);truth=mp.mpc(seed)
            word=[rng.randrange(len(acts)) for __ in range(N)]
            for command in word:
                law=[sum(law[j]*rows[command][j][l] for j in range(q)) for l in range(q)]
                truth=acts[command](truth)
            answer=sum(law[j]*verts[j] for j in range(q))*2*mp.mpf('0.1')*lam**N
            check(abs(answer-mp.mpf('0.1')*truth)<mp.mpf('1e-62'),'complete numerical response diagnostic');word_cases+=1
        examples.append({'r':r,'N':N,'reflection':reflection,'q':q,'Lambda_80_digit_diagnostic':mp.nstr(lam,75),
                         'row0_command1':[mp.nstr(z,75) for z in rows[1][0]],
                         'numeric_status':'80-digit evaluation of analytic formulas; not exact rational arithmetic'})
    diags['polygon_rows']=row_cases;diags['complete_word_responses']=word_cases;diags['precision_digits']=80
    export['polygon_examples']=examples

    rot=sp.Matrix([[0,-1],[1,0]]);flip=sp.diag(1,-1)
    reps=[sp.eye(2),flip]
    for command in [rot,flip]:
        for cidx,rc in enumerate(reps):
            prod=command*rc;cnext=0 if prod.det()==1 else 1;h=reps[cnext].T*prod
            check(h.det()==1 and reps[cnext]*h==prod,'finite-component cocycle')
    labels=[(c,s) for c in range(2) for s in range(4)]
    claimed=4 if mut=='unpaid-component' else 8
    check(len(labels)==claimed,'component label is charged')
    counts['coset_cocycle_identities']=4
    result={'schema':'gtf42.checks/1','exact_checks':counts,'floating_diagnostics':diags,
      'analytic_claims':{'nongapped_width':'Theta(N^(r/(2r+1))), dual badly approximable r-angle family',
        'all_finite_block_gaps':'zero in rotation/reflection hierarchy, proved analytically',
        'binary_rational_SO3':'g1*=0, g2*>0 conditional on external qualitative algebraic gap',
        'calibration':'finite projection optimization, SDP upper bound and frame stability',
        'generic_gap_decidability_claimed':False},
      'scope':'Finite exact identities and explicitly labelled numerical diagnostics. Not universal proof certification, an infinite spectral-gap computation, a full nonconvex optimizer, or priority clearance.'}
    if args.export:Path(args.export).write_text(json.dumps(export,indent=2,default=str,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
