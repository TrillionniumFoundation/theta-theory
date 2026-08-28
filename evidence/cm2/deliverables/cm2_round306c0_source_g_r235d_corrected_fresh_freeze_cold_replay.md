# Round306C0 cold replay

## Command

```sh
env -i HOME="$HOME" PATH=/usr/bin:/bin LANG=C LC_ALL=C TMPDIR=/tmp \
  /usr/bin/time -v python3 -I -B -S \
  deliverables/cm2_round306c0_source_g_r235d_corrected_fresh_freeze_independent_verifier.py \
  --verify-no-write \
  --candidate-dir /tmp/cm2-round306c0-candidate-final
```

## Observed result

```text
exit=0
elapsed=21:40.81
maximum_resident_set_kib=1613960
status=PASS_INDEPENDENT_C0_CANDIDATE_FULL_ROW_COMPARATOR__ZERO_GLOBAL_CREDIT
artifact_count=9
corrected_member_count=564460
corrected_base_root_count=367948
corrected_component_count=92672
corrected_partition_sha256=1ae914d4e2cff22d1fa6ddad4ffe4679c594bde3cdad27acf1480202b7a89434
cross_component_pair_denominator=158820108554
producer_or_upstream_producer_or_verifier_imported_or_executed=false
deliverables_write_syscalls=0
```

The replay independently reopens and revalidates all 23 authority pins,
reconstructs the corrected root/member universe, performs forward and reverse
fresh DSU applications, rebuilds all six expected ledgers, and compares every
candidate row.  The external candidate remains outside deliverables and all
nine candidate files remain regular, one-link, held-FD snapshots.

This cold replay does not by itself seal the package.  The final gate is the
manifest-first `--manifest-first-no-write` replay after the report, cold record,
and exact ordered manifest have been fixed.
