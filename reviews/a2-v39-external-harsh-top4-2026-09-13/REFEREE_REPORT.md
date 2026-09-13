# Independent referee-style report on A2 revision 39

## Submission and recommendation

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 13, 2026  
**Requested standard:** a leading general mathematics journal. This is an author-requested, AI-assisted external-referee-style assessment, not a commissioned report or an editorial decision of any journal.

| Object | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Submission branch | `revision/a2-v39-native-complete-article-2026-09-13` |
| Reviewed commit | `dd0e5aefd49d200652afc3fc3f29f7a6f38ae326` |
| Reviewed tree | `e936d5f6f463ea51f7f4cccb862de9216d4c258d` |
| Preceding referee commit | `ac0c9d136d5a14f5f5d60388253d3f197f478902` |
| Native article | `papers/A2-v17-boundary-information-coarsening/main.tex` |

The stable directory name `A2-v17` is not the revision number. The source keys S01–S16, immutable links, read coverage, and execution limits are recorded in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md). The report concerns this frozen submission, not a subsequently moving branch.

**Recommendation: MAJOR REVISION. I do not recommend acceptance, and I would not treat this as a completed submission package.**

The principal outstanding delivery requirement, C2, remains unfulfilled by the evidence examined here. The newly retrieved v39 build job executed no steps and produced no artifacts. Reorganizing source files, adding a roadmap, and configuring another build are not substitutes for delivering the complete, source-bound, inspectable article requested in the preceding report. This is a substantial delivery hold, not a counterexample to the mathematical theorems.

At the same time, the revision has made the particular editorial repair requested in R38-P1. That item should be closed. The new proof architecture is useful and mathematically more informative than a revision log. The principal inherited proofs examined below do not acquire a new defect merely because no full PDF has been delivered. **I have not established a new fatal mathematical counterexample within this round's stated coverage.** This sentence is neither a proof of every inherited assertion nor an endorsement of suitability for the requested journal tier.

This report extends direct scrutiny to the compact-local Gaussian comparison, its underlying moving-boundary modulus and original-alternative moments, and the charged global acquisition argument. It also checks the core relative-factorization and smooth-jet arguments rather than treating the preceding referee report as their proof.

## 1. What v39 actually changes

The comparison with the preceding referee commit is two commits ahead and changes nine paths. There are three edited pre-existing active TeX files: `main.tex`, `article/15_operator_comparison.tex`, and `article/65_envelope_minimax.tex`. The other changes are a new roadmap, a workflow, a narrowly scoped source-check program, and three preserved predecessor files. [S01]

The native entry adds a table of contents and a proof-dependency subsection, moves the two statistical-transfer chapters into Part II, and relocates the envelope-splicing attribution to the acknowledgments. The operator chapter repairs its now-forward reference to that statistical comparison. The envelope chapter changes its opening exposition, not the ensuing mathematical model or proof. The main input list retains the 52 predecessor entries and adds the roadmap. The 36-input auxiliary wrapper is not a changed path. These are meaningful organizational changes, but **not newly proved mathematics**. Preservation of an input list is also not a recursive build certificate. [S02–S04, S12]

| Item | Disposition | Reason |
|---|---|---|
| R38-P1, developmental narration in the envelope appendix | **Closed** | Mathematical exposition replaces the narrative; acknowledgment preserves attribution and the distinction from a commissioned journal report. |
| Proof hierarchy and separation of observation maps | **Improved at source level** | The new roadmap identifies the nonlinear mechanisms and distinguishes their conditional global and statistical consequences. Typeset coherence has not been inspected. |
| R37-M1, common-frame anchoring and rooted coverage | **Repair retained** | The introductory theorem and single-offset composition retain realizability, a common-frame anchoring pair, and coverage of every obstacle orbit. |
| R37-M2 and original-alternative moments | **Repair retained; direct arguments examined** | Contiguity uses normalized null likelihoods; the original-law moment calculation is not inferred from total variation. |
| R37-V1, actual-input provenance implementation | **Not reopened** | Its repaired implementation is not changed by v39. This round does not claim a fresh execution of the preceding provenance regression suite. |
| C2, complete native delivery and inspection | **Open; major delivery requirement** | The examined v39 job has no executed steps and no artifacts. No complete-main product was inspected in this review. |
| R39-I1, current revision navigation | **New minor presentation issue** | Both current README entries still advertise v38 and link its response/evidence rather than identifying the v39 submission. |

The distinction between “retained,” “directly checked,” and “independently executed” matters. In particular, the prior report's positive numerical and provenance findings are historical evidence, not computations newly performed by this referee.

## 2. The relative nonlinear law: what the proof does and does not establish

The relevant arguments are `thm:v4-factorization` and the operator chapter, especially `prop:v9-trace-transport` and `prop:v9-morse-transport`. [S04, S06]

The determinant mechanism is genuinely relative. For a stationary discrete action, the Dirichlet cofactor identity gives

$$
-W_{uv}=\frac{\prod_i J_i}{\det H_{\mathrm{int}}},\qquad
\frac{-W_{uv}}{(-W_{uv})^0}
 =\frac{\prod_i(J_i/J_i^0)}{\det(I+G^0\Delta H)}.
$$

The chapter correctly identifies the cofactor and inverse-decay statements as classical ingredients. The demanding assertion is that the *nonlinear* perturbation along the entire stationary bridge has a uniformly summable spatial profile. A small operator norm alone, multiplied by an increasing number of sites, would not suffice. Here locality and endpoint decay supply an entrywise summable perturbation and hence a trace-norm bound. Telescoping the logarithmic determinant series then yields dimension-independent continuity; fixed derivatives introduce polynomial factors in the series index, still summable against the strict geometric margin.

The factorization theorem contains a second step beyond bounded relative error. It glues a left half-line orbit to a reversed right half-line orbit, bounds the stationarity residual in the sum norm, and controls the correction by the inverse of a uniformly strictly diagonally dominant symmetric Hessian. Symmetry legitimately transfers the uniform maximum-norm inverse bound to the sum norm. The two retained blocks have size `floor(j/3)`. Removing the middle perturbation is small in trace norm, while the remote reflections and off-diagonal Green blocks are exponentially small. Thus the limiting logarithm splits into two half-line logarithms, rather than merely remaining bounded.

The use of a slower fixed exponential to absorb polynomial losses at each fixed derivative order is valid. The constants may depend on that order and on higher boundary norms. This is not an estimate uniform in an unrestricted derivative order. Nor are the geometric derivatives fixed-physical-time derivatives: the convention is channel-centered, with `t = j g(xi) + d`.

The normalized physical integral also has a substantive argument. The positive Hessian square-root chart reduces

$$
d^{-2}\int(d-E(y))_+a(y)\,dy
$$

to an integral on a fixed disk. Its dependence on `sqrt(d)` is even, which supplies a smooth right extension in `d` with a finite additional derivative budget. The exponential physical multiplier is left outside that stable normalized integral. This avoids differentiating a sharp moving boundary without justification and avoids dividing an absolute action remainder by the small reference twist.

I found no defect in these inspected mechanisms. This is not a fresh reconstruction of every finite-itinerary localization, suspension/flux, regular-terminal-level, or auxiliary dependency. Those limits of coverage are material; a positive reading of the determinant argument cannot certify them all by implication.

## 3. The signed inverse: the algebra is not the whole theorem

The single-offset inverse is examined in `thm:v26-density-inverse` and `prop:v26-density-stability`; the smooth inverse is examined through `prop:v22-last-jet-block`. [S07–S08]

For an interior positive density

$$
f(u,v)=Z^{-1}B(u)B(v)[d-S(u)-S(v)],
$$

the four-density ratio satisfies exactly

$$
1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=t(u)t(v),\qquad
 t(u)=\frac{S(u)}{d-S(u)}.
$$

A fixed nonzero anchor has positive action by strict convexity, selecting the positive scalar root. The formula recovers the unsymmetrized action and normalized amplitude. Its density evaluations are meaningful because the model supplies a unique continuous representative, not because a finite sample supplies pointwise density values. Stability is in a fixed interior `C^M` norm with positive denominators and a nonvanishing anchor; no derivative bound is inferred from total variation.

The principal inverse difficulty lies in passing from action jets to graph jets. The paper addresses the potential loss of one graph derivative in differentiated stationarity by working with finite-truncation action variations. Interior orbit variations cancel, and the surviving terminal term has summable exponential decay. The smooth-remainder lemma then interpolates *functions* with equal finite jets, integrates the exact finite envelope identity, and only afterwards takes the infinite-truncation limit. Its direct variation has the form

$$
\partial_t\ell_{r,t}(y,z)
 =\frac{h_{r,t}(y,z)}{\ell_{r,t}(y,z)}
   [\Delta\psi_r(y)+\Delta\psi_{1-r}(z)].
$$

The resulting action difference is `O(|u|^(M+1))`. The functional norm hypotheses are explicit; a finite coefficient list is not mistaken for a bound on an arbitrary smooth remainder. Flat perturbations are treated as a limitation on smooth boundary-image determination, not swept away by formal power series.

At the first occurrence of degree `n`, only the linear orbit contributes. The starting site is counted once and interior sites twice, giving the diagonal coefficient `coth(n gamma)` and the off-diagonal coefficient `r_b^n csch(n gamma)`. The determinant-one calculation is consistent with these multiplicities. The lower-order filtration and the invertible leading geometry, not the determinant identity in isolation, justify the finite triangular inverse.

I therefore do not reopen the earlier smooth-jet objection. Equality of smooth jets still does not identify a smooth obstacle globally. The manuscript properly reserves complete boundary-image recovery for connected analytic boundaries. Likewise, the periodic composition still needs realizability, unique framed signature matching, common-frame rank-two holonomies, and rooted coverage. The identity `L = V M^{-1}` recovers the lattice once those holonomies are known; it does not place unvisited obstacles. A fresh exhaustive audit of the separate gluing, orientation-quotient, and finite-signature chapters is not claimed in this round.

## 4. Fresh statistical audit: compact experiments and original-law moments

### 4.1 The finite-to-compact passage is actually proved

`lem:v32-finite-net` uses a single comparison kernel chosen on a fixed finite net and estimates its error at nearby parameters by contraction of total variation. The nearby net point occurs in the estimate, not as an unknown-parameter argument to the kernel. This gives

$$
\Delta(\mathsf E_n,\mathsf E)
\le \Delta(\mathsf E_n|_F,\mathsf E|_F)+\omega_n(r)+\omega(r).
$$

The order of limits is correct: first the sample-size limit with the net fixed, then the mesh limit. [S10]

The necessary modulus is supplied, not assumed away. For successful densities `f_theta = a_theta (w_theta)_+`, the moving-hypersurface lemma splits the domain into an `O(epsilon)` collar, where mass is `O(epsilon^2)`, and the common interior, where the squared root-density difference is bounded by amplitude error squared plus `epsilon^2/s`. Normal integration produces the logarithm. Joint smoothness then gives, for `s = ||h-h'|| <= 1`,

$$
H^2(f_{\delta_nh},f_{\delta_nh'})
 \le C_K\delta_n^2s^2[1+\log(1/\delta_n)+\log(1/s)].
$$

The failure probabilities in this vector model are identical. Multiplication by `p_n` and product subadditivity, together with `n p_n delta_n^2 log(1/delta_n) -> 1`, give the required uniform product modulus. The Gaussian modulus is evaluated on the identifiable subspace and does not invert the information matrix on its kernel. [S09–S10]

Thus an objection that the paper simply equates finite likelihood-vector convergence with compact Le Cam convergence would be incorrect. The fixed-window corollary retains separate cap and finite-bridge transfer errors. I have not reconstructed every transfer theorem or the separate count–endpoint multirate chapter in this round, so this finding does not automatically validate all its applications.

### 4.2 Contiguity and quadratic risk are not obtained circularly

The common-collar representative uses `q_n = delta_n [log(1/delta_n)]^(1/4)`. The probability of any censored successful observation is uniformly `O([log(1/delta_n)]^(-1/2))`. A parameter-independent reverse kernel can assign a fixed point to the rare censoring symbol. This is sufficient for experiment comparison; it is not sufficient by itself for transferring an unbounded loss.

The short contiguity proof invokes the normalized null-likelihood argument, with a strictly positive mean-one limiting likelihood. It does not assume an alternative central-sequence limit in order to obtain the contiguity used to prove that limit. The finite likelihood lemma separately constructs both comparison kernels from a common `L^1` coupling and conditional distributions. [S09]

More importantly, the article now verifies the mean under the original alternatives by expanding the *one-observation* density ratio on the common collar. It obtains `E_{n,h} Delta_n = J_Sigma h + o_K(1)`. A centered fourth-moment expansion then has the two terms

$$
[n p_n\delta_n^2\log(1/q_n)]^2,
\qquad n p_n\delta_n^4q_n^{-2}.
$$

These are bounded, with the latter tending to zero. Restoring the bounded mean supplies the uniform integrability needed for compact-local quadratic risk. There is no claim that an entire product likelihood is uniformly close to one. I found no defect in this inspected repair. It remains a reference-model local result, not a globally adaptive estimator of an unknown reference channel.

## 5. Fresh acquisition audit: the pilot and global reconstruction

The physical record space supplies planar positions in a common sensor frame for the two types of a channel, but does not register different channels. The acquisition labels and clock are fixed; unknown contact charts are not inserted into the record map. That is a richer experiment than the intrinsic transverse-law datum. The paper says so. [S11]

The capped pilot has a valid one-sided argument. There is a programmed grid point with true excess in `[h,2h]`. At that point the lower success bound gives the required failure probability. An earlier first success cannot precede onset. No inference that a finite sequence of failures proves zero probability is used, and no far-from-onset success lower bound is needed. The estimator

$$
\widehat g_e=(\min_b T_{e,b}-h)/j
$$

therefore satisfies `j |g_hat_e-g_e| <= h` on the good event. The two estimated contact positions and positive gap margin control the normalized direction. Crucially, the pilot is performed at the already selected final flight number `J`, which is not increased afterwards. This avoids silently losing control of the physical offset when the flight number grows.

The finite-separator construction includes the gap coordinates in the estimation criterion. Equal gaps and equal two-type joint endpoint laws at the one chosen offset would force equal action germs; thus the compact pair set is separated. Bounded Lipschitz tests, a finite subcover, and a finite template library provide a measurable estimator without claiming an effective analytic reconstruction rate. The phrase “endpoint marginals” here means marginalization of residual time while retaining the endpoint pair; it is not an inverse from two separate one-dimensional endpoint distributions. [S11]

The post-pilot sampling argument also keeps its probability conditioning straight. Conditional on the pilot, the uncapped success sequence has independent identically distributed marks. The proof couples it to the capped experiment and adds the cap failure probability; it does not condition on cap completion and then assert independence without justification. Shared samples among tests do not obstruct the union bound. All preparatory failures are charged.

Finally, the budget-indexed scheme runs its selected stage afresh. Its claim of a diverging minimum flight number does not apply to an accumulated historical transcript containing earlier stages. This distinction is essential and is explicitly retained.

These are positive findings about the declared compact-class consistency argument, conditional on its cited local law and global inverse. They do not turn non-effective compactness into a rate, remove the marked-incidence assumptions, or establish equivalence to the richer noiseless position experiment. The direct-position benchmark remains an important limitation on how the physical reconstruction should be advertised.

## 6. The envelope appendix and the repaired attribution

The opening of `article/65_envelope_minimax.tex` now reads as mathematics. The attribution has moved to the acknowledgments without disappearing. **R38-P1 is closed.** [S02, S05]

The retained lower-bound argument uses a fixed smooth envelope with strict norm slack, physically allowed leading-parameter splitting, and nuisance splices of width proportional to `s^(3/m)`. Every query has curvature-testing entropy at most a constant times `s^(6+6/m)`, including adaptive choices; outside the splice the alternatives agree. The padded stopped-transcript chain rule charges expected preparations. For timing, the entropy is taken in the support-compatible direction from the shifted-onset law to the earlier-onset law. The two lower bounds combine as worst-case bounds; they need not use the same pair.

I found no defect in those inspected lower-bound steps. The matching upper bound invokes an inherited theorem not freshly rederived here. Most importantly, the nuisance alternatives are not asserted to be exact finite-offset billiard probabilities. The new roadmap preserves this restriction. It would be erroneous to transfer this minimax lower bound to a smaller physical model without proving realizability, but that is not a claim made in the revised passage.

## 7. Outstanding delivery and presentation requirements

### C2 — complete native article: still open

For the frozen v39 head, the retrieved workflow run is `34748124986` and the job is `103699693209`. Its conclusion is `failure`, its step list is empty, its runner identifier is zero, and the run artifact count is zero. These metadata do not identify the cause. **They establish no executed TeX command and therefore must not be described as a TeX compilation failure.** [S14]

The new workflow sensibly attempts early immutable-source retention and full native building. The source checker explicitly distinguishes its narrow default mode from recursive graph checking and from TeX/PDF execution. I do not fault it for failing to perform a task it expressly disclaims. Neither program's presence supplies the missing deliverable. [S12–S13]

To close C2, provide durable, retrievable complete native main and companion products, their frozen source identities, commands, tool versions, return codes, raw logs and recorder/input evidence, and an explicit visual-inspection record. Remedy unresolved references, missing symbols, duplicate labels or destinations, and obstructive layout defects if found. These are checks to perform, not defects asserted without seeing the PDF. An artifact archive or release is acceptable; committing every binary to Git is not required. An earlier conversation attachment without a durable retrieval route is insufficient for a new referee.

This review did not compile or visually inspect either native manuscript. It cannot certify their typeset completeness. Repeating another source-only restructuring would not answer this standing requirement.

### R39-I1 — stale current entries: minor but concrete

At the reviewed commit, the root README and the paper README still designate v38 as current, name its branch, and direct the reader to its response and verification. The native main is v39. The nine-path v39 delta adds no matching response/evidence index. [S15]

Update the two current entries and provide one source-pinned v39 response/evidence entry distinguishing inherited evidence, newly executed checks, and C2's actual status. Preserve the historical records. This is a navigation and reproducibility repair, not an additional mathematical hypothesis or a reason to discard proofs.

## 8. Significance at the requested journal level

The strongest prospective contribution remains the nonlinear relative law composed with the unsymmetrized, all-order contact inverse under its precise observation map. The four-density cancellation, determinant-one identity, lattice matrix inversion, finite-net lemma, and compact-injection modulus are not separately adequate significance arguments merely because each is correct. The manuscript should be judged by the new analytic mechanism and the inverse information it makes accessible, not by the number of revisions, theorem labels, or author-requested reviews.

The new roadmap substantially improves this hierarchy at source level. I do not demand a replacement theorem or arbitrary deletion to compensate for missing build evidence. However, neither a successful build nor the closure of earlier objections automatically warrants acceptance at the requested level. A complete article and an affirmative assessment of its total mathematical significance remain necessary.

The primary records consulted describe different data: De Simoi–Kaloshin–Leguil study marked-length determination for analytic open billiards under stated symmetry/genericity conditions, while Finamore–Leguil study an enriched marked length spectrum for finite-horizon Sinai billiards. The present manuscript assumes signed channel laws, onsets, marked deck labels, and prescribed signature-rigid incidence information. No reduction between these observation maps has been established in this review. I therefore assert neither subsumption nor a counterclaim of lack of novelty. [L1–L2]

Meister–Reiss already provide a nonregular-regression/Poisson-boundary equivalence. Thus a Gaussian/Poisson contrast alone is not a novelty certificate; the manuscript already acknowledges this point. The present literature check is deliberately bounded and is not an exhaustive priority investigation. [L3]

## 9. Independent controls, limitations, and resubmission disposition

The attached [independent_checks.py](independent_checks.py) was executed normally and under Python optimization, with byte-identical output and empty stderr. [RESULTS.json](RESULTS.json) contains the actual values; [EXECUTION.json](EXECUTION.json) records commands, versions through the result file, return codes, hashes, and the diagnostic-development correction.

The four finite control families cover eight high-precision Hellinger comparisons in an explicit quadratic moving-support model, twelve original-alternative collar-moment evaluations, 216 exact rational grid/centering cases, and a finite-versus-compact negative control. The last is **not** a counterexample to this manuscript: it demonstrates why the modulus that the manuscript actually proves is indispensable. The scalar model has boundary information three; its Hellinger ratio tends to three quarters. At absolute shift `10^-8`, the computed ratios are approximately `0.773592`, still displaying the expected slow logarithmic correction. High working precision must not be confused with a small asymptotic error.

No manuscript source is imported by these controls. They do not simulate a realized periodic table, prove a LAN theorem, certify an infinite-dimensional inverse, execute the author's regression suite, or build a PDF. A complete checkout was not materialized. The detailed coverage ledger records other inherited arguments not freshly audited, including the complete auxiliary compendium, all multirate applications, and the full periodic gluing and orientation-quotient proofs.

The next submission should close C2 with actual products, repair R39-I1, and retain the accepted mathematical and editorial repairs. The requirements are **not** to abandon the programme, replace the intrinsic datum by richer position samples, reinterpret an envelope lower bound as physical, or shorten away difficult proofs. The precise conclusion is: the specific v38 appendix-presentation request is answered; the inspected core and additional statistical/acquisition arguments have no newly established fatal counterexample; the complete native delivery remains unproved by the available record; and acceptance is not recommended.
