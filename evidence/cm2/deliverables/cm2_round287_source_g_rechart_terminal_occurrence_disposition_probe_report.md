# CM2 Round287 — physical-side-corrected R275 occurrence disposition

Status: **PASS PROBE — TERMINAL DISPOSITION CONTRACT, ZERO CREDIT**

Round287 exhausts all `13,788` Round275 reverse-rechart rows and all `7,616`
Round286 coordinate-refinement rows.  It does not issue occurrence IDs.  Its
main correction is that a Round286 rational coordinate cell is not
automatically a nonempty slice of both signed sides of a Round275 regular
graph.

## Inclusion-alias lemma

Round287 freezes the following exact representation rule.

If a nonempty R275 signed open support, or a nonempty R286 signed support
slice, is strictly included in one certified connected positive-open
Round279 atom support under the same physical chart coordinates, and the
complete ten-field signature, exact key, and owner agree, the smaller row is
an exact representation-subcover witness for that atom occurrence identity.
It receives no new occurrence ID.

This rule does not use box containment alone.  It also does not permit
signature-only, face-only, partial-overlap, or Jx/Jy aliases, and it never
collapses two existing occurrence IDs.

The resulting inclusion-alias evidence is:

- `2,476` whole R275 contained-region witnesses;
- `5,532` nonempty refined signed support slices;
- all remain conditional on preservation or promotion of their containing
  Round279 atom identity.

## Round286 physical-side correction

For every refinement row whose parent is
`REGULAR_GRAPH_CROSSING`, the producer replays the frozen active factor,
strict derivative signs, and exact extremal signs.  Each coordinate cell is
then classified as full desired-side support, clipped desired-side support,
or empty for that signed R275 row.

The corrected cell census is:

- occupied: `3,484` full, `2,048` clipped, `168` empty;
- uncovered: `1,108` full, `432` clipped, `376` empty;
- total empty opposite-side coordinate rows: `544`;
- nonempty inclusion-alias slices: `5,532`;
- nonempty uncovered slices: `1,540`.

Thus the earlier coordinate-only preview (`1,916` uncovered rows, `1,224`
mixed parents, `692` internal faces) cannot be used for occurrence issuance.
After removing empty signed slices:

- `1,292` partial parents are physically fully atom-covered and create no
  parent alias or new occurrence;
- `892` parents retain uncovered support;
- `648` valid artificial internal physical faces contract the `1,540`
  uncovered slices to exactly `892` connected parent-local support unions.

Together with the `9,128` whole R275 rows having no matching positive-volume
atom overlap, the corrected conditional new-support census is:

```text
9,128 + 892 = 10,020
```

This is a conditional support census, not formal expanded-occurrence credit.

## Pairwise uniqueness and Round283 guard

The complete R275 pair sweep finds `3,488` rational/physical-t outer-overlap
pairs.  Every pair is exactly the two opposite signed sides of one certified
regular graph cell: same guard, same outer cell, opposite strict factor
signs, and different complete signatures.  The open factor sides are
physically disjoint.  No cross-guard or cross-return-branch positive-volume
duplicate remains.

Round283's `64` logical analytic children are not materialized occurrence
identity rows.  They may overlap across return branches and must only be
bound as refinement witnesses to the already disposed R275 supports.
Round287 awards them zero occurrence credit.

## Independent cacheless verification

The Round287 verifier does not import or execute the producer.  It first
reconstructs the Round286 common refinement directly from pinned
Round275/Round279/Round280/Round284 evidence, and only then independently
replays the signed physical support using exact rational outward square-root
enclosures and the frozen Round174/Round179/Round274 geometry formulas.

The independent reconstruction matched all five Round287 tables:

- `13,788` terminal region dispositions;
- `7,616` signed refinement-cell dispositions;
- `10,020` conditional new-support unions;
- `648` valid artificial internal physical faces;
- `3,488` mutually-exclusive outer-overlap pairs.

It independently recovered exactly `544` empty signed cells, `5,532`
nonempty inclusion-alias slices, `1,540` nonempty uncovered slices, `1,292`
physically fully atom-covered parents, and `892` connected partial-parent
unions.  It also enforced that box-only, signature-only, face-only, and
partial-overlap evidence cannot satisfy the inclusion-alias lemma.

`PYTHONHASHSEED=287071` and `287929` produced byte-identical verification
objects.  All `20/20` attacks were rejected, including `17` attacks that
reclosed every row, table, ledger, file binding, and result digest after
mutation.

- verifier SHA256:
  `2ef455c9a3ab9378698c0e4f46838f24f51c4cddd8f7aadc046c24822e8eca5c`;
- verification object SHA256:
  `1e228296c31af8225b0b188743766c8c3b1cab5c6f662ae6e6db450c111b0165`;
- verification file SHA256:
  `c0ad4d3e229a1e21cb5b4f4144575df7f5eaf88d7fc8a6960967ab4c1db515a3`.

## Remaining issuance blockers

Formal issuance still requires:

1. a frozen Round288 atom-to-existing-occurrence correction (the reported
   `640` additional Round204 aliases are not pinned in this Round287 package);
2. preservation/promotion of every containing Round279 atom identity;
3. an independent reconstruction of all `544` empty, `5,532` alias,
   `1,540` uncovered, `648` internal-face, `892` union, and `3,488`
   mutually-exclusive-pair rows;
4. binding the Round283 analytic children only as refinement witnesses;
5. deterministic issuance of the `10,020` new support IDs, followed by the
   true-seam/component DSU rebuild.

If Round288 freezes `295,336` conditional new Round279 atoms, the informational
combined expanded-occurrence arithmetic would be
`126,468 + 295,336 + 10,020 = 431,824`.  That arithmetic receives zero credit
here.

## Replay and strict status

Seeds `287071` and `287929` reproduce the result and the deterministic gzip
ledger byte-for-byte.

- result object SHA256:
  `477813c6ea4b178a6a6862eb31e002b1de763a0b1dff95bb4d76827cb0821c10`;
- result file SHA256:
  `1265475e5d27f99eda35b16f13ba342e0d270ca1bc064df215a018d3ffae89f9`;
- ledger SHA256:
  `29838e3e6b33f03bf623bbce8b87e6ba5c3306e66beb0b6634496503fb9a4f9a`.

Formal new occurrence, identity-collapse, component, seam, maximality, fibre,
global-disposition, and Jx/Jy credits all remain zero.  The frozen baseline
therefore remains expanded occurrences `126,468`, quotient `63,224`,
maximality `0/63,224`, fibres `0/116`, dispositions `0/224,580`, Gate5
`10/18`, D02 blocked, and CM2 `NO-GO_FOR_CLAIM`.
