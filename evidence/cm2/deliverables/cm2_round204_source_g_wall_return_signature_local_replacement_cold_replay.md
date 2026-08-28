# CM2 Round204 source-G wall return-signature cold replay

Date: 2026-07-26

This record covers both the producer replay and the independent formal
verifier replay.

## Frozen producer output

- Producer:
  `cm2_round204_source_g_wall_return_signature_local_replacement.py`
- Producer SHA-256:
  `7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77`
- Certificate:
  `cm2_round204_source_g_wall_return_signature_local_replacement_certificate.json`
- Certificate SHA-256:
  `e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818`
- Certificate result SHA-256:
  `ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd`
- Pinned Round182 manifest SHA-256:
  `32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5`
- Independent verifier SHA-256:
  `6bcfbb794005e5a92590b7bb60ffceda34db3441ced143a15ceb23e15d5c035e`
- Official verification SHA-256:
  `04525bd3f1257825fe4825cfbf17674b3391c503b3cbe987b45ffd6f7346e852`
- Verification result SHA-256:
  `bd523e7c288e8b6830a7e94d78d06039b324bc8d2fdcfd38dab2ec85b532b1fd`

The certificate wrapper is strict canonical JSON with one trailing newline.
Its recorded result digest equals a fresh canonical digest of `result`, and
its recorded producer digest equals the frozen producer file.

## Independent-seed producer replay

Both executions used `.venv-neurips/bin/python -B` with
`PYTHONDONTWRITEBYTECODE=1`.

| Run | `PYTHONHASHSEED` | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|---:|
| Official producer | 204051 | 99.52 s | 4.32 s | 1:43.95 | 2,333,656 KiB | 0 |
| Cold replay | 204062 | 99.53 s | 4.50 s | 1:44.07 | 2,334,080 KiB | 0 |

The replay wrote to the separate allowlisted path
`.cm2_round204_seed204062_certificate.json`. `cmp` returned zero, and both
certificate files have SHA-256
`e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818`.
Both stdout files contain only the same result digest and are byte-identical.

## Independent verifier replay

The hidden verifier replay used seed `204071`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=204071 /usr/bin/time -v \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py \
  --output deliverables/.cm2_round204_seed204071_verification.json
```

The official verifier run used seed `204072` and pinned the first run's
verification result:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=204072 /usr/bin/time -v \
  .venv-neurips/bin/python -B \
  deliverables/cm2_round204_source_g_wall_return_signature_local_replacement_verifier.py \
  --expect-result bd523e7c288e8b6830a7e94d78d06039b324bc8d2fdcfd38dab2ec85b532b1fd
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Hidden replay, seed `204071` | 113.74 s | 4.15 s | 1:58.26 | 2,336,756 KiB | 0 |
| Official, seed `204072` | 117.07 s | 4.39 s | 2:01.51 | 2,336,672 KiB | 0 |

Both stdout files contain only verification result SHA-256
`bd523e7c288e8b6830a7e94d78d06039b324bc8d2fdcfd38dab2ec85b532b1fd`
and are byte-identical. `cmp` returned zero for the hidden and official
verification files. Both files have SHA-256
`04525bd3f1257825fe4825cfbf17674b3391c503b3cbe987b45ffd6f7346e852`
and contain `8,537` bytes.

Each run rebuilt the complete expected Round204 result before opening the
candidate certificate, treated the producer as inert pinned bytes, and did
not import or execute it. Each independently re-pinned the complete
seven-entry Round182 package and rejected:

- `20/20` genuinely re-signed semantic mutations, with affected closed-row
  and ledger hashes recomputed;
- `15/15` strict JSON, encoding, and oversize attacks;
- `21/21` path/type/alias/temp attacks or prepositioned-temp bypass attempts.

The verified exact census is 64 origins, 512 leaves, 736 strict 3D regions,
96 tail regions, 224 source plus 224 target 2D cells, 1,024 1D strata,
580 0D strata, 32 tail glues, and 12 local exact-key joins. All 7,184
whole-tube/global-disposition credit-field occurrences are zero.

The AST audit found zero duplicate literal dictionary keys. It reports 43
exact lower-level function-body overlaps, while the producer `build_result`
and `main` bodies are not reused. The package makes no
implementation-diverse second-derivation claim.

## Producer assertions reached

- 64 exact Round182 wall-G origins and all 512 leaves were reconstructed.
- The sole return-signature obstruction was discharged on all 512 leaves.
- 736 unique strict open 3D region rows were materialized, including all 96
  tail regions.
- The closed-cell lineage contains 224 source 2D sheet cells, 224 target 2D
  sheet cells, 1,024 unique 1D strata, and 580 unique 0D strata.
- The exact source-target intersection contains 16 unique 1D segments with
  32 source-sheet and 32 target-sheet closed-boundary incidences, and 20
  unique endpoints.
- All 32 tail pairs have explicit empty-event-empty signature glue.
- All 736 local regions join exactly one of 12 immutable exact keys.
- Whole-original-tube credit and global-exact-key-disposition credit are
  both zero.
- The disposition remains D02 `BLOCKED`, Gate5 `10/18`, and CM2
  `NO-GO_FOR_CLAIM`.

## Output safety

The producer restricts output to its own deliverables directory and to the
official name or a hidden Round204 certificate replay name. It rejects
parent aliases, paths outside that directory, protected inputs, symlinks,
non-regular files, and multiply linked files. It writes through a
same-directory temporary file, flushes and `fsync`s it, atomically replaces
the destination, then `fsync`s the directory; the temporary file is removed
on failure.

The Round192 and Round196 probes were not read, imported, pinned, or used as
formal inputs. The producer did not import or execute the Round204 verifier.
The verifier did not import or execute the producer. The hidden producer and
verifier replay files were retained only through byte comparison, hash
capture, documentation, and manifest validation, then removed.
