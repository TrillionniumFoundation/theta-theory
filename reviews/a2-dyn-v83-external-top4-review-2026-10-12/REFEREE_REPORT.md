# External top-four referee report on A2-DYN revision 83

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v83-referee-response-2026-10-11`, `revision/a2-dyn-v83-referee-copy-2026-10-11`  
**Reviewed commit:** `658f42b2ce6c177687208287201abb7a86193e37`  
**Reviewed repository tree:** `78858b2b18f40d777bf3ae1d5aeee377b7590f48`  
**Active manuscript directory:** `papers/A2-DYN-v83-referee-response`  
**Journal entry / technical supplement:** `main.tex` / `supplement.tex`  
**Active mathematical source:** one hundred ninety-two numbered core modules; revision 82 adds module 189 and revision 83 adds modules 190--192  
**Preserved revision-82 author baseline:** `81012268c5b8826a188a77715a84e75b1e1aa002`  
**Preserved revision-82 paper tree:** `d1908253a6d134b5b1e4c732e84ad111ad4f836a`  
**Controlling external report:** `reviews/a2-dyn-v81-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `614b15b2bb77f2887e95f685a0cfb6b2db44e99d` / `818e5932c895aea686da68fe37cec6018d2de759`  
**Final-SHA qualification runs:** response `38155950212`; referee-copy `38155972991`  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, optical-geometry, geometric-measure-theory, harmonic-analysis, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 83 contains genuine and substantial new mathematics. It should be evaluated together with revision 82, because module 189 was introduced after the last external report and revision 83 uses and corrects its dyadic endpoint formulation. I therefore audited the four-module increment

- `core/189_dyadic_critical_source_criterion.tex`;
- `core/190_untruncated_optical_potentials.tex`;
- `core/191_complete_first_exit_surface_mass.tex`;
- `core/192_ordered_fractional_tail_and_endpoint.tex`;

as well as their direct interfaces with the revision-81 joint endpoint/incidence estimates, actual fractional insertions, common coarea kernels, optical transport, positive scalar remainder, and first-exit identities.

The new revision crosses two important thresholds.

First, the optical argument is no longer restricted by a positive initial lower cutoff on the endpoint gradient. For every fixed `0 < eta < 1/2`, the manuscript uses the actual untruncated source with insertion

\[
 I_m |g|^{-\eta},
\]

and proves a complete fractional-potential comparison for optical loss and genuine grazing first-exit starting mass. It then obtains local weak-`L^q` estimates for every fixed `2 < q < 4`, together with a quantitative critical-width gain.

Second, the manuscript now treats the actual nongrazing outgoing first-exit surface assignment itself. It does not relabel a volume multiplier theorem as a boundary theorem. By combining a complete starting-source estimate with both signs of optical variation, it proves a local interval-mass estimate for the one-sided first-exit surface source. On roof intervals of length `r`, the collision-normalized surface-assignment mass is `O(r^(33/32))`.

These are real advances over revision 81. I found no decisive counterexample, sign reversal in the optical variation, omitted exact label, hidden section renormalization, illegal collision-dependent Fourier band, or improper exchange of the critical cutoff and collision limits in the newly stated theorems. The source is also unusually explicit about what the new local norms and interval masses do **not** imply.

The negative recommendation is nevertheless unavoidable because the organizing theorem of the article remains unproved. Revision 83 reduces the original pointwise error to two nonnegative quantities:

1. the complete microscopic fractional tail, retained inside the normalized essential supremum and collision limsup; and
2. the full untruncated nongrazing first-exit surface **essential height**.

Neither quantity is proved to vanish as the outer roof width tends to zero.

The new weak-`L^q` estimate is finite only for `q < infinity`; it cannot be promoted to an `L^infinity` estimate without additional regularity or a microscopic envelope. Likewise, an `O(r^(33/32))` mass bound on every interval of length `r` is stronger than a bare finite measure statement but still permits peaks whose width shrinks with the collision count and whose normalized essential height does not vanish. The manuscript correctly acknowledges both facts.

Thus revision 83 proves that the two final positive mechanisms are locally integrable, quantitatively small in natural local norms, and attached to the correct physical volume and surface sources. It does not prove them pointwise small on the moving microscopic roof scale required by the exact-label local limit theorem.

At the requested benchmark, an exact characterization of the final obstruction is not a substitute for closing it.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`658f42b2ce6c177687208287201abb7a86193e37`.

The repository tree is

`78858b2b18f40d777bf3ae1d5aeee377b7590f48`.

The active directory is

`papers/A2-DYN-v83-referee-response`.

Revision 82 at

`81012268c5b8826a188a77715a84e75b1e1aa002`

is the immediate author baseline. It added module 189, a dyadic criterion for the critical Abel source. Revision 83 adds modules 190--192 and assembles a focused journal article together with the complete inherited supplement.

The source manifest records one hundred eighty-nine inherited core modules and one hundred ninety-two active modules. It states that every inherited core, Python source, appendix, bibliography, and provenance file is byte-preserved. The complete revision-81 and revision-82 articles are retained in the supplement.

The source also preserves the historical bytes of module 189. That module defines its dyadic interval as an absolute roof interval and then writes an integral in an offset variable over that same interval. Revision 83 identifies this mismatch explicitly and gives the unambiguous active definition in module 192:

\[
 ℓ_j^{-\kappa}\int_{ℓ_j/2}^{ℓ_j}v(t+s)\,ds,
\]

or equivalently integration of `v(u)` over

\[
 (t+ℓ_j/2,t+ℓ_j].
\]

I regard the corrected module-192 formulation as the active mathematical statement. The historical module-189 display should not be quoted independently without the adjacent clarification.

The present review branch starts directly from the final reviewed author SHA and adds only this report under

`reviews/a2-dyn-v83-external-top4-review-2026-10-12/`.

No author manuscript, workflow, prior report, historical paper, or unrelated repository path is intentionally modified.

## 3. Exact-source qualification and its boundary

The final-SHA qualification workflows completed successfully on both author refs:

- response branch run `38155950212`;
- referee-copy branch run `38155972991`.

Both runs use the reviewed SHA

`658f42b2ce6c177687208287201abb7a86193e37`.

According to the workflow and validation protocol, the qualification checks include

- the exact revision-82 paper tree;
- the controlling revision-81 report blob;
- byte preservation of all inherited sources;
- normal and optimized finite-fixture agreement;
- native compilation of the focused article and complete supplement;
- recorder coverage of all one hundred ninety-two core modules;
- stabilized references and warning gates; and
- PDF geometry and rendering checks.

The repository records a thirteen-page focused article, a six-hundred-thirty-four-page complete supplement, and 3,616 new finite fixtures for the revision-83 layer.

These checks are meaningful evidence of source identity, preservation, algebraic consistency, and successful typesetting. They do not prove

- the inherited four-record spectral theorem;
- the continued-peak Gaussian expansion;
- the common exact-label coarea identities;
- the optical derivative formula;
- the first-exit face decomposition;
- the weak-`L^q` potential theorem in the continuum;
- the microscopic tail decay; or
- the surface essential-height decay.

A successful CI run is not an independent specialist proof audit.

## 4. Scope of this review

The complete supplement contains one hundred ninety-two modules and a long inherited proof pipeline. I have not attempted to re-prove every historical theorem. The substantive audit concerns

1. the dyadic critical-source criterion and its corrected offset convention;
2. the untruncated fractional optical transport inequality;
3. the localized weak-`L^q` potential estimate;
4. the complete optical weak-height theorem;
5. the true-exit starting-mass estimate;
6. the definition of the actual nongrazing outgoing first-exit surface assignment;
7. the two-sided optical payment of the surface source and its pullback;
8. the local interval-mass estimate for that surface assignment;
9. the ordered microscopic tail decomposition;
10. the final exact-label pointwise error budget;
11. the additional finite-count envelope criterion; and
12. source identity and qualification evidence.

The inherited joint endpoint/incidence localization, actual fractional insertion theorem, complete-source fixed-width estimates, common-kernel covariance, optical normalization, all-contact motion estimate, positive scalar remainder, arithmetic reference, path remainder, and collision-to-return transfer are treated as source-pinned inputs. This report does not independently certify all of those chains.

## 5. The dyadic criterion and the corrected roof variable

Module 189 isolates the correct conceptual issue: a fixed-width concentration theorem does not by itself control an Abel kernel singular at zero. Splitting `(0,r]` into dyadic annuli gives the elementary bound

\[
 ∫_0^r s^{-1/2}v(t+s)\,ds
 ≤ C\sum_{j≥0}(2^{-j}r)^{-1/2}
       ∫_{2^{-j-1}r}^{2^{-j}r}v(t+s)\,ds.
\]

The important point is not the inequality itself but the order of limits. Bounds for each fixed dyadic scale do not control the collision limsup of the infinite sum unless the tail is uniform before the collision limit.

This warning is correct and remains essential in revision 83.

The literal variable notation in module 189 is inconsistent, as noted above. Module 192 repairs it by making the integration variable an offset. The repaired statement is mathematically coherent and preserves the intended dyadic partition.

I recommend that any submission copy either correct the display directly or label the historical module explicitly as superseded. A reader should not have to reconcile two different meanings of the same interval notation across the article and supplement.

## 6. Fractional optical transport without a lower cutoff

Let

\[
 z=|g|,
  \kappa_\eta=\frac{1-\eta}{2},
  Q_\eta=\kappa_\eta^{-1},
  0<\eta<\frac12.
\]

Then

\[
 \frac14<\kappa_\eta<\frac12,
   2<Q_\eta<4.
\]

The manuscript uses the actual source with insertion

\[
 I_m z^{-\eta},
\]

whose fixed-width concentration was proved in revision 81. It does not first truncate at `z=a`, take the collision limit, and subsequently send `a` to zero.

Along a regular survivor the inherited optical estimate is

\[
 |X\omega|\le C\omega I_m z^{-1},
\]

and radial growth gives

\[
 z(\Phi_sx)^2\ge z(x)^2+2\lambda_\circ s.
\]

Consequently

\[
 z(\Phi_sx)^{-1}
 ≤ C_\eta s^{-(1-\eta)/2}z(\Phi_sx)^{-\eta}.
\]

This is the correct interpolation between the singular time kernel and the actual fractional spatial insertion. Target-direction coarea covariance then gives

\[
 O_h^\varepsilon(t)+E_h^{\varepsilon,\mathrm{gr}}(t)
 ≤ C_\eta\int_0^h s^{-\kappa_\eta}v^\eta(t+s)\,ds.
\]

The proof uses negative optical variation to pay both surviving optical loss and the full starting mass of a genuine grazing exit. Those source classes are disjoint. The boundary value `\omega=0` is used only to identify the terminal optical value at a grazing exit; it is not used to declare the positive starting mass zero.

Within the stated inherited coarea framework, I found this argument internally coherent.

The load-bearing specialist checks are

- the common target-fiber version for every exact label;
- the ratio between source and target angular normalizations;
- the fact that the complete insertion `I_m z^{-eta}` is evaluated on the same target source;
- the monotone removal of compact flow-box truncations; and
- preservation of the first-exit and survivor selections under the common kernel.

Finite diagnostics cannot verify these continuum facts.

## 7. The localized weak-`L^q` estimate

Revision 83 defines

\[
 \mathcal N_Q(f;J)=
 \sup_{E\subset J,\,0<|E|<\infty}
 |E|^{-1+1/Q}∫_E f(t)\,dt.
\]

For the one-sided kernel

\[
 \mathsf P_{\eta,r}v(t)=∫_0^r s^{-\kappa_\eta}v(t+s)\,ds,
\]

it proves

\[
 \mathcal N_{Q_\eta}(\mathsf P_{\eta,r}v;J)
 ≤\frac{1}{1-\kappa_\eta}∫_{J+(0,r)}v(y)\,dy.
\]

This is the standard endpoint fractional-integration mechanism in a localized form. For a measurable set `E` of measure `a`, the decreasing kernel integrates over `E` by at most

\[
 \frac{a^{1-\kappa_\eta}}{1-\kappa_\eta}.
\]

Since `1/Q_eta = kappa_eta`, division by the normalization in `N_Q` is exact.

Combining this with the actual fixed-width source estimate gives, for every fixed interval length `L` and roof width `r`,

\[
 \limsup_m\sup_{R,n,k}\sup_{|J|=L}
 \mathcal N_{Q_\eta}(m^2D_r^\varepsilon;J)
 ≤ C_\eta(L+r),
\]

where

\[
 D_r^\varepsilon=\bar O_r^\varepsilon+
                  \bar E_r^{\varepsilon,\mathrm{gr}}.
\]

For initial critical width `b`, the corresponding bound gains

\[
 b_r^{\alpha-\eta},
   \alpha=\frac{129}{128}.
\]

The conversion to `L^p` for `p<Q_eta` has the expected factor

\[
 \left(\frac{Q_\eta}{Q_\eta-p}ight)^{1/p}
 L^{1/p-1/Q_\eta}.
\]

I found no exponent mismatch in these statements.

The endpoint is deliberately excluded:

\[
 p=\infty
\]

is not available. This exclusion is mathematically decisive, not a technical omission in the wording.

## 8. Why the weak-`L^q` result does not close the pointwise theorem

A uniformly bounded weak-`L^q` norm with finite `q` controls the distribution function of large values:

\[
 |\{f>\lambda\}\cap J|
 ≤ \min\{|J|,(A/\lambda)^q\}.
\]

It does not bound the essential supremum.

In the present problem a sequence may concentrate normalized mass on roof intervals whose widths tend to zero with the collision count. Its local weak-`L^q` norm may remain uniformly bounded while its essential height diverges or fails to vanish.

The critical gain improves the measure of such peaks but does not by itself exclude them on every moving central roof target. A uniform modulus, bounded variation estimate at the correct normalized scale, reverse Hölder estimate, or finite-count microscopic envelope would be needed to pass from the local weak norm to the required pointwise conclusion.

The manuscript does not claim otherwise. This is one of its strongest points of mathematical discipline.

## 9. All true exits in a fixed roof interval

Revision 83 defines the unweighted starting mass of trajectories exiting the original regular exact event by time `h`:

\[
 e_h(t)=∫\mathbf1_{\{\tau(x)\le h\}}\,d\mu_t(x).
\]

Every exact label, both section tests, and the original source normalization are retained.

The all-contact motion estimate implies that a true exit before `r` must enter one of the following starting layers:

- a small incidence layer;
- a small third-obstacle clearance layer; or
- a small distance-to-section-boundary layer.

The first two are controlled by the complete physical bad source with guard parameter proportional to `sqrt(r)`. Since the bad-source exponent is `1/16`, this contributes `r^(1/32)`. The section layers use the marked transverse-strip estimate and sum over depths geometrically.

The resulting finite-count bound is

\[
 m^2∫_J e_r(t)\,dt
 ≤ C r^{1/32}(|J|+B_*^{-1})
 +C_{B_*}(1+B_*|J|)m^3\rho_{B_*}^{m/2}.
\]

After the collision limit at fixed `r,L,B_*` and then enlargement of the auxiliary band,

\[
 \limsup_m\sup_{R,n,k}\sup_{|J|=L}
 m^2∫_J e_r(t)\,dt
 ≤ C Lr^{1/32}.
\]

The proof does not multiply a wordwise estimate by an uncontrolled number of words. It sums actual collision marks by depth and retains the exact displacement and occupation coefficient.

Subject to the inherited marked-strip and complete bad-source inputs, I found this estimate coherent.

## 10. The actual nongrazing outgoing surface assignment

The manuscript defines the outgoing physical flux on one-sided nongrazing faces by

\[
 d\zeta=
 \frac{\omega(b(\vartheta),\vartheta)}
      {4\pi c_*\chi(b(\vartheta),\vartheta)}\,d\vartheta.
\]

The starting-roof assignment is

\[
 \mathcal F_h(t)=∫_{\Gamma_{\rm ng}^+}
 \mathbf1_{\{0<L(y)-t\le h,\,L(y)-t<\tau^-(y)\}}\,d\zeta(y).
\]

This definition retains

- the one-sided incident physical component;
- first-exit selection;
- backward lifetime in the same exact event;
- competing-hit faces;
- section faces; and
- all initial momenta.

No lower cutoff on `|g|` remains.

This is the correct object to estimate. It is a surface measure, not a volume source with an indicator multiplier.

## 11. Two-sided optical payment

For a nongrazing first-exit orbit, write

\[
 w(s)=\omega(\Phi_sx).
\]

The two elementary inequalities

\[
 w(\tau-)
 ≤ w(0)+∫_0^\tau[w'(s)]_+\,ds,
\]

and

\[
 w(0)
 ≤ w(\tau-)+∫_0^\tau[-w'(s)]_+\,ds
\]

are used in different directions.

The first controls the outgoing surface assignment by starting mass plus positive optical variation:

\[
 \mathcal F_h(t)
 ≤ C e_h(t)+C_\eta\mathsf P_{\eta,h}v^\eta(t).
\]

The second controls the original exit and optical source by the outgoing assignment plus negative optical variation:

\[
 E_h^\varepsilon(t)+O_h^\varepsilon(t)
 ≤ C\mathcal F_h(t)+C_\eta\mathsf P_{\eta,h}v^\eta(t).
\]

At a grazing exit, the terminal optical weight vanishes and negative variation pays the complete positive starting weight. On a survivor it pays the optical loss. These cases are disjoint.

The argument retains the inverse forward Jacobian through the optical comparison; it does not silently replace that Jacobian by one.

This two-sided construction is a significant improvement over revision 81. It supplies a theorem for the actual surface source itself.

## 12. The surface local-mass theorem

Averaging the first two-sided inequality and applying the true-exit starting-mass estimate and the fractional potential estimate gives

\[
 \limsup_m\sup_{R,n,k}\sup_{|J|=L}
 m^2∫_J\overline{\mathcal F}_r(t)\,dt
 ≤ C Lr^{1/32}
 +C_\eta(L+r)r^{(1+\eta)/2}.
\]

For `L=r<1`, the first term is

\[
 Cr^{33/32}.
\]

The second term has exponent

\[
 1+\frac{1+\eta}{2}>\frac32,
\]

and is therefore smaller for small `r`. The printed `O(r^(33/32))` conclusion is consistent.

This is a strong local-mass theorem for the actual first-exit surface assignment. It is not merely the existence of a finite boundary measure.

I found no exponent error in this deduction.

## 13. Why the surface mass theorem is still not a surface height theorem

The original pointwise problem requires

\[
 \mathfrak F_M^{\rm all}(r)
 =\limsup_m\sup_{R,n,k}m^2
   \operatorname*{ess\,sup}_{t\in\mathcal C(M)}
                    \overline{\mathcal F}_r(t)
\]

to become small as `r` tends to zero.

The local-mass estimate controls

\[
 m^2∫_J\overline{\mathcal F}_r(t)\,dt
\]

for intervals of a prescribed positive length. It does not control the essential supremum.

Even the `O(r^(33/32))` estimate on intervals of length `r` permits a peak of height `r^{-a}` supported on a much smaller interval, provided its mass remains within the stated budget. If the location and width of this peak depend on the collision count, no fixed-scale limit prevents it from entering the central essential supremum.

A surface analogue of a reverse Hölder estimate, a normalized BV or modulus bound, a finite-count microscopic envelope, or a direct surface spectral insertion theorem could bridge the gap. Revision 83 proves none of these.

The source manifest correctly records

`surface_mass_bound_promoted_to_essential_height: false`.

## 14. The ordered microscopic fractional tail

Revision 83 defines

\[
 ℓ_j=2^{-j}r
\]

and the finite-count tail

\[
 T_{\eta,r,N}(t)=
 \sum_{j=N}^{\infty}ℓ_j^{-\kappa_\eta}
 ∫_{ℓ_j/2}^{ℓ_j}v^\eta(t+s)\,ds.
\]

This is formed before any collision limit.

On each dyadic annulus the fractional kernel lies between

\[
 ℓ_j^{-\kappa_\eta}
  \text{and} 
 2^{\kappa_\eta}ℓ_j^{-\kappa_\eta}.
\]

Therefore

\[
 T_{\eta,r,0}(t)
 ≤ \mathsf P_{\eta,r}v^\eta(t)
 ≤ 2^{\kappa_\eta}T_{\eta,r,0}(t).
\]

For any fixed finite number of dyadic scales, the interval lengths are fixed before the collision limit. The actual fixed-width source theorem gives a normalized contribution

\[
 C_\etaℓ_j^{1-\kappa_\eta}.
\]

The finite head therefore sums to

\[
 C_\eta r^{1-\kappa_\eta}
 =C_\eta r^{(1+\eta)/2}.
\]

The complete remaining tail stays inside the normalized essential supremum and collision limsup. Only afterwards is the dyadic truncation index sent to infinity.

This order is correct. It avoids the false inference

\[
 \limsup_m\sum_j a_{m,j}
 ≤ \sum_j\limsup_m a_{m,j}
\]

for an uncontrolled infinite family of nonnegative terms.

## 15. The exact remaining microscopic quantity

The ordered tail height is

\[
 \mathfrak T_{\eta,M}(r)
 =\lim_{N\to\infty}\limsup_m\sup_{R,n,k}m^2
 \operatorname*{ess\,sup}_{t\in\mathcal C(M)}
 T_{\eta,r,N}(t).
\]

The potential height satisfies

\[
 \mathfrak P_{\eta,M}(r)
 ≤ C_\eta r^{(1+\eta)/2}
       +2^{\kappa_\eta}\mathfrak T_{\eta,M}(r).
\]

Thus the finite dyadic head is controlled. The infinite microscopic tail remains.

The new weak-`L^q` theorem does not prove that tail zero. It controls the measure of large values at fixed local scales, whereas `mathfrak T` retains every scale down to zero before the collision limit.

The source manifest correctly records

`complete_microscopic_fractional_tail_height_decay_proved: false`.

## 16. The final pointwise error budget

The manuscript proves

\[
 \begin{split}
 \mathcal E_M\le{}&C_MB^{-1/192}
 +C\mathfrak F_M^{\rm all}(r)
 +C_\eta\mathfrak T_{\eta,M}(r)\\
 &+C_\eta r^{(1+\eta)/2}
 +C_\Theta(1+\varepsilon(B)^{-1})\sqrt r.
 \end{split}
\]

Here

\[
 \varepsilon(B)=A_0B^{-1/12},
\]

and all widths and auxiliary bands are fixed before the collision limsup.

Choosing

\[
 r(B)=c\varepsilon(B)^\gamma,
  \gamma>2,
\]

makes the explicit elementary errors vanish. The original exact-label pointwise theorem would follow if

\[
 \mathfrak F_M^{\rm all}(r)\to0
  \text{and} 
 \mathfrak T_{\eta,M}(r)	o0
\]

as `r` tends to zero.

These two limits are not proved.

This is the decisive mathematical reason for the recommendation.

## 17. The additional microscopic envelope is a criterion, not a theorem

Revision 83 formulates a useful sufficient condition. Suppose that, uniformly at finite collision count,

\[
 m^2∫_0^s v^\eta(t+u)\,du\le H(s),
\]

where `H` is nondecreasing and

\[
 ∫_0^{r_0}H(s)s^{-1-\kappa_\eta}\,ds<\infty.
\]

Then the ordered microscopic tail vanishes.

In particular,

\[
 H(s)\le As^{\kappa_\eta+\delta},
  \delta>0,
\]

gives the explicit tail estimate

\[
 m^2T_{\eta,r,N}(t)
 ≤\frac{Ar^\delta2^{-N\delta}}{1-2^{-\delta}}.
\]

This criterion is correct and useful. It identifies the finite-count uniformity actually needed.

It is not established for the Lorentz source in the manuscript. A list of fixed-scale collision limsups is not the same as the uniform finite-count envelope.

## 18. Exact labels, arithmetic classes, and limit order

The new arguments preserve

- the original section `Y_R^*`;
- the exact displacement `k`;
- the exact occupation coefficient `n`;
- terminal section membership;
- the original source normalization `c_*^{-1}`;
- all finite arithmetic peaks; and
- all zero arithmetic classes in the unnormalized theorem.

Positive upper comparisons sometimes drop endpoint tests, but only on the upper side and with the single stated normalization cost. They do not pool neighboring occupation labels.

The order of limits is also stated correctly:

1. fix the outer Fourier band, guard scale, roof width, and auxiliary bands;
2. take the collision limsup;
3. enlarge auxiliary bands;
4. take the outer band last.

No collision-dependent spectral band is inserted into a fixed-band theorem.

The dyadic tail and surface height are retained inside the collision-normalized pointwise norm rather than reconstructed from fixed-scale limits after the fact.

## 19. Downstream conditional statements remain conditional

The inherited positive path-remainder theorem identifies the ordered scalar pointwise error with the bounded-Lipschitz path-numerator error. Therefore no second independent numerator height theorem is needed after scalar closure.

However, scalar closure has not occurred.

Consequently the manuscript still does not establish unconditionally

- the exact-label raw pointwise local limit theorem;
- the pointwise roof-density local limit theorem;
- the same-roof collision-path bridge;
- the actual-return path bridge after clock transfer; or
- forward essential arithmetic likelihood convergence.

Normalization is appropriately restricted to positive arithmetic reference classes. Zero classes are not assigned conditional laws.

## 20. Specialist audit obligations

No independent human specialist audit is recorded. The following checks are load-bearing.

### 20.1 Fractional volume source

A billiards/anisotropic-spaces specialist should verify

- the revision-81 joint endpoint/incidence characteristic pairing;
- the physical cap on every real frequency;
- both positive layer cakes including finite-count remainders;
- the continued-peak normalization by a physical peripheral vector;
- the use of bounded strong approximants for stable-curve length estimates; and
- the exact fixed-band Gaussian coefficient extraction.

### 20.2 Optical and coarea transport

An optical-geometry/geometric-measure-theory specialist should verify

- the mixed-coordinate optical derivative;
- the endpoint angular normalization;
- target-direction coarea covariance;
- joint measurable source and surface kernels;
- exhaustion of the regular first-exit graph;
- the treatment of grazing terminal optical weight;
- one-sided nongrazing face orientations; and
- first-exit selection without later re-entry multiplicity.

### 20.3 Microscopic endpoint

A harmonic-analysis/probability specialist should verify

- the exact weak-`L^q` normalization;
- the dyadic tail order of limits;
- the distinction between local mass, weak norm, and essential height;
- the finite-count Dini envelope criterion; and
- any future mechanism proposed to upgrade the two local estimates to pointwise decay.

The successful finite fixtures and native builds do not perform these audits.

## 21. Significance and presentation at the requested benchmark

The focused article is substantially improved as a reading object. It isolates the final transport and endpoint mechanisms, while the complete historical pipeline remains in a supplement.

The mathematical package is also stronger than in the last report:

- actual untruncated fractional optical transport;
- complete weak-`L^q` optical bounds for `2<q<4`;
- quantitative critical localization;
- all true-exit interval mass;
- an actual first-exit surface-source theorem;
- two-sided optical comparison; and
- an exact ordered-tail criterion.

These results may be of independent interest in dispersing billiards, singular transfer operators, and boundary transport.

At a top-four level, however, the article is still organized around the exact-label raw pointwise theorem. That theorem is not proved. The two remaining conditions are not peripheral technicalities: they are exactly the passage from local mass/integrability to microscopic pointwise control.

Nor has the manuscript yet extracted the new weak-`L^q` and surface-mass mechanism as a general theorem for a broad class of singular hyperbolic systems with multiple independent applications. The completed results remain deeply tied to the one Lorentz family and its long inherited pipeline.

Thus neither route to a positive top-four recommendation is complete:

1. the source-specific organizing theorem remains conditional; and
2. a broader stand-alone theorem of comparable significance has not yet replaced it as the principal endpoint.

## 22. Required mathematical changes before another top-four review

A genuinely new revision should address the following items.

1. **Prove microscopic fractional-tail decay.** Establish a uniform finite-count envelope, Dini estimate, scale recursion, normalized variation bound, or another theorem implying
   \[
   \mathfrak T_{\eta,M}(r)	o0.
   \]
   Separate fixed-scale limsups are insufficient.

2. **Prove full surface essential-height decay.** Upgrade the interval-mass estimate for the actual one-sided first-exit surface source to
   \[
   \mathfrak F_M^{\rm all}(r)	o0.
   \]
   A local mass theorem must not be relabeled as this conclusion.

3. **Preserve the legal limit order.** Any microscopic scale may depend on the outer band, but it must be fixed before the collision limit. No collision-dependent Fourier band or post-limit cutoff removal may be introduced.

4. **Retain exact physical data.** Do not pool occupation labels, delete zero arithmetic classes, modify the section, or replace the first-exit surface by a volume surrogate.

5. **Normalize the dyadic statement.** The active submission should contain one unambiguous offset-variable definition. Historical preservation may remain in provenance, but a theorem with inconsistent variables should not remain an unqualified active reference.

6. **Obtain independent specialist review.** The revision-81 spectral insertion chain and the revision-83 surface/coarea chain require expert line-by-line checking.

7. **State a theorem commensurate with the submission.** Either finish the original exact-label pointwise theorem or formulate and prove a reusable general local-norm/surface-transport theorem with genuinely different applications.

## 23. Final assessment

Revision 83 is a serious mathematical advance.

It removes the artificial initial cutoff from the fractional optical transport, obtains complete weak-`L^q` bounds, proves quantitative true-exit interval mass, constructs and estimates the actual nongrazing outgoing surface assignment, and states the remaining pointwise obstruction in the correct ordered form. I found no decisive flaw in the four newly audited modules.

The manuscript also draws the crucial distinctions correctly:

- actual source versus auxiliary source;
- volume versus surface;
- local mass versus height;
- weak-`L^q` versus `L^infinity`;
- fixed-scale limits versus a uniform microscopic tail; and
- fixed-count cutoff removal versus exchange with the collision limit.

Nevertheless, the exact-label pointwise theorem remains conditional on two unproved essential-height decays. The full raw return LLT, pointwise roof-density LLT, and unconditional downstream path and likelihood statements are therefore still open in the submitted proof chain.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
