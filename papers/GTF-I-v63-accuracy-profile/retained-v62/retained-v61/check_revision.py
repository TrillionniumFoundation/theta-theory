"""Finite regressions for the v61 entropy argument and LPS-action example.

These checks do not certify the universal entropy/transport theorems, an
infinite free group, or the imported LPS spectral norm. Exact arithmetic
checks and floating entropy diagnostics are reported separately.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path
import sympy as sp
import qubit_compiler as qc

HOME=Path(__file__).resolve().parent
COUNT=0
NEGATIVE=[]

def check(ok:bool, message:str)->None:
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(message)

def negative(name, fn)->None:
    try:fn()
    except (ValueError,RuntimeError,KeyError):NEGATIVE.append(name)
    else:raise RuntimeError('negative control was accepted: '+name)

def reject_unless(ok,message):
    if not ok:raise ValueError(message)

def mm(a,b):
    bt=qc.transpose(b)
    return tuple(tuple(qc.dot(x,y) for y in bt) for x in a)

def kernel_checks():
    s,H=sp.symbols('s H',positive=True)
    Z=sp.integrate((1-s/H)**2/4,(s,0,H))
    check(sp.simplify(Z-H/12)==0,'sphere kernel normalizer')
    fisher=sp.integrate((4*s-s*s)/(Z*H*H),(s,0,H))
    check(sp.simplify(fisher-(24/H-4))==0,'sphere Fisher information')
    for k in range(1,65):
        h2=F(1,k);theta=k*h2/4;gamma=(1-F(5,9))*(1-theta)
        check(theta==F(1,4),'support fraction')
        check(gamma==F(1,3),'spectral entropy constant')
        check(F(3*24,1)/gamma**2==648,'occupation coefficient')
        # pi^2 < 10 and log(12k) <= 3k are proved in prose.
        for z in [F(1,100),F(1,4),F(1,2),F(3,4),F(1)]:
            check(19*k+6480*(1-z)*k/z<=6500*k/z,'rational constant relaxation')
    negative('wrong_normalizing_area',lambda:reject_unless(sp.simplify(Z-H/4)==0,'area factor'))
    negative('wrong_fisher_constant',lambda:reject_unless(fisher.subs(H,1)<=12,'insufficient Fisher bound'))
    negative('wrong_spectral_square',lambda:reject_unless(F(5,9)==F(5,3),'operator norm square'))


def centroid_checks():
    # Unit input directions with rational norms, including a zero-centroid label.
    e=sp.Matrix([1,0,0]);f=sp.Matrix([0,1,0]);zero=sp.zeros(3,1)
    vectors=[e,sp.Rational(3,5)*f,zero]
    masses=[sp.Rational(1,3)]*3
    I=sp.eye(3);A=sp.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
    for r in [sp.Rational(0),sp.Rational(1,4),sp.Rational(1,2),sp.Rational(1)]:
        rows=[[r,1-r],[1-r,r],[sp.Rational(1,2),sp.Rational(1,2)]]
        alpha=sum(m*sp.sqrt(c.dot(c)) for m,c in zip(masses,vectors))
        q=[sp.Rational(0),sp.Rational(0)];sums=[sp.zeros(3,1),sp.zeros(3,1)];flows=[]
        for pi,c,row in zip(masses,vectors,rows):
            norm=sp.sqrt(c.dot(c))
            for R in [I,A]:
                for j,prob in enumerate(row):
                    w=pi*prob*norm/2;q[j]+=w;sums[j]+=pi*prob*R*c/2
                    if norm:flows.append((j,w,R*c/norm))
        normout=[sp.sqrt(v.dot(v)) for v in sums]
        for j in range(2):
            v=sums[j]/normout[j] if normout[j] else e
            cost=sum(w*(u-v).dot(u-v) for i,w,u in flows if i==j)
            check(sp.simplify(cost-2*(q[j]-normout[j]))==0,'centroid flow identity')
        check(sp.simplify(sum(q)-alpha)==0,'unnormalized mass conservation')
        delta=sp.simplify(alpha-sum(normout))
        check(bool(delta>=0),'centroid mass monotonicity')
        check(sp.simplify(sum(q)/alpha-1)==0,'direction law normalization')
        check(sum(masses[i]*sp.sqrt(vectors[i].dot(vectors[i]))/alpha for i in range(3))==1,'zero centroids omitted')
    # The ordinary hidden-label probabilities are not the directional masses.
    alpha=F(1,2)*1+F(1,2)*F(1,5)
    check((F(1,2)/alpha,F(1,10)/alpha)==(F(5,6),F(1,6)),'mass-weighted directions')
    negative('ordinary_label_weights_as_direction_weights',lambda:reject_unless((F(1,2),F(1,2))==(F(5,6),F(1,6)),'lost mass weights'))
    negative('zero_centroid_normalized',lambda:reject_unless(qc.dot(qc.ZERO,qc.ZERO)>0,'zero direction'))
    # A finite-dimensional first-harmonic bound is not a full L2 gap:
    # rotations by +/- 2*pi/3 have mean cos(theta)=-1/2 but fix frequency 3.
    check(sp.cos(2*sp.pi/3)==-sp.Rational(1,2),'first harmonic contracts')
    check(sp.cos(3*2*sp.pi/3)==1,'third harmonic invariant')
    negative('first_harmonic_is_full_spectral_certificate',lambda:reject_unless(sp.cos(2*sp.pi)<sp.Rational(1,2),'higher invariant frequency'))


def geometry_and_compiler_checks():
    data=json.loads((HOME/'RAMANUJAN_INPUT.json').read_text())
    commands,seed,probes,eta=qc.supplied_input(data)
    check(len(commands)==7 and seed==qc.E1,'exact LPS input schema')
    check(probes is None and eta is None,'terminal input has no probes')
    for name,A in commands.items():
        check(mm(A,qc.transpose(A))==qc.I,'orthogonality '+name)
        check(qc.dot(A[0],qc.cross(A[1],A[2]))==1,'determinant '+name)
        check(all((5*x).denominator==1 for row in A for x in row),'denominator five '+name)
    # Verify the quaternion/Pauli lifts of the exact displayed rotations.
    pauli=[sp.Matrix([[0,1],[1,0]]),sp.Matrix([[0,-sp.I],[sp.I,0]]),sp.diag(1,-1)]
    for j,S in enumerate(pauli,1):
        U=(sp.eye(2)-2*sp.I*S)/sp.sqrt(5)
        check(sp.simplify(U*U.conjugate().T-sp.eye(2))==sp.zeros(2),'algebraic lift unitary')
        for a in range(3):
            for b in range(3):
                value=sp.simplify(sp.trace(pauli[a]*U*pauli[b]*U.conjugate().T)/2)
                check(value==sp.Rational(commands['A'+str(j)][a][b]),'Bloch action convention')
    orbits={seed};profile=[]
    for t in range(6):
        check(len(orbits)==5**t,'finite coset-orbit profile '+str(t));profile.append(len(orbits))
        check(all((5**t*x).denominator==1 for v in orbits for x in v),'orbit denominator lattice')
        check(all(qc.dot(v,v)==1 for v in orbits),'pure orbit')
        if t<5:orbits={qc.apply(A,v) for A in commands.values() for v in orbits}
    negative('free_ball_instead_of_coset_ball',lambda:reject_unless(profile[1]==7,'stabilizer must be counted'))
    negative('squared_generator_alphabet_substitution',lambda:reject_unless(commands['A1']==mm(commands['A1'],commands['A1']),'different alphabet'))
    bad=json.loads(json.dumps(data));bad['commands']['A1'][0][0]='2'
    negative('nonorthogonal_supplied_input',lambda:qc.supplied_input(bad))
    bad=json.loads(json.dumps(data));bad['seed']=[0,0,0]
    negative('zero_seed',lambda:qc.supplied_input(bad))
    bad=json.loads(json.dumps(data));bad['seed']=[1.0,0,0]
    negative('floating_input_misrepresented_as_exact',lambda:qc.supplied_input(bad))
    machine=qc.compile_exact(2,F(1,2),max_labels=100,commands=commands,seed=seed)
    verts=machine['vertices'];tables=machine['rows'];dec=machine['decoder_bloch']
    for name,rows in tables.items():
        for i,row in enumerate(rows):
            target=qc.scale(machine['contraction'],qc.apply(commands[name],verts[i]))
            check(qc.valid_row(verts,row,target),'exact common row '+name)
            for b in [3,8]:
                rr=qc.dyadic(row,b)
                check(sum((p for _,p in rr),F(0))==1 and min(p for _,p in rr)>=0,'dyadic row stochastic')
                check(len(rr)<=4 and {i for i,_ in rr}<={i for i,_ in row},'dyadic support preserved')
                p=dict(row);q=dict(rr)
                tv=sum((abs(p.get(i,F(0))-q.get(i,F(0))) for i in p.keys()|q.keys()),F(0))/2
                check(tv<=3*F(1,2**b),'dyadic TV budget')
    for word in product(commands,repeat=2):
        dist={machine['initial_label']:F(1)};target=seed
        for name in word:
            nxt={}
            for i,pi in dist.items():
                for j,t in tables[name][i]:nxt[j]=nxt.get(j,F(0))+pi*t
            dist=nxt;target=qc.apply(commands[name],target)
        out=tuple(sum((pi*dec[i][j] for i,pi in dist.items()),F(0)) for j in range(3))
        check(out==qc.scale(F(1,2),target),'compiled horizon word')
    check(all(qc.dot(v,v)<=1 for v in dec),'legal density decoders')
    negative('illegal_density_decoder',lambda:reject_unless(qc.dot((F(2),F(0),F(0)),(F(2),F(0),F(0)))<=1,'not PSD'))
    negative('capacity_limit_bypassed',lambda:qc.compile_exact(2,F(1,2),max_labels=1,commands=commands))
    noisy=qc.compile_noisy(1,F(1,2),max_labels=100,commands=commands,seed=seed)
    for name,A in commands.items():
        row=noisy['rows'][name][noisy['initial_label']]
        out=tuple(sum((p*noisy['decoder_bloch'][j][d] for j,p in row),F(0)) for d in range(3))
        diff=tuple(x-y for x,y in zip(out,qc.apply(A,seed)))
        check(qc.dot(diff,diff)/2<=F(1,4),'actual noisy LPS row meets Frobenius budget')
    check(noisy['total_fair_bits']==noisy['fair_bits_per_transition'],'actual fair-bit budget')
    # Squaring the exact cap comparison reduces to sqrt(2)/2 < 1.
    check(F(1,2)<1,'robust separation strict after squaring')
    return {'tested_orbit_radii':list(range(6)),'orbit_cardinalities':profile,
            'compiled_labels':machine['labels'],'compiled_horizon':2,'compiled_words':7**2,'max_row_support':4}


def spacing_checks():
    for N in range(1,9):
        for mask in range(1<<N):
            cuts=[i+1 for i in range(N) if mask>>i&1]
            for gap in [1,2,3]:
                selected=[]
                for t in cuts:
                    if not selected or t-selected[-1]>=gap:selected.append(t)
                check(len(cuts)<=gap*len(selected),'cofinite return spacing')


def entropy_diagnostics():
    # Floating point diagnostics, separately counted and never called exact.
    n=12;kappa=.6;checked=0;worst=0.
    for r in range(1,6):
        f=[n/r if i<r else 0. for i in range(n)]
        pf=[kappa*x+1-kappa for x in f]
        ent=lambda a:sum(x*math.log(x) for x in a if x)/n
        defect=ent(f)-ent(pf);bound=(1-kappa*kappa)*(1-r/n)
        if defect+1e-12<bound:raise RuntimeError('finite entropy diagnostic failed')
        worst=max(worst,bound-defect);checked+=1
    return {'finite_models':checked,'method':'floating-point diagnostics only','largest_bound_minus_loss':worst}


def main():
    kernel_checks();centroid_checks();g=geometry_and_compiler_checks();spacing_checks();e=entropy_diagnostics()
    result={'schema':'gtf61.checks/1','status':'success','exact_finite_assertions':COUNT,
            'negative_controls_detected':NEGATIVE,'new_example':g,'entropy_diagnostics':e,
            'spectral_gap_certified_by_tests':False,'infinite_freeness_certified_by_tests':False,
            'universal_transport_or_entropy_certified_by_tests':False,
            'scope':'Finite exact algebra, rational rows, short orbit profiles and separate floating diagnostics; universal claims rely on written proofs and identified external theorems.'}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
