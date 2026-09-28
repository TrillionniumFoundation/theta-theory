# A2 revision 100: response to the v99 referee report

## Controlling sources

The controlling report is `reviews/a2-v99-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`, blob `abd7744408a5db2e44b1a6ca46c48271a8c163eb`, on review commit `5485ed6d127b8443fce059db118dc215b68e283a`. It reviews paper commit `c49c6d0604f83badf47b32dfdf25dc043b4117ef`. The new branch is `revision/a2-v100-canonical-degeneration-and-singular-entrances-2026-09-20`.

The revision responds by adding mathematical results and exact evidence. It does not remove the relative atlas, the full-rank multiplicity law, the exact cubic fibre, either wall, the second-order formula, or their proofs. The principal article imports the inherited mathematical sections without modifying them. The companion archive contains the whole reviewed v99 article and its complete historical archive. The report itself is unchanged.

## R1. Identify the joint fibre relative to existing degenerations

**Change.** `article/v100/canonical.tex`, Theorem `thm:canonical`, identifies the fixed-centre initial fibre with the observation-unit section of the positive-real weighted tangent relation of the actual observation/coefficient image germ. Its proof includes the boundary rescaling needed to justify intersection with the closed unit ball; it does not simply interchange intersection and closure.

The algebraic comparison is explicit: weighted substitution and saturation by the scale variable yield the minimum-weight initial ideal. The real constrained fibre is its positive-real liftable part with the original branch conditions retained. The cusp `y^2=x^3` shows that even a real-prime original ideal can have a real algebraic initial fibre strictly larger than the positive-real tangent relation. The normal-cone and initial-ideal construction is credited to existing theory, rather than renamed as a new algebraic construction.

## R2. Establish intrinsic or reconstruction content

**Change.** Theorems `thm:filtered-naturality` and `thm:reconstruction` in the same file provide two additional statements. Filtered coordinate changes carry tangent relations and their unit sections when the observation norm and target decoding are transported. Equivalent norms alone are not claimed to preserve the leading diameter.

The reconstruction theorem determines the actual compact coefficient fibre from limiting quadratic distance probes centred at rational points. It proves locally uniform convergence of these probes, an explicit intersection formula, finite-net Hausdorff bounds, and an effective search for a rational separating probe between unequal algebraic fibres. This also states precisely which richer scalar information suffices; the revision does not claim that all possible scalar information is insufficient.

## R3. Strengthen scalar separation inside the principal experiment

**Change.** `article/v100/valuative_separation.tex`, Theorem `thm:binary-separation`, supplies two full binary experiments, with every model parameter unknown and competitors in the original closed model. They have degree one, roots `1/4,3/4`, mixture weight `1/2`, three clocks `2,3,4`, and strictly positive invertible channels.

In common parameter coordinates, observation orders agree on every real analytic arc. The orders of every polynomial scalar function of the target coefficient increments also agree, including mixed polynomial functions and identically zero cases. The proof explains equality of accessible real divisorial orders on common further modifications. It does not make a corresponding assertion about complex zero divisors.

Their profiled leading root ellipsoids are computed exactly. The squared maximum-bottleneck diameters are `129609775953/25280` and `10058351786055/1396384`, respectively. Thus the units erased by valuation have a measurable spectral consequence in the full binary model. This is a distinct strengthening of the retained v99 sharp-marginal example: the new example fixes all the specified orders, not all sharp scalar values. The reconstruction theorem explains why the latter distinction matters.

## R4. Position the regular remote formula in variational analysis

**Change.** The introduction and the closing discussion of `article/v100/singular_entrances.tex` compare the retained formula with metric projection and constrained value-function sensitivity, citing Rockafellar--Wets and Bonnans--Shapiro. Metric projection is not presented as a new operation. The complete proof of the existing second-order formula, including nonunique preimages and the common residual, is retained unchanged in `article/v99/remote_structure.tex`.

Proposition `prop:corner-criterion` gives a checkable route from a local Nash equality/inequality presentation to a full corner chart and cone coercivity. Its second-order conclusion explicitly assumes the centre's second-order expansion; the more general entrance theorem below requires only a C1 centre path.

## R5. Extend the wall theory beyond regular cubic corners

**Change.** Theorem `thm:singular-entrances` in `article/v100/singular_entrances.tex` treats fixed-format semialgebraic families with a finite exact parameter fibre, without a regular corner or injective derivative hypothesis. It proves eventual zero distance or a positive rational entrance power, finite exponent lists at fixed format, positive Nash leading coefficients, compact-uniform power remainders, independence of the isolating neighbourhood, and effective algebraic descriptions.

For any specified semialgebraic radius it decides the eventual sign of the exact radius-minus-distance function. Equality is included because the observation ball is closed and the minimum is attained. The limiting target set is the union of the exact target spectra of the included representatives. No truncated critical expansion is used to decide an unresolved equality.

Theorem `thm:entrance-realization` realizes every rational exponent at least one in strictly positive polynomial probability experiments as the format varies. This demonstrates why fixed format is necessary for a finite exponent list. It is not an assertion that every such exponent occurs in the cubic binary family. The explicit cubic weight and endpoint walls, their distinct feasible charts, and their nonidentified-side opening laws remain in the principal article.

## R6. Separate direct effective outputs from geometric certificate search

**Change.** The direct quantifier-elimination outputs remain explicit theorem conclusions. The new `article/v100/output_and_arithmetic.tex` specifies the algebraic input representation, attained-minimum formulas, rational-power encoding, and free-parameter limiting graphs used by the new scalar probes and entrance algorithm.

The prior geometric certificate search is retained in its original appendix rather than deleted. The introduction now distinguishes that supplementary existence-by-enumeration construction from the direct output algorithms. Neither complexity guarantees nor a practical arbitrary-degree resolution implementation is inferred from finite example scripts. The existing geometric proof and direct effective conclusions are preserved.

## R7. Supply the missing exact critical-example record

**Change and executed check.** `scripts/verify_a2_v100_math.py` computes both cubic examples by exact rational probability jets, without numerical differentiation or numerical optimization. The complete 26,929-byte JSON result is committed losslessly as `revisions/a2-v100/EXACT_DIAGNOSTICS.json.gz`. Its uncompressed SHA-256 is `02d4c016514a1d20b9e6716cfee6ab2453d335fe9ff3bd9621f9d60761a90213`. Decompression restores the entire JSON, not a digest-only substitute.

The record includes both free Gram matrices, projected Gram matrices and linear vectors, free optimizers, successful independent cone supports, exact rational values of mu-squared and mu-times-k, and rational isolating intervals. All projected principal minors are nonnegative; all projected linear entries are strictly negative; the empty support is the only successful independent-support KKT test. The appendix explains why these conditions prove uniqueness even though the projected Gram matrices are singular.

The script also verifies both seven-dimensional binary Fisher matrices and their profiled covariance matrices exactly. It has been executed repeatedly locally, including a final comparison with the retained full record. The endpoint result is mu approximately `0.0000632371341571021703`, k approximately `0.0718573582630708062`; the weight-wall result is mu approximately `0.00000213102491463131977`, k approximately `0.0112854054175421628`. The interval tests, not these printed approximations, are the assertions.

## R8. Bind the native build to the actual source head

**Change.** `.github/workflows/a2-v100.yml` checks out exactly the triggering commit. It expands the lossless record, checks source preservation and the principal input graph, recomputes the exact diagnostics, and invokes a recursive native TeX builder for the principal, archive and complete volume. The builder traverses inherited PDF dependencies, rather than assuming stale archive PDFs are valid.

`scripts/audit_a2_v100.py` checks the controlling report blob, addition-only preservation relative to the review, source-manifest hashes, references and citation keys. After an actual build it records each PDF/log/recorder hash, page count, and the actual repository inputs seen by TeX, with the checked-out source head. A source-only receipt cannot be reported as a native build receipt.

**Validation status.** The exact arithmetic and Python syntax checks have run locally. A complete inherited-source native TeX build has not been executed in the local environment. At preparation time the available GitHub Actions runs were queued, with no completed native receipt or artifact. The workflow definition is therefore not reported as a successful native build. `LOCAL_VALIDATION.json` records this boundary explicitly. A later native receipt must come from the actual head-bound workflow, not be fabricated in this revision.

## R9. Make the response and preservation traceable

**Change.** This response, `SOURCE_MANIFEST.json`, `LOCAL_VALIDATION.json`, the lossless exact record, and a reproduction README accompany the manuscript. The manifest pins the reviewed paper, controlling report and new source hashes, and lists the inherited imports. All modifications relative to the review are additions; the separately created v100 workflow is also new relative to that review. The final commit is identified by the branch/PR and by any runtime receipt, avoiding a self-referential committed hash.

## R10. Expand the literature comparison without conflating objectives

**Change.** `article/v100/references.tex` retains the prior references and adds normal-cone/weighted-degeneration sources, Bernig--Lytchak on subanalytic metric tangent limits, Rockafellar--Wets and Bonnans--Shapiro on variational geometry and perturbation, and Chen on finite-mixture rates. The introduction distinguishes the constrained weighted outer relation from an inner-metric tangent, and the deterministic whole-model spectral modulus from a local statistical estimation rate. The Stacks normal-cone section and the versioned Ha preprint were checked against their primary source records on September 20, 2026.

## Scope of the submission

The response presents the new proofs for independent mathematical scrutiny; it does not certify a journal's novelty threshold or acceptance decision. The exact arithmetic certifies the named finite specializations, not universal geometric theorems. The native runtime validation remains separately observable. None of these distinctions removes or weakens the inherited mathematical results.
