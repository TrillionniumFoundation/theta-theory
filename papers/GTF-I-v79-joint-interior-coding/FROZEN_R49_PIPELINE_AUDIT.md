# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 75 (r49)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed exact final head:** `16b78c8edef566300ea21300908854ad83455879`  
**Native theorem-source parent:** `efa7b14e2a42c6276f6748f98e3a15f2da018db3`  
**Revision 74 base:** `8477a4c44cbed327068ab895c244f2ddfa86e27a`  
**Prior external report:** v74/r48, `0fd7db3c634b85ad93a4d205b95bf04b6cb7e476`  
**Prior proof/pipeline audit:** `53371065e8684e33bd3f04748dbea652011c5a7e`  
**Exact-head read-only run:** `37181064054`, success  
**Audit branch:** `review/general-theta-foundations-i-v75-proof-pipeline-audit-r49-2026-10-04`  
**Date:** 4 October 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest completed revision | **Pass.** Revision 75 is the highest completed referee-ready GTF-I revision located. |
| Exact branch identity | **Pass.** The v75 work and referee-ready branches point to `16b78c8...`. |
| Source genealogy | **Pass.** v75 is three commits ahead of v74; the theorem-source parent and publication/evidence successor form a direct chain. |
| Full biased effect body | **Pass.** The target is the identifiable closed four-dimensional body of ordered binary qubit effects. |
| One-use normalization | **Pass.** `d_1(E,F)=2||E-F||_op=|a-a'|+|x-x'|`. |
| Bernoulli endpoint estimate | **Pass.** No fatal gap found in the support-cutoff block argument or monotonicity statement. |
| Spectral noncancellation | **Pass.** Maximal and minimal eigenvalue changes are separately witnessed by actual-pair eigenstate tests. |
| Scalar-overlap adaptive upper bound | **Pass.** The dilation overlap is scalar on the input and iterates through arbitrary common adaptive testers. |
| Angular lower bound | **Pass with inherited input.** The product witness and common bias-removing reduction correctly invoke the v73 unbiased theorem. |
| All-pair metric comparison | **Pass.** The spectral/angular path and separate lower witnesses give the stated constant comparison. |
| Full-body covering law | **Pass with small-error scope.** The projective-corner packing and lattice count both yield `N^2 log(N+2) delta^(-4)`. |
| Exact rational codec | **Pass for the declared schema.** Bias, contrast, and direction are encoded in one legal payload index. |
| Finite regression | **Pass as implementation evidence.** It does not prove the adaptive supremum, continuum cover, asymptotic lower bound, or novelty. |
| Exact final-head reconstruction | **Pass.** Run `37181064054` rebuilt the exact reviewed SHA read-only. |
| Cryptographic human signature | **Open.** The relevant commits are unsigned; no contrary claim is made. |
| Independent priority clearance | **Not established.** The active audit is author-side and omits a direct multi-shot rank-one-POVM comparison. |
| Whole Theta A/B/C/D closure | **Open.** All aggregate flags remain false. |
| Four-leading-journal threshold | **Not met.** This is an editorial significance conclusion, not a correctness failure. |

The local v75 mathematical package is coherent and materially broader than v74. It should be assessed as a theorem on one fixed quantum measurement interface, not as a general theory of POVM discrimination, unknown-device learning, mutable simulation space, or the repository-wide analytic programme.

---

## 1. Frozen object and branch genealogy

The latest completed manuscript branches located were

```text
revision/general-theta-foundations-i-v75-full-measurement-body-2026-10-04
revision/general-theta-foundations-i-v75-referee-ready-2026-10-04.
```

Both point to

```text
16b78c8edef566300ea21300908854ad83455879.
```

The exact final head has parent

```text
efa7b14e2a42c6276f6748f98e3a15f2da018db3,
```

which contains the readable theorem source and the v75 proof package. The final successor adds the rendered manuscripts and source-bound evidence. The declared predecessor is the completed v74 exact head

```text
8477a4c44cbed327068ab895c244f2ddfa86e27a.
```

A direct comparison shows three v75 commits after v74: an anchor, the theorem/source commit, and the publication/evidence commit. No manuscript or review branch is overwritten by this audit.

Both r49 audit branches were created directly from the exact final head. Each contains one new report commit and does not modify manuscript source, PDFs, workflows, evidence, predecessor files, or the other audit branch.

---

## 2. Active proof dependency graph

### 2.1 Target geometry and operational distance

```text
ordered binary qubit measurement
  -> one effect E with 0 <= E <= I
  -> Cartesian body (a,x), 0 <= a-|x| <= a+|x| <= 2
  -> spectral data 0 <= q <= p <= 1 and direction u when p>q

qc output channel with no residual quantum system
  + arbitrary common adaptive tester
  + finite reference, quantum memory, feedback, public stop <= N
  -> unhalved final trace distance d_N
```

The target is the effect matrix. At `p=q`, the eigendirection is not part of the identifiable object.

### 2.2 Spectral endpoint chain

```text
Bernoulli product laws
  + direct bit coupling
  + product-fidelity upper bound
  -> upper scale T_N(s,t)

support-sensitive no-success blocks
  + common stochastic recentering
  + finite majority amplification
  -> lower scale T_N(s,t)

extremal eigenstate of one actual effect
  + binomial likelihood-ratio monotonicity
  -> separate lower witness for p versus p'
  -> separate lower witness for q versus q'
```

This prevents changes of the two eigenvalues from cancelling through a change of eigendirection.

### 2.3 Fixed-spectrum angular upper chain

```text
put the two eigendirections in one real meridian
  -> explicit measurement isometries W_E, W_F
  + rotate an inaccessible environment
  -> W_E^* U W_F = c I on the input

scalar overlap c I
  + purify all common tester operations
  + repeat for N slots
  + pad public stopping with ignored calls
  -> output fidelity at least c^(2N)
  -> trace-distance upper bound

hybrid replacement bound
  + scalar-overlap bound
  -> angular scale K_N(p,q) h
```

The scalar identity, not merely a pointwise input overlap, is what permits arbitrary adaptive composition.

### 2.4 Fixed-spectrum angular lower chain

```text
pure tangent input along u-v
  -> Bernoulli gap (p-q) sin(h/2)
  -> denominator controlled by 1-b^2

common half-turn about a perpendicular axis
  + common outcome swap
  + randomize the two branches
  -> remove bias while retaining visibility p-q
  -> inherited unbiased finite entangled-block test
  -> denominator controlled by 1-(p-q)^2

legal-body inequality |b|+(p-q) <= 1
  -> one denominator controls V=p(1-p)+q(1-q)
  -> angular lower scale K_N h
```

These are pair-dependent nonadaptive witnesses. They do not define one estimator for the whole family.

### 2.5 All-pair metric chain

```text
separate endpoint witnesses
  + aligned two-row Bernoulli programme
  + fixed-spectrum angular comparison
  -> path upper bound H_N

actual-pair endpoint witnesses
  + angular projection through an aligned path
  -> lower bound by max{T_p,T_q,K h}
  -> lower bound by min{1,H_N}
```

The path uses the spectrum with the smaller angular coefficient. If one spectrum is scalar, alignment has zero cost.

### 2.6 Full-body covering lower chain

```text
projective-corner depth t
  -> p=1-alpha, q=beta, alpha,beta ~ t
  -> spectral and angular local scales both sqrt(N/t)

four-coordinate grid at operational spacing delta
  -> N^2 delta^(-4) separated points at one depth

geometric depths t=8^j/N
  + endpoint spectral noncancellation
  -> constant separation between different depths
  -> log(N+2) independent depth layers

union
  -> c N^2 log(N+2) delta^(-4) packing
  -> same lower bound against arbitrary legal centres
```

### 2.7 Exact rational upper chain

```text
probability square-root charts near 0 and 1
  -> rational spectral grid including both endpoints
  -> product Bernoulli error O(delta)

for each ordered spectral pair
  -> angular coefficient K_ij
  -> rational signed stereographic grid at mesh delta/K_ij

scalar pair i=j
  -> exactly one word and no direction field

triangular capacity sum
  + endpoint multiplicity bound
  + two-dimensional lattice sum with cutoff B^2/N
  -> C N^2 log(N+2) delta^(-4) words

rational Cartesian target
  + sign-before-squaring radical comparisons
  -> exact spectral rounding and chart rounding
  -> one canonical legal rational codeword
```

### 2.8 Inherited structural and historical graph

Revision 75 retains, but does not newly prove:

```text
stationarization under eventual approximate returns
stochastic purification and finite physical actions
fresh-repeatable-probe causal strong converse
spectral-entropy occupation and width laws
return-free/no-idle quantitative bounds
exponential-accuracy crossover
uniform numerical and Choi streaming
intrinsic instrument and preparation-boundary coding
coherent and input-dependent boundary families
Revision 74 unbiased measurement-ball geometry
```

The v75 proof uses only the required inherited statements. The broader historical graph does not become one common stronger model.

---

## 3. Claim-by-claim status table

| Claim | Main source | Audit result | Principal qualification |
|---|---|---|---|
| Exact one-use effect distance | Section 51 | Correct | Ordered binary qc measurement; unhalved trace norm. |
| Bernoulli endpoint comparison | Section 51, `lem:bernoulliproduct75` | No fatal gap found | Constants safe, not optimal. |
| Spectral endpoint noncancellation | Section 51, `lem:spectralprojection75` | Correct | Uses separate pair-dependent eigenstate witnesses. |
| Aligned spectral programme | Section 51 | Correct | Upper comparison, not an asserted exact formula. |
| Angular scalar-overlap upper bound | Section 51, `thm:biasedangular75` | Correct | Pairwise dilation gauge; no global seizing theorem. |
| Angular lower comparison | Section 51 | Correct modulo inherited v73 theorem | Uses product and bias-removing witnesses. |
| Full all-pair metric | Section 51, `thm:biasedmetric75` | No fatal gap found | Comparison up to constants, not exact optimization. |
| Full effect-body covering | Section 52, `thm:biasedcover75` | No fatal gap found | Sufficiently small error. |
| Projective-corner logarithm | Section 52 | Correct | Caused by depth accumulation, not chart overlap. |
| Exact rational realization | Section 52, `thm:biasedcodec75` | No fatal gap found | Supplied exact Cartesian target; no learning claim. |
| Reference codec implementation | `biased_codec.py` | Consistent with theorem | Quadratic arithmetic in spectral-grid size; no optimal workspace claim. |
| New finite regression | `check_biased_geometry.py` | Pass as regression | Does not prove universal adaptive/continuum claims. |
| Structural companion | inherited source | Preserved | Different fresh nondisturbing classical-probe interface. |
| Whole Theta programme | status/history files | Correctly open | No A/B/C/D aggregate gate is discharged. |

---

## 4. Detailed proof audit: target and one-use geometry

### 4.1 Identifiable body

The legal Cartesian set is the double cone

```text
|x| <= min{a,2-a}.
```

Writing `b=a-1` gives `|b|+|x|<=1`. The spectral coordinates satisfy

```text
p=(a+|x|)/2,
q=(a-|x|)/2.
```

For `p=q`, all choices of `u` give the same scalar effect. The covering code collapses those choices to one word, so the later dimension count does not charge a non-identifiable sphere.

### 4.2 Reference-assisted one-use norm

For a bipartite input `rho_AR`, the difference of the two qc outputs has classical blocks

```text
B_rho = Tr_A[((E-F) tensor I) rho],
-B_rho.
```

The total block trace norm is `2||B_rho||_1`. Duality against Hermitian contractions gives `||B_rho||_1<=||E-F||_op`. An eigenstate of `E-F` attains equality without a reference. For a `2 x 2` Hermitian matrix with scalar/vector coordinates, twice its operator norm is `|Delta a|+|Delta x|`. The normalization is correct.

---

## 5. Detailed proof audit: Bernoulli endpoint geometry

### 5.1 Upper bound

The direct coupling changes at most one bit with probability `|s-t|` per trial and gives the linear bound `2N|s-t|`. Product fidelity gives the square-root variance-sensitive bound. Combining them with the `1/N` cutoff produces the displayed `T_N` upper order, including endpoints.

### 5.2 Lower block construction

After complementing both laws, the proof reduces to `s<t` with controlled upper endpoint. The chosen block length is of order

```text
min{N,1/t}
```

and at least one. The no-success event differs by at least a constant multiple of `k(t-s)`. A common stochastic map sends its two probabilities to symmetric biases around one half. Repeating the processed block and applying the finite majority lemma produces the lower scale

```text
min{1, |s-t| sqrt(N min{N,1/t})}.
```

The variance comparison converts this to `T_N`. No central-limit approximation or asymptotic remainder is used.

### 5.3 Monotonicity

For binomial counts, the likelihood ratio is monotone in the count. Total variation is attained on an upper or lower count interval according to parameter order. Moving one parameter farther away increases the corresponding interval probability difference. This justifies the inequalities used in the spectral projection lemma.

---

## 6. Detailed proof audit: spectral noncancellation

Suppose `p>=p'`. Input a maximum-eigenvalue eigenstate of `E`. Under `E` the success probability is `p`; under `F` it is at most `p'`. Monotonicity therefore makes the product distance at least `B_N(p,p')`. The remaining order cases follow by interchanging the targets.

The same argument at a minimum-eigenvalue eigenstate gives `B_N(q,q')`. These are separate admissible experiments. The proof never asserts simultaneous extraction of both endpoints from one input.

When directions agree, first make the common projective measurement in that basis and then generate the public output using one of two Bernoulli rows. For an entangled input, the reference blocks are exactly the corresponding partial matrix elements. Pre-supplying two independent row-bit arrays therefore makes every adaptive tester a common channel of those arrays. Tensor-product triangle inequality gives the aligned upper bound.

Combining the actual-pair endpoint lower bounds with the aligned upper path gives the stated angular projection estimates without subtracting unrelated tests.

---

## 7. Detailed proof audit: scalar-overlap angular upper bound

### 7.1 Dilation algebra

In a common real meridian, the two effects are `E` and `R_t E R_t^T`. The displayed dilation records the public outcome while retaining an inaccessible square-root environment. A rotation of the second environment changes only the dilation gauge.

The cross overlap has the form

```text
(cos(phi) I + f sin(phi) J) R_(-t).
```

The selected `phi` cancels the `J` part and makes the overlap `cI`. Direct identities relating `f`, `A`, and `p-q` yield

```text
c^2 = A^2/(A^2+(p-q)^2 sin^2(t)).
```

The algebra handles `t=0` and `t=pi/2`. Cases with `A=0` are separated before division.

### 7.2 Adaptive iteration

Purify the tester's initial state and all common inter-slot operations. At each call, the scalar overlap multiplies the global inner product by `c`, independent of the current input/reference state. Common isometries preserve it.

For a publicly stopped tester, make fixed dummy calls after stopping and discard all dummy outputs. A purification of this padded process has overlap `c^N`; tracing inaccessible systems can only increase fidelity of the operational output. The pure-state trace-distance formula therefore supplies the adaptive upper bound.

This is a pairwise comparison. It does not construct one common processor or environment seizer for all effects simultaneously.

### 7.3 Conversion to `K_N`

The inequalities

```text
V <= A^2 <= 2V
```

and the elementary product bound convert the scalar-overlap estimate to the variance-normalized `sqrt(N)` term. The hybrid replacement estimate controls the projective endpoint where the variance vanishes. Their minimum gives the uniform cutoff.

---

## 8. Detailed proof audit: angular lower bound

### 8.1 Tangent product witness

A pure input in the direction `u-v` gives two Bernoulli probabilities centered at the same bias with separation `(p-q) sin(h/2)`. The larger variance is bounded using `1-b^2`. The Bernoulli lemma and `sin(h/2)>=h/pi` give the first lower scale.

### 8.2 Common bias-removing processing

Choose a half-turn mapping both directions to their negatives. Randomly use either the original measurement or the half-turned measurement followed by a public outcome swap. The average positive effect is

```text
(I + (p-q) u·sigma)/2,
```

and similarly for `v`. The same preprocessing/postprocessing is used under both hypotheses, so any test for the resulting unbiased pair is an admissible test for the original pair.

The inherited unbiased finite entangled-block theorem gives the second lower scale with denominator `1-(p-q)^2`.

### 8.3 Denominator comparison

Feasibility `|b|+r<=1` implies that at least one of `1-b^2` and `1-r^2` is within a fixed factor of

```text
1-b^2-r^2 = 2V.
```

Therefore one witness realizes the desired `K_N` order. Scalar and equal-direction cases are explicitly removed.

---

## 9. Detailed proof audit: all-pair comparison

The upper path changes spectra along one direction and then changes direction at the spectrum with smaller angular coefficient. The spectral endpoint estimates and fixed-spectrum theorem sum to at most a constant times `H_N`.

For the lower bound:

- the two endpoint scales are separately at most a constant times the actual-pair distance;
- an angular distance at either spectrum is at most a constant times the actual-pair distance by the aligned path; and
- the fixed-spectrum angular lower theorem transfers the smaller angular scale.

The maximum of three truncated lower bounds controls the truncated sum up to another constant. No invalid simultaneous-test inference is made.

The same argument at the nonadaptive supremum supports the statement that pair-dependent nonadaptive tests witness the lower order.

---

## 10. Detailed proof audit: full-body entropy

### 10.1 Local projective-corner metric

In a box with `alpha,beta~t`, the eigenvalue gap is bounded below and both endpoint variances are comparable to `t`. The two spectral moduli and angular modulus therefore all have coefficient comparable to `sqrt(N/t)`.

On the fixed stereographic chart, angular and Euclidean chart distances are uniformly comparable. This produces the stated local `l_infinity` lower metric in four coordinates.

### 10.2 One-depth packing count

The spectral intervals have width of order `t`. Mesh `delta sqrt(t/N)` gives order `sqrt(Nt)/delta` points in each of the two spectral coordinates. The angular chart has fixed width and gives order `sqrt(N/t)/delta` points in each angular coordinate. Multiplication yields

```text
N^2 delta^(-4)
```

points independently of `t`.

### 10.3 Cross-depth separation

If `t'` is at least eight times `t`, the upper endpoint defects differ by order `t'`. The spectral modulus is then bounded below by an absolute constant because `Nt'>=1`. The actual-pair spectral witness transfers this to operational separation.

There are order `log(N+2)` geometric depths between `1/N` and a fixed constant. Their union is a strict packing. Any radius-`delta` ball about any legal centre contains at most one packing point.

### 10.4 Small horizons

For bounded `N`, a fixed interior spectral rectangle and angular chart have a uniformly nondegenerate local metric. A standard four-dimensional grid supplies the `delta^(-4)` count; the factor `N^2 log(N+2)` is bounded above and below by constants in this finite range.

---

## 11. Detailed proof audit: rational upper cover

### 11.1 Spectral grid

The map `t -> t^2/(1+t^2)` parameterizes square-root probability vectors with uniformly bounded derivative. The reflected chart handles probabilities near one. Rounding the inverse chart to mesh `1/B` gives Hellinger error `O(1/B)` and therefore `N`-copy unhalved trace error `O(sqrt(N)/B)`.

The scalar quantizer is monotone, so separately rounded ordered eigenvalues remain ordered.

### 11.2 Angular grid

For every non-scalar rounded spectral pair, the proved angular coefficient determines `A_ij`. Signed stereographic coordinates in `[-1,1]` are rounded to denominator `A_ij`. The derivative bound gives angular error `O(1/A_ij)`, and the fixed-spectrum upper theorem converts this to the allocated error budget.

Each decoded direction is exactly rational and unit length. Each decoded effect is therefore legal and rational.

### 11.3 Exact target rounding

For rational Cartesian target data, `|x|^2` is rational even when `|x|` is irrational. Spectral threshold decisions have the form

```text
sign(c +/- sqrt(Q)).
```

Checking the rational sign before squaring makes these comparisons exact. Chart-coordinate comparisons have the same form. No floating approximation of an eigenvalue or normalized direction is needed.

### 11.4 Capacity

Let `m_i` measure endpoint depth and `U=B^2/N`. The angular weight satisfies a bound of the form

```text
K_ij^2 <= C N B^2/(m_i^2+m_j^2+U).
```

Endpoint depth multiplicity is bounded. Summing over dyadic square rings gives `O(log(N+2))`, because the ratio between the spectral-grid radius and the cutoff radius is `sqrt(N)`. With `B^2=O(N/delta^2)`, the total capacity is `O(N^2 log(N+2) delta^(-4))`.

The chart redundancy is included explicitly; it affects only constants.

---

## 12. Implementation audit

`biased_codec.py` implements:

- exact rational parsing of bias and Cartesian coordinates;
- exact legality of the effect body;
- exact public parameter validation before cached layout lookup;
- the rational endpoint grid;
- exact radical threshold decisions;
- ordered spectral-pair ranking;
- scale-dependent rational sphere charts;
- one mixed payload index for bias, contrast, and direction;
- exact rational Choi blocks for the two ordered outcomes;
- canonical envelope verification; and
- target-bound deterministic replay.

The implementation retains `O(B)` spectral values and row starts and performs `O(B^2)` exact arithmetic work to construct the layout, with `B` of order `sqrt(N)/delta`. It explicitly disclaims optimal workspace and polynomial running time in all encoded numerical lengths.

The new regression records 3,441 exact assertions covering Bernoulli cases, scalar-gauge identities, spectral intervals, radical comparisons, legal words, codec cases, CLI paths, and malformed/tampered inputs. It uses no floating-point decisions. Its scope statement correctly refuses to infer the continuum metric theorem, covering lower bound, adaptive supremum, or novelty from finite tests.

---

## 13. Build and workflow audit

### 13.1 Build receipt

The committed receipt records:

```text
quantitative paper: 55 pages
structural paper:   41 pages
complete edition:  156 pages
```

It reports an isolated rebuild, no recorded LaTeX diagnostics, ordinary/optimized agreement, 238 predecessor native files, 522 preserved labels, and 557 active complete-edition labels. Twelve exact suites are retained.

### 13.2 Exact-head workflow

Actions run `37181064054` has triggering head

```text
16b78c8edef566300ea21300908854ad83455879
```

and conclusion `success`. Its read-only job:

1. checked out the exact submitted object;
2. installed the pinned typesetting and arithmetic environment;
3. rebuilt submitted sources and every PDF page;
4. independently rebuilt the focused journal package; and
5. uploaded source-bound reconstruction evidence.

This supplies the trust separation that earlier self-publishing workflows lacked.

### 13.3 Evidentiary boundary

The final and source commits are unsigned. The workflow establishes byte identity and reproducibility, not human authorship. Finite regression, PDF equality, and source hashes do not certify continuum mathematics, priority, or acceptance.

---

## 14. Literature and priority audit

The active author-side comparison correctly distinguishes:

- Fiurášek–Mičuda's two-use projective-qubit discrimination;
- Sedlák–Ziman's single-shot unequal-visibility unbiased example;
- the single-use projective measurement distance of Puchała–Pawela–Krawiec–Kukulski; and
- the all-use projective endpoint and parallel-optimality theorem of Puchała–Pawela–Krawiec–Kukulski–Oszmaniec.

The manuscript's claimed increment is different: a global constant-comparison metric over all ordered biased binary qubit effects, followed by a global small-error covering theorem and exact supplied-description code.

A direct neighboring reference is still missing from the active comparison:

```text
A. Krawiec, L. Pawela, Z. Puchała,
Discrimination of POVMs with rank-one effects,
arXiv:2002.05452 (2020).
```

That work explicitly studies multiple-shot parallel and adaptive discrimination of rank-one POVMs and constructs a pair of symmetric informationally complete POVMs perfectly discriminated by a two-shot adaptive scheme. It is not theorem-equivalent to v75, but it bears directly on the broader multi-shot POVM-discrimination context.

The nonprojective single-shot literature, including Datta–Biswas–Saha–Augusiak, arXiv:2012.07069, should also be connected explicitly to the manuscript's scope.

The author audit itself states that it is targeted rather than independent. No external specialist priority clearance is present. This is a high editorial risk at the four-leading-journal level.

---

## 15. Repository-wide pipeline assessment

The frozen analytic graph remains

```text
A1 independent
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Open obligations include raw unsmoothed local limits, predictable stopped-path entropy/LDP recovery, a global past kernel, exact canonical coefficients and shell conditioning, process CLT and independent Mosco recovery, nonlinear Nisio resolvents and cores, regular filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction.

The v75 finite-use measurement metric and covering code neither assume nor prove those objects. A public stopping rule in an adaptive tester is not a stopped-path large-deviation theorem. A projective-corner volume calculation is not Mosco convergence. Exact codec replay is not filtering or posterior contraction.

Accordingly, the following remain false:

```text
historical A2 replacement
B4 aggregate
C2 aggregate
eleven-paper aggregate
whole Theta programme closure.
```

This separation is correctly recorded in the package and must be retained.

---

## 16. Risk register

### R1 — Priority risk: high

The exact theorem-level relation to multi-shot rank-one POVM discrimination and local quantum statistical geometry is not independently settled.

### R2 — Breadth risk: high for top-four, low for a specialist venue

The theorem is complete for one binary-qubit qc interface but does not cover general POVMs, higher dimensions, or residual quantum outputs.

### R3 — Exactness risk: moderate

The metric is determined only up to constants. Claims of exact adaptive geometry would exceed the proof.

### R4 — Error-range risk: moderate

The covering theorem is small-error. The all-pair metric is global, but it does not by itself give the same asymptotic code law at every fixed error.

### R5 — Resource-interpretation risk: moderate

Description length, encoder workspace, unknown-device learning, query complexity, and physical simulation are distinct. The current manuscript states this correctly; summaries must preserve it.

### R6 — Implementation risk: low

The exact rational codec closely follows the written construction and has extensive negative controls.

### R7 — Reproducibility risk: low

The exact final head has a successful read-only reconstruction. Human signing remains absent.

### R8 — Whole-program overclaim risk: controlled

All A/B/C/D aggregate flags remain false. Future introductions should not blur this boundary.

---

## 17. Recommended specialist-release gates

### Mathematical gates

- retain complete proofs of the Bernoulli endpoint lemma, spectral projection lemma, scalar-overlap dilation, both angular lower witnesses, full metric theorem, projective-corner packing, and lattice count;
- keep the exact one-use normalization visible;
- keep the small-error hypothesis in the covering theorem;
- preserve arbitrary legal centres in the lower cover;
- preserve pair-dependent test quantifiers; and
- avoid exact-distance language beyond the projective and one-use endpoints.

### Scope gates

- say “ordered binary qubit measurements with no residual quantum output” in the title/abstract;
- distinguish supplied-description coding from unknown-device learning;
- distinguish payload from workspace and expanded output;
- distinguish the v75 theorem from the inherited structural fresh-probe theorem; and
- state explicitly that no multi-outcome or higher-dimensional theorem is proved.

### Priority gates

- add the Krawiec–Pawela–Puchała rank-one-POVM comparison;
- add the relevant nonprojective single-shot literature;
- obtain an independent specialist priority review; and
- formulate the precise novelty as the full biased binary effect-body metric, projective-corner logarithm, and exact joint rational code.

### Reproducibility gates

- preserve exact-head read-only reconstruction for the submitted SHA;
- retain the source/package manifest and theorem-location map;
- keep finite-test scope disclaimers;
- use a signed release if human authorship provenance is desired; and
- do not equate Actions success with mathematical or priority certification.

### Editorial gates

- submit the focused quantitative paper separately;
- move long historical genealogy to repository notes or a short appendix;
- reduce repetition among the introduction, response, proof audit, and comparison; and
- keep the complete research edition archival.

---

## 18. Final audit verdict

### Local mathematics

**No fatal gap found in the inspected v75 theorem chain.** The Bernoulli endpoint analysis, spectral noncancellation, scalar-overlap adaptive upper bound, complementary angular lower witnesses, global metric comparison, full-body packing, and exact rational upper code form a coherent proof package.

### Reproducibility

**Pass.** The exact reviewed SHA has a successful read-only reconstruction and a source-bound receipt covering every PDF page and the focused journal package.

### Priority

**Open.** The author-side audit is careful but incomplete and non-independent. At least one direct multi-shot adaptive rank-one-POVM antecedent remains to be integrated.

### Repository-wide programme

**Open and separate.** No A/B/C/D aggregate gate is discharged.

### Editorial threshold

**Not met at the four leading general journals.** The work is a strong specialist theorem on a fixed binary-qubit interface, not yet a sufficiently broad general mathematical theory.

```text
latest revision identity:        PASS
full biased-body metric:         PASS WITH CONSTANT-COMPARISON SCOPE
full-body small-error entropy:   PASS
exact rational codec:            PASS
implementation regression:       PASS AS FINITE EVIDENCE
exact-head reconstruction:       PASS
independent priority:            OPEN
whole-program closure:           OPEN
four-leading-journal bar:        NOT MET
```
