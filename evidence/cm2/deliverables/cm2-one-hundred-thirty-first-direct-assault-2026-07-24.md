# CM2 one-hundred-thirty-first direct assault

Date: 2026-07-24

Result: **all tested re-signed semantic and strict-JSON attacks rejected.**

The assault re-signs mutations that alter the deficit count, invent a global
complete block, identify the symbolic overlap as one physical root, or change
CM2 to `GO_FOR_CLAIM`.  The independent reconstruction rejects every case.

The strict parser also rejects duplicate top-level keys, a UTF-8 BOM, and a
top-level array.  Missing or malformed certificates fail before output.

Two producer cold runs and two verifier cold runs under distinct hash seeds
are byte-identical to the official artifacts.

```text
touched symbolic words                     18
no-certified-incidence words           441262
base-R1 reciprocal pairs                    8
global complete 18-field blocks             0
global Gate5                            10/18
CM2                              NO-GO_FOR_CLAIM
```
