# Fixed-section moving-billiard primitive-gate audit (v48)

Date: 2026-07-14.  Scope: deterministic relative translation of the white
disk in Stenlund's fixed-section two-disk model, with
`Rbar=0.36`, `R=0.16`, and `epsilon=0.005`.

## What is now genuinely verified

1. **Exact geometric nonemptiness.**  The rational inequalities for boundary
   clearance, diagonal passage, finite-horizon lower margin, blocking, and the
   free-zone radius have strictly positive certified margins.  These are
   checked by `cm2_fixed_section_geometry_cert.py` without floating-point
   decisions.

2. **One common collision section and one common probability.**  Stenlund,
   Sections 2.3--2.4, defines every admissible return map on the same fixed
   section, proves that a return either misses the white disk or hits it
   exactly once, and records the common invariant probability
   `M0^{-1} cos(phi) dr dphi` and reversibility.  Therefore a deterministic
   analytic path `c(s)=c0+s v` has constant component masses, base dynamical
   RN density one, and a genuine raw two-copy law `mu x mu`.  This statement
   deliberately stops before any moving-face conditioning.

3. **Exact clean one-return impact/coarea primitive.**  On a non-grazing
   one-hit chart,
   `G(t,s)=|q0+t u-c(s)|^2-R^2` gives
   `t_s=(n.v)/(n.u)` and coarea density
   `[2R |n.u|]^{-1}`.  Hence on `|n.u|>=g` there is an explicit finite positive
   incidence envelope and a signed impact-time mark bounded by `|v|/g`.
   `cm2_fixed_section_impact_cert.py` checks the polynomial identities exactly.

These are real primitive gates for one nontrivial moving-scatterer pilot.  They
do **not** yet amount to the full concrete CM2 theorem.

## What the primary literature supplies, and where it stops

- **Stenlund fixed-section model** (arXiv:1210.0902): common section, common
  invariant law, reversibility, uniformly bounded return time, and at most one
  white-disk hit per return.  It supplies recovery/coupling architecture for
  refreshed or sequential maps, but not the derivative occurrence current or
  prescribed-depth polynomial jet.
- **Moving scatterers / sequential billiards** (arXiv:1210.0011;
  arXiv:2104.06947; arXiv:2502.07765): uniform hyperbolicity, loss of memory,
  projective cones, and sequential limit-theorem technology.  These are useful
  after entry into the regular family/cone; they do not construct the moving
  face source or prove exact physical/source matching.
- **Canestrari, small holes** (arXiv:2604.19671v2): invariance and conditional
  mixing of standard families, with the boundary functional
  `Z(G)=sum p_j/|W_j|`, after an initial regular standard family is already
  available.  This shortens the FS2 recovery and Z-recursion step but does not
  prove that the translated collision-face flux is such an entry family.

The arXiv searches repeated on 2026-07-14 found no newer paper that closes the
combination of moving-face coarea/current, exact source matching, hereditary
rare-cell moments, and all-depth PPE for this class.

## Remaining decisive all-depth gates

1. Identify the full differentiated transfer-operator occurrence current with
   the clean geometric graph current plus a recorded grazing/deep remainder.
2. Push that current into a regular flux standard family with a uniform
   long-side and distortion ledger.
3. Prove the cellwise estimate
   `integral_C W Z^chi dq <= K q(C)` simultaneously for global, shallow, and
   stopped-deep record cells.  An unconditional moment is insufficient.
4. Prove an invariant terminal native-z jet cone at every depth, then the
   fully typed PPE2--PPE4 amplitude estimates.
5. Construct, rather than assume, the exact recordwise physical/source and
   current matching.

## Shortest next proof attack

Work on clean one-return cylinders first.  Use the explicit coarea density and
`|t_s|<=|v|/g` to build the source envelope before invoking standard-family
technology.  Charge grazing boxes to the immutable depth variable.  The first
genuinely new estimate to target is a uniform flux-entry bound on every clean
cylinder; once that is proved, Canestrari's standard-family recursion can be
used without crossing its theorem boundary.  In parallel, the all-depth jet
must be proved symbolically/conically, not by finite-depth numerical sampling.
