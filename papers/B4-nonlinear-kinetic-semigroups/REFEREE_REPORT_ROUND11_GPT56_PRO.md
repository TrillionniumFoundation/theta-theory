# Independent Referee Report — Round Eleven

**Manuscript:** B4 — Nonlinear Kinetic Semigroups  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Reviewed branch:** `revision/round11-referee-positive-closure-11paper-2026-08-31@e81cbf57624d21be23ee9d982a1255c076363761`  
**Reviewed source:** `revision/round11-referee-final/B4_TYPED_MICROSCOPIC_LOG_PENALTY.tex` (Git blob `d2da4fbc81977e8ced924ddfa35398475f36ace9`)

## Executive assessment

The manuscript now distinguishes microscopic states, Koopman observables, pushed-forward laws, ensemble log-Laplace values, and the limiting action semigroup. It also charges preparation only at the initial boundary. These are correct typing repairs.

The new comparison theorem, however, rests on a false elementary implication. Boundedness of the logarithmic penalty does not force the product \(r_arepsilon e^{C_H|p_arepsilon|}\) to vanish. The observable core and infinite hierarchy corrector are also asserted without the required capacity and graph-domain estimates. The limiting semigroup therefore remains unproved.

## Major mathematical objections

### 1. The key logarithmic-penalty estimate is false

Let

\[
a=\kappa C_H\in(0,1),
\qquad
r_arepsilon=\varepsilon^{a/(2(1+a))}.
\]

Then \(r_arepsilon\to0\) and

\[
\Phi_arepsilon(r_arepsilon)
=\kappa\int_0^{r_arepsilon}
\log(1+s/\varepsilon)\,ds
\longrightarrow0.
\]

Thus this sequence is fully compatible with the only coercive conclusion used in the proof. But

\[
r_arepsilon
\left(1+\frac{r_arepsilon}{\varepsilon}\right)^a
\asymp
\varepsilon^{-a/2}
\longrightarrow\infty.
\]

Therefore the claimed implication

\[
r_arepsilon e^{C_H|p_arepsilon|}\to0
\]

does not follow from \(r_arepsilon\to0\) and the maximizing penalty bound. A stronger common modulus of continuity might force \(r_arepsilon=O(\varepsilon)\), but no such estimate is stated or proved.

### 2. The full Hamiltonian comparison remains outside controlled jet balls

The derivative is

\[
|p_arepsilon|
=\kappa\log(1+r_arepsilon/\varepsilon),
\]

which can diverge. Local Hamiltonian continuity on every fixed jet ball gives no control along this sequence. The proof's only proposed compensation is the false estimate above.

### 3. The graph-core theorem is not established by codimension counting

Triple collisions being codimension at least two does not imply that cutoffs around them have vanishing generator graph norm. Capacity for a first-order transport generator depends on the characteristic geometry, not just Lebesgue codimension. Grazing and multiple-collision strata can be reached by characteristics and carry nontrivial trace defects.

Weighted Stone–Weierstrass proves uniform density of functions, not graph-core density for an unbounded reflected transport generator. The range-density assertion for \(\lambda-A_arepsilon\) on the chosen cylinder class is precisely what must be proved.

### 4. The infinite hierarchy corrector lacks a uniform closed-domain theorem

The proof quotes a connected order-\(j\) bound and says that the Boltzmann–Grad coefficient makes the sum converge. It does not state the exact coefficient, the source/target label radii, or a bound uniform in \(arepsilon\) for the generator images. Solving each finite triangular system does not imply that the infinite sum belongs to the closed microscopic generator domain.

### 5. The microscopic “tower” is only a linear flow identity

Composing the terminal Koopman observable before one initial-law integral is correct, but it is not an autonomous nonlinear dynamic programming semigroup on a reduced state. The limiting Lax–Oleinik tower must still be obtained entirely from the B1–B2 LDP and its conditional recovery theorem.

### 6. The action semigroup imports all missing B2 compactness and recovery

Closed balance, compact action sublevels, attainment, smooth tilted recovery, and entropy-coercive source exhaustion are precisely the unproved parts of B2. Repeating them as inputs does not establish B4.

### 7. Entropy truncation is not locally uniform on the proposed jets

Clipping \(q=d\Gamma/dA_f\) and repairing balance can approximate finite-action paths, but the dual Hamiltonian contains \(e^{\Delta p}\). Uniform convergence on a sequence of logarithmically diverging jets needs quantitative exponential integrability and a repair bound depending on \(|p_arepsilon|\). No such estimate is given.

### 8. Generator convergence plus comparison has not been proved

The upper/lower nonlinear generator limits require corrected test functions, exponential compact containment, and stability on the same topology. Each is only cited. Since comparison fails, the half-relaxed-limit conclusion fails independently.

## Status of earlier objections

The state/observable/law typing, the terminal-value corrector sign, and the single initial preparation charge are repaired. The replacement comparison mechanism is mathematically false as written.

## Minimum reconstruction

The authors need a comparison penalty whose coercivity and jet growth are jointly quantified, or a restricted viscosity class with a proved common modulus. They must separately establish the reflected observable graph core and a uniform infinite-hierarchy corrector theorem.

## Recommendation

**Reject.** The central comparison estimate admits an explicit counterexample, so uniqueness and the microscopic semigroup limit do not follow.