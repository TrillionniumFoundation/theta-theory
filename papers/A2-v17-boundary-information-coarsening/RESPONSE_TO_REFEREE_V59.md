# Response to the independent A2 v58 report

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Revision:** A2 v59, September 15, 2026  
**Author:** Qian Qi

The addressed memorandum is `reviews/a2-v58-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, frozen at `464209b66aad6ff48b63f054711396fbfd759b64`. It reviews actual mathematical source `92a6d946c98e19c33ebff15997c0116ac158b89d`, rather than its preparation or review-ready commit. The report and its audit ledger were read completely. This exchange is author-requested and AI-assisted; it is not commissioned journal refereeing.

## 1. Disposition and the substantive revision

We thank the referee for accepting the scoped admissible-block proposition and for keeping the acquisition-dependency and anchored-contact corrections closed. The report establishes no new mandatory core repair. We do not reinterpret its unfavorable placement judgment as a false theorem that needs an algebraic patch, and we do not regard a further successful build as an answer to that judgment.

The mathematical issue isolated in R58-M3 is nevertheless a natural question about the principal mechanism: a uniformly invertible highest-degree diagonal does not control the full lower-triangular action derivative. Revision 59 answers a local analytic version of that question by using additional structure of the **actual stationary action**, not by strengthening the diagonal calculation. The new subsection is part of the existing contact-inversion section in both complete entries. It proves a local analytic inverse for the entire graph-to-action map in a specified bounded-holomorphic norm, including the lower-degree couplings. The old smooth, exact-global, differential and statistical theorems are not narrowed or replaced.

The distinction in hypotheses is important. The new estimate controls holomorphic extensions on one fixed small complex disc. It does not infer such control from a finite number of real density derivatives, total variation, or finitely many measurements. It does not prove analytic continuation to an entire obstacle is uniformly stable. Its role is to show that the core variational inverse is an actual local infinite-dimensional coordinate map in a natural strong analytic topology, not merely an invertible list of separate finite jets.

## 2. R58-M1 and M2: admissible blocks and actual smooth factorization

Proposition 12.9, its proof, its fixed-lower-jet comparison and its coefficient-space assertions remain verbatim. In particular, positivity is still used to obtain `lambda_b = r_b exp(-gamma) < 1`; determinant one alone is not substituted for admissibility. The order-uniform diagonal bounds retain their hyperbolic-margin qualification.

The actual-smooth finite-remainder argument and its terminal-envelope identity also remain verbatim. They still justify finite action-jet factorization before coefficient inversion. The new proof uses them only for the finite low-order quotient, not as an unproved order-uniform bound on all functional smooth remainders.

## 3. R58-M3: the complete derivative, not a diagonal inference

The new argument is in `article/23a2_analytic_contact_inverse_v59.tex`.

**Lemma 12.10: a holomorphic function-space construction.** The source constructs half-lines on an open ball in `H^infinity(D_R)^2`, with fixed constant, linear and quadratic contact jets. A uniform complex weighted contraction gives `|x_{b,i}(u)| <= rho^i |u|` for every interior visit. The proof makes explicit why differentiation on `H^infinity(D_R)` is not being assumed bounded: the stationarity equation at an internal site differentiates the graph only at contracted internal arguments. At the initial endpoint it uses the graph's value, not its derivative. Cauchy estimates are therefore taken on protected inner discs. The actual physical arcs remain convex on a common smaller real collar. The lemma does not assume that every perturbed analytic germ has a global periodic continuation.

**Lemma 12.11: the exact envelope operator.** Finite stationary differentiation, including the terminal term, gives

$$
(D\mathscr S(\psi)\eta)_b(u)=\alpha_b(u)\eta_b(u)
 +\sum_{i\ge1}v_{b,i}(u)\eta_{b+i}(x_{b,i}(u)).
$$

The initial multiplier is bounded away from zero. All interior arguments contract. The initial visit is counted once and the internal visits twice. The terminal contribution tends to zero in the analytic function norm before the identity is used. On variations vanishing through order `m-1`, the complete interior sum has norm at most `2W rho^m/(1-rho^m)`. Taylor truncation also gives a finite-rank approximation to this interior operator. This is a compactness statement on the same disc, not a claim that the full derivative improves the radius of holomorphy.

**Theorem 12.12: full local analytic inversion.** Choose one finite tail order `m` making the interior contribution small relative to the initial multiplier. A norm-convergent Neumann series inverts the full derivative on that high-vanishing subspace. On the finite quotient of degrees 3 through `m-1`, the existing actual-smooth triangular formula gives an invertible finite matrix. Solving the finite quotient first and then the tail provides a bounded inverse of the entire derivative. No uncontrolled finite sum with a growing number of lower-triangular factors remains.

A local contraction then inverts the complete nonlinear map. The theorem includes a local two-sided Lipschitz estimate in the fixed-disc analytic norm, bounds for all factorial-weighted coefficients on each smaller disc, and order-independent bounds for the complete linearized finite-jet inverses in **the quotient norms induced by the analytic norm**. These are not unweighted maximum norms of derivatives. The gap and quadratic variables can vary in the finite leading block, using the already explicit leading-curvature inverse.

Thus the abstract lower-bidiagonal control in the report remains correct: a diagonal bound alone cannot prove this result. The new proof uses an additional, specifically variational representation of the actual derivative. It neither labels the referee's abstract matrix a billiard counterexample nor assumes that the compact interior contribution is small on the entire function space. Only one sufficiently high-vanishing tail has to be small.

## 4. R58-M4 and M5: keep the central analytical mechanism intact

The two-ended relative determinant construction is unchanged. The exact normalized cofactor identity, summable endpoint perturbations, protected end compressions, remote-reflection estimates, trace-series telescoping and common-domain integration remain the source of the nonlinear physical boundary law. The new local analytic inverse does not supply a replacement forward probability theorem.

The terminal-envelope proof is now used a second time for a genuinely different estimate: it represents the complete action derivative as a multiplier plus contracted boundary evaluations. This is why the argument reaches beyond the diagonal coefficient response. It does not replace the original smooth statement, which remains useful when no common holomorphic extension is available.

## 5. R58-G1 through G4: observation, global geometry and acquisition

The positive-window and nonzero-anchor hypotheses remain. The new analytic action norm is not called a norm automatically available from conditional observations with arbitrary noise. Exact laws still determine the real action germ; analyticity gives uniqueness of its extension, but does not make extending noisy real data a bounded operation. The original fixed-order density stability and strong-topology window theorem remain separate, unchanged results.

The finite exact global fiber retains both inclusions and every geometric admissibility test. A local analytic inverse of a contact pair does not extend the recovered germ to a whole body by itself or remove finite rotational alternatives. The unknown lattice still follows from the actual integer gain matrix, not an assumed unimodular matrix or a supplied Gram form.

The common-strip differential proof, actual local symmetry branch and model-local scalar coordinates are retained unchanged. The new analytic-germ theorem neither assumes global parameterized analytic supports in place of local graphs nor purports to replace that full-table kernel proof.

Corollary 19.9 remains a substantive application of full Theorem F.47.3. Its sensor, calibration, compact-family, cap and risk hypotheses remain explicitly imported. The updated dependency ledger preserves the eight comparison targets and the one acquisition theorem input. The new subsection has no full-only statistical theorem premise. It cannot produce a uniform charged preparation budget over recording efficiencies that approach zero.

## 6. R58-E1/E2 and D1–D4: contribution and article-level scope

The principal article and the complete technical manuscript remain distinct compiled entries. The new proof belongs to the principal action-inversion mechanism; no additional stopped-experiment section or unrelated inverse problem is appended. The principal abstract and the existing proof discussion now identify the difference between finite smooth inversion and the complete local analytic inverse.

The new theorem is offered as a substantive extension of that mechanism, not as a formal closure of the referee's placement reservation. Its contribution is the use of stationary cancellation and geometrically contracted visits to control **all** local analytic couplings. The contraction principle and finite-dimensional linear algebra used at the end are standard tools, not new general principles claimed by the paper. The result does not make the observation unmarked or finite-dimensional, does not establish equivalence with marked length data, and does not make all later consequences independently exceptional innovations.

The four cited primary records were checked again. The enriched marked-length, analytic open-billiard and association-model settings remain distinguished, as does Florio–Leguil's version-5 correction. No reduction between observation maps, exhaustive priority result, or first-priority claim is asserted. Details are in `LITERATURE_CHECK_V59.md`.

The adverse editorial assessment and the mathematical status of the proofs remain separate. The next referee should examine the protected-domain analytic construction, the envelope operator and the finite-low-jet/high-tail inverse directly. Neither the absence of a defect in v58 nor the finite controls attached here certify the new theorem.

## 7. Preservation and verification

All 121 inherited active paths remain active. Six precisely prescribed amendments concern version metadata, explanatory prose, the new shared input and the current dependency-route name. Their exact originals and the source-matched v58 active manifest are archived under `history/v58-review-baseline/`; 115 inherited paths remain byte-identical in place.

All 574 inherited statement/proof source blocks, including 271 proof blocks, remain verbatim. Counts include shared display copies and are not counts of distinct mathematical results. One shared input adds two lemmas, one theorem and their three proofs. The final three-entry union has 122 paths. The prior headline theorem and its complete proof are not rewritten to suggest that a smooth class has acquired an analytic-norm hypothesis.

The v59 checker verifies these identities and current reference roles. Its exact finite controls test analytic-tail estimates and a genuinely lower-triangular weighted-composition model. Its numerical variational controls solve nine finite stationary chains for polynomial reflecting graphs and compare shape derivatives with the correctly counted envelope. The inherited admissible-block controls remain included. These tests are expressly not proofs of an infinite-dimensional contraction or arbitrary-order inversion.

All three entries are built from one committed source by the version-scoped workflow, with separately retained source identities, products, logs and verification results. The final review-ready ledger records the actual completed build and visual scope; this response does not substitute a future workflow for completed delivery.
