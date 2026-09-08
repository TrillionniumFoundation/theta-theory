# Author response to Referee Round Twenty-Two — A3

The Round-Twenty-Three state and recovery have been rebuilt around the two decisive objections: loss of order and singular atomic recovery.

## A3.1 — sufficient ordered state

Every excursion mark contains the complete legal physical trajectory.  The empirical object is a marked point measure on scaled start time and mark space.  The start-time coordinate orders its atoms.  The stopped physical path is also retained as a state coordinate, together with the complete terminal mark and truncation fraction.  Consequently different Eulerian orderings remain different states even when their unordered transition counts agree.

## A3.2 — history moment

The false uniform bound over all complete histories has been removed.  The exact conditional kernel satisfies a Lyapunov-weighted exponential moment and drift estimate.  Stable-holonomy distortion controls density ratios on Lyapunov sublevels.  These are the estimates actually used for entropy compactness.

## A3.3 — number of returns

No lower tightness of `nu_N/N` is asserted.  A controller that pays order-`N` entropy for one excursion of length `N` is admissible.  Its mass is carried by a recession coordinate, and its tail cost remains in the good rate function.

## A3.4 — finite-KL recovery

Representative atoms have been eliminated.  On a finite mark partition, the recovered kernel preserves the desired cell weights but uses the reference kernel conditioned inside each cell.  It is absolutely continuous and its KL cost is exactly the coarse relative entropy, bounded by the original KL through data processing.  Refining partitions and finite-history martingale approximation recover every finite-cost control while sampling only legal physical excursions.

## A3.5 — conditional path LDP

A path functional is not treated as a fixed cylinder insertion.  The proof first establishes exponential approximation by finite-memory functionals on rate sublevels, applies source-inserted A2 local inversion for fixed memory, and only then removes the approximation.  The local polynomial factors cancel after this justified step.

The positive collision-time, physical-time, and conditioned path principles are retained on the corrected ordered state.
