# Local visual inspection of A1 v23

The first completed local build produced a 125-page PDF after three `pdflatex` passes with shell escape disabled. The build check found no undefined-reference, multiply-defined-reference or overfull warnings.

Rendered pages inspected: 1, 3, 24, 25, 28, 29, 30, 76, 119, 120 and 125. These sample the title/abstract, contribution subsection, risk definitions, saturation and direct proof, relocated alternative proof, filtering comparison and references. No clipping, missing-glyph boxes, equation overflow or illegible layout was seen in those samples.

SHA-256 of that locally inspected PDF:
`fc96cc10a31470d037b5b64313df05bd6db7d78cbadc3e8a1def22da1379ab2d`.

This is a sampled visual inspection, not an assertion that all 125 pages were individually inspected. Later builds may differ at the PDF byte level because of build metadata; the actual final build hash is recorded separately in `BUILD_REPORT.json`.
