# CM2 Round306B1AF4 K2I2 preserved/non-graph identity and representation index

## Conclusion

`PASS_MECHANICAL_144296_MEMBER_183572_REPRESENTATION_INDEX__ZERO_THEOREM_CREDIT`

This package closes a mechanical identity/owner index for the preserved and
non-graph partial lane.  It does **not** prove normalized full support,
representation set equality, A1/A2, B1A, B2, maximality, fibre disposition,
global disposition, D02/D03/D04, Gate5, or CM2.  Every such formal credit is
zero.

## Exact census

- members: `144,296` = preserved `126,468` + non-graph `17,828`;
- primary engineering representations: `144,296`;
- preserved alias/subcover representations: `39,276` = R294 `39,000` +
  R295A `276`;
- representation candidates: `183,572` = preserved `165,744` + non-graph
  `17,828`;
- authority-gap rows: `6`;
- P1 A1/A2 obligations: `80,092`, explicitly a theorem-obligation census and
  not feature rows.

The eight published anti-joins/uniqueness counters are all zero.  R294's
`46,288` owners dispatch into `39,000` in-scope preserved aliases and `7,288`
out-of-scope R288 residuals.  R294 and R295A preserved target sets are
disjoint.

## Input-bound handles

The global raw-input commitment is
`86188adb64f7d73d0a4fc83434445a29f4490aeb2129c675747c54fa622736e3`.
It binds the three static anchor documents and P1's complete two-pass replay
audit over its raw input pins.

Each primary handle additionally binds its member, coarse/fine family, B0 row
ID/SHA, primary-source row ID/SHA, direct-construction row ID/SHA, and exact
geometry-payload SHA.  Each alias handle additionally binds its owner B0 row,
resolved R294 registry target row, alias source row, representation semantics,
and type-tagged geometry payload.  T2PS payloads bind the transformed
coordinate system, open cell, and exact volume rather than pretending that a
TPS box field exists.  Each gap handle binds its complete gap body and the
global raw-input commitment.

## Determinism and independent verification

Hash seeds `17` and `29` produced byte-identical copies of all four candidate
outputs.  The independent verifier does not import or execute the producer.
It holds static file descriptors, performs two-pass/final-path binding,
replays P1 from a held static source snapshot, reconstructs every expected
row, enforces canonical JSON/gzip order and the 8 MiB decoded-row cap, and
uses recursive type-strict equality.

The verifier reconstructed `144,296` member rows, `183,572` representation
rows, and `6` gap rows exactly.  Its attack suite rejects `false == 0` and
`true == 1` in both directions and confirms that mutations of input-commitment
fields change the digest.

The producer is `36,701` bytes with SHA-256
`c49601ec8884107ed72338ccdec60b6efc4ee18f565deba9021cabce86aad0a0`.
The independent verifier is `37,007` bytes with SHA-256
`02ff536b9e07b3e0f96fd3e00a9855b66693cd0922aef5739542287d668e72b7`.

## Candidate outputs

- authority gaps: `1,146` bytes,
  `8087a64240a9dc250439b62c3d130063cbb9ff8074e88dc182b20ee57e0314b1`;
- member index: `54,523,995` bytes,
  `fbbc37f578219e3167eab1e87f8fc5c67675af4fa6eee979c93d6c0f45d8fc31`;
- representation index: `50,484,688` bytes,
  `68774286f5e25c8e0e41ea42ee3b59fb601ea56d8540ef22e3b949cdce427e83`;
- result: `14,562` bytes,
  `4cd7c9982cdd9a72f34a912d78b6dd061fd8351b31581c84b5aaf20a70893e82`;
- verification receipt: `4,099` bytes,
  `7ba5d17cdbf9818418b272cf47975ed3b0363d1be0512972fc840b759e7c8a98`;
- attack receipt: `513` bytes,
  `4de0b879354d66c7f7766f97481b58c6753fcb24d6f1b1aebbcf300ed98553ca`.

No elapsed time, RSS, timestamp, PID, temporary path, or environment-derived
value is embedded in any candidate or receipt.
