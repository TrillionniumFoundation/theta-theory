#!/usr/bin/env python3
"""Exact finite regressions for v32. Analytic claims are proved in the article."""
from __future__ import annotations
import argparse
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import sympy as s


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError('CHECK_REJECTED: ' + message)


def mv(A, v):
    return tuple(sum(a*x for a,x in zip(row,v)) for row in A)


def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(len(B)))
                       for j in range(len(B[0]))) for i in range(len(A)))

R=((F(3,5),F(-4,5)),(F(4,5),F(3,5)))
I=((F(1),F(0)),(F(0),F(1)))
a=F(1,10)
V=((F(1,2),F(0)),(F(-1,2),F(1,2)),(F(-1,2),F(-1,2)))


def initial(x):
    return (F(1,2)+a*x[0], F(1,4)-a*x[0]/2+a*x[1],
            F(1,4)-a*x[0]/2-a*x[1])


def exact_rotation_tests():
    count=0; ranks=[]; min_prob=F(1)
    powers=[I]
    for _ in range(11): powers.append(mm(R,powers[-1]))
    require(mm(tuple(zip(*R)),R)==I,'Rational rotation is not orthogonal')
    require(R[0][0]*R[1][1]-R[0][1]*R[1][0]==1,'Rotation determinant')
    for n in range(9):
        for x in itertools.product([-1,1],repeat=2):
            p=initial(x)
            require(sum(p)==1 and min(p)>=0,'Seed encoder normalization')
            require(tuple(sum(p[k]*V[k][j] for k in range(3)) for j in range(2))==tuple(a*z for z in x),'Seed reconstruction')
            for word in itertools.product([0,1],repeat=n):
                q=0
                for c in word: q+=c
                expected=mv(powers[q],tuple(a*z for z in x))
                actual=tuple(sum(p[k]*mv(powers[q],V[k])[j] for k in range(3)) for j in range(2))
                require(actual==expected,'Counter realization mismatch')
                for j in range(2):
                    for b in [-1,1]:
                        z=(1+b*actual[j])/2
                        require(F(2,5)<z<F(3,5),'Uniform support diagnostic')
                        min_prob=min(min_prob,z)
                count+=1
        # Every cut has exact rank three; a three-column witness suffices.
        for t in range(n+1):
            rows=[]
            for x in itertools.product([-1,1],repeat=2):
                for q in range(t+1):
                    z=mv(powers[q],tuple(a*v for v in x))
                    rows.append([F(1),*z])
                    # Same rational triangle encloses every actual mean.
                    weights=(F(1,2)+z[0],F(1,4)-z[0]/2+z[1],F(1,4)-z[0]/2-z[1])
                    require(min(weights)>=0 and sum(weights)==1,'Static triangle does not enclose')
            require(s.Matrix(rows).rank()==3,'Cut rank witness')
            ranks.append([n,t,3])
    return {'complete_words':count,'rank_witnesses':len(ranks),
            'minimum_probability_in_finite_checks':str(min_prob),
            'rational_counter_peak':'3*(N+1)'}


def polygon_tests():
    rows=0; outputs=0; table=[]
    RR=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
    # Algebraic vertices and exact mean identities, with brackets selected once.
    for M in [4,8,12]:
        U=[s.Matrix([s.cos(2*s.pi*k/M),s.sin(2*s.pi*k/M)]) for k in range(M)]
        ratio=s.cos(s.pi/M)
        shift=0 if M==4 else 1
        for c in [0,1]:
            for k in range(M):
                l=(k+(shift if c else 0))%M
                w=s.simplify(ratio*(RR**c)*U[k])
                AB=s.simplify(s.Matrix.hstack(U[l],U[(l+1)%M]).inv()*w)
                A,B=map(s.simplify,AB)
                p=[s.simplify((1-A-B)/M+(A if j==l else 0)+(B if j==(l+1)%M else 0)) for j in range(M)]
                require(s.simplify(sum(p)-1)==0,'Polygon row normalization')
                # All are algebraic; SymPy signs are required, no tolerance test.
                require(all(v.is_nonnegative is True for v in p),'Polygon algebraic sign undecided or negative')
                z=s.zeros(2,1)
                for j in range(M): z+=p[j]*U[j]
                require(all(s.simplify(v)==0 for v in z-w),'Polygon update mean')
                if k==0: table.append({'M':M,'command':c,'row':[str(v) for v in p]})
                rows+=1
        # Use linearity to verify a four-command future decoder identity.
        for word in itertools.product([0,1],repeat=4):
            z=s.Matrix([s.Rational(1,10),-s.Rational(1,10)])
            for c in word: z=RR**c*z
            require(s.simplify((z.T*z)[0]-s.Rational(1,50))==0,'Rotation norm invariant')
            outputs+=1
    # Radius bounds in the analytic proof use only these rational inequalities.
    require(F(1)-F(5,16)==F(11,16),'Bernoulli radius constant')
    require(F(16**2*2,110**2)<1,'Terminal polygon radius')
    return {'exact_algebraic_rows':rows,'norm_word_checks':outputs},table


def lift_tests():
    # Agreement on the reachable affine line does not imply unit-state agreement.
    eh=[(F(1,2),F(0),F(1,2)),(F(0),F(1,2),F(1,2))]
    p=(F(1),F(0),F(0));q=(F(0),F(-1),F(1))
    require(all(sum(e[i]*(p[i]-q[i]) for i in range(3))==0 for e in eh),'Affine relation')
    require(p!=q,'Hidden unit states accidentally identified')
    # A simplex section can have more vertices than the ambient simplex.
    vertices=[tuple(v for bit in bits for v in ([F(1,3),F(0)] if bit else [F(0),F(1,3)]))
              for bits in itertools.product([0,1],repeat=3)]
    require(len(vertices)==8 and 8>6,'Lift example vertex count')
    require(all(sum(v)==1 and min(v)>=0 for v in vertices),'Lift simplex section')
    require(len({tuple(i for i,z in enumerate(v) if z==0) for v in vertices})==8,'Distinct active supports')
    return {'reachable_affine_counterexample':True,'simplex_section_dimension':3,
            'simplex_section_vertices':8,'ambient_simplex_labels':6}


def constants_tests():
    alpha=(s.sqrt(5)-1)/2; Fs=[0,1]
    for _ in range(23): Fs.append(Fs[-1]+Fs[-2])
    n=0
    for M in [3,4,8,16,32,64,128,256]:
        m=next(i for i,f in enumerate(Fs) if f>=32*M)
        q,p=Fs[m],Fs[m-1]
        require(32*M<=q<64*M,'Fibonacci net size')
        require(s.gcd(p,q)==1,'Fibonacci coprimality')
        require(s.simplify(q*alpha-p-(-1)**(m-1)*alpha**m)==0,'Fibonacci error identity')
        n+=1
    require(F(9*10*3,2*2*32**2)<a,'Support deficit constant')
    # sqrt(2)<10/7 gives the required area coefficient strictly.
    lower=a**3/(4096*F(10,7))
    require(lower>F(1,6000000),'Area constant')
    require(F(4)*6000000==24000000,'Profile sum constant')
    beta=F(1,4)+F(1,18)+F(1,17)
    require(beta==F(223,612) and F(9,20)-beta==F(131,1530),'Primitive strict margin')
    return {'golden_orbit_identities':n,'area_expansion_coefficient':'1/6000000',
            'profile_sum_bound':24000000,'primitive_margin':'131/1530'}


def frontier_tests():
    minimal={(0,0)};cases=0
    for m in range(1,41):
        minimal={(x+a,y+b) for x,y in minimal for a,b in [(3,4),(4,3)]}
        expected={(3*m+j,4*m-j) for j in range(m+1)}
        require(minimal==expected,'Minkowski frontier')
        require(min(max(p) for p in minimal)==(7*m+1)//2,'Peak balance')
        for x in range(3*m-1,4*m+2):
            for y in range(3*m-1,4*m+2):
                feasible=any(x>=u and y>=v for u,v in minimal)
                require(feasible==(x>=3*m and y>=3*m and x+y>=7*m),'Frontier holes')
                cases+=1
    return {'summand_counts_checked':40,'profile_cases':cases}


def negative(name):
    if name=='nonstochastic-row':
        row=list(initial((1,1)));row[0]+=F(1,10)
        require(sum(row)==1,'Mutant encoder row is not stochastic')
    elif name=='unread-command':
        z=(a,a);require(mv(R,z)==z,'Mutant advances on the idle command')
    elif name=='polygon-radius':
        require(F(3,5)+F(4,5)<=1,'Removing radial slack makes row negative')
    elif name=='unit-state-projection':
        require((1,0,0)==(0,-1,1),'Affine-prefix equality was extended to arbitrary unit states')
    elif name=='free-tag':
        supports=[{0},{0}];require(not(supports[0]&supports[1]),'Mutant shares a state across exact terminal tags')
    elif name=='separate-minima-splice':
        beta=F(223,612);require(beta>=F(9,20),'Three-parent/three-child splice violates the trace bound')
    elif name=='golden-net':
        require(32*8<=144,'Orbit is too short for the declared net constant')
    elif name=='volume-constant':
        require(a**3/(4096*F(10,7))>=F(1,5000000),'Mutant overstates the proved area coefficient')
    else: raise ValueError('Unknown control '+name)
    raise RuntimeError('Negative control failed to execute')


def main():
    p=argparse.ArgumentParser();p.add_argument('--negative-control');p.add_argument('--export',type=Path)
    args=p.parse_args()
    if args.negative_control: negative(args.negative_control)
    rot=exact_rotation_tests();poly,table=polygon_tests()
    out={'schema':'gtf32.exact/1','rational_rotation':rot,'polygon_rows':poly,
         'reachable_lift':lift_tests(),'constants':constants_tests(),'tagged_frontier':frontier_tests(),
         'separate_minimum':'3 at every internal cut',
         'golden_width_lower':'max(3, log2(N/24000000)/6)',
         'width_upper':'min(3*(N+1),4*ceil(sqrt(N+1)))',
         'all_hidden_state_lower_bound':True,
         'scope':'Finite identities and implementation checks. Volume minimization, uniform bounds and asymptotics are analytic proofs in the article; no numerical delta_M is claimed.'}
    if args.export:
        args.export.parent.mkdir(parents=True,exist_ok=True)
        args.export.write_text(json.dumps({'rational_rotation':[[str(v) for v in r] for r in R],
           'seed_vertices':[[str(v) for v in r] for r in V],'polygon_rows':table},indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    try: main()
    except RuntimeError as e:
        print(str(e),file=sys.stderr);sys.exit(1)
