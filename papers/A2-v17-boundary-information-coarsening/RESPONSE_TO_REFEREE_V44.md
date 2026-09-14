# Response to the independent referee on A2 v43

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 44 · September 14, 2026

We thank the referee for distinguishing fresh mathematical scrutiny, earlier repairs, delivery facts and editorial judgment. This response addresses the report at `6f7de242000a7db2bf473276b8e1792104c7cd42`, examining source `22d9b930a426cdb2c62984a5a3e5875e95e05e79` and products `edd95683ee57965ff8cd82cee1462a478d06ae39`. These are author-requested independent assessments, not commissioned journal reports.

The principal addition is a complete geometric realization of the observation-specific inverse mechanism, not a new claim that elementary matrix identities alone establish its significance. No inherited theorem has been removed or weakened. Exact preservation, build provenance and the finite checks are documented separately in [the dependency record](PRESERVATION_AND_DEPENDENCIES_V44.md) and [the execution ledger](VERIFICATION_V44.md).

## R43-S1: an integrated nonsymmetric periodic realization

The referee asks for an example or family exhibiting the measured channels, two independent deck cycles, a signature-rigid spanning structure and clearance together. The new Section 17 supplies this demonstration with explicit formulas and complete proofs. It is placed immediately after intrinsic rigidity and stability, before applications, so the reader encounters the realization next to the theorem it implements. The previous introduction and proof architecture remain; one added introductory subsection explains the role of the example.

### Simultaneous geometric realization — Theorem 17.1

Two analytic supports are used:

`h1(theta) = 1 + epsilon*(cos(2 theta) + cos(3 theta + pi/4)/4)`,

`h2(theta) = 3/4 + delta*(cos(2 theta) + cos(3 theta + pi/6)/4)`,

where both amplitudes range over `[1/200,1/100]`. The lattice is `T diag(8,10)`, with `||T-I|| <= 1/100`, and the second obstacle has center `T(4,5) + w`, `|w| <= 1/100`. The supports are not the observations and their parameters are not supplied to the inverse.

The proof computes positive curvature radii and separates the two curvature ranges. It excludes every proper rotation through the simultaneous nonzero second and third harmonics, excludes reflection through incompatible harmonic phases, and excludes exchange of obstacle types through their different perimeters. Thus the example does not rely on hidden geometric symmetry. Modulo its period translations, the whole table has no Euclidean symmetry.

The selected channels have marks `(1,2,-i e1-j e2)`, `i,j in {0,1}`. Every obstacle pair has separation greater than `43/10`; each selected closest segment has clearance at least `383/200` from every third obstacle. These inequalities are proved for all lattice translates by center-segment and support estimates, not inferred from a finite spatial search. A strictly concave scalar maximization finds each actual contact and gap; contacts are not incorrectly placed on the center directions. Fixed prescribed planar gates have uniform interior margins. These construction-frame coordinates are not given to the intrinsic observer as cross-channel registration.

The two cycles `e00 e10^{-1}` and `e00 e01^{-1}` start at the same channel frame and have deck displacements `e1,e2`. The edge `e00` itself is a signature-rigid spanning tree on the two obstacle orbits. The absence of proper obstacle symmetry verifies each required incidence transition. This checks the anchoring and spanning hypotheses in one table, rather than listing separately plausible conditions.

### Registration from recovered images — Proposition 17.2

After the established nonlinear inverse and analytic continuation have recovered complete obstacle images in each separate channel frame, their support Fourier coefficients can be computed. The ratio of the relative third coefficient to the relative second coefficient gives the relative rotation without any branch choice for an argument. The translation-covariant support center then fixes the translation. The coefficients cancel between copies of the same unknown obstacle: neither the construction parameters nor a preassigned geometric frame enters this registration.

In the resulting single frame, differences of registered second-type centers recover both period vectors. The fourth channel gives a redundant holonomy identity. The proposition proves local Lipschitz bounds for this registration stage in the uniform topology on support functions, using explicit nonvanishing Fourier margins. It does not turn analytic continuation into a Lipschitz map from jets, or claim a new effective statistical rate.

### Complete observation-to-table composition — Corollary 17.3

At a common positive offset, the two same-type signed laws at each of four channels and their four onsets determine the table and lattice up to one simultaneous proper Euclidean motion. The proof follows the actual dependency chain: the four-density identity cancels amplitudes; the finite-remainder signed inverse recovers both contact jets; analytic continuation gives complete images; intrinsic registration and the two cycles give the lattice and every obstacle placement. The actions in a channel cannot both be even, since the established contact inverse would then force an excluded global reflection symmetry.

An exact specified member is included. Its recovered Gram matrix is `[[64,2/5],[2/5,40001/400]]`. The accompanying diagnostic solves its nonlinear contact equations and registers support images; its reconstruction routine does not receive the matrix that generated the table. The wider finite diagnostic covers 108 parameter cases and 436 channel solves. This checks the finite geometric implementation, not the all-order boundary-law theorem.

### Persistence beyond a small model — Proposition 17.4

Independent real-analytic support perturbations with `C^2` norm at most `10^{-6}` preserve the curvature, separation, gate and clearance margins and the harmonic obstruction to symmetry. The same cycles, signature-rigid tree and intrinsic inverse continue to apply. Higher harmonics are allowed, so the result is not confined to fitting a finite list of trigonometric parameters. On compact analytic subfamilies satisfying the existing physical theorem's regularity conventions, its charged long-bridge reconstruction applies with these four labels. We distinguish this compact-subfamily assertion from the infinite-dimensional analytic neighborhood itself.

This addition addresses the specific request for an integrated demonstration and makes the reach of the existing nonlinear mechanism inspectable. Exceptional general-journal significance remains for the referee and editors to judge. Neither this response, the page count, nor the numerical tests are presented as an acceptance certificate.

## R43-D1: artifact existence versus Git retention

The referee is correct. The v43 native main and companion existed, and the review independently rebuilt them. The error was that an ordinary directory-level `git add` omitted 13 ignored PDF, auxiliary, recorder and raw-log files while the copy receipt claimed their retention. We do not recast this as a failed build or an unavailable native manuscript.

The v44 implementation separates three assertions: validated artifact copying, Git-index verification and committed-object verification after publication. It force-stages only the two named delivery subtrees, not the whole repository; publishes a new products branch; fetches that branch; and reads every promised blob with `git cat-file`, comparing byte counts, SHA-256 and Git blob identities. A separate attestation names the fetched published commit. After the attestation is committed and pushed, the final fetched tree is checked again. Thus a correct working directory cannot mask missing published files.

The original v43 archive is retained in a new `deliveries/a2-v43-repaired/<source-SHA>` subtree. The flawed historical receipt remains unchanged at its original path, so the correction does not erase the evidence. The new v44 archive is separate and source-pinned. Both contain the native PDFs, full source archive, raw logs, recorders and build evidence. Their actual published identities and execution outcome are recorded in the verification ledger; configuration alone is not treated as successful delivery.

A negative control runs this actual implementation in a temporary Git repository. It reproduces all 13 omissions under ordinary staging, fails verification as required, passes after explicit force-staging, and still verifies the committed PDF after the working-tree PDF is deleted. Ordinary and optimized Python produce identical JSON.

## R43-D2: current navigation

Both current README entries identify v44, its author branch, the addressed report, the complete native entries and the current source/build/product ledger. The earlier v42-labelled entries and complete v43 main are preserved byte-for-byte in `history/v43-review-baseline`. Failed earlier checkpoints remain historical evidence; they are no longer advertised as the current delivery state.

## Findings explicitly retained

The smooth functional-remainder argument, rather than merely the determinant-one matrix, remains the basis of finite-jet factorization. The positive scalar anchor remains in the single-offset inverse. The exact observation space, marked incidence, prescribed gates, common-frame rerooting and realizability assumptions remain unchanged. The compact-net Gaussian upgrade, differentiated relative estimates, physical pilot at the final flight number, charged failures, and distinction between intrinsic transverse laws and richer planar records are retained without rebranding them as fresh results of this revision.

The version-sensitive Florio–Leguil comparison and the distinctions from analytic open-billiard and enriched Sinai marked-length observations remain intact. The prior Poisson boundary-experiment literature is not claimed as a new general principle. The present revision's fresh proof work concerns the integrated geometric construction and its registration/persistence mechanism; it is not represented as a newly independent verification of every historical analytic or statistical theorem.
