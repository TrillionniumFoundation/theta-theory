# External top-four referee report on A2-DYN revision 51

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v51-referee-response-2026-10-09`, `revision/a2-dyn-v51-referee-copy-2026-10-09`  
**Reviewed commit:** `39ee9d88831a574a519785407732b3872ccbca3b`  
**Reviewed repository tree:** `16025cef389bc9a4b417d60d64d24e7b6f4fad42`  
**Ordinary source payload tree:** `ab57716245c04f820cc63b684f74ba1c2dfe0e2e`  
**Active manuscript directory:** `papers/A2-DYN-v51-referee-response`  
**Active mathematical source:** one hundred nine numbered core modules; revision 51 retains the one hundred seven revision-49 modules and adds modules 108--109  
**Completed mathematical baseline:** revision 49, commit `f3174ed1e7e339aa9c4bb5bd716a24653080c7dd`  
**Latest submission-status report:** `reviews/a2-dyn-v50-external-top4-review-2026-10-09/REFEREE_REPORT.md`, commit `e951b35077f020ae7e5ac711510e49be1faeb4ef`, blob `fa4b5109f7c38d8286f93cd723d6c751378df439`  
**Controlling substantive mathematical report:** `reviews/a2-dyn-v49-external-top4-review-2026-10-09/REFEREE_REPORT.md`, commit `11520f4876ca9033c0a0abfbdb0041e1f85c260e`, blob `cad56babdd60f941c0e554dc88c99e90c20335b4`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 51 is a complete theorem-bearing manuscript and is a substantive response to both controlling reports.

It resolves the procedural defect of revision 50: the two author branches now identify the same complete source, the full article and all inherited modules are present, and exact-source manuscript qualification has succeeded on both refs.

It also makes a genuine mathematical advance beyond revision 49. Revision 49 proved translation-uniform local-variation convergence for the complete original exact-index density but correctly left open the possibility of very narrow physical-boundary spikes. Revision 51 does not commit the invalid inference from local `L^1` convergence to uniform convergence. Instead it uses the exact positive source decomposition to prove that, at every fixed reconstruction band, the complete normalized density error is uniformly approximated by the **nonnegative physical remainder**. The immediate consequence is a one-sided essential-supremum local theorem:

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_u
 \bigl(\mathcal L_{m,R}(k_1,k_2,u,n)
             -m^2p_{n,R}(k,m,u)\bigr)_+\longrightarrow0.
\]

Equivalently, the original exact-index density cannot develop microscopic holes below the arithmetic transition profile, apart from a uniformly vanishing error. On target roof sets where the transition profile has a positive pointwise lower bound, this gives microscopic denominator bounds for arbitrary measurable subsets. On fixed positive-length windows it yields an asymptotically full common part of the true and reference conditional roof laws, together with reverse likelihood and reverse relative-entropy convergence.

I audited the new modules

- `core/108_positive_remainder_lower_law.tex`;
- `core/109_exact_roof_minorization.tex`;

and their dependence on the revision-49 local-variation theorem, the exact physical-only source partition, the protected pointwise correction, the all-depth decision correction, and the fixed-band arithmetic reconstruction. I found no decisive algebraic error, normalization error, sign error, invalid exchange of a count-dependent band with a fixed-band estimate, or hidden replacement of the original exact return event.

The new logical step is sound in its stated scope. In particular:

1. the convolution-height lemma controls only a **fixed smooth convolution**, not the unconvolved density;
2. the collision limsup is taken before the auxiliary local-window scale tends to zero;
3. the positive-remainder principle uses positivity only for the remainder, not for the reconstruction kernel or controlled source;
4. the arithmetic transition kernel is retained uniformly and the fixed-radius arithmetic residue is not set equal to one;
5. the lower denominator is an almost-everywhere density statement, not a positive probability for equality of a continuous roof coordinate;
6. conditional minorization is proved for the unchanged exact event and a fixed roof window; and
7. only reverse likelihood control is claimed.

The negative recommendation nevertheless remains unavoidable at the requested benchmark. The manuscript still does not prove its historical two-sided pointwise raw-density theorem. The positive physical remainder may contain arbitrarily narrow **upward** incidence or clearance spikes. Revision 51 identifies these spikes as the only remaining pointwise obstruction, but does not bound their essential height. Consequently the following remain unproved:

- the two-sided pointwise arithmetic raw local limit theorem;
- central-scale essential-height smallness of the incidence remainder;
- central-scale essential-height smallness of the clearance remainder;
- the full pointwise physical-boundary correction;
- a pointwise roof-conditioned path bridge;
- forward likelihood or forward relative-entropy convergence;
- and the unmodulated specialization unless the section residue criterion is separately verified.

The new abstract positive-remainder principle is useful but elementary. The difficult dynamical inputs remain highly specialized to the present triangular finite-horizon Lorentz family and depend on a long inherited anisotropic-space chain without independent specialist certification. At a top-four level, a manuscript of this size and title should either complete the two-sided pointwise endpoint or extract a substantially broader theorem whose independent significance no longer depends on that unfinished endpoint.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`39ee9d88831a574a519785407732b3872ccbca3b`.

The repository tree is

`16025cef389bc9a4b417d60d64d24e7b6f4fad42`.

The active article is

`papers/A2-DYN-v51-referee-response`.

The ordinary source payload tree is

`ab57716245c04f820cc63b684f74ba1c2dfe0e2e`.

The chronology is now correct.

1. Revision 49 is the last completed mathematical baseline.
2. The revision-49 external report is the controlling substantive assessment.
3. Revision 50 froze that report but did not contain a manuscript.
4. The revision-50 submission-status report returned that incomplete object without substantive review.
5. Revision 51 descends from the revision-50 report and restores the complete revision-49 article before adding new mathematics.

The source manifest records that all one hundred seven inherited core modules and all one hundred thirty-five inherited Python files are byte-identical. The bibliography, two compiled theorem appendices, inherited mathematical labels, former source records, and the original exact-return density target are retained. Revision 51 adds only the two proof modules listed above to the mathematical body, together with revised front matter, provenance, response, ledgers, audit maps, validation files, and qualification support.

The present review branch begins directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v51-external-top4-review-2026-10-09/`.

No author manuscript source, previous review, workflow, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The complete-manuscript qualification workflows succeeded on both final author refs:

- response branch run `37868721218`;
- referee-copy branch run `37868732858`.

The workflow verifies, among other things:

- the exact complete revision-49 baseline tree;
- strict blob identity for both the revision-49 substantive report and revision-50 submission-status report;
- all one hundred nine TeX core inclusions;
- byte identity of the one hundred seven inherited cores and one hundred thirty-five inherited scripts;
- retention of the bibliography, theorem appendices, and inherited labels;
- the ordinary-source Merkle identity and workflow hash;
- normal/optimized finite-check agreement;
- native TeX compilation with stabilized references;
- and label-based rendering of the new theorem pages.

The new finite tests check the convolution/source identity, positive-part contraction, separation of the two positive remainders, exact minorization normalization, residual mixture mass, band exponent arithmetic, a thin-hole counterexample, and positive-spike counterexamples to invalid forward-likelihood conclusions.

These checks are appropriate and useful. They establish source identity, finite algebra, build reproducibility, and consistency of the declared proof graph. They do not establish the inherited continuum assertions, including the physical thin-layer multiplier, full occupation-torus spectral theory, moving peak expansions, all-depth source decomposition, or the revision-49 local-variation theorem. Nor do they prove the missing positive-height bound.

## 4. Scope of this review

I did not attempt to re-prove all one hundred nine modules. The substantive audit concerns the steps that can change the revision-49 assessment:

1. the fixed-convolution height lemma;
2. the abstract positive-remainder principle;
3. the exact positive decomposition of the original source;
4. the transfer of revision-49 local variation to fixed-band smoothed height;
5. the ordered choice `epsilon(B)=A_0 B^(-1/12)`;
6. the normalized error representation by the positive physical remainder;
7. the one-sided pointwise arithmetic lower law;
8. equivalence of the two-sided pointwise theorem with positive incidence and clearance height smallness;
9. microscopic denominator bounds on positive-reference target sets;
10. exact-window conditional minorization;
11. reverse likelihood and reverse relative entropy;
12. the distinction between almost-everywhere density statements and conditioning at one prescribed roof value;
13. source completeness and qualification evidence;
14. editorial significance at the requested venue level.

The revision-49 physical local-variation theorem and its continuum dependencies are treated as the source-pinned mathematical baseline, subject to the verification qualifications already stated in the revision-49 report.

## 5. The fixed-convolution height lemma

The first new lemma states that for `K in W^{1,1}(R)` and a locally integrable `f`,

\[
 \|K*f\|_\infty
 \le \bigl(h^{-1}\|K\|_1+\|K'\|_1\bigr)
               \|f\|_{1,h}^{\mathrm{loc}}.
\]

The proof partitions the real line into intervals of length `h`. On each interval the absolutely continuous representative of `K` satisfies

\[
 \sup_I |K|\le h^{-1}\int_I|K|+\int_I|K'|.
\]

The translated `L^1` mass of `f` on every such cell is bounded by the local norm. Summing the cell suprema gives the displayed estimate. Since `K,K'` are integrable, the series is finite and Tonelli applies.

The limiting consequence is also correct. If

\[
 \limsup_m\sup_\lambda h^{-1}
   \|f_{m,\lambda}\|_{1,h}^{\mathrm{loc}}\le s
\]

for every fixed `h>0` with the same `s`, then at each fixed `h`

\[
 \limsup_m\sup_\lambda\|K*f_{m,\lambda}\|_\infty
 \le s(\|K\|_1+h\|K'\|_1).
\]

Only after this collision limsup does the proof let `h` tend to zero. The kernel remains fixed. Hence

\[
 \limsup_m\sup_\lambda\|K*f_{m,\lambda}\|_\infty
 \le s\|K\|_1.
\]

This does not estimate `\|f\|_\infty`, and the manuscript repeatedly preserves that distinction.

I found this lemma correct.

## 6. The positive-remainder principle

The abstract principle assumes, for each fixed reconstruction band,

\[
 P=A+R,\qquad R\ge0,
\]

with

- fixed-band reconstruction of the full density;
- pointwise correction control for `A`;
- local-variation control for `R`.

The exact identity is

\[
 P-G-R=(A-K_B*A)+(K_B*P-G)-K_B*R.
\]

The first term is bounded by the controlled correction estimate, the second tends to zero by fixed-band arithmetic inversion, and the third is bounded by the preceding convolution lemma. The kernel is permitted to change sign. The controlled source is permitted to change sign. Only `R` must be nonnegative.

Since

\[
 (G-P)_+\le |P-G-R|
\]

when `R>=0`, the same bound yields a one-sided lower theorem. The proof fixes the band throughout the collision limit and sends the band to infinity only afterwards.

I found the identity, sign use, norm estimate, and limit order correct.

The principle is worth isolating because it precisely identifies the additional information unavailable from local `L^1` convergence alone. It is, however, a short real-analysis observation rather than a general new local-limit theorem by itself.

## 7. Application to the original source

The inherited exact source decomposition is

\[
 p=f^{\varepsilon,1}
   +d^{\varepsilon,\varepsilon,1}
   +b^{\varepsilon,1},
\qquad
 b^{\varepsilon,1}
 =b_{\mathrm{inc}}^{\varepsilon,1}
  +b_{\mathrm{clr}}^{\varepsilon,1}\ge0.
\]

Here:

- `f` is the smoothly protected source;
- `d` is the complete physically protected section-decision source;
- `b` contains every history with an incidence or clearance defect, including histories which later have section-decision defects.

All terms retain the original exact labels and the original normalized section source. The factor `1/c` is already present in the density and is not inserted again in revision 51.

The nonnegativity of `b` is genuine source positivity before pushforward, not positivity of a signed Fourier correction. The incidence and clearance components form a disjoint first-physical-defect partition before pushforward.

This is the correct sign structure for the new principle.

## 8. Fixed-band smoothed height of the physical remainder

Revision 49 proves, for every fixed margin and fixed roof-window length,

\[
 \limsup_m\sup_{R,n,k,|w|\le M}
 \frac{m^2}{h}
 \|b^{\varepsilon,w}_{n,k,m,R}\|_{1,h}^{\mathrm{loc}}
 \le CM\varepsilon^{1/16}.
\]

Applying the convolution-height lemma to `m^2b` and the fixed kernel `K_B` gives

\[
 \limsup_m\sup_{R,n,k,|w|\le M}
 m^2\|K_B*b^{\varepsilon,w}_{n,k,m,R}\|_\infty
 \le CM\varepsilon^{1/16}\|K_1\|_1.
\]

The constant is independent of the fixed reconstruction band because `\|K_B\|_1=\|K_1\|_1`. This statement is not a supremum over `B=B_m` inside the collision limit.

The finite-count reading keeps the reconstruction band and auxiliary spectral band separate. Both are fixed before the collision count tends to infinity; the auxiliary band may be enlarged afterwards. No orbit is transported through a grazing or competing-hit seam.

This use of revision-49 local variation is legitimate.

## 9. The ordered exponent budget

The manuscript chooses

\[
 \varepsilon(B)=A_0B^{-1/12}.
\]

For the controlled source:

- the protected correction is `O(B^{-1/2})`;
- the all-depth decision correction is `O(\varepsilon^{1/16})`.

For the positive physical remainder, the smoothed-height contribution is also `O(\varepsilon^{1/16})`. Hence

\[
 \varepsilon(B)^{1/16}=A_0^{1/16}B^{-1/192}.
\]

The protected theorem requires `B>=C_2\varepsilon^{-12}`. With the displayed choice this is

\[
 B\ge C_2A_0^{-12}B,
\]

which follows once `A_0^{12}>=C_2`.

The exponent arithmetic and quantifier order are correct:

1. fix `B`;
2. thereby fix `\varepsilon(B)`;
3. take the collision limsup;
4. remove the auxiliary local regularization in the inherited physical estimate;
5. then send `B` to infinity.

No quantitative growth bound for spectral constants in `B` is used.

## 10. Uniform positive-remainder representation

The principal new estimate is

\[
 \limsup_{m\to\infty}\sup_{R,n,k}
 \|P_{m,R}^{n,k}-G_{m,R}^{n,k}
             -\mathfrak b_{B,m,R}^{n,k}\|_\infty
 \le CB^{-1/192},
\]

where

\[
 P=m^2p,\qquad
 G=\mathcal L_{m,R},\qquad
 \mathfrak b_B=m^2b^{\varepsilon(B),1}\ge0.
\]

The proof combines three statements in their proper norms:

1. fixed-band arithmetic reconstruction gives `K_B*P-G -> 0` uniformly;
2. the protected and decision sources have pointwise correction bounds;
3. the physical remainder has a local-variation bound, converted only after convolution to fixed-band height.

The proof does **not** estimate the unconvolved height of the physical remainder. It therefore does not close the two-sided pointwise theorem by sleight of hand.

I found this deduction correct, subject to the inherited continuum inputs.

## 11. The one-sided pointwise lower law

Because `\mathfrak b_B>=0`,

\[
 (G-P)_+\le |P-G-\mathfrak b_B|.
\]

For every fixed sufficiently large `B`, the collision limsup is at most `CB^{-1/192}`. Sending `B` to infinity gives

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_u(G-P)_+	o0.
\]

This is a genuine essential-supremum theorem for the complete original density. It excludes downward defects at the natural normalized scale.

Several scope qualifications are essential.

- The theorem is one-sided.
- It is an almost-everywhere density statement.
- The uniform main term is the finite transition kernel, not an unmodulated Gaussian.
- At fixed radius on central compact sets the main term is the Gaussian multiplied by the unchanged arithmetic coefficient.
- The theorem does not assign a value at an arbitrarily selected exceptional roof point.
- It does not control narrow upward spikes.

The manuscript states all of these qualifications accurately.

## 12. The remaining positive-height criterion

The error representation gives, on a fixed central compact set,

\[
 \bigl|\|(P-G)_+\|_\infty
       -\|\mathfrak b_B\|_\infty\bigr|
 \le \|P-G-\mathfrak b_B\|_\infty.
\]

This follows from the pointwise inequality

\[
 |x_+-b|\le|x-b|,\qquad b\ge0.
\]

Consequently the full two-sided pointwise law is equivalent to

\[
 \lim_{B\to\infty}\limsup_{m\to\infty}
 \|\mathfrak b_{B,m}\|_{\infty,M}=0.
\]

Since

\[
 \mathfrak b_B
 =m^2b_{\mathrm{inc}}^{\varepsilon(B),1}
  +m^2b_{\mathrm{clr}}^{\varepsilon(B),1}
\]

with both components nonnegative, vanishing of the sum in essential supremum is equivalent to separate vanishing of the two positive component heights.

This is a sharper characterization than the previous signed correction criterion. It rules out the possibility that a cancellation of signed convolution corrections could hide a positive spike.

It is nevertheless a criterion, not a proof of the criterion. Positive incidence and clearance concentration remain possible.

## 13. Microscopic denominator bounds

Let

\[
 \mathcal T(d)=\{u:G(u)\ge d\}.
\]

The lower law gives

\[
 P(u)\ge G(u)-\delta_m
\]

almost everywhere, uniformly, with `\delta_m->0`. Hence for sufficiently large `m`,

\[
 p_{n,R}(k,m,u)\ge \frac d{2m^2}
\]

for almost every `u in \mathcal T(d)`.

For every Borel set `E subset \mathcal T(d)` of finite Lebesgue measure,

\[
 \nu_R^*\{K_n=k,N_n=m,T_n\in E\}
 \ge m^{-2}(1-\delta_m/d)\int_EG(u)\,du.
\]

The set `E` may depend on `m` and may have arbitrarily small positive measure. This is stronger than the revision-49 fixed-window denominator statement on the lower side.

It remains only a lower bound. It supplies no matching upper asymptotic for count-dependent shrinking sets.

## 14. Exact-window conditional minorization

Fix a roof interval `I_t=[t,t+h]` on which `G>=d` almost everywhere. Put

\[
 F=\int_{I_t}P,\qquad H=\int_{I_t}G.
\]

The lower law gives

\[
 P\ge(1-\delta_m/d)G
\]

on the interval. The revision-49 local-variation theorem gives

\[
 F\le H+he_m(h)\le H(1+e_m(h)/d).
\]

Therefore, after normalization,

\[
 \mathbb P_{m,R}^{n,k,t}
 \ge \alpha_m(d,h)\mathbb Q_{m,R}^{n,k,t},
\]

with

\[
 \alpha_m(d,h)
 =\frac{1-\delta_m/d}{1+e_m(h)/d}\longrightarrow1.
\]

The event remains exactly

\[
 K_{n,R}=k,\qquad N_{n,R}=m,\qquad T_{n,R}\in I_t.
\]

The difference measure has mass `1-alpha_m` and yields the exact mixture

\[
 \mathbb P=\alpha_m\mathbb Q+(1-\alpha_m)\mathbb S.
\]

This proof is correct. It requires the **pointwise** lower bound `G>=d` on the whole window, not merely a positive integrated reference mass. The manuscript explicitly states this stronger target condition.

## 15. Reverse likelihood and entropy

Measure domination implies

\[
 \frac{d\mathbb Q}{d\mathbb P}\le\alpha_m^{-1}.
\]

Hence

\[
 D_\infty(\mathbb Q\Vert\mathbb P)
 \le -\log\alpha_m\to0,
\]

and

\[
 0\le D(\mathbb Q\Vert\mathbb P)
 \le D_\infty(\mathbb Q\Vert\mathbb P)\to0.
\]

The direction is important. The true law may carry a narrow positive spike of small total mass. Such a spike is compatible with domination of the reference by the true law and with reverse entropy convergence, while forward `D_\infty` or forward relative entropy may diverge.

The manuscript includes a correct elementary example demonstrating this asymmetry and does not claim a forward result.

## 16. Arithmetic scope

Revision 51 preserves the finite transition kernel `\mathcal L_{m,R}` in every uniform statement. At fixed radius and on central compact sets it specializes to

\[
 c\,\mathfrak a_R(k,n,m)g_{\Omega_R}(Z).
\]

No nontrivial section residue is silently set to zero. The lower denominator and minorization theorems apply only where the actual transition reference has a positive pointwise lower bound.

Thus zero arithmetic classes remain zero or negligible in the appropriate sense, and no conditional law is assigned to them.

The paper still has two mathematically legitimate routes for its final exact-index theorem:

1. retain the arithmetic coefficient and transition kernel as intrinsic; or
2. prove uniform phase masses for the concrete section and deduce the unmodulated specialization.

Revision 51 follows the first route for its proved theorems. That is the honest formulation.

## 17. What revision 51 does not prove

The remaining omissions are mathematically central.

### 17.1 No upper pointwise law

The manuscript does not prove

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_u
 \bigl(m^2p_{n,R}(k,m,u)-\mathcal L_{m,R}(k_1,k_2,u,n)\bigr)_+	o0.
\]

The positive physical remainder is precisely the possible obstruction.

### 17.2 No two-sided pointwise raw-density LLT

The inherited flags

- `full_raw_return_LLT_proved`;
- `pointwise_roof_density_LLT_proved`;
- `common_pointwise_return_correction_proved`;
- `full_return_complement_proved`

remain false.

### 17.3 No single-roof conditional bridge

A lower density at almost every roof value does not supply a path numerator at that same roof value. The fixed-window bridge and conditional roof minorization do not prove a bridge conditioned at one prescribed continuous roof coordinate.

### 17.4 No forward likelihood control

Upward spikes remain compatible with all new results.

### 17.5 No independent continuum audit

The most difficult billiard and operator estimates are inherited rather than independently verified.

## 18. Relation to existing local-limit theory and novelty

Existing work already contains local central limit theorems for the finite-horizon planar Lorentz process, mixing local limit theorems with endpoint observables for dispersing billiards, and abstract local central limit theorems for suspension flows including finite-horizon Sinai billiards.

Revision 51's distinctive contribution is not a Gaussian local limit in isolation. It is the conjunction of

- the actual four-coordinate first-return record;
- exact return and collision indices;
- arithmetic transition residues;
- a complete original roof density;
- an all-depth physical source decomposition;
- translation-uniform local variation;
- and a positivity mechanism yielding a one-sided pointwise theorem and exact-window minorization.

This is meaningful specialist mathematics. The positive-remainder argument also has some reusable value when a dynamical problem already supplies the three hypotheses of the abstract principle.

Nevertheless, the new abstract proposition is elementary and the difficult hypotheses are verified only through the manuscript's highly specialized Lorentz-gas machinery. The paper does not yet extract a broad theorem for a class of singular hyperbolic systems with several independent applications.

That level of specialization, together with the unfinished upper pointwise endpoint, is insufficient for the requested four-journal benchmark.

## 19. Presentation and architecture

Revision 51 improves the theorem hierarchy by placing the revision-49 local-variation theorem next to the new one-sided pointwise theorem. The introduction explicitly explains the passage from local variation to a lower law and identifies the positive-spike obstruction.

The article is nevertheless exceptionally large. It compiles one hundred nine core modules, multiple historical raw-inversion routes, two local records, arithmetic resonance theory, conditional bridges, physical source decompositions, validation ledgers, and retained theorem appendices.

For publication, the authors should choose one of two architectures.

### Architecture A: a focused local-variation and lower-law paper

Center the article on:

- the complete original density;
- translation-uniform local variation;
- the positive-remainder representation;
- the one-sided pointwise lower law;
- microscopic denominators and exact-window minorization.

The unfinished positive-height program can be moved to a sequel or companion technical paper.

### Architecture B: the complete raw-inversion paper

Retain the current title and full architecture after proving the incidence and clearance essential-height bounds and completing the two-sided pointwise arithmetic theorem.

At present the manuscript remains between these two editorial forms.

## 20. Independent specialist verification

Before the new results can be relied upon as a journal theorem, a human specialist should verify at least the following inherited inputs and their interface with revision 51:

1. image-side clearance geometry and the previous-disk exception;
2. uniform finite candidate-center lists;
3. stable transversality of incidence and clearance boundaries;
4. homogeneity-strip complexity and horizontal grazing thresholds;
5. the piecewise multiplier theorem on the actual strong completion;
6. absence of inverse-width losses;
7. moving-peak weak-to-strong interpolation;
8. full occupation-torus power bounds and peripheral decomposition;
9. all-depth decision summation;
10. the exact positive physical-only source partition;
11. finite-count `m^3 rho^(m/2)` physical errors;
12. fixed-band full-source arithmetic reconstruction;
13. the revision-49 local-variation theorem;
14. source normalization and the single factor `1/c`;
15. the use of essential-supremum representatives in revision 51.

The two new real-analysis lemmas themselves are straightforward, but their application inherits all these continuum obligations.

## 21. Required changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

1. **Control positive incidence height.**  
   Prove central-scale essential-supremum smallness of the positive incidence remainder in the ordered limit.

2. **Control positive clearance height.**  
   Prove the corresponding bound for the competing-hit clearance remainder.

3. **Complete the two-sided pointwise theorem.**  
   Combine those estimates with the revision-51 representation, retaining the transition kernel and arithmetic factor.

4. **Resolve the pointwise bridge if retained as a target.**  
   Supply a same-roof path numerator and a two-sided density denominator, rather than relying on fixed-window conditioning.

5. **Preserve arithmetic honesty.**  
   Do not replace the finite transition kernel by one Gaussian uniformly unless the section residue criterion is proved.

6. **Obtain independent specialist review.**  
   The physical multiplier and inherited operator chain require line-by-line verification.

7. **Extract greater generality or narrow the claim.**  
   Either formulate a reusable singular-hyperbolic positive-remainder theorem with independent applications or present the completed Lorentz-family result as a focused specialist paper.

8. **Shorten the proof route.**  
   Separate historical pipelines and status infrastructure from the minimal theorem dependency chain.

## 22. Technical and expository comments

1. Every occurrence of “pointwise” should continue to specify essential supremum or almost-everywhere density scope.
2. The uniform theorem should retain `\mathcal L_{m,R}` rather than replace it by a fixed-radius Gaussian.
3. The central compact restriction should be displayed whenever using `c\mathfrak a_R g_{\Omega_R}`.
4. The order `m -> infinity` before `B -> infinity` must remain visible.
5. The auxiliary spectral band and reconstruction band must remain distinct.
6. The dependence `epsilon(B)=A_0B^(-1/12)` should not be converted into a count-dependent margin without a new quantitative theorem.
7. The positive remainder should never be called small in height until the missing criterion is proved.
8. The lower denominator statement should retain “almost every roof value”.
9. A measurable roof set may depend on `m`, but must remain within the displayed positive-reference set.
10. Conditional minorization requires `G>=d` pointwise on the full fixed interval, not merely positive total transition mass.
11. Reverse and forward likelihood directions should remain explicitly distinguished.
12. The mixture residual `S_m` is a decomposition of the same conditional law, not a replacement event.
13. The fixed-window minorization should not be described as a single-roof bridge.
14. The source factor `1/c` should continue to appear exactly once.
15. The revision-50 charter and freeze workflow should remain provenance, not mathematical baseline evidence.
16. Source qualification should remain separated from proof certification.

## 23. Final assessment

Revision 51 is a serious and constructive response.

It restores a complete manuscript after the procedural failure of revision 50. More importantly, it uses the exact positivity structure of the physical remainder to extract new pointwise information which revision 49's local-variation theorem alone could not provide. The fixed-convolution lemma and positive-remainder identity are correct. The resulting one-sided essential-supremum arithmetic lower law, microscopic denominator bounds, exact-window minorization, and reverse likelihood convergence are genuine theorem-level advances.

The paper also identifies the remaining pointwise obstruction in a much cleaner form: the two-sided raw theorem is now equivalent to essential-height decay of two explicit nonnegative sources, incidence and clearance. This is a meaningful reduction.

But the reduction is not the endpoint. Positive narrow spikes remain unbounded. The complete two-sided pointwise arithmetic density theorem and single-roof conditioned path theorem remain open in the manuscript's own status ledger. The difficult dynamical machinery is still model-specific and awaits independent expert audit.

Subject to such verification, the revision-49 local-variation theorem together with the revision-51 lower law could support a strong specialist dynamics/probability paper, especially in a focused architecture.

At the requested *Annals* / *Acta* / *Inventiones* / *JAMS* benchmark, however, the central pointwise raw-inversion endpoint is still incomplete and the present generality/significance case does not compensate for that incompleteness.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
