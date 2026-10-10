# External top-four referee report on A2-DYN revision 72

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v72-referee-response-2026-10-11`, `revision/a2-dyn-v72-referee-copy-2026-10-11`  
**Reviewed commit:** `295800b658aa2ff3aada1707d5785ff757d60724`  
**Reviewed repository tree:** `a9aefcf74a273523d1e7538fdd1e17e887eaf2d7`  
**Active manuscript directory:** `papers/A2-DYN-v72-referee-response`  
**Active mathematical source:** one hundred fifty-nine numbered core modules; revision 72 retains all one hundred fifty-six revision-71 modules and adds modules 157--159  
**Frozen revision-71 author baseline:** `85152b57d47493e8d0ec2125e8365560aeb75cf0`  
**Frozen revision-71 paper tree:** `1689e32821be45fc3daca28f5da0cf6f8a374e07`  
**Controlling external report:** `reviews/a2-dyn-v71-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `3bf84b862a393456b0a57049d2966f9fbe34da08` / `129f78b849ebf2639130090189bb7b6e9bfebf8d`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 72 is a genuine theorem-bearing response to the revision-71 report. It does not merely rename the residual current from the previous revision. The new manuscript constructs a canonical distributional derivative of the complete original positive physical source, retains every moving-window entrance and exit trace, gives an exact compact primitive for the discrepancy between a density and its fixed-width average, and reallocates a bounded fraction of all three previously uncontrolled positive remainders while preserving the already controlled selected-disk source.

The new controlled source satisfies the ordered estimate

\[
 \mathcal H(s_{72,K})\le C\chi^6+CK\varepsilon^{1/16}.
\]

This is materially stronger than revision 71: the recovery now acts not only on the residual selected-disk angular loss, but also on the complete first-incidence source and the original first-clearance source outside the selected disks. The allocation is implemented by complementary bounded weights on the unchanged exact-label probability space.

The manuscript also proves the exact distributional identity

\[
 b-A_\delta b=\kappa_\delta*Db
\]

for the complete source. This puts all signed physical fluxes at one common roof before a positive part is taken. The resulting full pointwise budget is

\[
 \mathcal E_M\le C_MB^{-1/192}+CB^{-1/4}
       +CK(B)B^{-1/192}
       +\mathcal U_{\varepsilon(B),\delta(B)}(K(B)).
\]

I audited the new modules

- `core/157_global_window_current.tex`;
- `core/158_complete_physical_source_current.tex`;
- `core/159_all_source_recovery_and_height.tex`;

and their direct inputs in modules 106, 155 and 156. I also checked the revised opening, source manifest, response to the referee, proof ledger, specialist audit map, validation protocol, final clarification commit, and the exact-SHA workflow records.

I found no decisive counterexample, sign error in the moving-window atoms, missing section normalization, loss of a genuine jump, illicit pooling of different exact labels, incorrect compact-primitive multiplier, invalid source allocation, erroneous fixed-band exponent, or reversal of the stated collision/band order in the new proofs.

In particular, the following points are internally coherent.

1. The derivative of a truncated moving chart window contains both the entrance atom and the exit atom.
2. Artificial cuts glue with opposite orientations, while a genuine jump is counted exactly once.
3. Every truncated compactly supported current has zero total mass.
4. Passage to the full selected window is made in distributions through `L1` convergence, not by assuming an unproved outer-edge variation bound.
5. The complete current is defined directly from the pushforward of the unchanged original first-defect source.
6. The regular-patch coarea formula has the correct oriented boundary sign.
7. Partition independence follows from differentiating exact positive-source identities before taking any Jordan decomposition.
8. The kernel `kappa_delta` has the required unit jump at zero and satisfies `D kappa_delta = delta_0-rho_delta`.
9. The allocation coefficient is measurable, lies in `[0,1]`, and acts on the same exact-label source through the original roof observable.
10. The previously controlled source is never reduced.
11. The interval-average height estimate uses the inherited local-variation theorem in the legal order: fixed width and auxiliary band, collision limit, then enlargement of the auxiliary band.
12. The reserve cost is `K B^(-1/192)`, not the stronger selected-disk rate `K B^(-1/4)`.
13. The finite-measure local-flux proposition uses the Jordan decomposition of the complete physically weighted current, not a sum of wordwise absolute variations.
14. The manuscript does not claim that the finite-measure hypothesis or the directed-flux power estimate is proved for the unrestricted Lorentz family.

These are real advances. The negative recommendation is therefore not based on a failure of the new distributional identities or recovery algebra.

It is forced by the remaining term

\[
 \mathcal U_{\varepsilon,\delta}(K)
 =\limsup_m\sup_{R,n,k}m^2
   \|[b-KA_\delta b]_+\|_\infty.
\]

No estimate tending to zero is proved for this quantity on the unrestricted Lorentz family. The current is constructed as a compactly supported distribution of order at most one, but it is not proved to be a finite signed measure with collision-uniform directed local variation. The power bound used in the final sufficient implication is explicitly a hypothesis.

Thus revision 72 replaces three separate unestimated heights by one canonical, partition-independent full-source excess. This is a valuable reduction. It is not a proof that the excess vanishes.

Consequently the manuscript still does not establish

- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- complete ordered control of the original incidence and outside-clearance sources;
- unrestricted same-roof collision and actual-return bridges;
- forward essential-likelihood convergence;
- or the unrestricted pointwise roof-conditioned path theorem.

At the requested benchmark, the paper would need either

1. a proof that the complete current excess tends to zero in the legal ordered limit, with all source and numerator consequences closed; or
2. a substantially broader theorem of independent significance, with quantitatively verifiable assumptions and multiple genuinely different singular-hyperbolic realizations, so that the article no longer depends editorially on the unfinished Lorentz endpoint.

Revision 72 supplies neither endpoint yet. No independent human specialist audit has been obtained.

My assessment is therefore positive about the new mathematical reduction and negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`295800b658aa2ff3aada1707d5785ff757d60724`.

The repository tree at that commit is

`a9aefcf74a273523d1e7538fdd1e17e887eaf2d7`.

The active article is

`papers/A2-DYN-v72-referee-response`.

The immediate reviewed author baseline is revision 71 at

`85152b57d47493e8d0ec2125e8365560aeb75cf0`.

The revision-71 report is commit

`3bf84b862a393456b0a57049d2966f9fbe34da08`.

Revision 72 descends from that review commit. Its first theorem-bearing author commit is

`0d0c2ab641786b409fe5de524acb50901fb0b06f`.

The final reviewed commit then adds an explicit definition of the ordered exact-label height, identifies the raw-error limsup, clarifies that `e70` is the original first-clearance source outside the selected disks, and states that all suppressed width and reserve parameters are fixed before the collision limsup.

The final clarification is mathematically useful. It removes ambiguity about whether the new source estimates are finite-count, collision-limsup, or band-dependent statements.

The source manifest records

- all one hundred fifty-six inherited core modules byte-identical;
- all two hundred nine inherited Python sources byte-identical;
- all eleven inherited appendices byte-identical;
- `references.tex` byte-identical;
- every inherited compiled mathematical input and label retained;
- the old revision-71 opening reproduced verbatim in a compiled appendix;
- one hundred fifty-nine active core modules;
- `lorentz_window_current_with_entry_exit_proved: true`;
- `lorentz_complete_source_distributional_current_proved: true`;
- `lorentz_regular_patch_coarea_flux_proved: true`;
- `lorentz_complete_current_primitive_identity_proved: true`;
- `lorentz_all_source_capacity_recovery_proved: true`;
- `lorentz_all_source_recovered_height_proved: true`;
- `lorentz_full_source_finite_measure_current_proved: false`;
- `lorentz_complete_current_excess_decay_proved: false`;
- `lorentz_directed_flux_power_bound_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`; and
- `independent_human_review: false`.

These flags accurately distinguish the scoped new theorems from the unproved final endpoint.

The present review branch starts directly from the reviewed final author SHA and adds only this report under

`reviews/a2-dyn-v72-external-top4-review-2026-10-11/`.

No author manuscript, workflow, prior review, historical source or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The final exact-SHA revision-72 qualification workflows completed successfully on both reviewed refs:

- response branch run `38073663320`;
- referee-copy branch run `38073670419`.

Both final runs use the reviewed SHA

`295800b658aa2ff3aada1707d5785ff757d60724`.

Earlier successful runs on the pre-clarification commit are not substituted for these final runs.

According to the validation protocol and workflow, the verifier checks

- the frozen revision-71 paper tree;
- the controlling revision-71 report blob;
- every inherited core, Python source, appendix, reference and compiled label byte;
- all one hundred fifty-nine active core inputs;
- inherited proof-status booleans;
- normal and optimized finite diagnostics;
- native TeX compilation without shell escape;
- stabilized references and warning-free typesetting;
- rendered pages located through actual theorem labels; and
- the exact checkout SHA and branch ref.

The new finite diagnostics cover

- moving-window entrance and exit atoms;
- artificial-cut gluing;
- common-roof physical weights;
- the compact primitive and Fourier signs;
- zero, partial and exhausted capacities;
- preservation of the old controlled source;
- allocation across the three original residual types;
- the fixed-band exponents; and
- negative controls for missing exit atoms, label mixing, and invalid mass-to-height limit exchange.

These checks are meaningful source, algebra and typesetting evidence. They do not prove

- the continuum common-version bookkeeping for every coarea density;
- finite variation of the complete current;
- a collision-uniform directed-flux bound;
- the inherited full-source local-variation theorem;
- the inherited anisotropic and arithmetic chains;
- the complete current-excess decay;
- or independent human verification.

The validation documents state this boundary correctly.

## 4. Scope of this audit

I did not attempt to re-prove all one hundred fifty-nine modules. The substantive audit concentrates on the new proof route and its immediate inputs:

1. the selected-chart profile and active window;
2. the truncated capacities `X_H`, `Y_H`, `C_H`;
3. the entrance and exit traces;
4. gluing at artificial cuts and genuine jumps;
5. the full-window distributional limit;
6. the Fourier representation;
7. the complete original physical source `b`;
8. partition independence of `Db`;
9. the regular-patch coarea flux;
10. distributional exhaustion near critical and singular sets;
11. the compact primitive `kappa_delta`;
12. the all-source allocation coefficient;
13. realization by complementary source weights;
14. the interval-average height estimate;
15. the ordered controlled-height theorem;
16. the definition of the complete current excess;
17. the fixed-band raw-error budget;
18. the finite-measure local-flux implication;
19. the unchanged conditional consequences;
20. source preservation and final exact-SHA evidence; and
21. the requested top-four significance standard.

The inherited operator, arithmetic, critical-geometry, source-partition, coarea and local-limit chains are treated as source-pinned inputs, not as independently recertified mathematics. Their earlier specialist qualifications remain in force.

## 5. The moving-window derivative

For a fixed collision count, radius, exact label and selected chart family, the manuscript truncates the active radial window at `H<h` and defines

\[
 X_H(t)=\sum_zJ_z\mathbf 1_{(0,H)}(t-t_z)L_z(t-t_z),
\]

\[
 Y_H(t)=\sum_zJ_z\overline L_z\mathbf 1_{(0,H)}(t-t_z),
 \qquad C_H=X_H-Y_H.
\]

The derivative formulas are

\[
 DX_H=\sum_zJ_z\{
  \tau_{t_z}(DL_z|_{(0,H)})
       +L_z(0+)\delta_{t_z}-L_z(H-)\delta_{t_z+H}\},
\]

\[
 DY_H=\sum_zJ_z\overline L_z
       (\delta_{t_z}-\delta_{t_z+H}),
\]

and their difference.

The signs are correct. The entrance trace appears with a positive sign and the exit trace with a negative sign. The formula follows directly from BV integration by parts.

The statement that every truncated current has zero total mass is also correct. The interior derivative has mass `L_z(H-)-L_z(0+)`, which is cancelled by the two trace atoms.

This zero-mass check is more than cosmetic. Omitting the exit atom would produce a nonzero total derivative for a compactly supported profile, which is impossible.

The manuscript uses only local BV on `(0,H')` for `H'<h`. It does not assume a trace or finite total variation at the full outer edge. Since the profiles are bounded between zero and one and the selected family is finite at each count,

\[
 \|X-X_H\|_1+\|Y-Y_H\|_1\to0.
\]

Distributional differentiation is continuous under this `L1` convergence. Therefore the full current is well-defined as a distribution of order at most one.

This is the correct topology for the argument actually proved. It would be incorrect to infer convergence in measure variation or a uniform BV bound, and the manuscript does not do so.

## 6. Gluing and Fourier signs

If a profile is split at an artificial cut, the exit trace from the left piece and entrance trace from the right piece combine to the actual jump. At continuity the contribution vanishes. At a genuine jump it survives exactly once.

This is the appropriate gluing rule.

With the convention

\[
 \widehat f(\xi)=\int e^{-i\xi t}f(t)\,dt,
\]

the identity

\[
 \widehat{DX_H}(\xi)=i\xi\widehat X_H(\xi)
\]

has the correct sign.

The zero-frequency qualification is also correct: one uses the Fourier transform of the density at zero rather than dividing by `i xi` there.

The estimate

\[
 |\widehat{DX}(\xi)|\le |\xi|\|X\|_1
\]

is a fixed-count distributional bound. It is not high-frequency decay and does not provide a transfer-operator resolvent estimate. The manuscript keeps this distinction explicit.

## 7. The complete source current

Let

\[
 \mu^\varepsilon=(L_{m,R})_\#
 ((1-H_{m,R}^\varepsilon)\mathbf 1_{\Pi_{n,k,m,R}}\nu_R^*)
\]

and let `b` be its density.

The canonical definition

\[
 \langle Db,\phi\rangle
 =-\int_{\Pi_{n,k,m,R}}(1-H_{m,R}^\varepsilon)
                    \phi'(L_{m,R})\,d\nu_R^*
\]

is mathematically sound. It is simply the distributional derivative of the pushforward density and does not depend on a chart partition.

The section normalization is included once in `nu_R^*`. No additional factor is inserted in the new current.

Differentiating the exact positive-source decompositions gives

\[
 Db=Db^{\rm inc}+Db^{\rm clr}
\]

and

\[
 Db=Ds_{71,1}+Dd_{71,1}+Db^{\rm inc}+De_{70}.
\]

These identities are valid in distributions even when the individual currents are not finite measures.

Artificial interfaces cannot create a current in the sum. Physical itinerary boundaries, true source jumps and exact-label boundaries are not removed; they are retained in the global distribution.

This is the right source-level object for studying cancellations across the physical partition.

## 8. The regular-patch coarea flux

On a regular patch with roof `F`, source density `w` and

\[
 V=\frac{\nabla F}{|\nabla F|^2},
\]

the proposed formula is

\[
 Db_\Omega=F_\#\bigl(\operatorname{div}(wV)dx
              -(wV\cdot n)d\mathcal H^1|_{\partial\Omega}\bigr).
\]

The sign is correct. Applying the divergence theorem to `phi(F)wV` gives the positive boundary term for the integral of `phi'(F)w`; multiplying by minus one produces exactly the displayed current.

Common artificial interfaces cancel because their outward normals are opposite and the physical roof and density agree. A genuine density jump produces a jump flux and must remain.

The exhaustion argument proves only distributional convergence. Approximation of the positive source in `L1` gives convergence of its roof densities in `L1`, and therefore convergence of derivatives against smooth tests.

This does not yield a uniform bound on the total variation of the patch currents. Boundary flux may concentrate near a critical point even when the source mass of the removed neighborhood tends to zero.

The manuscript states this limitation accurately.

A specialist should nevertheless verify in detail that the inherited physical source, guard, exact-label event and regular coordinate patches admit the common exhaustion claimed here. This is a continuum geometric point not certified by finite fixtures.

## 9. The compact primitive

The kernel

\[
 \kappa_\delta(t)=
 \begin{cases}
 -(\delta+t)/(2\delta),&-\delta<t<0,\\
 (\delta-t)/(2\delta),&0<t<\delta,\\
 0,&|t|\ge\delta
 \end{cases}
\]

has slope `-1/(2 delta)` on both sides and a unit upward jump at zero. Hence

\[
 D\kappa_\delta=\delta_0-\rho_\delta dt,
 \qquad
 \rho_\delta=(2\delta)^{-1}\mathbf 1_{(-\delta,\delta)}.
\]

Convolution with the complete current gives

\[
 \kappa_\delta*Db=b-A_\delta b.
\]

This identity is correct in distributions. Since the right side is an `L1` function, it also fixes an almost-everywhere representative before the later positive part is taken.

The Fourier multiplier

\[
 \widehat\kappa_\delta(\xi)
 =\frac{1-\sin(\delta\xi)/(\delta\xi)}{i\xi}
\]

has the correct sign for the stated transform convention.

The bounds

\[
 |\widehat\kappa_\delta(\xi)|
 \le\min\{\delta^2|\xi|/6,2/|\xi|\}
\]

are valid.

The `1/|xi|` decay is not integrable in one dimension and supplies no high-frequency operator majorant by itself. The paper correctly declines to infer such a result.

## 10. The all-source allocation

Write

\[
 b=s+r,
 \qquad
 r=d_{71,1}+b^{\rm inc}+e_{70}.
\]

Let `q=A_delta b`. The allocation coefficient is

\[
 \alpha(t)=\min\{1,(Kq(t)-s(t))_+/r(t)\}
\]

where `r>0`, with an immaterial convention when `r=0`.

The resulting densities satisfy

\[
 s_{72,K}=\min\{b,\max(s,Kq)\},
\]

\[
 r_{72,K}=[b-\max(s,Kq)]_+.
\]

The algebra is correct in each of the three cases `Kq<=s`, `s<Kq<b`, and `Kq>=b`.

The estimate

\[
 r_{72,K}\le[b-Kq]_+
\]

is also correct.

The allocation preserves the old controlled source and is monotone in `K`.

It is realized by replacing complementary physical weights `W_s,W_r` with

\[
 W_s+\alpha(L_{m,R})W_r,
 \qquad
 (1-\alpha(L_{m,R}))W_r.
\]

These are bounded measurable insertions on the same original source. There is no trajectory transport and no exchange of labels.

This source-level realization is important. The allocation is not merely an identity between arbitrarily chosen density representatives.

A specialist should check that the manuscript fixes one common coarea/disintegration version for `s`, `r`, `q` and the three residual components before forming the ratio. The text adopts this convention, but it is not a finite-dimensional algebra issue.

## 11. Height of the interval average

For fixed `delta`, the average

\[
 q(t)=\frac1{2\delta}\int_{t-\delta}^{t+\delta}b(v)\,dv
\]

is controlled by the inherited complete physical local-variation theorem.

Using interval length `2 delta`, the finite-count estimate becomes

\[
 \sup_{R,n,k}m^2\|q\|_\infty
 \le C\varepsilon^{1/16}
      \left(1+\frac1{2\delta B_*}\right)
 +C_{B_*}\frac{1+2\delta B_*}{2\delta}
                m^3\rho_{B_*}^{m/2}.
\]

The order of limits is legitimate:

1. fix `epsilon`, `delta` and `B_*`;
2. let the collision count tend to infinity;
3. enlarge `B_*` with `delta` still fixed.

This gives

\[
 \mathcal H(q)\le C\varepsilon^{1/16}.
\]

The bound is for the average and not for the original density. The argument does not confuse these two objects.

Combining

\[
 s_{72,K}\le s+Kq
\]

with the revision-71 estimate

\[
 \mathcal H(s)\le C\chi^6
\]

yields

\[
 \mathcal H(s_{72,K})\le C\chi^6+CK\varepsilon^{1/16}.
\]

No number of words, witnesses or charts appears.

## 12. The full-source current excess

The manuscript defines

\[
 \mathcal U_{\varepsilon,\delta}(K)
 =\limsup_m\sup_{R,n,k}m^2
 \|[\kappa_\delta*Db-(K-1)A_\delta b]_+\|_\infty.
\]

By the compact primitive, its integrand is

\[
 [b-KA_\delta b]_+.
\]

This is a natural, partition-independent residual.

All signed physical currents are combined at the same roof before the positive part is taken. This avoids the severe loss that would result from summing wordwise or chartwise total variations.

The quantity is well-defined as an extended nonnegative number even when `Db` is only a distribution, because the compact primitive produces an actual `L1` function.

However, well-definedness is not smallness. The manuscript explicitly preserves that distinction.

## 13. The fixed-band budget

The choices are

\[
 \varepsilon(B)=A_0B^{-1/12},
 \qquad
 \chi(B)=\sqrt{\varepsilon(B)}.
\]

The exponent calculations are

\[
 \chi(B)^6=A_0^3B^{-1/4},
 \qquad
 \varepsilon(B)^{1/16}=A_0^{1/16}B^{-1/192}.
\]

Thus the complete budget

\[
 \mathcal E_M\le C_MB^{-1/192}+CB^{-1/4}
       +CK(B)B^{-1/192}
       +\mathcal U_{\varepsilon(B),\delta(B)}(K(B))
\]

has the correct powers.

The final clarification correctly states that `B`, `epsilon(B)`, `chi(B)`, `delta(B)` and `K(B)` are fixed before the collision limsup. Only after that limit may `B` tend to infinity.

The auxiliary spectral band `B_*` used to control the fixed-width average is distinct from the reconstruction band `B` and is enlarged after the collision limit with the other parameters fixed.

No collision-count-dependent reconstruction band is substituted into a fixed-band theorem.

The new route is not automatically sharper than the revision-71 three-term budget. Its advantage is structural: the three positive residual types are placed into one complete source and one canonical excess.

## 14. The local-flux sufficient condition

Assume additionally that the complete current `Db` is a finite signed measure. Then `b` has a BV representative.

For the convolution at a continuity point `t`, the kernel is positive on current points below `t` and negative on points above `t`, with absolute value at most one half.

Therefore

\[
 [b-A_\delta b]_+(t)
 \le\frac12\{(Db)^+([t-\delta,t])
              +(Db)^-([t,t+\delta])\}.
\]

This inequality is correct outside the countable jump set and hence controls the essential height.

Subtracting the nonnegative term `(K-1)A_delta b` can only reduce the positive part, so

\[
 \mathcal U_{\varepsilon,\delta}(K)
 \le\mathcal U_{\varepsilon,\delta}(1)
 \le\tfrac12\mathcal V_\varepsilon(\delta).
\]

If one had

\[
 \mathcal V_\varepsilon(\delta)\le A\varepsilon^{-q}\delta^\beta,
\]

then the choice

\[
 \delta(B)=\varepsilon(B)^{(q+a)/\beta}
\]

gives the claimed `B^{-a/12}` contribution.

The implication is sound.

But neither premise is proved for the complete Lorentz source:

- `Db` is not shown to be a finite signed measure with useful uniform control;
- the power bound for directed local variation is not established.

This is the decisive mathematical boundary of revision 72.

## 15. What revision 72 closes

Relative to revision 71, the manuscript closes several genuine gaps.

- The moving selected-chart window is differentiated with both boundary traces.
- Full-window currents are defined in the correct distributional topology.
- Artificial chart cuts and genuine jumps are separated correctly.
- A canonical current is defined on the complete original first-defect source.
- Incidence, selected clearance and outside clearance are all included before signed cancellation.
- Partition independence is proved at the distributional level.
- The exact compact primitive converts the current into a density discrepancy.
- The old controlled source is preserved.
- Portions of all three positive residuals are recovered by bounded physical weights.
- The recovered full-source height is `O(chi^6+K epsilon^(1/16))`.
- The raw pointwise problem is reduced to one complete current excess.
- A precise directed-flux theorem is given which would close the endpoint if its hypotheses were verified.
- The final author commit makes the ordered norm and parameter sequence explicit.

These are mathematically meaningful improvements in the organization and sharpness of the remaining obstruction.

## 16. What revision 72 does not close

The principal endpoint remains open.

The manuscript has not proved

\[
 \lim_{B\to\infty}
 \mathcal U_{\varepsilon(B),\delta(B)}(K(B))=0
\]

for any legal choices with

\[
 K(B)B^{-1/192}\to0.
\]

It has not proved a finite-measure theorem for the complete physical current with collision-uniform local variation.

It has not proved the required directed-flux power estimate.

It has not separately proved complete ordered heights for the remaining incidence and outside subweights. Those subweights are retained inside the complete excess.

It has therefore not proved the unrestricted pointwise density law.

Integrated local variation, small source mass, or a distributional primitive does not imply an essential-height estimate. A density may concentrate on a shrinking roof interval while preserving a nonvanishing normalized height.

The scalar example in the manuscript illustrates exactly this invalid implication. It is not a Lorentz counterexample, but it correctly demonstrates why the missing estimate is substantive.

## 17. Conditional and path-valued consequences

Revision 72 does not infer same-roof conditional conclusions from the source allocation alone.

That restraint is correct.

The inherited same-roof bridge and essential-likelihood statements require

- the scalar pointwise denominator estimate;
- the relevant path-valued numerator estimate;
- a positive arithmetic reference class; and
- common almost-everywhere versions.

The current construction does not supply those conclusions until the complete excess and inherited numerator obligations are closed.

No conditional law is assigned to a zero arithmetic class.

Probability total variation remains distinct from variation mass and from bounded-Lipschitz path dual norm.

## 18. Arithmetic and exact labels

The finite arithmetic transition kernel remains part of the main term.

Zero residue classes are retained.

The new current and allocation never pool different values of

- the collision count;
- the radius;
- the return index;
- the displacement label; or
- the roof value at which the densities are compared.

The interval average is an auxiliary capacity. It does not replace the exact record by a roof-window event.

The occupation convention remains half-open at collisions `0,...,m-1`, and terminal membership is imposed at collision `m`.

The section normalization is used once.

These conventions are preserved correctly.

## 19. Novelty and significance

The new distributional current and all-source recovery are not routine restatements of the classical Lorentz-process local limit theorem.

They act on a highly structured source already developed by the manuscript:

- exact return, displacement and collision labels;
- a complete first-physical-defect partition;
- moving selected radial charts;
- first incidence and next-collision clearance;
- finite arithmetic transition classes;
- and a pointwise raw inversion target.

The exact entry/exit trace formula, partition-independent complete current, and source-preserving capacity allocation are useful additions to this program.

Nevertheless, the methods in the new modules are principally BV/distributional calculus, positive-source allocation, and an application of an inherited local-variation estimate. The difficult dynamical input remains specific to the triangular finite-horizon Lorentz family and the manuscript's very large inherited proof chain.

The broad theorem route remains incomplete. The directed-flux hypothesis is not verified in the Lorentz system, much less in several independent singular-hyperbolic systems.

Thus revision 72 improves the mathematical reduction but does not yet supply the completed endpoint or the breadth expected at the requested four-journal level.

## 20. Architecture and editorial presentation

The new three-module route is substantially clearer than the cumulative historical architecture.

The paper now begins with

1. the complete physical current;
2. the all-source recovery theorem;
3. the exact remaining excess; and
4. the quantitative sufficient flux condition.

The revision-71 opening is preserved in an appendix rather than deleted.

This is good revision practice.

The complete article nevertheless contains one hundred fifty-nine core modules and a very large historical dependency chain. The strongest title-level theorem is still conditional on a new full-source estimate.

For a final journal submission, the author should choose one principal endpoint and present the shortest complete proof route to it. Provenance, validation ledgers and superseded theorem hierarchies should not dominate the mathematical narrative.

This is not a request to delete mathematics from the repository. It is an editorial requirement for a readable journal article.

## 21. Independent specialist verification

No independent human specialist audit has been obtained.

For the new modules, the highest-priority checks are:

1. the BV traces of every physical profile at the moving-window boundaries;
2. the sign and placement of entrance and exit atoms;
3. gluing at true jumps and artificial cuts;
4. use of common coarea versions before pooling or allocating densities;
5. exact inclusion of all incidence and outside states in the global source;
6. cancellation of artificial interfaces in the coarea-flux exhaustion;
7. retention of true exact-label and itinerary-boundary flux;
8. the distributional convolution with the discontinuous primitive kernel;
9. realization of the allocation as complementary weights on the original source;
10. application of the inherited local-variation theorem at fixed averaging width;
11. the order `m -> infinity`, then `B_* -> infinity`, followed separately by the outer `B` limit;
12. the complete budget and all powers of `B`;
13. the directed-flux inequality at jump points and common essential-supremum versions; and
14. the distinction between a distributional current and a finite-measure current.

The inherited specialist obligations also remain, including

- the anisotropic collision-space construction;
- the full occupation spectrum;
- arithmetic resonance transitions;
- physical thin-layer geometry;
- first-defect source completeness;
- exact-label coarea;
- the local raw-variation theorem;
- path-valued inversion; and
- collision-to-return clock transfer.

Exact source hashes, finite algebraic fixtures and successful typesetting do not replace these reviews.

## 22. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 22.1. Prove complete current-excess decay

Establish legal choices `delta(B)` and `K(B)` such that

\[
 K(B)B^{-1/192}\to0
\]

and

\[
 \mathcal U_{\varepsilon(B),\delta(B)}(K(B))\to0.
\]

The estimate must be uniform in the original exact labels and must respect the fixed-band collision-limit order.

### 22.2. Verify a usable full-source flux theorem

If the route through Proposition `prop:v72-flux-height` is retained, prove that the complete current is a finite signed measure and establish a directed local-variation bound with controlled dependence on `epsilon` and `delta`.

Wordwise BV or finite-count variation is not enough. The current must be combined physically before its Jordan decomposition, and the ordered bound must survive the supremum over exact labels.

### 22.3. Close the scalar pointwise theorem

Insert the complete current estimate into the budget and state the resulting unconditional arithmetic pointwise LLT with its finite transition kernel and zero classes.

Do not replace the theorem by an interval law, local `L1` theorem, exceptional-set theorem, or integrated total-variation theorem.

### 22.4. Close the numerator and conditional consequences

After the scalar theorem, verify the corresponding path-valued numerator at the same roofs and derive the unrestricted same-roof collision/return bridge and forward essential-likelihood conclusions.

Keep zero arithmetic classes excluded from normalization.

### 22.5. Audit common versions and interfaces

Provide a specialist-readable lemma which fixes one common disintegration/coarea version for all source components, averages, allocations and essential suprema. Identify every physical and artificial interface and show exactly which boundary currents cancel and which survive.

### 22.6. Obtain independent expert review

The complete current, inherited local variation, physical source partition, anisotropic spectrum and path-valued consequences require external human scrutiny.

### 22.7. Strengthen the breadth case or complete the endpoint

If top-four generality is sought independently of the Lorentz endpoint, formulate a reusable current-recovery theorem with hypotheses that can actually be verified in several genuinely different singular systems.

A conditional implication whose principal flux hypothesis is unverified in the motivating system does not by itself supply that breadth.

### 22.8. Reduce the journal proof burden

Prepare a submission-scale article organized around one completed main theorem. Keep the repository as the full research archive, but separate provenance, validation infrastructure and superseded routes from the journal narrative.

### 22.9. Sharpen the literature comparison

Explain theorem by theorem which exact-label pointwise, arithmetic, current, allocation and same-roof conclusions are not consequences of existing Lorentz-process, endpoint mixing-local-limit or suspension-flow theories after their hypotheses are checked.

## 23. Technical and presentation comments

1. Keep `B` and the auxiliary band `B_*` visibly distinct.
2. State whenever `epsilon`, `chi`, `delta` and `K` are fixed before the collision limsup.
3. Retain the definition of `mathcal H` near every theorem using ordered height.
4. Keep every density norm as an essential supremum.
5. Keep `e70` identified as the original first-clearance source outside the selected disks.
6. Do not absorb first incidence into `e70`.
7. Preserve both moving-window boundary atoms.
8. Do not assign a separate measure limit to the outer trace unless a variation bound is proved.
9. Combine artificial interfaces before taking a Jordan decomposition.
10. Retain true physical jumps and exact-label boundaries.
11. Keep the complete current distinct from the old scalar radial current.
12. Do not describe the Fourier identity as a resolvent estimate.
13. State that the `1/|xi|` multiplier is not an integrable high-frequency bound.
14. Fix common coarea versions before forming ratios of densities.
15. At `r=0`, state that the allocation convention is immaterial.
16. Do not call the allocation a transport plan.
17. Keep the interval average as an auxiliary capacity, not a changed conditioning event.
18. State the exact source weights realizing every density allocation.
19. Keep `K B^{-1/192}` distinct from the revision-71 selected-disk rate.
20. Do not let `K`, `delta` or `B` depend on the collision count inside a fixed-band theorem.
21. Keep the positive part outside the complete signed current combination.
22. Do not infer finite current variation from distributional construction.
23. In the flux proposition, keep the finite-measure premise in the theorem statement.
24. Distinguish the power-bound hypothesis from a proved Lorentz conclusion.
25. Keep source mass, local `L1`, and essential height logically separate.
26. Preserve the finite arithmetic transition kernel and zero classes.
27. Do not assign conditional laws to zero reference mass.
28. Keep probability total variation distinct from variation mass and path bounded-Lipschitz dual.
29. State that final qualification runs use the post-clarification SHA.
30. Keep source/build evidence separate from proof certification.
31. Retain the independent-human-review status as false.
32. Consider moving extensive provenance and validation files outside the main journal reading path.

## 24. Final assessment

Revision 72 is a serious and mathematically coherent response to the revision-71 report.

It constructs the correct moving-window derivative, including entrance and exit traces; defines a canonical distributional current on the complete original physical source; proves oriented coarea and compact-primitive identities; and implements a source-preserving recovery across the residual selected loss, first incidence and outside clearance.

The new controlled-height estimate

\[
 \mathcal H(s_{72,K})\le C\chi^6+CK\varepsilon^{1/16}
\]

is credible on the written inputs. The fixed-band exponent bookkeeping is consistent, and the final clarification correctly specifies the ordered norm and parameter sequence.

The new full-source reduction is conceptually cleaner than the previous three-residual budget. I found no decisive flaw in modules 157--159.

The decisive estimate, however, remains unproved. The complete current excess is defined but not shown to decay. The complete current is not shown to have the finite-measure and local-flux properties used in the final sufficient theorem. The unrestricted pointwise raw-density law and its same-roof consequences therefore remain open.

The manuscript is also extraordinarily large and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist paper on complete-source distributional currents, physical source recovery and the exact current-excess criterion could be valuable if the inherited Lorentz chain withstands expert audit. A future top-four submission should return after the complete excess is controlled in the legal ordered limit and the pointwise and conditional endpoint is actually closed.