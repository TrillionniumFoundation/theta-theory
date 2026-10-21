#!/usr/bin/env python3
"""Finite analytic diagnostics for native 323, never a continuum certificate.

All comparisons use exact rational arithmetic or symbolic identities.  The
quadratic examples are actual explicitly defined analytic functions on closed
elliptic sectors/annuli; they are not claimed to be realized billiard words.
Runtime timestamps and optimization flags belong in the execution receipt,
not this deterministic mathematical JSON.  No assertion statement is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

import sympy as s


class Audit:
    def __init__(self):
        self.counts = Counter()

    def require(self, condition, label, group):
        if not bool(condition):
            raise ArithmeticError(f'{group}: {label}')
        self.counts[group] += 1

    def equal(self, left, right, label, group):
        self.require(s.simplify(left - right) == 0, label, group)


def polynomial(coefficients, x):
    return sum((coefficient * x**i for i, coefficient in enumerate(coefficients)), Q(0))


def primitive(coefficients, x):
    return sum((coefficient * x**(i + 1) / (i + 1)
                for i, coefficient in enumerate(coefficients)), Q(0))


def stationary_points(coefficients, left, right):
    if len(coefficients) > 3:
        raise ValueError('Only degree at most two is used in the exact profile diagnostic')
    points = [left, right]
    if len(coefficients) == 3 and coefficients[2]:
        critical = -coefficients[1] / (2 * coefficients[2])
        if left < critical < right:
            points.append(critical)
    return sorted(set(points))


def profile(pieces, audit, label):
    """Exact variation of a sum of compactly supported quadratic densities.

    Each piece is (left, right, polynomial coefficients).  Endpoints can be
    taken closed: their values have no effect on the density or its variation
    as an L1 class.  Jump charges use one-sided polynomial limits.
    """
    for left, right, coefficients in pieces:
        audit.require(left < right, label + ': positive interval', 'quadratic_profiles')
        audit.require(all(isinstance(x, Q) for x in (left, right, *coefficients)),
                      label + ': rational data', 'quadratic_profiles')
    breaks = sorted({x for left, right, _ in pieces for x in (left, right)})
    mass, interior_variation, height = Q(0), Q(0), Q(0)
    for left, right in zip(breaks, breaks[1:]):
        middle = (left + right) / 2
        coefficients = [Q(0), Q(0), Q(0)]
        for start, stop, term in pieces:
            if start < middle < stop:
                for i, coefficient in enumerate(term):
                    coefficients[i] += coefficient
        critical = stationary_points(coefficients, left, right)
        values = [polynomial(coefficients, x) for x in critical]
        audit.require(min(values) >= 0, label + ': nonnegative on complete cell', 'quadratic_profiles')
        mass += primitive(coefficients, right) - primitive(coefficients, left)
        height = max(height, *values)
        interior_variation += sum((abs(b - a) for a, b in zip(values, values[1:])), Q(0))
    jumps, signed_jumps = Q(0), []
    for value in breaks:
        before = sum((polynomial(coefficients, value)
                      for left, right, coefficients in pieces if left < value <= right), Q(0))
        after = sum((polynomial(coefficients, value)
                     for left, right, coefficients in pieces if left <= value < right), Q(0))
        signed_jumps.append((value, after - before))
        jumps += abs(after - before)
    variation = jumps + interior_variation
    direct_mass = sum((primitive(coefficients, right) - primitive(coefficients, left)
                       for left, right, coefficients in pieces), Q(0))
    audit.require(mass == direct_mass, label + ': exact source/profile mass', 'quadratic_profiles')
    audit.require(2 * height <= variation, label + ': BV height factor one-half', 'quadratic_profiles')
    return {'mass': mass, 'height': height, 'interior_variation': interior_variation,
            'jump_variation': jumps, 'total_variation': variation, 'signed_jumps': signed_jumps}


def serialize(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize(item) for item in value]
    return value


def symbolic_checks(audit):
    group = 'symbolic_optical_and_coarea'
    A, D, R, c, omega = s.symbols('A D R c omega', positive=True)
    E, x, y = s.symbols('E x y', real=True)
    G = s.Matrix([[A, E], [E, D]])
    determinant = A * D - E**2
    inverse = G.inv()
    vector, perpendicular = s.Matrix([x, y]), s.Matrix([-y, x])
    chi_unscaled = (perpendicular.T * G * perpendicular)[0]
    inverse_quadratic = (vector.T * inverse * vector)[0]
    audit.equal(chi_unscaled, determinant * inverse_quadratic,
                'two-dimensional cofactor identity', group)
    grad_norm_squared = x*x + y*y
    gauss_jacobian = s.Matrix([[x, y],
        [(-y*A + x*E)/grad_norm_squared, (-y*E + x*D)/grad_norm_squared]])
    audit.equal(gauss_jacobian.det(), chi_unscaled / grad_norm_squared,
                'det D(F,arg grad F) has no missing gradient length', group)
    audit.equal(s.Matrix([[-A/R, -E/R], [E/R, D/R]]).det(),
                -determinant/R**2, 'signed endpoint-momentum determinant', group)
    derivative_pm_at_fixed_p0 = (E + D*(-A/E))/R
    audit.equal(derivative_pm_at_fixed_p0, -determinant/(R*E),
                'true implicit endpoint derivative', group)
    root_weight = R**2*omega/determinant
    h = R**2*chi_unscaled/determinant
    audit.equal(root_weight/(4*s.pi*c*h), omega/(4*s.pi*c*chi_unscaled),
                'density/root-weight equality, one normalization', group)
    audit.equal(h, R**2*inverse_quadratic, 'h includes exactly R squared', group)

    # A rational Cholesky coordinate y=Bq, valid for an arbitrary SPD example.
    # It differs from G^(1/2)q only by an orthogonal map, preserving sector angle.
    p, r = s.symbols('p r', positive=True)
    q, slope = s.symbols('q slope', real=True)
    B = s.Matrix([[p, q], [0, r]])
    quadratic_hessian = B.T*B
    direction = s.Matrix([1, slope])
    gradient = B.T*direction
    gradient_norm = (gradient.T*gradient)[0]
    gradient_perp = s.Matrix([-gradient[1], gradient[0]])
    chi_gauss = (gradient_perp.T*quadratic_hessian*gradient_perp)[0]/gradient_norm
    angle_jacobian = p*r*(1+slope**2)/gradient_norm
    audit.equal(chi_gauss, p**2*r**2*(1+slope**2)/gradient_norm,
                'anisotropic critical Gauss denominator', group)
    audit.equal(angle_jacobian/chi_gauss, 1/(p*r),
                'critical angular Jacobian cancels anisotropy exactly', group)
    beta = s.symbols('beta', nonnegative=True)
    critical_fan = omega/(4*s.pi*c) * 2*s.pi*beta/(p*r)
    audit.equal(critical_fan, omega*beta/(2*c*p*r),
                'critical fan coefficient has the required 2pi factor', group)
    critical_root = R**2*omega/(p*r)**2
    audit.equal(critical_fan, p*r*critical_root*beta/(2*R**2*c),
                'native critical coefficient equals physical inverse-root form', group)
    rho, T = s.symbols('rho T', positive=True)
    radial_mass = s.integrate(rho, (rho, 0, s.sqrt(2*T)))
    audit.equal(radial_mass, T, 'quadratic roof radial coarea r dr equals dt', group)
    audit.equal(omega/(4*s.pi*c*p*r) * 2*s.pi*beta*radial_mass,
                critical_fan*T, 'actual elliptic-sector area and roof mass', group)
    delta = s.symbols('delta', positive=True)
    audit.equal(s.limit(delta/(2*c*R*s.Rational(3, 4)), delta, 0, dir='+'),
                0, 'zero optical corner gives zero full-circle critical trace', group)
    return {'generic_cofactor_identity': 'chi=det(G)*e^T*G^(-1)*e',
            'critical_coefficient': 'omega*beta_y/(2*c_star*sqrt(det(G)))',
            'critical_example_domain': 'F=t0+|Bq|^2/2 on a closed elliptic sector',
            'critical_examples_are_billiard_realizations': False}


def rational_matrix_checks(audit):
    group = 'rational_positive_hessian_cases'
    diagonal = [Q(1, 2), Q(1), Q(2)]
    off_diagonal = [Q(-1, 3), Q(-1, 5), Q(1, 5), Q(1, 3)]
    radii = [Q(9, 20), Q(23, 50), Q(47, 100)]
    slopes = [Q(-3), Q(-2), Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1), Q(2), Q(3)]
    Lambda = Q(47, 6)
    pi_cstar = Q(91, 10000)
    cases = 0
    for A in diagonal:
        for D in diagonal:
            for E in off_diagonal:
                determinant = A*D-E*E
                audit.require(determinant > 0, 'positive definite Hessian', group)
                audit.require(max(A+abs(E), D+abs(E)) < Lambda,
                              'proved row upper bound below Lambda', group)
                for R in radii:
                    for slope in slopes:
                        x = (1-slope*slope)/(1+slope*slope)
                        y = 2*slope/(1+slope*slope)
                        chi = D*x*x - 2*E*x*y + A*y*y
                        omega = abs(E)/R
                        inverse = (D*x*x - 2*E*x*y + A*y*y)/determinant
                        u = R*R*omega/determinant
                        h = R*R*chi/determinant
                        density = omega/(4*pi_cstar*chi)
                        audit.require(x*x+y*y == 1, 'unit Gauss direction', group)
                        audit.require(chi > 0, 'positive Gauss coarea', group)
                        audit.require(h == R*R*inverse, 'cofactor and radial h', group)
                        audit.require(density == u/(4*pi_cstar*h), 'original normalized density', group)
                        audit.require(h >= R*R/Lambda, 'uniform physical h lower bound', group)
                        audit.require(density <= Lambda*u/(4*pi_cstar*R*R),
                                      'physical density upper bound', group)
                        cases += 1
    return {'cases': cases, 'matrices': len(diagonal)**2*len(off_diagonal),
            'radii': [str(value) for value in radii],
            'physical_normalization': 'pi*c_star=91/10000',
            'scope': 'Exact algebra on SPD matrices satisfying the stated upper bound; no orbit realization claim.'}


def cap_and_normalization_checks(audit):
    group = 'cap_and_physical_normalization'
    a, v, R, c, L, C = s.symbols('a v R c L C', positive=True)
    derivative = s.diff(s.atan(v/a), v)
    audit.equal(derivative, a/(a*a+v*v), 'cap angular antiderivative', group)
    cap_integral = s.integrate(a/(a*a+v*v), (v, -a, a))
    audit.equal(cap_integral, s.pi/2, 'each full physical cap angle is pi/2', group)
    for endpoint in ('initial', 'terminal'):
        for sign in (-1, 1):
            P = s.Matrix([-sign*a, v]) if endpoint == 'initial' else s.Matrix([-v, sign*a])
            tangent = P.diff(v)
            signed = s.Matrix.hstack(P, tangent).det()/(P.dot(P))
            audit.equal(signed*signed, (a/(a*a+v*v))**2,
                        endpoint + ' signed cap derivative ' + str(sign), group)
    one_side = L*C/(4*s.pi*c*R*R)*cap_integral
    audit.equal(one_side, L*C/(8*c*R*R), 'one cap charge', group)
    audit.equal(4*one_side, L*C/(2*c*R*R), 'exact four-cap charge', group)
    density = 1/(4*s.pi*c)
    audit.equal(density.subs(c, 2*c), density/2,
                'conditioning appears once, not twice', group)
    line_density = density/R
    audit.equal(line_density.subs(R, 2*R), line_density/2,
                'marked line-coordinate density has one inverse radius', group)
    arclength_density = 1/(4*s.pi*R*c)
    audit.equal(arclength_density*R, density,
                'initial angular coordinate absorbs the arclength radius', group)
    lower, upper, cap = Q(9,20), Q(47,100), Q(5,6)
    original_section_upper = Q(10600,12809)+Q(1,200)
    audit.require(original_section_upper < cap < Q(9,10),
                  'entire original section fits the proposed cap', group)
    audit.require(Q(47,6)/(2*lower**2) == Q(4700,243),
                  'four-cap physical radius coefficient', group)
    audit.require(lower < upper, 'original radius interval', group)
    return {'each_cap_angle': 'pi/2', 'four_cap_bound': 'Lambda*C_mom/(2*c_star*R_minus^2)',
            'strict_original_section_cap_gap': str(cap-original_section_upper),
            'conditioning_power': -1, 'marked_line_radius_power': -1}


def geometric_checks(audit):
    group = 'full_marked_boundary_sum'
    sigma = Q(47,59)
    for m in range(1,129):
        actual = sum((sigma**j+sigma**(m-1-j) for j in range(m)),Q(0))
        exact = 2*(1-sigma**m)/(1-sigma)
        audit.require(actual == exact, 'complete sum at m='+str(m),group)
        audit.require(actual <= 2/(1-sigma), 'uniform all-depth bound at m='+str(m),group)
    m = s.symbols('m', positive=True, integer=True)
    j = s.symbols('j', integer=True)
    exact_sigma = s.Rational(47,59)
    expression = s.summation(exact_sigma**j,(j,0,m-1))
    audit.equal(expression,(1-exact_sigma**m)/(1-exact_sigma),'symbolic complete finite geometric sum',group)
    audit.require(2/(1-sigma) == Q(59,6),'exact global marked coefficient',group)
    return {'collision_counts_checked':128,'sigma':'47/59',
            'exact_formula':'2*(1-sigma^m)/(1-sigma)','uniform_factor':'59/6'}


def quadratic_roof_checks(audit):
    # After factoring out the exact positive critical coefficient already
    # checked symbolically, these are actual roof densities on elliptic
    # sectors or annuli with radial polynomial source weights W(F-t0).
    examples = {
      'closed_critical_disk': [(Q(0),Q(1),[Q(1)])],
      'shifted_critical_ellipse': [(Q(3),Q(5),[Q(1)])],
      'closed_noncritical_annulus': [(Q(1),Q(3),[Q(1)])],
      'smooth_linear_radial_weight': [(Q(0),Q(2),[Q(1),Q(-1,2)])],
      'smooth_quadratic_radial_weight': [(Q(0),Q(2),[Q(0),Q(2),Q(-1)])],
      'positive_quadratic_radial_weight': [(Q(0),Q(2),[Q(1),Q(1),Q(-1,2)])],
      'disconnected_actual_radial_domain': [(Q(0),Q(1),[Q(1)]),(Q(2),Q(3),[Q(1)])],
      'one_roof_with_artificial_split': [(Q(0),Q(1),[Q(1)]),(Q(1),Q(2),[Q(1)])],
      'one_roof_without_artificial_split': [(Q(0),Q(2),[Q(1)])],
      'two_quadratic_sources_at_one_common_roof': [(Q(0),Q(2),[Q(1)]),(Q(1),Q(3),[Q(1)])],
    }
    origins = {
      'closed_critical_disk':[Q(0)],'shifted_critical_ellipse':[Q(3)],
      'closed_noncritical_annulus':[Q(0)],'smooth_linear_radial_weight':[Q(0)],
      'smooth_quadratic_radial_weight':[Q(0)],'positive_quadratic_radial_weight':[Q(0)],
      'disconnected_actual_radial_domain':[Q(0),Q(0)],
      'one_roof_with_artificial_split':[Q(0),Q(0)],
      'one_roof_without_artificial_split':[Q(0)],
      'two_quadratic_sources_at_one_common_roof':[Q(0),Q(1)]}
    expected = {
      'closed_critical_disk':(Q(1),Q(1),Q(2)),
      'shifted_critical_ellipse':(Q(2),Q(1),Q(2)),
      'closed_noncritical_annulus':(Q(2),Q(1),Q(2)),
      'smooth_linear_radial_weight':(Q(1),Q(1),Q(2)),
      'smooth_quadratic_radial_weight':(Q(4,3),Q(1),Q(2)),
      'positive_quadratic_radial_weight':(Q(8,3),Q(3,2),Q(3)),
      'disconnected_actual_radial_domain':(Q(2),Q(1),Q(4)),
      'one_roof_with_artificial_split':(Q(2),Q(1),Q(2)),
      'one_roof_without_artificial_split':(Q(2),Q(1),Q(2)),
      'two_quadratic_sources_at_one_common_roof':(Q(4),Q(2),Q(4))}
    results = {}
    for label,pieces in examples.items():
        value = profile(pieces,audit,label)
        mass,height,variation = expected[label]
        audit.require((value['mass'],value['height'],value['total_variation']) == (mass,height,variation),
                      label+': independently specified profile values','quadratic_profiles')
        critical,regular,interior = Q(0),Q(0),Q(0)
        for origin,(left,right,coefficients) in zip(origins[label],pieces):
            incoming = polynomial(coefficients,left)
            if left == origin:
                critical += incoming
            else:
                regular += incoming
            regular += polynomial(coefficients,right)
            points = stationary_points(coefficients,left,right)
            interior += sum((abs(polynomial(coefficients,b)-polynomial(coefficients,a))
                             for a,b in zip(points,points[1:])),Q(0))
        audit.require(value['total_variation'] <= critical+regular+interior,
                      label+': complete critical/regular/interior payment','quadratic_profiles')
        value.update({'incoming_critical_fan':critical,'regular_piece_boundary_upper_bound':regular,
                      'interior_piece_variation_upper_bound':interior})
        results[label]=value
    split=results['one_roof_with_artificial_split']
    unsplit=results['one_roof_without_artificial_split']
    audit.require(split['mass']==unsplit['mass'] and split['height']==unsplit['height']
                  and split['total_variation']==unsplit['total_variation'],
                  'artificial seam cancels in signed derivative before variation','quadratic_profiles')
    audit.require(dict(split['signed_jumps'])[Q(1)]==0,'no artificial seam atom','quadratic_profiles')
    disk=results['closed_critical_disk']
    audit.require(disk['height'] > (disk['regular_piece_boundary_upper_bound']
                                  +disk['interior_piece_variation_upper_bound'])/2,
                  'omitting the critical inlet gives a provably false half-TV height claim','scope_counterexamples')
    return {'normalization':'Each profile is divided by its exact positive elliptic-sector coarea coefficient.',
            'roofs':'F(q)=t0+|Bq|^2/2 on explicit closed sectors/annuli; radial weights are the listed polynomials.',
            'these_are_realized_lorentz_orbits':False,'profiles':serialize(results)}


def counterexample_checks(audit):
    group='scope_counterexamples'
    for m in range(1,65):
        density=profile([(Q(0),Q(1,m**4),[Q(1)])],audit,'narrow_spike_'+str(m))
        audit.require(density['height']==1 and density['mass']==Q(1,m**4)
                      and density['total_variation']==2,'exact narrow spike '+str(m),group)
        audit.require(m*m*density['height']==m*m,'normalized height does not decay '+str(m),group)
        audit.require(m*m*density['mass']==Q(1,m*m),'normalized mass does decay '+str(m),group)
    m=s.symbols('m',positive=True,integer=True)
    audit.equal(s.limit(m**2/m**4,m,s.oo),0,'small normalized mass limit',group)
    audit.require(s.limit(m**2,m,s.oo)==s.oo,'divergent normalized height limit',group)

    # H=1 on union_n (4^(-n),2*4^(-n)).  Each finite ordered collection
    # of selected points below lies strictly inside an interval or a gap,
    # and gives an exact 2N lower bound for the variation of this one H.
    lower_bounds=[]
    for N in range(1,33):
        pieces=[(Q(1,4**n),Q(2,4**n),[Q(1)]) for n in range(1,N+1)]
        truncation=profile(pieces,audit,'borel_truncation_'+str(N))
        audit.require(truncation['total_variation']==2*N,'finite selector variation '+str(N),group)
        audit.require(truncation['mass']==(1-Q(1,4**N))/3,'finite selector exact mass '+str(N),group)
        samples=[]
        for n in range(N,0,-1):
            samples.extend([(Q(3,4**n*4),0),(Q(3,2*4**n),1),(Q(3,4**n),0)])
        samples=sorted(set(samples))
        audit.require(all(samples[k][0]<samples[k+1][0] for k in range(len(samples)-1)),
                      'strict ordered variation partition '+str(N),group)
        for point,value in samples:
            actual=int(any(Q(1,4**n)<point<Q(2,4**n) for n in range(1,N+2)))
            audit.require(actual==value,'true infinite-selector sample value',group)
        actual_variation=sum(abs(b[1]-a[1]) for a,b in zip(samples,samples[1:]))
        audit.require(actual_variation==2*N,'infinite selector has variation at least2N',group)
        lower_bounds.append(actual_variation)
    n=s.symbols('n',positive=True,integer=True)
    audit.equal(s.summation(s.Rational(1,4)**n,(n,1,s.oo)),s.Rational(1,3),
                'infinite Borel selector has exact mass one-third',group)
    return {
      'small_mass_does_not_pay_normalized_height':{
        'density':'f_m(t)=1_[0,m^(-4)](t)','height':'1','mass':'m^(-4)',
        'total_variation':'2','m_squared_mass_limit':'0','m_squared_height_limit':'+infinity',
        'meaning':'Even uniform BV, uniform height and vanishing normalized mass do not imply o(m^(-2)) height.'},
      'borel_restriction_does_not_inherit_BV':{
        'majorant':'p=1_[0,1], with variation2 and height1',
        'selector':'H=1_union_{n>=1}(4^(-n),2*4^(-n))',
        'selected_mass':'1/3','selected_height':'1','selected_variation':'+infinity',
        'finite_partition_lower_bound':'Var(pH)>=2N for every N',
        'checked_partition_sizes':list(range(1,33)), 'checked_lower_bounds':lower_bounds},
      'critical_fan_cannot_be_omitted':{
        'example':'Constant density on a quadratic critical disk',
        'interior_variation':'0','regular_exit_charge':'1','incoming_critical_charge':'1',
        'actual_height':'1','correct_total_variation':'2'}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--details',type=Path,help='Write exactly the deterministic JSON also printed to stdout')
    parser.add_argument('--source',type=Path,
        default=Path(__file__).resolve().parents[1]/'core/323_complete_physical_roof_variation.tex',
        help='Exact native323 source whose identity this auxiliary run records')
    args=parser.parse_args()
    source=args.source.resolve()
    if not source.is_file():
        raise FileNotFoundError(f'Native source not found: {source}')
    audit=Audit()
    symbolic=symbolic_checks(audit)
    matrices=rational_matrix_checks(audit)
    caps=cap_and_normalization_checks(audit)
    geometric=geometric_checks(audit)
    roofs=quadratic_roof_checks(audit)
    counterexamples=counterexample_checks(audit)
    result={
      'status':'passed','schema_version':1,
      'scope':'Finite exact analytic/algebraic diagnostics for native323; no continuous billiard proof certificate.',
      'source_name':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'sympy_version':s.__version__,
      'continuum_proof_certificate':False,'full_raw_pointwise_llt_proved':False,
      'physical_orbit_realizations_verified':False,
      'full_two_dimensional_BV_claimed':False,'arbitrary_Borel_selector_BV_claimed':False,
      'unbounded_insertion_roof_Linfinity_claimed':False,
      'counts':dict(sorted(audit.counts.items())),'total_checks':sum(audit.counts.values()),
      'symbolic':symbolic,'rational_matrices':matrices,'caps_and_normalization':caps,
      'complete_marked_sum':geometric,'explicit_quadratic_roofs':roofs,
      'scope_counterexamples':counterexamples,
      'determinism':'Mathematical output excludes runtime timestamps and optimization mode; separate execution receipts record them.'}
    payload=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.details:
        args.details.parent.mkdir(parents=True,exist_ok=True)
        args.details.write_text(payload)
    print(payload,end='')


if __name__=='__main__':
    main()
