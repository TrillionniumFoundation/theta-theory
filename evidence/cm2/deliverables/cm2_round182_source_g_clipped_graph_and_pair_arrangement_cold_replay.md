# CM2 Round182 cold replay

Date: 2026-07-26  
Verdict: `PASS`

## Frozen artifact identities

- producer:
  `8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56`
- certificate file:
  `27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08`
- certificate result:
  `e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d`
- row attachment file:
  `ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c`
- row attachment result:
  `9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269`
- independent verifier:
  `790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566`
- verification file:
  `b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36`
- verification result:
  `61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797`

## Producer replay

The frozen formal certificate and its `158,815,476`-byte row attachment were
used as the baseline.  A clean replay under `PYTHONHASHSEED=211` ran:

```text
env PYTHONHASHSEED=211 ../.venv-neurips/bin/python \
  cm2_round182_source_g_clipped_graph_and_pair_arrangement.py \
  --output .cm2_round182_producer_seed211_certificate.tmp.json \
  --attachment .cm2_round182_producer_seed211_rows.tmp.json \
  --expect-certificate-result e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d \
  --expect-attachment-result 9f0f64d93bd0ac2a9dd41965cbfd95531f07582da5eb4c52f14c44da3d0db269
```

The replay certificate and row attachment were each compared with `cmp` by
both the producing agent and the parent agent:

- certificate: byte-identical, file SHA256 `27491e3943...f49f08`
- row attachment: byte-identical, exactly `158,815,476` bytes, file SHA256
  `ae6e0c38...f3f847c`
- elapsed: `14:52.90`
- maximum RSS: `1,339,732 kB`
- exit status: `0`

## Independent-verifier replays

The verifier reconstructs every row and all attachment bytes without
importing or executing the producer.  All three runs returned `PASS`, result
SHA256 `61715e...9797`, and a byte-identical verification file with SHA256
`b008c2...11f36`.

| hash seed | role | elapsed | maximum RSS |
|---:|---|---:|---:|
| `17` | formal verification | `26:54.04` | `2,148,492 kB` |
| `211` | producing-agent cold replay | `27:11.79` | `2,146,924 kB` |
| `182051` | parent-agent cold replay | `27:26.64` | `2,148,824 kB` |

The producing-agent seed-211 invocation was:

```text
env PYTHONHASHSEED=211 ../.venv-neurips/bin/python \
  cm2_round182_source_g_clipped_graph_and_pair_arrangement_verifier.py \
  --output cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification_seed211.tmp.json \
  --expect-result 61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797
```

The seed-17 and seed-211 outputs were compared locally with `cmp`; the
parent independently performed the seed-182051 replay and comparison.

Every run retained the same rejection matrix:

- re-signed semantic attacks: `36/36`
- strict JSON/oversize attacks: `10/10`
- path/type/output-alias/prepositioned-temp attacks: `12/12`

Temporary replay copies were removed only after byte comparisons, byte
counts, hashes, timings, and memory maxima had been recorded.

## State invariant

Cold replay creates no promotion:

- source-G global exact-key dispositions: `0/224580`
- Gate5: `10/18`
- complete global 18-field blocks: `0`
- D02: `BLOCKED`
- D03 negative oracle: `UNAUTHORIZED`
- CM2: `NO-GO`
