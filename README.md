# θ-Theory — active five-paper external-review repository

The default branch contains only the current five-paper series, its platform
registry, governance rules, and build/verification tools.

## Start here

1. `papers/README.md`
2. `papers/COMMON_ACTUAL_PLATFORM.md`
3. `papers/SERIES_MANIFEST.yaml`
4. `status/ACTIVE_STATUS.yaml`
5. `papers/EXTERNAL_REVIEW_CHECKLIST.md`

## Active papers

1. Geometric response and symbolic desingularization.
2. Physical-time correlated rough homogenization.
3. Microscopic collision games and physical theta-semigroups.
4. Information, filtering, and Isaacs extensions.
5. Tangent laws and stochastic representations.

## Historical archive

All previous manuscripts, cumulative canonical volumes, CM2 evidence, and
older review materials remain preserved on:

```text
archive/full-v4-pre-governance-2026-08-29
```

Archived files are not current theorem sources.

## Build and verify

```bash
make -C papers all
python3 tools/verify_external_review_tree.py
```

The active branch is a research manuscript set.  Successful builds and
finite-dimensional checks do not constitute external mathematical review.
