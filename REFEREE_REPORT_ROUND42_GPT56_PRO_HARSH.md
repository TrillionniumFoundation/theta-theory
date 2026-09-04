# External Referee Report on the Round-Forty-One Revision Branch State

## Recommendation: **Return without review / reject at Annals–Inventiones–JAMS–Acta level: the frozen branch contains no materialized manuscript**

**Repository:** `TrillionniumFoundation/theta-theory`  
**Claimed revision branch:** `revision/round41-referee-positive-closure-gpt56pro-2026-09-04`  
**Immutable reviewed head:** `7be5768713ab4e4247c5e1538fd470c38edf57a7`  
**Reviewed source tree:** `fc4f3a5a57f1033ed0f74c091fe120c4a83124eb`  
**Controlling preceding report:** `REFEREE_REPORT_ROUND40_GPT56_PRO_HARSH.md` at commit `1144f2c08a9dee66b6cc12b3bcc35252a054160b`  
**New review branch:** `review/round42-gpt56-pro-harsh-round41-materialization-2026-09-04`  
**Review date:** 4 September 2026  
**Reviewer:** GPT-5.6 Pro, at the repository user's request.

This is an AI-assisted independent referee-style assessment. It is not a report commissioned by, and it is not an editorial decision of, *Annals of Mathematics*, *Inventiones Mathematicae*, the *Journal of the American Mathematical Society*, or *Acta Mathematica*. I apply the correctness, originality, depth, self-containment, reproducibility, and lasting-significance threshold appropriate to those journals.

---

# Executive verdict

There is no Round-Forty-One manuscript to referee at the frozen revision head.

The branch does **not** contain:

- `ROUND41_REVISION.tex`;
- `ROUND41_READY_FOR_REVIEW.md`;
- `ROUND41_REVIEW_INDEX.md`;
- `AUTHOR_RESPONSE_ROUND40.md`;
- a `round41/` source directory;
- `tools/verify_round41.py`;
- a Round-Forty-One source manifest;
- a Round-Forty-One local-verification record; or
- a committed Round-Forty-One PDF.

The head commit is a CI/bootstrap commit entitled

```text
ci(round41): add source-only materialization lane
```

and adds a workflow whose purpose is to run a Python source generator, check for the files listed above, and push the generated files back to the same revision branch. The immediately preceding commit adds another permission-safe materialization fallback. The checked-in wrapper reads `tools/materialize_round41.py`, rewrites one source anchor **in memory**, and executes the modified generator with `exec(compile(...))`.

At the review freeze, the current materialization and verification runs had not produced a descendant source commit. Relevant current runs were queued; previous attempts on earlier branch heads had failed or been cancelled. The branch still pointed to `7be5768...`, and every principal Round-Forty-One review entry returned `404 Not Found`.

A generator containing string literals for a proposed future paper is not the paper. A workflow that may later mutate the branch is not an immutable submission. A referee cannot certify theorem statements, hypotheses, cross-references, bibliography, proof context, source integrity, or a build that do not exist in the reviewed tree.

The formal recommendation is therefore:

> **Return without review. In top-four editorial language, reject the present submission as administratively and mathematically non-reviewable. Do not count Round Forty One as a revision of the manuscript.**

The authors may submit a new, immutable revision after committing the actual source directly. Such a resubmission must be treated as a new review object with a new frozen SHA. No closure credit is due for text that exists only inside an unexecuted source-writing program.

I did inspect the checked-in materializer far enough to understand the intended response. It proposes directionally sensible repairs to several Round-Forty defects: a finite-prefix calibration condition, common force and duration bounds, an explicit duration-before-sign chronology, a compact Jacobi coefficient box, a supremum-norm compact-class strong law, deterministic separable filter-jet ranges, and a closed-set posterior upper-rate statement. Those intended changes are discussed provisionally below. They are **not** reviewed or accepted theorems because the generated source is absent.

Even if the generator were executed exactly as presently written, the intended result would still face a severe top-four significance problem. The proposed Jacobi “rate” is an upper large-deviation bound in a sampled response metric. Its coefficient modulus is asserted positive by compactness, not estimated quantitatively. The manuscript would still provide neither a matching lower bound, an explicit inverse-stability modulus, depth-dependent coefficient rates, operator-norm recovery, nor infinite-dimensional uncertainty quantification. The finite-dimensional part remains a regular five-parameter Gaussian theorem under engineered calibration.

---

# 1. The frozen repository object

## 1.1 Branch and head

The latest branch carrying the `revision/` prefix and a Round-Forty-One name is

```text
revision/round41-referee-positive-closure-gpt56pro-2026-09-04
```

At the time of the review freeze it pointed to

```text
7be5768713ab4e4247c5e1538fd470c38edf57a7
```

with tree

```text
fc4f3a5a57f1033ed0f74c091fe120c4a83124eb.
```

The parent is

```text
8cf68a1810e4257f59da2737f0493fe4e595bd71.
```

The head is not a mathematical-source commit. It is a workflow/bootstrap commit.

## 1.2 Principal requested files are absent

Direct reads at the immutable SHA returned `404 Not Found` for each of the following:

```text
ROUND41_REVISION.tex
ROUND41_READY_FOR_REVIEW.md
ROUND41_REVIEW_INDEX.md
AUTHOR_RESPONSE_ROUND40.md
tools/verify_round41.py
round41/
```

Code search likewise found no committed `ROUND41_REVISION.tex` in the repository state available to the reviewer.

This is not a complaint about a missing convenience file. The absent files are exactly the files that the materialization workflows themselves declare necessary before verification and publication.

## 1.3 What is present

The branch contains, among other historical files:

- the frozen Round-Thirty-Nine source;
- the Round-Forty referee report;
- `tools/materialize_round41.py`;
- `tools/run_materialize_round41.py`;
- several Round-Forty-One materialization/verification workflows; and
- commits modifying the generator and the workflow strategy.

The wrapper says explicitly that it repairs one literal anchor in the materializer source and then executes the modified program in memory. The main materializer says explicitly that it will copy `round39/` to `round41/`, replace proof blocks, add new theorem text, write reviewer-facing ledgers, write a source manifest, and write `ROUND41_REVISION.tex`.

Those verbs are future operations. Their output is absent from the frozen tree.

## 1.4 Workflow status at the freeze

At the frozen head, GitHub recorded four Round-Forty-One workflow runs associated with the new push. The visible materialization and verification runs were queued and had not produced a source commit. Earlier materialization and verification attempts on preceding heads were recorded as failures or cancellations. No successful descendant commit containing the generated manuscript existed.

I do not infer from a queued or pre-execution failure that a mathematical test failed. The only justified conclusion is narrower:

> **There is no remotely materialized and verified Round-Forty-One source at the reviewed head.**

---

# 2. Confidential recommendation to the editor

## 2.1 Decision

**Return without review; administratively reject the present object.**

There is no stable article on which a referee can issue a correctness recommendation. The branch contains instructions for creating a later article, not the article itself.

A top-journal editor should not send the object to another referee. The author should first produce a conventional immutable submission consisting of the source, all included files, a buildable PDF, and a precise response to the preceding report.

## 2.2 This is not a “minor repository issue”

The missing source cannot be treated as a clerical omission because the proposed generator changes mathematical hypotheses and proofs. It intends to:

- replace asymptotic calibration density by a finite-prefix inequality;
- insert uniform force and duration bounds;
- alter the conditional-expectation sigma-field in the sign argument;
- replace the empirical-contrast proof;
- replace the filter Banach-space subsection;
- replace the Jacobi posterior theorem;
- add a new compact-class strong-law lemma;
- rewrite the introduction and claimed novelty;
- add references;
- remove repository-governance prose from the article; and
- add a new posterior-rate theorem.

Until those substitutions are executed and their exact output committed, neither the statements nor the proofs are part of the submission.

## 2.3 A later workflow success would create a new review object

The materialization workflow has write permission and is designed to push generated source back to the revision branch. If it later succeeds, the branch head will change. That future descendant must be reviewed under its own immutable commit SHA.

It would be methodologically indefensible to issue a theorem-level report on `7be5768...` and silently treat a later generated descendant as though it had already been reviewed.

---

# 3. Why source-generation code is not a manuscript

## 3.1 The exact theorem text is not frozen as an article

The generator contains large raw strings intended to replace sections of the Round-Thirty-Nine source. This does not establish that:

- every replacement anchor matches exactly;
- every replacement occurs once;
- the resulting TeX is syntactically valid;
- labels and references are unique;
- all hypotheses are propagated consistently to later theorems;
- the bibliography compiles;
- no stale Round-Thirty-Nine assertion survives elsewhere;
- the generated manifest hashes the intended bytes;
- the PDF corresponds to the generated source; or
- the final branch contains no further unreviewed source-writing step.

These are precisely the questions answered by materializing and freezing the actual output.

## 3.2 The wrapper changes the generator in memory

`tools/run_materialize_round41.py` does not simply invoke a frozen generator. It reads the generator text, replaces one literal substring in memory, and executes the modified code using `exec(compile(...))`.

Even if the operation is deterministic, the submitted mathematical object is now distributed across:

1. the Round-Thirty-Nine source;
2. the materializer source;
3. the wrapper's in-memory source rewrite;
4. the Python execution environment; and
5. the uncommitted generated output.

That is unacceptable as a journal submission format. Reproducibility is improved by scripts that verify committed source, not by scripts that manufacture the source after submission.

## 3.3 A claimed deterministic generator does not supply line-addressable proofs

A referee report must be able to identify an exact theorem and an exact proof passage. Here the relevant lines exist only as string literals inside a program. Their final location, surrounding context, numbering, labels, and interaction with copied material are not frozen.

The fact that one can imagine the output is no substitute for reading the output.

## 3.4 The branch is not immutable in practice

The revision branch is expressly designed to mutate when a workflow obtains a runner and write permission. During an active review, this creates a moving target. The reviewer must therefore ignore the branch name and freeze a SHA. Once frozen, the SHA contains no manuscript.

---

# 4. Disposition of the Round-Forty objections

The generator appears intended to answer the Round-Forty report. That intention is not closure.

| Round-Forty item | Proposed generator action | Status at frozen Round-Forty-One head |
|---|---|---|
| Delayed-calibration counterexample | Impose `N_cal(m) >= rho m-C_cal` for every finite prefix | **Open: generated source absent** |
| Common exploitation-force bound | Introduce a fixed `U` | **Open: generated source absent** |
| Common duration bounds | Introduce `tau_min,tau_max` and `underline tau` | **Open: generated source absent** |
| Duration/sign chronology | Make duration `F_{i-1}`-measurable before the fresh sign | **Open: generated source absent** |
| Incomplete Jacobi box | Declare finite `c_+` and `b_+` | **Open: generated source absent** |
| Invalid uncountable `L^2`-net step | Replace it by a finite `C([0,T])` sup-norm net | **Open: generated source absent** |
| Filter-jet measurability | Introduce deterministic separable spaces `E_j^0` | **Open: generated source absent** |
| Qualitative Jacobi consistency only | Add a closed-set posterior upper-rate theorem | **Not submitted** |
| Article/repository separation | Generate a new article wrapper and reviewer packet | **Not submitted** |
| Clean verification | Generate verification script, manifest and build record | **Not submitted** |

The correct ledger status for every item is therefore not `closed`, but

```text
proposed_in_generator_not_materialized
```

---

# 5. Limited provisional audit of the intended generated mathematics

This section is included only because the generator exposes enough proposed text to identify the intended direction. It is not a substitute for reviewing a generated manuscript.

## 5.1 Finite-prefix calibration is the right repair in principle

The proposed condition

\[
N_{\rm cal}(m)\ge \rho m-C_{\rm cal}
\qquad(1\le m\le n)
\]

would eliminate the exact delayed-calibration counterexample in the Round-Forty report, provided:

- the constants are common across the full triangular experiment class;
- the condition is imposed pathwise at every horizon;
- the six-slot window partition is unambiguous;
- the duration is fixed before the random sign; and
- all later theorems refer to precisely this class.

The generator also proposes the pathwise count

\[
W_n=\left\lfloor N_{\rm cal}(n)/6\right\rfloor
\ge \rho n/6-C_{\rm win}.
\]

That is the correct elementary arithmetic for complete windows.

None of this can be credited until the actual source is present and all inherited statements are checked for consistency.

## 5.2 The proposed empirical-contrast repair is plausible but requires the final context

The generator proposes a radial compact index set, bounded martingale differences, a deterministic finite net, Azuma–Hoeffding, and interpolation. This is the natural repair.

A full review would still need to check:

- the exact filtration to which each candidate field is adapted;
- whether every current action randomizer is included before the observation noise;
- uniform parameter derivatives of the entire feedback-forced trajectory;
- the dependence of constants on `U`, `tau_min`, `tau_max`, and the parameter box;
- whether the policy kernel remains parameter independent on null histories;
- whether the conditional field has the stated common Lipschitz constant; and
- whether all small-horizon exceptions are absorbed without changing the theorem's quantifiers.

Those checks require the final integrated manuscript, not fragments of a source generator.

## 5.3 The proposed supremum-norm strong law is directionally correct

The Round-Forty proof incorrectly moved from a fixed-function maximal inequality to an uncountable supremum over an `L^2` net ball. The proposed replacement uses compactness of the response family in `C([0,T])` and the deterministic interpolation inequality

\[
\left|\frac1n\sum_{i=1}^nS_i\xi_i(f-g)(t_{M_i})\right|
\le \|f-g\|_\infty\frac1n\sum_{i=1}^n|\xi_i|.
\]

That is the appropriate mechanism: one empirical first moment controls an entire sup-norm ball at once.

A final review would need to verify that the response image is indeed compact in the sup norm under the exact coefficient topology and that the same argument is used, without reintroducing an uncountable maximal step, in every later uniform likelihood assertion.

## 5.4 The proposed deterministic separable filter-jet range is a reasonable repair

The generator proposes to take the closed span of point and derivative evaluations inside the large dual `(C_b^{j+1})'`. Because the Hilbert state is separable and the jet-evaluation maps are norm-continuous when one more test derivative is available, such a closed span can be separable.

This is substantially better than saying merely that a random dual-valued map is measurable because its scalar evaluations are measurable.

The final proof would still have to establish:

- Bochner measurability of every signed derivative integrand;
- strong differentiability in the stated dual norm;
- a common deterministic range independent of data and prior;
- the exact tensor norms for mixed parameter derivatives;
- total-variation differentiability of arbitrary tilted Borel priors; and
- measurable parameter suprema.

Again, the proposed text is not the submitted text.

---

# 6. The intended Jacobi posterior “rate” is not the top-journal advance claimed

Even granting exact materialization and correctness, the generator's proposed strengthening does not establish a top-four result.

## 6.1 It is an upper bound, not an exact large-deviation principle

The proposed theorem has the form

\[
\limsup_{n\to\infty}\frac1n\log\Pi_n(F)
\le -\frac{a^2}{2\sigma^2}\inf_{\beta\in F}D(\beta,\beta_0)
\]

for closed sets `F`.

This is an upper large-deviation bound. It is not an “exact posterior rate” in the standard sense unless a matching lower bound on open sets is proved, together with the necessary exponential tightness or an equivalent complete LDP framework.

The proposed introduction and response use the word “exact” too aggressively.

## 6.2 Positivity by compactness is not quantitative inverse stability

For a finite coefficient block, the generator defines

\[
\kappa_J(\delta)=
\inf_{d_J(eta,eta_0)\ge\delta}D(eta,eta_0)
\]

and proves only that this number is positive by compactness and injectivity.

That argument supplies no usable estimate of:

- the dependence on depth `J`;
- the dependence on separation `delta`;
- deterioration as the sampling weights `omega_m` decay;
- dependence on the coefficient box;
- instability caused by analytic continuation;
- the number of observations needed to recover the `J`th coefficient; or
- minimax sharpness.

Calling this “quantitative coefficient recovery” is misleading. It is a nonconstructive positive separation constant.

## 6.3 The response metric can conceal severe ill-posedness

The metric

\[
D(eta,eta_0)=
\sum_m\omega_m\{h_eta(t_m)-h_{eta_0}(t_m)\}^2
\]

is tailored to the sampling distribution. Far coefficients affect short-time boundary data only through increasingly high-order propagation. Depending on the weights and time interval, `kappa_J(delta)` may decay catastrophically with `J`.

The proposed theorem does not quantify this phenomenon. The central inverse-problem difficulty is moved into an unnamed compactness modulus.

## 6.4 The physical-time cost is hidden

The experiment proposes a washout time

\[
w_i=w_*i.
\]

After `n` stages, washout alone costs order `n^2` physical time. An exponential rate in the stage count `n` corresponds only to a stretched-exponential scale in total elapsed time.

A mechanical identification paper should report both statistical and physical-time complexity. Otherwise the apparent rate substantially overstates the efficiency of the experiment.

## 6.5 The infinite-dimensional design is not adaptive in the hard sense

The diagnostic duration is drawn from a fixed countable distribution, the sign is independent, and an increasing washout deliberately erases the preceding feedback state. The arbitrary feedback segment is therefore largely irrelevant to identification.

This is a valid experimental design. It is not a theorem showing that an adaptive optimizing policy learns an infinite operator while controlling the system.

## 6.6 No infinite-dimensional uncertainty quantification is proved

The intended infinite-Jacobi conclusion is posterior concentration in a compact product topology plus a closed-set upper exponent in response distance. It does not provide:

- a nonparametric Bernstein–von Mises theorem;
- credible-set coverage;
- posterior covariance structure;
- uncertainty bands for coefficients or the spectral measure;
- contraction in operator norm;
- contraction in a weighted sequence norm;
- contraction of the Weyl function on a complex domain; or
- an optimal recovery rate.

The genuinely infinite-dimensional label is accurate, but the inferential theorem remains weak.

---

# 7. Top-four significance assessment of the intended paper

## 7.1 The homogeneous part remains regular finite-dimensional inference

The first model estimates five coefficients of a bounded, uniformly damped lattice from a collocated boundary input/output channel. The calibration design is engineered to contain prescribed short durations with independent signs at a positive finite-prefix frequency.

Once the finite response embedding and contrast are proved, the random-information quasi-Bernstein–von Mises theorem is a regular finite-dimensional Gaussian Laplace argument with a summable transient nuisance.

That may be useful in a specialist statistics, inverse-problems, or control venue. It is not a theorem of the scale expected by the four journals named in the request.

## 7.2 The inverse Jacobi recursion is classical

Recovering Jacobi coefficients from the boundary Weyl function by successive Schur complements is classical inverse spectral theory. The intended paper acknowledges this.

The new layer is a noisy repeated-probe likelihood and posterior concentration. In its proposed form, this is obtained from compactness, identifiability, a uniform strong law, and full prior support. The proof architecture is standard once the deterministic inverse map is available.

## 7.3 Combining two modest packages does not create a general breakthrough

The proposed article combines:

1. finite-dimensional adaptive Gaussian asymptotics under scheduled calibration; and
2. qualitative or response-metric posterior concentration for an infinite Jacobi sequence under increasing washouts.

The two parts share a physical vocabulary, but they do not yet produce a new general theory of adaptive inverse problems, a sharp stability theorem, or a new spectral phenomenon.

## 7.4 A result that could alter the assessment

A substantially stronger project might include one or more of:

- explicit depth-dependent inverse-stability bounds for Jacobi coefficients;
- minimax-optimal posterior contraction rates;
- recovery in operator norm or a physically meaningful weighted coefficient norm;
- simultaneous uncertainty quantification for an increasing coefficient block;
- an experiment with bounded total washout cost;
- learning under a genuinely reward-seeking or stabilizing policy rather than scheduled diagnostics;
- unknown damping at every site;
- unbounded wave/beam/PDE generators and unbounded observations;
- conservative or slowly mixing hidden dynamics; or
- a full posterior LDP with matching upper and lower bounds.

That would be a new research programme, not a repository materialization fix.

---

# 8. Theorem-by-theorem disposition at the frozen head

| Intended result | Frozen-source status | Referee disposition |
|---|---|---|
| Uniform nonlinear adaptive quasi-BvM | Only the Round-Thirty-Nine theorem and generator edits are present | **Not reviewable as Round Forty One** |
| Finite-prefix calibration lemma | Exists only as a raw string in the materializer | **Not submitted** |
| Revised empirical contrast | Exists only as replacement text in the materializer | **Not submitted** |
| Five-parameter lattice BvM under corrected class | No integrated Round-Forty-One source | **Not reviewable** |
| Deterministic separable filter-jet spaces | Exists only as replacement text in the materializer | **Not submitted** |
| Functional memory posterior | No integrated source showing all revised hypotheses | **Not reviewable** |
| Complete Jacobi reconstruction | Historical Round-Thirty-Nine source exists; claimed Round-Forty-One article does not | **No new review disposition** |
| Compact response-class strong law | Exists only as replacement text in the materializer | **Not submitted** |
| Closed-set Jacobi posterior upper rate | Exists only as replacement text in the materializer | **Not submitted; terminology overstated provisionally** |
| Strong product-topology consistency | Claimed as a future corollary | **Not submitted** |
| Round-Forty-One build and manifest | Files absent | **Unverified** |

---

# 9. Minimum requirements for a valid resubmission

The following are submission requirements, not optional stylistic suggestions.

1. **Commit the actual manuscript source.** `ROUND41_REVISION.tex` and every file it inputs must exist at the review SHA.

2. **Commit the reviewer packet.** Include the author response, review index, proof ledger, and precise theorem map as ordinary files.

3. **Freeze the branch.** Source-writing workflows must be disabled or converted to read-only verification before external review begins.

4. **Build from committed bytes.** The PDF must be generated from the exact frozen source, not from a workspace modified by a prior workflow step.

5. **Record a successful clean build.** The verification record must identify the immutable commit and source manifest.

6. **Do not rely on in-memory source rewrites.** Apply every correction directly to committed source.

7. **Preserve the generator only as provenance.** It may document how the revision was constructed, but it must not define the publication unit.

8. **State the statistical rate honestly.** Call a closed-set limsup result an upper bound, not an exact LDP.

9. **Quantify inverse stability.** Supply explicit or asymptotic information about `kappa_J(delta)` if claiming quantitative coefficient recovery.

10. **Report physical-time complexity.** Translate stage-count rates under linearly growing washout into elapsed-time rates.

11. **Separate theorem validity from ledger status.** A machine-readable `closed` field is not evidence that a proof is correct.

12. **Request a new review only after the head is stable.** The new request must identify the exact immutable SHA.

---

# 10. Verification and provenance assessment

## 10.1 No source manifest can certify absent files

Because the Round-Forty-One source manifest is absent, there is no list of final source bytes to compare against the claimed revision. A manifest generated later would describe a later object.

## 10.2 No verification script is present

The current workflow expects `tools/verify_round41.py` after materialization, but that file is absent at the frozen head. Consequently the verification command named by the workflow cannot be run against the reviewed tree.

## 10.3 Queued runs are not evidence

A queued workflow establishes only that GitHub accepted an execution request. It does not establish:

- source generation;
- successful tests;
- successful TeX compilation;
- artifact publication;
- source immutability; or
- mathematical correctness.

## 10.4 Historical local checks do not transfer automatically

Round-Thirty-Nine local algebra and build records concern Round-Thirty-Nine bytes. The Round-Forty-One generator proposes extensive replacements. Historical checks cannot certify a source tree that does not yet exist.

---

# 11. Final recommendation

The repository demonstrates substantial effort to automate a positive response to the Round-Forty report. The materializer appears to target the correct local defects, and several proposed proof mechanisms are more responsible than their Round-Thirty-Nine predecessors.

That effort has not produced a submitted manuscript at the frozen head.

The distinction is absolute:

- source-generation instructions are not source;
- queued workflows are not commits;
- raw-string theorem text is not an integrated article;
- a future branch mutation is not an immutable review object; and
- an author's intended proof is not a proof available to a referee.

Accordingly:

> **Return without review. Reject the present Round-Forty-One branch state as non-reviewable. Do not invite a top-four major revision on this object. A later fully materialized source must be treated as a new submission and reviewed from its own frozen commit.**

Even on the most charitable provisional reading of the generator, the intended mathematical package remains below the standard of *Annals of Mathematics*, *Inventiones Mathematicae*, *JAMS*, or *Acta Mathematica*. Its proposed infinite-Jacobi rate is only a closed-set upper bound in a response metric with a nonconstructive compactness modulus, while the finite-dimensional theorem remains regular Gaussian asymptotics under prescribed calibration.

A carefully materialized, corrected, split, and substantially reframed specialist submission may be worthwhile. The present branch is not that submission.
