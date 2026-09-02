# External Referee Report on the Round-Thirty-One Revision

## Recommendation: **Reject all eleven manuscripts; return the present branch as unfinalized and do not invite another dossier-wide major revision**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round31-referee-positive-closure-11paper-2026-09-03`  
**Pre-review head:** `e41fe212e66e4e7af26087df0de23625e282c248`  
**Review branch:** `review/round32-gpt56-pro-harsh-11paper-2026-09-03`  
**Review date:** 3 September 2026  
**Scope:** the eleven active `ROUND31_POSITIVE_CLOSURE.tex` files and their wrappers, `AUTHOR_RESPONSE_ROUND30.md`, the Round-Thirty-One review index, proof-dependency ledger, mathematical-regression ledger, final-verification declaration, finalizer/hardener scripts, and the verification/publication workflows present at the reviewed head.

This report applies the correctness, self-containedness, significance, and presentation threshold expected at *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, or *Acta Mathematica*.

Round Thirty One is a genuine mathematical rewrite. It contains eleven new active theorem files and it addresses many of the explicit objections in the Round-Thirty report at the level of definitions. In particular, the revision distinguishes transition count from holding time, separates exact lattice fibres from summed cells, retains contact cycles, separates preparation from running action, and uses parameter-specific filters in the likelihood. These are real conceptual improvements.

The submitted branch is nevertheless not a valid final revision, and the active mathematics remains incorrect. There are two independent reasons.

First, the current head does not contain the finalized, hardened, remotely verified source that the repository says it contains. The last commits add one-shot patch scripts and workflows, but the patch markers and generated verification records are absent. The active source still contains the exact pre-hardening formulas those scripts were written to replace. The committed `ROUND31_FINAL_VERIFICATION.json` therefore does not describe the checked-in head.

Second, even before specialist-level questions are reached, the active manuscripts contain direct contradictions. Among them:

1. A2 imposes a Diophantine lower bound for every nonzero continuous frequency. The left side tends to zero as the frequency tends to zero, while the asserted right side tends to a positive constant.
2. A4 assumes only `B_Q(R) subset D(L_Q^3)` but claims an expansion through the `z^{-3}` coefficient with an `O(|z|^{-4})` remainder. The displayed resolvent identity gives only an `O(|z|^{-3})` remainder under the stated assumptions.
3. B2 defines `a_* = a_0 - Lambda T` and later assumes `a_0 > a_* + Lambda T`, which is the impossible inequality `a_0 > a_0`.
4. B2's proposed Ovsyannikov contraction integrates a `1/(t-s)` singularity. The corresponding time-simplex product is not integrable.
5. B4's ballistic compactification removes high-speed spatial oscillation but not high-speed collision-direction oscillation. A bounded amount of energy can change boundary direction by order one in a time tending to zero.
6. C1 contains literal control bytes in the active TeX source and therefore contradicts the branch's own printable-source and clean-build claims.
7. D1 writes a local density for a normalized continuous empirical variable without the required positive power of `N`; even an i.i.d. Gaussian mean contradicts the displayed normalization.

The remaining sections give the details and the paper-by-paper dispositions.

---

## 1. Confidential recommendation to the editor

I recommend **rejection of the complete eleven-paper dossier, without another dossier-wide major-revision invitation**.

I also recommend that the present Round-Thirty-One branch be marked **unfinalized** in the editorial record. The branch contains useful proposed repairs, but the checked-in head is not the source that its own one-shot finalizer, hardener, and publication workflow purport to certify. Referees must review committed mathematics, not a hypothetical future tree produced by an unexecuted workflow.

This recommendation is not based on ambition, style, or the number of papers. It is based on explicit false statements and empty theorem hypotheses in the root manuscripts. Once A2, A3, A4, B2, and B4 fail, all downstream filtering, rigidity, semigroup, and phase-synthesis claims lose their required inputs.

The proper editorial classification is not “promising work needing more details.” Several theorems are false as written, while several other “proofs” consist of assuming the difficult geometric or spectral conclusion as part of a certificate. A credible future submission should isolate one root theorem and develop it as a complete specialist paper.

---

## 2. Source identity and verification integrity

### 2.1 What is genuinely new

The Round-Thirty-One branch replaces all eleven active theorem sources and switches the wrappers to Round Thirty One. The review index identifies the active files unambiguously. I therefore reviewed those files, not the older Round-Twenty-Nine sources.

The author response is also unusually explicit about the intended repairs. This makes the mismatch between the intended final source and the checked-in source especially clear.

### 2.2 The finalizer and hardener have not materialized

At the reviewed head, all of the following expected artifacts are absent:

```text
.round31-finalized
.round31-hardened
ROUND31_CI_VERIFICATION.json
ROUND31_REMOTE_VERIFICATION.md
```

The head commit adds only the publication/verification workflow. Its immediate ancestors add the hardening workflow, the hardening script, the finalization workflow, the finalizer script, and the verifier. They do not contain commits produced by running those scripts against the active source.

This matters because the scripts themselves identify known defects in the active manuscripts and contain exact textual replacements for them. For example:

- the hardener changes A2's frequency condition from `b != 0` to `|b| >= 1`;
- the finalizer changes A4's memory input from `D(L_Q^3)` to `D(L_Q^4)`;
- the hardener replaces A4's relative-generation paragraph by a dissipative Lumer--Phillips argument with additional hypotheses;
- the hardener removes B1's assertion of conditional independence of disjoint anchor groups.

None of these replacements is present in the active source at the reviewed head.

### 2.3 The committed verification declaration is contradicted by the tree

`ROUND31_FINAL_VERIFICATION.json` states:

```text
source_materialization: complete
remote_ci: recorded by the GitHub Actions run attached to the final branch head
```

But the generated CI record is absent, the remote evidence file is absent, the finalization and hardening markers are absent, and the combined status endpoint for the reviewed head reports a pending state with no status contexts.

The file is therefore a declaration of intended status, not evidence of the checked-in status.

### 2.4 The active C1 source violates the verifier's own source gate

The active C1 source contains literal vertical-tab control bytes in the intended commands for the projective limit and a test function. The source appears as the equivalents of

```text
<U+000B>arprojlim
<U+000B>arphi
```

rather than valid TeX commands. The Round-Thirty-One verifier explicitly rejects control bytes below ASCII 32 other than tab/newline/carriage return. Thus either the active source has not passed that verifier, or the verification record corresponds to a different, uncommitted tree.

### 2.5 Editorial consequence

A build or verification claim must be reproducible from the exact submitted commit. Here the branch itself demonstrates that known source corrections were deferred to future self-modifying workflows. That is not an acceptable submission protocol for a mathematical journal.

The remainder of this report nevertheless reviews the actual active source on its own terms. The verdict would remain rejection even if the absent script patches were applied.

---

## 3. Direct contradictions in the root statements

### 3.1 A2: the stated Diophantine inequality is impossible near zero

A2 assumes that for fixed vectors `beta_j` and constants `c_D, nu_D > 0`,

```text
dist(b dot beta, 2 pi Z^{d_c+1})
    >= c_D (1+|b|)^{-nu_D},       b != 0.
```

Take any nonzero vector `v` and put `b=t v`. For sufficiently small `t`, the nearest lattice point is zero, so

```text
dist(t v dot beta, 2 pi Z^{d_c+1})
    <= t C_beta |v| -> 0.
```

The right side tends to `c_D > 0`. The inequality fails for every sufficiently small positive `t`.

Thus the “exact Diophantine arithmetic leaf” defined by the displayed hypothesis is empty. The branch's unexecuted hardener correctly attempts to restrict the condition to `|b| >= 1`, but a proposed patch is not part of the active theorem.

This alone invalidates A2, and hence every theorem importing A2's Fourier and Edgeworth estimates.

### 3.2 A4: the claimed fourth-order memory remainder does not follow

A4 assumes

```text
B_Q : R -> D(L_Q^3)
```

and writes, for `y=B_Q r`,

```text
(z-L_Q)^{-1} y
 = z^{-1}y + z^{-2}L_Q y + z^{-3}L_Q^2 y
   + z^{-3}(z-L_Q)^{-1} L_Q^3 y.
```

On the stated vertical half-plane the resolvent is only asserted to be uniformly bounded on the Hilbert space. Therefore the final term is

```text
O(|z|^{-3}),
```

not `O(|z|^{-4})`. Applying the Hilbert-bounded observation `C_Q` does not create an additional factor of `|z|^{-1}`.

To obtain the displayed expansion

```text
Khat(z)=z^{-1}C_QB_Q+z^{-2}C_QL_QB_Q
        +z^{-3}C_QL_Q^2B_Q+O(|z|^{-4}),
```

one needs one more resolvent identity and hence `B_Q(R) subset D(L_Q^4)`. The absent finalizer makes exactly that change. The active theorem is false as written.

### 3.3 A4: the relative-generation lemma lacks a generation theorem

The active lemma assumes a stable generator `L_0`, a relatively closed map `A:D(L_0)->H`, and

```text
sup ||A(z-L_0)^{-1}|| < 1
```

on a half-plane. It then says that differentiating the resolvent identity supplies the Hille--Yosida powers and that inverse Laplace transformation yields a semigroup with exponential decay.

That conclusion does not follow from the stated hypotheses. Uniform invertibility of the Neumann factor supplies a candidate resolvent, but Hille--Yosida generation requires the appropriate power estimates or an equivalent dissipativity/range theorem. Differentiating a bounded resolvent formula does not automatically produce the fixed-constant Hille--Yosida estimates. Nor does relative closedness alone give the dissipativity required for the claimed decay.

Again, the unexecuted hardener acknowledges the problem: it adds relative boundedness, dissipativity of a shifted operator, and a Lumer--Phillips range argument. Those hypotheses and that proof are absent from the active source.

### 3.4 B2: the finite-time theorem has an empty hypothesis

B2 defines

```text
a(t)=a_0-Lambda t,
a_*=a_0-Lambda T.
```

Its finite-time propagation theorem then assumes

```text
a_0 > a_* + Lambda T.
```

Substitution gives

```text
a_0 > (a_0-Lambda T)+Lambda T = a_0.
```

No parameter satisfies this strict inequality. The theorem is vacuous.

This is not a subtle analytic gap. It is a one-line algebraic contradiction in the principal hard-sphere propagation theorem.

### 3.5 B2: the claimed Ovsyannikov contraction integrates a nonintegrable kernel

The proof chooses an intermediate radius whose gap from the source radius is proportional to `t-s`. The creation estimate therefore costs

```text
C/(t-s).
```

But

```text
integral_0^t ds/(t-s) = infinity.
```

The weight `(a(t)-a_*)` depends on the final time and does not cancel the singularity along the integration diagonal `s=t`.

The displayed `n`-creation estimate has the product

```text
product_j [a(t_{j-1})-a(t_j)]^{-1}
 = Lambda^{-n} product_j (t_j-t_{j-1})^{-1}.
```

Its integral over the ordered time simplex diverges at every collision of adjacent times. The manuscript's assertion that the optimized simplex integral is summable is therefore false for the displayed majorant.

There is a second endpoint defect: at `t=T`, one has `a(t)-a_*=0`, so the norm used in the fixed-point argument gives no endpoint control, while the displayed bound for `||K_t||_{a(t)}` blows up. It cannot imply uniform convergence in the fixed radius `a_*` later claimed by the propagation theorem.

### 3.6 B4: ballistic spatial collapse does not control fast collision-direction changes

B4 collapses spatial position at infinite velocity but retains the direction of the energy recession measure. This removes the familiar free-flight counterexample, but it does not remove the collision counterexample.

Consider a state consisting of a regular slow background plus mass

```text
delta_R = R^{-2}
```

near velocity `R e_1`. The total kinetic energy of the fast component is of order one. Under the unforced collision law `q=1`, the running action is zero.

A fast particle collides with the background at rate of order `R`. The total event rate contributed by the fast mass is therefore of order

```text
delta_R R = R^{-1}.
```

Each non-grazing equal-mass collision redistributes an amount of energy of order `R^2` among new velocity directions. Consequently the time derivative of a continuous boundary-direction energy test is of order

```text
R^{-1} R^2 = R.
```

Over times `t_R=c/R -> 0`, the boundary energy-direction measure can change by order one while total energy remains fixed and the action remains zero.

Therefore the family is not equicontinuous in the proposed ballistic energy topology. This refutes the claimed path compactness and shellwise strong continuity. Collapsing spatial phase at infinity is insufficient; one would also need a topology or estimate controlling the collision-induced angular motion of recession energy.

The proof's collision estimate reveals the same issue. The contact measure already contains one factor `|v-v_*|`, while an energy-direction increment can be of order `|v|^2+|v_*|^2`. A second-moment bound alone does not control the resulting high-velocity integral.

### 3.7 D1: the normalized continuous variable has the wrong local-density power

D1 defines

```text
bar xi_N=(K_N/N,Y_N)
```

and later uses the fluctuation

```text
sqrt(N)(Y_N-y_j).
```

Thus `Y_N` is a normalized empirical quantity. But its labelled local density is written with only the lattice single-site factor `N^{-d_Z/2}` and no positive factor from the normalized continuous coordinates.

Take the elementary case `d_Z=0`, one phase, and `Y_N` equal to the mean of i.i.d. standard Gaussians. Its density is

```text
p_N(y)=sqrt(N/(2 pi)) exp(-N y^2/2).
```

At the minimizer, the density grows as `N^{1/2}`. D1's formula gives an order-one density. Integrating its formula over the natural `N^{-1/2}` neighbourhood gives probability of order `N^{-1/2}`, although the true probability is order one.

In `d_R` continuous dimensions, the missing Jacobian is `N^{d_R/2}`. Equivalently, converting the A2/B1 local theorem for an unnormalized sum to a density for the normalized mean multiplies by `N^{d_R}`. The polynomial exponents in D1's Morse--Bott formula are therefore not consistently normalized.

---

## 4. Paper-by-paper assessment

## A1 — buffered current response and Hilbert limits

The common reporting space is a sensible response to the previous covariance typing problem. The paper nevertheless remains incomplete.

### Major objections

1. The coherent jet relation is stated with `J^{(j+1)}` while the jet is only declared through order `r`. At the top order the defining equation is not typed unless the range is explicitly restricted to `j<r`.
2. The boundary shells are introduced independently at each derivative level, but the compatibility relations obtained by differentiating one shell family into the next are not stated. The later Bell expansions require precisely those relations.
3. The passage from weak material derivatives against transported tests to strong `C^r` differentiability in the common Hilbert space is compressed into a sentence. Weak boundedness of difference quotients is not norm convergence.
4. The seam-current projection estimate assumes that the current norm of a depth-`n` geometric sheet is proportional to its Bernoulli branch probability. A geometric current is not automatically probability weighted. The manuscript does not construct the random seam observable in a way that proves this factor.
5. The assertion that `P_0Y_q` can see only sheets of depth at least `|q|` needs an exact measurability/ancestry lemma. It is the decisive Maxwell--Woodroofe hypothesis and is not established by the stated product identity.
6. Covariance response differentiates conditional projections and an infinite score series. The necessary derivative bounds for the one-sided projection operators are asserted rather than proved.

### Disposition

**Reject.** A1 is less internally contradictory than several root papers, but it remains a compressed proof programme rather than a complete functional-analytic/probabilistic theorem.

---

## A2 — Sinai arithmetic, Fourier estimates, and Edgeworth expansion

### Major objections

1. The impossible small-frequency Diophantine inequality in Section 3.1 makes the declared arithmetic leaf empty.
2. The nonemptiness proof for `d_c=2` is dimensionally unexplained. Three scalar normal displacements are said to prescribe three vectors in `R^2`; that is six scalar target conditions. No six-dimensional parameter map or rank calculation is given.
3. The finite automaton, returned-UNI blocks, terminal nonstationarity charts, and their spectral-radius comparison are not constructed for the proposed billiard table. They are the hard global billiard geometry, not routine consequences of a finite subcover.
4. The claim that every terminal bad word has a nonstationary impact coordinate is not proved. Singular billiard branches can lose precisely such uniform transversality.
5. The intermediate-frequency cone contraction is reduced to one paragraph and does not verify the anisotropic strong/weak norm, matched-curve distortion, parameter derivatives, and singularity cuts required at every block.
6. The Edgeworth theorem requires a sixth-order eigenvalue expansion, fourth-order amplitude expansion, and four source derivatives uniformly on a singular billiard family. The active source contains no perturbation calculus at that level.

### Disposition

**Reject.** The theorem class is empty as written, and the principal operator estimates are not proved independently of the certificate language.

---

## A3 — transition entropy, chronological currents, and stopped local theory

The separation of transition count from holding occupation is correct in principle. The new two-scale current is not correctly defined.

### Major objections

1. The symbol `nu_N` is used both for the stopping count and for the transition-count occupation measure. This makes several formulas formally self-referential.
2. The incoming/outgoing measures use the indices `h_{k-1 plus/minus 1}`. Thus the alleged outgoing/incoming difference is `delta_{h_k}-delta_{h_{k-2}}`, not the one-step difference `delta_{h_k}-delta_{h_{k-1}}`. Summing it gives two endpoint layers and a factor-two-type bulk effect, not the declared divergence law.
3. The object `div_U J` is not typed. The current `J_N` as defined carries only a time and history coordinate, while the append map `U` requires both a history and a mark.
4. The tightness of `N delta_N(nu_N^+-nu_N^-)` in an `H^{-1}` history-distribution space is not proved. The entropy/mark moment controls mass, not the cancellation required after multiplication by `N delta_N`.
5. The converse recovery theorem claims that arbitrary limiting currents satisfying the displayed equations can be realized by legal finite-memory words. No integrality, orientation, endpoint, or compatibility theorem for that current is supplied.
6. The fractional conditional exponential moment with exponent `zeta<1-rho` is declared to follow from A2, but A2 proves no complete-past conditional estimate of that form.
7. In the conditioned-path corollary, the numerator contains a path source and therefore generally has different Riesz vectors and a different terminal matrix amplitude from the denominator. The amplitudes do not literally cancel. At exponential scale they may be negligible, but that is a different argument and requires uniform positive bounds.

### Disposition

**Reject.** The correct entropy clock is a useful repair, but the new chronological state, current equation, and stopped conditioning theorem are not established.

---

## A4 — weak Harris theory, renewal, compression, and memory

### Major objections

1. The relative-generation lemma is unsupported under its active hypotheses, as explained in Section 3.3.
2. The memory remainder is false under `D(L_Q^3)`, as explained in Section 3.2.
3. The compression theorem invokes the relative-generation lemma without restating all of its hypotheses for the concrete perturbation `A_P`; in particular, no dense-domain, closedness, or Hille--Yosida power verification is supplied.
4. The graph-angle isomorphism is assumed rather than constructed for the physical projection. Equality of finite ranks does not by itself give an isomorphism between the complementary graph domains.
5. The weighted weak-Harris theorem jumps from Wasserstein contraction for a capped cost to an operator spectral gap in a different unbounded weighted Hölder norm. This transfer requires a detailed coupling derivative estimate that is not present.
6. A “certified potential bridge” includes uniform irreducibility and a contour separating the positive eigenvalue from the rest of the spectrum. That certificate already contains the difficult spectral conclusion needed by C2. The paper does not construct such bridges for the unbounded sequence of exposing potentials.
7. The renewal formula is more coherently typed than in earlier versions, but no proof is given that `A(z),B(z),T(z)` act boundedly on the exact anisotropic/weighted spaces throughout the claimed continuation region.

### Disposition

**Reject.** Two central displayed theorems are false as written and the finite-amplitude spectral interface is conditional on the desired result.

---

## B1 — exact preparation and quadratic anchors

### Major objections

1. The active proof still says that disjoint anchor groups are conditionally independent up to a smooth hard-core factor. They are not conditionally independent: hard-core exclusion couples all anchor positions. Smooth coupling may permit iterated stationary phase, but that requires uniform mixed derivative estimates, not an independence assertion.
2. The number of reserved particles is stated only as `m_0>=7`, while the proof later chooses arbitrarily many disjoint anchor groups to exceed a prescribed Fourier exponent. The dependence of `m_0`, the constraint dimension, the source derivative order, and the thermodynamic scaling is not specified.
3. Uniform stationary-phase constants are claimed for every non-anchor exterior configuration. Exterior particles can make the allowed anchor domain arbitrarily thin, split it into many components, or approach a hard-core tangency. No uniform clearance/non-jamming theorem is proved.
4. The compact Maxwellian truncation used for stationary phase creates a tail error. There is no estimate showing that this error is uniform at the `N^{-1}` Edgeworth scale after four source derivatives.
5. The good-block event is called non-anchor measurable while the exact total momentum/energy conditioning couples anchors and non-anchors. The conditional density after exact-number and microcanonical disintegration is not shown to retain the asserted event independence.
6. The sixth-order saddle expansion and global activity modulus gap are imported from B2, whose pressure and finite-time propagation fail.

### Disposition

**Reject.** The equal-velocity degeneracy is recognized, but the proposed uniform anchor mechanism is not proved on the hard-sphere conditional ensemble.

---

## B2 — collision histories, pivots, Ovsyannikov evolution, and the dynamic LDP

This is the hard-sphere root paper. It contains the most decisive defects in the dossier.

### Major objections

1. The finite-time propagation theorem has the impossible hypothesis `a_0>a_0`, as shown in Section 3.4.
2. The fixed-point kernel `1/(t-s)` is not integrable, and the displayed time-simplex product diverges, as shown in Section 3.5.
3. The norm used in the fixed-point argument degenerates at `t=T`; the estimate gives no endpoint control and cannot imply convergence at radius `a_*`.
4. The tree right inverse has norm growing like `epsilon^{-2(K-1)}`. The manuscript never shows that projecting an ambient surplus variation through this inverse leaves a diagonal surplus derivative bounded below independently of `epsilon`. The projection may amplify or cancel the desired direction.
5. The conormal argument asserting that every diagonal failure is exactly grazing, simultaneous contact, collinear fork, or zero relative velocity is not proved. Hard-sphere genealogies have additional algebraic dependencies, repeated labels, and symmetry degeneracies.
6. In the singular-set estimate the constants depend on the velocity cutoff `L`, but the proof then chooses `L=sqrt(|log epsilon|)` without controlling that dependence. A constant growing faster than any fixed power can destroy the claimed positive `epsilon` exponent.
7. The assertion that a simultaneous pivot flow has a common rectangular domain after a finite partition is unsupported. Flows of different tangent vector fields need not commute and can leave chronology charts.
8. The logarithm in the history algebra and its identification with connected deterministic collision histories are asserted without proving convergence on the time-dependent radius scale.
9. The final pressure/LDP theorem is a large promotion: local projective pressure convergence, a recovery sketch, and a Chernoff sentence do not by themselves give exponential tightness and a full projective lower bound for deterministic hard-sphere trajectories.

### Disposition

**Reject.** The principal finite-time theorem is vacuous and its proposed analytic-radius proof contains a divergent integral. Hence B2 exports no valid pressure or LDP to B1--B4.

---

## B3 — kinetic fluctuations and the full contact Hessian

The normal/cycle split is a mathematically appropriate repair. The process proof remains invalid.

### Major objections

1. The passage from scalar cumulants to Hilbert-norm moments invokes a Hilbert--Schmidt embedding `S_m -> S_{m-2}`. A fixed two-order weight gap is not Hilbert--Schmidt in the full Fourier--Hermite--angular mode dimension used here; increasing `m` does not change the summability exponent of the embedding.
2. The dyadic chaining proof ignores the microscopic remainder in the moment estimate. At level `j` there are `2^j` increments, so the contribution `2^j mu_epsilon^{-p/2}` cannot be summed over all `j>=J` for fixed `epsilon`.
3. A maximum-jump estimate does not repair that infinite-level sum without an explicit `epsilon`-dependent terminal grid and a separate oscillation bound below it.
4. The deterministic-interval connected-graph estimate counts a first collision vertex in the interval, but density increments also contain free transport. That part is not represented by the same collision-vertex factor.
5. The conditional drift estimate is stated in a weaker space, but the chaining silently combines it with the martingale increment in a stronger path metric.
6. Process tightness is therefore not established, and neither the joint Gaussian martingale problem nor the covariance/Mosco identification follows.
7. The global near-Maxwellian graph estimate is again a one-paragraph perturbation of a difficult hypocoercive result; domains, velocity weights, boundary conditions, and time-dependent commutators are not verified.

### Disposition

**Reject.** The static Hessian formula is plausible, but the microscopic process CLT and the closed graph theorem are not proved.

---

## B4 — ballistic compactification and nonlinear semigroups

### Major objections

1. The fast-collision boundary counterexample in Section 3.6 refutes path compactness and shellwise strong continuity.
2. The compact shell permits arbitrary mass measures on the compactified velocity boundary, although positive mass at infinite velocity cannot be approximated by probability measures with a uniformly bounded finite kinetic energy. The actual closure of finite-energy states is not characterized.
3. The Hamiltonian is defined only through finite-velocity collision integrals. No generator is defined on boundary recession states, despite the semigroup being claimed on the entire compact shell.
4. The proof controls high-speed free transport because boundary energy tests forget position, but it does not control high-speed collision changes because those tests retain velocity direction.
5. The contact-current compactness argument controls only compact velocity sets. Boundary energy does not determine the limiting contact current or its entropy cost at infinity.
6. The canonical microscopic realization is defined by finitely many expectation constraints. It does not construct microscopic approximations of an arbitrary boundary-recession state, nor does it prove that the B1 saddle remains uniform along the diagonal number of constraints.
7. The viscosity comparison proof on the compactified shell is schematic. The collision Hamiltonian is not shown continuous at the boundary, which is precisely where the direct counterexample produces order-one motion.

### Disposition

**Reject.** The topology repairs free-flight compactness but fails for the collision dynamics the paper studies.

---

## C1 — stratified observations, projective derivatives, and adaptive BvM

### Major objections

1. The active source contains control bytes and is not a clean TeX source. This alone contradicts the branch's final-verification declaration.
2. The projective distribution space is written as an inverse/projective limit of dual cylinder spaces without specifying the bonding maps, locally convex topology, completeness, or measurable embedding of probability beliefs.
3. Pointwise convergence of difference quotients on every cylinder plus boundedness does not imply convergence in the asserted projective distribution topology.
4. The observable Gram inequality is imposed uniformly over all reachable beliefs and parameter tangents. No mechanical/noise example is shown to satisfy it.
5. A lower Fisher-information bound for induced observation laws does not by itself imply the Riccati contraction (C1.15) for normalized filtering derivatives. That is a separate nonlinear filter-stability theorem; the one-paragraph “completing the square” argument is insufficient.
6. A policy is required to select each of several length-`m_0` diagnostic words conditionally with positive probability. The scheduling, overlap, and sum constraints for these incompatible words are not defined.
7. The Bernstein--von Mises theorem assumes exactly the uniform recursive QMD, stable information, global testing, and annular estimates that remain unproved. In an adaptive partially observed model these are not consequences of a local Gram inequality alone.

### Disposition

**Reject.** The whole-channel normalization is repaired, but the filter derivative and adaptive statistical theory are not established on the actual infinite-dimensional hidden state.

---

## C2 — strict duality, rigidity, likelihoods, and optional projections

The strict-topology pullback is the strongest isolated component of this paper. The synthesis theorem remains unsupported.

### Major objections

1. The quantitative filter-stability lemma claims a linear bounded-Lipschitz estimate for the full path prediction. C1 contracts only an observable quotient; latent directions are merely transported continuously. Continuity gives a modulus, not the displayed linear bound, unless additional Lipschitz/observability hypotheses are imposed.
2. Assumption (P1) gives primitive-kernel convergence, while (P4) gives only a moment bound. The proof nevertheless says primitive characteristic convergence is contained in (P1). Second predictable characteristics do not follow from weak kernel convergence plus bounded moments without convergence of the corresponding second-moment kernels.
3. The optional-projection theorem for every bounded continuous functional on Skorokhod path space requires a uniform compact approximation by cylinder functions. This is nontrivial and not proved by path tightness alone.
4. The discrete likelihood formula is correct only when the action policy contributes the same parameter-independent conditional likelihood under numerator and denominator. That restriction is not stated in the proposition.
5. The rigidity theorem is conditional on certified bridges whose certificates already include a separated Riesz contour and irreducibility at every point. It does not prove that the exposing potentials needed for periodic localization possess such bridges.
6. The three BSDE theorems state familiar stability conclusions but do not specify the exact filtrations, martingale representation spaces, monotonicity/integrability conditions, or topology needed for the claimed joint convergence.
7. Every stochastic conclusion imports the unproved C1 filter stability and the failed A3/B3 path limits.

### Disposition

**Reject.** A strict-duality lemma might be salvageable as a separate note; the rigidity/filter/BSDE package is not established.

---

## D1 — phase weights and common-policy asymptotics

### Major objections

1. The continuous normalization error in Section 3.7 invalidates the phase coefficients.
2. A2 and B1 export central local expansions for selected additive sums. They do not export the labelled large-deviation local density

   ```text
   exp(-N I_j(k/N,y)) [a_j+N^{-1/2}b_j+N^{-1}c_j+...]
   ```

   uniformly over entire phase cells with a phase label `J_N` and a `C^5` Morse--Bott minimizer manifold.
3. The paper assumes sixth-order normal forms and four source derivatives uniformly in a policy-dependent family, although the upstream papers do not construct those phase labels or manifolds.
4. A finite-memory adaptive policy changes transition kernels recursively. It is not generally equivalent to inserting one fixed finite-dimensional Feynman--Kac source vector into an uncontrolled local theorem.
5. The causal finite-memory approximation gives only an `O(N epsilon_m)` logarithmic error. The simultaneous choice `N epsilon_{m(N)}=o(1)` with subpolynomial growth of all chart derivatives is assumed, not derived from a summable memory modulus.
6. The “uniform second epi-development” used for the final lexicographic selection is essentially the desired subleading optimization theorem restated as an assumption.
7. The complex zero-free and Gaussian coexistence conclusions inherit unavailable phasewise analytic expansions from the same unproved local input.

### Disposition

**Reject.** The fibre/cell distinction is conceptually correct, but the active normalization and upstream interfaces do not support the theorem.

---

## 5. Dependency-level consequence

The repository ledger is acyclic as a diagram, but the mathematical exports do not exist at the claimed strength.

### A-chain

- A2's arithmetic class is empty under its displayed small-frequency bound.
- A2 therefore supplies no Fourier or Edgeworth theorem.
- A3 loses its stopped local input and independently has an ill-defined two-scale current.
- A4 imports the failed A3 drift/state and contains independent false generation and memory statements.
- C2 rigidity and D1 phase asymptotics consequently lack their billiard inputs.

### B-chain

- B2's finite-time theorem has an impossible hypothesis and its fixed-point integral diverges.
- B2 supplies no grand-canonical pressure or dynamic LDP.
- B1 therefore lacks its upstream pressure and exact-number analytic saddle.
- B3 lacks the connected cumulants needed for its process theorem and has an invalid chaining proof in any event.
- B4 lacks the microscopic tree limit and also fails independently under the fast-collision compactification counterexample.

### Synthesis chain

- C1's derivative/filter/BvM theory is not established and its active source is not clean.
- C2 imports failed A3, A4, B3, and C1 statements.
- D1 imports unavailable Edgeworth/phase data and has an independent density-normalization error.

None of the eleven papers is therefore ready for publication.

---

## 6. What the revision does improve

For completeness, the following changes should be retained in any future reconstruction:

- A1's use of a common weak Hilbert reporting level is the correct way to type derivative-loss covariance tensors.
- A3 correctly distinguishes transition-count entropy from holding occupation.
- A3 correctly refuses to impose scalar independence of the renewal overshoot.
- B3 correctly retains positive-cost contact cycles in the joint theory.
- B4 correctly separates initial preparation entropy from the running action.
- C1 correctly introduces stratum-selection probabilities and an exact Radon--Nikodym envelope factor.
- C2 correctly uses parameter-specific filters in the discrete hidden-model likelihood.
- D1 correctly distinguishes an exact lattice fibre from a summed lattice cell and treats policy choice as optimization rather than integration.

These are useful design corrections. They do not compensate for false root theorems.

---

## 7. Minimum requirements for a scientifically meaningful future submission

A further simultaneous rewrite of all eleven papers is not an efficient or credible route. A future submission should satisfy the following minimum requirements.

1. **Freeze and verify one immutable source tree.** No mathematical correction may be deferred to a workflow that rewrites the submitted branch. The exact reviewed commit must contain the final source, build record, and source hashes.
2. **Submit one root paper.** Choose A2 or B2. Do not resubmit the dependent memory, filtering, semigroup, and phase papers until the root result has survived specialist review.
3. **For A2, state a nonempty arithmetic condition.** Separate the central-frequency regime from the large-frequency Diophantine bound and construct the periodic data, grammar, UNI blocks, and bad-word charts for one concrete billiard.
4. **For A2, provide the full anisotropic proof.** The stable-curve spaces, singularity partitions, matched branches, source derivatives, and every Fourier range must be treated in detail.
5. **For A3, replace the two-scale current by an exact typed discrete complex.** Fix the off-by-one indices, define the mark-valued current and its divergence, and prove exponential tightness and recovery in the actual topology.
6. **For A4, use a valid generation theorem.** State all domain, relative-bound, dissipativity, and range hypotheses. Correct the memory regularity order and prove the physical projection satisfies them.
7. **For B2, repair the analytic-radius argument.** Use a standard scale-of-spaces theorem with an integrable allocation of radius loss; the displayed `1/(t-s)` contraction cannot be used.
8. **For B2, prove collision rank without circular certificates.** Give a complete finite-graph coordinate theorem including label repetitions, chronology changes, singular strata, and explicit dependence on `epsilon`, `K`, and velocity cutoffs.
9. **For B3, prove process tightness with an epsilon-dependent terminal grid.** Show the Hilbert embeddings are genuinely Hilbert--Schmidt and control the microscopic remainder uniformly across dyadic levels.
10. **For B4, control recession collisions.** Either collapse enough boundary information to make collision dynamics continuous or propagate a stronger tail moment that excludes the fast-collision counterexample. Define the Hamiltonian on every state in the claimed semigroup domain.
11. **For C1, define the projective distribution space rigorously.** Remove control bytes, specify bonding maps/topology, and prove a genuine nonlinear filter derivative-stability theorem for a nonempty model class.
12. **For C2, separate conditional lemmas from model theorems.** State exact filter, characteristic, policy, and martingale-representation hypotheses and verify them in C1/A3/B3 rather than importing them by name.
13. **For D1, fix the density normalization.** Derive phase coefficients from an upstream labelled local theorem with consistent normalized/unnormalized variables before introducing policy optimization.
14. **Provide theorem-level literature interfaces and full proofs.** Terms such as “standard Ovsyannikov,” “Kawashima,” “weak Harris,” “Edgeworth,” “Dawson--Gartner,” “Riccati,” and “BvM” must refer to exact results whose hypotheses are checked on the active spaces.
15. **Use multiple independent specialists.** The billiard, hard-sphere, kinetic, filtering/statistics, and nonlinear-semigroup components require different expert referees.

These are reconstruction requirements, not a finite major-revision checklist for the present dossier.

---

## 8. Final verdict

Round Thirty One is more mathematically aware than the preceding revisions. It repairs several old definitions and records a clearer dependency structure.

It is not a completed proof package. The current branch is internally inconsistent about its own finalization and verification, and its active sources contain:

- an impossible A2 Diophantine hypothesis;
- a false A4 memory remainder;
- an unsupported A4 generation theorem;
- an empty B2 propagation hypothesis;
- a nonintegrable B2 fixed-point kernel;
- an invalid B3 infinite-level chaining argument;
- a B4 compactification defeated by fast collisions;
- malformed C1 source bytes and an unproved nonlinear derivative filter;
- unsupported C2 filter/characteristic convergence;
- and a D1 local-density normalization contradicted by the Gaussian mean.

These failures occur in the root nodes and propagate throughout the eleven-paper dependency graph. Compilation, theorem labels, patch scripts, and workflow declarations do not change the mathematical verdict.

**Recommendation to the editor: reject all eleven manuscripts, return the Round-Thirty-One branch as unfinalized, and do not invite another dossier-wide major revision. Any future submission should be a substantially reconstructed, immutable, self-contained root paper with complete proofs and independent specialist verification.**
