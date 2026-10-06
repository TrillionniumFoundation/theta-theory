# Referee Report — General Theta Foundations I, Revision 94 (Independent r62 Re-review)

**Focused quantitative manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*  
**Linked supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete archival edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`

**Reviewed complete branch:** `revision/general-theta-foundations-i-v94-r60-spectral-value-2026-10-06`  
**Reviewed exact final head:** `db6739da3487be8787a67fc175b9086bd62f0e80`  
**Qualified native theorem source:** `24f48c90d6bcc1eae1d4c38ac5195405ac21da7d`  
**Artifact publication object:** `0919ff61895716ea3de1d6a0f2a6a291935764d0`  
**Highest numerical branch inspected:** `revision/general-theta-foundations-i-v95-r60-spectral-decision-2026-10-06`, head `fd2b0d8d49fe0ab72886df89966b03cfe62057d7`  
**Prior external report:** v94/r61, `df919e7a2d917d71f5525d2034f524b97809121b`  
**Prior proof/pipeline audit:** v94/r61, `a5b01294ce8fe7d4ca3782f762fba71f0cd44509`  
**Exact-final-head workflow:** run `37436686847`, job `112180114437`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v94-spectral-value-independent-referee-r62-2026-10-06`  
**Date:** 6 October 2026

This is an author-requested external mathematical assessment stored in the repository. It is not a commissioned editorial decision of any named journal.

## Recommendation

**Reject at the Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica level.**

This is **not a correctness rejection**.

The v94 theorem chain is mathematically serious. I did not find a fatal gap in the new prescribed-spectrum value theorem, in its rank-constrained filtered-swap leaf optimization, in the rank-capped spectral concave-envelope argument, or in the finite instrument that attains the upper bound while keeping the first acquisition fixed. The inherited v91–v93 normal-form, rank-resolution, equality-set and rigidity results used by v94 are coherent in the load-bearing portions I checked.

The negative four-leading-general-journal recommendation is instead a judgment about **scope, conceptual displacement, priority clearance and presentation**. The closed form is obtained for a deliberately engineered finite two-call experiment with a once-selected latent basis reused at both calls, a prescribed biased prior, a fixed pure first acquisition and two specified retained-register cuts. The general arbitrary-experiment theorem remains a variational/dual characterization rather than a universal classification or closed formula. The wider local tangent-tube theory remains fixed-base and nonuniform, and the broader Theta analytic programme remains explicitly open. The package therefore contains strong specialist mathematics, but it does not presently reach the breadth expected at the four leading general mathematics journals.

For a leading specialist journal in mathematical quantum information, quantum statistics, operator theory or mathematical physics, I would recommend **major revision and resubmission**, not rejection on mathematical grounds. The v90–v94 finite-game chain should be extracted as a shorter, self-contained article; the no-message reduction should be promoted to a named lemma; the exact theorem should be compared at theorem level with the constrained-memory literature; and an independent specialist priority assessment is still required.

---

## 1. Frozen review object and branch chronology

### 1.1 Why v95 is not the review target

The repository contains a numerically later v95 branch. At the time of this review, its visible head adds only the fourth source-transport chunk `tools/gtf95/payload-3.b64`; its immediate ancestors add the preceding chunks and transport scaffold. The branch has no materialized v95 paper directory, no complete native source tree, no rendered manuscript, no build receipt and no exact-head reconstruction. It is therefore a transport/staging branch, not a deposited referee-ready revision.

A branch number is not sufficient to define a mathematical submission. The minimum review object must contain a readable source, a stable theorem statement, its dependencies and a reproducible final head. v95 does not yet satisfy those conditions.

### 1.2 The latest complete reviewable revision

The latest complete object is v94 at exact final head

```text
db6739da3487be8787a67fc175b9086bd62f0e80.
```

Its mathematical source is frozen at

```text
24f48c90d6bcc1eae1d4c38ac5195405ac21da7d,
```

and its rendered publication child is

```text
0919ff61895716ea3de1d6a0f2a6a291935764d0.
```

The commits after publication add review/final-head metadata and do not alter theorem source. The successful read-only workflow run `37436686847`, job `112180114437`, is bound to the exact final head `db6739...`, not directly to the artifact publication SHA. The distinction should remain explicit.

### 1.3 Package structure

The build receipt records:

```text
focused primary article:        78 pages
linked supplement:              87 pages
structural companion:           41 pages
complete archival edition:     289 pages
regression suites:               36
current source files:           870
```

The complete edition is an archival preservation object. It should not be treated as a second submission or as evidence of journal significance. The focused article is the relevant editorial object, while the supplement carries linked dependencies.

### 1.4 Relation to r60 and r61

The v90/r60 report accepted the central exact three-class hierarchy as apparently correct but rejected it at the four-leading-general-journal level because of breadth and priority. Revisions 91–94 materially strengthen the mathematics: they add an arbitrary finite two-call reset variational principle, rank-resolved cuts, the complete initial optimal face and rigidity, and finally the exact value at every prescribed initial spectrum.

A v94/r61 referee report and a companion proof/pipeline audit already exist. I reviewed the current source and its proof chain and then compared my conclusions with those reports. The present r62 report is a new branch and does not overwrite r61. Its conclusion agrees with r61 on correctness and journal scale, while adding an explicit editorial finding concerning stale Revision 93 PDF metadata in the v94 complete edition and separating more sharply the acceptable mathematical compression from the points that should be expanded before specialist submission.

---

## 2. Main theorem and operational meaning

Fix dimension `d>=2`, deformation parameter `0<=t<=1`, and the finite weighted ordered-basis family satisfying the exact second-moment identities of the v90 experiment. One latent basis index is sampled once and reused at both calls. Let

```text
L_0 = 2(d+1)-t^2,
p_E = (d+1)/L_0.
```

The first acquisition is fixed by a pure input-reference vector with Gram state `rho`. The old retained receiver dimension is bounded by `k`, the independently prepared fresh reference by `l`, and

```text
r = min(k,l).
```

For a nonnegative vector `u`, write `v_i=sqrt(u_i)` and define

```text
chi(u) = lambda_max(v v^* - diag(u)).
```

When the support has at least two points, this is the unique positive solution `x` of

```text
sum_i u_i/(u_i+x) = 1;
```

when the support has size at most one, it is zero.

Let `q^(r)(lambda(rho))` be the least probability vector of support at most `r` that majorizes the spectrum of `rho`, obtained by preserving the entries above a water level and flattening the remaining active mass. Set

```text
H_r(rho) = chi(q^(r)(lambda(rho))).
```

The v94 theorem states

```text
P^b_{k,l}(rho)
  = p_E + [t^2/(2L_0)] H_r(rho).
```

The upper is attained by a finite receiver instrument with at most `d` recorded outcomes. The construction leaves the prescribed first acquisition unchanged, may use the same receiver instrument after every first device label, and uses old and fresh retained dimensions at most `r`.

For the no-message subclass—where the receiver outcome is not used to select the fresh preparation—the value is

```text
P^nm_{d,r}(rho)
  = p_E + [t^2/(2L_0)]
      chi(lambda_1(rho),...,lambda_r(rho)).
```

For `t>0`, the message has strict value exactly when

```text
2 <= r < rank(rho).
```

The result therefore distinguishes three statements that should not be conflated:

1. a general variational theorem for arbitrary finite two-call reset experiments;
2. a closed spectral formula for one designed shared-basis family; and
3. a necessary-and-sufficient message-gain criterion for that family at a prescribed pure initial Gram state.

This is a clean and nontrivial operational result.

---

## 3. Audit of the cumulative v91–v94 proof chain

### 3.1 Unit-reset normal form

The v91 normal-form lemma is the correct starting point. A general unit-reset strategy is purified while retaining the reset cut. On every formal branch `(y,h)` it produces rectangular coefficient maps with Gram operators

```text
rho = C_0^* C_0,
A_yh = C_yh^* C_yh,
sum_h A_yh = rho,
b_yh = D_yh^* D_yh,
tr b_yh = 1.
```

The receiver block factors as an old conditional block tensor an independently prepared fresh block. Countable instruments are controlled by positive trace-class tails, public randomization is absorbed into a recorded seed, and abstract tester closure is invoked only after finite values have been realized and continuity applied.

The converse is also operationally meaningful: a finite legal Gram collection is implemented through the support pseudoinverse of `C_0`. Positivity of the common Gram sum forces every branch support into `supp(rho)`, so the pseudoinverse is used only where it is defined. This avoids the common error of silently inverting a singular initial state.

I find this reduction adequate for the stated finite-dimensional decision problem. It does not classify all physical notions called “memory”; it classifies the paper's specified fresh-preparation cut.

### 3.2 General variational principle and dual

For an arbitrary finite experiment, the branch continuation value is optimized first over the fresh state and final POVM, and then concavified over old Gram atoms with one common barycenter. This gives an attained primal formula. A Hermitian-majorant dual is obtained from the homogeneous hypographs of the concave envelopes, with finite-dimensional Slater duality.

Two points are important and correctly preserved:

- the envelope is over all density matrices, not only pure states;
- the branch weights are Gram-decomposition weights, not hypothesis-dependent history probabilities.

The contact-defect identity provides genuine quantitative optimality information when a universal majorant is known. Finite sampling of that universal inequality is not treated as a certificate.

### 3.3 Rank-resolved cuts

The v92 refinement records Kraus indices classically so that retained quantum dimensions are not enlarged by a dilation environment. This yields exact rank constraints on the old and fresh Gram factors and a rank-resolved variational/dual principle.

The finite-rank swap bounds are compatible with the underlying filtered-swap spectrum. Their equality cases lead to common flat projections, and the cyclic construction attains the complete two-cut dimension spectrum. The dependence on `min(k,l)` is a theorem for the specified family and reset architecture, not a general theorem about all memory-limited discrimination problems.

### 3.4 Initial spectra and rigidity

The v93 theorem identifies the complete set of initial states attaining the globally optimized rank-`r` value:

```text
rho <= I/r.
```

The interval-selection construction decomposes every such `rho` into at most `d` commuting normalized rank-`r` projections. This construction is elementary and effective at the level of a known spectrum. It does not construct the finite second-moment basis family.

The equality and stability results are consistent with the rank-sensitive swap inequalities. The quantitative constants are explicit but not claimed optimal. The exceptional `(d,r)=(2,1)` face is treated separately, which is necessary because the generic rigidity coefficient vanishes there.

### 3.5 The secular functional

The matrix definition of `chi` immediately yields symmetry, homogeneity and concavity through the maximal-eigenvalue variational formula after the appropriate superlevel-set argument. The secular equation supplies uniqueness on support size at least two and makes coordinate monotonicity transparent.

The strict Schur-concavity argument uses the strict concavity of `x/(x+c)` for fixed `c>0`. It is valid once the support and permutation exceptions are stated. The manuscript correctly handles the one-point support boundary by the matrix definition rather than forcing a positive secular root where none exists.

### 3.6 Rank-capped leaf optimization

For a positive old Gram `A` and a fresh density `B` of rank at most `l`, the relevant gain is the negative mass of the filtered swap. The v90 spectrum identity rewrites it in terms of the nonzero eigenvalues of `sqrt(A) B sqrt(A)`.

The v94 leaf proof then:

1. compresses to `supp(A)`;
2. uses the inverse-trace constraint only on that support;
3. aligns the active spectrum with the leading eigenspaces of `A` by a rearrangement inequality;
4. normalizes the resulting fresh density;
5. reduces the scalar optimization to the maximal eigenvalue of a rank-one perturbation; and
6. obtains one half of the truncated secular value.

This avoids an illegal claim that pinching automatically preserves the rank constraint. The optimizer may be chosen commuting with `A`, but it need not be unique when the leading eigenspace is degenerate.

I re-derived the filtered-swap spectrum and checked low-dimensional noncommuting instances against the stated optimizer. I found no normalization or factor-of-two defect.

### 3.7 Rank-capped concave roof

Let `lambda` be the spectrum of the prescribed barycenter. For any decomposition into rank-at-most-`r` atoms, Ky Fan inequalities imply that `lambda` is majorized by the average branch spectrum. Because `q^(r)(lambda)` is the least rank-`r` majorant, it is itself majorized by that average spectrum. Symmetry and concavity of the objective then give the upper through Schur concavity and Jensen.

For the converse, `lambda` lies in the convex hull of permutations of `q^(r)(lambda)`. Commuting diagonal atoms realize this decomposition; finite-dimensional Carathéodory reduction gives at most `d` atoms. Thus the roof is not merely bounded but evaluated and attained.

The direction of the majorization inequalities is load-bearing. In the manuscript it is the correct direction.

### 3.8 Exact fixed-spectrum converse

Every legal strategy has branch Grams whose sums equal the same fixed `rho` for every first label. The leaf bound is applied to each branch. When the old rank is the smaller cut, the leaf value already equals the homogeneous spectral functional; when the fresh rank is smaller, coordinate monotonicity bounds the truncated leaf value by the rank-capped majorant value.

The homogeneous concave extension is superadditive, so each first-label branch sum is bounded by `H_r(rho)`. Summation over the `d` first labels exactly cancels the `1/d` in the payoff constant. The final coefficient is therefore

```text
t^2/(2L_0),
```

as stated.

I find the constant accounting correct.

### 3.9 Exact attainment

The roof lemma supplies a commuting decomposition

```text
rho = sum_h w_h a_h
```

with every atom having spectrum `q^(r)(lambda(rho))`. Factors `C_h` and the support pseudoinverse of `C_0` give a trace-preserving recorded instrument on the initial Schmidt support. Each branch fresh state is chosen from the leaf optimizer, and the final effect is the positive spectral projection of the filtered payoff block.

This realizes equality branch by branch. It uses at most `d` messages and can use the same instrument after every first label. The construction is an existence proof, not an efficient circuit-synthesis theorem; the manuscript's status files correctly deny such a claim.

### 3.10 No-message value

The no-message comparator still permits the first device label, the old quantum receiver and an arbitrary final joint measurement; it only prohibits using the receiver-instrument outcome to choose the fresh source. A common old-receiver channel that does not influence the fresh preparation can be postponed to the final readout. The fresh state is then optimized once against the unconditioned fixed Gram, yielding the truncated secular expression.

I regard this argument as correct, but it is too compressed relative to its conceptual importance. A specialist version should promote it to a named lemma with explicit systems, allowed classical records and a Heisenberg-picture proof that postponement preserves the resource class.

### 3.11 Strict message gain and saturation

At `r=1`, both secular values vanish. When `r>=rank(rho)`, water filling does nothing and the communicated and no-message values agree. In the only nontrivial range `2<=r<rank(rho)`, the rank-capped majorant strictly increases at least one active coordinate without decreasing the others, and strict monotonicity/Schur comparison gives a positive gap for `t>0`.

The exact loss from the globally optimized rank-`r` value is

```text
[t^2/(2L_0)] * [(r-1)/r - H_r(rho)],
```

and vanishes exactly on the v93 optimal face `rho<=I/r`. This consistency with the previous equality-set theorem is a strong internal check.

---

## 4. What the proof does and does not establish

The manuscript establishes:

- an attained common-barycenter variational principle for arbitrary finite two-call reset experiments;
- an attained Hermitian-majorant dual and contact-defect identity;
- exact rank-resolved values for the specified shared-basis family;
- the complete optimal initial face and quantitative rigidity for the equal-prior family;
- the exact biased value at every prescribed pure initial spectrum;
- a finite attaining instrument;
- an exact no-message comparator; and
- a necessary-and-sufficient receiver-message advantage criterion in the stated family.

It does not establish:

- an explicit value formula for an arbitrary fixed pair of measurements or channels;
- strict separation for every arbitrary experiment;
- a classification of bounded coherent memory for arbitrary horizons;
- an equivalence among all operational definitions of quantum memory;
- an efficient global reset optimization or circuit-synthesis algorithm;
- device-independent certification of the reset cut from the score alone;
- physical calibration of reset independence or preparation defects;
- a global metric geometry of the full ordered-POVM body;
- a uniform theorem across changing support strata for the local tangent problem; or
- closure of the historical A2, B4, C2, eleven-paper or whole-Theta aggregates.

The machine-readable status file is commendably explicit about these negative statements.

---

## 5. Reproducibility and provenance

### 5.1 What is well done

The source/build package is unusually careful. It distinguishes:

- qualified native theorem source;
- artifact-only publication child;
- later review/final-head metadata;
- read-only exact-head reconstruction;
- Actions checks versus legacy commit statuses;
- finite regression evidence versus universal proof;
- object identity versus human signature; and
- archival preservation versus journal submission.

The exact final-head run completed successfully. The final-head job checked out `db6739...`, installed the pinned reconstruction tools, rebuilt the triggering head without write credentials and uploaded an artifact. The publication job on that run was correctly skipped.

The build receipt reports no unresolved references or citations in the four manuscripts, isolated native reconstruction, standalone journal reconstruction and identical ordinary/optimized regression output.

### 5.2 Limits of the evidence

The 36 suites, exact rational bisection and negative controls are useful regression evidence. They do not prove the quantified matrix theorems, establish priority, certify physical independence at the reset cut or verify human authorship. The source and publication commits are unsigned; this is not a correctness defect, but reconstruction is not a cryptographic author signature.

The scripts accept supplied spectra and trusted model data. They are not tomography, learning or device-certification procedures.

### 5.3 Editorial/provenance defects that remain

The v94 complete-edition source `main.tex` still has

```text
pdftitle={General Theta Foundations I: Complete Research Edition, Revision 93}.
```

This is a concrete stale-version defect in a Revision 94 release. It does not affect the theorem but should be corrected before any subsequent publication or archival deposit.

The higher-numbered incomplete v95 branch is also an operational hazard: automated branch selection can misidentify a transport staging branch as the current manuscript. It should either be completed and qualified or renamed/marked unmistakably as incomplete staging.

The repository documents promise or discuss several aliases and review states. A reader should be able to identify one canonical review head without reconstructing chronology from request files. Exact source/publication/final-head semantics should be summarized in one short current manifest.

---

## 6. Literature and priority assessment

The paper now acknowledges the relevant traditions: quantum testers and combs, adaptive channel discrimination, constrained classical and quantum memory, constrained separability, majorization, pure-state ensemble transformations, concave roofs/assistance, filtered swap calculations and finite convex decompositions.

Two recent comparators are especially relevant:

1. Ohst–Zhang–Nguyen–Plávala–Quintino, arXiv:2411.08110v2, published in *Quantum* 10 (2026), formulate memory-constrained channel discrimination through constrained separability and treat adaptive classical/quantum memory.
2. Zonnios–Binder, arXiv:2606.19511v1, introduce a coherent-memory-dimension hierarchy for autonomous multi-time process discrimination and prove finite-time completeness at sufficiently large coherent memory.

Neither model is identical to the paper's fresh-acquisition reset cut, and neither source, in the portions compared, gives the v94 prescribed-initial-spectrum formula. The distinction claimed by the manuscript is therefore plausible.

Nevertheless, the mathematical mechanisms behind the v94 spectral reduction have substantial antecedents: Nielsen-type majorization, ensemble transformations, Schur–Horn/Birkhoff convexity, concave-roof optimization and rank-one secular equations. The likely novelty is the **specific synthesis** of these tools for the shared-basis reset game, including the fixed-spectrum value, finite instrument and sharp message criterion.

That is a meaningful contribution. It is not yet an independently cleared priority claim. Repository chronology, unsuccessful search and CI reconstruction do not replace review by a specialist who knows the constrained-memory, entanglement-assistance and matrix-convexity literatures. The active status correctly leaves `independent_human_priority_clearance` false.

---

## 7. Four-leading-general-journal assessment

### 7.1 The exact closed form is highly structured

The closed formula depends on a specially designed second-moment family, a shared latent basis reused twice, a particular payoff block, a fixed prior, a pure prescribed initial acquisition and two finite rank cuts. Removing those features leads back to the general variational theorem rather than another closed law.

### 7.2 The general theorem is variational, not classificatory

The arbitrary-experiment result is important, but it expresses the optimum through concave envelopes and universal majorants. It does not provide a general invariant deciding when classical communication, retained receiver memory or coherent acquisition changes the value, nor an explicit formula for arbitrary channel pairs.

### 7.3 The memory notion is intentionally narrow

The reset architecture is well defined, but it is one resource cut among several in current quantum-information work. The paper does not classify arbitrary temporal depth, bounded classical memory, mixed coherent carryover, networks or indefinite causal order.

### 7.4 The local geometry is a different theorem family

The tangent-tube profile and hard-budget laws are mathematically separate. Their constants are fixed-object and may deteriorate with changing support or correction gaps. Combining them with the exact finite game in one long primary does not turn either result into a global geometry.

### 7.5 Established mechanisms do much of the conceptual work

The proof is elegant, but its core mechanisms—Helstrom positive-part optimization, swap spectra, majorization, concave roofs, finite convexity and secular rank-one perturbations—are established. The new contribution is a sharp synthesis in a designed problem rather than a broadly new organizing principle.

For these reasons, I do not regard the current submission as meeting the expected generality or conceptual displacement of the four leading general mathematics journals.

---

## 8. Required revisions before specialist-journal submission

### R01 — Freeze and label the review object

State on the repository front page and in the manuscript package that v94 at `db6739...` is the latest complete reviewable object. Mark v95 as incomplete transport staging until it is fully materialized, built and qualified.

### R02 — Extract a focused v90–v94 article

The 78-page primary still combines the local tangent-tube programme with the finite reset-game development. Create a shorter self-contained article centered on:

```text
general reset normal form and variational principle
-> rank-resolved cuts
-> exact shared-basis hierarchy
-> prescribed initial spectra and rigidity
-> exact spectral value
-> exact message criterion.
```

Move, do not delete, unrelated historical material to the existing supplement or archival edition.

### R03 — Put the general/special distinction on page one

The abstract and introduction should visibly distinguish the arbitrary-experiment variational theorem from the engineered-family closed form. Readers should not infer a universal spectral formula for every memory-constrained discrimination problem.

### R04 — Promote the no-message reduction to a lemma

Give a named postponement lemma with explicit input, old receiver, fresh reference, classical record and final POVM spaces. Prove in the Heisenberg picture that a common old-receiver channel not communicated to the source can be absorbed into the final measurement.

### R05 — Canonicalize `q^(r)` and `chi`

Define the least rank-capped majorant once, with the active-index rule, water level, uniqueness, zero padding and tie behavior. State both the matrix and secular definitions of `chi`, their equivalence and the support-one convention before the main theorem.

### R06 — Clarify Gram weights versus probabilities

Use separate notation for unnormalized Gram traces and normalized public probabilities. At each variational formula, remind the reader that the common-barycenter weights are not hypothesis-dependent history probabilities.

### R07 — Expand the finite attainment map

Display the domains and codomains of `C_0`, `C_h`, `D_h`, `C_0^+` and `V_h`; specify completion on the orthogonal complement; and prove the at-most-`d` message bound in place rather than through a distant reference.

### R08 — Strengthen theorem-level priority comparison

Compare the actual feasible sets, resource cuts, objectives and saturation notions with constrained-separability testers, autonomous coherent-memory hierarchies, entanglement-assistance roofs and pure-state transformation results. Bibliographic listing alone is insufficient.

### R09 — Obtain independent specialist priority review

A specialist assessment remains necessary before claiming firstness beyond the precise formula proved here. Preserve the current conservative novelty language until that review exists.

### R10 — Correct version and package metadata

Change the complete-edition PDF title from Revision 93 to Revision 94. Audit all current front matter, manifests, aliases and review entries for the same stale-version problem.

### R11 — Preserve exact release semantics

Continue to distinguish:

```text
native source       24f48c...
artifact publication 0919ff...
exact final head     db6739...
read-only run/job    37436686847 / 112180114437.
```

Do not summarize these distinct facts merely as “CI passed.”

### R12 — Separate proof from regression evidence

Keep exact arithmetic, randomized sanity checks and negative controls, but move long inventories out of the mathematical narrative. State once that finite tests protect formulas and build integrity but do not prove universal theorems.

### R13 — Preserve all scope restrictions

Do not promote the result to an arbitrary-pair formula, a universal memory hierarchy, device-independent dimension certification, efficient synthesis, global POVM geometry or closure of the wider Theta programme.

### R14 — Supply one compact worked example

Give one complete `d=3, r=2` prescribed-spectrum example from initial state through water filling, secular interval, instrument decomposition, no-message comparison and strict gain. Keep rational and irrational quantities distinguished.

### R15 — Simplify the referee route

A referee should receive the primary, one linked supplement, a concise theorem map, a short reproducibility note and the current response. Historical reports, dozens of schemas and preservation ledgers can remain in the archive without appearing in the initial route.

---

## 9. Detailed comments

### D01 — Stale PDF metadata

`main.tex` identifies the complete edition as Revision 93 in `pdftitle`. This should be fixed in v94 and checked in generated PDF metadata.

### D02 — Abstract focus

The primary abstract gives substantial space to the local profile theorem. For the extracted finite-game article, lead with the general reset variational theorem and exact prescribed-spectrum result.

### D03 — Rank language

Use “rank at most `r`” consistently. Exact rank is not required, and zero padding is part of the boundary convention.

### D04 — Endpoint `t=0`

State next to every strictness claim that all signal terms vanish at `t=0` and every value reduces to the prior baseline.

### D05 — Endpoint `r=1`

The secular value and message gain vanish. Put this in the main theorem statement rather than relying only on the support convention.

### D06 — Saturation at the initial rank

When `r>=rank(rho)`, write explicitly that `q^(r)(lambda(rho))=lambda(rho)` and that communicated and no-message values coincide.

### D07 — Eigenvalue ties

A commuting leaf optimizer exists, but it is not canonical when the leading eigenspace is degenerate. State the resulting nonuniqueness.

### D08 — Secular equation at zero coordinates

Remove zero coordinates before asserting uniqueness of the positive root. The matrix definition should remain the boundary-safe primary definition.

### D09 — Strict Schur comparison

List the equality cases and support qualifications where strictness is used. The main message theorem already avoids the trivial ranges; the lemma should match it precisely.

### D10 — Factor-of-two conventions

The paper uses unhalved trace norms in several inherited sections and Bayes improvements with explicit halves. Repeat the convention at the leaf lemma and main value theorem.

### D11 — First-label versus receiver feedback

The no-message class still permits dependence on the first device label. Include a resource-inclusion diagram distinguishing label feedback, receiver feedback, complete measure-and-reprepare and unrestricted coherent acquisition.

### D12 — Fixed-Gram versus global optimization

A positive message gain at a prescribed `rho` is compatible with a globally optimized strategy that needs no message. Repeat this qualification beside the operational interpretation.

### D13 — Prior dependence

The v94 formula uses the biased prior. The earlier equal-prior rank formula is a different objective. Do not call their combination a prior-independent memory law.

### D14 — Shared latent basis

Repeat in the boxed experiment definition that one basis index is drawn once and reused at both calls. Independent redraw removes the second-moment signal.

### D15 — Finite family existence

The Carathéodory construction proves existence of a weighted exact second-moment family. It is not an efficient design algorithm or a polynomial bit-complexity result.

### D16 — Efficient synthesis

The finite instrument is an existence construction from a known spectrum and eigenbasis. No gate complexity, noise robustness or laboratory compiler is supplied.

### D17 — Physical interpretation

The dimension certificates assume the specified calibrated reset architecture. They are not device-independent consequences of a score alone.

### D18 — Countable outcomes

The positive-tail lemma is sufficient, but the specialist article should keep all countable-outcome discussion in one place rather than repeating closure language in multiple theorems.

### D19 — Build evidence placement

Keep object hashes and one reconstruction receipt in the journal package. Move detailed source inventories and historical ledgers to the archive.

### D20 — Status terminology

Use “source-bound read-only reconstruction succeeded,” not “mathematics certified,” “externally approved” or “priority verified.”

### D21 — Human signatures

Unsigned commits do not count against mathematical correctness, but object reconstruction does not authenticate authorship. The current distinction should remain.

### D22 — Wider programme

The finite measurement results do not imply the historical A2 replacement, B4/C2 aggregates, process limits, nonlinear generator cores, filtering/LAN or posterior-contraction claims. Preserve the current false flags.

---

## 10. Final assessment

Revision 94 is a real mathematical advance. The prescribed-spectrum formula is not a numerical conjecture or an evaluation of one exhibited protocol: it includes an upper over the full stated rank-constrained reset class and a matching finite implementation. The proof uses the common-barycenter normal form correctly, solves the branch leaf problem, evaluates the rank-capped concave roof and identifies exactly when receiver communication changes the fixed-initial value.

I find no fatal correctness defect in the load-bearing theorem chain inspected.

The paper should nevertheless be declined at the four-leading-general-journal level. The exact result remains tied to a specially designed two-call experiment, the arbitrary-experiment theory remains variational, independent priority clearance is absent, and the journal-facing article is still too diffuse. These are significance and presentation judgments, not reasons to discard the mathematics.

For a leading specialist journal, the appropriate disposition is **major revision**. A sharply extracted v90–v94 article, with the no-message lemma expanded, the literature comparison made theorem-specific, the version/provenance defects corrected and the archive removed from the initial referee route, would merit serious consideration.
