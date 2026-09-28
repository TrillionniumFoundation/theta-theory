# External top-four referee report on A2 v15

**Manuscript:** Qian Qi, *Nonlinear boundary laws and asymmetric two-contact rigidity in dispersing billiards*  
**Latest delivery branch:** `revision/a2-v15-asymmetric-contact-rigidity-2026-09-28`  
**Latest delivery head:** `0dbe3b317da4b2b14f7a99e000da808fbbf8691e`  
**Reviewed mathematical manuscript commit:** `00f27ebd0071d75504995b61f9a15c67f896188f`  
**Mathematical-source checkpoint:** `cbb48f18a2820d85d0f9ba21f77224db6d1e5420`  
**Paper directory:** `papers/A2-v15-asymmetric-contact-rigidity`  
**Date:** 28 September 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

This is not a rejection for a known mathematical error. Version 15 is a genuine and substantial revision. It responds directly to the preceding report by producing a theorem-led primary article and, more importantly, by removing the individual-evenness assumption from the contact inverse after adding an explicit orientation-sensitive observable. On the portions audited in detail, I found no fatal counterexample to the new local law, the odd highest-jet block, the triangular recursion, the support-function realization, or the finite-window design.

The reason for the negative decision is the level and nature of the advance. The new theorem changes the information set from two scalar count germs to four framed germs: two count germs and two signed endpoint-position moments. The signed moment is deliberately chosen to pair an odd graph perturbation with an odd mark, thereby making the leading contribution even and nonzero. This is an elegant and apparently correct local moment inversion. It is not, however, an asymmetric rigidity theorem for the original count-only law, and it does not give a natural global rigidity statement for the billiard table. It recovers two participating analytic boundary images in supplied contact frames, with the gap, labels, separate curvatures, contact patches and transverse-axis orientation already supplied.

At a strong specialist journal, after a focused literature revision and some tightening of the theorem category, I would regard the new primary article as potentially publishable. In my judgment it still does not meet the exceptional conceptual threshold of the four journals named above. I would not recommend another open-ended revision cycle at that venue.

## 2. What v15 actually proves

The data for the new inverse are, for each orientation `b=0,1`,

\[
P_b(d)=\Pr(E_{2,b}(d)),\qquad
R_b(d)=\mathbb E[(u+v)\mathbf 1_{E_{2,b}(d)}].
\]

Here `u,v` are signed transverse coordinates at the first and last impacts in the three-impact itinerary `b,1-b,b`. The second quantity is an unconditional moment: failures contribute zero. The selected normal channel, its labels, the common transverse-axis orientation, the gap and the two separate contact curvatures are supplied. Area may be unknown.

The main theorem then asserts, at every fixed jet order:

1. the common leading probability coefficient determines the free area;
2. probability coefficients recover successive even graph jets;
3. signed-moment coefficients recover the intervening odd graph jets;
4. the two orientations give invertible two-by-two highest-jet blocks at every degree, including equal curvatures;
5. real-analytic germs determine the two participating analytic boundary images in the supplied frames;
6. actual periodic billiard families realize all odd and even directions independently;
7. finitely many positive-window scalar means are local coordinates on those supplied families;
8. an explicitly randomized binary compression has the ordinary fixed-dimensional parametric confidence and risk orders.

The full earlier smooth relative determinant law, symmetrized-profile inverse, Volterra compatibility, Abel stability and auxiliary statistical constructions are moved to a 133-page companion volume rather than discarded.

This is a much cleaner mathematical object than v14. The new article has a dominant theorem and a coherent proof sequence.

## 3. Source identity and reproducibility

The three v15 revision aliases found at the review cutoff all resolved to `0dbe3b...`. That commit changes only delivery metadata. Its `DELIVERY.json` binds the actual qualified manuscript to `00f27e...`, with paper tree `db84120af7be42acd785a9bc8d87dc6c652ee8d9`. I reviewed the mathematics at that immutable commit while creating the review branch from the latest delivery head.

The author records a successful local source-content qualification:

- 2,747 new exact finite checks in normal and optimized Python;
- 1,588 retained v14 checks in both modes;
- complete builds of 13, 133 and 7 pages;
- no final TeX warnings recorded for those builds;
- source-preservation checks before and after execution;
- a manifest binding the mathematical source content.

This evidence is materially better than the queued-state evidence available during the v14 review. It remains author-produced reproducibility evidence rather than independent proof certification.

At the final cutoff for this report, GitHub Actions run `36385817642` for the v15 delivery head was still `queued`, with no conclusion. I therefore record the commit-bound local receipt but do not claim a completed hosted v15 run.

The accompanying `SOURCE_AUDIT.md` gives the complete source chain and file scope.

## 4. Correctness audit of the new core

### 4.1 Exact local probability and signed-moment laws

The local three-impact path is obtained by eliminating the stationary middle coordinate. The quadratic reduced action has Hessian

\[
H_b=\frac1g
\begin{pmatrix}
 c_b-(2c_o)^{-1}&-(2c_o)^{-1}\\
 -(2c_o)^{-1}&c_b-(2c_o)^{-1}
\end{pmatrix},
\]

which is positive definite because `c_0c_1>1`. The generating-function Jacobian changes the local phase density to `(-W_{uv}) du dv dr`, and the residual-time interval is `0<r<d-E_b(u,v)`. This yields

\[
G_b(d)=\frac{a_b}{\pi d^2}\int(d-E_b)_+b_b\,du\,dv,
\]

and

\[
J_b(d)=\frac{a_b}{\pi d^2}\int(u+v)(d-E_b)_+b_b\,du\,dv.
\]

The fixed Morse-disk argument explains smooth extension in `d`: after scaling by `h=\sqrt d`, odd integrated powers cancel under `X\mapsto-X`. The marked amplitude vanishes at the origin, so `J_b(d)=O(d)`.

I found this calculation coherent. It keeps the event, residual time, failures and physical phase normalization explicit. It does not replace the exact two-flight experiment by a limiting law.

### 4.2 Even and odd highest-jet blocks

For even degree `2m`, the paper retains the block

\[
D_{Q_{2m}}\xi_{m-1}
=-\begin{pmatrix}(1+2z)^m&1+2mz\\1+2mz&(1+2z)^m\end{pmatrix}
\operatorname{diag}(k_mL_0^m,k_mL_1^m).
\]

For odd degree `2m+1`, the new block is

\[
D_{Q_{2m+1}}\eta_m
=-\begin{pmatrix}
 c_1(1+2z)^m&1+2mz\\
 1+2mz&c_0(1+2z)^m
\end{pmatrix}
\operatorname{diag}(2c_0C_mL_0^{m+1},2c_1C_mL_1^{m+1}).
\]

The mechanism is transparent. The action variation has degree `r`; the opposite-contact twist variation has degree `r-2`; the signed mark adds one degree. The cross-moment identity reduces `t\ell^{2m+1}` to an even moment. Both action and twist contributions are needed.

The determinant separation is strict:

\[
c_0c_1(1+2z)^{2m}-(1+2mz)^2
\ge z(1+2mz)^2>0.
\]

This follows from `c_0c_1=1+z` and Bernoulli's inequality. Equal curvatures cause no degeneracy.

I independently recomputed all four entries from closed unweighted and residual-weighted ellipse moments, rather than importing the author's polynomial/Wick implementation. On rational grids in `g,c_0,c_1` and degrees `3` through `19`, 5,100 entry comparisons, 1,275 determinant tests and all separation controls passed exactly. The cubic reference block is

\[
-\frac7{108}\begin{pmatrix}2&1\\1&2\end{pmatrix},
\]

and the quartic block agrees with the retained v14 value.

These diagnostics strongly support the printed finite algebra. They do not by themselves prove the nonlinear finite-jet degree bookkeeping.

### 4.3 Independence from arbitrary lower asymmetric jets

The important claim is not merely a linearization at an even reference contact. The paper argues that, at the highest degree relevant to a coefficient, every product with a lower nonlinear correction carries an extra power of `h`; odd powers disappear after fixed-domain integration. Hence the displayed derivative is independent of all lower odd and even jets and the coefficient is affine in the highest jet.

This is the right argument, and I did not find a contradictory low-order term. The presentation would nevertheless benefit from a compact standalone filtration lemma: assign weights to the reduced action, twist, mark and Morse map, and state once that the coefficient functional is triangular in that filtration. At present the reasoning is spread across prose. For a theorem whose central claim is “all degrees with arbitrary lower asymmetry,” this deserves theorem-level visibility.

### 4.4 Recursive recovery and analytic continuation

Once the highest-jet blocks are invertible, the degree-ordered recursion

\[
Q_r=B_r^{-1}\{Y_r-F_r(Q_3,\ldots,Q_{r-1})\}
\]

is immediate and gives fixed-order analytic local coordinates. Compact positive leading-geometry boxes give finite-order lower bounds on all denominators. The manuscript correctly avoids any uniform-in-order stability claim.

The last step, from equality of one local analytic graph germ to equality of the connected analytic boundary image, is plausible and standard, but currently compressed into a short continuation paragraph. A revised version should state the precise analytic-submanifold identity principle being used, including how continuation around a closed embedded curve avoids chart and monodromy ambiguity. This is a minor proof-presentation issue, not a counterexample.

### 4.5 Physical realization

The support family uses perturbations

\[
\{s_{0r}w_0(\theta)+s_{1r}w_1(\theta)\}\sin^r\theta,
\qquad 3\le r\le K,
\]

with one common global transverse coordinate at the two horizontal contacts. The left-contact sign convention is checked rather than hidden. The support-to-graph diagonal is

\[
\frac{\partial q_{b,r}}{\partial s_{b,r}}=-r!\kappa_b^r,
\]

while the opposite weight begins two orders later. The Jacobian is therefore triangular at every parity. A higher-order support term supplies an independent area direction without changing the displayed contact jets.

The positivity, embedding, nearest-neighbor gap and first-hit clearance arguments are local perturbation arguments around the disk and are adequate for the stated existence theorem. The conclusion is an actual family of billiard tables, not a formal jet image.

### 4.6 Positive-window coordinates and binary compression

For fixed area, ordinary Vandermonde blocks recover the finite coefficient vector. With area free, the two count orientations share the intercept `\alpha`; `n_e+1` nodes in one orientation and `n_e` in the other give an invertible shared-intercept matrix. Moment blocks have no constant term. Remainders are one order higher, so preconditioning turns them into `O(h)` perturbations.

The review's independent script checked fixed- and free-area matrices for orders `K=3,...,20`, three rational node scales, and repeated-node singular controls. All passed.

The statistical theorem is carefully scoped. The real signed mark is first observed and then compressed to a Bernoulli bit using independent private randomization. The seed and original mark are not returned. The lower bound is only for this specified finite collection of compressed channels, not for the uncompressed endpoint experiment. Once the finite mean map is bi-Lipschitz and all Bernoulli means have fixed margins, the `N^{-1}` risk is standard.

I found no logical defect in this section. I also do not regard its statistical part as an independent top-four contribution.

## 5. The central information-set issue

The strongest conceptual reservation is that v15 does not solve the asymmetric inverse problem for the v14 probability data. It solves a different, explicitly enriched problem.

The transformation

\[
\psi_b(y)\mapsto\psi_b(-y),\qquad b=0,1,
\]

preserves the two unmarked count germs and reverses the two signed moments. This proves that an **oriented** inverse cannot follow from counts alone. It does not prove that the count germs fail to determine the two asymmetric contacts modulo the simultaneous reflection. The latter is the natural quotient problem left open by the reflection obstruction.

The signed observable fixes precisely that parity ambiguity at the linear highest-jet level. It is mathematically legitimate and experimentally explicit, but it is also tailored to the missing odd information. The endpoint sensor has access to substantially more than the collision count before compression. Thus the main theorem should be understood as a **framed signed-moment contact inverse**, not as the removal of symmetry from the original count-law rigidity theorem.

This distinction is acknowledged in the body, but it should govern the title, abstract and significance discussion. At present “asymmetric two-contact rigidity” is broader than the intrinsic theorem unless the framed enriched information category is stated immediately beside it.

A stronger and more natural advance would be one of the following:

- recover asymmetric contacts from the two count germs modulo common transverse reflection;
- prove that a natural intrinsic marked distribution, rather than a chosen first moment in a supplied frame, determines the contacts;
- derive a global table-rigidity consequence from the local invariant;
- show that the signed moment is canonically extractable from a broader observation whose definition does not presuppose the contact frame.

I do not require all of these. The point is that the present enrichment closes the algebraic parity gap without settling the more intrinsic count-only quotient problem.

## 6. Novelty and literature position

A targeted search did not locate an earlier theorem with exactly the four A2 germs and the printed odd block. The signed-moment recursion therefore appears plausibly new.

The primary article's literature discussion is nevertheless inadequate for a top-journal submission. Its bibliography contains only De Simoi–Kaloshin–Leguil and the internal companion. Relevant comparison lines include:

- recovery of curvature and Lyapunov data from marked length spectra;
- global analytic marked-length determination under symmetry and genericity;
- homoclinic conjugacy and determination of a third scatterer from two known scatterers plus marked lengths;
- enriched marked-length rigidity for finite-horizon Sinai billiards;
- formal all-order reconstruction in analytic billiard normal-form problems where odd derivatives are treated as parameters;
- dynamical and Laplace spectral rigidity results for symmetric convex billiards.

These works do not subsume A2. They do determine what must be demonstrated for significance: why four highly local, frame-dependent scalar germs and a triangular moment calculation reveal a principle that goes beyond another tailored inverse coordinate system.

`LITERATURE_AUDIT.md` records the primary sources and exact comparison scope. No exhaustive novelty clearance is claimed.

## 7. Top-four significance assessment

The positive case is real:

- the new inverse uses only four scalar germs rather than a full endpoint distribution;
- the odd block is explicit at every order;
- no curvature-separation denominator or higher-jet genericity is needed;
- arbitrary lower asymmetric jets are allowed;
- the directions are realized in actual periodic billiards;
- the source has been reorganized around one theorem.

The negative case is stronger at the requested editorial level:

1. **The observation is enriched and framed.** The key new datum is chosen to expose odd parity and requires endpoint-position sensing plus a supplied transverse orientation.
2. **The target is local.** Only two participating contact germs or analytic boundary images are recovered. Unvisited obstacles and whole-table geometry remain free.
3. **Substantial leading geometry is supplied.** Labels, gap, separate curvatures, contact patches and frames are not recovered by the new theorem.
4. **The algebraic mechanism is finite-dimensional and triangular.** The cross-moment identity and determinant estimate are elegant, but they do not yet reveal a broader rigidity principle.
5. **The statistical conclusions are regular consequences.** They do not create a new asymptotic regime.
6. **The long smooth theory remains a separate large project.** It recovers symmetrized profiles rather than asymmetric contacts and is carried in a 133-page internal companion.

For these reasons I do not see the exceptional breadth or conceptual transformation expected for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 8. Manuscript architecture

Version 15 materially improves the v14 architecture. The 13-page primary article is theorem-led, and detailed provenance has been removed from the mathematical narrative.

A submission issue remains. The primary article repeatedly cites the 133-page `complete/main.tex` as an internal companion. The status of that volume must be formalized:

- If it is part of the submission, the editor and referees are effectively being asked to assess a roughly 153-page package, and the relationship between the two papers must be stated as a formal companion submission.
- If it is not part of the submission, the primary article should not rely on an internal repository path as the proof source for substantial smooth-law assertions.

The new asymmetric theorem itself is mostly self-contained. I recommend reducing Section 5 to the comparison needed for the new theorem and treating the older smooth project as a separately submitted paper with a normal bibliographic identity.

## 9. Required corrections for any resubmission

1. **Name the information category precisely.** Put “signed endpoint moment,” “supplied contact frames,” and “framed recovery” in the title or first sentence of the abstract.
2. **Discuss the count-only quotient problem.** State explicitly that count-only recovery modulo simultaneous transverse reflection is not proved, and explain whether it is expected to hold.
3. **Expand the literature section and bibliography.** The two-entry bibliography is not acceptable for the claimed inverse-rigidity scope.
4. **Promote the filtration argument to a lemma.** Make the independence of the highest-jet block from arbitrary lower asymmetric jets mechanically checkable.
5. **State a precise analytic continuation lemma.** Clarify the category in which a local analytic graph germ determines the connected boundary image.
6. **Formalize the companion.** Do not cite an internal source path as though it were an ordinary publication without explaining its submission and archival status.
7. **Preserve the experiment distinction.** Never describe the Bernoulli compression as count-only; the endpoint mark is observed before compression.
8. **Close hosted reproducibility separately.** A later successful workflow may be recorded, but it should not be retroactively substituted for evidence available at the review cutoff.

These corrections would improve a specialist-journal submission. They would not, by themselves, change my top-four significance judgment.

## 10. Independent diagnostics and limits

The accompanying `verify_review.py` imports no author code. It uses exact rational arithmetic and a closed-moment implementation different from the author's polynomial-pairing checker. It performs 7,907 checks:

- 5,100 displayed block-entry comparisons;
- 1,275 block determinant tests;
- 675 odd separation tests;
- 600 even separation tests;
- 3 low-degree reference blocks;
- 54 fixed-area window designs;
- 54 free-area shared-intercept designs;
- 108 deliberately singular controls;
- 18 dimension identities;
- 18 area-direction checks;
- 2 parity controls.

All passed. These computations are finite diagnostics only. I did not independently re-run the complete TeX toolchain, formally verify the Morse-domain filtration, simulate nonlinear billiard trajectories, or re-prove every theorem in the retained companion.

The literature search was targeted rather than exhaustive. The report makes no claim of a complete priority determination.

## 11. Final verdict

**Response to the v14 report:** substantial and mathematically meaningful. The paper now has a real asymmetric inverse theorem, a clear physical realization, a coherent primary article, and much stronger reproducibility evidence.

**Correctness:** no fatal counterexample found in the new v15 core. The explicit all-degree blocks and finite-window matrices survived independent exact checks. Several proof and presentation points should be strengthened, but I do not base the rejection on a known false theorem.

**Significance:** the theorem obtains framed local contact recovery by adding a purpose-built signed endpoint moment to the original count data. It does not solve the count-only asymmetric quotient problem, recover unsupplied leading geometry, or yield whole-table rigidity. The statistical consequences are regular once local invertibility is known.

**Recommendation: reject at the requested Annals/Acta/Inventiones/JAMS benchmark.** A substantially revised version centered on the framed signed-moment theorem could be a serious candidate for a strong specialist journal.
