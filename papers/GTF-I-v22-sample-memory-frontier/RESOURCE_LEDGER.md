# Resource ledger — v22

## General response-cover realization

The response alphabet has size d, dictionary size K, dyadic precision r and known response-mean calibration error ρ. For K≥2, the absorbing tournament uses exactly N=n(K−1) candidate training trials plus one candidate and one target validation. Its completed-training width is K(2m+1); during a comparison coin it is at most 3dK(2m+1). The decision width is K. The nested event, its sampler and validation buffers are all covered by the same peak bound.

Each active comparison coin uses r+2 fair bits. Ignored padded trials remain scheduled preparations. The description size is O(K²d(r+3)+log m+log n+log K) for a fixed binary encoding. An external clock provides only predetermined stage/time information. A coarse epoch bound is N(r+3)+r+4; autonomous storage multiplies peak width by at most T+1. No claim of optimal autonomous memory is made.

The error budget is 2^(1−r)+2ρ+4(K−1)θ+2(K−1)[exp(−4θm)+exp(−2nθ²)]. With m=ceil(log(2/δ)/(4θ)) and n=ceil(log(2/δ)/(2θ²)), the comparison error is at most δ. The inherited 12dK-width block realization remains a separate, exponentially longer regime.

## Exact revelation frontier

There are M unknown parameter values, a fixed known prior π, n independent reports and reveal probabilities q_t independent of the parameter. The charged profile is K_t after every report; deterministic construction uses no private randomizer or stored raw history. Terminal decoding is a function of the last state. Known time-dependent nested alphabets are supplied by the clock.

The exact optimum is Bayesian, not a newly claimed minimax value. Its upper bound includes all stochastic encoders and decoders, even arbitrary real transition kernels in that larger mathematical class. Its attained value requires only deterministic transitions. Refining each atomic report into a bitstream is a different interface and must add its intermediate cuts.

## Physical regimes — unchanged task

| Training preparations | Validation preparations | Decision labels | Peak labels | Peak bits (ceiling log2) |
|---:|---:|---:|---:|---:|
| 399 | 2 | 3 | 40602 | 16 |
| 320000 | 2 | 3 | 1604 | 11 |
| 12800·2^400 | 2 | 3 | 12 | 4 |

All three constructions achieve expected signed score strictly above 2/5 on the same stated positive-noise marked collision family. They are upper bounds, not an optimal fixed-sample frontier. The all-auditor decision optimum is three, and the unrestricted finite-schedule physical peak is only bounded between three and twelve. The new deterministic construction needs no sampling precision or private fair-bit register. Its autonomous clock conversion is separately bounded by (6n+12)max(4m+4,12), not by the free-clock peak alone.

## Active updates versus preparations

For the absorbing tournament, ideal expected active updates are at most (K−1)min(n,m²). Conditional drift gives the exact hitting-time expression and the bound m/(2|u−1/2|). Perturbing active reset source rows by α changes the retained output law by at most α E A (truncated at one). Expected signed score pays twice that value, plus validation defects. This does not bound the full raw-data transcript by α E A and does not erase ignored preparations from N.

## Confidence

A base audit uses b+2 preparations and width W≥3. With known dyadic 0<g≤γ and θ=g/8, the absorbing amplifier uses n(b+2) preparations and width at most (2m+1)max(W,9). The block amplifier uses 2LR(b+2) preparations and width at most 4max(W,9), at a much longer clock length. The additional coin uses s+3 fair bits when g has denominator 2^s. The original signed-accumulator and train-once amplifiers remain alternatives. Binary test optimality is not inferred from expected-witness optimality.
