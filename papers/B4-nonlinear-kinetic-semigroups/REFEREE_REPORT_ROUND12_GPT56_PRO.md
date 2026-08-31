# Independent Referee Report — Round 12

**Manuscript:** B4 — *Nonlinear Kinetic Semigroups*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `2785cc407ea5709b66c70bc16c935154b6f7fc4bc797ca819c93dd1bd9e3a9f3`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 correctly distinguishes microscopic states, Koopman observables, push-forward laws, ensemble endpoint values, and the limiting action semigroup. It also charges preparation only at the initial boundary and abandons the previous divergent doubled-jet comparison.

The replacement “primal verification comparison” is not a valid comparison proof for the displayed value semigroup. The subsolution inequality written in the manuscript does not imply that the subsolution lies below

\[
S_{s,t}\Phi(f)=\sup\{\Phi(\rho_t)-I_{s,t}^{\rm dyn}\}.
\]

At terminal time it gives an upper bound by \(\Phi+I\), not by \(\Phi-I\), and taking an infimum or supremum cannot repair the sign. The claimed sandwich \(u\le S\Phi\le v\) therefore does not follow. The graph-core and hierarchy-corrector theorems also remain largely assumed and depend on the invalid B1–B3 chain.

## Decisive objections

### 1. The displayed subsolution inequality is unrelated to the value semigroup

The action semigroup is

\[
(S_{s,t}\Phi)(f)
=
\sup_{(\rho,\Gamma):\rho_s=f}
\{\Phi(\rho_t)-I_{s,t}^{\rm dyn}(\rho,\Gamma)\}.
\]

The proof claims that a subsolution satisfies, along every regular control,

\[
u(s,\rho_s)
\le
u(t,\rho_t)+I_{s,t}^{\rm dyn}(\rho,\Gamma).
\]

At \(t=T\), with terminal condition \(u(T,\cdot)\le\Phi\), this gives

\[
u(s,f)
\le
\Phi(\rho_T)+I_{s,T}^{\rm dyn}(\rho,\Gamma)
\]

for every path. The right-hand side has a **plus** cost. It does not imply

\[
u(s,f)\le
\sup_{\rho}\{\Phi(\rho_T)-I_{s,T}^{\rm dyn}(\rho,\Gamma)\}.
\]

Taking the infimum of \(\Phi+I\) is a different control problem; taking the supremum only weakens the wrong inequality. The claimed conclusion \(u\le S\Phi\) is absent.

### 2. The HJ sign and verification orientation are inconsistent

For

\[
U(s,f)=S_{s,T}\Phi(f)
\]

with Hamiltonian

\[
H(f,p)=\sup_b\{\langle p,b\rangle-L(f,b)\},
\]

the backward equation is

\[
\partial_sU+H(f,DU)=0.
\]

Along a control,

\[
\frac d{dt}U(t,\rho_t)
=-H+\langle DU,b\rangle
\le L,
\]

which yields

\[
U(s,\rho_s)
\ge U(t,\rho_t)-I_{s,t}^{\rm dyn}.
\]

This is the dynamic-programming lower support inequality for the supremum value. The manuscript writes the opposite type of estimate for its “subsolution” and never states a convention that reconciles it with the displayed PDE.

A valid comparison theorem must fix one sign convention and prove the correct domination and recovery inequalities.

### 3. The supersolution half does not repair the missing subsolution half

The manuscript derives

\[
v(s,f)
\ge
\sup_{\rho_s=f}
\{v(t,\rho_t)-I_{s,t}^{\rm dyn}\},
\]

which can give \(v\ge S\Phi\) after iteration. Even granting this, the first half gives no \(u\le S\Phi\). Thus the final sandwich is a non sequitur.

### 4. “Primal verification” cannot replace comparison for arbitrary viscosity tests without a chain rule theorem

The proof applies Fenchel's inequality along weak balanced paths to a viscosity subsolution. A viscosity subsolution is not differentiable along an arbitrary control path. To obtain a pathwise verification inequality one needs a regularization/doubling argument, a metric viscosity framework with an upper-gradient chain rule, or a nonlinear semigroup domination theorem.

Partitioning time and citing smooth cylinder tests does not establish such a chain rule for a merely upper semicontinuous subsolution on the kinetic state space.

### 5. The graph-core proof is incomplete at singular configurations

The paper says smooth finite-coordinate functions are dense in the weighted uniformly continuous observable space after unfolding regular collision faces, while grazing and multiple-collision sets are “bypassed in the base norm.” Base-norm density is not enough to identify a core for the closed Koopman generator if those sets have nonzero graph capacity.

Although the resolvent argument correctly shows that \(R_\lambda\mathscr D_0\) is a core once \(\mathscr D_0\) is dense in the underlying space, the claimed density on the actual graph-completed hard-sphere phase space has not been proved.

### 6. The hierarchy corrector assumes the main deterministic expansion

Theorem 3.1 postulates a connected order-\(j\) bound

\[
j!C^jT^{j-1}
\]

and a closed full BBGKY/ledger generator, then concludes normal summability and cancellation of every correlation defect. These are not consequences of the sequence weight alone. One must construct the defects, show the triangular equation preserves the graph domain, and prove the generator-image estimates uniformly in \(\varepsilon\).

The proof delegates all substantive work to B2, whose block sewing and marked LDP remain open.

### 7. Action compactness is imported rather than proved

Finite relative collision entropy controls the contact-flow density relative to \(A_f\), but compactness of density paths also requires velocity tightness, temporal equicontinuity, closure of the nonlinear balance, and endpoint compactness. The paper simply states that B2 supplies all of these. Round 12 B2 does not prove the required topology or a full good LDP.

### 8. The Gaussian risk-sensitive limit is unsupported

The final quadratic semigroup uses B3's purported joint density/contact Gaussian process. B3's displayed covariance omits pure contact tests. A “uniform complex moment neighborhood” is also not proved for the centered process on the infinite-dimensional state. Hence the exponential-transform limit does not follow.

## Genuine improvements recognized

The following changes should be retained:

- exact typing of Koopman, law, and endpoint-value objects;
- initial preparation charged once;
- use of the observable resolvent rather than a state resolvent;
- an action-based limiting semigroup; and
- abandonment of an uncontrolled exponential doubled jet.

## Required reconstruction

The authors should first prove the B2 good dynamic LDP and define the action state topology. They should then formulate the HJ equation with a consistent time/sign convention and prove that viscosity sub- and supersolutions satisfy the correct value domination inequalities, using an established metric-viscosity chain rule or a valid comparison argument. The microscopic corrector theorem must be proved independently on the observable graph domain.

## Recommendation

**Reject.** The new comparison proof does not imply its central inequality and is inconsistent with the displayed backward value problem. Without comparison, the limiting semigroup is not uniquely identified; without B2/B3, the microscopic and Gaussian convergence claims are also unavailable.