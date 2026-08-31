# Independent Referee Report — Round 13

**Manuscript:** A4 — *History, Memory, and Universal Pressure*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `d9ea57315817a859c485ba07590f60f5bb7a2fbe254cfcdc140715ac3cbe9bea`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 13 correctly abandons impossible total-variation minorization on complete pasts, uses the correct Poisson martingale, and normalizes the nonlinear semigroup by a genuine Doob eigenfunction. It also distinguishes instantaneous distributional memory from an ordinary kernel. These are real improvements.

Two central claims remain false or ill-typed. First, a complex neighborhood of zero in the stated weighted Lipschitz space contains unbounded potentials for which `P(e^V)` is not finite, so the Feynman–Kac operator is not defined. Restricting to ordinarily bounded potentials removes the claimed open Banach neighborhood. Second, the memory theorem treats every pole of the compressed resolvent as a descriptor pole of the memory kernel. This is algebraically wrong: poles of `C(z)` become zeros of `C(z)^{-1}` and can cancel completely. A one-dimensional example gives identically zero memory despite a resolvent pole.

## Decisive objections

### 1. The Feynman–Kac eigenchart is not defined on a neighborhood in `Lip_W`

The weight is

\[
 W(H)=1+\sum_{j\ge0}e^{-\beta j}e^{\eta r(A_{-j})}.
\]

In the usual weighted Lipschitz norm, a neighborhood of zero contains functions satisfying `|V(H)| <= epsilon W(H)`. In particular it contains positive functions comparable to `epsilon W`. Then

\[
 e^{V(H)}\gtrsim
 \exp\{\epsilon e^{\eta r(A_0)}\}.
\]

The renewal kernel is assumed to have only an exponential moment in `r`. It need not, and generally does not, have the double-exponential moment required to make

\[
 P_V1=P(e^V)
\]

finite.

The manuscript tries to avoid this by calling `V` “bounded weighted Lipschitz.” If “bounded” means bounded in ordinary supremum norm, the bounded functions do not form an open neighborhood of zero in the stated weighted Banach space. If it means bounded only after division by `W`, the multiplier is not integrable. Either way the analytic Riesz neighborhood is not a well-defined Banach chart.

Every Doob eigenfunction, nonlinear tower, and source derivative depends on repairing this source space.

### 2. Poles of the compressed resolvent are not automatically memory descriptors

The manuscript lists every pole and every zero of

\[
 C_V(z)=R(z-L_V^D)^{-1}R
\]

and places their Laurent principal parts into `P_desc` for

\[
 \widehat K_V(z)=zR-RL_V^DR-C_V(z)^{-1}.
\]

At a pole of `C_V`, however, `C_V^{-1}` typically has a zero, not a pole. The pole may disappear completely from the memory kernel.

Take the one-dimensional example

\[
 L=-1,\qquad R=I.
\]

Then

\[
 C(z)={1\over z+1}
\]

has a pole at `z=-1`, but

\[
 \widehat K(z)=z+1-C(z)^{-1}=0.
\]

There is no `e^{-t}` descriptor mode and no nonzero memory at all. The proposed rule would nevertheless list the pole of `C` as a descriptor contribution.

Descriptors for the memory kernel must be extracted from the singularities of the Schur complement `zR-RLR-C^{-1}` after cancellation, not from the union of poles and zeros of `C` before cancellation.

### 3. The stated Wasserstein estimate does not by itself prove the claimed operator spectral gap

The coupling inequality contains the additive term

\[
 C\rho^n(W(H)+W(\widetilde H)).
\]

To obtain a spectral gap on a weighted Lipschitz Banach space one needs a complete weak-Harris/Doeblin–Fortet theorem: a Lyapunov drift, a `d`-small set, control of the weighted Lipschitz seminorm under one step, and compactness or quasi-compactness in the chosen weak topology.

The proof says that a “standard common-connector coupling” has geometric coupling time. For a countable Gibbs renewal kernel, a finite connector family and bounded distortion do not automatically give a uniform coupling probability from all states in a weighted sublevel. The required minorization/coupling constants and dependence on the current branch are not proved.

Kantorovich duality converts a proved Wasserstein contraction into test-function estimates; it does not manufacture the contraction or quasi-compactness.

### 4. The quenched rough theorem uses unproved A3 inputs

The physical-time result requires more than an LDP. It needs a conditional renewal law of large numbers, a functional time-change theorem, tight control of the residual flight at scale `sqrt(T)`, and joint convergence with the martingale area. A3 does not establish these CLT-level conditional estimates. Its proposed path LDP is itself incomplete.

Thus the assertion that A3 supplies time inversion and the terminal residual is an invalid dependency upgrade.

### 5. The renewal-resolvent vertical bounds are asserted rather than derived

A2 concerns returned transfer operators. Passing to the suspension resolvent requires precise entrance and exit operators, their graph domains, and uniform estimates after two vertical derivatives. Merely differentiating `E_z` and `X_z` does not automatically gain one power of `|y|`; boundary terms and the roof regularity determine that gain.

The proof gives no formulas showing that the derivatives are integrable, no treatment of nonreversibility (the entrance and exit operators need not be adjoints), and no determinant lower bound needed to control `C_V^{-1}` after compression.

### 6. “Unique normalized decomposition” is not established

Smith–McMillan factorization describes a finite-dimensional meromorphic matrix up to unimodular factors. Turning it into a causal descriptor realization requires a minimal state-space construction and a proof that the polynomial, resonant, and regular pieces are invariant under the chosen realization equivalence. Declaring monic companion form does not prove uniqueness of the operator-valued time-domain decomposition, especially when pole-zero cancellations occur as in objection 2.

## Genuine improvements recognized

The complete-past metric, correct martingale–coboundary formula, eigenfunction Doob normalization, causal Schur sign, and explicit instantaneous distributions should all be retained. They are the right corrections to earlier rounds.

## Dependency assessment

A4 depends on A2's valid integrable roof theorem and A3's valid stopped renewal theory. Both remain open. C2 and D1 therefore cannot use A4 as a certified source of filtration convergence, memory response, or rough likelihood limits.

## Required reconstruction

A viable version must:

1. choose a source Banach algebra on which `e^V` is actually a bounded/integrable multiplier;
2. prove a full weak-Harris spectral theorem for the complete-past kernel;
3. derive the suspension resolvent with explicit entrance/exit estimates; and
4. factor the memory Schur complement after all cancellations, rather than assigning descriptors to every resolvent pole.

## Recommendation

**Reject.** The revised probabilistic architecture is substantially better, but the Feynman–Kac chart is ill-typed and the central descriptor-memory theorem contains an elementary pole-cancellation error. The remaining model-specific estimates are not proved.
