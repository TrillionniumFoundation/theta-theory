# CM2 Round184 cold replay

Date: 2026-07-26

## Frozen artifact identities

The Round184 producer source SHA256 is:

```text
28e2bade0186150298827228670a45da54698a8c301180a1646464a2e0bfb906
```

The official certificate has file SHA256:

```text
292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f
```

and result SHA256:

```text
70026cc9e52cfe0adee0be2ff8daf0f4519a2f1947338e902399461039b82dbe
```

The independent verifier source SHA256 is:

```text
55a4e2b44d0f8617d7b7fd0befd251a5cb206d388c23d7b395e39b9a17fa4889
```

The official verification has file SHA256:

```text
7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6
```

and result SHA256:

```text
126bf98cd4bdc1fc7a69b2a57329b89359b74749bbbd1f43fdbccbc816add9e9
```

## Producer replay

A producer cold replay under `PYTHONHASHSEED=184052` wrote to the authorized
hidden path
`.cm2_round184_seed184052_certificate.json`.

It completed with:

| Metric | Value |
|---|---:|
| elapsed | `15:32.98` |
| maximum RSS | `694,244 KB` |
| exit status | `0` |

The hidden certificate and official certificate were compared with `cmp`.
The comparison exit status was zero, and both files had SHA256
`292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f`.
They were byte-identical.

Reproduction command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=184052 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round184_source_w_upper_candidate_priority_and_clipped_delta.py \
  --output deliverables/.cm2_round184_seed184052_certificate.json
```

## Independent-verifier runs

The official verifier run used `PYTHONHASHSEED=184061` and produced the
official verification:

| Metric | Value |
|---|---:|
| status | `PASS_PARTIAL_BOUNDED_ROUND184` |
| elapsed | `18:02.85` |
| maximum RSS | `742,164 KB` |
| exit status | `0` |

The parent cold replay used `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONHASHSEED=184051`, and the frozen expected result digest:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=184051 \
  /usr/bin/time -v .venv-neurips/bin/python -B \
  deliverables/cm2_round184_source_w_upper_candidate_priority_and_clipped_delta_verifier.py \
  --output deliverables/.cm2_round184_parent_184051_verification.json \
  --expect-result 126bf98cd4bdc1fc7a69b2a57329b89359b74749bbbd1f43fdbccbc816add9e9
```

It completed with:

| Metric | Value |
|---|---:|
| status | `PASS_PARTIAL_BOUNDED_ROUND184` |
| elapsed | `16:11.99` |
| maximum RSS | `743,880 KB` |
| exit status | `0` |

The hidden parent verification and official verification were compared with
`cmp`.  The comparison exit status was zero, and both files had SHA256
`7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6`.
They were byte-identical and both carried result SHA256
`126bf98cd4bdc1fc7a69b2a57329b89359b74749bbbd1f43fdbccbc816add9e9`.

The verifier independently rebuilt the complete expected certificate and
rejected 37/37 re-signed semantic attacks, 16/16 strict JSON attacks, and
15/15 path/type/output attacks on both runs.

## State invariant

Neither replay changes the claim state:

- Round184 new whole-parent exclusions: `620`;
- combined source-W ledger: `74,012 excluded + 2,820 live = 76,832`;
- remaining whole-exclusion upper candidates: `824`;
- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`; and
- CM2: `NO-GO_FOR_CLAIM`.

The hidden producer and parent-verifier replay files were retained only until
byte comparison, hash capture, documentation, and six-artifact manifest
validation completed.  They were then removed.
