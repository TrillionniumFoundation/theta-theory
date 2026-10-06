# Choi inputs and execution conventions — v66

`choi_streaming.py` uses standard-library integer and reduced rational arithmetic. Every complex integer entry is encoded by `[real, imaginary]`; real integers may also be supplied directly. Integers are mathematical integers, not floating-point approximations. The JSON representation is an interchange format; the theorem measures an explicit binary encoding of its integer data.

## One instrument

An instrument object contains `input_dimension=d`, `output_dimension=n`, `denominator=D` (all positive integers), and a nonempty list `outcomes` of square matrices of order `d*n`. Its optional `convention` must be `input-first-unnormalized`. For an entry indexed `(i*n+alpha,j*n+beta)`, the corresponding action coefficient multiplies `X[i,j]`, without conjugating or transposing that entry. Each numerator is Hermitian positive semidefinite and the sum of their output partial traces equals `D I_d`. The total Choi trace is `d`, not one.

An outcome may be an explicit zero Choi matrix. In the inherited v65 Kraus format the corresponding convention is a nonempty Kraus list containing a zero matrix; an empty Kraus list is not its zero-outcome encoding. The two formats are not interchangeable.

Run the deterministic compiler:

    python choi_streaming.py compile --input inputs/rectangular-choi.json --grid 4096

The output includes the compiled legal instrument, grid, tensor convention and an exact rational diamond-error upper bound. `verify_compilation` recomputes it from the supplied original rational instrument; altered bounds, grids, denominators or blocks are rejected. The exported `repair_grid` routine assumes coordinate error at most `1/B` relative to a valid target to invoke the theorem. It checks output legality but does not infer or certify that input-error promise without a target.

A dyadic input grid does not imply a dyadic compiled channel denominator. Output denominators are `B+m*n*c`. A zero outcome can acquire small positive mass during compilation; that mass is within the proved bound. To preserve known zero outcomes exactly, remove and restore them as described in the manuscript.

## Streaming description

A streaming object has `dimension=d>=2`, `initial_numerator` (a positive nonzero Gaussian-integer matrix), and a nonempty `commands` object. Each command key is a nonempty ASCII identifier without whitespace and maps to one valid square `d`-to-`d` instrument object. The normalized initial state is the numerator divided by its trace. The input dimension, outcome count, denominator lengths and total description length are all charged by the new theorem.

Run:

    printf '8\n2\nxxxxxxxx\n' | python choi_streaming.py stream --input inputs/choi-channel-stream.json

The first two decimal lines are `N>=2` and `L>=2`. Exactly `N` nonspace command bytes follow in the default compact mode. For arbitrary command identifiers use `--tokens` and whitespace-delimited names; token storage is bounded by the longest declared identifier, not by an unbounded incoming word. Outcomes are printed immediately, then the final numerical matrix uses signed hexadecimal numerators and a common positive denominator. Unknown commands, invalid dimensions, non-Hermitian/indefinite matrices and incorrect partial traces are rejected.

Precision is scanned with saturation at `ell_0+NH`; the time to read every supplied digit is still charged. Reduced rational Schur complements validate PSD with polynomially bounded rational operand lengths. This differs from the inherited fixed-dimension validator.

Exact mode stores the selected unnormalized positive numerator. Grid mode fixes its trace to `2^b+2d^2`. Branch probabilities come from the approximate current numerator, not an exact hidden-state oracle. Sampling uses ideal fair bits in the theorem and OS bits in the CLI. Rejection has bounded space per trial and expected, not worst-case, time. The interpreter allocator and OS entropy are not formally certified.

The compiled Choi object describes a genuine mathematical quantum instrument. The numerical streamer does not accept an unknown physical entangled input. A known joint state/controller can be simulated only after its entire rational description and joint dimension are charged.
