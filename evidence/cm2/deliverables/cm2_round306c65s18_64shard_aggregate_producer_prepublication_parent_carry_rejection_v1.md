# C65s18 aggregate producer pre-publication parent-carry rejection

- Recorded: `2026-08-12T16:14:15+08:00`
- Terminally rejected producer file SHA-256: `345eeb2465951c933893f2e372249e8bcc8d8c072784fa6c6eb2915d5c5a0dd8`
- Superseding producer file SHA-256: `4667ee6471c235980c4368c0999c3170af2d49dbc6eb0a3b0c682644beca87f7`
- Failed command: `--aggregate`
- Fail-closed result: `{"reason":"pair 31 replacement prefix/Kraft","status":"FAIL_CLOSED"}`

The rejected source treated the `23,997` strict-terminal rows present in the
C61 aggregate leaf ledger as the complete parent carry.  The frozen C61 full
12-parent summary also carries `462` C57 and `2,949` C58 earlier terminal
leaves, so the complete C61 base is `48,287` leaves: `27,408` strict terminal,
`20,879` collision-2 handoffs, and zero collision-3 rows.  Omitting those
`3,411` earlier terminal leaves made the incomplete path set fail the first
parent certificate at pair 31.

The failure occurred before either staging build or formal publication.  All
four aggregate output targets and all aggregate staging directories were
confirmed absent.  No shard, authority, runtime, canonical file, or credit
field was changed.  The rejected source must not be used as a producer,
verifier input, manifest member, prerequisite, or credit source.

The superseding source captures and pins the C61 v4 full parent-summary ledger
(`2206c817f49312c519a720e14bc2e152cde5362ed884cbe83d32349a7ff5bab2`),
validates its descriptor, 12 closed rows, exact pair order, base census, and
prefix/Kraft certificates, then replaces each of the `20,879` C2 sources by
its exact descendant partition while retaining all `27,408` base terminal
leaves.  For the frozen C65 shard data this yields `386,327` complete leaves:
`219,072` strict terminal, `167,255` collision-2 handoffs, and zero
collision-3 rows.  The successor remains zero-credit, is not authority, does
not consume C69b/C69c, and still requires independent cold replay after a
successful no-replace publication.
