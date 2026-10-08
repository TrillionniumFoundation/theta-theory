# External top-four referee report on A2-DYN revision 45

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v45-referee-response-2026-10-08`, `revision/a2-dyn-v45-referee-copy-2026-10-08`  
**Reviewed commit:** `5ab781065787b1aca00ff5182a62da49f847d2e4`  
**Reviewed repository tree:** `980d613da10c6ed30d84646b4dc14b029f174669`  
**Ordinary source payload tree:** `696e8820d1a759f49a094b4e900b8699bc82b7a2`  
**Active manuscript directory:** `papers/A2-DYN-v45-referee-response`  
**Active mathematical source:** ninety-seven numbered core modules  
**New unreviewed mathematics since the latest external report:** modules 94--97; revision 44 added modules 94--95 and revision 45 adds modules 96--97  
**Immediate author baseline:** revision 44, commit `848582734b94a6cda2d27484be2d6dcf646744a4`  
**Latest controlling external report:** `reviews/a2-dyn-v43-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `0418466ec7a126b032e64cc8c54238770104cf68` / `6d223bd63ddd76a5a2efc3351c475d0261e93839`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revisions 44 and 45 contain genuine new mathematics and materially improve the raw-inversion analysis.

Revision 44 proves a radius-uniform exponential height bound for every complete fixed-collision-count roof density, including arbitrary bounded measurable restrictions of the actual return source. It then uses the complete-component constructible germs to separate finite jumps from continuous positive-exponent cusps. The continuous singular terms can be localized with unchanged intrinsic coefficients and an arbitrarily prescribed summed supremum budget. This removes the divergent-germ obstruction and pays the entire continuous cusp contribution at the central local scale.

Revision 45 addresses the jump part by a genuinely dynamical argument. It introduces a protected class of normal-to-normal critical words whose incidence, clearance, and section-decision margins may decay exponentially with distance from the two endpoints. For each fixed protection parameter it constructs an endpoint collar of word-length-independent size, proves relative source-density distortion in that collar, compares its positive mass to the intrinsic jump coefficient, and combines this with a two-normal-strip exact-index local upper bound. The result is deconcentration of all protected critical jump clusters, including exactly coalescing critical values, at the required `m^{-2}` scale. The original positive source in any shrinking protected collar is also pointwise `o(m^{-2})`, and its contribution to the signed smoothing correction is negligible uniformly over all roof bandwidths.

I audited the four new modules

- `core/94_complete_density_bounds.tex`;
- `core/95_jump_cusp_separation.tex`;
- `core/96_uniform_critical_collars.tex`;
- `core/97_critical_edge_deconcentration.tex`;

as well as their front-matter statements, response to the referee, proof ledger, critical-cluster input map, specialist audit map, source manifest, publication status, validation record, and exact-source workflow evidence.

Within the scope of this audit, I found no decisive counterexample, normalization error, collision/return-label mismatch, missing factor of the section mass, incorrect power of the collar width, false use of a shrinking-band local limit, or illicit replacement of the arithmetic transition kernel by an unmodulated Gaussian.

The new scale calculation is internally consistent. A protected critical point has an endpoint collar of radius `O(epsilon^3)` and roof width `O(epsilon^6)`. A collar of roof width `h` has mass bounded below by `h` times the intrinsic jump coefficient and lies in two endpoint strips of width `O(sqrt(h))`. The endpoint-selected exact-index upper bound is therefore `O(h^2 m^{-2})`; division by the collar mass factor `h` gives an `O(h m^{-2})` bound on the complete protected jump cluster. Sending `h` to zero only after the collision-count limit correctly yields `o(m^{-2})` for each coalescing protected atom.

The negative recommendation is nevertheless unavoidable. The manuscript still does not prove the estimate that closes the raw theorem. The complete signed correction remains

```text
D_{B,n,R}=p_{n,R}-K_B*p_{n,R},
```

and the desired pointwise arithmetic local law still requires

```text
sup m^2 esssup |D_{B,n,R}(k,m,t)| -> 0
```

on central exact-index sets.

Revision 45 proves this only for the protected regular critical source. It does not control:

1. critical words violating the fixed protection envelope;
2. grazing and section-decision sources outside that envelope;
3. the remaining finite-jump contributions not represented by protected normal-to-normal words;
4. the noncritical coefficient-first inverse;
5. the full residual derivative or oscillatory budget;
6. the complete weighted signed correction.

The protection parameter is fixed before `m` tends to infinity. No threshold or rate is given when the protection parameter decreases with `m`, and no theorem shows that the unprotected source is negligible. Thus the new theorem does not exhaust the central singular source.

The concrete section residues are also not proved trivial. The correct fixed-radius singleton main term remains the arithmetic factor `mathfrak a_R` times the Gaussian, and the parameter-uniform main term remains the transition kernel `mathcal L_{m,R}`. The manuscript handles this correctly, but it does not prove the unmodulated radius-uniform singleton theorem.

At the requested benchmark, a manuscript organized around raw local inversion must either prove the complete arithmetic pointwise theorem or formulate a substantially broader conceptual result whose independent significance does not depend on that unfinished endpoint. Revision 45 does neither yet, although it is a serious advance toward the first alternative.

## 2. Frozen source, chronology, and qualification

Both reviewed author branches resolve to

`5ab781065787b1aca00ff5182a62da49f847d2e4`.

The repository tree at that commit is

`980d613da10c6ed30d84646b4dc14b029f174669`.

The active manuscript is

`papers/A2-DYN-v45-referee-response`.

The ordinary source payload tree recorded in the source manifest is

`696e8820d1a759f49a094b4e900b8699bc82b7a2`.

The branch chronology is clear. Revision 44 is an intervening author revision based on the revision-43 report; no separate external report was landed for revision 44. Revision 45 then starts from the qualified revision-44 author source. Accordingly, the present review covers both unreviewed additions, modules 94--95 and modules 96--97.

The final source preserves all ninety-five inherited core modules and all one hundred fifteen inherited Python scripts byte-for-byte, while adding modules 96 and 97, revised front matter, proof maps, provenance, diagnostics, and the revision-45 qualification workflow. The bibliography, inherited mathematical labels, and compiled A--X synopsis are retained.

The exact-source workflows completed successfully at the reviewed SHA:

- response branch run `37770668369`;
- referee-copy branch run `37770699128`.

These workflows establish source identity, inherited-file preservation, manifest consistency, normal/optimized finite-check agreement, native TeX compilation, stabilized references, and theorem-page rendering. They do not certify the continuum contact-Hessian calculation, physical collar continuation, coarea comparison, anisotropic transfer-operator estimates, resonance-transition argument, or the missing complete signed-correction theorem.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v45-external-top4-review-2026-10-08/`.

No author source, prior report, workflow, or unrelated repository path is intentionally modified.

## 3. Scope of this review

I did not attempt to re-prove all ninety-seven modules. The substantive audit concentrates on the additions capable of changing the revision-43 assessment:

1. the reduced endpoint action and its curvature on a complete regular word;
2. the coefficient-independent exponential bound on physical level complexity;
3. the complete fixed-count roof-density height estimate;
4. exclusion of divergent physical power--logarithm germs;
5. finite-count BV control and fixed-count smoothing;
6. the jump--cusp separation with unchanged intrinsic coefficients;
7. the summed supremum budget for all continuous singular germs;
8. the exact internal contact Hessian for a protected critical word;
9. exponential decay of endpoint influence;
10. continuation under graded incidence, clearance, and section margins;
11. the cross-Hessian determinant formula for the physical source density;
12. word-length-independent relative distortion;
13. the positive mass collar and its comparison to the intrinsic jump;
14. the two-normal-strip endpoint-selected exact-index upper bound;
15. the use of all resonance branches through parameter transitions;
16. deconcentration of coalescing protected jump clusters;
17. pointwise smallness of every shrinking protected collar source;
18. removal of that source from the signed correction uniformly in bandwidth;
19. the exact boundary between the proved protected estimate and the unresolved complete correction.

The inherited load-bearing inputs include the physical collision second variation, complete finite-collision constructible graph, cumulative return tail, full occupation-torus fixed-band spectrum, physical peripheral projection formula, uniform transition kernel, and fixed-radius arithmetic interval theorem.

## 4. Revision 44: complete fixed-count density height

### 4.1 Reduced endpoint action

For a regular word of `m` flights, the manuscript uses the two endpoint contact coordinates and the reduced polygonal action. The first variation is

```text
dF = R(-p_0 d alpha_0 + p_m d alpha_m).
```

The full contact second variation is positive. Eliminating internal contacts by a Schur complement preserves the positive endpoint-curvature terms, giving a lower Hessian bound proportional to the endpoint incidence cosines.

The endpoint map is also claimed to be injective on a fixed word. The proof interprets the physical reflected tuple as the unique minimizer of the convex polygonal length over the product of closed obstacle disks once the endpoints are fixed. At each internal disk the gradient points strictly outward relative to every different point of that disk, so the convex gradient inequality rules out a second regular reflected tuple with the same endpoints.

This is a useful strengthening of the earlier local critical-word calculation. I found no immediate contradiction in the sign or normalization, but this step deserves direct billiard-geometric verification because the later density bound depends on global injectivity on every regular word.

### 4.2 Exponential level complexity

The manuscript keeps the entire finite collision graph in auxiliary variables. The number of variables and sign conditions grows linearly with `m`, while the degrees remain bounded. A coefficient-independent semialgebraic component bound is therefore exponential in `m`.

Slicing the graph by an initial coordinate bounds the total length of almost every physical roof level. On near-normal endpoint portions, slicing the Gauss map bounds total absolute curvature. The argument is carried out before projection, so decision and grazing boundaries are included by regular exhaustion rather than converted from small discarded mass into a density estimate.

This is a plausible and conceptually appropriate use of finite-degree real geometry. It produces only an exponential-in-count bound, as the manuscript states.

### 4.3 Complete fixed-count height bound

Away from simultaneous near-normality, one of the two endpoint derivatives gives a lower roof-gradient bound of size at worst exponential in `m`. Near normality, strong convexity gives

```text
integral_{F=t} ds/|grad F|
 <= lambda^{-1} integral_{F=t} |curvature| ds.
```

The exponential level-complexity estimate and the finite number of words then yield

```text
||rho_{m,R}||_infinity <= C A^m.
```

The disjointness of the exact events with fixed collision count transfers the same bound to the sum of all actual-return components and to arbitrary bounded measurable insertions.

The theorem is not a local-limit estimate, but it supplies an important missing fact: complete physical component densities are bounded at every fixed count, even at singular and decision-boundary values.

## 5. Revision 44: bounded germs and jump--cusp separation

### 5.1 No divergent physical germs

The complete-component densities have convergent one-sided power--logarithm expansions inherited from the finite-graph preparation. The new fixed-count height bound excludes every negative exponent and every nonconstant logarithm at exponent zero. Thus every one-sided trace is finite.

All positive-exponent terms through exponent one have integrable first derivative, and the remaining prepared term has exponent greater than one. Each fixed component is therefore of bounded variation.

This correctly separates the much larger abstract class of integrable constructible germs from the physically possible complete density germs.

### 5.2 Uniform finite-count BV

For fixed `m`, the finite graph is promoted to a jointly definable family in the radius, section endpoints, and finite-record parameters. Uniform cell decomposition bounds the number of monotonicity intervals, while the fixed-count height bound controls their variation. Summing the finitely many labels gives a finite radius-uniform BV budget `V_m`.

No effective long-time growth bound for `V_m` is supplied. The manuscript does not conceal this limitation.

### 5.3 Intrinsic jumps versus continuous cusps

The complete density is decomposed as

```text
f_ell = j_ell + z_ell + q_ell,
q_ell in W^{2,1}.
```

Here `j_ell` contains localized step profiles with the exact intrinsic jump coefficients; `z_ell` contains the positive-exponent cusp terms with their exact coefficients; and `q_ell` is the residual.

Because each cusp tends to zero at its singular point, its support can be shortened until both its mass and supremum are as small as prescribed. A jump does not share this property: shortening its support reduces its mass but not its height. The manuscript keeps this distinction explicit.

Summing component budgets against the exact reference probabilities yields

```text
sum_ell ||z_ell||_infinity <= delta.
```

Consequently the full continuous singular contribution to `p-K_B*p` is negligible at any prescribed central polynomial scale. This includes continuous singularities arising from decision boundaries, not only regular Morse minima.

### 5.4 What revision 44 leaves

After the cusp terms are paid, the unresolved pointwise correction consists of:

- intrinsic jumps;
- the coefficient-first inverse of the `W^{2,1}` residual;
- any cancellation between those terms.

Revision 45 addresses a substantial subclass of the first item, but not the other two in full.

## 6. Revision 45: protected critical words

A normal-to-normal regular critical word is called `epsilon`-protected when its incidence cosine, section-boundary distance, and nonincident-disk clearance at contact `j` are at least

```text
epsilon q^{distance-to-endpoints/4},
q=47/53.
```

This is notably broader than a fixed positive-margin class. Deep interior contacts may approach grazing and decision boundaries exponentially with their distance from the endpoints.

The parameter `epsilon` is nevertheless fixed before the collision-count limit. The theorem supplies no useful threshold uniform for `epsilon=epsilon_m` tending to zero.

## 7. Endpoint influence and the contact Hessian

### 7.1 Exact internal matrix

In contact arclength coordinates the internal action Hessian is written

```text
H_int = D_c A D_c,
```

where `D_c` is the diagonal incidence matrix and `A` is tridiagonal with off-diagonal entries `-1/ell_j` and diagonal potential

```text
1/ell_{j-1} + 1/ell_j + 2/(R c_j).
```

The diagonal potential makes the normalized off-diagonal row sums at most

```text
q=47/53<1.
```

The Neumann series therefore gives exponential off-diagonal decay of `A^{-1}`. Restoring the incidence factors gives the corresponding estimate for `H_int^{-1}`.

In an endpoint derivative, one incidence factor at the first or last internal contact cancels against the endpoint--internal Hessian entry. This yields endpoint influence decaying geometrically into the word, with only one inverse incidence factor at the observed contact.

The matrix algebra and powers of `q` are internally consistent. The exact billiard second-variation formula, tangent-sign convention, and endpoint cancellation remain important items for specialist verification.

### 7.2 Graded continuation

The displacement of contact `j` under endpoint motion is bounded by

```text
C epsilon^{-1} q^{3 d_j/4} (|du|+|dv|).
```

The allowed margin is `epsilon q^{d_j/4}`. Their ratio therefore has the summable factor `q^{d_j/2}`. Endpoint motion of radius `r_* epsilon^3` keeps every protected margin above half its original lower bound.

The proof also uses that collision states, incidence cosines, section distances, and segment clearance are uniformly Lipschitz functions of adjacent contact positions as long as flight lengths remain bounded away from zero. No inverse incidence cosine is introduced at this stage.

For each fixed word the internal Hessian stays invertible throughout the continuation. Endpoint injectivity then glues the local continuations into the full endpoint square.

This is a coherent route to a word-length-independent collar. It is one of the strongest genuinely new ingredients in revision 45.

## 8. Relative physical source distortion

The physical source density in endpoint coordinates is expressed through the cross derivative of the reduced action:

```text
w_z = |partial_u partial_v F_z|/(4 pi R c).
```

Tridiagonal elimination gives

```text
|partial_u partial_v F_z|
 = c_0 c_m product_j(1/ell_j) / det A.
```

The internal incidence factors cancel between the off-diagonal product and `det H_int`. Logarithmic differentiation produces endpoint terms, flight-length terms, and `tr(A^{-1} dA)`.

The only potentially severe part is the derivative of the diagonal potential `2/(R c_j)`, which costs `|dc_j|/c_j^2`. Combining the endpoint-influence estimate with the protected lower bound gives

```text
C epsilon^{-3} q^{d_j/4} (|du|+|dv|).
```

This is summable over contacts. On the `epsilon^3` endpoint square the logarithmic density distortion is therefore bounded by an absolute constant, giving the relative ratio between `e^{-1}` and `e`.

The use of relative distortion is essential. An absolute derivative estimate for a long collision map would be far too large and would not compare collar mass to the intrinsic coefficient.

I found the determinant bookkeeping plausible and the normalization compatible with the collision probability on the actual section. It should nevertheless be checked independently, especially for parity conventions, the empty internal matrix, and the factor `4 pi R c`.

## 9. Positive mass collar

Strong convexity and bounded endpoint Hessian imply that the sublevel

```text
0 <= F_z-t_z < h
```

lies in the endpoint square when

```text
h < h_* epsilon^6.
```

Both endpoint tangential velocities are then `O(sqrt(h))`. The level is a closed strictly convex curve; its total turning is `2 pi`. Coarea, the Hessian bounds, and relative source distortion give a roof-density comparison

```text
a_* J_z <= g_{z,h}(t_z+s) <= A_* J_z,
0<s<h,
```

and a mass lower bound `a_* h J_z`.

Different word collars remain disjoint in the original deterministic source because the center itinerary and all section decisions are preserved.

This step correctly retains the actual section normalization and unchanged return index.

## 10. The two-normal-strip exact-index upper bound

For endpoint strip width `d`, the manuscript inserts a smooth collision observable supported on `|p|<2d` at both endpoints. Its physical mass is `O(d)`.

The revision-41 transition proof is repeated with these endpoint vectors. At a limiting actual resonance, the physical rank-one projection factorizes, and the endpoint amplitude is bounded by the product of the two endpoint masses, hence by `O(d^2)`. Near-resonant branches approaching the unit circle are retained rather than discarded; their scalar amplitudes converge to the corresponding resonant amplitude. Branches whose limiting modulus is below one decay.

For a fixed roof interval `J` and fixed `d`, ordered Fourier majorants then give

```text
limsup m^2 P(exact labels, roof in J, both endpoints in strips)
 <= C d^2 |J|.
```

The order of limits is important and is correctly stated:

1. fix `d` and the roof interval;
2. fix the Fourier band;
3. let `m` tend to infinity;
4. remove the interval envelope;
5. only later let the collar width tend to zero.

No estimate uniform in the strong multiplier norm as `d` tends to zero is needed. This avoids a common shrinking-observable error.

The inherited transition theorem and physical projection formula remain highly load-bearing, but the new endpoint-mass argument is internally consistent.

## 11. Protected critical-cluster deconcentration

For every protected critical value in `[t-h,t+h]`, take its positive physical collar of roof width `h`. The collars are disjoint, keep the same exact labels, have endpoints in strips of width `O(sqrt(h))`, and have roofs in `[t-h,t+2h]`.

The mass comparison gives

```text
h J^epsilon([t-h,t+h])
 <= P(exact labels, enlarged roof interval, two endpoint strips).
```

The two-strip upper bound is `O(h^2 m^{-2})`. Therefore

```text
limsup sup m^2 J^epsilon([t-h,t+h]) <= C h.
```

No word count and no separation of critical values appear. Exactly coincident values are combined in the positive atomic measure.

For an atom, the preceding interval estimate holds for every fixed `h`. Sending `h` to zero after the limsup proves

```text
sup m^2 J^epsilon({t}) -> 0.
```

This is a valid deconcentration mechanism and directly answers one of the principal concerns in the revision-43 report for the protected regular class.

## 12. Shrinking protected source collars

Let `r_m` be any deterministic sequence tending to zero. The roof density of the union of protected collars of excess width `r_m` is bounded by the protected coefficient measure on `[t-r_m,t]`.

For any fixed `h`, eventually `r_m<h`; the cluster estimate gives a limsup bounded by `C h`. Sending `h` to zero yields

```text
sup m^2 ||p^{epsilon,crit}||_infinity -> 0.
```

The domination is measure-theoretic, so it extends to arbitrary measurable insertions with a common supremum bound. The coefficient-profile version covers localized steps with coefficients bounded by the physical intrinsic jumps.

Finally,

```text
||f-K_B*f||_infinity
 <= (1+||K_1||_1)||f||_infinity
```

removes this already-small part from the signed correction uniformly over every bandwidth. This is not a growing-band transfer-operator estimate, and the manuscript correctly says so.

## 13. The decisive limitation: fixed protection parameter

The protected theorem does not imply that all central critical words are protected at one fixed `epsilon`.

For each finite regular word, the relevant incidence, clearance, and section margins are positive away from its boundaries. But along a sequence of longer words, the minimum ratio

```text
margin_j / q^{distance-to-endpoints/4}
```

may tend to zero arbitrarily fast. The present argument gives no quantitative threshold for the collision count as a function of `epsilon`, and therefore cannot choose `epsilon=epsilon_m` while preserving the deconcentration estimate.

Consequently the following sources remain outside the theorem:

- regular critical words with incidence smaller than the graded envelope;
- words approaching competing collisions or grazing faster than the envelope;
- words approaching section-decision boundaries faster than the envelope;
- singular boundary germs not generated by a protected normal-to-normal minimum.

No estimate shows that their total exact-label density is `o(m^{-2})`.

This is the principal reason the new result does not close the raw theorem.

## 14. The remaining noncritical inverse

Even if every intrinsic jump were controlled, the raw correction still contains the coefficient-first inverse of the `W^{2,1}` residual.

Revision 44 supplies a finite-count BV budget but no useful growth rate. Revision 43 supplies adaptive component bandwidths but no quantitative bound on the actual second-derivative budgets. Revision 45 bypasses those budgets only for the protected critical part.

There remains no theorem proving central-scale cancellation or pointwise smallness of the complete noncritical signed inverse. The fixed-band transition theorem evaluates `K_B*p`; it does not estimate `p-K_B*p` outside the protected source.

## 15. Boundary and decision sources

Revision 44 includes singular and decision-boundary contributions in the complete finite-count density and proves that their continuous positive-exponent cusp terms can be paid in summed supremum norm.

What remains are their finite jumps, any noncritical residual associated with them, and sources whose physical margins collapse too quickly for the protected collar argument.

The source manifest accurately keeps

```text
central_scale_boundary_source_smallness_proved = false,
full_signed_correction_proved = false,
full_raw_return_LLT_proved = false.
```

These are not bookkeeping technicalities; they identify the unresolved central pointwise contributions.

## 16. Arithmetic main term

The manuscript correctly retains the arithmetic structure.

At fixed radius, the exact-index interval and candidate density main term is

```text
c mathfrak a_R(k,n,m) g_{Omega_R}(Z),
```

or equivalently `mathfrak a_R g_{D_R}` in return normalization. Uniformly through changes of arithmetic type, the main term is the finite transition kernel `mathcal L_{m,R}`.

Revision 45 neither proves nor assumes that all concrete section residues vanish. The two-strip estimate sums the absolute contributions of every surviving resonant branch and therefore does not require an unmodulated law.

Any final pointwise theorem must retain this arithmetic main term unless the zero-residue criterion is independently verified.

## 17. Weighted consequences

The protected positive-source estimate extends to arbitrary bounded measurable insertions by domination. This is stronger than requiring such insertions to be strong multipliers for this particular source restriction.

It does not estimate the complete weighted signed correction. Unprotected sources and the noncritical inverse still need a parallel weighted theorem before one can promote the fixed-interval exact-event bridge to pointwise roof conditioning or obtain every historical weighted numerator and denominator.

Thus revision 45 improves the weighted critical-source analysis but does not complete the weighted raw program.

## 18. Relation to existing local-limit methods

The established literature already contains local central limit theorems for finite-horizon Lorentz processes, abstract local central limit theorems for suspension flows including finite-horizon Sinai billiards, anisotropic transfer-operator perturbation frameworks for Lorentz gases, and mixing local limit theorems with endpoint observables.

The distinctive content here is not the existence of local-limit or anisotropic methods in general. It is the simultaneous treatment of the moving family, actual section occupation, arithmetic exact return indices, raw roof singularities, and the protected critical-cluster comparison.

That content is technically substantial. At present it remains specialized to the triangular finite-horizon family and does not culminate in the full advertised raw-density theorem. The manuscript also does not formulate the protected-collar/deconcentration mechanism as a broad abstract theorem with several independent applications.

Accordingly, the new results strengthen the case for a focused dynamics/probability paper but do not by themselves establish the breadth or endpoint completion expected at the requested four-journal benchmark.

## 19. Independent specialist verification

The following claims require direct human expert audit:

1. the exact contact second variation and the factorization `H_int=D_c A D_c`;
2. the row-sum bound and off-diagonal decay of the inverse contact matrix;
3. cancellation of one incidence factor in the endpoint response;
4. Lipschitz control of incidence, clearance, and section distance without inverse-incidence loss;
5. continuation over the full endpoint square and endpoint injectivity;
6. the cross-Hessian determinant formula and the factor `4 pi R c`;
7. the logarithmic determinant derivative and the summation with exponent `1/4`;
8. the coarea total-turning comparison and collar density bounds;
9. disjointness of all physical collars while preserving exact return decisions;
10. endpoint-selected anisotropic pairings for shrinking normal strips;
11. scalar amplitude continuity through arithmetic transitions;
12. the full occupation-torus spectral theorem inherited from revisions 40--41;
13. the complete finite-graph constructible density at singular and decision boundaries;
14. the uniform definable-family BV argument;
15. the exact separation of jumps, cusps, and the residual inverse.

The successful workflows and finite rational models do not settle these continuum issues. The manuscript correctly distinguishes source qualification from proof certification.

## 20. Required work for a subsequent revision

A subsequent revision seeking the same benchmark should address the following in priority order.

### 20.1 Exhaust the protection scales

Prove a quantitative theorem for words whose protection parameter decreases with the collision count, or decompose the unprotected source into protection scales and sum the resulting estimates with explicit thresholds.

A statement for each fixed `epsilon` is not enough unless the complement is shown negligible.

### 20.2 Control the unprotected boundary source

Give a central-scale pointwise estimate for near-grazing, competing-hit, and section-decision sources outside the protected envelope. Continuous cusp localization is already available; the remaining finite jumps and residual terms must be treated.

### 20.3 Estimate the noncritical signed inverse

Prove direct cancellation or a quantitative Fourier/variation estimate for the complete `W^{2,1}` residual inverse. The current fixed-count BV existence and adaptive reconstruction certificates do not provide a long-time local-limit bound.

### 20.4 Close the complete arithmetic correction

Combine the protected critical estimate, unprotected boundary estimate, and noncritical inverse into

```text
sup m^2 esssup |D_{B,n,R}| -> 0
```

with `mathcal L_{m,R}` as the uniform main term and `mathfrak a_R` as the fixed-radius specialization.

### 20.5 Treat the complete weighted class

Extend the final signed-correction estimate to the endpoint and path insertions needed for pointwise conditioning. Domination of the protected positive source does not control the remaining signed terms.

### 20.6 Preserve the order of limits

Any use of the two-strip estimate must keep strip width and roof interval fixed until after the collision-count limit. A future proof with `epsilon_m`, shrinking strips, or growing bands must provide new quantitative estimates rather than reuse the qualitative theorem outside its quantifiers.

### 20.7 Obtain independent specialist review

The contact geometry, finite-graph preparation, anisotropic spectrum, resonance transitions, and bridge arguments should be audited by specialists before publication claims are made.

### 20.8 Strengthen the conceptual statement

If the full raw theorem remains out of reach, isolate the completed stationary, arithmetic interval, bridge, posterior, height, cusp, and protected-cluster results into a focused theorem package. Alternatively, formulate the protected-collar deconcentration mechanism abstractly and demonstrate it in genuinely distinct singular hyperbolic systems.

### 20.9 Reduce the central route

The current article asks the reader to navigate ninety-seven core modules while the title theorem remains open. A top-four submission should present one completed principal theorem and move historical derivation interfaces out of the main route unless they are closed.

## 21. Technical comments

1. Keep `m` for collision count and `n` for return index in every supremum.
2. Keep `B` for roof-frequency bandwidth and `J_z` for intrinsic jump coefficients.
3. State the fixed-protection quantifier whenever the critical-cluster theorem is invoked.
4. Do not infer a rate for `epsilon=epsilon_m` from the fixed-`epsilon` theorem.
5. Preserve the exact arithmetic transition kernel in every uniform pointwise target.
6. Do not describe the continuous cusp budget as a bound on jump coefficients or residual derivatives.
7. Do not describe the complete fixed-count height bound `C A^m` as a local-limit estimate.
8. Keep the distinction between relative source distortion and an absolute derivative bound.
9. Retain the actual section normalization `c^{-1}` in every collar coefficient.
10. State explicitly that the endpoint strip multiplier norms may diverge as `d` tends to zero; the proof avoids needing uniformity by its order of limits.
11. Preserve the right-trace convention at finite jumps.
12. Do not assign finite values to any divergent germ in an abstract preparation statement, even though revision 44 excludes such germs for the physical source.
13. Keep the unprotected boundary source separate from the protected regular critical source.
14. Keep the noncritical inverse visible in the final remainder.
15. Do not call all-band convolution removal a growing-band spectral theorem.
16. A finite packet average still does not identify a prescribed singleton.
17. The pointwise roof-conditioned bridge remains unproved.
18. Source qualification and finite tests remain distinct from continuum proof certification.

## 22. Overall assessment

Revisions 44 and 45 are serious and constructive responses to the latest external report.

Revision 44 establishes complete fixed-count density height control, excludes divergent physical germs, proves finite-count BV regularity, and removes every continuous positive-exponent singular term with a prescribed summed pointwise budget.

Revision 45 constructs word-length-independent endpoint collars under exponentially relaxed interior margins, proves relative physical source distortion, obtains a positive mass comparison with unchanged intrinsic jump coefficients, and combines this with the arithmetic transition theory to deconcentrate complete protected critical clusters. Coalescing protected atoms and every shrinking protected collar source are pointwise `o(m^{-2})`, and this source can be removed from the signed correction uniformly in bandwidth.

I found no decisive error in modules 94--97 within the scope of this review.

The manuscript nevertheless remains short of the theorem governing its title and central architecture. The protection parameter is fixed; the unprotected near-boundary source is not shown negligible; the noncritical residual inverse is not estimated; the complete signed correction is not proved small; the concrete arithmetic residues are not proved trivial; and the complete weighted pointwise theory remains open.

Subject to independent specialist verification, the completed stationary, interval, arithmetic, bridge, posterior, full-source reconstruction, complete-height, cusp, and protected-cluster results could support a strong focused paper. They do not yet constitute a complete top-four raw local inversion theorem.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
