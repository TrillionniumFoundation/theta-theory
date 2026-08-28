# C72b2 source 5b9c809d empty stages rejected and superseded

The producer source with SHA-256
`5b9c809d8b0e5dc6ef5dabd69f4c1635779874191ad7df0846a15aea74af26d8`
was stopped before either build emitted a member so that endpoint occurrence
conservation could be strengthened before publication.

The complete rejected stage set is:

- `.cm2-runtime/c72b2-build-a.v2-5b9c809d`: empty directory, no members.
- `.cm2-runtime/c72b2-build-b.v2-5b9c809d`: empty directory, no members.

Neither stage has a ledger, result, report, lock, receipt, or credit.  They
must never be populated, renamed, completed, or consumed.  Only fresh stage
names using the final strengthened successor source hash are eligible.
