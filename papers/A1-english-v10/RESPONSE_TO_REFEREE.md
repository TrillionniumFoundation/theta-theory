# Response to the A1 v9 referee report

**Revision:** A1 English v10, *Sparse observation algebras and effective memory across exponent collisions*.  
**Controlling report:** `reviews/a1-english-v9-2026-09-06/REFEREE_REPORT.md` at `7a499e3cb32396b18eda869342ec8e9c70d8d028`.  
**Reviewed submission:** `e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5`.  
**New branch:** `revision/a1-english-v10-effective-finite-memory-2026-09-06`.

We thank the referee for distinguishing correctness of the stated mathematical results from the level of significance required by the intended journals. The report and its accompanying technical note do not supply a blocking counterexample to the v9 principal theorem. We have therefore retained the full classification and its proofs, and addressed the significance objection by adding a finite numerical realization theorem rather than enlarging the calibration domain once more.

The principal change is operational. In v9, the codebook and transition functions could contain exact, possibly noncomputable, real data. In v10, a compact-state compilation theorem constructs finite integer transition tables and dyadic output tables from finite approximations to feasible-history states. Applied to the collision-uniform attainable geometry, it preserves the sharp causal memory order. It does not call an exponent-gap oracle, determine rank, or decide whether an additive collision is exact. Numerical precision is set by the state budget, not by the smallest gap.

The source and PDF retain all 42 predecessor named results and all 40 complete predecessor proof blocks. Special-case proofs are reorganized into appendices; nothing is inferred from a label count about mathematical significance. The new proofs are directly present in the English source. The short build script relocates two existing lemmas and the operational definition; it does not generate mathematical arguments.

## E9.1 — The determinant profile and classical finite spectral theory

We accept the referee's distinction. Proposition `prop:exterior-profile` identifies the maximal Vandermonde products with the exterior singular-value scales of the ordinary finite evaluation matrix, with constants depending on the fixed matrix dimension and not on node separation. Its proof factors the matrix into a bounded invertible Newton change of basis, diagonal Leja scales, and a bounded invertible evaluation factor. Inactive columns are completed without inverting zero pivots.

This proposition and the isolated arbitrary-prefix Hermite lemma are explicitly attributed to the referee's technical note and the classical interpolation literature. Neither is represented as a new spectral theorem. The introduction now distinguishes these algebraic facts from four additional requirements: transversality to an attained normalized-product tangent; an acquired-history law retaining failure evidence; a cover of the entire reachable image, not merely a local chart; and causal compatibility of the successive covers.

The new result is `thm:compact-compiler`, followed by `thm:digital-intrinsic`. A finite net of attainable grid histories is evaluated to prescribed accuracy. Farthest-first selection, with the classical approximation argument attributed to Gonzalez, chooses at most M representative indices. Appending each possible finite command code and report to each chosen history produces the offline transition table. At runtime, no state vector, prior-moment oracle, representative history or real-valued transition function is retained. Thus the added assertion is not a restatement of an exterior spectral identity.

## E9.2 — Consequences beyond the collision-tree formula

The collision-tree theorem and the two-parameter arrangement are retained with their original complete proofs. We do not count the technical note's discrete convexity and nested optimizers as a new author contribution. Those deductions remain in the preserved review branch and are not renamed as the main revision.

The additional consequence is that the sharp collision law can be attained before the smallest gap is numerically resolved. Let Xi_N(M,a) be the v9 maximum checkpoint profile. The finite compiler proves

    worst-history regret <= C [Xi_N(M,a) + h^2 + tau^2],

where h is the current-command mesh and tau is the certified offline evaluation error. The l=1 determinant term gives Xi_N(M,a) >= M^(-2). Hence choosing both errors of order (M+1)^(-1) retains the full sharp law, uniformly across collision strata. No individual small scale has to be estimated to make this choice.

Corollary `cor:calibration-precision` controls the finite moment data using the uniform Lipschitz dependence of t^b on a positive exponent b. Corollary `cor:digital-contact` applies the compiler to the retained two-parameter arrangement and arbitrary contact order. Its point is not a further crossover formula: the already established formula is realized by a finite numerical program whose precision has no additional inverse-gap penalty.

The argument involves information unavailable from the tree alone: uniform positive likelihoods, a global attainable cover, stability in commands and state, and an approximation allowance that survives every lossy update. Its editorial weight remains a matter for renewed independent assessment; the response does not substitute an acceptance claim for this theorem.

## E9.3 — What is and is not generalized

The compact-state compilation theorem is formulated for arbitrary finite-horizon compact Lipschitz state systems with finite evaluation data. It is not restricted to a single latent scalar or to monomial coordinates. It transfers a supplied covering order into a finite-table causal implementation without requiring the compiler to know that order.

For the positive sparse experiments, all its assumptions are verified rather than postulated. Formal raw moments give state and command Lipschitz bounds independent of additive gaps. A finite table of moments at formal degree N evaluates every candidate history and query. Prefix evidence at least kappa^n prevents a small denominator after sufficiently accurate numerical approximation. The same original acquisition experiment supplies the lower bound.

The following distinctions are maintained explicitly:

* The original arbitrary-full-support-prior theorem remains unchanged. Effective synthesis from numerical input additionally requires terminating approximation procedures, or supplied finite numerical advice. No procedure for obtaining noncomputable unsupplied data is claimed.
* Constants and arithmetic dimensions may depend on the fixed horizon and prior. There is no new horizon-uniform theorem or uniform conditioning over every full-support prior.
* For J scalar command entries, the finite read-only program has O(M^(J+1) log(M+1)) bits. It need not fit in the log(M) persistent-state budget. Polynomial cost in M is not polynomial cost in log(M).
* Input codes are current-command approximations. For comparison with the memory lower bound, their coding rule is fixed and memoryless, or uses fresh independent rounding. No past-dependent input-naming tape is available. Exact comparison of an arbitrary real command to a rounding boundary is not assumed computable.

These are resource specifications, not retreats from the inherited classification. The new theorem removes exact-real read-only data from the running filter under its declared finite-data hypotheses. It does not assert that every physical apparatus or arbitrary hidden-variable model has the monomial dimension formula.

## P9.1 — Explicit spectral comparison

Addressed in `sections/classical.tex`, Proposition `prop:exterior-profile`, including exact repetitions and the zero singular-value tail. The distinction between ordinary real evaluation matrices and nearby clustered Fourier/Vandermonde results is maintained. The comparison is up to constants, not an equality of maximal minors and singular-value products.

## P9.2 — Standalone arbitrary-prefix lemma

Addressed in Lemma `lem:prefix-hermite`. The proof treats an arbitrary ordered multiset, including nonadjacent repetitions. Prefix divided differences form a triangular unit-diagonal family on polynomials and hence a basis for complete Hermite data. The attribution is to de Boor's Proposition 7 and the referee technical note. The subsequent attained-rank proof still supplies the separate mixed/confluent pairing and normalization calculation.

## P9.3 — One dependency spine, with complete subsidiary proofs

The principal order is: experiment and persistent-state loss; exact attainable tangent; isolated interpolation, confluent positivity and global covering; intrinsic classification; finite numerical compilation. The full observation-algebra, affine, five-/seven-trial, decision-value and mechanical comparisons follow as appendices with their original hypotheses.

Two complete lemma-and-proof blocks and the finite-state definition/loss are relocated by `build.py`. Their original files remain unchanged in `core/`. The compiler checks the Git blob hashes of all ten v9 body files and verifies that all 40 complete proof blocks survive in the compiled document. It also checks all 42 predecessor named results and resolves source references. This is an executable preservation check, not a claim that source identity proves correctness.

## P9.4 — Reproduction and provenance

`V10_DIAGNOSTICS.json` records a fresh local run of `tests/test_v10.py`, with 7,904 passed assertions. The fixtures use exact rational integration with a uniform prior or density 3t^2; calibrations include an exact collision, a gap of 10^(-12), and a separated rational example. They test raw updates against direct product integration, approximate greedy selection, finite transition tables, index-only mutable state, coincident formal labels and grid-external commands. Their finite alphabets and fixed horizon cannot establish the continuum entropy theorem.

`PRESERVATION_REPORT.json` records source comparisons. `BUILD_REPORT.json` records a fresh three-pass pdfLaTeX build, with no undefined references/citations or overfull boxes. The PDF has 48 pages; rendered-page inspection is separate from proof assessment. These are local executions, not a GitHub Actions success. The predecessor author's execution counts and the referee's 3,821-check receipt are preserved as historical evidence and are not counted as freshly rerun here.

The complete new source is committed on the revision branch, together with the reference compiler, tests and this response. No earlier manuscript, referee report, default branch, repository permission or branch protection is modified. The revision is submitted for another referee examination, not described as independently approved.
