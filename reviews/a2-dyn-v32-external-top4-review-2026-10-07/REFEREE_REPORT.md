# External top-four referee report on A2-DYN revision 32

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v32-referee-response-2026-10-07`, `revision/a2-dyn-v32-referee-copy-2026-10-07`  
**Reviewed commit:** `f63fb5101c8bcf6202abf4468d703be6242923a1`  
**Reviewed repository tree:** `7bf5ae3cd839586b7ca9d207562f8de84749a389`  
**Frozen ordinary paper tree:** `d6462c94e0cb7a702bf4e46e60da0440fb94a5ac`  
**Active manuscript directory:** `papers/A2-DYN-v32-referee-response`  
**Active core tree:** `6695f231cf81c14f1c309b9bcc8aa08fe99d19be`  
**Reviewed v31 author baseline:** `c0b184a89ff3d38675d0bc90a9e60b584476e5c3`  
**Baseline ordinary paper tree:** `06d63ae32efec644d907a0d3d0118c54b8e74c4c`  
**Controlling report:** `reviews/a2-dyn-v31-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `ea8b02f156b1d99633443103ae5e88eb96a89fce` / `068e7f72d813f9ce2a558fb237af624d5cca90af`  
**Date:** 7 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards-specialist report.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 32 is a genuine and useful mathematical advance. It responds directly to several audit requests in the revision-31 report. In particular, it now places the collision-coordinate differential, determinant and exact action identity in one proof; gives an explicit finite candidate set and a complete first-hit transition guard; formalizes the earliest-forbidden-time partition and zero extension used in the source integrations by parts; extends the positive geometric extraction to the true roof-biased stationary entrance law; and constructs a positive compact-Fourier-support approximation of the full mixed law. The latter produces a finite-band likelihood on the original trajectory space and controls it uniformly against every bounded measurable trajectory statistic.

I found no decisive counterexample in the two new mathematical modules

- `core/65_source_geometry_and_stationary_extraction.tex`;
- `core/66_positive_microscopic_conditioning.tex`;

or in the declared revisions to the geometric extraction. The kernel normalization, interpolation estimate, total-variation approximation, interval-boundary estimate, posterior normalization and long-time exponent bookkeeping are mutually consistent. The stationary extension uses the actual entrance density proportional to the first-return roof rather than replacing it by the unbiased section law or by a bounded current-collision marginal.

The new result is nevertheless a **positive reconstruction theorem**, not the advertised raw mixed-density local limit theorem. The finite-band density is close to the true law in global mixed `L^1`, and the likelihood is close to a microscopic event indicator in source total variation. Neither statement evaluates the finite Fourier integral. Neither supplies a local essential-supremum estimate for the raw density. Neither proves the microscopic Gaussian denominator. The pointwise common signed correction, the complementary-frequency integral and the relative replacement of the original microscopic physical-time event remain open at the same scale.

This distinction is decisive. The required bandwidth may satisfy

```text
log B_n = O(n log n),
```

so the band itself may be as large as `exp(O(n log n))`. The inherited spectral estimates cover specified central, annular, compact, peripheral and anisotropic regions, but the manuscript does not prove that they cover and control the complete finite integral up to this bandwidth with the local norm required for the raw theorem. Positivity of the reconstruction does not create the missing Gaussian asymptotic.

At the requested benchmark, a robust approximation architecture cannot substitute for the principal local theorem when the remaining complement and pointwise correction contain the main Fourier-analytic difficulty. Revision 32 narrows and clarifies the gap, but does not close it.

## 2. Frozen source and revision chronology

The two named revision-32 branches resolve to the same commit,

`f63fb5101c8bcf6202abf4468d703be6242923a1`.

The full repository tree at that commit is

`7bf5ae3cd839586b7ca9d207562f8de84749a389`,

and the ordinary manuscript tree is

`d6462c94e0cb7a702bf4e46e60da0440fb94a5ac`.

The active core tree contains sixty-six numbered modules. Revision 32 retains the sixty-four-module revision-31 article and adds the two modules listed above. It also makes declared edits to the dependency guide and to the two geometric modules introduced in revision 31. The source manifest and edit ledger identify those changes explicitly.

The controlling report is the revision-31 report at commit

`ea8b02f156b1d99633443103ae5e88eb96a89fce`.

That report accepted the new all-itinerary derivative budget and singleton-lattice finite-band reduction as substantive progress, but identified six remaining obligations:

1. evaluate the actual finite complementary integral;
2. control the pointwise common signed correction;
3. prove a microscopic Gaussian denominator;
4. compare the original microscopic physical-time event with the return event at that denominator scale;
5. close the weighted class used by the downstream conditional theorem;
6. obtain an independent specialist audit of the new billiard geometry.

Revision 32 substantially strengthens items 5 and 6 at the level of formulation: it makes the geometric source argument more self-contained, and it removes regularity restrictions on a bounded selector in the finite-band event approximation. It does not complete items 1--4, and no independent human specialist review is supplied.

The present review branch starts directly from the reviewed author commit and adds this report only under

`reviews/a2-dyn-v32-external-top4-review-2026-10-07/`.

No manuscript source, author branch, prior report, workflow or unrelated repository path is intentionally modified.

## 3. Qualification evidence and verification boundary

The exact-source qualification runs for both reviewed branches completed successfully:

- response branch run: `37609061553`;
- referee-copy branch run: `37609089855`.

The validation protocol checks source hashes, inherited labels, declared edits, bibliography identity, normal and optimized diagnostic agreement, native TeX compilation and rendering of the new proof interval. The manuscript reports a 205-page build. These are meaningful provenance and reproducibility checks.

The new finite diagnostics check, among other things,

- the determinant of the collision matrix in invariant coordinates;
- the cubic-spline Fourier multiplier and its moments;
- the all-label interpolation arithmetic;
- finite weighted Fourier identities with oscillatory selectors;
- positivity and posterior normalization in model examples;
- a finite roof-bias model;
- the polynomial exponent margins in the chosen bandwidth.

They do not certify the continuum completeness of the first-hit guard, the global zero-extension argument, the all-itinerary source partition, the complementary Fourier estimates, the pointwise raw correction, or the microscopic LLT. The author-side validation correctly states this limitation.

## 4. Scope of this review

I have not attempted to re-prove every theorem in a 205-page, sixty-six-module article. The substantive audit concerns:

1. the two new revision-32 modules;
2. the revised interfaces in modules 54, 63 and 64;
3. the response letter, proof ledger, publication-status record and introductory Theorem W;
4. the relationship between positive finite-band reconstruction and the still-open raw local theorem;
5. source identity and the successful qualification runs.

The inherited Gaussian, covariance, phase-arithmetic, mesoscopic-window, stationary-conditioning and bridge results are treated as the qualified baseline of this revision. This report does not convert prior AI-assisted review into formal proof certification.

## 5. Collision differential and exact action

The new self-contained lemma writes, for one regular flight,

```text
DT_R = -[[ (v+c)/c',       v/(c c') ],
          [ v+c+c',         (v+c')/c ]],
```

where `v=tau_R/R`, `c=sqrt(1-p^2)` and `c'=sqrt(1-(p')^2)`. The manuscript derives the formula from the differentiated flight equation and reflection law, verifies determinant one in `(alpha,p)` coordinates, and obtains

```text
d tau_R = R p' d alpha' - R p d alpha.
```

The derivation is coherent. Substitution into the accumulated action gives

```text
partial_alpha L_m = R(p_m A_m-p),
partial_p     L_m = R p_m B_m,
```

and hence the exact transverse identity

```text
partial_alpha L_m-(A_m/B_m)partial_p L_m = -R p.
```

The positive-matrix argument bounding `A_m/B_m` then yields a source vector field `X_m` with `X_m L_m=1` outside the initial normal strip. I found no sign or determinant inconsistency in this chain.

This consolidation materially improves the paper. It also makes clear that the construction is special to the physical collision geometry and its exact action identity; it is not an abstract consequence of a generic transfer-operator theorem.

## 6. Complete first-hit guard and chart uniformity

The candidate set is now explicitly defined by the uniform horizon and the triangular lattice. The manuscript argues that every next collision center lies in this finite set. For a candidate disk it writes the entry discriminant, observes that a positive entry root cannot cross zero while the discriminant stays positive, and uses disjointness of closed disks to exclude a tie of two distinct positive entry roots. Therefore a change of first-hit label must pass through a candidate tangency.

This is the correct geometric mechanism. Including **all** candidate discriminants, not only the currently selected disk, is essential because the selected branch may disappear on one side of a tangency.

The four bounded half-angle charts give a discriminant numerator of degree at most eight and a positive denominator in `[1,16]`. The numerator is not identically zero, and continuity over the compact radius interval plus finiteness of the chart/candidate family gives a positive uniform coefficient minimum. This supplies the input for the polynomial sublevel estimate with exponent `1/16`.

I found this argument plausible and internally coherent. It remains one of the parts that most needs an independent billiards specialist. In particular, a human audit should verify the exact candidate radius margin, the coverage at chart overlaps and angular endpoints, the treatment of the outgoing initial disk, and the assertion that no first-hit transition escapes the discriminant list. The present finite scripts cannot establish those continuum statements.

## 7. Source partition and zero extension

The revised text indexes the first forbidden collision or first changing section decision. All earlier branches remain regular on a neighborhood. At the earliest bad input, a guard factor is identically zero on a two-sided neighborhood. Later, possibly undefined iterates are not differentiated; the whole product is defined as zero there. This is the right response to the previous concern that a one-sided branch derivative might be extended through a singularity and create a hidden boundary distribution.

The source is partitioned, modulo null sets, by finite center itinerary, section decisions, mark collision indices, output label and actual physical collision count. The pieces have disjoint interiors. The flat guard endpoints and the initial normal cutoff give the regularity needed for two integrations by parts. Consequently the absolute source integrals sum over the initial cylinder rather than over a symbolic multiplicity of words.

Within the stated finite-cutoff setting, I found this logic coherent. The measure-theoretic partition and zero-extension assertions are still load-bearing and merit an independent specialist check, especially near multiple singularities and simultaneous section/tangency boundaries. No fatal defect was identified in the written construction.

## 8. Stationary entrance-bias extraction

The equilibrium return suspension is written as

```text
d P_R^eq = (c_*/bar_tau_R) d nu_R^*(y) ds,
0 <= s < tau_R^*(y).
```

After integrating out the age variable, the entrance point has density

```text
rho_R = c_* tau_R^*/bar_tau_R
```

with respect to the section probability. This is the correct length bias. The manuscript does not replace it by the unbiased section law.

Using the uniform exponential moment of one return block, the text obtains a uniform `L^2` bound on `rho_R`. Cauchy--Schwarz then changes the section-law removal estimates into

```text
delta_eq <= C [ exp((a n-c L)/2)
                +(L+1)^(1/2) epsilon^(1/32) ].
```

On each retained source piece, the first-return roof is a finite collision sum, so multiplication by `rho_R` preserves the exponential derivative budget after changing constants. The same source integrations by parts yield an all-label `W^{2,1}` bound.

The loss from exponents `1/16` to `1/32` and from the full exponential tail to its square root is exactly what Cauchy--Schwarz predicts. I found the normalization and exponent bookkeeping correct.

The scope must remain explicit: the reconstructed record starts at the actual preceding section point `y`. Keeping the elapsed age `s` allows arbitrary statistics of the same stationary trajectory, but it does not identify this return record event with the original microscopic event measured at a deterministic physical endpoint.

## 9. Positive band-limited kernel

The kernel

```text
k(t) = (3/(8 pi)) [sin(t/4)/(t/4)]^4
```

is even, nonnegative and integrable. With the manuscript's Fourier convention its transform is the compactly supported cubic spline

```text
eta(b) = 1-6b^2+6|b|^3,    |b| <= 1/2,
         2(1-|b|)^3,       1/2 <= |b| <= 1,
         0,                |b| >= 1.
```

The stated mass one, zero signed first moment and second moment twelve are consistent with this formula. The dilation `k_B` therefore has Fourier support `[-B,B]` and second moment `12/B^2`.

For compactly supported components `q_ell in W^{2,1}`, the manuscript proves

```text
A_1 <= 2 sqrt(A_0 A_2),
sum_ell ||q_ell||_infinity <= A_1/2,
sum_ell ||q_ell-k_B*q_ell||_1 <= 6 A_2/B^2.
```

The first inequality follows from a translation/Taylor estimate optimized in the scale parameter; the second from integrating each derivative from both ends; the third from the vanishing first moment and the second-order Taylor remainder. The constants are consistent.

These are useful harmonic-analysis estimates, but they are approximate-identity estimates. They do not provide decay of the billiard characteristic function inside the support of `eta(b/B)`.

## 10. Positive approximation of the full mixed law

Write the true law as `mu=Q+E`, where `Q` is the positive regular submeasure and `E` is the positive discarded measure of mass `delta`. The finite-band density is exactly the roof convolution `k_B*mu`, with no convolution in the three lattice coordinates. Hence it is nonnegative, has total mass one and preserves the lattice marginal.

The estimate

```text
||mu-k_B*mu||_TV <= 2 delta+6 A_2/B^2
```

is correct: convolution is a contraction, `||E-k_B*E||` is at most `2delta`, and the regular part is controlled by the second-derivative budget.

This is a genuine strengthening over the sharp finite integral of revision 31. It supplies a positive global mixed-`L^1` approximation rather than only an interval identity. It also demonstrates that the small discarded measure causes no factor of `B` or `log B` in this global approximation.

The limitation is equally important. Global `L^1` convergence at an arbitrarily fast polynomial rate does not imply a small essential-supremum error on a prescribed microscopic central window. A density can have very small mass and arbitrarily large height. The manuscript explicitly retains this negative control and does not claim otherwise.

## 11. Event likelihoods and arbitrary bounded selectors

For an interval-fibre event `A`, the manuscript defines

```text
lambda_{A,B}=(k_B*1_{A_L})(T),
```

on the original probability space. It lies in `[0,1]`. The translation identity

```text
int |1_I(t)-1_I(t-y)| dt <= 2 J |y|
```

for a union of at most `J` intervals, combined with the all-label supremum bound, gives

```text
||1_A-lambda_{A,B}||_1
 <= delta+2 kappa_1 J sqrt(A_2)/B.
```

This calculation is sound. It is independent of the interval length, permits singleton lattice fibres, and sums over labels without introducing the number of occupied fibres.

Multiplying the pointwise error by an arbitrary bounded measurable trajectory statistic `W` yields

```text
|E[W 1_A]-E[W lambda_{A,B}]|
 <= ||W||_infinity E_B(J).
```

This is an exact source-total-variation statement. It correctly avoids differentiating `W`, treating `W` as an anisotropic multiplier, or assuming that `W` depends on finitely many returns. In that precise sense, revision 32 closes the bounded-selector restriction **at the finite-band reconstruction stage**.

It does not close the weighted Gaussian problem. The finite Fourier representation contains

```text
E[W exp(i(u.L+bT))]
```

throughout the entire band. For an arbitrary path selector, the manuscript supplies no uniform spectral estimate or Gaussian evaluation of this weighted transform. The theorem transfers the selector into a positive finite-band formula; it does not estimate that formula.

## 12. Posterior normalization and denominator sensitivity

The posterior comparison follows from the unnormalized total-variation bound and the elementary normalization inequality. If the true denominator `p_A` exceeds the absolute error, then

```text
||P(.|A)-Pi_{A,B}||_TV <= 2 E_B(J)/p_A.
```

Alternatively, an evaluated finite-band denominator satisfying `p_{A,B}>E_B(J)` gives the lower bound `p_A>=p_{A,B}-E_B(J)>0` and the corresponding posterior estimate. The same contraction works after intersecting with another measurable selector or multiplying by a nonnegative path weight bounded by one.

These are correct denominator-sensitive statements. They are not unconditional microscopic conditioning theorems. For an event whose probability is comparable to or smaller than the absolute reconstruction error, the estimate is vacuous. For a rare selected event, its own denominator must be established. The result therefore supplies an a posteriori positivity test, not the missing Gaussian lower bound.

A future presentation should distinguish consistently between:

- an absolute approximation of an unnormalized measure;
- a relative approximation after division by a proved denominator;
- a Gaussian asymptotic for that denominator.

Only the first and the conditional implication to the second are proved here at the original microscopic scale.

## 13. Long-time parameter choices and the size of the band

The manuscript chooses

```text
L_n = ceil(lambda n),
epsilon_n = epsilon_0 n^{-d},
A_n = 1+C exp(C(L_n+1) log(C/epsilon_n)),
B_n = n^(P+kappa+4) sqrt(A_n).
```

With `lambda` above the cumulative-tail slope and `d>32(P+5)`, the stationary discarded mass is `O(n^{-P-4})`. The two positive-kernel errors are then also `O(n^{-P-4})`, even after allowing `J=O(n^kappa)`. Multiplication by `n^2` leaves arbitrary inverse-polynomial accuracy. The algebra is consistent.

Because `L_n=O(n)` and `log(1/epsilon_n)=O(log n)`, one obtains

```text
log B_n=O(n log n).
```

This must not be read as `B_n=O(n log n)`. The band can be super-exponentially large on the scale of the earlier polynomial frequency windows. The positive-kernel approximation is able to use such a band because it is an identity plus a derivative budget; the inherited dynamical spectral theory is not thereby extended to every frequency below `B_n`.

This is where reconstruction and asymptotic evaluation separate. The manuscript can approximate the law by a band-limited density without possessing a usable dynamical estimate at every frequency in that band. To derive the raw LLT, it must evaluate or cancel the remaining finite complement in the local norm, not merely make the band finite.

## 14. The pointwise common correction remains open

The exact raw ledger inherited from revision 31 contains, schematically,

```text
common correction
 = discarded density
   - convolution of discarded measure
   + finite complementary inverse of the regular residual
   + far-roof inverse.
```

The far-roof inverse is controlled by the all-label second-derivative budget. The convolution of the discarded measure is controlled by its total variation and the chosen kernel. The positive reconstruction also controls the full difference globally in `L^1`.

The two decisive local terms remain uncontrolled:

1. the discarded density can have small `L^1` mass and large pointwise height;
2. the finite complementary inverse has not been bounded across every remaining frequency regime with constants compatible with the chosen cutoffs.

The manuscript accurately records that these terms may require signed cancellation. A theorem exploiting their cancellation would be acceptable; separate absolute bounds are not logically necessary. What is necessary is a local estimate strong enough to enter the raw inversion theorem. No such estimate is proved in revision 32.

## 15. Status relative to the revision-31 report

| Obligation from revision 31 | Revision-32 status |
|---|---|
| Self-contained collision differential and action | **Closed in presentation and proof.** The formulas, determinant and action identity now occur in one lemma. |
| Complete first-hit guard and zero-extension audit | **Substantially strengthened.** The candidate set, chart bounds and earliest-forbidden-time partition are explicit; independent specialist verification is still absent. |
| Stationary positive extraction with the true entrance law | **Closed for the preceding-section record.** The roof bias and elapsed age are retained. |
| Positive global approximation of the full mixed law | **Closed.** A finite-band density approximates the law in global mixed `L^1` and preserves all lattice coordinates. |
| Arbitrary bounded-selector reconstruction | **Closed at the absolute finite-band stage.** No regularity of the selector is used. |
| Complete finite complementary Fourier integral | **Open.** The finite integral is represented but not evaluated throughout the band. |
| Pointwise common signed correction | **Open.** Global `L^1` does not give the required local essential-supremum bound. |
| Microscopic Gaussian denominator | **Open.** Positivity and an a posteriori test are not a Gaussian asymptotic. |
| Relative original physical-event replacement | **Open.** The stationary record begins at the preceding section origin. |
| Gaussian evaluation for arbitrary path selectors | **Open.** The selector remains inside an unevaluated weighted transform. |
| Independent billiards-specialist audit | **Open.** The text is more auditable, but no independent human review is supplied. |

This table should remain visible in any subsequent revision. It prevents the number of completed approximation modules from obscuring the exact endpoint status.

## 16. Significance at the requested benchmark

The combined revision-31/32 geometric mechanism is elegant. A single source-space transverse direction, all-candidate guards, disjoint-source integration by parts and positive band-limited reconstruction form a potentially reusable regularization package for marked dispersing-billiard records. The arbitrary-selector contraction is also a clean way to avoid demanding impossible regularity from a downstream path functional.

In the current paper, however, these results are still organized as infrastructure for a triangular-family raw LLT. The positive kernel and interpolation arguments are classical harmonic analysis once the geometric `W^{2,1}` submeasure is available. Their main value is to turn the geometric extraction into a positive reconstruction and conditional-measure reduction. They do not constitute a replacement theorem of breadth comparable to the missing local limit.

The article contains several collections of unconditional results that could support strong specialist papers: uniform Gaussian and functional laws, phase arithmetic and nondegeneracy, mesoscopic stationary conditioning and Gaussian bridges, all-itinerary geometric regularization, and positive microscopic reconstruction. A carefully reorganized specialist submission could be compelling after expert verification.

At the four-journal benchmark requested here, the central raw theorem remains the natural measure of closure because it governs the title, abstract, theorem architecture and final physical-conditioning program. The remaining finite complement and pointwise correction are not routine polishing. They are the core local inversion problem.

## 17. Required mathematical changes before a future top-four resubmission

A future top-four submission should not return until the following chain is proved.

1. **Evaluate or eliminate the finite complement.** Establish estimates for the full prescribed-return transform throughout every frequency region left inside the actual reconstruction band, with constants compatible with the geometric cutoffs. A direct signed-cancellation theorem for the complete raw ledger would also suffice.

2. **Prove the local pointwise correction bound.** Obtain the central-window essential-supremum estimate required by the raw inversion theorem, or replace it with a rigorously equivalent local norm that yields the same density conclusion. Global total variation is not enough.

3. **Derive the microscopic Gaussian denominator.** At singleton lattice coordinates and bounded or shrinking roof intervals, prove the Gaussian main term and a uniform relative error. Positivity of a mollified likelihood is not the needed asymptotic.

4. **Transfer to the original microscopic physical-time event.** Under the actual stationary law, prove a relative symmetric-difference, coupling or equivalent comparison at the denominator scale of item 3. Retaining the age variable does not by itself identify the events.

5. **Evaluate the weighted formula for the downstream selector class.** The arbitrary-selector source-TV estimate is valuable, but a final conditional path theorem needs the weighted finite integral or another joint local theorem to be evaluated, together with a positive selected denominator.

6. **Obtain an independent specialist audit.** A billiards expert should check the candidate-center completeness, coordinate differential, simultaneous singularities, chart compactness, zero extensions and all-itinerary source integrations by parts. A harmonic analyst/probabilist should independently check the raw inversion and denominator passage.

## 18. Presentation recommendations

The revision has already improved its dependency diagram and bandwidth language. I recommend the following additional changes.

1. State beside every microscopic result whether its error is absolute or relative and identify the denominator needed for normalization.
2. Repeat at the main theorem that `B_n` itself may be `exp(O(n log n))`; readers can otherwise mistake the logarithmic statement for a polynomial band.
3. Keep global mixed `L^1`, source total variation and local essential supremum in separate notation throughout. They solve different problems.
4. In the all-selector theorem, emphasize that uniformity in `W` is obtained by contraction after the unweighted event estimate, not by a uniform spectral theorem for weighted transforms.
5. Preserve the status table, but reduce repeated prose disclaimers elsewhere. The present architecture is accurate yet difficult to navigate.
6. Consider separating the unconditional Gaussian/bridge theory and the geometric-positive reconstruction into focused papers. A 205-page cumulative article makes independent verification unusually difficult.
7. Expand the literature comparison around the completed geometric regularization and positive reconstruction, while avoiding any implication that existing Lorentz-gas LLTs automatically supply the missing moving-section mixed-density theorem.

## 19. Verification limitations

The successful workflows and finite scripts establish source identity, reproducible compilation and the correctness of selected finite algebraic identities. They do not prove:

- completeness of the continuum first-hit transition list;
- regularity of every zero extension at intersecting singular sets;
- validity of the source integrations by parts on every billiard cell;
- the full finite complementary spectral estimate;
- a pointwise common raw correction;
- a microscopic Gaussian denominator;
- a relative microscopic physical-event comparison;
- a weighted microscopic Gaussian theorem for arbitrary path selectors;
- the full parameter-uniform raw mixed-density LLT.

No independent human specialist report is claimed by the manuscript or by this assessment.

## 20. Final assessment

Revision 32 should be credited as substantive progress. It turns the geometric residual of revision 31 into a positive, globally accurate mixed-law reconstruction; extends the construction to the true stationary entrance bias; and proves a clean source-total-variation approximation that is uniform against arbitrary bounded measurable selectors. The source-geometric proofs are also significantly more explicit and auditable.

These advances do not complete the theorem around which the paper is organized. The finite complement remains unevaluated, the pointwise common correction remains open, the microscopic Gaussian denominator is absent, and the return record has not yet been replaced by the original microscopic physical-time event at that scale. The posterior theorem is denominator-sensitive rather than an unconditional local limit theorem.

For these reasons, my recommendation at the requested four-journal benchmark remains:

**reject in the present form.**

A later assessment could change materially if the exact raw ledger is closed in the required local norm and the resulting microscopic Gaussian and physical-conditioning statements are proved for the original record and event class.