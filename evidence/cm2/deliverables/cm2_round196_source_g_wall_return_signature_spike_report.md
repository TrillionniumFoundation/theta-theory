# CM2 Round196 wall-G side-specific return-signature spike

## Verdict: VALIDATED

Question: do the 96 strict open regions from Round192's 32 two-sheet wall
pairs have unique side-specific local return signatures and exact immutable
word-key bindings, with only the expected signature change across each source
or target sheet?

Yes, as a frozen-evidence feasibility result:

- unique signatures: `96/96`
- conflicts: `0`
- missing signatures: `0`
- pair glue: `32/32`
- unexpected cross-sheet changes: `0`

Each pair has the exact pattern

`empty word → one recorded X/Y wall event → empty word`.

The owner target, outgoing cell, and target chart remain unchanged.  Crossing
either the source sheet or the target sheet inserts or removes only the same
single wall event.

This is not a production certificate.  No signature row, whole tube, or
global exact-key disposition is promoted.

## Frozen evidence

The probe pins and checks every manifest entry, certificate result,
attachment result, and verification result in the complete Round174,
Round179, and Round182 chains.  It also reconstructs the immutable Gate5
registry through the pinned Round174 verifier and byte-for-byte reconstructs
the Round192 geometry evidence:

- Round192 leaf rows:
  `64`,
  SHA256
  `4702ad9ef4a0522d77796924c3ddc5ed075584f887059858d8350b3d81b26492`
- Round192 pair rows:
  `32`,
  SHA256
  `f93a25e1f322bb202c0db99e86357c9b4d7a1940a0ed691a8e508e83a5a9c732`

Probe-only caveat: importing Round192 imports Round182, Round179, and Round174
before their bytes can be pinned.  This is a frozen-workspace feasibility
probe, not an adversarial verifier.

## Why the signature inference is determined

The 64 relevant origins lie in 16 Gate3 parents.  Every origin has a genuine
face-adjacent Round174 resolved occurrence:

- 32 origins have one adjacent resolved anchor;
- 32 origins have two;
- shared-face axes: `t = 64`, `p = 32`.

All adjacent anchors agree with the sole exact key observed in their Gate3
parent.  That anchor has:

- no wall event;
- empty signed wall word;
- roof `1`;
- one fixed owner target, outgoing cell, and target chart.

The probe independently reruns the Round174 signature evaluator over all 512
relevant Round182 leaf enclosures.  Every one fails for exactly one reason:

- `wall_endpoint_or_count_transition:X:0`: `256`
- `wall_endpoint_or_count_transition:Y:0`: `256`

No owner, root, return-time, outgoing-chart, other-wall, or event-order reason
is present.  Round179 supplies 64 matching source/target regular wall normal
forms.  The active origins have no Round182 carried-normal-form rows; that
absence is explicitly not used as positive evidence.

Therefore, after the Round192 sign arrangement splits away the one recorded
wall zero:

- equal source/target signs give the anchored empty word;
- negative source to positive target gives `X+` or `Y+`;
- positive source to negative target gives `X-` or `Y-`;
- a one-event word has a unique order;
- the pinned immutable registry supplies exactly one official key.

The one-event keys are registry-derived from certified sign changes.  They
were not already observed as resolved rows inside these 16 partial parents.

## Tail result

The 96 Round192 tail regions have:

| signed word | regions |
|---|---:|
| empty | 64 |
| `X+` | 8 |
| `X-` | 8 |
| `Y+` | 8 |
| `Y-` | 8 |

All 32 pairs preserve the outcome-blind owner:

- positive-`t` owner pairs: `32`
- negative-`t` shadows: `32`
- pair pattern: `empty / one event / empty`
- pair-glue rows SHA256:
  `934ad2940f6e0fc104397545ae1d2b2ae15da86a2b3d996b01c448bd33d62f03`
- 96 region rows SHA256:
  `27e6286ce8fc562f7d21ed8fc7f8b102d11b9fd9776519b897542d21ee3e8c4a`

## Full 64-origin feasibility

Applying the same single-obstruction rule to all 512 Round182 leaves gives
736 strict open regions:

- unique: `736`
- conflicts: `0`
- missing: `0`
- 32 boundary-side origins: `8` regions each
- 32 target-graph-side origins: `15` regions each

The full word histogram is:

| signed word | regions |
|---|---:|
| empty | 512 |
| `X+` | 56 |
| `X-` | 56 |
| `Y+` | 56 |
| `Y-` | 56 |

Thus all 64 origins are feasible for complete local replacement.  Officially
materialized fully-local-replaced origins remain `0` until a producer emits
the complete rows and an independent verifier rebuilds them.

The inferred 736-region rows SHA256 is
`156f0caa371d6f736e319b3164e3982cd074dff564a59f780b7af3bb5fe589b1`.

## Exact-key fibre join

Every local region joins exactly one immutable registry key.  The 96 tail
regions touch 12 distinct keys:

- four empty-word keys with 16 local regions each;
- eight signed one-event keys with 4 local regions each.

Over all 736 regions, the same 12 keys have:

- four empty-word keys with 128 local regions each;
- eight signed one-event keys with 28 local regions each.

The 12 ordinals are:

`18715, 18716, 18717, 70920, 70921, 70922, 128050, 128059, 128060,
186165, 186174, 186175`.

This many-to-one local join does not exhaust any global exact-key fibre.
Consequently it does not produce a global disposition.

- tail fibre rows SHA256:
  `0c6bd2dc742f3de601bd2127531ac4651a9cdc7ecd8979f4cf863e2a7231631b`
- all-origin fibre rows SHA256:
  `320966dc2e09608f80acd6f2955af9a043b0a726de483f5d2f6c8043f4ec470d`

## Reproduction

Probe:

`cm2_round196_source_g_wall_return_signature_probe.py`

Probe SHA256:

`870f4ae54d06be2a44466f3eadb3354644cb7f842b9446348bbc98d3dc7eb656`

Command:

```bash
/usr/bin/time -v -o /tmp/cm2_round196_seed196052.time \
  env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=196052 \
  .venv-neurips/bin/python \
  deliverables/cm2_round196_source_g_wall_return_signature_probe.py \
  > /tmp/cm2_round196_seed196052.json
```

Measured:

- exit: `0`
- elapsed: `1:24.27`
- user/system: `81.11 s` / `3.14 s`
- maximum RSS: `873,860 KiB`
- output SHA256:
  `3e30c5816edf8a8e4cfd43d16c85b1c0e9494eaea65c4576ffa1e28e3e924d26`
- result SHA256:
  `9c71151a7994618039a38b600bde549c0f8489e6def9537c5501bc31a87d4a78`

`py_compile`, the read-only AST audit, and an independent post-run canonical
result-digest check passed.

## Required formal step

Rewrite this as a producer that materializes:

1. all 736 side-specific region rows;
2. exact source/target graph, edge, and corner lineage;
3. the 64 origin completion summaries;
4. all immutable word-key joins;
5. strict dimensional and positive-volume ledgers.

Its independent verifier must not import the producer and must rebuild the
geometry, sign-to-word transition, key mapping, pair glue, and full
attachment.  It also needs re-signed semantic attacks, strict JSON and path
attacks, plus at least two hash-seed cold replays.

Until that formal step passes:

- officially materialized local signature rows: `0`
- whole original tube credit: `0`
- source-G global dispositions: `0/224580`
- Gate5: `10/18`
- D02: `BLOCKED`
- CM2: `NO-GO`
