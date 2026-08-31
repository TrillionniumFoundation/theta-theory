# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — Cotangent Rigidity and Tangent Representations Across Deterministic Platforms  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `23466f62af7609c7adc787add73d6096b73e33c0`

## Executive assessment

The revision correctly separates equality of invariant integrals from pressure equivalence modulo constants, uses the coarse rather than complete history filtration, and recognizes that source-dependent Doob memory must differentiate the eigenfunction, invariant pairing, and projection.

The announced cotangent quotient is still not a quotient by a linear subspace; the Følner averaging lemma lacks the uniform moment bound needed for compactness; and the proposed Hilbert-bundle connection uses Radon–Nikodym derivatives between equilibrium path measures which are generally mutually singular. The memory transform also repeats the wrong Volterra sign. Optional-projection convergence remains dependent on A4's invalid coarse-kernel theorem.

## Major mathematical objections

### 1. \(\mathscr N_{m int}\) is not defined as a linear subspace

The paper writes

\[
\mathscr N_{m int}=
\overline{\{U-U\circ\Theta_t:U\in\mathscr A_W,\ t\ge0\}}.
\]

The set inside the closure is not generally closed under addition when the two coboundaries use different times. Thus its closure need not be a vector subspace, and the quotient/coset language used throughout is not defined.

The intended object is presumably the closed linear span of constants or rational/all-time coboundaries. That must be stated explicitly, and the chosen topology must be compatible with time shifts. This is not a cosmetic notation issue: Hahn–Banach annihilators and quotient cotangents require a closed linear subspace.

### 2. The invariant-separator theorem needs more than Hahn–Banach

Even after replacing the set by its closed span, the equivalence

\[
\nu(F)=\nu(G)\ 	ext{for every invariant probability}
\quad\Longleftrightarrow\quad
F-G\in\overline{\operatorname{span}\{U-U\circ\Theta_t\}}
\]

is a nontrivial duality theorem on a noncompact weighted space. The proof assumes every separating signed Radon functional can be averaged to an invariant weighted Radon functional without loss of tightness or pairing. The stated moment hypothesis does not imply this.

### 3. The Følner averages need a uniform-in-time moment bound

The assumption is

\[
\sup_{0\le t\le T}
\int W\circ\Theta_t\,d|\mu|
\le C_T\int(1+W)\,d|\mu|,
\]

where \(C_T\) may grow with \(T\). Relative compactness of

\[
\mu_T=T^{-1}\int_0^T(\Theta_t)_\#\mu\,dt
\]

as \(T\to\infty\) requires a uniform bound on the averaged \(W\)-moments. The displayed estimate permits \(C_T=e^T\), in which case the averages need not be tight. Compact sublevels of \(W\) do not compensate for a diverging moment bound.

For conserved-energy hard-sphere observables a uniform bound may be available, but for general path weights and the Sinai shift it must be proved platform by platform. The lemma as stated is false.

### 4. Nearby equilibrium path measures are generally mutually singular

The Hilbert-bundle connection contains

\[
\partial_\eta\log
\frac{d\nu_\eta^D}{d\nu_0^D}.
\]

For distinct stationary ergodic Gibbs measures on an infinite path space, mutual absolute continuity is exceptional. Even Bernoulli product measures with parameters \(p
e q\) are mutually singular. Analytic dependence of transfer eigenvectors does not make the corresponding infinite-volume invariant measures equivalent.

Therefore the Radon–Nikodym derivative in the definition of the connection may not exist. The claimed unitary trivialization by density square roots is unavailable. One must work in a common transfer-operator Banach space, finite-time likelihood spaces, or a bundle defined abstractly without identifying \(L^2(
u_\eta)\) through nonexistent densities.

### 5. The memory transform again has the wrong sign

For the compressed semigroup correlation \(C_\eta(z)\), the Volterra identity gives

\[
\widehat K_\eta(z)=zP_\eta-A_\eta-C_\eta(z)^{-1}
\]

on the resolved range. The paper writes

\[
\widehat K_\eta(z)=C_\eta(z)^{-1}-zP_\eta-A_\eta.
\]

This is not the memory kernel associated with the displayed resolved equation. Covariantly differentiating the wrong transform does not produce a commutative pressure–memory diagram.

### 6. The projection connection is not determined by \(P_\eta^2=P_\eta\) and orthogonality alone

Differentiating those relations constrains the off-diagonal blocks of \(P_\eta'\), but the derivative also depends on how the resolved subspace itself is transported. “Multiplication with \(h_\eta\)” is not unitary in the varying invariant measure, and the mutual-singularity problem prevents the proposed canonical transport. Thus \(
abla_\eta P_\eta\) is not a constructed object.

### 7. Optional projections inherit the A4 failure

The exact martingale identity is valid for any filtration. Its convergence to a diffusion optional projection requires the A4 uniform coarse-history kernel theorem. Since the stable-leaf quotient retains the future itinerary and A4 has no valid nondegenerate conditional kernel, Theorem r7-c2-optional has no proved input.

### 8. The nonlinear contraction notation remains ill typed

For a nonlinear map \(\mathcal C\), there is no linear adjoint \(\mathcal C^*\). The pressure of the contracted observable is obtained by composing test functions with \(\mathcal C\), not by evaluating \(Q\) at a nonlinear “pullback source” without defining the source manifold and its derivatives. The displayed \(D(Q\circ\mathcal C^*)\) formulas therefore need a precise functional setup before they can be called a contraction theorem.

## Required reconstruction

Define the two null spaces as closed linear spans in a declared topology. Prove a platform-specific invariant-separator theorem with uniform weighted tightness. Replace the Radon–Nikodym Hilbert connection by a common transfer-space or finite-time construction that remains meaningful for mutually singular phases. Correct the Volterra sign and derive projection transport from an actual family of resolved subspaces.

## Recommendation

**Reject.** The paper contains useful typing corrections, but its cotangent quotient is not presently a vector quotient, its invariant averaging is unjustified, and its Doob Hilbert connection is generally undefined on infinite path space.
