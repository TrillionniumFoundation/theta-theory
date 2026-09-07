#!/usr/bin/env python3
"""Independent A1-v18 referee diagnostics, not an author test suite or proof certificate.

Run: python independent_checks.py INDEPENDENT_CHECKS.json
Requires SymPy (executed with 1.14.0). All checked identities/inequalities below
use exact rational or symbolic arithmetic. No stochastic tests or float ranks.
The finite examples do not certify a theorem quantified over all experiments.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import platform
import sys
import sympy as S

PIN = 'be8effe038608bef255fa97318a9ee3b4434af2d'
R = S.Rational
GROUPS: list[dict] = []


def same(a, b=0):
    """Raise on a failed exact scalar or matrix identity."""
    if isinstance(a, S.MatrixBase):
        difference = a - b if isinstance(b, S.MatrixBase) else a
        if any(S.cancel(S.together(x)) != 0 for x in difference):
            raise AssertionError(f'Matrix identity failed: {difference}')
    elif S.cancel(S.together(a-b)) != 0:
        raise AssertionError(f'Identity failed: {a} != {b}')


def record(name, **details):
    GROUPS.append({'name': name, 'status': 'PASS', **details})


def augmented_rank():
    # Physical affine example: P(0)=1/2 is not in im DP=span{x}.
    u = S.symbols('u', real=True)
    x = [-1, 1]
    mu = [R(1, 2)] * 2
    likelihood = [(1+u*R(1, 3)*t)/2 for t in x]
    h = [R(1, 2)+R(1, 4)*t for t in x]
    z = sum(w*l for w, l in zip(mu, likelihood))
    num = sum(w*l*g for w, l, g in zip(mu, likelihood, h))
    y = S.Matrix([z, num]); p = num/z
    assert S.Matrix.hstack(y, y.diff(u)).rank() == 2
    same(S.diff(p, u), R(1, 12))
    assert S.Matrix.hstack(S.Matrix(likelihood).subs(u, 0),
                          S.Matrix(likelihood).diff(u)).rank() == 2
    # Evidence changes while the normalized prediction is constant.
    evidence = 1+u/5
    ye = S.Matrix([evidence, evidence*R(2, 5)])
    assert ye.diff(u).rank() == 1
    assert S.Matrix.hstack(ye, ye.diff(u)).rank() == 1
    same(S.diff(ye[1]/ye[0], u))
    record('augmented_rank_and_evidence_direction', physical_derivative='1/12',
           radial_direction_absent=True, evidence_only_normalized_rank=0)


def polynomial_two_step():
    # Four latent atoms, two orthogonal acquisition bits and positive future tests.
    u, v = S.symbols('u v', real=True)
    atoms = list(product([-1, 1], repeat=2))
    for y1, y2 in product([-1, 1], repeat=2):
        products = [(1+y1*u*a/4)*(1+y2*v*b/5)/4 for a, b in atoms]
        queries = [lambda a,b: R(1,2)+R(1,6)*a,
                   lambda a,b: R(1,2)+R(1,7)*b,
                   lambda a,b: R(1,2)+R(1,8)*a*b]
        z = sum(products)/4
        nums = [sum(P*f(a,b) for (a,b),P in zip(atoms, products))/4
                for f in queries]
        Y = S.Matrix([z]+nums)
        pred = S.Matrix([S.cancel(n/z) for n in nums])
        assert S.Matrix.hstack(Y, Y.jacobian([u,v])).rank() == 3
        assert pred.jacobian([u,v]).rank() == 2
        same(pred[0], R(1,2)+y1*u/24)
        same(pred[1], R(1,2)+y2*v/35)
        same(pred[2], R(1,2)+y1*y2*u*v/160)
    record('two_step_polynomial_actual_report_words', report_words=4,
           augmented_rank=3, normalized_rank=2)


def affine_bayes():
    u, v = S.symbols('u v', real=True)
    weights = [R(1,6),R(1,3),R(1,2)]
    fs = [S.Matrix([R(-1,5),R(1,7)]),
          S.Matrix([R(1,6),R(-1,8)]),
          S.Matrix([R(1,9),R(1,10)])]
    # sqrt(query weights)=(3/5,4/5), with both unweighted H in (0,1).
    hs = [S.Matrix([R(3,5)*a,R(4,5)*b]) for a,b in
          [(R(1,4),R(2,5)),(R(1,2),R(3,5)),(R(3,4),R(1,5))]]
    m = sum((w*f for w,f in zip(weights,fs)), S.zeros(2,1))
    hbar = sum((w*h for w,h in zip(weights,hs)), S.zeros(2,1))
    C = sum((w*(h-hbar)*(f-m).T for w,h,f in zip(weights,hs,fs)), S.zeros(2))
    assert C.det() != 0
    cmd = S.Matrix([u,v])
    for y in [-1,1]:
        ls = [(1+y*(cmd.T*f)[0])/2 for f in fs]
        z = sum(w*l for w,l in zip(weights,ls))
        pred = sum((w*l*h for w,l,h in zip(weights,ls,hs)), S.zeros(2,1))/z
        theta = y*cmd/(1+y*(m.T*cmd)[0])
        same(pred, hbar+C*theta)
    record('weighted_physical_affine_bayes', query_weights=['9/25','16/25'],
           covariance_rank=C.rank(), covariance_det=str(S.factor(C.det())))


def projective_change():
    for b in [1,2,3]:
        v = S.Matrix(S.symbols(f'v0:{b}'))
        # Rational nonzero m, with ||m||_1<1; symbolic commands remain free.
        m = S.Matrix([R(i+1, 10*b*b) for i in range(b)])
        denom = 1+(m.T*v)[0]
        theta = v/denom
        same(theta/(1-(m.T*theta)[0]), v)
        same(theta.jacobian(v).det(), denom**(-(b+1)))
        # Density is acquisition-evidence density times inverse Jacobian.
        same((denom/2**b)/theta.jacobian(v).det(), denom**(b+2)/2**b)
    record('projective_inverse_jacobian_and_evidence', input_dimensions=[1,2,3],
           theta_density_exponent='b+2 (not b+1)')


def interior_stratum():
    x,t,u,alpha,beta = S.symbols('x t u alpha beta', real=True)
    def moment(g): return S.integrate(g*(1+t*x)/2,(x,-1,1))
    cov = moment(x**3)-moment(x)*moment(x**2)
    same(cov, R(4,45)*t)
    prob = R(1,2)+beta*(R(1,3)+alpha*u*t/5)/(1+alpha*u*t/3)
    same(S.diff(prob,u), 4*alpha*beta*t/(45*(1+alpha*u*t/3)**2))
    same(prob.subs(t,0), R(1,2)+beta/3)
    record('interior_full_support_prior_stratum', cross_covariance='4*t/45',
           posterior_derivative='4*alpha*beta*t/(45*(1+alpha*u*t/3)**2)')


def zero_rank_endpoints():
    # A command-independent but informative first report. Both future outcomes positive.
    a,b=R(1,2),R(1,4)
    preds=[]
    for y in [-1,1]:
        ls=[(1+y*a*x)/2 for x in [-1,1]]
        hs=[R(1,2)+b*x for x in [-1,1]]
        z=sum(ls)/2
        preds.append(S.cancel(sum(l*h for l,h in zip(ls,hs))/2/z))
    assert preds == [R(3,8),R(5,8)]
    one_risk=sum((p-R(1,2))**2 for p in preds)/2
    same(one_risk,R(1,64))
    # Conversely, zero affine covariance gives an exactly constant query prediction.
    x,u=S.symbols('x u',real=True)
    num=S.integrate((1+u*x/3)*(R(1,2)+x*x/4)/2,(x,-1,1))
    den=S.integrate((1+u*x/3)/2,(x,-1,1))
    same(num/den,R(7,12))
    record('zero_rank_not_always_one_label', prediction_states=list(map(str,preds)),
           command_rank=0, exact_labels=2, one_label_average_risk=str(one_risk),
           zero_covariance_affine_prediction='7/12')


def determinant_pairing():
    # Exact Cauchy--Binet / finite Andreief checks in two different dimensions.
    cases=0
    for d in [2,3]:
        xs=[R(-2),R(-1),R(1),R(3)]
        V=S.Matrix([[x**i for x in xs] for i in range(d)])
        W=S.Matrix([[x**i+R(i,5)*x**(i+1) for x in xs] for i in range(d)])
        for weights in [[R(1,4)]*4,[R(1,10),R(1,5),R(3,10),R(2,5)]]:
            weighted=(V*S.diag(*weights)*W.T).det()
            cb=sum(V[:,J].det()*W[:,J].det()*math.prod(weights[j] for j in J)
                   for J in combinations(range(4),d))
            same(weighted,cb); cases+=1
    # Both individual evaluation determinants change sign, their product is positive.
    V=S.Matrix([[1,1,1],[0,2,1]])
    vals=[V[:,J].det() for J in combinations(range(3),2)]
    assert min(vals)<0<max(vals)
    assert all(z*z>0 for z in vals)
    # Sign-changing paired determinants yield an actual full-support singular prior.
    V=S.Matrix([[1,1,1],[-1,0,1]])
    W=S.Matrix([[1,1,1],[1,0,1]])
    products=[V[:,J].det()*W[:,J].det() for J in combinations(range(3),2)]
    assert products==[-1,0,1]
    determinants=[]
    for weights in [[R(1,2),R(1,3),R(1,6)],
                    [R(1,3)]*3,[R(1,6),R(1,3),R(1,2)]]:
        determinants.append(S.factor((V*S.diag(*weights)*W.T).det()))
    assert determinants[0]<0 and determinants[1]==0 and determinants[2]>0
    record('paired_determinants_and_positive_weights', cauchy_binet_cases=cases,
           sign_changing_products=list(map(str,products)),
           full_support_weighted_determinants=list(map(str,determinants)),
           matched_individual_determinants=list(map(str,vals)))


def scalar_quantization():
    c=R(2,15)
    z=S.symbols('z')
    budgets=[1,2,3,5,8,16,31]
    for M in budgets:
        risk=0
        for i in range(M):
            left=-c+2*c*R(i,M); right=-c+2*c*R(i+1,M)
            center=(left+right)/2
            risk+=S.integrate((z-center)**2/(2*c),(z,left,right))
        same(risk,c*c/(3*M*M))
        same((c/M)**2,c*c/(M*M))
    record('exact_scalar_uniform_cell_integrals', budgets=budgets,
           integrated_average='c^2/(3*M^2)', squared_cover_radius='c^2/M^2',
           limitation='Integrates the equal-cell code; optimality still needs the analytic argument.')


def leja_collision():
    node_lists=[[R(1,10),R(3,10),R(1,2),R(1,2)],
                [R(1,10),R(1,10),R(1,10)],
                [R(1,10),R(1,5),R(3,5),R(9,10)],
                [R(1,10),R(1,2),R(500001,1000000),R(9,10)]]
    inequalities=0
    for nodes in node_lists:
        remaining=list(range(len(nodes))); selected=[]; pivots=[]
        while remaining:
            scores={j:math.prod(abs(nodes[j]-nodes[i]) for i in selected) for j in remaining}
            best=max(remaining,key=lambda j:(scores[j],-j))
            pivots.append(scores[best]); selected.append(best);remaining.remove(best)
        assert all(pivots[j]>=pivots[j+1] for j in range(len(pivots)-1))
        for ell in range(1,len(nodes)+1):
            volume=max(math.prod(abs(nodes[j]-nodes[i]) for i,j in combinations(J,2))
                       for J in combinations(range(len(nodes)),ell))
            pref=math.prod(pivots[:ell])
            assert pref<=volume<=math.factorial(ell)*pref
            inequalities+=1
    record('leja_products_exact_and_near_collisions', node_sets=len(node_lists),
           prefix_volume_inequalities=inequalities)


def envelope():
    # Raise e to L=lcm(1,...,p), so every branch comparison remains rational.
    lists=[[R(1),R(2,3),R(2,3)], [R(1),R(1,10),R(1,100)],
           [R(1),R(1,4),R(0)], [R(0),R(0),R(0)],
           [R(1,4),R(1,4),R(1,16),R(1,16)]]
    tests=0
    for scales in lists:
        p=len(scales); L=math.lcm(*range(1,p+1)); products=[math.prod(scales[:j]) for j in range(1,p+1)]
        for ell,s in enumerate(scales,1):
            if not s: continue
            V=products[ell-1]; support=V/s**ell
            eL=max((products[j-1]/support)**(L//j) for j in range(1,p+1))
            same(eL,s**L)
            M=int(S.ceiling(support))
            eLM=max((products[j-1]/M)**(L//j) for j in range(1,p+1))
            assert V**L<=M**L*eLM**ell<=(2*V)**L
            tests+=1
    # A rigorous non-equality witness: for M>=2, the third branch lower bound
    # M*e(M)^2 >= (4/9)^(2/3)*M^(1/3) is increasing; at M=2 it is attained.
    same((2*(R(2,9))**R(2,3))**3,R(32,81))
    assert R(32,81)>R(2,3)**3
    record('integer_envelope_positive_repeated_zero_lists', supporting_budget_checks=tests,
           non_equality_witness_scales=['1','2/3','2/3'],
           witness_l=2, integer_infimum_cubed='32/81', product_cubed='8/27',
           limitation='Zero-product asymptotics are proved in the report, not certified by finitely many budgets.')


def circular_update():
    # Laurent coefficient multiplication with exact Gaussian rational numbers.
    tau=R(1,5)
    zs=[R(1,10)+S.I/20, R(-1,12)+S.I/30, R(1,15)-S.I/25]
    coeff={0:S.Integer(1)}; checked=0
    for z in zs:
        previous=coeff.copy(); old0=previous[0]
        coeff={}
        for j,c in previous.items():
            for shift,factor in [(0,1),(1,tau*z),(-1,tau*S.conjugate(z))]:
                coeff[j+shift]=S.expand(coeff.get(j+shift,0)+c*factor)
        def Y(j):
            if j<0: return S.conjugate(Y(-j))
            return S.cancel(tau**j*previous.get(j,0)/old0)
        denom=1+z*S.conjugate(Y(1))+S.conjugate(z)*Y(1)
        for j in range(1,len(zs)+1):
            exact=S.cancel(tau**j*coeff.get(j,0)/coeff[0])
            formula=(Y(j)+tau*tau*z*Y(j-1)+S.conjugate(z)*Y(j+1))/denom
            same(exact,formula); checked+=1
    record('inherited_weighted_fourier_update', exact_complex_identity_checks=checked,
           tau=str(tau), reciprocal_contrast_used=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    for fn in [augmented_rank,polynomial_two_step,affine_bayes,projective_change,
               interior_stratum,zero_rank_endpoints,determinant_pairing,
               scalar_quantization,leja_collision,envelope,circular_update]:
        fn()
    receipt={'reviewed_submission':PIN,
             'executed_at_utc':datetime.now(timezone.utc).isoformat(),
             'python':platform.python_version(),'sympy':S.__version__,
             'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'status':'PASS','named_groups':len(GROUPS),'groups':GROUPS,
             'scope':'Independent exact finite/symbolic diagnostics only. Not formal verification, a global minimax search, an author-validator rerun, or a typesetting/PDF check.'}
    args.output.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
