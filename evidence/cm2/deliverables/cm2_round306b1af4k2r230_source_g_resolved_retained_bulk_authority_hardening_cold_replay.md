# CM2 Round306B1AF4K2R230 cold replay

Date: 2026-08-02

Environment: `.venv-cm2/bin/python`, Python `3.12.3`, python-flint `0.9.0`.
All final commands used `-I -B`; no `PYTHONPATH`, bytecode output, temporary
spill, or `TMPDIR` input was accepted by the package.

Producer seeds `17` and `93` both returned rc `0` and produced byte-identical
`84,467,079`-byte ledgers with SHA-256
`ff604cd343cca5f07cd9fc646a1e1a927bddecdef9a4ebd8f5aab4b39f85110c`.
The ledger object digest is
`c889e348ee0b966f3f97b36ddf200b1610fc8cf0de29d6f0dbc7181c7807e26e`.

The 22-test isolated attack replay returned byte-identical output with SHA-256
`ec32df6cabefd6f3fe452df9ae8e099701104f3d812e42c0988b54ccba17d419`.

The independent full write replay returned rc `0` in `148.01` seconds wall
time with peak RSS `3,092,380` KiB.  The pre-seal no-write replay returned rc
`0` in `147.04` seconds with peak RSS `3,091,968` KiB.  The two modes produced
byte-identical receipts.  They rebuilt all `67,008` input commitments,
executed the pinned legacy independent semantic model without importing or
executing either producer, and finally rehashed all `19` held pins.  It
reproduced `8,960` interfaces, `784` accepted local patches, `740` rejects,
`448` stars, `464` local incidence deltas, `35,896` post-incident occurrences,
and `18,072` post-unattached occurrences.  Verification SHA-256 is
`b2e1465dfadafedab9ecae0080b4884fa833efe0c6e0aadfd11828b272de92a3`.

No member-full-support, representation, membership, maximality, fibre, global
disposition, B1A, B2, D02, Gate5, or CM2 credit is minted by this replay.
