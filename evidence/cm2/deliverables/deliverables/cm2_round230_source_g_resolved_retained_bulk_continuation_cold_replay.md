# CM2 Round230 cold replay

Date: 2026-07-27

Environment: project-local `.venv-cm2`, Python 3.12, `python-flint 0.9.0`.

## Producer replay

Command:

`.venv-cm2/bin/python deliverables/cm2_round230_source_g_resolved_retained_bulk_continuation.py --no-write`

Replayed values:

- producer SHA-256: `6b9bac3fd7da301bffb73b0545cc16505df84f69c4f496075cbb146157377cbb`;
- result SHA-256: `325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e`;
- encoded certificate SHA-256: `88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73`.

The replayed encoded certificate hash equals the stored 67,327,799-byte
certificate hash.

## Independent verifier replay

Command:

`.venv-cm2/bin/python deliverables/cm2_round230_source_g_resolved_retained_bulk_continuation_verifier.py --no-write`

Replayed values:

- status: `PASS_INDEPENDENT_ROUND230`;
- candidate SHA-256: `88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73`;
- verification result SHA-256: `051c32a9a338eab20b729cc4e6bc5706ca0a4c3a439dbf80a05f9564da85bbdb`.

The replay matches the stored verification envelope.  The verified census is
`8,960` interfaces, `784` accepted patches, `740` rejects, `448` bridge
stars, and `464` new known-block incidences.
