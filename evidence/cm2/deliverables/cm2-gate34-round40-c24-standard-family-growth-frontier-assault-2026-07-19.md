# CM2 Gates 3/4 round 40: corrected canonical-Z route and C24 Growth frontier

Date: 2026-07-19  
Status: **Round 39's C0-trace necessity claim is superseded for positive
standard-family initialization; the actual Gate-4 base gap is hereditary
C24 open Growth**

## 1. Exact correction to Round 39

Round 39 proved a valid local fact: the existing projective stable-test
controls do not bound a pointwise transverse trace.  That obstruction is
needed for moving inverse-branch face currents, where the source has type

```text
h -> w(h|I+ - h|I-) delta_Gamma.
```

It was too strong to infer that a C0 trace is necessary for initializing a
positive canonical standard family.  A standard-family representation is a
measure disintegration, not a pointwise restriction of a two-dimensional
density.  More decisively, the frozen dependency chain already certifies for
controlled `s=0` stopped atoms, in both orientations,

```text
Z_fw(K,j), Z_rev(K,j) <= C_mesh 2^K,
```

with the same restricted measure and same depth record.  Thus:

```text
ROUND-39 C0 TRACE NECESSITY FOR POSITIVE Z: SUPERSEDED
ROUND-39 MOVING-CURRENT NO-TRACE OBSTRUCTION: REMAINS VALID
ROUND-39 NO-PROMOTION VERDICT: REMAINS VALID
```

The correction does not certify Gate 4.  It removes a false intermediate
requirement and relocates the first missing operator.

## 2. Actual first missing operator

The positive initial family is available, but repeated multiplication by the
C24 survivor indicators can split and shorten its unstable carriers.  The
missing theorem is a same-ID, fixed-`s` open Growth recurrence of the form

```text
Z(hat F_C24^((p+1)n_*) G)
 <= gamma_C24 Z(hat F_C24^(p n_*) G) + Z0_C24 mass(G),
0 < gamma_C24 < 1.
```

This is a native standard-family statement.  It bypasses both the pointwise
C0 trace and the representation-dependent projective-norm comparison.

The frozen C24 geometry already supplies

```text
O1, O1' : P0=49,
O2      : Ct=1493,
boundary edges: 48 per collision component, 96 total,
uniformity: |s|<=1/400.
```

What is not yet supplied is the C24-specific expansion-versus-fragmentation
sum after conditioning, with a strict block coefficient below one.  The old
safe global one-step envelope is

```text
137751561/901685 > 1,
```

so it cannot be promoted to the needed Growth contraction.

## 3. Exact inverse-length boundary criterion

Let `eta=ell/delta in (0,1]` be normalized canonical carrier length and let
`nu` be its boundary-cell mass.  If

```text
nu{eta<=t} <= C_boundary M t^alpha,
```

then dyadic shells give

```text
integral eta^(-1) dnu
 <= 2 C_boundary M / (1-2^(1-alpha)),
```

provided `alpha>1`.  Exact multipliers include

```text
alpha=2: 4,
alpha=3: 8/3,
alpha=4: 16/7.
```

The strict inequality is necessary for this tail-only argument.  At
`alpha=1`, take

```text
eta_k=2^-k,  mass_k=2^(-(k+1))M.
```

Then `nu{eta<=2^-n}=M2^-n`, but every shell contributes `M/2` to the inverse
length moment, so `Z` diverges.  Round 26's tube law has exponent one in a
parameter-averaged physical width and is not the same canonical boundary-cell
law.  It therefore cannot close hereditary C24 Growth by itself.

## 4. Latest technology match

Official arXiv pages were checked directly on 2026-07-19:

```text
2104.06947v3  revised 2022-11-18,
2604.19671v2  revised 2026-05-21,
2606.10155v1  submitted 2026-06-08.
```

The relevant new mechanism is Canestrari `2604.19671v2`:

- Proposition 4.4 preserves regular standard families under that paper's
  conditional leaky evolution.
- Lemma 6.14 proves a block Growth recurrence with `gamma<1` by making
  expansion beat fragmentation and chopping short descendants.

This is the right proof architecture, but not a directly importable theorem
row.  The paper's small boundary-strip hole has not been identified with the
96-edge C24 phase hole.  A C24-specific expansion/fragmentation replay is
still mandatory.

The ordinary search endpoint was quota-limited during this round; direct
official arXiv fetches succeeded and supplied the version and theorem checks.

## 5. Strict boundary

```text
CONTROLLED s=0 INITIAL STANDARD-FAMILY Z: CERTIFIED PREVIOUSLY
INVERSE-LENGTH alpha>1 CRITERION:         CERTIFIED
C24 O1/O1'/O2 GEOMETRY:                  CERTIFIED PREVIOUSLY
HEREDITARY C24 OPEN GROWTH:               NOT CERTIFIED
PHYSICAL AGGREGATE Z / C_fw / C_rev / q: NOT CERTIFIED
GATE 3 / GATE 4 / CM2:                   NOT CERTIFIED / NO-GO
```

The delayed scalar fallback remains valid: a full-survivor characteristic
constant `C_N=4000/1999` would contract after `N=697`, while the generic F7
constant `580000/1999` would require `N=5694`.  Neither full-`Q_N` physical
constant is currently certified.

## Evidence

- `deliverables/cm2_gate34_round40_c24_standard_family_growth_frontier_cert.py`
- `deliverables/cm2_gate34_round40_c24_standard_family_growth_frontier_verifier.py`
- `deliverables/cm2-gate34-round40-c24-standard-family-growth-frontier-manifest-2026-07-19.json`

Syntax, frozen dependency hashes, strict JSON, exact rational replay and live
fail-close pass.  The verifier rejects `23/23` hostile mutations.
