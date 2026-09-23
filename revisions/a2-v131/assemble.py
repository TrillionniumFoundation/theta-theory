"""Assemble v131 from the immutable reviewed source and explicit revision files.
The old source tree and all review files are read-only inputs.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

REPO = Path(__file__).resolve().parents[2]
BASE = '472200a5373ce2adc6dacf8d211f02d765ff62f2'
REVIEW = '57c70a882150cc6e44d85ad6f68043b7327d8a10'
PREFIX = 'papers/A2-v17-boundary-information-coarsening/article/v129'
OUT = REPO / 'papers/A2-v17-boundary-information-coarsening/article/v131'
STAGE = REPO / 'revisions/a2-v131'

def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=REPO)

def write(path: str, text: str) -> None:
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def read(path: str) -> str:
    return (OUT / path).read_text(encoding='utf-8')

def once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f'Expected one replacement anchor, found {text.count(old)}: {old[:110]!r}')
    return text.replace(old, new, 1)

def section(text: str, start: str, end: str, replacement: str) -> str:
    i = text.index(start)
    j = text.index(end, i + len(start))
    return text[:i] + replacement + text[j:]

if OUT.exists():
    if OUT.is_symlink() or OUT.name != 'v131':
        raise RuntimeError('Unsafe assembly destination')
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
provenance = []
for entry in git('ls-tree', '-r', BASE, '--', PREFIX).decode().splitlines():
    meta, path = entry.split('\t', 1)
    mode, kind, blob = meta.split()
    rel = Path(path).relative_to(PREFIX)
    if kind != 'blob' or rel.parts[0] == 'evidence':
        continue
    if rel.suffix not in {'.tex', '.py', '.md', '.json', '.sh'}:
        continue
    dest = str(rel)
    if dest == 'PROVENANCE_MANIFEST.md':
        dest = 'INHERITED_PROVENANCE_V130.md'
    p = OUT / dest
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(git('show', f'{BASE}:{path}'))
    provenance.append({'source': path, 'reviewed_blob': blob, 'destination': dest})

for p in sorted((STAGE / 'source/parts').glob('*.tex')):
    write('parts/' + p.name, p.read_text(encoding='utf-8'))
write('parts/01c-graded-universal.tex', (STAGE / 'source/graded_corollary.tex').read_text())
for name in ['frontmatter.tex', 'RESPONSE_TO_REFEREE_V130.md', 'ISSUE_MATRIX.json']:
    write(name, (STAGE / 'editorial' / name).read_text())

relative = read('parts/09c-relative-primary-specialization.tex')
relative = section(relative,
    r'\begin{lemma}[Finite geometric-assassin stratification]',
    r'\begin{proof}[Proof of Theorem~\ref{thm:bounded-principal-colon-stratification}]',
    '\\input{parts/09d-relative-primary-filtrations.tex}\n\n')
relative = once(relative,
    'Their Hilbert polynomials and fibre ranks are then constant and commute\nwith base change.',
    'The specified exact diagrams then commute with arbitrary base change.\nFor graded coefficient algebras, Lemma~\\ref{lem:graded-flat-diagram}\ngives constant Hilbert functions and degreewise ranks on connected strata.')
write('parts/09c-relative-primary-specialization.tex', relative)

statement = read('parts/01b-boundary-atlas.tex')
statement = section(statement,
    r'\begin{corollary}[Universal primary finiteness for symmetric-power quotients]',
    'The theorem is independent of the special',
    '\\input{parts/01c-graded-universal.tex}\n\n')
statement = once(statement,
    'For every \\(\\alpha\\), all the assertions below are preserved by an\narbitrary base change \\(T\\to S_\\alpha\\).',
    'For every \\(\\alpha\\), all the assertions below are preserved by an\narbitrary base change \\(T\\to S_\\alpha\\).  Here \\(J\\) on a stratum\nmeans the image ideal, and each \\(K_q\\) is formed anew over that stratum.\nNo commutation across different strata is asserted.')
statement = once(statement,
    'target, image and cokernel modules are flat; in particular their\nfibre ranks commute with base change.',
    'target, image and cokernel modules are flat, and their defining exact\ndiagrams commute with arbitrary base change.  When grading is present,\ndegreewise numerical ranks are given by Lemma~\\ref{lem:graded-flat-diagram}.')
start = statement.index(r'\begin{theorem}[Universal symmetric-power determinant completion]')
end = statement.index(r'\end{theorem}', start) + len(r'\end{theorem}')
block = statement[start:end].replace(r'\twoheadrightarrow S', r'\twoheadrightarrow E').replace(r'\dim S', r'\dim E').replace(r'S=\Sym^rV', r'E=\Sym^rV')
statement = statement[:start] + block + statement[end:]
statement = once(statement, 'We next sharpen the corank-two analysis.',
    'The coefficient-space tables below concern surjective quadratic\nquotients on their stated generic coefficient strata.  Their intersection\nwith the smooth, basepoint-free web open is subject to\nProposition~\\ref{prop:smooth-web-rank-admissibility}.  In particular the\nambient index-six rows are not asserted to occur on that geometric open.\nTheorem~\\ref{thm:sharp-global-jacobian-depth} strengthens the global\nbound there to nilpotency index five.\n\nWe next sharpen the corank-two analysis.')
c3 = r'''\begin{theorem}[Projection corank three]
\label{thm:corank-three-depth}
For \(R\in G_4^\circ\), at every projection-corank-three point,
\begin{equation}\label{eq:corank3-no-d3}
 d^3\notin J,\qquad d^4\in J.
\end{equation}
The local nilpotency index is exactly five, and
\(\varepsilon_4(J)=0\) identically on this geometric open.
For arbitrary surjective coefficient data outside this open, the
universal bounds \(d^3\notin J\), \(d^5\in J\) and the membership
test for \(d^4\) remain valid; the smooth-web theorem eliminates
that binary alternative on \(G_4^\circ\).
\end{theorem}

'''
statement = section(statement, r'\begin{theorem}[Projection corank three]',
    'At the deepest Schubert stratum', c3)
write('parts/01b-boundary-atlas.tex', statement)

proof = read('parts/09b-boundary-atlas-proofs.tex')
i = proof.index(r'\begin{proof}[Proof of Theorem~\ref{thm:corank-three-depth}]')
j = proof.index(r'\end{proof}', i) + len(r'\end{proof}')
proof = proof[:i] + r'''\begin{proof}[Proof of Theorem~\ref{thm:corank-three-depth}]
Lemma~\ref{lem:no-d3-corank3} gives \(d^3\notin J\) for all the
stated coefficient data.  The polynomial restriction argument in
Theorem~\ref{thm:sharp-global-jacobian-depth}, using only the
corank-four theorem and this already proved exclusion, gives
\(d^4\in J\) on \(G_4^\circ\).  The nilpotency index is one plus
the first determinant exponent, hence exactly five.  Outside this
open the universal exponent-five bound and the definition of
\(\varepsilon_4\) still give the stated membership test.
\end{proof}''' + proof[j:]
i = proof.index(r'\begin{proof}', proof.index(r'\label{lem:effective-pieri-matrix-ring}'))
j = proof.index(r'\end{proof}', i) + len(r'\end{proof}')
proof = proof[:i] + r'''\begin{proof}
The skew diagram \(\nu/\lambda\) is a horizontal four-strip, so
\(c^\nu_{\lambda,\mu}=1\).  This alone does not prove nonvanishing
of polynomial multiplication.  Lemma~\ref{lem:fischer-determinant-projection}
calculates that the product \([123\mid123]^4x_{44}^4\) has isotypic
projection \((\det X)^4/35\).  Its factors belong to the indicated
Cauchy summands, so actual multiplication has nonzero projection.
Multiplicity one on the left and right factors and Schur's lemma
identify the resulting maps with nonzero multiples of the evaluation
pairings under
\(\mathbb S_{(4,4,4,0)}V=(\det V)^4\otimes(\Sym^4V)^*\).
They are nondegenerate.  In particular an arbitrary nonzero Jacobian
vector, not only the extremal vector used in the calculation, pairs
nontrivially with a suitable degree-four coefficient.  The coefficient
\(1/35\) is the Fischer isotypic normalization; no coefficient-one
straightening identity is needed.
\end{proof}''' + proof[j:]
write('parts/09b-boundary-atlas-proofs.tex', proof)

sharp = read('parts/11-sharp-global-laws.tex')
sharp = once(sharp,
    'The corank-three Schur-symbol exclusion proved in\nTheorem~\\ref{thm:corank-three-depth}',
    'The corank-three Schur-symbol exclusion of\nLemma~\\ref{lem:no-d3-corank3}')
write('parts/11-sharp-global-laws.tex', sharp)

intro = read('parts/01-introduction.tex')
intro = re.sub(r'\\label\{sec:introduction-v\d+\}', lambda _: r'\label{sec:introduction-v131}', intro)
intro = intro.replace(r'\widehat\NN_R^{,j}', r'\widehat\NN_R^{j}')
intro = once(intro, r'\subsection{The multiplication failure scheme}',
    (STAGE / 'editorial/intro_addition.tex').read_text() + r'\subsection{The multiplication failure scheme}')
intro = section(intro, r'\item At projection corank three,',
    r'\item At projection corank four,',
    '\\item At projection corank three, \\(d^3\\notin J\\) and\n\\(d^4\\in J\\); the index is exactly five.  The upper bound is the\nrestriction of the full-matrix identity, as proved in\nTheorem~\\ref{thm:sharp-global-jacobian-depth}.  The lower bound is\nthe functorial Schur-symbol exclusion.\n\n')
intro = once(intro,
    'Constructibility of fibrewise associated points\nand Noetherian induction give finite geometric support packets;\ntheir embedded multiplicities are measured by the finite-length\ntorsion modules at the associated generic points.',
    'Finite primary models and the two opposite associated-point inclusions\ngive exact geometric support packets.  A regular element on the quotient\nby a coherent torsion module excludes new torsion after specialization,\nand a finite power filtration computes the local lengths.  Noetherian\ninduction then handles the complement.')
intro = section(intro, 'The nine-dimensional count is classical Reye geometry,',
    r'\subsection{Organization and novelty boundary}',
    'The nine-dimensional count is classical Reye geometry, not a novelty\nclaim.  The manuscript-specific inverse statement is the recovery of\nthe polarized K3 from an abstract nonreduced failure scheme.  The original\nweb and the finite Torelli ambiguity are not identified with that K3.\nThe additional global advances here are the sharp exponent, the two\nminimal supports, and the explicit cross-corank geometry of\nSection~\\ref{sec:sharp-global-laws}.\n\n')
write('parts/01-introduction.tex', intro)

driver = once(read('geometry.tex'), r'\input{parts/09a-rees-specialization.tex}',
    '\\input{parts/11-sharp-global-laws.tex}\n\\input{parts/09a-rees-specialization.tex}')
write('geometry.tex', driver)
refs = r'''
\bibitem{BrunsVasconcelos}
W.~Bruns and W.~V.~Vasconcelos,
Minors of symmetric and exterior powers,
\emph{J. Pure Appl. Algebra} \textbf{179} (2003), 235--240.
doi:10.1016/S0022-4049(02)00115-9; arXiv:math/0111174.

\bibitem{CSSCayley}
S.~Caracciolo, A.~D.~Sokal, and A.~Sportiello,
Algebraic/combinatorial proofs of Cayley-type identities for derivatives
of determinants and pfaffians,
\emph{Adv. Appl. Math.} \textbf{50} (2013), 474--594.
doi:10.1016/j.aam.2012.12.001; arXiv:1105.6270.

\bibitem{StacksGenericFree}
The Stacks Project Authors,
\emph{The Stacks Project}, Lemma 10.118.2, ``Generic freeness,''
Tag 051S, \url{https://stacks.math.columbia.edu/tag/051S}.

\bibitem{StacksGeometricFibres}
The Stacks Project Authors,
\emph{The Stacks Project}, Sections 37.26--37.27,
``Reduced fibres'' and ``Irreducible components of fibres,''
\url{https://stacks.math.columbia.edu/tag/0553}.
'''
write('references.tex', once(read('references.tex'), r'\end{thebibliography}', refs + '\n' + r'\end{thebibliography}'))
for name in ['build.sh', 'verify_build.py']:
    write(name, (STAGE / 'control' / name).read_text())
write('checks/revision131_exact.py', (STAGE / 'control/revision131_exact.py').read_text())

hashes = {str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(OUT.rglob('*')) if p.is_file()}
manifest = {'revision': 131, 'reviewed_commit': BASE, 'controlling_review': REVIEW,
    'assembly_commit': git('rev-parse', 'HEAD').decode().strip(),
    'inherited_sources': provenance, 'assembled_sha256': hashes,
    'preservation': 'All historical source and review paths remain unchanged. The old packet proof and unnormalized Pieri assertion are replaced in v131; all inherited mathematical sections and exact scripts are retained.'}
write('PROVENANCE_MANIFEST.json', json.dumps(manifest, indent=2) + '\n')
write('PROVENANCE_MANIFEST.md', '# A2 v131 self-contained source provenance\n\n'
    f'Reviewed source: `{BASE}`. Controlling review: `{REVIEW}`.\n\n'
    'The JSON companion records every inherited Git blob and every assembled source hash. '
    'All TeX includes are local to this directory. The final article contains the new arguments, '
    'not only links to staging files. Source assembly and publication commits are distinguished '
    'in the build receipt. Historical source files remain unchanged.\n')
subprocess.run(['git', 'diff', '--exit-code', REVIEW, '--', PREFIX,
    'reviews/a2-v130-independent-harsh-top4-2026-09-23'], cwd=REPO, check=True)
print(f'Assembled {len(hashes)} source files at {OUT.relative_to(REPO)}')
