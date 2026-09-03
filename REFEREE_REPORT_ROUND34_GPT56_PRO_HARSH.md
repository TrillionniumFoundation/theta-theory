# External Referee-Style Report — Round 34

## Round 33: substantial proof repair, but not an eleven-paper top-journal research contribution

**Recommendation:** **Reject the present eleven-paper dossier for research publication at the requested top-four-journal level. Do not treat it as a dossier-wide major revision awaiting a finite list of proof repairs.**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision:** `revision/round33-referee-positive-reconstruction-2026-09-03`  
**Immutable reviewed commit:** `7bb555662a572bd400fbfb0d6011a812ad578593`  
**Reviewed source tree:** `e59d70e4a7e438f6777a04cbaddc9bb131d4111f`  
**Previous report commit:** `e037717914a34fe7c0636743b3f5c645969bcb20`  
**New review branch:** `review/round34-gpt56-pro-harsh-11paper-2026-09-03`  
**Date:** 3 September 2026  
**Reviewer:** GPT-5.6 Pro, at the repository user's request.

This is an AI-assisted independent referee-style assessment using the correctness, originality, significance, and completeness threshold appropriate to the requested comparison with Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a report commissioned by, or an editorial decision of, any of those journals.

**Important distinction from the preceding rounds:** I do not find grounds to describe Round 33 as an unfinalized source-patching submission, or to repeat that all of its active core arguments are invalid. Those would be inaccurate descriptions of the present source. The negative publication recommendation now rests principally on the absence of the original mechanical research results and the absence of a demonstrated new contribution of the requested significance. Two local statement qualifications are identified separately below; neither justifies dismissing the repaired core wholesale.

---

## 1. Assessment for the editor

Round 33 makes a material change in mathematical practice. The author response expressly says that not all original mechanical theorems have been established. The active chapters distinguish elementary proved constructions, conditional implications, nonempty examples, and outstanding applications. The earlier practice of presenting a named repair mechanism as if it had already supplied the difficult model estimate has largely been abandoned.

That change deserves recognition, not punishment. A conditional theorem is not false merely because one intended application remains open. A correct reconstruction lemma also does not become a new research result merely because earlier versions of it were wrong.

The present dossier is best understood as a collection of reconstruction notes supporting a research programme. It is not a completed eleven-paper programme in billiards, hard-sphere dynamics, kinetic large deviations, inference, and phase control. The source itself now acknowledges that distinction. It supplies several coherent proofs, but it does not demonstrate why these proofs, individually or collectively, constitute a sufficiently original and substantial research contribution for the requested journals.

The closest thing to a central analytic contribution is B2's equal-radius construction. Its corrected majorant is valid under the stated compatible-scale assumptions. However, this is an Ovsyannikov-type analytic-scale argument, not a proof of the hard-sphere creation estimates, all-genealogy rank, or trajectory large-deviation theorem. D1's common-policy selection result is another useful and checkable implication, but its mechanical local-density input and uniform policy expansion are assumed rather than constructed.

My recommendation is therefore rejection of the dossier as a top-journal research submission. I would not issue another invitation to repair all eleven papers simultaneously. A future submission should be assessed as a new, focused paper presenting one substantial theorem, with its novelty and model hypotheses established. This recommendation does not require solving the entire research programme before anything can be publishable.

### Three separate judgments

| Question | Finding in this review |
|---|---|
| Has the revision made genuine mathematical and source-integrity progress? | Yes. Several important old contradictions have been removed by actual proofs or by an explicit withdrawal of unsupported applications. |
| Do the proved reconstruction results withstand the checks documented here? | Broadly yes, subject to the local qualifications and precise scope recorded below. This is not a certification of every possible technical detail. |
| Does the dossier establish an original, completed contribution at the requested research-publication level? | Not demonstrated. The central mechanical applications remain outstanding, and the abstract results lack an adequate novelty case. |

These judgments must not be collapsed into either “all gaps closed” or “all mathematics false.”

---

## 2. Immutable scope and reproducibility audit

### 2.1 What was read

I read all eleven active chapter files at the frozen commit:

`round33/chapters/A1.tex`, `A2.tex`, `A3.tex`, `A4.tex`, `B1.tex`, `B2.tex`, `B3.tex`, `B4.tex`, `C1.tex`, `C2.tex`, and `D1.tex`.

I also read `AUTHOR_RESPONSE_ROUND32.md`, `ROUND33_REVIEW_INDEX.md`, `ROUND33_PROOF_LEDGER.md`, `round33/ISSUE_LEDGER.json`, `round33/LITERATURE.md`, `ROUND33_REVISION_DOSSIER.tex`, `ROUND33_PREAMBLE.tex`, `ROUND33_LOCAL_VERIFICATION.json`, `tests/test_round33.py`, `tools/verify_round33.py`, and `.github/workflows/verify-round33.yml`. The commit comparison against the preceding report confirms a real source revision, not a renamed ref.

The active architecture is different from earlier rounds: the canonical paper entries select Round 33 wrappers, and the active proof material is under `round33/chapters/`. Historical `ROUND31_POSITIVE_CLOSURE.tex` files are not the mathematics assessed here. Exact theorem labels are given below so that comments refer to the submitted source rather than a changing PDF page number.

### 2.2 Independently executed work

The author's `tests/test_round33.py` was reproduced in the review environment and its Git blob identity was checked before execution:

```text
Git blob SHA-1: fab9d94d471fb2562533ebf6ea574876ce46648e
SHA-256: 1a73138145e70aac4bf1c5c358df8e4229d46cfc9cbd67b470ccb83ecb9f2582
Bytes: 11797
Python: 3.13.5
Tests executed: 42
Passed: 42
Failed: 0
```

The issue ledger was independently counted after its reconstructed bytes were checked against Git blob `c8989cdfa303ed1bc8f0a6b4f54d901fa1bc71b2`. The companion file `review_artifacts/round34/verification.json` records these results and the two reviewer diagnostic checks.

### 2.3 Work not independently repeated

I did not rerun the full repository manifest/build verifier or the twelve LaTeX builds in this review session, and I did not independently inspect all manuscript PDF pages. The reported 38-page dossier, twelve PDFs, 58 labels, and 36 theorem-level statements are information in the author's local verification record, not new build measurements by this referee.

The local record explicitly sets `remote_ci_verified` and `all_original_gaps_closed` to false. I make no assertion that a remote workflow has completed. Absence of a legacy commit-status context would not, by itself, establish absence of GitHub Actions checks.

The new verification script checks source structure and hashes, executes finite examples, writes build outputs under `build/`, and rechecks the source manifest. The new workflow has read-only repository permissions and does not run a source-patching finalizer. I find no basis to carry forward the previous accusation that proposed patches are being presented as already active mathematics.

### 2.4 The meaning of the ledger

The machine-readable ledger contains 76 mapped objections with the following declared statuses:

| Chapter | `core_repaired` | `application_open` | `source_repaired` |
|---|---:|---:|---:|
| A1 | 5 | 1 | 0 |
| A2 | 1 | 5 | 0 |
| A3 | 4 | 3 | 0 |
| A4 | 3 | 4 | 0 |
| B1 | 3 | 3 | 0 |
| B2 | 4 | 5 | 0 |
| B3 | 3 | 4 | 0 |
| B4 | 1 | 6 | 0 |
| C1 | 4 | 2 | 1 |
| C2 | 4 | 3 | 0 |
| D1 | 3 | 4 | 0 |
| **Total** | **35** | **40** | **1** |

These are counts of responses to objections, not percentages of the original programme proved. A single open all-genealogy estimate may carry substantially more mathematical content than several repaired normalization identities. The status descriptions correctly say that `core_repaired` does not automatically validate the intended application.

---

## 3. Principal publication objections

### R34-M1 — The research object has changed, but a new research contribution has not been established

The active submission no longer proves the headline mechanical conclusions of the earlier dossier. It explicitly leaves open the concrete Sinai all-frequency theorem, chronological recovery and stopped local theorem, physical memory hypotheses, hard-sphere joint history large deviations, kinetic process identification, nonlinear semigroup, mechanical inference, and adaptive phase asymptotics.

This is an honest narrowing of claims. It is not a resolution of those targets. The publication case must consequently stand on the reconstruction theorems themselves. The dossier does not provide an adequate explanation of which such theorem is new, how it improves the closest result, or why its improvement is significant independently of the unproved application.

### R34-M2 — Standard mechanisms require a precise novelty comparison

The main proof mechanisms are familiar: finite-cylinder martingale decomposition, uniform differentiation of summable series, algebraic-number norms, Fourier inversion with an integrable remainder, the entropy chain rule, Lumer–Phillips generation, Gaussian orthogonal decomposition, analytic-scale majorants, finite-grid chaining, entropy duality, strict duality, conjugate Gaussian inference, and Lipschitz BSDE stability.

The B2 majorant in particular should be compared explicitly with Finkelshtein [L1], including equation (2.12) and the associated existence, uniqueness, and perturbation results. The characteristic `n^n/n!` scale estimate predates this dossier. The current measurable-time formulation should be compared hypothesis by hypothesis; I do not assert without such a comparison that every detail of it is literally identical to a theorem in [L1]. The issue is that the claimed advance has not been demonstrated.

Likewise, Hilbert-valued projective martingale approximation has a substantial existing literature, including [L2]. The current strong bounded-shell hypothesis makes a direct proof possible, but the manuscript must identify the additional contribution of parameter response or geometric realization, rather than treating the availability of a proof as sufficient evidence of novelty.

D1's power-drop/Hölder selection argument is a potentially useful lemma. Its proof is more convincing than the preceding versions. Nevertheless, the dossier supplies neither an adequate comparison with established asymptotic optimization nor a new mechanical application establishing its research significance. I do not claim to have conducted an exhaustive priority search for that lemma.

### R34-M3 — Nonemptiness of an auxiliary example is not realization of the mechanical model

The examples are genuinely nonempty, which is an improvement. Their relationship to the intended application remains limited:

* A1 deliberately inserts depth-decaying weights into its Dirac-current example; the original unweighted seam is not thereby represented.
* A2 uses independent Bernoulli and Gaussian increments; it does not construct a singular billiard transfer operator with the required estimates.
* A4 uses a dissipative two-dimensional matrix; an invertible measure-preserving mechanical flow does not inherit its coercivity.
* C1 estimates a sensor offset with a parameter-free, statistically irrelevant hidden mechanical state; it does not identify a billiard or hard-sphere parameter.

These examples validate consistency of the abstract setup. They do not cross the missing model interface. The author now says this correctly, so it would be unfair to characterize the missing interfaces as concealed. They remain decisive for the original research claims.

### R34-M4 — Conditional implications cannot be exported as completed dependencies

An estimate of the Fourier inversion remainder is not the source-differentiated anisotropic estimate it assumes. A scale-of-spaces evolution theorem is not the verified collision-creation bound it assumes. A finite-grid tightness theorem is not the microscopic within-cell estimate it assumes. A common-policy Laplace implication is not the labelled, off-central, policy-uniform density expansion it assumes.

The revised ledger largely respects these distinctions. The resulting graph is therefore a dependency plan with unresolved roots, not a completed theorem chain. No downstream paper should regain the earlier unconditional title or abstract merely because its abstract transfer lemma has passed review.

### R34-M5 — Eleven corrected notes do not automatically form eleven research papers

The number of files and the short length of individual chapters are not objections by themselves. A short theorem can be major mathematics. Here, however, the eleven-way organization mostly partitions a collection of general tools and repair explanations. There is no demonstrated independent research contribution for each proposed paper, and no single completed central theorem unifying the dossier.

A consolidated reconstruction or methods note would be a more accurate description of the current achievement. That is not a recommendation of acceptance by another journal. Research publication still requires a substantive result and a precise account of originality.

---

## 4. Chapter-by-chapter mathematical assessment

All locators below refer to `round33/chapters/<code>.tex` at the immutable reviewed commit.

### 4.1 A1 — Strong shell response and a Hilbert functional limit

**Locators:** `thm:r33-a1-response`, `lem:r33-a1-ancestry`, `lem:r33-a1-remainder`, `thm:r33-a1-fclt`.

The strengthened shell assumption is sufficient for the argument being made. Each shell is a genuinely differentiable finite-cylinder function with a uniform polynomial-times-exponential bound. Finite-product differentiation introduces only polynomial factors, so the Banach-valued fundamental theorem of calculus justifies strong differentiation of the mean. This is not the old invalid promotion of weak boundedness to strong differentiability.

The projection-support calculation is also explicit: a translated depth-n cylinder has support interval `[q-n,q+n]`, and its projection at zero vanishes when that interval lies entirely in the past or entirely in the independent future. The bounded partial-sum remainder follows by cancelling the interior pairs in the two finite double sums. Summability of the endpoint error is supplied by the shell bound. Forming the covariance on one common Hilbert reporting space removes the old distributional-loss mismatch.

I did not find a decisive contradiction in these core arguments. The weighted Dirac-current example is compatible with their hypotheses. It should remain labelled weighted; its coefficients cannot be silently removed when returning to the geometric problem.

**Unresolved research obligation:** prove the shell representation and derivative bounds for the original geometric current, and identify what the response theorem adds beyond existing projective martingale methods [L2]. The current example does not establish that step.

**Disposition:** reject as the proposed top-journal geometry/current paper; retain the repaired abstract construction as supporting material.

### 4.2 A2 — Arithmetic and a conditional Fourier budget

**Locators:** `prop:r33-a2-arithmetic`, `thm:r33-a2-integral`, and the section on the central Edgeworth remainder.

The arithmetic proof now has the correct frequency range. For `|b| >= 1`, nearest-integer reduction gives a nonzero algebraic integer `k-m sqrt(2)-n sqrt(3)`. Bounding its other three conjugates gives a polynomial lower bound. There is no lower bound bounded away from zero as `b -> 0`, and unrestricted openness is explicitly denied.

The integration theorem likewise makes its inputs visible. The intermediate region has polynomial volume, and the tail integral has order `N^(v-A(M-d_C))`. The strict exponent inequality gives the stated negligible noncentral integral. A central L1 remainder is separately required before an Edgeworth expansion is concluded. The independent Bernoulli/Gaussian example exercises these hypotheses without being relabelled a billiard.

**Unresolved research obligation:** construct the actual stable-curve spaces, periodic-data realization, returned and terminal cancellation, and differentiated central L1 remainder for a specified Sinai family. Merely having a finite list of desired estimates is not that construction. The statistical-limit framework in [L3] is relevant but does not supply the stated raw mixed Edgeworth theorem automatically.

**Disposition:** reject as a completed Sinai local-limit paper. The arithmetic and inversion lemmas are coherent, but the difficult model theorem remains absent.

### 4.3 A3 — Exact divergence and the entropy clock

**Locators:** `thm:r33-a3-balance`, `thm:r33-a3-entropy`, `prop:r33-a3-conditioning`.

The right-endpoint marked current has the correct head, tail, mark, and scaling. The identity

```text
partial_s L_N + div_U J_N = delta_initial - delta_terminal,
J_N = N Q_N,
```

follows exactly by telescoping. The text no longer invents an independently controllable mesoscopic current from an undefined divergence. It also correctly distinguishes a test-dual bound from a compactness theorem.

The stopped entropy formula is a bounded-horizon chain rule. Each selected transition is charged once. The binary constant-return example consequently has rate `H/r`, rather than the old erroneous rate `H`. Macroscopic holding intervals and source-dependent conditioning amplitudes are no longer discarded.

These corrections resolve the elementary consistency objections. They do not prove recovery for every proposed chronological state. In particular, an exact finite-word identity cannot by itself establish exponential tightness, realizability of a limit current, or a terminal-state local theorem for singular mechanical excursions.

**Unresolved research obligation:** define and analyze the actual chronological state, establish the complete-past moment estimate, and prove the upper/lower bounds and stopped local estimates on that state.

**Disposition:** reject as the original full path-LDP paper; the exact balance and entropy identities are useful prerequisites, not the path theorem.

### 4.4 A4 — Generation, compression, and memory

**Locators:** `thm:r33-a4-generation`, `prop:r33-a4-compression`, `thm:r33-a4-memory`.

The generation theorem now uses a real range condition and shifted dissipativity, so Lumer–Phillips is actually applicable. The compression construction is also materially better: an orthogonal finite-rank projection with basis in `D(L) intersect D(L*)` has bounded off-diagonal blocks. Subtracting these blocks is a genuine bounded perturbation on the underlying Hilbert space; the complementary generator is no longer obtained from a graph-angle slogan.

For memory, a Hilbert-bounded observation and input in `D(L_Q^4)` justify four resolvent identities. On a stable vertical half-plane, the final terms are uniformly `O(|z|^-4)`. The two-dimensional example checks the signs and the generic nonzero first coefficient. I do not carry forward the old third-domain/fourth-remainder objection.

**Unresolved research obligation:** show that a physically relevant mechanical representation satisfies these domain and coercivity hypotheses, and prove the weighted coupling, renewal strip estimates, and pressure bridges it requires. The manuscript correctly notes that mixing of an invertible measure-preserving flow does not establish dissipativity of its L2 complement. The weak-Harris framework [L4] does not remove that distinction.

**Disposition:** reject as a completed mechanical memory/pressure paper. The abstract implications are credible; their particular mechanical realization and novelty are not established.

### 4.5 B1 — A complete equilibrium Gaussian anchor

**Locators:** `thm:r33-b1-density`, `thm:r33-b1-fourier`, `prop:r33-b1-event`.

The equilibrium reference genuinely separates Gaussian velocities from coupled hard-core positions. Orthogonal decomposition in the label index proves independence of total momentum and relative energy, and the latter has the appropriate gamma law for more than one anchor particle. The joint characteristic function and the explicit anchor-size inequality provide a full momentum-energy Fourier integral, including the conic regime where momentum frequency grows with energy frequency.

The exceptional-event factorization is now exact because the event is measurable without reserved velocities and is used before exact energy disintegration. The chapter expressly says that a path-dependent tilt destroys this simple proof. This is a valid restriction rather than an unproved all-exterior smoothing claim.

There is a minor endpoint qualification at `m=1`, detailed in Section 5.2. It does not undermine the smoothing theorem, whose anchor-size condition already requires a larger group.

**Unresolved research obligation:** obtain the differentiated mixed-amplitude and saddle estimates under the actual extensive trajectory tilt. A linear/quadratic Gaussian tilt is not a general hard-sphere path source.

**Disposition:** reject as a dynamic exact-preparation paper at the requested level. The equilibrium calculation is sound supporting analysis but does not establish the advertised dynamic interface or its originality.

### 4.6 B2 — The principal analytic repair

**Locators:** `thm:r33-b2-scale`, `prop:r33-b2-unique`, `thm:r33-b2-stability`, `prop:r33-b2-rank`.

This chapter contains the clearest substantive repair. With `Delta=a_0-a_*`, the n operators use n equal radius gaps chosen before integrating time. Hence

```text
||U_n(t)|| <= (n^n/n!) (Mt/Delta)^n <= (eMt/Delta)^n.
```

For `q=eMT/Delta<1`, the series and geometric tail converge uniformly through the endpoint. A strict intermediate radius permits termwise integration in the final space. The proof contains neither a nonintegrable `1/(t-s)` bound nor a norm with a vanishing endpoint multiplier. The uniqueness statement is properly restricted to compatible bounded scale-valued solutions whose equations hold at lower radii. The stability argument uses finite-order convergence plus a common summable tail.

The rank section also now states the correct missing condition: surjectivity of `DG` on `ker DF` is equivalent to full stacked rank. Projecting onto the tree tangent space does not prove that rank. The chapter explicitly allows singular deterministic transition kernels and distinguishes time composition from cumulant combinatorics.

These arguments withstand the checks documented here. They should not be described as another iteration of the old false pivot or radius proof.

**Unresolved research obligation:** verify the actual hard-sphere scale estimate with controlled constants, all relevant genealogy constraints and repeated labels, signed cluster combinatorics, and the exponential tightness/recovery required for the stronger joint history LDP. The chapter does not claim these have been accomplished. Related primary hard-sphere results [L5–L6] cannot simply be substituted for a different joint state or stronger source class.

**Originality objection:** the scale mechanism is established analytic-scale methodology [L1]. A new nonautonomous refinement would need a precise comparison and a demonstrated gain; the current paper does not supply that publication case.

**Disposition:** reject as a top-journal hard-sphere root paper; preserve the corrected scale lemma as a reliable candidate tool.

### 4.7 B3 — Finite-grid tightness and static Mosco convergence

**Locators:** `thm:r33-b3-grid`, `thm:r33-b3-static`.

The terminal-grid construction counts the microscopic error only over finitely many levels. Its budget

```text
r_epsilon^p d_epsilon^(-1-p gamma) -> 0
```

is explicit, and within-cell oscillation is a separate assumption. This avoids the previous divergent infinite-grid summation and the invalid replacement of continuous within-cell oscillation by maximum jump size. The distinction between cadlag microscopic paths, continuous interpolants, and continuous limits is now correct. The mode-count condition `2s>D` also fixes the previously unsupported Hilbert–Schmidt embedding.

The static entropy Mosco result is proved by an appropriate dual liminf and truncated recovery. It retains the positive cost of collision-cycle directions and does not infer L2 compactness merely from a bounded entropy expression.

**Unresolved research obligation:** derive the interval, within-cell, and drift estimates for the actual hard-sphere field; establish the kinetic graph inverse; and prove moving-reference, nonlinear-balance recovery before identifying a dynamic covariance. A static reference-measure theorem does not establish these results.

**Disposition:** reject as the original kinetic fluctuation/Mosco paper; the revised conditional grid theorem and static form should remain explicitly separate from the application.

### 4.8 B4 — Kinematic compactification, not a boundary semigroup

**Locators:** `prop:r33-b4-closure`, `thm:r33-b4-compact`, and the collision-product section.

The set of pairs `(f,e)` with `E(f)<=e<=E_0` is correctly characterized as the narrow/total-energy closure. The recovery mixture moves vanishing probability to high velocity while preserving the desired total energy. This construction records a scalar defect and does not pretend to define its dynamics.

The positive path-compactness theorem supplies independent superlinear velocity-tail control and a local spatial-density bound. These give a reference contact-mass bound on short intervals. The entropy estimate then gives a narrow time modulus, while genuine quadratic uniform integrability upgrades it to W2. This is a coherent sufficient criterion. It is not the former false assertion that Gaussian relative entropy and energy alone imply W2 compactness.

The spatial oscillation example is important: W2 convergence does not pass the local collision product. The stated strong weighted L1 sufficient condition addresses that issue rather than hiding it in a velocity truncation.

**Unresolved research obligation:** obtain these tail and spatial hypotheses for the original finite-action controls, or construct boundary collision dynamics with an identified action. State invariance, selection, comparison, and microscopic realization still require proof. The chapter correctly does not assert a full boundary semigroup.

**Disposition:** reject as a completed nonlinear kinetic-semigroup paper. The closure and sufficient compactness criterion are not the original semigroup result.

### 4.9 C1 — Valid channels and a deliberately decoupled diagnostic example

**Locators:** `prop:r33-c1-channel`, `prop:r33-c1-projective`, `thm:r33-c1-push`, `thm:r33-c1-exact`.

The stratum-selection probabilities now remain in the observation density, so the entire channel has mass one. Differentiability in L1 is distinguished from square-root differentiability at a newly appearing stratum. The explicit tensor-Sobolev marginal spaces and bonding maps give a complete projective dual. The push-forward theorem is for measures and their resulting jets, not arbitrary distributions under arbitrary nonlinear maps.

The adaptive Gaussian calculation is also internally consistent. Common parameter-independent policy factors cancel in the chronological joint likelihood. Completing the Gaussian square gives the exact posterior. Diagnostic-frequency concentration and the martingale second-moment bound yield the stated uniform posterior approximation without a fictitious deterministic filter contraction.

**Decisive scope limitation:** the estimated parameter is a sensor offset and the hidden dynamics is parameter-free. The experiment demonstrates a nonempty consistent inference model, but the mechanical hidden state has been disconnected from the parameter-identification problem. That is not evidence that the original mechanical observation model is identifiable or has stable long-time filter derivatives.

**Unresolved research obligation:** establish induced-law identification, time-uniform derivative estimates, and posterior testing for a genuinely mechanical parameter and signal.

**Disposition:** reject as the proposed mechanical inference paper. The example is a correct calibration model, not the missing inference theorem.

### 4.10 C2 — Strict duality and finite-horizon prediction

**Locators:** `prop:r33-c2-strict`, `prop:r33-c2-likelihood`, `thm:r33-c2-evidence`, `thm:r33-c2-bsde`.

The c0-sum/Hahn–Banach proof of strict duality is much more satisfactory than the earlier compact-exhaustion arguments. The likelihood identity now includes the actual chronological policy convention and parameter-specific filters. The prediction estimate uses an explicit L1 comparison of whole-path observation densities, and it expressly distinguishes a uniform bound on each-time expectations from an expected-supremum or process-convergence estimate.

The BSDE stability result specifies a fixed Brownian–Poisson basis, representation property, integrand spaces, Lipschitz assumptions, and L2 errors. Its Itô–BDG argument is appropriate to that setting. It does not prove stability across arbitrary changing filtrations, and the chapter no longer says that it does.

The evidence theorem requires bounded versions on zero-evidence sets, rather than the literal arbitrary-version quantifier in its statement. Section 5.1 supplies the precise counterexample and repair. The underlying estimate with bounded versions remains valid.

**Unresolved research obligation:** construct the relevant full-path likelihood coupling and prediction-process tightness for the mechanical approximation, and establish the singular pressure bridges and Livšic extension. A finite graph cycle criterion does not do this.

**Disposition:** reject as a completed mechanical rigidity/prediction paper. The classical and conditional interfaces do not establish a new result of the requested scope.

### 4.11 D1 — Correct normalization and a useful conditional selection lemma

**Locators:** `prop:r33-d1-jacobian`, `thm:r33-d1-laplace`, `thm:r33-d1-selection`.

The raw-sum to empirical-mean Jacobian is now correct. The conditional fibre/cell calculation retains the continuous normalization and the full mixed normal Hessian. It requires an actual labelled local density, Gaussian domination, and control of the complement at the polynomial order claimed. These assumptions are no longer attributed to an unlabelled central LLT.

The common-policy selection theorem has a real near-maximizer argument. A power drop bounds distance to the leading phase set by a power of `log(N)/N`; Hölder continuity of the polynomial exponent then makes its possible gain, multiplied by `log N`, tend to zero. Compactness and finitely many phases give the matching upper bound, while a fixed common maximizer supplies the lower bound. I did not find a counterexample under the stated uniform hypotheses.

The symmetric two-phase example correctly shows a shared-policy loss at constant order while the leading maximum remains phase-blind. The memory discussion now computes the growth price of the approximating chart instead of silently calling it subpolynomial.

**Unresolved research obligation:** prove the physical phase labels, off-central local density and uniform adaptive expansion, and demonstrate the novelty or a substantive application of the abstract selection result. The theorem cannot itself produce those inputs.

**Disposition:** reject as the original phase-synthesis paper; the selection lemma is worth retaining and comparing carefully with existing asymptotic optimization.

---

## 5. Local statement corrections found in the active revision

These are genuine corrections to make, but their scale must not be exaggerated.

### R34-C2-01 — Zero-evidence versions must be bounded

**Location:** `round33/chapters/C2.tex`, `thm:r33-c2-evidence`.

The statement permits arbitrary versions on zero-evidence sets, whereas its proof chooses a version bounded by `||F||_infinity`. This restriction matters because a set null for the limiting observation law can have positive probability under the approximating law.

Take a one-point hidden state and an observation space `{0,1}` with counting measure. Let `F=0`, let the limiting observation law be `(1,0)`, and let the approximating law be `(1-epsilon,epsilon)`. A legitimate version of the limiting conditional expectation is zero at observation 0 and one at its null observation 1. The approximating conditional expectation is zero everywhere. Then the stated left side is `epsilon`, whereas

```text
b_n + 2 ||F||_infinity epsilon_{n,t} = 0.
```

Thus the literal arbitrary-version assertion is false. Replace it by a requirement that versions remain in `[-||F||_infinity,||F||_infinity]`, for example choose zero on zero-evidence sets. The supplied proof then works. The review diagnostic used exact rational `epsilon=1/10`.

**Classification:** local quantifier error with an immediate repair; not a refutation of the evidence-weighted coupling argument.

### R34-B1-01 — Specify the one-particle endpoint

**Location:** `round33/chapters/B1.tex`, `thm:r33-b1-density`.

The setup allows `N>=m`, and the theorem first states a gamma law with shape `d(m-1)/2`, before restricting the displayed density to `m>1`. At `m=1`, relative energy is identically zero and the correct law is a point mass at zero; `Gamma(0,1)` is not the gamma probability density being used.

Either restrict the whole nondegenerate law statement to integer `m>=2` or state the degenerate `m=1` case separately. If the phrase “for m>1” was intended to qualify the entire theorem, make that scope explicit. The Fourier smoothing budget already chooses more particles, so no claimed smoothing estimate is lost.

**Classification:** endpoint/scope qualification, not a structural failure.

### Additional editorial precision

B3's initial use of Minkowski in `L^(p/2)` should explicitly retain `p>=2`; its later grid theorem already assumes `p>2`. The fixed-basis BSDE statement should retain the usual measurability/predictability hypotheses on its drivers and the standard conditions on the intensity measure. These are specification improvements, not independently established counterexamples to the intended formulations.

---

## 6. What the 42 passing tests establish

The test suite is appropriately described by its author as finite algebraic/numerical examples rather than a proof assistant. My independent run confirms its execution result, not the infinite-dimensional theorems.

The tests check useful identities and safeguards: the factorial majorant, a fixed geometric tail, an exact finite marked-edge balance, the constant-return entropy clock, a finite algebraic-norm sample, a matrix resolvent, Gaussian characteristic normalization, a finite-grid exponent, contact-cycle cost, stratum normalization, a posterior calculation, and fibre/cell powers.

They do not construct a billiard grammar or a collision genealogy estimate. A finite scan of integers does not prove the all-frequency arithmetic proposition; its algebraic proof does. A posterior calculation for three numerical observations does not establish a uniform adaptive asymptotic theorem; its likelihood and concentration proof must do so. A symmetric two-phase grid does not exercise every near-maximizer regime in D1.

The suite also does not read the active TeX and derive its theorem assertions. A manuscript statement could change while its independently coded numerical example still passes. This is a limitation of regression testing, not evidence that the author claimed formal verification. The new source explicitly disclaims that claim.

Useful future tests would cover the bounded-version choice in C2, the `m=1` degenerate anchor, mixed covariance blocks in the Laplace calculation, nonconstant polynomial exponents near policy maximizers, and an actually adaptive diagnostic schedule. Such tests supplement proofs; they do not discharge the 40 open application items.

---

## 7. Literature interfaces and limits of this comparison

The following primary sources were used to check the relevant literature interfaces. This is not an exhaustive novelty search.

**[L1]** D. Finkelshtein, *Around Ovsyannikov's method*, Methods of Functional Analysis and Topology 21 (2015), 134–150; arXiv:1412.8628. The existence/uniqueness/limiting framework and the scale majorant are directly relevant to B2. A precise comparison is needed before claiming a new abstract evolution theorem.

**[L2]** C. Cuny and F. Merlevède, *On martingale approximations and the quenched weak invariance principle*, Annals of Probability 42 (2014), 760–793; DOI:10.1214/13-AOP856; arXiv:1202.2964. This supplies a relevant Hilbert-valued projective martingale context, not an automatic proof of this dossier's geometric current realization.

**[L3]** M. Demers, I. Melbourne and M. Nicol, *Martingale approximations and anisotropic Banach spaces with an application to the time-one map of a Lorentz gas*, Nonlinearity 33 (2020), 4095–4113; arXiv:1901.00131. Its statistical-limit scope should not be confused with the unproved source-uniform raw Edgeworth application in A2.

**[L4]** M. Hairer, J. C. Mattingly and M. Scheutzow, *Asymptotic coupling and a general form of Harris' theorem with applications to stochastic delay equations*, Probability Theory and Related Fields 149 (2011), 223–259; arXiv:0902.4495; DOI:10.1007/s00440-009-0250-6. The distance and integrability hypotheses must match the norm actually used.

**[L5]** T. Bodineau, I. Gallagher, L. Saint-Raymond and S. Simonella, *Statistical dynamics of a hard sphere gas: fluctuating Boltzmann equation and large deviations*, Annals of Mathematics 198 (2023), 1047–1201; DOI:10.4007/annals.2023.198.3.3; arXiv:2008.10403. The publisher's statement describes short-time results away from equilibrium, with regularity assumptions. This specific result is not a substitute for proving a stronger joint history-state theorem.

**[L6]** The same authors, *Cluster expansion for a dilute hard sphere gas dynamics*, arXiv:2205.04110; DOI:10.1063/5.0091199. Its real-trajectory cluster construction is relevant to the distinction between actual correlation cumulants and a formal logarithm of time-composition kernels.

The revision's `round33/LITERATURE.md` already acknowledges many of these limits. That is a positive change in attribution. It still does not provide the theorem-by-theorem comparison needed to establish a research advance.

---

## 8. Requirements for a genuinely new submission

A further submission should not merely rename the next round or expand the response ledger. It needs a different publication unit.

**First, choose one research theorem.** It may be a concrete billiard theorem, a hard-sphere result, or an abstract theorem with independently substantial scope. Completion of all eleven ambitions is not a prerequisite. The submission must, however, state what is newly proved rather than relying on the ambition of the surrounding programme.

**Second, give a hypothesis-level novelty comparison.** For an abstract scale theorem, compare the time dependence, measurability, scale assumptions, uniqueness class, constants, and stability conclusion with the nearest results. For A1 or D1, isolate the parameter-response or optimization feature that is claimed to be new and explain its mathematical consequence.

**Third, prove one real model interface.** A weighted toy current is not the unweighted seam, a Gaussian increment is not a billiard roof, and an independent sensor offset is not a hidden mechanical parameter. Specify a nonempty intended model and verify every imported hypothesis on it.

**Fourth, preserve the honest dependency ledger.** Conditional tools can be used once their premises are proved. Until then they remain implications, not established mechanical exports. Keep the local/remote build distinction and the read-only source verification adopted in this revision.

**Fifth, separate exposition from research claims.** Several chapters could be consolidated into preliminaries, appendices, or a methods note. A stand-alone submission should contain a coherent theorem, a complete proof, the exact literature interface, and a demonstrated contribution. A corrected elementary proof is valuable without being a top-four-journal paper.

The two local corrections in Section 5 should be made regardless of publication plans. They are not the reason a substantial new submission is required.

---

## 9. Final recommendation

Round 33 is a substantial improvement over Round 31. It contains actual replacement mathematics, a better source-verification protocol, several proofs that withstand the checks made here, and an explicit statement of what remains unproved. I withdraw the earlier round's general characterization of an unfinalized source-patching submission as a description of this revision.

I nevertheless recommend **rejection of all eleven components as the proposed top-four-journal research dossier**. The current achievement is a reconstruction of tools and conditional arguments, not completion of the original mechanical programme; nor has the dossier established sufficient originality and significance for those tools as independent research papers.

The appropriate conclusion is therefore:

> **Substantial and credible reconstruction progress; original applications still open; research-publication case not established. Reject the present dossier, while preserving the repaired lemmas and assessing any future focused research result on its own merits.**

This recommendation is not a claim that all active theorems are false, that the two local errata destroy the reconstruction, or that the remaining research targets are impossible.
