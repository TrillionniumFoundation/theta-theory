# CM2 Round128 cold replay

Date: 2026-07-24

## Frozen digests

```text
producer             d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35
certificate          7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e
certificate result   46601ee43c7ca8051dac51fd608605a814abfb755092ea8225fd3f0f2c755815
verifier             2745ccccdab9869c4754bab37f13ece70f32c7b59063bf0aed4f59cdd81af544
verification         3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d
verification result  2037fb4ad60901824b9a107e51b6092f761dcb9b2d47da1c2f76e2cb06926b45
```

## Two-seed producer replay

Two complete producer runs used:

```text
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=987654321 PYTHONDONTWRITEBYTECODE=1
```

Each run executed:

```text
.venv-neurips/bin/python
  deliverables/cm2_round128_base_r1_component_global_word_incidence.py
  --output <cold-directory>/certificate-{0,987654321}.json
```

Both runs exited `0`.  Their certificates are byte-identical to each other
and to the frozen certificate:

```text
certificate SHA256
  7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e
certificate result SHA256
  46601ee43c7ca8051dac51fd608605a814abfb755092ea8225fd3f0f2c755815
```

## Two-seed verifier replay

The same two hash seeds were used for full mutation-enabled verifier runs:

```text
PYTHONHASHSEED=<seed> PYTHONDONTWRITEBYTECODE=1
  .venv-neurips/bin/python
  deliverables/cm2_round128_base_r1_component_global_word_incidence_verifier.py
  --certificate
    deliverables/cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json
  --output <cold-directory>/verification-<seed>.json
```

Both runs exited `0`, returned `PASS`, and produced byte-identical artifacts.
The cold artifacts are byte-identical to the frozen verification JSON:

```text
verification SHA256          3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d
verification result SHA256   2037fb4ad60901824b9a107e51b6092f761dcb9b2d47da1c2f76e2cb06926b45
semantic mutations           64/64 rejected
strict-JSON attacks          18/18 rejected
```

The verification JSON uses `sort_keys=True`, two-space indentation,
ASCII-safe strings, `allow_nan=False`, and one final newline.  Its stored
result digest equals an independent canonical recomputation.

## Independently replayed state

```text
retained chart/target pairs                             448
crossing patterns per pair                             985
candidate return-word keys                          441280
candidate-row stream SHA256
  841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9
symbolic word/roof positions                        3286976
Gate25 physical cores                                    24
Round71/Round72 joined physical components               32
directed source/destination official-word edges           16
reciprocal unordered word pairs                            8
inside/outside trace incidences                           64
```

The verifier reconstructs every component, face, trace, path-cell, core,
official-word, incidence-row, directed-edge, and reciprocal-pair ID from the
byte-pinned upstream data.  It requires exact equality with Round69's
16-edge directed core graph and with the closed Round128 result.

## Overlap and physical-separation replay

```text
unique exact-seed/source-word overlap ordinal       346720
overlap component count                                  2
overlap directed destination ordinal                102440
exact stage-0 ordinal                               102441
exact stage-2 ordinal                               180256
```

The destination word is therefore distinct from both adjacent exact-seed
words.  A fresh 2048-bit collision replay from the Round121 anchor bracket
establishes:

```text
1/2 < exact stage-1 t < 3/5 < 69/100 <= core16 t
-1/2 < exact stage-1 p < -2/5 < -1/50 <= core16 p
0 < first-collision flight time < 3
```

The symbolic overlap remains physically disjoint.

## Round67 and lower-bound replay

```text
Round67 required composite-key fields                  12
actually joined fields                               0/12
Round67 -> Round72 component crosswalk rows              0

Gate25 local nonempty words                             24
Round127 exact-path local nonempty words                 3
intersection                                             1
scoped union / certified lower bound                    26
global exact nonempty candidate-key count             null
complete global domain census                         false
```

The number `26` remains a scoped lower bound, not an exact global count or a
coverage claim.

## Negative CLI and output-safety replay

Fresh output paths were used for all negative cases:

```text
valid official certificate             rc=0, PASS, output written
nonexistent certificate                rc=1, output absent
different/tampered certificate         rc=1, output absent
dangling output symlink                rc=1, target absent
output hardlink to a pinned upstream   rc=1, upstream hash unchanged
nonregular output target               rc=1, no artifact written
```

The verifier enforces the official certificate byte and result hashes before
writing.  It protects the certificate, producer, verifier, and every pinned
upstream path by resolved path and inode identity.

## Safety replay

Both deterministic artifacts retain:

```text
locally incidence-attached official words                 16
locally certified nonempty-key lower bound                26
global exact nonempty candidate-key count               null
global complete 18-field blocks                            0
Gate5 blocks                                                0
global Gate5 maturity                                   10/18
Gate5 status                                    NOT_CERTIFIED
CM2                                            NO-GO_FOR_CLAIM
```

The replay certifies typed local incidence and strict namespace/physical
separation.  It does not turn word membership into global physical coverage
or a complete operator block.
