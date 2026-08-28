# CM2 Round151 cold replay

Date: 2026-07-24

## Producer

The producer was rerun from cold processes under
`PYTHONHASHSEED=151001` and `PYTHONHASHSEED=151997`.

Both outputs were byte-identical to the formal certificate:

```text
593188b5e9996cfa8151cd15c318a7a6136c108dba123cc91e421c83f7aea821
```

Both result payloads had SHA256:

```text
66b495117aa7a31c4d221144240cb8cc1233c6c6ee8b58cf7619d0a123790744
```

## Verifier

The independent verifier was rerun from cold processes under
`PYTHONHASHSEED=151101` and `PYTHONHASHSEED=151909`.

Both outputs were byte-identical to the formal verification:

```text
61e053ca782cd030bb6d3a182e7ff4f032e4d6bb2fadf1fa82682789908ae1cd
```

Both verification result payloads had SHA256:

```text
eee4a736efd6b3cd7913fcafa28b371a77382d9c228f55b843f6be799445874d
```

## Verdict

```text
producer cold replay      BYTE_IDENTICAL
verifier cold replay      BYTE_IDENTICAL
formal verification      PASS
```
