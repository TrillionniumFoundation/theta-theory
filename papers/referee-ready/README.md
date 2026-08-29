# θ-Theory five-paper series — active v4 baseline

This directory contains the five controlling manuscripts retained after repository
governance cleanup. Historical source variants are preserved on
`archive/full-v4-pre-governance-2026-08-29` and are intentionally absent here.

For every paper, the only controlling manuscript and bibliography are:

```text
main.tex
references.bib
```

Normative technical appendices remain part of the formal-review package.

## Current papers

1. Paper I — bilateral response and symbolic desingularization.
2. Paper II — pressure, physical diffusion and suspension response.
3. Paper III — rough homogenization and microscopic theta semigroups.
4. Paper IV — filtering and games.
5. Paper V — tangent laws and stochastic representations.

This v4 set is a baseline for the v5 platform and architecture revision. No paper title,
theorem statement or proof was changed by the governance commit.

## Build

```bash
make -C papers/referee-ready all
```

Repository hygiene is checked by:

```bash
python3 tools/verify_active_tree.py
```

The revision has not yet received a second independent line-by-line mathematical
review. Compilation and finite-dimensional formula checks are not correctness
certification.
