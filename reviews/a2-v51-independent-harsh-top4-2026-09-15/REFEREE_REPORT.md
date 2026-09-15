# Independent referee-style report on A2, revision 51

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*, Qian Qi.  
**Assessment date:** September 15, 2026.  
**Requested standard:** the leading general mathematics journals.  
**Recommendation:** **Do not accept at the requested standard on the contribution and article-level case demonstrated.** This is not a finding that a principal theorem has been disproved. No newly established fatal theorem error was found in the technical coverage specified below.

This is an author-requested, AI-assisted referee-style assessment, not a commissioned report, endorsement, or decision of a journal. The frozen manuscript, rather than its revision number, build status, or earlier favorable checks, is the object of the assessment. Source identifiers [S01]–[S12], primary references [L1]–[L5], and reproduction evidence [D1] are specified in the accompanying [audit](AUDIT_AND_REPRODUCTION.md).

## 1. Submission identity, changes, and review coverage

The reviewed delivery is `revision/a2-v51-review-ready-2026-09-15`, frozen at **`ffd53f26383874dc798af9a54ae877ffdd0f81eb`**. The actual compiled mathematical source is **`b9201bc272bc7ecbab1ad6a91fc844216685fadd`**, under `papers/A2-v17-boundary-information-coarsening`. Its historical directory name does not mean that revision 17 was reviewed. The complete principal article has **269 pages**; the complete two-collision companion has **7 pages**. The workflow preparation commit is different from the compiled source commit. [D1]

The preceding v50 report is frozen at `4b22b793cc2c05d3f48efb9a98dfd46cab003e5c`. I read that report and the v51 response, but do not treat their conclusions as binding. Revision 51 adds Theorem B and Section 14: unknown numerical transverse origins and arbitrary positive, separate endpoint recording factors are allowed. Theorem A and the previous proof corpus remain. The preservation diagnostic, rerun here, finds all 522 inherited theorem-style/proof blocks, including 245 proof environments, retained verbatim. Independent byte checks also verify the old active sources or their archived originals. Preservation establishes provenance, not validity. [S11, D1]

Fresh technical coverage includes all new statements and proofs in Section 14 and their introductory formulation; the relative boundary-law construction; the actual-smooth signed jet inverse; the scalar-anchor density inverse; analytic continuation; finite congruence enumeration; and the differential registration and lattice interfaces. I additionally inspected the stated observation and hard-category calibration interfaces. I have **not** independently re-proved every local statistical experiment, minimax assertion, global estimator, auxiliary appendix theorem, or theorem of the companion. All-page source/build comparison is not all-page mathematical certification.

**Principal assessment.** The new extraction is valid in its stated local smooth and exact-law settings, as far as the checks below establish. It is a genuine enlargement of the allowed recording model. However, one must distinguish that enlargement from a new difficult inverse mechanism: separate endpoint factors already cancel in the earlier four-density identity, and, under the complete-cap hypothesis actually imposed, the missing numerical origins are already identifiable from the support alone. I give the latter argument below. Neither observation refutes the new theorem; both matter to its significance.

## 2. The new mathematical assertions

### R51-C1. The interaction formula and the zero-fiber characterization survive inspection

**Location:** Lemma 14.1, page 56; [S02], lines 13–101.

The recorded density is

$$\widetilde f(x,y)=\frac{A(x)C(y)}{Z}\,[d-S(x-\xi)-S(y-\eta)]_+,$$

with known positive $d$, strictly positive smooth $A,C$, and $S(0)=S'(0)=0$, $S''>0$. The complete positive cap is retained and is compactly contained in the coordinate box. On its interior, putting $u=x-\xi$, $v=y-\eta$ and $H=d-S(u)-S(v)$ gives

$$\mathcal K_{\widetilde f}=\partial_x\partial_y\log\widetilde f=-\frac{S'(u)S'(v)}{H^2}.$$

The separate factors and the normalizing constant disappear. Strict convexity makes zero the unique root of $S'$. Every nonempty vertical fiber has positive length, and therefore contains a point different from $\eta$. Consequently its interaction vanishes identically precisely when $x=\xi$. The horizontal assertion follows in the same way. At a noncentral slice point the relevant root is simple:

$$\partial_x\mathcal K(\xi,y_*)=-\frac{S''(0)S'(y_*-\eta)}{[d-S(y_*-\eta)]^2}\ne0.$$

These are interior calculations; no derivative across a moving support boundary is being taken. The existence of a continuous interior representative also resolves the otherwise legitimate concern about evaluating a density known only almost everywhere. The proof does not assume that the two effective recording profiles agree.

**Finding:** no error identified in this lemma. Its assumptions concerning strict positivity, the visible cap, known signed units, and known coordinate directions are essential to what is actually asserted.

### R51-C2. The complete support already identifies both numerical origins

**Location:** the observation model in (14.1)–(14.2), pages 55–56. This is an independent comparison derived from those hypotheses, not an assertion borrowed from the preceding report.

For $0<q\le d$, let $v_-(q)<0<v_+(q)$ be the two solutions of $S(v)=q$, and define

$$W(q)=v_+(q)-v_-(q).$$

They exist inside the specified interval. Strict convexity and the compact-sublevel hypothesis give

$$W'(q)=\frac{1}{S'(v_+(q))}-\frac{1}{S'(v_-(q))}>0.$$

The length of the vertical fiber of the observed positive set is therefore

$$w(x)=W\bigl(d-S(x-\xi)\bigr).$$

Because $S$ has its unique minimum at zero and $W$ is strictly increasing, **$w$ has its unique maximum at $x=\xi$**. Interchanging the coordinates shows that the horizontal fiber length has its unique maximum at $y=\eta$. Thus both origins are determined by the complete support, without knowing $S$, differentiating a density, or knowing either recording factor. There is no evenness assumption. In fact the maximum is nondegenerate:

$$w''(\xi)=-W'(d)S''(0)<0.$$

The compact-sublevel margin justifies the inverse-branch derivatives at $q=d$.

This observation has two limits which must be stated as carefully as its conclusion. First, it does **not** recover the whole action from one support. The support-preserving action modification already discussed in [S09] remains a relevant distinction. Second, the argument uses the cap boundary. It does **not** replace Proposition 14.3, whose perturbation norm is on a fixed interior rectangle and does not control that boundary. The mixed-derivative construction is useful precisely because it provides an interior local differentiable extraction.

**Finding:** this is a contribution benchmark, not a counterexample or a request for another appended theorem. The removal of unknown numerical origins should not be presented, by itself, as overcoming an otherwise unidentified geometric ambiguity in the complete-support experiment. A short acknowledgment of this comparison would make the significance discussion more exact while retaining the stronger interior-regularity argument.

### R51-C3. The action invariant is correct, but its weight cancellation is inherited algebra

**Location:** Theorem 14.2, page 57; [S02], lines 103–171; compare Theorem 13.1, page 49, [S05].

After recentering, define

$$R(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)},\qquad t(u)=\frac{S(u)}{d-S(u)}.$$

For two entirely different positive factors at the two endpoints,

$$1-R(u,v)=t(u)t(v).$$

A nonzero anchor $a$ on the small positive square gives $q=\sqrt{1-R(a,a)}=t(a)>0$, and hence

$$T(u)=\frac{1-R(u,a)}q,\qquad S(u)=\frac{dT(u)}{1+T(u)}.$$

This recovers negative and positive coordinates separately, including odd action coefficients. There is no pointwise square root at the degenerate minimum. The effective axis-factor ratios in (14.8) follow by substitution. Equal centered action germs give locally separate density ratios, and a separate density ratio leaves $R$ invariant; this proves the stated complete local invariant assertion at fixed $d$.

The proof is sound. But the separate-factor cancellation is already available from exactly the four-density calculation used in v50; equality of the two factors is not needed for that calculation. Revision 51 makes the larger nuisance interpretation explicit and couples it to unknown origins. This is worth recording, but it is not a second independent high-order inverse mechanism. Moreover, identifying the product of a physical amplitude with a recording efficiency does not separate those two factors. The source correctly says so.

The referee-designed controls exercise a non-even strictly convex action, unequal positive factors, the axis-factor identities, and the scalar anchor. They also check the anchor derivative rather than merely the undifferentiated formula. These finite identities support the algebraic assessment; they do not establish physical realization of the test action. [D1]

### R51-C4. The finite-loss differentiability statement is appropriately local

**Location:** Proposition 14.3, pages 57–58; [S02], lines 173–267.

The proof does not differentiate the set-valued operation of selecting a zero fiber. It first fixes two noncentral slices in a compact positive rectangle $Q$. The map

$$f\longmapsto f_{xy}/f-f_xf_y/f^2$$

is continuously differentiable from the positive part of $C^{m+3}(Q)$ into $C^{m+1}(Q)$. The simple-root margins allow two ordinary scalar implicit-function arguments. Their roots agree with the actual origins for model laws on the specified local branch. For arbitrary nearby nonmodel functions there is only a local root selection, which is all that is needed.

Translation by the extracted origins is then differentiated with surplus derivatives. Its variation includes the translated perturbation and both transport terms involving $f_xD\Xi$ and $f_yD\Upsilon$. Positive axis denominators, a nonzero scalar anchor, and $1+T$ bounded away from zero allow composition with the ratio inverse. A locally bounded derivative on a small convex ball gives the displayed Lipschitz estimate. This establishes the announced $C^{m+3}$-to-$C^m$ conclusion; it does not establish optimal derivative loss.

The origin variation formulas

$$\dot\xi=-\frac{\dot{\mathcal K}(\xi,y_*)}{\mathcal K_x(\xi,y_*)},\qquad \dot\eta=-\frac{\dot{\mathcal K}(x_*,\eta)}{\mathcal K_y(x_*,\eta)}$$

have the correct signs and account for translating origins. Once both are stationary, differentiating the centered ratio also requires differentiating its scalar anchor. The independent control detects a nonzero error if that term is deliberately dropped. Subtracting constant and linear terms from a nonmodel extracted action does not alter the recovered coefficients of order at least two.

**Finding:** no finite-loss or origin-transport defect identified. The theorem is neither a total-variation continuity statement nor a uniform result over vanishing density, root, or anchor margins. The source explicitly maintains these restrictions.

### R51-C5. The geometric fiber and derivative-kernel interfaces require both directions, and both are present

**Location:** Theorem 14.4, pages 58–59; [S02], lines 269–356; [S04]–[S08].

From each pair of recorded laws the extraction gives both signed action germs. With the gap, their quadratic coefficients determine the leading geometry. The actual finite-jet factorization then legitimizes the recursion for every fixed higher order. For analytic obstacles the recovered germs determine entire channel-frame images. This gives an inclusion of recorded realizations in the old finite table fiber.

For the reverse inclusion, an accepted old reconstruction branch places each recovered *ordered* channel pair by a proper Euclidean motion. Its local actions and normalized physical amplitudes consequently agree. The global phase-volume constant disappears under conditioning. Reusing the original numerical origins and endpoint recording profiles therefore realizes the complete recorded laws on that branch. This is the necessary reverse argument; mere finite enumeration would not establish equality of fibers. The noncircular finite ambiguity is not removed by the new nuisance invariant.

For derivatives, stationary recorded interior densities give stationary origins and action coefficients at every separately fixed order. The leading inverse and the differentiated recursion retain all terms:

$$\dot q_n=M_n^{-1}\{\dot s_n-\dot R_n-\dot M_nq_n\}.$$

Induction gives zero graph-jet variation. The common-strip analytic-support hypothesis makes the variation itself analytic, so the identity theorem applies. Finite symmetry is handled by the actual continuous congruence branch through the base alignment, not by assuming every base symmetry persists under perturbation. The displacement cochain then makes the gauge-fixed lattice derivative vanish.

The conclusion concerns the **projection of the joint data-derivative kernel onto table variations**. It does not identify every nuisance profile. Conversely, a common Euclidean table motion admits stationary records by holding suitable intrinsic profiles fixed; arbitrary nuisance changes need not preserve a law. Nonlinear injectivity is not substituted for derivative injectivity.

**Finding:** no new failure identified in these interfaces. The assumptions on analytic variations and persistent selected designs are substantive, not optional technical decoration.

## 3. Fresh checks of the inherited core

### R51-C6. Relative normalization is not dispensable

**Location:** Theorem 7.2 and its proof, pages 18–20; [S03], lines 118–250.

The reference twist is exponentially small, $d_j^0=q_p/\sinh(j\gamma)$. An absolute error of size $\vartheta^j$ does not automatically become a decaying relative error after division by this reference. The manuscript normalizes first, using the cofactor identity

$$\log b_j=\sum_{i=0}^{j-1}\log\{g[-\ell_{i\bmod2,uv}(y_i,y_{i+1})]\}-\log\det(I+G_j\Delta H_j).$$

The important point is the localized, subtracted Hessian. Its entries are summable along endpoint tails; the trace-class assertion is not obtained by multiplying an unweighted operator bound by an increasing matrix dimension. The half-line construction gives a convergent trace-series normalization on the chosen collar.

I inspected the gluing and comparison steps. Joining the two half-line segments gives an exponentially small residual with polynomial flight-length losses in an $\ell^1$ estimate. Uniform diagonal dominance controls the correction. At each fixed derivative order the residual equations retain the principal inverse. The determinant comparison uses two retained endpoint blocks and an entrywise summable tail. Remote Green-kernel terms and block coupling are exponentially small. Telescoping trace powers keeps one trace-norm factor with controlled operator-norm factors. Fixed polynomial losses can be absorbed into a slower exponential rate.

The subsequent fixed-positive-offset integration is also essential: it retains nonlinear half-line actions rather than collapsing immediately to their quadratic approximations. The amplitude factorizes, but the positive cap still couples the conditional endpoints. [S03], lines 252–386.

**Finding:** no new relative-normalization gap established in this coverage. This inherited argument is substantially more important than the elementary ratio identities. Finite symbolic controls alone would not verify it.

### R51-C7. The signed recursion concerns actual smooth jets, not merely formal power series

**Location:** Lemma 12.4, page 45, and the determinant-one recursion in Section 12; [S04].

The smooth-remainder step interpolates actual local graph pairs sharing their jets through order $M$. The common quadratic geometry supplies a common weighted half-line reference. The variation of the one-flight length is proportional to the graph difference evaluated along the stationary orbit. Taylor remainders and weighted orbit decay yield a summable estimate of the form

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|\le \frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

The finite stationary-envelope identity retains its terminal term before the infinite limit; that term is controlled and tends to zero. Integrating the finite identity in the interpolation parameter before passing to the limit avoids a formal-to-smooth substitution. Functional smooth bounds, not just finitely many jet values, are needed for these remainder constants.

Only after this filtration is established does the last-jet calculation apply. Boundary occurrences are counted once and interior occurrences twice. The resulting matrix is

$$M_n=\begin{pmatrix}\coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)\end{pmatrix},\qquad r_0r_1=1,$$

with determinant one. This yields a finite-order inverse, not an order-uniform condition estimate. Equality of all smooth jets does not imply equality of arbitrary smooth germs; analyticity is used separately for the global boundary conclusion. The registered analytic-continuation argument and the common-strip derivative argument maintain that distinction. [S06, S08]

The finite global matching also retains the actual invertible integer gain matrix in $L=(v_1\ v_2)M^{-1}$, rather than assuming unimodularity. It tests shape agreement, positive lattice determinant, disjointness and channel clearance before accepting a branch. The local angular lift uses a nonzero harmonic through the actual alignment and permits symmetry breaking. These are the correct mechanisms for reconciling a finite exact fiber with local infinitesimal rigidity. [S07, S08]

**Finding:** the source supports the actual-smooth and finite-branch interfaces examined. Neither this finding nor unchanged source certifies unexamined portions of the article.

## 4. What the new observation does not establish

The manuscript distinguishes four different levels: exact function-valued laws; perturbations in finite interior smooth norms; finitely many exact scalar expectations on a prescribed immersed model; and physically acquired finite histograms on a separately quantified class. This distinction is necessary. Theorem B addresses the first level and Proposition 14.3 the second. The old finite-coordinate theorem remains an ideal-law, finite-dimensional, model-local theorem. It has not been extended to an arbitrary infinite-dimensional recording-nuisance model merely by identifying the geometric component. [S01, S02, S08]

The number $N+1$ counts selected channels, not scalar measurements, independent observations, or bits. Marks, directions, signed units, gaps and known offsets remain supplied in the exact problem. Revision 51 removes the numerical origins, not the whole physical coordinate calibration. Neither an arbitrary nonlinear coordinate map nor a joint endpoint recording factor belongs to the theorem.

There is a particularly simple acquisition distinction. In an iid preparation protocol, replace both recording probabilities by $\varepsilon e_1$ and $\varepsilon e_2$, with $0<\varepsilon<1$. The normalized recorded conditional law is unchanged, while the probability of obtaining a recorded success is multiplied by $\varepsilon^2$. If the original success probability is $p$, the chance of at least one recorded success in $B$ preparations is at most $Bp\varepsilon^2$. Thus no fixed uniform preparation budget for acquiring successful records can follow over the new unconstrained recording class, even from an unchanged conditional density. This is not a counterexample to the paper: Section 14.5 expressly refuses that transfer.

The inspected calibration interface retains precisely the kinds of bounds that would be needed elsewhere. Its category error includes finite-flight error, amplified gap/clock error, and a cell-edge tube term, including outer edges. The stated bias is

$$2C_0\tau^j+2C_{\rm off}(jv_g+v_t)+2H_*V_\delta(r).$$

The pilot fixes the final flight number and estimated projections before fresh successful streams are used. Preparation caps require a separate lower success bound and are added before integrating over pilot histories; they are not obtained by treating successful samples as free trials. The richer planar-position pilot is not replaced by the new origin extraction. My check here concerns this interface, not an independent proof of every upstream pilot or quantized-continuation theorem. [S10]

The independent functional controls also verify that an excluded positive joint recording factor can mask distinct actions on a common cap. This tests the boundary of the theorem's nuisance model; it is not presented as a realized billiard counterexample or a defect in a theorem which explicitly excludes such factors. [D1]

## 5. Literature and disposition of the preceding report

The targeted primary-source check distinguishes two relevant comparisons. Holland–Wang's dependence function and Osius's odds-ratio association framework supply established marginal-factor invariants. Revision 51 cites them and does not claim to invent those invariants. Their existence does not, by itself, reconstruct a billiard or prove a sampling-equivalence result for this experiment. I checked the available bibliographic/abstract records and the manuscript's actual use; I did not undertake a new proof audit of those external papers. [L1, L2]

The billiard comparisons also concern different data. Finamore–Leguil's current arXiv record, v1, states a finite-horizon Sinai-billiard rigidity result using an enriched marked length spectrum. De Simoi–Kaloshin–Leguil's v4 concerns analytic open billiards under non-eclipse and suitable symmetry/genericity hypotheses. Florio–Leguil's v5 explicitly removes an earlier geometric spectral-rigidity assertion affected by an error while retaining dynamical results. The present manuscript does not import that removed assertion. [L3–L5]

No information reduction between those spectra and these conditional endpoint laws has been established in this review, and the priority search is not exhaustive. It would be unjustified to say either that those papers already prove the present signed-law inverse or that the present observation automatically removes their hypotheses.

The concrete v49 requests addressed in v50 remain resolved: the noncircular two-realization example, its extra-gap separator, and the exposition of the relative/smooth analytic obstruction have not disappeared. Their preservation was checked; the complete geometric proofs of the two unchanged examples were not independently repeated in this round. I do not replace the resolved request with another demand for an illustrative example. Likewise, the already corrected moving-reference derivative, actual finite-symmetry branch, hard-category edge control and charged-preparation distinctions are not reopened as though absent. [S11, S12]

Revision 51 genuinely responds to the earlier concern that the observation supplied numerical origins. That portion of the earlier observation critique must be updated. It remains legitimate to ask what the advance is under the *new* complete-cap, known-axis, function-valued observation; R51-C2 gives a concrete answer for the centering step rather than merely repeating the old objection.

## 6. Highest-journal assessment and bounded editorial requests

**R51-E1 — The incremental nuisance result does not change my placement recommendation.** The strongest contribution remains the chain from a relative nonlinear long-bridge law to an actual-smooth signed contact inverse, followed by analytic and finite-cochain globalization. That chain cannot fairly be dismissed as trivial algebra. Conversely, the two changes emphasized in Theorem B have comparatively direct mechanisms under the supplied observation: full-support geometry already locates the numerical origins, and the old scalar-anchor identity already cancels unequal separate factors. The useful new interior differentiability statement is obtained by simple roots and finite-smooth composition once those formulas are available.

An infinite-dimensional nuisance class can be important without its removal constituting an equally large new inverse mechanism. Here I regard the extension as a well-formulated robustness refinement of the central inverse, not as a transformation of the article's conceptual contribution. The exact theorem still starts from highly structured, selected, function-valued records. This is a legitimate mathematical problem, but its difficulty and return must be evaluated under those data, not under the more restrictive spectral observations of other rigidity problems. On that basis, the case for the exceptional general-journal placement requested remains unpersuasive to me.

**R51-E2 — The relation among the article's parts is clearer than their necessity as one major contribution.** The 269-page article combines exact rigidity, several distinct local experiments, finite-resolution continuation, and physical calibration. The new statement that interaction carries geometry while amplitudes and auxiliary records affect acquisition is a useful organizing principle. It is not itself a theorem transferring all later statistical conclusions to the new nuisance observation. The author correctly avoids that claim, but the consequence for the article-level assessment is that the separate results cannot simply be added up as though they solved one common calibrated-to-uncalibrated experiment.

This is not a universal page-limit objection or a request to delete valid arguments. Nor is an unspecified stronger theorem being imposed as a moving target. The bounded editorial requests are to acknowledge the support-only centering benchmark, keep the precise local-regularity benefit of the interaction extraction prominent, and explain why the inherited relative/smooth mechanism and the distinct statistical parts together require this particular general-journal treatment. These requests concern the interpretation and synthesis of what is proved. Satisfying them would not mechanically guarantee acceptance.

The significance judgment is explicitly a referee judgment. An editor or another specialist may evaluate the contribution differently. A negative placement recommendation must not be converted into a claim of a mathematical impossibility or a reason to weaken a valid theorem.

## 7. Reproduction and final disposition

The authorized native artifact was downloaded and its digest checked against the GitHub workflow record. All **582 source files** were verified by size, SHA-256 and Git blob identity. Reconstructing the directory objects gives manuscript subtree **`91989fa41b2714d28a8f93738c992f0c7d89ad2e`**, independently linked to the frozen source commit through the repository's Git trees. All **109 active records** and 34 native evidence files match their manifests. [D1]

Both complete entries were independently rebuilt with shell escape disabled, companion first. All **276 rebuilt pages** agree with the native products in extracted text and in 72-dpi RGB pixel arrays under the same PyMuPDF renderer. PDF byte identity is not claimed. Direct visual inspection was limited to the pages listed in the audit. The main final log contains three underfull boxes; the warning scan found no overfull box or unresolved reference/citation. Build success is not a mathematical certificate.

The author's preservation/control suite and the separate referee-designed script both pass under ordinary Python and `python -O`, with identical output within each pair. The author-suite output also matches the native retained output. The independent script imports no author code and includes negative controls for freezing moving origins, omitting the scalar-anchor derivative, and confusing joint with separate recording factors. Their scope is finite functional/matrix identities, not infinite-dimensional certification. [D1]

**Final disposition:** the new Section 14 arguments survive the stated technical checks; the complete source-matched delivery is independently reproduced; and no newly established fatal theorem error is reported in this coverage. Nevertheless, **I do not recommend acceptance at the requested highest-level general mathematics journal standard**, for the contribution and synthesis reasons above. The support-only centering comparison is the principal new critical observation of this review. No manuscript source, earlier report, unrelated workstream, or repository permission is changed by this assessment.
