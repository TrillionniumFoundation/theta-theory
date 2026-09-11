# Historical derivation audit — A2 v21

## Purpose

The v20 referee asked for theorem-level closure at four interfaces: non-dominated moving-support LAN, fixed spatial registration, quantitative exact-to-ideal statistical transfer, and the all-order signed/tangent inverse. This audit records which previously landed derivations support the v21 repairs and which steps are new.

## 1. The scalar statistical proof already contained the correct non-dominated mechanism

Historical source:

- `article/18_boundary_information_v18.tex`

The scalar theorem never needs a global likelihood ratio on the whole moving-support sample space. At finite information scale it shows that accumulated support-exclusive mass is `O(n p_n t_n^2)=o(1)`, expands the likelihood only on a high-probability common-support event, and treats the alternative singular part separately in the total-variation identity. It also proves the logarithmic Hellinger coefficient.

V21 lifts this logic to the vector experiment by a cleaner experiment-theoretic device: a parameter-independent reference-collar collapse. The new vector construction is therefore not a change of asymptotic scale; it is the rigorous vector realization of the support treatment already visible in the scalar proof.

## 2. The collar moment calculations from v20 remain valid

Historical source:

- `article/18a_vector_boundary_information_v20.tex`

The v20 vector source correctly computed the matrix logarithmic covariance, third/fourth score moments, collar mass and truncated-score centering. The defect identified by the referee was the global Radon–Nikodym notation for the original non-dominated family, not these coarea calculations.

V21 preserves the moment calculations and changes the experiment architecture around them. The likelihood expansion is now performed only after the collar-collapse map has produced a dominated family.

## 3. Fixed raw physical times existed before the statistical v20/v21 formulation

Historical source:

- `v6/10_experiment_transfer.tex`

The finite/boundary comparison is formulated on a common physical record space and permits predetermined physical times. Parameter-dependent excess

`d_i(xi)=t_i-j_i g_e(xi)`

is an internal proof variable, not an acquisition instruction. This is the historical basis for keeping `t_{j,l}=j g_0+d_l` fixed while allowing the local gap to vary.

## 4. The gap scale was already encoded by charged onset calibration

Historical source:

- `v5/50_self_calibration.tex`

The selected-channel success probability at programmed times depends on the onset displacement through `tau=j(g-g_0)`, and the historical self-calibration theorem gives a gap error of order `h^{m+1}/j` with explicit preparation cost. This is the derivational reason that the physical gap coordinate in a fixed laboratory time window has the local scale

`g-g_0 = delta_n a/j_n`.

V20 introduced that scale into the statistical experiment. V21 retains it unchanged.

## 5. The fixed spatial chart is compatible with the original local action construction

Historical sources:

- `v3/10_geometry_action.tex`
- `article/01c_geometric_setup_v18.tex`

The local flight action is written after choosing one Euclidean frame around a reference channel, with facing graphs

`(-psi_0(u),u)` and `(g+psi_1(v),v)`.

The general forward theorem later adopts a channel-centered derivative convention for convenience when differentiating the relative law. The v20 referee correctly noted that this convention cannot by itself serve as the common statistical observation map for generic moving contacts.

V21 therefore makes a distinct anchored registered subfamily explicit at theorem level: all local tables in the statistical family are represented in the same Euclidean chart with the same contact origins and tangent axes. This is not a new billiard coordinate construction; it is a precise model slice through the already used local graph representation. The more general deterministic forward theorem remains unchanged.

## 6. The signed all-order proof is assembled from already proved analytic machinery

Historical sources:

- `v3/10_geometry_action.tex` — alternating Jacobi recurrence, finite weighted Green estimates, differentiated fixed-point equations;
- `v4/10_boundary_layers.tex` — half-line Green kernel, unique stationary half-line solution, weighted derivative bounds;
- `article/23_two_contact_rigidity.tex` — highest-new-jet envelope calculation and triangular inverse in the historical even two-contact setting;
- `article/23a_signed_endpoint_rigidity_v19.tex` — signed support recovers the unsymmetrized actions and records the arbitrary-degree determinant-one block.

The referee's concern was not absence of all ingredients but that the arbitrary odd/even signed theorem promoted in v19/v20 compressed them too strongly. V21 writes the weighted half-line equation and the all-order induction explicitly, derives the stationary envelope identity by finite truncation, proves the first-appearance/no-contamination statement, evaluates the geometric sums, and derives the tangent inverse.

No historical inverse result is deleted. The older even theorem remains useful as an independent benchmark and derivational precursor.

## 7. The tangent information-kernel step is genuinely new in v21

V20 used the nonlinear signed inverse to conclude that a tangent vector with vanishing action derivative was zero. The referee correctly distinguished nonlinear injectivity from derivative injectivity.

The v21 proposition `Differential signed-jet inverse` is new. It differentiates:

1. the leading map `(a_0,a_1) -> (kappa_0,kappa_1)` at fixed gap;
2. the determinant-one degree-`n` recursion after lower tangent components have vanished.

This gives a bounded left inverse on every fixed compact finite-jet set. The finite-design information proof now cites this proposition directly.

## 8. The quantitative statistical transfer uses the historical Hellinger scale

Historical source:

- `article/18_boundary_information_v18.tex`

A normal support displacement `epsilon` produces squared Hellinger size of order

`epsilon^2 log(1/epsilon)`.

V21 generalizes this to a uniform support-remainder lemma with an additional regular amplitude term. The exact fixed-window billiard boundary law provides `r_n=o(delta_n)` in the defining function and `O(delta_n)` in the amplitude, so at

`k_n delta_n^2 log(1/delta_n) -> 1`

the exact and ideal product endpoint experiments are asymptotically equivalent. This closes an interface that v20 only described verbally.

## 9. Complete stopped transfer already charges failures

Historical sources:

- `article/17_adaptive_experiments.tex`
- `v6/10_experiment_transfer.tex`

The stopped transcript retains the designs, every success/failure result and stopping times. With a deterministic cap and at most `k_n` retained successes, the relative-law coupling gives the uniform bound `C k_n tau^{j_n}`. V21 keeps this theorem and sharpens only the terminology around what inherits the Gaussian endpoint information bound.

## 10. Pilot calibration and experiment sigma-fields

Historical source:

- `v5/50_self_calibration.tex`

The pilot estimator and its cost are reused. V21's new step is to say exactly what is observed in the pilot-centered comparison: the same pilot transcript is retained in both experiments and only the conditional post-pilot endpoint kernel is changed from data-centered to oracle-centered. The Hellinger bound is integrated over that common pilot transcript.

## 11. What is genuinely new in v21

1. Parameter-independent collar collapse and Le Cam equivalence for the original non-dominated vector local experiment.
2. A dominated compact-uniform LAN companion experiment, with contiguity and local-risk transfer back to the original family.
3. A general Hellinger stability lemma for small support/amplitude remainders.
4. A theorem-level anchored registered physical family in one fixed laboratory chart.
5. An exact-to-ideal endpoint experiment-distance proposition at the billiard critical scale.
6. A standalone arbitrary odd/even signed all-order proof in the weighted half-line space.
7. A differential signed-jet inverse with quantitative compact finite-order bounds.
8. A finite-design proof based on that tangent inverse.
9. Explicit endpoint-output versus complete-transcript terminology.
10. An explicit pilot comparison sigma-field and a canonical v21 source/build pointer.

## 12. Preservation

The v18, v19 and v20 sources are retained. V21 changes the active theorem hierarchy by adding strengthened source modules and selecting them in `main.tex`; it does not erase the historical derivation path.
