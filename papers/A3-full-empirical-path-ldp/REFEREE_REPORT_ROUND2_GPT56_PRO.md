# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** A3 — *Full Liouville Empirical-Path Large Deviations and Information Projections for Finite-Horizon Sinai Billiards*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `c17a8a2a15cd8398140660fba9b19bab7f7aa2ab`  
**Revision provenance:** the repository's discoverable eleven-paper revision ref contains prior referee material but no revised A3 source. This report reviews the controlling source on `main`.

## Overall assessment

The paper claims a full weak-topology empirical-path LDP in collision and physical time for a finite-horizon Sinai billiard. The proposed architecture—an exponential Young presentation, a countable-shift level-2 LDP, a singularity-shielded approximation, and a marked-renewal/Palm contraction—is plausible and could be mathematically important.

The revision improves several truth boundaries: it avoids a naive entropy formula for the countable shift, acknowledges that fixed central-window conditioning needs more than a level-2 LDP, and describes random-root limits through the convex hull of phases. Nevertheless, the three hard theorems in the architecture are still asserted in compressed sketches. In addition, the information-projection theorem remains false under its stated hypothesis, and the cotangent quotient remains ill-defined. Since A3 is load-bearing for A4 and C2, these are series-level defects.

## Major objections

### 1. Applicability of the countable-shift LDP is asserted, not established

The manuscript states that a “standard” Sinai Young tower can be coded as a finitely primitive countable Markov shift whose stationary law is a Bowen Gibbs state for a summable-variation finite-pressure potential, with exponential moments for collision length and physical duration. These properties are exactly the hypotheses needed for the cited countable-shift theorem, and each requires verification for the actual presentation.

The paper does not prove:

- finite primitivity or finite irreducibility of the selected return-block code;
- summable variations of the induced potential on that code;
- identification of the Gibbs state with the desired Liouville block law;
- finite pressure in the selected normalization;
- passage from one-sided to two-sided empirical-measure LDPs in the chosen topology; or
- exponential tightness after adjoining the unbounded return and duration marks.

Exponential return tails alone do not automatically yield the full marked empirical-measure statement used later. The manuscript itself calls these items imported inputs to be checked externally. Hence the first load-bearing theorem remains conditional.

### 2. The singularity-shielded Palm approximation is still only a proof program

The factor from return blocks to billiard path windows is discontinuous on iterated singularity and grazing sets. To obtain an exponentially good approximation, one needs quantitative estimates uniform in the return truncation, path-window length, weak-metric test family, singularity preimages, and Gibbs distortion constants.

The proof says that a singularity neighborhood has Liouville mass \(O(\delta^\alpha)\) and that bounded distortion gives an exponential-frequency cost tending to infinity as \(\delta\downarrow0\). This conclusion is not automatic. One must prove a uniform exponential deviation estimate for visits to the relevant union of singularity neighborhoods, whose complexity grows with both the block truncation and the path-window length. No constants, admissible order of limits, or dependence on the finite test family are provided.

This is the essential billiard-specific lemma. A few paragraphs cannot replace the theorem.

### 3. The marked random-time contraction is not proved

An LDP at return-block speed does not transform into collision-time or physical-time LDPs merely by dividing the rate by the mean mark. A complete random-time theorem must control:

- inversion of the random clock;
- the random number of complete excursions;
- initial and terminal residual blocks;
- size-biased Palm reweighting;
- continuity of the lift on the chosen weak/local-Skorokhod topology;
- exponential tightness after the time change; and
- both upper and lower bounds at the new speed.

The proof simply says to apply a joint LDP for the marks, use continuity for bounded marks, invoke the preceding approximation, and absorb incomplete blocks. This is an outline. In particular, goodness of the displayed rate functions on noncompact path spaces is asserted rather than derived.

### 4. The deterministic-path support proposition ignores singular closure effects

The path spaces are defined as closures of nonsingular deterministic orbit paths. Their closures may contain limiting paths meeting grazing or multiple-collision configurations where the billiard continuation is not represented by a single-valued map. It does not follow that every invariant probability on the closure is determined by a nonsingular time-zero marginal, nor that every weak limit charged by a rate is an ordinary deterministic lift.

A closed-support theorem compatible with the singular factor map is required. Otherwise the rate domain must explicitly include generalized limiting paths.

### 5. Presentation independence is invoked after an unproved contraction

Uniqueness of a good LDP rate does imply presentation independence once every presentation has been proved to yield a full LDP for the same family, topology, and speed. That is precisely what the missing marked-renewal theorem is supposed to establish. Rate uniqueness cannot be used to bypass proof of the hypotheses.

### 6. The information-projection theorem is false as stated

The theorem assumes only that the affine constraint set is nonempty and concludes that the minimizing set is nonempty and compact. A nonempty closed constraint set can lie entirely outside the finite-rate domain. Goodness gives compactness of finite sublevel sets; it does not make the rate finite everywhere.

The conditional concentration statement also requires:

- a finite constrained infimum;
- attainment within the effective domain;
- nonzero conditioning probabilities;
- a lower bound for the conditioning denominator; and
- an LDP continuity or exposedness condition for shrinking neighborhoods.

None follows from nonemptiness. The theorem needs at least an explicit assumption that the constraint intersects the effective domain with finite cost and that the shrinking conditioning sets are LDP-continuity sets.

### 7. The random-root conclusion is weaker than the word “mixture” suggests

The proof shows that test-function expectations of subsequential random-root laws lie in the closed convex hull of minimizing phases. To conclude representation as a probability mixture over the phase set, one needs compactness in a locally convex setting and an appropriate barycentric representation theorem. The current argument establishes a barycentric/convex-hull conclusion, not automatically a unique or canonical mixture.

### 8. The cotangent quotient is not a defined quotient space

The denominator

\[
\mathbb R+\overline{\{U-U\circ\Theta_t\}}
\]

is ambiguous. The manuscript does not specify the class of \(U\), whether \(t\) is fixed or variable, the ambient topology, or the closed linear span. The union of fixed-time coboundary sets over varying \(t\) need not be linear. Without quotienting by a precisely defined closed linear subspace, \(\mathscr V_R\) may fail to be a vector space or Hausdorff.

The subsequent multiplier theorem also requires a specified dual pairing and a constraint qualification.

### 9. A3 remains the unclosed parent theorem for A4 and C2

A4's universal pressure and phase law, and C2's contraction and cotangent claims, are built on the full physical path rate. Those downstream papers cannot treat A3 as established while the coding, singular approximation, and random-time lower bound remain conditional.

## Status of prior objections

The revised distinction between random-root conditioning and deterministic central-window conditioning is correct. The warning against a naive countable-shift entropy formula is also appropriate. These changes improve mathematical honesty but do not prove the central LDP.

## Required reconstruction

A credible resubmission must supply a complete standalone marked-renewal contraction theorem for one explicitly constructed Sinai Young presentation, including all singularity-frequency estimates and time-change topology. The information-projection theorem and cotangent quotient must be reformulated on the effective domain and a precise closed coboundary subspace.

## Editorial recommendation

**Reject.** The headline full path-space LDP remains a sequence of plausible but unproved bridges, and two downstream structural theorems are still false or ill-defined in their current form.
