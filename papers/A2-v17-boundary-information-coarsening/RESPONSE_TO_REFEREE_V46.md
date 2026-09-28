# Response to the independent report on A2 revision 45

**Revision:** A2 v46, September 14, 2026.  
**Author:** Qian Qi.  
**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*.

The addressed report is `reviews/a2-v45-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md`, on review branch `review/a2-v45-independent-harsh-top4-2026-09-14`, frozen at `0614a20bbba6312830b5523b806ddc726a6333f1`. Its reviewed mathematical source is `2f064b86b4e071d24ad671f4dc652d7de32a56a4`; the reviewed main has 235 pages and the companion seven. These are different identities and have not been conflated.

We thank the referee for distinguishing favorable mathematical findings from the adverse editorial assessment, and for withdrawing the superseded special-realization objection. The revision retains the full earlier article, all three mathematical parts and auxiliary proofs, and the complete companion. It makes the requested wording correction and proves an additional conditional quantitative theorem whose input consists of finitely many quantized transverse-law probabilities. The new mathematics is in Section 19, with its principal statement also in introductory Theorem 1.4. Proof provenance and execution evidence are recorded separately from the mathematical article.

## R45-P1: zero-net-gain backtrack

The proof of Theorem 18.7 now says “zero-net-gain backtrack $ee^{-1}$.” The correction does not assume an individually zero-marked edge, add a measured channel, or change the rank-two gain matrix. It applies also when N=1 and both selected channels are nonzero-marked self-loops. The remainder of this source module is byte-for-byte unchanged. The original is archived under `history/v45-review-baseline/article/23j_generic_finite_channel_rigidity_v45.tex`.

## R45-C1: preserve the generic theorem actually established

The universal clear-skeleton theorem, the N+1-channel generic determination theorem, their persistent-design quantifiers, and the mechanism-specific channel minimality statement are retained without additional assumptions. Obstruction descent still treats tangencies as obstructions. The two selected gains are only required to be linearly independent, not unimodular; the reconstruction uses the actual matrix M. The original genericity topology remains the relative C² topology on real-analytic supports. We do not reinterpret genericity as a probabilistic claim or turn existence of a selected design into unmarked design discovery.

## R45-C2: preserve the analytical proof mechanisms

The relative determinant estimates, nonlinear weighted half-line inverse, finite-truncation envelope differentiation, smooth finite-remainder filtration and anchored density cancellation are unchanged. The new finite Bellman calculation uses the already proved smooth filtration; it does not substitute formal power-series notation for that result.

Lemma 19.2 adds a finite algorithm for the lower-order terms of the jet inverse. Splitting an actual stationary half-line after its first flight gives a Bellman identity and a scalar stationary equation. The coefficient matrix at order n is expressed as `(I-B_n)^{-1}(I+B_n)`, equal to the inherited determinant-one block. The lower-order remainder is obtained by solving only through degree n-2. The omitted degree n-1 orbit term changes the stationary value at order 2n-2, which is beyond n. Thus a chosen finite-order Lipschitz constant is bounded by a finite differentiation and arithmetic procedure rather than by an unspecified inverse modulus.

## R45-E1: a new observation-level quantitative consequence

The report correctly distinguishes exact analytic continuation from a quantitative inverse for noisy laws, and complete-image registration from that preceding inverse. Section 19 supplies the latter under explicitly quantified analytic and forward bounds. It does not relabel the earlier image estimate.

**The measured error.** Theorem 19.5 starts from gap errors and the l¹ discrepancies of finite histogram vectors of the signed transverse endpoint laws. It does not begin with a C^m error of a measured density, known support coefficients, a registered image, or longitudinal positions. The mesh term is necessary: identical cell probabilities need not imply identical densities.

**The proof.** Lemma 19.1 first bounds the interior L¹ density error by histogram error plus mesh bias and then, using known finite-order forward bounds, controls its C^m error. Lemma 19.2 propagates that error through amplitude cancellation, the finite contact inverse and graph-to-support conversion. Lemma 19.3 continues a finite anchored support jet around the whole real-analytic boundary with an explicit strip-dependent exponent and geometric tail. Lemma 19.4 uses a B\'ezout identity for any finite nonzero harmonic witness with gcd one, followed by the same common-frame tree and cycle cochain. This yields the complete labelled table, the unknown Euclidean lattice and its Gram matrix.

**The new quantitative priors.** A common bounded holomorphic strip, forward density derivative bounds, positive anchor/density/contact margins and a finite nonvanishing asymmetry witness are printed in the class definition. They are not measurements of the unknown shapes. Such witnesses exist at every properly asymmetric analytic table, including bodies with vanishing second or third harmonics. The quantitative neighborhoods are bounded holomorphic-support neighborhoods, not arbitrary C² neighborhoods. No such priors have been inserted into the earlier qualitative theorem.

**Finite resolution and samples.** Equation (19.17) gives a finite choice of jet order, probability accuracy and mesh for any positive target error. The number of scalar probabilities may grow with accuracy; exact recovery from a fixed finite list is not claimed. Corollary 19.6 provides an empirical categorical confidence construction with explicit sampling error and exponentially small even-flight bias. Its preparation cap charges failed attempts. Concentration is applied to the uncapped stream of successful marks, and cap failure is added separately. We do not condition on cap completion and then assert iid sampling.

**The sensor distinction.** This theorem's reconstruction transcript retains only onset estimates and quantized transverse categories on a calibrated selected design. The direct longitudinal graph-interpolation estimator is not defined on this transcript. The existing richer position pilot and benchmark remain in the article, with their original sensor and budget. Section 19 does not claim that calibration or unmarked channel discovery can be performed from the compressed transcript alone.

**Conditioning and scope.** The displayed continuation exponent is conservative and the sufficient jet order can be enormous. No sharp minimax rate, practical algorithm for searching an arbitrary analytic class, or unrestricted Lipschitz inverse is asserted. Compactness can supply a measurable approximate selector, but is not used to define the quantitative inverse modulus. The finite-order accuracy prescription, not an infinite minimization over conditioning constants, is enough for the theorem.

These are mathematical additions to the observation-level conclusion, not a request that the referee count pages or certificates as evidence of significance. The classical cell interpolation, continuation and categorical concentration ingredients are identified as such; the contribution is their quantified composition with the nonlinear billiard inverse and intrinsic periodic gluing. Whether this contribution warrants the requested journal placement remains an independent editorial judgment. It is not marked “closed” by an author checklist, and this response claims neither journal approval nor an exhaustive priority result.

## Literature and preservation

The comparison with marked/enriched length spectra remains observation-specific. No reduction between those observations and selected endpoint laws is asserted. The version-sensitive earlier bibliography is retained; Trefethen's 2020 article on the ill-conditioning of analytic continuation is added for context, while the continuation lemma is proved in full. The article does not claim novelty for the three-circles principle or empirical-frequency concentration.

The native input graph contains the same 98 inherited main files and two new modules; the companion still has its single complete source. All 226 inherited theorem-style environments, all 22 remarks, and all 466 matched mathematical environment blocks are retained, with the single explicit P1 proof-text substitution. Seven theorem-style environments are added, including the introductory statement. The source audit and independent finite-series diagnostics are reproducible under both ordinary and optimized Python. They are not mathematical correctness certificates; a separate external referee remains necessary.
