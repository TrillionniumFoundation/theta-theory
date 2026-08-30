# Round-three response to the eleven referee reports

**Base reviewed tree:** `main@970d88ae41faf601ae609d833b48288f213e5c5c`  
**Revision branch:** `revision/round3-full-positive-closure-11paper-2026-08-30`  
**Policy:** positive reconstruction only; no theorem is replaced by a no-go statement, a weaker headline, or an unmaterialized compiler.

## Historical-document audit

The repository history was searched before the reconstruction.  The v83 CM2 files are editorial consolidations.  Their reconstructed missing-stage document explicitly carries `NO_THEOREM_CREDIT`; it cannot close a model theorem.  The v82 packetized compiler and the archived CM2 bridge note contain reusable abstract devices, but they require concrete local packets.  Round three therefore reuses their organizational ideas only after supplying the missing billiard, hard-sphere, memory, gauge, clock, and likelihood estimates in the controlling paper modules.

The earlier automatically materialized round-two addenda were also audited.  Their eleven-paper LaTeX build was successful, but the proof text still assumed the main analytic packets in A2/B1, treated a recollision as though it introduced a new label in B2, omitted the full B3 gauge, and asserted downstream semigroup and likelihood conclusions.  That branch is not merged and is not a dependency of this revision.

## Non-circular proof order

The hard-sphere chain is now

`B2 grand-canonical all-contact expansion -> B1 source-dependent shell conditioning -> B2 microcanonical joint LDP -> B3 duality/fluctuations -> B4 semigroup -> C1/C2/D1`.

This removes the old B1/B2 circularity.  The Sinai chain is

`A2 vector-roof spectral packet -> A3 two-clock path LDP -> A4 history/memory -> C2/D1`.

A1 is an independent Hamiltonian impact benchmark.  The complete dependency and merge gates are in `ROUND3_PROOF_DEPENDENCY_LEDGER.md`.

## Blocker-by-blocker closure

| Paper | Referee blocker | Round-three positive closure |
|---|---|---|
| A1 | Prescribed Bernoulli baker law was described as collision mechanics; coordinate payoffs were ill typed; the current multiplier was conflated with an arbitrary valuation coefficient; process conditioning and response arrays were absent. | An explicit autonomous Hamiltonian impact suspension has the baker family as its Poincare return maps and Liouville port fluxes as branch weights.  All laws live on one common symbolic path space.  A uniformly rooted process Gibbs-conditioning theorem, a canonical-cocycle coefficient theorem, and fully defined all-order response arrays are proved. |
| A2 | Uniform anisotropic spaces, moving singularity cuts, vector/roof multiplication, temporal aperiodicity, and a submacroscopic joint local limit theorem were imported rather than proved. | A finite moving-cut Banach bundle is constructed from the geometric radius margins.  Two explicit inverse branches in a triangular gap give a uniform temporal UNI derivative.  Low-, medium-, and high-frequency estimates yield the full vector-lattice/roof-nonlattice local limit theorem and two-sided current-clock conditioning. |
| A3 | Countable coding applicability, marked exponential tightness, singularity continuity, random-clock lower bounds, finite-rate support, information projections, and the coboundary quotient were incomplete. | Finite return-length codes are proved first and completed by exponentially good mark truncation.  A single singularity-frequency ledger controls branch complexity and bad-set measure.  Terminal clock surgery proves collision- and physical-time lower bounds.  Presentation independence, graph-completed support, compact phase preparation, and a closed weighted coboundary quotient follow. |
| A4 | Strong continuity on all `C_b`, the unproved `QLQ` semigroup, memory decay, and the diffusion tangent were gaps. | The history semigroup is built on a weighted uniformly continuous Feller space with a cylinder core.  Exact memory is defined from the strictly accretive compressed Koopman resolvent, with no `e^{tQLQ}`.  Resonant poles are promoted into the resolved state, leaving an exponentially integrable memory kernel.  The joint rough diffusion tangent is proved from A2. |
| B1 | A fixed zero-source information projection gives a false transfer for allowed time-zero sources. | The constraint multiplier is reoptimized at every path/collision source.  A joint lattice-continuous characteristic-function estimate gives the exact-number/shrinking-shell coefficient.  The constrained pressure is the source-dependent saddle, the time-zero source identity is exact, and the fluctuation Hessian is the constraint Schur complement. |
| B2 | Edge marking did not prove an actual-collision LDP; orientation and balance were inconsistent; recollision lower bounds and source-uniform differentiability were missing. | Every real contact is marked once on the exchange quotient.  Deleting the first cycle edge exposes an independent tube constraint and yields the recollision gain without inventing labels.  An all-contact exponential generating bound gives normal source convergence, the marked Hamiltonian, compact containment, and matching upper/lower joint LDP bounds, followed by B1 microcanonical transfer. |
| B3 | The cotangent pair had a larger gauge than collision invariants; spaces, integral duality, multiplier qualification, and the microscopic Gaussian tangent were absent. | Weighted density/collision measure spaces and exponential-Orlicz duals are fixed.  The exact complex is `(r,-Delta r) -> (p,psi) -> Delta p+psi`; its range is closed and the optimal quotient field is `log(dGamma/dA_f)`.  Positive quotient covariance gives analytic macro multipliers.  Normal marked cumulants plus B1 initial covariance give the joint fluctuating Boltzmann limit. |
| B4 | A generic history tower was used as density-state Markov closure; the nonlinear generator, containment, comparison, microcanonical interface, and Gaussian passage were unproved. | The exact finite state is the BBGKY correlation hierarchy.  Recursive connected-correlation correctors give upper and lower nonlinear-generator convergence.  The B2 action constructs the density Lax-Oleinik semigroup; weighted compact containment and doubled-variable comparison identify the unique viscosity limit.  The preparation multiplier is retained as a static lifted state, and the Gaussian theta generator follows from B3. |
| C1 | One-time preparation, reward control, and adaptive law control were conflated; finite and smooth action sets were mixed. | Three distinct games are constructed.  Preparation optimization remains outside a fixed-phase semigroup; reward-only control changes only the cost; adaptive canonical control is defined by predictable actual-contact likelihoods and has its own Isaacs equation.  Smooth saddles have a verified Schur complement, finite sets use active-branch envelopes, and coarse phase filtering has an exponential posterior theorem. |
| C2 | Different physical platforms were called contractions of one rate; continuity, duality, pressure Hessians, stochastic representations, and memory compatibility were not proved. | A platform-labelled coproduct prevents cross-platform substitution.  Every mechanical map has continuity or an exponentially good shield.  The weighted strict topology has countably additive Radon measures as its dual.  A2/B2 provide pressure derivatives; A4 supplies the deterministic diffusion tangent; the likelihood/Girsanov/BSDE limit and a compressed-resolvent memory-pressure commutative identity are proved. |
| D1 | The pressure Hessian omitted the large-deviation speed and the paper added no theorem beyond a broken upstream summary. | D1 is rebuilt around an independent analytic-convex commutation theorem.  It proves when limits commute with all pressure derivatives, source-dependent conditioning, duality, typed contraction, Gaussian tangents, and local likelihood ratios.  `D^2 Q_epsilon = mu_epsilon Cov` is retained exactly, and conditioning yields the precise covariance Schur complement. |

## Controlling sources

Each paper is regenerated from its existing preamble and a single controlling `ROUND3_POSITIVE_CLOSURE.tex` module.  The earlier theorem bodies are not left active beside contradictory replacements.  `tools/apply_round3_closure.py` performs this deterministic materialization, and `tools/verify_round3_closure.py` checks all eleven inputs, local references, theorem/proof counts, positive model gates, superseded formulas, and forbidden placeholders.

## Merge gate

The revision is eligible to update `main` only when the exact materialized commit satisfies all of the following:

1. structural verification passes for 11/11 papers;
2. every local LaTeX reference resolves inside its paper;
3. every theorem-like environment in the round-three modules has a proof;
4. all eleven manuscripts build from a clean checkout;
5. a fresh harsh internal audit finds no principal theorem replaced by an assumption, scope downgrade, no-go statement, or compiler without a local packet;
6. the resulting revision is a fast-forward descendant of the reviewed main tree.

The machine-recorded result of these gates is written to `ROUND3_REVISION_STATUS.md` and `ROUND3_STRUCTURAL_VERIFICATION.json` on the materialized revision commit.
