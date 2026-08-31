# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** C2 — Cotangent Rigidity and Tangent Representations  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `adfe8dcce427ff47b188f54110b796f1f2872d6806ee8d73daf6300e532b6f10`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

The paper has corrected several previous type errors. The nullspaces are now closed linear spans, infinite-path Radon–Nikodym trivializations are avoided, spectral and resolved projections are at least named separately, and nonlinear contractions are no longer assigned a fictitious linear adjoint.

Two principal theorems remain false or ill-typed. Equality of one scalar pressure does not characterize cohomology modulo constants; a two-symbol full shift gives an immediate counterexample. The Kato equation is asserted on one Banach bundle even though A2's own parameter derivatives lose one strong level. In addition, the final “chain rule” confuses differentiation of the pressure with respect to a source function and differentiation of the state map. The synthesis therefore does not provide a valid cotangent or response theorem.

## Major mathematical objections

### 1. Equal pressure does not imply cohomology modulo constants

The theorem states that two potentials have the same long-time pressure if and only if their difference belongs to

\[
\mathscr N_{\rm pr}
=\mathbb R\mathbf1+\overline{\operatorname{span}}
\{U-U\circ\Theta_t\}.
\]

This is false even for the full two-symbol shift. Let \(F=0\) and let \(G\) depend only on the current symbol, with

\[
G(0)=\log(3/2),
\qquad
G(1)=\log(1/2).
\]

Then

\[
P(G)=\log(e^{G(0)}+e^{G(1)})=\log2=P(F).
\]

But \(G\) is not cohomologous to a constant: its sums on the two fixed points are \(n\log(3/2)\) and \(n\log(1/2)\), which cannot differ from one common constant slope by bounded coboundary endpoints.

Equality of a single pressure value is an accidental scalar relation. Cohomology can be characterized by equality of all invariant integrals, periodic-orbit sums, or equality of the entire pressure functional under every perturbation—not by one pressure number.

### 2. The invariant-separator argument proves a different statement

The Hahn–Banach/Cesàro argument, when its tightness hypotheses hold, may identify the annihilator of all invariant measures with the closure of coboundaries. It does not imply the false pressure equivalence above. The variational principle gives

\[
P(F)=\sup_\nu\{h(\nu)+\nu(F)\},
\]

and two different functions can have the same supremum while having different integrals under most invariant measures.

Thus the proof makes an invalid jump from an invariant-integral quotient to a scalar-pressure quotient.

### 3. The Cesàro tightness lemma is not valid for every signed measure as stated

The bound is claimed for every weighted finite signed measure \(\mu\). A Foster–Lyapunov estimate for a physical Markov kernel controls expectations under measures evolved by that kernel, subject to its domain and moment assumptions. It does not automatically control arbitrary signed measures on a deterministic path space, especially when the weight contains shifted contact counts or return data.

The hard-sphere input is only a short-time exponential moment under the prepared physical law, not a uniform drift inequality for all signed measures and all \(T\ge1\). The compact Sinai argument likewise requires an explicitly defined path weight and shift estimate. The theorem's dual identification therefore lacks its noncompact tightness hypothesis.

### 4. The Kato ODE is ill-typed on the regularity-losing scale

A2 explicitly states that each material parameter derivative loses one strong Banach level. Accordingly, the Riesz-projector derivative has the form

\[
\Pi_\eta':\mathbb B^{m+1}\longrightarrow\mathbb B^m,
\]

not a bounded operator on one fixed \(\mathbb B^m\). The commutator

\[
[\Pi_\eta',\Pi_\eta]
\]

therefore also loses regularity. Picard iteration of

\[
U_\eta'=[\Pi_\eta',\Pi_\eta]U_\eta
\]

loses one level at every iterate and cannot produce a bounded invertible evolution on a fixed Banach space.

The phrase “common Banach bundle” does not solve the loss. One needs fixed-space differentiability, a tame smoothing connection, or a scale-valued evolution theorem with an explicit radius/regularity budget.

### 5. The resolved Hilbert bundle is assumed rather than constructed

The Kato transport is built from the Ruelle spectral projector on an anisotropic transfer space. The memory projection \(P_\eta\) then lives in a “common Hilbert realization” of the A4 Doob phase. No map relates these two spaces, proves that \(U_\eta\) acts on the Hilbert realization, or shows that conjugating \(P_0\) by this transport gives the intended physical resolved observables.

A4 itself has not constructed the claimed Hilbert generator or resolvent strip. Consequently the covariant memory theorem has no common operator domain.

### 6. The nonlinear pressure chain rule is ill-typed

The identity

\[
Q_{\mathcal C}(\varphi)=Q(\varphi\circ\mathcal C)
\]

is correct. If the source \(\varphi\) is varied by a test function \(h:Y\to\mathbb R\), the derivative is

\[
DQ_{\mathcal C}(\varphi)[h]
=DQ(\varphi\circ\mathcal C)[h\circ\mathcal C].
\]

The manuscript instead writes an expression involving

\[
D\varphi(\mathcal Cx_*)D\mathcal C(x_*)h,
\]

where \(h\) is now treated as a tangent vector in \(X\). This differentiates the composite observable with respect to the state \(x\), not the pressure functional with respect to its source \(\varphi\). The two derivatives are different mathematical objects.

The stated Hessian conclusion consequently mixes source response, state sensitivity, and contraction geometry without a declared parameter.

### 7. Optional-projection convergence inherits the false A4 martingale interface

The proof uses A4's conditional future kernels and enhanced tangent. A4's Poisson decomposition is algebraically wrong, and its quenched kernel convergence has not been proved. Uniform integrability of finite likelihoods does not by itself identify stable convergence of their optional projections when filtrations and state spaces vary.

### 8. The paper has no independent top-four theorem after correction

The valid ingredients—closed coboundary spans, Kato response on a fixed space, the contraction principle, and finite-time likelihood differentiation—are general structures. The model-specific hypotheses needed to instantiate them remain in A2–A4 and B2–B4. C2 currently repackages those desired interfaces rather than proving a new one.

## Dependency and editorial assessment

C2 is downstream of both the Sinai and hard-sphere chains. It cannot close their missing spectral, LDP, memory, or Gaussian theorems. D1 must not cite C2's quotient, Kato, or optional-projection statements as certified inputs.

A credible revision should separate: (i) the invariant-integral quotient; (ii) equality of full pressure functionals; (iii) fixed-space spectral response; and (iv) source versus state derivatives under contraction. Those are distinct theorems.

## Recommendation

**Reject.** The scalar-pressure rigidity theorem is false by an elementary full-shift counterexample, and the Kato and contraction formulas remain ill-typed. The manuscript is a synthesis of conditional structures, not a completed top-journal result.
