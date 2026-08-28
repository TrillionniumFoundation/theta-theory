# CM2 Round292 — R287 full-registry overlap exhaustion

## Verdict

Round292 independently exhausts the overlap that remained between the
`10,020` conditional Round287 support unions and the complete conditional
`421,804`-row preserved/base-atom registry.

The audit finds `1,564` exact positive-volume coordinate-representation
overlaps incident to `920` Round287 unions.  Exact `(t^2,p,s)` partitioning
removes every covered subcell and reconnects only uncovered cells across exact
identity-local common faces.  The resulting revised conditional R287 census
is:

- `616` source unions fully covered by existing occurrence representations;
- `304` source unions partly covered, each retaining one uncovered connected
  support;
- `9,100` source unions untouched by the registry;
- `9,404` refined, strictly uncovered connected support candidates; and
- `0` unresolved pairwise positive-volume overlaps.

This is a **ZERO-CREDIT** exhaustion.  No occurrence ID, representation alias,
component edge, seam edge, DSU rank reduction, maximality, fibre, disposition,
or `Jx/Jy` same-point-glue credit is issued.

## Independent source reconstruction

The standalone cacheless verifier reconstructs, from frozen Round174,
Round179, Round204, Round208, Round275, Round287, and Round288 inputs:

| Registry tranche | Rows |
|---|---:|
| Frozen preserved occurrences | 126,468 |
| Conditional Round288 new-atom candidates | 295,336 |
| **Conditional base/atom registry** | **421,804** |

It separately reconstructs all `10,020` Round287 unions as `10,668` exact
source support cells:

- `9,128` whole Round275 disjoint-region cells;
- `1,540` nonempty uncovered Round286 cells;
- `892` pre-audit mixed-parent unions; and
- `3,488` frozen mutually-exclusive outer-overlap region pairs.

Registry occurrence IDs are injective.  Matching is restricted to equal
source chart and complete ten-field return-signature digest, followed by exact
open-box overlap in transformed `(t^2,p,s)` coordinates.

## Registry overlap census

The exact shortlist and relation audit gives:

- same-chart/signature candidate groups: `60`;
- support-cell/registry-box shortlist comparisons: `295,720`;
- exact positive-volume representation overlaps: `1,564`;
- incident support cells: `920`;
- incident support unions: `920`;
- cells with multiple containing targets: `0`;
- overlap sources:
  - Round174: `752`;
  - Round179: `812`;
- relation classes:
  - Round287 cell contained in existing occurrence: `212`;
  - existing occurrence box contained in Round287 outer representation: `76`;
  - partial positive-volume outer-representation overlap: `1,276`;
  - exact coordinate equality: `0`.

The `212` contained cells have unique containing targets.  At union level,
`204` unions are wholly contained in one unique target; no union is wholly
contained in multiple targets.  These facts are representation evidence only,
not identity-alias credit.

## Exact refinement and revised conditional census

All overlap boundaries are inserted exactly into the open transformed
coordinates.  The `10,668` source cells become:

| Refined class | Cells |
|---|---:|
| Existing-representation occupied, unique target | 1,600 |
| Uncovered positive open cells | 10,252 |
| **Exact partition cells** | **11,852** |

No occupied cell has more than one target.  Within each source union, exact
positive common faces among uncovered cells produce local connectivity rank
`848`, hence:

```text
10,252 uncovered cells - 848 local identity faces
  = 9,404 refined connected support candidates.
```

The component-size histogram is:

- size 1: `9,124`;
- size 2: `80`;
- size 3: `12`;
- size 4: `88`;
- size 5: `84`;
- size 10: `16`.

Exact transformed volume is conserved:

```text
source volume = occupied volume + uncovered volume = refined volume.
```

The occupied volume is
`280061969321/13421772800000000`; every other volume commitment is retained
exactly as a rational string in the frozen result and ledger.

The full pairwise support audit performs `231,880` exact shortlist
comparisons.  It finds:

- same-union positive overlaps: `0`;
- distinct unresolved positive overlaps: `0`;
- physically active frozen mutually-exclusive overlaps: `0`.

Thus the prior conditional Round292 promotion arithmetic must be revised:

```text
conditional new Round288 atoms       295,336
conditional refined Round287 supports  9,404
conditional total new occurrences    304,740

frozen preserved occurrences         126,468
conditional registry total           431,208
```

These are downstream promotion inputs, not formal credits of this round.

## Ledger commitments

The deterministic ledger contains `22,820` rows:

- registry-overlap rows: `1,564`;
- exact refinement rows: `11,852`;
- refined new-support component rows: `9,404`;
- positive-overlap pair-audit rows: `0`.

Commitments:

- rows SHA-256:
  `556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055`;
- deterministic gzip SHA-256:
  `8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab`;
- result file SHA-256:
  `f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508`;
- embedded result-object SHA-256:
  `f6bc26c2a7f674901e411342ce388b5c2a9e8facc9a253ce244375bcf7e47372`.

## Standalone independent verification

The verifier pins the producer only as inert bytes and never imports or
executes it.  It completes the entire expected registry, overlap,
refinement, connectivity, pairwise audit, ledger, and result reconstruction
before the first read or hash of the candidate result or ledger.

It then requires:

- exact candidate result-object equality;
- exact candidate ledger-object equality;
- exact deterministic gzip-byte equality;
- every row's independent SHA-256 closure;
- every formal credit field equal to zero; and
- all frozen census and conservation identities.

The verifier rejects `31/31` targeted re-signed attacks, including row-level,
ledger-level, result-level, coordinated row→ledger→result, forged DSU/
quotient/`JxJy` credit, and alternate-gzip-header attacks.

Independent verifier cold replays with
`PYTHONHASHSEED/--seed = 292071` and `292929` are byte-identical.

Commitments:

- verifier source SHA-256:
  `9efd78054cdde8172b016a684951395f1ca96958412122034dfc1971312ea010`;
- verification JSON file SHA-256:
  `7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd`;
- embedded verification-object SHA-256:
  `608a3d0e93df4f4849f8efb83715ac04d7317d13f2732e101d5d3c7ef5ae9a39`.

## Frozen nonpromotion baseline

- expanded occurrences: `126,468`;
- quotient components: `63,224`;
- maximality: `0/63,224`;
- exact-key fibres: `0/116`;
- global dispositions: `0/224,580`;
- Gate5: `10/18`;
- D02: `BLOCKED`;
- CM2: `NO-GO_FOR_CLAIM`;
- occurrence credit: `0`;
- representation-alias credit: `0`;
- component/seam/DSU-rank credit: `0`;
- `Jx/Jy` same-point glue credit: `0`.

## Required next

The Round292 occurrence-promotion transaction must consume the revised
`9,404`, not the pre-exhaustion `10,020`, Round287 support census.  It must
independently issue or bind occurrence identities atomically while keeping
component and seam DSU rank at zero.  True-seam edge reconstruction, final
DSU, maximality, all `116` fibres, and all `224,580` global dispositions
remain downstream gates.
