# Author-side proof audit — Revision 65

This records checks of written arguments. It is not an independent referee report.

## New proof graph

    exact Hermitian, trace-preserving grid truncation
      -> operator-norm control of the truncation error
      -> explicit diagonal correction and normalization
      -> legal density matrix with a fixed integer denominator
      -> homogeneous repair of subnormalized branch matrices

    Jordan decomposition + trace preservation of the total instrument
      -> sum of branch trace norms contracts
      + repair cost proportional to branch mass
      -> whole classical-quantum history error <= (t+1) delta
      -> every adaptive classical control policy, including zero/rare outcomes

    fixed Gaussian-integer Kraus numerators
      -> integer outcome masses and interval sampling by fair bits
      -> almost-sure termination and bounded-space rejection
      + exact unnormalized numerator fallback
      -> O_input(min(N,L+log(N+1))) writable bits

    pure density target centered at I/d + all legal density decoders
      -> unit target and decoder norm <= 1
      + inherited v62 return-free entropy budget
      + inherited v64 complete-configuration reduction
      -> sharp fixed-program matrix-output space under explicit gap/caps

The process upper theorem does not depend on the spectral chain. The spectral chain does not extend the repeatable-probe classifier.

## Positive rounding

For E=Q_B(rho)-rho, the first d-1 diagonal errors have magnitude below 1/B and the last is at most (d-1)/B. The Hermitian off-diagonal entries contribute twice the squared error in each independent complex coordinate. Thus `||E||_F^2 <= 3d(d-1)/B^2` and `||E||op <= 2d/B`. Adding `(2d/B)I` therefore makes Q positive. Its trace is exactly `1+2d^2/B`.

Normalization gives `(E+eta(I-d rho))/(1+d eta)`, eta=2d/B. The elementary estimate `||I-d rho||_1<=2d` gives the stated safe `6d^2/B` bound. All denominators and signed divisions are explicit. This does not rely on floating eigenvalues.

The old Bloch-coordinate map and the new matrix map are different. The old map preserves a Euclidean ball. Direct matrix truncation without correction can be indefinite; the proof includes a determinant-negative rank-one example. The repair map is nonlinear and is not described as a physical CP map.

## Quantum instruments and adaptive histories

Write each instrument branch as `q^-2 sum M X M*` with fixed Gaussian-integer M and one common integer q. Completeness is an exact identity on the fixed data. Initial and later integer numerators are positive. Their outcome traces are nonnegative integers summing to `q^2 tr(P)`.

The block trace-norm contraction uses the Jordan decomposition of a Hermitian difference, which need not have trace zero on each history. The positive and negative pieces separately have preserved total trace after summing outcomes. The repair error is multiplied by the branch's trace, so summing histories costs delta, not delta divided by a rare probability.

The simulator's conditional numerical state is deterministic given a valid control–outcome history; only the choice of outcome is random. Therefore the subnormalized update in the proof agrees with the executable branch update. A common randomized controller can be conditioned on its private random seed and then mixed; trace-norm convexity preserves the bound. No controller has access to an unrecorded private simulator state.

The bound is for classical transcript plus numerical matrix blocks. It controls any common terminal measurement. It is not a TV bound on exact versus rounded binary matrix strings, a uniform normalized-posterior bound on every rare history, or a simulation of an arbitrary external entangled register.

## Bit model and sampling

Uniform integers below T are drawn by rejecting binary words outside [0,T). Each trial consumes ceil(log2 T) fresh fair bits and uses linear storage. The acceptance probability is strictly greater than one half unless T is a power of two, when it is one. T=1 consumes no random bits. Rejected words and their counts are discarded. Hence there is a worst-case space bound despite only expected-time and almost-sure-termination guarantees.

The selected interval has positive integer mass, so normalization never divides by zero. In approximate mode the new denominator is always B+2d^2, not a product of all previous outcome denominators. Divisions use at most two precision lengths plus fixed-data constants. In exact mode numerators are not divided; their positive integral trace is at most z0*q^(2t). Thus exact arithmetic needs O_input(t+1) bits.

The initial repair adds one error term. The choice B>=6d^2(N+1)2^L budgets every prefix. A capped precision parser selects the exact fallback before constructing a huge grid. Valid input processing, control counters, scratch, addresses and numerical output are charged. CPython and OS entropy implement a reference recurrence, not an allocator- or physical-randomness-certified ideal bit machine.

## Sharp matrix-output lower bound

For every D in D_d, `||D-I/d||_F <= sqrt((d-1)/d)`; equality holds on pure states. This supplies precisely the legal decoder norm needed for the centroid budget. The extension uses the proof of v62's occupation theorem, not an unsupported claim that its original orbit-hull set equals every target hull.

Almost-sure boundary termination and samplewise legality justify stochastic rows and legal conditional-mean decoders. Mean correctness remains the only accuracy requirement for the lower bound. The induced rows may depend on the public clock, making the comparison more permissive.

The finite budget has one logarithmic term and one epsilon*k^(2/p) term. Its dichotomy gives logarithmic configuration count of order at least min(N,L+log N). The work-tape corollary has constants and a starting horizon allowed to depend on the fixed finite program; it does not optimize over arbitrary uncharged hardwired control at each N,L.

The adjacent-coordinate Gaussian-rational unitaries generate SU(d) by the existing torus/Lie-algebra argument. An imported algebraic spectral-gap theorem and the retained least-orbit cap proof supply the converse hypotheses. The implementation never uses a spectral constant. The qubit, qutrit and ququart input files contain all adjacent generators, their inverses, identity, amplitude damping, projective measurements and dephasing. They are not relabeled as the different LPS Bloch alphabet.

## Literature and unchanged conclusions

The Chen–Wu comparison concerns exact strict-cutpoint language equivalence. Positive attenuation can preserve every sign while changing the numerical function. Its elementary example in Section 35 is not asserted as a new general automata principle. Finite-precision density propagation, trace-norm contraction and hybrid arguments are classical ingredients; the new package supplies the explicit legal integer construction and the matching spectral-space consequence.

No proof of the complete multiplicative width crossover, a universal noisy-channel lower bound, arbitrary-dimensional uniform constants, optimal leading constants, or a general disturbing-process finite-state classification is asserted. All inherited mathematical sections and active labels remain. No A/B/C/D analytic completion flag changes.
