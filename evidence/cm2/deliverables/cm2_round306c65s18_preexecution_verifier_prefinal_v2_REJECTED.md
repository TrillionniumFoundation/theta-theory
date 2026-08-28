# C65s18 pre-final verifier output rejection

Status: `REJECTED_PREEXECUTION_DIAGNOSTIC__ZERO_CREDIT`

An earlier v2 verifier emitted `independent_preexecution_verification_v2.json`
before its self-test count assertion was corrected from 52 to the actual 53
tests.  No shard was executed.  That pre-final output is excluded from the
final manifest and has zero formal, whole-parent, and D02 gate credit.

Only the final v2 verifier source and the explicitly named `*_final_v2.json`
verification and self-test outputs are eligible preexecution evidence.
