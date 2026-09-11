# Response to the A2 v22 independent referee report

**Revision:** A2 v23  
**Branch:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Report answered:** `reviews/a2-v22-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Review-head base:** `7057ec51b341264fa3752a0e5eb466650579bab1`  
**Active manuscript:** `papers/A2-v17-boundary-information-coarsening/main.tex`

The v23 revision takes the strengthening route throughout.  It preserves the v22 all-order determinant-one signed inverse, the non-dominated/common-collar endpoint theory, the fixed-window realization and the stopped finite-to-boundary transfer.  It does not replace those results by lower-order statements, does not narrow the paper to avoid the report, and does not delete accepted mathematical content.  Instead it adds an intrinsic periodic global theorem, two richer physical local experiments, and a growing-order analytic/statistical bridge.

## C22-M1 / R22-1: make the global theorem intrinsic and define the registration problem exactly

**New sources**

- `article/23b_intrinsic_multichannel_rigidity_v23.tex`
- `article/23c_analytic_continuation_v23.tex`

The v22 global theorem supplied the participating contacts and oriented channel frames in one common Euclidean registration.  V23 replaces that architecture by the native periodic channel index of the paper,

`e=(a,b,ell)`.

For each measured channel the intrinsic datum contains the lifted channel label `(a,b,ell)`, the physical onset, the two same-type signed endpoint-law germs and the transverse sign convention.  It is recorded only in the channel-adapted frame.  No Euclidean placement of that frame relative to the periodic lattice or to another measured channel is supplied.

The v22 all-order inverse recovers the complete analytic boundary germs at the two contacts.  A new standalone analytic-continuation lemma proves that a registered nonempty germ of a connected real-analytic strictly convex boundary determines the complete boundary image.  The proof uses analytic continuation of the signed curvature, equality of the arclength periods from positivity and total turning `2 pi`, and uniqueness of the planar Frenet system.

Thus each measured edge now recovers complete oriented analytic copies `C_{e,-}, C_{e,+}` of the two incident obstacle lifts in its own frame.  V23 then treats their relative placement as the inverse problem.

Let `Lambda_abs` be the marked abstract Euclidean lattice and let `iota` be an unknown oriented Euclidean realization.  An algebraic periodic gluing consists of `iota` and one `A_e in SE(2)` for every measured edge, with the condition

`tau_{-iota(nu(e,sigma))} A_e C_{e,sigma}
 = tau_{-iota(nu(f,sigma'))} A_f C_{f,sigma'}`

whenever the two incidences carry the same quotient obstacle label.  In words, every recovered obstacle lift is translated back by its deck vector before copies of the same quotient obstacle are matched.

The gluing is called **admissible** only if the resulting periodic translates have disjoint obstacle closures and the declared measured edges retain their prescribed facing contacts, onsets and selected closest-pair channel geometry.  Hence an arbitrary algebraic curve matching is not silently promoted to a billiard table.

The quotient of admissible periodic gluings by one simultaneous global `SE(2)` action is denoted `G_per(D)`.  The new classification theorem proves

`periodic dispersing table realizations / global SE(2)  <->  G_per(D)`.

This makes the remaining ambiguity an explicit object determined by the intrinsic observations.

### Symmetry and lattice holonomy

V23 proves that two framed points of a connected analytic strictly convex curve have identical complete oriented curvature signatures exactly when an orientation-preserving Euclidean symmetry carries one to the other.  Circle phase ambiguity and finite cyclic symmetries are therefore treated as genuine inverse ambiguities rather than hidden conventions.

For a closed measured channel cycle with signature-rigid incidence matches, compose the unique data-determined frame transitions.  The new cycle-holonomy lemma proves that the composition has no rotational part and is a translation `tau_{v_c}`.  If

`eta_c = sum epsilon_i ell_{e_i}`

is the total marked deck displacement, then every admissible realization satisfies

`R_{e0} v_c = iota(eta_c)`,

where `R_{e0}` is the rotation of the starting channel placement.  Thus a cycle with `eta_c != 0` fixes the orientation of the marked lattice relative to the channel network once the global Euclidean gauge is removed.

A **lattice-anchoring cycle** is a signature-rigid cycle with nonzero deck displacement.  A rooted **signature-rigid spanning tree** then propagates the placement from an obstacle met by that cycle to all obstacle orbits.  The resulting corollary proves that the complete labelled periodic table is determined up to one simultaneous global `SE(2)` motion, with no absolute contact point, tangent frame, inter-channel placement or channel-to-lattice orientation supplied in advance.

Two calibrated special cases are stated separately rather than conflated with the intrinsic theorem:

1. if the oriented lattice realization **and one root channel frame relative to that lattice** are supplied, a rooted signature-rigid tree determines the remaining placements;
2. if every channel frame is supplied in one laboratory, the registered v22 theorem is recovered.

This explicitly resolves the two readings of “registration forgotten” raised in the report, and it uses graph connectivity and deck displacement rather than the old vertex-cover notion alone.

## C22-M2: strengthen the global consequence rather than lower the target

The global theorem chain is now

`intrinsic signed lifted-channel laws`
`-> all-order framed contact inverse`
`-> complete analytic obstacle lifts`
`-> admissible symmetry/lattice-holonomy gluing`
`-> periodic table rigidity up to one Euclidean motion`.

The relative channel placement and the periodic deck geometry are part of the inverse theorem rather than external laboratory input.  The exact obstruction is `G_per(D)`; the paper then gives a concrete sufficient uniqueness mechanism through one anchoring cycle and a rooted signature-rigid spanning tree.

The registered analytic-continuation statement remains only as a special case, not as the headline global theorem.

## C22-M3 / R22-3: connect fixed finite-jet statistics to global analytic recovery

**New source:** `article/25_analytic_global_bridge_v23.tex`.

Let `K` be a compact analytic class, modulo one simultaneous global `SE(2)` action, with persistent lifted channels and singleton admissible periodic gluing.  For finite order `M`, let `D_M(T)` contain all measured channel onsets and the two half-line action jets through order `M`; the lifted labels `(a,b,ell)` are fixed by the design.

### Uniform finite-coordinate resolution

For every integer `q >= 0` and every `epsilon>0`, V23 proves that there are finite `M` and `eta>0` such that

`||D_M(T)-D_M(T')|| < eta  =>  d_q(T,T') < epsilon`

uniformly on `K`.

The proof is by compactness.  If the statement failed, one would obtain globally separated table pairs whose data agree to increasing finite order.  Compact subsequences give limiting tables with identical data at every finite order, hence identical complete intrinsic lifted-channel data.  The all-order inverse and singleton admissible periodic gluing then force the two limits to be the same table, contradicting the global separation.

This is a stability bridge on a compact analytic class; it does not use noisy Taylor-series analytic continuation as an algorithm.

### One growing-order sequence for all fixed global losses

Assume that every fixed `D_M` is uniformly consistently estimable in the physical experiment.  The diagonal theorem chooses a single deterministic `M_n -> infinity`, increasing arbitrarily slowly, and measurable minimum-distance estimators `T_hat_n` such that for every fixed integer `q` and every `epsilon>0`,

`sup_T P_T{ d_q(T_hat_n,T)>epsilon } -> 0`.

The diagonal construction is simultaneous over `q=0,...,m` at stage `m`, so the same `M_n` works for all fixed `C^q` losses.  No uniform-in-`M` lower singular-value estimate is inserted.  A sharp analytic minimax rate is not claimed.

This supplies the missing `M_n -> infinity` and global-loss passage while preserving the honest fixed-order conditioning statement of v22.

## C22-M4 / R22-2: analyze richer physical information instead of renaming the endpoint subexperiment

V23 keeps the v22 endpoint Gaussian experiment but places it in an explicit hierarchy and derives two richer experiments from the record spaces for which the historical coupling was actually proved.

### 1. Complete stopped endpoint--time experiment: Poisson boundary shift

**New source:** `article/18c_full_endpoint_time_information_v23.tex`.

The historical transfer theorem compares the selected per-preparation record consisting of the two signed endpoints, residual preparation-to-first-impact time, and a failure atom.  The adaptive theorem propagates this comparison through the entire stopped transcript, including designs, failures and stopping time.  V23 therefore analyzes this same record.

Conditional on success at design `ell`, the boundary law has density

`q_{ell,0}(u,v,r) = rho_ell(u,v) 1_{0<r<w_ell(u,v)}`,

with positive density at the moving ceiling `r=w_ell(u,v)`.

With `k_n` successful records, use local shape scale `1/k_n` and gap scale `1/(j_n k_n)`.  If `y=k_n(w-r)` is the scaled null ceiling slack, V23 proves convergence in Le Cam distance to independent Poisson point processes with intensities

`alpha_ell rho_ell(u,v) 1_{y>U_ell(u,v)z} du dv dy`.

The limit is generally non-dominated.  The proof explicitly removes the codimension-two `r=0, w=0` corner: by coarea its endpoint collar has area `O(1/k_n)`, its residual length is `O(1/k_n)`, hence its one-record mass is `O(1/k_n^2)` and its accumulated mass over `O(k_n)` records is `o(1)`.  On the remaining boundary layer, a binomial-to-Poisson total-variation bound gives the point-process limit; the common bulk has centered likelihood variance `O(1/k_n)` and contributes only the Poisson compensator at first order.

The positive finite design from v22 makes the support-velocity map injective, so every fixed labelled finite contact-jet coordinate is visible at shape scale `1/k_n` and gap at `1/(j_n k_n)`.

Before capping, the stopped boundary law factorizes exactly into a negative-binomial waiting count and iid successful endpoint--time marks.  Under `j_n=o(sqrt(k_n))`, the waiting-count Hellinger distance at this fastest scale is `O(j_n^2/k_n)=o(1)`, so waiting counts are ancillary here.  With `k_n tau^{j_n}->0`, the complete stopped endpoint--time experiment transfers to actual finite bridges by the existing v22 stopped coupling.

### 2. Residual time removed, waiting counts retained: two-speed Gaussian experiment

**New source:** `article/18d_count_endpoint_multirate_v23.tex`.

After residual time is integrated out, the endpoint density vanishes linearly at its moving support.  Waiting counts then expose the success probability `p ~ exp(-j gamma)`.

Let `lambda=D_vartheta gamma`, choose `v_gamma` with `lambda(v_gamma)=1`, and let `H_gamma=ker lambda`.  At

`k_n delta_n^2 log(1/delta_n) -> 1`

use

`vartheta = b/(j_n sqrt(k_n)) v_gamma + delta_n h`, `h in H_gamma`,

and

`g = g0 + delta_n a/j_n`.

The negative-binomial waiting-count likelihood gives a one-dimensional Gaussian shift in `b` with information one.  The slow `(a,h)` directions are asymptotically invisible to that count likelihood.  Conversely, under

`log(j_n sqrt(k_n))/j_n^2 -> 0`,

the fast `v_gamma` perturbation is invisible to the endpoint marks.  The latter retain the v22 Gaussian moving-support experiment restricted to `R x H_gamma`.  Exact stopped Bernoulli-mark factorization gives independence of the two Gaussian factors.

Thus the count--endpoint record has a genuine two-speed limit:

- hyperbolic shape direction: `(j_n sqrt(k_n))^{-1}`;
- iso-hyperbolic shape directions: `delta_n`;
- gap: `delta_n/j_n`.

Again the stopped finite-to-boundary transfer gives the same local experiment for actual finite bridges.

### 3. Waiting counts also removed: the v22 endpoint-output Gaussian experiment

The v22 non-dominated/common-collar endpoint theorem remains active as the third observation level.  It is no longer called complete physical information.  The three sigma-fields and their different critical scales are stated explicitly in `article/01b_observation_hierarchy_v23.tex`.

## C22-M5 / R22-5: exact-head build verification

The new workflow `.github/workflows/a2-v23-native-build.yml` is branch-specific and records the exact commit before running the native TeX build and numerical diagnostics.  It is configured to:

1. archive the exact source and commit;
2. install the native TeX/Python dependencies;
3. run `tools/build_submission.py`;
4. run `check_boundary_information.py` under normal and optimized Python and compare the outputs;
5. reject unresolved references/citations and fatal TeX diagnostics;
6. record PDF hashes;
7. upload exact-source and build artifacts.

The workflow has repeatedly been triggered on exact manuscript-source pushes, but GitHub currently returns a failed job with `steps=null` before checkout or any other runner command begins.  Explicit reruns have the same zero-step failure mode.  The revision therefore does **not** claim a successful native-build certificate.  It also does not label the zero-step runner failure a TeX failure.  `A2_REVISION_V23_VERIFICATION.md` records the exact source commit and workflow evidence.

## R22-4: preserve the v22 repairs

The following accepted v22 results remain active and are not weakened:

- weighted all-order half-line inverse;
- finite-truncation envelope cancellation and homogeneous action-jet filtration;
- determinant-one signed inverse at every order;
- even-flight same-type physical design;
- fixed laboratory endpoint coordinates for the local statistical family;
- one reference-based cap sequence with the correct quantifier order;
- explicit observation sigma-fields;
- non-dominated original endpoint family versus dominated common-collar LAN representative;
- parameter-independent comparison kernels;
- identifiable-subspace treatment of singular information;
- finite positive physical designs for every fixed finite jet order;
- stopped endpoint--time finite-to-boundary transfer;
- no total-variation claim for the full growing collision array.

## Secondary comments and source organization

- The exact success-ratio input for the reference cap is now traced directly to Theorem `thm:g-stability`, equation `eq:g-competition`.
- `article/18e_compatible_rates_v23.tex` gives one simultaneous nonempty rate regime:
  `delta_n=n^{-1}`, `k_n=floor(n^2/log n)`, `j_n=2 ceil(C log n)` with `C>|log tau|^{-1}`.
- The active introduction states explicitly that finitely many measured channel **families** are not finitely many scalar observations; each contains a continuum signed support germ.
- Fixed-order quantitative conditioning is never promoted to a uniform-in-order bound.
- The title/abstract/introduction are theorem-first.  Revision chronology and detailed referee provenance are kept in repository response/manifest files rather than used as proof authority.

## Resulting theorem architecture

The active deterministic chain is

`relative boundary law`
`-> all-order signed inverse`
`-> intrinsic lifted-channel analytic copies`
`-> admissible symmetry/lattice-holonomy gluing`
`-> fully intrinsic periodic table rigidity`.

The active statistical chain is

`stopped endpoint--time transcript`
`-> non-dominated Poisson boundary experiment`
`-> count--endpoint two-speed Gaussian experiment`
`-> endpoint-output Gaussian coarsening`
`-> growing-order compact analytic/global reconstruction`.

This is the v23 revision submitted for a fresh referee assessment.  The only unresolved item recorded as mechanical rather than mathematical is a successful execution of the exact-head native-build workflow on an available GitHub runner.
