# Independent Referee Report — Round 13

**Manuscript:** C2 — *Cotangent Rigidity and Tangent Representations*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `44489f62a01903ffc80a8243361cd2cfb425cab4efe7d9b1ed88c512c944697b`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 13 correctly separates equality of invariant integrals from equality up to a constant, uses the full perturbed pressure functional rather than one scalar pressure value, keeps source and state derivatives distinct, and avoids identifying mutually singular path laws by Radon–Nikodym square roots. These are genuine repairs.

The replacement functional analysis is not valid as stated. The space is introduced as a weighted dynamically Hölder cylinder algebra, but the proof identifies its continuous dual with Radon measures by invoking the strict dual theorem for weighted continuous functions. A Hölder/graph norm has a much larger dual, including distributional functionals. The proposed common form norm also uses `a_eta(F,F)` for sectorial, generally nonsymmetric forms; this quantity need not be real or nonnegative and therefore does not define a norm. Finally, type-(B) differentiability requires one fixed form domain, whereas the proof repeatedly consumes “fresh strong levels.” The central common-domain and memory-response theorems consequently have no valid domain.

## Decisive objections

### 1. The continuous dual of a Hölder/graph algebra is not just Radon measures

The manuscript defines `mathscr A_W` as a weighted dynamically Hölder cylinder algebra and takes the closure of coboundaries in that space. It then says that “weighted strict duality” represents every continuous functional by a countably additive signed Radon measure.

That duality theorem applies to an appropriate weighted continuous-function space equipped with the strict topology. It does not apply automatically to a stronger Hölder, differentiable, anisotropic, or graph norm. The dual of such a space contains continuous distributional functionals. On a smooth cylinder coordinate, for example,

\[
 F\longmapsto \partial_xF(x_0)
\]

is continuous in a `C^1`/graph norm but is not integration against a finite Radon measure.

Therefore

\[
 (\mathscr A_W/\mathscr N_{\rm inv})'
\]

cannot be identified with invariant signed measures until the exact locally convex topology is fixed and its dual is proved. If the authors switch to the strict topology to obtain Radon duality, the Hölder spectral and coboundary closures used elsewhere change.

### 2. Time averaging a separator does not prove equality with the coboundary closure in the stronger norm

Even when a functional is a measure, Cesàro averaging produces an invariant weak-* limit. It shows separation from a weak/strict closure of coboundaries. It does not show separation from a closure taken in a stronger dynamically Hölder norm unless the averaging maps are uniformly bounded and the dual topologies are matched.

The theorem conflates the norm closure needed for spectral response with the strict closure needed for Radon duality.

### 3. The proposed common-domain expression is not a norm for sectorial forms

The manuscript defines

\[
 \|F\|_{\mathcal V}^2
 =\sup_\eta\left(
 \|F\|_{L^2(\pi_\eta)}^2+
 \mathfrak a_\eta(F,F)+
 \|F\|_{\rm tr,\eta}^2\right).
\]

A closed sectorial form is generally nonsymmetric and complex-valued. The scalar `a_eta(F,F)` need not be real, much less nonnegative. It cannot be inserted into a norm without taking a shifted real part such as

\[
 \operatorname{Re}\mathfrak a_\eta(F,F)+c\|F\|^2
\]

and proving uniform sector/coercivity constants.

This is a direct typing error in the construction of the central space `mathcal V`.

### 4. “Fresh strong levels” are incompatible with type-(B) differentiability on one common domain

Kato type-(B) differentiability requires a fixed dense form domain `V` and differentiability of

\[
 \eta\mapsto\mathfrak a_\eta(F,G)
\]

for every fixed `F,G in V`, with uniform form bounds. The manuscript instead says that the `q`th derivative is available for vectors in “corresponding fresh strong levels.” That is a Banach-scale loss, not a differentiable type-(B) family on `V`.

Completing the cylinder algebra in the supremum of the zero-order forms does not guarantee that all higher-level derivatives extend to that completion. The resolvent derivative formula is therefore not justified on the claimed common space.

### 5. Supremum completion does not prove density in every phase Hilbert space

Even after replacing the sectorial term by its real part, the completion under

\[
 \sup_\eta\|F\|_{\eta,\rm form}
\]

can be much smaller than the individual form domains and need not be dense in each `L^2(pi_eta)`. Mutual singularity of the phase measures makes this a genuine issue. A common core of cylinders does not imply that its supremum-form completion is a common closed form domain for all generators.

The paper needs explicit uniform core and closure theorems, not the assertion that compactness of the parameter chart makes the norms equivalent.

### 6. The hard-sphere pressure-rigidity argument is insufficient

Equality of the full local pressure increments implies equality of all local cumulants under appropriate analyticity. The proof then invokes “strict convexity on the B3 quotient” to conclude that the base source difference is a constant plus the endpoint–balance gauge.

B3 does not prove strict convexity on the full infinite-dimensional source quotient; it proposes a covariance kernel on a perturbative chart, and its process proof is invalid. Equality of first and second variations is not by itself a global cohomology theorem. The hard-sphere rigidity conclusion is therefore an assumed interface.

### 7. The compressed-memory derivative inherits an unproved and partly false A4 decomposition

A4's memory theorem assigns descriptor modes before all pole-zero cancellations and has no valid Feynman–Kac source chart. C2 cannot obtain differentiability and exponential decay by citing that result. It also must prove that the finite resolved observables lie in the common generator/form domain and that the compressed matrix remains invertible away from tracked zeros.

### 8. Filtration convergence is not proved in A4

A4 establishes, at most, a proposed Wasserstein coupling and rough limit for additive functionals. It does not prove extended weak convergence of the microscopic filtrations, convergence of conditional future kernels on the complete likelihood class, or uniform `L^{1+delta}` bounds for likelihood martingales.

Those are precisely the hypotheses stated immediately before the optional-projection theorem. Saying that A4 proves them does not make it so. The Girsanov and BSDE conclusions remain conditional.

### 9. The paper is a synthesis without an independent closed theorem

The corrected source/state chain rules are elementary. The invariant quotient requires a new topology, the rigidity theorem imports A2/B3, the memory theorem imports A4, and the likelihood theorem imports A4/B3. Once those unresolved interfaces are removed, no standalone top-four contribution remains.

## Genuine improvements recognized

The two invariant-integral statements are now correctly separated, scalar-pressure rigidity has been abandoned, source and state derivatives are typed separately, and the use of infinite-path Radon–Nikodym trivializations has been removed. These changes should be retained.

## Dependency assessment

C2 depends on A2–A4 and B2–B4. Every one of those chains remains open. C2 cannot be used by D1 as a certified cotangent, memory, optional-projection, Girsanov, or BSDE interface.

## Required reconstruction

The authors must select one precise source topology. If Radon duality is desired, use a weighted continuous strict topology and restate the spectral claims on a separate stronger space with an explicit pairing. The generator family must be built from shifted real sectorial forms on one genuinely common dense domain. Filtration convergence should be a separate theorem with its own hypotheses and proof.

## Recommendation

**Reject.** Round 13 corrects several conceptual distinctions, but the invariant dual is identified in the wrong topology, the common form “norm” is not a norm, and the claimed type-(B), memory, and filtration theorems are unsupported.
