# Response to the external A2 v38 report

**Manuscript:** Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_.

**Controlling report:**
[`REFEREE_REPORT.md`](https://github.com/TrillionniumFoundation/theta-theory/blob/5dd7a7e346a9d31d7541efe791335d4e965cadb0/reviews/a2-v38-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md),
review commit `5dd7a7e346a9d31d7541efe791335d4e965cadb0`, report blob
`a36a7218e4f07f0f4bb6bf137e04cf608e804936`.

**Reviewed author source:** `a346669928e5147cf2c0ef86c3bc2a455b512d14`,
`papers/A2-v38-finite-field-rigidity`.

**Revised source:** `papers/A2-v39-response-rigidity`, on the new v39
author and referee-copy branches named in the README.

## 1. Substantive response

The report accepts the audited v37/v38 mathematical package and its
exact-source delivery. Its principal objections concern the strength
of the active datum, the relation between the apparatus settings, the
conceptual role of the collision experiment, and the organization of
the article. We have responded by proving a new joint inverse within
the same binary first-collision experiment and by making that inverse
the principal theorem of the article.

Sections 2 and 3 now treat **one unknown stationary launch law and
forward collision bits alone**. Directions and short positive lengths
are commanded. There are no cross-setting homothety relations, supplied
launch origins, supplied density values, or separately prescribed
reciprocal preparations in these statements. The exact theorem identifies
the entire launch density, as well as the footprint and obstacle table,
up to the common translation which the experiment necessarily preserves.
It also determines the full translation-period group and completes the
germ to all finite-length forward responses.

This result has a direct geometric proof. For the forward germ
\(q_\theta=\lim_{t\downarrow0}F_{t,\theta}/t\), the short-flight
boundary formula and the identity

\[
(({-\cos})_+)''+({-\cos})_+
=\delta_{\pi/2}+\delta_{-\pi/2}
\]

give a positive sum of spatially translated copies of the same unknown
density. Their support geometry, normalized mass and Steiner centers
identify the law and the boundary points. Angular inversion is classical;
the inverse uses the spatially resolved density copies left by that
operation. The proof of Theorem 2.3 recovers all boundaries directly
and does not invoke the stopped-Poisson occupation inverse.

Theorem 2.6 gives a broader exact statement. Inter-obstacle separation
greater than the footprint diameter, together with one obstacle whose
diameter exceeds that bound, suffices. A minimum-area angular support
component identifies the density even when antipodal copies from other
obstacles overlap. The odd part of the germ then supplies the
distributional gradient of occupation, from which all the remaining
obstacles follow by support cancellation. The identity and location of
the resolved obstacle are not supplied.

Theorem 3.3 supplies a finite acquisition theorem under quantitative
uniform separation and smoothness priors. It estimates regularized
angular responses using finite rational forward commands, explicitly
controls the short-flight, quadrature and displacement errors, and
charges all sampled centers and command occurrences. Corollary 3.4
gives the corresponding complete-aperture finite nonperiodic result.
Thus the finite theorem is proved separately from the exact differential
inverse.

The earlier claims and their proofs remain intact. The report's
successful v38 build and accepted inverse identities are not described
as defects repaired in this revision.

## 2. Report section 9.1: the exact datum

The abstract, Section 1 and Section 2 define the new exact input as
the family of raw forward means for every nominal center, every
commanded direction, and arbitrarily short positive lengths. The
limit is taken in \(L^1_{\mathrm{loc}}\). It is an active whole-field
datum with direction labels. It is not inferred from one fixed pooled
field and is not described as finite-dimensional information or a
passive trajectory invariant.

Lemma 2.1 derives the germ from the original bit, including the rule
that solid starts and misses return zero and remain in the denominator.
Lemma 2.2 constructs the angular derivative as a continuous
\(L^1_{\mathrm{loc}}\)-valued family. This specifies each angular slice
without evaluating an arbitrary distribution at a point.

Theorem 3.3 separately proves finite geometric acquisition. Its
regularization and sampling costs appear in the statement and proof;
the finite-stencil occupation theorem is not used to substitute a
finite oracle for the new directional germ.

**Locations:** `core/00h_single_law_overview.tex`,
`core/19_single_law_rigidity.tex`, `core/20_single_law_finite.tex`.

## 3. Report section 9.2: raw means and differences

The introduction and the comparison section distinguish the data
required by each inverse:

| Construction | Observed mean data | Result |
|---|---|---|
| New single-law inverse | Raw directional forward short-flight means \(F_{t,\theta}\) | Centered footprint, density and obstacles; complete fiber and periods |
| Retained stopped-Poisson inverse | Reciprocal differences \(g=F-R\) | Occupation and its components; exact obstacle periods |
| Retained width and perimeter deficits | Raw forward \(F\), together with recovered components | Homothety scales and support calibration |
| Retained area normalization | Reciprocal differences | Area-normalized homothety calibration |

The new angular differentiation uses direction-resolved raw forward
data. Neither the retained difference field nor an isotropically
pooled forward field is claimed to supply that datum. In the broader
Theorem 2.6, the difference between opposite **forward germs** is a
spatial occupation derivative. It is not an invocation of an
independently supplied reciprocal joint law.

**Locations:** Section 1; Section 5; Appendices A, F, G and H;
Theorem 2.6.

## 4. Report section 9.3: exact and finite periods

Corollary 2.5 and Theorem 2.6 identify the exact period group without
a periodicity prior. A germ period is equality in
\(L^1_{\mathrm{loc}}\) for every angle; the finite-length mean fields
have continuous representatives. The recovered configuration is
locally finite, nonempty and positively separated. Its discrete
translation group has rank two exactly when the configuration is a
finite-orbit planar crystal.

Theorem 3.3 retains the bounded periodic class
\(\mathcal B_\eta\) and a known positive nonperiod-patch margin.
Those assumptions make the finite primitive-data decision uniform.
The recovered geometry is expressed in the common translation gauge,
so the patch test is applied to the canonical table; the margin is
invariant under that change of frame.

Corollary 3.4 uses a different acquisition hypothesis: a finite
configuration with a bounded component count and a known protected
aperture containing every expanded component and its acquisition
collars. It requires neither periodicity nor a patch margin. These
results remain separate from a finite prior-free crystallinity test
for arbitrary infinite configurations, which the manuscript does
not assert.

**Locations:** Corollary 2.5, Theorems 2.6 and 3.3, Corollary 3.4,
and the retained period-recognition appendix.

## 5. Report section 9.4: the finite stencil and physical aperture

Appendix B retains the fixed-stencil occupation inverse, its
arbitrary-data stability and its primal-dual certificates. The
introduction explicitly identifies it as a pointwise estimator.
Its stencil radius is
\(K=\lceil(D+\Delta)/t\rceil\), so its number of sites depends on
the prior ratio \((D+\Delta)/t\). Independent target evaluations
incur the corresponding sum of attempted-bit and batch costs. Its
physical aperture needs the stated coarse footprint-location bound.

The new finite theorem makes its own acquisition count. Spatial
quadrature centers and direction-labelled occurrences are charged,
not just the target at which a scalar integral is estimated. With
\(s=6+\beta\), the sufficient total cost is

\[
N_\nu\le C\nu^{-Q_\gamma}\log\frac{C}{\nu\delta},
\qquad Q_\gamma=\frac{(3\gamma+27/2)s}{s-2},
\qquad S_\nu\le J_\nu\le N_\nu.
\]

The command length is of order
\(\nu^{(\gamma+5)s/(s-2)}\), and the coordinate mesh is of order
\(\nu^{(2\gamma+9)s/(s-2)}\). The total finite command description
is bounded by \(CJ_\nu\log(C/(\nu\delta))\) for computable fixed
priors and certified dyadic choices. Numerical construction is
separate from the observation count.

Periodicity permits a prior-bounded nominal aperture in the canonical
frame without knowing the common launch offset. Actual starts lie
in a translate of that aperture by the physical footprint, and the
flights in its short parallel body. A uniform absolute physical
aperture therefore additionally needs a coarse bound on the launch
offset. The theorem states this distinction explicitly; that bound
does not reveal or calibrate the origin.

**Locations:** Section 1; Theorem B.4; Theorem 3.3 and its aperture,
rounding and resource paragraphs.

## 6. Report section 9.5: the minimax comparator

Section 4 retains the complete upper and lower proofs and their
matching polynomial power

\[
q_0=\frac{3s/2+1}{s-2}.
\]

The introductory summary and Corollary 4.6 identify the comparator:
one fixed known uniform-disk launch law with radius in a fixed
positive range, a nondegenerate near-circle packing in the bounded
smooth class, the geometric loss including centered \(C^2\) support
error, fixed confidence, and worst-case expected attempted bits.
The lower bound already holds for the centered component loss.
The lower command class permits adaptive
short directions and lengths. The upper construction uses its stated
fixed pooled compass, with a deterministic attempt cap that also
bounds expected cost. The inequality between command classes has
the favorable direction required for the minimax bracket.

The upper and lower bounds still differ by one logarithmic factor.
The statement does not assert sharp confidence dependence. This
fixed-known-law theorem is not transferred to the new joint
unknown-footprint and unknown-density class. The new exponent
\(Q_\gamma\) is a sufficient finite acquisition bound for that
different experiment; its optimality is not claimed.

**Locations:** Section 1, Section 4, Corollary 4.6,
`core/16_sharp_stationary.tex`, `core/16a_shrinking_upper.tex`.

## 7. Report section 9.6: the apparatus relation

The principal exact and finite theorems now use one stationary
launch law. The source of additional identifiability is the
commanded directional short-flight response and its separated
spatial density copies. No second setting, exact homothety ratio,
cross-setting component correspondence or reciprocal preparation
enters their statements or proofs. This removes the cross-setting
apparatus relation from the new principal inverse itself.

Theorems 2.3 and 2.6 assume smooth strictly convex obstacle
boundaries of positive curvature and state their separation
conditions. The finite theorem additionally uses quantitative
curvature, regularity and boundary-mass priors and the stronger
uniform antipodal-copy gap. It does not claim a uniform finite
bound under only the single-resolved-obstacle exact hypothesis.
The finite acquisition uses known nominal command controls and
charges their prescribed precision and description.

The homothetic results remain complete in the appendices, with
their original strengths and assumptions: labelled settings,
exact positive homothety of supports, independent unknown origins,
unknown ratios and possibly different stationary densities.
Recovering origins and ratios in those theorems does not certify
the homothety relation. Manufacture, travel and physical metrology
remain separate from attempted-bit and digital-description counts.

**Locations:** Sections 2–3; Appendices D, F, G and H.

## 8. Report section 9.7: one principal theorem chain

The article now has a five-section body:

1. The collision experiment and the precise data and resource models.
2. The directional boundary measure, density-copy inverse, complete
   observational fiber, periods and the one-resolved-obstacle extension.
3. Finite forward reconstruction of the footprint and obstacle geometry.
4. The retained fixed-known-law stationary minimax benchmark.
5. The relationship to earlier inverse and geometric methods.

All earlier self-contained programmes are subordinate appendices
A–Q. They include global and finite-stencil occupation, stationary
queries, homothetic calibration and registration, isotropic commands,
earlier information estimates, retained statement collections,
localized reconstruction, finite controls, period locking and
physical packing. Their proofs remain available within the same
compiled primary. The proof-dependency map distinguishes the direct
exact inverse from auxiliary results used by the finite theorem.

This organization preserves the user's requested full mathematical
content. The source validator verifies that all 265 reviewed labels
remain active and all 66 reviewed proof bodies are byte-identical.
Ten new proved blocks bring the totals to 79 formal blocks and 76
proof environments. The article retains the title, billiard topic,
binary observation rule and all preceding quantitative claims.

## 9. Literature and proof evidence

Section 5 and the literature audit credit classical first variations
of convex sets, directional variation, planar cosine inversion,
support-function algebra and the earlier reconstruction methods.
The elementary angular identity is not presented as a new transform.
The present argument uses the positive spatial copies it exposes
to identify a common unknown launch density and the contact
locations, including their complete translation fiber.

The written proofs contain the continuum arguments. In particular,
they use supports of positive measures rather than a representative's
pointwise positivity set; identify densities almost everywhere;
justify \(L^1\) angular slices; normalize the occupation potential
distributionally; and derive finite quadrature and variance bounds
without a hidden density upper bound or continuity modulus.

The accompanying finite checks retain 608,298 v37/v38 checks and
add 14,678 checks for angular normalization, density-copy algebra,
translation, flux signs, weak errors, regularization, signed
estimators and the resource exponents. The qualification-contract
suite separately tests the delivery checks. Ordinary and optimized
executions must agree byte-for-byte. These checks and the native
LaTeX build are archived with the exact committed source and are
not substitutes for the continuum proofs.

The source and literature audits accompanying the v38 report remain
unaltered. The new workflow records the actual outcome at its
triggering commit and uploads the associated source, PDF, logs and
receipt for the next referee's independent examination.
