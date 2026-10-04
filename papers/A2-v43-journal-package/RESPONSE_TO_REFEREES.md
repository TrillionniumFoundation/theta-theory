# Response to the v42 referee — A2 v43

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*.
**Date:** October 4, 2026.
**Controlling report:** `74787c9c353b72983fe1bb43af467e31d3eb0f2a`,
`reviews/a2-v42-external-top4-rereview-2026-10-04/REFEREE_REPORT.md`.
**Reviewed author:** `fffc85d4da8c8ee6369833369d564b1cffabc63d`.

We thank the referee for the detailed examination of the exact and finite
arguments and for the recommendation of minor revision. We have addressed the
four author-side presentation and delivery requests. The independent specialist
confirmation remains an editorial process item. This revision does not change
the experiment or theorem hypotheses and does not add an unrelated result.
All 113 reviewed proof bodies remain byte-identical in the active primary and
supplement, including the deterministic alternative.

## 10.1. The default acquisition bound

The abstract now gives the conditional moment bound
`C tau^(-2) log(C(n+1)/delta)`. The introduction, the finite-law theorem,
its accompanying discussion, and the resource summary consistently identify

`N <= N_geom(c a_m,delta/2) + C a_m^(-2) log(Cm/delta)`

as the default finite-law bound. The theorem prints it first as
`eq:two-field-joint-default-cost`. The original
`eq:two-field-joint-decomposed-cost` is explicitly identified as the retained
deterministic all-node alternative. Lemma `lem:two-field-finite-moments` and
Proposition `prop:moment-complete-budget` carry the same designation.
Here deterministic refers to the nominal design, not to the Bernoulli outcomes.

The existing proof of the finite-law theorem establishes the deterministic
implementation and the common positive factor reconstruction. Theorem
`thm:linear-moment-sampling` and Corollary `cor:linear-joint-budget` prove the
default implementation. We state this dependency before the retained proof;
the corollary uses only the common factor reconstruction, not its own improved
bound. Its proof is unchanged. The ledger records this acyclic dependency.
Fine geometric accuracy, factorial moment conditioning, positive fitting,
resource exclusions and the exponential sufficient joint bound are unchanged.

## 10.2. Current and historical front matter

Every unprefixed journal-facing document now describes v43. There is one
current proof/dependency ledger and one current literature audit. Superseded
v41 front matter and v42 response/audit files are retained verbatim under
explicit `provenance/v41/` and `provenance/v42/` paths in the repository copy.
They are not presented as current journal documents or mixed into the journal
archive. The current source manifest is `SOURCE_PINS.json`.

The literature audit distinguishes rechecked primary sources from inherited
comparisons. The accepted Bernoulli manuscript linked by the journal was
reopened: Corollary 2.5 and Theorem 5.1 are the cited numbered statements.
We also cite the Gassiat--Le Corff--Lehericy erratum and state its quantitative
scope, distinguishing it from exact identification and from our internally
proved finite collision bounds. No priority claim is upgraded by this check.

## 10.3. Separate data models, hypotheses and norms

The abstract has separate exact and finite paragraphs. The introduction has
an explicit data/hypothesis/conclusion table, `tab:exact-finite-claims`.
It separates whole-plane fields from sampled bits, arbitrary compact-law exact
identification from finite recovery under quantitative geometry, local spatial
`L^1` prediction from `BV`-based uniform prediction, and exact period recovery
from finite decisions requiring a positive patch margin. The finite-configuration
alternative continues to require a complete protected aperture and no period
margin. No hypothesis is transferred silently between those assertions.

## 10.4. One immutable article-and-supplement package

`core/29_supplement_interface.tex` is byte-identical to the reviewed interface.
The exact section and its singular-support and nonsmooth-curvature inputs are
also byte-identical. All cross-document mathematical label names and their
owners are frozen in `JOURNAL_INTERFACE.json`; the PDF target names identify
v43. The same exact source commit produces both PDFs, the complete two-document
TeX closure, the current ledgers, the source hashes and the package manifest.
A standalone build script operates on that closure without patching sources.

The qualification refuses a missing companion, changed interface, duplicate
mathematical label, stale front-matter version, changed reviewed proof body,
or source-byte mismatch. Archive membership is checked, and the final archive
has a SHA-256 digest in the receipt. Reading the exact theorem does not require
any theorem from the supplement. Source-only capture and local development do
not claim remote PDF qualification.

## 10.5. Independent specialist confirmation

No independent human specialist check is represented as completed. The current
specialist brief preserves all five tracks requested by the referee, with
precise theorem labels, hypotheses and questions. It identifies the current
source and requires the eventual reviewer to state the scope actually checked.
The referee's favorable recommendation and the build evidence are not treated
as journal acceptance or a formal proof certificate.

The complete revised manuscript and supplement are submitted for the next
review with their positive exact and finite conclusions intact.
