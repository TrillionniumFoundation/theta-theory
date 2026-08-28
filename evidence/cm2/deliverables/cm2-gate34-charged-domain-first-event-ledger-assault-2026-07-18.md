# CM2 Gate 3/4 charged-domain first-event ledgers — 2026-07-18

## Result

This append-only leaf removes the preceding domain-typing obstruction without
reusing any selected-germ ledger.  Each exact charged positive cylinder is
registered as its own canonical Borel domain:

```text
closed charged z interval
x fixed source phase coordinate s=0
x one open actual-parameter side 0<|h|<=radius.
```

The source-relative first-core replay is joined by exact occurrence, side,
source-owner ID, suffix branch ID, source box, time, and destination.  Each
new ledger therefore has exactly one nonempty first-event slot, and that slot
equals the whole charged domain.

## Certified counts

- exact charged Borel domains: `128`;
- new domain-specific first-event ledgers: `128`;
- unique nonempty source-first-core slots: `128`;
- old selected-germ ledgers reused: `0`;
- preceding occurrence-only mismatches resolved by new domain registration:
  `124/124`;
- source-relative first-core times: minimum `3`, maximum `22`;
- strict regular preterminal states outside all 24 cores: `948`.

The finite prefix contains all core and singular first-event slots from source
time zero through the certified stop:

```text
total finite-prefix slots                  26900
unique nonempty destination-core slots       128
empty core slots                           25696
empty singular slots                        1076
total empty slots                          26772
```

At every preterminal time all 24 core slots are empty by strict outside-core
classification, and the singular slot is empty by the unique regular
collision replay.  At the terminal time the unique destination slot is the
whole domain, the other 23 core slots are empty, and the singular slot is
empty.

## Strict scope

The materialization ends at the first-core stop.  It creates:

- no post-stop slots;
- no nonreturning-cemetery slot;
- no statement about unregistered full all-scale germ domains;
- no collision-SRB mass or normalized hit fraction;
- no post-core first-return atom, tail, or induced operator.

The domains remain `(z,h)` objects with `s=0`; at fixed parameter they are
one-dimensional collision-source curves and do not acquire positive
two-dimensional collision-SRB mass from this ledger construction.

## Frozen artifacts

- `cm2_gate34_charged_domain_first_event_ledger_cert.py`
- `cm2_gate34_charged_domain_first_event_ledger_verifier.py`
- `cm2-gate34-charged-domain-first-event-ledger-manifest-2026-07-18.json`
- this report
- `cm2-gate34-charged-domain-first-event-ledger-manifest-2026-07-18.sha256`

No aggregate, root, memory, or preceding leaf was modified.

## Reproduction

```bash
.venv-neurips/bin/python -m py_compile \
  deliverables/cm2_gate34_charged_domain_first_event_ledger_cert.py \
  deliverables/cm2_gate34_charged_domain_first_event_ledger_verifier.py

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_charged_domain_first_event_ledger_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_charged_domain_first_event_ledger_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_charged_domain_first_event_ledger_verifier.py \
  --self-test

sha256sum -c \
  deliverables/cm2-gate34-charged-domain-first-event-ledger-manifest-2026-07-18.sha256
```

The verifier rejects 60/60 hostile mutations, including reusing an old germ
ledger, restoring the invalid occurrence-only join, changing domain equality,
time/core/slot identity, dropping an outside/regular guard, materializing
post-stop cemetery slots, manufacturing collision-SRB mass, or promoting a
gate.  Default live mode exits `2`.

## Verdict

```text
EXACT_CHARGED_BOREL_DOMAINS_128: CERTIFIED
DOMAIN_SPECIFIC_FIRST_EVENT_LEDGERS_128: CERTIFIED
DOMAIN_EQUAL_UNIQUE_NONEMPTY_SOURCE_FIRST_CORE_SLOTS_128: CERTIFIED
PRIOR_OCCURRENCE_ONLY_MISMATCHES_RESOLVED_BY_NEW_DOMAIN_REGISTRATION_124: CERTIFIED
FINITE_PREFIX_EMPTY_CORE_SLOTS_25696: CERTIFIED
FINITE_PREFIX_EMPTY_SINGULAR_SLOTS_1076: CERTIFIED
NONRETURNING_CEMETERY_SLOT: NOT_MATERIALIZED
COLLISION_SRB_MASS: NOT_CERTIFIED
POST_CORE_RETURN_OPERATOR: NOT_CERTIFIED
GATE3: NOT_CERTIFIED
GATE4: NOT_CERTIFIED
GATE5: NOT_CERTIFIED
```
