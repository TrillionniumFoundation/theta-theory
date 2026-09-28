# A2 v68 — native PDF visual audit

Date: September 16, 2026. Actual source: `de0deffc2ca7b0fd2f0d2d5ad5fbdff1eee0f0a6`. Native workflow: `35088239966`, attempt 1, artifact `10442234606`.

The downloaded native PDFs, not the preceding revision's PDFs, were rendered with PyMuPDF 1.26.7 in RGB at 108 dpi. Contact sheets were actually inspected for principal pages **1, 3, 51, 52, 53, 54, 55, 56, 57** and full-manuscript pages **1, 4, 52, 53, 54, 55, 56, 57**. Principal page **3** was additionally inspected at the full rendered size. Earlier local visual checks are not substituted for these native checks.

The inspected pages cover the revised title and abstract, the shared main theorem, the interface with the retained stopping proof, and every page of the new smooth-contact section in the principal article. No clipped equation, overlapping text, broken visible mathematical glyph, or unreadable page break was observed on these pages. The full technical title is separated from its contents page; no mathematical content was removed to achieve that layout.

Final native logs retain **two principal and seven full-manuscript underfull-vbox notices**, and none in the companion. They contain no overfull-box, missing-character, undefined-reference/citation, multiply-defined-label, or LaTeX-error pattern in the completed check. This is not a claim of zero typographic warnings or a universal journal-style certification.

A separate executable comparison checks all **497 pages** against the separately built final local revision. Extracted text and same-renderer 72-dpi RGB arrays agree page by page; PDF file bytes differ. See [POST_DOWNLOAD_VERIFICATION.json](POST_DOWNLOAD_VERIFICATION.json) and [verify_download.py](verify_download.py). All-page mechanical parity is **not** all-page visual inspection, and neither procedure certifies the mathematics.

The final native auxiliary files give principal locations: main Theorem 1.1 on p. 3; Section 11 begins on p. 51; Lemma 11.1 and Proposition 11.2 begin on p. 52; smooth Theorem 11.3 begins on p. 53; Lemma 11.4 on p. 54; real-profile Theorem 11.5 on p. 55; and the actual flat-family Proposition 11.6 on p. 56, with its proof ending on p. 57. In the full manuscript, the main theorem begins on p. 4, smooth rigidity on p. 54, real-profile stability on p. 55, and the flat family on p. 56 with proof on p. 57.
