# CM2 Round306 B1AF4 K2R233 — Source-G parametric graph-key row authority

## Verdict

`GO_R233_LOCAL_ROW_AUTHORITY_ONLY`; `CM2=NO-GO_FOR_CLAIM`.

This package closes the frozen-byte and row-authority defects of the old
Round233 artifact.  It does not turn a graph-key partition, an outer envelope,
or an almost-everywhere local key into normalized full support.

## Exact replay

- `16/16` inputs, `528,253,395` bytes, were opened with `O_NOFOLLOW`, required
  to be regular single-link files, hashed twice from held FDs, and revalidated
  against their final paths.
- The old four-entry manifest was pinned and validated before payload decode.
- Strict JSON rejects duplicate keys, floats, NaN/Infinity, invalid strings,
  and type aliases such as `false == 0` and `true == 1`.
- The 8 MiB limit is enforced on the final canonical row after a successful
  decode.  Main replay creates no spill file and does not consult `TMPDIR`.
- The old R233 producer and verifier are inert evidence: neither is imported
  nor executed.  The R179/R174/Gate3 engine chain is loaded from held bytes.
  Reusing that chain is an engineering replay boundary, not a new proof of its
  mathematical semantics.

## Row closure

Eight selected source/output tables contain `38,872` row appearances:

- R179 origins: `3,148`;
- R179 retained children: `3,148`;
- R179 resolved siblings: `3,148`;
- R220 split interfaces: `3,148`;
- R231 root summaries: `5,368` (`3,148` nonzero-frontier plus the complementary
  `2,220` zero-frontier rows used to prove the channel partition);
- R231 released descendants attached to the nonzero-frontier roots: `15,544`;
- R232 prior promotions: `2,220`;
- R233 graph-key partition outputs: `3,148`.

Every selected row now has source ordinal, selection ordinal, row ID, and
canonical row SHA-256.  All `38,872/38,872` row appearances are closed, with
zero missing SHA.  Each of the `3,148` R233 conclusions separately binds its
R179 origin/retained/sibling rows, R220 interface, R231 root and complete
released-descendant list, the frozen engine chain, the global `2,220 + 3,148`
channel universe, and its exact output row.  All `3,148` canonical input
commitments are distinct.

The exact replay reconfirms `3,148` strict interval derivatives, `3,148`
two-open-side cell partitions, `44` shared local official keys, `15,544`
released-descendant matches, and the frozen `5,368`-root local-disposition
census.  R232 local-promotion semantics are pinned and census-bound but are not
independently reproved here.

## Old package defects closed

1. The report and cold replay were incorrectly written under
   `deliverables/deliverables/` and were absent from the old four-entry
   manifest.  They are audit-only inputs here and receive no old authority.
2. The old package had only a single aggregate digest for the `3,148` output
   rows, no per-row SHA closure, and no input-bound conclusion digest.
3. Its path reads were not a held-FD two-pass/final-path protocol; the frozen
   R179 module was imported by name after path hashing.
4. Its JSON acceptance and ordinary equality did not close nonintegral,
   nonfinite, and bool/int alias cases; it also lacked a final canonical-row
   8 MiB check.
5. Its cold replay text was unsealed narrative, not a manifest member.

## Narrow authority and remaining blockers

The only positive authority is the frozen local R233 parametric graph-key row
partition and its input-bound engineering replay.  This package gives zero
credit to:

- input-bound full support (`3,148` rows still require it);
- physical incidence/equivalence (`3,148` rows still require it);
- representation pullback (`3,148` rows still require it);
- attachment of all `5,368` local dispositions to frozen known blocks;
- normalized support, B1A, B2, maximality, or CM2.

## Frozen hashes

- verifier: `6056bfc1ee917a796d1631368255dd578df6aafb97a2f87cc6d5f31b0f1505e7`;
- row ledger: `4c1a097c2c42dd71323a0276e7bb81dedad330bcdcf02572288009db6c563c1c`;
- ledger payload: `c166c393569116b74886bb173bf7eb38ed4b7672b581d5f4081b082a463f2f41`;
- attack suite: `ebe10211757401a849ee1178202f025b0e4c106f4e64934ccc8b61e830d69240`;
- attack result: `54d0c1c410c6633d622bac7d8952c58c73be385acbdf7fd090d7544a326bca97`;
- verification: `7180d972020c39b0680d47cf0eee34355c64776f0777c88525cd13a7c2893c5b`;
- verification result: `b45d127bec5f1321ceb5ca49a5a2207d8cddfb87d3468da6169b465d4d503391`.

