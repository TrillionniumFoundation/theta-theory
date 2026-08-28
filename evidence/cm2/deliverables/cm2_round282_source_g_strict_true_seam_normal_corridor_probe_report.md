# CM2 Round282 — strict true-seam normal-corridor probe

Status: **PASS PROBE — 24 PATCHES FAIL-CLOSED — ZERO CREDIT**

For every Round268 patch side and every candidate Round275 strict region, the
probe extends the rational adjacent-chart region to a 128-bit dyadic outer
enclosure containing the algebraic endpoint `t=±sqrt(1/2)`.  It then recomputes
the complete dynamic return signature on the whole outer corridor.  Only a
byte-exact match with the frozen Round275 ten-field signature is accepted.

Results:

- 152 true-seam patches / 304 directed endpoints audited;
- 2,660 strict normal-corridor candidates accepted;
- 264/304 directed endpoints have exact full `p×s` corridor coverage;
- 128/152 patches have full bidirectional strict coverage;
- 40 endpoints on 24 patches retain positive unresolved area;
- every residual is an explicit outgoing-chart-seam arrangement tail.

The remaining 24 patches are not treated as precision tails.  Their missing
area must be split by the regular zero graph of the outgoing equality and each
side-sign corridor must be connected separately.  Until that is done, this
probe emits zero cross-chart component edges and does not alter the DSU.

Seeds `282071` and `282929` produced byte-identical ledger and result files.
The deterministic gzip ledger passed decompression.

An independent verifier that neither imports nor executes the producer rebuilt
all 152 patches, all 304 directed sides, all 2,660 accepted whole-corridor
signatures, and every exact footprint union from the frozen R275/R280 inputs.
It reproduced the `264 + 40` side split and the `128 + 24` patch split.  All
13 semantic/serialization/promotion attacks were rejected; verifier seeds
`282071` and `282929` were byte-identical.

Frozen baseline remains: quotient 63,224; expanded occurrences 126,468;
maximality 0/63,224; fibres 0/116; global dispositions 0/224,580; Gate5 10/18;
D02 blocked; CM2 `NO-GO_FOR_CLAIM`; `Jx/Jy` glue credit 0.
