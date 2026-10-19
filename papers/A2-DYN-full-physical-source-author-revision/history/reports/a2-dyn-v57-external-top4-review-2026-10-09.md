# External top-four referee report on A2-DYN revision 57

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v57-referee-response-2026-10-09`, `revision/a2-dyn-v57-referee-copy-2026-10-09`  
**Reviewed commit:** `8dbfac97a74e2b498c77d1afd663dd1e7db18c91`  
**Reviewed repository tree:** `c0e04694ea5ec6df226a4e400fa7058bdabcd1f1`  
**Ordinary source payload tree:** `e4091eb88fe8786d45a0d9fc9047d5bdba890105`  
**Active manuscript directory:** `papers/A2-DYN-v57-referee-response`  
**Active mathematical source:** one hundred twenty-two numbered core modules; revision 57 retains all one hundred twenty revision-56 modules and adds modules 121--122  
**Frozen revision-56 author baseline:** `4292877a5100c4c22975d9d563a1c54793139db4`  
**Frozen revision-56 complete paper tree:** `c3210ca54af8edb21aa048796172a13832d1335f`  
**Controlling external report:** `reviews/a2-dyn-v56-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `f3d5a8a6238497950ecde6c6f276e3c80624fc4a` / `01e36e830daee2b04036320b562990f9daf47485`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 57 is a genuine and mathematically substantial advance over revision 56. The preceding report accepted a complete local variation theorem and a common all-resolution good-roof localization, but emphasized that those results neither controlled the tails of the moving arithmetic reference nor removed the incidence and clearance height obstruction. Revision 57 resolves the first of these two issues.

The new manuscript proves, uniformly in the radius, that the evaluated finite arithmetic transition kernel has a Gaussian envelope centered at the physical mean throughout changes of arithmetic type. It then combines this reference tightness with the inherited full-source local variation theorem and the actual fourth-moment estimate to obtain

\[
 \sum_{m\ge n}\sum_{k\in\mathbb Z^2}\int_0^\infty
 \left|p_{n,R}(k,m,u)-m^{-2}\mathcal L_{m,R}(k_1,k_2,u,n)\right|\,du
 \longrightarrow0.
\]

Thus the original exact return law is approximated in total variation on its **entire untruncated mixed record space**. No collision label, displacement label, positive roof value, central cutoff, return-index average or source guard remains in the final measure statement.

The second new module proves a joint observation/path result. The collision bridge and actual-return bridge are not treated as independent limits: the reference is the graph law

\[
 \mathsf H_R=\operatorname{Law}(\mathbb B_{\Omega_R},A_R\mathbb B_{\Omega_R}),
 \qquad A_R=c^{-1/2}L_R^{-1},
\]

and the complete record is asymptotically independent of this internally coupled bridge pair in observation variation and path bounded-Lipschitz dual. The result contracts through arbitrary record-only Markov observation kernels and gives correct mass-budget bounds after conditioning on the full output event.

I audited the new modules

- `core/121_pressure_controlled_transition_tails.tex`;
- `core/122_coupled_global_record_bridges.tex`;

and their use in the revised front matter. I also checked the relevant inherited definitions of the moving peak data, the transition kernel, the full-source local variation theorem, the fourth moment, the collision path numerator, the actual clock coupling, the positive-part normalization and the exact-source qualification records.

I found no decisive counterexample, missing power of the collision count, covariance-Jacobian error, Fourier-sign error, false independence step, invalid growing-band substitution or normalization-factor error in the new chain. In particular:

1. the centered positive pressure has no linear term and is bounded by `C|t|^2`;
2. physical smooth branch pairings, rather than possibly vanishing section amplitudes, are used to dominate each visible branch;
3. the optimizing imaginary tilt gives `|mu_j-mu_R|^2 <= C kappa_j`;
4. the damping and moving-center displacement combine into one physical-mean Gaussian envelope;
5. the `O(n^2)` number of central unit cells is exactly paid by the `m^{-2}` local scaling when `m` is comparable with `n`;
6. the true fourth moment and reference Gaussian tails close the passage from local to global variation;
7. replacing the signed transition kernel by its positive part decreases the error against the positive true law;
8. the bridge pair is obtained from a joint clock coupling, not inferred from two marginal limits;
9. record-only observation kernels contract the stated mixed norm; and
10. the postselection theorem retains the complete selection output and requires its reference mass to dominate the qualitative approximation error.

These results are significant within the manuscript's program. The negative recommendation is therefore not based on failure of the new global theorem.

It is instead forced by the endpoint that still governs the title, the retained pointwise architecture and the claimed top-four benchmark. Revision 57 explicitly does **not** prove the essential-height smallness of either positive physical defect source. Consequently it does not prove the unrestricted two-sided pointwise arithmetic raw-density theorem, unrestricted same-roof bridges, forward essential likelihood convergence or the full pointwise roof-conditioned path theorem.

Total variation on the complete mixed record is an integrated statement. A positive density spike may have vanishing mass and arbitrarily large essential height. The new Gaussian reference tail does not alter this logical distinction. The manuscript states the distinction accurately, but it remains mathematically decisive.

At the requested benchmark, the article would need either

1. completion of the unrestricted pointwise raw theorem that organizes its title and much of its 122-module proof architecture; or
2. a substantially broader theorem of independent significance, with multiple genuinely different singular-hyperbolic realizations, so that the paper no longer depends editorially on the unfinished pointwise endpoint.

Revision 57 supplies neither yet. Its new pressure comparison is useful and apparently coherent, but is proved only for the existing occupation-peak structure of this highly specialized Lorentz program. No independent human specialist audit has been obtained.

My mathematical assessment is therefore strongly positive about the new integrated theorem and cautious about the inherited continuum chain, but negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`8dbfac97a74e2b498c77d1afd663dd1e7db18c91`.

The repository tree at that commit is

`c0e04694ea5ec6df226a4e400fa7058bdabcd1f1`.

The active article is

`papers/A2-DYN-v57-referee-response`.

The ordinary source payload tree recorded in the manifest is

`e4091eb88fe8786d45a0d9fc9047d5bdba890105`.

The author commit has the revision-56 review commit

`f3d5a8a6238497950ecde6c6f276e3c80624fc4a`

as its parent. The chronology is therefore correct: revision 57 starts from the frozen external assessment and adds a new author manuscript rather than modifying the reviewed revision-56 source in place.

The source manifest records:

- all one hundred twenty inherited core modules retained byte-for-byte;
- all one hundred fifty-nine inherited Python files retained byte-for-byte;
- the bibliography and compiled appendices retained;
- every inherited mathematical label retained;
- two new modules, 121 and 122;
- `pressure_drift_damping_proved: true`;
- `global_transition_gaussian_envelope_proved: true`;
- `untruncated_mixed_TV_proved: true`;
- `joint_collision_return_graph_bridge_proved: true`;
- `record_observation_postselection_proved: true`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `arithmetic_factor_identically_one_proved: false`;
- and `independent_human_review: false`.

The former three leading statements and the complete revision-56 post-title front matter remain compiled in `appendices/v56_frontmatter.tex`. The former full main source and status material are archived under provenance. No inherited theorem is deleted, and the original exact physical source, half-open occupation convention, next-collision clearance convention, finite arithmetic transition kernel and unrestricted pointwise target remain in the manuscript.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v57-external-top4-review-2026-10-09/`.

No author manuscript source, prior review, workflow, historical manuscript or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflows completed successfully on both reviewed author refs:

- response branch run `37915773999`;
- referee-copy branch run `37915793125`.

The runs bind the source archive, verification, finite diagnostics, native TeX build and rendered theorem pages to the exact reviewed SHA.

According to the validation record, the verifier checks

- the frozen revision-56 paper tree and controlling report blob;
- all 120 inherited core modules;
- all 159 inherited Python scripts;
- inherited appendices, bibliography and mathematical labels;
- the exact moved front matter and twelve provenance archives;
- the ordinary-source Merkle identity;
- the read-only workflow hash;
- agreement of normal and optimized finite diagnostics;
- native TeX compilation with warnings and overfull boxes rejected;
- and theorem-label-based rendering.

The new finite checks cover rational tilt optimization, the damping/Gaussian energy inequality, accretive complex matrices, covariance Jacobians, finite count sums, signed positive-part normalization, observation-channel contraction and conditional total-variation factors. Negative controls retain continuity-only drift escape, narrow high spikes, dependent versus independent bridge marginals and rare events whose mass is smaller than the approximation error.

These checks are useful source and algebra evidence. They do not certify

- the inherited occupation spectrum;
- the physical thin-source geometry;
- existence and continuity of nonzero complex visible-branch pairings;
- the pressure domination on the anisotropic continuum operator;
- the complete first-physical-defect source partition;
- the local raw-variation theorem;
- the joint collision-to-return clock coupling;
- the incidence or clearance essential-height estimates;
- or any independent human proof audit.

The manuscript and validation files state this boundary accurately.

## 4. Scope of this review

I did not attempt to re-prove all 122 core modules. The substantive audit concentrates on the additions and on the inherited inputs which can change the revision-56 assessment:

1. the centered real exponential moment and its leading eigenvalue;
2. the use of full-collision smooth witnesses for each peripheral branch;
3. scalar continuity where the section amplitude may vanish;
4. centering of the branch logarithm and the imaginary-tilt derivative;
5. the uniform optimization giving squared drift bounded by damping;
6. the complex Gaussian normalization for accretive symmetric Hessians;
7. summation of every displacement and collision label and integration over the full roof;
8. the reference tail in the return-centered variables;
9. the true fourth-moment tail;
10. the exact local-to-global counting and `m^{-2}` scaling;
11. positive-part normalization of a signed finite transition density;
12. the fixed-radius arithmetic specialization;
13. the joint collision/return clock coupling;
14. graph pushforward of the collision bridge numerator;
15. common roof disintegration and measurable path test selection;
16. globalization of the joint path law;
17. contraction through record-only Markov kernels;
18. normalization after the full output selection event;
19. preservation of arithmetic zero classes;
20. source qualification and the unchanged pointwise obstruction.

The inherited revision-56 and earlier continuum chain is treated as a source-pinned baseline, not as independently certified mathematics.

## 5. The centered positive pressure

The new centered observable is

\[
 X_R=\mathsf f_R-\mu_R,
 \qquad \mu_R=(0,0,\bar\tau_R,c).
\]

The manuscript uses the analytic full occupation operator at an imaginary frequency. On a common small complex ball it writes

\[
 \int e^{-t\cdot S_mX_R}\,d\nu
 =\lambda_{0,R}(it)^m A_{0,R}(it)+O(\rho^m).
\]

At `t=0` the amplitude equals one. For real small `t`, the operator and its simple leading eigendata are real, so the eigenvalue and amplitude are real; continuity makes the amplitude positive and bounded away from zero. The eigenvalue is close to one and exceeds the complementary radius.

Jensen's inequality gives

\[
 \int e^{-t\cdot S_mX_R}\,d\nu\ge1
\]

because the observable is centered. If the leading eigenvalue were strictly below one, the displayed splitting would tend to zero, contradicting this bound. Thus the leading eigenvalue is at least one. Defining

\[
 \mathscr P_R(t)=\log\lambda_{0,R}(it)
\]

gives a nonnegative pressure.

Centering removes the linear term. Uniform analyticity on a fixed complex ball gives

\[
 0\le\mathscr P_R(t)\le C|t|^2.
\]

The remainder can be absorbed because the leading eigenvalue is at least one. I find this argument coherent. It uses only a fixed complex neighborhood and does not evaluate a growing frequency band.

The load-bearing inherited input is the exact positive physical pairing for the centered full occupation twist, together with a uniform simple splitting. This requires specialist verification; finite matrix diagnostics cannot establish it.

## 6. Physical witnesses for a visible branch

The drift estimate cannot rely on the section endpoint amplitude `B_j`, since that amplitude may vanish at a resonance. The revision correctly chooses bounded smooth initial and terminal functions `a,d` on the full collision space whose pairing with the rank-one peripheral projection is nonzero.

Such witnesses exist if the inherited physical representation of the projection is correct. Smooth functions are dense in the relevant physical `L^2` pairing, and a nonzero rank-one projection cannot annihilate every smooth initial-terminal pair.

The scalar-continuity argument for the section amplitude is then repeated for this pair. Finite-time physical pairings are continuous in the parameter. Dividing by the isolated leading eigenvalue and taking the large-time limit gives a continuous analytic branch amplitude, which stays bounded away from zero in a smaller neighborhood.

The proof covers the zero-damping locus by finitely many such neighborhoods. On the remaining compact part of a peak support, the damping has a positive minimum and the drift is bounded.

This is the right way to avoid a hidden nonzero-residue assumption. A specialist should nevertheless check, chart by chart, that

- the selected projection has the asserted bounded physical representative;
- the smooth witnesses remain admissible for the exact complex pairing;
- the complementary contour stays uniformly below the centered branch on the chosen neighborhood; and
- the local finite cover is compatible with the fixed peak partition used in the transition kernel.

I found no written contradiction in these steps.

## 7. Drift controlled by damping

The centered branch is

\[
 \widetilde\lambda_j(R,z)=e^{-iz\cdot\mu_R}\lambda_j(R,z).
\]

At a moving real maximum `a_j`, write

\[
 \kappa_j=-\log|\lambda_j(R,a_j)|,
 \qquad v_j=\mu_j-\mu_R.
\]

The exact physical pairing at `z=a_j+it` is bounded in modulus by the positive exponential moment of `X_R`. Taking `m`th roots and using the nonzero branch amplitude gives

\[
 \operatorname{Re}\log\widetilde\lambda_j(R,a_j+it)
 \le\mathscr P_R(t).
\]

At the real maximum the centered logarithmic gradient is `iv_j`. Uniform complex Taylor expansion therefore gives

\[
 -\kappa_j-v_j\cdot t\le C_1|t|^2.
\]

The drifts are uniformly bounded on the compact chart supports. After enlarging `C_1`, the tilt

\[
 t=-\frac{v_j}{2C_1}
\]

lies in the fixed complex neighborhood. Substitution yields

\[
 |v_j|^2\le4C_1\kappa_j.
\]

On the complement of the finite neighborhoods of the zero-damping locus, compactness supplies a positive damping minimum and the same conclusion with a larger constant.

The sign in this optimization is correct. Evaluating an analytic logarithm at `a_j+it` turns the purely imaginary real-frequency gradient `iv_j` into the real linear term `-v_j\cdot t`. The proof does not confuse parameter differentiation with frequency differentiation.

This squared-drift estimate is the genuinely new spectral statement of revision 57. Continuity alone would not suffice because the moving displacement is multiplied by `sqrt(m)`.

## 8. Complex Gaussian envelope

The moving peak Hessians are complex symmetric matrices with uniformly positive real part and uniformly bounded norm. For such a matrix `H`, the Gaussian inverse is

\[
 G_H(z)=(2\pi)^{-4}\int_{\mathbb R^4}
 e^{-iv\cdot z-v^{\mathsf T}Hv/2}\,dv.
\]

Analytic continuation of completion of the square gives

\[
 G_H(z)=(2\pi)^{-2}(\det H)^{-1/2}
 e^{-z^{\mathsf T}H^{-1}z/2}.
\]

For real `z`, if `w=H^{-1}z`, then

\[
 \operatorname{Re}(z^{\mathsf T}H^{-1}z)
 =\operatorname{Re}(w^*H^*w)
 \ge a_0|w|^2
 \ge \frac{a_0}{A^2}|z|^2.
\]

The singular values of `H` are bounded below by `a_0`, so the determinant prefactor is uniformly bounded. Hence

\[
 |G_H(z)|\le Ce^{-a|z|^2}.
\]

For the `j`th transition summand set

\[
 Z=\frac{y-m\mu_R}{\sqrt m},
 \qquad d_j=\sqrt m(\mu_j-\mu_R).
\]

Its modulus is bounded by

\[
 C e^{-m\kappa_j-a_1|Z-d_j|^2}.
\]

The new drift estimate gives `|d_j|^2<=C_Dm kappa_j`. Since

\[
 |Z|^2\le2|Z-d_j|^2+2C_Dm\kappa_j,
\]

the two exponent terms dominate a fixed multiple of `|Z|^2`. Summing the finite peak family therefore yields

\[
 |\mathcal L_{m,R}(y)|+|\mathcal K_{m,R}(y)|
 \le C\exp\left(-a\frac{|y-m\mu_R|^2}{m}\right).
\]

I find the completion-of-square and damping absorption correct.

## 9. Summation of the complete transition reference

The normalized reference density is

\[
 \gamma_{n,R}(k,m,u)=m^{-2}\mathcal L_{m,R}(k_1,k_2,u,n),
 \qquad m\ge n,\ u>0.
\]

Summing the two displacement Gaussians contributes `Cm`. Integrating the roof Gaussian contributes `Csqrt(m)`. The factor `m^{-2}` therefore leaves, at each collision count,

\[
 C m^{-1/2}
 \exp\left(-a\frac{(n-cm)^2}{m}\right).
\]

On the central count range `m` comparable with `n`, the resulting discrete Gaussian sum is bounded. On the lower outer range, `n-cm` is a fixed positive fraction of `n`, so the total is exponentially small in `n`. On the upper outer range, `cm-n` is a fixed positive fraction of `m`, so the remaining series is exponentially summable.

Thus the total variation mass of the signed reference is uniformly bounded.

For the return-centered variables

\[
 V_{n,R}(k,m,u)=rac{(k_1,k_2,m-n/c,u-n\bar\tau_R/c)}{\sqrt n},
\]

the central count range gives a uniformly invertible linear relation between `V` and `Z=(y-m mu_R)/sqrt(m)`. Spending part of the Gaussian exponent therefore yields

\[
 \int_{|V|>M}|\gamma_{n,R}|\le Ce^{-aM^2}+Ce^{-an}.
\]

No central cutoff remains in the definition of the reference.

## 10. From local variation to the full mixed law

The inherited local theorem states, on every unit roof interval,

\[
 \int_I\left|m^2p_{n,R}(k,m,u)
      -\mathcal L_{m,R}(k_1,k_2,u,n)\right|du\le e_m,
 \qquad e_m\to0,
\]

uniformly in `R,n,k` and the interval location.

On a fixed return-centered compact set, `m=n/c+O(sqrt(n))`, hence `m` is comparable with `n`. There are

- `O(n)` displacement labels;
- `O(sqrt(n))` collision-count labels; and
- `O(sqrt(n))` unit roof intervals for each discrete pair.

The total number of unit cells is therefore `O(n^2)`. Passing from the normalized density to the original density contributes `m^{-2}`, which is `O(n^{-2})` on this region. Hence the central integrated error is bounded by

\[
 C_M\sup_{m\ge a_Mn}e_m\to0.
\]

The manuscript's compressed proof is consistent with this calculation. In a final journal version, I recommend writing the `m^{-2}` factor and the `O(n^2)` cell count in the same display, since omitting either from the prose can make the summation appear dimensionally incorrect.

The true tail follows from

\[
 \int|J_{n,R}-n\bar G_R|^4d\nu_R^*\le Cn^2,
\]

which gives an `O(M^{-4})` bound outside `|V|<=M`. The reference tail is Gaussian. Letting first `n` tend to infinity and then `M` tend to infinity proves the complete `L^1` convergence.

I find no missing power of `n` in this passage.

## 11. Positive-part normalization

The evaluated transition kernel can be signed at finite count. The probability reference is therefore the normalized positive part

\[
 d\mathsf A_{n,R}
 =\frac{(\gamma_{n,R})_+}{Z_{n,R}^{\rm ref}}d\zeta,
 \qquad Z_{n,R}^{\rm ref}=\int(\gamma_{n,R})_+d\zeta.
\]

Because the true density `p` is nonnegative,

\[
 |p-\gamma_+|\le|p-\gamma|
\]

pointwise. Therefore the complete `L^1` error bounds both

\[
 |Z_{n,R}^{\rm ref}-1|
\]

and the negative mass of the signed transition reference. Normalization adds at most one further copy of the mass discrepancy. With probability total variation defined as one half of variation mass, the stated bound

\[
 d_{\rm TV}(\mathsf P_{n,R},\mathsf A_{n,R})\le E_n
\]

is correct.

The positive reference is a finite-count probability approximation. It does not assert that the signed transition kernel is pointwise nonnegative or that every arithmetic class has positive mass.

## 12. Fixed-radius arithmetic specialization

At fixed radius the transition kernel reduces on central sets to the finite residue factor times the Gaussian with covariance `D_R`. The covariance change satisfies

\[
 \Omega_R=cL_RD_RL_R^{\mathsf T},
 \qquad \det L_R=c.
\]

Consequently

\[
 g_{\Omega_R}(\sqrt cL_Rv)=c^{-3}g_{D_R}(v).
\]

Together with `m/n->c^{-1}`, this converts the transition scale to

\[
 n^{-2}\mathfrak a_R(k,n,m)g_{D_R}(V_{n,R}).
\]

The finite residue is bounded, nonnegative and retains zero classes. Its Gaussian tail permits the same local-to-global argument and normalization.

The arithmetic factor has not been replaced by one. This is mathematically necessary unless the separate concrete zero-residue criterion is proved.

## 13. The joint collision/return bridge

The two paths are constructed from the same trajectory. The correct limit is therefore a graph coupling, not a product of independent bridge laws.

The inherited clock-coupling identity controls

\[
 \mathcal Y_{n,R}-A_{m,n,R}\mathcal B_{m,R},
 \qquad A_{m,n,R}=\sqrt{m/n}\,L_R^{-1},
\]

under the finite positive local source. On central targets `n/m=c+O(m^{-1/2})`, so

\[
 A_{m,n,R}\to A_R=c^{-1/2}L_R^{-1}
\]

uniformly.

Uniform path tightness permits this deterministic linear map to be replaced on the source. The graph map

\[
 x\mapsto(x,A_Rx)
\]

is uniformly Lipschitz. Pushing the inherited collision-path numerator through it therefore gives the local pair numerator with reference

\[
 \mathsf H_R=\operatorname{Law}(\mathbb B_{\Omega_R},A_R\mathbb B_{\Omega_R}).
\]

The covariance identity gives `A_R Omega_R A_R^T=D_R`, so the second marginal is the actual-return bridge covariance.

This argument uses a joint trajectory coupling. It does not infer a joint limit from two marginal bridge theorems, and it does not sample the two Gaussian paths independently.

## 14. Common disintegration and the mixed norm

The paper uses one regular disintegration of the path pair conditional on the complete observed record. The observation labels are countable and the roof is standard Borel. A countable norming class for the path bounded-Lipschitz unit ball fixes common versions outside one null set for each discrete label.

The mixed norm is

\[
 \|\sigma\|_{\mathrm{obs},\mathrm{BL}}
 =\sup_\phi\left|\int\phi(z,x,y)d\sigma\right|,
\]

where `phi` is measurable in the observation and is a unit bounded-Lipschitz function in the two paths on each fiber.

For a disintegrated signed measure this equals the integral of the fiber dual norms. The upper inequality is immediate. The lower inequality follows by measurable selection from the countable norming class.

This norm is variation mass in the observation variable and bounded-Lipschitz dual in the path pair. It is **not** path-space total variation.

The common-version construction is essential because the test may depend measurably on every exact record label. The manuscript handles this correctly.

## 15. Globalization of the coupled bridge law

On a fixed return-centered compact set, the same `O(n^2)` unit-cell count and `m^{-2}` normalization used for the scalar law apply to the local path numerator.

Outside that region, a positive finite path measure has bounded-Lipschitz dual norm equal to its mass because the constant function one is admissible. Therefore the joint integrand is bounded by

\[
 p_{n,R}+|\gamma_{n,R}|.
\]

The true fourth-moment tail and the reference Gaussian tail close the discarded region. This proves the untruncated joint error

\[
 \epsilon_n=\sup_R\int
 \|p_{n,R}(z)\mathsf T_{n,R}^z
       -\gamma_{n,R}(z)\mathsf H_R\|_{\mathrm{BL}_2^*}d\zeta
 \to0.
\]

Replacing a negative scalar reference fiber by zero decreases the error against the positive true fiber. The constant test controls the reference mass. After normalizing the positive part, the complete joint law differs from

\[
 \mathsf A_{n,R}\otimes\mathsf H_R
\]

by at most two copies of the unnormalized error.

The statement that the record is asymptotically independent of the bridge pair is therefore correct in the stated mixed topology. The two paths inside the pair remain deterministically coupled in the limit.

## 16. Conditional pair bridge in mean

Pointwise in the common disintegration,

\[
 p\|Q-H\|_{\mathrm{BL}_2^*}
 \le\|pQ-gH\|_{\mathrm{BL}_2^*}+|p-g|.
\]

The constant path test gives

\[
 |p-g|\le\|pQ-gH\|_{\mathrm{BL}_2^*}.
\]

Hence

\[
 p\|Q-H\|_{\mathrm{BL}_2^*}
 \le2\|pQ-gH\|_{\mathrm{BL}_2^*}.
\]

Integrating with the signed transition fiber gives convergence of the conditional pair-bridge distance in mean under the complete true record law. No pointwise arithmetic floor and no division by a zero conditional density are used.

This is a strong global conditional statement. It remains a mean statement and does not give an unrestricted bridge at every prescribed roof value.

## 17. Record-only observation kernels

A Markov kernel from the complete record to a standard Borel output represents an arbitrary observation with independent randomization. It may report an interval, acceptance decision, label and random seed.

Pulling back an admissible output-path test through the kernel preserves its supremum bound and path Lipschitz constant. Therefore the complete mixed norm contracts, without any regularity assumption on the kernel in the record coordinates.

Under the reference law, the bridge pair remains independent of the output because the kernel reads only the record.

A procedure which reads the path is not covered by this theorem. The paper states this restriction correctly.

## 18. Full output postselection

Let `A` be a measurable event in the complete output and let its reference probability be at least `r_n>Delta_n`, where `Delta_n` is the uniform preselection mixed error.

If `alpha` and `beta` are the true and reference probabilities of `A`, then

\[
 |\alpha-\beta|\le\Delta_n,
 \qquad \alpha\ge r_n-\Delta_n.
\]

Restricting to the event does not increase the unnormalized error. Normalizing costs the event error plus the mass difference. Thus the output-path mixed error is at most

\[
 \frac{2\Delta_n}{r_n-\Delta_n}.
\]

On the output marginal this is an `L^1` variation bound. Dividing by two gives the probability total-variation estimate

\[
 \frac{\Delta_n}{r_n-\Delta_n}.
\]

The same pointwise scalar-to-path inequality gives the conditional mean pair-bridge bound.

The constants are correct. The theorem requires the **full output event** and preserves all information carried by an adaptive observation. It does not replace conditioning on a reported random interval by conditioning merely on membership in that interval.

The result is qualitative. It does not apply to a prescribed microscopic event whose reference mass is smaller than the unknown approximation error.

## 19. What revision 57 closes

Relative to revision 56, the new manuscript closes the following genuine issues.

- Moving spectral peaks cannot drift farther than their damping permits.
- The complete transition kernel has a radius-uniform physical-mean Gaussian envelope.
- The signed arithmetic reference has uniformly bounded total mass.
- Its tails are uniformly Gaussian in the return-centered variables.
- The full exact-return mixed law converges in `L^1` to the signed evaluated transition density.
- The normalized positive arithmetic reference converges in probability total variation.
- The negative mass of the finite transition kernel vanishes.
- The fixed-radius residue formula extends from central windows to the entire record law after normalization.
- The collision and actual-return bridges have a joint graph-coupled limit.
- The complete record is asymptotically independent of that coupled bridge pair in the stated mixed norm.
- The conditional pair bridge converges in mean under the complete record distribution.
- Arbitrary record-only observation kernels contract the theorem.
- Full-output postselection has exact denominator-loss bounds.

These are mathematically meaningful improvements. In particular, the global total-variation theorem is stronger than a collection of fixed-window consequences.

## 20. What revision 57 does not close

The manuscript still does not prove

\[
 \lim_{B\to\infty}\limsup_{m\to\infty}
 \sup_{R,n,k}
 \operatorname*{ess\,sup}_{u\ \mathrm{central}}
 m^2b^{\varepsilon(B),\mathrm{inc},1}_{n,k,m,R}(u)=0
\]

or the analogous estimate for the clearance source.

Therefore it does not prove

- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- the pointwise roof-density LLT for the four-coordinate return record;
- an unrestricted same-roof collision/return pair bridge;
- forward essential likelihood convergence on the complete central window;
- a pointwise roof-conditioned path theorem at every positive-reference roof;
- the strong critical `L^{145/144}` endpoint;
- or an unmodulated Gaussian law on arithmetic classes whose concrete residue has not been proved uniform.

The new global theorem does not change these implications.

## 21. Why complete total variation is not a pointwise theorem

Suppose a nonnegative density has a spike of height `H_j` and width `o(H_j^{-1})`. Its mass tends to zero while its essential supremum can diverge.

Complete `L^1` convergence rules out large total mass in the spike. It does not rule out its height.

The all-resolution theorem of revision 56 further localizes such a spike to a small exceptional set and makes that set small under the original source. It still does not control the height inside the set.

The Gaussian transition tail of revision 57 controls the **reference** at remote labels. It does not impose a pointwise upper bound on the positive physical remainder at a fixed central roof.

Thus none of the following implications is valid:

- global total variation implies uniform density convergence;
- reference Gaussian tails imply true essential-height control;
- conditional bridge convergence in record mean implies a bridge at every roof;
- postselection for events of mass larger than `Delta_n` implies a microscopic singleton theorem;
- small negative transition mass implies every finite transition value is positive.

The manuscript correctly avoids these implications.

## 22. Arithmetic modulation

The uniform theorem retains the complete finite transition kernel through changes of arithmetic type. At fixed radius it retains the concrete finite residue

\[
 \mathfrak a_R(k,n,m),
\]

including zero classes.

The positive part is normalized only to create a finite-count probability reference. The signed kernel remains the raw asymptotic expression, and its negative mass is proved to vanish.

Revision 57 does not prove that the arithmetic factor is identically one. It therefore does not assign conditional laws to zero classes or claim an unmodulated Gaussian theorem.

This is mathematically honest. A final title-level theorem should continue to display the arithmetic modulation unless the separate residue criterion is proved.

## 23. Novelty and relation to prior methods

The new spectral inequality

\[
 |\mu_j-\mu_R|^2\le C\kappa_j
\]

is not a formal consequence of continuity. It uses visible physical branch pairings and domination by a positive centered exponential moment. Its application to moving arithmetic peaks is a real contribution.

The local-to-global argument also controls an object more precise than a standard weak limit: the complete exact-return mixed law and its evaluated finite arithmetic transition reference in total variation.

The graph-coupled bridge theorem is stronger than listing two marginal bridge limits, and the observation-kernel formulation correctly handles adaptive record-dependent outputs without losing the selection event.

Nevertheless, the genuinely difficult inputs remain specific to one finite-horizon triangular Lorentz program and to its accumulated 120-module source construction. Positive-pressure domination, Gaussian completion of the square, fourth-moment tightness, Markov-kernel contraction and conditional normalization are standard techniques. Revision 57 does not formulate and verify a general spectral theorem across a wider class of singular hyperbolic systems.

This limits the top-four significance of the new advance even though the internal mathematics is substantial.

## 24. Generality and editorial significance

The A2-DYN program now contains, subject to inherited proof verification,

- stationary physical microscopic local laws;
- compact-family action estimates;
- exact occupation arithmetic and resonance classification;
- exact-index interval laws;
- finite transition kernels through arithmetic changes;
- complete-source local raw variation;
- one-sided pointwise lower laws;
- higher-integrability and Orlicz endpoints;
- positive incidence/clearance source decompositions;
- path-valued raw inversion;
- same-roof transport in mean;
- all-resolution exceptional-set localization;
- and now full-record total variation with graph-coupled bridges and postselection.

This is a technically impressive specialist program.

At the requested four-journal benchmark, four factors remain decisive:

1. the unrestricted pointwise endpoint remains unproved while the title and much of the architecture continue to center it;
2. the load-bearing continuum inputs are highly model-specific;
3. the article remains extraordinarily long and dependency-heavy;
4. no independent billiards/anisotropic-spaces audit has been obtained.

There is now a credible alternative editorial route: make the untruncated total-variation theorem and coupled bridge theorem the endpoint of a focused paper, retitle and reorganize accordingly, and place the pointwise positive-height program in a separate sequel or technical companion. This would not delete mathematics; it would align the submitted theorem with the title and editorial claim.

If the present title and unified architecture are retained, the incidence and clearance height estimates remain indispensable.

## 25. Independent specialist verification

No independent human specialist audit has been obtained. The following inherited points remain especially load-bearing:

1. the exact full occupation twist on the anisotropic collision spaces;
2. the physical representation of every retained peripheral branch;
3. the moving peak decomposition through arithmetic transitions;
4. the complete first-physical-defect source partition;
5. the all-depth marked local upper bound;
6. protected flow-box and critical-collar geometry;
7. the complete band-limited arithmetic inversion;
8. the complete-source local variation theorem;
9. the scalar and path positive raw-error identities;
10. common roof disintegration and countable norming classes;
11. the actual collision-to-return clock coupling;
12. uniform fourth moments and exact covariance normalization;
13. preservation of exact labels in every positive comparison;
14. half-open occupation at the terminal collision;
15. next-collision clearance on all matched branches;
16. parameter-uniformity across changes of arithmetic type.

For the new modules themselves, a specialist should check

- the uniform positive amplitude in the centered real-tilt splitting;
- construction of bounded smooth witnesses for each actual peripheral branch;
- scalar continuity of those witnesses where the section amplitude vanishes;
- complementary-power control after centering;
- the `m`th-root passage in the physical domination inequality;
- uniform optimization on finite peak supports;
- complex symmetric accretive Gaussian normalization;
- complete count and roof summation;
- the exact local-to-global `m^{-2}` bookkeeping;
- use of the joint, rather than marginal, clock coupling;
- common disintegration for the pair-path norm;
- and conditioning after arbitrary record-only observation kernels.

The exact-source workflows and finite diagnostics do not replace this audit.

## 26. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 26.1 Control the incidence essential height

Prove the uniform central-scale estimate for the entire original incidence source at the exact labels, without deleting a target-dependent exceptional set.

### 26.2 Control the clearance essential height

Prove the analogous estimate for the full competing-hit clearance source without continuing the trajectory through a physical seam or replacing it by a nearby regular word.

### 26.3 Complete the unrestricted pointwise theorem

Combine the two height estimates with the existing positive raw-error identity and the finite arithmetic transition kernel. Retain the arithmetic factor unless the concrete residue criterion is separately proved.

### 26.4 Deduce unrestricted same-roof bridges and likelihoods

Use the scalar-to-path implications already isolated by the manuscript to remove the target-dependent exceptional set from the collision and actual-return pair bridge and from forward essential likelihood convergence.

### 26.5 Obtain independent specialist review

The occupation spectrum, branch visibility, pressure comparison, physical boundary sources, raw local variation and joint clock transfer require external human verification.

### 26.6 Extract a broader spectral theorem

If top-four breadth is sought independently of the pointwise endpoint, formulate a reusable pressure--drift theorem for visible moving resonances in singular hyperbolic systems and verify it in more than one genuinely different dynamical setting.

### 26.7 Align the submission with its completed theorem

Alternatively, make the untruncated total-variation and graph-bridge theorem the principal endpoint of a focused article, with title, abstract and proof route aligned to that claim. Move the still-open pointwise program to a clearly separate sequel or companion without deleting its mathematics from the research archive.

### 26.8 Reduce the proof burden

Present the shortest complete chain needed for the submitted endpoint. Extensive provenance, validation ledgers, duplicated historical front matter and unfinished alternative endpoints should not dominate the journal narrative.

### 26.9 Sharpen the literature comparison

Explain theorem by theorem which full-record total-variation, moving-arithmetic, graph-coupled bridge and postselection conclusions are unavailable from existing Lorentz-process, billiard endpoint-LLT and suspension-flow LLT frameworks after checking their hypotheses.

## 27. Technical and presentation comments

1. In the global `L^1` proof, display the `O(n^2)` unit-cell count and the `m^{-2}` factor together.
2. Distinguish throughout between the fixed return index `n` tending to infinity and the collision count `m` summed in the record law.
3. Keep the signed transition density separate from its normalized positive part.
4. State that the negative transition mass tends to zero; do not call the finite signed kernel a probability.
5. Keep the fixed-radius residue, including zero classes, in every specialization.
6. Use “the record is independent of the coupled bridge pair” rather than language suggesting that the two bridges are independent of each other.
7. Keep observation variation/path bounded-Lipschitz dual distinct from path-space total variation.
8. Retain the full-output event in every adaptive postselection statement.
9. State explicitly that a path-reading selector is outside the record-only kernel theorem.
10. Keep the denominator condition `r_n>Delta_n` and the requirement `Delta_n/r_n->0` visible.
11. Do not infer a rate for a microscopic event from qualitative global variation.
12. Keep the pressure comparison on a fixed complex neighborhood; do not introduce a growing frequency band.
13. Distinguish the branch witness amplitude from the section endpoint amplitude `B_j`.
14. State where finitely many branch-witness neighborhoods are selected over the zero-damping locus.
15. Keep the complex determinant branch and accretivity assumptions visible in the Gaussian formula.
16. Preserve the true fourth-moment tail and reference Gaussian tail as separate inputs.
17. Do not infer essential-height control from global `L^1` convergence.
18. Keep the revision-56 exceptional-set theorem and the revision-57 full-record theorem logically distinct.
19. State that conditional pair-bridge convergence is in mean under the complete record law.
20. Keep the factor one half in probability total variation.
21. Preserve exact source normalization by `nu_R^*=nu|Y_R^*/c`, applied once.
22. Retain occupation at collision times `0,...,m-1` and clearance at collision `j+1`.
23. Keep source qualification and finite diagnostics separate from proof certification.
24. Retain all status flags for the unresolved pointwise endpoint and independent review.
25. Consider moving extensive provenance and validation material outside the principal journal narrative.

## 28. Final assessment

Revision 57 is a serious and mathematically coherent response to the revision-56 report.

It proves a new pressure--drift inequality for the retained moving spectral peaks, obtains a physical-mean Gaussian envelope for the complete arithmetic transition kernel, and uses it to upgrade the central mixed-measure theorem to total-variation convergence on the entire exact-return record space. It also proves a joint graph-coupled collision/actual-return bridge law, contracts it through arbitrary record-only observations, and gives correct postselection mass-budget bounds.

The pressure optimization, complex Gaussian estimate, count summation, local-to-global scaling, positive-part normalization, covariance transformation and conditional constants are internally consistent. I found no decisive error in modules 121--122.

The advance is nevertheless an integrated whole-law theorem, not closure of the unrestricted pointwise endpoint. Narrow positive incidence or clearance spikes remain compatible with global total variation, and the manuscript explicitly leaves their essential heights unproved. The unrestricted two-sided arithmetic raw-density theorem, unrestricted same-roof bridges and forward essential likelihood therefore remain open.

The manuscript also remains highly model-specific, extraordinarily large and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist or high-level dynamics/probability paper centered on the untruncated total-variation theorem, moving-arithmetic reference tails and graph-coupled bridge/postselection result could be significant if the inherited proof chain survives expert audit. A future top-four submission should return only after closing the incidence and clearance essential heights, or after extracting and independently validating a substantially broader pressure--drift theorem whose importance no longer depends on the unfinished pointwise endpoint.
