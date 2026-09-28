# Independent referee-style report on A2, revision 52

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*, Qian Qi.  
**Assessment date:** September 15, 2026.  
**Requested standard:** the leading general mathematics journals.  
**Recommendation:** **Do not accept at the requested level on the contribution and article-level case established.** This recommendation is an editorial assessment, not a finding that a principal theorem has been disproved. No newly established fatal mathematical error was found in the technical coverage specified below.

This is an author-requested, AI-assisted referee-style assessment, not a commissioned journal report or an institutional endorsement. The assessment is of a frozen mathematical submission, not of its revision count, build status, or earlier referee-style conclusions. Source identifiers [S1]–[S11], primary references [L1]–[L5], and reproduction evidence [D1] are specified in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md).

## 1. Submission, coverage, and principal assessment

The reviewed delivery is `revision/a2-v52-review-ready-2026-09-15`, frozen at **`95046e3b4fce025e5763b555c38180339d4869a0`**. Its actual compiled mathematical source is **`9fd0c14c7b3fd816bdb9d7c3db0fdbae2104dcd6`**, under `papers/A2-v17-boundary-information-coarsening`. The historical directory name does not identify the revision. The complete article has **273 pages**, and the complete two-collision companion has **7 pages**. The workflow preparation commit, compiled source commit, product commits, and review-ready commit are distinct and are not interchanged in this report. [D1]

Revision 52 adds Lemma 14.5, Theorem 14.6, and Corollary 14.7. It acknowledges the preceding referee's support-width centering observation, formulates extraction from a positive interior recording window, and proves the corresponding geometric-fiber and differential-kernel statements. The abstract and introduction now distinguish inherited association algebra from the relative boundary-law and actual-smooth signed inverse. Equation (1.6) identifies a common unnormalized measure behind the article's different observations. Theorems A and B and the inherited proof corpus remain. [S1, S2, S10]

Fresh technical coverage includes the complete new module, its introductory interpretation, the local origin/action extraction on which it depends, the relative long-bridge factorization, the actual-smooth finite-jet argument and determinant-one recursion, registered analytic continuation, finite congruence enumeration, and the differential registration/lattice interfaces. I also checked the finite-coordinate argument and the stated calibration-to-histogram interface. I have **not independently re-proved every statistical experiment, minimax assertion, analytic continuation estimate with quantitative rates, global estimator, pilot construction, or auxiliary result in the companion**. Reproducing all pages does not certify all their mathematics.

The principal findings are these. The window theorem survives the checks below and genuinely removes the need to observe the cap boundary. The preceding report's bounded editorial requests have been addressed; they should not be kept open by changing their meaning. Nevertheless, the new formulation is a consequence of the existing interior extraction, rather than another difficult inverse mechanism. A new quantitative benchmark in Section 4 shows how little uniform statistical information an exactly identifying window can contain. That benchmark is not a counterexample to a theorem which expressly permits its constants to deteriorate.

## 2. Disposition of the previous report

**R52-C1 — The support comparison is acknowledged correctly.** Lemma 14.5, pages 61–62, gives the complete-support argument without an evenness assumption. If $v_-(q)<0<v_+(q)$ are the inverse branches of $S(v)=q$, then

$$W'(q)=\frac1{S'(v_+(q))}-\frac1{S'(v_-(q))}>0.$$

The vertical width is $W(d-S(x-\xi))$. Its unique maximum is at $\xi$, and its second derivative there is $-W'(d)S''(0)<0$. The compact-sublevel margin justifies the inverse-branch derivatives near $q=d$. Horizontal fibers give $\eta$. Positive endpoint factors do not alter this support. The statement is attributed to the preceding memorandum and is not represented as an additional author-originated high-order inverse. [S2, lines 1–54]

The revision also makes the correct limitation explicit: locating the origins from a complete support is not the same as recovering the action, and a support-boundary argument does not supply an estimate from an interior smooth norm. It would be incorrect to repeat the old criticism as though these distinctions were still absent.

**R52-C2 — The interior advantage is now in the statement, not only the proof.** Theorem 14.6 observes only a known product window. Its support is fixed and cannot center the action by varying fiber widths. The numerical origins are not supplied, and neither the discarded mass nor the cap boundary is supplied. This is a genuine reduction of the observation relative to the complete-cap version. It is not merely a renaming of Lemma 14.5. [S2, lines 56–165]

**R52-C3 — The requested synthesis has been supplied.** The introduction now uses the unnormalized relative boundary measure to explain endpoint laws, residual-time records, and preparation frequency, while preserving their different hypotheses. The response does not pretend that one observation theorem implies all later statistical results. This closes the preceding request for an explicit relationship among the parts. Whether that relationship warrants this particular general-journal treatment remains a separate editorial judgment. [S1, S10]

No further appended theorem is required merely to answer those three already addressed requests.

## 3. Technical examination of the window extension

### R52-M1. Identification uses precisely the retained critical lines

On $\mathcal W=J_x\times J_y$, the model is

$$p(x,y)=\frac{A(x)C(y)}{Z_{\mathcal W}}\,H(x,y),\qquad
H(x,y)=d-S(x-\xi)-S(y-\eta)>0,$$

with $\xi\in J_x$, $\eta\in J_y$, known $d>0$, $S(0)=S'(0)=0$, $S''>0$, and separate positive smooth factors. The strict positivity extends to the closed window. Signed units and coordinate directions are still fixed. [S2, lines 56–104]

On its interior,

$$\mathcal K_p:=\partial_x\partial_y\log p
=-\frac{S'(x-\xi)S'(y-\eta)}{H(x,y)^2}.$$

For any $x\ne\xi$, the interaction cannot vanish identically on its vertical fiber: the open interval $J_y$ contains points different from $\eta$, and strict convexity makes $S'$ vanish only at zero. At $x=\xi$ it does vanish identically. The horizontal argument is identical. Thus the origins are recovered without a boundary value. The positive smooth representative of the density is determined by its almost-everywhere class, so these interior evaluations are legitimate.

After recentering, the four-density ratio satisfies

$$R(u,v)=\frac{p(\xi+u,\eta+v)p(\xi,\eta)}
 {p(\xi+u,\eta)p(\xi,\eta+v)},\qquad
1-R(u,v)=t(u)t(v),\quad t(u)=\frac{S(u)}{d-S(u)}.$$

Both different endpoint factors and the unknown window normalizer cancel. A small nonzero anchor $a$ gives $q=\sqrt{1-R(a,a)}=t(a)>0$, followed by

$$T(u)=\frac{1-R(u,a)}q,\qquad S(u)=\frac{dT(u)}{1+T(u)}.$$

The square root is taken at a positive scalar anchor, not at the degenerate minimum. Negative and positive coordinates are treated separately, so odd action coefficients are not discarded. Substitution on the two axes recovers effective factor ratios, not a separation of physical amplitudes from recording efficiencies. [S2, lines 107–136; S3]

**Finding:** no identification error found. The theorem is conditional on a suitable window containing both critical coordinate lines. It does not provide an unmarked procedure for finding that window, recover an unknown transverse scale, or tolerate an arbitrary joint recording factor. These restrictions are printed in the submission rather than concealed in the proof.

### R52-M2. The regularity claim is local and its derivative bookkeeping is adequate

Theorem 14.6 states a local $C^1$ extension from $C^{m+3}(Q)$ into $\mathbb R^2\times C^m([-r,r])$ for each separately fixed $m$. On a fixed noncentral slice, for example,

$$\partial_x\mathcal K_p(\xi,y_*)
=-\frac{S''(0)S'(y_*-\eta)}{[d-S(y_*-\eta)]^2}\ne0.$$

The map $p\mapsto p_{xy}/p-p_xp_y/p^2$ is continuously differentiable on a positive smooth neighborhood with the stated derivative loss. Two scalar implicit-function arguments produce the origins. Restriction after translating by the extracted origins is differentiated with spare derivatives; it retains both transport terms. The ratio construction then uses positive axis denominators and a positive scalar anchor. Its derivative must differentiate that anchor, and the source does so. A smaller convex neighborhood has a bounded derivative and therefore the displayed local Lipschitz estimate. [S2, lines 138–155; S3, lines 182–276]

There is no illicit differentiation across the cap boundary or the recording-window edge. For arbitrary nearby nonmodel inputs this is only a local extension; exact identification is asserted on the model class. The constants depend on density, root, anchor, and window margins. No total-variation estimate, optimal derivative loss, or uniformity as these margins vanish is established or claimed.

The independent implementation checks a non-even action, unequal factors, moving origins, the anchor derivative, and the fixed-window normalizer. Deliberately freezing the origins, omitting the anchor derivative, or omitting the normalizer derivative produces a nonzero diagnostic error. These checks corroborate finite formulas, not the infinite-flight arguments. [D1]

### R52-M3. Both directions of the geometric-fiber assertion are present

Corollary 14.7 requires more than the implication “cropped laws determine jets.” Its forward direction extracts both signed action germs for each channel, uses the gap and quadratic coefficients to recover the leading geometry, and invokes actual-smooth finite-jet factorization before applying the higher-order inverse. Analyticity then determines complete ordered channel-frame images. Every realization of the cropped records is consequently in the inherited compatible table fiber. [S2, lines 170–202; S5–S7]

For the reverse direction, an accepted ideal branch places each entire recovered ordered channel pair by a proper Euclidean motion. The physical local actions and amplitudes agree. Reusing the original numerical origins, windows, and recording profiles gives the same normalized window law; the overall phase-volume constant cancels. This establishes equality of fibers, not merely a finite upper bound on possible realizations. The marked lattice is still reconstructed with the actual inverse of the integer gain matrix, not by assuming that matrix is unimodular.

For parameter families the windows are fixed and their positivity and visibility conditions persist. With $w=AC$, differentiation gives

$$\dot Z_{\mathcal W}=\int_{\mathcal W}(\dot wH+w\dot H),$$
$$\dot H=-\dot S(x-\xi)-\dot S(y-\eta)
+S'(x-\xi)\dot\xi+S'(y-\eta)\dot\eta.$$

The offset is fixed in this statement. There is no moving integration boundary. Stationary density implies stationary extracted origins and action jets. The finite recursion retains every term:

$$\dot q_n=M_n^{-1}(\dot s_n-\dot R_n-\dot M_nq_n).$$

The common-strip hypothesis makes the support variation itself analytic, allowing the identity theorem. Following the actual continuous congruence branch avoids assuming that every finite symmetry survives perturbation. The displacement cochain then removes the lattice derivative in one common Euclidean gauge. Conversely a common proper Euclidean motion with suitable fixed intrinsic recording profiles leaves the data stationary. [S2, lines 204–236; S8]

**Finding:** no new fiber or derivative-kernel failure found. The conclusion concerns the projection of a joint derivative kernel onto table variations, not identification of every nuisance profile. Exact injectivity is not being substituted for derivative injectivity.

### R52-M4. The recording and finite-flight interpretations have the right quantifiers

On the relevant compact intervals the effective-to-physical factor ratios are smooth, positive, and bounded. Extending their logarithms by cutoffs, exponentiating, and multiplying by small positive constants realizes them as separate probabilities at most one. Those constants cancel after conditioning. The crop itself is a product of interval indicators.

For fixed weights and a fixed window, weak convergence of the ideal endpoint laws passes through reweighting and cropping because the four edges have zero limiting mass. The positive limiting denominator then permits normalization. This is a fixed-observation limit, not a rate uniform over vanishing efficiencies or accepted masses. The final paragraph expressly separates successful records from charged preparations. These are the quantifiers needed; I do not identify a missing uniformity theorem which the paper never asserts. [S2, lines 238–271]

## 4. A new quantitative benchmark: an identifying window can carry vanishing information

**R52-Q1 — Exact geometric-fiber equality must not be read as uniform statistical information preservation.** The following independent calculation concerns the functional observation model of Theorem 14.6. It is not a claimed realization theorem for arbitrary actions by global periodic billiards, and it is not a counterexample to Corollary 14.7.

Fix known $d>0$, origins zero, and two distinct positive constants $a,b$. For a small half-width $h$, take

$$S_a(u)=\frac a2u^2,\quad \mathcal W_h=(-h,h)^2,\quad
A_a(u)=\frac1{d-S_a(u)},\quad C_a(v)=\frac1{d-S_a(v)}.$$

For sufficiently small $h$, all the strict positivity and visibility hypotheses hold. These separate factors are smooth near the closed coordinate intervals and may be rescaled without changing the conditional law. With $t_a(u)=S_a(u)/(d-S_a(u))$,

$$A_a(u)C_a(v)[d-S_a(u)-S_a(v)]
=\frac1d[1-t_a(u)t_a(v)].$$

Under the known rescaling $u=hz$, $v=hw$, the normalized density on $[-1,1]^2$ is

$$q_{a,h}(z,w)=\frac{1-t_a(hz)t_a(hw)}
 {4-\left(\int_{-1}^1t_a(hs)\,ds\right)^2}.$$

Since $t_a(hz)=a h^2z^2/(2d)+O(h^4)$ uniformly, expansion of both numerator and normalizer gives

$$q_{a,h}(z,w)=\frac14+
\frac{a^2h^4}{16d^2}\left(\frac19-z^2w^2\right)+O(h^6).$$

Consequently the total-variation distance between the two conditional laws is $\Theta(h^4)$, although their quadratic action coefficients differ by the fixed amount $a-b$. With the explicit convention

$$H^2(P,Q)=\int(\sqrt p-\sqrt q)^2,$$

the sharper expansion is

$$H^2(q_{a,h},q_{b,h})
=\frac{7(a^2-b^2)^2}{16200d^4}\,h^8+O(h^{10}).$$

Indeed, the leading difference of square roots equals the leading difference of densities because the common limiting density is $1/4$, and

$$\int_{[-1,1]^2}\left(\frac19-z^2w^2\right)^2\,dz\,dw
=\frac{224}{2025}.$$

For $n$ iid successful window records, Hellinger affinity tensorizes. Thus $H^2(P^{\otimes n},Q^{\otimes n})\le nH^2(P,Q)$, while $\operatorname{TV}(P,Q)\le H(P,Q)$ under this convention. If $n_hh^8\to0$, the product total-variation distance tends to zero and the minimum equal-prior testing error tends to $1/2$. Achieving a fixed nontrivial testing advantage therefore requires, in this two-point functional example, successful-record sample size at least of order $h^{-8}$. This is a necessary scale, not an asserted sufficient procedure or an optimal global minimax rate.

The attached independent calculation checks the exact rational coefficient for $a=1$, $b=2$, $d=3$, namely $7/145800$, and corroborates it by quadrature over decreasing windows. The proof is the expansion and tensorization above, not a numerical fit. [D1]

There are three important limits to this criticism. First, exact identification at every fixed $h>0$ remains true. Second, the smooth local inverse permits its constants to depend on the shrinking window and anchor margins; the example does not refute it. Third, exact quadratic actions here have not been constructed as actions of a prescribed global analytic periodic table. The calculation establishes a benchmark for the stated functional nuisance model, not a billiard-class minimax theorem or a fixed-window deficiency lower bound against a specified richer experiment.

Its relevance is nevertheless concrete. Discarding the cap boundary may preserve the exact invariant while making estimation arbitrarily difficult. A finite number of channels still supplies function-valued data, and an exact algebraic cancellation of nuisance factors does not make successful observations or their acquisition uniformly informative. The manuscript's qualifications on page 8 and pages 61–64 are compatible with this benchmark. This is an interpretation test, **not a request to append another theorem or to prove uniform bounds already excluded by the statement**.

## 5. Fresh checks of the inherited mathematical mechanism

### R52-M5. The relative long-bridge law remains the substantive forward step

Theorem 7.2, pages 18–20, cannot be justified by dividing an arbitrary absolute error by an exponentially small reference twist. The reference is $d_j^0=q_p/\sinh(j\gamma)$. The source instead normalizes through the cofactor identity and a determinant of the subtracted, localized Hessian:

$$\log b_j=\sum_{i=0}^{j-1}\log\{g[-\ell_{i\bmod2,uv}(y_i,y_{i+1})]\}
-\log\det(I+G_j\Delta H_j).$$

I checked the half-line construction and the gluing/comparison argument rather than treating prior reports as certificates. The two endpoint tails give a summable Hessian perturbation. Gluing produces an exponentially small residual with a polynomial flight-length factor; uniform diagonal dominance controls the correction. Differentiating at each fixed order preserves the same principal inverse. The determinant comparison uses retained endpoint blocks, an entrywise summable tail, and exponentially small remote Green-kernel terms. In the trace-series comparison, telescoping powers keeps one trace-norm factor and controlled operator-norm factors. This is not an estimate obtained by multiplying an unweighted operator bound by the growing dimension. Fixed polynomial losses can be absorbed into a slower exponential rate. [S4, lines 11–250]

At fixed positive excess time the subsequent integration retains nonlinear half-line actions and endpoint amplitudes. It is not simply a Gaussian quadratic approximation. The factorized amplitude does not make the coupled positive cap a product observation. I found no new relative-normalization gap in this coverage. This argument carries substantially more mathematical weight than the later four-density cancellation. [S4, lines 252–327]

### R52-M6. The jet inverse is preceded by an actual-smooth argument

Lemma 12.4 and its surrounding proof do not merely manipulate formal series. For two actual smooth graph pairs with the same jets through order $M$, interpolate their graphs. The graph difference vanishes to order $M+1$. Evaluation along a uniformly decaying stationary half-line and the finite envelope identity produce a summable majorant. The terminal term is retained before passage to the limit. Integrating the finite identity in the interpolation parameter and then taking the half-line limit yields

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|
\le \frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

This proves finite-jet dependence of actual smooth actions, with constants requiring appropriate functional smooth bounds. Only then is the degree-$n$ last-jet block used. Boundary occurrences are counted once and interior occurrences twice, giving

$$M_n=\begin{pmatrix}
\coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\
r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)
\end{pmatrix},\qquad r_0r_1=1,\quad\det M_n=1.$$

The argument establishes a finite-order inverse and a finite-order tangent bound. It does not establish order-uniform conditioning or equality of arbitrary smooth germs from their Taylor series. Analytic continuation is a separate step, as it must be. [S5, especially lines 292–598; S6]

### R52-M7. Global and differential compatibility are not replaced by dimension counting

Finite noncircular symmetry permits finitely many exact alignments; it does not create an infinitesimal rotational symmetry. The source follows the actual local angular lift through the base alignment and allows symmetry breaking. The finite reconstruction checks ordered-pair consistency, lattice determinant, disjointness, and channel clearance. It uses $L=(v_1\ v_2)M^{-1}$ with the actual rank-two gain matrix. [S7]

The differential forward argument retains the moving reference:

$$\dot G=-G\dot H^0G,\qquad
\dot{\Delta H}=\dot H-\dot H^0,\qquad
\dot T=\dot G\Delta H+G\dot{\Delta H}.$$

The common-strip hypothesis is used to make the variation analytic; it is stronger than merely requiring every individual member to be analytic. After the geometric derivative kernel is removed, finite-dimensionality is used only to select a basis of scalar test derivatives on an immersed ideal-law model. The lower Lipschitz estimate is obtained by keeping the derivative close to one fixed invertible matrix on a convex ball, not by an invalid appeal to pointwise nonsingularity alone. [S8]

The selected-channel count is not a scalar-observation count. The finite-coordinate theorem uses exact expectations on a specified finite-dimensional ideal-law family. It is not extended to arbitrary infinite-dimensional recording profiles by Corollary 14.7.

The inspected hard-histogram interface likewise retains its separate assumptions. Its bias contains finite-flight, amplified clock/gap, and cell-edge terms,

$$2C_0\tau^j+2C_{\rm off}(jv_g+v_t)+2H_*V_\delta(r).$$

Conditioning first on a good pilot history, using fresh successful records, and charging capped preparations with a separate lower success bound are genuine parts of that argument. They are not replaced by the window inverse. This is an interface check, not a fresh proof of the complete pilot or all quantitative reconstruction theorems. [S9]

## 6. Literature, contribution, and placement

The targeted primary-source check confirms the appropriate distinction between association algebra and billiard reconstruction. Holland–Wang's dependence function and Osius's odds-ratio framework are established marginal-factor invariants. Osius's paper explicitly writes the four-density cross-product ratio. Revision 52 credits these ideas and does not claim to invent them. Their statistical conclusions cannot simply be transported to this cropped billiard experiment. My external check covered the relevant introductory definitions and bibliographic/abstract records, not a new proof audit of the entire external literature. [L1, L2]

The spectral-rigidity comparisons use different observations. The current Finamore–Leguil arXiv record concerns finite-horizon Sinai billiards with an enriched marked length spectrum. De Simoi–Kaloshin–Leguil concern analytic open billiards under non-eclipse and symmetry/genericity hypotheses. Florio–Leguil's fifth version expressly removes an earlier geometric spectral-rigidity assertion affected by an error; the present article does not import that removed result. No reduction between those data and the conditional endpoint laws has been established here. The search is not exhaustive and does not prove priority or redundancy of the present inverse. [L3–L5]

**R52-E1 — The strongest contribution is identifiable, but the new extension does not transform it.** The passage from exponentially rare physical bridges to a nonlinear relative law, and then from actual smooth actions to signed contact jets, is a substantial and coherent mechanism. It should not be dismissed as elementary cross-ratio algebra. Conversely, the newly weakened observation is obtained by localizing an already available extraction and composing it with the already available global inverse. It clarifies the reach of the main mechanism; it is not another independent mechanism of comparable depth.

My placement reservation concerns the return from that mechanism under the actual data supplied. The inverse starts from selected marked channels, known signed units and offsets, gaps, and exact function-valued local laws. In the window version it still assumes that the two critical lines are retained. Under these structured observations the local action is extracted by a direct invariant, and much of the subsequent exact global recovery is analytic continuation and finite congruence compatibility. Those are legitimate conclusions, not defects. But the observation strength must be counted when judging the scale of the inverse problem. The manuscript has not established that its datum is comparable in information content to a marked length spectrum, and the channel count must not stand in for a finite-data complexity claim.

On that basis, I regard the demonstrated result as a serious specialized inverse-dynamical contribution whose exceptional general-journal significance is not established to my satisfaction. That judgment is not a claim that the work is known, trivial, or impossible to strengthen. Another specialist may assign greater weight to the relative/smooth mechanism. It is also not a demand for an unspecified stronger theorem as a condition of closing this revision's concrete requests.

**R52-E2 — The common measure explains the article, but does not make the observations equivalent.** Equation (1.6) now gives an honest organizing object. Normalizing it, integrating residual time, or retaining its mass answers different questions. This materially improves the exposition. Nevertheless, the exact nuisance quotient, finite-smooth perturbation problem, finite-coordinate ideal model, and physically acquired histogram problem remain different mathematical experiments. Section 4 supplies a quantitative illustration of why the distinction matters even before preparation costs are considered.

I am not persuaded that the combination of the exact rigidity core and all of those separately conditioned statistical analyses establishes the degree of conceptual unity and broad consequence needed for the requested placement. This is not a numerical page-limit objection. The objection would remain if the same material were typeset more compactly. Nor does preserving 532 statement/proof blocks make that significance judgment cumulative: preservation is a provenance safeguard, not an editorial metric. The earlier request for an explanation has been answered; the explanation has not changed my placement recommendation.

## 7. Reproduction and final disposition

The authorized workflow artifact was downloaded and its SHA-256 checked against the GitHub artifact record. All **598 frozen source files** were checked by size, SHA-256, and Git blob identity. Reconstructing their directory objects gives manuscript subtree **`ba34d61e1eda687d1257be33d1cbae9758127d94`**, which is independently linked through GitHub's Git trees to the frozen compiled source. All **110 active inputs** and **34 native evidence files** match their manifests. [D1]

Both complete manuscript entries were rebuilt from the downloaded source with shell escape disabled, companion first. All **280 pages** agree with the native products in extracted text and in 72-dpi RGB arrays under the same PyMuPDF renderer. PDF byte identity is not claimed. Direct visual inspection was limited to main pages **8 and 61–64**. The final main log contains four underfull-box notices; the scan found no overfull box or unresolved reference/citation. [D1]

The author diagnostic was rerun under ordinary and optimized Python, with identical outputs matching the native retained output. Its preservation component finds 109 inherited active inputs, 104 byte-identical in place, five exact archived originals, and all 532 inherited statement/proof blocks, including 250 proofs, retained verbatim. The separately written reviewer implementation imports no author code and also gives identical ordinary and optimized outputs. None of these tests certifies unexamined theorems or the physical realization of the functional benchmark. [D1]

**Final disposition.** The bounded v51 editorial requests are addressed. The new window extraction, its stated local regularity, and the inspected geometric/differential interfaces survive this review. No mandatory theorem correction or newly established fatal proof error is identified in the stated coverage. The new small-window benchmark sharpens the interpretation of exact identification without contradicting the manuscript's qualifications. Nevertheless, **I do not recommend acceptance at the requested highest general mathematics journal level**, for the contribution and synthesis reasons above. This report should not be converted into either a full mathematical certificate or a mathematical impossibility claim.
