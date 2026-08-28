# Round300-G cold replay

All four runs were cacheless full reconstructions from the sealed upstream
inputs.  Producer and verifier were replayed under distinct Python hash
seeds.

| role | `PYTHONHASHSEED` | mode | elapsed | max RSS | status |
|---|---:|---|---:|---:|---|
| producer | `300611` | write | `59.90 s` | `3,705,140 KB` | PASS |
| producer | `300977` | no-write | `61.41 s` | `3,704,428 KB` | PASS |
| verifier | `300673` | write | `66.19 s` | `3,706,712 KB` | PASS |
| verifier | `300991` | no-write | `64.05 s` | `3,705,412 KB` | PASS |

Both producer runs reproduced:

```text
3,232 complete Round300-A canonical pairs
128 exact explicit outgoing-seam candidates selected
128 exclusions
0 eligible component edges
```

Both verifier runs reproduced:

```text
128 independently reconstructed exclusion rows
43/43 targeted attacks rejected
34 semantic recommitment attacks rejected
9 parser/path attacks rejected
```

The byte-stable embedded commitments are:

- result:
  `4b4be63fc29c22f567934431088a5edce1746d353e6ef199359319ae26b71f15`;
- attack suite:
  `55de38ef3dc2ed4d4bed943c82c3e7e877940fd55da0d49ace98be600af1f07f`;
- verification:
  `390664db253c6046272b10bf993c6a4f5bd5a5f6ef4235b913af8d901b22a44b`.

The dual-seed cold replay is closed.
