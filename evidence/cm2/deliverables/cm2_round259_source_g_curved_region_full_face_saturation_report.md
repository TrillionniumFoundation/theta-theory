# CM2 Round259 Source-G Curved-Region Full-Face Saturation

## Result

Round259 certifies the immediately decidable subset of the 13,836 same-signature curved-region boundary-face candidates left fail-closed by Round258.

- 1,988 exact positive-area faces have a full relative-open region proof and explicit strict three-dimensional corridors on both sides.
- 1,764 accepted faces pair one Round208 factor region with a certified whole-box region.
- 224 accepted faces pair two Round204 target-graph regions.
- Accepted axes are `x/y/z = 904/1,068/16`.
- The 1,988 faces induce 1,504 distinct external Round258 component pairs, of which 1,480 reduce rank and 24 are redundant certified physical edges.
- The unified lower-bound quotient decreases from 73,544 to 72,064 components and remains exact-key pure.
- All 53,968 occurrence assignments and all 116 exact-key frontiers are rebuilt.

## Exact Geometry

The Round208 channel evaluates the independently reconstructed `HPLUS` and `HMINUS` factor profiles on the complete common face. The Round204 channel independently evaluates both the source wall factor and target graph factor on the complete common face. Every accepted side then receives the first successful inward dyadic normal corridor at depth at most three.

- Corridor depth histogram: `1: 3,548`, `2: 424`, `3: 4`.
- Exact accepted face-area sum: `2374447/3276800000`.
- Exact two-sided corridor-volume sum: `19879047/1677721600000`.

## Fail-Closed Remainder

No partial face, box contact, signature equality, or key equality receives glue credit.

- 10,784 Round208 candidates require a common dyadic face refinement between two curved factor regions.
- 1,064 Round204 candidates require a common dyadic face refinement because at least one full-face target-graph sign proof fails.
- Total remaining fail-closed candidates: 11,848.

## Independent Verification

The verifier does not import or execute the Round259 producer. It loads the pinned Round204 and Round208 independent evaluator chains, recomputes all 13,836 geometric dispositions, reconstructs the 1,504 external component pairs, reruns the deterministic DSU, and checks the 72,064-component, 53,968-occurrence, and 116-key ledgers.

- Status: `PASS_INDEPENDENT_ROUND259`.
- `PYTHONHASHSEED=259071` and `PYTHONHASHSEED=259929` produce byte-identical certificates and verification documents.

## Strict Boundary

Round259 proves additional physical connectivity only. It does not prove component maximality, global fibre exhaustion, or global exact-key dispositions. Gate 5 remains `10/18`, and CM2 remains `NO-GO_FOR_CLAIM`.

The next core step is dyadic common-face refinement of the remaining 10,784 Round208 and 1,064 Round204 candidates, followed by pinned cross-chart transition exhaustion.
