# Response to the independent referee report on A2 geometric thresholds v2

**Revised manuscript:** *Uniform collision thresholds and endpoint curvature recovery in periodic dispersing billiards*, A2 v3.  
**Author:** Qian Qi.  
**Controlling report:** `reviews/a2-geometric-thresholds-v2-harsh-independent-2026-09-09/REFEREE_REPORT.md`, commit `fbe11e631e2e8f19eacff804cebbc5496d1fb822`, report blob `1253acf953e8721bf1b9f5e3a8538d42a30271df`.  
**Reviewed manuscript:** `daeea828a7666acc42adcabdb9ab9057e9e1bac7`.  
**New revision branch:** `revision/a2-geometric-thresholds-v3-observability-2026-09-09`.

The report distinguishes a significance objection from a disproved theorem. The revision therefore does not replace the valid threshold law by a weaker claim. It proves a geometric criterion which removes the near-circle restriction, and a quantitative inverse theorem for explicitly specified physical endpoint records. The scalar count data and the additional record data are kept separate. The inverse theorem is accompanied by actual periodic obstacles on which every leading count amplitude stays fixed but the endpoint records vary.

## GTC-R1 — The organizing result and the geometric class

**Locations:** Theorems 1.1–1.2, pp. 2–3; Lemma 2.1, pp. 4–5; Lemmas 3.1–3.2, pp. 5–7; Section 5, pp. 10–13. Sources: `v3/00_results.tex`, `v3/10_geometry_action.tex`, `v3/30_observability.tex`.

Theorem 1.1 now applies locally about **any** periodic configuration of a positive finite number of smooth strictly convex obstacles with positive curvature and disjoint lifted closures, on any fixed full-rank planar lattice. The obstacles need not be congruent, centrally symmetric or close to a circle. Finite horizon is not assumed. Uniformity is on compact smooth parameter families in a neighborhood of such a reference configuration, with constants depending on positive separation, curvature and the required higher smooth norms. No uniformity up to zero separation or vanishing curvature is claimed.

Lemma 2.1 verifies the criterion from the configuration itself. Only finitely many lifted pairs can have a bounded distance. Strong convexity gives a unique closest segment and a positive distance Hessian for each reference minimum. Global minimality gives clearance from every third obstacle. The gap to nonminimal pairs and the separation of the finitely many normal outgoing states force every sufficiently short flight to reverse the preceding channel. Since a small total excess bounds each flight's excess, the same collar works at every collision order. This is a proof of the criterion, not a hypothesis that the complete event is already localized. Finite local coverings extend the constants to compact families without choosing a nonsmooth minimum as a differentiation coordinate.

Lemma 3.2 is the reusable parameter-dependent Dirichlet and relative-flux result. Its full proof contains the scaled Green kernel, the weighted contraction, a derivative induction in the same weighted spaces, and the trace-norm estimate for the relative determinant. The endpoint Hessian is uniformly positive while the physical twist is exponentially small; the latter is estimated multiplicatively. The stationary flow normalization and radial integral are then performed for this general configuration in Section 4. The old noncircular six-channel formula and its competition mechanism are specializations, not removed results.

The second principal result identifies the information retained before the scalar flux-to-volume ratio is taken. Theorem 1.2 shows that two centered Euclidean endpoint variances recover both contact curvatures, with a Lipschitz constant independent of every odd flight number and without a curvature-separation assumption. Theorem 5.3 realizes the scalar ambiguity by actual analytic periodic tables. This is the consequence on which the revised importance argument rests; source summability, interface jumps and smooth-test differentiation are presented as consequences of the common construction, not as several independent conceptual advances.

## GTC-R2 — Area dependence in the equal-gap family

**Location:** Proposition 6.3 and proof, pp. 15–16; `v3/40_inverse.tex`.

The report's area computation is incorporated with a complete Fourier calculation:

\[
|D|=\pi\left[R^2+2R\alpha-\frac{33}{2}\alpha^2
-\frac{45}{4}(\beta^2+\zeta^2)\right].
\]

Putting \(b_r=(\kappa_r^{-1}-R)/36\), the proof gives

\[
\alpha=\frac13\sum_r b_r,\qquad
\beta^2+\zeta^2=\frac23\sum_r(b_r-\alpha)^2.
\]

Thus the free area is a symmetric function of the recovered curvature triple and the observed gap. The introduction and comparison now state explicitly that it is **not a fourth independent inverse invariant** in this selected three-parameter family. The exact theorem, its multiplicity treatment, its Möbius transform and its elimination of an initially unsupplied normalizer remain intact. The new two-variance theorem does not need the free area at all: it cancels in the actual conditional law.

## GTC-R3 — Coalescence and a quantitative physical inverse

**Locations:** Proposition 6.3, pp. 15–16; Theorem 1.2 and its proof, pp. 10–11; Proposition 5.2, pp. 11–12.

The circular first-order loss of sensitivity is proved in the manuscript, not merely described as a generic caveat. Along \(\alpha=\zeta=0,\beta=s\), the contact radii are \((R+36s,R-18s,R-18s)\), and \(A(s)=A(0)+45\pi s^2/4\). Differentiating the exact amplitude gives \(C_j'(0)=0\). Therefore each fixed finite amplitude vector changes by \(O_J(s^2)\), whereas its curvature multiset changes by order \(|s|\). This is compatible with the retained exact infinite-data identifiability theorem.

The quantitative inverse uses a different, explicitly defined observation. In a selected oriented channel, let \(Q_0,Q_j\) be the first and last physical collision positions, lifted to fixed contact patches. Set

\[
V_{j,b}(d)=d^{-1}\{\mathbb E|Q_b|^2-|\mathbb E Q_b|^2\}.
\]

The conditioning event and expectations are those of the full-phase experiment. Neither the unknown contact point nor the unknown tangent is used in this statistic. Proposition 5.1 proves

\[
\operatorname{Cov}(u,v)/d=\mathsf H_{j,e}^{-1}/3+O(d)
\]

with a smooth, fixed-order differentiated remainder uniform in \(j\), and proves that centered Euclidean variances have the corresponding leading diagonal entries. The proof integrates the actual endpoint density; odd terms cancel on the symmetric radial domain, so nonsymmetric cubic boundary jets do not degrade the variance bias to order \(\sqrt d\).

For odd \(j\), the limiting variances satisfy

\[
(v_0,v_1)=\frac{g\coth(j\gamma)}{3\sinh\gamma}
\left(\sqrt{c_1/c_0},\sqrt{c_0/c_1}\right).
\]

Their geometric mean determines \(\gamma\), because \(F_j(\gamma)=\coth(j\gamma)/\sinh\gamma\) is strictly decreasing. The proof bounds \(-F_j'\) above and away from zero uniformly in odd \(j\) on compact positive geometric boxes. The ratio determines \(c_0/c_1\). This gives a two-sided Lipschitz comparison for \((g,\kappa_0,\kappa_1)\leftrightarrow(g,v_0,v_1)\), including equal curvatures. It does not invert an exponentially small off-diagonal covariance.

For normalized variance errors at most \(\delta\), the reconstruction error is at most \(C(d+\delta)\). Proposition 5.2 gives an empirical estimator using pairs of independent successful preparations and proves an error of order

\[
d+\sqrt{\log(4/\eta)/K}
\]

with probability at least \(1-\eta\). It also charges the expected number of unconditioned preparations, of order \(K d^{-2}e^{j\gamma}\), for \(2K\) successes. No independence of successive impacts in one billiard orbit is assumed. The window offset is known; a location error is not silently treated as a free timing adjustment.

We do not claim a Lipschitz noisy inverse for the original unlabelled amplitude vector at coalescence. The positive stability theorem explains which additional, measurable record statistics resolve the loss and proves their accuracy and acquisition cost.

## GTC-R4 — The product ambiguity is realized and resolved

**Location:** Theorem 5.3 and proof, pp. 12–13; experiment definition, pp. 1–2; comparison in Section 8.

The report identified an algebraic fiber at fixed gap and area. Theorem 5.3 constructs it in actual periodic billiards. On the lattice \(3\mathbb Z\times4\mathbb Z\), use a real-analytic support family through the unit disk, with

\[
g(s)=1,\quad A(s)=12-\pi,\quad c_0(s)=2e^s,\quad c_1(s)=2e^{-s}.
\]

The proof gives explicit trigonometric functions with prescribed zero, first and second contact jets. A third function has zero second jets at both contacts and a nonzero area derivative. An analytic implicit-function correction holds the area exactly fixed. Positive curvature, disjointness, clearance and the strict gap to all nonhorizontal pairs persist. The only two oriented ground channels are horizontal. Consequently every leading full maximal-count coefficient is exactly

\[
\frac{1}{(12-\pi)\sinh(j\operatorname{arcosh}2)},
\]

independent of \(s\), and all threshold locations agree. The ordered endpoint curvatures nevertheless vary. At each odd \(j\), their conditional variance ratio is \(v_1/v_0=e^{2s}\), separating this realized fiber with the uniform inverse bounds. Equality is claimed for leading coefficients, not for all finite-offset remainders, marked length spectra or all other billiard observables.

The selected-channel inverse is valid throughout the general nonsymmetric class. The unlabelled curvature-triple theorem is still stated only on its equal-gap centrally symmetric family. The introduction places these restrictions next to the respective claims. For a nonminimal channel, its own onset window and its physically observed itinerary selection are required; ground-onset counts alone eventually suppress a fixed gap difference when \(j\Delta\ge\varepsilon_0\). The new theorem does not invent unobserved labels or merge these experiments.

## GTC-R5 — Attribution, architecture and notation

**Location:** Section 8, bibliography, and the reorganized main entrypoint.

The full Prony recovery proof remains in Section 6, with Batenkov–Yomdin now cited for finite-exponential-sum reconstruction and local conditioning. The comparison identifies their regular-point result and its dependence on node separation; it does not attribute the billiard amplitude or the odd-index transform to that reference.

The inverse-billiard comparison now includes Finamore–Leguil's pinned October 2025 preprint, Theorem A. Its finite-horizon global isometry conclusion uses enriched marked lengths, including data arising from geodesic approximations. Our local curvature observation and its conditional sampling cost are not equated to that datum. The open three-obstacle results of Bálint–De Simoi–Kaloshin–Leguil and the periodic rare-event comparison remain. Hill-type determinant identities and the quadratic-sublevel covariance calculation are identified as classical or elementary mechanisms; the manuscript's work lies in their uniformly controlled physical realization and the resulting separation of geometric observables.

The active article now proves the general geometric criterion, weighted boundary-value lemma and relative determinant **before** its integration and inverse consequences. The circular hierarchy and its explicit calculations occupy Appendices A–G. The repeated circular contraction and determinant arguments invoke the already proved even analytic specialization, retaining the explicit Green, Hessian, cofactor and logarithmic determinant formulas and all old labels. The original full circular proof sources remain in `sections/`, and all old geometric sources remain in `v2/`. No archival proof has been erased.

Scalar remainders in the main theorem are denoted by \(\mathcal R\); endpoint Hessians by \(\mathsf H\). The fixed parameter-chart multi-index conventions and matrix norms are stated once in Section 1; growing record arrays retain their explicit maximum norm in Section 7. The original smooth-test and moving-cut response proofs remain, with their topology and transversality margins.

## Historical preservation and executed validation

The new Git subtree is based on the entire reviewed native subtree `517298b550ee2a10b05508c2c32f3e1b6bbd9315`. The complete controlling report is retained by its exact Git object in `review-basis-v2/`. The old entrypoint and publication metadata are saved under `history/v2-publication/`; original `v2/`, `sections/`, earlier reports and historical source trees remain. In the active source closures, every one of the 118 inherited labels remains defined. All 29 inherited theorem-like results remain, either verbatim or explicitly generalized; there are five added results. The seven-page two-collision companion is byte-identical as TeX, and all its PDF page texts agree with the supplied v2 companion. The source map and proof-integration ledger distinguish preservation from a claim of a fresh full audit of every historical derivation.

The Round 33 arithmetic and Fourier compiler was read. Its arithmetic result and conditional integration theorem are preserved, not replaced by the current onset argument. The present manuscript does not infer model-level transfer-operator bounds or unrestricted long-window expansions from a series of different onset windows. Those historical statements retain their own explicit premises.

A current complete native build produced a **31-page main article and 7-page companion**. Six compiler invocations succeeded; the auxiliary files stabilized after three paired cycles; recorder inputs match the declared source closure; final logs have no unresolved references or citations, multiply defined or changing labels, or overfull boxes. The build is identified by exact source hashes and precedes creation of its publication commit; the null pre-publication commit field is intentional.

The new diagnostic program passed 257 explicit finite checks: 90 exact-rational metric checks, 27 exact-symbolic checks, 60 numerical inverse/Jacobian checks, 50 numerical fiber checks and 30 numerical endpoint-quadrature checks. Ordinary and optimized execution produced identical JSON. The inherited 328-check geometry program and 411-check threshold program were also rerun in both modes with identical outputs. Local nonlinear quadratures include unequal curvatures and nonsymmetric cubic jets; physical variances approach their predicted limits with the displayed order-d bias. These are non-interval diagnostics, not continuum or formal proof certificates, and not a simulation of the complete equilibrium billiard. The referee's separate 241-check program is not claimed as replayed.

Final layout inspection uses all-page thumbnail sheets for page balance and enlarged samples of the principal theorem, conditional inverse, realized fiber and other representative pages; a Poppler render separately checks the inverse-proof page. The visual record identifies the inspected samples. Current source identities, build logs, results and limitations accompany the revision. The mathematical arguments, rather than the number of pages or tests, are submitted for the next independent assessment.
