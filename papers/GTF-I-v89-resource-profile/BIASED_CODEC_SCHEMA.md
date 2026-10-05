# Full biased binary-measurement code — Revision 75

## Target and scope

```json
{
  "schema": "gtf75.biased-binary-target/1",
  "bias": "1/5",
  "bloch_vector": ["1/2", "1/3", "1/5"]
}
```

The target is the ordered binary qubit measurement

\[
 E_+=\frac{(1+b)I+x\cdot\sigma}{2},\qquad E_-=I-E_+.
\]

`bias` is the exact rational number \(b\). `bloch_vector` contains either two coordinates in the fixed first-two-Pauli plane or all three coordinates. Every scalar is a canonical rational string, such as `"-1/5"` or `"0"`; floating-point values and unreduced strings are refused. Legality is checked by the exact inequalities

\[
 -1\le b\le1,\qquad \sum_a x_a^2\le(1-|b|)^2.
\]

No rationality assumption is made about \(\|x\|\). Its two spectral probabilities

\[
 p=\frac{1+b+\|x\|}{2},\qquad q=\frac{1+b-\|x\|}{2}
\]

may be irrational. Bias, contrast \(p-q\), and direction all belong to the target and are charged by one payload index. The target is supplied as a finite description. This interface does not learn an unknown measurement from uses of a device.

## Public parameters and exact alphabet

The public parameters are the dimension \(d\in\{2,3\}\), the positive integral horizon \(N\), and the rational requested unhalved trace error \(0<\delta\le1/4\). These determine the entire alphabet. In particular, the bias and spectral probabilities are absent from the public header.

Set

\[
 B=\left\lceil\sqrt{64N/\delta^2}\right\rceil.
\]

There are \(2B+1\) rational spectral grid points:

\[
 P_j=\begin{cases}
 j^2/(B^2+j^2),&0\le j\le B,\\
 1-(2B-j)^2/(B^2+(2B-j)^2),&B<j\le2B.
 \end{cases}
\]

An endpoint layer is an ordered pair \((P_i,P_j)\), \(0\le j\le i\le2B\). For that layer put

\[
 V_{ij}=P_i(1-P_i)+P_j(1-P_j),\qquad
 K_{ij}^2=\frac{N(P_i-P_j)^2}{V_{ij}+1/N}.
\]

If \(i=j\), the layer is one scalar-measurement word and has no angular digits. Otherwise set

\[
 A_{ij}=\max\left\{1,
 \left\lceil\sqrt{128(d-1)K_{ij}^2/\delta^2}\right\rceil\right\}.
\]

Its angular words consist of an axis \(a\in\{0,\ldots,d-1\}\), a sign \(s\in\{-1,1\}\), and \(d-1\) integers in \([-A_{ij},A_{ij}]\). The exact capacity is

\[
 C_{N,\delta,d}=
 \sum_{i=0}^{2B}\sum_{j=0}^{i}
 \begin{cases}
 1,&i=j,\\
 2d(2A_{ij}+1)^{d-1},&i>j.
 \end{cases}
\]

The manuscript proves the covering estimate for this alphabet in Theorem `thm:biasedcodec75`. The program evaluates the finite sum itself; it does not replace it with an asymptotic formula or treat a numerical capacity sample as proof of an optimal rate.

## One charged index

`body_hex` is one lowercase hexadecimal integer in \([0,C_{N,\delta,d})\). Endpoint rows are ordered by increasing \(i\), and layers within a row by increasing \(j\). In a non-scalar layer, the axis/sign index is followed by the \(d-1\) angular digits, ranked in base \(2A_{ij}+1\). Thus the decoder recovers both spectral endpoints, the axis/sign, and all angular digits from the same integer.

`fixed_length_bits` is exactly

\[
 \left\lceil\log_2 C_{N,\delta,d}\right\rceil.
\]

The canonical JSON envelope is not the payload. It also contains the schema, public parameters, derived `spectral_grid`, decimal-string `codeword_count`, derived bit length, `adaptive_error_upper`, and constant scope text. The decoder checks all of these against the derived canonical header. It rejects a missing or additional field, a modified error certificate, an out-of-range index, and noncanonical hexadecimal spelling. A caller cannot add an uncharged bias, contrast, visibility, or direction field.

## Exact encoding and decoding

The encoder quantizes each endpoint in its square-root chart. For a probability \(z\le1/2\), it rounds \(\sqrt{z/(1-z)}\) to the nearest \(k/B\); for \(z>1/2\), it rounds \(\sqrt{(1-z)/z}\) and uses the complementary chart. Midpoint ties go toward zero in the chart coordinate. This scalar quantizer is nondecreasing, so it preserves the order of the two endpoints.

The program never evaluates either of these square roots. Binary search compares the endpoint with the rational function \(t^2/(1+t^2)\), or its complement, and reduces the comparison to the sign of \(c\pm\sqrt{Q}\), where \(Q=\sum_a x_a^2\). It checks the sign of \(c\) before squaring. Equality and negative thresholds are handled explicitly.

For a non-scalar layer, the encoder chooses an axis of maximal \(|x_a|\), breaking ties by the smallest axis index. Write \(s=\operatorname{sign}(x_a)\). The chart coordinates are

\[
 z_b=\frac{x_b}{\sqrt{Q}+|x_a|},\quad b\ne a.
\]

Their magnitudes are rounded to the nearest \(k/A_{ij}\), with midpoint ties toward zero. The sign comparison for \(|x_b|/(\sqrt{Q}+|x_a|)-t\) first checks the sign of \(|x_b|-t|x_a|\) and squares only when that quantity is nonnegative. A zero-contrast decoded layer uses its singleton word and does not request a direction, including at a scalar target \(x=0\).

The decoder maps the rational chart vector \(z\) to the exact unit vector

\[
 u_a=s\frac{1-\|z\|^2}{1+\|z\|^2},\qquad
 u_b=\frac{2z_b}{1+\|z\|^2}\quad(b\ne a).
\]

It returns the rational coordinates

\[
 b'=P_i+P_j-1,\qquad x'=(P_i-P_j)u.
\]

For scalar layers \(x'=0\). Every valid index is legal, including the zero effect, identity effect, rank-one faces, projective measurements, and scalar coins. The two output Choi blocks are exactly \(E_+^T\) and \(E_-^T\) in the input-first unnormalized convention used by `choi_streaming.py`. The output is the existing `gtf66.choi-instrument/1` schema. Its integer numerator matrices share one positive denominator. Positivity and the sum-to-identity constraint are checked with exact rational arithmetic.

## Error budget and replay semantics

The square-root-chart spacing gives a Euclidean Bernoulli square-root-vector error at most \(1/(2B)\) for each spectral endpoint. The same-direction two-coin comparison yields an adaptive unhalved error at most \(2\sqrt N/B\le\delta/4\).

The angular chart has unit-vector chord error at most \(\sqrt{d-1}/A_{ij}\). The finite-use angular upper bound and the chosen angular grid give a second error at most \(\delta/4\). The combined certificate in the header is therefore `adaptive_error_upper = delta/2`, leaving a factor-two margin within the requested error. This statement uses the mathematical upper bounds in the manuscript; matrix legality alone does not establish an adaptive error estimate.

`verify` decodes the codeword and re-encodes the supplied target using the deterministic decisions above. It accepts exactly the canonical code selected for that target. A different valid index is refused even though its decoded measurement is legal. Distinct targets within one lossy quantization cell can share a codeword, so replay is not an injective target identifier. It is also not a universal verifier for arbitrary proof claims or for the distance from any independently chosen codeword.

## Command-line interface

From this paper directory:

```sh
python biased_codec.py encode --input inputs/biased-measurement-3.json --horizon 3 --error 1/8
python biased_codec.py decode --input path/to/code.json
python biased_codec.py verify --input inputs/biased-measurement-3.json --certificate path/to/code.json
python check_biased_geometry.py
```

Each successful command writes one JSON object to standard output. `verify` returns exit status 1 with `verified: false` when canonical replay fails. A malformed input or code returns exit status 2 and a diagnostic on standard error. Duplicate JSON fields are rejected by the actual command-line parser.

## Resources and finite evidence

The reference implementation computes the triangular capacity using \(O(B^2)\) exact arithmetic operations. It retains \(O(B)\) spectral values and row-prefix integers, with a bounded cache of four layouts. It ranks angular words without enumerating them. These are counts of arithmetic operations and stored values, not unit-cost bit-complexity or interpreter-heap bounds. The implementation is pseudo-polynomial in the numerical grid size; the JSON envelope, expanded Choi matrices, temporary integers, and runtime are separate from the charged fixed-length index.

`check_biased_geometry.py` performs exact finite checks of signed radical comparisons, endpoint rounding intervals, the two-sided Bernoulli product constants, the scalar-gauge overlap matrix and its spectral identities, layer ranking, scalar and boundary words, rational effect determinants and traces, the Pauli-Y transpose convention, the algebraic error budgets, serialization, the three command-line actions, and explicit refusal cases. The gauge checks use rational spectral square roots and six rational rotations, multiplying out the normalization factor before comparison. It tests a wrong but legal index separately from illegal matrices. Large-horizon and small-error parameter checks evaluate the grid formulas without claiming to enumerate those large alphabets. The resulting JSON states these limits explicitly; its finite assertions do not replace the continuum or minimax proofs.
