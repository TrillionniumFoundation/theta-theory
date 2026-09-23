# Response to the two v16 referee reports

**Manuscript:** General Theta Foundations I: Adaptive Testing and Collision-Sensitive Comparison, seventeenth revision.

**Controlling report:** second independent report, `b59d8527c8edc0361be3085604bcf3a920dbfbda`, report blob `e5da7aad09a5a5df84b16d6e8daa76e5dc7054c0`. **Earlier report:** pipeline-aware report, `f52d4afe6a688a2c440d4f9f351e3664e1f08a2a`, blob `59dc90d92c5dfc0b0448114c4d27907790359e3d`. Both reviewed v16 HEAD `5941223e297f6c54583d729cc292831c183277e9`.

We thank the referees for separating credible finite mathematics from the structural questions still unanswered by v16. The revision retains the prior mathematics and supplies three new theorem groups: independent adaptive testing with intrinsic test-size bounds; a collision-sensitive marked resource gap; and whole-process optional-projection stability with a microscopic verification of its hypotheses. The clean canonical source tree no longer imports mathematical files across revision directories. The archive preserves the earlier development.

## E16-R2.1 / E16.1 — Polynomial positivity and priority

The introduction now cites the exact nearby results: de Klerk–Laurent Theorem1.4, Laurent–Slot Theorem2/Corollary3, and de Klerk–Vera Theorem9/Proposition2. The source/locators and subtraction are in LITERATURE_COMPARISON.md. Generic positivity under degree elevation, hypercube certificate hierarchies and their degree estimates are not claimed as new. The new result controls an independent simplex-valued behavior test, not the bit complexity or degree of a generic positivity verifier. Applying the classical verifier after pulling that test back to row variables is an expressly separate step.

The article's three-weight witness makes the distinction concrete: its test is a function of the proposed observable law, while its final 17-coefficient positivity check is classical exact arithmetic. We do not claim that a better hypercube Positivstellensatz follows from it.

## E16-R2.2 / E16.2 — A genuine independent variational object

The old theorem is now headed “Strict polynomial lower-certificate hierarchy.” Its statements and proof are retained under the same label. The new `thm:v17-dual` instead optimizes over an independently feasible class `C(B,Delta_m)`, with a measure dual over revealed candidate behaviors. The finite-level `thm:v17-degree` has two compact feasible sets and an attained minimax identity; its moment dual has finite support.

The verification game's information is explicit. It receives the proposed law, not an unknown runtime parameter or mark. A lottery over revealed candidate laws is not scored at its barycenter. Thus this duality does not convexify the private simulator's feasible image. It is not advertised as a new unrestricted Le Cam randomization theorem or a one-observation test. These distinctions are part of the definition, theorem and proof, not a footnote.

## E16-R2.3 / E16.8 — Intrinsic quantitative size

`thm:v17-degree` proves `0 <= delta-d_n <= 4 R a/sqrt(n)` in observable affine dimension `a` and diameter `R`. A sparse test uses at most `(n+1)^a` occupied entries; the score has coordinatewise degree at most `n+1`; an attained moment-dual minimizer uses at most `(n+2)^a` atoms. The chart is obtained by a near-maximal determinant argument from the behavior image. Redundant stochastic rows do not enter these existence bounds.

This answers the request for an intrinsic degree/support law, not the stronger question of intrinsic verification bit complexity. Minimization on the nonconvex behavior set, finding a chart, its coefficient bit length and describing the feasible set may still be expensive. The theorem says so explicitly.

`prop:v17-smallcertificate` gives a three-weight cubic test on the two-report example. Nine nonnegative derivative terms and seventeen positive rational Bernstein coefficients prove a lower bound `2/5+9/8960`. A two-square identity also yields `3/8` with affine weights. Constant-test mixtures give zero. The source prints every coefficient; the verifier checks the identities exactly. The metadata reports dimensions, degrees, integer bit lengths and serialized certificate size. This is not an assertion that the example attains the general worst-case degree bound.

## E16-R2.4 — Strict-margin and finite-boundary meanings

The old Bernstein hierarchy remains complete for strict rational levels `L<delta`. No equality certificate is claimed. The new continuous adaptive supremum need not attain; Borel tests do. Finite-level polynomial test and moment-dual extrema do attain. These are separate assertions. For rational finite data, generic real quantifier elimination can decide the semialgebraic equality question, but that classical fact neither supplies a nonnegative Bernstein expansion at equality nor a useful runtime bound. The physical algorithm stops at any requested positive interval width only.

## E16-R2.5 / E16.3 — Resource separation in one physical model

The new target reports a noisy collision-generated bit and then receives a gate controlling the second acquisition. Its actual mark is correlated with the incoming impact orientation and remains unobserved. The reference joint masses are `5/16` for equal bit/mark and `3/16` otherwise. `thm:v17-markedgap` gives, at the same width-one private register, private and visible value `sqrt(5/2)-9/8`, but hidden-two-selector value `1/8`.

The all-on gate gives a sharp lower witness. The optimal private independent-bit table and the hidden two-table construction give upper bounds for every feedback rule by the same gated pushforward. Visible randomness is compared jointly with an independent target selector. No emitted history is silently reread by the simulator. Hidden selection does not erase the actual-mark obstruction.

## E16-R2.6 / E16.4 — Collision geometry does mathematical work

`lem:v17-scattering` treats full-dimensional rational preparation boxes for two labeled equal-mass spheres. An explicit nongrazing first collision creates a tagged transverse velocity of signed magnitude above1/2. The bounded detector is zero on the incoming range. For diameters .9–1.1 and noise at most1/12, `thm:v17-physicalgap` transfers the reference values with error below1/300: private/visible >.45, hidden <.13.

For diameter at most.4 the same preparation and detector undergo no collision during acquisition; the reports become independent pure-noise bits and every deficiency is zero. Thus the separation cannot be attributed to conserved collective momentum. The conserved longitudinal component only labels the actual mark. The bounds are uniform on a nontrivial diameter interval and under geometric similarity. They are not Boltzmann–Grad or particle-number-uniform estimates. Feedback is a later sensor gate, not a mechanical force; this is stated at the beginning of the section.

`prop:v17-collisioncompute` uses a separated explicit collision root and a computable Lipschitz bound to produce rational marked prefix laws uniformly. The finite target realization is distinguished from extra memory available to the simulator.

## E16-R2.7 / E16.5 — Exact relationship to v15 and v16

The v15 stateless physical-to-rational triangle remains the physical transfer theorem. The v16 addition was the global strict polynomial lower module, the collective benchmark and the exponential-value estimate. We state this explicitly both where `thm:v16-main` first appears and in the dependency appendix. The new v17 results are the independent-test degree/support law, the scattering resource gap and the posterior-process criterion. Reusing a transfer inequality with another lower-certificate module is not presented as rediscovering the transfer principle.

## E16-R2.8 — Effective quantifiers

`prop:v17-effective` requires one algorithm returning the rational instrument and certified rational errors from the presentation index, and uniform finite subroutines from that index and the resource signature. Its proof searches the certified errors before dovetailing finite lower and upper witnesses. The v16 general physical theorem is annotated with this requirement. The scattering theorem verifies it directly. A sequence whose elements are merely individually computable is not enough.

## E16-R2.9 / E16.6 — A proved downstream conditional-law input

The new C2 contribution is `thm:v17-optional` and `thm:v17-physicaloptional`. The first controls the entire posterior martingale under equivalent joint marked laws with a common latent marginal, using Bayes' formula and maximal inequalities. The second verifies joint variation convergence from L2 graph-core approximation in Gaussian observation of an invariant microscopic hard-sphere flow. It yields uniform-in-time L2 convergence for latent L2 variables and probability convergence for latent L1 variables, not merely finite-dimensional convergence followed by an unsupported tightness assertion.

This supplies an explicit sufficient conditional-law/optional-projection hypothesis in a real microscopic class. It addresses the optional-projection part of historical C2 without claiming that changing microscopic path limits, limiting Gaussian likelihood identification, Girsanov/BSDE limits, rigidity, strict duality or covariant form response have thereby all been proved. The convergence coupling is not used as a free causal simulation channel.

The historical B4 gate still needs its dynamic action, action-sublevel compactness, nonlinear resolvent comparison, uniform hierarchy corrector and kinetic limit. None is replaced by a graph-core, single collision or total-variation estimate. The pipeline graph preserves every earlier status and records the new proved scoped C2 input. All full-historical-target closure flags remain false. The independent A2 primary geometry remains independent. The program's targets have not been deleted; their dependencies are kept distinct.

## E16-R2.10 / E16.7 — Norberg original-text comparison

This requirement is **not fully closed**. The Norberg original was not obtained at proof level through the publisher and catalog routes tried in this revision. We do not reconstruct its definitions or theorem from an abstract or from a later author's description. LITERATURE_COMPARISON.md records the missing proof-level questions explicitly.

The accessible Weisshaupt original was inspected at Definition5.1 and Theorems5.1–5.2, including its adapted operator and finitely-additive-output scope. It supplies a precise adjacent comparison, not a substitute for Norberg. The article credits filtered deficiency as prior theory and claims neither priority for that concept nor proof that Norberg lacks a particular theorem. The new mathematics is independently stated and proved; the outstanding historical priority audit remains for further verification.

## Technical and presentation comments

The finite carrier and strict-margin qualifications accompany the old completeness claim. Value invariance, independent-test existence size and row-certificate complexity are separated. Visible reference selector laws are displayed jointly in the new physical theorem. The old collective section now explains action timing, collision cancellation, diameter independence in its solvable regime, and the projection meaning of its residual. The bounded exponential estimate remains an accuracy-transfer prerequisite, not a large-deviation or kinetic theorem.

The new canonical entry and every transitive TeX input are local to this directory. A standalone submission source archive is built and its closure checked. The archive with historical introductions is explicitly not required for understanding the canonical article. No unpublished inherited theorem is relabeled as previously published work; the source-preservation map records ancestry, while the journal text presents one theorem narrative and a mathematical dependency appendix.

All predecessor bodies, hypotheses and goals are preserved; three local copies have identified wording/hypothesis annotations. The build checks the 402 inherited inputs and all 812 prior development labels. Diagnostic counts, build identities and exact coefficients are reproducibility records, not evidence of theorem novelty or independent analytic verification. Whether the enlarged result set meets the requested venue's significance standard remains a matter for independent review.
