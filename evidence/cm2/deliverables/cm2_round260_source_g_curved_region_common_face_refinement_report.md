# CM2 Round260 Source-G Curved-Region Common-Face Refinement

## Result

Round260 applies a canonical dyadic common-face search to all 11,848 curved-region candidates left fail-closed by Round259.

- Canonical ordering is the shallowest successful depth, then the lexicographically first transverse cell.
- Face depths `1..4` and inward normal corridor depths `1..24` are evaluated with exact rational boxes and independently reconstructed interval geometry.
- 6,728 candidates receive strict positive-area common-face patches and explicit strict three-dimensional corridors on both sides.
- 6,168 accepted patches use the Round208 factor-region geometry; 560 use the Round204 target-graph geometry.
- 5,120 candidates remain fail-closed because none of the 256 depth-4 face cells is strict for both regions: 4,616 Round208 and 504 Round204.

## Geometry Census

- Round208 face depths: depth 1 = 6,144; depth 2 = 24.
- Round204 face depths: depth 1 = 400; depth 2 = 80; depth 3 = 24; depth 4 = 56.
- Exact accepted patch-area sum: `59341379/13107200000`.
- Exact two-sided corridor-volume sum: `5893262088549/879609302220800000`.
- All accepted corridors close by normal depth 17; the certificate records the complete depth histogram.

## Quotient Update

The 6,728 accepted patches produce 3,828 distinct external Round259 component pairs. Deterministic exact-key-pure DSU saturation gives 3,188 rank reductions and 640 redundant independently certified physical edges.

- Unified quotient: `72,064 → 68,876`.
- Occurrence frontier: `53,968 / 53,968` rebuilt.
- Exact-key frontier: `116 / 116` rebuilt.

## Independent Verification

The verifier does not import or execute the Round260 producer. It loads the pinned Round204 and Round208 independent verifier evaluator chains, recomputes all 11,848 canonical searches and corridors, reruns the DSU, and checks every component, occurrence, and key ledger.

- Status: `PASS_INDEPENDENT_ROUND260`.
- Seeds `260071` and `260929` produce byte-identical certificates and verification documents.

## Strict Boundary

The 5,120 unresolved candidates retain zero glue and zero maximality credit. Round260 does not prove component maximality, fibre exhaustion, global dispositions, or additional Gate 5 fields. Gate 5 remains `10/18`; CM2 remains `NO-GO_FOR_CLAIM`.

Next: deepen the remaining 4,616 Round208 and 504 Round204 common-face candidates beyond depth 4, then begin pinned cross-chart transition exhaustion.
