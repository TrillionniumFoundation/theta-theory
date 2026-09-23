# Independent harsh referee report — A2 revision 141

## Manuscript and review scope

**Manuscript:** *Intrinsic reconstruction from nonreduced failure schemes*  
**Author:** Qian Qi  
**Reviewed revision branch:** `revision/a2-v141-functorial-spectral-reconstruction-2026-09-23`  
**Exact reviewed branch head:** `bf0d9be9e2624058d24a57c48b19ec4c38105c1f`  
**Immediate substantive manuscript predecessor:** `revision/a2-v140-intrinsic-pencil-moduli-2026-09-23`, reviewed at `6bac73f9ebcaadcfa135e4960de19c93323bbfd7`  
**Immediate controlling referee report:** `reviews/a2-v140-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `17e039fe55fc0d060b443d486421d937f637439a`  
**Review standard:** external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested, AI-assisted independent referee-style report, not a journal-commissioned editorial decision.

I reviewed the v141 branch head, the v141 restoration workflow, the materialized v138–v140 source trees, the v140 principal article and its key new Sections 20–21, the v140 response to the v137 report, the v140 literature audit, and the immediate v140 referee report. I also checked whether the v141 branch contains a new native manuscript object, issue matrix, response, or mathematical source tree corresponding to revision 141.

## Recommendation

**Reject in the present form at a general top-four mathematics journal, and do not treat v141 as a completed mathematical revision of v140.**

The reason is unusually concrete. Revision 141, as currently committed, is primarily a **source-restoration/materialization revision**, not a new mathematical manuscript revision. The branch head is explicitly

> `A2 v141: materialize authentic v138-v140 native manuscript trees [skip ci]`

and the branch does not contain a native
`papers/A2-v17-boundary-information-coarsening/article/v141/`
manuscript tree. Attempts to read the expected v141 `README.md`, `ISSUE_MATRIX.json`, `complete.tex`, and principal source parts return 404. The v141 workflow itself is named **“A2 v141 native source restoration”** and its job is to restore v138, reconstruct v139 and v140, then commit those predecessor trees.

This does repair an important reviewability defect identified in the v140 report: the previously transport-only v140 source is now materially present on the v141 branch. That is useful and should be preserved. But it does **not** constitute a response to the substantive B140.2–B140.4 objections, and it does not create a new mathematical object that can fairly be called “A2 revision 141” in the ordinary referee sense.

The mathematics available on the branch remains essentially the v140 mathematics. My substantive assessment therefore remains: the core reconstruction program contains several strong and technically interesting results, but the closest historical comparison, the exact novelty audit of the all-dimensional contraction theorem, and the general top-four significance case remain unresolved.

## 1. What v141 actually fixes

### 1.1 The source-state blocker B140.1 is materially improved

The v140 report objected that the reviewed branch did not itself contain the native v140 manuscript tree and instead depended on a failed Actions reconstruction chain. Revision 141 directly addresses that operational weakness.

The workflow `.github/workflows/a2-v141-native-bootstrap.yml` pins:

- the v138 referee artifact and its archive SHA-256;
- the source commit and controlling review commit;
- the authenticated v140 transport;
- the exact decoded v140 source-package SHA-256;
- the predecessor provenance manifest;
- the restoration receipt.

The final v141 head then materializes the authentic v138, v139, and v140 manuscript trees. I was able to read the v140 native article directly from the v141 branch, including `complete.tex`, the introduction, the finite-neighbourhood section, the spectral-specialization section, the response file, and the literature audit.

This is a real improvement. A subsequent referee should not have to reverse-engineer the v140 transport chain merely to inspect the manuscript.

### 1.2 The materialized v140 article is coherent with the prior reviewed mathematics

The v140 `complete.tex` includes the expected principal sequence:

- uniform support;
- relations;
- Fitting core;
- intrinsic web reconstruction;
- structural coefficient reconstruction;
- natural pencils;
- finite neighbourhoods;
- spectral specialization;
- polarization/moduli/classical comparison;
- the technical appendices.

The introduction accurately announces the v139 sharp finite-order result and the v140 spectral specialization. I do not see evidence that the materialization process silently replaced the advertised v140 mathematical content with a different manuscript.

That said, provenance fidelity is not the same thing as a new theorem.

## 2. New blocker B141.1: there is no native v141 manuscript

This is the first issue that must be corrected before another serious referee round.

The branch is named
`revision/a2-v141-functorial-spectral-reconstruction-2026-09-23`,
but there is no corresponding `article/v141` tree. In particular, there is no:

1. v141 principal `geometry.tex/pdf`;
2. v141 complete source;
3. v141 supplement;
4. v141 issue matrix;
5. v141 response to the v140 referee report;
6. v141 literature audit;
7. v141 build receipt tied to the actual v141 mathematical source;
8. v141 theorem-level changelog.

The branch head is therefore best understood as a **reproducibility repair for v140**.

For a top-tier revision process, the version identifier must denote a reviewable mathematical state. The current arrangement blurs three different things:

- transport/source restoration;
- manuscript revision;
- response-to-referee closure.

Those should not be conflated.

**Required action:** create a genuine v141 native manuscript tree with a source-bound build receipt and an explicit response to `review/a2-v140-independent-harsh-top4-2026-09-23`. If the authors intend no mathematical change beyond source restoration, then the branch should not be presented as having closed the v140 report.

## 3. B140.2 remains open: Ballico 1993 is still not compared at theorem level

The v140 literature audit states plainly that the full text of

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* 163 (1993), 5–13,

was not obtained and that the six requested comparison axes remain unverified:

1. parameter space;
2. reduced versus scheme-theoretic failure locus;
3. varied multiplication/higher-order map;
4. nilpotent, infinitesimal, colon, or normal-cone structure;
5. relative/base-change statements;
6. inverse/reconstruction statements.

Nothing in v141 changes this. The branch materializes the existing v140 audit; it does not supply the missing theorem-level comparison.

This remains important because the manuscript's conceptual vocabulary is exceptionally close to that historical title. A top-four novelty assessment cannot stop at “we do not claim exhaustive priority.” The relevant burden here is narrower and more reasonable: the closest already-identified predecessor should be read and compared precisely.

I do **not** infer anticipation. I also do **not** certify nonanticipation.

**Required action:** obtain the full 1993 article through a lawful library/interlibrary route and write a theorem-by-theorem comparison along the six axes above, with exact theorem numbers and hypotheses.

## 4. B140.3 remains open: the all-dimensional contraction theorem still lacks an expert-level novelty map

One of the manuscript's broadest and potentially most significant claims is the all-dimensional contraction/kernel theorem for the specific equivariant map built from

[
j_n:det(V)otimes mathrm{Sym}^n(V)	o igwedge^nmathrm{Sym}^2(V)
]

and contraction by a quadratic form, including singular-rank behavior and the even-dimensional nondegenerate exception.

The paper does useful work distinguishing this from nearby classical material:

- harmonic decomposition;
- transvectants;
- apolar differential operators;
- exterior contraction;
- skew-flattening support;
- Jacobian/polarization embeddings.

But the manuscript itself still records that an exhaustive map-specific priority audit is not complete. Revision 141 contains no new mathematical literature comparison on this point.

For a specialized journal, a complete proof plus a bounded literature discussion may be enough. For a general top-four paper, if this theorem is part of the claimed source of generality and significance, the authors must explain precisely where it sits relative to the classical representation-theoretic literature.

**Required action:** provide a map-by-map comparison showing whether equivalent kernel formulas appear under different normalizations or representation-theoretic packaging. In particular, identify the exact domain, codomain, group action, rank strata, irreducible summands, and kernel dimensions in each compared source.

## 5. B140.4 remains open: the significance case is improved but not yet top-four level

The strongest materialized v140 additions remain mathematically worthwhile:

- the natural all-pencil multiplication-failure reconstruction;
- the sharp finite neighbourhood order
  (d=n^2+2n-4);
- the closed parameter immersion;
- recovery of the spectral torsion sheaf;
- a flat family with fixed full discriminant and fixed reduced rank loci but changing spectral partition ((3,1)	o(2,2));
- the reciprocal conic-to-line specialization.

I continue to regard these as genuine progress relative to the earlier A2 states.

But the top-four significance issue identified in the v140 report is not closed by simply materializing those same results.

### 5.1 The spectral theorem is mainly an interpretation of the internal invariant in classical pencil language

The finite neighbourhood recovers the pencil; classical pencil theory recovers the elementary divisors/spectral module. The unpaired-sheaf congruence argument is elegant, but the overall theorem still largely says what the new internal invariant remembers.

That is a good theorem. It is not yet obviously a field-level theorem.

### 5.2 The rank-preserving specialization is exact but remains an explicit model family

The ((3,1)) versus ((2,2)) transition is clean, and the flatness argument for the truncated failure neighbourhoods is not vacuous. The reciprocal curve changing from a conic to a line is independently visible.

However, this is still one carefully engineered one-parameter family. The manuscript does not yet classify the possible spectral specializations under fixed discriminant and reduced rank data, nor characterize the corresponding moduli strata.

### 5.3 The sharp order is intrinsic but presently bespoke

The exact order (n^2+2n-4) is mathematically precise. But its significance is still internal to the failure-scheme construction unless the authors connect it to a standard infinitesimal/moduli invariant or prove an external theorem where that order is forced by pre-existing geometry.

### 5.4 What would materially change the assessment

Any one of the following, if proved at sufficient strength, could change the significance assessment:

- a classification of fixed-discriminant/fixed-reduced-rank pencil strata in which the failure neighbourhood gives a canonical refinement or normalization;
- a theorem identifying the first relation module with a standard syzygetic, deformation-theoretic, or moduli-theoretic object and deriving a new consequence about that standard object;
- a nontrivial theorem on fibres or monodromy of a classical web–K3–Reye/Enriques map, with the failure scheme resolving a previously existing ambiguity;
- a general specialization theorem characterizing exactly which Segre partitions can occur in flat families with fixed determinant and reduced rank loci, with the failure neighbourhood providing the complete invariant;
- a genuinely unexpected application of the all-dimensional contraction theorem outside the internal reconstruction formalism.

Without such an external theorem, I would still regard the paper as a technically ambitious specialized contribution rather than a clear general-top-four paper.

## 6. Proof-level comments on the materialized v140 mathematics

I do not find a new fatal proof error in the two v140 sections most relevant to the latest changes.

### 6.1 The finite-neighbourhood convention appears internally consistent

The convention
[
Z_R^{[k]}=V(mathfrak b^{k+1})
]
means a degree-(d) homogeneous relation first becomes visible at order (k=d). The previous referee's off-by-one check remains valid after materialization.

The paper should continue to call this **uniform sharpness**, not a claim that every pair of pencils has pairwise minimal distinguishing order exactly (d).

### 6.2 The torsion-sheaf-to-congruence argument is plausible as written

The use of a polynomial square root of the commuting invertible operator over (mathbf C) is the key step. The argument needs the usual finite-dimensional functional calculus modulo the minimal polynomial, and the manuscript should keep that hypothesis and field dependence explicit. It should not be casually generalized to arbitrary fields.

### 6.3 The reduced/full determinantal distinction must remain explicit

The specialization has constant **reduced** rank loci, but not constant full determinantal/Fitting ideals. The manuscript itself correctly notes the local gcd change from (z) to (z^2).

This qualifier is mathematically essential and should appear every time the example is summarized.

### 6.4 The flatness theorem is about finite neighbourhoods, not the unrestricted failure schemes

The paper correctly limits the flatness conclusion. Future versions should resist wording that suggests the full (widehat D_{R_t}) family is proved flat.

## 7. Presentation and architecture

The manuscript is now extremely large relative to the conceptual message. The complete compilation is over one hundred pages in the prior review package, with a principal article plus a long technical supplement and a large audit/evidence layer.

For a top-four paper, length itself is not disqualifying. But the proof architecture must make the hierarchy unmistakable.

I recommend that the genuine v141 manuscript have a one-page theorem dependency map distinguishing:

- foundational algebra/Fitting construction;
- intrinsic deepest-stratum and normal-cone recovery;
- web recombination;
- all-dimensional contraction/support theorem;
- natural all-pencil theorem;
- finite-order theorem;
- spectral application;
- boundary/primary supplementary results.

This would help a referee determine which claims depend on the heaviest representation theory and which are logically independent.

The response history, provenance receipts, machine checks, and literature access logs should remain available in the repository but should not substitute for a clean mathematical narrative in the submitted article.

## 8. Required conditions before the next referee round

I would regard the following as minimum conditions for a meaningful new review:

1. **Materialize an actual v141 manuscript tree.** The branch version must correspond to a native mathematical source, not only restored predecessors.
2. **Write a direct response to the v140 report.** Each of B140.2, B140.3, and B140.4 should be marked closed or open with evidence.
3. **Close the Ballico 1993 comparison.** Exact theorem-level six-axis comparison.
4. **Complete the map-specific novelty audit for the contraction theorem.**
5. **Add one external significance theorem or a substantially stronger moduli/classification consequence.**
6. **Run and record a source-bound green build on the exact v141 manuscript commit.**
7. **Preserve the current good qualifiers.** In particular: reduced rank loci, finite-neighbourhood flatness only, no formal-proof claim from symbolic scripts, no exhaustive-priority claim without evidence.
8. **Provide a compact dependency/novelty map** separating classical input, manuscript-specific theorem, and computational regression evidence.

## 9. Final assessment

The project has advanced far beyond an early speculative draft. The materialized v140 manuscript contains serious mathematics: intrinsic reconstruction from nonreduced Fitting data, a natural all-pencil family, a sharp finite infinitesimal order, spectral recovery, and explicit degenerations invisible to reduced rank data.

But **revision 141, as currently committed, is not a mathematical revision that closes the v140 referee report**. It is chiefly a restoration and reproducibility repair that makes the v140 source genuinely inspectable. That is useful, but it does not resolve the remaining historical-novelty and significance objections.

Accordingly, my recommendation remains **reject in the present form for a general top-four mathematics journal**, with encouragement to resubmit for a genuinely fresh round only after the substantive blockers above are closed.
