# CM2 Round 117 — countable homogeneity operator cells

Date: 2026-07-23  
Verdict: **VERIFIED exact countable operator-cell generator on all 72 Round113 parent regions; actual standard-curve children remain unbuilt.**

## What Round117 pays

Round117 installs the exact `q=2` homogeneity partition

```text
H_n = (sin((n+1)^-2), sin(n^-2)],  n >= 128.
```

The rational local square extends to `1/16384`, strictly beyond
`sin(128^-2)`.  The nonempty difference is retained as the central/outer
class `H0=(sin(128^-2),1/16384]`; it is not discarded by a finite cutoff.
The symbolic monotonicity, adjacency, limit, union, and unique-index formula
pay the entire infinite tail.

All 72 Round113 parent proof boxes are refined:

- **8 HIT parents** use independent source and actual-third labels `(j,k)`
  with four exact tail/central-outer generator families;
- **64 BYPASS parents** use a source label only, because analytic `b3` is not
  a collision angle;
- the actual BYPASS G-winner is recomputed on every parent and is strictly in
  central `H0` throughout all **64/64** parents;
- total finite generator-family templates: **112**;
- parent regions with nonempty source central/outer intersection: **24**;
- natural trace-ledger rows: **8**.

Artificial boundaries use a unique half-open owner: `b(n)` belongs to `H_n`.
Natural zero-angle boundaries remain in the singular trace ledger.  Stable
operator-cell IDs use exact integer label codes and Cantor pairing.

## Independent verification

- producer precision: **512 bits**;
- independent verifier precision: **640 bits**;
- producer imported by verifier: **false**;
- parent regions independently rejoined: **72/72**;
- HIT parent schemas and stable IDs rechecked: **8/8**;
- BYPASS winner geometry and strict H0 membership recomputed: **64/64**;
- symbolic generator-family templates rechecked: **112/112**;
- directed boundary queries re-enclosed: **6/6**;
- natural trace-ledger rows rechecked: **8/8**;
- hostile semantic mutations rejected: **6/6**;
- strict-JSON attacks rejected: **3/3**;
- producer and verifier cold replays: **byte-identical**.

## What remains open

The output is an exact two-dimensional root-graph/operator-cell generator,
not an actual parent-`W` standard-curve join.  It installs no adapted-arclength
recut and no Gate5 F1--F6 child field.  Whole-trace collars and quantitative
reach/self-separation remain open.

Gate5 remains **`10/18`**, with zero complete blocks.  CM2 remains
**`NO-GO_FOR_CLAIM`**.
