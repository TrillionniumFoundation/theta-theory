"""Exact finite regressions and adversarial source-binding tests for Round 47.

These tests check identities/implementations, not the validity of every
infinite-dimensional theorem. The all-depth arguments are in the manuscript.
"""
from __future__ import annotations
from fractions import Fraction as F
from math import comb, factorial, log
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"tools"))
from round47_certificates import (Box, ResourceLimit, generator, jacobi_matrix,
    matvec, step_polynomial, grid_certificate, outer_confidence)
from verify_round47 import (VerificationError, git_blob, verify_source, tex_graph,
    strip_comments, check_recorded_inputs)


def multiply(A, B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))), F(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def inverse(A):
    n = len(A)
    rows = [[F(v) for v in row]+[F(i == j) for j in range(n)]
            for i, row in enumerate(A)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [v/scale for v in rows[j]]
        for i in range(n):
            if i != j:
                scale = rows[i][j]
                rows[i] = [v-scale*w for v, w in zip(rows[i], rows[j])]
    return [row[n:] for row in rows]


def moments(J, degree):
    x = [F(1)]+[F(0)]*(len(J)-1)
    out = []
    for _ in range(degree+1):
        out.append(x[0])
        x = matvec(J, x)
    return out


def response_v(A, degree):
    x = [F(0)]*len(A)
    x[len(A)//2] = F(1)
    x = matvec(A, x)
    out = []
    for _ in range(degree+1):
        out.append(x[0])
        x = matvec(A, x)
    return out


def monic_from_moments(mu, degree):
    if degree == 0:
        return [F(1)]
    H = [[mu[i+j] for j in range(degree)] for i in range(degree)]
    low = matvec(inverse(H), [-mu[degree+i] for i in range(degree)])
    return low+[F(1)]


def quadratic(poly, mu, shift=0):
    return sum((x*y*mu[i+j+shift] for i, x in enumerate(poly)
                for j, y in enumerate(poly)), F(0))


class AlgebraTests(unittest.TestCase):
    def setUp(self):
        self.c = F(5, 4)
        self.a = [F(1, 2)+F(i, 100) for i in range(6)]
        self.b = [F(3)+F(i, 10) for i in range(7)]
        self.J = jacobi_matrix(self.a, self.b)
        self.A = generator(self.c, self.a, self.b)

    def test_block_polynomial_identity(self):
        AA = multiply(self.A, self.A)
        n = len(self.J)
        for i in range(2*n):
            for j in range(2*n):
                expected = -self.J[i % n][j % n] if i//n == j//n else F(0)
                self.assertEqual(AA[i][j]+self.c*self.A[i][j], expected)

    def test_closed_response_moment_formula(self):
        mu = moments(self.J, 6)
        v = response_v(self.A, 12)
        self.assertEqual(v[0], 1)
        self.assertEqual(-v[1], self.c)
        for m in range(7):
            recovered = (-1)**m*sum((comb(m, k)*self.c**(m-k)*v[m+k]
                                     for k in range(m+1)), F(0))
            self.assertEqual(recovered, mu[m])

    def test_monic_gram_factorization(self):
        mu = moments(self.J, 12)
        for n in range(1, 7):
            H = [[mu[i+j] for j in range(n)] for i in range(n)]
            inv = inverse(H)
            calculated = [[F(0)]*n for _ in range(n)]
            rho_product = F(1)
            for k in range(n):
                p = monic_from_moments(mu, k)
                rho = quadratic(p, mu)
                self.assertEqual(rho, rho_product)
                pad = p+[F(0)]*(n-len(p))
                for i in range(n):
                    for j in range(n):
                        calculated[i][j] += pad[i]*pad[j]/rho
                rho_product *= self.a[k]**2 if k < len(self.a) else 1
            self.assertEqual(calculated, inv)

    def test_reconstruction_including_depth_zero(self):
        v = response_v(self.A, 20)
        c = -v[1]
        mu = [(-1)**m*sum((comb(m, k)*c**(m-k)*v[m+k]
                           for k in range(m+1)), F(0)) for m in range(11)]
        for j in range(5):
            p = monic_from_moments(mu, j)
            p_next = monic_from_moments(mu, j+1)
            rho = quadratic(p, mu)
            self.assertEqual(quadratic(p, mu, 1)/rho, self.b[j])
            self.assertEqual(quadratic(p_next, mu)/rho, self.a[j]**2)

    def test_vandermonde_induced_norm(self):
        for N in range(1, 10):
            V = [[F(k**r, factorial(r)) for r in range(N+1)] for k in range(N+1)]
            value = max(sum(abs(x) for x in row) for row in inverse(V))
            self.assertLessEqual(value, 2**N*comb(2*N, N))
            self.assertLessEqual(2**N*comb(2*N, N), 8**N)

    def test_return_path_first_changed_derivative(self):
        for J in range(5):
            b = list(self.b)
            delta = F(1, 7)
            b[J] += delta
            changed = generator(self.c, self.a, b)
            x, y = [F(0)]*len(self.A), [F(0)]*len(self.A)
            x[len(self.b)] = y[len(self.b)] = F(1)
            # h^(r)(0) = ell A^(r-1) B for r >= 1.
            for r in range(1, 4*J+5):
                difference = y[0]-x[0]
                if r < 4*J+4:
                    self.assertEqual(difference, 0)
                else:
                    expected = -delta
                    for a in self.a[:J]:
                        expected *= a*a
                    self.assertEqual(difference, expected)
                x, y = matvec(self.A, x), matvec(changed, y)

    def test_shallow_ratio_and_exponent_ledger(self):
        Q = F(16)
        for k in range(1, 25):
            S, A = Q**k, Q**(5*k)
            V = k*A*(1+k*S)
            R = S*S+2*Q**(2*k)*S*V
            T = S*S+2*Q**(2*k+1)*S*V
            self.assertLessEqual(V, Q**(9*k))
            self.assertLessEqual(R, Q**(13*k))
            self.assertLessEqual(T, Q**(14*k))
            self.assertLessEqual((T+Q*R)*Q**(2*k), Q**(17*k))
            bound_a = (Q**(13*(k+1))+Q**2*Q**(13*k))*Q**(2*k+1)/2
            self.assertLessEqual(bound_a, Q**(15*(k+1)))
        self.assertLessEqual(Q**14/2, Q**17)  # J=0 a_0 bound.

    def test_exact_posterior_exponent(self):
        self.assertEqual(-F(13, 32)+F(3, 32)+F(1, 16), -F(1, 4))

    def test_step_polynomial_first_four_orders(self):
        t = F(1, 10)
        A = generator(F(1), [], [F(2)])
        self.assertEqual(step_polynomial(A, t, 3), t*t/2-t**3/6-t**4/24)


class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.box = Box(F(1), F(2), F(1, 2), F(1), F(3), F(4), F(1))

    def test_exact_grid_remainders_and_law_masses(self):
        for mode in ("compact", "long"):
            for J in (0, 1, 3):
                for delta in (F(1), F(1, 64)):
                    cert = grid_certificate(self.box, J, delta, mode)
                    cert.validate()
                    K = (cert.order-8)//4
                    expected = F(2)**(-K-3 if mode == "compact" else -K-1)/cert.order
                    self.assertEqual(cert.atom_mass, expected)
                    self.assertGreater(cert.separation, 0)
                    if mode == "compact":
                        self.assertEqual(cert.order*cert.spacing, self.box.horizon/4)

    def test_grid_search_cap_is_not_a_false_certificate(self):
        with self.assertRaises(ResourceLimit):
            grid_certificate(self.box, 1, F(1, 100), "long", max_order=12)

    def test_reject_float_and_invalid_box(self):
        with self.assertRaises(TypeError):
            grid_certificate(self.box, 0, 0.5)
        with self.assertRaises(ValueError):
            Box(1, 2, 1, 2, 3, 4)

    def test_long_law_mass_and_mean_with_exact_tail(self):
        u = 1/(256*self.box.lam)
        for M in (0, 1, 5, 20):
            mass = sum((F(2)**(-K-1) for K in range(M+1)), F(0))
            mean = sum((F(2)**(-K-1)*u*(4*K+9)/2 for K in range(M+1)), F(0))
            self.assertEqual(mass+F(2)**(-M-1), 1)
            missing_mean = u*F(4*M+17, 2)*F(2)**(-M-1)
            self.assertEqual(mean+missing_mean, 13*u/2)

    def test_compact_law_half_mass(self):
        # Exact rectangular truncation plus its geometric complement.
        for J, S in ((0, 1), (3, 4), (8, 9)):
            mass = sum((F(2)**(-k-s-2) for k in range(J+1)
                        for s in range(1, S+1)), F(0))
            self.assertEqual(mass, F(1, 2)*(1-F(2)**(-J-1))*(1-F(2)**(-S)))

    def test_explicit_visit_budget_scalar_inequality(self):
        for B in (1., 2., 100., 1e12):
            for C in (4., 100., 1e12):
                L = log(2.718281828459045*C*(16*B)**2)
                n = 16*B*L
                self.assertGreaterEqual(n, B*log(C*n*n))

    def test_outer_union_contains_center_and_is_complete(self):
        t = F(1, 1000)
        A = generator(F(3, 2), [F(3, 4)], [F(7, 2), F(7, 2)])
        H = step_polynomial(A, t, 4)
        result = outer_confidence(self.box, 0, [(t, H-F(1, 100), H+F(1, 100))],
                                  tail_depth=1, mesh_radius=F(1), taylor_order=4)
        self.assertTrue(result.complete)
        self.assertEqual(result.examined_boxes, 1)
        self.assertEqual(len(result.boxes), 1)
        for interval, value in zip(result.boxes[0], (F(3, 2), F(3, 4), F(7, 2))):
            self.assertLessEqual(interval[0], value)
            self.assertLessEqual(value, interval[1])

    def test_outer_cap_raises_before_partial_enumeration(self):
        with self.assertRaises(ResourceLimit):
            outer_confidence(self.box, 0, [(F(1, 1000), F(-1), F(1))],
                             tail_depth=1, mesh_radius=F(1, 100), taylor_order=4,
                             max_boxes=1)

    def test_outer_infeasible_band_is_certified_empty(self):
        result = outer_confidence(self.box, 0, [(F(1, 1000), F(100), F(101))],
                                  tail_depth=1, mesh_radius=F(1), taylor_order=4)
        self.assertTrue(result.complete)
        self.assertEqual(result.boxes, ())


class SourceBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="round47-test-")
        self.root = Path(self.temp.name)
        self.command("init", "-q")
        self.command("config", "user.name", "Round47 test fixture")
        self.command("config", "user.email", "fixture@example.invalid")
        (self.root/"sub").mkdir()
        (self.root/"round47").mkdir()
        (self.root/"main.tex").write_text("\\documentclass{article}\n\\input{sub/child}\n")
        (self.root/"sub/child.tex").write_text("Fixture only.\n")
        self.roots = ("main.tex",)
        self.support = ()
        self.write_manifest()
        self.sha = self.commit("source fixture")

    def tearDown(self):
        self.temp.cleanup()

    def command(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.STDOUT).decode().strip()

    def commit(self, message):
        self.command("add", "--all")
        self.command("commit", "-qm", message)
        return self.command("rev-parse", "HEAD")

    def write_manifest(self, omit=(), fake=None):
        names = tex_graph(self.root, self.roots) | set(self.support)
        entries = {name: {"git_blob": git_blob((self.root/name).read_bytes())}
                   for name in names if name not in omit}
        if fake:
            entries[fake]["git_blob"] = "f"*40
        value = {"schema": 1, "roots": list(self.roots), "support": list(self.support), "files": entries}
        (self.root/"round47/SOURCE_MANIFEST.json").write_text(json.dumps(value, sort_keys=True))

    def verify(self, sha=None):
        return verify_source(self.root, sha or self.sha, roots=self.roots, support=self.support)

    def test_valid_source_commit_passes(self):
        result = self.verify()
        self.assertTrue(result["source_bound"])
        self.assertEqual(result["source_commit"], self.sha)

    def test_nonexistent_well_formed_commit_is_rejected(self):
        with self.assertRaises(VerificationError):
            self.verify("f"*40)

    def test_short_alias_is_rejected(self):
        with self.assertRaises(VerificationError):
            self.verify("HEAD")

    def test_omitted_active_input_is_rejected(self):
        self.write_manifest(omit=("sub/child.tex",))
        sha = self.commit("invalid omitted-input fixture")
        with self.assertRaises(VerificationError):
            self.verify(sha)

    def test_working_source_mutation_is_rejected(self):
        (self.root/"sub/child.tex").write_text("Changed source.\n")
        with self.assertRaises(VerificationError):
            self.verify()

    def test_committed_false_manifest_is_rejected(self):
        self.write_manifest(fake="sub/child.tex")
        sha = self.commit("invalid false-digest fixture")
        with self.assertRaises(VerificationError):
            self.verify(sha)

    def test_working_manifest_mutation_is_rejected(self):
        path = self.root/"round47/SOURCE_MANIFEST.json"
        path.write_text(path.read_text()+"\n")
        with self.assertRaises(VerificationError):
            self.verify()

    def test_artifact_only_descendant_is_allowed(self):
        (self.root/"result.pdf").write_bytes(b"fixture artifact, not a real PDF")
        head = self.commit("artifact-only fixture")
        result = self.verify()
        self.assertEqual(result["source_commit"], self.sha)
        self.assertEqual(result["checkout_commit"], head)

    def test_source_changed_in_descendant_is_rejected(self):
        (self.root/"sub/child.tex").write_text("Changed in descendant.\n")
        self.commit("source mutation fixture")
        with self.assertRaises(VerificationError):
            self.verify()

    def test_local_package_cannot_be_omitted(self):
        (self.root/"main.tex").write_text("\\documentclass{article}\n\\usepackage{localfixture}\n\\input{sub/child}\n")
        (self.root/"localfixture.sty").write_text("% fixture package\n")
        self.write_manifest(omit=("localfixture.sty",))
        sha = self.commit("invalid omitted local package fixture")
        with self.assertRaises(VerificationError):
            self.verify(sha)

    def test_dynamic_filename_rejected(self):
        (self.root/"main.tex").write_text("\\input{\\selectedfile}\n")
        with self.assertRaises(VerificationError):
            tex_graph(self.root, self.roots)

    def test_unbraced_input_rejected(self):
        (self.root/"main.tex").write_text("\\input sub/child.tex\n")
        with self.assertRaises(VerificationError):
            tex_graph(self.root, self.roots)

    def test_parent_path_rejected(self):
        (self.root/"main.tex").write_text("\\input{../outside.tex}\n")
        with self.assertRaises(VerificationError):
            tex_graph(self.root, self.roots)

    def test_comments_do_not_create_phantom_inputs(self):
        (self.root/"main.tex").write_text("% \\input{missing}\n\\input{sub/child}\n")
        self.assertEqual(tex_graph(self.root, self.roots), {"main.tex", "sub/child.tex"})
        self.assertIn("\\%", strip_comments("x\\%y % comment"))
        self.assertNotIn("comment", strip_comments("x\\%y % comment"))

    def test_recorded_undeclared_input_rejected(self):
        build = self.root/"freshbuild"
        build.mkdir()
        extra = self.root/"surprise.tex"
        extra.write_text("undeclared")
        fls = build/"main.fls"
        fls.write_text("INPUT "+str(extra)+"\n")
        with self.assertRaises(VerificationError):
            check_recorded_inputs(self.root, fls, {"main.tex", "sub/child.tex"}, build)

    def test_recorded_generated_auxiliary_allowed(self):
        build = self.root/"freshbuild"
        build.mkdir()
        aux = build/"main.aux"
        aux.write_text("fixture generated auxiliary")
        fls = build/"main.fls"
        fls.write_text("INPUT "+str(aux)+"\nINPUT "+str(self.root/"main.tex")+"\n")
        check_recorded_inputs(self.root, fls, {"main.tex", "sub/child.tex"}, build)

if __name__ == "__main__":
    unittest.main()
