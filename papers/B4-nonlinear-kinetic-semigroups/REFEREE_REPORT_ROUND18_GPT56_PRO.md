# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** B4 — *Microcanonical Excess-Pressure Semigroups and Kinetic Theta-Generators*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`B4_CONTROL_TRANSFER_TROTTER_KATO.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The Nisio resolvent, m-dissipativity, graph-core corrector, and nonlinear semigroup limit are not proved.

## 1. Overall assessment

The revision improves the type discipline of the project. It distinguishes deterministic flow, Koopman observables, probability laws, factorial hierarchies, and limiting value functions. It also correctly notes that transferring a state-dependent control should preserve the relative multiplier `q`, not reuse one fixed collision measure for two different density paths.

The paper's central nonlinear-semigroup argument nevertheless contains a decisive algebraic error: it applies the linear pseudo-resolvent identity to a nonlinear supremum resolvent. The subsequent proof of a parameter-independent graph, full range, m-dissipativity, comparison, and uniqueness collapses. The control-transfer lemma, compactness, hierarchy corrector, and nonlinear Trotter–Kato verification contain additional major gaps and depend on the unproved B1–B3 results.

## 2. Decisive mathematical objections

### 2.1. [MAJOR] The exact law–hierarchy realization is not proved at the stated level of generality

Theorem `thm:r17-b4-intertwiner` claims that Lenard positivity, consistency, and an exponential bound characterize the image of all finite-volume hard-sphere laws under the factorial-correlation transform. A reconstruction theorem requires precise configuration space, exclusion constraint, local finiteness, normalization, boundary conditions, and a moment-determinacy hypothesis. The proof's appeal to an entire Janossy generating functional is only a sketch.

The BBGKY evolution at hard-sphere boundaries is not obtained merely by integrating the Liouville equation against factorial observables. One must specify boundary traces, collision terms, domains, and the topology in which the infinite hierarchy is solved. The claimed bounded evolution `\mathscr U_t^\varepsilon` on the weighted norm and invariance of the realizable cone are not established.

This theorem might be recoverable in a carefully finite-volume setting, but in its present form it cannot serve as a graph-core or convergence input.

### 2.2. [FATAL] The state-dependent control-transfer lemma does not construct a positive admissible path

Lemma `lem:r17-b4-transfer` starts with a regular controlled path `\Gamma=qA_f` and a nearby initial density `g_s`. If `g` is defined as the solution of the biased Boltzmann equation with intensity `qA_g`, then `(g,qA_g)` is already balanced; no residual correction is needed. The proof instead claims an `O(d_*)` residual in finitely many “mass, momentum, energy, and balance coordinates” and applies the B3 right inverse.

Balance is an infinite-dimensional weak PDE constraint, not a finite list of coordinates. It is unclear what residual remains or what equation the correction `R(f,g)` solves. Moreover:

1. B3's bounded right inverse is unproved and has the wrong coercive basis;
2. an `L^1_w`-small signed correction need not be absolutely continuous with respect to `A_g`;
3. adding a Maxwellian collision background controls a negative part only if there is a pointwise domination estimate, not from total variation smallness;
4. a positive Maxwellian background changes the balance and the action and must itself be compensated;
5. local Lipschitz continuity of the perspective entropy requires ratios bounded away from zero and infinity, which the construction does not provide.

Thus the lemma neither defines nor proves the admissible comparison path required for continuity in the initial state.

### 2.3. [FATAL] Compactness of dynamic action sublevels is not established

Lemma `lem:r17-b4-compact` claims compactness for all balanced paths with bounded action, starting from a compact initial family with bounded mass and energy. The state space `\mathcal E`, weighted bounded-Lipschitz metric `d_*`, and contact topology are not defined.

The entropy inequality controls integrals of bounded test functions against `qA_f` only when the exponential moment of the test under `A_f` is uniformly controlled. Mass and energy alone do not give the fixed exponential velocity moment invoked in the proof. Conservation of energy yields tightness at the second-moment level, but not the stronger weighted topology used elsewhere.

The weak balance equation gives bounded variation of each smooth test coordinate under suitable transport/contact moment estimates; it does not automatically give a common modulus of continuity. Contact measures can concentrate in time, so density paths may be only càdlàg in weak topologies. Arzelà–Ascoli on countably many coordinates requires uniform equicontinuity and a compact separating embedding, neither of which is shown.

Finally, lower semicontinuity of

\[
(f,\Gamma)\mapsto\int \ell(d\Gamma/dA_f)dA_f
\]

is not an immediate perspective theorem because `A_f` depends quadratically on `f`. Weak convergence of `f_n` does not generally imply convergence of `f_nf_{n,*}` without additional compactness/strong convergence.

### 2.4. [FATAL] Strong continuity on global `BUC(\mathcal E)` is not proved

Theorem `thm:r17-b4-nisio` claims a strongly continuous contraction semigroup on weighted uniformly continuous functions. Pointwise availability of a zero-cost Boltzmann path and a short-time weak balance estimate may show

\[
S_th(f)\to h(f)
\]

for each fixed regular `f`. Strong continuity in the sup norm requires convergence **uniform over the whole noncompact state space**. Such uniformity is generally false on `BUC` without a globally uniform small-time displacement bound or a restricted weighted norm/state class. No such estimate is stated.

Attainment of the supremum also does not follow merely from compact action sublevels; one must control the terminal reward, establish upper semicontinuity of the objective, and ensure that nearly optimal controls lie in one common compact sublevel.

### 2.5. [FATAL, direct algebraic error] The displayed nonlinear resolvent identity is the linear pseudo-resolvent identity

The manuscript writes

\[
R_\lambda-R_\mu=(\mu-\lambda)R_\lambda R_\mu
\]

“in the nonlinear resolvent sense.” This formula is meaningful for linear pseudo-resolvents, where subtraction, scalar multiplication, and operator composition interact linearly. Here `R_\lambda` is defined by a supremum over controlled paths and is a nonlinear map. The displayed equality is not the nonlinear resolvent identity for an m-accretive graph.

For a standard nonlinear resolvent `J_lambda=(I+\lambda A)^{-1}`, the resolvent relation instead has the implicit form

\[
J_\lambda x
=J_\mu\!\left(\frac{\mu}{\lambda}x+\left(1-rac{\mu}{\lambda}\right)J_\lambda x\right),
\]

with the precise parameter convention adjusted if the discount is indexed reciprocally. The submitted proof does not derive any such identity from the discounted dynamic programming principle.

This is fatal for `thm:r17-b4-comparison`: the alleged independence of the graph from `\lambda`, the range condition, dissipativity, and application of Crandall–Liggett are all deduced from the incorrect formula. Defining

\[
(u,g)\in\mathcal H\quad\Longleftrightarrow\quad
u=R_\lambda(u+\lambda^{-1}g)
\]

also contains an apparent variable error (`u` versus `nu`) in the active source; even correcting the typo, independence of `\lambda` is exactly what remains unproved.

### 2.6. [FATAL] The discounted variational operator has not been shown to be a resolvent of the claimed generator

Splitting an infinite-horizon discounted payoff at time `s` yields a Bellman identity. To convert this into a nonlinear resolvent equation, one must define the infinitesimal graph, prove the correct resolvent relation, establish contraction with the correct normalization, and verify the range condition. The proof says that integrating the DPP “gives the nonlinear resolvent identity,” but no calculation is written.

The cost is represented in the definition as `\ell(d\Gamma/dA_f)A_f(dt)`, which mixes a density and a measure notation without specifying the spatial/velocity integrations. Finiteness, measurability, and discount-tail control are not proved. Thus even before the algebraic error, `R_\lambda` has not been constructed as a globally defined map on the announced function space.

### 2.7. [FATAL] The hierarchy corrector is only an outline and uses incompatible genealogy estimates

Theorem `thm:r17-b4-corrector` claims one exact observable `F_\varepsilon` in the Liouville graph domain for every limiting cylinder, with locally uniform generator convergence. Its proof says that the `j`th connected defect is bounded by `j!C^jT^{j-1}`, while the hierarchy weight `1/j!` leaves a geometric tail.

This argument omits several decisive points:

1. the remaining factor is `(Ce^\alpha)^j`; geometric decay requires an explicit smallness inequality, not just the word “tail”;
2. B2's own convergence proof mishandles this factorial bound, so the cited estimate is not established;
3. the recollision error is written as `C_K\varepsilon^\gamma` with one genealogy-uniform exponent `\gamma`, whereas B2 explicitly avoids assuming a genealogy-uniform Łojasiewicz exponent;
4. choosing `K(\varepsilon)` requires a quantitative growth bound on `C_K`, absent here;
5. solving a finite terminal corrector equation does not show that the resulting observable satisfies exact specular boundary compatibility;
6. “resolvent regularization” of the Liouville generator can alter boundary traces and must be proved to preserve the collision jump;
7. a formal exponential boundary factor does not establish locally uniform convergence on action sublevels.

The theorem is the main microscopic-to-kinetic bridge and receives no actual construction.

### 2.8. [FATAL] The nonlinear Trotter–Kato hypotheses are listed, not verified

The proof of `thm:r17-b4-limit` says that B2 gives compact containment, the corrector gives both generator inequalities, compact action sublevels give equicoercivity, and comparison identifies half-relaxed limits. Every one of these inputs is missing or invalid:

- B2's dynamic LDP/compact containment is unproved;
- one approximate equality for a proposed corrector does not automatically furnish both upper and lower extended-generator inclusions;
- comparison depends on the incorrect resolvent theorem;
- the topology and compact sets for local uniform convergence are not fixed;
- initial-condition convergence and exponential tightness of values are absent.

Exact law–hierarchy realizability, even if true, only says the finite objects correspond to probability laws. It does not imply convergence of their nonlinear semigroups.

## 3. Dependency consequences

B4 depends on B2's dynamic action, B1's microcanonical transfer, and B3's right inverse; all three inputs fail independent review. B4 also fails internally at the nonlinear resolvent identity. Its Nisio semigroup and kinetic generator therefore cannot be used in C1, C2, or D1.

## 4. Minimum requirements for reconsideration

A future submission would need:

1. a precise state space and dynamic action with a genuine compactness/lower-semicontinuity theorem;
2. a correct state-dependent stability/control-transfer theorem preserving positivity and balance;
3. a semigroup on a function space where strong continuity is actually true;
4. derivation of the correct nonlinear resolvent identity and the associated m-accretive graph/range theorem;
5. an explicit finite-particle graph-domain corrector with quantitative `K`–`\varepsilon` estimates and boundary compatibility;
6. a complete nonlinear semigroup convergence theorem verifying each extended-generator and compact-containment hypothesis.

## 5. Recommendation

**Reject.** The paper's type distinctions are valuable, but the central resolvent calculation is wrong for a nonlinear operator. The comparison and m-dissipativity theorem therefore collapses, and the microscopic corrector/Trotter–Kato argument remains a program rather than a proof.