# CM2 Gate 3 global physical-subrow atlas assault

Date: 2026-07-15  
Arithmetic: 192-bit Arb (`python-flint==0.9.0`)  
Verdict: **bulk atlas certified; maximal rows and global DQ/matching remain open**

## 1. What is new

The eight source charts are parameterised without a floating-point angular
coordinate.  On each dominant normal cell,

\[
 z\in[-1,1],\qquad t=z/\sqrt2,\qquad |s|\le 1/400.
\]

The four charts meet only on the exact seams `z=±1`.  For every
parameter-active signed chart sheet the certificate partitions the `(z,s)`
rectangle and proves, on every positive box, all of the following strict
properties:

1. the tangent direction is outgoing and its source coordinate is interior;
2. the tangent target occurs at `0<tau<3`;
3. no other physically admissible target is visible first;
4. there is a unique non-grazing first miss target after the tangency;
5. the parameter-coarea polarity is constant and nonzero.

Thus every positive box is a compact connected immutable physical subrow.
Positive boxes sharing an edge and the complete label

```text
(source chart, tangent target, side, miss target, coarea polarity)
```

are unioned by an exact rational edge test.

## 2. Finite completeness and performance guard

The first-hit test uses the already-certified source-wise candidate unions:

- source `G`: 76 targets;
- source `W`: 68 targets.

Their completeness follows from the frozen horizon `tau_max<3` and the
candidate reduction.  Only boxes that pass the first-hit test construct the
full 162-lift post-tangency miss registry.  Static target centres and radii
are cached.  This changes only evaluation order, not the predicates.

The final run used eight initial `z` intervals and adaptive depth nine.  It
finished in 95.36 seconds on one CPU core, with peak RSS about 251 MB.

## 3. Exact certified output

Across 384 parameter-active chart signed sheets:

| quantity | exact value |
|---|---:|
| leaf boxes | 200,464 |
| physical immutable boxes | 11,900 |
| complete physical labels | 60 |
| connected certified subrow components | 60 |
| largest component | 388 boxes |
| total parameter area | `96/25` |
| certified physical area | `1127/6400` |
| certified empty area | `339463/102400` |
| unresolved area | `35721/102400` |
| unresolved fraction | `11907/131072` |

The exact partition identity is

\[
 \frac{1127}{6400}+\frac{339463}{102400}
 +\frac{35721}{102400}=\frac{96}{25}.
\]

The complete leaf digest is
`5b2ba40fb621ba7484f90bace311fab8502b073c2811b73cdb6930569806bc23`.

## 4. Certified bulk symmetry matching

The 60 labels form exactly 15 four-element `Jx/Jy` orbits.  In every orbit:

- the box count and exact rational parameter area agree;
- `Jx` reverses the parameter-coarea polarity;
- `Jy` preserves it.

Consequently the polarity-weighted parameter area of the entire certified
bulk is exactly zero.  The orbit digest is
`502e20efe3a0815c86a9f691adf446222a004481818225cf2c8ab8fc4472502e`.

This is an exact bulk symmetry statement.  It is not the physical coarea
current identity on the unresolved collars, and it is not global DQ.

## 5. Fail-closed boundary

The remaining unresolved parameter area consists of strict interval collars:

| collar class | exact area |
|---|---:|
| source/target endpoint | `15573/51200` |
| miss-owner boundary | `717/20480` |
| first-visibility boundary | `399/51200` |
| parameter-polarity boundary | `3/1600` |

Therefore this result does **not** certify:

- maximal components across unresolved collars;
- quotienting components across the eight chart seams;
- the complete connected immutable event-row registry;
- distributional quotient (`DQ`) or physical scalar matching;
- unconditional CM2.

The earlier 320 suspect endpoint descriptors remain independently certified
physical-empty.  The present positive boxes are bulk subrows, not a revival
of the retracted 16-joint claim.

## 6. Reproduction

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_global_physical_subrow_atlas_cert.py

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_global_physical_subrow_atlas_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_global_physical_subrow_atlas_verifier.py \
  --self-test

# Deliberately exits 2 while maximal rows/global DQ remain open.
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_global_physical_subrow_atlas_verifier.py
```

Artifacts:

- `cm2_gate3_global_physical_subrow_atlas_cert.py`;
- `cm2-gate3-global-physical-subrow-atlas-manifest-2026-07-15.json`;
- `cm2_gate3_global_physical_subrow_atlas_verifier.py`;
- `cm2-gate3-global-physical-subrow-atlas-manifest-2026-07-15.sha256`.

