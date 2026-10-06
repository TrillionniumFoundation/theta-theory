# Intrinsic instrument codec — exact schema and resource boundary

## Input

Use the v66 `gtf66.choi-instrument/1` schema: positive integer input/output dimensions d,n; positive common denominator; a nonempty ordered outcome list of Hermitian positive semidefinite matrices with Gaussian-integer entries. The sum of output partial traces equals the denominator times I_d. Tensor order is input first and Choi normalization is unnormalized. JSON integers are exact; Boolean values are rejected as dimensions and grid values. Existing CP, tensor-convention and partial-trace checks are reused.

## Coordinates and payload

For each outcome, enumerate rows u and columns v>=u. Diagonals contribute one real coordinate; off-diagonals contribute real then imaginary coordinates. Omit the entire input-index submatrix at one declared outcome and one declared output basis coordinate. Exactly d^2 real coordinates are omitted. There are s=d^2(m n^2-1) digits left. Truncate each retained coordinate toward zero after multiplying by the positive integer grid B. Its digit z lies in [-B,B].

Pack the digits z+B in base 2B+1, in the declared order, including leading zeros. A fixed-size binary payload needs ceil(log_2((2B+1)^s)) bits. The implementation computes this with integer bit_length and emits the nonnegative payload in canonical hexadecimal. In the zero-dimensional singleton case, the mathematical payload is empty and JSON uses the marker `0`.

The omitted submatrix is filled by the exact summed partial-trace identity; no omitted coordinate is transmitted. Add c I to every integer numerator, where c=2nd(1+mn), and divide by D=B+mnc. The result is tested for positive semidefiniteness and exact joint trace preservation. Arbitrary range-valid words can fail positivity and are rejected by the strict CLI. A total mathematical decoder can assign such words the canonical blocks I/(mn).

`active_outcomes` is an increasing index mask in the original outcome list. When `preserve_zeros=true`, exactly zero outcomes are removed before encoding and restored afterwards. The constants and dimension count use the active count. The mask itself is extra header data unless already fixed publicly. Removing a nonzero outcome fails target-bound verification.

## Error certificate

The stored formula K/D, K=3mndc, bounds the sum of Choi-block trace errors and hence diamond error **only for a word produced by the encoder from the supplied target**. `decode` recomputes legality and formula consistency; it cannot certify approximation to an absent target. `verify` recomputes the complete encoder output from a specified rational target and detects tampering. No floating estimate is treated as a coordinate-error certificate.

`adaptive` additionally validates J_y>=aI for the supplied rational margin. It requires 0<a<1/(mn), 0<delta<1 and N>=1, and chooses the integer grid

    B = ceil((K/a) (2 + 4 ceil(sqrt(N))/delta)).

Integer square root and rational arithmetic determine B. The resulting decoded instrument has Choi margin at least a/2. Its common-tester stopped joint trace error after at most N repeated calls is at most delta, by the written theorem. Transcript TV is at most delta/2. The output's reference stability is a property of genuine quantum instruments; no physical classical realization is supplied.

## Costs

The optimality statements concern fixed-parameter payload length. The JSON header, dimensions, mask, common denominator, validity computation, full decoded matrices and input description are not free in an implemented program. Encoding/decoding have polynomial bit complexity in the explicit input and output lengths; these are finite-description operations, not a streaming-space minimizer. Exact Schur validation uses reduced rational fractions with the bordered-minor length bound from the manuscript. The v66 trajectory program and its separately charged preprocessing remain a different program and resource statement.

No statistical channel query, random bit, eigenvector routine or Kraus factorization is used by this codec. The Python interpreter's allocator is not claimed to realize an optimal binary tape implementation.
