# Resource ledger — Revision 68

The new interior and rank-boundary laws price a reusable target-dependent **classical description** with public family parameters, N and delta. The codebook is allowed to depend on those parameters. In the rank-aware code the target-dependent pivot mask costs at most mn bits and the mixed-radix body costs at most ceil(log2(2D(2B+1)^(D-1))). Declared dimensions, rank bounds and B are not encoded afresh per target. The JSON interchange format and all bound certificates are not the optimal binary payload.

The input is an explicit rational matrix description, not samples of an unknown instrument. Exact PSD validation and Schur preprocessing may use polynomial workspace in that input size. The decoded Choi matrices can be much larger than the compressed index. Integer arithmetic, temporary fractions and serialization are charged separately as construction/decoding cost. No general minimum-workspace theorem is inferred from the codebook lower bound.

The preparation codec is deterministic: it has no sampling loop or fair-bit requirement. The inherited trajectory code still has almost-sure termination/expected time and bounded storage per rejection trial. The full description and maximum command-identifier length remain charged by S in that model.

The tester in d_N is a quantum tester with arbitrary common reference/memory and bounded public stopping. The program-state reduction is a mathematical quantum channel, not a physical finite-classical-message realization. Outcomes remain explicit; transcript TV is half the unhalved classical block trace norm. Rare conditional branches retain the existing weighted/tail/event limitations.

Fixed-dimensional leading coefficients are sharp; the constants in terms of growing dimension, rank, positive margin and validation cost are not claimed optimal.

## Inherited resource accounts

The complete inherited resource accounts are retained in `RESOURCE_LEDGER.json` and `predecessor-v67-audit/RESOURCE_LEDGER.json`.
