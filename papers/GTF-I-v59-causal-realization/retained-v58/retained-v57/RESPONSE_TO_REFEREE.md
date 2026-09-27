# Response to Revision 55 / r37 — Revision 57 continuation

**Controlling report:** review `0b2226b43a10f10c4ed0c5f969c058cde8d59230`, blob `d9841d9b928800977e5965d5d6df52347fa64547`.  
**Predecessor:** already published Revision 56, `5c3b3fb9ab878748f58462e065850d0a5cbbc2f6`, qualified source `d8b09977c368a490440c2213fa98bb4f01455710`.  
**Article:** *Stochastic Realization, Finite Quotients, and Uniform Orbit Geometry*.

## Why this is a separate continuation

At the remote survey, v55/r37 remained the latest review, but v56 had already been published on its own branch. This revision starts from that exact v56 publication and does not overwrite it. The v56 same-width stationarization, physical-equivariant purification, positive critical boundary, phase minima and existential-real completeness are inherited results. They are re-examined and retained, not claimed as new v57 discoveries. The response below preserves all seven major and thirty-two local responses with that provenance.

## New response to quantitative breadth and legal outputs

The most substantial continuation of R37 7.7 is no longer one nonabelian sphere. Section `sec:uniform57` gives a general orbit theorem with two distinct exponents: a uniform small-ball exponent over *all* unit feature directions, and the target orbit's covering dimension. The conditional-centroid contraction needs the former. The inner-hull construction needs the latter. These hypotheses are not conflated.

Section `sec:matrix57` verifies both exponents in every dimension for traceless Hermitian conjugation. A dimension-dependent adjacent spectral gap survives all eigenvalue multiplicities. It maps a small conjugacy cap into a Grassmannian cap and yields the uniform exponent `2(d-1)`. This corrects the tempting but invalid shortcut that conditional centroids remain pure. The target pure-state orbit has dimension `2(d-1)`, giving width between `c(N/log(N+2))^(d-1)` and `C(N+1)^(d-1)` for the full legal density-matrix interface. The exact upper construction uses an inner positive polytope, common command rows, and legal density-matrix decoders. The logarithmic gap remains explicitly present.

Section `sec:extreme57` answers the full-matrix pure-amplitude zero-error endpoint. Every exact profile is bounded below by the number of reachable extreme orbit points at each cut; deterministic orbit storage attains all those bounds simultaneously. This proof includes the terminal cut and needs no identity letter. For one fixed algebraic dense free pair in `SU(d)`, its inverses and the identity, a specified transcendental seed has exact width `2*3^N-1`. For that very same alphabet and seed every fixed positive subcritical error instead has the above polynomial bounds. The algebraic dense-free and spectral-gap theorems are explicitly imported. The seed is not advertised as algebraic, and no algorithm for finding the free pair is claimed. This is not a purported resolution of the scalar planar exact endpoint.

A fixed finite tomography law carries the matrix result exactly when its legal image and reconstructed norm are retained. Enlarging the decoder set to the entire probability simplex is a different problem: all target tomography vectors are interior simplex points. The revised text exhibits this distinction, rather than claiming an extreme-output bound for arbitrary categorical decoders.

Section `sec:matrixprecision57` strengthens R37 7.6. Rounding a Gram factor and normalizing gives rational positive semidefinite decoders with exact trace one and an explicit error bound. General clocked row error accumulates with `N+1`, while stationary permutation rows need no rounding. Fair-bit and storage costs are stated for supplied algebraically encoded machines; exact unencoded real tables are not represented as finite programs.

## Rechecked inherited structural response

The inherited proof was checked at its delicate interfaces: finite-word compactness uses the requested closed error ball, Ramsey colors include actual neutral and command composite rows, the last neutral table is absorbed into the decoder, and physical-identity-kernel averaging retains a legal convex decoder and randomized initialization. The phase gauge keeps multiplication order explicit. The finite-group existential-real theorem is not promoted to a total complexity bound for general rational matrix closures. All v56 active labels remain loaded in the new article, and all 145 native predecessor files are preserved byte-for-byte.

The following seven major responses and thirty-two local responses describe the retained v56 resolutions, augmented by the preceding new results. The original v56 response is also preserved unchanged under `retained-v56/`.

## Major revision requests

### R37 7.1 — Priority comparison for purification

The comparison now separates the classical minimum-rank idempotent, compact group corner, recurrent-class simplex and permutation action from the joint physical-coordinate and closed-error constraints. Flor's Theorems 2 and 3 were checked against the finite nonnegative idempotent and bounded corner group used here. Theorem `thm:equivariant56` additionally averages the physical-identity kernel and passes to its label orbits, obtaining a continuous action of the physical group itself without width or error loss. Theorem `thm:stationarization56` is a separate Ramsey argument, not an assertion that classical purification by itself removes a clock. Fijalkow--Paperman's Theorem 10 on neutral-letter advice languages is explicitly compared, as a relevant deterministic antecedent. The comparison is author-side and targeted; it is not independent or exhaustive priority clearance.

### R37 7.2 — Stationary and clocked theorem map

Table `tab:map56`, on its own page following the introduction, lists the stationary minimum, quotient radii, clocked width, critical component radius, length-phase minima, the retained exact-rank proof, quantitative hypotheses and finite encoding model. Theorem `thm:stationarization56` establishes the exact relation: under eventual approximate returns, the clocked width converges to the stationary minimum, with eventual equality when finite. Without that synchronization hypothesis the two quantities are not identified.

### R37 7.3 — The positive profinite clocked boundary

The question is answered by Theorems `thm:stationarization56` and `thm:completeboundary56`, rather than merely restated. At every error, bounded clocked width is equivalent to a finite stationary realization and to an open normal subgroup whose constrained quotient radius is at most that error. This includes the positive critical value R_0. At equality, boundedness holds exactly when the infimum of finite-quotient radii is attained. Failure at equality implies a uniform occupation bound for each fixed width even with arbitrary other registers. The proof first extracts a stationary finite-word competitor from a homogeneous set of actual composite kernels; compactness of the stationary parameter space supplies a strict finite witness. It never takes a limit of machines with errors larger than the requested tolerance.

### R37 7.4 — Output and hidden-state scope

The structural theorems now allow norm-compact convex subsets of Banach spaces as outputs. Their proofs use finite convex combinations and compact parameter spaces, not finite output dimension. The localization and algebraic sections retain their declared finite-dimensional hypotheses. The final subsection of `sections/13-equivariant-boundary.tex` explains why arbitrary countable hidden labels, general compact convex hidden state spaces, and operator kernels are different: total-variation compactness, finite rank, and a finite recurrent vertex set need not survive. No online, adaptive-query, or path-law theorem is inferred from a terminal interface.

### R37 7.5 — A complexity theorem beyond termination

Theorem `thm:ETR56` proves that stationary width decision for explicitly tabulated finite groups and rational categorical interfaces is existential-real complete. Membership uses the physical-equivariant reduction and a polynomial-size formula of degree at most three. Hardness already holds for the trivial group, one query, and zero error, via normalized nonnegative rank and Shitov's Theorem 2. This yields hardness, not a matching upper bound, for the broader rational orthogonal polynomial-input problem. `finite_group_formula.py` implements the finite-group formula construction and validation; it is not a general group-closure or quantifier-elimination engine.

### R37 7.6 — Finite descriptions, precision and random bits

Lemma `lem:dyadic56` and Theorem `thm:bits56` give explicit dyadic row-rounding, table-size and fair-bit budgets. A general clocked implementation accumulates a stated error proportional to N+1. A purified stationary group realization rounds only initialization and the terminal decoder, so its additional error and at most 2b fair bits are independent of the horizon. Temporary sampler registers and indexing are charged separately. Effective rounding is asserted for exact algebraic encodings; the included executable utility implements the rational subcase. An arbitrary unencoded real table is not advertised as an executable finite-description program.

### R37 7.7 — A nonabelian quantitative application

Theorem `thm:spherical56` treats the full spherical vector orbit under a spectral-gap alphabet. Its lower bound is c(N/log(N+2))^((d-1)/2), its exact upper bound is C(N+1)^((d-1)/2), and it bounds occupation at fixed k by C k^(2/(d-1)) log(k+2). Corollary `cor:SO356` uses two explicit rational noncommuting rotations and their inverses to obtain N/log N versus N on SO(3). Density is proved; the spectral gap is imported from Bourgain--Gamburd's algebraic dense-generator theorem. The logarithmic gap is explicit. This is a nonabelian spherical representation, not an abelian observable factor, and is not called a universally matched compact-Lie-group law.

## All thirty-two local comments

### R37 local 01 — Minimum rank

Lemma `lem:idempotent55` explicitly chooses the least occurring integer matrix rank in the nonempty joint semigroup before powering. It does not require continuity of rank.

### R37 local 02 — Powering space

The same proof names the compact monothetic subgroup in H times the finite product of peripheral unit circles, containing the physical element and peripheral eigenvalues.

### R37 local 03 — Peripheral Jordan blocks

The proof states that a nontrivial Jordan block at a unit-modulus eigenvalue gives polynomial growth, contradicting stochastic power boundedness.

### R37 local 04 — Corner injectivity

For B=EBE the proof displays (xE)B=xB. Thus the restriction to row(E) determines B and is injective.

### R37 local 05 — Stationary idempotent rows

Lemma `lem:simplex55` retains the direct Markov-chain proof: every row of E is stationary; stationary mass is supported on closed classes and decomposes into their unique stationary rows.

### R37 local 06 — Intertwining

The purification proof now displays V B_a=Pi_a V for the recurrent-vertex matrix V. The physical-kernel reduction also displays V pi=bar(pi) V for orbit-uniform rows.

### R37 local 07 — Width and padding

The recurrent-simplex and orbit reductions explicitly have r<=k. Fixed-point dummy labels are only used to express a proposed common bound, not counted as eliminated private memory.

### R37 local 08 — Closure topology

The fixed-permutation minimum uses the product of the original compact topology on H and the discrete topology on finite S_k; this is stated explicitly.

### R37 local 09 — Inverse fibers

The finite-quotient proof writes (hU)^(-1)=U h^(-1)=h^(-1)U by normality.

### R37 local 10 — Actual finite quotient

After Corollary `cor:intrinsicminimum56`, the joint-group quotient is identified as H/U isomorphic to P/N, with P the hidden projection and N its physical-identity kernel. The coarser factorial bound and possible additional kernel of the orbit action are distinguished.

### R37 local 11 — Cycle direction

Proposition `prop:C655` specifies the forward generator i -> i+1 on the two- and three-cycles.

### R37 local 12 — Positive return lengths

The return-language definition explicitly excludes the empty word and uses positive lengths. Zero is used only as an empty padding convention elsewhere.

### R37 local 13 — Reversed concatenation

Lemma `lem:phasegroup55` gives the executable chronological concatenation a^(p-1), w, a, whose physical product is a x a^(p-1) under the article convention.

### R37 local 14 — Repeated phases

Both the earlier phase section and the new exact-minimum section state that quantities repeat when the order q of H/J properly divides the chosen block length p.

### R37 local 15 — Lost cuts

The earlier proof lists its fixed-prefix/suffix loss. The new phase minimum proof bounds the extra loss for residue ell by ell+b+1<=2p and the total by 2p^2 plus the block occupation constants, including short horizons.

### R37 local 16 — Period notation

The return period is changed to p throughout the phase section and new phase theorem. The inherited symbol d denotes a contraction defect in its own section; no formula identifies them.

### R37 local 17 — Open subgroups

The infinite-component radius argument explicitly says that every open subgroup contains H^0 because a connected image in a finite discrete space is a singleton.

### R37 local 18 — Equivalent norms

Lemma `lem:Lieapprox55` chooses constants a_j,b_j with a_j||v||<=|v|_2<=b_j||v|| and an initial approximation finer than a_j eta/b_j before the Euclidean projection.

### R37 local 19 — Translate orientation

The exact-boundary proof defines L_g f(x)=f(g^(-1)x) and identifies f(y_l x_i) as evaluation of L_(y_l^(-1))f at x_i.

### R37 local 20 — Finite evaluation ranks

New standalone Lemma `lem:evaluation56` proves that all finite evaluation matrices have rank at most k exactly when the translate span has dimension at most k.

### R37 local 21 — Profinite matrix image

The exact-boundary proof invokes the closed-subgroup theorem/no-small-subgroups consequence, with a Lie-group reference: a compact totally disconnected matrix group is a zero-dimensional compact Lie group, hence finite.

### R37 local 22 — Digit tail

The dyadic example displays the exact geometric tail sum of 2/3^(n+1) for n>=m, equal to 3^(-m).

### R37 local 23 — Fourier sign

The dyadic circulant proof declares the positive exponential Fourier convention before its eigenvalue calculation.

### R37 local 24 — Hankel to circulant

The proof explicitly sends i to -i-1 modulo 2^m, converting b(i+j) into the function of j-i used in the circulant formula.

### R37 local 25 — Terminal cut

The dyadic occupation proof retains the separate terminal-cut charge, since the paired-suffix rank argument applies only before the terminal register.

### R37 local 26 — Binary total variation

Corollary `cor:unitnoise55` retains the explicit fact that binary total variation is one half of mean error in its amplitude-budget argument.

### R37 local 27 — Defining equations

The effectivity section states that the algorithms must compute equations defining the actual joint compact closure, not an arbitrary set of equations merely vanishing on the generated subgroup.

### R37 local 28 — Crude tuple count

The fixed-width permutation enumeration is explicitly before quotienting by simultaneous conjugacy; the factorial count is deliberately crude.

### R37 local 29 — Flor hypotheses

The revised comparison and literature audit identify Flor Theorems 2 and 3 and their relevant hypotheses, and credit the prior stochastic/semigroup work cited there. The proofs here remain self-contained.

### R37 local 30 — Classical kernel table row

The comparison table now includes compact stochastic-semigroup kernels and bounded nonnegative groups, and distinguishes the external physical-coordinate uniform-error quantifier. A separate row treats neutral-letter advice automata.

### R37 local 31 — Abstract organization

The abstract separates the clocked stationarization hypothesis, the stationary physical-group reduction, and the extra arithmetic/spectral-gap assumptions of the quantitative consequences.

### R37 local 32 — Random initialization

The abstract and first stationary definition explicitly retain randomized initialization. Neither purification theorem is described as a deterministic-initialization theorem.

## Preservation, proofs and reproducibility

All 145 native v56 files are preserved byte-for-byte under `retained-v56/`, including the earlier article, nested derivation sources, regression programs, and frozen reports. Every v56 mathematical label remains loaded in the revised main article. The previous exact-rank and localization proofs remain as independent arguments even where a new structural theorem subsumes their existence conclusion.

The source-bound builder reruns new and inherited regression suites, compiles the new article and six retained documents, and independently rebuilds the native archive without repository or network access. `evidence/THEOREM_LOCATIONS.json` maps source labels to the actual compiled theorem numbers and pages. The build receipt records the actual source commit and results, not an anticipated successful run.

Finite exact checks test examples, multiplication conventions, extraction formulas, encodings and negative controls. They are not proofs of the universal Ramsey extraction, compact-group reduction or spectral-gap input. The article gives written proofs, subject to independent mathematical review. The external literature comparison is not independent priority clearance or a guarantee of editorial acceptance.

The independent A/B/C/D analytic pipeline receives no new closure credit. Those obligations are recorded in the frozen repository ledger and do not follow from the stochastic-realization results.
