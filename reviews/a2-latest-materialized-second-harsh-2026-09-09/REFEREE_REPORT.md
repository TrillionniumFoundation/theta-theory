# A2: second referee report on the latest materialized manuscript
## With a separate audit of the unmaterialized v6 submission pointer

**Date:** September 9, 2026 (Asia/Singapore).  
**Author:** Qian Qi.  
**Manuscript:** *Collision threshold laws and statistical contact rigidity in periodic dispersing billiards*.  
**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewer:** GPT-6 Astra Pro, providing an AI-assisted referee-style assessment requested by the repository owner. This is not a journal-commissioned report, an editorial decision, a proof-assistant certificate, or an assessment by a second human referee. The preceding report was read; this review is not blinded. Its additional calculations were developed and executed without importing the author's diagnostic code.

**Recommendation on the materialized v5:** reject in its present form at the requested top-four general mathematics-journal level. No fatal error was identified in the central proof chain examined below. The principal negative judgment concerns the demonstrated importance and integration of the actual results, with specific statement and observation-model corrections identified separately.

**Disposition of the branch called v6:** no new v6 manuscript is present at the inspected commit. There is therefore no v6 mathematical revision to accept, reject on its merits, or certify as having answered the preceding report. The substantive assessment below concerns the actual v5 source, not an inferred or imagined v6.

**New review branch:** `review/a2-latest-materialized-second-harsh-2026-09-09`.  
**Review directory:** `reviews/a2-latest-materialized-second-harsh-2026-09-09/`.

## 1. What was actually submitted

The branch name and the committed source must be distinguished before discussing mathematics. Direct GitHub ref reads, commit metadata, the papers tree, and an exact commit comparison give the following record.

| Item | Frozen identity and interpretation |
|---|---|
| Highest-numbered inspected A2 revision branch | `revision/a2-v6-relative-laws-calibrated-count-rigidity-2026-09-09` |
| Its inspected tip | `9975aa037d5d9eb1f339b9220f9cd21fb54c0876` |
| Tip commit | September 9, 2026, 06:51:53 UTC / 14:51:53 Singapore; message: `review(A2 v5): independent harsh audit with sensitivity and three-amplitude refinements [skip ci]` |
| Tip root tree | `f5108a0a7824ea348b24b9bdefc53f22c1b94d73` |
| Actual latest materialized author version | `revision/a2-v5-statistical-contact-rigidity-2026-09-09`, commit `1e57d9c024f90f0304e5572c0e320707bab88074` |
| Author commit time | September 9, 2026, 03:43:02 UTC / 11:43:02 Singapore |
| Manuscript directory | `papers/A2-v5-statistical-contact-rigidity/` |
| Manuscript directory tree | `6445f4fbefa574e575ac870d4987754bf8cf94fe` |
| Main source blob | `abfa6f48301c26552946dd42d5cf2bdb6dd857cf` |

Comparing `1e57d9c...` with `9975aa...` returns exactly one commit and three added files, all under `reviews/a2-v5-statistical-contact-rigidity-harsh-independent-2026-09-09/`: `REFEREE_REPORT.md`, `VERIFICATION.json`, and `independent_diagnostics.py`. It returns **no manuscript changes**. The inspected papers tree contains the v5 manuscript, not a v6 manuscript directory. A second direct read of the v6 ref again returned `9975aa...`.

The parallel branch `revision/a2-v5-boundary-factorization-pairwise-recovery-2026-09-09` points to `ee879236d0fae1f84c685bef4ff27326403d4b2d`, timestamped 03:00:33 UTC on the same date. Its distinct additions are not attributed to the later statistical-contact-rigidity manuscript.

This is a submission-state finding, not an accusation about intent and not an adverse mathematical verdict on an unpublished revision. A branch may have been created before its intended files were pushed. Nevertheless, a referee cannot infer new theorems from the phrase “relative-laws-calibrated-count-rigidity” in its name. In particular, this review cannot mark the five preceding SCR requests as newly resolved.

The review branch is based on the inspected `9975aa...` snapshot. All mathematical locators below refer to its unchanged `papers/A2-v5-statistical-contact-rigidity/` source unless stated otherwise. LaTeX labels, rather than unverified PDF page numbers, are the controlling locators.

## 2. Overall mathematical and editorial assessment

The central achievement remains the collision-order-uniform passage from a nonlinear stationary bridge to a *relative* two-boundary determinant factorization, and then to the normalized full-phase onset probability. An estimate for the action alone would not control a mixed endpoint derivative that is exponentially small. The manuscript addresses this distinction with weighted localization and a trace-class comparison rather than concealing it inside an absolute remainder.

The materialized v5 also contains genuine improvements over v4: an all-order triangular inverse for identical even contacts; finite-dimensional analytic realizations at fixed selected leading data; a positive nearby-pairwise inverse across a triple root; and a calibration experiment that charges fine timing and remains safe on unsuccessful pilot outcomes. These improvements should not be dismissed as cosmetic. The earlier NBL requests concerning those matters should not be recycled as unresolved v4 defects.

At the same time, these results solve several different problems with different data. Exact coefficients of a normalized germ, four exact leading count amplitudes, and positions in successful selected records are not interchangeable observations. Their separate existence does not establish one comprehensive, count-only, noisy reconstruction theorem for a general periodic table. The author often acknowledges these distinctions, but several headline formulations remain broader than the adjacent precise statements.

I do not find the actual source sufficient to recommend one of the requested four journals. The uniform relative boundary law is the strongest result, but the manuscript has not yet established a convincing case that its consequences amount to an exceptional advance beyond this particular locally alternating channel problem. This is an editorial assessment of the present case for significance, not a theorem that such a result cannot merit that venue. Locality, symmetry in an application, or an elementary last step are not independently disqualifying. Nor has this review found an earlier paper containing the complete physical law.

The new calculations in Sections 4 and 5 sharpen, rather than manufacture, this judgment. The finite-flight calculation supports the top-jet signs and makes the finite/limiting information comparison explicit. The vertical-channel calculation shows exactly why “all leading data” must be indexed by the selected channel. Neither is a fatal counterexample to the correctly delimited central theorem.

## 3. Audit of the central proof chain

### 3.1 Geometry and physical preparation

**Sources:** `v5/00_introduction.tex`, `thm:g-stability`; `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`; `v3/20_integration.tex`, `lem:g-radial`.

The geometry is not restricted to near-circular scatterers. Periodicity, bounded representatives, and positive separation reduce candidate short pairs to a finite list. Strict convexity supplies unique closest contacts. The local Hessian

$$\frac1g\begin{pmatrix}1+g\kappa_0&-1\\-1&1+g\kappa_1\end{pmatrix}$$

is positive definite. Clearance from other obstacles follows for a shortest segment, and persists on a small contact neighborhood. Distinct outgoing normal states are separated. Since every complete flight is at least the minimum gap, a bound on the *total* excess bounds each individual excess without a factor depending on the number of flights. Reflection then forces reversal along the same short channel. This is the mechanism for the common onset collar; it is not a claim about arbitrary long itineraries.

The alternating Jacobi scaling is correctly retained when the two curvatures differ. With $c_b=1+g\kappa_b$, $c=\sqrt{c_0c_1}$, and $\gamma=\operatorname{arcosh}c$, the effective endpoint Hessian stays uniformly positive while its mixed derivative decays exponentially. The nonlinear contraction uses a summable two-end weight. The cofactor identity

$$-W_{uv}=\frac{\prod_i[-\ell_{i,uv}]}{\det H_{\rm int}}$$

is applied relative to its value at the normal segment. The trace-norm bound follows from the sum of the entries of a localized tridiagonal perturbation, not from matrix dimension times an operator norm. I do not identify a gap in these steps under the printed compact-family assumptions.

The physical phase density is $(-W_{uv})\,du\,dv\,dr/(2\pi A)$. The residual interval is shorter than the preceding roof and the unused terminal interval cannot add a hit. Consequently the residual-time integration is the actual normalized phase-volume experiment, not an arbitrarily chosen transverse preparation. The constructive Morse map uses the uniformly positive endpoint Hessian, and radial cancellation gives smooth right offset derivatives without assuming even scatterers. The absence of finite horizon does not invalidate this local flight-tube calculation.

### 3.2 Relative factorization and the physical limit

**Sources:** `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `thm:v4-factorization`, `thm:v4-law`; `v5/15_differentiated_operators.tex`.

The half-line fixed point has summable differentiated endpoint layers. Its action and logarithmic edge sum converge. The amplitude has a specified relative Fredholm determinant, so an unspecified infinite determinant normalization is not being smuggled into the law.

Gluing two half-lines gives an exponentially small summable stationarity residual. Uniform diagonal dominance controls its correction. For the determinant, retaining the first and last $\lfloor j/3\rfloor$ blocks loses exponentially small trace norm. Finite Green kernels converge on these blocks to the corresponding half-line kernels; the cross-block kernel is exponentially small. Telescoping the logarithmic determinant series retains a trace-class factor. The differentiated addendum correctly requires smallness only of the undifferentiated product; differentiated factors need bounded trace norms, not small norms.

The transition to probabilities is also substantive. Comparing common Morse coordinates controls the normalized integral and its right derivatives down to offset zero. One does not simply differentiate a moving indicator set formally. The limiting endpoint density factors before imposing the residual-energy constraint, but the resulting conditional probability is not a product law. The scaled bounded-Lipschitz formulation is appropriate for including a fixed number of end collisions.

The first-pole consequence concerns an onset series with a different physical window for each coefficient. It should not be counted as a pressure theorem for all itineraries. The addendum correctly explains that parameter derivatives moving a pole can raise its order while the remainder stays holomorphic on smaller common domains.

### 3.3 Jet recovery and analytic continuation

**Source:** `v5/20_contact_rigidity.tex`, `thm:v5-jets`, `cor:v5-analytic-rigidity`, `thm:v5-realization`, `prop:v5-one-flight`.

The highest-jet diagonal is supported by the finite-degree argument, not only by a formal derivative at a circle. At fixed lower even jets, the first varying length term is $(u^{2m}+v^{2m})/(2m)!$. Its mixed derivative vanishes. The stationary action variation and the interior determinant variation are therefore distinct contributions. The author's negative diagonal has the correct factors, including the two occurrences of each interior site and the residual-time weighting.

Nonvanishing gives a triangular inverse at every fixed finite order. It does not give a uniform inverse as the recovered order tends to infinity. Exact analytic continuation from an identified germ gives uniqueness of each participating analytic boundary in its contact frame; it does not give a stable global reconstruction from finitely many noisy counts or recover an unknown lattice and unobserved obstacles.

The area compensator in the realization theorem is legitimate and lies above the chosen jet order. Its preservation claim must, however, remain indexed by the horizontal ground channel. Section 5 below makes this qualification explicit with a calculation inside the same support family.

### 3.4 Pairwise inverse and calibration

**Sources:** `v5/40_pairwise_inverse.tex`; `v3/30_observability.tex`; `v4/30_saturation_acquisition.tex`; `v5/50_self_calibration.tex`.

The four-amplitude theorem is formulated in the ambient model

$$C_j(A,r)=A^{-1}\sum_{i=1}^3\operatorname{csch}\!\left(j\operatorname{arcosh}(1+g/r_i)\right).$$

The contour extension to elementary symmetric coefficient coordinates is the correct method at a triple root. The displayed four-function Wronskian has been independently recomputed here. The inverse-function theorem is applied in a full coefficient neighborhood before restricting to physical real roots. The root matching argument retains multiplicities. The resulting one-third exponent is a coefficient-to-root effect supported by the physical two-sided cubic path; it is not a new universal root perturbation theorem. An actual-curvature interpretation still requires equal facing curvatures within each channel, unlike the general forward setup.

The selected-position acquisition theorem is a different statistical experiment. Its paired-position estimator uses independent successful preparations, not independence of impacts within one trajectory. The timing calculation has the uncancelled harmonic term $-vH_m/h$. The pilot correctly estimates the zero of the square root of an onset probability instead of pretending extrapolation removes that term. Unknown positive normalizers do not affect the zero.

The coarse bracket $|j(g-g_0)|\le h/4$ is an assumption and is explicitly not acquired at the stated cost. The pilot only uses positive physical offsets; evaluation of its Taylor polynomial is not evaluation of an unphysical probability. The fallback keeps all second-stage offsets at least $h/4$, including on unsuccessful pilot outcomes. This is essential to the unconditional expected-cost claim and is present. I find no fatal error in the calibration argument as delimited. Its bound does not become an unlabelled count-only triple-curvature rate merely by juxtaposition with the pairwise inverse theorem.

## 4. An additional referee calculation: the top-jet diagonal at every finite flight number

This calculation was derived for this review from the stationary action and the cofactor formula. It is not attributed to an uncommitted v6 theorem. It gives a useful consistency bridge between the one-flight and half-line formulas already printed in v5.

Work in the identical-even contact class, fixing $g,\kappa>0$, and set

$$\gamma=\operatorname{arcosh}(1+g\kappa),\qquad a=\frac{\sinh\gamma}{g}.$$

For a bridge of $j\ge1$ flights let

$$H_j=a\begin{pmatrix}\coth(j\gamma)&-\operatorname{csch}(j\gamma)\\-\operatorname{csch}(j\gamma)&\coth(j\gamma)\end{pmatrix},$$

$$\ell_i=\left(\frac{\sinh((j-i)\gamma)}{\sinh(j\gamma)},\frac{\sinh(i\gamma)}{\sinh(j\gamma)}\right),\qquad
\nu_i=\ell_iH_j^{-1}\ell_i^{\mathsf T},\quad 0\le i\le j.$$

Here $\ell_i$ is a row vector, not the nonlinear one-flight length. For $1\le i<j$ put

$$G_{ii}=\frac{\sinh(i\gamma)\sinh((j-i)\gamma)}{a\sinh(j\gamma)}.$$

Let $w_0=w_j=1$, with $w_i=2$ for interior sites, and let

$$\alpha_m=\frac{2}{2^m(m+1)(m!)^2},\qquad m\ge2.$$

Writing $f_{j,m-1}=[d^{m-1}]F_j(d)$, the calculation gives

$$\boxed{
\frac{\partial f_{j,m-1}}{\partial q_{2m}}
=-\alpha_m\left[
\sum_{i=0}^j w_i\nu_i^m
+4m\sum_{i=1}^{j-1}G_{ii}\nu_i^{m-1}
\right]<0.} \tag{F}
$$

The empty interior sum at $j=1$ is zero. Every term has a definite sign. In particular, an intermediate finite flight number does not introduce a vanishing diagonal or a new exceptional jet order.

### Derivation

At degree $2m$, the envelope identity evaluates the first variation of the stationary action on the linear stationary segment $x_i=\ell_iY$:

$$\delta W^{[2m]}(Y)=\frac1{(2m)!}\sum_{i=0}^j w_i(\ell_iY)^{2m}.$$

At degree $2m-2$, the first variation of the normalized twist is

$$\delta b^{[2m-2]}(Y)=-\frac{2}{(2m-2)!}\sum_{i=1}^{j-1}G_{ii}(\ell_iY)^{2m-2}.$$

There is no edge-product term in that degree because the first varying length term has zero mixed derivative. Variation of the stationary coordinates starts too high to contribute: the baseline Hessian perturbation starts in degree two in the even class. Products with lower nonconstant action or amplitude terms also lie above the degree in question.

Integrate with the physical weight $(d-Y^{\mathsf T}H_jY/2)_+$. The normalization is $\pi d^2/\sqrt{\det H_j}$. After converting the ellipse to a disk, the unweighted sublevel moment associated with action variation gives $\alpha_m\nu_i^m$. The residual-weighted amplitude moment gives $4m\alpha_mG_{ii}\nu_i^{m-1}$. The moving boundary supplies no first-variation term because the residual weight is zero there. Adding the two negative contributions proves (F).

For $j=1$, both $\nu_i$ equal $\nu_1=g\cosh\gamma/\sinh^2\gamma$. Formula (F) reduces to the printed one-flight diagonal

$$-\frac{4\nu_1^m}{2^m(m+1)(m!)^2}.$$

At the two separated ends as $j\to\infty$,

$$\sum_iw_i\nu_i^m\longrightarrow 2a^{-m}\coth(m\gamma),$$

$$\sum_{i=1}^{j-1}G_{ii}\nu_i^{m-1}\longrightarrow a^{-m}D_m,\qquad
D_m=\frac1{e^{2(m-1)\gamma}-1}-\frac1{e^{2m\gamma}-1}.$$

Thus (F) also reduces to the printed limiting diagonal. The endpoint localization justifies these summable limits at each fixed $m$.

### Interpretation

The same finite-degree bookkeeping yields triangular contact recovery from any fixed finite-flight nonlinear germ in this identical-even class. This reinforces the author's own one-flight comparison: exact contact identifiability is not exclusive to the long-bridge limit. It does **not** render the uniform relative limit redundant, since a collection of fixed-$j$ statements would not imply a common collar, uniform derivatives, or the limiting physical law.

Nor is (F) a noisy-data condition-number theorem. Extracting coefficients from measured probabilities is another inverse problem. No minimax conclusion or uniform estimate as $m\to\infty$ follows from a positive summand formula. The preceding report's limiting/one-flight sensitivity comparison remains a useful benchmark, not a counterexample to a theorem that never claimed such uniformity.

The accompanying script checks the finite formula using independently constructed rational Schur complements at $g=\kappa=1$, for $j=1,\ldots,8$ and $m=2,\ldots,8$, as well as its one-flight reduction and finite-to-limit consistency. Those checks support the calculation; the derivation above, not a check count, is its justification.

## 5. A concrete scope test for “all leading data”

**Locator:** `thm:v5-realization`, its support-function construction, the abstract, and the first paragraphs of `v5/00_introduction.tex`.

The realization theorem preserves the full collision-order hierarchy of the selected **horizontal ground channel**. It does not preserve all channel-resolved leading data of the periodic billiard. The distinction can be tested inside the displayed family, without adding a different model.

Take its $M=2$ subfamily on $3\mathbb Z\times4\mathbb Z$:

$$h_s(\theta)=1+s\sin^4\theta+z(s)\sin^6\theta,$$

where obstacle area is exactly $\pi$. At the disk, the derivative of area in a support direction $f$ is $\int_0^{2\pi}f\,d\theta$. Hence

$$z'(0)=-\frac{\int\sin^4\theta\,d\theta}{\int\sin^6\theta\,d\theta}=-\frac65.$$

The horizontal gap and facing curvatures stay fixed as claimed. Now inspect the nonminimal vertical channel, which has a clear closest segment near the reference disk. Symmetry keeps its supporting contacts at normals $\pi/2$ and $3\pi/2$. Its gap is $g_v=4-2h_s(\pi/2)$ and its contact radius is $r_v=(h_s+h_s'')(\pi/2)$. Direct differentiation gives

$$g_v(0)=2,\qquad g_v'(0)=\frac25,\qquad r_v(0)=1,\qquad r_v'(0)=3,$$

so $\kappa_v'(0)=-3$. For $c_v=1+g_v\kappa_v$, one obtains

$$c_v(0)=3,\qquad c_v'(0)=-\frac{28}{5}.$$

Free area stays $A=12-\pi$. The oriented one-flight leading coefficient at this channel's own onset is

$$L_{1,v}=\frac1{2A\sqrt{c_v^2-1}},\qquad
\boxed{\left.\frac{d}{ds}\log L_{1,v}\right|_{s=0}=\frac{21}{10}\ne0.} \tag{V}
$$

The positive-curvature and clearance conditions persist for a small deformation, so this is a physical selected-channel calculation, not merely an arbitrary algebraic change of curvature. The vertical onset itself also moves.

This does not refute the horizontal-channel theorem or the complete *ground-onset* count law. It refutes an interpretation in which “complete leading count and endpoint-metric data” means all selected channels, including their own nonminimal onsets. The repair is precise and inexpensive: say **“all collision-order leading count and endpoint-metric coefficients of the selected horizontal ground channel.”** Keep the general forward theorem unchanged. The channel index must not disappear when the realization is advertised in the abstract or introduction.

## 6. The preceding requests: what remains and what must not be misreported

The controlling prior report for the *next* revision is the report at `9975aa...`, not the earlier v4 report to which the existing response letter replies. Because the inspected manuscript has not changed, the following are still the relevant requests, with their original logical status.

| Request | Present disposition |
|---|---|
| SCR-R1: actual versus effective curvatures | The formal four-amplitude model is valid. Its headline geometric interpretation must state equal facing curvatures within each channel, or use effective channel parameters. |
| SCR-R2: exact germs versus noisy recovery | Finite-jet local Lipschitz inversion is not stable analytic continuation or uniform high-order conditioning. The preceding sensitivity calculation was already supplied in the prior report, not newly discovered here. Formula (F) adds a finite-flight consistency calculation. |
| SCR-R3: constrained area versus an independent nuisance parameter | The four-amplitude theorem concerns an ambient four-parameter model. The preceding report separately demonstrated a three-amplitude inverse locally in the constrained physical family at a specified radius. That earlier sharpening is not presented here as a newly re-executed diagnostic or as a global minimal-data theorem. |
| SCR-R4: unlabelled counts versus selected positions | The charged calibration theorem estimates selected-channel curvatures from positions after a count pilot. It is not a count-only acquisition theorem for the unlabelled coalescing triple. The previous known-gap baseline count calculation is also not a new result of this report. |
| SCR-R5: central significance and literature comparison | The source remains unchanged. Its strongest claim should be assessed as a relative physical boundary law and its actual consequences, rather than an accumulation of several different inverse and sampling headings. |

The algebra behind SCR-R1 is especially decisive. In the general forward setting, leading scalar data depend on

$$c_e=\sqrt{(1+g\kappa_{e,0})(1+g\kappa_{e,1})},$$

not separately on the two endpoint curvatures. At $g=1$, the pair $\kappa_0(s)=2e^s-1$, $\kappa_1(s)=2e^{-s}-1$ leaves $c_e=2$ fixed. The existing `thm:v3-fibers` realizes this distinction in a periodic billiard. Thus the missing restriction is about the observable, not stylistic caution.

The new scope clarification (V) is similarly a clarification of an actual quantifier, not a request to abandon the realization theorem. Conversely, neither this clarification nor a bibliographic addition, by itself, settles the top-four importance question. I do not impose a new arbitrary-itinerary theorem, a new global noise theorem, or any particular enlargement as a moving acceptance condition. A strong case for the actual relative mechanism could be made on its own merits.

## 7. Targeted literature comparison

The following primary records were checked directly. Their abstracts and bibliographic records were inspected, not their complete proofs; this is not an exhaustive priority investigation.

Zelditch's analytic-domain work [1] connects localized wave-trace invariants around periodic billiard orbits to spectral determination in stated symmetry classes. It is relevant to the strategy of extracting boundary geometry from successive coefficients. The spectral datum is not the present phase-volume onset probability, and no containment of the statistical theorem is asserted. The comparison section should explain that difference while also acknowledging the related coefficient-to-geometry strategy.

Bolotin and Treschev [2] develop Hill-type identities relating action Hessians and monodromy for discrete and continuous Lagrangian systems. This is predecessor structure for the determinant mechanism, not a substitute for its nonlinear relative two-boundary limit and physical residual-time integration.

De Simoi, Kaloshin and Leguil [3] study marked-length determination for analytic open billiards under no-eclipse, symmetry, and genericity assumptions. Their table-determination problem differs from contact-germ recovery in a periodic system. The v5 comparison already makes important parts of this distinction correctly. A missing or added citation is not evidence that the central theorem is known or exceptionally important; that assessment must concern actual statements and methods.

## 8. Executed diagnostics and reproducibility limits

The new `independent_checks.py` completed **166 named checks: 123 exact checks and 43 ordinary floating, non-interval checks**. It completed both normally and under `python -O`, with byte-identical JSON output in the executed environment. Explicit failure exceptions are used rather than optimization-removable assertions. It imports no repository code and makes no network calls.

The exact checks include the vertical support/area derivatives in (V), the four-function Wronskian, rational Schur-complement instances of (F), the one-flight reduction, and finite-order extrapolation and harmonic identities. Floating checks include finite-to-half-line diagonal comparisons and Newton solution of actual nonlinear stationary chains. The latter uses the local graph $\psi(y)=y^2/2+y^4/24$, $g=1$, endpoints $u=0.06$, $v=-0.035$, and evaluates the exact length derivatives and the cofactor determinant. It is not merely evaluation of the printed limiting amplitude formula.

Representative nonlinear results are:

| Flights | Excess stationary action | Logarithm of normalized twist |
|---:|---:|---:|
| 4 | 0.004214197057659936 | -0.008185220311879071 |
| 8 | 0.004176769882254892 | -0.007937155722281375 |
| 16 | 0.004176577093051736 | -0.007935243327981567 |
| 32 | 0.004176577087929013 | -0.007935243243004209 |
| 64 | 0.004176577087929014 | -0.007935243243082368 |

The displayed agreement at large flight number reaches ordinary floating-point limitations; it is not an interval enclosure or proof of the continuum convergence theorem. The polynomial contact graphs used for this diagnostic are not a simulation of a globally area-compensated periodic billiard. The vertical-channel calculation, separately, concerns the actual analytic support family by its exact first variation.

Executed environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0. Script SHA-256: `08df5fb37412b5ff3f522d2fa4c9150cca155fb5f0abc7e1da0863e50a70cc66`. Full diagnostic JSON SHA-256: `ff7eda86b31486a76aa49206300aa61e1b714e8aea756dacf860d4d789101ca0`. `VERIFICATION.json` records commands, hashes, source identities, and the distinction between this execution and the preceding review's execution. Cross-version floating-point byte identity is not promised.

The direct source audit covered the main statement and its geometric/nonlinear bridge and full-phase integration foundations, the complete two-boundary factorization proof, its differentiated operator addendum, the contact-jet theorem and realization, the endpoint variance and sampling arguments, the known-gap timing/acquisition argument, the complete self-calibration proof, the four-amplitude pairwise proof, the author's v5 response, the current comparison section, and the previous review. The physical three-amplitude sharpening in that preceding report was not independently re-executed in this round.

The unchanged circular appendices, general record-response chapters, two-collision companion, historical Round 33 material, and every other historical branch were not separately re-audited. I did not execute the author's validation suite, compile or inspect a manuscript PDF, certify remote CI, perform a proof-assistant check, or establish exhaustive originality. A successful finite diagnostic does not certify any uninspected chapter or external proof.

## 9. Final disposition

There is no committed v6 mathematical response at the inspected v6 pointer. A future push must be reviewed at its own exact commit; the present report must not be used to approve it prospectively.

For the materialized v5, the relative boundary-law mechanism and the new inverse/calibration arguments withstand the focused proof audit without an identified fatal counterexample. This is substantial credit. The finite-flight calculation strengthens the internal consistency of the jet formulas. The vertical-channel calculation isolates a genuine scope restriction in the advertised preserved data.

My recommendation remains **reject at the requested top-four level in the present form**. The manuscript has not yet made a sufficiently compelling case for the exceptional importance of its specialized relative mechanism and the collection of inverse consequences attached to it. That judgment must be kept separate from correctness: the report does not say the central theorems are false, the v5 changes were cosmetic, or the program cannot advance. The actionable record is the precise source-state finding, the unresolved SCR dispositions, and the channel/observable qualifications above—not an instruction to delete correct mathematics or abandon the general forward setup.

## Primary references and frozen source links

[1] S. Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269. DOI: 10.4007/annals.2009.170.205. Primary publisher record: https://annals.math.princeton.edu/2009/170-1/p06.

[2] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), no. 2. DOI: 10.1070/RM2010v065n02ABEH004671. Primary author record: https://arxiv.org/abs/1006.1532.

[3] J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*. DOI: 10.1007/s00222-023-01191-8. Primary author record: https://arxiv.org/abs/1905.00890.

Frozen author manuscript: https://github.com/TrillionniumFoundation/theta-theory/tree/1e57d9c024f90f0304e5572c0e320707bab88074/papers/A2-v5-statistical-contact-rigidity.

Frozen preceding report: https://github.com/TrillionniumFoundation/theta-theory/blob/9975aa037d5d9eb1f339b9220f9cd21fb54c0876/reviews/a2-v5-statistical-contact-rigidity-harsh-independent-2026-09-09/REFEREE_REPORT.md.

Exact inspected change set: https://github.com/TrillionniumFoundation/theta-theory/compare/1e57d9c024f90f0304e5572c0e320707bab88074...9975aa037d5d9eb1f339b9220f9cd21fb54c0876.
