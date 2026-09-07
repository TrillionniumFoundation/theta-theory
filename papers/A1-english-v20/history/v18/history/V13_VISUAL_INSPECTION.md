# PDF layout inspection — v13

The complete 68-page local manuscript was compiled in three pdflatex passes,
with zero undefined-reference or overfull-box warnings. All pages were rendered
with MuPDF. The title/abstract, new common-name theorem, saturation corollaries
and request-conformance pages were inspected at reading resolution. The layout
retains ordinary AMS theorem/proof typography, displayed equations and the full
appendix chain. No clipping, overlap or missing glyph was observed on the
inspected pages. A whole-document word-box check found no words outside page
bounds. These are layout checks, not mathematical verification.

The publication workflow rebuilds from the same source manifest and reports its
own PDF hash and page count. The preserved v12 proof-block identities are checked
before either build. The source identity, rather than PDF byte identity across
TeX versions or creation times, is the comparison basis.
