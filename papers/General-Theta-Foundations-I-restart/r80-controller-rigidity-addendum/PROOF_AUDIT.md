# Mathematical proof audit: first-order optimizer rigidity

## New conclusion and exact assumptions

The theorem concerns beta=1/4, a fixed hidden model chosen from two scalar instruments, two autonomous live labels, all six stochastic command/update probabilities, prescribed pure initial label 1, compulsory success stopping, and unit paid costs. A selected family can be discontinuous in epsilon. Near optimality means J_epsilon-V_2(epsilon)=o(sqrt(epsilon)), not merely convergence to the baseline value. Improperness is measured from the prescribed start; inaccessible dark labels are not incorrectly inverted.

The complete written proof is in the native Section 60. Its load-bearing chain is:

1. Baseline monotonicity, compactness and lower semicontinuity place every near-optimal family at the complete R80 equality set, including both possible command-row orientations.
2. R80 coercivity controls r-r0 and s+delta by O(sqrt(epsilon)), and gamma by O(epsilon).
3. A new uniform negative derivative in alpha proves 1-alpha=O(sqrt(epsilon)) before Taylor expansion. Simply knowing alpha tends to one would be insufficient.
4. The exact model-0 cost identity forces the repair sum s+delta to have a positive normalized limit and keeps the nonnegative gamma/epsilon term.
5. The full model-1 expansion keeps the nonnegative alpha-deficit and success-activation terms, uniformly in xi.
6. A positive weighted average and the strict equality cases of AM-GM force all normalized coordinates, including gamma/epsilon and the alpha deficit, to their specified limits.
7. Every scaled subsequence has the same constrained limits; xi remains arbitrary. The converse separately establishes properness, evaluates both costs, and compares to the inherited value asymptotic.

## Independent internal mathematical check

A separate internal checker reconstructed both implications from the frozen research proof and reviewed its actual R80 Section 57 prerequisites, including the polynomial certificate and the opposite-orientation derivative signs. It found no substantive error. It specifically verified arbitrary discontinuous selections, gamma=o(epsilon), the alpha deficit, free xi, the singular boundary and reverse realizability. Its one wording clarification, improperness from the prescribed initial label, is incorporated in the native theorem.

Frozen proof SHA256: `1da2e2d681f06a6b4b8bb1a4d8ba42d60e7dd60ac04098841ab06d742fc6cb71`.
Independent internal verification-record SHA256: `dc1d2628f0b2f322b1b1bb37042eaa4c8e7ee8d7391baf587dc5daaf80e0e176`.
Pinned R80 Section 57 SHA256: `d7566b473142d8e87797a5929f17186b48d790754583d233799be1a8080d43ce`.

This is not an external referee report, human-specialist endorsement, priority certificate, or review of all inherited mathematics. The controlling external report remains the actual older R65 document. The current authors also reconstructed Sections 58 and 59; that author read is not mislabeled a second independent review.

## Finite and native checks

`diagnostics_rigidity.py` checks the exact resolvent derivatives, full first-order coefficients, weighted cancellation and balanced coefficients with symbolic algebra, in ordinary and optimized Python. It uses no disableable assert statements. These checks support the written proof but do not replace its quantifiers, compactness argument or asymptotic remainder control. The strict complete build reruns all 32 unchanged inherited suites and compiles the full paper, supplement and companion. It does not turn counts or compilation into a mathematical or editorial verdict.
