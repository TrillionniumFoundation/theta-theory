# Response to the seventeenth pipeline-aware referee report

**General Theta Foundations I — Revision 33**  
**Compatible Polyhedral Lifts and Quantitative Causal Width**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v32-causal-width-pipeline-harsh-top4-r17-2026-09-25/REFEREE_REPORT.md`, frozen at `eaa2661530ed473f8b79407eba7a1182c8e0a450`. Reviewed publication: v32 at `d38fca741135d147dfdbdbd99cfd9a1a716a88a5`, native source `4ccfe985f0507154969b4405e94b99a2c8a451f3`.

The report accepts the prior full-support, fixed-alphabet divergence theorem but identifies the missing extension-complexity comparison and the logarithmic-versus-square-root gap as central. This revision takes that diagnosis literally. It formulates compatible stochastic lifts, improves the quantitative potential and the exact construction, obtains matching growth for the clearly defined vector-state class, provides an explicit rational-angle rate, and gives a clock-free comparison under an explicitly stronger anytime query specification. Earlier mathematical content is preserved, not withdrawn. The new analytic proofs stand in the focused article independently of the large archives.

## 12.1 / Sections 4 and 13 — positive realization and finite Hankel comparisons

**The missing direct precedent is restored, with the stationary quantifier made explicit.**

The main article now cites Benvenuti–Farina (1999), *An example of how positivity may force realizations of “large” dimension*. It gives the degree-three family H_m in the normalization of Czaja–Jaming–Matolcsi, Example 2, equation (3.1), and credits both the original lower bound m and the later exact positive order m. We inspected the original authors' full 2003 survey and the full later matching-order proof; access to the original 1999 text itself was not represented as a complete proof-level audit.

A still closer conceptual comparison is included: Benvenuti–Farina (2003), Section 3, Example 4, has a nonnegative Hankel factorization of inner size three without a three-dimensional positive realization. Their Theorem 2 includes the positive intertwining equation. Therefore the need for compatibility, or failure of positive factorization alone, is not advertised as a new discovery.

A finite prefix–suffix matrix is analogous to a finite Hankel truncation: a state register factors it positively. But a lower bound requiring one repeated positive matrix does not automatically apply after the rows are allowed to change at every epoch. The present experiment fixes all command words and permits a new realization for each finite horizon. No encoding of the classical H_m family preserving this complete interface and separate minima three is asserted. Conversely, no new stationary lower bound for H_m is claimed. The additional content is a cumulative finite-horizon inequality valid even when every row can vary, plus the sharpened constructive bounds.

The autonomous theorem later in the paper uses Cayley–Hamilton and the classical peripheral-spectrum restriction explicitly. It is an application of those tools, not a claim that the old stationary obstruction was missing.

## 12.2 / Section 5 — static extensions versus compatible stochastic lifts

**A normalized dynamic object, a dual extension criterion and a strict extension defect are proved.**

`prop:slack` shows that a positive-dimensional bounded polytope with f facets is affinely equivalent to a section of Delta_f. Strictly positive weights balancing its facet normals normalize its slacks. Thus bounded static extensions do not lose their facet count merely by being written as simplex sections. Unbounded extensions are not being covered by that statement.

The essential extra requirement is ambient stochastic extendibility. A positive affine map between sections may fail to extend to a row-stochastic map on their full ambient simplices. `thm:extension-dual` gives a necessary and sufficient support-function inequality for fixed sections and a fixed proposed affine map. Its feasibility and separation versions are linear programs. This is elementary convex duality, not a global optimizer over unknown lifts.

`prop:extension-gap` quantifies the distinction. On Q={e in Delta_4: e1+e2=e3+e4=1/2}, the map F(e)=(2e1,2e2) is positive and normalized. Nevertheless its least uniform total-variation error over all ambient stochastic extensions is exactly 1/4. The lower witness compares two source vertices; an explicit stochastic row attains the bound. This is not a claim that every small extension of a regular polygon has the same obstruction.

`def:dynamic` requires compatible sections, seed lifts, inter-epoch affine maps, observable intertwining, stochastic ambient extensions, and a final decoder that also extends to the ambient simplex. `thm:lift-equivalence` proves equality of the entire feasible coordinate-profile set with that of the original hidden-state machine. The data contain no supplied residual-state restriction. The fixed-data extension test makes the extra dynamical condition explicit.

Yannakakis' slack/nonnegative-rank theorem, regular-polygon logarithmic extensions of Fiorini–Rothvoss–Tiwary and the refinements of Vandaele–Gillis–Glineur are now central comparisons. The inherited 2^K projected-vertex estimate is explicitly a classical face count. The paper neither assumes that static logarithmic lifts furnish stochastic transitions nor asserts that they can never do so.

## 12.3 — sharpening the growth theorem

**The general lower and upper bounds improve; the vector-state problem has matching cube-root order.**

The new potential is mean support m(P), equivalently perimeter/(2 pi), rather than area. `lem:accumulation` proves that the mean-support increase of a q-step orbit hull is at most (q-1) times the one-step increase. `lem:perimeter` gives the sharp inscribed-polygon perimeter bound. A convergent p/q with q>=8M then gives, in `thm:mean-growth`,

```
m(conv(P union R P))-m(P) >= 3a/(4 M^2 q),  a B_2 subset P.
```

For partial quotients bounded by A, a suitable q is less than 8(A+1)M. The profile gain is therefore of order M^(-3), without the old conversion of a displacement into a squared area cap. Applying the reachable-section bound M<=2^K gives

```
sum_(t<N) 2^(-3 K_t) <= 160(A+1).
```

At the golden angle the right side is 320, compared with the earlier exponent six and constant 24,000,000.

`lem:resonance` and `thm:upper` use regular polygons whose order is a convergent denominator. The mismatch angle is of order q^(-2), and the radial expansion per step has log lambda <= 40/q^3. Explicit two-point active rows and an idle-plus-uniform row implement the exact rotated barycenter. For q the first convergent above max(5,(40N)^(1/3)), all states remain in the observation square. This improves the unrestricted upper bound from O(sqrt N) to O_alpha(N^(1/3)) at bounded-type angles.

The lower bound becomes polynomial under a **separate, explicit statewise hypothesis**: each available state carries its own predictive vector and each row intertwines these vectors. Then the observable polygon has at most K vertices, rather than 2^K. `thm:profiles` consequently gives sum K_t^(-3)<=160(A+1). Combined with the resonant construction this proves V_N=Theta_alpha(N^(1/3)) against all time-dependent vector-state chains, not only regular polygons.

We do not identify V_N with the unrestricted hidden width W_N. The general problem remains between a logarithmic lower bound and a cube-root upper bound. Its possible savings through genuinely hidden compatible lifts are exactly why the paper separates the two classes. The original unrestricted theorem is strengthened, not silently replaced by a restricted one.

## 12.3 / 12.4 — explicit rational-angle rate and honest constants

**An elementary rate replaces solely formal effectiveness.**

For zeta=(3+4i)/5, the nonzero Gaussian integer (3+4i)^r-5^r has modulus at least one. Hence ||r alpha||>=5^(-r)/(2 pi). Applied to successive convergents, this gives Q_alpha(M)<7*5^(8M), which combines with the same potential to prove

```
sum_(t<N) 2^(-2 K_t) 5^(-8*2^K_t) <= 140,
N <= 140*2^(2W_N)*5^(8*2^W_N).
```

The resulting explicit hidden lower rate is doubly logarithmic; the vector-state lower rate is logarithmic. This does not rely on unproved bounded-type behavior of the rational rotation angle. It is quantitatively weak but explicit in N, unlike a claim that a quantifier-elimination program eventually returns some threshold. The rational counter upper bound 3(N+1) remains and is reproved with exact rows.

For the golden angle the displayed lower bound exceeds three after N>163,840. The old threshold was N>6,291,456,000,000. Both numbers are stated. The new bound is not described as a practical optimum at small horizons; it is a stronger analytic budget and supports the exact order in the vector-state class.

## 12.5 — clock-free and contractive comparisons

**A linear-order theorem is obtained for one fixed decoder at all stopping lengths.**

`def:anytime` removes the epoch input, uses one state set and fixed command rows, and requires one fixed decoder to answer a terminating query after every length 0 through N. There is still only one query, not repeated independent access. The new specification is stronger than answering only at exactly N and is marked as such throughout.

`thm:autonomous` proves N+1<=A_N<=3(N+1)+2 for every infinite-order rotation. If a K-state device worked through length K, Cayley–Hamilton applied to the first K+1 active-command outputs would force the rotation eigenvalue into its stochastic transition matrix. A unit-modulus eigenvalue of a finite stochastic matrix is a root of unity, a contradiction. The matching-order counter upper machine has fixed rows and a decoder reading the stored count; its entire phase/count alphabet is charged. Rational rotations give rational rows.

This yields a concrete distinction: fixed-length vector-state width is cube-root at bounded-type angles, but anytime autonomous total state count is linear. The resonant upper machine does have stationary command rows; its horizon-dependent decoder compensates exactly N contractions and cannot be used unchanged at earlier stopping lengths.

`cor:contraction` also proves that a strict contraction rho R has a horizon-independent finite polygon realization, with O_alpha(1+(-log rho)^(-1/3)) processing labels at bounded-type angles. This is a quantitative instance of the classical invariant-polytope principle. Neither autonomous comparison prices read-only tables or exact coin implementation, and no succinct bit-space theorem is inferred.

## 12.6 — composition beyond exact tags

**The old theorem is retained with its exact hypothesis; noisy-tag composition is not inferred.**

The r17 report correctly identifies exact final tag recovery as the source of support separation in the prior profile sum. That theorem remains unchanged in the supporting manuscript. The current revision pursues compatible lifts and quantitative rotation geometry instead of filling a noisy-tag theorem with an unsupported extension. Its growing tagged frontier is not re-advertised as a new main result. Full support belongs to the rotation experiment, not to wrong-tag-zero examples.

## 12.7 / 12.8 — focus, history and originality

The focused article contains its own model, lift tests, mean-support proof, convergent construction, rational bound and autonomous comparison. The program name is retained, but no independent analytic dependency or editorial outcome is asserted by it. The neutral contribution table distinguishes inherited, classical and new ingredients. The repository's A2/A3/A4/C2/D1 and hard-sphere analytic chains retain their Fourier/LLT, large-deviation, common-domain, semigroup and optional-projection obligations. None is marked closed by these finite-state results.

We re-read the frozen Round-Seventeen proof-dependency ledger and the prior source arguments used in the current proof. The full v32 article is preserved byte-for-byte as supporting-results.pdf. Its cumulative volumes follow the current article and a divider in separate archives. The compact referee package excludes those archives. No old repository source or report is overwritten.

`LITERATURE_AUDIT.md` records inspected primary texts, precise theorem comparisons and access limits. The original 1999 paper is credited via its publication record, its authors' detailed full survey and the full subsequent exact-order construction. The original Yannakakis result is credited and compared through the inspected FRT statement and proof context. An exhaustive independent priority review is not claimed and cannot be manufactured by a citation list or a build receipt.

## Consolidated disposition of the detailed comments

The core definitions distinguish available labels, hidden affine sections and vector states; the 2^K count is standard extension face counting. The final query is singular and fixed-length except in the separately named anytime section. Bounded-polytope simplex normalization is proved, while stochastic map and decoder extensions are required separately. The golden rows use exact computable-real constants, not a finite fair-bit implementation. The old rational counter's full count alphabet is charged in the autonomous comparison. Quantifier elimination is not a new main theorem. Contraction and higher-dimensional scope are discussed without transferring unsupported exponents. The seed hull and separate-rank hypotheses remain explicit. Historical appendix and tag theorems are preserved without entering the new novelty summary. Finite checks stay outside the proof narrative.

The principal remaining mathematical boundary is the unrestricted hidden-lift gap. The new matched vector-state result, general cube-root upper bound, stronger general lower profile, explicit rational rate and autonomous comparison are proved in full. None is represented as a solution of every research direction proposed in the report.
