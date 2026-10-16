# External top-four referee report on A2-DYN revision 110

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v110-nongrazing-source-referee-response-2026-10-14`, `revision/a2-dyn-v110-nongrazing-source-referee-copy-2026-10-14`  
**Reviewed author commit:** `0abce3fcfbc735ff5cc6d085279abea5f32a7a22`  
**Reviewed repository tree:** `25396bdb818cfb5521280815874520f50ae107a0`  
**Active manuscript directory:** `papers/A2-DYN-v110-referee-response`  
**Active mathematical source:** 264 numbered core modules in the complete packet; revision 110 adds modules 262--264  
**Immediate mathematical baseline:** revision 109 author commit `ab0ad79b9c101b82c80e33511529588d101a45c0`  
**Frozen revision-109 manuscript tree:** `99e677d4a40f087fc21a2c050e1cc4f43e3ef155`  
**Controlling report:** `reviews/a2-dyn-v109-capacity-abundance-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Controlling review commit / report blob:** `cdf0149246de7dd6b68b0b276d9dc1c4ca5537c2` / `dac29f62397ea98f43d6229928d45faced6dbc2a`  
**Exact-SHA qualification at review freeze:** response run `38528720288`, queued; referee-copy run `38528745560`, queued  
**Date:** 14 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 110 is a genuine theorem-bearing response to the revision-109 report. It does not merely introduce another comparison certificate, relabel the nongrazing residual, or replace the original pointwise objective by an averaged statement. It acts directly on the original positive microscopic source and proves a new finite-count payment for a positive submeasure of that source.

The central new decomposition is the following. On each complete physical pairing segment, let

\[
\mathcal V^\varepsilon(\theta)
  =\operatorname{Var}_{[a(\theta),b(\theta)]}
       f^\varepsilon(\cdot,\theta)
\]

be the total variation of the original weighted density, and let

\[
c^\varepsilon(\theta)
 =\min\{f^\varepsilon(a+,\theta),f^\varepsilon(b-,\theta)\}
\]

be the original paired coefficient. For an outer multiplier \(\gamma\ge1\), the revision splits

\[
c^\varepsilon
 =c_{\rm var}^{\varepsilon,\gamma}
  +c_{\rm per}^{\varepsilon,\gamma},
\]

where

\[
c_{\rm var}^{\varepsilon,\gamma}
 =\min\{c^\varepsilon,\gamma\mathcal V^\varepsilon\},
\qquad
c_{\rm per}^{\varepsilon,\gamma}
 =(c^\varepsilon-\gamma\mathcal V^\varepsilon)_+.
\]

The first term is a genuine positive submeasure of the original source. It is not an endpoint-current difference, a signed Jordan component, a comparison capacity, or a density with a changed normalization.

Using the closed-segment absolute continuity established in revision 109, revision 110 proves

\[
\mathcal V^\varepsilon(\theta)
 \le C_{\rm reg}(1+\varepsilon^{-1})
       \int_{a(\theta)}^{b(\theta)}
       \frac{A(u,\theta)I_m(u,\theta)}{z(u,\theta)}\,du.
\]

It then performs the complete one-copy physical sum before taking any norm. If the selected segment contains the original target roof \(t\) and has length below \(h\), the entire segment lies in \((t-h,t+h)\). Consequently

\[
T_{H,\rm var}^{\varepsilon,\gamma}(t)
 \le C_{\rm reg}\gamma(1+\varepsilon^{-1})
       \int_{t-h}^{t+h}v^0(u)\,du.
\]

At the stated outer schedule

\[
 h_B=\delta(B)/2,
 \qquad
 \gamma_B=\max\{2,\varepsilon(B)^{-1/32}\},
\]

this gives

\[
\mathcal H_M(\mathsf U_B^{\rm var})
 \le C_MB^{-95/384}.
\]

This is a substantive positive-source estimate. It does not use a lower residence cutoff, an endpoint-speed lower bound, an angular continuation corridor, a selected comparison family, or an unweighted count of collision words.

The revision also proves a useful physical description of the complementary coefficient. If

\[
c_{\rm per}^{\varepsilon,\gamma}>0,
\]

then the original density is nearly constant on the whole closed segment:

\[
|f^\varepsilon(u,\theta)-c^\varepsilon(\theta)|
 <\gamma^{-1}c^\varepsilon(\theta).
\]

In particular the original guard remains positive at every point of the segment. At each point at least one original incidence or clearance test lies below its doubled guard threshold, although the witnessing test may vary along the segment. Conversely, if the original guard vanishes at even one point of the closed segment, the whole paired coefficient is assigned to the paid variation part.

Finally, keeping the full original nongrazing comparison pool, the manuscript obtains the exact positive identity

\[
\mathsf U_B^{\rm micro}
 =\mathsf U_B^{\rm var}
  +\min\{\mathsf U_B^{\rm per},K_BP_{r_B}^{\rm ng}\}
  +\mathsf R_B^{\rm per},
\]

where

\[
\mathsf R_B^{\rm per}
 =\bigl(\mathsf U_B^{\rm per}-K_BP_{r_B}^{\rm ng}\bigr)_+.
\]

The old and new shortages satisfy

\[
0\le
\mathsf R_B^{\rm ng}-\mathsf R_B^{\rm per}
\le
\mathsf U_B^{\rm var},
\]

and hence

\[
\mathcal H_M(
\mathsf R_B^{\rm ng}-\mathsf R_B^{\rm per})
 \le C_MB^{-95/384}.
\]

I audited the newly landed material

- `core/262_positive_variation_payment.tex`;
- `core/263_persistent_guard_and_nongrazing_shortage.tex`;
- `core/264_optical_cofactors_and_simultaneous_endpoints.tex`;
- the revised article shell;
- `RESPONSE_TO_REFEREE.md`;
- `PROOF_LEDGER.md`;
- `SOURCE_MANIFEST.json`;
- `PUBLICATION_STATUS.json`;
- `VALIDATION.md`;
- the retained revision-109 optical and endpoint modules needed by the new proof; and
- the controlling revision-109 report.

Within the assumptions actually stated in those files, I found no decisive sign error, no invalid positive-source subtraction, no missing factor of the roof-window length, no exponent-arithmetic error, no hidden differentiation of the selector, no word-count multiplier, and no illegal exchange of the collision limit with an outer scale. The total-variation payment, persistence implication, positive-part comparison, signed corner cofactor, multi-mark optical expansion, and simultaneous-endpoint passage are internally coherent.

The negative recommendation is nevertheless forced by the exact endpoint of the revision. The final scalar theorem is

\[
\mathcal E_M
 \le
\mathcal H_M(\mathsf R_B^{\rm per})
 +C_MB^{-1/384},
\]

and the manuscript proves that the unchanged exact-label raw pointwise assertion is equivalent to

\[
\mathcal H_M(\mathsf R_B^{\rm per})\longrightarrow0
\qquad
\text{for every fixed }M.
\]

**No theorem establishes this limit.**

The revision proves that every surviving source coefficient lies on a short nongrazing segment with nearly constant positive density and a persistent original guard. It does not prove that the ordered pointwise height of those coefficients is small. A positive density can remain essentially constant on an arbitrarily short segment while retaining a large pointwise value. The fixed-window volume estimates control an integral or a paid variation component; they do not by themselves control this remaining amplitude.

The full nongrazing comparison pool may also remain capacity-deficient at the prescribed, collision-independent window. Neither the per-itinerary multi-mark bound nor the existence of a bad guard witness at every roof point supplies a collision-uniform summation theorem over the physical pairing family.

Thus revision 110 proves another real physical component of the scarcity problem, but the persistent guarded shortage remains the upper pointwise obstruction itself. It is not a harmless secondary error after the main theorem.

At the requested four-journal benchmark, this is insufficient for acceptance. The new decomposition and optical refinements are technically meaningful, but the article continues to be organized around an exact-label raw pointwise local limit theorem which remains unproved. Nor, in its present highly specialized form, does the variation payment by itself constitute a separate theorem of top-four breadth independent of that unfinished endpoint.

## 2. Frozen source and chronology

The two reviewed author branches both resolve to

`0abce3fcfbc735ff5cc6d085279abea5f32a7a22`.

The repository tree at that commit is

`25396bdb818cfb5521280815874520f50ae107a0`.

The active article is

`papers/A2-DYN-v110-referee-response/main.tex`.

The complete revision-109 packet is preserved under

`papers/A2-DYN-v110-referee-response/archive/v109`,

with frozen tree

`99e677d4a40f087fc21a2c050e1cc4f43e3ef155`.

The theorem-bearing revision-110 author commit descends from the initial revision-110 source-freeze commit

`5dd17967af39b4a831f2c69424a95219332fc30d`.

The mathematical baseline reviewed by the controlling report is revision 109 at

`ab0ad79b9c101b82c80e33511529588d101a45c0`.

The controlling review commit is

`cdf0149246de7dd6b68b0b276d9dc1c4ca5537c2`,

and its report blob is

`dac29f62397ea98f43d6229928d45faced6dbc2a`.

Revision 110 retains modules 260--261 byte-for-byte and adds

- `core/262_positive_variation_payment.tex`;
- `core/263_persistent_guard_and_nongrazing_shortage.tex`;
- `core/264_optical_cofactors_and_simultaneous_endpoints.tex`.

The complete packet contains 264 numbered core modules. The original model source remains blob

`6af1dcb4548e1b5dd82b9a330dead6e04fd09797`.

The active source manifest accurately keeps the following claims false:

- persistent-shortage height decay;
- the full raw-return local limit theorem;
- closure of the primary referee request;
- a weighted word-sum theorem derived from the multi-mark identity;
- independent human review; and
- formal proof certification.

The present review branch starts directly from the exact revision-110 author commit and adds only this report under

`reviews/a2-dyn-v110-persistent-guard-external-top4-review-2026-10-14/`.

No author manuscript, author branch, workflow, prior report, historical paper tree, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-v110-source-and-manuscript.yml`.

At the freeze of this report, the exact-SHA runs were

- response branch run `38528720288`: `queued`, conclusion `null`;
- referee-copy branch run `38528745560`: `queued`, conclusion `null`.

I therefore do not describe revision 110 as remotely qualified at the review freeze.

The local validation record reports:

1. a successful native pdfLaTeX build of the 18-page active article;
2. stable references, no duplicate labels, and no overfull boxes;
3. exact blob matching for the retained revision-109 active sources;
4. matching ordinary and optimized Python diagnostics;
5. 56 optical/continuant/Schur configurations;
6. 1,016 marked-set inequalities;
7. 4,096 positive-source and shortage identities;
8. 108 whole-segment localization cases; and
9. exact rational verification of the exponents \(95/32\) and \(95/384\).

These checks are useful source and implementation evidence. A later successful workflow would not certify

1. the inherited incident-component pairing-space construction;
2. the one-copy physical multiplicity convention;
3. the common coarea versions for the complete exact-label family;
4. the inherited regular-point weighted derivative estimate;
5. the fixed-window spectral and pressure averages;
6. the collision-uniform scarcity of persistent guarded segments;
7. a weighted physical summation of the multi-mark optical estimate;
8. decay of \(\mathsf R_B^{\rm per}\); or
9. the full exact-label raw pointwise local limit theorem.

The manuscript and validation record correctly distinguish software qualification from mathematical certification.

## 4. Scope of this review

The substantive audit concentrates on

1. the measurability of the total variation on the Borel physical pairing space;
2. the passage from the regular derivative bound to full closed-segment variation;
3. the positive coefficient split before roof pushforward;
4. whole-segment localization in the original target window;
5. Tonelli summation and one-copy use of the uncut optical volume;
6. the outer exponent arithmetic;
7. the persistence consequence for the original guard;
8. the exact three-term positive decomposition;
9. comparison of the old and new shortages;
10. the remaining limit and its quantifier order;
11. the signed endpoint corner cofactor;
12. the positive optical polynomial and multi-mark inequality;
13. simultaneous endpoint mechanisms;
14. the explicit uniform trace modulus; and
15. source identity and qualification chronology.

The first 261 numbered modules, the global pairing construction, and the larger inherited spectral, pressure, arithmetic, Gaussian, coarea, and raw-inversion pipeline are treated as source-pinned inputs. I have not independently re-proved that complete historical chain.

## 5. The inherited obstruction from revision 109

Revision 109 had reduced the original pointwise problem to

\[
\mathcal E_M
 \le
\mathcal H_M(\mathsf R_B^{\rm ng})
 +C_MB^{-1/384},
\]

with

\[
\mathsf R_B^{\rm ng}(t)
 =\bigl(
 \mathsf U_B^{\rm micro}(t)
 -K_BP_{r_B}^{\rm ng}(t)
 \bigr)_+.
\]

It had already proved:

- a uniformly positive reduced endpoint Hessian;
- an exact positive optical denominator;
- one-mark inverse-incidence bounds;
- integrability of the inverse gradient in Gauss coordinates;
- finite one-sided endpoint traces;
- zero paired source on visited-grazing-ended segments;
- payment of their complete comparison capacity; and
- the distinction between visited grazing and tangency to an unvisited third disk.

The revision-109 report emphasized that the remaining nongrazing shortage could still contain unvisited tangencies, nongrazing critical entrances, section-boundary cuts, shrinking flat or short-reach segments, and capacity-deficient physical sheets.

Revision 110 acts on that correct remaining source. It does not change the section, guard, labels, normalization, central roof sets, or essential-height topology.

## 6. Borel total variation and closed-segment payment

Module 262 defines

\[
\mathcal V^\varepsilon(\theta)
 =\operatorname{Var}_{[a(\theta),b(\theta)]}
     f^\varepsilon(\cdot,\theta).
\]

The measurability argument is appropriate. After pulling each physical segment back to \([0,1]\), continuity in the segment variable permits computation of variation using finite rational partitions. The variation is therefore a countable supremum of Borel functions.

Because revision 109 established absolute continuity on the closed segment,

\[
\mathcal V^\varepsilon
 =\int_a^b|\partial_u f^\varepsilon|\,du.
\]

The inherited regular derivative input gives

\[
\mathcal V^\varepsilon
 \le C_{\rm reg}(1+\varepsilon^{-1})
       \int_a^b AI_m/z\,du.
\]

This is stronger than an endpoint-difference estimate. A function may return to the same endpoint value while varying substantially in the interior; the manuscript pays the full variation.

For a selected segment of length below \(h\) containing \(t\), the inclusion

\[
(a,b)\subset(t-h,t+h)
\]

is exact. Multiplication by the original selector is harmless because the selector remains at the starting roof and lies in \([0,1]\). Summing the resulting nonnegative integrals over the complete physical pairing space before taking a norm is the correct order. The inherited one-copy coarea identity then gives the finite-count payment by \(v^0\).

I found no hidden number-of-sheets factor in this argument.

## 7. The outer schedule and rate

With

\[
\gamma_B=O(\varepsilon^{-1/32}),
\qquad
h_B=O(\varepsilon^4),
\]

the payment is

\[
O\bigl(
\varepsilon^{-1/32}
(1+\varepsilon^{-1})
\varepsilon^4
\bigr)
 =O(\varepsilon^{95/32}).
\]

Since \(\varepsilon(B)=A_0B^{-1/12}\), this is

\[
O(B^{-95/384}).
\]

The exponent arithmetic is correct. The widths and multiplier are chosen from the outer parameter before the physical sum, uniform norms, and collision limsup.

The rate is much faster than the inherited \(B^{-1/384}\) budget. It can therefore be absorbed without changing the governing error scale.

## 8. Persistence of the original guard

If

\[
c_{\rm per}^{\varepsilon,\gamma}>0,
\]

then

\[
c^\varepsilon>\gamma\mathcal V^\varepsilon.
\]

An endpoint attains \(c^\varepsilon\), and total variation bounds the change from that endpoint to every point of the closed segment. Hence

\[
|f^\varepsilon(u)-c^\varepsilon|
 \le\mathcal V^\varepsilon
 <\gamma^{-1}c^\varepsilon.
\]

This proves strict positivity of the weighted density throughout the segment.

On the nongrazing class, the optical factor is finite and positive on the closed segment, including a critical incoming endpoint with fixed Gauss direction. Thus \(f^\varepsilon>0\) implies \(W^\varepsilon>0\).

Because every guard factor lies in \([0,1]\) and equals one once its normalized argument is at least two, \(W^\varepsilon>0\) implies that at least one original incidence or clearance test is below its doubled threshold. The witness may vary with the roof coordinate, as the manuscript correctly states.

Conversely, if the guard vanishes at one point, then the weighted density vanishes there. The total variation from an endpoint attaining the positive paired minimum is at least the minimum itself, so the whole coefficient is paid by the variation part. This implication is correct.

The result is a useful necessary condition for the unresolved source. It is not a smallness theorem for that source.

## 9. Exact residual comparison

Set

\[
U=\mathsf U_B^{\rm per},
\qquad
Y=K_BP_{r_B}^{\rm ng}.
\]

Then

\[
U=\min\{U,Y\}+(U-Y)_+.
\]

Combining this identity with

\[
\mathsf U_B^{\rm micro}
 =\mathsf U_B^{\rm var}
 +\mathsf U_B^{\rm per}
\]

gives the displayed three-term source decomposition.

Moreover, the positive-part map is monotone and one-Lipschitz. Since

\[
\mathsf U_B^{\rm micro}
 =\mathsf U_B^{\rm per}+\mathsf U_B^{\rm var},
\]

one obtains

\[
0\le
(\mathsf U_B^{\rm micro}-Y)_+
 -(\mathsf U_B^{\rm per}-Y)_+
\le
\mathsf U_B^{\rm var}.
\]

This is exactly the claimed comparison between \(\mathsf R_B^{\rm ng}\) and \(\mathsf R_B^{\rm per}\).

The full nongrazing comparison pool is retained. It is not restricted to the persistent source class, and already-paid sheets may still supply scalar roofwise capacity. This is consistent with the earlier canonical allocation framework.

## 10. Optical appendix

### 10.1. Signed corner cofactor

The signed formula

\[
G_{0m}=(-1)^{m-1}
 \frac{R^2c_0c_m}
 {\bigl(\prod_{i=0}^{m-1}\tau_i\bigr)\det J}
\]

is consistent with the Schur complement and the alternating sign of the corner entry of the inverse tridiagonal matrix. The direct \(m=1\) case has positive sign, and the \(m=2\) case has negative sign. Taking the absolute value only when defining \(\omega\) removes a possible ambiguity in the earlier exposition.

### 10.2. Positive multi-mark expansion

Expanding

\[
\mathsf C(\kappa)=I+\kappa E
\]

inside the optical product gives the positive polynomial

\[
\mathfrak b_m
 =\sum_{S\subset\{1,\ldots,m-1\}}
   \left(\prod_{j\in S}\kappa_j\right)
   \prod_{\nu=0}^{|S|}T_{j_\nu,j_{\nu+1}}.
\]

All coefficients are positive. Retaining the unmarked reflection factors and factoring the coefficient of a prescribed marked set into intervening optical blocks gives

\[
\frac{\omega}{\prod_{j\in S}c_j}
 \le
\frac{R_+^{|S|+1}}
 {2^{|S|}\tau_-^{|S|+1}}
\varrho^{m-|S|-1}.
\]

The formula specializes correctly to the zero-mark and one-mark estimates. The manuscript appropriately restricts the conclusion to a fixed finite itinerary and does not sum it over collision words without a separate weighted-complexity theorem.

### 10.3. Simultaneous endpoints

The whole-approach endpoint argument is clearer in revision 110. Gauss-coordinate control gives a full one-sided limit, not merely a subsequential one. The designated entry root is continuous up to tangency, the flight lower bound prevents collapse, and the reflection map is continuous at tangency. Finite horizon reduces possible nearby third-disk centers to a finite set, so the clearance minimum also has a limit.

This treats simultaneous visited grazing, unvisited tangency, a section boundary, and a critical incoming endpoint without continuing the event beyond its physical boundary.

### 10.4. Uniform trace modulus

The explicit constant

\[
C_{\rm H}
 =\frac{500C_{\rm reg}\sqrt{2\Lambda_\circ}}
 {4\pi c_*\lambda_\circ^2}
\]

is consistent with the marked optical bound, \(\chi\ge\lambda_\circ\), the regular derivative input, and the Gauss-coordinate inverse-gradient estimate. Its remaining inherited dependence is exactly the uniform regular variation constant \(C_{\rm reg}\).

## 11. The decisive remaining obstruction

The required estimate is

\[
\lim_{B\to\infty}
\limsup_{m\to\infty}
\sup_{R,n,k}m^2
\esssup_{t\in\mathcal C_{m,R,n,k}(M)}
\bigl(
\mathsf U_{B,m}^{\rm per}(t)
 -K_BP_{r_B,m}^{\rm ng}(t)
\bigr)_+=0.
\]

Revision 110 does not prove this statement.

The new persistence theorem says that every surviving segment has:

1. positive nongrazing optical density;
2. relative oscillation below \(\gamma_B^{-1}\);
3. the original guard active at every roof point; and
4. at least one small original incidence or clearance test at each roof point.

These are strong structural restrictions, but they do not control pointwise height. A nearly constant coefficient of size one supported on a segment of length \(h_B\) has small roof mass but can retain order-one pointwise height. The inherited uncut volume estimate pays variation; it does not rule out such an almost-flat spike.

Nor does the pointwise existence of a guard witness produce a uniform physical summation. There are \(O(m)\) possible incidence and clearance tests, their thresholds depend on depth, and the witness may change along the segment. A future proof must control the complete family without multiplying a per-itinerary estimate by an uncontrolled number of words or sheets.

The nongrazing pool may also have insufficient fixed-window capacity at the prescribed \(r_B\). The manuscript has not shown that persistent source height is bounded by that capacity, nor that the capacity shortage is rare in the essential-roof topology.

This is the exact point at which the main theorem remains open in the manuscript.

## 12. What a decisive next revision must prove

A revision capable of changing the recommendation must close the displayed persistent-shortage limit. Merely producing another positive split or another certificate class will not suffice unless it yields the required collision-uniform pointwise estimate.

Several routes remain logically possible.

### Route A: persistent-segment scarcity

Prove a physically summed theorem showing that segments with

\[
\mathcal V^arepsilon<c^arepsilon/\gamma_B
\]

and an active original guard at every roof point have vanishing ordered height. Such a theorem would need a collision-uniform packing, multiplicity, or weighted-complexity estimate in the original essential-roof topology.

### Route B: fixed-window capacity abundance

Prove that the complete nongrazing canonical pool has enough capacity at the prescribed outer window to pay the persistent source, up to a term of vanishing ordered height.

### Route C: uniform guard-witness summation

Convert the pointwise existence of an incidence or clearance witness into a finite-count positive decomposition with a collision-uniform weighted sum. The witness may change along the segment, so a valid proof must handle the resulting cover without an uncontrolled \(m\)- or word-count factor.

### Route D: genuine microscopic insertion

Establish the previously formulated inverse-residence or logarithmic source insertion with constants uniform in collision count, radius, labels, and the outer stage. The existing criteria are implications, not proved estimates on the full Lorentz source.

A successful proof along any route must retain the current order of limits:

1. fix all outer scales and costs;
2. prove the finite-count identity on the original physical source;
3. complete the positive physical sum;
4. take the essential-roof, radius, and exact-label suprema;
5. take the collision limsup; and
6. send \(B\to\infty\) last.

## 13. Specialist audit obligations

Even apart from the unresolved final limit, the following load-bearing inputs and passages require independent specialist reconstruction before publication:

1. the original incident-component pairing-sheet construction;
2. the one-copy physical multiplicity convention;
3. common coarea versions at fixed \(m,R,n,k\);
4. the regular weighted derivative estimate used to control total variation;
5. the fixed-window paired and uncut-volume estimates;
6. joint Borel measurability of the endpoint-completed density on the physical sheet space;
7. the endpoint optical denominator and Schur-complement formulas;
8. simultaneous endpoint mechanisms;
9. the weighted use, if any, of the new multi-mark identity; and
10. the inherited scalar equivalence between the raw pointwise theorem and microscopic-source decay.

The finite diagnostics do not certify these continuum statements.

## 14. Presentation and minor requests

The current 18-page standalone exposition is materially clearer than another layer of TeX hooks. The following revisions would further improve verifiability.

1. In Lemma 7.1, state explicitly that the endpoint-completed density is jointly Borel because its endpoint values are one-sided limits of Borel interior evaluations. The rational-partition argument then becomes entirely self-contained.

2. In Theorem 8.1, cite the exact positive denominator formula when asserting positivity of the optical factor at a nongrazing critical endpoint.

3. Immediately after defining \(\mathcal P_B\), restate that the surviving coefficient is \(c-\gamma_B\mathcal V\), not the original coefficient \(c\). The manuscript does say this, but it is central to interpreting the remaining source.

4. Keep the distinction between a pointwise-changing guard witness and a single uniform witness visually prominent in the main theorem statement.

5. If a later v110 workflow completes, record it in a versioned provenance file without altering the freeze-time statement in this report.

6. Continue to distinguish per-itinerary optical estimates from any physical weighted-word sum.

These are not substitutes for the missing persistent-shortage theorem.

## 15. Significance at the requested benchmark

The revision contains technically credible progress:

- a positive payment on the original source rather than only on comparison capacity;
- a full total-variation estimate rather than an endpoint-difference estimate;
- a clean persistence characterization of every surviving coefficient;
- a sharper exact residual comparison;
- explicit optical cofactor signs;
- a positive multi-mark expansion; and
- simultaneous endpoint and uniform-modulus refinements.

These results may form useful components of a strong specialist dynamics or probability paper after independent verification and appropriate reorganization.

For a top-four mathematics journal, however, the current article still has two central deficiencies.

First, its organizing raw pointwise local limit theorem remains conditional on the unproved persistent-shortage limit. Second, the newly proved results are specialized technical reductions inside that unfinished Lorentz-gas program; the manuscript has not yet extracted a broad general theorem or a complete application of comparable independent significance.

Accordingly, the recommendation remains negative at the requested benchmark.

## 16. Final recommendation

**Reject in the present form at the requested top-four benchmark.**

This recommendation should not be read as a finding that the new modules are empty or internally inconsistent. Revision 110 makes a real and mathematically relevant advance over revision 109. In the portions audited, I found no decisive counterexample to the new finite-count variation payment, persistence theorem, residual identities, or optical appendix.

The recommendation follows because the article itself proves that its organizing raw pointwise theorem is equivalent to a persistent guarded shortage estimate which is still unproved. Until that collision-uniform essential-height limit is closed, the main result has not been established.

---

### Status boundary

This report is an author-requested, AI-assisted referee-style assessment. It is not a commissioned report from a journal, an editorial decision, an independent human specialist audit, or a formal proof certificate. It reviews the exact source identified above and adds no author-source modifications.