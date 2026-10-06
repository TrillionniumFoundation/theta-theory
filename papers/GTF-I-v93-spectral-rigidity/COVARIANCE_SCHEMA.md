# Exact covariance certificate and affine repair — schema 1

`covariance_metric.py` implements a finite Gaussian-rational upper-certificate evaluator. The universal inequality is proved in Section 67; the implementation does not optimize an adaptive tester.

Input has exactly `schema`, `dimension`, `outcomes`, `effects_e`, and `effects_f`. Schema is `gtf83.closed-povm-pair/1`. Dimensions are positive integers, not booleans, and outcomes is at least two. Each effect is a square matrix whose entry is `[real,imaginary]`; both components are canonical rational strings (`0`, `-2`, `3/7`, not floating-point values, nonreduced fractions or expression strings). Effects must be Hermitian positive semidefinite and each tuple must sum exactly to the identity. Zero effects are accepted.

`--horizon` is a positive integer. `--max-system-dimension` is an explicit resource cap; exceeding it raises an error and emits no certificate. The real tangent system has p=(k-1)d² variables. Its Gram matrix is retained: the equation is `(L+G/N)x=b`, not `(L+I/N)x=b`. Legality, the linear residual and the exact squared modulus are checked.

The output schema is `gtf83.covariance-upper/1`. It binds a canonical input SHA-256, horizon, dimension, outcomes, system dimension, the exact rational squared modulus and solution tuple. `adaptive_upper_squared` is `min(4,4(k+1)Qcal²)`; take its nonnegative square root to obtain a valid upper bound. Equality of rational output objects is part of replay. Unknown keys, altered bounds, changed solutions and mismatched inputs fail verification. `--verify FILE` recomputes and compares the complete certificate. Supplying `--horizon` on replay also requires that exact requested horizon; omitting it uses the horizon bound into the certificate.

```sh
python covariance_metric.py examples/covariance-noncommuting.json --horizon 3 > certificate.json
python covariance_metric.py examples/covariance-noncommuting.json --horizon 3 --verify certificate.json
python covariance_check.py
python -O covariance_check.py
```

The function `affine_repair(matrices, accuracy)` performs the guarded map of Section 68. Its input is an explicitly represented Hermitian tuple and a positive rational accuracy. It returns the repaired tuple and a fallback indicator. If the candidate fails either balanced spectral bound, the result is the uniform tuple, exactly legal on every such record. Malformed matrix representations are rejected, not interpreted as observations.

The software executes finite matrix identities, certificate checks and guarded algebraic maps. The inherited scalar ternary statistical certificate is rerun unchanged. No general physical learner, complete arbitrary-dimensional statistical certificate grid or optimal dictionary is executed by this module. Runtime bounds for exact rational evaluation and affine repair do not imply efficient global code construction or readout synthesis.
