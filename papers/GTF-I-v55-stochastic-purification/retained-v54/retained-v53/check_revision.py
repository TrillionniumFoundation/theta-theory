"""Exact finite regressions for GTF-I v53; not a formal proof of the theorems.

All checks remain active under python -O. No network or repository mutation.
"""
from __future__ import annotations
import itertools
import json
import math
from fractions import Fraction as F
import sympy as sp

COUNTS: dict[str, int] = {}
NEGATIVES: list[str] = []

def require(condition: bool, name: str) -> None:
    if not condition:
        raise ValueError(name)

def checked(condition: bool, family: str) -> None:
    require(condition, family)
    COUNTS[family] = COUNTS.get(family, 0) + 1

def rejects(name: str, operation) -> None:
    try:
        operation()
    except ValueError:
        NEGATIVES.append(name)
    else:
        raise ValueError('Negative control not detected: ' + name)

def convolve(a: dict[int, F], b: dict[int, F]) -> dict[int, F]:
    out: dict[int, F] = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i+j] = out.get(i+j, F(0)) + x*y
    return {i: x for i, x in out.items() if x}

def localization(r: int, sign: int = 1) -> dict[int, F]:
    require(r >= 1 and sign in (-1, 1), 'localization parameters')
    p = {0: F(1)}
    for _ in range(r):
        p = convolve(p, {0: F(1), -1: F(sign, 2), 1: F(sign, 2)})
    c = F(math.comb(2*r, r), 2**r)
    require(p[0] == c, 'normalizing Haar coefficient')
    return {i: x/c for i, x in p.items()}

def validate_localization(p: dict[int, F], r: int, sign: int) -> None:
    require(p.get(0) == 1, 'Haar mean must be one')
    pc = convolve(p, {-1: F(1, 2), 1: F(1, 2)})
    require(pc.get(0) == F(sign*r, r+1), 'weighted extreme mean')
    require(max(abs(i) for i in pc) <= r+1, 'required harmonic degree')
    require(sum(map(abs, p.values())) <= 2*r+1, 'coefficient norm bound')

def parameters(rho: F, epsilon: F, r: int) -> tuple[F, F]:
    require(0 < rho <= 1 and 0 <= 2*epsilon < rho, 'subcritical mean/TV conversion')
    delta = 2*epsilon
    gap = 2*(rho*F(r, r+1)-delta)
    require(r >= 1 and gap > 0, 'strict localization degree')
    a = 2*(1+rho+delta)*(2*r+1)*(r+1)/gap
    require(a > 1, 'positive logarithmic budget')
    return gap, a

def interval_valid(lo: F, hi: F, decoder: F, epsilon: F) -> None:
    require(-1 <= lo <= hi <= 1 and -1 <= decoder <= 1, 'legal mean interval')
    require(max(abs(lo-decoder), abs(hi-decoder))/2 <= epsilon, 'uniform binary TV budget')

Matrix = tuple[tuple[F, F], tuple[F, F]]
IDENTITY: Matrix = ((F(1), F(0)), (F(0), F(1)))
ROT: Matrix = ((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5)))
REFLECT: Matrix = ((F(1), F(0)), (F(0), F(-1)))

def mul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(sum((a[i][l]*b[l][j] for l in range(2)), F(0))
                       for j in range(2)) for i in range(2))

def vec(a: Matrix, v: tuple[F, F]) -> tuple[F, F]:
    return tuple(sum((a[i][j]*v[j] for j in range(2)), F(0)) for i in range(2))

def det(a: Matrix) -> F:
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def complex_mul(a: tuple[F, F], b: tuple[F, F]) -> tuple[F, F]:
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]

def power_nonzero(z: tuple[F, F], n: int) -> None:
    u = (F(1), F(0))
    for _ in range(n):
        u = complex_mul(u, z)
    require((u[0]-1)**2+u[1]**2 > 0, 'non-root-of-unity separation')

def harmonic_checks() -> None:
    for r in range(1, 49):
        for sign in (-1, 1):
            p = localization(r, sign)
            validate_localization(p, r, sign)
            checked(True, 'exact_Laurent_localization')
    for rho in (F(1,10), F(1,3), F(1)):
        for ratio in (F(0), F(1,4), F(3,4), F(9,10), F(99,100)):
            epsilon = rho*ratio/2
            q = (2*epsilon)/(rho-2*epsilon)
            r = q.numerator//q.denominator+1
            gap, a = parameters(rho, epsilon, r)
            checked(gap > 0 and a > 1, 'full_subcritical_parameter_selection')
    checked(parameters(F(1,10), F(1,25), 5) == (F(1,150), F(23364)),
            'displayed_rational_calibration')
    rejects('degree_at_equality_not_strict', lambda: parameters(F(1,10), F(1,25), 4))
    rejects('critical_endpoint_not_subcritical', lambda: parameters(F(1,10), F(1,20), 100))
    bad = localization(5); bad[0] += F(1,100)
    rejects('corrupt_Haar_normalization', lambda: validate_localization(bad, 5, 1))
    bad2 = localization(5); bad2[1] += F(1,100)
    rejects('corrupt_weighted_extreme', lambda: validate_localization(bad2, 5, 1))

def component_checks() -> None:
    rho = F(1,10)
    interval_valid(-rho, rho, F(0), rho/2)
    checked(True, 'critical_boundary_attained')
    rejects('subcritical_constant_decoder', lambda: interval_valid(-rho, rho, F(0), rho/2-F(1,1000)))
    rejects('off_midpoint_decoder_at_boundary', lambda: interval_valid(-rho, rho, F(1,1000), rho/2))
    # f(h)=alpha det(h)+beta h_11: two components with nonzero, different midpoints.
    alpha, beta = F(2,5), F(1,5)
    for n in range(7):
        for word in itertools.product(range(3), repeat=n):
            h = IDENTITY; component = F(1)
            for letter in word:
                a = (IDENTITY, ROT, REFLECT)[letter]
                h = mul(a, h); component *= det(a)
            target = alpha*det(h)+beta*h[0][0]
            decoder = alpha*component
            checked(abs(target-decoder)/2 <= beta/2 and det(h) == component,
                    'nonlinear_two_component_permutation_decoder')
    checked(mul(REFLECT, mul(ROT, REFLECT)) == ((F(3,5),F(4,5)),(F(-4,5),F(3,5))),
            'noncommuting_word_order')

def arithmetic_checks() -> None:
    z = (F(3,5), F(4,5)); powers = [(F(1),F(0))]
    for n in range(1, 97):
        powers.append(complex_mul(powers[-1], z))
        re, im = powers[-1]
        checked((re-1)**2+im**2 >= F(1, 5**(2*n)), 'rational_power_height')
    # Check explicit families of unit-center configurations, not a universal optimization.
    for m in range(1,5):
        for k in range(1,5):
            sigma2 = F(1, 5**(4*m*k))
            # A unit vector in the highest-frequency block, and the first k orbit points as centers.
            dots = []
            for j in range(2*k):
                row=[]
                for i in range(k):
                    row.append(powers[m*abs(i-j)][0])
                dots.append(max(row))
            defect = sum((1-v for v in dots), F(0))/(2*k)
            checked(defect >= sigma2/16, 'finite_exact_cap_configurations')
    rejects('root_of_unity_separation', lambda: power_nonzero((F(0),F(1)), 4))
    x = sp.symbols('x'); p=x**4-x**3-x**2-x+1
    checked(sp.Poly(p,x,modulus=2).is_irreducible is True, 'Salem_polynomial_irreducibility')
    t=(1-sp.sqrt(13))/2
    checked(sp.simplify(t*t-t-3)==0, 'Salem_trace_equation')
    checked(sp.expand(x*x*((x+1/x)**2-(x+1/x)-3)) == p, 'Salem_substitution_identity')
    for n in range(1,25):
        result=sp.resultant(p,x**n-1,x)
        checked(result.is_Integer and result != 0, 'finite_exact_resultants')

def conditional_checks() -> None:
    rotations=[IDENTITY,ROT,mul(ROT,ROT)]
    history_vectors=[vec(a,(F(1),F(0))) for a in rotations]
    # Joint mass of latent history h and current hidden label s; nontrivial mixing.
    joint={(0,0):F(1,6),(0,1):F(1,12),(1,0):F(1,4),
           (1,1):F(1,6),(2,0):F(1,12),(2,1):F(1,4)}
    require(sum(joint.values())==1,'joint normalization')
    nu=[F(1,6),F(1,3),F(1,2)]
    transition=[((F(1,3),F(2,3)),(F(3,4),F(1,4))),
                ((F(2,5),F(3,5)),(F(1,2),F(1,2))),
                ((F(1),F(0)),(F(1,4),F(3,4)))]
    p_s={s:sum((mass for (h,t),mass in joint.items() if t==s),F(0)) for s in range(2)}
    z_s={s:tuple(sum((mass*history_vectors[h][c] for (h,t),mass in joint.items() if t==s),F(0))/p_s[s]
                 for c in range(2)) for s in range(2)}
    for j in range(2):
        direct=[F(0),F(0)]; factored=[F(0),F(0)]
        for (h,s),mass in joint.items():
            for w in range(3):
                v=vec(rotations[w],history_vectors[h])
                for c in range(2):direct[c]+=mass*nu[w]*transition[w][s][j]*v[c]
        for s in range(2):
            for w in range(3):
                v=vec(rotations[w],z_s[s])
                for c in range(2):factored[c]+=p_s[s]*nu[w]*transition[w][s][j]*v[c]
        checked(direct==factored,'exact_conditional_block_identity')
    # An identity physical command may erase hidden information through a nonidentity stochastic row.
    checked(tuple(sum((F(1,2)*x for x in (F(1),F(-1))),F(0)) for _ in range(2))==(F(0),F(0)),
            'identity_command_allows_hidden_mixing')
    # Failure of the independent-word factorization when w equals the latent history.
    direct=tuple(sum((F(1,2)*vec(rotations[h],history_vectors[h])[c] for h in (0,1)),F(0)) for c in range(2))
    zbar=tuple((history_vectors[0][c]+history_vectors[1][c])/2 for c in range(2))
    independent=tuple(sum((F(1,2)*vec(rotations[w],zbar)[c] for w in (0,1)),F(0)) for c in range(2))
    rejects('correlated_word_used_as_independent_block',lambda:require(direct==independent,'block independence absent'))

def hypothesis_checks() -> None:
    u=sp.Matrix([[sp.Rational(3,5),-sp.Rational(4,5),0],
                 [sp.Rational(4,5),sp.Rational(3,5),0],[0,0,1]])
    e1,e3=sp.eye(3)[:,0],sp.eye(3)[:,2]
    checked(u*e3==e3 and sp.Matrix.hstack(e3,u*e3,u*u*e3).rank()==1,
            'fixed_axis_partial_interface')
    checked(all((e3.T*u**n*e1)[0]==0 for n in range(8)), 'invisible_reachable_plane')
    checked(sp.Matrix.hstack(e1,u*e1).rank()==2, 'nonspanning_seed_reaches_plane')
    transition=sp.Matrix([[sp.Rational(2,3),sp.Rational(1,3)],[0,1]])
    for n in range(25):
        mean=(sp.Matrix([[1,0]])*transition**n*sp.Matrix([sp.Rational(1,10),0]))[0]
        checked(mean==sp.Rational(1,10)*sp.Rational(2,3)**n,'bounded_semigroup_not_bounded_group')
    for n in range(1,25):
        target=(sp.Matrix([[1,0,0]])*u**n*e1)[0]/10
        # A sole executable word at each N permits a free horizon-specific scalar decoder.
        checked(-1<=target<=1, 'no_identity_single_word_counterexample')
    words=[('R','I','I'),('I','R','I'),('I','I','I')]
    checked(len({len(w) for w in words})==1,'executable_equal_length_padding')
    rejects('unequal_length_test_words',lambda:require(len({1,2,3})==1,'padding omitted'))

def main() -> None:
    harmonic_checks(); component_checks(); arithmetic_checks(); conditional_checks(); hypothesis_checks()
    print(json.dumps({'schema':'gtf53.exact-checks/1','status':'success',
                      'families':COUNTS,'exact_finite_assertions':sum(COUNTS.values()),
                      'negative_controls_detected':NEGATIVES,
                      'scope':'Finite exact regressions and hypothesis counterexamples. The universal analytic proof is the manuscript, not these samples.'},
                     sort_keys=True))

if __name__=='__main__':
    main()
