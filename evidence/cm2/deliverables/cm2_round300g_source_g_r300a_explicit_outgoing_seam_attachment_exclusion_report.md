# CM2 Round300-G — explicit outgoing-seam attachment exclusion

## Outcome

Round300-G closes the exact `128`-row explicit-witness subset of the
Round300-A `3,232` canonical graph-zero pair frontier.

The formal result is fail-closed:

- `128/3,232` Round300-A canonical pairs have the named R295-A explicit
  two-sided lower graph-sheet witness;
- all `128` are traced through R293, R291, R182, R279, and the two R294
  endpoint atoms;
- all plausible R246/R247 retained-stratum attachment candidates are
  exhausted;
- zero rows prove a one-sided included-owner attachment;
- zero rows are eligible for component-edge or DSU application.

This is a coverage/exclusion gate.  Its eligible edge channel is explicitly
empty.

## Exact selected subset

The complete Round300-A ledger is reopened, not sampled.  Its `3,232`
canonical rows split exactly into:

- `128` rows with
  `R295A_explicit_lower_graph_sheet_witness_present = true`;
- `3,104` other rows.

The selected subset closes as:

- `128` R295-A physical-incidence binding rows;
- `128` R293 exact two-sided graph-sheet bindings;
- `48` R291 outgoing-chart-seam dispositions;
- `128` selected physical witness cells;
- `128` clipped R182 graph-sheet leaves;
- `56` distinct R179 retained children;
- `48` distinct containing R174 origins;
- `256` distinct R294 endpoint occurrences;
- `256` distinct R279 atoms;
- `44` distinct complete ten-field return signatures.

The source-chart histogram is exactly `32` in each of `G:E`, `G:N`, `G:S`,
and `G:W`.

## Why signature matching cannot select an attachment

Exact full-signature matching against R246 and R247 produces `19,884`
endpoint-node relations:

- `18,108` R246 relations over `2,044` distinct nodes;
- `1,776` R247 relations over `216` distinct nodes.

The directional candidate multiplicity per canonical pair is highly
non-unique:

| endpoint candidate counts | pair count |
|---|---:|
| `80|55` | 31 |
| `132|160` | 27 |
| `160|132` | 17 |
| `55|80` | 13 |
| `9|2` | 10 |
| `2|11` | 8 |
| `11|2` | 8 |
| `2|9` | 6 |
| `25|64` | 4 |
| `64|25` | 4 |

Thus signature equality is a candidate generator, not an owner selector.

The R247 signature candidates split into `844` relations whose source-seam
status says `E_OR_W_HALF_OPEN_OWNER` and `932` whose status says
`N_OR_S_EXCLUDES_DIAGONAL_TIE`.  This status still cannot select an
attachment without the required ancestry and geometry.

## Complete ancestry exclusion

The complete R220 table contains `13,076` one-step split interfaces.
Against that full table:

- `0/56` selected R179 leaf children occur as an interface endpoint;
- `0/48` selected containing origins occur as an interface origin.

Every signature-matching R246/R247 node is independently traced through its
own R232/R238 whole-origin promotion and R220 interface.  Those interfaces
belong to other retained children and other origins.  Therefore no missing
direct-ID join is silently replaced by a count-based or same-signature
ancestor claim.

## Complete geometry exclusion

Every endpoint's whole R182 leaf box and strict positive-volume R294 inner
support box is compared with every exact-signature R246/R247 candidate box.

R247 is completely disjoint:

- `1,776/1,776` whole-leaf comparisons are disjoint;
- `1,776/1,776` inner-support comparisons are disjoint;
- zero closed contacts and zero strict positive-volume intersections.

R246 has no strict positive-volume intersection:

- whole-leaf comparison: `18,076` disjoint and `32` closed-boundary-only;
- inner-support comparison: `18,092` disjoint and `16`
  closed-boundary-only;
- zero strict positive-volume intersections.

At pair level:

- `96` pairs have no geometric contact;
- `16` have a whole-leaf closed contact only;
- `16` have both whole-leaf and inner-support closed contacts only.

All `32` closure-only contacts have different origins from their candidate
node.  None uses the selected child as the candidate R220 interface
endpoint.  Of those contacts, `24` merely share a parent and `8` do not even
share a parent.  Closure contact alone is not a connectivity or attachment
lemma.

## Strict nonpromotion

Every ledger row fixes all of the following to zero or false:

- component-edge credit;
- component-union and DSU-rank-reduction credit;
- occurrence-identity-collapse and seam-edge credit;
- maximality, fibre, and global-disposition credit;
- endpoint owner-attachment credit;
- signature-only and closed-contact selection eligibility;
- eligibility for component DSU application.

The Round300-G disposition is:

```text
NO_ROUND220_ANCESTOR_INTERFACE__
NO_STRICT_VOLUME_INTERSECTION__
CLOSED_CONTACT_INSUFFICIENT
```

## Independent verification and attacks

The independent verifier never imports, executes, parses, or tokenizes the
producer.  It treats the producer only as inert hash-pinned bytes.  It
reconstructs the complete expected ledger and result from thirteen pinned
upstream artifacts before opening either candidate file.

All `43/43` attacks are rejected:

- `34` fully recommitted semantic attacks, including every forbidden credit,
  forged owner/interface/intersection claims, signature-only and
  closed-contact promotions, lineage/box/candidate-commitment forgery,
  row drop/duplicate/reorder, and result-level overclaims;
- `9` parser/path and independence attacks covering duplicate keys,
  nonfinite numbers, NUL input, malformed GZIP, trailing JSON, and attempted
  producer import/execute/parse.

## Artifact commitments

| artifact | SHA-256 |
|---|---|
| producer | `8fabd80fc6c7fe6f4c3b3f133d18b05ed3532443204d7f9442ddfec1b9167ed8` |
| exclusion ledger | `84b4e855cd95867758cd87a88f0ef55b712218999166796712495d70602bb61b` |
| result file | `5693f64262623dccbdc0138edc7dc876b06b2822f552eee26ac580c27f861c1c` |
| embedded result | `4b4be63fc29c22f567934431088a5edce1746d353e6ef199359319ae26b71f15` |
| verifier | `2b3a241ed3769273113d17f3907007da57626f7eb3e5f7b75eb107b833b1f9a9` |
| attack-suite file | `d416db01cccaf14a46ad0c8207c0045716533d37055aa98cc36f6acbff6f4dff` |
| embedded attack suite | `55de38ef3dc2ed4d4bed943c82c3e7e877940fd55da0d49ace98be600af1f07f` |
| verification file | `2416d2efe04935fddc615c5542b1f0f0c56411111152d5e27d1021c59d8782ff` |
| embedded verification | `390664db253c6046272b10bf993c6a4f5bd5a5f6ef4235b913af8d901b22a44b` |

## Downstream consumption

Round301 may consume all `128` rows as a sealed coverage/exclusion channel
with `eligible_edge_channels = ()`.  It must not extract an edge, union, or
rank-reduction credit from this package.
