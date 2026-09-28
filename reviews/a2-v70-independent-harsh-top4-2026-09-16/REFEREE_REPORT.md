# Independent referee report on A2, revision 70

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment. It is not a commissioned journal report, an editorial decision, or a formal proof certificate. Correctness, originality, exceptional significance, presentation, and delivery integrity are assessed separately. Earlier reports are evidence to examine, not authorities whose verdicts are inherited.

## 1. Recommendation, object, and coverage

**Recommendation: do not accept at the requested highest general-journal level in the present form. The reorganization is a genuine improvement, and the central smooth-contact/finite-preparation chain withstands the scoped examination below. No new fatal mathematical error or mandatory core proof repair is established. The principal remaining problem is the case for exceptional originality and significance, including a concrete omission in the comparison with smooth obstacle scattering/lens rigidity.**

This recommendation does not mean that the theorem is already known, that detecting flat geometric information is impossible, or that a strong specialist result has no value. It also does not mean that another arbitrary theorem must be appended to manufacture a new repair cycle. Conversely, a correct proof and a reproducible delivery do not establish the threshold for the four requested journals.

| Reviewed object | Immutable identity |
|---|---|
| Compiled source | `16ec1030b9dfd9b185a1f0da8e50b10b40a71940` |
| Manuscript subtree, independently reconstructed | `63fdb25cd2002d9d2b3a238e7e7f1862b2328d2b` |
| Referee-ready head / parent of this review | `b529b340650f5582b1d04fabd599533450b51d0b` |
| Submission branch | `revision/a2-v70-referee-ready-2026-09-16` |
| Source branch | `revision/a2-v70-central-proof-architecture-2026-09-16` |
| Native workflow run / attempt / artifact | `35105117912` / `1` / `10449368306` |
| Previous independent report | `ba42d7a3a7873739c596497c5b2b884452f130d1` |
| Previous compiled source | `1a46fd69a508bccb90c6d2553892124f068f4657` |

The source directory is `papers/A2-v17-boundary-information-coarsening/`; its historical name is not the revision number. The principal article has **167 pages**, the full technical manuscript **343**, and the companion **seven**. Their overlapping contents must not be counted as 517 pages of distinct mathematical contributions. The compiled-source-to-submission comparison consists of three delivery/index commits and no changed manuscript input. The repository's directory metadata independently identifies the same manuscript subtree as the reconstructed archive. [D1, R2]

### Scope of fresh examination

The new introduction `article/00i_main_thesis_v70.tex` was read in full and its Theorems 1.1–1.2 checked against their actual dependencies. The fresh core examination covers all of the periodic relative-law module, the graph-coordinate/action-extraction/envelope/signed-jet portion of the periodic inverse module (lines 1–347), the complete global-curvature and corrected finite-iteration module, the complete smooth-contact module, and the complete finite-preparation module. The abstract, both entry files, author response, cover letter, dependency ledger, historical audit, literature note, and delivery index were also examined. [S1–S7]

This is **not a fresh line-by-line audit of every retained theorem in all 517 compiled pages**. In particular, the remainder of the analytic Banach inverse, all global registration/lattice and moving-family arguments, the older observation/coarsening catalogue, every earlier finite-chain prerequisite, and the companion are not independently certified here. The read physical/relative interfaces are examined substantively; successful compilation is not used to fill the remaining mathematical coverage gaps.

## 2. What revision 70 actually changes

The author correctly describes this revision as a consolidation, not a new collection of discoveries. The principal proof chain now begins on p. 7 rather than being submerged behind the earlier catalogue. The smooth inverse appears on pp. 27–33, and finite preparations on pp. 33–37. The introductory theorem is genuinely about the fixed marked experiment subsequently proved; it does not silently combine the stronger conclusions of several incompatible observation models. [S1, S7]

Independent comparison with a separately downloaded v69 artifact verifies that all **895** inherited source paths remain: **890 unchanged**, five modified, with byte-exact and mode-exact originals archived. All five central proof modules are unchanged. All **136** earlier active TeX inputs remain active; the new introduction and principal abstract raise the union to **138**. The two older introductory modules change only their opening section titles, while the entry files reorganize their inclusion. [D1]

| Prior issue | Disposition in this review |
|---|---|
| R69-M1–M5: forward bounds, interior estimation, realizable selection, rates, failed preparations | Re-examined at the operative interfaces; no regression found. The finite-preparation theorem remains a genuine observation advance. |
| R69-M6 and the v68 smooth-contact repairs | Re-examined, including the constant-one contraction and pair-dependent actual envelope. No regression found. |
| R69-E2 / D3: precise observation and regularity scope | Retained prominently in the new introduction. These are theorem hypotheses, not undisclosed loopholes. |
| R69-E3: the central proof is buried in the architecture | **Substantially closed.** The actual proof chain is now printed first. The remaining length is a presentation/placement consideration, not the same unresolved defect. |
| R69-D4 and the earlier ZIP-mode issue | No recurrence. Current raw archive modes match the Git manifest; previous source preservation verifies. |
| R69-E1 / D5: exceptional significance | Reconsidered on the improved presentation; still not established. The lens/scattering comparison in R70-E1 below is an additional concrete issue. |

It would be incorrect to continue claiming that the bounded, independently reset experiment requires an exact differentiated limiting density as supplied data. Section 6 estimates that norm and charges failures. It would likewise be incorrect to dismiss the smooth theorem as equality of Taylor series masquerading as equality of smooth germs. Its last step uses the actual functions. [S5, S6]

## 3. Mathematical examination

### R70-M1. The relative theorem addresses the right exponentially small quantity

**Locations:** Theorem 1.1, principal p. 3; Section 2, especially Theorems 2.3 and 2.5; S2.

For a returning period of length $P$ and $N=nP$, the reference mixed twist is

$$D_{N,b}=\frac{\sinh\chi}{(\mathcal M_b)_{12}\sinh(n\chi)},\qquad \operatorname{tr}\mathcal M_b=2\cosh\chi.$$

The geometric Jacobi operator has positive mass and nearest-neighbor off-diagonals. The transfer matrix and cofactor formulas give the same reference normalization. The finite and half-line Green estimates retain an exponentially small reflected-end error, and the weighted stationary construction controls the actual nonlinear bridges, not just the quadratic reference. Gluing the two half-lines leaves an exponentially small residual at each prescribed finite differentiation order. [S2]

The decisive determinant identity is formed **after dividing out the exact reference cofactor**:

$$\log\beta_N=\sum_i\log\frac{-\ell_{i,12}}{k_i}-\log\det(I+G_N\Delta H_N).$$

The Hessian perturbation is localized near the two ends, with a uniformly small trace norm on the collar. Cutting off the middle leaves two separated contributions; the trace-series comparison then gives the product of the two nonlinear endpoint amplitudes. The proof does not divide an uncontrolled absolute error by $D_{N,b}$. That would be a fatal error, but it is not the argument printed here. [S2]

The estimates are for every **separately fixed** finite derivative order. The constants are not asserted uniform in an unweighted all-jet norm. The slower exponential base can absorb the order-dependent polynomial factors without making this an analytic estimate. That quantifier distinction survives the new introductory formulation. [S1, S2]

### R70-M2. Physical normalization, graph sensors, and two-offset extraction are compatible

**Locations:** Theorem 2.5, pp. 12–13; Lemma 3.1 and Proposition 3.2, pp. 14–16; S2–S3.

The unconditioned endpoint measure contains the actual factor

$$\frac{D_{N,b}}{2\pi\mathcal A}\,\beta_{N,b}(u,v)
\{d-E_{N,b}(u,v)+p_bu-p_bv\}_+.$$

The linear momenta cannot simply be erased by calling the action gauged. The source restores them in the physical residual. The small positive time window, the specified itinerary, and the requirement of no further reflection make the time-split parametrization unambiguous. This is not a claim about an arbitrary maximal-collision event. [S2]

The measured graph coordinate is a tangent projection based on supplied marks, not an unknown arclength coordinate or the unknown graph height. The graph/arclength conversion keeps the gauge and endpoint Jacobians. For the limiting densities, write $H=A(u)+C(v)$ and

$$q=\frac{f_{d_1}(u,v)f_{d_2}(0,0)}{f_{d_2}(u,v)f_{d_1}(0,0)}.
\qquad
H=\frac{d_1d_2(1-q)}{d_2-d_1q}.$$

Unknown positive scalar normalizers and common amplitudes cancel. The denominator stays away from zero on the stipulated positive-residual square with separated offsets. The axes determine $A$ and $C$ because the anchored actions vanish at zero; the known momenta restore the future/past gauged actions. [S3]

This is a legitimate exact identification and fixed-order stability argument on the physical law image. It is not an identity for an arbitrary noisy density tuple, a proof that two offsets are minimal, or a calibration procedure for unknown marks. The new introduction does not make those stronger claims. [S1, S3]

### R70-M3. Global quadratic identification and the signed higher blocks do not assume the answer

**Locations:** Theorem 3.4, pp. 17–18; Theorem 4.2, pp. 23–25; S3–S4.

With supplied polygonal coefficients $k_i$ and unknown positive curvatures $c_i$, the future action Hessians satisfy

$$s_i=k_i+c_i-\frac{k_i^2}{k_i+c_{i+1}+s_{i+1}}.$$

For prescribed positive $s$, the projected map

$$\Phi_s(z)_i=\left[s_i-k_i+\frac{k_i^2}{k_i+s_{i+1}+z_{i+1}}\right]_+$$

is a contraction on the nonnegative orthant, with constant bounded by $\max_i[k_i/(k_i+s_{i+1})]^2<1$. Its fixed point belongs to the positive-curvature image exactly when all components are positive. The map is therefore not being inverted by selecting an unexplained local branch. Nor is every positive action-Hessian vector claimed realizable. The printed excluded example $s=(1/10,10)$, $k=(1,1)$ correctly gives a zero component of the projected fixed point. [S4]

At degree $n$, the signed shift satisfies $T_n^r=\Lambda^n I$, and the response block is $(I+T_n)(I-T_n)^{-1}$. The individual one-step contractions have magnitude less than one; odd-order signs are not discarded. In particular,

$$\det\bigl((I+T_n)(I-T_n)^{-1}\bigr)
=\frac{1-(-1)^r\Lambda^n}{1-\Lambda^n}.$$

The actual stationary envelope proves finite-jet factorization before this block is used. Thus the lower-order remainders belong to actual smooth graph jets, rather than to unrelated formal series. Global quadratic identification followed by finitely many signed inversions gives each fixed finite-order inverse. It does not by itself provide the complete analytic norm inverse or equality of smooth germs. [S3, S4]

### R70-M4. The functional last step really removes flat ambiguity

**Locations:** Lemma 5.1, Proposition 5.2, Theorem 5.3, pp. 28–30; S5.

The proof needs more than a bound $C\rho^j|u|$ with an uncontrolled prefactor. Actual half-line uniqueness identifies later visits with compositions of one-step maps. On a common collar for the segment between the two graph tuples, their derivatives are uniformly bounded by $a<1$. Consequently,

$$|x_{b,j}^t(u)|\le a^j|u|$$

has multiplicative constant one. The initial envelope coefficient has a positive floor, while the later visit weights have uniform upper bounds. Integrating the actual envelope along the graph segment produces

$$\mathcal S(G)-\mathcal S(F)=\overline\alpha(G-F)+K(G-F),
\quad \overline\alpha\ge\tfrac12.$$

In the real weighted norm $\|h\|_{m,R}=\max_b\sup_{0<|u|\le R}|h_b(u)|/|u|^m$,

$$\|\overline\alpha^{-1}K\|_{m,R}
\le\frac{6a^m}{1-a^m}<1$$

for a sufficiently large finite $m$. Equality of action functions, together with the requisite finite-jet agreement, then forces equality of the actual graph functions on a common collar. The collar and operator may depend on the candidate pair. This is sufficient for uniqueness; the paper does not turn that pair-dependent operator into a directly observable computational inverse. [S5]

The stationary envelope used here retains the terminal variation in the finite problem and proves its decay before taking the half-line limit. The later-visit series is summable for the anchored variations under consideration. These details are substantive; a formal all-orders computation would not replace them. I find no flatness-to-identity fallacy in this chain. [S3, S5]

### R70-M5. The stability argument and the actual flat family have the advertised, limited scope

**Locations:** Lemma 5.4, Theorem 5.5, Proposition 5.6, pp. 30–33; S5.

For a bounded positive $C^{m+3}$ class, the polynomial alignment corrects the finitely many lower jets before applying the weighted inverse. The forward action comparison for this polynomial perturbation is obtained from the summable actual envelope. Taylor's remainder then converts the aligned $C^m$ action discrepancy into the weighted norm. This yields a $C^0$ estimate for the complete profile from a $C^m$ discrepancy between **realizable** laws. It is not a $C^0$-law inverse, an unweighted all-jet estimate, or a uniform assertion at zero curvature, grazing incidence, or a vanishing contraction margin. [S5]

The flat construction changes one contact by $\varepsilon\chi(u)e^{-1/u^2}$ and uses a remote normal bump, with nonzero area derivative, to preserve free area. Convexity, clearance, and the marked orbit persist for a small family. Contact jets and action jets agree, while the positive actual envelope gives a nonzero action difference, asymptotic to $\varepsilon e^{-1/u^2}$ at that contact. The remote area correction contributes nothing to the local action. This is an actual-table construction, not merely a list of formal coefficients. [S5]

The conclusion concerns full laws versus contact/action Taylor records. It does **not** construct equal full marked length spectra, and it does not assert that the normalized density jets coincide. The normalization constants could change. Revision 70 explicitly preserves these distinctions; they must also govern the significance argument in Section 4 below. [S1, S5]

### R70-M6. The finite-preparation bridge does not smuggle in an exact-law oracle

**Locations:** Theorem 1.2, p. 5; Lemma 6.1 and Theorems 6.2–6.3, pp. 34–37; S6.

The forward bounds precede conditioning. A positive residual integral and the relative numerator estimates give $\|f_N-f\|_{C^m}\le C_0e^{-\omega N}$, uniform finite higher derivative bounds, and success probability at least $c_0e^{-\Gamma N}$. The upper bound on free area is in the correct direction for the success lower bound. Densities are normalized on the larger gate $Q_+$ and restricted to the interior $Q$, not renormalized there. [S6]

In dimension two, the derivative-kernel summand has envelope $Ch^{-m-2}$ and variance $CHh^{-2m-2}$. The stated stochastic terms

$$\sqrt{\frac{L_n}{nh^{2m+2}}},\qquad\frac{L_n}{nh^{m+2}}$$

therefore have the correct dimensional and derivative factors. Interior support permits the integration by parts without postulating a smooth zero extension across the gate boundary. The finite grid and its Lipschitz interpolation yield the displayed uniform bound. Bounded coordinate recording errors enter pathwise as $C\delta h^{-m-3}$; no independence of those errors is needed after exact acceptance. Misclassified gate labels, offset errors, or a single unreset trajectory are different models and are not covered. [S6]

The measurable first-near-minimizer over a countable dense subset of the actual law image is important. Separability supplies the subset; a countable infimum and derivative evaluations on a fixed dense spatial set make the selector measurable. No compactness of the image, attained distance minimum, or efficient enumeration is assumed. The triangle inequality compares the selected table's limiting law to the true limiting law, and **only then** invokes the realizable geometric stability theorem. The kernel estimate and the finite-flight density are not asserted to satisfy the limiting factorization. [S6]

For $\alpha=s/[2(m+s)+2]$ and $\gamma=s/(m+s+3)$, the bandwidth balances bias with variance and bounded readout error, giving the accepted-sample radius $C\{e^{-\omega N}+(L_n/n)^\alpha+\delta^\gamma\}$. An independent preparation is exactly a mixture of a failure atom and a successful conditional mark. Its Bernoulli stream can be separated from the mark stream; the first successful marks retain their product law even under the sufficient-success event. The fixed-budget union bound costs a second $\zeta$. [S6]

Rounding $N$ down to a returning multiple of $P$ changes only a fixed constant. The resulting exponent is

$$\beta=\frac{\alpha\omega}{\omega+\alpha\Gamma}<\alpha.$$

Thus unsuccessful preparations are not treated as free. All $JB$ preparations are charged, with time bounded by $CJB(1+N_B)$. The displayed small-error, bandwidth, and sufficient-success requirements must remain, especially when confidence varies. The result is a sufficient uniform upper bound on a stipulated class, not minimax optimality or efficient reconstruction. No new error is established in this passage. [S1, S6]

### R70-M7. The earlier stopping-error repair remains intact

**Location:** Proposition 4.4, pp. 26–27; S4, lines 293–433.

The finite-iteration curvature error still passes through the higher-jet recursion with its sensitivity multiplier:

$$\|\widehat q_{\le M}^{(j)}-q_{\le M}\|\le C_M(\tau^N+\varepsilon)+L_M E_j.$$

The off-fixed-point extension is specified algebraically; it is not mislabeled a physical stationary tuple. The resolvent derivative estimate does not assume a matrix variation commutes with the cyclic shift, and the lower-order remainder sensitivity is propagated inductively. The earlier coefficient-one amplification error has not returned. This fixed-order reconstruction remains separate from the finite preparation budget. [S4]

## 4. Major concerns about originality and significance

### R70-E1 — Major: the relevant smooth scattering/lens comparison is missing

**Locations:** Introduction Section 1.4, principal p. 6; `LITERATURE_CHECK_V70.md`; active bibliography inputs. [S1, S7]

The new comparison concentrates on marked-length rigidity. That comparison is useful and, within the checked statements, carefully qualified. It is not sufficient for a paper whose measured endpoint laws are explicitly converted into real action functions.

A directly relevant primary source is L. Noakes and L. Stoyanov, *Lens Rigidity in Scattering by Unions of Strictly Convex Bodies in R²*, arXiv:1803.02542v2. Its Theorem 1.1, printed p. 3, identifies finite disjoint unions of strictly convex planar domains with $C^3$ boundaries from almost-everywhere equality of travelling times, or of scattering length spectra. The paper supplies a separate planar proof correcting the coverage of an earlier argument. That corrected source, not only the earlier higher-dimensional statement, should be used. [L1]

Independent search of every frozen TeX/bibliography file finds no occurrence of either author's name, the relevant identifiers, or the associated lens/travelling-time terminology. This is a checkable omission, not a generic demand for more citations. [D1]

**This does not prove that Noakes–Stoyanov subsumes A2.** Their global exterior-ray data and geometry are different from A2's local near-periodic conditional endpoint laws with supplied internal polygonal marks. No data reduction in either direction has been established here. The relevance is that smooth obstacle recovery from sufficiently rich scattering data is not, by itself, a new category of rigidity phenomenon. [L1; comparison inference]

The author should add a theorem-level comparison of geometry, regularity, supplied calibration, observed data, spatial coverage, and conclusion, and explain what the relative-law/local-contact mechanism accomplishes that is not merely a reformulation of an available scattering inverse. A reasoned distinction may suffice; a dominance theorem is required only if dominance is claimed. This request does not require changing the theorem's assumptions or claiming equality of the two data models.

### R70-E2 — Major: the combined mechanism is credible, but its exceptional significance is not yet persuasive

**Locations:** Introduction Sections 1.2–1.4; cover letter; S1, S7.

The strongest defensible thesis is the combination of a nonlinear **relative physical limit** with an **actual smooth-contact inverse**, and a finite charged observation that reaches the required topology. The geometric argument is not reducible to the displayed transfer-matrix algebra alone. In particular, the determinant comparison and actual envelope must survive the nonlinear geometry. Those are real contributions deserving serious assessment. [S2–S6]

Nevertheless, the present general-journal case remains largely a statement that these two obstacles have been overcome in this specially marked model. The final weighted contraction is structurally a Neumann-series argument once the actual visits and coefficients have been supplied. The statistical implementation uses a proved but classical derivative-kernel estimate, separable minimum-distance selection, and a binomial budget balance. The manuscript now acknowledges this; the revision should receive credit for that honesty, but these components cannot be counted again as independent methodological breakthroughs. [S1, S5, S6]

The flat family gives a genuine same-model distinction from the formal Taylor record. Once the actual smooth inverse is available, however, a small flat perturbation is naturally separated; the construction does not also establish that A2 separates tables indistinguishable by a standard full billiard invariant. The extra area constraint makes the example physical, but does not change that comparison boundary. This is a reason to calibrate the significance argument, not to delete the example or to require a new equal-spectrum counterexample. [S5, S6]

The revision's marked-length comparisons correctly avoid claiming that arbitrary-period endpoint-law rigidity removes the assumptions of the analytic marked-spectrum theorem, or that a limitation of one set of spectral relations is an impossibility theorem for the full spectrum. The statements of Bálint–De Simoi–Kaloshin–Leguil, De Simoi–Kaloshin–Leguil, and the enriched-spectrum work of Finamore–Leguil concern genuinely different observations. Their presence does not by itself establish the comparative difficulty or reach of the present problem. [L2–L4]

My adverse placement judgment rests on that uncompleted case for an exceptional advance, not on an assertion that every constituent is known or that a paper about a fixed periodic polygon is automatically unsuitable for a leading journal. A corrected literature comparison and a sharper account of the mathematical gain are necessary for reassessment; neither guarantees acceptance. Producing more revision labels, diagnostics, or restated introductory theorems would not address this issue.

### R70-E3 — Scope that must remain explicit, not a new correctness defect

The full smooth profile is recovered on a class-dependent contact collar near the supplied polygon. This is not arbitrary smooth whole-obstacle determination from unlabeled passive observations. The finite experiment requires exact itinerary/gate/offset information, independent resets, fixed geometric margins, and sufficiently high but finite smoothness bounds. Whole-obstacle continuation is reserved for the separately stated analytic setting. The new front matter preserves these distinctions, so I do not request that the main theorem be weakened. [S1, S4–S6]

At a fixed nonzero $u_*$ the flat family is statistically distinguishable once the displayed error radius is below a constant times $\Delta=\varepsilon e^{-1/u_*^2}$. With zero readout error, the sufficient budget condition obtained from that bound can grow exponentially in $1/u_*^2$; the constants and logarithms still matter. This is an implication of the **sufficient upper bound**, not a necessary sample-complexity lower bound. It cannot be advertised as uniform inexpensive detection at a vanishing spatial scale. The source currently does not advertise it that way. [S5, S6]

### R70-P1 — Minor: the repository landing page still points to revision 68

At the pinned referee-ready head, the root `README.md` describes A2 revision 68 and points to `A2_REVISION_V68_INDEX.md`, whereas the current entry is `A2_REVISION_V70_REVIEW_READY.md`. The manuscript-directory README is updated, but the repository landing route is stale. Update that route in the next delivery. This is a navigation defect, not grounds for mathematical rejection. [R2]

## 5. Independent reproduction and its limits

The native v70 and baseline v69 workflow artifacts were downloaded through the connected GitHub service. Independent code, importing no author modules, checked archive inventories, byte lengths, SHA-256 hashes, Git blob hashes, and the **raw Unix modes**. Reconstruction gives the two expected Git manuscript trees. All **911** current source files and all **47** hash-listed native evidence files verify. Previous-path retention and the continued activation of the prior source inputs verify as described in Section 2. The four recorded author normal/optimized diagnostic pairs agree; those author programs were **not rerun**. [D1]

All three entries were independently rebuilt from a clean extracted source, with `latexmk -norc` and `pdflatex -no-shell-escape`, in dependency order `two_collision`, `main`, `rigidity`. The final logs contain no detected undefined references, multiply defined labels, missing characters, LaTeX errors, or overfull notices; they retain five underfull notices in the full manuscript and one in the principal article. These underfull notices are not proof errors. [D2]

Every one of the **517 pages** has identical extracted text and identical RGB rendering at 72 dpi between the native and independently rebuilt PDFs under the same PyMuPDF renderer. The PDF byte hashes themselves differ, so byte-for-byte PDF identity is **not** claimed. Automated render equality does not establish that every page was visually or mathematically examined. [D2]

Actual visual inspection covered contact sheets for principal pp. **3–6, 28–29, 31–32, and 34–37**, with p. **36** additionally inspected at **108 dpi**. No clipping or unreadable displayed formula was observed in that sample. No all-page visual judgment is inferred from it.

The independent exact-rational program checks **36** cofactor/transfer/Cayley–Hamilton cases, **56** signed cyclic matrix cases, **36** two-offset cases, **144** rate cases, two finite binomial normalizations, eight conditional-first-success-mark identities, and four weighted thresholds. It detects 36 deliberately unanchored-normalizer controls and 288 wrong-dimension/omitted-rarity controls. Normal and optimized Python outputs agree. These finite checks corroborate algebraic bookkeeping; they do not prove concentration, trace-class limits, realizability, smooth inversion, optimality, or originality. [D3]

## 6. Required response and final disposition

**R70-D1 — Mathematical status.** No new mandatory core repair or fatal counterexample is established in the stated examination. Preserve the actual relative normalization, physical gauge, signed blocks, constant-one visit contraction, polynomial alignment, realizable selection, and charged-budget qualifications. Do not present this scoped finding as certification of all retained results.

**R70-D2 — Concrete major response.** Address R70-E1 by engaging the corrected planar lens/scattering theorem at the level of data and hypotheses. A response merely saying that the title uses “boundary laws” rather than “lens data” would not answer the mathematical comparison. Equally, conceding without proof that the results are equivalent would be unwarranted.

**R70-D3 — Placement response.** Address R70-E2 with an evidence-based account of the specific advance, not stronger adjectives or a larger theorem count. The relative-law/smooth-envelope combination is the appropriate subject of that account. An efficient estimator, an optimal rate, or a same-spectrum counterexample could be separate research achievements, but none is invented here as a mandatory correctness repair.

**R70-D4 — Closed points and delivery.** Credit the corrected architecture, the retained finite-preparation advance, source preservation, raw-mode integrity, and independent builds. Fix the minor root-index route. Do not reopen already answered objections to exact-law access or to smooth identity solely from jets.

**R70-D5 — Recommendation.** Do not accept at the requested top-four level on the present exceptional-significance case. The report does not direct the author to abandon the program, reduce the theorem's scope, or remove valid technical material. Further assessment must engage the actual claimed result and the relevant prior art, rather than perpetuating an arbitrary repair cycle.

Only review files are added by this review. No manuscript, prior review, native delivery, default-branch ref, branch protection, repository permission, or existing branch is modified or deleted.

## Sources and reproducibility keys

All S-keys refer to compiled source `16ec1030b9dfd9b185a1f0da8e50b10b40a71940`, under `papers/A2-v17-boundary-information-coarsening/`. Page numbers refer to that source's native principal `rigidity.pdf`.

- **S1:** `article/00i_main_thesis_v70.tex`, lines 1–386, and `article/00j_abstract_v70.tex`; principal pp. 1–7. Main theorem lines 65–118; charged-budget theorem beginning line 238.
- **S2:** `article/10a_periodic_itinerary_relative_v64.tex`, lines 1–549; principal Section 2, pp. 7–13. Relative theorem starts line 162; physical theorem line 424.
- **S3:** `article/10b_periodic_contact_inverse_v65.tex`, lines 1–347; principal pp. 14–18. The later analytic function-space inverse is outside this fresh line-by-line examination.
- **S4:** `article/10c_global_curvature_inverse_v66.tex`, lines 1–433; principal pp. 22–27.
- **S5:** `article/10d_smooth_contact_rigidity_v68.tex`, lines 1–445; principal pp. 27–33.
- **S6:** `article/10e_sampled_smooth_recovery_v69.tex`, lines 1–358; principal pp. 33–37.
- **S7:** `main.tex`, `rigidity.tex`, `RESPONSE_TO_REFEREE_V70.md`, `COVER_LETTER_V70.md`, `HISTORICAL_DERIVATION_AUDIT_V70.md`, `journal/DEPENDENCY_LEDGER_V70.md`, and `LITERATURE_CHECK_V70.md`.
- **R1:** `reviews/a2-v69-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md` at `ba42d7a3a7873739c596497c5b2b884452f130d1`.
- **R2:** `A2_REVISION_V70_REVIEW_READY.md` and root `README.md` at `b529b340650f5582b1d04fabd599533450b51d0b`; GitHub compiled-source-to-submission comparison and source `papers` directory metadata.
- **D1:** `AUDIT_EVIDENCE.json`, delivery/retention section; `verify_delivery.py` in this review directory.
- **D2:** `AUDIT_EVIDENCE.json`, independent-build section; `compare_builds.py`; reproduction instructions in this review directory's `README.md`. Detailed local logs and inspected images accompany the local audit archive.
- **D3:** `independent_checks.py` and its exact emitted results in `AUDIT_EVIDENCE.json`.
- **L1:** L. Noakes and L. Stoyanov, *Lens Rigidity in Scattering by Unions of Strictly Convex Bodies in R²*, arXiv `1803.02542v2`, Theorem 1.1, printed p. 3; primary abstract/version record and PDF inspected September 16, 2026: https://arxiv.org/abs/1803.02542v2 and https://arxiv.org/pdf/1803.02542 .
- **L2:** P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, arXiv `1809.08947`; DOI `10.1007/s00220-019-03448-x`; Theorem D, Corollary E and Remark 2.3, printed p. 9: https://arxiv.org/abs/1809.08947 .
- **L3:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv `1905.00890v4`; related DOI `10.1007/s00222-023-01191-8`: https://arxiv.org/abs/1905.00890v4 .
- **L4:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv `2510.18983`; current primary record retrieved September 16, 2026: https://arxiv.org/abs/2510.18983 .
