# Round302-A cold replay

From `deliverables/`, with no candidate cache:

```sh
PYTHONHASHSEED=101 python \
  cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion.py \
  --seed 302101

PYTHONHASHSEED=997 python \
  cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion.py \
  --seed 302997

PYTHONHASHSEED=173 python \
  cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_verifier.py \
  --seed 302173 --write

PYTHONHASHSEED=991 python \
  cm2_round302a_source_g_r248_double_endpoint_sheet_attachment_exclusion_verifier.py \
  --seed 302991
```

Both producer runs emitted the same ledger/result commitments.  Both
verifier runs emitted verification self-closure
`c294b46739228de648779dca5af9e41fdae04d9902c078aeab44b3609cc646ef`
and attack-suite self-closure
`e30c7115f48a1f5fe9e0677b1ba6d744c3358f85f34a6aa65bd10b1f5f449b2e`.
All 46 attacks were rejected.
