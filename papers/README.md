# θ-Theory five-paper external-review series

This directory is the complete active manuscript set.  It contains exactly five
papers and no historical paper versions.

## Series spine

```text
Paper I   geometric response and symbolic desingularization
   ↓
Paper II  correlated rough homogenization and physical time
   ↓
Paper III exact microscopic DPP and physical theta-HJB
   ├──→ Paper IV  filtering / information / Isaacs extensions
   └──→ Paper V   tangent-law core and stochastic representations

Paper IV ──→ Paper V optional pure-game representation only
```

## Platforms

- `OB3-MG-v1`: physical flagship.  Three-disk no-eclipse specular open
  billiard, specified Markov-Gibbs law, actual free-flight roof.
- `FB4-EXACT-v1`: exact nonzero moving-seam response and CI benchmark.
- `SL-SIM-v1`: similarity Lorentz conjugate control and maximality boundary.
- `AR-FILTER-v1`: optional hidden-state extension in Paper IV.
- `SV-CONTROL-v1`: optional volatility-control representation in Paper V.

A theorem may be called *same-platform* only when all load-bearing imports
carry one platform identifier or an explicit bridge theorem is supplied.

## External review object

Each paper directory contains only:

```text
main.tex
references.bib
README.md
REFEREE_GUIDE.md
```

Run:

```bash
make -C papers all
python3 tools/verify_external_review_tree.py
```

The five generated `main.pdf` files are the circulation copies.  Build success
does not certify mathematical correctness.

## Historical material

All prior paper versions, cumulative canonical volumes, CM2 evidence, and old
review packages are preserved on:

```text
archive/full-v4-pre-governance-2026-08-29
```
