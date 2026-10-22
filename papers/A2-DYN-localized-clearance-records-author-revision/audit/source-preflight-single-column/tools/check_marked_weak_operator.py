#!/usr/bin/env python3
"""Exact finite identities supporting native332; not a strong spectral certificate."""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from pathlib import Path

from analytic_check_support import Audit, command_arguments, emit_result, fraction_text


def dot(a: tuple[F,F], b: tuple[F,F]) -> F:
    return a[0]*b[0]+a[1]*b[1]


def scale(value: F, vector: tuple[F,F]) -> tuple[F,F]:
    return value*vector[0], value*vector[1]


def matvec(matrix: tuple[F,F,F], vector: tuple[F,F]) -> tuple[F,F]:
    a,b,d=matrix
    x,y=vector
    return a*x+b*y, b*x+d*y


def inverse(matrix: tuple[F,F,F]) -> tuple[F,F,F]:
    a,b,d=matrix
    det=a*d-b*b
    if det <= 0 or a <= 0:
        raise RuntimeError("This inverse requires a positive definite matrix.")
    return d/det,-b/det,a/det


def check_gauss(audit: Audit) -> None:
    directions=[(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),
                (F(-3,5),F(4,5)),(F(5,13),F(-12,13))]
    matrices=0
    for a,b,d in product(range(1,5),range(-2,3),range(1,5)):
        if a*d<=b*b:
            continue
        matrices+=1
        matrix=(F(a),F(b),F(d))
        inv=inverse(matrix)
        lower=F(a*d-b*b,a+d)
        upper=F(a+d)
        for e in directions:
            audit.check("Gauss direction is exactly unit", dot(e,e)==1)
            gie=matvec(inv,e)
            h=dot(e,gie)
            audit.check("quadratic inverse Hessian bounds", 1/upper<=h<=1/lower)
            for z in (F(1,7),F(1),F(7,3)):
                zt=1/(z*h)
                qt=scale(zt,gie)
                audit.check("Gauss q_t includes the full H denominator", matvec(matrix,qt)==scale(zt,e))
                audit.check("Gauss physical action derivative is exactly one", dot(scale(z,e),qt)==1)
                audit.check("Gauss uniform infinity norm upper bound", max(abs(qt[0]),abs(qt[1]))<=upper/(lower*z))
                for radius in (F(9,20),F(47,100)):
                    dp=(-zt*e[0]/radius,zt*e[1]/radius)
                    audit.check("actual endpoint momentum first variation", (-radius*dp[0],radius*dp[1])==matvec(matrix,qt))
                    audit.check("actual endpoint momentum derivative bound", max(abs(dp[0]),abs(dp[1]))<=upper/(radius*z))
                q_at_2z=scale(1/(2*z*h),gie)
                audit.check("critical inverse-gradient factor is retained", scale(2,q_at_2z)==qt)
    audit.detail("Gauss_identities", {
        "rational_SPD_matrices":matrices,
        "q_t":"G^(-1)e/(z*H)",
        "z_t":"1/(z*H)",
        "H":"e^T G^(-1)e",
        "critical_factor":"1/z is paid by the full physical moment; it is not removed pointwise",
        "finite_matrix_examples_are_not":"a verification of the physical Hessian theorem itself",
    })


def check_localization_and_constants(audit: Audit) -> None:
    sigma=F(47,59)
    rplus=F(47,100)
    rminus=F(9,20)
    taumin=F(3,50)
    jstar=F(2845,354)
    cc=jstar*(1+rplus/taumin*(1+1/sigma))
    audit.check("inherited exact endpoint localization constant", jstar==max(F(1),rplus/(2*taumin)*(sigma+1/sigma)))
    audit.check("supersolution cancellation with physical flight gap", 2/rplus-(1/sigma-1)/taumin==0)
    audit.check("inherited exact incidence and momentum constant", cc==jstar*(1+rplus/taumin*(1+1/sigma)))
    for m in range(1,129):
        s=[sigma**i+sigma**(m-i) for i in range(m+1)]
        audit.check("endpoint localization weights include both endpoints", s[0]>=1 and s[-1]>=1)
        audit.check("exact full-chain geometric sum", sum(s)==2*(1-sigma**(m+1))/(1-sigma))
        audit.check("summable endpoint dependence uniform in m", sum(s)<=2/(1-sigma))
        l=[F(i%4,3) for i in range(m+1)]
        audit.check("weighted phase derivative sum", sum(x*y for x,y in zip(l,s))<=2/(1-sigma))
        for i in range(m+1):
            neighbor=i+1 if i<m else i-1
            audit.check("one-sided neighboring localization weight", s[neighbor]<=s[i]/sigma)
            bound=rplus*jstar/taumin*(s[i]+s[neighbor])+jstar*s[i]
            audit.check("interior tangential momentum coefficient without inverse incidence", bound<=cc*s[i])
    # lambda=9*sqrt(19)/200, Lambda=47/6. The exact endpoint constant is
    # 470/27 + (4700/513)*sqrt(19), with no numerical square-root approximation.
    rational_part=F(47,6)/rminus
    radical_part=F(47,6)*F(200,171)
    audit.check("C_test,end exact rational part", rational_part==F(470,27))
    audit.check("C_test,end exact sqrt19 coefficient", radical_part==F(4700,513))
    phase_radical=radical_part*(jstar+cc)
    audit.detail("physical_constants", {
        "R_minus":fraction_text(rminus),
        "R_plus":fraction_text(rplus),
        "tau_minus":fraction_text(taumin),
        "sigma":fraction_text(sigma),
        "J_star":fraction_text(jstar),
        "C_c":fraction_text(cc),
        "lambda_circ":"9*sqrt(19)/200",
        "Lambda_circ":"47/6",
        "C_test_end":fraction_text(rational_part)+" + "+fraction_text(radical_part)+"*sqrt(19)",
        "C_test_phase":fraction_text(phase_radical)+"*sqrt(19)",
        "full_weight_sum_upper_bound":fraction_text(2/(1-sigma)),
        "constant_names_do_not_collide_with":"the inherited296 radius-disintegration C_end",
    })


def check_true_tangent_derivative(audit: Audit) -> None:
    directions=[(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-5,13),F(12,13))]
    for integer in (2,3,10,100,1000):
        directions.append((F(2*integer,integer*integer+1),F(integer*integer-1,integer*integer+1)))
    smallest_positive=None
    for normal,velocity,rho,xi in product(directions,directions,(F(-2),F(0),F(1,3)),(F(-1,7),F(0),F(5,2))):
        tangent=(-normal[1],normal[0])
        dv=scale(rho,(-velocity[1],velocity[0]))
        dtangent=scale(-xi,normal)
        derivative=dot(dv,tangent)+dot(velocity,dtangent)
        expected=dot(dv,tangent)-dot(velocity,normal)*xi
        audit.check("tangential momentum geometric derivative identity", derivative==expected)
        audit.check("tangential momentum derivative has no incidence divisor", abs(derivative)<=abs(rho)+abs(xi))
        incidence=dot(velocity,normal)
        if incidence>0 and (smallest_positive is None or incidence<smallest_positive):
            smallest_positive=incidence
    audit.detail("geometric_observable_derivative", {
        "identity":"D(v dot n') = Dv dot n' - (v dot n)*Dalpha",
        "uses_reflection":"tangential momentum is preserved at the terminal reflection",
        "minimum_positive_incidence_among_examples":fraction_text(smallest_positive),
        "incidence_lower_bound_in_proof":None,
        "scope":"Finite algebraic examples include arbitrarily small chosen positive incidence; the branch-uniform bound is the native Jacobi/flight argument, not a sampling conclusion.",
    })


def check_products_and_normalization(audit: Audit) -> None:
    endpoint_pairs=[(F(a,4),F(b,4)) for a,b in product(range(5),repeat=2) if a+b<=4]
    for (a0,a1),(b0,b1) in product(endpoint_pairs,repeat=2):
        audit.check("actual C1 test norm supplies both partial-derivative terms", a1*b0+a0*b1<=2)
        for d,j,c,phase in ((F(3),F(5),F(7),F(0)),(F(1,7),F(2,3),F(4,5),F(9,2))):
            expression=d*a0*b0+j*(c*(a1*b0+a0*b1)+phase*a0*b0)
            audit.check("weak operator constant includes endpoint product derivative", expression<=d+2*j*c+j*phase)
        audit.check("tested source mass is bounded by endpoint suprema", a0*b0<=1)
    for cstar,jmass,capfraction in product((F(1,100),F(1,7),F(2,3)),(F(1),F(5,2),F(20)),(F(0),F(1,5),F(1))):
        cap_integral=jmass*capfraction
        coarea_integral=cap_integral/cstar
        audit.check("one original conditioning division in full moment", coarea_integral*cstar==cap_integral)
        audit.check("full inverse-gradient moment payment", coarea_integral<=jmass/cstar)
    audit.detail("normalization_and_test_space", {
        "C1_norm":"sup|a| + max(sup|partial_alpha a|, sup|partial_p a|)",
        "J_test":"J_cross/c_star",
        "coarea_identity":"integral_theta sum_word integral A/z = c_star^(-1) integral_cap 1/z dnu",
        "full_source_bound":"1/z <= I_m/z and integral I_m/z dnu <= J_cross",
        "extra_conditioning_divisions":0,
        "operator_space":"C1(compact collision cylinder) -> its complex linear dual",
    })


def check_bv_fourier_arithmetic(audit: Audit) -> None:
    cycle=[(F(1),F(0)),(F(0),F(1)),(F(-1),F(0)),(F(0),F(-1))]
    for values in product(range(-2,3),repeat=4):
        augmented=(0,)+values+(0,)
        variation=sum(abs(b-a) for a,b in zip(augmented,augmented[1:]))
        # For s=pi/2, multiplication by s removes the elementary interval
        # antiderivative denominator. Unit-complex phases are represented exactly.
        numerator=[F(0),F(0)]
        for index,value in enumerate(values):
            left,right=cycle[index%4],cycle[(index+1)%4]
            numerator[0]+=value*(right[0]-left[0])
            numerator[1]+=value*(right[1]-left[1])
        audit.check("compact BV Fourier integration-by-parts variation bound", numerator[0]**2+numerator[1]**2<=variation**2, values)
    audit.detail("Fourier_scope", {
        "uniform_bound":"min(1,(D_all^w + 2*J_test*C_test,end)/abs(s))",
        "phase_addition":"J_test*C_test,phase*L_m",
        "strong_anisotropic_operator_bound_proved":False,
        "decay_in_collision_count_proved":False,
        "integrable_high_frequency_tail_proved":False,
        "raw_pointwise_local_limit_proved":False,
    })


def main() -> None:
    program=Path(__file__).resolve()
    args=command_arguments(program)
    audit=Audit()
    check_gauss(audit)
    check_localization_and_constants(audit)
    check_true_tangent_derivative(audit)
    check_products_and_normalization(audit)
    check_bv_fourier_arithmetic(audit)
    emit_result(args,program,["330_all_label_physical_roof_variation.tex","331_return_tower_and_polynomial_likelihood.tex","332_endpoint_tested_marked_roof_operator.tex"],audit,[
        "Checks exact Gauss/Hessian algebra, physical constant arithmetic, summable endpoint weights, tangential momentum derivatives, actual C1 norms, conditioning normalization and finite BV Fourier examples.",
        "The complete physical Hessian, all-word moment and boundary inputs remain inherited theorems, not conclusions of these finite checks.",
        "Certifies no continuous billiard pressure bound, strong transfer-operator estimate, raw pointwise LLT, or long-time inverse Jacobian theorem.",
        "Uses exact rational arithmetic and explicit exceptions; normal and optimized Python must yield identical deterministic output.",
    ])


if __name__=="__main__":
    main()
