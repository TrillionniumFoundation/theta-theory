# Response to the independent referee report on A2, revision 76

**Revision:** 77 — *Statistical action recovery and smooth rigidity of dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Report:** `review/a2-v76-independent-harsh-top4-2026-09-17`, commit `fd4c9f57b9d0b142b60e163b266a708b61d80c94`.  
**Reviewed baseline:** `revision/a2-v76-relative-envelope-2026-09-17`, commit `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`.  
**Frozen manuscript tree:** `950c448c8e8f19c6181fee26e425a9ac23b7dca9`.

The report distinguishes the correctness of the periodic physical-to-smooth inverse from its general-journal significance. We have addressed its principal request by changing the inverse theorem, rather than presenting another refinement of the contraction threshold as a new main result. The periodic theorem and all inherited material remain available, with their statements intact.

The principal article is now `rigidity_v77.tex`; the complete technical manuscript is `main_v77.tex`. The first part of both contains the new experimental model, absolute action inverse, nonlinear shared-prefix theorem, Euclidean distance reconstruction, finite coverage theorem, and stability. The inherited periodic and multichannel material remains in the same revision. All 1,035 files of the frozen manuscript tree are byte- and mode-exact; version-specific copies make the changed notation and entry points explicit.

## R76-M1 and Sections 6–7: change the theorem's input or conclusion

The main result of the new first part is **Smooth rigidity from weighted scalar records**, `thm:v77-main`. Its input is a finite collection of three-clock joint endpoint laws for regular reflection branches and their one-flight extensions. Endpoint labels are coordinates on an abstract boundary atlas. Euclidean contact points, tangent frames, chart speeds, periodic polygons, branch length anchors and the lattice Gram form are not supplied.

For each branch the source density is unknown but independent of initial free time in the relevant flow box. Joint retention efficiency is unknown and need not separate into endpoint factors. Both are fixed across the three clocks for that branch. Distinct branches and distinct candidate tables may have different source and retention functions.

The proof has three exact steps.

1. **Absolute action recovery.** `thm:v77-clock` eliminates three unknown normalizations and a common arbitrary positive joint multiplier. An anchored affine clock identity determines the formerly unknown absolute anchor length; the two-clock quotient then determines the entire finite action. `lem:v77-physical` derives this model from actual phase volume in arbitrary scalar boundary coordinates.
2. **Nonlinear prefix cancellation.** `prop:v77-cancellation` matches initial covectors through an equation in recovered action derivatives. The matching derivative equals `-U_st^2/(U_tt+ell_tt)<0`, by a positive Schur complement of the actual reflection Hessian. A root bracket gives a unique physical branch. Subtracting the two absolute actions recovers the full last-flight distance kernel, including its constant.
3. **Euclidean reconstruction.** `prop:v77-distance` gives a finite rank-two/rank-five certificate, an explicit metric solve and whole-function trilateration. Overlap triples register the patches; two labeled translated copies recover the lattice. No analyticity or equality-of-jets principle occurs in this argument.

The conclusion is therefore not confined to germs about a supplied periodic polygon. It determines the parametrized target arcs and their relative Euclidean placement, and the full table and lattice when the atlas covers them. The uniqueness theorem compares arbitrary realizations of the same admissible atlas, not only nearby tables.

This is not advertised as a strict ordering of the old and new statistical experiments. The new protocol removes supplied Euclidean marks and permits joint source/detection bias, but uses a third clock and a larger spatial branch family. The two observation models are stated separately.

## Coverage is proved on an actual nonempty smooth class

The new result does not stop at “assume the whole boundary is covered.” `thm:v77-finite-atlas` constructs a finite identifying atlas for every finite-horizon periodic dispersing table with locally nonconic boundaries, with every measured prefix longer than any prescribed finite lower bound.

The proof establishes regular finite extensions of a ray fan, connectedness of the lifted obstacle visibility graph, finite boundary coverage by compactness, availability of finite distance certificates, and registration of two basis translates. It then fixes scalar gates and absolute clocks on an open neighborhood. It does not use density of periodic points to infer a uniform inverse radius.

`prop:v77-example` supplies an explicit triangular-lattice family with support function `h(theta)=R+epsilon cos(3 theta)`. Disk inclusion proves finite horizon and separation, positive radius of curvature proves strict dispersion, and the analytic noncircular threefold symmetry excludes a conic subarc. Once the finite atlas is fixed, small nonanalytic smooth perturbations preserve its finite strict certificates. Whole-boundary reconstruction on these perturbed tables uses the actual distance functions, not analytic continuation.

The design theorem is an existence and persistence theorem. A finite universal adaptive search without any admissibility information is not made a premise or claimed as a consequence. Coarse time brackets in `lem:v77-clock-design` select three admissible absolute clocks without supplying an exact length action. Exact scalar atlas, branch, and lift labels remain information in the experiment.

## R76-M2: phase weights and fixed-norm conditioning

The periodic phase-weighted estimate and its `kappa(w)` cost are retained. The first part now explicitly distinguishes the spectral radius of a fixed domination matrix from the norm-equivalence cost of its weights. Permuting phases and changing positive phase units preserve that matrix's spectral radius by similarity, not its fixed-norm condition number.

The new finite-action theorem is not advertised as a uniform conditioning improvement over the periodic theorem. Its constants retain the clock-anchor denominator, finite mixed twist, matching Schur complement, distance singular values and finite registration depth. In particular a long shared prefix can have a small matching derivative. This cost is stated next to the stability theorem.

## R76-M3: explicit instantiation of the determinant comparison

The new `cor:v77-periodic-blocks`, in `article/10n_periodic_determinant_bridge_v77.tex`, makes the bridge explicit. With `r=floor(N/3)`, it specifies the retained end projections and the reduced matrix `(P G_N P) Delta_E` and proves:

- trace-norm middle deletion bounded by a fixed polynomial times `rho^r`;
- uniformly bounded differentiated trace norms of the diagonal blocks;
- Hilbert–Schmidt cross coupling bounded by a fixed polynomial times `q_G^(N-2r)`;
- padded half-line diagonal comparison bounded by a fixed polynomial times `rho^r+rho^(N-r)+q_G^(2(N-r))`;
- a common operator margin throughout the interpolation, including the block dephasing identity;
- the resulting quadratic cross-coupling term `q_G^(2(N-2r))` in the logarithmic determinant estimate.

The proof maps each bound to the Green-reflection, localization and gluing estimates in the inherited periodic-relative theorem. It applies the trace-ideal comparison before probability normalization. The local block symbol is now `mathsf B_N`; the scalar physical twist remains `D_{N,b}`.

## R76-M4: integration into the principal theorem and narrative

The opening part of both current manuscripts contains the new theorem and every deterministic proof input. The later periodic part retains the relative law, global quadratic inverse, finite signed jets and actual smooth envelope. The introduction identifies which observation model each mechanism uses. The finite clock theorem does not invoke the periodic determinant limit, and the inherited periodic theorem is not made to depend on the larger spatial atlas.

The old matrix envelope remains a useful quantitative statement. We have not relabeled it as a new abstract theorem with applications not proved in the manuscript. The change in scope is instead supplied by the new physical-to-action-to-distance theorem and the finite coverage construction.

## R76-M5: finite-preparation assumptions and their costs

`thm:v77-stability` gives a finite-order geometric comparison from differentiated conditional densities. `cor:v77-sampling` is a consequence on bounded classes with an explicit retained-success floor and smoothness bounds. Every attempt is charged. A measurable actual-table selector, rather than an arbitrary formal reconstructed kernel, produces the estimator. The rate is sufficient, not claimed to be minimax or an effective enumeration theorem.

Because these are exact finite actions, there is no limiting-law approximation term. The finite twist and rare retention costs remain in the constants and preparation floor; fixing a finite flight number does not eliminate them. The original Liouville-calibrated count/area results remain valid in their original model. Unknown source normalization is not silently converted into a recovered local area scalar.

## Required literature comparison and scope precision

The introduction now compares mechanisms with the corrected planar Noakes–Stoyanov travelling-time/scattering result, the enriched marked-spectrum theorem of Finamore–Leguil, and the complete-bipartite distance rigidity work of Connelly–Gortler–Theran. It does not assert priority for smooth global obstacle rigidity, general generating-function composition, or generic distance reconstruction. It identifies the passage from normalized jointly weighted scalar records to absolute physical actions and distance kernels as the new observation interface.

Locally conic geometries are not declared nonidentifiable by the new certificate. The certificate is sufficient; the original marked smooth theorem, which does not require the nonconic condition, is preserved. Unlabelled branch mixtures, arbitrary clock-dependent sources, and unknown coordinate convolutions are not silently included in the stated shared-weight model.

## Preservation and verification

The frozen source tree was recovered from the source-matched v76 workflow artifact and rehashed to its exact Git tree ID. Every inherited file is retained unchanged. The new principal and complete technical entries compile from that same enlarged tree, and the two-collision companion is unchanged.

`tools-v77/check_revision_v77.py` performs symbolic three-clock cancellation and checks actual nonlinear reflected trajectories, positive interior Hessians, incidence margins, prefix-path identity, the Schur derivative, and reconstruction of full strictly convex boundary patches. These checks supplement the written proofs; they are not formal verification or independent referee certification. The build and publication status are recorded separately in the root handoff file, including whether a remote write actually occurred.
