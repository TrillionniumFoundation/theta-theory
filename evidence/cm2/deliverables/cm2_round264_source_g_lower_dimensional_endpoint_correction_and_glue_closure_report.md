# CM2 Round264 Source-G Lower-Dimensional Endpoint Correction and Glue Closure

Round264 revisits the 248 Round252 `t`-face contacts that were previously
carried only as unresolved lower-dimensional endpoint data.  The exact
Source-G coordinate on this channel is `(9/25)t`.  Reconstructing the pinned
Round234/235/248 lineage shows that the 400 associated one-sided endpoint
cells each contain one nominal Round248 3D branch with empty physical
support.

## Exact correction

- Distinct Round235 endpoint cells: 400.
- Empty `EVENT_ABSENT` branches: 184.
- Empty `EVENT_PRESENT` branches: 216.
- Empty Round248 bulk nodes removed: 400.
- Invalid `EVENT_ABSENT` sheet-owner edges removed: 184.
- Empty `EVENT_PRESENT` singleton phantom components removed: 216.
- Quotient after phantom pruning: `68,716 -> 68,500`.

The retained endpoint sheets are not empty.  Exact common refinements give
248 positive-area sheet identities:

- rank-reducing edges: 184;
- redundant certified edges: 64;
- common-area histogram:
  `1/102400:48`, `1/51200:16`, `1/25600:40`, `1/12800:88`,
  `1/6400:48`, `1/3200:8`;
- total exact common area: `123/6400`;
- quotient after sheet identities: `68,500 -> 68,316`.

The 32 frozen Round204 tail pairs are then cross-checked through their
3D/2D/1D lineage.  They contribute four rank reductions and 28 redundant
certified glues, giving the corrected Round264 quotient:

`68,316 -> 68,312`.

The corrected quotient contains 10,904 occurrence-bearing (`B`) components
and 57,408 zero-occurrence carrier (`Z`) components.  It preserves 53,968
inherited local occurrences and 116 exact keys, and rebuilds the complete
133,284-node valid virtual frontier after removing the 400 empty bulk nodes.

## Independent verification

The independent verifier does not import or execute the producer.  It pins
all upstream files and the producer bytes, reconstructs the complete expected
certificate before opening the candidate, checks every row closure and
conservation identity, requires strict canonical-JSON byte equality, and
rejects `12/12` semantic, `17/17` strict-JSON, and `8/8` file/path attacks.
Its frozen status is `PASS_INDEPENDENT_ROUND264`; both fixed hash seeds are
required to produce byte-identical certificate and verification documents.

## Scope correction and strict non-promotion

Round264 closes the endpoint correction and glue channels over the inherited
post-Round263 frontier.  A subsequent ancestry audit found that this
53,968-row frontier is the residual-derived subset
(`17,192` Round179, `736` Round204, `36,040` Round208), not the whole observed
Source-G positive-volume universe: Round174 also contains 72,500 separately
materialized strict 3D occurrence rows.  Round265 therefore expands the
working universe to 126,468 occurrences before any maximality or fibre claim.

Accordingly Round264 grants:

- lower-dimensional identity/glue edges: 280;
- component-union credit: 188;
- maximal-component credit: 0;
- globally exhausted exact-key fibres: `0/116`;
- global exact-key dispositions: `0/224,580`;
- `Jx`/`Jy` same-point glue credit: 0.

Gate5 remains `10/18`, D02 remains `BLOCKED`, and CM2 remains
`NO-GO_FOR_CLAIM`.

Next: expand by all 72,500 Round174 occurrences, saturate only the
full-signature safe face channel, close the remaining curved face channel,
then audit all lower-dimensional carriers before attempting expanded
component maximality and the 116 exact-key fibres.
