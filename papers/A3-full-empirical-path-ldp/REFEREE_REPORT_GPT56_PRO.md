# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A3 — Full Empirical-Path LDP  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`  
**Role in the series:** load-bearing bridge for A4 and C2.

## Executive assessment

The paper claims a full weak-topology level-2 LDP for collision-time and physical-time empirical path measures of a finite-horizon Sinai billiard. Its proposed route—Young-tower coding, countable-shift level-2 LDP, singularity-shielded approximation, and a random-speed Palm/renewal contraction—is mathematically plausible as a research program.

The program is not executed. Every billiard-specific and random-time step is compressed into a sketch, while the final statement is global and topological. Two downstream statements are additionally false or ill-defined at the level of their hypotheses: a nonempty affine constraint set need not intersect the finite-rate domain, and the proposed “coboundary quotient” is not specified as a quotient by a closed linear subspace.

## Major mathematical objections

### 1. The countable-shift theorem is invoked without verifying its hypotheses for the chosen coding

A level-2 theorem for a countable Markov shift cannot be applied by writing “use a standard Sinai Young tower.” The actual presentation must be shown to have the required finite irreducibility/primitivity, potential regularity, finite pressure, Gibbs property, and exponential moment bounds for every attached mark.

The manuscript does not prove:

- finite primitivity of the selected coding;
- summable variations/Bowen regularity for the relevant potential;
- identification of the Gibbs state with the desired billiard invariant law;
- exponential tightness after adjoining unbounded return and duration marks;
- passage from the one-sided coded process to the natural extension; or
- compatibility of the coded empirical measure with the two-sided local path observables.

Exponential tails of the tower return time do not automatically imply the full marked empirical-measure statement used later.

### 2. The singularity-shielded approximation is the central new billiard lemma and is missing

The factor map from symbolic excursions to finite billiard path windows is discontinuous on iterated singularity and grazing sets. To use an extended contraction principle, the manuscript must construct continuous truncations and prove that they are exponentially good uniformly over the weak-metric tests retained at each stage.

A mass estimate of the form \(\nu(N_\delta(S))=O(\delta^\alpha)\) does not by itself give an exponentially small probability that the empirical process visits singularity neighborhoods too often. One needs a uniform exponential-frequency bound for the induced Gibbs process, with constants tracked against:

- return-block truncation;
- path-window length;
- singularity preimages;
- distortion constants; and
- the collision and suspension clocks.

The manuscript supplies no such theorem. This omission alone invalidates the advertised path-space LDP.

### 3. The random-speed Palm/renewal contraction is not a formal division by mean length

Starting with an LDP at excursion count \(N\), one cannot obtain a fixed collision-time or fixed physical-time LDP merely by dividing the rate by a mean return length. A complete theorem must handle:

- inversion of the random clock;
- random numbers of completed excursions;
- initial and terminal residual blocks;
- size-biased Palm reweighting;
- continuity on the selected local Skorokhod/weak topology;
- exponential tightness at the new speed; and
- matching upper and lower bounds.

The displayed infimum formulas are reasonable candidates, but no theorem with checked hypotheses is given. Goodness on a noncompact path space is asserted, not proved.

### 4. The deterministic-path support claim is not stable under singular closure without proof

The state space is the closure of nonsingular deterministic orbit paths. Such a closure can contain limiting paths meeting singular configurations where continuation is not represented by a single-valued billiard map. It does not follow from prelimit support alone that every finite-rate weak limit is a deterministic lift.

The paper needs a closed-support theorem for the singular factor map or must enlarge the state space and state the rate on generalized continuations. The claim that the rate is automatically infinite off deterministic lifts is unsupported.

### 5. Presentation independence is invoked circularly

A good rate is unique once a full LDP for the same laws, topology, and speed is proved. The manuscript uses uniqueness to claim independence of tower/coding presentation before proving that each presentation yields such an LDP. Uniqueness cannot replace the missing renewal-contraction and singularity-approximation arguments.

### 6. The information-projection theorem is false under the stated nonemptiness assumption

A nonempty closed affine constraint set may lie entirely outside the effective domain of a good rate. Goodness means compact finite sublevel sets; it does not imply that every probability measure has finite cost. Hence nonemptiness alone neither guarantees a finite constrained minimum nor a meaningful conditioning denominator.

A valid conditional concentration theorem additionally requires finite infimum, attainability, nonvanishing conditioning probabilities, an LDP continuity/exposedness condition for shrinking neighborhoods, and a strict rate gap away from the minimizer set. None follows from the stated hypothesis.

### 7. The proposed cotangent quotient is not mathematically defined

The denominator

\[
\mathbb R+\overline{\{U-U\circ\Theta_t\}}
\]

is ambiguous: the class of \(U\), the allowed times, the ambient norm/topology, and the linear span are unspecified. The union of fixed-time coboundary sets over varying \(t\) need not be a linear subspace. Without a precisely defined closed linear span, the quotient may fail even to be a vector space, let alone a Hausdorff cotangent space.

The multiplier theorem also needs a constraint qualification and a precise dual pairing; exposedness is not a substitute.

### 8. Random-root conditioning yields only a barycentric/convex-hull conclusion in the nonunique case

Sampling a uniform interior root can identify an empirical average up to an endpoint error. When minimizers are nonunique, subsequential limits lie in an appropriate closed convex hull, subject to tightness. Calling every such limit a “mixture” requires a representation theorem in a specified topology. The manuscript overstates the conclusion.

## Dependency assessment

A3 is the main upstream obstruction in the A-series. Until the full LDP is proved, A4 has no established universal static pressure or phase law, and C2 has no parent path rate from which to contract rigidity and tangent statements. Merely citing A3 cannot close those papers.

## Minimum viable reconstruction

A credible resubmission must be a standalone theorem on marked random-time contraction for a specifically constructed Sinai tower, with all singularity and exponential-tightness estimates. The information-projection and quotient sections should be rewritten only after the effective domain and dual topology are fixed.

## Recommendation

**Reject.** The headline full empirical-path LDP is not proved, and several advertised consequences are false or undefined as stated. This is a foundational gap, not a matter of exposition.
