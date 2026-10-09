# External top-four referee report on A2-DYN revision 52

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v52-referee-response-2026-10-09`, `revision/a2-dyn-v52-referee-copy-2026-10-09`  
**Reviewed commit:** `4449ba65b59d2670fb1231515e860d874b466b87`  
**Reviewed repository tree:** `616a829a2e0aa168ed711f1ae886f01ea3fc1ac1`  
**Ordinary source payload tree:** `cf730d1b759b587bb20e3191b4de417769ce4053`  
**Active manuscript directory:** `papers/A2-DYN-v52-referee-response`  
**Active mathematical source:** one hundred eleven numbered core modules; revision 52 retains all one hundred nine revision-51 modules and adds modules 110--111  
**Frozen revision-51 author baseline:** `39ee9d88831a574a519785407732b3872ccbca3b`  
**Frozen revision-51 paper tree:** `39ddc1f7c3be0c3010dc1388a5aeddd7789a4075`  
**Controlling report:** `reviews/a2-dyn-v51-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `f3c14d327837289fd44d3824d0447c010565aba2` / `a46a201ebef4fcc56e4b80df5494d7358389e42a`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 52 is a genuine theorem-bearing advance over revision 51. The new work does not claim that the still-uncontrolled positive physical remainder has small essential height, and it does not infer pointwise conditional path convergence by differentiating a fixed-window bridge theorem. Instead it attacks a different obstruction left open by the preceding report: whether the path numerator can be controlled at the same roof coordinate and uniformly over a sufficiently rich class of path tests.

The revision adds two proof modules:

- `core/110_path_valued_raw_inversion.tex`;
- `core/111_same_roof_conditional_bridges.tex`.

Their principal conclusions are as follows.

1. On every protected endpoint chart, the map from the two endpoint contacts to the entire pinned collision path is Lipschitz in the path supremum metric with bound
   \[
   C\varepsilon^{-1}m^{-1/2}.
   \]
   Hence every unit bounded-Lipschitz functional of the whole path is an admissible protected insertion for sufficiently large collision count at each fixed protection scale.

2. For every fixed reconstruction band, the band-limited exact-label path measure factors uniformly in the bounded-Lipschitz dual norm into the scalar arithmetic transition coefficient and the Gaussian collision-bridge law.

3. The complete path-valued raw-density error admits a common positive-remainder representation:
   \[
   \mathbf P_{m,R}^{n,k}(u)
   -G_{m,R}^{n,k}(u)\mathsf W_R
   =\mathbf b_{B,m,R}^{n,k}(u)+O_{\mathrm{BL}^*}(B^{-1/192})
   \]
   after the collision limsup at each fixed large band. The same positive physical path measure works simultaneously for every unit bounded-Lipschitz path test.

4. Integrating the bounded-Lipschitz dual norm over any translated fixed roof interval gives convergence to zero. Thus a bounded-Lipschitz path test may be chosen measurably after the roof value, without differentiating that roof-dependent selection as a source insertion.

5. An exact pinned time change transfers the roof-integrated path-valued local law from the collision clock to the actual return clock.

6. The regular conditional collision- and return-path kernels at their own roof values converge to their Gaussian bridges in mean under the unchanged conditional roof law, and also under the arithmetic reference roof law.

7. The existing scalar positive-height criterion is sufficient for the remaining uniform pointwise bounded-Lipschitz bridge. No second independent path-numerator criterion is left once the scalar physical heights are controlled.

I audited the two new modules, their use in the new leading theorem, the response to the revision-51 report, the proof ledger, the specialist map, the source manifest, and the exact-source qualification records. I found no decisive counterexample, missing section normalization, Fourier-sign error, collision/return endpoint mismatch, unlawful substitution of a count-dependent Fourier band into a fixed-band theorem, or hidden replacement of the original exact return event.

The new chain is mathematically substantial. In particular, the same-roof result is stronger than a bridge law for the mixture over a fixed interval: it controls regular conditional kernels at their own roof coordinate in mean and in conditional roof probability. The path-valued raw law is also stronger than convergence of finitely many path coordinates, because its norm takes a supremum over the full bounded-Lipschitz unit ball on continuous path space.

The negative recommendation is nevertheless forced by the scalar endpoint that continues to organize the title and the raw-inversion architecture. Revision 52 does **not** prove that the positive incidence and clearance remainders have vanishing essential height. It therefore does not prove

\[
\sup_{R,n,k}\operatorname*{ess\,sup}_u
\left|m^2p_{n,R}(k,m,u)
      -\mathcal L_{m,R}(k_1,k_2,u,n)\right|\longrightarrow0,
\]

nor the fixed-radius arithmetic specialization of this two-sided statement. The path theorem shows that this same scalar criterion would also finish the uniform pointwise bridge, but an implication from an unproved criterion is not the missing theorem itself.

The following therefore remain unproved:

- central-scale essential-height smallness of the positive incidence remainder;
- central-scale essential-height smallness of the positive clearance remainder;
- the two-sided pointwise arithmetic raw local limit theorem;
- the full pointwise physical-boundary correction;
- an unconditional uniform same-roof bridge at all positive-reference roofs;
- forward likelihood and forward relative-entropy convergence;
- the unmodulated specialization unless the concrete section-residue criterion is verified;
- and independent specialist certification of the inherited continuum chain.

At the requested benchmark, a paper of this size and title must either complete the scalar two-sided pointwise endpoint or extract a much broader theorem whose independent significance no longer depends on that unfinished endpoint. Revision 52 advances the second-order path consequences and eliminates a separate numerator obstruction, but it does not yet satisfy either alternative.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`4449ba65b59d2670fb1231515e860d874b466b87`.

The repository tree is

`616a829a2e0aa168ed711f1ae886f01ea3fc1ac1`.

The active article is

`papers/A2-DYN-v52-referee-response`.

The ordinary source payload tree is

`cf730d1b759b587bb20e3191b4de417769ce4053`.

The reviewed author commit has the completed revision-51 external-report commit as its parent. This is the correct chronology: the new author revision begins from the frozen review and adds a complete new manuscript tree. It does not modify the reviewed revision-51 author source in place, and it does not use a review commit as though it were mathematical source.

The source manifest records:

- all one hundred nine inherited core modules retained byte-for-byte;
- all one hundred thirty-nine inherited Python files retained byte-for-byte;
- all inherited labels, bibliography, and compiled appendices retained;
- two new core modules, 110 and 111;
- the new active payload tree listed above;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `pointwise_roof_conditioned_bridge_proved: false`;
- `forward_likelihood_convergence_proved: false`;
- and `independent_human_review: false`.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v52-external-top4-review-2026-10-09/`.

No author manuscript source, prior report, workflow, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflows completed successfully on both reviewed branches:

- response branch run `37873837124`;
- referee-copy branch run `37873855553`.

The verifier checks, among other things:

- the frozen revision-51 author tree;
- the controlling revision-51 report blob;
- all one hundred eleven core inclusions;
- byte identity of the one hundred nine inherited core modules and one hundred thirty-nine inherited scripts;
- retention of the inherited appendices, bibliography, and mathematical labels;
- the ordinary-source Merkle identity and workflow hash;
- normal/optimized finite-diagnostic agreement;
- native TeX compilation with stabilized references;
- and theorem-label-based page rendering.

The new finite tests cover exact pinning, Gaussian cross-term cancellation, half-open return-clock identities, the path-measure remainder identity with a sign-changing kernel, finite bounded-Lipschitz norms, numerator normalization, and posterior error charges. Negative controls reject four invalid implications:

1. a scalar local law does not by itself imply conditional path convergence;
2. small positive mass does not imply small essential height;
3. weak path convergence does not imply path-space total variation;
4. a count-dependent Fourier band cannot be substituted into a theorem proved only for each fixed band.

These are useful source, algebra, and regression checks. They do not prove the continuum endpoint influence estimate, infinite-dimensional signed-measure compactness, the inherited anisotropic-space estimates, the physical thin-layer multiplier, the moving spectral charts, the all-depth source decomposition, or the still-missing physical height estimate. The manuscript and validation records state this boundary accurately.

## 4. Scope of this review

I did not attempt to re-prove all one hundred eleven mathematical modules. The substantive audit concerns the new chain intended to answer the revision-51 report:

1. the standard-Borel disintegration of the original exact-label source and the positive physical subsource;
2. the countable bounded-Lipschitz norming class and common roof versions;
3. the endpoint Lipschitz estimate for the entire pinned collision path;
4. admissibility of every unit bounded-Lipschitz path test in the protected correction theorem;
5. construction of a positive band-limited time-domain upper function dominating the signed reconstruction kernel;
6. the fourth-moment estimate for the dominating positive path measures;
7. tightness of total variations of the signed path measures;
8. extension from cylindrical characteristic functions to bounded-Lipschitz norm convergence on continuous path space;
9. the common positive path-remainder identity;
10. the roof-integrated path-valued local-variation theorem;
11. measurable roof-dependent path selectors;
12. the unnormalized pinned return-clock transfer;
13. the same-roof conditional bridge in mean;
14. the exceptional-roof-set corollary;
15. the pointwise path error charge by the physical posterior;
16. the implication from scalar height control to the pointwise actual-return bridge;
17. arithmetic normalization and the order of limits;
18. and source identity and qualification evidence.

The inherited revision-51 chain is treated as the source-pinned baseline. This report does not independently certify every one of the inherited modules on which the new proof depends.

## 5. Path measures, disintegration, and the bounded-Lipschitz norm

Let

\[
\mathcal C=C([0,1],\mathbb R^4)
\]

with the supremum metric, and let \(\mathcal F\) be the real functions with supremum norm and Lipschitz constant at most one. The manuscript defines

\[
\|\sigma\|_{\mathrm{BL}^*}
=\sup_{F\in\mathcal F}|\sigma(F)|.
\]

For a positive finite measure this norm equals its mass, because the constant function one belongs to the test class. For probability measures it is the manuscript's bounded-Lipschitz distance convention. The paper does not call it total variation in path space.

The original exact-label source is disintegrated with respect to its continuous roof coordinate. For almost every roof value \(u\), the manuscript defines

\[
\mathbf P_{m,R}^{n,k}(u)
=m^2p_{n,R}(k,m,u)\mathsf Q_{m,R}^{n,k,u},
\]

where \(\mathsf Q^{u}\) is the conditional law of the pinned collision path. The physical-defect subsource is disintegrated simultaneously, producing a positive finite path measure \(\mathbf b_B(u)\) satisfying

\[
0\le \mathbf b_B(u)\le \mathbf P(u)
\]

as measures and

\[
\mathbf b_B(u)(1)=\mathfrak b_B(u),
\]

the scalar physical remainder of revision 51.

This is the correct measure-valued formulation. In particular, the physical remainder is chosen once from the source and is not selected separately for each test function.

The use of a countable norming class for \(\mathrm{BL}^*\) is appropriate on the separable path space. It permits all scalar density versions needed for the norm to be chosen off one common roof-null set for fixed discrete labels. The manuscript should retain this explicit version argument; without it the essential supremum of a supremum over uncountably many tests would be ambiguous.

I found no source-normalization error here. The factor \(1/c\) already belongs to the original return probability and is not inserted again in the path measures.

## 6. Endpoint control of the entire pinned path

The first new lemma is load-bearing. On a protected endpoint chart, write the endpoint arclengths as \(a,b\) and internal contacts as \(y_j(a,b)\). The prefix action satisfies

\[
dS_j=-p_0\,da+p_j\,dy_j,
\]

with the corresponding terminal formula for \(S_m\). The inherited endpoint-influence estimates give

\[
|dy_j|\le C\varepsilon^{-1}(|da|+|db|)
\]

uniformly in the prefix and collision length.

On a chart with persistent physical word and section decisions:

- every displacement prefix is constant;
- every occupation prefix is constant;
- only the roof coordinate of the centered prefix can vary.

After the path normalization by \(m^{-1/2}\), the complete path map therefore has endpoint Lipschitz constant

\[
C\varepsilon^{-1}m^{-1/2}.
\]

Polygonal interpolation does not enlarge the supremum bound. Composition with a unit bounded-Lipschitz path functional gives a scalar Lipschitz insertion with the same weak endpoint-gradient budget.

This argument correctly avoids differentiating across a physical or section boundary. It also uses the order of limits correctly: for a fixed reconstruction band the protection scale is fixed first, and only then does the collision count tend to infinity. Thus the endpoint budget is eventually below the common admissibility threshold.

Subject to the inherited endpoint-influence theorem, I found this deduction coherent.

The final manuscript should make one point especially visible: constancy of all displacement and occupation prefixes is a statement about one protected word chart with all section decisions fixed. It must not be read as a global continuity statement across cell-label or section boundaries.

## 7. A positive band-limited dominator for the signed kernel

To control the total variation of the signed path measure created by the reconstruction kernel, the manuscript constructs

\[
q(s)=\left(\frac{\sin s}{s}\right)^2
+\left(\frac{\sin(s+\pi/2)}{s+\pi/2}\right)^2.
\]

The two terms do not vanish simultaneously. Moreover,

\[
q(s)\ge \frac{c}{1+s^2},
\]

and its Fourier transform is supported in a fixed compact interval. Since the fixed-band reconstruction kernel is Schwartz, for each fixed band there is a finite constant \(C_B\) such that

\[
C_Bq(s)\ge |K_B(s)|.
\]

This gives a positive, integrable, band-limited roof weight dominating the variation of the signed path measure.

The construction is valid precisely because the band is fixed. No bound on the growth of \(C_B\) is used, and the paper does not substitute \(B=B_m\) into this step.

For readability, I recommend giving this positive dominator a notation distinct from the reconstruction kernel's band notation. The present notation `q_B` can be misread as a rescaling of \(q\), whereas the proof only needs a fixed-band-dependent multiplicative constant.

The Fourier-transform normalization and the fact that the transform is integrable should also be stated once explicitly, because the next fourth-derivative argument uses both compact support and integrability.

## 8. Fourth moments and tightness of the dominating path measures

For the positive path measure weighted by the preceding roof function, the manuscript derives

\[
m^2\int q_B(T_{n,R}-u)
 |\mathcal B_{m,R}(s)-\mathcal B_{m,R}(r)|^4\,d\nu_R^*
\le C_B|s-r|^2.
\]

The scaling is correct. The inherited unnormalized fourth-moment theorem gives an \(O(l^2m^{-2})\) estimate for the fourth power of an unscaled tied increment of length \(l\). Dividing by \(m^2\) for the normalized path and multiplying by the outside \(m^2\) leaves \(O((l/m)^2)\).

The positive roof weight has compactly supported integrable Fourier transform, so the same chronological three-block derivative calculation applies. Centering at each moving spectral peak cancels the linear drift. The four-frequency inverse supplies the natural \(m^{-2}\) coefficient scale.

The paths start at zero, and the fourth-moment exponent is sufficient for tightness in continuous path space. The treatment of finite measures with possibly vanishing mass is also sound: one may add mass at the zero path and normalize by a common mass upper bound before applying the probability tightness criterion.

The variation of the signed reconstruction measure is dominated by this positive tight family. Consequently the total variations are uniformly tight.

This is the key new input beyond finite-dimensional factorization. I did not find a scaling error in it.

## 9. From cylindrical factorization to bounded-Lipschitz norm convergence

For fixed rational observation times and fixed characteristic cylinder tests, the inherited pinned factorization identifies the limiting signed path measure. The exact weighted-frequency identity cancels both the drift term and the mixed Gaussian term on every moving resonance chart. The damped curvature-continuity estimate replaces the chart Hessian by the physical covariance. All occupation resonances remain present.

The manuscript then uses:

- tightness of the total variations;
- convergence of the scalar masses;
- convergence of cylinder characteristic functions;
- determination of finite measures on continuous path space by rational-time cylinders;
- continuity of the Gaussian bridge law in the radius;
- and a finite equicontinuous net for the bounded-Lipschitz unit ball on a compact path set.

These ingredients yield

\[
\|\sigma_m-\sigma_m(1)\mathsf W_R\|_{\mathrm{BL}^*}\to0
\]

uniformly in all targets at each fixed band.

This compactness passage is plausible and, in outline, correct. Because it is one of the genuinely infinite-dimensional steps of the paper, the final version should isolate it as a standalone signed-measure lemma. A clean statement should assume:

1. uniformly bounded total variation;
2. tight total variations;
3. convergence on a determining cylindrical class;
4. convergence of total masses;

and conclude bounded-Lipschitz norm convergence. Writing this abstract lemma once would make clear that no path-space total-variation conclusion is being used.

The proof's use of positive dominating measures is legitimate: if \(|\sigma_m|\le\tau_m\), then \(\tau_m\pm\sigma_m\) are positive and tight. The manuscript should state this domination explicitly at the point where Prokhorov compactness is invoked.

I found no decisive failure in this passage, but it remains an important specialist audit item.

## 10. The common positive path remainder

For a path test \(F\), the complete source identity is

\[
p^F=f^{\varepsilon,F}
+d^{\varepsilon,\varepsilon,F}
+b^{\varepsilon,F}.
\]

Let \(a^F=f^{\varepsilon,F}+d^{\varepsilon,\varepsilon,F}\). The exact error decomposition is

\[
\begin{aligned}
m^2p^F-G\mathsf W_R(F)-m^2b^{\varepsilon,F}
={}&m^2(a^F-K_B*a^F)\\
&+\{m^2K_B*p^F-G\mathsf W_R(F)\}\\
&-m^2K_B*b^{\varepsilon,F}.
\end{aligned}
\]

The three terms are controlled in different ways:

- the smoothly protected term uses the endpoint-gradient budget and contributes \(O(B^{-1/2})\);
- the all-depth decision term is controlled by bounded-source domination and contributes \(O(\varepsilon^{1/16})\);
- the fixed-band path factorization makes the middle term vanish;
- the convolution of the physical remainder is controlled by the revision-51 fixed-convolution lemma and its local-variation bound.

With \(\varepsilon(B)=A_0B^{-1/12}\), the dominant ordered error is

\[
O(B^{-1/192}).
\]

The countable norming class makes the exceptional roof set common, converting the scalar estimates into

\[
\limsup_m\sup_{R,n,k}\operatorname*{ess\,sup}_u
\|\mathbf P(u)-G(u)\mathsf W_R-\mathbf b_B(u)\|_{\mathrm{BL}^*}
\le CB^{-1/192}.
\]

This is a genuine measure-valued strengthening of revision 51. It is important that \(\mathbf b_B\) is one positive path measure, not a family of signed scalar remainders chosen after \(F\).

Integrating and using that the bounded-Lipschitz norm of a positive measure equals its mass gives the roof-integrated theorem after taking the collision limsup first and the reconstruction-band limit last.

I found the sign bookkeeping and order of limits correct.

## 11. Roof-dependent bounded-Lipschitz selectors

The roof-integrated path norm controls measurable functions \(\Psi(u,x)\) for which

\[
\Psi(u,\cdot)\in\mathcal F
\]

at every roof value and whose roof support lies in the translated fixed interval. The selector may depend on all target parameters and may be chosen after observing \(u\).

This follows by evaluating the finite signed path measure at the selected unit bounded-Lipschitz function at each roof value and integrating the path-dual norm. No derivative of the roof-dependent selection is taken.

This is substantially stronger than a theorem for one fixed path test. It remains weaker than a theorem for arbitrary measurable path selectors, since bounded-Lipschitz regularity in path space is essential.

The statement should explicitly retain joint Borel measurability of \(\Psi\). The current prose indicates measurability, but making the product-space condition part of the corollary would remove a minor ambiguity.

## 12. Unnormalized transfer to the actual return clock

The return-clock transfer is carried out before division by a rare-event mass. Let

\[
\lambda_m=(m^2/h)\mathbf1_E\nu_R^*
\]

for the exact discrete event and fixed roof interval. Its mass is uniformly bounded by the scalar fixed-window upper estimate. The inherited unnormalized fourth moment makes the collision-path measures tight even when this mass tends to zero.

At the \(l\)-th actual return, put \(\theta_l=N_{l,R}/m\). The half-open occupation convention gives

\[
A_{N_{l,R},R}=l,\qquad A_{m,R}=n,
\]

and hence

\[
\theta_l-l/n
=-\frac{\sqrt m}{n}(\mathcal B_{m,R})_4(\theta_l).
\]

Tightness of the fourth path coordinate forces the maximum clock displacement to tend to zero in the unnormalized finite measures. The central terminal vector is uniformly bounded on the target class. The exact pinned time-change identity and the modulus of continuity of the tight collision paths then give the coupling of the actual return path with the deterministic linear image of the collision path.

The covariance transformation is the inherited one:

\[
c^{-1}L_R^{-1}\Omega_RL_R^{-\mathsf T}=D_R.
\]

This is the correct passage to the actual return bridge. It changes neither the roof event nor the exact return index.

There is a notation collision in the current proof: `A_{m,R}` is used both for the occupation count and for the deterministic covariance-change matrix \(\sqrt{m/n}L_R^{-1}\). This should be repaired. I recommend reserving \(A_{j,R}\) for the occupation count and using, for example, \(\mathsf A_{m,R}\) for the linear map.

Apart from that notation defect, I found the clock identity and scaling coherent.

## 13. Same-roof conditional convergence in mean

For a fixed interval \(I_t=[t,t+h]\), the target class assumes

\[
|Z(t)|\le M_0,
\qquad
H_m=\int_{I_t}(G(u))_+\,du\ge dh.
\]

The scalar local-variation theorem gives a true mass

\[
F_m=\int_{I_t}P(u)\,du\ge dh/2
\]

for large counts. The original conditional roof law and the reference roof law are

\[
\pi_m(du)=\frac{\mathbf1_{I_t}(u)P(u)}{F_m}\,du,
\qquad
\widehat\pi_m(du)=\frac{\mathbf1_{I_t}(u)(G(u))_+}{H_m}\,du.
\]

The manuscript uses the elementary inequality

\[
P\,d_{\mathrm{BL}}(Q,W)
\le \|PQ-GW\|_{\mathrm{BL}^*}+|P-G|
\le 2\|PQ-GW\|_{\mathrm{BL}^*}.
\]

The second inequality follows because the constant function one is in the bounded-Lipschitz test class. Integrating and dividing by the positive denominator proves convergence in mean under \(\pi_m\). The actual-return statement follows from the integrated clock-transfer lemma.

Replacing \(\pi_m\) by \(\widehat\pi_m\) costs only the scalar probability total-variation distance, since the path distance is bounded. Thus the conclusion is version-independent under both roof laws.

This is a correct use of the actual path numerator. A scalar conditional roof theorem alone would not prove it.

The terminology “same-roof bridge” should continue to be accompanied by the qualification that the objects are regular conditional kernels defined almost everywhere. The theorem does not assign positive probability to the singleton event \(T_{n,R}=u\), and it does not make a statement at every externally prescribed exceptional roof value.

## 14. Asymptotically full roof sets

From uniform convergence of the mean path distances, Markov's inequality produces target-dependent exceptional roof sets whose masses under both \(\pi_m\) and \(\widehat\pi_m\) tend uniformly to zero. Outside those sets, both collision- and return-bridge distances tend to zero along a deterministic qualitative sequence.

This is a useful consequence. It is not a prescribed shrinking-roof resolution and it does not upgrade convergence in roof probability to essential-supremum convergence.

The manuscript states this distinction correctly.

## 15. The pointwise path error charge

On roofs satisfying \(G(u)\ge d\), the revision-51 lower law gives \(P(u)\ge d/2\) eventually. Define the physical-defect posterior

\[
\beta_B(u)=\frac{\mathfrak b_B(u)}{P(u)}.
\]

Let

\[
\mathsf E=\mathbf P-G\mathsf W_R-\mathbf b_B.
\]

Taking masses gives

\[
\mathsf E(1)=P-G-\mathfrak b_B.
\]

The exact identity

\[
P(\mathsf Q-\mathsf W_R)
=\mathbf b_B-\mathfrak b_B\mathsf W_R
+\mathsf E-\mathsf E(1)\mathsf W_R
\]

implies

\[
P\,d_{\mathrm{BL}}(\mathsf Q,\mathsf W_R)
\le 2\mathfrak b_B+2\|\mathsf E\|_{\mathrm{BL}^*}.
\]

After division by the lower denominator, the conditional path error is charged to twice the exact physical posterior plus the ordered \(B^{-1/192}\) error.

This algebra is correct. It proves that the scalar positive-height criterion is sufficient for the uniform collision-path bridge. Tightness and the exact clock identity then give the actual-return bridge under the same condition.

The logical scope is important:

- the path numerator no longer contributes an independent obstruction;
- the scalar positive physical height remains unproved;
- the pointwise bridge is therefore conditional, not established unconditionally.

The manuscript preserves this distinction.

## 16. Arithmetic modulation and normalization

Every uniform assertion retains the finite transition kernel

\[
\mathcal L_{m,R}.
\]

At fixed radius and on central compact sets, this specializes to

\[
c\,\mathfrak a_R(k,n,m)g_{\Omega_R}(Z),
\]

with the equivalent original-return normalization using \(D_R\). No nontrivial section residue is set equal to one.

The path theorems likewise retain all resonance branches. The common positive path remainder is attached to the original exact \((n,k,m)\) source. No return-index packet, substitute section, or averaged collision count is introduced.

The integrated conditional theorem uses a positive integrated reference mass. The pointwise implication separately assumes \(G(u)\ge d\). These two lower conditions are not conflated.

I found no missing factor of \(c\) or covariance transformation error in the new modules.

## 17. What revision 52 does and does not close

Revision 52 closes a genuine path-numerator issue.

Before this revision, one had:

- scalar local variation on fixed roof windows;
- a one-sided scalar essential-supremum lower law;
- interval-conditioned bridges under denominator hypotheses;
- but no path-valued raw numerator at each roof and no proof that the scalar height criterion alone would finish the pointwise bridge.

The new revision supplies:

- bounded-Lipschitz path-valued raw local variation;
- a common positive physical path remainder;
- same-roof regular conditional bridge convergence in mean;
- convergence outside roof sets of vanishing conditional probability;
- and sufficiency of the scalar positive-height criterion for the uniform pointwise bridge.

It does **not** supply:

- small essential height of the incidence source;
- small essential height of the clearance source;
- the upper half of the scalar pointwise density theorem;
- the full two-sided raw local limit theorem;
- an unconditional pointwise bridge at every positive-reference roof;
- path-space total variation;
- arbitrary measurable-path-selector Gaussian amplitudes;
- a polynomial rate in the collision count;
- a proof that the arithmetic factor is identically one;
- or independent human verification.

The source manifest and publication-status record distinguish these items honestly.

## 18. The decisive remaining scalar obstruction

The central unresolved condition is

\[
\lim_{B\to\infty}\limsup_{m\to\infty}
\|\mathfrak b_{B,m}\|_{\infty,M}=0,
\]

or, equivalently, the separate vanishing of the positive incidence and clearance heights.

Revision 51 showed that the complete scalar density error is uniformly approximated by this nonnegative physical remainder. Revision 52 shows that the complete path-density error is approximated by the corresponding positive path measure and that its scalar mass controls the pointwise conditional path error.

Thus the remaining obstacle is now sharply isolated. It is also plainly not cosmetic. A positive remainder can have arbitrarily small local mass and arbitrarily large height on a very narrow roof set. Neither local variation, reverse likelihood, nor convergence in conditional mean excludes such spikes.

Until those positive heights are bounded at the natural \(m^{-2}\) scale, the advertised two-sided pointwise raw theorem is not proved.

## 19. Independent specialist verification

The new modules add several continuum obligations to the already long inherited audit list.

The following points require detailed human checking:

1. the first-variation formula for every prefix roof on a full protected word;
2. the word-length-uniform internal-contact response used in the whole-path endpoint bound;
3. constancy of all discrete prefixes on the protected endpoint charts;
4. weak differentiability of Lipschitz path insertions and compatibility with the protected correction theorem;
5. the positive two-sinc-square dominator and its Fourier normalization;
6. the extension of the chronological fourth-derivative calculation to the dominating positive roof test;
7. tightness of finite path measures with possibly vanishing mass;
8. total-variation tightness of the signed reconstruction measures;
9. determination of signed measures by rational-time cylinder characteristic functions;
10. the passage from cylindrical convergence to bounded-Lipschitz norm convergence;
11. simultaneous disintegration of the original source and positive physical subsource;
12. the common-null-set construction for the path dual norm;
13. the endpoint-gradient budget uniformly over the full path-test class;
14. the exact source identity with path insertions;
15. the unnormalized pinned return-clock transfer;
16. the regular conditional-kernel version arguments;
17. the pointwise posterior charge;
18. and all inherited thin-layer, moving-peak, full-torus, protected, and all-depth decision estimates.

The successful workflows and finite diagnostics do not certify these continuum steps. No independent specialist audit has been obtained.

## 20. Novelty and the requested venue standard

The manuscript correctly avoids claiming that Gaussian bridges or bounded-Lipschitz weak convergence are new in isolation. Existing billiard and suspension local-limit theories already organize many fixed-table spatial, endpoint, and flow local limits.

The distinctive content of the present program is the conjunction of:

- the actual four-coordinate first-return record;
- exact return and collision indices;
- the finite arithmetic transition kernel;
- complete unprotected roof densities;
- physical incidence and clearance layers;
- all-depth source decompositions;
- translation-uniform local density variation;
- a one-sided pointwise lower theorem;
- and now a path-valued raw numerator and same-roof conditional kernels.

This is a serious specialist contribution. The new path-valued theorem is not a formal corollary of the scalar theorem, because it requires uniform tightness and compactness over an infinite-dimensional test class.

Nevertheless, the overall result remains concentrated in one triangular finite-horizon Lorentz family and depends on a very large model-specific proof architecture. The abstract part newly isolated in revision 52—endpoint path Lipschitz control plus tight signed-measure factorization—is useful, but it is not yet formulated and demonstrated as a broad theorem with multiple independent applications.

At the requested four-journal level, the unresolved scalar pointwise endpoint and the absence of a broad independent general theorem remain decisive.

## 21. Submission architecture

The front matter now presents three principal layers more clearly:

1. the complete scalar local-variation theorem;
2. the one-sided scalar essential-supremum theorem;
3. the path-valued raw and same-roof conditional theorem.

This hierarchy is substantially better than a cumulative list of every historical milestone.

The article is still exceptionally large. The shortest logical route to the new theorem depends on a chain spanning physical geometry, anisotropic transfer operators, arithmetic resonances, protected inversion, all-depth decisions, physical local variation, positive remainders, and path compactness.

For a future submission, the authors should choose one unmistakable principal endpoint.

- If the current raw-inversion title and architecture are retained, the positive incidence and clearance heights should be closed and the two-sided pointwise theorem stated as the principal result.
- If the scalar pointwise endpoint remains open, the completed local-variation, lower-law, path-valued, and same-roof-in-mean theorems should be presented as a focused specialist paper, with the unfinished essential-height program clearly separated from the main editorial claim.

This is not a recommendation to discard valid mathematics. It is a recommendation to align the title, abstract, theorem hierarchy, and proof burden with the strongest theorem actually established.

## 22. Required changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

1. **Control the positive incidence height.**  
   Prove the central-scale essential-supremum smallness of the first-incidence physical remainder at the natural \(m^{-2}\) density scale.

2. **Control the positive clearance height.**  
   Prove the corresponding essential-height estimate for the competing-hit clearance remainder, without transporting trajectories across a physical seam.

3. **Complete the two-sided arithmetic raw theorem.**  
   Combine those estimates with the existing transition kernel and retain the arithmetic residue unless it is independently proved trivial.

4. **Upgrade the pointwise bridge unconditionally.**  
   Once the scalar criterion is proved, invoke the revision-52 path charge and clock transfer to state the actual same-roof bridge as a theorem rather than an implication.

5. **Resolve the concrete section arithmetic or keep it intrinsic.**  
   Either prove the section phase masses are uniform or retain \(\mathfrak a_R\) and \(\mathcal L_{m,R}\) in the final principal statements.

6. **Obtain independent specialist review.**  
   The physical thin-layer multiplier, full occupation spectrum, moving peaks, all-depth source bounds, endpoint path budget, and infinite-dimensional compactness passage require expert verification.

7. **Extract a reusable path-valued principle.**  
   Formulate abstract hypotheses under which scalar exact-label local inversion, endpoint path regularity, and a positive remainder imply bounded-Lipschitz path-valued local laws and same-roof conditional convergence.

8. **Provide independent applications if claiming broad significance.**  
   A second singular hyperbolic model or a genuine family theorem would materially strengthen the top-four case.

9. **Reduce the proof burden.**  
   Separate source-verification infrastructure and historical pipeline material from the shortest complete mathematical route.

10. **Keep all topology distinctions explicit.**  
    Continue to separate path bounded-Lipschitz convergence, roof total variation, scalar essential supremum, and path-space total variation.

## 23. Technical and presentation comments

1. Rename the deterministic matrix currently denoted `A_{m,R}` in the return-clock proof; that symbol is already used for occupation count.
2. State the exact Fourier-transform normalization of the positive two-sinc-square dominator.
3. Record explicitly that its Fourier transform is integrable as well as compactly supported.
4. Give the fixed-band-dependent dominator a notation distinct from the reconstruction-band scaling notation.
5. Isolate the signed-measure compactness argument as an abstract lemma.
6. State explicitly that the positive dominating measure bounds the total variation of the signed reconstruction measure.
7. Include joint Borel measurability in the roof-dependent-selector corollary.
8. Retain the countable norming-class argument and the common roof-null set.
9. Keep the path metric and bounded-Lipschitz normalization fixed throughout.
10. Continue to state that path-space total variation is not proved.
11. Keep the reconstruction band fixed before every collision limit.
12. Do not infer any estimate at `B=B_m` from the fixed-band factorization.
13. Distinguish the reconstruction band from every auxiliary spectral band.
14. State central enlargement explicitly when a fixed interval around `t` is used under a compact bound on `Z(t)`.
15. Keep `G` and `(G)_+` distinct: the raw signed reference uses `G`, while the conditional reference roof probability uses `(G)_+`.
16. Preserve the almost-everywhere meaning of same-roof conditional kernels.
17. Do not describe convergence in conditional mean as convergence at every prescribed roof value.
18. Keep the scalar positive-height condition visibly conditional in every pointwise path corollary.
19. Preserve the order `m -> infinity` first and `B -> infinity` second in the path charge.
20. Continue to state that the physical path remainder is common to all tests.
21. Keep the source normalization `nu_R^*=c^{-1}nu|_{Y_R^*}` visible near every source enlargement.
22. Retain the exact half-open occupation convention in the clock proof.
23. State that the return index and roof value are unchanged throughout the disintegration and time change.
24. Keep arbitrary bounded-Lipschitz path selectors separate from arbitrary measurable path selectors.
25. Preserve the distinction between reverse likelihood results from revision 51 and the still-unproved forward likelihood bounds.
26. Continue to separate source qualification from continuum proof certification.

## 24. Final assessment

Revision 52 is a serious and constructive response to the preceding report.

It proves a uniform endpoint budget for the entire pinned path, extends fixed-band factorization from cylinder tests to the full bounded-Lipschitz path class, constructs a common positive physical path remainder, obtains roof-integrated path-valued local variation, transfers the result to the actual return clock, and proves same-roof regular conditional bridge convergence in mean. It also shows that the already isolated scalar positive-height criterion is sufficient for the remaining pointwise bridge, so no separate path-numerator obstruction survives.

I found no decisive error in the new modules, subject to the inherited continuum inputs and the specialist checks identified above.

The central top-four objection nevertheless remains. The manuscript still permits narrow positive incidence or clearance spikes. It therefore lacks the upper half of the pointwise density theorem, the full two-sided raw local limit, and an unconditional uniform pointwise bridge. The new path consequences, while mathematically meaningful, do not replace the missing scalar theorem that continues to govern the title and overall editorial claim.

Subject to independent specialist verification, the local-variation theorem, one-sided lower law, path-valued raw theorem, and same-roof bridge in mean could support a strong focused dynamics/probability submission. At the requested four-journal benchmark, however, the remaining scalar endpoint and the model-specific proof burden are decisive.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
