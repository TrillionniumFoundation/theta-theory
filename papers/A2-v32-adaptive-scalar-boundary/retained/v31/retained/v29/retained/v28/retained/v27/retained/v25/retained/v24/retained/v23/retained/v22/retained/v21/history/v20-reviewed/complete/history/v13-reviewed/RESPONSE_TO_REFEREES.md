# Response to the A2 v12 independent report

**Revision:** A2 v13, 10 September 2026.  
**Reviewed source:** `2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`.  
**Report:** `reviews/a2-v12-independent-harsh-two-flight-2026-09-10/REFEREE_REPORT.md`
at `2ae2751f61224b66f314915fd5fc22f6321b606f`.

We thank the referee for separating the closed correctness questions from
the remaining comparison and significance questions. We accept the
independent-contact two-flight calculation and have integrated a complete
proof and its experimental consequence in the article. It does not
invalidate the limiting block. It gives a stronger finite observation
design and a more precise account of the function-valued relative theorem.
The report's contribution is acknowledged in Section 11, the acknowledgments,
and reference [22]. This is an author-requested independent AI report, not
a journal-commissioned report or editorial decision.

## R12-1 — The independent-contact short-record comparator

**Action:** addressed by Theorem 11.1, Corollary 11.2 and Theorem 11.3,
all in `article/29_two_flight_benchmark.tex`; introduced in Section 1.1.
The proof works for independent individually even contacts with either
unequal or equal curvatures, at fixed supplied labelled leading geometry.

Theorem 11.1 begins with the exact two-flight action, with three impacts
and the middle contact counted twice. It calculates the Schur-complement
endpoint Hessian and its three relevant variances. It then varies both
the stationary action and the normalized mixed endpoint derivative. The
other-contact twist contributes the additional factor 2mz. Keeping the
action variation alone would therefore give the wrong off-diagonal entry.
Two explicit ellipse moments, including the physical residual-time weight,
produce the report's all-order matrix. Its separating factor is
(1+2z)^m − (1+2mz), positive by the binomial identity for every m >= 2.
The proof includes the finite-jet dependence, the Morse-domain degree
justification, the affine last-jet dependence, an explicit recursive
inverse, compact finite-order stability, and analytic continuation of the
participating boundaries. No curvature-separation denominator appears.

The theorem was checked against two independent finite routes. The new
Schur/action/twist calculation agrees with the matrix formula on rational
positive geometry grids. In addition, the unchanged `finite_block_row`
from reviewed `tools/verify_v12.py` was evaluated at j = 2 and compared
with the new formula in 216 exact cases, including unequal curvatures and
both orientations. The original finite routine is not described as wrong
or absent; the revision extracts and proves its short-flight consequence.

Corollary 11.2 makes the relation to Theorem 9.1 explicit. For fixed M,
the maps q -> Xi and q -> f have analytic triangular inverses, and their
compositions give analytic changes of finite-jet coordinates. This is not
an identification of finite and limiting law functions, a uniform-in-M
stability theorem, or a statistical domination claim.

Theorem 11.3 strengthens Theorem 10.3 to **j0 = 2 for every fixed M**.
The support realization first gives physical jet coordinates. The two-flight
inverse gives Xi coordinates; positive offsets h, ..., (M−1)h yield a
Vandermonde derivative plus a remainder whose transformed norm is O(h).
A fixed sufficiently small h makes the actual probability map locally
bi-Lipschitz. This proof contains no tau^j approximation step. The theorem
also gives the Borel finite-net estimator, deterministic confidence charge,
squared-risk upper bound, and a physical two-point lower bound allowing
adaptive randomized window choice. All alternatives keep the selected
leading hierarchy fixed. The offsets and conditioning may depend on M.

For preservation and comparison, the previous Theorem 10.3 and its full
long-bridge proof remain active. The introduction and the final paragraph
of Section 11 now identify Theorem 11.3 as the direct strengthened design.
The revision therefore changes both the proof and the physical design,
rather than only adding a disclaimer that long records were not necessary.
It does not claim that two flights are minimal in every restricted family.

## R12-2 — The contribution after the short-record comparison

**Action:** the abstract and introduction have been rewritten around the
relative physical law and its complete smooth invariant. No established
geometric, inverse, acquisition or calibration theorem has been removed.

The main inverse question is now explicit: without access to boundary
actions, a symmetry restriction, or a supplied finite-dimensional graph
family, do selected physical count laws determine a stable nonlinear
boundary invariant on an entire onset collar, and can it be acquired by
charged binary preparations? Theorem 1.1, the compatibility theorem of
Section 8, the Abel inverse of Section 12, and Theorems 14.3 and 14.5 give
the answer for the stated symmetrized energy invariant.

The relative estimate addresses an exponentially small physical twist,
not just an absolute stationary-action remainder. It normalizes the exact
cofactor, controls differentiated perturbations in trace norm without a
factor equal to the interior dimension, and passes the result through
physical residual-time integration on a nonshrinking collar. The inverse
then identifies complete smooth functions by a Volterra argument, not by
recovering Taylor coefficients. The observation theorem handles the
integrated flux, structured bridge error and scalar Bernoulli noise in
different norms, includes the origin, and charges a separate pilot when
g, A and gamma are unknown. These statements do not use the exact-family
probability oracle of Theorem 11.3.

The three compatible conclusions requested by the report are stated at
the beginning of the introduction: leading amplitudes do not determine
higher jets; nonlinear short records do determine finite even-contact
jets; long bridges construct and control a general smooth function-valued
invariant. The physical open image in Theorem 10.1 supplies genuine
independent directions invisible to the selected leading hierarchy. It
prevents the invariant's geometric nontriviality from resting only on
formal coefficient variations.

The regular N^(-1) finite-family risk is described as parametric after
local invertibility, not as a new general statistical rigidity principle.
The sufficient full-profile accuracy exponent remains
2 + 6/(m−1/2) + gamma/|log(tau)|, or with gamma replaced by gamma_+ in
the self-calibrated uniform bound. The two-derivative gain, positive-node
construction, smooth-bias treatment and pilot proof remain unchanged.
No new optimization claim is used as a substitute for the principal
physical result. The abstract no longer suggests that long records are
needed for finite jets or that analytic continuation itself is the novel
step. The article retains its full positive conclusions with their actual
information sets. The assessment of exceptional journal significance is
left to the next independent review; the revision does not certify an
editorial outcome.

## R12-3 — Theorem-level literature comparison

**Action:** new Section 1.5, `sec:v13-literature`, compares geometric class,
observations, supplied information, recovered object, and mechanism for
three primary-source results. Source locations and retrieval scope are
recorded in `LITERATURE_VERIFICATION.md`.

The comparison uses De Simoi–Kaloshin–Leguil's Definition 1.3, Main Theorem,
Remark 1.5 and geometric reconstruction; Finamore–Leguil's cited Theorem A
and the definition of its enriched spectrum; and Zelditch's specified
symmetry classes and Theorems 1.1 and 1.4. In particular, the word
“enriched” is retained for the Sinai-billiard theorem. The text does not
infer that A2 observations supply another paper's spectrum or that a
local contact/profile conclusion implies its global isometry conclusion.
It identifies the shared highest-jet and continuation mechanisms without
claiming an exhaustive priority search or re-refereeing those papers.

## Closed issues and retained content

The original general relative determinant and integration proofs, the
independent limiting block, the analytic support realization, the weighted
Abel inverse, the two-derivative integrated-flux gain, the m+2 positive-node
reconstruction, and the charged smooth-class calibration remain active.
Earlier endpoint, nuisance, count-only, coalescence, contact-jet and
collision-response proofs remain in the complete appendix. No old paper
or report is deleted or overwritten at its original path.

The source audit verifies all 212 reviewed formal result/proof blocks
byte-for-byte, independently of their surrounding prose, and retains all
reviewed active inputs. Six new blocks give a total of 218. The inherited
bibliography and replaced front matter are preserved under the pinned
history directory. The main manuscript is 123 pages after compilation.

## Verification and next review

The v13 suite passes 3,295 finite checks in both ordinary and optimized
Python; its output files are identical. These include 216 comparisons with
the reviewed finite-block routine. The referee's separate 1,335-check suite
was also rerun in both modes with identical output. The complete main and
companion compile locally. The final main log has no undefined references,
undefined citations, duplicate-label warnings or overfull boxes. The
source, tests, pins and build commands are included for independent reruns.
These are finite diagnostics and typesetting checks, not a formal proof
certificate, a nonlinear billiard simulation, or a remote CI result.
