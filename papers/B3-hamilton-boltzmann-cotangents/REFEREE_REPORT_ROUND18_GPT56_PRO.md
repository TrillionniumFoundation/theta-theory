# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** B3 — *Hamilton–Boltzmann Cotangent Geometry from Deterministic Hard-Sphere Collisions*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`B3_CUMULANT_MOSCO_PROCESS.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The observability, process CLT, and Mosco identification are not proved.

## 1. Overall assessment

The revision correctly removes a previous double counting of the collision bias: using control measure `qA_f` with integrand `\Delta p+\psi` is equivalent to using `A_f` with the factor `\sqrt q` in the integrand, but not to using both. It is also methodologically sound to separate construction of a Gaussian limit from identification of its Cameron–Martin form with a second variation.

The actual proofs do not achieve either objective. The first theorem claims velocity `H^1` observability from a cutoff hard-sphere collision operator, a regularity gain that the operator does not possess. The cumulant estimate depends on B2's invalid factorial majorant. The nuclear-space tightness argument omits the conditional estimates required for process convergence, and the action is treated as convex despite its nonlinear dependence on `A_f=ff_*B`. The claimed closed range, bounded right inverse, Gaussian process, and Mosco limit therefore remain unavailable.

## 2. Decisive mathematical objections

### 2.1. [FATAL] The observability estimate has the wrong coercive strength for cutoff hard spheres

Theorem `thm:r17-b3-observability` asserts

\[
\|p\|_{L^2(0,T;H^1_{x,v,w})}^2
\lesssim
\|F\|_{L^2(0,T;H^{-1}_w)}^2+
\int |\Delta p|^2q\,dA_f,
\]

modulo invariants and endpoints. In the angular-cutoff hard-sphere setting encoded by a finite collision kernel `B`, the linearized collision Dirichlet form gives a weighted `L^2` coercivity/spectral-gap estimate on the microscopic component. It does not control a full velocity derivative. Velocity fractional/Sobolev regularization is a feature of non-cutoff collision kernels, not of the cutoff operator used here.

The proof says that the biased collision operator is a bounded perturbation of the Maxwellian linearized operator and that its spectral gap gives “velocity coercivity,” then writes an energy controlling `H^1_v`. A spectral gap in weighted `L^2_v` cannot be upgraded to `H^1_v` by terminology. The transport commutator can transfer microscopic damping to hydrodynamic spatial modes (hypocoercivity), but it does not create missing velocity derivatives in the cutoff collision operator.

A direct diagnostic is to take a sequence of microscopic velocity functions with bounded weighted `L^2` norm and increasingly rapid velocity oscillations. The cutoff collision Dirichlet form remains comparable to a weighted `L^2` norm, while the `H^1_v` norm diverges. No estimate of the displayed form can hold uniformly for such a sequence.

This invalidates the theorem's principal estimate and hence the asserted Hilbert closed-range consequence and bounded right inverse. Every later quadratic correction that cites that right inverse fails with it.

### 2.2. [FATAL] The nonautonomous hypocoercive argument is only a slogan

Even after replacing `H^1_v` by a correct cutoff coercive norm, the proof would need substantial work. The coefficients `f(t)` and `q(t)` vary in time and space; the paper assumes only that they lie in a “small regular source chart” without defining the norms or proving uniform bounds. Freezing on a time partition and passing by Gronwall requires stability of domains, commutator estimates, and convergence of evolution families.

The treatment of the hydrodynamic block is also incomplete. Endpoint conditions do not automatically control all collision invariants for each spatial Fourier mode, and an exact balance gauge is not identified as a closed subspace of the declared weighted spaces. The conclusion “closed range and bounded inverse follow from the Hilbert closed-range theorem” requires an estimate for the adjoint on the orthogonal complement of the kernel in fixed Hilbert spaces; those spaces, kernels, and boundary conditions are not specified.

### 2.3. [MAJOR] The nuclear Gelfand triple is named rather than constructed

The manuscript says that `\mathscr S` is a projective intersection of weighted Sobolev spaces and that this gives a nuclear Gelfand triple. A countable intersection of Hilbert spaces is not automatically nuclear. One must choose the scale so that the embeddings between sufficiently separated levels are Hilbert–Schmidt (or nuclear), including the Gaussian velocity weights, time/space boundary conditions, and compatible contact traces.

The collision-test space `\mathscr S_c`, its symmetry quotient, and the direct-sum nuclear topology are likewise not defined. Without a concrete nuclear space, Mitoma's theorem and the path-space topology in `thm:r17-b3-clt` are not available.

### 2.4. [FATAL] The localized cumulant estimate rests on the invalid B2 expansion and is not derived after conditioning

Lemma `lem:r17-b3-cumulants` claims, for every deterministic interval `I`,

\[
|\kappa_{r,\varepsilon}(\Theta_1,\ldots,\Theta_r)|
\le C_r\mu_\varepsilon^{1-r/2}
(|I|+\mu_\varepsilon^{-1})\prod_j|\Theta_j|_{m'}.
\]

Its proof invokes the “fixed-horizon B2 factorial majorant.” In B2, the active source gives `k!C^kT^{k-1}` and then incorrectly drops `k!` to claim convergence. Thus the expansion on which this lemma relies has not been established.

Independently, the first-marked-vertex argument does not prove uniform localization for arbitrary intervals shorter than the microscopic collision scale. Multiple marks on one contact, boundary contacts at interval endpoints, and connected clusters spanning outside `I` must be counted. Exact microcanonical conditioning changes all cumulants through derivatives of a source-dependent saddle; it is not enough to say that a finite Schur complement preserves the same interval-local estimate. Uniform high-order saddle derivatives and locality of their correction terms would be required.

### 2.5. [FATAL] Finite-dimensional cumulants do not yield the stated process tightness by the submitted argument

The proof obtains a fourth-moment expression of the form

\[
\mathbf E\|Z_\varepsilon(t)-Z_\varepsilon(s)\|_{-m}^4
\le C(|t-s|+\mu_\varepsilon^{-1})^2.
\]

This estimate, even if valid, does not directly give uniform Kolmogorov tightness as `|t-s|\downarrow0` because of the nonvanishing microscopic term. For càdlàg processes one needs Aldous-type **conditional** increment estimates at stopping times, compact containment in a fixed dual space, and control of simultaneous contact jumps. The proof states that the probability of a jump larger than `\eta` tends to zero, but no scaling calculation for the marked contact masses is given.

The density coordinate is claimed to converge in `C([0,T];\mathscr S')`, while the microscopic empirical density under hard-sphere flow has collision-induced velocity jumps. Continuity may emerge after central-limit scaling in a sufficiently weak topology, but this needs an estimate showing the maximum jump tends to zero and that accumulated jumps have the correct bracket. The contact coordinate requires a precise `D` topology and compensator/martingale structure. Neither is constructed.

Mitoma's theorem reduces tightness on a nuclear dual to tightness of real projections only after the nuclear space and path topology are fixed. It does not replace the Aldous/compact-containment proof.

### 2.6. [FATAL] The limiting covariance and Gaussian martingale problem are inferred from a formal Hamiltonian

Differentiating a limiting log-Laplace Hamiltonian can identify candidate finite-dimensional covariances if the pressure convergence is sufficiently differentiable. It does not by itself construct a Gaussian process satisfying the exact linearized balance, initial/contact cross-covariances, or uniqueness in the chosen distribution space.

The proof cites the invalid observability theorem for uniqueness. It also treats the collision noise as an isonormal random measure with control `qA_f`, but no limiting martingale decomposition of the deterministic microscopic contact process has been proved. The covariance formula is plausible as a formal second variation; it is not a process CLT.

### 2.7. [FATAL] The action is treated as convex although `A_f` is nonlinear in `f`

Theorem `thm:r17-b3-mosco` calls the rescaled functionals `I_\eta` convex and uses convex duality to identify the quadratic form. The B2 action has the form

\[
I(f,\Gamma)=I_0(f_0)+\int \ell(d\Gamma/dA_f)\,dA_f,
\qquad A_f\propto ff_*B.
\]

The perspective entropy is convex in the pair `(A,\Gamma)`, but the map `f\mapsto A_f` is quadratic. The resulting functional need not be convex in `(f,\Gamma)` on the balance constraint. No proof of local convexity, prox-regularity, or twice epi-differentiability is given. Therefore the invocation of convex Mosco convergence and Legendre duality is unjustified.

The source also contains a malformed expression `q+\nho` in the entropy expansion, suggesting that the relative perturbation variable was not even consistently typeset in the active module. This is minor compared with the structural issue, but it obstructs literal verification.

### 2.8. [FATAL] The second-order recovery is not constructed

The proposed recovery takes a smooth tangent `(h,K)`, invokes the B3 bounded right inverse, and adds a second-order correction cancelling the nonlinear balance defect. Even if the right inverse existed, the nonlinear defect must be shown to lie in its range and to satisfy all endpoint, mass, momentum, energy, and gauge compatibility conditions. No calculation of the defect is provided.

Positivity is not secured by saying “after truncating the smooth tangent.” The background density and collision flow live on unbounded velocity space and may become arbitrarily small. An `L^2` or Sobolev-small perturbation need not be pointwise dominated by `f` or `qA_f`. To keep `\Gamma_\eta\ll A_{f_\eta}` with a positive ratio, weighted relative bounds are required.

The density of smooth range vectors in `\operatorname{Ran}\Sigma^{1/2}` is also asserted without a theorem connecting the analytic balance operator to the covariance range. Finally, identifying the quotient quadratic form with `\Sigma^{-1}` requires proof that the Gaussian covariance is the inverse of the Hessian on the exact quotient, not just a formal duality statement.

## 3. Dependency consequences

B3 depends on B2-GC and B1, both of which fail their own review. It also fails independently at the coercivity and Mosco stages. Its closed-range/right-inverse claim is subsequently used by B4 for control transfer and by C2 for hard-sphere rigidity; those uses are invalid.

## 4. Minimum requirements for reconsideration

A future submission would need:

1. a correct cutoff hard-sphere coercive space, or an explicit non-cutoff model if velocity Sobolev regularity is essential;
2. a fully specified nonautonomous hypocoercive observability/closed-range theorem;
3. an actual nuclear test-function scale with Hilbert–Schmidt embeddings;
4. a valid connected-cumulant theorem independent of the flawed B2 majorant;
5. stopping-time increment and compact-containment estimates for nuclear-dual process tightness;
6. a microscopic martingale/covariance derivation;
7. a nonconvex second-order variational framework, or proof of the local convexity being used;
8. an explicit positive exactly balanced second-order recovery.

## 5. Recommendation

**Reject.** The normalization of the collision noise is improved, but the foundational observability estimate has the wrong regularity for the cutoff hard-sphere operator. The process CLT and Mosco theorem then rely on unavailable cumulant, tightness, convexity, and recovery results. The manuscript is not close to a complete proof at a top-journal standard.