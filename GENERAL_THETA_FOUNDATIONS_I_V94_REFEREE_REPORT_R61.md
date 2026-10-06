# Referee Report — General Theta Foundations I, Revision 94 (r61)

**Focused quantitative manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*  
**Current linked supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed complete branch:** `revision/general-theta-foundations-i-v94-r60-spectral-value-2026-10-06`  
**Reviewed exact final head:** `db6739da3487be8787a67fc175b9086bd62f0e80`  
**Mathematical publication object:** `0919ff61895716ea3de1d6a0f2a6a291935764d0`  
**Qualified native source:** `24f48c90d6bcc1eae1d4c38ac5195405ac21da7d`  
**Completed predecessor publication:** Revision 93, `3b660839818d6ef676da72fb6e9969501be4e59a`  
**Predecessor native source:** `2595ee56f70138c58b1924591d32e09cbad31381`  
**Controlling external report:** r60, `cf13712c54e9ef0c9c54a240b1f26efc78cc3568`  
**Controlling proof/pipeline audit:** r60, `e4e72a512bf747e7bd190196cd8dc3db35689e3c`  
**Exact-final-head read-only run:** `37436686847`, conclusion `success`  
**Exact-final-head job:** `112180114437`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v94-spectral-value-external-referee-r61-2026-10-06`  
**Date:** 6 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**.

Revision 94 is a genuine and mathematically substantial advance over the object reviewed in r60. The earlier exact operational hierarchy established, for a specially designed two-use shared-device ensemble, different exact Bayes values for classical measure-and-reprepare adaptation, unit-reset strategies and unrestricted adaptive strategies. Revisions 91–93 then supplied the common-barycenter normal form, rank-resolved resource cuts, fixed-initial-spectrum geometry, equality sets and rigidity. Revision 94 now evaluates the biased fixed-initial-spectrum optimization itself.

For a fixed pure first acquisition with Gram state `rho`, old and fresh retained dimensions `k,l`, and

```text
r = min(k,l),
```

the paper defines the least rank-at-most-`r` majorant

```text
q^(r)(lambda(rho))
```

and the secular spectral functional

```text
H_r(rho) = chi(q^(r)(lambda(rho))).
```

For a nonzero vector `u`, `chi(u)` is equivalently

```text
lambda_max(v v^* - diag(u)),   v_i = sqrt(u_i),
```

or the nonnegative secular root

```text
sum_i u_i/(u_i+chi) = 1,
```

with value zero when the support has size at most one. With

```text
L_0 = 2(d+1)-t^2,
p_E = (d+1)/L_0,
```

the exact biased value is

```text
P^b_{k,l}(rho)
  = p_E + [t^2/(2L_0)] H_r(rho).
```

The upper is attained by a finite receiver instrument with at most `d` recorded outcomes, using commuting Gram atoms of one common spectrum, without changing the prescribed initial acquisition. The old retained register and the fresh reference may both be chosen of dimension at most `r`. The manuscript also evaluates the no-message subclass:

```text
P^nm_{d,r}(rho)
  = p_E + [t^2/(2L_0)] chi(lambda_1(rho),...,lambda_r(rho)),
```

and proves, for `t>0`,

```text
P^b_{d,r}(rho) > P^nm_{d,r}(rho)
  iff 2 <= r < rank(rho).
```

This is a clean operational theorem. It identifies exactly when communication of a receiver outcome to the next fresh preparation has positive value while the initial acquisition is held fixed. It also identifies the initial-rank saturation threshold and treats singular spectra and the deformation endpoints.

I did not find a fatal mathematical gap in the new spectral-value section or in the v91–v93 machinery on which it depends. The load-bearing steps are coherent:

1. the fixed pure initial acquisition is represented by one Gram matrix and is not silently replaced by a public mixture of different first acquisitions;
2. common-barycenter weights are Gram-decomposition weights, not hypothesis-dependent branch probabilities;
3. the leaf problem is reduced to a rank-capped filtered-swap optimization and solved by a secular equation;
4. singular support is handled by compression and pseudoinverse/support restriction rather than an illegal inverse;
5. the leaf optimizer can be chosen commuting on the leading eigenspaces;
6. the rank-capped concave roof is identified by the least rank-`r` majorizing spectrum;
7. the converse uses Ky Fan inequalities, concavity and majorization in the correct direction;
8. the finite commuting decomposition follows from finite-dimensional Schur–Horn/Birkhoff convexity;
9. the same receiver instrument may be used after every first device label;
10. the no-message class is distinguished from full measure-and-reprepare adaptation;
11. the strict message-gain criterion is invoked only in the nontrivial range; and
12. the exact executable is correctly limited to supplied spectra and certified root intervals.

The four-leading-general-journal conclusion nevertheless remains negative. The exact theorem concerns a deliberately engineered, finite, two-call shared-basis experiment with a fixed prior, a once-selected latent basis reused at both calls, a prescribed pure initial Gram state and two finite rank cuts. It does not solve arbitrary-pair quantum channel or measurement discrimination, classify finite-memory strategies in general, produce a global metric geometry of the ordered-POVM body, or establish a general law for the value of classical communication in quantum decision problems. Its spectral core is an elegant synthesis of established majorization, concave-roof, filtered-swap and finite-dimensional convexity mechanisms. In my judgment, this is strong specialist mathematics but not yet the breadth or conceptual displacement required by the four leading general mathematics journals.

**Disposition outside the four leading general journals:** the focused v90–v94 finite-game development is a serious candidate for a leading specialist journal in mathematical quantum information, quantum statistics, operator theory or mathematical physics after substantial editorial extraction and the priority revisions below. I would not request another wholesale reconstruction of the historical corpus.

---

## 1. Reviewable object and branch chronology

A numerically later branch exists:

```text
revision/general-theta-foundations-i-v95-r60-spectral-decision-2026-10-06.
```

At review time its tree contains only four base64 transport chunks. Their concatenation begins a compressed source stream but does not reach an end-of-stream marker. The branch has no materialized paper directory, no complete native source, no PDFs, no build receipt and no Actions run. It is therefore a source-transport staging branch, not a submitted revision. Branch numbering alone cannot make an incomplete transport object the review target.

The latest complete reviewable object is v94 at

```text
db6739da3487be8787a67fc175b9086bd62f0e80.
```

The mathematical publication in that chain is

```text
0919ff61895716ea3de1d6a0f2a6a291935764d0,
```

whose qualified native-source parent is

```text
24f48c90d6bcc1eae1d4c38ac5195405ac21da7d.
```

The commits after the publication add a review entry and an exact-final-head request/receipt; they do not alter theorem source. Run `37436686847`, job `112180114437`, checked out exact head `db6739...` without persisted write credentials and reconstructed the four manuscripts and regression package read-only.

The package contains:

```text
focused primary article:        78 pages,
linked binary supplement:       87 pages,
independent structural paper:   41 pages,
complete preservation edition: 289 pages.
```

The primary is the journal-facing object. The complete edition is an archive and should not be counted as a second submission or as evidence of significance.

The build receipt records 870 current source files, 841 predecessor native files, 1088 complete-edition labels, 256 quantitative-package labels, 116 structural labels and 36 regression suites. Inherited mathematical sections are reported byte-identical. This is strong source-preservation evidence, but not a formal proof certificate.

---

## 2. Exact operational interface

The theorem is meaningful only with its complete interface visible.

### 2.1 Shared finite family

The unknown device belongs to the finite once-selected basis family introduced in the operational hierarchy. One latent basis is sampled once and the same device is queried twice. Redrawing the basis independently at each use would destroy the shared second-moment signal and would be a different experiment.

The deformation parameter satisfies `0<=t<=1`, the dimension is fixed at `d>=2`, and the prior is the biased prior built into the experiment. Revision 94 does not optimize the prior.

### 2.2 Fixed pure initial acquisition

The first acquisition is fixed by a pure probe–reference state with Gram matrix

```text
rho = C_0^* C_0 in D_d.
```

This is stronger than fixing only a reduced state after a classical resolution. The first acquisition may not be replaced by an ensemble of distinct acquisitions selected by a public seed. Such a replacement would change the feasible common-barycenter problem.

### 2.3 Receiver outcome and common barycenter

After the first use, a receiver instrument produces a classical outcome `h` and an old retained quantum register. The same outcome may choose the fresh second-use preparation. The branch Gram matrices satisfy a common-barycenter identity whose total trace weight is normalized only after division by `d`. The manuscript must keep this distinction visible: Gram weights are not ordinary probabilities before normalization.

### 2.4 Rank cuts

The old retained register has dimension at most `k`; the fresh reference has dimension at most `l`. Only

```text
r=min(k,l)
```

enters the exact value. Every occurrence of “rank `r`” should be read as rank at most `r`, with zero padding allowed.

### 2.5 No-message subclass

The no-message comparator fixes the fresh second-use state independently of `h`. It is not the same as a fully classical strategy that measures and re-prepares every quantum register. The distinction is essential to the strict-message theorem.

---

## 3. Cumulative v91–v94 theorem chain

Revision 94 should be read as the endpoint of a cumulative chain, not as an isolated formula.

### 3.1 Common-barycenter variational principle

The earlier revision reduces every legal two-call reset strategy to a finite or closed common-barycenter decomposition. Conversely, every legal decomposition is implementable by a receiver instrument through a support pseudoinverse. This supplies an exact variational principle rather than an upper bound.

The corresponding Hermitian-majorant dual is important because it separates the fixed barycenter from branchwise continuation values. This general result applies beyond the particular rank-capped closed form of v94.

### 3.2 Rank-resolved memory cuts

The next stage constrains the old and fresh retained dimensions and shows that their operational effect depends on the active overlap `r=min(k,l)`. For the globally optimized engineered experiment, explicit biased- and equal-prior rank formulas are obtained.

Those formulas do not yet answer the prescribed-initial-spectrum question: a globally optimal first acquisition may itself depend on `r`.

### 3.3 Initial spectra, equality and rigidity

The subsequent stage fixes the initial Gram spectrum, identifies when the global rank-`r` optimum remains attainable, gives commuting projection-frame decompositions and proves quantitative rigidity/stability near the optimal face.

Revision 94 then evaluates the whole prescribed-spectrum value, not only its equality set.

---

## 4. Mathematical audit of the new spectral theorem

### 4.1 The secular functional

For `u>=0`, let `v_i=sqrt(u_i)` and

```text
K(u)=v v^* - diag(u).
```

The largest eigenvalue is nonnegative. On support size at least two it is the unique positive solution of

```text
sum_i u_i/(u_i+x)=1.
```

On support size at most one it is zero. This agrees with the matrix formula and makes the singular boundary continuous.

The manuscript proves the properties needed later: symmetry, positive homogeneity, coordinatewise monotonicity, concavity and strict Schur concavity away from the trivial boundary. The variational matrix formula is the cleanest source of concavity; the secular formula is the cleanest source of strict comparison and computation.

I find these arguments sound in the finite-dimensional setting used here. The strict statement should continue to be accompanied by its support and non-proportionality qualifications.

### 4.2 Rank-capped leaf optimization

The branchwise decision problem reduces to the negative part of a filtered swap, with a positive old Gram operator `A` and a fresh density operator `B` of rank at most `l`. Compression to the leading support and a rearrangement argument align an optimizer with the leading eigenspaces of `A`. The remaining scalar optimization is the secular problem.

The resulting branch value is one half of the secular functional applied to the leading admissible eigenvalues. The factor one half, normalization of `B`, support convention and unhalved/halved discrimination conventions must remain explicit.

The optimizer may be chosen commuting with `A` on the active support. Degenerate leading eigenspaces produce nonuniqueness but do not change the value.

### 4.3 Least rank-capped majorant and concave roof

For a probability spectrum `lambda`, the water-filled vector `q^(r)(lambda)` is the least spectrum supported on at most `r` coordinates that majorizes `lambda`. Equivalently, it preserves the largest coordinates above a water level and equalizes the remaining active mass, with zero padding thereafter.

For any continuous symmetric concave functional `f`, the paper proves that the rank-capped concave roof over decompositions with barycenter spectrum `lambda` equals

```text
f(q^(r)(lambda)).
```

The upper follows from Ky Fan majorization of the average branch spectra, the minimality of `q^(r)`, Schur concavity and Jensen. The lower follows by representing `lambda` in the convex hull of permutations of `q^(r)(lambda)` and choosing commuting atoms. The finite-dimensional construction can be reduced to at most `d` atoms.

This is the central convex-geometric step. I find the direction of the majorization inequalities and the attainment construction coherent.

### 4.4 Exact converse

The common-barycenter normal form expresses every strategy as a weighted family of branch Gram operators. Applying the leaf bound branchwise and the homogeneous extension of the secular functional gives a rank-capped concave-roof upper. The roof lemma then yields `H_r(rho)`.

The paper does not assume that the first receiver outcome diagonalizes `rho`; that restriction appears only in the commuting attainment construction.

### 4.5 Exact attainment

A finite commuting decomposition of `rho` into rank-at-most-`r` atoms with common spectrum `q^(r)(lambda(rho))` is chosen. The receiver instrument is constructed from the atom factors and the support pseudoinverse of the fixed initial factor. Completeness follows from the common-barycenter identity. The branchwise fresh state is chosen from the leaf optimizer.

This keeps the first acquisition fixed, uses at most `d` public outcomes and realizes the upper value. The same receiver instrument may be used for each first device label, which is stronger than required.

### 4.6 No-message value

When `h` is not communicated to the second preparation, common processing can be postponed and the fresh state is optimized against the unconditioned fixed Gram state. The leaf lemma then gives the truncated-spectrum expression.

This postponement argument should be isolated as a named lemma in a revised specialist submission. It is conceptually important and presently too compressed relative to the main theorem.

### 4.7 Strict message gain

The communicated and no-message values compare

```text
chi(q^(r)(lambda(rho)))
```

with

```text
chi(lambda_1(rho),...,lambda_r(rho)).
```

For `r=1` both vanish. Once `r>=rank(rho)`, water filling changes nothing and there is no gain. In the remaining range `2<=r<rank(rho)`, strict Schur concavity gives a strict gain for `t>0`.

The theorem correctly does not claim that a receiver message is always useful, or that the same criterion holds for arbitrary devices and losses.

### 4.8 Saturation and exact spectral loss

The gap to the globally optimized rank-`r` value is

```text
[t^2/(2L_0)] * [(r-1)/r - H_r(rho)].
```

It vanishes precisely on the previously identified optimal face `rho<=I/r`. For a fixed initial rank `s`, the optimized value increases through the active ranks and saturates once `r>=s`.

This is a useful consistency check linking v94 to the earlier equality and rigidity theorem.

---

## 5. Computational evidence

The v94 executable accepts a supplied rational spectrum, rank cuts and rational deformation parameter. It computes the water-filled majorant exactly, isolates the secular root with rational bisection, and returns certified intervals for the communicated value, no-message value and their difference.

The suite records 755 exact checks, 600 deterministic numerical sanity checks and 12 rejection controls, in addition to the inherited suites. Ordinary and optimized Python outputs agree.

The executable does **not**:

- estimate an unknown spectrum from device calls;
- verify that a physical laboratory instrument realizes the common-barycenter decomposition;
- synthesize an efficient general receiver;
- prove the continuum theorem by finite tests;
- establish optimal constants outside the stated game; or
- supply independent priority clearance.

The manuscript and machine-readable flags correctly preserve these limits.

---

## 6. Literature and priority

The current comparison now acknowledges the relevant traditions:

- concave roofs and assistance-type optimizations;
- finite-dimensional majorization and Schur–Horn/Birkhoff convexity;
- swap/partial-transpose and negativity calculations;
- constrained classical and quantum memory in channel discrimination;
- coherent-memory-dimension resource measures; and
- adaptive versus nonadaptive channel discrimination.

The manuscript should not claim first introduction of concave-roof optimization, majorization-based ensemble construction, memory restrictions or filtered-swap spectral analysis. Its plausible novelty lies in the exact synthesis for the prescribed-initial-spectrum reset game, the rank-capped least-majorant evaluation, the finite implementer and the sharp message criterion.

An author-side targeted comparison and unsuccessful search for an identical formula are not independent priority clearance. Before a strong novelty statement is made, a specialist familiar with finite-memory discrimination, entanglement assistance and rank-constrained matrix convexity should assess whether an equivalent roof evaluation or message criterion already appears in another language.

---

## 7. Why the four-leading-general-journal threshold is not met

### 7.1 Speciality of the exact game

The theorem is exact because the experiment has unusually strong structure: a finite basis family, reuse of one latent basis, two calls, a particular block form, a prescribed prior, a pure initial Gram state and dimension cuts that reduce to one active rank. The result does not presently survive as an explicit formula for a generic pair of measurements or channels.

### 7.2 General result remains variational

For arbitrary two-call reset experiments, the manuscript has an exact variational principle and dual, but not a universal closed form or classification. The v94 formula evaluates one important family inside that general framework.

### 7.3 No general memory hierarchy

The paper does not classify bounded quantum memory across arbitrary horizons, bounded classical memory, mixed initial resources, coherent communication across nominal reset boundaries, networks or indefinite causal order. Nor does it prove an arbitrary fixed-pair separation between every adjacent resource class.

### 7.4 Local geometry remains nonuniform

The inherited tangent-tube theorems are fixed-base, fixed-direction and fixed-remainder statements. Their constants may degenerate near changing support or collapsing correction gaps. They do not yet give a global bi-Lipschitz or stratified metric geometry of the whole ordered-POVM body.

### 7.5 Broader statistical programme remains open

Full-boundary entropy, common learning, sharp growing-outcome minimax laws, efficient dictionaries, general recovery synthesis and collective-readout synthesis remain separate problems.

### 7.6 Conceptual mechanisms are established

Helstrom optimization, majorization, concave roofs, finite convex decompositions, secular rank-one perturbations and memory-constrained discrimination are established mechanisms. The manuscript uses them effectively, but the conceptual displacement is not yet of general-journal scale.

---

## 8. Required revisions for a specialist-journal submission

### R01 — Freeze the actual review object

State explicitly that v94 at `db6739...` is the latest complete reviewable object and that the higher-numbered v95 branch is incomplete source transport. Do not use “latest revision” for an unmaterialized transport branch.

### R02 — Put the cumulative theorem chain on page one

The abstract and introduction should explain the sequence:

```text
common-barycenter variational principle
-> rank-resolved cuts
-> fixed-spectrum optimal face and rigidity
-> exact prescribed-spectrum value
-> exact receiver-message criterion.
```

The novelty is this cumulative chain, not the isolated secular equation.

### R03 — Separate the general and special results

Distinguish visibly between:

1. the exact variational/dual theorem for arbitrary two-call reset experiments; and
2. the closed spectral formula for the engineered shared-basis game.

Do not let readers infer that every two-call memory problem has the displayed formula.

### R04 — Define the least rank-capped majorant once and canonically

Give a formal definition of `q^(r)`, its water-level construction, uniqueness, support convention and minimal-majorant property before its first theorem use.

### R05 — Expand the leaf lemma

State the filtered-swap operator, trace convention, rank convention, singular support case, secular equation and optimizer normalization in one self-contained result.

### R06 — Define the homogeneous extension before use

The converse uses superadditivity of the homogeneous extension of the concave functional. Define that extension and prove the needed superadditivity before the theorem proof invokes it.

### R07 — Isolate the no-message postponement lemma

Prove as a named lemma that common processing can be postponed in the no-message class, and identify exactly which stored systems remain available at final readout.

### R08 — Clarify weights and probabilities

The branch trace weights sum to `d`, while normalized public probabilities sum to one. Use separate notation and repeat the normalization at the variational theorem and the finite implementer.

### R09 — Separate prior-dependent formulas

The v94 closed form is biased-prior. The equal-prior rank formula belongs to an earlier globally optimized theorem. Do not combine them into a prior-independent “memory law.”

### R10 — Clarify the finite decomposition bound

Explain why at most `d` outcomes suffice in the commuting construction, rather than merely citing an unrestricted Carathéodory bound.

### R11 — Treat eigenvalue ties explicitly

State how the leaf optimizer and the finite decomposition behave when the `r`th eigenvalue is repeated. Value invariance is clear, but optimizer nonuniqueness should be acknowledged.

### R12 — Strengthen theorem-level literature comparison

Compare the actual optimization objects, feasible decompositions, rank restrictions and losses in the concave-roof, majorization, negativity and finite-memory antecedents. Bibliographic proximity is not enough.

### R13 — Obtain independent specialist priority assessment

No repository chronology, build identity or regression suite can replace an independent assessment of mathematical priority.

### R14 — Extract the specialist paper

A 78-page primary carrying many generations of retained results is too diffuse. A specialist submission should center the v90–v94 finite-game chain and move most historical coding, learning and preservation material to the linked supplement or archive.

### R15 — Correct release semantics

Use the exact identities:

```text
native theorem source: 24f48c...
artifact publication:  0919ff...
review/exact-head:      db6739...
read-only run/job:      37436686847 / 112180114437.
```

The read-only run verifies `db6739...`; it is not a direct run on `0919ff...`. Legacy combined-status lists are empty and should not be represented as populated.

### R16 — Resolve the promised review alias

If documentation promises a `review-ready` alias, create it and pin it, or remove the promise. A reader should not have to infer the review head from chronology.

### R17 — Clean up v95 transport staging

Complete, validate and publish the transport, or mark the branch unambiguously as incomplete staging. Do not let automated “latest branch” selection choose it as a manuscript.

### R18 — Preserve wider-pipeline separation

Continue to state that the finite measurement theorem does not close the historical A2 replacement, B4, C2, eleven-paper or whole-programme aggregates.

---

## 9. Detailed comments

### D01 — Rank means “at most”

Use `rank<=r` consistently. Exact rank is not required, and zero padding is used at singular points.

### D02 — Endpoint `t=0`

State next to the strict-gain theorem that all values collapse to the baseline at `t=0`.

### D03 — Endpoint `r=1`

The secular value is zero. This should be visible in the theorem statement rather than left to a convention several pages earlier.

### D04 — Initial rank one

A pure Gram spectrum saturates immediately; messages cannot improve the value. This is a useful sanity check.

### D05 — Full active rank

When `r>=rank(rho)`, `q^(r)(lambda)=lambda` and the communicated/no-message values agree. State the identity explicitly.

### D06 — Matrix versus root definitions of `chi`

Prove their equivalence once and use one notation thereafter. The matrix definition handles boundaries; the root definition handles computation.

### D07 — Zero coordinates

Terms with `u_i=0` should be removed from the secular sum before uniqueness is asserted.

### D08 — Strict Schur concavity

List the exact equality cases. Proportionality and one-point support are boundary exceptions.

### D09 — Water level

Give the index-selection rule for the water level and verify continuity as the active set changes.

### D10 — Leading-eigenspace ties

Avoid language suggesting a canonical optimizer when the leading spectral subspace is degenerate.

### D11 — Factor one half

Keep the factor connecting negative filtered-swap mass to Bayes improvement visible in every transition.

### D12 — Trace norm convention

The broader paper uses unhalved trace separation, while Bayes formulas introduce their own halves. Repeat conventions at the finite game.

### D13 — Pseudoinverse

Specify that the support pseudoinverse is taken on `supp(rho)` and that the constructed instrument vanishes on the orthogonal complement before completion.

### D14 — Common instrument across labels

This strengthening is interesting and should be highlighted as a corollary, not buried in the attainment proof.

### D15 — At most `d` messages

Give the actual convexity argument producing this cardinality.

### D16 — No-message versus classical adaptation

These are different resource classes. Add a small inclusion diagram.

### D17 — Fixed-Gram versus global optimum

A positive fixed-Gram message gain is compatible with a globally optimized strategy that needs no feedback. Repeat this qualification near the operational interpretation.

### D18 — Biased versus equal prior

Do not use one formula as evidence for the other without restating the objective.

### D19 — Example

The `d=3,r=2` spectrum `(3/4,1/8,1/8)` is useful; include the actual two values or their certified intervals in the primary text.

### D20 — Real spectra

The theorem is analytic for arbitrary real spectra. Rationality belongs only to the executable interface.

### D21 — Numerical bisection

Report an interval certificate, not a floating-point point estimate, when the secular root is irrational.

### D22 — Physical synthesis

Existence of a finite receiver instrument does not give an efficient circuit. Preserve this distinction.

### D23 — Spectrum acquisition

The script assumes the spectrum as input. It is not a tomography or learning algorithm.

### D24 — Page length

The primary should be shortened sharply for journal submission. Preservation concerns should not determine the journal-facing organization.

### D25 — Bibliography

Consolidate duplicate historical bibliographies and make the current comparison the sole journal-facing priority map.

### D26 — Theorem numbering

A reader should not need the complete 289-page edition to identify the v90–v94 dependency chain. Add a current theorem map.

### D27 — Build evidence

Keep the PDF hashes and source identities, but move long regression inventories out of the mathematical narrative.

### D28 — Status language

Use “verified by the source-bound read-only reconstruction” rather than “approved,” “certified mathematics,” or “independently accepted.”

### D29 — Unsigned commits

Object identity is not human authorship authentication. The current package correctly avoids that claim; preserve the distinction.

### D30 — Open programme

Do not use the size of the archive or the existence of many prior sections as a significance multiplier for this submission.

---

## 10. Verification and interpretive boundary

The source/build package is unusually careful. The native source was isolated, the publication artifacts were rebuilt, inherited source was preserved, 36 suites were executed under ordinary and optimized Python, and the exact review head was reconstructed read-only by run `37436686847`, job `112180114437`.

These facts establish a strong relationship among repository objects and finite computations. They do not establish:

- formal proof-assistant verification;
- independent mathematical priority;
- verified human authorship;
- physical realization of the reset condition;
- efficient quantum-control synthesis;
- arbitrary-pair or arbitrary-horizon generalization; or
- closure of the wider Theta programme.

## Final disposition

The v94 spectral theorem is mathematically serious, appears correct in the load-bearing portions inspected, and materially improves the paper. It should be preserved and developed. My negative recommendation is specifically a judgment about the breadth, priority clearance and conceptual scale required by the four leading general mathematics journals.

For a leading specialist journal, I would recommend **major revision**, centered on a shorter self-contained v90–v94 article, a sharper theorem-level priority comparison, exact release semantics and a cleaner separation between the general variational theorem and the engineered closed form.
