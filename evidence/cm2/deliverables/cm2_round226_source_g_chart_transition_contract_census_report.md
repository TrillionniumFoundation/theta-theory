# Round226 source-G chart-transition contract census — frozen report

## Verdict

`PASS_PARTIAL_FORMAL_ROUND226`.

The verifier independently replayed the pinned Round173 `Jx/Jy` parameter
maps and the complete Round220 rejected-coordinate pool without importing or
executing the Round226 producer.  It reconstructed all 16 directed chart
contracts and all 9,830 candidate rows.

The exact coordinate classification is:

- 328 same-chart identity-region rows;
- 16 cross-chart rows whose faces become exactly equal after the pinned
  rational `Jx/Jy` transform;
- 260 rows whose pinned transform produces unequal regions; and
- 9,226 rows with no pinned Klein generator for the chart pair.

The decisive event-trace audit is stronger than this coordinate census:
all 9,830 candidate pairs have zero event-sheet incidence on both endpoint
faces and both endpoint resolved children, and all endpoint faces are marked
`coordinate_stratum_only`.  Therefore none maps to a Round211 sheet pair and
none is eligible for event-trace glue.  The 344 exact coordinate-region
identities are not physical edges.

This closes the Round220 rejected-coordinate pool as a source of event-trace
glue.  It does not prove that a separate transformed-face census over retained
or event-sheet-bearing strata is empty.

## Hostile audit and replay

The verifier rejected `12/12` re-signed semantic attacks, `16/16` strict-JSON
attacks, and `8/8` path/file-object attacks.  Cold replays under hash seeds
`226041` and `226919` both exited zero with identical output.

## Frozen hashes

- producer: `f39e37f410d586a7589ba942b4846b164f38ac06b447b63cf5be9db2f96ac457`;
- certificate: `226e1f350c53fe4d7357ba9a74850e21d5aee5d720c0ea714c460181a6c797e8`;
- certificate result: `8c2a8f0393b4d3d5b4b103e670e2e76b8c1a41f239c0cdc9f35c21ffc90bb088`;
- verifier: `1ae1f5154b383980679a32288f80e57f30f078ab64add13d6c1a2e4f9a9fcad0`;
- verification: `b49d6c65df01851096682a1d1226d096a638ef38c3a0973ee898cc2c095a72e1`;
- verification result: `a4f156431e310c9d322381b828a8225d070b0704935240d2d5e1a53d00fbc2b0`.

## Strict boundary

No physical-glue or component credit is added.  The 7,404 known-connectivity
blocks are not maximal physical components.  D02 remains `BLOCKED`, Gate5
remains `10/18`, and CM2 remains `NO-GO_FOR_CLAIM`.

