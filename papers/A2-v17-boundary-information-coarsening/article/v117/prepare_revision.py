#!/usr/bin/env python3
"""Materialize the preserved reading editions from the pinned v116 source.
Only the sibling v117 directory is written. No historical source is edited.
"""
from pathlib import Path
import hashlib, json, re, shutil
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'v116'
REVIEW='a65e0e92b24fe6882e60ebcf678bb2f9f5048312'
REVIEWED='fadcfaa11a1939625177eb12e97569b63b7a1a9d'
BRANCH='revision/a2-v117-finite-quotient-primary-structure-2026-09-22'
CORE=['00a-conductor-introduction','01-sharp-conductor','02-quotient-hilbert',
      '03-plane-generators','04-etale-descent','00d-contact-primary-structure',
      '00e-moving-contact-normalization','05-collision-types','06-finite-literature']
OLDCORE=['00c-conductor-reduction','00-introduction','00-polar-residual-theory',
 '00b-intrinsic-residual-germs','02-global-geometry','02c-residual-calculus',
 '02g-orientation-descent','02d-all-dimension-components','02e-wall-geometry',
 '02f-higher-products','02j-higher-hyperplane-classification','06-priority-and-application']
APPS=['01-contact-native','03-realization-stability','02b-component-structure',
 '01b-structural-overview','04-statistical-experiments','04b-uniform-constants','05-complements']
ABSTRACT=r'''We identify multiplication failure schemes for linear series containing the sections vanishing on a finite divisor. On the projective line the conductor range is sharp and depends on the dimension of the restricted series; an evaluation-kernel criterion extends the comparison to curves. For generating hyperplanes in any finite locally free algebra, all higher failure schemes coincide with the space of length-two quotient algebras carrying a generating line. This determines the full primary structure for every contact multiplicity partition, including Grassmannian-cohomology transverse algebras, exact lengths and nilpotency indices. The moving hyperplane failure scheme is smooth, although its fixed-contact fibres are nonreduced. For generating three-planes on a reduced divisor, total-degree truncation and Haiman's diagonal-ideal theorem determine the stable ideal and all its powers. The contact-pencil primary formula and normalization are retained, with explicit descent at branch intersections. These results concern entire conductor-containing families, not the unrestricted ambient Grassmannian; all cokernel comparisons are compatible with arbitrary base change.'''
TITLE=r'Finite quotients and primary structures\\of multiplication failure schemes'
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs(names): return ''.join(r'\input{parts/'+n+'.tex}\n' for n in names).replace('\\n','\n')
def main():
    if not (OLD/'paper.tex').is_file(): raise RuntimeError('Pinned sibling v116 source is required')
    archive=HERE/'history/v116_source'; archive.mkdir(parents=True,exist_ok=True)
    oldtex=sorted(list(OLD.glob('*.tex'))+list((OLD/'parts').rglob('*.tex')))
    hashes={}
    for p in oldtex:
        rel=p.relative_to(OLD); q=archive/rel; q.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(p,q); hashes[str(rel)]=h(p)
    for p in (OLD/'parts').glob('*.tex'):
        q=HERE/'parts'/p.name
        if p.name!='00a-conductor-introduction.tex': shutil.copyfile(p,q)
    for name in ['00d-contact-primary-structure','00e-moving-contact-normalization']:
        p=HERE/'parts'/(name+'.tex'); t=p.read_text()
        t=t.replace('n\\ge2d-1','n\\ge2d-2').replace('thm:conductor-reduction','thm:sharp-conductor')
        t=t.replace('n\\ge7','n\\ge6')
        if name.startswith('00e'):
            t=t.replace('Each component downstairs is a prime Cartier divisor in the smooth\nambient space.',
             'Lemma~\\ref{lem:etale-primary-descent} applies to this regular ambient\nspace and its invariant weighted divisors, including all branch\nintersections. It proves that each component downstairs is a prime\nCartier divisor; irreducibility here does not assert smoothness or\ngeometric unibranchedness.')
        p.write_text(t)
    oldpaper=(OLD/'paper.tex').read_text(); pre=oldpaper.split('\\title[',1)[0]
    metadata=(r'\title[Finite quotients and multiplication failure]{'+TITLE+'}\n'+
      '\\author{Qian Qi}\n\\date{September 22, 2026}\n'+
      '\\subjclass[2020]{14M12, 14H50, 13C40, 14B05, 14N15}\n'+
      '\\keywords{Multiplication of sections, finite quotient algebras, Hilbert schemes, primary decomposition, nilpotent structures}\n'+
      '\\hypersetup{pdftitle={Finite quotients and primary structures of multiplication failure schemes},pdfauthor={Qian Qi}}\n')
    start=pre+metadata+'\\begin{document}\n\\begin{abstract}\n'+ABSTRACT+'\n\\end{abstract}\n\\maketitle\n'
    end='\\input{references.tex}\n\\end{document}\n'
    (HERE/'geometry.tex').write_text(start+inputs(CORE)+end)
    sep=r'''\section*{Complementary geometry: full statements and proofs}
The following sections retain the quadratic, polar, residual, wall and
unrestricted hyperplane developments with their original hypotheses.
They are not premises of the finite-quotient theorems above. The first
section also retains the earlier two-layer conductor proof in its
original sufficient range. The shorter geometry reading edition ends
before these complements; no theorem below is discarded.
'''
    (HERE/'paper.tex').write_text(start+inputs(CORE)+sep+inputs(OLDCORE)+'\\appendix\n'+inputs(APPS)+end)
    app=(OLD/'applications.tex').read_text().replace('[geometry.pdf]','[paper.pdf]')
    app=app.replace('Conductor reduction\nand primary structures','Finite quotients\nand primary structures')
    app=app.replace('References to the geometric article are','References to the full geometric complements are')
    (HERE/'applications.tex').write_text(app)
    refs=(OLD/'references.tex').read_text()
    additions=r'''
\bibitem{ABHS} S. Arpin, S. Bozlee, L. Herr, and H. Smith,
\emph{The scheme of monogenic generators I: Representability},
arXiv:2108.07185v2 (2022), especially Proposition 3.6, Definition 3.12,
and Proposition 3.14.
\bibitem{Haiman} M. Haiman,
\emph{Hilbert schemes, polygraphs, and the Macdonald positivity conjecture},
J. Amer. Math. Soc. \textbf{14} (2001), 941--1006;
arXiv:math/0010246v2, Corollary 3.8.3.
\bibitem{Grinberg} D. Grinberg,
\emph{A basis for a quotient of symmetric polynomials},
arXiv:1910.00207v2 (2021), Theorem 2.7 and the subsequent discussion.
'''
    (HERE/'references.tex').write_text(refs.replace('\\end{thebibliography}',additions+'\\end{thebibliography}'))
    shutil.copyfile(OLD/'make_crossrefs.py',HERE/'make_crossrefs.py')
    receipt=(OLD/'make_receipts.py').read_text()
    receipt=receipt.replace("REVIEW='1cb4e00c86699247454d21dbec2dcce01a9c6b8b'","REVIEW='"+REVIEW+"'")
    receipt=receipt.replace("BASE='acfd3d57e0053e1b03df53020fd8e79e14599c03'","BASE='"+REVIEWED+"'")
    receipt=receipt.replace('revision 116','revision 117').replace('v116 source-bound','v117 source-bound')
    receipt=receipt.replace('V115_SOURCE_MANIFEST','V116_SOURCE_MANIFEST').replace('V115_RERUN_DIAGNOSTICS','V116_RERUN_DIAGNOSTICS')
    (HERE/'make_receipts.py').write_text(receipt)
    (HERE/'evidence').mkdir(exist_ok=True)
    manifest={'review_commit':REVIEW,'reviewed_head':REVIEWED,'archive':'history/v116_source','sha256':hashes,
      'active_changes':{'00a-conductor-introduction.tex':'strengthened introduction; original archived',
      '00d-contact-primary-structure.tex':'sharper bound and reference only',
      '00e-moving-contact-normalization.tex':'sharper bound and standalone descent reference'}}
    (HERE/'evidence/V116_SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    (HERE/'IDENTITY.json').write_text(json.dumps({'version':'A2-v117-finite-quotient', 'branch':BRANCH,
      'base_review_commit':REVIEW,'reviewed_v116_head':REVIEWED,
      'excluded_divergent_v116_head':'cbfb78d7451ef9ca9fe694d292fb973f757d9f42',
      'primary_article':'geometry.tex','complete_archive':'paper.tex',
      'applications':'applications.tex','source_commit_record':'evidence/SOURCE_RECEIPT.json'},indent=2)+'\n')
    print(json.dumps({'archived_tex_files':len(hashes),'core_parts':CORE,'complementary_parts':OLDCORE,'application_parts':APPS},indent=2))
if __name__=='__main__': main()
