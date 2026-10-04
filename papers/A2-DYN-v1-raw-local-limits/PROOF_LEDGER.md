# A2-DYN v1 — theorem and dependency ledger

All labels below refer to the active `main.tex`. A theorem with hypotheses is
not registered as an unconditional theorem about the full billiard.

| Result | Kind | Inputs and conclusion |
|---|---|---|
| `prop:marked` | Physical, unconditional | Invariant equilibrium suspension; entire marked collision record including both residual flights. No independent roofs. |
| `lem:winding` | Physical plus finite interval proof | Scalar reflection equation, 32 exact rational radius slabs, verified clearance and incidence; true four-impact winding orbit and rotation. |
| `prop:lattice` | Physical arithmetic, zero roof frequency | Explicit four-square first-return set, four physical fixed points, augmented determinant one. Periodic evaluation requires regularity; nonzero roof twist is not eliminated. |
| `lem:hessian` | Physical, unconditional | Positive optical action and Schur elimination; exact determinant at a normal alternating word. |
| `thm:edge` | Physical, unconditional | Two-dimensional Morse change of variables and section flux; explicit one-sided density jump. Fixed-word smooth constants only. |
| `prop:general-edge` | Physical, unconditional | Positive optical Jacobi matrix; unique normal-to-normal critical path for each admissible center word and uniform individual jump bound. No summed word bound. |
| `cor:raw-density` | Physical, unconditional | Coarea away from isolated regular critical points gives the actual mixed density for each finite induced count, with bounded insertions. No uniform LLT inferred. |
| `cor:nonLone` | Physical, specified inducing set | Nonzero jump in the `(0,0,2n)` lattice component prevents a globally L1 raw joint transform. Not a failure of the central LLT. |
| `prop:subtract` | Exact local repair | Add and subtract the explicit exponential edge. Original density is unchanged; isolated remainder has a finite second derivative measure. |
| `thm:LLT` | Conditional analytical interface | Printed uniform Gaussian expansion, L1 residual tail, and summable explicit edge measure imply raw mixed-density LLT. Full billiard hypotheses not verified. |
| `lem:splice` | Conditional frequency algebra | Actual fixed derivative-growth constants and strict compatible cutoff; exponential residual integrals. It does not produce those constants. |
| `prop:conditioning` | Conditional downstream interface | Weighted/unweighted uniform central density estimates give almost-everywhere density conditioning and contained shrinking intervals. Not arbitrary path insertions or saturated windows. |
| `prop:clock` | Conditional downstream interface | Functional CLT, uniform clock law, and small unfinished records give physical-time covariance. A scalar LLT does not supply these hypotheses. |
| `lem:covariance` | Conditional comparison | Finite-time parameter comparison and exponential correlations give a Green–Kubo modulus. |
| `prop:prediction` | Conditional inference | Actual LLT and geometric parameter modulus yield the explicit `sqrt(n)` mean-error amplification. |
| Collision-rate paragraph | Physical, unconditional | Exact equilibrium rate has derivative below 110 on the radius interval; geometric radius recovery suffices. |

## No circular import

The old round-17 raw LLT is a candidate being audited, not an input. A2-GEOM
is used only in the final collision-rate application. The residual LLT theorem
is proved from its own hypotheses by Fourier inversion; none of the mechanical
results invokes that theorem. Clock and covariance statements have independent
printed assumptions. No theorem calls an unproved global stage a certificate.
