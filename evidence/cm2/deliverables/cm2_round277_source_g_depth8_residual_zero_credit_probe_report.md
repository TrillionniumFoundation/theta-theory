# CM2 Round277 full depth-8 residual probe

Status: `ZERO_CREDIT_PROBE`

The exact 89,792-row depth-4 residual ledger was replayed through face depth 8.
Cells carrying a strict complete signature different from the requested
signature were safely pruned; only cells still reporting an active
outgoing-seam or wall transition were subdivided.  Every newly found positive
MATCH patch was then checked with correctly oriented inward corridors on both
incident sides.

## Exact result

- source depth-4 residuals: **89,792**
- new positive MATCH patches: **57,124**
- new edges with both inward corridors: **57,124**
- corridor or orientation failures: **0**
- remaining depth-8 fail-closed tails: **32,668**
- residual candidate-index SHA256:
  `b38984f7d5de2bece1a08b970c8acc05ac745c3e8cfea76ee8394d2d35f17a2f`

By active family:

- outgoing-chart seam: **54,428 found**, **31,372 residual**
- wall endpoint/count transition: **2,696 found**, **1,296 residual**

Remaining tails by source-round pair:

- R208/R208: **5,028**
- R208/R269: **7,904**
- R269/R269: **18,088**
- R270/R270: **352**
- R271/R271: **1,232**
- R272/R272: **64**
- R269/R271: **0** (all four closed)

The original Round277 candidate universe now has **298,056** probe-level local
edge witnesses in total: 240,932 from depth 4 plus 57,124 from depth 8.  The
remaining 32,668 rows require explicit outgoing-seam or wall arrangements;
they are not certified absences.

## Artifacts and hashes

- probe source SHA256:
  `3b8e2b220f62224884944ea04fc1a73e92342502c7f4c949e0ce3588d986c1bb`
- result JSON SHA256:
  `88a10b85f88420e90e5bfa1e37cea3943f41107a636e44f89ccb42e67350ba99`
- 57,124-row accepted ledger SHA256:
  `fe6ea98eb8a374448378940677899360f5bb3d86c3fd5e32c4f994f05a1d603e`
- 32,668-row residual ledger SHA256:
  `f585628173548ec1cae60dc809633b762fa4ebe4802c781e2133c9ea0d2c02cd`
- accepted witness-row digest:
  `1754e4c060c682932f25b9cbc07aab06dc7bb54bd16f0d938e4f19496edc2e5d`
- structural ledger verification SHA256:
  `67646222933ff4f3c5a499f2e739b58777bd8b1abf2ac71277d3b5f7d2be9c7c`

The structural verifier checks exact accepted/residual partition, positive
patch dimensions, correct geometric inward direction, and corridor containment.
It is not yet the independent dynamic-evaluator recomputation required for a
formal certificate.

All results remain probe-level.  No occurrence, component-edge, rank,
quotient, maximality, fibre, disposition, seam, or `Jx/Jy` credit is issued.
CM2 remains `NO-GO_FOR_CLAIM`.
