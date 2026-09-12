# Independent referee-style report on A2 v33

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/a2-v33-finite-experiment-integration-top4-2026-09-13`  
**Immutable submission:** `b577cffcb3ca5597cb4905269bea9de3bd4ead38`  
**Submission tree:** `425e794b942e4da497e51c0003fb98748e0019a9`  
**Previous review commit:** `8b7643b6e8fc3e07d85bf1452e6d4838c3222a0b`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v33-external-harsh-top4-2026-09-13`  
**Report date:** September 13, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the requested standards of Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned journal report, an editorial decision, or a claim of journal affiliation. The assessment is independent of the author's revision claims; it does not represent an additional human referee. Source keys below are resolved in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). References are to immutable source labels, not to uninspected PDF page numbers.

## Recommendation and principal findings

**Major revision of the assembled submission; no acceptance recommendation in its present state.** The mathematical increment in v33 survives the checks performed here. In particular, the finite-likelihood comparison is a genuine proof with common kernels and the correct normalization hypothesis, not a new name for likelihood convergence. The previous M1–M3 requests have been addressed. The compact local Gaussian conclusions, E1, remain closed at their stated observation level. However, the current submission identity has regressed, I1, and complete native submission verification, C2, remains unresolved. A short local-alternative moment calculation should also be made explicit, R1 below.

**No fatal mathematical counterexample to a stated theorem was established in this round.** That is not a certification of the entire article. I examined the revised statistical arguments and selected substantial inherited modules, including the two-sided Poisson reconstruction, finite-signature matching, orientation equivariance, and the compact global-estimation argument. I did not freshly rederive every finite-bridge foundation, nonlinear half-line estimate, physical calibration theorem, companion proof, or active appendix. Nor did I compile or inspect a complete native manuscript PDF. Earlier favorable module assessments are not cumulative substitutes for such a review.

| Issue | Current disposition | Reason |
|---|---|---|
| E1: compact local convergence | Remains closed for the stated local models | Finite likelihood comparison, uniform Hellinger modulus, finite-net argument and product comparisons are distinguished and supplied |
| M1: logical wording and integration | Closed | The fixed-window theorem now says “In particular” and explicitly points to the compact conclusion; the introduction and vector chapter agree |
| M2: retained observation | Closed | The count theorem now specifies laboratory transverse endpoint pairs and explicitly excludes normal coordinates, residual time and intermediate collisions |
| M3: finite-experiment theorem | Closed | `lem:v33-finite-likelihood` states and proves the result actually used, including normalization and both kernels |
| I1: submission identity | Reopened as a delivery inconsistency | Native main identifies v33, while both principal README entries still identify v32 and earlier ancestry |
| C2: complete native submission | Open; submission-verification blocker | No current complete build evidence was located; the v33 branch query returned no Actions runs, and the latest queried v32 attempt still failed without executed steps or artifacts |
| R1: alternative-mean control | Minor proof clarification, not a new fatal gap | Make the bounded local-alternative mean explicit before applying the fourth-moment formula |

The required response is narrow: complete and accurately identify this submission, supply verifiable native products, and close R1 in place. Another expansion of the theorem list is not a response to these requests. No arbitrary deletion of mathematical content or weakening of the established compact conclusions is requested.

## 1. What v33 actually changes

The authenticated comparison with the preceding review commit is one commit ahead, zero behind, and lists twelve changed paths. Five active manuscript files change: the main, introduction, vector-information chapter, fixed-window chapter and count–endpoint chapter. The other seven additions preserve previous entries or sources. There is no deleted file. The v32 compact-experiment section itself is unchanged. Thus this is primarily a proof-integration revision, not a new proof of the entire geometric programme. [S1–S8]

The new finite-likelihood lemma is the substantive addition. The fixed-window wording, introduction and count observation map implement the preceding referee's specific requests. Credit should be given for those changes: it would be incorrect to repeat the previous M1–M3 objections as though they had been ignored. Conversely, copying a README to a historical filename does not update the active README. Both active entries still direct the reader to the v32 branch, older source identity, and v31 response chain. [S2–S8, S14]

The version date in the manuscript is September 13, 2026. GitHub records the reviewed commit at September 12, 2026, 16:52:29 UTC. Those are different facts; the manuscript date must not be used as the commit timestamp. [S1, S2]

## 2. The new finite-likelihood proof is valid at its stated scope

### 2.1 Normalization, not weak convergence alone, controls the tails

In `lem:v33-finite-likelihood`, let the likelihood-vector laws under the references be mu_n and mu. Each coordinate is nonnegative and has mean one both before and after passage to the limit. For every A,

\[
 \int(x_i-A)_+\,d\mu_n
 =1-\int(x_i\wedge A)\,d\mu_n
 \longrightarrow
 1-\int(x_i\wedge A)\,d\mu.
\]

The truncation function is bounded and continuous. Combining this identity with the elementary tail inequality at threshold 2A proves coordinatewise uniform integrability, and hence uniform integrability of the finite-dimensional l1 norm. Finitely many initial indices do not obstruct that argument. The manuscript is entitled to derive uniform integrability rather than impose it as an additional assumption. [S5]

The normalization is indispensable. Under a reference with P(A_n)=1/n, take L_n=n times the indicator of A_n. Every prelimit mean is one and L_n converges in distribution to zero, but the limiting mean is zero. The alternative concentrated on A_n is at total-variation distance 1-1/n from the reference. A conclusion obtained by ignoring the lost mean would be wrong. This example tests a hypothesis of the new lemma; it is not a counterexample to it. The Gaussian likelihood coordinates used in v33 have mean one, including when the information matrix is singular. [S5; independent calculation]

### 2.2 The comparison kernels do not receive the parameter

Weak convergence together with the preceding first-moment control yields couplings pi_n of the two likelihood-vector distributions such that

\[
 \int\|x-y\|_1\,d\pi_n(x,y)\longrightarrow0.
\]

The finite-rectangle proof given in the manuscript is adequate: match the common rectangle masses, bound unmatched mass inside the fixed cube, and control the complement through uniform integrability. The cube and partition boundaries can be chosen null for the limiting measure, also relative to the nonnegative orthant. This avoids assuming total-variation convergence of the likelihood-vector distributions themselves. [S5]

The likelihood statistic is exactly sufficient for a finite dominated experiment. A regular conditional distribution under the reference reconstructs the original observation, and multiplication by a likelihood coordinate reconstructs the corresponding alternative. Standard Borelness is the relevant hypothesis. Disintegrating the same coupling in each direction then gives

\[
 \|K_n(x_i\mu_n)-y_i\mu\|_{\rm TV}
 \le \frac12\int|x_i-y_i|\,d\pi_n.
\]

The factor one half agrees with the manuscript's convention that total variation is the supremum over events. The same kernel works at every index, including the reference; reversing the disintegration gives the other deficiency. There is no parameter-specific simulator hidden in this construction. [S5]

The moving-support application first uses the reference-dominated common-collar representative. It does not manufacture a reference likelihood on observations lying outside the original reference support. Adjoining the reference to a finite parameter set before restriction is legitimate. The count application uses genuinely common-support discrete waiting laws. These are the correct two settings for the lemma. **M3 is closed.** [S5, S7]

### 2.3 Finite and compact convergence remain separate steps

`lem:v32-finite-net` still supplies the necessary additional argument. A single kernel selected for a finite r-net is applied throughout the experiment; a nearby net point is used only to bound its error. The resulting inequality is

\[
 \Delta(\mathsf E_n,\mathsf E)
 \le \Delta(\mathsf E_n|_F,\mathsf E|_F)
       +\omega_n(r)+\omega(r).
\]

One first sends n to infinity for a fixed finite net and then sends r to zero. The moving-boundary estimate gives the required product modulus of order s times the square root of 1+log(1/s). The Gaussian modulus is evaluated on the identifiable range and does not invert the singular information matrix on its kernel. [S5, S6]

The distinction is real. On K consisting of zero and 1/m, let the nth experiment output one only at parameter 1/n and zero otherwise. Each fixed finite restriction is eventually trivial, but its distance to the one-point experiment on all of K is one half. A reverse kernel must approximate two distinct point masses with one distribution. The manuscript's uniform modulus excludes this example. It would be wrong to replace the compact argument by the new finite lemma alone; v33 does not do so. [Independent calculation; S6]

The fixed-window theorem now uses implication rather than false equivalence and points to `cor:v32-compact-fixed-window`. The introduction and the vector chapter's terminology are consistent with that structure. **M1 is closed and E1 remains closed at this local scalar-output scope.** This supplies neither an unbounded-parameter equivalence theorem nor a Gaussian experiment for the noiseless planar position record. [S4–S8]

## 3. The count–endpoint product has the right error budgets

The local coordinates separate the fast hyperbolic displacement from the tangent space to a level set of gamma:

\[
 \eta_n=(j_n\sqrt{k_n})^{-1},\quad
 g=g_0+\delta_na/j_n,\quad
 \vartheta=\eta_nbv_\gamma+\delta_nh,
 \qquad D\gamma(h)=0.
\]

The remainder after the success log-ratio term -b/sqrt(k_n) is bounded by

\[
 C_K(\delta_n+\eta_n+j_n\delta_n^2
                  +j_n\delta_n\eta_n+j_n\eta_n^2).
\]

Every term is negligible after multiplication by sqrt(k_n) under the displayed rate assumptions. In particular, the quadratic slow drift and mixed fast–slow terms have not been silently suppressed. [S7]

The negative-binomial score for log p, its variance, and the displayed second and third likelihood derivatives are correct. A separate exact check gives the geometric affinity

\[
 A(G_p,G_q)=\frac{\sqrt{pq}}
                   {1-\sqrt{(1-p)(1-q)}}.
\]

For a total wait stopped at k successes the affinity is exactly the kth power of this expression, by the negative-binomial generating function. This agrees with the Hellinger comparison in the manuscript and confirms that no Poisson approximation is required for the waiting-time experiment. The accompanying diagnostic evaluates a rational example, not an asymptotic substitute for the proof. [S7; independent calculation]

The important order of operations is respected. First remove the caps; waiting times and successful marks then factor exactly. Replace the waiting law by its b-only ideal family. Remove the fast displacement from the endpoint marks using

\[
 k_n\eta_n^2\log(e/\eta_n)
 =\frac{1+\log(j_n\sqrt{k_n})}{j_n^2}\longrightarrow0.
\]

Combine the compact kernels on the coordinate projections and restrict their product to the actual compact parameter set. Restore the cap error only afterward. Finally add the success-weighted finite-bridge comparison. This does not assume that a compact parameter set is a Cartesian product, or that successful marks remain iid after conditioning on completion before a cap. [S6–S8]

The revised theorem explicitly retains the laboratory transverse pairs (y_first,y_last), not the full planar endpoints. Normal coordinates, residual time and intermediate collisions are excluded in the statement itself. Thus the richer position experiment's singular support is not an objection to this theorem. **M2 is closed.** I found no new mathematical defect in this product argument. Its physical transfer still depends on the stated inherited stopped-transfer theorem; this round does not reprove every underlying billiard flux estimate. [S7, S8]

## 4. Further examination beyond the changed statistical pages

### 4.1 The two-sided Poisson reconstruction includes a genuine reverse kernel

In `thm:v24-two-sided-deficiency`, the layer is selected from reference quantities, with width R/k around the reference ceiling. The forward map extracts a binomial point process, whose Poissonization error is O(1/k), and the support/trace remainders control the intensity error. The fixed face r=0 is not ignored: the endpoint strip has width O(1/k), the corresponding residual interval also has width O(1/k), and its one-record mass is O(1/k squared). After multiplication by k its contribution vanishes. [S9]

The reverse map reconstructs the layer points, generates the remaining observations from the reference conditional bulk law, and randomly interleaves the two groups. Invalid corner reconstructions and excessive Poisson counts have explicit conventions and vanishing probabilities. Most importantly, the normalized bulk comparison uses the separate relative-density hypothesis of size O(1/k), giving one-record squared Hellinger error O(1/k squared), hence product total-variation error O(1/sqrt(k)). This is more than convergence of a extracted point process. [S9]

A stress test illustrates why the bulk hypothesis matters. On the unit disk put w(u,v)=1-u squared-v squared and

\[
 q_{k,\theta}(u,v,r)=\frac2\pi
       (1+\theta u/\sqrt{k})\mathbf1_{\{0<r<w(u,v)\}}.
\]

For bounded theta and large k these are normalized densities. The ceiling is fixed and the amplitude converges uniformly to 2/pi. Nevertheless, k observations contain a regular local score with information E(u squared)=1/6. A parameter-independent ceiling Poisson limit would miss that bulk information. This family violates the manuscript's O(1/k) relative-density hypothesis and therefore does not refute its theorem. The explicit additional hypothesis is mathematically necessary in this argument; it is not expendable technical decoration. The manuscript also explains why its anchored physical application satisfies it. [S9; independent calculation]

**Assessment:** the inspected two-sided reconstruction proof is sound under its displayed hypotheses. This does not independently certify the earlier construction of every physical density to which it is applied.

### 4.2 Finite-signature uniqueness is not inferred from a distant-arc gap

The finite-signature argument addresses both local and global matching. A nonconstant analytic curvature function cannot have all its positive-order derivatives vanish at one point. Compactness therefore selects a finite jet order giving uniform immersion. A Taylor estimate supplies local separation. Trivial orientation-preserving symmetry separates distinct distant points through their complete signatures; a second compactness argument selects finitely many coordinates uniformly. The transition-obstacle asymmetry used here follows from the stated signature-rigidity assumption. [S10]

The noisy matching lemma assumes C2 control of the recovered signature curve. The minimum is first localized to the correct short arc, then strict positivity of

\[
 \frac{d^2}{dx^2}\frac12|\widetilde J(x)-y|^2
 =|\widetilde J'(x)|^2+
              (\widetilde J(x)-y)\cdot\widetilde J''(x)
\]

gives uniqueness. Its local Lipschitz assertion in the target and C1 curve perturbations is valid within that controlled C2 neighborhood. It is not a theorem about arbitrary uniformly close curves. [S10]

For example, J(x)=(x,0) and J_tilde(x)=(x,epsilon cos(pi x/epsilon)) are C0-close. For target zero, the squared distance is epsilon squared at zero and epsilon squared/4 at each of plus or minus epsilon/2. On a symmetric compact interval a minimizing point exists, cannot be zero, and has a distinct reflected minimizer. The perturbation is not C2-small. Again this is a hypothesis stress test, not a counterexample to the stated lemma. [Independent calculation]

The subsequent compact inverse modulus is a different result: it uses exact injectivity and compactness. The tail C times 2 to the power -M is a product-metric truncation bound, not an exponential analytic-continuation accuracy rate. The manuscript explicitly makes this distinction. I found no justification for reopening the former local-uniqueness objection. [S10]

### 4.3 The global estimator avoids two common circular arguments

The finite-separator proof includes the gaps in the data vector rather than assuming conditional laws determine them. Exact single-offset law injectivity and continuity, on a compact class, select finitely many bounded Lipschitz tests. The finite-template estimator therefore does not assume that empirical weak or total-variation accuracy controls arbitrary high density derivatives. Its deterministic implication follows from the separation margin and a finite minimum-distance rule. [S11]

The final flight number is selected before the pilot accuracy. Thus the pilot controls J times the gap error for the flight number actually used; the proof does not increase J afterward without recalibration. Successful marks are treated as iid in the uncapped sequence, with cap failures added to the error budget afterward. Tests sharing data need no independence for the union bound. The budget-indexed construction runs a selected stage afresh, so its diverging minimum flight number is not falsely attributed to a cumulative archive. These are correct and important details. [S11]

The resulting theorem remains conditional on the compact marked analytic class, unique incidence structure, relative-law estimates and observable calibration theorem. Its library and inverse moduli may be non-effective, as the author acknowledges. This is a consistency theorem, not a computational algorithm with a proved rate. I independently checked its logical composition, not every earlier calibration and geometric dependency. [S10, S11]

### 4.4 Orientation and the active appendix

The transported-anchor formula is genuinely equivariant away from the exact factorized density family. Its domain and denominator margins are explicit. The quotient uses the tagged common orientation relative to the marked lattice, transported together with every channel law; it is not an untagged density quotient silently substituted for that datum. The global reflection action preserves the incidence equations by conjugating the channel placements and reflecting the lattice realization. I found no new algebraic defect in these inspected modules. Their conclusion does not extend to pointwise sign erasure or declare arbitrary perturbed densities globally realizable. [S12, S13]

The active auxiliary compendium still lists thirty-six inputs. They remain part of the mathematical submission, despite being called auxiliary. I spot-checked the bounded-flight binary-count lower-bound chapter: the adaptive chain-rule exposure bound and two-point testing argument are consistent with the stated cubic indistinguishability input, and its restrictions to binary records, bounded flight numbers and shrinking offsets are explicit. That is not a verification of all thirty-six appendices, or of the imported physical support-family construction. [S17, S18]

## 5. R1: make the alternative mean explicit in the quadratic-risk argument

Near the end of the proof of `thm:v22-vector-boundary-gaussian`, the manuscript invokes the fourth-moment formula for sums to obtain uniform integrability of compact-local quadratic risk. The higher absolute score moments are available, but the local-alternative mean should be written explicitly. Bounded summand moments and weak convergence alone are not a general justification for the asserted uncentered fourth-moment bound. This is a minor omitted calculation, not evidence that the theorem is false. [S5]

Here is a direct completion using the manuscript's notation. On the common collar, writing s=w_0(x), Taylor expansion of the density before division gives, uniformly on compact h-sets,

\[
 \frac{f_{\delta_nh}}{f_0}
 =1+\delta_nh^t\mathsf S+O_K(\delta_n^2(1+s^{-1})).
\]

Consequently

\[
 \begin{split}
 \mathbb E_{n,h}\Delta_n={}&
 np_n\delta_n\mathbb E_0[\mathsf S\mathbf1_{C_n}]\\
 &+np_n\delta_n^2
       \mathbb E_0[\mathsf S\mathsf S^t\mathbf1_{C_n}]h
 +O_K(np_n\delta_n^3\log(1/q_n)).
 \end{split}
\]

The first term is O(np_n delta_n q_n)=o(1), the second tends uniformly to J_Sigma h, and the last is o(1). Thus the means are uniformly bounded. Applying the independent-sum fourth-moment estimate to the centered summands gives a bound by a constant times

\[
 (np_n\delta_n^2\log(1/q_n))^2
       +np_n\delta_n^4q_n^{-2},
\]

which is bounded under the stated rate; restoring the bounded mean proves the claimed uniform fourth moment. This also clarifies that each censored observation contributes zero to the statistic, rather than the entire sample statistic being set to zero whenever any censoring occurs.

**Required change:** insert this calculation, or an equally explicit bounded-mean argument. Do not label it a new theorem or reopen compact convergence because of it. Its repair is local to the existing proof.

## 6. I1 has regressed and C2 remains open

### 6.1 Current identity

The main source and PDF metadata identify revision 33. Both principal README entries identify revision 32, its branch and older source/review chain. The comparison shows only historical copies were added, not active-entry replacements. This is an objective delivery inconsistency. It does not change the validity of `lem:v33-finite-likelihood`, but it prevents a reader following the advertised entry from identifying the intended revision and response. **I1 is reopened.** [S1–S3, S14]

The next entry must distinguish the reviewed submission SHA, its predecessor review, and the SHA actually used for any new build. Historical mathematical-source commits may remain documented, but must not be presented as the current assembled submission. A point-by-point v33 response should explicitly close M1–M3 and carry forward C2 with its actual disposition.

### 6.2 Current execution evidence

The authenticated query for Actions runs on the v33 branch returned total_count zero. The retained `a2-v32-native-build.yml` push filter names the v32 branch only. Its presence does not establish execution on v33. The unchanged verification document still discusses a prospective complete native attempt and explicitly declines to certify C2. [S15, S16, S19]

Fresh queries of the existing v32 run 34701204570 returned latest-attempt job 103583939776 with conclusion failure. The job-step query returned an empty list and the run-artifact query returned an empty list. This is a different job identifier from the earlier attempt cited in the v32 report; the current report records the newly queried identifier rather than silently reusing the old one. No service-level cause was established. A failed attempt without executed steps is not a LaTeX counterexample, and these v32 observations are not a build of the v33 submission. [S19]

I did not execute the full native main or companion in this review. No complete manuscript PDF was inspected. The independent diagnostics attached here are not the author's native-source build and do not close C2. The evidence supports the statement that complete current verification was not established, not the stronger assertion that no author-side local build could exist anywhere.

**Required evidence:** execute the unchanged complete source graph for `main.tex` and `two_collision.tex`, retain the exact tested SHA, commands, compiler versions, full logs, reference/citation and duplicate-label checks, product hashes, and complete PDFs. Inspect the resulting documents and state the inspection coverage. A functioning local build is acceptable; success of a particular hosted service is not a mathematical requirement. A changed-section fixture, a generated workflow, an unstarted job, or a passing finite script is not this evidence. Successful compilation would establish the assembled artifact, not prove all its mathematics.

## 7. Significance at the requested journal level

The introduction's comparison is more disciplined than a claim to have subsumed marked-length spectral rigidity. De Simoi, Kaloshin and Leguil address analytic open dispersing billiards under their symmetry and genericity conditions. Finamore and Leguil address finite-horizon Sinai billiards using an enriched marked length spectrum. The present signed channel laws, onset gaps, marked deck labels and signature-rigid incidence hypotheses constitute a different data map. The manuscript correctly declines to claim inclusion between those observation maps without a proof. [S4; L1, L2]

Likewise, Meister and Reiss already obtain a nonregular regression/Poisson asymptotic equivalence. A Gaussian/Poisson contrast, Poissonization, or the classical finite-likelihood lemma cannot by itself carry an exceptional-novelty claim. The revised manuscript appropriately treats the latter lemma as standard. [S4, S5; L3]

The potential major contribution must therefore be judged through the uniform nonlinear relative boundary law, its unsymmetrized all-order contact inverse, and the intrinsic consequences genuinely derived from them. The four-density cancellation, determinant-one block algebra, final lattice matrix multiplication, compact inverse theorem and finite-template consistency principle are useful components; none alone establishes the requested level of significance. The same-experiment direct-position benchmark is a welcome comparison and must remain: supplying noiseless geometric samples and restricting flight length is not, by itself, a new intrinsic inverse theorem. [S4, S10, S11]

This literature check is an abstract-and-metadata comparison of selected primary sources, not an exhaustive priority audit. It does not establish that the core result is unoriginal. Equally, this review's positive findings on several modules do not establish the exceptional significance and complete correctness required for an acceptance recommendation. The precise distinction is important: an adverse recommendation is not permission to invent a counterexample or to equate missing build evidence with false mathematics.

## 8. Required response and final disposition

The next revision should deliver a coherent, source-pinned complete article rather than another increment that leaves the previous delivery blocker untouched. Correct the active navigation and current response record; supply an executed full-native main and companion with actual evidence; insert R1's alternative-mean calculation. Retain the observation hierarchy, common-versus-reference domination distinction, signed-versus-folded data distinction, charged failures, fixed-order stability qualifications and non-effective nature of the global consistency construction.

Do not obtain a cleaner-looking record by quietly removing active proofs or excluding difficult dependencies from the submission. Preserve the historical sources while making the role and hypotheses of every active component explicit. The unresolved task is completion and verification of this article, not arbitrary contraction of its scope or automatic expansion into further claims.

**Final disposition:** M1, M2 and M3 are closed. E1 remains closed at the stated compact local scope. I1 is reopened because the current delivery points to the previous revision. C2 remains open. R1 is a minor, explicitly repairable proof clarification. The newly added finite-experiment argument passes this review, and the additional inspected modules contain no newly established fatal defect. Acceptance of the complete submission at the requested journal level is not recommended on the present record.

## References and reproducibility

The exact source coverage, exclusions and authenticated execution queries are recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). The accompanying [diagnostics.py](diagnostics.py) was executed in ordinary and optimized Python with byte-identical [output](diagnostics.json). Its examples test specific identities and the necessity of stated hypotheses; none is represented as a physical-table counterexample to the manuscript or as a full proof verifier.

**L1.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), revised August 17, 2022; related DOI `10.1007/s00222-023-01191-8`. Abstract and version metadata checked; no full external proof audit.

**L2.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025. Abstract and version metadata checked; no later publication status asserted.

**L3.** A. Meister and M. Reiss, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248v1](https://arxiv.org/abs/1101.5248v1), January 27, 2011. Abstract checked for the nonregular regression/Poisson comparison. No external-paper PDF was inspected.
