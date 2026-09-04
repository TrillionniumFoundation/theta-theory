# External Referee Report on the Round-Thirty-Nine Revision

## Recommendation: **Reject for Annals/Inventiones/JAMS/Acta-level publication; the principal policy-uniform theorem is false for the frozen admissible class**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round39-adaptive-jacobi-identification-gpt56pro-2026-09-04`  
**Immutable reviewed head:** `1f1409c10d4444ef38c746e12ce426520d7f1ef5`  
**Reviewed source tree:** `f0f3b7e50dfef527100fa28cc62987b41a6c5152`  
**Controlling preceding report:** `REFEREE_REPORT_ROUND38_GPT56_PRO_ADVERSARIAL.md` at commit `39d9622406d4a50680992836ee1f70e970d6d627`  
**New review branch:** `review/round40-gpt56-pro-harsh-round39-jacobi-2026-09-04`  
**Review date:** 4 September 2026  
**Reviewer:** GPT-5.6 Pro, at the repository user's request.

This is an AI-assisted independent referee-style assessment. It is not a report commissioned by, and it is not an editorial decision of, *Annals of Mathematics*, *Inventiones Mathematicae*, the *Journal of the American Mathematical Society*, or *Acta Mathematica*. I apply the correctness, originality, depth, breadth, self-containment, and lasting-significance threshold appropriate to those journals.

---

# Executive verdict

Round Thirty Nine is a substantial mathematical rewrite, not a cosmetic response to Round Thirty Eight. The author has done several things that the previous report explicitly requested:

- the adaptive experiment is written with an action-before-noise filtration;
- uniform stochastic orders are defined over a triangular experiment class;
- the random-information Laplace normalization is isolated as a lemma;
- initial-state misspecification is called quasi-Bayesian and a pseudo-true parameter is discussed;
- the five-parameter homogeneous lattice identifies the bath damping and pinning as well as the boundary coefficients;
- filter derivatives are assigned an explicit Banach-dual topology;
- the memory kernel is pushed through the parameter posterior by a functional delta argument;
- a second experiment treats a complete infinite Jacobi coefficient sequence; and
- the manuscript no longer calls finite preparation weights thermodynamic phases.

I also independently checked the finite local algebra at the level needed for a referee reading. The displayed response jets through `r_7`, the triangular inverse for

\[
(c,k,\epsilon,c_b,k_b),
\]

the generalized Vandermonde interpolation mechanism, and the scalar Jacobi Schur recursion are mutually consistent. The abstract random-information Laplace argument is materially better written than in Round Thirty Five. I do not find a responsible basis for saying that the entire paper is fabricated or that every central calculation is false.

The frozen Round-Thirty-Nine submission is nevertheless not correct as stated. Its principal five-parameter empirical-contrast theorem admits a direct counterexample because the admissible policy class combines two assertions:

1. calibration slots are required only to have “lower density” \(\rho\); and
2. policies are expressly allowed to depend on the terminal sample size \(n\).

For every terminal size \(n\), take a policy with **no calibration slot among the first \(n\) observations**, and make every slot after \(n\) a calibration slot. This is a predictable infinite policy whose asymptotic lower calibration density is one. On the observed horizon, choose zero force on all exploitation blocks and take the true initial state to be zero. Then

\[
 m_i^\vartheta=0
 \quad(1\le i\le n,\;\vartheta\in\Theta),
\]

so the empirical contrast and the realized information matrix are identically zero. This contradicts Proposition `prop:balanced-contrast` with probability one. It also destroys the claimed uniform root-\(n\) quasi-Bernstein--von Mises theorem for that admissible sequence of policies.

This is not an interpretation invented by the referee. The repository contains an unexecuted workflow, `.github/workflows/finalize-round39-sources.yml`, whose intended source patch replaces “lower density” by the finite-prefix condition

\[
N_{\rm cal}(m)\ge \rho m-C_{\rm cal}
\quad\text{for every }m,
\]

and introduces common exploitation-force and duration bounds. That workflow failed and did not commit its changes. A proposed future patch is not part of the frozen manuscript.

The second, genuinely infinite-dimensional posterior theorem also has an incomplete proof. Its uniform strong law is obtained from a finite \(L^2(\omega)\) net. The displayed Doob estimate controls one fixed approximation error, but the proof then takes a supremum over the uncountable collection of errors in each net ball without a bracketing, entropy, or chaining argument. Total boundedness in \(L^2\) alone does not justify that step. In this particular model a repair may be available from the stronger compactness of the response family in \(C([0,T])\), but the repair is not the proof on the page.

There are additional frozen-source defects: the infinite Jacobi parameter space uses an undeclared upper endpoint \(b_+\); the five-parameter application asserts that every block duration is at least \(\tau\), although the policy paragraph imposes that duration restriction only on calibration blocks; the filter theorem inherits the same false time lower bound; and every remote Round-Thirty-Nine workflow at the reviewed head ended in failure before executing a recorded step.

Even after the obvious repairs, the manuscript would not meet the standard of the four journals named above. The five-parameter part remains a regular finite-dimensional Gaussian inference theorem under engineered calibration. The infinite Jacobi part combines classical Weyl-function uniqueness with compact product-topology posterior consistency under i.i.d. diagnostic durations and washout times growing linearly with the experiment index. It gives no contraction rate, no quantitative inverse stability, no uncertainty quantification for the infinite sequence, and no adaptive design theorem for that sequence.

My recommendation is therefore:

> **Reject. Do not invite a major revision at Annals/Inventiones/JAMS/Acta level.**

A corrected and substantially reframed specialist paper may be worth considering in inverse problems, systems and control, spectral theory, or mathematical statistics. Such a paper should be treated as a new submission after the exact frozen-source errors and proof gaps below are repaired.

---

# 1. What was reviewed

The repository contains three Round-Thirty-Nine revision branches. I did not select one merely from its timestamp.

- `revision/round39-adaptive-boundary-spectral-closure-2026-09-04` points to the preceding Round-Thirty-Eight review state and is not a new mathematical manuscript.
- `revision/round39-adaptive-jacobi-identification-2026-09-04` contains a supersession pointer and is expressly not the complete submission.
- `revision/round39-adaptive-jacobi-identification-gpt56pro-2026-09-04` is declared to be the canonical complete revision and is the branch reviewed here.

I froze the review at commit

```text
1f1409c10d4444ef38c746e12ce426520d7f1ef5
```

and tree

```text
f0f3b7e50dfef527100fa28cc62987b41a6c5152.
```

The principal materials inspected were:

- `ROUND39_REVISION.tex`;
- `round39/introduction.tex`;
- `round39/triangular.tex`;
- `round39/lattice.tex`;
- `round39/filter_memory.tex`;
- `round39/infinite_jacobi.tex`;
- `round39/preparations_verification.tex`;
- `round39/appendix_uniformity.tex`;
- `round39/references.tex`;
- `AUTHOR_RESPONSE_ROUND38.md`;
- `ROUND39_REVIEW_INDEX.md`;
- `ROUND39_READY_FOR_REVIEW.md`;
- `round39/PROOF_LEDGER.json`;
- `round39/SOURCE_MANIFEST.json`;
- `ROUND39_LOCAL_VERIFICATION.json`;
- `tests/test_round39.py`;
- `tools/verify_round39.py`;
- the three Round-Thirty-Nine workflows and their recorded runs; and
- the branch and commit history connecting Round Thirty Eight to Round Thirty Nine.

Relative to the Round-Thirty-Eight report commit, the canonical branch contains approximately twenty-three new commits and a complete new source packet. I therefore reviewed its new claims rather than mechanically repeating the Round-Thirty-Eight assessment of the older two-parameter model.

---

# 2. Confidential recommendation to the editor

## 2.1 Decision

**Reject without a top-four major-revision invitation.**

There are two independent reasons.

First, the frozen manuscript contains a direct counterexample to the policy-uniform empirical-contrast proposition on which its five-parameter BvM, evidence, state-filter, and memory-posterior conclusions depend. A central theorem is therefore false for the class actually stated.

Second, once the policy class is repaired, the paper still lacks the conceptual scale required for a top-four general mathematics journal. Its two substantive packages are:

1. finite-dimensional regular Bayesian asymptotics for five coefficients of a stable bounded lattice under prescribed calibration windows; and
2. classical inverse Jacobi uniqueness followed by qualitative posterior consistency in a weak compact product topology under an experiment with linearly increasing washout.

Both packages may contain useful specialist mathematics. Neither is an *Annals*, *Inventiones*, *JAMS*, or *Acta* result in its present form.

## 2.2 Why the current source cannot be reviewed as though the finalizer had run

The head commit adds an “idempotent final source audit and clarification pass.” Its workflow contains source substitutions that would:

- declare \(0<c_-<c_+<\infty\) and \(2a_+<b_-<b_+<\infty\) in the Jacobi parameter space;
- distinguish the transient envelope from the mean increment in the abstract likelihood proof;
- introduce one fixed exploitation-force bound \(U\);
- introduce fixed exploitation-duration bounds \(0<\tau_{\min}\le\tau_{\max}<\infty\);
- impose the finite-prefix calibration count \(N_{\rm cal}(m)\ge\rho m-C_{\rm cal}\);
- require the calibration duration to be measurable before the fresh sign; and
- replace the false assertion “every duration is bounded below by \(\tau\)” by a bound involving \(\min(\tau,\tau_{\min})\).

Those are not formatting changes. They repair mathematical hypotheses used in the proofs.

The workflow did not execute successfully and did not produce a descendant commit. The canonical branch still points to `1f1409c...`, and the source files still contain the pre-patch text. Refereeing a Git repository means refereeing committed bytes, not the contents of a failed script that might have rewritten them.

---

# 3. Summary of the claimed contribution

The paper has two models.

## 3.1 Homogeneous five-parameter bath

The first model is a uniformly damped, pinned half-line oscillator lattice on

\[
\ell^2(\mathbb N_0)\oplus\ell^2(\mathbb N_0).
\]

The unknown parameter is

\[
\vartheta=(c,k,\epsilon,c_b,k_b),
\]

where \(c,k\) are the boundary damping and pinning, \(\epsilon\) is the homogeneous coupling, and \(c_b,k_b\) are bath damping and pinning. Force and observation are collocated at site zero.

The step-response jets are used to reconstruct the five coefficients. Six short durations interpolate the jets through order eight, and a smooth triangular inverse reconstructs the parameter. Calibration windows use every duration in

\[
\{\tau,2\tau,\ldots,6\tau\}
\]

once, with a fresh random sign. The sign pairing is intended to eliminate cancellation by the state present at the beginning of a block. A general Gaussian likelihood theorem is then invoked to give a five-dimensional random-information quasi-BvM theorem and evidence formula.

The filter is compared with a Dirac mass at the forced trajectory in strong dual norms. The inferred finite parameter is mapped to the entire exponentially weighted memory kernel by a Banach-space delta method.

## 3.2 Fully unknown Jacobi stiffness sequence

The second model keeps one common damping coefficient but makes every Jacobi off-diagonal and diagonal coefficient unknown:

\[
\beta=(c,(a_j)_{j\ge0},(b_j)_{j\ge0}).
\]

The exact boundary response determines the Weyl function. Successive Schur complements recover every \(b_j\), every positive \(a_j\), and the next tail Weyl function.

For statistics, the experiment chooses a diagnostic duration from a fixed countable dense set, chooses an independent sign, and precedes the diagnostic with a washout time \(w_i=w_*i\). The resulting posterior is claimed to be strongly consistent in the compact product topology for every full-support prior.

This second theorem is genuinely infinite-dimensional in the literal sense that infinitely many coefficients are learned coordinatewise. That fact is acknowledged in this report. It does not settle correctness, novelty, quantitative strength, or top-journal significance.

---

# 4. Decisive correctness failure: “lower density” does not imply the finite-horizon contrast used in the theorem

## R40-M1. A direct admissible-policy counterexample

The balanced-design paragraph requires a predictable sequence of calibration slots “with lower density \(\rho\).” The five-parameter theorem then permits sample-size-dependent policies and claims constants uniform over all such policies.

Fix any terminal sample size \(n\). Define an infinite policy as follows.

- Slots \(1,\ldots,n\) are exploitation slots.
- Every slot after \(n\) is a calibration slot.
- After slot \(n\), partition the calibration slots into six-slot windows and use the required six durations with fresh signs.
- In the first \(n\) slots choose force zero and any bounded duration allowed by the current prose.

This policy is predictable. Its calibration set has asymptotic lower density one, hence at least \(\rho\) for every \(\rho\le1\). It therefore satisfies the stated lower-density requirement.

Now choose the true initial state \(z_0=0\). On the observed horizon the realized force is identically zero, so the zero-initial-state trajectory is identically zero under every parameter:

\[
 x_i^\vartheta=0,
 \qquad
 m_i^\vartheta=0,
 \qquad
 1\le i\le n.
\]

Consequently

\[
\sum_{i=1}^n
(m_i^\vartheta-m_i^{\vartheta_0})^2=0
\]

for every candidate \(\vartheta\). The ratio in `eq:full-empirical-contrast` is zero, not bounded below by a positive \(c_*\). The failure probability is one, not at most \(C_1e^{-C_2n}\).

Likewise,

\[
Dm_i^{\vartheta_0}=0,
\qquad I_n=0,
\qquad\Delta_n=0.
\]

The posterior receives no parameter information from the first \(n\) observations. It cannot be uniformly root-\(n\) concentrated and cannot be approximated by a nonsingular Gaussian with the asserted covariance.

Because the theorem explicitly allows the policy to depend on \(n\), one may choose this delayed-calibration policy for every terminal size. There is no single policy-dependent burn-in that can save a uniform triangular statement.

This counterexample invalidates, for the frozen policy class:

- Proposition `prop:balanced-contrast`;
- the information lower bound used by Theorem `thm:lattice-bvm`;
- the five-parameter quasi-BvM theorem;
- the five-parameter evidence expansion;
- the finite-rank state-posterior corollary insofar as it uses that BvM theorem;
- the memory-kernel posterior corollary; and
- the finite-preparation Gaussian mixture theorem.

## R40-M2. The needed repair is a prefix-count assumption, not a prose gloss

The correct uniform condition is of the form

\[
N_{\rm cal}(m)\ge\rho m-C_{\rm cal}
\quad\text{for every }m,
\]

with constants common to the entire policy class. This is exactly the condition present in the failed finalizer's proposed replacement text.

After such a change, the proof must recompute the number of complete six-slot windows and the constants lost to incomplete windows. The theorem should not continue to refer merely to “lower density,” because lower asymptotic density and a uniform finite-prefix discrepancy bound are different hypotheses.

---

# 5. The policy class does not supply the uniform force and time bounds used by the proofs

## R40-M3. “Arbitrary bounded” is not one uniform model class

The frozen source says that exploitation blocks may use “arbitrary bounded force-duration actions.” It does not introduce one deterministic force bound shared by all policies. A supremum over policies cannot use response and state constants independent of the policy if each policy is free to choose its own bound.

The energy estimate controls the forced trajectory by a constant proportional to the common input bound. Without a common \(U<\infty\), the claimed deterministic derivative bound

\[
\sup_{i,\vartheta}\left|\partial^\alpha m_i^\vartheta\right|\le B
\]

is not uniform over the stated class. The compact-net size, martingale increment bound, Sobolev score constants, global envelope, and evidence comparison all inherit that missing constant.

## R40-M4. The manuscript asserts a lower duration bound that it never imposed

Immediately before the five-parameter BvM theorem, the paper states:

> Every duration is bounded below by \(\tau\).

That statement does not follow from the policy definition. Calibration durations lie in the six-element set generated by \(\tau\); exploitation durations are only described as bounded.

Thus the displayed estimate

\[
\left|\partial_\vartheta^\alpha b_i^\vartheta(z)\right|
\le C_re^{-\lambda_ri\tau}
\]

is unsupported. One may choose exploitation durations tending to zero, so block index \(i\) need not be comparable to physical time \(t_i\). The same unsupported comparison appears in the filter theorem through

\[
\|T_\vartheta(t_n)\|
\le Ce^{-\lambda n\tau}.
\]

A correct statement needs either:

1. one common lower duration \(\tau_{\min}>0\) on every exploitation block; or
2. a proof that the finite-prefix calibration count alone forces a sufficiently large cumulative time, with the decay rate written in terms of that count.

Again, the failed finalizer proposed the first repair. The repair is not present in the reviewed source.

## R40-M5. The chronological measurability of the duration should be explicit

The sign-cancellation proof conditions on the past and the selected duration. For the predictable conditional lower bound used in the martingale argument, the duration at a calibration slot must be fixed before the fresh sign is drawn. The current prose says that the six durations form a possibly data-dependent permutation but does not state the sigma-field with respect to which the current duration is measurable.

The finalizer proposed to require \(s_i\) to be \(\mathcal F_{i-1}\)-measurable. That is the correct hypothesis. It must be in the theorem, not only in a failed workflow.

---

# 6. The infinite Jacobi parameter space is not completely defined in the frozen source

## R40-M6. The upper diagonal endpoint is undeclared

The infinite-Jacobi section begins by fixing

\[
0<a_-<a_+<\infty,\qquad c_->0,
\qquad b_->2a_+,
\]

and then defines

\[
\mathfrak B=[c_-,c_+]
\times\prod_{j\ge0}[a_-,a_+]
\times\prod_{j\ge0}[b_-,b_+].
\]

The paragraph does not introduce \(b_+\). The symbol \(c_+\) has appeared in the preceding homogeneous model, but its reuse is not declared as part of the new model. In particular, the statement “with its compact metrizable product topology” and the uniform operator upper bound require a finite diagonal upper endpoint that has actually been fixed.

The failed finalizer proposed the self-contained assumption

\[
0<c_-<c_+<\infty,
\qquad
2a_+<b_-<b_+<\infty.
\]

That is a small repair, but it is a repair to the mathematical definition on which compactness, boundedness of \(J_\beta\), and uniform stability depend.

---

# 7. The uniform strong law in the infinite-sequence posterior proof has a genuine logical gap

## R40-M7. A fixed-error Doob bound is used as if it controlled an uncountable supremum

The consistency proof introduces the compact response-difference family

\[
\mathcal D
=\{m\mapsto\delta_\beta(m):\beta\in\mathfrak B\}
\subset L^2(\omega).
\]

It selects a finite \(L^2(\omega)\) net. For one approximation error

\[
e=d-d^k,
\]

the appendix obtains a Doob bound of the form

\[
\Pr\left\{
\max_{m\le2^r}|M_m(e)|>2^r\delta
\right\}
\le \frac{C\varepsilon^2}{2^r\delta^2}.
\]

This inequality is valid for one fixed \(e\). The next sentence concludes that the finite net and Borel--Cantelli control

\[
\sup_{d\in\mathcal D}|M_n(d)|/n.
\]

That conclusion does not follow. For every net center there are generally uncountably many errors \(e\) in its \(L^2\) ball. A probability bound for each fixed error cannot be union-bounded over that ball. The proof supplies no measurable envelope for the ball, no brackets, no entropy integral, no chaining argument, and no finite-dimensional parameterization with controlled metric entropy.

The same defect affects the uniform law for the square class.

Total boundedness of a function class in \(L^2(P)\) is not, by itself, the missing stochastic equicontinuity argument. The proof has established pointwise laws plus finite-net convergence; it has not established uniform approximation between a function and its net representative.

## R40-M8. A model-specific repair appears available, but it is not the written proof

Lemma `lem:product-continuity` proves more than the consistency proof uses: the response image is compact in

\[
C([0,T])
\]

with the supremum norm. A finite sup-norm net would give, for every error in a net ball,

\[
\frac1n|M_n(e)|
\le \|e\|_\infty\,rac1n\sum_{i=1}^n|\xi_i|,
\]

uniformly over the entire ball. The ordinary strong law for \(|\xi_i|\) would then provide the required approximation. The bounded square class could be treated similarly.

That repair is short and plausible. It must actually be made. Until it is, equations `eq:uniform-score-slln` and `eq:uniform-square-slln` are not proved, so the exponential numerator bound and Theorem `thm:jacobi-consistency` remain incomplete.

---

# 8. The strong filter-jet theorem remains under-justified

## R40-M9. It inherits the invalid block-time comparison

The filter-jet theorem uses

\[
\sup_{\vartheta,|\alpha|\le r+1}
\|\partial_\vartheta^\alpha T_\vartheta(t_n)\|
\le C_re^{-\lambda_r n\tau}.
\]

As explained above, the policy class does not imply \(t_n\ge n\tau\). Thus the theorem's displayed exponential-in-\(n\) estimate is not established for the frozen class.

## R40-M10. Strong dual-valued measurability needs a deterministic argument

The concentrated-push-forward lemma is a useful attempt to repair the weak-on-tests problem identified in earlier rounds. The choice of one additional bounded test derivative is sensible, and a strong derivative in

\[
(C_b^{j+1}(\mathscr H))'
\]

is plausible.

The measurability paragraph, however, is too compressed. It says that the continuous range generates a separable closed subspace and that the dual norm is a supremum over a countable dense subset of “test restrictions.” For a random normalized measure and a nonseparable ambient dual, the manuscript should identify one deterministic separable range or one explicit countable norming class and prove that it norms the particular derivative functionals under consideration. A pathwise separable range that may depend on the sample point is not automatically a Bochner-measurability proof.

The paper also needs an explicit bound showing the dependence of the push-forward constant on the total-variation derivative norms of the random weights. It later takes moments of that constant; the polynomial dependence should be stated rather than inferred from prose.

These issues may be repairable. The present paragraph is not a publication-level proof of all the strong measurability and supremum assertions advertised in the theorem.

---

# 9. Assessment of the abstract random-information quasi-BvM theorem

## 9.1 Genuine improvement over the preceding version

The abstract section is one of the strongest parts of Round Thirty Nine. It now contains:

- a two-stage filtration;
- parameter-independent chronological policy cancellation;
- explicit uniform stochastic-order notation;
- an exact integrated nuisance factorization;
- derivative budgets uniform over arbitrary Hilbert-ball working priors;
- a pseudo-true parameter estimate under transient misspecification;
- Sobolev control of smooth martingale fields;
- a global likelihood envelope;
- root-\(n\) posterior localization; and
- a relative unnormalized \(L^1\) Laplace lemma that normalizes a moving random Gaussian.

Subject to ordinary extension and measurability details, the abstract theorem is plausible under its assumptions.

## 9.2 It does not rescue the invalid model verification

The abstract theorem assumes the global contrast event. In the five-parameter application, proving that assumption is the main model-specific obligation. Proposition `prop:balanced-contrast` fails for the stated triangular policy class by the delayed-calibration counterexample. A valid implication theorem cannot compensate for a false verification of its hypothesis.

## 9.3 The abstract theorem is not top-four mathematics as presently situated

After the summable nuisance is factored out, the theorem concerns a fixed-dimensional smooth Gaussian mean model with known variance, compact parameter space, a uniformly coercive empirical contrast, bounded derivatives, and a predictable random design. The proof is a clean localization and Laplace argument. It does not establish a new semiparametric efficiency theory, a nonparametric BvM theorem, or adaptive-policy coverage without information stability.

The manuscript cites Du--Nair--Janson for adaptive-data BvM phenomena. It must compare theorem against theorem:

- nonlinear versus linear mean;
- global contrast versus local information assumptions;
- policy-uniform triangular arrays;
- quasi-Bayesian transient misspecification;
- posterior TV approximation versus frequentist coverage; and
- assumptions needed when the realized information does not converge.

At most, the abstract result appears to be a useful specialist extension and repackaging. The paper has not demonstrated the conceptual novelty or breadth expected by a top-four general journal.

---

# 10. Assessment of the five-parameter mechanical result

## 10.1 What appears mathematically sound

The following parts are credible on direct inspection:

1. The Lyapunov functional yields uniform exponential stability for a bounded, uniformly damped and uniformly pinned generator.
2. The response coefficients through `r_7` are consistent with repeated application of the banded generator.
3. With \(\epsilon\ge\epsilon_->0\), the triangular formulas recover \(c\), \(k+\epsilon\), the positive \(\epsilon\), \(k\), \(c_b\), and \(k_b\).
4. Six short durations form an invertible generalized Vandermonde interpolation system for the relevant jets.
5. A sufficiently small fixed \(\tau\) gives a model-specific global embedding on a compact parameter box.
6. Given a valid finite-prefix calibration condition and a fresh sign at every calibration slot, the sign-square identity can provide a persistent contrast.

This is a substantial improvement over the Round-Thirty-Five model, where the bath coefficients were known.

## 10.2 The result remains finite-dimensional and severely conditioned

The unknown is five-dimensional. The topology and all remote bath structure are known and homogeneous. Force and observation remain collocated at the boundary. The generator remains bounded and uniformly exponentially stable. Coupling is bounded away from zero so that division by \(\epsilon^2\) is uniformly safe.

The bath parameters first enter high-order short-time jets. The paper proves existence of a small-duration embedding but gives no useful conditioning analysis as \(\tau\downarrow0\), no statistical efficiency comparison among durations, no robustness to model error, and no treatment of weak coupling \(\epsilon\to0\). The global lower constant can be extremely small because reconstructing an eighth-order jet from noisy finite-time observations is ill-conditioned.

These omissions do not necessarily invalidate the theorem. They sharply limit its significance.

## 10.3 “Balanced calibration” remains imposed excitation

Replacing positive probability for every diagnostic atom at every block by positive-density six-slot calibration windows is a meaningful relaxation. It is still prescribed persistent excitation. The policy is adaptive only in the ordering of calibration durations and in exploitation between mandatory windows.

The paper does not derive excitation from an optimizing policy, prove a reward-information tradeoff, allow vanishing calibration density, or characterize when closed-loop exploitation itself identifies the system. The hard adaptive-design problem remains outside the theorem.

---

# 11. Assessment of memory inference

The memory map

\[
\mathscr M:\vartheta\mapsto\mathcal K_\vartheta
\]

is a smooth map from five real parameters into an exponentially weighted Banach space. Once the five-dimensional BvM theorem is valid, the functional posterior statement is the ordinary delta method:

\[
\sqrt n(\mathcal K_\vartheta-\mathcal K_{\vartheta_0})
\approx D\mathscr M_{\vartheta_0}
\sqrt n(\vartheta-\vartheta_0).
\]

This is correctly much stronger than merely computing a known memory kernel, as Round Thirty Five did. It still does not infer an unrestricted memory function. The posterior lives asymptotically on the image of a five-dimensional Gaussian under a finite-rank derivative.

The manuscript should therefore describe the result as finite-dimensional parametric uncertainty propagated to a kernel-valued quantity. It is not a nonparametric functional BvM theorem.

Moreover, the corollary currently depends on the invalid policy-uniform lattice BvM theorem. It cannot stand until the calibration and duration assumptions are repaired.

---

# 12. Assessment of the complete Jacobi reconstruction

## 12.1 Deterministic uniqueness is classical and plausible

The identities

\[
\widehat h_\beta(z)
=\frac1z m_0(z^2+cz),
\]

and

\[
m_j(w)=\frac1{w+b_j-a_j^2m_{j+1}(w)}
\]

lead to the standard successive recovery of \(b_j\), \(a_j^2\), and the next tail Weyl function. Positivity fixes the sign of \(a_j\). Cyclicity of \(e_0\) rules out a finite-support spectral measure and hence a rational Weyl function.

This is a clean direct presentation of classical Weyl--Titchmarsh/inverse-Jacobi machinery. The manuscript itself acknowledges that the recursion and inverse spectral uniqueness are classical. The standard literature includes Gesztesy--Simon, Teschl, and dynamic inverse work of Mikhaylov and collaborators.

## 12.2 The statistical design asymptotically resets the system

Before the \(i\)-th diagnostic observation, the experiment inserts a washout

\[
w_i=w_*i.
\]

The total washout time through observation \(n\) is therefore of order \(n^2\). The arbitrary feedback segment is deliberately erased before each diagnostic. The diagnostic duration and sign are then drawn independently from a fixed design.

This is a legitimate consistency experiment. It is not a difficult adaptive-identification theorem for the infinite sequence. The infinite-dimensional statistical part is essentially an i.i.d. Gaussian regression on a compact identifiable response family, perturbed by a summable residual.

## 12.3 Product-topology consistency is qualitative and weak

An open product neighbourhood constrains only finitely many coefficients. The theorem therefore says that every fixed finite coefficient block is eventually learned. It does not provide:

- a contraction rate for coefficient \(j\) as a function of \(j\) and \(n\);
- consistency in a weighted \(\ell^p\), operator, spectral-measure, or transfer-function norm;
- quantitative stability of the inverse Weyl recursion;
- posterior uncertainty or credible sets for the infinite sequence;
- minimax or lower-bound analysis;
- a finite-time truncation rule;
- sample complexity for learning the first \(J\) coefficients;
- robustness to observation-time error or model misspecification; or
- an adaptive design for choosing durations to optimize recovery.

Analytic continuation from a finite time interval and successive high-energy Weyl limits are severely ill-conditioned operations. A top-journal statistical inverse theorem would need to confront that instability quantitatively. Pure injectivity plus qualitative product consistency avoids the hard question.

## 12.4 Prior-art comparison remains incomplete

The revised bibliography is much better than the four-entry Round-Thirty-Five list. It still does not compare the posterior consistency theorem with general Bayesian inverse-problem consistency results, where deterministic stability or injectivity is combined with regression consistency, nor with modern posterior contraction results for learning infinite-dimensional operators from noisy data.

At a minimum, the paper should explain why its compact-separation argument is more than a model-specific instance of established consistency templates, and why no quantitative contraction theorem is attempted despite the inverse problem's severe instability.

---

# 13. Verification and repository status

## 13.1 The local verification record is accurately limited

`ROUND39_LOCAL_VERIFICATION.json` records:

```text
28-page two-pass LaTeX build
6 tests
finite jet algebra
triangular rational inverse
Vandermonde nonsingularity
finite Jacobi Schur identity
theorem-label presence
source-manifest hashes
formal proof assistant: false
remote CI verified: false
```

The record expressly excludes:

- martingale empirical-process proofs;
- the relative random-information Laplace theorem;
- strong Banach-dual differentiability;
- infinite Jacobi inverse uniqueness;
- posterior consistency; and
- novelty or journal significance.

This is an honest scope statement. The six tests cannot be cited as verification of the analytic theorems.

## 13.2 All three remote workflows failed before recorded source execution

At the frozen head, the repository records three Round-Thirty-Nine workflow runs:

1. `Synchronize Round 39 source manifest` — failure;
2. `Verify Round 39 revision` — failure;
3. `finalize-round39-sources.yml` — failure.

The first two jobs have empty step lists and no assigned runner. The finalizer produced no job. I therefore do **not** interpret the status as evidence that the algebra tests or TeX build ran and failed. The accurate conclusion is:

> There is no successful remote verification record for the frozen Round-Thirty-Nine head, and the source-finalization substitutions were not applied.

That distinction matters. The failed finalizer contains the very assumptions needed to remove several objections in this report.

## 13.3 A proof ledger is not independent evidence

`round39/PROOF_LEDGER.json` marks every focused Round-Thirty-Eight obligation “closed.” That is an author-side bookkeeping assertion. It cannot override a counterexample to the policy class, an undeclared parameter bound, or a missing empirical-process step.

---

# 14. Theorem-by-theorem disposition

| Result | Correctness assessment at the frozen head | Top-four originality/significance assessment |
|---|---|---|
| Uniform stability of the homogeneous lattice | Credible for the bounded uniformly damped/pinned box. | Standard Lyapunov-semigroup estimate. |
| Five response-jet formulas | Independently consistent on inspection. | Useful finite local algebra. |
| Triangular five-parameter inverse | Correct-looking under \(\epsilon_->0\). | Explicit but elementary finite-dimensional inversion. |
| Six-duration interpolation | Plausible; constants may be badly conditioned. | Model-specific Vandermonde reconstruction. |
| Global six-duration embedding | Plausible after the interpolation bounds. | Not a broad inverse theorem. |
| Balanced empirical contrast | **False for the stated sample-size-dependent lower-density policy class.** | Prescribed calibration even after repair. |
| Abstract random-information quasi-BvM | Plausible under its explicit contrast and smoothness assumptions. | Clean specialist finite-dimensional Laplace theorem; novelty not established at top-four level. |
| Five-parameter lattice BvM | **Not proved because its contrast hypothesis fails for an admissible policy.** | Regular parametric inference after forced excitation. |
| Evidence formula | Correct Gaussian normalization conditional on a valid BvM/localization theorem. | Standard Laplace consequence. |
| Strong filter jets | Inherits the false block-time lower bound; strong measurability proof remains compressed. | Stable-transient consequence, not a major filtering theorem. |
| Finite-rank state Gaussian image | Dependency on invalid BvM; otherwise plausible. | Explicitly rank at most five, hence not an infinite-dimensional BvM. |
| Functional memory posterior | Dependency on invalid BvM; otherwise a smooth delta-method corollary. | Five-dimensional parametric uncertainty in a function-valued output. |
| Complete Jacobi reconstruction | Classical and broadly correct-looking, after fixing the parameter-space definition. | Standard Weyl/Schur inverse uniqueness. |
| Nonrationality of the infinite Weyl function | Credible from cyclicity. | Classical spectral observation. |
| Uniform washout correction | Plausible with common force/duration bounds. | Engineered summable-reset estimate. |
| Infinite Jacobi posterior consistency | **Incomplete: the uniform strong-law approximation step is unjustified.** | Qualitative compact product consistency, no rates or UQ. |
| Finite preparation mixture | Dependency on invalid five-parameter BvM; otherwise routine finite-mixture normalization. | Not a phase theorem. |
| Local verification packet | Supports six finite algebra/source checks. | Reproducibility aid only. |

---

# 15. Minimum repairs before a specialist submission

The following is not a top-four major-revision invitation. It is a minimum correctness and presentation checklist for a new specialist submission.

1. **Commit the assumptions rather than scripting them.** Apply the finalizer's mathematical substitutions to the source in an ordinary author commit, regenerate the manifest, and freeze a new immutable head.

2. **Replace asymptotic lower density by a uniform prefix count.** State
   \[
   N_{\rm cal}(m)\ge\rho m-C_{\rm cal}
   \]
   for every prefix and use this exact inequality in the proof.

3. **Fix one common exploitation class.** Declare a common force bound, a positive common lower duration, and any upper duration needed for the claimed uniformity.

4. **Make the calibration chronology formal.** State that duration selection is measurable before the fresh sign and that noise is sampled after both.

5. **Reprove the empirical contrast.** Count complete calibration windows at every finite horizon and track the constants lost to incomplete windows.

6. **Correct every block-time estimate.** Replace unsupported \(t_n\ge n\tau\) assertions by the bound actually implied by the policy class.

7. **Define the Jacobi parameter space self-containedly.** Introduce finite \(c_+\) and \(b_+\) explicitly and state all common operator bounds.

8. **Repair the uniform strong law.** Use the already proved compactness in \(C([0,T])\) and a sup-norm net, or give a valid bracketing/entropy/chaining proof. Do not use a fixed-function Doob estimate as an uncountable supremum bound.

9. **Complete the strong filter-measurability argument.** Supply an explicit deterministic separable range or countable norming class and state the polynomial dependence of constants on weight-derivative norms.

10. **State one principal contribution.** The current abstract combines a general BvM lemma, five-parameter mechanics, filter jets, memory uncertainty, inverse spectral reconstruction, infinite posterior consistency, and finite mixtures. A specialist paper should separate the finite-dimensional Bayesian-mechanics theorem from the infinite Jacobi consistency theorem unless a genuine common theorem links them.

11. **Expand the prior-art comparison.** Compare the finite mechanical identification theorem with classical and modern infinite-dimensional adaptive identification; compare the BvM theorem with adaptive-data results; compare the Jacobi consistency theorem with general Bayesian inverse-problem consistency and operator-learning contraction theory.

12. **Add quantitative inverse analysis or reduce the claims.** For the Jacobi sequence, provide stability and contraction rates in a meaningful topology, or present the current result honestly as qualitative product-topology consistency.

13. **Obtain a successful clean remote run.** A pre-execution runner failure is not a mathematical disproof, but a source packet advertised as reproducible should have one successful immutable-head verification record.

14. **Remove repository governance from the article.** Branch names, referee hashes, closure ledgers, and workflow semantics belong in a submission README or response letter, not in the mathematical paper.

---

# 16. What kind of result could change the top-four assessment

A qualitatively stronger project would need to confront one of the hard phenomena that the current experiments avoid. Examples include:

- posterior contraction rates for the complete Jacobi sequence in a weighted coefficient or operator topology;
- quantitative stability estimates linking noisy finite-time boundary response to deep Jacobi coefficients;
- minimax lower bounds showing the optimal dependence on coefficient depth and observation budget;
- a nonparametric BvM or valid uncertainty-quantification theorem for an infinite-dimensional spectral object;
- recovery of an unknown damping sequence as well as the stiffness Jacobi operator;
- an unbounded wave or beam generator with an unbounded boundary observation operator;
- calibration generated by a reward-seeking adaptive policy rather than imposed by a prefix-density constraint;
- vanishing exploration with a sharp information threshold;
- finite total-time or near-linear-time experimental designs rather than linearly increasing washout at every stage; or
- a theorem whose key inferential phenomenon provably disappears on every fixed finite-chain approximation.

Any of these would be a new research project. That is why the present manuscript is not a top-four major-revision case.

---

# 17. Selected literature that must frame any resubmission

The following list is not exhaustive. It illustrates the bodies of work against which the revised claims must be positioned.

- J. Baumeister, W. Scondo, M. A. Demetriou, and I. G. Rosen, *On-line parameter estimation for infinite-dimensional dynamical systems*, SIAM J. Control Optim. **35** (1997), 678--713.
- M. A. Demetriou and I. G. Rosen, *Adaptive identification of second order distributed parameter systems*, Inverse Problems **10** (1994), 261--294.
- M. A. Demetriou and I. G. Rosen, *On the persistence of excitation in the adaptive identification of distributed parameter systems*, IEEE Trans. Automat. Control **39** (1994), 1117--1123.
- S. Chattopadhyay, S. Sukumar, and V. Natarajan, *Adaptive identification of linear infinite-dimensional systems*, Internat. J. Control **98** (2025), 593--608.
- K. Du, Y. Nair, and L. Janson, *Bernstein--von Mises for adaptively collected data*, arXiv:2511.06639.
- F. Gesztesy and B. Simon, *m-functions and inverse spectral analysis for finite and semi-infinite Jacobi matrices*, J. Anal. Math. **73** (1997), 267--297.
- G. Teschl, *Jacobi Operators and Completely Integrable Nonlinear Lattices*, AMS, 2000.
- A. Mikhaylov, V. Mikhaylov, and related collaborators, work on dynamic inverse problems and response data for semi-infinite Jacobi matrices.
- S. Vollmer, *Posterior consistency for Bayesian inverse problems through stability and regression results*, Inverse Problems **29** (2013), 125011.
- M. V. de Hoop, N. B. Kovachki, N. H. Nelsen, and A. M. Stuart, *Convergence rates for learning linear operators from noisy data*, SIAM/ASA J. Uncertain. Quantif. **11** (2023), 480--513.

The manuscript need not claim that any one of these papers subsumes Round Thirty Nine. It must identify the nearest theorem and explain precisely what is new, stronger, weaker, or merely different.

---

# 18. Final recommendation

Round Thirty Nine deserves credit for a real change of mathematical content. It answers several presentation and proof-organization criticisms from Round Thirty Eight, extends the homogeneous mechanical model from two to five unknown coefficients, propagates parameter uncertainty to a memory kernel, and introduces a genuinely infinite coefficient sequence with a classical constructive inverse map.

The frozen submission is nevertheless not correct. Its policy-uniform contrast theorem is contradicted by a delayed-calibration policy that is admissible under the stated lower-density condition and the expressly allowed sample-size dependence. Its time-decay estimates use an exploitation-duration lower bound that was never imposed. Its infinite Jacobi parameter space omits an upper endpoint. Its posterior-consistency proof lacks the stochastic equicontinuity step required to pass from a finite \(L^2\) net to a uniform strong law.

The repository itself contains proposed source patches for several of these problems, but the finalizer failed and no patched descendant commit exists. Referee credit cannot be given for unexecuted future text.

Even after repair, the paper would remain below the standard of *Annals of Mathematics*, *Inventiones Mathematicae*, *JAMS*, or *Acta Mathematica*. The finite-dimensional part is regular parametric inference under prescribed calibration. The infinite-dimensional part proves only qualitative product-topology consistency under an increasingly washed-out diagnostic experiment, using classical inverse spectral uniqueness and without rates, quantitative stability, or infinite-dimensional uncertainty quantification.

**Recommendation: reject; do not invite a top-four major revision.**

A corrected, split, and substantially reframed specialist submission may be worthwhile.