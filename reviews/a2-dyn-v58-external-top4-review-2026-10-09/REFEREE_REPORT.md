# External top-four referee report on A2-DYN revision 58

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v58-referee-response-2026-10-09`, `revision/a2-dyn-v58-referee-copy-2026-10-09`  
**Reviewed commit:** `b9c8e1f15b65e4843d1321f23ed5b816378b855c`  
**Reviewed repository tree:** `8eeccb222c31bce3ca328f0b3f7118840fb922eb`  
**Ordinary source payload tree:** `79b121c4771166af579908161316d721f3dadc9f`  
**Active manuscript directory:** `papers/A2-DYN-v58-referee-response`  
**Active mathematical source:** one hundred twenty-four numbered core modules; revision 58 retains all one hundred twenty-two revision-57 modules and adds modules 123--124  
**Frozen revision-57 author baseline:** `8dbfac97a74e2b498c77d1afd663dd1e7db18c91`  
**Frozen revision-57 complete paper tree:** `c379f1471b26a29a16a74b267d90c544516afbfb`  
**Controlling external report:** `reviews/a2-dyn-v57-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `4ffcf6bea86fabad719e8d893e4ae43bbb56da26` / `8293a37ac814e4028d0af8e831102d77d245c69e`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 58 is a genuine and mathematically substantive advance over revision 57. The preceding report accepted the new untruncated mixed total-variation theorem and the graph-coupled collision/return bridge law, but emphasized two distinct limitations:

1. the moving arithmetic transition reference had been controlled only as a finite sum of Gaussians with branch-dependent centers and complex Hessians; and
2. the positive physical incidence and clearance sources still lacked the essential-height bounds required for the unrestricted pointwise raw-density theorem.

Revision 58 resolves the first limitation and does not claim to resolve the second.

The new manuscript proves a scalar pressure-contact principle. For a visible damped spectral branch with damping `kappa`, centered drift `v`, branch Hessian `H` and physical covariance `Sigma`, the pressure gap has value, gradient and Hessian

```text
kappa,   v,   Sigma - Re H
```

at the zero tilt. At zero damping the branch and physical Hessians agree. Retaining this quadratic contact in the imaginary-tilt comparison yields

\[
 |v|\le C\left(\sqrt{\kappa h}+\kappa^{2/3}\right),
 \qquad h=\|\Sigma-\operatorname{Re}H\|,
\]

and hence

\[
 \frac{|v|^2}{\kappa}\longrightarrow0
\]

uniformly as the damping tends to zero. A peak which survives at inverse-count damping therefore has no surviving diffusive displacement of its Gaussian center.

Applied to the actual occupation spectrum of the Lorentz system, this permits every branch-dependent mean and complex covariance in the evaluated transition kernel to be replaced, in a Gaussian-weighted uniform norm, by the physical mean and physical covariance. All original phases, damping factors, partition amplitudes and arithmetic zero classes remain in one scalar coefficient. After the exact collision-to-return covariance change, revision 58 obtains a uniform full-space approximation

\[
 p_{n,R}(k,m,u)
 \approx n^{-2}\alpha_{m,R}(k,n,u)
                  g_{D_R}(V_{n,R}(k,m,u))
\]

in total variation over all `m >= n`, all lattice displacements and every positive roof value.

The new module also states the pressure-contact theorem in arbitrary dimension and verifies it independently for a three-strip deterministic baker map. In that example a nontrivial damped peak has

\[
 \kappa_\varepsilon=\frac{\pi^2}{9}\varepsilon^2+O(\varepsilon^3),
 \qquad
 v_\varepsilon=\frac{\pi^2}{18}\varepsilon^3+O(\varepsilon^4),
\]

so the damping may survive while the separate diffusive center disappears.

I audited the new modules

- `core/123_flat_pressure_contact.tex`;
- `core/124_common_gaussian_arithmetic_law.tex`;

and their use in the new front matter. I also checked the inherited moving-peak definitions, positive pressure, physical witness construction, transition kernel, global total-variation theorem, covariance change, graph-coupled bridge theorem and exact-source qualification records.

I found no decisive counterexample, sign error in the imaginary tilt, missing collision-count power, covariance-Jacobian error, false independence step, invalid growing-band substitution or normalization-factor error in the new chain. In particular:

1. the pressure gap has the printed sign `kappa + v dot t`;
2. its quadratic term is `Sigma - Re H`, not a branch covariance alone;
3. the two tilt regimes give the stated square-root/contact and cubic-remainder terms;
4. the full complex Hessian mismatch tends to zero by compactness on the zero-damping locus;
5. the Gaussian replacement pays both the moving shift and the matrix perturbation under the spectral damping factor;
6. the Baker-map coefficients printed in the article agree with the finite exponential-sum expansion;
7. the two factors of `1/c` in the return reference arise from different operations and are consistent;
8. the central record space contains `O(n^2)` unit cells and the local density scale is `O(n^{-2})`;
9. the signed reference is kept distinct from its normalized positive part; and
10. the bridge pair remains a graph coupling, not two independent Gaussian bridges.

These are meaningful achievements. The negative recommendation is not based on failure of the new flat-contact or canonical-reference theorems.

It is forced by the endpoint that still governs the title and most of the raw-inversion architecture. Revision 58 explicitly does **not** prove essential-height smallness for either positive physical defect source. Therefore it still does not prove the unrestricted two-sided pointwise arithmetic raw-density theorem, unrestricted same-roof bridges, forward essential likelihood convergence or the full pointwise roof-conditioned path theorem.

The new reference is simpler and more canonical, but it is still a reference in an integrated mixed-measure theorem. A true positive density may contain a spike of vanishing mass and unbounded essential height. Replacing a moving Gaussian reference by one physical Gaussian does not control such a spike.

At the requested benchmark, the paper would need either

1. completion of the unrestricted pointwise theorem that organizes its title and a large fraction of its one-hundred-twenty-four-module architecture; or
2. a general dynamical theorem of substantially greater independent breadth, with nontrivial realizations whose significance does not depend editorially on the unfinished Lorentz pointwise endpoint.

Revision 58 has moved toward the second route, but the abstract pressure-contact theorem is, once its strong spectral hypotheses are granted, a scalar Taylor/optimization lemma. The baker realization is exact and useful, but it is an i.i.d. finite-alphabet calculation and does not independently test the difficult continuous-density, singular-boundary or anisotropic-space mechanisms of the Lorentz theorem. It does not by itself supply four-journal breadth.

No independent human specialist audit has been obtained. My assessment is therefore positive about the new mathematics and cautious about the inherited continuum pipeline, but negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`b9c8e1f15b65e4843d1321f23ed5b816378b855c`.

The repository tree is

`8eeccb222c31bce3ca328f0b3f7118840fb922eb`.

The active article is

`papers/A2-DYN-v58-referee-response`.

The ordinary source payload tree recorded in the manifest is

`79b121c4771166af579908161316d721f3dadc9f`.

The author commit has the revision-57 external-review commit

`4ffcf6bea86fabad719e8d893e4ae43bbb56da26`

as its parent. The chronology is correct: revision 58 begins from the frozen external assessment and preserves that report.

The source manifest records:

- all one hundred twenty-two inherited core modules retained byte-for-byte;
- all one hundred sixty-three inherited Python files retained byte-for-byte;
- old compiled appendices and the bibliography retained;
- all inherited mathematical labels retained;
- two new modules, 123 and 124;
- `flat_pressure_contact_proved: true`;
- `common_gaussian_transition_proved: true`;
- `uniform_canonical_arithmetic_law_proved: true`;
- `baker_pressure_realization_proved: true`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `arithmetic_factor_identically_one_proved: false`; and
- `independent_human_review: false`.

The former revision-57 front matter remains compiled in `appendices/v57_frontmatter.tex`. The old main source and supporting status files are archived under provenance. The original title, exact return record, source normalization, arithmetic modulation and unrestricted pointwise target remain present.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v58-external-top4-review-2026-10-09/`.

No author source, prior report, workflow, historical manuscript or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA qualification workflows completed successfully on both reviewed author refs:

- response branch run `37924525405`;
- referee-copy branch run `37924539346`.

The runs bind the source archive, finite diagnostics, native build and rendered theorem pages to the reviewed SHA.

According to the validation record, the verifier checks

- the frozen revision-57 paper tree and artifact identity;
- the controlling revision-57 report blob;
- one hundred twenty-two unchanged inherited core files;
- one hundred sixty-three unchanged inherited Python files;
- the bibliography and compiled appendices;
- all one hundred twenty-four core inclusions;
- all inherited mathematical labels;
- twelve provenance copies;
- the ordinary Git payload identity;
- the read-only workflow hash;
- agreement of normal and optimized finite diagnostics;
- native TeX compilation; and
- theorem-label-based rendering.

The new finite checks include rational tilt cases, exact Baker-series coefficients, high-precision maxima, accretive Gaussian matrix checks, covariance normalization and negative controls.

These are meaningful source, algebra and bookkeeping checks. They do not certify

- the inherited full occupation operator on anisotropic spaces;
- the bounded physical representation of peripheral vectors;
- the branch-isolation and scalar-continuity arguments through arithmetic transitions;
- the positive physical witness construction;
- the resonant Hessian identity;
- the complete local raw-variation theorem;
- the incidence and clearance source decomposition;
- the joint clock coupling; or
- either missing essential-height estimate.

The manuscript and validation files state this limitation accurately.

## 4. Scope of this review

I did not attempt to re-prove all one hundred twenty-four core modules. The substantive audit concentrates on the new chain and the inherited inputs directly used by it:

1. the abstract pressure and visibility hypotheses;
2. passage from physical scalar pairings to a branch pressure inequality;
3. the signs in the imaginary-frequency Taylor expansion;
4. the two-regime optimization of the tilt;
5. uniformity near the compact zero-damping locus;
6. the `o(kappa)` drift conclusion;
7. the complex accretive Gaussian normalization;
8. Gaussian differentiation in the center and Hessian;
9. absorption of a moving center by spectral damping;
10. the split between low and positive damping;
11. verification for the actual occupation spectrum;
12. the explicit baker-map realization and its expansions;
13. construction of the common scalar arithmetic coefficient;
14. slow roof variation and asymptotic negativity control;
15. the collision-to-return covariance and count scaling;
16. summation over all exact labels and all positive roofs;
17. fixed-radius reduction to the finite residue;
18. transfer of the graph-coupled bridge reference;
19. preservation of exact selection events;
20. the distinction between integrated variation and pointwise height;
21. source preservation and qualification evidence; and
22. top-four significance and architecture.

The inherited revision-57 and earlier continuum chain is treated as a source-pinned baseline, not as independently certified mathematics.

## 5. The abstract pressure-contact framework

Module 123 separates four types of hypotheses.

### 5.1 Positive physical pressure

For a centered bounded observable `X_lambda`, the original probability satisfies

\[
 \int e^{-t\cdot S_mX_\lambda}\,d\nu_\lambda
 \le C e^{m\mathscr P_\lambda(t)},
\]

with

\[
 \mathscr P_\lambda(0)=0,
 \qquad D\mathscr P_\lambda(0)=0,
 \qquad D^2\mathscr P_\lambda(0)=\Sigma_\lambda.
\]

This is the appropriate order structure. The proof does not assume positivity of an anisotropic transfer operator at a complex frequency.

Centering and Jensen give the lower bound one for the exponential moment. Combined with the upper estimate and then taking `m`th roots, this implies `mathscr P_lambda(t) >= 0`. The harmless prefactor `C` disappears in the limit.

### 5.2 Visible spectral branches

Near the zero-damping locus, each retained branch has physical bounded endpoint tests whose scalar pairing contains that branch with an amplitude bounded away from zero and an exponentially smaller remainder.

This condition is stronger than nonvanishing of the observation amplitude `B_j`. The manuscript correctly permits `B_j=0` and chooses different witnesses on finitely many neighborhoods.

This distinction is important. A section pairing can vanish by arithmetic cancellation even when the spectral branch itself remains visible to another physical test.

### 5.3 Second-order contact

At zero damping the branch Hessian equals the physical covariance:

\[
 H_j=\Sigma_\lambda.
\]

The manuscript treats this as an independent hypothesis, not as a consequence of continuity of the drift or nonnegativity of pressure.

That is mathematically correct. Without contact one obtains only the quadratic drift bound of revision 57.

### 5.4 Compact finite branch supports

The zero-damping set is compact inside finitely many branch charts. Continuity therefore converts exact contact into a modulus

\[
 \omega(\delta)=
 \sup_{\kappa_j\le\delta}\|H_j-\Sigma_\lambda\|
 \longrightarrow0.
\]

The empty-set convention and absence of an asserted rate are both appropriate.

## 6. The physical domination inequality

For a physical witness pair and `z=a_j+it`, the pairing has modulus bounded by

\[
 \|a\|_\infty\|d\|_\infty
 \int e^{-t\cdot S_mX_\lambda}\,d\nu_\lambda.
\]

The branch expansion gives

\[
 A_j^{a,d}(\lambda,z)e^{m\psi_j(z)}+E_{j,m}(\lambda,z).
\]

Because the amplitude is bounded away from zero, one may first isolate the branch term, then take `m`th roots. The exponential remainder does not affect the limiting inequality. Since pressure is nonnegative and the remainder radius is below one, one obtains

\[
 \operatorname{Re}\psi_j(a_j+it)\le\mathscr P_\lambda(t).
\]

Thus

\[
 F_j(t)=\mathscr P_\lambda(t)
        -\operatorname{Re}\psi_j(a_j+it)
 \ge0.
\]

I find this argument sound in the written setting.

For exposition, a final version should isolate this root-taking step as a short lemma, explicitly displaying the amplitude and remainder inequalities. It is load-bearing and presently compressed into prose.

## 7. The Taylor sign and the covariance difference

The branch convention is

\[
 \operatorname{Re}\psi_j(a_j)=-\kappa_j,
 \qquad D\psi_j(a_j)=iv_j,
 \qquad -D^2\psi_j(a_j)=H_j.
\]

At the imaginary tilt `a_j+it`, one has

\[
 \operatorname{Re}\psi_j(a_j+it)
 =-\kappa_j-v_j\cdot t
   +\frac12t^{\mathsf T}\operatorname{Re}H_jt+O(|t|^3).
\]

Subtracting from the pressure gives

\[
 F_j(t)=\kappa_j+v_j\cdot t
 +\frac12t^{\mathsf T}
   (\Sigma_\lambda-\operatorname{Re}H_j)t+O(|t|^3).
\]

The printed signs are correct.

At zero damping, `F_j(0)=0` and `F_j>=0`, so its gradient vanishes and `v_j=0`. The exact contact makes the Hessian vanish as well.

This is the substantive improvement over revision 57. Replacing the quadratic term by an unspecified `C|t|^2` loses the contact information and gives only `|v|^2=O(kappa)`.

## 8. The two tilt regimes

Insert

\[
 t=-r\frac{v_j}{|v_j|}.
\]

Nonnegativity yields

\[
 |v_j|\le\frac{\kappa_j}{r}+rac12h_jr+C_3r^2,
 \qquad h_j=\|\Sigma_\lambda-\operatorname{Re}H_j\|.
\]

The manuscript chooses

\[
 r=\min\left\{\kappa_j^{1/3},
                    \sqrt{\kappa_j/h_j}\right\},
\]

with the second term interpreted as infinity when `h_j=0`.

There are two cases.

If

\[
 h_j\le\kappa_j^{1/3},
\]

then `r=kappa_j^(1/3)` and every term is `O(kappa_j^(2/3))`.

If

\[
 h_j>\kappa_j^{1/3},
\]

then `r=sqrt(kappa_j/h_j)` and the first two terms are `O(sqrt(kappa_j h_j))`. The cubic term satisfies

\[
 \frac{\kappa_j}{h_j}\le\sqrt{\kappa_jh_j}
\]

precisely because `h_j^3>kappa_j`.

Thus

\[
 |v_j|\le C
 \left(\sqrt{\kappa_jh_j}+\kappa_j^{2/3}\right).
\]

The exponent arithmetic is correct.

Squaring gives

\[
 |v_j|^2\le C\kappa_j
             (h_j+\kappa_j^{1/3}).
\]

Compact contact then implies the uniform ratio limit.

## 9. Diffusive center collapse

If `m kappa_j <= L`, then

\[
 m|v_j|^2
 \le CL\left\{\omega(L/m)+(L/m)^{1/3}\right\}
 \longrightarrow0.
\]

Hence

\[
 \sqrt m\,v_j\longrightarrow0
\]

for every branch which survives with bounded damping exponent.

This conclusion is strictly stronger than tightness of the moving centers. It rules out a distinct shifted Gaussian in the transition regime.

The statement is qualitative because the parameter modulus `omega` is qualitative. The manuscript correctly does not advertise a polynomial collision-count rate.

## 10. Complex accretive Gaussians

For complex symmetric `H` with uniformly positive real part, the manuscript uses

\[
 G_H^{(d)}(Z)
 =(2\pi)^{-d/2}(\det H)^{-1/2}
     e^{-Z^{\mathsf T}H^{-1}Z/2}.
\]

The accretive symmetric domain is convex and contains the real positive matrices, so the determinant square-root branch is well defined by continuation.

Uniform exponential decay for real `Z` follows from positivity of `Re(H^{-1})`. One useful identity, which should be printed in the final version to avoid transpose/conjugate ambiguity, is

\[
 \operatorname{Re}H^{-1}
 =\overline{H}^{-1}(\operatorname{Re}H)H^{-1}.
\]

On a compact accretive family this gives a uniform positive lower bound for `Re(H^{-1})`.

Differentiation in `Z` and in `H` introduces only polynomial factors, which can be absorbed into a slightly weaker Gaussian exponent. The manuscript's derivative bound is therefore plausible and standard.

This point deserves a displayed lemma because a formally incorrect use of `w^T H w` instead of the Hermitian identity would be dangerous. I do not find such an error in the final v58 argument, but the justification is too compressed for the role it plays.

## 11. The common Gaussian-shape estimate

The evaluated peak sum is

\[
 K_m=\sum_jq_{j,m}
 G_{H_j}^{(d)}(Z-\sqrt m\,v_j),
 \qquad |q_{j,m}|\le Ce^{-m\kappa_j}.
\]

The target common shape is

\[
 \left(\sum_jq_{j,m}\right)g_{\Sigma_\lambda}(Z).
\]

Along the matrix and center segments, the difference of the two Gaussians is bounded by

\[
 C(\|H_j-\Sigma_\lambda\|+\sqrt m|v_j|)
 \sup_{0\le s\le1}e^{-b|Z-s\sqrt m v_j|^2}.
\]

The weaker global estimate

\[
 |v_j|^2\le C_D\kappa_j
\]

allows the shift exponential to be absorbed into half of the damping.

For `kappa_j <= delta`, the Hessian term costs `omega(delta)`, while

\[
 \sqrt{m\kappa_jh_j}\,e^{-m\kappa_j/2}
 \le C\sqrt{\omega(\delta)}
\]

and

\[
 \sqrt m\,\kappa_j^{2/3}e^{-m\kappa_j/2}
 \le Cm^{-1/6}.
\]

For `kappa_j > delta`, the contribution is exponentially small in `m delta`.

The resulting estimate

\[
 \sup e^{a|Z|^2}|K_m-S_mg_\Sigma|
 \le C\left\{
 \omega(\delta)+\sqrt{\omega(\delta)}
 +m^{-1/6}+e^{-m\delta/4}
 \right\}
\]

is correct. Choosing, for example, `delta=m^(-1/2)` proves convergence.

The final version should make this chosen diagonal explicit immediately after the theorem statement, because the left side does not depend on the free `delta`.

## 12. Verification for the Lorentz occupation spectrum

The Lorentz realization uses the centered four-component collision observable containing

- the two displacement coordinates;
- the bounded roof; and
- the actual section occupation.

The pressure is supplied by the positive full-occupation twist. Its Hessian at the origin is the physical collision/occupation covariance `Omega_R`.

The inherited moving-peak theorem states that at a true resonance

\[
 H_j=\Omega_R,
 \qquad \mu_j=\mu_R.
\]

The inherited physical representation permits smooth endpoint witnesses with nonzero branch amplitude even when the section amplitude `B_j` vanishes.

Subject to those inherited results, the hypotheses of the abstract theorem are matched correctly.

This application is one of the highest-priority points for independent specialist review. It depends on the simultaneous correctness of the full occupation operator, physical peripheral representation, scalar continuity, branch isolation and resonant covariance identity.

## 13. The baker-map realization

The map

\[
 \mathcal B(x,y)=(3x-i,(y+i)/3)
\]

on the three vertical strips is the standard invertible, area-preserving baker transformation. Its derivative is `diag(3,1/3)` on each piece and its strip digits are exactly independent and uniform under Lebesgue probability.

For

\[
 f_\varepsilon\in\{0,1,2+\varepsilon\},
\]

the characteristic moment is the exact finite sum

\[
 \varphi_\varepsilon(z)^m,
 \qquad
 \varphi_\varepsilon(z)
 =\frac13(1+e^{iz}+e^{i(2+\varepsilon)z}).
\]

The physical witnesses are `a=d=1`, the amplitude is one and the remainder is zero.

The physical variance

\[
 \Sigma_\varepsilon
 =\frac23+\frac23\varepsilon+rac29\varepsilon^2
\]

is correct.

Expanding the real maximum near `2 pi` gives

\[
 a_\varepsilon
 =2\pi-\pi\varepsilon+rac\pi3\varepsilon^2
 +O(\varepsilon^3),
\]

and the printed damping, drift and Hessian expansions are consistent with direct differentiation of the finite exponential sum.

This is a valid second realization of the scalar spectral principle.

Its significance should nevertheless be described with restraint. The example is exactly Bernoulli at the symbolic level, the observable has finite support, and no continuous roof-density inversion, physical boundary source, anisotropic multiplier or raw-return theorem is involved. It verifies the analytic lemma independently; it does not provide a second realization of the main Lorentz density theorem.

## 14. The common arithmetic coefficient

Revision 58 defines

\[
 \Phi_{m,R}(y)=\frac1c\operatorname{Re}
 \sum_je^{-ia_j(R)\cdot y}z_j(R)^mB_j(R).
\]

Every original branch retains

- its phase;
- its damping;
- its observation amplitude;
- its partition weight; and
- its possible zero class.

The roof phase is not discarded.

The common transition reference is

\[
 \mathcal L^\circ_{m,R}(y)
 =\Phi_{m,R}(y)g_{\Omega_R}
       \left(\frac{y-m\mu_R}{\sqrt m}\right).
\]

The abstract common-shape theorem applies with

\[
 q_{j,m}=c^{-1}e^{-ia_j\cdot y}z_j^mB_j.
\]

Taking real parts is legitimate after the complex estimate. The resulting Gaussian-weighted error is uniform in every real target and every radius.

This is a real simplification of the transition formula: moving centers and complex branch Hessians disappear from the Gaussian factor, while arithmetic remains in the scalar coefficient.

## 15. Slow roof variation and reference negativity

A zero-damping branch has zero roof frequency. Continuity and compactness therefore imply that the roof frequency is small when the damping is small.

Differentiating the common kernel gives two contributions:

1. the derivative of the roof phase, bounded by
   \[
   \sum_j|b_j|e^{-m\kappa_j};
   \]
2. the derivative of the physical Gaussian, bounded by `C m^(-1/2)`.

Splitting at `kappa=m^(-1/2)` proves a uniform derivative bound `d_m -> 0`.

Let

\[
 P=m^2p\ge0,
 \qquad G^\circ=\mathcal L^\circ.
\]

The inherited unit-interval local variation theorem and the kernel comparison give

\[
 \int_u^{u+1}|P-G^\circ|
 \le e_m+\theta_m.
\]

If `G^circ(u)=-h`, then slow variation gives

\[
 G^\circ(v)\le-h+d_m
\]

on the unit interval. Positivity of `P` forces

\[
 h\le e_m+\theta_m+d_m.
\]

Thus the negative height of the **reference** vanishes uniformly.

The argument is correct in scope. It proves neither an upper bound on the positive part of `P` nor the missing incidence/clearance heights. The manuscript repeatedly preserves this distinction.

For clarity, the final version should state explicitly that the true roof density is extended by zero outside its physical support and that the local variation theorem is being used uniformly for every translated unit interval.

## 16. The two factors of `1/c`

The fixed section mass is

\[
 c=\nu(Y_R^*)=\frac{91}{10000\pi}.
\]

The first factor `1/c` occurs already in `Phi`; it comes from the original return-source normalization and the collision transition formula.

The return-scale coefficient is

\[
 \alpha_{m,R}=\Phi_{m,R}/c.
\]

This second factor is not a second source normalization. It results from the count and covariance conversion.

Indeed

\[
 \Omega_R=cL_RD_RL_R^{\mathsf T},
 \qquad \det L_R=c.
\]

In four dimensions,

\[
 \det\Omega_R=c^6\det D_R,
\]

and therefore

\[
 g_{\Omega_R}(\sqrt cL_RV)=c^{-3}g_{D_R}(V).
\]

On the central return scale

\[
 m^{-2}\sim c^2n^{-2}.
\]

Thus

\[
 m^{-2}\Phi\,g_{\Omega_R}
 \sim n^{-2}(\Phi/c)g_{D_R}.
\]

The printed normalization is correct.

## 17. The full canonical arithmetic return law

The signed canonical reference is

\[
 q^\circ_{n,R}(k,m,u)
 =n^{-2}\alpha_{m,R}(k,n,u)
       g_{D_R}(V_{n,R}(k,m,u)).
\]

It includes

- every collision count `m >= n`;
- every displacement label;
- every positive roof value;
- every damped phase;
- every arithmetic zero class; and
- no averaging over the return index.

### 17.1 Replacement of the old transition kernel

The weighted common-shape estimate gives

\[
 \int m^{-2}|\mathcal L_{m,R}-\mathcal L^\circ_{m,R}|
 \le C\sup_{m\ge n}\theta_m\to0.
\]

The summation is the same Gaussian count sum audited in revision 57.

### 17.2 Collision-to-return scale

On `|V| <= M`, one has

\[
 m=n/c+O_M(\sqrt n)
\]

and

\[
 \frac{y-m\mu_R}{\sqrt m}
 =\sqrt{n/m}\,L_RV.
\]

The covariance identity and count prefactor give uniform pointwise error `o(n^-2)` between the two references.

### 17.3 Cell bookkeeping

The central region contains

- `O_M(n)` displacement pairs;
- `O_M(sqrt(n))` collision counts; and
- `O_M(sqrt(n))` unit roof intervals.

Hence there are `O_M(n^2)` unit cells. The density error is `o(n^-2)`, so the integrated central error is `o(1)`.

This bookkeeping is correct.

### 17.4 Tail bounds

The coefficient `alpha` is uniformly bounded and `D_R` is uniformly elliptic. Direct Gaussian summation yields a bounded total variation norm for the signed reference and an `e^{-aM^2}` tail outside `|V|<=M`.

Combining the central comparison, the old reference tail and the true fourth-moment tail proves the full-space `L^1` theorem.

### 17.5 Positive normalization

For the positive true density `p`, replacing the signed reference by its positive part decreases pointwise absolute error. The reference mass therefore tends to one and normalization costs at most a second copy of the unnormalized error in variation mass. Division by two gives the stated probability total-variation bound.

The negative reference mass also tends to zero.

I find this chain internally consistent.

## 18. Fixed-radius arithmetic

At a fixed radius, every branch with positive damping decays exponentially in `m`. The remaining branches are true resonances. Their roof frequency is zero, their center and covariance are physical, and their finite phase sum is the inherited residue.

Consequently the coefficient `alpha_{m,R}` may be replaced by

\[
 \mathfrak a_R(k,n,m)
\]

on the complete record space after normalization.

The residue, including its zero classes, is retained. The manuscript does not replace it by one.

This is the correct fixed-radius specialization. Uniformity through arithmetic changes requires the finite damped coefficient, not a discontinuous choice of resonance group.

## 19. Coupled paths and postselection

Revision 58 changes only the record reference. The bridge reference remains

\[
 \mathsf H_R=
 \operatorname{Law}(\mathbb B_{\Omega_R},
       c^{-1/2}L_R^{-1}\mathbb B_{\Omega_R}).
\]

The second path is a linear image of the first. The two are not independent.

Total variation between the old and new record references tends to zero. Tensoring their signed difference with the probability `H_R` controls the mixed observation/path norm. The revision-57 graph-coupled theorem therefore transfers by the triangle inequality.

A record-only Markov kernel contracts the mixed norm. Restriction to the full output event does not enlarge the unnormalized error. If its reference mass is at least `r_n > Delta_n`, the true mass is at least `r_n-Delta_n`, and normalization gives

\[
 \frac{\Delta_n}{r_n-\Delta_n}
\]

in probability total variation and twice that amount in the joint path-dual norm.

The factors are correct. The theorem does not cover a path-reading selector or a microscopic event whose mass is smaller than the qualitative approximation error.

## 20. What revision 58 closes

Relative to revision 57, the manuscript closes the following issues.

- The moving spectral means are not merely tight; their diffusive displacement vanishes on surviving weakly damped branches.
- The branch-dependent complex Hessians can be replaced by the physical covariance in a Gaussian-weighted uniform norm.
- The complete finite transition sum has one physical Gaussian shape through arithmetic changes.
- The full exact-return law has a canonical physical-covariance arithmetic reference uniformly in the radius.
- The fixed-radius finite residue is recovered on the entire record space.
- The signed canonical reference has vanishing negative mass.
- The graph-coupled bridge and full-output selection theorems use the same canonical record reference.
- A scalar abstract pressure-contact theorem is stated in arbitrary dimension.
- A deterministic baker map supplies an independent exact realization of that scalar theorem.

These are real advances and should not be described as merely cosmetic simplification of revision 57.

## 21. What revision 58 does not close

The manuscript does not prove

\[
 \lim_{B\to\infty}\limsup_{m\to\infty}
 \sup_{R,n,k}
 \operatorname*{ess\,sup}_{u\,\mathrm{central}}
 m^2b^{\varepsilon(B),\mathrm{inc},1}_{n,k,m,R}(u)=0
\]

or the analogous clearance estimate.

It therefore does not prove

- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- the pointwise roof-density LLT;
- unrestricted same-roof collision and actual-return bridges;
- forward essential likelihood convergence;
- a pointwise roof-conditioned path theorem at every prescribed positive-reference roof;
- the strong critical `L^{145/144}` endpoint;
- an identically-one arithmetic factor; or
- an independent proof certificate.

The source manifest and publication-status file record these limitations accurately.

## 22. Why the canonical reference does not solve the height problem

Suppose

\[
 \|p_n-q_n\|_{L^1}\to0
\]

and `q_n` is a smooth Gaussian-weighted arithmetic density. This does not imply

\[
 \|p_n-q_n\|_{L^\infty}\to0.
\]

A nonnegative spike may have height `H_n`, width `o(H_n^{-1})` and mass tending to zero. It is invisible in total variation but prevents pointwise convergence.

The new theorem improves `q_n`; it does not change this logical fact.

Likewise:

- reference-negative-height smallness does not imply true positive-height smallness;
- Gaussian reference tails do not exclude physical boundary spikes;
- postselection stability above the global error scale does not cover an individual roof fiber;
- record-mean bridge convergence does not imply a bridge at every prescribed roof; and
- a canonical covariance does not remove incidence or competing-hit seams.

The manuscript avoids these invalid implications, but the obstruction remains central to its advertised pointwise endpoint.

## 23. Novelty and the scalar general theorem

The flat-contact theorem is clean and potentially reusable. It identifies a useful principle:

> if a visible damped branch is dominated by the original positive pressure and has second-order contact with that pressure at zero damping, then its drift is negligible relative to its damping.

The conclusion is stronger than the usual quadratic drift bound and is exactly what is needed to collapse moving Gaussian centers.

However, the proof after the hypotheses are established is a finite-dimensional nonnegative Taylor expansion followed by an optimized one-dimensional tilt. The difficult dynamics are concentrated in the hypotheses:

- construction of a positive pressure;
- physical visibility of each branch;
- isolation and continuity of branch data; and
- Hessian contact at true resonances.

The abstract result is therefore not, by itself, a broad transfer-operator theorem for singular hyperbolic systems.

The baker example verifies the scalar mechanism independently but in an exactly Bernoulli finite-support setting. It does not test the hard Lorentz features: singularity growth, anisotropic multipliers, continuous roof inversion, physical boundary sources or induced-return geometry.

At a specialist-journal level, this is a useful conceptual addition. At a top-four level, it does not yet provide the breadth requested in the revision-57 report.

## 24. Architecture and editorial significance

The new front matter is substantially clearer than the accumulated historical opening. It presents two principal statements and places the new proof first.

Nevertheless, the complete article still contains one hundred twenty-four numbered modules and a very long dependency chain. Its title continues to emphasize raw local inversion, while the unrestricted pointwise raw theorem remains unproved.

There are now two strong, but different, possible papers inside the source:

1. a focused paper on flat pressure contact, canonical arithmetic transition laws, whole-record total variation and graph-coupled bridges; and
2. the larger pointwise raw-inversion program requiring physical incidence and clearance heights.

The current manuscript keeps both under one title. That is permissible as a research archive, but it is not yet an effective four-journal submission.

For a positive top-four recommendation, either the pointwise endpoint should be completed or the integrated/canonical theorem should be extracted into a substantially shorter article whose general significance is demonstrated independently of the unfinished source-height program.

## 25. Independent specialist verification

No independent human specialist audit has been obtained.

For the new modules, the highest-priority checks are:

1. the physical scalar witness expansion near every zero-damping branch;
2. uniform nonvanishing of its amplitude on a finite cover;
3. the centered pressure Hessian identification;
4. the equality `H_j=Omega_R` at every true resonance;
5. branch isolation and continuation through arithmetic transitions;
6. the sign conventions in the complex logarithm;
7. the accretive complex Gaussian inverse and determinant branch;
8. uniform Gaussian differentiation in the matrix parameter;
9. the low/high damping split in the weighted shape estimate;
10. the two source/count factors of `1/c`;
11. the central cell count and tail summation;
12. the fixed-radius residue identification;
13. the common path disintegration and graph clock coupling; and
14. the exact output-event normalization.

The inherited continuum obligations remain even more extensive:

- actual section occupation as a strong-space multiplier;
- full occupation-torus power bounds;
- measurable peripheral representations;
- finite-cover arithmetic rigidity;
- physical thin-layer construction;
- first-defect source decomposition;
- critical-collar geometry;
- complete local raw variation;
- positive path-remainder identity;
- actual-return clock transfer; and
- incidence and clearance essential-height estimates.

The workflow, finite diagnostics and symbolic expansions do not replace this audit.

## 26. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 26.1 Prove the incidence essential-height estimate

Establish the central-scale uniform estimate for the complete incidence source at the original exact labels, without deleting an exceptional set and without replacing the physical word.

### 26.2 Prove the clearance essential-height estimate

Establish the corresponding estimate for the full competing-hit clearance source, respecting the next-collision convention and without continuing an orbit across a physical seam.

### 26.3 Complete the unrestricted pointwise theorem

Combine the two height estimates with the retained positive raw-error identity and the canonical arithmetic reference.

The finite arithmetic factor must remain unless its concrete zero-residue criterion is proved separately.

### 26.4 Deduce unrestricted same-roof consequences

Only after pointwise source control should the manuscript promote the record-mean bridge and likelihood results to unrestricted same-roof bridge and forward essential-likelihood statements.

### 26.5 Obtain independent specialist review

The occupation spectrum, branch visibility, pressure comparison, critical physical geometry, local raw variation and clock coupling require external human verification.

### 26.6 Strengthen the general theorem if breadth is the chosen route

A top-four general-theorem route should verify the pressure/contact mechanism in at least one additional system where the difficult hypotheses are nontrivial, rather than exactly reducible to independent finite digits. Ideally the second realization would involve a genuine singular transfer-operator problem and a nontrivial local or density consequence.

### 26.7 Give a standalone proof of the scalar theorem

Print the root-taking lemma, accretive Gaussian lemma, branch-cover argument and chosen diagonal explicitly. The scalar theorem should be independently readable without reconstructing conventions from the Lorentz pipeline.

### 26.8 Reduce the journal proof burden

Present the shortest complete route to one principal endpoint. Extensive provenance, source manifests, validation ledgers and historical theorem hierarchies should remain in the repository or a technical supplement rather than dominate the journal narrative.

### 26.9 Sharpen the literature comparison

Explain theorem by theorem which aspects of the canonical full-record law, arithmetic transition, coupled bridge and flat-contact principle are not consequences of existing Lorentz-process, endpoint mixing-LLT, suspension-flow LLT or standard analytic perturbation results once their hypotheses are verified.

## 27. Technical and presentation comments

1. State explicitly in the abstract theorem that the branch logarithm is the centered logarithm used in the physical pairing.
2. Isolate the `m`th-root pressure-domination step as a lemma with the nonzero amplitude and remainder written out.
3. Keep `h_j=||Sigma-Re H_j||` distinct from the full complex modulus `omega(delta)=sup||H_j-Sigma||`.
4. Print the identity for `Re(H^{-1})` used in the complex Gaussian decay estimate.
5. Specify the determinant square-root branch once and use the same convention in every complex Gaussian formula.
6. After the common-shape theorem, choose `delta_m` explicitly before saying that the left side tends to zero.
7. Keep the qualitative modulus separate from the explicit `m^{-1/6}` cubic term; no global polynomial rate follows.
8. State where the physical witnesses may change from one branch neighborhood to another.
9. Do not identify nonzero physical witness amplitude with nonzero section amplitude `B_j`.
10. In the Baker computation, keep the centered derivative convention adjacent to the coefficient `v_epsilon` to prevent a sign ambiguity.
11. Describe the baker realization as a scalar spectral realization, not as a second raw-density theorem.
12. Keep `Phi` signed and distinguish it from the normalized positive probability reference.
13. Keep both factors `1/c` visible and explain their separate origins near the main theorem.
14. State explicitly that exact integer labels make the phase independent of frequency lifts.
15. In the reference-negativity proof, state the zero extension of the true roof density and the translated unit interval.
16. Do not infer positive true-density heights from vanishing negative reference heights.
17. Keep the `O(n^2)` unit-cell count and `O(n^{-2})` density scale in the same display.
18. Preserve the order `n -> infinity` first and central radius `M -> infinity` second.
19. Keep source fourth-moment tightness and reference Gaussian tightness as separate inputs.
20. Retain zero arithmetic classes in every fixed-radius specialization.
21. Use the normalized positive part only for probability references; retain the signed coefficient in raw inversion.
22. Keep probability total variation equal to one half of variation mass.
23. Keep the observation/path mixed norm distinct from path-space total variation.
24. State that the collision and return bridges inside the graph law are not independent.
25. Preserve the complete output event under record-only postselection.
26. Exclude path-reading selectors from the contraction theorem.
27. Retain the condition `Delta_n/r_n -> 0`; no microscopic selection rate is available.
28. Do not describe whole-record total variation as pointwise density convergence.
29. Do not describe the common Gaussian covariance as removal of the physical boundary source.
30. Keep the incidence and clearance status flags false until the corresponding essential-height proofs are supplied.
31. Keep arithmetic modulation in the title-level summary unless residue triviality is proved.
32. Separate exact-source qualification from mathematical certification.
33. Consider moving the baker expansion details to a short appendix while retaining the exact coefficients.
34. Consider presenting the abstract scalar theorem before any Lorentz notation, as the current module largely succeeds in doing.
35. Reduce repeated historical summaries in the body; the compiled provenance appendix already preserves them.

## 28. Final assessment

Revision 58 is a serious and mathematically coherent response to the revision-57 report.

It strengthens the moving-peak estimate from

\[
 |v_j|^2=O(\kappa_j)
\]

to

\[
 |v_j|^2=o(\kappa_j),
\]

under a clearly stated second-order pressure-contact hypothesis. It then converts the finite transition kernel to one physical Gaussian shape, uniformly through arithmetic changes, and derives a canonical full-space arithmetic Gaussian law for the original exact-return record.

The pressure-gap sign, covariance-difference Hessian, two tilt regimes, complex Gaussian scaling, Baker coefficients, section/count normalization and full-space cell bookkeeping are internally consistent. I found no decisive error in modules 123--124.

The new scalar theorem and baker realization improve the conceptual organization and generality of the manuscript. The canonical physical-covariance reference is more informative than the moving complex-Gaussian reference of revision 57.

The advance nevertheless remains an integrated-reference theorem. It does not bound the essential height of either positive physical defect source. The unrestricted two-sided pointwise raw-density theorem, unrestricted same-roof bridges and forward essential likelihood therefore remain open.

The abstract theorem is useful but elementary after its difficult spectral hypotheses are granted, and the baker example is an exactly Bernoulli finite-support realization rather than an independent test of the hard Lorentz mechanisms. The article remains highly model-specific, extraordinarily long and dependent on an inherited continuum pipeline which has not received independent human specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused high-level dynamics/probability paper built around flat pressure contact, the canonical arithmetic Gaussian whole-record law and graph-coupled bridges could be significant if the inherited proof chain survives expert audit. A future top-four submission under the present title should return only after the two physical essential-height estimates close the unrestricted pointwise theorem, or after a substantially broader and independently verified general theorem makes that unfinished endpoint editorially secondary.