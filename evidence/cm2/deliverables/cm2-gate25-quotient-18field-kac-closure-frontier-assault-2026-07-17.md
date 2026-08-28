# CM2 Gates 2/5: quotient, 18 fields, three norms and Kac/phase

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the separate all-plaque class-H gauges, Gate-2 quotient schema,
24-core operator seeds, all-key characteristic theorem, and Gate-5 Kac/norm
frontiers  
Strict verdict: **class H cannot replace a physical stable quotient; Gate 2
remains `0/17`.  Gate 5 now has one all-key formula field (`field 7`) and two
24-core local seeds (`fields 5–6`), but zero complete physical 18-field
blocks.  The direct-standard-`N` phase route itself is selected and needs no
extra phase tower; three norms and physical Kac typing remain open.**

## 1. Class H does not imply PPE

Take the invertible 97-cycle

```text
F(i)=37i+11 mod 97
```

with constant cocycle `A=diag(2,1/2)`.  Both canonical holonomy families are
the identity, so the cocycle is class H with Hölder constant zero.  Any finite
or countable edge-label refinement still leaves exactly one physical past at
every target.  The reverse conditional is Dirac and its diagonal two-copy
Riesz coefficient is exactly one.

Thus even exact class-H holonomies do not create a stable quotient, reverse
randomness, or PPE.  The new separate lower/upper all-plaque gauges cannot be
inserted into Gate 2 without the physical stable-saturated base and branch
registry.

## 2. Gate 2 remains 0/17

The immutable Gate-2 schema still requires 17 jointly labelled objects,
starting with

```text
Lambda_A, I_A, pi^s, stable-holonomy SRB Jacobian,
connected return strips, onto h_a, rho, p_a, ...
```

All 17 physical completion flags remain false.  The first missing object is
the stable-saturated product base `Lambda_A`; the first reverse-kernel object
is the stable projection `pi^s`.  Class H is cocycle regularity over a base,
not the construction of this base or quotient.

## 3. Exact 18-field maturity

The physical per-level schema has 18 fields.  Its current maturity is:

```text
field 5  inverse_Jacobian_bound:       24-core local seed,
field 6  log_Jacobian_distortion_sum:  24-core local seed,
field 7  one_step_cut_growth_Z_sum:    all 441280 keys and every maximal
                                       component, finite but noncontracting.
```

The field-7 formula is

```text
Z_*(1_{D_w(s)}F)<=C_src Z_*(F),
C_G=580000/1999, C_W=572000/1999.
```

Physical homogeneous subbranch ids are still absent.  Hence fields 5–6 are
not full-key slots, field 7 is not an instantiated homogeneous slot, and no
complete block exists:

```text
schema-level all-key formula fields:       1/18,
complete physical homogeneous slot fields: 0/18,
complete 18-field operator blocks:             0.
```

## 4. Three norms and Kac/phase

One-collision seeds exist for regular density, standard families, flux/face,
and dynamic tests.  None is a return-wide prefix/suffix intertwiner, so all
three CM2 norm lifts remain open.

The finite-Borel four-term Kac algebra is exact.  The singular event current
has TV at most `16128/5`, and its height-nine phase lift is at most
`290304/5`.  The two regular terms and the propagated singular terms are not
separately typed in CM2 spaces.

The standard-`N` component cycle gcd is one.  On the preferred
`direct_standard_N` route no separate phase tower is required.  Therefore
the current direct-route blocker is not component periodicity: it is the
missing return-word operator blocks, three norm intertwiners, and physical
typing of all four Kac terms.  The optional operator-Wiener route remains
unproved but is not needed for the preferred route.

```text
CLASS H -> PHYSICAL PPE NONIMPLICATION:     CERTIFIED
GATE-2 PHYSICAL QUOTIENT FIELDS:            0/17
GATE-5 ALL-KEY FORMULA FIELDS:              1/18
COMPLETE PHYSICAL 18-FIELD BLOCKS:          0
DIRECT-STANDARD-N PHASE ROUTE CHOICE:       CERTIFIED
RETURN-WIDE THREE NORM INTERTWINERS:        NOT CERTIFIED
FULL PHYSICAL KAC CM2 OUTPUT:               NOT CERTIFIED
GATES 2 AND 5:                              NOT CERTIFIED
```

## 5. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate25_quotient_18field_kac_closure_frontier_cert.py \
  deliverables/cm2_gate25_quotient_18field_kac_closure_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_quotient_18field_kac_closure_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_quotient_18field_kac_closure_frontier_verifier.py \
  --self-test

# Expected exit 2: quotient/PPE/operator blocks/norms/Kac remain open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_quotient_18field_kac_closure_frontier_verifier.py
```
