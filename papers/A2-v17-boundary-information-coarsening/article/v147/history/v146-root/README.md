# A2 revision 146 — referee reading guide

The principal review object is **geometry.pdf**, built from geometry.tex. The presentation uses theorem/proof-centered AMS mathematical typography, not a conference template. Every input needed by the principal proof is included in that manuscript. The title and all original all-pencil claims are retained.

Read the original sharp inverse and curve theorem first, then **Reconstruction of moving pencils and their isomorphisms**. The new section proves the varying coefficient subbundle lemma, the unmarked moving-family inverse, the actual source-bundle gluing step, uniform sharpness, and the filtered automorphism-kernel exact sequence. It ends with an everywhere regular nonconstant P1-family through six spectral collisions. The spectral classification that follows is retained with its classical attribution.

The separate **applications.pdf** retains the real likelihood and projective critical-scheme results. The complete **archive-v144.pdf** is a non-submitted historical research archive, not an additional submission supplement. All prior mathematical part files remain unchanged; modified root documents have byte-preserved copies under history/v145-root. The predecessor v145 directory is unchanged.

- Response: RESPONSE_TO_V144_REPORTS_V146.md.
- Exact issue dispositions and domains: ISSUE_MATRIX_V146.json.
- Literature boundary and six comparison axes: LITERATURE_AUDIT_V146.md.
- Immutable source: SOURCE_LOCK_V146.json and PROVENANCE_MANIFEST_V146.json.
- Completed execution and PDF hashes: evidence/BUILD_RECEIPT_V146.json.
- Source preservation: INHERITED_SOURCE_V146.json and NONDELETION_V146.json.

Run `bash build.sh` from this directory in the repository checkout (Python with SymPy/NumPy and native pdflatex/poppler required). It executes 23 regression scripts and compiles all three PDFs. Finite regressions do not formally verify the geometric proofs. The Ballico 1993 full-text theorem comparison remains documentary-open; neither metadata nor a different article is substituted for it. No editorial decision or exhaustive priority clearance is asserted.

## Principal strengthening: a single unmarked Artin local algebra

The final v146 theorem `thm:artin-local-inverse-v146` reconstructs every complex pencil from `C[t_ij]/((det T) I_p(gamma_R Sym^2 T)+(t_ij)^(d+1))`, without grading, generators, tangent coordinates, tensor factors or a positive-dimensional support. The order `d=n^2+2n-4` is still smallest uniform. This is not inferred from a reduced determinant cone. The first relation kernel reconstructs the homogeneous cone; its determinant quotient supplies the coefficient module.

The new conceptual ingredient is `lem:coefficient-orientation-v146`: in a multiplicity-one Cauchy summand, a proper nonzero left coefficient space tensored with the full right factor has unequal factor-support ranks. A transposed matrix map exchanges those ranks and cannot identify two ideals of that type. For every pencil the ranks are `(1, binomial(N,2))`, so transposition is excluded even at one point. This is a local intrinsic orientation criterion and applies beyond the particular projective-bundle obstruction used in the earlier proof.

Theorem `thm:unrestricted-moving-v146` consequently removes the source-projectivization restriction from the whole moving-family theorem. The earlier restricted theorem and its proof remain valid special cases and are preserved. Proposition `prop:local-automorphisms-v146` gives the full local tangent-identity kernel: every generator may receive an arbitrary element of the squared maximal ideal. The kernel is a unipotent algebraic group, with affine-space underlying variety of dimension `n^2(length-1-n^2)`, and generally nonadditive group law. This replaces the earlier limitation to curve-supported reconstruction by a proved stronger inverse, not by a weakened claim.

A second new script checks support ranks, three concrete genuine three-variable pencil coefficient spaces against their transposes by exact finite-field evaluation, and general higher-order corrections in a first-relation algebra. All 23 scripts are executed. Sampling does not prove the universal orientation theorem; the representation-theoretic support argument supplies that proof. The Ballico 1993 full-text priority comparison remains documentary-open and is not discharged by this strengthening.
