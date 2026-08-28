# C64-L global owner decider candidate report v1

Status: `CONSUMPTION_READY_CANDIDATE__911_STRICT_PASS__131_TIES_FAIL_CLOSED__ZERO_CREDIT`.

C64 freezes a queryable global edge-owner decider candidate over the exact C63 scope-overlay bytes. An edge response is an ordered atom-owner vector, preserving span changes along an edge; it is never collapsed to an unjustified single owner.

## Query domain and decisions

- Exhaustive query domain: 1,042 C63 edges; overlap between outcomes: 0.
- Strict PASS: 911 owner-unique edges, containing 11,766 exact atom-owner decisions.
- Selected owners are exact incident occurrences and the unique lexicographic-minimum semantic path on their atom.
- There are 9,932 distinct selected physical occurrences; the largest edge vector contains 31 atoms.
- Fail closed: 131 owner-rule-tied edges, containing 1,337 atoms. Of these, 345 atoms are tied and 992 atoms are individually unique but occur on a blocked edge.
- The 131 blockers are separate records with their exact tied atom spans and occurrence IDs. No arbitrary tie-break is added.

## Input and TOCTOU binding

The candidate pins the exact C63 overlay, atom replay, edge replay, independent verification, and manifest bytes, plus C60 atom and edge bytes. Every producer read uses `O_NOFOLLOW`, requires a regular file with `st_nlink==1`, compares path and file-descriptor identities before reading, rechecks descriptor and path identities after reading, and checks SHA-256.

The cold independent verifier does not import or execute the producer. It reconstructs all 11,766 atom-owner rows, 911 strict edge vectors, and 131 tie blockers from pinned C63/C60 bytes. It passes 30 coherently reclosed semantic attacks and 8 TOCTOU contract attacks (38/38 total). Runtime and canonical snapshots remain unchanged.

## Authority boundary

This object is a consumption-ready authority candidate, not an installed runtime authority. It carries no formal or D02 gate credit. CM2 remains `NO-GO_FOR_CLAIM`.

The structurally observed rooted-anchor-distance condition on the 131 ties is intentionally outside C64's frozen rule and must be evaluated in a separately versioned decider.
