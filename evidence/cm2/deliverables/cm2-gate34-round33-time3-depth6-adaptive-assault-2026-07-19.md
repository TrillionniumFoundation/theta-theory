# CM2 Gate 3/4 round-33 time-three depth-six adaptive assault

Date: 2026-07-19  
Verdict: **finite Q3 ledger enlarged; no uniform tail promoted**

The complete 384-bit Arb replay starts from all 114,006 certified Q2 anchors
and bisects every unresolved time-three outer cell along its longest normalized
`(t,p,s)` side through additional depth six.  It produces

```text
terminal leaves                         5,225,458
strict Q3 inner cells                     965,360
strict R3 inner cells                           0
unresolved cells                        4,260,098
```

Exact coordinate-base mass is conserved:

```text
Q3          43469813/163840000000
R3                                  0
unresolved   24955951/32768000000
total          5257799/5120000000.
```

Relative to depth four, Q3 gains 720,656 certified cells and unresolved mass
falls by the exact factor `24955951/29067244`; the relative reduction is
`4111293/29067244`, approximately 14.1441%.  The two remaining blocker classes
are 4,152,062 unresolved competitor/discriminant leaves and 108,036 outgoing
chart-or-geometry leaves.

The observed finite-depth ratio is not iterated as a uniform contraction.
Zero certified R3 cells are not retyped as physical emptiness.  Complete
limiting `R3/Q3`, survivor-conditioned recovery, a weighted return tail and
Gates 3/4 remain `NOT_CERTIFIED`.

Replay:

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_round33_time3_depth6_adaptive_verifier.py --replay
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_round33_time3_depth6_adaptive_verifier.py --self-test
```

