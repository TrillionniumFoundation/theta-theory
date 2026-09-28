# Historical derivation audit — A2 v20

## Question addressed

The v19 referee accepted the new signed deterministic inverse but identified a mismatch between the abstract centered moving-support model and the advertised unknown-billiard physical experiment. This audit records which previously landed derivations support the v20 repair and which new steps are genuinely added.

## 1. Raw physical coordinates were already present before v19

The crucial historical source is:

- `v6/10_experiment_transfer.tex`

It defines finite and boundary laws on a common physical record space with a failure atom and proves one-record and product total-variation bounds. Its final paragraphs explicitly allow predetermined physical times `t_i`, with parameter-dependent excess used only inside the proof:

`d_i(xi)=t_i-j_i g_e(xi)`.

Thus the historical relative-law machinery never required an experimentalist to know the true gap in order to compare physical and boundary experiments. V19 failed to propagate this common-window formulation into the new geometry-as-parameter LAN theorem; v20 does.

## 2. Stopped/adaptive transfer already retained failures and stopping times

The second key source is:

- `article/17_adaptive_experiments.tex`

Its stopped transcript contains every design, success/failure record and stopping time. The theorem gives

`||P_xi^pi-Q_xi^pi||_TV <= C E sum Y_i tau^{j(a_i)}`.

For a deterministically capped policy stopping no later than the `k`th success, this is at most `C k tau^J`. V20 now inserts the local alternatives and fixed physical windows into this theorem and uses deterministic caps so that its bounded-stopping hypothesis is satisfied literally.

This is the proof source for the new experiment-level finite-bridge transfer. No new coupling principle is invented in v20; the new work is the correct statistical specialization.

## 3. The gap direction was already known to be an onset/timing direction

Historical calibration source:

- `v5/50_self_calibration.tex`

For a coarse bracket it writes the selected-channel probability at programmed times as

`p_l = K_j (l h - tau)^2 F_j(l h-tau)`, `tau=j(g-g_0)`.

The stable zero-extrapolation lemma and the self-calibration theorem give

`|g_hat-g| <= C h^{m+1}/j`

with fully charged preparation cost.

This historical formula shows directly why the physically relevant gap perturbation is amplified by `j` in a fixed laboratory time window. V20 turns this observation into a local statistical scaling:

`g=g_0+delta a/j`.

Then the fixed-window excess is `d-delta a`, so the gap produces an order-`delta` normal support displacement. This is the new conceptual step that closes the v19 missing-gap information direction without assuming the onset is known.

## 4. Signed rigidity supplies the shape injectivity after the gap is separated

Sources:

- `v3/10_geometry_action.tex`: signed endpoint variables and arbitrary odd/even graph jets are already present in the basic stationary action.
- `article/23_two_contact_rigidity.tex`: historical highest-jet envelope calculation and triangular recovery mechanism.
- `article/23a_signed_endpoint_rigidity_v19.tex`: support recovers the unsymmetrized actions and the highest new arbitrary-degree jet block has determinant one.

The v20 information-kernel argument uses these sources exactly as follows:

1. a null vector for every raw fixed-window information matrix satisfies
   `a + D_h S_b(u)+D_h S_b(v)=0` on every small same-type support level;
2. the `v=0`, `u->0` limit gives `a=0`;
3. therefore `D_h S_b=0` for both labels;
4. at fixed `g`, the signed-rigidity leading formulas and determinant-one recursion give `h=0` on the finite labelled contact-jet model.

Thus v20 does not reuse the v19 incomplete phrase "on the graph-jet parameter space" to conclude full positive definiteness. The gap direction is killed first by the raw timing term.

## 5. Scalar boundary information already contains the calibration stability scale

Source:

- `article/18_boundary_information_v18.tex`

A normal support displacement `epsilon` has squared Hellinger size

`O(epsilon^2 log(1/epsilon))`.

Combining this with the historical self-calibration error gives the v20 pilot condition

`k r_n^{2m+2} log(1/r_n) -> 0`.

Under that condition the data-driven windows `j g_hat+d_l` and the oracle centered windows `j g+d_l` have vanishing product Hellinger distance. This supplies the missing quantitative propagation of the pilot through the local experiment.

## 6. Why deterministic caps were added

The historical adaptive theorem is stated for policies with a deterministic preparation cap. A literal "stop at the kth success" rule is unbounded. V20 therefore uses a cap `N_{n,l}` chosen from a compact-neighborhood lower bound on the success probability, with

`N_{n,l} p_{n,l} >= 2 k_{n,l}`.

Binomial Chernoff gives exponentially small probability that the cap prevents the target success count. This closes a technical bounded-stopping point rather than relying on an unprinted limiting argument.

## 7. Why `j_n delta_n -> 0` is printed

The conditional endpoint boundary singularity itself needs only

`k_n delta_n^2 log(1/delta_n) -> 1`.

However the raw selected-event probability also contains a long-bridge factor depending on the geometry, asymptotically `e^{-j gamma}`. A shape perturbation of size `delta_n` changes its exponent by order `j_n delta_n`. V20 therefore prints the auxiliary regime

`j_n delta_n -> 0`

when comparing physical preparation costs uniformly with the reference table. This is compatible with `k_n tau^{j_n}->0`; choosing `j_n` logarithmic in `k_n` is sufficient.

The endpoint-output LAN deliberately coarsens away waiting-count information. The manuscript now says explicitly that the richer waiting transcript can carry faster information in directions changing `gamma`.

## 8. Vector LAN proof audit

The v19 vector theorem polarized the scalar calculation correctly but compressed several theorem-level steps. V20 keeps the same mechanism and makes the dependencies explicit:

- coarea/tubular coordinates give the matrix logarithmic covariance;
- the third and fourth score moments are `O(q^{-1})` and `O(q^{-2})`;
- the omitted collar has probability `O(q^2)`;
- truncated-score centering is `O(q)`;
- `q_n=delta_n log(1/delta_n)^{1/4}` gives Lindeberg, vanishing likelihood remainder and concentration of the quadratic term;
- support-exclusive accumulated mass is `o(1)` at the logarithmic rate;
- local asymptotic minimax is stated first for truncated quadratic loss, then passed to quadratic loss with uniform integrability.

No new external theorem is used to replace these calculations.

## 9. What is new in v20 versus reused

### Reused and strengthened in presentation

- nonlinear relative boundary law;
- scalar transport/determinant identification;
- signed endpoint rigidity and determinant-one jet block;
- scalar boundary Hellinger coefficient;
- adaptive/stopped physical transfer;
- charged gap self-calibration.

### New v20 deductions

1. fixed-reference physical windows combined with `g-g_0=delta/j` give a common raw local experiment including the gap;
2. the full gap-plus-contact support velocity has a trivial common information kernel;
3. compactness produces a finite positive-offset physical information design on the full local coordinate `(gap, finite labelled contact jets)`;
4. deterministic caps turn the existing stopped transfer into a literal bounded-policy local-experiment theorem;
5. the charged self-calibration theorem plus the Hellinger expansion yields a quantitative pilot-to-centered Le Cam equivalence.

## 10. Preservation

No historical mathematical source is deleted. V19 sources remain in Git history and the v19 vector source remains in the tree; `main.tex` selects the v20 replacement. The auxiliary compendium continues to retain earlier acquisition, inverse, minimax and benchmark modules. The v20 revision changes the active theorem hierarchy rather than erasing the development record.
