# Response to the independent referee report on A1 v20

**Revised manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Revision:** A1 English v21, 7 September 2026.  
**Controlling report:** `078f34222b00797203cdf6dd421eab9f9f428c59`,
`reviews/a1-english-v20-independent-2026-09-07/REFEREE_REPORT.md`.  
**Reviewed submission:** `6f103ad252d7c65f140720f4095585026f7bb1b9`.  
**New branch:** `revision/a1-english-v21-causal-transfer-and-proof-hierarchy-2026-09-07`.

We thank the referee for distinguishing the resolved exact-kernel objection
from the remaining contribution and architectural questions. We have treated
the collision/causal theorem, rather than successive auxiliary additions, as
the center of the revision. The main statement keeps its original scope and
conclusions. Its proof now passes through a reusable geometric-to-causal
transfer theorem whose hypotheses concern actual sets, acquisition measures
and state maps. All previous technical results and complete proofs remain
in the compilation, with the single dimension-free feasibility correction
identified explicitly. Stable labels below locate the arguments; compiled
numbers and pages refer to the recorded 114-page build.

## E20.1 — dimension-free feasibility

**Change made.** Appendix B begins with Lemma B.1
(`lem:dimension-free-feasibility`, `sections/kernel_feasibility.tex`). For
an arbitrary finite-dimensional W in C(X), it proves equivalence between
W containing no nonzero nonnegative function, zero lying in the relative
interior of its moment body, and existence of a full-support probability
annihilating W. Separation and a small mixture with any prescribed full-
support reference measure give a complete proof and a finite atomic
component. W=0 is treated explicitly in R^0; no comparison between the
dimensions of E and F occurs.

The statement and feasibility paragraph of `thm:exact-kernel` now invoke
this lemma directly with W=W_U. The rest of the theorem and proof is
unchanged. In particular, we retain exact equality of the prescribed kernel,
maximal rank on the full-support slice, weak openness and density of the
maximal-rank locus, arbitrary small bounded continuous density perturbations,
the finite grid witness argument and the finite-atom mixture conclusion.
This is not a retreat from exact realization to containment. Exact old/new
text is recorded in `REVISION_EDITS.json` and enforced by the standalone
builder, so the repair cannot hide additional formal changes.

The new finite diagnostics include W=0 and nontrivial full-support mixture
witnesses; the inherited v20 quotient-chart diagnostics are rerun. These are
checks of examples, not substitutes for the separation proof.

## E20.2 — finite maximum rank and classical attribution

**Change made.** Proposition `prop:finite-matroid-rank`, in
`sections/finite_pairing_comparison.tex`, explicitly identifies the finite
U=0 case with maximum common independence in two represented linear
matroids. We prove the rectangular statement using every minor of
A diag(w) B^t. Distinct subset monomials give the symbolic rank; positive-
orthant nonvanishing and homogeneity then give an attaining full-support
probability. The empty independent set and rank zero are included.

The text calls this a classical specialization. Harvey (2009) supplies the
older algebraic background, while the explicitly inspected common-base
criterion on Terao's SWAT 2026 page 39:2 provides a precise primary-source
comparison. This does not attribute invention of the method to Terao. The
previous correct Banaji–Pantea and Müller et al. comparisons remain intact.

We then explain why the unrestricted argument does not prove the entire
constrained theorem: imposing H_mu U=0 restricts weights to an affine slice,
where distinct monomials may satisfy new relations. On a compact space the
quotient chart identifies the correct moment coordinates and realizes an
open neighborhood by bounded continuous positive density tilts. The
contribution claim is confined to that constrained realization statement;
no new matroid-intersection identity or algorithm is claimed.

## Section 5 — square evidence-containing moving kernel

**Change made.** Proposition B.16 (`prop:square-moving-kernel`) includes the
referee's four-point example with both E and F three-dimensional and
containing 1. We credit the example here to Section 5 of the controlling
report. Its pairing has rank two for every positive prior, kernel
span{p4 e3 - p3 e4}, zero common kernel and zero multiplication closure.
It satisfies feasibility and the dimension test, but its generic rank is
2 rather than 3. It therefore supports the exact-kernel criterion.

The proof also gives the actual positive affine acquisition, the two
physical binary queries, the weighted covariance matrix and the unique
nonzero squared singular scale
(p1^2+p2^2)(p3^2+p4^2)/512. The uniform affine theorem yields the one-step
M^{-2} risk law with that scale. This calculation is not used to advertise
a new general multistep resolution theorem. The example and its covariance
identities are checked on 126 positive rational priors by the new diagnostic
suite, which also checks two pairings with zero common kernel.

## E20.3 — the mathematical center and the compatibility implication

**Change made.** The main statement remains Theorem 1.1. The new
Theorem 5.1 (`thm:causal-transfer`) identifies the implication that was
previously embedded separately in checkpoint and streaming proofs. Its
three hypotheses are independent mathematical obligations:

* (G) the **entire reachable image** has bounded semialgebraic format,
  dimension at most p_n, and ordered containing side lengths after a
  uniformly invertible physical-coordinate change;
* (A) the **actual unconditional acquisition law**, including report
  probabilities, has uniform positive mass on every nonzero initial
  resolution rectangle, with all checkpoint laws arising from one
  exploration experiment;
* (C) the **actual state update** is uniformly Lipschitz and maps reachable
  representatives to reachable states, using only current inputs.

None of these hypotheses assumes the desired quantization or causal error
law. From them the theorem proves the matching checkpoint bounds, constructs
one causal filter, and gives the full propagated-error sum for arbitrary
integer budgets M_1,...,M_{N-1}. Hence the best causal maximum-checkpoint law
is comparable to the maximum of the checkpoint profiles, uniformly in the
degeneracy parameter. Independent randomization does not remove the lower
bound. This statement is reusable on other compact-state families once
these verifiable geometric and measure hypotheses are established.

Lemma 5.2 (`lem:positive-remaining-update`) derives (C) on arbitrary compact
latent spaces from positive finite remaining-test closure. It explicitly
allows dependent tests. The Bayes denominator is bounded on posterior-
mixture segments, so this lemma uses no inverse interpolation gap. It does
not assert (G) or (A) merely from positivity.

**Model-specific mathematical work.** Section 6.3 gives a direct proof of
the main theorem from this transfer principle. It explicitly constructs
T=[[A^{-1},0],[-BA^{-1},I]] from the active block of the Newton evaluation
matrix. Both T and its inverse are uniformly bounded, even when inactive
coordinates vanish. This extends the active-block argument to a genuinely
invertible ambient change, exactly as required by (G), without dividing by
zero scales. The proof separately verifies bounded-format global geometry,
the factor-normalization dimension bound, all prefix masses from the actual
failure-word chart, and stable raw remaining-moment updates. It does not
invoke the old checkpoint or streaming classification as a premise.

The contribution case now rests on the compatibility established by that
verification: all necessary acquired flags, the global dimensional
truncation, and one causal update coexist uniformly at exact collisions.
The fixed-parameter dimension exponent alone cannot recover this transition
law; an observation-side spectral estimate alone supplies neither the
history measure nor the causal realization. The collision-tree formula and
two-parameter intersecting-collision example are retained immediately after
the main proof, demonstrating the resulting multiscale memory regimes.

We do not present the elementary cover-to-filter construction as a new
entropy inequality, and we do not claim the local exact-kernel theorem
settles global resolution. The revised argument strengthens the explicit
mathematical organization and exposes a reusable implication; it does not
replace an editorial judgment of exceptional significance with a theorem
count or a numerical receipt. The requested journal standard remains the
target of this submission, not a conclusion certified by the revision.

## E20.4 — complete preservation and submission architecture

**Change made.** The principal narrative now ends before Appendix A, which
begins on page 22. It has one main statement, the necessary analytic inputs,
the transfer theorem, the acquired collision flags, a direct verification,
and the bit/tree consequences. The old direct collision checkpoint and
streaming proofs are compiled in Appendix D as complete alternative proofs,
not interleaved with the minimal principal route.

The remaining full text is grouped in seven appendices by logical role:
structural and affine results; positive pairings and exact kernels;
circular/inverse/ambiguity geometry; complete specialized collision routes;
observation algebra and decision consequences; effective construction and
resource bounds; and literature comparison. The scope table remains. The
companion results retain their theorem statements and full derivations,
rather than becoming unproved summaries.

The complete previous source is immutable in its original directory and
commit. Superseded front matter is also archived in this revision. The
builder verifies the independently pinned published source manifest and
all 729 entries. It then verifies retention of all 347 earlier labels,
113 unchanged old proof blocks and 116 unchanged old statement blocks,
plus the exact one-proof/one-statement E20.1 correction. The resulting
compilation contains 120 proof blocks and 122 statement blocks. This is a
preservation accounting, not a claim that the blocks have equal importance
or that source identity proves their truth.

## Validation and the next review

`validation/EXECUTION_REPORT.json` records the actual rerun of the ten
inherited suites, the new exact diagnostics, the new suite under `python -O`,
an actual inverse-source mutation rejected by standalone preparation, and
three successful TeX passes with no undefined references or overfull boxes.
`validation/VISUAL_INSPECTION.json` records the pages actually rendered and
examined; it does not claim a new independent mathematical audit of every
appendix. The branch publication includes readable LaTeX, the complete PDF,
the response, source/proof ledgers and execution receipts.

The principal questions for the next referee are the transfer hypotheses
and their independent monomial verification, the physical meaning of the
uniform collision law, the exact scope of the compact constrained-kernel
result, and whether the reorganized contribution meets the requested
mathematical significance standard. We have answered the concrete
mathematical and comparison issues without weakening the original main
claims, removing difficult material, or treating the previous negative
editorial recommendation as a mathematical impossibility result.
