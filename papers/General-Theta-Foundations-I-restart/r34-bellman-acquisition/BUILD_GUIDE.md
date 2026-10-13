# Build and independent reconstruction

Requirements: Python 3.11+ with NumPy and pypdf; pdfLaTeX with AMS fonts/packages; pdfinfo and pdftotext. The hosted workflow fixes NumPy 2.3.5 and pypdf 5.9.0. Builds disable shell escape. SOURCE_DATE_EPOCH, UTC and locale are fixed by the scripts.

```
python verify.py
python regression.py
python -O regression.py
python benchmark.py --reports 0 -1 2
python native_build.py --output /tmp/r34-native --receipt /tmp/r34-native.json
python build.py --source-sha <ORDINARY_SOURCE_SHA> --expected-tree <ORDINARY_PROJECTION_SHA> --output /tmp/r34-pdfs --receipt /tmp/r34-full.json
```

`native_build.py` makes two isolated three-pass builds from the ordinary source manifest and checks normal/optimized outputs, actual recorder inputs, references, labels and layout warnings. `build.py` also rebuilds the complete R32 packet by its fixed source/projection pins. It copies reviewed R32 into Companion H and the complete G/F/E/D/C/B/A/X/W/V/U/T/S without rewriting them. The inherited pipeline includes its own full regressions and the explicit corrected-F cover.

The expected total is 40 isolated PDF builds per complete environment, three passes each, producing 15 delivery PDFs. Actual page totals/check counts/hashes are read from the receipts, not assumed here. Nested historical counts are NOT added and presented as independent native tests.

The ordinary projection excludes `review_inputs`, `artifacts`, `evidence`, caches and git metadata. The pinned external R32 report is separately checked by its exact Git blob. The actual native Git directory and full repository tree are recorded in publication evidence. Source, artifact and final evidence commits are distinct; source hashes are not inserted circularly into their own files.

A separate reconstruction must download the actual remote packet, hash every input before/after, rebuild, compare all delivery PDF page counts and normalized text, then render/inspect pages. Byte reproducibility is claimed only for repeated builds within one environment unless cross-environment hashes are actually equal. Any cross-engine difference must be reported. Generated evidence does not establish continuum correctness, novelty or journal acceptance.
