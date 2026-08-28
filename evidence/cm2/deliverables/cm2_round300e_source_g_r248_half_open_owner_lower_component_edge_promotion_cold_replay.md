# Round300-E cold replay

All runs were cacheless full reconstructions from the sealed upstream inputs.
The producer and independent verifier were replayed under distinct Python
hash seeds.

| role | `PYTHONHASHSEED` | mode | elapsed | max RSS | status |
|---|---:|---|---:|---:|---|
| producer | `300511` | write | `91.73 s` | `4,587,960 KB` | PASS |
| producer | `300977` | no-write | `92.90 s` | `4,591,100 KB` | PASS |
| verifier | `300571` | write | `320.86 s` | `4,603,700 KB` | PASS |
| verifier | `300929` | no-write | `322.36 s` | `4,619,948 KB` | PASS |

Both producer runs reported:

```text
12,992 witnesses
12,992 canonical all edges
472 Round300-C overlaps
12,520 novel edges
```

The first verifier run rejected `36/36` attacks, including `32` fully
recommitted semantic attacks, and produced:

- attack suite SHA-256:
  `3591536d58e3999fe059cd121e28bcbdc14fc795538ca49b5d1c2e88ddbea112`;
- verification SHA-256:
  `313008d59a2d67b5ce4b7c8d62cd68a26a855a65c34396b5ae0176dda2096d4a`.

The second verifier seed reproduced the same attack and verification bytes
exactly. The dual-seed cold replay is closed.
