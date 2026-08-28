# CM2 Round152 cold replay

Date: 2026-07-24

## Producer

The producer was rerun from cold processes under
`PYTHONHASHSEED=152001` and `PYTHONHASHSEED=152997`.

Both outputs were byte-identical to the formal certificate:

```text
f5f3ff201706ecd27bee6d3c668e67fa6a549cdcdf484ae7759ccf31eb45118f
```

Both result payloads had SHA256:

```text
c98f7dc36a3a1bf9aaf5527890f2d9521dd7d66ed21178fe39bdacb6b8f1c5ff
```

## Verifier

The independent verifier was rerun from cold processes under
`PYTHONHASHSEED=152101` and `PYTHONHASHSEED=152909`.

Both outputs were byte-identical to the formal verification:

```text
0cadd6786867906a1afc4eae290fa19b9e241f72b0a4505ebb95a699060b5600
```

Both verification result payloads had SHA256:

```text
7410da7fc0fa7c692a99b7626bdd4d54031f4caa71cdd61707c361db0eb6ff14
```

## Verdict

```text
producer cold replay      BYTE_IDENTICAL
verifier cold replay      BYTE_IDENTICAL
formal verification      PASS
```
