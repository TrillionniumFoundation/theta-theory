# Exact first-order measurement-curve certificate

`curve_geometry.py` accepts one JSON object with exactly `schema`, `dimension`, `outcomes`, `effects`, and `tangent`. The schema is `gtf85.measurement-first-jet/1`. Matrices use the inherited canonical Gaussian-rational representation. Outcomes are ordered. The dimension and number of matrices must agree, effects must be positive semidefinite and sum exactly to I, and tangent matrices must be Hermitian and sum exactly to zero.

For every support P_j the program requires `(I-P_j)H_j(I-P_j)=0`. The written normalized-factor lemma proves that, on this represented input, this is exactly first-order realizability by some analytic two-sided measurement curve. It is not a test that an arbitrary separately claimed curve is C2 or has a supplied curvature bound.

The certificate schema is `gtf85.curve-certificate/1`. It returns the input digest, support ranks/span dimension, exact Gamma matrix, Hilbert–Schmidt support projection/residual, covariance range membership, and finite-use regime. A zero tangent returns `higher_order_undetermined` and no curve-classification theorem label. A nonzero tangent returns `square_root` or `linear` under the fixed-two-sided-C2-curve theorem. It supplies neither uniform constants nor an angle interval for an unspecified curve.

Use `--verify certificate.json` to reconstruct and compare the entire canonical certificate. Extra/missing/modified fields are rejected. `--max-system-dimension` caps `(k-1)d²` before computation; exceeding it is an error, never a partial result. Error exits do not emit a successful certificate.

```sh
python curve_geometry.py examples/curve-rank-opening.json > curve-certificate.json
python curve_geometry.py examples/curve-rank-opening.json --verify curve-certificate.json
python curve_check.py
python -O curve_check.py
```

The exact decision is polynomial in represented rational bit length. No arbitrary real oracle, exact adaptive-distance computation, general recovery synthesis, physical experiment, continuum proof or independent priority judgment is performed. The complete statistical learner has a different interface and does not receive this known-pair advice.
