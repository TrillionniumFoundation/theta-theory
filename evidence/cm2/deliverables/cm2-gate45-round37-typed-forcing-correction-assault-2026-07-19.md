# CM2 Gates 4/5 round 37: typed forcing correction

Date: 2026-07-19  
Status: **the round-36 aggregate recurrence remains valid abstractly, but its
four-term physical forcing description is corrected by operator type**

## Correction

Round 36 informally wrote

```text
J_n=J_core,n+J_owner,n+J_occurrence,n+J_cemetery,n.
```

That expression mixed fixed-parameter standard-family evolution, parameter
currents, and absorbing strong charges.  The frozen coefficient

```text
a=360134800/360493663
```

already counts every true continuity/collision-singularity component, the
first-visible owner partition, and the homogeneity cuts and multiplicities.
They are not a second additive base-`Z` injection.  Moving occurrences belong
to F10/F13/F16 parameter current and flux.  The strong cemetery is a separate
absorbing boundary/trace charge and is not zero by collision-null mass.

For the fixed-`s` base survivor family, the repeated extra restriction is the
C24 complement:

```text
Z_(n+1)<=a Z_n+b m_n+J_C24,n.
```

The round-36 recurrence remains a correct abstract bookkeeping inequality
when `J_n` means the actual unpriced extra strong cost.  Its old four-term
decomposition is not a certified typed physical bound.

## Exact complement obstruction

The positive inner-core theorem controls one retained interval with multiplier
`2000/1999`.  It gives

```text
(2000/1999)*a
 =720269600000/720626832337
 <1.
```

But deleting one core interval can leave two survivor intervals.  The safe
two-component estimate is

```text
(4000/1999)*a
 =1440539200000/720626832337
 >1,
```

with exact excess `719912367663/720626832337`.  Therefore the one-component
`M_core` contraction does not imply a contraction for `M_C24^c`.

## Exact functional countermodel

Let one standard curve be `W_L=[0,L]` with constant density one.  Its old
unnormalised boundary functional is `Z_old=L/L=1`.  Remove a central interval
using two stationary transverse affine faces.  The two survivors each
contribute one, hence `Z_new=2`, while the local data are ideal:

```text
F8=1, F9=0, F10=0.
```

A universal mass-additive estimate `Z_new<=Z_old+C L` would require
`1<=C L`.  Taking `L=2^-k` violates it for every finite `C`.  This is an
exact non-implication for the standard-family functional, not a claim about
the frequency of physical C24 cuts.

## Corrected frontier

The first missing base-`Z` theorem is a hereditary C24-complement open Growth
inequality, or an equivalent physical weighted tail for two-sided core splits
before normalization.  Global F10 and F12/F13 remain necessary in parallel
for the parameter current, but local face regularity cannot by itself supply
the fixed-`s` base survivor bound.

```text
HEREDITARY C24 OPEN GROWTH:             NOT CERTIFIED
PHYSICAL AGGREGATE Z BOUND:             NOT CERTIFIED
COMPLETE C_fw,C_rev,q:                  NOT CERTIFIED
STRONG CEMETERY:                        NOT CERTIFIED
GATE 5 MATURITY:                        7/18 UNCHANGED
GATES 3--5 / CM2:                       NOT CERTIFIED / NO-GO
```

## Evidence

- `deliverables/cm2_gate45_round37_typed_forcing_correction_cert.py`
- `deliverables/cm2_gate45_round37_typed_forcing_correction_verifier.py`
- `deliverables/cm2-gate45-round37-typed-forcing-correction-manifest-2026-07-19.json`

Syntax, dependency integrity, replay and live fail-close pass.  The verifier
rejects `16/16` hostile mutations.
