# Response to the independent report on A1 English v19

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Revision:** A1 English v20, 7 September 2026.  
**Report:** `reviews/a1-english-v19-independent-2026-09-07/REFEREE_REPORT.md`, commit `59018a3231abb551d93947929f7e9bf0e3ddcd9e`.  
**Reviewed manuscript:** `01abeb689b203ea871b88495d16a826bb4942e16`.

We thank the referee for distinguishing the correct printed containment theorem from the stronger, incorrect description in the introduction and response. We also appreciate the explicit credit given to the rectangular and covariance additions, and the identification of the collision/causal synthesis as the strongest part of the manuscript. This revision addresses the mathematical issue by proving an exact-kernel theorem and addresses the organizational issue by making that synthesis the center of the paper. Every inherited formal statement and proof is retained.

Stable source labels below refer to the complete revised manuscript. This response is an owner-requested, AI-assisted revision record, not an assertion of a journal appointment or an independent certification of the revision.

## E19.1. Exact realization, not just feasible annihilation

The referee's eight-point example is correct. In the notation of the report, requiring `span{sigma}` to be contained in the kernel forces every block imbalance to vanish and therefore also annihilates `j sigma`. The relative-interior condition in the old theorem cannot distinguish the one-dimensional requested subspace from its two-dimensional forced enlargement. We have corrected the introductory and section-opening descriptions of `thm:v19-rank-alternative`. Its actual statement and proof are unchanged. The old response remains available as a historical record under `history/v19/`; the present response supersedes its unqualified statement that each permitted kernel is realized.

The revision does not stop at this correction. Section `sec:exact-kernels` supplies the additional condition and its positive witnesses.

### The product quotient

For continuous finite-dimensional spaces E and F on a compact metric space, and U contained in F, put W_U = span(EU) and V = span({1} union EF). Feasible annihilation by a full-support probability is equivalent to W_U containing no nonzero nonnegative function. Under that condition, choose coordinates [1],[v_1],...,[v_s] on V/W_U. Multiplication by E on representatives of F/U gives a completely specified affine matrix pencil H_U(z).

`lem:kernel-moment-chart` proves that the quotient moment image of full-support annihilating priors is a nonempty open convex set. The proof is explicit: subtract the mean and the L2 projection onto W_U from each v_i. The resulting bounded continuous functions are independent and have a positive definite Gram matrix. Small density perturbations preserve every annihilation equation and give local coordinates through this Gram matrix. Full support is preserved by a strict positive density bound.

`thm:exact-kernel` then proves that U is exactly realizable if and only if annihilation is feasible and the algebraic rank of H_U is dim(F/U). Equivalently, one maximal column minor is a nonzero polynomial on the full affine quotient. This is not merely an existential search for a nonzero minor somewhere on the unknown prior slice: the local-chart theorem identifies a full-dimensional open moment set, so nonvanishing can be tested as a polynomial identity before selecting a prior.

More generally, the maximum pairing rank on the entire constrained slice is the algebraic rank r_U. The maximizing priors are relatively weakly open and dense, and may be obtained by arbitrarily small bounded continuous density tilts of any feasible prior. A grid with r_U+1 values per local coordinate supplies a finite witness test because the relevant determinant has degree at most r_U. This is an algebraic assertion with given real moments, not a computability claim for unspecified moment data. For any prescribed full-support reference probability, a finite-atom mixture witness preserving the entire pairing is also proved. The mixture weight is not asserted uniform.

### Forced directions and an explicit positive classification

`prop:forced-kernel` identifies the common kernel of every prior on the slice as cl_E(U) = {f in F : Ef is contained in W_U}. This multiplication closure is idempotent and preserves W_U. It gives a preliminary necessary test; it is not substituted for the full determinantal condition. In particular, the tests include a one-row/two-column example in which there is no forced nonzero direction but exact zero kernel is dimensionally impossible.

`prop:block-kernels` goes beyond a single counterexample. On {1,...,n} times {±1}, take block-indicator acquisition space and future space R1 plus sigma times the polynomials of degree less than m, with n >= m+1. For nonzero polynomial subspace S, let Z_S be its common zeros among the n block locations. We prove that its forced kernel consists exactly of the polynomials vanishing on Z_S, and the maximum pairing rank is 1+|Z_S|. Exact realization holds precisely when S is the product of the simple root factors at Z_S times all polynomials of degree less than m-|Z_S|.

The witnesses are explicit strictly positive probabilities: all block masses are 1/n, and imbalances are 1/(2n) on Z_S and zero elsewhere. The acquisition likelihoods have a common positive lower bound and the fixed binary query probabilities lie in [1/4,3/4]. For n=4 and m=2, S=span{1} reproduces the report's failure of exact realization. Each S=span{z-j_0} instead gives an exactly realizable one-dimensional kernel in the same positive experiment. Thus the revision retains the counterexample and supplies a classification with positive realizations, rather than turning it into a no-go conclusion about the programme.

`cor:kernel-history-rank` converts the constrained maximum rank to the actual normalized prediction rank r_U-1. Its proof adjoins evidence before normalization and obtains unconditional mass by an inverse chart completed with kernel coordinates, integrating over the whole kernel-coordinate box and retaining the report-word probability. It does not put mass on a lower-dimensional section. Whole-image and causal claims are not inferred from this local statement alone.

## E19.2. Mathematical center, attribution, and significance

We agree with the report's separation of a proof defect from an editorial assessment. A significance judgment cannot be settled by renaming elementary ingredients or counting new statements. The revision therefore does not present separation as new convexity theory, Fourier perturbation as a new orthogonal expansion, or the analytic-arc consequence as a new Smith normal form.

The Banaji–Pantea square comparison and the Müller et al. rectangular sign-vector comparison are retained at their precise locations. The new bibliography entry for de Wolf explicitly identifies the product-character expansion used in the positive sign-cube density. Kaveh–Makhnatch continues to identify the classical analytic-order/singular-value connection. The physical covariance and memory conclusions are not attributed to these sources, and the classical inputs are not claimed as independent discoveries.

The revised contribution statement is centered on the following combination in the positive experiment: actual histories acquire complete Newton–Hermite prefixes with unconditional mass; the entire reachable image has a dimension-truncated anisotropic cover; and gap-free raw-moment updates propagate reachable representatives into one causal finite-state filter. The truncation by attained past dimension enters before quantization. The global upper cover is not inferred from a local chart. The causal recurrence includes accumulated earlier errors and uses no uncharged command tape. Uniformity includes exact additive collisions, with a fixed full-support prior and fixed horizon under the printed compactness hypotheses.

The structural rank theorem explains which dimension conclusions extend to arbitrary compact latent spaces and specified priors. The affine theorem provides the exact physical covariance profile, uniformly through rank loss. The kernel section separates the annihilation equations from exact rank attainability and returns that separation to actual prediction derivatives. These results illuminate distinct parts of the same acquisition–observation problem; none is advertised as replacing the multi-step collision proof.

This is the mathematical case offered for the paper. We retain the intended journal standard but do not claim that the revision, its diagnostics, or its source-preservation checks compel an acceptance recommendation. The next referee should reassess the conclusions and their significance directly.

## Presentation and preservation obligations in Section 7 of the report

The abstract and opening introduction now lead with the collision-uniform checkpoint and causal law. A dedicated subsection explains the three proof obligations and their relation. The monomial transversality and collision proofs precede the general structural and affine classifications in the body. This order makes the principal mathematical argument readable without following the order in which revisions were written.

Table `tab:scope` compares the monomial, structural, affine, exact-kernel, circular, and prior-ambiguity results. It states which conclusions are uniform across degeneracy and which require fixed-rank or domination hypotheses, and separates checkpoint profiles, causal filters, and local rank information. Its resource caption retains post-label query selection, charged persistent labels, known read-only calibration and clock, and the absence of a free command tape. The full integer-budget inverse remains distinct from finite observations of a risk curve, horizon maxima, and uncertainty floors.

All correct mathematical content remains in the complete manuscript. Reordering does not delete or replace inherited proofs. The old introduction, response, source, and receipts remain in an independently anchored v19 snapshot, and the old repository manuscript and review are untouched. The current build verifies all 109 inherited proof blocks and all 112 inherited formal statement blocks byte for byte. The revised compilation adds five complete proof/statement pairs. The original v17 source independently anchors the inverse theorem even in standalone preparation.

## Executed checks and their limits

The v20 diagnostic suite uses exact symbolic and rational calculations, imports no repository theorem code, and explicitly raises on failure even under Python optimization. It checks the eight-point counterexample, all four exact one-dimensional alternatives in that experiment, quotient-pairing identities, local Gram and tilt identities, positive witnesses, 37 root-saturated block instances and their actual covariance ranks, a nonsaturated polynomial subspace, and empty/zero-dimensional cases. Its initial execution passed 987 explicit checks. These are check calls, not 987 theorems.

The full validator reruns the inherited suites as well, performs an actual corruption/restoration test of the inverse source, and compiles the complete manuscript. The actual final counts, PDF pages, source hashes, and build outcome are recorded in `validation/EXECUTION_REPORT.json`; this response does not substitute an anticipated outcome for that receipt. The referee's own earlier 2,445 checks are credited as reported in the controlling review, not counted as newly executed author checks here.

No formal proof assistant, independent journal referee, exhaustive global novelty search, or optimizer over all possible encoders is represented by these execution records. The new proofs are supplied in full for mathematical review.
