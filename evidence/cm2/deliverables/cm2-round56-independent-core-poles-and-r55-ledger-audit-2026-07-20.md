# CM2 Round 56 independent core-poles / Round-55 ledger audit

Date: 2026-07-20  
Scope: independent read-only audit of the Round-55 aggregate, its three leaves,
the strongest surviving Gate-1/2/3 evidence, and official 2025--2026 technology  
Strict verdict: **no Gate-1/2/3 structural pole is closed; Gate 4 and Gate 5
must not be promoted; CM2 remains `NO-GO_FOR_CLAIM`.  This audit does close one
validation-bookkeeping correction and one Gate-5 coupling-order correction.**

## 1. Decision summary

The strongest defensible Round-56 audit result is:

```text
Gate 1 physical full-cross/common vertex:        ALREADY CERTIFIED
Gate 1 same representative class-H + twisting:  NOT CERTIFIED

Gate 2 candidate affine cone-product layers:     7/7 (NON-OFFICIAL)
Gate 2 invariant stable-product layers:          0
Gate 2 immutable physical fields:                0/17

Gate 3 fixed free graph-current slots:            41,508
Gate 3 physical Q_s/R_s and MT_DQ:               NOT CERTIFIED

Gate 4 physical J_pair / first return:            NOT CERTIFIED
Gate 5 maturity / complete blocks:                10/18 / 0
complete composite gates:                         0/5
CM2:                                              NO-GO_FOR_CLAIM
```

No official theorem checked here directly constructs any of the three missing
physical interfaces.  The available results can become useful only after the
CM2-specific common carrier, IDs, operators and norms have been built.

All Gate-4/5 status statements in this document are **as of the pinned
Round-55 baseline**.  They are a read-only audit boundary and may be superseded
by a separately validated Round-56 Gate-4 or Gate-5 leaf; this document does
not prejudge or negate such a later append-only result.

Two append-only corrections are required:

1. the live Round-55 hostile-test total is `40+27+127=194`, not the stale
   aggregate `38+27+115=180` written in the Round-55 total report;
2. the synchronized coupling is a valid alternative witness, but it is not
   pointwise ordered below the normalized-product witness.  Only
   `d_best=min(d_sync,d_product)` is never worse and sometimes strictly better.

Neither correction changes a leaf manifest's mathematical verdict.  In
particular all three leaves still fail close on the same physical interfaces.

## 2. Frozen evidence read in full

The audit hash-pins the Round-55 aggregate and all three Round-55 leaf reports.
For the independent poles it also pins:

- the certified physical Gate-1 full-cross transition;
- the global class-`H`/twisting representative-separation theorem;
- the last nonlinear cross-term rate frontier;
- the actual Gate-2 R1 cone-product candidate and the immutable 17-field
  stable-quotient frontier;
- the finite-`s` common DQ carrier, the 41,508-slot free graph-current carrier,
  and the vector-current F17 frontier.

The exact dependency hashes are in the companion manifest.  No earlier file is
edited by this audit.

## 3. Round-55 aggregate corrections

### 3.1 Hostile-test count: `194`, not `180`

The Round-55 total report says

```text
38/38 + 27/27 + 115/115 = 180/180.
```

The current pinned leaf verifiers instead print

```text
hereditary terminal-Z leaf:  40/40
global image-recut leaf:     27/27
synchronized/delayed leaf:  127/127
total:                       194/194
```

All three self-tests exit zero.  All six certificate/verifier default entries
exit exactly `2`, meaning valid package plus open mathematics.  The three leaf
SHA ledgers pass in their declared relative-path conventions.

The observable file ordering is consistent with the aggregate report having
retained pre-final self-test counts while the leaf packages were finalized.  In
any event, the current fact is determined by executable replay: `194/194` is the
correct live total.  This is an **aggregate bookkeeping correction**, not a
manifest-integrity or analytic-theorem failure.

### 3.2 Synchronized coupling is not globally sharper by itself

Let `d_sync` be the same-source hit/miss cost and `d_product` the Round-54
normalized-product cost.  The Gate-5 leaf correctly contains two exact models:

```text
H=M=identity on the uniform two-point law:
    d_sync=0, d_product=1/2;

H=identity, M=flip on the uniform two-point law:
    d_sync=1, d_product=1/2.
```

Thus neither cost dominates the other.  The aggregate phrase “the synchronized
witness is strictly sharper” and the label `CERTIFIED_STRICTLY_SHARPER` are too
strong if read as `d_sync<=d_product`.  The exact replacement is

```text
SYNC_COUPLING: VALID_ALTERNATIVE_SAME_SOURCE_WITNESS
d_sync <= d_product: FALSE_IN_GENERAL
d_product <= d_sync: FALSE_IN_GENERAL
d_best=min(d_sync,d_product): NEVER_WORSE_AND_SOMETIMES_STRICT
```

This correction does not remove the valid synchronized BL estimate.  It also
does not supply the missing physical same-source decay rate and cannot pay any
positive F10 or cemetery mass.

## 4. Gate 1: the “physical common magnet” must be typed precisely

The geometry is no longer the first Gate-1 obstruction.  The frozen physical
24-collision transition already certifies:

```text
actual invariant graphs,
true transverse heteroclinic root,
four-face physical full crossing,
reverse inherited full-cross strip,
actual endpoint transition derivatives.
```

It would therefore be a regression to state that Gate 1 still lacks every
physical common vertex/full-cross object.  What remains open is the global
cocycle interface on one and the same representative.

The clean finite horseshoe has a faithful diagonal representative in Butler--Park
class `H`, but its same-axis twisting is exactly zero.  The compact logarithmic
representative has the selected nonzero wedges, but is refuted as class `H` on
the frozen connector common basic set.  The variable-diagonal construction
solves the stable and unstable Green equations separately.  For the combined
gauge `D=U_v L_u`, its remaining critical term is

```text
Z_n = R_-n(x)^(-1)
      v(sigma^-n y)
      [u(sigma^-n y)-u(sigma^-n x)]
      v(sigma^-n x).
```

Two sufficient routes are certified abstractly:

```text
R_-n(x)>=m^n,
|u(sigma^-n y)-u(sigma^-n x)|<=H omega^n d(x,y)^beta,
omega<m,
```

or exact uniform finite-memory cancellation.  No row of either type has been
instantiated on the physical finite SFT, and the selected wedges have not been
recomputed in that combined representative.

### 4.1 Latest official technology does not fill this object

- Kalinin--Sadovskaya, `arXiv:2604.13401v1`, proves cocycle cohomology/rigidity
  from conjugate periodic data under narrow-spectrum, constant-target,
  measurable-cohomology or bounded-conjugacy hypotheses.  It does not construct
  the CM2 common frame or verify the nonlinear cross-term rate.
- Wang, `arXiv:2606.29603v1`, proves global `C^{1+Holder}` periodic-data
  rigidity for `C^2` Anosov diffeomorphisms on tori with irreducible
  linearization and conjugate derivative data at every periodic orbit.  A
  singular billiard horseshoe with an unbuilt same-representative gauge is not
  such an input.
- Mohammadpour--Varandas, `arXiv:2508.05771v1`, starts with a fiber-bunched,
  `1`-typical cocycle.  Those are precisely properties still missing here, not
  conclusions that construct them.

Therefore no checked result closes Gate 1.  The shortest honest next
certificate is a physical `m,omega` row with `omega<m` (or an exact
finite-memory/coboundary cancellation), followed by same-representative replay
of all selected twisting wedges.

## 5. Gate 2: mixing theorems do not construct the return quotient

The strongest physical precursor is an actual positive-area R1 tile with an
affine cone-product coordinate system and exact affine area disintegration.
Its seven candidate layers are real, but the affine fibres have not been proved
to be invariant stable plaques.  The official Gate-2 count therefore remains
`0/17`.

The first missing physical object is still

```text
Lambda_A: a positive stable-saturated product base,
I_A:      a reference unstable interval,
pi^s:     physical stable projection,
J_hol:    conditional SRB stable-holonomy Jacobian.
```

Only after those records exist on one common label can one define connected
full-image return strips, inverse branches `h_a`, quotient density `rho`,
reverse weights `p_a`, transported matrices/endpoints, inverse-cylinder
diameters, native stopping, overshoot cemetery, off-diagonal projective
near-collision and the amplitude moment.

The two-dimensional first-return map before stable quotienting is invertible
modulo zero.  Refining its graph by any finite or countable path-key alphabet
leaves a Dirac reverse conditional and two-copy diagonal energy coefficient
one.  Label abundance is therefore not the missing randomness.

### 5.1 `arXiv:2607.06242v2` does not bypass the quotient

Liu--Lu--Shi--Wang, *Exponential mixing and Freidlin--Wentzell large deviation
principle for Markov cocycles*, `arXiv:2607.06242v2`, Theorem 2.2, considers
Feller transition probabilities on a Polish state space in an ergodic random
environment.  Its hypotheses `(H1)--(H4)` include Lyapunov/drift control, a
premetric contraction coupling, a martingale energy estimate, and total-
variation defects comparing the generalized coupling's second marginal to
the true transition law.  The conclusion is pullback/forward exponential
stability in a truncated Wasserstein metric.

This result is not a direct Gate-2 upgrade because it supplies none of:

```text
stable-saturated billiard product base or stable projection,
physical quotient density and reverse weights,
projective spatial Frostman/small-ball regularity,
same-label endpoint/cocycle typing,
native stopping and overshoot cemetery,
normalized stopped amplitude moment.
```

Moreover, verifying `(H1)--(H4)` for the physical inverse-branch/projective
operator would itself require a new generalized coupling estimate.  The
theorem is potentially useful **after** a physical kernel is built; it does
not build that kernel or turn base Wasserstein mixing into the required
projective Frostman estimate.

### 5.2 Fixed-law Furstenberg regularity is still the wrong carrier

Rush, `arXiv:2601.14061v1`, obtains the Frostman dimension of the Furstenberg
measure for one compactly supported probability law on `SL(2,R)` satisfying
strong irreducibility and proximality, using classical Le Page transfer
operators.  The CM2 reverse law is place dependent and its physical quotient
has not been constructed.  No state-dependent Markovization or same-label
stopped-tree theorem is stated there.

Therefore Gate 2 cannot be closed by citing a modern Markov/Furstenberg
theorem before materializing the 17-field common registry.

## 6. Gate 3: normal traces are not a dynamic anisotropic current norm

The positive Gate-3 stack is substantial but finite-depth:

```text
fixed stopped-endpoint mass carrier:       CERTIFIED
s=0 depth-two atlas modulo zero coarea:    CERTIFIED
fixed free graph-current carrier:           41,508 slots
finite additive two-cut identity:          CERTIFIED
physical source current injection:         constant 1
boundary-trace suffix TV multiplier:       constant 1
```

The free carrier is not a physical strong Banach triple.  The required maps

```text
R_s:B2_physical -> X2_hat,
Q_s:X0_hat      -> B0_physical,
Q_s P_hat_s R_s = P_s
```

are absent on the moving branch/component IDs.  So are finite-`s` future-
singularity continuation, strong-source restriction invariance, moving-test
convergence, all-field assembly and the growing-depth no-`|s|^-1` tail.

The current-valued source representation

```text
T_(K,B)(phi)=integral K dot grad(phi) dm+B(phi)
```

has injection norm one.  But for the area-preserving maps

```text
S_L=diag(L,L^-1),  K=e_1,
```

the source bulk cost is `1/L` and the pushed-forward bulk cost is `1`.
Thus determinant one and generic Piola naturality alone force a multiplier at
least `L`; they cannot yield the required uniform physical F17 suffix bound.

### 6.1 `arXiv:2607.11467v1` supplies trace calculus, not the suffix bound

De Cicco--Scilla, *Gauss-Green formulas for divergence measure tensor fields
on rough domains*, `arXiv:2607.11467v1`, Theorem 1.3, defines tensor/BV
pairings and normal traces for essentially bounded tensor fields with
measure divergence and proves Gauss--Green formulas on bounded finite-
perimeter sets.  This is a useful typing technology for tensor currents.

It does not state any billiard transfer-operator result, dynamic Piola
contraction, branch-ID cancellation, anisotropic observable inclusion,
moving-parameter differentiability, or numerical suffix multiplier.  It
therefore cannot promote F17 or `MT_DQ`.

Christopher Irving's `arXiv:2503.09536v2` similarly characterizes an
Arens--Eells normal-trace target and extension theory, but supplies no
same-ID killed intertwining or billiard dynamic estimate.

### 6.2 Current billiard response results remain narrower

Canestrari, `arXiv:2604.19671v2`, differentiates the conditional survival
measure of one fixed Sinai billiard with respect to the size of a boundary
hole at size zero.  Its scalar fixed-map hole perturbation does not provide
the finite-`s` moving-scatterer branch atlas or operator-norm `MT_DQ` required
here.

Demers--Liverani, `arXiv:2606.10155v1`, explicitly leaves as Problem 8.7 the
general cone-method loss-of-memory problem when characteristic restrictions
can concentrate the evolved density on atypical trajectories.  This is
consistent with, rather than a solution of, the present repeated
component-restriction interface.

Gate 3 therefore remains open.  The shortest route is to build one physical
anisotropic vector-current norm with bounded bulk and trace injections,
same-ID artificial-boundary cancellation, observable inclusion and a
billiard-specific directional Piola/coboundary bound, then install `R_s/Q_s`
and the finite-`s` common dynamic atlas.

## 7. Gate-4/5 nonpromotion audit (pinned Round-55 baseline only)

The Round-55 Gate-4 leaves are internally careful and remain valid only with
their declared typing:

```text
coarse terminal Z l1:          CERTIFIED
global connected-image cap:   CERTIFIED
natural-mesh path rule/join:   NOT CERTIFIED
physical J_pair and I_D:       NOT CERTIFIED
physical first return/q:       NOT CERTIFIED
```

This is not a claim about any independently produced Round-56 Gate-4 leaf.
If a later leaf pins the natural-mesh rule, metric and same-ID joins and passes
its own analytic/integrity audit, its newer status supersedes this baseline.

In particular a fixed image-recut cap does not decide whether the natural
mesh uses a path maximum or an additive timewise union, does not prove its
Kac-tower moment, and does not identify its cells with the coarse terminal
IDs.

For Gate 5:

```text
same-source sync coupling:     VALID ALTERNATIVE
physical sync decay rate:      NOT CERTIFIED
delayed collar recovery:       CERTIFIED CONDITIONAL
same physical trace law:       NOT CERTIFIED
same Round-42 operator:        NOT CERTIFIED
arbitrary level suffix horizon:NOT CERTIFIED
physical weak clearance tail:  NOT CERTIFIED
Gate-5 maturity:               10/18, complete blocks 0
```

The delayed theorem cannot be promoted merely from a formal inequality:
level `k` needs at least `k+1` compatible 9,148-collision blocks on the same
owner/operator record.  A fixed finite suffix does not provide this for
unbounded `k`.

## 8. Strict closeability and shortest next steps

| Gate | Can this audit close it? | Exact shortest new physical input |
|---|---|---|
| 1 | **No** | Instantiate `m,omega` with `omega<m` (or exact cancellation) on the actual clean SFT and replay twisting in that same gauge. |
| 2 | **No** | Build a positive invariant stable-saturated product base, stable projection and holonomy Jacobian; then materialize the common 17-field quotient/stopping registry. |
| 3 | **No** | Build the physical anisotropic vector-current norm and `R_s/Q_s`, plus a finite-`s` common future-singularity atlas and restriction/DQ estimates. |
| 4 | **No** | Freeze the natural-mesh path rule, metric ledger and same-ID terminal refinement; then prove `J_pair`, `J_cap` and a physical first return. |
| 5 | **No** | Prove a physical same-source rate or same-law weak clearance tail together with the same-operator and unbounded suffix-horizon joins; finish F10/F13/F14/F15/F17/F18. |

There is no honest “one citation away” closure among Gate 1, Gate 2 or Gate
3.  The next work should construct the missing physical carriers rather than
continue theorem-name substitution.

## 9. Official-source provenance

The following versioned official PDFs were streamed from `arxiv.org/pdf` and
hashed during this audit:

```text
2607.06242v2  037d2789745ce9e085cb8d404d1be70d5a804675630ea1351f8a3f7672c2abe6
2607.11467v1  f5232558bd958bf1628bb524623800fe631b8273cb10a75f292614fd74dfccba
2601.14061v1  fa1c64f3a17bcb5a2cee105549820f4b2326a5f0d5f16ddbdccbf7a1ba96e4be
2604.13401v1  bd62a5989838f9ba26a1c96b6b2bb165add3ee79f83cfa32f5883e4174c690e4
2606.29603v1  71d1f43cf3d2be39ec466e6e73af4fa21eba6e3fd60f31bdcab2ff323678a329
2606.10155v1  3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798
2604.19671v2  fc00f45a8ec6513763665bf8fa34569a95ca5d6d6b9fa5d90b7e1089fabd9004
```

Official links:

- <https://arxiv.org/abs/2607.06242v2>
- <https://arxiv.org/abs/2607.11467v1>
- <https://arxiv.org/abs/2601.14061v1>
- <https://arxiv.org/abs/2604.13401v1>
- <https://arxiv.org/abs/2606.29603v1>
- <https://arxiv.org/abs/2606.10155v1>
- <https://arxiv.org/abs/2604.19671v2>

## 10. Replay

```bash
python deliverables/cm2_round56_independent_core_poles_and_r55_ledger_audit_cert.py \
  --summary
python deliverables/cm2_round56_independent_core_poles_and_r55_ledger_audit_verifier.py \
  --integrity-only
python deliverables/cm2_round56_independent_core_poles_and_r55_ledger_audit_verifier.py \
  --replay
python deliverables/cm2_round56_independent_core_poles_and_r55_ledger_audit_verifier.py \
  --self-test

# Both default entries deliberately fail close with exit 2.
python deliverables/cm2_round56_independent_core_poles_and_r55_ledger_audit_cert.py
python deliverables/cm2_round56_independent_core_poles_and_r55_ledger_audit_verifier.py

cd deliverables
sha256sum -c \
  cm2-round56-independent-core-poles-and-r55-ledger-audit-2026-07-20.sha256
```

Exit `2` means that the audit package is valid while the composite claim is
not certified.  Integrity or semantic replay failure exits `1`.
