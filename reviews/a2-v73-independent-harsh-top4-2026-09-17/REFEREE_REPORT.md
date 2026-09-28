# Independent referee report on A2, revision 73

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment, not a commissioned journal report, an editorial decision, or a formal proof certificate. The previous report is part of the revision history, not authority for the conclusions reached here.

## 1. Recommendation and immutable object of review

**I do not recommend acceptance at the requested highest general-journal level in the present form. The new complete-invariant theorem and joint finite-preparation estimate survive the examination described below: I establish no new fatal mathematical error or mandatory repair of their core proof. Revision 73 makes a genuine, accurately delimited addition by recovering the free cell area from the charged record. My negative placement recommendation concerns the demonstrated mathematical weight of the combined contribution, not an invented missing lemma.**

The distinction matters. The manuscript is not refuted by the fact that its observations are marked and local, or by the fact that its statistical construction is not computationally efficient. Those are stated features of the theorem. Equally, a correct classification and another successful compilation do not compel a top-four recommendation. I explain the mathematical findings and placement judgment separately.

| Object | Immutable identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Source branch | `revision/a2-v73-complete-local-invariant-2026-09-17` |
| Examined source commit | `3b1e7ce971cf84c8eed10a0077914f43b1b7ca68` |
| Source tree | `365e1dca5b91f066762761d2364ed066c2e74d2a` |
| Native-products branch | `revision/a2-v73-native-products-35177253679-1` |
| Native-products head; parent selected for this review | `70b0e466bdd2615381e007ed73b1576aaa21f3a0` |
| Native-products tree | `b50be37fed461ea2cbc25cd1aa54d0002336ea06` |
| Preceding v72 report commit | `c6715aff47ad6e8180acfa7ba229fd680e795293` |

The operative manuscript directory is `papers/A2-v17-boundary-information-coarsening/`; its historical directory name does not identify the current revision. Connected branch searches identify v73 as the latest revision found, including a repeated search for v73 and an empty search for v74. The comparison from the source commit to the native-products head contains only delivery additions, not manuscript changes. The comparison from the preceding report to that head identifies the new v73 section and the limited edits to the v72 section. [G1]

The committed author-generated `pdfinfo` transcripts describe a **183-page principal article** and a **359-page full technical entry**. These are overlapping entries, not 542 pages of independent contributions. This review uses pinned TeX labels and file locations rather than claiming freshly verified PDF page locators. [D1]

### Scope of fresh examination

I read the entire new complete-record section and its introductory theorem, the current main introduction, the complete revised single-law section, the response, observation ledger and literature note. I re-examined the complete periodic relative/physical-law, smooth-contact, sampled-recovery and local-completion modules; the quadratic inverse through source line 230; and the periodic contact-inverse source through line 690. In particular, this examination reaches the holomorphic half-line construction and complete analytic Banach inverse, beyond the prefix audited in the previous report. [S1–S11]

That last extension does **not** certify every later analytic statement: the real-to-disc lemma invoked by the conditional analytic continuation estimate was not freshly audited here. The later global registration/lattice, moving-family, older information/acquisition catalogue and companion proofs have not received a new complete line-by-line audit. I do not convert their retention into mathematical verification.

Nor did this session independently retrieve the binary PDFs/ZIP, rebuild the manuscript, verify their hashes, or render their pages. A direct container Git retrieval failed at host resolution; connected text access supplied the examined sources. Author-generated delivery transcripts are identified as such. The independently executed computations in Section 8 concern mathematics, not PDF provenance or layout.

## 2. Disposition of the preceding report

The response correctly says that the v72 report found no new fatal error in its examined core. It does not pretend that an unrequested theorem is a repair of a nonexistent contradiction. The two concrete mathematical presentation suggestions were implemented:

* The finite-flight mixed-log clock now includes both the reference-twist term and the amplitude correction, with no unsupported sign assertion.
* The class-dependent sufficient order condition `6a^m/(1-a^m)<1` is printed directly in the joint smooth-rigidity statement, rather than left to an inherited reference.

Both changes are appropriate. The unknown-offset, signed-anchor, actual-smooth and charged-sampling arguments remain operative. The six earlier v64–v71 proof modules used by the core have no changes in the connected comparison. The new v73 work must nevertheless be judged on its own, especially where area recovery magnifies curvature error. [R1, S2, G1]

The corrected planar lens comparison remains answered within its stated observation model. I do not reopen it as a missing comparison, nor require unmarked recovery, noisy tags, a single unreset trajectory, minimax optimality or whole-table smooth rigidity as repairs of the present theorem.

## 3. Examination of the new mathematics

### R73-M1. The central area identity is exact, but uses the specified phase preparation

**Locations:** `prop:v73-area-anchor`, `eq:v73-area-anchor`; physical formula `eq:v71-local-measure`. [S1, S8]

Suppress the phase index. The success subdensity is

$$
\rho_N(u,v)=\frac{D_N}{2\pi\mathcal A}\,\beta_N(u,v)r_N(u,v),
\qquad r_N=d-E_N+pu-pv,
$$

on the positive gate. By definition, `beta_N(0,0)=1`; the reference stationary orbit gives `E_N(0,0)=0`. Since the conditional density is normalized on that **same gate**, `rho_N=pi_N f_N`. Therefore

$$
\pi_Nf_N(0,0)=\frac{D_Nd}{2\pi\mathcal A},
\qquad
\mathcal A=\frac{D_Nd}{2\pi\pi_Nf_N(0,0)}.
$$

No asymptotic replacement occurs in this identity. The graph-coordinate change has derivative one at the origin, so it does not insert a missing central Jacobian. The positive orientation of the returning mixed twist has already been fixed by the signed Jacobi construction. The exact time-split argument, including the adjacent free-flight margins, is essential to its normalization. [S3, S4]

There is no circular curvature oracle here. The limiting laws first identify the fixed offsets and the actual contact germs. Their second derivatives determine the positive Jacobi operator and hence the **finite** reference twist. With those quantities identified, one finite experiment's success mass and central density determine the area.

The alternative prefactor is also correct:

$$
\lim_n\frac{\pi_{nP}}{D_{nP}}
 =\frac{d}{2\pi\mathcal A f(0,0)},
\qquad
\lim_ne^{n\chi}\pi_{nP}
 =\frac{d\sinh\chi}{\pi\mathcal A(\mathcal M_b)_{12}f(0,0)}.
$$

Only the **prefactor**, not the decay exponent alone, identifies area. The text explicitly declines to interpret an infinite limit as a finite-sample observation.

**Finding:** the exact anchor and its reconstruction order are supported. Its elementary character should be acknowledged, as the response already does. Its validity depends on normalized unit-speed Liouville resetting and the exact observation protocol; it is not a volume formula for an unknown preparation law.

### R73-M2. The complete-invariant statement has both directions, with the correct germ convention

**Location:** `thm:v73-fibers`, its following completion and adaptive-record paragraphs. [S1, S8]

The stated invariant is

$$
\mathfrak I(T,d)=\bigl((F_b^T)_b\text{ as actual germs},(d_b)_b,\mathcal A(T)\bigr).
$$

For the forward implication, equal charged records give equal positive success masses and conditional densities. Taking the relative limits supplies the v72 single-law inverse at every physical phase, which identifies offsets and actual contacts. The Jacobi normalizations then coincide. The central finite subdensity identifies the remaining area. This is a genuine identification of a geometric scalar not determined by the conditional law.

For the reverse implication, equal contact germs must be represented on common collars. The gates must be shrunk so the stationary bridges remain on those collars and the endpoint segments retain common clear tubes. The finite variational problems, mixed twists and physical residuals then agree. Their only remaining full-phase normalization is the common area. Hence the success submeasures and the failure atoms agree exactly, not merely in a long-flight limit.

This is why the word **germ** cannot be dropped. Equality of contact germs says nothing about endpoints outside their common representatives. The manuscript distinguishes a newly specified smaller gate, with its own normalization, from restricting a density already normalized on a larger gate. That distinction is sufficient for the stated converse.

The remote deformation argument is also used in the correct direction. A bump outside all relevant collars and tubes can change area while preserving the conditional experiments. A second disjoint bump, with nonzero area derivative, supplies an exactly compensating area correction. Thus there are nonconstant actual completions with the same full charged local record. This proves neither determination of remote profiles nor equality of complete exterior data.

The extension to a fixed finite adaptive composition is a consequence of equality of the one-step record kernels, conditional on the common past. It requires the same record-based setting rule and independent auxiliary randomization. It is not an assertion that this invariant is a sufficient statistic extracted exactly from one finite sample.

**Finding:** no missing implication is established. The classification is a valid synthesis of the smooth inverse and locality. The new geometric information beyond conditional laws is one volume scalar, not newly recovered remote boundary arcs.

### R73-M3. The logarithmic normalization estimate retains the necessary flight factor

**Location:** `lem:v73-log-twist`. [S1, S3]

With fixed flight lengths and positive curvatures,

$$
Q_i(c_i)=\begin{pmatrix}1+2c_i/k_i&1/k_i\\2c_i&1\end{pmatrix},
\quad
D_{nP,b}=\frac{\sinh\chi}{(\mathcal M_b)_{12}\sinh(n\chi)}.
$$

Taking a logarithm and differentiating gives precisely

$$
\nabla\log D_{nP,b}
=\{\coth\chi-n\coth(n\chi)\}\nabla\chi
 -\nabla\log(\mathcal M_b)_{12}.
$$

On a compact positive box the trace is uniformly greater than two, the off-diagonal monodromy entry has a positive floor, and their derivatives are bounded. Integrating this gradient on the segment between two curvature vectors yields

$$
|\log D_{N,b}(\widetilde c)-\log D_{N,b}(c)|
 \le C(1+N)\|\widetilde c-c\|_\infty.
$$

The factor cannot simply be replaced by a constant independent of flight count: along a path with nonzero `dot chi`, the derivative divided by `n` tends to `-dot chi`. Increasing one curvature gives a positive trace derivative in the positive transfer product. This argument concerns sensitivity of this normalization, not a lower bound for every possible statistical estimator.

Independent cofactor/transfer tests and differentiated matrix-product tests support the signs, factor of two in the masses, returning-period convention and derivative formula. In the homogeneous diagnostic with `k=1`, `c=1/2`, `P=6`, the normalized logarithmic derivatives approach approximately `-5.366563146`; their distances at `n=10,100,1000` are `0.12,0.012,0.0012`. This is a diagnostic illustration of the analytic formula, not its proof.

**Finding:** the sensitivity estimate is correct under its compact positive-class hypotheses. The author does not suppress the flight factor or misidentify it as minimax optimality.

### R73-M4. The finite-record stability argument does not substitute a C0 profile error for curvature control

**Location:** `prop:v73-finite-record-stability`. [S1, S2, S5, S6]

Set

$$
\Delta_f=\max_b\|f_{N,b}^{\vartheta}-f_{N,b}^{\widetilde\vartheta}\|_{C^m(Q)},
\quad e_N=\Delta_f+e^{-\omega N},
\quad \Delta_\pi=|\log(\widetilde\pi_{N,b_0}/\pi_{N,b_0})|.
$$

For nearby realizable finite records, the forward comparison bounds the limiting-law distance by `Delta_f+2C_0 exp(-omega N)`. The fixed-slice inverse controls the **actions in C^m**, not just the profiles in C0. Its second derivatives, followed by the global positive quadratic inverse, give curvature error at most `Ce_N`. This intermediate control is indispensable: a C0 profile estimate alone would not control the reference twist.

Taking the logarithm of the exact area identity for the two actual candidates gives

$$
\log\frac{\widetilde{\mathcal A}}{\mathcal A}
=\log\frac{D_N(\widetilde c)}{D_N(c)}
 +\log\frac{\widetilde d}{d}
 -\log\frac{\widetilde\pi_N}{\pi_N}
 -\log\frac{\widetilde f_N(0,0)}{f_N(0,0)}.
$$

The positive offset and density floors control the second and fourth terms; R73-M3 controls the first. The claimed area bound follows. No absolute error is divided by an exponentially small twist. An area upper bound suffices to convert logarithmic area distance into absolute area distance between the two bounded candidates. An extra area lower bound is not required for that particular conversion.

The common stability collar, fixed derivative order and small-error threshold remain necessary. The text retains them, including the sufficient condition `6a^m/(1-a^m)<1` on the enlarged positive quadratic class.

**Finding:** the finite-to-limiting-to-geometric interface is supported. The proof does not lose the curvature estimate required by its new output.

### R73-M5. The selected area really belongs to the selected table

**Location:** `eq:v73-record-image` and the estimator preceding `thm:v73-charged-invariant`. [S1]

The fitted image is

$$
\mathcal J_N(T,d)=((f_{N,b}|_Q)_b,\log\pi_{N,b_0})
 \in C^m(Q)^r\times\mathbb R.
$$

This is a change from fitting only the limiting conditional laws and subsequently attaching an independent area number. A countable dense subset of this **finite realizable image** is selected, retaining an actual table–offset representative for every point. The first representative within `n^{-2}` of the infimum is measurable. It exists without compactness of the parameter class or attainment of an exact minimum. Separability of the finite C^m product is sufficient; it is not an effective enumeration theorem.

Consequently the profile, offsets and area output by the estimator belong to one actual pair. The comparison theorem is applied only between that pair and the true pair. Arbitrary kernel estimates, which may even be negative, are never asserted to define a billiard or an exact factor model. If the count condition fails, a fixed actual representative is returned. This defines an estimator on all records under the theorem's design conditions.

**Finding:** the realizability issue is properly handled. It would be wrong to demand a closed or compact image merely to justify this approximate countable selector. It would also be wrong to advertise the selector as a computational reconstruction procedure; the author does not do so.

### R73-M6. Counts, density derivatives and charged budgets are combined consistently

**Locations:** `thm:v73-charged-invariant`, `cor:v73-budget`; inherited `lem:v69-density-estimation`. [S1, S7]

There are `B` independent resets per phase and `rB` charged preparations in total. With `q_N=c_0 exp(-Gamma N)` and `n=floor(Bq_N/2)`, the binomial comparison ensures enough successes in all phases on the stated good count event. Bernstein's inequality yields

$$
|\log\widehat\pi-\log\pi_{N,b_0}|
 \le C\sqrt{\frac{\log(4r/\zeta)}{Bq_N}},
$$

when the relative count error is at most one half. The sufficient-count condition makes this step legitimate; logarithms of zero counts are not silently used.

Independent resetting admits a Bernoulli/conditional-mark representation. An infinite extension of its mark sequence justifies applying the density bound to the first `n` successes; the good count event ensures that the actual estimator uses only observed successes. No independence between the count-error and density-error events is required. The union bound is enough. Bounded post-acceptance readout errors are controlled pathwise, not by assuming those errors independent.

In dimension two the interior differentiated-kernel estimate is

$$
C\left\{h^s+\sqrt{\frac{L_n}{nh^{2m+2}}}
 +\frac{L_n}{nh^{m+2}}+n^{-2}+\delta h^{-m-3}\right\}.
$$

The powers of the bandwidth are consistent with the variance, envelope and readout derivative bounds. The interior gap avoids a boundary-kernel assumption. The stipulated bandwidth gives `C{(L_n/n)^alpha+delta^gamma}`, where

$$
\alpha=\frac{s}{2(m+s)+2},\qquad \gamma=\frac{s}{m+s+3}.
$$

Because `alpha<1/2`, the count error is dominated by that upper bound in the stated `L_n/n<=1` regime. Near-minimum selection changes the comparison by at most a factor of two and its tolerance. The forward bias is added at the finite-image stability step. This yields the stated joint bound

$$
C(1+N)\{e^{-\omega N}+(L_n/n)^\alpha+\delta^\gamma\}
$$

outside an event of probability at most `2 zeta`.

The readout-dependent returning length is a useful correction to a naive area extension of the older budget schedule. Put

$$
\beta=\frac{\alpha\omega}{\omega+\alpha\Gamma},\quad
x=(L_B/B)^\beta,\quad t=x+\delta^\gamma,
\quad N=P\left\lfloor\frac{\log(1/t)}{P\omega}\right\rfloor.
$$

Then `exp(-omega N)<=exp(omega P)t`, `1+N<=C log(e/t)` and `n>=cBt^{Gamma/omega}` under the count conditions. The identity

$$
\alpha-\frac{\beta\alpha\Gamma}{\omega}=\beta
$$

gives the required sample bound and hence `Ct log(e/t)`. With a fixed positive readout floor, extending the flight count indefinitely would unnecessarily amplify a curvature error through the logarithmic normalization. The new schedule stops that amplification. The older profile-and-offset result remains separately available without this area-related logarithm.

**Finding:** the charged rate and noise-dependent schedule are supported as sufficient, class-dependent upper bounds. No optimality, efficient search, free accepted samples, uncertain tags or unknown preparation distribution is established or claimed. The explicit conditions cannot be dropped merely by writing the asymptotic rate.

### R73-M7. The finite clock clarification is correct and is not the area identity

**Location:** `eq:v73-finite-clock` in the retained single-law section. [S2]

At the origin, `r_N=d`, `r_{N,u}=p`, `r_{N,v}=-p` and `r_{N,uv}=D_N`. Consequently

$$
\partial_{uv}\log f_N(0,0)
 =\frac{p^2}{d^2}+\frac{D_N}{d}
   +\partial_{uv}\log\beta_N(0,0).
$$

The last term has no general sign asserted here. Relative C2 convergence and positive floors supply the finite plug-in clock's exponential bias bound. The exact limiting mixed derivative is not being substituted into a finite experiment. Conversely, the new **central value** area anchor is exact at finite flight count. It is important not to conflate these two statements.

The independent polynomial-action diagnostics retain the identity between the mixed action derivative and the chosen amplitude, and verify this correction exactly. They are algebraic tests, not claimed billiard realizations.

## 4. Re-examination of the inherited mechanism

The v73 conclusions are not consequences of their short scalar algebra alone. The inherited arguments must remain part of the mathematical assessment.

**Relative physical normalization.** The cofactor identity cancels the exponentially small reference twist before taking logarithms of the nonlinear determinant. The Hessian perturbation is trace class with end-localized size bounded independently of flight count. The proof separates the two ends using finite/half-line Green comparisons and a middle cutoff, and controls the logarithmic determinant through a convergent trace expansion. Fixed derivatives introduce polynomial losses absorbed by strict exponential margins. This is the right mechanism; dividing an absolute action error by the success probability would not be a substitute. The actual first/last free-segment margins justify the time-split interval appearing in the phase measure. [S3]

**Global quadratic and signed higher-order identification.** The Schur equation

$$
s_i=k_i+c_i-\frac{k_i^2}{k_i+c_{i+1}+s_{i+1}}
$$

is inverted by a strict contraction on the nonnegative orthant; positivity of the fixed point characterizes the strictly positive curvature image. Thus local nonsingularity is not being mistaken for global injectivity. The higher-order blocks retain the signed cyclic products at odd degrees. Doubling the oriented period does not create twice as many independent physical germs or permit erasing those signs. [S4, S5]

**Actual smooth separation.** The decisive estimate is for actual functions after sufficient jet alignment:

$$
\mathcal S(G)-\mathcal S(F)=\overline\alpha(G-F)+K(G-F),
\quad \overline\alpha\ge\tfrac12,
\quad \|\overline\alpha^{-1}K\|_{m,R}\le\frac{6a^m}{1-a^m}<1.
$$

The multiplicative constant one in `|x_j(u)|<=a^j|u|` is obtained from successive one-step contraction and uniqueness of shifted half-lines. Equal jets make the weighted norm finite; equality of the **full action functions** then makes the difference vanish. The proof does not make the false inference that equal smooth Taylor series determine a smooth germ. For approximate data the finite-jet polynomial correction is introduced before applying the weighted Taylor remainder. [S6]

**The additionally examined analytic Banach inverse.** The holomorphic construction avoids an unbounded boundary differentiation on `H^infinity(D_R)`: stationarity uses the initial graph value at the external endpoint, while differentiated graph values occur at protected interior arguments. Schwarz and Cauchy estimates provide the contracted visits on a smaller disc. The derivative inverse is obtained by inverting a sufficiently high vanishing tail and a finite lower-jet quotient, not by inferring boundedness of an infinite triangular inverse from its diagonal blocks. This supports the local analytic inverse as examined. It does not establish unrestricted analytic continuation or a global quantitative table inverse. [S4]

These findings strengthen the positive assessment of the actual mathematical mechanism. They do not certify every retained theorem in the principal and technical entries.

## 5. Observation qualifications and independent negative controls

Two useful failure tests sharpen the theorem without refuting it.

**Gate normalization.** Let `Z_+` be the integral of the unconditioned numerator on the success gate and `Z_0` its integral on a strictly smaller interior gate. Combining the success probability for the larger gate with a density renormalized on the smaller gate gives

$$
\mathcal A_{\rm wrong}=\mathcal A\frac{Z_0}{Z_+},
$$

not the true area. The sixteen exact negative controls in the attached script detect this error. The manuscript avoids it: the finite estimator restricts densities without renormalization, whereas the germ experiment changes the gate and the experiment together. This is a successful safeguard, not a newly missing hypothesis. [S1, S11]

**Unknown acceptance efficiency.** Outside the theorem's exact-tag model, suppose successes are independently hidden with an unknown constant efficiency `epsilon`. The observed success subdensity has multiplier `epsilon/A`; the conditional density is unchanged. The area formula would identify `A/epsilon`, not `A`. This is an observation-model confounding identity, not a counterexample among the stipulated exact records. No noisy-tag extension is required to repair the present theorem.

The second control also explains a wording point. “Without a flux model” should be understood as **without supplied endpoint amplitudes or a separately calibrated local flux factor**. Recovery of the global area still uses the explicitly specified normalized Liouville preparation and exact success protocol. The displayed assumptions are clear, so this is a nonblocking wording clarification rather than an omitted assumption.

“One law” likewise remains a complete two-variable distribution per marked phase, not a single number or trajectory. The recovered fixed offset does not erase the supplied polygon, physical momentum, coordinates, gates or reset protocol. The text generally maintains these distinctions; they should remain visible in any abstract or cover-letter summary.

## 6. Primary-literature comparison and exceptional significance

### R73-E1. The external comparisons remain comparisons of different data

I revisited the primary records for Noakes–Stoyanov, Bálint–De Simoi–Kaloshin–Leguil, De Simoi–Kaloshin–Leguil and Finamore–Leguil. For the last I also checked the HTML definition/statement interface of the enriched spectrum and Theorem A. This is a bounded statement-level check, not an audit of their proofs or an exhaustive priority search. [L1–L4]

The Noakes–Stoyanov record explicitly supplies the planar correction; its exterior-data result cannot be invoked as an unqualified theorem in arbitrary dimension. The Bálint–De Simoi–Kaloshin–Leguil result reconstructs two-periodic curvature and periodic Lyapunov information from marked lengths in its open-billiard setting. The analytic determination result of De Simoi–Kaloshin–Leguil retains its symmetry and genericity setting. Finamore–Leguil's Theorem A concerns diffeomorphic finite-horizon Sinai tables with the same **enriched** marked length spectrum, which includes additional geodesic information rather than just the ordinary periodic billiard lengths. [L1–L4]

These checks support the manuscript's qualified comparison. They do not show that its local conditional-law theorem is already known. They also do not establish same-data superiority, removal of assumptions from those different inverse problems, or exhaustive novelty clearance. The v73 response does not make those stronger claims.

### R73-E2. The added invariant is substantive but its new mechanism is limited

I give the revision credit for a real distinction: conditioning loses a global scalar, and the charged record recovers it. The theorem proves the converse and exhibits nontrivial fibers rather than merely listing quantities that can be estimated. The finite construction has been adjusted coherently so all outputs belong to one actual table and rare-normalization sensitivity is propagated. It is not cosmetic renaming.

Nevertheless, the new identification follows from three already operative ingredients: the exact central phase-volume density, v72 conditional identification, and v71 locality. Once these are available, the area coordinate is obtained by one division, and the converse is the existing locality calculation with its area factor fixed. The logarithmic sensitivity is differentiation of the explicit monodromy formula. The estimator uses classical density/count concentration and countable minimum-distance selection, with a carefully handled new finite-image interface.

That is a useful completion of this inverse experiment; it is not a new general mechanism of volume recovery, a new remote-shape rigidity theorem, or a new theory of statistical inversion. The response acknowledges this. The exceptionally significant part of the case must therefore remain the **combined relative physical-law and actual functional-inverse mechanism**, not multiplication of these closely dependent corollaries into separate breakthroughs.

### R73-E3. Why I still withhold the requested recommendation

The combined mechanism has genuine mathematical content: it preserves information at an exponentially rare scale and separates actual smooth germs, including flat differences. My reservation is not that these statements are false or that rich local observations are automatically unworthy of a general journal.

Rather, the manuscript demonstrates that mechanism within a tightly specified, phase-resolved local experiment around a supplied polygon. The new classification exactly describes that experiment's equivalence classes, but does not enlarge the observed geometric region beyond a normalization scalar. The preparation theorem makes the law accessible under its differentiated geometric priors, yet the resulting rate remains a sufficient class-dependent bound and the inverse remains an existence construction on a realizable image. These stated limitations are relevant to the weight of the contribution even though they are not defects in its logic.

In my judgment, the case presented still does not establish the exceptional breadth or conceptual impact needed for an affirmative recommendation at the requested highest general-journal level. A specialist or editor could weigh the synthesis more favorably; this report is not evidence of a consensus. I do not infer lack of originality, mathematical futility or a need to abandon the target from this judgment.

There is **no concealed mandatory research checklist** here. I do not require a minimax lower bound, a practical enumeration algorithm, loss of all marks, imperfect acceptance tags, an unreset observation model or whole-table smooth determination. Such results would change the problem. A further response may defend the significance of the proved mechanism; it need not manufacture another mathematical addition solely to label a placement reservation “closed.” No deletion or arbitrary reduction of valid scope is requested.

## 7. Concrete presentation and delivery findings

### R73-P1. The advertised review-ready entry is absent at the reviewed delivery head

At the immutable source and delivery state, the root `README.md` still announces **revision 72** and routes the current referee entry to `A2_REVISION_V72_REVIEW_READY.md`. The current manuscript-subtree README announces v73 and says that `A2_REVISION_V73_REVIEW_READY.md` identifies the native products and final reading branch. A direct connected fetch of that exact root path at `70b0e466bdd2615381e007ed73b1576aaa21f3a0` returns **404**. [D2]

This is a concrete routing discrepancy. A submission handoff should have one working v73 entry identifying the source commit and corresponding delivery, without sending a reader to v72 or a missing path. The manuscript and native product paths were nevertheless recoverable through the branch/commit comparison, so this discrepancy does not invalidate the mathematical proofs or establish a failed build. This review does not edit either README; the new review directory supplies its own explicit pointers.

### R73-P2. Preserve the preparation-model qualification in short summaries

The area-recovery wording should distinguish unknown local amplitudes from an unknown reset measure or unknown acceptance efficiency, as explained in Section 5. The actual theorem already fixes the required preparation model. This is an expository recommendation, not a demand for a new theorem.

The current mathematical introduction otherwise exposes the central proof route and separates smooth local conclusions from analytic/global branches. It would be inaccurate to repeat an older claim that the main mechanism remains hidden in an undifferentiated catalogue. Page count and preservation inventories should remain delivery evidence, not substitutes for an originality or significance argument.

## 8. Independent computations and evidence limits

`independent_checks.py` was written for this review and imports no manuscript diagnostic module. It was executed with Python 3.13.5, SymPy 1.14.0 and mpmath 1.3.0, normally and with `python -O`. The JSON outputs were byte-identical. Explicit exceptions keep every check active under optimization.

The checks comprise sixteen central-anchor cases; sixteen finite-clock cases; sixteen incorrect-gate negative controls; sixteen unknown-efficiency negative controls outside the theorem's observation model; twenty-seven exact periodic cofactor/transfer comparisons, including sixteen direct Jacobi determinants; twenty high-precision derivative comparisons; a three-term homogeneous sensitivity sequence; three symbolic rate identities; thirty-six returning-budget schedule cases; and four sufficient weighted-order checks. `MATHEMATICAL_CHECKS.json` records the results.

The polynomial test actions obey the imposed mixed-action/amplitude relation, but are not asserted to arise from actual billiards. The transfer calculations test exact finite Jacobi algebra, not nonlinear geometric realization. Numerical differentiation is a diagnostic, not an interval or formal verification. The budget tests check the schedule algebra, not the unknown values of all theorem-class constants. None of these tests certifies trace-class differentiation, infinite-dimensional smooth inversion, statistical uniformity or the unaudited auxiliary results.

`AUDIT_EVIDENCE.json` records immutable sources, fresh coverage, the independently executed diagnostic hashes, the author-generated delivery metadata read, and the binary/build/layout checks **not** performed. A successful source comparison, finite test, or manuscript compilation must not be described as acceptance or full mathematical certification.

## 9. Final disposition

**R73-D1 — Examined mathematics.** The new area anchor, complete local invariant, logarithmic twist comparison, finite-image stability and jointly realizable charged estimator withstand the described review. No new fatal mathematical error or mandatory repair of that examined core is established. This is not a blanket certificate for the entire retained manuscript.

**R73-D2 — Response to the preceding referee.** Both concrete presentation suggestions have been implemented. The new consequence is genuine. Previously resolved locality and observation-comparison issues remain resolved within their hypotheses.

**R73-D3 — Requested placement.** I do not recommend acceptance at the requested top-four level, for the specific significance reasons above. That judgment is separate from theorem validity and is not a requirement to solve a different inverse problem.

**R73-D4 — Handoff and isolation.** Repair the concrete v73 entry discrepancy before a clean submission handoff. This review itself adds only its own files on a new review branch based on the pinned native-products head. It does not rewrite manuscript files, previous reports, existing revision/review branches, the default branch or repository permissions. The final connected comparison is the check of that isolation.

## Source registry

Unless stated otherwise, S-keys are under `papers/A2-v17-boundary-information-coarsening/` at source commit `3b1e7ce971cf84c8eed10a0077914f43b1b7ca68`. Git blob identifiers and fresh coverage are recorded in `AUDIT_EVIDENCE.json`.

| Key | Source and coverage |
|---|---|
| S1 | `article/10h_complete_record_v73.tex`, all 432 lines; all new mathematical statements and proofs |
| S2 | `article/10g_uncalibrated_single_law_v72.tex`, complete revised section |
| S3 | `article/10a_periodic_itinerary_relative_v64.tex`, complete module |
| S4 | `article/10b_periodic_contact_inverse_v65.tex`, lines 1–690; includes the local analytic Banach inverse; the externally invoked real-to-disc lemma was not freshly audited |
| S5 | `article/10c_global_curvature_inverse_v66.tex`, lines 1–230, quadratic global inverse and comparisons |
| S6 | `article/10d_smooth_contact_rigidity_v68.tex`, complete module |
| S7 | `article/10e_sampled_smooth_recovery_v69.tex`, complete module |
| S8 | `article/10f_local_observation_comparison_v71.tex`, complete module |
| S9 | `article/00i_main_thesis_v70.tex`, complete current introduction |
| S10 | `article/00n_record_overview_v73.tex`, complete new overview; `rigidity.tex`, active source routing |
| S11 | `journal/DEPENDENCY_LEDGER_V73.md`; `LITERATURE_CHECK_V73.md`; current manuscript README |
| R1 | `RESPONSE_TO_REFEREE_V73.md`, complete |
| R2 | `reviews/a2-v72-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md` at `c6715aff47ad6e8180acfa7ba229fd680e795293`, preceding report and dispositions |
| G1 | Connected branch/commit reads; comparisons `c6715aff...` to `70b0e466...` and `3b1e7ce9...` to `70b0e466...` |
| D1 | `deliveries/a2-v73/3b1e7ce971cf84c8eed10a0077914f43b1b7ca68/rigidity-pdfinfo.txt` and `main-pdfinfo.txt` at native head; author-generated text, not fresh PDF inspection |
| D2 | Root README at source pin; manuscript README and 404 for root `A2_REVISION_V73_REVIEW_READY.md` at native head; source-to-native comparison |

Primary literature, checked September 17, 2026:

**L1.** L. Noakes and L. Stoyanov, *Lens Rigidity in Scattering by Unions of Strictly Convex Bodies in R²*. Primary record and planar-correction qualification: https://arxiv.org/abs/1803.02542.

**L2.** P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*. Primary record: https://arxiv.org/abs/1809.08947.

**L3.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*. Primary record: https://arxiv.org/abs/1905.00890.

**L4.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*. Primary record https://arxiv.org/abs/2510.18983; HTML Theorem A and enriched-spectrum definition interface: https://arxiv.org/html/2510.18983v1. No claim is made to have audited the full proof.
