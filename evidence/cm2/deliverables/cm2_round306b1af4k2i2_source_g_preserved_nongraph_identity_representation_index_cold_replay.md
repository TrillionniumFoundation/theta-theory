# K2I2 cold replay and immutable no-write contract

## Producer replay

Run the pinned producer twice with distinct hash seeds into two real,
single-link output directories, one of which is outside `deliverables`:

```text
python -I -B cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_producer.py --produce --output-directory <seed17-dir> --hash-seed 17
python -I -B cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_producer.py --produce --output-directory <seed29-dir> --hash-seed 29
```

The authoritative replay required byte identity for the gap, member,
representation, and result files.  All four comparisons passed.  The producer
never embeds its own SHA; the independent verifier supplies the external
static producer pin.

## Controlled first receipt publication

The only mode authorized to publish receipts is:

```text
python -I -B cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_independent_verifier.py --verify-publish --output-directory .
```

It completed a full replay and atomically published exactly two canonical
receipts.  Their file SHA-256 values are:

- verification: `7ba5d17cdbf9818418b272cf47975ed3b0363d1be0512972fc840b759e7c8a98`;
- attack suite: `4de0b879354d66c7f7766f97481b58c6753fcb24d6f1b1aebbcf300ed98553ca`.

## Post-manifest no-write replay

All verification after manifest creation must use:

```text
python -I -B cm2_round306b1af4k2i2_source_g_preserved_nongraph_identity_representation_index_independent_verifier.py --verify-no-write
```

This mode rejects any `--output-directory`, never calls the receipt publisher,
and writes only a canonical summary to stdout.  A successful replay must
report `filesystem_write:false`, `mode:"VERIFY_NO_WRITE"`, verification
receipt SHA
`7ba5d17cdbf9818418b272cf47975ed3b0363d1be0512972fc840b759e7c8a98`,
and attack receipt SHA
`4de0b879354d66c7f7766f97481b58c6753fcb24d6f1b1aebbcf300ed98553ca`.

Take SHA-256, byte size, `mtime_ns`, and `ctime_ns` snapshots for every
manifest member and the manifest itself immediately before and after this
command.  Exact snapshot equality is required.  Runtime elapsed/RSS data, if
collected externally, is diagnostic only and must not enter the package.
