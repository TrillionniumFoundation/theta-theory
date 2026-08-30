# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A3 — *Full Liouville Empirical-Path Large Deviations and Information Projections for Finite-Horizon Sinai Billiards*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `9b0d466b25fcf1cfdee29a35062d337a4c16e3d2`

## Overall assessment

This revision correctly recognizes the “one big excursion” obstruction which invalidated the preceding induced-Palm argument. It replaces superexponential return truncation by a proposed direct collision pressure with an induced branch and a survivor/escape branch. That is the right conceptual direction.

The new direct-pressure theorem and the full LDP lower bound are not proved. The survivor systems are not shown to be finite Markov systems, strict dominance of a survivor pressure does not imply a unique analytic equilibrium state, and the rate-density lemma relies on an impossible periodic-orbit approximation of positive-entropy laws. The resulting full collision and physical empirical-path LDPs therefore remain unestablished.

## Major objections

### 1. The finite survivor truncations are not shown to be finite hyperbolic Markov systems

For fixed singularity depth `m` and homogeneity cutoff `K`, the manuscript deletes components hitting the magnet and calls the remaining dynamics “a finite union of uniformly hyperbolic Markov components.” This does not follow from the construction.

A finite cut of the singularity set does not determine the full future itinerary of an arbitrarily long survivor orbit. New preimages of singularities appear at all later depths. To obtain a finite-state survivor system one needs a genuine Markov partition for the open billiard, or a finite subshift whose cylinders have exact forward invariance. Neither is constructed.

Consequently the operator `E_{R,F}^{m,K}(n)`, its state space, its semigroup/cocycle property, and its Perron root are not rigorously defined. The claimed monotone convergence of finite survivor pressures therefore has no established foundation.

### 2. The renewal identity is asserted without controlling its operator domains

The formula

\[
\mathscr G_F(z)=
\mathscr E_F^{\rm in}(z)
(I-\mathscr R_{R,F}(z))^{-1}
\mathscr E_F^{\rm out}(z)+\mathscr G_{F,\infty}(z)
\]

is plausible at the scalar combinatorial level, but the manuscript does not specify common Banach spaces for all four terms, convergence half-planes, boundary operators, or how paths with tangencies and graph-completed singular limits are assigned. The statement that entrance/exit series are analytic “to the left of both candidate abscissae” is especially unsupported; an exponential return tail gives only a finite strip whose location depends on the source.

Without this analytic renewal theorem, equality of the direct pressure with the maximum of two abscissae is not proved.

### 3. A strict survivor winner need not have a unique or analytic equilibrium phase

The survivor set may have several topologically transitive components with the same pressure. Strict inequality

\[
q_{\infty,R}(F)>q_{Y,R}(F)
\]

only separates survivor behavior from returning behavior. It does not select a unique component inside the survivor set. Nor does monotone convergence of finite truncation Perron roots imply convergence of projectors, a spectral gap, or analytic dependence of the limiting survivor pressure.

Thus the claims that a strict survivor winner is analytic and has a unique equilibrium law are false without additional irreducibility and spectral assumptions.

### 4. The rate-dense exposed-phase lemma contains a direct entropy error

For a zero-magnet-frequency invariant law, the proof says:

> approximate it by periodic orbit measures in the finite-depth survivor sets, with convergence of entropy plus potential cost.

Every periodic orbit measure has metric entropy zero. A positive-entropy survivor law cannot be approximated by periodic measures with convergence of entropy unless its entropy is zero. Weak density of periodic measures, where available, does not imply entropy-density or convergence of the pressure-dual cost.

Long convex concatenations do not repair this problem: concatenating periodic words may approximate a measure weakly, but it does not automatically reproduce its entropy/free-energy cost, and the resulting measure need not be the unique equilibrium state of a vanishing perturbation.

This invalidates the rate-preserving exposed approximation which is the only argument extending the lower bound from unique equilibrium phases to all finite-rate laws.

### 5. The full LDP lower bound is therefore missing

The proof of the full collision empirical-path LDP has the form:

1. pressure gives the upper bound;
2. a Perron change of law gives the lower bound at unique exposed phases;
3. the invalid rate-density lemma gives all other lower bounds.

Step 3 fails. A convex dual of a pressure limit is a candidate rate; it does not by itself supply a full LDP lower bound at nonexposed points. This is a central, not technical, gap.

### 6. The large singular-source Chernoff estimate is unproved

The manuscript claims

\[
Q_R^c(sb_{q,\delta})-Q_R^c(0)
\le C(e^s-1)e^{\kappa q}\delta^\alpha
\]

and then sends `s` to infinity as the neighborhood shrinks. Such an estimate requires pressure control for arbitrarily large positive bounded sources supported near singularities, uniformly across both induced and survivor branches. It does not follow from a small spectral perturbation theorem or from a one-step mass estimate.

In particular, a large positive source can select rare orbits which repeatedly shadow singularity neighborhoods. The required uniform nonlinear pressure estimate is not proved.

### 7. The physical-time contraction assumes continuity not established on the stated graph completion

Finite horizon makes the roof bounded, but it may still be discontinuous across collision singularities. The manuscript invokes the graph-completed factor theorem, whose proof itself relies on the unproved large-source estimate. The claimed continuous Palm map and goodness of its image are therefore not yet available.

### 8. The information-projection theorem omits conditioning regularity hypotheses

Finite-rate feasibility and goodness give attainment. Exponential conditional concentration for shrinking neighborhoods additionally requires that the conditioning sets have the correct LDP lower exponent—typically a continuity-set or exposedness hypothesis for the constraint value. “Unique exposed minimizer” does not by itself guarantee every arbitrarily chosen shrinking sequence has a denominator of the asserted exponential order.

The nonunique statement that every limit is a probability mixture supported on the minimizer set also requires tightness of the rooted conditional laws and an explicit disintegration argument.

### 9. The cotangent quotient is not consistently typed in the final theorem

The revision defines the weighted-strict quotient

\[
C_W/\mathscr N_W,
\]

but the final closure theorem says cotangents live in

\[
\mathscr A_\beta/\mathscr N_\beta.
\]

These are different spaces and topologies. The claimed Radon-dual annihilator theorem is proved, if at all, for the former. The conclusion silently switches back to the former notation from an earlier draft.

The Hahn--Banach/Jordan argument also needs care: an arbitrary signed invariant separator with total mass zero does not automatically yield two invariant probability measures of finite `W`-moment with equal total masses without a normalization argument.

## Revision status of prior objection

The paper has genuinely closed one previous objection: it no longer discards a macroscopic return block at superexponential cost. However, the replacement survivor-pressure route has not been completed, and the active lower-bound proof now contains a direct entropy contradiction.

## Minimum viable reconstruction

A serious paper would need to choose one of two routes:

1. construct a direct collision-time transfer/pressure theory on the full graph-completed path space, including survivor components and a complete level-2/3 theorem; or
2. prove a precise inducing theorem with a recession measure that records macroscopic excursions and establish a full lower-bound approximation theorem.

In either case the authors must prove entropy-density of the chosen exposed phases rather than invoke periodic measures, and must separate uniqueness inside the survivor sector from dominance over the induced sector.

## Recommendation

**Reject.** The revision discovers the correct one-big-excursion issue but does not solve it. The claimed full empirical-path LDP relies on an invalid rate-density lemma and unproved survivor spectral theory.