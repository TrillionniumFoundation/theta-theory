# Referee Report

**Manuscript:** A3 — Full Empirical-Path LDP  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

The paper claims a full weak-topology level-2 LDP for collision and physical empirical path measures of a finite-horizon Sinai billiard, obtained by coding a Young tower, applying a countable-shift LDP, and performing a singularity-shielded random-time Palm contraction. This is the central bridge on which A4 and C2 depend.

The bridge is not established. The manuscript replaces several difficult theorems—construction of a suitable finitely primitive code, exponential approximation across billiard singularities, and a marked renewal LDP under random speeds—by short sketches. It also contains two precise statement-level defects: nonempty constraint sets do not imply finite-rate information projections, and the proposed “coboundary quotient” is not defined as a vector-space quotient.

## Major objections

### 1. Applicability of the countable-shift LDP is not verified

Takahasi’s level-2 theorem assumes a finitely irreducible or finitely primitive countable Markov shift and a Bowen Gibbs state for an appropriate finite-pressure potential. The manuscript asserts that a “standard” Sinai Young tower can be coded with all of the following properties:

- finite primitivity;
- summable variations;
- finite pressure;
- a Gibbs state matching the selected stationary block law;
- exponential moments for collision and physical-duration marks.

None is proved for the actual presentation. Passing from the one-sided theorem to the natural extension, and then adjoining unbounded return/duration marks, also requires a theorem, not one sentence. Exponential return tails alone do not automatically provide the asserted empirical-measure exponential tightness for all marked coordinates.

### 2. The singularity-shielded Palm approximation is a major new lemma, not a proof sketch

The factor from symbolic excursions to billiard path windows is discontinuous on iterated singularity sets. To obtain an exponentially good approximation one needs quantitative estimates uniform over:

- return blocks up to the truncation level;
- the finite family of path-window tests used in the weak metric;
- all relevant singularity preimages;
- the Gibbs distortion constants;
- the collision and suspended physical-time normalizations.

The manuscript says that singularity neighborhoods have mass \(O(\delta^\alpha)\) and therefore their excessive empirical frequency has a cost tending to infinity. This conclusion is plausible only after a uniform exponential-frequency estimate has been proved for the induced Gibbs process. No such estimate, constants, or dependence on the truncation level is given.

This lemma is the essential billiard-specific step. Without it, the extended contraction principle cannot be invoked.

### 3. The random-speed marked-renewal contraction is not proved

A block LDP at speed \(N\) does not become a fixed-collision-time or fixed-physical-time LDP merely by dividing the rate by the mean return length. One must control the random number of completed excursions, initial and terminal residual blocks, continuity of the size-biased Palm map, exponential tightness under the new clock, and both upper and lower bounds after inversion of the renewal time.

The displayed infimum formulas are reasonable candidates, but the proof provides no random-time-change theorem with hypotheses and no verification of those hypotheses. In particular, goodness on the noncompact local Skorokhod path space is asserted rather than demonstrated.

### 4. The orbit-path support argument ignores singular closure effects

The path spaces are defined as closures of nonsingular deterministic orbits. Their closures can contain limiting paths through singular configurations where the continuation is not represented by a single-valued billiard map. It does not follow that every finite-rate weak limit is a deterministic lift solely because every prelimit path is. The claim that the rate is automatically infinite off deterministic lifts requires a closed-support theorem compatible with the singular factor map.

### 5. Presentation independence is circular at the point it is invoked

Uniqueness of a good rate implies presentation independence only after each presentation has been proved to yield a full LDP for the same family, in the same topology and at the same speed. That is exactly the unproved content of the renewal-contraction theorem. Rate uniqueness cannot substitute for proving the hypotheses.

### 6. The information-projection theorem is false as stated

The theorem assumes only that the affine constraint set is nonempty. A good rate need not attain a finite minimum on an arbitrary nonempty closed constraint set if every point in that set has infinite rate. Goodness controls finite sublevel sets; it does not make the entire effective domain equal to the probability space.

The conditional concentration formula also requires:

- finite constrained infimum;
- a denominator lower bound;
- nonzero conditioning probabilities;
- an LDP continuity/exposedness condition for shrinking balls;
- a strict rate gap outside the chosen neighborhood.

None follows from nonemptiness. Boundary or unattainable constraints provide immediate counterexamples to the stated formulation.

### 7. The “cotangent quotient” is not a quotient space

The denominator
\[
\mathbb R+\overline{\{U-U\circ\Theta_t\}}
\]
is ambiguous: neither the class of \(U\), the allowed \(t\), the norm/topology of closure, nor the linear span is specified. The union of fixed-time coboundaries over varying \(t\) need not be a linear subspace. Without taking a precisely defined closed linear span, the quotient is not a vector space and may not be Hausdorff.

The subsequent Lagrange-multiplier theorem also needs a constraint qualification; exposedness alone is not a substitute for infinite-dimensional convex duality hypotheses.

### 8. Random-root conditioning gives at most a barycentric conclusion

The argument correctly observes that a uniform interior root samples the empirical average up to an endpoint error. In the nonunique case it yields a limit in the closed convex hull of minimizing phases, subject to tightness. The paper should say “barycenter/closed convex hull” and prove the required compactness. Calling every such limit a “mixture” is acceptable only after a precise representation theorem and topology are fixed.

## Editorial recommendation

**Reject.** The paper’s headline full path-space LDP is not proved, and several downstream theorems are false or ill-defined in their current form. A credible resubmission would need a complete standalone marked-renewal contraction theorem with all billiard singularity estimates.
