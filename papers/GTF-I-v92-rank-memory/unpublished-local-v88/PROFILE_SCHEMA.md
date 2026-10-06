# Exact allocation certificate — v88

Input JSON has exactly `allocation` (a nonempty list of positive integers, excluding booleans) and optional `phase_per_call` (canonical Fraction string in `(0,1/4]`). The latter represents the public product `Delta*s`; it does not assert a computed correction gap or curvature bound. Unknown keys, duplicate JSON keys, malformed fractions, a exceeded group cap, and an oversized input are errors, never a truncated certificate.

Output `gtf88.allocation/1` records the exact input hash, total calls, second moment, largest group, rational effective width and exact maximum under the same total/width budget. The maximizer uses the run-length triple `(full_groups,full_size,residual_size)`. This is not a search over physical testers. Optional clipping records `min(n_r,floor(1/(2Delta*s)))`, with every original group represented. It explicitly leaves the quadratic error condition unchecked.

Replay reconstructs all fields and compares canonical typed JSON, not Python's loose bool/int equality. A claimed operational distance, physical execution, continuum proof or priority clearance is rejected as a changed/extra field. All such scope indicators are false in the canonical output.

```sh
python profile_geometry.py examples/allocation-unequal.json > profile.json
python profile_geometry.py examples/allocation-unequal.json --verify profile.json
python profile_check.py
```

The integer bookkeeping is polynomial in the represented list length and bit length. The code neither samples a quantum device nor realizes the analytic bounded-statistic readout.
