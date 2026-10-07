# Response to the external referee: A2-DYN revision 35

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v34-external-top4-review-2026-10-07/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `b4ea180550cd805fba88019e52d0b1a54ca8eef1` / `776a78aaecf82ea2dc92cd661e49c8bddf58e522`.  
**Reviewed author SHA:** `882035928dbf3a0c7fe079ec2a7813ab9b921d65`.  
**Frozen author paper tree:** `b6457e9d07e3efaf4418e1f48143fc0e07333158`.  
**New article:** `papers/A2-DYN-v35-referee-response/main.tex`.

We thank the referee for recognizing that revision 34 evaluates the original stationary singleton, rather than merely representing its Fourier complement. This revision addresses the new report, not the obsolete objections to revision 13. It preserves the title, the triangular mechanical setting, the actual four-coordinate return record, and its full raw mixed-density target. It expands the operator argument and develops its geometric scope beyond the circular parameter line. The new results have complete proofs in the article; they are not assertions made only in this response.

## R1. Independent specialist proof audit

No independent human audit has been obtained in this author revision. A source build is not represented as one. `SPECIALIST_AUDIT_MAP.md` identifies the exact continuum inputs, the new proof locations, and the questions which a billiards/anisotropic-spaces referee should check. In particular it separates the imported unweighted growth and distortion lemmas from the new weighted calculation, and the measurable finite-cover proof from any periodic evaluation of distributions.

The revision itself performs an explicit author-side source and proof audit. It finds a small but real statement/proof mismatch in the varying-test corollary: small limiting measure of an open set alone does not control the limsup of its source measures. Module 70 now requires small measure of its closure and a null boundary, as its Portmanteau proof actually uses. The physical overlap tests satisfy this condition by the same one-flight geometry, now checked in the compact-family application as well. The old module is preserved under provenance and the exact two replacements are recorded in `INHERITED_EDITS.json`. This does not remove or weaken the physical local theorem.

## R2. Expanded operator proof

New module `72_action_norm_details.tex` supplies the following details.

* It defines the weak, strong stable, and unstable norms in the common density convention, including graph matching, little-Hölder tests, the length normalization and an explicit compatible exponent choice.
* It states the preceding-flight partition requirements: bounded pieces in each homogeneity strip, bounded stable intersection count, and an `O(epsilon)` boundary-neighborhood length estimate. The analytic exponential and each fixed derivative are estimated in the piecewise multiplier algebra.
* It records the four exact geometric Jacobian/length sums imported from Demers--Zhang, derives the never-long length-weighted sum, and keeps the last-long-ancestor decomposition visible in the weak payment of the stable average term.
* It derives the action estimate from `d tau = T*theta - theta` with `theta = sin(phi) dr`, which applies to a general smooth scatterer. Matched connectors are the regular connectors of the original collision decomposition. Intermediate singularity cuts remain unmatched; paired endpoints have the same lattice itinerary. Trimming is accounted for, rather than declared costless.
* It separates the unmatched `epsilon^varsigma` contribution, the old graph/test and Jacobian errors, and the additional `epsilon^(1-q)` weight difference. The stable cross coefficient remains `C_B C_3^m`, not a constant independent of the iterate.
* It chooses the block length before the coefficient in the equivalent norm. No growing-band estimate follows from this choice.
* It proves faithfulness on the **strong** completion by transverse averaging of curve pairings, rather than assuming faithfulness of the entire weak completion. It then uses Cesaro projections of smooth bounded densities and `L1` domination to construct a nonzero bounded physical phase. The phase equation is passed to a weak-star limit of actual densities, avoiding a discontinuous test on an abstract distribution.

The preceding-flight and observation hypotheses are verified for oriented ellipses in `lem:v35-ellipse-geometry`, including explicit entry-root coefficients, uniform geometry, the finite singularity partition, and the closed exceptional neighborhoods for cell intervals. These are continuum proof arguments; finite regression tests are not used to establish them.

## R3. Theorem-level prior-art comparison

Module `75_literature_and_routes.tex`, placed first in Part I, compares the exact objects and topologies with Szász--Varjú, Demers--Pène--Zhang, and Dolgopyat--Nándori. The bibliography now records the published 2020 DPZ article, while retaining its arXiv version for lemma numbering; the previous bibliography is archived.

The comparison makes several points explicit. A fixed-table cell local limit, regular endpoint factors, and geometric perturbations are not by themselves new principles. A discrete singleton does not give a stronger topology than a lattice mixing local limit. The fixed-parameter physical conclusion belongs to suspension local-limit theory after the relevant joint observable, endpoint coboundaries and arithmetic group are verified. The scalar suspension application is not simply cited as the compact-parameter vector theorem used here.

The collision count is itself a suspension reward up to a bounded endpoint correction: equation `eq:v35-count-as-suspension-reward` proves the exact identity. Its presence is therefore not advertised as an intrinsically new arithmetic group. What this article adds to its own proof chain is the action-weighted roof realization and uniform norm calculation, the rotation-free joint phase argument, a compact-family physical local principle with verified noncircular examples, and the source-level posterior comparison after a proved microscopic denominator. No unverified claim of historical priority is needed.

## R4. Original endpoint and a broader mechanism

The four-coordinate raw actual-return LLT is **not** claimed complete by the new three-coordinate theorem. The pointwise common return correction and the full return-frequency complement retain their exact roles in `thm:LLT` and the coherent raw-inversion modules. They have not been deleted, redefined as averaged quantities, or marked proved in the manifest.

The present substantive advance follows the referee's proposed general-mechanism route without changing the mechanical topic. Module `73_rotation_free_arithmetic.tex` proves complete physical phase rigidity without the circular proof's rotations. The roof phase vanishes by measurable contact holonomy. The displacement and the constant collision step are then put together in the integer cocycle `(kappa,1)` in `Z^3`. A proper kernel has a nonzero finite character `(a,c)` modulo a prime. On the actual finite lattice cover it yields either a nontrivial unit-modulus eigenvalue when `c` is nonzero, or a mean-zero invariant function when `c=0`. Mixing/ergodicity excludes both. The argument uses no common periodic representative and no rotational symmetry.

Module `74_compact_family_local_principle.tex` combines this arithmetic with the expanded action estimates to prove a compact-family microscopic physical local theorem from geometric hypotheses. It verifies these hypotheses for the entire family of ellipses with semiaxes in `[0.45,0.47]` and arbitrary orientation on the same triangular lattice. This contains the circular radius family but is generally not sixfold rotationally symmetric. The covariance remains uniformly positive, including through the circular locus. Theorem 2 in the introduction states this extension. This is an additional proved family and proof mechanism, not a new name for the still-unproved return-frequency estimate.

## R5. Regular amplitudes versus arbitrary posterior tests

The general theorem states the regular endpoint class, null-boundary and closed-exceptional-neighborhood conditions, and the positive product-of-means condition for selected denominators. The arbitrary bounded-test statement is only a total-variation comparison of the original posterior with its positive-band approximation. The proof does not infer a Gaussian amplitude for a path-dependent selector from that comparison. No microscopic conditional path bridge is asserted.

## R6. Order of limits

Every local spectral use freezes `B` first, takes the collision count to infinity, and only then enlarges `B` through positive upper and lower envelopes. The new compact-family theorem displays this order inside its proof. The subsequent choice `B=m^(P+3/2)` uses only the explicit `O(1/B)` source-smoothing error and the independently proved `m^(-3/2)` denominator. It makes no claim about the dependence of the spectral constants on a growing band. The inherited signed middle conclusion remains a consequence of the independently evaluated positive probability.

## R7. Article-level dependency structure

The article now has two parts. Part I begins with the theorem-level comparison and a short proof route, then presents the expanded norms, rotation-free arithmetic and compact-family application. It retains the three detailed v34 collision/endpoint/physical modules immediately after that route. Part II contains the complete actual-return analysis and its raw inversion problem. All 71 inherited core modules are still compiled, as are the 24 A--X introductory statements and their proofs. All 967 inherited mathematical labels remain. The v34 main file is preserved verbatim under provenance. The new direct route no longer requires first navigating the whole cumulative return pipeline.

## R8. Exact reproducibility

The frozen v34 evidence is one successful response-branch run, `37629733461`, at the reviewed SHA. Its artifact is `11485927618`, archive digest `ad2fb3c74e73cd90495b0b794616474dc29b217254202287c862964dafb64a2a`. We do not describe it as two independent executions.

For v35, both new branches are created at the frozen review commit before the completed revision is pushed. The new read-only qualification workflow archives the exact event source, v34 baseline, inherited baselines and controlling report. It checks the frozen ordinary Git tree, exact inherited edits, all core inclusions and labels, ordinary-source Merkle manifest, bibliography, workflow hash, normal/optimized finite diagnostics, native typesetting and generated proof-page renders. Each dynamic receipt identifies the event SHA, actual run ID, PDF hash and scoped-source cleanliness. A run is reported successful only after observing its actual completed result. Independent human review and a full raw-return certificate remain false in every receipt.

The new packet is submitted for a substantive review of the expanded continuum proof, the rotation-free arithmetic and the noncircular compact-family theorem, together with the retained original return-density problem.
