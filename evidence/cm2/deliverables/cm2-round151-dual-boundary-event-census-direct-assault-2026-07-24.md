# CM2 Round151 direct hostile assault

Date: 2026-07-24

Independent verification status: **PASS**.

The verifier independently reconstructs both 21-box event graphs and
rejects ten fully re-signed semantic mutations attempting to:

- erase C24 fibrewise uniqueness;
- delete one D3 x slab;
- inflate the certified graph-separation bound;
- replace the sole D3 anchor candidate;
- disable strict anchor preemption;
- close Round144 D02;
- authorize the D03 negative oracle;
- mint a fake component identifier;
- promote global Gate5 to `18/18`; or
- change CM2 to `GO_FOR_CLAIM`.

It also rejects four strict parser attacks: duplicate JSON keys, a UTF-8
BOM, a top-level array and `NaN`.

```text
re-signed semantic attacks rejected       10/10
strict JSON/encoding attacks rejected       4/4
C24 event boxes reconstructed                 21
D3 event boxes reconstructed                  21
radius-four candidate tests replayed   5,582,031
D02                                      BLOCKED
global Gate5                               10/18
CM2                             NO-GO_FOR_CLAIM
```
