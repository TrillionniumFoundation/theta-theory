# Author-team AI challenge: exact optimal memory for reset experiments

## Status and object

This note records a separately assigned mathematical challenge within the
author's AI-assisted revision team. It is **not an independent human referee
report**, a proof-assistant certificate, a priority clearance, or an editorial
decision. The challenge read the proposed section `52-optimal-reset-memory.tex`
against the inherited reset model and its Bellman/residual proofs in
`sections/16-reset-control.tex` of the complete R76 source, commit
`891643799f2dfb2737ad5c147bf8def2d460630b`.

The section's three new results are the exact pure-start memory formula with
tied actions, the strictly positive finite memory-gap certificate, and the
physical realization of arbitrary finite optimal-action covering problems.
The development-file hashes and actually executed diagnostics are recorded in
`RESET_DIAGNOSTICS_RECEIPT.json`. A subsequent source-bound build must identify
the committed files it actually executes; this development receipt is not such
a build and is not a hosted-CI result.

The mathematical challenge found a necessary scope boundary: replacing the
exposure hypothesis by arbitrary positive-semidefinite failure effects makes
the proposed all-report formula false. The explicit counterexample below was
sent to the lead author and incorporated into the new section. Within the
stated strict-positivity, positive-cost, finite-reset, pure-start model, the
cover and gap arguments survive the challenges described here.

## 1. Dependency and quantifier checks

The inherited model has finitely many commands and observed failure reports,
with a failure map

\[
  \mathcal I_{a,i}(\rho)=\operatorname{tr}(E_{a,i}\rho)\sigma_i.
\]

The state after report `i` is the fixed physical state `sigma_i`, independent of
the earlier hidden state and private coins. Success compels immediate stopping;
failure forbids stopping. Each label has one fixed command distribution. The
initial label is prescribed and pure, and there is no additional persistent
coin, clock, or uncharged state. Call costs have conditional mean
`tr(G_a rho)` with a strictly positive uniform lower bound. These conditions
are part of the theorem, not conventions that can silently be removed.

The no-closed-failure-set hypothesis supplies a finite Bellman vector `v` and
the all-initial-state spectral minimax value `V_*`. The new section uses that
proved result rather than assuming the existence of a solution to a new
optimization problem. Nonnegative Bellman residuals are

\[
 d_{ia}=c_{ia}+\sum_jQ_{iaj}v_j-v_i,\qquad
 A_i^*=\{a:d_{ia}=0\}.
\]

Every optimal-action set is nonempty. Ties and arbitrary numbers of commands
and reset states are admitted; uniqueness of local decisions is not required.

The strong hypothesis `E_ai > 0` exposes every report on the very first call
under any nonzero density matrix, including a singular least-favorable
preparation. The proof actually needs only positive first-failure exposure
under one fixed optimal dual preparation for every initial row under
consideration. Thus positive definiteness is a convenient sufficient condition,
not a claimed necessary condition on every individual instrument. The
counterexample in Section 4 shows why all exposure assumptions cannot simply
be omitted.

## 2. Challenge of the exact cover formula

Let `P_*` denote the optimal initial command distributions and let
`I(p)={i:supp(p) subset A_i^*}`. For a subset of reports `J`, let `t(J)` be the
minimum number of commands intersecting every `A_i^*` for `i` in `J`.
The claimed formula is

\[
 m_*=1+\min_{p\in P_*}t([s]\setminus I(p)).
\]

The lower argument has two essential steps. First, every robust optimal
controller has its initial row in `P_*`, since its cost matrix dominates the
Bellman start matrix and the latter has worst-state value at least `V_*`.
Second, evaluation at a fixed optimal dual preparation leaves no nonnegative
Bellman slack. Strict first-failure exposure therefore forces any label used
after report `i` to have its support contained in `A_i^*`.

This remains true with randomized updates depending on the previous label and
command: at least one label is reached with positive conditional probability,
and any reached label has zero residual. A noninitial mixed row that serves
several reports has support in their entire intersection. Selecting any one
action from that support covers all those reports simultaneously. Thus mixed
continuing rows cannot improve the cover count. Duplicate selected actions
only reduce the number needed. No inference about reachability from a
different response law is used.

The initial row must be treated separately. It can serve every report in
`I(p)` without an additional label. Counting `1+t([s])` unconditionally would
be wrong; the exact example in Section 5 exercises this case. Conversely,
using the initial row on `I(p)` and one pure row per command in a transversal
of the remaining reports makes every continuation Bellman-optimal. The
positive cost floor and the finite potential imply finite expected stopping
time by the same telescoping argument as in the inherited proof. There is no
hidden assumption that an arbitrary minimizing selector is already proper.

The finite algebraic procedure is a decidability claim: one may enumerate
proper deterministic selectors, solve their finite linear systems, retain
those satisfying the Bellman inequalities, and use real algebraic feasibility
for the optimal start face and support patterns. This does not establish a
polynomial-time algorithm or an efficient physical compiler.

## 3. Challenge of the one-step gap certificate

For `M` command rows, set

\[
 r_i=\min_{1\le k\le M}\sum_a p_a^k d_{ia},\qquad
 K_M=\sum_a p_a^1L_a+\sum_{a,i}p_a^1r_iE_{a,i}.
\]

Every finite-cost controller using these rows has cost operator at least
`K_M`: retain only its first post-failure nonnegative Bellman residual and
discard later residuals. Infinite expected cost cannot violate a finite
lower bound. Minimizing `lambda_max(K_M)-V_*` over the product of simplices
is legitimate because the displayed expression is continuous and the domain
is compact.

If that minimum vanishes, evaluation at the same least-favorable preparation
forces every `r_i` to vanish. This implication uses exposure; it is not a
consequence of `K_M` being merely positive-semidefinite. Zero residuals give
covering rows and the upper construction from Section 2, hence an actual
optimal controller. Conversely an optimal cover makes every `r_i` zero.
This establishes a strictly positive lower gap precisely when `M<m_*`.

The certificate is not generally the complete memory-constrained value
curve. Section 5 provides an exact strict example: `D_1=1/4` while the actual
one-label excess cost is `1/2`. Therefore this theorem does not close the
separate general-`M` squared-sign risk question or claim an exact risk
frontier for arbitrary experiments.

## 4. Exact boundary counterexample

On `C^2`, use one reset state `sigma=|0><0|` and commands `a,b` with

\[
 E_a=E_b=\tfrac12|0\rangle\langle0|,\qquad
 G_a=\operatorname{diag}(1,6),\quad G_b=\operatorname{diag}(2,5).
\]

The success probability from the reset state is `1/2`, so there is no closed
failure set. The Bellman value is `v=2`, with unique optimal reset action `a`.
The start matrices are

\[
 L_a=\operatorname{diag}(2,6),\qquad
 L_b=\operatorname{diag}(3,5).
\]

Writing `x` for the initial probability of `a`, the largest eigenvalue is
`5+x`; hence `V_*=5` and the unique optimal initial row is `b`. A blind
application of the all-report cover formula would predict two live labels.
But constant `b` has exact cost matrix `diag(4,5)` and is a one-label robust
optimum. Its reset continuation is locally nonoptimal but remains below the
worst-state value. The least-favorable preparation `|1><1|` succeeds
immediately and never exposes that slack.

All quantities are rational and the example is physically realizable with
diagonal cost/report effects. It is a counterexample to the unsupported
semidefinite extension, not to the theorem as stated.

## 5. Exact initializer reuse and a nonsharp gap

Use dimension three, two reset basis states, two commands, and
`E_ai=I/4` for every command and reset report. Let

\[
 G_a=\operatorname{diag}(1,3,6),\qquad
 G_b=\operatorname{diag}(3,2,7).
\]

The Bellman vector is `(5/2,7/2)`, the optimal reset sets are `{a}` and `{b}`,
and

\[
 L_a=\operatorname{diag}(5/2,9/2,15/2),\qquad
 L_b=\operatorname{diag}(9/2,7/2,17/2).
\]

The unique minimizing initial row is `a`, with `V_*=15/2`. It can also serve
the first reset state, so exactly two live labels suffice. The formula that
counts a separate initializer plus a cover of both reports would overcount.

For one fixed row with probability `x` of command `b`, exact solution of the
two-state continuation equations gives

\[
 (3+5x/2,\;5-x/2),\qquad
 V_1(x)=8+3x/2.
\]

The third initial coordinate dominates throughout `0<=x<=1`: its differences
from the first two are `5-x` and `3+2x`. Thus the exact one-label optimum is
`8`. The one-step matrix has largest eigenvalue `31/4+5x/4`, so `D_1=1/4`
while the true one-label gap is `1/2`. The script checks these polynomial
identities, affine endpoint bounds and monotonicities exactly. Its additional
17 rational evaluations only guard implementation consistency; they are not
used to infer a continuum extremum.

## 6. A noncommuting quantum instance

The classification is not restricted to simultaneous diagonalization. On
`C^2`, take reset states `|0><0|`, `|1><1|` and command-independent effects

\[
 E_1=\begin{pmatrix}1/4&1/8\\1/8&1/4\end{pmatrix},\qquad
 E_2=\begin{pmatrix}1/4&-1/8\\-1/8&1/4\end{pmatrix},
\]

with `G_a=diag(1,3)` and `G_b=diag(3,2)`. The effects have eigenvalues
`1/8,3/8`, sum to `I/2`, and fail to commute with the cost operators. The
Bellman vector is again `(5/2,7/2)`, and

\[
 L_a=\begin{pmatrix}5/2&-1/8\\-1/8&9/2\end{pmatrix},\qquad
 L_b=\begin{pmatrix}9/2&-1/8\\-1/8&7/2\end{pmatrix}.
\]

An optimal initial probability of `a` and a dual density are

\[
 p=\frac13+\frac{\sqrt2}{48},\qquad
 \rho_*=
 \begin{pmatrix}1/3&-\sqrt2/3\\-\sqrt2/3&2/3\end{pmatrix},
 \qquad V_*=\frac{23}{6}+\frac{\sqrt2}{12}.
\]

The script verifies exact trace one, rank one and positivity of `rho_*`, the
top-eigenvalue equation, and equality of its pairings with both start
operators. Both pure initial rows have strictly larger spectral cost, so all
optimal initial rows are mixed. Since the two reset optima are distinct
singletons, three labels are required and attained.

The mean costs and report effects can be realized jointly. Give each failure
outcome cost one. Split success into two unobserved outcomes with effects
`|j><j|/2`, costing `2(G_a)_{jj}-1` for command `a` and similarly for `b`.
These refined effects sum to the identity; their cost-weighted sum is exactly
the specified cost matrix. Both hidden costs are at least one. All failure
maps prepare the specified reset state, and the controller observes only the
declared report or terminal success. Thus no incompatible hypothetical
measurement is being used to define the example.

## 7. Universality and finite exact diagnostics

For nonempty proper action sets `A_1,...,A_s` on `q>=2` commands, the proposed
universal realization has dimension `s+q`, effects `(r/s)I`, and cost
diagonals

\[
 G_a(e_i,e_i)=1+\mathbf1_{a\notin A_i},\qquad
 G_a(f_j,f_j)=3+\mathbf1_{a=j}.
\]

The actual reset instrument is completely positive and trace preserving
after adding success effect `(1-r)I`. A hidden basis measurement followed by
the declared success/failure coin realizes the cost means without an extra
observation. The relevant cost and effect operators commute; **the reset
superoperators need not commute with each other**. This wording correction
was sent to the lead author.

The Bellman vector is constant `1/(1-r)` and the optimal action sets are
exactly the prescribed sets. The extra `f_j` coordinates make the worst-state
start cost `3+r/(1-r)+max_j p_j`; its unique minimizing row is uniform.
Its support is contained in none of the proper sets, which gives
`m_*=1+t`. The rational maps and cost matrices have polynomial encoding size
in the set-system incidence table for fixed rational `r`. Adjoining an unused
action reduces unrestricted nonempty transversal instances to proper sets
without changing their optimum. The NP-hardness claim is this explicit
classical covering reduction; it is not borrowed from a different partially
observed control model.

`diagnostics_r77_reset.py` exhaustively enumerates all **513** simple
hypergraphs with `q=2,3,4` and one to three distinct nonempty proper edges.
Repeated edges do not change the cover invariant; the diagnostics do not
claim to enumerate arbitrary larger hypergraphs. For each graph they check
three rational failure rates, `1/3`, `1/2`, and `3/4`, giving **1,539** physical
instances. The checks independently solve the rational continuation cost
system by Gaussian elimination, recover the Bellman-optimal action sets,
construct and test the entire initial expected-cost operator, and verify
that the selected continuing labels are reached.

At one label below the claimed optimum, the script enumerates **5,137**
families of possible mixed-row supports. Zero Bellman residual depends only
on support, so choosing the uniform distribution on each support exhausts
the relevant zero-residual incidence patterns. It checks a strictly positive
rational one-step operator gap for every such family. This is not a numerical
minimization over all probability weights and is not presented as a uniform
quantitative lower bound obtained by finite sampling.

The completed ordinary and optimized runs each checked **21,163** explicit
exact conditions, using rational arithmetic and symbolic algebra, with
**zero floating-point checks**. Their output bytes agree. Every test uses an
explicit exception-producing condition; disabling Python `assert` statements
does not disable the tests. The initial attempt with the default Python
interpreter failed before execution because SymPy was absent. The successful
runs used the already available Python environment recorded in the receipt;
no dependency was installed for this check.

## 8. What remains outside this check

The written arguments establish the arbitrary-size conclusions; the finite
diagnostics are consistency tests and exact counterexample checks. This note
does not re-prove every inherited theorem or assess the complete manuscript's
priority and significance. It supplies no human endorsement.

The reset theorem does not classify non-reset quantum instruments, arbitrary
temporal experiments, unexposed semidefinite boundary cases, or every
memory-constrained risk frontier. The pure-start convention matters. Timing,
program-description complexity, efficient synthesis, and the independent
A1/A2 and broader Theta objectives retain their separate status. The new
result provides an exact optimal-memory invariant for the stated tied-action
reset class, including realizability, a scope counterexample and a strict
finite-resource separation; those are the claims this challenge examined.
