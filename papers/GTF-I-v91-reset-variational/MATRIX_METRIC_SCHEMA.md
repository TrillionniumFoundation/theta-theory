# Exact matrix-effect midpoint certificates — Revision 76

## Mathematical object and scope

The input supplies two Hermitian effects on one fixed complex Hilbert
space, `0 <= E,F <= I_d`. Each effect determines the ordered binary
memoryless measurement with effects `E,I_d-E` and no residual quantum
output. The positive integer `horizon` is the maximum number of calls.

The program computes the intrinsic midpoint modulus in Theorem
`thm:matrixmetric76`. Put

\[
H=F-E,\qquad M=\frac{E+F}{2},\qquad V=M(I_d-M),
\]

and solve the strictly positive Sylvester equation

\[
VX+XV+\frac{X}{N}=H.
\]

Then

\[
Q_N(E,F)^2=N\operatorname{tr}(HX).
\]

No eigenbasis is selected, including when the midpoint has repeated
eigenvalues. The finite cutoff `1/N` is retained at every rank and at
both support endpoints.

The certificate contains the exact rational squared bounds

\[
L^2=\frac{\min\{1,Q_N(E,F)^2\}}{(8192d)^2},
\qquad
U^2=\min\{4,64Q_N(E,F)^2\}.
\]

Their meaning is `L <= d_N^na <= d_N <= U`, where the distances use the
unhalved final joint-state trace norm. The upper bound permits retained
references, common adaptive operations, feedback, and bounded public
stopping. Its mathematical validity comes from the theorem and its
proof; the finite computation evaluates its expression for a supplied
pair. The program does not return an exact adaptive distance, produce
an optimal high-dimensional encoder, or learn a measurement from calls
to an unknown device. No triangle inequality for `Q_N` is assumed.

## Supplied-pair format

```json
{
  "schema": "gtf76.matrix-effect-pair/1",
  "dimension": 2,
  "effect_e": [
    [["3/4", "0"], ["0", "0"]],
    [["0", "0"], ["1/4", "0"]]
  ],
  "effect_f": [
    [["1/2", "0"], ["0", "1/10"]],
    [["0", "-1/10"], ["1/3", "0"]]
  ]
}
```

Every matrix entry is a two-element array `[real, imaginary]`, each
component being a canonical reduced rational string. For example,
`["-2/3","1/5"]` denotes `-2/3+i/5`. Integers must be written without a
denominator and zero must be `"0"`. Strings such as `"2/4"`, `"0/1"`,
`"-0"`, `"+1"`, `"01"`, and `"sqrt(2)"` are refused. Expressions are
never passed to a symbolic expression parser. Floating-point entries,
bare JSON numbers in matrix entries, and Boolean numeric substitutes
are refused.

`dimension` must be a positive JSON integer of exact integer type;
`true` is not accepted as `1`. Both matrices must have exactly that
order and must be Hermitian, including conjugate off-diagonal entries
and real diagonal entries. The allowed fields are exactly the four
shown above. Duplicate JSON keys are refused by the actual parser,
including in nested objects. Nonfinite JSON constants are refused.

## Exact legality and linear algebra

Legality is checked separately for `E`, `I_d-E`, `F`, and `I_d-F` by
Gaussian-rational Schur elimination. A negative diagonal pivot refuses
the matrix. At a zero pivot, every remaining entry in that column must
be zero; otherwise the matrix is not positive semidefinite. This step
handles singular effects and avoids the invalid test which checks only
leading principal minors. Each positive pivot is removed by its exact
Schur complement. No floating-point or numerical eigenvalue decision
is used.

For the Sylvester solve, column vectorization gives

\[
\bigl(I_d\otimes V+V^{\mathsf T}\otimes I_d+N^{-1}I_{d^2}\bigr)
\operatorname{vec}(X)=\operatorname{vec}(H).
\]

The implementation uses SymPy's exact domain-matrix inverse to solve
this Gaussian-rational linear system. It then checks the entire
Sylvester residual exactly, checks that `X` is Hermitian, and checks
that `N tr(HX)` is real and nonnegative. It also checks that this number
vanishes exactly when `E=F`. These checks are unconditional runtime
checks, not Python assertions disabled by `-O`.

## Certificate and replay

The certificate has schema `gtf76.matrix-effect-bound/1` and the exact
fields:

| Field | Meaning |
|---|---|
| `dimension`, `horizon` | Positive integer dimension and call horizon |
| `pair_sha256` | SHA-256 of the canonical supplied-pair JSON |
| `q_squared` | Exact reduced rational `Q_N(E,F)^2` |
| `nonadaptive_lower_squared` | Exact rational `L^2` above |
| `adaptive_upper_squared` | Exact rational `U^2` above |
| `sylvester_solution` | Gaussian-rational Hermitian matrix `X` |
| `theorem` | The fixed identifier `thm:matrixmetric76` |
| `normalization`, `scope` | Fixed strings specifying the distance and scope |

Canonical pair JSON sorts object keys, uses compact separators, and
keeps every validated rational string unchanged. Whitespace and object
key order in the original file therefore do not change the identity.
The two effects remain ordered within the supplied pair. A pair with
the same modulus but different matrices does not pass replay merely
because its modulus agrees.

`verify` validates the complete pair and complete certificate, recomputes
the Sylvester solution and all fields, and compares the full canonical
certificate. No extra field is accepted. Changing a bound, changing a
Hermitian solution matrix, changing the pair identity, or swapping the
two hypotheses is refused by replay. The caller may also pin the
expected horizon with `--horizon`; otherwise the certificate's explicit
horizon supplies that public parameter.

A well-formed certificate with different recomputed values returns
`verified: false` and exit code `1`. A malformed pair or certificate
returns exit code `2` with a diagnostic on standard error. A successful
command returns exit code `0` and one JSON object on standard output.
The digest binds this finite certificate to its supplied data; it is
not a signature or a proof of an asymptotic theorem.

## Commands

From the paper directory:

```sh
python matrix_metric.py compute --input inputs/matrix-effect-3.json --horizon 7
python matrix_metric.py verify --input inputs/matrix-effect-3.json --certificate path/to/certificate.json --horizon 7
python check_matrix_geometry.py
python -O check_matrix_geometry.py
```

The four supplied examples have dimensions one through four. They
include a scalar Bernoulli pair, a genuinely complex qubit pair, a
noncommuting three-dimensional pair, and noncommuting rank-two
projections in dimension four.

## Resources and finite evidence

The PSD checks take `O(d^3)` Gaussian-rational field operations under
the usual unit-cost field-operation accounting. The dense Sylvester
formulation has `d^2` unknowns and `O(d^4)` coefficients; conventional
dense elimination or inversion uses `O(d^6)` field operations and
`O(d^4)` stored field elements. SymPy and interpreter overhead, growth
of integer numerators and denominators, the bit length of `N`, and
serialization are additional costs. These are not unit-cost
bit-complexity or Python-heap guarantees. No dimension-independent
practical running-time bound, optimal workspace bound, or optimal
description length is asserted for this reference implementation.

`check_matrix_geometry.py` performs finite exact checks against
Bernoulli product distances and independent qubit formulas; tests
noncommuting Gaussian-rational effects in dimensions three and four;
checks unitary covariance of both the modulus and its Sylvester
solution; and covers scalar, repeated-spectrum, projective, and
one-sided singular strata. It independently checks Schur legality
against all principal minors on the small matrices tested. Interior
effects with rational complementary square roots exercise the
horizontal tangent equations, the vanishing dilation overlap, the
derivative Gram matrix, the anti-Hermitian realizing gauge, and the
regularized residual splitting. The horizontal realization tests use
strictly interior effects; the boundary extension remains the limit
argument in the proof.

Actual CLI cases check duplicate-key refusal, changed values, additional
fields, a pinned horizon, and byte-identical normal/`-O` outputs. The
whole suite is also intended to run in both interpreter modes with
identical JSON results. Its finite assertions are evidence for the
implemented algebra and validation. They do not prove a continuum
metric comparison, a multi-logarithmic entropy law, an optimal coding
theorem, or literature priority.
