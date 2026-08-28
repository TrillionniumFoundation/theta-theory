# Round219 source-G partial-face common-refinement glue

## Verdict

`FORMAL_ADAPTIVE_EXACT_SUBFACE_PREFIX__468_NEW_EXACT_CONTACT_COMMON_REFINEMENTS_COMPLETE__7016_EXACT_AND_236_PARTIAL_CONTACTS_REMAIN_FAIL_CLOSED`

Round219 takes exactly the `7,484` closed exact-face frontier rows and `264`
partial-face frontier rows from Round217.  It adaptively partitions each exact
face along its transverse rational interval to maximum dyadic depth six,
splitting only children whose interval proof remains unresolved.

This materializes:

- `52,292` terminal exact subfaces:
  - `22,960` strict `TRACE` subfaces;
  - `22,096` strict `ABSENT` subfaces; and
  - `7,236` fail-closed `UNRESOLVED` subfaces;
- `22,960` restricted zero-curve credits;
- `45,920` two-sided local incidence credits;
- `22,960` exact local subface-glue credits; and
- `22,096` formal zero-absence credits.

Exactly `468` of the `7,484` Round217 exact frontier contacts have no
unresolved terminal child.  Those contacts therefore receive complete
TRACE-plus-ABSENT common-refinement credit.  Together with Round217's `448`
direct contacts, the cumulative exact-contact prefix is `916 / 7,932`; the
remaining exact-contact frontier is `7,016`.

At depth zero, the partial-face probe proves `28` additional whole-subface
zero absences (`p:16`, `t:12`) and retains `236` partial contacts
fail-closed (`p:128`, `t:108`).  It promotes no partial trace and performs no
endpoint-to-curve-interior join.

The `7,236` unresolved count is a count of terminal subfaces, not contacts.
Depth seven or deeper is not claimed.  Exact root isolation or a symbolic
exact root coordinate remains necessary before endpoint-to-curve-interior
joins and physical-component quotient closure can be certified.

## Formal artifacts

- Producer:
  `cm2_round219_source_g_partial_face_common_refinement_glue.py`
  - SHA256:
    `8b670ffbcabd5a9796fb67580cbb9e3318b8eb2ee1cd65c5e71f7f1f360b3019`
- Certificate:
  `cm2_round219_source_g_partial_face_common_refinement_glue_certificate.json`
  - SHA256:
    `8341a8b08a0abd5c7a16c61b918b7b47db4d05c3c4e6fae8615892e3aafaf096`
  - result SHA256:
    `f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e`
- Independent verifier:
  `cm2_round219_source_g_partial_face_common_refinement_glue_verifier.py`
  - SHA256:
    `c8fe996f8a6c4faf22d51862e3f4c4a28d405c653159054841c962b6ad1c841c`
- Verification:
  `cm2_round219_source_g_partial_face_common_refinement_glue_verification.json`
  - SHA256:
    `564778c5172751006e5035f13a0caf421dcdc36ace1d61f28a1260d9ec24681c`
  - result SHA256:
    `e570f360e1d52380f708ea828501ab83846ce4e843445bf1d8230dc49f42c5ad`
  - status: `PASS_PARTIAL_FORMAL_ROUND219`

## Frozen input boundary

The producer and verifier pin:

- Round217 source:
  `687fd48134e204a99c807e1fd18954cef7633879396db5f4d291ece1568dfa66`;
- Round217 certificate:
  `1ccf9b4bf65bb4f45603594ea19f47e3b2103ea682bebfff0b023234308938fd`;
- Round217 result:
  `fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286`;
- Round209 probe:
  `dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f`;
- Round186 interval factor evaluator:
  `5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64`;
- Round208 certificate:
  `4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938`;
  and
- Round208 result:
  `d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8`.

The independent verifier reconstructs its complete expected result before it
loads the Round219 candidate.  It does not import or execute the Round219
producer.

## Adaptive partition proof

Each original exact common face is represented by a rational closed interval.
An unresolved child is bisected at its exact rational midpoint.  Every
terminal row records its dyadic path, rational child interval, depth, owning
contact, interval witness digest, and half-open ownership:

`LEFT_CLOSED_RIGHT_OPEN_EXCEPT_FINAL_RIGHT_CLOSED`.

For every contact, the ordered terminal intervals:

1. start at the original lower endpoint;
2. end at the original upper endpoint;
3. meet exactly at consecutive rational endpoints;
4. have no gap; and
5. have no owned overlap under the half-open rule.

A child is `TRACE` only when the selected full-child endpoint C0 signs are
strict and opposite and the full-child graph-axis derivative is strict.  It
is `ABSENT` only when those endpoint signs are strict and equal and the
derivative is strict.  Direct interval endpoint signs are used when strict;
otherwise the pinned centered enclosure is used.  Box touch, midpoint touch,
or a signature hash alone never creates a trace or glue credit.

The terminal-depth histogram is:

| depth | terminal subfaces |
|---:|---:|
| 1 | 7,252 |
| 2 | 7,828 |
| 3 | 7,784 |
| 4 | 7,524 |
| 5 | 7,392 |
| 6 | 14,512 |

The `468` newly complete contacts resolve at:

| maximum resolution depth | complete contacts |
|---:|---:|
| 1 | 96 |
| 2 | 160 |
| 3 | 132 |
| 4 | 48 |
| 5 | 24 |
| 6 | 8 |

They cover 16 official key ordinals.  The complete-contact per-ordinal map
SHA256 is
`113a03b64e784d27512131e341d58fee69027e1a1d9998b0fd5d9cb6b3e540da`.
This is a local ordinal census only; no official key fibre is claimed
globally exhausted.

## Formal ledgers

| ledger | rows | rows SHA256 | row-ID SHA256 | row-hash SHA256 |
|---|---:|---|---|---|
| terminal subfaces | 52,292 | `a0f971e1e62deea85219d424f5bb5bd9b2e8314f771309dbc89a555b1275ca25` | `a87964d9ece380de5c5ba9b2d2c45a5b6a988c1ab7242d51eddb3498280495ce` | `2e2bba8a80069955a050d08b15c44569522bdb5d817f1c6fb3cec251b9f46a13` |
| exact-contact partitions | 7,484 | `0832941ba68d14fc3c87c17dc01fd271114691cd0e4b4c9f2c9230d72258c308` | `f25669a1918ee894f60c9c516404bd70db8d5e38074ee999bb362c5d4f0ee39b` | `f6e5ace15c7c5a80a42cf07137048cbdeb8599a9e8a0357f2f4270f38d061c0d` |
| partial-contact probes | 264 | `6d16ea4ad588175e2cc7f05da15f5e4827d7ce0bd1f66a18adf2d3b1a7e73f62` | `fe6892052fa32515af7c521a23c698f69cc84fe0f713761b90b3d467e8749325` | `ef31f1639e4c56b360afe2eb4e51152887e67f2032b4e4018dc949e40efa76b7` |

Every row is closed by its own SHA256.  Every ledger separately closes its
ordered rows, row IDs, and row hashes.

## Independent verification and attacks

The verifier demands full expected Python-object equality and full expected
canonical equality, then rejects:

- `21/21` genuinely re-signed semantic attacks;
- `15/15` strict JSON attacks; and
- `19/19` filesystem/path/output attacks.

The semantic suite covers omitted or duplicated subfaces and contacts,
subface interval/owner/depth/classification changes, false complete-contact
promotion, partial TRACE promotion, unresolved-subface/contact confusion,
Round217 overlap forgery, depth-seven claims, partition gap/overlap claims,
and component/whole-origin/whole-tube/global-disposition credit theft.

The strict JSON suite rejects duplicate keys, nonfinite numbers, BOM, NUL,
invalid UTF-8, a lone surrogate, trailing bytes, missing final newline,
non-object top levels, empty input, and size violations.

The path suite rejects symlink, hardlink, FIFO, directory, empty, oversized,
misnamed, wrong-parent, missing, and parent-escape inputs; it also rejects
symlink/hardlink/FIFO/directory/nested/unallowlisted outputs.  In particular,
it rejects input and output symlink-parent aliases and an explicit output
`..` parent alias before normalization.  Raw parents, absolute parents, and
resolved parents must all match the exact allowed directory.

AST scans find zero duplicate literal dictionary keys in both frozen sources.

## Strict boundary

Round219 does not close the physical-component equivalence relation.  It
does not invent exact coordinates for endpoint rows and does not equate a
numerical approximation with an exact root coordinate.

All of the following remain zero:

- component-deduplication credit;
- whole-leaf, whole-origin, and whole-original-tube credit;
- global-component and global-fibre credit;
- global exact-key-disposition credit; and
- official source-G dispositions (`0 / 224,580`).

Therefore D02 remains `BLOCKED`, Gate5 remains `10/18`, and CM2 remains
`NO-GO`.

