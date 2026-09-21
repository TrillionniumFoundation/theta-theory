# Response to the A2 v108 independent referee report

**Revision:** A2 v109, *Single-contact recovery of information metrics through polynomial multiplication*.

**Controlling report:** `reviews/a2-v108-independent-harsh-top4-2026-09-21/REFEREE_REPORT.md`, immutable review commit `5a8a8190e6a5979719591b286fca92aae3cc15cc`. The report evaluates mathematical source `4ed51300c2aa6e7b11e701a38ed1d14f8b9e8191`.

We respond by proving a partial-data native recovery theorem in every shared dimension, rather than by relabelling the complete-conormal determinant calculation. The principal article now has a single dependency chain from normal second jets to polynomial multiplication, native realization, stability, and finite noisy observations. All earlier proofs remain in the complete companion and repository. The statements below identify changes and their scope; they do not presume a favourable journal decision or substitute diagnostics for proofs.

## R108.1 — Classical conormal rigidity and the novelty boundary

The introduction and Section 5 explicitly identify the rank-one cone with the quadratic Veronese variety and its dual with the singular-quadratic discriminant. The degree-two determinant consequence is stated as a classical lemma, with GKZ attribution and an elementary proof. Hankel forms versus polynomial multiplication are also attributed to structured-matrix duality (Mourrain–Pan). Neither ingredient is claimed as a new general algebraic principle.

The new theorem observes only prescribed normal spaces. If U_nu is the normal-polynomial space at an observed point and U is the sum of its within-point product spaces, the entire native second-jet fibre is `(theta + U^perp) intersect Omega`. This is a complete fibre and rank statement for partial observation. The substantive native step is its realization by the calibrated binary experiment in Theorem 3.2, not the formal act of intersecting two linear spaces.

## R108.2 — A native interaction beyond a two-parameter line

Theorem 3.2 proves that, for every d >= 2, k = 3d+2 root pairs suffice for a nonempty open family in which one positive contact point identifies all 2k-1 native moment coordinates. At precisely the same point arbitrary positive ambient metrics have a local fibre of dimension 5d(d+1)/2. Thus the obstruction removed by the native structure is high-dimensional and grows with d.

The proof derives J from the observation's actual square score system and Schur complement. With coefficient indices 0,...,3d+1, it chooses the tangent band E = {d+1,...,2d} and the complementary normal exponent set S = {0,...,d} union {2d+1,...,3d+1}. The same-colour root sign pattern makes -J e_(d+1) strictly positive. An explicit loading has tangent space J span(E), so its normal-polynomial space is span{t^a:a in S}. The three intervals in S+S cover every exponent 0,...,2k-2. The proof then gives an open loading neighbourhood and excludes extra global image sheets by a finite algebraic sign-fibre argument and properness.

This is a construction for every dimension and every separated positive root/clock configuration of the stated square experiment; it is not extrapolated from numerical examples. Additional rational examples in d = 2,3,6 have globally separated point (1,...,1), with exact ranks 15,21,39. Modular rational-rank checks and a separate inversion of the raw score matrix agree. The information is not chosen to manufacture a desired residual metric: J is fixed first by the native experiment, and the loadings specify a physical synchronized subfamily independent of exposure choice.

## R108.3 — Higher dimensions and noninjective quadratic measurements

Section 5 states plainly that, with complete conormal data and an injective full-symmetric measurement map, d >= 3 already identifies arbitrary ambient metrics. Native structure is unnecessary for that older identification result.

The new theorem uses one normal space, for which unrestricted matrices remain nonidentifiable in every positive tangent dimension. Moreover k = 3d+2 is less than dim(Sym_d) when d >= 6. The new realization therefore includes necessarily noninjective full-symmetric measurement maps. Its local reduction uses full column rank and coercivity of q_A, not the old stronger hypothesis. The original companion results keep their original hypotheses. No unproved extension of their statements is silently invoked.

## R108.4 — Exact oracle counts, stability, and finite noisy observations

The 2k-1 query statement is retained as an exact-real deterministic scalar dual-jet oracle result. The input, adaptivity, and output are specified. The response explains why an ordinary directional curvature is not generally a dual-normal query in higher codimension.

Theorem 4.1 proves a perturbation bound with the actual least singular value gamma of the multiplication observation operator: moment error is at most `(2 M^2/gamma)` times the Frobenius jet error. The complete fibre theorem supplies the matching failure of identifiability when gamma is zero. Norms and positive block bounds are explicit; no norm-free numerical conditioning claim is made.

Theorem 4.2 defines a different, finite statistical experiment. It uses the finitely many normal basis directions and pairwise sums, two nonzero contact offsets in each direction, and independent Gaussian noise on symmetric contact readings. No derivative is supplied. On a compact convex native parameter set, the exact finite-offset mean is globally bi-Lipschitz, with scale h^2, for sufficiently small fixed h. Fitting that exact mean gives the nonasymptotic squared-error bound `4 p sigma^2/(N a^2 h^4)`. The manuscript derives LAN, the positive per-replicate information, least-squares efficiency, and the local asymptotic minimax bound using classical Gaussian asymptotic theory. It verifies the needed hypotheses instead of treating generic LAN as a new theorem.

This theorem concerns noisy contact values, not raw unlabelled categorical samples from the underlying binary law. The exact finite-offset mean is not replaced by its quadratic Taylor approximation; doing so would introduce nonvanishing fixed-offset bias. Higher-order information is not declared invisible merely because second-jet rank fails. The statistical claim is limited to the observations actually specified.

## R108.5 — Effective endpoint fibres versus structural classification

The function-input endpoint representation result remains in the companion and is explained in Section 6.3. At each fixed endpoint dimension its KKT encoding and real quantifier elimination produce the exact representation fibre. Searching dimensions terminates under a finite-representability promise. No unproved intrinsic dimension bound, general efficient algorithm, or explicit classification of all higher-dimensional fibres is attributed to QE.

The explicit fully visible and first-degenerate-stratum classifications and their exhaustion proofs are preserved in full; they are not replaced by the effective statement. The principal recovery theorem does not depend on this endpoint algorithm. The inverse parametric programming comparison retains Hempel–Goulart–Lygeros and Nguyen–Olaru–Rodriguez-Ayerbe–Hovd–Necoara, with verified bibliographic data. It distinguishes scalar value graphs from optimizer maps without alleging that those works require a supplied hidden active fan.

## R108.6 — A genuine dependency chain without deleting the archive

The principal source is a self-contained amsart manuscript with definitions, theorems, proofs, and a short local-reduction appendix. Its progression is normal contact, complete product-space fibre, native realization, and quantitative/statistical recovery. The dependency table names assumptions actually used and stronger assumptions not used.

The complete v108 article remains the companion. Every one of its actual TeX inputs is included in the manifest; all prior mathematical sources are unchanged. The prepared copies preserve all proof/theorem environments as checked by the inherited preparation script. Shortening the principal narrative is therefore not deletion of the previous results or their arguments. The companion's historical title, numbering, and claims are preserved as historical text, not silently promoted to new principal contributions.

## R108.7 — Exact committed source and build provenance

The reviewed mathematical commit indeed lacks the four prepared inputs. A subsequently completed v108 native run, `35553783129`, provides a 58-page PDF at a different, materialized source commit, `9affc52cc4eb62e5c14cffb564b380b86503aec2`. Comparison with the reviewed source shows exactly the four added prepared inputs plus their preservation manifest. It does not retroactively make the earlier commit complete.

Revision 109 includes those existing prepared blobs in its source commit. Its principal TeX source has no generated inputs. The new verifier checks exact Git source bytes, checks inherited source against the controlling review, verifies all preparation hashes, runs v109/v108/v107 diagnostics plus the unchanged independent referee checks, builds both volumes, and rejects unresolved references or overfull horizontal boxes. Receipts record source commit separately from the subsequent evidence commit, along with manifest/PDF/log hashes and the native run URL when applicable.

A partial local source-bundle run is deliberately distinguished: it records `source_bound: false` and never claims that a queued Actions run succeeded. The actual receipt, not this response letter or the workflow definition, determines the executed build status. The review branch, default branch, and other manuscript branches are not modified.

## Additional precision points

The full-conormal lemma states k >= d(d+1)/2 where full-symmetric injectivity is assumed. Positive fibres are intersections with the admissible cone, not entire affine lines. Nonorthonormal normal bases require the Gram factors `K G^(-1) K`, whose omission would be incorrect. Equality of observed second jets is not equality of all contact orders. The single-contact construction gives a sufficient k, not a minimality claim. Rational-loading enumeration is algorithmic only for specified exact algebraic root/clock input; arbitrary real configurations give an existence statement. All finite diagnostics are labelled as such.
