# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 76 (r50)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed exact final head:** `c041c011274973728a8cc55029192c057696aa43`  
**Native theorem-source parent:** `a107cd1a0f7ec4e356e807f5f49c7ab998553552`  
**Completed predecessor:** v75 exact head `16b78c8edef566300ea21300908854ad83455879`  
**Controlling external report:** v75/r49 at `4de14a3fe5c271c77de64e410e1bd67fa2e7dce8`  
**Controlling proof/pipeline audit:** v75/r49 at `8ee073109d5911c6526ff81314bede13bafe9f6c`  
**Exact-head read-only run:** `37198984154`, success  
**Audit branch:** `review/general-theta-foundations-i-v76-proof-pipeline-audit-r50-2026-10-04`  
**Date:** 4 October 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest completed revision | **Pass.** Revision 76 is the highest completed referee-ready GTF-I revision located. |
| Exact branch identity | **Pass.** The v76 response and referee-ready branches identify `c041c011...`; the native theorem source is its direct parent `a107cd1a...`. |
| Source genealogy | **Pass.** The revision is a direct successor of completed v75 and preserves the controlling r49 reports verbatim. |
| Ordered binary matrix body | **Pass.** The object is exactly `0<=E<=I_d`, with ordered classical outcomes and no residual quantum output. |
| One-use normalization | **Pass.** `d_1(E,F)=2||E-F||_op`. |
| Horizontal dilation | **Pass.** The prescribed factors are genuine local dilations and satisfy `W*dot W=0`. |
| Adaptive tangent bound | **Pass.** Orthogonality of differentiated slots and the regularized residual yield the stated path inequality. |
| Midpoint resolvent upper bound | **Pass.** Operator concavity and the integrable endpoint factor give `d_N<=8Q_N`. |
| Matrix converse | **Pass.** Diagonal Bernoulli tests and exact two-dimensional compressions control every weighted entry. |
| Adaptive/nonadaptive comparison | **Pass with dimension dependence.** The factor is `O(d)` and is not an equality or a dimension-free statement. |
| Spectral noncancellation | **Pass.** The intersecting-subspaces argument covers every ordered eigenvalue and multiplicity. |
| Local form comparison | **Pass.** The normalized variance perturbation gives uniform fixed-dimensional local equivalence. |
| Boundary operational-ball volume | **Pass.** The proof moves inward by order `r/N` and contains a full legal ellipsoid. |
| Spectral determinant | **Pass.** The real Hermitian determinant and squared Vandermonde factors are consistent. |
| Nested endpoint integral | **Pass.** Balanced signed prefixes give at most `floor(d/2)` logarithms, and separated paired boxes match them. |
| Full-body covering law | **Pass with fixed-d/small-error scope.** Arbitrary legal centres are allowed. |
| Rational centres | **Pass as existence.** No arbitrary-dimensional efficient or canonical encoder is established. |
| Common qubit learner | **Qualified pass.** The mathematics closes, but the dyadic procedure must explicitly terminate on first rejection. |
| Learning minimax converse | **Pass.** Scalar effects reduce every adaptive training strategy to Bernoulli data. |
| Learned exact description | **Pass for qubits.** Rationalization plus the inherited v75 codec uses no additional device calls. |
| Matrix-geometry regression | **Pass as finite evidence.** It is not a continuum proof or adaptive-distance solver. |
| Common-learning regression | **Pass as finite identity/budget evidence.** It is not an executable learner or risk certificate. |
| Native build | **Pass.** Isolated build, all manuscripts, label preservation, and normal/optimized agreement are recorded. |
| Exact final-head reconstruction | **Pass.** Run `37198984154` rebuilt the exact final SHA and journal package read-only. |
| Cryptographic human signature | **Open.** The source/publication commits are unsigned; no contrary claim is made. |
| Independent priority clearance | **Not established.** The literature audit is author-side. |
| Whole Theta A/B/C/D closure | **Open.** Every aggregate flag remains false. |
| Four-leading-journal threshold | **Not met in the accompanying referee judgment.** This is a significance conclusion, not a correctness failure. |

The v76 local theorem package is coherent and materially broader than v75. It should be assessed as a theory of one complete binary measurement interface, not as a theorem for all POVMs, instruments, channel learning, or the repository-wide analytic programme.

---

## 1. Frozen object and branch genealogy

The active revision branches located for the completed manuscript are

```text
revision/general-theta-foundations-i-v76-r49-response-2026-10-04
revision/general-theta-foundations-i-v76-native-source-2026-10-04
revision/general-theta-foundations-i-v76-referee-ready-2026-10-04.
```

The exact submitted head is

```text
c041c011274973728a8cc55029192c057696aa43.
```

Its direct theorem-source parent is

```text
a107cd1a0f7ec4e356e807f5f49c7ab998553552.
```

The final child adds the rendered papers and source-bound evidence. The completed mathematical predecessor is v75 at

```text
16b78c8edef566300ea21300908854ad83455879.
```

The two r49 reports are frozen inputs to v76. Their exact commits and branches are recorded in `CONTROLLING_REPORTS.json`. The v76 response addresses them without overwriting the review branches.

The two r50 branches were created directly from the exact v76 final head. Each review branch is independent of the other and is intended to add only its own report. Manuscript source, PDFs, workflows, evidence, and historical files remain unchanged by the review commits.

---

## 2. Scope of the active object

For fixed input dimension `d`, the target body is

\[
 \mathfrak E_d=\{E=E^*:0\preceq E\preceq I_d\}.
\]

The corresponding memoryless device consumes one input system and returns one of two ordered classical labels according to the effects `E` and `I-E`. There is no residual quantum output. A finite-use tester may retain an arbitrary reference and quantum memory, use common intermediate channels and classical feedback, and stop publicly after at most `N` calls.

The distance `d_N` is the supremum of the **unhalved** final trace norm. Its nonadaptive restriction `d_N^na` permits a block-entangled input and retained reference but no feedback between calls. Pair-dependent witnesses are legal in both definitions.

The new matrix metric and covering theorems hold for every fixed `d`. Constants and the small-error cap may depend on `d`. The new common learner and implemented exact joint codec are restricted to input dimension two.

---

## 3. Active proof dependency graph

### 3.1 Matrix metric upper chain

```text
binary effect G
  -> square-root factors sqrt(G), sqrt(I-G)
  -> horizontal derivative H0 = S K + K S
  -> genuine local Kraus gauges with W* dot W = 0

W* dot W = 0
  + purification of common adaptive tester
  -> differentiated call slots are orthogonal
  -> horizontal derivative cost 2 sqrt(N) ||K||op

regularized Sylvester equation
  S K + K S + N^(-1/2) K = H
  -> horizontal tangent + residual tangent
  -> residual controlled by N-slot hybrid bound
  -> output derivative <= 4 g_(N,G)(H)

integrate along a path
  + interior approximation for closed-body paths
  -> d_N <= 4 integral g_(N,G)(G')

straight path E -> F
  + operator concavity of G(I-G)
  -> V_(G(t)) >= 2 min(t,1-t) V_M
  -> integral factor 2
  -> d_N(E,F) <= 8 Q_N(E,F)
```

### 3.2 Matrix metric lower chain

```text
midpoint eigenbasis
  -> weighted entries q_ij

diagonal q_ii
  -> repeated basis-state input
  -> Bernoulli endpoint lower bound

off-diagonal q_ij
  -> exact compression to span{e_i,e_j}
  -> full biased-qubit metric from v75
  + variance identity at the compressed midpoint
  -> nonadaptive lower witness

max_ij q_ij >= Q_N/d
  -> d_N^na >= min(1,Q_N)/(8192d)
```

### 3.3 Spectral and local matrix chain

```text
ordered eigenvalue k
  -> first-k eigenspace of one effect
  intersect complement of first-(k-1) eigenspace of the other
  -> vector with ordered Bernoulli probabilities
  -> spectral noncancellation

W_E = E(I-E)+(2N)^(-1)I
  + normalized perturbation expansion
  -> local Loewner comparison of W_E and W_F
  -> local comparison of quadratic forms and determinant densities
```

### 3.4 Entropy chain

```text
local metric/form equivalence
  -> operational ball contained in a form ellipsoid
  -> uniform upper mu_N-volume

boundary centre E
  -> inward shift E_s=(1-2s)E+sI, s ~ r/N
  -> full legal ellipsoid around E_s
  -> uniform lower mu_N-volume

quadratic-form determinant
  + Hermitian spectral Jacobian
  -> spectral integral I_d(1/N)

endpoint sector signs epsilon_i
  -> signed prefixes S_j
  -> cumulative exponents A_j=S_j^2/2
  -> at most floor(d/2) critical logarithmic variables

nested opposite-endpoint pairs at separated scales
  -> matching lower boxes
  -> total volume N^(d^2/2) log(N)^(floor(d/2))

uniform ball volumes + total volume
  -> covering lower and upper bounds
  -> rational-centre existence
```

### 3.5 Common-learning chain

```text
coarse six-axis product experiment
  -> estimate x=r u
  -> data-dependent low/high contrast branch

low contrast
  -> variance-sensitive product estimate of direction
  -> fresh +/- estimated-axis endpoint data
  -> Hellinger endpoint control
  -> d_N loss O(delta)

high contrast
  -> GHZ input + independent fair sign
  -> exact cancellation of unknown bias
  -> two complex transverse powers
  -> dyadic accepted block scales
  -> first rejection identifies noise scale
  -> fine two-plane phase estimate
  -> fresh endpoint samples
  -> d_N loss O(delta)

scalar Bernoulli subfamily
  -> future-N separation at Delta ~ delta/sqrt(N)
  -> every adaptive training record is postprocessing of iid bits
  -> KL testing lower bound
  -> M >= c N delta^(-2) log(1/eta)
```

---

## 4. Matrix metric audit

### 4.1 Tangent identities

For interior `G`, `S=sqrt(G(I-G))` commutes with both square-root factors. The proposed derivatives satisfy

\[
 A_1^*B_1+B_1^*A_1=SK+KS,
\]

\[
 A_0^*B_0+B_0^*A_0=-(SK+KS),
\]

\[
 \sum_yA_y^*B_y=0,\qquad
 \sum_yB_y^*B_y=K^2.
\]

The gauge

\[
 T_y=(B_y-R_y'(0))R_y(0)^{-1}
\]

is anti-Hermitian because differentiating `R_y(s)^2=G_y(s)` cancels the Hermitian part after multiplication by `R_y(0)` on both sides. Thus the tangent is realized by actual isometries.

### 4.2 Adaptive orthogonality

For two distinct differentiated slots, common isometries after the later slot cancel in the overlap. The remaining factor contains `W*dot W` or its adjoint and is zero as an operator. The proof therefore obtains a square-root sum of slot norms rather than a linear sum. This remains valid with reference systems and coherent control of classical histories.

Public stopping is covered by padding with ignored fixed-input calls. The dummy outputs must not be made part of the operational output, and the proof observes this convention.

### 4.3 Residual hybrid term

For the residual `R=N^(-1/2)K`, one call has two opposite reference blocks. Their total unhalved trace norm is at most `2||R||op`. Inserting the tangent in each slot and contracting through all later common channels gives `2N||R||op`. Combining with the horizontal term gives `4sqrt(N)||K||op`.

In a spectral basis of `G`,

\[
 K_{ij}=\frac{H_{ij}}
 {\sqrt{v_i}+\sqrt{v_j}+N^{-1/2}}.
\]

The denominator squared dominates `v_i+v_j+1/N`, so the Hilbert–Schmidt norm of `K` is controlled by the declared quadratic form.

### 4.4 Path integration and boundary

The output path of each fixed tester is absolutely continuous with the stated derivative bound. Integrating before taking the tester supremum is legitimate. The inward regularization of a closed-body path supplies a uniform integrable bound at fixed `N`; the hybrid inequality gives convergence of endpoint distances.

### 4.5 Midpoint comparison

For the straight segment, operator concavity gives the precise factor `2min(t,1-t)`. Left-plus-right multiplication preserves Loewner order as a quadratic form on Hermitian matrices. Inversion reverses it. The singular endpoint factor is integrable and gives exactly the additional factor two in the path length.

### 4.6 Diagonal lower witnesses

If `m_i` is a midpoint eigenvalue and `H_ii` the diagonal change, the two Bernoulli probabilities have variances whose sum is at most `2m_i(1-m_i)`. The v75 finite Bernoulli theorem therefore controls the weighted diagonal entry with no positive variance assumption.

### 4.7 Off-diagonal lower witnesses

Compression to `span{e_i,e_j}` is a legal fixed input embedding. The compressed midpoint is diagonal, and the identity

\[
 V_M=\frac12V_E+rac12V_F+rac14(F-E)^2
\]

bounds its variance trace below by either endpoint variance. The scalar component of the compressed difference has no off-diagonal entry. Its traceless component yields the spectral-plus-angular control required to invoke the v75 theorem. Scalar compressed effects are handled without fictitious directions.

### 4.8 Dimensional factor

The weighted Hilbert–Schmidt norm contains `d^2` entries. Hence one entry is at least `Q_N/d`. No stronger dimension dependence is proved. The corollary comparing adaptive and nonadaptive values inherits this factor and should not be advertised as dimension-uniform.

No fatal gap was found in this chain.

---

## 5. Entropy audit

### 5.1 Local normalized perturbation

With `W_E=E(I-E)+tau I/2`, diagonalization gives

\[
 \|W_E^{-1/2}HW_E^{-1/2}\|_{HS}\le2g_{N,E}(H).
\]

The exact expansion of `W_(E+tH)-W_E` has a normalized linear term of size `O(|t|q)` and a quadratic term of size `O(t^2q^2)`. For small `q`, this gives two-sided Loewner comparison and determinant-density comparison.

### 5.2 Metric/form inclusions

The global metric lower bound first makes the midpoint modulus small; the local comparison then transfers it to an endpoint form. Conversely, a small endpoint form transfers to the midpoint form and then to the metric upper bound. The order of these implications is correct.

### 5.3 Boundary lower ellipsoid

At a projection, a centred ambient ellipsoid is mostly illegal. The proof avoids this issue. It moves inward by `s=ar/N`, pays only `O(r)` in the form, and proves both `E_s+X>=0` and `I-E_s-X>=0` for every point of a smaller full ellipsoid. Its weighted measure is comparable to `r^(d^2)`.

### 5.4 Determinant density

There are `d` diagonal real directions with weights `N/(2w_i)` and two real directions for every complex off-diagonal pair with weight `N/(w_i+w_j)`. Taking the square root of the determinant yields total power `N^(d^2/2)` and the stated product density.

### 5.5 Spectral integral upper bound

In an ordered depth sector, a same-endpoint pair contributes at most one positive power of the larger depth, while an opposite-endpoint pair contributes its reciprocal. Together with the individual square-root factors, the exponent at the `j`th depth is `a_j-1`, where

\[
 a_j=\frac12+\epsilon_jS_{j-1}.
\]

The cumulative exponent telescopes to `S_j^2/2`. Logarithmic variables reduce the integral to a simplex with exponentially damped positive-prefix coordinates and undamped zero-prefix coordinates. There can be at most `floor(d/2)` zero prefixes.

### 5.6 Matching lower bound

Pairing one eigenvalue near zero with one near one at each selected depth gives one constant contribution per scale. Cross-interactions between two separated pairs contain two same-endpoint factors and two opposite-endpoint factors whose depth powers cancel. The number of increasing scale tuples is of order `log(N)^(floor(d/2))`.

### 5.7 Covers and rational centres

Uniform upper ball measure proves the converse against arbitrary legal centres. A maximal separated set and uniform lower ball measure prove the upper cover. Rational replacement uses an inward move and fixed-horizon continuity. It gives existence, not computational complexity.

No fatal gap was found in this chain.

---

## 6. Common-learning audit

### 6.1 Endpoint metric and concentration

The Bernoulli square-root distance controls the `N`-fold product trace norm uniformly at support endpoints. Bernstein's inequality gives the required square-root-variance plus linear-error form. Sorting in the `arcsin sqrt` coordinate preserves ordered endpoint accuracy.

### 6.2 Product regime

The Pauli-axis half-differences estimate the Bloch vector. The feasibility inequality `|b|+r<=1` implies the low-contrast variance comparison used to control the angular coefficient. Endpoint misalignment is second order in the angular error and is absorbed into fresh endpoint concentration. The returned spectral pair is sorted and therefore legal.

### 6.3 GHZ parity identity

For `O=2E-I=bI+x·sigma`, a fresh fair sign in the GHZ coherence causes the sign-weighted parity to eliminate the two diagonal powers and retain the desired off-diagonal complex power. The observation remains bounded in `[-1,1]`. Two phases and two transverse planes determine both local angular coordinates.

### 6.4 Safe cone and phase

The induction maintains `h<=2a/m` before testing length `m`. This keeps `m theta_i` strictly inside the principal phase interval and makes each complex amplitude comparable to `r^m`. The reconstruction map from the two divided phases to a unit direction is locally Lipschitz.

### 6.5 Block selection

On the simultaneous good event:

- length one is accepted in the high-contrast branch;
- acceptance implies `r^m` is bounded below and updates the angle to `O(1/m)`;
- first rejection implies the preceding accepted scale is comparable to `(1-r)^(-1)`; and
- reaching the cap gives a scale comparable to `N`.

The proof requires the procedure to stop on the **first rejection**. The current prose says to retain the preceding accepted length but does not state termination with sufficient precision. Continuing to larger scales would violate the pre-stage cone invariant. This is a specification blocker for publication, not a counterexample to the intended algorithm.

### 6.6 Confidence and worst-record cost

The stage allowances are conditional on the preceding good record. Their union bound uses only the sum of the tested powers of two. The same public caps bound cost on exceptional records. The weighted logarithmic sum is `O(N log(1/eta))` and introduces no `log log N` factor.

### 6.7 Fine estimate

The selected scale satisfies `m_*(V+1/N)>=c`. The final complex tolerance therefore translates to `K_N h=O(delta)`. Fresh axis-aligned endpoint groups have sample size `O(N delta^(-2) log(1/eta))` and give Hellinger error `O(delta/sqrt N)`.

### 6.8 Lower bound

For scalar effects, outcomes are independent of every chosen input and the retained reference state factors from the parameter-dependent Bernoulli law. Adaptive controls and stopping are common postprocessings. Future-`N` separation requires a parameter gap of order `delta/sqrt N`; the training KL is order `M delta^2/N`. Testing therefore forces the claimed lower bound.

### 6.9 Coding consequence

Rational approximation and inward rescaling make the real estimate a legal rational qubit effect. The one-use identity plus the hybrid inequality bounds this postprocessing loss. The inherited exact codec then supplies one reusable word. Device calls, payload, arithmetic, and workspace remain separate.

The theorem receives a qualified pass pending explicit first-rejection pseudocode.

---

## 7. Inherited dependencies and preservation

The complete v76 graph preserves every one of the 557 mathematical labels active in the v75 complete edition. The focused articles preserve their respective predecessor proof graphs. The structural companion remains independently buildable.

The new matrix converse legitimately depends on the active v75 biased-qubit theorem. The common learner also depends on the v75 angular upper bound, aligned spectral programme, and exact codec. These dependencies are present in the active source package rather than only in historical PDFs.

The following inherited boundaries remain unchanged:

- v65–v66 numerical instrument simulation concerns supplied rational data and charged streaming resources;
- v67–v72 description theorems have their own interior, rank, input-basis, readout, and seizing hypotheses;
- v73 treats public visibility and pair-dependent finite angular witnesses;
- v74 treats the complete unbiased qubit ball and regular target subsets;
- v75 treats the complete biased qubit body and its exact rational code;
- the structural companion uses fresh nondisturbing classical probes, not destructive quantum-measurement reuse.

Preservation is not a new independent validation of every inherited theorem.

---

## 8. Build, finite evidence, and provenance

The committed build receipt records:

- focused quantitative paper: 69 pages;
- structural companion: 41 pages;
- complete research edition: 174 pages;
- 658 active complete-edition labels;
- 557 preserved predecessor labels;
- 266 preserved predecessor native files;
- 296 source files in the v76 object;
- successful isolated rebuild;
- no recorded LaTeX diagnostics for the three entry points; and
- identical normal and optimized Python results.

The new matrix regression reports 3,293 exact assertions covering scalar, Bernoulli, qubit-compatibility, noncommuting matrix, unitary-covariance, repeated-midpoint, PSD, Sylvester, horizontal-gauge, and CLI cases. Its negative controls reject malformed matrices, false certificates, altered moduli, incorrect normalization, and target substitution.

The common-learning regression reports 118,584 exact checks and 93 negative controls. It covers GHZ tensor identities, random-sign cancellation, outcome normalization, endpoint alignment, variance bounds, dyadic budgets, stage failure allowances, block caps, and legality fixtures. It explicitly states that it is not a stochastic implementation of the learner or a probability-risk certificate.

The exact final-head workflow run `37198984154` successfully:

1. checked out the exact submitted SHA;
2. installed the declared dependencies;
3. rebuilt the submitted sources and every PDF page read-only;
4. independently rebuilt the focused journal package; and
5. preserved the source-bound reconstruction evidence.

These checks establish source identity, reproducibility, and extensive finite regression. They do not prove continuum inequalities, the adaptive supremum, minimax risk, novelty, authorship, or journal acceptance.

The relevant commits are unsigned. No human cryptographic signature is supplied or inferred.

---

## 9. Literature and priority audit

The active comparison now covers the neighboring measurement-discrimination papers requested in r49 and distinguishes outcome count, ancilla access, number of uses, and perfect-versus-quantitative discrimination.

It also credits the main methodological antecedents:

```text
horizontal Kraus geometry
  -> Fujiwara–Imai and channel-QFI methods

adaptive channel-extension bounds
  -> Demkowicz-Dobrzanski and collaborators

finite-pair path integration
  -> Yuan–Fung and later adaptive-discrimination work

inverse Sylvester / Bures tensor
  -> Dittmann and matrix-geometry literature

spectral integration
  -> standard Hermitian eigenvalue Jacobians and Bures-volume methods

measurement/channel tomography
  -> current finite-sample POVM and diamond-distance channel learning

multiscale phase estimation
  -> increasing-power phase-estimation and robust calibration methods
```

The precise claims still requiring independent priority review are:

1. the closed-body midpoint-resolvent comparison with a matching nonadaptive converse;
2. the total regularized matrix-effect volume and its `floor(d/2)` logarithmic multiplicity;
3. the resulting operational covering law; and
4. the sharp future-`N` qubit learning rate under the stated training model.

Mele–Bittel's current diamond-distance channel-learning work includes measurement channels as special cases. Zambrano–Ramos-Calderer–Kueng give finite-sample POVM tomography in one-use operational losses. Sieniawski–Demkowicz-Dobrzanski connect adaptive channel discrimination with metrological bounds. These are direct constraints on novelty language, even though none of the checked statements directly supplies the v76 finite-horizon matrix entropy.

No independent specialist opinion is present. The author-side bounded search cannot establish absence of equivalent results.

---

## 10. Separation from the A/B/C/D analytic programme

The frozen Round-Seventeen dependency graph remains

```text
A1 independent
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The unresolved gates include, among other things:

- unsmoothed raw local limits;
- predictable-control stopped-path entropy and LDP recovery;
- a global past kernel;
- exact canonical coefficients and shell conditioning;
- process CLT and independent quadratic Mosco recovery;
- nonlinear Nisio resolvents and graph cores;
- regular filtering and QMD/LAN;
- changing-filtration response; and
- labelled posterior contraction.

The v76 results do not close these gates:

```text
bounded public stopping in a tester
  != predictable-control stopped-path LDP

matrix-effect boundary volume
  != Mosco recovery or nonlinear semigroup convergence

horizontal finite-dimensional dilation
  != filtering/LAN or changing-filtration response

common qubit learner
  != labelled posterior contraction in the historical models

exact codec regression
  != analytic A/B/C/D closure
```

The flags for historical A2 replacement, B4 aggregate, C2 aggregate, the eleven-paper aggregate, and the whole Theta programme remain false. This audit makes no change to them.

---

## 11. Risk register

### Publication blocker P0

**P0-1 — dyadic first-rejection semantics.**  
The high-contrast learner must explicitly stop at the first rejected block length and return the preceding accepted scale. Add pseudocode and prove the invariant against that exact control flow.

### Major P1 items

**P1-1 — independent priority.**  
The closest 2025–2026 channel/measurement learning and adaptive-discrimination papers require direct specialist comparison.

**P1-2 — novelty language.**  
Do not claim first common measurement tomography or first path-integrated adaptive bound.

**P1-3 — fixed-dimensional scope.**  
Constants and error caps depend on `d`; no dimension-uniform regime is proved.

**P1-4 — learner dimension.**  
The sharp learner is qubit-only and must not be merged rhetorically with the arbitrary-dimensional geometry.

**P1-5 — constructive status.**  
Arbitrary-dimensional rational centres exist, but no optimal matrix encoder is implemented.

**P1-6 — journal-facing length.**  
The 69-page focused article should move most inherited supporting material to a companion or supplement.

**P1-7 — finite evidence boundary.**  
The common-learning checks are not a full stochastic implementation or uniform risk verification.

### Minor P2 items

**P2-1.** Keep unhalved trace norm and classical TV factors explicit.  
**P2-2.** State reference access in every definition of `d_N^na`.  
**P2-3.** Keep scalar compressed effects free of artificial directions.  
**P2-4.** State that the adaptive/nonadaptive constant is unoptimized.  
**P2-5.** Keep rational-centre density distinct from bit complexity.  
**P2-6.** State that workflow hashes are unsigned reproducibility records.

No fatal mathematical blocker was identified.

---

## 12. Recommended acceptance gates for the next submission object

A specialist-ready successor should satisfy all of the following:

1. preserve the exact v76 theorem statements or strengthen them with complete proofs;
2. specify the high-contrast learner as executable pseudocode with first-rejection termination;
3. include one explicit confidence/resource ledger;
4. complete an independent priority comparison of the four new theorem objects;
5. compare theorem-by-theorem with current channel and POVM learning results;
6. keep arbitrary-dimensional geometry, qubit learning, and qubit coding visibly separate;
7. retain the operational-ball proof before invoking spectral volume;
8. identify rational-centre existence as nonconstructive in general dimension;
9. compress the journal-facing manuscript without deleting the archived proof corpus;
10. rebuild the exact final submitted SHA and its self-contained journal package;
11. preserve all false A/B/C/D aggregate flags; and
12. avoid representing finite regression, workflows, or hashes as mathematical certification.

---

## 13. Final independent verdict

Revision 76 materially changes the assessment of General Theta Foundations I. The local quantitative paper now contains an arbitrary-fixed-dimensional matrix theorem, a matching all-strata entropy law, and a separate sharp common learner. The proof architecture is coherent, the declared interfaces are mostly disciplined, and the reproducibility package is unusually extensive.

The central mathematical classification is:

```text
matrix midpoint comparison:             PASS
adaptive path upper bound:              PASS
one-/two-dimensional converse:          PASS
all-rank spectral noncancellation:      PASS
uniform operational-ball volume:        PASS
nested endpoint spectral integral:      PASS
full fixed-d covering law:              PASS
common qubit learning upper bound:      QUALIFIED PASS
common qubit learning lower bound:      PASS
arbitrary-d efficient code:             NOT CLAIMED / OPEN
independent priority clearance:         OPEN
A/B/C/D aggregate closure:              OPEN
top-four general-journal threshold:     NOT MET IN R50 JUDGMENT
```

The only direct proof-procedure correction required is to state first-rejection termination in the dyadic learner. The remaining objections concern priority, scope, construction, and editorial significance rather than a discovered false theorem.

**Independent audit conclusion: mathematically credible and specialist-significant; not certified for priority, not a whole-program closure, and not recommended for the four leading general mathematics journals.**
