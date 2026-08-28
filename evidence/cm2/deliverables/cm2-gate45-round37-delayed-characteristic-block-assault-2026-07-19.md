# CM2 Gates 4/5 round 37: delayed characteristic block

Date: 2026-07-19  
Status: **the delayed-restriction scalar route is exactly contractive, but the
required full-survivor characteristic multiplier is not physical yet**

## Conditional block theorem

The closed map satisfies

```text
Z(T_*^N F)
 <=a^N Z(F)+b(1-a^N)/(1-a) mass(F),
a=360134800/360493663.
```

If the entire `N`-step survivor set `Q_N` had one same-carrier
characteristic multiplier `C_N`, then

```text
Z(M_QN T_*^N F)
 <=C_N a^N Z(F)
   +C_N b(1-a^N)/(1-a) mass(F).
```

Hence `C_N a^N<1` gives a deterministic pointwise and weighted Green
resolvent without inverse component mass or cellwise retained depth.

## Exact thresholds

For the hypothetical uniform two-component multiplier `4000/1999`, exact
integer arithmetic gives the first contracting block at

```text
N=697,
(4000/1999)a^697 <49973/50000<1,
(4000/1999)a^696 >=1.
```

The weight `99973/99946>1` leaves weighted coefficient
`<99973/100000` and weighted resolvent `<100000/27`.

For the frozen generic F7 multiplier `580000/1999`, the first contracting
block is

```text
N=5694,
(580000/1999)a^5694 <24983/25000<1,
(580000/1999)a^5693 >=1.
```

The weight `49983/49966>1` leaves weighted coefficient `<49983/50000`
and weighted resolvent `<50000/17`.

## Missing physical quantifier

Neither constant presently applies to the full arbitrary-depth survivor
union:

- `4000/1999` is only one curve minus one core interval;
- `580000/1999` is one frozen finite return-word key fibre or one maximal
  component, not the union over `24*441280^n` path words;
- the arbitrary-`n` schema materializes no complete `R_n/Q_n` branch table or
  uniform/subexponential full-union characteristic constant `C_N`;
- `N_open` is uniform but nonnumeric and controls weak survivor mass, not the
  strong characteristic functional;
- the old scheduled dwell route still lacks native no-hidden-recut incidence.

The exact next scalar target is therefore:

```text
find one physical N and full-survivor C_N on the same strong carrier
such that C_N a^N<1.
```

```text
CONDITIONAL DELAYED SCALAR BRIDGE:       CERTIFIED
FULL-Q_N CHARACTERISTIC C_N:            NOT CERTIFIED
PHYSICAL KILLED STRONG CONTRACTION:      NOT CERTIFIED
HEREDITARY C24 OPEN GROWTH:              NOT CERTIFIED
GATES 3--5 / CM2:                        NOT CERTIFIED / NO-GO
```

## Evidence

- `deliverables/cm2_gate45_round37_delayed_characteristic_block_cert.py`
- `deliverables/cm2_gate45_round37_delayed_characteristic_block_verifier.py`
- `deliverables/cm2-gate45-round37-delayed-characteristic-block-manifest-2026-07-19.json`

Syntax, dependency integrity, replay and live fail-close pass.  The verifier
rejects `15/15` hostile mutations.
