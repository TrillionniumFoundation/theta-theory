# Render inspection

The local native manuscript was independently typeset twice with pdfTeX (TeX Live 2025/dev/Debian), three passes per build. Its 31 pages were rendered with PyMuPDF and visually inspected as six page sheets covering every page. The title/abstract, quotient propositions, central theorem, forced moment operators, full-ledger formulas, mandatory-state and minimax theorems, all three realizations, algorithm pseudocode and bibliography were inspected for clipping, overlap and malformed layout. The final log rejects overfull boxes, unresolved references/citations and duplicate labels.

A further final local reconstruction is run after the notational edits. The remote TeX environment is recorded separately in its build receipt; its PDF need not have the same byte hash as a different local TeX distribution. Within each recorded environment, a fresh-directory reconstruction must match byte-for-byte.

The source commit precedes the artifact-only child. The independent remote read-only job verifies that exact child without retained write credentials and deposits its own receipt outside the verified commit. Render/source-integrity inspection is not a mathematical proof certificate.
