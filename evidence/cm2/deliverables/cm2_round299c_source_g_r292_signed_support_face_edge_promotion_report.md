# Round299-C Source-G R292 signed-support face-edge promotion

## Outcome

Round299-C passes as an independently verified formal component-edge package.
The independent verifier reconstructs the complete signed-support
classification from pinned mathematical sources before opening any Round299-C
candidate ledger or result.

The exact census is:

| class | count |
|---|---:|
| Round292 refinement cells | 11,852 |
| same-chart, same-physical-t-sign face classifications | 43,092 |
| accepted positive-area physical patches | 29,948 |
| accepted nonself raw edge witnesses | 27,856 |
| canonical nonself occurrence-edge pairs | 25,452 |
| accepted self-endpoint contacts with zero edge credit | 2,092 |
| rejected contacts with exact exclusion evidence | 13,144 |
| unresolved contacts | 0 |
| endpoint pairs having both accepted and rejected faces | 4 |

The four mixed endpoint pairs use the frozen `EXISTS` contract: one exact
positive-area patch with strict positive-volume corridors on both sides is
sufficient for the pair, and a rejected face for that same endpoint pair does
not negate the accepted witness.

## Independent reconstruction boundary

The verifier is
`cm2_round299c_source_g_r292_signed_support_face_edge_promotion_verifier.py`
with SHA-256
`21d6bd3fd99d7b4717f831becbc1afacd7fd41a076a9d540ec115582736175a6`.
It:

1. never imports, executes, or parses the Round299-C producer;
2. uses the producer bytes only as the inert fixed SHA-256
   `4c8209f283709649c2a969bbc98b2efe080afb8b760b0d246a0a00501c871920`;
3. does not read the persisted Round299 probe ledger or result as an expected
   classification oracle;
4. calls the fixed Round299 mathematical classifier source, SHA-256
   `d6cae0b9ede704b7da57fd9c37b8097919e01592482a8a0eee63fd4a27178b24`,
   directly on pinned Round174/179/274/275/287/292/294/295A/296/297 inputs;
5. completes all 43,092 expected classifications and all three derived formal
   ledgers before opening the Round299-C candidate artifacts; and
6. then demands both exact object equality and deterministic JSON/GZIP byte
   equality.

The replay uses Python 3.12.3, `python-flint==0.9.0`, 512-bit Arb precision,
256-bit square-root construction, and 512-bit square-root replay.

## Witness validation

Every accepted raw witness is rebound to its source classification row and
validates:

- a canonical, distinct formal-occurrence endpoint pair;
- an exact positive-area transformed coordinate-face patch;
- exact left and right positive-volume corridors;
- equality of each corridor's tangential footprint with the accepted patch;
- the strict left/right inward interval relation;
- exact corridor volume;
- square-root enclosure-certificate digest closure;
- nonempty dyadic shrink-trace digest closure and final-trace binding; and
- inherited full support or an exact active-factor strict-support replay.

Every canonical row recommits its accepted raw witnesses and source
classification rows, records any rejected faces for the same pair, and grants
exactly one formal component-edge credit under `EXISTS`. Every self or
excluded contact is separately frozen with zero witness and edge credit.

The new canonical pairs have zero intersection with the already frozen
channels:

| existing channel | intersection |
|---|---:|
| Round295A lower continuation | 0 |
| Round296 true seam | 0 |
| Round297 ordinary face | 0 |

## Exact candidate equality

The independently reconstructed files equal the existing candidate objects
and deterministic bytes:

| artifact | SHA-256 |
|---|---|
| classification inventory | `2b7afa578911a701bf72e9d04032cd179bec3b7f86163530561d6fe81c53faa3` |
| accepted nonself raw witnesses | `3e05e96d98ef5b72c3cdd4d4fd63047fd9636281354997b3d4a9dfc6480aa150` |
| canonical occurrence-edge pairs | `e63f164bf9cc559ec8d3a2895e66493933b43b90f1ad3b163dfb41e12bb04df1` |
| self and exclusion ledger | `cc9583b5a00db9f4c727c95692db7a356b1d37a443074b28610a3e6822168b96` |
| result file | `7954669c0cc421732b28277ae2c03cacd6fbd70d9c5575765a5c087b7c65c5f4` |
| result self-closure | `36a484e614fb0d660062fa1b7529afb0d5f6ca0fd617955bebcf47ce650a4b8c` |

The producer, four candidate ledgers, result, and historical producer
self-attack suite were not changed.

## Independent attack rejection

The historical 22-case producer self-audit is preserved separately:

```text
file SHA-256
61de25264720cca43a3ca72ae0db241c6f09624c70ce9f34eef83340e802d45e

self-closure
c0a859150234b7af5da01934d3ac0551b0ab85508d57b0bac57703752f94d071
```

The independent verifier adds 56 attacks:

| attack class | rejected |
|---|---:|
| reclosed semantic and inventory forgeries | 46 |
| strict JSON/encoding attacks | 4 |
| strict/deterministic GZIP attacks | 3 |
| symlink, hardlink, and path-traversal attacks | 3 |
| total | 56 |

All 56 are rejected and none is accepted. The independent commitments are:

```text
independent attack-suite file SHA-256
ca1bfdf6c8c7199dc7f834b64ece75121bf9bf09747384b610fb68ba21c6696d

independent attack-suite self-closure
16bc87111e88a157c047a4302f7bab410b96d2fce72d5a2c3548fb613b476d28

verification file SHA-256
82a96d122f6b3059d390d5864b99ff2d58e2720da9b0677bdd06012adaf02853

verification self-closure
5b6db1069e140b1c5bf8eeb01ee9bc3790de1fef32757bae568858fcc1b72fb1
```

## Dual-seed cacheless replay

The final verifier was run twice with distinct seed and `PYTHONHASHSEED`
values. The first run wrote the two independent audit artifacts; the second
used `--no-write` and required exact equality with those persisted bytes.

| replay | seed / hash seed | wall time | maximum RSS |
|---|---:|---:|---:|
| first | 299351 | 586.58 s | 9,065,792 KiB |
| second, `--no-write` | 299953 | 583.17 s | 9,067,228 KiB |

Both runs emitted the same independent attack file/self and verification
file/self commitments. The exact commands are recorded in the cold-replay
document.

## Formal credit and nonpromotion boundary

Round299-C grants:

| formal credit | value |
|---|---:|
| raw component-edge witness credit | 27,856 |
| canonical component-edge credit | 25,452 |
| occurrence-identity collapse credit | 0 |
| DSU rank-reduction credit | 0 |
| maximality credit | 0 |
| fibre credit | 0 |
| global-disposition credit | 0 |

No component DSU is applied, no current quotient-component count is asserted,
and no maximality, fibre, global disposition, D02, or CM2 promotion follows
from this package alone. CM2 remains no-go pending the combined DSU and
maximality gates.

