# Round302-C R248 residual single-endpoint sheet disposition closure

## Verdict

**PASS.** Round302-C seals the complete attachment disposition of the 25,336
R248 single-endpoint sheets not promoted by Round300-E.

The scope is deliberately narrow: this is a **complete attachment disposition
frontier**, suitable as an input to a later maximality audit. It does not issue
or prove component maximality. Formal maximality credit is exactly `0`.

## Exact frontier

The complete R248 wall-sheet frontier is partitioned without overlap:

| Tranche | Count | Sealed disposition |
| --- | ---: | --- |
| R300-E single-endpoint sheets | 12,992 | positive owner attachment |
| R302-C residual single-endpoint sheets | 25,336 | fail-closed exclusion |
| R302-A double-endpoint sheets | 32 | fail-closed exclusion |
| **Complete R248 wall-sheet frontier** | **38,360** | complete attachment disposition |

For every residual sheet, Round302-C streams the complete 55,428-row R291
disposition ledger and complete 113,452-row R295-A binding ledger. Every one
of the 25,336 residual sheets fails the first legal attachment predicate:

`P01_NO_R291_SAME_RETAINED_CHILD_AND_SOURCE_CHART_PHYSICAL_CELL`

The exact 0/1 partition is independently reproduced:

- residual sheets with a same-lineage R291 physical cell: `0 / 25,336`;
- R300-E-positive sheets with a same-lineage R291 physical cell:
  `12,992 / 12,992`, exactly one each;
- residual sheets with a same-lineage R295-A exact two-sided graph binding:
  `0 / 25,336`;
- R300-E-positive sheets with that binding: `12,992 / 12,992`, exactly one
  each.

Later equation, base, containment, owner-signature/key, and Round266-root
predicates are not evaluated after P01 fails. Each row records that fact
explicitly and fail-closed.

## Round266 and Round300-C context

All 25,336 residual sheet nodes occur in the complete Round266 valid-virtual
frontier.

- 25,152 owner-bulk nodes are also present and share the sheet's Round266
  component root.
- 184 owner-bulk nodes are absent from the Round266 valid frontier.

The latter is recorded as context, not promoted to a later failure predicate,
because P01 has already failed.

Round300-C contains no direct residual sheet witness. It supplies 272
owner-bulk context witnesses on 272 distinct residual bulks. These bulk
witnesses are non-transferable and contribute zero sheet-attachment credit.

## Output commitments

- disposition rows: `25,336`;
- row IDs:
  `a30f6cddfa7e95b3e59522e03fd0057bc3bae5fc7a726a65327a2943270c8b21`;
- row hashes:
  `67a8c305fa10926f3ae1c69a7d25c2876c8f79788cdd02a6cc6264cef9117e3d`;
- rows:
  `99c6aa1b956c58ef96d8b3ac4cbefeddcd8f927fa235e0f571dbdfad779c3ec3`;
- result self-closure:
  `cdb22066742b427bae5011ed0271dbba4a84bb0dd9838cbd39f5163488ff72bb`.

The gzip ledger is canonical JSON compressed with an empty filename,
`mtime=0`, and compression level 9.

## Independent verification

The verifier never imports, executes, tokenizes, or parses the producer. It
reconstructs all expected rows, result semantics, canonical JSON, and
deterministic gzip bytes before opening candidate artifacts. The producer is
handled only as fixed bytes pinned by:

`e583aff49329c047ae9797084bfba8509b1a3184f2bb04b63de2351f04adbaef`

Candidate byte pins:

- ledger:
  `c326d50f62a427c71e6f41b188b00b08baf6db7bf535ba082f23678239eebba6`;
- result:
  `d371d3d6ce01b0779717dc817216204cf0c142d0b95caf42ede3d1d243d5daa2`.

The verifier rejected all 51 attacks:

| Attack class | Rejected |
| --- | ---: |
| semantically modified and reclosed | 34 / 34 |
| strict JSON | 7 / 7 |
| deterministic GZIP | 5 / 5 |
| path/symlink/hardlink boundary | 5 / 5 |
| **Total** | **51 / 51** |

Attack-suite self-closure:
`a2fc5550dbf3e28095a0c7dfa04e1b994a86d64d253f6bb988c038cc13b1dabc`.

Verification self-closure:
`3ae6e3f6fe7acf6e4d5778e6175f99d5553fa7e201cfab11a381d2573d5e3594`.

## Cacheless replay

Two producer seeds and two verifier seeds were exercised. The second run of
each used a distinct explicit `PYTHONHASHSEED`, `python -B`, and
`PYTHONDONTWRITEBYTECODE=1`.

| Run | Seed / hash seed | Mode | Wall time | Result |
| --- | --- | --- | ---: | --- |
| producer A | `302311` / ambient | write | 2:55.85 | PASS |
| producer B | `302929` / `302929` | write and exact-byte comparison | 3:01.25 | PASS, unchanged |
| verifier A | `302373` / ambient | write | 5:27.37 | PASS, 51/51 rejected |
| verifier B | `302977` / `302977` | `--no-write` and file-pin comparison | 5:20.22 | PASS, unchanged |

The ledger/result file pins remained identical across producer replays.
Attack/verification file pins remained identical across verifier replays.
`seed_affects_output` is `false`.

## Strict nonclaims

Every disposition row is ineligible for component DSU application. The result
and all rows assign:

- eligible component edge count: `0`;
- component edge and union credit: `0`;
- occurrence-identity collapse credit: `0`;
- DSU rank-reduction credit: `0`;
- quotient credit: `0`;
- maximality credit: `0`;
- fibre credit: `0`;
- global-disposition credit: `0`.

No Round301 file and no spike artifact is read by either the producer or the
independent verifier.
