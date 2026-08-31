# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C2 — *Path-Space Cotangent Rigidity, Universal Contractions, and Tangent Representations*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/C2_SCALE_CONNECTION_RESOLVED_MEMORY.tex`  
**Reviewed source SHA-256:** `966d20ec2c6c4331a3149539dd186bfd65693a3b67fef2118a08448c738dd3a5`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

The paper now distinguishes invariant-integral and pressure null spaces, avoids infinite-volume Radon–Nikodym trivializations, and separates the phase spectral projector from the physical resolved projection. These are important corrections.

The new Kato construction is not well posed on a regularity-losing Banach scale, and it does not construct the Hilbert-space resolved projection or its differentiable inner product. The invariant-separator theorem also rests on an unproved uniform Lyapunov bound for arbitrary signed measures. Optional projections remain downstream of the false A4 martingale/semigroup package.

## Major objections

### 1. The Kato ODE is not typed on the stated scale

The projector derivative is only a map
\[
 (\Pi_\eta^{\rm sp})':
 \mathbb B^{m+1}\to\mathbb B^m.
\]
Hence the commutator in
\[
 U'=[(\Pi^{\rm sp})',\Pi^{\rm sp}]U
\]
loses one level of regularity. Picard iteration applies the coefficient repeatedly and would require
\[
 \mathbb B^{m+2}\to\mathbb B^{m+1}\to\mathbb B^m\to\mathbb B^{m-1}\to\cdots .
\]
It does not define an evolution on one Banach space, let alone an invertible map with an inverse on the same scale.

An operator from \(\mathbb B^{m+1}\) to \(\mathbb B^m\) cannot be “invertible” in the sense needed for a trivialization. A tame scale theorem, smoothing connection, or fixed-space construction is required.

### 2. The formula for the Doob generator is not well defined

The manuscript writes
\[
 L_\eta^D=h_\eta^{-1}(L_\eta-P_\eta)h_\eta,
\]
but \(P_\eta\) is not identified here as a scalar pressure/eigenvalue or an operator; the notation is already used for projections elsewhere. Domains of multiplication by \(h_\eta^{\pm1}\) on the strong/weak scale are not established.

### 3. Kato transport of an eigenline does not construct a phase Hilbert bundle

The transfer Banach space and the phase \(L^2\) correlation space are different objects. Transporting the leading Riesz eigenline does not produce:

- a common Hilbert space for all source parameters;
- differentiability of the full correlation inner product;
- an orthogonal projection \(R_\eta\) onto arbitrary resolved observables; or
- bounded derivatives of that projection.

The sentence “re-orthonormalize with its differentiable Gram matrix” assumes the differentiability and nondegeneracy that must be proved.

### 4. The uniform Cesàro estimate is not established for every signed measure

The lemma quantifies over every finite signed weighted Radon measure:
\[
 \sup_{T\ge1}\frac1T\int_0^T\int W\circ\Theta_t\,d|\mu|\,dt
 \le C\int(1+W)d|\mu|.
\]
Platform estimates for a distinguished Gibbs or prepared law do not imply this bound for an arbitrary signed measure. If \(W\) includes return, history, or contact-ledger coordinates, its orbit average can grow from initial states with long deterministic excursions or accumulating ledger mass.

Without the uniform estimate, the Cesàro averages need not be weighted tight, and the Hahn–Banach separator need not yield an invariant probability.

### 5. The cotangent annihilator theorem needs more than signed-measure averaging

Even if an invariant signed separator exists, the Jordan components must be invariant and have finite nonzero mass before they can be normalized to invariant probabilities. These points are not checked on the weighted noncompact space. The theorem should be stated conditionally on a complete dual/ergodic averaging result.

### 6. The compressed resolvent may not be invertible on the asserted half-plane

For an arbitrary resolved projection \(R_\eta\), the finite matrix
\[
 R_\eta(z-L_\eta^D)^{-1}R_\eta
\]
can have transmission zeros. A4 explicitly introduces zeros and descriptor modes. It does not give invertibility on a common right half-plane for every moving \(R_\eta\) and parameter. The memory derivative formula is valid only away from zeros, with domain and contour changes tracked.

### 7. The derivative of memory is formal until the moving domains are fixed

Even algebraically correct covariant formulas require a common domain for \(L_\eta^D\), resolvent differentiability, differentiability of \(R_\eta\), and compatibility of the Banach and Hilbert pairings. None has been constructed.

### 8. Optional-projection convergence inherits A4's false probability theorem

A4's martingale–coboundary decomposition is algebraically wrong and its normalized nonlinear history pressure is not a semigroup. The claimed uniform quenched kernel theorem therefore cannot be used as a closed input here.

### 9. The final contraction theorem is generic

The contraction principle and ordinary chain rule are valid under their hypotheses, but they do not supply any new platform theorem. The paper repeatedly packages conditional standard facts as a universal rigidity result.

## Dependency assessment

C2 is downstream of A2/A3/A4 and B1/B2/B3. It also has an independent scale-connection failure. None of its memory or optional-projection diagrams can be certified at present.

## Required reconstruction

The source response should be formulated on one fixed transfer Banach space, or with a rigorous tame-scale evolution. The physical resolved Hilbert space and projection must then be constructed separately from the spectral eigenline. Cotangent separation should be stated under a proved platform-specific averaging theorem.

## Recommendation

**Reject.** The Kato transport is not a well-defined invertible evolution on the declared scale, and the resolved-memory Hilbert bundle is assumed rather than built.
