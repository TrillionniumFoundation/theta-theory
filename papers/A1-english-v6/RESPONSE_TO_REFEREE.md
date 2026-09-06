# Response to the source-pinned A1 v5 referee report

**Controlling source:** `review/a1-english-v5-harsh-referee-2026-09-06`,
commit `171a7e20470d7e83a5b6b614f60a3434fd3145d7`,
`reviews/a1-english-v5-2026-09-06/REFEREE_REPORT.md` and `CLAIM_AUDIT.md`.
**Reviewed submission:** `20a26285a26cb468206b771c38166fd216283af0`.
**New principal source:** `papers/A1-english-v6/main.tex`.

The report correctly distinguishes the validity of the v5 proof chain from its
judgment of significance. This revision supplies a different central structural
result and genuine sequential and finite-state consequences. It does not recast
the report as a mathematical refutation, assume publication approval, or abandon
the mechanical and first-principles program. The complete v5 source is retained
verbatim as a companion and at its original path.

## E1 — Beyond saturated polynomial spaces

**Action:** Theorem `thm:rank`, Lemmas `lem:mixed-moment` and
`lem:binomial-tangent`, Theorem `thm:causal`, and Proposition `prop:three`.

For every finite real exponent set `A` containing zero, the new law is
`d_A(n,m)=min{n(|A|-1),|mA|-1}`. This is not the invalid rank-only substitution
`(|A|-1)min(n,m)`. At the feasible factors `(1+c_i t^D)/2`, with distinct small
positive `c_i`, the unnormalized product tangent is exactly the monomial space
with exponents

`{0,D,...,nD} union {a+jD : a in A\{0,D}, 0<=j<n}`.

Its size is `n(|A|-1)+1`. A generalized Vandermonde argument and a determinant
integration identity prove strict positivity of every square mixed-moment minor
against the future exponent set `mA`, for every full-support prior, including
priors without a density. The normalized derivative removes exactly one rank.
The proof then supplies the attainable local section, genericity in the actual
command cube, and the global history-encoding upper bound.

Thus the new contribution is not another finite degree count or one numerical
example: it proves transversality throughout the sparse monomial class. The
observation algebra and its Hilbert function determine the future side; the
attainable tangent controls the past side. For three integral exponents we prove
the complete Hilbert formula from the defining homogeneous relation. The
reviewer's example is credited and recovered for every full-support prior, and
its original exact determinant is separately reproduced in the tests.

The theorem does not claim an unsupported rank formula for arbitrary
nonmonomial spaces or suppress a parameter-dependent denominator. Those require
their actual product–test pairing. This is an extension beyond the old full
polynomial theorem, not a restriction or deletion of that theorem.

## E2 — From checkpoint coding to an evolving finite state

**Action:** Definition `def:finite-state`, Lemma `lem:lipschitz`, and Theorems
`thm:stream-upper`, `thm:stream-lower`, `thm:control-bound`.

The new filter reads only `(old index, current command, current report)` and
stores one of `M` indices after every step. Representatives belong to attainable
state sets. It performs `Q_{n+1}(T_n(representative,current input))`; it does not
recompute a state from an exact retained prefix. At the factor-to-moment switch,
it uses the already quantized representative factors.

The proof bounds every update error by
`e_{n+1} <= L_n e_n + C M^(-1/D_A(N))`, iterates this recurrence, and bounds the
squared-prediction excess. At a peak checkpoint, the same fixed independent
uniform-command exploration protocol gives a matching lower power through an
unconditional subprobability minorization and the finite-center volume bound.
Past command seeds are charged; fixing fresh independent coins is a proof device,
not an uncharged historical tape.

The resulting prediction exponent is genuinely streaming at fixed horizon.
For optimal additive observable control the revision proves a separate upper
bound with power `1/D_A(N)`, using attained actions at representatives and Bellman
telescoping. It does not claim a matching control lower bound from the prediction
experiment. Read-only real calibration and execution workspace are not charged
as persistent states; no finite-precision or efficient policy-synthesis theorem
is implied. The executable finite-menu fixture verifies actual index-only
transitions and is expressly not evidence for the continuous-menu asymptotic.

## E3 — Rare probes and useful finite resolution

**Action:** equation `eq:zero-memory` and the immediately following comparison
in Section 5.1; Section 6 supplies a separate common-risk finite-resolution task.

We accept and display the referee's bound: if every probe factor is at most
`v<1`, the zero forecast has regret at most `v^(2m)`. In the shared physical menu
this is `(c+delta)^(2m)`, and `(5/8)^40 < 10^-8`. It is shown alongside the new
streaming upper bound, not buried in the response.

The new result matches the memory exponent at a fixed horizon. Its constants
retain dependence on the horizon, prior, calibration, Jacobian, chart radius and
failure evidence. No horizon-uniform useful-memory claim is made, no rare event
is removed, and no loss is silently rescaled. The independent two-cartridge
comparison predicts placement failure and uses a common total risk; it is not
advertised as a uniform-in-horizon replacement theorem for the old probe score.
The structural advance in E1 and actual streaming construction in E2 stand on
their own declared statements rather than on such an interpretation.

## E4 — A single finite-budget comparison with a common Bayes baseline

**Action:** Theorem `thm:finite-bit-value`, Corollary `cor:threshold`.

The old sign-erasure memory exponents remain structural ablations against each
device's own full-history forecaster. They are not used to order total finite-bit
risk. The new comparison fixes the same two uncensored cartridges and the same
second-cartridge placement-failure variable `Y`. The first raw report is either
kept or deterministically coarsened by merging the signs, then encoded in `M`
states before forecasting `Y`.

For each alphabet the exact optimum is

`R_M = E[h] - max_{partitions Q, |Q|<=M} sum_{B in Q} z_B^2/p_B`.

Randomization cannot improve this optimum. The difference of these common total
risks is nonnegative for every `M`, equals the original strict gain `Delta` at
`M>=4`, and for `M=3` equals `Delta-min_pair delta(pair)`. The two-state case is
completely determined by seven raw and three erased partitions. A separate
analytic argument proves that, for sufficiently small positive amplitude,
`Gamma_M=0` for `M=1,2,3`, while `Gamma_M=Delta>0` for `M>=4`.

This is a positive four-state realization together with an exact resolution
threshold, not an inference from the rank jump. For the report's physical
uniform-prior instance, rational outward enclosures freshly give

`5.6376025880993289137312813786859719e-13 < Delta`

`Delta < 5.6376025880993289137312813786859720e-13`.

The finite partition inequalities also certify `Gamma_2=Gamma_3=0` in that
instance. The small magnitude is retained honestly. The general small-amplitude
result rests on its written proof, not on this one computation.

## P1–P5 — Definitions, attribution and presentation

**P1:** `def:future` explicitly restricts a common continuation to future inputs
and identical task data, without access to distinct old prefixes or seeds. The
constant-gate/repeat-old-command example explains why the quantifier is needed.

**P2:** The abstract, principal theorem and causal theorem distinguish the
posterior-dependent state from a payoff automaton. A finite task automaton
multiplies the charged state count; arbitrary hidden-parameter losses are not
silently included in the observable quotient.

**P3:** Matching powers are called matching exponents, not optimal distortion
constants. Constants and the nonuniform conditioning boundary are stated in the
main results and Section 5.1. The curved-image lower bound uses a projected ball,
not an unjustified flat ball in the entire prediction image.

**P4:** The new narrative uses source-pinned references rather than stale
"current English-v3" or "current referee" labels. The old text is preserved
verbatim in the explicitly archival companion so provenance is not destroyed.
The original PSR paper's PDF title page was also checked: its three authors,
including Satinder Singh, are correctly listed despite the incomplete abstract
page metadata.

**P5:** Section 6 explicitly separates deterministic coarsening of the first
uncensored raw report from the older convention of erasing the sign before a
four-entry comparator is interpreted. No Blackwell ordering of those older
censored experiments is inferred from the new uncensored comparison.

## Execution, preservation and the next referee's remit

The principal manuscript compiled to 16 pages. All pages were rendered; key
proof pages were inspected at full size. New tests completed 101/101 checks,
including 1,057 exact mixed minors, the review's rank-five determinant, sparse
updates, exact physical interval/partition calculations, and an index-only
finite-menu transducer fixture. These counts are not inherited v5 executions.
No formal proof assistant, fresh legacy build, or exhaustive priority review is
claimed. The exact original v5 Git subtree is included unchanged, as are all
existing repository files through the review parent.

The next review should examine the binomial-tangent transversality proof, the
normalization rank loss, the actual causal quantization construction and seed
quantifiers, and the common-risk threshold proof. We submit those full arguments
for scrutiny; an author response does not itself close the editorial judgment.
