# Round303-A occurrence-anchor to connected-side bridge — sealed report

Status:
`PASS_SEALED_ROUND303A_87824_OCCURRENCE_ANCHOR_CONNECTED_SIDE_BRIDGES__8_W_TAIL_ENDPOINTS_UNRESOLVED__ZERO_COMPONENT_EDGE_AND_DOWNSTREAM_CREDIT`.

Round303-A materializes the following narrow bridge:

```text
Round294 issued occurrence inner anchor B
  -> independently strict positive-volume subbox B0
  -> uniquely bound complete connected source signed region A
```

The sealed theorem is
`ROUND294_CANONICAL_ATOM_OCCURRENCE_ANCHOR_TO_CONNECTED_SOURCE_SIDE_BRIDGE_V1`,
with SHA-256
`41141dbd0fbc9d501c5714ab61b7907711f1a6fdcee1796a6cbc602e9aab138f`.
It neither identifies the full occurrence support with `A` nor proves a
component edge.

## Frozen artifact pins

- producer:
  `b85d6a8f33e81feb613b2cdb04de648376a10c94635b23119bd7f70439ba461a`;
- bridge ledger:
  `efe0e4b71804848611f3702063698ee77bbdf9dc779bc473fba989fb5db7e465`;
- unresolved ledger:
  `a029eae97e1f35b87f9699adb0446f1b1329a55c5b4ee0887b03bd1f4a9db0b8`;
- result file:
  `796b2167e2263108e3e2c373650e1d488152f7558bbc03fffe977d38e0e81d19`;
- embedded result self-closure:
  `fe51b38ecda288a4d1afd89f8a9184423125a78a68be83f1d9db55b79e303631`;
- independent verifier:
  `f8ffa2080b6ccc51c48ce7a37dc6c80ae0a94187f19a744b3f46a03a144f45e3`;
- attack suite:
  `ce29c15b9d685d9e863ab4534adc50302995131283f4dc03e68d34a18a678bf2`;
- verification:
  `ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549`.

## Exact census and credit boundary

- materialized occurrence-anchor to connected-side bridges: `87,824`;
- unresolved W-tail endpoints: `8`;
- W-tail nonedge or exclusion claims: `0`;
- full-occurrence-support equality claims: `0`;
- component-edge credit: `0`;
- DSU rank-reduction credit: `0`;
- Jx/Jy same-point glue credit: `0`;
- occurrence identity or official-key merge credit: `0`;
- maximality, fibre, and global-disposition credit: `0`.

The eight unresolved rows remain neither nonedges nor exclusions.

## Producer replay equality

The three producer replays returned the same exact four hashes above:

| Replay | Hash seed / invocation seed | Mode | Wall time | Maximum RSS |
| --- | --- | --- | ---: | ---: |
| alpha | `303001` / `303001` | no-write | `573.74 s` | `2,641,340 KiB` |
| beta | `303997` / `303997` | formal write | `576.19 s` | `2,639,924 KiB` |
| cold | `303777` / `303777` | fresh pycache root, no-write | `575.30 s` | `2,641,540 KiB` |

For alpha, beta, and cold:

```text
bridge_ledger_file_sha256=efe0e4b71804848611f3702063698ee77bbdf9dc779bc473fba989fb5db7e465
unresolved_ledger_file_sha256=a029eae97e1f35b87f9699adb0446f1b1329a55c5b4ee0887b03bd1f4a9db0b8
result_file_sha256=796b2167e2263108e3e2c373650e1d488152f7558bbc03fffe977d38e0e81d19
result_self_sha256=fe51b38ecda288a4d1afd89f8a9184423125a78a68be83f1d9db55b79e303631
```

The no-write runs establish equality of observed exact hashes, not an
output-file `cmp` claim.

## Independent cacheless verification

The verifier treats the producer only as the inert byte pin
`b85d6a8f33e81feb613b2cdb04de648376a10c94635b23119bd7f70439ba461a`.
It reconstructs the complete expected scope, both ledgers, deterministic GZIP
bytes, result semantics, and all commitments before opening candidate bytes.

| Replay | Hash seed | Mode | Wall time | Maximum RSS | Verification SHA-256 |
| --- | ---: | --- | ---: | ---: | --- |
| alpha | `303073` | fresh pycache, no-write | `1,882.67 s` | `10,210,332 KiB` | `ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549` |
| beta | `303929` | fresh pycache, formal write | `2,105.40 s` | `10,209,912 KiB` | `ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549` |

Both replays returned
`PASS_INDEPENDENT_CACHELESS_EXACT_RECONSTRUCTION_87824_BRIDGES_8_W_TAIL_UNRESOLVED`.
The persisted verification file is exactly
`ada33e5f1a780f92b228861f0e3606ff2c383665d056f1c83b38c0fda56a4549`.
The suite rejected `28 / 28` attacks: 19 semantic re-signing, 5 strict JSON,
and 4 strict GZIP attacks.

## Strict nonclaims

Round303-A alone does not prove or change component connectivity, occurrence
identity, official-key identity, DSU union or rank, seam/Jx/Jy glue,
maximality, fibres, global dispositions, Source-W, D02, or unconditional CM2.
Any later edge promotion must separately verify the closure-limit and
two-sided attachment theorem against this exact sealed package.
