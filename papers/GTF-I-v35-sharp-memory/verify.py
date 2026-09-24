#!/usr/bin/env python3
"""Exact finite identities and separately labelled 80-digit diagnostics for v35.
The arbitrary-horizon theorems are analytic results in the article, not inferred
from these checks. All rejection guards survive Python -O.
"""
from __future__ import annotations
import argparse
import itertools as it
import json
import math
import random
import sys
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
import mpmath as mp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError('CHECK_REJECTED: '+message)


def greedy(ends: list[int], B: int) -> list[int]:
    chosen=[]
    for t in ends:
        if t>=B and (not chosen or t-chosen[-1]>=B): chosen.append(t)
    return chosen


def interval_dp(widths: list[int], weights: dict[int,F]) -> F:
    f=[F(0)]
    for t,k in enumerate(widths,1):
        b=2*k-1
        f.append(max(f[-1],f[t-b]+weights[b]) if b<=t else f[-1])
    return f[-1]


def packet_rows(k: int) -> list[list[int]]:
    B=2*k-1
    return [[1]*j+[0]*(B-j) for j in range(B+1)]


def negative(name: str) -> None:
    if name=='free-packet-time':
        k=5; require(1==len(packet_rows(k)[0]),'a packet still consumes 2k-1 elementary commands')
    elif name=='dependent-fresh-packet':
        # Y is uniform +/-1, S is constant, G=Y. Then E[Y|S]=0 but GY=1.
        require(F(1)<=F(0),'fresh packet independence cannot be removed: G=Y recovers amplitude')
    elif name=='wrong-terminal-factor':
        require(F(1,10)-F(1,100)==F(1,10)-2*F(1,100),'binary TV changes mean by twice the error')
    elif name=='interval-double-count':
        iv=[(0,3),(1,4)]
        require(all(b<=c or d<=a for i,(a,b) in enumerate(iv) for c,d in iv[i+1:]),'overlapping packets cannot be multiplied')
    elif name=='omit-starting-direction':
        # Rotation around z has an invariant z direction: no universal Haar loss on all R^3 directions.
        require(F(1,4)<=F(0),'an invariant representation direction makes orbit distortion zero')
    elif name=='linear-angular':
        x=mp.mpf('0.00001');l=6
        ratio=abs(mp.cos(l*x)-mp.cos(x))/(1-mp.cos(x))
        require(ratio<=l,'universal homogeneous angular coefficient has quadratic order')
    elif name=='local-equals-final':
        # Two flips cancel exactly; the two local TV errors against the identity are each one.
        require(F(2)==F(0),'accumulated local certificate is not actual final error')
    elif name=='omit-output-direction':
        # Two opposite incoming centroids assigned to one state have zero, not unit, final amplitude.
        require(abs((1+(-1))/2)==1,'one endpoint state cannot retain two independently chosen centroid directions')
    else: raise ValueError('Unknown negative control: '+name)


def check(export: Path|None=None) -> dict:
    rng=random.Random(351903);mp.mp.dps=80
    counts={'packet_words':0,'interval_selections':0,'weighted_interval_cases':0,
            'exact_fourier_coefficients':0,'angular_polynomial_identities':0}
    for k in range(1,33):
        rows=packet_rows(k);B=2*k-1
        require(len(rows)==2*k and all(len(w)==B for w in rows),'packet dimensions')
        require([sum(w) for w in rows]==list(range(B+1)),'uniform count support')
        counts['packet_words']+=len(rows)
    for n in range(1,10):
        for mask in range(1<<n):
            ends=[i+1 for i in range(n) if mask>>i&1]
            for B in [1,3,5,7]:
                chosen=greedy(ends,B)
                require(len(ends)<=B-1+B*len(chosen),'greedy coverage')
                require(all(v-u>=B for u,v in zip(chosen,chosen[1:])),'greedy disjointness')
                counts['interval_selections']+=1
    weights={b:F(1,b*b+1) for b in [1,3,5,7,9]}
    for n in range(1,10):
        for _ in range(12):
            ks=[rng.randrange(1,6) for _ in range(n)]
            intervals=[(t-(2*k-1),t,weights[2*k-1]) for t,k in enumerate(ks,1) if 2*k-1<=t]
            best=F(0)
            for mask in range(1<<len(intervals)):
                taken=[v for i,v in enumerate(intervals) if mask>>i&1]
                if all(b<=c or d<=a for i,(a,b,_) in enumerate(taken) for c,d,_ in taken[i+1:]):
                    best=max(best,sum((w for a,b,w in taken),F(0)))
            require(interval_dp(ks,weights)==best,'weighted interval recurrence')
            counts['weighted_interval_cases']+=1
    u=sp.Symbol('u')
    for l in range(1,25):
        r=u**l-1-l*(u-1)-(u-1)*sum(u**j-1 for j in range(l))
        require(sp.expand(r)==0,'angular remainder identity')
        require(l*(l-1)+(l-1)==l*l-1,'angular coefficient')
        counts['angular_polynomial_identities']+=1
    require(sum(F(83,36)**j/math.factorial(j) for j in range(14))>10,'golden logarithm constant')
    a=(sp.sqrt(5)-1)/2;ap=-(sp.sqrt(5)+1)/2
    for l in range(1,41):
        p=int(mp.nint(l*(mp.sqrt(5)-1)/2))
        require(sp.expand((l*a-p)*(l*ap-p))==p*p+l*p-l*l,'golden quadratic norm')
        require(p*p+l*p-l*l!=0,'golden nonzero integer')
    # Matrix-product Fourier coefficients on a two-state arbitrary stochastic program.
    p=sp.Matrix([[sp.Rational(2,5),sp.Rational(3,5)]])
    d=sp.Matrix([sp.Rational(1,3),sp.Rational(-2,7)])
    matrices=[]
    for t in range(5):
        matrices.append([sp.Matrix([[sp.Rational(t+1,t+3),sp.Rational(2,t+3)],
                                   [sp.Rational(c+1,c+t+4),sp.Rational(t+3,c+t+4)]]) for c in range(2)])
    # Correct normalization of second row depends on c; use its complement directly.
    for t in range(5):
        for c in range(2): matrices[t][c][1,1]=1-matrices[t][c][1,0]
    for n in range(1,6):
        vals={}
        for w in it.product(range(2),repeat=n):
            e=p
            for t,c in enumerate(w): e=e*matrices[t][c]
            vals[w]=(e*d)[0]
        for mask in range(1<<n):
            v=sum(val*(-1)**sum(w[t] for t in range(n) if mask>>t&1) for w,val in vals.items())/2**n
            e=p
            for t in range(n): e=e*(matrices[t][0]+(-1)**((mask>>t)&1)*matrices[t][1])/2
            require(sp.simplify(v-(e*d)[0])==0,'branching-program Fourier product')
            counts['exact_fourier_coefficients']+=1
    diagnostics={'decimal_precision':80,'random_hidden_packet_cases':0,
                 'golden_separation_cases':0,'resonant_rows':0,'angular_sharpness_cases':0}
    # Hidden-packet checks include nontrivial hidden past distributions, not just vector-state starts.
    zeta=mp.mpc(3,4)/5
    for k in range(1,7):
        m=2*k;rot=[zeta**j for j in range(m)]
        sigma2=min(abs(v-w)**2 for i,v in enumerate(rot) for w in rot[i+1:])
        loss=sigma2/16
        for _ in range(30):
            joint=[[F(rng.randrange(1,10)) for s in range(4)] for y in range(5)]
            total=sum(map(sum,joint),F(0));joint=[[v/total for v in r] for r in joint]
            to_mp=lambda f:mp.mpf(f.numerator)/f.denominator
            zs=[sum(to_mp(joint[y][s])*zeta**(y*y+1) for y in range(5)) for s in range(4)]
            q0=sum(abs(z) for z in zs)
            bs=[mp.mpc(0) for _ in range(k)]
            for s in range(4):
                for j in range(m):
                    row=[rng.randrange(1,10) for _ in range(k)];den=sum(row)
                    for r in range(k):bs[r]+=zs[s]*rot[j]*mp.mpf(row[r])/(den*m)
            q1=sum(abs(z) for z in bs)
            require(q1<=(1-loss)*q0+mp.mpf('1e-65'),'all-hidden packet loss')
            diagnostics['random_hidden_packet_cases']+=1
    alpha=(mp.sqrt(5)-1)/2
    for k in range(1,101):
        B=2*k-1;s=min(abs(l*alpha-mp.nint(l*alpha)) for l in range(1,B+1))
        require(s>=1/(mp.mpf(3)*B)-mp.mpf('1e-70'),'golden separation')
        require(mp.sin(mp.pi*s/2)**2>=s*s-mp.mpf('1e-70'),'circle chord loss')
        diagnostics['golden_separation_cases']+=1
    for l in range(2,17):
        t=mp.mpf('1e-12');ratio=abs(mp.cos(l*t)-mp.cos(t))/(1-mp.cos(t))
        require(abs(ratio-(l*l-1))<mp.mpf('1e-18'),'angular sharp limiting coefficient')
        diagnostics['angular_sharpness_cases']+=1
    # Resonant upper construction checked in 80 digits, distinctly not exact algebra.
    for p0,q in [(3,5),(5,8),(8,13),(13,21),(21,34)]:
        delta=2*mp.pi*(alpha-mp.mpf(p0)/q);aa=mp.pi/q
        lam=mp.cos(aa-abs(delta))/mp.cos(aa)
        w=mp.sin(abs(delta))/(lam*mp.sin(2*aa))
        require(0<=w<=1 and lam>=1,'resonant stochastic row')
        require(mp.log(lam)<mp.mpf(40)/q**3,'resonant radial bound')
        for s in range(q):
            vv=lambda j:mp.e**(2j*mp.pi*j/q)
            actual=lam*((1-w)*vv(s+p0)+w*vv(s+p0+int(mp.sign(delta))))
            require(abs(actual-mp.e**(2j*mp.pi*alpha)*vv(s))<mp.mpf('1e-65'),'resonant mean')
            diagnostics['resonant_rows']+=1
    result={'schema':'gtf35.checks/1','exact_counts':counts,'floating_diagnostics':diagnostics,
      'proved_claims':{'badly_approximable_hidden_width':'Theta_(alpha,epsilon)(N^(1/3)), 0<=epsilon<1/20',
      'finite_packet_bound':'floor(N/(2K-1))*s_(2K-1)^2 <= log(1/kappa)',
      'golden_exact_lower':'W > (N/168)^(1/3), W>=3',
      'nonuniform_occupation':'count<=2k-2+8*b^(-2)*k^3*log(1/kappa)',
      'orthogonal_group_budget':'sum Gamma_k(mu)<=log(1/kappa)',
      'compact_SO_d_width':'Theta_(d,epsilon)(N^((d-1)/2)) in separate compact-input model',
      'angular_sharp_coefficient':'l^2-1'},
      'scope':'Finite algebra and labelled numerical diagnostics; analytic proofs establish universal claims. No independent proof or priority certification.'}
    if export:
        export.parent.mkdir(parents=True,exist_ok=True)
        export.write_text(json.dumps({'k':3,'actual_packet_length':5,'words':packet_rows(3),
          'count_probabilities':['1/6']*6,'independence':'between packets, not between commands in a packet',
          'golden_rational_lower_constant':'1/168','diagnostics':diagnostics},indent=2)+'\n')
    return result


def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--negative-control');p.add_argument('--export',type=Path)
    a=p.parse_args()
    if a.negative_control:
        mp.mp.dps=80;negative(a.negative_control)
        raise RuntimeError('Negative control unexpectedly survived')
    print(json.dumps(check(a.export),indent=2,sort_keys=True))

if __name__=='__main__':
    try: main()
    except (ValueError,RuntimeError) as e:
        print(str(e),file=sys.stderr);sys.exit(1)
