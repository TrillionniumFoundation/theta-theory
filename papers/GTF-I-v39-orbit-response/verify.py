#!/usr/bin/env python3
"""Exact finite witnesses. Universal orbit/entropy assertions are analytic proofs."""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path
import sympy as sp

R=sp.Rational

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError('CHECK_REJECTED: '+message)

def partitions(n: int, lo: int=1):
    if n==0:
        yield ()
    else:
        for j in range(lo,n+1):
            for tail in partitions(n-j,j):
                yield (j,)+tail

def orbit_rank(q: int, mult: tuple[int,...], complex_case: bool) -> int:
    vals=[i for i,m in enumerate(mult) for _ in range(m)]
    A=sp.diag(*vals)
    generators=[]
    for i in range(q):
        for j in range(i+1,q):
            K=sp.zeros(q);K[i,j]=1;K[j,i]=-1;generators.append(K)
            if complex_case:
                L=sp.zeros(q);L[i,j]=sp.I;L[j,i]=sp.I;generators.append(L)
    if complex_case:
        for i in range(q-1):
            K=sp.zeros(q);K[i,i]=sp.I;K[q-1,q-1]=-sp.I;generators.append(K)
    columns=[]
    for B in generators:
        C=B*A-A*B
        columns.append(sp.Matrix([sp.re(z) for z in C]+[sp.im(z) for z in C]))
    return sp.Matrix.hstack(*columns).rank()

def calculate(negative: str|None=None):
    counts={};witness={}
    dims={};rankcases=0
    for q in range(2,7):
        records=[]
        for mult in partitions(q):
            if len(mult)==1: continue
            pair=sum(mult[i]*mult[j] for i in range(len(mult)) for j in range(i+1,len(mult)))
            require(pair>=q-1,'Minimal nontrivial self-adjoint orbit dimension')
            if q<=5:
                for beta in [1,2]:
                    require(orbit_rank(q,mult,beta==2)==beta*pair,'Infinitesimal orbit-rank identity')
                    rankcases+=1
            records.append({'multiplicities':mult,'real':pair,'complex':2*pair,'quaternionic':4*pair})
        require(min(t['real'] for t in records)==q-1,'Sharp minimum over spectral strata')
        dims[str(q)]=records
    counts['tangent_rank_cases']=rankcases
    witness['self_adjoint_orbit_strata']=dims
    if negative=='generic-orbit-exponent':
        require(3==min(x['real'] for x in dims['3']),'Generic orbit dimension is not the uniform minimum')
    if negative=='fixed-vector-small-ball':
        require(R(1,1)<=R(1,100)**2,'A fixed orbit does not satisfy a positive small-ball exponent')

    x,y,z=sp.symbols('x y z');r2=x*x+y*y+z*z
    zonal=[z,(3*z*z-r2)/2,(5*z**3-3*z*r2)/2,(35*z**4-30*z*z*r2+3*r2*r2)/8]
    ranks=[]
    for f in zonal:
        f=sp.expand(f)
        require(sp.expand(sum(sp.diff(f,t,2) for t in [x,y,z]))==0,'Harmonic seed')
        images=[sp.expand(y*sp.diff(f,z)-z*sp.diff(f,y)),sp.expand(z*sp.diff(f,x)-x*sp.diff(f,z)),sp.expand(x*sp.diff(f,y)-y*sp.diff(f,x))]
        monom=sorted(set().union(*(sp.Poly(g,x,y,z).monoms() for g in images)))
        M=sp.Matrix([[sp.Poly(g,x,y,z).coeff_monomial(m) for g in images] for m in monom])
        require(M.rank()==2,'Zonal stabilizer tangent rank');ranks.append(M.rank())
    counts['zonal_harmonic_degrees']=len(ranks)
    witness['zonal_tangent_ranks']=ranks

    c,v=R(-3,5),R(4,5)
    rotations=[sp.Matrix([[1,0,0],[0,c,-v],[0,v,c]]),sp.Matrix([[c,0,v],[0,1,0],[-v,0,c]])]
    verts=[sp.Matrix(t)/sp.sqrt(3) for t in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
    V=sp.Matrix.hstack(*verts);D=3;lam=R(1,2*D)
    require(V*sp.ones(4,1)==sp.zeros(3,1),'Centered regular simplex')
    require(V*V.T==R(4,3)*sp.eye(3),'Simplex covariance')
    def bary(a):
        return sp.Matrix([[sp.simplify((1+D*(vv.T*a)[0])/4) for vv in verts]])
    T=[]
    for U in rotations:
        rows=sp.Matrix.vstack(*(bary(lam*U*vv) for vv in verts))
        if negative=='unnormalized-sign-row': rows[0,0]+=R(1,9)
        require(rows*sp.ones(4,1)==sp.ones(4,1),'Sign-simulation row must normalize')
        require(all(a>=0 for a in rows),'Nonnegative sign-simulation row')
        require(rows*V.T==lam*V.T*U.T,'One common sign-simulation update')
        T.append(rows)
    count=0
    for n in range(6):
        for word in itertools.product(range(2),repeat=n):
            U=sp.eye(3);A=sp.eye(4)
            for j in word: U=rotations[j]*U;A=A*T[j]
            for seed in verts:
                actual=bary(lam*seed)*A*V.T
                desired=(lam**(n+1)*U*seed).T
                require((actual-desired).applyfunc(sp.simplify)==sp.zeros(1,3),'Exact wordwise attenuated coefficient')
                count+=1
    if negative=='attenuation-is-exact-numeric':
        require(lam**4==R(1,10),'Sign preservation does not preserve the original numerical amplitude')
    counts['sign_simulation_words_and_seeds']=count
    witness['sign_simulator']={'dimension':3,'labels':4,'lambda':str(lam),
        'rows':[[[str(a) for a in row] for row in mat.tolist()] for mat in T],
        'probability_bias':'lambda^(N+1)*<e_j,U_w x>/2'}

    # The direct-sum construction is a mixture, not a free selector or product law.
    constituents=[{'d':3,'s':2},{'d':8,'s':4},{'d':1,'s':0}]
    total=sum(a['d'] for a in constituents);rho=R(1,8*total)
    weights=[R(a['d'],total) for a in constituents]
    require(sum(weights)==1,'Paid branch probabilities')
    require(max(a['s'] for a in constituents)==4,'Constituent maximum includes nontrivial summands')
    if negative=='minimum-across-constituents':
        require(min(a['s'] for a in constituents)==4,'A fixed summand cannot erase a hard nontrivial constituent')
    for i,a in enumerate(constituents):
        signal=rho/weights[i]
        if negative=='missing-branch-amplification' and i==1: signal=rho
        require(weights[i]*signal==rho,'Branch reweighting must reproduce the original coefficient')
        require(signal<=R(1,8*a['d']),'Each branch satisfies its inradius signal constraint')
    witness['direct_sum']={'dimensions':[a['d'] for a in constituents],'least_orbit_dimensions':[2,4,0],
        'weights':list(map(str,weights)),'signal':str(rho),'width_exponent':2,'charged_label_count':'sum of branch label counts'}
    counts['paid_branch_identities']=len(constituents)

    # Quaternionic trace: only its real part is the real Hilbert inner product.
    i=sp.Quaternion(0,1,0,0);j=sp.Quaternion(0,0,1,0)
    traceAB=i*(-j)+(-i)*j
    require(traceAB==sp.Quaternion(0,0,0,-2),'Quaternion trace counterexample')
    if negative=='quaternion-trace-is-real':
        require(traceAB.b==0 and traceAB.c==0 and traceAB.d==0,'Quaternionic matrix trace requires its real part')
    require(traceAB.a==0,'Real Hilbert trace in quaternionic self-adjoint space')
    witness['quaternion_trace']={'trace_AB':str(traceAB),'real_trace_AB':'0'}

    # These checks normalize an explicitly external spectral input; they do not prove it.
    raw=[q for q in itertools.product(range(-2,3),repeat=4) if sum(a*a for a in q)==5]
    canonical=[q for q in raw if q[0]>0 and q[0]%2==1 and all(t%2==0 for t in q[1:])]
    require(len(raw)==48 and len(canonical)==6,'Norm-five quaternion parity representatives')
    require(set(canonical)=={(1,2,0,0),(1,-2,0,0),(1,0,2,0),(1,0,-2,0),(1,0,0,2),(1,0,0,-2)},'Six generators with inverse pairing')
    norm2=(2*sp.sqrt(5)/6)**2;gap=1-norm2
    if negative=='unsquared-gap': gap=1-sp.sqrt(5)/3
    require(sp.simplify(gap-R(4,9))==0,'Squared norm gap is 4/9')
    witness['arithmetic_normalization']={'representatives':canonical,'unnormalized_norm_upper':'2 sqrt(5)',
        'normalized_norm_upper':'sqrt(5)/3','squared_gap':'4/9',
        'spectral_inequality_status':'EXTERNAL theorem, not a finite-test output',
        'original_LPS_number_verified':False,
        'explicit_numbered_restatement':'Pisier, Quadratic forms in unitary operators, Theorem 3(ii)'}
    counts['norm_five_quaternions']=len(raw)
    counts['selected_inverse_representatives']=len(canonical)
    return {'schema':'gtf39.checks/1','exact_counts':counts,
            'analytic_claims':{'irreducible_exponent':'min_unit dim(G orbit)/2',
            'reducible_exponent':'max_nontrivial_irreducible min_unit dim(G orbit)/2',
            'full_gap_required':True,'fixed_small_signal_and_error':True,
            'uniform_orbit_bound':'proved by compact differential charts, not finite sampling',
            'old_projective_signal_range_preserved':True},
            'scope':'Exact finite algebra, model distinctions and representative stochastic rows; not independent proof certification, spectral-gap computation or priority clearance.'},witness

def main():
    p=argparse.ArgumentParser();p.add_argument('--negative-control');p.add_argument('--export',type=Path);a=p.parse_args()
    report,w=calculate(a.negative_control)
    if a.export:
        a.export.parent.mkdir(parents=True,exist_ok=True)
        a.export.write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__': main()
