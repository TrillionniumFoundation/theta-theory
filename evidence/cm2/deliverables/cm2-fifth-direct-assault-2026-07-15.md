# CM2 fifth direct assault: resonant holonomy obstruction, full-mass scale gap, and refined event rows

Date: 2026-07-15 (Asia/Shanghai)  
Execution: direct interactive work only; no CM2 cron or detached scheduler  
Frozen inputs: v51/v52 and their manifests were read but not edited

## Verdict

**Unconditional CM2 remains `NO-GO FOR CLAIM`.**  Under the strict composite
typing used throughout the project, the five main gates remain **0/5 fully
closed**.  This pass nevertheless changes the proof frontier in three
material ways:

1. the natural QNL canonical-holonomy route is now closed-negative by an
   exact cubic resonance, rather than merely lacking fiber bunching;
2. the physical size of Gate 2's missing stable saturation and return
   alphabet is now bounded from below; and
3. Gate 3's unresolved parameter area is reduced by more than 70%, while
   exact physical scalar pairing is promoted to all 64 refined certified
   components.

| gate | strongest certified layer after this pass | strict remaining obstruction | verdict |
|---|---|---|---:|
| 1. common magnet / twisting | actual common vertex, four-face full-cross, finite 96-collision shadow and four wedges | frozen natural QNL canonical stable holonomy provably diverges; a genuinely different cohomology/coding or applicable non-FB theorem is absent | **OPEN** |
| 2. physical SRB/PPE | two local physical crossings, direct stopped-energy theorem, exact SRB mass audit | interval-indexed stable saturation, full-mass quotient, actual tail PPE, endpoints and amplitude registry | **OPEN** |
| 3. global event/DQ | refined 64-component bulk, source-grazing normal forms, 5,906 exact `Jx` coarea pairs | remaining first/miss/grazing collars, seam quotient, maximal rows and arbitrary-test DQ | **OPEN** |
| 4. same-occurrence `q` | completed-row two-view/common-`m`/single-charge schema on every refined certified component | numeric forward/reverse costs and controlled stopped-parent recovery on the global physical partition | **OPEN** |
| 5. full-boundary transfer | finite Kac algebra, bounded-Borel singular typing, component phase gcd one, refined-bulk scalar roof cancellation | typed global singular currents, distortion/cut/test constants and all CM2 norm lifts | **OPEN** |

## 1. Gate 1: exact resonance closes the frozen natural holonomy route

The literal geometry from the preceding passes remains certified: the actual
local QNL unstable and connector stable graphs meet transversely, their
24-collision transition has a four-face full-cross, and the 96-collision
finite shadow has four nonzero transported wedges.  This pass audits the
missing canonical QNL transport itself.

Let `F` denote the exact gray--white--gray QNL return in its eigencoordinates,
with

```text
DF(0)=diag(lambda,mu),  lambda*mu=1,
lambda>1, 0<mu<1.
```

Exact Taylor reconstruction proves

```text
all quadratic derivatives of F at 0 vanish,
F2_xyy(0)/mu = -325/72.
```

For a nonzero sufficiently local point `z` on the QNL stable manifold, put

```text
H_n=DF^n(z)^(-1)DF^n(0).
```

The exact cocycle order is

```text
H_n^(-1)H_(n+1)=A^(-n)B_n^(-1)AA^n,
```

and its lower-left entry has the strict limit

\[
 \lim_{n\to\infty}(H_n^{-1}H_{n+1})_{21}
 =\frac{325}{144}c(z)^2>0.
\]

Hence `H_n` cannot converge.  An independent audit rechecked the matrix
order, the exact coefficient, the stable asymptotic, the even-time passage
to the original collision cocycle, and the finite-prefix passage from a
global homoclinic tail.

Consequences must be kept sharply typed:

- Park--Piraino on the two frozen natural codings is `NO-GO` because the
  periodic fiber-bunching spectral obstruction persists under same-coding
  Hölder conjugacy;
- the Butler--Park class-`H` canonical-limit condition fails for the faithful
  frozen natural representative;
- the finite shadow and its wedges stay certified, but are not a QNL
  canonical holonomy loop;
- an arbitrary point-dependent Hölder cohomology, another non-fiber-bunched
  theorem, or a genuinely alternative coding/transport is neither certified
  nor refuted by this calculation.

The literature audit through 2026-07-15 found no theorem that accepts this
singular billiard derivative, dispenses with the failed canonical limit, and
promotes the finite shadow to the required projective spectral statement.

Evidence:

- `cm2-gate1-canonical-holonomy-resonance-assault-2026-07-15.md`;
- `cm2_gate1_canonical_holonomy_resonance_cert.py`.

## 2. Gate 2: exact scale and mass deficit

The preceding leaf-level result was not merely numerical: the actual stable
leaf of the 96-collision point reaches the common face and a positive-width
96-word physical crossing is certified.  What remains is an interval-indexed
family of compatible stable plaques with a physical holonomy Jacobian.

The new 900-bit audit quantifies the gap.  The stable endpoint separation is
strictly greater than `8.29e-15`, while the current uniform physical tube has
stable half-height `10^-80`.  Therefore

```text
endpoint-separation / certified tube halfheight > 8.29e65,
common-rectangle halfheight / tube halfheight   = 4.2e65.
```

The problem is not localization of the one certified crossing; its
uncertainty is below `8.53e-172`.  The missing object is uniform correlated
continuation over a positive unstable interval.

There is also an exact physical mass obstruction to calling the two current
raw strips a quotient partition.  Collision SRB is constant in `(s,p)`, and
the QNL strip contributes exactly

\[
 \frac{27}{280}=0.09642857\ldots
\]

of the common rectangle.  Even charging the entire 96-word loop rectangle
adds less than `4.54e-119`.  Thus

```text
current enumerated physical fraction < 0.097,
unregistered physical complement      > 0.903.
```

At least that complement still needs a first-return/singularity/component
registry.  The result does not rule out a countable completion; it proves
that the branches, physical weights and tail estimates cannot be omitted.

Evidence:

- `cm2-gate2-stable-saturation-scale-gap-assault-2026-07-15.md`;
- `cm2_gate2_stable_saturation_scale_gap_cert.py`.

## 3. Gate 3: refined collars and exact 64-component scalar pairing

The depth-nine 192-bit atlas uses the same complete first-hit and 162-lift
miss registry as its predecessor.  Two exact identities remove interval
dependency that had been misclassified as physical uncertainty:

\[
 c_p^2+p^2=1,
 \qquad
 \operatorname{sign}(\eta\varepsilon c_pu_y/\ell)
 =\operatorname{sign}(\eta\varepsilon u_y)
\]

on outgoing rows.  The resulting partition is

| class | boxes | exact parameter area |
|---|---:|---:|
| physical immutable subrow | 11,812 | `5569/25600` |
| strict empty | 26,168 | `180207/51200` |
| unresolved collars | 42,104 | `5263/51200` |

The total unresolved area drops from `35721/102400` to `5263/51200`, a
reduction of the exact fraction `25195/35721` (`70.53%`) of the old
uncertainty.  Relative to the full parameter domain, the remaining fraction
is exactly

\[
 \frac{5263}{196608}.
\]

All remaining endpoint collars are genuine source-grazing `c_p=0` collars;
the `tau=3` endpoint collar is empty.  Of 23,376 such boxes, 16,304 certify a
unique transverse common-tangent graph `z=z(s)`, covering `1019/25600`.
Uniform event labels on every outgoing curved half-box are still missing.

The refined physical bulk has 64 connected same-label components in 16
exact `Jx/Jy` four-orbits.  A full replay constructs

```text
11,812 physical boxes,
 5,906 exact Jx box pairs,
    32 exact Jx component-label pairs.
```

Under `Jx`, `s`, `n_x`, `u_x` and the tangency sign reverse, while flight,
source cosine, `|dt/dz|` and collision-SRB density are invariant.  Therefore
the positive coefficient measures obey `(Jx)_*m_e=m_Jxe`, and all 64
certified refined-bulk components have the exact scalar identity

\[
 \widehat\mu(\dot r)_{\rm refined\ bulk}=0.
\]

This is physical coefficient-law pairing, not merely cancellation of box
area.  It is still not arbitrary-test DQ: reflected endpoints are distinct,
and remaining collars/seams have not been assembled into maximal rows.

Evidence:

- `cm2-gate3-endpoint-identity-refinement-assault-2026-07-15.md`;
- `cm2-gate3-bulk-jx-coarea-pairing-assault-2026-07-15.md`.

## 4. Gates 4--5: refined structural ledger, physical norms still open

For every certified connected immutable subrow, the all-sheet theorem gives
two nonadditive descriptions of the same occurrence, one common positive
coarea law `m_e`, and the single pre-recovery expression

\[
 q_e=\max\{C_e^{\rm fw},C_e^{\rm rev},2\}\,m_e.
\]

The forward and reverse views are alternatives, not additive copies.  Each
occurrence also has two singular Kac coordinates with the fixed structural
mark `(+1,-1)` and one shared coefficient law.  The bounded-Borel measure
typing is exact.

The refined 64-component promotion is structural: it freezes one occurrence
and one pre-recovery `q` expression per component, and rejects charging once
per Kac coordinate.  The physical numerical costs `C_fw,C_rev`, controlled
bidirectional stopped recovery, and the standard-family/flux/dynamic-test
norms are not supplied by this bookkeeping.

Scalar roof cancellation is now exact across the refined physical bulk, but
the family `n(delta_a-delta_b)` remains a strict counterexample to inferring
an arbitrary-test current norm from zero scalar mass.  Accordingly the
following remain open:

- the maximal all-row physical event/DQ registry;
- stopped-parent recovery under the single frozen `q`;
- inverse-Jacobian/distortion and homogeneity cut-growth sums;
- face transversality and dynamic-test pullback constants;
- four fully typed global singular currents;
- standard-family, flux-face and dynamic-test CM2 norm lifts.

Evidence:

- `cm2-gate45-immutable-subrow-kac-ledger-assault-2026-07-15.md`;
- `cm2-gate4-all-sheet-single-charge-schema-assault-2026-07-15.md`;
- `cm2-gate5-prefix-suffix-norm-assault-2026-07-15.md`.

## 5. Shortest remaining route

1. Cover the Gate-2 stable segment by correlated first-hit boxes over a
   positive unstable interval, prove plaque compatibility/invariance, and
   construct the physical stable-holonomy Jacobian.
2. Enumerate the `>90.3%` physical complement into a full-mass countable
   return alphabet; instantiate its actual density, reverse weights,
   off-diagonal projective collision bounds, stopped antichain, endpoints and
   normalized amplitudes.
3. Resolve the Gate-3 outgoing sides of the source-grazing graphs plus the
   remaining first/miss/polarity collars, quotient seams, and freeze maximal
   global physical rows.
4. Compute physical coarea currents and the numeric forward/reverse recovery
   costs on every row; assemble arbitrary-test DQ and all four Kac currents.
5. Export the complete distortion, cut, face and test constants through the
   fixed-to-full-boundary intertwiners and certify the CM2 norm lifts.
6. For Gate 1, either build a genuinely different typed cocycle/coding with
   valid holonomies or close the projective input directly through the actual
   Gate-2 physical PPE, bypassing the refuted frozen natural QNL route.

## 6. Verification discipline

- All positive certificates in this pass exit zero.
- Fail-closed live verifiers for the still-open physical gates exit two by
  design; their self-tests reject promoted completion flags.
- New SHA-256 manifests and the frozen v51/v52 manifests are checked after
  this report and the research log are pinned.
- No CM2 cron was used and no residual CM2 computation is retained.

