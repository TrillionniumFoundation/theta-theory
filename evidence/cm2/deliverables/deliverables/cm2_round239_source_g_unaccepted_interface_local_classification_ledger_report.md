# CM2 Round239 — exhaustive local classification ledger

`PASS_PARTIAL_FORMAL_ROUND239`.

Rounds 232, 233, 236, 237, and 238 form a disjoint exhaustive ledger for all
`8,512` Round230-unaccepted resolved/retained interfaces.  Classification
counts are `2,220` whole outgoing signatures, `3,148` outgoing shared-key graph
partitions, `2,640` wall endpoint finite-key partitions, `240` crossing-time
whole signatures, and `264` source-chart-seam whole signatures.

Candidate-key counts are `6,280` one-key, `2,216` two-key, and `16` three-key
interfaces.  The ledger touches all `116` observed exact keys.  It is disjoint
from the `448` Round230 accepted interfaces, and together they exhaust all
`8,960` Round220 interfaces.

The independent verifier returns `PASS_INDEPENDENT_ROUND239`; hash seeds
`239071` and `239929` reproduce certificate
`08d392f43fbc7a8d88c6d70b2c36aed7f8d710aac2f6569cf5910dba240ed9cf`
and verification result
`30bc6de917fd277d9e2ac8daf7300d0e18a6f17a6dfa47e2f5eed6a2cf5b5e42`.

This closes local classification, not incidence.  Known-block, component,
maximality, and global-fibre credits remain zero; CM2 remains
`NO-GO_FOR_CLAIM`.  The next gate is to construct retained/common-refinement
incidence witnesses from these ledger rows to the `7,404` frozen known blocks.
