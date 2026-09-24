#!/usr/bin/env python3
"""Exact characteristic-zero finite checks and complete F22 linear algebra.
The universal theorems are not certified by these finite computations.
The F22 result is a fixed finite computer-assisted calculation, not a sample
used to extrapolate a formula in arbitrary dimension.
"""
from __future__ import annotations
import collections, hashlib, itertools as it, json, math, runpy
from pathlib import Path
import sympy as s
from sympy.polys.matrices import DomainMatrix
HERE=Path(__file__).resolve().parent

def require(test: bool, message: str) -> None:
    if not test: raise AssertionError(message)

def f22() -> dict:
    x,y=s.symbols('x y');a,b,c,d,e=s.symbols('a b c d e')
    vs=(e,d,c,b,a);weights=(2,2,2,1,1)
    q=a*x+b*y;r=c*x*x+d*x*y+e*y*y
    equations=s.Poly(-q**3+2*q*r,x,y).coeffs()+s.Poly(q**4-3*q*q*r+r*r,x,y).coeffs()
    mon=lambda ex:s.prod(v**i for v,i in zip(vs,ex))
    mons=lambda n:[c**i*d**j*e**k for i in range(n+1) for j in range(n+1-i) for k in [n-i-j]]
    proposed=mons(3)+[b*f for f in mons(2)]+[a*f for f in mons(2)]+[
        b*b*e-e*e,b*b*d-d*e,b*b*c-a*a*e,b**3-2*b*e,
        2*a*b*e-d*e,2*a*a*e+2*a*b*d-2*c*e-d*d,2*a*b*c-c*d,
        3*a*b*b-2*a*e-2*b*d,a*a*d-c*d,a*a*c-c*c,
        3*a*a*b-2*a*d-2*b*c,a**3-2*a*c]
    require(len(proposed)==34,'34 displayed Groebner polynomials')
    G=s.groebner(equations,*vs,order='grevlex',domain=s.QQ)
    H=s.groebner(proposed,*vs,order='grevlex',domain=s.QQ)
    require(G==H,'displayed basis and reciprocal ideal agree over QQ')
    require(len(G.polys)==34,'basis size')
    for f in proposed: require(G.reduce(f)[1]==0,'basis lies in reciprocal ideal')
    for f in equations: require(H.reduce(f)[1]==0,'reciprocal ideal lies in displayed ideal')
    pairs=0
    for p,q0 in it.combinations(G.polys,2):
        ep=p.LM(order=G.order).exponents;eq=q0.LM(order=G.order).exponents
        lcm=tuple(max(i,j) for i,j in zip(ep,eq))
        f=mon(tuple(i-j for i,j in zip(lcm,ep)))*p.as_expr()/p.LC(order=G.order)
        f-=mon(tuple(i-j for i,j in zip(lcm,eq)))*q0.as_expr()/q0.LC(order=G.order)
        require(G.reduce(s.expand(f))[1]==0,'Buchberger pair');pairs+=1
    leading=[p.LM(order=G.order).exponents for p in G.polys]
    bounds=[min(ex[i] for ex in leading if ex[i]>0 and sum(ex)==ex[i]) for i in range(5)]
    basis=[ex for ex in it.product(*(range(v) for v in bounds)) if not any(all(v>=u for v,u in zip(ex,lm)) for lm in leading)]
    weight=lambda ex:sum(i*j for i,j in zip(ex,weights))
    basis.sort(key=lambda ex:(weight(ex),ex));idx={ex:i for i,ex in enumerate(basis)};n=len(basis)
    def vec(f):
        out=s.zeros(n,1)
        for ex,value in s.Poly(G.reduce(s.expand(f))[1],*vs).terms():
            if value: out[idx[ex]]=value
        return out
    matrices=[s.Matrix.hstack(*[vec(v*mon(ex)) for ex in basis]) for v in vs]
    for A,B in it.combinations(matrices,2): require(A*B==B*A,'multiplication matrices commute')
    soc=s.Matrix.vstack(*matrices).nullspace()
    power=s.eye(n);dims=[n]
    for j in range(1,7):
        products=s.Matrix.hstack(*[A*power for A in matrices]);cols=products.columnspace()
        power=s.Matrix.hstack(*cols) if cols else s.zeros(n,0);dims.append(power.cols)
        if not cols:break
    require(dims==[22,21,16,10,5,0],'powers of the maximal ideal')
    require(len(soc)==7,'socle type')
    hilbert=dict(sorted(collections.Counter(weight(ex) for ex in basis).items()))
    require(hilbert=={0:1,1:2,2:6,3:6,4:7},'weighted Hilbert function')
    complexes={}
    for p in range(6):
        for subset in it.combinations(range(5),p):
            for j,ex in enumerate(basis):
                w=sum(weights[h] for h in subset)+weight(ex)
                complexes.setdefault((p,w),[]).append((subset,j))
    ranks={};differentials={}
    for (p,w),columns in sorted(complexes.items()):
        if not p:ranks[p,w]=0;continue
        rows=complexes.get((p-1,w),[]);ri={v:i for i,v in enumerate(rows)};entries={}
        for j,(subset,h) in enumerate(columns):
            for l,v in enumerate(subset):
                target=subset[:l]+subset[l+1:]
                for k,co in enumerate(matrices[v][:,h]):
                    if co: entries[ri[target,k],j]=(-1)**l*co
        A=s.MutableSparseMatrix(len(rows),len(columns),entries)
        ranks[p,w]=DomainMatrix.from_Matrix(A).rank();differentials[p,w]=A
        if (p-1,w) in differentials:
            require(differentials[p-1,w]*A==s.zeros(differentials[p-1,w].rows,A.cols),'Koszul differential squares to zero')
    betti={}
    for (p,w),columns in sorted(complexes.items()):
        value=len(columns)-ranks.get((p,w),0)-ranks.get((p+1,w),0)
        if value:betti[p,w]=value
    expected={(0,0):1,(1,3):4,(1,4):5,(2,5):4,(2,6):12,(2,7):12,
              (3,8):21,(3,9):20,(3,10):1,(4,10):21,(4,11):8,(5,12):7}
    require(betti==expected,'entire weighted Betti table')
    z=s.Symbol('z');num=sum((-1)**p*v*z**w for (p,w),v in betti.items())
    require(s.expand(num-sum(v*z**w for w,v in hilbert.items())*(1-z)**2*(1-z*z)**3)==0,'Hilbert numerator identity')
    return {'pass':True,'coefficient_field':'QQ','all_S_pairs_checked':pairs,
        'groebner_basis':[str(p.as_expr()) for p in G.polys],
        'variable_order':[str(v) for v in vs],'variable_weights':weights,
        'standard_basis':[str(mon(ex)) for ex in basis],
        'weighted_hilbert':hilbert,'length':n,
        'maximal_ideal_power_dimensions':dims,'local_hilbert':[dims[i]-dims[i+1] for i in range(len(dims)-1)],
        'socle_basis':[str(sum(v*mon(ex) for ex,v in zip(basis,col))) for col in soc],
        'multiplication_matrices':{str(v):[[i,j,str(A[i,j])] for i in range(n) for j in range(n) if A[i,j]] for v,A in zip(vs,matrices)},
        'koszul_ranks':[{'homological_degree':p,'weight':w,'chain_dimension':len(complexes[p,w]),'rank':v} for (p,w),v in sorted(ranks.items())],
        'betti':[{'homological_degree':p,'weight':w,'value':v} for (p,w),v in betti.items()]}

def block_numerators() -> int:
    z=s.Symbol('z');cases=0
    for n in range(1,6):
        for m in range(1,4):
            for t in range(n):
                numerator=s.Integer(1)
                for i in range(1,n*m-t+1):
                    val=sum(math.comb(n,b)*math.comb(b-1,t)*s.Poly(((1+z)**m-1)**b,z).nth(i+t) for b in range(t+1,min(n,i+t)+1))
                    numerator+=(-1)**i*val*z**(i+t)
                series=sum(math.comb(n,j)*((1-z)**(-m)-1)**j for j in range(t+1))
                require(s.cancel(numerator-series*(1-z)**(n*m))==0,'block Betti/Hilbert numerator')
                cases+=1
    return cases

def apolar_small() -> list:
    rows=[]
    for d in range(1,4):
        xs=s.symbols(f'x0:{d}');pairs=list(it.combinations_with_replacement(range(d),2))
        ys=s.symbols(f'y0:{len(pairs)}')
        Q=sum(v*xs[i]*xs[j] for v,(i,j) in zip(ys,pairs))
        equations=s.Poly(Q*Q,*xs).coeffs()
        G=s.groebner(equations,*ys,order='grevlex',domain=s.QQ)
        leading=[p.LM(order=G.order).exponents for p in G.polys]
        bounds=[min(ex[i] for ex in leading if ex[i]>0 and sum(ex)==ex[i]) for i in range(len(ys))]
        standard=[ex for ex in it.product(*(range(v) for v in bounds)) if not any(all(v>=u for v,u in zip(ex,lm)) for lm in leading)]
        h=dict(sorted(collections.Counter(sum(ex) for ex in standard).items()))
        expected={p:math.comb(d+1,p)*math.comb(d+1,p+1)//(d+1) for p in range(d+1)}
        require(h==expected,'symmetric determinant apolar Hilbert')
        require(len(standard)==math.comb(2*d+2,d+1)//(d+2),'Catalan length')
        rows.append({'d':d,'polynomial_hilbert':h,'length':len(standard)})
    return rows

def main() -> None:
    inherited=runpy.run_path(str(HERE.parent/'v153'/'check_v153.py'),run_name='v153_regression_import')
    for name in ('squarefree_checks','binary_checks','fitting_checks','multivariate_checks'):
        inherited[name]()
    data={'revision':154,'all_checks_pass':True,
          'v153_families_rerun':inherited['results'],
          'F22':f22(),'block_numerator_parameter_cases':block_numerators(),
          'apolar_small_cases':apolar_small(),
          'ternary_fibre_length_lower_bound':math.comb(18,9)//10,
          'historical_28_checks_rerun':False,
          'general_proofs_certified_by_computation':False,
          'F22_is_a_fixed_exact_computer_assisted_calculation':True,
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'EXACT_CHECKS_V154.json').write_text(json.dumps(data,indent=2)+'\n')
    print('All listed exact checks passed; F22 length 22, type 7, total Betti numbers 1,9,28,42,29,7.')

if __name__=='__main__':main()
