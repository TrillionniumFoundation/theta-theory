# Exact one-sided cone and pair certificate

The input schema is `gtf86.one-sided-jet/1`. Its exact top-level keys are `schema`, `dimension`, `outcomes`, `effects`, `direction`, and `pair`. Effects and directions are lists of square matrices. A complex entry is `[real,imaginary]`, with both coordinates canonical reduced rational strings (for example `"0"`, `"-1/3"`). Binary floats, noncanonical rationals, unexpected keys and Boolean dimensions are rejected.

`pair` is either null or an object with exactly `effects`, `scale`, `remainder_budget`, `component_budgets`. These are the supplied legal F, rational s>0, rational Lambda>=0, and k nonnegative rational lambda_j with sum at most Lambda. Every PSD inequality `lambda_j s^2 I ±(F_j−E_j−sH_j)>=0` is required. Passing these sufficient tests proves the one supplied pair lies in the finite remainder neighborhood. It does not assert that s is smaller than a local theorem constant.

The exact program validates a legal normalized E, a Hermitian zero-sum H, and J_j=Q_jH_jQ_j>=0. It reports one of `regular_tangent`, `coherent_tangent`, `support_opening`, or `higher_order_undetermined`. The first two require every J_j=0 and are separated by the real Hilbert–Schmidt projection of Gamma=(i/2)sum[P_j,H_j] onto the support span. A zero H is not stationarity.

A positive diagonal element of a nonzero J supplies v=Qe_r, its squared norm and rational positive opening rate. When F is supplied, the exact label probability p is reported. The repeated impossible-event lower is then `2(1−(1−p)^N)` for every positive integer N. This expression is not the exact adaptive distance in general.

Use `python cone_geometry.py INPUT --verify CERTIFICATE` to rebuild all fields and compare canonical JSON. A tampered pair, changed mechanism, partial basis, altered rational field or integer-to-Boolean substitution fails replay. `--max-system-dimension` bounds `(k−1)d²`; exceeding the cap is an error, not a partial certificate. The mathematical polynomial bit claim charges the complete represented input length. It is unrelated to constructing the entropy-optimal dictionary or a quantum recovery.

The evaluator does not compute an entire curve, its curvature, the allowed small interval, a general tester or recovery circuit, or physical device data. Those exclusions are machine-readable in the output. See `cone_check.py` for exact finite identities and rejection controls; no finite regression output is a proof of the universal theorems.
