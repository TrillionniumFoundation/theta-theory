#!/usr/bin/env python3
"""Finite exact-algebra checks for the v71 review. Requires SymPy.
These checks neither import manuscript code nor certify analytic estimates.
"""
import json
import sympy as s

def require(value, message):
    if not value:
        raise ArithmeticError(message)

def main():
    d1, d2, h = s.symbols('d1 d2 h')
    q = d2*(d1-h)/(d1*(d2-h))
    extracted = d1*d2*(1-q)/(d2-d1*q)
    require(s.cancel(extracted-h) == 0, 'Two-offset rational identity')
    require(s.cancel(d2-d1*q-d2*(d2-d1)/(d2-h)) == 0, 'Denominator identity')
    cofactor_cases = 0
    for r in (2, 3, 5):
        k = [s.Rational(i+3, i+2) for i in range(r)]
        mass = [s.Rational(i+2, i+3) for i in range(r)]
        M = s.eye(2)
        for i in range(r):
            Q = s.Matrix([[1+mass[i]/k[i], 1/k[i]], [mass[i], 1]])
            M = Q*M
        require(M.det() == 1, 'Transfer determinant')
        for n in (1, 2, 3):
            N = r*n
            H = s.zeros(N-1)
            for j in range(1, N):
                i = j % r
                H[j-1,j-1] = k[(j-1)%r]+k[i]+mass[i]
                if j < N-1:
                    H[j-1,j] = H[j,j-1] = -k[i]
            cofactor = s.prod(k[j%r] for j in range(N))/H.det()
            require(cofactor == 1/(M**n)[0,1], 'Finite cofactor vs monodromy')
            require((M**n)[0,1] == M[0,1]*s.chebyshevu(n-1,s.trace(M)/2), 'Chebyshev normalization')
            cofactor_cases += 1
    signed_cases = 0
    for r in (2, 3, 4, 5):
        sigma = [s.Rational((-1)**(j+1), j+3) for j in range(r)]
        lam = s.prod(sigma)
        for degree in (2, 3, 5):
            T = s.zeros(r)
            for i in range(r): T[i,(i+1)%r] = sigma[i]**degree
            I = s.eye(r)
            require(T**r == lam**degree*I, 'Signed cycle power')
            C = (I+T)*(I-T).inv()
            require(C.det() == (1-(-1)**r*lam**degree)/(1-lam**degree), 'Signed determinant')
            require(C*((I-T)*(I+T).inv()) == I, 'Response inverse')
            signed_cases += 1
    action = [s.Rational(1,10), s.Integer(10)]
    z = [s.Integer(0), s.Rational(109,11)]
    mapped = [max(s.Integer(0), action[i]-1+1/(1+action[(i+1)%2]+z[(i+1)%2])) for i in range(2)]
    require(mapped == z, 'Excluded quadratic-image example')
    alpha, omega, Gamma = s.symbols('alpha omega Gamma', positive=True)
    beta = alpha*omega/(omega+alpha*Gamma)
    require(s.simplify(alpha*(1-Gamma*alpha/(omega+alpha*Gamma))-beta) == 0, 'Charged exponent balance')
    out = {'status':'passed', 'scope':'Finite exact identities only, not a proof certificate.',
           'sympy_version':s.__version__, 'author_modules_imported':False,
           'two_offset_rational_identity':True, 'two_offset_denominator_identity':True,
           'cofactor_monodromy_chebyshev_cases':cofactor_cases,
           'signed_cyclic_inverse_determinant_cases':signed_cases,
           'excluded_quadratic_image_example':True, 'charged_exponent_balance':True}
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
