# Theta-Theory v6 deterministic path-ensemble review tree

This package contains five revised manuscripts whose load-bearing platform is
`FB4-PE-v1`.

The central change is that the stochastic path law and theta parameter are no
longer supplied independently.  Lebesgue uncertainty in a deterministic
area-preserving collision map gives the base path law.  Conditioning a
mechanical current selects a unique canonical driven ensemble and

\[
\theta=I'(a).
\]

The theta-semigroup is the excess pressure of that path ensemble.  The five
papers then derive physical-time homogenization, dynamic programming,
controlled saddle corrections, axiomatic rigidity, tangent laws, Girsanov, and
BSDE representations.

Build all papers with:

```bash
make -C papers all
python tools/verify_v6.py
```

External line-by-line mathematical review is pending.
