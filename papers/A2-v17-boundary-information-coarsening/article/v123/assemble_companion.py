"""Assemble without rescaling either manuscript's pages.

The divider is typeset by paper.tex. Direct page insertion preserves the source
page dimensions and vector content instead of the tiny placement transformations
introduced by a PDF-inclusion typesetting wrapper.
"""
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parent
main = fitz.open(ROOT / 'geometry.pdf')
wrapper = fitz.open(ROOT / 'paper_latex.pdf')
archive = fitz.open(ROOT.parent / 'v122' / 'paper.pdf')
if len(archive) != 130 or len(wrapper) != len(main) + 1 + len(archive):
    raise RuntimeError('Unexpected source page counts; refusing to assemble.')
leaf = len(main)
if 'Complete retained mathematical companion' not in wrapper[leaf].get_text():
    raise RuntimeError('The expected preservation leaf was not found.')
out = fitz.open()
out.insert_pdf(main)
out.insert_pdf(wrapper, from_page=leaf, to_page=leaf)
out.insert_pdf(archive)
out.set_metadata({'title':'A2 revision 123 — complete mathematical companion',
                  'author':'Qian Qi',
                  'subject':'Revision 123 and the complete preserved revision 122',
                  'creator':'LaTeX and direct PDF page assembly'})
out.set_toc([[1,'Revision 123: polarized ramification and higher corank',1],
             [1,'Preservation and historical scope',len(main)+1],
             [1,'Revision 122: complete preserved mathematics',len(main)+2]])
# Original printed page numbers are retained; no overlay or stamp is introduced.
out.save(ROOT / 'paper.pdf', garbage=4, deflate=True)
print(f'Assembled {len(out)} pages with no page rescaling.')
