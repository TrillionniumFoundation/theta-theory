#!/usr/bin/env python3
"""Build a native, self-contained revision without modifying any v152 file.

Usage: python assemble_v153.py [--build]
All inputs are local, and checked against the controlling reviewed tree.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'v152'
REVIEW = '60f1a3c5f8078c31019dfab249d334d0e717e225'
REPO_PREFIX = 'papers/A2-v17-boundary-information-coarsening/article/v152/'
MAIN = [
 '33-first-relations-v147.tex', '00-ruling-foundations-v145.tex',
 '34-coefficient-descent-v147.tex', '13a-criterion-v145.tex',
 '18-pencil-proof-v145.tex', '20-finite-neighbourhoods.tex',
 '32-local-inverse-v146.tex', '37-common-divisor-strata-v149.tex',
 '40-canonical-divisor-boundary-v151.tex', '@NEW',
 '44-conductor-and-collisions-v152.tex', '46-divisor-intersections-v152.tex',
 '45-pencil-orbit-boundary-v152.tex']
APPENDIX = [
 '00-principal-introduction-v152.tex', '35-coefficient-symmetries-v148.tex',
 '29-curve-reconstruction-v145.tex', '31-moving-pencils-v146.tex',
 '38-pencil-deformation-equivalence-v149.tex', '41-rigidification-v151.tex',
 '42-pencil-specialization-v151.tex', '39-transverse-relations-v149.tex',
 '36-covering-moduli-v148.tex', '21-spectral-specialization.tex',
 '22-relative-spectral-strata.tex', '25-fixed-spectral-strata-v145.tex',
 '17-assistance.tex', '43-assistance-specific-v151.tex',
 '47-assistance-specific-v152.tex']
INPUT = re.compile(r'\\input\{([^{}]+)\}')
LABEL = re.compile(r'\\label\{([^{}]+)\}')
BLOCK = re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|definition|example|remark|proof)\}')
changes: list[dict] = []
source_hashes: dict[str,str] = {}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_old(rel: str) -> str:
    path = (OLD / rel).resolve()
    if not path.is_relative_to(OLD.resolve()):
        raise ValueError(f'Input escapes locked source: {rel}')
    data = path.read_bytes()
    expected = subprocess.check_output(
        ['git','show',f'{REVIEW}:{REPO_PREFIX}{rel}'], cwd=HERE)
    if data != expected:
        raise RuntimeError(f'Reviewed source changed: {rel}')
    source_hashes[rel] = sha256(data)
    return data.decode('utf-8')


def flatten(text: str, stack: tuple[str,...] = ()) -> str:
    def expand(match: re.Match) -> str:
        rel = match.group(1)
        if not rel.endswith('.tex'):
            rel += '.tex'
        if rel in stack:
            raise RuntimeError(f'Cyclic input: {stack + (rel,)}')
        return flatten(read_old(rel), stack + (rel,))
    return INPUT.sub(expand, text)


def replace_one(text: str, old: str, new: str, name: str, issue: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f'Expected exactly one patch target: {name}: {issue}')
    changes.append({'file':name, 'issue':issue, 'old':old, 'new':new})
    return text.replace(old,new,1)


def revise_part(name: str) -> tuple[str,str]:
    original = flatten(read_old('parts/' + name))
    text = original
    if name == '00-principal-introduction-v152.tex':
        text = replace_one(text, r'\section{Introduction}',
            r'\section{Detailed reconstruction statements and comparisons}', name, '16,20: appendix architecture')
    if name == '46-divisor-intersections-v152.tex':
        text = replace_one(text,
            'In particular, at a relation $K=a_0^mL$ with $\\gcd(L)=1$, the',
            'In particular, at a relation $K=a_0^mL$ with $a_0$ a nonzero\nlinear form and $\\gcd(L)=1$, the', name, '7: linear power divisor')
    if name == '45-pencil-orbit-boundary-v152.tex':
        text = replace_one(text, 'canonical operation: changing the basis of its entire cotangent',
            'linear coordinate-change action: changing the basis of its entire cotangent', name, '9,10,17: acting group and choices')
        text = replace_one(text, '[A universal ramified boundary point]',
            '[A common point in full first-relation orbit closures]', name, '9,10,17: theorem title')
        text = replace_one(text,
            'by the\ncoefficient-span statement for $C_R$.',
            'by Lemma~\\ref{lem:pencil-irreducibility} and the nonzero\nmatrix-coefficient inclusion in \\eqref{eq:general-coefficient-map}.',
            name, '13: exact coefficient-span reference')
        text = replace_one(text, 'Their number is',
            'The number of coefficient variables is', name, '14: variables versus equations')
        text = replace_one(text,
            'A matrix of constant fibre rank has\nlocally split image, which proves the subbundle assertion over the\nwhole line, not just at its closed points.',
            'The ideal of its maximal minors in $\\C[\\tau]$ has no common\nclosed zero, and is therefore the unit ideal. On each maximal-minor\nopen a corresponding square submatrix is invertible and splits the\nimage. These opens cover $\\operatorname{Spec}\\C[\\tau]$, proving the\nsubbundle assertion over the whole line, including all scheme points.',
            name, '12: maximal-minor subbundle argument')
        marker = '\\begin{theorem}[A common point in full first-relation orbit closures]'
        text = replace_one(text, marker,
            'The group in $Z_R$ is the full $\\operatorname{GL}(E)$, not the\n$\\PGL(V)$ congruence group of the pencil. Fixing the standard flag,\nscalar direction and complement specifies the displayed common point;\nno choice-independent distinguished moduli point is asserted.\n\n' + marker,
            name, '9,10,11,17: precise boundary scope')
    if name == '44-conductor-and-collisions-v152.tex':
        marker = '\\subsection{Two coprime divisor choices}'
        text = replace_one(text, marker,
            'The formal-image and separated-germ steps below are isolated in\nLemma~\\ref{lem:formal-image-v153}. Lemma~\\ref{lem:coprime-lifts-v153}\ngives the Artin cancellation and a direct positive lower bound for the\nsplit codimension. Theorem~\\ref{thm:atlas-v153} supplies the full\nWeierstrass incidence functor in every collision order;\nTheorem~\\ref{thm:fitting-v153} evaluates the singular ideal for all ranks.\n\n' + marker,
            name, '1-6: formal and singular-ideal dependencies')
    if LABEL.findall(text) != LABEL.findall(original):
        raise RuntimeError(f'Patch changed mathematical labels in {name}')
    if BLOCK.findall(text) != BLOCK.findall(original):
        raise RuntimeError(f'Patch changed theorem/proof blocks in {name}')
    return original, text


def assemble() -> dict:
    driver = read_old('geometry.tex')
    names = [x.removeprefix('parts/') for x in INPUT.findall(driver) if x.startswith('parts/')]
    chosen = [x for x in MAIN + APPENDIX if x != '@NEW']
    if collections.Counter(names) != collections.Counter(chosen):
        raise RuntimeError('Reading order must contain every principal part exactly once')
    preamble = flatten(read_old('preamble.tex'))
    bibliography = flatten(read_old('references-main-v152.tex'))
    bibliography = replace_one(bibliography, r'\end{thebibliography}',
        '\n\\bibitem{Grinberg2019}\nD.~Grinberg, \\emph{A basis for a quotient of symmetric polynomials},\narXiv:1910.00207, version of September 24, 2021, Theorem~2.7.\n\n\\end{thebibliography}',
        'references-main-v152.tex', 'classical reciprocal-ring attribution')
    original_all, body = [], []
    new_core = (HERE/'new-core.tex').read_text()
    for sequence, is_appendix in [(MAIN, False), (APPENDIX, True)]:
        if is_appendix:
            body.append('\\appendix\n')
        for name in sequence:
            if name == '@NEW':
                body.append('% BEGIN NEW MATHEMATICS v153\n' + new_core)
            else:
                original, revised = revise_part(name)
                original_all.append(original)
                body.append('% BEGIN PRESERVED PART ' + name + '\n' + revised)
    disclosure = ('\\section*{Assistance in the present revision}\n'
        'An AI assistant helped formulate and write the binary conductor stratification,\n'
        'the simultaneous incidence atlas, the evaluated singular Fitting ideal, and\n'
        'the minimal-relation-module argument for pure-power fibres. It also prepared\n'
        'the source-preserving reorganization and finite exact consistency checks.\n'
        'The written proofs, rather than those finite checks, are the mathematical\n'
        'basis of the statements and are submitted to independent scrutiny.\n')
    full = (preamble + '\n\\begin{document}\n' +
        (HERE/'frontmatter-v153.tex').read_text() + '\n' +
        (HERE/'introduction-v153.tex').read_text() + '\n' +
        '\n'.join(body) + '\n' + disclosure + '\n' + bibliography + '\n\\end{document}\n')
    old_labels = collections.Counter(LABEL.findall('\n'.join(original_all)))
    new_labels = collections.Counter(LABEL.findall(full))
    missing = list((old_labels - new_labels).elements())
    duplicates = [x for x,n in new_labels.items() if n>1]
    if missing or duplicates or INPUT.search(full):
        raise RuntimeError(f'Label/input audit failed: missing={missing}, duplicate={duplicates}')
    (HERE/'geometry.tex').write_text(full)
    receipt = {'revision':153, 'controlling_review_commit':REVIEW,
        'every_principal_part_retained_once':True, 'missing_predecessor_labels':missing,
        'duplicate_labels':duplicates, 'predecessor_label_count':sum(old_labels.values()),
        'current_label_count':sum(new_labels.values()),
        'predecessor_math_block_count':len(BLOCK.findall('\n'.join(original_all))),
        'predecessor_inputs_verified_against_git':source_hashes,
        'approved_textual_changes':changes, 'geometry_source_sha256':sha256(full.encode()),
        'new_core_sha256':sha256(new_core.encode()),
        'old_source_files_modified':False, 'proof_certified_by_computation':False}
    (HERE/'NONDELETION_V153.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def build(receipt: dict) -> None:
    for index in range(3):
        result = subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode',
            '-halt-on-error','geometry.tex'],cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (HERE/f'build-pass-{index+1}.txt').write_text(result.stdout)
        result.check_returncode()
    log = (HERE/'geometry.log').read_text(errors='replace')
    forbidden = ['undefined references','undefined citations','multiply defined',
                 'LaTeX Warning: Reference','LaTeX Warning: Citation','Overfull \\hbox']
    failures = [x for x in forbidden if x in log]
    if failures:
        raise RuntimeError(f'Build audit: {failures}')
    info = subprocess.check_output(['pdfinfo','geometry.pdf'],cwd=HERE,text=True)
    pages = int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    subprocess.run(['pdftotext','-layout','geometry.pdf','geometry.txt'],cwd=HERE,check=True)
    pdf = (HERE/'geometry.pdf').read_bytes()
    receipt.update({'compiled':True,'pages':pages,'pdf_sha256':sha256(pdf),'pdf_bytes':len(pdf),
        'clean_references_and_no_overfull_hboxes':True,
        'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip(),
        'historical_28_checks_rerun':False, 'Ballico_1993_full_text_comparison_completed':False,
        'journal_acceptance_asserted':False})
    (HERE/'BUILD_RECEIPT_V153.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    args = parser.parse_args()
    audit = assemble()
    if args.build:
        build(audit)
    print(json.dumps({'assembled':True,'built':args.build,'labels':audit['current_label_count']}))
