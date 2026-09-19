# Local typesetting scope

The newly written main text and three new mathematical modules were compiled together with pdflatex twice in the local working environment. The resulting core-only check had 11 pages and no overfull horizontal or vertical boxes. All 11 pages were rendered and inspected for clipping and layout defects.

The check intentionally omitted all inherited appendices. Its synthetic title-page notice said that inherited references were unresolved and that it was not the full revision. The core-only PDF and its reduced bibliography are not committed as the final manuscript.

This result verifies local TeX syntax and layout of the new material only. It does not establish successful compilation of the 27-file active manuscript, absence of unresolved references in that complete document, or execution of the Git source-preservation audit. Those are separate exact-head workflow requirements. The local finite diagnostics were run with --diagnostics-only; their output explicitly records that the source audit was not run locally.
