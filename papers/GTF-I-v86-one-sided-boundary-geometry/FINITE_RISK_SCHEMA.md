# Finite rational readout risk certificates

`finite_risk_certificate.py` replays the general finite-certificate transfer
assertion in Section 64, `thm:finitecertificate81`, using exact Gaussian-rational
arithmetic. It accepts a supplied finite dictionary and a complete rational
collective readout. It regenerates the entire prescribed interior grid and
checks every exact risk inequality. The executable does **not** search for the
general optimal learner or reconstruct the optimal dictionary of
`thm:interiorcodec79`. A successful supplied-dictionary replay alone makes no
query-optimality or payload-optimality claim.

The two committed examples are diagnostic, fully executed scalar certificates.
Neither uses the small-accuracy, small-failure parameters of the headline
learning theorem. The general all-real transfer assertion applies to them.

## Input schema

The schema identifier is `gtf81.finite-risk-certificate/1`. The top-level object
must have exactly the following fields. Additional fields, missing fields,
duplicate JSON keys, nonfinite JSON numbers and noncanonical rational strings
are rejected.

| Field | Type and meaning |
| --- | --- |
| `schema` | Exactly `gtf81.finite-risk-certificate/1`. |
| `dimension` | Positive JSON integer (d); booleans are rejected. |
| `calls` | Positive JSON integer (m). |
| `horizon` | Positive JSON integer (N), or `null` for an operator-risk-only certificate. |
| `a` | Canonical rational string with (0<a\le1), the grid good-label radius. |
| `r` | Canonical rational string with (0<r\le1/4), the public grid covering radius. |
| `alpha` | Canonical rational string with (0\le\alpha<1), the permitted grid failure. |
| `choi_convention` | Exactly `y=1:E^T; y=0:(I-E)^T; left-to-right tensor order; d^(-m)`. |
| `dictionary` | Nonempty ordered list of (d\times d) Gaussian-rational Hermitian centres (C_j\in[I/8,7I/8]). |
| `readout` | Complete ordered list of exactly (2^m) conditional POVMs, as specified below. |
| `target` | `null`, or an object with exactly `accuracy` and `failure`, both canonical rational strings. A nonnull target requires `horizon`, (0<\delta\le2), and (0<\eta<1). |

A rational is written in reduced form: `"0"`, `"1"`, `"-3/8"` are valid;
`"2/4"`, `"-0"`, `"01"`, `"0.5"`, numeric `0.5` and symbolic expressions are
invalid. Every matrix coordinate is a two-element list `[real, imaginary]` of
such strings. For example,

```json
[
  [["1/2", "0"], ["0", "1/8"]],
  [["0", "-1/8"], ["1/2", "0"]]
]
```

represents a (2\times2) Hermitian matrix. Hermiticity is checked explicitly;
the lower triangle is not inferred or repaired. Positivity uses the inherited
exact Schur elimination, including the condition that a zero pivot in a PSD
matrix forces its remaining row and column to vanish.

Each `readout` entry has exactly two fields:

- `y`: the (m)-bit string, including leading zeros;
- `effects`: an ordered list of exactly (L=|\mathcal D|) matrices (A_{j,y}),
  each of dimension (D=d^m).

Branches must appear once each in binary order from the all-zero string to the
all-one string. Every branch is required, including branches with zero
probability for particular effects. Each matrix must be PSD and

\[
\sum_{j=1}^L A_{j,y}=I_D
\]

must hold exactly in every branch. No supplied grid, probability table, PSD
assertion or claimed verification result is accepted as a substitute.

## Complete public grid

The verifier computes

\[
K=\left\lceil\frac{4d}{r}\right\rceil\ge16d
\]

by exact integer arithmetic. It enumerates every denominator-(K)
Gaussian-rational Hermitian matrix in ([I/4,3I/4]). The complete coordinate
stream can be pruned before the PSD tests without losing any admissible point:

- diagonal numerators range from (\lceil K/4\rceil) to
  (\lfloor3K/4\rfloor);
- real and imaginary numerators above the diagonal each range from
  (-\lfloor K/4\rfloor) to (\lfloor K/4\rfloor).

For an interior matrix (G), (\|G-I/2\|_{\rm op}\le1/4), so each
off-diagonal coordinate has modulus at most (1/4). These restrictions
therefore retain every legal grid point. The remaining tuples still undergo
full PSD tests for (G-I/4) and (3I/4-G); coordinate restrictions alone do
not prove matrix positivity.

The stream is ordered by diagonal coordinates first, then real and imaginary
coordinates for upper-triangular pairs in lexicographic order. The report's
`candidate_tuples_checked` counts this entire safely pruned coordinate
superset; `legal_grid_points_checked` counts tuples passing both PSD tests.
The distinction matters in dimension at least two.

The complete finite set is an operator-norm (r)-net. For any real
(E\in[I/4,3I/4]), displace it to

\[
T=(1-8d/K)E+(4d/K)I.
\]

Its spectrum has margin (2d/K) from the two interior boundaries, and
(\|T-E\|_{\rm op}\le2d/K). Coordinate rounding to denominator (K)
adds at most (d/K) in operator norm and stays in the interior. Thus the
complete grid contains a (G) with

\[
\|G-E\|_{\rm op}\le3d/K\le3r/4\le r.
\]

This covering argument is the mathematical input to the transfer; a finite
regression is not its proof.

## Exact risk calculation and all-real conclusion

For each grid point the verifier recomputes

\[
R_y(G)=d^{-m}\bigotimes_{\ell=1}^m G_{y_\ell}^{\mathsf T},
\qquad G_1=G,\quad G_0=I-G,
\]

and

\[
p_j(G)=\sum_y\operatorname{tr}(A_{j,y}R_y(G)).
\]

The blocks are subnormalized. Their traces are the branch probabilities;
there is no division by an unknown branch probability. Transpose is taken in
the fixed public basis and is not replaced by adjoint. Tensor factors follow
the bit string from left to right. For (d=1), the implementation groups the
supplied branch effects by Hamming weight; this is the same exact rational
sum, and the regression independently compares it with binomial probabilities.

The good set is

\[
J(G)=\{j:aI-(G-C_j)\succeq0,\ aI+(G-C_j)\succeq0\}.
\]

Equality is included. A successful replay checks

\[
\sum_{j\in J(G)}p_j(G)\ge1-\alpha
\]

at **every** legal grid point. It records the exact minimum and the first
minimizing point in the deterministic stream.

For the same fixed readout, Choi-state tensor telescoping gives

\[
\|\Gamma_m(E)-\Gamma_m(G)\|_1
\le2m\|E-G\|_{\rm op}.
\]

Consequently the two output-index laws differ in total variation by at most
(mr). Transfer the one fixed label set (J(G)), rather than perturbing a
decision boundary. Its elements satisfy (\|E-C_j\|_{\rm op}\le a+r), so

\[
\sup_{E\in[I/4,3I/4]}
\Pr_E\{\|E-C_J\|_{\rm op}>a+r\}\le\alpha+mr.
\]

The report includes both the raw failure bound and its harmless clipping at
one. When (N) is supplied, both target and centre are in ([I/8,7I/8]), and
the retained interior metric comparison gives the additional certified radius

\[
\min\{2,\;4\lceil\sqrt N\rceil(a+r)\}
\]

in unhalved future distance (d_N). The report deliberately retains this
general comparison even for scalar examples where a sharper conversion is
available.

If an explicit `target` is supplied, both its accuracy and failure must follow
from these transfer bounds. Otherwise the replay is rejected, even if the
underlying grid inequalities pass. With no target, success certifies precisely
the displayed general bounds.

## Relation to the headline parameter recipe

For rational target ((\delta,\eta)), the recipe in Section 64 is

\[
a=\frac{\delta}{8k},\qquad
r=\min\left\{\frac{\delta}{32k},\frac{\eta}{16m}\right\},
\qquad \alpha=\eta/4,\qquad k=\lceil\sqrt N\rceil.
\]

When those exact equalities and (\delta\le2^{-13}), (\eta\le1/8) hold,
the report labels the parameters `theorem-parameter-recipe`. All other
accepted cases are labelled `diagnostic-outside-theorem-range`. This label
classifies only the numerical parameters. The report also explicitly records
that the dictionary is supplied and hash-bound, that the optimal public
dictionary was not reconstructed, and that general optimal-learner synthesis
was not executed. Establishing the optimal call and word-length orders remains
the mathematical content of `thm:rationallearner81`.

The replay concerns ideal Choi preparation and the supplied rational POVM.
Physical trusted-control tolerances are budgeted separately in the manuscript.
They are not silently included in `alpha` or in the grid-to-real buffer.

## Resource cutoff, output and invocation

The CLI defaults to a maximum of 10,000 coordinate tuples. The verifier first
computes the exact size of the complete safely pruned superset. If it exceeds
the limit, the verifier returns `status: "incomplete"`, `complete_grid: false`,
and exit code 2 before allocating that enumeration. This conservative preflight
limit bounds all coordinate tuples, including those that would fail PSD. It
does not certify a prefix and emits no partial risk success.

Invalid structure, an exact risk violation, or an uncertified explicit target
returns `status: "rejected"` and exit code 1. A complete successful replay
returns schema `gtf81.finite-risk-replay/1`, `status: "success"`,
`complete_grid: true` and exit code 0. Canonical JSON of the full supplied
certificate is SHA-256 bound in the report. Strict JSON parsing is shared with
`matrix_metric.loads`, including rejection of duplicate keys.

Run the complete scalar examples with the exact required tuple limits:

```bash
python finite_risk_certificate.py examples/finite-risk-scalar-coarse4.json --max-grid-candidates 17
python finite_risk_certificate.py examples/finite-risk-scalar-binomial4.json --max-grid-candidates 65
python finite_risk_check.py
python -O finite_risk_check.py
```

Suggested source-receipt output names are `REPLAY_FINITE_RISK_SCALAR_COARSE.json`,
`REPLAY_FINITE_RISK_SCALAR_BINOMIAL.json` and `FINITE_RISK_CHECK.json`. The verifier
prints JSON to standard output and does not alter the supplied certificate.

## Executed examples and regressions

Both examples use (m=4), (d=1), (N=1), all 16 bit strings, and the centres
((1/4,1/2,3/4)). They decode at (1/4) for zero or one success, at (1/2)
for two successes, and at (3/4) for three or four successes. Every conditional
POVM is explicitly supplied, with one scalar effect equal to one and the
others zero.

| Example | (a) | (r) | (K) | Complete grid points | Exact worst grid failure (\alpha) | All-real operator radius | Certified all-real failure |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `finite-risk-scalar-coarse4.json` | (1/4) | (1/8) | 32 | 17 | (280125/1048576) | (3/8) | (804413/1048576) |
| `finite-risk-scalar-binomial4.json` | (1/8) | (1/32) | 128 | 65 | (89263805/134217728) | (5/32) | (106041021/134217728) |

The second example has an all-real operator radius strictly below (1/4) and
a failure bound strictly below one. Both examples are explicitly labelled
diagnostic. They exercise completed risk replay; they do not demonstrate a
theorem-scale optimal learner.

`finite_risk_check.py` completes **150 checks with 27 negative controls**. It
independently checks the binomial probabilities at all **82** scalar grid
points, includes norm-boundary equalities, and detects an understated grid
failure by an exact rational difference of (2^{-40}). The negative controls
also cover malformed rationals, dimensions, missing or duplicate branches,
positivity, normalization, dictionary legality, unsupported supplied grids or
probabilities, stronger-than-certified targets and resource exhaustion.

The complex (d=2) tests validate local Choi transpose/tensor identities,
subnormalization and singular PSD cases. In one local experiment the correct
transpose gives probability (3/16), while replacing it by adjoint gives
(5/16). A norm equality at radius (1/8) is accepted and radius (1/9)
is rejected. **No complete (d=2) grid is executed.** The explicit cutoff test
returns incomplete for that case. No test infers theorem validity or priority
from a finite collection of examples.

The complete regression JSON is byte-for-byte identical under normal Python
and `python -O`. Validation uses explicit exceptions, never removable `assert`
statements.
