# CM2 Round306 C43 D02-A prospective dependency-frontier plan v1

Status: **READ-ONLY PLANNING EVIDENCE; ZERO FORMAL CREDIT**.

This plan is derived from the installed C42 authority and the audited C41 B0
inventory.  It does not assume that the C43 candidate is authority.  The C43
candidate remains pending an independent audit and a separate authority
transaction.

## Exact planning pins

- Pair-preserving post-C42 plan SHA-256:
  `780ad6e837e5bcbfc466e47d5e36f3635c0c77dbc45297d95ae6dcc9368093d0`.
- Post-C42 B0 task count: `3,442`.
- Raw whole-pair-gain frontier: `67` tasks over 12 pairs.
- Installed C42 removes pair 391's one task, leaving `66` prospective tasks.
- If and only if C43 later becomes authority, pairs 592 and 715 remove two
  more tasks, leaving `64` prospective whole-pair-gain tasks.

## Prospective post-C43 frontier

The 64 tasks split into two strict queues.

### Direct whole-pair queue: 61 tasks

| pair | task count | category |
|---:|---:|---|
| 1 | 2 | C2 wall endpoint |
| 374 | 6 | C2 wall endpoint |
| 396 | 10 | C2 wall endpoint |
| 739 | 10 | C2 wall endpoint |
| 771 | 18 | C2 wall endpoint |
| 858 | 15 | C2 wall endpoint |

These sources may be adaptively routed in parallel, but they receive no parent
credit until all representative/reflected faces, corners, internal strata and
canonical-owner obligations close.

### Owner-blocked sole-deficit queue: 3 tasks

| blocked pair | sole task | canonical residual owners that must close first |
|---:|---:|---|
| 97 | 1 | pair 668 |
| 211 | 1 | pairs 496 and 783 |
| 664 | 1 | pair 695 |

The prerequisite B0 workloads are exact: pair 668 has 43 tasks, pair 496 has
39, pair 783 has 38, and pair 695 has 7.  These 127 tasks are dependencies, not
immediate whole-pair credit.  Closing only the local interiors of pairs
97/211/664 remains invalid while those canonical owners are residual.

## Execution contract

1. Keep C42 as the installed baseline until C43 independently audits and its
   authority seal commits.
2. Run the six direct whole-pair groups pair-preservingly with adaptive rather
   than fixed-depth termination.
3. Run the four owner prerequisite groups in parallel, retaining exact
   representative/reflected occurrence binding and complete incidence.
4. Recompute canonical ownership after every prerequisite group closes; never
   infer that 97/211/664 became eligible merely from local routing.
5. Accept only strict exclusion, connection to a known component, or a strict
   cemetery/disconnected certificate.  Budget exhaustion is a checkpoint, not
   a terminal disposition.
6. Every graph, endpoint, face, corner and incidence row remains zero ambient
   credit until its complete ownership certificate is installed with the
   parent conservation ledger.

The plan neither promotes D02 nor authorizes D03/D04.  CM2 remains
`NO-GO_FOR_CLAIM`.
