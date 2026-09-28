# A2 revision 97 — response to the latest referee reports

## Source pin and correction of the previous response

The controlling report is **the v96 report**, not the v94 report:

- Review branch: `review/a2-v96-independent-harsh-top4-2026-09-20`.
- Exact review head: `b4ab165062f3625e06717002fb419bd44ab8e7f7`.
- Report: `reviews/a2-v96-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`.
- Reviewed manuscript head: `423a0e135c217d6dc42fc973d8da4ee13893e865`.

We also read and answer the preceding v95 report:

- Review branch: `review/a2-v95-independent-harsh-top4-2026-09-20`.
- Exact review commit: `c020b5ede3ca07852db4166f614354341b0d8494`.
- Report: `reviews/a2-v95-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`.
- Reviewed manuscript head: `ebb796e49ca51a62b90d92ec0d09819cfe8d00a4`.

The v95 report was committed at 2026-09-19T18:35:37Z; the v96 manuscript
was committed at 2026-09-19T18:55:55Z. The v96 response's statement that
no later A2 report had been found was therefore incorrect. It is not
repeated or used as a premise here. The historical file is preserved
unchanged as a record, and this paragraph is the explicit correction.

This revision is based on the controlling **review head**, so the latest
report and the complete reviewed manuscript remain in its ancestry.
No existing branch is overwritten. All new files are confined to A2 v97
entrypoints, modules, revision records, two scripts, and one scoped workflow.

## What changed mathematically

The revised article is *Projective polynomial observations: real spectral
atlases and identification walls*. Its principal theorem graph is:

real constrained graph → joint specialization → finite parameter atlas →
explicit multiplicity/boundary laws → cross-rank cubic inverse → remote
weight-wall entrance law.

The general scalar divisor-ratio result is explicitly credited to classical
resolution/Łojasiewicz theory. The joint real set and its spectral diameter,
not scalar finiteness alone, organize the manuscript. The explicit model
class is no longer restricted to one double/triple cubic pattern: at every
fixed degree the full-rank binary theorem allows all coprime multiplicity
patterns and endpoint/interior assignments. The cubic theorem retains
rank-deficient channels and supplies a separate identification-wall model.

The wall calculation corrects a possible premise in the report rather than
manufacturing the requested blow-up. At the weight wall the base local
Fisher constants stay positive, while a remote exact component enters the
full observation ball. The disappearing global exclusion radius and a
blowing-up local inverse constant are not interchangeable quantities.

## Point-by-point disposition of v96 Sections 12 and 16

Here “answered” means that a statement and proof are supplied for further
independent review, not that a referee or a formal proof checker has
certified them. The source labels below are stable even if pagination changes.

| Request | Disposition | Location and mathematical response |
|---|---|---|
| 12.1 Correct the controlling report | Answered | Exact v96 and v95 branches, paths and commits are pinned above; the chronology error is expressly corrected. |
| 12.2 Theorem-by-theorem novelty comparison | Answered | Introduction, Table 1, and the following comparison paragraph distinguish BM uniformization/resolution, BE Proposition 4.3/Theorem 4.8, Hardt triviality, and Hà v1 Theorems 5.8/12.3 from the joint feasible root-set and stochastic outputs. Existing family chamber results are not denied. |
| 12.3 Genuine change of singularity type | Answered by broader theorems | `thm:atlas` gives fixed-format real parameter data; `thm:mult-atlas` explicitly treats arbitrary degree-d coprime binary root patterns, including interior/boundary changes. The orders are 1,k/2 in interior clusters and k at the boundary; the root exponent changes between 1/2 and 1. |
| 12.4 G identically zero | Answered | `def:monomial` records exact pieces separately, with all target H zero on identified fibres; they enter no 0/0 ratio. Nonzero-G pieces with zero H contribute infinity only for H. |
| 12.5 Effective algebraic representation | Answered | `def:input` specifies constants, roots, probabilities, clocks, graphs, inequalities and isolating data. Every subsequent construction uses this representation. |
| 12.6 Real-accessible cover theorem | Answered | `prop:real-cover` treats square-slack lifts, regular-locus coverage, recursive singular real loci, strict dimension descent, properness, principalization, real generic points and transversals. `lem:relative` spells out generic-fibre spreading and separate induction over excluded base loci. |
| 12.7 Quantitative inverse | Answered | `lem:local-cubic` lists common positive normalization, marginal, discriminant, coefficient-duality and positivity margins. It separately defines the positive compact remote-separation minimum. No determinant lower bound for U is smuggled into a rank-one proof. |
| 12.8 Identification-wall asymptotics | Answered, with a mathematical correction to the proposed blow-up mechanism | `thm:wall`, `lem:mu-positive`, and `lem:remote-control` prove d_rem(δ)=μ_E δ+O(δ^(3/2)), μ_E>0, a two-scale whole-model transition, and the exact-fibre square-root opening on the other side. `C_loc` extends positively through E=0. The report's suggested necessary divergence of C is rejected for this wall, with a proof. |
| 12.9 Valuation and Fisher walls | Answered within stated theorem scopes | `thm:atlas` gives a common refinement; `thm:mult-atlas` computes valuation changes and Fisher faces in an explicit broader class. `ex:crossover` gives the t-scale multiplicity transition. A general semialgebraic constant program is not called a Fisher quadratic program unless its normal form is proved. |
| 12.10 Diagnostics versus proofs | Answered | Exact records are labeled finite regressions. They include a distinct degree-four (3,4) multiplicity pattern, coefficient-order witnesses, wall factorization, KKT values and geometric-wall opening. No numerical test is cited as a proof of a universal assertion. |
| 12.11 Article architecture | Answered without deleting history | `rigidity_v97.tex` is a self-contained 21-page principal article. `rigidity_v97_archive.tex` imports the complete unchanged v96 article and all its inherited appendices. `rigidity_v97_complete.tex` assembles both PDFs. All old sources remain byte-identical. |
| 12.12 Three meanings of stability | Answered | Final subsection and `thm:wall` separate multiplicity/valuation, exact identification, and local Fisher conditioning. The example with a colliding pair actually has a divergent linear-law constant; the remote weight wall does not. |

The stronger route in v96 Section 16 is addressed with both a general
finite real parameter theorem and an explicit variable-multiplicity model
class. The manuscript does not claim that one elementary formula explicitly
classifies every rank-deficient polynomial model, every degree at once, or
all changes of observation architecture. Such an assertion is not required
by the fixed-format atlas and is not inferred from the cubic calculation.

## Major objections in v96 Sections 4–10

**Breadth and the bridge to valuation data.** The explicit atlas now permits
all multiplicities and endpoint/interior statuses at fixed degree. Its
constant for an interior cluster of multiplicity m has factor
`2 sqrt((m-1)/m)`, and its coefficient orders are proved by actual real
root arcs and whole-model inverse bounds. General parameter stratification
is not obtained by resolving the total space once: the proof resolves
generic fibres, spreads the finite construction over an open base, and
recurses on the excluded parameter locus. Real-accessibility flags and
Fisher signs are added separately. These relative uniformity steps are a
particular target for the next independent referee's scrutiny.

**Novelty boundary.** Even granting scalar finite-max valuation theory,
one still has to retain joint weighted coefficients and the observation
metric, take real closure with the centre fixed, show Hausdorff convergence,
exclude cross-cluster matchings, compute the target diameter, and realize
the stochastic alternatives. These operations and the remote entrance
calculation are isolated from the classical inputs. The versioned Hà
comparison acknowledges its actual family hypotheses and outputs.

**Effective construction.** Equations `eq:closure-formula` and
`eq:matching-formula` supply the quantifier pattern, finite permutation
matching, and attained compact optimum. Real algebraicity of the unique
constant follows after this logical encoding. No full implementation of
the generic resolution or quantifier-elimination algorithm is claimed.

**Rank-crossing inverse.** The second-marginal argument supplies common
local constants independently of the first-channel rank. The remote
separation is a different, explicitly minimized positive quantity on
identified compact sets. Both components of the whole-model proof now
have separate statements and roles.

**Actual walls.** The weight wall has a positive spectral jump at its first
additional exact point, a linear remote entrance distance from the
identified side, and a square-root splitting on the nonidentified side.
At the geometric wall the extra pencil interval has quadratic length in
the clearance D-b; the corresponding exact point again is remote. The
explicit two-scale Fisher entrance theorem is for the weight wall. A
claim of the same cone at the geometric endpoint is deliberately not made.
At the critical ray λ=μ_E, membership is exactly t≥d_rem(δ); the sign of
its first nonzero higher Puiseux term decides the outcome, or equality
puts the remote point in the closed ball. The universal first-order
threshold is not overstated as a universal critical-ray selection.

**Architecture.** Preservation and journal organization are now different
artifacts: a complete principal proof and an unchanged archival companion.
The main article neither appends the entire historical programme nor
silently deletes it from the deliverable.

## Explicit carry-forward disposition of v95 requests

The v95 requests on G=0, input representation, real-cover recursion,
cluster matching, ordinary-jet versus divisor finiteness, cover independence,
parameter dependence, exact-fibre equality cases, algebraic matching minima,
and finite diagnostics are addressed respectively by `def:monomial`,
`def:input`, `prop:real-cover`, `thm:joint`, `cor:orders`, `cor:orders`,
`lem:relative`/`thm:atlas`, `thm:wall`, `eq:matching-formula`, and the
explicit non-proof labels. Its requested active-set partition and
rank-two perturbation result are retained and restated as
`prop:cubic-Q`/`thm:cubic-local`; the local statement is strengthened
through the actual identification walls. Its request to distinguish
stability mechanisms is answered by the final subsection and the two
contrasting crossover models. Its centre-known statistical interpretation
is preserved as `cor:risk`, including a rounding remainder.

## Validation and scope of evidence

- The complete **principal v97 article** was compiled locally with latexmk
  and pdfLaTeX: 21 pages, no undefined references/citations, no overfull
  boxes, and no LaTeX warnings in the final local log.
- All pages were rendered; a page montage and selected full-page views
  were inspected for layout. This is layout inspection, not peer review.
- The exact SymPy regression passed; the committed JSON contains the
  rational outputs and checked isolating intervals.
- The local staging source hashes are recorded. This staging directory
  is not represented as a full Git checkout.
- The unchanged archival companion and assembled complete PDF were not
  compiled locally because the historical source tree was not mounted
  in that staging directory. The new branch-scoped workflow builds all
  three entrypoints from an actual checkout and binds its receipt to
  the checked-out head. A workflow definition is not evidence of a
  successful workflow run; the runtime receipt/artifact, when available,
  is the evidence for that separate claim.
- No formal proof assistant, full-model nonlinear optimizer, generic
  resolution implementation, or complete symbolic elimination of the
  closed stochastic model was run. No journal decision is predicted.
