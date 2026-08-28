# CM2 Gates 3/4: source-relative first-core stopping

Date: 2026-07-18 (Asia/Shanghai)  
Mode: append-only, fail-closed, 2048-bit Arb replay  
Strict verdict: **all 128 charged hit/miss positive cylinders now have a
first-core stopping time measured from the source collision state.  This
closes the time-origin gap in the twenty-third-round leaf.  It does not cover
the whole source rows or all-scale germs, normalize collision-SRB mass, bound
cemetery, or construct the induced return operator; Gates 3/4 remain open.**

## 1. The time-origin gap

The preceding leaf declared the regular suffix collision to be time zero.
That suffix occurs

```text
hit side: source -> near-grazing target -> regular suffix,  offset 2,
miss side: source -----------------------> regular suffix,  offset 1.
```

Thus suffix-relative first stopping did not by itself say that the source
state or the hit-side intermediate state avoided the frozen 24-core union.
This replay supplies exactly those missing classifications.

## 2. Strict pre-suffix classification

For each of the 64 exact charged source boxes, the certificate regenerates
the collision normal and outgoing velocity and applies one fail-closed core
classifier.  A state is outside only when each of the three cores in its
strictly determined dominant chart has a strict separating inequality.  A
chart seam, core boundary touch, overlapping enclosure, or unresolved Arb
comparison aborts the replay.

The same classifier is applied to the 64 hit-side intermediate states.  Its
independent near-grazing enclosure contains the singular `r=0` boundary
trace.  Strict outside-core separation on this larger closed enclosure
therefore covers every regular state with `r>0`; it does not call the
boundary trace regular.

```text
shared source-state rows:                              64/64 outside,
source-state references across oriented branches:       128,
hit pre-suffix intermediate rows:                      64/64 outside,
unique new pre-suffix classification rows:               128,
ambiguous classifications:                                 0.
```

The parent global-owner audit is replayed, so each hit intermediate target
remains the unique physical first collision on its positive side.

## 3. Source-relative stopping theorem

Adding the exact collision offsets to the parent stopping words gives

```text
source-relative stopping cylinders:                    128/128,
strict preterminal outside-core state count:                948,
strict terminal inside-one-core state count:                 128,
total classified states:                                    1076,
distinct destination cores:                                   14,
maximum source-relative first-core time:                       22.
```

The oriented-cylinder histogram is

```text
3:22, 4:32, 5:18, 6:8, 8:8, 9:12, 10:8,
11:4, 17:2, 18:2, 20:4, 21:6, 22:2.
```

The terminal destinations and the 14-core digest are unchanged from the
suffix-relative parent leaf.

## 4. Strict boundary

```text
SOURCE STATES OUTSIDE ALL 24 CORES:                       64 CERTIFIED
HIT PRE-SUFFIX STATES OUTSIDE ALL 24 CORES:               64 CERTIFIED
SOURCE-RELATIVE FIRST-CORE STOPPING CYLINDERS:        128/128 CERTIFIED
MAXIMUM SOURCE-RELATIVE FIRST-CORE TIME:                   22 CERTIFIED

WHOLE MAXIMAL-ROW / ALL-SCALE-GERM COVERAGE:          NOT CERTIFIED
NORMALIZED COLLISION-SRB CORE-HIT MASS:                NOT CERTIFIED
FULL PHYSICAL SOURCE/CORE FIRST-RETURN PARTITION:      NOT CERTIFIED
QUANTITATIVE COLLISION-SRB CEMETERY TAIL:              NOT CERTIFIED
POST-CORE INDUCED RETURN OPERATOR:                     NOT CERTIFIED
COMMON TWO-VIEW STRONG RESTRICTION:                    NOT CERTIFIED
GATE 3 / GATE 4:                                      NOT CERTIFIED
```

This is an entrance first-stop theorem on 128 labelled positive cylinders,
not a post-core first-return theorem for two-dimensional core rectangles.

## 5. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python -m py_compile \
  deliverables/cm2_gate34_source_relative_first_core_stopping_cert.py \
  deliverables/cm2_gate34_source_relative_first_core_stopping_verifier.py

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_source_relative_first_core_stopping_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_source_relative_first_core_stopping_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_source_relative_first_core_stopping_verifier.py \
  --self-test
```

Integrity and replay pass; `51/51` hostile mutations are rejected.  Default
live mode exits `2`, preserving the unchanged Gate-3/4 verdict.
