# Independent Referee Report — Round 15

**Manuscript:** C2 — *Cotangent Rigidity and Tangent Representations*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence and submission integrity

No Round-Fifteen C2 module is present in the paper folder or recoverable from the truncated payload. The controlling source is Round Fourteen. The branch therefore does not provide the claimed new C2 revision for review.

## Executive assessment

Separating the strict Radon topology from the stronger response topology is necessary, and the invariant-integral quotient is stated more carefully than in earlier rounds. The common form-bundle theorem still omits the derivative of the varying Hilbert metric, and the compressed memory operator is not defined for resolved observables lying only in the form domain. Several later stochastic representations are explicitly conditional on A4/B3 inputs that are not proved.

## Decisive objections

### 1. Differentiating a varying Hilbert realization creates an extra term

The weak resolvent equation is written as

\[
z(u,v)_{H_\eta}+a_\eta(u,v)=\langle f,v\rangle.
\]

If \(H_\eta\) has a parameter-dependent inner product, differentiation yields

\[
z\,D_\eta (u,v)_{H_\eta}
+(D_\eta a_\eta)(u,v)
+\text{terms from }D_\eta u.
\]

The manuscript writes only

\[
D(z-L_\eta)^{-1}
=(z-L_\eta)^{-1}(DL_\eta)(z-L_\eta)^{-1}.
\]

That formula is valid after transporting all operators to one fixed Hilbert space and including the metric/connection derivative in \(DL_\eta\). A common form domain alone does not provide such a transport. The missing term changes the response formula.

### 2. \(P_\eta L_\eta P_\eta\) may be undefined

The resolved observables are assumed to lie in the common form domain

\[
V=D((-L_\eta)^{1/2})
\]

but the memory formula uses the operator compression

\[
P_\eta L_\eta P_\eta.
\]

In general \(V\not\subset D(L_\eta)\). A finite-dimensional subspace of the form domain need not lie in the generator domain.

The paper must either choose resolved vectors in a common operator core or formulate the compression entirely through the closed form. Without that, the Schur complement and its derivative are ill-typed.

### 3. The claimed common-domain equivalence is imported, not proved

The text assumes the uniform real coercive form estimates “proved in A4/B4.” Those papers do not construct one common form on the same platform/state space with the required parameter differentiability. Sinai transfer operators, suspension generators, hard-sphere kinetic forms, and memory projections are different objects. They cannot be merged into one theorem by notation.

### 4. Radon quotient and strong response remain only loosely connected

The strict topology gives signed Radon measures as a dual. The strong anisotropic/graph topology admits distributions. Pullback embeds the Radon dual into the strong dual, but pressure differentiability on the strong source space need not determine every strict-topology invariant measure, nor does Hahn–Banach in one topology identify the annihilator closure in the other.

The rigidity theorem differentiates a local pressure family and then claims a global coboundary representation. The precise source domain, density of perturbations, and periodic-orbit/finite-time separation theorem are not supplied.

### 5. The optional-projection theorem is conditional on missing filtration convergence

The paper explicitly assumes conditional-kernel convergence and a uniform \(L^{1+\delta}\) likelihood bound. A4's controlling manuscript does not prove the required filtration-level extended weak convergence, and B3 does not prove the likelihood estimate. The Girsanov and BSDE conclusions are standard once those hypotheses hold; they are not independent results of C2.

### 6. The pressure-rigidity argument overreaches its local chart

Equality of the full perturbation functionals on a neighborhood can identify nearby equilibrium derivatives. It does not by itself show equality of all periodic sums or every balanced variation outside that neighborhood. The Sinai Livšic conclusion and hard-sphere balance-gauge conclusion each require a model-specific density/separation theorem on the precise observable space.

### 7. Cross-platform synthesis obscures rather than closes dependencies

The Sinai and hard-sphere objects have different path spaces, forms, filtrations, and null modes. A “platform-typed” statement is legitimate, but each platform requires its own complete theorem. The present manuscript packages unresolved interfaces and calls the package a common cotangent theory.

## Required reconstruction

Fix one platform. Transport all Hilbert spaces to a fixed reference space or include an explicit metric connection. Put resolved observables in a common operator domain or use form-level memory. Prove the rigidity and filtration results from model-specific inputs before presenting them as a synthesis.

## Recommendation

**Reject.** No Round-Fifteen C2 manuscript is present, and the controlling common-domain response formula omits necessary metric terms and uses an undefined operator compression.
