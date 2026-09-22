# Response to the v5 intrinsic referee report — sixth revision

**Manuscript:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction. **Author:** Qian Qi. **Date:** 22 September 2026.

The controlling report is `reviews/general-theta-foundations-i-v5-intrinsic-2026-09-22/REFEREE_REPORT.md` at `ee210f3cfe3b4923ef51310e20cd8b20a6a367e1` (blob `2fee1ac088b7452eb87423cf36d9dca9b55e138b`). It reviewed the fifth intrinsic snapshot `1fe6b459213ab86e5e49872490a1ec05eb0e0741`. This reply uses the report's current E1–E7 and Sections 12–15, not an earlier round's numbering.

We thank the referee for identifying the precise remaining structural questions. The sixth revision adds complete proofs, rather than arguing that the fifth revision's hypotheses were already sufficiently broad. The title, earlier mathematical bodies and dual-reading architecture are retained.

## Principal changes

The Markov-renewal theorem proves a matched finite profile on primitive subshifts with forbidden transitions, higher-dimensional bounded-distortion realizations, finite-delay observable Hölder readouts and nongeometric renewal times. A new strict renewal-energy inequality replaces the strict cylinder-mass inequality that fails at unique predecessors. All unary vertices are charged. The pressure theorem is proved on the admissible language; zeros in transfer matrices remain zero.

The critical theorem classifies power-log, iterated-log and bounded corrections for polynomially modified geometric tails on arbitrary primitive Parry graphs. It also proves uniform finite-size profile limits. A separate posterior-contraction theorem gives matched hard-register risk on an unbounded, continuously observed process without any global common-refresh law. The Gaussian example verifies this absence for every fixed-step hidden kernel. Operational simulations compare finite-event, split-register and binary-checkpoint conventions.

The complete edition adds an application to the **actual A2-v118 known-mark count-to-contact protocol**, with an explicit joint sample/label deficiency bound and a smaller sufficient overflow alphabet than a polynomial truncation radius requires. The statistical argument is given in full; the new conductor and nilpotent-scheme theorems are not misused as noise models.

## E1 — full shift, dimension, observable and geometric clock

**Mathematical response:** `thm:v6-profile`, `thm:v6-pressure`, `lem:v6-suffix-energy` and `lem:v6-realization`.

The alphabet has a primitive zero–one adjacency matrix with Perron root greater than one. Forbidden transitions and vertices with a single successor are allowed. The geometric hypotheses include similarities in every Euclidean dimension; general bounded conformal distortion is explicitly a metric assumption, not an unproved consequence of pointwise differentiability.

For an observable f, the current value may fail to identify the state. A finite delay vector must give a quantitative snowflake lower bound. The planar golden-mean example `ex:v6-delay` verifies this condition for a noninjective scalar observable. A completely constant observable would have zero risk and cannot satisfy the geometric lower bound; the theorem does not conceal observability inside a notation change.

The acquisition weights have ratios bounded between fixed positive constants less than one. They need not be geometric. For every nonempty admissible prefix u the new proof gives strictly smaller distortion for uv than for v. Stationarity then gives strict mass-weighted energy decrease even when the two cylinder masses are equal. This is the point at which the full-shift proof could not simply be copied.

The entire greedy admissible tree is suffix closed. For L leaves the exact count is `1 + sum_internal actual_outdegree`, and the bound is `(b+1)(2L-1)`. The old regular full-tree formula is not applied to a graph with unary nodes. A bounded unary-chain argument and a fixed-budget-dilation lemma make the upper count compatible with the same-M lower bound.

For the exponent, forbidden concatenations are dropped only in the upper partition-sum inequality. Lower bounds use spatial and terminal terms and admissible Gibbs measures. Exponential tail rate is sufficient for the pressure exponent, but not for its critical correction. Strong separation, a finite graph and the stated distortion/observability remain real assumptions; this is not a theorem for overlapping or countably branched systems.

## E2 — a hidden common-refresh component is still regeneration

**Mathematical response:** `thm:v6-filter`, `lem:v6-compander`, `cor:v6-gaussian`.

The new theorem receives observations at every time. It assumes a recursion for the true full-history conditional mean with a conditional fourth-moment contraction coefficient. Individual updates may expand. There is no renewal clock, kernel minorization, independent reference component, or artificially supplied initial posterior in this theorem.

An inward rational compander with `(2n-1)^d` values controls its own fourth moments on the unbounded state space. The exact and quantized recursions use the same observations. Conditional contraction gives a uniform excess-risk bound proportional to `n^-2`, while a density lower bound on the stationary posterior mean gives the unrestricted M-centre lower bound. Consequently the optimal raw risk is `B + Theta(M^(-2/d))`, where B is the **full-history** Bayes floor.

For the stationary autoregressive hidden Gaussian chain with nonzero coefficient and Gaussian observation noise, we derive the conditional variance, gain and contraction from Gaussian conditioning. Its k-step hidden transitions are translated Gaussians with unbounded means. A bounded-set argument excludes every nonzero global common minorizing measure for **each fixed k**. Thus this example cannot be inserted into the earlier fixed-step global-minorization comparison.

The constants display their deterioration as the posterior contraction coefficient approaches one. The result is not asserted at coefficient one or for arbitrary nonlinear filters. The earlier positive-minorization theorem remains intact, but is no longer the only dependence mechanism.

## E3 — the active A2 endpoint was stale

**Correction and source refresh:** `HISTORY_AUDIT.md`, `HISTORY_INPUT_MANIFEST.json`, and `history-sources/A2-v118/`.

The active numbered A2 branch found in the fresh discovery is `revision/a2-v118-higher-defect-nonreduced-generators-2026-09-22`, fixed at `44bfc648ead008896a6981a7302a6d5ab8b21bb8`. We downloaded its source-bound artifact from successful run `35716811626` and consulted the native higher-defect conductor, nonreduced-generator/fat-point and statistical-experiment proofs. Their exact bytes and provenance are recorded, and the four selected source files are included as uncompiled consultation material.

A2-v112 is retained only as the explicitly older source edition used in previous revisions. It is not described as the current endpoint. The v118 conductor example has a nonreduced rank-jump locus; its determinant powers and arbitrary-base-change statements require their exact scheme strata. None is converted into an observational likelihood by assertion.

The active A1 endpoint was also freshly queried and remains v37 at `90465076589f5e5c69227d624f278c47744f1c1d`. The audit distinguishes this **fixed discovery snapshot** from the frozen eleven-paper history. It makes no claim about revisions created after that discovery or about rereading every archive file word for word.

## E4 — theorem-producing leverage on the pipeline

**New application:** `thm:v6-a2-budget`, in the complete edition.

The current A2 count-to-contact proof permits deterministic score precision tending to zero and a growing overflow radius. We fix its known-mark, preassigned-centre physical protocol and make its hard alphabet explicit. For r contact-score coordinates, a J-by-...-by-J grid with one overflow state has at most `J^r+1` labels, and its Le Cam distance to the contact Gaussian experiment is bounded by

`C [ N^(-1/5) + J/(R sqrt(N)) + R/J + exp(-c R^2) ]`.

This follows from a direct jittered-Poisson total-variation estimate, boundary-crossing control for the **unjittered physical statistic**, and a parameter-independent Gaussian histogram reconstruction. The jitter is a comparison device, not an additional physical measurement. Taking `R ~ sqrt(log N)` and `J ~ R N^(1/4)` supplies error `O(N^(-1/5))` with `O(N^(r/4)(log N)^(r/2))` labels. This is a sufficient budget, not an unproved optimal lower bound. It is a quantitative extension of an actual current pipeline experiment, not an unrelated surrogate Gaussian model.

The nonregenerative theorem also provides a fully verified, noncompact posterior realization with an infinite-time hard-register rate, rather than an unspecified compact coordinate approximation. It does not prove the old Sinai/hard-particle observation charts.

We do not declare the historical Sinai raw LLT, particle/path LDP, nonlinear semigroup, common unbounded form domain or physical phase theorem proved by these applications. They are different statements with different hypotheses. The new application is precisely identified so that its actual mathematical leverage can be evaluated without turning a programme label into a proof.

## E5 — nearest-neighbour literature and novelty

The introduction now compares the actual statements with Lindsay–Mauldin (2002), Atnip–Roychowdhury–Urbański (fixed 2018 preprint, Theorem 3.1), Ghomi–Linder–Yüksel (2022), Kara–Yüksel (2022, Theorem 12), and **the published 2026 Cregg–Alajaji–Yüksel paper, Theorem 2 and Corollary 2**. The latter's published primary PDF became accessible from the authors' university site and was checked; its numbering is not confused with the earlier preprint.

Spatial thermodynamic quantization and stability-based finite-memory approximation are expressly acknowledged as established results. The infinite conformal literature permits geometries beyond this paper's hypotheses. Our asserted differences are the survival-weighted observable orbit, admissible exact suffix realization, unrestricted persistent-state converse, and the matched whole-register Bayes excess in the continual-observation setting. Neither a thermodynamic formula nor filter quantization alone is presented as a new invention. `LITERATURE_AUDIT.md` specifies source versions and exactly what was checked, rather than claiming a complete priority determination.

## E6 — critical second order

**Mathematical response:** `thm:v6-critical` and `thm:v6-window`.

For the Parry law on an arbitrary primitive graph and equal-ratio geometric branches, take survival `q^k(k+1)^(-kappa)`. At `q_c=r^(2 beta)`, the matched risk has correction `(log M)^(1-kappa)` for `0<=kappa<1`, `log log M` for `kappa=1`, and a bounded factor for `kappa>1`. Thus the same graph, observable, metric geometry, first-order pressure roots and critical exponential survival rate admit different second-order laws.

For `q_n=q_c exp(x/n)` the finite profile has a uniform bounded-x limit, with an integral for kappa below one, logarithmic normalization at one and a zeta normalization above one. The optimal risk is comparable to the profile; an exact optimal coefficient is not inferred. These theorems classify a specified Markov-renewal family and show that first-order pressure data alone do not determine a universal critical correction. They do not classify every unequal-derivative geometric-tail Gibbs model.

## E7 — operational meaning of the resource

**Mathematical response:** `thm:v6-interface` and `ex:v6-interface`.

An M-state machine whose decoder also sees a K-valued event can be simulated pathwise with KM states and no free decoder event. Conversely a machine may ignore that extra input. Register tuples and binary checkpoint encodings admit exact state-set bijections. Fixed finite overheads preserve the exponent, and preserve risk orders for the proved fixed-dilation profiles.

A continuously valued free decoder observation changes the experiment: for an exactly observed uniform scalar, one free-observation state has zero risk, while an M-valued post-update register alone has error `1/(12 M^2)`. The operational theorem therefore proves specific equivalences and a specific strict boundary. It does not identify persistent cardinality with runtime, description length, or a channel-rate constraint.

## Sections 12–15 and proposed routes

The frozen eleven-paper history, active A1 and active A2 are separately pinned. All previous core proof bodies remain in the complete edition; the principal edition contains the new realization chain and its full retained general-converse dependency. Earlier root, calibration, HMM and control results remain available but are not used as unproved premises for the new theorems.

| Proposed route | Actual revision |
|---|---|
| A, beyond the full shift | Primitive forbidden-transition language, charged unary nodes, metric realizations in arbitrary dimension. |
| B, no one-step regeneration | Conditional posterior contraction and an unbounded hidden Gaussian chain with no fixed-step global common minorizer. |
| C, observables | Quantitative finite-delay observability; an explicit noninjective planar example. |
| D, critical refinement | Power-log/log-log/bounded classification and uniform finite-size profile windows for a Markov-renewal family. |
| E, pipeline theorem | Joint sample/register deficiency theorem for the current A2 count-to-contact protocol; historical model-specific gates are not conflated with it. |
| F, current snapshot | Native A2-v118 source and active A1-v37 head checked and pinned. |
| G, literature | Theorem-level primary-text comparisons, including the actual published 2026 finite-window paper. |

Both editions are submitted for further mathematical refereeing. The source, generated products and verification receipts are distinct objects. No diagnostic count, source-preservation result or successful build is presented as independent mathematical approval, priority certification or acceptance by a journal.
