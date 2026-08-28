# CM2 Gate 3 continuation: candidate reduction and first-hit machinery

Date: 2026-07-15  
Scope: rational two-disk torus pilot on the standard solid-boundary section
`N=G disjoint-union W`, with white center `(1/2+s,1/2)` and
`|s|<=1/400`.  The frozen v51/v52 manuscripts and the shared research log
were not edited.

## Decision

**Gate 3 remains `NOT_CERTIFIED`.**  The global one-return event inventory,
pair/triple incidence table, DQ assembly and scalar matching are still absent.
This continuation nevertheless closes the first genuinely finite
chart/target reduction and instantiates the first reusable strict-root
comparison engine:

- all `8*162=1296` source-chart/target-lift pairs are classified by an exact
  executable table;
- `848` pairs are rigorously empty and `448` remain conservative candidates;
- each gray source cell retains `57` targets and each white source cell
  retains `55` targets;
- two positive-width three-parameter boxes have fully certified physical
  first targets, including comparison with every retained competitor;
- the generic 256-bit Arb machinery now computes the line-circle
  discriminant, selected incoming root and competing-hit inequalities.

The evidence package is:

- `deliverables/cm2_gate3_candidate_first_hit_cert.py`;
- `deliverables/cm2-gate3-first-hit-atlas-manifest-2026-07-15.json`;
- `deliverables/cm2_gate3_first_hit_manifest_verifier.py`;
- `deliverables/cm2-gate3-first-hit-atlas-manifest-2026-07-15.sha256`.

## 1. Exact conservative reduction on all eight source cells

The previously certified horizon bound is

\[
  \tau_{\max}<3.
\]

Let `c_S`, `R_S` be the source center and radius and let `a_T`, `R_T`
be a target lift.  If the target is hit at time `tau<3`, then

\[
 |a_T-c_S|<3+R_S+R_T.                         \tag{1.1}
\]

Indeed, if `q` is the source point and `x` the target contact, then
`|q-c_S|=R_S`, `|x-a_T|=R_T` and `|x-q|=tau`.  The contrapositive of
(1.1), minimized exactly over `|s|<=1/400`, certifies the first family of
empty chart/target pairs.

There is a second independent necessary condition.  Write the outgoing
source normal as `n` and the target contact normal as `e_T`.  From

\[
 \tau u=(a_T-c_S)+R_Te_T-R_Sn,
 \qquad u\cdot n>0,
\]

one obtains

\[
 (a_T-c_S)\cdot n>R_S-R_T.                    \tag{1.2}
\]

On each dominant-coordinate normal cell `E/W/N/S`, the certificate uses the
exact rational brackets

\[
 \frac{707}{1000}<\frac1{\sqrt2}<\frac{708}{1000}
\]

to bound the support function on the whole cell and on the full parameter
window.  If this rational upper bound is strictly below `R_S-R_T`, (1.2)
cannot hold and the pair is empty.

The complete counts are:

| source cells | retained per cell | empty per cell | self | horizon-distance | outgoing-halfspace |
|---|---:|---:|---:|---:|---:|
| `G:E/W/N/S` | 57 | 105 | 1 | 85 | 19 |
| `W:E/W/N/S` | 55 | 107 | 1 | 93 | 13 |

Thus

\[
 1296=448\ \text{retained}+848\ \text{certified empty}.
\]

The same Euclidean source lift is the single `self` row.  Strict convexity
excludes its re-entry by an outgoing interior ray; other periodic copies of
the same obstacle remain separate target lifts and are not removed by this
argument.  This table covers the phase interiors `|p|<1`; the grazing strata
`p=+/-1` remain separately registered boundaries and are not silently counted
as interior first-hit rows.

Every one of the 1296 ordered classification rows and every one of the eight
ordered candidate lists has a canonical SHA-256 digest in the manifest.  The
verifier reruns the generator and rejects a changed count, label, proof string
or ordering.

## 2. Selected-root and competing-hit interface

On a source chart use

\[
 q=c_S+R_Sn,\qquad
 u=\sqrt{1-p^2}\,n+p,n^\perp.
\]

For `d=a_T-q`, put

\[
 \ell=u\cdot d,\qquad
 \Delta_T=R_T^2-(u^\perp\cdot d)^2.
\]

When `Delta_T>0`, the incoming line-circle root is

\[
 \tau_T^- = \ell-\sqrt{\Delta_T}.              \tag{2.1}
\]

The new root engine evaluates these quantities on Arb boxes and accepts a
physical target only after proving

\[
 \Delta_T>0,\qquad 0<\tau_T^-<3.
\]

For each retained competitor it then proves either:

1. the whole box has no real intersection;
2. the whole intersection lies strictly behind the source; or
3. its positive incoming root is strictly later than (2.1).

This is the exact interface needed by a future adaptive first-hit partition.
At a tangency, the previously certified identity

\[
 |\partial_\varphi\Delta_T|=2R_T\ell>
 \frac{1821}{31250}
\]

supplies the uniform submersion margin once a physical first-tangency row is
selected.

## 3. Two fully certified local first-hit patches

Both patches use

\[
 |t|\le10^{-3},\qquad |p|\le10^{-3},
 \qquad |s|\le1/400.
\]

The full parameter interval is retained in the Arb evaluation.

### 3.1 Gray east cell

On `G:E`, the selected target is `G[1,0]`.  Arb proves

\[
 \frac{279}{1000}<\tau^-_{G[1,0]}<\frac{281}{1000}.
\]

Among the other 56 retained targets, 54 miss the whole line box and 2 have a
strictly later positive incoming root.  Together with the exact exclusions
from Section 1, `G[1,0]` is therefore the physical first target throughout
this nonzero-width box.

### 3.2 White east cell

On `W:E`, the selected target is `W[1,0]`.  Arb proves

\[
 \frac{67}{100}<\tau^-_{W[1,0]}<\frac{69}{100}.
\]

Among the other 54 retained targets, 52 miss the whole line box and 2 are
strictly later.  Hence `W[1,0]` is the physical first target throughout this
second nonzero-width box.

These are physical open first-hit patches, not isolated floating-point
samples.  They do not cover either entire source cell.

## 4. One exact tangency seed already compatible with the interface

The independent quadratic-field certificate
`cm2_gate4_explicit_tangency_cert.py` gives a physical `G:E -> W[0,0]`
first-tangency seed with

\[
 \ell=\frac{\sqrt{610}}{50},\qquad
 \partial_sH=
 \frac{4(25\sqrt{610}-56)}{8425}>0,
 \qquad
 \partial_\varphi H=\frac{4\sqrt{610}}{625}>0.
\]

It instantiates the tangency/submersion side of the interface.  It remains a
single exact seed: no explicit rational/Arb neighborhood cover or immutable
global event row is claimed here.

## 5. What remains before Gate 3 can close

The raw incidence burden after the safe reduction is still large.  If one
formed every pair and triple before further first-hit subdivision, the four
gray and four white cells would generate

\[
 4\left\{\binom{57}{2}+\binom{55}{2}\right\}=12324
\]

pair rows and

\[
 4\left\{\binom{57}{3}+\binom{55}{3}\right\}=221980
\]

triple rows.  The next mathematically useful step is therefore an adaptive
first-hit partition that records a much smaller active target set on each
leaf, rather than blindly materializing these conservative combinations.

The fail-closed manifest still requires:

1. selected-root/first-hit boxes covering all retained portions of all eight
   charts, including the tangency boundaries;
2. complete pair and triple incidence classifications on that refined atlas;
3. parameter continuation across the full `s` window;
4. global DQ assembly, ownership/polarity and restrictionwise scalar-current
   matching.

Accordingly, this continuation reduces the global finite search by 65.4% and
certifies two physical leaf boxes, but does not certify the global event
inventory or unconditional CM2.

## 6. Reproduction

```bash
python3 -m py_compile \
  deliverables/cm2_gate3_candidate_first_hit_cert.py \
  deliverables/cm2_gate3_first_hit_manifest_verifier.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_candidate_first_hit_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_first_hit_manifest_verifier.py --self-test

# Expected exit 2: integrity passes, global completion remains absent.
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_first_hit_manifest_verifier.py
```

The positive certificate and verifier self-test exit `0`.  The live manifest
verifier exits `2` by design and lists the eight still-missing global layers.
