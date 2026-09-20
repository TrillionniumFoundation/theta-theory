#!/usr/bin/env python3
"""Exact finite checks for displayed A2 v104 algebra; not formal proof verification."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening/article/v104/paper.tex'


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def subsets(n: int) -> list[tuple[int, ...]]:
    return [tuple(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]


def endpoint_check(e: int) -> dict:
    k = e + 1
    B = s.eye(e).col_join(-s.ones(1, e))
    C = (3 * s.eye(e) + s.ones(e)) / 4
    A = s.eye(k) + B * C.inv() * B.T
    H = {}
    cones = 0
    for I in subsets(e):
        BI = B[:, list(I)]
        CII = C.extract(I, I)
        P = BI * CII.inv() * BI.T if I else s.zeros(k)
        H[I] = A - P
        z = s.Matrix([int(i in I) for i in range(e)])
        w = s.Matrix([int(i not in I) for i in range(e)])
        y = -C * z + w
        shift = 1 + sum(abs(a) for a in y)
        x = s.Matrix([a + shift for a in y] + [shift])
        require(all(a > 0 for a in x), 'Positive witness failed')
        require(B.T*x + C*z == w, 'KKT witness failed')
        if I:
            require(-CII.inv()*BI.T*x == z[list(I), :], 'Active inverse failed')
        value = (x.T*A*x + 2*x.T*B*z + z.T*C*z)[0]
        require(value == (x.T*H[I]*x)[0], 'Value formula failed')
        cones += 1
    require(len({tuple(M) for M in H.values()}) == 2**e, 'Non-distinct Hessians')
    ordered_pairs = 0
    for I in H:
        for J in H:
            PI, PJ = A-H[I], A-H[J]
            if set(I).issubset(J):
                require((H[I]-H[J]).rank() == len(J)-len(I), 'Lattice rank failed')
            else:
                witnesses = PJ.nullspace()
                require(any((v.T*PI*v)[0] > 0 for v in witnesses), 'Order counter-witness failed')
            ordered_pairs += 1
    U = B  # diag(C)=1, and orientation is read on the empty-active cone.
    Uplus = (U.T*U).inv()*U.T
    reconstructed = (Uplus*(A-H[tuple(range(e))])*Uplus.T).inv()
    require(reconstructed == C, 'Normalized reconstruction failed')
    require((A-H[tuple(range(e))]).rank() == e, 'Minimal dimension witness failed')
    D = s.diag(*range(1, e+1))
    Bg, Cg = B*D, D*C*D
    for I in H:
        if I:
            Bgi = Bg[:, list(I)]
            Hg = A-Bgi*Cg.extract(I,I).inv()*Bgi.T
        else:
            Hg = A
        require(Hg == H[I], 'Positive scaling invariance failed')
    return {'endpoint_dimension': e, 'visible_cones': cones,
            'ordered_pair_checks': ordered_pairs, 'normalized_reconstruction': True,
            'minimal_rank': e, 'positive_scaling': True}


def native_check(k: int) -> dict:
    unit = [s.eye(k)[:, i] for i in range(k)]
    Z = unit + [unit[i]+unit[j] for i in range(k) for j in range(i+1,k)]
    m = len(Z)
    a = s.Rational(1, 2*m)
    probabilities = [a/2]*(2*m) + [s.Rational(1,2)]
    require(sum(probabilities)==1 and all(p>0 for p in probabilities), 'Probability normalization')
    L, D = s.zeros(2*m+1,m), s.zeros(2*m+1,k)
    for j,z in enumerate(Z):
        L[2*j,j]=L[2*j+1,j]=s.Rational(1,2)
        L[-1,j]=-1
        D[2*j,:]=z.T
        D[2*j+1,:]=-z.T
    W=s.diag(*[1/p for p in probabilities])
    require(L.T*W*D == s.zeros(m,k), 'Nuisance orthogonality')
    Q = 4*sum((z*z.T/a for z in Z), s.zeros(k))
    require(D.T*W*D == Q, 'Native information factor')
    vect=lambda M:s.Matrix([M[i,j] for i in range(k) for j in range(i,k)])
    tensors=s.Matrix.hstack(*[vect(z*z.T) for z in Z])
    require(tensors.rank()==k*(k+1)//2, 'Native full dimension')
    for d in range(1,k+1):
        require(Q[:d,:d].det()>0, 'Real positivity')
    return {'retained_dimension':k,'native_dimension':tensors.rank(),
            'normalized_secant_dimension':tensors.rank()-1,
            'sharp_query_count':tensors.rank(),'positive_probabilities':True,
            'nuisance_cross_block_zero':True}


def collision_check() -> dict:
    q=s.symbols('q', positive=True)
    # lambda=1, t=q^2. Square-root branches are checked symbolically.
    t=q**2
    for sigma,tau in itertools.product((-1,1),repeat=2):
        u=sigma*s.sqrt(2*t-2*t**2)
        v=tau*s.sqrt(2*t**2)
        x,y=(u+v)/2,(u-v)/2
        require(s.simplify(x*x+y*y-t)==0,'Collision fast equation 1')
        require(s.simplify(x*y-(t/2-t**2))==0,'Collision fast equation 2')
    x,y=s.symbols('x y')
    F=s.Matrix([x*x+y*y,x*y])
    require(s.expand(F.jacobian([x,y]).det())==2*(x*x-y*y),'Discriminant determinant')
    # Verify the slow degree-six bound, not only the fast inverse identities.
    # On the prescribed tube, |u| is comparable to t^(1/2) and |v| to t.
    u,v=s.symbols('u v', nonzero=True)
    gx,gy=(u+v)/2,(u-v)/2
    slow=s.Matrix([gx**6,gx**3*gy**3,gy**6])
    invfast=s.Matrix([[1/(2*u),1/u],[1/(2*v),-1/v]])
    first=slow.jacobian([u,v])*invfast
    second=s.Matrix(list(first)).jacobian([u,v])*invfast
    def weight_order(expr):
        terms=s.Add.make_args(s.expand(expr))
        orders=[]
        for term in terms:
            if term==0:
                continue
            powers=term.as_powers_dict()
            eu,ev=powers.get(u,0),powers.get(v,0)
            require(s.simplify(term/u**eu/v**ev).free_symbols==set(),
                    'Derivative is not the asserted Laurent polynomial')
            orders.append(s.Rational(eu,2)+ev)
        return min(orders) if orders else s.oo
    require(min(weight_order(g) for g in slow)>=3,'Slow residual order')
    require(min(weight_order(g) for g in first)>=s.Rational(3,2),'Fast slope order')
    require(min(weight_order(g) for g in second)>=-s.Rational(1,2),'Fast second derivative order')
    return {'lambda':1,'four_exact_inverse_branches':True,
            'det_DF':'2*(x^2-y^2)','tested_homogeneous_degree':6,
            'c_over_radius_exponent':'1','radius_times_M_exponent':'3/2'}


def clock_check() -> dict:
    z=s.symbols('z')
    f1=(z-1)**2
    f2=(z-2)**2
    clocks=list(range(4,9))
    for i in clocks:
        require(any(f1.subs(z,j)*f2.subs(z,i)!=f2.subs(z,j)*f1.subs(z,i)
                    for j in clocks),'Existential pair missing')
    return {'example_clocks':clocks,'for_each_i_exists_j':True,
            'universal_pair_claim_used':False}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'revisions/a2-v104/EXACT_DIAGNOSTICS.json')
    args=parser.parse_args()
    record={'status':'passed','arithmetic':'exact sympy rational and symbolic arithmetic',
            'sympy_version':s.__version__,'source_sha256':hashlib.sha256(PAPER.read_bytes()).hexdigest(),
            'principal_source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in [PAPER,*sorted((PAPER.parent/'parts').glob('*.tex'))]},
            'endpoint_tests':[endpoint_check(e) for e in range(1,5)],
            'native_tests':[native_check(k) for k in range(1,6)],
            'ramified_collision':collision_check(),'clock_quantifier':clock_check(),
            'scope':'Finite displayed algebra and constructed instances only. Not formal verification of any universal theorem, not statistical simulation, not a full native archive receipt.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':'passed','output':str(args.output)}))


if __name__=='__main__':
    main()
