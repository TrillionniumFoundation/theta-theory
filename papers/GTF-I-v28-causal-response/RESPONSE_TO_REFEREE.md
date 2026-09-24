# Response to the r11 and r12 reports on General Theta Foundations I

**Revision 28: Robust Saddles, Causal Memory, and Validation Order**  
24 September 2026

Controlling latest report: `reviews/general-theta-foundations-i-v27-pipeline-harsh-top4-r12-2026-09-24/REFEREE_REPORT.md` at `63f52685341e0121f5494c63768bf53999f3c6c5`. The parallel r11 report is frozen at `ebd325871e0706d1346780b6c00503d9246b72dc`. Both concern the v27 publication at `7a659e0a2a41cd91f1f6f4ddc3b01c50a77882e3`.

The reports credit the saddle-contact synthesis but identify three related limitations: the sharp full-execution theorem depends on a chosen order; positive-noise persistence has only an existential threshold; and the broad realization statement gives less information than the exact example. This revision addresses their intersection. It solves an explicit full-support saddle region, proves that the original Brownian sensor lies in that region throughout its stated noise range, and derives the optimal validation orders from contact-forced continuation channels. A zero-noise reverse-order construction and matching converse establish an exact memory jump at the support boundary.

The results are analytic theorems with explicit inequalities and channel witnesses. The accompanying regressions reproduce those witnesses; they are not offered as a substitute for proof. Stable labels below are resolved to actual numbers and pages in `evidence/THEOREM_LOCATIONS.json`.

## 1. r12 §12.1 / r11 §10.2: whole-schedule order dependence

**Resolved across all externally declared clocked interleavings for the positive-noise family. The remaining scheduler distinction is explicit.**

The existing interface, Definition `def:physical-class`, declares clocked schedules externally and charges autonomous phases. There are twenty interleavings of the two three-slot validation tapes when the internal report/report/mark order of each tape is preserved. Theorem `thm:all-clock-orders` minimizes the whole-schedule peak over all twenty schedules, and over all stochastic controller wirings within each schedule. For every positive off-diagonal parameter in the full-support rectangle, the minimum is exactly twelve. Exactly the candidate-first and target-first serial orders attain it. All eighteen nonserial orders need at least fourteen states.

This is not a comparison of two selected compilers. The converse starts with an arbitrary minimax-optimal original-interface controller. The supporting common-garbling private subfamily forces the full-word Bayes signs and the extreme-count contact coordinates. Strict words force deterministic validation events. The extra extreme-count witnesses are genuinely mixed future-output channels. At a cut with one report from each tape there are ten required deterministic channel vertices and four disjoint additional faces; at a cut with two reports from one tape and one from the other there are twelve vertices and two additional faces. Every nonserial order passes one of these cuts. The two serial orders have matching twelve-state residual implementations.

A potential loophole is treated explicitly: fresh randomized gates may have independent coins in the two validations. A zero mean when both words equal the indifferent atom therefore need not be a deterministic zero output. Every additional face witness is chosen so that its prefix excludes simultaneous occurrence of that atom. At least one event indicator is then deterministic, and the whole output channel, not merely its mean, is fixed. The lower proof permits both fresh-gate and stored-mask realizations.

Theorem `thm:reverse-jump` also determines the ideal target's reverse serial peak: it is exactly ten, with profile `(5,5,9,9,10,7,3)` during selection/validation. The first target bit can be discarded because the second equals it almost surely. A lower certificate at the cut after the target and the first candidate bit has eight deterministic vertices and two disjoint additional faces. Hence the old candidate-first count twelve is not order-independent at zero noise.

The following distinctions are part of the theorem, not post-hoc qualifications. The positive-noise result optimizes all twenty **fixed clocks**; an observation-dependent scheduler is a different action interface and is not optimized here. The ideal reverse-serial value ten is not asserted to be the ideal minimum over every interleaving. Nor is every nonserial full-support order claimed to have exact peak fourteen: the uniform converse fourteen is enough to characterize all minimizing orders, and some displayed upper implementations use fifteen.

## 2. r12 §12.2, §§5/10 / r11 §10.2: exact positive-noise memory and explicit range

**Resolved for the original physical family throughout `0 < sigma <= 1/24`.**

Theorem `thm:positive-saddle` treats the target family

```
Q(000)=Q(111)=(1+gamma)/4-kappa,
Q(001)=Q(110)=(1-gamma)/4-kappa,
Q(each off-diagonal atom)=kappa,
6/25 <= gamma <= 13/50,  0 <= kappa <= 1/1000.
```

For kappa>0 every target atom is positive. The value is determined by the unique root `33/100 < r < 7/20` of

```
r^3+(13-2*gamma+8*kappa)*r^2+(3-12*gamma+48*kappa)*r-1-2*gamma+8*kappa=0.
```

The theorem proves an explicit global square factorization, strict transverse monotonicity, all posterior coefficient signs, and a matching least-favorable two-point prior. Contact fixes the same five response rows, with a tie parameter uniformly in `(1/10,1/4)`. Three forced cube vertices and two disjoint faces therefore prove exact decision width five throughout the rectangle. This is an exact positive-support theorem, not a continuity statement about the ideal optimum.

Theorem `thm:physical-noise-form` identifies the existing microscopic target exactly. Conditional on the outgoing signal amplitude, the two equal-length Brownian windows have independent errors with a **common** conditional error probability e. Reflection of the y coordinates interchanges the preparation bit B without changing the signal amplitude. The actual mark W depends only on the independent center-of-mass z box. Thus the distribution of e does not depend on (B,W). With `mu1=E[e]` and `mu2=E[e^2]`, the physical law is exactly the displayed family at

```
gamma=1/4-mu1/2,       kappa=(mu1-mu2)/2.
```

The original mechanical/Gaussian estimates give `0<e<1/600`. Hence

```
1/4-1/1200 < gamma < 1/4,
0 < kappa < 1/1200,
```

inside the proved rectangle for **every `9/10 <= d <= 11/10`, `0 < sigma <= 1/24`**. The dependence of the two reports through their common random signal is retained: replacing `E[e^2]` by `(E[e])^2` would be incorrect and is included as a negative control.

Combining these theorems yields exact physical decision width five and exact minimum declared-clock peak twelve on the whole original positive-noise range. In the reverse serial order exact memory jumps from ten at sigma=0 to twelve at every positive sigma in that range. Thus full support can alter exact memory even as the law converges in total variation. This gives both a stability region away from the support boundary and an explicit description of a failure of stability at that boundary.

The rectangle is a two-parameter symmetric region of full-support laws, not an arbitrary nonsymmetric total-variation neighborhood. The result does not evaluate the old four-state loss delta_*; it makes that unevaluated quantity unnecessary for the exact classification of this physical family. It is stronger in this direction than inferring persistence from delta_* and a TV bound.

### Calibration and stochastic precision

For a specified target, the exact constants are integrals of its known preparation and sensor law. They do not give the auditor the unknown private simulator parameters. Proposition `prop:physical-acquisition` additionally treats acquired target calibration. Three category counters from n target preparations give estimates of gamma and kappa. With probability at least `1-4 exp(-n*a^2/2)`, the estimated-target response, using a dyadic tie coin within `2^(-b)`, has true worst-case score at least

```
U2(true target) - 9*a - 2^(-b).
```

The counter register, report buffers, program selector and fair-bit coin workspace are all charged. The total preparation count is n+4. Exact atomic state counts are not conflated with exact finite-fair-bit implementation of an algebraic probability.

## 3. r12 §12.3 / r11 §10.1: a reusable realization-complexity certificate

**A finite-interface facial scheduling theorem is added, with a matching physical application.**

Theorem `thm:facial-schedule` associates lower capacities with consumed-prefix configurations in a legal schedule graph. The capacities are obtained from continuation rows forced by contact for **every** optimizer, using mandatory vertices and disjoint faces. They are therefore lower bounds on all stochastic architectures, not the nonnegative ranks of a chosen response. Upper capacities come from one family of residuals closed under restriction; independent cut factorizations are not spliced into a fictitious machine.

The minimum of the maximum capacity along a schedule path is a finite bottleneck quantity. A matching compatible residual path certifies the exact optimal schedule peak. If the lower and upper fields agree, a simple bottleneck recursion computes the invariant, and slot-preserving exact causal recodings preserve it. With target support restrictions, a compatible completion is required: minimizing each cut's partial function separately is not sufficient.

This theorem applies to any finite frozen-decision experiment for which the stated contact and residual certificates can be established. Its ingredients are elementary and classical; no general solution of nonnegative rank or all causal realization problems is asserted. The new application is not merely formal: the capacity witnesses give twelve for each serial entrance and at least fourteen at every nonserial entrance, proving the exact optimum over the full declared-clock interface. The same language explains the ten-state ideal reverse realization and its full-support jump.

This makes the new theorem more than the v27 loss decomposition, while keeping a precise boundary around what is and is not classified.

## 4. r12 §9: separate the elementary loss identity

**Implemented without deleting the result.**

The old displayed identity is now Proposition `prop:loss-decomposition`, with its short proof. Theorem `thm:saddle-realization` is titled “Saddle-face contact and compatible realization” and carries the actual exact-attainment, contact, stationarity and compatibility statements. Its stable label remains. The assembly reversibly checks this expository split against the frozen predecessor, so no part of the old statement or argument disappears.

## 5. r12 §12.4 / r11 §10.3: sharp large-N asymptotics

**The existing all-N results are retained; this revision pursues the order/noise routes rather than claiming a new sharp asymptotic expansion.**

The reports explicitly propose alternatives rather than demanding every route. The endpoint law, universal least-favorable-prior localization and the derived ideal marked contact geometry remain in full. The new two-parameter full-support saddle is used to obtain exact physical memory and schedule consequences; it is not presented as a new asymptotic expansion. No first large-N correction, sharp Wasserstein rate or complete finite-N support classification is inferred.

## 6. r12 §12.5 / r11 §10.5: downstream proof dependencies

**The physical order/noise theorem is a new essential local consumer; historical dependencies are not fabricated.**

The exact Brownian target formula uses the previously proved collision-time and signal bounds, but adds preparation-symmetry analysis not supplied by the earlier TV estimate. Its exact saddle and decision-memory theorem require the new full-support contact calculation. The fixed-clock physical peak theorem then requires the new channel capacities and schedule theorem. None of these conclusions follows from the old chosen-machine upper bound or compactness persistence alone.

The Round-Seventeen ledger remains unchanged: A2's Fourier/LLT gates, A3's entropy/stopped-LDP gates, A4's global-kernel gates, B3's Gaussian/Mosco gates, B4's nonlinear-resolvent/semigroup gates, and C2's strict/form/optional-projection gates are distinct. This finite-state theorem does not prove their aggregates. No artificial edge is added to declare the eleven-paper pipeline closed.

## 7. Novelty, exposition and preservation

The introduction isolates the new theorem claims from their ancestry. Stochastic positive realization, invariant cones, nonnegative rank, compatible state minimization and bottleneck dynamic programming remain classical ingredients. The originality claim under consideration is the explicit full-support saddle containing the actual Brownian experiment, its contact-forced all-declared-order memory classification, and its support-boundary jump. The adjacent literature record states the depth at which the sources were actually checked; no complete Norberg or Heller proof-level non-overlap audit is invented.

The article retains every preceding mathematical module and the complete previous substantive body. Only the introductory hierarchy is rewritten and the loss identity is split. Both complete predecessor volumes are appended unchanged. No original path is overwritten. Preserved page count is not an argument for significance; the new analytic proofs, rather than extra diagnostics, answer the reports.

The next referee can therefore focus on the global full-support square identity and posterior signs, physical symmetry and common-signal averaging, the safe mixed-channel witnesses under fresh gate randomization, the twenty-order path argument, and the compatible ideal reverse construction. These are the theorem-level changes of revision 28.
