#!/usr/bin/env python3
"""Exact, independent diagnostics for the pinned A1 v32 referee assessment.

Run with Python 3, normally or under -O. No dependencies, network, or assertions.
These finite diagnostics are not a verification of the whole manuscript.
"""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path

COMMIT = 'e712437fe13cf29978715d3f16d825eadb450fea'
PROOF_BLOB = 'db8ae28cff76c143b709dabb8d68e64516c7f6b7'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def likelihood(theta, command, report):
    p = {(0, 0): F(1, 4), (0, 1): F(1, 3),
         (1, 0): F(2, 3), (1, 1): F(3, 4)}[theta, command]
    return p if report else 1-p


def action(stage, state, command):
    p = (F(1, 3), F(3, 4))[state] if stage != 2 else (F(0), F(2, 5))[state]
    return p if command else 1-p


def update(stage, state, command, report, new_state):
    p = F(1 + ((stage + 2*state + command + 3*report) % 6), 7)
    return p if new_state else 1-p


def history_likelihood(theta, history):
    out = F(1)
    for c, x in history:
        out *= likelihood(theta, c, x)
    return out


def check_compatibility():
    prior = (F(1, 3), F(2, 3))
    alpha = {((), 0): F(1), ((), 1): F(0)}
    joint = {(theta, (), i): prior[theta] if i == 0 else F(0)
             for theta in range(2) for i in range(2)}
    tested = 0
    zero_histories = 0
    for stage in range(1, 4):
        histories = sorted({h for h, i in alpha})
        next_alpha = {}
        for h in histories:
            evidence = sum(prior[z]*history_likelihood(z, h) for z in range(2))
            for c, x, j in product(range(2), repeat=3):
                r = sum(prior[z]*history_likelihood(z, h)*likelihood(z,c,x)
                        for z in range(2))/evidence
                next_alpha[h+((c,x),), j] = r*sum(
                    alpha[h,i]*action(stage,i,c)*update(stage,i,c,x,j)
                    for i in range(2))
        next_joint = {}
        for (z,h,i), mass in joint.items():
            for c,x,j in product(range(2), repeat=3):
                key = (z,h+((c,x),),j)
                next_joint[key] = next_joint.get(key,F(0))+mass*action(stage,i,c)*likelihood(z,c,x)*update(stage,i,c,x,j)
        for (h,j), mass in next_alpha.items():
            direct = sum(next_joint.get((z,h,j),F(0)) for z in range(2))
            require(mass == direct, 'Compatibility recurrence disagrees with direct latent-state enumeration')
            evidence = sum(prior[z]*history_likelihood(z,h) for z in range(2))
            for z in range(2):
                require(next_joint.get((z,h,j),F(0))*evidence == mass*prior[z]*history_likelihood(z,h),
                        'Conditional latent-state factorization failed')
            tested += 1
        require(sum(next_alpha.values()) == 1, 'Occupancy normalization failed')
        zero_histories += sum(sum(next_alpha[h,j] for j in range(2)) == 0
                              for h in {h for h,j in next_alpha})
        alpha,joint=next_alpha,next_joint
    return {'stages':3,'states':2,'commands':2,'reports':2,
            'history_state_equalities':tested,'zero_mass_history_occurrences':zero_histories,
            'result':'PASS'}


def pmul(a,b):
    out={}
    for x,v in a.items():
        for y,w in b.items():
            out[x+y]=out.get(x+y,F(0))+v*w
    return {x:v for x,v in out.items() if v}


def padd(*items):
    out={}
    for p in items:
        for x,v in p.items(): out[x]=out.get(x,F(0))+v
    return {x:v for x,v in out.items() if v}


def scale(p,c): return {x:v*c for x,v in p.items() if v*c}
def moment(p): return sum((v/(1+x) for x,v in p.items()),F(0))


def factors(a,g):
    eps=F(1,24)
    k=[{F(0):F(1,3),a[0]:eps}, {F(0):F(1,3),a[1]:eps},
       {F(0):F(1,3),a[0]:-eps,a[1]:-eps}]
    return [scale(k[j],g[j]) for j in range(3)]+[padd(*(scale(k[j],1-g[j]) for j in range(3)))]


def check_perturbation():
    calibrations=[(F(1),F(199,100)),(F(1),F(2)),(F(1),F(201,100)),
                  (F(1),F(3)),(F(2),F(3))]
    g=(F(1,3),F(1,2),F(2,3));delta=F(1,60);kappa=F(1,16)
    gp=(g[0]+delta,g[1]-delta,g[2]+delta)
    tested=0; max_ratio=F(0)
    for a in calibrations:
        fs,ft=factors(a,g),factors(a,gp)
        future=factors(a,(F(3,8),F(5,8),F(1,2)))[3]
        H=pmul(future,future)
        for stage in range(1,4):
            for reports in product(range(4),repeat=stage):
                p={F(0):F(1)};q=dict(p)
                for x in reports: p,q=pmul(p,fs[x]),pmul(q,ft[x])
                require(moment(p)>=kappa**stage and moment(q)>=kappa**stage,
                        'Evidence lower bound failed')
                ep,eq=moment(pmul(p,H))/moment(p),moment(pmul(q,H))/moment(q)
                require(0<=ep<=1 and 0<=eq<=1,'Target outside unit interval')
                ratio=abs(ep-eq)/(stage*delta/kappa)
                require(ratio<=1,'Positive likelihood target perturbation bound failed')
                max_ratio=max(max_ratio,ratio);tested+=1
    return {'prior':'uniform [0,1]; integrals of rational-exponent monomials evaluated exactly',
            'calibrations':[[str(x) for x in a] for a in calibrations],
            'delta':str(delta),'kappa':str(kappa),'comparisons':tested,
            'max_error_over_printed_bound':str(max_ratio),'result':'PASS'}


def partition_stats():
    words=list(product((-1,1),repeat=4)) # X1,U1,X2,U2
    stats=[];n=0;sums=[0]*4;old=0
    # Fix the first word outside label 1; complements then need not be repeated.
    for k in range(1,1<<15):
        gray=k^(k>>1);bit=(gray^old).bit_length()-1
        sign=1 if (gray>>bit)&1 else -1;n+=sign
        for j in range(4): sums[j]+=sign*words[bit+1][j]
        stats.append((n,*sums));old=gray
    return stats


def check_delayed():
    stats=partition_stats();results=[]
    ratios=[F(0),F(1,8),F(1,5),F(2,9),F(1,4),F(1,3),F(1,2)]
    for r in ratios:
        # Work in gamma^2 units; r=0 is a boundary diagnostic, not the printed e>0 domain.
        max_min=F(0);max_sum=F(0)
        for n,x1,u1,x2,u2 in stats:
            v1=x1+r*u1;v2=x2+r*u2;den=n*(16-n)
            max_min=max(max_min,min(v1*v1,v2*v2)/den)
            max_sum=max(max_sum,(v1*v1+v2*v2)/den)
        formula=max(F(1,3),(2+r)**2/15)
        require(max_min==formula,'Printed early-law value disagrees with exhaustive deterministic optimum')
        tails=[2+2*r,4+2*r,6+2*r,F(8),8+2*r,8+4*r,8+4*r,8+4*r]
        tail_max=max(A*A/(4*n*(16-n)) for n,A in enumerate(tails,1))
        require(tail_max==formula,'Upper-tail endpoint formula disagrees')
        require(max_sum==1,'Sampled seeded symmetry benchmark disagrees')
        current=max(F(1),(1+r)**2/3)
        require(current==1,'Just-in-time scalar quantizer failed')
        results.append({'e_over_gamma':str(r),'early_risk_over_gamma_squared':str(1+r*r-formula),
                        'jit_risk_over_gamma_squared':str(r*r),
                        'best_sum_explained_over_gamma_squared':str(max_sum)})
    return {'unordered_deterministic_partitions_per_ratio':len(stats)+1,
            'constant_encoder_included':True,'ratios':results,
            'scope':'Finite exhaustive checks plus algebraic tail endpoints; all-stochastic and all-parameter proof reviewed analytically, not supplied by these samples.',
            'result':'PASS'}


def check_rounding():
    rows=[(F(1,3),F(2,5),F(4,15)),(F(1,17),F(6,17),F(10,17)),(F(0),F(1),F(0))]
    tested=0
    for b in (1,2,7,19):
        for row in rows:
            q=[F((p*b).numerator//(p*b).denominator,b) for p in row[:-1]]
            q.append(1-sum(q));tv=sum(abs(x-y) for x,y in zip(row,q))/2
            require(sum(q)==1 and min(q)>=0,'Rounded row is not stochastic')
            require(tv<=F(len(row)-1,b),'Row total variation bound failed')
            tested+=1
    return {'row_checks':tested,'result':'PASS'}


def main():
    result={'reviewed_commit':COMMIT,'new_results_git_blob':PROOF_BLOB,
            'independent_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'arithmetic':'fractions.Fraction; explicit exceptions; no assert-dependent checks',
            'compatibility':check_compatibility(),'perturbation':check_perturbation(),
            'delayed':check_delayed(),'rounding':check_rounding(),
            'limitations':['No full native manuscript/companion build.',
                           'No formal verification of the continuum theorems.',
                           'No enumeration of the general M-state controller net.',
                           'No rerun of author scripts or inherited CI.',
                           'No exhaustive literature or priority certification.']}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
