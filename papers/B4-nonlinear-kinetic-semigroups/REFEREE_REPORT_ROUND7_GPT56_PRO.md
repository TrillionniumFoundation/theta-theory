# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — Nonlinear Kinetic Semigroups  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `3ab2723da53bf23a1870c0042f6914d2ad95c6e7`

## Executive assessment

The revision correctly distinguishes the complete augmented law from a one-particle density state, replaces the previous negative-time formal inverse by a terminal-value equation, adopts the weak topology with energy as a lower-semicontinuous containment function, and tries to keep doubled-variable cotangents inside a bounded exponential core.

Three direct defects remain. The analytic approximation uses a nonexistent “entire cutoff”; the proposed bounded-gradient penalty does not become coercive as its parameter tends to zero and therefore does not force the two doubled variables together; and the transition action includes the initial preparation cost, which destroys the claimed semigroup law by double counting at intermediate times. The full-BBGKY corrector is also not proved in the microscopic graph domain.

## Major mathematical objections

### 1. The “entire cutoff equal to one on a box” does not exist

The proof of Lemma r7-b4-approx asks for an entire cutoff which is identically one on the coordinate projection of a compact containment set and suppresses growth outside a slightly larger box. A nonconstant entire function on \(\mathbb C^d\), or a real-analytic function on a connected real domain, cannot equal one on a set with nonempty interior and then change elsewhere. The identity theorem makes it identically one.

Thus the proposed Bernstein polynomial approximation cannot simultaneously:

- belong to the analytic law algebra globally;
- agree exactly with the target on an open coordinate box;
- remain bounded outside that box; and
- have uniformly bounded first and second derivatives/collision increments.

Without such a construction, the extension from analytic polynomial cylinders to general \(C_b^3\) cylinders fails.

### 2. The Tataru penalty does not force the diagonal

The paper defines

\[
\Psi_\eta(f,g)=\eta^{-1}\omega(\eta d_B(f,g)),
\]

with \(\omega(r)=r\) near zero. Since \(d_B\) is bounded on the probability/energy state set, for every fixed pair and sufficiently small \(\eta\),

\[
\Psi_\eta(f,g)=d_B(f,g).
\]

The penalty therefore approaches a fixed bounded distance; it does not diverge off the diagonal and does not force maximizing pairs to satisfy \(f-g	o0\). This is exactly why its derivative coefficients remain bounded: the construction has removed the coercive scaling required by the doubling-of-variables argument.

The subsequent instruction “finally send \(\eta\) to zero” changes nothing. The Hamiltonian continuity lemma cannot be applied at two potentially separated states, so the comparison proof does not close.

### 3. The initial cost is incorrectly included in the transition action

The paper defines

\[
\mathcal I(f,\Gamma)=I_0(f_0)+
\int_0^T\ell(d\Gamma/dA_f)dA_f\,dt
\]

and then defines the transition value \(V_t\) by subtracting \(\mathcal I_{[0,t]}\). If this action is composed at an intermediate time \(s\), the second leg charges a new initial cost \(I_0(f_s)\). Hence

\[
V_{t+s}\ne V_tV_s
\]

in general; the right side double counts static preparation.

A Lax–Oleinik transition action must contain only the dynamic cost. The initial microcanonical/grand-canonical rate belongs in the boundary functional once, not in every semigroup segment. The manuscript previously recognized this distinction but reintroduces it here.

### 4. The forward corrector is not connected to the finite microscopic generator

The terminal-value identity

\[
\partial_tc_j+A(t)c_j=-D_j
\]

is algebraically correct for the limiting propagator \(A(t)\). The microscopic perturbed-test theorem, however, requires cancellation under the finite augmented BBGKY logarithmic generator \(\mathbb A_arepsilon\), including all \(arepsilon\)-dependent boundary domains. The proof does not show that the limiting propagator solves the finite graph-domain equation up to a controlled error at every label/ledger order.

The estimate \(\|D_j\|\le Cho^j\) with “\(ho<\mu_arepsilon\)” is not a normal-summability theorem for \(\mathbb A_arepsilon c_j\). It gives no uniform domain control, no boundary trace compatibility, and no estimate for interchanging the infinite corrector sum with the unbounded generator.

### 5. The analytic law algebra is only formally defined

The graph norm itself contains \(\|\mathbb A_arepsilon M_J\|\), while stability under products and exponentials is deduced from the claim that the generator raises degree by at most one. The hard-sphere boundary generator is unbounded and its product/Leibniz domain is not shown to be a Banach algebra. Defining weights using the desired graph images does not prove completeness, closability, or the derivation property.

### 6. Compactness and microscopic convergence remain dependent on B2

The action compactness lemma assumes the B2 good rate, closed balance, and contact entropy estimates. The microscopic convergence theorem then cites the same B2 lower recovery. Since B2-GC is not proved, these cannot serve as independent inputs. Nor can generator convergence plus the failed comparison theorem identify a unique limit.

## Required reconstruction

Separate static preparation from dynamic action. Construct a genuine graph core using smooth bounded functional calculus rather than an impossible entire cutoff. A comparison proof must use a coercive penalty and simultaneously control the resulting unbounded cotangents—this tradeoff cannot be removed by rescaling a linear \(\omega\). Finally, solve the corrector equation for the actual finite generator domains with explicit uniform estimates.

## Recommendation

**Reject.** The paper repairs the sign of the terminal corrector and the state topology, but its analytic approximation is impossible, its comparison penalty is noncoercive, and its action cannot satisfy the stated semigroup law.
