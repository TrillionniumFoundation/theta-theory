# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** B4 — *Microcanonical Excess-Pressure Semigroups and Kinetic Theta-Generators*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `1e6c5a870ca1ecf3319c1f1d950a1f0f1564dfb4`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

No revised B4 source exists on the declared Round-Nineteen branch. The active file is the same source previously rejected, including the incorrect nonlinear resolvent identity. No corrected Crandall–Liggett graph construction, compactness theorem, graph-core corrector, or Trotter–Kato proof has been supplied.

## 2. Unresolved fatal defects

### 2.1. The control-transfer lemma still does not construct a positive admissible path

If `g` solves the biased Boltzmann equation with the same relative multiplier `q`, then `(g,qA_g)` is already balanced; the manuscript's claimed finite-dimensional “balance residual” is unexplained. Balance is an infinite-dimensional PDE constraint, not a finite list of mass, momentum, energy, and balance coordinates. The proposed correction uses B3's unavailable right inverse, and `L^1` smallness cannot guarantee absolute continuity or pointwise domination by `A_g`. Adding a Maxwellian collision background changes both balance and action and is not compensated.

### 2.2. Compactness and strong continuity remain unproved

Mass and energy do not yield the fixed exponential velocity moments used in the compactness proof. Weak balance bounds coordinate variation only after quantitative contact and transport estimates; contact measures may concentrate in time. Lower semicontinuity is not a direct perspective theorem because `A_f` depends quadratically on a weakly convergent `f`.

Pointwise short-time continuity along one zero-cost path does not give strong continuity in the global supremum norm on a noncompact state space. A uniform small-time displacement estimate or a restricted weighted function space is necessary and absent.

### 2.3. The nonlinear resolvent identity is still algebraically wrong

The source continues to assert

`R_\lambda-R_\mu=(\mu-\lambda)R_\lambda R_\mu`

for a nonlinear supremum resolvent. This is the linear pseudo-resolvent identity. For a nonlinear accretive graph, the resolvent relation is implicit and involves an affine combination of the datum and one resolvent value. The submitted dynamic-programming paragraph does not derive that identity or an equivalent graph relation.

Consequently the claimed independence of the graph from `\lambda`, full range, `m`-dissipativity, comparison, Crandall–Liggett generation, and uniqueness all rest on a false formula. The discounted variational operator has not otherwise been proved to be the resolvent of any closed graph.

### 2.4. The hierarchy corrector remains an outline

The corrector theorem invokes B2's invalid factorial majorant and then assumes a geometric tail without an explicit smallness inequality. It also uses one genealogy-uniform recollision exponent although B2 does not provide one, and chooses `K(\varepsilon)` without controlling the growth of `C_K`. Exact specular boundary compatibility, graph-domain regularization, and locally uniform generator convergence are not constructed.

### 2.5. Nonlinear Trotter–Kato hypotheses remain merely listed

Compact containment, upper and lower extended-generator recovery, equicoercivity, comparison, and initial convergence are all imported from unavailable results or asserted. One approximate equality on a formal core does not automatically provide both generator inequalities. Exact law–hierarchy realizability, even if proved, would not establish convergence of nonlinear value semigroups.

## 3. Editorial consequence

A valid revision must first derive the correct nonlinear resolvent relation and graph, establish a function space with true strong continuity, and construct quantitative finite-particle correctors satisfying the boundary domain. None of these repairs appears on the branch.

## 4. Recommendation

**Reject without reconsideration.** The core comparison and semigroup theorem still collapses at the resolvent identity.