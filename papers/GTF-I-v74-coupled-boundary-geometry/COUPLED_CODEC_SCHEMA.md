# Joint binary-measurement code — Revision 74

## Supplied target

    {"schema":"gtf74.binary-ball-target/1","bloch_vector":["1/2","1/3","1/5"]}

Two coordinates mean the fixed first-two-Pauli disk; three mean the full ball. Strings must be canonical exact rationals. Sum of squared coordinates must be at most one. A unit direction or rational norm is not required. No separate visibility field is accepted.

## Public header and charged body

Public: dimension d in {2,3}, positive integer horizon N, rational error delta in (0,1/4]. Encoder/decoder use the same radial layer table B=ceil(sqrt(64N/delta²)). At layer i>0, r_i=2iB/(B²+i²), and A_i=ceil(sqrt(64(d-1)K(N,r_i)²/delta²)), bounded below by one. The erased layer i=0 has one word; layer i>0 has 2d(2A_i+1)^(d-1) words.

`body_hex` is one lower-case hexadecimal index into the union of all layers. Capacity is `codeword_count`; `fixed_length_bits` is ceil(log2(capacity)). Radial layer, axis/sign and angular grid digits are all recovered from this one index. Visibility is charged in this body, never a free public parameter.

The canonical envelope also includes schema, public parameters, derived radial grid, capacity, error certificate `delta/4`, and scope. The JSON byte length is not the payload. Every field is checked against the derived canonical header; additional, missing, duplicate or modified fields are rejected.

## Correctness boundaries

Every legal index decodes to rational Bloch coordinates in the closed unit ball and to a completely positive trace-preserving ordered binary measurement. Choi blocks are E_+^T and E_-^T in the input-first convention. The decoder proves legality, not that a codeword represents a particular target.

`verify` re-encodes the supplied target, with deterministic chart/tie decisions, and compares the full canonical code. It rejects a valid code for a different target. It is not a universal mathematical verifier, a learned-device estimator, or a physical classical processor.

## Complexity

The reference code enumerates O(B) radial layer sizes and uses exact integer/Fraction arithmetic; angular words are ranked without enumeration. A bounded layer cache accelerates repeated calls. These temporary resources, public header size, expanded matrices and execution time are separate from the fixed-length payload; no optimal-workspace or polynomial encoded-precision claim is made.
