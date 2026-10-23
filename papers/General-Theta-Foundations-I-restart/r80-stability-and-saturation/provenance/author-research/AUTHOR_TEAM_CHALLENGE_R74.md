# Separate author-team proof challenge for the R74 developments

## Role and exact scope

This is scrutiny by a separate author-team AI agent. It is not an independent
human referee report, a proof-assistant certificate, an exhaustive priority
review or an editorial assessment. The result is that **no blocking mathematical
defect was found in the specific arguments examined below**. The proofs, with
their hypotheses, remain the mathematical authority.

The following exact file versions were read. A later native integration must
retain their mathematical conditions; a final publication receipt, not this
working-file record, supplies the eventual source commit SHA.

| Examined object | SHA-256 |
|---|---|
| `r74-research/structural.md`, Theorems A–F, Lemma B, and the payoff/threshold/Fourier arguments | `dbe2d6bac479b27e6a563e64c27e28471f7e1e4c16266fce56ed253000706cd4` |
| Final native `sections/37-contrast-memory.tex`, including the full elementary S3 proof | `cbd4fffa320472e1273cf570b6db008bfb849a256f0a638ef8ea6588b3daae17` |
| Final native `sections/38-quotient-memory.tex`, including the robust finite-table corollary | `092daa2329adafb71772fa0ae1bfbdfed99e5eaf88d725e5b5aa38c9cd5d4a17` |
| `r74-research/draftnoisy.tex`, common contraction, the complete finite-order/infinite-order instrument theorem, and inherited four-period specialization | `66d30f83d0a230b9c4eac380098b914505114b6ed9e8a466af5016bbd6d4038f` |
| Superseded draft of `sections/39-instrument-realization.tex`, including the algebraic dictionary construction; this duplicates retained R68 results and is not a new R74 theorem | `f8e6af94a79bda8a98cb675966777b9c9a1ea7a8ebe533ec61e40b14483b66ac` |
| Replacement native `sections/39-instrument-realization.tex`, an explicit bridge to the retained R68 theorem without duplicate new statements | `e909b6a0bda9318ef2ceeea1fc0a3c0432d8fdd76e7d1412a719c9f6706c25f4` |
| Current native `sections/40-joint-contraction.tex` | `aec640ae7b46b95f3cd74a4cd2c9a67694587b30c9fd6981f6d159bca2a43c79` |
| Native `sections/41-conditional-memory.tex`, with the priority/wording changes separately compared to the fully challenged draft | `3e5e00288b8730f5e979098521a5e3d0102d27930c6e2fd465255c0b85d1ef66` |
| Native `supplement-r74-period-four.tex`, explicitly identified as the inherited R69 specialization | `0eefee62aed1d463b99534efc7a7a67fbebeb0e12aad6eadafd521be2a5367f5` |
| Superseded draft `supplement-r74-instruments.tex`; the stronger R68 dictionary lower bound remains authoritative | `0da5e3c4bb0df933ffbdf20ad21757f555ffa554d4e0253c5e8ec6b3e9e29ffc` |
| Separate finite diagnostic `r74-research/challenge_c2_four.py`, including all robust witnesses | `cdecc602737d0eafa45536c47c51fb6db1c7b6fa5e3f94ffdc9ce5dbe51772cf` |

The current native paths are relative to
`papers/General-Theta-Foundations-I-restart/r74-positive-memory-structure`.
The inherited R73 normal form, pure-start formula, module lower bound, R69
first-sector theorem and R70 Perron/relative-spectrum arguments were checked
against the source at `e9d5f2765a2369ed7e136ca02e47fda8f3e9a49b`.

Superseded drafts in the table are historical author-research versions,
not active current theorem files. Their former logical names identify the
inspected argument; the current preservation map gives their archived
location. The original stronger R68 theorem bodies remain current.

## 1. Low terminal contrast and the permutation-module minimum

The proposed saturation theorem was reconstructed independently from the
probability-factorization definition. Its essential positivity step works
for arbitrary finite groups and for multiple outputs.

The invariant part of the cyclic response module is exactly the line spanned
by the group-average probability row. Indeed, averaging every spanning
residual gives that same constant response. A vector in the complementary
zero-average module has total output mass zero. After equivariant embedding
in a minimum permutation module, it is orthogonal to the entire invariant
subspace, so both its coordinate sum and its uniform average vanish. These
facts justify both the probability normalization of the perturbed uniform
initial row and the zero-sum decoder perturbations.

The constants in the draft were checked directly. With
`epsilon=1/(2 k ||a||_infinity)`, every initial coordinate is at least
`1/(2k)`. With `B=max |T(x,c)|/pi_c` and
`t_0=min(1,epsilon/B)`, every decoder entry is nonnegative and every row has
mass one. Equivariance gives the whole group table, hence every command
word. No assertion about positive coordinates in the minimal observable
space is smuggled into this argument.

Zero-average outcomes are legitimately removed because the original response
is a probability table: a nonnegative coordinate with zero group average is
identically zero. At positive contrast the affine change on the module is
invertible and preserves residual equality and the group kernel. The R73
module lower bound and pure-start formula therefore supply the matching
minimum. The zero-contrast constant case must remain separate.

## 2. Normal stabilizers, the LP reduction and its dual

The orbit absorption proof was checked at the action level. Normality gives
`H x h g = H x g`, so the local probability response of a mixed orbit depends
only on `H g`. That response can be used as the decoder from the identity
coset. Contributions from repeated copies of the same normal quotient can
then be merged by their weights. This does not prove absorption for arbitrary
nonnormal stabilizers; the draft correctly keeps that restriction.

The linear subprobability variables have constant row mass `p_H` and recover
both normalization and the common group action. The support function is
computed by choosing an output separately on each coset. A convex hull of
the quotient-table polytopes has the maximum of their support functions,
as used in the payoff criterion. The closest-point separation argument
supplies a strict score when infeasible. The stated `l_1`/supremum-norm
perturbation margin follows directly from the signed pairing.

The family optimization remains a finite combinatorial selection of
polytopes. One separating score excludes one selected family. It must not be
reported as automatically excluding the union of all admissible families;
the full lower certificate can consist of the finite family-by-family
witnesses. The current statements respect this distinction.

For groups all of whose subgroups are normal, the residual stabilizer is
normal and fixes the entire orbit whenever it fixes the initial residual.
Minimal observability therefore makes that stabilizer trivial, proving
`N=|G|`. The bounded feasible LPs have vertices, and the coordinates of a
vertex solve a full-rank linear system over the stated coefficient field.
The rational/same-real-algebraic-field realization claim is consequently
valid; it is not a running-time claim.

## 3. Exact contrast thresholds

For each finite action the full preparation/decoder parameter space is
compact. Feasibility in the contrast parameter is closed. Mixing a feasible
decoder with the constant group-average decoder realizes every smaller
nonnegative contrast, so the feasible set is an initial closed interval.
There are only finitely many actions at a fixed state budget. The endpoint
is therefore attained; the lower memory remains valid at the transition
itself. The group module is unchanged only for positive contrast, which is
why `t=0` is treated separately.

For the normal-subgroup class the endpoint optimization is a bounded LP.
The support-dual formula was checked also in the potentially degenerate
affine-hull case. If the response direction is outside the polytope's affine
span, an annihilating linear functional yields an attained zero endpoint.
Inside that span, a finite inequality description gives an active facet with
positive directional coefficient. This justifies attainment of the dual
infimum without an unstated interior-point assumption.

The native S3 specialization was also checked in full. Its four explicitly
displayed standard-representation matrices span every two-by-two matrix.
Constant and sign-orbit contributions are orthogonal to the standard
matrix coefficients. Therefore the rank-one coefficient identity forces
the natural-orbit initial perturbation and decoder perturbation to be
scalar multiples of the displayed vector. Their positivity bounds give
`t <= 2/3`, even after adding any available fixed or sign orbits to a
five-point action. The three-point construction is valid at equality, and
the residual six-point upper proves the sharp high-contrast branch.
The pure-start minima four and six use the retained initializer formula;
they do not follow from the module dimension alone.

## 4. The five-character family on the four-bit group

The Fourier obstruction and both constructions were reconstructed without
using a numerical optimizer. The five active characters have a unique
five-term dependence and no relation on a proper subset. Thus a quotient
of dimension `r<4` contains at most `r` active characters.

For a core of size at most eleven, a degree-eight orbit would leave room
for at most one additional active character, hence cannot cover all five.
The remaining nontrivial degrees are two and four. Their total cost must
be ten, so every active character occurs in exactly one chosen orbit and
each such orbit reaches the maximum allowed character count. A degree-four
orbit's extra pair-product character is inactive and belongs to no other
chosen orbit. It cannot be cancelled by a different orbit, so its
coefficient must vanish. Positivity then gives
`a_H >= |I_H| t/8`; summation gives `3/8 >= 5t/8`.

The ten-point decoder is bounded exactly on the required low-contrast
interval. In the twelve-point construction, the pair-indicator and
three-variable majority expansions cancel because
`chi_1 chi_2 = chi_3 chi_4 chi_5`. Their constants and active coefficients
are exactly those of the target. This establishes the threshold `3/5`,
including equality on the lower branch. The rank is six, the residual count
sixteen and the module minimum ten. R73 then gives pure-start minima eleven
and thirteen. These are special-family exact values, not a universal formula
for every group.

A separate exact diagnostic enumerated all **67** subspaces of the dual
four-bit space and all **69,728** distinct quotient families of cost at most
eleven. Exactly **52** families cover the target characters: 26 degree-ten
families and their 26 versions with one fixed point. Each satisfies the
unique-assignment and noncancellation properties used in the proof. The
diagnostic also checks the character identities, both constructions,
orthogonality, rank and residual count. It was then extended to reconstruct
the native signed witness for each of the 52 admissible families, hence all
26 distinct singleton/pair partitions. Every stabilizer average is checked
exactly against the claimed nonnegative singleton or pair product. The
score histograms and normalized absolute sums `3/2`, `17/8`, `9/4` agree
with the native table. The final version performed **5,170 exact checks**;
ordinary and optimized Python outputs were identical. This is a finite
independent diagnostic of that example, not proof of the general theorems.

The robust corollary's quantifiers and constants were checked separately.
A table perturbation of size less than `(5t-3)/18` is also smaller than
`t/8` throughout `3/5 < t <= 1`. All five active Fourier coefficients
remain nonzero, retaining the same faithful group and sixteen residuals.
Every action of cost at most eleven must still have the classified partition,
even if extra Fourier coefficients appear. Its own witness has norm at most
`9/4`, while its target pairing is `(3-5t)/8`; the proposed perturbation
radius therefore keeps that pairing strictly negative. This excludes every
candidate family, not just one chosen decomposition. It proves core size
at least twelve and pure-start size at least thirteen. It does not supply
a matching upper outside the exact contrast line, a sharp perturbation
radius, or robustness under a change of command quotient.

## 5. Retained physical posterior positivity and adaptive instrument realization

**Inheritance correction from the full-source comparison.** The proposed
Section 39 and its dictionary supplement were independently compared with
`sections/27-interior-instruments.tex`. The R68 source already proves the
same physical net, uniform branchwise realization, adaptive/stopped-law and
cost transfer, algebraic synthesis, sparse branch rows, and a stronger
universal state-positive dictionary lower bound. In particular its
`thm:r68-noise-exponent` gives `s^(-(h-1))`, stronger than the draft lower
`((1-s)/s)^(h-1)`. These are inherited results, not a new R74 improvement.
The author accepted this finding, retained the complete R68 body unchanged,
and removed the duplicate numbered statements from the active R74 packet;
the inspected drafts are preserved as superseded author research. The
current main Section 39 serves as a bridge to those retained authorities.
The following proof scrutiny documents the inspected draft and its valid
geometry, without reclaiming the inherited results as new.

The projective-space metric, cap measure, packing bound and support-function
argument were checked directly. The cap of sine-distance radius `r` has
measure `r^(2h-2)`. A maximal `sqrt(eta/h)`-separated family has at most
`(4h/eta)^(h-1)` points. Approximating a top eigenvector of an arbitrary
Hermitian test matrix gives the exact support inequality in the native
proof, including indefinite test matrices. Thus the convex hull of those
physical pure states contains every density matrix bounded below by
`eta I/h`.

The hypothesis ranges over **all** incoming density matrices. It therefore
applies to the auxiliary pure states of this dictionary, rather than merely
to the original experiment's reached states. Each branch has a valid
subprobability expansion; a zero-probability positive output is the zero
operator. The initializer is counted and the first outcome is generated
during its transition. Induction gives the stated subnormalized-operator
identity, which is stronger than equality of one terminal expectation.

That identity justifies all terminal POVMs and all common policies based on
the visible history. Conditional policy probabilities are identical in the
two experiments, so finite cylinders and finite stopped histories agree.
Countable additivity and monotone convergence yield the asserted stopped
laws, bounded scores and nonnegative cost expectations. This does not give
a policy access to the simulator's private label. Fixed known primitives and
preparation are essential: no common unknown-model or unknown-input
quantifier follows.

The supplementary lower bound was checked independently. A dictionary
element covering a pure direction at level `1-s>1/2` has a unique top
eigenvector; its other eigenvalues sum to at most `s`. The covered directions
lie in a projective cap with squared sine radius at most `s/(1-s)`. Covering
all directions forces the displayed reciprocal-volume lower bound. It
matches the small-noise power for a **universal physical dictionary**. The
draft expressly does not substitute it for a lower bound on arbitrary
abstract stochastic simulators of one fixed instrument.

The native algebraic-construction addition was checked as well. Given
algebraic `eta`, rank-one projectors and squared separation exceeding
`eta/h` form finite polynomial constraints over the real algebraic numbers.
A feasible system has an algebraic witness obtainable by real quantifier
elimination. The same packing bound forces successive selection to stop;
absence of a further separated point gives the required covering property.
Thus this addition does not rely on approximate sampling of a net or on
replacing a strict covering condition by unverified rounding. Its execution
complexity is not estimated and a general QE computation was not performed.

## 6. Joint contraction

The contraction theorem's common norm is imposed on every command through
one certificate. The packing argument gives a finite net whose convex hull
contains `rho B`; hence every command maps the whole chosen polytope into
itself. The bound on output dual norms makes all auxiliary decoder rows
legal. Actual prefix states are retained separately until the first
transition into that polytope; the stated condition on `T` puts that
transition inside `rho r B`. The empty-word label and the first command are
both counted.

The optional product-bound construction of a common norm also has the right
operator order: appending/prepending one command still gives a word in the
supremum, proving contraction by the chosen `rho`. Equivalence of norms
gives the stated safe radius estimate. This is an existence construction
from a supplied certificate, not a decision procedure for joint spectral
radius or an efficiency guarantee.

## 7. The stationary rank-three instrument family

The Choi lower bound is uniform in the rotation angle. The two subtracted
positive Choi matrices have norms `1/4` and `3/16`, while the depolarizing
Choi matrix is `I_4/2`; the remaining branch is bounded below by `I_4/16`.
The outcome probability intervals therefore hold on every incoming density
matrix. Inserting one unobserved outcome composes with the completely
depolarizing map and factors the probabilities of separated blocks, giving
the stated one-dependence and stationarity from `I/2`.

The selected cylinder probabilities are
`u_n=8^(-n)(1+cos(n theta)/2)/64`. Their three nonzero distinct exponential
modes give a nonsingular three-by-three Hankel minor whenever
`sin(theta) != 0`; real symmetric states give the matching upper rank three.
Deleting inactive states of a proposed hidden model preserves this sequence.
Positive connecting paths bound every entry of the active branch powers by
a multiple of `8^(-n)`. Perron normalization can therefore be applied to the
irreducible block carrying the relative unit phase.

The proof's cycle quantifier was challenged explicitly. Irreducibility
propagates equality in the maximal-modulus eigenvector argument to every
coordinate and every positive edge. Thus every directed cycle has length
divisible by the order `q`. This propagation sentence was added in the
examined final draft. Without a root of unity, no finite block is possible.
With a root of order `q>=3`, every model has at least `q` states.

For the matching upper, the regular `q`-gon contains a disk of radius at
least one half. The third branch's normalized Bloch vector has norm at most
`5/11`, while the first branch permutes the polygon and the second resets to
a vertex. All three branch outputs therefore have valid expansions in the
same `q` vertices. The uniform initialization represents `I/2`; a stationary
hidden initialization can also be obtained by Cesaro averaging without
changing that represented state or the number of labels.

For a pure start on exactly `q` states, the peripheral block must use every
state. It contains a simple directed `q`-cycle. Any extra edge would create
a shorter cycle, so the zero-outcome matrix is a weighted cycle. The
probabilities of `0^n`, for `1<=n<=q`, force every weight to be `1/8`.
The probabilities of `0^n 1` then force every coordinate of `T_1 1` to be
`1/8`. This would give `p(11)=1/64`, whereas the actual process has
`p(11)=3/128`. Thus the extra initializer is necessary, proving the exact
`q+1` pure-start count. The argument excludes arbitrary real hidden
transition probabilities, not only rational or polygon-based competitors.

The algebraic irrational-phase specialization and the distinction between
average depolarization and each conditioned branch are correct. No first
existence claim for one-dependent non-HMM processes is supported by this
challenge. The manuscript must retain its primary-source priority discussion.

The mathematical phase-order mechanism also has explicit classical
antecedents: commensurate-phase exact minima and irrational-phase Perron
obstructions predate this construction. The manuscript's primary-source
comparison with Fanizza--Lumbreras--Winter addresses that history. The
resource theorem here must be assessed through its simultaneous physical
and probabilistic properties and its pure-start lower, not as the first
finite/infinite phase-order dichotomy.

## 8. The four-period correction is inherited

The three-label threshold `1/sqrt(3)` was checked directly against the
already retained R69 first-sector theorem with `M=3` and `theta=pi/2`.
The zero-damping case requires two labels, while the damped four-cycle gives
the upper above the three-label threshold. The new corollary is therefore a
correct explicit consequence of the inherited theorem, not a newly proved
spectral-boundary result. The earlier rational finite-gap certificate remains
a separate valid statement.

## 9. Final native scope and quantifier pass

A final read-only pass at `2026-10-20T13:14:04.821726+00:00` examined the
main wrapper, current overview, Sections 37--41, and the replacement R68
bridge. `FINAL_SCOPE_READ_R74.json` records each actual file hash. The final
main wrapper has SHA-256
`72e5ec3ffba9fd004b0c6971437db596cc5295152eff4dbed5ec59e3e53bd187`;
the overview has
`514e84c4ffa1d20b4e30a344c614a52572af8c589053b8f61ebb860d121e1fb9`.
Sections 37, 38, and 40 remain byte-identical to the proof-challenged
versions in the table. Section 41's additional primary-source attribution
does not change its theorem or proof.

The abstract now specifies groups whose **subgroups are all normal**, the
permutation module **containing the observable module**, and finite phase
orders **q >= 3**. The overview explicitly fixes **one known prepared state**
when quoting the one-initializer R68 bound. The main scope separates exact
simulation from boundary optimization, terminal contrast from repeated
channel damping and branch noise, and physical-dictionary lower bounds
from unrestricted hidden-model lower bounds. The finite-table robustness
statement gives only a lower outside the exact contrast line. The R66/R67
rigid tied criterion and the R68/R69 closures are not reopened.

The newly added Fanizza section citation initially used an undefined key;
this was reported and corrected to the existing bibliography key. The
final cited-key check found no undefined key in any of the seven examined
files. Native compilation remains a separate gate. No unresolved
mathematical or scope defect was identified in this bounded final pass.

## Remaining limits

This challenge does not settle general boundary-optimal feedback, nonrigid
tied minimax classification, the general fixed-memory squared-sign risk
frontier, exact timing frontiers, all-resource complexity, independent Theta
pipeline claims, mathematical novelty or journal suitability. It supplies
bounded written-proof scrutiny and one separately executed finite diagnostic
at the file identities stated above.
