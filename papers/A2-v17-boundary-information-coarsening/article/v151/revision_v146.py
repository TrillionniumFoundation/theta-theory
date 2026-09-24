#!/usr/bin/env python3
"""Assemble and verify the isolated A2 v146 revision. No other branch is mutated."""
from pathlib import Path
from collections import Counter
import hashlib, json, os, re, shutil, subprocess, sys
SCRIPT=Path(__file__).resolve().parent
ROOT=SCRIPT.parents[1] if SCRIPT.name=='a2-v146' else SCRIPT.parents[3]
PREFIX='papers/A2-v17-boundary-information-coarsening/article'
BASE=ROOT/PREFIX/'v145'
HERE=ROOT/PREFIX/'v146'
BOOT=ROOT/'.revision-bootstrap/a2-v146'
BASE_SHA='89edc80cce6fd1801b356313544419d30f377636'
REVIEW='d8376b5dbb47422d93a474add8362d39cf2a68c1'
BRANCH='revision/a2-v146-referee-proof-completion-2026-09-24'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def dump(p,x):write(p,json.dumps(x,indent=2)+'\n')
def expand(p,root):
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(root/(m[1] if m[1].endswith('.tex') else m[1]+'.tex'),root),p.read_text())
def entry(verified=False,source=None):
    p=PREFIX+'/v146'
    status=('Native source: `'+source+'`. All 23 executed exact-regression scripts and all three native LaTeX builds passed. See the source-bound receipt; these checks do not certify all proofs or historical priority.') if verified else 'Native sources have been assembled. Build success must be read from the source-bound v146 receipt, not inferred from this source commit.'
    write(ROOT/'CURRENT_REVIEW_ENTRY.md','\n'.join([
      '# Canonical A2 referee entry — revision 146','',status,'',
      'Controlling v144 second report: `'+REVIEW+'`. Immediate predecessor: `'+BASE_SHA+'`.','',
      '**Principal submission:** [geometry.pdf]('+p+'/geometry.pdf) · [native source]('+p+'/geometry.tex).','',
      '**Separate applications manuscript:** [applications.pdf]('+p+'/applications.pdf).','',
      '**Non-submitted preserved research archive:** [archive-v144.pdf]('+p+'/archive-v144.pdf).','',
      '[Point-by-point response]('+p+'/RESPONSE_TO_V144_REPORTS_V146.md) · [Reading guide]('+p+'/README.md) · [Issue matrix]('+p+'/ISSUE_MATRIX_V146.json).','',
      '[Source lock]('+p+'/SOURCE_LOCK_V146.json) · [Build receipt]('+p+'/evidence/BUILD_RECEIPT_V146.json) · [Nondeletion audit]('+p+'/NONDELETION_V146.json) · [Literature audit]('+p+'/LITERATURE_AUDIT_V146.md).','',
      'New in v146: an unmarked single-point Artin local inverse, coefficient-support orientation, an explicit local unipotent kernel, and intrinsic reconstruction of nonconstant pencil subbundles over smooth projective bases; recovery of the actual source bundle; classification of geometric isomorphisms with a filtered nilpotent automorphism kernel; an explicit nonisotrivial family across six spectral collisions. The all-pencil theorem, uniform sharpness, curve theorem and all predecessor mathematical parts are preserved.','',
      'The complete Ballico 1993 theorem-level six-axis comparison remains documentary-open. No anticipation, nonanticipation, exhaustive priority or editorial-acceptance claim is certified. Earlier revision and review branches are unchanged.','']))
def assemble():
    assert BASE.exists() and (BOOT/'families.tex').exists()
    if HERE.exists():shutil.rmtree(HERE)
    shutil.copytree(BASE,HERE,ignore=shutil.ignore_patterns('*.pdf','*.aux','*.log','*.out','*.toc','*.pyc','__pycache__','evidence'))
    hist=HERE/'history/v145-root';hist.mkdir(parents=True)
    for f in BASE.iterdir():
        if f.is_file() and f.suffix in {'.tex','.py','.sh','.md','.json'}:shutil.copy2(f,hist/f.name)
    if (ROOT/'CURRENT_REVIEW_ENTRY.md').exists():shutil.copy2(ROOT/'CURRENT_REVIEW_ENTRY.md',hist/'CURRENT_REVIEW_ENTRY_AT_V145.md')
    preserve={}
    for f in BASE.rglob('*'):
        rel=f.relative_to(BASE)
        if not f.is_file() or f.suffix not in {'.tex','.py','.sh','.md','.json'} or 'evidence' in rel.parts or '__pycache__' in rel.parts:continue
        dest='history/v145-root/'+f.name if len(rel.parts)==1 else str(rel)
        preserve[str(rel)]={'sha256':sha(f),'preserved_at':dest}
    dump(HERE/'INHERITED_SOURCE_V146.json',{'predecessor_commit':BASE_SHA,'review_commit':REVIEW,'source_files':preserve})
    shutil.copy2(BOOT/'families.tex',HERE/'parts/31-moving-pencils-v146.tex')
    for n in ['check_v146.py','revision_v146.py','RESPONSE_TO_V144_REPORTS_V146.md']:shutil.copy2(BOOT/n,HERE/n)
    old=(BASE/'frontmatter-v145.tex').read_text()
    abstract=r'''\begin{abstract}
We reconstruct every complex quadratic pencil from an abstract unmarked
finite-order neighbourhood of its multiplication-failure scheme.  For
embedding dimension \(n\ge3\), the smallest uniform order is
\(d=n^2+2n-4\); all lower orders are independent of the pencil.  A
neighbourhood supported on one Schubert line already suffices.  More
generally, for a pencil subbundle varying over a smooth connected
projective base with nontrivial source projectivization, the unmarked
finite scheme recovers the base, the actual source bundle and the whole
pencil family, up to one constant left transformation.  The proof
recovers intrinsic tensor rulings and the varying coefficient line.
We describe all geometric isomorphisms through their linear data and a
filtered nilpotent automorphism kernel.  An explicit nonisotrivial
family illustrates reconstruction through spectral collisions.  The
universal finite neighbourhood is compatible with arbitrary complex
base change with its relative socle retained.  For regular pencils the
spectral readout includes all elementary divisors and higher Fitting
incidence schemes.  Framed parameter embeddings, unmarked geometric
inverses and relative constructions are distinguished throughout.
\end{abstract}'''
    fm=re.sub(r'\\begin\{abstract\}[\s\S]*?\\end\{abstract\}',lambda m:abstract,old).replace('revision 145','revision 146')
    write(HERE/'frontmatter-v146.tex',fm)
    intro=(BASE/'parts/00-principal-introduction-v145.tex').read_text()
    addition=r'''\subsection{A moving family, not only its individual fibres}
The same finite object also reconstructs a pencil that varies over its
projective reduction.  Let \(B\) be a smooth connected projective
complex variety, let \(\mathcal U\) have rank \(n\) with nontrivial
projectivization, and let \(\mathcal R\) be a rank-two subbundle of
\(\Sym^2V\otimes\OO_B\) with locally free quotient.  Use the local
ideal \((\det T)I_p(\gamma\Sym^2T)\) in
\(\Hom(\mathcal U,V)\) and truncate at order \(d\).
Theorem~\ref{thm:moving-reconstruction-v146} states that two resulting
abstract finite schemes are isomorphic exactly when their data are
related by an isomorphism of reduced bases, one constant linear left
map, and an actual isomorphism of the source bundles, carrying one
pencil subbundle to the other.  The projection and both tensor factors
are forgotten in the input.  The varying coefficient line is recovered
as a subbundle, not by pointwise choices of projective coordinates.

This strengthens the constant-pencil curve theorem in two directions:
the reduced base and source bundle may vary in the comparison, and the
pencil need not be constant on that base.  Example~\ref{ex:nonconstant-pencil-v146}
has a nonconstant unordered cross-ratio and six spectral collision
points, all retained by the same finite scheme.  Theorem~\ref{thm:automorphism-kernel-v146}
then identifies the remaining freedom in an isomorphism.  Its quotient
is the group of the recovered linear data; its kernel acts trivially
on the associated graded scheme and has a terminating commutator
filtration.  Explicit nonlinear shears show why that kernel cannot be
omitted.  These statements are consequences of the unmarked inverse,
not additional claims of novelty for the classical Pluecker map or
for spectral cross-ratios.

'''
    anchor='\\subsection{Framed families and spectral consequences}'
    assert intro.count(anchor)==1
    write(HERE/'parts/00-principal-introduction-v146.tex',intro.replace(anchor,addition+anchor))
    geom=(BASE/'geometry.tex').read_text().replace('frontmatter-v145','frontmatter-v146').replace('00-principal-introduction-v145','00-principal-introduction-v146')
    anchor='\\input{parts/29-curve-reconstruction-v145.tex}'
    assert geom.count(anchor)==1
    geom=geom.replace(anchor,anchor+'\n\\input{parts/31-moving-pencils-v146.tex}')
    write(HERE/'geometry.tex',geom)
    write(HERE/'applications.tex',(BASE/'applications.tex').read_text().replace('revision 145','revision 146'))
    write(HERE/'build.sh','#!/usr/bin/env bash\nset -euo pipefail\ncd "$(dirname "$0")"\nexport OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1\npython revision_v146.py build\n')
    readme='''# A2 revision 146 — referee reading guide

The principal review object is **geometry.pdf**, built from geometry.tex. The presentation uses theorem/proof-centered AMS mathematical typography, not a conference template. Every input needed by the principal proof is included in that manuscript. The title and all original all-pencil claims are retained.

Read the original sharp inverse and curve theorem first, then **Reconstruction of moving pencils and their isomorphisms**. The new section proves the varying coefficient subbundle lemma, the unmarked moving-family inverse, the actual source-bundle gluing step, uniform sharpness, and the filtered automorphism-kernel exact sequence. It ends with an everywhere regular nonconstant P1-family through six spectral collisions. The spectral classification that follows is retained with its classical attribution.

The separate **applications.pdf** retains the real likelihood and projective critical-scheme results. The complete **archive-v144.pdf** is a non-submitted historical research archive, not an additional submission supplement. All prior mathematical part files remain unchanged; modified root documents have byte-preserved copies under history/v145-root. The predecessor v145 directory is unchanged.

- Response: RESPONSE_TO_V144_REPORTS_V146.md.
- Exact issue dispositions and domains: ISSUE_MATRIX_V146.json.
- Literature boundary and six comparison axes: LITERATURE_AUDIT_V146.md.
- Immutable source: SOURCE_LOCK_V146.json and PROVENANCE_MANIFEST_V146.json.
- Completed execution and PDF hashes: evidence/BUILD_RECEIPT_V146.json.
- Source preservation: INHERITED_SOURCE_V146.json and NONDELETION_V146.json.

Run `bash build.sh` from this directory in the repository checkout (Python with SymPy/NumPy and native pdflatex/poppler required). It executes 22 regression scripts and compiles all three PDFs. Finite regressions do not formally verify the geometric proofs. The Ballico 1993 full-text theorem comparison remains documentary-open; neither metadata nor a different article is substituted for it. No editorial decision or exhaustive priority clearance is asserted.
'''
    write(HERE/'README.md',readme)
    audit='''# Literature and scope audit — A2 v146

## What was inherited and what was checked in this revision

The preserved LITERATURE_AUDIT_V145.md contains the predecessor's full-text Ohta pins and its separate Ballico 1996 comparison. The new revision retains those attributions and the independent dimension/component proofs. It does not represent those historical inspections as a newly successful full-PDF retrieval. Current publisher and exact-title searches did not produce the complete Ballico 1993 article; the available Library search did not contain that article.

## Ballico 1993: explicit six-axis ledger

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13; DOI 10.1002/mana.19931630102.

| Axis | Present manuscript | Ballico 1993 theorem text |
|---|---|---|
| Parameter space | Quadratic relation planes; cube-zero algebras and socle Grassmannians; nonconstant rank-two subbundles over admissible projective bases | Not obtained; no content inferred |
| Defining map | Literal unital symmetric multiplication; local ideal (det T) I_p(gamma Sym^2 T) | Not obtained; no map identity inferred |
| Scheme structure | Full maximal-minor/Fitting ideal, including nonreduced structure | Not obtained; no claim about reduced versus nonreduced scope |
| Infinitesimal information | First nonzero relation kernel at d=n^2+2n-4 recovers the untruncated homogeneous cone | Not obtained; no comparison theorem invented |
| Families and base change | Universal finite relative construction with supplied socle; separately an intrinsic inverse over smooth reduced projective bases | Not obtained; no family or base-change statement inferred |
| Inverse conclusion | All-pencil inverse; moving-family and actual-bundle reconstruction; geometric automorphism quotient and nilpotent kernel | Not obtained; no anticipation or nonanticipation conclusion |

The strengthened theorem does not close this documentary obligation. Every entry in the last column is unverified at theorem level. The distinct 1996 article remains a substantive antecedent but is not a substitute.

## Classical input and mathematical contribution

The pencil exterior representation, Pluecker embedding, matrix rank loci and spectral cross-ratio are classical ingredients, explicitly identified as such. The new theorem proves their intrinsic assembly for a varying coefficient subbundle, including the global orientation, constant left map, actual right-bundle gluing and residual geometric automorphism kernel. No priority claim for the individual classical ingredients is made. Ohta's full orthogonal partition/dominance input is retained with the exact proposition, theorem and page pins recorded in v145. The independent operator priority question remains with the non-submitted archive.

## Domains

All complex fibre pencils are permitted by the inverse. Its reduced base is smooth connected projective and the right projective bundle is nontrivial. Arbitrary nonreduced-base change belongs to the separate marked-socle construction. Regularity belongs to the spectral readout. Split semisimplicity and simple disjoint poles belong to the critical-divisor application; real definiteness and separated data belong to the real likelihood application. The automorphism exact sequence is a statement about complex geometric groups, not a moduli-stack or full deformation equivalence.
'''
    write(HERE/'LITERATURE_AUDIT_V146.md',audit)
    issues={
     '1_5_11_16_intrinsic_consequence':'new proof: moving coefficient subbundle inverse, actual bundle recovery and nonisotrivial family; editorial significance is for independent assessment',
     '2_15_7_sharpness':'preserved and extended: smallest uniform d; not pairwise minimality',
     '3_4_15_4_families':'new group-kernel theorem; geometric, framed and marked-socle claims remain distinct; no stack equivalence',
     '6_15_3_orthogonal_input':'v145 exact Ohta references and full-O versus SO proof preserved, not newly claimed',
     '7_9_15_1_15_2_critical_arguments':'v145 rational-point and nonreduced Hessian expansions preserved and re-executed in separate applications',
     '12_13_publication_object':'principal reconstruction paper, separate applications, complete non-submitted research archive; no deletion',
     '10_Ballico_1993':'documentary-open: complete theorem text not obtained; no priority clearance',
     '14_evidence':'22 actual script statuses, native PDFs and source hashes required; computation does not certify proofs or priority',
     '15_5_15_6_scope':'all-pencil inverse retained; exact regular/split/real/nonreduced-base conditions retained; full Fitting data not reduced rank data'}
    dump(HERE/'ISSUE_MATRIX_V146.json',{'revision':146,'controlling_review':REVIEW,'predecessor':BASE_SHA,'issues':issues})
    dump(HERE/'SOURCE_LOCK_V146.json',{'revision':146,'predecessor_commit':BASE_SHA,'review_commit':REVIEW,'source_commit':None,'build_status':'not yet verified','historical_priority_certified':False})
    entry()
    print('Assembled',HERE,'with',len(preserve),'preserved predecessor source files')

def build():
    os.chdir(HERE);e=HERE/'evidence';e.mkdir(exist_ok=True)
    names='exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact revision137_exact revision138_exact revision139_exact revision140_exact revision141_spectral_exact revision141_likelihood_exact revision142_exact revision143_critical_exact revision144_projective_exact'.split()
    scripts=['checks/'+n+'.py' for n in names]+['check_v145.py','check_v146.py','check_local_v146.py']
    records=[]
    for script in scripts:
        print('Execute',script,flush=True)
        log=e/(Path(script).stem+'.log')
        with log.open('w') as out:r=subprocess.run([sys.executable,script],stdout=out,stderr=subprocess.STDOUT)
        records.append({'script':script,'sha256':sha(HERE/script),'returncode':r.returncode,'log':str(log.relative_to(HERE))})
        dump(e/'EXECUTED_CHECKS_V146.json',records)
        if r.returncode:print(log.read_text());raise SystemExit(r.returncode)
    for name in ['geometry','applications','archive-v144']:
        for ext in ['aux','out','toc']:(HERE/(name+'.'+ext)).unlink(missing_ok=True)
        for k in range(1,4):
            print('Compile',name,'pass',k,flush=True)
            log=e/(name+'-pass'+str(k)+'.log')
            with log.open('w') as out:r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],stdout=out,stderr=subprocess.STDOUT)
            if r.returncode:print(log.read_text()[-12000:]);raise SystemExit(r.returncode)
        aux=(HERE/(name+'.aux')).read_text()
        write(HERE/(name+'-labels.aux'),'\n'.join(x for x in aux.splitlines() if x.startswith('\\newlabel{') and not x.startswith('\\newlabel{tocindent'))+'\n')
        shutil.copy2(HERE/(name+'.log'),e/(name+'-final.log'))
    verify()

def verify():
    e=HERE/'evidence';checks={}
    text={n:expand(HERE/(n+'.tex'),HERE) for n in ['geometry','applications','archive-v144']}
    labels=lambda t:re.findall(r'\\label\{([^}]+)\}',t)
    refs=lambda t:set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',t))
    main=text['geometry'];apps=text['applications'];archive=text['archive-v144']
    checks['principal_all_references_internal']=not(refs(main)-set(labels(main))) and '\\externaldocument' not in main
    checks['applications_references_resolve']=not(refs(apps)-set(labels(main))-set(labels(apps)))
    checks['archive_references_resolve']=not(refs(archive)-set(labels(archive)))
    for name,t in text.items():
        checks[name+'_labels_unique']=len(labels(t))==len(set(labels(t)))
        log=(e/(name+'-final.log')).read_text(errors='replace')
        checks[name+'_no_unresolved_references']=not bool(re.search(r'(There were undefined references|Citation .+ undefined|Reference .+ undefined|multiply defined|Rerun to get cross-references)',log))
        checks[name+'_no_overfull_boxes']='Overfull \\hbox' not in log and 'Overfull \\vbox' not in log
        checks[name+'_native_pdf_exists']=(HERE/(name+'.pdf')).exists()
    inherited=json.loads((HERE/'INHERITED_SOURCE_V146.json').read_text())
    checks['all_predecessor_source_bytes_preserved']=all((HERE/r['preserved_at']).exists() and sha(HERE/r['preserved_at'])==r['sha256'] for r in inherited['source_files'].values())
    checks['all_v145_part_files_unchanged']=all(sha(HERE/f.relative_to(BASE))==sha(f) for f in (BASE/'parts').rglob('*.tex'))
    pattern=r'\\begin\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}[\s\S]*?\\end\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}'
    old=expand(BASE/'geometry.tex',BASE)
    oldblocks=re.findall(pattern,old);newblocks=re.findall(pattern,main)
    checks['all_v145_principal_math_blocks_retained']=not(Counter(oldblocks)-Counter(newblocks))
    checks['all_v145_principal_labels_retained']=set(labels(old))<=set(labels(main))
    checks['archive_driver_unchanged']=sha(HERE/'archive-v144.tex')==sha(BASE/'archive-v144.tex')
    checks['new_moving_and_automorphism_results_present']={'thm:moving-reconstruction-v146','thm:automorphism-kernel-v146','lem:moving-coefficients-v146','ex:nonconstant-pencil-v146','ex:invisible-shear-v146'}<=set(labels(main))
    checks['separate_application_scope_retained']={'thm:projective-critical-v144','thm:critical-ramification-v144','thm:totally-real-reciprocal-likelihood'}<=set(labels(apps))
    checks['local_inverse_exact_regression_passed']=json.loads((e/'LOCAL_INVERSE146_EXACT.json').read_text())['ok']
    checks['local_inverse_and_unrestricted_family_present']={'thm:artin-local-inverse-v146','thm:unrestricted-moving-v146','prop:local-automorphisms-v146','lem:coefficient-orientation-v146'}<=set(labels(main))
    records=json.loads((e/'EXECUTED_CHECKS_V146.json').read_text())
    checks['twenty_three_scripts_executed_successfully']=len(records)==23 and all(r['returncode']==0 and sha(HERE/r['script'])==r['sha256'] for r in records)
    checks['v145_exact_regression_passed']=json.loads((e/'REVISION145_EXACT.json').read_text())['ok']
    checks['v146_exact_regression_passed']=json.loads((e/'REVISION146_EXACT.json').read_text())['ok']
    pdfs={}
    for n in text:
        f=HERE/(n+'.pdf');info=subprocess.check_output(['pdfinfo',str(f)],text=True)
        pdfs[n]={'pages':int(re.search(r'^Pages:\s*(\d+)',info,re.M)[1]),'sha256':sha(f),'bytes':f.stat().st_size}
    source=os.environ.get('A2_SOURCE_COMMIT','LOCAL-PREFLIGHT-NOT-A-REMOTE-SOURCE')
    result={'revision':146,'source_commit':source,'predecessor_commit':BASE_SHA,'controlling_review_commit':REVIEW,'all_checks_pass':all(checks.values()),'checks':checks,'executed_script_count':len(records),'executed_scripts':records,'pdfs':pdfs,'labels':{n:len(labels(t)) for n,t in text.items()},'preserved_predecessor_source_files':len(inherited['source_files']),'preserved_principal_math_blocks':len(oldblocks),'proof_certified_by_computation':False,'Ballico_1993_full_text_comparison_completed':False,'historical_priority_certified':False}
    dump(e/'BUILD_RECEIPT_V146.json',result)
    dump(HERE/'NONDELETION_V146.json',{'source_commit':source,'predecessor_commit':BASE_SHA,'all_source_bytes_preserved':checks['all_predecessor_source_bytes_preserved'],'all_v145_parts_unchanged':checks['all_v145_part_files_unchanged'],'all_principal_blocks_retained':checks['all_v145_principal_math_blocks_retained'],'all_principal_labels_retained':checks['all_v145_principal_labels_retained'],'source_files':inherited['source_files'],'preservation_is_not_proof_certification':True})
    dump(HERE/'SOURCE_LOCK_V146.json',{'revision':146,'source_commit':source,'predecessor_commit':BASE_SHA,'review_commit':REVIEW,'publication_object':'geometry.pdf','separate_application':'applications.pdf','non_submitted_archive':'archive-v144.pdf','receipt':'evidence/BUILD_RECEIPT_V146.json','all_checks_pass':result['all_checks_pass'],'historical_priority_certified':False})
    manifest={}
    for f in HERE.rglob('*'):
        rel=f.relative_to(HERE)
        if f.is_file() and f.suffix in {'.tex','.py','.sh','.md','.json'} and not any(k in rel.parts for k in ['evidence','__pycache__']) and f.name not in {'PROVENANCE_MANIFEST_V146.json','SOURCE_LOCK_V146.json','NONDELETION_V146.json'}:manifest[str(rel)]=sha(f)
    dump(HERE/'PROVENANCE_MANIFEST_V146.json',{'source_commit':source,'sha256':manifest})
    print(json.dumps(result,indent=2))
    if not result['all_checks_pass']:raise SystemExit('v146 verification failed')
    entry(True,source)

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in {'assemble','build','verify'}:raise SystemExit('Usage: revision_v146.py assemble|build|verify')
    globals()[sys.argv[1]]()
