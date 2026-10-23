# Proof audit — General Theta Foundations I, R78

This is an author proof audit and internal cross-challenge record. It is not an external referee report, proof-assistant certificate, human expert endorsement, exhaustive priority clearance or editorial decision. The latest applicable R65 report reviewed R65; the current additional arguments require new independent assessment.

## New proof chain and adversarial points

| Point examined | Argument and resolution | Boundary retained |
|---|---|---|
| Finiteness of the fixed-row Bellman problem | Start the original prescribed-label controller from each sigma_i. The all-initial-state guarantee gives a proper comparison policy and x_i<=C for every reset state. | A single fixed prior does not give this conclusion. Restart is used in the comparison proof, not granted to the new controller. |
| Arbitrary stochastic updates | Every original continuation uses the same finite row palette. Bellman inequalities apply even when the old controller remembers sampled commands/private coins. A simultaneous minimizing selector writes one existing label after each report. | Only routing is determinized; mixed command rows are not generally purified. |
| Unreachable improper pairs | The proof constructs a new proper reset-state selector. It never requires transience of every pair in the old sM product chain. | An unused label may be improper without invalidating an all-state pure-start controller. A diagnostic explicitly realizes this. |
| Compact bound rather than a hidden assumption | A full-support one-row controller is explicitly proper; its resolvent gives C0. Every contender at cost b<=C0 has palette potential x_i<=b. | At an infimum equal to C0 the baseline is the certificate; below C0 use an approximating sequence. No attained optimum is assumed prematurely. |
| Necessity and sufficiency | Finite supersolutions bound finite-prefix costs. The positive conditional mean cost floor implies finite expected duration; positivity of effects gives the initial operator bound. Conversely normal form gives a feasible certificate. | Zero-cost infinite failure loops are excluded by the floor. No bounded-score or TV theorem is used for an unbounded duration. |
| Attainment and exact algebraic synthesis | A nonempty finite union of compact row/potential sets has a minimizing spectral value. Polynomial constraints and principal minors give exact algebraic decision/sample procedures. | No general elimination computation, polynomial runtime or exact numerical tie detection is claimed. |
| Continuity | Fixed proper attaining selector gives upper semicontinuity; locally bounded supersolution subsequences with one selector give the lower inequality. | A limit supersolution need not lie below one selected limiting cap; its finite certificate already proves properness. The discrete threshold may jump. |
| Continuing-row purity in the cover family | At a global minimum, separate concavity lets each noninitial row be replaced by a simplex vertex without worsening the objective. | Family-specific existence of a pure optimizer, not purity of every optimizer or of general reset instruments. |
| Uniform-subset initializer | Capped-simplex exchange minimizes the linear term; the remaining value is affine between reciprocal-integer caps, hence an endpoint suffices. | Flat regions permit other nonuniform optimizers. Uniform support is not asserted to be unique. |
| Exact hierarchy and older D_M | Singleton coefficients give the formula for every M. Re-solving with the first-residual coefficient gives D_M=(V_M-V_*)/2. | n>=2, r=1/2 and the displayed family are essential to the strict steps and factor two. |
| Noncommuting physical realization | The offdiagonal effect perturbation leaves all reset expectations unchanged, so x_i<=4 and value changes by at most 4 epsilon. Split success into F9=(G-I)/8 and F1=B-F9, with charges 9 and 1. | Mean costs stay between I and 4I; actual charges {1,9} are not [1,4]. No cost suboutcome is exposed as an extra observation. |

The complete proofs are in `sections/53-reset-memory-frontier.tex`, not deferred to numerical diagnostics or an abstract realization hypothesis. The exact native theorem/dependency map gives their premises and original-source references. A root-author pass added an explicit infimum-at-C0 argument and separated construction reuse from logical dependence at the r=0 endpoint.

## Internal cross-challenge

Two author-team AI work streams independently identified the full reset frontier as the substantive gap beyond R77's D_M. One developed the written proofs; the other challenged the all-state cap, unreachable-pair issue, covering reduction, initializer optimality, continuity and noncommuting cost/report compatibility. The independent challenge memorandum and its development evidence are retained in `provenance/r78-author-challenge/`. This describes internal author work and does not pretend to be a commissioned or human referee assessment.

## Independent finite mathematical diagnostics

`diagnostics_r78_frontier.py` uses exact rational arithmetic and independently evaluates controllers on reachable product chains before comparing with enumerated report-only selectors. It checks arbitrary stochastic routing, singular effects, noncommuting qubit effects/costs, nonorthogonal reset states, the fixed-prior boundary, an unreachable improper label, the old semidefinite exposure example, finite mixed palettes for arbitrary cover families, and all resource levels for n=2,...,8 in the singleton family.

The development execution reported 102,462 exact conditions and no floating conditions, with identical ordinary/optimized outputs. Those development files are retained as such. The strict current-source verifier must rerun the integrated script and all 26 inherited suites. Its actual execution receipt, not this audit, establishes which integrated runs completed. Finite enumerations validate the stated instances and algebra; they do not prove universal optimality, quantify over all primitives, or certify novelty.

## Inherited proof continuity

The 235 predecessor native statement labels remain current. Every preexisting section theorem body except the editorial overview remains byte-identical; the supplement's complete mathematical suffix remains byte-identical; the R58 companion tree remains `007a1d7d5f5b880c670fc6f47a812ebd476bfb00`. All 622 predecessor files are preserved, including replaced wrappers, source manifests, old dependency maps and reports. The exact prior proof audit remains at `inputs/r77/PROOF_AUDIT.md`; its earlier closure judgments retain their stated scopes.

No R77 shared-preparation, common-mean Fourier, initializer, stationary, antichain or positive-exposure theorem was discarded or silently weakened. The old positive-semidefinite example still disproves the unqualified transversal formula; the new full program handles it through a different necessity-and-sufficiency theorem. The original general-M squared-sign problem and other independent open tasks remain explicit.

## Primary-source and evidence classification

The newly checked Amato–Bernstein–Zilberstein theorem already formulates fixed-size stochastic-controller optimization as an NLP. The main and priority ledger cite it directly; no novelty is claimed for that encoding. Bellman/SSP, spectral matrix order, finite concavity and real-algebraic elimination remain classical ingredients.

Written proof, exact finite computation, floating diagnostics, source authentication, native LaTeX, visual inspection, hosted CI, human specialist assessment and editorial decisions are distinct. A full native build can verify compilation and locators; it cannot establish the mathematical strength required by a particular journal. The publication receipt records actual build success/failure, SHA binding, file hashes and remote readback separately.
