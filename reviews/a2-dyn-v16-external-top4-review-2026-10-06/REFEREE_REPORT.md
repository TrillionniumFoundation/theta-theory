# External top-four referee report on A2-DYN revision 16

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v16-referee-response-2026-10-06`, `revision/a2-dyn-v16-referee-copy-2026-10-06`  
**Reviewed commit:** `2054310e587e576ce593112c30cdfabac6742105`  
**Reviewed repository tree:** `8143830ccaf76746e76818a6060270914cc643ec`  
**Active manuscript directory:** `papers/A2-DYN-v16-referee-response`  
**Immediate author baseline:** revision 15 at `656104408b8f9d62ccab0b1d7bc847e3be950a08`  
**Controlling substantive report:** `reviews/a2-dyn-v14-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `43d797ce65ad5e4cf92f874a6656c9cd0af9d572` / `197a42fbe2c815860423fa405f10e96cbe82e3d4`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revisions 15 and 16 contain genuine and technically substantial new mathematics. Revision 15 completes the measurable arithmetic of physical collision phases, including irrational spatial frequencies, and proves quantitative defect lower bounds for bounded-variation circle phases and normalized complex functions on fixed compact nonzero collision-frequency bands. Revision 16 develops a different argument at frequencies tending to zero, proves a quantitative finite-record variation theorem, constructs an exact lift from the actual return system to the collision tower, regularizes that lift with explicit error and BV budgets, and transfers the collision defect bounds to the genuine unbounded return record throughout the intervening annulus

\[
 2n^{-99/200}\le |z|\le n^{-2/5}.
\]

I found no decisive counterexample in the four new mathematical modules audited here:

- `core/34_complete_phase_arithmetic.tex`;
- `core/35_quantitative_phase_defects.tex`;
- `core/36_near_origin_defects.tex`;
- `core/37_actual_return_defects.tex`.

The complete-phase argument avoids a rationality assumption on the spatial character; the fixed-band proof distinguishes exact phase rigidity from approximate-vector coercivity; the near-origin proof uses the already established uniform ellipticity at the correct diffusive collision scale; and the actual-return argument localizes the lifted defect exactly at true tower tops rather than assuming that the full lift is regular. The displayed logarithmic and polynomial budgets are internally coherent.

These results close important parts of the work requested in the revision-14 report. In particular, the paper now has a quantitative function-level obstruction on the entire small-frequency annulus which had previously been left between the growing central band and the contemplated outer regimes.

The negative recommendation is not based on a source failure, a version alias, mathematical vacuity, or a detected fatal error in the new theorems. It is based on the fact that the main raw mixed-density local limit theorem remains unproved. The new conclusions are one-step defect lower bounds for bounded-BV functions. They are not yet:

1. a construction of the actual unbounded induced twist on an anisotropic distribution space;
2. a reconstruction theorem sending approximate distributional spectral vectors into the bounded-BV function class with the displayed normalization and regularity budgets;
3. a Fredholm or quasi-compact resolvent estimate on the full unit circle;
4. a decay estimate for powers of the twisted induced operator;
5. an integrated complementary-frequency estimate for the physical characteristic function or its edge-subtracted residual.

There is an additional spectral-parameter boundary. The actual-return theorem controls

\[
 f\circ F_R^*-e^{iz\cdot(G_R-\bar G_R)}f,
\]

that is, the unit spectral parameter for the centered multiplier. It does not control

\[
 f\circ F_R^*-e^{i(c+z\cdot(G_R-\bar G_R))}f
\]

uniformly for an arbitrary peripheral phase `c`. The collision theorem allows a constant collision phase, but the present tower lift does not convert an arbitrary constant per return into that collision phase. This distinction is explicitly acknowledged by the manuscript and remains essential for a full resolvent argument.

The complete critical/singular raw branch extraction and the weighted exact-conditioning chain also remain open. At the requested benchmark, an article organized around a parameter-uniform raw LLT has not yet reached its announced endpoint.

The unconditional package is nevertheless substantial. After independent specialist checking, a paper reorganized around the proved Gaussian, functional, marked, moment, nondegeneracy, phase-rigidity, and function-defect theorems could be a strong specialist contribution. That assessment is distinct from the top-four standard requested here.

## 2. Frozen source, chronology, and qualification

The two named revision-16 author branches resolve to the same commit:

`2054310e587e576ce593112c30cdfabac6742105`.

The immediate author baseline is revision 15:

`656104408b8f9d62ccab0b1d7bc847e3be950a08`.

Revision 15 did not receive a separately located substantive referee report in the branch history inspected for this review. I have therefore reviewed both the v15 additions and the v16 additions rather than treating the v15 results as already refereed.

Revision 15 adds the complete phase-arithmetic and fixed-band quantitative-defect modules. Revision 16 preserves all thirty-five inherited core modules and adds:

- `core/36_near_origin_defects.tex`;
- `core/37_actual_return_defects.tex`.

The source manifest records that the inherited core and Python files are byte-identical, that old mathematical labels and bibliography entries remain, and that the only inherited edits occur in the introduction and bibliography. It also correctly records that the anisotropic-to-BV reconstruction, full complementary integral, raw second-derivative sum, and full raw LLT are not proved.

The exact-source workflow completed successfully on both reviewed branches at the reviewed SHA:

- response branch run `37427671120`;
- referee-copy branch run `37427693440`.

For the response branch, exact checkout, source archive, native TeX installation, verification/build, and artifact upload all completed successfully. The qualification artifact is

`11395319956`,

named

`a2-dyn-v16-2054310e587e576ce593112c30cdfabac6742105`,

with digest

`sha256:48a705a03c4c49a4855762cd59e676efe2e205ab592a63b5023fe378d7af8ea1`.

These facts establish source identity and successful execution of the declared finite checks and native build. They do not certify the continuum hyperbolic, semialgebraic, tower-regularization, or raw-density arguments.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v16-external-top4-review-2026-10-06/`.

No manuscript source, author branch, workflow, earlier review, or unrelated repository path is modified.

## 3. What revisions 15 and 16 actually prove

The new chain has four levels.

### 3.1 Complete physical collision-phase arithmetic

For

\[
 \phi_{R,\omega}=u\cdot\kappa_R+s+t\tau_R,
 \qquad \omega=(u,s,t)\in\mathbb T^2\times\mathbb T\times\mathbb R,
\]

revision 15 proves that a measurable circle-valued solution of

\[
 q\circ T_R=e^{i\phi_{R,\omega}}q
\]

exists only at the zero frequency, where `q` is constant.

The proof first uses the revision-14 measurable holonomy argument to eliminate the roof and constant components. It then makes the phase constant on a positive-measure product set, propagates that value through the countable character orbit, and obtains a measurable cocycle taking values in `\mathbb Z^2/L`, where `L` is the kernel of the spatial character. If `L` is proper, a finite character produces a nonconstant invariant on a genuine finite physical cover of the billiard, contradicting ergodicity.

The same section proves that finitely many positive-measure first-return cells of the product set have records generating `\mathbb Z^3`. These are measurable witnesses of positive mass, not evaluations at isolated periodic points.

### 3.2 Quantitative defects on fixed compact nonzero bands

Revision 15 proves a finite-time stable/unstable holonomy defect estimate for bounded-BV circle phases. It handles the product-measure comparison by truncating Radon--Nikodym derivatives rather than asserting an unproved uniform density bound.

A four-corner area argument gives a logarithmic lower bound on compact roof bands. The positive-measure return witnesses then control the lattice and constant phases when the roof frequency is small. Consequently, for fixed radius and compact nonzero frequency set,

\[
 \|q\circ T_R-e^{i\phi_{R,\omega}}q\|_1
       \ge \frac{c_{R,\mathcal K}}{1+\log H}
\]

for unit phases of BV norm at most `H`.

A coarea-based circle truncation and a modulus-variance estimate reconstruct a controlled phase from a normalized complex function without assuming a positive lower modulus. This yields

\[
 \|f\circ T_R-e^{i\phi_{R,\omega}}f\|_2
       \ge \frac{c'_{R,\mathcal K}}{(1+\log H)^2}.
\]

For a fixed regularity budget, compactness gives a lower bound uniform in the physical radius. The manuscript correctly does not combine these two results into a radius-uniform logarithmic estimate for a growing regularity budget.

### 3.3 Near-origin collision defects

Revision 16 uses the bounded collision compensation

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*}
\]

and the already proved uniform ellipticity of its collision covariance.

At physical frequency `r=|z|`, it smooths only a middle collision block, with

\[
 \delta=\tfrac14r^{1/12},
 \qquad
 m\asymp r^{-2}.
\]

The smooth twisted middle power has a fixed contraction because its leading eigenvalue has real logarithm bounded above by `-c r^2`. The unsmoothing error is

\[
 O\!\left(r^{1/24}\sqrt{1+|\log r|}\right).
\]

The two endpoint functions are smoothed independently and separated from the middle twisted block by untwisted mixing segments of length `O(1+\log H)`. Iteration of an approximate phase equation over the full block produces an error proportional to the block length. Since that length is `O(r^{-2})`, the contradiction gives the quadratic phase defect

\[
 \|q\circ T_R-e^{i(\sigma+z\cdot h_R)}q\|_1\ge c r^2
\]

when `r(1+\log H)` is small.

The modulus-variance and circle-truncation argument then gives a normalized complex-function defect of order

\[
 \frac{r^2}{1+\log(H/r)}.
\]

Both conclusions are uniform in the radius and permit an arbitrary constant collision phase.

### 3.4 Exact lifting to the actual return record

Revision 16 defines the genuine collision tower over the actual return section and lifts a section function by the accumulated centered collision phase. The lift is exact on every nontop tower level. Its only defect occurs at a true tower top and is precisely

\[
 f\circ F_R^*-e^{iz\cdot(G_R-\bar G_R)}f.
\]

The norm and defect identities keep their distinct factors:

\[
 \|\mathsf L_{R,z}f\|_p^p
 =c_*\int r_R^*|f|^p\,d\nu_R^*,
\]

whereas

\[
 \|\mathcal D_{R,z,0}\mathsf L_{R,z}f\|_p^p
 =c_*\int|f\circ F_R^*-e^{iz\cdot(G_R-\bar G_R)}f|^p\,d\nu_R^*.
\]

The exact lift need not be BV. The paper truncates the tower age, smooths the initial section function, and proves

\[
 \|\mathsf L_{R,z}f-Q_{L,\epsilon}\|_1
 \le C(L\epsilon V_f+M_f e^{-cL}),
\]

with the corresponding `L^2` error and the explicit regularity budget

\[
 \|Q_{L,\epsilon}\|_{\mathrm{BV}}
 \le M_f\exp\{C L\log(2+L)\}
        (1+\epsilon^{-1}+|z|).
\]

This yields actual-return defect lower bounds. With

\[
 \Lambda=1+\log(H/r),
 \qquad
 \mathcal K(H,r)=\Lambda\log(2+\Lambda),
\]

unit section phases have defect at least `c r^2`, and normalized complex section functions have defect at least

\[
 \frac{c r^2}{\mathcal K(H,r)}.
\]

For polynomial regularity budgets these estimates hold uniformly on the entire annulus

\[
 2n^{-99/200}\le|z|\le n^{-2/5}.
\]

This is the principal new conclusion of revision 16.

## 4. Audit of the complete phase arithmetic

The spatial part of the exact-phase classification is handled more carefully than by taking a logarithm of a circle-valued function.

Once the roof and constant phases are eliminated, stable and unstable holonomy make the phase constant almost everywhere on a positive-measure product set. Ergodicity propagates the value to a countable character orbit. The quotient by the kernel of the character is countable, so the inverse from the countable range is measurable and defines a cocycle in `\mathbb Z^2/L`.

If `L` is proper, the elementary subgroup lemma gives a nonzero finite character. On the physical billiard modulo `p\Lambda`, the function

\[
 \exp\!\left(\frac{2\pi i}{p}
 [a\cdot\ell-\chi(h(x))]\right)
\]

is invariant, has modulus one, and has zero sheet average. This contradicts ergodicity of the finite cover.

The argument includes irrational spatial frequencies and does not assume that the kernel subgroup has full rank. I found the algebra coherent.

The load-bearing specialist point is the physical-cover input: the finite cover must remain a connected finite-horizon dispersing billiard in the class of the cited ergodicity theorem. The geometry appears consistent with that use, but it remains an appropriate target for an independent billiards expert.

The positive-measure witness lemma is also sound in structure. If the subgroup generated by the first-return cell records were proper, a finite character would make the tower construction close at every return and would create a forbidden exact measurable collision phase. The conclusion uses only finitely many positive-mass cells because an integer representation of the standard basis is finite.

## 5. Audit of the fixed-band quantitative phase proof

The finite-holonomy estimate telescopes the one-step defect over a fixed number of iterates. It does not estimate the BV norm of a long pullback. Smoothing is applied at the endpoints, and contraction of homogeneous stable or unstable arcs supplies the geometric smallness.

The passage from conditional-pair measures to reference product measures is not made through an unproved bounded density. Instead, the proof truncates the relevant Radon--Nikodym derivatives. The constants therefore depend on finite density-tail choices at the fixed product set. This is logically appropriate.

For roof frequencies bounded away from zero, multiplication around four oriented product-set edges gives a positive area phase. Selecting a positive-measure subset on which the symplectic area is bounded below produces the logarithmic lower bound after choosing the smoothing and iteration scales.

For small roof frequency, the finite positive-measure witnesses control the three torus phases. The integer combinations of their records transfer small return phases to the standard generators of `\mathbb Z^3`. Combining this with approximate constancy on the product set forces a one-step defect.

The complex-vector reconstruction is also correctly separated from the circle-phase theorem. The modulus of an approximate complex vector is shown to be nearly constant by collision mixing; coarea produces a finite-perimeter threshold; and the resulting circle phase has controlled BV norm even if the original function vanishes.

I found no decisive contradiction in this chain.

Two limitations are essential:

1. the logarithmic constant on a fixed compact band is proved at each fixed radius and is not quantified uniformly in the radius as `H` grows;
2. the parameter-uniform compactness theorem fixes `H` and supplies no logarithmic dependence on a growing regularity budget.

Consequently revision 15 alone would not control a radius-uniform sequence of reconstructed vectors whose BV budgets grow polynomially with time.

## 6. Audit of the diffusive near-origin collision argument

The middle block is placed at the correct scale `m\asymp r^{-2}`. Uniform positive definiteness of the covariance makes the smoothed leading eigenvalue contract by a fixed amount over that block. The analytic-radius requirement is satisfied because

\[
 r\delta^{-2}=O(r^{5/6}),
\]

and the cubic term is smaller than the quadratic term.

The proof does not apply the unsmoothed multiplier to the collision distribution space. It estimates the difference between smoothed and unsmoothed collision sums in ordinary `L^2`, obtaining the displayed `r^{1/24}` error.

The endpoint treatment is important. The proof removes the twist from two logarithmic end blocks, smooths the two endpoint phases, and uses untwisted mixing to replace both end powers by the rank-one projection. The endpoint operator loss is polynomial in the smoothing scale and is absorbed by choosing the end length proportional to `\log H`.

Iteration of the approximate phase equation gives a pairing of modulus at least `1-Nd`; the comparison bounds the same pairing by a fixed number below one. Since `N=O(r^{-2})`, the defect is at least `c r^2`.

For complex functions, the modulus-variance estimate and the controlled circle truncation produce the additional logarithmic loss. I found the scale choices and the direction of the inequalities coherent.

The theorem concerns the centered collision multiplier and permits an arbitrary constant collision phase. It is a function theorem, not a spectral theorem for distributions.

## 7. Audit of the finite-record variation theorem

The finite-record lemma is not derived from one-collision BV by composition. It gives an independent semialgebraic complexity argument.

A finite set of possible next disk centers follows from the uniform horizon. For a fixed label word, normal vectors, outgoing velocities, and flight lengths are introduced as auxiliary variables. The flight equation, specular reflection, incidence signs, and no-earlier-hit conditions are encoded by bounded-degree polynomial sign conditions. Minimizing squared distance along each candidate segment reduces the no-earlier-hit condition to finitely many endpoint/interior cases.

A word of length `O(L)` uses `O(L)` variables and bounded-degree tests; the label and membership alternatives are at most exponential in `L`. The finite sign-condition component bound then gives a safe complexity budget

\[
 \exp\{C L\log(2+L)\}.
\]

After fixing one input coordinate and a superlevel, projection of each connected lifted component is connected, so the number of interval components does not increase. One-dimensional coarea bounds the slice variation; integration over the other coordinate gives the two distributional first derivatives, including itinerary jumps.

This route is plausible and substantially more informative than a formal assertion that finite iterates preserve BV. I did not find a direct contradiction.

The most important specialist checks are:

- the exact polynomial encoding of the first admissible collision near tangencies and competing roots;
- uniqueness of the regular lifted fiber after all label alternatives are combined;
- the coefficient-uniform use of the sign-condition component bound in dimension growing with `L`;
- the superlevel projection and coarea passage at chart seams and singular conventions.

Even if correct, this lemma proves only first variation of bounded initial-coordinate functions. It gives no second-derivative estimate for inverse-coarea densities.

## 8. Audit of the exact tower lift and its regularization

The tower levels

\[
 D_{j,R}=T_R^j\{y\in Y_R^*:r_R^*(y)>j\}
\]

partition a full-measure set by invertibility and recurrence. The lifted function accumulates the centered collision phase from the most recent section visit.

At every nontop level the collision defect vanishes exactly. At a true top, the accumulated collision sum is the centered one-return record. This gives the stated norm and defect identities with the correct normalization. The top is counted once per return, not with the length-biased tower law.

The finite-age approximant is also correctly organized. On retained ages, smoothing the initial section function costs `L\epsilon V_f`; the omitted ages have exponentially small measure by the genuine return-tail theorem. The `L^2` error follows from the supremum bound. The level indicator is written as an exact product of section indicators along the finite backward record, so its jumps are included in the finite-record BV budget.

The logarithm of the approximant's BV norm is of order

\[
 L\log L+\log(1+\epsilon^{-1}),
\]

which leads to the extra `\log\log` factor in the return-function theorem. The proof chooses the approximation accuracy before applying the collision function bound and tracks its effect on the regularity budget. I found no circular choice in the printed argument.

## 9. What the annulus theorem closes—and what it does not

For a polynomial initial regularity budget, revision 16 proves one-step physical function-defect lower bounds on

\[
 2n^{-99/200}\le|z|\le n^{-2/5}.
\]

This is precisely the small-frequency annulus singled out in the revision-14 report. It is a significant closure at the level of physical functions.

It does **not** prove the complementary Fourier integral. Several further steps are indispensable.

### 9.1 No actual induced distribution-space operator

The paper has not constructed a strong/weak anisotropic family for the unbounded induced multiplier on which the necessary Lasota--Yorke, Fredholm, or quasi-compact estimates hold uniformly. The exact tower lift is a function identity, not such an operator construction.

### 9.2 No anisotropic-to-BV reconstruction

An approximate spectral vector in a distribution space is not automatically a bounded function, has no automatic nonzero modulus, and need not have a polynomial BV budget. The v15 and v16 theorems begin after these properties have been supplied.

A future reconstruction theorem must control normalization, supremum norm, BV norm, and physical defect with constants compatible with the annulus lower bound.

### 9.3 Only the unit centered spectral parameter on returns

The actual-return theorem excludes approximate solutions of

\[
 f\circ F_R^*=e^{iz\cdot(G_R-\bar G_R)}f.
\]

A resolvent estimate must generally exclude approximate solutions with an arbitrary unit spectral parameter. The present collision theorem has an arbitrary constant phase, but the printed tower lift does not transfer an arbitrary constant per return. The manuscript expressly leaves arbitrary induced eigenvalues open.

### 9.4 A one-step defect is not power decay

Even a lower bound for every normalized function in a selected class does not, by itself, imply decay of the physical characteristic function. One still needs an operator family, an invariant or recoverable class, and quantitative estimates converting the one-step defect into resolvent or power bounds.

### 9.5 The fixed compact bands remain quantitatively mismatched

At fixed radius, v15 permits a polynomially growing BV budget on a compact nonzero collision-frequency band. Uniformly over the radius, it proves separation only for a fixed budget. A parameter-uniform complementary integral with time-dependent reconstructed vectors requires these two forms of control to be reconciled.

### 9.6 Growing and far roof regimes remain

The near-origin theorem covers small four-dimensional physical frequencies. The compact-band theorem treats bounded nonzero collision frequencies. Neither gives the required estimates for growing roof frequencies or the far roof tail. The strict splice constants remain to be proved.

For these reasons, the main complementary-frequency blocker has been advanced but not closed.

## 10. Complete critical and singular branch extraction remains open

The finite-record variation theorem concerns bounded functions in initial collision coordinates. The raw inversion problem concerns densities obtained by pushing forward many-return branches through a map with critical values and singular boundaries.

The paper still needs a decomposition including:

- every regular critical word;
- central critical branches;
- grazing and competing-root boundaries;
- dynamically generated image boundaries;
- extraction of every nonintegrable jump;
- local control of the extracted density and its low-frequency convolution;
- summation of the second distributional derivative norms of the residual with their actual `n`-dependence.

The semialgebraic first-variation budget does not control inverse Jacobians, second derivatives of inverse-coarea densities, or the summability of their jumps. The manuscript correctly keeps these statements separate.

## 11. Weighted exact physical conditioning remains open

The inherited marked theorems control one function of one actual return state, with an exact unchanged denominator. The new tower lift begins with a specified section function and does not show that a multiple-time or exact physical observation indicator belongs to a controlled reconstruction class.

The final conditioning theorem still needs:

- weighted complementary-frequency power or integral estimates;
- weighted critical/singular edge extraction;
- local denominator lower bounds on the actual raw scale;
- a relative comparison between the completed-return event and the exact physical observation event.

The same-event central and moment results do not perform this replacement.

## 12. Top-four significance assessment

The revision sequence now contains a broad unconditional package for one physical Lorentz family:

- Gaussian and functional laws for the actual unbounded return record;
- growing integrated central bands;
- initial and single-marked insertions;
- unsmoothed fourth moments and actual covariance convergence;
- full joint covariance nondegeneracy;
- complete measurable physical phase arithmetic;
- fixed-band quantitative BV phase and function defects;
- uniform near-origin collision defects;
- exact tower localization and actual-return defect bounds on the intervening annulus.

This is mathematically substantial. The v15--v16 additions are not cosmetic and respond directly to the principal analytical gap identified in the v14 report.

At a top-four benchmark, however, the article still presents the raw mixed-density LLT as its organizing endpoint while leaving the operator-power conversion, full complementary integral, complete raw branch sum, and exact weighted-conditioning chain open. Alternatively, a top-four claim would require the compensation/phase/tower method to be formulated as a broad abstract theorem and demonstrated in several genuinely different hyperbolic systems. The present manuscript remains tied to one carefully engineered family.

I therefore do not regard revision 16 as meeting the closure and breadth threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 13. Required work before another top-four review

### A. Construct the actual induced operator and reconstruction theorem

Build a strong/weak anisotropic realization of the unbounded induced twists, or another framework with equivalent power control. Prove:

- uniform Lasota--Yorke/Fredholm estimates;
- normalization and nonvanishing information for approximate vectors;
- a quantitative map into the bounded-BV class;
- a defect comparison compatible with the v15--v16 budgets;
- control for every relevant unit spectral parameter, not only the centered eigenvalue one.

### B. Convert defects into the complete complementary integral

Starting at the actual central cutoff, prove an integrated estimate through:

- the intervening annulus;
- compact nonzero torus frequencies;
- growing roof frequencies;
- the far roof tail.

All constants must be uniform in the radius and compatible with the time-dependent regularity budgets. The splice must have a strictly nonempty verified parameter range.

### C. Complete the raw branch decomposition

Construct the full extracted edge measure and prove residual `L^1` integrability, second-derivative summation, and local edge conditions with the true return-count growth. Do not infer these estimates from the finite-record first-variation theorem.

### D. Complete the weighted exact-conditioning chain

Prove the complementary tails and edge estimates for the actual initial, terminal, path, and exact-event insertion classes used downstream. Establish the relative event-replacement estimate rather than changing the event implicitly.

### E. Obtain independent specialist review

At minimum, independent experts should check:

- the finite-cover ergodicity in the complete-phase proof;
- the product-measure/Radon--Nikodym truncation in the quantitative holonomy proof;
- the diffusive middle-block spectral word and endpoint smoothing;
- the semialgebraic first-collision graph and component bound;
- the tower top normalization and approximation budgets;
- the future anisotropic reconstruction and resolvent estimates;
- the complete raw coarea branch decomposition.

### F. Consider a specialist-paper reorganization

If the raw LLT is not completed, reorganize around the unconditional theorems. In that version, the raw LLT should be a separated future criterion rather than the apparent endpoint of the submitted article.

## 14. Presentation and technical comments

1. State immediately beside Theorem G that it controls the centered multiplier at spectral parameter one and not an arbitrary induced peripheral phase.
2. Use separate notation for the physical Fourier frequency, the collision constant phase, and the operator resolvent parameter.
3. Keep both annulus scales visible: `2n^{-99/200}\le|z|\le n^{-2/5}` and `2n^{1/200}\le|\sqrt n z|\le n^{1/10}`.
4. Keep the fixed-radius logarithmic estimate separate from the radius-uniform fixed-budget compactness theorem; neither implies the other with a growing budget.
5. In the finite-cover phase proof, retain the explicit physical geometry and connectedness statement.
6. In the finite-record lemma, identify the precise sign-condition theorem and distinguish a lifted graph bound from a projected density-derivative bound.
7. Display the exact tower top convention and the factors `c_*` in the norm and defect identities together.
8. Avoid describing the new theorem as a completed “phase reconstruction” without the anisotropic-to-BV map and arbitrary spectral phase.
9. Do not call a function-defect estimate a complementary Fourier-tail estimate.
10. Continue to distinguish first variation of initial-coordinate records from second variation of raw pushforward densities.
11. Retain the statement that the full lift is not presumed BV and that the finite-age approximation is only a proof device.
12. Beside every raw inversion statement, identify which frequency regions and weighted classes are proved rather than assumed.
13. The exact inherited-edit ledger and dynamic workflow receipt should remain part of source qualification.
14. Supporting publication metadata should continue to distinguish an author revision, a successful build, an external referee-style report, and formal proof certification.

## 15. Verification boundary

I reviewed the frozen v16 source, the v15 complete-phase and quantitative-defect modules, the v16 near-origin and actual-return modules, the controlling v14 report, the source manifest, proof ledger, response, input maps, branch and commit identities, and the actual GitHub Actions results at the reviewed SHA.

I did not independently reconstruct every inherited billiard singularity estimate, formally certify the Basu--Pollack--Roy component theorem, or prove the future anisotropic and raw coarea interfaces.

Finite diagnostics can check source hashes, exponent arithmetic, finite tower identities, and model sign calculations. They cannot prove the continuum product structure, semialgebraic projection/coarea bound, Banach-space spectral construction, full complementary integral, or global raw branch sum.

This recommendation is a mathematical and editorial referee assessment at the requested standard, not a formal proof certificate.

## 16. Final conclusion

Revisions 15 and 16 make credible and important progress. They upgrade qualitative phase rigidity to quantitative bounded-function defects, extend the analysis uniformly toward the origin, prove a quantitative finite-record variation theorem, and transfer the resulting obstruction to the actual unbounded return record on the full small-frequency annulus. I found no decisive counterexample in these new proof chains.

The exact source is properly qualified, and the new results materially strengthen the unconditional package.

Nevertheless, the advertised raw mixed-density LLT still lacks the induced operator/reconstruction and power estimates needed to convert those defects into the complete complementary Fourier integral. The complete critical/singular residual decomposition and the weighted exact-conditioning chain also remain open.

For those reasons I recommend rejection at the requested top-four benchmark in the present form, while recognizing revision 16 as a substantial mathematical advance and a potentially strong specialist contribution.