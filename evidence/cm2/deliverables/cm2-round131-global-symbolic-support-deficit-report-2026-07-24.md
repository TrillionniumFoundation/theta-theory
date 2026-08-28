# CM2 Round131 — global symbolic support-deficit decomposition

Date: 2026-07-24

Verdict: **VERIFIED exhaustive incidence-only decomposition of the frozen
441,280-key symbolic registry.  Eighteen words have at least one previously
certified incidence; 441,262 have no such incidence.  No global field or
Gate5 block is promoted.**

## Exact decomposition

The independent verifier reconstructs the Round127 exact-seed incidence set
and the Round128 base-R1 component incidence set from byte-pinned artifacts.

```text
exact-seed incident words                 3
base-R1 component incident words         16
symbolic overlap                          1
union touched words                      18
no-certified-incidence words        441262
global symbolic words                441280
```

The complement is represented by 19 exact ordinal runs.  Their counts sum to
441,262 and, together with the 18 touched ordinals, partition `0..441279`
without overlap or omission.

The one overlap is official word ordinal `346720`.  Round128 already proves
that this is symbolic equality only: the two witnesses do not share a
physical root, physical subbranch, or operator block.

## Core frontier

The sharpest finite next target is the set of 16 base-R1 incident official
words, organized into eight reciprocal pairs.  These words already have
certified physical component incidences and local F10/F13/F16 values.  A
promotion still requires same-root homogeneous subbranches, F1–F18 same-key
operator registration, owner/cemetery plus raw-Z/Orlicz control, and an
independent all-field verifier.

## Verification

The verifier does not import or execute the producer.  It independently
rebuilds the exact-seed set, the base-R1 set, the overlap, all 18 union rows,
and all complement runs.  Two producer and two verifier runs under distinct
`PYTHONHASHSEED` values are byte-identical.  Four fully re-signed semantic
mutations and three strict-envelope/encoding attacks fail closed.

```text
producer SHA256      8e1ef0931704b3828a00cf9e99c2870465a039dcefcde653596c2ce9147f99d3
certificate SHA256   e01ba9eb3cbd6dd4f4bdcafe7e11c7397a493ba4774315b4b440e52d177665a6
verifier SHA256      af013cc73c247ba9cc916ed848c2325ea10ea3751be64df62fafd5dc14610168
verification SHA256  259c8a1953b62c47db741cd892725ae26463b641c4c290e63a8d4ef91ded3088
```

## Frozen safety boundary

```text
positive-Borel every-exact-fibre local maturity   18/18
global complete 18-field blocks                       0
Gate5 blocks                                          0
global Gate5 maturity                             10/18
Gate5 status                              NOT_CERTIFIED
CM2                                      NO-GO_FOR_CLAIM
```

“No certified incidence” is not an empty-domain decision and is not evidence
of zero measure.  This round quantifies the exact global support deficit; it
does not solve it.
