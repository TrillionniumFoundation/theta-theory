# CM2 Gate 3 second continuation: adaptive `G:E` first-hit atlas

Date: 2026-07-15  
Scope: rational two-disk torus pilot, standard solid-boundary section
`N=G disjoint-union W`, gray east source chart.  The frozen v51/v52 files and
the shared research log were not edited.

## Decision

**Gate 3 remains `NOT_CERTIFIED`.**  This continuation gives a complete,
machine-replayable **conservative interval cover** of one full source cell,
uniform on the complete small parameter window.  It does not yet give an
exact event partition because 11,266 final leaves retain multiple possible
targets.

The certified advances are:

- the entire `G:E` chart is contained in an exact dyadic cover of 16,580 Arb
  leaves;
- 5,276 leaves have one strictly certified physical first target;
- 38 leaves carry one certified monotone physical first-tangency graph;
- those resolved leaves occupy exactly
  `1902927/204800000` of the covered volume, or
  `1902927/2899968 = 65.62...%` of the full cover;
- every leaf spans the complete interval `|s|<=1/400`; no parameter split or
  point-sampling shortcut is used;
- all 1,596 target pairs and 29,260 target triples now have reproducible
  conservative incidence-interface rows.

Evidence package:

- `deliverables/cm2_gate3_ge_interval_atlas_cert.py`;
- `deliverables/cm2-gate3-ge-interval-atlas-manifest-2026-07-15.json`;
- `deliverables/cm2_gate3_ge_interval_atlas_verifier.py`;
- `deliverables/cm2-gate3-ge-interval-atlas-manifest-2026-07-15.sha256`.

## 1. Exact coverage domain

The actual gray east cell is parametrized by

\[
 -1/\sqrt2\le t\le1/\sqrt2,
 \quad n=(\sqrt{1-t^2},t),
 \quad -1<p<1,
 \quad |s|\le1/400.
\]

The certificate covers the slightly larger closed rational box

\[
 -\frac{177}{250}\le t\le\frac{177}{250},
 \quad -1\le p\le1,
 \quad -\frac1{400}\le s\le\frac1{400}.
                                                        \tag{1.1}
\]

This is a certified superset because

\[
 (177/250)^2>1/2.
\]

Thus the phase interior and both grazing endpoint strata are covered; the
small normal-cell overlap introduced by the rational `t` padding is harmless
and deliberately conservative.

The initial `8*16=128` rational boxes are bisected deterministically to depth
at most 8.  Since every split replaces one box by its two exact rational
halves, the final leaves have exact total volume

\[
  \frac{177}{12500},
\]

which equals the volume of (1.1).  The executable verifier recomputes this
identity and the canonical digest of every ordered leaf row.

## 2. Rigorous leaf classifications

The 57 previously retained `G:E` target lifts are evaluated with 192-bit Arb.
For each target,

\[
 \ell=u\cdot(a-q),\qquad
 \Delta=R^2-(u^\perp\cdot(a-q))^2,
 \qquad
 \tau^- = \ell-\sqrt\Delta.
\]

Each final leaf is one of four fail-closed classes.

### 2.1 `unique_first`

One target has `Delta>0`, `tau^->0`, and its root interval lies strictly
before the rigorous lower bound for every possible competitor root.  The
competitor lower bound remains valid when its discriminant ball straddles
zero:

\[
 \tau^-_{\rm competitor}
 \ge \ell_{\rm lower}-\sqrt{\max(\Delta_{\rm upper},0)}.
                                                        \tag{2.1}
\]

There are 5,276 such leaves.

### 2.2 `tangency_graph`

One target has an interval discriminant crossing zero, positive physical
flight `0<ell<3`, opposite strict signs of `Delta` on the two `p` faces, and
a fixed-sign derivative

\[
 \partial_p\Delta
 =\frac{2(u^\perp\cdot(a-q))\ell}{\sqrt{1-p^2}}.
                                                        \tag{2.2}
\]

Equation (2.2) plus the face signs proves exactly one monotone tangency graph
over `(t,s)` in the leaf.  Its occurrence time is strictly before every
possible competitor.  There are 38 certified physical first-tangency leaves.

### 2.3 `multi_candidate`

The interval evidence has not isolated a single first target or one physical
tangency graph by depth 8.  Every target not rigorously made later by (2.1)
is retained in the active set.  This class is conservative evidence, not an
event certificate.  There are 11,266 such leaves, with at most 14 active
targets on one leaf.

### 2.4 `no_future_root`

Every retained target is absent or behind.  No such leaf occurs, consistently
with the independent `tau_max<3` certificate.

The exact volume breakdown is:

| class | leaves | exact volume |
|---|---:|---:|
| `unique_first` | 5,276 | `943587/102400000` |
| `tangency_graph` | 38 | `15753/204800000` |
| `multi_candidate` | 11,266 | `997041/204800000` |
| `no_future_root` | 0 | `0` |

The number of leaves is not used as a probability.  The resolved-volume
statement above uses the exact rational box volumes.

## 3. Uniform continuation on the parameter window

All 16,580 leaf boxes have

\[
 s\in[-1/400,1/400].
\]

The adaptive splitter never needed to bisect `s`; every root, no-root,
ordering and tangency-graph inequality is therefore uniform on the full
window.  This is a genuine small-window interval continuation layer.

It is not yet a global event-label continuation theorem: labels can still
change inside a `multi_candidate` collar, so those collars must be subdivided
or put into exact joint normal form.

## 4. Pair/triple incidence interface

For every unordered pair and triple of the 57 retained targets, the generator
records whether the targets co-occur in at least one `multi_candidate` active
set.

| order | total rows | separated by atlas | unresolved co-occurrence collar |
|---|---:|---:|---:|
| pairs | 1,596 | 1,137 | 459 |
| triples | 29,260 | 27,522 | 1,738 |

`separated_by_interval_atlas` is rigorous on this cover.  At a true shared
boundary point, closed interval evaluation would retain both discriminants;
a strict unique/tangency classification cannot discard the second target.

`unresolved_cooccurrence_collar` deliberately makes no claim that a physical
pair/triple incidence exists.  It is the finite list on which resultant,
common-tangent, duplicate-cancellation or joint-normal-form work must now be
performed.  Each full row registry has a canonical digest checked on replay.

## 5. Certified owner targets on resolved leaves

The resolved atlas selects 13 target lifts:

`G[0,-1]`, `G[0,1]`, `G[1,-1]`, `G[1,0]`, `G[1,1]`,
`G[2,-1]`, `G[2,1]`, `W[0,-2]`, `W[0,-1]`, `W[0,0]`,
`W[0,1]`, `W[1,-1]`, and `W[1,0]`.

These owner labels are interval-certified on their leaves.  Their presence
does not imply that the other 44 conservative target lifts are globally
empty; some remain only inside unresolved collars.

## 6. Remaining blockers

This second stage does not close Gate 3.  The exact missing work is now:

1. resolve or normal-form the 11,266 multi-candidate leaves;
2. classify the 459 unresolved pair and 1,738 unresolved triple collars;
3. repeat the interval atlas for the other seven source cells;
4. attach immutable face labels, one-sided physical traces, coarea
   coefficients, polarity and ownership to every actual event row;
5. assemble the global DQ and prove restrictionwise physical/source scalar
   matching.

The manifest keeps all five layers null/fail-closed.  Neither this local cell
cover nor the resolved-volume percentage is counted as an unconditional CM2
claim.

## 7. Reproduction

```bash
python3 -m py_compile \
  deliverables/cm2_gate3_ge_interval_atlas_cert.py \
  deliverables/cm2_gate3_ge_interval_atlas_verifier.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_ge_interval_atlas_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_ge_interval_atlas_verifier.py --self-test

# Expected exit 2: the conservative cover passes, exact/global layers do not.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_ge_interval_atlas_verifier.py
```

The certificate and verifier self-test exit `0`.  The live manifest audit
exits `2` until the unresolved collars and global DQ/matching fields close.
