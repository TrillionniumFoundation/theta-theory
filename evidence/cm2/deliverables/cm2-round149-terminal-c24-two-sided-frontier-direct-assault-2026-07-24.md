# CM2 Round149 direct hostile assault

Date: 2026-07-24

Independent verification status: **PASS**.

The verifier replayed two complete 1,648-stage cells and 530,656 radius-four
candidate tests.  It rejected 8/8 fully re-signed mutations targeting:

- the terminal return/survive classification;
- the strict unclassified gap;
- a false unique-global-graph claim;
- illicit D02 closure or D03 authorization;
- a minted component identifier;
- global Gate5 promotion; and
- `GO_FOR_CLAIM`.

It also rejected 4/4 strict parser attacks: duplicate keys, UTF-8 BOM,
top-level array, and `NaN`.

```text
D02                  BLOCKED
global Gate5         10/18
complete blocks      0
CM2                  NO-GO_FOR_CLAIM
```
