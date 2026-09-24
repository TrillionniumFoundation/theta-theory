#!/usr/bin/env python3
"""Exact finite regressions for v31. Analytic universal proofs are in the article."""
from __future__ import annotations
import argparse, itertools, json, math
from fractions import Fraction as F
from pathlib import Path
import sympy as sp


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise RuntimeError('CHECK_REJECTED: '+reason)


def rows_h(h: F, x: tuple[int,int]) -> list[tuple[F,F]]:
    return [(h,h),(h,-h),(-h,F(0)),(-h/2,h*x[0]/4),(-h/2,h*x[1]/4)]


def triangle_weights(h: F, u: F, v: F) -> list[F]:
    return [(h+u+2*v)/(4*h),(h+u-2*v)/(4*h),(h-u)/(2*h)]


def seed(d: int) -> sp.Matrix:
    r=sp.Rational
    if d==5:
        return sp.Matrix([[r(1,2),1,r(1,3),1,1],[r(1,2),0,r(1,3),1,1],
            [r(1,2),r(1,2),r(1,3),0,1],[r(1,2),r(1,2),0,r(1,3),0],
            [0,r(1,2),1,r(1,3),0],[1,r(1,2),1,r(1,3),0]])
    if d==9:
        return sp.Matrix([[1,0,0,0,0,0,0,0,1],[1,1,0,1,r(1,2),1,1,0,0],
            [1,0,1,1,r(1,2),0,1,1,0],[0,1,1,1,r(1,2),0,0,1,1],
            [0,1,1,0,r(1,2),1,0,0,0],[0,0,0,1,r(1,2),0,1,1,0],
            [1,1,0,0,r(1,2),1,1,1,0],[0,1,1,0,r(1,2),1,1,0,1],
            [0,0,1,1,r(1,2),1,0,1,1],[1,0,0,0,1,0,0,0,1]])
    raise ValueError('Only the displayed seeds d=5,9 are defined')


def as_fraction(q) -> F:
    return F(int(q.p),int(q.q))


def check(mutant: str|None=None, export: Path|None=None) -> dict:
    counts={'profile_rows':0,'seed_words':0,'conditional_means':0,'stochastic_rows':0,
            'additive_inputs':0,'rational_sampler_rows':0}
    # Analytic interval certificate is monotonic; its worst endpoint is rational.
    delta=F(1,10)
    beta=F(1,4)+delta/(2*(1-delta))+delta/(2-3*delta)
    require(beta==F(223,612),'triangle endpoint constant')
    require(F(9,20)-beta==F(131,1530)>0,'strict triangle margin')
    corners=list(itertools.product((-1,1),repeat=2))
    for h in [F(9,10),F(19,20),F(99,100),F(1)]:
        a=h/4;parent=[(-a,-a),(3*a,-a),(-a,3*a)]
        actual=[rows_h(h,x) for x in corners]
        flat=sp.Matrix([[F(1),*[q for pair in rows for q in pair]] for rows in actual])
        child=sp.Matrix([[1,*pair] for rows in actual for pair in rows])
        require(flat.rank()==3 and child.rank()==3,'cut ranks must both be three')
        for x,rows in zip(corners,actual):
            lam=[F(2-x[0]-x[1],4),F(1+x[0],4),F(1+x[1],4)]
            require(min(lam)>=0 and sum(lam)==1,'first-cut barycentric row')
            for j,(u,v) in enumerate(rows):
                # Explicit (4,3) machine.
                w=triangle_weights(h,u,v)
                require(min(w)>=0 and sum(w)==1,'three-state child row')
                dec=[(h,h),(h,-h),(-h,F(0))]
                require(tuple(sum(w[s]*dec[s][k] for s in range(3)) for k in range(2))==(u,v),'(4,3) reconstruction')
                # Explicit (3,4) machine.
                temp=[]
                for pu,pv in parent:
                    state=[(h,h),(h,-h),(-h,F(0)),(-h/2,pu),(-h/2,pv)][j]
                    four=[(1+e[0]*state[0])*(1+e[1]*state[1])/4 for e in corners]
                    require(min(four)>=0 and sum(four)==1,'four-state child row')
                    temp.append(tuple(sum(four[i]*corners[i][k] for i in range(4)) for k in range(2)))
                require(tuple(sum(lam[s]*temp[s][k] for s in range(3)) for k in range(2))==(u,v),'(3,4) reconstruction')
                if h==F(9,10):
                    require(all(F(1,20)<=(1+b*z)/2<=F(19,20) for z in (u,v) for b in (-1,1)),'full-support endpoint')
                counts['profile_rows']+=1
        if mutant=='incompatible-splice':
            illegal=triangle_weights(h,-h/2,3*a)
            require(min(illegal)>=0,'independent static minima cannot be spliced')
    # General non-binary additive encoder, checked under all input permutations.
    X=[(0,1,2),(0,1),(-1,1,2)]
    def fi(i,x):
        return ([F(x,60),F(-x,60),F(0)] if i==0 else
            [F(0),F(x,30),F(-x,30)] if i==1 else [F(-x,90),F(0),F(x,90)])
    low=[[min(fi(i,x)[s] for x in X[i]) for s in range(3)] for i in range(3)]
    c=[F(1,3)+sum(low[i][s] for i in range(3)) for s in range(3)]
    g=lambda i,x:[fi(i,x)[s]-low[i][s] for s in range(3)]
    weights=[sum(g(i,X[i][0])) for i in range(3)]
    w0=sum(c)
    require(min(c)>=0 and w0+sum(weights)==1,'additive decomposition')
    for x in itertools.product(*X):
        expected=[F(1,3)+sum(fi(i,x[i])[s] for i in range(3)) for s in range(3)]
        for order in itertools.permutations(range(3)):
            p=[v/w0 for v in c];W=w0
            for i in order:
                p=[(W*p[s]+g(i,x[i])[s])/(W+weights[i]) for s in range(3)];W+=weights[i]
            require(p==expected,'additive synthesis under a prescribed permutation')
            counts['additive_inputs']+=1
    exports={};aug={}
    for d in (5,9):
        U=seed(d);m=d+1
        V=2*U-sp.ones(m,d)
        if mutant=='center-shift': V=2*U
        require(all(-1<=v<=1 for v in V),'centering vertices in the outer cube')
        M=sp.ones(m,1).row_join(V);A=M.inv();aug[d]=(M,A)
        require(abs(M.det())=={5:32,9:12800}[d],'seed determinant')
        require(all(A[0,j]==sp.Rational(1,m) for j in range(m)),'centroid')
        require(all(sum(abs(A[i,j]) for i in range(m))==1 for j in range(m)),'absolute inverse columns')
        VF=[[as_fraction(V[s,i]) for i in range(d)] for s in range(m)]
        BF=[[as_fraction(A[i+1,s]) for i in range(d)] for s in range(m)]
        q={}
        for i in range(d):
            for x in (-1,1):
                q[i,x]=[abs(BF[s][i])+x*BF[s][i] for s in range(m)]
                if mutant=='hadamard-assumption':q[i,x]=[(1+x*VF[s][i])/m for s in range(m)]
                require(min(q[i,x])>=0 and sum(q[i,x])==1,'critical local distribution')
                for s in range(m):
                    row=[F(i,i+1)*int(s==t)+F(1,i+1)*q[i,x][t] for t in range(m)]
                    require(sum(row)==1 and min(row)>=0,'critical replacement row')
                    counts['stochastic_rows']+=1
                    D=math.lcm(*(v.denominator for v in row));b=(D-1).bit_length()
                    if D>1:
                        accepted=list(range(D+(1 if mutant=='coin-boundary' else 0)))
                        boundaries=[];cur=0
                        for v in row:cur+=int(v*D);boundaries.append(cur)
                        nout=[sum(int((boundaries[t-1] if t else 0)<=J<boundaries[t]) for J in accepted) for t in range(m)]
                        require(sum(nout)==len(accepted)==D,'rational sampler acceptance boundary')
                        require([F(v,D) for v in nout]==row,'rational sampler exact law')
                        require(F(2**b,D)*b<2*b,'rational sampler expected bits')
                        counts['rational_sampler_rows']+=1
        for x in itertools.product((-1,1),repeat=d):
            for order in [tuple(range(d)),tuple(reversed(range(d)))]:
                p=[F(1,m)]*m
                for t,i in enumerate(order,1):
                    p=[F(t-1,t)*p[s]+F(1,t)*q[i,x[i]][s] for s in range(m)]
                    if mutant=='replacement-weight':p=q[i,x[i]][:]
                require(min(p)>=0 and sum(p)==1,'streaming distribution')
                expected=[F(1,m)+sum(BF[s][i]*x[i] for i in range(d))/d for s in range(m)]
                require(p==expected,'exact barycentric query law')
                for j in range(d):
                    mean=sum(p[s]*VF[s][j] for s in range(m))
                    target=F(x[j],d)
                    if mutant=='query-factor':target=F(x[j],2*d)
                    require(mean==target,'exact conditional decoder mean')
                    counts['conditional_means']+=1
                counts['seed_words']+=1
        exports[str(d)]={'vertices':[[str(v) for v in row] for row in VF],
            'barycentric_linear_coefficients':[[str(v) for v in row] for row in BF],
            'local_distributions':{f'{i+1}:{x}':[str(v) for v in q[i,x]] for i in range(d) for x in (-1,1)},
            'rule':'T_t(s,s_prime)=(t-1)/t*1[s=s_prime]+q_t(s_prime|x_t)/t'}
    tensor_dimensions=[]
    for d,e in [(5,5),(5,9)]:
        M,A=aug[d];N,B=aug[e];K=sp.kronecker_product(M,N);I=sp.kronecker_product(A,B);m=K.rows
        require(K*I==sp.eye(m),'tensor inverse')
        require(all(I[0,j]==sp.Rational(1,m) for j in range(m)),'tensor centroid')
        require(all(sum(abs(I[i,j]) for i in range(m))==1 for j in range(m)),'tensor critical positivity')
        require(all(-1<=v<=1 for v in K),'tensor cube')
        tensor_dimensions.append(m-1)
    if export:
        export.parent.mkdir(parents=True,exist_ok=True);export.write_text(json.dumps(exports,indent=2,sort_keys=True)+'\n')
    return {'schema':'gtf31.exact/1','counts':counts,'cut_ranks':[3,3],
        'exact_pareto_profiles':[[3,4],[4,3]],'full_support_family':'9/10 <= h < 1',
        'triangle_margin':'131/1530','canonical_rank_two_compatibility':'proved analytically in manuscript',
        'online_nonhadamard_dimensions':[5,9],'online_tensor_dimensions_checked':tensor_dimensions,
        'checkpoint_RAC_equivalence':'attributed to Kondo et al., v3, Theorem 14 and Lemma 15',
        'scope':'Finite exact regressions and explicit rows, not proof of universal claims, independent verification or priority clearance.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--negative-control');parser.add_argument('--export',type=Path)
    args=parser.parse_args()
    if args.negative_control not in {None,'incompatible-splice','center-shift','hadamard-assumption','coin-boundary','replacement-weight','query-factor'}:
        parser.error('Unknown negative control')
    print(json.dumps(check(args.negative_control,args.export),indent=2,sort_keys=True))
