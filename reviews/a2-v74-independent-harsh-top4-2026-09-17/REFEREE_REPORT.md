# Independent referee report on A2, revision 74

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment. It is not a commissioned journal report, an editorial decision, or a formal proof certificate. Earlier reports are evidence of the revision history, not authority for this assessment.

## 1. Recommendation

**I do not recommend acceptance at the requested highest general-journal level in the present form. The new moment reconstruction and charged estimation results survive the examination reported here: I establish no new fatal error in their core proofs. Revision 74 provides a correct-looking and useful structural refinement, but it does not, in my judgment, establish the exceptional mathematical significance needed to reverse the negative placement recommendation.**

The main reason is not a missing build artifact, an unproved matrix identity, or a demand that every statistical result be minimax optimal. The new algebra is an elementary exact rank-two reconstruction, its conditioning follows from signed monotonicity, and the improved statistical exponents arise from estimating four one-dimensional weighted profiles instead of a two-dimensional density. The difficult geometric inputs remain the differentiated relative physical law and the actual smooth contact inverse developed earlier. These inputs deserve serious consideration; the new corollaries should not be counted as independent solutions of those problems.

This distinction must remain explicit in any response. “No newly identified fatal error” is not a certificate that every theorem in the 365-page technical manuscript is correct. Conversely, a negative top-four recommendation does not manufacture a theorem gap that can be closed by another revision number, a longer appendix, or another successful workflow.

## 2. Immutable object and scope of examination

| Object | Identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Current source branch | `revision/a2-v74-moment-reconstruction-2026-09-17` |
| Source-branch head inspected | `5076a85439d8bb0f770b6c80e23b82ea2d27aa4b` |
| Compiled manuscript source | `c52fa361108a0f716d9e89017cd97eea71b0f3da` |
| Manuscript subtree | `48787e35d236d4a896abe328d78eff0ef154fdee` |
| Native-products branch | `revision/a2-v74-native-products-35181781858-1` |
| Native-products head; parent selected for this review | `c6f0c23625ff35fc695d26b0e4ad451bbcbf333d` |
| Native-products repository tree | `c5920a93b5c0164f999926a243b626df8e0dce26` |
| Preceding v73 report | `9c69f03f97dea57e83061af96aeb9bfe4dcc80d3` |
| Retrieved workflow artifact | run `35181781858`, artifact `10480077964` |

The operative source directory is `papers/A2-v17-boundary-information-coarsening/`; the historical directory name does not mean that revision 17 was reviewed. Connected branch discovery, repeated before delivery, identifies v74 as the latest revision found. The connected comparison from the compiled source to the source-branch head contains only root handoff documentation. The comparison to the native-products head contains those documentation changes and delivery additions, with no manuscript changes. [G1–G3]

### Fresh mathematical reading

The examination includes the complete new 487-line moment section, its overview and unified abstract, the current principal introduction, the response and historical derivation audit. It also includes the complete current single-law, complete-record, local-completion and smooth-contact modules; the periodic relative/physical-law module; and the coordinate, actual-envelope, signed finite-jet and positive quadratic arguments on which the new inverse depends. For the latter two source files, the reviewed core is the contact-inverse material through the signed cyclic response and the global quadratic inverse through its first image examples, rather than a new audit of their entire later analytic and stopping branches. [S1–S9]

The analytic Banach inverse, real-to-complex continuation estimates, global registration/lattice catalogue, older information/coarsening/acquisition catalogue and two-collision companion have **not** received a new complete theorem-by-theorem recertification in this session. Their presence in a compiled entry is not substituted for that work. The report therefore gives a detailed judgment on the new contribution and its main smooth/physical dependency chain, not an unconditional approval of all historical material.

### Native-object verification

Unlike the preceding report, this review retrieved the binary workflow archive. The independent script in this directory verified all **992** frozen source files against their lengths, SHA-256 hashes, Git blob hashes and ZIP file modes, then reconstructed the manuscript Git tree exactly as `48787e35d236d4a896abe328d78eff0ef154fdee`. The source ZIP hash is `5bd86317bfc2433ca0735bae6e3944afe51aa7c56f1f05fb5dbdb6404104a6ff`.

| Retrieved native entry | Independently counted pages | SHA-256 |
|---|---:|---|
| `rigidity.pdf` | 190 | `90fe54a362e62add088253aa3bf4f266585bcfdf95a027c689688342addbfe9f` |
| `main.pdf` | 365 | `c209fcd631be3168ec58240319823dd274ddd6377fc051af3da37aa306d593d2` |
| `two_collision.pdf` | 7 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |

These hashes agree with the pinned handoff. The entries overlap and must not be added as independent mathematical output. Local rendering and visual inspection covered principal pages **1, 8, 54–60, 153–155 and 190**, full-manuscript pages **1 and 365**, and companion pages **1 and 7**. No blocking clipping or missing-symbol issue was found on this sample. This is not an all-page visual certificate.

I did not locally rebuild the TeX or reproduce the CI execution. The build logs remain author/workflow-generated evidence. The independent checks establish the identities of the retrieved source and product objects; they are not a substitute for a fresh compilation or a mathematical proof. [D1]

## 3. Disposition of the v73 report

**R73-P1, missing handoff: resolved.** The root v73 historical entry now exists, a current v74 entry is present, and the current route distinguishes the frozen source from its later documentation and native products. The previous missing-file objection should not be repeated.

**R73-P2, preparation measure: resolved at the level examined.** The unified abstract and observation description now specify independent normalized unit-speed Liouville preparations, exact acceptance gates and exact success/failure tags. The claim concerns recovery without separately supplied local amplitudes, not recovery under an arbitrary unknown reset density or unknown detection efficiency. Coordinate errors are post-acceptance errors. This is a substantive clarification of the observation model, not merely a verbal concession. [S2, S3]

**R73-M1–M7: retained with the necessary qualifications.** The same-gate area anchor, both directions of the germ-level invariant, logarithmic twist sensitivity, curvature-before-profile argument, physically realizable selection, charged counting and finite-clock amplitude correction remain operative. The v74 response does not pretend that the previous report required another theorem to repair an identified fatal contradiction. That is appropriate. The significance objection remains an editorial judgment, not an unacknowledged list of new mathematical obligations. [R1, S2]

## 4. Examination of the new moment reconstruction

### R74-M1. The matrix identity is correct, but classical in mechanism

**Location:** Lemma 10.1, principal p. 55; `lem:v74-skeleton`, S1 lines 38–83.

Write the rank-two kernel as

$$
f(u,v)=a(u)^{\mathsf T}Cb(v),\qquad
L=\int_J\binom{1}{u}a(u)^{\mathsf T}\,du,
\quad R_0=\int_J b(v)(1\ \ v)\,dv.
$$

The definitions give

$$
H_f=LCR_0,\qquad M(u)=a(u)^{\mathsf T}CR_0,
\qquad N(v)=LCb(v).
$$

If the square product is nonsingular, each factor is nonsingular; cancellation gives precisely

$$
f(u,v)=M(u)H_f^{-1}N(v).
$$

The matrix need not be symmetric. The orientation of the row and column factors is correct. An independently checked nonsymmetric polynomial example satisfies this identity and fails with the transposed inverse, so the check is not protected by accidental symmetry.

On a bounded compressed-data set with a determinant floor, the adjugate formula controls the inverse. For total derivative order at most m, the differentiated kernel is `M^(i)(u) H^{-1} N^(j)(v)`. The inverse-resolvent identity and replacement of one factor at a time give the stated C^m Lipschitz bound without an extra derivative. This is a deterministic statement about the reconstruction map; no stochastic independence of its factors is needed.

The paper's attribution to the exact CUR literature is appropriate. Hamm–Huang's exact decomposition theorem supplies the relevant classical low-rank context; the present moment functionals are not literally sampled rows and columns, but the cancellation mechanism is the same elementary factorization argument. That source does not prove the billiard result, and the billiard application does not turn the general matrix identity into a new foundational theorem. [L1]

**Finding:** no algebraic or derivative-loss defect is established. Its value here lies in compatibility with the geometric model and its finite-flight comparison, not in novelty of the cancellation identity.

### R74-M2. Geometric nondegeneracy is proved, with essential class dependence

**Location:** Proposition 10.2, pp. 55–56; `prop:v74-nondegeneracy`, S1 lines 86–144.

For

$$
f=Z^{-1}w(u)z(v)\{d-A(u)-C(v)\},
$$

the choice of basis `(w,wA)` and `(z,zC)` gives the coefficient matrix

$$
Z^{-1}\begin{pmatrix}d&-1\\-1&0\end{pmatrix}.
$$

Consequently,

$$
\det H_f=-\frac{W^2V^2}{Z^2}
\operatorname{Cov}_{\mu_w}(u,A(u))
\operatorname{Cov}_{\mu_z}(v,C(v)).
$$

The minus sign is necessary and is correct. The identity

$$
\operatorname{Cov}(X,g(X))
=\tfrac12\mathbb E[(X-Y)(g(X)-g(Y))]
$$

shows that a derivative of fixed sign and magnitude at least `p_*/2` gives covariance of that sign and magnitude at least `(p_*/2) Var(X)`. The two action derivatives have opposite signs. The printed density lower/upper bounds give the claimed variance floor, and a uniform C^2 action bound permits one fixed small gate. No measured curvature or additional conditioning oracle is being smuggled into this step.

The conditioning is nevertheless not uniform as obliquity vanishes or the gate shrinks. A useful exact illustration, independently derived here, is the positive affine model on `[-R,R]^2`, with `d>2|p|R`:

$$
f(u,v)=\frac{d+pu-pv}{4R^2d},\qquad
\det H_f=\frac{p^2R^4}{9d^2}.
$$

Thus even this simple model loses the moment determinant at a fourth power of gate radius. The manuscript explicitly permits this deterioration. It would be wrong to reject the fixed-class theorem for failing to establish a uniformity that it expressly declines to claim.

At normal incidence an even quadratic model can have separation rank two while the first-moment matrix is singular. The source acknowledges this and retains the independent normal-incidence routes. Obliquity is a necessary hypothesis of this particular first-moment argument, not a newly discovered impossibility result for all normal-incidence observations.

**Finding:** the nondegeneracy proof is supported. Its geometric usefulness should be credited, but it is a short monotone-covariance argument under fixed-class hypotheses, not a general cure for ill-conditioned inverse problems.

### R74-M3. The compression is not injective on arbitrary finite densities

**Locations:** discussion after Corollary 10.3, p. 56; Proposition 10.4, pp. 56–57; S1 lines 147–241.

An independent negative control makes the issue particularly transparent. On `[-1,1]^2`, put

$$
f(u,v)=\frac{4+u/2-v/2}{16},\qquad q(x)=x^2-\frac13,
\qquad \widetilde f=f+\frac1{100}q(u)q(v).
$$

Both are positive normalized densities. Because `integral q = integral xq = 0`, they have exactly the same four profiles and the same H. Their common determinant is `1/576`, yet the first kernel has rank two and the perturbed kernel has rank three. The reconstructed expression from their common compressed data equals f, not the perturbed density.

**This is a generic kernel example, not a constructed pair of billiard tables and not a counterexample to Proposition 10.4.** Its purpose is to identify exactly why the physical finite-rank defect cannot be omitted.

The manuscript handles this distinction correctly. It first uses the differentiated relative estimate on the full gate to compare the two compressed finite records with their rank-two limits. It reconstructs those limits using their uniform determinant floor. It then compares the actual finite densities on the interior gate. The resulting error is

$$
C\{\Delta_M+e^{-\omega N}\},
$$

not `C Delta_M` alone. No exact finite-sample sufficiency claim follows. Nor are the weighted profiles replaceable by two ordinary unpaired marginal samples: M1 and N1 retain pair information.

The full-gate convention also survives this check. H and the integrated profiles use the same full normalization gate; restriction to the interior does not reset their mass. A mixture of normalizations would invalidate the identity, but that mixture is not used in the present source.

**Finding:** the finite comparison retains the indispensable defect term. The negative control strengthens the scope distinction; it does not create an unrepaired gap.

### R74-M4. The geometric and area stability interface uses the right data

**Location:** Proposition 10.4, pp. 56–57; S1 lines 194–241; `prop:v73-finite-record-stability`, S4 lines 222–273.

After recovering limiting densities in C^m, the source invokes the signed fixed-slice action inverse and the positive quadratic inverse. This recovers the offsets and curvatures before the C0 contact comparison. It does not infer second derivatives from a uniform graph error.

For each actual candidate the central identity is

$$
\mathcal A(T)=\frac{D_{N,b}(c)d_b}
 {2\pi\pi_{N,b}f_{N,b}(0,0)}.
$$

The reference stationary orbit has zero gauged action at the origin and the normalized twist is one there. The density and success probability refer to the same gate. These points, together with the prescribed Liouville preparation, are what make the formula exact.

Subtracting logarithms for two actual candidates produces the twist, offset, success-mass and central-density differences. The logarithmic twist comparison is

$$
|\log D_N(\widetilde c)-\log D_N(c)|
\le C(1+N)\|\widetilde c-c\|.
$$

For returning length `N=nP`, differentiating the transfer expression gives

$$
\nabla\log D_{nP,b}
=(\coth\chi-n\coth(n\chi))\nabla\chi
-\nabla\log(\mathcal M_b)_{12}.
$$

This explains the retained flight factor. It cannot simply be erased from this comparison on paths with nonzero derivative of chi. It is not, by itself, a minimax lower bound for all estimators.

The resulting estimate `C(1+N)(Delta_M+exp(-omega N))+Delta_pi` is supported. The finite central density belongs to the fitted actual table; it is not silently replaced in the exact area identity by the rank-two reconstructed surrogate.

**Finding:** the new compression does not break the curvature-to-area dependency. The area output remains one scalar of the full normalization, not a recovery of previously unvisited boundary arcs.

## 5. Examination of the statistical statements

### R74-M5. The one-dimensional derivative estimate has the stated powers

**Location:** Lemma 10.5, pp. 57–58; S1 lines 243–345.

For a derivative of order k of a weighted kernel profile, a summand has envelope of order `h^(-k-1)` and variance of order `h^(-2k-1)`. The second exponent includes one factor h from integration in the smoothed coordinate; the bounded paired-coordinate weight costs no further smoothing dimension. Taylor cancellation yields bias `h^s` on the protected interior interval.

The grid mesh `n^(-2) h^(m+2)` is adequate because the empirical derivative and its expectation have Lipschitz constants bounded by `C h^(-m-2)`. Under `h>=1/n`, the number of grid points is polynomial in n. Bernstein's inequality and a union bound over coordinates, derivative orders and phases therefore give

$$
h^s+\sqrt{\frac{L_n}{nh^{2m+1}}}
+\frac{L_n}{nh^{m+1}}+n^{-2}.
$$

The moment-matrix entries are averages of bounded variables and their errors are absorbed by this bound. The four profiles can be correlated; their independence is neither available nor required.

A coordinate perturbation bounded by delta changes the kth derivative summand by at most `C delta (h^(-k-2)+h^(-k-1))`. This yields the additional `delta h^(-m-2)` term uniformly over the sample. It permits sample-dependent readout errors because the comparison is deterministic after the latent sample is fixed. It does not permit noisy acceptance or corrupted success tags.

**Finding:** the one-dimensional powers, grid argument, paired weights and adversarial post-acceptance perturbation bound are internally consistent. Merely importing the old two-dimensional exponent would have been incorrect; the new source actually proves the changed estimate.

### R74-M6. The estimator is measurable and physically compatible, but nonconstructive

**Location:** S1 lines 348–375; Theorem 10.6, pp. 58–59.

The fitted image is the finite compressed record of actual pairs `(T,d)`, augmented by one log success probability. The ambient finite C^m product is separable. A countable dense subset of this image, with one actual representative for every selected point, suffices for the first-within-`n^(-2)` near-minimum construction. Neither closedness nor compactness of the image is needed.

The estimator consequently returns an actual table and offsets from the stipulated class. Its area is the area of that same table. An arbitrary signed kernel estimate or an arbitrary separated density is never declared physically realizable.

The first n successes can be analyzed using the Bernoulli/conditional-mark representation of independent preparations. Extending the latent success sequence for purposes of a probability bound avoids falsely conditioning it on a finite count event. The actual estimator uses only observed marks when every count is sufficient. A common union bound handles the count and smoothing events without independence between those errors.

The fallback on a fixed actual pair makes the definition total under the design conditions. The source expressly does not provide an effective enumeration of the image or a polynomial-time reconstruction algorithm. That limits computational interpretation but is not a defect in the stated statistical existence theorem.

**Finding:** the realizability and measurability issues are handled correctly at the claimed level.

### R74-M7. The rate improvement is real as an upper-bound comparison, not an optimality theorem

**Locations:** Theorem 10.6 and Corollary 10.7, pp. 59–60; S1 lines 378–487.

Balancing the bias against the variance and readout terms gives

$$
\alpha_1=\frac{s}{2(m+s)+1},\qquad
\gamma_1=\frac{s}{m+s+2}.
$$

The printed maximum bandwidth controls both sources simultaneously. The Bernstein envelope exponent is `(m+2s)/(2(m+s)+1)`, at least alpha1. Since alpha1 is less than one half and n is comparable to `Bq_N`, the relative count error is absorbed. The two exceptional events account for the stated probability `1-2 zeta`.

The physical bias is added at the comparison between actual candidates, rather than being charged twice inside the empirical estimator. For `q_N=c0 exp(-Gamma N)`, balancing the flight bias and charged sampling error yields

$$
\beta_1=\frac{\alpha_1\omega}{\omega+\alpha_1\Gamma}.
$$

The floor in the returning-length rule changes constants only. With

$$
t=(L_B/B)^{\beta_1}+\delta^{\gamma_1},
$$

the local bound is `Ct` and the joint local/area bound is `Ct log(e/t)`, subject to the explicitly retained count, small-error, bandwidth and returning-length conditions. Every one of the rB preparations is charged, including failures; the area uses an existing phase count rather than a free extra experiment.

For fixed m, s and the same physical class constants, the exponents strictly improve the preceding two-dimensional sufficient bounds. The improvement does not establish a sharp resolution threshold, a lower bound, or superiority over a different observation model. It also does not make the constants uniform as weak hyperbolicity forces the required inverse order m upward. The source is careful about these distinctions.

**Finding:** the displayed balances are supported. The useful dimensional reduction should not be inflated into a new general statistical optimality principle.

## 6. Re-examination of the inherited geometric mechanism

The new matrix result would be of little geometric value if its inherited action-to-contact passage were merely formal. I therefore checked the following interfaces rather than treating prior review conclusions as a proof.

First, the physical relative limit is based on the positive periodic Jacobi operator and an exact cofactor/transfer normalization. The argument compares the endpoint-localized perturbations of the determinant, controls interaction between the two ends through exponentially decaying Green entries, and then performs the exact time-split phase-volume calculation. Its logical direction is not “prove an absolute error and divide by an exponentially small success probability.” The signed coordinate conversion and the same central normalization remain necessary. [S6]

Second, the single-law inverse removes the unknown offset through the marked nonzero derivatives. The cross ratio has the form `R_f=1-U V`, and its mixed derivative at the origin is `p^2/d^2`. Fixed nonzero slices then identify U and V without spending one additional derivative at every inverse order. The corrected finite clock includes both the reference twist and the mixed logarithmic amplitude contribution; the latter has no asserted sign. [S5]

Third, positivity of the quadratic coefficients is used for a global curvature inverse, rather than concluding global injectivity from a nonsingular derivative. Signed cyclic finite-jet inversion then aligns lower jets. The actual smooth step still requires more than all Taylor coefficients: flat functions would otherwise remain invisible. [S7, S8]

The crucial functional estimate is supplied by the stationary envelope over actual later visits. After fixing a positive bounded class, the one-step contraction is made uniform with constant one. On differences flat to order m, the later-visit operator satisfies the sufficient bound

$$
\|\bar\alpha^{-1}K\|\le\frac{6a^m}{1-a^m}<1.
$$

Polynomial alignment handles the nonflat lower jets before this estimate is used for stability. The graph regularity and enlarged positive quadratic class are stated; the required m is class dependent. This is a genuine argument on actual smooth functions, not the invalid inference that equality of all jets forces equality of smooth germs. [S9]

Finally, the locality result has an actual converse on sufficiently small common collars. Equal local graphs and area give equal success submeasures and the same failure atom. Remote disjoint bumps with an exactly compensating area adjustment realize nonconstant completions with the same record. Hence the complete invariant consists of the contact germs, the fixed offsets and free area. Its word “complete” is relative to this experiment; it is not whole-table smooth rigidity. [S4, S10]

**Assessment:** I find no new fatal contradiction in these examined interfaces. This is the strongest part of the mathematical case. It is more substantial than the rank-two cancellation and should carry the significance argument. The present review does not promote this assessment into certification of the separate analytic/global branches.

## 7. Why the top-four recommendation remains negative

### R74-E1. The new theorem is a refinement of the existing mechanism, not a new principal rigidity mechanism

The four profiles reconstruct the same limiting law already used by the one-law theorem. The counts recover the same free-area scalar already identified in v73. The actual smooth inverse is unchanged. The new statistical theorem uses the same record and returns the same invariant, with improved sufficient powers because the smoothing dimension is lower.

This is worthwhile mathematics. It does not, by itself, provide a persuasive new reason to treat the paper as an exceptional general-journal contribution. The matrix identity, covariance sign and kernel calculation are not comparable in depth to establishing the relative physical law or the flat-sensitive geometric inverse. Giving each an additional headline should not obscure that hierarchy.

### R74-E2. The demonstrated comparison with the literature is accurate but does not establish exceptional reach

The corrected planar Noakes–Stoyanov result concerns global determination of finite strictly convex obstacle unions from exterior travelling-time or scattering-length data. Its supplied information and target are different from internally marked periodic reset experiments. [L2]

The analytic open-billiard result of De Simoi–Kaloshin–Leguil and the enriched marked-length Sinai result of Finamore–Leguil likewise use different data and hypotheses. [L3, L4] The present source appropriately declines to claim same-data dominance, removal of their assumptions within their problems, or equality with an exterior scattering relation.

Therefore the literature discussion no longer contains the earlier simplistic contrast “smooth rigidity here versus only analytic rigidity elsewhere.” That correction is welcome. It also means that broad global-rigidity language cannot carry the significance case. The case must be made for this particular singular-scale, richly marked, local experiment and its analytic mechanism. In my judgment, the manuscript has not yet made that case strongly enough for the requested venue.

This is not a claim that the theorem is already in the literature. The search was targeted, not an exhaustive priority certification. Nor is it a demand that the author solve an unmarked, single-trajectory or whole-boundary problem as a repair of the present theorem.

### R74-E3. The principal article remains larger than its central mathematical narrative justifies

The mechanism-first opening is an improvement and the central route is identifiable. Nevertheless, the 190-page principal entry continues through several separate inverse observations and then retains broader introductory formulations in its appendices; the full entry extends to 365 pages. The introductory hierarchy now has successive smooth, finite-preparation, single-law, complete-invariant and first-moment formulations, several of which are nested consequences of the same chain.

There is no universal page ceiling, and length is not a mathematical counterexample. The issue is the ratio of genuinely independent conceptual advances to repeated formulations, specialized consequences and retained historical routes. Preservation of every proof file is valuable for the repository, but preservation is not itself an argument that every route belongs in the principal journal narrative.

For editorial reconsideration, the principal statement should distinguish the irreducible geometric mechanism from its observation refinements and derived estimation bounds. The remaining formulations should have an explicitly justified role. This does not require deleting research from the repository, weakening a theorem, or concealing a proof in an unavailable supplement. It requires a coherent article rather than treating the accumulated revision history as the article's architecture. [S3, S11]

## 8. Concrete comments and their severity

**R74-P1 — minor, definite correction.** The organization paragraph in `article/00i_main_thesis_v70.tex`, beginning at source line 382, describes the central route through the complete-record section and then moves to subsequent parts. It omits the new Section 10. Add the moment reconstruction, finite-rank defect and charged one-dimensional estimate to that roadmap. This is a navigation defect, not a theorem gap.

**R74-P2 — optional quantitative clarification.** The affine determinant calculation in R74-M2, or an equivalent explicit example, would make the fixed-gate conditioning restriction immediately visible to a reader of the overview. The source already acknowledges the restriction, so this is not a missing hypothesis or a prerequisite to correctness.

**R74-P3 — editorial requirement for reconsideration, not a proof obligation.** Supply a sharply delimited significance account that identifies what is nonstandard in the relative physical comparison and actual smooth inverse, separates those steps from the classical matrix/statistical machinery, and explains the necessity of each principal part. A longer list of corollaries or more provenance checks will not answer this objection. This requirement does not predetermine which further research result, if any, should be pursued.

I do **not** require, as repairs of the stated theorems, exact finite-sample sufficiency of the four profiles, an unpaired-marginal experiment, noisy success tags, unknown reset measures, efficient enumeration, minimax optimality, unmarked recovery, uniformity at normal incidence, or determination of remote smooth boundary arcs. Those are different claims. The author should not turn this report into an artificial checklist of such new problems.

## 9. Independent diagnostic record and reproducibility

`independent_checks.py` was written for this review and executed normally and with `python -O`, using explicit exceptions rather than assertions that optimization would remove. The retained outputs are `checks-normal.json` and `checks-optimized.json`. Both report success.

The checks cover a nonsymmetric exact reconstruction with a failing transpose control; four positive weighted polynomial models with both obliquity signs; the exact covariance determinant; a positive rank-three density invisible to the compression; a normal-incidence rank-two example with singular first moments; the affine gate-conditioning formula; and thirty integer `(m,s)` pairs checking the sample, readout, count and budget balances. The generic polynomial models are not represented as realized billiard tables. The proof of the uniform statistical estimate is the analytic argument discussed above, not the finite grid of exponent tests.

The optional provenance mode verifies the source files, archive modes and reconstructed Git tree and computes the native object hashes. Run from this directory:

```sh
python independent_checks.py
python -O independent_checks.py
python independent_checks.py --native-dir /path/to/extracted/a2-v74-native-artifact
```

The script requires SymPy; the recorded environment used version 1.14.0. It performs no network access or repository writes. Successful diagnostics, native compilation and mathematical significance are three different kinds of evidence. None is converted into either of the other two.

## 10. Sources and locators

All S-locators below refer to the immutable source commit `c52fa361108a0f716d9e89017cd97eea71b0f3da` under `papers/A2-v17-boundary-information-coarsening/`. PDF page numbers refer to the retrieved 190-page principal entry, not the differently paginated full entry.

- **S1:** `article/10i_moment_reconstruction_v74.tex`, complete; overview `article/00p_moment_overview_v74.tex`.
- **S2:** `RESPONSE_TO_REFEREE_V74.md`; `HISTORICAL_DERIVATION_AUDIT_V74.md`.
- **S3:** `article/00q_abstract_v74.tex`; `article/00i_main_thesis_v70.tex`; `rigidity.tex`.
- **S4:** `article/10h_complete_record_v73.tex`, complete, especially the area anchor, invariant, logarithmic twist and finite-record comparison.
- **S5:** `article/10g_uncalibrated_single_law_v72.tex`, complete.
- **S6:** `article/10a_periodic_itinerary_relative_v64.tex`, complete periodic-relative and physical-law route.
- **S7:** `article/10b_periodic_contact_inverse_v65.tex`, coordinate, actual-envelope and signed cyclic finite-jet portions; no new certification of its complete analytic continuation branch.
- **S8:** `article/10c_global_curvature_inverse_v66.tex`, global positive quadratic inverse through source line 215; later stopping material not fully recertified here.
- **S9:** `article/10d_smooth_contact_rigidity_v68.tex`, complete.
- **S10:** `article/10f_local_observation_comparison_v71.tex`, complete; `article/00k_lens_comparison_v71.tex`.
- **S11:** principal entry point `rigidity.tex`, its current introduction and the inspected principal/technical native entries.

**G1:** [Pinned compiled source](https://github.com/TrillionniumFoundation/theta-theory/tree/c52fa361108a0f716d9e89017cd97eea71b0f3da/papers/A2-v17-boundary-information-coarsening).  
**G2:** [Compiled source to source handoff comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/c52fa361108a0f716d9e89017cd97eea71b0f3da...5076a85439d8bb0f770b6c80e23b82ea2d27aa4b).  
**G3:** [Compiled source to native-products comparison](https://github.com/TrillionniumFoundation/theta-theory/compare/c52fa361108a0f716d9e89017cd97eea71b0f3da...c6f0c23625ff35fc695d26b0e4ad451bbcbf333d).  
**D1:** [Pinned native delivery](https://github.com/TrillionniumFoundation/theta-theory/tree/c6f0c23625ff35fc695d26b0e4ad451bbcbf333d/deliveries/a2-v74/c52fa361108a0f716d9e89017cd97eea71b0f3da); independently retrieved artifact and local checks described above.  
**R1:** [Preceding v73 referee report](https://github.com/TrillionniumFoundation/theta-theory/blob/9c69f03f97dea57e83061af96aeb9bfe4dcc80d3/reviews/a2-v73-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md).

Primary literature checked for this assessment:

**L1.** K. Hamm and L. Huang, *CUR Decompositions, Approximations, and Perturbations*, arXiv:1903.09698v2, especially the exact decomposition theorem in Section 4. [Primary manuscript](https://arxiv.org/abs/1903.09698v2).

**L2.** L. Noakes and L. Stoyanov, *Lens Rigidity in Scattering by Unions of Strictly Convex Bodies in R²*, SIAM Journal on Mathematical Analysis 52 (2020), 471–480; corrected planar argument, Theorem 1.1. [Primary manuscript](https://arxiv.org/abs/1803.02542v2).

**L3.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*. [Primary manuscript](https://arxiv.org/abs/1905.00890).

**L4.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*. [Primary manuscript](https://arxiv.org/abs/2510.18983).

## Final assessment

Revision 74 is not defeated by the elementary checks in this report. It makes a genuine, carefully delimited improvement in the extraction and estimation of an already identified local invariant. The proof preserves the physical rank defect, paired information, actual-table constraint and area sensitivity instead of hiding them.

**My recommendation nevertheless remains negative at the requested top-four level. The unresolved issue is the demonstrated depth, reach and editorial concentration of the combined contribution, not an invented fatal defect in the new matrix identity.** A response should address that judgment directly, while keeping the concrete minor correction and optional conditioning illustration separate from mathematical correctness. The present report imposes no hidden requirement to produce another theorem merely to continue the revision cycle.
