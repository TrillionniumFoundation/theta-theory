#!/usr/bin/env python3
"""Independent finite controls for A2 v60, not theorem or billiard-realization certificates.
Requires SymPy and mpmath. No author checker is imported; no removable assertions.
"""
import json
from fractions import Fraction as F
import mpmath as mp
import sympy as sp


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def operator_controls():
    z = sp.Symbol('z')
    q, top = 3, 14
    A, phi, w = 1+z/4, z/3+z*z/24, sp.Rational(1,2)+z/5
    columns = []
    for n in range(q, top+1):
        p = sp.Poly(sp.expand(A*z**n+w*phi**n), z)
        columns.append([p.nth(k) for k in range(q, top+1)])
    L = sp.Matrix.hstack(*(sp.Matrix(c) for c in columns))
    for i in range(L.rows):
        require(L[i,i] == 1+sp.Rational(1,2)*sp.Rational(1,3)**(q+i), 'Graded block')
        for j in range(i+1,L.cols):
            require(L[i,j] == 0, 'Triangularity')
    require(L*L.inv() == sp.eye(L.rows), 'Exact finite inverse')
    # Genuine kernel despite invertible multiplier and a contractive argument.
    f = z**q/(1+z/4)
    resonant = sp.cancel((1+z/4)*f-2**q*(1+z/8)*f.subs(z,z/2))
    require(resonant == 0, 'Resonance control')
    # a^{-1}=4/3, W=9, rho=1/2, m=7.
    nu = F(4,3)*9*F(1,2)**7/(1-F(1,2)**7)
    require(nu < 1, 'Resonant high tail must still be small')
    return {'finite_quotient_dimension':L.rows,'nonlinear_argument':str(phi),
            'exact_inverse_checked':True,'resonant_kernel':str(f),
            'resonant_tail_bound':str(nu),'resonant_degree':q}


def interpolation_controls():
    mp.mp.dps = 80
    configurations = [(mp.mpf(1)/40,mp.mpf(1)/5,mp.mpf(1)/2),
                      (mp.mpf(1)/10,mp.mpf(1)/4,mp.mpf(3)/4),
                      (mp.mpf(1)/8,mp.mpf(1)/4,mp.mpf(51)/100)]
    balances, nodes, monomials = 0, 0, 0
    records=[]
    for s,r,v in configurations:
        A=2*(r+s)/s; b=(r+s)/(v-s); theta=mp.log(1/b)/mp.log(A/b)
        require(0<b<1 and 0<theta<1, 'Admissible interpolation radii')
        # Integer rounding near endpoints and across many scales.
        for exponent in [mp.mpf(1)/100,mp.mpf(1)/2]+list(range(1,81)):
            eps=mp.power(10,-exponent)
            n=int(mp.ceil(mp.log(1/eps)/mp.log(A/b)))
            target=eps**theta
            require(eps*A**(n-1) <= target*(1+mp.mpf('1e-70')), 'First balance term')
            require(b**n <= target*(1+mp.mpf('1e-70')), 'Second balance term')
            balances+=1
        for n in range(1,41):
            for k in range(1,n+1):
                angle=(2*k-1)*mp.pi/(2*n)
                derivative=2**(1-n)*s**(n-1)*n/abs(mp.sin(angle))
                require(derivative >= n*(s/2)**(n-1)*(1-mp.mpf('1e-70')), 'Nodal derivative')
                nodes+=1
        for n in range(1,101):
            eps=s**n
            require(r**n <= (1+v/(v-r))*eps**theta, 'Monomial restriction bound')
            monomials+=1
        records.append({'s':str(s),'r':str(r),'contour':str(v),'theta':str(theta),
                        'theta_over_3':str(theta/3)})
    return {'balanced_integer_choices':balances,'chebyshev_nodal_derivatives':nodes,
            'exact_norm_monomial_cases':monomials,'radii':records}


def density_controls():
    # Algebraic density model only: no global or local graph realization is asserted.
    pts=[F(k,40) for k in range(-4,5)]
    a=F(3,40); d=F(1)
    count=0
    for cubic in [F(-1,3),F(0),F(2,5)]:
        def S(x): return F(3,4)*x*x+cubic*x**3+F(1,5)*x**4
        for mode in range(3):
            # At mode 2 the separate positive factors are not differentiable at zero.
            def U(x): return 1+(abs(x) if mode==2 else (mode+1)*x*x)
            def V(y): return 2+(abs(y) if mode==2 else F(1,3)*(mode+1)*y)
            def f(u,v): return F(5,7)*U(u)*V(v)*(d-S(u)-S(v))
            def R(u,v): return f(u,v)*f(0,0)/(f(u,0)*f(0,v))
            anchor=S(a)/(d-S(a))
            require(1-R(a,a)==anchor**2, 'Scalar anchor')
            for u in pts:
                for v in pts:
                    require(1-R(u,v)==S(u)*S(v)/((d-S(u))*(d-S(v))), 'Separate-factor cancellation')
                    count+=1
                T=(1-R(u,a))/anchor
                require(d*T/(1+T)==S(u), 'Signed action recovery')
    return {'exact_four_density_identities':count,'exact_action_recoveries':9*len(pts),
            'nondifferentiable_positive_factors_tested':True,
            'scope':'Algebraic factorization tests only; no billiard realization or nuisance estimation.'}


def weak_norm_controls():
    # T_h(x,y)=(1-|x|/h)_+(1-|y|/h)_+.
    # Integral T_h=h^2, sup T_h=1. Therefore sup(h T_h)^3=integral(h T_h).
    x, y, a = sp.symbols('x y a', positive=True)
    tent_integral = 4*sp.integrate(sp.integrate(a*(1-x/a)*(1-y/a), (x,0,a)), (y,0,a))
    require(sp.simplify(tent_integral-a**3)==0, 'Exact two-dimensional tent integral')
    rows=[]
    for n in range(1,21):
        h=F(1,2**n)
        require(tent_integral.subs(a,sp.Rational(h.numerator,h.denominator))==sp.Rational((h**3).numerator,(h**3).denominator), 'Tent scaling')
        rows.append({'width':str(h),'fixed_Lipschitz_sup':str(h),
                     'fixed_Lipschitz_L1':str(h**3),
                     'no_regularization_sup':'1','no_regularization_L1':str(h*h)})
    # On [-1,1]^2, p=1/4 and p_tilde=1/4+delta*sin(2*pi*x/delta)/(8*pi),
    # delta=2/m. All grid-cell integrals of the difference vanish. Its gradient
    # has norm <=1/4 while its L1 norm is delta/pi^2>0. This is NOT the billiard model.
    histogram=[{'cells_per_side':m,'delta':str(F(2,m)),'cell_mass_difference':'0',
                'L1_difference':f'{F(2,m)}/pi^2','Lipschitz_bound':'1/4'} for m in [2,4,8,16,32]]
    for item in histogram:
        m=item['cells_per_side']; delta=sp.Rational(2,m)
        positive_half=sp.integrate(sp.sin(2*sp.pi*x/delta), (x,0,delta/2))
        require(sp.simplify(2*m*2*positive_half*delta/(8*sp.pi)-delta/sp.pi**2)==0, 'Histogram L1 norm')
        for k in range(m):
            lo=-1+k*delta; hi=lo+delta
            require(sp.integrate(sp.sin(2*sp.pi*x/delta),(x,lo,hi))==0, 'Exact cell integral')
    return {'tent_scalings':rows,'fixed_grid_bias_controls':histogram,
            'scope':'General Lipschitz functions/densities, not optimality or nonidentifiability within the billiard subclass.'}


if __name__=='__main__':
    print(json.dumps({'scope':'Finite exact algebra and high-precision scalar controls only.',
                      'imports_author_checker':False,'operator':operator_controls(),
                      'interpolation':interpolation_controls(),'density':density_controls(),
                      'weak_norm':weak_norm_controls()},indent=2,sort_keys=True))
