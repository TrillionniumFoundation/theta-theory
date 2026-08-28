# CM2 Gate 3 third continuation: all eight source-cell interval atlases

Date: 2026-07-15  
Scope: rational two-disk torus pilot, standard solid-boundary section
`N=G disjoint-union W`, complete parameter window `|s|<=1/400`.  The frozen
v51/v52 files and the shared research log were not edited.

## Decision

**The complete eight-cell conservative first-hit atlas is certified.  Gate 3
itself remains `NOT_CERTIFIED`.**

The previous continuation covered only `G:E`.  This continuation evaluates
four representative charts with 192-bit Arb and transports them through the
only two reflections that preserve the horizontally displaced family.  It
thereby covers all eight source cells without shrinking the parameter window:

- direct Arb representatives: `G:E`, `G:N`, `W:E`, `W:N`;
- exact reflected charts: `G:W`, `G:S`, `W:W`, `W:S`.

The resulting atlas has 143,248 exact dyadic leaves:

| leaf class | count | certified meaning |
|---|---:|---|
| `unique_first` | 47,436 | one incoming root is strictly earlier than every possible competitor |
| `tangency_graph` | 216 | one monotone physical first-tangency graph, with every competitor later or absent |
| `multi_candidate` | 95,596 | conservative unresolved collar; no event claim |

Across the eight full candidate registries, 3,038 pair rows and 10,288 triple
rows remain unresolved co-occurrence collars.  Consequently no immutable
global event table, DQ, or scalar-current matching is claimed.

Evidence:

- `deliverables/cm2_gate3_eight_cell_symmetry_atlas_cert.py`;
- `deliverables/cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json`;
- `deliverables/cm2_gate3_eight_cell_symmetry_atlas_verifier.py`;
- `deliverables/cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.sha256`.

## 1. Uniform physical domain and first-root semantics

Every chart uses the closed rational cover

\[
 -\frac{177}{250}\le t\le\frac{177}{250},\qquad
 -1\le p\le1,\qquad
 -\frac1{400}\le s\le\frac1{400}.
\]

Since `(177/250)^2>1/2`, this contains the complete dominant-coordinate
normal cell.  Every leaf spans the entire `s` interval; no parameter sampling
or `s=0` reduction occurs.

For each retained target, the certificate evaluates

\[
 \ell=u\cdot(a-q),\qquad
 \Delta=R^2-(u^\perp\cdot(a-q))^2,
 \qquad \tau^-=\ell-\sqrt\Delta.
\]

Thus a resolved leaf uses the selected positive incoming root, not merely the
sign of the discriminant.  Every possible competing root is either absent,
behind, or proved strictly later.  At a tangency leaf, a fixed-sign
`partial_p Delta`, opposite face signs, and strict competitor separation give
one physical first-tangency graph.

## 2. Exact reflection transport

Only two orientation-reversing isometries preserve this parameter family.
After rebasing the source lift they are

\[
 J_x:(x,y,s,p)\mapsto(1-x,y,-s,-p),
 \qquad
 J_y:(x,y,s,p)\mapsto(x,1-y,s,-p).
\]

`J_x` maps `E` to `W`; `J_y` maps `N` to `S`.  In both cases `t` is
unchanged.  The sign change of `p` follows because a reflection reverses the
chosen counterclockwise tangent orientation.

For example, on a gray source `J_x` relabels

\[
 G[i,j]\mapsto G[-i,j],\qquad
 W[i,j]\mapsto W[-i-1,j],
\]

while on a white source, after rebasing `W[0,0]`, it relabels

\[
 G[i,j]\mapsto G[1-i,j],\qquad
 W[i,j]\mapsto W[-i,j].
\]

The executable certificate checks, for every retained target:

1. the relabeling is a bijection onto the reflected chart's candidate list;
2. the target-minus-source centre displacement agrees coefficientwise as an
   affine function of `s`;
3. the normal and tangent transformation gives `p -> -p`.

Orthogonality then preserves `ell`, `Delta`, and `tau^-`, hence also all
first-root order comparisons and tangency incidence rows.  The four complete
relabeling registries have immutable digests in the manifest.

A 90-degree rotation is **not** used: for `s!=0` it turns the horizontal
displacement `(1/2+s,1/2)` into a vertical one and therefore leaves the
specified parameter family.

## 3. Per-chart results

| chart | provenance | leaves | unique | tangency | multi | unresolved pairs | unresolved triples |
|---|---|---:|---:|---:|---:|---:|---:|
| `G:E` | direct Arb | 16,580 | 5,276 | 38 | 11,266 | 459 | 1,738 |
| `G:W` | exact `J_x` | 16,580 | 5,276 | 38 | 11,266 | 459 | 1,738 |
| `G:N` | direct Arb | 16,630 | 5,340 | 42 | 11,248 | 459 | 1,740 |
| `G:S` | exact `J_y` | 16,630 | 5,340 | 42 | 11,248 | 459 | 1,740 |
| `W:E` | direct Arb | 18,930 | 6,518 | 24 | 12,388 | 294 | 824 |
| `W:W` | exact `J_x` | 18,930 | 6,518 | 24 | 12,388 | 294 | 824 |
| `W:N` | direct Arb | 19,484 | 6,584 | 4 | 12,896 | 307 | 842 |
| `W:S` | exact `J_y` | 19,484 | 6,584 | 4 | 12,896 | 307 | 842 |

The gray charts retain 57 targets and therefore have 1,596 pair and 29,260
triple registry rows each.  The white charts retain 55 targets and have 1,485
pair and 26,235 triple rows each.  Every row digest is replayable from the
leaf active sets.

The unresolved counts are not counts of physical multiple incidences.  They
only state that a closed interval leaf retains those labels simultaneously.
Calling them physical pair/triple events would be an invalid strengthening.

## 4. What remains before Gate 3 closes

The scope has advanced from one of eight cells to all eight, but the exact
global event inventory is still blocked by:

1. exact resolution or joint normal forms for the 95,596 multi-candidate
   leaves;
2. physical common-tangent/root-order classification of the 3,038 unresolved
   pair and 10,288 unresolved triple rows;
3. immutable face labels, one-sided traces, ownership, polarity and coarea
   coefficients for every actual global row;
4. global DQ assembly;
5. restrictionwise physical/source scalar-current matching.

Further blind dyadic refinement is not by itself a proof strategy: a genuine
tangency or root-order boundary remains interval-unresolved at every finite
depth unless it is put into a validated normal form.

## 5. Reproduction and fail-closed behavior

```bash
python3 -m py_compile \
  deliverables/cm2_gate3_eight_cell_symmetry_atlas_cert.py \
  deliverables/cm2_gate3_eight_cell_symmetry_atlas_verifier.py

# Full positive certificate; about 31 minutes on the reference host.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_eight_cell_symmetry_atlas_cert.py

# Fast provenance/registry tamper test.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_eight_cell_symmetry_atlas_verifier.py --self-test

# Expected exit 2: conservative cover passes, exact/global layers remain open.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_eight_cell_symmetry_atlas_verifier.py

# Optional second full Arb replay of every digest.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_eight_cell_symmetry_atlas_verifier.py --replay
```

The full positive certificate exited `0` after 1,835 seconds.  The quick
self-test exits `0`; the live incomplete-global verifier exits `2` by design.
The frozen v52 manifest was rechecked and every row returned `OK`.
