# CM2 Gate 5: selected component chart-field slots

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the 24 selected positive maximal components, 28 field-7 roof
slots, physical core charts, and the four roof-two wall charts  
Strict verdict: **fields 3 and 4 are now materialized on all 28 selected roof
levels.  The selected-level minimum maturity rises from `2/18` to `4/18`.
The full homogeneity tables, fields 2, 5–6 as roof-level fields, fields 8–18,
three norms and Gate 5 remain open.**

## 1. Exact chart join

Every selected maximal component is defined with a fixed physical word,
source collision chart, target open-semicircle chart, and every intermediate
oriented transparent-wall chart.  These labels are part of the component
predicate, not labels inferred from its rational seed.

The join materializes, for every selected `(word key, homogeneous component,
roof level)`, the immutable slots

```text
field 3: homogeneous_prefix_chart,
field 4: homogeneous_suffix_chart.
```

Counts are

```text
selected maximal components: 24,
roof-one components:          20,
roof-two components:           4,
selected roof levels:          28,
field-3 slots:                 28,
field-4 slots:                 28.
```

Roof-one levels connect a source collision chart directly to the fixed target
open-semicircle chart.  Roof-two levels connect

```text
source collision -> oriented wall chart -> target collision.
```

The four wall crossings remain uniformly away from corners and carry the
frozen local diffeomorphism bounds.

## 2. Fields 5 and 6 remain seeds

The universal inverse-Jacobian and log-distortion packets are now joined to
all 24 selected component IDs.  They remain component-local seeds, not
completed roof-level fields.  In particular, first-derivative wall-chart
`D_infinity` bounds are not silently promoted to the field-6 logarithmic
distortion slot.

## 3. Maturity update

Each of the 28 selected levels now has

```text
field 1  nonempty domain,
field 3  homogeneous prefix chart,
field 4  homogeneous suffix chart,
field 7  finite characteristic cut-growth formula.
```

Therefore

```text
selected component-level maturity: 4/18,
remaining fields per selected level: 14,
complete key homogeneity tables: 0,
complete 18-field blocks: 0.
```

The first missing field remains field 2, the complete physical homogeneity
subbranch table.  One selected row does not decide all homogeneous rows of a
key.

## 4. Strict frontier

```text
SELECTED FIELD-3 PREFIX CHART SLOTS:         28 CERTIFIED
SELECTED FIELD-4 SUFFIX CHART SLOTS:         28 CERTIFIED
SELECTED COMPONENT-LEVEL MATURITY:           4/18
COMPLETE KEY HOMOGENEITY TABLES:             0
COMPLETE 18-FIELD OPERATOR BLOCKS:           0
THREE-NORM/KAC CLOSURE:                      NOT CERTIFIED
GATE 5:                                      NOT CERTIFIED
```
