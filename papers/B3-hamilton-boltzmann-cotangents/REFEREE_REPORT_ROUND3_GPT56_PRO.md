# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangent Geometry from Deterministic Hard-Sphere Collisions*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `326617914838c44414485263768b92d249ee520e`

## Executive assessment

The revision correctly recognizes the larger representation gauge that invalidated the previous cotangent uniqueness theorem. The invariant object is now the combination

\[
z=\Delta p+\psi,
\]

and the pair `(p,psi)` is quotiented by `(r,-Delta r)`. The finite-volume Hessian normalization is also corrected, and the paper attempts to specify weighted primal and Orlicz dual spaces.

These are important improvements. The new duality theorem is nevertheless false on the very singular measures it claims to cover: the exponential Orlicz space is defined modulo `A_f`-null sets, so it cannot be paired continuously with a collision measure singular to `A_f`. The proof’s singular-part test uses a function that is the zero element of the Orlicz space. The claimed `+infinity` alternative is therefore unavailable.

The positivity of the quotient covariance, global uniqueness of information projections, and path-space Gaussian limit are also asserted by arguments far too weak for their conclusions. The paper remains downstream of the unproved B1/B2 theorems.

## Improvements relative to the preceding circulation

1. The full gauge `(p,psi) ~ (p+r,psi-Delta r)` is now explicit.
2. Collision invariants are correctly treated as only a subset of the gauge directions.
3. The finite-volume identity

\[
D^2Q_\epsilon=\mu_\epsilon\operatorname{Cov}
\]

is stated correctly.
4. The initial microcanonical covariance is represented by the B1 Schur complement.
5. The paper attempts to define a weighted density/collision topology and an exponential-Orlicz dual.

These changes remove the most elementary defects of the prior version, but not the analytical ones.

## Major mathematical objections

### 1. The Orlicz dual cannot detect collision measures singular to `A_f`

The paper defines the collision-source space as an exponential Orlicz heart relative to the reference measure `A_f`. Such a space consists of equivalence classes modulo `A_f`-null sets. If `B` satisfies

\[
A_f(B)=0,
\qquad
\Gamma(B)>0,
\]

then `1_B` is the zero element of the Orlicz space. The proof of the duality theorem nevertheless takes

\[
z=n1_B
\]

and integrates it against `Gamma` to force the supremum to infinity.

This pairing is not well defined on the Orlicz equivalence class. Choosing a different representative changes `\int z\,d\Gamma` while leaving the Orlicz element unchanged. If one instead treats pointwise functions with the Orlicz seminorm, the source space is non-Hausdorff and integration against singular `Gamma` is not continuous.

Consequently the theorem

\[
\sup_{p,\psi}\mathfrak L_{f,\Gamma}(p,\psi)
=
+\infty
\quad\text{for }\Gamma\not\ll A_f
\]

is not proved and is generally false for the declared dual pair.

A correct construction can dualize first against bounded continuous collision functions, whose dual contains Radon measures, and then identify the absolutely continuous entropy part by monotone approximation. The current Orlicz formulation cannot simultaneously provide the entropy conjugate and see arbitrary singular measures without an enlarged dual topology.

### 2. The exact gauge sequence assumes the main continuity statement

The sequence

\[
0\to\mathcal Y_p
\xrightarrow{r\mapsto(r,-\Delta r)}
\mathcal Y_p\times\mathcal Y_\psi
\xrightarrow{(p,\psi)\mapsto\Delta p+\psi}
\mathcal Y_z\to0
\]

is algebraically exact if `Delta` is a continuous map from `Y_p` into the same Orlicz source space. The manuscript defines `Y_p` only as a completion under a norm that “controls” `Delta p`; it does not prove that the completion has well-defined endpoint traces, transport derivative, collision increment, or continuous image in `Y_psi`.

The closed-range conclusion is therefore conditional on a function-space theorem that is not supplied.

### 3. The quotient-covariance nullspace is not identified

The proof of positive quotient covariance says that zero variance would make an observable constant under every microscopic configuration in an open hard-sphere phase set, and that varying one free flight and one collision shows it is a gauge.

Zero asymptotic variance does not imply pointwise constancy. It can indicate a dynamical coboundary, a balance identity, a conservation law, or a null direction of the limiting hierarchy. Proving that the covariance nullspace equals the closed balance-gauge range requires a density/annihilator theorem in the selected weighted spaces.

The repository contains an attempted lemma in `B1_B3_NULLSPACE_PACKET.tex`, but it is not included in the controlling manuscript. Even there, the key statement that local free-flight and collision variations are dense in the full balanced tangent space is only asserted through a partition-of-unity argument.

### 4. Local strict convexity does not give global uniqueness of the information projection

The inverse-function theorem gives a locally unique source and phase in a regular analytic chart. It does not exclude another minimizer outside that chart with the same macro value and lower or equal rate. The theorem states that the constrained information projection is unique for every target in the local mean image, but no global strict convexity of the rate or global exposedness argument is given.

The correct conclusion is local uniqueness of the analytically parameterized phase, unless a separate global variational theorem rules out competing phases.

### 5. The path-space Gaussian limit does not follow from cumulant convergence alone

Normal convergence of finite-dimensional log-moment functions can identify limiting cumulants for finitely many tests. It does not establish tightness of the processes

\[
\sqrt{\mu_\epsilon}(\pi^\epsilon-f),
\qquad
\sqrt{\mu_\epsilon}(\Gamma^\epsilon-\Gamma)
\]

in a weighted distribution path space. The macroscopic exponential compact containment claimed in B2 controls order-one deviations; it is not a central-limit-scale modulus estimate.

A process CLT requires uniform martingale or correlation estimates, a Mitoma-type tightness theorem on a specified nuclear/test space, endpoint control, and uniqueness of the limiting martingale problem. The manuscript supplies none of these.

### 6. The collision fluctuation formula contains undefined derivatives

The theorem writes

\[
\Xi(\psi)
=
\int\psi\,dM^{\rm coll}
+
\int\psi\,DA_f[\zeta]q
+
\int\psi\,A_fDq[\zeta].
\]

It does not define the map `q(f)` or the derivative `Dq[zeta]`. If `q=e^{Delta p+psi}` for a fixed external source, `q` has no density derivative. If `p` is an optimizer or solution depending on `f`, its derivative must be obtained from a specified linearized adjoint equation. The formula is not typed.

### 7. The integral duality proof omits endpoint and density-domain issues

The balance pairing involves endpoint traces, transport derivatives, and collision increments on unbounded velocity space. The proof reduces everything to a scalar conjugacy after one formal use of balance. It does not show density of smooth tests in the completed trace space, continuity of the endpoint maps, or closure of the product measure `A_f` under the allowed density-path convergence.

These are not cosmetic details; they determine whether Fenchel–Rockafellar duality applies.

### 8. The theorem remains dependent on unproved upstream results

- B2 does not prove the global actual-collision joint LDP or source continuation.
- B1 does not prove its mixed lattice/continuous shell coefficient.
- The microcanonical pressure derivatives and covariance therefore have no established microscopic source.

Formal convex analysis cannot substitute for those inputs.

### 9. The controlling manuscript is not standalone

The active source consists of a preamble and one closure module. The underlying hard-sphere law, source domain, B2 rate, B1 shell, and weighted test spaces are not defined at submission-level completeness.

## Editorial recommendation

**Reject.** The gauge correction is conceptually right and should be retained. A viable paper must choose a dual pair that genuinely includes countably additive collision measures, prove the balance-adjoint complex and its nullspace on explicit spaces, restrict multiplier uniqueness to what the analytic chart proves, and establish a separate central-limit tightness theorem. Until B1 and B2 exist, the deterministic interpretation of the Hamiltonian remains conditional.