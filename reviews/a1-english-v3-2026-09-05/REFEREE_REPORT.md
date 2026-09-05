# Independent referee report — A1, English revision 3.0

**Manuscript:** *A1: Realizable Mechanical Experiments, Path Selection, and Response — Positive polynomial readouts, exact finite-budget inference, and attainable adaptive control in a Lorentz laboratory*  
**Author named in the submission:** Qian Qi  
**Review date:** 5 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested general-mathematics-journal level in its present form.**

This is an independent AI-assisted referee-style assessment requested by the repository owner. It is not a report commissioned by, or an editorial decision of, any named journal. Rejection concerns the contribution demonstrated by this submission, not the possibility of developing the research program.

## 1. Exact submission and scope of this review

The reviewed branch is `revision/a1-english-v3-operational-closure-2026-09-05`, pinned at:

```
commit:         025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6
repository tree:7ccde192102a6a5fe6709d93bd2136d4273b375f
A1 source tree: ec09fa385c5fdcc5f2aece59a6b7f0806bfbb8ea
principal path:papers/A1-english-v3/main.tex
```

The preceding source-publication commit is `19fc74bcfcdad1e8b6daf28e6444929d423c542f`; the controlling English-v2 review is `40be02de7479712d866a575c4b0b9ec930699282`. The principal manuscript is now published as ordinary files. The missing-publication objection from the previous review is therefore **closed for the principal source**. This does not by itself verify a PDF build.

I read the complete current principal mathematical source: its main file, all seven numbered sections, both appendices, and bibliography. I read its response to the referee and proof/provenance maps, and directly checked the three revised companion sections on selection, response, and hybrid sensitivity. The companion's other historical mathematics is not represented here as a fresh 63-statement re-audit. In particular, this report does not certify all eleven papers or all historical branches.

The submission's ledger identifies 13 proof-bearing principal statements and reports a 22-page build. The 13 statements are audited individually in [CLAIM_AUDIT.md](CLAIM_AUDIT.md). Page numbers remain author-reported: I did not compile LaTeX, inspect a PDF, or rerun the author's 39 diagnostics. Instead, I executed a separate 20-check program, with the source and results supplied here. The unchanged reviewed A1 directory is preserved as the Git subtree [source/](source/); all source links below refer to that pinned copy.

## 2. Editorial judgment: a real improvement, but not yet the claimed level of mathematical significance

The revision does more than rename the old objects. It has a specified parameter-independent preparation, a computed observation kernel, a single gate class used consistently in inference and control, an explicit likelihood representation, a matching continuous-state lower bound, and a proof of attainment including zero-evidence boundary cases. The old criticism that the paper merely adjoined an all-tests predictor and a formal Bellman equation to an unrelated collision calculation is no longer an adequate description of this submission.

In particular, Theorem 4.3 is not a naive count of polynomial coefficients. Its open-family and coprime-factor argument supplies the missing lower-bound mechanism. Theorem 5.3 correctly controls normalized rare failures and the *probability-weighted* continuation value at zero evidence. These improvements deserve explicit credit.

Nevertheless, I do not find a sufficiently consequential central mathematical advance for the requested journals. The paper constructs an intentionally engineered positive cubic statistical experiment inside an ideal classical apparatus, and then exploits the algebra and compactness that this construction supplies. Most of the advertised consequences become short consequences of that algebra. The manuscript needs to identify and establish a result whose importance goes materially beyond the coherence of this particular construction.

This is a significance judgment, not a claim that a cited paper already contains the entire submitted theorem. The targeted literature examination below does not establish such an exact prior duplication. Nor am I demanding that a paper explicitly restricted to short trials must solve unrestricted long-time billiards. A substantial structural theorem within a finite-budget laboratory would be a legitimate alternative. The present result must be judged on the depth actually established, not on the difficulty of problems that its setup deliberately avoids.

Two local formulation defects remain: an omitted smooth-readout qualification in the principal version of A.3, and an overstatement of the intrinsic dimension of the gate body. Neither is a counterexample to the apparatus kernel or to the core positive-filter/Bellman construction. Repairing these sentences alone would not change the editorial recommendation.

## 3. Disposition of the preceding review

| Previous issue | Current disposition | Reason |
|---|---|---|
| M1: retained bias versus bare entropy | Closed in the inspected statements | Principal A.1 and companion Proposition 4.4 retain the objective `D(Q||P)-QB`; bare entropy is restricted appropriately. |
| M2: two density traces at a moving interface | Closed for the stated internal-interface formula | Principal A.2 and companion Theorem 12.2 retain both physical density traces. |
| M3: smooth preparation versus smooth dynamics | Substantially closed | Both versions state transported/weighted preparations with derivative envelopes and normalization. The separate readout qualification identified below must be synchronized. |
| S1: singular ideal record versus regular observed experiment | Correctly retained, not evaded | The ideal record still identifies the radius on collisions; the specified noisy detector is a different push-forward whose kernel is actually calculated. |
| Missing effective likelihood state and attained model-specific control | Substantively addressed | Theorems 4.1–4.3 and 5.1–5.3 are now proved for the same instrument. |
| Missing ordinary source publication | Closed for current principal source | The manuscript and all inputs are accessible at the pinned revision. Build and binary-delivery claims remain separate facts. |
| Top-journal significance | Still open; decisive editorial objection | The new mathematical content needs a sharper structural advance and a closer comparison with polynomial computation and Bayesian experiment theory. |

It would be unfair to count the first six rows again as unchanged failures. Conversely, a response document marking them resolved is not itself proof of the final row.

## 4. Mathematical audit of the new principal chain

### 4.1 Preparation and collision geometry

**Anchors:** [Section 2](source/sections/02_laboratory.tex), `eq:prep`, `eq:ambient-tube`, `prop:raw`.

The ambient preparation uses the fixed cell area `a0=sqrt(3)/2`, not the radius-dependent accessible area. An insertion failure has probability `pi R^2/a0` and consumes a cartridge. The allowed position mass is `(a0-pi R^2)/a0`. Independent unused cartridges retain their product preparation conditional on the observed history. These facts eliminate the previous danger of an uncharged, parameter-dependent equilibrium reset.

For `R in [0.45,0.47]`, different lifted disks are at least `0.06` apart. The time window is shorter than this separation. Convexity rules out an immediate return to the same disk; the distance estimate rules out a second disk. The backward collision tube therefore has both coverage and nonoverlap. At fixed laboratory velocity angle, the position Jacobian has magnitude `R cos(phi)`. Integrating its time, boundary-angle, and incidence-angle coordinates gives collision probability `2RT/a0` for an ambient attempt. Conditional on successful placement it gives `2RT/(a0-pi R^2)`, but that is a different conditional experiment and resource interpretation.

I find no error in this geometry or normalization. The argument uses separation and one-collision geometry; it does not extract a difficult consequence of chaotic long-orbit dynamics. The author now makes that limitation explicit, which is mathematically appropriate.

### 4.2 The detector and the exact attainable family

**Anchors:** Sections [2](source/sections/02_laboratory.tex) and [3](source/sections/03_attainability.tex), `eq:detector-map`, `eq:raw-kernel`, `thm:attainable`.

At impact, `|z|^2=R^2`. The inverse-CDF detector consequently gives, with respect to the stated reference measure, the three numerator densities

\[
\pi R^2,\qquad a_0-\pi R^2-2TR,\qquad
2TR\{1+\epsilon R^2\cos(y-\theta)\}.
\]

They normalize exactly and have the positive margins printed in Proposition 2.1. The uniform seed is prepared independently; it is not an additional unspecified random perturbation. The local pointer discussion is consistent with the declared ideal classical instrument, including its explicitly prepared pointer-momentum sheet. It is not a derivation of finite-energy or finite-precision laboratory resources, and the author does not claim otherwise.

For a prescribed mode, a common gate `g(x)` produces accepted density `g k_R` and failure mass `integral (1-g)k_R`. Necessity and sufficiency hold within this expressly defined comparator class. A gate depending on the unknown radius is correctly excluded. Both the placement-failure symbol and the censoring symbol are charged and retained. Fresh-cartridge pasting is sufficient to justify adaptive composition; mixing of a single billiard orbit is neither necessary nor used.

This is a valid exact characterization of the declared class. Its force should not be confused with characterizing all physically possible interventions on a billiard.

### 4.3 Positive likelihood representation and degree elevation

**Anchor:** [Section 4](source/sections/04_positive_filter.tex), `thm:filter`, `thm:general`.

The degree-three Bernstein representations of `R`, `R^2`, and `R^3` are correct. The inequality `d_j <= u^2 r_j` gives positivity even when the cosine term is negative. Failure coefficients are integrals of positive raw coefficients against `1-g`, so negative coefficients in the power basis do not imply a negative likelihood.

The product identity

\[
B_i^d B_j^3=
\frac{\binom di\binom3j}{\binom{d+3}{i+j}}B_{i+j}^{d+3}
\]

gives exactly the stated update. Dividing all coefficients by their sum removes only a parameter-independent scalar. Under a uniform prior, `(d+1)B_i^d` is the beta density with parameters `(i+1,d-i+1)`, and the normalized coefficient vector really does give the stated mixture weights. The claimed linear per-update arithmetic count is appropriate **given the one-step coefficients**; it does not include evaluating arbitrary gate integrals or solving the control problem.

The uniform degree-elevation estimate follows from the without-replacement/with-replacement coupling with collision probability at most `j(j-1)/(2m)`. Uniform coefficient bounds and a uniform positive lower bound permit a common degree. The rational denominator is retained at every step. These arguments appear sound.

### 4.4 The lower bound is genuine, but its quantifiers matter

**Anchor:** Section 4, `thm:dimension`.

For a fixed positive `T` and `epsilon`, the failure polynomial has power coefficients

\[
a_0(1-m_0),\quad b(m_0-m_1),\quad
\pi(m_0-m_\partial),\quad -b\epsilon m_2,
\qquad b=2T.
\]

The map from the four moments to these four coefficients is invertible. Small sinusoidal gate perturbations around `1/2` therefore produce an open family of positive cubics. For pairwise coprime cubic factors `F_i`, the kernel of the product differential consists exactly of `delta F_i=lambda_i F_i` with `sum lambda_i=0`. The rank is consequently `3n+1`; normalization removes one dimension. A local section and invariance of domain give the advertised continuous encoding lower bound.

I find this proof persuasive. It is stronger than a formal coefficient count and should be preserved. Its conclusion concerns exact likelihood curves across known command histories, not the realized histories of every fixed controller, not discontinuous encodings, not approximate inference, and not a point-mass prior. The full-support qualification for the posterior version is essential and is present.

The same proof works for an open family of degree-`q` positive factors and gives dimension `qn`. Thus the source of the dimension growth is a general polynomial-product geometry, rather than a billiard-specific memory mechanism. This observation is relevant to significance, not an objection to correctness.

### 4.5 Moment-body optimization, representatives, and boundary gates

**Anchor:** [Section 5](source/sections/05_control.tex), `lem:body`, `thm:control`, `thm:boundary`.

The weak-star compact order interval of gates is metrizable here because the reference measure has separable `L^1`. Integration against the four likelihood-moment functions and the continuation integrand is continuous. The support formula is the pointwise maximization of a linear functional over an interval.

The manuscript does not simply evaluate an `L^infinity` equivalence class at an observed point. The dyadic conditional-average construction provides a jointly Borel representative. Its compact-fiber selection argument has the needed closed-graph and compact-domain properties. The accepted posterior is independent of the positive scalar gate value; the failure posterior depends on its four moments. These facts make the displayed Bellman objective jointly continuous for a positive acceptance floor.

The removal of that floor is handled correctly. If `s(g)=integral(1-g)dnu`, each nonzero failure factor has coefficients between `h_* s(g)` and `H_* s(g)`. Normalization therefore retains a strictly positive margin independent of how rare failure is. At zero evidence the posterior need not converge, but the bounded continuation value multiplied by its failure probability converges to zero. The proof uses continuity of this weighted term, not a false everywhere-continuous posterior map.

The finite-menu approximation also uses the correct estimate: uniform approximation of the compact family of integrands, rather than uniform `L^1` approximation of every measurable gate. Backward propagation is legitimate at a fixed budget. I find no counterexample to the attained recursion in its stated compact, bounded, observable-reward setting.

### 4.6 Response, Fisher information, and stability

**Anchors:** Sections [6](source/sections/06_response.tex) and [7](source/sections/07_stability.tex).

For a fixed parameter-independent adaptive controller, every command at a fixed realized history is the same when the physical radius is varied. Its chronological density is therefore a product of polynomial conditional densities. The finite reference measure and bounded coefficient functions justify strong variation differentiation, including exact vanishing beyond degree `3N`. The common-support relative-derivative argument justifies quadratic-mean differentiability also for endpoint gates. Conditional scores are centered martingale differences, giving the information sum without treating an adaptive design as fixed after the fact.

The mark-information formula and the flags-plus-mark decomposition agree with direct differentiation. Censoring contributes its conditional mean score rather than zero. The ideal collision record remains a different, non-equivalent statistical experiment; infinite relative entropy there does not contradict the regularity proved here.

The posterior error and value-stability estimates are conservative but valid under the stated relative-error premises. The manuscript correctly declines to infer that every floating-point implementation meets those premises or that a bound between two prior values automatically controls an arbitrary recursively rounded controller. These qualifications should not be removed in a revision.

## 5. Local statement corrections required

### M1. Principal Theorem A.3 omits the smooth-readout qualification present in the companion

**Severity:** Local statement-scope defect; not a refutation of Theorem 1.1.  
**Anchors:** [principal Appendix A](source/sections/A_scope_repairs.tex), `thm:transport-prep`; [companion Section 13](source/foundations/sections/13_hybrid.tex), `thm:chamber`.

The principal chamber assumptions specify smooth flights, guards, and resets. Its first conclusion then includes the *terminal report* among the quantities that are jointly `C^r`. No smoothness of that report map is stated there. The companion instead first asserts regularity of the terminal **state** and then explicitly restricts the report to a fixed smooth finite-dimensional map. These are not equivalent formulations.

A counterexample to the unqualified principal clause has no collisions or events at all. On a common compact neighborhood, take

\[
\dot x=a,\qquad x(0)=0,\qquad T=1,\qquad |a|<1/4.
\]

The preparation is fixed, the flow is smooth, and the itinerary is the empty regular itinerary. Use the fixed Borel terminal readout `Y=1_{x(T)>0}`. Then

\[
Y_a=\mathbf 1_{\{a>0\}},
\]

which is not even continuous at zero. Nothing in smooth dynamics makes an arbitrary measurable observation smooth.

This example does **not** satisfy an additional hypothesis requiring differentiable report jets; it is directed at the earlier unqualified report-regularity assertion, not at a version that already assumes those jets. It also does not challenge the polynomial detector response, which is proved independently by its explicit integrated kernel.

**Required correction:** Synchronize the principal statement with the companion: prove regularity of terminal states, and obtain regularity of reports only for a specified jointly `C^r` readout with the required uniform bounds. State a fixed smooth reporting manifold/embedding when invoking `H^{-s}`. The transported-preparation repair itself should be retained.

### M2. The gate body has five coordinates, not necessarily intrinsic dimension five

**Severity:** Minor dimensional overstatement; the optimization formula remains valid.  
**Anchor:** [Section 5](source/sections/05_control.tex), `eq:gate-body`, and the abstract's dimension language.

Choose an admissible problem with `lambda=0` and terminal payoff `G=1`. Then every continuation value is one, and

\[
w_{c,a}(x)=\bar k_c^a(x).
\]

Writing `M_j=E_{pi_c}R^j`, this function belongs to the span of the four components of `v_a`:

\[
w_{c,a}=A\cdot v_a,\quad
A=\frac1{a_0}\bigl(\pi M_2,
 a_0-\pi M_2-bM_1,\ bM_1,\ b\epsilon M_3\bigr).
\]

Every feasible point consequently satisfies `u=A dot m`. The body lies in a four-dimensional hyperplane of `R^5`; under the nondegenerate gate interval the four moment directions themselves can vary. The manuscript proves an exact **five-coordinate representation**, or intrinsic dimension **at most five**, not a uniformly five-dimensional body for every allowed reward and state.

**Required correction:** Use “a compact moment body in `R^5`” or “at most five-dimensional.” Keep separate the genuinely sharp `3n` likelihood-state theorem, whose nondegeneracy hypotheses and open-set proof do establish intrinsic dimension.

For A.2, a further notation cleanup would help: label the dotted bulk derivatives as Eulerian derivatives at fixed spatial position, as its proof uses, and append an explicit external-boundary flux if moving outer boundaries are intended. I do not count this clarification as a new counterexample to the fixed-outer-domain theorem.

## 6. Main contribution objections

### E1. The cubic likelihood is engineered through an exact internal radius measurement

The detector is not logically circular: its program receives a physical impact coordinate, not a parameter supplied by an oracle. Within the declared ideal apparatus this is legal. But on the collision shell that coordinate already satisfies `|z|=R`. The apparatus then deliberately garbles this exact geometric information into a selected smooth density.

More generally, let `q(r,y)>0` be any smooth normalized circle density on the radius interval. Define

\[
F_r(y)=\frac1{2\pi}\int_0^y q(r,v)\,dv.
\]

Using `F_{|z|}^{-1}(U)` at collision produces the hit density

\[
\frac{2TR}{a_0}q(R,y).
\]

The paper's cubic family results from the particular firmware choice `q(r,y)=1+epsilon r^2 cos(y-theta)`. The polynomial closure is therefore not forced by the mechanics. It is a designed property of an admissible observation channel.

That construction can still be mathematically useful. What is missing is an explanation, supported by a stronger theorem, of why this particular engineered closure is a major result rather than a convenient exactly solvable statistical model. A structural classification or a quantitatively robust class theorem would answer this better than adding further interpretations to the same cubic formula. No objection here requires abandoning the ideal apparatus or claiming that the broader program is impossible.

### E2. The closest comparison is polynomial likelihood algebra, not merely predictive representations

The bibliography discusses predictive states but does not adequately place the central computational device in the literature on Bernstein polynomial arithmetic. Farouki and Rajan [R1] explicitly develop arithmetic and other algebraic procedures directly in Bernstein form. A positive convolution update should be compared with that established algebra; it is not a new operation merely because the polynomial is a likelihood.

The beta-mixture identity is also a familiar connection: Petrone and Wasserman's primary technical report [R2] discusses Bernstein densities as mixtures of known beta densities in Bayesian nonparametric inference. Their problem is not the present finite-budget static-radius filter, so this is **not** a claim that their result subsumes Theorem 4.1. It does show why the identity alone cannot carry the novelty burden.

The more promising contribution is the attainable open family and sharp encoding lower bound. The paper should isolate the general degree-`q` statement, specify the topology of admissible continuous encodings, and explain which nontrivial model constraints permit or prevent the full-rank family. A mere replacement of `3` by `q`, however, is not by itself a sufficient strengthening: the current coprime-factor proof already makes that extension nearly immediate.

### E3. The control result proves existence and reduction, but little specific control structure

The gate support formula is a finite-dimensional vector-integral construction related to the moment-body/lift-zonoid background already cited [R3]. Posterior-state optimality and continuity are central themes of partially observed control [R4]. The latter reference concerns expected total costs and is not a plug-in theorem for the paper's multiplicative payoff; I am not asserting an exact theorem identity. The present proof appropriately verifies its own model-specific conditions.

Even so, after the kernel and compact positive state are available, most of Section 5 follows from compact maximization and a representative/selection argument. The “fifth coordinate” is the integral of the current continuation objective. It is not a fixed five-dimensional description of every future instrument or a solved continuous optimization problem. The author explicitly acknowledges this, but that acknowledgement does not supply additional depth.

The manuscript should deliver a genuine policy-structure or quantitative performance result within this model. For example, it could characterize optimal gate boundaries for a specified nontrivial payoff, certify a strictly positive adaptive advantage over a defined nonadaptive class, or quantify finite implementation complexity under stated regularity. The endpoint-gate result below is already available from the current assumptions and illustrates how much more specific the control theorem can become.

## 7. A positive strengthening available now: optimal endpoint gates

This subsection is a **referee-derived consequence**, not a claim that the submitted manuscript already proves it and not an assertion of literature priority.

**Claim.** Under the printed reward assumptions, an optimal Borel feedback controller can be chosen with gates taking only the two values `eta` and `1-eta`. For the full interval these are deterministic accept/reject gates `0` and `1`. No nonlinear extra cost depending on the gate itself is being added.

**Proof.** Fix a resource level, current posterior, and mode. Define the positive homogeneous continuation functional on nonnegative finite parameter measures by

\[
\mathcal W(\zeta)=\sup_\Pi\int L_\Pi(R)\,\zeta(dR),
\]

where `Pi` ranges over the common admissible remaining policies and terminal decisions, and `L_Pi(R)` is their bounded nonnegative conditional payoff. This is a supremum of linear functionals and hence is convex. If `zeta` has positive mass, it equals that mass times the normalized-posterior continuation value; at zero it equals zero.

For a gate `g`, the unnormalized parameter measure after censoring is

\[
\zeta_g(dR)=f_R^{a,g}\pi_c(dR).
\]

It is affine in `g`. The accepted continuation term is linear in `g`, because its posterior update is independent of a nonzero accepted gate factor. Thus the complete command objective `Q(g)` in Theorem 5.2 is convex in `g`. Its weak-star continuity, including zero evidence, is precisely what Theorems 5.2–5.3 establish.

Put `h=(g-eta)/(1-2eta)` and, for `0<=t<1`, define

\[
g_t=\eta+(1-2\eta)\mathbf1_{\{h>t\}}.
\]

The layer-cake identity gives `g=integral_0^1 g_t dt` in the weak-star sense. Convexity yields

\[
Q(g)\le\int_0^1 Q(g_t)\,dt.
\]

Take an optimal gate `g*` for the fixed mode, with value `M`. Every `Q(g*_t)<=M`, so equality of the integral forces `Q(g*_t)=M` for almost every `t`. Moreover `g*_t` is right-continuous in the weak-star topology by dominated convergence of its level indicators. Consequently `Q(g*_t)` is right-continuous. A value strictly below `M` at any `t<1` would persist on a right interval of positive length, contradicting the almost-everywhere equality. Hence every threshold `t<1`, in particular `t=1/2`, is optimal.

Finally, the manuscript already supplies an optimal mode/gate selection with a jointly Borel representative `g*(c,x)`. Replacing this representative by

\[
\eta+(1-2\eta)\mathbf1_{\{g^*(c,x)>1/2\}}
\]

is jointly Borel and preserves the fixed-mode optimal command value. Backward induction supplies an optimal endpoint-gate feedback controller. This argument does not imply that its acceptance set is a finite union of intervals. The existing finite-lookup approximation remains useful for that distinct issue. **End of proof.**

This theorem is a concrete improvement over an unspecified optimum over all fractional gates. It does not by itself settle top-journal significance, but it is a constructive route available without weakening the paper's positive objective.

## 8. A robustness diagnostic, and the distinction from coefficient roundoff

### S1. Small smooth detector changes need not preserve exact cubic closure

Change only the collision mark amplitude to

\[
c_\delta(r)=\epsilon r^2+\delta\sin r,
\]

with nonzero `delta` small enough that `|c_delta(r)|<1` throughout the interval. The same measured-coordinate inverse-CDF construction implements this smooth positive detector. Its changed hit numerator contains

\[
2T\delta R\sin R\cos(y-\theta).
\]

The fourth radius derivative of the new term is

\[
2T\delta\{R\sin R-4\cos R\}\cos(y-\theta),
\]

which is not identically zero. Exact cubic closure and the degree-three derivative cutoff therefore fail for this modified detector even after one cartridge.

This is **not a counterexample to Proposition 2.1 or Theorem 6.1**: those theorems specify the original detector. It shows that smooth physical realizability and strict positivity alone do not imply their exact algebra. The coefficient-roundoff analysis in Section 7 does not address this change of model.

### A finite-budget model-error certificate

There is also a positive statement. Suppose two apparatus families on the same report space satisfy the uniform one-step bound

\[
\sup_{R,a,g}\operatorname{TV}
 (K_R^{a,g},\widetilde K_R^{a,g})\le\varepsilon_0.
\]

For any common fixed adaptive policy, chronological telescoping gives path distance at most `min(1,N epsilon_0)`. Equivalently, couple the experiments while their observed histories agree: they then choose the same command, and each next step has mismatch probability at most `epsilon_0`. A common censoring channel cannot increase raw total variation. The same bound holds for the joint parameter/history law under a common prior.

With the paper's unchanged bounded payoff, set

\[
m_N=G_-e^{-N|\lambda|B},\qquad M_N=G_+e^{N|\lambda|B}.
\]

Integration of a function in `[m_N,M_N]` gives, uniformly over policies and hence over their common supremum,

\[
|V-\widetilde V|\le
(M_N-m_N)\min\{1,N\varepsilon_0\}.
\]

A policy optimal for the approximate apparatus has regret at most twice this bound in the true apparatus. This is a comparison of complete policy experiments; it does not condition on a rare history and claim a uniform posterior estimate there.

For the particular amplitude perturbation above, the exact raw one-step distance is

\[
\operatorname{TV}(K_R^a,\widetilde K_R^a)
=\frac{2TR\,|\delta\sin R|}{a_0\pi},
\]

because the mean of `|cos y|` over the circle is `2/pi`. Thus a common fixed-budget implementation can be stable in value even though exact polynomial closure is destroyed. This elementary certificate distinguishes a physical model error from arithmetic roundoff and offers a precise starting point for a stronger approximation theorem.

## 9. What a further revision must accomplish

First, correct M1 and M2 without altering the valid preparation, failure, and common-support qualifications. Keep the already successful M1–M3 repairs from the preceding review; the new labels in this report are not a claim that those previous errors survived unchanged.

Second, separate three levels of claim: the general positive-polynomial experiment algebra; the sufficient conditions producing a full-dimensional attainable failure family; and the Lorentz apparatus as one verified realization. Supply a theorem-by-theorem comparison with the closest work, especially Bernstein arithmetic and Bayesian representations. Do not replace a novelty argument with another count of theorems, proof pages, or passing checks.

Third, prove a result that materially deepens the model: a nontrivial structural class/robustness theorem, or a sharp policy/performance theorem with a genuinely informative controlled example. The endpoint-gate argument and the model-error calculation above are concrete starting points, not a list of unrelated impossible demands. No particular long-time billiard theorem is made a mandatory prerequisite. However, merely appending these elementary consequences to the present exposition would not automatically meet the requested journal standard; the central significance still needs to be demonstrated.

## 10. Executed diagnostics and reproducibility limits

The accompanying [referee_checks.py](referee_checks.py) ran **20/20 checks successfully**; [DIAGNOSTICS.json](DIAGNOSTICS.json) records every check, its type, and numerical values where relevant. The checks include exact Bernstein identities and failure coefficients, finite coprime differential ranks for `n=1,...,4`, rare-failure normalization, finite moment-body and control analogues, the two scope diagnostics, direct Fisher-information quadrature, and the smooth-detector perturbation calculation.

These are not 20 proofs of the manuscript. The all-budget lower bound is assessed through its coprime/submersion proof, not inferred from four ranks. The continuous Bellman theorem is assessed through compactness, selection, and induction, not inferred from a finite grid. The geometric coverage argument is read analytically, not certified by a sampled Jacobian.

The first local run had one test-harness type-conversion error when converting a SymPy Boolean directly to an integer. Converting it through Python `bool` fixed the harness; the final complete run passed. This was not a manuscript failure. The final script's SHA-256 is recorded in the receipt. No author test program was imported or rerun, and no LaTeX/PDF verification was performed. The author's reported 39 passing checks and 22 pages remain attributed to the submission, not presented as independent execution results.

The report, claim audit, script, and receipt are additions on a new review branch. The reviewed source subtree is preserved by its exact Git tree identity. Neither the manuscript nor the revision or main branch needs modification to publish this review.

## 11. Targeted primary-source comparisons

The following primary pages/abstracts were inspected for the comparisons used here. This was not an exhaustive priority search or a full proof audit of these external papers.

**[R1]** R. T. Farouki and V. T. Rajan, *Algorithms for polynomials in Bernstein form* (1988). [IBM Research primary publication record](https://research.ibm.com/publications/algorithms-for-polynomials-in-bernstein-form). Relevant to existing Bernstein arithmetic and the need to distinguish positive operations from a universal numerical-conditioning guarantee.

**[R2]** S. Petrone and L. Wasserman, *Consistency of Bernstein Polynomial Posteriors*, Carnegie Mellon technical report 708. [Primary author/institution abstract](https://www.stat.cmu.edu/tr/tr708/tr708.html). Relevant to the established Bernstein/beta-mixture connection, not an asserted prior proof of the present exact controlled-radius filter.

**[R3]** A. M. Kulik and T. D. Tymoshkevych, *Lift zonoid and barycentric representation on a Banach space with a cylinder measure*, arXiv:1211.2927. [Primary preprint record](https://arxiv.org/abs/1211.2927). Context for vector-integral/moment-body geometry; the support formula used in this review is also checked directly.

**[R4]** E. A. Feinberg, P. O. Kasyanov, and M. Z. Zgurovsky, *Partially Observable Total-Cost Markov Decision Processes with Weakly Continuous Transition Probabilities*, arXiv:1401.2168v2. [Primary preprint record](https://arxiv.org/abs/1401.2168). Context for posterior-state continuity, optimality equations, and policy existence; its expected-total-cost criterion is distinguished from the manuscript's multiplicative payoff.

## Final recommendation

**Reject at the requested four-journal level, while recognizing substantial mathematical improvement over English v2.** The revised principal apparatus/filter/control chain appears largely correct under its explicit ideal-model assumptions, with the local qualifications identified above. The decisive unresolved issue is the depth and significance of the central contribution, not a fabricated failure of the cubic kernel, an uncorrected rejection-record error, or an asserted impossibility of further progress.
