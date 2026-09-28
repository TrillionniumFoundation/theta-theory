# Preservation and submission boundary

## Immutable starting point

Repository: `TrillionniumFoundation/theta-theory`.

The revision is an additive child of the v87 review commit `976d23ef269126e68dd90c4c9d3184ee67ff0b54`, whose tree is `409f4ee5b4669da774a4782ca1ea776d7d8253d4`. That review is a child of the reviewed v87 source commit `4304524ff671bf1ff57217b3d288923405c7ca03`.

The existing principal source `papers/A2-v17-boundary-information-coarsening/article/v87/paper.tex` has Git blob `45abc130f8bcebb347abbe895498b1a568bc7e7b`. The controlling report has Git blob `e5272a1fb231aabd26b2cfc2c334a374d78cdedd`. The 64-character source digest printed inside the report is not used as a Git blob identifier.

Every inherited path is retained unchanged. This includes the v87 principal article, `rigidity_v87_companion.tex`, all files it includes, earlier revisions, historical detector and geometric derivations, reviews, and existing workflows. Only the new revision branch is updated. No main-branch merge, force push, report rewrite or archive deletion is part of this revision.

## Principal article and archive

The formal v88 article is `rigidity_v88.tex`, which inputs the new `article/v88/paper.tex` and six new modules. Its proofs are self-contained. The preserved 122-page v87 companion remains an archival reference; it is not a 122-page proof prerequisite attached to the new principal theorem. The revision does not need a renamed copy of that companion to preserve its mathematics.

## Mathematical correspondence

| v87 content | v88 location |
| --- | --- |
| Three-clock pole reconstruction; exact fixed-channel two-clock fibre | Lemma 3.1; embedded in the degree-d normalization theorem |
| Arbitrary-rank one-sided gap-free action inverse | Theorems 1.1 and 3.2; Proposition 3.4 |
| Intrinsic observation-fibre envelope | Retained as theta_*; strengthened by observable eta in Theorem 3.2 |
| Simple/repeated spectral factor reconstruction | Proposition 3.4, with the alternative-representation rank step made explicit |
| Compact residual modulus and honest sets without signal floors | Lemma 5.1 and Theorem 5.2 |
| Arbitrary-rank fixed-marginal product family | Lemma 5.3, with an additional observable leading-singular-value identity |
| Full-spectrum-collapse family | Lemma 5.3 |
| Minimax transition and adaptive clock lower bounds | Theorem 5.4, now also on eta classes |
| Binary determinant and relative-throughput implications | Section 6 |
| Original logarithmic observation law | Section 6, unchanged |
| Shared spatial, other detector and geometric regimes | All inherited archive sources unchanged; their distinct roles explained in Section 6 |

The archive is not deleted to make the article shorter. Conversely, preserving it does not assert that every historical regime has the new polynomial or affine modulus.

## Machine-checkable preservation

Run from the repository root:

```sh
git diff --name-status 976d23ef269126e68dd90c4c9d3184ee67ff0b54 HEAD
git hash-object papers/A2-v17-boundary-information-coarsening/article/v87/paper.tex
```

Every diff entry must be an addition; the hash must equal the value above. The branch workflow also runs `verification/verify_v88.py --review-base 976d23ef269126e68dd90c4c9d3184ee67ff0b54` and fails on any modification or deletion of an inherited path. The local manuscript-only build did not pretend to run this full-repository check; its actual scope is recorded separately.
