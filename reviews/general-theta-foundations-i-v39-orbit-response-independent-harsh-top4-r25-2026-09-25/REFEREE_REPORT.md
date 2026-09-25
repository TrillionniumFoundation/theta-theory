# Independent Referee Report — General Theta Foundations I, Revision 39

**Manuscript:** *General Theta Foundations I: Minimal Orbits and the Width of Numerical Experiments*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v39-referee-ready-2026-09-25`  
**Reviewed head:** `28890c62dd69f217bf2f1c205ff9542eb537c2ef`  
**Native mathematical source recorded by the manuscript:** `cb9c9edc0d20ea32b4702c668dcddae6b791f0ce`  
**Controlling manuscript response:** response to r23 at the reviewed head  
**Existing first review of this head:** r24, commit `24bd1abe003ef13df4eb223a8b2010010de9f82b`  
**This independent review branch:** `review/general-theta-foundations-i-v39-orbit-response-independent-harsh-top4-r25-2026-09-25`  
**Date:** 25 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is an independent second review of the same Revision-39 manuscript head. A fresh remote branch survey found no Revision 40 or later referee-ready branch at the time of review. I therefore did not pretend that a new manuscript had arrived. I re-read the current article, its proof/status ledgers, the controlling repository dependency DAG, and the closest external sources that materially affect the novelty and source-audit assessment.

Revision 39 is a serious specialist contribution. In the nonuniform, finite-horizon, clocked, atomic stochastic-row model actually defined, I did not find a short fatal counterexample to the central mathematical chain. The uniform orbit-stratum estimate, the inherited entropy occupation argument, the minimum-orbit synthesis, the reducible paid-branch construction, and the numerical-versus-cutpoint separation are all coherent at the level of a referee audit.

The negative recommendation is not an allegation that the headline theorem is false. It follows from the gap between the theorem actually proved and the editorial claim suggested by the program branding.

The decisive objections are these.

1. **The headline “representation law” is not intrinsic to the represented numerical experiment.** The lower theorem assumes a full spectral gap on `L^2_0(G)` for a chosen presenting group `G`. The same representation and the same response laws can be presented by `G x T`, with a compact factor `T` acting trivially. The orbits, widths, and invariant `s(U)` are unchanged, while the full regular-representation gap can disappear completely. The theorem should be formulated on the effective image group or in terms of the actual Koopman representation needed by the proof.
2. **The manuscript contains a concrete primary-source discrepancy in its current quantum-automata comparison.** It cites `arXiv:2604.07058v2`, attributes a `k+1`-state GFA-to-PFA conversion to Proposition 3.1, and states a `q^2+1` universal PFA bound. During this review, the primary arXiv record accessible at `arXiv:2604.07058` listed only v1; there Proposition 3.1 is the `n^2` quantum-to-GFA linearization, Theorem 3.2 gives `2k+6` PFA states, and Corollary 3.3 gives `2n^2+6`. Third-party metadata did report a differently titled v2, but the primary source needed to verify the manuscript's theorem-level claim was not available. A top-four submission cannot use an inaccessible or mismatched version as settled evidence.
3. **The invariant `s(U)` is a definition rather than a representation-theoretic classification.** The manuscript proves that this invariant controls the exponent under strong expansion and calibration hypotheses. It does not classify `s(U)` for general irreducible compact-group representations, give a highest-weight formula, or identify minimizing stabilizers beyond selected families.
4. **The genuinely difficult dynamic converse is substantially inherited from Revision 38.** The new material is an effective and useful synthesis of compactness, orbit geometry, quadratic support approximation, and paid direct sums. It is not a second four-journal-scale breakthrough beyond the already specialist-level entropy occupation theorem.
5. **The resource model remains highly permissive and nonuniform.** Horizon, epoch, arbitrary real row tables, table construction, lookup, arithmetic, and exact atomic sampling are free. The machine and decoder can be redesigned for every `N`. This is positive-realization width, not uniform computational space, total branching-program size, autonomous memory, or finite-random-bit complexity.
6. **The reducible theorem is an exponent theorem under restrictive activation and small-signal conditions, not an exact direct-sum classification.** It does not determine finite feasible profiles, leading constants, vanishing-signal behavior, or multi-query product tasks.
7. **The arithmetic six-gate application remains externally source-bound.** The local normalization appendix is careful, but the exact original LPS theorem/page used for `(LPS5)` remains unverified from the original full text. The enormous resulting finite constant further confirms that this is a certificate, not a sharp finite complexity result.
8. **The repository-wide Foundations pipeline is unchanged at every difficult analytic gate.** The new orbit theorem does not discharge any of the branchwise Fourier/LLT, stopped-LDP, global-kernel, nonlinear-semigroup, graph-core, filtering, optional-projection, or typed-contraction obligations in the controlling A/B/C/D chains.

The manuscript should be evaluated as a potentially strong specialist article on hidden stochastic realization of expanding group actions. It should not be presented as approaching the level or scope of the four leading general mathematics journals.

---

## 1. Scope and independence of this report

The latest remote referee-ready branch was Revision 39. No Revision 40 branch was visible. This report is therefore an independent second pass on the exact same reviewed head rather than a nominal review of nonexistent new mathematics.

I examined:

- `papers/GTF-I-v39-orbit-response/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `orbit-strata.tex`;
- `orbit-entropy.tex`;
- `orbit-synthesis.tex`;
- `reducible-width.tex`;
- `matrix-families.tex`;
- `numerical-semantics.tex`;
- `comparison.tex`;
- the retained conjugation, projective, effective-gate, and arithmetic-normalization appendices;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `GAP_CERTIFICATE.json`;
- the reviewed publication and native-source commits;
- the existing r24 report, only as a record of issues already raised;
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also checked the current primary arXiv records for the 2026 quantum-automata papers named in the manuscript, and consulted primary or author-hosted sources on homogeneous-space metric entropy, orbitopes, positive-semidefinite rank, and compact-group spectral gaps where available.

This review branch starts directly from the manuscript head. It does not contain, amend, or overwrite r24. The only intended change is this report.

The 22-page article is sufficiently self-contained for its new arguments. The 514-page mathematical archive and 1067-page development archive are provenance records, not additional proof or significance. Hashes, clean builds, page comparisons, and negative controls are useful engineering but carry no editorial mathematical weight.

---

## 2. What the manuscript actually proves

### 2.1 Irreducible case

For a fixed nontrivial real irreducible orthogonal representation `U` of a compact connected Lie group, define

```text
s(U) = min_{||u||=1} dim(G u).
```

Under a finite command law with the manuscript's full group norm gap, fixed positive signal, and fixed error below the calibration threshold, the paper proves

```text
W_(N,epsilon) = Theta(N^(s(U)/2)).
```

The lower bound permits arbitrary hidden states, arbitrary time-dependent stochastic rows, and a different machine for every horizon. The upper construction uses one minimum-dimensional orbit, common command rows, and an `N`-dependent decoder.

This is a clean conditional exponent theorem.

### 2.2 Reducible case

For an orthogonal direct sum into invariant and irreducible constituents, the paper defines

```text
sigma(U) = max_i s(U_i)
```

over nontrivial irreducible constituents. With spanning seeds, a positive seed-activation constant, sufficiently small fixed signal, and fixed error below a seed-dependent threshold, it proves

```text
W_(N,epsilon) = Theta(N^(sigma(U)/2)).
```

The lower bound projects the whole-machine terminal correlation into one constituent. The upper construction randomizes over constituents, charges the branch identity in disjoint labels, and amplifies the conditional represented vector by the reciprocal branch probability.

This maximum law is correct in the declared one-query marginal model. It should not be confused with an exact profile sum, a tensor-product output task, or a free branch selector.

### 2.3 Static-versus-compatible separation

With symmetric basis seeds, each selected cut separately has positive minimum `D+1`, while the compatible width can grow polynomially with `N`. The manuscript correctly embeds a selected-cut factorization into a full finite machine by allowing unrestricted registers elsewhere.

This is an operational separate-minimum statement, not merely an amputated matrix factorization.

### 2.4 Numerical-versus-cutpoint semantics

The `D+1`-label simplex simulator attenuates the target vector by `(2D)^(-N-1)`. It preserves the sign of every selected coordinate relative to the cutpoint `1/2`, including ties, while losing fixed numerical amplitude.

The construction correctly demonstrates that strict-cutpoint language equivalence and fixed-accuracy numerical realization are different resource questions in the same reset-command-query syntax.

---

## 3. Technical audit of the uniform orbit theorem

### 3.1 The infinitesimal rank argument is sound

For a unit vector `u`, the derivative

```text
A_u : Lie(G) -> V,
A_u(X) = dU(X)u
```

has rank `dim(G u)`. If `s=s(U)`, then the `s`th singular value of `A_u` is positive for every `u`. It varies continuously in `u`; compactness of the unit sphere supplies a uniform positive minimum.

This is the correct starting point for a uniform all-strata estimate.

### 3.2 The local co-Lipschitz chart argument appears valid

At each `(g_0,u_0)`, the proof chooses `s` group-coordinate directions and a projection to `R^s` with invertible derivative. Uniform derivative control on a small product chart yields a lower Lipschitz estimate in those `s` coordinates. For a fixed value of the other coordinates, the preimage of an ambient radius-`r` ball has `s`-dimensional measure `O(r^s)`. Bounded Haar density and integration over the remaining coordinates preserve that order.

A finite cover of `G x S(V)` makes the constant uniform in `u` and the target center `v`.

I see no need for constant stabilizer type in this step. The proof handles singular strata by compactness rather than by a regular-orbit density formula.

### 3.3 The local lower power at a minimum orbit is also correct

A minimum-dimensional orbit is a smooth compact homogeneous submanifold. The pushforward of Haar probability is its invariant volume, and local volume in an ambient ball is comparable to `r^s`. Thus no larger exponent can hold uniformly over all directions.

This establishes sharpness of the geometric small-ball exponent. It does not by itself establish the dynamic width lower bound; the entropy occupation theorem remains essential.

### 3.4 The theorem is geometric, not a classification of orbit types

The chart proof shows that once the minimum orbit dimension is known, it is the uniform concentration exponent. It does not determine the minimum orbit dimension from highest-weight data or classify the corresponding stabilizers.

That distinction is central to the editorial assessment.

---

## 4. Technical audit of the minimum-orbit upper realization

### 4.1 The inradius argument is coherent

For an irreducible real orthogonal representation, Haar averaging of one orbit gives mean zero and covariance `I/d`. For a unit functional with orbit maximum `M`, the identity

```text
E[(M-f)(f+1)] = M - 1/d >= 0
```

implies `M>=1/d`. Hence the convex hull of a unit orbit contains the ball of radius `1/d`.

The real, complex, and quaternionic commutant types do not invalidate this covariance statement: the covariance is self-adjoint, and the self-adjoint part of the irreducible commutant is scalar.

### 4.2 Quadratic support loss on a compact orbit is standard and correctly used

At a support maximizer, the first tangential derivative vanishes. A uniform second-derivative bound on the compact orbit gives support loss `O(h^2)` for an intrinsic `h`-net. Combined with the inradius, this yields

```text
(1-c h^2) conv(O) subset conv(V_h).
```

Taking `h` of order `N^(-1/2)` gives `O(N^(s/2))` labels.

The covering exponent and quadratic support estimate are classical geometric facts. The nontrivial realization step is to use the contracted hull at every layer with legal common stochastic rows.

### 4.3 The stochastic update construction is exact in the stated model

For each label `v_i` and command `a`, the point

```text
eta U_a v_i
```

lies in the finite net hull. Any convex decomposition gives a stochastic row. With represented scale `a_t=eta^(-t)/4`, the expectation evolves by exactly `U_a`. The terminal decoder remains in `[-1,1]` because `eta^N` stays bounded below.

The construction is correct as an existence theorem with free row tables and exact atomic sampling.

### 4.4 The computational content is minimal

The proof does not provide:

- an efficient algorithm to find the convex decompositions;
- a succinct description of the row tables;
- bit-complexity bounds;
- an exact finite-coin compiler for arbitrary algebraic or irrational weights;
- total branching-program size;
- a uniform machine serving all horizons.

Carathéodory bounds the number of successors in one row. It does not bound the number of rows, table-generation cost, or advice length.

---

## 5. Technical audit of the reducible maximum law

### 5.1 The constituent lower bound is legitimate

Fix a constituent and a seed with nonzero projection to it. The terminal coordinate errors combine into a Euclidean error at most `2 sqrt(D) epsilon`. Correlation with the normalized constituent orbit gives a positive terminal conditional-centroid amplitude whenever

```text
rho a_i / sqrt(D) - 2 epsilon > 0.
```

The same whole-machine hidden state is used in the conditional expectation. No free access to the constituent label is assumed.

Applying the irreducible occupation theorem gives the lower exponent of each activated constituent, and hence the maximum.

### 5.2 The paid branch upper construction is coherent

Choosing branch `i` with probability `d_i/D`, amplifying the branch's conditional target by the reciprocal weight, and taking the disjoint union of branch state sets yields the exact marginal numerical response. The signal restriction ensures every amplified initialization lies within the applicable inradius.

The branch identifier is genuinely charged. The construction does not use an unrecorded selector.

### 5.3 The activation threshold is decomposition-dependent in isotypic components

The exponent is independent of the orthogonal decomposition into equivalent irreducibles, because all equivalent summands have the same `s_i`. The activation constant

```text
a_* = min_i max_x ||pi_i x||
```

need not be comparably intrinsic. In an isotypic component with multiplicity, rotating the irreducible decomposition can change the individual projection sizes and therefore the stated error threshold.

This does not make the theorem false: one may fix a decomposition and obtain a positive constant from spanning seeds. It does mean that the reducible calibration statement is not yet in a canonical representation-theoretic form.

A better theorem would formulate activation at the isotypic level or optimize over decompositions.

### 5.4 The maximum law is only an order statement

The theorem does not identify:

- exact finite widths;
- complete feasible profiles;
- leading constants;
- constituent interactions at finite `N`;
- multiple simultaneous terminal queries;
- vanishing activation or vanishing signal;
- arbitrary nonspanning seed sets.

The phrase “classification” should be qualified accordingly.

---

## 6. A new and concrete source-audit defect

The manuscript's `references.tex`, `numerical-semantics.tex`, response, and `LITERATURE_AUDIT.md` rely on a claimed revised version of Chen--Wu, `arXiv:2604.07058v2`.

The manuscript states, in substance, that:

- the revised paper has a GFA-to-PFA conversion with `k+1` states;
- its Proposition 3.1 is that conversion;
- its Theorem 3.2 gives `q^2+1` states for strict-cutpoint simulation of a `q`-state general one-way QFA;
- the version was inspected as a late-August revision.

During this review, the primary arXiv record accessible for `2604.07058` listed only **v1**, dated 8 April 2026. In that primary text:

- Proposition 3.1 is the `n^2`-dimensional 1gQFA-to-GFA linearization;
- Theorem 3.2 converts a `k`-state GFA to a PFA with at most `2k+6` states;
- Corollary 3.3 gives a PFA upper bound `2n^2+6`;
- the matching lower bound is `n^2-1`.

Third-party indexing did display a differently titled item labelled v2 with a claimed `n^2+1` result. That conflict makes the situation worse, not better, for a formal referee audit. The manuscript's theorem-number-level citation is not independently checkable from the primary source currently exposed.

This is not a mathematical counterexample to Revision 39. It is a serious source-integrity problem.

Before any specialist submission, the authors must do one of the following:

1. cite the primary version that is actually publicly accessible and state its correct theorem numbers and constants;
2. provide a stable public primary link to the claimed v2 and verify its submission history;
3. include an exact bibliographic snapshot or permitted local reference record sufficient for a referee to identify the version;
4. remove the unverifiable `q^2+1` and `k+1` claims and compare only the robust `Theta(q^2)` strict-cutpoint law.

A top-four paper cannot build an originality boundary on a version mismatch between its own audit and the current primary record.

---

## 7. The full-group gap is not intrinsic

### 7.1 A trivial extension changes the hypothesis but not the experiment

Suppose a numerical experiment is generated by an effective compact group `H` acting through `U`. Present the same representation as an action of

```text
G = H x T
```

where the compact connected factor `T` acts trivially. Lift every command with identity `T` coordinate.

Then:

- every command matrix on `V` is unchanged;
- every orbit is unchanged;
- every response probability is unchanged;
- every realization width is unchanged;
- `s(U)` is unchanged.

But convolution on `L^2_0(G)` has norm one on nonconstant functions of the unused `T` coordinate. The manuscript's full-group gap fails.

Therefore the property in the headline theorem is not a property of the represented experiment.

### 7.2 The proof needs an action gap, not arbitrary regular-representation expansion

The entropy production lemma uses a gap for the Koopman action on functions on `V`, away from the invariant projection relevant to that action. A full `L^2_0(G)` gap is a sufficient way to obtain it by transference. It is much stronger than necessary.

The theorem should be restated using one of the following intrinsic objects:

- the effective compact image group `H=closure(U(G))` and the pushforward command law;
- the quotient `G/ker U` when this is the appropriate effective group;
- the actual operator norm of the command average on the noninvariant part of `L^2(V)`;
- constituent-specific action gaps in the reducible theorem.

Only after this reformulation can the exponent formula reasonably be called a representation-level law.

### 7.3 Full expansion also excludes broad classes by assumption

Compact groups with positive-dimensional abelian quotients do not admit the required finite-support regular-representation gap in the way used here. The theorem therefore concerns an expanding semisimple-type class, not arbitrary compact connected representations.

The circle examples in the historical chain are outside the hypothesis. Their arithmetic width behavior is not classified by the new theorem.

---

## 8. `s(U)` is not yet a usable general classification

### 8.1 Selected families are correctly computed

The manuscript correctly identifies the least orbit dimensions for:

- real symmetric traceless matrices under `SO(q)`;
- complex Hermitian traceless matrices under `SU(q)`;
- quaternionic self-adjoint traceless matrices under `Sp(q)`;
- fixed-degree real spherical harmonics of `SO(3)`.

The resulting exponents follow from the general theorem.

### 8.2 General irreducible representations remain untreated

For a general compact simple group and a highest-weight representation, the paper does not provide:

- a formula for the maximum stabilizer dimension;
- a classification of minimum-dimensional projective or spherical orbits;
- a table for fundamental, minuscule, quasi-minuscule, spin, or exceptional representations;
- a criterion identifying the minimizing orbit from weight data;
- a tractable algorithm in a succinct representation model.

The real-algebraic statement using all minors of the infinitesimal action matrix is formally correct for fully expanded algebraic input. It is not a representation-theoretic solution of the orbit-type problem.

### 8.3 The minimum orbit can be far from the generic orbit

The harmonic and matrix examples already show that generic orbit dimension is not the correct invariant. This makes the minimum-orbit problem mathematically substantive. It also makes the absence of a structural classification more consequential.

A four-journal-level “classification” claim would need to resolve, not merely name, this invariant across a broad representation class.

---

## 9. Numerical simulation versus strict cutpoints

### 9.1 The same-task attenuating simulator is a useful clarification

The manuscript no longer relies only on semantic prose. It constructs a legal positive machine of constant command width whose centered response is

```text
lambda^(N+1) <e_j,U_w x>.
```

This preserves the strict sign at cutpoint `1/2` but loses any fixed positive numerical calibration.

The example directly demonstrates the distinction.

### 9.2 The distinction limits the quantum claim

The growing classical width is a lower bound for fixed numerical accuracy. It is not a lower bound for:

- strict-cutpoint language recognition;
- bounded-error regular-language recognition;
- every probabilistic simulation notion used in quantum automata;
- total automaton size including syntax parsing;
- uniform classical space.

The fixed quantum register comparison is mathematically clean but narrow.

### 9.3 Static rank methods cannot prove the horizon growth

The centered prefix-suffix response matrix has ordinary rank at most `D` at every split. Static sign rank, ordinary rank, and operator-space dimension alone do not force a growing horizon-dependent width.

The manuscript is correct that the growth comes from dynamic positive compatibility, not from one static linear dimension.

---

## 10. The six-gate effective example

### 10.1 The local normalization appendix is improved

The paper now explicitly states the imported `(LPS5)` inequality, enumerates the parity representatives, identifies the displayed adjoint rotations, handles inverse pairs, divides by six, squares the norm, and explains the transfer from one copy of each `SO(3)` irreducible on the sphere to the regular representation with multiplicities.

Those local steps are appropriate and appear coherent.

### 10.2 The imported source remains incompletely verified

The manuscript itself records that:

- the original LPS full text was not obtained;
- the original theorem number was not verified;
- the exact imported line is taken through a later numbered restatement and a coauthor account;
- finite harmonic tests do not certify the infinite-dimensional gap.

This transparency is commendable. It also means that the numerical example remains an external conditional corollary rather than independently audited primary mathematics.

### 10.3 The constants are certificates, not sharp complexity

At zero error the explicit lower bound exceeds the separate four-state minimum only at an enormous horizon. The upper constant is also a proof constant. The result is effective in the logical sense, not a determination of useful finite widths or leading asymptotics.

The manuscript should resist using the word “sharp” near this example except for the linear exponent.

---

## 11. Resource-model assessment

The charged quantity is the maximum number of available labels at a cut. The model gives the machine substantial free resources:

- the entire horizon;
- the external epoch;
- redesign for every horizon;
- arbitrary cut-dependent state sets in the lower class;
- exact real stochastic kernels;
- unbounded read-only transition and decoder tables;
- table construction and lookup;
- arithmetic on row entries;
- one selected terminal query rather than a joint output family.

This model is legitimate for positive realization. It is not conventional computational space.

The following distinctions must remain explicit:

```text
labels != label bits != total table size
       != fair-bit workspace != autonomous states
       != uniform algorithmic space.
```

The asymptotic label theorem does imply logarithmic label-bit growth for polynomial width. It does not imply that a uniform implementation uses that much space once its nonuniform tables and exact sampling are priced.

---

## 12. Pipeline assessment

The local Revision-39 proof chain is coherent:

```text
uniform infinitesimal orbit rank
    -> all-strata orbital concentration
    -> entropy occupation lower exponent

minimum-orbit covariance
    -> quadratic support approximation
    -> exact common-row synthesis

constituent terminal correlation
    + paid stochastic branch
    -> reducible maximum exponent

positive attenuation embedding
    -> cutpoint/numerical separation.
```

This chain is not part of either controlling analytic DAG:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

or

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The unresolved gates still include:

- common induced branch bundles and raw multidimensional local limits;
- stopped large deviations and exact entropy representations;
- one global kernel and unsmoothed renewal resolvents;
- nonlinear Nisio semigroups and graph-core approximation;
- exact belief kernels and QMD/LAN;
- strict duality, operator-core compression, and changing-filtration optional projection;
- labelled latent-phase contraction.

Revision 39 supplies no theorem satisfying those obligations.

Its own status records correctly leave false or unresolved:

- historical A2 replacement;
- B4 aggregate closure;
- C2 aggregate closure;
- the eleven-paper aggregate;
- fully adaptive collision scheduling;
- noisy-tag composition;
- all-irrational classification;
- numerical general-`q` gaps;
- optimized constants;
- original LPS theorem-number verification;
- independent external review.

The local statement `sharp_general_representation_width=true` is meaningful only inside its narrow scope string. It cannot be converted into repository-wide foundational closure.

---

## 13. Minimum changes for a credible specialist submission

These are not a route to top-four acceptance. They are the minimum for a fair specialist evaluation.

### 13.1 Reformulate the gap intrinsically

State the main theorem on the effective image group or directly with the action/Koopman gap used by the entropy proof. Prove invariance under replacing the presenting group by a compact extension with the same effective action.

### 13.2 Repair the Chen--Wu citation immediately

Reconcile the manuscript's claimed `v2`, theorem numbering, and `q^2+1` constant with the current primary arXiv record. Do not cite third-party metadata as a substitute for a stable primary version.

### 13.3 Retitle the paper

Remove “General Theta Foundations I.” A subject-specific title could be:

- *Minimum-Orbit Exponents for Hidden Stochastic Transducers*;
- *Numerical Realization Width of Expanding Compact-Group Actions*;
- *Orbit Geometry and Positive Memory under Group Expansion*.

### 13.4 Replace “classification” by a scoped theorem

Say explicitly that the paper gives a conditional exponent formula in terms of `s(U)`. Reserve “classification” for a result that also computes or structurally identifies `s(U)` over a broad representation class.

### 13.5 Add a representation-theoretic treatment of `s(U)`

At minimum provide a serious table and proofs for classical fundamental representations, adjoint representations, spin representations, and selected exceptional examples. Explain the relation to maximal stabilizers and minimal projective orbits.

### 13.6 Canonicalize the reducible calibration

State the lower threshold at the isotypic level or optimize the activation constant over irreducible decompositions. The current constituent projection constant is adequate for existence but not intrinsic.

### 13.7 Keep all resource measures separate

Do not infer uniform space, finite-coin memory, table complexity, or total branching-program size from atomic label width.

### 13.8 Treat the LPS application as optional

The conditional general theorem should stand without the six-gate example. Keep the exact imported inequality and source limitation explicit until the original theorem is independently checked.

### 13.9 Remove pipeline sales language from the article

The A/B/C/D labels and cumulative archive sizes belong in repository metadata, not in the mathematical case for publication.

### 13.10 Obtain independent expert review

The entropy occupation mechanism should be reviewed by experts in information theory and stochastic realization; the orbit theorem by compact transformation-group experts; and the quantum-automata comparison by automata theorists using the exact publicly available versions.

---

## 14. Specific major and minor points

1. Replace the full `L^2_0(G)` assumption by an intrinsic effective-action formulation.
2. State explicitly that adding a trivially acting compact factor leaves the experiment unchanged but may destroy the present hypothesis.
3. Distinguish the effective image group from the abstract presenting group everywhere.
4. Do not call `s(U)` classified merely because it is semialgebraically decidable from fully expanded matrices.
5. Give a canonical treatment of isotypic multiplicities in the reducible theorem.
6. State the decomposition dependence of the displayed seed-activation constant.
7. Separate exact exponent order from finite width and leading constant.
8. State whether all constants in the upper machine depend continuously or only existentially on the representation.
9. Add primary references for metric entropy of compact homogeneous spaces.
10. Add a standard transformation-group reference for orbit-type stratification and slice/tubular-neighborhood theory.
11. Clarify that the chart proof produces a uniform exponent, not sharp uniform constants for every stratum.
12. Clarify that the minimum-orbit net is not a design and uses no moment matching.
13. State that a quadratic support loss follows from smoothness at support maxima, not from a new quantization theorem.
14. Do not identify sparse successor rows with succinct transition tables.
15. State explicitly that arbitrary algebraic commands need not yield rational convex-decomposition weights.
16. Keep `rho<=1/(8D)` separate from the stronger minimal-orbit/projective signal range.
17. Keep the seed-activation threshold visible whenever the reducible theorem is quoted.
18. State that the maximum law is for one selected marginal query.
19. Do not infer a product-output law from the paid branch construction.
20. Correct or remove the claimed `arXiv:2604.07058v2` theorem numbers until a primary version is accessible.
21. If a later primary version exists, record its exact submission date and title rather than a third-party snapshot.
22. Keep strict-cutpoint language equivalence separate from numerical probability preservation.
23. State that the sign simulator's exponentially shrinking margin is the entire reason it evades the numerical lower bound.
24. Do not advertise the quantum comparison as a bounded-error language lower bound.
25. Keep ordinary rank, nonnegative rank, PSD rank, and dynamic compatible width distinct.
26. Quote `(LPS5)` whenever the numerical gap is used.
27. Do not imply a numerical gap on half-integer `SU(2)` representations.
28. State that the effective crossover is a conservative proof artifact, not a practical threshold.
29. Include the final two-label cut consistently in finite-width statements.
30. Keep available labels distinct from labels of positive probability under one converse law.
31. State that the command sequence is externally supplied, not adaptively optimized.
32. Do not infer autonomous stopping-length recognition.
33. Do not use build receipts or archive length as evidence of proof or significance.
34. Remove internal pipeline labels from the article's conclusion.
35. Remove “Foundations” from a specialist submission title.

---

## 15. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | Principal proofs appear coherent; no short fatal counterexample found |
| Independent source integrity | Defective: current primary arXiv record does not verify the cited Chen--Wu version or theorem numbers |
| Advance over Revision 38 | Meaningful representation-level packaging and reducible extension |
| Originality boundary | Incomplete; orbit geometry is largely classical and `s(U)` is not structurally classified |
| Mathematical depth | Strong specialist level, below top-four general-journal level |
| Sharpness | Matching exponent under strong expansion and fixed calibration only |
| Intrinsic formulation | Inadequate: full regular-representation gap depends on redundant group presentation |
| Reducible result | Correct asymptotic maximum law under restrictive seeds, signal, and error |
| Resource model | Nonuniform atomic-row width with free advice, arithmetic, and exact sampling |
| Quantum comparison | Correct semantic distinction, narrow numerical task |
| External dependencies | Deep group expansion; LPS primary-source bridge remains incomplete |
| Pipeline impact | None on decisive A2/B4/C2/D1 analytic gates |
| Presentation | Technically improved; branding and classification rhetoric remain excessive |
| Reproducibility | Strong engineering, not proof or priority certification |
| Editorial recommendation | Reject at top-four level; reconsider only after intrinsic reformulation and specialist repositioning |

---

## 16. Final assessment

Revision 39 contains a coherent theorem of real interest. Under a strong expansion hypothesis and fixed numerical calibration, a minimum orbit determines the hidden-label exponent; a matching common-row construction exists; reducible actions obey a paid maximum law; and strict-cutpoint simulation is explicitly separated from fixed-accuracy numerical realization.

Those are genuine accomplishments.

They do not establish a general foundations theory.

The main hypothesis is not intrinsic to the represented experiment. The central invariant is named rather than broadly classified. Much of the difficult dynamic converse is inherited. The resource model is highly nonuniform. The quantum comparison concerns one narrow numerical objective. The effective arithmetic example remains source-bound. The manuscript's current quantum-automata audit contains a primary-version discrepancy. The repository's principal analytic pipeline is unchanged.

Put bluntly:

**Revision 39 proves a conditional exponent theorem for expanding numerical group experiments. It does not classify finite memory, positive realization, or quantum/classical simulation in any journal-wide foundational sense.**

My recommendation is firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A substantially retitled article, reformulated on the effective image/action gap, with the external citation discrepancy repaired and a serious representation-theoretic analysis of minimum orbits, could receive strong specialist consideration. That would be a new editorial submission rather than another internal revision marketed as approaching the four-journal threshold.
