# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A1 — *Deterministic Path Ensembles, Driven Collision Maps, and Endogenous Conjugate Parameters*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `e1508999b777aded8fa5ca911440818e3cb09cc1`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/A1_RECUT_HAMILTONIAN_RESPONSE.tex`, blob `77ffe62ab129ee4d8c11e0cb3d401b10055d970d`

## Source-control verdict

The round-five candidate is not part of the manuscript. All eleven paper-level controlling modules on the branch are byte-for-byte the round-four modules. The fail-closed publication workflow stopped while materializing this very A1 packet because it contains the ASCII control byte `0x08`; every subsequent hostile gate, clean build, certificate, and publication step was skipped.

Accordingly the legally reviewable paper is the active round-four source, for which the preceding objections remain dispositive: the announced mapping torus has incompatible incoming and outgoing boundary types, the work one-form does not descend through the gluing, and the response operators are not defined. I have nevertheless reviewed the proposed round-five packet as a candidate replacement. It also does not establish the advertised theorem.

## Assessment of the active manuscript

The active paper cannot be accepted. Its first-return construction does not define a Hamiltonian flow on the stated quotient, and its mechanical-current statement uses a piecewise form which is incompatible with nontrivial changes of port label. Compilation and the presence of a proof environment do not repair those type errors.

## Audit of the proposed round-five replacement

### 1. The proposed mechanical work form does not realize the current on the full Liouville path law

The candidate replaces the non-descending form by

\[
\alpha_a=\sum_i\epsilon_i\chi_i(x)\rho(\tau)d\tau,
\]

where each `chi_i` is one only on a port core and vanishes near every seam. The proposition then claims that every regular return entering port `i` accumulates exactly `epsilon_i`. This is false for regular points of the same open port lying outside the chosen core. Along the suspension flight the section coordinate is fixed, so their accumulated work is

\[
\epsilon_i\chi_i(x),
\]

not `epsilon_i`.

A smooth function cannot simultaneously be one on the entire open port and vanish in a neighborhood of its boundary. The omitted collar has positive Liouville area for every fixed choice. Therefore the resulting mechanical cocycle is not the symbolic branch current on the complete natural path law, and the later exact change-of-law and calibration claims do not follow from this form.

The authors may retain the branch current as a measurable section cocycle, or construct a genuinely global smooth observable on a modified channel. They cannot claim both exact smooth mechanical work and the full Bernoulli current without resolving this mismatch.

### 2. The graph-completed suspension and smoothing theorem is asserted rather than constructed

The candidate introduces a graph completion cut by both vertical and horizontal seams and defines recutting as the coordinate identity between cut atlases. This is a reasonable repair direction, but the proof does not establish the full global theorem it states. In particular it does not provide:

- a complete compatible corner atlas at multiple seam intersections;
- a proof that the quotient after time-one gluing is a Hausdorff symplectic manifold with corners rather than a stratified correspondence;
- a relative Hamiltonian extension theorem for all four prescribed affine branches with the required boundary behavior;
- compatibility of the collar isotopies with recutting; or
- preservation of return time, section flux, and the claimed work observable under corner smoothing.

The phrase “relative Moser equation removes the cutoff error” is not a substitute for constructing the exact isotopy and checking its support and boundary restrictions. Moser’s method adjusts symplectic forms; it does not automatically produce a prescribed return map with all of the listed dynamical properties.

### 3. The response calculus remains incomplete at the physical moving-seam level

The symbolic transfer operator on the one-sided full shift is now defined, which is an improvement. The paper then adds a physical saltation term

\[
\sum_i s_i'(a)[G_a]_{s_i(a)}\,\mathfrak j_i
\]

and asserts all-order convergence of finite differences. No Banach space of physical observables with seam traces is specified, the flux distributions `j_i` are not defined as continuous functionals, and no all-order estimate controls repeated seam crossings and parameter derivatives. The symbolic spectral-gap calculation does not prove the physical-coordinate saltation theorem.

### 4. The candidate file itself is not valid source material

The exact candidate blob contains an ASCII backspace byte. The repository’s own materializer rejects it before writing any paper. This is not merely a cosmetic CI failure: the branch does not contain a materialized manuscript incorporating the claimed repair, and there is no clean build or exact-source verification for it.

### 5. The calibration theorem is conditional, not endogenous selection by mechanics

The candidate correctly says that equality of the valuation coefficient and the mechanical conjugate field follows only after requiring equality of the two likelihood cocycles in common units. That is a compatibility theorem. It does not show that deterministic mechanics selects a preference coefficient among all admissible valuation rules. The title and abstract continue to invite a stronger reading than the theorem supports.

### 6. Top-four novelty remains absent after correction

Once the global mechanical claims are properly scoped, the mathematical content is an explicitly solvable Bernoulli baker benchmark, a multinomial Gibbs-conditioning calculation, a standard exponential-family identity, a CARA classification under strong axioms, and elementary response estimates on a full shift. This can be useful as a benchmark or expository note, but it is not of the depth or novelty required by any of the four journals.

## Required reconstruction

A viable version must first materialize valid UTF-8 source, then define one actual cut-section self-map and its global suspension, construct a work observable which agrees exactly with the branch cocycle on the full regular section, and prove the physical moving-seam response theorem in declared trace spaces. The mechanical/valuation identification must remain explicitly conditional.

## Recommendation

**Reject.** The active manuscript is unchanged and invalid at its main mechanical interface. The unmaterialized candidate improves the architecture but still fails to realize the current on the full Liouville law and does not prove the global suspension or physical response theorem. Correctly scoped content remains below the top-four threshold.