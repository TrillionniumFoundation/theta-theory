# CM2 Round185 — preconditioned C0/C1 residual refinement

Date: 2026-07-26  
Verdict: `PARTIAL_PRECONDITIONED_C0_C1_RESIDUAL_REFINEMENT__NO_WHOLE_PARENT_PROMOTION`

## Frozen input and scope

Round185 pins the complete Round183 package and processes all of its
remaining carriers:

- 25,040 dynamic residual outers;
- 530 inherited collision1/source-seam carriers;
- 25,570 combined inputs;
- exact combined input coordinate volume
  `697725681/26843545600000`.

The dynamic pipeline applies one additional bounded split to non-`H2`
residuals.  The `H2` pipeline first uses the exact factorization

`H2=(n2_x+n2_y)(n2_x-n2_y)=h_plus*h_minus`

and then applies at most two additional transverse splits to the remaining
factor-existence residual.  Inherited carriers receive one additional
bounded split.

Centered mean-value C0 bounds, full-box automatic C1 bounds, strict
corner-segment brackets, and signed-factor separation are recorded
separately.  A strict derivative is only regularity if a zero exists; it is
not used as an existence proof.  Likewise, rank two is never used to infer
intersection existence.

Frozen Round185 artifacts:

- producer SHA256:
  `7b48f3ee3417fcfdf5ef6c852e0ab591eb849b357e704e46ee3aaa259d20acc2`;
- certificate file SHA256:
  `2034e939a6046cd36f749546ab8dc2c0a004b3325c803b5335a3f5e34831fff1`;
- certificate result SHA256:
  `ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf`;
- certificate byte count: `106,100,901`;
- verifier SHA256:
  `88d5b72c68ba216a1c807b868156c8e0da7e9e63db968eda5b5a66dd86d5651f`.

## Exact output census and conservation

| Ledger | Output outers | Exact coordinate/support volume |
|---|---:|---:|
| Dynamic local exact-key cells | 19,050 | `1105719/13421772800000` |
| Dimensionally arranged nonempty `H2` seams | 4,468 | `668529/26843545600000` |
| Dynamic residual | 15,830 | `876681/13421772800000` |
| Inherited local exact-key cells | 0 | `0` |
| Inherited local exclusions | 170 | `1947/409600000` |
| Inherited residual | 890 | `6903/327680000` |

The dynamic identity is exact:

`1105719/13421772800000 + 668529/26843545600000
+ 876681/13421772800000 = 4633329/26843545600000`.

The inherited identity is also exact:

`0 + 1947/409600000 + 6903/327680000
= 42303/1638400000`.

The 14,838 recorded split faces account for the output-count expansion:

`25,040 + 530 + 14,838 = 40,408`.

The combined remaining residual is 16,720 outers with exact volume
`283623561/13421772800000`, approximately 81.30% of the frozen combined
input volume.  The integer census delta is zero.

The dynamic residual statuses are:

- 4,170 `ACTIVE_DELTA_1`;
- 220 `ACTIVE_DELTA_2`;
- 592 `H2_FACTOR_EXISTENCE_RESIDUAL`;
- 9,076 `POINT_WINNER_NONSTRICT`;
- 1,772 `WALL_ENDPOINT`.

The 890 inherited residual outers consist of 440 collision1 Delta/root
collars, 312 collision1 outgoing-chart collars, 98 collision1 root-order
collars, 8 point-winner-nonstrict descendants, and 32 source-chart seam
collars.  The 170 exclusions are local to the frozen collision1 live
stratum and carry zero global credit.

## `H2` factor result

All 11,908 incoming `OUTGOING_H2` boxes have strict full-box derivatives in
the original `t` and `p` axes.  None has a complete original-axis or
oblique-face bracket, and none has an original-axis or oblique
interval-Newton self-map.  This explicitly prevents regularity from being
misreported as existence.

Centered C0 evaluation of `H2` directly proves 6,380 boxes strict.  Exact
signed-factor analysis then obtains:

- 6,904 boxes with both factor zero sets absent by centered C0 bounds;
- 4,468 boxes with one independently nonempty regular factor graph and a
  dimensionally retained 2D seam arrangement;
- 592 terminal factor-existence residual outers;
- zero boxes in which both factor zero sets overwrap;
- zero simultaneous `h_plus=h_minus=0`, excluded by
  `n2_x^2+n2_y^2=1`.

The 4,468 nonempty seams are retained once as 2D carriers.  They are not
ambient 3D closures and do not generate whole-parent credit.

## Dimension ledger and nonpromotion

Round185 independently reclassifies all 14,838 half-open 2D split faces;
5,002 faces have different child statuses.  Their dimension ledger contains:

- 12,636 nominal boundary-surface 1D intersection outers;
- zero certified nonempty transverse 1D intersections;
- 118,704 raw 0D corner occurrences;
- 20,986 unique 0D corner keys;
- zero certified 0D boundary-incidence credit.

The two-Delta ledger contains 14,232 outers with strict rank two conditional
on an intersection.  It certifies zero intersection existences, zero unique
1D incidences, and zero 0D multiple incidences.

All 16 live parent strata remain partial.  Whole-parent/stratum promotions,
integer census delta, and global credit are all zero.  Local Gate5-key
observations at ordinals 290575, 291560, 321111, and 322097 remain local.

## Verification and reproducibility

The formal verifier pins the Round185 producer as inert bytes and neither
imports nor executes it.  It rebuilds the complete 106,100,901-byte
certificate result from the frozen Round183 chain and requires full
canonical equality.

The official verification is `PASS`:

- verification result SHA256:
  `b63c15eabc468192c113d7221c7adfd37fec94aa38f4b02c97acb25598962cf6`;
- verification file SHA256:
  `bda1286ec582f17724b6478e3af98973280f482bf9192235f96842c55513642e`;
- independently rebuilt certificate result SHA256:
  `ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf`;
- full expected-result canonical equality: true;
- re-signed semantic attacks rejected: 32/32;
- strict JSON attacks rejected: 9/9;
- path/type/output attacks rejected: 11/11.

The semantic suite covers C0/factor censuses, forged Newton and bracket
successes, rank-versus-existence separation, split-face ownership and
reclassification, 1D/0D credit, source-seam ownership, parent completion,
Gate5, D02, CM2, and exact volume conservation.

Producer seed `185052` and verifier seed `185062` cold replays are
byte-identical to the official certificate and verification respectively.
Commands, timings, memory use, hashes, and comparisons are recorded in the
cold-replay note.

The required runtime is `.venv-neurips/bin/python` (Python 3.12.3),
python-flint 0.9.0, with effective Arb precision 384 bits.  The system
`python3` in this workspace does not provide `flint`.

## Independence boundary and hardening limitations

The verifier is process- and provenance-independent from the Round185
producer, but it is not an implementation-diverse mathematical checker.  A
source audit found 67 of 72 common-named functions AST-identical, including
the result-building algorithm.  It therefore gives strong canonical
reconstruction and tamper detection, while a common algorithmic error could
survive both implementations.

The local upstream Python modules are imported before their later byte-pin
validation.  A pin mismatch still makes acceptance fail closed, but the
program is not a security sandbox for a malicious working tree.
`lstat()` followed by `read_bytes()` also leaves a narrow concurrent
replacement window, and the output path policy is broader than a single
fixed filename.  These limits do not change the frozen-data result but
constrain the verifier's adversarial-filesystem claim.

## Global state and next core gate

Round185 issues no global promotion:

- `D02 = BLOCKED`;
- Gate5 remains `10/18`;
- complete 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.

The next bounded gate is to continue only the 592 `H2` transverse
factor-existence residual cells, then apply centered/Krawczyk treatment to
the Delta/root-order residuals and the inherited collision1/source
carriers.  A global promotion remains forbidden until every required
dimension under the same exact key closes.
