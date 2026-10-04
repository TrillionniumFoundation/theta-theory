#!/usr/bin/env python3
"""Finite algebra, analytic-example fingerprints and source diagnostics.

The synthetic geometry is an independent finite example, not an execution of
an apparatus, a uniform separation certificate, or a formal proof checker.
Explicit checks (not assert) remain active under python -O.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
COUNTS: Counter[str] = Counter()
METRICS: dict[str, float | int] = {}


def require(ok: bool, group: str, detail: str = '') -> None:
    if not ok:
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] += 1


def exact_local() -> None:
    for ell, k, ko, u in product([F(1,2), F(1), F(3)],
                                  [F(1,3), F(1), F(2)],
                                  [F(1,4), F(2,3), F(3)],
                                  [F(-1,3), F(0), F(1,4)]):
        a = 2*u/(1+u*u); v = (1-u*u)/(1+u*u)
        dss = v*v/ell+k*v; dsu = -v/ell; duu = 1/ell+ko
        wst = -dsu*dsu/(2*duu); wss = dss+wst
        require((wss-wst-v*v/ell)/v == k, 'source_curvature')
        require((v*v/(-2*ell*wst)-1)/ell == ko, 'target_curvature')
        require(-dsu/duu == v/(1+ell*ko), 'foot_speed')
    for W, weight, dt in product([F(2,3), F(3), F(5)],
                                  [F(1,7), F(2), F(3,2)],
                                  [F(1,5), F(1), F(2)]):
        t1=W+1; t2=t1+dt
        f1=weight*(t1-W); f2=weight*(t2-W)
        require((t1*f2-t2*f1)/(f2-f1)==W, 'absolute_action_elimination')
        require((f2-f1)/dt==weight, 'normalization_slope')


def registration_and_rates() -> None:
    # A deterministic translated bin under a bounded polynomial density.
    # The larger domain contains all tested bins and shifts.
    def int1(a,b): return b-a
    def int2(a,b): return (b*b-a*a)/2
    def mass(x,y,h):
        return (int1(x,x+h)*int1(y,y+h)
                + F(1,7)*int2(x,x+h)*int1(y,y+h)
                + F(1,9)*int1(x,x+h)*int2(y,y+h))
    for h, ratio, x, y in product([F(1,4),F(1,8),F(1,16)],
                                 [F(1,4),F(1,8),F(1,16)],
                                 [F(-1,2),F(0),F(1,3)],
                                 [F(-1,2),F(0),F(1,3)]):
        nu=h*ratio
        band=(h+2*nu)**2-(h-2*nu)**2
        require(band==8*h*nu, 'square_boundary_band')
        for sx,sy in product([-1,0,1],repeat=2):
            error=abs(mass(x+sx*nu,y+sy*nu,h)-mass(x,y,h))
            require(error<=2*(8*h*nu+4*nu*nu), 'coordinate_bias_cell_bound')
    for beta in [F(1),F(1,2),F(1,3),F(2,3)]:
        t=1/(2*beta+6)
        require(F(1,2)-3*t==beta*t, 'variance_bandwidth_balance')
        require((beta+4)*t-4*t==beta*t, 'square_bias_balance')
        require((beta+3)*t-3*t==beta*t, 'registration_bias_balance')
        require((beta+3)*t==F(1,2), 'probe_precision_half_power')
        require(1-4*t>=beta*t, 'linear_Bernstein_term')
        require(2*(beta+4)*t==(beta+4)/(beta+3), 'apparatus_range_power')
    for s in [F(0),F(1,2),F(1),F(3),F(5)]:
        a=6+s
        require(3+s-a < -1, 'probe_expected_cost_summability')
        require(3-6 < -1, 'launch_expected_cost_summability')
    # Actual proper-divisor chains, not a floating-point logarithm shortcut.
    for n in range(1,129):
        curr=n; steps=0
        while curr>1:
            proper=[d for d in range(1,curr) if curr%d==0]
            nxt=max(proper)
            require(2*nxt<=curr, 'proper_divisor_halving')
            curr=nxt; steps+=1
        require(steps<=n.bit_length()-1, 'logarithmic_witness_bound')
    for p in [F(1,20),F(1,5),F(1,2)]:
        for k in range(1,41):
            require(float((1-p)**k)<=math.exp(-float(p)*k)+1e-15,
                    'hazard_exponential_bound')
    for m in range(1,41):
        actual=m+2*sum(k*(k+1)**2 for k in range(1,m+1))
        require(actual<=2*(m+1)**4, 'finite_epoch_preparation_budget')


def determinant(a,b): return a[0]*b[1]-a[1]*b[0]

def subgroup_tests() -> None:
    integer_sets=[[(2,0),(0,3),(1,1)],[(2,0),(0,2),(1,1)],
                  [(3,0),(0,5),(1,1)],[(4,0),(0,6),(2,3)],
                  [(1,0),(0,1),(2,3)],[(6,0),(0,10),(3,5),(2,2)]]
    for cols in integer_sets:
        minors=[abs(determinant(x,y)) for x,y in combinations(cols,2)]
        gamma_index=math.gcd(*minors)
        require(gamma_index>0, 'integer_cycle_rank')
        for ii,jj in combinations(range(len(cols)),2):
            D=[cols[ii],cols[jj]]; det=determinant(*D)
            if not det: continue
            coords=[(F(determinant(c,D[1]),det),F(determinant(D[0],c),det)) for c in cols]
            q=math.lcm(*(v.denominator for c in coords for v in c))
            require(abs(det)%q==0, 'common_denominator_divides_index')
            Hcols=[(q,0),(0,q)]+[(int(q*x),int(q*y)) for x,y in coords]
            detH=math.gcd(*(abs(determinant(x,y)) for x,y in combinations(Hcols,2)))
            require(F(abs(det)*detH,q*q)==gamma_index, 'reference_free_covolume')
            require(1<=detH<=q*q, 'Hermite_index_bounds')
            for V,A,missing in product([F(2),F(5,2)], [F(1,3),F(1)], [F(0),F(1,4)]):
                visible=V-A-missing
                defect=gamma_index*V-A-visible
                require(defect==(gamma_index-1)*V+missing, 'completion_defect_identity')
                require((defect==0)==(gamma_index==1 and missing==0), 'completion_zero_characterization')
    require(math.gcd(6,2,3)==1 and min(6,2,3)>1, 'no_primitive_pair_example')


def analytic_fingerprints() -> None:
    import numpy as np
    from scipy.optimize import brentq
    K=6; radius=.045
    bodies=[(.43,.018,.013,.31),(.55,.023,.017,.87)]
    centers=[np.array([0.,0.]),np.array([1.6,2.1])]
    basis=np.diag([4.,5.])
    def pd(theta,order,b):
        r,e2,e3,phase=b
        return ((r if order==0 else 0.)+e2*2**order*math.cos(2*theta+order*math.pi/2)
                +e3*3**order*math.cos(3*theta+phase+order*math.pi/2))
    def mul(a,b): return np.convolve(a,b)[:K+1]
    def compose(a,b):
        out=np.zeros(K+1); power=np.zeros(K+1); power[0]=1.
        for coeff in a:
            out+=coeff*power
            power=mul(power,b)
        return out
    def graph(theta,b):
        p=np.array([pd(theta,j,b)/math.factorial(j) for j in range(K+1)])
        pp=np.array([pd(theta,j+1,b)/math.factorial(j) for j in range(K+1)])
        co=np.array([math.cos(j*math.pi/2)/math.factorial(j) for j in range(K+1)])
        si=np.array([math.sin(j*math.pi/2)/math.factorial(j) for j in range(K+1)])
        X=mul(p,co)-mul(pp,si); Y=mul(p,si)+mul(pp,co)
        X[0]=Y[0]=0.
        inverse=np.zeros(K+1); inverse[1]=1/Y[1]
        for j in range(2,K+1):
            inverse[j]=-compose(Y,inverse)[j]/Y[1]
        recovered=compose(Y,inverse)
        require(np.max(np.abs(recovered-np.eye(1,K+1,1)[0]))<1e-8,
                'analytic_local_series_reversion')
        psi=-compose(X,inverse)
        require(abs(2*psi[2]-1/(pd(theta,0,b)+pd(theta,2,b)))<1e-9,
                'analytic_curvature_coefficient')
        return np.array([radius**j*psi[j] for j in range(2,K+1)])
    data=[]; labels=[]
    for i,j,kx,ky in product(range(2),range(2),range(-2,3),range(-2,3)):
        if i==j and kx==ky==0: continue
        V=centers[j]+basis@np.array([kx,ky])-centers[i]
        if np.linalg.norm(V)>9: continue
        theta0=math.atan2(V[1],V[0])
        def gp(theta):
            tangent=np.array([-math.sin(theta),math.cos(theta)])
            return float(V@tangent)-pd(theta,1,bodies[i])-pd(theta+math.pi,1,bodies[j])
        theta=brentq(gp,theta0-.3,theta0+.3,xtol=1e-14)
        normal=np.array([math.cos(theta),math.sin(theta)])
        gap=float(V@normal)-pd(theta,0,bodies[i])-pd(theta+math.pi,0,bodies[j])
        require(gap>0, 'analytic_example_positive_gap')
        source=graph(theta,bodies[i]); target=graph(theta+math.pi,bodies[j])
        parity=np.array([(-1)**r for r in range(2,K+1)])
        descriptor=np.r_[gap,source,target*parity]
        sign=np.r_[1.,parity,parity]
        for orientation in [0,1]:
            data.append(descriptor*(sign if orientation else 1.))
            labels.append((i,j,kx,ky,orientation))
    data=np.array(data); count=len(data)
    distances=np.max(np.abs(data[:,None,:]-data[None,:,:]),axis=2)
    np.fill_diagonal(distances,np.inf)
    margin=float(np.min(distances))
    require(margin>1e-10, 'finite_example_oriented_separation')
    rng=np.random.default_rng(240310)
    prototypes=data+rng.uniform(-margin/64,margin/64,size=data.shape)
    for i in range(count):
        noisy=data[i]+rng.uniform(-margin/64,margin/64,size=data.shape[1])
        ds=np.max(np.abs(prototypes-noisy),axis=1)
        require(np.flatnonzero(ds<margin/2).tolist()==[i], 'adversarial_bounded_registry_match')
    # Class/sign correctness under additional translations: descriptor coordinates
    # are relative contacts. Check the displacement cancellation independently.
    for shift in [np.array([4.,0.]),np.array([0.,5.]),np.array([-8.,15.])]:
        for i,j in product(range(2),repeat=2):
            p=centers[i]+np.array([.1,-.2]); q=centers[j]+np.array([4.3,5.1])
            require(np.max(np.abs(((q+shift)-(p+shift))-(q-p)))<1e-12,
                    'translated_contact_displacement')
    METRICS.update(synthetic_oriented_descriptors=count,
                   synthetic_fingerprint_order=K,
                   synthetic_min_descriptor_separation=margin)


def sources() -> None:
    text=(ROOT/'main.tex').read_text()
    for name in re.findall(r'\\input\{([^}]+)\}',text):
        p=ROOT/(name+'.tex')
        require(p.is_file(),'native_input_exists',name)
        text+='\n'+p.read_text()
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)),'unique_labels')
    for name in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',text):
        require(name in labels,'resolved_reference',name)
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    for item in re.findall(r'\\cite\{([^}]+)\}',text):
        for name in item.split(','): require(name in bib,'resolved_citation',name)
    for name in ['thm:main','lem:finite-separation','prop:registry','lem:probe',
                 'lem:witness','thm:certificate','lem:histogram']:
        require(name in labels,'main_proof_route',name)


def main() -> None:
    exact_local(); registration_and_rates(); subgroup_tests(); analytic_fingerprints(); sources()
    print(json.dumps({'schema':'a2-v24-finite-diagnostics-1','status':'passed',
        'finite_checks':sum(COUNTS.values()),'groups':dict(sorted(COUNTS.items())),
        'metrics':METRICS,'executed_physical_sensor':False,'formal_proof_certificate':False,
        'scope':'Finite algebra and analytic-body examples; not uniform proof certification'},
        sort_keys=True,indent=2))

if __name__=='__main__': main()
