# Round294 Source-G occurrence-registry atomic promotion: dual-seed cold replay

## Verdict

PASS. Two producer replays and two independent-verifier replays under distinct
`PYTHONHASHSEED` values were byte-identical at every reported output
commitment. Neither program uses the seed to select, order, or transform rows.

## Producer commands

```text
PYTHONHASHSEED=294071 python -B cm2_round294_source_g_occurrence_registry_atomic_promotion.py --seed 294071 --no-write
PYTHONHASHSEED=294929 python -B cm2_round294_source_g_occurrence_registry_atomic_promotion.py --seed 294929 --no-write
```

The two runs reported the same commitments:

```text
registry_ledger_file_sha256
c6b26f13e90072db99fa98f99fc62c77135ff1cbdb23bbbd5bac3e9f64a834bb

representation_binding_ledger_file_sha256
f9fcc986771b1c3551420516cd9f2c5dde662f87d044666d9306404f30bb6833

result_file_sha256
dc93ef564ce1aec4aabbc7ff717ac76749b92899e210179a00dba63f2d32d626

result_sha256
53b9444bd4063671d8bfeeb7731e7b1cca4726f4bddd1abddd4c9ec2ea7572ce
```

Wall-clock observations were 786.84 seconds and 793.68 seconds. Both runs
reported:

```text
431208 registry rows
126468 preserved Round266 occurrence IDs
295336 formal new Round288 atom occurrence IDs
9404 formal new refined Round287 occurrence IDs
304740 total formal new occurrence IDs
46288 formal representation bindings
```

## Independent verifier commands

```text
PYTHONHASHSEED=294071 python -B cm2_round294_source_g_occurrence_registry_atomic_promotion_verifier.py
PYTHONHASHSEED=294929 python -B cm2_round294_source_g_occurrence_registry_atomic_promotion_verifier.py --no-write
```

The two cacheless runs independently reconstructed every source-to-output row
mapping and reported the same commitments:

```text
verification_file_sha256
13dcb461f269a8e346c220b85cad0e87a0392b5e2682b7dd70132fd8bd7a1245

verification_sha256
e0051d008e543e86f5a28716004361817bce80b9b7de3267470629a4449a5a25

attack_suite_file_sha256
aefb50be4969676d752cf8c8cb06f355db508007be4c1ee95f07c305e19a8adb

attack_suite_sha256
cd2fa0b8e4d5223f22b919f7cc0334acf4cd837500a8eea6952ed77e3c87642d
```

Wall-clock observations were 498.77 seconds and 499.93 seconds. Both runs
rejected all 41 attacks: 11 fully reclosed semantic attacks and 30 strict
JSON/GZIP/path/file-object attacks.

## Scope held fixed in every replay

The 431,208 rows are the current formal Stage-A open-3D plus Round287-refined
registry frontier, not a final exhaustive all-stratum registry. The final
registry count remains undetermined. The Round291 576-gap frontier and Round289
396-entry incidence-refinement frontier may lead only to append-only extensions.

No Round294 component, DSU, seam, Jx/Jy, maximality, fibre, disposition, Gate5,
or CM2 promotion occurred. The value 63,224 is retained only as the legacy
pre-Round294 preserved-registry quotient baseline. The post-Round294 expanded
registry DSU has not been rebuilt, so its quotient-component count is null.
