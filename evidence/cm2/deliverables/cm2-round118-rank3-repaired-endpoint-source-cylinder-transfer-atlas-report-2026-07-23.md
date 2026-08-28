# CM2 Round118 — repaired endpoint identity / source-cylinder transfer atlas

## Result

Round118 closes one narrow but necessary identity/coordinate-transfer gap:

- all `8/8` preserved source-grazing incidences have a unique, independently replayed
  `face ↔ registered port ↔ natural trace ↔ HIT/BYPASS sheets ↔ root stitch ↔ nofold root`
  crosswalk;
- all eight withdrawn Round102 endpoint IDs are retained only as traceability aliases;
  `0/8` are reused in the repaired identifiers;
- all eight repaired identifiers are freshly minted from the preserved face ID, port ID,
  branch key, Round113 trace ID, and the two Round112 sheet IDs;
- the local source-cylinder transfer is exact for source component `G`, radius `R_G=9/25`;
- the Round115 projective coordinate `q` transfers to physical momentum `p` as a closed-interval
  C1/bi-Lipschitz coordinate with
  `1/1001 < |dq/dp| < 10` on the positive-`c0` overlap and the corresponding finite-difference
  bound at the endpoint.

The independent verifier passes `42/42` hostile mutations.  The result is intentionally
fail-closed: it does not install a whole-face transfer, physical-owner whole-trace atlas,
positive reach, other-singularity separation, two-sided physical collar, standard-curve
child, canonical recut, or any Gate5 field.

## Why the endpoint identities had to be repaired

Round111 classifies Round102 as `PARTIAL_COMBINATORIAL_FACE_LEDGER`.  It preserves exactly
the 12 face IDs, 120 registered ports, 108 internal links, and source-grazing
event-type/candidate incidence.  It withdraws the broad terminal brackets and their endpoint
IDs, endpoint completeness, whole-domain physical completeness, and the associated
zero-residual statements.

Therefore Round118 uses a Round102 source-grazing row only through:

1. its preserved `SOURCE_GRAZING` incidence type;
2. its preserved face ID;
3. its mated registered port ID;
4. its candidate/branch incidence obtained from that preserved face.

The old `source-grazing:*` identifier is copied into
`withdrawn_round102_endpoint_id` with status `TRACEABILITY_ONLY_NOT_REUSED`.  It is not an
input to the repaired-ID digest.  Terminal parameter brackets and Round102
`endpoint_complete` are not used.

## Eight-row identity atlas

The table displays digest prefixes; the certificate contains every full identifier.

| ray | face digest | port digest | source charts | Round113 trace digest | repaired endpoint digest |
|---:|---|---|---|---|---|
| 0 | `fb2cd8f68dd1` | `5280d18a5f9e` | `E→S` | `7c4b3a644823` | `3af6664a7d4e` |
| 1 | `42a7bdb3d568` | `a61c4be9be1e` | `E→N` | `e8ac46873966` | `3d6f7d1869c3` |
| 2 | `89bea948a8f8` | `259a99847c78` | `N→W` | `94dad4d1e232` | `c6d6f684c779` |
| 3 | `545b8a628b96` | `7fe25667a85b` | `N→E` | `9fef6e45cc0c` | `021737e7b569` |
| 4 | `e3c162741642` | `24fa16d9eebe` | `S→W` | `5111655df189` | `41218e9c292f` |
| 5 | `455f5408cde3` | `a976f0d86446` | `S→E` | `b6270c3fa7d5` | `263c2564c534` |
| 6 | `51b24804178f` | `6560602edb3c` | `W→S` | `774d312baa3c` | `b51512b792e8` |
| 7 | `adf0662ca30c` | `2953fea26eae` | `W→N` | `7fdca2011313` | `e5e288e88fae` |

For every row, the verifier independently checks:

- equality of the branch key reconstructed from the Round102 face and the branch keys in
  Rounds112–115;
- equality of projective end across the preserved incidence, Round114 seam bridge, and
  Round114 root stitch;
- equality of the adjacent source chart across Rounds102, 112, 114, and 115;
- equality of the incident HIT/BYPASS sheet IDs across Rounds112–114;
- positive Round114 seam width and replayed selected-owner clearance;
- Round114 root-edge coverage and Round115 q-injectivity/nofold;
- uniqueness and disjointness of the eight repaired IDs and eight withdrawn aliases.

## Exact source-cylinder metric transfer

The physical source cylinder is tagged by its component.  On component `G`, write

`P = (G, r, p)`, with `r = R_G θ` and `R_G = 9/25`.

Its physical product metric is

`d_phys² = (9/25)² dθ² + dp²`.

This is not the unit-normal reference metric.  For comparison only, define

`M = (G, n_x(θ), n_y(θ), p)`

with product distance

`d_ref² = ||n(θ₁)-n(θ₂)||² + |p₁-p₂|²`.

The component tag `G` is mandatory: normals and momenta on different cylinders must not be
identified.  Each audited old/adjacent chart pair admits an unwrapped angular difference
`0 ≤ δ ≤ π`.  If `h = 2 sin(δ/2)` is the unit-normal chord, then

- `h ≤ δ`;
- concavity of sine on `[0,π/2]` gives `h ≥ 2δ/π`;
- `(9/25)π/2 < 1`, certified rationally using `π < 22/7`, gives `(9/25)δ ≤ h`.

Consequently, on each of the eight audited chart unions,

`(9/25) d_ref ≤ d_phys ≤ d_ref`.

For a C2 parameterized curve in the same chart union,

`(9/25)|M'| ≤ |P'| ≤ |M'|`

and

`|P''| ≤ |M''|`.

The last inequality follows from

`||n''||² = (θ'')² + (θ')⁴`,

while `P''=((9/25)θ'',p'')`.  These are coordinate-transfer estimates only.  No positive
reach, global self-separation, whole-face atlas, or transverse collar follows from them.

## Exact `q ↔ p` endpoint transition

Round115 supplies, on every root edge `0 ≤ c0 ≤ 1/16384`,

- `p(c0)=σ0 sqrt(1-c0²)`;
- `q'(0)=0` exactly;
- `|q'(c0)/c0| > 1/1000` for `c0>0`, with fixed sign;
- `|q''(c0)| < 10`.

The stationary identity and the q-second-derivative bound give

`|q'(c0)/c0| < 10`

for `c0>0`.  Also

`dp/dc0 = -σ0 c0/sqrt(1-c0²)`,

so

`|dq/dp| = |q'(c0)/c0| sqrt(1-c0²)`.

Exact rational comparison at `c0≤1/16384` gives

`sqrt(1-c0²) > 1000/1001`.

Therefore

`1/1001 < |dq/dp| < 10`.

The derivative sign is constant.  Integration supplies the same strict finite-difference
bound for any two distinct root parameters, including a pair with one endpoint `c0=0`.
The C2 regularity of q in `c0` and `q'(0)=0` give a C1 q-as-a-function-of-p endpoint
extension.  No C2 `q→p` claim is installed: Round115 does not supply the q-third/odd-term
control required for a second p-derivative at the grazing endpoint.

Moreover `p(0)=σ0` lies on the momentum boundary, so `c0=0` remains in the source-grazing
singularity ledger.  The transition does not create a uniform positive two-sided physical
collar at the closed endpoint.

## Independent verification and attacks

The verifier imports no producer code.  It reparses and byte-pins the six upstream JSON
certificates plus the two formula-source files, independently reconstructs every join and
repaired ID, and redoes the rational inequalities.

Strict parsing rejects duplicate keys at any depth, floating JSON numbers, NaN, and Infinity.
The 42 hostile cases include schema and signature substitution, old-ID reuse, repaired-ID,
face, port, trace, chart, component and radius substitutions, metric/bound inflation,
whole-face/C2/collar/reach/Gate5 promotions, singular-ledger removal, upstream-pin mutation,
row deletion, unknown row/result fields, booleans masquerading as zero counts, and malformed
strict JSON.  Parser attacks cover floating numbers, overflowing exponent notation, NaN,
positive/negative Infinity, top-level arrays/null, negative zero, overlong integers, UTF-8
BOM, and unpaired Unicode surrogates.  All gate and count fields use exact integer type checks;
all certificate fraction fields are compared as exact canonical strings.

Final verified byte hashes:

- producer: `bfd517d6dd71aa923ed89400719302bd022945db9cce38e4b74f163ed0fa45f4`
- certificate: `91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f`
- verifier: `c011c6eb502fddba6e06aa16ec74d01edce3d1d42163203e4a6c717f33d38c97`
- verification: `240b9f0dc15257b5dd9309acdc2129910f5a2a8231cc9afc45f0739b258fd85b`

Two clean temporary-directory replays independently regenerated the certificate and
verification.  Both replay pairs and the canonical artifacts were byte-identical:

- certificate replay A/B/canonical:
  `91bd73445fd13eeb759e932b0626ba64acef1f10a061d6d416577dfd96feb34f`;
- verification replay A/B/canonical:
  `240b9f0dc15257b5dd9309acdc2129910f5a2a8231cc9afc45f0739b258fd85b`.

## Gate discipline

Round118 changes no frozen upstream file and makes no gate promotion:

- Gate5 remains `10/18`;
- complete 18-field operator blocks remain `0`;
- F1–F6 actual-child fields remain `{0,0,0,0,0,0}`;
- actual standard-curve children remain `0`;
- canonical recut instances remain `0`;
- CM2 remains `NO-GO_FOR_CLAIM`.

The next geometric step may use this repaired identity/coordinate atlas as an input, but it
must independently prove any whole-trace reach or self-separation statement and must keep the
closed grazing endpoint fail-closed unless a genuine endpoint-compatible collar theorem is
added.
