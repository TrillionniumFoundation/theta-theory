# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — *Nonlinear Kinetic Semigroups from Deterministic Hard-Sphere Hierarchies*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `0857ac443cedaf588ce02fa7f6fe5cc9efda8e48`

## Editorial summary

The change to the ordinary weak topology with energy as a lower-semicontinuous containment function correctly resolves the previous second-moment compactness objection. The paper also now distinguishes the exact full-law dynamics from the limiting one-particle kinetic semigroup.

The central full-BBGKY corrector is nevertheless algebraically wrong. The proposed finite-time integral is not an inverse of the hierarchy generator and leaves a nonzero terminal defect. The law-coordinate algebra does not contain the generic `C_b^3` cylinders to which the theorem is applied, and the comparison proof uses cotangents whose collision increments leave every bounded analytic core. Consequently neither the perturbed-test generator convergence nor uniqueness of the Hamilton–Jacobi limit is proved.

## Major mathematical objections

### 1. The proposed Duhamel corrector does not cancel the defect

Let `A` denote the complete BBGKY generator and `U(t)=e^{tA}` its formal group. The manuscript defines

\[
\mathfrak c=-\int_0^T U(-s)D\,ds
\]

and claims that applying the generator cancels `D`. Direct calculation gives

\[
A\mathfrak c
=-\int_0^T A U(-s)D\,ds
=U(-T)D-D.
\]

Therefore

\[
D+A\mathfrak c=U(-T)D,
\]

not zero. The uncancelled terminal defect is of the same order as `D`; it does not move automatically to the next label level and does not vanish with `epsilon`.

An actual inverse would require an integral to infinity with decay, a resolvent `(lambda-A)^{-1}`, or a time-dependent corrector solving a backward terminal-value equation whose boundary term is included in the perturbed test. None is present. This explicit identity invalidates `lem:r6-b4-correctors` and `thm:r6-b4-generator` before any issue of convergence arises.

### 2. Negative-time BBGKY evolution is not a bounded operator on the declared hierarchy spaces

The exact Liouville flow on full microstates is invertible, but the BBGKY hierarchy is an infinite triangular coordinate system with boundary traces and label weights. The paper uses `U_BBGKY(-s)` as a bounded inverse on the same connected norm without proving that backward evolution preserves the exponential label radius, Gaussian weight, or trace regularity.

Forward collision trees gain ordered-simplex factors; reversing them can require reconstruction of boundary data and can enlarge high-label correlations. The B2 estimate, even if accepted, is a forward Feynman–Kac bound. It gives no strongly continuous group and no graph-domain theorem for negative time. Thus the very operator in the corrector formula is undefined on the claimed Banach space.

### 3. The law-coordinate algebra does not contain the cylinders used later

`mathfrak A_{alpha,beta}` is defined as the completion of finite polynomials under an absolute coefficient norm. Such a completion contains functions represented by absolutely convergent power series in the hierarchy coordinates. It does not contain an arbitrary

\[
\varphi\in C_b^3
\]

of finitely many moments. A generic smooth bounded function is not analytic and has no absolutely summable polynomial expansion in that norm.

The manuscript nevertheless applies the connected exponential expansion and infinite corrector to every `C_b^3` density/contact cylinder. Density of polynomials on compact subsets is not enough: the generator, exponential map, and coefficient norm require global control, while the hierarchy coordinates are not uniformly bounded over the full law space.

The assertion that the algebra is “closed under exponentiation of bounded cylinders” is also circular unless the bounded cylinder already belongs to the algebra. A bounded nonanalytic cylinder does not enter merely because its scalar exponential has a Taylor series.

### 4. Path-contact observables are not coordinates of the instantaneous law state as defined

The exact state is a law `rho` on current microstates. The cylinder later includes `Gamma(rho)`, the actual-contact measure accumulated over a time interval. That is a path functional, not a function of the instantaneous law unless the state is augmented by the past contact ledger or the semigroup is formulated on path laws.

The paper alternates between current law states, full hierarchy coordinates, and density/contact path cylinders without defining one Markov state carrying all of them. This typing problem affects the algebra homomorphism, the logarithmic generator, and the terminal-value semigroup.

### 5. Normal summability of coefficients does not imply membership in the generator graph domain

Even if the coefficient bound

\[
\|c_j\|\le C\rho^j
\]

were valid, applying an unbounded generator term by term requires convergence of both the series and the series of generator images in the graph norm. The proof bounds only connected coefficients and then asserts that “the absolute graph norm permits” the interchange; no graph-norm estimate is displayed.

The factors `mu^{1-j}` do not solve this problem uniformly on hierarchy compact sets because the generator raises label number and carries `epsilon`-dependent collision-boundary factors. Nor is it shown that the nonlinear logarithmic generator of an exponential law functional is defined by the linear BBGKY generator on this infinite series.

### 6. The same corrected sequence cannot automatically give both relaxed inequalities

Perturbed-test convergence in an infinite-dimensional large-deviation/Hamilton–Jacobi theorem normally requires upper and lower recovery sequences compatible with semicontinuity and compact containment. The paper says that one exact corrector yields both because it cancels defects termwise. That cancellation is already false, and no control is given when the approximating law is not represented by smooth hierarchy densities.

In particular, the trace-hierarchy compact sets used for local uniformity are much stronger than the weak-energy state topology of the limiting equation. No theorem shows that every weakly convergent sequence relevant to the half-relaxed limits remains in a common trace compact set.

### 7. The Hamiltonian continuity lemma does not cover the doubled-variable cotangents

`lem:r6-b4-hamiltonian` assumes `p,q` lie in one bounded core set, so that `Delta p+psi` is uniformly bounded. In the comparison proof, the derivative of

\[
\frac1{2\eta}\sum_{j=1}^J2^{-j}
|\langle f-g,\phi_j\rangle|^2
\]

has coefficients of order

\[
\eta^{-1}\langle f-g,\phi_j\rangle.
\]

At a penalized maximum one generally obtains only `|<f-g,phi_j>|=O(sqrt eta)`, so these coefficients can grow like `eta^{-1/2}`. The collision increment of the test therefore leaves every fixed bounded core as `eta` tends to zero. Because the Hamiltonian contains

\[
e^{\Delta p},
\]

there is no uniform modulus of continuity to pass to the limit.

The fact that each finite penalty lies algebraically in `mathscr D_b` does not provide a uniform core bound. A valid comparison proof needs a penalization adapted to the exponential Hamiltonian, an a priori bound on the doubled cotangent, or a containment/Tataru-distance argument. The stated order of limits does not address this blow-up.

### 8. Weak compactness alone does not prove action-sublevel compactness in path space

Fixed mass and energy make each time marginal weakly tight. Path compactness additionally requires a uniform modulus for a convergence-determining family. The balance equation bounds test increments by contact mass, but entropy relative to `A_f` controls contact mass only after a uniform bound on `A_f([s,t])` and its velocity tails. Those bounds are not derived for all finite-action paths in the weak topology.

The proof also cites B3's closed balance and lower semicontinuity, while B3's functional-analytic framework and B2's dynamic LDP are unproved. Thus the attainment and concatenation results are not independent foundations for the semigroup.

### 9. The viscosity lower inequality is circular

The Lax–Oleinik proof uses the “B2 normalized regular tilt” as a recovery path. B2's lower bound itself uses a regularized tilt and later B3/B4 structures. The submitted dependency ledger declares B2 upstream, but the mathematical argument here assumes precisely the recovery theorem that remains missing in B2.

Similarly, microscopic convergence is first obtained from the B2 good LDP and then called “independent” because the invalid BBGKY corrector reaches the same equation. There are not two completed proofs.

### 10. The Gaussian tangent is only inherited from the invalid B3 theorem

The final risk-sensitive generator is the standard exponential transform of a Gaussian diffusion once a finite-dimensional Gaussian limit exists. B3 has not established the process covariance or tightness, and B1 has not established the prepared initial Schur complement. This subsection adds no microscopic proof.

## What is actually improved

The full-law versus one-density distinction and the weak-energy topology are now correctly stated. The variational action, if independently obtained from a valid joint LDP, would indeed generate a dynamic programming semigroup by concatenation. Those formal facts do not establish the announced full-BBGKY generator convergence or comparison theorem.

## Required reconstruction

A viable revision must:

1. replace the finite-time integral by a correct time-dependent Poisson/resolvent equation and retain all boundary terms;
2. prove bounded forward/backward hierarchy operators on the spaces actually used, or avoid negative-time evolution;
3. choose an analytic observable algebra and restrict the theorem to it, then separately approximate nonanalytic `C_b^3` cylinders;
4. augment the exact state to carry path-contact observables consistently;
5. prove graph-norm convergence of the infinite corrector;
6. construct a comparison penalization whose collision increment stays uniformly bounded; and
7. break the circular use of the B2 lower-bound recovery path.

## Recommendation

**Reject.** The topology repair is valid and the paper now types the exact law more honestly, but its principal corrector has an explicit nonzero boundary remainder, its observable algebra does not contain the claimed test class, and its comparison cotangents escape the Hamiltonian domain. The nonlinear kinetic semigroup has not been derived from the deterministic hierarchy.