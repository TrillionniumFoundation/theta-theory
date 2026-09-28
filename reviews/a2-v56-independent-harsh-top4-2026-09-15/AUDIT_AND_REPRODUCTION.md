# A2 v56: independent audit and reproduction ledger

## Frozen object

The report concerns source `ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de`, manuscript subtree `d554cd4c53737717594a5e30d97978238055bbb2`, at `papers/A2-v17-boundary-information-coarsening/`. The repository tree is `c90ba69166462c8eccff24bda4989d978014abff`.

Native run: 34952042203. Artifact: 10389393610, named `a2-v56-native-ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de-1`. Artifact ZIP SHA-256: `32fa3e4c3235a648a3ee8a96a1c0b122cd76ff0d2a366070f40e154991ce006a`. It was downloaded through the connected GitHub artifact action. The native product branch is `revision/a2-v56-native-products-34952042203-1`; products are under `deliveries/a2-v56/ae0eea2a3368b01a72ab6eaf50bad0cfb50ec8de/`.

The review branch starts at the frozen source. Its review directory is additive; no manuscript, original revision branch, main branch, permissions or branch protections are changed by this review.

## Mathematical coverage

The report freshly examines the new local Theorem 1.1 and its supporting relative determinant and full-phase integration interfaces; the actual-smooth finite-envelope and finite-jet proof; the new graph-to-support appendix; the density and interior-window inverses; the finite clear-channel skeleton; finite congruence matching and actual local angular alignment; and the common-strip differential kernel and finite-coordinate arguments. The principal proof interfaces are assessed from the source, not inferred from successful tests.

The two-table example's principal construction was also examined. The complete older statistical experiment catalogue, the complete charged physical-acquisition theorem F.47.3, every quantitative inverse consequence and the companion's complete mathematics did not receive a fresh line-by-line proof review. Prior referee conclusions were read as history, not adopted as a proof certificate.

The new semantic dependency finding is Corollary 19.9, principal p. 87, source `article/23j_generic_finite_channel_rigidity_v45.tex`, lines 493–515. Its statement imports F.47.3 and its proof invokes that theorem's acquisition argument. The label appears outside the proof delimiters; this does not remove the mathematical dependency. The source explicitly displays the F-prefix, so the finding is not an unresolved-reference defect or a demonstrated circularity in Theorems 1.1, A or B.

## Rebuild procedure

The artifact contains `native-source.zip`, the source and active-input manifests, all three PDFs, and native logs and auxiliary files. Extract the source ZIP into a clean directory. Run the entries in dependency order, from its `source/` directory:

```sh
for entry in two_collision main rigidity; do
  latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
    -file-line-error -recorder \
    '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' "$entry.tex"
done
```

Then run the independent audit, passing the original downloaded artifact ZIP, the directory containing the rebuilt PDFs, and an output path:

```sh
python verify_delivery.py a2-v56-native.zip /path/to/rebuilt/source DELIVERY_VERIFICATION.json
python check_local_mechanisms.py INDEPENDENT_CHECKS.json
python -O check_local_mechanisms.py INDEPENDENT_CHECKS_OPTIMIZED.json
cmp INDEPENDENT_CHECKS.json INDEPENDENT_CHECKS_OPTIMIZED.json
```

The audit requires PyMuPDF; the finite algebra checker requires SymPy. The recorded runs used PyMuPDF 1.26.7 and SymPy 1.14.0. The checker does not import author checking code. A different TeX environment or renderer may change PDF bytes and pagination; the recorded text and image equality is for the actual compared builds, not a guarantee for every installation.

## Results actually obtained

All 662 frozen files passed size, SHA-256 and Git blob checks. Reconstructing the tracked source tree reproduced the pinned manuscript subtree. The active manifest contains 110 main sources, 41 principal sources and one companion source, with 120 distinct files in the union. Main plus companion use 111 distinct sources. Generated imported auxiliary files are not new mathematical sources.

All three native PDFs were compared with independent rebuilds. The principal has 106 pages, full technical manuscript 283, companion seven. All 396 pages have identical extracted text and identical 72-dpi RGB arrays under the same PyMuPDF renderer. None of the three PDF files is byte-identical to its native counterpart. Native and rebuilt SHA-256 values are in `DELIVERY_VERIFICATION.json`.

Rebuild logs contain one underfull-vbox notice for the principal and three for the full manuscript; none for the companion. The inspected logs have no undefined-reference, multiply-defined-reference, overfull-hbox or fatal-error notices. Such observations are delivery checks, not proof checks.

Only principal pages **2, 44, 87 and 99** were actually inspected visually, at 93.6-dpi rendered resolution. They cover the new local theorem entry, the smooth remainder statement, the external-dependent corollary, and the new graph/support appendix. Other pages were not claimed as visually inspected merely because every page was computationally compared.

The finite checker verifies graph/support derivatives through order six, 90 rational last-jet blocks, four-density extraction retaining a cubic term, the mixed-log derivative, and recovery with a determinant-six gain matrix. Ordinary and optimized runs have identical JSON output. The polynomial density fixture and the rational matrix controls are not asserted to be billiard realizations. Their role is to test algebra and scope distinctions, not to certify convergence or global geometry.

The source preservation counts across all earlier revisions were not independently re-derived in this audit. The present tree and products were verified; that is a different claim. Likewise, no exhaustive literature-priority search and no full proof review of the external cited papers is claimed.
