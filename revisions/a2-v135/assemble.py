#!/usr/bin/env python3
"""Assemble A2 v135 only, from an immutable reviewed tree and text overlays."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, re, shutil, subprocess, tarfile, tempfile
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE='a08b157800c27c0f73f0c5c9a52155265ef4f395'
REVIEWED='74b1aa9ffb95557f63e993e428a22e491a1edd0f'
SOURCE=Path('papers/A2-v17-boundary-information-coarsening/article/v134')
DEST=SOURCE.with_name('v135')
REVIEW='reviews/a2-v134-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md'
sha=lambda b:hashlib.sha256(b).hexdigest()

def unpack(data, dest):
    with tarfile.open(fileobj=io.BytesIO(data)) as ar:
        for m in ar.getmembers():
            p=PurePosixPath(m.name)
            if p.is_absolute() or '..' in p.parts or not (m.isfile() or m.isdir()):
                raise RuntimeError('Unsafe archive member')
            target=dest/m.name
            if m.isdir(): target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(ar.extractfile(m).read())

def compiled(root, driver):
    seen=set(); text=[]
    def visit(n):
        if n in seen:return
        if Path(n).is_absolute() or '..' in Path(n).parts:raise RuntimeError(n)
        seen.add(n); s=(root/n).read_text();text.append(s)
        for c in re.findall(r'\\input\{([^}]+)\}',s):visit(c)
    visit(driver)
    return seen,set(re.findall(r'\\label\{([^}]+)\}','\n'.join(text)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--base-dir',type=Path)
    args=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='a2-v135-') as td:
        td=Path(td)
        if args.base_dir:
            base=args.base_dir.resolve();assembly='local-preflight-not-a-remote-commit'
        else:
            subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
            unpack(subprocess.check_output(['git','archive',BASE,str(SOURCE)],cwd=ROOT),td/'base')
            base=td/'base'/SOURCE
            assembly=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        prior=json.loads((base/'PROVENANCE_MANIFEST.json').read_text())
        for n,h in prior['assembled_sha256'].items():
            if sha((base/n).read_bytes())!=h:raise RuntimeError('Reviewed source hash: '+n)
        inherited_inputs,inherited_labels=compiled(base,'geometry.tex')
        target=td/'new';shutil.copytree(base,target)
        shutil.rmtree(target/'evidence',ignore_errors=True)
        for p in list(target.rglob('__pycache__')):shutil.rmtree(p)
        for p in target.glob('geometry.*'):
            if p.suffix!='.tex':p.unlink()
        def get(n):return (target/n).read_text()
        def put(n,s):
            p=target/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
        def change(n,old,new):
            s=get(n)
            if s.count(old)!=1:raise RuntimeError('Expected one replacement: '+n+' '+old[:70])
            put(n,s.replace(old,new))
        # Checked mathematical overlays are ordinary editable text files.
        for p in (HERE/'overlay').rglob('*'):
            if p.is_file():
                dest=target/p.relative_to(HERE/'overlay');dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(p,dest)
        change('preamble.tex',r'\usepackage[hidelinks]{hyperref}',r'\usepackage{xr-hyper}'+'\n'+r'\usepackage[hidelinks]{hyperref}')
        # Isolate the proof pivots; retain the previous coordinate argument as an alternative.
        n='parts/12d-schur-support.tex';s=get(n)
        begin=s.index(r'\begin{proof}',s.index(r'\label{lem:schur-contraction-kernel}'))
        end=s.index(r'\end{proof}',begin)+len(r'\end{proof}')
        oldproof=s[begin:end]
        parity=oldproof[oldproof.index('Any possible image'):oldproof.index('It remains to check')]
        put('parts/12h-coordinate-parity.tex',
            '\\subsection{An alternative coordinate character calculation}\n'
            '\\label{sec:coordinate-character-alternative}\n'
            'The following direct calculation is independent of the character decomposition in '
            'Lemma~\\ref{lem:orthogonal-exterior-cube}; it is not needed for the main proof.\n'
            'Use an orthonormal basis and write \\(\\rho=\\sum_i x_i^2\\).\n\n'+parity)
        s=s[:begin]+r'\input{parts/12g-contraction-proof.tex}'+s[end:]
        pos=s.index(r'\begin{lemma}[The contraction kernel]')
        s=s[:pos]+r'\input{parts/12f-structural-lemmas.tex}'+'\n\n'+s[pos:]
        s=s.replace(r'put\n\(\kappa_q(f)=\iota_qj(f)\).',r'put\n\(\kappa_q(f)=\iota_qj(f)\).')
        s=s.replace('For \\(0\\ne q\\in\\Sym^2V^*\\), put\n\\(\\kappa_q(f)=\\iota_qj(f)\\).',
            'For \\(0\\ne q\\in\\Sym^2V^*\\), let\n'
            '\\(\\kappa_q:D\\otimes\\Sym^4V\\to\\bigwedge^3\\Sym^2V\\)\n'
            'be the map \\(\\epsilon\\otimes f\\mapsto\\iota_qj(\\epsilon\\otimes f)\\).')
        s=s.replace('This equivalence follows by choosing\ncoordinates along the kernel and using characteristic zero.',
            'This is the first-catalecticant characterization of essential variables\n'
            '\\cite[Proposition~1]{Carlini}; it also follows by choosing\n'
            'coordinates along the kernel and using characteristic zero.\n'
            'This subspace of \\(V\\) is distinct from the exterior-support\n'
            'subspace of \\(W=\\Sym^2V\\) defined below.')
        a=s.index('Apply the exhaustive pencil classification of')
        b=s.index('If the closed pencil has a distinct second',a)
        s=s[:a]+r'''On the component line, the quadratic Pluecker ideal restricts to
\((b-a)H_{w_R}\), where
\(H_{w_R}=\langle\ell_{F,R}\rangle\subset H^0(\Pj^1,\OO(1))\).
If this space has dimension two, its ideal sheaf is \((b-a)\).
If it has dimension one, the intersection is the degree-two divisor
of \((b-a)\ell\), including multiplicities.  If it is zero,
the entire line is contained in the Grassmannian.  These assertions
follow directly from the ideal generated by the Pluecker quadrics;
no classification of an ambient boundary is used.

'''+s[b:]
        s=s.replace('then \\(Qw_R\\in\\bigwedge^3R\\wedge W\\) by\n\\eqref{eq:exceptional-tangent-criterion}, giving the same\ncontradiction.',
            'then the line is tangent at \\([w_R]\\): its restricted equations\n'
            'have zero first derivative there.  Its direction is \\(Qw_R\\)\n'
            'modulo \\(\\C w_R\\), so \\(Qw_R\\in\\bigwedge^3R\\wedge W\\),\n'
            'giving the same contradiction.')
        s=s.replace('equality of open subschemes: their determinantal complement has no\ngeometric points and is empty.',
            'equality of open subschemes.  Here \\(G_4^\\circ\\) has the\n'
            'reduced open-subscheme structure inherited from \\(\\Gr(4,10)\\).\n'
            'The complement is defined by the two-by-two minors of the\n'
            'two-column coefficient matrix of the residual linear forms.\n'
            'It is a closed subscheme of finite type over \\(\\C\\) with no\n'
            'geometric points, hence is empty, regardless of possible nilpotents\n'
            'in that determinantal presentation.')
        put(n,s)
        # Keep the smooth inverse proof independent of the ambient boundary appendix.
        n='parts/12-intrinsic-web-reconstruction.tex'
        change(n,r'\input{parts/12c-exceptional-fibres.tex}'+'\n','')
        change(n,r'\input{parts/12e-global-rank-strata.tex}'+'\n','')
        change(n,'Define \\(G_4^{\\mathrm{rec}}\\subset G_4^\\circ\\) by the conditions',
            'Put \\(X=\\Gr(4,W)\\), and let \\(X^\\times\\) be the open\n'
            'where both projections are nonzero.  Set\n'
            '\\(H_w=\\langle\\ell_{F,w}:F\\in\\mathcal I_{\\mathrm{Pl},2}\\rangle\\),\n'
            'and let \\(\\pi:X^\\times\\to\\Pj(E_{175})\\times\\Pj(E_{35})\\)\n'
            'send \\([w]\\) to its pair of component lines.\n'
            'Define \\(G_4^{\\mathrm{rec}}\\subset G_4^\\circ\\) by the conditions')
        change(n,'Determinant\ncompletion, or the sharp bound \\(d^4\\in J_R\\), implies\n\\(\\sqrt{dJ_R}=(d)\\).',
            'If \\(T\\) is invertible, \\(\\gamma_R\\Sym^2T\\) is onto,\n'
            'so its maximal minors do not vanish simultaneously.  Thus\n'
            '\\(V(dJ_R)=V(d)\\); the determinant is irreducible, and the\n'
            'Nullstellensatz gives \\(\\sqrt{dJ_R}=(d)\\).  This argument\n'
            'does not require any higher-colon or primary-boundary calculation.')
        change(n,'merely on a nonempty subopen.  Proposition~\\ref{prop:global-pencil-rank-strata}\ngives its global algebraic definition.',
            'merely on a nonempty subopen.  The coefficient-rank condition in\n'
            '\\eqref{eq:reconstruction-open} defines this open algebraically.')
        change(n,'The same ideal-sheaf argument as in\nLemma~\\ref{lem:exact-plucker-pencil} proves that\n\\eqref{eq:reconstruction-open} makes the pencil intersection the\nsingle reduced point \\([w_R]\\).',
            'Indeed the restricted quadrics are \\((b-a)H_{w_R}\\).\n'
            'When \\(H_{w_R}\\) is the full space of linear forms, those\n'
            'forms generate the unit ideal sheaf on the line, and the\n'
            'intersection has ideal sheaf \\((b-a)\\).  It is the single\n'
            'reduced point \\([w_R]\\).')
        # Refine ambient scheme statements without deleting their original theorems.
        n='parts/12e-global-rank-strata.tex'
        change(n,r'\subsection{Algebraic rank strata and the ramification scheme}',r'\subsection{Algebraic rank strata and Fitting ramification}')
        change(n,r'\begin{proposition}[The rank stratification and its finite part]',
            '\\input{parts/12i-residual-sections.tex}\n\n'
            '\\begin{proposition}[The rank stratification and its finite part]')
        change(n,'Define the ramification scheme by\n\\(\\Fitt_0\\Omega_{X^\\times/Y}\\), where\n\\(Y=\\Pj(E_{175})\\times\\Pj(E_{35})\\).  Its ideal is locally',
            'Put \\(Y=\\Pj(E_{175})\\times\\Pj(E_{35})\\) and\n'
            '\\(\\mathcal R=V(\\Fitt_0\\Omega_{X^\\times/Y})\\).  We call\n'
            '\\(\\mathcal R|_{X^\\times\\setminus D_0}\\) the \\emph{Fitting\n'
            'ramification locus of the quasi-finite part}.  This convention\n'
            'records the failure to be unramified, equivalently the nonvanishing\n'
            'of the relative differential module \\cite[Lemma~29.36.14]{StacksUnramified};\n'
            'it does not assert a globally finite or flat double cover.\n'
            'The same Fitting ideal is defined on all of \\(X^\\times\\).\n'
            'Its local formula is')
        a=get(n).index('Away from \\(cd(c+d)=0\\) it exchanges')
        b=get(n).index('On the complement\nof \\(D_0\\)',a)
        s=get(n);s=s[:a]+'The Cartier-section and involution assertions, with their\nnonreduced scheme structures, follow from\nLemma~\\ref{lem:residual-cartier-sections}.  '+s[b:];put(n,s)
        # Split a genuinely independent technical programme, preserving all labels.
        n='parts/03-fitting.tex';s=get(n);pos=s.index(r'\begin{corollary}[Ordinary powers]')
        put('parts/03-fitting-core.tex',s[:pos])
        put('parts/03-relative-powers.tex','\\section{Ordinary powers and relative flat flags}\n'
            '\\label{sec:supplement-relative-powers}\n'+s[pos:])
        mainparts=['01-introduction','02-relations','03-fitting-core',
          '12-intrinsic-web-reconstruction','04-polarization','05-moduli','07-classical','15-support-literature']
        suppparts=['03-relative-powers','04-depth','10-reye-priority','16-ambient-pencil',
          '14-boundary-overview','01b-boundary-atlas','06-coranktwo','08-corank-boundary',
          '09-stratified-nilpotent','09b-boundary-atlas-proofs','09c-relative-primary-specialization',
          '11-sharp-global-laws','09a-rees-specialization','14-separating-pencils','08-weighted','09-certificates']
        put('parts/16-ambient-pencil.tex','\\section{The ambient component pencil}\n'
            '\\label{sec:ambient-pencil-supplement}\n'
            '\\input{parts/12c-exceptional-fibres.tex}\n'
            '\\input{parts/12e-global-rank-strata.tex}\n'
            '\\input{parts/12h-coordinate-parity.tex}\n')
        inputs=lambda names:''.join('\\input{parts/'+n+'.tex}\n' for n in names)
        put('geometry.tex','\\input{preamble.tex}\n\\externaldocument{supplement-labels}[supplement.pdf]\n'
            '\\begin{document}\n\\input{frontmatter.tex}\n'+inputs(mainparts)+
            '\\input{references.tex}\n\\end{document}\n')
        put('supplement.tex','\\input{preamble.tex}\n\\externaldocument{geometry-labels}[geometry.pdf]\n'
            '\\renewcommand{\\thesection}{S\\arabic{section}}\n\\begin{document}\n'
            '\\title[Boundary structures and exact certificates]{Boundary structures, specialization, and exact certificates\\\\'
            'Technical supplement to intrinsic reconstruction of webs}\n'
            '\\author{Qian Qi}\n\\date{September 23, 2026 (Revision 135)}\n'
            '\\begin{abstract}This supplement contains the complete primary-boundary,\n'
            'relative-specialization and exact-coordinate theory accompanying the\n'
            'reconstruction article.  It also gives the ambient component-pencil\n'
            'classification and its scheme-theoretic residual involution.\n'
            'These results are not hypotheses of the smooth-locus inverse theorem.\n'
            'References with ordinary numerical section numbers refer to the\n'
            'reconstruction article; sections of this supplement are prefixed S.\n'
            '\\end{abstract}\n\\maketitle\n\\enlargethispage{3pt}\n\\tableofcontents\n'+inputs(suppparts)+
            '\\input{references.tex}\n\\end{document}\n')
        put('complete.tex','\\input{preamble.tex}\n\\begin{document}\n'
            '\\input{frontmatter.tex}\n'+inputs(mainparts)+'\\appendix\n'+inputs(suppparts)+
            '\\input{references.tex}\n\\end{document}\n')
        s=get('frontmatter.tex').replace('Revision 134','Revision 135').replace('revision 134','revision 135')
        s=s.replace('The ambient exceptional\nlocus lies over binary quartics, and its rank stratification and\nramification scheme are described by a vector-bundle morphism.',
            'The support of the ambient rank-defect locus is contained in the\n'
            'inverse image of the binary-quartic subspace variety; no equality\n'
            'or ambient component classification is asserted.')
        pos=s.index('Complete accompanying appendices')
        end=s.index(r'\end{abstract}',pos)
        s=s[:pos]+'''A separate technical supplement retains the full primary-boundary
and relative-specialization theory.  The reconstruction proof uses
the nonreduced normal cone directly, without a higher-corank primary
atlas or an exceptional-open hypothesis.
'''+s[end:];put('frontmatter.tex',s)
        # A new article introduction ends with a mathematical dependency map, not a revision log.
        n='parts/01-introduction.tex';s=get(n);pos=s.index(r'\subsection{Organization and novelty boundary}')
        # Preserve the old editorial scope discussion as a historical note, not a proof input.
        put('history/organization-v134.tex',s[pos:])
        s=s[:pos]+r'''\subsection{Organization and relation to prior work}

Sections~\ref{sec:relations} and \ref{sec:fitting} construct the algebra
and its Fitting scheme.  Section~\ref{sec:intrinsic-web-reconstruction}
contains the complete reconstruction argument: the deepest stratum,
its oriented normal cone, the universal coefficient readout, one
common projective transformation, and the contraction-kernel and
exterior-support theorems.  The scheme structure of the cone is
used directly; no primary decomposition of its ideal is needed.
Sections~\ref{sec:polarization}--\ref{sec:classical} compare this
invariant with the polarized Jacobian surface and its moduli.
Section~\ref{sec:support-literature} identifies the classical
representation and secant tools and the precise additional
contraction calculation.

The technical supplement is a separate reading object, not part of
the proof of the main inverse theorem.  It contains the full
nilpotent-depth, primary-boundary, collision, relative-filtration,
and exact-coordinate results, as well as the detailed Reye comparison
and the ambient component-pencil classification.  All mathematical
statements and labels of those results are retained.  Its rank-defect
schemes are defined by actual minors; their support is only contained
in the binary-Jacobian boundary.  No complete embedded-primary atlas
of the highest-corank residual layers is used or asserted.

Finite exact checks accompany the calculations, but do not formally
verify the written structural proofs.  The historically relevant
Ballico paper \cite{Ballico93} remains a specific documentary issue:
its complete text has not been obtained, and no theorem-level
nonanticipation conclusion is drawn from its title or later citations.
This does not change the hypotheses or conclusion of the reconstruction
theorem proved here.
''';put(n,s)
        # Bibliography additions are primary texts; no inferred theorem in the unread source.
        refs=r'''
\bibitem{Boralevi}
A.~Boralevi, A note on secants of Grassmannians,
\emph{Rend. Istit. Mat. Univ. Trieste} \textbf{45} (2013), 67--72.
\url{https://rendiconti.dmi.units.it/volumi/45/011.pdf}.
\bibitem{Carlini}
E.~Carlini, Reducing the number of variables of a polynomial,
in \emph{Algebraic Geometry and Geometric Modeling}, Springer, 2006,
237--247; author preprint arXiv:math/0507531, Proposition 1.
\bibitem{LandsbergWeyman}
J.~M.~Landsberg and J.~Weyman, On the ideals and singularities of
secant varieties of Segre varieties, author manuscript (January 2007),
Definition 1 and Theorem 3.1.
\url{https://people.tamu.edu/~jml//1-07LWsecseg.pdf}.
\bibitem{StacksUnramified}
The Stacks Project Authors, \emph{The Stacks Project}, Section 29.36,
Unramified morphisms, Tag 02G3, accessed September 23, 2026.
\url{https://stacks.math.columbia.edu/tag/02G3}.
'''
        change('references.tex',r'\end{thebibliography}',refs+'\n'+r'\end{thebibliography}')
        # Imported labels describe the other PDF; local labels are unique in the complete driver.
        current_inputs,current_labels=compiled(target,'complete.tex')
        if not inherited_labels<=current_labels:
            raise RuntimeError('Lost labels: '+str(inherited_labels-current_labels))
        unchanged={str(p.relative_to(base)):sha(p.read_bytes()) for p in base.rglob('*.tex')
                   if (target/p.relative_to(base)).is_file() and (target/p.relative_to(base)).read_bytes()==p.read_bytes()}
        for n in ['parts/12a-universal-readout.tex','parts/12b-functoriality.tex']:
            if n not in unchanged:raise RuntimeError('Accepted proof changed: '+n)
        sources={str(p.relative_to(target)):sha(p.read_bytes()) for p in sorted(target.rglob('*'))
          if p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'}
          and p.name not in {'PROVENANCE_MANIFEST.json','PROVENANCE_MANIFEST.md'}
          and 'evidence' not in p.parts}
        manifest={'revision':135,'assembly_commit':assembly,'reviewed_commit':REVIEWED,
          'controlling_review_commit':BASE,'controlling_review':REVIEW,
          'inherited_compiled_inputs':sorted(inherited_inputs),'inherited_mathematical_labels':sorted(inherited_labels),
          'compiled_complete_inputs':sorted(current_inputs), 'unchanged_inherited_tex_sha256':unchanged,
          'assembled_sha256':sources,
          'architecture':{'main':'geometry.tex','technical_supplement':'supplement.tex','complete':'complete.tex'}}
        put('PROVENANCE_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
        put('PROVENANCE_MANIFEST.md','# A2 v135 provenance\n\nImmutable review: `'+BASE+'`.\n'
          'The entire v134 source was hash-checked before assembly. All inherited mathematical labels remain compiled '
          'in complete.tex and distributed between the article and supplement. Accepted universal-readout and '
          'common-g proofs are byte-identical. The remote publication commit follows the recorded executed source commit.\n')
        final=ROOT/DEST
        if final.exists():
            m=final/'PROVENANCE_MANIFEST.json'
            if not m.is_file() or json.loads(m.read_text()).get('revision')!=135:raise RuntimeError('Unknown destination')
            shutil.rmtree(final)
        shutil.copytree(target,final)
        print(json.dumps({'destination':str(DEST),'source_commit':assembly,
          'preserved_labels':len(inherited_labels),'unchanged_tex':len(unchanged)},indent=2))
if __name__=='__main__':main()
