# External top-four referee report on A2-DYN revision 26

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v26-referee-response-2026-10-07`, `revision/a2-dyn-v26-referee-copy-2026-10-07`  
**Reviewed commit:** `6a790b65b48f57d264dbc7871bd1ae46571c2662`  
**Reviewed repository tree:** `90c4f09735ac018b80f8735a9a0140c254fb685b`  
**Frozen ordinary paper tree:** `6101fe93f514d9586658d748e08a0ffd6c610044`  
**Active manuscript directory:** `papers/A2-DYN-v26-referee-response`  
**Immediate author baseline:** revision 25 at `4c07267338175932688a20a6021dae1b602074a0`  
**Controlling substantive report:** `reviews/a2-dyn-v25-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `b9d11ff3bc2c08bb7410d93d3128d847e277cc08` / `c24a1e7273ad3be3a233c9b3e55d32660659e9ee`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 26 is a genuine and mathematically substantial advance. It responds positively to two concrete weaknesses identified in the revision-25 report.

First, revision 25 had enlarged the prescribed-count Fourier region by proving one anisotropic box with a long flight-time direction. The new revision replaces reliance on one fixed width vector by a shape-independent theorem. It controls every measurable rescaled frequency set satisfying three quantitative bounds: a maximal radius, a four-dimensional volume, and a first radial moment. It then constructs one explicit nonrectangular dyadic cross that reaches all four coordinate axes, contains genuinely mixed directions, and retains the previously proved isotropic ball and roof box.

Second, the earlier sequence of enlarging Fourier cutoffs created a conceptual concern: each cutoff changes both the extracted-edge convolution and the residual inverse. Revision 26 identifies and preserves their exact cancellation. For a fixed finite extraction and the same physical weight, it defines a signed combined raw correction and proves the exact transport identity

```text
R_chi - R_psi = (K_psi - K_chi) * mu^L.
```

It then proves that the complete normalized change-of-cutoff contribution between the new dyadic cutoff, the previous coordinate box, and the previous isotropic cutoff tends to zero at an explicit rate.

I found no decisive counterexample in the two new mathematical modules:

- `core/55_shape_adaptive_fixed_count.tex`;
- `core/56_coherent_raw_cutoff_transport.tex`.

The weighted-volume exponent calculation is coherent. The expansion orders remain fixed. The dyadic shell count pays its entire logarithmic multiplicity in the definition of the region. The smooth cutoff is a nonnegative subsum of a product partition and has the stated support and plateau. The mixed discrete-continuous kernel uses the actual third, collision-count coordinate for count separation. The sign in the raw correction identity is correct, and the identity is formed at the density level before taking norms, so no subtraction of two infinite essential suprema occurs.

These are meaningful advances. Revision 26 closes the *transition* problem between the successive raw cutoffs and supplies a single larger fixed-count Fourier domain with constants uniform over its full, `n`-dependent shape.

The negative recommendation nevertheless remains necessary at the requested benchmark. The article is still organized around a parameter-uniform raw mixed-density local limit theorem that it does not prove.

The new nonrectangular region is not the complete isotropic ball at rescaled radius `n^(1/10)`, nor does it cover the full fixed-count complement. Compact nonzero torus frequencies, complete peripheral regimes, growing roof frequencies, and the far roof-frequency splice remain. More decisively, the cutoff-transport theorem proves only that the *difference* between three signed raw corrections is small. It does not prove that their common signed correction is small. It does not prove isolated local-edge smallness, an absolute complementary residual estimate, or the genuine long-time second-derivative budget at a collision cutoff proportional to `n`.

The weighted raw denominator and the relative replacement of completed-return events by exact physical-time and lattice observation events also remain open.

These are load-bearing mechanisms of the advertised raw theorem. They are not presentation details. The new transport theorem has usefully reduced several apparent interfaces to one common raw remainder, but that common remainder is still uncontrolled.

The unconditional package is now unusually substantial for a single Lorentz family. A reorganized article centered on the completed Gaussian, functional, moment, phase, finite-extraction, averaged-orbit, isotropic fixed-count, anisotropic fixed-count, shape-adaptive, and cutoff-transport results could be a strong specialist contribution after independent expert review. That is a different editorial claim from acceptance at the requested four-journal benchmark for the still-unproved raw endpoint.

## 2. Frozen source, chronology, and exact qualification

The two named revision-26 author branches resolve to the same commit:

`6a790b65b48f57d264dbc7871bd1ae46571c2662`.

The repository tree at that commit is

`90c4f09735ac018b80f8735a9a0140c254fb685b`.

The frozen ordinary paper tree is

`6101fe93f514d9586658d748e08a0ffd6c610044`.

The immediate mathematical baseline is revision 25 at

`4c07267338175932688a20a6021dae1b602074a0`,

with ordinary paper tree

`5c5378441102a155ccbf76f4b7f18d426390d3a9`.

The controlling revision-25 report is frozen at commit

`b9d11ff3bc2c08bb7410d93d3128d847e277cc08`

and blob

`c24a1e7273ad3be3a233c9b3e55d32660659e9ee`.

Revision 26 preserves all fifty-four inherited core files, all forty-nine inherited Python files, every inherited mathematical label, and the bibliography. Five exact source edits affect the main article. The earlier abstract is retained separately in `HISTORICAL_ABSTRACT.md`. The revision adds the two proof modules named above and `SHAPE_AND_RAW_TRANSPORT_INPUT_MAP.md`.

The source records correctly distinguish the completed statements from the remaining endpoint. In particular they record:

- `shape_adaptive_fixed_count_proved: true`;
- `full_isotropic_one_tenth_band_proved: false`;
- `full_fixed_return_complementary_integral_proved: false`;
- `isolated_active_edge_smallness_proved: false`;
- `exact_physical_event_replacement_proved: false`;
- `full_raw_LLT_proved: false`.

The exact-source qualification completed successfully on both reviewed branches:

- response branch run `37537199282`;
- referee-copy branch run `37537242097`.

For the response branch, exact checkout, source and report-scope archiving, native TeX and numerical-check installation, normal and optimized verification, complete article build, PDF metadata and proof-page rendering, and artifact upload all completed successfully.

The response artifact is

`11446932702`,

named

`a2-dyn-v26-6a790b65b48f57d264dbc7871bd1ae46571c2662`,

with digest

`sha256:110ca336b9a9d05159c95a6f9f59a44157754a13e031b126a70c85f9e3f8b15d`.

These facts establish exact source identity and successful execution of the declared finite checks and native build. They do not certify the continuum billiard inputs, the high-order collision estimates, the new measurable-shape theorem, the common raw remainder, or the full local limit theorem.

The present review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v26-external-top4-review-2026-10-07/`.

No manuscript source, author branch, workflow, earlier report, or unrelated repository path is modified.

## 3. Executive description of the new mathematics

Revision 26 adds two theorems, designated P and Q in the introduction.

Theorem P has two levels.

At the abstract level, it gives a fixed-count Fourier bound for an arbitrary measurable rescaled set `Omega_n` satisfying

```text
sup_{v in Omega_n} |v|        <= C n^(9/100),
|Omega_n|                     <= C n^(41/175),
integral_{Omega_n} |v| dv     <= C n^(67/280).
```

For the actual transform at a prescribed return count and one actual-return insertion, it proves

```text
n^2 integral_{n^(-1/2) Omega_n, |z| >= 2 n^(-99/200)}
    |Phi_n^[k],a(z)| dz
 <= C [ M_a n^(-3/280) + V_a n^(-5559/175) ].
```

At the concrete level, it constructs one nonrectangular domain `H_n` as a finite union of dyadic boxes. Its scale budget is determined by

```text
a_n = 2 n^(1/200),
U_n = n^(9/100),
T_n = n^(67/280) / log(2+n)^3,
(product_i lambda_i) max_i lambda_i <= T_n,
max_i lambda_i <= U_n.
```

This domain reaches all four coordinate axes to rescaled order `n^(9/100)`, includes mixed directions beyond the old isotropic exponent, and has the required volume and first-moment budgets.

Theorem Q defines, for one exact finite extraction `mu^L = E + Q`, the signed raw correction

```text
R_chi = e - K_chi * E + F^(-1)[(1-chi) Q_hat].
```

It proves

```text
R_chi = p^L - K_chi * mu^L,
R_chi - R_psi = (K_psi - K_chi) * mu^L.
```

For the new dyadic cutoff, the previous coordinate-box cutoff, and the previous isotropic cutoff, it then establishes on the actual central windows

```text
n^2 ess sup |R_chi - R_psi|
 <= C [ M_a n^(-3/280) + V_a n^(-983/350) ]
    + C_P M_a n^(-P).
```

This theorem proves that enlargement of the known Fourier domain does not create a new independent raw obstruction. It does not estimate the common value of the raw correction.

## 4. Audit of the weighted-volume criterion

The first new proof replaces a fixed exponent vector by three geometric quantities. This is a useful conceptual simplification.

The stopping comparison contributes

```text
C M_a n^(-1/4) integral_{Omega_n} |v| dv.
```

With first radial moment at most `C n^(67/280)`, this is exactly

```text
C M_a n^(-3/280).
```

The deterministic collision interval has length `n/c_* + O(1)`, uniformly in the prescribed mark.

The proof then uses the inherited high-order damped-unsmoothing theorem with fixed choices

```text
P = 26,
Q = 29,
delta   = n^(-19/100) / 4,
epsilon = n^(-32) / 4.
```

The residual phase is expanded through degree fifty-one, whereas the smoothed spectral logarithm is controlled through degree twenty-nine. These are separate finite expansions. No argument requires them to have the same degree, and neither order grows with `n`.

The maximal radius `n^(9/100)` gives the same two analytic margins as the concrete roof box:

```text
1/2 - 9/100 - 2(19/100) = 3/100,
28(1/2 - 9/100) - 2(19/100)(30) = 2/25.
```

Thus the smoothed real-frequency damping remains valid uniformly over the entire measurable set.

The fine insertion error is bounded by volume times `epsilon V_a`. Its decay exponent is

```text
32 - 41/175 = 5559/175.
```

The fine residual replacement has exponent

```text
32 - 41/175 - 51(1/2 + 9/100) = 1173/700.
```

For the residual moment term with `b` nonsingleton blocks, the displayed exponent before taking its negative decay sign is

```text
41/175 + 52(9/100) - 26 + (81/100)b.
```

The largest value occurs at `b=26`. Its decay is

```text
26(19/100 - 18/100) - 41/175
 = 9/350
 = 3/280 + 3/200.
```

The strict extra margin `3/200` absorbs the fixed logarithmic factor. Decreasing `b` improves the power by `81/100` for each removed block. In particular, the connected `b=1` contribution is not omitted.

The damped polynomial term has a fixed polynomial prefactor, including the cost of at most fifty-two multipliers, and an exponential factor at most `exp(-c n^(1/100))` outside the original central ball. It is therefore negligible relative to any fixed inverse power.

I found the exponent calculation coherent. The proof uses only the supremum, volume, and first radial moment of the measurable set. It does not covertly require boundary regularity or a fixed, `n`-independent shape.

The load-bearing input that still warrants independent specialist inspection is the uniform use of the inherited collision-space power bound inside chronological words with up to fifty-two smooth multipliers. The manuscript includes all resulting fixed-order constants in a fixed constant depending on `P` and `Q`; it does not claim uniformity as the order grows. I found no internal contradiction in that use.

## 5. Audit of the weighted dyadic cross

The dyadic construction is designed to turn the shape criterion into one explicit domain with a common set of constants.

For a four-tuple of nonnegative integers `j`, write

```text
S(j) = sum_i j_i,
J(j) = max_i j_i.
```

The proof bounds the number of tuples with `S+J=t` by `C(t+1)^3`. Choosing one coordinate attaining the maximum and then distributing the remaining sum among three coordinates gives this upper bound. Tied maxima are overcounted, which is harmless.

Consequently

```text
sum_{S+J <= K} 2^(S+J) <= C 2^K (K+1)^3.
```

With base scale `a`, product threshold `T`, and maximum scale `U`, this yields

```text
sum_j (product_i lambda_i) lambda_* <= C T log(T/a^5)^3,
sum_j  product_i lambda_i          <= C (T/a) log(T/a^5)^3.
```

The revision takes

```text
a_n = 2 n^(1/200),
U_n = n^(9/100),
T_n = n^(67/280) / log(2+n)^3.
```

The logarithm in `T_n` pays the full dyadic counting loss. It does not reappear in the final central rate.

For the union `H_n` of the corresponding boxes, the second scale sum gives

```text
|H_n| <= C n^(67/280 - 1/200) = C n^(41/175).
```

The first scale sum gives

```text
integral_{H_n} |v| dv <= C n^(67/280).
```

The maximal radius is at most a fixed multiple of `n^(9/100)`. Thus the set satisfies the measurable-shape theorem with one fixed constant.

The support description using

```text
x_i(v) = max{a_n, |v_i|},
x_*(v) = max_i x_i(v)
```

is also correct up to the displayed fixed constants. The inner product condition selects dyadic scales within a factor two of each coordinate and leaves the required factor thirty-two in the product budget.

The domain contains the original central ball. It reaches each coordinate axis to order `n^(9/100)` in rescaled variables, corresponding to physical order `n^(-41/100)`. This is a genuine improvement over revision 25, which gave that long reach only in the roof direction.

It also contains new mixed directions. For example, the exponent vector

```text
(1/25, 1/25, 1/25, 1/20)
```

has sum plus maximum `11/50`, strictly below `67/280`.

The manuscript correctly states the limitation. The domain is not the full isotropic ball of radius `n^(1/10)`. A vector with all four coordinates of order `n^(3/50)` violates the product budget. Therefore Theorem P enlarges the proven region in a nontrivial and useful way but does not close the entire farther annulus.

## 6. Audit of the smooth nonrectangular cutoff

Revision 26 constructs a smooth cutoff adapted to the dyadic cross rather than using the indicator of the union.

Let `chi_0` be even, compactly supported, and nonincreasing on the positive half-line. Define a nonnegative dyadic partition

```text
phi_0(t) = chi_0(t),
phi_j(t) = chi_0(t/2^j) - chi_0(t/2^(j-1)),  j >= 1.
```

The full product partition sums to one. The new cutoff `Xi_n` is the subsum over admissible four-tuples.

Because all summands are nonnegative,

```text
0 <= Xi_n <= 1.
```

Every summand is supported in its associated box, so `Xi_n` is supported in `H_n`.

At a point in the stated inner product region, every nonzero dyadic product has admissible scales. Hence the subsum equals the full product partition and is one. On the original central ball, only the zero-scale product is nonzero and it equals one.

This verifies the support and plateau statements. In particular, the new cutoff vanishes outside a region where the full-law transform has already been controlled, while remaining one on the inherited central ball.

For the inverse kernel, each one-dimensional dyadic factor is a difference of two dilates of fixed Schwartz functions. Tensorization gives

```text
|K_n^sharp(x)|
 <= C_J sum_j product_i [ B_{j,i} (1+B_{j,i}|x_i|)^(-J) ].
```

The first three output coordinates remain integer-valued. The argument does not replace them by continuous variables. The frequency support lies inside one torus chart for sufficiently large `n`, so the mixed inverse convention is consistent.

The high-count support is separated in the third coordinate. Every third-coordinate physical scale is at least

```text
2 n^(-99/200).
```

Across a count gap of order `n`, this supplies decay `n^(-101J/200)`. Multiplying by the remaining scale sum and by the raw factor gives

```text
n^2 sup |K_n^sharp * T_high|
 <= C_J M_a n^(41/175 - 101J/200).
```

Thus a fixed sufficiently large Schwartz order yields any prescribed inverse power. The argument correctly uses the third, count coordinate rather than the larger roof-frequency scale.

## 7. Audit of the exact raw correction identity

This is the most conceptually useful addition in revision 26.

Fix one finite extraction

```text
mu^L = E + Q,
p^L  = e + r,
```

where the residual transform is integrable. For a smooth compactly supported cutoff `chi`, define

```text
R_chi = e - K_chi * E + F^(-1)[(1-chi) Q_hat].
```

Absolute residual inversion gives

```text
F^(-1)[(1-chi) Q_hat] = r - K_chi * Q.
```

Therefore

```text
R_chi = e + r - K_chi*(E+Q)
      = p^L - K_chi * mu^L.
```

Subtracting the identities for `chi` and `psi` gives

```text
R_chi - R_psi = (K_psi - K_chi) * mu^L.
```

The sign is correct.

In frequency form, the change of the extracted-edge contribution and the change of the residual contribution combine into

```text
(psi-chi) mu_hat^L.
```

This is precisely the cancellation lost if the two changes are bounded separately in absolute value.

Because the cutoff difference is compactly supported and the Fourier transform of the finite measure is bounded, the difference has a bounded continuous representative. The proof forms the almost-everywhere density identity first and takes norms only afterward. It does not subtract two potentially infinite essential suprema.

The theorem does not depend on a special choice of extraction beyond the stated exact decomposition and integrable residual transform. It introduces no estimate for the long-time derivative sum.

I regard this algebraic reorganization as correct and valuable.

## 8. Audit of the quantitative cutoff transport

The revision compares three cutoffs:

- the new dyadic cross cutoff;
- the previous coordinate-box cutoff;
- the previous isotropic cutoff.

Each equals one on the original central ball. The support of any pairwise difference is contained in the retained union of the new cross, the old roof box, and the old isotropic region.

For the full marked law at the prescribed count, the existing fixed-count Fourier estimates therefore give

```text
n^2 integral |chi-psi| |mu_hat_full| dz
 <= C [ M_a n^(-3/280) + V_a n^(-983/350) ].
```

This is not inferred from an averaged return-count theorem.

For the truncated law, write

```text
mu^L = mu_full - T_high.
```

The high-count convolution is controlled by the relevant count-separation bounds for the two kernels. This gives, on the actual central windows,

```text
n^2 ess sup |R_chi - R_psi|
 <= C [ M_a n^(-3/280) + V_a n^(-983/350) ]
    + C_P M_a n^(-P).
```

The stronger global statement under the additional cumulative-tail slope follows by combining exponential high-count mass with polynomial kernel suprema.

The corollary stating that smallness of the signed raw correction for one cutoff is equivalent to smallness for all three is then a direct triangle-inequality consequence, under the displayed weight growth assumptions.

This closes the *change-of-cutoff* contribution. It means that future work can select whichever of the three cutoffs is most convenient without creating a second independent local remainder.

The manuscript correctly does not infer either of the following:

- smallness of the isolated extracted-edge term;
- smallness of the absolute residual integral.

A signed cancellation may make their sum small while either absolute piece is large.

## 9. What revision 26 closes from the preceding report

The revision-25 report identified that a single elongated box left most mixed directions untreated. Revision 26 materially improves this point.

It proves a theorem uniform over `n`-dependent measurable shapes rather than applying a fixed-exponent theorem with uncontrolled constants. It then gives one explicit domain whose constants are common to all scales.

The new domain reaches all four axes, not only the roof axis. It includes mixed directions outside the old isotropic ball. The entire old isotropic ball and roof box are retained rather than replaced.

The preceding report also emphasized that each new cutoff must carry its own raw edge and residual terms. Revision 26 goes further: it proves that the *combined signed correction* transforms coherently and that the complete transition between the three cutoffs vanishes quantitatively.

Accordingly, two objections are now closed:

1. the known fixed-count domain is no longer merely one fixed coordinate box;
2. enlargement of the cutoff no longer introduces an unconnected raw interface.

These closures should be credited as substantial progress.

## 10. The remaining fixed-count frequency complement

The complete raw theorem still requires control outside the retained union.

The new cross has maximal rescaled coordinate size `n^(9/100)`, but it is restricted by a product-volume budget. It is not the full ball of radius `n^(1/10)`.

The following regions remain, among others:

1. balanced mixed directions in which several coordinates are simultaneously between the old isotropic exponent and `1/10`;
2. the remaining part of the farther small-frequency annulus;
3. compact nonzero lattice and count torus frequencies;
4. all relevant peripheral return phases at the prescribed count;
5. growing roof frequencies outside the cross;
6. the far roof-frequency tail and its strict splice with finite-band bounds.

A proof of the full complementary integral need not literally establish one isotropic ball if another cover controls every required frequency. However, it must cover the entire complement with one compatible normalization and weight class. The present union does not do so.

The old direct-orbit mean-square theorem, cyclic spectral arc bounds, exterior Abel estimate, and fixed-test-frequency Cauchy limit still cannot replace this prescribed-count absolute integral.

## 11. The common signed raw remainder

Revision 26 has usefully shown that the three cutoffs share one local raw problem up to a vanishing error.

For the new cutoff, the exact identity on the central count labels is

```text
p_n^[k],a
 = K_n^sharp * mu_n^[k],a
   + R_chi^a,L_n
   - K_n^sharp * T_high^a,L_n.
```

The central full-law term and high-count term are controlled. The unresolved object is the signed common correction

```text
R_chi^a,L_n = p^a,L_n - K_chi * mu^a,L_n.
```

The new transport theorem proves that replacing `chi` changes this object by `o(n^(-2))` on the local scale. It does not prove

```text
n^2 ||R_chi^a,L_n||_infinity -> 0.
```

This distinction is decisive.

Future work has two legitimate routes.

One route is to prove the isolated edge correction and absolute residual integral small, together with the far-roof estimate. This is sufficient but may be stronger than necessary.

A potentially sharper route is to estimate the common signed correction directly, preserving cancellation between extracted edge and residual. Revision 26 makes this route mathematically well posed and cutoff-independent.

Either route must produce an actual local bound for the common correction. Cutoff transport alone cannot supply it.

## 12. Long-time finite-count preparation and the derivative budget

The exact finite-count extraction remains qualitative at each fixed packet. At a linear collision cutoff

```text
L_n proportional to n,
```

the raw far-roof estimate still contains

```text
A_2(n,L_n,R,w)
 = sum_ell || partial_t^2 r_n,R^{w,L_n}(ell,.) ||_1.
```

The new dyadic and cutoff arguments do not bound this quantity.

A usable long-time estimate must control the true growth of:

- the number of singular and regular cells;
- prepared power and logarithmic exponents;
- distances of exponents from critical integrability thresholds;
- germ radii;
- jet coefficients;
- singular-value and critical-value coalescence;
- inverse-coarea Jacobians;
- derivative integrals on regular intervals;
- all dependencies on the radius, count cutoff, and physical weight.

Fixed-order moments of bounded collision observables do not imply these pushforward-density derivative bounds.

The cutoff-transport theorem avoids creating a *second* derivative budget merely to compare cutoffs. It does not establish the original budget.

## 13. Isolated edge and absolute residual estimates

For the new cutoff the article still records the extended-real quantities

```text
E_sharp = ess sup |e - K_sharp * E|,
C_sharp(B) = integral_{|b|<=B} |1-Xi_n| |Q_hat|.
```

The raw inequality contains

```text
n^2 E_sharp,
n^2 C_sharp(B),
n^2 A_2 / (pi B).
```

No smallness theorem is proved for the first two absolute quantities.

This is not a logical defect in the new cutoff-transport theorem. The theorem deliberately estimates their signed combined change. But it remains a missing part of the advertised raw local limit theorem unless the common signed remainder is controlled by another argument.

Authors should not infer isolated absolute estimates from the signed transport identity. The manuscript presently avoids that inference.

## 14. Weighted raw theory and denominator asymptotics

The new fixed-count Fourier theorem applies to a bounded-BV function of one actual marked return.

The raw extraction additionally requires finite-record admissibility of the exact weight

```text
w_n,k,R = c_* a composed with (F_R^*)^k.
```

The cutoff-transport theorem applies to the intersection of these two classes and uses the same weight, count, mark, extraction, and cutoff conventions on both sides.

This is correct, but it does not prove that the downstream physical observation indicators belong to a class with all required uniform budgets.

The final conditional theorem still requires:

- the full weighted fixed-count complement;
- a weighted common raw-remainder estimate;
- weighted long-time derivative control;
- the raw asymptotic of the exact denominator;
- stability under the actual terminal and path observations used in the application.

The same-event marked conclusion divides by the identical existing probability. It is not a raw denominator theorem.

## 15. Relative physical-event replacement

No physical event is replaced in revision 26.

The new transport theorem compares analysis cutoffs for one fixed measure. It does not compare two events.

The final application still needs a relative estimate between:

- the completed-return event used in the return-map analysis;
- the exact physical-time and lattice observation event in the stated application.

An absolute unfinished-return or clock error is insufficient under a rare lattice constraint unless it is small relative to the true raw denominator.

The previous `L^q` clock estimates and the present shape estimates do not establish that relative comparison.

## 16. Correctness assessment and specialist verification

I found no decisive contradiction in the new proofs.

The following points are load-bearing and should receive independent human specialist verification:

1. the simultaneous use of fixed high-order collision estimates through residual degree fifty-one and up to fifty-two smooth multipliers;
2. the uniformity of the measurable-shape theorem over all sets satisfying only the three geometric bounds;
3. the weighted dyadic tuple count and its conversion into both volume and first radial-moment estimates;
4. the plateau proof for the nonnegative product-partition cutoff;
5. the mixed torus/real inverse transform and its coordinatewise Schwartz estimate;
6. the use of the third coordinate, rather than the maximal roof scale, in count separation;
7. the almost-everywhere density identity defining the coherent raw correction;
8. the sign and Fourier normalization in the exact cutoff-transport formula;
9. the transfer from full-law fixed-count estimates to the truncated correction using the high-count signed measure;
10. the uniform weight-class intersection in the quantitative transport theorem.

These are verification requests, not detected counterexamples.

The finite diagnostics check the rational exponents, tuple counts, partition plateaux, count-coordinate powers, and finite Fourier cancellation identities. They do not prove the continuum collision-space inputs or the long-time raw-density estimates.

## 17. Top-four significance assessment

The manuscript now contains a very large unconditional package for one carefully engineered triangular Lorentz family:

- exact physical return records and compensation;
- parameter-uniform Gaussian and functional limits;
- growing central Fourier integrals;
- marked initial, terminal, intermediate, and logarithmic-window results;
- unsmoothed moments and all fixed marked Gaussian moments;
- uniform covariance nondegeneracy;
- measurable phase rigidity and quantitative phase defects;
- actual-return and peripheral phase lifting;
- compressed local resolvent statements with their limitations recorded;
- exact finite-count edge extraction;
- prescribed-count isotropic and anisotropic Fourier regions;
- arbitrary fixed-order damped unsmoothing;
- a shape-adaptive fixed-count region;
- coherent signed transport among several raw cutoffs.

Several ideas are mathematically interesting. The bounded collision compensation, exact return stopping, high-order damped unsmoothing, observed count-coordinate localization, shape-adaptive Fourier criterion, and coherent cutoff transport are particularly notable.

At the four-journal benchmark, however, the paper is still organized around a theorem that remains unproved. The remaining common raw remainder, full fixed-count complement, long-time derivative budget, weighted denominator, and exact-event replacement are central to that endpoint.

The manuscript is also highly specialized to one family. In the absence of the advertised endpoint, a four-journal case would require a broadly formulated principle with applications in several substantially different systems. Revision 26 does not yet provide that breadth.

I therefore do not recommend acceptance or another journal-managed major revision at the requested benchmark in the current form.

A specialist-journal version centered on the completed results could be very strong. Such a version would need a substantial reorganization so that conditional raw interfaces are not presented as the principal completed theorem.

## 18. Required work before another top-four review

### A. Close the remaining fixed-count frequency complement

Prove an actual prescribed-count integral estimate over every frequency not already covered by the central and retained domains.

The proof must include compatible treatment of:

- balanced mixed small frequencies;
- compact nonzero torus frequencies;
- full peripheral return phases;
- growing roof frequencies;
- the far roof tail;
- one strict splice with the true constants and weight losses.

A non-isotropic cover is acceptable, but it must cover the entire complement.

### B. Prove smallness of the common signed raw remainder

Use revision 26's cutoff-independence theorem to focus on one cutoff and prove

```text
n^2 ||R_chi^{a,L_n}||_{L^infinity(central window)} -> 0
```

uniformly in the required radius and weight class.

This may be done by separate absolute edge and residual estimates or by a direct signed-cancellation argument. The latter is now a legitimate and potentially sharper target.

### C. Establish the genuine long-time preparation bound

Give a quantitative bound for `A_2(n,L_n,R,w)` at `L_n` proportional to `n`, with all radius, weight, and count dependencies explicit.

If a direct common-remainder proof avoids this particular quantity, the replacement argument must provide an equally strong far-roof control.

### D. Complete the weighted raw denominator theory

For the actual downstream indicator classes, prove:

- the weighted full complement;
- the weighted common remainder;
- the weighted derivative or replacement tail estimate;
- the exact raw denominator asymptotic.

State precisely which bounded-BV, finite-record, multiple-time, and physical-event classes are stable under every operation.

### E. Prove relative physical-event replacement

Compare the completed-return event with the exact physical-time and lattice event at the scale of the same raw denominator.

The comparison must be relative, not merely an absolute clock estimate.

### F. Obtain independent specialist verification

The collision-space spectral inputs, high-order multiplier words, constructible finite-count preparation, mixed Fourier normalization, and coherent correction identity should be checked by independent experts before a claim at this level is renewed.

## 19. Presentation and technical comments

1. The distinction between the measurable-shape theorem and the concrete dyadic cross should remain explicit.

2. The manuscript should continue to state that the cross is not the full isotropic `n^(1/10)` ball.

3. Both physical and rescaled frequency scales should be displayed whenever a new region is introduced.

4. The fixed nature of `P=26` and `Q=29` should remain visible; no limit in the expansion order is taken.

5. The connected `b=1` residual term should remain in the exponent ledger.

6. The logarithmic factor in `T_n` should continue to be explained as payment for the dyadic counting multiplicity.

7. The inner and outer product descriptions of `H_n` are useful and should be kept near the theorem statement.

8. The cutoff `Xi_n` should remain distinguished from the sharp indicator of `H_n`.

9. The fact that the third coordinate is collision count, while the fourth is roof time, should remain stated beside the high-count kernel estimate.

10. The coherent correction should be defined before any absolute edge or residual bounds are introduced.

11. The almost-everywhere identity should continue to precede the norm comparison, avoiding any impression of subtracting extended-real quantities.

12. The phrase *complete change-of-cutoff contribution* is acceptable only when accompanied by the statement that the common correction itself is not bounded.

13. The manuscript should not infer isolated edge smallness from signed correction transport.

14. The intersection of bounded-BV marked weights and finite-record admissible weights should remain explicit.

15. Same-event conditioning should remain distinguished from physical-event replacement.

16. Collision-clock absolute correlation summability should remain distinguished from induced-map Cesaro covariance.

17. Workflow qualification should remain described as execution evidence, not proof certification.

18. The separate `HISTORICAL_ABSTRACT.md` is acceptable as provenance, provided the article abstract itself accurately states the incomplete raw endpoint.

19. The introduction could benefit from one compact diagram showing the central ball, isotropic band, roof box, dyadic cross, and uncovered complement. This is a presentation suggestion, not a mathematical requirement.

20. Given the length of the article, a short theorem-dependency roadmap in the main text, rather than only in source maps, would materially aid expert verification.

## 20. Verification boundary

The successful exact-SHA workflows establish that:

- both named author branches point to the reviewed SHA;
- the declared source tree was checked;
- inherited-file and label-preservation diagnostics ran;
- normal and optimized finite checks agreed;
- the native TeX article built successfully;
- the qualification artifact was uploaded.

They do not establish:

- the continuum billiard-space estimates;
- the validity of every high-order chronological operator word;
- the uniform constructible-preparation constants at linear count cutoff;
- the full complementary Fourier integral;
- smallness of the common raw remainder;
- the weighted raw denominator;
- relative physical-event replacement;
- journal acceptance.

## 21. Final recommendation

Revision 26 should be credited for two substantial achievements:

1. a shape-adaptive prescribed-count Fourier theorem yielding one explicit four-direction dyadic region at the retained central rate;
2. an exact and quantitative coherent transport theorem showing that the signed raw correction is cutoff-independent up to a vanishing normalized error.

I found the new logic coherent and no decisive counterexample in the two added modules.

Nevertheless, the complete raw mixed-density local limit theorem remains unproved. The common raw remainder, full fixed-count complement, long-time density derivative control, weighted denominator, and exact physical-event replacement remain central open responsibilities within the manuscript.

**Recommendation: reject in the present form at the requested top-four benchmark.**
