# External top-four referee report on A2-DYN revision 100 (uniform capacity)

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v100-uniform-capacity-referee-response-2026-10-13`, `revision/a2-dyn-v100-uniform-capacity-referee-copy-2026-10-13`  
**Reviewed author commit:** `7b2d9c999e987f61a38e9fcadd7fd7605192f35a`  
**Reviewed repository tree:** `6f3136dc8dddbc9c16b2a14d6114b94dd4ede958`  
**Active manuscript directory:** `papers/A2-DYN-v100-uniform-capacity-referee-response`  
**Canonical revision identity:** `a2-dyn-v100-uniform-capacity-finite-tests-2026-10-13`  
**Active mathematical source:** 243 numbered core modules; revision 100 adds modules 241--243 and inherits the unreviewed v99 modules 238--240  
**Immediate author baseline:** revision 99 at `09685ba342a68d8551c87587540ff5a17c09726e`  
**Frozen revision-99 paper tree:** `864bea62f1a63c5ec07e765cf4f720aaba0ebbe4`  
**Controlling external report:** `reviews/a2-dyn-v98-external-top4-review-2026-10-13/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `357e47da83265ac52bbc65b524aecccc6100508b` / `041bdf3eb46f24c09dbc1a469a5e728713c4d900`  
**Exact-SHA qualification runs at review freeze:** response `38357156664` queued; referee-copy `38357171483` in progress; neither had a conclusion at the freeze  
**Date:** 13 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, thermodynamic-formalism, geometric-measure-theory, probability, o-minimal-geometry, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 100 is a substantial theorem-bearing response to the revision-98 report. It also incorporates revision 99, which was an intervening author revision rather than an intervening external review. The cumulative new chain in modules 238--243 does materially more than rename the two obstructions identified in revision 98.

The manuscript now supplies an explicit bridge from the original endpoint-momentum fibers to geometric stable-Jacobian pressure sums. It then gives a new family-uniform geometric argument which bounds those pressure sums by finitely many transverse stable tests and the standard curve-growth estimate. Subject to the inherited interfaces and to the delicate geometric assertions discussed below, this closes the family-uniform spectral-capacity obstruction left open in revision 98.

More specifically, the cumulative v99--v100 contribution proves, at its stated scope:

1. global uniqueness of a regular physical orbit for a fixed lifted itinerary and fixed endpoint-momentum pair;
2. a nonaccumulating comparison between the optical density and a genuine stable Jacobian;
3. removal of the stable factor at a marked inverse-incidence insertion;
4. a bound for the actual weighted endpoint-momentum fiber by physical itinerary pressure sums, not by an unweighted word count;
5. radius-uniform boundedness of the homogeneous geometric pressure sum by a finite stable-testing construction;
6. a uniform bound on the actual weighted momentum capacity \(\mathcal K_m\);
7. verification, for every fixed admissible auxiliary band, of
   \[
   m^6\mathcal K_m\theta_{B_*}^{2m}\longrightarrow0;
   \]
8. uncut concentration for the actual source \(I_m z^{-p}\) for every \(1\le p<129/128\), with the full positive two-cap error retained at finite collision count;
9. radius-uniform essential-height recovery of the long critical residual;
10. radius-uniform control of the complete short-segment trace-comparison error and of all grazing-ended selected short sources; and
11. a family-uniform scalar reduction with no remaining spectral-capacity hypothesis.

I found no decisive internal sign error, Jacobian reversal, exponent error, illegal collision-dependent cutoff, hidden homogeneous-strip count, or illicit interchange of a fixed-radius limit with a radius supremum in the written modules 238--243. The endpoint-momentum uniqueness argument is coherent. The marked pressure comparison uses the correct physical multiplicities. The two-cap layer-cake exponents are consistent. The stated order of limits is legal. The new pressure proof is highly load-bearing and requires independent specialist reconstruction, but I do not identify an immediate contradiction in it.

The recommendation nevertheless remains negative because the central pointwise theorem is still not proved. After the capacity obstruction has been removed, the scalar endpoint is

\[
\mathcal E_M
\le
\mathcal H_M\!\left(T_{\mathsf S}^{\varepsilon(B)}\right)
+C_MB^{-1/192}
+C(qr)^{257/256}
+C(1+\varepsilon(B)^{-1})qr,
\]

with

\[
q=\frac18,
\qquad
r=c\varepsilon(B)^4,
\qquad
a=\sqrt{qr},
\qquad
\delta=6qr.
\]

The explicit terms tend to zero. The remaining quantity

\[
\mathcal H_M\!\left(T_{\mathsf S}^{\varepsilon(B)}\right)
\]

is not proved to tend to zero, even at one fixed radius. Here \(T_{\mathsf S}\) is the positive minimum of the two original weighted endpoint traces on each selected short physical segment. It is not the Jordan positive part of a projected signed current. On a nongrazing short segment both traces may be positive, and their minimum may concentrate at exceptional roofs while the associated volume source has small mass.

Thus revision 100 closes one of the two independent revision-98 obstructions and leaves the other one explicit. It still does not prove:

- decay of the positive nongrazing paired short-trace height;
- vanishing of the complete residual upper source;
- unconditional upper-spike persistence;
- the upper pointwise half of the exact-label raw local limit theorem;
- the unrestricted pointwise exact-label raw local limit theorem; or
- the unrestricted point-conditioned kernel, likelihood, entropy, and path-space conclusions which require that scalar theorem.

At the requested benchmark, an exact reduction to one positive boundary source is important but is not a substitute for proving that source negligible in the original pointwise topology.

## 2. Frozen source, chronology, and source identity

The branch search shows a plain branch

`revision/a2-dyn-v100-referee-response-2026-10-13`

at an earlier placeholder-style commit. It is not the latest theorem-bearing revision. The later paired branches

- `revision/a2-dyn-v100-uniform-capacity-referee-response-2026-10-13`;
- `revision/a2-dyn-v100-uniform-capacity-referee-copy-2026-10-13`

both resolve to

`7b2d9c999e987f61a38e9fcadd7fd7605192f35a`.

The repository tree is

`6f3136dc8dddbc9c16b2a14d6114b94dd4ede958`.

The active article packet is

`papers/A2-DYN-v100-uniform-capacity-referee-response`.

The source manifest pins revision 99 as the immediate author baseline at

`09685ba342a68d8551c87587540ff5a17c09726e`,

with paper tree

`864bea62f1a63c5ec07e765cf4f720aaba0ebbe4`.

Revision 99 itself descends from the exact revision-98 external-review commit

`357e47da83265ac52bbc65b524aecccc6100508b`.

There was no separate external report between revision 99 and revision 100. Accordingly this audit treats the following six modules as the cumulative new mathematical chain since the controlling report:

- `core/238_global_momentum_uniqueness_and_stable_weight.tex`;
- `core/239_marked_pressure_comparison_and_growth.tex`;
- `core/240_fixed_radius_recovery_and_uniform_scope.tex`;
- `core/241_uniform_geometric_pressure_by_finite_tests.tex`;
- `core/242_uniform_capacity_and_uncut_gradient_moments.tex`;
- `core/243_uniform_source_recovery_and_positive_trace.tex`.

The packet declares that all 240 inherited cores, 305 inherited Python sources, 28 appendices, bibliography files, provenance files, and executable modes are preserved. It also retains the complete revision-99 article and the two distinct revision-88 variants.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v100-uniform-capacity-external-top4-review-2026-10-13/`.

No author manuscript source, author revision branch, workflow, prior review, preserved source variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source workflow is

`.github/workflows/a2-dyn-v100-uniform-capacity-qualification.yml`.

At review freeze, the two exact-SHA runs were:

- response branch: `38357156664`, status `queued`, conclusion `null`;
- referee-copy branch: `38357171483`, status `in_progress`, conclusion `null`.

I therefore do not describe revision 100 as having completed fresh remote qualification at the freeze.

The validation contract is meaningful. It is designed to verify:

- the revision-99 paper-tree pin;
- the controlling revision-98 report blob;
- both preserved revision-88 variants;
- byte and mode preservation of inherited sources;
- all revision-99 top-level snapshots;
- exactly the two declared capacity/margin status supersessions;
- agreement of ordinary and optimized finite fixtures;
- native compilation of the focused article and complete archive;
- actual recorder coverage of all 243 core modules;
- stabilized references and warning gates; and
- page geometry and rendered-output checks.

The author reports a successful complete local validation of a 21-page article, an 833-page archive, all 243 recorded cores, and 3,624 new finite fixtures in ordinary and optimized modes. I treat that as local source/build evidence, not as completed remote qualification.

Neither successful source qualification nor finite fixtures would certify:

- the global physical-orbit uniqueness theorem;
- the stable optical comparison;
- the uniform long-cell reduction;
- the finite stable-testing construction;
- injectivity into inverse-curve components;
- the bounded final physical split;
- the uniform pressure theorem;
- the continuum coarea and trace identities; or
- the missing positive paired-trace height theorem.

The manuscript states this boundary correctly.

## 4. Scope and limitations of this audit

The complete source contains 243 core modules and a very large inherited archive. I have not independently reconstructed every historical theorem from first principles.

The substantive audit concentrates on:

1. the two open requests in the revision-98 external report;
2. the cumulative v99 momentum-fiber bridge in modules 238--240;
3. the global uniqueness argument for fixed itinerary and endpoint momenta;
4. the optical/stable-Jacobian normalization;
5. removal of one marked incidence from the stable cocycle;
6. the actual momentum-fiber pressure comparison;
7. the common geometric constants used in module 241;
8. the uniform long-cell reduction;
9. the finite family of transverse stable tests;
10. stable-convexity and the injective assignment of backward cells to inverse pieces;
11. the uniformly bounded final physical split;
12. the radius-uniform pressure estimate;
13. the uniform momentum-capacity theorem;
14. the two-cap layer cake for \(I_mz^{-p}\);
15. the critical-target and paired-trace recovery theorems;
16. the final scalar reduction and its scale arithmetic;
17. the distinction between the trace-comparison error and the positive paired trace itself;
18. source identity, claim status, and limit order; and
19. completeness and significance at the requested four-journal benchmark.

I read directly the cited Baladi--Demers thermodynamic-formalism paper and the Demers--Zhang uniform-family paper. Their results support, respectively, whole-cell distortion and long-cell pressure mechanisms, and uniform family/curve-growth estimates. The finite stable-testing construction and its application to the present radius family are new arguments of this manuscript rather than quoted theorems from those references.

The inherited four-record spectral theorem, critical-volume estimate, positive scalar remainder, Borel maximal-segment map, common coarea kernels, and revision-97 capped-clock/running-compression reduction are treated as source-pinned inputs. Their interfaces with modules 238--243 are checked here. This report is not a substitute for an independent specialist reconstruction of those inputs.

## 5. Response to the revision-98 report

Revision 98 left two independent obligations:

```text
(A) prove the family-uniform weighted momentum capacity / SC;
(B) prove decay of the positive nongrazing paired short-trace height.
```

Revision 100 responds as follows.

### 5.1. Actual weighted momentum capacity

**Substantially addressed at manuscript level.**

Revision 99 first replaces the unquantified physical-fiber multiplicity by an explicit dynamical comparison. Revision 100 then proves a family-uniform bound for the geometric pressure sum used on the right side of that comparison. The resulting theorem gives

\[
\sup_{R,m}\mathcal K_m(R)<\infty
\]

and therefore verifies SC at every fixed auxiliary band.

This is the right object. It is not a bound for an unweighted number of symbolic words, and it does not import a pressure theorem for a different weight without comparison.

The conclusion remains subject to the correctness of the new uniform pressure proof, whose most delicate geometric steps require independent checking. Within the written chain I found no decisive contradiction.

### 5.2. Positive paired short-trace height

**Not addressed to closure.**

Revision 100 proves a radius-uniform estimate for

\[
R_H^\varepsilon-T_H^\varepsilon
\]

for every fixed Borel selector on short segments. It also controls the complete source whenever one physical endpoint is grazing, because in that case the corresponding weighted trace is zero.

It does not prove that

\[
T_{\mathsf S}^\varepsilon
\]

is small on nongrazing short segments. A small comparison error cannot control a positive common part of two traces.

This is the decisive remaining obstruction.

### 5.3. Separation of the two obligations

**Addressed.**

The manuscript explicitly says that capacity and paired-trace deconcentration are different. It does not describe verification of SC as verification of the pointwise theorem.

### 5.4. Complete finite-count error and legal limit order

**Addressed.**

The full two-cap error is displayed before the collision limit. The zero-gradient layer cake is formed at finite count. Every auxiliary band is fixed before \(m\), enlarged only afterwards, and the reconstruction parameter \(B\) remains outermost.

### 5.5. Scalar-first discipline

**Addressed.**

No unrestricted posterior, likelihood, entropy, path-total-variation, or same-roof conditional theorem is promoted from the new capacity result.

### 5.6. Independent specialist verification

**Not addressed.**

The repository records no independent human audit of the new pressure proof, inherited spectral chain, coarea constructions, or trace theorem.

## 6. Audit of module 238: global momentum uniqueness and stable optical weight

### 6.1. Global fixed-itinerary uniqueness

The theorem fixes a lifted sequence of scatterers and the two endpoint tangential momenta. For two candidate regular trajectories, the polygonal length

\[
S(Q)=\sum_{j=0}^{m-1}|Q_{j+1}-Q_j|
\]

is convex in the Cartesian contact variables. Monotonicity of its gradient gives

\[
\sum_j
(\nabla_jS(Q)-\nabla_jS(\widehat Q))
\cdot(Q_j-\widehat Q_j)\ge0.
\]

Because the two contacts at time \(j\) lie on the same circular scatterer,

\[
Q_j-\widehat Q_j=R(n_j-\widehat n_j).
\]

The fixed endpoint momenta give equal endpoint normal speeds, while the tangent contribution vanishes against the normal difference because rotation by ninety degrees is skew symmetric. The displayed monotonicity sum becomes the negative of a sum of strictly positive coefficients times

\[
|n_j-\widehat n_j|^2.
\]

It can be nonnegative only if all contacts coincide.

This is a legitimate global argument. It does not assume convexity of the physical word domain or an interpolating family of physical trajectories. Repeated visits to one scatterer are handled as distinct Cartesian variables.

I found no sign defect in this proof.

### 6.2. Optical density and stable Jacobian

The module derives

\[
C_0^{-1}c_mJ^sT_R^m(x)
\le \omega(x)
\le C_0c_mJ^sT_R^m(x).
\]

The proof compares the relevant matrix entry with the unstable Jacobian using invariant cones, and then uses the exact collision-area identity

\[
J^uT_R^mJ^sT_R^m
\frac{e(T_R^mx)}{e(x)}
=rac{c_0}{c_m}.
\]

Uniform transversality of the stable and unstable cones prevents an accumulating angle constant. This is the correct mechanism.

The one-step estimate

\[
\frac{J^sT_R(x)}{c(x)}\le C_1
\]

then removes the stable factor at a marked inverse incidence.

### 6.3. Marked incidence removal

For an internal mark \(i\), the cocycle is factored at time \(i\), and the one-step estimate is applied to the factor carrying \(c_i^{-1}\). This gives

\[
\frac{\omega(x)}{c_i(x)}
\le C
J^sT_R^i(x)
J^sT_R^{m-i-1}(T_R^{i+1}x).
\]

No inverse-incidence multiplier remains on the right. This is essential for the later factorization of itinerary sums.

I found no missing stable factor or off-by-one error in the displayed decomposition.

## 7. Audit of module 239: actual momentum-fiber pressure comparison

### 7.1. Physical itinerary sums

The module defines

\[
P_j(R)=
\sum_{w\in\mathcal W_j(R)}
\sup_{x\in[w]_R\cap M'}J^sT_R^j(x),
\]

where \(w\) is a realizable lifted physical itinerary. Endpoint section, guard, occupation, and exact-label restrictions are dropped only on the upper side.

Each homogeneous continuity cell determines a physical itinerary, so refining by homogeneous cells gives

\[
P_j(R)\le Q_j(R).
\]

This is an inequality between positive sums, not an identification of physical words with homogeneous cells.

### 7.2. Fiber comparison

Global uniqueness gives at most one momentum-fiber preimage per lifted itinerary. The unmarked part is controlled by \(P_m(R)\). For the internal mark \(i\), an itinerary is determined by:

- its first \(i\) flights;
- one physical middle step; and
- its last \(m-i-1\) flights.

The middle step has uniformly finitely many lifted choices by finite horizon. Therefore

\[
\mathcal K_m(R)
\le
1+C\left[
P_m(R)+D\sum_{i=1}^{m-1}q_0^{d_i}
P_i(R)P_{m-i-1}(R)
\right].
\]

The argument does not count homogeneous strips after the marked stable factor is removed. This directly addresses the central objection to the fixed-count multiplicity \(N_m\) in revision 98.

### 7.3. Fixed-radius result versus family result

At a fixed radius, the established pressure theorem gives bounded \(Q_j(R)\), and hence bounded capacity. Revision 99 correctly did not interchange this pointwise-in-radius bound with \(\sup_R\limsup_m\).

The uniform family question is delegated to module 241 rather than hidden by compactness.

## 8. Audit of module 241: uniform geometric pressure by finite tests

This is the most delicate new module and the principal place where independent billiards expertise is required.

### 8.1. Uniform family geometry

The radius family has common:

- positive minimum and finite maximum free flight;
- positive lower and upper curvature;
- bounded boundary derivatives;
- invariant cone bounds and cone separation;
- finite one-flight displacement alphabet; and
- homogeneous-strip geometry.

The cited uniform-family theory supplies common hyperbolicity, distortion, and curve-growth constants under such bounds. The manuscript also notes that changes in physical arclength can be represented by uniformly bounded coordinate changes.

This is an appropriate starting point. The proof does not appeal to a parameter-uniform mixing time.

### 8.2. Uniform curve growth

For a homogeneous short stable curve \(W\), the manuscript uses

\[
\sum_{V\in\mathcal G_j(W)}
\sup_VJ_VT_R^j
\le C_g.
\]

This is the correct uniform curve-growth estimate for inverse-image components. It is exactly the type of positive bound needed after the finite-testing assignment.

### 8.3. Whole-cell distortion

The proof requires comparison of stable Jacobians on different short stable curves lying in the same homogeneous backward cell. It does not suffice to compare two points on one curve.

The cited whole-cell distortion lemma is formulated at the cell level and is the appropriate input. The manuscript uses it before the final subcell is selected; the test curve need not meet the particular last-step subcell.

This is a subtle but coherent use of the input.

### 8.4. Uniform long-cell fraction

The manuscript reconstructs the long-cell reduction with common one-step contraction, common geometric loss series, finite initial iterates, and common expansion. It obtains

\[
c_{\rm long}Q_m(R)
\le
\sum_{A:\,\operatorname{diam}^uB_{m-1}(A)\ge\delta_*}
\sup_AJ^sT_R^m.
\]

The proof does not infer uniformity from the fixed-table limiting pressure theorem. Instead it traces each choice to common geometric constants and finitely many initial iterates.

I found no explicit reversal of quantifiers. The validity of the claimed common long-cell fraction is nevertheless a major specialist-audit item.

### 8.5. Finite stable testing

For every radius, finitely many short stable test curves are selected so that every long unstable backward cell meets one test. The number of tests is uniform because:

- a long cone-unstable arc has a uniformly positive transverse projection;
- it cannot remain in an arbitrarily thin homogeneity strip;
- only finitely many strip indices are therefore relevant; and
- a transverse grid of sufficiently small mesh meets every such arc.

The tests may depend on \(R\), but the numerical bound on their number does not.

The proof then assigns each backward cell to its first meeting test. Connected intersections with one test determine homogeneous inverse branches. Distinct backward cells give disjoint inverse components, so one inverse component is not charged twice.

This is the new geometric idea of revision 100. I do not see an immediate multiplicity defect in the written assignment. Its validity depends on the claimed stable-convexity of backward cells and on the treatment of chart and strip boundaries. Those points require independent line-by-line verification.

### 8.6. Bounded final physical split

For fixed backward cell \(B\), the possible forward cells \(A\) arise from the last true one-step singularity cuts. The manuscript claims a uniform bound \(D_*\) because only finitely many disks can be the next hit and each singularity graph cuts a stable-convex cell in at most one connected arc.

The absence of a final homogeneity cut in the selected partition convention is important. If a countable final strip split were present, the argument would fail. The manuscript states the convention explicitly.

I found the stated partition bookkeeping internally consistent. This remains another specialist-audit point.

### 8.7. Pressure estimate

Combining the long-cell fraction, the bounded final split, whole-cell distortion, finite tests, injective inverse-component assignment, and curve growth gives

\[
\begin{aligned}
c_{\rm long}Q_m(R)
&\le C_1D_*C_d
\sum_{j=1}^{N_*}
\sum_{V\in\mathcal G_{m-1}(W_j)}
\sup_VJ_VT_R^{m-1}\\
&\le C_1D_*C_dN_*C_g.
\end{aligned}
\]

Hence

\[
\sup_R\sup_mQ_m(R)<\infty.
\]

The algebraic conclusion follows from the preceding lemmas. I found no missing factor growing with \(m\) in the written sum.

My assessment is therefore:

- the proof is a serious direct attempt at the correct family-uniform statement;
- it does not merely relabel a fixed-table theorem;
- its use of published uniform growth and whole-cell distortion is compatible with those inputs;
- no decisive internal contradiction is apparent; but
- the finite-test geometry, stable-convexity, long-cell uniformity, and final-split count are sufficiently load-bearing that independent billiards specialists must reconstruct them before publication.

## 9. Audit of module 242: uniform capacity and uncut moments

### 9.1. Uniform capacity

Inserting the uniform bound \(P_j(R)\le Q_*\) into the actual momentum-fiber comparison gives

\[
\mathcal K_m
\le
K_*:=
1+C\left(
Q_*+DQ_*^2\frac{2q_0}{1-q_0}
\right).
\]

The depth weights are summable, and no physical-word cardinality remains.

For each fixed admissible band, \(\theta_{B_*}<1\), so

\[
m^6\mathcal K_m\theta_{B_*}^{2m}
\le K_*m^6\theta_{B_*}^{2m}
\longrightarrow0.
\]

This is the correct verification of SC. No block length depending on \(m\) is used.

The optional finite-block certificate follows by choosing a fixed block \(L\) after the band has been fixed. It is not needed for the direct bounded-capacity implication.

### 9.2. Two-cap layer cake

For

\[
w_{p,b}(t)\,dt
=F_\#\left(I_mz^{-p}\mathbf1_{\{0<z<b\}}\bar\nu\right),
\qquad 1\le p<\alpha=\frac{129}{128},
\]

the inherited spectral cap and the physical quadratic cap give an error majorant

\[
\min\{Ev^{1/2},Hv^2\}.
\]

The crossing scale is

\[
v_0=(E/H)^{2/3}.
\]

The positive layer cake yields the error scale

\[
E^{(4-2p)/3}H^{(2p-1)/3}.
\]

The exponents of the common \(m^2\) factor add to one. The exponential factor is

\[
\theta_{B_*}^{m(4-2p)/3},
\]

which decays for the stated range. The leading critical-volume integral is finite because \(p<\alpha\). The quadratic lower-scale integral is finite because \(p<2\).

The exponent bookkeeping is correct.

### 9.3. Scope of the moment theorem

The theorem controls

\[
I_mz^{-p},
\]

not

\[
(I_m/z)^p.
\]

This distinction is maintained in the abstract, theorem, response, ledger, and manifest.

### 9.4. Limit order

At fixed \(b,L,B_*\), the finite-count error tends to zero uniformly in radius and exact labels. The band is enlarged only after the collision limit. The large-gradient part of \(v^0\) uses the inherited complete \(I_m\) source bound.

I found no illegal collision-dependent lower cutoff or growing band.

## 10. Audit of module 243: uniform source recovery

### 10.1. Long critical residual

The inherited finite-count target certificate is

\[
\mathsf C^\varepsilon(t)
\le
C_0\int_t^{t+d}w_{1,b}(u)\,du,
\qquad
b=(a^2+2\Lambda_\circ d)^{1/2}.
\]

Applying the uniform uncut first-gradient estimate gives

\[
\limsup_m\sup_{R,n,k}
 m^2\|\mathsf C^\varepsilon\|_\infty
\le
Cd(a^2+2\Lambda_\circ d)^{1/256}.
\]

On the retained schedule \(a^2=qr\) and \(d=2qr\), this is

\[
C(qr)^{257/256}.
\]

The exponent is correct.

### 10.2. Short-segment trace-comparison error

The inherited finite-count inequality is

\[
|R_H^\varepsilon(t)-T_H^\varepsilon(t)|
\le
C(1+\varepsilon^{-1})
\int_{t-\delta}^{t+\delta}v^0(u)\,du.
\]

The new uniform \(v^0\) estimate yields

\[
\limsup_m\sup_{R,n,k}
 m^2\|R_H^\varepsilon-T_H^\varepsilon\|_\infty
\le C(1+\varepsilon^{-1})\delta.
\]

The target selector is held at the target roof and is not differentiated. The Borel maximal-segment map counts intermediate physical interiors once. This is the correct use of the comparison theorem.

If one endpoint is grazing, its weighted optical trace is zero, so the paired minimum is zero. A backward critical trace may be nonzero and is retained.

### 10.3. Scalar reduction

The final inequality is

\[
\mathcal E_M
\le
\mathcal H_M(T_{\mathsf S}^{\varepsilon(B)})
+C_MB^{-1/192}
+C(qr)^{257/256}
+C(1+\varepsilon(B)^{-1})qr.
\]

With \(r=c\varepsilon^4\), the new explicit terms have sizes

\[
(qr)^{257/256}=O(\varepsilon^{257/64}),
\qquad
(1+\varepsilon^{-1})qr=O(\varepsilon^3).
\]

Both tend to zero. The capacity condition no longer appears as a hypothesis.

This is a genuine improvement over revision 98.

## 11. The decisive remaining positive boundary source

For the short residual \(\mathsf S\), the paired trace is schematically

\[
T_{\mathsf S}^\varepsilon(t)
=
\int
\mathbf1_{\{a_\sigma<t<b_\sigma\}}
\mathbf1_{\mathsf S}(\Psi_\sigma(t))
\min\{f_\sigma^-,f_\sigma^+\}\,d\sigma.
\]

This quantity is nonnegative. The two traces belong to the same maximal physical segment and retain the original guard and endpoint conventions.

The trace-comparison theorem says that the interior target density is close to this minimum on sufficiently short segments. It does not say that the minimum is small.

Several already established facts are insufficient:

1. **Small short-segment volume mass is insufficient.** A positive roof density may be supported on an interval of vanishing length while retaining fixed height.
2. **Small outgoing-minus-incoming trace is insufficient.** Two large positive traces can have a small difference.
3. **Bounded geometric pressure is insufficient.** Pressure controls weighted volume/fiber sums; it does not by itself deconcentrate the positive common boundary trace.
4. **The signed projected forcing is insufficient without a new comparison.** The minimum is formed before summing physical sheets and is not the Jordan positive part after projection.
5. **One-sheet Hölder regularity is insufficient.** Summing a one-sheet modulus over an uncontrolled transverse family reintroduces the multiplicity problem unless a new physical capacity theorem controls the sum.
6. **Grazing trace vanishing is insufficient.** The remaining source is precisely the nongrazing part; backward critical entrances may carry nonzero traces.

The required theorem must operate in the original normalized essential-height topology.

A sufficient quantitative form would be

\[
\mathcal H_M(T_{\mathsf S}^{\varepsilon})
\le
C_M\varepsilon^{-Q}\delta^\beta,
\qquad \beta>0,
\]

with exponents compatible with \(\delta\asymp\varepsilon^4\), or any direct bound proving

\[
\mathcal H_M(T_{\mathsf S}^{\varepsilon(B)})
\longrightarrow0
\]

under a legal outer schedule.

This is not a cosmetic last line. It is the exact mechanism that can still sustain a nonpersistent pointwise upper spike.

## 12. Limit order and quantifier audit

The legal order in revision 100 is:

1. form every physical itinerary sum, marked source, endpoint trace, source restriction, and projected scalar comparison at finite collision count;
2. fix the reconstruction parameter \(B\);
3. at that fixed \(B\), fix \(\varepsilon(B)\), \(q\), \(r\), \(a\), \(\delta\), the auxiliary band \(B_*\), and all other positive thresholds;
4. take the collision limsup and the supremum over the prescribed radius interval and exact labels using the newly proved uniform constants;
5. enlarge the previously fixed auxiliary band only after that limit; and
6. send \(B\to\infty\) last.

The new pressure estimate is proved before the radius and collision suprema are taken. It is not obtained by reversing a fixed-radius limit.

The finite stable test curves may depend on the radius, but their number and all geometric constants are uniform. This is compatible with taking the radius supremum after the finite-count estimate.

I found no cutoff chosen as a function of the collision count.

## 13. Claims established and claims still open

Subject to the inherited inputs and the correctness of the new geometric pressure proof, revision 100 establishes:

- global fixed-itinerary endpoint-momentum uniqueness;
- optical/stable-Jacobian comparison;
- marked stable-factor removal;
- actual weighted momentum-fiber pressure comparison;
- radius-uniform bounded geometric pressure;
- radius-uniform bounded weighted momentum capacity;
- family-uniform verification of SC at every fixed admissible band;
- uncut concentration for \(I_mz^{-p}\), \(1\le p<129/128\);
- radius-uniform long critical residual height;
- radius-uniform short trace-comparison height;
- radius-uniform recovery of all grazing-ended short sources; and
- a family-uniform scalar reduction with one positive source remaining.

It does not establish:

- decay of the positive paired trace on short nongrazing segments;
- the corresponding result even at one fixed radius;
- vanishing of the complete residual upper source;
- unconditional upper-spike persistence;
- the unrestricted upper pointwise half;
- the full raw return LLT;
- unrestricted same-roof point-conditioned kernel convergence;
- forward essential-likelihood convergence;
- unrestricted path total variation or relative entropy convergence;
- independent human specialist approval; or
- a formal proof certificate.

The source manifest, publication-status file, proof ledger, response, referee-status file, and specialist-audit file represent these boundaries accurately.

## 14. Requirements for a successful next revision

### 14.1. Prove positive paired-trace deconcentration

The next revision should be organized around a theorem that controls

\[
T_{\mathsf S}^{\varepsilon}
\]

itself, not only its difference from the interior source.

The theorem must include all nongrazing short segments selected by the original residual and must retain nonzero backward critical traces.

### 14.2. Work after physical summation or prove bounded overlap

A sheetwise endpoint modulus is not enough. A successful argument should either:

- operate directly on the physically summed trace measure; or
- prove a collision-uniform bounded-overlap/capacity theorem which justifies summing sheetwise estimates.

No unweighted word count should appear.

### 14.3. Possible mathematical routes

Plausible routes include, but are not limited to:

1. a two-ended transverse capacity estimate for the common positive trace;
2. a bounded-overlap theorem for endpoint-momentum fibers of genuinely short segments;
3. a residence-shell persistence theorem showing that a large paired trace forces nearby roof mass of quantitative width;
4. a signed entrance/termination current whose projected cancellation controls the positive common part rather than only the trace difference;
5. a reverse-Hölder or maximal inequality for the physically summed boundary trace;
6. a same-segment endpoint map with a Jacobian gain converting the short length into a positive power after transverse integration; or
7. regularity above the one-dimensional pointwise embedding threshold with a norm which vanishes under the outer schedule.

Any chosen route must be proved for the complete exact-label physical source.

### 14.4. State an explicit rate compatible with the outer schedule

A result of the form

\[
\mathcal H_M(T_{\mathsf S}^{\varepsilon})
\le C_M\varepsilon^{-Q}\delta^\beta
\]

must be accompanied by an explicit check that the retained or rebalanced choice of \(\varepsilon(B),q,r,a,\delta\) makes every term vanish.

A finite-mass, weak-type, or fixed finite-\(p\) estimate alone is not sufficient.

### 14.5. Preserve exact physical conventions

The proof must retain:

- the original exact labels;
- the original section and guard;
- the actual Borel target selector;
- both physical endpoint traces;
- the nonzero backward critical trace when present;
- all arithmetic classes, including zero classes in the unnormalized theorem; and
- the established order of limits.

### 14.6. Close the scalar theorem before further downstream promotion

Only after the positive paired-trace height is proved should the manuscript promote unrestricted denominators, same-roof ratios, likelihoods, entropies, or point-conditioned path laws.

### 14.7. Obtain independent specialist verification

Before a claim of top-four readiness, independent specialists should reconstruct at least:

- the global fixed-itinerary uniqueness theorem;
- the optical/stable-Jacobian normalization;
- the marked pressure comparison;
- the uniform long-cell reduction;
- the finite stable-testing construction;
- stable-convexity and inverse-component injectivity;
- the bounded final physical split;
- the uncut layer-cake theorem;
- the inherited four-record spectral and critical-volume inputs;
- the Borel maximal-segment and endpoint-trace constructions; and
- the eventual positive paired-trace theorem.

### 14.8. Consolidate the final presentation

If scalar closure is achieved, the paper should present a compact dependency graph for the current theorem. Hundreds of historical modules may remain archived, but the principal argument should not require readers to infer which historical conditional statements have been superseded.

## 15. Exposition

The focused revision-100 article is candid and materially clearer than the full archive. The following distinctions should remain explicit.

1. The uniform pressure theorem closes SC; it does not close the pointwise theorem.
2. The short trace-comparison error is not the positive paired trace.
3. The paired minimum is not a projected Jordan positive part.
4. A backward critical trace may be nonzero.
5. The moment theorem concerns \(I_mz^{-p}\), not \((I_m/z)^p\).
6. The uniform pressure proof is direct and should not be summarized as compactness plus fixed-table convergence.
7. The finite stable tests may depend on \(R\), while their count and constants are uniform.
8. Exact-SHA workflows certify source/build identity, not the continuum proof.
9. The plain v100 placeholder branch should not be confused with the later uniform-capacity manuscript.
10. Historical provenance should remain supplementary rather than dominate the theorem narrative.

## 16. Significance and venue assessment

Revision 100 represents a genuine mathematical advance over revision 98. In particular, the following ideas may be reusable beyond this manuscript:

- Cartesian monotonicity for endpoint-momentum uniqueness;
- removal of a marked inverse incidence through stable cocycles;
- comparison of actual weighted momentum fibers with geometric pressure;
- finite transverse testing of long backward cells;
- family-uniform pressure without a uniform mixing time; and
- positive two-cap integration of a singular gradient insertion.

If independently verified, the cumulative modules 238--243 could support a strong specialized paper on singular transport and pointwise inversion in dispersing billiards, even before the final pointwise theorem is closed, provided the publication claim is reorganized accordingly.

At the requested *Annals/Acta/Inventiones/JAMS* benchmark, however, the manuscript is organized around the unrestricted uniform pointwise raw local limit theorem. The present revision ends with an exact reduction to an unproved positive boundary-trace height. That remaining source is capable of carrying the full upper obstruction. The governing theorem therefore remains incomplete.

Even after the paired-trace theorem is supplied, the breadth and novelty claim would require an independent expert audit and a sharply consolidated presentation. At present the missing scalar theorem is already decisive.

## 17. Final recommendation

Revision 100 responds seriously and positively to the revision-98 report. It incorporates the v99 momentum-fiber bridge, proves a direct family-uniform geometric pressure estimate, bounds the actual weighted momentum capacity uniformly, verifies SC, establishes uncut gradient moments, and recovers the critical and grazing-ended residual sources without an extra capacity premise.

I found no decisive internal error in modules 238--243 at their stated scope, conditional on the inherited inputs. The new pressure theorem is delicate and must be independently checked, but it is not merely a relabeling of a fixed-radius result.

Nevertheless, the positive paired short-trace height on nongrazing segments is not proved to vanish, even at a fixed radius. The scalar upper endpoint, unrestricted pointwise exact-label raw local limit theorem, and unrestricted downstream laws therefore remain unproved.

**I recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**
