# Current Risk Register

Updated: 2026-07-11 CST

## R0. Dynamical versus positive response spaces

- Status: closed by a proved two-space architecture, not by asserting a false
  stronger gap.
- The centered Demers--Zhang spectral gap and Neumann resolvent act on the
  transported dynamical strong bundle `B_U`.
- The positive flux-seed completion `D_U` contains rescaled phase derivatives
  and physical face restrictions.  Transfer invariance and exponential
  contraction in that stronger norm do not follow from the Demers--Zhang
  theorem and are not claimed.
- Proposition 3.5, the positive-waiting primitive, correlation susceptibility,
  second-order strong remainder, radial reset, and the main theorem now use
  `B_U` consistently.  The base regular coordinate is the Banach-sum weak
  space `D_U^{w,(0)}`, into which `B_U` embeds.
- Moving-face traces use a separate `L^infinity`-anchored weighted primitive
  domain, not bare `B_U`.  Its target records every canonical backward
  singularity/homogeneity cut.  The multiplicative weight is the actual
  one-step `C^r` pullback norm and therefore absorbs, rather than suppresses,
  polynomial strip loss.  Admissible refinements form an isometric direct
  limit.  The anchor proves closability, and radial invariant jets,
  fixed-length assembled currents/primitives, and tubular extensions have
  proved membership.  No trace continuity from `B_U`, and no transfer
  invariance of the primitive domain, is claimed.

## R1. Radial reset and R3 leakage

- Status: closed for the claimed scalar assembly-first theorem.
- The R3-dependent fixed-length lemma remains a separate generic statement and
  is not used for radial reset.
- The manuscript defines the physical-cutoff multiplier on regular, face,
  point/jet, and terminal coefficient sectors.  For each fixed cutoff it is
  bounded, intertwines with realization, preserves the realization kernel,
  descends to the quotient, and passes from finite-support tuples to the
  countable completion.  Realization and total-current assembly therefore
  commute exactly with the common physical cutoff on a completed historical
  class.
- The assembled current is `(I-L^N)rho_j`.  The radial flux jets are bounded,
  `L^N` preserves `L^infinity`, and the grazing flux has mass
  `O(2^{-4M})`.  This gives the reset tail uniformly in the waiting length
  without R3.
- Remaining boundary: no equality with, or convergence of, the raw historical
  label-resolved terminal state is claimed.

## R2. Block-flux graph domain

- Status: theorem-level overclaim removed; the calculation is an unnumbered
  appendix remark.
- The auxiliary norm has the correct base term `N_{m+2}^flux`; level three
  therefore embeds in `D_U^(3)=N_5^flux`.
- It records the grouped face and regular weak/holonomy block estimates in one
  fixed radial blown-up atlas.
- No chart/refinement equivalence, completed operator extension, transfer
  invariance, next-event return, recursive module structure, or S1 is claimed.
- Remaining boundary: a reusable Banach-module theorem would require exactly
  those missing atlas/refinement and multiplier/holonomy estimates.

## R3. Prescribed source and transport regularity

- Status: retained only as an exact-conjugacy consistency proposition, not
  closed for nonconjugate radial inflation.
- In a flux-conjugate family, choose a nonconstant physical observable first
  and set `g_s=(a_s-<rho_s,a_s>)rho_s`.  A common rigid table translation
  with `a(q,v)=omega dot v` is explicit and nonzero.
- Only after the source is fixed is
  `h_0=(I-L_0)^{-1}g_0` introduced.  Conjugacy transports `h_0` and proves
  the Poisson identity.
- For common rigid translation, the exact conjugacy is chosen as the
  Banach-bundle trivialization.  The fixed-fiber operator, source, and
  primitive are constant, so `q_1=q_2=0`, terminal coordinates and the strong
  remainder vanish identically, and the infinite susceptibility is `C^J`.
  No differentiability of a general anisotropic distribution under transport
  is inferred.
- Remaining boundary: no moving face occurs in this example.  It does not solve
  the genuinely nonconjugate prescribed radial-source problem.  On the actual
  weighted primitive/Poisson-pullback domains, the localized
  gluing map is onto arbitrary smooth face profiles, so its admissible kernel
  has infinite codimension and a bounded complement on fixed compact trace
  subarcs.
- After recovery through order m-1, the localized order-m face
  coefficient depends affinely on the next source jet through m G delta g;
  each finite order therefore imposes another affine infinite-codimension
  constraint.
- At the base table `rho_0=1`, the Poisson-independent weighted
  local-potential class already has a split-surjective defect map.  Separately,
  centering defines the pullback correlation graph class; on that graph
  topology the localized observable defect is split surjective and the
  complemented affine obstruction repeats jet by jet.  No Baire claim is made
  for all ordinary `C^r` observables.
- Time-reversal/parity alone does not force that kernel condition unless it
  identifies the two branch traces pointwise.  Resolvent projection into the
  kernel is possible using the bounded right inverse, but is
  Poisson-primitive-defined, so neither route
  supplies the missing independent source.
- More strongly, for a finite geometric symmetry with a free orbit of moving
  face subarcs, projecting the right inverse by the central idempotent of any
  irreducible representation remains onto inside every isotypic subspace.  A
  symmetry-based positive theorem therefore needs
  a pointwise face stabilizer Ward identity, not parity alone.
- The remaining stabilizer exception is ruled out for finite physical torus
  isometries on regular grazing faces by strict convexity and scatterer
  separation; no open grazing subarc can be fixed pointwise.
- A proposed local Noether/Ward primitive must satisfy every periodic-orbit
  sum condition.  These functionals have arbitrarily large finite rank;
  invariant charges give zero source, while charge increments are exact
  currents already separated from the missing prescribed class.
- Face gluing and periodic-orbit Ward sums cannot be traded against one
  another.  Their joint defect operator is split onto the direct sum of the
  face-profile space and every finite orbit-sum space, so a proposed source
  must satisfy both independent families of constraints.
- A finite-label finite-memory Ward ansatz cannot evade this boundary on a
  finite strongly connected regular itinerary subsystem: the periodic tests
  force it to be a graph coboundary, hence an exact-current benchmark.

## R4. Radial higher order and genericity

- The isolated circular second transfer letter contains
  `partial_s^2 alpha ~ u^{-6}`, leaving a nonintegrable `u^{-3}` flux
  coefficient.
- A fourth-order moving grazing germ creates a localized endpoint atom unless
  a complete assembled identity cancels it.
- Scalar total-current cancellation cannot imply label-resolved S1, and a
  centered periodic point atom rules out generic source-resolvent decay.
- Hence every positive nonconjugate higher-order result must be
  source/assembly specific.

## R5. Presentation and continuous time

- The actual radial package now precedes the appendices.  Appendix A contains
  the auxiliary no-go results; Appendix B begins with the source-module
  construction used for the reset theorem and then
  separates the genuinely conditional S1--S3 propagation subsection, which
  is explicitly not used in the radial theorem.
- Fixed-table BDL material has been removed from the collision/spectral main
  line and compressed into the final logical-boundary section.
- Only the fixed-table citation correspondence and three moving-flow
  obstructions remain.  No moving-family flow theorem, common graph domain,
  symbol estimate, or derivative-loss budget is asserted.
