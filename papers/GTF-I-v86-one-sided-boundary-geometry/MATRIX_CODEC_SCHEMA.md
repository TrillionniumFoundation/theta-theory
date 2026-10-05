# Finite exact rational matrix code — Revision 77

## Mathematical interface

`matrix_codec.py` implements the finite construction in
Theorem `thm:matrixcodec77`, using the exact Gaussian-rational routines
of `matrix_metric.py`. A source is a supplied Hermitian matrix
\(E\in\mathfrak E_d=\{0\preceq E\preceq I_d\}\), expressed in the fixed
public input basis. It specifies the ordered binary memoryless
measurement with effects \(E,I_d-E\) and no residual quantum output.

The public parameters are the positive integer dimension \(d\), the
positive integer future horizon \(N\), and a rational accuracy
\(0<\delta\le1\). The operational loss is the unhalved final joint-state
trace norm, maximized over the reference-assisted adaptive testers
specified in Section `sec:matrixmetric76`. The code satisfies
\[
d_N(\mathcal M_E,\mathcal M_{\mathrm{decode}(\mathrm{encode}(E))})
\le \frac{11}{16}\delta.
\]
This guarantee follows from the theorem. The program evaluates exact
matrix expressions; it does not calculate a general exact adaptive
distance or make calls to an unknown measurement.

## Source and decoded-effect format

The source schema is `gtf77.matrix-effect/1`, with exactly these fields:

| Field | Required value |
|---|---|
| `schema` | The string `gtf77.matrix-effect/1` |
| `dimension` | A positive JSON integer of exact integer type |
| `effect` | A square matrix of the declared dimension, in the entry format below |

The supplied scalar example is
`examples/matrix-codec-scalar-source.json`:

```json
{
  "schema": "gtf77.matrix-effect/1",
  "dimension": 1,
  "effect": [
    [["2/7", "0"]]
  ]
}
```

Every entry is a two-element array `[real, imaginary]` of canonical
reduced rational strings. Thus `["-2/3","1/5"]` denotes
\(-2/3+\mathrm i/5\). An integer has no denominator, zero is `"0"`, and
the denominator of a noninteger rational is positive. Examples of
rejected values include `"2/4"`, `"0/1"`, `"-0"`, `"01"`, `"1.0"`,
`"+1"`, and `"sqrt(2)"`; JSON numeric entries and Boolean substitutes
are also rejected. Strings are validated as rational literals and
are never interpreted as symbolic expressions.

The matrix must be Hermitian, with real diagonal entries and
conjugate off-diagonal entries. Exact Schur elimination separately
checks \(E\succeq0\) and \(I_d-E\succeq0\), including at zero pivots.
No spectral margin is required of a source. Duplicate object keys,
missing or extra fields, nonfinite JSON constants, and inconsistent
matrix dimensions are rejected. The decoder returns an effect in
this same schema.

## Code format and the total fixed-length decoder

The wire schema is `gtf77.matrix-effect-code/1`, with exactly these
fields:

| Field | Required value |
|---|---|
| `schema` | The string `gtf77.matrix-effect-code/1` |
| `dimension` | Public positive integer \(d\) |
| `horizon` | Public positive integer \(N\) |
| `accuracy` | Canonical rational string for public \(0<\delta\le1\) |
| `payload` | A string of binary digits of the reconstructed fixed length |

For the supplied scalar source with \(N=1,\delta=1\), the exact code is

```json
{
  "schema": "gtf77.matrix-effect-code/1",
  "dimension": 1,
  "horizon": 1,
  "accuracy": "1",
  "payload": "0011"
}
```

The decoder first reconstructs the entire prescribed dictionary from
the public parameters. If it contains \(M\) retained centres, the
payload length is
\[
B=\lceil\log_2M\rceil,
\]
computed by integer arithmetic as `(M-1).bit_length()`. The length is
determined only after complete enumeration. The binary payload uses
zero-based indexing with leading zeros to reach exactly \(B\) bits.
For each index \(j<M\), the output is the retained centre \(C_j\).
Every remaining word of the same length returns the legal effect
\(I_d/2\). Consequently all \(2^B\) words of the prescribed length
have legal semantics, including unused indices. An empty payload
would be accepted only if the reconstructed length were zero.
Malformed binary strings and strings of the wrong length are
rejected.

For the example, \(K=32\), the legal grid has 33 points, the completed
dictionary has 11 centres, and \(B=4\). The word `0011` decodes to
\(9/32\). Its actual scalar one-use distance from \(2/7\) is
\(2|2/7-9/32|=1/112\). The unused words with indices 11 through 15,
such as `1111`, decode to \(1/2\).

The only source-dependent transmitted data are the \(B\) payload bits.
The JSON object is a readable envelope carrying the public parameters
alongside those bits; its complete UTF-8 byte length is not claimed to
equal \(B\). If the parameters are not already public, the chosen
parameter header must be charged separately. No custom centre list,
matrix-dependent advice, externally supplied dictionary size, or
extra field is accepted by the wire decoder. The in-process
`encode_with_book` and `decode_with_book` helpers permit reuse of an
already completed local construction; they are not additional wire
formats.

## Deterministic construction

Set
\[
K=\left\lceil\frac{32dN}{\delta}\right\rceil,\qquad
s=\frac{2d}{K},\qquad
\eta_{\mathrm{grid}}=\frac{\delta}{16}.
\]
The symbol \(\eta_{\mathrm{grid}}\) here is a deterministic separation
threshold, not a learning failure probability.

The independent real coordinates are ordered as all diagonal entries,
followed by \((\operatorname{Re}G_{ij},\operatorname{Im}G_{ij})\) for
\(i<j\) in lexicographic order. Diagonal grid entries range from 0 to 1
in steps \(1/K\), and other coordinates range from \(-1\) to 1 in the
same steps. All legal matrices are enumerated in the induced order.
The implementation prunes tuples using the necessary inequalities
\[
|KG_{ij}|^2\le
\min\{a_i a_j,(K-a_i)(K-a_j)\},\qquad a_i=KG_{ii}.
\]
Integer square roots implement this pruning exactly. It removes no
legal point and preserves the order of the surviving points.
Full positivity checks of both outcomes remain necessary and are
performed; two-dimensional principal conditions alone are insufficient
in general dimension.

The first legal grid point is retained. A later point \(G\) is retained
precisely when \(Q_N(G,C)^2>\delta^2/256\) for every earlier retained
centre \(C\). For non-diagonal pairs, the square is computed by the
exact regularized Sylvester equation in `matrix_metric.py`. Diagonal
pairs use the identical explicit diagonal formula. No comparison
requires a square-root approximation to \(Q_N\).

The source is moved to \((1-2s)E+sI_d\), and each independent real
coordinate is rounded to the nearest \(1/K\) multiple, with ties
toward positive infinity. Conjugate entries are set together. The
program additionally checks the certified inequalities
\[
\frac dK I_d\preceq G(E)\preceq
\left(1-\frac dK\right)I_d,\qquad
-\frac{3d}{K}I_d\preceq E-G(E)\preceq\frac{3d}{K}I_d
\]
by exact PSD tests. It encodes the first retained centre satisfying
\(Q_N(G(E),C)^2\le\delta^2/256\).

All source operations use supplied Gaussian-rational matrices. The
theorem also explains how an arbitrary real effect represented by
certified rational coordinate approximations can be encoded with the
same bound. The JSON interface does not itself certify a claimed
approximation to an unseen real matrix or learn such a matrix from
device calls.

## Summary and prefix-audit outputs

`summary` emits `gtf77.matrix-effect-codebook-summary/1` only after
complete construction. Its fields are:

| Field | Meaning |
|---|---|
| `schema`, `theorem` | Summary schema and `thm:matrixcodec77` |
| `dimension`, `horizon`, `accuracy` | Public parameters |
| `grid_denominator` | The exact integer \(K\) |
| `legal_candidates` | Number of legal grid matrices in the completed traversal |
| `centres`, `payload_bits` | Completed dictionary size \(M\) and fixed length \(B\) |
| `ordered_centres_sha256` | Digest of the ordered retained effects |
| `complete` | Always `true` for this completed-summary format |
| `scope` | Fixed text identifying complete construction and public-parameter accounting |

The list digest hashes each retained effect's canonical source-schema
JSON followed by a newline, in dictionary order. Canonical JSON uses
sorted keys and compact separators. The parameters are reported
separately in the summary; the digest alone identifies the ordered
list. It is a reproducibility checksum, not a proof of the asymptotic
theorem or an external codebook accepted by the decoder.

`audit-prefix` emits `gtf77.matrix-effect-codec-prefix-audit/1`. It
reports `dimension`, `horizon`, `accuracy`, `grid_denominator`,
`legal_prefix_checked`, `retained_in_prefix`,
`exact_modulus_comparisons`, `prefix_sha256`, and `scope`, together
with the fixed declarations
`full_enumeration_claimed: false` and `codec_produced: false`.
The prefix digest uses all checked legal points in order, not merely
retained points. A prefix is a finite kernel audit. It is never
returned as a dictionary, assigned a fixed payload length, or accepted
as a code by the decoder.

For `encode`, `decode`, and `summary`, the optional positive integer
`--max-candidates` limits the number of legal candidates processed.
If the full traversal would exceed the limit,
`IncompleteConstruction` produces exit code 2 and a diagnostic on
standard error, with no code or summary on standard output. The limit
is not part of the code and does not alter a successfully completed
dictionary. It is not a wall-clock timeout or a bound on rejected raw
coordinate tuples.

Successful commands return exit code 0 and one JSON object on standard
output. Input validation and handled construction failures return exit
code 2. There is no separate `verify` subcommand: `decode` reconstructs
the dictionary and validates the complete code envelope and fixed
payload length.

## Reproducible commands

Run these commands from the paper directory with the dependencies in
`requirements.txt`:

```sh
python matrix_codec.py summary --dimension 1 --horizon 1 --accuracy 1 --max-candidates 33
python matrix_codec.py encode --input examples/matrix-codec-scalar-source.json --horizon 1 --accuracy 1 --max-candidates 33 > /tmp/gtf77-matrix-scalar-code.json
python matrix_codec.py decode --input /tmp/gtf77-matrix-scalar-code.json --max-candidates 33
python matrix_codec.py audit-prefix --dimension 2 --horizon 1 --accuracy 1 --legal-limit 96
python matrix_codec_check.py
python -O matrix_codec_check.py
```

The first three commands complete the scalar construction and
round-trip described above. The fourth command audits a
dimension-two prefix and explicitly reports that it produced no code.
For a reproducible incomplete-construction example:

```sh
python matrix_codec.py encode --input examples/matrix-codec-scalar-source.json --horizon 1 --accuracy 1 --max-candidates 1
```

This last command intentionally exits with code 2 and no payload.

## Size, computation, and finite evidence

The theorem proves, for every fixed \(d\),
\[
M\le C_dN^{d^2/2}
[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}.
\]
Together with the covering lower bound for
\(0<\delta\le\delta_d\), this gives
\[
B=\frac{d^2}{2}\log_2N+
\lfloor d/2\rfloor\log_2\log(N+2)+
d^2\log_2(1/\delta)+O_d(1).
\]
This is a payload bound. The ambient coordinate grid has at most
\[
T=(K+1)^d(2K+1)^{d(d-1)}
\]
tuples. Full construction tests legality and can compare each legal
point with all retained centres. Conventional dense Schur and
Sylvester elimination give the coarse field-operation bound
\(O(Td^3+TMd^6)\). Retaining the centres requires \(O(Md^2)\)
rational entries; a dense Sylvester solve uses \(O(d^4)\) field
entries. Integer numerator and denominator growth, iteration pools,
recursion, SymPy operations, source precision, serialization, and
Python storage add costs. Neither these field-operation estimates nor
the entropy law assert practical efficiency or polynomial running time
in the payload length. The decoder repeats the complete construction.

The recorded run of `matrix_codec_check.py` reports 1,038 exact
assertions, with byte-identical JSON under ordinary Python and
`python -O`. Complete theorem dictionaries were executed only
in dimension one, for \(N=1,2,4\) and \(\delta=1,1/2\). Each of these
six cases checks 38 rational sources against independently computed
exact Bernoulli final-law distances, all fixed-length words, and the
unused-word fallback. The largest completed case has \(K=256\),
257 legal grid points, 73 centres, and a 7-bit payload.

Separate kernel checks exhaust dimension-two grids at \(K=2,3\)
(13 and 40 legal points) and the dimension-three grid at \(K=2\)
(63 legal points). The dimension-two enumeration is compared with
independent necessary-and-sufficient determinant conditions. These
coarse grids are not the theorem's full grids at those dimensions.
Other checks cover strict threshold equality, noncommuting
Gaussian-rational moduli against `matrix_metric.compute`, boundary
rounding, exact ties, CLI replay, malformed inputs, and refusal to
produce a code after a resource cutoff.

For the actual dimension-two theorem parameters \(N=1,\delta=1\),
the regression checks a 96-point legal prefix at \(K=64\), performing
480 exact modulus comparisons. It explicitly records
`full_dictionary_executed_in_dimension_at_least_two: false`.
No completed arbitrary-dimensional dictionary or numerical
computation of a general adaptive operational distance is claimed by
this finite evidence. The general construction, termination, covering
guarantee, and optimal payload order are established in the paper's
proof.
