# Independent Referee Report — Round 15

**Manuscript:** B4 — *Nonlinear Kinetic Semigroups*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Recoverable registered Round-Fifteen candidate:** near-complete `B4_LAW_BOUNDARY_NISIO_RANGE.tex` from the truncated checksum-pinned payload  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence boundary

The paper folder still loads Round Fourteen. A nearly complete Round-Fifteen B4 candidate was recoverable; only the closing citation list is truncated. I reviewed its substantive theorems as supplemental candidate material. It was not materialized, built, or certified in the submitted branch.

## Executive assessment

The candidate fixes two prior typing errors: the exponential collision term is attributed to the ensemble boundary jump rather than the interior Koopman derivation, and the discounted value includes the initial condition \(f(0)=f_0\). Its central comparison/range theorem remains unsupported. The proof assumes that one can concatenate the same nearly optimal balanced control from two nearby density states, although admissibility and the reference intensity \(A_f\) depend nonlinearly on the state.

Existence of a variational value and sup-norm contraction does not by itself establish \(m\)-dissipativity, full range, viscosity comparison, or generator convergence.

## Decisive objections

### 1. “Common nearly optimal control” is not admissible from two different states

The comparison proof proposes to start from nearby \(f\) and \(g\), concatenate a common nearly optimal balanced control, and let their distance vanish.

A control here is not an external drift independent of state. Feasibility requires

\[
\partial_tf+v\cdot\nabla_xf=\Delta^*\Gamma,
\]

and the running cost uses

\[
A_f=\tfrac12ff_*B.
\]

A contact flow \(\Gamma\) admissible from \(f\) generally is not admissible from \(g\), and even if both paths exist, the entropy densities relative to \(A_f\) and \(A_g\) differ.

The paper supplies no controllability, coupling, or stability theorem that transports a balanced path/control between nearby initial states with vanishing cost error. The step that is supposed to yield

\[
\lambda\sup(u-v)\le0
\]

therefore has no mathematical basis.

### 2. Resolvent existence does not prove full range or \(m\)-dissipativity

The graph is defined retrospectively by

\[
\mathscr H=\{(u,\lambda(u-h)):u=R_\lambda h\}.
\]

To conclude that this graph is independent of \(\lambda\), dissipative, closed, and has the nonlinear resolvent identity requires proof. The variational formula gives a contraction in \(h\), but it does not automatically establish the Crandall–Liggett resolvent identity or consistency for different \(\lambda\).

The text declares these properties “exactly” the range and dissipativity conditions, which is circular.

### 3. Compactness of the infinite-horizon action is not established

The proof cites contact-mass control, time oscillations, energy conservation, and an exponential initial moment. The state space \(\mathcal E\), its metric, the class of initial data, and the topology in which action sublevels are compact are not defined. A lower-semicontinuous energy alone does not yield compactness in velocity, and transition action contains no initial exponential-moment penalty.

### 4. The corrector theorem gives only an iterated limit

The candidate states

\[
F_{\varepsilon,K}\to F,
\qquad
\mathscr H_\varepsilon F_{\varepsilon,K}\to\mathbb H F
\]

first as \(arepsilon\to0\), then \(K\to\infty\). Nonlinear semigroup convergence requires a single recovery sequence \(K=K(\varepsilon)\) with uniform graph bounds and compact-containment compatibility. No diagonal rate or equicoercive estimate is supplied.

### 5. The law–hierarchy intertwiner is asserted on too large a class

Factorial moment hierarchies do not uniquely determine arbitrary probability laws without moment determinacy and uniform exponential bounds. The exact intertwining is clear for finite polynomial cylinders, but the proof later treats it as an isomorphism on the complete law space and passes exponential observables through the infinite hierarchy. The needed convergence, determinacy, and domain statements are absent.

### 6. The ensemble boundary identity does not by itself close the nonlinear generator

A single-contact Taylor expansion gives the formal factor \(e^{\Delta p}-1\), but the limiting Hamiltonian requires convergence of the exponentially tilted boundary flux under the full ensemble law, including recollisions and source-dependent correlations. This is exactly B2's unproved marked cluster theorem. The local boundary identity is not a replacement for it.

### 7. The Gaussian exponential limit is inherited, not proved

Uniform \(L^{1+\delta}\) bounds for likelihood ratios do not follow merely from normal convergence of a pressure on a complex ball unless centered finite-volume normalizers and source radii are controlled uniformly. The argument also inherits B3's misnormalized Gaussian driver and unresolved process tightness.

## Required reconstruction

Prove a state-dependent control stability theorem or formulate comparison directly from an established nonlinear semigroup/resolvent identity. Define the state space and action compactness precisely. Establish the nonlinear resolvent equation and \(\lambda\)-consistency before invoking \(m\)-dissipativity, and produce one diagonal perturbed-test sequence.

## Recommendation

**Reject.** The candidate corrects the source of the exponential Hamiltonian but does not prove comparison or full resolvent range; these are exactly the steps needed to identify the limiting semigroup.
