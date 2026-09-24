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

Run `bash build.sh` from this directory in the repository checkout (Python with SymPy/NumPy and native pdflatex/poppler required). It executes 22 regression scripts and compiles all three PDFs. Finite regressions do not formally verify the geometric proofs. The Ballico 1993 full-text theorem comparison remains documentary-open; neither metadata nor a different article is substituted for it. No editorial decision or exhaustive priority clearance is asserted.
