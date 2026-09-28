# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 58 (r39)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed publication head:** `27be4b236b9336bbfa2fa855dec3a346d63b8be7`  
**Native theorem-source commit:** `3997b7247b75b892be1fd6e313bf81b9e69c11c1`  
**Revision 57 base:** `0e07470b9693a2789af00222f063e715a83ff454`  
**Prior referee report:** r38, commit `5b2fb03f87a6b28bddcef51d498a0c78429bfa22`  
**Qualification workflow run:** `36325682981`, successful 27 September 2026  
**Review branch:** `review/general-theta-foundations-i-v58-proof-pipeline-audit-r39-2026-09-27`  
**Date:** 27 September 2026

## Executive classification

| Dimension | Audit result |
|---|---|
| Latest revision identity | **Pass.** The work and referee-ready v58 branches are identical at `27be4b...`; no v59 branch was located. |
| Native-source genealogy | **Pass.** The readable theorem source is frozen at `3997b724...`; the publication commit adds rendered and evidentiary outputs without changing native theorem source. |
| New local mathematics | **Pass with qualifications.** No fatal gap found in the least-orbit theorem, rational free endpoint, robust profile, or constructive compiler. |
| Inherited structural core | **Pass with stated hypotheses.** Same-width stationarization, stochastic purification, and finite physical quotient arguments remain coherent in their declared scope. |
| Imported deep inputs | **Qualified.** Bourgain–Gamburd is used for the noisy lower bound only; no effective spectral-gap constant is computed. |
| Finite checker | **Pass as regression evidence.** It does not prove infinite freeness, universal small-ball estimates, or spectral gap. |
| Compiler implementation | **Pass for the explicit qubit experiment.** The theorem is more general than the hardcoded CLI implementation. |
| Reproducibility pipeline | **Strong internal evidence.** One successful Actions qualification run and an isolated source/page rebuild are recorded. |
| Exact final-head CI attestation | **Partial.** The workflow self-publishes the final commit; no run or combined status is attached with `27be4b...` itself as the triggering head. |
| Independent novelty/priority closure | **Not established.** The literature audit is explicitly author-side and targeted. |
| Whole Theta A/B/C/D pipeline | **Open.** All aggregate completion flags remain false. |
| Four-leading-journal threshold | **Not met.** This is an editorial significance conclusion, not a correctness failure. |

The local proof package is materially stronger than Revision 57 and is suitable for specialist-level consideration after independent priority review. It does not close the repository-wide analytic program and should not be represented as doing so.

---

## 1. Frozen object and branch genealogy

At audit time, the two Revision 58 manuscript branches were:

```text
revision/general-theta-foundations-i-v58-finite-input-2026-09-27
revision/general-theta-foundations-i-v58-referee-ready-2026-09-27
```

Both pointed to:

```text
27be4b236b9336bbfa2fa855dec3a346d63b8be7.
```

A direct branch comparison returned `identical`, with zero commits ahead or behind. The v58 publication is four commits ahead of the v57 publication `0e07470b...`.

The review-ready entry names `3997b724...` as the qualified native source. A direct comparison from `3997b724...` to `27be4b...` shows one publication commit adding the review-ready marker, PDFs, logs, receipts, archives, theorem-location data, page checks, and inherited regression outputs. The native theorem source is not modified in that step.

Both present audit branches were created directly from `27be4b...`. Neither audit branch is descended from the other. No manuscript, predecessor, review, or unrelated paper branch is modified by these reports.

---

## 2. Mathematical dependency graph

The active proof dependencies can be compressed as follows.

### 2.1 Structural article

```text
compact stationary parameter space
  -> finite stationary obstruction
  -> Ramsey extraction from recurrent narrow cuts
  -> same-width, same-closed-error stationarization

compact joint physical/stochastic closure
  -> minimum-rank stochastic idempotent over physical identity
  -> recurrent simplex with rank-many vertices
  -> compact corner group permutes vertices
  -> width-preserving permutation purification
  -> averaging over hidden kernel
  -> finite continuous physical action
  -> open-normal finite-quotient criterion
  -> equality/attainment statements at the critical boundary
```

### 2.2 General quantitative article

```text
all-direction small-ball estimate
  + L2 spectral gap
  -> executable O(log k)-length contraction
  -> moving conditional-centroid contraction
  -> narrow-cut occupation bound
  -> width lower bound with logarithmic loss

smooth target orbit
  -> quadratic inner orbit-hull approximation
  -> common stochastic rows
  -> legal decoder rescaling
  -> polynomial upper width
```

### 2.3 Revision 58 geometric closure

```text
minimum infinitesimal orbit rank p_*
  -> uniform local submersion over every unit direction
  -> uniform O(h^{p_*}) small-ball estimate
  -> optimal all-direction cap exponent
  -> class-wide lower width exponent p_*/2
```

### 2.4 Revision 58 explicit endpoint

```text
six quaternion numerators modulo 5
  -> rank-one residue matrices with inverse-pair zero products
  -> free projective quaternion triple
  -> rational squared generators U,V form a free pair
  + third quaternion axis
  -> rational pure seed has trivial projective stabilizer
  + irrational torus powers and Lie brackets
  -> density in SU(2)
  -> reachable-state count 2*3^t-1
  + extreme legal outputs
  -> exact pointwise cut profile
  + 25^{-t} Bloch denominator lattice
  -> robust profile for epsilon <= 625^{-N}/16
  + Bourgain–Gamburd
  -> fixed-positive-error lower law
  + rational inner-hull compiler
  -> fixed-positive-error constructive upper law
```

These chains are local to the realization papers. They do not invoke the repository's A2/A3/A4, B1–B4, C1/C2, or D1 analytic gates.

---

## 3. Claim-by-claim proof audit

| Claim | Main proof location | Audit status | Principal qualification |
|---|---|---|---|
| Width-preserving stationarization | `sections/12-stationarization.tex` | No fatal gap found | Requires eventual approximate returns at every sufficiently large length. |
| Stochastic purification | `sections/09-purification.tex` | No fatal gap found | Finite labels, stationary machine, compact physical group, terminal convex outputs. |
| Finite physical quotient criterion | structural classification chain | No fatal gap found | Legal-output-constrained radius; randomized initialization may reduce minimum width. |
| General orbit occupation/lower law | `sections/16-uniform-orbits.tex` | No fatal gap found | Imported `L2` gap; lower logarithm remains. |
| Quadratic inner-hull upper law | `sections/16-uniform-orbits.tex` | No fatal gap found | Nonuniform horizon-dependent common rows are allowed by the model. |
| Least-orbit-dimension cap theorem | `sections/20-minimal-orbits.tex` | No fatal gap found | Fixed representation; constants not dimension/representation uniform. |
| Algebraic rank certificate | `sections/20-minimal-orbits.tex` | Correctly scoped | Assumes exact algebraic infinitesimal representation matrices; decision, not efficiency. |
| Extreme-output exact profile | `editions/extreme-profile.tex` | No fatal gap found | Depends critically on the legal decoder set and terminal affine injectivity. |
| Explicit rational free experiment | `sections/21-rational-endpoint.tex` | No fatal gap found | Density proof is exact; finite enumeration is only regression evidence. |
| Robust exponentially small error profile | `sections/21-rational-endpoint.tex` | No fatal gap found | Error range depends exponentially on horizon; not one fixed positive error. |
| Fixed-positive-error lower bound | `sections/21-rational-endpoint.tex` | Valid modulo imported theorem | Spectral-gap constant is non-effective. |
| Rational/dyadic compiler | `sections/22-rational-compiler.tex` | No fatal gap found | Pseudo-polynomial in numerical parameters; CLI hardcodes principal example. |

### 3.1 Stationarization

For fixed width, the stationary parameter space is compact. If no error-`epsilon` stationary machine exists, the nested finite-word feasibility sets have empty total intersection, so a finite word-length obstruction with strict margin exists.

The clocked-to-stationary extraction uses actual composite kernels between narrow cuts. Each pair is colored by a finite cell containing one neutral return kernel and one command-plus-return kernel for every command. A Ramsey-homogeneous clique gives approximate common representatives. Prefix and suffix returns, together with the clique edges, form one genuine horizon-length word for every short stationary test word.

The proof avoids three invalid shortcuts:

1. hidden return rows need not approach the identity;
2. the neutral representative need not be idempotent; and
3. individual microscopic rows need not converge.

The neutral table is absorbed into the decoder. Stochastic multiplication contracts row `l1`, so entrywise table approximation gives the needed output telescoping bound even if the stationary comparison accumulates small mass on padded labels. The resulting contradiction proves the occupation theorem and the limit of clocked minima.

The theorem is correct in its declared scope. The eventual-return assumption is essential and is not supplied by mere subsequential recurrence.

### 3.2 Purification and finite physical actions

The joint closure

```text
closure{(u_w^{-1}, T_w)}
```

is a compact semigroup projecting onto the physical compact group. A minimum-rank element has a power subnet converging simultaneously to the physical identity and to the stochastic peripheral spectral projection. The resulting idempotent has minimum rank.

The minimum-rank corner acts invertibly on the idempotent's row space and is a compact group. The fixed rows of a stochastic idempotent form the simplex generated by recurrent-class stationary distributions; their number equals the rank. Stochastic corner elements and their stochastic inverses act by affine automorphisms, hence permute the vertices.

Projecting initialization into this recurrent simplex, retaining permutation command actions, and evaluating old legal decoders on recurrent vertices gives a new machine with no width or error increase. Averaging over the finite hidden kernel above the physical identity then descends to a finite continuous action of the physical group.

The finite-quotient criterion follows through the open normal kernel of this finite action. The converse coset machine uses centers constrained to the legal output set. This is important: the ambient unconstrained Chebyshev radius is a different invariant.

### 3.3 Uniform executable contraction

The quantitative converse requires a small-ball estimate uniform over every normalized conditional-centroid direction, not merely points on the target orbit. A union bound over `k` candidate directions gives Haar defect of order `k^{-2/p}`. The group `L2` spectral gap alone controls an average norm; the proof smooths over a small Riemannian ball to obtain a pointwise value at the identity. The small ball has volume of order `delta^D`, and choosing `delta` proportional to the Haar defect leads to block length `O(log k)`.

The moving-centroid lemma applies at selected narrow cuts. Identity fillers cannot increase conditional-centroid norm by Jensen. Greedy block placement yields the occupation bound and the lower width law. The `O(log k)` executable block is exactly where the logarithmic gap enters.

The upper construction is separate. A smooth `q`-dimensional target orbit has an intrinsic net of size `O(delta^{-q})`. Vanishing first derivative of each support functional at its orbit maximum gives quadratic support loss. Since the orbit spans and has zero Haar mean, its convex hull contains a neighborhood of zero, converting additive loss to a multiplicative inner-hull inclusion. Barycentric common rows then produce the upper machine.

### 3.4 Least orbit dimension

For every unit `u`, the infinitesimal action matrix has rank at least `r=p_*`. One of finitely many `r`-minors is therefore nonzero. The maximum absolute minor is continuous and strictly positive on the compact unit sphere, so it has a positive minimum. Together with uniform entry bounds, this yields a selected derivative minor with uniformly bounded least singular value.

For each possible selected basis ordering, a small product-exponential chart is a local diffeomorphism. Uniform derivative closeness makes the projected orbit map quantitatively injective in the selected `r` variables for fixed remaining coordinates. The area/change-of-variables bound gives at most `C h^r` preimage volume for an ambient ball. Finitely many translates cover the group.

Optimality follows from a unit vector with orbit dimension `r`: the Haar pushforward is a smooth positive invariant density on the compact homogeneous orbit, and small ambient balls have lower mass of order `h^r`.

The argument is proof-level and does not depend on finite tests. The proposition computing `p_*` uses real quantifier elimination on supplied algebraic infinitesimal matrices. It does not solve compact-closure recognition or spectral-gap computation.

### 3.5 Quaternion freeness, stabilizer, and density

The six numerators `1 +/- 2i`, `1 +/- 2j`, `1 +/- 2k` map modulo five to six rank-one matrices with distinct projective image lines. Each kernel line is the image line of the inverse letter. Therefore adjacent matrix products vanish exactly for inverse cancellation. A freely reduced product has nonzero residue.

An integral scalar numerator of norm `5^n` is impossible for odd `n`; for even positive `n`, it is divisible by `5` and has zero residue, contradicting the preceding nonzero product. Hence every nonempty reduced word is nonscalar, proving free projective generation.

The displayed rational unitaries are the squares of the first two quaternion generators. A reduced word in those squares expands without cancellation to a nontrivial word in the free triple. If such a word fixed the rational pure seed, it would commute with the third quaternion direction. But conjugating the third generator by a nonempty word in the first two gives a distinct reduced word. Thus the projective stabilizer is trivial.

The trace of each rational generator is rational and nonintegral. A root-of-unity eigenvalue would make the trace a rational algebraic integer and therefore an integer. Hence powers are dense in each generator's circle subgroup. The two infinitesimal axes and their bracket span `su(2)`, proving density of the closed generated subgroup.

### 3.6 Robust cut profile

In Bloch coordinates, every generator rotation has entries in `25^{-1} Z`. A cut-`t` reachable point therefore belongs to the lattice `25^{-t} Z^3`, and distinct reachable points have Euclidean distance at least `25^{-t}`.

Fixing one suffix at a cut makes each label's conditional terminal decoder mean independent of the prefix. Frobenius error `epsilon` gives Bloch mean error at most `sqrt(2) epsilon`. Because every conditional mean lies in the unit ball,

```text
sum_i p_i ||z_i-n||^2 <= 2 sqrt(2) epsilon.
```

Thus some positive-mass label lies within radius `sqrt(2 sqrt(2) epsilon)` of the target. At the stated threshold, twice this radius is strictly less than `25^{-N}`, hence less than every relevant `25^{-t}`. The target caps are disjoint, so different prefixes require distinct labels. Deterministic exact storage supplies the upper profile.

The proof uses neither density nor spectral gap; it uses freeness/trivial stabilizer for cardinality and exact rational separation for robustness.

### 3.7 Rational compiler

The rational stereographic grid approximates every sphere direction within `sqrt(2)/m`, so every support functional has value at least `1-m^{-2}` on some grid point. The support-function criterion gives the inner ball inclusion.

For any rational rotation and vertex, the contracted target lies in the polytope. Intersecting its ray with a supporting face and triangulating gives a representation using the origin and at most three nonzero vertices. Exhaustive triple enumeration, Cramer's rule, nonnegativity checks, and exact barycentric equality produce a certified rational row.

With

```text
m >= sqrt(N/(1-beta)),  r=1-m^{-2},
```

Bernoulli's inequality gives `r^N >= beta`. Decoder Bloch vectors scaled by `beta/r^N` remain inside the unit ball, so the matrix decoders are positive semidefinite of trace one.

Dyadic rounding preserves each sparse support. With at most four entries, the total-variation row error is at most `3*2^{-b}`. Accumulation over `N` transitions and the density-matrix diameter produce the stated output-error budget.

The source implementation exactly verifies all unrounded row identities with `Fraction` arithmetic. Optional SciPy supplies only candidate facets; exhaustive triples are the fallback. The CLI currently hardcodes the explicit `I,U,U*,V,V*` alphabet and first-axis seed. The proof supports a more general supplied rational rotation list, so the code is a certified implementation of the principal experiment rather than the full generic theorem interface.

---

## 4. Finite regression audit

`check_revision.py` labels itself a finite exact regression rather than a universal proof. This distinction is borne out by its behavior.

It checks, among other things:

- exact unitarity and determinant-one identities for the displayed matrices;
- the Bloch-rotation convention;
- all six modulo-five residue matrices and the exact inverse-pair zero-product relation;
- reduced quaternion words only through a finite depth as a regression, while relying on the written induction/product proof for infinity;
- free-pair orbit profiles through a finite radius;
- denominator-lattice assertions;
- dimension formulas for the least orbit rank in the matrix example;
- rational net points and size bounds;
- exact sparse barycentric rows;
- all words at a small compiled horizon;
- dyadic stochasticity, support preservation, and TV budgets;
- explicit negative controls for wrong contraction, reversed words, illegal decoders, invalid input, and false spectral-gap claims; and
- the endpoint cap-diameter inequality over a finite range as an arithmetic regression.

It explicitly records

```text
spectral_gap_certified: false
universal_small_ball_certified_by_tests: false
```

and does not infer infinite freeness from finite enumeration. This is the correct evidentiary role.

The finite tests remain co-authored with the proof package. They are excellent regression and reproducibility evidence but not independent mathematical verification.

---

## 5. Build and workflow audit

### 5.1 Workflow topology

The branch-specific workflow is triggered on pushes to

```text
revision/general-theta-foundations-i-v58-finite-input-2026-09-27
```

for the assembly inputs or by manual dispatch. It performs the following high-level steps:

1. assemble and commit readable native source;
2. record that native-source commit in `GTF_SOURCE_COMMIT`;
3. install pinned Python packages and TeX dependencies;
4. run `build.py --check-isolated`;
5. verify that the receipt binds to `GTF_SOURCE_COMMIT` and that source hashes match both Git and the working tree;
6. commit rendered PDFs and evidence without changing native source; and
7. upload the qualification outputs as an Actions artifact.

The workflow has `contents: write` because it self-publishes the source and output commits. It also checks that staged paths remain within the isolated revision directory plus the review-ready marker.

### 5.2 Observed run

The GitHub Actions API returned one branch qualification run:

```text
run:       36325682981
trigger:   b43688da27d709e8d0e20959e334c66ef43f649c
workflow:  GTF I v58 native qualification
status:    completed
conclusion: success
```

Its sole job, `qualify`, completed successfully. Checkout, Python setup, native source commit, dependency installation, isolated qualification, qualified PDF publication, and artifact preservation all report success.

The run's `head_sha` is the triggering staging commit, not the native-source or publication commit created inside the run. This is expected for a workflow that pushes new commits itself.

### 5.3 Final-head status limitation

A query restricted to `head_sha=27be4b...` returned zero workflow runs, and the combined commit-status endpoint returned no statuses. Thus the final publication commit is causally produced by the successful run and is internally bound by the receipt/hash checks, but it is not itself the triggering head of a second read-only verification run.

This is a provenance limitation, not evidence that the recorded build failed. It means the strongest accurate statement is:

> A successful branch workflow created and internally verified the source and publication commits; the final publication SHA does not carry a separate post-publication CI run/status.

A stronger release design would use two trust stages:

1. a write-capable builder that produces a candidate commit or release artifact; and
2. a read-only verifier triggered by that exact candidate SHA, publishing a status/check on the final object.

The present self-publishing design is adequate for reproducibility but does not provide that separation.

### 5.4 Build receipt

The committed receipt records:

- Python `3.11.16`;
- SymPy `1.14.0`;
- PyMuPDF `1.26.7`;
- optional SciPy `1.17.0`;
- ten rendered documents with fixed page counts and hashes;
- no undefined references, malformed bookmarks, or overfull boxes in the recorded builds;
- source-hash equality;
- page-text and page-raster equality under isolated rebuild;
- equality of the rational compiler output;
- normal/optimized Python agreement;
- inherited regression suites from v57 back through earlier versions;
- 37,315 new finite assertions; and
- named negative controls.

The native-only isolated rebuild is especially useful: it is recorded as requiring neither repository context nor network access after the package is assembled.

The receipt is still generated by repository code and committed by the same workflow. It is reproducibility evidence, not a formal proof certificate or an independently signed attestation.

### 5.5 Remaining release-hardening items

1. Run a second read-only workflow on the exact final publication SHA.
2. Publish a signed tag or signed release for the reviewed head.
3. Preserve long-lived release artifacts rather than relying only on a 30-day workflow artifact.
4. Include the workflow run ID and final commit in a small externally verifiable release manifest.
5. Consider moving publication commits out of the qualification job so the check suite naturally attaches to the candidate being reviewed.
6. Keep the exact source archive minimal; the current package contains extensive inherited page images and evidence that are useful for provenance but heavy for ordinary journal review.

---

## 6. Literature and priority audit

The Revision 58 literature file compares the work against compact stochastic semigroups and nonnegative matrix groups, positive realization, probabilistic and weighted automata, advice automata, approximate behavioral metrics, rational series, reversible/group automata, quantum finite automata, hidden Markov realization, compact recognition, homogeneous-space entropy, and classical/quantum succinctness.

The comparisons are materially better than in earlier revisions. Classical ingredients are generally credited rather than rebranded. The file identifies the new quantifiers: same width, same closed numerical error, arbitrary intervening register widths, randomized initialization, legal convex outputs, all-direction cap uniformity, fixed rational inputs, pointwise cut profiles, robust error intervals, and constructed sparse rational tables.

However, the audit itself states that it is author-side and targeted. It also records incomplete theorem-text access in at least one neighboring controlled/HMM area. This is not a defect in proof correctness. It means independent priority closure remains open.

For editorial purposes, the following should not be inferred from the current bibliography package:

- that no equivalent stationarization theorem exists in another realization language;
- that every same-width neutral-letter/advice result has been exhausted;
- that the finite physical action reduction is new in every compact stochastic-semigroup formulation;
- that the full-density-matrix exact profile has no equivalent operator-system or automata expression; or
- that the explicit rational separation resolves a recognized external open problem.

A specialist submission should be accompanied by an independent theorem-by-theorem novelty review.

---

## 7. Repository-wide pipeline assessment

The frozen repository ledger separates the following analytic chains:

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent
```

The open obligations include raw unsmoothed local limits, stopped-path large deviations, a global past kernel and weak-Harris control, canonical shell conditioning, process CLT and Mosco recovery, nonlinear Nisio resolvents and graph cores, exact-experiment filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction.

The present finite-dimensional realization theorems neither assume nor prove these gates. The new least-orbit-rank and finite-field tools may be mathematically reusable in future work, but no concrete bridge theorem in Revision 58 connects them to an open A/B/C/D gate.

Accordingly, the following remain false:

```text
historical A2 replacement
B4 aggregate
C2 aggregate
eleven-paper aggregate
whole Theta program closure
```

This separation is healthy. It prevents local reproducibility or local theorem closure from being mistaken for global program completion.

---

## 8. Risk register

### R1 — Priority risk: high

The proof package is coherent, but equivalent formulations may exist across several mature neighboring literatures. This is the principal publication risk.

### R2 — Model-breadth risk: high for top-four, moderate for specialist venues

The width invariant omits clock and table-description costs. The results are valid in that model, but the interpretation must remain narrow.

### R3 — Quantitative sharpness risk: moderate

The logarithmic lower-bound loss is explicit and unresolved. No effective spectral-gap constant is supplied.

### R4 — Hypothesis risk: moderate

Structural clock removal depends on eventual returns at every sufficiently large length. Removing or weakening this condition is open.

### R5 — Implementation-scope risk: low

The general compiler theorem and the hardcoded qubit CLI have slightly different interfaces. Documentation can resolve this.

### R6 — Reproducibility risk: low to moderate

The internal evidence is strong and one Actions run succeeded. Exact final-head post-publication status and signature are absent.

### R7 — Whole-program overclaim risk: controlled

The current files repeatedly state that A/B/C/D aggregate closure is false. Future summaries must preserve this.

---

## 9. Recommended acceptance gates for a specialist release

A specialist-ready release should satisfy all of the following.

### Mathematical gates

- retain complete written proofs of the least-orbit, rational freeness, stabilizer, robust-profile, and compiler theorems;
- keep the imported spectral-gap theorem visually separated from the elementary exact/robust arguments;
- keep the logarithmic lower/upper mismatch in the abstract and main theorem;
- retain legal-output constraints in every exact-profile statement;
- state the recurrence hypothesis in every stationarization headline; and
- avoid claiming dimension-uniform constants.

### Priority gates

- obtain external review from experts in stochastic semigroups/positive realization and probabilistic/weighted automata;
- add a theorem-level closest-result table approved independently of the author-side audit;
- identify one clear specialist community and rewrite the introduction around its language; and
- avoid novelty claims based on the entire repository history.

### Reproducibility gates

- run read-only verification on the exact final SHA;
- sign the release/tag;
- preserve source, manifest, and core outputs as long-lived release assets;
- record the exact run ID and artifact digest in the release entry; and
- keep finite tests explicitly classified as regressions rather than proofs.

### Editorial gates

- submit the quantitative and structural papers separately;
- keep the complete research edition archival;
- reduce provenance material in the journal-facing package; and
- place the resource convention and its uncharged quantities on page one.

---

## 10. Final audit verdict

### Local mathematics

**No fatal gap found in the inspected proof chains.** Revision 58 closes the principal local technical objections from r38 concerning all-direction caps, finite-input explicitness, robust exact profiles, and constructive positive upper realizations.

### Reproducibility

**Strong, but not fully trust-separated.** The branch workflow run `36325682981` succeeded, the source/publication genealogy is coherent, and the committed isolated-rebuild evidence is extensive. The workflow self-publishes the final commit, so the final SHA lacks a separate post-publication status/check and signature.

### Priority and significance

**Not closed at the four-leading-journal level.** The theorem package is substantial but specialized; the quantitative law remains logarithmically nonsharp and partly non-effective; the output theory is terminal; and the independent novelty boundary across several classical areas remains unsettled.

### Repository-wide program

**Open.** No A/B/C/D aggregate gate is discharged by this revision.

### Overall

Revision 58 is a credible, technically serious specialist-level theorem package with unusually strong internal reproducibility records. It should be judged on the focused structural and quantitative papers, not on the wider Theta pipeline. The correct disposition is:

```text
local proof closure:          PASS WITH QUALIFICATIONS
explicit finite-input result: PASS
constructive compiler:        PASS FOR PRINCIPAL IMPLEMENTATION
reproducibility:              STRONG INTERNAL / PARTIAL FINAL-HEAD ATTESTATION
independent priority:         OPEN
whole-program closure:        OPEN
four-leading-journal bar:     NOT MET
```
