# CM2 Round230 cold replay

Date: 2026-07-27

Environment: `.venv-cm2`, Python 3.12, `python-flint 0.9.0`.

Producer replay with `--no-write` reproduced producer
`6b9bac3fd7da301bffb73b0545cc16505df84f69c4f496075cbb146157377cbb`,
result `325993f934e8bd86dc418c019d8e02d9dec5b1731f374f6592e82debb427a94e`,
and encoded certificate
`88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73`.
The last hash equals the stored 67,327,799-byte certificate.

Independent verifier replay with `--no-write` returned
`PASS_INDEPENDENT_ROUND230`, candidate
`88d9d826bd985635d42820c7b66389603ab56a48717531ace525ee2eaf6d3a73`,
and verification result
`051c32a9a338eab20b729cc4e6bc5706ca0a4c3a439dbf80a05f9564da85bbdb`.
Verified census: `8,960` interfaces, `784` accepted, `740` rejected, `448`
stars, and `464` incidence deltas.
