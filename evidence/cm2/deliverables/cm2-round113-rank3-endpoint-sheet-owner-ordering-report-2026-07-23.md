# CM2 Round113 — endpoint-sheet physical owner ordering

Date: 2026-07-23  
Verdict: **VERIFIED on all sixteen regular relative-interior endpoint sheets; CM2 remains NO-GO.**

## Result

Round113 upgrades the Round112 selected-collision root sheets to physical
next-owner sheets on their regular relative interiors:

- 8 HIT sheets and 8 BYPASS sheets;
- 16/16 sheets closed;
- 72 closed proof boxes, 0 residual boxes;
- 12,168 independently replayed candidate rows (`57 + 55 + 57` on each box);
- 216 independently replayed official legs, three per proof box;
- 8 natural boundary/trace rows;
- one unique regular third owner and one unique three-key official path on each
  whole local sheet.

Certificate result digest: `33f564bd6afea1ba346ed0048a4bc61fa1a1bf91ebbbac546a32b051643bda67`  
Verification result digest: `c87d20aee8d652f45a52ca4bd8e9b58753de536036ec6373b2067ef381c972b9`

This pays **complete candidate classification plus a unique next owner**.  It
does not pay a pairwise total order among all candidates.

## Candidate source audit

The immutable candidate universe is the frozen Gate3 retained-lift table,
translated by the Round26 helper after materializing the generator as a tuple.
The three legs have different universe sizes:

```text
source G leg:          57 candidates
first-owner W leg:     55 candidates
second-owner G leg:    57 candidates
```

The source audit explicitly preserves the earlier corrections:

- Round79 supplies algebraic tangency/carrier seeds, not a physical sheet order;
- Round98 found that the historical membership test consumed a generator;
- Round99 requires a full immutable-table replay for every physicality label;
- Round107's complete tables and owners cover only 24 local witness germs;
- Round108's official paths cover only fixed-`s=0` local witness boxes.

No Round107 or Round108 whole-sheet claim is inherited.  Round113 recomputes
the complete tables and official words on its own root-sheet cover.

## Root-graph and strict-owner proof

For every dyadic parameter box, the verifier checks strict opposite signs on
two constant-`t` faces and one strict sign of `partial_t F`.  The stored root
face is expanded by the explicit rational amount `10^-9`; therefore the
unique implicit root remains stable under the independent 640-bit replay.

On each of the three legs, every candidate is classified as a strict
whole-line miss, a strict behind intersection, or a strict future near root
on the regular relative interior.  The selected owner is then compared with
every other future near root.  The smallest stored lower owner-gap bound over
all 216 legs is greater than `0.248896`.

The same proof boxes also certify:

- `0 < flight < 3` on all three selected legs;
- no simultaneous obstacle collision;
- fixed collision charts, with global stored chart-dominance lower bound above
  `0.001771`;
- source-chart dominance above `0.866192`;
- no grid-wall endpoint or vertical/horizontal corner tie;
- one ordered clean-wall record and one official Gate5 key per straight leg.

An official rank-three path is therefore three official keys, not one owner
tuple.  All 16 endpoint sheets have distinct three-key path IDs.

## HIT and BYPASS owners

The HIT-side third owner is the designated candidate.  The BYPASS-side
designated candidate is a strict miss only for `b3>0`; the actual regular
third owners are:

| corner | HIT owner | BYPASS owner |
|---:|---|---|
| 0 | `W[1,-1]` | `G[2,-1]` |
| 1 | `W[1,0]` | `G[2,1]` |
| 2 | `W[-1,1]` | `G[-1,2]` |
| 3 | `W[0,1]` | `G[1,2]` |
| 4 | `W[-1,-2]` | `G[-1,-2]` |
| 5 | `W[0,-2]` | `G[1,-2]` |
| 6 | `W[-2,-1]` | `G[-2,-1]` |
| 7 | `W[-2,0]` | `G[-2,1]` |

Each HIT sheet closes in one proof box.  Each BYPASS sheet uses eight depth-3
proof boxes to obtain a strict interval collision-chart enclosure; its owner
and official path are nevertheless constant across all eight boxes.

## Natural boundaries are not regular cells

Every corner has a separate natural-boundary row with three strata:

1. `c0=0`: source-grazing edge;
2. `c3=0` / `b3=0`: shared designated-third tangency edge;
3. `c0=c3=b3=0`: double-grazing corner.

The closed proof boxes provide one-sided enclosures up to these strata, but
regular owner and official-word claims apply only on

```text
HIT:    c0>0 and c3>0,
BYPASS: c0>0 and b3>0.
```

In particular, no box containing `b3=0` calls the designated candidate a
strict miss.  At `b3=0` it is a future tangency and is owned by the trace
ledger.  It precedes the BYPASS regular winner by a stored separation whose
global absolute lower bound exceeds `0.293955`; when `b3>0`, that designated
root disappears and the listed G-lift becomes the next collision.  HIT
`c3=0` is likewise a tangency boundary, not a transverse regular collision.

Artificial dyadic boundaries use the exact convention `[lower,upper)` in
each coordinate, except that a leaf ending at the outer domain endpoint owns
that endpoint.  The verifier checks the exact rational cover, including all
grid vertices and edge probes.

## Independent verification

The independent verifier does not import the Round113 producer or engine.  At
640 bits it recomputes:

- all 16 implicit root sheets;
- all 72 proof boxes;
- all 12,168 candidate classifications and strict next-owner comparisons;
- all 216 clean-wall/official-key legs;
- 1,144 stored numeric-enclosure containments;
- all eight natural boundary rows and the half-open cover.

It rejects 12 re-signed semantic/schema attacks and 3 strict-JSON attacks.
Direct upstream byte pins include the core geometry, Gate3/26 candidate
source, Round28 official registry helper, Round76/79 formulas, Round112, and
the audited Round79/87/94/98/99/100/107/108 artifacts.

## Strict nonclaims

- No pairwise total order of all 57 third-leg candidates is claimed.
- No regular owner or official word is applied on a natural grazing edge.
- These are local endpoint sheets, not a whole grazing-trace collar.
- No countable homogeneity-tail theorem is installed.
- No canonical standard-curve recut or actual child ID is installed.
- No Gate5 child field is installed; Gate5 remains `10/18`, blocks `0`.
- Round113 does not repair the remaining Round101 seam-to-grazing chain.

## Next core gate

The next legal step is to intersect these owner/word-constant regular sheets
with exact source and actual-collision homogeneity strips.  HIT needs the
double `(j,k)` angle index; BYPASS must use the cosine coordinate of its actual
G-lift collision, not the analytic miss coordinate `b3`.  Only after the
official three-leg flow is recut along actual standard curves may the first
cell-keyed Gate5 field `F1` be installed.
