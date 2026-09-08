# Round 43 ready for review

Round 43 is a fully materialized, line-addressable revision responding to the
Round 42 return-without-review report.  The canonical article is
`ROUND43_REVISION.tex`; no source generator or in-memory rewrite is needed to
read or build it.  The revision branch retains exactly one workflow,
`.github/workflows/verify-round43.yml`, and it has read-only repository
permissions.  Referees should freeze the branch head attached to the review
request, then compare `round43/SOURCE_MANIFEST.json`,
`ROUND43_LOCAL_VERIFICATION.json`, and the committed `ROUND43_REVISION.pdf`
against that immutable object.  The proof ledger expressly distinguishes
mathematical arguments from executable consistency checks.
