# Revision 78 finite-control learning audit

## Scope and status

This audit covers `sections/59-finite-control-learning.tex`, which addresses
frozen r51 required revision 10 and detailed comment 7. The mathematical
object remains a memoryless, consuming, ordered binary measurement with
classical output and no residual quantum output. The new result supplies a
finite trusted-control form of the common learners; it does not change the
unknown-device interface, the future loss, or the training resource.

The hybrid estimate, finite-description construction, algebraic control-flow
check, and resource transfer have been checked symbolically against
Sections 55 and 56. This is a written mathematical audit, not an executed
physical implementation, a statistical simulation certificate, or a
formal proof-assistant verification. PDF production and layout checks are
recorded separately by the revision build.

Stable theorem locations:

| Object | Source label |
| --- | --- |
| Finite-control section | `sec:finitecontrol78` |
| Adaptive hybrid lemma | `lem:controlhybrid78` |
| Uniform pathwise control-error condition | `eq:controlbudget78` |
| Final state bound | `eq:controlhybrid78` |
| Normalized rational-vector approximation | `eq:controlstate78` |
| Learning transfer theorem | `thm:finitecontrollearning78` |
| Preserved device-call orders | `eq:finitecontrolcalls78` |

## 1. Trusted accuracy replaces exact physical preparation

An ideal target state or control is computed from the public parameters
and the complete classical record. An actual trusted preparation need
only approximate that target in **unhalved trace norm**. An actual known
control must approximate the target in **diamond norm**, so its error
promise holds for every input and any retained reference. The actual
state-preparation or control procedure itself has a finite classical
specification and terminates in the declared trusted implementation
model.

The hypotheses remain explicit accuracy promises for available controls.
The theorem does not prove that arbitrary laboratory hardware can realize
the instructions, choose a universal gate set, or guarantee polynomial
state-synthesis time. Preparation time, quantum preparation workspace,
classical computation, and the number of elementary known gates are
separate from the unknown-device call budget.

A quantum instrument is charged as one complete flagged CPTP channel,
including every outcome. If an implementation supplies a separate error
bound for each completely positive outcome map, those bounds must be
summed to obtain the event charge. Postselecting an outcome and
renormalizing it is not an admissible zero-cost substitute for this
complete-channel comparison. Independent entrywise rounding of Kraus
operators is not assumed to preserve complete positivity and trace
preservation.

## 2. Hybrid proof, including record-dependent precision

Let `e_j(h)` be the error charge for the next trusted event after history
`h`. The required condition is

\[
\sum_{j\text{ on }h_*}e_j(h_{<j})\le e
\quad\text{for every complete record }h_*.
\]

It applies to unsuccessful records, off-cone phase estimates, equality
branches, and paths that have zero probability for a particular unknown
effect. Public stopping is padded with identity events. The original and
approximate experiments use the same unknown channel, so an unknown-device
call contributes zero error to this comparison.

At a scheduled event, let `rho` and `rho_tilde` be the ideal and actual
preceding classical–quantum states. Insert the ideal state between their
updates. Contractivity of the actual CPTP map gives

\[
D_j\le D_{j-1}+\sum_h p_{j-1}(h)e_j(h),
\]

where `p` is the **ideal** history distribution. Summing yields the ideal
expectation of the entire pathwise error sum, bounded by `e`. This is why
the proof permits precision chosen after the preceding record without
requiring a separate worst-case supremum at every tree node. A uniform
per-event allocation is a simpler sufficient condition.

A preparation's trace-norm error is sufficient only because it is a
fresh replacement channel: conditional on the record, its output is
tensor-separated from every carried system. Bounds on marginal prepared
states alone would not control hidden correlations across blocks.

The result is an unhalved trace-norm bound `e` on the entire final
classical–quantum state and hence a total-variation bound `e/2` on any
unchanged classical output. No coupling of individual measurement
outcomes, no stability of a branch comparison, and no continuity of the
loss is assumed.

## 3. Exact confidence and precision allocation

For requested `(delta, eta)`, run the ideal learner at the **same loss
target `delta`** and failure allowance `eta/2`. Let `M_* >= 1` be a
computable public upper bound on its unknown-device calls on every
record, after the finite sample-budget convention below.

The explicit learners can prepare an entire fresh input block at one
trusted event. Every such block contains at least one device call, so
there are at most `M_*` preparation events. For each realized history:

| Allocation | Unhalved error allowance |
| --- | ---: |
| Finite normalized rational-vector target versus ideal block state | `eta/(2 M_*)` |
| Trusted actual preparation versus that finite target | `eta/(2 M_*)` |
| Total per fresh block | `eta/M_*` |
| Total on every complete record | `eta` |
| Total variation of returned hypotheses | `eta/2` |
| Ideal statistical failure | `eta/2` |
| Actual statistical failure | at most `eta` |

If a realization instead has additional known control events, replace
`M_*` by a public upper bound on the **total** number of trusted events
and charge every map, including any imperfect randomness source or
imperfect routing operation. A device-call bound alone is not a universal
bound on the number of elementary preparation gates.

For each fixed unknown `E`, the bad-output set is the set of returned
effects `F` for which the original `d_N(M_E, M_F)` exceeds `delta`.
Total variation controls this event even when it depends discontinuously
on `F` or its membership is not tested by the learner. Thus the procedure
requires no `delta/N` preparation precision and no additional statistical
loss allowance. Such a loss allowance would be needed for a separate
perturbation of the final hypothesis, which is not made here.

Halving confidence changes `log(d/eta)` only by an absolute constant
factor in the declared range. The preserved call orders are

\[
O\!\left(d^4N\delta^{-2}\log(d/\eta)\right)
\]

for the original matrix learner and

\[
O\!\left(d^4\frac{N^2}{b}\delta^{-2}\log(d/\eta)\right)
\]

for the learner with block cap `1 <= b <= N`. Its horizon/error/confidence
orders and the original legal-effect output are unchanged. Finite-control
realizations lie inside the corresponding ideal permitted experiment
class, so an already proved lower bound for that class remains applicable.
The scalar case `d = 1` retains its smaller order
`O(N delta^(-2) log(1/eta))`, independently of `b`.

## 4. The actual v77 control flow is computable

The finite executable interface takes integer dimensions/horizons and
rational positive error/confidence targets. A requested real tolerance
can be replaced by a supplied rational tolerance between one half and
the requested value. This retains the original guarantees and constant
orders without postulating an oracle representation for arbitrary real
parameters.

The only sample-budget issue is handled explicitly: for rational `x > 1`,
replace each natural logarithm `log x` in a sample count by

\[
\ell(x)=\min\{k\in\mathbb N:2^k\ge x\}.
\]

The inequalities `log x <= ell(x) <= 1 + log x/log 2` preserve all
concentration and geometric-sum estimates. Remaining multipliers can be
chosen rational, so ceiling operations are then exact integer arithmetic.
In the phase refinement, the squared precision is rational, including
the factor `m/N`. This convention gives a fully computable ideal
reference experiment with conservative sample counts. The hybrid compares
its actual realization with this same reference experiment.

| Operation from Sections 55/56 | Finite computation |
| --- | --- |
| Device frequencies and complex empirical means | Rational arithmetic on finite integer counts |
| Coarse norm threshold, amplitude threshold, endpoint sorting | Exact real algebraic comparisons, including equality |
| Calibration eigenbasis at repeated eigenvalues | Ordered algebraic spectral projections, projection of the public basis, exact zero tests, fixed-order Gram–Schmidt |
| Clipping and normalization | Algebraic eigenvalues and positive square roots with specified ordering |
| Frame choice | Compare the finitely many algebraic absolute inner products; apply the declared first-index tie rule |
| Phase guards and failure fallbacks | Rational inequalities for the empirical complex means; every rejected case has its specified output |
| Phase update after a passed guard | Algebraic root selection described below |
| GHZ preparation phases | Only `0` and `pi/2`, hence amplitude factors `1` and `i`, with a fresh finite sign |
| Embedding into a calibration-selected two-dimensional subspace | Algebraic isometry determined by the finite calibration record |
| Matrix legalization | Enumerate a finite grid in the public basis; exact rational PSD tests; certified algebraic objective approximations with slack |
| Exact matrix codec, if used as output | Finite rational grid and exact rational Sylvester/PSD comparisons |

The phase notation hides no transcendental comparison. For a nonzero
empirical complex number `z` passing the right-half-plane guard, form
`q = z/|z|`. Its `m`th roots are algebraic. The principal root is the
unique root with the largest real part, since the guarded argument lies
strictly inside `(-pi, pi)`. Select that root `v` by exact algebraic
comparison. Then

\[
\tan(\operatorname{Arg}(z)/m)=\operatorname{Im}(v)/\operatorname{Re}(v),
\]

with a strictly positive denominator. The normalization and subsequent
frame operations are therefore algebraic. This validates the finite
computable-expression statement in the v77 learning/code corollary.

Every relevant equality test concerns rational or algebraic data; the
procedure is not required to decide equality of arbitrary computable real
numbers. Exact classical arithmetic here means finite symbolic/integer
algorithms, not an exact physical real-number register. Computation may
be extremely large. Because the finite-outcome record tree has bounded
depth, there is a finite maximum computation over its records; no useful
polynomial bound is claimed.

## 5. Finite state and channel specifications

For a prescribed computable unit vector `psi` in `C^D`, compute a nonzero
Gaussian rational vector `z` with Euclidean error at most `epsilon/8`.
The finite instruction specifies `z` and the rule

\[
\phi=z/\sqrt{\sum_k|z_k|^2}.
\]

Normalization changes the vector error by at most a factor two, and
the unhalved pure-state trace distance is at most twice that normalized
vector error. Therefore the finite target is within `epsilon/2` of the
ideal state. A trusted actual realization within another `epsilon/2`
has the claimed `epsilon` total error.

Coordinate accuracy of order `epsilon/sqrt(D)` suffices. The coefficient
description has

\[
O\!\left(D\log(D/\epsilon)\right)
\]

bits in the fixed public basis, with dimensions and schedule public.
No claim that arbitrary complex unit vectors have dense exactly
normalized rational amplitudes is needed. The normalization is algebraic;
indeed the resulting pure-state density matrix is rational over the
Gaussian rationals because its denominator is `sum |z_k|^2`.

For a known algebraic Stinespring isometry `V`, a Gaussian rational
matrix `A` sufficiently close in operator norm has full column rank.
The specified polar normalization

\[
W=A(A^*A)^{-1/2}
\]

is an exact algebraic isometry. If `||A-V||_op <= r < 1/2`, singular-value
comparison gives `||W-V||_op <= 2r`. The resulting channels have diamond
distance at most `4r`. A finite flagged instrument is covered by keeping
its outcome register. This supplies finite target descriptions preserving
CPTP legality before the separate trusted realization allowance is
applied.

For `K` trusted events the per-event norm target can be `eta/K`. The
precision per coordinate is logarithmic in `K/eta`, with the relevant
dimension factor retained. For a directly described `m`-probe block,
`D = d^m`, so the explicit coefficient bound is

\[
O\!\left(d^m\log(d^mK/\eta)\right).
\]

This can be exponential in block length. It is not a claim about
efficient synthesis, a fixed gate alphabet, or the size of the reusable
classical measurement codeword.

## 6. Freshness, block width, and persistent-memory boundary

The explicit learners prepare fresh product states or fresh embedded GHZ
states. Their approximate replacements occupy exactly the same `m <= b`
probe registers. Preparation workspace is reset or discarded before the
block experiment; no leftover quantum system is carried into the next
block. The finite-control transfer therefore respects the block cap and
does not create additional cross-block entanglement.

For the broader lower-bound experiment class, retaining old quantum
memory is different from allowing it to control future quantum inputs.
A sufficient precise boundary is:

1. Conditional on the full recorded classical history, the next block's
   probes and its own reference are freshly prepared independently of
   the old memory.
2. Until all probes in that block have been consumed, old memory does
   not interact with its probes or its reference. Within-block
   reference-assisted operations remain permitted.
3. After the block is completed, its surviving reference may be merged
   with old memory, and an arbitrary collective final readout is
   permitted. Classical outcomes from instruments on stored memory may
   determine later fresh preparations.

Merely forbidding a direct old-memory/probe unitary is insufficient:
joint measurement of old memory and a new block's entangled reference
before that block is consumed can transfer coherent information into
unused probes. A lower bound for independent fresh blocks must exclude
that transfer or prove a stronger separate amortization statement. The
finite-control construction in Section 59 obeys the stronger freshness
boundary automatically.

## 7. Claims deliberately left outside this result

The theorem does not approximate or discretize the unknown effect, does
not replace the future adaptive loss by one-use or block loss, and does
not alter exact legal output decoding. It does not assert that arbitrary
continuous-outcome adaptive protocols have finite computable decision
trees. Its general hybrid lemma needs a specified finite tree, and its
application verifies that the particular common learners have one.

The finite-outcome alphabet refers to observed device bits, fresh signs,
and any explicitly specified finite flagged controls. Retained quantum
states may still vary over a continuum. Finally, the preparation result
does not remove the separate need for an independent human specialist
priority assessment identified in r51.
