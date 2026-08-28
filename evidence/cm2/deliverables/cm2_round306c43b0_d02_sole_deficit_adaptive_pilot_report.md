# Round306C43B0 sole-deficit adaptive pilot

Run: `2026-08-11 15:27 CST (+0800)`  
Status: `PASS_READ_ONLY_C43B0_ADAPTIVE_PILOT__ZERO_CREDIT`  
Formal effect: none

The read-only pilot is SHA-pinned to the installed C42 f1 authority and the
audited C41/C40 lineage.  Its source SHA256 is
`00c03e5a9f869a917649d49137f2aece69357e0e9a073e59f9e2d990b0365609`.
It held every authority input open across the computation, replayed the C42
installed-state auditor, and verified that the watched runtime directory tree
was byte- and identity-stable.  It created no candidate, receipt, checkpoint,
or authority object.

The post-C42 zero-surface inventory contains five remaining sole-deficit
representatives: pairs 97, 211, 592, 664, and 715.  Starting at each exact C41
residual path, the pilot continued the same 384-bit C41 router with adaptive
longest-axis dyadic splitting.  A leaf stopped only on a D02-A exit class or
an operational checkpoint.  With maximum additional depth three and 127
route evaluations per pair, no checkpoint was reached.

```text
pair   splits   leaves   deepest +depth   terminal class
  97        2        3                2   3 x collision-two owner mismatch
 211        2        3                2   3 x collision-two owner mismatch
 592        1        2                1   2 x collision-one word mismatch
 664        3        4                3   4 x collision-one word mismatch
 715        1        2                1   2 x collision-one word mismatch
total       9       14                    14/14 TERMINAL_EXCLUDED
```

For every pair the emitted adaptive leaves are prefix-free, their exact
relative Kraft sum is one, and their absolute covered parent fraction is
`1/512`.  Aggregate work was 23 route evaluations and nine splits.  There
were zero collision-3-ready leaves and zero residual checkpoints.  The
depth-three pilot report object was
`be81084c36d959f3841121c0887190c9253e913da6d49e30acf9de740af4a5a5`.
A separate depth-four replay was deterministic across two runs and produced
object `3db5ddd1a2cb9dd267befeb9b15019efe68c285bb7b862453faf6d1f35251624`.

These results establish a high-confidence finite target for a formal C43
producer, but they do not grant whole-parent credit.  Formal promotion still
requires independent representative and reflected terminal recomputation,
all internal and external face/corner/half-open ownership certificates, the
global incident-cell census, exact 862-parent conservation, a manifest,
execution receipt, independent hostile audit, and a separate authority
installation.  Only after all of those pass may the anticipated census move
from 574 paired / 1,150 unresolved to 584 paired / 1,140 unresolved.
