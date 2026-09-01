# Round-Twenty-One historical derivation audit

**Referee source:** `review/round20-gpt56-pro-harsh-11paper-2026-09-02@1e69f06bfa6df29cad985f6ccef6aa9559ac6a7b`  
**Revision branch:** `revision/round21-referee-positive-closure-11paper-2026-09-02`  
**Source tree inherited:** `1e69f06bfa6df29cad985f6ccef6aa9559ac6a7b`  
**Policy:** positive reconstruction; no theorem downgrade; no no-go substitution; no historical status word receives theorem credit.

## Audit rule

The audit covers the canonical recursive volume, `CM2_CURRENT_STATUS.md`,
`CM2_LATEST_STATUS.md`, all earlier historical audits, all paper-level
Round-Three through Round-Seventeen proof modules, the Round-Eleven local proof
packets, and the Round-Eighteen/Round-Twenty reports.

The CM2 control index itself records
`AllPositiveActualInstantiationGapsClosed: false` and `FormalCredit: 0`.  Its
latest-status file is explicitly fail-closed.  Therefore a historical label
such as `PROVED`, `CLOSED`, `PASS`, an implementation receipt, or a certificate
summary is never promoted to a theorem.  A mechanism is reused only when its
state space, quantifiers, operator domains, boundary conditions, estimates,
and noncircular dependency order are restated and proved in the active paper.

## Corpus conclusion

No previous derivation document closes the Round-Twenty objections as a
model-specific package.  The old corpus nevertheless contains valuable local
mechanisms.  The table records exactly what survives, what fails, and where the
new active proof repairs it.

| Paper | Reusable historical mechanism | Why it did not close Round Twenty | Round-Twenty-One active replacement |
|---|---|---|---|
| A1 | exact affine branch primitive; labelled biseam idea; full-port work; one-sided Bernoulli resolvents | individual closed gluing graphs were mistaken for a proper global quotient; dual trace direction was reversed; labelled currents could cancel after ambient summation; closability and FCLT estimates were only asserted | proper mapping torus of one labelled diffeomorphism; descended exact one-form; incidence-completed positive test jets and their Hilbert dual; fixed-fibre transpose derivative; explicit geometric projective estimate and trace-norm FCLT |
| A2 | parent-fold pairing; stable-curve anisotropic norms; periodic loops; returned UNI; near-opposition cancellation | countable branches were summed without inverse-Jacobian weights; the certificate was a summary rather than a mathematical implication; high-frequency constants depended on an unbounded derivative order selected after the split | Jacobian-weighted branch theorem; finite geometric continuation proof of four periodic differences and common-suffix UNI; fixed two-coordinate branchwise coarea bound; exhaustive four-dimensional raw Fourier theorem |
| A3 | exact Gibbs entropy representation; recession-profile idea; connector recovery architecture | the billiard was replaced by an unproved one-step countable edge chain with branchwise constant continuous marks; state, compactness, recovery, prefix rate, and clock contraction were not constructed | exact regular conditional history kernel retaining the continuous branch point and complete excursion; proper marked Polish completion; stopped entropy chain rule; explicit good rates; legal finite-memory recovery; collision/physical-time and conditional Laplace principles |
| A4 | history kernel; Doob transform; Poisson equation; unresolved-initial-data forcing; compressed-resolvent algebra | summable variation was upgraded to exponential without proof; drift/minorization and operator gap were named; source multiplication changed weights; scalar Fourier estimates were promoted to an operator renewal theorem; transmission-zero promotion had no finite termination argument | stable-holonomy proof of exponential variation; derived power drift and synchronized minorization; direct weighted-Lipschitz operator contraction; fixed-space analytic source ball; induced-operator renewal factorization; simultaneous finite Jordan transmission closure and inverse-Laplace memory bound |
| B1 | positive exact-number formulation; source-dependent saddle; cell exposure; coefficient extraction architecture | only four conditional derivatives were available while `O(N)` integrations by parts were taken; velocity integration missed position constraints; shell and relative-error regimes were conflated | quotient constraint space; fixed-size full-rank blocks using position and velocity coarea coordinates; fixed derivative order in each sequential block; mixed lattice--continuous shell theorem; joint activity/constraint saddle extraction with inserted-source uniformity |
| B2 | Green trace orientation; causal precontact zero set; real reflected future; collision entropy action | the displayed genealogy bound retained `k!` but the convergence proof dropped it; global rank and trace compactness were unproved; smoothing ignored the nonlinear map `f\mapsto A_f`; a Poisson compensator was used as a finite-volume deterministic-contact likelihood | singular-boundary nonconcentration and closed trace graph; compact analytic rank stratification; `1/k!` built into the connected coefficient and Catalan majorant; controlled Boltzmann positive recovery; exact initial-law exponential tilt followed by limiting Legendre identification; full GC/MC LDPs |
| B3 | single collision-noise convention; balance gauge; covariance-first principle; Lax--Milgram architecture | a cutoff collision gap was falsely promoted to `H^1_v`; nuclearity, stopping-time tightness, and microscopic covariance were absent; global convexity was assumed despite quadratic `A_f` | cutoff weighted microscopic `L^2` graph coercivity; nonautonomous Kawashima estimate and closed range; explicit Hilbert--Schmidt nuclear scale; localized connected cumulants and Aldous bounds; Gaussian process construction; positive exponential balance chart and nonconvex second epi-derivative |
| B4 | law/hierarchy typing; Nisio DPP; graph-core and diagonal approximation ideas | the linear pseudo-resolvent identity was applied to a nonlinear supremum map; compactness, transfer, hierarchy reconstruction, corrector boundary domain, and Trotter--Kato conditions were not proved | defined weighted kinetic state/action topology; positive same-multiplier controlled evolution; energy-shell strong continuity; correct implicit nonlinear resolvent relation and maximal dissipative graph; absolute Janossy inversion; exact specular terminal corrector; nonuniform-exponent diagonal and half-relaxed semigroup convergence |
| C1 | unnormalized evidence; positive-evidence posterior charts; finite-coordinate idea; score statistics | transition and observation were conflated; hidden-state domination was omitted; smoothing atomic observations was unsupported; zero evidence had no state; DPP hypotheses were missing; fixed-experiment QMD/score CLT was promoted to triangular-array LAN and BvM | separate hidden transition and observation; lattice/atomic/continuous stratified dominating measure; model-derived reachable compact dominated chart; explicit cemetery null convention; Feller belief DPP and selectors; direct third-order triangular-array likelihood expansion; uniform tests, posterior contraction, and BvM |
| C2 | strict/strong distinction; transported Hilbert metric; form compression; likelihood martingale | the topology had no seminorm definition or weighted dual proof; constants were excluded using an unassumed invariant measure; platform form hypotheses and Livšic/annihilator results were unverified; fixed-time conditional convergence was promoted to process optional projection and stochastic exponential; morphisms encoded conclusions | explicit weighted strict seminorms and dual theorem; platform invariant probabilities; verified A4/B3/B4 type-(B) forms; form Schur theorem; constructive countable-history Livšic and hard-sphere closed-range annihilator; finite-dimensional plus Aldous changing-filtration theorem; innovation representation; data-only contraction definition and proved examples |
| D1 | exact phase-cost sign; elementary finite-mixture LDP; local complex-leading-term architecture | phases were assumed rather than disintegrated from the original law; `(x,\rho)` was insufficient; domination was missing; separately optimized component values were combined; zero-free dominance was assumed; Gaussian scaling and tie exponent were wrong | finite-volume Borel phase events from separated order-parameter minima; exact disintegration and component local asymptotics; full phase-conditioned belief vector; common C1 likelihood; one shared policy optimized outside the sum; upstream-derived complex dominance; corrected labelled centered Gaussian variable and complete subexponential tie constants |

## New mathematical tools introduced in Round Twenty One

1. **Incidence-dual current calculus:** traces are applied on a positive
   Sobolev test-jet complex and only then transposed to currents.
2. **Proper one-diffeomorphism suspension lemma:** the mapping-torus equivalence
   relation is proved closed and proper and the primitive is descended at the
   one-form level.
3. **Weighted countable-branch complexity theorem:** inverse Jacobians, roof
   derivatives, and radius derivatives are summed in one exponential return
   estimate.
4. **Two-coordinate returned coarea tail:** a fixed number of branchwise
   integrations supplies an integrable raw Fourier tail without derivative
   constants depending on the frequency split.
5. **Exact continuous marked-history kernel:** complete past, current unstable
   coordinate, and full physical excursion form the reference Markov state.
6. **Simultaneous Jordan transmission closure:** all compression zeros in a
   strip are converted once into explicitly resolved Jordan chains.
7. **Normalized Catalan trajectory expansion:** the exponential-generating
   `1/k!` factor is part of the connected coefficient before estimation.
8. **Fixed-size conditional smoothing blocks:** arbitrary Fourier directions
   are regularized by a finite coarea block; the number of blocks, not the
   derivative order, grows with particle number.
9. **Cutoff transport--collision graph coercivity:** microscopic weighted
   `L^2` collision damping and macroscopic Kawashima control replace a false
   velocity-Sobolev gain.
10. **Nonconvex balanced second epi-derivative:** an implicit positive
    exponential chart gives exact nonlinear balance and second-order recovery.
11. **Implicit nonlinear resolvent proof:** a memoryless discounted stopping
    decomposition yields the accretive resolvent relation.
12. **Stratified dominated filtering:** counting and surface volume on genuine
    observation strata eliminate unsupported smoothing of atomic data.
13. **Innovation-stable changing-filtration theorem:** conditional-kernel
    convergence is combined with a stopping-time modulus and martingale
    representation.
14. **Shared-policy latent-phase Bellman principle:** component aggregation is
    performed for one common policy before optimization.

## Noncircular dependency order

The positive proof order is

```text
A1
A2 -> A3 -> A4
B2-GC -> B1 -> B2-MC -> B3 -> B4
(A3,A4,B1,B2,B3,B4) -> C1
(A3,A4,B3,B4,C1) -> C2
(A1,A2,A3,A4,B1,B2,B3,B4,C1,C2) -> D1
```

`B2-GC` uses no B1 theorem.  B1 extracts exact-number coefficients from the
already constructed source-uniform grand-canonical pressure.  Only then is the
microcanonical B2 theorem formed.  B3 constructs the Gaussian process before
identifying the second epi-derivative.  B4 uses the corrected B3 graph right
inverse only where a tangent graph theorem is actually needed; its positive
control transfer instead solves the controlled Boltzmann equation directly.
D1 contracts only component experiments already constructed upstream.

## Credit conclusion

Historical documents provide provenance and design ideas, not closure by
status.  Each Round-Twenty blocker is answered in the active source of the
corresponding paper.  No paper is removed, no advertised positive theorem is
replaced by a no-go theorem, and no genericity or conditional statement is used
as a substitute for the declared regular model class.  Repository checks and
compilation remain reproducibility gates and do not replace external
mathematical review.
