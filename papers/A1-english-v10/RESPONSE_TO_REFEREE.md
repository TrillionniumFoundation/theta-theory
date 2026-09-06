# Response to the v9 referee report

**Controlling report:** `reviews/a1-english-v9-2026-09-06/REFEREE_REPORT.md`, commit `7a499e3cb32396b18eda869342ec8e9c70d8d028`.

**Reviewed submission:** `e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5`.

**Revision:** A1 English v10, *Sparse observation algebras: collision geometry and shared memory*.

We thank the referee for separating mathematical closure from the question of mathematical significance. The report identifies no blocking defect in the scalar intrinsic theorem, but its editorial objections require more than another collision example or a reformulation of a classical matrix invariant. We retain the complete scalar proof and add a shared-state composition theorem with an unrestricted joint coding converse and an observation-order consequence. We also implement all four presentation requests. The requested journal target is unchanged; this response does not convert source preservation, test execution or the author's judgment into a referee endorsement.

## E9.1 — The finite determinant profile has classical spectral content

We agree with the mathematical comparison. Proposition `prop:ordinary-spectrum` now explicitly proves, for the ordinary square real Vandermonde matrix W on a fixed number q of nodes in [0,1],

    V_l(x) ≍_q product_{j≤l} sigma_j(W(x)) = || exterior^l W(x) ||.

The proof includes the exact zero tail at repeated nodes. The monic Newton coefficient matrix and an extended active Leja matrix both have gap-independent inverses. No reciprocal zero pivot occurs. The proposition is credited to the source-pinned technical note, and the text distinguishes it from clustered Fourier-matrix theorems. The scalar determinant law is not presented as a new general spectral principle.

The additional composition theorem asks a different operational question. The future observation algebra of independent experiments is a tensor product, but their reachable posteriors lie in a product image. A bounded linear extraction map recovers each component raw vector from the full tensor query vector. This map also acts on arbitrary off-image decoded centers. The memory converse thus counts genuinely attainable component directions, not tensor ambient multiplicities. The new theorem is neither implied by declaring a tensor matrix to be ill-conditioned nor justified by counting its columns.

## E9.2 — A consequential result beyond a tree evaluation or inserted tangency

Sections `08_shared_memory.tex` and `09_scheduling.tex` contain the new development. The model permits any fixed finite collection of independent sparse experiments, with different exponent sets, compact calibration sets, detectors, command cubes, full-support priors and horizons. A prescribed schedule interleaves them, and the entire machine has a single M-valued index. The future target is the physically executed full tensor product query, not merely a separately scored list of marginal forecasts.

At a checkpoint, let p_b be each block's own attainable past cap, V_{b,0}=1, and V_{b,l} its determinant volumes. The new law uses

    A_k = max_{sum l_b=k, 0≤l_b≤p_b} product_b V_{b,l_b},
    Theta_s(M) = max_{1≤k≤sum p_b} (A_k/M)^(2/k).

Theorem `thm:shared-state` proves matching unconditional and maximum-history checkpoint bounds, and then proves that one causal M-label transducer realizes the maximum of these profiles over all checkpoints. The proof addresses four possible gaps explicitly.

1. The tensor probability image is metrically equivalent to the component raw image, with a linear left inverse on arbitrary decoded centers (`lem:product-metric`). No decoder is assumed to output a product posterior.
2. The upper cover is a product of blockwise dimension-truncated covering polynomials. It retains each cap p_b separately. Merely applying a total-dimensional rectangle bound could incorrectly allocate too many axes to one block.
3. The lower law is the product of actually acquired subprobability rectangles under the one common independent exploration experiment. The acquisition evidence is retained. A union-of-balls argument applies to arbitrary joint M-center codes and the declared independent coding randomness.
4. A joint representative is read-only program data. Its index is the entire persistent state. Only the active block undergoes a raw moment update; the whole tuple is then re-encoded. The error recurrence includes every previous re-encoding, including errors in inactive components, and never rereads an exact history.

The logarithmic inversion (`thm:shared-bits`) yields

    B_omega*(epsilon,a) = max_s sum_b b_b(n_b(s),epsilon,a_b) + O(1),

uniformly through collisions. Consequently a joint encoder cannot save an unbounded number of bits over this additive checkpoint requirement. The observation-order theorem (`thm:schedule-extrema`) proves that serial schedules attain max_b L_b+O(1), while the largest schedule cost is sum_b L_b+O(1), where L_b=max_n b_b(n,epsilon,a_b). The serial schedule is the same for every accuracy and calibration. The exact continuous-dimensional statements have no O(1) remainder.

Corollary `cor:concurrency-exponent` makes the consequence visible without another perturbation parameter. For B independent {0,1} blocks of horizon 2h, the serial streaming rate is M^(-2/h), while a schedule with all blocks simultaneously at their middle count has rate M^(-2/(Bh)). Both use exactly 2Bh trials and one shared state budget. The distinction is the coexistence of future-relevant acquired information, not an artificially declared observable jet.

These consequences are not counted as multiple independent deep theorems merely because they have separate labels. The central additional claim is the attainable, calibration-uniform, causally compatible composition law against arbitrary joint coding. Its scheduling consequence is a new question resolved by that law. Whether this additional structure has the significance required by the requested journals remains for the next substantive review; the manuscript does not claim to settle that editorial judgment by assertion.

## E9.3 — Generality must concern the experiment, not only calibration notation

The new setting changes both the hidden state and the resource problem: it has a multicomponent hidden vector, heterogeneous observation blocks, tensor future queries, and a shared persistent memory that must be reallocated as counts change. Independence is an explicit product-prior and conditional-trial assumption. The result is not a scalar theorem relabeled as a theorem for arbitrary multivariate priors.

All earlier positive scalar assertions remain under their original assumptions. Constants are still for fixed priors and finite horizons. Calibration is known; read-only exact-real programs are allowed. The lower law still has continuous exogenous command exploration. Neither an arbitrary optimally chosen control objective nor a finite-precision synthesis algorithm is inserted without proof. The future-only task explains why completed independent blocks may be forgotten; an externally specified retrospective payoff requires its own task memory and is not silently erased.

## P9.1 — Isolate the ordinary Vandermonde comparison

Implemented as `prop:ordinary-spectrum` before the attainable Newton-flag argument. Its complete proof covers repeated labels and zero scales. The text explicitly states which parts of the statistical theorem do not follow from the matrix statement.

## P9.2 — Isolate the arbitrary-prefix Hermite principle

Implemented as `lem:hermite-prefix`, with arbitrary ordering and nonadjacent repetitions. Independence follows from the triangular evaluation of the prefix functionals on 1,z,...,z^(p-1); the complete Hermite data have dimension p. Substitution of t^(Hz) gives complete logarithmic multiplicity blocks. The precise classical comparison is de Boor, *Divided Differences*, Proposition 7, printed page 48. The strict confluent mixed-pairing lemma and its unchanged proof immediately follow, before posterior attainment is invoked. The v9 proof's corresponding internal argument is preserved rather than deleted.

## P9.3 — One dependency spine, without removing subsidiary proofs

The principal now follows the order:

    experiment and resource model
      -> exact product tangent
      -> complete Hermite flags and finite spectral scales
      -> global dimension-truncated cover
      -> intrinsic attained checkpoint and causal law
      -> shared-state composition
      -> additive bits and observation-order extrema.

The complete algebraic, affine, fixed-calibration streaming/control, five-/seven-trial, decision and mechanical proofs are printed in appendices. The convex collision-energy consequence is also printed there and credited to the referee's technical note; it is not called a new v10 contribution. The former introduction and scope exposition are preserved verbatim in `retained/`, and the entire v9 path remains unchanged by branch ancestry. The source check verifies all 42 prior result labels and all 40 prior proof blocks in the *printed* v10 inputs, not merely in an unprinted archive.

The principal has 53 named labels and 50 proof blocks. The difference includes classical lemmas, summaries and consequences; it is not an originality score. Revision logistics, execution receipts and source provenance are outside the mathematical narrative.

## P9.4 — Separate preservation, execution, compilation and review

`validation/PRESERVATION.json` checks pinned source blobs, retained labels and exact proof hashes. It does not certify proofs. `build.py` executes the unchanged v7/v8/v9 programs in a temporary copy, including the exact v7 sibling required by the inherited v8 test; it neither edits those programs nor suppresses a conditional assertion. The v10 program tests the capped allocation identities, arbitrary-center tensor recovery, schedule extrema and one-index raw-update fixtures. The source-pinned reviewer program is rerun separately and is labeled an author's rerun, not a new independent referee execution.

Fresh local, Actions and standalone receipts have separate directories and record their input identity, program hashes, runtime, logs and PDF hash. The committed principal is readable without running the source materializer. The standalone bundle contains the original source inputs needed to reproduce every invoked check. A successful execution establishes only the reported finite assertions and compilation, not the continuum lower law, exhaustive priority or journal acceptance.
