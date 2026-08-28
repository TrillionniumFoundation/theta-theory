# C70-L large-component consumption intersection report v1

## Strict conclusion

`PASS_EXACT_READ_ONLY_CONSUMPTION_INTERSECTION__298_OF_1042_EDGES__73_OF_1044_CORRIDORS_READY__ZERO_CREDIT`

This round is a read-only intersection audit. It does not install C66, mint a handoff, close a whole cell, or change any formal/D02 authority. Runtime and `CM2_LATEST_STATUS.md` were not written. CM2 remains `NO-GO_FOR_CLAIM`.

## Frozen inputs and predicates

The edge predicate was independently reconstructed as:

`C66 owner ∧ C63 semantic history ∧ C67 full named margin ∧ C68 source local ∧ C68 target local`.

The history predicate is exactly C63 `all_atom_semantic_mappings_complete && all_atoms_in_complete_overlay_scope`, which passes `1,042/1,042`. C63's legacy combined `overall_owner_history_mapping_pass` passes only 911 and was deliberately not reused: C66 separately supplies the post-tie full-domain owner predicate for `1,042/1,042` edges.

The corridor predicate was independently reconstructed as:

`all immediate incident edges pass the five-way edge predicate ∧ C68 whole-rooted-local`.

C68 current-cell local remains recorded separately and whole-rooted-local is required to imply it. Partial edge/corridor coverage is never interpreted as credit.

## Exact edge census

- Owner pass: 1,042
- Semantic-history pass: 1,042
- Full named-margin pass: 491
- Source-local pass: 348
- Target-local pass: 379
- Both-local pass: 300
- Five-way ready: 298
- Blocked: 744

The eight exact `(margin, source-local, target-local)` combinations, with owner/history both true throughout, are:

- `(0,0,0)=547`, `(0,0,1)=1`, `(0,1,0)=1`, `(0,1,1)=2`
- `(1,0,0)=68`, `(1,0,1)=78`, `(1,1,0)=47`, `(1,1,1)=298`

By component, ready/blocked is component 0: `147/374`; component 1: `151/370`.

## Source-seam boundary

There are 16 `SOURCE_CHART_TRANSITION` edges. Thirteen pass the C67 full named-margin predicate, but zero have both direct-C41 endpoint-local flags and therefore zero pass the five-way intersection. All 16 remain fail-closed.

## Exact corridor census

- Immediate-incident-edge all-pass: 248
- Current-cell local: 350
- Whole-rooted-local: 89
- Corridor ready: 73
- Corridor blocked: 971

The exact `(all-incident, whole-rooted-local, current-local)` combinations are:

- `(0,0,0)=694`, `(0,0,1)=86`, `(0,1,1)=16`
- `(1,0,1)=175`, `(1,1,1)=73`

By component, ready/blocked is component 0: `2/520`; component 1: `71/451`. Incident degree census is `1:254, 2:574, 3:186, 4:26, 5:4`.

## Rejected predecessor tuple

An unsealed pre-freeze result captured ledger descriptors before deterministic gzip close. Its result file `465d0323…6a80`, object `5266c940…941d`, and producer `55c82ac2…07f0` are terminally rejected and must never be consumed. The explicit rejection marker binds both the rejected descriptor tuple and the accepted frozen producer `12757adc…6da2`. The corrected ledgers were generated twice in isolated staging directories and compared byte-for-byte before the candidate was retained.

## Independent verification

The cold verifier treats the producer as opaque bytes and never decodes, imports, compiles, or executes it. It independently:

- checks actual gzip SHA-256 and byte size against each descriptor;
- checks all 1,042 and 1,044 rows, row hashes, closed schemas, counts, and row-hash sequences;
- rejoins C63/C66/C67/C68 and reconstructs every edge and corridor row;
- reproduces all summary and blocker-intersection censuses;
- verifies source-seam ready count is zero and every formal/handoff/whole-cell/D02 credit field is zero;
- rejects 24/24 coherent reclosed and symlink/hardlink/hash-substitution attacks;
- produces byte-identical verification output on two isolated runs.

## Frozen hashes

- Producer: `12757adc50c13b38cf8d0971bfbc4a97edc336bad0c8e1a802c7b188fabd6da2`
- Edge ledger: `d440cbefccb0c3c49c6e35b2f42b73a0cef6ad7a83797a1d712e1c5dfeba0d78`
- Corridor ledger: `dd9bad188879d1e63b2a7d7cd0d4abef91e8d975c84476619e69fa2057b9a693`
- Result file: `6f981c2dced0c5dc97357d43660d9b40c733ada4c964a7322c7cb15fe4e413d8`
- Result object: `86fb7b4d203e567e16e1b308456758ccd3a645382379bca4f656034af86febfd`
- Rejection marker: `6fd0cd001d2c9bfb2f9352626201aa6807965de0fd74c0cb48328b15a13a1318`
- Independent verifier: `648b07038172b372c4beab2c784486ec3e6796f733ce66a716f70e4322b75f5c`
- Independent verification file: `3fc715968dbe26cb2f3cd7b9ef468f14c7986cc81ddfad3ff49c3083a11b6d53`
- Independent verification object: `d69981616ae5a7b202f9212d866b2c66533de61037d6bd0f38888c765334dab5`
- C53 head unchanged: `f62483c87df4b6f4a8a2ad8dcf56febbfce9977200ce94a0ad6ce38e736aeeb3`
- Canonical unchanged: `922fc5d01918b217556bc3f392c44efcc7c9c6345c881371e6cd34950eb99b57`

## Credit boundary

`formal_credit=0`, `handoff_credit=0`, `whole_cell_credit=0`, and `D02_gate_credit=0` in every ledger row, result, rejection marker, and verification. The 298/73 ready subsets are diagnostic consumption intersections only.
