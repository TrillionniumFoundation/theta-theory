# CM2 Gates 2/5: selected-component field-7 slot frontier

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the 24 positive seeded maximal components, the all-key/all-
component characteristic theorem, the selected QNL homoclinic component
incidence, the 18-field schema, and the scheduled field-7 dwell block  
Strict verdict: **field 7 is no longer only a schema-level formula.  It is
now bound to 24 positive physical maximal-component rows and all 28 of their
roof-level slots; together with field 1, each selected component level has
`2/18` completed fields.  The selected QNL homoclinic component has one
explicit field-7 slot.  The complete homogeneity tables, the other 16 fields,
physical dwell installation, stable quotient and PPE remain open.**

## 1. Materialized selected component rows

The frozen seeded registry contains 24 pairwise distinct physical word keys
and one positive maximal connected component for each key.  Every row is
nonempty for every `|s|<=1/400`, is uniformly strict-first-hit, and fixes
central source/target homogeneity `|p|<3/10`.

For each row the certificate materializes

```text
h_selected = hash(word key,
                  maximal component id,
                  source/target central homogeneity,
                  defining component predicate).
```

The exact counts are

```text
source G components: 12,
source W components: 12,
roof 1 components:   20,
roof 2 components:    4,
selected h rows:      24,
roof-level slots:     28.
```

This is one selected homogeneous component row per known positive key.  It
is not a complete homogeneity table for any key and says nothing about the
remaining candidate keys or other components.

## 2. Field-7 binding

The all-component theorem gives, on every maximal component,

```text
source G: Z_*(1_M F)<=(580000/1999) Z_*(F),
source W: Z_*(1_M F)<=(572000/1999) Z_*(F).
```

Binding this formula to `(word key,h_selected,roof level j)` produces 28
immutable physical field-7 slot IDs.  Field 1 is also complete on every row
because the certified component proves its word key nonempty.  Therefore the
selected-component maturity becomes

```text
field 1  nonempty_or_empty_domain_proof:  NONEMPTY,
field 7  one_step_cut_growth_Z_sum:       FINITE FORMULA,

completed fields per selected level:     2/18,
remaining fields per selected level:    16/18,
complete 18-field blocks:                    0.
```

The field-7 coefficient alone is not a contraction.

## 3. Selected QNL homoclinic slot

The already certified physical corridor places the selected QNL homoclinic
collision in component

```text
7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5
```

with key

```text
["G:E","W[0,0]",[],1].
```

Its materialized field-7 slot is

```text
slot:530fb5797b653dca584f9c9ac32ce70328dea04f8fca3db195349dd663948c8f
```

and carries multiplier `580000/1999`.  This joins the selected homoclinic
orbit to one physical field-7 operator slot.  A collision-component label is
still not a stable-quotient branch label and supplies no `rho`, `p_a` or PPE.

## 4. Conditional dwell packet

Every selected field-7 slot receives the abstract scheduled packet

```text
one field-7 restriction
  + 12108 valid fixed-core steps
  => cycle coefficient <13213125/16375808,

cut weight 6/5
  => weighted coefficient <7927875/8187904,
     weighted Green resolvent <32.
```

The packet is conditional.  Native installation still requires a physical
occurrence-to-24-core transport, a common strong norm, and proof that no
hidden recut occurs during all `12108` steps.  None is promoted here.

## 5. Physical incidence probe

The 24 component rows and 64 singular occurrence rows were replayed with the
restored `python-flint` environment.  The occurrence rows contain source,
target, event-side and witness fields; they still contain no recovery-carrier
ID, transport time, core-component destination, or identical pulled-back
restriction.  Source/target matching therefore remains the already audited
many-to-many label relation, not a transported incidence.  The new slot IDs
do not repair that missing dynamical record.

```text
TRANSPORTED OCCURRENCE ->24-CORE INCIDENCE:        NOT CERTIFIED
COMPLETE KEY HOMOGENEITY TABLES:                   0
SELECTED PHYSICAL FIELD-7 ROOF SLOTS:              28
SELECTED COMPONENT FIELD MATURITY:                 2/18
COMPLETE 18-FIELD OPERATOR BLOCKS:                 0
STABLE QUOTIENT / PPE:                             NOT CERTIFIED
GATE 2:                                            NOT CERTIFIED
GATE 5:                                            NOT CERTIFIED
```

## 6. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate25_selected_component_field7_slot_frontier_cert.py \
  deliverables/cm2_gate25_selected_component_field7_slot_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_selected_component_field7_slot_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_selected_component_field7_slot_frontier_verifier.py \
  --self-test

# Expected exit 2: complete blocks, stable quotient and Gates 2/5 remain open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate25_selected_component_field7_slot_frontier_verifier.py
```
