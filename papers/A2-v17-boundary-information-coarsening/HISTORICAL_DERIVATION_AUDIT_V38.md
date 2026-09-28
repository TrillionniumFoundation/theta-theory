# A2 v38 — historical derivations and proof dependencies

Date: September 13, 2026. This is a record of the material examined for the present revision, not a new exhaustive correctness certificate for every paper or appendix in the programme.

## Report and source chain examined

The starting point is the complete v37 referee report at `377efa79597776e75e3cc1d399c1986edd097aaf`, examining submission `6c311aa389e3af833f06f14ae98de7bfc28c1327`. Its final dispositions, required revisions, reproduced build defect and minor wording comments were read. The current entry, introduction, complete vector-information chapter, complete detailed likelihood-tilting module, complete single-offset inverse chapter, complete rank-two lattice chapter, preamble and auxiliary input wrapper were examined. The v37 historical audit was read to trace earlier forward-law work; its descriptions of earlier inspections are not claimed here as fresh re-inspections of all those files.

## 1. From the law inverse to the complete marked table

The complete source `article/23f_single_offset_law_inverse_v26.tex`, blob `63ed36efd417cd23e6f869952627719de00e6ef7`, was read together with `article/23d_rank_two_lattice_recovery_v24.tex`, blob `5e34a7c034ee8a5de0ae915a2b4c622f0f042b2c`.

The four-density identity cancels both the unknown multiplicative amplitude and its normalization. At a fixed nonzero interior anchor, strict convexity makes the scalar anchor factor positive. Recovery is signed, and local stability is in every fixed interior C^M norm; the argument does not infer high derivatives from total variation or differentiate a pointwise square root at the degenerate action minimum.

The law identity supplies the unsymmetrized actions to the retained all-order inverse; it does not replace the weighted half-line operator, finite-truncation envelope argument or smooth finite-remainder analysis. The latter dependence is explicitly preserved in the detailed composition and the native input chain. Analytic continuation is used for complete connected boundary images, not for a conclusion about arbitrary smooth images from their infinite jets.

The lattice chapter distinguishes metric recovery from complete placement. Its anchoring definition requires two signature-rigid cycles based at the same oriented channel frame. Their independent real deck directions prescribe the lattice and its Gram form after one common gauge is chosen. A rooted signature-rigid spanning tree then places every remaining obstacle orbit. Realizability supplies an admissible realization. The v38 introductory statement and proof were aligned with this precise historical chain; the detailed v37 composition was not weakened or replaced.

## 2. From null likelihood normalization to original-law risk

The full vector-information source and the full detailed module `article/18a2_likelihood_tilting_moments_v34.tex`, blob `b6f74b4d5cbf6e1065af521dc7364dab98445b38`, were examined together. Three logically different steps remain separate.

First, null LAN and unit likelihood means yield uniform integrability by bounded truncation. A strictly positive limiting likelihood gives reverse contiguity directly under the null. This part uses neither an alternative central-sequence limit nor the later unbounded-risk conclusion. The v38 short proof now says so and points to the existing detailed argument.

Second, the density expansion before division by the linearly vanishing defining function gives the mean under each original local alternative. Centering the independent summands under that same alternative controls their fourth moment. With ell = log(1/delta), q = delta ell^(1/4) and B = np delta^2 ell tending to one, the truncation-mean budget is B ell^(-3/4), the second-moment budget is B(1 - log(ell)/(4 ell)), and the single-sum fourth-moment budget is B ell^(-3/2). Restoring the bounded mean gives uniform integrability for quadratic loss on the fixed identifiable quotient. The actual excluded observation has contribution zero; a censoring event elsewhere does not erase the rest of the sample.

Third, likelihood-vector convergence on finite sets is not identified with compact-parameter deficiency convergence. The uniform moving-boundary modulus and finite-net argument remain separate native inputs. The present revision changes no information matrix, rate, parameter set, observation level or compact conclusion in that chain.

## 3. Historical finite diagnostics

The exact preceding-referee script, blob `39f24673fc43580fcc8c7f39d79f26cfa9138d01`, was read, verified against its Git and SHA-256 identities and executed without modification. Its six diagnostic families all passed in normal and optimized Python. The source itself states the limitations: finite checks are not proofs; the radial probability models are not asserted to come from billiards. Its historical manuscript identifier remains historical. The current [execution ledger](VERIFICATION_V38.md) records a new execution rather than relabelling an old output.

## 4. Build provenance and the native companion

The old builder's recorder handling was examined against the report's concrete counterexamples. The replacement tests actual compilation bytes against frozen Git objects, and its negative controls exercise the exact driver. The preamble's external reference to the native companion led to explicit generated-auxiliary transfer rather than an unexplained local input. Genuine TeX integration tested this dependency on a labelled miniature repository.

The complete `two_collision.tex` was also read and recovered byte-for-byte. Its stationary suspension identity, complete short-flight transversality, regular terminal level and finite-order moving-level differentiation remain unchanged. The new execution builds this actual native companion only. The complete main was not built, and the inherited forward-law, analytic matching, stopped-transfer and global acquisition proofs have not all received a fresh line-by-line audit in this session.

## 5. Preservation and unexamined scope

The [preservation record](PRESERVATION_V38.md) gives the exact three-file mathematical diff and the unchanged dependency identities. The latest referee's bounded accepted findings are retained as dispositions, not converted into a fresh universal endorsement. No exhaustive literature, novelty or top-journal acceptance audit is claimed. The requested complete-main build and visual delivery remain the explicit open item C2, distinct from the manuscript revisions and the repaired source-provenance implementation.
