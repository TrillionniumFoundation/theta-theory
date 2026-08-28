# CM2 Round125 cold replay

Date: 2026-07-23  
Status: **PASS.**

## Frozen code and logical digests

```text
producer             e360c511c87f10483ee19cf566d9542f123a2fbdf37585d9954a9c33575b940b
certificate          cecae7d1b864abcb62215c317bb87bbf392848c70b6affca253d350a9f687579
certificate result   b75c0574aa337c7ea5f9659e04980d0e415c30a2dd1a2b81b3774ed0577053ba
verifier             15f5313fc9f9593a0e1d41b95a9c09f7cc204f3471e177c17b1355b9a3f13737
verification         919c50840eee75bcebb7ed8d870f2300d6a47466055bd4d25d95645dbbc6bd62
verification result  92919d7d41bf159628068d589f6e16e390be2f04017c6094f1aa4cdedd32527c
```

## Producer replays

Two complete producer runs used the repository environment containing
`python-flint`, fixed locale and timezone, disabled bytecode writes, and
distinct hash seeds:

```text
PYTHONHASHSEED=125731 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=125947 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
interpreter: .venv-neurips/bin/python
```

Both exited `0`.  The canonical certificate and both replay outputs are
byte-identical with SHA256
`cecae7d1b864abcb62215c317bb87bbf392848c70b6affca253d350a9f687579`.
All three pairwise `cmp` checks return `0`.  Each result digest independently
recomputes to
`b75c0574aa337c7ea5f9659e04980d0e415c30a2dd1a2b81b3774ed0577053ba`.

The producer precision is 1536 bits.  The comparison covers all four
recipient components, 72 recipient maps, three source contracts, 72
graph-current legs, three source derivations, 144 input traces, 432 output
traces, 215 output incidences, 120 F17 slots, the 2040-key combined ledger,
and all nested and outer digests.

## Independent verifier replays

Two complete mutation-enabled verifier runs consumed the corresponding
producer replay certificates under the same two environments.  Both exited
`0` with `PASS`.

The canonical verification and both replay artifacts are byte-identical with
SHA256
`919c50840eee75bcebb7ed8d870f2300d6a47466055bd4d25d95645dbbc6bd62`.
All three pairwise `cmp` checks return `0`, and each result digest recomputes
to
`92919d7d41bf159628068d589f6e16e390be2f04017c6094f1aa4cdedd32527c`.

```text
producer precision                         1536 bits
verification precision                     3072 bits
semantic mutations rejected              248/248
strict-JSON attacks rejected                15/15
actual common children                         24
graph-current leg rows                         72
recipient components                            4
recipient pullback maps                        72
source contracts / derivations                3 / 3
input artificial traces                       144
stage-3 output artificial traces              432
stage-3 incidences cancelled / retained    192 / 23
retained typed output trace sides              48
new F17 full-key slots                         120
stage slot counts                         48/24/48
combined child-local slots                    2040
rank3 seed-child maturity                    17/18
remaining child field                          F18
global Gate5                                10/18
complete 18-field blocks                         0
Gate5 blocks                                     0
CM2                                   NO-GO_FOR_CLAIM
```

All six JSON files pass strict loading, canonical pretty-print roundtrip, and
independent compact-result digest recomputation.

## Negative cold paths

A nonexistent certificate exits `1` with no output.  A valid-JSON copy whose
top-level `precision_bits` was changed from `1536` to `1537` also exits `1`
with `VerificationError: certificate result digest` and writes no output.

System `python3` is not a valid replay environment on this host because it
lacks `python-flint`; the frozen replay commands deliberately use
`.venv-neurips/bin/python`.
