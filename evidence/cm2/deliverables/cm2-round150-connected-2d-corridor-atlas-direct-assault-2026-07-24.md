# CM2 Round150 direct hostile assault

Date: 2026-07-24

Independent verification status: **PASS**.

The verifier reconstructs all 18 new full R1648 audits and rejects ten
fully re-signed semantic mutations attempting to:

- change a certified return cell to survive;
- delete an exact-face adjacency;
- erase the unique terminal event graph;
- restore Round149's old unclassified gap;
- claim that the local corridor is maximal;
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
full audited objects reconstructed           18
radius-four candidate tests replayed   4,775,904
D02                                      BLOCKED
global Gate5                               10/18
CM2                             NO-GO_FOR_CLAIM
```
