# Response to the v73 external reports — A2-DYN revision 74

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

**Author baseline:** `39575228f055862103edbebdd984bd6764fa0ad9`.

**Controlling rereview:** `e31a74560d86082da1c2f2ef55c513343cfd41a0`, `reviews/a2-dyn-v73-external-top4-rereview-2026-10-11/REFEREE_REPORT.md`, blob `28d7999c60fc0083f99ffcb8550a932057af5b8f`.

**Earlier corrected review also addressed:** `246d5e723648d51f20dcfd4632bbaf8f34aedeb4`, blob `d4115fea5cbebf1ea9788c1da7300da70736e810`.

We thank the referee for separating fixed-count finite variation from collision-uniform concentration, and for requiring an explicit physical graph rather than an appeal to a generic definability slogan. We retain the original raw pointwise theorem, every exact label, the full arithmetic transition kernel and all original source components. Revision 74 does not replace the problem by a window theorem, a pooled label, a removed source, or a different realization.

## 1. Collision-uniform paired flux and actual narrow excursions

**Rereview §§12–13, 18(1)–(3); earlier review §§12–13, 20(1)–(4).** The quantitative point is accepted. Fixed-count BV and a small integrated source do not prove the normalized essential height small.

We have sharpened the relevant quantity at the level of the complete physical density. For a nonnegative BV density f, let I_u(t) be the essential component of {f>u} containing t, and define

`S_delta f(t) = integral_0^{f(t)} (1 - |I_u(t)|/delta)_+ du`.

Module 165 proves

`[f - 2 A_delta f]_+ <= S_delta f <= min{f, incoming positive Jordan mass, outgoing negative Jordan mass}`.

Thus the incoming and outgoing endpoints must belong to the same component at the same height. The old paired minimum can charge different height layers. We give a strict example on a roof neighborhood where that minimum is one and the new bound is zero. Conversely a true narrow pulse attains the new height estimate exactly. The reserve two is shown optimal for a bound charging only components shorter than delta.

The same module proves the exact integrated component identity and the sharp bound

`integral S_delta f <= (delta/8) ||Df||_TV`.

This is explicitly an L1 estimate, not an essential-height estimate. Its use cannot conceal collision-count growth.

For the literal original b, module 166 proves the two-sided comparison

`S_M(B,delta) <= E_M + C_M B^(-1/192)` and

`E_M <= S_M(B,delta) + C_M B^(-1/192)`.

Therefore the ordered short-excursion budget has exactly the same outer limit as the original scalar error, for every legal choice of delta(B). It is also bounded by the old paired-flux budget. No threshold-current or wordwise absolute variation is substituted for the complete current.

**What is and is not closed.** The sharper inequality, exact error comparison and preservation of all source terms are proved. The collision-uniform Lorentz short-excursion tail estimate is not proved in this revision. Accordingly the full raw pointwise local limit theorem, unrestricted same-roof conditional laws and forward essential likelihood are not marked established. This is a precise remaining proof obligation, not a redefinition or abandonment of the original theorem.

## 2. A quantitative tail theorem with a legal limit order

**Rereview §18(1)–(2), §19(6); earlier review §20(4), (8).** Module 165 gives the identity

`S_delta f(t) = delta^(-1) integral_0^delta T_f(t,r) dr`,

where T_f(t,r) is the height measure of superlevel components through t of length less than r. It also gives an inverse-length moment bound with sharp scalar coefficient `beta^beta/(beta+1)^(beta+1)`.

Module 166 proves that an ordered physical bound

`T_{epsilon,M}(r) <= A epsilon^(-q) r^beta`

would give

`S_M(B,delta) <= A epsilon(B)^(-q) delta^beta/(beta+1)`.

The proof uses finite upper Riemann sums. The mesh, epsilon and delta are fixed first; then the collision limsup is taken; only afterwards is the mesh refined. Thus it does not exchange a limsup with an integral without a domination argument. Choosing `delta(B)=epsilon(B)^((q+a)/beta)` produces the stated sufficient closure rate. Every use of this estimate is labeled as an implication under a dynamical premise. No premise is promoted to a Lorentz theorem.

The required estimate controls persistence of the actual full-density levels, not word counts, total source mass or an integrated variation norm. A finite narrow-pulse control in the verifier deliberately survives with normalized height bounded below while its mass vanishes.

## 3. Explicit moving-section and tame integration proof

**Rereview §9, §18(5), §19(2)–(6); earlier review §8 and §20(5), (7).** Module 164 supplies the requested full statement.

The moving angle is represented by `q_R=tan(theta_R/2)`, the unique root on `(49/100,53/100)` of

`8 R q (1+q^2) - 4 q (1-q^2) + sqrt(3)(1-6q^2+q^4)=0`.

Endpoint signs and a derivative bound below -2 are proved by rational bounds. The actual winding root is identified, rather than replacing the section center. Its normals and p coordinates are semialgebraic. Angular section membership is tested by a dot-product inequality with a fixed center normal and fixed angular width. This includes the enlarged fifth rectangle and the original normalization `c_*=91/(10000 pi)`.

The module states the finite candidate alphabet from the uniform flight bound, a finite set containing every attainable `(n,k)`, the collision/reflection/first-hit equations, positive denominator and branch conventions, exact occupation of times 0 through m-1, and terminal membership at time m. The projection is to the original two initial coordinates. Its determinism prevents multiplicity inflation. The exact integration density is printed as

`1_Pi W_y 1_{L<=t} / [2 pi c_* (1+x^2)]`.

The parameter domain is explicit: fixed m, R in I, epsilon positive, y in `[1,2]^(2m+1)`, roof threshold real, and the finite exact-label set. The constructible integration theorem applies to this precise integrand. The derivative is asserted definable, not necessarily constructible. Uniform monotonicity is a fixed-formula assertion defining J_m, not an unproved uniform bound over increasing formulas.

The outer Stieltjes measure may be signed; each threshold restriction is positive. The compact roof range is `[m tau_-, m tau_+]`, not one common compact range for all m. These distinctions are stated in the theorem and proof.

## 4. Common source and downstream consequences

**Rereview §§14–15, §18(4); earlier review §§14–16.** The source-preserving capacity allocation in module 166 retains `s_{71,1}` and splits the original residual by a Borel coefficient of the same physical roof. Its remaining density is bounded by `S_delta b`. First incidence and clearance outside the selected disks are both retained and are not conflated. No regularity is asserted for the newly Borel-allocated subsource.

Module 167 restates the inherited positive path-remainder input explicitly and proves the scalar/path norm comparison and equality of ordered errors. It gives the exact denominator bounds, ratios and forward normalized roof-likelihood inequality on positive arithmetic classes. Zero classes remain in the unnormalized target and are never normalized. Bounded-Lipschitz convergence is not described as path-space total variation. The actual-return path still uses the original clock-transfer input; no new clock theorem is asserted here.

These consequences are not called unconditional before the scalar endpoint is established.

## 5. Article, technical supplement and provenance

**Rereview §17, §18(8); earlier review §18, §20(7).** The journal entry point is now `main.tex`, with a compact source-pinned dependency statement before the new theorems. The separate `supplement.tex` compiles the complete inherited mathematical pipeline. All 163 old core files, 12 appendices, 214 Python sources and `references.tex` are byte-identical to the frozen v73 paper tree. The four new core modules are compiled in the journal. Actual TeX recorder coverage must total all 167 distinct cores.

Old masters and replaced metadata are retained under `provenance/v73-*`. The supplement's assembly changes only the prior master title and date to identify its role; the exact old master is retained byte-for-byte. Inherited opening material and its labels still compile. Cross-document references import only mathematical labels, not amsart layout-register labels. No inherited theorem is silently deleted to make the article shorter.

## 6. Metadata, source identity and specialist review

**Rereview §3, §18(6)–(7), §19(9)–(10); earlier review §§18–20.** `SOURCE_MANIFEST.json` is the active authority. `PUBLICATION_STATUS.json`, `REFEREE_STATUS.md` and `VALIDATION.md` are deterministic projections checked without rewriting during qualification. The active README, route, response, proof ledger and build record all identify revision 74. Prior active versions are retained in provenance. All inherited Boolean claim flags are preserved, including the false endpoint, human-review and proof-certificate flags.

The final response and referee-copy branches are required to point to one author SHA. Qualification records the actual checkout SHA at runtime and pins the baseline paper tree and the controlling report blob. The two different earlier v73 review branch SHAs are recorded accurately, rather than silently treating them as identical.

Independent human specialist review has not been obtained. Native compilation, finite rational fixtures, source hashes and PDF geometry are reproducibility evidence only. The precise audit targets remain the physical height theorem, tame integration domain, oriented coarea decomposition, inherited spectral/path/clock chain and the still-needed collision-uniform physical length-tail estimate.
