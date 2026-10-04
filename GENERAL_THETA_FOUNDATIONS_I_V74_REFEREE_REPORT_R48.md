# Referee Report — General Theta Foundations I, Revision 74 (r48)

**Quantitative manuscript:** *Coupled Boundary Geometry and Reusable Measurement Descriptions*  
**Structural manuscript:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v74-coupled-boundary-geometry-2026-10-04`
- `revision/general-theta-foundations-i-v74-referee-ready-2026-10-04`

**Reviewed exact final head:** `8477a4c44cbed327068ab895c244f2ddfa86e27a`  
**Candidate publication:** `7753a7512c2e8d724fbbff4585017c3dd1b3825b`  
**Qualified native source:** `82f9f5c9868f7ad5847784bf92109f297ae0b876`  
**Source predecessor:** Revision 73 final head `ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f`  
**Controlling external report:** Revision 73 r47, `fa857238020a0b5f2befd936b39820a9b426390a`  
**Controlling pipeline audit:** `62ffc56f0911b939f3e6b79ae0a5e38563e5a988`  
**Source qualification workflow:** `37172756259`, conclusion `success`  
**Exact-head read-only reconstruction:** `37173200597`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v74-external-referee-r48-2026-10-04`  
**Date:** 4 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 74 contains a coherent and technically serious theorem package. I did not find a fatal gap in the finite-use metric comparison on the full unbiased binary qubit measurement ball, the radial Bernoulli reduction and support-cutoff estimate, the cancellation-free coupling of radial and angular perturbations, the weighted Ahlfors covering theorem, the boundary-contact trichotomy, the disk and ball covering laws, or the exact rational joint codec. I also rechecked the inherited Revision 73 equal-visibility angular theorem and finite Bernoulli majority estimate at the points where the new proof uses them.

The central metric statement is attractive. For

```text
E_x^± = (I ± x·sigma)/2,   x in B_3,
```

put

```text
s = min{|x|,|y|},
a_N(s) = sqrt(N/(1-s^2+1/N)),
D_N(x,y) = a_N(s)|x-y|.
```

The manuscript proves, with absolute constants and at every finite horizon,

```text
(1/256) min{1,D_N(x,y)}
 <= d_N(M_x,M_y)
 <= min{2,6D_N(x,y)}.
```

The comparison includes complete erasure, unequal visibilities, changing directions, and projective endpoints. It is not merely an integration of a local Fisher metric. The decisive lower-bound step is a genuine noncancellation argument: one fixed input shows that the actual unequal-direction pair is at least as distinguishable as its aligned radial projection; triangle inequality then transfers control to the same-radius angular pair. This is mathematically cleaner than subtracting two lower bounds whose leading effects could cancel.

The metric comparison is then converted into a useful geometric statement. On a compact identifiable `k`-Ahlfors-regular subfamily `X`, the small-error covering number, even when lower-bound centres are allowed to be arbitrary legal memoryless binary qubit instruments, is comparable to

```text
delta^(-k) ∫_X [N/(1-|x|^2+1/N)]^(k/2) dmu(x).
```

The support-depth distribution produces interior, critical-logarithmic, and boundary-dominated regimes. In particular, the coordinate disk has covering order

```text
N log(N+2) delta^(-2),
```

whereas the full ball has order

```text
N^2 delta^(-3).
```

The exact rational codec charges visibility and direction in one payload index, accepts rational Cartesian vectors whose Euclidean norm need not be rational, and decodes every word to a legal rational measurement.

These are meaningful advances over Revision 73. Revision 73 treated one equal-visibility circle with public visibility. Revision 74 encodes the radial coordinate, proves an all-pair finite-use comparison, and extracts a general weighted local-covering criterion for regular identifiable subsets of the whole unbiased binary qubit ball.

The four-leading-journal disposition nevertheless remains negative. The new mathematical core is still a finite-dimensional analysis of one very special measurement body. After the pairwise operational metric has been identified up to constants, the passage to covering numbers uses classical Ahlfors regularity, separated nets, weighted local volume, and Stieltjes integration. The result does not classify biased POVMs, multi-outcome measurements, general instruments, nonobservable readouts, or coupled reversible/support-changing directions outside this qubit ball. It is restricted to a fixed small-error regime, gives no exact all-use metric formula or sharp leading constants, and supplies pair-dependent tests rather than one common estimator. The constructive theorem encodes supplied matrix data; it is not unknown-device learning, mutable-workspace complexity, or a physical finite-classical-resource simulator.

The independent priority boundary is also not yet settled. The author has correctly added Sedlák--Ziman and the 2018 Puchała--Pawela--Krawiec--Kukulski single-shot result. The focused comparison still omits J. Fiurášek and M. Mičuda, *Optimal two-copy discrimination of quantum measurements*, **Physical Review A 80** (2009), 042312, arXiv:0909.2940. That paper analyzes two uses of projective single-qubit measurements and shows that adaptive probing, entangled probes, and feed-forward can each improve discrimination. It does not contain the present all-`N` noisy-ball metric, weighted covering theorem, or rational code, but it is a direct antecedent for the adaptive two-use measurement-discrimination interface and should be discussed explicitly.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is a strong specialist-level contribution in quantum information, finite-use measurement discrimination, metric entropy, and exact rational coding. I would encourage submission to a strong specialist venue after an independent priority review, a direct comparison with the two-copy discrimination literature, and substantial compression of inherited material. The structural manuscript remains a coherent specialist contribution, but it is inherited in this revision and retains its fresh nondisturbing classical-probe scope.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 74 manuscript branches are identical at

```text
8477a4c44cbed327068ab895c244f2ddfa86e27a.
```

No Revision 75 branch was present in the branch survey used for this report. The final head is a direct successor of candidate publication `7753a751...` and adds only the exact-head reconstruction request. The candidate publication is a direct successor of qualified native source `82f9f5c9...`. Revision 74 is seven commits ahead of the completed Revision 73 head `ab67d30d...`.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/50-coupled-boundary-geometry.tex`;
- the inherited `sections/49-noisy-readout-crossover.tex` used in the angular comparison;
- `coupled_codec.py` and `check_coupled_geometry.py`;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r47 report and proof/pipeline audit;
- the active focused bibliography and comparison section;
- the schemas, resource ledgers, build receipt, source hashes, page checks, theorem locations, and preservation manifest;
- source qualification run `37172756259`; and
- exact-head read-only reconstruction run `37173200597`.

The quantitative paper has 46 pages, the structural companion 41 pages, and the complete research edition 146 pages. The package preserves 222 predecessor native files and 502 predecessor complete-edition labels; the current complete edition has 522 active labels.

I also made a targeted comparison with primary work on single-shot and multiple-shot quantum-measurement discrimination, adaptive two-use projective-measurement discrimination, noisy metrology, environment-programme methods, and finite-dimensional metric entropy. This is not a formal proof-assistant verification and not an exhaustive novelty search. Where priority remains uncertain, I treat it as an editorial limitation rather than as a mathematical counterexample.

---

## 2. Executive assessment of the new mathematics

### 2.1 The entire unbiased binary measurement ball

The target family consists of ordered binary qubit measurements with Bloch vector `x` in the closed Euclidean unit ball. The origin is one identifiable erased measurement, not a sphere with an unobservable direction. Opposite vectors remain distinct because the outcome labels are ordered.

The proposed local scale

```text
a_N(r) = sqrt(N/(1-r^2+1/N))
```

has the correct finite-use interpolation:

- at fixed interior visibility it is of order `sqrt(N)`;
- within distance of order `1/N` from the projective boundary it reaches order `N`;
- at erasure it remains of order `sqrt(N)`, but the Euclidean parameter itself collapses all directions to one point.

The theorem compares the adaptive operational distance directly to this weighted Euclidean scale, rather than assigning independent radial and angular payloads.

### 2.2 Exact radial reduction

For aligned vectors `ru` and `su`, the measurement is a fixed projective measurement along `u` followed by an independent Bernoulli flip. Every adaptive tester is therefore a common channel of the `N` flip bits. Repeated use of the `+u` eigenstate attains the full product-Bernoulli trace distance. This proves an exact equality, not merely an upper bound.

The support-cutoff argument chooses a block length comparable to

```text
min{N,(1-s)^(-1)}.
```

The event of no success converts a rare Bernoulli probability into a symmetric bias with a common stochastic post-processing. The inherited finite majority lemma then gives square-root amplification over the independent blocks. This correctly handles probabilities approaching zero, where a variance-only normal approximation would be inadequate.

### 2.3 Cancellation-free coupling of radial and angular directions

Suppose `x=ru`, `y=sv`, with `r>=s`. Inputting the `+u` eigenstate produces a binomial pair whose second success parameter is at least that of the aligned radial comparison. Monotone likelihood ratio of binomial counts shows that its total variation is no smaller. Consequently,

```text
d_N(M_ru,M_su) <= d_N(M_ru,M_sv).
```

Triangle inequality then gives

```text
d_N(M_su,M_sv) <= 2 d_N(M_ru,M_sv).
```

The inherited fixed-visibility angular lower bound and the new radial lower bound can now be combined without subtracting one effect from the other. The constants in the final `1/256` lower estimate are conservative and consistent.

For the upper bound, radial and angular paths are concatenated. The elementary inequalities

```text
r-s <= |ru-sv|,
sh <= (pi/2)|ru-sv|
```

lead to the stated factor `6`. The endpoint `s=0` is separately and correctly assigned to the radial argument.

### 2.4 Weighted local covering

Let

```text
e_N(x)=1-|x|^2+1/N,
w_N(x)=sqrt(N/e_N(x)).
```

On Euclidean balls of radius proportional to `t/w_N(x)`, the relative change of `e_N` is bounded by a fixed multiple of `t`. Conversely, sufficiently small operational distance forces Euclidean localization at that scale. Hence the operational balls on `X` are locally comparable with weighted Euclidean balls.

If `mu` is `k`-Ahlfors regular, the weighted measure

```text
dnu_N = w_N^k dmu
```

assigns mass of order `t^k` to every sufficiently small operational ball. Standard separated-net arguments then give both covering bounds. The lower bound genuinely permits arbitrary legal centres: a `3 delta`-separated target packing cannot have two points in any radius-`delta` ball, regardless of where that ball is centred. No unproved retraction onto `X` is used.

This theorem is correct under its explicit regularity and small-error hypotheses. It should not be advertised for arbitrary fractal or nonregular families without additional local-measure assumptions.

### 2.5 Boundary contact

The Stieltjes calculation uses the distribution

```text
F(t)=mu{1-|x|^2 <= t}.
```

If `F(t)` has order `t^alpha`, integration of

```text
(t+1/N)^(-k/2)
```

gives the three regimes stated in the paper. An atom on the projective boundary contributes `N^k` because `w_N=N` there.

For a `d`-dimensional coordinate ball, the depth exponent is one. Thus:

- `d=1`: ordinary interior order `sqrt(N) delta^(-1)`;
- `d=2`: critical order `N log(N+2) delta^(-2)`;
- `d=3`: boundary-dominated order `N^2 delta^(-3)`.

The logarithm for the disk is a genuine joint-family effect. It is not obtained by multiplying or integrating independent fixed-visibility circle code lengths without checking local geometry.

### 2.6 Exact rational joint codec

The radial coordinate is encoded through rational values

```text
r_i = 2 t_i/(1+t_i^2),   t_i=i/B.
```

For a rational Cartesian target `x`, comparison of its possibly irrational norm with a rational radial layer is reduced to a comparison of rational squares. The direction chart uses

```text
x_l/(|x|+|x_j|),
```

but the nearest rational digit is selected by first checking the sign of `b-va` and only then squaring. This avoids an invalid equivalence when the unsquared side is negative.

Every signed-axis stereographic grid point has exact rational unit norm. Multiplication by `r_i` produces a legal rational Bloch vector. The decoded Choi blocks are positive semidefinite and sum to the identity. The single union index charges the radial layer and the angular chart/digits together.

The radial precision gives operational error at most `delta/8`; the angular precision gives at most `delta/8`. The implementation records a more conservative `delta/4` certificate. The capacity estimates correctly produce the harmonic sum in dimension two and the square-summable boundary layers in dimension three.

The implementation is pseudo-polynomial in the numerical grid size. The paper correctly makes no polynomial-time claim in the binary lengths of `N` and `1/delta`, and no optimal-workspace claim.

---

## 3. Detailed correctness comments

### 3.1 Ordered-outcome convention

The one-use identity `d_1=|x-y|` depends on treating the two outcomes as ordered. The manuscript maintains this convention. Quotienting by outcome relabelling would identify `x` with `-x` and change the parameter space and covering law.

### 3.2 The radial block length

When the smaller Bernoulli probability is `q`, the choice

```text
k=min{N,floor((2q)^(-1))}
```

ensures both a nontrivial number of blocks and a lower bound on the no-success probability. The proof separately excludes the only singular identical endpoint. The floor estimates used to compare `k` with `min{N,q^(-1)}` are safe.

### 3.3 Common stochastic processing

The affine map from the two no-success probabilities to opposite symmetric biases is common to the two hypotheses. The displayed values of `b` and `c` satisfy `b>=0`, `b+c<=1`, and `c>=1/2`. Thus the processing is a genuine binary stochastic channel, not a signed normalization.

### 3.4 Binomial monotonicity

For fixed lower success probability, total variation from a binomial law is monotone as the upper parameter increases. The monotone-likelihood-ratio argument is the correct justification. This step is important because it supplies the inequality between the aligned radial pair and the actual coupled pair.

### 3.5 Use of inherited angular theorem

The fixed-visibility theorem is applied after one common unitary rotation places the two directions in an equatorial great circle. This does not change the adaptive distance. The inherited theorem has ordered outcomes and public fixed visibility, exactly as required for the intermediate comparison.

### 3.6 Local versus global metric

The weight `w_N(x)` is not a globally constant Riemannian density. The covering proof only needs comparability on sufficiently small operational balls. The manuscript correctly restricts the covering theorem to an absolute family-dependent small-error cap.

### 3.7 Identifiability

The Ahlfors set is the image in the Bloch ball, not an arbitrary redundant parameter chart. In particular, the erased measurement has no angular multiplicity. This prevents charging unobservable coordinates.

### 3.8 Arbitrary centres

The lower covering number permits every legal memoryless binary qubit instrument as a centre. The proof uses only separation and triangle inequality, so the centre need not lie in the target family or in the Bloch subset `X`.

### 3.9 Boundary atoms

When `mu` has positive mass on the projective sphere, the theorem gives order `N^k`. This statement concerns the weighted measure of a `k`-regular target family. It should not be confused with the ambient Euclidean dimension of the sphere or with one fixed boundary orbit.

### 3.10 Contact-order illustration

The codimension/contact-order example requires two-sided control of transverse volume and support deficit. It is a sufficient geometric model, not a theorem that every semialgebraic or singular target set automatically has the stated exponent.

### 3.11 Exact codec versus optimal cover

The rational code gives an upper cover of the coordinate disk and ball. It does not produce a minimum codebook, optimize leading constants, or prove that its chart redundancy is necessary.

### 3.12 Rational inputs

The target coordinates are rational; the norm may be irrational. The algorithm never stores that norm. All comparisons reduce to exact rational inequalities and integer square roots.

### 3.13 Decoder legality and target replay

Every syntactically valid codeword decodes to a legal measurement. Whether it is the canonical encoding of a supplied target is a stricter statement checked by re-encoding. The implementation keeps these two assertions separate.

### 3.14 Payload accounting

The payload is the fixed-length index capacity. Public dimension, horizon, and requested error are outside that leading payload, while visibility is not public and is charged through the radial layer. JSON syntax, encoder workspace, lookup tables, and expanded matrices are distinct resources.

### 3.15 Small-error range

The operational metric theorem holds at all distances, but the covering criterion and its payload consequences require a fixed sufficiently small error. The abstract and theorem statements preserve this distinction. No large-error multiplicity theorem for the full ball is established.

---

## 4. Implementation and reproducibility

### 4.1 Codec source

`coupled_codec.py` implements:

- strict rational parsing of two- or three-dimensional Cartesian targets;
- exact unit-ball validation;
- radial and angular grid computation by integer ceiling square roots;
- algebraic nearest-layer comparison without evaluating `|x|`;
- sign-before-square direction comparison;
- one-index layer/chart/digit ranking;
- canonical hexadecimal payload parsing;
- exact rational stereographic decoding;
- legal binary qubit Choi assembly; and
- target-bound canonical replay.

The cache validates arguments before lookup, avoiding the Python `bool`/`int` key collision. This is a useful implementation detail and is explicitly regression-tested.

### 4.2 Finite regression

`check_coupled_geometry.py` records 2,265 exact assertions across binomial bounds, monotonicity, algebraic comparisons, codec cases, and all-word legality, together with 33 named negative controls. It uses no floating-point decision. It checks representative finite consequences of the written proof and implementation identities.

It does not prove the continuum Ahlfors theorem, the adaptive supremum, the all-pair operational metric, or novelty. The files state this limitation correctly.

### 4.3 Build evidence

The committed build receipt records:

- 46 pages for the quantitative paper;
- 41 pages for the structural paper;
- 146 pages for the complete edition;
- isolated rebuild success;
- no recorded LaTeX diagnostics;
- normal and optimized test agreement;
- all ten inherited suites plus the new v74 suite;
- 222 preserved predecessor native files; and
- 522 complete-edition labels.

These are strong reproducibility practices. They are not mathematical proof or independent priority clearance.

### 4.4 Exact-head verification

Run `37173200597` checked out the exact reviewed final head without retained credentials, rebuilt all sources, pages, and tests read-only, independently rebuilt the minimal journal source package, and uploaded an external exact-head attestation. The earlier source qualification run `37172756259` also completed successfully.

The final commit is unsigned. The package does not claim a cryptographic human author signature, and source identity should not be described as authorship authentication.

---

## 5. Priority and significance

### 5.1 Correctly credited antecedents

The paper now directly discusses:

- Sedlák--Ziman on single-shot discrimination of noisy qubit measurements with possibly unequal noise levels;
- Puchała--Pawela--Krawiec--Kukulski on the single-shot projective-measurement distance;
- the later multiple-shot projective-measurement theorem used in the inherited observable-readout result;
- classical channel-programme and noisy metrological bounds;
- environment-parametrized and environment-seizable channel methods;
- quantum population compression;
- adaptive channel discrimination; and
- finite-dimensional channel learning and physical simulation as distinct resource questions.

These comparisons substantially improve the priority presentation.

### 5.2 Missing direct adaptive two-use antecedent

Fiurášek--Mičuda, *Optimal two-copy discrimination of quantum measurements*, **Phys. Rev. A 80** (2009), 042312, studies two uses of projective single-qubit measurements and compares fixed probes, adaptive probes, entangled probes, and feed-forward. It proves strict adaptive advantages in parts of the parameter range and perfect two-use discrimination for sufficiently separated measurements with entanglement and feed-forward.

The model is narrower than the present arbitrary-`N` noisy-ball family and does not give a covering theorem or exact rational code. It is nevertheless a direct historical antecedent for the adaptive two-use quantifier and should be added to the focused comparison and bibliography.

### 5.3 What appears genuinely new in this package

Subject to an independent expert priority review, the strongest plausible increments are:

1. a single all-pair, all-horizon two-sided metric comparison on the whole unbiased binary qubit measurement ball with one finite-use support cutoff;
2. the cancellation-free coupling of support change and basis change;
3. the weighted Ahlfors covering criterion for regular identifiable subfamilies, including arbitrary off-family legal centres in the lower bound;
4. the boundary-contact trichotomy and the critical logarithm for the disk; and
5. an exact rational joint visibility/direction codec accepting rational Cartesian targets of irrational norm.

The individual ingredients—binary product testing, adaptive measurement discrimination, programme contraction, local packing, Stieltjes integration, and stereographic charts—are classical or have clear antecedents.

---

## 6. Why the four-leading-journal threshold is not met

### 6.1 Restricted object

The new theorem treats ordered, unbiased, binary qubit measurements. It does not cover biased effects, more outcomes, higher-dimensional POVM bodies, quantum outputs, or disturbing instruments.

### 6.2 Conditional geometric criterion

The covering theorem assumes compactness, identifiability, and uniform Ahlfors regularity. These are useful and transparent hypotheses, but the theorem does not derive them from a broad class of instrument varieties or singular semialgebraic models.

### 6.3 Small-error scope

The covering law is local in the accuracy. There is no full submaximal-error covering classification for the coupled ball and no common-estimator argument controlling large-radius multiplicity.

### 6.4 Constants and exact distance

The theorem gives absolute comparison constants, not an exact finite-use adaptive distance, sharp leading covering constants, or a characterization of optimal testers.

### 6.5 Pair-dependent lower witnesses

The lower bound may choose a different test for each pair. This is sufficient for metric packing but does not provide a single estimator, tomography protocol, or codeword-identification measurement for the whole family.

### 6.6 Supplied description, not learning

The encoder receives the exact target matrix data. The result does not give sample/query complexity for an unknown measurement and does not address statistical estimation error.

### 6.7 Description, not physical simulation

A rational codeword specifies a mathematical quantum measurement. It is not a finite classical device that implements the measurement on an unknown or entangled physical input.

### 6.8 No general boundary classification

The paper isolates one support-changing/coherent crossover. It does not classify general tangent directions of quantum instrument bodies, nonobservable readouts, or coupled reversible and irreversible parameters.

### 6.9 Priority remains external

The author-side audit is candid and useful, but it is not independent expert priority clearance. The missing 2009 adaptive two-use comparison confirms that the literature boundary still needs specialist review.

### 6.10 Structural contribution is inherited

The structural companion is not materially advanced in Revision 74. Its same-width stationarization, finite-action classification, and repeatable-probe strong converse should be judged separately and retain their established scope restrictions.

### 6.11 No whole-program closure

The finite-dimensional covering result does not establish any raw local limit, stopped-path large deviation, global past kernel, shell conditioning, Mosco/Nisio recovery, filtering/LAN, changing-filtration response, or posterior-contraction gate in the repository-wide A/B/C/D programme. Every aggregate completion flag remains false.

### 6.12 General-journal breadth

I do not see a consequence resolving a recognized external open problem of breadth comparable to the leading general journals. The paper is strongest as a precise specialist theorem about finite-use measurement-description geometry.

---

## 7. Required changes before specialist submission

1. **Add Fiurášek--Mičuda (2009)** to the focused bibliography and compare its adaptive, entangled, and feed-forward two-use strategies directly with the present metric interface.

2. **Commission an independent priority review** from an expert in quantum measurement discrimination and local quantum statistical geometry.

3. **Keep the focused quantitative article independent.** The 146-page research edition should remain archival rather than part of the journal submission.

4. **State the target class in every headline.** “Unbiased ordered binary qubit measurements” should not be shortened to “measurement bodies” without qualification.

5. **Keep the small-error cap explicit** in the abstract, introduction, and every covering corollary.

6. **Separate the metric theorem from the covering theorem.** The former is global in pair distance; the latter is local and regularity-dependent.

7. **Display the identifiable-image convention** before any dimension or Ahlfors statement.

8. **Do not advertise a general Fisher-volume theorem.** The operational comparison is proved here for this ball; it is not a formal consequence of quantum Fisher information.

9. **Retain arbitrary-centre wording in the converse.** It is one of the stronger aspects of the theorem.

10. **Clarify the role of pair-dependent tests.** They prove packing separation, not one common estimator.

11. **Keep visibility charged in the v74 code.** Do not mix this convention with the inherited public-visibility v73 circle theorem.

12. **State the pseudo-polynomial implementation boundary.** The reference codec is finite and exact but not polynomial in the binary lengths of all numerical parameters.

13. **Keep payload, workspace, matrix expansion, and physical hardware separate.** No one of these should be described as the others.

14. **Retain the ordered-outcome convention.** Any quotient by relabelling would require a new theorem and code.

15. **Explain the source of the disk logarithm in one self-contained paragraph.** It comes from critical boundary contact in the weighted volume, not from a chart-counting artefact.

16. **Separate inherited structural results from v74 novelty** in the cover letter and abstract-level positioning.

17. **Expose the exact final-head verification** and immutable source hashes in supplementary material, without describing them as proof certification.

18. **Provide a signed release if authorship attestation is desired.** The present unsigned commit and CI establish reproducibility, not human identity.

19. **Keep the A/B/C/D pipeline out of the local novelty claim.** No aggregate progress follows from the current theorem.

20. **Tighten the significance claim.** The strongest presentation is the all-pair qubit-ball metric plus weighted covering/contact law and exact joint codec, not a general theory of quantum boundary geometry.

---

## 8. Further detailed comments

1. In the definition of `d_N`, continue to state that trace distance is unhalved.

2. The radial equality should explicitly say that unused programme bits after public stopping are discarded.

3. The `q=0` radial endpoint occurs only for the identical projective pair under the ordering used; the proof handles it, but a one-sentence reminder would help.

4. The no-success block event is a proof device, not an operationally optimal radial statistic.

5. The monotone-likelihood-ratio paragraph should cite a standard binomial stochastic-order reference or retain its present self-contained event argument.

6. The relation between chordal Euclidean distance and angular distance should keep its constants visible.

7. The lower constant `1/256` is safe but not claimed sharp; say this immediately after the theorem.

8. The one-use equality is exact even with a reference. The short duality argument should remain in the focused article.

9. Ahlfors regularity should be stated for the identifiable image and not for a parameter domain before quotienting.

10. The family-dependent error cap `delta_X` may depend on `r_0,c_0,C_0`; avoid language suggesting an absolute universal accuracy range.

11. The weighted measure `nu_N` is an auxiliary geometric measure, not a statistical prior or a hidden-register entropy.

12. The lower arbitrary-centre argument requires pairwise separation strictly greater than `2 delta`; the use of `3 delta` is safe.

13. When `F(0)>0`, distinguish boundary mass in the target measure from the ambient surface measure of the sphere.

14. The contact-order example should retain “two-sided” hypotheses; one-sided upper contact alone does not determine the asymptotic.

15. For the disk, state explicitly that `k=2` and `alpha=1`; for the ball, `k=3` and `alpha=1`.

16. The line case can be proved by the same weighted criterion even though the implemented codec theorem is written only for dimensions two and three.

17. The radial `t` grid contains both endpoints and the erased layer; no angular data should be encoded at `i=0`.

18. The signed-axis chart count includes overlap. This bounded redundancy affects constants, not exponents.

19. The maximum-coordinate chart choice is deterministic and canonical; ties should remain resolved by the fixed axis rule implemented in code.

20. The sign-before-square comparison is essential and merits a highlighted warning in the schema documentation.

21. The certificate field `adaptive_error_upper=delta/4` is a construction budget, not a computed exact error.

22. Every valid codeword is legal, but not every word is the canonical encoding of every target. Keep legality and replay separate.

23. The cache validation against Boolean horizons is good defensive programming and should remain covered by a negative control.

24. The finite regression does not inspect all continuum targets or all adaptive testers; the current scope statement is accurate.

25. The exact-head run verifies the reviewed SHA, unlike an in-workflow self-published successor. This is a genuine provenance improvement.

26. The final SHA is unsigned; do not use “signed attestation” terminology for the Actions artifact.

27. The structural paper's probes are fresh, classical, and nondisturbing. They are not repeated quantum measurements on one system.

28. The old v63 exponential-width multiplicative gap remains unrelated to the new description-covering theorem.

29. The new theorem does not imply an optimal mutable-space lower bound for a streaming implementation of the code.

30. The paper should avoid the phrase “entire boundary geometry” without immediately adding “of the unbiased binary qubit measurement ball.”

31. The arbitrary-centre lower bound is a covering-number statement; it does not imply a nearest-point retraction or convex projection.

32. The disk logarithm is robust under equivalent Ahlfors measures, but constants depend on the regularity data.

33. The full ball order `N^2 delta^(-3)` is not the naive `N^(3/2)` interior volume law; the boundary layer dominates.

34. The projective boundary has coherent scale `N`, while interior directions have scale `sqrt(N)`; the cutoff `1/N` captures their finite-use transition.

35. The bibliographic comparison should distinguish the 2009 two-copy adaptive result, the 2014 noisy single-shot result, the 2018 single-shot distance formula, and the 2021 multiple-shot projective theorem.

36. A specialist cover letter should state explicitly which of those antecedents supply mechanisms and which conclusions remain new.

---

## 9. Final assessment

Revision 74 answers the principal structural question raised by r47 within one important model. It no longer treats visibility as a public parameter. It proves a cancellation-free operational metric comparison for the whole unbiased binary qubit measurement ball, converts that comparison into a weighted local-covering theorem, identifies the critical boundary logarithm, and supplies an exact rational joint code.

I found no fatal gap in the new theorem chain or in the inherited v73 lemmas on which it directly depends. The source, tests, PDFs, and exact final head are reproducible under the recorded workflows.

The result remains a fixed-dimensional specialist theorem. General POVMs and instruments, large-error coupled covers, common estimators, unknown-device learning, physical simulation, sharp constants, and independent priority clearance remain open. The accumulated repository-wide analytic programme is mathematically separate and unclosed.

**Recommendation: reject at the four leading general mathematics journals; encourage a focused submission to a strong specialist venue after the literature and priority corrections above.**
