# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A1 — *Deterministic Path Ensembles, Driven Collision Maps, and Endogenous Conjugate Parameters*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `ef750c21c1a933e38b41c72b0d6ddee6efe198db`

## Executive assessment

Round eight correctly recognizes that every iterated preimage seam must be retained. It therefore replaces the finite biseam cell complex by a graph over the two-sided full shift and also abandons the previous isotropic-Hölder spectral claim. Those are genuine conceptual improvements.

The replacement does not define the claimed mechanical system. The new “complete dynamic germ surface” is homeomorphic to a Cantor shift, not to a two-dimensional Liouville section, while the autonomous Hamiltonian theorem treats it as the Poincaré section of a smooth symplectic flow. The auxiliary router returns to one physical point and hence cannot remember the extra symbolic germ that distinguishes two endpoint expansions. Independently, the proposed depth-weighted norm does not yield the displayed Lasota–Yorke contraction for a bilateral invertible shift: shifting trades future depth for past depth and does not remove total depth. Thus both the mechanical realization and the response theorem remain invalid.

## Genuine repairs recognized

The manuscript should retain the following changes:

- all forward and backward singularity cuts are acknowledged;
- the work cocycle is supported on the full incoming port rather than a smaller core;
- the mechanical/valuation coefficient identification is stated as a conditional compatibility axiom;
- the paper no longer relies on an ordinary isotropic Hölder spectral gap for an invertible baker map.

These repairs do not close the theorem package.

## Fatal mathematical objections

### 1. The complete germ surface is not a symplectic return section

For an alphabet with at least two symbols, the two-sided shift space

\[
\Omega=\mathcal A^{\mathbb Z}
\]

is a compact totally disconnected Cantor space. The graph

\[
\widehat\Sigma_a^\infty
=\{(q_a(\omega),p_a(\omega),\omega):\omega\in\Omega\}
\]

is homeomorphic to \(\Omega\). It is therefore not a two-dimensional manifold with corners, does not carry the area form \(dq\wedge dp\) as a nondegenerate symplectic form, and has no Liouville area measure of the kind used later.

A smooth Hamiltonian Poincaré section is a finite-dimensional smooth or stratified symplectic object. One may form a symbolic extension of such a section, but the symbolic extension is not itself the physical section. The manuscript repeatedly identifies these two different objects.

### 2. The routed suspension cannot distinguish germs after the router returns to zero

The claimed section is

\[
\{\tau=0,\ y=\eta=0\}.
\]

At the end of every route the auxiliary pair returns to \((0,0)\). Two symbolic endpoint expansions having the same physical coordinates \((q,p)\) therefore arrive at the same point of this smooth section. A deterministic Hamiltonian flow has one future from one phase point; it cannot choose two different images according to an additional symbol that is absent from the phase point.

To realize the symbolic germ extension mechanically, the phase space would need distinct physical sheets or an explicit discrete/branched coordinate retained on the return section. The present router erases exactly the information on which \(\widehat F_a\) depends.

### 3. The Lasota–Yorke estimate is incompatible with the bilateral shift and the declared weight

The proof says that the shift “removes one future symbol and adds one past symbol.” With the norm weighted only by total word length

\[
\ell(w)=r+s+1,
\]

this operation preserves total depth. It gives no factor \(\rho<1\).

A concrete translated-cylinder test exposes the problem. Let \(f_N\) be a centered observable depending only on the coordinate \(\omega_N\). In the proposed scale its minimal cylinder description lies at future depth \(N\), so its weak-to-strong ratio tends to zero as \(N\to\infty\). Applying the inverse-shift transfer \(N\) times moves the same martingale difference to the present coordinate. Its strong norm is then order one rather than \(O(\rho^N)\), while the compact weak term was chosen to be vanishingly small. This contradicts the displayed uniform Lasota–Yorke estimate.

An anisotropic space for an invertible shift must distinguish forward and backward regularity directionally. A symmetric total-depth weight does not do so.

### 4. The spectral-gap proof is not a proof on the completed current space

The statement that “the shift removes the first martingale difference” is a one-sided argument. The system and the norm are two-sided. The Perron/Koopman operator of the invertible Bernoulli shift is unitary on the natural \(L^2\) space, and a nontrivial spectral gap requires a carefully constructed anisotropic distribution space. No such directional construction or resolvent estimate is supplied here.

The asserted compact embedding also depends on representing all refined cylinder currents by a unique compatible coefficient system. The phrase “the cylinder relations are quotiented before completion” does not define that quotient, prove it Hausdorff, or establish the tail estimate used in the compactness argument.

### 5. “Matching flat jets on every symbolic germ” is undefined in the smooth router

There are infinitely many dynamically generated seam germs, dense in the physical square. The router construction uses finitely many tubes indexed only by the current branch \(i\). It does not construct collars or smooth compatibility data for all iterated symbolic seams. A smooth Hamiltonian in the physical and routing coordinates cannot have separate jets indexed by the full bi-infinite sequence after the symbolic coordinate has been removed from the smooth phase space.

### 6. The response theorem has no typed physical operator once the section fails

The parameter-current expressions are defined on the symbolic graph, whereas the claimed Liouville expectation and mechanical work are defined on a smooth Hamiltonian section. Since no measure-preserving identification between these objects has been constructed, the physical response formula and the statement that common-root finite differences recover all seam currents are unproved.

### 7. Top-four novelty remains insufficient after a correct scoping

A valid symbolic version would consist of an explicit Bernoulli coding, an additive cylinder cocycle, and parameter differentiation of product measures. A valid smooth mechanical version would require a new branched symplectic realization and a genuine anisotropic response theorem. The current paper supplies neither completed theorem, and the symbolic residue alone is far below the required editorial threshold.

## Required reconstruction

A viable reconstruction must choose one of two honest objects:

1. a symbolic extension, explicitly labelled as such, with no claim that the Cantor graph is a Liouville section; or
2. a finite-dimensional branched/sheeted symplectic section in which every retained germ is an actual phase-space point and the Hamiltonian return map is single valued.

Only after that object exists can one build a directional anisotropic transfer scale and prove parameter response. The depth norm must be redesigned so that the bilateral shift has a true strong/weak contraction.

## Recommendation

**Reject.** Round eight fixes the finite-seam bookkeeping but replaces it by a Cantor symbolic graph that is then incorrectly treated as a smooth symplectic return section. The transfer-space contraction is independently false on the declared bilateral depth norm.