# Proof ledger — fourteenth revision

This file maps claims to proofs and precise hypotheses. It is not an independent correctness certificate. Printed theorem numbers and pages are generated from the final LaTeX auxiliary files in the build receipt.

| Stable label | Source | Hypotheses and assertion |
|---|---|---|
| `thm:v13-main` | Unchanged v13 `intrinsic-deficiency.tex` | Finite causal instruments, actual marked feedback tests, task/parameter-blind transducer. Attained private/fixed-selector spectra, priced hidden testing dual, visible zero-set distinction, optimized composition. |
| `prop:v13-rank` | Same unchanged source | Delayed finite channel; exact private budget is a stochastic nonnegative factorization. Identity-channel sharp error laws and rank-three hidden/private separation. |
| `thm:v14-local` | `local-certificates.tex` | Finite rational instruments; fixed finite widths, horizon and selector signature; full actual feedback tests. Product clipped-simplex cells, exact vertex minima for each separately affine test, rational lower/upper bounds, original-budget upper implementation, causal gap modulus, monotone dyadic convergence. Algebraic equality clause invokes classical real quantifier elimination. |
| `cor:v14-converse` | Same | Fixed private resource, finite model. Deficiency at most epsilon iff no finite local test-cover lower bound exceeds epsilon. Strict decisions have finite certificates; rational equality uses a distinct algebraic decision procedure. No polynomial-time or effective infinite-prefix assertion. |
| `thm:v14-stability` | Same | Two-way executable stateless bridges with actual marked feedback error, no extra seed and compatible interfaces. Intrinsic error changes by at most a+b; a finite rational certificate transfers to original nonfinite carriers without increasing widths. No nonfinite optimizer existence used. |
| `thm:v13-endogenous` | Unchanged v13 `endogenous-tasks.tex` | Finite controlled history tree, task-known controller/common task-blind encoder, actual reachable supports. Exact cover face, occupation regret, finite infeasibility margin and lossy upper comparison. |
| `thm:v13-average`, `thm:v13-cycle` | Unchanged v13 `regenerative-risks.tex` | Stationary finite-register policies; actual independent synchronous plant/register reset; fixed positive reset probability. Nonsummable average criterion, uniform mixing and compact risk images, geometric age-error transport. Not arbitrary nonstationary optimality. |
| `lem:v13-words`, `thm:v13-active` | Unchanged v13 `active-hard-spheres.tex` | True fixed-N hard-sphere flow, orthogonal velocity kicks, increasing finite graph-core spaces, noisy acquisitions, uniformly L2 preparations, fixed actual initial-mark channel. Controlled-product convergence and stateless marked comparison before width optimization. |
| `thm:v14-residual` | `residual-certificates.tex` | A fixed finite V contained in D(L), skew-adjoint L, unitary interventions, actual initial-mark/noisy-report setup. PSD graph/intervention residual factorization, word-error bound and root-sum-square feedback comparison. No need for interventions to preserve D(L). |
| `cor:v14-average-certificate` | Same | Regenerative setup above, finite age cutoff. Weighted finite-age errors plus exact geometric remainder; unchanged consumer resources. A vector presentation needs a separate finite-report bridge before the rational local algorithm applies. |

## Distinctions used in the proofs

The maximum of several separately affine tests is not generally separately affine. Only one fixed test is minimized over row vertices in the lower certificate; the upper witness evaluates the maximum at an actual vertex. The code checks that a monomial never repeats a row.

The visible selector changes the reference experiment as well as the simulated experiment. Its fixed signed-event oscillation therefore uses `2s+(1-s)b`; the hidden mixture uses `s+(1-s)b`. Both are handled without charging the number of unexecuted modes as repeated policy steps.

Dyadic upper monotonicity uses the fact that every coarse vertex remains a vertex of some finer cell containing it. Lower monotonicity uses the exact minimum of a fixed separately affine function on a product of row polytopes. Neither argument needs convexity of the global behavior image.

The physical residual is evaluated on the approximate suffix vectors and uses exact prefixes only through their norm-one property. It never differentiates a kicked vector outside the generator domain. The first-mismatch argument integrates against the original preparation, retains actual mark coupling and conditions on independent exposed seeds.

The residual estimate need not vanish for every graph-core sequence. A posteriori majorants and the inherited strong-convergence theorem are complementary claims. A floating-point finite matrix diagnostic is not a rigorous physical Gram enclosure.

## Retained analytic boundaries

No assertion is made of compactness for arbitrary nondominated strategic measures, average-cost optimality without the declared reset signature, polynomial-time private synthesis, a free convex private converse, or completion of the historical nonlinear kinetic/Sinai spectral targets. Full original-source priority comparison with Norberg and Paull–Unger remains unverified. These boundaries do not remove or alter their historical derivation files.
