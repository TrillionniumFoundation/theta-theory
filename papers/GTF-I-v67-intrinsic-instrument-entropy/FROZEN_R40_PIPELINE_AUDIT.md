# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 61 (r40)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed final head:** `2c215579336a253585499328f19a647446445dc4`  
**Candidate publication:** `36a75595e46da636bd967b0d30f6395fdc05d029`  
**Qualified native source:** `776ba0fec6ec7ddd57a5fc188764763700cd5008`  
**Predecessor:** Revision 59 final head `310dabfa4020a7c4da2d7999c59ea692dede7850`  
**Prior reports:** `6daa50db42873a4a32cd3c1610f19630f5739b51`, `849cbc2fb4d589d8fd13d8c7d34492af191e0f75`  
**Builder run:** `36378348045`  
**Read-only final-head run:** `36378669691`  
**Audit branch:** `review/general-theta-foundations-i-v61-proof-pipeline-audit-r40-2026-09-28`  
**Date:** 28 September 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest revision identity | **Pass.** Both advertised v61 branches point to `2c215579...`; no higher GTF-I revision was located. |
| Source genealogy | **Pass.** Native source -> candidate publication -> final request is a direct three-commit chain. |
| Spectral-entropy proof | **Pass with stated hypotheses.** No fatal gap found in smoothing, entropy defect, centroid transport, or occupation telescoping. |
| Logarithmic-loss claim | **Pass.** The multiplicative logarithm is removed; only an additive initial entropy range remains. |
| LPS constant | **Pass as imported primary theorem.** The exact six-rotation norm is `sqrt(5)/3`. |
| Effective width theorem | **Pass.** The displayed numerical lower and constructive upper constants follow from the stated estimates. |
| Exact `5^t` profile | **Pass.** The orbit is a right-coset ball with cyclic stabilizer; the denominator lattice proves the robust interval. |
| Revision 59 causal classification | **Pass in the repeatable-probe model.** No fatal gap found in the common-itinerary or finite-cut testing argument. |
| Adaptive compiler | **Pass with strict-positive-probe hypothesis.** The path-law KL and dyadic-kernel arguments are coherent. |
| Inherited terminal structure | **Pass in previously stated scope.** Stationarization, purification, and finite-action criteria remain hypothesis-sensitive. |
| Finite tests | **Regression evidence only.** They do not prove universal entropy or spectral assertions. |
| Source reproducibility | **Pass.** Exact-final-head read-only reconstruction succeeded. |
| Cryptographic authorship | **Not supplied and not claimed.** |
| Independent novelty closure | **Open.** The literature audit remains author-side. |
| A/B/C/D analytic closure | **Open.** Every aggregate flag remains false. |
| Four-leading-journal significance | **Not established.** This is separate from correctness. |

The local Revision 61 proof package is substantially stronger than the one reviewed in r39. The main new theorem chain appears mathematically coherent. The repository-wide analytic program remains independent and incomplete.

---

## 1. Frozen review object

The reviewed branches are:

```text
revision/general-theta-foundations-i-v61-sharp-width-2026-09-28
revision/general-theta-foundations-i-v61-referee-ready-2026-09-28
```

Both point to:

```text
2c215579336a253585499328f19a647446445dc4.
```

The final commit adds only `GENERAL_THETA_FOUNDATIONS_I_V61_FINAL_HEAD_REQUEST.json`. It pins:

```text
candidate publication: 36a75595e46da636bd967b0d30f6395fdc05d029
native source:          776ba0fec6ec7ddd57a5fc188764763700cd5008
builder run:            36378348045
```

The final-head verifier checks that the request is the direct successor of the candidate publication and that the publication is the direct successor of the native source. The two present r40 branches were created directly from the reviewed final head and modify no manuscript or historical review branch.

The source predecessor is Revision 59, not Revision 58. Revision 60 is recorded only as an unused preparation anchor and supplies no theorem premise. Because no separate Revision 59 referee report was found, its causal theorems were independently inspected for this audit.

---

## 2. Active proof dependency graph

### 2.1 Sharp terminal-width chain

```text
full Koopman/action L2 gap off invariant functions
  + all-direction orbit-cap estimate
  -> fixed entropy defect for a density supported in k small caps

compactly supported spherical kernel
  -> pointwise density bound
  -> finite Fisher information despite zeros
  -> entropy continuity under W2 transport of centers

actual stochastic transition rows
  -> exact weighted-centroid flow identity
  -> monotone total centroid mass
  -> W2 transport cost paid by centroid-mass loss

wordwise terminal correctness
  + legal decoder norm <= 1
  -> residual centroid mass zeta

selected narrow cuts
  + one random physical letter per gap
  + arbitrary hidden processing on identity fillers
  -> entropy telescope across selected cuts
  -> O(k^(2/p)) occupation
  -> Omega(N^(p/2)) horizon width

quadratic inner orbit hull
  -> O(N^(q/2)) common-row upper machine

p=q
  -> Theta(N^(q/2)) fixed-positive-error width
```

### 2.2 Effective LPS chain

```text
six norm-five Lipschitz-quaternion rotations
  + imported LPS Koopman norm sqrt(5)/3
  + exact S2 cap and smoothing constants
  -> numerical linear occupation and lower-width constants

free quaternion triple
  + cyclic stabilizer of first-axis seed
  -> right-coset ball cardinality 5^t
  + extreme density-matrix outputs
  -> exact simultaneous cut profile 5^t

rational denominator-five orbit lattice
  -> target separation at cut t
  -> same profile for epsilon <= 25^(-N)/16

generic rational compiler
  -> sparse rational rows
  -> legal density-matrix decoders
  -> dyadic hidden transitions
  -> O(N/epsilon) constructive upper width
```

### 2.3 Repeatable-process chain

```text
future-response functions
  + compact group action
  -> finite behavioral quotient iff open-normal coset quotient

finitely many distinct types
  -> one common separating control itinerary
  -> repeated nondisturbing probes
  -> disjoint high-probability output events

causal finite cut register
  -> common suffix mixture by cut label
  -> width >= m(1-epsilon-delta)
  -> exact m-label lower bound below error 1/2

finite future-response quotient
  -> exact stationary permutation commands
  -> state-preserving fresh probe emissions
  -> exact adaptive transcript law
```

### 2.4 Adaptive compiler chain

```text
rational spherical inner hull
  -> sparse common rotation rows

physical/hidden geometric coupling
  -> E||V_t-X_t||^2 <= 2t/m^2

strictly positive affine probes
  -> conditional KL <= A||V-X||^2/eta
  -> trajectory KL chain rule under adaptive policies
  -> whole-transcript TV bound

joint-kernel dyadic rounding
  -> first-discrepancy coupling
  -> additional path TV budget
```

None of these chains invokes an open A/B/C/D analytic gate.

---

## 3. Claim-by-claim proof status

| Claim | Location | Audit status | Essential hypotheses |
|---|---|---|---|
| Spherical entropy continuity | `lem:smoothentropy61` | No fatal gap found | Fixed finite dimension; compactly supported `C^1` kernel; finite-center laws. |
| Spectral entropy defect | `lem:entropydefect61` | No fatal gap found | Full action `L^2` gap off all invariants; thin orbitwise support. |
| Centroid-loss transport | `lem:centroidtransport61` | No fatal gap found | Actual Markov row depends only on retained label/current command; residual mass positive. |
| Sharp occupation | `thm:sharpoccupation61` | No fatal gap found | Identity command or exact-return extension; full action gap; all-direction cap law; legal unit-ball decoder. |
| Matching power law | `cor:matchedorbits61` | Correctly scoped | Fixed positive subcritical error; equality of lower and target dimensions. |
| Exact LPS gap | `lem:lpsgap61` | Verified as imported theorem | Uniform measure on six nonidentity norm-five rotations. |
| Effective linear law | `thm:effectivelps61` | No fatal gap found | Qubit legal outputs; LPS gap; fixed positive error. |
| Exact/robust `5^t` profile | `thm:effectivelps61` | No fatal gap found | Pure-state legal outputs; free group; cyclic stabilizer; rational lattice. |
| Causal finite quotient | `thm:causalclassification59` | No fatal gap found | Compact group; repeatable fresh probes; whole-transcript TV; adaptive policy. |
| Adaptive rational compiler | `thm:adaptivecompiler59` | No fatal gap found | Rational rotations/unit seed; affine probes uniformly bounded below. |
| Effective process lower | `thm:processlower59` | No fatal gap found | Repeated coordinate probes consume explicit horizon; exponent not claimed sharp. |
| Same-width stationarization | `thm:stationarization56` | Inherited, scope preserved | Eventual approximate returns. |
| Stochastic purification | `thm:purification55` | Inherited, scope preserved | Stationary finite labels; compact physical group; terminal convex outputs. |

---

## 4. Detailed audit of the entropy proof

### 4.1 Full-action gap versus finite-dimensional contraction

The theorem uses

```text
||P f - Pi f||_2 <= kappa ||f-Pi f||_2
```

on the entire function space of the sphere. The range of `Pi` is the full invariant subspace. In a nontransitive action this may be larger than the constants. The proof does not collapse these two objects.

A contraction of the original vector representation would not be enough: high harmonics can be nearly invariant. The manuscript explicitly preserves this distinction. When a regular-representation gap is available, Peter--Weyl decomposition transfers the same bound to nontrivial irreducible blocks of the action. This implication is legitimate, including the inverse convention after taking the adjoint.

### 4.2 Spherical kernel estimates

Let `s=||x-u||^2`. In local polar coordinates the distribution of `s` behaves as `s^((m-3)/2)` at zero. The normalizing constant is therefore comparable to `h^(m-1)`. Differentiating the squared cutoff yields Fisher information `O(h^-2)`. Mixture Fisher information is bounded by the mixture of component informations through pointwise Cauchy--Schwarz.

The entropy lower bound is Jensen relative to normalized round measure. The pointwise density bound gives the upper entropy range.

For the transport bound, paired centers follow shortest geodesics. Rotation invariance supplies the continuity equation. The flux energy is bounded by the optimal center coupling cost. Entropy differentiation is regularized by adding a uniform positive density; the limiting argument is valid because the kernel is bounded and `x log x` is continuous at zero.

No pointwise lower bound on the mixture density is used.

### 4.3 Thin-support entropy defect

If `f` is supported in `A`, then orbitwise Cauchy--Schwarz gives

```text
(Pi sqrt(f))^2 <= (Pi 1_A)(Pi f).
```

The invariant component of `sqrt(f)` is therefore small when every orbit spends at most `theta` mass in `A`. The spectral gap controls the orthogonal component. The Hellinger lower bound for Jensen entropy loss yields the fixed defect.

The proof does not assume self-adjointness of `P`; it uses the declared operator norm and the identities `P Pi=Pi P=Pi`. It also does not use log-Sobolev or pointwise total-variation mixing.

### 4.4 Directional law and transport

The direction law is not the hidden-label distribution. It is normalized from weights

```text
p_s ||E[X|S=s]||.
```

This choice is forced by the flow identity. For each output label `i`, the incoming weighted unit vectors sum to the new centroid vector. Expanding squared chordal distances gives exactly `2(q_i-m_i)`. Summing proves that centroid mass cannot increase.

One coupling transports the rotated old directional law to the normalized incoming-direction law at the new labels. A second coupling moves excess mass to the normalized new centroid law. The sphere diameter and chordal/geodesic comparison give the stated constant `3 pi^2`.

Zero centroids contribute no mass; zero-probability labels never enter a division.

### 4.5 Terminal residual mass

The target is a unit orbit vector scaled by `rho`. For each deterministic external word, correctness of the conditional mean output gives an inner product at least `rho-epsilon`. Averaging over the external word distribution and conditioning on the terminal hidden label yields

```text
zeta <= sum_i p_i <E[X|S=i],D_i> <= alpha_terminal,
```

because every legal decoder has norm at most one. This is a statement about conditional means, not per-label pointwise correctness.

Monotonicity through the final fixed suffix implies every selected cut has centroid mass at least `zeta`.

### 4.6 Narrow-cut telescope

Each selected cut has at most `k` nonzero centroid directions. The smoothed law is supported in a union of `k` chordal caps. The all-direction cap bound implies that the orbitwise average of the support indicator is at most one half when `h=c k^(-1/p)`.

Thus every selected gap loses at least `gamma` entropy before stochastic hidden merging. The merging can restore entropy only by transporting directions, and that transport is paid for by the centroid mass lost in the same gap. Total lost centroid mass over all gaps is at most `1-zeta`.

The resulting inequality is

```text
gamma M <= L_h + C h^(-1) sqrt(M(1-zeta)/zeta).
```

It gives `M=O(h^-2)`. Since `L_h=O(log k)` is additive, it does not create a multiplicative log in the final width power.

### 4.7 Synchronization boundary

The proof inserts exactly one random physical letter in each selected gap and fills the remainder with the physical identity. The hidden identity row may be arbitrary. If no identity letter exists, the stated extension requires exact identity products at every sufficiently large length. An approximate-return word changes the physical direction and would require a new quantitative error budget; it is correctly excluded.

---

## 5. Effective LPS audit

### 5.1 Primary imported result

The six nonidentity matrices are the adjoint rotations of the norm-five quaternion set used by LPS. The primary restatement by Pinochet Lobos and Pittet states that the subgroup is free of rank `(p+1)/2` and that the one-step discrepancy on the round sphere equals

```text
2 sqrt(p)/(p+1).
```

At `p=5`, this is exactly `sqrt(5)/3`. The manuscript's numerical `kappa` is therefore correct.

The identity letter used for padding is not included in the uniform six-letter spectral measure.

### 5.2 Exact constants

For normalized `S^2`, chordal squared distance has constant density `1/4` on `[0,4]`. Therefore:

```text
cap area = h^2/4,
D_3 = 12,
B_3 = 24.
```

With `h=k^-1/2`, `theta=1/4`, and `kappa^2=5/9`, the entropy defect is `1/3`. Substitution into the general occupation proof gives the displayed coefficients `6` and `648 pi^2`. The simplification to `6500 k/zeta` is valid but intentionally loose.

### 5.3 Density of the action

Each coordinate-axis generator has rotation cosine `-3/5`. If its angle were a rational multiple of `2pi`, twice the cosine would be a rational algebraic integer and hence an integer, contradicting `-6/5`. Thus powers are dense in each coordinate circle. The three coordinate circles generate `SO(3)`.

This direct argument is independent of finite word enumeration.

### 5.4 Stabilizer and coset count

The free generators are denoted `a,b,c`, with `a` rotating around the first axis. An element fixing the first-axis vector commutes with `a`. The centralizer of the primitive generator `a` in the free group is `<a>`. Hence the stabilizer is exactly cyclic.

The orbit is indexed by right cosets of `<a>`. Removing the maximal terminal `a`-power gives a unique shortest representative that ends in one of the four letters `b^(+/-1),c^(+/-1)`. At length `ell>=1` there are `4*5^(ell-1)` such representatives. The radius-`t` coset ball has exactly `5^t` elements.

### 5.5 Robust lattice separation

Every product of `t` rational rotations has entries in `5^-t Z`. Distinct reachable vectors therefore differ in at least one coordinate by at least `5^-t`. One fixed suffix preserves Euclidean distance. Small Frobenius error forces a positive-mass conditional decoder mean into a cap of radius `sqrt(2 sqrt(2) epsilon)`. At `epsilon<=25^-N/16`, twice this radius is strictly smaller than every relevant cut separation.

The exact deterministic orbit machine attains the entire profile simultaneously.

### 5.6 Compiler bound

The existing rational spherical net and exact triple solver apply to the supplied seven rotations. The amplitude slack and dyadic rounding budgets fit inside the requested Frobenius tolerance. The real-tolerance bound uses a rational tolerance strictly between `epsilon/2` and `epsilon`, which accounts for the factor `104` rather than `52`.

---

## 6. Causal proof audit

### 6.1 Behavioral types

The future-response map contains all future left physical translations and all probe coordinates. It is a compact behavioral invariant. Finite cardinality yields a continuous permutation action of the compact group on the finite type set. The action kernel is open normal, and exact type labels provide a stationary causal realization.

This is a behavioral quotient, not linear predictive rank. The manuscript correctly avoids inferring the theorem from finite Hankel or PSR dimension alone.

### 6.2 Positive-word executability

The positive semigroup generated by the command alphabet is dense in the compact generated group because inverses are limits of positive powers. Therefore every separation visible at a group element can be approximated by an executable positive word while preserving strict inequality of a probe coordinate.

### 6.3 Common itinerary

Distinctness of future types is preserved under a common command continuation. Processing all pairs sequentially therefore constructs one shared itinerary. Repeated probes at each recorded location generate empirical-frequency vectors whose neighborhoods are disjoint for all selected initial types.

The proof uses fresh conditional probe samples and leaves the physical state unchanged during repetition.

### 6.4 Cut-register test

Given cut label `z`, causality makes the suffix output law `Q_z` independent of the chosen prefix after the prefix output history has been marginalized. Whole-transcript TV contracts under marginalization. The target high-probability event lower bound therefore transfers to the approximate suffix mixture.

Summing over disjoint events bounds the number of labels. If success exceeds one half, one label cannot serve two events. This gives the eventual exact minimum below error one half.

### 6.5 Model boundary

The theorem does not extend automatically to destructive probes, nonrepeatable observations, general irreversible dynamics, or noncommuting quantum measurements. Those are not presentation details; repeatability is the mechanism that amplifies behavioral distinctions and pads horizons.

---

## 7. Adaptive compiler audit

### 7.1 Hidden geometry

The rational inner-hull construction gives a sparse stochastic row whose conditional mean is `r A_a v`. The hidden point is always zero or a unit net point, plus the supplied rational unit seed. The second-moment recursion is valid even when the zero label persists.

### 7.2 Auxiliary path law

Under the auxiliary law, hidden labels follow the constructed rows but probes emit according to the true physical point. The public process is therefore exactly the target experiment under the same adaptive policy. The auxiliary law is used only in the proof and is not claimed as the implemented machine.

### 7.3 KL accumulation

Uniform positivity `q_y(v)>=eta` gives

```text
D(q(X)||q(V)) <= A ||X-V||^2 / eta.
```

The policy and hidden-transition factors cancel in the trajectory relative-entropy chain rule. The unconditional moment bound is enough; no posterior approximation after a rare transcript is assumed.

### 7.4 Dyadic joint kernels

Probe probabilities and hidden transitions are rounded as actual nonnegative joint kernels. Under a common policy-randomness coupling, paths agree until the first one-step kernel discrepancy. The whole-transcript TV cost is therefore at most the sum of one-step row TV errors.

The fair-bit total includes classical probe emissions in the causal mode.

---

## 8. Regression and implementation evidence

The Revision 61 checker reports 4,112 exact finite assertions and 13 named negative controls, executed in normal and optimized Python. It checks finite algebra, row identities, variance and transport calculations on test instances, compiler examples, rational lattice properties, and transcript laws.

The tests do **not** prove:

- the universal entropy-continuity lemma;
- the universal centroid transport lemma;
- the full action spectral gap;
- the LPS/Deligne theorem;
- the infinite free-group statements beyond their written proof;
- independent priority; or
- four-journal significance.

The compiler examples include default terminal, generic terminal, generic causal, LPS terminal, and LPS noisy configurations. Every accepted geometric row is rechecked by exact rational barycentric equality. Optional SciPy only proposes candidate facets; exhaustive rational triples remain the fallback.

The implementation is pseudo-polynomial in the numerical horizon and inverse accuracy. It is not a minimum-width solver and is not advertised as practical for large horizons.

---

## 9. Build and final-head verification

### 9.1 Source-bound builder

The build receipt identifies:

```text
source commit:       776ba0fec6ec7ddd57a5fc188764763700cd5008
predecessor:         310dabfa4020a7c4da2d7999c59ea692dede7850
native source files: 344
predecessor files:   285
quantitative pages:  29
structural pages:    36
complete pages:      76
```

It records source hashes, document hashes, compiler outputs, inherited regression suites, isolated reconstruction, page-text equality, page-raster equality, and normal/optimized agreement.

### 9.2 Exact final-head verifier

The workflow has only:

```text
permissions:
  contents: read
```

It checks out `${{ github.sha }}` with credentials disabled. The verifier requires `HEAD==GITHUB_SHA`, validates the direct commit genealogy, checks the builder identity, verifies the native archive inventory and every source hash, reconstructs in a temporary directory, compares page and compiler receipts, reexecutes regressions, and confirms that tracked repository files remain unchanged.

The exact final head triggered run `36378669691`; the job and all steps completed successfully. This resolves the final-head status limitation recorded for Revision 58.

### 9.3 What CI does not certify

The attestation explicitly excludes:

- universal mathematical proofs;
- independent priority;
- cryptographic author signature;
- journal acceptance; and
- A/B/C/D analytic closure.

This separation is appropriate.

---

## 10. Pipeline separation

The frozen analytic graph remains:

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent
```

Open obligations still include:

- raw unsmoothed local limits;
- stopped-path entropy and large deviations;
- a global past kernel and weak-Harris control;
- canonical shell conditioning;
- process CLT and Mosco recovery;
- nonlinear Nisio resolvents and graph cores;
- exact-experiment filtering/QMD/LAN;
- changing-filtration response; and
- labelled posterior contraction and typed phase recovery.

The entropy potential in Revision 61 is an auxiliary finite-dimensional directional entropy. It is not the stopped-path entropy theorem required by A3. The causal process result is not the filtering or response gate required by C1/C2. The LPS gap supplies no local-limit or Mosco result.

Accordingly the following remain false:

```text
historical A2 replacement
B4 aggregate
C2 aggregate
eleven-paper aggregate
whole Theta program closure
```

No local success in source verification changes this mathematical dependency statement.

---

## 11. Risk register

### R1 — Priority risk: high

The exact combined theorem may be new, but the boundary against positive realization, controlled hidden-state approximation, automata advice, quantization, and entropy-dissipation methods has not been independently cleared.

### R2 — Model-interpretation risk: high

Readers may mistake label width for uniform computational memory. The uncharged clock, tables, arithmetic, and exact sampling must remain visible.

### R3 — Spectral-hypothesis risk: moderate

The full action gap is much stronger than a finite-dimensional matrix gap. Examples without the full gap lie outside the sharp theorem.

### R4 — Synchronization risk: moderate

The quantitative theorem needs identity or cofinite exact returns. Approximate returns require additional estimates.

### R5 — Causal-scope risk: high outside the declared model

Repeatable fresh probes are central. The theorem is not a general process-realization or quantum-measurement result.

### R6 — Sharpness risk: moderate

Power exponents match only when `p_*=q`. Leading constants, the full error crossover, and the causal exponent remain open.

### R7 — Imported-input risk: controlled

The LPS constant was verified in a primary restatement. The older Bourgain--Gamburd constant remains non-effective and is kept separate.

### R8 — Reproducibility risk: low

The exact-final-head read-only run succeeded. A cryptographic author signature is still absent but is not claimed.

### R9 — Whole-program overclaim risk: controlled

All aggregate flags remain false and the manuscript repeatedly preserves the separation.

---

## 12. Specialist-release gates

### Mathematical gates

- Preserve the full action-gap formulation and invariant projection `Pi`.
- Preserve the compact-support/zero-density regularization argument.
- Keep centroid-mass weighting explicit.
- Keep identity/return synchronization hypotheses in theorem headlines.
- Keep exact, robust shrinking-error, and fixed-positive-error regimes separate.
- State matching width only for fixed positive subcritical error and `p=q`.
- Keep repeatable-probe assumptions explicit in every causal summary.

### Priority gates

- Obtain external comparison from experts in positive realization and probabilistic automata.
- Obtain external comparison from experts in controlled HMM/PSR/causal-state theory.
- Compare the entropy telescope to quantization and filter-stability literatures theorem by theorem.
- Avoid using revision count or repository breadth as novelty evidence.

### Reproducibility gates

- Preserve the successful exact-head attestation and immutable run identity.
- Publish a compact release manifest binding source, PDFs, examples, and verifier run.
- Keep the complete historical archive available but outside the normal journal-facing package.
- Do not describe CI as mathematical certification.

### Editorial gates

- Submit the quantitative and structural articles separately.
- Treat the complete edition as archival.
- Shorten the front matter and evidence discussion in the article itself.
- Center the quantitative introduction on the entropy occupation theorem and the LPS example.
- Center the structural introduction on repeatable-process classification and finite physical actions.

---

## 13. Audit verdict

### Local mathematical correctness

**Pass with qualifications.** I found no fatal gap in the inspected new spectral-entropy, LPS, causal, or compiler chains. The qualifications are the displayed full-action gap, synchronization, legal-output, repeatable-probe, and strict-positive-probe hypotheses.

### Imported mathematics

**Pass for stated use.** The exact LPS norm matches the displayed six rotations. The older Bourgain--Gamburd input remains non-effective and is not silently reused as a numerical constant.

### Reproducibility

**Pass.** The exact reviewed SHA has a successful, separate, contents-read-only reconstruction run. This is strong source/artifact evidence, not mathematical independence or signature.

### Priority

**Open.** The audit remains author-side, and several neighboring theorem languages require independent expert review.

### Repository-wide program

**Open.** No A/B/C/D aggregate gate is discharged.

### Editorial significance

**Strong specialist potential; four-leading-journal threshold not established.**

```text
latest-object identity:          PASS
new local proof chain:           PASS WITH HYPOTHESES
LPS numerical specialization:   PASS
causal repeatable-probe chain:   PASS IN DECLARED MODEL
generic causal compiler:         PASS IN DECLARED MODEL
exact-final-head reproduction:   PASS
independent priority:            OPEN
whole Theta program:             OPEN
Annals/Inventiones/JAMS/Acta:    REJECT
```
