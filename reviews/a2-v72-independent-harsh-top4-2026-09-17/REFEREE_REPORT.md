# Independent referee report on A2, revision 72

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment. It is not a commissioned journal report, an editorial decision, or a formal proof certificate. The preceding report is evidence about the revision history, not authority for the mathematical verdict below.

## 1. Recommendation and object of review

**I do not recommend acceptance at the requested highest general-journal level in the present form. Revision 72 nevertheless makes a genuine mathematical improvement: for the stipulated oblique marked experiment, a single conditional law determines both unequal endpoint actions and the previously unreported positive offset. The new algebra, its fixed-order stability, the passage to actual smooth contacts, and the charged joint estimator withstand the examination described below. I establish no new fatal mathematical error and identify no mandatory repair of the examined core proof. The negative recommendation is an exceptional-significance judgment, not a disguised assertion that a missing lemma or counterexample remains unresolved.**

In particular, it would be wrong to describe this revision as cosmetic, to dismiss its inverse as a mere formal Taylor calculation, or to repeat the already answered demand for comparison with the corrected planar lens theorem. Conversely, neither a correct strengthening nor a successful build mechanically entails an acceptance recommendation at the requested level. My reasons concern the demonstrated mathematical gain and are stated separately in Section 6.

| Object | Immutable identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Reading branch | `revision/a2-v72-referee-ready-2026-09-17` |
| Reading head; parent of this review | `161ee773c42bc39db4bdb0e18aaf8d516848140b` |
| Compiled source commit | `020c8b08176617e7bfb5dc37110c5b58fef99c1c` |
| Manuscript subtree | `78fb5bad4944d0bff60e108996cca84d4473fa85` |
| Native product commit | `13af7ec64cd3f5d36d67ae6d11dac9ea1e266125` |
| Attested native-products head | `e044dffdc9380070ff6b49427f655e2cd3fd8b87` |
| Prior report | `7bb8971f6b792894ee961f6fab5c6f68847d373d` |
| Prior compiled source | `b0a0c9a42e61422cdf7c82df3fb80bedc0d105af` |

The operative manuscript directory is `papers/A2-v17-boundary-information-coarsening/`; its historical directory name does not identify the current revision. The author entry reports 176 principal pages, 352 technical pages and a seven-page companion. The committed principal `pdfinfo` transcript reports 176 pages. These are overlapping entries, not 535 pages of distinct contributions. Page locators below follow the supplied entry map; source labels and pinned files are the primary review locators. [R2, D1]

### Scope of fresh examination

I read the complete new Section 8, its introductory theorem, the current introduction, and the operative dependencies: the complete periodic relative/physical-law module; the graph-coordinate, two-offset, actual-envelope and signed finite-jet arguments through line 360 of the periodic inverse; the quadratic global inverse through line 230 of the curvature module; the complete smooth-contact, sampled-recovery and local-completion modules. I also compared the retained symmetric one-law inverse through line 215 with the new theorem, and examined the response, dependency ledger, literature note and reading entry. [S1–S10, R2]

This is **not** a fresh line-by-line audit of every retained theorem. The analytic Banach inverse beyond the examined prefix, later real-to-complex continuation, complete global registration/lattice and moving-family arguments, older coarsening/acquisition catalogue, and companion proofs remain outside this examination. Nor did this session independently download, rebuild, hash-verify or render the manuscript PDFs or frozen ZIP. The separate author-side and previous-review delivery claims are not adopted as work performed here. These limits do not mean an error has been found in the unaudited material; they mean it is not certified by this report.

## 2. Disposition of the preceding report

| Previous issue | Disposition on revision 72 |
|---|---|
| R71-M1–M7: operative mathematical interfaces and observation qualifications | Re-examined to the scope above. The six v64–v71 core modules are unchanged in the connected source comparison. No regression is established. |
| Corrected planar lens comparison and actual equal-area completion | Remain answered. The current locality proof and the corrected external theorem support the comparison. No renewed missing-citation objection is made. |
| R71-E1–E3: significance and the danger of a cosmetic moving target | The response supplies a genuinely different observation theorem. Its significance is reassessed, not presumed insufficient merely because the preceding recommendation was negative. |
| Root routing and preservation | The current entry identifies v72 and its frozen source. Git comparisons confirm that the source-to-reading commits do not alter the manuscript directory. Full archive preservation is an author verification claim, not independently repeated here. |
| Scope of independent certification | Retained explicitly. An unchanged file is not automatically a newly verified theorem. |

The new response correctly distinguishes changing the data required by the inverse from proving a new general method of factorization or statistical regularization. It also retains the normal-incidence and broader analytic routes rather than erasing them to make the new theorem look universal. [R1, R2, S10, D1]

## 3. Examination of the new Section 8

### R72-M1. Offset identification is correct, with an essential marked scale

**Location:** Proposition 8.1; `prop:v72-clock` and equations `eq:v72-model`–`eq:v72-clock`. [S2]

Write the positive limiting density, up to an arbitrary positive scalar, as

$$
f(u,v)=Z^{-1}B_-(u)B_+(v)\{d-A(u)-C(v)\},
\quad A(0)=C(0)=0,\quad A'(0)=-p,\quad C'(0)=p,
$$

where the signed nonzero momentum $p$ is supplied by the polygon, whereas $d>0$, the two amplitudes and the normalizer are not. Cancellation gives

$$
\mathcal R_f(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}
=1-U(u)V(v),\qquad U=\frac{A}{d-A},\quad V=\frac{C}{d-C}.
$$

The axis residuals are positive because positivity is imposed on the square, including its axes. Since $U'(0)=-p/d$ and $V'(0)=p/d$,

$$
\kappa_f=\partial_{uv}\mathcal R_f(0,0)
=\partial_{uv}\log f(0,0)=\frac{p^2}{d^2},
\qquad d=\frac{|p|}{\sqrt{\kappa_f}}.
$$

The sign and positive square-root branch are correct. Unknown normalization and separate endpoint factors have genuinely disappeared. A continuous density is uniquely specified by its law on the open positive square; evaluating its derivatives is therefore legitimate for exact-law identifiability. It would not be legitimate to equate this operation with observing density derivatives from a finite sample. The manuscript does not make that substitution; Section 8.3 supplies a separate statistical argument.

The retained scale is important. This is offset recovery in a marked physical coordinate system, not recovery with all scales unknown. In the abstract factor model, simultaneous scaling $(d,A,C,p,Z)$ by a common positive factor preserves $f$ when $p$ is not fixed. That observation is outside the fixed-mark theorem, and is not an actual-table counterexample. It simply makes clear why the supplied momentum matters. Likewise, the nuisance offset is fixed during repetitions and returning lengths. Random clock drift, incorrect success tags and erroneous gates are not included in this result. These qualifications are already stated in the new overview. [S1, S2]

**Disposition:** no correction established. The removal of supplied numerical offset calibration is real; the removal of all geometric calibration is neither proved nor claimed.

### R72-M2. Signed fixed anchors separate unequal actions without an additional derivative loss

**Location:** Theorem 8.2; `thm:v72-separation`. [S2]

An unanchored product $UV$ determines nonzero factors only up to $(\lambda U,\lambda^{-1}V)$. After $d$ has been recovered, the prescribed slopes force $\lambda=1$. The constructive version chooses a fixed nonzero $a$ and uses

$$
v_a=\frac d p\partial_u\mathcal R_f(0,a)=V(a),\qquad
u_a=-\frac d p\partial_v\mathcal R_f(a,0)=U(a).
$$

Both anchors are signed scalars; neither is replaced by an absolute value. The recovery formulas are

$$
U_f(u)=\frac{1-\mathcal R_f(u,a)}{v_a},\qquad
V_f(v)=\frac{1-\mathcal R_f(a,v)}{u_a},\qquad
A_f=\frac{dU_f}{1+U_f},\quad C_f=\frac{dV_f}{1+V_f}.
$$

The amplitudes follow from the axis density ratios multiplied by $1+U_f$ or $1+V_f$. The denominators satisfy $1+U=d/(d-A)>0$ and the analogous identity for $V$. The formulas remain valid through zeros of an action; there is no pointwise square root at a degenerate contact.

The stability assertion deserves explicit credit. Evaluating the second derivative of the cross ratio at one point is a bounded **scalar** functional on $C^M$ for $M\ge2$. The first derivatives used for the anchors are also scalar functionals. The recovered functions themselves use fixed-slice restrictions, which are bounded in the same $C^M$ norm. Thus this construction does not differentiate an entire recovered function along an axis and does not lose one further derivative. Products and reciprocals are locally Lipschitz with the stated floors. The open-neighborhood extension need not satisfy the physical factorization and is not claimed to produce a billiard.

The uniform anchor condition is derived rather than smuggled into the data: with $|p|\ge p_*$, a $C^2$ action bound $H_2$, and fixed $a>0$ satisfying $H_2a\le p_*$, Taylor's theorem gives $|A(a)|,|C(a)|\ge p_*a/2$. An upper bound on the axis residuals then bounds both anchor magnitudes below. The other floors follow from the positive offset interval and the physical density bounds. Constants can deteriorate as obliquity vanishes. [S2]

The historical theorem in `23f_single_offset_law_inverse_v42.tex` already uses a fixed-anchor rank-one factorization, but assumes the same action at the two ends and a known offset. It is not a theorem for unequal actions at an unreported offset. The new proof is an elementary extension of that algebraic idea with a useful new identification consequence, not its rediscovery and not a new general factorization theory. [S9]

**Disposition:** no correction established. Sixteen exact signed-anchor examples pass; replacing both anchors by their absolute values fails a marked-slope check in all sixteen negative controls. [D2]

### R72-M3. The new physical-to-smooth interface uses actual functions

**Location:** Theorem 8.3; `thm:v72-rigidity`; inherited Theorems 5.3 and 5.5. [S2, S4, S6]

In the measured graph coordinates the actual physical actions are $A_b=S_b^- -p_bu$ and $C_b=S_b^++p_bv$. Recovering $A_b$ and adding the known linear term supplies the future action used by the smooth inverse. No unknown normal graph height or unknown arclength conversion is inserted as observation data. This interface is exact for the limiting law.

The final step is not the false implication that equal Taylor series determine a smooth function. The inherited proof first uses global positive quadratic inversion and signed higher-order blocks to identify contact jets. For the actual difference $h=G-F$, the integrated envelope then gives

$$
\mathcal S(G)-\mathcal S(F)=\overline\alpha h+Kh,
\qquad \overline\alpha\ge\tfrac12,
\qquad
\|\overline\alpha^{-1}K\|_{m,R}\le\frac{6a^m}{1-a^m}<1.
$$

The constant-one visit estimate $|x_{b,j}(u)|\le a^j|u|$ follows from one-step contraction and uniqueness of shifted actual half-lines. Flatness makes the weighted norm finite, but equality of the complete actions is used again to force $h=0$. This is the step detecting a nonzero flat perturbation. A merely formal coefficient inverse would not suffice.

For stability, finite-jet polynomial alignment is made before the weighted norm is applied. The action-level estimate therefore accepts the $C^m$ actions produced by Theorem 8.2 and yields the claimed $C^0$ profile error together with scalar offset error. The integer $m$ is the sufficiently large order chosen for the inherited bounded positive class; it is not a claim that arbitrary $m=3$ works uniformly over all hyperbolicity margins. Since that order is already at least three, the order-two clock functional introduces no further loss.

The flat-contact construction is also used correctly. Equality of the new law tuple, even with candidate offsets initially different, first forces equal offsets and then equal actual smooth germs. This distinguishes the inherited flat contact family. It does not recover remote smooth boundary arcs; identical contact collars with the same offsets retain the exact locality property. [S6, S8]

**Disposition:** the new theorem connects to the operative smooth inverse with the required hypotheses. No circularity or Taylor-series substitution is established.

### R72-M4. The first-hit argument gives the claimed obliquity coverage

**Location:** Lemma 8.4; `lem:v72-obliquity`. [S2]

At a normal reflection, the outgoing ray is the previous incoming ray in reverse. Because that open flight is clear, its first subsequent collision is precisely the preceding lifted contact. For a polygon with at least three distinct physical contacts, the preceding and following cyclic positions cannot therefore be distinct physical contacts, a contradiction. The word **first** is decisive: this is not a statement about an unconstrained ray extended through obstacles.

In the two-contact case, equality of the preceding and following lifted contact forces zero closing translation; periodicity makes the other reflection normal as well. The exceptional orbit is the ordinary self-retracing two-contact orbit. The ambient marked setup has at least two contacts. The proof establishes the asserted coverage without a genericity assumption.

At normal incidence the new mixed-derivative clock vanishes. This is a limitation of that formula, not a proof of non-identifiability from every conceivable normal-incidence observation. The retained known-offset symmetric and two-known-offset results have not been invalidated. Oblique two-contact configurations are not excluded by the new theorem when its hypotheses otherwise hold.

**Disposition:** no correction established.

### R72-M5. A finite-flight clock correction makes the limiting qualification testable

**Locations:** physical law `eq:v64-phase-density`; Proposition 8.1 and the forward estimates in the proof of Theorem 8.5. [S2, S3]

An independent differentiation gives a useful exact check not needed as a new assumption. Suppress the phase index and put

$$
f_N=Z_N^{-1}\beta_N r_N,\qquad
r_N=d-E_N+pu-pv.
$$

At the origin, $E_N=E_{N,u}=E_{N,v}=0$ and $E_{N,uv}=W_{N,uv}=-D_N$. Hence

$$
\boxed{\partial_{uv}\log f_N(0,0)
=\frac{p^2}{d^2}+\frac{D_N}{d}
+\partial_{uv}\log\beta_N(0,0).}
$$

The same quantity is the origin mixed derivative of the anchored finite-density cross ratio. In general it is **not** exactly $p^2/d^2$. The last term has no sign asserted by this calculation. A direct finite-flight plug-in clock would therefore have a bias.

This does not contradict revision 72. Its clock identity is stated for the limiting law, and its estimator uses a differentiated finite-flight-to-limit comparison. The relative theorem controls the mixed log-amplitude term because the limiting amplitude is a product of separate endpoint functions; the exact reference twist decays as well. Equivalently, positive density floors and the $C^2$ convergence control the displayed scalar functional directly. The proof of Theorem 8.5 retains this bias inside $e^{-\omega N}$.

The accompanying independent script verifies the correction for an anchored quadratic action with mixed term $-Duv$ and an amplitude $e^{\eta uv}$. This is an algebraic diagnostic, not an assertion that arbitrary test coefficients define an actual billiard. The displayed identity itself follows directly from the manuscript's exact physical formula.

**Disposition:** no missing bias term is established in the theorem. Printing this short identity would usefully prevent a common misreading, but it is an explanatory addition, not a mandatory proof repair.

### R72-M6. The joint charged estimator retains realizability and the rarity cost

**Location:** Theorem 8.5; `thm:v72-sampling`; inherited derivative-estimation lemma. [S2, S7]

The statistical parameter is the pair $(T,d)$, with one fixed nuisance offset per phase. Uniformity in the offset is justified by its compact positive range, its affine occurrence in the physical residual, and the common positive normalization integral. The exact twist and the free-area upper bound give the success lower bound in the correct direction. The proof consequently has uniform forward derivative bounds, $C^m$ finite-flight bias and success probability at least $c_0e^{-\Gamma N}$.

The derivative-kernel calculation in dimension two has variance scale $h^{-2m-2}$ and envelope scale $h^{-m-2}$. On the interior square it gives

$$
E_{n,N,h}=C\left\{e^{-\omega N}+h^s+
\sqrt{\frac{L_n}{nh^{2m+2}}}+\frac{L_n}{nh^{m+2}}
+n^{-2}+\delta h^{-m-3}\right\}.
$$

The positive-gap inclusion $Q\Subset Q_+$ avoids a boundary-kernel assumption. Densities normalized on $Q_+$ are restricted without renormalization. The error term for bounded readout perturbations is pathwise, so their independence is unnecessary; the latent endpoints, however, arise from independent resets, and the gate and itinerary tags remain exact. This is not an arbitrary-contamination theorem.

The fitted functions are not automatically physical. A countable dense subset of the realizable law image in $C^m(Q)^J$, retaining an actual pair for every point, gives a measurable near-minimum-distance selector. Its distance from the true law tuple is at most $2E_{n,N,h}+n^{-2}$. The geometric inverse is then applied only between realizable pairs, with this distance required to be at most $\eta_0$. Including the offset in the selected representative avoids attaching an unrelated numerical clock to a different reconstructed table. Noncompactness of the parameter class does not invalidate this approximate countable-image selection; the theorem does not claim an attained exact minimum or effective enumeration.

With

$$
\alpha=\frac{s}{2(m+s)+2},\qquad
\gamma=\frac{s}{m+s+3},\qquad
\beta=\frac{\alpha\omega}{\omega+\alpha\Gamma},
$$

the specified bandwidth controls the bias, stochastic and readout terms. For $B$ preparations in each of $J=r$ groups, the lower-tail bound and first-success representation produce $n_B=\lfloor Bc_0e^{-\Gamma N_B}/2\rfloor$ accepted marks per group outside an event of probability at most $\zeta$. The logarithmic returning-length choice balances $e^{-\omega N_B}$ against the effective accepted-sample term. The density-estimation event costs another $\zeta$, giving the stated error radius $C\{(L_B/B)^\beta+\delta^\gamma\}$ with total exceptional probability at most $2\zeta$.

The returning-length floor changes constants, not the exponent, under the explicit count conditions. The small-error and upper-bandwidth restrictions cannot be dropped at finite budget or varying confidence. They are present. All $rB$ resets are charged. The change from $2r$ groups to $r$ is a change in the observation design, not a demonstrated factor-two improvement of optimal total sample complexity; inverse constants and admissible classes also differ. The estimator remains an existence construction and the rate an upper bound, as stated.

**Disposition:** the amended nuisance-parameter interface and charged exponent are supported by the examined proof. No free-success accounting, arbitrary-density inversion or suppressed derivative-oracle assumption is established.

## 4. Re-examination of the inherited analytic mechanism

The preceding findings depend on substantial inherited arguments, not just the new algebra. Three checkpoints are particularly important.

**Relative rather than absolute control.** The exact cofactor identity cancels the exponentially small reference twist before the nonlinear determinant comparison. The perturbation of the Jacobi Hessian is trace class with end-localized size independent of the flight count. The proof compares finite and half-line Green operators, cuts off the middle, controls the opposite-end blocks and uses a convergent trace expansion for the logarithmic determinant. Fixed derivatives introduce polynomial factors absorbed by strict exponential margins. This supplies the relative amplitude estimate required for conditioning. An absolute action remainder divided by an exponentially rare success probability would not suffice; that invalid argument is not used. The short preceding/following free-segment margins also justify the full residual time-split interval in the actual phase-volume formula. [S3]

**Measured coordinates and global low-order identification.** The recorded graph coordinate is a supplied-frame tangent projection, not the unknown boundary height. The arclength conversion includes its Jacobian and gauge correction. In the action variation, the finite terminal contribution is retained and estimated before taking the half-line limit. The signed cyclic blocks keep the signs of the one-step contractions at odd degree. For quadratic identification, the Schur equation

$$
s_i=k_i+c_i-\frac{k_i^2}{k_i+c_{i+1}+s_{i+1}}
$$

is inverted by a strict contraction on the nonnegative orthant; positivity of its fixed point characterizes the positive-curvature image. Thus nonsingularity of a local Jacobian is not substituted for global injectivity. These facts support the absence of a candidate-closeness assumption in the smooth theorem. [S4, S5]

**Actual smooth remainder.** The weighted inverse is legitimate only after sufficient low-order vanishing is established. The source proves constant-one contraction of successive real visits and aligns finite jets before using a weighted Taylor bound for approximate data. Its operator depends on the candidate pair, appropriately for separation; it is not advertised as a directly observable algorithm. Constants and the necessary derivative order depend on the positive marked class. No uniform assertion at vanishing hyperbolicity, grazing or varying period is inferred. [S6]

These checks support the chain used by v72. They are not a certificate for unrelated retained analytic or global theorems that happen to occur in the same principal entry.

## 5. Locality and primary-literature comparison

The current local-completion argument remains valid within the specified record. Equal contact collars and common trajectory margins give the same stationary bridges and twists. Only the normalized Liouville area changes, so the success subprobability is multiplied by $\mathcal A/\widetilde{\mathcal A}$. Conditioning cancels that factor; equality of charged records additionally uses equal area. A failure is one symbol, not a rejected trajectory trace. Independent resetting is part of the experiment. [S8]

The actual remote deformation uses disjoint smooth bumps away from the contact collars and trajectory tubes. A nonzero area derivative in the compensating bump gives an exactly equal-area family by the implicit function theorem; disjoint support ensures the first bump is not canceled. Removing lattice copies gives distinct finite compact obstacle unions satisfying the corrected planar Noakes–Stoyanov hypotheses. The contrapositive of their travelling-time and scattering-length conclusions distinguishes those exterior data. I inspected the primary PDF's definitions and Theorem 1.1, including rendered pages. The dimension-two correction is not optional. [S8, L1]

This establishes that equality of the selected local record is not a substitute for equality of complete exterior data. It does not establish two-way incomparability, equality of full marked length spectra, or same-data superiority. Revision 72 does not make those stronger claims.

The other comparisons also concern different observations. Bálint–De Simoi–Kaloshin–Leguil recover two-periodic curvature and periodic Lyapunov information from marked lengths in open dispersing billiards. De Simoi–Kaloshin–Leguil treat analytic spectral determination under their symmetry and genericity conditions. Finamore–Leguil's Theorem A concerns diffeomorphic finite-horizon Sinai tables with equal **enriched** marked length spectra; its enrichment includes geodesic information beyond the ordinary billiard periodic-orbit record. The primary records of the first two and the statement/definition interface of the last were checked, not all their proofs. [L2–L4]

None of these checks proves that A2's marked conditional-law inverse is already known or follows from an existing global theorem. Equally, changing the observation does not remove hypotheses from those different-data theorems. The author's comparison is appropriately qualified; an exhaustive priority clearance is not claimed here.

## 6. Exceptional significance: the remaining negative recommendation

### R72-E1. The observation improvement is substantive, but its incremental mechanism is limited

Revision 72 should receive full credit for an additional identifiable nuisance parameter, separation of unequal actions, fixed-order stability, and a corresponding finite-preparation theorem. The result covers every clear polygon with at least three distinct physical contacts in the stated class, not merely a generic subclass. These are mathematical changes to the observation theorem. [S1, S2]

Nevertheless, the new step operates inside the already derived separable residual-law family. Once that family and its marked first derivatives are available, a mixed log derivative identifies the scale and fixed anchors separate a rank-one product. The proof is elegant, but it is not another analytic mechanism comparable in depth to the relative determinant analysis or actual smooth envelope. The new sampling theorem transports the inherited derivative-estimation and realizable-selection argument to a larger parameter. Its correctness and utility do not by themselves demonstrate an exceptional general advance.

The strongest case for this paper remains the **combined** relative-physical-law and actual-functional-inverse mechanism, now with a better observation theorem. I do not assess its significance by counting the new section as an unrelated paper, nor by treating the number of retained theorem statements or pages as independent contributions.

### R72-E2. One conditional law is still a rich, tightly specified observation

“One law” denotes an entire two-variable probability distribution per marked phase, not one number or one trajectory. The finite theorem makes that information accessible under an explicit growing reset budget, but retains the supplied polygon and frames, resolved phases, exact tags and gates, a fixed nuisance-offset range, positive geometric margins and differentiated priors. No unknown contact height is supplied, so this is not tautological boundary recovery. It remains, however, a deliberately selected local inverse experiment. [S1, S2, S7]

The new theorem removes numerical offset knowledge but not this surrounding observation structure. The complete-profile conclusion is stronger than all-order jet determination, yet local in the smooth category. The finite rate is a sufficient bound in a class-dependent differentiated topology, not an optimal resource law. These are precise features of the result actually proved, not unacknowledged defects.

In my judgment, the manuscript has not yet demonstrated why this particular synthesis, with this observation structure, has the exceptional reach warranted by the requested highest general-journal placement. That is a judgment of mathematical weight, not a proof that rich-data local inverse problems cannot merit such placement. A specialist or editor could reasonably weigh the synthesis more favorably. This report supplies no authority for a claim of consensus, a theorem of unpublishability, or a conclusion that the program should be abandoned.

### R72-E3. Do not convert this judgment into an invented repair checklist

I do **not** make a minimax lower bound, an efficient global search, noisy-tag robustness, recovery from an unreset trajectory, removal of all marks, or determination of the whole smooth table a mandatory repair. Those would be separate research results. Their absence is not a contradiction in the present theorem. The corrected lens comparison is already adequate and should not be reopened as a missing task.

A further response should defend the significance of the demonstrated mechanism or develop a genuinely relevant consequence, rather than generate another cosmetic version whose only purpose is to re-label an editorial reservation as closed. The present revision has already supplied a genuine consequence. The reason I still withhold a top-four recommendation is stated above; it is not a hidden demand to continue indefinitely until an unspecified number of revisions has been reached. No deletion or reduction of valid mathematical scope is requested.

## 7. Presentation and evidence quality

The current introduction exposes the main proof interfaces and distinguishes smooth contact recovery from analytic/global branches. The new dependency ledger already distinguishes supplied, observed and reconstructed quantities. It would be inaccurate to repeat the old claim that the main argument is buried behind an undifferentiated catalogue. [S1, S10]

Two nonblocking clarifications would improve the new section. First, restate the inherited condition $6a^m/(1-a^m)<1$ alongside the new joint stability theorem, so that its reference to a bounded class cannot be skimmed as an assertion for every $m\ge3$. Second, include the finite-flight identity in R72-M5 to make the calibration bias visible next to the exact limiting formula. These are expository suggestions, not newly discovered gaps. The larger retained material can remain available without being counted repeatedly in the novelty argument.

### D1. What was independently verified about delivery

Connected branch and commit reads locate v72 and pin the source. The comparison from the v71 compiled source to the v72 source reports six intervening commits and no change to the six operative v64–v71 mathematical modules. The comparison from the v72 compiled source to the reading head reports three delivery/index commits and no changed path in the manuscript directory. New Section 8 is active in `rigidity.tex`. These are source/Git checks.

The author entry describes native builds, archive reconstruction, hash checks, all-page render equality and selected visual inspection. I did not reproduce those operations in this session. Container network retrieval was unavailable and binary products were not retrieved through the text connector. Consequently this report makes no new all-page layout claim, source-ZIP hash certification, native compilation certification, or PDF-byte comparison. The prior report's separate reconstruction is not silently presented as our own. This limitation is not an allegation that the retained delivery is defective.

### D2. Independent finite mathematical checks

The attached `independent_checks.py` imports no manuscript diagnostic module. It was executed with Python 3.13.5 and SymPy 1.14.0 both normally and with `python -O`; its JSON outputs were byte-identical. Explicit exceptions keep the tests active in optimized mode. Checks include 16 unequal-action/signed-anchor cases, 16 absolute-anchor negative controls, 12 signed cyclic inverse/determinant cases, nine exact Jacobi cofactor/transfer comparisons, the general cross-ratio identity, vanishing of the normal-incidence clock, the finite-flight mixed-log correction, the unfixed-scale model identity, and the rarity/readout exponent balances.

The rational test laws have verified positive residual and amplitude bounds on their square. They are factor-model tests, not asserted geometric realizations. The tests do not certify nonlinear localization, trace-class differentiability, infinite-dimensional smooth inversion, statistical uniformity or any unaudited theorem. `MATHEMATICAL_CHECKS.json` contains the results; `AUDIT_EVIDENCE.json` records the precise coverage and delivery limits.

## 8. Final disposition

**R72-D1 — Examined mathematics:** no new fatal error or mandatory proof repair is established. The positive findings concern the specified hypotheses and reviewed dependencies, not a blanket certification of the entire repository.

**R72-D2 — Revision response:** the unknown-offset single-law result is substantive; the old symmetric inverse does not already give its full statement. The previously closed planar comparison and locality issues remain closed.

**R72-D3 — Requested placement:** I withhold a recommendation of acceptance at the requested top-four level on exceptional significance. This is a transparent editorial-style judgment, not theorem falsification or a requirement to solve a different inverse problem.

**R72-D4 — Delivery and preservation:** this review adds only its own files on a new branch based on the pinned v72 reading head. It does not edit the manuscript, prior reports, native delivery, default branch, existing revision/review branches, or repository permissions. A final connected comparison should be used to verify that isolation.

## Source registry

All S-keys are under `papers/A2-v17-boundary-information-coarsening/` at reading head `161ee773c42bc39db4bdb0e18aaf8d516848140b`. The source-to-reading Git comparison shows no manuscript changes relative to compiled source `020c8b08176617e7bfb5dc37110c5b58fef99c1c`. Blob identities and coverage are also recorded in `AUDIT_EVIDENCE.json`.

- **S1:** `article/00i_main_thesis_v70.tex`, complete current introduction; `article/00l_one_law_overview_v72.tex`, lines 1–57, Theorem 1.3.
- **S2:** `article/10g_uncalibrated_single_law_v72.tex`, lines 1–386, complete new Section 8. Author page map: principal pp. 42–46.
- **S3:** `article/10a_periodic_itinerary_relative_v64.tex`, lines 1–549, complete relative, physical, transmission and realization module.
- **S4:** `article/10b_periodic_contact_inverse_v65.tex`, lines 1–360; coordinates, law separation, actual envelope and finite signed blocks. Later analytic arguments are not included in this coverage.
- **S5:** `article/10c_global_curvature_inverse_v66.tex`, lines 1–230; actual Schur characterization and global positive quadratic inverse. Later global/finite-iteration arguments are outside this prefix review.
- **S6:** `article/10d_smooth_contact_rigidity_v68.tex`, lines 1–445, complete actual smooth inverse, finite-order stability and flat family.
- **S7:** `article/10e_sampled_smooth_recovery_v69.tex`, lines 1–358, complete derivative estimation, realizable selection and charged recovery.
- **S8:** `article/10f_local_observation_comparison_v71.tex`, lines 1–202, complete locality and equal-area completion argument.
- **S9:** `article/23f_single_offset_law_inverse_v42.tex`, lines 1–215; retained symmetric known-offset factorization and stability. Later global proof claims are not freshly certified.
- **S10:** `rigidity.tex`, `RESPONSE_TO_REFEREE_V72.md`, `journal/DEPENDENCY_LEDGER_V72.md`, and `LITERATURE_CHECK_V72.md`.
- **R1:** `reviews/a2-v71-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md` at `7bb8971f6b792894ee961f6fab5c6f68847d373d`.
- **R2:** `A2_REVISION_V72_REVIEW_READY.md` and delivery `rigidity-pdfinfo.txt` at the reading head. Their build/layout assertions remain attributed to the supplied records.
- **D1:** Connected Git comparisons `b0a0c9a42e61422cdf7c82df3fb80bedc0d105af...020c8b08176617e7bfb5dc37110c5b58fef99c1c` and `020c8b08176617e7bfb5dc37110c5b58fef99c1c...161ee773c42bc39db4bdb0e18aaf8d516848140b`; the coverage JSON in this directory.
- **D2:** `independent_checks.py` and `MATHEMATICAL_CHECKS.json` in this directory; reproduction instructions in `README.md`.

### Primary external literature checked

**L1.** L. Noakes and L. Stoyanov, *Lens Rigidity in Scattering by Unions of Strictly Convex Bodies in R²*, arXiv:1803.02542v2. Definitions on printed p. 2 and Theorem 1.1 on printed p. 3 were inspected in the primary PDF, including rendered pages. https://arxiv.org/abs/1803.02542v2 ; https://arxiv.org/pdf/1803.02542v2 .

**L2.** P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, arXiv:1809.08947v3; DOI 10.1007/s00220-019-03448-x. Fresh inspection at primary record/abstract level, not a new proof audit. https://arxiv.org/abs/1809.08947 .

**L3.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4; DOI 10.1007/s00222-023-01191-8. Fresh inspection at primary record/abstract level. https://arxiv.org/abs/1905.00890v4 .

**L4.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1. Theorem A, the introductory observation discussion and Definition 4.2 were inspected in the primary HTML text; the full proof was not reverified. The enriched-data and finite-horizon qualifications are retained. https://arxiv.org/abs/2510.18983 ; https://arxiv.org/html/2510.18983v1 .
