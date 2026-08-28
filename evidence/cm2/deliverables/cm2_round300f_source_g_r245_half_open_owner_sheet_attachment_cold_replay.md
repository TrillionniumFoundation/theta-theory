# Round300-F cold replay

All four runs were cacheless full reconstructions from the sealed upstream
inputs.  The producer and independent verifier were replayed under distinct
Python hash seeds.

| role | `PYTHONHASHSEED` | mode | elapsed | max RSS | status |
|---|---:|---|---:|---:|---|
| producer | `300511` | write | `98.18 s` | `4,210,952 KB` | PASS |
| producer | `300977` | no-write | `101.13 s` | `4,198,124 KB` | PASS |
| verifier | `300571` | write | `104.48 s` | `4,207,124 KB` | PASS |
| verifier | `300977` | no-write | `99.67 s` | `4,206,060 KB` | PASS |

Both producer runs reproduced:

```text
264 R245 transition sheets
264 unique owner → post-Round266-root edge witnesses
264 excluded shadow incidences
0/128 Round300-A explicit-pair intersection
```

Both verifier runs reproduced:

```text
264 independently reconstructed ledger rows
36/36 targeted attacks rejected
27 semantic recommitment attacks rejected
9 parser/path attacks rejected
```

The byte-stable embedded commitments are:

- result:
  `48e7fa4e534cb372562c0fc44f4f84a6c4e728843b5e1b8d7b48a52ba0020938`;
- attack suite:
  `5ea43ed860c277686655617735dff058feb1e9f8d807b1e95aac9adc8ae15185`;
- verification:
  `f9f02ac65343ea60e048c9e93ee6e4b72dc81d04463fbc384a8f69f78737bf3a`.

The dual-seed cold replay is closed.
