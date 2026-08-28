# CM2 Gate 5 assault: fixed section to standard full boundary

Date: 2026-07-15 (Asia/Shanghai)  
Frozen inputs: `cm2-bridge-note-v51.tex`, `cm2-bridge-note-v52.tex`, and the
v52 manifest were read only  
Target model: the same centered finite-horizon two-disk pilot, in the fixed
arclength--angle gauge

## Verdict

Gate 5 is **not closed**.  The exact status is now narrower:

| clause | status | certified content / remaining obstruction |
|---|---|---|
| `SF1 COMMON_REFINEMENT` | proved | `X=M*=M sqcup W` contains both `M` and `N=G sqcup W`; the 160-bit Arb horizon certificate gives `tau_max<3`, return depth to `N` at most `9`, and target lifts in `[-4,4]^2`. |
| `SF2 RETURN_BLOCK_DQ` | open | This is not an independent analytic mystery: it is the restriction of Gates 3--4 to the finite return-word partition.  The global occurrence manifest, boundary current, and exact source/`q` matching are still absent. |
| `SF3 KAC_CENTERING` | algebra proved; singular terms not typed | Fixed flux measures make the Kac quotient derivative explicit.  `dot S` and `dot r` remain singular return-boundary currents and therefore depend on `SF2/SF5`. |
| `SF4 RETURN_WIENER_APERIODICITY` | target `N` closed; optional phase tower open | Demers--Zhang gives the uniform spectral gap/Wiener remainder for the standard collision map on `N`.  A separately introduced common-refinement tower still needs an actual finite graph and a cycle-gcd-one certificate. |
| `SF5 PHASE_TEST_NORM_LIFT` | regular-density subspace proved; singular face-current subspace open | Demers--Liverani 2026, Theorem 6.1, identifies the density cone norm and anisotropic Banach norm in the SRB case.  It does not embed one-dimensional standard-pair or face-current measures in that Banach space. |

Consequently `SECTION_FULL_CM2` remains `NO-GO FOR CLAIM`.  A direct theorem
on `N` eliminates the *need* for a section-transfer theorem, but it cannot be
counted as a proof of Gate 5 and does not remove Gates 1--4.

## 1. Exact common-refinement and Kac conclusions

Let `M` be the Stenlund section (gray collisions and selected clean
transparent-wall crossings), `W` the white collision component, and

```text
X = M* = M sqcup W,          N = G sqcup W.
```

The first return to `M` has depth in `{1,2}`.  The independent 160-bit Arb
cover in `cm2_standard_section_horizon_lift_cert.py` proves, uniformly in the
white-center displacement,

```text
tau_max < 3,       gray/white target indices in [-4,4]^2.
```

The number of integer grid lines crossed by one solid-to-solid flight is
therefore uniformly bounded, and the first return from `X` to `N` has depth
at most

```text
K_N <= 2 ceil(tau_max) + 3 <= 9.
```

The component alphabet and lift range are finite, so the bounded return-word
sets are Borel.  This proves the geometric/measurable content of `SF1`; it
does not differentiate their moving boundaries.

All obstacle perimeters and the abstract arclength--angle gauges are fixed.
Thus the collision-flux probabilities on `M`, `N`, and `X` are parameter
independent.  For either base `B=M,N`,

```text
mu_X(h_s) = mu_B(S_{B,s} h_s) / mu_B(r_{B,s}),
mu_B(r_{B,s}) = 1 / mu_X(B),
```

and the denominator is constant.  Whenever the four displayed currents are
typed, differentiation gives

```text
d[S_s h_s - r_s mu_X(h_s)]
  = dot(S) h + S dot(h) - dot(r) mu_X(h) - r mu_X(dot(h)).
```

This closes the scalar/algebraic part of `SF3`.  It does not turn `dot(r)` or
the moving-level part of `dot(S)` into bounded observables.

## 2. What the June 2026 norm-equivalence theorem adds

Demers--Liverani, *Recent Progress in the Application of Transfer Operators
to Dispersing Billiards*, arXiv:2606.10155v1 (8 June 2026), Theorem 6.1,
proves the following in the SRB case.  If the anisotropic Banach space is
defined using the common stable-curve class and the cone parameters satisfy
their stated inequalities (`q=1/p`, `A>4`, `A_c>1+C_s`, and the stated
Holder-exponent bound), then

```text
||.||_B  equivalent to  ||.||_*
```

on the same distribution space.  The construction uses a curve class common
to the compact family of fixed-perimeter billiards, so the equivalence
constants are uniform after the pilot path is restricted to its compact
uniform billiard class.

Source: <https://arxiv.org/abs/2606.10155>, Theorem 6.1 and Remarks 6.2--6.3.
PDF checked in this audit:

```text
sha256 3330b5467c5c7107e58ba7966a0386f2ab51415990399b387ad2f7e571f61798
```

This closes only the **regular two-dimensional density** part of `SF5` on
the standard collision section.  It cannot be applied to the CM2 face source
by renaming that source a cone element.  The paper's cone consists of density
functions/distributions obtained from the Banach completion; the CM2 source
space in v52 is instead the positive-decomposition completion of measured
one-dimensional standard curves and oriented coarea currents.  No embedding
with a uniform norm bound is supplied.

This distinction is confirmed explicitly by Canestrari's 2026 work below:
the standard-pair argument is used precisely because no available general
piecewise-hyperbolic Banach space is known to contain the required unstable
curve measures.

## 3. What the two Canestrari linear-response theorems do not supply

### 3.1 Discontinuous perturbations

Canestrari, *On linear response for discontinuous perturbations of smooth
endomorphisms*, Advances in Mathematics 2026, Theorem 2.4, proves linear
response if

1. the piecewise maps form an admissible finite-branch family;
2. the initial defect `nu_t/t` converges as a finite measure; and
3. hypothesis `(H4)` supplies a summable, uniform correlation bound for the
   conditional curve measures of a foliation of the moving discontinuity
   complement.

Proposition 2.5 then decomposes the limiting defect into a Lipschitz density
plus a finite singular measure.  This is the correct abstract shape of the
desired billiard current, but the theorem does not verify its hypotheses for
a moving billiard.  In particular the billiard homogeneity atlas is
countable near grazing, the global first-hit partition has not been
instantiated, and `(H4)` is essentially the missing recovery/`q` ledger.

Source: <https://arxiv.org/abs/2411.16628>, Definition 2.2, Theorem 2.4,
Proposition 2.5, and the discussion following Proposition 2.6.  PDF checked:

```text
sha256 175aa794149bcf81fe37e6a2c1cf4bfaab964513c0882a0204633c1da32e868c
```

### 3.2 Small holes in Sinai billiards

Canestrari, *Linear response for Sinai billiards with small holes*,
arXiv:2604.19671v2, Theorem 2.1, proves differentiability at zero hole size.
Proposition 4.4 and Theorem 4.7/Corollary 4.8 give invariance and exponential
conditional relaxation of regular standard families.  The derivative is a
one-sided series generated by the vertical boundary measure at the fixed
hole location.

Source: <https://arxiv.org/abs/2604.19671v2>, Theorem 2.1, Proposition 4.4,
Theorem 4.7, and Corollary 4.8.  PDF checked:

```text
sha256 fc00f45a8ec6513763665bf8fa34569a95ca5d6d6b9fa5d90b7e1089fabd9004
```

This supplies a strong source-first template, not `SF2` or `SF5` for the
pilot.  The map is fixed and the perturbation is a shrinking vertical hole;
there is no derivative of a moving collision branch, no global collision
event inventory, no two-sided same-occurrence CM2 factorization, and no
fixed-section/full-boundary intertwiner.

## 4. Dependency reduction

The remaining pieces of Gate 5 can be placed exactly:

```text
Gate 3 global event/DQ
        |
        +--> SF2 return-block DQ
        |
Gate 4 same-occurrence q/recovery
        |
        +--> singular-current part of SF5

standard-N spectral gap --> target part of SF4       [proved]
fixed flux/Kac algebra --> scalar part of SF3         [proved]
DL 2026 norm equivalence --> regular part of SF5      [proved]
```

Thus there is no separate theorem that can close `SF2` before the global
event/occurrence work is done.  Conversely, once Gates 3--4 are proved
directly on `N`, the physical current and tests already live on the target
section and a fixed-to-full transfer is unnecessary.  This is a rigorous
route reduction, not a promotion of Gate 5 to `GO`.

## 5. Fail-closed certification target

Any future Gate-5 certificate must contain all of the following on one model
identifier and one immutable occurrence registry:

1. the complete finite return-word table and its Borel coverage;
2. one DQ/current witness for every moving return boundary;
3. exact physical/source occurrence and scalar-current matching;
4. the four separately typed Kac terms;
5. either a target-direct declaration (no phase tower) or a strongly
   connected finite phase graph whose weighted cycle gcd is one;
6. explicit bounded maps for regular densities, singular curve/face sources,
   physical tests, and both CM2 norms.

The companion `cm2_gate5_transfer_audit.py` checks this logical interface and
fails on the current pilot manifest.  It is a verifier for completeness and
phase periodicity, not a substitute for the missing analytic witnesses.
