# External top-four referee report on A2-DYN revision 19

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v19-referee-response-2026-10-06`, `revision/a2-dyn-v19-referee-copy-2026-10-06`  
**Reviewed commit:** `e56eed31c3b7d70ceb71a7f4b075092c2bd3e98d`  
**Reviewed repository tree:** `e65347f8fd1b6b5fb8765531e782ef0a6915c02d`  
**Frozen ordinary paper tree:** `57ea4229c9e344f9d61fd08be6ef7f7954d29feb`  
**Active manuscript directory:** `papers/A2-DYN-v19-referee-response`  
**Substantive v19 parent commit:** `8373ea3d36e9b6db944e6905989e18cdef333b10`  
**Frozen v18 ordinary-source baseline:** `68618cdaad6824912b49b505d58c9a9fcb0ab823`  
**Latest located substantive report:** `reviews/a2-dyn-v16-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `b0b7ddfcd90f493e02254742b33174e9108fc5a7` / `805f04cd60d144bc6321ce3f4304ebe1cda34999`  
**Date:** 6 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revisions 17, 18 and 19 contain several genuine and technically substantial advances. They do not merely rename the function-defect theorem reviewed in revision 16. In particular, the manuscript now provides:

1. an exact lift of an arbitrary peripheral phase per actual return to a collision phase, including the pure return-spectral direction and the shifted-frequency cancellation line;
2. quantitative lower bounds for physical defects in the joint physical/return-spectral parameters;
3. finite-rank orthogonal compressions of the actual unbounded return Koopman operator, with a proved reconstruction class, an exact residual comparison, local peripheral resolvent bounds, and a finite-time comparison with the unmodified characteristic function;
4. a complete structural extraction of all singularities of every fixed finite-count raw density into finite power--logarithm jets, leaving a `W^{2,1}` residual;
5. an exact count-localized inversion identity for the original unmodified law on central windows, including the high-count convolution correction rather than silently discarding it;
6. an exponential finite-record variation budget and a single-logarithm return-defect estimate;
7. central Gaussian and actual first/second moment laws under the unchanged joint observation of logarithmically many genuine returns.

I found no decisive counterexample in the six new mathematical modules audited for this report:

- `core/38_peripheral_return_phases.tex`;
- `core/39_compressed_return_resolvents.tex`;
- `core/40_finite_count_edge_extraction.tex`;
- `core/41_count_localized_raw_inversion.tex`;
- `core/42_exponential_reconstruction.tex`;
- `core/43_logarithmic_return_windows.tex`.

The exact peripheral lift has the correct top-versus-height normalizations. The compression residual identity is an orthogonal decomposition and does not assume normality. The fixed-count extraction includes singular itinerary and image-boundary effects through the full integration domain. The count-localized identity keeps the original law and the omitted high-count measure. The binomial component estimate genuinely improves the finite-record budget from `exp(C L log L)` to `C exp(C L)`. The logarithmic-window theorem approximates the whole observation product rather than assuming a bounded variation norm for a long pullback, and its final event and denominator are unchanged.

These are meaningful advances. They close the peripheral-phase omission identified in the revision-16 report, replace an individual-edge picture by a complete fixed-count structural extraction, and enlarge the proved central and moment theory to a nontrivial multiple-time class.

The negative recommendation is not based on source aliasing, absence of progress, or a detected fatal flaw in those new theorems. It is based on the continued gap between the organizing endpoint of the manuscript and the unconditional conclusions actually proved. The parameter-uniform raw mixed-density local limit theorem still requires, at minimum:

- an actual long-time decay estimate for the uncompressed twisted return dynamics, and hence an integrated complementary-frequency estimate;
- uniform quantitative control of the finite-count `W^{2,1}` derivative budget and the local extracted-edge correction when the return count and collision cutoff grow linearly with `n`;
- the weighted versions of those estimates for the conditioning classes used downstream;
- a relative comparison between the completed-return event and the exact physical observation event.

Moreover, the estimates currently used to connect the finite-rank compression to the physical characteristic function have a concrete scale incompatibility on the target annulus. The local compressed resolvent and the finite-time consistency theorem are individually credible, but their presently displayed constants cannot be chosen simultaneously to produce the required annular power bound. This is not a contradiction between the two theorems. It is a proof that the current interface between them does not yet close the complementary-frequency argument.

At the requested benchmark, an article organized around the raw local limit theorem must prove these mechanisms rather than leave them as exposed error terms or future reconciliation steps. The unconditional package may support a strong specialist paper after independent expert review and a reorganization around the theorems that are complete. That is a different editorial standard from the one requested here.

## 2. Frozen source and chronology

The two named revision-19 author branches resolve to the same commit:

`e56eed31c3b7d70ceb71a7f4b075092c2bd3e98d`.

The final v19 commit changes only the qualification runner selector from the ARM pool to the x64 `ubuntu-24.04` pool. The manuscript subtree is unchanged from its substantive parent

`8373ea3d36e9b6db944e6905989e18cdef333b10`.

The latter commit adds the v19 mathematics and freezes the ordinary paper tree

`57ea4229c9e344f9d61fd08be6ef7f7954d29feb`.

There is no separately located substantive referee report on revisions 17 or 18 in the branch history inspected for this review. I therefore reviewed the mathematical additions of revisions 17--19 together rather than treating the v17 and v18 modules as previously accepted.

The chronology relevant to the mathematics is as follows.

### 2.1 Revision 17

Revision 17 adds:

- `core/38_peripheral_return_phases.tex`;
- `core/39_compressed_return_resolvents.tex`.

It treats the return spectral phase `xi` separately from the physical Fourier variable `z`, constructs the exact lift for every `xi`, proves a joint near-origin function-defect theorem, and introduces fitted finite-rank compressions of the actual twisted return Koopman operator.

### 2.2 Revision 18

The v18 ordinary source, frozen in the v19 baseline, adds:

- `core/40_finite_count_edge_extraction.tex`;
- `core/41_count_localized_raw_inversion.tex`.

The historical v18 branch itself still names an assembly-stage commit, but the immutable ordinary paper subtree was created and then pinned without rewriting the old branch. The v19 source manifest uses the ordinary v18 baseline at

`68618cdaad6824912b49b505d58c9a9fcb0ab823`.

The v18 modules integrate the complete finite physical graph below a collision-count cutoff, extract every one-dimensional power--logarithm singularity whose second derivative would fail to be integrable, and insert that exact finite extraction into a central-window identity for the original law.

### 2.3 Revision 19

Revision 19 preserves all forty-one inherited core modules and adds:

- `core/42_exponential_reconstruction.tex`;
- `core/43_logarithmic_return_windows.tex`.

It sharpens the finite-record variation budget, improves the return spectral defect and compressed resolvent constants, improves the finite-time compression comparison, and proves central and moment theorems for several observations in a logarithmically growing actual-return window.

The source manifest correctly records that the following are still not proved:

- uncompressed power decay;
- a uniform long-time raw derivative bound;
- the full raw local limit theorem.

The present review branch starts directly from the reviewed v19 author commit and adds only this report under

`reviews/a2-dyn-v19-external-top4-review-2026-10-06/`.

No manuscript source, author branch, workflow, earlier review, or unrelated repository path is modified.

## 3. Exact-source qualification status

The v19 static validation record correctly says that a future workflow result must not be predeclared successful. At the time this report was frozen, the two exact-SHA x64 qualification runs were still queued:

- response branch run `37455890344`;
- referee-copy branch run `37455903106`.

They had no conclusion and no run-bound qualification artifact at the review freeze. The preceding ARM attempts had likewise remained queued without assigned runners, which is why the final v19 commit changed only the runner selector.

Accordingly, I do not represent the exact v19 SHA as remotely qualified in this report. This is not a failed mathematical or source check: no failing job result was observed. It is an incomplete execution record. A later successful exact-SHA run would establish that the declared finite checks and native build executed on the frozen source. It would not alter the mathematical assessment below or certify the continuum proofs.

The source chronology and exact paper bytes are nevertheless sufficiently explicit to identify the object under review. The report is based on the committed ordinary source, the frozen paper tree, the source manifest, the proof ledger, the response to the previous referee, and the new mathematical modules themselves.

## 4. What revisions 17--19 actually prove

The inherited paper already proves Gaussian and functional limits for the actual return record, growing central Fourier integrals, marked insertions, actual fourth moments and covariance convergence, uniform joint covariance nondegeneracy, complete measurable collision-phase arithmetic, and quantitative function defects on collision and return spaces.

The new revisions extend that package in three directions.

### 4.1 Peripheral return phases and local finite-rank resolvents

For

\[
 \mathcal E_{R,z,\xi}f
   =f\circ F_R^*-e^{i(\xi+z\cdot g_R)}f,
 \qquad g_R=G_R-\bar G_R,
\]

revision 17 constructs an exact collision-tower lift for every real return phase `xi`. The physical frequency is shifted according to

\[
 \sigma=c_*\xi,
 \qquad
 w=z-\sigma e_3,
\]

and the exact identity

\[
 \sigma+w\cdot h_R=z\cdot h_R+\xi\eta_R
\]

turns the constant phase per return into the correct collision phase plus the section indicator.

The resulting defect is localized at true tower tops and equals the actual return defect. The lift norm remains return-time weighted, while the defect norm is integrated once per top. These two normalizations are not interchanged.

The joint theorem includes:

- `z=0`, `xi != 0`;
- the shifted-frequency line on which `w=0`;
- complex functions with zeros;
- polynomial and certain subexponential regularity budgets on the physical annulus.

The theorem is local in the joint parameter

\[
 \rho=(|z|^2+\xi^2)^{1/2}.
\]

It is not a full-circle peripheral estimate.

### 4.2 Complete fixed-count raw extraction

For every fixed return count `n`, collision cutoff `L`, radius `R`, and admissible bounded finite-record subanalytic weight, revision 18 proves that the restricted actual law has a compactly supported mixed density.

Its one-dimensional time components are constructible. Every singular germ is represented by finitely many rational powers and logarithmic powers. The extraction removes all nonzero terms

\[
 x^\alpha(\log x)^k,
 \qquad -1<\alpha\le1,
\]

with suitable one-sided cutoffs. Constants and slopes are included because their zero extensions produce distributional boundary terms even when their classical second derivatives vanish.

The residual belongs to `W^{2,1}` in each lattice component. Consequently its mixed Fourier transform is integrable and has a proved far-roof tail bounded by the actual finite second-derivative sum.

This extraction concerns the entire finite-count density, not only the previously retained regular Morse edge. Singular itinerary boundaries, competing roots, grazing boundaries, and image-boundary effects enter through the full finite integration graph.

### 4.3 Logarithmic observation windows

Revision 19 treats a product

\[
 W_R(y)=\prod_{j=1}^{q}u_j((F_R^*)^{\ell_j}y)
\]

with distinct observations in a window of at most `a log n` genuine returns. The product itself need not have a usable variation norm.

The proof smooths the individual initial-coordinate factors, restricts only the proof approximation to a finite collision-count event, resolves binary section-membership words, and proves a bounded-variation budget for the whole approximating weight. It then removes the approximation in the original measure.

The final conditional event is exactly

\[
 A_{n,k,R}
 =\bigcap_j\{x:(F_R^*)^{k+\ell_j}x\in E_j\}.
\]

No collision-count cutoff is inserted into this final event, and its probability is not factored into individual masses.

The article proves:

- an integrated central Gaussian comparison on a positive polynomially growing rescaled band;
- conditional central Gaussian convergence for polynomially rare unchanged events under explicit strict margins;
- convergence of the actual conditional normalized mean and covariance;
- an exact weighted raw inversion identity when the observation class also satisfies the finite-record subanalytic hypothesis.

This is a substantial extension of the single-mark theory, but it is not a weighted conditional raw local limit theorem.

## 5. Audit of the peripheral phase lift

The principal identity of revision 17 is correct and important.

Recall that the collision-count coordinate of the bounded compensation is

\[
 h_{R,3}=1-c_*^{-1}\eta_R.
\]

With

\[
 b_{R,\xi}=\eta_R+e^{i\xi}(1-\eta_R),
 \qquad
 \sigma=c_*\xi,
 \qquad
 w=z-\sigma e_3,
\]

the exact real identity

\[
 \sigma+w\cdot h_R=z\cdot h_R+\xi\eta_R
\]

holds before exponentiation.

On an actual return tower starting at the section, the section indicator appears once from the initial level through the top. The multiplier `b_{R,xi}` therefore inserts precisely one factor `e^{i xi}` per completed return. At every nontop level the collision equation is exact. At the top the defect is exactly

\[
 f(F_R^*y)-e^{i(\xi+z\cdot g_R(y))}f(y).
\]

The case of return time one is included because the initial level is then already the top. I found no endpoint or sign error in this construction.

The frequency map

\[
 (z,\xi)\longmapsto(w,\sigma)
\]

is a fixed invertible linear map near the origin. Thus the pure return-spectral direction and the cancellation line `w=0` are genuinely covered. The proof does not divide by the shifted physical frequency.

The quadratic endpoint improvement is also coherent. Removing a phase over a short untwisted end block costs

\[
 |w|\,\|S_\ell h_R\|_2=O(|w|\sqrt\ell),
\]

rather than `O(|w| ell)`, because the compensation is centered and has summable collision covariances. No independence of the two end blocks is used.

The constant-phase alternative treats the region in which the collision constant phase dominates `|w|^2`. Choosing a deterministic time with cosine at most `-3/4`, after the mixing threshold, and comparing the characteristic integral with one by the second moment gives a quadratic lower bound. This includes the pure constant-phase case `w=0`.

The modulus argument for general complex functions follows the established pattern: approximate invariance makes the modulus almost constant, a controlled coarea truncation produces a circle phase, and the circle defect is transferred back. No pointwise lower modulus or selected measurable logarithm is assumed.

I found no decisive defect in this proof chain.

## 6. Audit of the finite-rank compression

The fitted grid on the five section rectangles gives a finite-dimensional piecewise-constant space `V_{R,h}` satisfying

\[
 \dim V_{R,h}=O(h^{-2}),
 \qquad
 \|f\|_\infty+\|f^0\|_{\mathrm{BV}}
      \le Ch^{-1}\|f\|_2.
\]

The scaling is consistent with cell mass of order `h^2`, total internal edge length of order `h^{-1}`, and Cauchy--Schwarz over the cells.

The actual twisted Koopman operator

\[
 \mathcal U_{R,z}f=e^{-iz\cdot g_R}f\circ F_R^*
\]

is unitary on `L^2`. Its compression

\[
 A_{R,h,z}=P_{R,h}\mathcal U_{R,z}|_{V_{R,h}}
\]

is a contraction. The matrix entries integrate the full unbounded return record; they are not obtained from truncated return blocks or an independent Markov model.

The residual comparison is an exact orthogonal decomposition. If `P f=f`, `|lambda|=1`, and `A=P U`, then

\[
 \|(U-\lambda)f\|^2
 =\|(A-\lambda)f\|^2+1-\|Af\|^2.
\]

An approximate compressed eigenvector therefore gives an approximate physical vector. Since `A` need not be normal, controlling the smallest singular value rather than only its eigenvalues is the correct approach.

Combining the reconstruction budget with the joint return defect yields the local finite-matrix resolvent estimate

\[
 \|(e^{i\xi}-A_{R,h,z})^{-1}\|
 \le C\frac{\Lambda_h^2}{\rho^4},
 \qquad
 \Lambda_h=1+\log(H_h/\rho),
 \quad H_h=C/h,
\]

under

\[
 \rho^2\Lambda_h\le a.
\]

The radial extension and neighboring resolvent disk follow from the singular-value bound and the triangle inequality. No normality assumption is used.

The finite-time comparison with the actual characteristic function is likewise an exact projection telescope. The count cutoff occurs only in estimating the projection error; neither the matrix entries nor the final characteristic function are replaced.

These are valid and useful finite-dimensional conclusions. They do not yet provide an uncompressed spectral gap, a mesh-uniform contour estimate, or a power bound for the actual return dynamics.

## 7. A concrete scale incompatibility in the current compressed route

The manuscript correctly says that the consistency and resolvent scales must still be reconciled. The present estimates show that this is a substantive obstruction, not an omitted line of bookkeeping.

The improved finite-time consistency theorem gives

\[
 \left|
 \mathbb E e^{-iz\cdot U_{n,R}}
 -\langle1,A_{R,h,z}^n1\rangle
 \right|
 \le Cn\left\{
 e^{(a_{\mathrm t}n-c_{\mathrm t}L)/2}
 +\sqrt{h(1+|z|)e^{CL}}
 \right\},
 \qquad L\ge n.
\]

To make the grid term tend to zero at time `n`, one needs at least

\[
 h e^{CL}=o(n^{-2}),
\]

and therefore

\[
 \log(1/h)\ge CL+2\log n+o(1).
\]

Since `L>=n`, the reconstructed regularity budget satisfies

\[
 \Lambda_h
 =1+\log(C/(h\rho))
 \ge c n
\]

for some positive constant along any such consistency scale.

But the local compressed resolvent theorem requires

\[
 \rho^2\Lambda_h\le a.
\]

On the target physical annulus, even at its smallest radius,

\[
 \rho\ge |z|\ge2n^{-99/200},
\]

so the two requirements imply

\[
 \rho^2\Lambda_h
 \ge c n^{-198/200}n
 =c n^{1/100},
\]

which diverges. At the upper annulus endpoint `rho=n^{-2/5}` the conflict is stronger.

Thus there is no common choice of the presently displayed `h` and `L` that simultaneously:

1. makes the finite-time compression error vanish at time `n`; and
2. stays inside the local compressed-resolvent domain throughout the annulus.

This calculation does not refute either theorem separately. It shows that the current finite-rank route cannot yet be concatenated into the annular power estimate required for the complementary Fourier integral.

A successful continuation must change at least one side of this interface. Possible routes include:

- a consistency theorem whose regularity cost is substantially smaller than `e^{CL}` on time scale `n`;
- a resolvent/reconstruction theorem allowing regularity budgets with logarithm comparable to `n` at the annular frequencies;
- a genuine anisotropic operator construction in which the long-time dynamics is controlled without approximating every time-`j` phase by a fitted BV grid;
- a different direct characteristic-function argument that bypasses this compression interface.

Until such a change is proved, the local compressed resolvent is a rigorous finite-dimensional approximation theorem, not a proof of complementary-frequency power decay.

## 8. Audit of the complete finite-count extraction

Revision 18 materially improves the raw-density side of the paper.

At fixed `(n,L,R)`, the physical collision graph has finitely many disk-label words and finite rational angular charts. The graph encodes:

- actual first admissible entries rather than arbitrary roots;
- specular reflection;
- exclusion of earlier hits;
- section membership at every collision;
- exact return count and lattice displacement;
- the total flight time.

Consequently the cumulative time distribution of each lattice component is an integral of a globally subanalytic integrand over a globally subanalytic family. The cited Cluckers--Miller stability theorem supports the constructible conclusion for this fixed finite-dimensional problem.

The article separately invokes the inherited regular-word coarea result to establish absolute continuity. It does not attempt to extend an inverse Jacobian smoothly through every singular boundary. This separation is appropriate.

The one-variable constructible preparation is then used to produce convergent one-sided Puiseux--logarithm germs. Integrability removes exponents at most `-1`. Subtracting every remaining exponent at most one removes:

- divergent classical second derivatives;
- jumps in the first derivative;
- value and slope boundary distributions created by zero extension.

The residual has matching zero value and first derivative at the prepared singular points and belongs to `W^{2,1}`. The Fourier bounds

\[
 |\widehat r(b)|\le
 \min\{\|r\|_1,|b|^{-2}\|r''\|_1\}
\]

then imply mixed Fourier integrability and the stated far-roof tail.

I found the logic of this extraction coherent. In particular, the manuscript does not claim that only Morse jumps occur and explicitly permits fractional powers and logarithms from singular boundaries.

Two points deserve independent specialist verification:

1. the passage from the cited constructible preparation theorem to the exact convergent Laurent--Puiseux--logarithm representation used for two differentiations;
2. the complete semialgebraic/subanalytic encoding of every first-hit and section-boundary alternative in the full finite collision graph.

These are verification requests, not detected contradictions.

The decisive limitation is quantitative. The preparation constants, cutoff widths, singular-value separations, number of germs, jet coefficients, and regular-interval derivative integrals may all deteriorate with `n`, `L`, and `R`. The theorem proves

\[
 A_2(n,L,R,w)<\infty
\]

for each fixed packet. It does not prove a uniform long-time growth bound usable when `L` is proportional to `n`.

## 9. Audit of the count-localized inversion identity

Using the collision count as an observed lattice coordinate is a useful structural idea.

For a label whose count coordinate is at most `L`, the original density and the finite-count density agree exactly. With

\[
 L_n=\lceil\lambda n\rceil,
 \qquad \lambda>c_*^{-1}+1,
\]

every fixed central window lies in those fibers for large `n`.

The exact finite-count extraction and the localized Fourier kernel give

\[
 p_{n,R}
 =K_n*\mu_{n,R}
 +(e^{L_n}_{n,R}-K_n*E^{L_n}_{n,R})
 +\mathcal F^{-1}[(1-\chi_n)\widehat Q^{L_n}_{n,R}]
 -K_n*\mathsf T^{L_n}_{n,R}
\]

on the central window.

Every term is retained. The last term is the high-count measure convolved with the proof kernel. Its normalized contribution on central labels is smaller than every power because the count support is separated by a distance proportional to `n` and the kernel is Schwartz. This does not assert a pointwise density bound for the high-count law or decay of its physical Fourier transform.

The resulting raw error budget correctly exposes the remaining three terms:

1. the local extracted-edge correction;
2. the finite-band complementary residual integral;
3. the far-roof term involving the actual finite-count second-derivative sum.

The central Gaussian term and limiting Gaussian tail are already controlled. The count correction is controlled. The raw local limit is therefore reduced to sharply identified quantitative estimates rather than proved.

This is substantial structural progress. It also makes clear why the paper remains incomplete: finiteness of the extracted packet at every `n` does not imply that the normalized three exposed terms tend to zero uniformly in the radius.

## 10. Audit of exponential finite-record reconstruction

The sharpening from `exp(C L log L)` to `C exp(C L)` is justified by the finite binomial component bound actually used.

If the lifted graph has `k=O(L)` variables and `s=O(L)` sign tests of bounded degree, then

\[
 d(2d-1)^{k-1}
 \sum_{j=0}^{k}\binom{s}{j}4^j
 \le d(2d-1)^{k-1}5^s
 \le Ce^{CL}.
\]

The exponentially many discrete label alternatives can be absorbed into the same form. Projection cannot increase the number of connected pieces beyond the number of projected connected components. Fixing a coordinate and adjoining a superlevel test preserves linear complexity.

The subsequent slice-coarea argument gives exponential first variation for bounded finite records and binary membership words. This is first variation in initial collision coordinates, not a second-derivative estimate for pushforward densities.

The improved tower regularization consequently has BV budget

\[
 CM_f e^{CL}(1+\epsilon^{-1}+|z|)
\]

with the same approximation error. Taking logarithms removes the previous additional `log log` factor. The single-logarithm joint return theorem and improved compressed resolvent therefore follow by the same controlled modulus and orthogonal-residual arguments.

The accuracy parameter is chosen before the smallness constants, and the absorption uses

\[
 \epsilon_0(1+|\log\epsilon_0|)\to0.
\]

I found no circular dependence in this choice.

A specialist should nevertheless inspect the slice-coarea implementation carefully. The component-count theorem bounds topological complexity of definable superlevel sets; the BV conclusion also uses the piecewise regular structure of the bounded definable record. The manuscript supplies that graph structure and an explicit zero-extension convention, so I do not regard this as a detected gap, but it is a load-bearing continuum step.

## 11. Audit of the logarithmic return-window theorem

The new window theorem is a credible same-event extension of the marked theory.

### 11.1 Approximation of the whole weight

The weight

\[
 W_R(y)=\prod_{j=1}^{q}u_j((F_R^*)^{\ell_j}y)
\]

is not assigned a variation bound by pulling the factors through long induced iterates. Each factor is smoothed in its original collision coordinates. Invariance of the actual return map controls the smoothing error before the collision-count cutoff is introduced.

On each binary section-membership word below a collision cutoff, all observation collision indices are fixed. The exponential finite-record theorem then gives

\[
 \|W_{L,\epsilon}^0\|_{\mathrm{BV}}
 \le C(1+q\epsilon^{-1})e^{C_{\mathrm w}L},
\]

while

\[
 \|W_R-W_{L,\epsilon}\|_1
 \le C\{\epsilon V+e^{a_{\mathrm t}m-c_{\mathrm t}L}\}.
\]

The approximation has supremum at most one because the word supports are disjoint. Internal word jumps and the section trace are included.

### 11.2 Central integral and exponent margins

The marked central estimate is re-evaluated on a subband

\[
 |v|\le2n^\theta,
 \qquad 0\le\theta\le1/200.
\]

The two leading margins are

\[
 s_0(\theta)=1/28-5\theta,
 \qquad
 s_1(\theta)=1/14-4\theta.
\]

At `theta=1/200` they reproduce the inherited single-mark exponents. Applying this estimate to the full-window approximant and removing it in the original measure gives the four explicit margins

\[
 1/28-5\theta,
 \quad
 1/14-4\theta-C_{\mathrm w}b-d,
 \quad
 d-\kappa-4\theta,
 \quad
 c_{\mathrm t}b-a_{\mathrm t}a-4\theta.
\]

The exhibited parameter choice is strictly nonempty for arbitrary positive complexity and return-tail constants. I checked the displayed inequalities: the first three rational margins and the positive fraction of `c_t b` have the asserted slack.

### 11.3 Unchanged rare event

For indicator factors, the final event is the exact multiple-return event. Its probability is independent of the start index by invariance, but no independence of the observations or factorization of their probabilities is claimed.

Dividing by this unchanged probability gives conditional central convergence under the strict rarity margins. The proof cutoff is absent from the final event.

### 11.4 Actual moments

The marked moment theorem is applied to the approximating whole-window weight. The replacement cost is estimated in `L^2` by the square root of its `L^1` error, using the inherited actual fourth moment. The conditional normalized mean and covariance therefore converge under the separately displayed margins.

This is a genuine result for logarithmically many observations. It does not prove arbitrary long-path conditioning or exact physical lattice/time conditioning.

### 11.5 Weighted raw interface

When the observations additionally satisfy the finite-record subanalytic hypothesis, the same original weighted measure has a finite-count extraction and exact count-localized raw identity.

The article correctly does not identify arbitrary BV observations with this subanalytic class. It also leaves the weighted complementary residual, weighted edge correction, weighted derivative growth, and exact physical-event comparison explicit.

I found no decisive mathematical contradiction in the window theorem.

## 12. Remaining complementary-frequency problem

The raw Fourier complement begins at the physical central cutoff

\[
 |\omega|\asymp n^{-99/200}.
\]

The new theorems now provide function defects and local compressed resolvents on a meaningful joint neighborhood and on the previously missing small-frequency annulus. They do not yet provide the integrated transform estimate required by raw inversion.

The remaining tasks include:

1. a common operator or direct probabilistic estimate yielding long-time decay rather than a one-step defect;
2. compatibility of the reconstruction/mesh scale with the time scale, including the explicit conflict in Section 7 of this report;
3. control of the rest of the peripheral circle;
4. radius-uniform growing-regularity control on compact nonzero torus frequencies;
5. growing roof-frequency estimates;
6. the far roof-frequency tail;
7. a strict splice with constants that leaves a nonempty parameter range.

A local finite-matrix resolvent does not by itself give a contour-to-power estimate uniform in a dimension and mesh tending to infinity. The full `L^2` twisted Koopman operator is unitary, so its behavior cannot be substituted for the required anisotropic or regularized spectral dynamics.

## 13. Remaining raw-density estimates

Revision 18 converts the qualitative “all branches” request into a finite packet with exact error quantities. This is valuable. The following long-time estimates remain:

### 13.1 Uniform derivative growth

For `L_n` proportional to `n`, one needs a radius-uniform bound on

\[
 A_2(n,L_n,R,w)
 =\sum_\ell
   \|\partial_t^2 r^{w,L_n}_{n,R}(\ell,\cdot)\|_1
\]

strong enough to choose the far-roof cutoff while keeping the normalized error small.

Finiteness at each fixed packet is not enough. The prepared exponents may approach the threshold, singular values may coalesce, germ radii may shrink, and the number and coefficients of jets may grow.

### 13.2 Local edge correction

The exact correction

\[
 e^{L_n}-K_n*E^{L_n}
\]

must be small on the actual central windows after normalization. The finite extraction includes every edge but does not prove that this combined correction is negligible there.

### 13.3 Finite-band residual integral

The edge-subtracted residual transform must be integrated over the full complement of the central cutoff up to the selected roof cutoff. The function-defect theorem and compressed local resolvent are inputs, not this estimate itself.

All three estimates must be proved uniformly in the physical radius. Compactness alone does not control the finite preparation data as `n` grows.

## 14. Exact physical conditioning

The logarithmic-window theorem proves central and moment conclusions for an exact event measurable at several actual return states. It does not complete the final physical conditioning application.

That application still requires:

- weighted complementary-frequency estimates for the actual indicator class;
- weighted finite-count derivative and local-edge bounds;
- a raw-scale lower bound for the same exact denominator;
- a relative event-replacement estimate between the completed-return event and the exact physical-time/lattice observation event.

An `O(log t)` unfinished-return error cannot be discarded under a single lattice constraint without such a relative estimate. The same-event return-window theorem does not perform this replacement.

## 15. Top-four significance assessment

The manuscript now contains an unusually broad unconditional package for one carefully engineered Lorentz family:

- Gaussian and functional limits for an actual unbounded return record;
- growing central Fourier integrals;
- initial, terminal, intermediate and logarithmic-window observations;
- unsmoothed fourth moments and actual covariance convergence;
- uniform joint covariance nondegeneracy;
- complete measurable phase arithmetic;
- quantitative physical function defects;
- exact peripheral phase lifting;
- local finite-rank compressed resolvents;
- complete structural raw extraction at every finite count;
- exact count-localized central inversion identities.

Several of these ideas are mathematically interesting in their own right. The exact top-localized phase lift, the measurable phase rigidity, and the use of the observed count coordinate in raw inversion are particularly notable.

At the requested benchmark, however, the article is still organized around a raw mixed-density local limit theorem that it does not prove. The remaining estimates are precisely the long-time operator and density bounds that convert the structural framework into the announced theorem. They are not peripheral polishing.

Alternatively, a top-four claim could be supported by extracting a broad general theorem from the compensation, tower-lift, phase-defect, or finite-extraction methods and applying it in several substantially different systems. The current text remains centered on one triangular Lorentz family and a sequence of highly specialized interfaces.

I therefore do not regard revision 19 as meeting the closure and breadth threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

A reorganized paper centered on the completed Gaussian, marked/window, phase, compression, and finite-extraction results could be a strong specialist contribution after independent review. In that version the raw LLT should be presented as a precise future theorem or conditional interface unless the remaining bounds are proved.

## 16. Required work before another top-four review

### A. Resolve the compression-scale incompatibility

Provide a theorem with one common parameter choice that simultaneously controls:

- the physical finite-time consistency error at time `n`;
- the reconstruction norm of compressed vectors;
- the local peripheral resolvent;
- the contour-to-power conversion.

The parameter calculation must be written explicitly on the target frequency regions. The current estimates cannot simply be combined.

A genuine induced anisotropic space, a sharper finite-time approximation, or a new direct argument may be needed.

### B. Close the entire complementary Fourier integral

Prove the actual integrated estimate from the edge of the central ball through:

- the small annulus;
- compact nonzero lattice frequencies;
- the full peripheral return phase;
- growing roof frequencies;
- the far roof tail.

The result must apply to the physical characteristic function or the exact edge-subtracted residual, not only to one-step defects or finite matrices.

### C. Prove uniform long-time raw derivative and edge bounds

Quantify the constructible preparation uniformly for the finite-count packets used at time `n`. Bound the full second-derivative sum, the local extracted-edge correction, and the finite-band residual term with their true radius and count dependence.

Do not infer these estimates from initial-coordinate first variation or from finiteness of each fixed packet.

### D. Complete the weighted raw theory

For the actual conditioning classes, prove weighted versions of:

- the complementary integral;
- the finite-count derivative budget;
- the local edge correction;
- the raw denominator asymptotic.

State exactly which BV, subanalytic, marked, and multiple-time classes are stable under every step.

### E. Prove the physical-event replacement

Compare the exact physical observation with the completed-return event at relative, not merely absolute, scale. The comparison must be strong enough for the shrinking rare-event probabilities used downstream.

### F. Obtain independent specialist review

At minimum, experts should independently check:

- the Demers--Zhang collision-space imports;
- the Young product-set and finite-cover arguments;
- the exact peripheral tower lift and frequency shift;
- the finite-rank reconstruction and residual identity;
- the BPR finite-complexity application and slice-coarea step;
- the Cluckers--Miller constructible integration and preparation application;
- the complete finite-count graph and all singular-boundary alternatives;
- the eventual long-time operator and raw-density estimates.

## 17. Presentation and technical comments

1. Keep `z`, `xi`, `sigma`, `w`, `rho`, and the scalar resolvent parameter distinct. The current v17 section does this well.
2. Retain the height-weighted lift norm and unweighted top-defect formulas beside each other. They are easy to confuse.
3. State prominently that the exact peripheral lift is valid for every `xi`, while the quantitative defect theorem is local in `(z,xi)`.
4. Add the scale calculation of Section 7 of this report to the manuscript. It should appear before suggesting that the compressed route may yield annular power decay.
5. Do not call a finite-dimensional local resolvent a resolvent estimate for the uncompressed return operator.
6. Keep the smallest-singular-value formulation; an eigenvalue-only discussion would be insufficient for the non-normal compressions.
7. In the finite extraction, retain the reason constants and slopes are removed. This is an important distributional point.
8. Identify precisely where the Cluckers--Miller preparation supplies convergence, rather than only asymptotic preparation, for the differentiated one-variable germs.
9. Continue to distinguish finite-count structural completeness from uniform long-time estimates.
10. Beside every Fourier cutoff, display both the physical and rescaled radii.
11. In the logarithmic-window theorem, keep the four exponent margins visible; they explain the cost of the enlarged observation class.
12. Keep the final event separate from the proof cutoff and state explicitly that its probability need not factor.
13. Keep arbitrary BV observations distinct from finite-record subanalytic weights.
14. Do not identify conditional central characteristic convergence or conditional moment convergence with a conditional raw LLT.
15. Preserve the exact edit ledger and ordinary-source identity in future revisions.
16. Update validation prose only after an exact-SHA remote run actually completes.

## 18. Verification boundary

I reviewed:

- the exact branch and commit identities;
- the source chronology from revisions 17--19;
- the source manifest, proof ledger, response, validation record, and publication-status metadata;
- the six new mathematical modules;
- the displayed frequency, regularity, rarity, and moment margins;
- the finite binomial component estimate used in the exponential complexity theorem;
- the stated constructible integration/preparation inputs and their use in the one-dimensional raw extraction;
- the actual GitHub Actions state at the reviewed SHA.

I did not independently reconstruct every inherited billiard singularity estimate, formally verify every constructible germ, or certify the complete 125-page manuscript proof by proof.

Finite diagnostics can verify algebraic exponents, exact tower identities, source hashes, compression residual identities, and selected finite models. They cannot prove the continuum collision-space estimates, the full semialgebraic collision graph, the constructible preparation application, mesh-uniform uncompressed power decay, uniform long-time raw derivative bounds, or the final local limit theorem.

The present report is therefore a mathematical and editorial assessment at the requested standard, not a formal proof certificate.

## 19. Final conclusion

Revisions 17--19 make credible and substantial progress.

The arbitrary peripheral return phase is lifted exactly. Local physical defects are converted into finite-rank resolvent bounds without normality assumptions. The entire fixed-count raw density, including singular itinerary boundaries, is structurally extracted into explicit power--logarithm jets and a `W^{2,1}` residual. The observed count coordinate yields an exact central-window inversion identity for the original law. Exponential finite-record complexity sharpens the regularization budget, and logarithmic return windows admit unchanged-event central and moment laws.

I found no decisive counterexample in these new proof chains.

Nevertheless, the raw mixed-density LLT remains unproved. The current compression consistency and local resolvent estimates have incompatible scales on the target annulus. The complete complementary integral, uniform long-time derivative and local-edge bounds, weighted raw estimates, and exact physical-event replacement remain open interfaces.

These are central analytical mechanisms rather than technical presentation tasks. For that reason I recommend rejection at the requested top-four benchmark in the present form, while recognizing revision 19 as a materially stronger manuscript and a potentially strong specialist contribution after reorganization and independent expert verification.
