# CM2 Round202 — formal H2 factor t-face C0 absence

Date: 2026-07-26  
Verdict: `PARTIAL_FORMAL_H2_FACTOR_T_FACE_C0_ABSENCE__NO_WHOLE_PARENT_PROMOTION`

## Frozen input and theorem

Round202 selects exactly the 592 frozen Round185 dynamic residual rows whose
status is `H2_FACTOR_EXISTENCE_RESIDUAL`.  Their exact coordinate volume is
`2301/2684354560000`.  The parent distribution is:

- `W:E:00.14.01101`: 264;
- `W:E:02.11.110`: 32;
- `W:E:05.04.001`: 32;
- `W:E:07.01.10010`: 264.

For every selected row, exactly one factor of
`H2=HPLUS*HMINUS` has a strict negative full-box C0 enclosure and is absent.
The other, active factor has strict full-box `dt` and `dp`.  Round202
constructs complete centered mean-value C0 atlases on both endpoint faces
`t-` and `t+`, with exact rational bisection only in `p` and relative depth
at most two.  Both complete endpoint faces have the same strict sign.
Strict monotonicity in `t` therefore excludes an active-factor zero
throughout the box.  Regularity alone is never treated as existence or
absence.

Frozen Round202 input identities:

- producer SHA256:
  `630f0e9177807499eda3a75de368d1fff3c8c3454532558703d08f0f80d33786`;
- certificate file SHA256:
  `d33bf83615b3e5917c02e42e71e5f0cbb8da8eebd2a0b52af38042e1793cfe1c`;
- certificate result SHA256:
  `fe90ce27e02d3cb9a2a20bd0b1eb60572396eef742c41637cda7f00ef512a183`;
- certificate byte count: `13,436,333`.

The complete Round185 six-file package is pinned by its exact manifest,
whose SHA256 is
`ec018e261e866b48039d1cf775e972c6a9b1a9558a1ecf043665c6340ad3dc26`.

## Complete local evidence

The formal evidence ledger contains:

- 592 independently selected and rebuilt evidence rows;
- 1,184 complete endpoint-face atlases;
- 1,568 strict centered-C0 terminal face cells;
- active factors: 296 `HPLUS`, 296 `HMINUS`;
- active endpoint signs: 320 positive, 272 negative;
- outgoing charts: 160 `N`, 160 `S`, 272 `W`;
- maximum face-depth census: 928 at depth 0, 128 at depth 1,
  128 at depth 2.

All terminal cell rows carry exact boxes, exact centers and half-widths,
direct and centered C0 enclosures, full-cell C1 enclosures, exact face area,
and closed row hashes.  Every split records its exact coordinate, child
paths, left half-open ownership, exclusion of the common split face from
the right child, dimension one, and zero credit.  Terminal cell areas
conserve each complete face exactly.

The resulting 592 rows are local exact-key rows with status
`LOCAL_EXACT_KEY_FACTORIZED_T_FACE_C0_ATLAS`.  They carry zero global credit
and zero whole-parent or stratum credit.  No whole-parent, live-stratum, or
global exact-key disposition is issued.

## Exact updated ledgers and conservation

| Ledger | Row count | Exact coordinate/support volume |
|---|---:|---:|
| New Round202 local exact delta | 592 | `2301/2684354560000` |
| Updated dynamic local exact | 19,642 | `139653/1677721600000` |
| Unchanged dimensionally arranged H2 seams | 4,468 | `668529/26843545600000` |
| Updated dynamic residual | 15,238 | `108147/1677721600000` |
| Unchanged inherited residual | 890 | `6903/327680000` |
| Combined remaining residual | 16,128 | `35451507/1677721600000` |

The updated dynamic residual has zero
`H2_FACTOR_EXISTENCE_RESIDUAL` rows.  Its remaining status census is:

- 4,170 `ACTIVE_DELTA_1`;
- 220 `ACTIVE_DELTA_2`;
- 9,076 `POINT_WINNER_NONSTRICT`;
- 1,772 `WALL_ENDPOINT`.

The dynamic output count remains exactly 39,348:

`19,050 + 4,468 + 15,830 = 19,642 + 4,468 + 15,238`.

The exact dynamic output volume remains
`4633329/26843545600000`; the integer and exact-volume deltas are both
zero.  All 16 parent rows remain `PARTIAL`.  The first remaining analytic
blocker is the `WALL_ENDPOINT` row
`W:E:00.14.01101 / 00.14.0110100000000101101001111`.

## Independent verification boundary

The verifier SHA256 is
`bee71997bfb2a04cac3deb200f83e04e4c526d5a903e6442b3cb2e0816f04dd0`.
It pins the Round202 producer only as inert regular-file bytes and never
imports or executes it.  The source contains neither a Round202 producer
import nor the frozen certificate-result digest.

Before importing any evaluator, the verifier pins all six Round185 files
and the exact Round185 manifest.  It imports only the pinned Round185
verifier as a low-level interval-AD evaluator, then repeats the complete
pin after import, after loading the Round183 source ledger, and after all
evaluation.  It also audits that the Round202 producer module is absent
before and after reconstruction.

The verifier independently implements recursive endpoint-face refinement,
cell enclosure construction, factor-role selection, exact source binding,
592 evidence and local rows, the selected/retained key partition, updated
exact and residual hash ledgers, parent rows, first residual, all censuses,
and exact conservation.  It does not import or copy a producer
`build_result`.  Acceptance requires equality of the complete rebuilt
canonical result, whose independently obtained SHA256 is
`fe90ce27e02d3cb9a2a20bd0b1eb60572396eef742c41637cda7f00ef512a183`.

The verification is `PASS`:

- verification result SHA256:
  `5b02b9a36485c0f97ffbd961c768bb7a673caff0de867010fb3b4b68a736ead6`;
- verification file SHA256:
  `8b53ce1c990466d522e844fb2aab89629334d132a3817207fa8b2b0aef7fae71`;
- full expected-result canonical equality: true;
- re-signed semantic attacks rejected: 52/52;
- strict JSON and encoding attacks rejected: 13/13;
- filesystem, path, alias, type, and output attacks rejected: 18/18.

The 52 re-signed attacks cover active/fixed factor roles, fixed-factor
sign, `dt` and `dp` signs, same-sign endpoint faces, terminal enclosures
and row hashes, exact cell and face area, split coordinate/lineage/owner,
Round185 binding, evidence and local row hashes, local-versus-global and
whole-parent credit, exact and residual rows/hash ledgers, all material
censuses and volumes, conservation, parent completion, the first residual,
unchanged dimensions, D02, Gate5, complete global blocks, CM2, and the
top-level partial verdict.  Every forged top-level result digest is
recomputed before rejection.

The strict JSON suite covers duplicate keys, floats and exponents, NaN and
Infinity, BOM, NUL, invalid UTF-8, noncanonical whitespace, a trailing
document, wrong top-level type, missing newline, and CRLF.  The path suite
covers symlink, hardlink, directory, FIFO, oversize, certificate alias and
wrong name, output escape and parent aliases (including a symlink parent),
protected producer/certificate/verifier/Round185 outputs, and existing
symlink, hardlink, FIFO, and directory outputs.

An AST scan of the final verifier found zero duplicate literal dictionary
keys.  All frozen inputs were regular, non-symlink files with link count
one.

## Reproducibility and limitations

Producer seed `202052` and verifier seed `202062` cold replays are
byte-identical to the official certificate and verification.  Exact
commands, timings, memory use, hashes, and comparisons are recorded in the
cold-replay note.

The verifier is independent of the Round202 producer and independently
assembles the complete expected result, but deliberately shares the pinned
Round185 low-level interval-AD evaluator.  It is therefore not a
second implementation of the underlying collision geometry.  The file
checks are fail-closed for the tested types and aliases but are not an OS
sandbox; a narrow concurrent replacement race between metadata inspection
and reading remains outside the package's claim.

## Global state

Round202 makes no global promotion:

- `D02 = BLOCKED`;
- Gate5 remains `10/18`;
- complete global 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.

The next core gate is centered/Krawczyk treatment of the remaining
Delta/root-order, point-winner, wall-endpoint, and inherited
collision1/source carriers.  Whole-parent promotion remains forbidden until
every required dimension under the same exact key is closed.
