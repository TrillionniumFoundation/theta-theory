# Research status — General Theta Foundations I, R73

The paper remains **General Theta Foundations I: Acquired Geometry and Causal
Resource Transfer**. Its scientific problem is the relation between information
acquired in causal experiments and the resources required to realize its
optimal use. The research objective remains the standard of Annals of
Mathematics, Acta Mathematica, Inventiones Mathematicae and the Journal of the
American Mathematical Society. The response to the outstanding contribution
objection is the new mathematical chain below, with complete proofs and
explicit scope. This document does not supply an editorial assessment of
whether that objective has been reached.

## What has been established in the current manuscript

### 1. A structural theorem for arbitrary finite stochastic realizations

Let $b:A^*\to\Delta(C)$ be a finite-dimensional response whose minimal
observable shift dynamics is compactly reversible. The inherited R72 theorem
proves that an exact finite stochastic realization exists if and only if the
observable group is finite, equivalently the residual set is finite. The
present theorem starts with **any** such finite stochastic realization. It
constructs a faithful permutation core, preserving the whole response for
every command word, with at most one additional initialization label.

The proof does not assume that hidden rows lie in the minimal observable
space or that the original stochastic matrices already form a group. It
constructs an idempotent from observable identity-word loops, proves the
sandwiched identities needed to act on its recurrent simplex, and establishes
faithfulness through the observable quotient. If the resulting core starts
from a mixed distribution, the original pure initial label must have been
transient. That supplies the exact extra-label lower bound. A converse
construction applies the first command during the counted initialization
transition and then uses only permutations.

This theorem applies to every finite family of prepared unitary commands,
after removing exactly the directions invisible to all future terminal tests.
The full physical unitary group may be infinite while the observable group is
finite. The result concerns exact input-response simulation; it does not expose
the simulator's private state to an external controller.

### 2. An exact memory formula, sharp bounds and two distinct obstructions

Write $N$ for residual cardinality and $\kappa_G(b)$ for the least size of a
finite permutation action admitting a probability preparation and bounded
terminal probability decoder. The prescribed pure-start memory is exactly

$$
m(b)=\min\{N,\,1+\kappa_G(b)\}.
$$

Thus the optimization retains both the initialization charge and the positivity
of the decoder. An $M$-label realization has $|G|\le M!$; if $M<N$, then
$|G|\le(M-1)!$. These bounds are sharp. If $d=\dim V_b$, equality
$m(b)=d$ holds exactly when $N=d$, and every $d$-label realization then
has permutation transitions.

For every $k\ge3$, two commands generating the natural $S_k$ action give an
explicit family with rank $k$, residual count
$k!/(n_1!\cdots n_j!)$ for preparation multiplicities $n_i$, and memory
$\min\{N,k+1\}$. Pairwise distinct preparation weights give exactly $k+1$
stochastic labels versus $k!$ deterministic-transition labels. Pure,
repeated-weight, constant-preparation and constant-decoder cases are stated
separately. This factorial family has a diagonal quantum realization and is
already classical; the comparison is stochastic versus deterministic memory.

The permutation-module lower bound is not a substitute for positivity. The
manuscript gives two $S_3$ responses with the same natural module, rank three
and six residuals, whose stochastic minima are four and six. For the second,
$\beta(g)=1/2+uP_gu^{\mathsf T}/4$, $u=(1,-1,0)$, endpoint probabilities
exclude every probability factorization on five or fewer points. Its exact
six-label lower bound has a prepared-qubit realization. This is a concrete
obstruction invisible to the group, rank and module alone.

### 3. Exact synthesis on a declared algebraic input class

For a supplied finite real-algebraic linear representation, assuming
probability validity and compact reversibility on the minimal observable
quotient, a terminating procedure decides finite stochastic realizability and
returns a smallest realization when one exists. The unitary corollary proves
those promises from the supplied algebraic physical primitives.

Reachable/observable reduction, the classical finite-group order bound, finite
matrix-group recognition and real-algebraic feasibility are explicitly
credited. The normal form permits the minimum to be searched over finite
permutation actions with an exactly counted initializer and bounded multi-output
decoder. The negative answer has a finite list of distinct observable command
products beyond the stated finite-group bound. The positive answer has exact
controller tables and finite algebraic feasibility certificates.

This establishes decidability and exact minimal synthesis within the stated
class. It does not establish a new general polynomial-time matrix-group or
probabilistic-automaton algorithm, decide positivity of an arbitrary supplied
series, learn an unknown representation, or minimize program and sampling
resources simultaneously with labels.

### 4. Finite separation and a matching stable-memory theorem

For any supplied $d$-dimensional linear probability response and any proposed
$M$-label machine, agreement through word length $d+M-1$ implies agreement
on all words. This is the classical finite-equivalence argument. Compactness
of all stochastic tables and bounded decoder rows then gives an **attained
strictly positive finite-probe gap** precisely when no exact $M$-label
realization exists. Algebraic data make the gap and a rational strict lower
certificate effectively computable. The finite separation also persists under
an explicit perturbation bound on preparation, channels and terminal effects.

For a finite compactly reversible response, its minimal normal form supplies
a common stationary row. Mixing each command toward the associated
group-averaged background preserves an exact realization on the same labels.
The finite gap supplies the matching lower in a positive interval. This
background has a physical prepared-unitary realization as an invariant state;
it need not be the maximally mixed state. Arbitrary noise perturbations receive
the stated lower bound, not an unproved matching upper.

For the period-four response, an explicit three-state nonnegative polynomial
identity gives $\delta_3>1/36$. The same response under damping has exactly
four labels for $89/90\le\alpha\le1$. This is a certified sufficient
interval. The general algebraic periodic cutoff is effectively computable;
the exact first transition point is not claimed.

## Inherited conclusions remain active

The main article retains the original actual-history causal transfer theorem
and its proof. The current supplement retains the complete performed-law,
finite-resource synthesis, compact risk and attainment, variational/dual,
stopping, reset, rank-constrained discrimination, predictive quotient, spectral
and geometric results. R71's arbitrary-phase Diophantine envelope and R72's
controlled reversible criterion, periodic partition formula and leakage law
remain fully proved contributions with their own hypotheses.

The R66/R67 robust-tie and weighted-rigidity criteria on the declared rigid
herald class remain inherited closures. They are not reopened because the new
central theorem has advanced. The exact two-label formulas and special
qubit models remain exact model theorems; local spectral geometry remains
local; the original independent ordered-measurement and reset results retain
their general and special-case distinctions. `PRESERVATION_MAP.md` gives the
current bodies and immutable independent source locations.

The current catalog contains 171 inherited numbered statements and 14 added
statements. This includes supporting classical lemmas and specializations;
the count is an inventory, not a novelty claim. `THEOREM_INDEX.json` binds
the current numbers and pages to the native build.

## Questions that remain unresolved

| Scientific question | What this revision contributes | What remains open |
|---|---|---|
| General-$M$ squared-sign risk frontier $V_{p,\alpha,M}-V_{p,\alpha}$ | Exact memory structure, preserved low-memory results and finite response obstructions provide additional tools. | The sharp approximation-risk curve at arbitrary fixed memory is a different objective and is not computed here. It requires matching risk lower bounds and admissible minimizing controllers for that objective. |
| General multi-command boundary-optimal feedback | One common realization reproduces every supplied command word; prepared unitary families receive a general finite-realizability criterion. | Optimality when the controller itself chooses commands or faces a nonrigid boundary experiment requires its own physical and decision-theoretic proof. |
| Closed memory formulas for arbitrary finite groups and responses | The probability-factorization formula is necessary and sufficient, and algebraic input permits exact minimization. | A simple formula in representation data alone is ruled out by the bounded-decoder example. Further sharp formulas require control of the actual bounded positive factorization. |
| General damping transitions | A nonempty plateau is proved and algebraic sufficient cutoffs are computable; the period-four cutoff is explicit. | The exact first transition point, all later transitions and sharp risk behavior at fixed smaller memory remain model-dependent questions. |
| Timing and arithmetic precision | Existing timing statements and both arbitrary-phase logarithmic growth exponents are retained. | The intermediate phase-type timing frontier, sharp arithmetic leading constants and certain simultaneous favorable-scale questions are not settled. |
| Full computational resources | Exact algebraic controller tables can be synthesized in the declared class. | Matching program-size, arithmetic-time, precision, workspace and exact-sampling lower bounds are not consequences of an exact live-label count. |
| Unknown predictive models | The fixed-law predictive quotient and supplied finite observable reduction remain valid. | Reconstruction or certification of a generally unknown quotient from finitely many observations needs additional assumptions and a separate theorem. |
| A1, A2 and the larger Theta program | The General Theta results retain their own explicitly stated dependencies and scientific role. | Independent geometric/dynamical constructions, B4/C2 pipeline flags, process limits, nonlinear-generator and filtering/posterior assertions are not proved by a response-memory classification. |

These open questions remain research objectives. They do not change the paper's
identity or publication target, and they do not authorize extrapolating a
special model or a local theorem to completion of the larger program.

## Verification and assessment status

The current work contains full English author proofs, separately challenged
critical arguments, exact finite diagnostic scripts and inherited verification
programs. Reconstructed files receive fresh hashes and executions. The strict
source-bound build and publication receipts determine the actual final source,
compiled outputs, checks run and their outcomes; a prospective suite total or
an unsealed checkpoint is not a success record.

The new diagnostics test specified finite identities and realizations, including
an exact all-word comparison for a concrete pair of machines through finite
reachable-span closure. They do not replace the universal proofs. The claimed
general real-algebraic decision procedures are proved algorithms, not reported
completed general quantifier-elimination computations. No formal proof-assistant
verification, new human specialist report, journal acceptance or editorial
decision is supplied by this author revision. An independent referee can assess
the actual new theorem chain from the source-bound entry without accepting any
such additional claim.
