# CM2 Round148 direct hostile assault

Date: 2026-07-24

Independent verification status: **PASS**.

Eight fully re-signed semantic attacks were rejected.  They attempted to:

- close D02 without a maximal outer atlas;
- authorize D03;
- mint a component or parent-W identifier;
- promote F5 or global Gate5;
- change CM2 to `GO_FOR_CLAIM`; and
- partially bind one atomic future slot.

Four strict parser attacks were rejected: duplicate keys, UTF-8 BOM,
top-level array, and `NaN`.

Dual hash-seed producer and verifier replays are byte-identical.

```text
newly certified DAG nodes       D05 D06 D08
first exact blocker             D02
versioned identifiers minted      0
global Gate5                   10/18
CM2                 NO-GO_FOR_CLAIM
```
