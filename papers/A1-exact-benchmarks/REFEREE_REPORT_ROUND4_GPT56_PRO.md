# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A1 — *Deterministic Path Ensembles, Driven Collision Maps, and Endogenous Conjugate Parameters*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `e1508999b777aded8fa5ca911440818e3cb09cc1`

## Overall assessment

The revision makes two real improvements. It abandons the false claim that the affine baker branches are globally generated on a torus by the Hamiltonian `qp`, and it correctly types change of law on a common symbolic path space. It also now distinguishes a mechanical conjugate field from an arbitrary preference parameter unless a canonical-cocycle compatibility axiom is imposed.

The new mechanical realization is nevertheless not a well-defined return-flow construction as written. The mapping-torus gluing has incompatible incoming and outgoing cut surfaces, the purported work one-form does not descend through the gluing, and the response section uses operators which are nowhere defined in the controlling paper. Even after these defects are repaired, the remaining mathematics is an elementary Bernoulli benchmark rather than a top-four contribution.

## Major objections

### 1. The announced mapping torus is not defined from the displayed data

The manuscript sets

\[
\mathcal Q_a^- = \bigsqcup_i I_i(a)\times(0,1),
\qquad
\mathcal Q_a^+ = \bigsqcup_i (0,1)\times J_i(a),
\]

and constructs a symplectic bijection

\[
R_a:\mathcal Q_a^-\longrightarrow\mathcal Q_a^+.
\]

It then forms

\[
\widetilde{\mathcal M}_a=\mathcal Q_a^-\times[0,1]\times\mathbb R_E
\]

and writes `(x,1,E) ~ (R_a x,0,E)`. The bottom boundary of this product is a copy of `\mathcal Q_a^-`, whereas `R_a x` belongs to `\mathcal Q_a^+`. A mapping torus requires a self-map of one boundary manifold, or a cobordism whose two boundary parametrizations are explicitly specified. Neither is supplied.

There is a necessary “recutting” map from the horizontal partition to the next vertical partition. It must forget the outgoing strip label and assign the next incoming label from the new `Q` coordinate. If instead one identifies equal branch labels, every orbit remains in one branch and the Bernoulli itinerary is lost. The revision does not define this recutting map, prove that it is symplectic on the cut completion, or show that the resulting quotient is Hausdorff and a manifold with corners.

Thus the first-return theorem is not presently a theorem about a constructed Hamiltonian flow.

### 2. The proposed work one-form does not descend to the quotient

The manuscript declares

\[
\alpha=c(x)d\tau,
\qquad c(x)=\epsilon_i\text{ on incoming port }i.
\]

For a one-form to descend through the gluing one needs compatibility of its two boundary traces. Here that would require

\[
c(x)=c(R_a x)
\]

under the actual recutting identification. This is false for a nontrivial itinerary: the next branch sign is generally different from the current one. Hence `c(x)d\tau` is not a globally defined one-form on the claimed mapping torus.

The current can certainly be retained as a measurable section cocycle, but then it must be stated and proved as such. It cannot simultaneously be called a globally defined mechanical port-work one-form.

### 3. Exact symplecticity does not prove the collar realization asserted

The collar theorem says that exactness of each branch primitive produces a compactly supported Hamiltonian isotopy between the identity and the branch after embedding the incoming and outgoing rectangles in disjoint Darboux collars. This requires a relative symplectic extension theorem with specified embeddings, boundary behavior, flux, and compatibility with the recutting map. The proof supplies none of these data.

The phrase “standard Moser correction” is especially insufficient: Moser's argument adjusts forms, not automatically a prescribed discontinuous four-port return correspondence while preserving the core map, return time, port flux, and work integral.

### 4. The all-order response theorem is not typed in the controlling manuscript

The response section introduces

\[
L_a,\quad \Pi_a,\quad Q_a=I-\Pi_a,\quad
S_a=(I-L_a)^{-1}Q_a,
\]

and a contraction constant `\rho_K`, but none of these operators, spaces, invariant densities, or projectors is defined in the controlling module or in `main.tex`. Compilation does not repair this omission.

Even if one infers the elementary one-dimensional Perron operator, the derivative of `Q_a`, the precise centered space, and the domain/codomain of every word must be stated. The final theorem currently invokes undefined mathematical objects.

### 5. The calibration theorem is conditional rather than a mechanical selection theorem

The Kolmogorov--Nagumo/CARA calculation is standard once one assumes one smooth utility, cash additivity, conditional law invariance, and strong time consistency. The equality of its coefficient with the current multiplier is then imposed by requiring equality of the two likelihood cocycles and common physical units.

This is a legitimate compatibility theorem, but it is not a derivation that mechanics uniquely selects the coefficient among all valuation functionals. The abstract and title should maintain that distinction consistently.

### 6. Correctly scoped content remains below the journal threshold

After replacing the global mechanical claims by a properly defined cut-section cocycle, the unconditional content is:

- an exactly solvable Bernoulli baker family;
- hypergeometric-to-Bernoulli conditioning;
- an elementary exponential tilt;
- a standard CARA classification under strong axioms; and
- geometric-series response estimates for an affine transfer operator.

This is useful benchmark material, but not a theorem of the depth, novelty, or breadth expected by any of the four journals.

## Required reconstruction

A viable benchmark note would need to:

1. define an actual self-return map on one cut symplectic section, including the horizontal-to-vertical recutting;
2. construct the suspension as a precise symplectic cobordism or mapping torus;
3. replace the non-descending work one-form by a well-typed section cocycle, or construct a genuinely global form;
4. define every transfer operator and projector used in the response calculus; and
5. state the calibration result explicitly as conditional on the canonical-cocycle axiom.

## Recommendation

**Reject.** The revision fixes the previous torus-Hamiltonian error but does not yet construct the claimed Hamiltonian return flow, and the corrected symbolic theorem is not a top-four result.