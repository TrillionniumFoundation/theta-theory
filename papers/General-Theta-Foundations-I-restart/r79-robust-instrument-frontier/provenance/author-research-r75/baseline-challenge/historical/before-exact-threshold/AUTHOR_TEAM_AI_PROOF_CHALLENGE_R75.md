# Author-team AI proof challenge — General Theta Foundations I, R75

This is a second author-side AI reading of specified source files. It is not
an independent human referee report, a journal assessment, a formal proof
verification or an editorial recommendation. The exact reviewed source
hashes and the observed integration snapshot are recorded in
`PROOF_CHALLENGE_SOURCE_IDENTITIES_R75.json`.

## Result and scope

No blocking mathematical defect was identified in the reviewed new proof
chain. This judgment covers the finite-group Fourier/multiplicity argument,
the normality/convexity criterion, the strengthened two-level symmetric-group
law, the stationary initialization theorem, the complete noisy-instrument
bounds and rigidity, and the bounded-target-cost stopped-law approximation.
It does not claim that every historical result has been reproved or that the
new results meet a particular journal's importance threshold.

One quantifier ambiguity in an intermediate subgroup-index paragraph was
flagged: the stronger index inequality also requires positive standard
multiplicity. The final reviewed nonabelian draft explicitly includes that
condition. No theorem change was required. The sharper no-intermediate-core
argument was separately challenged after it was proposed and is included in
the final reviewed nonabelian file, SHA-256
`c0a16af16343f7fdc91e99cf33ae67352be243f5a509f9dcca6eb0ffce813ce2`.
At the observed integration snapshot, the root source still contained the
previous endpoint-only section. The identity receipt distinguishes these two
objects; integration of the strengthened section must be verified before
sealing. No unobserved final hash is certified by this note.

The checks below are mathematical source analysis. No diagnostic suite,
quantifier-elimination computation, native build or hosted CI was executed
as part of this proof challenge. Those are separate evidence categories.

## 1. Fourier rank, real descent and positive synthesis

The normalized transform of a left translate is indeed
`A_rho(b) rho(h)`, with the common output blocks stacked vertically. The
cyclic group-algebra span on an irreducible block is exactly
`{A_rho M : M in M_d(C)}`; a rank-r matrix generates r row copies of the
right irreducible module. The trivial block has rank one because it is the
nonzero average probability vector. Taking the maximum of individual output
ranks in place of the vertical stack would be wrong; the manuscript uses the
correct stacked rank.

The complex-to-real injection argument is valid for all real representation
types. In real bases a complex equivariant injection is `A+iB`, and both real
parts are intertwiners. A full-column minor of `A+zB` is a real polynomial
nonzero at `z=i`, so it cannot vanish at every real value. Its degree is at
most the real source dimension, so the stated finite list of real candidates
suffices. This argument avoids an incorrect unqualified identification of
complex multiplicity with real multiplicity for quaternionic types.

For a prescribed G-set, the centered response module has no invariant
vectors. Its equivariant image is orthogonal to invariant rows in the real
permutation space. Thus the chosen uniform row maps to zero under the
projection/inverse map, and the decoder correction has zero row sums.
The preparation perturbation is at most half a uniform coordinate, while
the explicit contrast restriction keeps every decoder entry nonnegative.
Output columns with zero average are identically zero and can be removed and
restored. The nonconstant case ensures the displayed denominators are
positive; the constant case is explicitly separate. These facts justify the
positive matching construction, rather than only a signed or complex linear
factorization.

The orbit-copy lower follows from semisimplicity of finite group modules,
and its integer covering formulation permits every subgroup conjugacy type.
The fixed-orbit copy count remains distinct from an unrestricted optimum.
The small-contrast statement does not claim a full-contrast linear-program
formula for arbitrary nonabelian groups.

## 2. Normality and the exact convexity boundary

For normal H, each response on `H\G` is left-H-invariant, and point
preparation at H realizes every such probability table. This proves the
whole response polytope identity.

For nonnormal H, the subgroup average in the group algebra cannot act as
zero or identity on every irreducible block: otherwise it would be central,
which is equivalent to conjugacy invariance of H. Hence some nontrivial
irreducible has fixed-space dimension strictly between zero and its degree.
The normalized permutation character has a nonzero scalar identity Fourier
block there, with full rank. A single orbit supplies only the smaller
multiplicity. This excludes the average of the individually realizable
return laws and continues to exclude every positive contrast of that
average.

The quantitative margin is valid against every preparation and decoder on
the orbit. A rank-deficient competing Fourier matrix has a unit kernel
vector, so its operator distance from the positive scalar identity is at
least that scalar. The normalized Fourier transform is bounded by the
uniform scalar-table error because the representation matrices are unitary.
No claim that this margin is sharp is made. Nonnormality implies index at
least three, so the binary reference `(1/d,1-1/d)` is an interior probability
vector and the local nonconvexity statement has no endpoint defect.

## 3. The arbitrary-controller symmetric-group law

The standard representation of S_n is faithful and irreducible over C on
the zero-sum subspace. The full-rank standard Fourier block therefore gives
both residual cardinality `n!` and observable dimension `1+(n-1)^2`.

For any subgroup K, its standard multiplicity is one less than its number
of natural point orbits. The factorial-product bound on subgroup index is
valid for all such subgroups; for three or more orbits it yields the stronger
`index >= n*r` when n is at least five. For two orbits, a singleton part
identifies a subgroup of a point stabilizer, and any proper subgroup doubles
that index; two nonsingleton parts cost at least `binom(n,2) >= 2n`.
The stronger inequality is explicitly restricted to positive standard
multiplicity. Transitive exceptional subgroups, including the exceptional
index-six phenomenon in S_6, have zero standard multiplicity and do not
invalidate this argument.

Consequently every permutation module carrying the response costs at least
`n(n-1)` points, and a core with fewer than `n^2` points can have only exactly
n-1 natural standard-carrying orbits. The lower is not restricted to a
preferred orbit type: the retained reversible normal-form theorem first
reduces arbitrary finite stochastic realizations to the positive-core
problem, and the subgroup estimate covers every G-set orbit in that problem.

The explicit low-contrast decoder is stochastic on its stated interval.
Its sum uses the identity that a permutation has exactly one preimage of n,
so it reproduces the fixed-point character for every group element.
At full contrast, value one at the identity forces each positive-weight
component's decoder to equal one on its preparation support. The group
average then excludes any active orbit of size less than n and forces every
active natural component to have a point preparation and point-indicator
decoder. Transposition evaluations require positive mass `1/n` at all n
natural points, which is impossible with only n-1 components. This proves
the full `n^2` lower without silently allowing only deterministic initial
preparations before the rigidity argument.

The strengthened exclusion of every intermediate core size is also valid.
Write the response as the contributions `B_N+B_E` of natural and extra
orbits. The natural contribution has only trivial and standard Fourier
support; the extras have no standard multiplicity. Subtraction from the
target shows that the aggregate extras have no other nontrivial Fourier
block either. Thus `B_E=v_E` is a constant vector with nonnegative coordinates
and total mass `w_E`. Positive contrast forces `w_N=1-w_E>0`. On the same
natural core the preparation `lambda_N/w_N` and decoder
`w_N D_N + 1 v_E` are stochastic and reproduce the exact original response.
This genuinely removes all extra orbits, rather than assuming they have zero
mass at positive contrast.

The attained lower-memory contrast set is a closed initial interval by the
retained compact-feasibility theorem. The explicit construction puts its
endpoint at least `1/(n-1)`, full-contrast rigidity puts it below one, and the
absence of intermediate sizes gives the two-level law including its endpoint.
The rational finite table makes the endpoint an effectively computable real
algebraic number through the retained finite decision procedure. This is not
a claim that the procedure was executed or that a closed formula is known.
Finally `n^2+1<n!` for n at least five justifies using the `1+kappa` branch of
the retained pure-start formula throughout the positive-contrast family.

The two-generator prepared quantum model is consistent with row-transition
and chronological composition conventions. Both the mixed and maximally
entangled preparations give the stated return probability for the diagonal
binary effect. No minimal quantum-dimension or common-resource quantum
advantage claim follows from that realization alone.

## 4. Stationary initialization, with all terminal quantifiers

The elimination uses equality of complete future-response functions, not
hidden-chain stationarity. The full-support averaged command law is needed:
if its initial self-transition is one, every command must fix that label,
which gives precisely the one-label exception. Otherwise the initial future
response is a convex combination of the other labels' future responses.
Redirecting all transitions into the initial label according to those
coefficients preserves every remaining recursion and every decoder.

The empty-word terminal-readout identity is essential and is included in the
statement. It ensures that deleting the initial label also preserves a
terminal experiment performed before any physical call. The upper's extra
initializer performs the first actual report transition `mu T_{a,y}` and
uses `mu d` for a zero-call terminal readout; no free persistent random coin
or uncounted call is inserted.

The inequalities apply to reducible realizations and to realizations whose
hidden states are not a basis of the minimal linear model. They prove the
exact +1 law whenever the response is not one-label, including the infinite
convention. For one-command stationary processes, a usual hidden stationary
initial distribution can also be obtained without new labels by Cesaro
averaging under the unobserved transition matrix: every averaged initial row
has the same future response, and a stationary cluster point preserves it.
This supports the ordinary stationary-HMM interpretation of the corollary.

Equality of all word/readout laws extends to common adaptive policies by
multiplying by the same policy kernels, summing finite stopped histories,
and taking decreasing continuation events. Nonnegative record-measurable
cost expectations then agree even when infinite. The statement keeps an
external policy's own persistent memory separate.

## 5. Complete noisy instruments and boundary rigidity

The CP margin follows from the stated Choi norms and leaves a positive
`I/16` lower for the third branch. All report probabilities stay within their
specified positive intervals. Summing the three maps gives exact
preparation at `I/2`; fixed-command stationarity and one-dependence follow.
This does not imply that an adaptive feedback-controlled output process is
stationary. Report 1 remains a pure reset, so this positive realization is
not obtained by falsely applying the stronger every-posterior interior
hypothesis inherited from R68.

The three cylinder modes are nonzero and distinct for positive retention
and nonreal phase. Their Vandermonde minor proves rank three. At zero
retention the two-by-two cylinder determinant is `2^-19`, and the explicit
two-state tables reproduce the diagonal subnormalized states. The initial
weights and all row sums in that construction are consistent.

For arbitrary HMMs, every productive entry of the zero-report matrix is
bounded through fixed positive entrance and exit paths by a constant times
`8^-n`. This gives spectral radius at most `1/8` without assuming global
irreducibility. Cayley--Hamilton forces the nonreal cylinder mode to occur
in an irreducible diagonal block. Perron normalization is performed only on
that block. Its stationary row annihilates the nonreal eigenvector, so the
rank-one stochastic mixture contracts its eigenvalue to the desired
`alpha exp(i theta)` while retaining at most M labels. This is a valid
necessary stochastic spectral condition for all nonnegative controller
tables, not only physical-state dictionaries.

The common regular polygon is invariant under branch zero when its complex
multiplier belongs to the polygon, under branch one by reset to a vertex,
and under branch two because its normalized Bloch norm is at most `5/11`,
strictly less than every relevant polygon inradius. Multiplying barycentric
coefficients by branch probabilities gives common nonnegative transition
matrices whose sum is stochastic. The exact state identity proves all
terminal POVMs and common adaptive-command laws. Piecewise continuous
barycentric selection supplies the claimed Borel dependence on a real angle.

At a first-sector boundary, a smaller carrying block is excluded by the
strict sector inequality and the rank-three lower. The carrying block must
therefore use all M labels. Applying the sector inequality before radial
contraction forces its Perron root to equal `1/8`, and equality fixes the
normalized zero-report matrix to the lazy directed cycle. The manuscript
correctly states diagonal similarity and makes no analogous assertion for
the other report matrices.

The all-angle dictionary count includes equality at a polygon inradius.
For a count above three, the single angle `pi/(K-1)` excludes every smaller
size; for three, any nonreal phase gives the rank lower. Thus a single
common dictionary attains the worst-phase lower. The finite-alphabet and
full-angle quantifiers are distinguished, and the general stationary
initialization law supplies the exact additional pure-start label. The
arithmetic lift uses only the necessary spectral condition and the actual
polygon upper, so it does not assume sufficiency of the entire stochastic
spectral region for a full instrument.

## 6. Target-cost uniform stopped approximation

The one-step trace-distance bound is valid for every positive qubit input:
the depolarized state differs from a unitary image by trace norm at most its
trace. The two opposite branch perturbations give exactly the stated
`epsilon/8` coefficient after the one-half trace-distance factor. The
exclusion of an additional entangled quantum register is material to this
constant and is explicit.

The finite-horizon telescoping orientation is correct. In the summand for
call t+1 the prefix is entirely the target process and only the remaining
tail is approximate, so the input mass is exactly the target survival
probability. Trace-norm contraction of the common positive trace-preserving
tail gives the target expectation of `min(tau,H)`, rather than an unbounded
or unspecified hybrid cost.

For the infinite-horizon limit, retain every stopped block through H and
collapse all unfinished mass to a scalar symbol. The sum of finite stopped
block norms increases to its full sum; the unfinished masses separately
converge to the two nontermination probabilities, and their absolute
difference therefore converges. This proves the stated complete stopped
classical-quantum distance, with a scalar nontermination block. The target's
finite expected cost gives zero target nontermination mass; approximate
nontermination may remain, but is bounded by the same total-variation error.
The text correctly refuses to deduce an approximate expected-cost bound
from total variation of bounded-score records.

The dictionary is chosen once for the whole policy class. Exact realization
of the damped subnormalized states introduces no further approximation.
The inverse-square-root label upper, the zero-retention endpoint and the
zero-cost exception follow with their stated constants. Composing an
L-label policy with the mixed K-label core and one initializer accounts for
the first actual physical call and all persistent policy labels.

## Remaining limits of this challenge

The numerical value or a closed formula for the symmetric-group threshold
is not established. The general full-instrument memory away from the stated
sectors remains bounded rather than exactly classified; the stopped-law
approximation is an upper bound without a matching optimal exponent. The
results do not solve the general-M squared-sign risk frontier, arbitrary
nonrigid robust control, independent A1/A2 dependencies or the broader Theta
pipeline. Prior classical representation, positive-realization and spectral
results require their existing primary-source credit. None of these limits
is converted into a proof failure of the scoped statements above, and no
journal-level endorsement is inferred from this author-team challenge.
