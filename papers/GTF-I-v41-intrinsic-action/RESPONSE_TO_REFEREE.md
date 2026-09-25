# Response to the twenty-fifth independent referee report

**General Theta Foundations I — Revision 41**  
**Intrinsic Action Gaps and Numerical Memory**  
26 September 2026

Controlling report: `reviews/general-theta-foundations-i-v39-orbit-response-independent-harsh-top4-r25-2026-09-25/REFEREE_REPORT.md`, frozen at `9707844addcd9eb478eb863514f288923f9d40fd`. Reviewed v39 publication: `28890c62dd69f217bf2f1c205ff9542eb537c2ef`; native mathematical source: `cb9c9edc0d20ea32b4702c668dcddae6b791f0ce`. The first review of that same manuscript was r24 at `24bd1abe003ef13df4eb223a8b2010010de9f82b`.

The remote survey also found two existing v40 working branches, but no later referee-ready report. This revision starts from r25 and uses a new v41 branch; neither v40 branch is altered or represented as reviewed. A substantive intrinsic-action source module was committed remotely before assembly, at `57868074a949ef1f5e672ddf4fc4ac196d66c6dc`.

The report raises two genuine nonintrinsic choices in the preceding theorem: a redundant presenting group, and an arbitrary splitting of multiplicity spaces. Both are removed. The extension goes beyond quotienting out a kernel: a faithful experiment with a genuinely acting circle factor and no full group gap now has a matched width theorem. The representation invariant is also evaluated through complete centralizer calculations for all compact simple adjoint types and a growing fundamental family. The entropy theorem, classical root theory, and inherited constructions are credited rather than relabelled as new.

Stable labels below refer to the native LaTeX; `evidence/THEOREM_LOCATIONS.json` gives compiled numbers and pages. Source and regression records are delivery evidence, not independent mathematical certification.

## 13.1 / Section 7 — intrinsic gap and effective image

**Addressed by `prop:action41` and `thm:intrinsic-width41`.**

The group is the closure of the actual command matrices. On each active irreducible model E we use the action norm `g_E=1-||P_E-Pi_E||^2` on its unit sphere. Polar coordinates prove that it equals the exact Lebesgue-action gap used by entropy production. Harmonic decomposition gives an exact supremum over finite-dimensional harmonic restrictions; finite truncations are explicitly not certificates for that supremum.

The two operators depend only on the pushed-forward command law. We prove their invariance under orthogonal intertwiners, redundant group extensions, and splitting identical letters. The old full-group gap is preserved as a sufficient transference certificate, not imposed as the intrinsic hypothesis.

More substantially, the matched-order theorem requires expansion only on **one active type attaining the largest minimum-orbit dimension**. The exact constructive upper bound does not need expansion on any type. Thus requiring gaps on every constituent would still be unnecessarily strong.

`prop:mixed41` supplies a faithful ten-command rational example on R^3 + R^2. Its effective group is SO(3) x SO(2). The SO(3) factor uses the identity and inverse pairs of two rational-axis rotations. Density and the external Benoist–de Saxcé theorem provide a qualitative gap there. The active circle factor has Fourier multipliers arbitrarily close to one, so the complete effective group has no norm gap. Nonetheless, for symmetric basis seeds, `rho<=1/40` and `epsilon<rho/(2 sqrt(3))`, the numerical width is Theta(N). Its upper bound is O(N)+O(sqrt(N)), with a paid branch selector. This is not just the removal of a trivially acting factor. No numerical SO(3) gap is claimed computed.

## 13.6 / Section 5.3 — canonical multiplicity calibration and arbitrary seeds

**Addressed by `def:activation41`, `prop:activation41`, and `thm:intrinsic-width41`.**

We first restrict to `R_X=span(H X)`, not to an arbitrary ambient decomposition. No assumption that the original finite seed set itself spans the ambient space is needed. Its canonical isotypic components determine which types are active.

For all isometric intertwiners J of one irreducible model into an isotypic component, define

```
a_lambda = max_(x,J) ||J* x||,
B(J) = ||J*||_(infinity -> 2),
c_lambda = max_(x,J) ||J* x|| / B(J).
```

The maxima are attained on a compact set and do not choose a splitting into copies. The query norm refers to the actual prescribed queries. If `C_(lambda,x)` is the Haar covariance of the projected seed, then

```
a_lambda^2 = d_lambda max_x lambda_max(C_(lambda,x)).
```

The covariance is the Hilbert–Schmidt projection onto the matrix commutant. The proof works for real, complex and quaternionic commutant types: a commuting self-adjoint operator on an irreducible real representation is scalar. This supplies a spectral computation, not only a renamed optimization. The sharper c_lambda remains an explicit compact optimization incorporating query geometry; we do not claim a closed eigenvalue formula for that non-Euclidean norm.

Terminal correlation now gives `kappa_lambda=rho c_lambda-2 epsilon`. This canonical threshold applies to the actual entire hidden register, without free constituent information. The upper signal bound uses the active dimension r rather than the possibly larger ambient D. Old spanning-seed bounds are retained as sufficient special cases, with their original statements in the inherited appendix. The projective/minimal-orbit signal improvements remain unchanged.

`cor:error41` additionally states the constituent-wise occupation bound and its maximum lower bound on optimized actual terminal error. It does not sum local errors or rule out cancellation.

## 13.4–13.5 / Section 8 — evaluate the orbit invariant

**Addressed on complete adjoint and stated fundamental families, not claimed for every highest weight.**

`thm:adjoint41` proves the formula

```
s(Ad) = |Phi| - max_alpha |Phi_(Delta minus alpha)|
```

for every compact simple adjoint representation, and identifies all minimizing rays and their Levi centralizers. Its table includes A, B, C, D and all five exceptional types. The resulting exponents are l, 2l-1, 2l-1, 2l-2, 5, 15, 16, 27 and 57, respectively. The proof uses conjugacy into a closed Weyl chamber and counts roots vanishing at its points. It distinguishes compact real-vector orbits from complex nilpotent and projective orbits. Classical root theory is explicitly attributed; the numerical width application is the present use of those calculations.

`prop:standard41` gives defining real, complex and quaternionic actions with their stabilizers, and the Spin(3), Spin(5), and Spin(6) spin/half-spin consequences through low-rank identifications.

`thm:exterior41` gives a full singular-value/stabilizer analysis of the fundamental module wedge^2 C^n, viewed over R, for every n>=3. Its least orbit dimensions are 5 at n=3,4; 13 at n=5; 14 at n=6; and 4n-7 for n>=7. At n=6 the minimizer is the full-rank symplectic form with stabilizer Sp(3), not a decomposable highest-weight vector. The latter orbit has dimension 17, whereas the true minimum is 14. This produces the conditional width N^7 rather than N^(17/2). The reducible real-form issue at n=4 is handled explicitly.

The special skew normal form is proved via an antilinear quaternionic pairing, not delegated to an uninspected source. The broader Youla normal form is credited as classical. The exact finite checker independently constructs tangent matrices for n=3,...,8 and enumerates root systems and node deletions; these checks do not replace the proofs for all ranks.

We do not assert a complete classification of every spin, exceptional fundamental or arbitrary highest-weight module. The results supply complete infinite families and every simple adjoint type rather than a formal real-quantifier-elimination placeholder. The general theorem is an exponent formula conditional on its intrinsic dynamical hypothesis; the representation tables are separately identified evaluations.

## 13.2 / Section 6 — Chen–Wu version discrepancy

**Resolved by a fresh primary, explicitly versioned audit; the v2 constant is currently verifiable.**

On 26 September 2026 the primary arXiv abstract record for 2604.07058 lists both versions: v1 at 8 April 2026, 13:10:02 UTC, and v2 at 27 August 2026, 12:09:39 UTC. We read the explicit v1 HTML, explicit v2 HTML, and the v2 PDF; the latter's printed pages 4 and 5 were inspected as page images.

The report's v1 theorem numbers and constants are correct for **v1**: Proposition 3.1 gives q^2 mixed-state linearization, Theorem 3.2 gives 2k+6, and Corollary 3.3 gives 2q^2+6. The explicit **v2** has a different title and statements: Proposition 3.1 gives k+1 for a zero-cutpoint GFA; Theorem 3.2 gives q^2+1. The positive length-dependent attenuation is explicit in that proof. The v39 v2 claim is therefore supported by the primary source now accessible. We make no claim about why the earlier review's primary access differed.

Both versions now have separate bibliography entries. `PRIMARY_SOURCE_AUDIT.json` records exact primary URLs, dates, titles, theorem locators, inspected representations and the observation date. No third-party metadata substitutes for the primary text. No full external article or fabricated PDF hash is redistributed. The numerical/cutpoint separation is proved internally and does not depend on choosing either external constant.

## 13.7–13.8 / Sections 10–11 — resources and arithmetic example

The main theorem still concerns nonuniform clocked atomic-row label width. It does not infer uniform space, total branching-program size, table complexity, exact finite-coin workspace or autonomous length recognition. One selected marginal query is answered. Labels, label bits and a jointly specified output law remain distinct. Every stochastic branch is charged, including its identity and amplification; the final held answer has a two-label cut.

The six-gate theorem remains an optional conditional corollary of the precise imported inequality (LPS5). The full general theorem and the new faithful mixed example do not use LPS5. The original LPS theorem/page verification has not been completed in this revision; the previously proved local normalization and explicit limitation are retained. No finite spectral calculation is represented as verification of the infinite-dimensional bound.

## 13.3, 13.9–13.10 — writing, scope and independent review

The General Theta Foundations I prefix is retained, with the mathematical subtitle naming intrinsic action gaps and numerical memory. The article leads with a new operational theorem, not with journal positioning or archival volume. Its notation distinguishes effective group, active seed span, isotypic component, irreducible model, query calibration and available labels.

The proof sequence is effective action -> uniform orbit geometry -> entropy occupation -> canonical activation -> dominant-only matching -> explicit nongapped example -> evaluated representation families. Classical, inherited and new contributions are distinguished in the introduction and literature audit. Existing material is preserved in the manuscript appendices and unchanged supporting volumes; none is replaced by a negative theorem or a build receipt.

The frozen Round-Seventeen ledger and relevant v39/history sources were consulted. No statement here establishes the separate branchwise Fourier/LLT, stopped-LDP, global-kernel, nonlinear-semigroup, common-domain, filtering, optional-projection or typed-contraction obligations of A2/A3/A4/B4/C2/D1. Their original sources and status are unchanged. Independent expert review has not been obtained and is not impersonated by these internal revisions.

## Remaining precise boundaries

Exact finite profile optima, leading constants, general vanishing-signal regimes, a nongapped dominant-type classification, all higher spin/highest-weight orbit minima, an optimized c_lambda formula, full finite-bit resource accounting, and original-page LPS verification are not claimed. The new positive conclusions are intrinsic action invariance, canonical arbitrary-seed activation, a strictly weaker dominant-only expansion hypothesis, a faithful nongapped example with matching width, and complete orbit calculations on the stated representation families. They are supplied with analytic proofs for the next independent referee.
