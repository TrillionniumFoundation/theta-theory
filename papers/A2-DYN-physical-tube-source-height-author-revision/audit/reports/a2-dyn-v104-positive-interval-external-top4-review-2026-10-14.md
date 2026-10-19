# External top-four referee report on A2-DYN revision 104 (positive angular intervals)

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v104-positive-interval-referee-response-2026-10-14`, `revision/a2-dyn-v104-positive-interval-referee-copy-2026-10-14`  
**Reviewed author commit:** `32e839acc2e190b7c93365aafee96f8e2c32f5e3`  
**Reviewed repository tree:** `241833641783b0802ad8e56da69d10a15ca16258`  
**Active manuscript directory:** `papers/A2-DYN-v104-referee-response`  
**Active mathematical source:** 252 numbered core modules; revision 103 adds modules 247--249 and revision 104 adds modules 250--252  
**Immediate theorem-bearing baseline:** revision 103, commit `7949b93131806711109c8f126d2a56fe37da7b59`  
**Frozen revision-103 paper tree:** `3657fe1eb821ec398484f0487f3a8095dd44deed`  
**Latest submission-state report:** `reviews/a2-dyn-v103-submission-state-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Submission-state report blob:** `952e695da87ea365053f284cff18b819e80a48e4`  
**Latest substantive mathematical report before revisions 103--104:** `reviews/a2-dyn-v102-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Substantive report commit / blob:** `37faf38478a5b561c3aa4a1faf63da378caf8189` / `6c6bbd2fc9fd5e6da575ac6db9827448e091af3d`  
**Exact-SHA qualification:** response run `38493120336`, success; referee-copy run `38493122942`, success  
**Date:** 14 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, o-minimal-geometry, probability, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revisions 103 and 104 contain genuine mathematical progress on the exact positive source left by revision 102. They are not branch aliases or bookkeeping-only packets. Revision 103 changes the comparison coordinates on the same positive paired measure, constructs two endpoint-distance clocks, identifies the regular critical incoming trace, separates exact zero-speed flat pulses, and recovers a positive portion of the preceding three-clock failure source. Revision 104 then introduces a different comparison which does not divide by an endpoint velocity at all. It compares angular intervals by positive segment inclusion and integrated trace mass, proves a finite-count pointwise inequality, and applies it to stationary-critical arms. On those arms it also pays the entire outgoing-trace shortage by the inherited uncut optical variation, so no lower bound on the outgoing trace fraction is required.

I audited the newly landed modules

- `core/247_endpoint_distance_coarea_and_critical_traces.tex`;
- `core/248_gap_clock_pointwise_recovery.tex`;
- `core/249_expanding_endpoint_certificate.tex`;
- `core/250_positive_angular_interval_comparison.tex`;
- `core/251_stationary_critical_arm_recovery.tex`;
- `core/252_positive_deficit_and_original_endpoint.tex`;

as well as the focused article, the response, the proof ledger, the source manifest, the qualification record, and the revision-102 substantive report which posed the positive-source obstruction.

Within the stated scopes I found no decisive sign error, missing segment-length factor, reversed Jacobian, incorrect exponent arithmetic, illegal exchange of the collision limit with the outer bandwidth, hidden differentiation of the Borel selector, or unaccounted word-count factor. The positive angular-interval comparison in module 250 is particularly clean: it uses only a product-a.e. interval inclusion, an integrated source/comparison mass balance, and a bounded physical overlap. The deficit

\[
  (C_j-\kappa D_j)_+
\]

is retained as an actual positive shortage, not assigned zero or absorbed into a signed cancellation. In module 251 the identity

\[
  D_j=P_j-E_j,
  \qquad
  E_j=\int_{J_j}[f_-^\varepsilon-f_+^\varepsilon]_+\,d\theta,
\]

and the estimate \(C_j\le \kappa P_j\) give the correct algebraic bound

\[
  (C_j-\kappa D_j)_+\le \kappa E_j.
\]

Subject to the inherited weighted-variation input and multiplicity-one physical summation, the subsequent payment of \(E_j\) by the original uncut volume is internally coherent.

The new estimates are therefore meaningful. In the strongest uniform arm class they give essential height

\[
  O(B^{-1/192}),
\]

and under the allowed outer balance budget they give

\[
  O(B^{-1/384}).
\]

They also cover positive-measure configurations on which all three preceding clocks can be small.

The negative recommendation is nevertheless forced by the exact endpoint of the new scalar theorem. After the entire certified stationary-critical arm source and its outgoing-trace shortage have been removed, the article obtains

\[
  \mathcal E_M
  \le
  \mathcal H_M(\mathsf U_B^{\rm outside})
  +C_MB^{-1/384},
\]

and proves that the original exact-label pointwise assertion is equivalent to

\[
  \mathcal H_M(\mathsf U_B^{\rm outside})\longrightarrow0.
\]

No theorem establishes this limit. The outside source still includes, among other possibilities,

- flat endpoint pulses on isolated chambers with no admissible comparison interval;
- loss of physical continuation before the comparison levels are reached;
- singular critical extensions not covered by the regular critical trace formula;
- simultaneous or higher-order endpoint stationarity without a schedule-compatible level-width budget;
- families for which the comparison intervals do not have a uniform physical overlap bound;
- nonstationary positive pairs not covered by the stationary-arm geometry; and
- any remaining trace shortage outside the critical incoming normalization.

The source manifest and publication status correctly keep complete physical coverage, full positive-deficit decay, all-three-clock failure decay, flat-pulse decay, the full raw-return local limit theorem, and closure of the primary referee request false.

Thus the manuscript has again reduced the governing positive obstruction to a smaller and better-structured positive obstruction, but it has not proved that the final obstruction vanishes. Since the paper itself proves equivalence between the organizing pointwise theorem and that missing limit, this is not an optional refinement after the main result. It is the unresolved upper pointwise half of the main result.

At the requested benchmark, a technically serious partial deconcentration theorem does not substitute for the exact-label raw pointwise local limit theorem around which the article is organized. A positive recommendation would require either closure of the complete outside source or a separate theorem of independent breadth and significance whose statement does not depend on the unfinished endpoint. Revision 104 supplies neither yet.

## 2. Frozen source and revision chronology

The two reviewed author branches both resolve to

`32e839acc2e190b7c93365aafee96f8e2c32f5e3`.

The repository tree at that commit is

`241833641783b0802ad8e56da69d10a15ca16258`.

The active article is

`papers/A2-DYN-v104-referee-response/main.tex`,

and the complete inherited article is compiled through the accompanying `supplement.tex`.

Revision 104 starts from the actual revision-103 author commit

`7949b93131806711109c8f126d2a56fe37da7b59`.

This chronology matters. The latest report carrying a revision-103 label was a submission-state report: at its freeze, the visible revision-103 branch was only an alias for the revision-102 review commit. The theorem-bearing revision-103 source was landed later. Consequently the mathematical additions in modules 247--249 had not received a substantive external report before revision 104 was built on them. I have therefore reviewed revisions 103 and 104 together rather than treating revision 103 as an independently certified baseline.

Revision 103 adds endpoint-distance coarea, positive recovery and an expanding-endpoint certificate. Revision 104 retains those modules and adds positive angular-interval comparison, paid stationary-critical arm recovery and the exact residual scalar decomposition.

The current review branch starts directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v104-positive-interval-external-top4-review-2026-10-14/`.

No author source, author branch, workflow, prior report, historical source variant or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-v104-positive-interval-qualification.yml`.

Both exact-SHA runs completed successfully:

- response branch run `38493120336`;
- referee-copy branch run `38493122942`.

They check the final author SHA, the frozen revision-103 source tree, the submission-state report blob, inherited blobs and executable modes, the replacement snapshots, ordinary and optimized diagnostics, native article and supplement builds, warning and page-geometry gates, and recorder coverage of all 252 mathematical modules. The revision also repairs nested Git-tree enumeration by using `git ls-tree --full-tree` rather than silently accepting an empty relative listing.

This is meaningful source and build evidence. It establishes that the two author refs identify the same committed packet and that the stated source compiles under the encoded protocol. It does not certify the continuum arguments. In particular it does not prove

1. the physical pairing-sheet decomposition and multiplicity-one summation;
2. the regular critical trace formula at every claimed arm;
3. the definable classification of exact zero-speed sets;
4. the stopped endpoint-distance covariance on all relevant Borel restrictions;
5. the product-a.e. interval inclusion for a complete physical comparison family;
6. the inherited weighted optical variation inequality at one-sided traces;
7. the common target-window payment of all comparison deficits;
8. the actual continuation to the three prescribed outgoing roof levels;
9. a uniform level-width ratio on every remaining physical arm;
10. decay of the outside source; or
11. the full exact-label raw pointwise local limit theorem.

The author packet correctly distinguishes software qualification from independent mathematical verification.

## 4. Scope of this review

The substantive audit concentrates on the following chain:

1. the endpoint-distance coordinate changes on the unchanged positive paired source;
2. the pullback Jacobians and finite-count capped-clock inequality;
3. the regular backward-critical incoming trace;
4. the exact zero-speed/flat-pulse decomposition;
5. the expanding-endpoint certificate and its outer schedule;
6. the positive angular-interval comparison;
7. the stationary-critical width and trace balance;
8. the payment of outgoing-trace shortage by the uncut volume;
9. the positive source decomposition at the original target roof;
10. the final scalar equivalence; and
11. the exact physical families which remain outside the proof.

The 246 earlier modules inherited by revision 103, and the broader historical Gaussian, arithmetic, pressure, coarea and inversion pipeline, are treated as source-pinned inputs. I have not re-proved the complete historical chain. This report therefore does not convert the present AI-assisted review history into formal proof certification.

## 5. The inherited positive obstruction

Revision 102 had reached the positive paired source

\[
 d\pi^\varepsilon
 =c^\varepsilon(\theta)\ell(\theta)\,d\theta\,ds,
 \qquad
 c^\varepsilon(\theta)
 =\min\{f^\varepsilon(a+,\theta),f^\varepsilon(b-,\theta)\},
\]

with roof map

\[
 \mathscr F(\theta,s)=a(	heta)+s\ell(	heta),
 \qquad \ell=b-a.
\]

The pointwise difficulty is the positive minimum itself. Both endpoint traces can be large and close, so a small signed trace difference does not control this minimum. Revision 102 gave a pointwise height estimate only on the source admitted by a relative transverse clock. Its scalar theorem left the positive clock-failure source as the exact upper obstruction.

Revision 103 and revision 104 attack that correct object. Neither replaces it by a signed current, an average on the left, a volume collar, a different event, or a finite norm weaker than the target essential height.

## 6. Revision 103: endpoint-distance coordinates

Module 247 replaces the barycentric relative coordinate by the roof distances

\[
 x_-=u-a(	heta),
 \qquad
 x_+=b(	heta)-u.
\]

Since \(x_-=s\ell\) and \(x_+=(1-s)\ell\), the factor \(\ell\) in the barycentric measure is exactly the coordinate Jacobian, and in either coordinate

\[
 d\pi^\varepsilon=c^\varepsilon(	heta)\,d	heta\,dx_\pm.
\]

This is an exact change of variables on the same positive measure.

At fixed \(x_\pm\), the roof derivative is \(e_\pm'\), so the unit-roof-speed fields have densities

\[
 \rho_\pm^\varepsilon=rac{c^\varepsilon}{|e_\pm'|}.
\]

The pullback Jacobian

\[
 J_h^\pm(y)
 =\frac{\rho_\pm^\varepsilon(\Theta_h^\pm y)}
        {\rho_\pm^\varepsilon(y)}
\]

has the correct orientation for the displayed covariance identity. The absolute speed is retained. I found no missing \(\ell\)-factor or reciprocal error in this coordinate change.

The finite-count pointwise comparison in module 248 disjointizes the source by the first successful endpoint-distance clock. Each admitted part is transported through the exact covariance and bounded by the complete short paired target. The factor two counts the two explicitly chosen comparison directions, not the number of words or chambers. Since the source selector remains at the starting roof and the target comparison is positive, no selector derivative or signed cancellation is needed.

Under the stated schedule the recovered part has height \(O(B^{-1/384})\). The exact positive split

\[
 \mathsf U_B
 =\mathsf V_B+\mathsf U_B^{\rm rem}
\]

is valid at finite count, with \(0\le \mathsf U_B^{\rm rem}\le \mathsf U_B\).

These arguments are coherent within their admitted domain.

## 7. Critical trace and exact zero speed

Module 247 computes the regular nongrazing backward-critical incoming trace as

\[
 f^\varepsilon(a+,\theta)
 =\frac{\omega(q_*)W^\varepsilon(q_*)}
 {4\pi c_*\,e_\perp(\theta)^{\mathsf T}K_*e_\perp(\theta)}.
\]

This formula correctly permits a positive trace. It does not infer that the positive minimum with the outgoing trace has controlled relative variation. That distinction was essential in the previous reports and is preserved.

The exact zero-speed lemma is also appropriately limited. If at least one endpoint derivative is nonzero, the relative speed vanishes at at most one \(s\)-value and is paired-measure null. When both endpoint derivatives vanish on a definable interval, the endpoint roofs are constant there and the source is an explicit positive rectangular pulse. The article does not declare those pulses negligible.

The load-bearing issues for a specialist are the one-sided critical trace convention, the regularity of the physical extension, and the definable classification of the common derivative-zero set. I found no contradiction in the written argument, but these continuum points are not certified by the finite fixtures.

## 8. The expanding-endpoint certificate

Module 249 proves a sufficient certificate under

\[
 |\dot e|\ge\nu,
 \qquad
 0\le\dot\ell\le K|\dot e|,
 \qquad
 |(\log c^\varepsilon)^{\boldsymbol\cdot}|\le A,
 \qquad
 |(\log|\dot e|)^{\boldsymbol\cdot}|\le A,
\]

and the corresponding one-sided reach and scale conditions.

Keeping the distance to the selected endpoint fixed is the correct construction. Because the residence is nondecreasing, every initial relative position remains inside the segment, including approach to either endpoint. The density ratio then gives a clock bounded below without a logarithmic derivative of the residence. The opposite-slope corollary and the two elementary models correctly demonstrate why the endpoint-distance clocks can recover positive source missed by the relative clock.

The theorem remains a certificate. It does not prove that every physical pair has the speed, trace-variation and reach properties. Flat pulses, simultaneous stationarity, short reach and rapid trace variation remain outside. Revision 104 is designed to remove the endpoint-speed requirement on an important stationary-critical family.

## 9. Revision 104: positive angular-interval comparison

Module 250 is the conceptual center of revision 104. It assumes source angular sets \(I_j\), comparison sets \(J_j\), and one-sided interval inclusion. For the positive masses

\[
 C_j=\int_{I_j}c\,d\theta,
 \qquad
 D_j=\int_{J_j}c\,d\theta,
\]

it sets

\[
 \alpha_j=\min\{1,\kappa D_j/C_j\}
\]

when \(C_j>0\).

If the selected source at a roof \(t\) is positive, the product-a.e. inclusion implies that almost every comparison angle contains the appropriate one-sided interval of roofs of length \(r\). Hence

\[
 rD_j
 \le
 \int_{t+\tau_j(0,r)}T_{J_j}(u)\,du,
 \qquad
 \alpha_jT_{H,j}(t)
 \le \alpha_jC_j
 \le\kappa D_j.
\]

Summing and using the physical overlap bound gives

\[
 \sum_j\alpha_jT_{H,j}(t)
 \le
 \frac{N\kappa}{r}
 \int_{t-r}^{t+r}\mathsf T_\Delta^\varepsilon(u)\,du.
\]

The quantifiers are sound: positivity of the selected integral gives a source set of positive angular measure, and Fubini converts the product-a.e. inclusion into the needed statement for almost every comparison angle. The proof does not require a pointwise map from each source trajectory to a comparison trajectory.

The exact positive remainder satisfies

\[
 (1-\alpha_j)C_j=(C_j-\kappa D_j)_+.
\]

This is the correct deficit. The theorem neither differentiates the positive minimum nor divides by any endpoint or relative speed. It therefore genuinely reaches stationary endpoint geometries missed by the preceding clocks.

The theorem is conditional on the interval inclusion, mass balance and physical overlap. Its strength on the Lorentz family depends entirely on verifying those conditions on a sufficiently complete family.

## 10. Stationary-critical arm balance

On a regular critical arm the incoming roof is constant and

\[
 f_-^\varepsilon(x)=\frac{N_*}{Q_*(x)},
 \qquad
 \lambda_\circ\le Q_*(x)\le\Lambda_\circ.
\]

The outgoing roof is written

\[
 b(x)=a_*+d+\psi(x),
 \qquad 0\le d\le\delta/2,
\]

with three actual reached levels. The source and comparison intervals are

\[
 I=(0,x_1),
 \qquad
 J=(x_2,x_3),
\]

where \(\psi(x_1)=\delta/2\), \(\psi(x_2)=2\delta\), and \(\psi(x_3)=3\delta\).

Writing

\[
 w=\min\{1,f_+^\varepsilon/f_-^\varepsilon\},
 \qquad
 \mu_J=|J|^{-1}\int_Jw,
\]

the estimate

\[
 \frac{\int_Ic^\varepsilon}
      {\int_Jc^\varepsilon}
 \le
 \frac{\Lambda_\circ}{\lambda_\circ\mu_J}
 \frac{x_1}{x_3-x_2}
\]

is correct. Under the elasticity bound

\[
 \frac{x\psi'(x)}{\psi(x)}\le K,
\]

integration of \(\psi'/\psi\) gives

\[
 x_3-x_2
 \ge x_1\frac{\log(3/2)}{K},
\]

and hence the displayed mass balance. No lower bound on \(\psi'\) is needed.

The interval inclusion is also correct: source lengths are at most \(\delta\), comparison lengths are below \(4\delta\), and the outgoing endpoint advances by more than \(\delta\). Disjoint physical arms give overlap one on the pairing-sheet space.

This proves a genuine pointwise height theorem for the certified stationary-critical arm source, including every relative position.

The theorem does not prove that every stationary-critical arm reaches the three levels before a true boundary, has a schedule-compatible level-width ratio, or belongs to a family with a uniform finite-order budget. Finite-count definability alone gives no uniform bound on the order, neighborhood or reach. The author states these limitations correctly.

## 11. Paying the outgoing-trace shortage

The strongest new step is Theorem `thm:v104-paid-arms`, which removes the lower bound on the average outgoing trace fraction.

For one comparison interval it defines

\[
 P_j=\int_{J_j}f_-^\varepsilon,
 \qquad
 E_j=\int_{J_j}[f_-^\varepsilon-f_+^\varepsilon]_+,
 \qquad
 D_j=P_j-E_j.
\]

The critical incoming normalization and geometric width ratio imply \(C_j\le\kappa P_j\), so

\[
 (C_j-\kappa D_j)_+
 \le\kappa E_j.
\]

This algebra is valid even if \(D_j=0\).

The inherited weighted variation bound is then used in the form

\[
 [f_-^\varepsilon(x)-f_+^\varepsilon(x)]_+
 \le
 C(1+\varepsilon^{-1})
 \int_{a_j}^{b(x)}
       A(u,x)I_m(u,x)/z(u,x)\,du.
\]

Because the incoming roof is common on the arm, every comparison segment contributing to a source roof \(t\) lies in the common window

\[
 (t-\delta,t+4\delta).
\]

After summing disjoint comparison intervals on the original physical sheet space, the Borel segment identity charges the complete variation to the same uncut source \(v^0\) with multiplicity one. Only after that positive physical sum is formed does the proof apply the fixed-width averaged bound on \(v^0\).

This is the correct order. The argument does not assume a pointwise bound on \(v^0\), and it does not replace the original variation by an averaged trace difference on the left.

The step is nevertheless highly load-bearing. An independent specialist should verify line by line:

1. that the inherited derivative estimate applies to the same one-sided endpoint traces and guard used here;
2. that compact-interior integration passes to both endpoint traces without an unrecorded boundary measure;
3. that the comparison intervals are genuinely disjoint on the incident-component pairing-sheet space;
4. that no physical segment is counted twice when several arms meet a geometrical boundary point;
5. that the common incoming roof is preserved throughout the family being summed;
6. that the window \((t-\delta,t+4\delta)\) contains every paid segment with the stated endpoint conventions; and
7. that the inherited uncut volume estimate is uniform in the same labels and outer parameters.

I found no fatal inconsistency in the written proof, but the finite diagnostics do not establish these continuum and multiplicity assertions.

## 12. The exact residual scalar decomposition

Module 252 applies the comparison to the original selector \(H_B\) which already includes the short-source condition and failure of all three preceding clocks. It writes

\[
 \mathsf U_B^{\rm rem}
 =\mathsf V_B^{\rm int}+\mathsf R_B^{\rm int}
\]

at finite count, with both terms positive. The recovered part consists of the fractions \(\alpha_j\) on the chosen intervals. The remainder contains

- the entire source outside the chosen \(I_j\); and
- the explicit comparison deficits on the chosen \(I_j\).

If \(N_B\kappa_B\le C\varepsilon(B)^{-1/32}\), the recovered height is \(O(B^{-1/384})\); if \(N_B\kappa_B\) is bounded, it improves to \(O(B^{-1/192})\). The exponent arithmetic is correct for

\[
 \varepsilon(B)=A_0B^{-1/12},
 \qquad
 \delta=O(\varepsilon^4).
\]

On the paid stationary-critical arms the entire comparison deficit is bounded by

\[
 C\kappa_B(1+\varepsilon^{-1})\delta
 =O(\varepsilon^{95/32})
\]

under the allowed budget. Therefore the whole source on those arms, not only a trace-balanced fraction, is removed from the scalar obstruction.

What remains is exactly

\[
 \mathsf U_B^{\rm outside}
 =T_{H_B\mathbf 1_{(\cup I_j)^c}}^{\varepsilon(B)}.
\]

The final theorem is

\[
 \mathcal E_M
 \le
 \mathcal H_M(\mathsf U_B^{\rm outside})
 +C_MB^{-1/384},
\]

with equivalence between the original pointwise theorem and the vanishing of this outside height.

This is a precise and honest endpoint. It is also an explicit statement that the principal theorem is not yet proved.

## 13. The unresolved physical classes

The article identifies several mechanisms which can remain in the outside source.

### 13.1. Flat endpoint pulses

If both endpoint roofs are constant on a positive angular interval, the source is a positive rectangular roof pulse. Such a chamber may have no comparison interval satisfying the required one-sided inclusion. Revision 104 does not bound the total height of these pulses.

### 13.2. Insufficient physical reach

The arm theorem requires that the actual physical continuation reaches the outgoing levels \(\delta/2\), \(2\delta\), and \(3\delta\) before a true endpoint, section change, singularity or loss of pairing. Algebraic continuation of the endpoint profile is not enough. No complete reach theorem is given.

### 13.3. Singular critical extensions

The critical incoming trace formula applies to a regular nongrazing stationary extension. Coincident singular extensions remain in the original source. They are not shown null or small in the target height norm.

### 13.4. Unbounded order or width ratio

A finite-order asymptotic \(\psi(x)\sim\beta x^k\) gives a local elasticity bound, but the article does not prove a uniform order \(k\), a uniform asymptotic neighborhood or a schedule-compatible outer budget for every physical arm.

### 13.5. General nonstationary pairs

The positive angular-interval theorem is abstract enough to handle other families, but no theorem constructs comparison pairs with controlled overlap and mass balance for the complete nonstationary remainder.

### 13.6. General trace deficits

The uncut-volume payment uses the stationary critical incoming normalization. Comparison families without that common normalization can still leave a positive deficit in \(\mathsf R_B^{\rm int}\).

Any one of these classes could, in principle, carry the remaining upper spike. The manuscript gives no global classification theorem proving otherwise.

## 14. Why the missing limit is decisive

The full exact-label raw pointwise theorem is not merely one downstream corollary among many. It is the organizing statement of the article. The manuscript retains the original event, labels, guard, arithmetic zero classes and scalar-first order of proof. It also proves necessity: if the scalar pointwise conclusion holds, then the remaining positive source height must vanish.

Therefore the final outside-source estimate cannot be postponed as a technical improvement while the main theorem is declared complete. The article's own logic identifies it as the last upper obstruction.

Until that obstruction is closed, the paper cannot promote unrestricted point-conditioned kernels, denominators, same-roof ratios, likelihood laws or other downstream conclusions which require the full pointwise theorem. The author packet correctly refrains from doing so.

## 15. Significance and architecture at the requested benchmark

The positive comparison machinery is technically interesting. In particular:

- it isolates the exact positive obstruction rather than a signed proxy;
- it supplies three distinct comparison mechanisms;
- it works at finite collision count before the target norm;
- it preserves arbitrary Borel selectors at the starting roof;
- it avoids a word-count loss by summing on disjoint physical sheets;
- it handles stationary endpoint speeds through integrated interval comparison; and
- it connects trace shortage to an original uncut optical source rather than an unavailable pointwise density bound.

These are nontrivial contributions.

The current focused article is much shorter than the historical supplement, but its principal theorem remains a partial source-recovery theorem inside a very long proof pipeline. At a strong specialist-journal level, a self-contained paper on positive paired-trace deconcentration might be viable if its hypotheses, physical applications and remaining classes were separated sharply. At the requested four-journal level, however, the submission still lacks the theorem which motivates the entire construction.

The number of successful reductions does not itself establish top-four significance. The decisive question is whether the exact-label raw pointwise law is proved, or whether the comparison method is elevated to a broadly reusable theorem with several independent applications. Revision 104 does neither.

## 16. Required changes before another top-four review

A genuinely decisive revision should address the following items.

1. **Classify the complete outside source.** Give a theorem decomposing every remaining physical pairing sheet into finitely or countably many comparison classes with schedule-compatible overlap and mass balance, plus a residual class whose target height is proved small.

2. **Control flat endpoint pulses.** Prove their total essential height vanishes, compare them by a new positive mechanism, or establish a physical theorem excluding them except on a target-null set. Merely displaying the pulse is not enough.

3. **Prove physical reach.** Establish that every relevant stationary-critical arm reaches the required comparison levels before a true boundary, or quantify and control the source lost by failure of reach.

4. **Handle singular critical extensions.** Either extend the trace/interval argument to them or prove their complete positive source has negligible height in the original norm.

5. **Uniformize the level-width budget.** Show that the physical orders, elasticity constants and comparison widths satisfy the \(B\)-dependent budget on the complete family. Fixed-count definability does not supply this uniformity.

6. **Extend the paid-deficit mechanism.** For comparison families without the stationary incoming normalization, prove an analogous payment or a direct positive mass balance.

7. **Prove the final limit.** Establish

   \[
   \mathcal H_M(\mathsf U_B^{\rm outside})\to0
   \]

   for every fixed \(M\), and then derive the exact-label pointwise theorem without changing the event, topology or order of limits.

8. **Obtain an independent specialist audit.** The physical sheet construction, critical trace, one-sided endpoint passage, uncut variation payment, multiplicity-one summation and inherited pressure/coarea inputs require expert verification independent of the author-side finite diagnostics.

9. **Keep downstream promotion conditional until scalar closure.** Denominators and unrestricted conditioned laws must follow only after the complete pointwise theorem is established.

## 17. Technical and presentation comments

1. The introduction should state explicitly that the latest submission-state report did not review the subsequently landed revision-103 mathematics. The present source history is correct in Git, but a reader could otherwise mistake the v103 packet for an independently reviewed baseline.

2. The focused `main.tex` repeats the definitions of \(q,F,g,z,I_m\) verbatim in the inherited-source section. One copy should be removed.

3. The proof of Theorem `thm:v104-block` should spell out the Fubini quantifier in one sentence: from a positive selected source set and a product-null exceptional set, almost every comparison angle satisfies the inclusion for almost every selected source angle. The current proof is correct but terse at this point.

4. The statement of the stationary-arm theorem should distinguish clearly between disjoint source intervals and disjoint entire physical arms. The overlap-one conclusion uses disjointness of the comparison intervals on the incident-component sheet space, not merely disjointness of the source \(I_j\).

5. The paid-deficit theorem should cite the exact inherited theorem and endpoint convention supplying the weighted derivative bound, rather than only the focused input label. This is the most load-bearing imported estimate in revision 104.

6. A table should list, for every physical failure class, whether it is controlled by the relative clock, an endpoint-distance clock, the positive interval comparison, the uncut-volume deficit payment, or no current theorem. This would make the final outside source auditable.

7. The manuscript should keep the two rates separate throughout: \(O(B^{-1/192})\) requires a bounded balance cost, while \(O(B^{-1/384})\) permits the specified growing budget. Neither rate applies to the uncovered source.

8. Model interval calculations should remain labeled as model checks. They verify the comparison mechanism but do not establish realized Lorentz geometry or complete physical coverage.

9. The remote exact-SHA successes should be recorded in the final static source metadata. The manifest was written before publication and correctly says that remote publication was not yet observed; a later source revision may update the evidentiary record without changing the mathematical claims.

## 18. Final assessment

Revisions 103 and 104 are substantive advances. They act on the correct positive paired source, introduce comparison mechanisms genuinely different from the original relative clock, cover certified critical-corner and opposite-slope geometries, eliminate the endpoint-speed requirement on stationary-critical arms, and pay the complete outgoing-trace shortage on those arms by the original uncut optical variation. I found no decisive mathematical error in the new six-module chain.

The source and build record is also strong: both author refs identify one commit and both exact-SHA workflows succeeded.

Nevertheless, the exact result proved is still a partial recovery theorem. The complete outside source is retained, its essential height is not shown to vanish, and the article proves that the original pointwise theorem is equivalent to precisely that missing limit. The full exact-label raw return local limit theorem and its unrestricted downstream consequences therefore remain unproved.

At the requested *Annals* / *Acta* / *Inventiones* / *JAMS* benchmark, the manuscript is not ready.

**Final recommendation: reject in the present form.**
