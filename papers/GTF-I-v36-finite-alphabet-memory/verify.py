#!/usr/bin/env python3
"""Exact finite regressions and labelled high-precision diagnostics for GTF-I v36.

No finite test here establishes an L2 spectral gap, an asymptotic theorem,
independent mathematical correctness, or a novelty/priority claim.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
import mpmath as mp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError('CHECK_REJECTED: ' + message)


def matrix_data():
    q=sp.Rational
    rx=sp.Matrix([[1,0,0],[0,q(-7,25),q(-24,25)],[0,q(24,25),q(-7,25)]])
    rz=sp.Matrix([[q(-7,25),q(-24,25),0],[q(24,25),q(-7,25),0],[0,0,1]])
    return [sp.eye(3),rx,rx.T,rz,rz.T]


def word_collision_check() -> int:
    # Eight equally likely words, two spellings for each C4 product.
    # The endpoint may distinguish the spellings; exhaust all binary assignments.
    phases=[(1,0),(0,1),(-1,0),(0,-1)]*2
    for assignment in itertools.product(range(2),repeat=8):
        v=[[0,0],[0,0]]
        for (x,y),r in zip(phases,assignment):v[r][0]+=x;v[r][1]+=y
        # Each centroid contributes its unnormalised norm / 8.
        # The two sums are opposites. q'^2 <= 1/2 exactly.
        require(v[0][0]+v[1][0]==0 and v[0][1]+v[1][1]==0,'Collision sum')
        require(v[0][0]**2+v[0][1]**2<=8,'Full-word contraction witness')
    return 256


def rational_checks() -> tuple[dict,dict]:
    matrices=matrix_data();q=sp.Rational
    for a in matrices:require(a.T*a==sp.eye(3) and a.det()==1,'SO(3) gate identity')
    require(matrices[1]*matrices[3]!=matrices[3]*matrices[1],'Noncommuting generators')
    pauli=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    for axis,index in [(0,1),(2,3)]:
        a=(3*sp.eye(2)-4*sp.I*pauli[axis])/5
        require(sp.simplify(a*a.conjugate().T)==sp.eye(2),'Unitary lift')
        for j in range(3):
            rhs=sum([matrices[index][i,j]*pauli[i] for i in range(3)],sp.zeros(2))
            require(sp.simplify(a*pauli[j]*a.conjugate().T-rhs)==sp.zeros(2),'Bloch adjoint')
    # An exactly rational octahedral machine at short horizons, not the
    # asymptotically optimal stereographic construction.
    vertices=[sp.eye(3)[:,j]*s for j in range(3) for s in [1,-1]]
    gamma=q(2,3);rows=[]
    for a in matrices:
        t=sp.zeros(6)
        for i,v in enumerate(vertices):
            w=gamma*a*v
            for j in range(3):t[i,2*j if w[j]>=0 else 2*j+1]+=abs(w[j])
            rem=1-sum(abs(w[j]) for j in range(3))
            require(rem>=0,'Octahedral slack')
            t[i,0]+=rem/2;t[i,1]+=rem/2
            require(sum(t[i,j] for j in range(6))==1,'Rational row sum')
            recon=sum([t[i,j]*vertices[j] for j in range(6)],sp.zeros(3,1))
            require(recon==w,'Rational row mean')
        rows.append(t)
    count=0;means=0
    for n in [1,2,3]:
        scale=q(1,5)/gamma**n
        require(scale<1,'Decoder bound')
        for seed_idx,x in enumerate(vertices):
            e=sp.zeros(1,6);e[0,seed_idx]=q(1,2);e[0,0]+=q(1,4);e[0,1]+=q(1,4)
            for word in itertools.product(range(5),repeat=n):
                p=e;v=x
                for a in word:p=p*rows[a];v=matrices[a]*v
                result=scale*sum([p[j]*vertices[j] for j in range(6)],sp.zeros(3,1))
                require(result==v/10,'Complete-word exact output')
                require(all(q(9,20)<=(1+result[j])/2<=q(11,20) for j in range(3)),'Uniform support')
                count+=1;means+=3
    # Dimension witness is independent of the horizon.
    witness=sp.Matrix([[1,*list(x/10)] for x in vertices])
    require(witness.rank()==4,'Separate normalized rank four')
    cap_cases=0
    for n in range(1,41):
        eta=1-q(1,8*n)
        require(eta**n>=q(7,8),'Radial decoder budget')
        cap_cases+=1
    grid_count=0
    for m in [1,2,3]:
        for t in itertools.product([q(-1),q(-1,2),q(0),q(1,2),q(1)],repeat=m):
            d=1+sum(x*x for x in t)
            u=[2*x/d for x in t]+[(1-sum(x*x for x in t))/d]
            require(sum(x*x for x in u)==1,'Rational stereographic sphere')
            grid_count+=1
    export={'gate_order':['I','Rx','Rx_inverse','Rz','Rz_inverse'],
            'rational_gates':[[[str(x) for x in a.row(i)] for i in range(3)] for a in matrices],
            'short_horizon_octahedral_rows':[[[str(x) for x in a.row(i)] for i in range(6)] for a in rows],
            'short_horizon_scope':'6 states, shrink 2/3, scale a_t=(1/5)*(3/2)^t; exact for horizons 1,2,3. This is a finite regression, not the asymptotically optimal net.',
            'spectral_gap':'Bourgain--Gamburd theorem is invoked analytically. No numerical gap is asserted.'}
    return {'rational_word_cases':count,'exact_coordinate_means':means,'stereographic_points':grid_count,
            'radial_budget_cases':cap_cases,'bloch_adjoint_identities':6,'command_rows':30},export


def sampler_checks() -> dict:
    comparisons=0;rows=0
    for b in range(1,9):
        for m in range(2**b+1):
            count=0
            for u in range(2**b):
                if m==2**b: outcome=True
                elif m==0: outcome=False
                else:
                    outcome=False
                    for i in range(b-1,-1,-1):
                        ub=(u>>i)&1;mb=(m>>i)&1
                        if ub!=mb:outcome=ub<mb;break
                require(outcome==(u<m),'Bitwise threshold without prefix register')
                count+=int(outcome);comparisons+=1
            require(count==m,'Exact Bernoulli law');rows+=1
    # A sequential categorical tree with rational conditional probabilities.
    for probs in [[F(1,7),F(2,7),F(4,7)],[F(0),F(3,5),F(1,5),F(1,5)],
                  [F(1,4)]*4,[F(1),F(0)]]:
        for b in range(1,9):
            rem=F(1);true_rem=F(1);rounded=[]
            for p in probs[:-1]:
                c=p/true_rem if true_rem else F(0)
                z=F(math.floor(c*2**b),2**b)
                rounded.append(rem*z);rem*=1-z;true_rem-=p
            rounded.append(rem)
            tv=sum(abs(a-bb) for a,bb in zip(probs,rounded))/2
            require(tv<=(len(probs)-1)*F(1,2**b),'Categorical row TV budget')
    return {'threshold_rows':rows,'bit_comparisons':comparisons,'categorical_rounding_cases':32}


def interval_checks() -> int:
    count=0
    for n in range(1,11):
        for mask in range(2**n):
            low=[i+1 for i in range(n) if mask>>i&1]
            for B in [1,2,3,4]:
                remaining=[t for t in low if t>=B];selected=[]
                while remaining:
                    t=remaining[0];selected.append(t);remaining=[u for u in remaining if u>=t+B]
                require(all(b-a>=B for a,b in zip(selected,selected[1:])),'Disjoint packets')
                require(len(low)<=B-1+B*len(selected),'Occupation packing bound')
                count+=1
    return count


def monomial_diagnostics() -> dict:
    mp.mp.dps=80;tol=mp.mpf('1e-65');alpha=(mp.sqrt(5)-1)/2
    p0,q0=34,55;q=2*q0;M=3;N=13
    delta=2*mp.pi*(alpha-mp.mpf(p0)/q0);a=mp.pi/q
    require(q>=max(8*M,8,(160*M*N)**(1/3)),'Resonance size')
    def lam(n):return mp.cos(a-abs(n*delta))/mp.cos(a)
    Lambda=max(lam(n) for n in range(-M,M+1))
    require(mp.log(Lambda)<=160*M/q**3,'Resonance radial bound')
    require(Lambda**N/4<1,'Monomial decoder range')
    rows=0
    for n in range(-M,M+1):
        ln=lam(n);omega=mp.sin(abs(n*delta))/(ln*mp.sin(2*a))
        require(-tol<=omega<=1+tol,'Edge weights')
        for l in [0,1,17,43,81]:
            for conjugate in [False,True]:
                old=-l if conjugate else l
                base=(old+2*n*p0)%q;shift=0 if n==0 else (1 if n*delta>0 else -1)
                c=(1+ln/Lambda)/2
                rr=[(base,c*(1-omega)),((base+shift)%q,c*omega),
                    ((base+q//2)%q,(1-c)*(1-omega)),((base+shift+q//2)%q,(1-c)*omega)]
                got=sum(w*mp.exp(2j*mp.pi*j/q) for j,w in rr)
                target=mp.exp(2j*mp.pi*(mp.mpf(old)/q+n*alpha))/Lambda
                require(abs(got-target)<tol,'Sparse monomial exact-identity diagnostic')
                require(abs(sum(w for _,w in rr)-1)<tol,'Sparse row stochasticity');rows+=1
    return {'decimal_precision':80,'sparse_monomial_rows':rows,'scope':'High-precision diagnostics, not exact algebraic proof.'}


def negative(name:str)->None:
    if name=='dependent-word':
        # Product is always identity, but spelling reveals Y=+1 or -1.
        q0=0;q1=1
        require(q1<=q0,'Fresh full word, not merely fresh product, is necessary')
    elif name=='product-sufficiency':
        same_product=[0,0];rows=[[1,0],[0,1]]
        require(rows[0]==rows[1],'Same-product spellings may have different endpoint rows')
    elif name=='finite-spectrum-is-gap':
        # Quarter-turn: first harmonic averages to zero, fourth is invariant.
        z=[1,sp.I,-1,-sp.I]
        require(sum(t**4 for t in z)/4!=1,'First-harmonic contraction is not a full L2 gap')
    elif name=='haar-is-one-letter':
        B=17;charged=1
        require(charged==B,'Finite mixing packet must charge every command')
    elif name=='free-sampler-clock':
        b=8;states=1
        require(states>=b,'Threshold comparison must retain its bit position')
    elif name=='probabilities-are-languages':
        p=F(3,5);shrunk=F(1,2)+(p-F(1,2))*F(1,2)**20
        require(p==shrunk,'Positive shrinking margin preserves a cutpoint, not probabilities')
    elif name=='missing-conjugation':
        z=1+2*sp.I
        require(z==sp.conjugate(z),'Conjugation is an actual command, not a phase permutation omission')
    elif name=='unpriced-antipode':
        Lambda=F(11,10);ln=F(21,20)
        require(F(1,1)/ln==F(1,1)/Lambda,'Common radius needs the charged antipodal mixture')
    elif name=='wrong-terminal-tv':
        p=F(3,5);q=F(1,2)
        require(abs((2*p-1)-(2*q-1))<=abs(p-q),'Mean error is twice binary TV')
    elif name=='overlapping-packets':
        intervals=[(0,3),(2,5)]
        require(intervals[0][1]<=intervals[1][0],'Independent packet budget requires disjoint blocks')
    else:raise ValueError('Unknown negative control: '+name)
    raise RuntimeError('Negative control unexpectedly passed: '+name)


def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--negative-control');p.add_argument('--export',type=Path)
    args=p.parse_args()
    if args.negative_control:negative(args.negative_control);return
    counts,export=rational_checks()
    counts['full_word_binary_assignments']=word_collision_check()
    counts['interval_profile_cases']=interval_checks();counts.update(sampler_checks())
    floating=monomial_diagnostics()
    if args.export:
        args.export.parent.mkdir(parents=True,exist_ok=True)
        args.export.write_text(json.dumps(export,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'schema':'gtf36.checks/1','exact_counts':counts,'floating_diagnostics':floating,
       'analytic_statements':{'word_product_collisions':'Full fresh-word kernels; no product-sufficiency restriction',
       'spectral_gap_class':'(N/log(N+1))^((d-1)/2) <= constant*W <= constant*N^((d-1)/2); logarithmic gap retained',
       'explicit_rational_gates':'Five fixed symbols, three-dimensional sphere; rank four; N/log N lower and N upper',
       'matched_monomial_class':'Theta(N^(1/3)) for fixed badly approximable angle and finite resonant monomial alphabet',
       'dyadic_control':'O(K log(N/delta)) labels, fixed alphabet and sparse common rows; self-paced nonuniform model',
       'spectral_gap_numerically_certified':False,'priority_independently_certified':False},
       'scope':'Finite exact algebra and labelled high-precision diagnostics; universal bounds, spectral gap and asymptotics are analytic arguments, not certified by these tests.'},indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError) as e:
        print(str(e),file=sys.stderr);sys.exit(1)
