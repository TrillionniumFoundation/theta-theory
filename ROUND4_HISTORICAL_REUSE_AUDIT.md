# Round-four historical derivation reuse audit

## Scope

The new reports on
`review/round3-referee-reports-11paper-2026-08-30` were compared against:

- `canonical/theta_theory_recursive.md` from
  `archive/full-v4-pre-governance-2026-08-29`;
- `canonical/CM2_LATEST_STATUS.md`;
- `canonical/THETA_THEORY_CURRENT_STATUS.md`;
- `canonical/THETA_MAXIMAL_FINAL_STATUS_V3.md`;
- the eight files under `revision/round3-rereview/`;
- the active eleven controlling modules reviewed by the referee.

Historical status words such as `CLOSED`, `PROVED`, `PASS`, or a compiler name
were not counted as theorem credit unless the proof was materialized into the
controlling manuscript and all model-specific dependencies were present.

## Exact conclusion

| Paper | Prior material that is genuinely reusable | What remained unsolved | Round-four action |
|---|---|---|---|
| A1 | Common symbolic path law, Bernoulli change of measure, response arrays | The purported global torus Hamiltonian was not defined; calibration assumed the entropic form | New cut-port exact symplectic map, autonomous mapping-torus suspension, and derived Kolmogorov--Nagumo calibration |
| A2 | `A2_UNIFORM_GEOMETRY.tex`, polygon UNI calculations, finite-iterate geometry | All-depth moving cuts, boundary currents, quantitative Dolgopyat block, Livsic/covariance theorem, complete LLT smoothing | Materialized the old packets and added a current-augmented bundle plus the full four-frequency proof |
| A3 | `A3_DIRECT_PATH_LDP.tex` correctly identified an escape branch | Survivor pressure, exposed zero-frequency phases, full lower bound, and a Radon cotangent proof | Constructed survivor operators, the renewal/escape maximum, exposed-phase approximation, and bounded-strict annihilator theorem |
| A4 | `A4_RAY_FELLER.tex` correctly separated Ray and exposed-phase continuity | Time-domain memory regularity, pole realization, exact nonlinear tower, explicit memory scaling | Added a Volterra kernel construction, minimal realization, Doob-normalized tower, and defined rough/memory limit |
| B1 | Source-dependent saddle and mixed shell setup | Safe-box activity scale was wrong; the span-one repair repeated it | Replaced the argument by singleton-dominated connected pressure and source-uniform mixed Fourier inversion |
| B2 | `B2_GLOBAL_SOURCE_LDP.tex`: bounded real sources, positive balance right inverse, regularization | The first-cycle bound did not dominate all later recollisions | Added ancestral witness strata and forgetful graph surgery for the complete cyclic sector, then used the old global-source packet |
| B3 | Local balanced variation idea in `B1_B3_NULLSPACE_PACKET.tex` | Orlicz equivalence classes could not detect singular Radon current; process tightness and `Dq` were absent | Rebuilt the dual/gauge complex in bounded-strict Radon topology and added a nuclear-space process CLT |
| B4 | B2 tree estimates and B3 covariance are reusable inputs | Superquadratic Gaussian source, false moment conservation, noncompact topology, formal correctors | Added energy-compatible topology and backward connected Duhamel correctors |
| C1 | `C1_BLOCK_NORMALIZED_CONTROL.tex` correctly removed the artificial compensator | Uniform conditional source theorem, correct expected testing exponent, LAN, and sufficient information state | Added exact conditional block DPP, Chernoff expected exponent, finite-mean LAN/BvM, and posterior-plus-history state |
| C2 | `C2_STRICT_MEMORY.tex` supplied the Doob generator and correctly typed compressed memory formula | Strict phase compactness lacked coercivity; varying filtrations were not controlled | Added explicit rate coercivity and uniform resolved-kernel/optional-projection convergence |
| D1 | Analytic pressure and Schur-complement calculations | Missing constrained-rate constant and wrong finite-volume centering | Added normalized constrained duality and exact finite-mean likelihood identities |

## Why the previous corpus did not already close the reports

The recursive and CM2 documents contain a large amount of correct abstract
infrastructure, but several passages explicitly classify the relevant items as
conditional, synthetic, implementation-only, or dependent on an actual model
packet.  The eight later repair files improved six papers, but were not
included in the active controlling sources at the reviewed commit and still
left the A1, B1, B3, B4, and D1 blockers untouched.  Therefore the new referee
objections were not caused merely by an indexing error; they exposed both a
materialization defect and new mathematical defects.

## Round-four policy

All useful historical derivations are incorporated before adding new tools.
No principal theorem is deleted, weakened to a no-go statement, or marked
conditional.  Every replacement is checked against a forbidden-regression
registry, a local theorem/reference verifier, a non-circular dependency DAG,
and a clean eleven-paper LaTeX build.
