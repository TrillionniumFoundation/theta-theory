# Local PDF visual inspection

The complete 62-page locally built manuscript was rendered with MuPDF. Four
contact sheets covering pages 1–16, 17–32, 33–48 and 49–62 were visually
inspected for layout continuity, blank/missing pages, visible clipping and
overlaps. The stable common-advice theorem page was also inspected at a
larger resolution; the added section occupies pages 31–37 in this build.
Automated PDF word-box checks found no words outside a 20-point horizontal
and 10-point vertical safety boundary. Three-pass TeX checks reported no
undefined references or overfull boxes. The final probe command correction
is verified in the rebuilt source and the corresponding rendered page.

The inspection concerns the local full manuscript. A later GitHub Actions
rebuild is an independently executed build, not a separate human visual
review. The PDF metadata timestamp may differ; source hashes identify the
mathematical content. Visual inspection is not mathematical proof checking.
