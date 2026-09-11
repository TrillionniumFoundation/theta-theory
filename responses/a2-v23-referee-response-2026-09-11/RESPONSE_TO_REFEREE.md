# Response to the A2 v22 independent referee report

**Revision:** A2 v23  
**Revision branch:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Report answered:** `reviews/a2-v22-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Report branch head used as revision base:** `7057ec51b341264fa3752a0e5eb466650579bab1`  
**Reviewed v22 revision head:** `ea97acaa8efb1f4009df5394af58cf9c367a13ab`  
**Active entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`

We thank the referee for separating the defects already repaired in v22 from the remaining architectural questions.  The v23 revision does not downscale the determinant-one inverse, remove the non-dominated statistical results, or replace the global theorem by a weaker local statement.  It builds outward from the v22 core in the directions requested by the report.

The principal changes are theorem-level rather than rhetorical:

1. the global analytic theorem is reformulated on intrinsic **lifted-channel** data, with no common laboratory placement of distinct channel frames;
2. obstacle placement and periodic deck/lattice placement are reconstructed by an explicit gluing/holonomy theorem on a connected measured network;
3. the complete stopped endpoint--time acquisition transcript is given a fastest-scale Poisson boundary limit;
4. after residual time is removed, waiting counts and endpoints are analyzed jointly in a two-speed Gaussian experiment;
5. a compact analytic finite-coordinate theorem and diagonal sieve argument connect fixed-order physical information to growing-order global table recovery;
6. the manuscript is reorganized around the active theorem chain, while the mathematical modules supporting the v22 repairs are retained.

## C22-M1 / R22-1. Intrinsic global rigidity rather than supplied common registration

**Addressed in:**

- `article/23c_analytic_continuation_v23.tex`;
- `article/23b_intrinsic_multichannel_rigidity_v23.tex`.

The referee correctly identified two different inverse problems hidden by the v22 phrase “registration forgotten.”  V23 therefore defines the data before the theorem and uses the same periodic channel index as the geometric setup.

A measured channel is `e=(a,b,ell)`, where `ell` is the marked lattice deck displacement.  For each channel, the **intrinsic signed lifted-channel datum** contains:

- the lifted label `(a,b,ell)`;
- the physical onset;
- the two same-type signed endpoint-law germs;
- the sign convention for the transverse endpoint coordinate.

The law is expressed only in that channel's adapted frame.  No Euclidean placement of this frame relative to the periodic lattice or to another measured channel is supplied.

The v22 all-order inverse, followed by the new standalone analytic-continuation lemma, recovers complete oriented analytic copies of the two incident obstacle **lifts** in the edge frame.  V23 then treats the periodic placement problem itself as unknown.

Let `Lambda_abs` be the marked abstract Euclidean lattice and let `iota` be an unknown oriented Euclidean realization of it.  If an incidence `(e,sigma)` has deck offset `nu(e,sigma)`, a periodic gluing consists of `iota` and edge-frame placements `A_e in SE(2)` satisfying

`tau_{-iota(nu(e,sigma))} A_e C_{e,sigma}
 = tau_{-iota(nu(f,sigma'))} A_f C_{f,sigma'}`

whenever the two incidences belong to the same quotient obstacle orbit.  After translating each recovered lift back by its deck vector, all copies of the same quotient obstacle must coincide.

The quotient of these gluings by one simultaneous global `SE(2)` action is the data-determined periodic gluing space `G_per(D)`.  The new classification theorem proves a bijection

`periodic table realizations modulo one global SE(2)  <->  G_per(D)`.

Thus the remaining ambiguity is classified rather than hidden in an external registration assumption.

### Obstacle symmetries

For an oriented connected real-analytic strictly convex closed curve, equality of the complete curvature signature at two points is equivalent to the existence of an orientation-preserving Euclidean symmetry carrying one framed point to the other.  A circle therefore has a genuine continuous phase ambiguity; a cyclically symmetric obstacle can have a finite one.  V23 records those ambiguities as part of the gluing space.

### Periodic lattice holonomy

The interface audit also makes explicit a periodic issue which the registered v22 theorem did not have to confront.  A signature-rigid spanning tree can propagate relative obstacle placements, but by itself it need not determine the orientation of the marked periodic lattice relative to the channel network.  V23 therefore tracks deck translations rather than suppressing them.

For a signature-rigid closed channel cycle, the recovered frame transitions compose to a translation `v_c` in the starting channel frame.  The same cycle has marked deck displacement

`eta_c = sum epsilon_i ell_{e_i}`.

Every realization satisfies the holonomy identity

`iota(eta_c)=v_c`.

If `eta_c != 0`, this fixes the orientation-preserving realization of the marked Euclidean lattice relative to the starting channel frame.  Such a cycle is called **lattice-anchoring**.

Hence a signature-rigid spanning tree plus one signature-rigid lattice-anchoring cycle gives a fully intrinsic periodic rigidity theorem: the complete labelled periodic table is determined up to one simultaneous global Euclidean motion, with no absolute contact point, tangent frame, inter-channel placement, or lattice orientation relative to the channel frames supplied in advance.

If an oriented ambient lattice frame is independently known physical structure, the anchoring cycle is unnecessary and the signature-rigid spanning tree alone suffices.  If all channel and lattice placements are supplied, the v22 registered theorem is recovered as a special case.

This directly answers the report's Sections 4.2--4.3: the data model, group action, graph connectivity, periodic lift labels and placement induction are now explicit theorem ingredients rather than prose qualifications.

## C22-M2. Top-four conceptual consequence

V23 strengthens the global consequence rather than changing the venue target or narrowing the result.

The global chain is now

`intrinsic signed lifted-channel laws
 -> all-order framed contact inverse
 -> complete analytic lifted obstacle copies
 -> symmetry + lattice-holonomy gluing
 -> global periodic table up to one Euclidean motion`.

Relative placement of measured channel frames and the periodic deck geometry are inside the inverse theorem.  The exact obstruction is the periodic gluing space; the paper then supplies a concrete uniqueness mechanism through signature-rigid propagation plus a nonzero anchoring holonomy.  This is materially stronger than the registered v22 corollary while preserving the determinant-one local mechanism.

## C22-M3 / R22-3. Bridge fixed-order statistics to analytic/global recovery

**Addressed in:** `article/25_analytic_global_bridge_v23.tex`.

The referee correctly observed that v22 placed an all-order analytic exact theorem beside a fixed-finite-jet local statistical theorem without an `M_n -> infinity` passage.  V23 adds two results.

### Finite-coordinate resolution on a compact analytic class

Let `K` be a compact analytic class, modulo one simultaneous global `SE(2)` action, with persistent lifted channels and **singleton periodic intrinsic gluing**.  For each `M`, let `D_M(T)` contain the channel onsets and the action derivatives through order `M`; the lifted channel labels and deck displacements are fixed by the experimental design.

For every global `C^q` tolerance `epsilon>0`, the new theorem proves that there exist finite `M` and `eta>0` such that

`||D_M(T)-D_M(T')|| < eta  =>  d_q(T,T') < epsilon`

uniformly on `K`.

The proof is by compactness.  Otherwise one obtains globally separated subsequences agreeing to increasing finite order.  Passing to limits gives equality of every finite action jet, hence equality of the full intrinsic lifted-channel data, and the intrinsic periodic rigidity theorem forces equality of the limiting tables, a contradiction.

A sufficient geometric model for the singleton-gluing hypothesis is a persistent signature-rigid spanning tree together with a persistent lattice-anchoring cycle.  With a known oriented ambient lattice frame, the spanning tree suffices.

This is a global stability statement which avoids pretending that noisy Taylor-series analytic continuation is a stable numerical algorithm.

### Diagonal growing-order reconstruction

Assume that for every fixed `M` the physical experiment admits uniformly consistent estimators of `D_M`.  V23 proves that one can choose a deterministic nondecreasing `M_n -> infinity` and minimum-distance estimators on the compact analytic class whose global `C^q` risk tends to zero uniformly for every fixed `q`.

The sequence `M_n` may grow arbitrarily slowly.  No uniform-in-`M` lower singular-value bound is assumed.  This supplies the missing growing-order/global-loss passage while preserving the honest v22 statement that the quantitative signed-jet inverse is fixed-order.

A sharp analytic minimax rate is not claimed; obtaining one would require new uniform-in-order conditioning estimates.  The revision states this boundary explicitly.

## C22-M4 / R22-2. Complete the physical information theorem rather than narrow the headline

V23 takes the stronger path suggested by the report.

### A. Endpoint--time Poisson boundary experiment

**Addressed in:** `article/18c_full_endpoint_time_information_v23.tex`.

The historical v6 transfer theorem is already proved for a per-preparation record retaining the two endpoints, residual preparation-to-first-impact time, and a failure atom.  The adaptive theorem already compares the entire stopped transcript built from those records, including designs, failures, and stopping time.  V23 therefore studies that same record rather than inventing a new observation space.

Conditional on success at design `l`, the boundary record has density

`q_{l,0}(u,v,r) = rho_l(u,v) 1_{0<r<w_l(u,v)}`,

with positive density at the moving ceiling `r=w_l(u,v)`.  With `k_n` successful records, shape perturbations of order `1/k_n` and gap perturbations of order `1/(j_n k_n)` move that ceiling by order `1/k_n`.

The scaled ceiling slacks form independent Poisson point processes with intensity

`alpha_l rho_l(u,v) 1_{y>U_l(u,v) z} du dv dy`.

The limit is generally non-dominated.  The finite positive design from v22 makes the family of support velocities injective, so every fixed labelled finite contact-jet coordinate is identifiable at this fastest scale.

The proof separates the `1/k_n` boundary layer from the common bulk.  The boundary layer has rare-cell probabilities of order `1/k_n` and Poissonizes; after its compensator is extracted, the centered bulk likelihood has vanishing variance.  Thus the limit is a boundary-shift Poisson experiment rather than a Gaussian LAN experiment.

Under `j_n=o(sqrt(k_n))`, the negative-binomial waiting count is asymptotically ancillary at this fastest `1/k_n` shape scale.  The reference cap is still adequate, and the existing stopped finite-to-boundary theorem transfers the entire endpoint--time transcript to actual finite bridges if `k_n tau^{j_n}->0`.

### B. Waiting-count plus endpoint multirate experiment after residual time is removed

**Addressed in:** `article/18d_count_endpoint_multirate_v23.tex`.

Once residual time is integrated out, the fastest ceiling layer disappears and the endpoint density vanishes linearly at its moving boundary.  V23 then retains the waiting counts jointly with endpoints.

Let `lambda = D_vartheta gamma` at the reference channel, choose `v_gamma` with `lambda(v_gamma)=1`, and put `H_gamma=ker lambda`.  At the endpoint scale

`k_n delta_n^2 log(1/delta_n) -> 1`,

use

`vartheta = b/(j_n sqrt(k_n)) v_gamma + delta_n h`, with `h in H_gamma`,

and `g=g_0+delta_n a/j_n`.

The stopped waiting count is negative binomial.  The exact success asymptotic gives

`log(p_n(b,a,h)/p_n(0)) = -b/sqrt(k_n) + o(k_n^{-1/2})`.

Hence the waiting-count likelihood has a one-dimensional Gaussian shift limit with information one.  The slow iso-hyperbolic directions are invisible to this count likelihood.

Conversely, the fast hyperbolic perturbation is invisible to the endpoint experiment because

`k_n eta_n^2 log(1/eta_n) = log(j_n sqrt(k_n))/j_n^2 -> 0`.

The endpoint marks retain the v22 Gaussian shift on `(a,h)` with the positive-definite information matrix restricted to `R x H_gamma`.  Exact factorization of the stopped Bernoulli-mark experiment gives independence of the two limiting factors.

Thus the count--endpoint observation has a genuine two-speed Gaussian limit:

- hyperbolic shape direction: `(j_n sqrt(k_n))^{-1}`;
- iso-hyperbolic shape directions: `delta_n`;
- gap: `delta_n/j_n`.

The actual finite-bridge experiment has the same limit by the stopped physical transfer.

### C. The endpoint-output theorem is retained as the next coarsening

The v22 non-dominated/common-collar endpoint Gaussian theorem remains active.  It is no longer advertised as all physical information.  Instead it is the third level of an explicit hierarchy:

1. endpoints + residual time + waiting/stopping transcript: Poisson boundary experiment at the fastest scale;
2. residual time removed, waiting counts retained: two-speed Gaussian count--endpoint experiment;
3. residual time and waiting counts removed: moving-endpoint Gaussian experiment.

This strengthens the paper rather than narrowing its title.

## C22-M5 / R22-5. Canonical build

A new exact-branch workflow, `.github/workflows/a2-v23-native-build.yml`, is included in this revision.  It is configured to:

1. check out and record the exact revision head;
2. archive the exact manuscript source;
3. install a native TeX/Python toolchain;
4. run `tools/build_submission.py`;
5. run the boundary diagnostics under normal and optimized Python;
6. reject unresolved references/citations and fatal LaTeX diagnostics;
7. record source and PDF hashes;
8. upload source and build artifacts.

The source revision is not described as submission-ready unless this workflow actually executes successfully.  Its exact run status is recorded separately in `A2_REVISION_V23_VERIFICATION.md` after each canonical source correction.

## R22-4. Preserve the v22 repairs

All mathematical repairs which the report explicitly accepted remain active:

- the weighted all-order half-line inverse;
- finite-truncation envelope cancellation and homogeneous jet filtration;
- determinant-one all-order signed inverse;
- even-flight same-type convention;
- fixed laboratory observation coordinates;
- one reference-based cap sequence independent of compact local parameter sets;
- the exact observation-sigma-field hierarchy;
- the non-dominated/common-collar distinction;
- parameter-independent comparison kernels;
- the identifiable-subspace formulation for singular information;
- fixed-order finite positive physical designs;
- the stopped endpoint/residual-time finite-to-boundary transfer;
- the statement that full growing collision histories are not compared in total variation.

No accepted v22 theorem was removed merely to improve the venue assessment.

## R22-6. Reorganize around the strongest theorem chain

The active title is now

*Boundary laws, intrinsic rigidity, and multiscale physical information in dispersing billiards*.

The abstract and introduction are theorem-first rather than revision-first.  The active manuscript is organized around

`relative boundary law -> all-order signed inverse -> intrinsic lifted-channel gluing -> periodic analytic rigidity`

and

`endpoint-time Poisson experiment -> count-endpoint multirate experiment -> endpoint Gaussian coarsening -> growing-order analytic/global bridge`.

Historical modules required by the proofs remain in the source, but revision-history language and the long list of referee memoranda have been removed from the mathematical narrative.  Provenance is retained in repository response/manifest documents rather than used as proof authority.

## Secondary comments

The smaller points in Section 9 of the report are also addressed.

- **9.1--9.3 Data model and group action.**  The intrinsic lifted-channel datum is defined before the global theorem.  The same `(a,b,ell)` channel convention as the geometric setup is used.  Absolute laboratory placement, quotient modulo one global `SE(2)`, and unrelated per-channel frames are separate objects.  Connectivity, deck displacement, obstacle symmetry and lattice holonomy are explicit.  A signature-rigid spanning tree plus a nonzero anchoring cycle gives a constructive fully intrinsic periodic placement theorem.
- **9.4 Cap citation.**  `article/18e_compatible_rates_v23.tex` points the cap success-ratio estimate directly to Theorem `thm:g-stability`, equation `eq:g-competition`, and explains how the smooth prefactor and `sinh(j gamma)^{-1}` factor give the `1+o(1)` ratio under `j_n delta_n -> 0`.
- **9.5 Compatible rates.**  The same file gives the explicit choice `delta_n=n^{-1}`, `k_n=floor(n^2/log n)`, `j_n=2 ceil(C log n)` with `C>|log tau|^{-1}`.  It simultaneously satisfies the endpoint-critical, slow-hyperbolic-variation, stopped-transfer, endpoint--time and two-speed conditions.
- **9.6 Fixed-order conditioning.**  The introduction and global bridge repeatedly state that the compact lower singular-value bound is fixed-`M`; no uniform-in-`M` conditioning is claimed.
- **9.7 Finite channel data.**  The introduction explicitly says that finitely many lifted channel families are not finitely many real numbers: each channel supplies a continuum support germ.
- **9.8 Analytic continuation.**  `article/23c_analytic_continuation_v23.tex` gives a standalone lemma: equality of a nonempty registered analytic boundary germ implies equality of the full connected boundary image, with a proof by analytic curvature continuation and uniqueness of the Frenet system.
- **9.9 Structure.**  Mathematical modules are retained, but the active title/abstract/introduction and part headings expose the dependency graph directly.
- **9.10 Proof provenance.**  The article is self-contained; the acknowledgment is reduced to a concise provenance statement, while detailed AI/referee history remains outside the theorem narrative.

## Summary

V23 accepts the referee's central diagnosis but takes the strengthening route throughout.  The determinant-one inverse remains all-order.  The global theorem no longer obtains channel placement or periodic deck placement for free from a common laboratory registration.  The physical theorem now treats the endpoint--time transcript and the waiting-count channel rather than calling the endpoint coarsening complete.  The exact analytic theorem and the finite-order statistical theorem are connected by a growing-order compact analytic reconstruction principle.

The remaining mechanical question is the exact-head native build.  The mathematical revision is committed independently of that infrastructure status, and the verification record reports the result without converting a runner failure into either a theorem failure or a false build certificate.
