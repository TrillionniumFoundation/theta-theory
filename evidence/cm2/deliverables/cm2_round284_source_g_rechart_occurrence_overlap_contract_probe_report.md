# CM2 Round284 — R275 occurrence-overlap contract probe

Status: **PASS PROBE — ZERO CREDIT**

The complete 13,788-row Round275 reverse-rechart region universe was compared
with every matching frozen Round279 atom support box.  Complete ten-field
signature equality and adjacent-chart identity were already required by the
frozen Round280 incidence index; this probe classifies the exact box relation
without equating connected regions with occurrences.

Results:

- 2,476 regions are strictly contained in an existing atom support and are
  occurrence-alias candidates;
- 2,184 regions have genuine partial positive-volume overlap and require an
  exact common refinement before occurrence identity can be assigned;
- 9,128 regions have no positive-volume atom overlap and are new-disjoint
  candidates, not yet credited occurrences;
- 3,036 regions have at least one positive-area face contact;
- exact equal boxes: 0;
- atom-contained-in-region cases: 0.

Relation rows comprise 2,476 containment relations, 5,572 partial-volume
relations, and 5,544 common-face-only relations.  Face contact is component
frontier data and never an occurrence identity rule.

Seeds `284071` and `284929` reproduce the result and deterministic gzip ledger
byte-for-byte.  The formal occurrence count, DSU quotient, maximality, fibres,
global dispositions, and `Jx/Jy` glue remain unchanged.

The next occurrence-identity step is an exact refinement of all 2,184 partial
regions, followed by issuance of alias/new occurrence IDs only after the 152
true-seam corridor and endpoint pairing gate is closed.

## Independent verification

A cacheless verifier that neither imports nor executes the producer rebuilds
all 13,788 region classifications and all atom/region relations directly from
the pinned frozen inputs.  It reproduces:

- 2,476 contained alias candidates;
- 2,184 partial-overlap refinement cases;
- 9,128 new-disjoint candidates;
- 2,476 containment, 5,572 partial-volume, and 5,544 common-face-only
  relations.

`PYTHONHASHSEED=284071` and `284072` produce byte-identical verification
files.  All 17 directed resigning attacks are rejected, including dropped or
duplicated rows, forged relation owners/classes, promotion of face contact to
alias, and forged occurrence/component/maximality/Jx-Jy credit.
