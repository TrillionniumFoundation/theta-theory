# External top-four referee report on A2-DYN revision 13

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v13-referee-response-2026-10-06`, `revision/a2-dyn-v13-referee-copy-2026-10-06`  
**Reviewed commit:** `47d2430dc14c4d98a9e80db6fd573b049be8808c`  
**Reviewed repository tree:** `e0965fafd63731c4e2a5faaa7c1a0972cc626703`  
**Active manuscript directory:** `papers/A2-DYN-v13-referee-response`  
**Immediate qualified baseline:** revision 12 at `13b088e47bfbe8d46313b00bb97bc92a235a2376`  
**Controlling substantive report:** `reviews/a2-dyn-v11-substantive-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `fd84da57359a3ad2fefed532b0b5094ab8c6e436` / `73976d7df2e54353c97d3300c040a2f608df2b10`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 13 is a genuine mathematical revision and a materially stronger source packet than the revision-11 object reviewed in the controlling report. Revision 12 repaired the exact-source and TeX defects identified there and obtained a successful exact-SHA qualification. Revision 13 then adds two substantive mathematical modules:

- `core/30_unsmoothed_moments.tex`;
- `core/31_count_nondegeneracy.tex`.

The first proves finite-product decoupling for bounded-variation collision observables, fourth moments and maximal fourth moments for the unsmoothed collision sums, a fourth-moment return-clock window, an actual two-sided stopping comparison in `L^2`, convergence of the normalized covariance of the true return record, marked first and second moment estimates at any actual return, and a Cesaro form of the induced Green--Kubo formula. The second proves that the collision-count coordinate has strictly and uniformly positive Gaussian variance.

I found no decisive counterexample in these two new proof chains. The deterministic-gap smoothing argument does not estimate variation of long pullbacks; the ordered four-point summation gives the advertised `O(m^2)` fourth moment; the random stopping comparison uses the cumulative-return tail on exceptional events rather than pretending that a randomly stopped unbounded sum has a deterministic second-moment bound; and the count-nondegeneracy argument correctly converts a hypothetical scalar coboundary into a forbidden circle eigenfunction of the mixing collision map.

The new results close several points that were previously left open. In particular, `D_R` is now identified with the uniform limit of the actual normalized second moments, rather than only with the covariance of a weak Gaussian limit. The manuscript also proves nondegeneracy of one physically important coordinate and obtains same-event conditional moment statements for the marked insertion class.

The negative recommendation is therefore not based on a source failure, a version alias, or a detected fatal defect in the new theorems. It is based on the remaining mismatch between the organizing endpoint of the article and the unconditional conclusions currently established. The parameter-uniform four-dimensional raw mixed-density local limit theorem still requires:

1. uniform positive definiteness of the entire matrix `D_R`, not only positivity of its collision-count diagonal entry;
2. an integrated estimate on the full complementary-frequency region beyond the proved growing central ball;
3. a complete critical/singular raw branch decomposition with quantitative local-edge and derivative-sum bounds;
4. weighted complementary tails and relative event-replacement estimates for the exact physical conditioning application.

These are the mechanisms that turn the central Gaussian and moment theory into the raw density theorem advertised by the title and final synthesis. They are not routine presentation changes. At the requested benchmark, the article still lacks either the completed raw theorem or a comparably broad abstract principle with several substantial applications outside the one triangular Lorentz family.

The unconditional package is nevertheless mathematically substantial. After independent expert checking and a reorganization around the proved Gaussian, functional, growing-central-band, marked-insertion and moment theorems, it could form a strong specialist contribution. That assessment is distinct from the four-journal standard requested here.

## 2. Frozen source, chronology, and qualification

The two named revision-13 author branches resolve to the same commit:

`47d2430dc14c4d98a9e80db6fd573b049be8808c`.

The immediate parent revision 12 is

`13b088e47bfbe8d46313b00bb97bc92a235a2376`.

Revision 12 is the repaired source packet requested by the substantive v11 report. It corrected the split `\ref` source defect, repaired the malformed marked-event display, made the preservation claims match the actual tree, and bound the dynamic build receipt to the exact workflow run. GitHub Actions run `37399143352` completed successfully at that exact revision-12 SHA.

Revision 13 is ahead of this qualified source by two commits. The first adds the unsmoothed-moment and actual-covariance theorem; the second adds the count-direction nondegeneracy argument and updates the supporting records. The source manifest records twenty-eight inherited core files byte-identically, one explicitly documented deletion of a stray `+` after `\end{proof}` in `core/15_exponential_returns.tex`, and the two new core files. This is an accurate preservation statement rather than the blanket claim that failed at revision 11.

The exact-source workflow completed successfully on both reviewed revision-13 branches at the reviewed SHA:

- response branch run `37402522539`;
- referee-copy branch run `37402537171`.

For the response branch, every job step completed successfully, including exact checkout, source archive, native TeX installation, verification/build, and artifact upload. The qualification artifact is `11385627458`, named `a2-dyn-v13-47d2430dc14c4d98a9e80db6fd573b049be8808c`, with digest

`sha256:3e640c907341d098cbf1caee37c825ce1e5cb4ae34c0ac36619f373a0d8d891f`.

These facts cure the source-governance objection made against revision 11. They establish source identity, execution of the declared checks, and successful native typesetting. They do not certify the continuum billiard proofs.

The present review branch starts directly from the reviewed revision-13 author commit and adds only this report under

`reviews/a2-dyn-v13-external-top4-review-2026-10-06/`.

No manuscript source, author branch, workflow, earlier review, or unrelated repository path is modified.

## 3. What revision 13 actually proves

Let

\[
 h_R=f_R-\bar G_R\mathbf 1_{Y_R^*}
\]

be the bounded centered collision compensation and let

\[
 U_{n,R}=J_{n,R}-n\bar G_R
\]

be the centered record of `n` actual returns. Earlier revisions proved Gaussian and functional limits, a growing integrated central band, and a marked central transform at any actual return. Revision 13 adds the following unconditional conclusions.

### 3.1 Finite-product collision decoupling

For two to four bounded-variation collision observables evaluated at ordered collision times, the manuscript proves exponential factorization across any chosen deterministic gap. The proof smooths each factor at a scale selected from that gap, applies the existing collision spectral splitting only to the one power crossing the gap, and balances the smoothing and operator errors.

This is stronger than a two-point covariance estimate and is exactly the finite-order input needed for fourth moments and centered three-point insertions. It is not a new mixing theorem for the induced return map.

### 3.2 Unsmoothed fourth moments

For every centered bounded-variation collision observable `u`, and every deterministic collision interval of length `m`, the article proves

\[
 \mathbb E\left|\sum u\circ T_R^j\right|^4\le C m^2
\]

and the corresponding maximal fourth-moment bound. The estimates are uniform in the radius, in the deterministic location and orientation of the interval, and under bounded initial densities.

Applied to the section indicator and the collision compensation, these estimates provide fourth-moment return-clock windows and pathwise maximal control without smoothing the final observable.

### 3.3 Actual two-sided stopping

Recenter the physical orbit at an arbitrary marked return. The actual centered record is a two-sided collision sum over random backward and forward return clocks. The deterministic comparison uses the Kac-scale collision lengths on both sides of the mark.

The manuscript proves

\[
 \left\|\frac{Z_{n,k,R}-W_{n,k,R}}{\sqrt n}\right\|_2
 \le Cn^{-1/6}
\]

uniformly in the radius and the mark. It also improves the characteristic stopping error to

\[
 C M_a(1+|v|)n^{-2/9}.
\]

The proof separates the ordinary `L^2` comparison scale from the scale optimizing the characteristic error, which is mathematically appropriate.

### 3.4 Actual covariance and marked quadratic moments

For an insertion `a` evaluated at any actual return, the manuscript proves first and second moment estimates for the same physical record. In particular,

\[
 \sup_R\left\|
 \frac1n\int U_{n,R}\otimes U_{n,R}\,d\nu_R^*-D_R
 \right\|\le Cn^{-1/6}.
\]

Thus `D_R` is now the covariance limit of the actual normalized return record, not only the covariance in the characteristic-function limit.

The exact finite covariance identity also gives convergence of the induced Green--Kubo expression with Cesaro weights:

\[
 C^*_{0,R}+
 \sum_{j=1}^{n-1}\left(1-\frac jn\right)
 \left(C^*_{j,R}+(C^*_{j,R})^{\mathsf T}\right)
 \longrightarrow D_R.
\]

The manuscript correctly does not call this absolute convergence of the induced correlation series.

### 3.5 Same-event conditional moments

For the exact marked-state event already used in the marked central theorem, the article obtains conditional first and second moment bounds by inserting the same indicator and dividing by its unchanged probability. The conditional covariance converges under explicit probability and boundary-variation budgets.

This is a genuine strengthening of the same-event bridge. It does not compare two different rare events and does not replace an exact physical observation by a completed-return observation.

### 3.6 Uniformly positive collision-count variance

For the collision-count direction `e_3=(0,0,1,0)`, revision 13 proves

\[
 e_3^{\mathsf T}D_Re_3\ge d_N>0
\]

uniformly in the radius. The argument uses the established `L^2` coboundary characterization. If this variance vanished, then

\[
 1-c_*^{-1}\mathbf 1_{Y_R^*}=b-b\circ T_R
\]

for a real `b\in L^2`. Exponentiating with the factor `2\pi c_*` produces a unit-modulus eigenfunction

\[
 q\circ T_R=e^{-2\pi i c_*}q.
\]

Since `2\pi c_*=91/5000`, the eigenvalue is not one. Collision mixing forces the correlation of this mean-zero eigenfunction with itself at time `m` to tend to zero, whereas the eigenrelation makes that correlation have modulus one. This contradiction gives pointwise positivity; continuity of `D_R` and compactness of the radius interval give the uniform lower bound.

This is a clean and useful nondegeneracy result. It does not prove that every nonzero joint direction has positive variance.

## 4. Audit of the finite-product decoupling argument

The proof of Lemma `lem:bv-finite-product` avoids the main regularity trap. It never estimates the BV norm of `u_j\circ T_R^{t_j}`. Instead every factor is smoothed before it enters the collision transfer word. Telescoping changes the original and smoothed products by `O(\varepsilon)` using invariance and the uniform supremum bounds.

After translating the earliest time to zero, the joint expectation is represented as a chronological word of smooth multipliers and collision transfer powers. Replacing the one power across the selected gap by the rank-one projection exactly factors the smoothed expectation into the two desired blocks. The multiplier losses are polynomial in `\varepsilon^{-1}`, while the complementary power decays exponentially in the gap. Choosing

\[
 \varepsilon\asymp \vartheta^{d/(2q+1)}
\]

balances the two errors and yields exponential decoupling. Repeated times and a zero gap are covered by the bounded operator `I-\Pi_R`.

I found this proof coherent. Its imported ingredients remain the local collision spectral splitting, uniform power bounds, smooth multiplier estimate, and mean-preserving BV smoothing. Those are already load-bearing in the earlier Gaussian chain and remain appropriate targets for independent specialist verification.

## 5. Audit of the fourth-moment argument

The ordered four-point calculation is the core new combinatorial estimate. At collision times

\[
 0,\quad a,\quad a+b,\quad a+b+c,
\]

splitting at the middle gap gives the product of the two outer covariances plus an error exponentially small in `b`. Splitting off the first or last centered factor gives bounds exponentially small in `a` and `c`. Combining these estimates yields a connected remainder controlled by

\[
 Ce^{-\gamma\max\{a,b,c\}}.
\]

The covariance-pairing term sums to `O(m^2)`: the two outer gaps are exponentially summable, while the initial position and middle gap each contribute one linear factor. The connected remainder is summable over all three gaps and contributes only `O(m)`.

The maximal fourth moment is obtained by a dyadic prefix decomposition. At one scale, the fourth moment of the maximum is bounded by the sum over all dyadic blocks at that scale. Minkowski's inequality across scales gives an `L^4` norm of order `m^{1/2}`, hence a fourth moment of order `m^2`, without a logarithmic loss.

This calculation is internally consistent, including repeated times. It supplies the uniform integrability that was absent from the earlier weak-convergence proof.

## 6. Audit of the return-clock and stopping estimates

The fourth-moment clock window applies the unsmoothed maximal estimate to the centered section visit count. The exact equivalences between a return-clock event and a visit-count deviation yield

\[
 \nu_R^*\{|N_{j,R}^{\pm}-\lfloor j/c_*\rfloor|>b\}
 \le C\frac{(j+b)^2}{b^4}.
\]

The backward estimate uses invertibility and invariance rather than an unproved symmetry of the section.

For the actual marked sum, the cumulative-return exponential tail controls the total random collision length. On the event that this length is at most a fixed multiple of `n`, the sum is bounded by deterministic forward and backward maxima. On the complementary event, boundedness of the collision compensation and the exponential return tail control the fourth moment directly. No independence of the two clocks is invoked.

To compare the actual and deterministic two-sided sums, the proof uses a clock window of size `b`. Off the exceptional event, the difference lies in deterministic collision windows of length `O(b)`. On the exceptional event, Cauchy--Schwarz combines the `O(n^2)` fourth moments with the fourth-moment clock probability. This gives the normalized squared `L^2` error

\[
 C\left(\frac bn+\frac n{b^2}\right).
\]

The choice `b\asymp n^{2/3}` gives the claimed `L^2` rate `n^{-1/6}`. Optimizing the characteristic comparison separately at `b\asymp n^{5/9}` gives `n^{-2/9}`. These exponents are correct.

## 7. Audit of the marked moment and covariance identification

The deterministic quadratic insertion lemma centers the insertion and uses the finite-product estimate for two and three factors. The centered linear insertion is exponentially summable over one collision index. For the quadratic correction, ordering the three times `0,i,j` and splitting at either gap gives a bound exponentially small in the larger gap. This is summable over `(i,j)\in\mathbb Z^2`.

The unweighted deterministic interval covariance differs from its length times `\Gamma_R` by a bounded amount because the collision covariances have exponentially summable first moments. Consequently the insertion changes the linear or quadratic collision moment by at most a constant times `\|a\|_\infty+\|a\|_{\mathrm{BV}}`, independently of the interval location.

The actual marked theorem transfers this deterministic estimate through the `L^2` stopping comparison. For the quadratic term, the tensor inequality

\[
 \|z\otimes z-w\otimes w\|
 \le |z-w|(|z|+|w|)
\]

and Cauchy--Schwarz combine the stopping `L^2` rate with the fourth moments. The deterministic interval length is `n/c_*+O(1)`, uniformly in the mark, so division by `n` gives `D_R=\Gamma_R/c_*`.

This establishes the actual covariance limit with a quantitative rate. The resulting Cesaro induced Green--Kubo formula is an exact expansion of this second moment. It should continue to be described as Cesaro convergence; the article correctly does not infer absolute summability of the induced correlations.

## 8. Audit of count-coordinate nondegeneracy

The new count argument is short but conceptually important.

The collision spectral splitting gives mixing for smooth densities and tests. Approximation in `L^2` and invariance extend the correlation limit to arbitrary `L^2` functions. This extension is sufficient for the circle-valued function `q`, whose modulus is one.

Under the zero-variance hypothesis, the existing kernel theorem gives a real collision coboundary for

\[
 1-c_*^{-1}\eta_R.
\]

Because `\eta_R` is integer-valued, exponentiation cancels its contribution exactly and produces the eigenvalue `\lambda=e^{-2\pi i c_*}`. Invariance forces the mean of `q` to vanish because `\lambda\ne1`. Mixing then says

\[
 \int \overline q\,(q\circ T_R^m)\,d\nu\to0,
\]

while the eigenrelation makes the same integral equal to `\lambda^m`, a contradiction.

The proof therefore establishes strict positivity for each radius. Continuity of `D_R` and compactness give a uniform lower bound. The actual covariance convergence then transfers this lower bound to the finite-`n` collision-count variance for all sufficiently large `n`.

I found no logical defect in this argument. For readability, the final article should retain the explicit value `2\pi c_*=91/5000` and state once that `|q|=1`, since these two facts make the contradiction immediate.

## 9. What the count result does and does not close

The scalar count result removes one possible kernel direction and is stronger than merely showing that the count coordinate is not deterministic. It also confirms that the limiting count variance is the limit of the actual normalized variances.

It does **not** prove positive definiteness of the joint covariance. A hypothetical zero-variance direction may combine displacement, collision count, and flight time. The simple exponentiation argument works because the section indicator is integer-valued after multiplication by the specific count coefficient. For an arbitrary real joint direction, the collision contribution is not eliminated modulo an integer by the same scalar choice.

The manuscript therefore still needs either:

- a regularity theorem turning the `L^2` transfer function into an object evaluable on the explicit periodic orbits, so that the full periodic rank may be applied; or
- a different direct argument excluding every nonzero joint zero-variance direction uniformly in the radius.

Until then, the Gaussian matrix may be singular in directions not parallel to `e_3`, and the four-dimensional raw density theorem cannot use `D_R^{-1}` or `\det D_R` unconditionally.

## 10. Same-event conditional moments

The conditional moment corollary uses the same marked-state event in the numerator and denominator. Its insertion is the exact indicator of the event at the chosen return. Dividing the marked first and second moment bounds by the exact event probability yields the stated budgets.

The exponent conditions are consistent. The conditional second moment about the original center converges under the weaker condition, while convergence of the conditional covariance additionally requires the conditional mean to vanish. Subtracting the tensor square of that mean explains the stronger variation budget.

This remains a same-event result. It does not control a relative symmetric difference between an exact physical observation and a completed-return event. It also does not provide weighted complementary-frequency or edge estimates. The paper states these limitations accurately and they should remain visible in any future abstract or introduction.

## 11. Remaining blockers for the raw mixed-density LLT

### 11.1 Full uniform positive definiteness

The count direction is now uniformly nondegenerate, but the smallest eigenvalue of the full four-dimensional covariance is not controlled. The raw Gaussian density and the inversion corollaries still assume a uniform positive lower bound.

The earlier periodic geometry and rank calculations remain promising inputs, but an `L^2` transfer function cannot be evaluated on a prescribed measure-zero periodic orbit without an additional regularity or approximation theorem.

### 11.2 The full complementary-frequency integral

The proved central physical radius remains of order

\[
 n^{-1/2+1/200}=n^{-99/200}.
\]

The previously discussed outer regime begins farther away, around a scale such as `n^{-2/5}`. The intervening annulus is genuine. The manuscript still lacks one integrated estimate covering that annulus, compact nonzero torus frequencies, growing roof frequencies, and the far tail.

The improved stopping exponent affects one error term inside the central analysis. It is not a resolvent or contraction estimate for the transform throughout the complement.

### 11.3 Complete critical and singular branch extraction

The exact critical-edge calculation and individual jump subtraction are retained. The new fourth moments concern collision sums, not second distributional derivatives of many-return inverse-coarea densities.

The raw theorem still requires a decomposition including every regular critical word, central critical branch, grazing and competing-root singular boundary, and dynamically generated image boundary. All nonintegrable jumps must be extracted, and the remaining derivative norms must be summed with their actual return-count dependence.

### 11.4 Weighted raw tails and exact physical conditioning

The initial and single-marked central theorems cover a useful insertion class. The new moment results extend the same class at the level of first and second moments. They do not supply weighted complementary tails, weighted local edge estimates, multiple-time insertions, or the relative event-replacement estimate required for the exact physical conditioning theorem.

A conditional Gaussian moment statement is not a conditional raw local limit theorem.

## 12. Top-four significance assessment

The progression from revisions 9 through 13 is mathematically meaningful:

1. bounded collision compensation and actual Gaussian/functional limits;
2. a growing integrated central band;
3. one insertion at any actual return;
4. unsmoothed fourth moments and actual covariance convergence;
5. a direct scalar nondegeneracy theorem for collision count.

This is a coherent package, not a collection of unrelated calculations. The compensation-and-stopping architecture may have value beyond this example.

At the requested benchmark, however, the paper remains centered on a raw mixed-density theorem whose nondegeneracy, complementary-frequency and complete branch-summation mechanisms are not proved. Nor has the compensation/moment method yet been abstracted into a general theorem with multiple substantially different applications. The present family-specific package therefore does not, in my judgment, meet the closure and breadth expected by *Annals*, *Acta*, *Inventiones*, or *JAMS*.

For a strong specialist journal, the assessment is more favorable. A reorganized manuscript with the unconditional Gaussian, functional, growing-band, marked and moment theorems as its main endpoint could be compelling, provided the collision-space imports and new continuum arguments receive independent expert scrutiny.

## 13. Required work before another top-four review

### A. Prove full covariance nondegeneracy

Close every possible joint zero-variance direction, uniformly in the radius. The theorem must cover the discontinuous section contribution. Scalar count positivity alone is insufficient.

### B. Close the complete complementary-frequency region

Provide an integrated estimate from the boundary of the proved central ball through the intermediate annulus, compact nonzero frequencies, growing roof frequencies, and far roof-frequency tail. State actual constants and verify a nonempty splice range.

### C. Complete the raw branch decomposition

Construct the full extracted edge measure, including singular itinerary boundaries, and prove the residual integrability and local-edge estimates with their true `n`-dependence.

### D. Complete the weighted conditioning application

Prove weighted complementary tails and edge estimates for the actual terminal or path indicators, together with a relative event-replacement theorem for the exact physical observation.

### E. Obtain independent specialist review

At minimum, experts in dispersing billiards and anisotropic transfer operators should check:

- the Demers--Zhang common-space and multiplier import;
- the semialgebraic collision partition near grazing, tangency, and competing roots;
- the bounded collision covariance and smooth perturbation chain;
- the marked two-sided spectral product;
- the new finite-product BV decoupling and unsmoothed fourth moments;
- the eventual full cohomology/nondegeneracy bridge;
- the complete raw critical/singular branch sum.

## 14. Presentation and technical comments

1. The abstract now says that the collision-count variance is uniformly positive. It should immediately add that full positive definiteness of `D_R` is not proved, so that this sentence cannot be read as closing the joint nondegeneracy problem.
2. Keep `D_R` described as positive semidefinite in every theorem that does not assume more. Reserve `d_N` for the scalar count lower bound.
3. In the count proof, retain the explicit relation `2\pi c_*=91/5000` and state `|q|=1` before invoking mixing.
4. The `L^2` extension of mixing from smooth densities and tests is standard but load-bearing. A one-line approximation inequality for both factors would make the proof self-contained at that point.
5. Keep the actual covariance rate and the characteristic stopping rate separate. They arise from different optimizing choices of the clock window.
6. Do not describe the induced Cesaro formula as convergence of the induced Green--Kubo series without the word “Cesaro.”
7. State consistently whether an insertion is integrated against `\nu|_{Y_R^*}` or the normalized section probability. The current Theorems C and D do this correctly.
8. Preserve the distinction among a return-state event, a terminal return-state insertion, a multiple-time path event, and an exact physical observation.
9. The source manifest's one-character repair is correctly explicit. Future preservation claims should keep that exact accounting rather than revert to a blanket byte-identity statement.
10. The publication-status record is appropriately modest and should remain so: successful CI is execution evidence, not proof certification or journal acceptance.

## 15. Verification boundary

I reviewed the exact branch and commit identities, the controlling substantive report, the repaired revision-12 chronology, the revision-13 source manifest and validation records, the actual GitHub Actions outcomes, the new unsmoothed-moment and count-nondegeneracy source, and the way those results enter the full article.

I did not independently reconstruct every inherited billiard singularity estimate, reproduce the full anisotropic-space construction from first principles, or formally certify every theorem in the historical manuscript. The exact diagnostics verify source hashes, finite algebra, exponent identities, finite models and native typesetting. They cannot prove continuum collision regularity, full covariance positivity, a high-frequency resolvent, or the global coarea branch sum.

The recommendation is therefore an editorial and mathematical referee assessment at the requested standard, not a formal proof certificate.

## 16. Final conclusion

Revision 13 repairs the source-qualification failure identified at revision 11 and makes a real mathematical advance. It proves unsmoothed fourth moments, controls the actual two-sided stopping in `L^2`, identifies the covariance through the actual normalized second moments, establishes marked quadratic laws and same-event conditional moments, and proves uniform nondegeneracy of the collision-count coordinate. I found no decisive counterexample in these new arguments.

The result is nevertheless not a completed four-dimensional raw mixed-density local limit theorem. Full joint nondegeneracy, the complete complementary-frequency integral, the all-branch critical/singular residual estimate, and the exact weighted conditioning chain remain open within the manuscript. At the requested top-four benchmark I therefore recommend rejection in the present form, while recognizing the unconditional package as a potentially strong specialist-journal contribution after independent expert review and appropriate reorganization.
