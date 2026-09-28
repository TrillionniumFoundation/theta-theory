#!/usr/bin/env python3
"""Materialize the small edits to inherited files; all new proofs are plain TeX.

Run only on the new v46 author branch. No external downloads, encoded payload,
source deletion, default-branch update or historical-branch rewrite is used.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess

P=Path('papers/A2-v17-boundary-information-coarsening')
H=P/'history/v45-review-baseline'
SOURCE='2f064b86b4e071d24ad671f4dc652d7de32a56a4'
TARGET={
'main.tex': 'e03944f219b88340adf7195b8b1be24f5c14d69c',
'article/01f_generic_rigidity_overview_v45.tex': 'db914e2fc86204be5d76e8424f3bda562b4ccf29',
'article/23j_generic_finite_channel_rigidity_v45.tex': '18e7e152e6296716232cd289570cfb7f4642712d',
'v5/references_v43.tex': 'efcb092ad97cfc3a0afed685eaa6fe1e543cfa2a',
'article/01g_quantized_reconstruction_overview_v46.tex': '5b9df93cc7fe56b72cd55557f7d767dd40786b84',
'article/23k_quantized_law_stability_v46.tex': 'fcc9069b176ff6423652f3ad2b0812c6858137d7',
}

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def blob(path):
    d=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()

def replace_once(text,old,new):
    require(text.count(old)==1,'Expected exactly one edit anchor: '+old)
    return text.replace(old,new)

def verify_targets():
    for name,sha in TARGET.items():require(blob(P/name)==sha,'Local-reviewed target differs: '+name)
    subprocess.run(['python3','-B',str(P/'tools/check_revision_v46.py')],check=True)

def main():
    if H.exists():
        verify_targets()
        return
    manifest_path=Path('deliveries/a2-v45')/SOURCE/'active-source-manifest.json'
    require(blob(manifest_path)=='5952fb7ced54d21ea8680d845d3b09a378ecd7dc','Wrong native baseline manifest')
    manifest=json.loads(manifest_path.read_text())
    for entry,files in manifest.items():
        for name,identity in files.items():require(blob(P/name)==identity['git_blob'],'Inherited baseline differs: '+name)
    require(blob(Path('README.md'))=='77cfebf6346f21cfd20c84889b6d9fbdc39ee28a','Root baseline changed')
    H.mkdir(parents=True)
    for name in ('main.tex','article/01f_generic_rigidity_overview_v45.tex','article/23j_generic_finite_channel_rigidity_v45.tex','v5/references_v43.tex','README.md'):
        dest=H/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/name,dest)
    shutil.copy2('README.md',H/'ROOT_README.md')
    shutil.copy2(manifest_path,H/'active-source-manifest.json')
    (H/'IDENTITY.json').write_text(json.dumps({'review_commit':'0614a20bbba6312830b5523b806ddc726a6333f1','review_ready_commit':'1e60d66b4826bf6b6f64a342b66857774ac3b420','compiled_source_commit':SOURCE,'run_id':34829418911,'source_artifact_id':10341597640,'native_artifact_id':10341144241},indent=2)+'\n')
    s=(P/'main.tex').read_text().replace('revision 45','revision 46')
    s=replace_once(s,'generic finite-channel rigidity, lattice holonomy,','generic finite-channel rigidity, quantized-law stability, lattice holonomy,')
    addition=r'''Under a common holomorphic-support bound and finite asymmetry witnesses,
we obtain a quantitative inverse from finite histograms of the transverse
laws to the entire table and marked lattice.  Its modulus combines a finite
Bellman contact recursion, a quantified continuation of finite support jets,
and intrinsic incidence registration.  It supplies a finite accuracy
prescription, with categorical sampling and even-flight bias bounds; it does
not require longitudinal endpoint positions or an unspecified separation
modulus of the exact inverse.

'''
    s=replace_once(s,'The local information depends on the retained record.',addition+'The local information depends on the retained record.')
    s=replace_once(s,r'\input{article/01f_generic_rigidity_overview_v45}',r'\input{article/01f_generic_rigidity_overview_v45}'+'\n'+r'\input{article/01g_quantized_reconstruction_overview_v46}')
    s=replace_once(s,r'\input{article/23j_generic_finite_channel_rigidity_v45}',r'\input{article/23j_generic_finite_channel_rigidity_v45}'+'\n'+r'\input{article/23k_quantized_law_stability_v46}')
    (P/'main.tex').write_text(s)
    p=P/'article/23j_generic_finite_channel_rigidity_v45.tex'
    p.write_text(replace_once(p.read_text(),'zero-gain edge followed by its reverse','zero-net-gain backtrack $ee^{-1}$'))
    p=P/'article/01f_generic_rigidity_overview_v45.tex'
    p.write_text(replace_once(p.read_text(),'Image-registration stability is not promoted to\nan effective law-to-entire-boundary rate.',r'''Image-registration stability alone is not a law-to-entire-boundary rate;
Section~\ref{sec:v46-quantized-stability} proves a separate quantitative
law-to-table estimate under explicit uniform analytic and forward bounds.'''))
    p=P/'v5/references_v43.tex'
    bib=r'''\bibitem{Trefethen2020}
L.~N.~Trefethen, Quantifying the ill-conditioning of analytic continuation,
\emph{BIT Numer. Math.} \textbf{60} (2020), 901--915.
\href{https://doi.org/10.1007/s10543-020-00802-7}{doi:10.1007/s10543-020-00802-7}.

'''
    p.write_text(replace_once(p.read_text(),r'\end{thebibliography}',bib+r'\end{thebibliography}'))
    (P/'tools/retain_native_v46.py').write_text((P/'tools/retain_native_v45.py').read_text().replace('v45','v46'))
    Path('README.md').write_text('''# Theta-Theory: A2 revision 46 and preserved workstreams

## A2: quantitative reconstruction from quantized transverse laws

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards** — Qian Qi, September 14, 2026.

[Complete main source](papers/A2-v17-boundary-information-coarsening/main.tex) · [Manuscript entry](papers/A2-v17-boundary-information-coarsening/README.md) · [Response to v45](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V46.md) · [Verification](papers/A2-v17-boundary-information-coarsening/VERIFICATION_V46.md).

Author branch: `revision/a2-v46-quantized-law-boundary-stability-2026-09-14`. The addressed report is pinned at `0614a20bbba6312830b5523b806ddc726a6333f1`. Introductory Theorem 1.4 and Section 19 add a conditional quantitative histogram-law-to-table inverse, including recovery of the unknown marked Euclidean lattice. The precise analytic priors, finite accuracy prescription and statistical bounds are printed in the complete manuscript. The qualitative generic theorem is unchanged except for the requested zero-net-gain backtrack wording.

All 226 inherited theorem-style environments, 22 remarks, three mathematical parts, auxiliary proofs and the complete companion remain active. Seven theorem-style environments and two input modules are added. No fixed finite-scalar exact recovery, sharp minimax rate, unmarked discovery or referee acceptance is claimed.

Native products are built from the actual materialized source commit and retained with full logs and input manifests under `deliveries/a2-v46/` on new products branches. The final review-ready entry records completed native publication checks; the workflow preparation head is not silently identified with the compiled source.

## A1 and the preserved programme

[Exact pre-v46 root entry](papers/A2-v17-boundary-information-coarsening/history/v45-review-baseline/ROOT_README.md) · [Pre-v46 paper entry](papers/A2-v17-boundary-information-coarsening/history/v45-review-baseline/README.md) · [Earlier programme index](README_PRE_V27.md).

A1, other workstreams, historical manuscripts, reports and delivery directories are unchanged. No default-branch merge, force update of a historical branch, permission change or membership change is made.
''')
    (P/'README.md').write_text('''# A2 author revision 46

**Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards**  
Qian Qi — September 14, 2026.

[Full main source](main.tex) · [Complete unchanged companion](two_collision.tex) · [Point-by-point response](RESPONSE_TO_REFEREE_V46.md) · [Historical derivation audit](HISTORICAL_DERIVATION_AUDIT_V46.md) · [Preservation](PRESERVATION_AND_DEPENDENCIES_V46.md) · [Verification](VERIFICATION_V46.md).

Introductory Theorem 1.4 and Section 19 supply a quantitative inverse from finite histograms of signed transverse endpoint laws to complete analytic obstacle images, placements and the marked Euclidean lattice. Uniform analytic and forward bounds are explicit; finite-order constants are computed by a Bellman recursion and propagation through the exact local inverse. The observed reconstruction transcript uses no longitudinal coordinates. Calibration remains separately specified.

The latest report is pinned at `0614a20bbba6312830b5523b806ddc726a6333f1`; its compiled baseline is `2f064b86b4e071d24ad671f4dc652d7de32a56a4`. Exact edited originals and the baseline active manifest are preserved in `history/v45-review-baseline/`.

Author branch: `revision/a2-v46-quantized-law-boundary-stability-2026-09-14`. Source-matched complete native products and raw evidence are retained in `deliveries/a2-v46/<actual-source-commit>/` on the corresponding new products and review-ready branches. The source-preparation workflow head and actual compiled source are distinguished in the evidence.

All inherited mathematics remains active. The severe worst-case conditioning is recorded, not suppressed. The next independent review should assess the new proof and its significance; successful compilation and finite diagnostics are not mathematical certification or editorial acceptance.
''')
    verify_targets()

if __name__=='__main__':main()
