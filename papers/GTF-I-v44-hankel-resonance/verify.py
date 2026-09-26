#!/usr/bin/env python3
"""Exact finite regressions for v44. These are not universal proof certificates."""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import random
import sys
import sympy as s
from finite_bit import DyadicRotationMachine, Interval, pi_interval, sincos, root_floor

MUTANTS=['reverse-hankel-update','drop-normalization','reverse-rate-bound','omit-rounding-cost',
         'free-random-scratch','reuse-random-word','drop-minimum-branch','reverse-interval-rounding']

def check(ok, message):
    if not ok: raise ValueError('CHECK_REJECTED: '+message)

def inside(i, value):
    value=Q(value)
    return Q(i.lo,1<<i.bits)<=value<=Q(i.hi,1<<i.bits)

def run(mutant=None):
    counts={'hankel_cuts':0,'factor_entries':0,'interval_operations':0,'root_bounds':0,
            'dyadic_rows':0,'decoder_weights':0,'exact_word_responses':0,'coin_draws':0,
            'exponent_cases':0,'rounding_cases':0}
    rho=s.Rational(1,10)
    A=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
    seeds=[s.Matrix([1,0]),s.Matrix([0,1]),s.Matrix([-1,0]),s.Matrix([0,-1])]
    # Rational triangle larger than the equilateral one used in the analytic proof.
    vertices=[s.Matrix([-3*rho,-3*rho]),s.Matrix([3*rho,-3*rho]),s.Matrix([0,3*rho])]
    V=s.Matrix.hstack(*[v.col_join(s.Matrix([1])) for v in vertices])
    for N in range(5):
        for t in range(N+1):
            prefixes=[rho*(A**j)*x for j in range(t+1) for x in seeds]
            suffixes=[A**j for j in range(N-t+1)]
            B=s.Matrix([[ (1+bb*(U*v)[j])/2 for U in suffixes for j in range(2) for bb in [-1,1]] for v in vertices])
            E=s.Matrix([(V.inv()*v.col_join(s.Matrix([1]))).T.tolist()[0] for v in prefixes])
            H=s.Matrix([[(1+bb*(U*v)[j])/2 for U in suffixes for j in range(2) for bb in [-1,1]] for v in prefixes])
            check(H.rank()==3,'rank-three prefix/suffix witness')
            check(all(x>=0 for x in E) and all(x>=0 for x in B),'factor positivity')
            check(all(sum(E.row(i))==1 for i in range(E.rows)),'initial factor normalization')
            if mutant=='drop-normalization': B[0,0]+=s.Rational(1,10)
            check(all(B[i,j]+B[i,j+1]==1 for i in range(B.rows) for j in range(0,B.cols,2)),'binary continuation normalization')
            check(E*B==H,'normalized positive factorization')
            counts['hankel_cuts']+=1;counts['factor_entries']+=len(E)+len(B)
    # Noncommuting controlled suffix order, independent of the planar rank witness.
    R=s.Matrix([[1,0,0],[0,0,-1],[0,1,0]]);S=s.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
    x=s.Matrix([1,2,3]);expected=S*R*x
    actual=R*S*x if mutant=='reverse-hankel-update' else S*R*x
    check(actual==expected,'command-prefix order in suffix restriction')
    # Exact one-dimensional dual witness, including both normalized coordinates.
    c=s.Matrix([1,0]);ends=[s.Matrix([0,1]),s.Matrix([s.Rational(1,4),s.Rational(3,4)])]
    z=s.Matrix([1,0]); dual=(z.dot(c)-max(z.dot(v) for v in ends))
    check(dual==s.Rational(3,4) and max(abs(x) for x in c-ends[1])==dual,'Hankel extension primal/dual witness')
    # A triangle and a quarter turn: lambda=2 is feasible; the four-phase k=3 rate is smaller.
    gamma=(2-s.sqrt(2))/4
    check(gamma>0 and 1-gamma>=s.Rational(1,8),'three-letter repeat comparison lambda^(-3)<=1-Gamma')
    if mutant=='reverse-rate-bound': check(1-gamma<=s.Rational(1,8),'reversed distortion/dilation direction')
    for r in range(1,9):
        for h in [s.Rational(1,100),s.Rational(1,2*r-1),s.Rational(2),s.Rational(5)]:
            upper=r*(1+h)/(2*r+1+h); sharp=min(s.Rational(1,2),upper)
            check(sharp<=upper,'a weaker upper bound still follows from a minimum')
            check((upper<=s.Rational(1,2))==(h*(2*r-1)<=1),'exact minimum branch cutoff')
            if mutant=='drop-minimum-branch' and upper>s.Rational(1,2):
                check(sharp==upper,'loss of the sharper minimum branch')
            counts['exponent_cases']+=1
    # Directed interval arithmetic, with exact rational oracle values.
    for a,b in itertools.product([Q(-7,11),Q(-1,3),Q(0),Q(2,7),Q(19,13)],repeat=2):
        ia,ib=Interval.fraction(a,64),Interval.fraction(b,64)
        for interval,value in [(ia+ib,a+b),(ia-ib,a-b),(ia*ib,a*b)]:
            check(inside(interval,value),'directed interval operation');counts['interval_operations']+=1
        if b>0:
            check(inside(ia/ib,a/b),'directed interval division');counts['interval_operations']+=1
    if mutant=='reverse-interval-rounding':
        check(inside(Interval(1,1,2),Q(1,3)),'inward rounding omitted the true value')
    pi=pi_interval(160)
    # Machin enclosure is checked against two rational 60-digit pi brackets.
    # Use a direct 50-decimal bracket, sufficient for the 160-bit interval.
    pilo=Q('3.14159265358979323846264338327950288419716939937510')
    pihi=Q('3.14159265358979323846264338327950288419716939937511')
    check(Q(pi.lo,pi.scale)<=pihi and Q(pi.hi,pi.scale)>=pilo,'Machin pi enclosure agrees with rational bracket')
    for angle,sv,cv in [(Q(0),0,1),(Q(1,4),1,0),(Q(1,2),0,-1),(Q(3,4),-1,0)]:
        sn,cs=sincos(2*pi*angle)
        check(inside(sn,sv) and inside(cs,cv),'Taylor interval at exact quarter circle')
    for degree in range(2,6):
        for rad in range(2,6):
            for b in [8,31,65]:
                m=root_floor(degree,rad,b)
                check(m**degree<=rad*(1<<(b*degree))<(m+1)**degree,'exact algebraic digit bisection');counts['root_bounds']+=1
    for n in [1,2,7,29,1001]:
        for b in [4,8,16]:
            p=[Q(1,3),Q(1,7),Q(11,21)];den=1<<b
            r=[Q(int(p[0]*den),den),Q(int(p[1]*den),den)];r.append(1-sum(r))
            tv=sum(abs(a-bb) for a,bb in zip(p,r))/2
            bound=Q(0) if mutant=='omit-rounding-cost' else Q(2,den)
            check(tv<=bound,'dyadic row error is charged');counts['rounding_cases']+=1
    exports=[]
    class CountBits(random.Random):
        def __init__(self):super().__init__(731);self.calls=[]
        def getrandbits(self,n):self.calls.append(n);return super().getrandbits(n)
    for n,r in [(1,1),(2,1),(3,1),(2,2),(7,2),(16,3)]:
        m=DyadicRotationMachine(n,r,Q(1,1000));den=1<<m.b
        check(m.error_bound<m.epsilon,'total certified wordwise error')
        check(len(m.commands)==r+1 and len(m.initial)==4,'no stored per-label transition table')
        for j in range(m.q+1):
            for command in range(r+1):
                row=m.row(j,command)
                check(all(0<=state<=m.q and w>=0 for state,w in row) and sum(w for _,w in row)==den,'exact dyadic stochastic row')
                counts['dyadic_rows']+=1
        dec=[[m.positive_answer_weight(j,a) for a in range(2)] for j in range(m.q+1)]
        check(all(0<=w<=den for row in dec for w in row),'bounded rounded decoder');counts['decoder_weights']+=2*(m.q+1)
        rng=CountBits();m.sample((j%(r+1) for j in range(n)),2,1,rng)
        expected=n+1 if mutant=='reuse-random-word' else n+2
        check(rng.calls==[m.b]*expected,'fresh fixed-length random words including deterministic cases');counts['coin_draws']+=len(rng.calls)
        if mutant=='free-random-scratch':check(m.b==0,'random sampling word requires charged work bits')
        # Exact rational whole-word probabilities; reference truth enclosed by integer interval trigonometry.
        if n<=3:
            bits=160;ppi=pi_interval(bits);scale=1<<bits
            roots=[0]+[root_floor(r+1,1<<i,bits)%scale for i in range(1,r+1)]
            for word in itertools.product(range(r+1),repeat=n):
                for seed in range(4):
                    dist={}
                    for st,w in m.initialization(seed):dist[st]=dist.get(st,Q(0))+Q(w,den)
                    for command in word:
                        nxt={}
                        for st,pr in dist.items():
                            for st2,w in m.row(st,command):nxt[st2]=nxt.get(st2,Q(0))+pr*Q(w,den)
                        dist=nxt
                    check(sum(dist.values())==1,'exact propagated probability mass')
                    angle=Q(seed,4)+sum((Q(roots[c],scale) for c in word),Q(0));angle-=angle.numerator//angle.denominator
                    ai=Interval.fraction(angle,bits).widen_units(n+1)
                    sn,cs=sincos(2*ppi*ai)
                    for query,trig in enumerate([cs,sn]):
                        true=(1+m.rho*trig)/2
                        actual=sum(pr*Q(dec[st][query],den) for st,pr in dist.items())
                        check(max(abs(actual-Q(true.lo,scale)),abs(actual-Q(true.hi,scale)))<m.epsilon,'exact word response versus interval-certified target')
                        counts['exact_word_responses']+=1
        exports.append(m.certificate())
    result={'schema':'gtf44.checks/1','exact_checks':counts,
      'analytic_claims':{'universal_comparison':'sup_B -log(1-Gamma(k,B))/B <= log(lambda(k,a))',
       'separate_planar_ranks':[3,3,3], 'finite_bit_compiler':'uniform wordwise epsilon; no per-label table; fixed number of fair bits',
       'space_scope':'Theta(log N) for explicit alphabets; clean label exponent is not whole-machine configuration exponent',
       'referee_minimum':'retain sharper minimum; old weaker inequality was still logically implied'},
      'scope':'Exact finite rational/algebraic and directed-integer-interval regressions. No universal proof, spectral-gap computation, asymptotic optimization or independent priority certification.'}
    return result,exports

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--negative-control',choices=MUTANTS);ap.add_argument('--export',type=Path)
    args=ap.parse_args()
    try:result,export=run(args.negative_control)
    except ValueError as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
    if args.negative_control:
        print('MUTANT_NOT_DETECTED',file=sys.stderr);sys.exit(0)
    if args.export:args.export.write_text(json.dumps({'compiler_certificates':export,'note':result['scope']},indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
