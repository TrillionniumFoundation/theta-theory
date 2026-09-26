#!/usr/bin/env python3
"""Exact finite regressions for v45. Universal proofs are in the article."""
from __future__ import annotations
import argparse
from itertools import product
import json
from pathlib import Path
import sys
import sympy as sp

Q=sp.Rational
NEGATIVES=['omit-clock-drift','omit-tail-conjugates','reverse-cocycle-order',
 'ambient-instead-active','drop-row-compatibility','drop-normalization',
 'ignore-moving-projection','drop-minimum-branch']


def check(ok, message: str) -> None:
    if not bool(ok): raise ValueError(message)


def key(m):return tuple(m)


def finite_closure(commands, reference=0, conjugate=True, safety=256):
    """Finite-instance audit, with a safety cap (not the general decision oracle)."""
    a=commands[reference];ai=a.inv();d=a.rows
    seen={key(sp.eye(d)):sp.eye(d)}
    for u in commands:
        g=ai*u;seen[key(g)]=g
    rounds=0
    while True:
        old=list(seen.values());fresh={}
        for g in old:
            for h in [g.inv(),*([ai*g*a,a*g*ai] if conjugate else [])]:fresh[key(h)]=h
            for h in old:
                v=g*h;fresh[key(v)]=v
        for k,v in fresh.items():seen[k]=v
        rounds+=1
        check(len(seen)<=safety,'finite-instance audit reached its noncertifying safety cap')
        if len(seen)==len(old):return list(seen.values()),rounds


def run(mutant: str|None=None):
    counts={};export={}
    r=sp.Matrix([[Q(3,5),-Q(4,5)],[Q(4,5),Q(3,5)]])
    p=sp.Matrix([[0,1,0],[1,0,0],[0,0,1]])
    q=sp.Matrix([[0,1,0],[0,0,1],[1,0,0]])
    a=sp.diag(r,q);commands=[a,sp.diag(r,q*p)]
    for u in commands:check(u.T*u==sp.eye(5),'nonorthogonal command')
    group,rounds=finite_closure(commands,conjugate=mutant!='omit-tail-conjugates')
    check(len(group)==6,'tail conjugates must generate all six relative permutations')
    other,_=finite_closure(commands,reference=1)
    check({key(g) for g in other}=={key(g) for g in group},'reference-dependent subgroup')
    check(commands[0]*commands[1]!=commands[1]*commands[0],'example accidentally commutes')
    group_set={key(g) for g in group};rows=words=mean_coordinates=0
    powers={i:a**i for i in range(-7,8)}
    for t in range(6):
        for u in commands:
            b=powers[-t-1]*u*powers[t]
            check(key(b) in group_set,'cocycle escaped the relative group')
            images=[]
            for g in group:
                images.append(key(b*g));rows+=1
            check(len(set(images))==6 and set(images)==group_set,'update is not a permutation')
    for n in range(1,7):
        for word in product(range(2),repeat=n):
            g=sp.eye(5);uword=sp.eye(5)
            for t,c in enumerate(word):
                b=powers[-t-1]*commands[c]*powers[t]
                g=g*b if mutant=='reverse-cocycle-order' else b*g
                uword=commands[c]*uword
            check(g==powers[-n]*uword,'relative cocycle multiplication order')
            read=g if mutant=='omit-clock-drift' else powers[n]*g
            check(read==uword,'horizon decoder must restore common clock motion')
            for xindex in range(5):
                for sign in [-1,1]:
                    x=sign*sp.eye(5)[:,xindex]
                    check(read*x==uword*x,'finite tracker mean mismatch')
                    mean_coordinates+=5
            words+=1
    counts.update(finite_group_order=6,closure_rounds=rounds,reference_choices=2,
                  finite_tracker_words=words,finite_tracker_mean_coordinates=mean_coordinates,
                  permutation_command_rows=rows)
    export['noncommuting_commands']=[[[str(v) for v in u.row(i)] for i in range(5)] for u in commands]
    export['relative_group']=[[[str(v) for v in g.row(i)] for i in range(5)] for g in group]

    one,_=finite_closure([r]);check(len(one)==1,'one-letter drift is not relative uncertainty')
    rz=sp.diag(r,1);seed=sp.Matrix([0,0,1])
    reachable=sp.Matrix.hstack(seed,rz*seed,rz**2*seed)
    dim=3 if mutant=='ambient-instead-active' else reachable.rank()
    check(dim==1,'unused rotating coordinates must not enter the active space')
    check(rz.trace()==Q(11,5) and rz.trace().q!=1,'rational trace certificate failed')
    check((rz**5).T*(rz**5)==sp.eye(3),'infinite-order example is not orthogonal')
    n=5;bound=sp.prod(3**n-3**j for j in range(n))
    check(bound<3**(n*n),'finite group order bound')
    counts.update(one_letter_relative_order=1,active_fixed_axis_dimension=dim,
                  rational_infinite_order_trace=str(rz.trace()),finite_order_bound_dimension=n)

    # A complete variable-width continuation flag, with exact common rows.
    ts=[
      [sp.Matrix([[Q(1,2),Q(1,3),Q(1,6)],[Q(1,4),Q(1,4),Q(1,2)]]),
       sp.Matrix([[Q(1,3),Q(1,3),Q(1,3)],[0,Q(2,3),Q(1,3)]])],
      [sp.Matrix([[Q(1,2),Q(1,2)],[1,0],[Q(1,3),Q(2,3)]]),
       sp.Matrix([[Q(1,4),Q(3,4)],[0,1],[Q(2,3),Q(1,3)]])],
      [sp.Matrix([[Q(1,3),Q(2,3)],[Q(1,2),Q(1,2)]]),
       sp.Matrix([[0,1],[Q(3,4),Q(1,4)]])]]
    f=[{} for _ in range(4)];f[3][()]=sp.Matrix([[Q(1,3),-Q(1,2)],[-Q(2,3),Q(1,4)]])
    for t in range(2,-1,-1):
        for c in range(2):
            for suffix,mat in f[t+1].items():f[t][(c,)+suffix]=ts[t][c]*mat
    if mutant=='drop-row-compatibility':ts[1][0][0,0]+=Q(1,10);ts[1][0][0,1]-=Q(1,10)
    init=sp.Matrix([[Q(1,4),Q(3,4)],[Q(2,3),Q(1,3)]])
    if mutant=='drop-normalization':init[0,0]+=Q(1,10)
    check(all(sum(init.row(i))==1 for i in range(init.rows)),'initialization must be normalized')
    shifts=0
    for t in range(3):
        for c in range(2):
            check(all(sum(ts[t][c].row(i))==1 for i in range(ts[t][c].rows)),'command normalization')
            for suffix,mat in f[t+1].items():
                check(f[t][(c,)+suffix]==ts[t][c]*mat,'one common continuation row failed')
                shifts+=mat.cols*ts[t][c].rows
    for word in product(range(2),repeat=3):
        value=init
        for t,c in enumerate(word):value=value*ts[t][c]
        check(value*f[3][()]==init*f[0][word],'flag forward/backward mismatch')
    counts.update(continuation_shift_coordinates=shifts,flag_complete_words=8)

    # Every separate probability Hankel cut has a normalized three-factor witness.
    vertices=sp.Matrix([[Q(1,2),0],[-Q(1,2),Q(1,2)],[-Q(1,2),-Q(1,2)]])
    bary=sp.Matrix.vstack(sp.ones(1,3),vertices.T).inv()
    rp={i:r**i for i in range(5)};rho=Q(1,10);hcases=entries=0
    for n in range(1,4):
        for t in range(n+1):
            erows=[];targets=[]
            for prefix in product(range(2),repeat=t):
                for j in range(2):
                    for sign in [-1,1]:
                        z=rho*rp[sum(prefix)]*(sign*sp.eye(2)[:,j]);targets.append(z)
                        weights=bary*sp.Matrix([1,z[0],z[1]])
                        check(sum(weights)==1 and min(weights)>=0,'triangle encoding invalid')
                        erows.append(list(weights))
            fm=[];descriptors=[]
            for suffix in product(range(2),repeat=n-t):
                for j in range(2):
                    for sign in [-1,1]:descriptors.append((suffix,j,sign))
            for v in vertices.tolist():
                fm.append([(1+sign*(rp[sum(suffix)]*sp.Matrix(v))[j])/2 for suffix,j,sign in descriptors])
            e=sp.Matrix(erows);b=sp.Matrix(fm)
            h=sp.Matrix([[(1+sign*(rp[sum(suffix)]*z)[j])/2 for suffix,j,sign in descriptors] for z in targets])
            check(e*b==h,'nonnegative factorization mismatch')
            check(min(b)>=0 and max(b)<=1 and all(b[i,j]+b[i,j+1]==1 for i in range(3) for j in range(0,b.cols,2)),'factor normalization')
            check(h.rank()==3,'probability Hankel rank is not three')
            hcases+=1;entries+=h.rows*h.cols
    counts.update(hankel_cuts=hcases,hankel_entries=entries)
    # A fixed axis destroys a whole-space packet even though moving directions compress.
    plane_gamma=1-sp.sqrt(sp.Rational(4,5));full_gamma=sp.Integer(0)
    test_gamma=full_gamma if mutant=='ignore-moving-projection' else plane_gamma
    check(test_gamma>0,'the moving subspace must be isolated before compact uniformization')
    check((sp.eye(3)+rz)*seed/2==seed,'fixed-axis zero-distortion witness')
    counts['moving_packet_loss']=str(plane_gamma)

    exponent_cases=0
    for rr in range(1,8):
        for hh in [Q(1,10),Q(1,2),Q(1),Q(2),Q(5)]:
            candidate=rr*(1+hh)/(2*rr+1+hh);strong=min(Q(1,2),candidate)
            check(strong<=candidate,'dropping the minimum would only weaken an upper bound')
            check((candidate<=Q(1,2))==(hh*(2*rr-1)<=1),'active exponent branch condition')
            if rr==1 and hh==2:
                chosen=candidate if mutant=='drop-minimum-branch' else strong
                check(chosen==Q(1,2),'the displayed sharp upper branch must retain the minimum')
            exponent_cases+=1
    counts['minimal_type_branch_cases']=exponent_cases
    export['certificate_counts']=counts
    return {'schema':'gtf45.checks/1','exact_checks':counts,
            'proved_in_article':{'boundedness':'finite synchronization subgroup iff uniformly bounded exact width',
             'robust_basis_threshold':'epsilon < rho/(2D)',
             'algebraic_decision':'terminating exact normal-conjugation enumeration; not a spectral-gap algorithm',
             'flag':'actual terminal-error formula in full continuation coordinates',
             'growth_rates':'earlier arithmetic theorems retained; no new general rate claim'},
            'scope':'Exact finite identities and representative compiler tests; not universal proof, independent priority certification, or exhaustive testing of an infinite matrix group.'},export


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--negative-control',choices=NEGATIVES)
    parser.add_argument('--export',type=Path);args=parser.parse_args()
    try:result,extra=run(args.negative_control)
    except ValueError as exc:
        print('CHECK_REJECTED: '+str(exc),file=sys.stderr);sys.exit(2)
    if args.negative_control:
        print('Negative control unexpectedly survived',file=sys.stderr);sys.exit(3)
    if args.export:args.export.write_text(json.dumps(extra,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
