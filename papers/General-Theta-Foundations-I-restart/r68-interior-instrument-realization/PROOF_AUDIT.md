# Author proof audit — R68

This is an author-side audit, not an external review or proof-assistant certificate.

| Statement | Load-bearing step | Critical boundary |
|---|---|---|
| Interior hull | Exact projective cap mass, net packing, support-function separation | Rayleigh error is quadratic in projective distance; arbitrary Hermitian directions are tested |
| Finite instrument realization | Positive branch interpolation and matrix identity at every actual history | Each recorded branch, zero branches, prescribed preparation anchors; no freely observed hidden index |
| Sparse rows | Exact elimination of affine dependence | At most d^2 successors per command/report row, not d^2 total hidden states |
| Stopped law and cost | Common external policy, disjoint finite terminal cylinders, monotone nonnegative sums | Nontermination included; mean observables give cost expectations, not an unspecified cost-observation joint law |
| Noise exponent | Fidelity cap for arbitrary mixed vertices and finite replacement-command net | Matching exponent only in the declared state-positive all-terminal-effects class; command count may grow |
| Algebraic construction | Finite projector/intertwining equations, quantified positivity, real-algebraic sample | Termination for a supplied positive margin; no polynomial bit complexity or general no-margin decision |
| Block interiority | Counted prefix images and phase; branch decomposition at block end | Intermediate reports and stopping preserved; physical calls not batched into a free call |
| Average-noise negative control | Recorded irrational unitary path stays pure | Proves no state-positive all-audit realization; does not prove arbitrary scalar HMM impossibility |
| Near-peripheral lemma | Eigenvector variance, a path of probability at least M^-n, repeated state | No irreducibility, symmetry or all-edge positive floor |
| Fixed-angle lower | Characteristic recurrence plus Gaussian-integer separation | Non-sharp bound; different from known worst-phase noise lower; not the squared-sign general-M curve |

Every new load-bearing step is proved in `sections/27-interior-instruments.tex`. The supplement gives explicit primitive Kraus maps, positive interpolation and a two-label adaptive observer. Exact rational killed-map calculations compare its performed cost and score with the 14-state joint hidden model. Finite checks diagnose formulas, not continuum truth.

The R67 source is byte-preserved in full. All previous current theorem bodies remain current; changes to main/supplement ordering and cross-reference filenames do not change their proofs. The current map is generated from actual native auxiliary files. R65 criticism of general boundary optimal-memory classification remains relevant: a finite physical hidden model is not a finite optimal controller, and that conclusion is not claimed.
