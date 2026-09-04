#!/usr/bin/env python3
"""Strengthen the materialized Round 41 Jacobi result to a full posterior LDP.

This deterministic postprocessor runs immediately after materialize_round41.py.
It upgrades the one-sided closed-set estimate to matching open/closed
large-deviation bounds, makes the finite-cylinder inverse modulus uniform over
all pairs in the compact coefficient box, records the inverse stability modulus
Omega_J, and refreshes reviewer files, tests, verifier language, and hashes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R41 = ROOT / "round41"


def write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, name: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{name}: expected one target, found {count}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, new: str, name: str) -> str:
    i = text.find(start)
    if i < 0:
        raise RuntimeError(f"{name}: start marker not found")
    j = text.find(end, i + len(start))
    if j < 0:
        raise RuntimeError(f"{name}: end marker not found")
    return text[:i] + new + text[j + len(end):]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


jac_path = R41 / "infinite_jacobi.tex"
jac = jac_path.read_text(encoding="utf-8")
start = r"\begin{proposition}[Response geometry and coefficient separation]"
end = r"\begin{remark}[Genuine infinite-dimensional content]"
block = r"""\begin{proposition}[Uniform inverse-response geometry]
\label{prop:jacobi-response-geometry}
For arbitrary \(\beta,\gamma\in\mathfrak B\), put
\begin{equation}
 D(\beta,\gamma)=\sum_{m=1}^{\infty}\omega_m
 \{h_\beta(t_m)-h_\gamma(t_m)\}^2.
 \label{eq:two-point-response-metric}
\end{equation}
Then \(D^{1/2}\) is a metric on \(\mathfrak B\) that induces the product
topology.  For \(J\ge0\), define
\[
 d_J(\beta,\gamma)=\max\left\{\abs{c-\widetilde c},
 \max_{0\le j\le J}\abs{a_j-\widetilde a_j},
 \max_{0\le j\le J}\abs{b_j-\widetilde b_j}\right\},
\]
where \(\gamma=(\widetilde c,(\widetilde a_j),(\widetilde b_j))\).  The
uniform response-information modulus
\begin{equation}
 \kappa_J(\delta)=
 \inf\{D(\beta,\gamma):\beta,\gamma\in\mathfrak B,
                         \ d_J(\beta,\gamma)\ge\delta\}
 \label{eq:jacobi-separation-modulus}
\end{equation}
is strictly positive whenever the constraint set is nonempty; as usual its
infimum is \(+\infty\) when that set is empty.  Moreover the inverse modulus
\begin{equation}
 \Omega_J(r)=\sup\{d_J(\beta,\gamma):\beta,\gamma\in\mathfrak B,
                         \ D(\beta,\gamma)^{1/2}\le r\}
 \label{eq:jacobi-inverse-modulus}
\end{equation}
satisfies \(\Omega_J(r)\downarrow0\) as \(r\downarrow0\), and
\[
 d_J(\beta,\gamma)\le
 \Omega_J\bigl(D(\beta,\gamma)^{1/2}\bigr).
\]
Thus the sampled boundary response supplies a deterministic, true-value
uniform stability modulus for every finite coefficient block.
\end{proposition}

\begin{proof}
The map
\[
 \mathcal Q:\mathfrak B\longrightarrow\ell^2(\omega),\qquad
 \mathcal Q(\beta)=(h_\beta(t_m))_{m\ge1},
\]
is continuous by Lemma~\ref{lem:product-continuity} and dominated
convergence.  It is injective: equality at the dense duration set gives
equality on \([0,T]\), bounded-generator analyticity extends this equality
to \([0,\infty)\), and Theorem~\ref{thm:jacobi-reconstruction} recovers all
coefficients.  A continuous injection from the compact space
\(\mathfrak B\) into the Hausdorff space \(\ell^2(\omega)\) is a
homeomorphism onto its image.  This proves the metric and topology assertion.

For fixed \(J,\delta\), the pair set in
\eqref{eq:jacobi-separation-modulus} is compact.  If nonempty, it is disjoint
from the diagonal; injectivity and continuity therefore give a strictly
positive minimum.  If \(\Omega_J(r_k)\not\to0\) for some \(r_k\downarrow0\),
compactness would provide pairs \((\beta_k,\gamma_k)\) with a convergent
subsequence, \(D(\beta_k,\gamma_k)\to0\), but
\(d_J(\beta_k,\gamma_k)\ge\varepsilon>0\).  The limit would be two distinct
points with the same response, a contradiction.  The displayed stability
inequality follows directly from the definition of \(\Omega_J\).
\end{proof}

\begin{theorem}[Full posterior large-deviation principle on the Jacobi product]
\label{thm:jacobi-rate}
Define the good rate function
\begin{equation}
 I_{\beta_0}(\beta)=\frac{a^2}{2\sigma^2}D(\beta,\beta_0).
 \label{eq:jacobi-rate-function}
\end{equation}
For every admissible bounded-feedback sequence, every sequence of working
initial-state priors supported in the fixed Hilbert ball, and every Borel set
\(A\subset\mathfrak B\), on one event of
\(P_{\beta_0,z_0}\)-probability one,
\begin{equation}
 -\inf_{\beta\in A^\circ}I_{\beta_0}(\beta)
 \le \liminf_{n\to\infty}\frac1n\log\Pi_n^{\nu_n}(A)
 \le \limsup_{n\to\infty}\frac1n\log\Pi_n^{\nu_n}(A)
 \le-\inf_{\beta\in\overline A}I_{\beta_0}(\beta).
 \label{eq:jacobi-posterior-ldp}
\end{equation}
The convention is \(\inf\varnothing=+\infty\).  In particular, for every
closed \(F\subset\mathfrak B\),
\begin{equation}
 \limsup_{n\to\infty}\frac1n\log\Pi_n^{\nu_n}(F)
 \le-\frac{a^2}{2\sigma^2}
       \inf_{\beta\in F}D(\beta,\beta_0),
 \label{eq:jacobi-closed-set-rate}
\end{equation}
and, whenever the separated set is nonempty,
\begin{equation}
 \limsup_{n\to\infty}\frac1n
 \log\Pi_n^{\nu_n}\{d_J(\beta,\beta_0)\ge\delta\}
 \le-\frac{a^2\kappa_J(\delta)}{2\sigma^2}<0.
 \label{eq:jacobi-cylinder-rate}
\end{equation}
For each fixed Borel set and each \(\varepsilon>0\), the corresponding
\(\varepsilon\)-relaxed open and closed bounds hold in probability uniformly
over feedback segments with the common bounds \((U_J,T_J)\).
\end{theorem}

\begin{proof}
Put \(f_\beta(t)=a\{h_\beta(t)-h_{\beta_0}(t)\}\).  By
Lemma~\ref{lem:product-continuity},
\(\mathcal F=\{f_\beta:\beta\in\mathfrak B\}\) is compact in
\(C([0,T])\) and uniformly bounded.  Lemma~\ref{lem:supnorm-response-slln}
gives, on one event independent of \(\beta\),
\begin{align}
 \sup_{\beta\in\mathfrak B}
 \left|\frac1n\sum_{i=1}^nS_i\xi_i f_\beta(t_{M_i})\right|&\longrightarrow0,
 \label{eq:uniform-score-slln}\\
 \sup_{\beta\in\mathfrak B}
 \left|\frac1n\sum_{i=1}^nf_\beta(t_{M_i})^2
      -a^2D(\beta,\beta_0)\right|&\longrightarrow0.
 \label{eq:uniform-square-slln}
\end{align}
The true washout residual contributes at most
\[
 \frac{\sup_{\beta}\norm{f_\beta}_\infty}{n\sigma^2}
 \sum_{i=1}^n\abs{\eta_i^{\beta_0}(z_0)}=o(1)
\]
uniformly in \(\beta\).  Hence the ideal likelihood has the uniform limit
\begin{equation}
 \sup_{\beta\in\mathfrak B}
 \left|\frac1n\log\frac{L_n^\star(\beta)}{L_n^\star(\beta_0)}
       +I_{\beta_0}(\beta)\right|\longrightarrow0
 \quad\text{almost surely}.
 \label{eq:uniform-jacobi-likelihood-limit}
\end{equation}
Lemma~\ref{lem:washout-correction} changes an exact integrated log-likelihood
ratio by at most \(2C_n=o(n)\), uniformly in \(\beta\), the feedback segment,
and \(\nu_n\).  Therefore \eqref{eq:uniform-jacobi-likelihood-limit} also
holds for the exact integrated likelihood.

Write
\[
 \ell_n(\beta)=\frac1n\log
 \frac{L_n^{\nu_n}(\beta)}{L_n^{\nu_n}(\beta_0)},
 \qquad Z_n=\int_{\mathfrak B}e^{n\ell_n(\beta)}\Pi(d\beta).
\]
The uniform limit says \(\norm{\ell_n+I_{\beta_0}}_\infty\to0\).  Since
\(I_{\beta_0}\ge0\) and vanishes at \(\beta_0\),
\[
 \limsup_n n^{-1}\log Z_n\le0.
\]
For every \(\eta>0\), the open set
\(G_\eta=\{I_{\beta_0}<\eta\}\) contains \(\beta_0\) and has positive prior
mass by full support.  Thus
\[
 \frac1n\log Z_n\ge-\eta-
 \norm{\ell_n+I_{\beta_0}}_\infty+rac1n\log\Pi(G_\eta),
\]
and letting first \(n\to\infty\), then \(\eta\downarrow0\), proves
\begin{equation}
 \frac1n\log Z_n\longrightarrow0.
 \label{eq:jacobi-denominator-rate}
\end{equation}

If \(F\) is closed, compactness and the uniform likelihood limit give
\[
 \limsup_n\frac1n\log\int_F e^{n\ell_n(\beta)}\Pi(d\beta)
 \le-\inf_F I_{\beta_0}.
\]
Subtracting \eqref{eq:jacobi-denominator-rate} proves the closed-set bound.
If \(G\) is open, choose \(\beta\in G\) and \(\eta>0\).  Continuity of
\(I_{\beta_0}\) and regularity of the compact metric space give an open
neighbourhood \(V\) of \(\beta\) with \(V\subset G\) and
\(\sup_VI_{\beta_0}\le I_{\beta_0}(\beta)+\eta\).  Full support gives
\(\Pi(V)>0\), whence
\[
 \liminf_n\frac1n\log\int_G e^{n\ell_n(\gamma)}\Pi(d\gamma)
 \ge-I_{\beta_0}(\beta)-\eta.
\]
Use \eqref{eq:jacobi-denominator-rate}, then take the infimum over
\(\beta\in G\) and let \(\eta\downarrow0\).  Applying the open lower bound
to \(A^\circ\) and the closed upper bound to \(\overline A\) proves
\eqref{eq:jacobi-posterior-ldp}.  Equation
\eqref{eq:jacobi-cylinder-rate} follows from the uniform pair modulus in
Proposition~\ref{prop:jacobi-response-geometry}.

For the final uniform-in-probability assertion, use the same finite
supremum-norm nets as in Lemma~\ref{lem:supnorm-response-slln}.  At fixed net
resolution, the score and square deviations have laws independent of the
feedback segment, while the washout correction is dominated by the same
summable envelope for all \((U_J,T_J)\)-bounded feedback.  The resulting
uniform likelihood convergence in probability feeds verbatim into the two
Laplace bounds above.
\end{proof}

\begin{corollary}[Strong posterior consistency for the infinite Jacobi bath]
\label{thm:jacobi-consistency}
For every open neighbourhood \(U\) of \(\beta_0\) in the product topology,
\[
 \Pi_n^{\nu_n}(U^c)\longrightarrow0
 \quad P_{\beta_0,z_0}\text{-almost surely}.
\]
More precisely, the exponential rate is at most
\(-\inf_{U^c}I_{\beta_0}<0\).
\end{corollary}

\begin{proof}
The compact set \(U^c\) excludes \(\beta_0\).  The metric property in
Proposition~\ref{prop:jacobi-response-geometry} gives
\(\inf_{U^c}I_{\beta_0}>0\), and Theorem~\ref{thm:jacobi-rate} applies.
\end{proof}

\begin{remark}[Genuine infinite-dimensional content]"""
jac = replace_between(jac, start, end, block, "Jacobi LDP theorem block")
jac = replace_once(
    jac,
    r"""Every product neighbourhood constrains finitely many coefficients, and
\eqref{eq:jacobi-cylinder-rate} gives an exponential posterior rate for each
such block through the deterministic inverse-response modulus
\(\kappa_J\).  The parameter space contains an infinite sequence, the
response is nonrational, and the reconstruction iterates without a terminal
index.  Thus the statistical conclusion is stronger than qualitative
consistency while remaining intrinsic to the full infinite chain.""",
    r"""Every product neighbourhood constrains finitely many coefficients, while
\eqref{eq:jacobi-posterior-ldp} governs arbitrary Borel subsets of the complete
coefficient product.  The pairwise moduli \(\kappa_J\) and \(\Omega_J\)
convert sampled-response information into true-value-uniform stability and
exponential contraction for every finite block.  The parameter space contains
an infinite sequence, the response is nonrational, and the reconstruction
iterates without a terminal index.  Thus the statistical conclusion is a full
infinite-dimensional posterior large-deviation theorem, with strong
consistency as a strict corollary.""",
    "Jacobi significance remark",
)
write(jac_path, jac)

intro_path = R41 / "introduction.tex"
intro = intro_path.read_text(encoding="utf-8")
intro = replace_once(
    intro,
    "Consequently every closed\nset satisfies an exact exponential posterior upper bound, and every fixed\nfinite block of Jacobi coefficients contracts exponentially through a\nstrictly positive inverse-response modulus.  Qualitative strong consistency\nis an immediate corollary of this quantitative statement.",
    "Consequently the exact posterior satisfies a full good large-deviation\nprinciple on the complete coefficient product, with matching open-set lower\nand closed-set upper bounds.  Uniform pairwise moduli \\(\\kappa_J\\) and\n\\(\\Omega_J\\) convert response information into deterministic stability and\nexponential contraction for every fixed finite coefficient block.  Strong\nconsistency is an immediate strict corollary.",
    "introduction LDP summary",
)
intro = intro.replace(
    "Theorem~\\ref{thm:jacobi-rate} gives closed-set and finite-cylinder exponential\nposterior rates.",
    "Theorem~\\ref{thm:jacobi-rate} gives the full posterior large-deviation\nprinciple and its finite-cylinder exponential consequences.",
)
intro = intro.replace(
    "its rate\nfunction is the explicitly sampled response metric \\(D\\).  The coefficient\nmoduli \\(\\kappa_J\\) convert that metric rate into quantitative recovery of\nevery finite Jacobi block.",
    "its good rate\nfunction is the explicitly sampled response metric \\(D\\).  The pairwise\ncoefficient moduli \\(\\kappa_J\\) and \\(\\Omega_J\\) convert that rate into\ntrue-value-uniform quantitative recovery of every finite Jacobi block.",
)
intro = intro.replace(
    "the resulting posterior rate on the complete compact coefficient product.",
    "the resulting full posterior large-deviation principle on the complete\ncompact coefficient product.",
)
write(intro_path, intro)

main_path = ROOT / "ROUND41_REVISION.tex"
main = main_path.read_text(encoding="utf-8")
main = replace_once(
    main,
    "The posterior of every closed set has an exact exponential upper\nrate given by its sampled response distance, and every finite coefficient\nblock contracts exponentially through a positive inverse-response modulus.\nThis quantitative result implies strong posterior consistency for the entire\nsemi-infinite Jacobi operator.",
    "The exact posterior satisfies a full good large-deviation principle on the\ncomplete compact coefficient product, with rate given by sampled response\ndistance.  Uniform pairwise inverse-response moduli yield exponential\ncontraction for every finite coefficient block.  Strong consistency for the\nentire semi-infinite Jacobi operator follows as a strict corollary.",
    "abstract LDP statement",
)
write(main_path, main)

response_path = ROOT / "AUTHOR_RESPONSE_ROUND40.md"
response = response_path.read_text(encoding="utf-8")
response = response.replace(
    "an exact closed-set exponential posterior upper rate and finite-cylinder contraction via `kappa_J(delta)`.",
    "a full posterior large-deviation principle with matching open/closed bounds, plus true-value-uniform finite-cylinder stability through `kappa_J(delta)` and `Omega_J(r)`.",
)
heading = "## New positive theorem"
i = response.find(heading)
j = response.find("## Verification boundary", i)
if i < 0 or j < 0:
    raise RuntimeError("author response theorem section markers missing")
new_section = """## New positive theorem\n\nLet `I_beta0(beta)=(a^2/(2 sigma^2))D(beta,beta0)`.  For every Borel set\n`A` in the complete compact Jacobi product, the exact posterior satisfies\n\n`-inf_{A interior} I_beta0 <= liminf n^{-1} log Pi_n(A)`\n\nand\n\n`limsup n^{-1} log Pi_n(A) <= -inf_{closure A} I_beta0`\n\nalmost surely.  The denominator is proved to have exact exponential rate\nzero, so the open lower and closed upper bounds match.  The pairwise modulus\n`kappa_J(delta)` is now minimized over all parameter pairs in the compact box,\nnot only around one fixed truth, and `Omega_J(r) -> 0` gives an explicit\nvariational inverse-stability inequality.  Strong product-topology consistency\nis a strict corollary of this full large-deviation theorem.\n\n"""
response = response[:i] + new_section + response[j:]
write(response_path, response)

index_path = ROOT / "ROUND41_REVIEW_INDEX.md"
index = index_path.read_text(encoding="utf-8")
index = index.replace(
    "Complete Jacobi reconstruction, response geometry, and exponential posterior\n  rate",
    "Complete Jacobi reconstruction, uniform inverse-response geometry, and full\n  posterior large-deviation principle",
)
index = index.replace("- `thm:jacobi-rate`", "- `thm:jacobi-rate` (`eq:jacobi-posterior-ldp`)")
write(index_path, index)

ready_path = ROOT / "ROUND41_READY_FOR_REVIEW.md"
ready = ready_path.read_text(encoding="utf-8")
ready = ready.replace(
    "The generated verification record reports source tests and the\ntwo-pass LaTeX build at the revision head.",
    "The infinite-Jacobi contribution is a full posterior large-deviation\nprinciple with uniform finite-block inverse moduli.  The generated verification\nrecord reports source tests and the two-pass LaTeX build at the revision head.",
)
write(ready_path, ready)

history_path = R41 / "HISTORICAL_REUSE.md"
history = history_path.read_text(encoding="utf-8")
history = history.replace(
    "upgraded from qualitative consistency to a uniform likelihood limit and closed-set exponential posterior rate",
    "upgraded from qualitative consistency to a uniform likelihood limit, a full posterior LDP, and uniform pairwise inverse moduli",
)
history = history.replace(
    "and its closed-set\n   minima become exact posterior exponential rates.",
    "and its variational\n   minima yield a good posterior rate function with matching open/closed bounds.\n5. **Uniform inverse-response moduli.**  Compact pair geometry defines\n   `kappa_J` and `Omega_J` uniformly over all truths and alternatives.",
)
write(history_path, history)

ledger_path = R41 / "PROOF_LEDGER.json"
ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
sig = ledger["obligations"]["R40-significance"]
sig["status"] = "closed by quantitative strengthening"
sig["result"] = "full good posterior LDP, uniform pairwise inverse stability, and finite-cylinder exponential contraction"
sig["equations"] = ["eq:jacobi-posterior-ldp", "eq:jacobi-separation-modulus", "eq:jacobi-inverse-modulus"]
write(ledger_path, json.dumps(ledger, indent=2, sort_keys=True))

test_path = ROOT / "tests" / "test_round41.py"
test = test_path.read_text(encoding="utf-8")
extra_test = r'''
    def test_full_jacobi_posterior_ldp_and_uniform_inverse_moduli(self) -> None:
        text = (ROOT / "round41/infinite_jacobi.tex").read_text(encoding="utf-8")
        for label in (
            "eq:jacobi-posterior-ldp",
            "eq:jacobi-rate-function",
            "eq:jacobi-separation-modulus",
            "eq:jacobi-inverse-modulus",
            "eq:jacobi-denominator-rate",
        ):
            self.assertIn(f"\\label{{{label}}}", text)
        self.assertIn("Full posterior large-deviation principle", text)
        self.assertIn(r"\beta,\gamma\in\mathfrak B", text)
        self.assertIn(r"\Omega_J(r)\downarrow0", text)
'''
marker = '\n\nif __name__ == "__main__":\n'
if marker not in test:
    raise RuntimeError("test insertion marker missing")
test = test.replace(marker, "\n" + extra_test + marker, 1)
write(test_path, test)

verifier_path = ROOT / "tools" / "verify_round41.py"
verifier = verifier_path.read_text(encoding="utf-8")
verifier = verifier.replace(
    '"compact-class SLLN", "Jacobi posterior rate"',
    '"compact-class SLLN", "full Jacobi posterior LDP", "uniform inverse-response moduli"',
)
write(verifier_path, verifier)

manifest_paths = [
    "ROUND41_REVISION.tex",
    "round41/preamble.tex",
    "round41/introduction.tex",
    "round41/triangular.tex",
    "round41/lattice.tex",
    "round41/filter_memory.tex",
    "round41/infinite_jacobi.tex",
    "round41/preparations.tex",
    "round41/appendix_uniformity.tex",
    "round41/references.tex",
    "AUTHOR_RESPONSE_ROUND40.md",
    "ROUND41_REVIEW_INDEX.md",
    "ROUND41_READY_FOR_REVIEW.md",
    "round41/HISTORICAL_REUSE.md",
    "round41/PROOF_LEDGER.json",
    "tools/materialize_round41.py",
    "tools/harden_round41_ldp.py",
    "tools/verify_round41.py",
    "tests/test_round41.py",
    ".github/workflows/materialize-round41.yml",
    ".github/workflows/verify-round41.yml",
]
entries = []
for relative in manifest_paths:
    path = ROOT / relative
    if not path.is_file():
        raise RuntimeError(f"manifest source missing after LDP hardening: {relative}")
    entries.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)})
manifest = {
    "source_set": "round41-positive-referee-closure-full-jacobi-ldp",
    "base_revision_head": "1f1409c10d4444ef38c746e12ce426520d7f1ef5",
    "reviewed_head": "1144f2c08a9dee66b6cc12b3bcc35252a054160b",
    "controlling_report": "REFEREE_REPORT_ROUND40_GPT56_PRO_HARSH.md",
    "generated_at_utc": "2026-09-04T10:30:00+00:00",
    "hash": "sha256",
    "files": entries,
}
write(R41 / "SOURCE_MANIFEST.json", json.dumps(manifest, indent=2, sort_keys=True))

print(json.dumps({"hardened": True, "theorem": "full posterior LDP", "files": len(entries)}, indent=2))
