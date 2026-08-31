# Independent Referee Report — Round 12

**Manuscript:** A1 — *Exact Benchmarks*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `0a0dd68bdea96bf38669ba6b8b1a1f427fc082563542c69f4e16201bb0d0069e`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 correctly abandons the false product of two independent one-sided shifts, refines source cells by target labels, introduces higher-codimension flag currents, and keeps the mechanical valuation coefficient conditional on a likelihood-compatibility axiom. Those are genuine improvements.

The new geometric centerpiece is nevertheless false as stated. Refining a full baker map simultaneously in every forward and backward symbolic coordinate does not produce a compact lamination with two-dimensional symplectic leaves. The bi-cylinders shrink in both physical directions. The resulting split inverse limit is the zero-dimensional symbolic natural extension, up to duplicated seam germs. Consequently there is no nondegenerate leafwise two-form on the claimed section and no four-dimensional-leaf Hamiltonian suspension built from it. The response theorem then rests on an incorrectly typed geometric object.

## Decisive objections

### 1. The inverse limit has zero-dimensional local structure, not two-dimensional leaves

Let

\[
p_*:=\max_i p_i(a)<1
\]

on the compact parameter interval. A bi-cylinder

\[
C_{i_{-m},\ldots,i_n}
\]

has horizontal diameter bounded by a product of the future branch widths and vertical diameter bounded by a product of the past branch widths. Hence

\[
\operatorname{diam}_q C_{i_{-m},\ldots,i_n}
\le p_*^{\,n+1},
\qquad
\operatorname{diam}_p C_{i_{-m},\ldots,i_n}
\le p_*^{\,m}.
\]

Both diameters tend to zero as \(m,n\to\infty\). The completed finite cells are components of the split finite-stage space, so their inverse images are clopen cylinder neighborhoods. These clopen neighborhoods form an arbitrarily fine basis. The regular inverse-limit point is therefore determined by one two-sided itinerary and has zero-dimensional local symbolic topology.

This is the usual natural extension of the full baker map, not a two-dimensional symplectic leaf with a Cantor transversal. A solenoidal lamination arises from inverse limits of genuine covering maps whose fibers retain positive-dimensional local directions; successive two-sided Markov refinements with shrinking physical diameters do not have that property.

Thus the assertions

\[
\mathscr S_a^\infty
\text{ has two-dimensional symplectic leaves}
\]

and

\[
\mathcal M_a
\text{ has four-dimensional Hamiltonian leaves}
\]

are incompatible with the actual inverse-limit geometry.

### 2. The finite-stage symplectic forms do not rescue the limit

At every finite depth, each cell is a rectangle and carries \(dq\wedge dp\). That does not imply that these forms define a nondegenerate two-form on a limiting leaf. Along a compatible bi-cylinder sequence the tangent widths collapse in both directions. A compatible family of forms on shrinking rectangles is not a tangent bundle on the inverse limit.

The manuscript therefore cannot pass from “every finite restriction is symplectic” to “the inverse limit is leafwise symplectic” without constructing a separate leaf equivalence relation and proving that its leaves are manifolds. No such relation is defined.

### 3. The collar-extension lemma does not prove refinement functoriality

The proof invokes a Whitney extension, a Hamiltonian correction, and a relative Moser equation, then claims that “uniqueness” makes the construction functorial under every refinement. Neither the Whitney extension nor the Hamiltonian isotopy is canonical, and the Moser vector field is not unique without a fully specified gauge and compatible global boundary data.

Compatibility is the load-bearing point: an arbitrary choice on a coarse rectangle need not restrict to the independently constructed choices on all finer rectangles. Without a genuinely functorial construction, the mapping-torus data do not define a consistent inverse-limit flow even before the dimensional objection above is considered.

### 4. The graded-current norm is not yet a defined refinement norm

The expression

\[
\sum_C \rho^{|C|}
\sum_k\kappa^k
\sum_{F\in\mathfrak F_k(C)}\|U_{C,F}\|_{C^{r-k}}
\]

uses \(|C|\) without defining whether it is past depth, future depth, total word length, or refinement generation. The direct-limit quotient also contains many presentations of the same physical current. The inequalities \(4\rho<1\) and \(M\kappa<1\) count descendants and flags only after a precise multiplicity theorem, which is not supplied.

In particular, boundedness of push-forward under \(\widehat B_a\) requires tracking how past and future depths change separately. A single total-depth weight is not automatically invariant under the coupled shift.

### 5. Closure of the exponential tilt inside the declared family is assumed

The work theorem states that tilting by \(\theta A_n\) changes the branch weights to “the member \(a=\Lambda'(\theta)\) of the same family.” For a general one-parameter family \(p_i(a)\), the exponential tilt

\[
\widetilde p_i(\theta)
\propto p_i(a_0)e^{\theta c_i}
\]

traces a specific exponential-family curve in the probability simplex. It lies in the originally declared curve \(a\mapsto p(a)\) only under an additional closure/calibration hypothesis. The theorem does not state that hypothesis.

### 6. The corrected mathematical core remains a benchmark, not a top-four theorem

If the inverse-limit symplectic claims are removed, the surviving content is an explicit Bernoulli baker coding, one-sided Poisson/resolvent calculations, Hadamard differentiation of moving rectangular partitions, and an additive work cocycle. These are useful regression tests, but the manuscript does not establish the depth or novelty expected by the four journals named above.

## Dependency and scope assessment

A1 is largely independent of the remaining series, but it must not be cited as a completed Hamiltonian realization of the symbolic natural extension. It can support symbolic benchmark identities only after the geometric claims are removed or replaced by a correctly constructed finite-dimensional physical suspension.

## Required reconstruction

A viable revision would have to choose one of two honest routes:

1. keep the ordinary physical square as the symplectic section and treat the two-sided symbolic object purely as a measurable/topological coding; or
2. construct a genuine solenoidal inverse system from covering maps that retain two-dimensional leaves, then prove that the baker dynamics and work cocycle extend to it.

The current successive-refinement inverse limit cannot serve both roles.

## Recommendation

**Reject.** Round 12 repairs the symbolic coupling and several typing defects, but its principal new geometric theorem confuses a zero-dimensional bi-symbolic refinement with a two-dimensional symplectic lamination. The claimed autonomous Hamiltonian solenoid and the response calculus built on it are therefore not established.