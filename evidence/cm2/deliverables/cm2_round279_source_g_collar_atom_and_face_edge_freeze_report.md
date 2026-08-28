# CM2 Round279: collar-atom and common-face witness freeze

## Certified scope

Round279 formally freezes the local collar frontier, while deliberately
awarding no occurrence or DSU credit.

- The `332,020` frozen signature rows from Rounds
  208/269/270/271/272 quotient to exactly `332,016` canonical
  `(Round182 leaf, complete signature)` atoms.
- The only contractions are the `4` Round271 artificial `t`-split aliases.
  Each is backed by an exact complete common face and two strict-negative
  inward corridors.
- Exactly `36,040` atoms retain existing Round208 occurrence backing.
  The other `295,976` are frozen occurrence-region *candidates*, not promoted
  expanded occurrences.
- The true-support common-face universe contains exactly `330,724` edges.
  Every edge has one exact positive-area face patch and two geometrically
  oriented positive-volume inward corridors (`661,448` corridors total).

The exact disjoint witness partition is:

- `240,932` `DEPTH4_ADAPTIVE_STRICT_PATCH`;
- `57,124` `DEPTH8_SAFE_PRUNED_STRICT_PATCH`;
- `32,416` `ACTIVE_GRAPH_SIDE_STRICT_PATCH`;
- `252` `P_ENDPOINT_WEDGE_STRICT_PATCH`.

Thus the local common-face residual is zero.  Round268 true-seam edges and
all cross-chart DSU operations remain outside this freeze.  Jx/Jy still
receive zero same-point glue credit.

## Cacheless production and replay

The formal depth4 materializer and combined producer reconstruct the
candidate universe from the frozen R182 and R208/269/270/271/272 inputs.
They contain no `pickle` import and no read of the historical unpinned
Round277 `/tmp` cache.

For the adversarial replay, that cache pathname was replaced by a directory,
so any legacy read would have raised `IsADirectoryError`.  Cacheless depth4
materialization still reproduced the same `240,932` rows byte-for-byte.
Combined seeds `279071` and `279929` then reproduced the certificate and both
large attachments byte-for-byte:

- certificate SHA256:
  `ef60a40cc05d47b3d899b73169017bee8e246583ce51a5b543f1b1a1047f064e`;
- atom attachment SHA256:
  `283a10799e0c7d1156695c30cdb2533488602ca646a18804f93211c0a3132dbe`;
- edge attachment SHA256:
  `bc1b976c0609c3271690e3d52c9bae85571f1a7661f404d7bc2e65bb707a2695`;
- certificate result SHA256:
  `628b07e56a6aa7ecdbdfde95f184a3a3c0ad1eb5a5addb84588e960a87af1677`.

## Independent verification

The independent verifier does not import the Round279 producer.  It rebuilds
all canonical atoms and the full true-support candidate universe from pinned
inputs, rechecks all four aliases with the Round179 interval evaluator, and
calls the pinned Round174 dynamic evaluator on every one of the `330,724`
face patches and all `661,448` corridors.

It also enforces strict single-document JSON, single-member GZIP, duplicate
key and nonfinite-number rejection, compressed/uncompressed size limits, and
HERE-only regular non-symlink/non-hardlink attachment paths.  Nineteen
semantic and parser/path attacks are required to be rejected, including
row reorder/drop, orphan endpoint, corridor-side swap, zero-area patch,
forged credit, cache-source injection, duplicate/NaN/trailing JSON,
trailing/oversize GZIP, symlink, hardlink, and path escape.

Final verification status and SHA256 are filled only after the complete
dynamic replay:

- status: `PASS_INDEPENDENT_ROUND279`;
- verification SHA256:
  `a4cd7a96a43a9011e223d230c9f604f567fa56f1b095403cf802261daab5de21`;
- attacks: `19/19` rejected.

## Strict non-promotion

Round279 grants zero expanded-occurrence, component-edge, DSU rank reduction,
maximality, exact-key fibre, global-disposition, and Jx/Jy same-point credit.
The pre-existing strict baseline therefore remains:

- quotient components: `63,224`;
- expanded occurrences: `126,468`;
- maximality: `0/63,224`;
- exact-key fibres: `0/116`;
- dispositions: `0/224,580`;
- Gate5: `10/18`;
- D02: `BLOCKED`;
- CM2: `NO-GO_FOR_CLAIM`.

The next gate may consume these atoms and face witnesses only after separately
materializing legitimate physical occurrences, completing reverse-rechart and
Round268 seam incidence, and then rebuilding the DSU.
