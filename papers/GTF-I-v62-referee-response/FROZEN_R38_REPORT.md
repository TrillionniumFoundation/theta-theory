# Referee Report — General Theta Foundations I, Revision 57

**Manuscript:** *Stochastic Realization, Finite Quotients, and Uniform Orbit Geometry*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v57-uniform-orbit-2026-09-27`
- `revision/general-theta-foundations-i-v57-referee-ready-2026-09-27`

**Reviewed publication head:** `0e07470b9693a2789af00222f063e715a83ff454`  
**Validated native-source commit:** `de638216469bdcb300bd6b94bf3f0d56c2433e30`  
**Workflow trigger:** `1b2b674dffd316ecb14e2b83f5b1f66a56379739`  
**Qualification workflow:** `36321061729`  
**Source predecessor:** Revision 56 publication `5c3b3fb9ab878748f58462e065850d0a5cbbc2f6`  
**Controlling located prior report:** r37, `0b2226b43a10f10c4ed0c5f969c058cde8d59230`, reviewing Revision 55  
**Review branch:** `review/general-theta-foundations-i-v57-uniform-orbit-harsh-top4-r38-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** Revision 57 is a serious paper and a substantial advance over the versions reviewed in r35–r37. It contains several class-wide structural theorems, not merely candidate certificates, finite examples, or compactness observations. I did not find a fatal counterexample to the width-preserving stationarization theorem inherited from Revision 56, the stationary stochastic purification and physical-equivariant quotient, the equality-inclusive finite-quotient boundary, the new uniform-orbit lower and upper bounds, the density-matrix application, the extreme-orbit exact profile, the free-group endpoint example, or the positivity-preserving finite-precision compiler.

The strongest structural conclusion is that, under eventual approximate returns, the limiting clocked width equals the unrestricted stationary minimum at the **same error and the same number of labels**, with an all-profile occupation bound below that minimum. For compact groups, every stationary stochastic realization can moreover be replaced, without width or error loss, by a finite continuous physical-group action with randomized initialization. These are attractive and nontrivial realization results.

The strongest quantitative conclusion is the separation of two geometric exponents: an all-centroid small-ball exponent controlling the converse, and a target-orbit covering dimension controlling a positive common-row construction. For full legal density-matrix outputs under a spectral-gap alphabet in `SU(d)`, this gives width exponent `d-1` on both sides, up to a logarithmic loss in the lower bound. The pure-amplitude endpoint can simultaneously have exact width `2*3^N-1` for one fixed free alphabet and seed, while every fixed positive subcritical error has polynomial width.

The top-four rejection is therefore **not** a correctness dismissal. It rests on the following independent points.

1. **The central model remains specialized and exceptionally permissive.** The clock, horizon, horizon-dependent real transition tables, their construction and lookup, exact real arithmetic, and exact atomic sampling are uncharged. The structural clock-removal theorem also requires eventual approximate returns at every sufficiently large length.
2. **The stationarization and purification mechanisms stand close to classical compact stochastic-semigroup, nonnegative-matrix-group, advice-automata, and recurrent-simplex structure.** The manuscript adds important closed numerical-error and physical-coordinate constraints, but the independent theorem-level priority boundary is not yet settled.
3. **The nonabelian quantitative laws are not sharp.** The lower bounds retain a logarithmic loss, no matching constants are known, and the spectral-gap constants are imported and non-effective.
4. **The exact exponential endpoint is deliberately non-effective.** It uses a nonconstructively selected algebraic dense free pair and a specified transcendental seed. It is not a rational or algebraic finite-input separation result.
5. **The broadest quantitative theorem assumes a strong uniform small-ball estimate over every possible conditional-centroid direction.** This is verified for spheres and conjugation on traceless Hermitian matrices, but not developed into a general computable theory for compact homogeneous interfaces.
6. **The output theorem is terminal and convex-valued.** It does not classify online observations, adaptive queries, joint output processes, arbitrary operator-valued hidden states, or general irreversible compact semigroups.
7. **The manuscript is again accretive.** The fifty-five-page article combines clock removal, stochastic purification, finite quotients, phase minima, radius classification, planar/profinite laws, nonabelian orbit geometry, an exact free endpoint, existential-real complexity, and finite precision. These form at least two substantial papers.
8. **The wider repository pipeline remains mathematically independent and open.** None of the finite-dimensional realization results supplies the raw local-limit, stopped-LDP, global-kernel, nonlinear-semigroup, filtering, strict/form response, or labelled posterior-contraction gates in the frozen A/B/C/D dependency graph.

**Disposition outside the four leading general journals:** after a conventional priority audit and substantial refocusing, I regard the work as a potentially strong specialist contribution in probabilistic or weighted automata, positive realization, compact semigroup dynamics, control, convex geometry, or theoretical computer science. The paper has passed the stage at which another wholesale mathematical reconstruction is needed. It has not passed the significance and positioning threshold for the four leading general mathematics journals.

---

## 1. Scope, genealogy, and material reviewed

At the final branch survey used for this report, Revision 57 was the latest referee-ready `General Theta Foundations I` revision. The work and referee-ready branches both pointed to

```text
0e07470b9693a2789af00222f063e715a83ff454.
```

No Revision 58 branch and no pre-existing Revision 57 review branch were present at that survey.

Revision 57 starts from the already published Revision 56 head

```text
5c3b3fb9ab878748f58462e065850d0a5cbbc2f6,
```

rather than from the Revision 55 head reviewed in r37. The Revision 56 structural results are therefore inherited mathematics, not new Revision 57 discoveries. Since no separate Revision 56 referee branch was located, I independently audited the inherited stationarization, physical-equivariant purification, complete boundary, phase-minimum, nonabelian spherical, complexity, and finite-precision arguments needed to assess the present article.

I reviewed the complete active source graph, with particular attention to:

- `papers/GTF-I-v57-uniform-orbit/main.tex`;
- `sections/00-introduction.tex`;
- `sections/12-stationarization.tex`;
- `sections/09-purification.tex`;
- `sections/13-equivariant-boundary.tex`;
- `sections/01-classification.tex`;
- `sections/02-localization.tex`;
- `sections/10-return-phases.tex`;
- `sections/11-profinite-boundary.tex`;
- `sections/03-consequences.tex`;
- `sections/04-width-laws.tex`;
- `sections/14-nonabelian.tex`;
- `sections/16-uniform-orbits.tex`;
- `sections/17-matrix-orbits.tex`;
- `sections/18-extreme-endpoint.tex`;
- `sections/05-algebraic-circle.tex`;
- `sections/06-effective.tex`;
- `sections/15-complexity-resources.tex`;
- `sections/19-positive-precision.tex`;
- `sections/07-comparison.tex`;
- `sections/08-bibliography.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PROOF_STATUS.json`;
- `HISTORY_AND_PIPELINE_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `FROZEN_R37_REPORT.md`;
- `FROZEN_PIPELINE_LEDGER.md`;
- `FROZEN_PIPELINE_HISTORY.md`;
- the complete retained Revision 56 native source inventory;
- the new and inherited exact-check programs;
- `evidence/BUILD_RECEIPT.json`;
- the source-hash, theorem-location, isolated-rebuild, and referee-package records;
- the branch-specific workflow and completed Actions job;
- the complete r37 report;
- the Revision 56 publication and source records; and
- the frozen repository-wide Round-Seventeen dependency ledger.

I also made targeted comparisons with classical nonnegative matrix groups and stochastic semigroups, neutral-letter/advice automata, positive and weighted realization, group and reversible automata, quantum finite automata, homogeneous-space metric entropy, dense free subgroups, and spectral-gap results. This was not an exhaustive independent priority search.

The source genealogy is clean. Revision 57 is four commits ahead of the exact Revision 56 publication. Its readable theorem source was committed at `de638216...`, qualification was executed against that source, and the publication head added derived PDFs and evidence without changing the native theorem source. The new review branch has the publication head as its unique base. No previous revision, review, main-branch file, or unrelated manuscript path is modified by this report.

---

## 2. Executive assessment of the mathematical contribution

### 2.1 Same-width, same-error stationarization

Let `M_epsilon` be the least width of a stationary stochastic realization, and let `W_{N,epsilon}` be the least peak command-register width of a horizon-specific clocked realization. Under eventual approximate returns, Revision 56 proves

```text
W_{N,epsilon} -> M_epsilon.
```

If the stationary minimum is finite, equality holds for all sufficiently large horizons. More strongly, when `k<M_epsilon`, every admissible clocked realization has only a uniformly bounded number of positive cuts of width at most `k`, even if all other registers are arbitrarily wide.

This theorem removes the clock without losing a state or increasing the error. The clocked rows themselves need not converge or become stationary.

### 2.2 Width-preserving stationary purification

An arbitrary stationary stochastic realization on `k` labels is placed inside the compact joint closure of physical and stochastic word products. A minimum-rank stochastic idempotent over the physical identity defines a recurrent simplex. The compact corner group permutes that simplex's vertices. The original initialization is projected onto the recurrent simplex, while old decoder values are averaged on its vertices.

The resulting realization has permutation command rows, randomized initialization, at most `k` labels, and the same uniform error. A further average over the hidden kernel above the physical identity descends this action to a continuous homomorphism from the physical compact group into a finite symmetric group, again with no width or error loss.

### 2.3 Exact finite-quotient and critical-boundary criteria

For a compact group and compact convex legal outputs, a stationary finite realization exists at error `epsilon` exactly when the interface can be approximated on cosets of some open normal subgroup within constrained radius `epsilon`.

Combined with stationarization, this gives an equality-inclusive clocked criterion under eventual approximate returns. At the component radius, bounded clocked realization exists exactly when the infimum over finite quotients is attained. The length-phase theorem identifies the exact limiting minimum in every return residue without adding a phase register.

### 2.4 A general quantitative orbit theorem

Revision 57 separates two geometric quantities:

- a uniform small-ball exponent `p` over **all unit feature directions**, needed because conditional centroids need not remain on the target orbit; and
- the covering dimension `q` of the target orbit, used to construct a finite inner polytope.

With an `L^2` group spectral gap and identity padding, it proves

```text
W_{N,epsilon} >= c (N/log(N+2))^(p/2)
```

throughout the fixed subcritical range, together with a narrow-cut occupation bound. At strict amplitude it constructs an exact horizon-specific realization using

```text
W_{N,0} <= C N^(q/2).
```

When `p=q`, the polynomial exponents match, up to the logarithmic loss.

### 2.5 Full legal density-matrix outputs

For conjugation on traceless Hermitian matrices, the paper proves a small-ball exponent `2(d-1)` uniform over all unit matrices, including matrices with repeated eigenvalues. The proof extracts a uniformly separated adjacent spectral cut and reduces to a Grassmannian cap estimate.

The pure-state target orbit has the same real dimension `2(d-1)`. Consequently, for legal density-matrix output and Frobenius error, the width exponent is `d-1` on both sides, again up to a logarithm. The upper construction remains inside the density-matrix cone and can be exact at every strict amplitude.

### 2.6 The exact extreme endpoint

For an orbit consisting of extreme points of the legal compact convex output set, exact correctness forces different reachable orbit points to use disjoint hidden supports at every cut. Therefore the exact minimum profile equals the reachable orbit cardinalities, and deterministic orbit storage attains it.

Applying this to rank-one density matrices and a fixed dense free subgroup of `SU(d)` gives one fixed alphabet and seed with

```text
W_{N,0}=2*3^N-1,
```

while every fixed positive subcritical error has polynomial width. The exact/noisy transition is therefore genuinely discontinuous in growth order for that legal full-matrix interface.

### 2.7 Finite encodings and positive precision

For explicitly tabulated finite groups and rational categorical targets, stationary width decision is shown existential-real complete. Separately, supplied algebraically encoded matrix realizations admit rational finite-table implementations. Gram-factor rounding preserves positive semidefiniteness and trace exactly, and the accumulated row, decoder, storage, and fair-bit costs are displayed.

These results correctly distinguish nonuniform real-label width from finite-description computation.

---

## 3. Detailed correctness audit

### 3.1 The width convention

The article defines `W_{N,epsilon}` using only the command registers `S_0,...,S_N`. A numerical decoder vector is not an additional sampled-answer register. This convention is used consistently in the new extreme-orbit theorem.

In particular, if the reachable orbit has one point, the exact command width may be one. The formula

```text
W_{N,0}=|O_N|
```

therefore has no hidden `max(2,...)` correction. Charging a sampled categorical answer would change only the separate implementation resource, not the mathematical command-width theorem.

### 3.2 Finite stationary witnesses

For fixed width `k`, the stationary parameter space is compact: stochastic matrices and initialization rows lie in finite-dimensional simplexes, while legal decoders lie in compact output sets. If no stationary error-`epsilon` realization exists, the nested closed finite-word constraint sets have empty total intersection. The finite intersection property therefore gives a word-length cutoff `m` and a strict gap

```text
e_{k,m}=epsilon+gamma.
```

This step is correct and importantly uses a closed error ball. It does not assume continuity of the supremum over all words.

### 3.3 Ramsey extraction of stationary rows

The stationarization proof selects many narrow cuts, identifies each register with a subset of a common `k`-label set, and colors each ordered cut pair by cells containing the actual composite return kernel and the actual composite command-plus-return kernels.

A homogeneous clique gives one approximate neutral table and one approximate table per command. For a test word of length at most `m`, consecutive command edges are followed by one final neutral edge. Prefix and suffix return words turn this into one genuine word of the original horizon. The physical target differs from the intended short-word target only through finitely many insertions near the physical identity.

The telescoping estimate uses only contraction of row total variation under stochastic multiplication. The neutral representative is absorbed into the decoder and is never asserted idempotent. No microscopic clocked row is assumed to converge, and no physical return is assumed to act trivially on hidden labels.

I regard this argument as correct. It is also one of the places where the novelty boundary against advice-automata and neutral-letter collapse must be examined most carefully.

### 3.4 Occupation and limiting equality

If a stationary `k`-label machine exists, it supplies a clocked `k`-label machine at every horizon. Conversely, unboundedly many `k`-width cuts would yield the extracted stationary machine. Hence every `k<M_epsilon` has a uniform occupation bound.

When `M_epsilon=K<infinity`, the stationary upper bound and the occupation obstruction for `K-1` imply eventual equality `W_{N,epsilon}=K`. If `M_epsilon=infinity`, applying the occupation theorem to every fixed `k` gives divergence. The handling of the one-label case is explicit.

### 3.5 Minimum-rank stochastic idempotents

Choose a minimum matrix rank in the compact joint semigroup and an element attaining it. Stochastic power boundedness makes all peripheral Jordan blocks semisimple. A simultaneous return subnet in the physical compact group and the peripheral eigenvalue torus makes the matrix powers converge to the real stochastic spectral projection `E`.

Minimum-rank choice forces `rank(E)` to equal the selected rank. Every element of the corner `eTe` has the same rank, and its restriction to the row space of `E` is invertible. The corner embeds as a compact submonoid of a topological group and is therefore a group.

This is a sound application of classical compact-semigroup structure.

### 3.6 The recurrent simplex

For a finite stochastic idempotent, every row is stationary. The stationary probability rows are exactly the convex hull of the unique stationary rows on the closed recurrent classes. These rows have disjoint supports and are linearly independent, so their number equals the matrix rank.

A stochastic corner-group element and its stochastic inverse give inverse affine maps of this simplex. They therefore permute its vertices. The manuscript uses this correctly and does not mistake the singular idempotent for the identity matrix.

### 3.7 Closed error constraints and purified outputs

The joint closure uses physical coordinate `u_w^{-1}` so that chronological word concatenation matches semigroup multiplication. Continuity extends every original wordwise error inequality to the full compact joint semigroup.

Projecting initialization through `E`, expressing it in recurrent-simplex coordinates, and evaluating the old decoder on recurrent vertices gives legal decoder values by convexity. The intertwining identity

```text
V B_a = Pi_a V
```

makes the row convention explicit. Products of the corner command elements have the correct physical coordinate, while `(1,E)` handles the empty word. Thus the new permutation machine remains in the same closed error balls.

The purification theorem is correct in its finite-label, stationary, terminal-output scope.

### 3.8 Descent to a physical-group action

Let `N` be the finite hidden permutation kernel above the physical identity. Averaging the error inequalities over `N` is legitimate because norm balls and legal output sets are convex. Uniform rows on `N`-orbits form a smaller recurrent label set.

Two joint-group elements over the same physical element differ by this kernel, so their induced actions on `N`-orbits agree. The resulting homomorphism from the compact physical group to a finite symmetric group is continuous. Randomized initialization is retained.

This proves physical equivariance without silently identifying physical and hidden relations in the original machine.

### 3.9 Finite quotient and critical equality

The kernel of a finite physical action is an open normal subgroup. Conversely, storing a seed and an open-normal coset, with a constrained Chebyshev center as decoder, gives a finite realization.

For an arbitrary compact group, open normal subgroups in the profinite component quotient approximate the identity component. Uniform continuity of the finite interface gives

```text
R_0 = inf_U r(U).
```

Stationarization then makes critical clocked boundedness equivalent to attainment of this infimum. The proof does not pass to equality from a sequence of machines with larger tolerances.

### 3.10 The uniform all-direction small-ball step

The new quantitative lower bound correctly requires the small-ball estimate for every unit `u,v` in the representation space. Conditional centroids of orbit points, after normalization, need not themselves lie on the target orbit; an orbit-only cap estimate would be insufficient.

A union bound makes the Haar mean of the best of `k` centers fall below one by order `k^{-2/p}`. The spectral gap controls a smoothed evaluation at the identity. The functions have one common Lipschitz bound because the representation is finite-dimensional, and averaging over a small Riemannian ball turns the `L^2` estimate into a pointwise estimate. Choosing the block length logarithmic in `k` gives an executable contraction with the declared defect.

I regard the argument as correct. The dependence of all constants on the chosen bi-invariant metric, representation, small-ball constants, and spectral-gap constant should be gathered in one explicit sentence.

### 3.11 Conditional-centroid contraction

At a selected block endpoint, the actual composite stochastic row may depend on the block word and on the incoming state, but not on an unrecorded physical history once the current label and external word are fixed. Pairing each terminal conditional centroid with its own direction reduces the sum to the maximum over at most `k` directions. The uniform orbit gap then contracts the expected conditional-centroid norm.

Identity-letter fillers cannot increase this norm by conditional Jensen, even if their hidden rows perform arbitrary processing. Greedy block placement therefore yields the displayed occupation bound with unrestricted intervening widths.

### 3.12 Quadratic inner approximation

A compact smooth homogeneous orbit has intrinsic covering number `O(delta^{-q})`. At a support maximum, the first derivative of a linear functional vanishes along the orbit; a uniform second-derivative bound gives support loss `O(||b|| delta^2)`.

Because the orbit spans the representation and has Haar mean zero, the origin lies in the interior of its convex hull. The additive support loss can therefore be converted to a multiplicative inclusion

```text
(1-C delta^2) Q subset conv{z_i} subset Q.
```

This is the correct quadratic scale for the upper realization.

### 3.13 The common-row upper machine

For each command and each net point, the contracted image `r R(u_a)z_i` lies in the finite inner polytope. Its barycentric coordinates define a legal stochastic row. Inductively, row means evolve as

```text
r^t R(u_w) z_0.
```

The terminal decoder rescales each net vertex by `rho/r^N`. The choice of `delta` ensures that this coefficient is at most one, so the decoder remains in the legal orbit hull. This gives an exact horizon-specific realization at strict amplitude.

The construction is nonuniform in the horizon and may choose arbitrary barycentric coordinates. Both facts are permitted by the stated model.

### 3.14 Uniform conjugacy caps

For a unit traceless Hermitian matrix, some adjacent eigenvalue gap is bounded below by a dimension-dependent constant. The spectral projection across that gap is well defined even when there are multiplicities inside either block.

The exact spectral-overlap identity controls the distance between these projections by the distance between conjugates. A nonempty small ball around any target matrix is therefore mapped into a Grassmannian cap. Its measure has exponent `2m(d-m)`, at least `2(d-1)`.

Rank-one centered projections show that the exponent cannot be improved uniformly. This correctly handles conditional-centroid directions with degenerate spectra and avoids the false assumption that centroids stay pure.

### 3.15 Positive density-matrix upper realization

The maximal projective net of pure states has cardinality `O(delta^{-2(d-1)})`. Approximating a top eigenline proves the support inequality

```text
(1-d delta^2)(D_d-c_d)
       subset conv{P_i-c_d}.
```

The resulting command rows are stochastic. The decoder

```text
c_d + (a'/r^N)(P_i-c_d)
```

is a genuine density matrix whenever the coefficient is in `[0,1]`. The selected `delta` guarantees this. Thus the upper bound does not enlarge the legal output set to an ambient Euclidean ball.

The lower and upper exponents are both `d-1`; the remaining logarithmic factor is real and is not hidden in notation.

### 3.16 The tomography encoding

The finite POVM-style map is affine and injective. On its legal image, the reconstructed Frobenius norm makes it an affine isometry. The total-variation comparison follows from the `l1/l2` inequalities for the traceless basis coefficients.

It is essential that the legal categorical output set remain the image of the density-matrix set. Enlarging it to the full simplex is a different problem and destroys the extreme-output inference. The manuscript states this correctly.

### 3.17 The extreme-orbit formula

Fix a suffix after a cut. Conditional expected terminal decoder values lie in the legal convex set. Exact output is an extreme orbit point. Hence every label used by a prefix producing that point must decode, after the suffix, to that same point.

An invertible physical suffix separates distinct prefix orbit points, so their hidden supports are disjoint. This proves the pointwise lower bound at every cut, including the terminal cut. Deterministic storage of the current orbit point attains all bounds simultaneously.

The theorem is elementary but useful, and its quantifiers are correct.

### 3.18 The free-group endpoint

The algebraic-entry subgroup of `SU(d)` is dense. The cited dense-free-subgroup theorem therefore supplies algebraic free generators `U,V`. A free group contains no nonidentity scalar torsion.

The specified transcendental projective seed has trivial stabilizer under every nonscalar algebraic matrix. Consequently, the projective orbit map is injective on the free group. With identity padding, products of length `N` are exactly the reduced free-word ball of radius `N`, whose cardinality is

```text
1+4(1+3+...+3^(N-1)) = 2*3^N-1.
```

The extreme-orbit theorem gives the exact width. The same algebraic alphabet has a spectral gap by the cited external theorem, so every fixed positive subcritical error falls under the polynomial matrix-orbit bounds.

This is mathematically sound, but its seed is intentionally transcendental and the generating pair is existential rather than explicit. The example must not be advertised as a rational-input complexity separation.

### 3.19 Positive Gram rounding

Approximating a square root `D^{1/2}` and normalizing `QQ*` preserves positivity and trace exactly. The Frobenius perturbation estimate and denominator bit bounds are adequate.

Rounding stochastic rows accumulates total variation over initialization and the `N` transitions. A density-matrix decoder has Frobenius diameter `sqrt(2)`, so distribution error and decoder error combine as stated. For stationary permutation rows, no transition rounding or transition randomness is needed, making the added error and fair-bit count horizon independent.

The theorem compiles a supplied algebraically encoded realization. It neither finds a width minimizer nor turns arbitrary real advice into a finite program.

### 3.20 Existential-real completeness

For an explicitly tabulated finite group, a finite permutation action, stochastic initialization, legal categorical decoder, and total-variation slack have a polynomial-size existential-real description. The binary encoding of `k` does not cause an exponential formula because a trivial exact realization bounds every relevant `k` by the explicit input size.

Hardness through normalized nonnegative rank is valid: a stochastic factorization is exactly a zero-error realization for the trivial group. This is a meaningful complexity boundary, but it does not give membership for compact matrix-group input with an implicitly described closure.

---

## 4. Novelty and priority

The manuscript's author-side audits are substantially better than those in early revisions, but they do not yet establish the independent priority boundary required for a top-four recommendation.

### 4.1 Classical structural ingredients

The following are classical or very close to classical:

- minimum-rank idempotents in compact semigroups;
- bounded groups of nonnegative or stochastic matrices;
- recurrent-class decomposition of a stochastic idempotent;
- permutation action on the vertices of a finite recurrent simplex;
- finite quotient actions of compact groups;
- Haar averaging and compact-group representation theory;
- homogeneous-space covering estimates;
- projective and Grassmannian cap volumes;
- nonnegative-rank universality;
- dense free subgroups in semisimple Lie groups; and
- algebraic-generator spectral gaps.

The paper does not generally claim these as inventions. The question is whether the **combined same-width numerical-error theorems** have already appeared in equivalent language.

### 4.2 The closest comparisons still needed

A publishable version should contain a theorem-by-theorem table comparing at least:

1. compact stochastic semigroups and nonnegative matrix groups, including Flor and Schwarz;
2. positive realization and finite-dimensional invariant cones;
3. probabilistic and weighted automata with real-valued outputs;
4. advice automata and neutral-letter collapse, including the precise hypothesis and conclusion of the cited Fijalkow–Paperman result;
5. approximate and metric Myhill–Nerode theories;
6. rational series and Hankel minimization;
7. reversible and group automata;
8. measure-once quantum finite automata and additive probability approximation;
9. hidden Markov realization and controlled HMM interfaces;
10. compact semigroup recognition and almost-periodic functions;
11. metric entropy and width of compact homogeneous orbits; and
12. classical versus quantum state-complexity separations for full-state or tomographic outputs.

For each principal theorem, the paper should say exactly which quantifier is new: horizon-dependent advice, closed additive numerical error, same-width stationarization, arbitrary intervening widths, constrained legal outputs, or pointwise exact profile.

### 4.3 Imported deep inputs

The nonabelian examples depend on deep external theorems:

- algebraic dense-generator spectral gap; and
- dense free subgroup existence.

The manuscript identifies these inputs correctly. They should remain visually separated from the realization arguments in every abstract-level summary. A finite regression suite cannot certify either input.

### 4.4 Significance at the four-journal level

The paper has a coherent specialist-level mathematical core. What is still missing for the four leading general journals is one of the following:

- a truly general clock-removal theorem not tied to eventual returns;
- a sharp nonabelian width law without the logarithmic loss;
- a broad irreversible semigroup boundary theory;
- a finitely encoded explicit exponential-versus-polynomial separation;
- a general dual characterization of approximate stochastic realization width;
- or a consequence resolving a recognized open problem outside the manuscript's own revision program.

The present collection does not yet reach that level.

---

## 5. Scope and resource model

### 5.1 Eventual returns are substantial

Stationarization requires approximate physical returns at every sufficiently large length, not merely recurrence along a subsequence. This hypothesis is natural for alphabets containing identity and for several multi-letter compact-group systems. It fails for a single irrational rotation letter, where a horizon-specific decoder can exploit the unique word at each length.

The theorem therefore does not identify clocked and stationary minima for arbitrary finite alphabets or arbitrary compact semigroups.

### 5.2 Finite hidden labels are essential

Compactness of the finite simplex, minimum matrix rank, finitely many recurrent vertices, and Ramsey coloring of finite stochastic tables all use finite label sets. The proof does not extend automatically to countably many labels, general compact convex hidden state spaces, Markov kernels, or operator-valued memories.

### 5.3 Terminal output is essential

Queries are selected at the terminal time. A prescribed joint terminal law may be treated as one compact convex output, but the paper does not address online observation, adaptive querying, path-law approximation, or repeated sampled outputs. Those problems have additional consistency constraints.

### 5.4 Nonuniform real advice is free

The primary invariant does not charge:

- the horizon or epoch;
- the description of stochastic tables;
- construction or lookup of those tables;
- exact real arithmetic;
- exact sampling from arbitrary real rows; or
- time complexity.

This makes the lower bounds stronger within the declared model, but it separates the invariant from ordinary finite-memory computation. The finite-precision theorems are therefore necessary companions, not implementation details.

### 5.5 Legal output sets matter

The density-matrix and extreme-endpoint results depend on restricting decoder values to a compact convex legal set. Replacing that set by a larger simplex or ambient ball can lower the width and invalidate extremality. This is mathematically legitimate, but it narrows comparisons with automata models that expose only scalar acceptance probabilities.

---

## 6. Quantitative limitations

### 6.1 The logarithmic gap

Both the spherical and matrix-orbit results have the form

```text
c (N/log N)^alpha <= W_N <= C N^alpha.
```

The lower logarithm comes from converting an `L^2` spectral gap into a pointwise executable block with length `O(log k)`. It may be intrinsic to this method, but the paper does not show that it is intrinsic to the realization problem.

Removing the logarithm, or proving that it is necessary for some fixed alphabet, is the clearest next quantitative problem.

### 6.2 Constants are non-effective

The spectral-gap constant supplied by the imported theorem is not computed. The small-ball constants and inner-hull constants are dimension dependent. Thus the nonabelian asymptotic law is qualitative in its constants even for algebraic alphabets.

### 6.3 The exact endpoint is not a finite-input example

The free-group example uses:

- an existential algebraic free pair;
- a specified transcendental seed; and
- a full density-matrix terminal value.

This is a valid mathematical example, but it does not imply an explicit rational-input state-complexity separation. The distinction should appear in the abstract, not only in the proof-status records.

### 6.4 Growth below the general structural boundary

The finite-quotient classification identifies whether bounded width exists. It does not generally determine the rate at which width diverges below the boundary. The orbit theorems do so only under strong geometric and spectral assumptions.

---

## 7. Article architecture

Revision 53 successfully produced a focused fourteen-page article. Revision 57 returns to a fifty-five-page integrated article containing several largely independent themes.

I recommend division into at least two papers.

### Paper A: Clock removal and finite physical actions

This paper should contain:

- the clocked and stationary models;
- width-preserving Ramsey stationarization;
- stationary purification;
- physical-kernel descent;
- the finite-quotient criterion;
- the complete critical boundary;
- phase minima; and
- the explicit finite-group complexity boundary.

Its central statement would be conceptually clear: under synchronization, clocked nonuniform stochastic realization has the same finite-state minimum as a stationary finite physical-group action.

### Paper B: Uniform orbit geometry and stochastic width

This paper should contain:

- the all-direction small-ball theorem;
- the orbit-hull upper construction;
- spherical and density-matrix applications;
- the extreme-orbit profile;
- the free-group endpoint; and
- positivity-preserving finite precision.

Its central statement would be geometric: stochastic width is controlled by a converse exponent for all centroid directions and a covering exponent for the legal target orbit.

The earlier arithmetic, two-state, simplex, Gram, and SOS theories can remain in archival supplements or separate companion articles. They should not all be loaded into the main submission merely to preserve revision genealogy.

The current standalone title is a substantial improvement over the old series branding. The manuscript should retain that standalone presentation.

---

## 8. Relation to the repository-wide paper pipeline

The local mathematical dependency graph is coherent:

```text
common stochastic-row compatibility
  -> positive/reachable sections and endpoint contraction
  -> stationary stochastic purification
  -> physical-kernel quotient
  -> finite physical action;

finite stationary witness
  + eventual approximate returns
  + Ramsey homogeneous composite kernels
  -> same-width stationarization
  -> exact critical boundary and phase minima;

uniform all-direction orbit caps
  + group spectral gap
  -> executable contraction
  -> occupation and lower width;

smooth orbit geometry
  -> quadratic inner hull
  -> exact positive upper realization;

extreme legal outputs
  -> disjoint hidden supports
  -> exact orbit-cardinality profile.
```

These are genuine local advances.

They do **not** close the frozen Round-Seventeen analytic chains

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Those chains require model-specific results including:

- raw unsmoothed Fourier and density local limits;
- entropy-controlled stopped-path large deviations;
- one global past kernel and weak-Harris estimates;
- exact canonical coefficients and shell conditioning;
- process CLT and Mosco recovery;
- nonlinear Nisio resolvents and graph-core identities;
- regular filtering and exact-experiment QMD/LAN;
- strict/form response with changing filtrations; and
- labelled posterior contraction.

No such theorem follows from the present finite-state realization analysis. Accordingly, I assign **no credit** for:

```text
historical A2 replacement;
B4 aggregate closure;
C2 aggregate closure;
eleven-paper aggregate closure;
whole-Theta-program closure.
```

The manuscript's own `PROOF_STATUS.json` correctly keeps all these flags false. Repository accumulation and preservation do not alter the editorial assessment of this paper.

---

## 9. Reproducibility and publication audit

The publication record is substantially improved relative to early revisions.

The reviewed branch points to

```text
0e07470b9693a2789af00222f063e715a83ff454.
```

The readable theorem source is bound to

```text
de638216469bdcb300bd6b94bf3f0d56c2433e30.
```

Workflow `36321061729` completed successfully. Its job committed the readable source before qualification, installed fixed dependencies, ran source-bound qualification and an isolated native archive build, published the PDFs without changing the source, and preserved the actual outputs.

The build receipt records:

- a 55-page principal article;
- six retained rendered documents;
- 181 native source files;
- 145 byte-identical predecessor files;
- 12,575 new finite assertions;
- 17 named new negative controls and 34 executions;
- normal/optimized agreement;
- re-execution of all inherited regression suites;
- equality of all isolated native source hashes;
- all-page text equality;
- all-page raster equality; and
- no repository or network dependency for the isolated rebuild.

These are strong provenance and regression controls. They are not independent proof verification, spectral-gap certification, dense-free-generator certification, priority clearance, or journal acceptance. The manuscript states this distinction accurately.

The commits are unsigned. I do not treat the absence of a signing credential as a mathematical defect, provided source hashes and ancestry remain explicit and no signature claim is made.

---

## 10. Required revision before specialist submission

### 10.1 Establish the priority boundary conventionally

Commission or perform a theorem-level comparison with the closest stochastic-semigroup, advice-automata, probabilistic/weighted-automata, positive-realization, and quantum-automata literature. The comparison must state hypotheses and conclusions, not only thematic similarity.

### 10.2 Split the structural and quantitative papers

The clock-removal/purification/finite-quotient theory and the orbit-geometry/endpoint theory each have enough content for a focused paper. Combining them weakens both narratives.

### 10.3 Isolate the genuinely new quantifiers

For every main theorem, highlight which of the following is new:

- horizon-specific nonuniform advice;
- same width and same closed error;
- arbitrary intervening widths;
- randomized initialization;
- legal convex output constraints;
- equality at the critical boundary; or
- exact pointwise width profiles.

### 10.4 Clarify effective versus existential statements

Separate:

- existence of a finite physical quotient;
- computation of that quotient from matrix generators;
- existential-real decision for an explicitly tabulated finite group;
- construction of a minimizing realization; and
- compilation of an already supplied encoded realization.

These are different problems.

### 10.5 Treat the logarithmic gap as a central open problem

Either remove the logarithm in a nontrivial family, prove a matching lower example with a logarithm, or state clearly that the quantitative result determines only the power exponent.

### 10.6 Add an explicit finite-input endpoint example or narrow the claim

The exact exponential example is mathematically valid, but a stronger computational conclusion would require explicit finitely encoded generators and seed. Otherwise the paper should consistently describe it as an existence theorem in real compact-group geometry.

### 10.7 Keep the legal-output distinction prominent

The density-matrix and tomography results must not be summarized as ordinary categorical-output automata without the legal image constraint. State the constraint in theorem titles or immediately adjacent prose.

### 10.8 Preserve the pipeline boundary

Retain the explicit statement that none of the A/B/C/D analytic gates is closed by this work. Do not use cumulative archive size or inherited labels as significance evidence.

---

## 11. Local and editorial comments

1. In the opening model table, state immediately that `W_{N,epsilon}` excludes a sampled answer register; defer alternative charging conventions to a remark.
2. Give one compact dependency line for every constant in the uniform-orbit theorem: group metric, representation, small-ball constants, spectral gap, and orbit geometry.
3. In Lemma `orbitgap57`, explicitly distinguish the dimension of the group from the small-ball exponent `p` and the orbit dimension `q`.
4. State that the ball-average argument uses a fixed bi-invariant Riemannian metric on a compact connected Lie group.
5. Explain once why reverse chronological products under the iid word law have the same distribution.
6. In the occupation proof, display the exact integer ceiling used when replacing `a^{-1}` by the asymptotic power of `k`.
7. In Lemma `orbithull57`, state that the orbit is a smooth embedded quotient `G/G_{z_0}` and that `q` is its real dimension.
8. When converting additive support loss to multiplicative loss, name the inradius of `Q` in the span `E`.
9. In the common-row construction, say explicitly that the barycentric row may be chosen independently for each finite command and net vertex; no measurable selection theorem is needed.
10. The threshold assertion in the uniform-orbit theorem should restate that error is measured in the same norm that defines `Q`.
11. In the Grassmannian lemma, distinguish Frobenius chordal distance and the projective metric before the exact cap formula.
12. In the conjugacy-cap proof, spell out that a nonempty target ball is compared with one chosen conjugate, so no spectral decomposition of the arbitrary center `B` is required.
13. The adjacent-gap lower bound is deliberately crude; state that no dimension-uniform constant is asserted.
14. In the matrix theorem, keep the normalization from Frobenius error to the centered unit orbit visible in the theorem statement, not only in the proof.
15. The upper construction at positive tolerance uses only half the available error. Say this is deliberate slack.
16. In the algebraic-alphabet corollary, either give the embedded adjacent-`SU(2)` generators explicitly or cite a standard Lie-generation lemma.
17. State whether the imported spectral-gap theorem is used for the exact displayed generating set or only for the existence of some algebraic dense set.
18. In the tomography subsection, define the norm on the affine span before referring to an affine isometry.
19. Keep the lower and upper total-variation comparison constants next to the reconstruction formula.
20. In the extreme-orbit theorem, emphasize that one fixed suffix suffices for the cut lower bound and that its action is injective.
21. The monotonicity `n_t<=n_{t+1}` uses any fixed alphabet letter; mention explicitly that the alphabet is nonempty.
22. In the free endpoint theorem, state in its first sentence that the seed is transcendental and the generators are existentially selected.
23. Separate the dense-free theorem from the spectral-gap theorem in the proof; they play logically independent roles.
24. The Liouville-number proof is useful but interrupts the main realization argument. It belongs in an appendix.
25. In the finite-precision lemma, state the encoding assumed for algebraic matrix square roots and isolating data.
26. The output bit-length estimate is not a runtime estimate. Repeat this immediately after the bound.
27. Fair bits for hidden stochastic draws do not sample a quantum state or matrix-valued terminal output. This distinction is correctly stated and should remain.
28. In the existential-real theorem, state how instances with `k` above the trivial exact bound are normalized before formula construction.
29. The nonnegative-rank hardness is imported; cite the exact complexity corollary, not only the universality theorem in general.
30. The Ramsey number bound is intentionally enormous and irrelevant quantitatively. Consider moving it to a remark so it does not distract from the qualitative theorem.
31. In the stationarization proof, keep the neutral representative visibly inside the terminal decoder; do not name it as if it were a transition identity.
32. In the physical-equivariant theorem, write the row-action convention once before the inverse `h^{-1}` appears.
33. The finite-quotient deterministic construction stores the seed as well as the coset. Separate this coarse bound from the stochastic minimum.
34. In the phase theorem, keep the physical quotient period and the return-length gcd as separate symbols throughout.
35. The 55-page main article should not also require the referee to inspect six rendered predecessor documents for correctness of the new theorems. State clearly which are provenance only.
36. A bibliography organized by theorem role—semigroup structure, automata, compact groups, metric entropy, spectral gap, and realization—would improve readability.

---

## 12. Final recommendation

Revision 57 has crossed an important mathematical threshold. The paper now contains:

- a same-width, same-error clock-removal theorem;
- width-preserving stationary purification;
- a physical finite-action reduction;
- an equality-inclusive finite-quotient boundary;
- quantitative nonabelian orbit laws;
- legal positive matrix realizations;
- an exact exponential extreme endpoint; and
- explicit finite-description companions.

I find these results substantially more compelling than the early revision sequence, and I found no fatal mathematical defect in the central arguments after the checks described above.

Nevertheless, the work remains a specialized realization theory in a permissive nonuniform resource model, with a nontrivial but incompletely mapped classical antecedent literature, a logarithmic quantitative gap, and an exact endpoint example that is not finitely encoded. It also remains independent of the broader repository analytic pipeline.

My recommendation is therefore:

```text
Reject at Annals / Inventiones / JAMS / Acta level.

Encourage division into focused structural and quantitative papers,
followed by conventional external priority review and submission
to strong specialist or broad theoretical-computer-science/control venues.
```
