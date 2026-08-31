# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** A1 — Exact Benchmarks  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `365c92435c9e64ba369e1249727f0e70cc47d3bc931838adea7589c2728c8142`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

Round ten makes several genuine corrections. The physical square is no longer identified with a Cantor symbolic graph; the false bilateral Koopman estimate is removed; the valuation coefficient is explicitly conditional on equality of likelihood cocycles; and the intended suspension is now described as a mapping torus rather than a flow followed by an external reset.

The replacement theorem package is nevertheless not correct. The stated physical–symbolic conjugacy uses an inverse of a one-sided past shift that does not exist, the past update is coupled to the current future symbol, and the alleged Hamiltonian suspension is only a stratified quotient with branch seams rather than a globally defined smooth Hamiltonian system. The cut-current response space is also not constructed with enough precision to support the advertised all-depth formula. After these claims are removed, the remaining Bernoulli calculation is a useful benchmark but not a top-four-journal result.

## Major mathematical objections

### 1. The factor conjugacy is written with a nonexistent independent past inverse shift

The paper defines

\[
\Sigma^+=\mathcal A^{\mathbb N_0},\qquad
\Sigma^-=\mathcal A^{\mathbb N},
\]

and claims

\[
\mathfrak c_a\circ B_a
=(\sigma_+\times\sigma_-^{-1})\circ\mathfrak c_a.
\]

There is no single-valued inverse \(\sigma_-^{-1}\) on a one-sided shift. More importantly, the new past symbol is the branch just used by the future coordinate. If \(x=(x_0,x_1,\ldots)\) and \(y\) is the past sequence, the natural-extension update is

\[
T(x,y)=(\sigma x,\,x_0y),
\]

not a product of two independent maps. The current symbol \(x_0\) couples the two factors. Thus the displayed conjugacy theorem is false as stated, and the subsequent claim that the full physical dynamics is handled by two independent one-sided operators is not a consequence of that theorem.

The Bernoulli product law is invariant under the correctly coupled natural-extension map, so the basic model can be repaired. The manuscript, however, must rewrite the factor map and every response identity that uses the false product dynamics.

### 2. The mapping-torus quotient is not shown to be a smooth symplectic Hamiltonian manifold

The construction glues finitely many channel cylinders by a discontinuous piecewise-affine map and calls the result a “finite branched symplectic manifold with corners.” A branched quotient is not, without an additional atlas and compatibility theorem, a symplectic manifold on which a globally defined Hamiltonian vector field exists and is unique. At a seam or multiple preimage seam there are several incident strata. Saying that the seam has Liouville measure zero does not establish a Hamiltonian flow there, nor does an “oriented branched completion” produce a standard smooth autonomous Hamiltonian system.

What is proved is an almost-everywhere suspension of a piecewise symplectic return map. That is a legitimate measurable construction, but it is strictly weaker than the theorem's “exact autonomous Hamiltonian suspension” language.

### 3. The channel work form does not automatically descend through the gluing

The paper places \(\eta=c_i\,d\tau\) on channel \(i\). At an outgoing face of channel \(i\) glued to an incoming face of a generally different channel \(j\), the coefficients are \(c_i\) and \(c_j\). Unless an explicit transition form or matching condition is supplied, these local forms do not define one continuous global one-form on the quotient. Their segment integrals still define an additive symbolic reward, but that is not the same as a globally defined closed mechanical work form on \(\mathcal M_a\).

### 4. The all-depth current Banach space is underspecified

The norm

\[
\sum_w\theta^{|w|}\sum_{j\le r}\|D_a^jF_w\|_{C^1(R_w)}
\]

depends on a decomposition \(F=(F_w)_w\) over all cylinder rectangles. Such decompositions are highly nonunique under refinement. The statement that internal faces cancel is an algebraic observation for one finite refinement; it does not define the quotient, prove completeness, or show that the material derivative is independent of all infinite refinement presentations.

The symbol \(\theta\) is also used for the one-sided Hölder contraction with only \(0<\theta<1\), whereas absolute summability over four-ary words requires a separate weight below the inverse combinatorial growth. These are different constraints and should not be conflated.

### 5. The response theorem does not follow from the two marginal resolvents

Even after correcting the coupled natural extension, a transported physical observable may depend jointly on future and past coordinates. Parameter differentiation changes the coding map, the product law, and the seam locations simultaneously. Two marginal Poisson resolvents do not by themselves account for mixed future–past cylinder terms or prove that the proposed bulk/current/score decomposition is invariant under the chosen coding convention.

There is also a basic scope issue: Lebesgue measure on the physical square is independent of \(a\). For an actually fixed physical observable \(F\), \(\int F\,dq\,dp\) has zero response. Nontrivial formulas arise only after prescribing a parameter-dependent transport of the observable. That transport must be part of the theorem data, not an informal convention.

### 6. Correcting the defects leaves benchmark mathematics, not a top-four contribution

The valid core is a generalized baker map, its Bernoulli coding, standard one-sided Ruelle contraction, elementary exponential tilting, and a piecewise symplectic suspension. These are useful regression tests for the series but do not meet the depth or novelty threshold of the four journals named above.

## Dependency and editorial assessment

A1 remains independent of the Sinai and hard-sphere chains, and no downstream paper should cite it as a mechanical derivation of a universal risk coefficient. The round-ten conditional calibration statement is appropriately cautious and should be retained.

A credible revision would state the coupled natural-extension map correctly, present the suspension as a measurable/stratified symplectic mapping torus unless a genuine smooth desingularization is built, define the current quotient rigorously, and reduce the response theorem to a precisely specified transported-observable class.

## Recommendation

**Reject.** The revision contains real conceptual improvements, but two headline theorems—the product factor conjugacy and the global Hamiltonian suspension—remain incorrectly stated. The corrected material is a benchmark note rather than a top-four-journal paper.
