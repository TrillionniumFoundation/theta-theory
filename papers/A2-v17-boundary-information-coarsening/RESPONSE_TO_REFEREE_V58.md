# Response to the independent A2 v57 report

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Revision:** A2 v58 · September 15, 2026 · Qian Qi

The addressed report is `reviews/a2-v57-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, frozen at `e14138660e716daf60471f3b98e8f1d30cb61a34`. Its actual mathematical source is `e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6`, not the preparation or review-ready commit. We read the full report, its continuation and its audit ledger. This is an author-requested AI-assisted exchange, not a commissioned journal evaluation.

## 1. Disposition and mathematical revision

We thank the referee for closing R56-C1 and the anchored-contact wording, and for evaluating the separately compiled principal article on its actual proof architecture. Those points remain closed. The report identifies no new mandatory core repair within its stated coverage. We do not recast its unfavorable significance judgment as a false theorem or as a demand for another stopped-experiment result.

The present revision strengthens the original contact-inverse mechanism at precisely the place identified in R57-M3. The new **Proposition 12.9** is part of the existing signed-contact section in both entries, and its conclusion is incorporated into **Theorem 1.1(3)** of the principal article. It proves that the geometrically admissible highest-degree matrices and their inverses are uniformly bounded in degree, and that both approach the identity exponentially. The proof also gives an order-independent two-sided estimate for actual smooth pairs with identical lower jets, and places the block-diagonal statement on an explicit factorial-weighted coefficient space. No unrelated probability section or additional principal global theorem is introduced.

The uniform matrix estimate and the observation that positive curvature constrains the shape factors are credited to the v57 memorandum in the new proposition and both bibliographies. The actual fixed-lower-jet estimate, coefficient-space consequences and explicit separation of the strictly lower-triangular part are developed here from that estimate and the inherited smooth factorization. These are consequences of the same geometric calculation, not separate claims of a new general inversion principle.

## 2. R57-M1/M2: preserve the relative limit and actual-smooth factorization

The complete two-ended relative proof in `v4/10_boundary_layers.tex` and all existing statement/proof blocks in `article/23a_signed_endpoint_rigidity_v27.tex` are unchanged. The latter receives only an input of the new final subsection. The finite envelope, terminal contribution, actual functional remainder and signed homogeneous isolation therefore precede the new use of the highest-degree matrix exactly as before.

In particular, the proof of the new actual-smooth comparison invokes the existing finite-jet factorization before using `Delta s_n = M_n Delta q_n`. It does not assert that an arbitrary smooth graph equals its infinite Taylor series. The relative amplitude theorem retains fixed-order smooth-family bounds, the trace-norm endpoint localization, compressed Green comparison and normalization before division by the exponentially small twist. No new order-uniform derivative estimate for that forward theorem is stated.

The strengthened headline theorem's proof map now refers separately to the old relative/smooth proofs and to Proposition 12.9. Its former general sentence about not asserting an infinite-order estimate has been made specific: the block estimates are uniform in degree, whereas the nonlinear smooth estimates and reconstruction still have their separately prescribed finite-order hypotheses.

## 3. R57-M3: admissibility, uniform blocks, and the location of conditioning

Put `t = exp(-gamma)` and `theta = (1+t^2)/2`. The decisive geometric identity is

`r_b = c/c_(1-b) < c`, hence `lambda_b = r_b t < theta < 1`.

It uses `c_b = 1+g kappa_b > 1`, not determinant one alone, and does not require equal curvatures. The proof writes both matrices explicitly, with opposite signs on the off-diagonal entries of the inverse. Their absolute row sums give

`max(||M_n||_infinity, ||M_n^(-1)||_infinity) <= (3+t^6)/(1-t^6)`

and

`max(||M_n-I||_infinity, ||M_n^(-1)-I||_infinity) <= 4 theta^n/(1-t^6)`

for every `n >= 3`. A positive lower bound on `gamma` gives uniform constants and a common exponential rate, without a separate upper bound on the curvature ratio. The estimate is not uniform as the hyperbolic margin tends to zero.

For two actual smooth graph pairs with the same gap and equal jets through order `n-1`, the lower-order remainder is identical. Thus the difference in degree `n` satisfies a two-sided maximum-norm estimate with the same degree-independent constant. This is the direct geometric application of the bound; it preserves odd terms and the anchored-contact convention.

For the sequence space with norm `sum_(n>=3) R^n ||x_n||_infinity/n!`, the blockwise operator is a bounded isomorphism without a coefficient-radius loss. Its difference from the identity, and that of its inverse, maps into the space of radius `R/theta`; truncating either correction after degree `N` has operator error at most `4 theta^(N+1)/(1-t^6)`. The proof sums absolute coefficient estimates; it does not presume that arbitrary sequences are realized contact jets of a globally admissible table.

The manuscript then identifies the precise remaining algebra: at fixed leading geometry, the complete finite derivative is `L_M = D_M + N_M`, with `D_M` block diagonal and `N_M` strictly block lower triangular. Its inverse contains the finite sum of powers of `-D_M^(-1)N_M`. The new bound controls `D_M^(-1)`, not that sum. Neither the lower-jet remainders nor the density-to-jet operation nor analytic continuation is thereby bounded uniformly in order. This distinguishes a proved coefficient-space diagonal statement from an unproved full nonlinear analytic inverse.

The finite controls include admissible unequal-curvature matrices and an inadmissible determinant-one comparison that violates the bound. They also verify a triangular map with identity diagonal and rapidly growing inverse row sums. These controls explain the scope of the inference; the latter is an abstract algebraic comparison, not a billiard counterexample.

## 4. R57-M4/M5 and the existing global statements

The centered density and interior-window inverses are retained verbatim. Their nonzero scalar anchors, positive density margins, strong finite differentiability topology, visible critical lines, unknown-origin conventions and separate recording nuisances are not altered. In particular, a coefficient-space statement about the diagonal cannot turn total variation into arbitrarily high derivative control.

Theorems A/B, the clear skeleton, finite symmetry and both fiber inclusions, unknown-lattice cochain, graph/support lemma, differential kernel and model-local scalar coordinates retain their statements and proofs. A fixed positive hyperbolic margin in Proposition 12.9 is a condition for its uniform constants, not a newly imposed hypothesis on exact global determination. No lattice metric or inter-channel pose is added to the datum.

## 5. R57-A1–A3: acquisition remains a declared additional input

The corrected Corollary 19.9 and its complete application proof are byte-identical. It remains an application of full Theorem F.47.3 under its compact analytic, physical-record and uniform-margin assumptions. The acquisition theorem is not a premise of Theorems 1.1, A or B. The current dependency ledger preserves eight background/comparison targets and one substantive theorem target and refreshes their source locations. Its roles are reading-derived declarations, not a semantic certification by a token scanner.

The fixed-order physical-estimation source is unchanged. The finite tests and sample target are chosen before the final flight number; the pilot then uses that final flight. Concentration concerns the uncapped fresh successful streams conditional on the pilot, and preparation-cap failure is charged separately. The increasing-order budget policy executes its selected stage afresh. None of these statements is replaced by a block-norm estimate.

We preserve the distinction drawn in R57-A3: compactness supplies existence of separation constants, libraries and inverse moduli, not an effective universal computational bound. The diagonal improvement does not provide a minimax rate, a table-independent finite observation vector or uniform analytic continuation. The manuscript's acquisition statements remain positive uniform consistency results under their own hypotheses.

## 6. R57-E1/E2: contribution and literature

The principal article continues to lead with the relative normalization and actual-smooth inverse. The strengthened matrix statement is presented as a refinement of that inverse, not as a substitute for its main analytical mechanisms. The additional proof is in the existing contact section; the full statistical corpus remains separately available and is not restored to equal prominence in the principal article.

The leading-data comparison family remains unchanged: its nonlinear law distinguishes geometries that its leading quadratic threshold record cannot. It is not a pair with equal complete marked length spectra, and is not used to infer a reduction between different observation maps.

Primary records were rechecked on September 15, 2026. Finamore–Leguil uses enriched marked length data for finite-horizon Sinai billiards; the definition and Theorem A were also inspected in its PDF. De Simoi–Kaloshin–Leguil concerns its analytic open-billiard class with the stated non-eclipse and symmetry/genericity assumptions. Osius supplies association-model background rather than billiard reconstruction. The cited fifth version of Florio–Leguil expressly removes the earlier affected geometric assertion and retains dynamical results. The manuscript does not claim that these observations are equivalent or that this targeted check establishes first priority. Exact records and scope are in `LITERATURE_CHECK_V58.md`.

We maintain the original global and local results and their full proofs. The refinement corrects the possible impression that the isolated admissible blocks are the source of an all-order loss. Whether the relative/smooth mechanism and its consequences warrant the requested journal placement remains for independent assessment; no revision count, finite diagnostic or completed build is offered as a resolution of that judgment.

## 7. Preservation and review package

The complete principal, full technical and two-collision entries are retained. All 120 inherited active source paths remain active; the shared new subsection gives 121 in the union. Seven precisely amended input originals and the v57 native manifest are archived under `history/v57-review-baseline/`. The 113 other inherited paths remain byte-identical in place.

All 572 inherited statement/proof blocks remain present. Of these, 570 are verbatim; only Theorem 1.1 and its proof map are strengthened. One proposition and proof are added. Counts are per source path, including shared display copies, not counts of independent theorems. The old dependency correction, the full technical corpus and the companion are not deleted.

`tools/check_revision_v58.py` checks these identities, all three active graphs, preserved labels, bibliography resolution, declared cross-document roles, and exact finite block controls. Native products are compiled from the actual committed source and retained in Git with hashes. The final `REVIEW_READY_V58.md` records the completed build identities, warnings and actual visual scope. These operational records are separate from proof and journal evaluation.
