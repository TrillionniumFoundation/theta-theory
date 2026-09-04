"""Exact finite algebra and source regression tests, not a proof assistant."""
from fractions import Fraction as F
from math import factorial, comb
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def solve(a, b):
    n = len(b)
    x = [[F(v) for v in row] + [F(bi)] for row, bi in zip(a, b)]
    for k in range(n):
        p = next(i for i in range(k, n) if x[i][k])
        x[k], x[p] = x[p], x[k]
        d = x[k][k]
        x[k] = [v / d for v in x[k]]
        for i in range(n):
            if i != k:
                d = x[i][k]
                x[i] = [v - d * w for v, w in zip(x[i], x[k])]
    return [row[-1] for row in x]


def apply_j(v, a, b):
    return [b[i] * v[i] - (a[i-1] * v[i-1] if i else 0)
            - (a[i] * v[i+1] if i+1 < len(v) else 0) for i in range(len(v))]


def moments(a, b, order):
    v = [F(1)] + [F(0)] * (len(b)-1)
    out = []
    for _ in range(order+1):
        out.append(v[0])
        v = apply_j(v, a, b)
    return out


def response_jets(c, a, b, order):
    old = [F(1)] + [F(0)] * (len(b)-1)
    v = [-c * x for x in old]
    out = [old[0], v[0]]
    for _ in range(2, order+1):
        jold = apply_j(old, a, b)
        old, v = v, [-c*x-y for x, y in zip(v, jold)]
        out.append(v[0])
    return out


def recover_moments(v, order):
    c = -v[1]
    mu = [F(1)]
    for m in range(1, order+1):
        previous = sum((-1)**k * comb(2*m-k, 2*m-2*k)
                       * c**(2*m-2*k) * mu[k] for k in range(m))
        mu.append((-1)**m * (v[2*m]-previous))
    return c, mu


def gram(mu, depth):
    polynomials, norms = [], []
    for j in range(depth+2):
        p = solve([[mu[r+s] for s in range(j)] for r in range(j)],
                  [-mu[j+r] for r in range(j)]) + [F(1)] if j else [F(1)]
        polynomials.append(p)
        norms.append(sum(p[r]*p[s]*mu[r+s] for r in range(j+1) for s in range(j+1)))
    diagonal = []
    for j in range(depth+1):
        p = polynomials[j]
        diagonal.append(sum(p[r]*p[s]*mu[r+s+1]
                            for r in range(j+1) for s in range(j+1))/norms[j])
    return [norms[j+1]/norms[j] for j in range(depth+1)], diagonal, norms


def shift_one(coefficients):
    """Exact coefficients of P(z+1), low power first."""
    return [sum(coefficients[j]*comb(j,k) for j in range(k,len(coefficients)))
            for k in range(len(coefficients))]


class Round45Tests(unittest.TestCase):
    def test_exact_moment_and_gram_reconstruction(self):
        for depth in range(6):
            a = [F(1,4)+F(i,100) for i in range(depth+4)]
            b = [F(2)+F(i,20) for i in range(depth+5)]
            c = F(7,8)
            m = 2*depth+2
            mu = moments(a,b,m)
            v = response_jets(c,a,b,2*m)
            recovered_c, recovered = recover_moments(v,m)
            self.assertEqual(recovered_c,c)
            self.assertEqual(recovered,mu)
            a2, diag, norms = gram(mu,depth)
            self.assertEqual(a2,[x*x for x in a[:depth+1]])
            self.assertEqual(diag,b[:depth+1])
            prod = F(1)
            for j,rho in enumerate(norms):
                self.assertEqual(rho,prod)
                prod *= a[j]**2

    def test_all_depth_polynomial_certificates(self):
        # Each difference is nonnegative for j=z+1, z>=0.
        certificates = {
            'V_table': [-1,-3,4],       # 8j²-(4j²+3j+1)
            'R_table': [-2,-3,5],       # 13j²-(8j²+3j+2)
            'T_table': [-3,-3,6],       # 14j²-(8j²+3j+3)
            'b_ratio': [-1,-2,3],      # 17j²-(14j²+2j+1)
            'a_ratio': [0,2,2],        # 15(j+1)²-[13(j+1)²+2+2j]
            'jet_composition': [-4,-16,31], # 64j²-[4(2j+1)²+17j²]
            'log_prefactor': [0,-12,-548,560], # 4400j³-[3840j³+548j²+12j]
        }
        for name, coefficients in certificates.items():
            shifted = shift_one(coefficients)
            self.assertTrue(all(c>=0 for c in shifted),(name,shifted))
        self.assertEqual(shift_one(certificates['jet_composition']),[11,46,31])
        # Preserve the exact old counterexamples as a regression test.
        self.assertEqual([j for j in range(8)
             if 4*(2*j+3)**2+8*(j+1)**3>12*(j+1)**3],[0,1,2,3])

    def test_vandermonde_norm_bound(self):
        for r in range(1,13):
            a = [[F(k**j,factorial(j)) for j in range(r+1)] for k in range(r+1)]
            columns = [solve(a,[int(k==j) for k in range(r+1)]) for j in range(r+1)]
            c = max(sum(abs(columns[j][k]) for j in range(r+1)) for k in range(r+1))
            self.assertLessEqual(c,2**(r+1)*factorial(r+1))

    def test_posterior_exponent_arithmetic(self):
        self.assertEqual(-F(13,32)+F(3,32)+F(1,16),-F(1,4))
        self.assertEqual(F(20,80),F(1,4))
        for j in range(100):
            self.assertLessEqual(2*(4*j+8)+3,20*(j+1))

    def test_visit_allocation_and_grid(self):
        for n in (1,2,10,100):
            self.assertEqual(sum(F(1,m*(m+1)) for m in range(1,n+1)),1-F(1,n+1))
        for depth in range(20):
            r = 4*depth+8
            cells = [(depth,1,k) for k in range(1,r+1)]
            self.assertEqual(len(cells),r)
            self.assertTrue(all(k>0 for _,_,k in cells))

    def test_source_graph_and_references(self):
        seen = set()
        def visit(path):
            self.assertTrue(path.is_file(),str(path))
            if path in seen:return
            seen.add(path)
            for relative in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
                visit(ROOT/relative)
        visit(ROOT/'ROUND45_REVISION.tex')
        self.assertEqual(set((ROOT/'round45').glob('*.tex')),seen-{ROOT/'ROUND45_REVISION.tex'})
        text = '\n'.join(p.read_text() for p in seen)
        labels = re.findall(r'\\label\{([^}]+)\}',text)
        self.assertEqual(len(labels),len(set(labels)))
        refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
        self.assertFalse(set(refs)-set(labels),set(refs)-set(labels))
        self.assertIn(r'L_J=Q^{64(J+1)^2}',text)
        self.assertNotIn(r'Q^{12(J+1)^3}',text)
        self.assertIn(r'\Psi_n(q_n/16)',text)
        self.assertIn('supermartingale',text)
        self.assertIn('positive-time cells',text)
        self.assertIn(r'(1+\log(i+1))',text)


if __name__ == '__main__':
    unittest.main()
