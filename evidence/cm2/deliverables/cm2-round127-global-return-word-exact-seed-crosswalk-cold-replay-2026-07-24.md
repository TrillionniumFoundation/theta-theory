# CM2 Round127 cold replay

Date: 2026-07-24

## Frozen digests

```text
producer             ea461b3ed1301149bca350f32190348aca955f0a04ce42663fab23451144b0dd
certificate          4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408
certificate result   b6341ea382b099b488a46c0d68279ba8e434a22999f66e550ef231d85ec1933a
verifier             24de0b53c872d43f0a0d7422164e5a2a776a1d35879c923bcf5a07afef94e157
verification         5958b4905b8e005886302a6bffc32d15fd1091cf8dbe20b743488e3f91eeb383
verification result  256d691fa24342761262f84162d99695416708f4414335cd137d2d6d7bb85c61
```

## Two-seed producer replay

Two complete producer runs used:

```text
PYTHONHASHSEED=127031 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=127249 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
```

Each command ran:

```text
python3 deliverables/cm2_round127_global_return_word_exact_seed_crosswalk.py
  --output <cold-directory>/certificate-{A,B}.json
```

Both producer runs exited `0`.  Their certificates are byte-identical to
each other and to the frozen certificate.  All three have SHA256

```text
4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408
```

and result SHA256

```text
b6341ea382b099b488a46c0d68279ba8e434a22999f66e550ef231d85ec1933a.
```

## Two-seed verifier replay

The same two environments were used for full mutation-enabled verifier
runs, with each cold certificate passed explicitly through `--certificate`.
Both runs exited `0`, returned `PASS`, and produced artifacts byte-identical
to each other and to the frozen verification artifact.

```text
verification SHA256          5958b4905b8e005886302a6bffc32d15fd1091cf8dbe20b743488e3f91eeb383
verification result SHA256   256d691fa24342761262f84162d99695416708f4414335cd137d2d6d7bb85c61
semantic mutations           61/61 rejected
strict-JSON attacks          14/14 rejected
```

The verification JSON is canonical
`sort_keys=True, indent=2, allow_nan=False` with a final newline.  A
canonical pretty roundtrip is byte-identical, and the independently
recomputed outer result digest matches its stored value.

## Independently replayed census

```text
retained chart/target pairs                             448
monotone crossing patterns                             985
candidate return-word keys                          441280
candidate-row stream SHA256       841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9
symbolic word/roof positions                        3286976
official path words                                        3
official symbolic word/roof positions                      5
Round121 common children                                  24
Round121 refined subbranches                              24
operator carriers                                         72
seed-local base keys                                      120
seed-local field slots                                   2160
```

The second-leg relative registry target remains `G[1,1]`; its absolute
physical owner remains `G[0,0]`.

## Negative CLI paths

The verifier CLI was exercised with:

```text
valid canonical certificate      rc=0, PASS, output written
nonexistent certificate          rc=1, no output
tampered schema certificate      rc=1, no output
```

The in-verifier attack suite additionally rejects a stale outer result
digest and 61 fully re-signed semantic mutations.  Missing or invalid input
therefore cannot create a false-green verification artifact.

## Safety replay

Both deterministic artifacts retain:

```text
seed-local maturity                         18/18
seed-local complete level blocks              120
seed-local complete child packets               24
global Gate5 maturity                         10/18
global complete 18-field blocks                   0
Gate5 blocks                                      0
Gate5 status                          NOT_CERTIFIED
CM2                                  NO-GO_FOR_CLAIM
```

The replay certifies registry membership and seed-local slot accounting
only.  It does not convert incidence into domain, measure, or physical
coverage.
