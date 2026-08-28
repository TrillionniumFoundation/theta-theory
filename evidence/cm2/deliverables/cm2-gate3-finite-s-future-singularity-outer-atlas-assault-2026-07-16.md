# CM2 Gate 3: finite-`s` future-singularity outer-atlas assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: eleventh-pass iterated common-atlas frontier and finite-`s`
common moving-endpoint mesh  
Strict verdict: **a finite rectangular future-candidate outer atlas on the
entire `|s|<=1/400` window, together with uniform fixed-`s` candidate-root
and artificial-`t`-boundary outer charges, is certified; a complete root-isolated
future atlas, a physical future face/current, branch-record `MT_DQ`,
`FACE_2CUT/FACE_TIME`, and Gate 3 remain `NOT_CERTIFIED`**

## 1. What is new

The eleventh pass had a full-measure depth-two atlas only at `s=0`.  The new
certificate replays the next-collision geometry on one fixed labelled
finite-parameter carrier

```text
A_fs = disjoint_union_(e=0)^63 ([0,1]_t x [0,1]_v),
s=(2v-1)/400.
```

Here `t` is the inward-angle coordinate of the already certified moving
maximal row, after the absolute angular endpoint trim `2^-20`.  Every moving
row boundary and all subsequent tangent, miss-collision, reflection, flight,
and next-target formulae are evaluated by two-variable first-order automatic
differentiation with 384-bit Arb interval arithmetic.

For every one of the `4,704` occurrence/candidate tangency discriminants, a
box is assigned one of three fail-closed types:

1. `immutable`: one next-collision owner is strictly earlier than every
   possible competitor throughout the box;
2. `transverse_root_strip`: exactly one candidate discriminant blocks the
   owner comparison, its `d/dt` interval excludes zero, the two vertical
   edges have strict opposite signs throughout the parameter slab, and its
   `t` width is at most `1/1024`;
3. `terminal unresolved`: any prerequisite, owner ordering, multi-root,
   tangency, or interval-dependency question not certified by the finite
   refinement remains positively in the outer cover.

No unresolved box is deleted or converted into a zero-measure assertion.
The normalized parameter slabs use half-open ownership `[v0,v1)`, with only
the final endpoint `v=1` closed, so adjacent slabs neither double-count nor
lose a parameter slice.

The replay begins with `32*8=256` rectangles per row and allows five
additional `t` bisections and three additional `v` bisections.  The
candidate-only fast path used for vertical-edge bracketing is guarded by an
exact audit: eight rows and parameter points give identical value, `d/dt`,
and `d/ds` ledgers to the full `4,704`-function evaluation.  The total
candidate count is separately asserted to be exactly `4,704`.

## 2. Exact full-window materialization

The 32-worker materialization made `1,507,924` strict interval audit calls;
the largest row required `86,746`.  It produced

```text
immutable terminal leaf components             626,274
transverse candidate-root strip leaves           6,246
terminal unresolved leaves                     129,634

immutable normalized (t,v) area          2028651/32768
root-strip normalized (t,v) area              921/8192
unresolved normalized (t,v) area             64817/32768
total carrier area                                      64

root-strip + unresolved outer area             68501/32768
outer fraction of the 64-row carrier       68501/2097152
                                                3.2663822174%
immutable fraction                              96.7336177826%
```

All `6,246` retained root strips have a strict `d/dt` sign and opposite
vertical-edge signs.  Therefore each contains one and only one candidate
root `t=t(v)` for every parameter in its slab.  The stored integer ceiling
on

```text
|dt/dv| = |(partial_s Delta)/(partial_t Delta)| / 200
```

gives the exact aggregate graph-length upper bound `8593/32`.  Its planar
candidate-root tube has the nonphysical parameter-integrated bound

```text
Leb([S_root]_rho) <= (408337/16) rho,       0<=rho<=1.
```

The full leaf registry is not transported through multiprocessing pipes.
Each worker sorts and hashes its own immutable, root, and unresolved
records, then returns a small row ledger.  The ordered global ledgers are

```text
row-record digest
  8c202faa1491cdca7351bd3ff9d0402f23504ff0eb3d8181ee20b72f0e810a28
row-work digest
  4817377eb109fd82d228a29a96a82aa3eab992554236a14fd11d7022512d9afc
parameter-slice digest
  b17617ec5e766e3575aac2ab5210ab12c35f31787279008602902ec79bd50b2c
```

This preserves a deterministic immutable audit trail while avoiding the
former gigabyte-scale result-pipe failure mode.

## 3. Typing boundary: parameter bookkeeping is not physical mass

The coordinate `v` only normalizes the parameter interval.  It is **not** a
probability variable and carries no physical law.  Consequently every
two-dimensional `(t,v)` area, perimeter, graph length, and tube above is
labelled parameter-integrated bookkeeping.  Multiplying such a
two-dimensional number by the row-density ceiling does not turn it into a
physical mass or current.

The valid physical-density use is instead a supremum on each fixed-`s`
slice.  Sweeping all half-open slab endpoints gives the following exact
uniform counts:

```text
maximum artificial leaf intervals on one slice       32,295
maximum candidate-root graphs on one slice               129
maximum unresolved intervals on one slice              2,062
maximum unresolved total t-width                      1031/512
```

For `N` artificial intervals, the `rho`-collar of their `2N` rectangular
`t`-boundaries has length at most `4N rho`.  The frozen angular density is at
most `18/5` with `dtheta/dt<7`, hence the normalized-`t` row-law density is at
most `126/5`.  This gives

```text
artificial t-boundary Lebesgue coefficient              129180
row-law-density weighted coefficient                   3255336
formal two-mark coefficient                            6510672.
```

For the candidate-root graphs, the corresponding fixed-s coefficients are

```text
candidate-root Lebesgue coefficient                         258
row-law-density weighted coefficient                    32508/5
formal two-mark coefficient                             65016/5.
```

Including the positive unresolved intervals, the full future-candidate
outer charge is

```text
row-law charge <= 64953/1280 + (547092/5) rho,
formal two-mark bookkeeping
               <= 64953/640  + (1094184/5) rho.
```

The nonzero intercept `64953/1280` is decisive: this finite-resolution
certificate does not prove a zero-intercept future-singularity boundary law.
Moreover, a retained candidate root has not yet been typed as the
**physical-first** collision boundary.  The displayed formal `(+1,-1)`
two-point charge is therefore not called a physical current.

## 4. What this closes, and what it does not

This closes the finite-parameter existence problem at the outer-atlas level:

```text
full |s|<=1/400 fixed rectangular carrier             CERTIFIED
finite future-candidate outer atlas                    CERTIFIED
uniform fixed-s artificial rectangular t-boundary Z   CERTIFIED
uniform fixed-s candidate-root outer Z                 CERTIFIED
```

It does not silently upgrade any of the following:

```text
complete finite-s root-isolated future atlas           NOT_CERTIFIED
physical-first typing and physical marked current      NOT_CERTIFIED
strong-space invariance of component restrictions      NOT_CERTIFIED
operator-norm one-step/depth-two DQ                     NOT_CERTIFIED
fixed-time branch-record MT_DQ                          NOT_CERTIFIED
physical FACE_2CUT / FACE_TIME                          NOT_CERTIFIED
Gate 3                                                  NOT_CERTIFIED
```

The exact next boundary is:

1. eliminate every terminal fixed-s unresolved interval, or dominate its
   positive intercept analytically on the same component carrier;
2. type retained roots by physical-first owner and construct the genuine
   marked current;
3. prove strong-source invariance for all immutable and root-strip
   restrictions;
4. prove operator-norm one-step DQ and common dynamic-test BL convergence;
5. propagate regular, face, product-current, and response types on that same
   physical subatlas;
6. close `FACE_2CUT/FACE_TIME` and the no-`|s|^-1` per-depth estimate.

## 5. Technology boundary

The applicable literature boundary remains unchanged.  Stenlund--Young--
Zhang `arXiv:1210.0011v4` supplies uniform one-time recovery for a compact
moving-table class, not a differentiable future-singularity atlas.
Canestrari `arXiv:2604.19671v2` supplies a closed-map Growth Lemma layer, not
the present finite-`s` branch-record DQ or repeated-cut interface.
Demers--Liverani `arXiv:2606.10155v1`, Problem 8.7, leaves general loss of
memory after characteristic-function restrictions open.  No audited theorem
as of 2026-07-16 replaces the six missing interfaces above.

## 6. Replay and fail-closed behavior

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate3_finite_s_future_singularity_outer_atlas_cert.py \
  deliverables/cm2_gate3_finite_s_future_singularity_outer_atlas_verifier.py

CM2_WORKERS=32 PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_finite_s_future_singularity_outer_atlas_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_finite_s_future_singularity_outer_atlas_verifier.py \
  --self-test

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_finite_s_future_singularity_outer_atlas_verifier.py
```

The independent clean full replay reproduced the three frozen digests above
and passed integrity in `15:21.60`.  The eleven-mutation self-test also exits
zero.  The live default prints only the certified outer-atlas layers, keeps
the complete future atlas, physical current, `MT_DQ`,
`FACE_2CUT/FACE_TIME`, and Gate 3 `NOT_CERTIFIED`, and exits `2` by design.
