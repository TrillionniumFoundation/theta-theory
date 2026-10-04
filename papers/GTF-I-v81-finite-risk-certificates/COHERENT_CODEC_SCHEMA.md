# Exact coherent/preparation code and retraction

`coherent_codec.py encode` takes a legal rational preparation Choi file, a unit quaternion supplied as four canonical rational strings, a positive integer horizon, rational error in (0,1/32], and public output-rank bounds. The prep file is validated as input erasing; the emitted combined instrument is not input erasing. It has data input dimension 2 and output dimension 2n.

The quaternion body is one integer indexing four chart anchors and three digits in [-B,B]. It is serialized as canonical lowercase hexadecimal without leading zeros. Its charged length is ceil log2[4(2B+1)^3], with omitted leading bit padding counted. The target quaternion is globally sign-flipped to make its first maximal-absolute coordinate positive; q and -q therefore have the same encoder output. The exact sphere decoder returns a rational unit quaternion. Its squared coherent hybrid certificate is 48N^2/B^2.

The nested preparation code is the unchanged v68 adaptive schema at error delta/2. Pivot masks and its fixed-length body are charged. Rank may decrease; a zero outcome stays zero. The combined squared error upper bound is twice the sum of the two squared component bounds, which safely includes the triangle cross term. Decode recomputes these bounds, validates their budget, expands exact Choi numerators and checks positivity/trace preservation. This does not certify an unspecified target. Verify replays both encoders and compares the complete canonical code.

The general-d library includes `unitary_atlas_decode` and exhaustive `unitary_atlas_encode`. The latter uses a rational squared-Choi test. A configured finite search cap raises an explicitly inconclusive error; it never declares the mathematical family non-encodable.

`retract` instead accepts any legal memoryless instrument description and returns the preparation centre C_y(I/d). It does not require an input-erasing target and may increase rank. Repeated application agrees as a rational map, even when unreduced denominator encodings differ. This is a separate interface, not the target-rank-preserving codec.

Malformed grids, noncanonical rational or hexadecimal strings, out-of-range words, wrong parameter types, crossed horizons, altered bounds, wrong target quaternion and invalid rank promises are rejected in the finite regression suite. Fractions and integer square roots are used; no floating-point feasibility decision occurs.
