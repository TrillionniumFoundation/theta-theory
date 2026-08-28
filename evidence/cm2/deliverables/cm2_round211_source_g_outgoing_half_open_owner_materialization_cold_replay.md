# CM2 Round211 cold replay

Date: 2026-07-27

## Frozen artifacts before replay

```text
producer
9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02

official certificate
bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f

certificate result
3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b

verifier
df90f2dd869bef3b873fe800fe124a256e82ef7e772359fbea49a9b793725176

official verification
1dee3afbe5cc04829ef5546ef16f8ef76b6d9a32f7bd1aab61037066419ad2f9

verification result
eed5687f736c6244421ec432a4d1fc283d84386147293825a19837173cbb819d
```

## Producer replay

Official:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=211051 \
  ../.venv-neurips/bin/python -B \
  cm2_round211_source_g_outgoing_half_open_owner_materialization.py
```

Independent replay:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=211052 \
  ../.venv-neurips/bin/python -B \
  cm2_round211_source_g_outgoing_half_open_owner_materialization.py \
  --output \
  .cm2_round211_source_g_outgoing_half_open_owner_materialization_replay_211052.json
```

Both exited zero and printed

```text
3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b.
```

Resources:

| run | elapsed | maximum RSS |
|---|---:|---:|
| official seed 211051 | `1:08.01` | `748,700 KiB` |
| replay seed 211052 | `1:01.55` | `749,088 KiB` |

The two `140,690,802`-byte certificates have SHA256

```text
bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f
```

and `cmp` exits zero.

## Verifier replay

Official:

```bash
env PYTHONDWRITEBYTECODE=1 PYTHONHASHSEED=211061 \
  ../.venv-neurips/bin/python -B \
  cm2_round211_source_g_outgoing_half_open_owner_materialization_verifier.py
```

Independent replay:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=211062 \
  ../.venv-neurips/bin/python -B \
  cm2_round211_source_g_outgoing_half_open_owner_materialization_verifier.py \
  --certificate \
  .cm2_round211_source_g_outgoing_half_open_owner_materialization_replay_211052.json \
  --output \
  .cm2_round211_source_g_outgoing_half_open_owner_materialization_verification_replay_211062.json
```

Both exited zero with

```text
PASS_PARTIAL_FORMAL_ROUND211.
```

Resources:

| run | elapsed | maximum RSS |
|---|---:|---:|
| official seed 211061 | `1:42.77` | `1,022,724 KiB` |
| replay seed 211062 | `1:49.25` | `1,021,828 KiB` |

The two verification documents have SHA256

```text
1dee3afbe5cc04829ef5546ef16f8ef76b6d9a32f7bd1aab61037066419ad2f9
```

and `cmp` exits zero.

The verifier rebuilt the complete expected result before opening either
certificate, imported or executed neither the producer nor Round209 probe,
and rejected:

```text
20/20 re-signed semantic mutations
 9/9  strict JSON and encoding attacks
 8/8  path, type, and output attacks.
```

## Cleanup and final state

The two hidden replay documents were byte-identical to their official
counterparts and were removed after comparison.  No Round208 file was
modified.

The replay does not alter the strict promotion boundary:

```text
global component credit              0
whole-original-tube credit            0
global exact-key disposition credit   0
source-G global dispositions          0/224580
D02                                   BLOCKED
Gate5                                 10/18
CM2                                   NO-GO_FOR_CLAIM.
```
