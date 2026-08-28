# CM2 Round306 B1AF4 K2R209 — local outgoing-W half-open owner lineage authority

## Verdict

`GRANTED_LOCAL_AUTHORITY_ONLY`.

The package formally materializes the factor-derived half-open owner and its
dimension-safe local lineage for exactly:

- `17,716` two-dimensional sheet rows;
- `20,456` one-dimensional clipping-incidence rows;
- `40,912` zero-dimensional endpoint-incidence rows.

This is a local row-authority result.  It is not whole-leaf, whole-origin,
whole-tube, physical-component, global-component, or exact-key-disposition
credit.

## Authority boundary

Round195 remains a nonformal feasibility probe and grants **zero** formal
credit.  The positive local result is supported instead by:

1. the pinned Round173 formal seam contract, `E or W owns; N or S excludes`;
2. the pinned Round208 formal leaf, strict-region, face, and U|U rows; and
3. a fresh independent replay that reconstructs all expected rows directly
   from those Round173/Round208 inputs.

Round209 is used only as a pinned producer-side evaluator.  The independent
verifier neither imports nor executes the new producer and neither imports
nor executes the Round209 probe.

## Row-bearing ledgers

| ledger | rows | logical rows SHA-256 | file SHA-256 | bytes |
|---|---:|---|---|---:|
| 2D sheet owner | 17,716 | `5eb916321cd16e2f992aa06dbceb4dd07574ca42ce68e1f5b960fad77666927a` | `3a038e1bfa5d39cccbbf62e0713bf0a6e5e825d5a316296a901ddcec4fbb47ac` | 9,283,213 |
| 1D curve incidence | 20,456 | `9f7c8c04dcaf080b896c92ac2778e0ff63b77a25985b522ce0a6c901879bbb52` | `b9bce03d22ca8179b543e36865e30d4bd98430592ca0b32a3f8bf78285de44d1` | 8,408,222 |
| 0D endpoint incidence | 40,912 | `67cd55ff840f5032830ffa0539683184dcf6842f51a2f6ff6baff9ca52146dff` | `317a9f01bf01851a61eb8893e35bf81918eccee7f882885bf0380c1f12a27159` | 20,592,295 |

Every row contains a complete canonical input commitment and its digest,
then closes the complete row with its own SHA-256.  Sheet commitments bind
the Round173 rule, Round208 result, leaf row, owner region, shadow region,
and (for U|U) the ordering row.  Curve and endpoint commitments additionally
bind their exact parent row hashes and face/endpoint incidence payloads.

The deterministic result object digest is
`2853728a94ba4efba0ba3dc7b47cf47f3505ca4d2f0ccf56409c0909e53d4bd9`.
The result file SHA-256 is
`e8803c4ef98b3157dda2a7ad76edd980164a5d5daea1984bee2f1b038fc905fe`.

## Theorem and lineage checks

All `17,716` nonempty sheets have exactly one owner in `{E,W}` and one
shadow in `{N,S}`.  Owner cells are balanced `E=8,858`, `W=8,858`; shadows
are balanced `N=8,858`, `S=8,858`.  Each of the four active-factor / strict
inactive-sign cases occurs `4,429` times.

The verifier checks the whole-box inactive-factor sign, the identities
`HMINUS=2*Nx` on an `HPLUS=0` sheet and `HPLUS=2*Nx` on an `HMINUS=0`
sheet, the strict owner/shadow factor-sign pairs, and exact equality of the
paired return-signature cores after removing only `outgoing_cell` and
`target_chart`.

All curve rows join exactly one sheet row by ID and row hash.  All endpoint
rows join exactly one curve and one sheet row by ID and row hash.  The exact
identity `40,912 = 2 * 20,456` is enforced.  No incidence row is interpreted
as a physical or global component.

## U|U ordering

All `88` U|U sheets and `76` origins are bound into the local authority:

- owners: `E=44`, `W=44`;
- active factors: `HPLUS=44`, `HMINUS=44`;
- `76` two-curve sheets are strictly ordered and disjoint (`38/38` by order);
- `12` one-curve sheets have the opposite t-face strictly zero-absent;
- local U|U incidences: `164` curves and `328` endpoints;
- curve-pair intersections: `0`.

## Hardening and independent replay

- `18` actual upstream files are fixed by filename, size, and SHA-256.
- Every pin uses held descriptors, two full hash passes, and final file/path
  and directory-identity revalidation.
- Symlinks, hardlinks, path swaps, and TOCTOU changes fail closed.
- No decoded-row spill is used; `TMPDIR` is ignored, making the
  outside-deliverables spill condition vacuous.
- JSON rejects duplicate keys, nonintegral numbers, NaN/infinity, BOM/NUL,
  and noncanonical candidate wire encodings.
- The 8 MiB cap is enforced after successful final row decoding and
  canonicalization.
- Gzip ledgers use `mtime=0` and CRC verification.
- Type-strict equality rejects `false == 0` and `true == 1` aliases.
- The independent attack suite rejected `16/16` coherent mutations.

The final source hashes are:

- producer: `f0aed300fbc212bd24ce5105c75dcf6b08e9df307beaa0805d1babab391fabf5`;
- independent verifier: `a10149563118127d2b536504d75400f59a8ffceb8bcbb92f0e2d7d353d705ba0`;
- attack suite: `091e3fbbea19b6c7476d947858dbfa01119d21e2c762e7953f709ab8f311de0b`;
- verification receipt: `00fa5429c2bb755defbb316c6d342b2a9e2c2411c3b65774f67a84f210872f78`.

## Strict nonpromotion

The formal credit issued is exactly `17,716 + 20,456 + 40,912 = 79,084`
local dimensional owner/lineage rows.  All broader fields remain zero:

- whole-leaf credit: `0`;
- whole-origin credit: `0`;
- whole-original-tube credit: `0`;
- physical-component credit: `0`;
- global-component credit: `0`;
- global exact-key disposition credit: `0`;
- official Source-G dispositions: `0/224,580`;
- `D02=BLOCKED`, Gate5 `10/18`, complete global 18-field blocks `0`;
- `CM2=NO-GO_FOR_CLAIM`.

Remaining work is physical/global component deduplication, whole-object
exhaustion, and immutable global exact-key routing.  This package must not be
used to bypass those gates.
