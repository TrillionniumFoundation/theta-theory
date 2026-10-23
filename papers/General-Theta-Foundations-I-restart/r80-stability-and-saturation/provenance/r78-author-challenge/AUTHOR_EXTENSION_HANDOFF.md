# R78 author mathematics handoff

## Delivered mathematical sources

- `53-reset-memory-frontier.tex`: a complete new section with five numbered results and their proofs.
- `R78_DECLARED_STATEMENTS.json`: theorem-map declarations in the inherited schema, including hypotheses, dependencies, internal load-bearing facts, priority keys and limits.

These files are authored against the complete R77 mathematical source. They do not replace, edit or reinterpret an independent referee report. The parent selects the verified source baseline and integrates this section into the new complete source.

## Central advance

The previous R77 reset result gives the exact label count attaining the unrestricted optimum under positive failure exposure, and an attained first-residual certificate below that count. The present addition determines the entire cost frontier at every fixed memory for the full finite reported-reset class, including merely positive semidefinite effects and reports unexposed by a least-favorable state.

The proof does not simply assert that a general stochastic finite-state controller can be optimized as a fully observed process. It fixes the existing command rows of a given controller. Because every observed failure resets the physical system to a supplied state, the row-selection continuation has a finite Bellman equation. Crucially, the robustness quantifier permits the original controller to start with label 1 at each reset density matrix, proving that this row-selection problem is proper and bounded at every state. The replacement controller writes one existing row label after each report, so it needs no additional memory. This yields pointwise initial-state dominance, and then the compact exact finite-memory certificate.

The arbitrary-memory formula is constructive and attained. Its state vector is bounded by a concrete full-support one-label controller, not by an assumed optimal-trajectory estimate. Algebraic feasibility is used only after the original infinite-duration control problem has been proved equivalent to the finite certificate. No numerical optimization or external elimination theorem supplies a missing probabilistic argument.

For the physically realized R77 action-cover family, the finite certificate can be solved further. Every continuing row has a pure optimizer, while the initial row has an optimizer uniform on a subset. A finite formula in the cover incidence table gives every intermediate memory value, not just the optimum threshold. Singleton covers produce any desired number of successive strict memory improvements with fixed success probability and bounded primitive costs. The inherited first-residual lower certificate is exactly half the full excess cost for that displayed family; this quantifies its previously acknowledged limitation without invalidating it.

## Delicate points and their resolutions

1. **Inaccessible reports.** A least-favorable preparation may avoid a reset state, so the R77 cover converse cannot be exported to all semidefinite effects. The new theorem instead uses the all-initial-state guarantee at each reset density, with the original initial label, to bound the Bellman continuation. It does not infer mandatory exposure or attach a false cover constraint.

2. **Comparison restarts.** Restarting the old controller from a reset density is a proof comparison, not a free operation executed by the new device. The actual new device always begins at its one prescribed initial label, then uses a deterministic table to update an existing label after each report.

3. **Properness.** A finite supersolution, a strictly positive conditional mean cost floor, and nonnegative costs bound expected duration and remove the survival remainder. No uniform positive success probability is assumed in the general theorem, and no unsupported global spectral-radius premise is added. The matrix of an attaining deterministic reset selector is proved transient from every reset state before its resolvent is used in the continuity argument.

4. **Mixed rows.** Only report updates become deterministic in the general theorem. Continuing command rows are purified only for the action-independent-transition construction, using separate concavity at a global optimum. The initial row is not subjected to that purification. Uniform-on-subset initial rows are proved to exist by a capped-simplex endpoint argument; ties may allow other initial optimizers.

5. **Compactness.** The explicit full-support one-label cost supplies the common cap. Every relevant controller of robust cost at most that cap has its row-choice Bellman vector below it. The original memory class is not silently convexified. Finite selector enumeration plus compact row and supersolution coordinates gives actual attainment and a strict gap at every insufficient memory.

6. **Stability.** Near a fixed primitive instance, the same full-support row remains transient, providing local uniform caps. An attaining controller gives upper semicontinuity by its transient resolvent. Limit supersolutions give lower semicontinuity. A limit vector need not lie below one particular newly chosen cap to produce an actual proper-controller certificate.

7. **First-residual gap.** For arbitrary cover systems, the full objective and the first-residual certificate use different coefficients inside an optimization, so their minima are not generally proportional. The explicit factor two is proved only for the singleton family at failure probability one half.

8. **Noncommuting physical realization.** Modifying only `E_(1,1)` by `epsilon (|e_1><f_1|+|f_1><e_1|)` leaves reset transition matrices unchanged and has a nonzero commutator with the mean cost operator. The primitive mean costs remain between `I` and `4I`. It would be unsafe to claim that the same realized cost support `[1,4]` remains jointly implementable with this effect. The proof instead explicitly splits success into effects `(G-I)/8` and `B-(G-I)/8`, with realized costs nine and one, and charges one on failures. This is a positive joint cost/report instrument with exactly the desired mean, and the cost outcome is not supplied as an additional controller observation.

9. **Perturbed hierarchy.** For the explicit perturbation every row-list continuation remains at most four. Its initial cost operator changes by norm at most `4 epsilon`, so every optimized value changes by at most that amount. Consecutive gaps remain positive for `epsilon < (n-1)/(8n^2)`. The exact closed formula and the exact `2 D_M` relation apply to the unperturbed instance only. The initial success probability of the perturbed model need not remain exactly one half, although subsequent reset-state calls retain that probability.

## Relation to historical open issues

This addition substantively closes the R77 statement that its reset certificate was not the full memory-constrained cost frontier: a complete exact variational frontier now exists for every finite reported-reset instrument in the stated general class. The positive-exposure cover formula remains an inherited simpler special-case invariant. The broader semidefinite case has an exact finite feasibility characterization rather than a newly claimed combinatorial cover formula.

The arbitrary-length strict hierarchy supplies matching attained upper and lower values at every intermediate memory in a growing finite-dimensional family, and its strict ordering survives valid perturbations including noncommuting effects. These are genuine further structural and quantitative results. They do not close the original general-M squared-sign risk curve, arbitrary nonreset partially observed feedback, phase-type timing, general quantum discrimination resource frontiers, or A1/A2/other independent Theta objectives.

## Evidence status

The proofs are written author arguments, not formal proofs or independent human assessments. Another author-team AI agent independently checked the central formulas and is preparing diagnostics and primary-source priority notes. No claim of an executed numerical, algebraic-elimination, native-build or hosted-CI pass is made by this handoff itself. Such claims require the parent revision's actual source-bound receipts.

The classical inputs are finite stochastic-shortest-path dynamic programming, fixed-size stochastic-controller optimization, compact optimization, spectral bounds, simplex allocation and real-algebraic decision. The proposed contribution is the exact counted-memory normal form, full compact frontier and realized all-memory hierarchies inside the stated reset experiment. A literature search does not constitute comprehensive priority clearance or external expert approval.
