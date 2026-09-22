# Preservation and proof dependencies

The immutable source boundary is v114 at `d58d4ad0546487f4313cf8ed2f05ad9321b54e63`. The controlling report is R114 at `09869129e16fd43bd2420fa3573a09cd5cbbdff9`.

## Preservation

All 19 reviewed TeX files are archived byte-for-byte in `history/v114_source/`, with SHA256 hashes in `evidence/V114_SOURCE_MANIFEST.json`. The 26 materialized source-pack file hashes were checked when the upstream artifact was retrieved. Thirteen of the 19 active files remain byte-identical. The changes to the others are additions to the introduction, exact-germ/wall/priority structure, new bibliography entries, a rewritten abstract, and one repair of a malformed `Sing(D)_{m red}` typesetting command to `Sing(D)_{\mathrm{red}}`.

The verifier confirms all 136 old theorem/lemma/proposition/corollary/proof environments are retained (with only that documented typesetting normalization), all 169 old labels survive, and all 25 old bibliography keys survive. The current manuscript has 201 labels and 27 bibliography keys. No old chapter is silently replaced by a shorter summary. The complete manuscript includes every appendix; the two reading copies are alternate compilations, not content removal.

## Principal new dependencies

| Statement | Proof inputs | What is not inferred |
|---|---|---|
| Joint polar relations | Intrinsic kernel/cokernel derivative; differentiation of the multiplication map | No direct-sum reduction of multi-annihilator relations |
| Exact residual matrix germ | Schur elimination; analytic coordinate theorem; intrinsic derivative | No identification of all nonlinear terms with their linearization |
| Transverse determinant model | Surjective intrinsic derivative; generic minor geometry | No assertion that transversality holds in arbitrary systems |
| Minimal corank-one equations | Incidence isomorphism; polar tangent dimension; implicit function theorem | Complete intersection asserted only with expected local codimension |
| Simple normal determinant | Smooth contained branch; simple zero of the normal determinant | Reducedness is concluded locally, not assumed |
| Higher hyperplane support/coranks | Rank-two Hankel characterization; pencil propagation; split/tangent monomial products | No transfer of a two-point-sector count to all contacts |
| Hyperplane regularity off C_n | Explicit plane derivative rank n and residual image dimension mn-3 | Not merely generic distinct-support smoothness |
| Saturation and associated points | Regularity off C_n; maximal-minor order at C_n; secant quadratic initial form; SL2 equivariance | No global primary decomposition in the unrestricted quadratic excess regime |
| Nilpotency lower bound | Order(F^j)=2j and J_m contained in the m-th maximal-ideal power | No assertion that the bound is sharp |

The old native and statistical appendices are not assumptions in the geometric theorem. Their internal hypotheses and distinctions between experiments are preserved.
