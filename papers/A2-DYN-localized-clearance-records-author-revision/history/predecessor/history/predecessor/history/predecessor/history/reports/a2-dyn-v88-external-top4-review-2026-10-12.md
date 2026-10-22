# External top-four referee report on A2-DYN revision 88

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v88-referee-response-2026-10-12`, `revision/a2-dyn-v88-referee-copy-2026-10-12`  
**Reviewed commit:** `e0d462e7b04c35fa3547435ede29adafe1968d8f`  
**Reviewed repository tree:** `137215b83dc5ea00d6bdd38234d11a03e286889e`  
**Active manuscript directory:** `papers/A2-DYN-v88-referee-response`  
**Active mathematical source:** two hundred seven numbered core modules; revision 88 adds modules 205--207  
**Immediate author baseline:** revision 87 at `44785327cc0331d994d5d1de371710615cfd6b93`  
**Frozen revision-87 paper tree:** `08608632533c4e0555ddd7f66a8df3f179f26d76`  
**Controlling external report:** `reviews/a2-dyn-v85-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `af90a4e75bb4262cf16e64ff5e62a688bc21c007` / `86ecdfdf87d9ad7f6ecbe20c97f10cc75967eec5`  
**Exact-source qualification runs:** response `38216063798`; referee-copy `38216070973`; both were queued when this report was frozen  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 88 is a genuine theorem-bearing revision. It contains substantial new analysis and should not be described as a cosmetic reformulation of the revision-87 source charge. The new work improves three load-bearing parts of the endpoint program:

1. it obtains marked-incidence local estimates with every exponent strictly below `3/2` by combining a physical `s^2` cap with interpolation of the finite peak projectors;
2. it derives actual unconditioned optical moments `I_m^p` for every `1<p<3/2`, with a finite-count spectral remainder retained throughout the layer-cake argument; and
3. it applies the stronger moment to a larger shrinking family, proving a finite-count uniform optical envelope of order `h^(1/10)` for initial gradient at least `h^(1/8)` and total residence at least `h^(1/4)`, without an incidence or optical-sensitivity cutoff.

The revision also proves a total-variation modulus for original weighted roof fibers restricted to common survivors and gives a fixed-interval mass estimate for the complementary original source. These are mathematically useful and sharpen the final obstruction.

I audited the new modules

- `core/205_adjustable_incidence_and_optical_moments.tex`;
- `core/206_expanded_shrinking_family_envelope.tex`;
- `core/207_weighted_fiber_stability_and_exact_source.tex`;

and, because no external report was deposited for revisions 86 or 87, I also reviewed the continuous increment formed by modules 199--204:

- `core/199_complete_mixed_optical_moments.tex`;
- `core/200_microscopic_large_sensitivity_envelope.tex`;
- `core/201_causal_optical_charge_and_endpoint.tex`;
- `core/202_complete_segment_trace_estimate.tex`;
- `core/203_shrinking_segment_optical_envelope.tex`;
- `core/204_original_source_concentration_localization.tex`.

I found no decisive counterexample, no reversal of the physical roof-flow direction, no error in the printed exponent arithmetic, no hidden growing Fourier band, no word-count factor introduced in the Borel segment summation, and no illicit claim that fixed-interval mass control proves essential-height control.

The negative recommendation is forced by one remaining assertion which is both explicit and central. Let

\[
 R_h^\varepsilon(t)
 =\int W^\varepsilon(x)
   \mathbf 1_{\{z(x)<h^{1/8}\ \mathrm{or}\ \ell(x)<h^{1/4}\}}
   \,d\mu_t(x),
\]

and let

\[
 \mathfrak R_{\varepsilon,M}
 =\lim_{h\downarrow0}\mathcal H_M(R_h^\varepsilon)
\]

be its collision-normalized ordered essential-height charge on the original central roofs and exact labels. Revision 88 retains the exact source-level equivalence

\[
 \mathcal E_M
 =\lim_{B\to\infty}\mathfrak R_{\varepsilon(B),M},
 \qquad \varepsilon(B)=A_0B^{-1/12},
\]

but does not prove that the right-hand side vanishes.

Thus the revision gives a sharper and more physical localization of the original pointwise error. It does not prove the unrestricted pointwise raw local limit theorem. Fixed-interval mass decay of the exceptional source does not fill this gap: a sequence of nonnegative densities may have vanishing mass on every fixed interval while its normalized essential height remains positive or diverges because the mass concentrates on narrower roof intervals.

At the requested benchmark, the final organizing theorem must be proved. Identifying the precise concentration charge, enlarging the uniformly controlled complement, and obtaining common-survivor stability are important advances, but they are not substitutes for proving the charge zero.

## 2. Frozen source, chronology, and source identity

Both reviewed author branches resolve to

`e0d462e7b04c35fa3547435ede29adafe1968d8f`.

The repository tree at this commit is

`137215b83dc5ea00d6bdd38234d11a03e286889e`.

The active article is

`papers/A2-DYN-v88-referee-response`.

The immediate author baseline is revision 87 at

`44785327cc0331d994d5d1de371710615cfd6b93`,

with frozen paper tree

`08608632533c4e0555ddd7f66a8df3f179f26d76`.

The active manifest records 204 inherited core modules and 207 active modules. The three new modules are precisely 205--207. The repository packet states that all inherited cores, Python sources, appendices, bibliographies, provenance records, and revision-87 top-level snapshots are preserved.

The latest deposited external report preceding this revision is the revision-85 report at

`af90a4e75bb4262cf16e64ff5e62a688bc21c007`.

Revisions 86 and 87 are author revisions responding to that report; they do not contain a later independent review decision. For this reason, the present audit treats modules 199--207 as one continuous mathematical response rather than accepting the revision-86 and revision-87 status transitions without inspection.

The manuscript retains the original title, Lorentz family, section, physical guard, source normalization, exact displacement and occupation labels, terminal section test, finite arithmetic reference, and arithmetic zero classes. It does not replace the pointwise objective by a roof interval theorem, a collision-count window, a pooled occupation class, a removed-source theorem, or a result outside the original exact event.

## 3. Qualification evidence and its boundary

The exact-SHA workflows attached to the two author refs are

- response run `38216063798`;
- referee-copy run `38216070973`.

At the time this report was frozen, both runs were queued and had no conclusion. I therefore do not treat either run as completed remote build evidence.

The validation contract states that a completed run checks, among other items,

- the frozen revision-87 paper tree and controlling revision-85 report blob;
- preservation of all inherited sources and snapshots;
- inclusion of all 207 active core modules across the article and supplement;
- ordinary and optimized finite fixtures;
- native builds of the focused article and complete supplement;
- stable references and warning gates;
- recorder coverage; and
- PDF word geometry and selected renders.

These checks are valuable evidence of source identity, finite algebra, and typesetting integrity. Even after successful completion, they would not certify

- the imported four-record spectral theorem;
- the anisotropic projector interpolation on every moving peak chart;
- the physical endpoint/incident-component conventions;
- the common-kernel disintegrations;
- the collision-uniform source concentration estimate still missing; or
- the correctness of the complete 207-module continuum proof chain.

The manuscript and specialist-audit map correctly state this boundary.

## 4. Scope of this mathematical audit

The complete archive contains 207 core modules and a very large inherited supplement. I have not attempted to re-prove every historical theorem. The substantive audit concentrates on:

1. the finite peak decomposition and adjustable projector interpolation in module 205;
2. the physical `s^2` incidence cap and its combination with weak multiplier bounds;
3. the marked-incidence coefficient estimate for every exponent below `3/2`;
4. the layer-cake passage from marked incidence to actual `I_m^p` moments;
5. the strict parameter range `1<p<3/2` and the finite-count remainder;
6. the positive-density trace theorem inherited from revision 87;
7. the enlarged shrinking family and the `h^(1/10)` exponent;
8. the use of one fixed auxiliary Fourier band before the collision limit;
9. the common-survivor weighted-fiber total-variation comparison;
10. the fixed-interval mass estimate for the exceptional original source;
11. the exact source-level endpoint squeeze;
12. the difference between mass decay and essential-height decay;
13. preservation of exact labels, original weights, and arithmetic classes; and
14. the requested top-four theorem and significance standard.

The inherited collision spectrum, local limit, coarea, first-exit, residence, positive-remainder, path-remainder, and collision-to-return chains are treated as source-pinned inputs. Their use is inspected at the new interfaces, but this report does not independently certify every historical argument.

## 5. Revision 86: actual mixed optical moments above one

Revision 86 first established a complete mixed moment on the actual physical source. In its notation, `z=|g|` is the endpoint-gradient norm and

\[
 I_m=1+\sum_{i=1}^{m-1}q_0^{d_i}/c_i
\]

is the additive optical sensitivity. Starting from a capped joint marked-incidence estimate, it proved finite-count bounds for

\[
 F_\#(I_m^p\mathbf1_{\{z<\zeta\}}\bar\nu)
\]

and

\[
 F_\#(I_m^p z^{-\eta}\mathbf1_{\{0<z<\zeta\}}\bar\nu)
\]

when

\[
 1<p<17/16,
 \qquad 0<\eta<1-p/2.
\]

The proof uses weighted Jensen to reduce `I_m^p` to a geometrically weighted sum of marked incidence powers. It then performs the incidence layer cake before any limit. The cap

\[
 \min\{\zeta\rho^{m/2},s^2\}
\]

is integrated exactly, producing a remainder with a genuine positive power of the exponential factor. A second, positive gradient layer cake yields the `z^{-eta}` moment.

I find the logic of this finite-count calculation coherent. In particular:

- the moment source is an actual positive source, not an asserted bounded multiplier on the anisotropic space;
- the marked powers are summed with the original geometric weights, not a physical-word count;
- the lower endpoints of both layer cakes are removed by monotone convergence only after the finite-count cap is inserted; and
- the strict inequalities on `p` and `eta` correspond to different integrability requirements and are not interchangeable.

The theorem did not prove an untruncated first inverse-gradient moment. The source correctly avoided substituting `eta=1`.

## 6. Revision 86: the complete high-sensitivity microscopic sector

Revision 86 then selected the actual source sector

\[
 I_m>s^{-\gamma}
\]

inside the fractional optical potential. On a dyadic offset interval of scale `ell_j`, the extra moment gives

\[
 I_m\mathbf1_{\{I_m>s^{-\gamma}\}}
 \le \ell_j^{\gamma(p-1)}I_m^p.
\]

After multiplying by the fractional time kernel, the dyadic exponent is

\[
 d=\gamma(p-1)-(1-\eta)/2.
\]

When `d>0`, both the leading terms and the finite-count spectral remainders form geometric series. This yields a finite-count uniform microscopic envelope before any collision limit.

For the explicit choice

\[
 p=33/32,\qquad \eta=1/4,\qquad \gamma=16,
\]

one has `d=1/8`. The selected high-sensitivity source therefore has finite-count envelope `K h^(1/8)` and ordered collision-limsup height `C h^(9/8)`.

The order of operations is correct:

1. fix one auxiliary Fourier band;
2. sum the complete nonnegative dyadic tail at finite count;
3. take the collision limit;
4. enlarge the auxiliary band; and
5. remove the outer microscopic width.

No infinite sum of collision limsups is used. This genuinely proves zero microscopic charge for the complete selected high-sensitivity sector. It does not prove the complementary moderate-sensitivity sector small, and the source states this accurately.

## 7. Revision 86: reachable-fiber localization

The unrestricted fractional potential is larger than the optical drift actually reached by the stopped transport. Revision 86 retained the physical selector

\[
 \tau^-(y)>s
\]

and defined a reachable-fiber drift on the same maximal regular exact-event segment.

This is a valid source-level improvement. A target point appears only when it can be reached by flowing a source point on that segment through roof time `s`; later re-entry is not included. Radial growth then gives a lower gradient bound along the reached target and compares the causal drift to the older fractional majorant.

The high-sensitivity part is paid by the finite-count envelope just described. The remaining causal moderate-sensitivity charge is smaller than the old fractional charge, but its vanishing was not proved. Revision 86 therefore sharpened the sufficient conditions without closing the scalar theorem.

## 8. Revision 87: a positive-density trace theorem

Revision 87 introduced an elementary but important trace estimate. Let `A>0` be locally absolutely continuous and suppose

\[
 |A'|\le DAI.
\]

For `p>1`, applying the fundamental theorem of calculus to `A^(1/p)` and then Hölder gives a pointwise bound in terms of an interior average and

\[
 \int AI^p.
\]

The use of `A^(1/p)` is appropriate: it converts the logarithmic derivative into an `L^p` energy without requiring a lower bound for `A` or an estimate on `A^{-1}`.

Applied to the exact physical angular density

\[
 A_j(u,\theta)=\frac{\omega}{4\pi c_*\chi},
\]

this trace theorem is summed through the Borel maximal-segment bijection. The longer side of each selected segment supplies an interior anchor interval; radial growth keeps every joining path away from zero gradient; and multiplicity one converts the complete angular-energy sum into the actual `I_m^p` volume source.

The resulting collared source-height theorem is credible at its stated fixed positive gradient and residence cutoffs. It does not remove those cutoffs.

## 9. Revision 87: simultaneous shrinking cutoffs

Revision 87 selected the initial family

\[
 z\ge h^{1/128},
 \qquad \ell\ge h^{1/64}.
\]

For `p=33/32`, the trace/Hölder calculation yields

\[
 \mathcal V_h^{a,\delta}(t)
 \le \frac{C_p}{a}(h/d)^{1-1/p}M_p(J_t),
\]

where `d` is the anchor scale. With the printed powers,

\[
 -\frac1{128}
 +\frac1{33}\left(1-\frac1{64}\right)
 =\frac{31}{1408}>0.
\]

Thus one fixed auxiliary band gives a finite-count uniform envelope

\[
 \sup_{m,R,n,k}m^2
 \|\mathcal V_h^{\rm reg}\|_\infty
 \le K h^{31/1408}.
\]

This estimate covers all optical sensitivities and all positive incidences on the stated initial family. It is stronger than the revision-86 high-sensitivity selection because it no longer imposes a sensitivity threshold. The complementary initial source, however, still consists of states with small initial gradient or small total residence.

## 10. Revision 87: exact original-source localization

Revision 87 kept the complementary mass as an actual original weighted source:

\[
 R_h^\varepsilon(t)
 =\int W^\varepsilon
   \mathbf1_{\{z<h^{1/128}\ \mathrm{or}\ \ell<h^{1/64}\}}
   \,d\mu_t.
\]

It then proved a two-sided comparison between the height of the complete original bad source and the ordered charge of this restriction. Combining that comparison with the positive scalar remainder gave an exact source-level equivalence between the original pointwise error and the outer limit of the residual source charge.

This is an important conceptual improvement. Earlier revisions supplied sufficient pairs of optical and residence charges. Revision 87 isolated a restriction of the original source whose charge is equivalent to the organizing endpoint.

The charge was not proved zero. The revision correctly left the full raw LLT and all unconditional downstream laws unpromoted.

## 11. Revision 88: adjustable peak-projector interpolation

Module 205 revisits the marked-incidence input. The physical incidence layer has three different kinds of information:

- a strong multiplier estimate which need not be small;
- a weak geometric estimate with a positive but limited power of the layer width; and
- the physical cap
  \[
  \nu\{c<s\}\le Cs^2.
  \]

The revision interpolates finite-rank peak projectors between strong and weak controls. On the principal peak component, this converts the physical cap into a coefficient of order `s^kappa` for every `kappa<3/2`. On the complementary spectral component, the proof retains an exponential factor and the true `s^2` cap.

The stated outcome has the form

\[
 \bigl|\ell(Q_\xi^{m-j}M_sQ_\xi^j\mathbf1)\bigr|
 \le C_\kappa s^\kappa
     +C_\kappa\min\{\rho_\dagger^{m/2},s^2\},
 \qquad \kappa<3/2.
\]

I did not find an algebraic contradiction in this argument. The use of a strict exponent below `3/2` is appropriate; the endpoint `3/2` is not claimed.

The following details remain load-bearing and should receive independent specialist verification:

1. the peak charts and finite-rank projectors must have uniform strong/weak constants across the radius family;
2. the interpolation statement must apply to every continued peak projection, including charts which appear or disappear with the parameter;
3. the weak-injectivity endpoint used to identify the interpolated functional must not assume the conclusion it proves;
4. the source/image convention in `Q^(m-j) M_s Q^j` must match the marked physical collision index;
5. dropping endpoint section indicators must occur only in a positive upper bound; and
6. the normalization by `nu_R^*` must be retained exactly once.

The manuscript identifies these as imported or specialist-sensitive points rather than software-certified facts.

## 12. Revision 88: marked incidence with every exponent below three halves

After summing the moving peak charts, module 205 derives a local marked-incidence estimate of the form

\[
 m^2\nu_R^*\{K_m^{\rm c}=k,A_m=n,F-m\bar\tau_R\in J,
                    c(T^jx)<s\}
 \le C_\kappa s^\kappa(|J|+1)
      +C_\kappa m^2\min\{\rho_\dagger^{m/2},s^2\}.
\]

The estimate preserves the exact displacement and occupation labels. Its role is not merely to improve a printed exponent: the range `kappa<3/2` permits an optical moment `p` arbitrarily close to `3/2` from below.

The true cap in the finite-count remainder is essential. Without it, the incidence layer cake would fail near zero when the threshold shrinks before the collision limit. The manuscript retains the cap and does not replace it by a limiting Gaussian term.

I found no error in the stated exponent relation. For every `p<3/2`, one may first choose `kappa` with

\[
 p<\kappa<3/2,
\]

and then integrate the positive layer cake.

## 13. Revision 88: unconditioned optical moments below three halves

Module 205 applies weighted Jensen to the complete additive sensitivity and derives an actual unconditioned moment source

\[
 u_p(t)\,dt=F_\#(I_m^p\mathbf1_\Pi\nu_R^*)
\]

for every

\[
 1<p<3/2.
\]

The finite-count interval estimate retains a fixed-band remainder with exponent determined by `2-p`. The decisive point is that the moment is proved on the original exact-label physical source; it is not postulated as a multiplier norm.

The layer-cake calculation is internally coherent:

- the incidence exponent is chosen strictly larger than `p`;
- the principal coefficient is integrable at zero;
- the physical cap controls the finite-count remainder;
- the geometric weights in `I_m` are summed without a word-count factor; and
- one fixed auxiliary band is used throughout the microscopic estimate.

This is a genuine improvement over the `p<17/16` range in revision 86.

## 14. Revision 88: the expanded shrinking family

Module 206 uses

\[
 p=10/7,
 \qquad e_p=1-1/p=3/10,
\]

and selects the larger initial family

\[
 z\ge a(h)=h^{1/8},
 \qquad \ell\ge\delta(h)=h^{1/4}.
\]

The anchor scale is

\[
 d(a(h),\delta(h))=c_dh^{1/4}
\]

for sufficiently small `h`. The trace/Hölder estimate has outside factor

\[
 a(h)^{-1}\left(\frac h{d(h)}\right)^{3/10}.
\]

The exponent arithmetic is

\[
 -\frac18+\frac3{10}\left(1-\frac14\right)
 =-\frac18+\frac9{40}
 =\frac1{10}.
\]

Thus, on the stated family,

\[
 \sup_{m,R,n,k}m^2
 \|\mathcal V_h^{\rm reg}\|_\infty
 \le Kh^{1/10}
\]

at one fixed auxiliary band.

I find this calculation correct. Compared with revision 87, the complement is strictly smaller:

- the initial-gradient threshold improves from `h^(1/128)` to `h^(1/8)` in the sense relevant to the selected set; and
- the residence threshold improves from `h^(1/64)` to `h^(1/4)`.

For small `h`, these larger threshold values make the selected regular family smaller pointwise, but the theorem is stronger in its use of the improved moment and yields a larger explicit decay exponent. The decisive source question is not which exponent is numerically larger in isolation, but whether the complementary union has zero ordered height. The manuscript does not claim that it does.

The theorem covers all positive incidences and all sensitivity values inside the selected family. It introduces no hidden internal-incidence corridor and no collision-dependent Fourier band.

## 15. Revision 88: weighted common-survivor fibers

Module 207 compares original weighted roof fibers transported along common surviving segments. Its conclusion has the form

\[
 \sup_{m,R,n,k}m^2\operatorname*{ess\,sup}_t
 \|\sigma_h(t)-\sigma_0(t)\|_{\rm TV}
 \le K\{h^{1/10}+\varepsilon^{-1}h^{1/4}\}.
\]

This is stronger than a scalar mass comparison. It controls every bounded measurable test on the common-survivor weighted fiber.

The decomposition used in the proof is plausible:

1. the smooth guard changes by a controlled amount along a surviving segment;
2. the physical Jacobian and angular density change are paid by the optical drift;
3. the Borel segment parametrization supplies multiplicity one; and
4. the common-kernel construction fixes compatible versions of the roof fibers.

The theorem does not compare the entire starting fiber to the entire translated fiber across true exits. It is explicitly a common-survivor statement. This scope is correct and must not be enlarged when applying the result to the residual exceptional source.

The most delicate verification points are:

- the transport of arbitrary bounded tests through the common physical map;
- the treatment of incident components at one-sided endpoints;
- the exact inverse-Jacobian factor;
- the common exceptional roof set used for total variation; and
- the fact that the guard modulus is uniform in every exact label.

No decisive inconsistency was found in the written argument, but these points require a human specialist audit.

## 16. The exceptional original source

Revision 88 retains the complementary original source as

\[
 R_h^\varepsilon(t)
 =\int W^\varepsilon(x)
   \mathbf1_{\{z(x)<h^{1/8}\ \mathrm{or}\ \ell(x)<h^{1/4}\}}
   \,d\mu_t(x).
\]

This is a restriction of the original weighted source. It keeps

- the original section normalization;
- all exact displacement and occupation labels;
- grazing and nongrazing endpoint types;
- all physical words;
- the smooth guard; and
- all arithmetic classes.

The two alternatives are a union rather than a double-counted sum.

The revision proves a fixed-interval mass estimate whose leading terms include positive powers such as

\[
 h^{\alpha/8}
 \quad\hbox{and}\quad
 h^{1/128},
\]

plus a fixed-band finite-count remainder.

This estimate is useful. It shows that the residual source has small normalized mass on fixed roof intervals after the stated limits. It does not prove that its normalized essential height tends to zero.

## 17. Why fixed-interval mass does not prove pointwise height

The logical distinction is decisive. Consider, schematically, a sequence of nonnegative densities

\[
 f_m(t)=m^{-2}a_m\mathbf1_{[0,a_m^{-2}]}(t),
 \qquad a_m\to\infty.
\]

Then

\[
 m^2\|f_m\|_\infty=a_m\to\infty,
\]

while for every fixed interval containing zero,

\[
 m^2\int f_m(t)\,dt=a_m^{-1}\to0.
\]

This example is not asserted to arise from the Lorentz source. It demonstrates why a fixed-interval mass estimate alone cannot establish the ordered essential-height conclusion required here.

To close the theorem one needs additional source-specific information, for example:

- a collision-uniform modulus of continuity at the microscopic scale;
- a Carleson or maximal-function estimate converting local mass to height;
- a uniform BV or directed-variation bound with admissible collision growth;
- a reverse persistence mechanism on the exceptional source itself; or
- a finite-count envelope which directly includes the union `z<a(h) or ell<delta(h)`.

The common-survivor total-variation theorem does not supply this missing information, because the exceptional source is precisely outside the selected common-survivor family.

## 18. Exact source-level endpoint equivalence

Revision 88 preserves the two-sided localization

\[
 \mathfrak R_{\varepsilon,M}
 \le\mathcal H_M(b^\varepsilon)
 \le\mathfrak R_{\varepsilon,M}+C\varepsilon^{1/16}.
\]

Combining it with the unchanged positive scalar remainder gives

\[
 \mathfrak R_{\varepsilon(B),M}
 \le\mathcal E_M+C_MB^{-1/192},
\]

and

\[
 \mathcal E_M
 \le\mathfrak R_{\varepsilon(B),M}+C_MB^{-1/192}.
\]

Consequently

\[
 \mathcal E_M
 =\lim_{B\to\infty}\mathfrak R_{\varepsilon(B),M}.
\]

This is one of the strongest conceptual conclusions in the recent revision sequence. It identifies the exact remaining obstruction on a restriction of the original source rather than on an auxiliary optical majorant.

It also makes the present publication status unambiguous. The unrestricted pointwise theorem is proved if and only if the residual original-source charge vanishes. The manuscript has not proved this vanishing.

## 19. Limit order and fixed-band discipline

The new modules generally respect the required order of limits:

1. fix the outer reconstruction band `B`;
2. fix `epsilon(B)`;
3. fix the microscopic roof width `h` and all physical cutoffs depending on it;
4. fix one auxiliary Fourier band for the finite-count moment and trace estimates;
5. take the collision-count limsup and exact-label suprema;
6. enlarge auxiliary bands only where the argument requires it;
7. remove `h`; and
8. send the outer reconstruction band to infinity last.

The module-206 finite-count envelope is particularly useful because one admissible auxiliary band is kept fixed uniformly in `h` and `m`. There is no substitution of a collision-dependent frequency band into a theorem proved only at fixed bandwidth.

The outstanding charge retains the microscopic cutoff inside the normalized height before the cutoff is removed. This is the correct formulation; it is also why fixed-cutoff results do not settle the endpoint.

## 20. Arithmetic reference and exact labels

The focused article retains the finite moving spectral-peak reference, including active noncentral peaks and arithmetic zero classes. The new source estimates do not replace this reference by one Gaussian term.

The marked-incidence and moment inputs keep the exact displacement and occupation labels. Positive upper comparisons may drop endpoint tests, but the final source and target do not pool labels.

The endpoint squeeze is unnormalized and remains meaningful on arithmetic zero classes. Conditional path laws, density ratios, and forward likelihoods are stated only on positive reference classes. This scalar-first order is correct and should be preserved.

## 21. Downstream consequences remain conditional

Because the scalar pointwise endpoint remains open, the following conclusions are not yet unconditional:

- the full raw exact-label actual-return LLT;
- the pointwise roof-density LLT;
- a uniform positive pointwise denominator on every positive arithmetic class;
- same-roof collision path conditioning;
- the actual-return path bridge after clock transfer; and
- forward essential arithmetic likelihood convergence.

The active manifest correctly leaves these flags false. The equality of scalar and bounded-Lipschitz path-numerator errors from revision 73 means that no second independent numerator-height theorem is needed after scalar closure. It does not allow path normalization before scalar closure.

## 22. Mathematical significance at the requested benchmark

The accumulated manuscript contains a large amount of original work:

- explicit periodic arithmetic for the exact return record;
- anisotropic collision operators with physical roof twists;
- compact-frequency and local-limit analysis;
- positive source decompositions and raw inversion;
- coarea transport and first-exit geometry;
- complete maximal-segment parametrization;
- optical moment estimates above one;
- finite-count microscopic envelopes;
- residence-band persistence;
- weighted-fiber stability; and
- an exact original-source endpoint criterion.

Revisions 86--88 materially sharpen the endpoint analysis. In particular, the program has moved from broad sufficient optical charges to an exact concentration charge on the original source.

Nevertheless, the requested benchmark is determined by proved theorems, not by the sophistication of a reduction. The title and opening continue to organize the paper around an unrestricted exact-label pointwise raw local limit theorem. That theorem remains equivalent to an unproved source-concentration assertion.

The remaining assertion is not plainly a routine estimate. It must exclude concentration precisely where both the initial endpoint gradient and total regular residence collapse with the microscopic roof scale. These are the most singular physical configurations in the proof.

At a top-four level, the paper needs either

1. a proof that this original source charge is zero, completing the stated endpoint and its scalar-first consequences; or
2. a separate theorem of broad independent significance, with quantitatively checkable hypotheses and multiple genuinely different realizations, so that the article no longer depends editorially on the unfinished Lorentz endpoint.

Revision 88 supplies neither endpoint yet.

## 23. Required mathematical changes before another top-four review

### 23.1. Prove the original exceptional-source charge is zero

The central task is

\[
 \lim_{B\to\infty}\mathfrak R_{\varepsilon(B),M}=0
\]

for every fixed central radius `M`.

The proof must preserve

- the original exact labels;
- the smooth guard;
- the exact section normalization;
- all endpoint types;
- the finite arithmetic reference and zero classes; and
- the legal order of microscopic and collision limits.

A fixed-interval mass estimate is not sufficient.

### 23.2. Supply a microscopic mass-to-height mechanism

A viable next theorem should convert the new interval-mass bounds into essential-height decay by an additional collision-uniform mechanism. Possibilities include a source-specific reverse-persistence inequality, a maximal estimate, a uniform oscillation theorem, or a local variation bound with acceptable collision growth.

The theorem must act on the exceptional union itself, not only on its complementary common-survivor family.

### 23.3. Reconcile criticality and zero residence geometrically

The residual source is the union

\[
 z<h^{1/8}
 \quad\hbox{or}\quad
 \ell<h^{1/4}.
\]

The next proof should identify whether these mechanisms can occur independently at the normalized pointwise scale or whether the billiard geometry forces a compensating persistence, angular-volume, or incidence gain.

A union bound by two fixed-scale mass estimates will not by itself close the essential-height charge.

### 23.4. Independently audit the adjustable peak interpolation

A specialist should verify:

- the moving peak charts and projectors;
- strong-to-weak interpolation constants;
- the physical `s^2` cap;
- the principal/remainder decomposition at every collision position;
- source/image conventions for marked insertions; and
- uniformity in the radius parameter.

### 23.5. Independently audit the segment and fiber constructions

The following should also be checked line by line:

- the Borel maximal-segment bijection;
- multiplicity one after angular summation;
- the physical density `omega/(4 pi c_* chi)`;
- one-sided endpoint traces;
- common-kernel roof disintegration;
- the inverse-Jacobian payment; and
- the total-variation comparison for transported weighted fibers.

### 23.6. Keep downstream laws conditional until scalar closure

No point-conditioned path law, density ratio, return bridge, or forward likelihood should be promoted before the scalar charge is proved zero. Arithmetic zero classes must remain in the unnormalized theorem and must not be divided by.

## 24. Expository and architectural comments

1. The focused article is preferable to the historical all-in-one manuscript, but the complete supplement remains exceptionally large. A formal submission should separate the indispensable proof from provenance and historical revisions more aggressively.
2. The paper should include one dependency diagram from the final source charge back to the exact spectral and geometric inputs, with theorem labels and current-page references.
3. The phrase “expanded shrinking family” should always be accompanied by the explicit inequalities defining the selected family; otherwise it is easy to confuse a larger threshold with a larger selected set.
4. Keep the finite-count remainder visible whenever the lower incidence or gradient cutoff moves. The leading constant alone does not justify cutoff removal.
5. State near the main theorem that interval mass is not pointwise height. This is the final logical distinction.
6. The fixed auxiliary band used in module 206 should be named once and kept distinct from the outer inversion band throughout.
7. The report packet should update the qualification status only after the exact-SHA runs complete. A queued workflow is not passing evidence.
8. The active manuscript should continue to state explicitly that no independent human specialist audit has been obtained.
9. The final journal version should not ask readers to reconstruct the current theorem from historical status files. One authoritative theorem/assumption ledger should suffice.
10. Source receipts, finite fixtures, and rendering diagnostics should remain outside the mathematical argument.

## 25. Final assessment

Revision 88 is a substantial advance over revision 85 and a meaningful continuation of revisions 86 and 87.

It proves or materially strengthens:

- actual optical moments `I_m^p` for every `1<p<3/2`;
- marked-incidence local bounds with every exponent below `3/2`;
- a complete finite-count optical envelope on the family
  \[
  z\ge h^{1/8},\qquad \ell\ge h^{1/4},
  \]
  with decay `h^(1/10)`;
- total-variation stability of original weighted common-survivor fibers;
- a small fixed-interval mass estimate for the complementary original source; and
- preservation of the exact source-level equivalence between the residual charge and the original pointwise error.

I found no decisive flaw in modules 199--207 at the level of this referee-style audit. The most delicate imported spectral, coarea, segment, and fiber inputs still require independent human verification.

The revision does not prove

- zero ordered concentration charge for the original exceptional source;
- the unrestricted exact-label pointwise raw LLT;
- the pointwise roof-density LLT; or
- the unconditional path, clock, and likelihood consequences.

The organizing theorem therefore remains open within the submitted manuscript.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
