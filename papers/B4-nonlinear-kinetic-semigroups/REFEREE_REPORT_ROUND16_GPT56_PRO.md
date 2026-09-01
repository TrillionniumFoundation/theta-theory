# Independent Referee Report — Round Sixteen

**Paper:** `B4 — Nonlinear Kinetic Semigroups`  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Submitted revision branch:** `revision/round16-referee-positive-closure-11paper-2026-09-01`  
**Locked submitted commit:** `2901535c56013bb61ca4211d7b7bb2b35007fff0`  
**Paper directory:** `papers/B4-nonlinear-kinetic-semigroups`  
**Recovered Round-Sixteen candidate module:** `revision/round16-referee-final/B4_STATE_DEPENDENT_NISIO_RESOLVENT.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, *Journal of the AMS*  
**Recommendation:** **Reject**

## Scope and source-integrity ruling

The submitted branch does not contain a materialized Round-Sixteen manuscript. Its visible `main.tex` remains the Round-Fourteen paper and still loads `ROUND14_POSITIVE_CLOSURE.tex`. The only Round-Sixteen additions are six base64/XZ payload fragments. Streaming recovery produced the complete candidate module named above, but the archive ends inside `tools/materialize_round16_referee.py`; no complete materializer, Round-Sixteen `main.tex`, author response, build record, or final certificate is present in the submitted tree.

I therefore separate two questions. The **formal journal submission** is the actual visible Round-Fourteen manuscript and is not cured merely by an unmaterialized payload. The **supplemental mathematical review** below audits the complete recovered Round-Sixteen candidate module byte-for-byte. No unavailable file is inferred from workflow labels or author claims.

## Summary of the candidate

The candidate abandons the previous comparison argument that reused one state-dependent balanced control from two different initial densities. It instead defines a discounted control resolvent
\[
R_\lambda h(f)
 =\sup\int_0^\infty e^{-\lambda t}
   \bigl[\lambda h(f_t)-\dot{\mathcal A}(f,\Gamma)_t\bigr]\,dt,
\]
claims that it maps the weighted energy state space into `BUC`, derives the nonlinear resolvent identity, defines an \(m\)-dissipative graph from \(R_\lambda\), proves equality with a smooth cylinder core, and then invokes nonlinear Trotter–Kato convergence from BBGKY correctors.

This is a more appropriate architecture than the old “common control” proof. The decisive continuity, core, and graph-convergence theorems are nevertheless missing.

## Major objections

### 1. The `BUC` continuity proof still reuses an inadmissible source

To compare trajectories from \(f\) and \(g\), the candidate says to use the same bounded collision source and apply a Gronwall estimate. An admissible hard-sphere control is not a free additive vector field. It is a nonnegative contact current, usually written relative to the state-dependent intensity \(A_f\), and it must satisfy the balance equation.

A source admissible from \(f\) need not be absolutely continuous with respect to \(A_g\), need not have finite entropy relative to \(A_g\), and may drive the second trajectory outside the positive density cone. This is especially clear when \(f\) or \(g\) vanishes on a collision sector. The candidate proves continuity only by assuming away the state dependence that caused the preceding defect.

On a compact class with densities uniformly bounded above and below one might construct a transfer of controls, but no such theorem is stated, and the resolvent is claimed on the whole energy-moment state space.

### 2. Compactness of action sublevels is not established in the claimed state space

The proof says that entropy bounds control contact mass and hence give compact controlled trajectories. It does not prove existence, closure, or compactness for weak solutions of the controlled Boltzmann/hard-sphere balance equation with state-dependent collision measures.

The action sublevel must be closed under simultaneous convergence of \(f_n\), \(A_{f_n}\), and \(\Gamma_n\). Lower semicontinuity of
\[
\mathrm{Ent}(\Gamma_n\mid A_{f_n})
\]
with both numerator and reference moving is not automatic, particularly near vacuum. Nor is the nonlinear collision map continuous in the weak moment topology without uniform integrability estimates. These are prerequisites for attainment and the dynamic programming principle.

### 3. The resolvent identity does not prove the smooth core equality

Even if the abstract discounted resolvent were well-defined and satisfied its identity, the crucial claim
\[
\overline{\mathcal H_{\rm cyl}}=\mathcal H
\]
in the uniform graph norm is unsupported. The proposed proof takes Yosida approximants, smooths them in finitely many coordinates, truncates velocities, and then invokes B2's entropic projection to restore balance.

This paragraph contains several theorem-sized gaps:

* Yosida approximants are merely bounded uniformly continuous functions; finite-coordinate smoothing does not approximate their generator values uniformly on an infinite-dimensional state space.
* velocity truncation changes the collision operator and the action;
* restoring balance by a positive entropic projection is exactly the invalid B2 range claim;
* no commutator estimate controls the graph error;
* no diagonal sequence is shown to work simultaneously for the function and generator components.

The equality of the full graph with the cylinder core is the essential comparison theorem. It cannot be declared by an approximation slogan.

### 4. The corrector estimate does not yield the asserted hierarchy tail

The connected \(j\)-particle defect is bounded schematically by
\[
j!\,C^j T^{j-1}.
\]
The factorial hierarchy norm cancels \(j!\), leaving exponential growth \(C^j\). A geometric tail \(C\rho^K\) requires a weight radius strictly smaller than \(1/C\), uniformly over time, controls, cutoffs, and the state class. The candidate does not specify or prove such a uniform radius.

Similarly, genealogywise estimates with constants \(C_K\) and exponents \(\alpha_K\) allow a slowly growing diagonal only for pointwise errors. Nonlinear Trotter–Kato convergence requires graph errors uniform on the compact-containment sets used by the semigroup. That uniformity is not established.

### 5. The nonlinear Trotter–Kato hypotheses are not checked

The manuscript presents one family of formal upper/lower correctors and concludes convergence of microscopic nonlinear semigroups. It does not prove:

* liminf graph convergence for arbitrary convergent approximating sequences;
* range stability of the microscopic resolvents;
* exponential compact containment;
* consistency of the ensemble-boundary jump term under the same diagonal;
* uniqueness/comparison for the limiting Hamilton–Jacobi equation independently of the core claim.

A one-sequence consistency calculation is not a nonlinear Trotter–Kato theorem.

### 6. Law–hierarchy determinacy does not prove realizability under the flow

Exponential number moments may make factorial correlations determine a law. The candidate further claims that the BBGKY image is closed and every limiting hierarchy remains realizable. This requires positivity, consistency, and tightness of all marginals under collision boundary traces. Termwise differentiation of a formal generating functional does not prove those properties.

### 7. Upstream inputs remain unavailable

The action and contact-source compactness use B2's unproved positive recovery; the Gaussian tangent and graph approximation use B3's unproved Mosco theorem; microcanonical variants use B1's invalid coefficient theorem. The candidate cannot use these as closed inputs.

## Genuine progress

The shift to a discounted resolvent and an \(m\)-dissipative graph is conceptually better than the prior common-control argument. The initial state is now present in the value function, and the ensemble-boundary exponential term is more clearly typed. These improvements should be retained.

They do not supply the missing state-dependent admissible-control continuity or smooth-core theorem.

## Minimum requirements for a new submission

A new version must prove:

1. a state-dependent control-transfer/stability theorem preserving positivity, balance, and entropy;
2. compactness and lower semicontinuity of controlled action sublevels with moving \(A_f\);
3. the nonlinear resolvent identity on a precisely defined complete state space;
4. graph-norm density of a concrete core with quantitative commutator bounds;
5. uniform factorial-radius and recollision estimates for one diagonal corrector family;
6. every hypothesis of the chosen nonlinear Trotter–Kato theorem;
7. law–hierarchy realizability, not only algebraic determinacy.

## Verdict

**Reject.** The abstract resolvent architecture is improved, but the candidate's comparison theorem is hidden in unproved `BUC` continuity and core-density claims. The microscopic-to-nonlinear semigroup convergence is not established.
