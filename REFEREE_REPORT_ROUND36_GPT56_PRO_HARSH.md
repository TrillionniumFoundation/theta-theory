# External Referee-Style Report on the Round-Thirty-Five Revision

## Recommendation: **Reject for Annals/Inventiones/JAMS/Acta-level publication; do not invite a major revision at that level**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round35-mechanical-identification-2026-09-03`  
**Immutable reviewed head:** `bca291f85e47916cc5f089c0c01350f0c0c6f3b0`  
**Reviewed source tree:** `bc45f1c9366f1d96723f4e3f87f4b65e775fd18b`  
**Mathematical source commit:** `38c71d53cba3ca99d7a7d0a49209a49e2ffdd3e0`  
**Controlling preceding review:** `REFEREE_REPORT_ROUND34_GPT56_PRO_HARSH.md` at commit `9f5276233b63218a0d89df6611381975dc873232`  
**New review branch:** `review/round36-gpt56-pro-harsh-mechanical-identification-2026-09-03`  
**Review date:** 3 September 2026  
**Reviewer:** GPT-5.6 Pro, at the repository user's request.

This is an AI-assisted independent referee-style assessment. It is not a report commissioned by, and it is not an editorial decision of, *Annals of Mathematics*, *Inventiones Mathematicae*, the *Journal of the American Mathematical Society*, or *Acta Mathematica*. I apply the correctness, originality, depth, breadth, and lasting-significance threshold appropriate to those journals.

---

## Executive verdict

Round Thirty Five is a substantial improvement in submission discipline. It no longer presents eleven mutually dependent research programmes as eleven completed papers. The focused unit

> *Constructive Adaptive Identification of Local Damping and Stiffness in an Infinite Mechanical Lattice*

is a real manuscript about a specified model. It has a fixed infinite Hilbert state, a bounded coupled generator, a physical input and output, a two-duration identification map, forced exploration by four action atoms, a transient unknown initial state, a parameter-posterior calculation, a current-state filter comparison, and a Jacobi-bath memory formula. The author also correctly leaves the old Sinai and hard-sphere programme open.

That change deserves explicit recognition. I do **not** find a responsible basis for repeating the Round-Thirty-Two claim that the active source is unmaterialized, and I do **not** find an elementary one-line counterexample that destroys every central Round-Thirty-Five theorem. The energy calculation, the leading step-response algebra, the sign-pair cancellation, the fixed-box embedding certificate, and the Jacobi Schur-complement calculation are broadly consistent on inspection.

The manuscript is nevertheless nowhere near the publication threshold of the four journals named above. The decisive problem is no longer wholesale algebraic invalidity. It is that the paper has not demonstrated a sufficiently original, deep, or important mathematical contribution. In its present form, the infinite-dimensional aspect is technically benign and largely disappears from the statistical asymptotics. The inferential core reduces to a regular two-parameter adaptive Gaussian regression with a bounded, exponentially dying nuisance term and compulsory persistent exploration. The memory formula is a separate standard Jacobi-resolvent computation. The supporting B1/B3/C2 notes are errata and elementary transfer lemmas, not additional top-journal papers.

The novelty discussion is especially inadequate. The bibliography has four entries and omits literature directly addressing adaptive parameter identification, persistence of excitation, stiffness/damping recovery, and stable SISO infinite-dimensional systems. This is not a cosmetic citation defect. Until the paper is compared theorem by theorem with that literature, the claimed contribution cannot be evaluated, let alone judged top-four material.

My formal recommendation is therefore:

> **Reject. Do not invite a major revision for a top-four general mathematics journal.**

A heavily expanded and substantially reframed version may be appropriate for a specialist journal in systems and control, inverse problems, or mathematical statistics. Such a submission should be treated as a new paper, not as the next closure round of the eleven-paper dossier.

---

# 1. Confidential recommendation to the editor

## 1.1 Decision

**Reject without a top-four major-revision invitation.**

The paper has crossed an important threshold from “proposed proof architecture” to “focused, mostly coherent model calculation.” It has not crossed the much higher threshold from a coherent model calculation to a major research advance of broad mathematical interest.

The central construction is clever but modest:

1. use two short forcing durations to read the first parameter-dependent coefficients of a local step response;
2. include both signs of the forcing so the pre-existing state cross term cancels after conditional averaging;
3. impose a fixed positive lower probability for every diagnostic word;
4. exploit uniform exponential damping so the infinite initial state contributes only a summable transient;
5. apply a finite-dimensional quadratic likelihood and Laplace argument.

Every one of these steps is useful. Their combination does not, as presently situated, constitute an *Annals*, *Inventiones*, *JAMS*, or *Acta* theorem.

## 1.2 Why this is not a major revision decision

A top-journal major revision is appropriate when a paper already contains a result of the requisite conceptual importance and needs a finite set of repairs. Here the missing item is the principal editorial premise itself: a convincing novelty-and-significance case.

The paper could be made longer, the uniformity arguments could be formalized, and the bibliography could be enlarged. None of those changes, by itself, would turn a two-parameter bounded linear lattice experiment into a major general theorem. To reach the requested level, the authors would need a qualitatively stronger result—for example, identification of genuinely infinite-dimensional or spatially distributed unknowns, a new theorem for unbounded generators, a nontrivial partially observed adaptive design theorem beyond forced exploration, or a Bayesian asymptotic result that materially advances the existing adaptive-data theory.

That would be a new research project, not a repair list.

---

# 2. What was reviewed

I reviewed the focused source and its declared interfaces at the frozen head:

- `ROUND35_REVISION.tex`;
- `round35/mechanical.tex`;
- `round35/errata.tex`;
- `round35/references.tex`;
- `AUTHOR_RESPONSE_ROUND34.md`;
- `ROUND35_REVIEW_INDEX.md`;
- `round35/PROOF_LEDGER.json`;
- `round35/SOURCE_MANIFEST.json`;
- `round35/EMBEDDING_CERTIFICATE.json`;
- `tools/certify_round35.py`;
- `tools/mechanical_benchmark.py`;
- `tests/test_round35.py`;
- `ROUND35_LOCAL_VERIFICATION.json`;
- the active supporting files `round35/supporting/B1.tex`, `B3.tex`, and `C2.tex`;
- the four canonical entries switched to Round Thirty Five.

The reviewed head differs from the mathematical commit only by a byte-level correction to `round35/requirements.txt`. I found no later mathematical commit on the revision branch before freezing this report.

## 2.1 Verification status

The committed local record reports:

```text
44 tests run
0 test failures
29 manifest-bound source files
5 declared LaTeX builds
12-page focused manuscript
exact embedding certificate: true
formal proof assistant: false
remote CI verified: false
all original gaps closed: false
```

I accept that this is the author's local execution record. I do not equate it with proof verification.

The GitHub Actions workflow `Verify Round 35 immutable sources` has conclusion `failure` on the frozen head in both recorded attempts. The job record contains no steps and no assigned runner. I therefore interpret this as a failure before source execution, not as evidence that the tests or TeX build failed. The only sound conclusion is that **there is no successful remote verification record for this head**.

That repository fact is not a mathematical rejection reason. It should nevertheless be stated accurately.

## 2.2 Scope of the present decision

The focused C1/mechanical manuscript is the only plausible research-publication unit in Round Thirty Five. The B1, B3, and C2 entries are corrected supporting notes. The remaining original A/B/C/D programme is expressly left open in the proof ledger. I do not reject the focused paper merely because it does not prove the unrelated Sinai and hard-sphere targets.

Conversely, those open targets cannot be counted toward the significance of the focused paper. A research programme is not an additive significance multiplier for a theorem that does not establish its principal applications.

---

# 3. Summary of the mathematical content

The state space is

\[
\mathscr H=\ell^2(\mathbb N_0)\oplus\ell^2(\mathbb N_0),
\]

with a bounded half-line spring operator. The unknown parameter is the two-vector

\[
\theta=(c,k)
\]

appearing only in the damping and pinning at site zero. The bath damping, bath pinning, coupling, noise variance, force bound, and diagnostic probabilities are known.

At the end of each adaptively selected block, the experiment observes one noisy coordinate,

\[
Y_i=q_0(t_i)+\xi_i,
\qquad \xi_i\sim N(0,\sigma^2).
\]

Every one of the four atoms

\[
(\tau,a),\quad(\tau,-a),\quad(2\tau,a),\quad(2\tau,-a)
\]

has conditional probability at least \(\rho/4\), independently of sample size.

The short-time step response has expansion

\[
h_\theta(t)=\frac{t^2}{2}-\frac{ct^3}{6}
 +\frac{(c^2-k-\varepsilon)t^4}{24}+O(t^5).
\]

Two linear combinations of \(h(\tau)\) and \(h(2\tau)\) recover, to controlled error, first \(c\) and then \(k\). Positive and negative input signs remove the cross term caused by the current state. Uniform damping makes the contribution of the unknown initial state exponentially summable. A Gaussian likelihood argument then yields a local quadratic expansion, root-\(n\) posterior localization, and a total-variation Gaussian approximation using the realized information matrix.

The paper separately projects out site zero and computes the bath memory transform through a scalar Jacobi continued fraction.

This is a coherent outline. The question is not whether it is intelligible. The question is whether it is a sufficiently new and consequential theorem for the journals specified by the user. It is not.

---

# 4. Major objection I: the novelty review is grossly inadequate

## 4.1 Four references are not an acceptable priority analysis

The bibliography contains only:

1. Du–Nair–Janson on Bernstein–von Mises for adaptively collected data;
2. Finkelshtein on Ovsyannikov methods;
3. Bryutkin–Levine–Urteaga–Marzouk on canonical Bayesian linear-system identification;
4. Nickl on Bernstein–von Mises theorems for time-evolution equations.

This list does not cover the most directly relevant control and inverse-problem literature.

At a minimum, the authors must compare their theorem with:

- J. Baumeister, W. Scondo, M. A. Demetriou, and I. G. Rosen, **“On-Line Parameter Estimation for Infinite-Dimensional Dynamical Systems,”** *SIAM Journal on Control and Optimization* **35** (1997), 678–713. That paper treats adaptive identification in abstract linear and nonlinear infinite-dimensional systems, develops infinite-dimensional persistence of excitation, and includes estimation of stiffness and damping parameters in a one-dimensional wave equation with Kelvin–Voigt damping.

- M. A. Demetriou and I. G. Rosen, **“Adaptive identification of second order distributed parameter systems,”** *Inverse Problems* **10** (1994), 261–294.

- M. A. Demetriou and I. G. Rosen, **“On the persistence of excitation in the adaptive identification of distributed parameter systems,”** *IEEE Transactions on Automatic Control* **39** (1994), 1117–1123.

- S. Chattopadhyay, S. Sukumar, and V. Natarajan, **“Adaptive identification of linear infinite-dimensional systems,”** *International Journal of Control* **98** (2025), 593–608, DOI `10.1080/00207179.2024.2353731`; also arXiv:2305.11868. This work studies stable SISO infinite-dimensional systems, persistence of excitation, transfer-function coefficient recovery, parameter reconstruction, and PDE examples.

There is also a large literature on adaptive observers, positive-real infinite-dimensional systems, distributed-parameter identification, stochastic evolution systems, and Bayesian system identification. The report need not demand an encyclopedic bibliography. It does demand engagement with the papers most similar in model class and objective.

## 4.2 The omission changes the editorial assessment

The manuscript currently presents the combination

> infinite-dimensional stable plant + persistent excitation + local coefficient identification

as the central model-specific contribution. That combination has a long history. The possible novelty is therefore narrower:

- a particular two-duration/four-sign finite excitation library;
- a Bayesian total-variation posterior approximation under this library;
- treatment of a bounded but possibly misspecified initial-state prior as an exponentially transient nuisance;
- simultaneous display of a bath memory formula.

The paper does not establish that this narrower package is new. It merely says that priority is not asserted on the basis of an exhaustive search. That disclaimer is honest but editorially fatal at the top-four level. Authors, not referees, bear the burden of demonstrating novelty.

## 4.3 Required theorem-by-theorem comparison

A serious revision for any research journal should contain a table with columns:

| This manuscript | Closest prior theorem | Difference in model | Difference in assumptions | Difference in conclusion | Why the difference matters |
|---|---|---|---|---|---|

The comparison must address at least:

- online versus block observations;
- deterministic versus stochastic plant equations;
- known versus unknown bath/operator coefficients;
- finite versus infinite-dimensional unknowns;
- forced persistent exploration versus derived excitation;
- point/state observation versus general output operators;
- consistency versus posterior Gaussian approximation;
- known versus unknown noise variance;
- correctly specified versus misspecified initial-state priors;
- finite-dimensional approximations versus direct Hilbert-space proofs.

Without this analysis, a top-journal significance judgment cannot even begin.

---

# 5. Major objection II: the “infinite-dimensional” difficulty is largely decorative

## 5.1 The unknown is only two-dimensional and local

The unknown parameter is \((c,k)\), located at the observed and actuated site. Every bath coefficient is known. The bath is uniformly damped and pinned. The generator is bounded. The input and output are collocated at site zero.

These assumptions remove most of the difficulties that make infinite-dimensional inverse problems difficult:

- there is no unbounded generator domain;
- there is no unknown function or operator;
- there is no ill-posed observation inversion;
- there is no slowly decaying or conservative nuisance;
- there is no unknown bath spectrum;
- there is no non-Gaussian observation model;
- there is no partial identifiability modulo hidden symmetries;
- there is no mesh-refinement or posterior-dimension problem.

## 5.2 The identifying coefficients are local before the bath becomes relevant

The key expansion is

\[
h_\theta(t)=\frac{t^2}{2}-\frac{ct^3}{6}
 +\frac{(c^2-k-\varepsilon)t^4}{24}+O(t^5).
\]

The leading identification of \(c\) and \(k\) occurs in the first four coefficients at the driven coordinate. The infinite bath enters only through known coupling and the controlled remainder. Thus the infinite-dimensional calculation is used principally to certify that remote coordinates do not invalidate a finite local Taylor inversion.

That is mathematically legitimate. It is not a deep infinite-dimensional identification theorem.

A useful diagnostic question is:

> If the bath were replaced by a sufficiently large known finite chain, which principal theorem would fail?

For the current proof, essentially none of the statistical conclusions changes. The energy constants, response derivatives, excitation, Gaussian likelihood, BvM approximation, and finite-rank state image persist. The infinite half-line matters to the exact memory formula and to the statement that the proof does not pass through a truncation limit. It does not generate a qualitatively new inferential phenomenon.

## 5.3 Exponential stability trivializes the initial-state nuisance asymptotically

The initial state is infinite-dimensional, but its contribution satisfies an exponential estimate. Consequently its entire marginal log-likelihood correction is \(O_P(1)\), with fixed-order parameter derivatives also \(O_P(1)\). At root-\(n\) scale the correction is negligible.

This is a useful lemma. Calling it “infinite-dimensional nuisance” does not make it a semiparametric Bernstein–von Mises problem in the usual difficult sense. There is no nuisance tangent space competing at \(n^{-1/2}\) scale; no least-favourable direction; no semiparametric efficiency calculation; no posterior contraction rate for the nuisance; and no prior-mass condition near the true nuisance. The nuisance is dynamically erased.

That is precisely why the prior may miss the true initial state without altering the parameter limit. It is also why the result is much less ambitious than the abstract and title suggest.

---

# 6. Major objection III: the statistical theorem is a regular finite-dimensional adaptive regression in disguise

## 6.1 The likelihood after transient removal

After fixing the realized action record, the observation law is Gaussian with mean \(m_i^\theta\), plus a summable initial-state correction. The parameter is two-dimensional, the noise variance is known, the mean has uniformly bounded derivatives, and compulsory exploration provides a uniformly positive empirical information matrix.

Once those facts are established, the posterior theorem is a standard finite-dimensional Laplace argument with random design.

The manuscript itself cites Du–Nair–Janson, whose adaptive Gaussian experiment allows the covariate at time \(j\) to be selected from the previous history and proves total-variation Gaussian approximation using empirical information. Round Thirty Five is nonlinear in \(\theta\), but it does not establish a new general adaptive nonlinear BvM theorem. It verifies regularity and global contrast for one elementary stable mechanical model and carries out the familiar localization argument.

That may be publishable in a specialist venue. It is not a broad breakthrough in Bayesian asymptotics.

## 6.2 “No information limit” is not a new contribution here

The theorem approximates the posterior by

\[
N(I_n^{-1}\Delta_n,I_n^{-1})
\]

without assuming that \(I_n\) converges. The paper correctly avoids calling this classical LAN with a deterministic information limit.

But the absence of an information limit is already a central feature of adaptive-data BvM results. The manuscript explicitly acknowledges this. Therefore the novelty cannot be “BvM without information convergence.” It must lie in the model verification, and that verification is too special and elementary for the requested journals.

## 6.3 Forced exploration makes the information theorem nearly tautological

Every diagnostic atom has probability at least \(\rho/4\) at every block. This assumption forces persistent excitation forever. The policy can be adaptive only in the remaining probability mass.

The sign calculation

\[
\frac12[(d+ab)^2+(d-ab)^2]=d^2+a^2b^2
\]

is clean and useful. It also shows how strong the design assumption is. The paper does not prove that an optimizing or learning policy generates excitation. It hard-codes excitation into the admissible class.

This is not a defect in correctness. It sharply limits the claimed importance. The result is closer to “Bayesian inference under a randomized calibration schedule” than to a general adaptive-identification theorem.

---

# 7. Major objection IV: uniformity is asserted more broadly than it is formalized

The manuscript repeatedly states uniformity over:

- all admissible policies;
- policies that may depend on \(n\);
- all true initial states in a Hilbert ball;
- all initial priors on that ball;
- all true parameters in a compact interior subset.

These assertions are plausible because the proof uses deterministic envelopes. They are not formalized at a level suitable for publication.

## 7.1 The experiment class must be defined as a mathematical object

The paper should introduce notation such as

\[
\mathfrak P_n,
\qquad
P_{\theta_0,z_0}^{\pi_n},
\qquad
\Pi_n^{\nu,\pi_n},
\]

and state exactly:

- which sigma-fields are present before action selection and before observation noise;
- whether the fresh policy randomizer is part of the filtration;
- whether policies are universally measurable or Borel kernels;
- whether \(\pi_n\) may depend on the parameter prior or on \(n\);
- how null histories are handled;
- what “uniform in probability” means when the underlying probability spaces vary;
- whether suprema are ordinary or outer probabilities.

At present these matters are handled in prose.

## 7.2 Two-stage predictability should be explicit

The score terms are martingale differences because the current action is selected before the current Gaussian noise. There are naturally two filtrations:

\[
\mathcal F_{i-1}^{Y,A}
\subset
\mathcal G_i=\sigma(\mathcal F_{i-1}^{Y,A},A_i)
\subset
\mathcal F_i^{Y,A}.
\]

The sensitivity \(g_i\) is \(\mathcal G_i\)-measurable and \(\xi_i\) is independent of \(\mathcal G_i\). With this filtration the predictable bracket is exactly the realized information. With the coarser filtration one averages over the fresh action. The manuscript discusses this informally but should fix one convention before stating the martingale theorems.

## 7.3 Uniformity in the true parameter requires another index variable

The net proof of the empirical contrast is written for a fixed \(\theta_0\), with a net over candidate parameters and unit directions. The manuscript later takes a supremum over \(\theta_0\) in a compact set. To justify this literally, the net and Lipschitz estimates must include the true parameter as another index, or the proof must explain why the same finite net works uniformly after translation.

This is repairable. It is not presently written.

---

# 8. Major objection V: the global localization and BvM proof is too compressed

I did not find a direct contradiction in the likelihood expansion. The proof nevertheless compresses several nontrivial uniform steps into a few paragraphs.

## 8.1 A standalone uniform localization lemma is needed

The global bound is of the form

\[
\log\frac{L_n^\nu(\theta)}{L_n^\nu(\theta_0)}
\le -c n|\theta-\theta_0|^2
    +Z_n\sqrt n|\theta-\theta_0|.
\]

The paper should state and prove, with explicit quantifiers, that \(Z_n\) is uniformly tight over the full experiment class. The proof currently collects several terms under the symbol \(O_P\) while simultaneously taking suprema over policies, priors, initial states, parameters, and candidates.

## 8.2 The random-information Laplace lemma should be isolated

A clean theorem should say:

- \(I_n\) lies with high probability in one deterministic compact subset of positive definite matrices;
- \(\Delta_n\) is uniformly tight;
- the local log density converges uniformly on each fixed ball;
- a common integrable envelope controls all tails;
- the prior ratios converge uniformly on fixed balls;
- normalization converts unnormalized \(L^1\) convergence into TV convergence.

The present proof contains these ideas but does not separate them. This makes it difficult to distinguish a theorem from a sketch, especially because neither \(I_n\) nor \(\Delta_n\) is assumed to converge.

## 8.3 The evidence formula inherits the same uniformity burden

The formula

\[
\frac{\mathcal Z_n^\nu}{L_n^\nu(\theta_0)}
=\frac{2\pi\pi(\theta_0)}{n\sqrt{\det I_n}}
 \exp\left(\frac12\Delta_n^TI_n^{-1}\Delta_n\right)[1+o_P(1)]
\]

has the correct two-dimensional Gaussian normalization. The relative \(o_P(1)\), however, is only as strong as the preceding uniform Laplace lemma. It should not be left as a one-line consequence of “completing the square.”

---

# 9. Major objection VI: the initial-state prior is deliberately misspecified, but the terminology is not

The true initial state need not belong to the topological support of \(\nu\). Thus the data-generating law can lie outside the Bayesian model used to construct the marginal likelihood.

The conclusion may still be correct because the mismatch is exponentially transient. But this is a **misspecified or quasi-Bayesian posterior** from a frequentist point of view. Calling it simply the “actual marginal parameter posterior” obscures the distinction.

The paper should specify:

1. the assumed Bayesian model;
2. the true data-generating experiment;
3. the pseudo-true parameter under misspecification;
4. why the pseudo-true parameter equals \(\theta_0\);
5. whether the result is uniform over sequences of misspecified priors;
6. which posterior statements are Bayesian identities and which are frequentist asymptotics under an external truth.

The transient estimate probably makes this section straightforward. It is conceptually important and potentially one of the more interesting aspects of the paper. It should be treated as a theorem, not hidden inside a permissive prior sentence.

---

# 10. Major objection VII: the filter-jet theorem needs a real functional-analytic proof

The filter comparison is one of the more distinctive claims. It deserves more than the current compressed argument.

## 10.1 Exact Banach spaces and measurability

The paper uses the norm dual of \(C_b^{j+1}(\mathscr H)\), where derivatives are Fréchet derivatives. It should state:

- the precise norm on \(C_b^r\);
- whether the space is complete under that norm;
- how signed derivative functionals are identified;
- strong measurability of the random dual-valued derivatives;
- whether the supremum over \(\theta\) is measurable;
- the meaning of \(\partial_\theta^j\delta_{x_n^\theta}\) as a symmetric multilinear parameter derivative.

## 10.2 Uniform Taylor remainder on the test unit ball

The proof says that one extra test derivative controls the strong dual derivative. This is plausible: bounded \((j+1)\)-st derivatives yield a uniform remainder for the \(j\)-th derivative. It should be written as an explicit lemma with the relevant operator norms.

Pointwise differentiation against every test is not sufficient for norm differentiability in a dual. Earlier rounds repeatedly made this mistake. Round Thirty Five appears to know the issue, but the final proof should show the norm estimate, not merely state that “the same likelihood majorants justify” it.

## 10.3 Interpretation of the state-posterior Gaussian

The state corollary approximates the scaled current state by the push-forward of a two-dimensional random Gaussian under \(G_n\). Its covariance has rank at most two and need not converge.

That is a valid finite-rank approximation statement. It is not an infinite-dimensional Bernstein–von Mises limit in the usual sense. The abstract should not encourage that interpretation. The infinite state uncertainty from the initial condition has vanished; only two parameter directions remain.

---

# 11. Major objection VIII: the memory result is correct-looking but editorially separate and standard

The bath calculation gives

\[
s(z)=\frac{p(z)-\sqrt{p(z)^2-4\varepsilon^2}}{2},
\qquad
p(z)=z^2+c_bz+k_b+2\varepsilon.
\]

This is the standard scalar Schur-complement/continued-fraction solution for a constant-coefficient half-line Jacobi operator. The high-frequency coefficients are consistent with the block products. The theorem is a useful exact calculation.

It does not materially interact with the adaptive posterior theorem. The same physical model appears in both sections, but the memory formula is neither used to prove identification nor inferred from the posterior. The manuscript currently bundles two modest results:

- a two-parameter adaptive Gaussian inference theorem;
- a textbook-resolvent formula for the bath.

Their coexistence does not create top-journal depth.

For a specialist submission, the authors should decide whether memory is:

1. an application illustrating the model;
2. an essential inferential quantity to be estimated;
3. an object whose uncertainty is propagated through the posterior;
4. or an independent appendix.

At present it is the fourth, presented rhetorically as the third.

---

# 12. The exact certificate: useful reproducibility, limited mathematical force

The rational certificate verifies one concrete box:

\[
c,k\in[1,2],\quad c_b=3/2,\quad k_b=1,
\quad\varepsilon=1/10,\quad\tau=1/32.
\]

It computes finite local Taylor coefficients and bounds the infinite tail by an operator-norm series. The reported Frobenius error is below \(1/2\) in operator norm, so it supports the concrete embedding claim.

This is good practice. It is not a proof assistant verification of the manuscript, and it does not establish:

- the martingale net argument;
- the uniform posterior localization;
- the total-variation BvM theorem;
- the filter-jet topology;
- the label-mixture limit;
- novelty or significance.

The manuscript and certificate are honest about this. The editorial report should be equally clear: reproducibility of an elementary inequality is not evidence of top-four depth.

---

# 13. The supporting corrections

## 13.1 B1 singleton endpoint

The active source now correctly separates \(m=1\), where the relative energy is a point mass at zero, from \(m\ge2\), where the positive-shape gamma law applies. The correction is satisfactory.

## 13.2 B3 Minkowski range

The scalar-to-Hilbert moment implication now explicitly assumes \(p\ge2\), proves the inequality for finite sums, and passes by monotone convergence. This is satisfactory as an abstract lemma. The hard-sphere within-cell estimate remains open, as it should.

## 13.3 C2 zero-evidence versions

The evidence-weighted comparison now chooses conditional versions bounded by \(\|F\|_\infty\) on zero-evidence sets. This removes the Round-Thirty-Four counterexample. The correction is satisfactory.

## 13.4 C2 BSDE measurability

The mark space, compensator, predictability, driver measurability, and fixed martingale-representation filtration are now specified. This makes the fixed-basis BSDE statement well typed.

These corrections close local errors. They are not research papers and should not be presented as four independent canonical publication units.

---

# 14. Theorem-by-theorem disposition

| Result | Correctness assessment in this review | Originality/significance assessment |
|---|---|---|
| Uniform energy and semigroup derivatives | The Lyapunov computation appears correct for the bounded, uniformly damped and pinned generator. | Standard stable-semigroup perturbation estimate. |
| Integrated initial-state likelihood | Formula and exponential derivative budget are plausible; misspecification and uniform quantifiers need formalization. | Useful transient-nuisance lemma, but not a difficult semiparametric result. |
| Two-duration embedding | Leading algebra is correct; the small-time estimate and concrete certificate are credible. | Elementary local Taylor inversion for two site-zero coefficients. |
| Exact rational certificate | Supports the stated parameter box. | Reproducibility device, not a research contribution by itself. |
| Four-word excitation | Sign cancellation and conditional lower bound are correct-looking; uniform net proof needs full quantifiers. | Forced persistent excitation, not an adaptive-design theorem. |
| Smooth martingale score | Plausible under a two-stage filtration; uniformity should be rewritten. | Standard finite-dimensional martingale-field estimate. |
| Local quadratic likelihood | Plausible on fixed balls with the stated bounded derivatives. | Regular parametric expansion. |
| Global posterior localization | Main coercive idea is sound; proof is too compressed for the claimed uniform class. | Standard contrast-plus-martingale localization. |
| TV posterior approximation | Plausible after a complete random-information Laplace lemma. | Model-specific instance adjacent to existing adaptive BvM theory. |
| Evidence expansion | Correct normalization; inherits BvM uniformity gap. | Standard Laplace evidence formula. |
| Filter jets | Potentially useful; strong dual differentiability needs expanded proof. | Infinite initial state is exponentially erased; only finite parameter directions survive. |
| State-posterior Gaussian | Plausible BL push-forward consequence. | Rank-two random Gaussian approximation, not an infinite-dimensional BvM theorem. |
| Bath memory | Schur-complement formula appears correct. | Standard Jacobi resolvent computation, independent of inference theorem. |
| Preparation-label amplitudes | Plausible finite-mixture Bayes-factor consequence. | Routine corollary of the bounded transient evidence. |
| B1/B3/C2 corrections | Local corrections are satisfactory. | Errata/supporting lemmas, not top-journal papers. |

This table explains the rejection. The paper is no longer rejected because every theorem is obviously false. It is rejected because the body of plausible results is too standard, too special, and too weakly situated in the literature for the requested venue.

---

# 15. What would constitute a genuinely stronger result

The authors should not attempt another round of rhetorical “closure.” They should decide which mathematical problem they actually want to solve.

A substantially stronger paper could pursue one of the following directions.

## 15.1 Identify an infinite-dimensional unknown

For example:

- a spatially varying damping or stiffness coefficient;
- an unknown bath spectral measure;
- an unknown Jacobi sequence;
- an unknown boundary operator;
- an infinite-dimensional forcing profile.

Then posterior contraction, identifiability, and uncertainty quantification would confront a genuinely infinite-dimensional inverse problem.

## 15.2 Treat an unbounded mechanical generator

A wave, beam, or PDE generator with domain issues would make the response derivatives, observation operator, and adaptive likelihood nontrivial. The current bounded operator avoids these questions.

## 15.3 Remove compulsory fixed exploration

Derive excitation from an optimizing policy, or characterize the tradeoff between reward and information. A theorem saying that every diagnostic action is sampled with a fixed positive probability is a calibration theorem, not a general adaptive-design result.

## 15.4 Allow persistent nuisance directions

If the initial state decays only polynomially, contains neutral modes, or interacts with the parameter at root-\(n\) scale, the nuisance would no longer be an \(O(1)\) correction. That could produce real semiparametric mathematics.

## 15.5 Infer the memory kernel

The current paper computes the memory kernel from known bath parameters. A more consequential theorem would infer the kernel or bath parameters from the same adaptive observations and propagate posterior uncertainty to the memory law.

Any one of these directions would require a new manuscript and a new novelty review.

---

# 16. Minimum requirements for a specialist-journal submission

The following are not a top-four major-revision checklist. They are minimum requirements before the focused paper should be submitted elsewhere.

1. **Replace the four-reference bibliography with a serious literature review.** Include the classical and current infinite-dimensional adaptive-identification literature and compare hypotheses and conclusions explicitly.

2. **State one principal theorem.** The abstract currently lists identification, BvM, filtering, evidence, state posteriors, memory, and preparation labels. Identify the one result that is new and make the rest corollaries or applications.

3. **Define the experiment class formally.** Introduce the two-stage filtration, policy kernels, probability laws, priors, and uniformity notation.

4. **State the misspecified-prior theorem honestly.** Distinguish the assumed Bayesian model from the true initial state and explain why the pseudo-true parameter remains the physical parameter.

5. **Expand the empirical-contrast proof.** Give the full index set, net, interpolation constants, and uniform treatment of \(\theta_0\).

6. **Expand the random-information BvM proof.** Isolate localization, unnormalized \(L^1\) convergence, tail domination, and normalization as separate lemmas.

7. **Expand the filter-jet proof.** Define the Banach and dual norms, dual-valued measurability, multilinear derivatives, and uniform Taylor estimates.

8. **Reframe the infinite-dimensional claim.** Explain precisely which theorem would fail for a finite chain and which part genuinely uses the half-line limit.

9. **Clarify the role of the memory section.** Either connect it to an inferential result or move it to an appendix.

10. **Remove the eleven-paper packaging from the publication unit.** The focused paper should not carry unrelated canonical-entry machinery and historical closure terminology into a journal submission.

11. **Report remote verification accurately.** At the frozen head no workflow steps ran successfully. This need not delay mathematical submission, but the repository should not imply otherwise.

12. **Tone down the title and abstract unless a stronger theorem is proved.** “Infinite mechanical lattice” currently advertises more inferential complexity than the theorem uses.

---

# 17. Minor mathematical and expository comments

1. The symbol \(\pi\) is used for the parameter prior while policy notation is mostly prose. Reserve distinct notation for priors and policies.

2. State explicitly that the four atom probabilities require \(0<\rho\le1\) and that the residual policy distribution has mass \(1-\rho\).

3. Define the total-variation convention. Some authors include the factor \(1/2\), others do not.

4. The phrase “actual marginal parameter posterior” should be replaced when the true initial state can lie outside the prior support.

5. The statement that policies may depend on sample size should be moved into the formal definition of the policy class.

6. The constants in the conservative \(\tau_0\) theorem are extremely small. Explain whether the concrete certificate, rather than the generic bound, is intended to carry the practical example.

7. The embedding certificate should record the exact source commit in generated evidence, while avoiding self-referential manifest hashes.

8. Separate the general \(\varepsilon\ge0\) theorem from the genuinely coupled \(\varepsilon>0\) result. At \(\varepsilon=0\), the bath is statistically irrelevant.

9. State whether the Gaussian noise variables are independent of all policy randomizers and the initial state under both the assumed model and the true experiment.

10. The phrase “nonlinear mechanical mean” should not be confused with a nonlinear mechanical system. The state equation is linear; the output mean is nonlinear as a function of the coefficients.

11. Give a precise finite-chain comparison theorem if the claim is that the proof is intrinsically infinite-dimensional.

12. In the label theorem, distinguish a latent preparation label from a known experimental label. If the policy observes the label, policy factors need not be common.

13. The almost-sure limit \(R_\infty^\nu\) is stated only for one fixed infinite policy. Keep this qualification in every later use.

14. The memory square-root branch should be specified on a connected component of the resolvent set, not merely by a phrase about continuation wherever used.

15. The local verification JSON is useful, but the manuscript should not cite test counts as mathematical evidence.

---

# 18. Final editorial assessment

Round Thirty Five is the first revision in this sequence that resembles a plausible focused research manuscript rather than an eleven-node proof ledger. The authors have made several correct strategic choices:

- they chose a specific model;
- they materialized the proof before verification;
- they stopped claiming that unrelated old applications were closed;
- they repaired the Round-Thirty-Four local errata in active source;
- they distinguished posterior Gaussian approximation from frequentist coverage;
- they did not call random-information local quadratic approximation classical LAN;
- they recorded the limits of the exact certificate.

Those improvements materially raise the mathematical credibility of the project.

They do not make the paper a top-four contribution. The plant is a bounded, uniformly stable, fully known infinite bath with two unknown local coefficients. Persistent excitation is imposed by fixed action atoms. The infinite initial state is exponentially negligible. The BvM theorem is a regular finite-dimensional adaptive Gaussian Laplace calculation after model-specific identifiability is established. The filter result is a stable push-forward estimate. The memory formula is a standard Jacobi Schur complement. The literature comparison omits work directly on adaptive identification of infinite-dimensional systems and even prior stiffness/damping estimation in distributed mechanical models.

The manuscript may contain a publishable specialist result after substantial rewriting. It does not contain a result of the originality, difficulty, generality, or mathematical consequence expected by *Annals of Mathematics*, *Inventiones Mathematicae*, the *Journal of the American Mathematical Society*, or *Acta Mathematica*.

## Final recommendation

> **Reject for the requested top-four-journal level. Do not invite a major revision at that level. A future specialist-journal submission should be a new, self-contained paper with a comprehensive priority analysis and fully expanded uniform-in-policy proofs.**
