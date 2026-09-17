# Independent referee report on A2, revision 76

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Reviewed branch:** `revision/a2-v76-relative-envelope-2026-09-17`  
**Reviewed head:** `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`  
**Requested standard:** the level expected of the four leading general mathematics journals.

This is an author-requested, AI-assisted independent referee-style assessment. It is not a commissioned report from, or an editorial decision of, any journal. I have deliberately separated mathematical correctness, revision-specific defects, and the much higher question of general-journal significance.

## 1. Recommendation

**I do not recommend acceptance at the requested highest general-journal level in the present form.**

Revision 76 is materially stronger than revision 75. It repairs the principal-transition inconsistency identified in the preceding report, makes the conditioning costs more explicit, isolates a dimension-independent two-end determinant comparison, and introduces a phase-dependent actual-function envelope whose sufficient differentiability order depends on a geometric mean of phasewise contraction bounds rather than the worst phase. These are real improvements.

However, after examining the new mathematical material, I do **not** find that revision 76 changes the central editorial conclusion. The strongest theorem is still a highly marked local inverse theorem: phase-resolved endpoint laws at two prescribed offsets, around a supplied clear nongrazing periodic polygon with supplied contacts/frames and exact gate/itinerary information, determine the complete smooth contact germs; finite-preparation recovery is then obtained on bounded classes under substantial uniform priors. That theorem is technically substantial, and I have not found a fatal error in its core argument in this review. But the revision-specific additions are principally abstractions and quantitative refinements of mechanisms already needed by that theorem. They do not, in their current formulation, elevate the result to a broadly reusable theorem of sufficient independent conceptual reach for the requested placement.

My recommendation is therefore negative for **placement**, not a claim that the main theorem has been disproved.

## 2. Scope of this review

I treated revision 76 as a revision of the already audited v75 principal route rather than pretending to have formally reverified every theorem in the full technical catalogue. In particular I examined:

- the response to the v75 referee report;
- the revision-76 relative determinant abstraction in `article/10k_relative_decoupling_v76.tex`;
- the revision-76 phase-weighted smooth envelope in `article/10l_phase_weighted_envelope_v76.tex`;
- the integrated conditioning/budget discussion in `article/10m_conditioning_budget_v76.tex`;
- the active main thesis and its relation to the inherited v64--v70 argument;
- the previous v75 report, especially its checks of the relative cofactor/determinant argument, physical clock, two-offset extraction, quadratic inverse, signed jets, and actual-function envelope.

I did not treat compilation, preservation ledgers, source hashes, finite fixtures, or repository checkers as proof verification. They are useful integrity checks, not substitutes for mathematical reasoning.

## 3. What revision 76 genuinely improves

### 3.1 The previous narrative defect is repaired

The response identifies the stale principal transitions from v75 and replaces the relevant principal copies. The revised organization no longer advertises a nonexistent immediately preceding analytic theorem as the premise of the smooth route. This is a genuine editorial repair.

### 3.2 The conditioning discussion is substantially clearer

The new conditioning section correctly distinguishes several different losses that should not be conflated:

1. the smooth-envelope contraction threshold;
2. the inverse prefactor near that threshold;
3. the finite-jet and polynomial-alignment constants;
4. the two-offset denominator/density floors;
5. the rarity of accepted trajectories;
6. the finite-flight error and area sensitivity.

The explicit formulas for the scalar threshold

\[
 a^m<1/7
\]

and for a prescribed contraction margin make clear that the least admissible differentiability order can be numerically useless from a conditioning standpoint. This is an improvement over presenting a positive exponent as though it represented a practical or uniformly well-conditioned inverse.

### 3.3 The phase-weighted envelope is mathematically meaningful

The matrix-domination proposition is a clean way to state the nonlinear actual-function step. If

\[
 H\le \alpha_*^{-1}G+K_mH,
\]

with a nonnegative finite matrix `K_m` of spectral radius below one, then

\[
 H\le \alpha_*^{-1}(I-K_m)^{-1}G.
\]

For the cyclic phase model, the displayed weights satisfy

\[
 \widehat a_b^m w_{b+1}=\overline a^m w_b,
\qquad
 \overline a=(\prod_b\widehat a_b)^{1/r},
\]

so the geometric series indeed has spectral radius

\[
 \vartheta_m=\frac{6\overline a^m}{1-\overline a^m}.
\]

Importantly, the paper does **not** hide the cost of returning to the unweighted norm: it records

\[
 \kappa(w)=\frac{\max_b w_b}{\min_b w_b}.
\]

This matters because `\kappa(w)` can be large when the phasewise bounds are strongly heterogeneous. The revision's wording is appropriately limited: the geometric-mean criterion can improve a *sufficient order*, but it is not claimed to uniformly improve the unweighted condition number.

### 3.4 The two-end determinant proposition isolates the right cancellation

The revision observes that for

\[
 T=D+E,
\]

with `D` block diagonal and `E` block off diagonal,

\[
 \operatorname{tr}((I+D)^{-1}E)=0.
\]

The exact second-order identity

\[
 \log\det(I+D+E)-\log\det(I+D)
 =-\int_0^1(1-t)\operatorname{tr}(R(t)ER(t)E)\,dt
\]

therefore gives a dimension-free `O(||E||_2^2)` comparison under a uniform operator margin. The fixed-order parameter-derivative argument is also structurally sound: every differentiated term retains two Hilbert--Schmidt `E` factors, while the remaining factors are controlled in operator norm. I do not find a new determinant-class error in the finite-dimensional statement as written.

This is a useful extraction of the inherited mechanism.

## 4. Major concerns

### R76-M1. The revision-specific mathematics is mostly an abstraction/refinement of the existing proof, not a new theorem of comparable scope

This is the principal reason for my negative placement recommendation.

The determinant proposition packages the already used fact that a closed trace crossing between two separated ends must cross back. The phase-weighted envelope packages the already used actual-function contraction into a nonnegative matrix criterion and improves the sufficient order when the phase contractions are heterogeneous. Both are legitimate and reusable ideas. But in the manuscript they remain tightly tethered to the existing local inverse proof.

A top general-journal revision would need to make one of these mechanisms into a theorem whose mathematical content survives substantially beyond the billiard application. For example, the authors could formulate and prove an abstract inverse-rigidity principle for contracted nonlinear envelopes on a directed graph, including perturbations, stability, and a natural invariant criterion; or a genuinely infinite-dimensional relative determinant decoupling theorem with a class of applications not already encoded in the billiard proof. Revision 76 stops short of that. It extracts lemmas from the proof, but extraction is not the same as establishing broad independent significance.

### R76-M2. The phase-weighted refinement improves the differentiability threshold but can worsen the fixed-norm constant dramatically

The revision correctly acknowledges this, so it is **not** a hidden correctness flaw. It is nevertheless important for how the result is advertised.

The explicit weights obey

\[
 \frac{w_{b+1}}{w_b}=
 \left(\frac{\overline a}{\widehat a_b}\right)^m.
\]

Thus, when the `\widehat a_b` are heterogeneous, the condition number `\kappa(w)` may grow rapidly with `m`. The corollary only needs finiteness on a fixed bounded class, so the qualitative stability theorem survives. But the geometric-mean improvement should not be presented as an across-the-board improvement in conditioning or reconstruction difficulty. The new conditioning section mostly says this correctly. I recommend making the same limitation explicit wherever the phase-dependent criterion is first advertised, including the introduction and any abstract/conclusion language.

A particularly clean presentation would report the refinement as a tradeoff:

- lower sufficient derivative order from `\max_b \widehat a_b` to `\overline a`;
- potentially larger norm-equivalence constant `\kappa(w)`;
- unchanged dependence on the finite-jet inverse and class margins.

### R76-M3. The application of the abstract determinant proposition to the billiard operator remains too compressed at the new abstraction point

The proposition itself is clear. The application paragraph says that the Green/gluing estimates from the proof of the inherited periodic-relative theorem give the trace-norm deletion error, diagonal limits, Hilbert--Schmidt off-diagonal estimate, and operator margin. Given the detailed inherited proof examined at v75, I do not regard this as evidence of a fatal gap. But as a standalone reusable statement, the bridge is currently asserted in one paragraph rather than exposed as a corollary with explicit hypotheses and rates.

For the revision's claimed conceptual advance, this matters. The reader should not have to infer which inherited estimates provide:

- the uniform `C^k(S_1)` bounds on the diagonal blocks;
- the uniform `C^k(S_2)` bound on the off-diagonal coupling;
- the common `q<1` operator margin along `D+tE`;
- the rate after fixed parameter derivatives and polynomial-in-`N` losses;
- the trace-norm error introduced by deleting the middle and replacing finite end blocks by their half-line limits.

I recommend a concrete billiard corollary immediately after the abstract proposition, with the actual `N`-dependent rates and explicit citations to the lemmas supplying each hypothesis. That would materially strengthen the claim that the abstraction captures the proof rather than merely paraphrasing it.

### R76-M4. The new material is not yet integrated into the statement of the main conceptual theorem

The active main thesis still presents the smooth mechanism primarily through the scalar tail

\[
 6a^m/(1-a^m)<1.
\]

The phase-dependent criterion appears later as a refinement. This is mathematically harmless, and retaining the scalar theorem as a simple sufficient condition is sensible. But it weakens the editorial case that the revision has discovered a more general structural principle.

If the matrix envelope is intended to be one of the paper's conceptual contributions, the introduction should state that principle at the same level as the two-end determinant mechanism, explain exactly what is invariant under changes of phase decomposition, and distinguish the abstract spectral-radius condition from the special cyclic closed form. As written, the paper still reads primarily as a very elaborate solution of one marked inverse problem with two extracted technical devices.

### R76-M5. The finite-preparation theorem remains strongly conditional and should not be used to inflate the scope of the inverse result

The statistical theorem assumes a bounded class with fixed clearance, incidence, flight-length, residual, smoothness, density/gate, and area-type margins; exact itinerary and gate tags; independent normalized Liouville resets; and sufficiently small bounded post-acceptance recording error. The accepted events become exponentially rare with flight number, and the displayed rate incorporates that rarity.

This is mathematically legitimate. But it is not a general noisy dynamical inverse theorem and should not be rhetorically counted as an independent second breakthrough. It is a finite-sample consequence of the deterministic stability theorem under a carefully specified experimental design.

The revision has improved its honesty about these assumptions. I recommend preserving that restraint.

## 5. Correctness findings on the new material

### R76-C1. No fatal error found in the phase-weighted matrix calculation

The cyclic conjugation is correct. With

\[
 (A_m z)_b=\widehat a_b^m z_{b+1}
\]

and the displayed `w`, one has `A_mw=\overline a^m w`, including the closing phase. Hence

\[
 K_m=6A_m(I-A_m)^{-1}
\]

has Perron eigenvalue `6\overline a^m/(1-\overline a^m)`. The conversion back to the unweighted norm pays `\kappa(w)`, as it must.

### R76-C2. No fatal error found in the separated determinant identity

Under the stated finite-dimensional hypotheses and `||D+tE||<1`, the logarithmic power series is valid; the first variation at `t=0` vanishes by block parity; and the second variation is bounded by the square of the Hilbert--Schmidt norm without a dimension factor. The fixed-order derivative claim is consistent with the displayed resolvent differentiation.

### R76-C3. The conditioning corollary correctly cancels the rare scalar mass before normalization

For

\[
 w_N=c\,d_N\,\beta_Nr_N,
\]

the scalar `d_N` cancels exactly from the conditional law. The argument estimates the normalized `\beta_Nr_N`, rather than dividing an absolute approximation error by a vanishing rare-event probability. This is the right logical order.

### R76-C4. The new refinement does not repair or need to repair the old flat-function issue: that issue was already handled by the actual-function envelope

The paper continues to distinguish finite-jet identification from smooth-function identification. The latter uses an integrated envelope on actual functions, after finite-jet alignment. Revision 76 refines the tail domination; it does not revert to the invalid principle that equality of all Taylor coefficients alone determines a `C^\infty` function.

## 6. Significance relative to the requested general-journal standard

This is where the manuscript remains unconvincing.

The central theorem is an inverse-rigidity result with a sophisticated chain of exact identities and nonlinear estimates. Its strongest feature is the passage from a rare physical conditional law to complete smooth local contact germs without analyticity, using a relative twist/determinant normalization and an actual-function envelope. That is mathematically interesting.

But the observation model remains heavily marked and local. The inverse is supplied with the periodic polygon, contact phases/frames, exact itinerary/gate information, and a reset law; it recovers the visited contact germs, not a global unknown billiard table from standard scattering or spectral data. The later extensions and finite-record protocols add breadth inside the program but do not erase this distinction.

Revision 76 does not materially enlarge that theorem's data model or conclusion. Instead it:

- improves the sufficient smooth inverse order under heterogeneous phase contraction;
- clarifies quantitative conditioning;
- abstracts an existing two-end trace cancellation.

Those are good revision-level contributions, but they do not answer the significance objection raised in v75. At the requested level I would expect either a substantially more global rigidity theorem, a strikingly weaker/natural data model, or an abstract mechanism with consequences well beyond this billiard setting. I do not see that threshold crossed here.

## 7. Required changes before I would support renewed top-general-journal consideration

These are not all required for mathematical validity; they are what I would need for the **placement** judgment to change.

1. **Promote the reusable mechanism to a genuinely independent theorem.** The matrix envelope should be developed beyond the exact cyclic billiard tail, or the relative determinant principle beyond the finite-matrix wrapper, with nontrivial applications outside the present proof.
2. **Integrate the revision-specific principle into the main narrative.** The introduction should explain the spectral-radius criterion and its relationship to the scalar criterion, including the `\kappa(w)` tradeoff.
3. **Make the billiard instantiation of the determinant abstraction explicit.** State a corollary with the concrete end/middle decomposition and rates, and map every abstract hypothesis to an inherited estimate.
4. **Keep scope claims exact.** Do not turn supplied marks, exact tags, reset distribution, or bounded-class priors into conclusions.
5. **Strengthen the comparison with neighboring inverse-rigidity literature by mechanism, not only by data table.** The manuscript should explain what new obstruction is overcome that existing marked-length/scattering/spectral techniques cannot handle, and why that obstruction is of independent importance.
6. **If the authors want a top-general-journal case based on the present theorem rather than a broader abstraction, enlarge the theorem itself.** Examples would include substantially less marked data, a global reconstruction statement, or a natural observation model that removes one of the current exact-information interfaces.

## 8. Minor/editorial comments

1. The notation `D_N` is used in the determinant proposition for a block-diagonal operator, while `D_{N,b}` elsewhere denotes the scalar reference twist. The text warns the reader, but a different letter would reduce needless cognitive load.
2. The phrase "dimension-independent" is accurate for the determinant constant under the stated trace-ideal hypotheses, but it should not be read as saying the hypotheses themselves are automatic uniformly in dimension. The concrete corollary suggested above would make this distinction transparent.
3. The heterogeneous finite fixture is appropriately labelled non-geometric. Keep that qualification prominent; it demonstrates algebraic strictness of the sufficient-order comparison, not geometric realizability.
4. The conditioning section is useful enough that some of it belongs earlier. In particular, the distinction between minimum admissible order and a usable inverse margin should be visible before the finite-preparation theorem is advertised.
5. The manuscript should use one consistent phrase for "complete smooth contact germs" versus "complete real profiles on a collar" and remind the reader when the conclusion is local to the visited contacts.

## 9. Bottom line

Revision 76 is a serious, technically competent response to the previous review. The two new mathematical extractions are not cosmetic. I find the phase-weighted matrix calculation coherent, the determinant cancellation coherent under its stated hypotheses, and the conditioning discussion materially improved. I do **not** establish a fatal defect in the central physical-to-smooth inverse route.

Nevertheless, my recommendation at the requested Annals/Inventiones/Acta/JAMS-type level remains **negative**. The revision strengthens and clarifies the machinery of a highly marked local inverse theorem, but it does not yet demonstrate the breadth, conceptual independence, or enlargement of scope that would change the significance judgment. The most productive next step is not another layer of preservation/checking infrastructure. It is to turn one of the two extracted mechanisms into a theorem with genuinely wider mathematical reach, or to obtain a substantially stronger inverse result from materially weaker/natural data.
