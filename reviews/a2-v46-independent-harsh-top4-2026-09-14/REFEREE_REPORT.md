# Independent referee-style report on A2 revision 46

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Report date:** September 14, 2026  
**Requested standard:** a highest-level general mathematics journal.  
**Status:** an author-requested, AI-assisted independent assessment. This is not a commissioned journal report, a representation of journal affiliation, or an actual editorial decision.

| Object reviewed | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Review-ready branch | `revision/a2-v46-review-ready-2026-09-14` |
| Review-ready commit | `b48685189554e594d81baa6be9c72fd7ec873975` |
| Actual compiled mathematical source | `ab99196fadc20682c1ee44d6bb433a788c7274ab` |
| Workflow preparation commit | `44457d01bfb809b07c5e22b92e7200c146005bb6` |
| Native run / attempt / artifact | `34838199154` / `1` / `10345480046` |
| Native manuscripts | Main: 243 pages; companion: 7 pages |
| Previous report | v45, commit `0614a20bbba6312830b5523b806ddc726a6333f1` |

Source identifiers S01–S10 and literature identifiers L1–L3 are defined in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md). Page numbers refer to the final 243-page native main, not the superseded initial 244-page build. The historical source-directory name `A2-v17` does not identify the revision being reviewed.

## Recommendation

**I do not recommend acceptance at the requested highest-level general-journal standard. My recommendation is editorial rejection of this submission at that level, not a technical rejection based on a demonstrated false theorem.** Within the fresh proof coverage specified below, I have not found a fatal error in the new quantized-law inverse or its conditional sampling corollary. This distinction is essential: an adverse placement judgment must not be converted into a fictitious mathematical gap.

Revision 46 makes a genuine advance over revision 45. In particular, the concrete criticism that the manuscript has no quantitative inverse from observation-law error to the entire boundary is now superseded. Section 19 starts from finitely many histogram probabilities, not derivatives of an observed density or already reconstructed curve images. It supplies an explicit finite-order accuracy prescription, not an unnamed compactness separation constant. It also reconstructs the unknown marked Euclidean lattice rather than assuming the lattice metric as calibration. These are substantive favorable findings. [S01–S03]

My remaining reservation concerns the strength and conceptual reach of the contribution at the exceptionally selective level requested. The new theorem quantifies an existing inverse by a finite Bellman recursion, classical conditional analytic continuation, and finite registration algebra. That composition is useful and mathematically nonvacuous. I nevertheless do not judge it, together with the inspected inherited core, to establish an exceptional general-mathematical advance warranting this placement. This is an evaluative judgment, not a theorem about what a journal must publish, not an exhaustive priority conclusion, and not a claim that the program should be abandoned. An editor could reasonably assign greater significance to the relative nonlinear inverse and reach a different decision.

## 1. Disposition of the preceding report

| Previous finding or objection | Present disposition |
|---|---|
| R45-P1: the common-frame paragraph should use a zero-net-gain backtrack | **Corrected.** The proof of Theorem 18.7 now uses the required wording. No individually zero-marked edge is assumed. |
| Generic determination had replaced the earlier special-realization restriction | **Retained.** There is no reason to revive the superseded example-only objection. |
| Finite smooth-remainder factorization was not merely formal Taylor algebra | **Retained and freshly checked at the interface needed here.** |
| A quantitative observation-law-to-whole-table inverse was absent | **Substantively superseded by Theorem 19.5 and equation (19.17).** This is not an image-space estimate with a new title. |
| The richer position experiment also permits direct graph interpolation | **Still true for that richer record, but not a refutation of Section 19.** The new reconstruction transcript omits longitudinal positions. |
| Current native delivery and source identity | **No outstanding objection on the checks performed.** Separate rebuilding and scoped inspection are documented below. |
| Exceptional general-journal significance | **Reassessed, but still not established to my satisfaction.** This is not a binary proof-repair item. |

The author has responded to a substantive direction identified in the previous report. It would be unfair to dismiss this revision as another checklist or another build certificate. Equally, supplying that new theorem does not mechanically settle an editorial placement judgment. The two statements should be recorded separately. [S01, S02, S09]

## 2. What the new theorem actually proves

The design consists of a spanning tree and two selected non-tree channels, with N+1 channels for N obstacle orbits. Obstacle labels, deck labels, tree-path labels and the invertible integer gain matrix M are fixed. The Euclidean realization L of the marked lattice is unknown. The observation comprises the gaps and two same-type signed limiting endpoint laws per channel at a fixed positive offset. Only finite histogram vectors of those laws enter the quantitative estimate. [S03, Section 19.1]

The quantitative class has additional, explicit priors: a common bounded holomorphic strip for the contact-centered support functions; positive geometric, density and anchor margins; the finite forward derivative bounds required at the selected order; and nonvanishing finite Fourier witnesses whose indices have greatest common divisor one. These are substantial assumptions, but they are legitimate conditional-stability assumptions, not supplied values of the unknown support functions. The author correctly distinguishes neighborhoods in a bounded holomorphic-support norm from the relative C² topology of the earlier genericity theorem.

For the maximum gap discrepancy e_g and histogram discrepancy e_p, the input to the modulus is

\[
 \eta=e_p+C_{\rm bin}\delta,
\]

where delta is the grid mesh. The conclusion controls the labelled obstacle images and L modulo one common proper Euclidean motion. On the prescribed bounded class it also controls the marked lattice Gram matrix. The representatives and deck marks are not independently changed inside the distance. [S03, equations (19.4)–(19.5), Theorem 19.5]

Thus the theorem gives finite scalar information for each prescribed positive geometric accuracy, with the number and accuracy of the scalars allowed to increase. It does not assert exact recovery of arbitrary analytic boundaries from one fixed finite list of scalars. Nor does it discover an unmarked design. These restrictions are printed, not missing hypotheses discovered by this referee.

## 3. Fresh proof audit of Section 19

### 3.1 Histogram probabilities really control a finite density jet

Lemma 19.1 first compares a density with its cell-average function on Q_1. Each replacement costs at most a constant times H_1 times the mesh. The L¹ difference of the two cell-average functions is exactly the sum of absolute cell-mass differences. This proves the required L¹ bound by eta without differentiating an empirical histogram.

For an interior square Q_0, the differentiated convolution estimate has cost

\[
 C h^{-m-2}\eta,
\]

where the exponent two is the dimension of the endpoint pair. The C^{m+1} forward bound supplies an approximation error C H_{m+1}h. Choosing h proportional to eta^{1/(m+3)} gives the asserted C^m estimate. The interior margin keeps all convolution points in Q_1. The product polynomial kernel has sufficient boundary regularity for the integrations by parts used. [S03, pp. 86–88]

This is not the false assertion that total variation alone controls derivatives. The forward regularity assumptions are doing essential work. The complement category is also correctly retained so that the recorded cells define a probability vector, while the proof needs derivative bounds only inside Q_1.

An exact functional negative control in the accompanying independent script confirms why the mesh term cannot simply be erased. On the unit square, the positive densities 1 and 1+(1/5)sin(14 pi x) have equal masses on all seven equal vertical cells, but their L¹ distance is 2/(5 pi). This is a test of the histogram argument, not a claimed realizable billiard counterexample.

**Finding R46-C1:** the passage from a finite probability vector to a fixed-order density jet is supported under the stated priors. It does not import a measured C^m density as an additional observation.

### 3.2 The finite Bellman recursion contains the lower-order terms

The most important addition is Lemma 19.2. The stationary half-line satisfies

\[
 S_b(u)=\ell_b(u,V_b(u))-g+S_{1-b}(V_b(u)),
 \qquad
 0=\partial_2\ell_b(u,V_b(u))+S_{1-b}'(V_b(u)).
\]

The scalar linearization in the stationary coordinate is g^{-1}+kappa_{1-b}+a_{1-b}, which is positive on the prescribed class. The slopes alpha_b satisfy alpha_0 alpha_1=e^{-2 gamma}. At order n, with the lower jets already known, the coefficient equation is

\[
 (I-B_n)s_n=(I+B_n)q_n+P_n,
 \qquad
 B_n=\begin{pmatrix}0&\alpha_0^n\\\alpha_1^n&0\end{pmatrix}.
\]

Here P_n is not an unspecified inverse remainder. The manuscript explains how to compute it by setting the new order-n coefficients to zero, solving stationarity through degree n-2, and substituting into the action. The omitted degree-(n-1) term in V_b changes a stationary value at order 2n-2, which exceeds n for n at least three. The separate quadratic recovery handles n=2. Both I-B_n and I+B_n have determinant 1-e^{-2n gamma}; consequently the leading inverse block is well defined and the inherited forward block has determinant one. [S03, pp. 88–89]

I independently checked the cubic and quartic identities by exact symbolic arithmetic at a nonsymmetric rational quadratic geometry, leaving the new cubic and quartic graph coefficients symbolic. The identities and determinant agree. A negative control which suppresses the quartic lower-order remainder produces nonzero errors, so the test is not merely verifying the leading two-by-two determinant. These finite calculations support the coefficient bookkeeping; they do not independently establish the infinite half-line construction.

That latter distinction is covered by an actual inherited lemma, not concealed by the calculation. The smooth finite-jet factorization proof interpolates graph functions with equal finite jets, differentiates finite stationary actions, controls the terminal orbit term, and passes to the limit under a summable bound. It gives an action difference O(|u|^{M+1}) from graph differences of that order. This justifies the dependence on finite jets before polynomial representatives are used. I freshly inspected this functional-remainder argument. [S04, Lemma 12.4, source lines 298–404]

The graph-to-support step is also consistent. In the individual outward-normal frame, the equation psi'(y)=tan(theta) and the stationary expression

\[
 h(\theta)=-\psi(y(\theta))\cos\theta+y(\theta)\sin\theta
\]

give h''(0)=1/kappa. The same stationary cancellation controls the higher-order truncation. The sign reversal of the proper tangent at the opposite contact is explicitly addressed. It is a known coordinate conversion, not an unknown pose supplied to the inverse.

Finally, the prescription for A_m lists finite product, reciprocal, root and implicit-series operations with positive denominator bounds. The four-density inverse is compared at its two realizable endpoints; it does not assume that an interpolating density still has the special factorization. The manuscript neither requires nor claims that A_m is bounded uniformly in m. [S03, p. 89; S05]

**Finding R46-C2:** this is a finite algorithm for the order-dependent conditioning constants, not an appeal to an unspecified infinite-dimensional inverse modulus. It is also not, by itself, a computationally efficient inverse on an arbitrary analytic model class.

### 3.3 Continuation from a finite jet is quantitatively justified

Lemma 19.3 uses r=min(s/8,1/8), J_s=ceil(pi/r)+1 and beta_s=2^{-J_s}. A radius-4r disk centered on the real line lies strictly inside the bounded strip. Cauchy's estimate therefore bounds the unobserved Taylor tail on the initial radius-r disk by

\[
 \frac{8B}{3}4^{-m-1}.
\]

The three-circles inequality at radii r, 2r and 4r changes a small bound v into at most sqrt(2B v). Moving the center by at most r and iterating yields the printed exponent. The additional coverage margin permits smaller disks about every real point, which justifies the claimed fixed-order derivative bounds. Periodicity closes the passage around the boundary. [S03, pp. 89–90]

The argument uses an actual common analytic bound; equality of formal infinite jets is not being treated as a quantitative continuation principle. The exponent is very conservative, but I found no invalid exchange of limits or unsupported global continuation step here. The classical nature and ill-conditioning of this procedure are acknowledged; the Trefethen reference provides relevant context rather than a substitute proof. [L1]

### 3.4 General finite witnesses register the images in one frame

The phase convention in Lemma 19.4 is correct. For a proper congruence C_t=e^{i omega}C_s+t, normalized Fourier coefficients satisfy p_k(C_t)=e^{-ik omega}p_k(C_s). Hence

\[
 \prod_{k\in F_a}\left(\frac{p_k(C_s)}{p_k(C_t)}\right)^{b_{a,k}}
 =e^{i\omega}
\]

when the Bezout coefficients satisfy sum k b_{a,k}=1. No root or argument branch is selected. This works for witnesses such as {4,9}, and also for gcd-one sets having no coprime pair, such as {6,10,15}. The independent script checks the latter case as well. [S03, p. 90]

The positive harmonic margins give a Lipschitz bound for normalized phases. The translation-covariant center supplies translations, and finite tree propagation puts all edge displacements into one root frame. The two cycle defects equal L times the two fixed gains. Multiplication by the actual M^{-1} recovers L; no unimodular-pair assumption has been substituted. The representative correction uses this same L throughout. Uniform support distance is the Hausdorff distance for convex bodies, and the bounded first derivative of the supports controls small registration rotations. The Gram estimate then follows directly on the bounded class. [S03, S06]

**Finding R46-C3:** the quantitative registration covers arbitrary prescribed finite asymmetry witnesses. It does not retreat to the two-harmonic example, erase the common-frame requirement, or assume the unknown lattice.

### 3.5 The modulus is not circular

For each fixed m, the four lemmas give a valid table bound. Taking the infimum over m in equation (19.15) preserves the inequality. Its convergence to zero follows by choosing a fixed m large enough to make the analytic tail small and only then decreasing the observational errors. No uniform control of A_m as m tends to infinity is needed.

More importantly, equation (19.17) removes any need to evaluate the infinite infimum. Given a target epsilon, the displayed formula first specifies a positive v, then a finite jet order, then finite gap and histogram accuracies and a finite mesh. Substitution yields the claimed bound. This is a genuine constructive accuracy prescription at the level asserted. [S03, p. 91]

It may be extremely expensive. For illustration only, substituting s=1, B=2, C_reg=10 and epsilon=10^{-3} gives J_s=27 and a sufficient jet order 1,093,049,875 in the printed prescription. This is log-domain arithmetic with illustrative constants, not a certified instance of a particular periodic table. It is neither a necessary-order lower bound nor a minimax obstruction. The author already warns about potentially enormous conditioning, and the theorem does not promise practical performance. The example simply prevents interpreting the word quantitative as a demonstrated usable statistical rate.

### 3.6 Sampling, selection and caps are handled in the right order

Corollary 19.6 uses the expectation bound E||p_hat-p||_1 at most sqrt(K_delta/n), followed by bounded differences with single-sample sensitivity 2/n. The resulting tail exp(-nt²/2), union bound over the 2N+2 laws, and factor two converting total variation to vector L¹ discrepancy are consistent.

The confidence set contains the true limiting vectors on the coverage event. Triangle inequalities produce the factors two in the gap and probability arguments of Omega. The measurable approximate selector uses a nonnegative excess residual over a countable dense set; a positive selection tolerance enlarges the two error arguments. Compactness supplies a selector here, not the inverse modulus proved earlier. [S03, pp. 91–93]

The charged acquisition argument also avoids the common stopping mistake. Concentration is applied to the uncapped iid stream of successful categories; cap failure is added afterward. It is not asserted that conditioning on completion of the cap preserves the original iid law. The lower success bound and cap chosen in equation (19.20) give the stated binomial failure control. The separate gap-event failure probability can be added without assuming independence, provided the sampling bound is uniform as stipulated.

**Finding R46-C4:** the conditional categorical confidence construction survives this audit. It is not a newly proved sharp statistical experiment equivalence or an optimal reconstruction rate, and the manuscript does not label it as either.

## 4. One minor clarification about calibration, not a counterexample

### R46-P1 — make the exact-offset premise adjacent to the sampling radius

Corollary 19.6 assumes calibrated signed charts and marks with the stated fixed-offset finite-flight bias. Its supplied gap error is used to define the candidate set. That is a valid conditional formulation. For maximal clarity, add a sentence next to equation (19.19) saying that b_j there accounts for finite-flight error in those calibrated laws and does not, without an additional estimate, also account for imperfect timing or chart calibration.

The distinction matters if a reader programs t=j g_hat+d_0. The true offset is then d_0+j(g_hat-g). Thus a physical implementation using estimated onsets needs the corresponding timing term, not just the unmultiplied gap error in the candidate geometry. Hard histogram cells also require control of probability crossing cell boundaries under chart error; the bounded-Lipschitz test estimate cannot simply be applied verbatim to indicator functions.

I checked the existing physical implementation before classifying this point. Part III already chooses the final even flight number J before the pilot, runs that pilot at the same J, and controls J|g_hat-g|. It bounds offset error by total-variation continuity and chart error for the bounded-Lipschitz tests actually used there. Section 19 expressly presents the richer position pilot as separate and excludes calibration discovery from the compressed transcript. Therefore this is **not** a newly discovered defect in that pilot, a refutation of Theorem 19.5, or a missing premise that invalidates the conditional corollary. A short explicit cross-reference and distinction suffice; a new uncalibrated histogram theorem is not being demanded. [S03, p. 93; S07, source lines 184–266; S08, source lines 130–173]

An independent functional check illustrates the timing issue without alleging a billiard counterexample. For normalized two-dimensional quadratic-cap densities at positive offsets d<D, the exact total-variation distance is (D-d)/(D+d). Taking D=d+j epsilon exhibits a first-order j epsilon contribution. It is an error-model diagnostic, not a contradiction to a theorem assuming the correct offset.

## 5. Significance at the requested journal level

### R46-E1 — the quantitative gap is closed, but my placement judgment remains adverse

The strongest feature of this program is the nonlinear local inverse: relative normalization on long bridges, functional control of smooth finite remainders, and recovery of signed contact jets without reflection symmetry or supplied curvature. It would be inaccurate to reduce that work to the final four-density identity or the determinant-one block. The generic availability theorem also genuinely changes the geometric domain of the result. These favorable conclusions should not disappear merely because this report has an adverse recommendation.

The new quantitative contribution must nevertheless be assessed at its actual level. Once a finite smooth jet inverse has been obtained, the route from cell error to a finite jet, then to a bounded analytic function by continuation, and then to a finite registered configuration is a natural conditional-stability composition. The finite Bellman recipe is the substantive new link in that composition. The remaining estimates make the old inverse effective in a specified observation norm; they do not identify a new rigidity mechanism independent of the existing jet inverse. In my judgment, this is a useful quantitative completion rather than a further advance of the breadth or conceptual force needed to change the venue recommendation.

That judgment does not rest on saying that the theorem has infinitely many measured scalars at each fixed accuracy: it does not. Nor does it rest on calling the modulus nonconstructive: its accuracy prescription is finite. Nor may the direct longitudinal-position benchmark be used to dismiss this theorem: those coordinates are absent from its reconstruction transcript. Those would all be inaccurate criticisms of revision 46.

The price of the result is instead visible in the assumptions and the kind of consequence established. The quantitative theorem is conditional on analytic width, analytic size, finite-order forward bounds and quantitative asymmetry margins. It does not provide a class-wide conditioning law for the earlier C²-open dense locus. Its sampling result propagates categorical concentration through the conditional modulus, without identifying a new information threshold or an optimal dependence on analytic width and observation accuracy. These are descriptions of the proven contribution, not allegations of omitted hypotheses. I do not require a sharp minimax theorem as a retroactive premise of the theorem submitted.

The sample and preparation bounds reinforce existence at finite accuracy, but they are not an independent demonstration of exceptional statistical significance. Conversely, the poor sufficient numerical prescription is not by itself a reason to reject a pure mathematics paper. The placement assessment turns on the mathematical contribution as a whole, not on whether its algorithm is practical.

The literature comparisons remain observation-specific. Finamore–Leguil prove a rigidity result for finite-horizon Sinai billiards using an enriched marked length spectrum, not the selected endpoint-law datum used here. No reduction between those observations is established by the materials examined. Their result therefore does not prove this inverse is already known, and the present theorem should not be advertised as removing hypotheses from that different theorem. [L2]

The version-sensitive Florio–Leguil citation is likewise not an outstanding defect. Its v5 notice removes an earlier geometric spectral-rigidity assertion affected by an error while retaining dynamical conjugacy results. That distinction should remain explicit, as it is in the manuscript's treatment. The present literature check is limited; it cannot establish an exhaustive priority claim. [L3]

A 243-page manuscript can be appropriate for a sufficiently important theorem. Its length, number of retained environments, or number of successful builds is neither evidence for exceptional significance nor a reason to demand arbitrary deletion. The article's accumulated local-experiment and physical-acquisition conclusions should be evaluated individually rather than counted as additional independent breakthroughs merely because they are presented together. I have not freshly re-refereed all of those inherited conclusions and do not use them as independently certified grounds either for acceptance or for rejection.

There is no hidden request here for another round adding unmarked discovery, fixed-finite-scalar exact determination, a sharp minimax theory and a spectral-data reduction simultaneously. Those would be distinct research contributions. The author should not be asked to keep satisfying a moving list while the same editorial reservation is relabelled as an unresolved proof gap.

## 6. Independent verification and its limits

The final native artifact was downloaded through GitHub Actions and its SHA-256 checked. All 34 evidence entries listed in the native build report and all 101 active source entries were checked against the extracted archive. The companion and complete main were rebuilt separately, companion first, with shell escape disabled. Both commands succeeded. All 250 pages match their native counterparts in extracted text and same-renderer 72-dpi pixels. The PDF byte streams differ and are not claimed to be identical. The main rebuild has five underfull-box notices, no overfull-box notice and no unresolved citation or reference; the companion has no such warning. [S10; CHECK_RESULTS.json]

Readable-resolution visual inspection in this review covered main pages 88–93. No clipping, overlap or broken mathematical layout was observed there. Whole-document pixel comparison is a separate reproducibility check, not a claim that every page was individually visually inspected.

The accompanying independent script imports no author diagnostic. Ordinary and optimized Python executions produce identical JSON. It checks exact cubic/quartic Bellman identities, a lower-remainder negative control, 300 Bezout phase cases, exact histogram aliasing, offset sensitivity and log-domain arithmetic for the stated accuracy prescription. The author's preservation and finite-chain scripts were separately rerun under ordinary and optimized Python; those results are labelled as author-code reruns, not as this referee's independent implementation.

The fresh mathematical audit covers the complete new Section 19, its introductory statement, the directly used finite-jet and density-inverse mechanisms, the relevant generic-registration construction and the specified physical-calibration interface. It does **not** constitute a new line-by-line proof audit of every relative-operator estimate, LAN theorem, Poisson deficiency argument, deconvolution result, appendix or companion theorem in the retained corpus. Successful compilation, finite symbolic checks and earlier referee findings do not fill that gap in coverage. No formal mathematical certificate is claimed.

## Final disposition

Revision 46 should be credited with a genuine conditional quantitative inverse from finite transverse-law histograms to the complete labelled periodic table and unknown marked lattice. The old assertion that only an exact inverse or recovered-image stability is available is no longer tenable. The new proofs inspected here withstand targeted adversarial checking, and the source-matched native delivery is reproducible.

I nevertheless do not support acceptance at the requested highest-level general mathematics journal on my assessment of the demonstrated contribution. The recommendation is editorial, not a claim of mathematical impossibility or a technical rejection supported by an invented counterexample. The calibration clarification is minor and is not the reason for the adverse recommendation. Preserve the valid theorems and their honest qualifications; do not weaken them or delete mathematics merely to turn this judgment into a nominally closed checklist.
