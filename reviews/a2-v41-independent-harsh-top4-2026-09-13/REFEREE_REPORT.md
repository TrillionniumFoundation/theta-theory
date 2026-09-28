# Independent referee-style report on A2 revision 41

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 13, 2026  
**Standard requested:** a leading general mathematics journal at the level of the four journals specified by the author. This is an author-requested, AI-assisted independent assessment, not a commissioned journal report or an editorial decision.

| Object | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Submission branch | `revision/a2-v41-complete-native-delivery-2026-09-13` |
| Reviewed commit | `c730a60bbc8af2a4c6e432813c31dccc897828e7` |
| Reviewed tree | `1c626923b2623cadd97450d0a93dbaffd564fe34` |
| Previous submission | A2 v40, `070aa946fb28001916ad1bbd3503afa5f6cae3b3` |
| Native entry | `papers/A2-v17-boundary-information-coarsening/main.tex` |

The directory name `A2-v17` is historical. References S01–S16 and L1–L4, immutable source links, retrieval coverage, and execution details are in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md). Source assertions below concern this commit, not a moving branch. The preceding report is S05.

## Recommendation

**MAJOR REVISION. Acceptance is not recommended for this snapshot.** The revision improves the explanation of the mathematical contribution and correctly repairs a version-sensitive literature comparison. It does not close the outstanding complete-native-delivery requirement C2 or the stale-navigation item R39-I1. A branch called “complete native delivery” is not evidence of that delivery.

Within the fresh coverage specified here, **I have not established a new fatal mathematical counterexample**. In particular, the single-offset inversion, the finite smooth-remainder argument, the anchoring-compatible rerooting, the charged calibration policy, and the examined moving-support Gaussian arguments withstand the checks described below. This finding is not a certification of every theorem, all auxiliary chapters, or the entire physical transfer chain. An honest severe review must distinguish an actual contradiction from a missing delivery, a restricted theorem from an overstated reading of it, and an unresolved significance assessment from a proof gap.

The central prospective contribution is the composition of a relative nonlinear bridge law with reconstruction of labelled contact jets from genuinely coarsened transverse laws. The global matrix identity, compactness argument, and algebraic density cancellation do not individually establish exceptional general-journal significance. Conversely, it would be inaccurate to dismiss the whole argument as those elementary steps: the nonlinear half-line analysis and finite-remainder filtration do real work.

| Issue | Current disposition |
|---|---|
| C2: complete source-bound main and companion delivery | **Open; major delivery hold.** The exact-head hosted run executed no steps and supplied no artifacts. |
| R39-I1: current-version navigation and response/evidence entry | **Open.** Both current README entries still designate v38. |
| Root compatibility with the common anchoring frame | **Resolved and retained.** The v40 lemma is now explicitly integrated into the introductory proof. |
| Florio–Leguil version-sensitive comparison | **Resolved in the inspected v41 text.** It uses v5 and distinguishes smooth conjugacy from the removed rigidity assertion. |
| Freshly examined local, statistical, and acquisition arguments | No new fatal defect established; scope and dependencies are recorded below. |
| Exceptional significance at the requested journal level | Not established by this assessment; an editorial evaluation, not a mathematical impossibility claim. |

## 1. What was revised, and what was not

The comparison with the previous submission has three additional commits and eleven changed paths. Five are the inherited v40 review package. The author-side changes are a workflow, a new introduction, a new proof-architecture subsection, a new bibliography, a preserved v40 entry, and changes to the native entry. The final mathematical-presentation commit itself changes five paths. It does not replace the underlying local, statistical, or global proofs. [S01–S05]

That is not intrinsically objectionable: a revision can answer an exposition or composition objection without changing a correct theorem. Here the new introduction makes the coarsened observation map more prominent, explains why the analytic input precedes the elementary inversion formulas, and explicitly invokes the rerooting lemma. It also makes the same-experiment direct-position benchmark conspicuous. Those changes answer real concerns and should not be dismissed merely because the underlying proof files are unchanged. [S02–S03]

But the immediate predecessor asked for actual complete delivery and accurate current navigation. The unchanged root and paper README still identify v38, send the reader to its response and evidence, and state that the complete main has not been built in that earlier revision session. There is no new current response/evidence entry in the inspected v40-to-v41 delta. The new workflow is an attempted means of delivery, not a response documenting delivery. The mathematical exposition cannot be counted as having answered those separate requests. [S01, S04, S14]

## 2. Relative asymptotics: the inspected argument is genuinely relative

The forward assertion is not just convergence of a stationary action. It controls the normalized mixed endpoint derivative, whose unnormalized value is exponentially small in the number of flights. An absolute action estimate would not suffice to obtain the claimed conditional law. The source does address that distinction. [S06]

At quadratic order the half-line interior Hessian has diagonal entries $2c_{(b+i)\bmod2}/g$ and adjacent entries $-1/g$. With the manuscript's definition of $\sigma_i^{(b)}$, its Green kernel is

$$
G_{ik}^{(b)}=\frac{g\sigma_i^{(b)}\sigma_k^{(b)}}{2c\sinh\gamma}
\left(e^{-\gamma|i-k|}-e^{-\gamma(i+k)}\right).
$$

The weighted-space bound follows by splitting the sum at $k=i$, with both geometric ratios strictly below one when $e^{-\gamma_-}<\rho<1$. Locality of the nonlinear equations then gives a contraction on a common small endpoint collar. At each fixed differentiated order, the same invertible linearized operator multiplies the highest orbit derivative. This is a fixed-order assertion requiring the corresponding smooth bounds, not a uniform statement over unrestricted derivative orders. [S06–S07]

More importantly, locality and endpoint decay bound the sum of the absolute Hessian-perturbation entries. They therefore give trace-norm control independently of the finite bridge dimension. The proof glues left and right half-lines, controls the resulting residual in the sum norm, and uses symmetry of the diagonally dominant Hessian to transfer its maximum-norm inverse bound to that sum norm. The interaction and boundary overwrites are exponentially small up to fixed polynomial factors.

For the determinant comparison it retains blocks of size $\lfloor j/3\rfloor$ at the two ends. The discarded middle perturbation is small in trace norm. Finite Green kernels on the retained blocks approach the corresponding half-line kernels, while the cross blocks decay exponentially. Telescoping the logarithmic determinant series bounds its difference by a trace-norm difference. The argument thus compares relative determinants before exponentiating. I found no erroneous division of an uncontrolled error by an exponentially small reference twist in these steps. [S06]

The moving-sublevel integration is also given a mechanism: a constructive Morse change of variables converts it to a fixed domain, with additional but finite derivative requirements for offset differentiation. The smooth extension at zero offset is not obtained by formally differentiating a sharp moving indicator. I accept the inspected mechanism under its declared geometric hypotheses. I have not independently reconstructed every finite-itinerary localization and phase-volume normalization on which it relies; those dependencies are not certified by this paragraph.

## 3. The single-offset inverse and the all-order contact recursion

### 3.1 The actual datum is a density, not merely a support

On the interior square the same-type law has density

$$f(u,v)=Z^{-1}B(u)B(v)\{d-S(u)-S(v)\}.$$

Its four-density ratio satisfies

$$
R(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)},\qquad
1-R(u,v)=t(u)t(v),\qquad t(u)=\frac{S(u)}{d-S(u)}.
$$

This cancellation is correct, including for non-even actions and nonconstant amplitudes. Strict convexity makes $t(a)>0$ at a fixed nonzero anchor. Consequently $t(u)=(1-R(u,a))/\sqrt{1-R(a,a)}$ and $S=dt/(1+t)$. The continuous-density convention legitimately makes these slice values determined by the law; it does not make them directly observed in a finite sample. [S08]

The stated stability uses an interior $C^M$ norm, positive density denominators, and a positive scalar anchor bound. Those hypotheses justify the fixed-order product and reciprocal estimates. They do not imply recovery of high derivatives from total variation alone. The finite-flight corollary correctly controls normalization on the whole endpoint box and differentiates only inside a square where the cutoff remains positive. Its projection subtracting estimated constant and linear action terms is also appropriate.

Our exact rational controls retain an odd action term and an unknown nonconstant amplitude: 361 pair identities and 38 action/amplitude reconstructions pass. A separate monotone support-preserving transformation changes the density-ratio invariant. This is a negative control against replacing the density theorem by a one-support theorem, not a counterexample to the manuscript. It would be wrong to reopen the already distinguished support-versus-law issue on that basis.

### 3.2 The determinant is not the filtration proof

The substantial question is why an order-$n$ action jet depends only on graph jets through order $n$, despite the extra derivative that can occur in the stationarity equations. The exact finite-truncation envelope argument resolves that issue in the inspected source. Interior orbit variations cancel, and the remaining terminal variation tends to zero with a summable bound. [S07]

The smooth-remainder lemma is essential. It interpolates two actual anchored smooth graph pairs with equal finite jets, uses

$$
\partial_t\ell_{r,t}(y,z)=\frac{h_{r,t}(y,z)}{\ell_{r,t}(y,z)}
\{\Delta\psi_r(y)+\Delta\psi_{1-r}(z)\},
$$

and integrates the exact finite envelope identity before taking its limit. Weighted orbit decay makes the resulting action difference $O(|u|^{M+1})$. The argument therefore factors through finite jets without identifying a smooth function with its Taylor series. It explicitly requires functional smoothness bounds; a bounded coefficient list is not substituted for them. Nor does the local graph interpolation purport to realize a global periodic-table interpolation.

At the first occurrence of a new graph jet only the linear half-line orbit contributes. The initial site has multiplicity one and every interior site multiplicity two. The resulting coefficients are

$$
1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),\qquad
2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
=\mathfrak r_b^n\operatorname{csch}(n\gamma).
$$

Together with $\mathfrak r_0\mathfrak r_1=1$, these give the stated determinant-one block. The explicit leading quadratic inverse and the proved lower-triangular dependence, rather than the determinant alone, justify the finite tangent isomorphism. Analyticity is needed only later for boundary-image determination. [S07–S08]

To test more than symbolic matrix algebra, I independently solved 96 finite nonlinear stationary-orbit problems, using 96 edges and exact Euclidean flight lengths, at symmetric and asymmetric positive curvatures and both starting types. Envelope coefficients for degrees three through six approach the claimed blocks with the expected quadratic trend as the endpoint is halved in the parabolic baseline. The maximum stationarity residual was $1.28\times10^{-15}$ to the displayed precision; the largest coefficient error at $|u|=0.01$ was below $9.82\times10^{-5}$. Deliberately swapping the asymmetric label in the proposed coefficient produces an error exceeding $0.165$ and is detected. These are finite numerical diagnostics, not an infinite-dimensional proof or tests of arbitrary analytic boundary families.

## 4. Intrinsic periodic composition: a repaired step, with its real hypotheses

The new introductory proof now explicitly transports the tree root to the common anchoring frame using `lem:v40-signature-rigid-rerooting`. The short proof is valid assuming the analytic signature-symmetry lemma it cites. A unique full oriented signature at one framed point forces every proper symmetry to fix a point and its tangent, hence to be the identity. The cited signature classification then makes signatures unique everywhere on that boundary. [S02, S09]

Only edges on the path from the old root to the new root reverse. Every intermediate new parent was already a parent on that path and hence has unique signatures; the terminal new parent has them by hypothesis. Off-path edges keep their orientation. A signature-rigid anchoring incidence supplies the new-root hypothesis. This does not permit rerooting at an arbitrary symmetric leaf, but that stronger assertion is not made. The revision adds no measured channel or registration assumption to force the result.

The interpretation of the global theorem must remain exact. It uses realizable marked data, signed channel conventions, two independent cycle holonomies based in one frame, and signature-rigid propagation reaching every obstacle orbit. Once their geometric reconstruction is available, $L=VM^{-1}$ determines the lattice, including its Gram form. That matrix identity does not independently provide matching, existence, admissibility, or placement of unvisited obstacles. The v41 introduction now says so explicitly. [S02–S03, S08–S09]

I do not require the author to strengthen these conditions or to solve an unmarked inverse problem not claimed in the paper. Equally, an abstract or summary cannot replace this conditional result by determination of an arbitrary periodic billiard from arbitrary trajectory observations. The full gluing, orientation-quotient and signature-stability chapters were examined in the preceding report; this round freshly checks the local-to-global composition and the rerooting argument, not every line of those chapters again. Earlier favorable discussion is not a substitute for their proofs in the submission.

## 5. Fresh audit of the charged physical acquisition argument

This round extends direct scrutiny of the calibration and global-estimation chapters, rather than merely recycling the predecessor's local conclusions. The distinction between intrinsic laws and the richer acquisition experiment survives this audit. The detector observes planar positions in one common frame for the two types of a channel, while distinct channel frames remain unregistered. The preparation space and success/failure record map use acquisition labels and physical time, not unknown contact charts. Independent preparations from normalized phase volume are part of the model. [S10–S11]

### 5.1 Onset and frame calibration

The pilot lower bound is $p_*(j,h)=c_*h^2e^{-j\gamma_+}$ for a true excess in $[h,2h]$. On the programmed grid there is always such a point. At that point $N$ failures have probability at most $e^{-Np_*}$; an earlier success cannot precede onset. Thus the union bound over channels and types gives the asserted simultaneous first-success event. It does not infer that a finite string of failures proves zero success probability.

On that event $jg<T_{e,b}\le jg+2h$, and

$$\widehat g_e=\frac{\min_bT_{e,b}-h}{j}$$

satisfies $j|\widehat g_e-g_e|\le h$. Endpoint localization gives contact-position error $O(\sqrt h)$ and a tangent error of the same order after normalizing the contact displacement. The denominator is bounded below using the positive gap margin. Absolute sensor origins need not be bounded because the error is expressed through displacements. [S10]

A crucial ordering is correct: the final even flight number $J$ is chosen before the pilot, and the pilot itself uses $j=J$. One therefore controls the actual later time error $J|\widehat g-g|$, not an obsolete smaller-flight error. The total pilot cap includes all failed preparations at earlier scan times. There is no hidden free calibration sample.

### 5.2 Tests, caps and the compact-class estimator

The post-pilot statistic is an observable projection. Its error is compared with ideal centering only in the analysis. At a fixed true table, the finite and limiting position laws use the same embedding; applying the observable projection is a common map. The Lipschitz test then absorbs coordinate error $O(\sqrt h)$, and fiber integration bounds the offset-law error by $O(h)$. This is not a false total-variation continuity claim for planar measures supported on different curves. [S10]

The finite separation argument includes the gaps as well as the law moments. With all gaps fixed, equality of the two endpoint laws at a single offset would force equality of the action germs; compactness then gives a finite separating library of bounded Lipschitz tests. The positive separation margin may depend non-effectively on the compact class. It is not produced by estimating high derivatives in total variation. The finite-template rule has a fixed measurable tie convention, and its elementary $3c<8c$ bound correctly converts moment error into finite-data accuracy. [S11]

After conditioning on a good pilot history, fixed-design successful marks in the uncapped sequence are independent with the appropriate successful law. The proof compares capped and uncapped sampling on the event that the cap is not reached. It does not incorrectly condition on cap completion and then assert independent marks. Binomial lower-tail bounds control insufficient successes, and a union bound over tests does not require independence between tests using the same sample. The displayed finite cap charges the rare-event cost.

Finally, the increasing-order construction uses the pre-existing compact inverse modulus to select each stage. The budget-indexed version runs the selected stage afresh; it does not claim that an archive containing earlier short flights has a diverging minimum flight number. This resolves a genuine possible ambiguity. No new defect was found in these controlling steps, conditional on the forward estimates, stopped-transfer bounds and compact rigidity modulus that they invoke.

The limitation is mathematical scope, not a discovered contradiction: this is a uniform-consistency existence theorem on a specified compact marked analytic class. It is neither a numerical analytic-continuation rate nor an effective polynomial-cost design theorem. Its pilot uses planar positions, and its same-experiment direct-position benchmark remains relevant. It must not be advertised as global acquisition from a scalar-only uncalibrated record. The current introduction explicitly maintains these distinctions; they should be preserved, not counted as new flaws.

## 6. Moving-support Gaussian experiments and quadratic loss

I freshly checked the vector collar, likelihood, moment and compact-experiment arguments. The original moving-support family need not be absolutely continuous relative to its zero-parameter member. The source first removes a common collar, whose product mass is negligible, and only then uses reference likelihoods. At

$$q_n=\delta_n[\log(1/\delta_n)]^{1/4},\qquad np_n\delta_n^2\log(1/\delta_n)\to1,$$

the relevant budgets satisfy

$$
np_nq_n^2\to0,\qquad np_n\delta_nq_n\to0,\qquad
np_n\delta_n^4q_n^{-2}\to0.
$$

The censoring and reverse reconstruction are independent of the unknown local parameter. Positivity on the retained collar and a positive censored reference atom justify the reference domination used in the LAN expansion. [S12]

For finite experiments, weak convergence of the likelihood vector together with unit prelimit and limiting means gives coordinatewise uniform integrability by truncation. An $L^1$ coupling of the likelihood-vector laws and disintegration in both directions supply common Markov kernels. This is more than simply naming LAN. The separate Hellinger estimate

$$H^2(f,\widetilde f)\le C\{\varepsilon^2\log(e/\varepsilon)+\eta^2\}$$

comes from a small boundary strip and integration of $\varepsilon^2/s$ outside it. After products it yields a modulus of order $s\sqrt{1+\log(1/s)}$ in total variation on local parameter differences. The finite-net lemma uses one kernel for the whole parameter set; the nearest net point is only an error-comparison device. This supports the stated compact-local upgrade, including singular information on its identifiable subspace. It does not give uniform equivalence on an unbounded local parameter space. [S12–S13]

The quadratic-risk argument also survives direct inspection. Normalized likelihoods give the tilted weak limit without presupposing an alternative central limit theorem. Separately, the one-mark density expansion on the collar gives the original-alternative mean, and independence plus the fourth-score-moment bound yields a uniformly bounded fourth moment of the central sequence. This is the necessary uniform integrability for quadratic loss; vanishing total variation by itself would not establish it. The v35-labelled equations cited from the tilting subsection are present in the vector chapter, not missing references inferred from inspecting that subsection in isolation. [S12, S15]

An independent radial linearly vanishing density model has boundary information $J=2$. Its exact collar-mass and truncated-mean calculations agree with the asserted asymptotic budgets. The displayed diagnostic uses a continuous scaling proxy for sample size and is not a Monte Carlo theorem check. Its convergence is slow, which is entirely compatible with the logarithmic asymptotics. I have not freshly certified all Poisson-kernel, count–endpoint, anchored physical-realization, and auxiliary minimax arguments in this round. Nothing here upgrades a restricted Gaussian statement to the full richer position experiment.

## 7. Literature and the requested journal threshold

The literature correction is now specific and correct. Florio–Leguil v5 states the dynamical smooth-conjugacy result and its open-billiard application; its revision notice says the earlier spectral-rigidity assertion was removed after an error in Proposition 3.1. The new introduction and bibliography use precisely that version and do not present it as a currently proved general Euclidean table-rigidity theorem. This item is closed in the inspected text. [S02–S03; L2]

The nearby inverse results use different observations. De Simoi–Kaloshin–Leguil study marked-length determination for analytic open billiards with symmetry and genericity hypotheses. Finamore–Leguil's stated finite-horizon Sinai result uses an enriched marked length spectrum. These descriptions do not establish that either observation map is a coarsening of the signed channel-law map, or conversely. The manuscript now refrains from claiming such a reduction. I found no basis in this bounded check for a priority refutation or an automatic superiority claim. [L1, L3]

Meister–Reiss already provide nonregular-regression equivalence with Poisson boundary experiments. Thus a Gaussian/Poisson contrast alone is not a new principle; the billiard-specific laws, retained-record distinctions and transfer kernels must carry the additional contribution. This work is cited in the manuscript, so there is no allegation of concealed precedence. [L4]

My remaining significance reservation is an evaluation, not an instruction to manufacture a stronger theorem. The nonlinear relative law and its contact inverse are the strongest case. Compact-injection consistency, the final lattice equation, and the long-flight restriction in a noiseless position experiment should not be offered as independent reasons for a top-level general-journal placement. The revised proof-architecture subsection is a substantial improvement in this respect. A completed native submission should make it possible to evaluate the main mechanism and its supporting arguments as one article. Neither another version number nor an additional finite diagnostic count answers that editorial question. This literature check is bounded, not an exhaustive novelty survey.

## 8. Required resubmission and final disposition

**C2 remains open on actual retrieved evidence.** For the exact reviewed commit the queried Actions endpoint returns run `34759179999`, marked failed. Job `103728806195` has an empty step list, runner identifier zero, and no named runner. The artifacts endpoint returns zero artifacts. This is not an observed TeX compilation failure: no TeX command is shown as having executed. Nor does it establish that a separate unobserved local build was impossible or unsuccessful. It does establish that this hosted attempt cannot close the requested complete-delivery item. [S14]

To close C2, provide the complete native main and companion in a durable retrievable package, with the exact source commit and recursive input identities, actual build commands and tool versions, return codes, raw logs, recorder evidence, generated cross-document auxiliary provenance where used, and an inspection record for the resulting PDFs. Correct unresolved references, missing material and obstructive layout defects if found. No such typeset defect is asserted here without a PDF. A release or artifact archive is acceptable; this request does not require committing every binary to Git. A fixture, a companion alone, or source-preservation tests are not the complete main.

To close R39-I1, update both current entries to the actual revision and add one response/evidence entry keyed to the immediately preceding report. Distinguish newly executed checks from inherited records, preserve the earlier files, and give actual output links rather than workflow intentions. The current native entry and its surrounding navigation should not disagree by three revisions. [S04–S05]

The mathematical repairs recognized above should be retained. No arbitrary deletion of proofs, change to a richer intrinsic datum, additional registration hypothesis, or abandonment of the programme is requested. For an actual submission, the substantive theorems must remain assessable independently of the author-requested review history; the current acknowledgment correctly identifies that history as such.

**Final recommendation: major revision, with no acceptance recommendation and a concrete delivery hold.** The central arguments inspected here have not produced a new fatal counterexample, but this is not a certificate for the unexamined remainder or a promise of acceptance once the files compile. The next revision should deliver the complete source-matched article and close the already identified documentary items, rather than treating improved presentation as completed delivery.
