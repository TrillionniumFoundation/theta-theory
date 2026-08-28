# Round225 source-G certified-connectivity rebuild — frozen report

## Verdict

`PASS_PARTIAL_FORMAL_ROUND225`.

An independent verifier reconstructed the Round222 partition from frozen
upstream certificates, added only the exact Round223 and Round224 TRACE glues,
and matched the complete Round225 candidate result byte-for-byte at the
canonical semantic layer.  It did not import or execute the Round225 producer.

The certified known-connectivity quotient changes from `7,640` to `7,404`
blocks.  The 7,016 Round223 pairs are rank-redundant and reduce zero blocks;
the 236 Round224 pairs reduce exactly 236 blocks.  The remaining known-contact
cross-block frontier is zero and the 28 inherited proved-ABSENT rows remain
nonedges.

## Hostile audit

The final verifier rejected:

- `12/12` independently re-signed semantic mutations;
- `16/16` strict-JSON attacks, including duplicate keys, non-integral numbers,
  non-finite tokens, trailing data, and invalid Unicode surrogates; and
- `10/10` path/file-object attacks, including symlink, hardlink, FIFO,
  directory, missing/empty/oversize input, path alias, protected output, and
  output symlink cases.

Two cold replays under `PYTHONHASHSEED=225052` and `225997` both exited zero
and produced the identical verification result and file hashes.

## Frozen hashes

- producer: `1c6637751c398ff26faceee0419421ffdab1616d17bab9ad99fa3c24a9b3d9f2`;
- certificate: `0d040af30906f22f600820e14867c45115e679e33b6ee6f052c51a914cf7d841`;
- certificate result: `0aedfdcc43e45810d97cc0699562a4d1e9faefb0ca3f3e055c84b1ad3ec77512`;
- verifier: `33f6a2a0675c91c19b4467e9e8fc486cfcc013c0ee0184871cd65fc2072cb4c5`;
- verification: `160f8f038edc954361a70ae90a3feed13d299e4e218f5cd5e01482af26736b51`;
- verification result: `979456672f3a2bcf535f907a969a9803223f27efa78d9c6f71682e4260ee3534`.

## Strict boundary

The `7,404` objects are certified known-connectivity blocks, not maximal
physical components.  Cross-parent/cross-chart transition equivalence and
occurrence-fibre exhaustion remain incomplete.  Component, whole-origin,
global-fibre, and exact-key-disposition credits remain zero; D02 remains
`BLOCKED`, Gate5 remains `10/18`, and CM2 remains `NO-GO_FOR_CLAIM`.

