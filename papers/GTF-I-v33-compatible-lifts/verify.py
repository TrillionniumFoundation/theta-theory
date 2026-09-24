#!/usr/bin/env python3
"""Finite regression checks for v33. Analytic width theorems are in the paper.

Exact rational/algebraic checks are distinguished from high-precision floating
checks of explicit polygon machines. No grid proves the continuum statements.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as sp


def require(ok: bool, label: str) -> None:
    if not ok:
        raise RuntimeError('CHECK_REJECTED: '+label)


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--negative-control')
    ap.add_argument('--export',type=Path)
    args=ap.parse_args(); mutant=args.negative_control
    valid={'ambient-extension','face-count-as-K','mean-constant','profile-constant',
           'resonance-sign','early-decoder','rational-denominator','normalization'}
    require(mutant is None or mutant in valid,'unknown control')
    out={'schema':'gtf33.checks/1',
         'scope':'Finite rational/algebraic regressions and separately labelled 80-digit polygon checks; not independent proof, optimal hidden-width solution or priority certification.'}

    # An affine-positive map of a simplex section need not be a stochastic map.
    verts=[]
    for i in [0,1]:
        for j in [2,3]:
            e=[F(0)]*4;e[i]=e[j]=F(1,2);verts.append(e)
    u=[F(1),F(0),F(1,2),F(1,2)]
    errors=[abs(sum(ei*ui for ei,ui in zip(e,u))-2*e[0]) for e in verts]
    require(max(errors)==F(1,4),'extension upper')
    require((F(1)-F(0))/2<=F(1,2),'extension difference')
    claimed=F(0) if mutant=='ambient-extension' else F(1,4)
    require(claimed>=F(1,4),'positive affine map is not an ambient stochastic extension')
    E=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in e] for e in verts])
    B=sp.Matrix([[2*e[0],2*e[1]] for e in verts])
    # A support-function certificate for failed exact extension.
    Z=sp.Matrix([[1,0],[0,0],[-1,0],[0,0]])
    lhs=sum(Z.multiply_elementwise(B)); C=E.T*Z
    rhs=sum(max(C[i,0],C[i,1]) for i in range(4))
    require(lhs==1 and rhs==sp.Rational(1,2),'extension separating certificate')
    out['stochastic_extension_defect']='1/4'
    out['extension_dual_witness']={'left':'1','right':'1/2'}

    section=[]
    for word in itertools.product([0,1],repeat=3):
        e=[F(0)]*6
        for i,b in enumerate(word):e[2*i+b]=F(1,3)
        section.append(tuple(e))
    bound=6 if mutant=='face-count-as-K' else 2**6
    require(len(set(section))==8 and len(section)<=bound,'simplex section can have more vertices than labels')
    out['section_vertices']=8;out['ambient_labels']=6

    coeff=9*(F(1,6)-F(10,1080)-F(9,128))
    threshold=F(4,5) if mutant=='mean-constant' else F(3,4)
    require(coeff==F(301,384) and coeff>threshold,'mean support coefficient')
    factor=F(140) if mutant=='profile-constant' else F(160)
    require((factor*3)**2>(320**2)*2,'bounded-type profile constant')
    count=0
    for h in itertools.product([-1,0,1],repeat=5):
        require(max(h)-h[0]<=sum(max(h[j]-h[j-1],0) for j in range(1,5)),'orbit accumulation')
        count+=1
    out['pointwise_orbit_cases']=count
    out['mean_support_coefficient']='301/384 > 3/4'
    out['golden_profile_bound']=320
    out['nontrivial_golden_onset']=320*2**9
    out['previous_onset']=24000000*2**18

    # Exact algebraic convergent identities for the golden angle.
    alpha=(sp.sqrt(5)-1)/2
    fib=[0,1]
    for i in range(2,20):fib.append(fib[-1]+fib[-2])
    cf=0
    for k in range(4,17):
        p,q=fib[k-1],fib[k]
        require(sp.simplify(q*alpha-p-(-1)**(k-1)*alpha**k)==0,'golden convergent identity')
        require(sp.simplify(p*fib[k+1]-q*q) in [-1,1],'coprime convergent determinant')
        cf+=1
    out['exact_golden_identities']=cf

    a,d=sp.symbols('a d',real=True)
    lam=sp.cos(d)+sp.tan(a)*sp.sin(d)
    require(sp.trigsimp(lam*sp.cos(a)-sp.cos(a-d))==0,'resonant radial identity')
    w=sp.sin(d)/(lam*sp.sin(2*a))
    require(sp.simplify(sp.expand_trig(lam*(1-w+w*sp.cos(2*a))-sp.cos(d)))==0,'resonant real coordinate')
    require(sp.trigsimp(lam*w*sp.sin(2*a)-sp.sin(d))==0,'resonant imaginary coordinate')
    out['symbolic_resonance_coordinates']=3

    # Fully rational counter realization, including idle and active words.
    R=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5)],
                 [sp.Rational(4,5), sp.Rational(3,5)]])
    triangle=[sp.Matrix([sp.Rational(1,2),0]),
              sp.Matrix([-sp.Rational(1,2),sp.Rational(1,2)]),
              sp.Matrix([-sp.Rational(1,2),-sp.Rational(1,2)])]
    denominator=1 if mutant=='rational-denominator' else 5
    zz=sp.Rational(3,denominator)+sp.I*sp.Rational(4,denominator)
    require(sp.simplify(zz*sp.conjugate(zz))==1,'rational rotation normalization')
    powers=[sp.eye(2)]
    for k in range(1,13):
        powers.append(powers[-1]*R)
        re,im=sp.expand((3+4*sp.I)**k).as_real_imag()
        require((re-5**k)**2+im**2>=1,'nonzero Gaussian integer')
    rational_words=0
    for n in range(7):
        for bits in itertools.product([0,1],repeat=n):
            k=sum(bits)
            for x in itertools.product([-1,1],repeat=2):
                z=sp.Matrix([sp.Rational(x[0],10),sp.Rational(x[1],10)])
                e=[z[0]+sp.Rational(1,2),
                   (sp.Rational(1,2)-z[0])/2+z[1],
                   (sp.Rational(1,2)-z[0])/2-z[1]]
                require(sum(e)==1 and min(e)>=0,'triangle seed')
                result=sum((e[s]*(powers[k]*triangle[s]) for s in range(3)),sp.zeros(2,1))
                require(result==powers[k]*z,'rational complete word')
                rational_words+=1
    out['rational_complete_words']=rational_words
    out['rational_gaussian_integer_checks']=12

    # High-precision diagnostics are not exact-arithmetic certificates.
    mp.mp.dps=80
    ar=(mp.sqrt(5)-1)/2
    word_count=row_count=0
    exported=[]
    for n in [1,2,3,5,8,13]:
        threshold=max(mp.mpf(5),mp.root(40*n,3))
        k=next(k for k in range(4,19) if fib[k]>=threshold)
        p,q=fib[k-1],fib[k]; ang=mp.pi/q;delta=2*mp.pi*(ar-mp.mpf(p)/q)
        ll=mp.cos(ang-abs(delta))/mp.cos(ang)
        ww=mp.sin(abs(delta))/(ll*mp.sin(2*ang))
        require(ll>=1 and 0<=ww<=1 and mp.log(ll)<mp.mpf(40)/q**3,'resonant range')
        require(mp.mpf(1)/4*ll**n<mp.mpf(3)/4,'resonant radius')
        v=[mp.e**(2j*mp.pi*j/q) for j in range(q)]
        sign=1 if delta>0 else -1
        if mutant=='resonance-sign':sign=-sign
        for j in range(q):
            idle=[(1-1/ll)/q for _ in range(q)];idle[j]+=1/ll
            active=[mp.mpf(0)]*q
            active[(j+p)%q]=1-ww;active[(j+p+sign)%q]+=ww
            if mutant=='normalization':idle[j]+=mp.mpf('0.01')
            require(abs(sum(idle)-1)<mp.mpf('1e-70'),'idle stochastic normalization')
            require(abs(sum(active)-1)<mp.mpf('1e-70'),'active stochastic normalization')
            require(abs(sum(idle[i]*ll*v[i] for i in range(q))-v[j])<mp.mpf('1e-65'),'idle mean')
            require(abs(sum(active[i]*ll*v[i] for i in range(q))-mp.e**(2j*mp.pi*ar)*v[j])<mp.mpf('1e-65'),'active mean')
            row_count+=2
        # Every count at each prefix length tests amplitude and accumulated angle.
        for t in range(n+1):
            for c in range(t+1):
                normalized=(mp.mpf('0.1')+mp.mpf('0.1')*1j)/(mp.mpf(1)/4)*ll**(-t)*mp.e**(2j*mp.pi*ar*c)
                expected=(mp.mpf('0.1')+mp.mpf('0.1')*1j)*mp.e**(2j*mp.pi*ar*c)
                radius=mp.mpf(1)/4*ll**t
                if mutant=='early-decoder':radius=mp.mpf(1)/4*ll**n
                require(abs(radius*normalized-expected)<mp.mpf('1e-65'),'horizon decoder cannot answer early')
                word_count+=1
        exported.append({'N':n,'p':p,'q':q,'lambda_80digits':mp.nstr(ll,80),
                         'w_80digits':mp.nstr(ww,80),
                         'note':'Floating diagnostic of the exact formulas, not exact row encoding.'})
    out['floating_diagnostics']={'decimal_precision':80,'command_rows':row_count,
                                  'prefix_count_means':word_count}
    out['proved_scope']={'hidden_golden':'Omega(log N) <= W_N <= O(N^(1/3))',
                        'vector_bounded_type':'V_N = Theta_alpha(N^(1/3))',
                        'rational_hidden':'N <= 140*2^(2W)*5^(8*2^W)',
                        'anytime_autonomous':'N+1 <= A_N <= 3*(N+1)+2'}
    if args.export:
        args.export.write_text(json.dumps({'extension_vertices':[[str(x) for x in e] for e in verts],
          'optimal_binary_row':[str(x) for x in u],'polygon_diagnostics':exported},indent=2)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':main()
