# Referee Report

**Manuscript:** A1 — Exact Benchmarks  
**Recommendation:** **Reject**  
**Standard applied:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / JAMS  
**Review target:** the pinned eleven-paper clean-main review tree (archive SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`).

## Overall assessment

The manuscript contains a correct and pleasantly explicit generalized baker-map calculation: the branch process is iid, the scalar current has a binary Cramér rate, fixed-window conditioning is hypergeometric-to-Bernoulli, and exponential tilting changes the branch weights. Those facts make the paper a useful sanity check for notation used elsewhere in the series.

They do not, however, constitute a top-four-journal result. The manuscript repeatedly upgrades an elementary Bernoulli model into claims about “mechanical collision paths,” “first-principles theta selection,” and “all-order response” without proving the additional structures those phrases normally require. The central calculations are standard consequences of product measures. The paper’s main difficulty is therefore not a missing estimate but a mismatch between the mathematical content and the claimed conceptual scope.

## Major objections

### 1. The “collision” and “mechanical winding” language is not mathematically earned

The map is a generalized four-strip baker map. No billiard table, free-flight geometry, specular reflection law, collision normal, physical clock, or Hamiltonian flow is constructed. Labelling the four branch symbols as signed windings does not turn a Bernoulli observable into a mechanical current. The main theorem should be stated as an exact symbolic benchmark, not as a first-principles collision-mechanics theorem.

This is not cosmetic. Later manuscripts use the present paper as evidence that deterministic mechanics selects a risk-sensitive parameter. In A1 the deterministic map is designed so that its branch widths realize a chosen Bernoulli law. That is a realization theorem for a prescribed symbolic law, not a derivation of the law from an independently specified mechanical model.

### 2. The excess-pressure identity is valid only after a missing typing restriction

The finite canonical tilt changes the law of the branch sequence. It therefore identifies expectations under the driven map only for functionals defined on a common symbolic path space, or after an explicit coding/pullback has been fixed.

The manuscript instead allows an arbitrary bounded “terminal mechanical work” \(F\). The maps \(B_{a_0}\) and \(B_a\) have different codings from square coordinates to symbolic paths. If \(F\) depends on physical coordinates rather than only on the common branch sequence, the displayed Radon–Nikodym argument does not prove the claimed identity. The paper must either:

1. restrict \(F\) to the branch sigma-field on a common symbolic path space; or
2. construct the coding isomorphisms and state exactly which pullback of \(F\) is being compared.

Without this, the principal bridge from symbolic tilting to “mechanical work” is ill-typed.

### 3. “Endogenous theta” is an interpretation, not a theorem

The equality
\[
\theta(a)=I'(a)
\]
correctly identifies the Lagrange multiplier conjugate to the conditioned branch current. It does not imply that the same number is the risk-aversion parameter for every unrelated terminal payoff. The manuscript obtains the entropic functional only by inserting that same scalar into a log-moment generating function. This is a modelling calibration.

“Measured in the same units” does not prove uniqueness of this calibration. One could use any valuation parameter for a terminal payoff while retaining the same mechanically prepared current law. The paper may call \(\theta\) the canonical current field; it may not claim that mechanics alone has selected a universal preference/risk parameter.

### 4. The microcanonical equivalence theorem is much narrower than the prose suggests

The result controls a fixed or slowly growing central window of symbols under conditioning on one scalar count. It does not give total-variation equivalence of the full conditioned path law, a process-level Gibbs-conditioning principle, or an equivalence for physical orbit observables. The title and main theorem should not imply any of these stronger statements.

### 5. The response theorem ends with undefined objects

The Sobolev estimates for \(\partial_a^k L_a\) and the contraction on centered functions are elementary and appear correct. The claimed consequences for “reduced-resolvent words,” “bilateral response arrays,” and “finite parameter differences” are not defined as mathematical objects and are not stated with norms, index sets, or convergence modes. A top journal cannot accept a theorem whose advertised final consequences are vocabulary rather than propositions.

### 6. Novelty is insufficient

After the above restrictions are imposed, the paper proves:

- Cramér’s theorem for a binary iid observable;
- a standard sampling-without-replacement coupling bound;
- exponential tilting of a product measure;
- the conditional log-Laplace tower;
- elementary differentiation of affine inverse branches.

This is a coherent worked example, but not a research contribution at the level claimed.

## Required reconstruction before reconsideration elsewhere

A viable paper would be an explicitly labelled benchmark note. It should remove mechanical overstatements, type all observables on one path space, separate the current conjugate field from a valuation parameter, define every response object, and compare the example honestly with standard Bernoulli/baker-map thermodynamic formalism.

## Editorial recommendation

**Reject.** The core benchmark is mostly correct, but the top-journal claim rests on terminology and interpretation rather than new mathematics.
