# Response to the latest v29 referee report — A2 v31

Paper: Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*. Report: `6444b57768313ac68978b3ee04a428b4832ccb6e`, blob `d5e4be543ceb354341e01897fda83532707b1481`. Reviewed author: `b81664d3961cdbad58563f37dcaed03288de199e`. Immediate baseline: v30 at `c01118b11779b6161cc34e311f840e5ab36a019c`. Revision date: 4 October 2026.

We thank the referee for separating validity from information-content and venue judgments. This further revision builds on v30 rather than relabelling its completed corrections as new. It retains the collision-law topic and earlier theorems. Its main addition is recovery without an almost-sure common directional cone: finite mean exit replaces finite deterministic stopping, and the resulting pooled-direction experiment is implemented on a fixed grid with rational enclosures. No new v30 referee report is presumed.

## 1. Capacity, morphology and probing comparisons

Sections 7–8 preserve the v30 endpoint-excluded capacity identity and theorem-level comparisons with Matheron, Molchanov, X-ray and wedge probing. We do not attribute novelty to the general use of hit/no-hit probes. Sections 9–10 additionally credit Lawler–Limic and Bertsekas for classical stopped-martingale, Green and value-iteration ideas. The new application concerns measured signed forcing, two different unknown zero sets and finite local acquisition; it is not a new general Bellman or potential-theory principle. The sources and comparison limits are in LITERATURE_AUDIT.md.

## 2. Attempted-solid-start normalization

The abstract, opening reciprocal theorem, Section 9 protocol and Theorem 10.1 state that solid starts and free misses both produce zero and remain in the denominator. Direction randomization does not alter this convention. Conditioning on successful free preparation is a different experiment and is not assumed to yield the same forcing.

## 3. One-bit output and spatial input complexity

The abstract and Theorem 10.1 keep one-bit output next to O(nu^-3) spatial centers, localization sigma proportional to nu^(3/2), and the attempt count. At a center only two pooled means are required, without direction-resolved statistics. The controller still implements a known displacement distribution and the translated reverse joint preparation. The exact continuous-law result is a functional statement on spatial commands, not two scalar observations or a finite quadrature oracle. Four atoms and exact grid shifts give the separate finite implementation.

## 4. Mean stability versus input calibration

Theorem 9.2 proves ||u-u'|| <= H ||g-g'|| for physical candidates with different zero sets. It stops at each candidate's own zero, not a supplied reference set. This scale/depth-independent comparison does not apply to arbitrary noisy iterates: their bound is a geometric tail plus n times forcing and update errors. Theorem 10.1 uses a fixed prior-dependent depth adequate for occupation thresholds.

The unchanged position/timing/angle estimate still costs inverse localization scale. The pooled theorem permits mean bias 1/(512 n_*), with sufficient displacement error ell+tau+t alpha <= c sigma/n_*. Reciprocal-law total variation has a separate bounded-operator estimate. Calibration is independently assumed, never inferred from bits. Scale-independent inverse conditioning is not scale-independent apparatus tolerance.

## 5. Known positive patch margin

The opening theorem and Theorem 10.1 explicitly include known eta, bounded periodic presentation and smoothness priors. Local identification and mean exit require neither periodicity nor eta. Uniform finite primitive-period decisions use the unchanged two-sided patch test and rational locking under eta. The older unknown-margin pointwise conclusion and symmetry-jump example remain active. No observable uniform stopping certificate for unknown eta is asserted.

## 6. Rational relations and real coordinates

The finite result identifies bounded-denominator relations in an independent-pair basis; real Euclidean basis coordinates are estimated. Rational Bellman intervals concern the local scalar stage, not exact real geometry. The later smoothing stage retains its independently specified certified-evaluation model. Equation (9.10) is a sharp finite killed-Dirichlet Green norm, not a physical minimax lower bound.

## 7. Existence versus effective reconstruction

Theorem 4.1 remains an existence regularization. The constructive v30 route in Theorem 6.3 is retained separately. The new Theorem 10.1 realizes pooled directions through four exact lookups per node, with no continuous integration oracle, randomized path-tree enumeration or infinite-dimensional candidate search. Proposition 9.4 justifies killing outside a fixed enlarged aperture at every iteration depth. The supplied rational interval CLI has explicit input validation, adversarial tests and a runnable synthetic example. Its occupation enclosures remain conditional on the forcing/confidence and survival hypotheses.

## Further mathematical content, preservation and qualification

Lemma 9.1 gives the quantitative diameter-to-variance exit bound. Corollary 9.3 extends identification to every nontrivial bounded law by a positive-probability cone, rather than an almost-sure cone; constants are displayed and can be large. The symmetric two-site example now has convergent recovery despite no finite exact termination. This extends, rather than contradicts, the earlier finite-stopping theorem.

All nine v30 core files remain active and unchanged. The exact complete v30 tree and nested earlier material are supplied at retained/v30. No original manuscript or review is overwritten; no count-germ or passive spectral theorem is inferred. The response does not equate a finite check count with top-four editorial significance.

The actual local primary run passed 8,513 finite math/source and 49 contract checks with normal/optimized agreement and a warning-free 26-page build. It records source-content execution. The independently read successful v30 thirteen-document run is historical only. The new exact-SHA workflow declares fourteen documents, delegates unchanged inherited validators, and records actual failures or success. Its own receipt, not a workflow definition, determines hosted qualification. Mathematical review, apparatus calibration and editorial evaluation remain separate.
