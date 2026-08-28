# Final addendum: exact full high-frequency moving-family BDL

Let `Q_a=s(a)Q_0` be a compact smooth similarity family of a finite-horizon periodic Sinai table, with `0<s_-<=s(a)<=s_+`.  Let `C_a` be phase-space scaling and `A_a` the flow generator.

## Theorem P2-BDL-HF-SIMILARITY

The flow satisfies

\[
\Phi_a^tC_a=C_a\Phi_0^{t/s(a)},
\qquad
A_a=s(a)^{-1}C_aA_0C_a^{-1}.
\]

Therefore

\[
\boxed{
(z-A_a)^{-1}
=s(a)C_a(s(a)z-A_0)^{-1}C_a^{-1}.
}
\]

Every fixed-table high-frequency BDL resolvent estimate transfers uniformly to the compact parameter family; resonances scale by `s(a)^{-1}`; and every parameter derivative supported by the smooth maps `s(a),C_a` follows by differentiating the exact identity.

This is an actual full-frequency moving-scatterer theorem.  A nonconjugate family requires the separately declared graded generator-symbol packet; geometric compactness alone does not imply parameter differentiability of its high-frequency resolvent.

## Export

```text
P2-BDL-HF-FAMILY
```

is interpreted as the disjoint union of:

1. the unconditional exact-similarity theorem above;
2. the nonconjugate packet theorem under complete graded symbol data.
