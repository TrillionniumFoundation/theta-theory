#!/usr/bin/env python3
"""Exact finite diagnostics for A1 v34. Not a formal proof or optimizer."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import factorial
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


COMMANDS = ((F(1, 3), F(2, 3)), (F(3, 4), F(1, 4)))
NU = (F(1, 3), F(2, 3))


def report(k: tuple[F, F], g: tuple[F, F], x: int) -> F:
    return g[x] * k[x] if x < 2 else sum((1-g[z])*k[z] for z in range(2))


def support_checks() -> dict:
    matrices = []
    overlap = sum(NU[c]*min(1-g[0], 1-g[1]) for c,g in enumerate(COMMANDS))
    for choices in product(range(2), repeat=6):
        a = [[F(0) for _ in range(2)] for _ in range(2)]
        for k,c in product(range(2), range(2)):
            a[k][choices[3*c+k]] += NU[c]*COMMANDS[c][k]
            a[k][choices[3*c+2]] += NU[c]*(1-COMMANDS[c][k])
        require(all(sum(row)==1 for row in a), 'garbling row sums')
        require(sum(min(a[0][j],a[1][j]) for j in range(2)) >= overlap,
                'common submeasure not preserved')
        matrices.append(a)
    mk = [sum(NU[c]*COMMANDS[c][k] for c in range(2)) for k in range(2)]
    for coeff in product((-1,0,1), repeat=4):
        C = [coeff[:2],coeff[2:]]
        explicit = max(sum(C[k][j]*a[k][j] for k,j in product(range(2),repeat=2))
                       for a in matrices)
        formula = sum(mk[k]*max(C[k]) for k in range(2)) + sum(
            NU[c]*max(sum((1-g[k])*C[k][j] for k in range(2)) for j in range(2))
            for c,g in enumerate(COMMANDS))
        require(explicit == formula, 'support mismatch')
    return {'deterministic_postprocessings':64,'reward_tables':81,
            'overlap_lower_bound':str(overlap),'passed':True}


def transition(n: int, i: int, c: int, x: int) -> tuple[F,F,F]:
    v = F(((n+1)*(i+2)+2*c+x)%7,8)
    return v,1-v,F(0)  # third label is deliberately unreachable


def occupancy_check(name: str, cells: tuple[tuple[F,F],tuple[F,F]]) -> dict:
    mu=(F(2,5),F(3,5)); M=3; N=4
    q=[[F(1),F(0),F(0)] for _ in cells]
    coeff=[{(0,0):F(1)}, {}, {}]
    # histories store command probability, likelihood at each latent atom,
    # and the conditional label distribution given this full history.
    histories=[(F(1),(F(1),F(1)),(F(1),F(0),F(0)))]
    rows=[]
    for n in range(1,N):
        A=[[[F(0) for _ in range(M)] for _ in range(2)] for _ in range(M)]
        for i,k,j in product(range(M),range(2),range(M)):
            A[i][k][j]=sum(NU[c]*(g[k]*transition(n,i,c,k)[j]
                           +(1-g[k])*transition(n,i,c,2)[j])
                           for c,g in enumerate(COMMANDS))
        q=[[sum(q[t][i]*cells[t][k]*A[i][k][j]
                for i,k in product(range(M),range(2))) for j in range(M)]
                for t in range(2)]
        next_coeff=[{} for _ in range(M)]
        for i,k,j in product(range(M),range(2),range(M)):
            for alpha,v in coeff[i].items():
                beta=tuple(alpha[z]+int(z==k) for z in range(2))
                next_coeff[j][beta]=next_coeff[j].get(beta,F(0))+v*A[i][k][j]
        coeff=next_coeff
        for alpha in ((a,n-a) for a in range(n+1)):
            require(sum(c.get(alpha,F(0)) for c in coeff)==F(factorial(n),
                    factorial(alpha[0])*factorial(alpha[1])), 'multinomial identity')
        for t,j in product(range(2),range(M)):
            polynomial=sum(v*cells[t][0]**a[0]*cells[t][1]**a[1]
                           for a,v in coeff[j].items())
            require(polynomial==q[t][j],'formal occupancy evaluation')
        new_histories=[]
        for prob,L,dist in histories:
            for c,g in enumerate(COMMANDS):
                for x in range(3):
                    Lnew=tuple(L[t]*report(cells[t],g,x) for t in range(2))
                    dnew=tuple(sum(dist[i]*transition(n,i,c,x)[j] for i in range(M))
                               for j in range(M))
                    new_histories.append((prob*NU[c],Lnew,dnew))
        histories=new_histories
        for t,j in product(range(2),range(M)):
            direct=sum(prob*L[t]*dist[j] for prob,L,dist in histories)
            require(q[t][j]==direct,'history versus coefficient recursion')
        # One physical future success query: N-n accepted reports of cell 0
        # at a fixed command whose first coordinate is 1/2.
        h=tuple((F(1,2)*cells[t][0])**(N-n) for t in range(2))
        w=[sum(mu[t]*q[t][j] for t in range(2)) for j in range(M)]
        b=[sum(mu[t]*q[t][j]*h[t] for t in range(2)) for j in range(M)]
        decoder=[b[j]/w[j] if w[j] else F(0) for j in range(M)]
        B=F(0); direct_risk=F(0); zero_evidence=0
        for prob,L,dist in histories:
            evidence=sum(mu[t]*L[t] for t in range(2))
            if not evidence:
                zero_evidence+=1
                continue
            target=sum(mu[t]*L[t]*h[t] for t in range(2))/evidence
            B+=prob*evidence*target**2
            direct_risk+=prob*evidence*sum(dist[j]*(target-decoder[j])**2 for j in range(M))
        formula=B-sum(b[j]**2/w[j] if w[j] else F(0) for j in range(M))
        require(direct_risk==formula and formula>=0,'centroid risk mismatch')
        require(w[2]==0 and b[2]==0, 'zero occupancy missing')
        rows.append({'checkpoint':n,'histories':len(histories),'zero_evidence_histories':zero_evidence,
                     'zero_occupancy_labels':sum(v==0 for v in w),'risk':str(formula)})
    if name=='zero_evidence_cells':
        require(rows[-1]['zero_evidence_histories']>0,'zero evidence not exercised')
    return {'model':name,'checkpoints':rows,'passed':True}


def tie_checks() -> dict:
    # F0=g0, F1=g1, F2=(g0+g1)/2: diagonal ties have positive atomic mass.
    grid=(F(1,4),F(1,2),F(3,4)); ties=0
    for g in product(grid,repeat=2):
        costs=(g[0],g[1],sum(g)/2)
        regions=[all(costs[j]<costs[l] for l in range(j)) and
                 all(costs[j]<=costs[l] for l in range(j+1,3)) for j in range(3)]
        require(sum(regions)==1,'half-open cells fail to partition')
        require(regions.index(True)==min(range(3),key=lambda j:costs[j]),'tie rule mismatch')
        ties+=int(len([v for v in costs if v==min(costs)])>1)
    p=F(2,5); c=F(1,2); LB=1-c
    dnum= -3*p/4; dden=-(1+2*p)/4
    derivative=(dnum*LB-p*LB*dden)/LB**2
    require(derivative==-p*(1-p)/(2*(1-c)), 'two-cell derivative')
    return {'atomic_points':9,'minimum_tie_points':ties,
            'two_cell_derivative':str(derivative),'passed':True}


def main() -> None:
    result={'schema':'a1-v34-exact-finite-diagnostics-v1',
        'scope':'Finite exact-arithmetic consistency diagnostics; not continuum proofs, optimization, or priority certification.',
        'support':support_checks(),
        'occupancy':[
            occupancy_check('positive_nonmonomial_cells',((F(3,4),F(1,4)),(F(1,4),F(3,4)))),
            occupancy_check('zero_evidence_cells',((F(1),F(0)),(F(0),F(1))))],
        'ties':tie_checks(),'formal_proof_assistant':False,
        'global_controller_optimization':False}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
