# Independent referee-style report on A2 v28

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Revision branch:** `revision/a2-v28-common-orientation-quotient-top4-2026-09-12`  
**Reviewed commit:** `f5fcd5e319cb4a37bdcbf8d9f9d190786ec7fc7d`  
**Reviewed tree:** `a532ddec6150d12e3b3c05dc357a2699295b29ae`  
**Mathematical-source commit:** `6d8f158c60f3636c572daa64779f57c9c9ec757b`  
**Preceding review tip:** `e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v28-external-harsh-top4-2026-09-12`  
**Date:** September 12, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the standards sought for Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned journal report, an editorial decision, or a representation of affiliation with those journals. The object of this report is the pinned A2 revision, not A1 or the whole theta-theory programme. The accompanying [source audit](SOURCE_AUDIT.md) distinguishes complete readings, sampled dependencies, independent calculations, and unperformed verification.

## Recommendation

**Further revision and submission validation are required before an acceptance recommendation. The exact common-orientation classification resolves the preceding C1. The complete-native submission requirement C2 remains open. No fatal counterexample to the core signed inverse or the exact orientation-quotient theorem has been established in this review.**

There is one additional, bounded technical qualification: equivariance of the exact inverse must not be silently extended to the fixed-anchor formula on arbitrary perturbed densities. Section 3 supplies an explicit positive-density counterexample to that stronger extension and an exact anchor-transport remedy. This is not a counterexample to the exact-law classification, and it does not justify reopening C1 as a major mathematical failure. The conditional stability argument is correct for an equivariant inverse on its stated domain; the point is to identify that domain and any off-model extension unambiguously.

The appropriate mathematical disposition is therefore **a resolved exact-classification clarification, a narrowly scoped stability-domain clarification, and an outstanding assembled-submission validation requirement**, not a demand to rebuild the theory or add another unrelated flagship theorem. On the material independently inspected, I do not have grounds for a new major-reconstruction verdict. Equally, the absence of such grounds is not an acceptance certificate for the entire assembled paper or evidence that its exceptional-significance threshold has been met.

## 1. Revision identity and response to the preceding report

The branch search identified A2 v28 as the latest named A2 revision available during this audit. The reviewed head is three commits ahead of the preceding review tip, with no divergence. The two commits after the mathematical-source commit change navigation, diagnostics, and verification records, not the mathematical TeX sources. These facts were checked using repository comparisons, rather than inferred from the version number alone. [S1–S3]

The active change consists of a revised observation-hierarchy section, a replacement of the ambiguous orientation sentence in the intrinsic-gluing section, and a new common-orientation subsection. The native main entry retains the broader three-part article and its auxiliary compendium. The comparison lists no deleted files. Preservation is welcome, but preservation of a dependency is not independent verification of that dependency.

| Prior item | v28 finding | Disposition |
|---|---|---|
| C1: a common orientation quotient versus pointwise sign erasure | The active definition specifies a diagonal action, transports the marked lattice orientation, and proves equivariant gluing and both directions of classification | Closed for the exact datum actually defined |
| C2: complete native main/companion build and reference verification | Two live workflow jobs failed before any step executed; the author expressly leaves C2 open | Open |
| Observed-type error repaired in v27 | The matched-record dichotomy and its measure-theoretic proof remain active and were re-examined | No reopened objection |
| Arbitrary smooth remainders repaired in v27 | Functional interpolation, finite truncation, and the summable action remainder remain active and were re-examined | No reopened objection |
| Fixed-order stability under reflection | Correct for the equivariant exact inverse; a fixed-anchor off-model formula needs an explicit convention | Bounded clarification T1 in Section 3 |

I read the complete new orientation subsection, the revised observation hierarchy, the intrinsic classification section including its ending, the single-offset inverse, and the full signed finite-jet argument. I also examined the rank-two lattice section, the main observed-type proof, and selected introduction and scalar-compatibility material. This does not constitute an independent line-by-line recertification of all forward estimates, all local asymptotic experiments, every global-estimator proof, the companion, or the complete auxiliary compendium. [S4–S12]

## 2. C1 is mathematically resolved for the exact marked datum

### 2.1 The orientation character is necessary bookkeeping, not an inferred angle

The inherited gluing problem places channel frames by proper Euclidean motions and realizes the marked lattice in an orientation-preserving sector. Reflecting the table cannot act within that sector. The new definition correctly enlarges the realization space to the two sectors and writes

\[
\mathscr R(\epsilon,\mathscr D)
  =(-\epsilon,\mathscr R_0\mathscr D),
\qquad
\mathscr R_0\Pi_{e,b,d}=r_*\Pi_{e,b,d},
\quad r(u,v)=(-u,-v).
\]

One and the same reversal is applied to every edge, contact type, and retained offset. Deck elements, obstacle labels, directed edge labels, and gaps are unchanged. Reversing a directed channel is expressly a different operation. This is the data-map definition missing from the preceding formulation. [S4, `def:v28-common-orientation-datum`]

The qualification concerning the marked lattice is substantive. The orbit retains the relation between transverse signs and the marked basis. It is not the quotient obtained by forgetting that relation independently. Indeed every tagged orbit meets the positive orientation sector exactly once. Even when all laws themselves are reflection invariant, the two tagged representatives remain distinct because their orientation characters differ. There is no missing fixed-point case in the stated two-element orbit.

Thus the quotient is geometric convention bookkeeping for the complete marked signed information, not a newly proved statistical recovery theorem from erased signs. The manuscript now says this. It would be wrong to read the result as reconstruction from a collection of independently unorientated channels or from unsigned endpoint samples.

### 2.2 Recovery and gluing really are equivariant

Set \(J(x,y)=(x,-y)\). The representative transformation is

\[
(\iota,(A_e),(C_{e,\sigma}))
\longmapsto
(J\iota,(JA_eJ),(JC_{e,\sigma})).
\]

The two conjugations in \(JA_eJ\) matter: simply replacing \(A_e\) by \(JA_e\) would leave the prescribed class of proper channel placements. In the actual formula, \(JA_eJ\) remains proper, while \(J\iota\) has the opposite orientation character. At each incidence the identity is

\[
\tau_{-J\iota(\nu)}(JA_eJ)(JC_{e,\sigma})
 =J\bigl(\tau_{-\iota(\nu)}A_eC_{e,\sigma}\bigr).
\]

This verifies the deck correction as well as the curve placement. The argument does not merely compare unmarked obstacle shapes. A global proper change of representative \(B\) becomes the global proper change \(JBJ\), so the construction descends to the proper-motion quotient. Disjointness, facing geometry, flight lengths, and strict convexity are preserved. [S4, `lem:v28-reflection-equivariance`; S5]

The contact identities are also correct:

\[
S_b^r(u)=S_b(-u),\qquad q_{b,n}^r=(-1)^nq_{b,n}.
\]

They follow from reflection of finite stationary bridges and the half-line limit. They do not require identifying a smooth function with its infinite Taylor series. For exact factorized endpoint laws the single-offset inverse is independent of the chosen admissible nonzero anchor, and hence has exactly this equivariance. Section 3 explains why the word **exact** cannot be dropped when one retains a fixed anchor in an off-model formula.

### 2.3 Both directions of the Euclidean classification are supplied

The new theorem takes the disjoint union of the two corresponding signed gluing spaces and quotients it by the common involution. A proper Euclidean motion stays within a signed class. Every improper motion can be written \(BJ\), with \(B\) proper; it first changes the common representative and then identifies proper classes. Conversely, identification in the quotient yields precisely one of these two possibilities. This proves a bijection, not just an implication from congruent tables to equal data. [S4, `thm:v28-unoriented-classification`]

The singleton conclusion follows because reflection bijects the two signed gluing spaces. It does not select an arbitrary phase when a signed gluing space has several admissible elements. In particular, the inherited symmetry and signature-rigidity hypotheses remain necessary for the cited sufficient uniqueness criteria; they are not removed by writing an unoriented quotient.

### 2.4 Holonomy and the exact-inverse stability argument are sound

Positive arclength orientation reverses under reflection, so the curvature signature changes by alternating derivative signs. Unique signature matching is preserved. Cycle congruences are conjugated by \(J\), and a translation holonomy becomes the translation by its reflected vector. Thus

\[
V^r=JV,\qquad L^r=JL,\qquad (L^r)^TL^r=L^TL.
\]

The metric-free matrix identity uses independent real deck columns, not a primitive integer basis. A marked matrix of determinant other than \(\pm1\) is therefore not an objection. In the fixed-Gram problem the orientation sector must still be transported; in the rank-two refinement the recovered Gram form is reflection invariant. [S4, `cor:v28-quotient-holonomy-stability`; S8]

For an equivariant inverse \(F\) with a signed estimate valid for every representative pair used in the comparison, the quotient estimate follows by choosing a minimizing group element:

\[
\bar d'(F[D],F[E])
\le d'(F(D),F(\mathscr R^\eta E))
\le C_M\bar d([D],[E]).
\]

The sectorwise restriction is legitimate: an orbit has a representative in either sector, and estimates may be compared consistently within one sector. The conclusion retains the original fixed-order constants and assumptions. No order-independent analytic-continuation stability follows.

### 2.5 Folded observations are explicitly excluded

The four-term folded density and the pair of positive density examples correctly distinguish a law-valued orbit from a sample-space coarsening. The example is not a constructed pair of billiard tables. The author expressly avoids that stronger assertion. Neither this reviewer nor the author should promote an elementary density example into a physical nonidentifiability theorem. The active observation hierarchy now explicitly says that the common-orientation quotient is not another Markov coarsening in that hierarchy. [S4, `rem:v28-folded-records`; S6]

**Disposition of C1:** closed for the exact marked law-valued quotient that is actually defined and proved. No further unsigned-data theorem is required to close the preceding request.

## 3. Technical qualification T1: fixed-anchor off-model reconstruction is not automatically equivariant

**Locations:** `cor:v28-quotient-holonomy-stability` in S4 and `prop:v26-density-stability` in S7.  
**Severity:** bounded mathematical scope clarification; not a counterexample to exact-law rigidity.

The interior stability proposition deliberately allows a perturbed density that does not factorize. On that neighborhood the explicit formula uses a fixed anchor \(a\). Let

\[
T_a(f)(u)=\frac{1-R_f(u,a)}{\sqrt{1-R_f(a,a)}},
\qquad F_a(f)(u)=\frac{dT_a(f)(u)}{1+T_a(f)(u)}.
\]

For arbitrary such densities, direct substitution gives

\[
F_a(f^r)(u)=F_{-a}(f)(-u),
\]

not generally \(F_a(f)(-u)\). The exact model hides the distinction because every admissible anchor recovers the same action. An empirical or perturbed density need not satisfy that rank-one identity.

### 3.1 An explicit positive-density witness

Take \(d=1\), \(S(u)=u^2\), and on the unit disk define

\[
f_\varepsilon(u,v)=\frac2\pi(1-u^2-v^2)_+
                  \bigl(1+\varepsilon uv(u+v)\bigr).
\]

For sufficiently small positive \(\varepsilon\) this is a probability density. The unperturbed radial density integrates to one, and the perturbation has zero integral by simultaneous reversal. The multiplier is positive on the disk for the displayed numerical choice below. On a fixed square \(I^2\), with \(I=[-1/3,1/3]\), it is smooth and strictly positive, and it approaches the exact factorized density in every fixed \(C^M\) norm as \(\varepsilon\to0\). It is therefore a legitimate off-model perturbation of the kind allowed in the interior formula; no assertion of physical billiard realizability is needed or made.

Put \(a=1/4\), \(\varepsilon=1/100\),

\[
D=\left(\frac{a^2}{1-a^2}\right)^2=\frac1{225},
\qquad R_{f_0}(a,a)=\frac{224}{225},
\qquad h=2\varepsilon a^3R_{f_0}(a,a)=\frac7{22500}.
\]

Both anchor radicals are positive since \(D-h>0\). The perturbation vanishes on the axes and at \((-a,a)\). Consequently

\[
T_a(f_\varepsilon^r)(a)^2=D+h=\frac{107}{22500},
\qquad
\bigl(T_a(f_\varepsilon)(-a)\bigr)^2
 =\frac{D^2}{D-h}=\frac4{837}.
\]

Their difference is exactly

\[
-\frac{h^2}{D-h}=-\frac{49}{2092500}\ne0.
\]

Both quantities before squaring are positive. Since \(t\mapsto t/(1+t)\) is injective there, the action reconstructions also differ. The same reasoning gives arbitrarily small nonzero perturbations. This is an algebraic proof of nonequivariance of the **fixed-anchor off-model extension**, not a numerical suggestion.

### 3.2 What this does and does not require

The conditional orbit-stability proof in v28 is valid for an equivariant \(F\). The exact signed inverse has that property. The counterexample therefore does not refute the exact corollary on the physical image, nor the unoriented classification. What fails is an unqualified application of that proof to the fixed-anchor extension in the earlier arbitrary-density stability proposition.

**Requested clarification T1:** state explicitly that the corollary applies to the equivariant exact inverse, or specify how the anchor is transported when extending it to perturbed densities. A minimal compatible choice is to use anchor \(\epsilon a\) in sector \(\epsilon\). Then

\[
F_{-a}(f^r)=r^*F_a(f)
\]

holds identically on the common formula domain. The positive anchor bounds in the two sectors follow from the corresponding compact nondegenerate bounds, so the fixed-order Lipschitz argument is preserved. The amplitude formula transforms in the same way. No new physical inverse theorem, rate, or removal of an existing result is required.

This qualification should be recorded rather than left implicit, especially because the text discusses densities on symmetric boxes immediately after the orbit-stability argument. It is a finite repair with an exact identity, not a reason to restart the revision programme.

## 4. Re-examination of the principal inherited arguments

### 4.1 The amplitude-free law inverse survives the audit

For the exact interior density, direct cancellation yields

\[
1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}
 =\frac{S(u)}{d-S(u)}\frac{S(v)}{d-S(v)}.
\]

Strict convexity and a nonzero anchor fix the positive scalar root. The formula does not take a differentiated square root at the degenerate minimum. The manuscript also correctly distinguishes a continuous density determined by a law from values supplied by a finite sample. The normalization and flux amplitude are removed algebraically, while the onset gap remains a separate datum. [S7]

The finite-flight statement uses differentiated interior estimates and a separate control of the normalizing integral. It does not infer derivative convergence from total variation. My inspection of this step is conditional on the inherited differentiated relative estimates; I have not independently reproved their complete input chain here. T1 does not invalidate the signed-coordinate Lipschitz estimate itself.

### 4.2 The smooth finite-jet repair remains substantive

The weighted Green estimate uses two summable geometric series, with \(e^{-\gamma_-}<\rho<1\). The nonlinear operator is local, its small perturbation is controlled in the weighted sequence norm, and the inverse follows from a Neumann bound. At each fixed derivative order the same inverse controls the highest orbit derivative. [S9, `lem:v22-weighted-inverse`]

For two smooth graph pairs with equal jets through order \(M\), the functional interpolation argument is the essential repair. It treats the difference of the graphs as a function, not merely as a finite list of coordinates. The exact finite-truncation derivative cancels interior orbit variations; its terminal term tends to zero. Integrating in the interpolation parameter before passing to the infinite limit gives

\[
|S_b^{[1]}(u)-S_b^{[0]}(u)|
 \le C_M|u|^{M+1}\sum_{i\ge0}\rho^{(M+1)i}.
\]

This proves equality of finite action jets without assuming convergence of a smooth Taylor series. The uniform statement requires functional graph-norm bounds, not just bounded coefficients. Analytic continuation is used only later for complete boundary images. I find no reason to reopen the v27 smooth-remainder objection. [S9, `lem:v27-smooth-jet-factorization`]

The homogeneous isolation then gives the last-jet block by counting the starting site once and every interior site twice. The own-contact and opposite-contact geometric sums are respectively \(\coth(n\gamma)\) and \(\mathfrak r_b^n\operatorname{csch}(n\gamma)\). Their determinant is one because \(\mathfrak r_0\mathfrak r_1=1\). The lower-jet remainder and the leading curvature inverse yield a finite block-triangular inverse. This is a fixed-order conclusion, not an infinite-dimensional conditioning result.

### 4.3 The observed-contact dichotomy remains correctly qualified

The current statement compares matched successful records: either both retain residual time or both delete it. When the observed type is the varying homothetic obstacle, distinct boundary curves meet only at the fixed anchor. Removing that zero-probability point produces pairwise disjoint full-probability events. For a kernel applied to a commonly dominated scalar family, all output laws are dominated by one probability measure, which can charge only countably many such disjoint events. The worst-case deficiency is therefore one for every finite successful-sample size. [S10]

When the observed type is the fixed obstacle, its graph embedding and transverse projection are parameter-independent inverse maps on the supported boxes. The two matched experiments are equivalent. The fixed obstacle is a known constant of that specified family, not a hidden unknown supplied to a kernel. This resolves the historical type error and should remain intact.

None of these conditional successful-law statements permits ignoring failed preparations in the separate charged acquisition experiment. Nor does equality of two exact law-valued data sets imply statistical equivalence between finite samples of scalar coordinates and noiseless positions.

## 5. C2 remains open: no complete native submission was verified

The live run collection for the revision branch contained two runs. I separately read their job responses. [S13]

| Run | Job | Source commit | Observed completion | Executed steps |
|---|---|---|---|---|
| `34677164341` | `103508962672` | `6d8f158c60f3636c572daa64779f57c9c9ec757b` | September 12, 2026, 06:03:58 UTC; failure | `[]` |
| `34677568860` | `103510063039` | `c6827750cc595d058a1786aa818a57d52266cfdc` | September 12, 2026, 06:13:29 UTC; failure | `[]` |

Both responses have runner ID zero and an empty runner name. Neither job executed checkout, the source scanner, or TeX. The later reviewed head is an evidence-only successor, not a successfully compiled release. The separate source comparison shows that the mathematical files did not change after the first source commit. [S2]

These observations establish the absence of a successful native execution in the inspected runs. They do not establish a TeX error, a billing cause, a permissions cause, or any other explanation of the pre-step failure. I did not rerun workflows or modify permissions as part of this review.

The author reports an eight-page revised-module fixture with ten unresolved-reference occurrences involving eight inherited labels. That is expressly not the native main article. I read the verification record, but did not independently compile or visually inspect that fixture or the complete PDFs. Missing references in a fixture that omits their defining sections are not, by themselves, missing references in the full manuscript. Conversely, the fixture cannot certify the full manuscript. [S14]

**Required completion C2 remains the same:** provide one immutable-source package containing the complete native input closure for both `main.tex` and `two_collision.tex`, an executed recursive reference/citation audit including companion references, successful native engine logs and versions, complete PDFs with hashes and page metadata, and an explicit inspection of remaining layout warnings. If the build source and reviewed head differ only in documentation, demonstrate the identity of the mathematical input closure.

A clean local execution or another functioning environment is sufficient. A particular hosted runner and repeated unsuccessful workflow launches are not mathematical requirements. The new review does not require deletion of auxiliary mathematics or replacement of the full paper by the changed-module fixture. Compilation is not proof; nevertheless an assembled, inspectable submission is necessary for a submission-level recommendation.

## 6. Journal-level assessment and presentation

The most substantial candidate contribution remains the geometry-specific chain from a uniform nonlinear relative law to unsymmetrized actions, finite contact jets, and intrinsic periodic recovery under explicit incidence hypotheses. The orientation quotient is a correct clarification of that chain; it should not be presented as an independent breakthrough. The lattice matrix identity, compact inverse-continuity argument, and group quotient are useful organizing steps, not substitutes for the difficult forward estimates and contact inverse. [S4, S7–S9, S11]

The distinction between exact transverse laws and physical position records is now essential to an honest account of significance. A noiseless planar endpoint already supplies a point on the boundary. A physical acquisition theorem in that richer experiment must be compared with the direct graph-sampling route, not described as establishing that half-line inversion is necessary. The inspected introduction makes that distinction and acknowledges non-effective compact inverse moduli. I do not demand that the same clarification be converted into a new result. [S11]

The limited primary-source check supports caution about priority claims. De Simoi–Kaloshin–Leguil study marked-length determination for analytic chaotic billiards under symmetry and genericity assumptions; Finamore–Leguil study an enriched marked length spectrum for finite-horizon Sinai billiards; Meister–Reiß provide a nonregular regression-to-Poisson equivalence precedent. These are different observation maps and hypotheses. Their available abstracts do not establish either that A2 is a consequence of those papers or that its entire mechanism has no precedent. An exhaustive priority assessment and independent checking of every theorem in those sources were not performed. [L1–L3]

A large number of revisions or finite checks does not answer the top-four significance question. On this audit I would not issue an unconditional recommendation to accept the complete article at that level. That is distinct from asserting that the present core inverse is false or demanding an unrelated theorem merely to keep the review negative.

One minor presentation issue remains in the observation hierarchy. A per-preparation record and a stopped multi-preparation transcript do not literally form successive nested sigma-fields on the same sample space until a common full stopped-history space is specified. A cleaner formulation starts with that full acquisition transcript, takes endpoint-time and count-endpoint coarsenings there, and identifies the per-preparation map as their building block. This is an expository correction, not a demonstrated failure of the adaptive transfer theorem. [S6]

## 7. Executed diagnostics and evidentiary limits

The author's exact script was reproduced byte-for-byte from the pinned source. Its Git blob was checked as `8467debd339b36a7c51db0486fb542b28497485b`. It was run with Python 3.13.5 in ordinary and optimized modes. Both outputs were byte-identical and reproduced all **883** recorded checks. The output itself has the existing Git blob `8edbf8a22284816c1dc555c026dd962068fbb3bd`; it is included here as [author_checks_reproduced.json](author_checks_reproduced.json). This is an actual rerun, not a restatement of the author's log. [S15]

The separate [independent script](independent_checks.py) was written for this review and run in both modes with byte-identical output. Its **1,784** exact finite checks cover affine conjugation and changes of root representative, nonprimitive rank-two recovery, asymmetric density inversion, exact inverse equivariance, positive leading geometry, determinant-one blocks, folded and samplewise-orbit examples, tagged symmetric-law edge cases, and the fixed-anchor counterexample with its transported-anchor repair. The [result file](independent_checks.json) records the source commit, script hash, and rational witness.

The script uses exact rational arithmetic and explicit exceptions, not removable assertions. Most checks are inexpensive grid identities. Their number is not a measure of theorem coverage. In particular, they do not prove infinite half-line convergence, physical realizability of arbitrary densities, analytic continuation, global statistical consistency, or full Le Cam equivalence. The new nonequivariance conclusion rests on the explicit algebra in Section 3; the finite evaluations make the calculation reproducible but do not replace it.

No complete native build, full recursive source audit, proof-assistant verification, or complete-PDF visual inspection was executed in this review. Historical v27 author and referee suites were not rerun and are not included in the counts above.

## 8. Bounded requests and final disposition

**C1 is closed** for the exact common-orientation datum. Preserve the diagonal action, the transported marked-lattice character, and the distinction from folded observations.

**T1 requires a short explicit domain/convention clarification:** keep orbit stability on the equivariant exact inverse, or transport the anchor when an arbitrary-density extension is used. The algebraic remedy is given above. Do not misreport the witness as a physical-table nonidentifiability result or as a failure of the exact classification.

**C2 remains open** until an actually executed, source-pinned complete native main/companion submission is supplied and inspected. Another manifest or changed-module fixture is not that execution.

The v27 observed-type and smooth-remainder repairs should remain closed on their merits. The minor hierarchy wording should be cleaned up without changing its intended experiments. No new theorem is demanded merely because previous objections have been answered. The manuscript must be judged on what is proved, what remains unchecked, and what its stated observations actually contain—not on an automatic cycle of escalating referee demands.

## Source key

Repository references are relative to `papers/A2-v17-boundary-information-coarsening` at commit `f5fcd5e319cb4a37bdcbf8d9f9d190786ec7fc7d`, except where marked repository-relative. Stable theorem labels are used instead of invented PDF page numbers. The [source audit](SOURCE_AUDIT.md) records scope and hashes.

- **S1:** `main.tex`, repository root `README.md`, and `ACTIVE_SOURCE_MANIFEST_V28.md`.
- **S2:** Repository comparisons `e5a153b1...f5fcd5e3` and `6d8f158c...f5fcd5e3`, and the revision commit metadata.
- **S3:** `RESPONSE_TO_REFEREE_V28.md`; repository-relative `reviews/a2-v27-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`.
- **S4:** `article/23h_global_orientation_quotient_v28.tex`.
- **S5:** `article/23b_intrinsic_multichannel_rigidity_v28.tex`.
- **S6:** `article/01b_observation_hierarchy_v28.tex`.
- **S7:** `article/23f_single_offset_law_inverse_v26.tex`.
- **S8:** `article/23d_rank_two_lattice_recovery_v24.tex`.
- **S9:** `article/23a_signed_endpoint_rigidity_v27.tex`.
- **S10:** `article/18f_domination_and_position_comparison_v27.tex`, main domination and observed-type proofs and examples.
- **S11:** `article/01_introduction_v27.tex`, inspected through the beginning of the local-information discussion.
- **S12:** `article/20_boundary_compatibility.tex`, sampled positive factorization, Volterra uniqueness, profile stability, and finite-jet transform.
- **S13:** Live GitHub Actions run collection for the revision branch, and job collections for runs `34677164341` and `34677568860`; normalized observations in [ci_observations.json](ci_observations.json).
- **S14:** `VERIFICATION_V28.md` and `ACTIVE_SOURCE_MANIFEST_V28.md`; their reported typesetting and preservation executions are not independent whole-native executions by this reviewer.
- **S15:** `tools/check_revision_v28.py`, independently rerun after exact blob verification.

### Primary literature checked for the limited comparison

**L1.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, last revised August 17, 2022; related publication DOI `10.1007/s00222-023-01191-8`. The arXiv abstract and version metadata were read on September 12, 2026.

**L2.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, submitted October 21, 2025. The arXiv abstract and version metadata were read on September 12, 2026; no later version or publication status is asserted here.

**L3.** A. Meister and M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, arXiv:1101.5248v1, submitted January 27, 2011. The arXiv abstract and version metadata were read on September 12, 2026. This is a precedent for the type of limiting experiment, not an A2 billiard theorem.
