# External Adversarial Referee Report on the Round-Thirty-Five Revision

## Recommendation: **Reject for Annals/Inventiones/JAMS/Acta-level publication; do not invite a top-four major revision**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round35-mechanical-identification-2026-09-03`  
**Immutable reviewed head:** `bca291f85e47916cc5f089c0c01350f0c0c6f3b0`  
**Reviewed source tree:** `bc45f1c9366f1d96723f4e3f87f4b65e775fd18b`  
**Mathematical source commit:** `38c71d53cba3ca99d7a7d0a49209a49e2ffdd3e0`  
**New review branch:** `review/round38-gpt56-pro-adversarial-audit-2026-09-04`  
**Review date:** 4 September 2026  
**Reviewer:** GPT-5.6 Pro, at the repository user's request.

This is an AI-assisted external referee-style assessment. It is not a report commissioned by, and it is not an editorial decision of, *Annals of Mathematics*, *Inventiones Mathematicae*, the *Journal of the American Mathematical Society*, or *Acta Mathematica*. I apply the correctness, originality, depth, breadth, self-containment, and lasting-significance threshold appropriate to those journals.

I also inspected the existing Round-Thirty-Six report. This report is a fresh adversarial audit, not a claim of a blinded second opinion. There is no Round-Thirty-Seven mathematical revision in the repository. The latest revision branch remains frozen at the same Round-Thirty-Five head already considered in Round Thirty Six. Accordingly, the central Round-Thirty-Six objections have not been answered by a subsequent author revision; they remain live.

---

# Executive verdict

Round Thirty Five is much better disciplined than the earlier eleven-paper closure dossier. It presents one identifiable mathematical object: a bounded, uniformly damped oscillator lattice on a half-line, with two unknown local coefficients, collocated forcing and observation, Gaussian readout noise, and forced randomized diagnostic actions. The paper also explicitly leaves the original Sinai-billiard and hard-sphere programme open. That narrowing is correct and should be preserved.

I recomputed the main local algebra. I do not find a one-line counterexample that destroys the whole manuscript. In particular, the following ingredients are broadly consistent on inspection:

- the Lyapunov energy calculation for a bounded, uniformly damped and pinned generator;
- the first parameter-dependent coefficients of the step response;
- the two-duration algebra recovering the local damping and stiffness coordinates;
- the positive/negative forcing identity that removes the current-state cross term after conditional averaging;
- the two-dimensional Gaussian normalization in the evidence formula; and
- the scalar Schur-complement formula for the constant-coefficient Jacobi bath.

That is not enough for publication in any of the four journals named above. The paper fails the top-journal test for structural reasons.

First, the principal inferential theorem is, after removal of an exponentially decaying transient, a regular **two-parameter adaptive Gaussian regression** with known variance, uniformly bounded derivatives, compact parameter space, and compulsory persistent exploration. The infinite-dimensional state is not an unknown infinite-dimensional parameter. It is a known stable bath plus an initial condition whose contribution is summable and asymptotically negligible at root-sample-size scale.

Second, the infinite-dimensional identification literature is not seriously reviewed. The manuscript has four references and omits directly relevant work on adaptive parameter estimation, persistence of excitation, stiffness/damping recovery, stable SISO infinite-dimensional systems, and online estimation in partially observed distributed systems. This omission is not cosmetic. It prevents the authors from identifying what, if anything, is new.

Third, several of the strongest statements are presented at proof-sketch rather than journal-proof level. The full uniform triangular experiment is not defined. The empirical net argument does not include all variables over which uniformity is claimed. The random-information Laplace argument is compressed into a paragraph of uniform `O_P` notation. The strong dual differentiability of filter jets is asserted rather than proved in the stated norm. These gaps may be repairable, but they are real proof obligations.

Fourth, the memory calculation is mathematically separate from the adaptive posterior theorem and is standard in form. The paper does not infer an unknown memory kernel. It computes the kernel of a completely known bath. Likewise, the preparation-label amplitudes are finite-mixture Bayes factors produced by a bounded transient likelihood correction; they are not a new phase-selection theory.

Fifth, the only remote Round-Thirty-Five workflow at the frozen head has conclusion `failure`, with an empty recorded step list. This appears to be failure before source execution rather than a failed mathematical test. The correct conclusion is therefore limited but clear: there is no successful remote verification record for the frozen head. The committed local test record and rational certificate are useful reproducibility artifacts, not proof verification.

My recommendation is:

> **Reject. Do not invite a major revision at Annals/Inventiones/JAMS/Acta level.**

A substantially rewritten specialist paper could be considered in systems and control, inverse problems, or mathematical statistics after the authors complete a serious prior-art analysis and expand the proofs. Such a submission should be treated as a new paper. It should not be marketed as another closure round of the original eleven-part programme.

---

# 1. Scope of this audit

I reviewed the following frozen materials:

- `ROUND35_REVISION.tex`;
- `round35/mechanical.tex`;
- `round35/errata.tex`;
- `round35/references.tex`;
- `AUTHOR_RESPONSE_ROUND34.md`;
- `ROUND35_REVIEW_INDEX.md`;
- `round35/PROOF_LEDGER.json`;
- the committed local verification metadata;
- the exact embedding-certificate description and its declared scope;
- the active B1, B3, and C2 corrections;
- the branch and commit history relevant to Round Thirty Five;
- the existing Round-Thirty-Six report; and
- the remote workflow status attached to the reviewed head.

The frozen branch head differs from the mathematical source commit only by a byte-level correction to `round35/requirements.txt`. There is no later mathematical commit on the revision branch.

The focused manuscript is the only plausible research-publication unit. The active B1, B3, and C2 files are errata or supporting lemmas. The proof ledger itself correctly records `all_original_gaps_closed: false` and leaves every original A/B/C/D application obligation open. Those open obligations cannot be used as evidence for the significance of the focused lattice theorem.

---

# 2. Editorial decision

## 2.1 Decision

**Reject without a top-four major-revision invitation.**

A top-four major revision is appropriate when a manuscript already contains a result of the required conceptual importance and needs a finite list of repairs. That is not the situation here. Even granting the central calculations, the present theorem package is too special, too close to regular parametric inference under forced excitation, too weakly situated in prior work, and too loosely connected to its memory appendix.

The missing ingredient is not merely a lemma. It is the editorial premise that the result represents a major mathematical advance of broad interest.

## 2.2 Why another closure round is not an answer

The repository already contains a Round-Thirty-Six report on the same frozen mathematical source. No Round-Thirty-Seven revision follows it. Renumbering another report does not create progress on the manuscript.

A meaningful response would require one of two things:

1. a fully revised specialist paper that answers the proof and literature objections; or
2. a qualitatively stronger theorem that introduces genuine infinite-dimensional inference, a nontrivial adaptive-design problem, or an unbounded-generator difficulty.

Neither can be replaced by more proof-ledger statuses, branch names, checksum manifests, or self-issued closure declarations.

---

# 3. What the paper actually proves, if its compressed steps are completed

The state belongs to

\[
\ell^2(\mathbb N_0)\oplus\ell^2(\mathbb N_0),
\]

and evolves under a bounded linear generator. The unknown parameter is the two-vector

\[
\theta=(c,k),
\]

where both entries occur at site zero, the same site at which force is applied and displacement is observed. All bath coefficients, the coupling, the noise variance, and the forcing bounds are known.

At every block, each of the four actions

\[
(\tau,a),\quad (\tau,-a),\quad (2\tau,a),\quad (2\tau,-a)
\]

has conditional probability at least \(\rho/4\). Thus the design forces persistent diagnostic excitation forever.

The local step response is

\[
h_\theta(t)=\frac{t^2}{2}-\frac{ct^3}{6}
+\frac{(c^2-k-\varepsilon)t^4}{24}+O(t^5).
\]

Two explicit linear combinations of \(h(\tau)\) and \(h(2\tau)\) recover \(c\) and \(k\), up to a controlled remainder. Pairing positive and negative signs cancels the cross term caused by the state already present at the beginning of a block. Uniform damping makes the unknown initial-state effect exponentially summable. A regular Gaussian likelihood calculation then gives local quadratic expansion, root-\(n\) localization, and a random-information Gaussian posterior approximation.

This is coherent. It is also modest. The essential inferential geometry is finite-dimensional and local. The infinite bath is known, stable, and asymptotically erased from the parameter likelihood.

---

# 4. Fatal top-four objection: novelty and significance have not been established

## 4.1 The bibliography is not remotely adequate

The bibliography has four items. That is untenable for a paper whose central phrases are “adaptive identification,” “infinite mechanical lattice,” “persistent excitation,” “damping and stiffness,” “partially observed,” and “Bernstein--von Mises.”

At a minimum, the authors must compare their results theorem by theorem with the following directly relevant literature:

1. J. Baumeister, W. Scondo, M. A. Demetriou, and I. G. Rosen, **On-Line Parameter Estimation for Infinite-Dimensional Dynamical Systems**, *SIAM Journal on Control and Optimization* 35 (1997), 678--713, DOI `10.1137/S0363012994270928`. This work treats adaptive identification in abstract linear and nonlinear infinite-dimensional systems, develops infinite-dimensional persistence of excitation, and includes stiffness and damping estimation in a one-dimensional wave model.

2. M. A. Demetriou and I. G. Rosen, **Adaptive identification of second order distributed parameter systems**, *Inverse Problems* 10 (1994), 261--294.

3. M. A. Demetriou and I. G. Rosen, **On the persistence of excitation in the adaptive identification of distributed parameter systems**, *IEEE Transactions on Automatic Control* 39 (1994), 1117--1123.

4. S. Chattopadhyay, S. Sukumar, and V. Natarajan, **Adaptive identification of linear infinite-dimensional systems**, *International Journal of Control* 98 (2025), 593--608, DOI `10.1080/00207179.2024.2353731`. This paper studies stable SISO infinite-dimensional systems, persistent excitation, transfer-function coefficient recovery, parameter reconstruction, and PDE examples.

5. L. Sharrock and N. Kantas, **Joint Online Parameter Estimation and Optimal Sensor Placement for the Partially Observed Stochastic Advection-Diffusion Equation**, *SIAM/ASA Journal on Uncertainty Quantification* 10 (2022), 55--95, DOI `10.1137/20M1375073`.

6. The classical stochastic-regression and adaptive-control literature underlying modern adaptive-data inference, including the work of Lai and Wei already discussed in the adaptive BvM literature cited by the manuscript.

The point is not that these papers automatically subsume Round Thirty Five. The point is that they make the manuscript's current novelty discussion non-credible. The authors have not identified the nearest theorem, the exact hypothesis difference, the exact conclusion difference, or why that difference matters.

At a top-four journal, failure to establish priority is independently fatal.

## 4.2 The finite-chain invariance test

A simple editorial diagnostic exposes the weakness of the “infinite-dimensional” branding:

> Replace the known infinite bath by a sufficiently large known finite stable chain. Which principal statistical theorem fails?

For the present argument, essentially none fails. The energy bound, parameter derivatives, two-duration inversion, sign cancellation, empirical information, local likelihood, BvM approximation, and rank-two state image all survive. The exact half-line memory formula changes, but that formula is not used in the inferential theorem.

This shows that the infinite half-line is not the source of the statistical difficulty. It is a setting in which a finite-dimensional local inference problem is embedded.

## 4.3 The unknown is two-dimensional, local, and collocated

The manuscript does not infer:

- an unknown damping field;
- an unknown stiffness field;
- an unknown Jacobi sequence;
- an unknown bath spectral measure;
- an unknown input or observation operator;
- an unknown memory kernel; or
- an infinite-dimensional initial state at a non-negligible asymptotic scale.

It infers two scalars at the driven and observed site. This is not a criticism of correctness. It is decisive for significance.

## 4.4 Forced exploration removes the hard adaptive-design problem

The theorem assumes that every diagnostic atom is sampled with fixed positive conditional probability at every block. This is persistent excitation by fiat.

The paper does not prove that a reward-seeking, stabilizing, or posterior-driven policy generates enough information. It does not characterize a reward-information tradeoff. It does not handle vanishing exploration. It does not derive excitation from closed-loop dynamics.

The adaptive freedom lies only in the remaining probability mass. The core theorem is therefore closer to inference under a randomized calibration schedule than to a general adaptive-design result.

## 4.5 Exponential damping trivializes the nuisance asymptotically

The initial state is infinite-dimensional, but every contribution to the parameter log likelihood is exponentially summable. The marginal initial-state correction and each fixed parameter derivative are \(O_P(1)\). At root-\(n\) scale they vanish.

There is no semiparametric nuisance tangent space competing with the parameter score, no nuisance contraction theorem, no least-favourable direction, no efficiency calculation, and no prior thickness requirement near the true initial state. Indeed, the prior may miss the true state precisely because dynamics erase the discrepancy.

That observation is useful. It does not constitute a difficult infinite-dimensional Bernstein--von Mises theorem.

## 4.6 The memory theorem is separate and standard in form

The bath transform

\[
s(z)=\frac{p(z)-\sqrt{p(z)^2-4\varepsilon^2}}{2}
\]

is the expected scalar Schur-complement/continued-fraction formula for a constant-coefficient half-line Jacobi operator. The calculation appears consistent. It is not used to prove identifiability, likelihood localization, posterior normality, or filter contraction.

The paper computes a known-bath kernel; it does not infer a kernel from data. Placing the formula beside an adaptive posterior theorem does not fuse the two into a top-journal contribution.

---

# 5. Proof obligations not discharged at journal level

The following are not all counterexamples. They are places where a strong claim is supported only by a compressed outline. A top journal cannot accept the manuscript on the assurance that the omitted details are routine when the omitted details carry nearly all of the stated uniformity.

## R38-M1. The triangular experiment and filtration are not defined

The paper claims uniformity over:

- all admissible policies;
- policies depending on the terminal sample size;
- all true parameters in a compact interior set;
- all true initial states in a Hilbert ball; and
- all initial-state priors on that ball, including misspecified priors.

No mathematical object representing this experiment class is introduced. The paper should define, for example,

\[
\mathfrak K_n,\qquad P_{\theta_0,z_0}^{\kappa_n},
\qquad \Pi_n^{\nu,\kappa_n},
\]

and then state every uniform probability assertion with explicit quantifiers.

There are naturally two filtrations at block \(i\): one before the action and one after the action but before the observation noise. The contrast proof conditions before action randomization. The score proof needs the sensitivity to be measurable after the current action is selected and before \(\xi_i\) is drawn. The paper informally moves between these viewpoints.

A publishable proof must specify

\[
\mathcal F_{i-1}\subset \mathcal G_i\subset \mathcal F_i,
\]

with the action measurable in \(\mathcal G_i\) and \(\xi_i\) independent of \(\mathcal G_i\). It must also distinguish the realized bracket from the bracket averaged over fresh action randomization.

The current prose is enough to guess the intended construction. It is not enough to support the theorem as written.

## R38-M2. The empirical-contrast net omits variables over which uniformity is claimed

The proof of `lem:r35-excitation` fixes \(\theta_0\) and introduces a net over candidate \(\theta\) and direction \(v\). The theorem later takes a supremum over \(\theta_0\) in a compact interior set.

To justify the literal uniform statement, the stochastic field must be indexed by the true parameter as well, or a common translation argument must be supplied. The proof must give:

1. the full compact index set;
2. deterministic bounds and Lipschitz constants on that full set;
3. a finite net whose cardinality is independent of \(n\) and of the policy;
4. the Azuma or Freedman constants;
5. the interpolation loss for both the realized field and its conditional expectation; and
6. treatment of the extension at \(\theta=\theta_0\).

The sign-pair conditional identity is convincing. The simultaneous all-candidate, all-true-parameter exponential event is only sketched.

## R38-M3. Uniform `O_P` notation is carrying unproved quantifiers

In `thm:r35-lan`, several terms are collected into a uniformly tight random variable \(Z_n\). The underlying probability law varies with the policy, true parameter, true state, and prior. Ordinary `O_P` notation under one fixed law does not express this.

The paper needs a definition such as

\[
\lim_{K\to\infty}\sup_n\sup_{E\in\mathfrak E_n}
P_E(|Z_{n,E}|>K)=0,
\]

followed by a proof that each term satisfies it. The innovation field, initial-state cross term, nuisance derivative, empirical contrast event, and lower evidence event should be handled separately.

Without this, the advertised policy-uniform triangular theorem is not proved; only a plausible fixed-experiment argument is visible.

## R38-M4. The random-information Laplace theorem is compressed beyond acceptability

The BvM theorem does not assume \(I_n\) or \(\Delta_n\) converges. That is permissible, but it requires a careful relative \(L^1\) argument on moving random Gaussian densities.

A standalone lemma should prove, uniformly over the experiment class:

- deterministic upper and high-probability lower spectral bounds for \(I_n\);
- tightness of \(\Delta_n\);
- uniform local likelihood expansion on every fixed ball;
- a common integrable tail envelope;
- uniform prior-ratio convergence on fixed balls;
- convergence of unnormalized integrals relative to the random Gaussian normalizer; and
- stability of normalization in total variation.

The current proof states these ideas in a few sentences. It does not provide enough estimates to verify the relative error in either the BvM formula or the evidence expansion.

I regard the fixed-ball quadratic expansion as plausible. I do not regard the full uniform total-variation theorem as established at top-journal proof standard.

## R38-M5. The misspecified initial-state prior is not named as misspecification

The true initial state may lie outside the support of \(\nu\). Then the data-generating law is outside the Bayesian model used to form the marginal likelihood. The resulting object is a quasi-posterior or a posterior under model misspecification from the stated frequentist truth.

The paper calls it the “actual marginal parameter posterior.” That terminology is misleading.

The authors should state:

- the assumed Bayesian model;
- the external true experiment;
- the corresponding pseudo-true parameter;
- why the pseudo-true parameter remains \(\theta_0\);
- whether \(\nu\) may depend on \(n\); and
- which conclusions are Bayesian identities versus frequentist asymptotics under misspecification.

The transient bound likely makes the correction manageable. The conceptual distinction is mandatory.

## R38-M6. The filter-jet theorem is not proved in the claimed strong topology

`thm:r35-filter` is one of the most distinctive statements, and one of the least adequately proved.

The paper must define precisely:

- the Banach norm on \(C_b^r(\mathscr H)\);
- the tensor norm for parameter derivatives;
- the norm on the dual-valued derivative functional;
- the meaning of \(\partial_\theta^j\delta_{x_n^\theta}\);
- strong measurability of the random dual-valued map;
- measurability of the supremum over \(\theta\); and
- strong, rather than merely weak-on-tests, differentiability.

The present argument says that one additional bounded test derivative controls the Taylor remainder and that likelihood derivatives have polynomial total-variation bounds. That is the right strategy, but it is not the proof.

At minimum, the authors need an explicit deterministic lemma showing norm differentiability of

\[
\theta\mapsto
\int \phi(x_n^\theta+T_\theta(t_n)z)\,w_{n,	heta}^
u(dz)
\]

as an element of the stated dual, uniformly over the unit ball of tests and over arbitrary Borel \(\nu\) supported in the Hilbert ball. They then need a separate stochastic envelope argument for the normalized likelihood derivatives.

Until that is written, the strong filter-jet claim remains an assertion.

## R38-M7. The state “BvM” is rank two and should not be advertised as infinite-dimensional Gaussian asymptotics

The current-state corollary pushes a two-dimensional random Gaussian through

\[
G_n:\mathbb R^2\to\mathscr H.
\]

Its covariance has rank at most two. All infinite-dimensional initial-state uncertainty has been exponentially erased. This may be a valid bounded-Lipschitz approximation, conditional on the parameter BvM and filter theorem.

It is not an infinite-dimensional Bernstein--von Mises limit in the usual sense. The title and abstract should not invite that interpretation.

## R38-M8. The preparation-label theorem is a routine finite-mixture consequence, not a phase theorem

The “preparation-memory amplitudes” are normalized finite-component evidences. Their limiting randomness comes from the finite amount of early information retained in the summable initial-state likelihood correction.

The result is plausible once component-wise evidence expansions are proved uniformly. The manuscript should still define whether the label is latent or observed, identify the true component law, and state the common-policy assumption formally.

The current terminology overstates the result. This is a finite-mixture Bayes-factor corollary, not a new theory of phases or persistent macroscopic memory.

## R38-M9. The exact certificate proves only a narrow finite algebraic inequality

The rational certificate is useful. It supports one concrete parameter rectangle and one derivative bound for the two-duration map. It does not verify:

- the experiment construction;
- the empirical martingale net;
- global posterior localization;
- the random-information BvM argument;
- strong dual filter jets;
- the state-posterior corollary;
- the label-mixture theorem;
- novelty; or
- journal significance.

The proof ledger correctly says that no formal proof assistant was used. The manuscript should stop using “verified” as a general adjective when the verification is a local certificate plus author-written regression tests.

## R38-M10. The failed remote workflow must be described accurately

At the frozen head, the Round-Thirty-Five workflow completed with conclusion `failure`. The recorded job contains no executed steps. This is consistent with a runner or pre-execution failure; it is not evidence that the mathematical tests failed.

Equally, it is not a successful independent build. The accurate statement is:

> local verification is committed; remote verification of the frozen head is absent.

No stronger claim is warranted.

---

# 6. Theorem-by-theorem disposition

| Result | Correctness assessment | Top-four assessment |
|---|---|---|
| Uniform energy estimate and semigroup derivatives | The Lyapunov calculation appears correct for the bounded, uniformly damped and pinned generator. | Standard stable-semigroup estimate. |
| Integrated initial-state likelihood | The likelihood factorization and summable derivative budget are plausible. The model-misspecification interpretation and uniform quantifiers are not formalized. | Useful transient lemma, not a difficult semiparametric theorem. |
| Two-duration embedding | The displayed Taylor algebra is correct; the conservative small-time argument is credible. | Elementary inversion of two local coefficients. |
| Rational embedding certificate | Credible for the stated box if the checked source matches the frozen manifest. | Reproducibility artifact of narrow scope. |
| Four-word conditional excitation | The sign-pair identity is correct-looking. | Forced persistent excitation, not an adaptive-design breakthrough. |
| Uniform empirical contrast | Plausible, but the net proof omits the full true-parameter index and explicit uniform quantifiers. | Standard compact-net martingale concentration once written. |
| Smooth score field | Plausible with a two-stage filtration. | Standard finite-dimensional martingale-field estimate. |
| Fixed-ball quadratic likelihood | Plausible from bounded derivatives and Gaussian innovations. | Regular parametric expansion. |
| Global root-\(n\) localization | Coercive idea is sound; uniform tightness is compressed into `O_P`. | Standard contrast-plus-score localization. |
| Total-variation BvM | Plausible after a complete random-information Laplace lemma; not presently proved at the claimed uniform level. | Model-specific regular parametric BvM adjacent to existing adaptive-data theory. |
| Evidence expansion | Gaussian constant is correct; relative error inherits the BvM proof gap. | Standard Laplace formula. |
| Filter jets | Strategy is plausible; strong dual norm differentiability is not established in detail. | Potential specialist lemma, not a top-four theorem. |
| Current-state Gaussian image | Plausible conditional consequence. | Rank-two random image, not genuine infinite-dimensional BvM. |
| Jacobi bath memory | Schur-complement formula appears correct. | Standard and disconnected from inference. |
| Preparation labels | Plausible finite-mixture consequence. | Routine Bayes-factor corollary. |
| B1/B3/C2 corrections | The local corrections appear to address the stated endpoint, moment-range, and zero-evidence issues. | Errata/supporting lemmas, not independent research papers. |

This table is the core of the decision. The manuscript is not rejected because every line is wrong. It is rejected because the plausible mathematics is regular, special, under-situated, over-advertised, and below the requested significance threshold.

---

# 7. The manuscript is not in acceptable top-journal form

## 7.1 Internal audit machinery should not be part of the article

The title matter refers to a controlling referee report, immutable report commits, proof ledgers, round numbers, and repository history. Those may be useful for internal project governance. They are not substitutes for a self-contained mathematical paper.

A journal submission should contain:

- one stable title;
- one precise principal theorem;
- a normal introduction explaining novelty;
- complete proofs;
- a serious bibliography; and
- a conventional appendix for computations.

The branch chronology should be removed from the mathematical narrative.

## 7.2 Twelve pages are not enough for the claimed theorem package

The focused manuscript attempts to cover:

- infinite-state mechanics;
- global identifiability;
- adaptive martingale concentration;
- a uniform triangular BvM theorem;
- misspecified initial-state priors;
- strong filter derivatives;
- a Hilbert-state posterior approximation;
- a memory-kernel resolvent; and
- preparation-label evidence limits.

The result is severe compression. Several “proofs” are paragraph-length road maps for arguments that require independent lemmas and careful quantifiers.

The solution is not to add more claims. It is to choose one principal contribution and prove it completely.

## 7.3 The abstract overstates the infinite-dimensional content

Phrases such as “infinite-dimensional nuisance,” “actual infinite-state filtering,” and “current-state posterior approximation” are formally defensible but rhetorically misleading here. The nuisance decays exponentially, the parameter is two-dimensional, and the final Gaussian covariance is rank two.

The abstract should say exactly that.

---

# 8. Questions the authors must answer before any specialist submission

1. What theorem is new relative to Baumeister--Scondo--Demetriou--Rosen and the subsequent infinite-dimensional adaptive-identification literature?

2. What theorem is new relative to modern adaptive Gaussian BvM results once the model-specific response map and forced information bound have been verified?

3. Why is the infinite half-line essential to the inferential theorem, rather than only to the separate memory formula?

4. Can the authors state the exact triangular experiment class and prove every advertised uniformity with one set of quantifiers?

5. Is the initial-state prior allowed to depend on \(n\)? If so, state and prove that version. If not, remove language suggesting uniformity over arbitrary prior sequences.

6. What is the exact Banach-valued derivative asserted in the filter theorem, and where is norm differentiability proved?

7. Is the preparation label latent? What is the true component, and is the policy allowed to know the label?

8. Which principal inference theorem uses the memory kernel? If none, why are the two presented as one contribution?

9. Why should compulsory fixed-probability calibration be described as a substantive adaptive-design theorem?

10. What successful independent build or remote verification exists for the frozen source? At present, none is recorded.

---

# 9. Minimum requirements for a credible specialist-journal paper

These are not a top-four revision checklist. They are minimum conditions for a new specialist submission.

1. **Rewrite the literature review.** Compare exact hypotheses and conclusions with classical and current infinite-dimensional identification, persistence-of-excitation, adaptive inference, and partially observed system-identification work.

2. **Choose one principal theorem.** Identification plus BvM is a coherent candidate. Treat memory and preparation labels as applications or remove them.

3. **Define the experiment rigorously.** Introduce policy kernels, the before-action and after-action filtrations, the triangular law, and the meaning of every uniform probability statement.

4. **State the misspecification theorem honestly.** Separate the Bayesian working model from the external true initial state.

5. **Write the empirical-contrast proof in full.** Include the true parameter in the index set and record the net and interpolation constants.

6. **Write a standalone random-information Laplace lemma.** Prove localization, relative unnormalized \(L^1\) convergence, tail domination, and normalization.

7. **Write the filter-jet functional analysis in full.** Define the spaces and prove strong dual differentiability uniformly over arbitrary supported priors.

8. **Reduce the claims.** Do not call a rank-two Gaussian image an infinite-dimensional BvM theorem, and do not call finite-mixture Bayes factors phase amplitudes without qualification.

9. **Separate computation from proof.** State exactly what the rational certificate certifies and what it does not.

10. **Obtain a successful clean build.** A failed pre-execution workflow is not a mathematical problem, but a reproducible submission should have a successful frozen-source run.

11. **Remove round-governance prose from the article.** Referee-report hashes and branch history belong in repository documentation, not in the journal manuscript.

---

# 10. What kind of result could change the top-four assessment

A genuinely stronger project would have to confront a difficulty that the current assumptions deliberately remove. Examples include:

- identifying a spatially varying damping or stiffness field;
- recovering an unknown Jacobi sequence or bath spectral measure;
- inferring the memory kernel itself and propagating posterior uncertainty to it;
- treating an unbounded wave, beam, or PDE generator with an unbounded observation operator;
- allowing neutral or polynomially decaying nuisance directions that contribute at root-\(n\) scale;
- deriving excitation from an optimizing adaptive policy rather than imposing fixed diagnostic mass;
- proving a general nonlinear adaptive BvM theorem whose hypotheses are verified by the lattice as a nontrivial example; or
- establishing a phenomenon that fails for every finite-chain replacement and is genuinely caused by the infinite bath.

Any of these would be a new research project. That is exactly why the present paper is not a top-four major-revision case.

---

# 11. Final recommendation

The authors deserve credit for replacing an incoherent multi-paper closure claim with a concrete and mostly coherent model. The local mechanics and Gaussian calculations appear substantially more responsible than earlier versions. The proof ledger also correctly leaves the original programme open.

Nevertheless, the manuscript does not meet the standard of *Annals of Mathematics*, *Inventiones Mathematicae*, *JAMS*, or *Acta Mathematica*.

The decisive reasons are:

1. the inferential core is a regular two-parameter Gaussian problem under compulsory excitation;
2. the known stable infinite bath is not the source of a new statistical phenomenon;
3. direct prior art is omitted and novelty is not established;
4. the strongest uniform and functional-analytic claims are not proved at publication level;
5. the memory and label sections are separate, standard or routine consequences; and
6. no revision after Round Thirty Six addresses these objections.

**Recommendation: reject; do not invite a top-four major revision.**

A substantially rewritten specialist paper may be worthwhile. It should be evaluated as a new submission, on a conventional manuscript, after the authors complete the literature comparison and proof obligations listed above.
