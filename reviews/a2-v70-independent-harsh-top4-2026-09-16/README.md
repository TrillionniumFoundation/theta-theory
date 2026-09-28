# Independent review of A2 v70

The [referee report](REFEREE_REPORT.md) separates scoped correctness, originality, highest-journal significance, and delivery integrity. It recommends against acceptance at the requested top-four level in the present form. It establishes no new fatal error in the examined core. The concrete new major comment concerns the omitted corrected planar lens/scattering comparison, not a claim that the manuscript is subsumed by that literature.

## Reviewed snapshot

- Referee-ready parent: `b529b340650f5582b1d04fabd599533450b51d0b`.
- Compiled source: `16ec1030b9dfd9b185a1f0da8e50b10b40a71940`; manuscript subtree: `63fdb25cd2002d9d2b3a238e7e7f1862b2328d2b`.
- Manuscript directory: `papers/A2-v17-boundary-information-coarsening/`.
- Current native run/attempt/artifact: `35105117912` / `1` / `10449368306`.
- Baseline v69 artifact: `10446655754`; source: `1a46fd69a508bccb90c6d2553892124f068f4657`.

Only the six files in this new review directory are added. No manuscript or existing branch is changed. This is an author-requested AI-assisted referee-style assessment, not a commissioned journal report or formal proof certificate.

## Evidence and independent programs

[AUDIT_EVIDENCE.json](AUDIT_EVIDENCE.json) records the actual checks and their limits. The three programs import no author modules. `verify_delivery.py` uses the Python standard library; `independent_checks.py` additionally requires SymPy; `compare_builds.py` requires PyMuPDF. Run them with Python 3.10 or newer.

Download the two identified workflow artifact ZIPs through an authorized GitHub connection. With filenames `a2-v70-native-evidence.zip` and `a2-v69-baseline-evidence.zip`, run:

```sh
python verify_delivery.py a2-v70-native-evidence.zip a2-v69-baseline-evidence.zip > delivery.json
python independent_checks.py > independent-normal.json
python -O independent_checks.py > independent-optimized.json
cmp independent-normal.json independent-optimized.json
```

The archive check validates source bytes, lengths, SHA-256 and Git blob hashes, raw Unix modes, Git-tree reconstruction, active literal inputs, inherited originals, and native evidence-file hashes. It compares recorded author diagnostic outputs; it does not execute those author programs. The finite rational checks and their deliberately wrong controls are diagnostics, not substitutes for the proofs.

## Independent TeX rebuild

Extract the outer v70 artifact into a new directory, called `artifact` below. Its `native-source.zip` contains the frozen `source/` subtree and `SOURCE_MANIFEST.json`. After validating the archive, extract that source to a new directory and restore each file mode from the manifest; ordinary ZIP extraction need not preserve modes. Keep the verified original source separate from a clean build copy.

With TeX Live, `latexmk`, and the required LaTeX packages available, enter the clean manuscript build directory and run the following in order. No author Python checker is needed for these builds.

```sh
for entry in two_collision main rigidity; do
  latexmk -norc -pdf -interaction=nonstopmode -halt-on-error \
    -file-line-error -recorder \
    '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' "$entry.tex" \
    > "$entry-independent-build.txt" 2>&1 || exit 1
done
```

`main` imports the companion auxiliary file; `rigidity` imports the generated full-manuscript/companion references. The dependency order therefore matters. From this review directory, compare the retained native products with the fresh build:

```sh
python compare_builds.py /path/to/artifact /path/to/clean-build > build-comparison.json
```

The actual review used PyMuPDF 1.26.7 for comparison. All 517 pages matched in extracted text and 72-dpi RGB arrays. The PDF bytes differ. Final log checks found no covered critical warning/error; five full-manuscript and one principal underfull notices remain. The exact check categories are in `compare_builds.py`.

The local review archive also retains independent build transcripts and the inspected contact sheets, with principal p. 36 at 108 dpi. Visual sampling covered principal pp. 3–6, 28–29, 31–32 and 34–37. Automated all-page parity is not an all-page visual or mathematical audit. The report states the narrower proof coverage explicitly.
