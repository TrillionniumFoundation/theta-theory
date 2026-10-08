# External top-four referee report on A2-DYN revision 41

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v41-referee-response-2026-10-08`, `revision/a2-dyn-v41-referee-copy-2026-10-08`  
**Reviewed commit:** `e8bb719f3100f16cb945ab57c2b3408d19f678dc`  
**Reviewed repository tree:** `d3eb59923ab0a59b6dc6f83a9bd94bd9f9d83578`  
**Ordinary source payload tree:** `a63fd6270c19463cbc4c21e128fe87ab194a1ebc`  
**Active manuscript directory:** `papers/A2-DYN-v41-referee-response`  
**Active mathematical source:** eighty-nine numbered core modules  
**New mathematics since the latest external report:** modules 84--89; modules 84--86 were landed as revision 40 and modules 87--89 as revision 41  
**Immediate revision-40 author commit:** `d07c73f9db6a27c216fcfb2f32f844d63858c90b`  
**Controlling external report:** `reviews/a2-dyn-v39-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `a76fcf9d6ef7288ea324fed327c4f2f0ce088461` / `34fd05b1740816104f38ca84c75826b11eec1694`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

This recommendation should not obscure the scale of the progress in revisions 40 and 41.

The latest external report found that the paper had classified the occupation resonance group but had not converted the classification into fixed-collision-count coefficient asymptotics. In particular, Abel and partial-sum cancellation did not control the coefficient at a prescribed collision count, and the noncentral occupation-frequency contribution remained unevaluated.

The present manuscript addresses that objection directly. Revision 40 develops a full fixed-roof-band operator theory on the entire occupation torus. It then identifies the finite resonance group, proves that every occupation resonance has zero roof coordinate, computes the physical endpoint residue of each resonance, and obtains a fixed-radius exact-index local theorem for a fixed roof interval. The resulting main term contains a finite, nonnegative arithmetic coefficient determined by the phase-class masses of the actual section.

Revision 41 goes further. It retains spectral branches as they move into the unit disk when the radius changes, evaluates their local Fourier integrals, and produces a finite Gaussian transition kernel which is uniform through changes of arithmetic type. It also proves a conditional Gaussian bridge for the genuine return path under the unchanged exact event, subject to the natural microscopic lower-mass condition. Finally, it proves a radius-uniform unmodulated local law after averaging over one fixed finite packet of return indices, and it gives an exact criterion for when the unmodulated single-index interval law itself is uniform.

I audited the new modules

- `core/84_occupation_cut_power_bounds.tex`;
- `core/85_occupation_holonomy_and_residues.tex`;
- `core/86_fixed_count_arithmetic_local_law.tex`;
- `core/87_uniform_resonance_transition.tex`;
- `core/88_exact_event_return_bridges.tex`;
- `core/89_residue_filters_and_denominators.tex`;

and their use in the fifth and sixth leading theorems. I found no decisive counterexample, collision/return endpoint mismatch, Fourier-sign error, missing section-mass factor, covariance-normalization error, or illegitimate inference from an Abel average to a fixed coefficient.

The new chain is mathematically substantial. In particular, the paper now contains what appears to be a genuine exact-index **fixed-interval** local theorem at each fixed radius, with the correct arithmetic modulation, together with a radius-uniform transition formula and an exact-event bridge theorem.

The negative recommendation is nevertheless forced by the theorem which still organizes the title and the raw-inversion portion of the manuscript. The following remain unproved:

1. the common pointwise roof correction for the actual return record;
2. the complete high-roof-frequency complement and critical/singular edge sum;
3. a pointwise roof-density local limit;
4. vanishing of every nontrivial section endpoint residue for the concrete family;
5. the radius-uniform **unmodulated** exact-index interval law without the residue criterion;
6. the full raw mixed-density theorem stated in the inherited pipeline.

The interval theorem is not a density theorem. The existence of one slowly shrinking interval sequence is not a prescribed shrinking-scale estimate, a Lebesgue differentiation theorem with uniform constants, or control of the raw Fourier tail. Moreover, the new arithmetic calculation shows that the exact-index interval law naturally carries a factor

\[
\mathfrak a_R(k,n,m),
\]

which need not equal one unless the section phase masses are uniform. Thus the original unmodulated endpoint is not merely missing a technical estimate: it requires a concrete residue theorem, or a reformulation which displays the arithmetic factor.

At the requested benchmark, a very large article entitled around raw local inversion should either prove that raw endpoint or present a general theorem of sufficiently broad independent significance that the unfinished endpoint no longer governs the editorial claim. Revision 41 does neither yet, although it narrows the gap much more sharply than any earlier version.

## 2. Frozen source, chronology, and qualification

Both reviewed author branches resolve to

`e8bb719f3100f16cb945ab57c2b3408d19f678dc`.

The repository tree is

`d3eb59923ab0a59b6dc6f83a9bd94bd9f9d83578`.

The active paper is

`papers/A2-DYN-v41-referee-response`.

The substantive revision-41 author commit is `4818a3f291171966fc4bda6052d99047d7663bad`. The final reviewed commit makes the quantifier in the uniform transition display explicit: the collision count `m` tends to infinity and is not itself a variable under the supremum. It also regenerates the complete source manifest. No mathematical proof is otherwise altered by that final correction.

The source manifest records:

- eighty-six inherited core modules retained byte-for-byte;
- ninety-nine inherited Python files retained byte-for-byte;
- three new core modules in revision 41;
- all inherited mathematical labels, bibliography, and the compiled A--X synopsis retained;
- the active payload tree listed above;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `common_pointwise_return_correction_proved: false`;
- `full_return_complement_proved: false`;
- `unmodulated_radius_uniform_exact_index_LLT_proved: false`;
- `independent_human_review: false`.

The exact-source qualification workflows completed successfully at the final reviewed SHA:

- response branch run `37727389724`;
- referee-copy branch run `37727418486`.

These runs establish source identity, native compilation, manifest consistency, normal/optimized agreement, finite regression checks, and proof-page rendering at the exact event SHA. They do not certify the continuum anisotropic-space arguments, holonomy construction, peripheral-spectrum classification, transition expansion, or conditional bridge theorem.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v41-external-top4-review-2026-10-08/`.

No author source, prior report, workflow, or unrelated path is intentionally modified.

## 3. Scope of this review

I did not attempt to re-prove all eighty-nine modules. The substantive audit concentrates on the new chain which is intended to answer the controlling report:

1. linear rather than exponential complexity of the iterated section cuts on an already regular inverse collision curve;
2. the weighted weak, stable, and unstable inequalities on the full occupation torus;
3. the passage from polynomial power bounds to a full fixed-band peripheral spectral description;
4. exclusion of nonzero roof coordinates from occupation resonances;
5. the physical rank-one projection and endpoint residue at every resonance;
6. the resonant quadratic expansion and its covariance;
7. the fixed-radius exact-index arithmetic local theorem;
8. the uniform spectral reduction and transition kernel through changes of arithmetic type;
9. the sharp interval passage;
10. pinned finite-dimensional bridge factorization;
11. the unnormalized fourth-moment estimate and path tightness;
12. the exact passage from collision time to return time;
13. the zero-residue criterion and fixed finite packet theorem;
14. the remaining distinction between fixed intervals and pointwise roof density.

The earlier action-weighted collision norms, strong-space faithfulness, exact section multiplier, covariance positivity, finite-cover mixing, return/occupation disintegration, endpoint envelopes, and corrected parameter-varying Portmanteau step are treated as source-pinned inherited inputs. They remain load-bearing and still require independent specialist verification.

## 4. Linear occupation cuts on a regular inverse curve

The key observation in module 84 is that the true section occupation should be counted after the ordinary collision singularity and homogeneity cuts have already produced a regular inverse branch.

For one such branch `U`, every intermediate image `T^j U` is a regular stable graph. A horizontal or vertical side of one of the finitely many section rectangles is crossed at most once after the fixed chart cuts. Hence the union of section-boundary crossings over times `0,...,m-1` has at most `K m` points. The whole occupation itinerary is constant on the complementary intervals.

This is the correct place to obtain a polynomial complexity bound. Multiplying the number of cells in a one-step partition over `m` steps would instead produce an irrelevant exponential bound.

The manuscript then refines the old geometric sums. The total Jacobian sum and the inverse-Jacobian power sum lose at most one factor proportional to the number of cuts. The length-weighted sums use

\[
\sum_i |V_i|^{\varsigma}
 \le r^{1-\varsigma}|U|^{\varsigma}.
\]

The displayed estimates use a slightly weaker linear loss, which is harmless.

I found this counting mechanism coherent. The specialist point is geometric rather than algebraic: every intermediate image called regular must already include all collision singularity and homogeneity cuts, and the section sides must remain uniformly transverse to the stable graphs in the chosen local coordinates. The paper states these requirements and refers back to the exact-section multiplier geometry. A human billiards expert should verify them against the adopted common-space construction.

## 5. Matched pairs and the unstable norm

Counting cuts on one curve is not enough for the unstable seminorm. The manuscript therefore refines the old matched pairs by removing connectors which cross a section side at an intermediate time.

On a retained pair, the two occupation itineraries agree exactly. The occupation factors then cancel in the difference of the accumulated weights. The roof-action estimate supplies the same `C epsilon^(1-q)` bound as in the inherited argument.

The removed pieces are charged to the unmatched family. Their terminal lengths remain `O(epsilon)`, and the old inverse-Jacobian sum acquires the explicit polynomial multiplicity. This yields the additional stable-norm error

\[
C_B(1+m) C_4^m\epsilon^{\varsigma}\|h\|_s.
\]

The exponents used in the paper keep every power of `epsilon` strictly above the unstable exponent `gamma`.

The organization is mathematically correct in form. The principal specialist check is that a connector is retained only if every intermediate connector is regular and remains in the same occupation cell as its partner; otherwise the entire relevant interval must be charged to the unmatched part. The manuscript states precisely this convention. I found no omitted exponential word-count factor in the displayed bookkeeping.

## 6. Full occupation-torus Lasota--Yorke inequalities

For each fixed roof band, the new inequalities have polynomial weak growth and exponentially contracting leading strong coefficients:

\[
|\mathscr T_\theta^m h|_w
 \le C_B(1+m)|h|_w,
\]

\[
\|\mathscr T_\theta^m h\|_s
 \le C_B(1+m)(\theta_*^{(1-\varsigma)m}+\Lambda^{-qm})\|h\|_s
     +C_B(1+m)|h|_w,
\]

and

\[
\|\mathscr T_\theta^m h\|_u
 \le C_B(1+m)\Lambda^{-\gamma m}\|h\|_u
     +C_B(1+m)C_4^m\|h\|_s.
\]

The block/equivalent-norm construction is in the right order. The roof band is fixed first. One then chooses a block length for which the leading stable and unstable coefficients contract, and only afterwards chooses the coefficient of the unstable seminorm in the equivalent norm.

Iteration produces a Doeblin--Fortet inequality with a polynomial weak term. This suffices for quasi-compactness and an essential radius below one. The proof correctly does not claim uniform weak power boundedness at this stage.

I found no algebraic inconsistency in this passage. Constants are allowed to depend on the fixed roof band, and no later theorem inserts an `m`-dependent band into these estimates.

## 7. Peripheral power boundedness

The full-band peripheral theorem must do more than show quasi-compactness. Polynomial power growth alone allows semisimple unit-circle eigenvalues but must rule out Jordan blocks.

The manuscript uses bounded physical pairings of smooth densities and smooth global tests. In the finite-dimensional peripheral expansion, a nonzero nilpotent part would produce a positive-degree exponential polynomial in `m`. Cesaro separation of the peripheral phases removes such coefficients. Strong-space faithfulness then eliminates the corresponding vectors.

This is a reasonable and noncircular way to obtain semisimplicity before invoking power boundedness. The physical Cesaro argument supplies bounded measurable eigenfunctions. Quotients of two such eigenfunctions are ordinary collision eigenfunctions; mixing and ergodicity give simplicity.

Strong-to-weak spectral stability and a finite cover of the compact joint parameter-frequency band then give uniform power boundedness and a uniform gap on compact subsets of the nonresonant complement.

This is one of the technically delicate parts of the revision. I did not find a contradiction, but an independent specialist should check that the physical pairing family is separating enough, together with the strong-space faithfulness lemma, to kill every nilpotent coefficient and not merely its global smooth pairings.

## 8. Excluding nonzero roof resonances

Module 85 strengthens the inherited resonance classification.

Stable and unstable pairs differ in section occupation by finite integer holonomies. Borel--Cantelli is applied to the exponentially shrinking probability that two contracted points lie on opposite sides of a section boundary. Independence is not used.

Multiplication around a stable--unstable rectangle gives

\[
\exp\left(ib\int_Q d\vartheta_R\right)
   \in \{e^{ivj}:j\in\mathbb Z\}.
\]

The right-hand side is countable, even when dense in the circle. On a regular product block the symplectic area of the rectangle varies continuously and strictly monotonically with one nonatomic transverse coordinate. Therefore it has no atoms. If `b` were nonzero, the displayed relation could hold only on a null set of rectangles.

This countability argument is sound in principle and avoids assuming continuity of a long occupation itinerary. It proves that every actual occupation resonance has zero roof coordinate.

The required geometric point is that the rectangle-area parameter truly has a fixed nonzero derivative on the restricted product block and that the conditional coordinates are absolutely continuous. These are the same local-product inputs used earlier in the paper. I found no immediate flaw in their use here.

## 9. Physical projections and endpoint residues

At a resonance, the manuscript compares the strong spectral projection with the orthogonal `L^2` projection of the corresponding unitary weighted composition operator. The eigenspace is one-dimensional, so

\[
\Pi_\gamma(a\nu)
  =q_\gamma\nu\int\overline{q_\gamma}a\,d\nu.
\]

Consequently the section-to-section coefficient is

\[
A_\gamma=|\nu(\eta_Rq_\gamma)|^2.
\]

This is the correct physical residue. The source identity also correctly shows why the elementary pure-occupation cancellation does not annihilate a general resonance with nonzero displacement coordinate or nontrivial scalar phase.

This point materially changes the interpretation of the earlier target. Nontrivial resonances may survive the true section endpoints. Their contribution is not an artefact of an abstract anisotropic eigenvector.

## 10. Quadratic expansion at every resonance

The continued eigenvalue near a resonance has the expansion

\[
\lambda_\gamma(\delta)
 =\zeta_\gamma\exp\left(
 i\delta\cdot\mu_R-	frac12\delta^{\mathsf T}\Omega_R\delta
 +O(|\delta|^3)\right).
\]

The paper derives the Hessian by centering the family and differentiating the physical transfer pairing. Conjugation by the circle eigenfunction leaves the covariance equal to the same joint covariance `Omega_R` which appears at the origin.

The use of local contour analyticity and a finite cover of the compact resonance locus gives uniform radii and cubic bounds. The manuscript explicitly avoids claiming that a resonance persists at every nearby radius.

I found the normalization and covariance identification coherent. The delicate step is the strong convergence of the differentiated eigenvector series and the continuity of the left functional on that series. Those properties follow if the centered vector lies in the complementary strong subspace and the local spectral gap is the one already established. This should be checked carefully by a specialist, but I found no missing mean term or sign error.

## 11. Fixed-radius arithmetic local theorem

At a fixed radius the resonance group is finite cyclic. Choosing a normalized generator gives section phase masses

\[
w_l=\nu\{x\in Y_R^*:q_*(x)=e^{2\pi il/d}\}.
\]

The arithmetic coefficient is

\[
\mathfrak a_R(k,n,m)
 =\frac d{c^2}\sum_l w_lw_{l+r_R(k,n,m)}.
\]

It is nonnegative, bounded, and has mean one over one complete residue period in the return index.

The fixed-coefficient inverse now uses long powers of the operator. Outside the finitely many resonance neighborhoods the powers decay exponentially. Inside each neighborhood, rescaling by `sqrt(m)` gives the common Gaussian, the physical endpoint residue, and the constant arithmetic phase. Finite Fourier orthogonality yields exactly the coefficient above.

This answers the central objection in the controlling report: the coefficient at a prescribed collision count is evaluated directly. It is not inferred from an Abel limit or a partial-sum estimate.

The passage to a sharp roof interval uses ordered upper and lower Fourier envelopes. Because every resonance has roof coordinate zero, both envelopes acquire the same arithmetic factor. The order of limits is fixed band, collision count to infinity, and only then band to infinity.

Within the stated fixed-radius quantifiers, I found no decisive defect in this proof.

## 12. Exact zero classes

The theorem further states that if the arithmetic coefficient is zero, the event is exactly null for every roof interval.

On the exact section-to-section event, the iterated phase equation forces a deterministic relation between the initial and terminal section phase classes. If every permitted class pair has zero initial or terminal measure, invariance makes the event null.

This is stronger than an asymptotic support statement and is consistent with the finite cyclic decomposition. The argument appears correct.

## 13. Uniform spectral reduction in the radius

The fixed-radius arithmetic data need not vary continuously when a resonance appears or disappears. Module 86 therefore first proves a radius-uniform finite spectral reduction.

A finite cover of the compact parameter-frequency band supplies local rank-one branches near every genuine resonance and exponentially decaying contours elsewhere. The branches are retained on their entire local charts, even when their modulus becomes strictly less than one at nearby radii.

This is the correct object to use before any attempt at a radius-uniform asymptotic. There is no need for a globally continuous generator of the finite resonance group.

## 14. Moving spectral peaks

Module 87 evaluates the retained branches.

For each local branch, the real part of the logarithm has a unique nearby maximum `a_j(R)`. The proof needs only continuity in the radius and analyticity in the frequency variables. Uniform negative Hessians permit a contraction-map version of the implicit function argument.

The associated data are:

- the peak frequency `a_j(R)`;
- the damping `kappa_j(R)=-log|z_j(R)|`;
- the drift `mu_j(R)`;
- the complex Gaussian curvature `H_j(R)`;
- the endpoint/partition amplitude `B_j(R)`.

At an actual resonance, the damping is zero, the roof coordinate of the peak is zero, the drift is the physical mean, and the curvature is `Omega_R`.

The transition kernel retains

\[
e^{-m\kappa_j(R)}
\]

through parameter sequences on which the branch approaches the unit circle at inverse collision scale. This is essential; setting this factor to zero or one pointwise in the radius would lose the transition regime.

The local stationary-phase calculation is uniform because the target oscillation has modulus one, the real Hessian has a common positive lower bound, and the number of charts is finite. I found no sign or normalization error in the displayed kernel.

A specialist should still check that each chart is reduced enough to contain only the one real maximum assigned to the branch and that the partition functions are extended by zero in a way compatible with the uniform stationary-phase estimate. The manuscript addresses both points.

## 15. Replacing the peak roof transform by its mass

The band-limited test contribution initially contains `q-hat(-b_j)`, where `b_j` is the roof coordinate of the moving peak.

The paper proves that this may be replaced uniformly by `q-hat(0)` after summing the damped branches. On the zero set of the damping, `b_j=0`. Away from a small neighborhood of `b_j=0`, compactness gives a positive damping minimum. Near zero, uniform continuity of the Fourier transform pays the difference.

This argument is correct and uses the damping rather than an unsupported assertion that every continued peak remains on the roof-zero plane.

## 16. Uniform exact-index interval transition formula

The resulting theorem states

\[
\sup_{R,n,k,t}
\left|m^2P_{n,m,R}(k,t;J)-|J|\mathcal L_{m,R}(k,t,n)\right|
\longrightarrow0.
\]

The collision count `m` is the asymptotic parameter, not part of the supremum. The final author correction makes this explicit.

The formula is an evaluated finite Gaussian expression, not an unevaluated operator Fourier integral. It is uniform through changes of arithmetic type. At fixed radius it reduces on central compact sets to the finite arithmetic Gaussian.

The sharp interval passage again uses positive source order and fixed-band envelopes. The manuscript also derives that the imaginary part of the complex kernel and the negative part of its real part vanish uniformly.

Within the fixed-interval topology, this is a meaningful and strong theorem. It should not be described as the unmodulated Gaussian LLT: the transition kernel retains branch damping, phase, drift, curvature, and endpoint residue.

## 17. Slowly shrinking intervals

A diagonal argument produces one deterministic sequence `h_m` tending to zero for which

\[
\frac{m^2}{h_m}P(T_n-t\in[0,h_m])
\]

is approximated by the transition kernel.

The manuscript correctly states the limitation. The sequence is chosen after the qualitative fixed-interval convergence. No rate is prescribed. This does not give a pointwise density value, a result for a user-specified shrinking sequence, or a high-frequency estimate.

The point is worth emphasizing: an existential diagonal sequence cannot replace the common coarea derivative control and complete roof-frequency complement required by the raw density theorem.

## 18. Pinned characteristic factorization

The bridge process is tied to its actual terminal record. The block perturbations are chosen so that their weighted sum is exactly zero. Consequently:

- the branch drift contributions cancel;
- the cross terms between the Fourier variable and the bridge marks cancel;
- the remaining characteristic factor is a quadratic form in the marks.

On a branch with nonzero damping, the curvature may differ from `Omega_R`. The paper uses

\[
\sup_R e^{-m\kappa_j(R)}\|H_j(R)-\Omega_R\|\to0
\]

to replace it. This is the same compactness argument used elsewhere: near the zero set the curvatures converge, and away from it the damping is exponential.

The sharp roof interval is handled without dividing by the event probability. The modulus-one path mark allows the upper-envelope error to be dominated by an unmarked positive source difference. This gives an unnormalized factorization at the natural `m^-2` scale.

I found this structure coherent.

## 19. Fourth moments and tightness

The manuscript proves the unnormalized bound

\[
\int_E
\left|\mathsf S_{r+l}-\mathsf S_r-rac lm\mathsf S_m\right|^4
\,d\nu_R^*
\le C_Jl^2m^{-2}.
\]

The fourth power is generated by differentiating a three-block chronological product. Each block is centered at the moving branch drift. The scalar centering factors cancel because the inserted coefficients have zero total weighted length.

Cauchy's estimate on a circle of radius `L^-1/2` gives `L^(p/2)` for a `p`th derivative. The Leibniz sum is bounded by `C l^2`. At least one block has macroscopic length, yielding either a four-dimensional Gaussian integral of order `m^-2` or an exponentially small complementary term.

The scaling is correct: after division by an event of mass comparable to `m^-2`, a raw pinned increment of length `l` has fourth moment of order `l^2`, and the normalized bridge increment has fourth moment of order `(l/m)^2`.

The proof is compressed but plausible. A specialist should check all allocations of derivatives when the complementary factor lies on a short block and confirm that the remaining principal blocks still provide either macroscopic Gaussian localization or exponential decay. I found no obvious allocation producing a larger order.

## 20. Conditional collision bridge

On event classes satisfying

\[
|Z|\le M,
\qquad m^2P(E)\ge\epsilon,
\]

the unnormalized characteristic factorization may be divided by the exact event mass. The fourth-moment estimate gives uniform tightness of the polygonal paths. Finite-dimensional convergence identifies the centered Gaussian bridge with covariance `Omega_R`.

The lower-mass condition is essential and is displayed rather than hidden. The theorem does not claim uniform conditioning on exact events whose arithmetic residue vanishes or whose mass falls below the natural scale.

## 21. Passage to the actual return clock

The collision bridge controls the centered occupation coordinate uniformly. Since

\[
A_{N_l,R}=l
\]

on genuine returns, the inverse occupation clock satisfies

\[
\max_l\left|N_l/m-l/n\right|\to0
\]

in the same conditional probabilities.

The exact compensation identity then gives the return path as a linear transformation of the collision path evaluated at the random return clock. Tightness and continuous limiting paths permit replacing the random clock by `l/n`.

The covariance transforms according to

\[
c^{-1}L_R^{-1}\Omega_R(L_R^{-1})^{\mathsf T}=D_R.
\]

This yields the Gaussian bridge for the original return record under the unchanged exact event. No induced-map mixing theorem and no substitute conditioning event are used.

At fixed radius, the positive arithmetic classes have a positive minimum coefficient, so the fixed-radius interval LLT supplies the denominator. Radius-uniformly, the theorem correctly retains the explicit lower-mass assumption.

I found this clock conversion and covariance normalization consistent.

## 22. The zero-residue criterion

Module 89 proves that the following are equivalent on a compact radius set:

1. every nontrivial section endpoint residue vanishes;
2. the section phase masses are uniform over the finite cyclic classes;
3. the radius-uniform unmodulated single-index interval Gaussian law holds.

The forward implication uses damping and scalar continuity to eliminate charts whose exact peripheral amplitude is zero. The converse tests every residue on a central sequence and applies finite Fourier inversion to the autocorrelation of the phase masses.

This criterion is valuable because it identifies the exact missing arithmetic statement. It does **not** prove that the criterion holds for the concrete five-rectangle section.

Accordingly, any synopsis or theorem statement for the raw return law must continue to distinguish:

- the proved transition kernel;
- the fixed-radius arithmetic factor;
- the conditional unmodulated law under zero residues;
- the still-unverified residue condition for the whole radius family.

## 23. Fixed finite packets

Let `L` be a common multiple of all possible resonance orders. Averaging over `L` consecutive exact return indices inserts the finite filter

\[
p_L(v)=L^{-1}\sum_{j=0}^{L-1}e^{-ijv}.
\]

It equals one at the origin and vanishes at every nonzero actual occupation resonance. Damping and compactness eliminate nearby subunit branches. The result is a radius-uniform unmodulated local law for one fixed finite packet.

This is stronger than the earlier diverging-window theorem. The packet length does not grow with the collision count.

It still does not identify a preassigned index. The paper states this correctly. The existence of at least one positive-mass index in each packet is useful for denominators but is not a singleton theorem for an arbitrary requested residue class.

## 24. The decisive unresolved raw endpoint

The manuscript has now largely resolved the occupation-frequency side of the fixed-interval problem. What remains is sharply localized.

### 24.1 Arithmetic residue of a preassigned exact index

At fixed radius, the correct interval theorem includes `mathfrak a_R`. Radius-uniformly, the correct object is the finite transition kernel. The paper has not proved that every nontrivial section endpoint residue vanishes.

If the inherited raw theorem is intended to have an unmodulated Gaussian main term at every exact index, the authors must prove the zero-residue condition. Otherwise the theorem must explicitly incorporate the arithmetic factor or the transition kernel.

### 24.2 Pointwise roof density

All new exact-index theorems use a fixed positive roof interval, except for one existential slowly shrinking sequence. None controls a specified shrinking interval uniformly, the derivative of the local time profile, or the entire roof Fourier tail.

The common pointwise coarea correction, critical/singular edge sum, and full return-frequency complement therefore remain indispensable.

### 24.3 Full raw mixed-density theorem

The original target combines exact lattice coordinates, exact return/collision indices, and a pointwise continuous roof coordinate. It is not proved by:

- a fixed-interval exact-index LLT;
- a finite packet LLT;
- a conditional bridge under a fixed interval;
- an existential slowly shrinking sequence;
- source total-variation approximation from the stationary physical theorem.

The repository metadata correctly leaves the full raw theorem unverified.

## 25. Significance at the requested venue level

Revisions 40 and 41 contain serious mathematics. Subject to expert verification, the following package is potentially strong:

- full occupation-torus anisotropic estimates at fixed roof band;
- finite occupation resonance classification with zero roof coordinate;
- physical endpoint residues and arithmetic support classes;
- fixed-radius exact-index interval LLT;
- uniform transition asymptotics through changes of arithmetic type;
- exact-event conditional bridges;
- a fixed finite packet theorem;
- the earlier compact-family stationary theorem and nonelliptic applications.

This is substantially beyond a routine application of a standard local limit theorem.

I am nevertheless not persuaded that the current combined manuscript meets the *Annals* / *Acta* / *Inventiones* / *JAMS* standard. The main reasons are:

1. the title and inherited architecture continue to center a pointwise raw theorem which is not proved;
2. the correct exact-index interval statement is arithmetically modulated, while the concrete vanishing of the modulation is unresolved;
3. the pointwise roof problem, including critical edges and the full tail, remains open;
4. the article is extremely large and combines completed theorems with a long unfinished raw-inversion program;
5. the most delicate anisotropic and holonomy arguments have not received an independent specialist audit;
6. the literature/significance comparison does not yet isolate a general theorem broad enough to compensate editorially for the missing endpoint.

A focused paper built around the arithmetic fixed-interval theorem, transition kernel, and exact-event bridge could plausibly be a strong dynamics/probability submission after expert verification. A top-four case for the unified article would require completion of the raw pointwise theorem or a much broader general exact-index/bridge principle with several independent applications.

## 26. Architecture and exposition

The six leading theorems distinguish their topologies more honestly than earlier versions. In particular, the latest manuscript separates:

- stationary physical singleton laws;
- compact-family action principles;
- diffusive and fine return-index windows;
- exact-index concentration;
- fixed-radius arithmetic interval laws;
- radius-uniform transition kernels;
- exact-event bridges;
- the unresolved pointwise raw theorem.

That is a significant expository improvement.

The paper remains difficult to assess as one submission. The reader must traverse eighty-nine modules, a large provenance and validation apparatus, a completed stationary theory, a completed arithmetic fixed-interval theory, and an incomplete pointwise inversion pipeline.

For journal submission, I recommend one of two architectures:

1. complete the pointwise raw theorem and retain the unified narrative; or
2. separate the completed stationary/action and arithmetic exact-index/bridge results into a self-contained article, while moving the unresolved pointwise raw program to a sequel or technical companion.

This is not a recommendation to delete valid mathematics. It is a recommendation to align the principal claim and proof path with what is actually complete.

## 27. Required changes before another top-four review

1. **Resolve the concrete section residues.**  
   Prove that all nontrivial endpoint residues vanish for the actual section, or state the principal exact-index theorem with its arithmetic factor/transition kernel rather than an unmodulated target.

2. **Complete pointwise roof inversion.**  
   Establish the common pointwise correction, the critical/singular edge sum, and the full roof-frequency complement in the norm required by the raw density theorem.

3. **Do not use the diagonal shrinking interval as a density substitute.**  
   A prescribed shrinking-scale theorem requires new quantitative uniformity; a pointwise density requires still more.

4. **Preserve every quantifier distinction.**  
   Fixed-radius arithmetic asymptotics, radius-uniform transition formulas, lower-mass conditional bridges, and packet averages are different statements.

5. **Keep band dependence explicit.**  
   Every future use of the full occupation-torus estimates must retain the dependence of constants, block lengths, contours, and coordinate radii on the fixed roof band.

6. **Audit the polynomial-cut geometry independently.**  
   Verify intermediate regularity, section-side transversality, matched connector removal, and the refined Jacobian/length sums.

7. **Audit the peripheral and transition arguments independently.**  
   Check semisimplicity from physical pairings, the physical projection formula, resonant curvature, scalar continuity, moving maxima, and the uniform stationary-phase expansion.

8. **Audit the bridge moment proof.**  
   Check all derivative allocations in the three-block product and the passage from grid fourth moments to continuous-path tightness.

9. **Strengthen the novelty comparison.**  
   Explain theorem by theorem what is not already organized by existing Lorentz-process LLTs, billiard mixing LLTs, suspension local central limit theory, and standard spectral perturbation.

10. **Reduce the main submission burden.**  
    Move historical ledgers, validation details, and unresolved companion pipelines out of the principal mathematical route where possible.

## 28. Technical and presentation comments

1. The final correction removing `m` from the supremum subscript in the transition theorem is necessary and should be retained everywhere that theorem is summarized.
2. The term “exact-index local law” should specify whether it means a fixed interval, a pointwise roof density, an arithmetic factor, or the transition kernel.
3. The arithmetic coefficient should be displayed in the abstract or principal theorem whenever the fixed-radius exact-index result is advertised.
4. The transition kernel should not be called an ordinary Gaussian density when subunit branches with complex curvature contribute.
5. The roof coordinate of an actual resonance is zero; the roof coordinate of a damped moving peak need not be zero. The distinction should remain explicit.
6. The common packet length `L` may be very large. Its existence is enough for the theorem, but no practical numerical interpretation should be suggested without an effective order bound.
7. The finite-packet lower bound identifies at least one qualifying index, not a specified index. The bridge corollary states this correctly.
8. The radius-uniform bridge theorem requires `m^2P(E)>=epsilon`. This hypothesis should appear in every front-matter summary.
9. At fixed radius, “all positive arithmetic classes” means classes with positive endpoint residue; zero classes are exactly impossible.
10. The slowly shrinking interval result is qualitative and existential. It should not be cited as a rate statement.
11. Qualification workflows and finite diagnostics should remain separated from proof certification, as they are in the present metadata.
12. A future revision should again identify the exact author SHA, paper tree, controlling report, and completed qualification runs.

## 29. Final assessment

Revision 41 is a major advance over the manuscript reviewed in the v39 report.

It replaces coefficient-level Abel information by full fixed-band long-power control, computes the physical endpoint residues, proves an arithmetic exact-index interval theorem at fixed radius, evaluates parameter transitions by a finite Gaussian kernel, and establishes a Gaussian bridge under the unchanged exact return event. The fixed finite packet theorem is also a genuine strengthening of the earlier diverging-window result.

On the portions audited here, I found no decisive mathematical error. The new results appear credible subject to independent expert verification of the anisotropic-space, holonomy, and moment arguments.

The paper nevertheless does not prove its original pointwise raw-return theorem. The exact-index interval law may carry a nontrivial arithmetic factor, and the concrete vanishing of that factor is not established uniformly. More importantly, the pointwise roof correction and full high-frequency complement remain open.

The gap is now sharply identified and substantially smaller, but it still separates the strongest proved theorem from the raw mixed-density endpoint advertised by the article.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
