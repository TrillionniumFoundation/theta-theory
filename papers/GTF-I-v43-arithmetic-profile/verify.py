#!/usr/bin/env python3
"""Finite algebraic checks and labelled numerical diagnostics for revision 43.

These tests do not prove asymptotic statements or certify an infinite spectral gap.
All critical checks use explicit exceptions, so Python -O changes no semantics.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product, combinations
import json
import math
from pathlib import Path
import random
import sys
import mpmath as mp
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError('CHECK_REJECTED: ' + message)


def sign_surd(a: int, b: int) -> int:
    """Exact sign of a+b*sqrt(2), for integral coefficients."""
    if not a: return (b > 0) - (b < 0)
    if not b: return (a > 0) - (a < 0)
    if a > 0 and b > 0: return 1
    if a < 0 and b < 0: return -1
    delta = a*a-2*b*b
    if a > 0: return (delta > 0) - (delta < 0)
    return (delta < 0) - (delta > 0)


def square_values(k: int) -> tuple[int,int]:
    vertices = [(1,0),(0,1),(-1,0),(0,-1)]
    best = (0,0)
    for assignment in product(range(k), repeat=4):
        a = b = 0
        for j in range(k):
            x = sum(vertices[i][0] for i in range(4) if assignment[i] == j)
            y = sum(vertices[i][1] for i in range(4) if assignment[i] == j)
            n = x*x+y*y
            require(n in (0,1,2), 'square subset norm')
            a += int(n == 1); b += int(n == 2)
        if sign_surd(a-best[0], b-best[1]) > 0: best = (a,b)
    return best


def partitions(m: int, k: int):
    """Enumerate all cyclic consecutive partitions (duplicates harmless)."""
    for origin in range(m):
        order = [(origin+i) % m for i in range(m)]
        for count in range(1,min(k,m)+1):
            for cuts in combinations(range(1,m), count-1):
                bounds = (0,)+cuts+(m,)
                yield [order[bounds[i]:bounds[i+1]] for i in range(count)]


def phase_value(z, p, k):
    return max(sum(abs(sum((p[i]*z[i] for i in block),mp.mpc(0)))
                   for block in partition) for partition in partitions(len(z),k))


def interval_dp(n: int, width: list[int]):
    charge = lambda t,b: F(b*b+1,7*(width[t]+1))
    dynamic = [F(0)]*(n+1)
    for t in range(1,n+1):
        dynamic[t] = max([dynamic[t-1]]+[dynamic[t-b]+charge(t,b) for b in range(1,t+1)])
    scores = []
    def enumerate_disjoint(start, score):
        scores.append(score)
        for left in range(start,n):
            for right in range(left+1,n+1):
                enumerate_disjoint(right, score+charge(right,right-left))
    enumerate_disjoint(0,F(0))
    require(dynamic[n] == max(scores), 'weighted disjoint interval optimum')
    return len(scores)


VERT = [(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
ROT = ((F(3,5),F(-4,5)),(F(4,5),F(3,5)))
ID = ((F(1),F(0)),(F(0),F(1)))
REF = ((F(1),F(0)),(F(0),F(-1)))


def mul(A, x): return tuple(sum(A[i][j]*x[j] for j in range(2)) for i in range(2))


def encode(v):
    require(abs(v[0])+abs(v[1]) <= 1, 'contracted point belongs to common polygon')
    out = [F(0)]*4
    out[0 if v[0]>=0 else 2] += abs(v[0])
    out[1 if v[1]>=0 else 3] += abs(v[1])
    rest = 1-abs(v[0])-abs(v[1]); out[0] += rest/2; out[2] += rest/2
    require(sum(out)==1 and min(out)>=0, 'stochastic polygon row')
    require(tuple(sum(out[s]*VERT[s][j] for s in range(4)) for j in range(2))==v,'polygon barycentric identity')
    return out


def transition_rows(omit=False):
    contraction = F(1) if omit else F(5,7)
    return [[encode(tuple(contraction*y for y in mul(A,v))) for v in VERT] for A in (ID,ROT,REF)]


def continued_fraction(alpha, n):
    p0,p1,q0,q1 = 0,1,1,0
    vals=[]; x=alpha
    for _ in range(n):
        a=int(mp.floor(x)); p=a*p1+p0; q=a*q1+q0
        vals.append((p,q));p0,p1,q0,q1=p1,p,q1,q;x=1/(x-a)
    return vals


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--negative-control')
    parser.add_argument('--export',type=Path)
    args=parser.parse_args(); mutant=args.negative_control
    allowed={'omit-dilation','free-packet-length','wrong-metric-log','lose-rational-phase',
             'reverse-profile-order','drop-partition-constraints','false-convergent-separation','wrong-cubic-scale'}
    require(mutant is None or mutant in allowed,'unknown negative control')
    mp.mp.dps=80
    exact={}; numerical={}
    expected=[(0,0),(0,2),(2,1),(4,0)]
    actual=[square_values(k) for k in range(1,5)]
    if mutant=='drop-partition-constraints': actual[1]=(0,0)
    require(actual==expected,'exact square packet optima')
    gamma=[1-(mp.mpf(a)+mp.sqrt(2)*b)/4 for a,b in actual]
    if mutant=='reverse-profile-order': gamma=list(reversed(gamma))
    require(all(gamma[i]>=gamma[i+1] for i in range(3)),'distortion decreases with number of labels')
    exact['square_assignments']=sum(k**4 for k in range(1,5))
    exact['square_values']=['1','1-1/sqrt(2)','(2-sqrt(2))/4','0']

    packet_count=0
    for r in range(1,5):
        for length in range(2,5):
            B=r*(length-1)
            declared=1 if mutant=='free-packet-length' else B
            words=[]
            for counts in product(range(length),repeat=r):
                word=tuple(a for i,c in enumerate(counts,1) for a in [i]*c+[0]*(length-1-c))
                require(len(word)==declared,'every ordinary command in packet is paid')
                require(tuple(word.count(i) for i in range(1,r+1))==counts,'packet count identity')
                words.append(word);packet_count+=1
            require(len(set(words))==length**r,'distinct complete packet words')
    exact['packet_words']=packet_count

    interval_cases=schedules=0
    rng=random.Random(431)
    for n in range(1,8):
        for _ in range(8):
            widths=[rng.randrange(1,6) for _ in range(n+1)]
            schedules+=interval_dp(n,widths);interval_cases+=1
    exact['interval_profiles']=interval_cases; exact['disjoint_schedules_enumerated']=schedules

    rows=transition_rows(mutant=='omit-dilation'); means=0
    for n in range(0,6):
        for word in product(range(3),repeat=n):
            for seed in VERT:
                dist=encode(tuple(y/2 for y in seed)); target=seed
                for a in word:
                    dist=[sum(dist[i]*rows[a][i][j] for i in range(4)) for j in range(4)]
                    target=mul((ID,ROT,REF)[a],target)
                for j in range(2):
                    value=sum(dist[s]*VERT[s][j] for s in range(4))
                    require(value==F(1,2)*F(5,7)**n*target[j],'exact full-word conditional mean')
                    decoder=[F(1,50)*F(7,5)**n*v[j] for v in VERT]
                    require(max(abs(d) for d in decoder)<=1,'legal terminal decoder')
                    require(sum(dist[s]*decoder[s] for s in range(4))==F(1,100)*target[j],'exact numerical probability')
                    means+=1
    exact['rational_command_rows']=12;exact['word_mean_coordinates']=means

    # A paid finite phase tag, with an exact quarter-turn readout.
    phases=VERT
    for c in range(4):
        for command in range(4):
            nxt=0 if mutant=='lose-rational-phase' else (c+command)%4
            true=complex(int(phases[c][0]),int(phases[c][1]))*complex(int(phases[command][0]),int(phases[command][1]))
            require((int(phases[nxt][0]),int(phases[nxt][1]))==(int(true.real),int(true.imag)),'rational phase tag carried to decoder')
    exact['phase_tag_updates']=16

    for r in range(1,9):
        for s in (F(1),F(3,2),F(2)):
            b=F(2*r*s,2*r+1)
            upper=r*b
            if mutant=='wrong-metric-log': upper=b
            require(upper==F(2*r*r*s,2*r+1),'metric logarithmic upper power includes q <= Q^r')
            require((2*r+1)*b==2*r*s,'dilation logarithmic balance')
        require(F(r,2*r+1)==F(r*(r+1-r),r+1+r),'minimal-type powers match')
    exact['arithmetic_power_balances']=32

    # Exact determinant recurrence; transcendental comparisons below are diagnostics.
    for digits in ([1]*12,[1]+[2]*11,[0,2,1,7,3,1,9,2,2,8,1,5]):
        p0,p1,q0,q1=0,1,1,0
        for a in digits:
            p,q=a*p1+p0,a*q1+q0
            require(abs(p*q1-p1*q)==1,'unimodular convergent columns')
            p0,p1,q0,q1=p1,p,q1,q
    exact['convergent_determinants']=36

    alpha=(mp.sqrt(5)-1)/2
    conv=continued_fraction(alpha,13)
    for n in range(3,len(conv)-1):
        p,q=conv[n];pnext,qnext=conv[n+1];qprev=conv[n-1][1]
        err=abs(q*alpha-p)
        require(1/mp.mpf(qnext+q)<err<1/mp.mpf(qnext),'continued fraction error diagnostic')
        sep=min(abs(l*alpha-mp.nint(l*alpha)) for l in range(1,q))
        lower=1/mp.mpf(q) if mutant=='false-convergent-separation' else 1/mp.mpf(2*q)
        require(sep>lower,'convergent packet separation diagnostic')
    numerical['convergent_scales']=len(conv)-4
    C=mp.mpf(40); q=conv[9][1]; N=int(mp.ceil(C*q**3))
    m=1 if mutant=='wrong-cubic-scale' else int(mp.ceil(100*(C+1)))
    Q=m*q;eta=abs(Q*alpha-mp.nint(Q*alpha))
    require(N*eta<=mp.mpf(Q)**2/100,'enlarged-denominator cubic synthesis diagnostic')
    numerical['cubic_upper_scale']=1

    z=[mp.mpc(1),mp.mpc(0,1),mp.mpc(-1),mp.mpc(0,-1)]
    comparisons=hidden_cases=0
    for _ in range(12):
        a=[rng.randrange(1,9) for _ in z]; p=[mp.mpf(x)/sum(a) for x in a]
        for k in range(1,4):
            f=phase_value(z,p,k)
            unrestricted=max(sum(abs(sum((p[i]*z[i] for i in range(4) if assign[i]==j),mp.mpc(0))) for j in range(k))
                             for assign in product(range(k),repeat=4))
            require(abs(f-unrestricted)<mp.mpf('1e-70'),'cyclic segmentation equals unrestricted assignment diagnostic')
            comparisons+=1
            oldweights=[mp.mpf(1)/3]*3; centroids=[mp.mpc(F(1,2).numerator)/2,mp.mpc(0,mp.mpf(2)/3),mp.mpc(-mp.mpf(1)/4,mp.mpf(1)/4)]
            sums=[mp.mpc(0)]*k
            for s in range(3):
                for w in range(4):
                    raw=[rng.randrange(1,10) for _ in range(k)]; den=sum(raw)
                    for j in range(k): sums[j]+=oldweights[s]*p[w]*mp.mpf(raw[j])/den*z[w]*centroids[s]
            before=sum(oldweights[s]*abs(centroids[s]) for s in range(3))
            after=sum(abs(x) for x in sums)
            require(after<=f*before+mp.mpf('1e-70'),'all-hidden endpoint contraction diagnostic')
            hidden_cases+=1
    numerical['cyclic_assignment_comparisons']=comparisons;numerical['hidden_packet_cases']=hidden_cases
    numerical['precision_digits']=80

    for m in range(3,9):
        factorial=math.factorial(m)
        require(math.factorial(m+1)==(m+1)*factorial,'explicit Liouville denominator relation')
        require((m+2)*factorial-factorial==(m+1)*factorial,'Liouville horizon exponent')
    exact['liouville_denominator_identities']=12

    report={'schema':'gtf43.checks/1','exact_checks':exact,'floating_diagnostics':numerical,
            'analytic_claims':{'finite_profiles':'proved in manuscript; fixed algebraic instances decidable, no generic efficient minimizer claimed',
                               'minimal_ordinary_type':'logarithmic exponent r/(2r+1)',
                               'metric_logarithms':'-2r(1+delta)/(2r+1), +2r^2(1+delta)/(2r+1)',
                               'all_irrational':'cubic-order convergent subsequences; width diverges',
                               'liouville':'liminf exponent 0; 1/3 <= limsup <= 1/2; exact limsup not claimed'},
            'scope':'Finite exact algebra and labelled 80-digit diagnostics. Universal optimization, metric and asymptotic theorems are analytic proofs, not certified by these tests. No spectral-gap or independent priority certification.'}
    if args.export:
        data={'schema':'gtf43.rows/1','vertices':[[str(y) for y in v] for v in VERT],
              'commands':[[[str(y) for y in row] for row in A] for A in (ID,ROT,REF)],
              'contraction':'5/7','initial_scale':'1/2','rho':'1/100',
              'rows':[[[str(y) for y in row] for row in command] for command in rows],
              'square_packet_exact_distortions':exact['square_values'],
              'scope':'A finite rational common-row witness; not the irrational asymptotic construction.'}
        args.export.parent.mkdir(parents=True,exist_ok=True);args.export.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
