# CM2 Gates 3/4: all-occurrence first-core stopping cylinders

Date: 2026-07-18 (Asia/Shanghai)  
Mode: append-only, fail-closed, binary64 proposal plus independent Arb admission  
Strict verdict: **the existing 128 labelled positive hit/miss cylinders now
have genuine suffix-relative first-core stopping times.  This closes the old
finite-word typing gap on those cylinders only; it does not cover whole germ
domains, quantify collision-SRB mass, estimate cemetery, or close Gate 3/4.**

## 1. Source owner audit

The exact charged source box of every maximal occurrence is reclassified as
the same physical immutable subrow.  On both actual-parameter sides, the
global collision-owner decision is redone against the complete radius-four
lattice candidate universe.

```text
physical source-box label rechecks:                    64/64,
hit tangent target is global first owner:              64/64,
hit regular suffix target is global second owner:      64/64,
miss tangent discriminant is negative on open side:    64/64,
miss regular suffix target is global first owner:      64/64,
hit/miss regular suffix chart agrees:                  64/64.
```

The hit square-root enclosure is adjusted to each exact cylinder radius and
has proposal status only until the 2048-bit Arb owner replay passes.  The two
old `2^-220` cylinders are also strictly contained in their predecessor
all-scale germs.

## 2. First-core stopping classification

The stopping clock is explicit:

```text
time 0 = the regular suffix state.
```

The earlier source-to-suffix collision(s), including the hit-side tangent
contact, are not part of this clock.  Every state in every displayed word is
classified by strict Arb comparisons against all three core rectangles in
its unique collision chart.

```text
oriented charged cylinders:                           128,
strict preterminal states outside all 24 cores:       756,
strict terminal states inside exactly one core:       128,
ambiguous core classifications:                         0,
distinct destination cores:                            14,
maximum suffix-relative first-core time:                20.
```

The oriented-cylinder stopping-time histogram is

```text
2:44, 3:20, 4:16, 7:16, 8:8, 9:8, 16:4, 19:8, 20:4.
```

Thus all 128 former entrance-time upper bounds are upgraded to actual first
stopping times on the same positive cylinders.

## 3. Strict boundary

```text
CHARGED FIRST-CORE STOPPING CYLINDERS:              128 CERTIFIED
GLOBAL HIT/MISS SOURCE OWNER AUDITS:              64/64 CERTIFIED
MAXIMUM SUFFIX-RELATIVE FIRST-CORE TIME:             20 CERTIFIED

WHOLE-GERM FIRST-CORE STOPPING:                 NOT CERTIFIED
LABELLED COORDINATE VOLUME = COLLISION-SRB MASS:       FALSE
NORMALIZED SELECTED CORE-HIT FRACTION:           NOT CERTIFIED
QUANTITATIVE CEMETERY TAIL:                      NOT CERTIFIED
POST-CORE FIRST-RETURN OPERATOR:                 NOT CERTIFIED
COMMON TWO-VIEW / STRONG-SPACE OPERATOR:         NOT CERTIFIED
GATE 3 / GATE 4:                                NOT CERTIFIED
```

## 4. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_all_occurrence_first_core_stopping_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_all_occurrence_first_core_stopping_verifier.py \
  --self-test
```

Replay and integrity pass.  The verifier rejects `38/38` hostile mutations;
live mode exits `2` because both composite gates remain open.
