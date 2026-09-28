# Independent external referee report on A2 v24

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Revision examined:** `revision/a2-v24-uniform-physical-global-top4-2026-09-11`  
**Immutable source commit:** `c35b31b1924a1621374eab72ee60e4cb5ab37df5`  
**Previous manuscript used for the revision comparison:** `55b2d3b41acd3e0beb7e9071c13e54637137f9ad`  
**Active source:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v24-external-harsh-top4-2026-09-12`  
**Review date:** September 12, 2026  
**Standard:** deliberately severe consideration at the level of Annals, Inventiones, JAMS, or Acta.

This is an author-requested, AI-assisted independent referee-style assessment. It is not a commissioned report or editorial decision of any journal. The manuscript, its author response, and previous referee conclusions are treated as claims to be examined, not as certificates of correctness.

## Recommendation

**Reject in the present form at a top-four mathematics journal. A substantively repaired successor could warrant fresh consideration.**

This recommendation is not a claim that the deterministic inverse is false, that the research program should be abandoned, or that the scope must be reduced. Several parts of v24 genuinely answer the preceding report. In particular, the rank-two reconstruction removes the previously supplied lattice metric; the new layer/bulk argument supplies substantially more than weak Poisson convergence; and the normal-quotient formulation repairs the noncanonical presentation of the count direction. Repeating the old objections to those points without examining the new proofs would be unfair.

The remaining decisive issue is the passage from intrinsic channel laws to the advertised **implementable global physical experiment**. The new proof constructs an estimator using centered channel coordinates, but the common observable that produces these coordinates over the global analytic class is not constructed. The inherited physical theorem obtains its common coordinates by restricting to an anchored, registered local family. A timing pilot does not by itself extend that restriction to the new global class. In addition, the finite-separator argument omits the gap component of the target vector from its identifiability justification, although the preceding signed inverse explicitly obtains that component from the physical onset. These are gaps in the proof of the statistical flagship theorem, not merely requests for improved rates.

There is a separate defect in the finite-signature stability argument: separation from points outside a matching arc is used as if it guaranteed a unique match inside the arc. It does not. An explicit analytic strictly convex oval below illustrates the missing implication. This does not refute exact analytic rigidity or the conditional compactness modulus; it invalidates the stated justification of robust finite-signature matching.

Finally, the paper must explain the mathematical necessity of its long-bridge construction relative to much shorter signed-record experiments. I give an elementary one-flight support inverse below. That inverse does not replace the limiting-law theorem, because the observation families differ, but it is a serious benchmark for the significance of a broad global finite-bridge consistency claim.

## 1. Scope, source control, and status of the preceding objections

The v23-to-v24 comparison consists of eleven commits. The mathematical delta comprises the new introduction, five new substantive modules, and the modified main file. I read that new mathematical delta and the v24 response, then checked the inherited signed-contact inverse, the physical coordinate conventions, the finite-to-boundary comparison, the count experiment, the relevant endpoint-time expansion, and the onset calibration on which the new claims depend. Source links and stable theorem labels are supplied below.

This is a revision-focused mathematical audit, not a claim to have independently recertified every historical appendix. No native compilation of the complete exact-head source tree was performed in this review. The accompanying independent diagnostic program checks selected identities and witnesses; it is not the manuscript's test suite and is not a proof checker.

| Previous R3 issue | Assessment of v24 | Reason |
|---|---|---|
| M1: global statistical recovery was conditional | Substantial new argument, but not closed | A finite-separator estimator and capped policy are now proposed; the common-observation and gap-identifiability steps remain unresolved. |
| M2: a known lattice Gram form was supplied | Substantively resolved under the stated marked-data assumptions | Two independent deck holonomies determine the full linear lattice realization. |
| M3: global gluing stability | Partially resolved | Compact inverse continuity is valid conditionally; the finite-signature persistence argument contains an unjustified local uniqueness step. |
| M4: reverse Poisson deficiency | Substantively resolved for the inherited physical local model | Explicit parameter-independent kernels and a product Hellinger bound are now provided. |
| M5: noncanonical count splitting | Substantively resolved | The quotient construction and explicit positive curvature derivatives identify the intrinsic normal direction. |
| M6: theorem hierarchy | Improved, but significance still needs sharper positioning | Two flagship statements are identifiable; a stronger comparison with short-flight signed data and prior work is still needed. |
| M7: exact-head build | Not certified at the time of inspection | The native-build job remained queued, with no conclusion. This is not evidence of a TeX failure. |

The evaluation below distinguishes an unsupported proof step, a counterexample to a particular inference, a correct conditional theorem, and an editorial objection. These categories should not be collapsed into one list of supposedly false results.

## 2. Mathematical progress that should be retained

### 2.1 The signed all-order inverse has a substantive proof mechanism

In [S3], `thm:v22-signed-rigidity`, positivity of the endpoint amplitude identifies the support threshold

$$
T_b(u,v)=S_b(u)+S_b(v),\qquad S_b(u)=T_b(u,0).
$$

The proof then uses a weighted half-line inverse, a finite-truncation envelope identity, and homogeneous degree isolation. This is materially better than a formal assertion that Taylor coefficients can be inverted. In particular, the orbit variations cancel by stationarity before the highest graph jet is isolated. The distinction between the derivative order required by the stationarity equations and the degree at which a graph jet enters the action is handled explicitly.

For the degree-$n$ block, with $x=e^{-\gamma}$ and $r=\mathfrak r_0=\mathfrak r_1^{-1}$, the multiplicities give

$$
1+2\sum_{k\geq1}x^{2nk}=\coth(n\gamma),
\qquad
2r^n\sum_{k\geq0}x^{n(2k+1)}=r^n\operatorname{csch}(n\gamma).
$$

Consequently

$$
\det M_n=\coth^2(n\gamma)-\operatorname{csch}^2(n\gamma)=1.
$$

The independent diagnostic reproduces the sums, determinant, and proposed inverse in 100 exact rational cases. These checks support the algebra; they do not establish the infinite-dimensional estimates by themselves. I found no specific contradiction in the weighted-envelope and homogeneous-isolation argument examined here.

The appropriate claim remains a fixed-order inverse with constants depending on the order. Determinant one alone would not prove a uniform condition number for the whole lower-triangular jet map, and the manuscript appropriately does not claim that conclusion.

### 2.2 Recovering the uncalibrated lattice is a genuine strengthening

In [S4], `prop:v24-metric-free-holonomy` and `thm:v24-lattice-gram-recovery`, let $M$ have the two marked deck displacements as columns and let $V$ have the corresponding observed translation holonomies as columns. After fixing the root-frame rotation,

$$
L=VM^{-1},\qquad G=L^tL=M^{-t}V^tVM^{-1}.
$$

This is correct. The two deck vectors need only be independent over the reals; they need not be a unimodular basis of the integer lattice. Realizability supplies the compatible orientation and invertibility. A global rotation left-multiplies $L$ and leaves $G$ unchanged. The diagnostic includes non-unimodular marked pairs and verifies the Gram identity and rotational invariance exactly.

The result still assumes the combinatorial deck labels. That assumption is stated explicitly and should not be criticized as if v24 were silently claiming to discover unknown labels. Nor should the older, metrized formulation in the preceding section be mistaken for the stronger theorem actually announced in v24.

The difficult geometric input remains the recovery of channel copies and the uniqueness of incidence congruences. Once those have been established, the last lattice step is finite-dimensional linear algebra. The paper should allocate its claims of novelty accordingly.

### 2.3 The new reverse kernel addresses the actual previous deficiency objection

In [S6], `thm:v24-two-sided-deficiency`, the forward kernel extracts a reference layer defined independently of the local parameter. The reverse kernel maps Poisson points back to records, fills the remaining sample positions from the reference bulk law, and uniformly permutes the records. Conditional on the layer count, the iid sample has precisely the layer/bulk factorization used in the proof.

The estimates have the right structure:

$$
k p_{n,z}^2=O(k^{-1}),\qquad
H^2(B_{n,z},B_{n,0})=O(k^{-2}),
$$

and therefore

$$
H^2(B_{n,z}^{\otimes(k-m)},B_{n,0}^{\otimes(k-m)})=O(k^{-1}).
$$

Together with the layer-intensity comparison and the negligible Poisson count tail, this gives the claimed vanishing reverse error. The bulk factor is not merely declared ancillary after examining one marginal statistic; it is reconstructed by a common kernel.

One qualification should be made explicit in the statement. Mere $C^0$ convergence of the density factor in `eq:v24-deficiency-remainder` would not imply the $O(k^{-2})$ bulk Hellinger bound for arbitrary triangular arrays. The bounded $O(k^{-1})$ relative density expansion is needed. In the present physical application, the inherited endpoint-time section [S8] gives the $O(k^{-1})$ trace perturbation, and the smooth fixed-window dependence supplies the relevant expansion. State this as a hypothesis or explicit dependency of the lemma. I do not regard that presentation issue as an unclosed version of R3-M4.

### 2.4 The count quotient is correctly identified

In [S7], at fixed gap,

$$
\gamma=\operatorname{arcosh}\sqrt{(1+g\kappa_0)(1+g\kappa_1)}
$$

implies

$$
\partial_{\kappa_0}\gamma=
\frac{g(1+g\kappa_1)}{2\sqrt{(1+g\kappa_0)(1+g\kappa_1)}\sinh\gamma}>0,
$$

with the analogous formula for the other curvature. Thus $d\gamma\ne0$ in the declared anchored finite-jet model. The count coordinate naturally lives on $N=V/\ker d\gamma$.

The change of splitting representative is negligible because the inherited rate conditions give

$$
k\eta_n^2\log(1/\eta_n)=\frac{\log(j_n\sqrt{k_n})}{j_n^2}\longrightarrow0,
\qquad \eta_n=(j_n\sqrt{k_n})^{-1}.
$$

The potentially troublesome second-order slow-coordinate term is also negligible: $\sqrt{k_n}j_n\delta_n^2\to0$ follows from $k_n\delta_n^2\log(1/\delta_n)\to1$ and $j_n\delta_n\to0$. I therefore find no reason to repeat the previous coordinate-invariance objection as a major defect of this revision.

## 3. Major objection M1: the global policy is not yet constructed on its claimed common physical observation space

**Location:** [S1], `lem:v24-finite-separators`, `thm:v24-fixed-M-physical-estimability`, and `thm:v24-physical-global-reconstruction`; compare [S9] and [S10].

**Classification:** unresolved experiment-definition and implementability step; not an information-theoretic impossibility result.

The finite-separator construction uses $Q_{T,a}^{\infty}$ in channel-local signed coordinates. Its empirical statistic is the average of a fixed function $\phi_r(u,v,r)$ in those coordinates. The theorem then says that no unknown gap, local chart, or table parameter is supplied to the policy.

The inherited physical experiment achieves a common measurable observation map by a much more restrictive construction. In [S9], the graphs are anchored in one fixed laboratory chart, with the same transverse origins and tangent direction throughout the local family. The recorded endpoints are literal laboratory coordinates. The compactly supported smooth perturbations in [S10] preserve those anchors. This makes the local theorem meaningful, but does not construct a corresponding globally valid experiment over an arbitrary compact analytic class.

For a general table in the new global class, a centered transverse coordinate has the schematic form

$$
u_e=t_e(T)\mathbin{\cdot}(X-p_e(T)),
$$

where $p_e(T)$ is a contact point and $t_e(T)$ its oriented transverse unit vector. A fixed laboratory coordinate need not equal this quantity throughout the class. Even the special case $u=Y-c_e(T)$ requires either a supplied center, an observable centering operation, or an estimated center. The new pilot estimates $g_e(T)$; its conclusion contains no estimate of $p_e(T)$, $t_e(T)$, or the transformations needed to evaluate all the separator functions.

This objection concerns **within-channel anchoring**, not the relative Euclidean placement of different channels. Recovering inter-channel registration by deterministic gluing does not automatically make the within-channel statistical normalization a common observable before that reconstruction has been carried out.

The transfer theorem [S11] does not close this gap. A parameterwise estimate

$$
\sup_T\|P_T-Q_T\|_{\rm TV}\leq\epsilon
$$

between already specified laws is useful. It does not establish that a family of transformations $C_T$ used to define or analyze those laws can be applied by the experimenter without knowing $T$. The same boundary embedding can be used on both sides of a comparison at a fixed parameter without becoming a parameter-independent statistical kernel. The inherited transfer section itself distinguishes these issues.

There are two coherent formulations, but the manuscript must actually choose and prove one. It may declare signed contact-centered coordinates to be direct outputs of a specified measurement apparatus; then that supplied acquisition structure must be stated at theorem level, and its relation to the laboratory model must be explained. Alternatively, it may remain with the declared laboratory observables and prove a charged within-channel localization/registration stage, or formulate the separator argument directly on those observables. In the latter case, the needed coordinate estimates and their effect on successful-law expectations must be controlled uniformly.

This is not a demand to supply the forbidden common inter-channel placement, and it need not weaken the deterministic inverse. It is a demand that the global estimator be a measurable function of the same observations that the theorem claims to use.

**Required closure:** define one design space, one observation space, the per-preparation record map, and the allowed pilot information independently of the unknown table. Show that each empirical separator and adaptive design is measurable in the resulting transcript. Prove the uniform approximation on that space. An appeal to compactness of a family of parameter-dependent centered descriptions is not a substitute.

## 4. Major objection M2: the finite-separator proof does not account for the gap coordinates it promises to estimate

**Location:** [S1], definition of $\mathcal D_M$ and `lem:v24-finite-separators`, particularly the implication in its proof; compare [S3], `eq:v22-support-threshold` and `eq:v22-leading-recovery`.

**Classification:** missing identifiability implication with a direct possible repair. No counterexample to equality of the full nonlinear conditional laws is asserted here.

The target vector is

$$
\mathcal D_M(T)=\bigl(g_e,S_{e,0}^{(m)}(0),S_{e,1}^{(m)}(0)\bigr)_{e,\,2\leq m\leq M}.
$$

The separator proof argues that equality of all centered successful boundary laws gives equality of the two action germs, and then concludes equality of $\mathcal D_M$. The second implication has not been proved. In the signed inverse itself, the support determines $S_0,S_1$, while the physical onset supplies $g$. The new separator family uses centered conditional laws indexed by excess $d$; it does not include the physical onset in the displayed expectation vector.

The distinction is already visible in the leading recovery formula. At fixed $a_0=a_1=a$, the compatible quadratic geometries satisfy

$$
\kappa_0(g)=\kappa_1(g)=\frac{\sqrt{1+g^2a^2}-1}{g}.
$$

For example, $a=1$ is compatible with $(g,\kappa)=(3/4,1/3)$ and $(4/3,1/2)$. Thus the quadratic action data do not themselves supply the onset. Higher action data or density amplitudes could conceivably provide additional information; the present proof does not establish the specific full-law implication required. The examples above are deliberately not presented as two periodic tables with identical complete conditional boundary laws.

The omission also appears in the estimator. Its minimum-distance criterion uses only

$$
\mu(T')=\bigl(Q_{T',a_r}^{\infty}\phi_r\bigr)_r.
$$

The estimated gaps are used to program times, but they are not included in this displayed criterion. Retaining the pilot in the transcript does not by itself prove that an estimator whose stated consistency argument ignores this information separates the missing coordinate.

The natural repair is to use the augmented observable family

$$
\mathcal I(T)=\bigl((g_e(T))_e,\ (Q_{T,a}^{\infty})_a\bigr).
$$

Its injectivity for the required finite data follows by the precise deterministic argument already available. On the compact separated-pair set, each pair can then be separated either by a gap coordinate or by a bounded boundary-law test. A finite subcover gives a finite mixed separator list. The physical pilot estimates the former coordinates; fresh successful records estimate the latter. A weighted minimum-distance criterion involving both $\widehat g$ and the empirical separator vector can then be analyzed.

This approach preserves the intended scope. It does not require the author to solve a stronger and currently unproved question about whether centered conditional amplitudes alone determine the gap.

**Required closure:** prove the missing conditional-law implication, or explicitly augment the separator lemma, criterion, and risk bound with onset coordinates. The second route is more directly supported by the current manuscript.

## 5. Major objection M3: an outside-arc signature margin does not give unique finite-signature matching inside the arc

**Location:** [S5], item 3 in the definition of the robust analytic class, and `lem:v24-gluing-persistence`.

**Classification:** a demonstrably invalid inference in the finite-signature argument. It is not a counterexample to the exact all-order rigidity theorem.

The assumption gives a lower separation of the selected finite curvature signature from competing framed points **outside** a prescribed matching arc. The proof uses that margin to conclude that the designated match is the unique minimizer among competing points and continues uniquely under perturbation. Nothing in the displayed outside-arc inequality controls competitors inside the arc.

This is not just a semantic concern about the word quantitative. Consider the real-analytic support function

$$
h(\theta)=3-\frac13\cos(2\theta)-\frac1{16}\cos(3\theta).
$$

Its radius of curvature is

$$
\mathcal R(\theta)=h(\theta)+h''(\theta)
=3+\cos(2\theta)+\frac12\cos(3\theta)\geq\frac32.
$$

It therefore defines a real-analytic strictly convex closed oval, with curvature

$$
\kappa(\theta)=\mathcal R(\theta)^{-1}.
$$

The curvature has its unique global minimum $2/9$ at $\theta=0$ modulo $2\pi$: simultaneous equality in both cosine upper bounds occurs only there. On the complement of any fixed small arc about zero, compactness supplies a strictly positive separation from this minimum. Thus the scalar signature allowed by $m_{\rm sig}=0$ has precisely the asserted outside-arc gap at the selected point.

Nevertheless, for every sufficiently small nonzero $\theta$, the nearby scalar target $\kappa(\theta)$ has two matches, at $\theta$ and $-\theta$, both inside the arc. These are distinct points. The support function has harmonics of orders two and three, so it has no nontrivial rotational symmetry; its reflection symmetry does not identify the two points under the orientation-preserving symmetry quotient used in the manuscript. Complete oriented curvature signatures distinguish them, but the chosen scalar finite signature does not.

The same phenomenon is apparent in the local model $\kappa(s)=\kappa_*+s^2$: an upward perturbation of the target produces two in-arc matches. The closed-oval construction shows that this is compatible with analytic strictly convex obstacle geometry, rather than being an arbitrary unrelated scalar example.

This witness does not establish two tables with the same complete intrinsic data. It establishes that the stated finite-margin hypothesis, and the proof's first inference from it, do not deliver the finite-signature robustness being claimed. Exact uniqueness of a complete analytic signature does not automatically validate a particular finite truncation or its noisy matching rule.

One repair is to select a sufficiently rich finite signature and prove a uniform local embedding estimate, together with the already stated outside-arc separation. For instance, a suitable version would control the local parameter difference by the finite-signature difference on the chosen arc, modulo exactly the declared symmetries. Another repair could use a different, fully defined matching functional with an explicitly proved local uniqueness property. Analyticity and compactness may help to find a finite order, but the selection, exclusion of symmetry degeneracy, and uniformity have to be proved.

**Required closure:** distinguish global exclusion of wrong arcs from local injectivity within the correct arc. Supply a matching lemma with both ingredients, then propagate its actual continuity or stability estimate through the finite graph. Do not infer the second ingredient from the first.

## 6. Additional technical corrections in the new global argument

### 6.1 The asserted finite-dimensional tangent bundle is not specified

In [S1], `lem:v24-uniform-positive-design`, the proof invokes a compact unit tangent bundle over a finite-dimensional model on $\mathfrak K$. The class introduced in [S5] is a compact class of analytic boundaries, not a specified finite-dimensional manifold. Truncating the target vector to $\mathcal D_M$ does not make the underlying experiment finite dimensional: the positive-offset law can still depend on higher-order geometry.

A finite-rank bundle of selected perturbation directions over a compact, even infinite-dimensional, base can certainly be constructed. The objection is not that such a bundle is impossible. The manuscript has not constructed it, specified its transition maps, handled compatibility of jets at multiple contacts on the same analytic obstacle, or shown that the resulting information forms vary continuously. The smooth anchored bump proposition [S10] does not automatically furnish a bundle of analytic variations lying in the global class.

This issue is separable from global consistency. The later minimum-distance proof explicitly takes a separator route that does not require a Fisher-information lower bound. It is therefore possible to prove the corrected global estimator without this tangent-bundle lemma as an essential dependency. But the lemma remains an assertion in the paper and must either receive a well-defined setting and proof or be clearly separated from the global theorem. No uniform finite-dimensional structure should be attributed to the analytic class without construction.

### 6.2 Pilot accuracy must be chosen for the final flight number

The proof of `thm:v24-fixed-M-physical-estimability` runs the pilot and only later chooses and increases the common even flight number $J$. The pilot conclusion controls $j_e|\widehat g_e-g_e|$ at its specified flight numbers. Such a bound does not automatically become $J|\widehat g_e-g_e|<\epsilon$ after $J$ is increased.

This is a repairable quantifier/order error, not a circularity obstruction. A valid ordering is: choose the target accuracy and separators; choose empirical sample sizes; choose the final post-pilot flight number and transfer budget; choose pilot precision for that number; then run the pilot and subsequent batches with their predetermined caps. A different pilot flight number is also possible, provided its required absolute gap error is adjusted explicitly to the final $J$.

The cited calibration section [S12] initially works with odd $j$, while the same-type endpoint batches use even $J$. The onset argument may extend without difficulty, or an odd pilot can be used with the adjusted precision. The proof should state the choice rather than silently identifying the two experiments.

### 6.3 Uniform continuity must be in a topology strong enough for the selected tests

The separator proof chooses bounded measurable tests using total variation duality. Continuity of their expectations then needs total variation continuity, or a different selection of tests supported by the available weak topology. On a common fixed positive-offset coordinate space, the bounded-density/fiber estimates make total variation continuity plausible and accessible. State and prove that uniform continuity in the corrected observable model. Merely saying that the boundary laws are continuous is insufficient when their coordinate representations are precisely the unresolved issue in M1.

## 7. What the inverse modulus does, and does not, establish

The compactness argument in [S5], `thm:v24-global-modulus`, is mathematically legitimate once the complete data map is continuous and injective on the stated compact class. The function

$$
\omega_q(t)=\sup\{d_q(T,T'):d_{\mathcal D}(T,T')\leq t\}
$$

then tends to zero. The estimate

$$
d_{\mathcal D}(T,T')\leq C\|\mathcal D_M(T)-\mathcal D_M(T')\|_M+C2^{-M}
$$

also follows from the selected weighted product metric. In particular, its tail bound uses the summability of the weights and the truncation by one; it is not an exponential analytic-continuation accuracy estimate.

The resulting modulus is non-effective: it is defined through a supremum over the unknown inverse problem. The proof does not derive a computable rate from $\rho,B,\chi,\sigma_{\rm sig},\sigma_{\rm hol}$. For a purely existential uniform consistency theorem, an effective rate is not required. I do not reject the theorem for failing to prove a sharp minimax rate that it explicitly disclaims.

However, the new finite-signature lemma cannot be advertised as an established algorithmic stability mechanism merely because a separate compactness argument supplies an abstract inverse modulus. Exact rigidity plus compactness may bypass that lemma for a nonconstructive continuity result; it does not prove the faulty finite-signature matching step. The revised article should keep these logical routes separate.

Similarly, once a valid uniform fixed-order physical estimator exists, the final diagonal choice over $q\leq s$ is sound in principle. The diagonal argument is not the remaining central difficulty. The difficulty is the experiment and estimator to which it is applied.

## 8. A stronger short-flight benchmark and the significance of the flagship theorem

### 8.1 Signed one-flight support already determines the two graph germs

The manuscript's own one-flight action [S13], `eq:g-length`, is

$$
\ell(u,v)=\sqrt{(g+\psi_0(u)+\psi_1(v))^2+(v-u)^2}.
$$

Assume a mixed-type, one-flight endpoint experiment is available in the same calibrated signed transverse coordinates, with the physical onset retained. The finite physical flux is positive on a sufficiently small contact box, as in [S11] and [S13]. The endpoint-support threshold as the physical observation time varies therefore gives the local function $\ell(u,v)$ itself. Equivalently, thresholding by excess gives $E_1=\ell-g$ and the onset supplies $g$.

Taking the two coordinate slices yields the elementary exact inverse

$$
\psi_0(u)=\sqrt{\ell(u,0)^2-u^2}-g,
\qquad
\psi_1(v)=\sqrt{\ell(0,v)^2-v^2}-g.
$$

The positive square-root branch is fixed by $g+\psi_b>0$. Neither reflection symmetry nor supplied curvatures are needed. All contact jets follow, and analytic continuation and the same intrinsic gluing problem can then be considered. The accompanying diagnostic verifies the reconstruction algebra in twenty exact rational examples.

This benchmark uses **mixed-type one-flight signed support data**, not the same-type long-bridge limiting law. It does not prove that one observation family is a Markov coarsening of the other, and it does not replace the relative half-line theorem. The important distinction is exactly the observation restriction.

The article already includes a two-flight benchmark [S14], but that benchmark concerns integrated probability germs for even contacts at supplied leading geometry. It does not address the much richer signed-support benchmark above.

If the global statistical architecture permits arbitrary finite-flight endpoint-time designs, the author must explain why a global consistency result obtained by choosing long bridges represents the principal mathematical advance rather than one possible route to an inverse problem already accessible through the displayed short-flight identity. If only long even same-type records are admissible, this restriction should be unambiguous in the flagship theorem and the comparison should be made within that restricted experiment. Neither answer requires deleting the long-bridge theory; it requires identifying what that theory uniquely recovers or explains.

The same within-channel coordinate issue in M1 affects this benchmark. It is not offered as a shortcut around that missing physical argument.

### 8.2 The comparison with existing rigidity and nonregular statistics needs to be restored at the theorem level

De Simoi, Kaloshin, and Leguil prove marked-length determination for analytic open dispersing billiards under symmetry and genericity assumptions [L1]. Finamore and Leguil's 2025 preprint treats finite-horizon Sinai billiards using an enriched marked length spectrum [L2]. These are relevant comparisons, but their data are not the signed channel-law family used here. It would be incorrect either to declare A2 subsumed by those results or to describe A2 as a direct generalization without specifying a relation between the observation maps.

For statistics, Smith's nonregular-support analysis includes the critical linear-vanishing boundary case with an altered normal rate [L3]. Meister and Reiss establish Le Cam equivalence between nonregular regression and Poisson experiments carrying the target as an intensity support boundary [L4]. Thus a moving-boundary Gaussian/Poisson distinction and a Poissonization strategy are not, by themselves, new general principles.

The plausible contribution of A2 is the billiard-specific relative law, its unsymmetrized contact inverse, and the explicit connection between nested physical record levels. The new introduction [S2] should explain that contribution against the actual hypotheses, data restrictions, and conclusions of these references. A long bibliography without that comparison is not sufficient positioning for a top-four submission.

## 9. Mechanical status and reproducibility

The exact reviewed source head was checked against GitHub Actions. Run `34608745010`, named `A2 v24 complete native build`, had job `103293603377` in status `queued`, with null conclusion and no executed-step result returned at inspection. The existence of the workflow is not a build certificate. Conversely, queued infrastructure is not a mathematical defect and does not establish a LaTeX failure.

The root README still points to an older A2 version. The active revision was therefore identified from its actual revision branch, main file, and commit comparison rather than the root index. This is a navigation defect, not a reason to reject a theorem.

The report uses source filenames and theorem labels instead of asserting compiled page numbers. No complete unresolved-reference audit or native PDF inspection is claimed. The paper should obtain an exact-head native build and archive the log, source/PDF hashes, and any diagnostic output before submission.

The independent diagnostic included with this report was run under Python 3.13.5 in both normal and optimized mode. The JSON outputs agree byte for byte. It checks 100 last-jet block cases, six lattice cases, six curvature-derivative cases, two leading-geometry witnesses, six paired finite-signature samples, and twenty one-flight reconstruction cases. The witnesses diagnose specific logical implications; passing them does not certify the manuscript.

## 10. Concrete conditions for another substantive review

The next revision should make the physical-to-global argument inspectable through a small number of precise statements rather than another layer of claimed closures.

1. **A common-observable acquisition theorem.** Specify the actual observations and parameter-independent record maps on the global analytic class. Prove any required within-channel calibration using only the declared transcript, with charged costs and uniform error bounds.
2. **An augmented finite-separator theorem.** Include onsets and conditional laws, or prove the stronger missing conditional-law identifiability statement. Give the corresponding minimum-distance estimator and its uniform risk bound, including the pilot coordinates actually used.
3. **A correct finite-signature matching theorem.** Supply both local in-arc uniqueness and exclusion of other arcs, with a proved uniform choice of finite signatures. Separate this from exact analytic rigidity and from the abstract compact inverse modulus.
4. **A coherent dependency and design schedule.** Specify any finite-rank tangent model that remains in the article; choose the final flight numbers before the required pilot precision; state the topology of law continuity used by bounded tests. Then apply the otherwise appropriate compactness/diagonal argument.
5. **A theorem-level significance comparison and a clean build.** Address the signed one-flight benchmark, distinguish the limiting-law and physical acquisition restrictions, compare the closest rigidity and nonregular-statistics literature, and certify the exact submitted source mechanically.

There is no request here to remove the all-order contact derivation, assume equal contacts, restore a prescribed lattice metric, impose reflection symmetry, or abandon global reconstruction. The request is to prove the precise strong theorem that is advertised, on its actual observation space, and to explain why that theorem is a sufficiently significant advance.

**Final assessment:** v24 is a real mathematical revision, not a cosmetic response. The local algebraic and statistical repairs deserve credit. Nevertheless, its central global physical-estimation claim is not yet supported by the complete common-observation and identifiability argument stated in the paper. Together with the finite-signature proof defect and the unresolved short-flight comparison, this prevents a positive recommendation at the requested journal standard.

---

## Source and literature references

All manuscript links below are pinned to the reviewed commit. The stable labels cited in the text identify the relevant assertions even if later versions renumber sections.

[S1]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/25a_uniform_physical_global_v24.tex
[S2]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/01_introduction_v24.tex
[S3]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v22.tex
[S4]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/23d_rank_two_lattice_recovery_v24.tex
[S5]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/23e_quantitative_gluing_stability_v24.tex
[S6]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/18c1_endpoint_time_deficiency_v24.tex
[S7]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/18d1_intrinsic_count_geometry_v24.tex
[S8]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/18c_full_endpoint_time_information_v23.tex
[S9]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/18b_raw_physical_multirate_v22.tex
[S10]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/18b0_anchored_realization_v22.tex
[S11]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/v6/10_experiment_transfer.tex
[S12]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/v5/50_self_calibration.tex
[S13]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/v3/10_geometry_action.tex
[S14]: https://github.com/TrillionniumFoundation/theta-theory/blob/c35b31b1924a1621374eab72ee60e4cb5ab37df5/papers/A2-v17-boundary-information-coarsening/article/29_two_flight_benchmark.tex

**[L1]** J. De Simoi, V. Kaloshin, M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829–901. [Institutional publication record](https://research-explorer.ista.ac.at/record/12877). DOI: `10.1007/s00222-023-01191-8`.

**[L2]** D. Finamore, M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. [Primary preprint record](https://arxiv.org/abs/2510.18983v1). The comparison here is specifically with the enriched marked length spectrum described there.

**[L3]** R. L. Smith, *Maximum likelihood estimation in a class of nonregular cases*, Biometrika 72 (1985), 67–90. [Publisher record](https://academic.oup.com/biomet/article-abstract/72/1/67/242523). DOI: `10.1093/biomet/72.1.67`.

**[L4]** A. Meister, M. Reiss, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, arXiv:1101.5248v1, January 27, 2011. [Primary preprint record](https://arxiv.org/abs/1101.5248v1).

Public bibliographic records were checked during this review. The comparisons above concern their stated data and theorem scope; they are not claims of a complete new literature survey or of mathematical subsumption of A2 by those papers.
