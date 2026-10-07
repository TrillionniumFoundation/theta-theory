# Response to the substantive referee: A2-DYN revision 30

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v30-referee-response`  
**Controlling report:** `reviews/a2-dyn-v26-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Report commit / blob:** `20337e845157a833fe770687ea98f337788fa586` / `f75e48fa7276be7be654c61afe3cc276ba44d514`  
**Immediate qualified author source:** `18c3f14ff7e7275cd7a2955bcbe58bd89ada940f` (v29)  
**Frozen baseline paper tree:** `512509ff9d5a3141e3f53183bafe7fba61b4eebb`  
**Date:** 7 October 2026

We thank the referee for keeping the prescribed-count complement, common signed raw correction, denominator and event-replacement questions distinct. The latest inspected review branch contains the v26 report. Revisions 27--29 have subsequently advanced the signed-window and stationary physical-window arguments. We continue from the qualified v29 source, not from the older reviewed article, and do not attribute an unlocated later assessment to the referee.

The principal new result is Theorem U: the whole stationary physical path, conditioned on the exact endpoint windows of Theorem T, converges to its nondegenerate Gaussian bridge. The same limit holds under all four endpoint descriptions on the same stationary space. The proof also establishes actual denominators and conditioned path laws for a concrete class of multiple-time physical indicators. This closes a limitation explicitly retained in the preceding author response: comparison of conditioned measures had not identified their common functional limit, and an additional path-weight denominator had been assumed rather than proved for a specified class.

The title, triangular family, actual section, joint record, and raw microscopic endpoint remain unchanged. Every inherited theorem and proof module is retained. We do not adopt a change to a specialist-paper topic. The new theorem is an additional proved component of the original conditioning pipeline, with its exact resolution stated.

## A. Complete fixed-return frequency complement

The new Fourier theorem is for finitely many consecutive deterministic collision blocks and a genuinely integrated endpoint frequency. It extends the collision estimate used by Theorem T; it is not relabeled as a new prescribed-return-count Fourier domain.

For any fixed number of blocks, including blocks of length zero, and block frequencies `u_l` satisfying `max |u_l| <= m^(1/200)`, Theorem `thm:multiblock-collision-band` proves

`integral_{|v|<=C m^(9/100)} |C_m(v;u)-G_m(v;u)| dv <= C m^(-3/280) sqrt(log(2+m))`.

The constant is uniform in the block boundaries and the allowed growing path frequencies. These are the two additional uniformities needed by the functional conditioning argument. The physical endpoint-frequency radius is `C m^(-41/100)`; the physical block-frequency shifts are at most `m^(-99/200)`.

The central proof explicitly handles short blocks. After expanding the chronological product, an adjacent mixed factor is rewritten as `N(z)^l Pi(w)=N(z)^l(Pi(w)-Pi(z))`, with `N(z)^0` interpreted as `I-Pi(z)`. This prevents an unjustified exponential estimate on a short or zero block. The all-complementary term is exponentially small because the total collision length is `m`. The projector differences, cubic remainder, initial-density smoothing, observable smoothing and covariance change are all integrated with the original four-dimensional volume.

On the outer collision annulus, the residual order is fixed at `P=40`, the spectral order at `Q=29`, and the fine and coarse smoothing exponents are unchanged. Additional block boundaries increase the fixed number of operator factors but do not create a count-dependent word. Every segment frequency has size comparable to the endpoint frequency, so the sum of segment damping exponents controls `|v|^2`. All residual block numbers `1<=b<=40` are included. The largest moment power remains `-1/25`, with margin `41/1400` over the central rate.

This improves the weighted collision input needed for physical conditioning. Balanced unresolved fixed-return directions, compact/peripheral frequencies, growing roof frequencies and the full far-roof splice remain required for the microscopic raw theorem. The inherited shape-adaptive prescribed-count domain and exact cutoff-transport identities are unchanged.

## B. The common signed raw remainder

The v27 signed-window bound and the v26 coherent transport theorem are preserved. Neither is promoted to a pointwise or absolute raw-remainder estimate. The new path theorem uses the already proved actual window denominator and a joint Fourier comparison. It does not estimate `n^2 ||R_chi||_infinity`, differentiate the extracted coarea density, or infer isolated edge smallness from cancellation.

The referee's direct signed-correction route remains a well-defined target. No proof of that microscopic bound is claimed in this revision.

## C. Long-time preparation and derivative growth

The entire finite-count power--logarithm extraction and second-derivative framework is retained. The new proof uses fixed collision moments, not an inverse-coarea derivative estimate at a linear cutoff. It supplies neither a bound for `A_2(n,L_n,R,w)` nor a replacement far-roof estimate strong enough to eliminate that responsibility. Fixed high moments are not represented as raw-density regularity.

## D. A proved weighted denominator and a conditional functional limit

### D.1. Endpoint-window comparison with path frequencies

Proposition `prop:window-conditional-characteristic` treats arbitrary consecutive block increments jointly with the original terminal box of standardized half-width comparable to `m^(-2/25)`. It augments the three endpoint coordinates by a fourth coordinate, truncates that coordinate at `m^(1/400)`, and uses the endpoint-safe four-dimensional envelopes. No trace of an `L1(R^4)` Fourier estimate is taken.

An oscillatory numerator cannot be bounded above and below by order inequalities. The proof instead uses the pointwise modulus-one bound to control the envelope replacement by the unweighted envelope excess, and uses the Gaussian marginal to dominate the weighted Gaussian endpoint measure. The exact conditional characteristic function is then compared to the Gaussian bridge increment formula, uniformly even for test frequencies of order `m^(1/200)`. Its rate is `m^(-23/2800) sqrt(log m)`.

### D.2. Tightness with the rare denominator paid

Finite-dimensional convergence alone does not prove the claimed bridge. Theorem `thm:collision-window-bridge` therefore provides a separate tightness proof.

A finite trigonometric tail test converts the uniform conditional characteristic estimate into an increment probability bound. Three collision blocks suffice, independently of the time interval. On dyadic levels through `J_m=floor(log_2(m)/200)`, thresholds decrease as `2^(-j/8)`. The largest probe frequency has order `m^(1/1600)`, strictly within the permitted budget. The accumulated Fourier error is `m^(-9/2800) sqrt(log m)`, while the Gaussian part has a summable dyadic tail.

Inside the finest cells, the fixed 128th collision maximal moment is used under the bounded initial density. Dividing the union bound by the actual endpoint probability `>=c m^(-6/25)` leaves `m^(-3/40)`. Thus the argument does not assume that unconditional tightness survives conditioning on a vanishing-probability event. All orders and grids are specified in the manuscript.

### D.3. Explicit multiple-time physical selectors

The limiting law is

`B_{V_R,xi}(s)=s xi+V_R^(1/2)(W(s)-s W(1))`.

For fixed distinct interior times `s_l` and fixed bounded boxes `D_l` with nonempty interiors, the event uses the actual physical observations

`D_t = intersection_l { t^(-1/2) V_R(t s_l) in D_l }`.

The new denominator is

`P_R(D_t intersection A_t^j) = 8 t^(-6/25) g_{V_R}(xi) b_R(xi;s,D) (1+o(1))`.

Here `b_R` is an explicitly displayed finite-dimensional Gaussian bridge box integral. Its covariance blocks are `(min(s_l,s_k)-s_l s_k)V_R`, and its value has a positive uniform lower bound for bounded `xi`. This lower bound follows from uniform ellipticity and the nonempty box interiors; it is not an additional unverified denominator hypothesis. The exact indicator need not be a single-return BV function.

The physical path conditioned on this event converges to the Gaussian bridge restricted to those boxes. The manuscript also states the corresponding result for fixed bounded continuous path weights, with the precise positivity condition when the weight is not a concrete cylinder selector. Arbitrary rare or count-dependent path weights are not silently included.

## E. Relative comparison on one stationary probability space

Lemma `lem:whole-physical-clock-coupling` upgrades the retained observation coupling to the whole physical path. A union over deterministic integer physical times, followed by bounded increments between them, gives a supremum error `O(t^(-1/8))` outside probability `O_P(t^(-P))` for every fixed `P`. Short initial times are bounded directly. Under the endpoint conditioning, the error probability is explicitly divided by the denominator and remains `O_P(t^(-P+6/25))`.

The outgoing collision marginal is still the exact bounded density `tau_R/mean(tau_R)`, not the unbounded entrance roof bias. The same physical trajectory, section origin and elapsed age are retained throughout. Theorem `thm:stationary-physical-bridge` first proves the bridge under the collision endpoint event and then uses the already proved conditional total-variation comparison to transfer it to the prescribed-return, last-return and actual physical endpoint events.

For the concrete multiple-time selector, intersecting both endpoint events with the same `D_t` only reduces their symmetric difference. Dividing by the newly proved cylinder denominator retains the rate `t^(-23/2800) sqrt(log t)` for conditional initial total variation. The selected physical event has therefore both its own denominator and a relative comparison, rather than merely an absolute clock bound.

The endpoint width remains the original Theorem-T width `t^(21/50)`. This is not a fixed-label microscopic denominator. The original raw physical event, full weighted complement and pointwise common correction remain unchanged targets.

## F. Specialist verification, source identity and presentation

The two new proof modules import no additional external theorem. They use the retained collision splitting, mean-preserving BV approximation, fixed-order damping and moments, endpoint-safe envelopes, stationary normalization and event comparison. Independent review should focus on the mixed-projector identity at zero-length blocks, multiblock residual expansion, oscillatory envelope replacement, the uniform growing test-frequency budget, conditional fine-grid division and whole-clock coupling.

All twenty presentation comments continue to be respected: sharp sets and smooth cutoffs, both frequency scales, fixed orders, connected residual terms, the actual count coordinate, the signed identity before norms, weight-class distinctions, collision versus induced Cesaro covariance and execution versus proof evidence remain explicit. The main-text roadmap now connects Theorem T to the new Theorem U. The optional domain diagram is not used to replace any estimate.

All 60 inherited core files, 59 inherited Python files, 787 old mathematical labels and the bibliography are preserved; core and Python files are byte-identical. Five exact main-article edits add revision identity, the abstract addition, Theorem U, its two source inclusions and the roadmap. The exact edit ledger and manifest record these changes. The inherited verifier was separately run against the qualified v29 baseline before modification.

The final qualification is a read-only exact-SHA build of ordinary committed source, with normal and optimized finite diagnostics, native TeX, page rendering and dynamic hashes. These checks do not certify the continuum path argument or journal acceptance. The new conditional path theorem is submitted for substantive review as an advance within the same raw mixed-density program.
