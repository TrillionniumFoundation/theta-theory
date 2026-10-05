# A2-DYN v4: validation

The native build `sh build.sh` passed locally and produced a 29-page AMS article. The final pdfLaTeX log has no warnings, undefined references, overfull boxes or underfull boxes. All 29 pages were rendered and inspected; the new Hessian and physical-clock pages were also inspected at page resolution. The recorded TeX input closure agrees with all fifteen active source files; no text block extends outside a PDF page.

The source audit verifies 37 proof bodies and 107 labels, including every one of the 28 v3 proof bodies and 78 labels. It checks the unchanged old core blobs, references and citations, exact rational constants, and fifteen adjacent increment comparisons from eighteen finite certified excursion samples. It passes identically under ordinary Python and Python -O. Three deliberate source mutations are rejected in both modes.

The four retained finite diagnostics also pass: rational winding geometry, finite excursion minimum enclosures, the v1 finite mechanical/algebraic suite, and the separate v2 finite mechanical suite. The new source audit performs 437 finite checks. These counts describe tests, not mathematical theorems or continuum certification.

`evidence/local-build.json` records the local PDF SHA-256, source-audit digest, compiler, layout and mutation checks. `evidence/source-audit.json` pins every active manuscript source by Git blob and SHA-256. These receipts explicitly do not assert remote CI success, independent human review, or completion of the full raw billiard LLT. Remote build results, when present, must be tied to their actual workflow head SHA.

The published core tree must equal `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`. Reproduction requires Python 3 and pdfLaTeX with AMS, Latin Modern, geometry, hyperref, mathtools and microtype packages. No shell escape, external data service or extra observation source is used by the mathematical diagnostics.
