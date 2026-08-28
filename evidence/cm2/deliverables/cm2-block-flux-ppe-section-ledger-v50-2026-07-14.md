# CM2 v50 block/flux/PPE/section ledger

Date: 2026-07-14 (Asia/Shanghai)

Scope: continuation from frozen v49.  This ledger separates theorems proved
in v50 from sufficient interfaces that remain to be verified for the full
two-disk dynamics.  It does not call the fixed-section pilot a concrete CM2
nonvacuity theorem.

## 1. Direct/entry/exit block currents

The exact bounded-inducing identity remains

```text
P_c = A_c + B_c C_c,
Delta_s P = Delta_s A + (Delta_s B) C_0 + B_s Delta_s C.
```

v50 closes a topology missing from v49.  Weak convergence of `Delta_s C` and
separate weak convergence of `Delta_s B` do not control the moving product
`B_s Delta_s C`.  The typed gluing theorem requires strong continuity of the
adjoint test action

```text
||(B_s^* - B_0^*) phi||_{T_W} -> 0.
```

Under the recorded block certificate the raw induced current is exactly

```text
J_P(h,phi) = J_A(h,phi) + J_B(C_0 h,phi) + J_C(h,B_0^* phi).
```

No intermediate centering is allowed on the white-disk phase.  Centering is
performed only after the three raw currents and their boundary traces have
been assembled.

The manuscript includes an explicit weighted-l2 countermodel showing that
separate weak convergence is insufficient.  It also proves the Reynolds
switching-current formula on persistent regular charts and the regular
tangency trace identity: the direct and two-step traces agree at a tangent
white contact, so their artificial boundary currents cancel only after the
`B_0` trace is applied.

A query-independent diagonal occurrence construction now gives exact
coefficient pushforward, exact scalar-current matching on every record
restriction, and `m <= q` with constant one, provided the physical MPD and
its predictable envelope have already been built.  The density floor
`C_occ >= 1` is explicit.

What is actually instantiated for the pilot: a positive-mass compact core on
which the entry map, reflection, and reversed exit map are analytic and
uniformly transverse.  This supplies genuine local entry/exit DQ currents
and, for every predeclared smooth carrier fixed before the final query,
identity occurrence/source matching through two atomic entry/exit types on
fixed TV-measure source spaces and fixed `C^1` test spaces.  The current
operator is defined on the whole source space, not only on the selected
carrier.  This local theorem does not identify those atoms with the
pre-existing complete tree law; the global physical/tree Radon--Nikodym
record remains a gate.  It does not supply the full direct
switching atlas, grazing/endpoint/lift boundary tightness, or the global
propagated envelope.

## 2. Positive flux to an initial standard family

On the compact sub-cylinder

```text
|y| <= 1/200, |w| <= 1/200, |s| <= 1/800,
phi = arctan(w), tau = t_-(y,w,s),
```

the incoming collision map satisfies

```text
1/4 < |dr_+/dphi| < 50/99,
823/100 < dphi_+/dr_+ < 41/4.
```

The positive incidence multiplied by the constant-sign impact mark has exact
image density

```text
rho_ent(r_+) = N_M^{-1} cos(phi) (partial_s t)/(2 R tau).
```

It is uniformly positive, bounded, and log-Lipschitz.  Compactness gives
uniform curvature and an upper length bound; a uniformly finite equal-length
subdivision gives a positive component-length floor and a uniform boundary
functional.  Thus each fixed `(y,s)` fibre is a uniform initial standard
family.  The continuous `(y,s)` mixture is kept as an outer occurrence
kernel.  It is not silently identified with the total-variation completion
of countably supported standard pairs; only the separate weak-* regular
measure class of Canestrari is available for the phase-space mixture.
In Canestrari's parameter convention the boundary constant is
`B_* = ell_sf^{-1}` and the graph-curvature constant is the separately
recorded `D_*`; the local slope cone is fixed as `8 < dphi/dr < 11`.

## 3. Hereditary weighted boundary complexity

Family-average growth does not imply a rare-cell normalized estimate.  v50
adds a two-curve countermodel: the global boundary functional remains
uniformly bounded while the cell selecting a curve of length `epsilon` has
normalized boundary mark `epsilon^{-1}`.

A sufficient cellwise bridge is proved.  On every positive record cell `C`,
let `X` be the full charged nonnegative `Z` mark.  For the bare boundary
functional, choosing a component by its true family mass gives
`X=1/|W_J|`; all other recovery/homogeneity factors must be included before
the following condition is invoked.  If

```text
E_C X <= B,          E_C W^p <= K_p,
p > 1,               chi p' < 1,
```

then

```text
E_C[W X^chi]
 <= K_p^(1/p) (1 + chi p' B/(1-chi p'))^(1/p').
```

This proves hereditary `W Z^chi` once the same two conditional inputs are
verified separately on every global, shallow, and stopped-deep law.  Existing
growth lemmas control family averages; they do not provide this recordwise
quantifier.

## 4. All-depth jets and weighted PPE

v50 isolates an exact affine branch recurrence and its extended Faa di Bruno
jet cocycle.  An orientation-recorded invariant cone, a terminal seed with a
nonzero top derivative, and a one-step top-coordinate lower bound give the
all-depth estimate

```text
|partial_z^D X^[N,L]| >= c_0 exp(-a_0 k).
```

This is a genuine induction theorem; finite-depth numerical sampling is not
used as an all-depth substitute.

On retained good components, the weighted finite-type estimate loses no
second component-count factor because the component density sum is already
part of the exact PPE amplitude mark.  The remaining PPE2 inputs are a
tilted bad-mass estimate and a conditional moment of the amplitude mark.  A
noncircular sufficient route is a Foster--Lyapunov field restarted on each
global/shallow/stopped-deep parent.  The first-hit record is disintegrated
first, and every accepted, missed, and cemetery record is continued to the
same deterministic prescribed depth `N`:

```text
E[V_{t+1}|F_t] <= rho V_t + C, rho < 1,
```

with `V_N` dominating both the required amplitude moment and exponentially
tilted bad mass.  The proof uses the fixed-time estimate at `N`; it does not
apply a pointwise drift estimate at a randomly selected terminal time.  A
countable finite-operation-word registry makes the amplitude index
standard-Borel and query-independent when every actual amplitude is generated
by a uniquely recorded finite word and the record-to-word map is Borel on
the whole countable disjoint-union registry (equivalently, the length map and
the restrictions to its Borel strata are Borel).

The cone induction gives `c_0 exp(-a_0 k)`.  A unit-prefactor
`exp(-a_jet k)` gate with `a_jet>a_0` is used only beyond the explicit seed
threshold; the small-`r` window is reduced accordingly, while the remaining
finite depths retain `c_0` in the sublevel constant.

PPE3 still requires record-preserving retained continuations and a resolving
buffer.  PPE4 still requires parameter-uniform cones, drift, registry, and
moving-cut estimates up to `N <= L(s)`.  The countermodel
`X_s^[N]=(1-s exp(aN)) z^D` shows that an all-depth cone at `s=0` alone is
insufficient.

## 5. Fixed section versus the full collision map

Stenlund's depth-{1,2} identity links the fixed section `M` to the enlarged
section `M* = M disjoint_union W`; it does not identify either with the
solid-boundary collision section `N = G disjoint_union W`.

For a height-two extension v50 proves the exact Kac centering identity

```text
S(h-mu_hat(h))
 = S h - r mu_hat(h)
 = S h - mu(S h) + (r_bar-r) mu_hat(h).
```

The last term is a genuine roof correction.  It also proves the exact block
resolvent with

```text
R(z)=zA+z^2BC, D(z)=I-R(z).
```

A constant-roof-two tower over a mixing base has the phase eigenfunction
`(-1)^level`; this gives nondecaying full correlations although its induced
observable vanishes.  Thus bounded roof and base CM2 cannot transfer CM2.

The sufficient phase-lift theorem requires: exact common-refinement/Kac
typing, typed block currents, removal of the invariant pole in an
exponentially weighted operator Wiener algebra, no nontrivial unit-circle
return resonance, and bounded phase test/current lifts.  These hypotheses
give a two-variable Wiener response and hence absolute CM2 summability.
The base return resolvent has singular coefficient
`Pi_M/(r_bar(1-z))`; only after the block prefix/suffix reconstruction is the
full phase coefficient `Pi_hat/(1-z)`.  The differentiated induced observable
keeps all four terms

```text
dot(S) h + S dot(h) - dot(r) mu_hat(h)
             - r d_s[mu_hat_s(h_s)]|_0
```

as separately typed current/test contributions.

`SECTION_FULL_CM2` is therefore split into five falsifiable gates:
`COMMON_REFINEMENT`, `RETURN_BLOCK_DQ`, `KAC_CENTERING`,
`RETURN_WIENER_APERIODICITY`, and `PHASE_TEST_NORM_LIFT`.

## 6. Targeted literature check through 2026-07-14

- Canestrari, arXiv:2604.19671v2, supplies the vertical-fibre standard-family
  construction and weak-* initial regular measures used locally.  Its growth
  theorem starts after a regular entry object has been built and controls a
  family average, not every record-conditioned rare cell.
- Stenlund supplies the common fixed section/law, reversibility, one-white-hit
  geometry, and depth-{1,2} enlarged-section representation.  It does not
  differentiate the return blocks or transfer response between the two
  collision sections.
- Melbourne--Terhesiu, arXiv:1404.2508v2, supplies an operator-renewal/Schur
  template, not moving billiard boundary currents or a differentiated
  Poincare-section CM2 theorem.
- Galatolo--Lucarini, arXiv:2603.19509v3, works on a fixed transfer-operator
  sequence space and does not identify different singular sections.
- Friedland, arXiv:2606.24823, can shorten a scalar finite-order exponential
  polynomial sublevel estimate only after bounded exponential order is
  proved; it does not construct the billiard jet cone or weighted amplitude
  moments.
- Bajovic--Petkovic, arXiv:2607.11180v1 (13 July 2026), treats monotone
  shrinking targets and waiting-time exponents.  It does not control
  stopped-parent amplitude tilts or hereditary boundary complexity.
- Duvall, arXiv:2606.27488v1, proves survivor-conditioned renewal and reward
  bounds for open intermittent maps through a killed induced operator.  Its
  one-dimensional hypotheses do not construct billiard moving-flux entry or
  recordwise weighted boundary moments.
- A targeted arXiv query on 14 July 2026 found no newer dispersing-billiard
  response result beyond Canestrari's small-hole paper that closes the
  moving-scatterer block-current or section-transfer gates.

## 7. Remaining shortest path

1. Extend the local entry/exit theorem to a global recorded direct/entry/exit
   atlas and prove all genuine-boundary tightness and propagated envelope
   bounds.
2. Prove cellwise standard-family regularity and conditional `L^p` weight
   bounds on every global/shallow/stopped-deep record law.
3. Verify the exact jet recurrence/cone, Lyapunov drift, PPE3 continuation,
   and PPE4 moving-parameter window on the same stopped tree.
4. Build the common refinement with the solid-boundary section and verify
   return-word DQ, Kac centering currents, Wiener aperiodicity, and the phase
   test-norm lift.

No cited result currently supplies these four global verifications.  v50
therefore advances each frontier by a proved local theorem or an exact
noncircular sufficient criterion while keeping the remaining dynamical
inputs explicit.
