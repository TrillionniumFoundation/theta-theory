#!/usr/bin/env python3
"""Rational outward certificates for all-history bounds and the marked two-state ROC.
No floating special function or empirical simulation certifies these intervals.
The original normal-interval primitive is credited in interval_normal.py.
"""
from __future__ import annotations
import argparse,json
from fractions import Fraction as F
from pathlib import Path
from interval_normal import I,B,normal_tail,ceildiv

Q=F(1,4);MU=F(1);KAPPA=F(1)
def demand(ok,msg):
    if not ok:raise RuntimeError(msg)
def times(a,b):
    a=I.lift(a);b=I.lift(b);D=a+b+2*KAPPA*a*b
    return (2+KAPPA*(a+b))/D,(a-b)/D

def qprofile(t:F):
    t=F(t);demand(t>=1,'profile domain')
    if t==1:
        return normal_tail(MU),F(0),F(0)
    lo=F(0);hi=F(6)
    def mass(h):return normal_tail(h-MU)+normal_tail(h+MU)
    demand(mass(lo).lo*t>B and mass(hi).hi*t<B,'profile bracket')
    for _ in range(50):
        mid=(lo+hi)/2;v=mass(mid)*t
        if v.lo>=B:lo=mid
        elif v.hi<=B:hi=mid
        else:raise RuntimeError('profile bisection undecided')
    a=t*normal_tail(hi+MU);b=t*normal_tail(lo+MU)
    return I(a.lo,b.hi),lo,hi

def two_state(beta:F,N:F):
    beta=F(beta);N=F(N);demand(N>=1 and 0<=beta<=1,'two-state domain')
    if N==1:return {'kind':'first-call','optimum':I.q(1).strings(),'feasible_risk':I.q(1).strings(),'feasible_mean':I.q(1).strings(),'decoder':'0'}
    end=2/beta+KAPPA if beta else None
    if end is not None and N>=end:
        return {'kind':'positive-revelation','optimum':I.q(0).strings(),'feasible_risk':I.q(0).strings(),'feasible_mean':I.q(end).strings(),'decoder':'1'}
    # The negative atom is partially accepted before all Gaussian reports matter.
    sw=F(2+KAPPA*(2-beta),2-beta+2*KAPPA*(1-beta))
    if beta and N<=sw:
        b=(2+KAPPA-N)/(N*(1+2*KAPPA)-KAPPA)
        T,m=times(1,b);r=m.midpoint();risk=1-m.square();feas=1-2*r*m+r*r
        demand(1-beta<=b<=1,'atomic routing probability')
        return {'kind':'negative-revelation-randomization','negative_reveal_accept':str((b-1+beta)/beta),'optimum':risk.strings(),'feasible_risk':feas.strings(),'feasible_mean':T.strings(),'decoder':str(r)}
    def curve(h):return times(beta+(1-beta)*normal_tail(h-MU),(1-beta)*normal_tail(h+MU))
    lo=F(-6);hi=F(6)
    demand(curve(lo)[0].hi<=N*B<=curve(hi)[0].lo,'two-state initial bracket')
    for _ in range(50):
        mid=(lo+hi)/2;t,_=curve(mid)
        if t.hi<=N*B:lo=mid
        elif t.lo>=N*B:hi=mid
        else:raise RuntimeError('two-state bisection undecided')
    tl,ml=curve(lo);th,mh=curve(hi)
    demand(tl.hi<=N*B<=th.lo,'two-state final feasibility')
    r=ml.midpoint();risk=I((1-mh.square()).lo,(1-ml.square()).hi);feas=1-2*r*ml+r*r
    return {'kind':'positive-reveal-and-Gaussian-tail','h_bracket':[str(lo),str(hi)],'optimum':risk.strings(),'feasible_risk':feas.strings(),'feasible_mean':tl.strings(),'decoder':str(r)}

def run():
    rows=[]
    for beta,N in [(F(0),F(n)) for n in (2,4,8,32)]+[(F(1,4),F(n)) for n in (2,3,4,8,9)]+[(F(1),F(n)) for n in (1,2,3)]:
        r=max(F(0),1-beta*N)
        if r==0:
            low=I.q(0);upper=I.q(0);mean=I.q(1/beta);threshold=None
        else:
            t=N*(1-beta)/r
            prof,lo,hi=qprofile(t)
            lowerprof,*_=qprofile(2*(1-Q)*t)
            low=4*Q*r*lowerprof
            ap=normal_tail(lo-MU);am=normal_tail(lo+MU)
            hazard=beta+(1-beta)*(ap+am)
            mean=1/hazard;upper=4*(1-beta)*am/hazard
            demand(mean.hi<=N*B+10**15,'outward feasible upper mean')
            # tiny tolerance above is only fixed-point enclosure at exact N=1;
            # all nonzero bisection thresholds certify <=N with no tolerance.
            if t>1:demand(mean.hi<=N*B,'strictly certified feasible threshold')
            threshold=str(lo)
        two=two_state(beta,N)
        demand(low.lo>=0 and upper.lo>=0,'risk positivity')
        demand(low.hi<=upper.lo or upper.hi==0,'lower/upper ordering')
        rows.append({'beta':str(beta),'N':str(N),'unrevealed_mass_lower':str(r),'all_history_lower_function':low.strings(),'three_state_feasible_risk':upper.strings(),'three_state_mean':mean.strings(),'three_state_threshold':threshold,'two_state':two})
    return {'status':'PASS','q':str(Q),'mu':str(MU),'method':'72-decimal outward integer intervals, 240-term normal series with rigorous remainder, 50 rational bisections','rows':rows,'scope':'all-history lower function; actual three-state construction upper; exact all-program two-state optimum enclosure. No exact all-history finite-budget optimum is asserted.'}

def display(v,d=6):
    a,b=map(F,v);s=10**d
    lo=a.numerator*s//a.denominator;hi=ceildiv(b.numerator*s,b.denominator)
    def fmt(z):
        sign='-' if z<0 else '';z=abs(z);return f'{sign}{z//s}.{z%s:0{d}d}'
    out=f'[{fmt(lo)}, {fmt(hi)}]';l,u=map(F,out[1:-1].split(','))
    demand(l<=a<=b<=u,'display is not outward')
    return out

def table(data):
    lines=[r'\begin{center}',r'\small',r'\begin{tabular}{@{}rrlll@{}}',r'\toprule',r'$\beta$ & $N$ & all-history lower & three-state upper & two-state optimum \\',r'\midrule']
    for r in data['rows']:
        lines.append('$'+r['beta']+'$ & '+r['N']+' & $'+display(r['all_history_lower_function'])+'$ & $'+display(r['three_state_feasible_risk'])+'$ & $'+display(r['two_state']['optimum'])+r'$ \\')
    lines +=[r'\bottomrule',r'\end{tabular}',r'\end{center}',r'Here $q=1/4$ and $\mu=1$. The lower and upper columns enclose the explicitly proved bound functions, not the unknown exact checkpoint optimum. Every upper uses a certified feasible rational threshold or an exact finite revealing-symbol rule. The two-state column encloses the exact optimum proved in Theorem~\ref{thm:two-state}.']
    return '\n'.join(lines)+'\n'
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();root=Path(__file__).resolve().parent
    data=run();text=table(data)
    if args.write:
        (root/'GAUSSIAN_CERTIFICATE.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n');(root/'sections/gaussian-table.tex').write_text(text)
    else:
        demand(json.loads((root/'GAUSSIAN_CERTIFICATE.json').read_text())==data,'certificate JSON mismatch');demand((root/'sections/gaussian-table.tex').read_text()==text,'certificate table mismatch')
    print(json.dumps(data,sort_keys=True,indent=2))
