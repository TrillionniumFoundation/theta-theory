"""Exact finite v51 regressions and a supplied-local-witness checker.

This module does not optimize over unknown lifts and does not certify the
universal mathematical statements by sampling. All checks survive python -O.
"""
from __future__ import annotations
import itertools
import json
from fractions import Fraction
from typing import Callable
import sympy as s


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def zero(a: s.Matrix) -> bool:
    return all(x == 0 for x in a)


def check_local(P: s.Matrix, Z: s.Matrix, T: s.Matrix, U: s.Matrix,
                seeds: list[tuple[s.Matrix, s.Matrix]], rho: s.Rational,
                Q: s.Matrix | None = None, Y: s.Matrix | None = None) -> None:
    """Check one exact rational/algebraic transition of Theorem local51."""
    Q = P if Q is None else Q
    Y = Z if Y is None else Y
    k, d = Z.shape
    l = Y.rows
    require(P.shape == (k, k) and Q.shape == (l, l), 'projector shape')
    require(T.shape == (k, l) and U.shape == (d, d), 'transition shape')
    require(zero(U.T*U-s.eye(d)), 'nonorthogonal command')
    for A in (P, Q):
        require(A == A.T and A*A == A, 'not an orthogonal projector')
    require(all(-1 <= z <= 1 for z in list(Z)+list(Y)), 'illegal mean')
    require(all(t >= 0 for t in T), 'negative transition')
    require(T*s.ones(l, 1) == s.ones(k, 1), 'row sum')
    require(zero(P*T*(s.eye(l)-Q)), 'span not invariant')
    require(zero(P*(T*Y-Z*U.T)), 'observable identity')
    for x, p in seeds:
        require(p.shape == (1, k), 'seed shape')
        require(all(v >= 0 for v in p) and sum(p) == 1, 'illegal seed')
        require(p*P == p and p*Z == rho*x.T, 'seed identity')


def perm(states: list[s.Matrix], U: s.Matrix) -> s.Matrix:
    T = s.zeros(len(states))
    for i, x in enumerate(states):
        matches = [j for j, y in enumerate(states) if U*x == y]
        require(len(matches) == 1, 'state set not permuted')
        T[i, matches[0]] = 1
    return T


def signed_axes(d: int) -> list[s.Matrix]:
    return [sign*s.eye(d)[:, i] for i in range(d) for sign in (1, -1)]


def robust_certificate(rho: Fraction, eps: Fraction, n: int) -> bool:
    require(0 < rho < 1 and n >= 0, 'signal/horizon domain')
    require(0 <= eps <= rho*rho/2000, 'outside proved error interval')
    return Fraction(512,363)**n > 2*Fraction(500,499)**2/(rho*rho)


def main() -> None:
    checks: dict[str, object] = {}
    negatives: list[str] = []
    def reject(name: str, f: Callable[[], object]) -> None:
        try:
            f()
        except (ValueError, AssertionError):
            negatives.append(name)
        else:
            raise RuntimeError('Negative control was accepted: '+name)

    rho = s.Rational(1,10)
    axes = signed_axes(2)
    corners = [s.Matrix(z) for z in itertools.product((-1,1), repeat=2)]
    Z = s.Matrix.vstack(*(z.T for z in corners))
    B = s.ones(4,1).row_join(Z)
    P = B*(B.T*B).inv()*B.T
    seeds = [(x, s.Matrix([[s.Rational(1,4)*(1+rho*(x.T*z)[0]) for z in corners]])) for x in axes]
    commands = [s.eye(2), -s.eye(2), s.Matrix([[0,1],[1,0]]), s.diag(-1,1)]
    for U in commands:
        check_local(P,Z,perm(corners,U),U,seeds,rho)
    require(P.rank()==3 and Z.rank()==2, 'section rank')
    vertices = []
    # In this three-dimensional row span, the mass-one section has dimension two.
    for active in itertools.combinations(range(4),2):
        equations = [(s.eye(4)-P)[:,j].T for j in range(4)]
        equations += [s.ones(1,4)] + [s.eye(4)[i,:] for i in active]
        A = s.Matrix.vstack(*equations)
        rhs = s.Matrix([0]*4+[1]+[0]*2)
        try:
            sol, params = A.gauss_jordan_solve(rhs)
        except ValueError:
            continue
        if params.rows == 0 and all(v>=0 for v in sol):
            v = tuple(sol)
            if v not in vertices:
                vertices.append(v)
    require(len(vertices)==4, 'section vertex enumeration')
    images = {tuple((s.Matrix([v])*Z).T) for v in vertices}
    require(images=={tuple(x) for x in axes}, 'section image')
    checks['rank_three_four_label_section']={'rank':3,'vertices':4,'binomial_bound':6}

    fullZ = s.Matrix.vstack(*(rho*x.T for x in axes))
    fullseeds = [(x,s.eye(4)[i,:]) for i,x in enumerate(axes)]
    for U in commands:
        check_local(s.eye(4),fullZ,perm(axes,U),U,fullseeds,rho)
    require(s.ones(4,1).row_join(fullZ).rank()==3, 'observation kernel')
    checks['rank_four_four_label_lift']={'rank':4,'observation_kernel':1}

    P5=s.diag(1,1,1,1,0)
    Z5=fullZ.col_join(s.zeros(1,2))
    T5=s.zeros(5)
    T5[:4,:4]=perm(axes,-s.eye(2));T5[4,0]=1
    seeds5=[(x,p.row_join(s.zeros(1,1))) for x,p in fullseeds]
    check_local(P5,Z5,T5,-s.eye(2),seeds5,rho)
    require(not zero(T5*Z5+Z5), 'missing ambient failure witness')
    checks['unreachable_fifth_state']={'restricted_identity':True,'ambient_identity':False,'charged_labels':5}
    reject('false_ambient_projection',lambda:check_local(s.eye(5),Z5,T5,-s.eye(2),seeds5,rho))
    badP=P.copy();badP[0,0]+=s.Rational(1,10)
    reject('nonidempotent_projector',lambda:check_local(badP,Z,s.eye(4),s.eye(2),seeds,rho))
    badT=s.eye(4);badT[0,0]=2
    reject('unnormalized_transition',lambda:check_local(P,Z,badT,s.eye(2),seeds,rho))
    badT2=s.eye(4);badT2[0,0]=2;badT2[0,1]=-1
    reject('negative_transition',lambda:check_local(P,Z,badT2,s.eye(2),seeds,rho))
    badZ=Z.copy();badZ[0,0]=2
    reject('illegal_decoder_mean',lambda:check_local(P,badZ,s.eye(4),s.eye(2),seeds,rho))
    badseeds=[(axes[0],s.Matrix([[2,-1,0,0]]))]
    reject('negative_seed_probability',lambda:check_local(P,Z,s.eye(4),s.eye(2),badseeds,rho))
    reject('wrong_command_identity',lambda:check_local(P,Z,s.eye(4),-s.eye(2),seeds,rho))

    axes3=signed_axes(3);Z3=s.Matrix.vstack(*(rho*x.T for x in axes3))
    seeds3=[(x,s.eye(6)[i,:]) for i,x in enumerate(axes3)]
    A3=[s.eye(3),-s.eye(3),s.Matrix([[0,1,0],[1,0,0],[0,0,1]]),s.diag(-1,1,1)]
    T3=[perm(axes3,U) for U in A3]
    for U,T in zip(A3,T3):check_local(s.eye(6),Z3,T,U,seeds3,rho)
    wordchecks=0
    for word in itertools.product(range(4),repeat=3):
        for x,p in seeds3:
            q=p;v=x
            for a in word:q=q*T3[a];v=A3[a]*v
            require(q*Z3==rho*v.T, 'six-state word mismatch');wordchecks+=1
    require(A3[2]*A3[3]!=A3[3]*A3[2], 'three-dimensional commutation')
    tetra=[s.Matrix(z) for z in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
    for x in axes3:
        require(any((a+b)/2==x for a,b in itertools.combinations(tetra,2)), 'tetrahedron containment')
    checks['six_state_frontier_witness']={'exact_word_seed_checks':wordchecks,'tetrahedron_contains_C1':True}
    require(3+2<2*3,'one-surplus strict dimension')
    reject('false_planar_one_surplus_gap',lambda:require(2+2<2*2,'D=2 central polygon exception'))

    R=s.Matrix([[3,-4],[4,3]])/5;F=s.diag(1,-1)
    require(R.T*R==s.eye(2) and F*R*F==R.inv() and F*R!=R*F,'rational group identities')
    require(s.trace(R)==s.Rational(6,5) and s.trace(R).q!=1,'root-of-unity trace witness')
    checks['rational_noncommuting_group']={'trace':'6/5','reflection_conjugates_to_inverse':True}

    triangle=s.Matrix([[1,0],[-1,1],[-1,-1]])
    Fanchor=s.Matrix([[s.Rational(1,2),s.Rational(1,4),s.Rational(1,4)],
                     [(1+rho)/2,(1-rho)/4,(1-rho)/4],
                     [s.Rational(1,2),(1+2*rho)/4,(1-2*rho)/4]])
    Mstar=s.Matrix([[1,0,0],[1,rho,0],[1,0,rho]])
    require(Fanchor*s.ones(3,1).row_join(triangle)==Mstar,'anchor normalization')
    infnorm=lambda M:max(sum(abs(M[i,j]) for j in range(M.cols)) for i in range(M.rows))
    require(infnorm(Mstar.inv())==2/rho,'anchor target inverse bound')
    require(infnorm(Fanchor.inv())<=6/rho,'anchor inverse comparison')
    delta=s.Rational(1,100000)
    perturbed=triangle.copy();perturbed[0,0]-=delta
    M=Fanchor*s.ones(3,1).row_join(perturbed)
    require(infnorm(M-Mstar)<=2*delta and infnorm(M.inv())<=2/(rho-4*delta),'perturbed inverse')
    require(960000<994008,'robust multiplier arithmetic')
    require(robust_certificate(Fraction(1,10),Fraction(1,200000),16),'sixteen horizon certificate')
    require(not robust_certificate(Fraction(1,10),Fraction(1,200000),15),'fifteen not certified')
    reject('premature_fifteen_horizon_claim',lambda:require(robust_certificate(Fraction(1,10),Fraction(1,200000),15),'not certified'))
    reject('unsupported_noise_interval',lambda:robust_certificate(Fraction(1,10),Fraction(1,100000),16))
    reject('vanishing_anchor_margin',lambda:require(rho-4*(rho/4)>0,'singular margin'))
    checks['stable_anchor']={'exact_inverse_checked':True,'perturbed_inverse_checked':True,'rho':'1/10','TV_bound':'1/200000','sufficient_horizon':16}

    u=[s.Integer(1),s.Integer(0),s.Rational(1,2),s.Rational(1,2)]
    errors=[abs((u[i]+u[j])/2-(1 if i==0 else 0)) for i in (0,1) for j in (2,3)]
    require(max(errors)==s.Rational(1,4),'quarter extension witness')
    require(s.Rational(1,2)*(1-s.Rational(1,2))==s.Rational(1,4),'quarter lower witness')
    checks['stochastic_extension_defect']='1/4'
    out={'schema':'gtf51.exact-finite-regressions/1','status':'success','checks':checks,
         'negative_controls_detected':negatives,'scope':'Supplied local identities and finite rational examples only; universal theorems are proved in the manuscript, not by these tests.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
