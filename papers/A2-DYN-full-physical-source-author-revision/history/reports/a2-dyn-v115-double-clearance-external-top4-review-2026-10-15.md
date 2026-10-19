# External top-four referee report on A2-DYN revisions 114–115

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branch:** `revision/a2-dyn-v115-double-clearance-transversality-2026-10-15`  
**Reviewed author commit:** `31792379408c5ace2c09284c2eb22d2331023433`  
**Reviewed repository tree:** `008dba443ce2ca29b3e276b1bf05bcf7021011c1`  
**Active manuscript directory:** `papers/A2-DYN-v115-double-clearance-author-revision`  
**Active mathematical source:** numbered modules 260–276; revision 114 supplies the clearance-to-roof and critical-roof modules 274–275, and revision 115 adds module 276  
**Immediate complete scientific baseline:** revision-114 full-delivery commit `8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`, paper tree `c2e9e83f39985a34690300433f4b40de4f1f88ac`  
**Revision-114 branch head:** documentation-only successor `d98549fc721f757ad2a4b5918d57110368acbf9f`  
**Controlling substantive report:** `reviews/a2-dyn-v112-incidence-load-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `d7fd0b24314d7341f9a611130bb650371d2d5ef2` / `0ad9f500c92db32ea4fc9f6d9ee28630b4484699`  
**Intervening submission-state report:** `reviews/a2-dyn-v113-submission-state-external-top4-review-2026-10-15/REFEREE_REPORT.md`; it reviewed a workflow-only branch, not the mathematics of revisions 114–115  
**Exact-SHA qualification at review freeze:** v114 run `38821386148`, queued; v115 run `38832286710`, queued  
**Date:** 15 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, an independent human billiards/probability/geometric-measure-theory audit, or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revisions 114 and 115 are genuine theorem-bearing author revisions. They are not branch aliases, source-export checkpoints, or documentation-only changes. Since revision 114 did not receive a substantive mathematical referee report before revision 115 was built on it, I have reviewed the entire unreviewed clearance increment rather than treating revision 114 as an externally certified baseline.

The new mathematics is real and, within its stated local or retained-input scopes, largely coherent.

Revision 114 develops four substantive interfaces:

1. an exact finite-itinerary Jacobian from a physical unvisited-clearance mark to the endpoint coordinates and to the roof/Gauss-angle coordinates;
2. local positive roof-density estimates for finite-type charts and angular folds, integrating the clearance variable before taking the roof supremum;
3. an exact identification of regular critical roof trajectories with reversing periodic orbits, together with a return-stability expression for the critical density coefficient; and
4. a selector-uniform local critical coarea formula which retains one-sided unvisited boundaries and section cuts instead of setting their positive traces to zero.

Revision 115 adds a second-order physical clearance theorem. For two distinct unvisited disks marked on one actual free flight it proves a uniform angular transversality constant, an exact ordered two-mark coarea identity, and a quadratic second-factorial bound. It follows that the excess of the mark count over the one-witness indicator has total variation `O(epsilon^2)` on the original collision-end depth schedule, even with the original exact labels retained.

I audited the active modules

- `core/270_exact_clearance_flux.tex`;
- `core/271_transverse_clearance_geometry.tex`;
- `core/272_clearance_transfer_tests.tex`;
- `core/273_record_disintegration_and_bridge.tex`;
- `core/274_clearance_roof_coarea_and_folds.tex`;
- `core/275_critical_roofs_reversibility_and_stability.tex`;
- `core/276_exact_two_mark_clearance_flux.tex`;

as well as the active manuscript, response, proof ledger, source manifest, publication-status file, validation/execution records, literature audit, the revision-112 controlling report, and the exact Git chronology separating workflow-only revision 113 from the theorem-bearing revision 114 source.

Within the assumptions actually stated in those files, I found no decisive missing factor in the one-mark or two-mark collision measure, no reversed coarea Jacobian, no evident double counting of ordered clearance pairs, no incorrect factor in the critical return-stability coefficient, no hidden independence assumption, no uncontrolled physical-word multiplier, no invalid positive-source subtraction, and no illegal insertion of a collision-dependent roof or spectral window into a fixed-window theorem.

The negative recommendation is nevertheless forced by the exact endpoint of the argument. The organizing theorem remains equivalent to the collision-normalized pointwise shortage limit inherited from revision 112. In the current notation the paper still requires, for every fixed central-window parameter `M`,

\[
\lim_{B\to\infty}\limsup_{m\to\infty}\sup_{R,n,k}m^2
\operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}
\bigl(\mathsf U_{B,m}^{\rm low}(t)-K_BP_{r_B,m}^{\rm ng}(t)\bigr)_+
=0.
\]

No theorem in revisions 114–115 establishes this limit.

The local fold and critical-roof estimates do not come with a collision-uniform complete chart sum in the required `m^2 L^infty(dt)` topology. The two-mark theorem controls duplicate marks on one flight in total variation; it does not control the first-order single-mark clearance source, marks on different flights, or the roofwise height of the clearance-selected exact-record measure. Capacity abundance for the full nongrazing pool remains open. Low-incidence shallow source, positive critical/section contributions outside the verified local charts, and singular pairing configurations also remain.

Thus the revisions solve several finite-dimensional geometric and local coarea problems, but they do not close the positive obstruction which is itself equivalent to the claimed raw pointwise local limit theorem. At the requested benchmark this is decisive.

## 2. Frozen source and chronology

The visible revision-115 author branch resolves to

`31792379408c5ace2c09284c2eb22d2331023433`.

Its repository tree is

`008dba443ce2ca29b3e276b1bf05bcf7021011c1`.

The active article is

`papers/A2-DYN-v115-double-clearance-author-revision/main.tex`.

The branch parent is

`d98549fc721f757ad2a4b5918d57110368acbf9f`.

That parent is the documentation-only head of the genuine revision-114 branch. Its own parent,

`8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`,

is the complete theorem-bearing revision-114 delivery. The latter adds the full clearance-roof paper packet, including modules 274–275; the later head only adds a post-push publication receipt and does not change the scientific article.

The revision-113 branch previously carrying the label `clearance-geometry` was workflow-only. The revision-113 submission-state report correctly did not treat that branch name as a manuscript. Revision 114 subsequently supplied actual mathematical source, and revision 115 now extends that source. Accordingly, the present report reviews the mathematical increment from the revision-112 author source through the revision-115 author source.

The revision-115 packet preserves the complete revision-114 source beneath

`provenance/v114-frozen`,

and keeps active modules 260–275 byte-identical to the revision-114 article. Its new proof module is

`core/276_exact_two_mark_clearance_flux.tex`.

The current review branch starts directly from the exact revision-115 author commit and adds only this report under

`reviews/a2-dyn-v115-double-clearance-external-top4-review-2026-10-15/`.

No author source, workflow, historical report, preserved packet, or unrelated paper is intentionally modified.

## 3. Qualification evidence and its boundary

The revision-115 packet records a completed local native build split into the same fail-closed phases as its monolithic build script. The recorded results include:

- successful source-identity checks for the active source, the frozen revision-114 packet, and the preserved revision-112 files;
- execution of the inherited finite checks and the new two-mark diagnostics under ordinary and optimized Python;
- 1,296 exact root/Jacobian cases, 18 numerical angular coarea comparisons, and 3,000 actual next-collision Lorentz rays for the new module;
- a three-pass native build of the preserved revision-112 article to 31 pages;
- a three-pass native build of the revision-115 article to 51 pages;
- zero unresolved references, zero multiply-defined labels, and zero overfull boxes in the finalized logs.

At the freeze of this report, the remote exact-SHA workflows were still queued:

- revision-114 run `38821386148` at author commit `8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`;
- revision-115 run `38832286710` at author commit `31792379408c5ace2c09284c2eb22d2331023433`.

I therefore do not describe either revision as remotely qualified at this review freeze. A later successful run would improve source/build reproducibility but would not certify the continuum mathematics.

In particular, software qualification cannot prove:

1. the complete incident-component pairing construction and one-copy physical multiplicity;
2. the retained family-uniform pressure and stable optical comparison;
3. the regular/singular endpoint trace conventions on every physical component;
4. collision-uniform summability of all finite-type, fold, critical, and degenerate clearance charts;
5. a pointwise roof bridge for the clearance kernel;
6. capacity abundance for the nongrazing comparison pool;
7. decay of the remaining positive shortage; or
8. the full raw four-coordinate local inversion theorem.

The packet itself states these boundaries, although several pre-push metadata fields still read `remote_commit: null` and `remote_push_completed: false`. Those are frozen preparation-time records rather than the current Git state. This should be cleaned up in a later author packet without rewriting historical evidence.

## 4. Scope of this review

The substantive audit concentrates on:

1. the exact line-space Jacobian and global multiplicity in the one-mark flux theorem;
2. the interior-foot and finite-candidate geometry;
3. the grazing-uniform transversality calculation on stable test curves;
4. the use and exact status of the retained curve-growth input;
5. the exact-record roof-kernel disintegration and its normalization;
6. the long-record clearance-to-endpoint and roof/Gauss Jacobians;
7. the finite-type band estimate and integrated fold estimate;
8. critical half-path reversibility and the occupation convention;
9. the monodromy determinant and critical density coefficient;
10. the local polar coarea formula with arbitrary Borel cuts;
11. the pressure-based finite-count critical coefficient sum;
12. the two-mark lattice transversality constant;
13. the exact ordered double-mark coarea identity and its multiplicity;
14. the quadratic factorial bound, unique-mark law, and depth-scheduled duplicate payment;
15. the order of limits and the distinction between total variation, stable-test bounds, and roof essential height; and
16. the exact classes which remain unproved.

I do not independently re-prove the entire historical spectral, arithmetic, pressure, optical, and raw-inversion chain. Where the new proofs invoke a retained global input, the present assessment is relative to that input unless otherwise stated.

## 5. The inherited obstruction

Revision 112 had paid deep, numerous, and high-load incidence source but retained the positive low-incidence-load shortage

\[
\mathsf R_B^{\rm low}
=(\mathsf U_B^{\rm low}-K_BP_{r_B}^{\rm ng})_+.
\]

The remaining source permits clearance-only guards, including unvisited tangencies, and may also be capacity-deficient. The controlling report asked for a genuine target-roof summation or another collision-uniform positive-source estimate for these classes.

Revisions 114–115 attack the clearance side rather than renaming this residual. That is the correct direction. They establish exact physical line-space formulae, local roof coarea, critical density coefficients, and second-order multiplicity control. They do not alter the original section, roof, exact labels, arithmetic classes, or order of limits.

## 6. Exact one-mark clearance flux

Module 270 defines `N_delta` as the number of unvisited lattice disks whose distance from one actual free flight lies in `(R,R+delta)`. A mark is not inserted as a collision and does not change the collision count or physical roof.

The interior-foot lemma is correct on the stated radius range. At either incident endpoint, a third lattice center is at least distance `1-R` from the collision point, so its disk clearance is at least `1-2R`. A near miss below `delta_*=(1-2R_+)/4` cannot attain its minimum at an endpoint. The perpendicular foot is therefore in the open flight and stays a uniform positive distance from both incident collisions.

The local Jacobian calculation is also consistent. With physical collision measure

\[
d\nu=\frac{d\alpha\,dp}{4\pi},
\]

line direction `vartheta` and signed impact `b` satisfy

\[
\left|\det D_{(\alpha,p)}(\vartheta,b)\right|=R,
\qquad
 d\nu=\frac{d\vartheta\,db}{4\pi R}.
\]

The two impact signs and `db=du` then yield

\[
\int\sum_{z\in\mathcal Z_\delta(x)}a(x,z)\,d\nu(x)
=
\frac1{4\pi R}\sum_{\sigma=\pm1}
\int_0^{2\pi}\int_0^\delta
 a(X_R,Z_R)\,du\,d\vartheta.
\]

The global inverse construction is plausible and properly distinguishes the marked disk from the two incident disks. Tangent partitions are treated as null sets and the proof uses monotone exhaustion before assuming integrability. I found no missing factor of two or radius in the displayed identity. Setting `a=1` gives the exact mean

\[
\int N_\delta\,d\nu=\delta/R.
\]

This is a useful exact Crofton-type identity. It is, however, an integrated collision-space statement, not a roofwise density estimate.

## 7. Transverse clearance geometry and stable tests

Module 271 proves a one-flight strip estimate on short stable-type test graphs. On an increasing-slope graph the signed impact derivative is

\[
b_z'=-\cos\varphi-t_z\vartheta'.
\]

At a physical forward near miss the foot time `t_z` has a uniform positive lower bound, while `vartheta'` is uniformly positive. Hence `-b_z'` is uniformly bounded below even near grazing. The argument controlling the number of impact-band crossings through monotonicity of `beta-vartheta` is coherent on the prescribed short curve length.

The backward-flight result follows by time reversal. The theorem is deliberately stated for physical arclength and bounded representatives rather than as a multiplier theorem on an unspecified anisotropic distribution space. That restraint is correct.

Module 272 propagates this local clearance gain through arbitrarily many collisions only after stating a retained homogeneous stable-curve growth input. Under that input, branchwise change of variables gives a stable-test seminorm of order `delta^(1-a)`, uniformly in collision count and record frequencies.

This is genuine uniform information, but its topology is weaker than the required roof essential height. The absence of growth in the roof Fourier frequency is not decay in that frequency, and the result does not justify an unbounded Fourier inversion. The manuscript correctly says so.

The retained curve-growth input remains a load-bearing specialist interface. A top-four evaluation cannot treat the local geometric proof as an independent reconstruction of that global functional-analytic theorem.

## 8. Exact-record disintegration and the missing bridge

Module 273 preserves the exact return, displacement, collision-count, section, and roof information in the positive kernel

\[
\mathcal K_{m,R,n,k,j,u}.
\]

The normalization

\[
\int\mathbf1_\Pi N_\delta(T_R^jx)
       \mathbf1_{\{L_{m,R}\in A\}}\,d\nu_R^*
=
\frac1{4\pi Rc_*}\int_0^\delta
\mathcal K_{m,R,n,k,j,u}(A)\,du
\]

is consistent with the one-mark flux and the original section normalization. There is no second factor of `c_*`.

The module then states a strong sufficient bridge:

\[
\mathcal K_{m,R,n,k,j,u}|_{\mathcal C_{m,R,n,k}(M)}
\le C_Mm^{-2}\,dt.
\]

This bridge is explicitly unproved. Neither the one-flight flux nor the stable-test estimate establishes it. The long-time derivative of the roof along the marked line can have folds, cancellations, and critical points.

This is the right normalization to expose, but it is also a precise statement of the remaining problem. The subsequent revision-114 local coarea estimates control selected chart types; they do not prove this bridge or a summed substitute for the complete physical source.

## 9. Long-record Jacobian

Module 274 introduces the endpoint map

\[
\mathcal Q_j(\vartheta,u)=(\alpha_0,\alpha_m)
\]

for a marked physical itinerary and the roof

\[
S=F\circ\mathcal Q_j.
\]

The determinant identities

\[
|\det D\mathcal Q_j|=(R\omega)^{-1},
\qquad
|\det D(S,\arg\nabla F)|=\chi/(R\omega)
\]

are consistent with collision-area preservation, the line-coordinate Jacobian, and the endpoint optical derivative. The normalization check recovers exactly

\[
\omega/(4\pi c_*\chi)
\]

as the target roof/Gauss-angle density.

The Hessian formula

\[
D^2S=A^{\mathsf T}GA+
       \sum_ag_aD^2(\mathcal Q_j)_a
\]

correctly retains the second term away from a critical roof. At `g=0` the term vanishes and

\[
\sqrt{\det D^2S}=\frac{\sqrt{\det G}}{R\omega}.
\]

I found no determinant or section-normalization error in this calculation.

The resulting exponential lower bound concerns determinants. It does not control the smallest singular value, the condition number of the chart, the number of charts, or the sum of inverse Jacobians. Those missing statements are exactly what a global roof-density theorem would need.

## 10. Finite-type bands and integrated folds

The one-dimensional band lemma in module 274 is proved rather than imported. Its divided-difference argument yields

\[
|\{a<f<a+h\}|\le2\ell(h/\kappa)^{1/\ell}
\]

under `|f^(ell)|>=kappa`. The factorial factors in the divided-difference denominator and the final constant are consistent.

The finite-type theorem uses monotonicity in the clearance coordinate and applies the band estimate to the base roof `S(vartheta,0)`. It gives a local density of order

\[
\delta^{1/\ell}
\]

with all Borel event cuts retained on the source side.

The simple-fold theorem is also analytically coherent. Strict angular convexity gives at most two roots, with fixed-clearance density behaving like

\[
(t-v(u))^{-1/2}.
\]

Monotonicity of the fold value in `u` makes this singularity integrable and yields

\[
\|D_{E,h,\delta}\|_\infty
\le2H_f\sqrt{\frac{2\delta}{a_fb_f}}.
\]

The displayed normal form confirms the constant.

These are useful local theorems. Their hypotheses are not verified with collision-uniform constants on the complete physical chart family. In particular, charts with `S_u=0`, unclassified higher degeneracy, singular physical boundaries, and uncontrolled chart multiplicity remain. Summing local `delta^c` estimates over a collision-dependent family is not justified merely because each individual chart is controlled.

## 11. Critical roofs and reversing periodic orbits

Module 275 uses

\[
\nabla_qF=R(-p_0,p_m)
\]

so a regular endpoint roof is critical precisely when both endpoint momenta vanish. The geometric reversal argument then produces an actual `2m`-collision periodic orbit which retraces the half-path.

The manuscript correctly avoids claiming that the doubled occupation equals `2n`. The original section need not be invariant under time reversal; the correct identity is

\[
A_{2m,R}=A_{m,R}+A_{m,R}^{\mathcal I}.
\]

This is an important bookkeeping point and is handled correctly.

## 12. Monodromy and the critical coefficient

Writing the endpoint Hessian as

\[
G=\begin{pmatrix}a&e\\e&d\end{pmatrix},
\qquad \Delta=ad-e^2>0,
\]

the half-map derivative obtained from the generating relations is

\[
B=
\begin{pmatrix}
-a/e&-R/e\\
-\Delta/(Re)&-d/e
\end{pmatrix},
\qquad \det B=1.
\]

At normal endpoints, time reversal gives the full return derivative

\[
\mathcal M=JB^{-1}JB,
\qquad J=\operatorname{diag}(1,-1).
\]

For a determinant-one `B`,

\[
\operatorname{tr}(JB^{-1}JB)-2=4b_{12}b_{21},
\]

and substitution yields

\[
\operatorname{tr}\mathcal M-2
=\frac{4\Delta}{e^2}
=|\det(I-\mathcal M)|.
\]

Together with `omega=|e|/R`, this gives

\[
\mathfrak J(x)
=
\frac{\omega}{2c_*\sqrt{\Delta}}
=
\frac{1}{Rc_*\sqrt{|\det(I-DT_R^{2m})|}}.
\]

The signs and factor two are consistent. This is a local density coefficient attached to the marked reversing orbit, not a conditional probability or a periodic-orbit trace formula.

## 13. Critical local coarea

The critical coarea theorem normalizes endpoint coordinates by

\[
y=G_x^{1/2}(q-q_x),
\]

so the roof has Hessian `I` at the critical point. Polar coordinates and radial substitution give the local density

\[
D_E(t_x+s)=
\int_0^{2\pi}
\mathbf1_E(q_s(\theta))
 w(r_se(\theta))
 \frac{r_s}{\partial_rf(r_se(\theta))}\,d\theta.
\]

The leading coefficient is

\[
2\pi w(0)=\mathfrak J(x),
\]

not half that value. The error estimate of order `sqrt(s)` follows from the stated Hessian and weight Lipschitz bounds. The proof does not differentiate the Borel selector.

The formula is carefully local: it describes the source restricted to one coordinate ball. For an arbitrary exact-event cut the angular fraction `a_E(s)` is retained rather than assumed to have a limit. At an unvisited tangency or section cut, the auxiliary smooth action extension is used only to calculate the physical-side measure; no fictitious physical orbit or undefined return derivative is asserted.

This is a substantial clarification of the critical interface. It does not by itself give collision-uniform radii, error constants, separation of overlapping critical neighborhoods, or a complete sum of the local remainders in the normalized topology.

The pressure-based sum

\[
\sum_x\mathfrak J(x)
\le\frac{C_0Q_*}{2c_*\lambda_\circ}
\]

is a complete finite-count positive coefficient sum relative to the retained pressure input. It is unscaled and gives no `m^{-2}` gain. It also does not control the local `O(sqrt(s))` constants.

## 14. Two-mark transversality

Module 276 considers two distinct unvisited lattice disks on the same actual flight. If their signed impact parameters are `b_1,b_2`, then

\[
|b_2-b_1|
\le2(R_++\delta_*)=97/100.
\]

The triangular-lattice spacing gives `|z_2-z_1|>=1`, hence

\[
|(z_2-z_1)\cdot v_\vartheta|
=
\sqrt{|z_2-z_1|^2-(b_2-b_1)^2}
\ge\sqrt{591}/100.
\]

This excludes the simultaneous same-flight angular degeneracy uniformly on the stated radius and clearance ranges. The relative center belongs to a finite lattice set determined by the finite-horizon upper flight length.

The argument is elementary and correct. It does not use mixing, independence, symbolic renewal, or a word count.

## 15. Exact ordered two-mark coarea

After applying the one-mark flux to the first center, the second center is represented by a nonzero lattice difference `w`. For fixed first impact and signs, its impact equation is

\[
w\cdot v_\vartheta^\perp
=
\sigma_2(R+u_2)-\sigma_1(R+u_1).
\]

There are two angular roots, and the one-dimensional Jacobian is

\[
\left|\frac{\partial\vartheta}{\partial u_2}\right|
=
\frac1{\sqrt{|w|^2-d_{\sigma_1\sigma_2}(u_1,u_2)^2}}.
\]

The exact identity keeps a physical mask requiring both feet to lie on the same actual collision flight and prohibiting the marked disks from becoming reflections. This mask is retained in the equality and dropped only in the upper bound.

The multiplicity convention is consistent with an ordered pair. The first mark is fixed by the one-mark flux; the relative lattice vector, second sign, and angular branch then identify the second mark. The terms with `w` and `-w` correspond to the two opposite orderings and therefore should both be present.

I found no missing factor in the prefactor `1/(4pi R)` or in the eight sign/root choices used for the upper bound.

## 16. Quadratic bound and unique-mark law

Dropping the positive mask and using the transversality constant gives

\[
\int N_{\delta_1}(N_{\delta_2}-\text{same-center contribution})\,d\nu
\le
\frac{2N_{\rm pair}}{\pi Rc_{\rm pair}}\delta_1\delta_2.
\]

For equal clearances this is a bound on the second factorial moment `E[N_delta(N_delta-1)]`. Combined with the exact first moment `E[N_delta]=delta/R`, deterministic integer inequalities yield

\[
\nu(N_\delta\ge1)=\delta/R+O(\delta^2),
\qquad
\nu(N_\delta\ge2)=O(\delta^2).
\]

The lower bound for exactly one mark is also consistent. This is a genuine uniform first-order unique-clearance law and does not rely on a Poisson approximation.

For the collision-end depth schedule, invariance and positive domination give

\[
\int\mathbf1_\Pi\psi(L)
\sum_j\bigl(N_{\delta_j}-\mathbf1_{\{N_{\delta_j}\ge1\}}\bigr)
\,d\nu_R^*
\le
\frac{8C_{\rm pair}\varepsilon^2}{c_*(1-r^2)}.
\]

The factor `8` follows from at most two indices at each depth and `delta_j=2epsilon r^{d_j}`. This bound retains the original exact labels until the final positive domination.

## 17. What the two-mark theorem does not pay

The second-factorial estimate controls **duplicates**. It proves that, in a weak integrated sense, replacing the clearance mark count by the one-witness indicator costs only `O(epsilon^2)`.

It does not bound the one-witness indicator itself. The first-order mass remains

\[
\nu(N_\delta\ge1)=\delta/R+O(\delta^2),
\]

which is of order `delta`, not `delta^2`.

More importantly, neither estimate controls the roofwise `L^infty` height after conditioning on the complete exact record. A measure can have small total mass and still have a high density spike. The paper explicitly warns that the `O(epsilon^2)` total-variation gain cannot be multiplied by `m^2` at fixed outer `B`.

The theorem is also restricted to two marks on the same physical flight. It does not control:

- a single unvisited near miss;
- clearance marks on two different flights;
- correlations among many flights;
- a clearance-only guard with no duplicate mark;
- the long-time roof derivative of the marked record;
- capacity deficiency of the nongrazing comparison pool; or
- singular and boundary source outside the verified local charts.

These are not minor technicalities. The dominant clearance source is first order, while the new theorem is second order.

## 18. The decisive remaining mathematical obstruction

The paper still lacks a theorem which converts its local or weak clearance control into the complete positive roof-density estimate required by the organizing LLT.

A successful proof must control the complete physical sum before taking the roof essential supremum, uniformly in radius and exact labels, then take the collision limsup with all outer widths fixed, and only afterwards let the outer parameter tend to infinity.

The following remain open.

### 18.1 Complete clearance chart sum

The author must classify and sum finite-type charts, simple folds, higher degeneracies, zero-clearance-derivative charts, regular critical roofs, one-sided unvisited boundaries, section cuts, and pairing seams. Local constants and chart radii must be controlled in the complete `m^2 L^infty` topology. A separate shrinking neighborhood at every collision count is insufficient.

### 18.2 Single-mark and cross-flight clearance

The first-order single-mark source needs a target-roof summation or another normalized positive-source estimate. A natural extension would be a roofwise marked-pressure or clearance-load theorem for unvisited near misses across flights, with physical one-copy multiplicity and the original exact labels. The same-flight second factorial bound alone cannot supply this.

### 18.3 Critical and boundary budgets

The critical coefficient sum is unscaled, and the local error constants are not summed. The physical-side action extensions must be integrated with the actual pairing construction without treating bulk-null boundary sets as zero endpoint traces.

### 18.4 Low-incidence shallow source

Clearance progress does not pay the remaining incidence-only low-load source. An original-source scarcity estimate or valid capacity comparison remains necessary.

### 18.5 Capacity abundance

No theorem proves that the full nongrazing pool has sufficient roofwise capacity to dominate the remaining positive source. The local critical stability coefficient and the duplicate-mark mass do not imply such abundance.

### 18.6 Inherited global inputs

The family-uniform pressure theorem, stable optical comparison, complete pairing multiplicity, singular null-set passage, spectral/arithmetic inversion chain, and denominator consequences still require independent specialist reconstruction under their actual quantifiers.

## 19. Significance at the requested benchmark

The exact one-mark flux, integrated fold estimate, critical return-stability coefficient, and exact same-flight two-mark formula are interesting specialized results. They clarify genuine geometric mechanisms in finite-horizon dispersing billiards and could be useful in a focused specialist paper after independent verification.

They do not presently constitute a complete theorem of independent top-four breadth. The manuscript remains organized around a raw exact-label pointwise LLT and four-coordinate inversion which it explicitly does not prove. The new results are local or weak components of that program. The two-mark maximal transversality is confined to one flight and a specific triangular equal-disk radius range; the critical formula is a local coefficient; the fold theorem is conditional on chart constants; and the global conclusions still rely on a long inherited chain.

At a top-four benchmark, completing several correct interfaces while leaving the governing theorem equivalent to an unproved positive-shortage limit is not sufficient for acceptance.

## 20. Required revisions before another substantive top-four review

A further revision capable of changing the recommendation should contain at least one of the following, proved in the original order of limits.

1. **A complete normalized clearance theorem.** Prove the full exact-label one-copy chart sum, including folds, critical roofs, one-sided boundaries, and degenerate cases, with an `m^{-2}` roof-density bound on the central target.

2. **A target-roof clearance insertion theorem.** Establish a marked-pressure or exponential-moment theorem for unvisited clearance witnesses across physical flights, analogous in strength and topology to the incidence-load theorem, without assuming independence or multiplying by word count.

3. **A capacity-abundance theorem.** Show that the full nongrazing comparison pool pays the remaining source uniformly after the complete physical sum.

4. **A direct proof of the remaining shortage limit.** Any route is acceptable if it controls the original source, exact labels, and ordered limits without changing the theorem.

In addition, the author should obtain an independent billiards/transfer-operator audit of the inherited pressure, optical, pairing, and singular-interface chain before representing the complete result as journal-ready.

## 21. Presentation and source-record requests

These are secondary to the missing theorem, but should be addressed.

1. The next theorem-bearing author revision should have paired response/copy refs resolving to one SHA. Revision 115 currently exposes only one named author branch.
2. Current source manifests should distinguish preparation-time metadata from post-push facts. Fields such as `remote_commit: null` should not be presented as current after the commit exists.
3. The manuscript should keep revision-114 results and revision-115 results visibly separated. Modules 270–273, 274–275, and 276 have different provenance and different novelty status.
4. State the finite-horizon constant `tau_+` and, where feasible, the resulting finite lattice count `N_pair` in a readily auditable location.
5. Continue to distinguish ordered from unordered two-mark moments and mark counts from witness indicators.
6. Preserve the explicit warning that total variation is not roof essential height.
7. The equality `E_delta^- = I E_delta^+ = T_R E_delta^+` should retain an explicit set-image/preimage convention to avoid ambiguity.
8. The critical local density should continue to be described as a component restricted to a coordinate ball, not automatically as the entire global density near that roof.
9. Workflow completion should be recorded only after re-reading the exact-SHA run. Local PDF and finite diagnostics are not proof certification.

## 22. Final assessment

Revisions 114–115 make genuine progress on the precise clearance obstruction identified in the revision-112 report.

The strongest new achievements are:

- exact one-copy physical flux for unvisited near misses;
- grazing-uniform one-flight transverse geometry;
- an exact record-preserving clearance disintegration;
- the long-record clearance-to-roof Jacobian with the full Hessian chain rule;
- local finite-type and integrated-fold roof-density estimates;
- an exact reversing-periodic-orbit interpretation of regular critical roofs;
- the return-stability formula for the critical density coefficient;
- selector-uniform local critical coarea, including one-sided physical boundaries;
- an exact same-flight two-mark coarea formula;
- a uniform second-factorial clearance bound; and
- an `O(epsilon^2)` weak payment for duplicate same-flight marks.

I did not find a decisive algebraic or normalization error in those new statements within their expressly stated scopes.

However, the dominant first-order single-clearance source, cross-flight clearance, full chart summation, local critical remainder budgets, low-incidence shallow source, and capacity deficiency remain. None of the new estimates proves the collision-normalized roofwise shortage limit. The full raw pointwise LLT and four-coordinate inversion therefore remain unproved.

**Formal recommendation: reject in the present form at the requested top-four benchmark.**
