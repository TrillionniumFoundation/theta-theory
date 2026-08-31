# Response to the Round-Nine Referee Reports

**Review branch:** `review/round9-gpt56-pro-harsh-11paper-2026-08-31`  
**Review head:** `322e4efe825146254d5f4eb6850625b8f99052ea`  
**Reviewed payload:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`

The reports identify direct counterexamples to several Round-Nine
load-bearing statements.  The prior candidate is therefore not promoted.  A
new controlling source and a paper-local `AUTHOR_RESPONSE_ROUND10.md` are
provided for each of the eleven papers.

## Series-level reconstruction

- The A1 bilateral Koopman estimate is removed.  Physical response is built
  from the two one-sided noninvertible Ruelle operators, and the physical map
  is realized by an exact mapping torus rather than an external reset.
- A2 supplies separate model-specific theorems for moving births, arithmetic
  aperiodicity, geometric UNI, the Dolgopyat range, and the very-high-frequency
  density tail.
- A3 uses deterministic speeds and a sufficient marked edge-flow state.
- A4 conditions on a genuine past, uses a correctly centered Poisson
  martingale difference, an eigenfunction Doob semigroup, and the full
  unresolved-space memory realization.
- B1 restricts shell conditioning to regular interior targets and proves
  global regenerative smoothing under the typical compound law.
- B2 constructs the compatible trace graph and replaces pointwise/QR
  transversality by an integrated physical Jacobi small-ball theorem.
- B3 proves covariance first and identifies the action tangent by second
  epi-differentiation; the raw perspective Hessian is never assumed positive.
- B4 distinguishes microscopic observables from law push-forwards, constructs
  an observable graph core, charges preparation once, and proves comparison by
  a two-scale coercive Tataru argument.
- C1 retains unnormalized observation currents and log evidence in an
  arbitrary-codimension filtering tower.
- C2 uses closed linear nullspaces and a common transfer Banach bundle, not
  infinite-path Radon--Nikodym trivializations.
- D1 begins with positive common-space phase components and proves exact
  physical reconstruction before applying labelled contraction.

## Verification boundary

The blocker map is recorded in `ROUND10_REFEREE_INVENTORY.*`, the historical
provenance in `ROUND10_HISTORICAL_DERIVATION_AUDIT.md`, and the acyclic proof
order in `ROUND10_PROOF_DEPENDENCY_LEDGER.md`.  Structural and hostile
regression scripts inspect exact source bytes and explicit failure modes.
Successful internal verification and compilation do not constitute acceptance
or independent mathematical certification by an external journal referee.
