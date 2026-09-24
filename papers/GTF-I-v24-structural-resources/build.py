#!/usr/bin/env python3
"""Build the v24 referee package without altering predecessor files.

Dependencies: Python >=3.11, sympy 1.14.0, PyMuPDF 1.26.7, pdflatex.
Generated evidence reports executed checks, never independent proof approval.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile
import fitz

P = Path(__file__).resolve().parent
OLD = Path(os.environ.get('GTF_V23_DIR', str(P.parent/'GTF-I-v23-compatible-frontiers'))).resolve()
REVIEW = 'e34f5eb4fe1b1f03018c6baec2e594ab22766dfb'
PREDECESSOR = 'e926b783b643b3e7f275a18105528927b76cc97b'
EXPECTED = {
    'paper.pdf':'b2e85e87f281fcbf867d4a02acfd03a183da4a14261276291de111397b4a9e4d',
    'complete-development.pdf':'17e33f92f9a16187de17a4ae1b4fc64a3a72605c04338a1c14db9a5dbb600a71',
    'HISTORICAL_PIPELINE_V20.json':'6aa747159fbe4cba56c1fc54dccd8dd955e242e3f65c99e2bf5bad4a95aff7bf',
    'main.tex':'92266256202f7607c43fd68e404d0411e70bc9b00a435a2193602c4da14c65c1',
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def run(arguments: list[str], cwd: Path = P, **kwargs):
    return subprocess.run(arguments,cwd=cwd,check=True,text=True,**kwargs)

def main() -> None:
    E = P/'evidence'
    E.mkdir(exist_ok=True)
    for name,digest in EXPECTED.items():
        require(sha(OLD/name) == digest, 'frozen predecessor mismatch: '+name)
    inheritance = json.loads((OLD/'INHERITANCE.json').read_text())
    for name,digest in inheritance['unchanged_math_modules'].items():
        require(sha(OLD/name) == digest, 'inherited module mismatch: '+name)
    old_sources = {f.relative_to(OLD).as_posix():sha(f) for f in sorted(OLD.rglob('*'))
                   if f.is_file() and 'evidence' not in f.relative_to(OLD).parts
                   and f.suffix in {'.tex','.py','.md','.json'}}
    write_json(E/'PREDECESSOR_SOURCE_HASHES.json',old_sources)

    # Idempotent metadata correction from the author-maintained bibliography.
    # It affects only the new source and is recorded in the publication commit.
    mainfile = P/'main.tex'
    text = mainfile.read_text()
    text = text.replace('W. C. Flower','R. A. Flower')
    if '\\emergencystretch=2em' not in text:
        text = text.replace('\\begin{document}','\\emergencystretch=2em\n\\begin{document}',1)
    mainfile.write_text(text)
    write_json(E/'EDITORIAL_PREFLIGHT.json',{
        'author_metadata':'R. A. Flower, verified against Hellman author bibliography',
        'layout':'two-em emergency paragraph stretch; no mathematical source reduction',
        'idempotent':True,
    })

    suites = [
      ('v24',P,'verify.py',['certificate','selector','polynomial','profile','shared-row','autonomous']),
      ('v23',OLD,'verify_v23.py',['minimax-as-bayes','wrong-terminal-denominator','drop-minors','shared-row-free','unpriced-calibration','fair-bit-exact','wrong-roc-order']),
      ('v22',OLD,'verify.py',['walk-absorption','walk-time','revelation-prior','revelation-bottleneck','frontier-rounding','active-budget','confidence-gap','physical-buffer']),
      ('v21',OLD,'verify_v21.py',['block-default','block-hazard','precision','capacity','physical-margin','clock','confidence','training-transport']),
      ('v20',OLD,'verify_v20.py',['triangle','response','labels','profile','margin','clip']),
    ]
    results,negative = {},[]
    for label,directory,script,mutants in suites:
        extra = ['--output-dir',str(E)] if label == 'v24' else []
        normal = json.loads(run([sys.executable,script,*extra],cwd=directory,capture_output=True).stdout)
        optimized = json.loads(run([sys.executable,'-O',script],cwd=directory,capture_output=True).stdout)
        require(normal == optimized, 'normal/optimized mismatch: '+label)
        results[label] = normal
        write_json(E/(label.upper()+'_CHECKS.json'),normal)
        for opt in ([],['-O']):
            for mutant in mutants:
                result = subprocess.run([sys.executable,*opt,script,'--mutant',mutant],
                                        cwd=directory,text=True,capture_output=True)
                require(result.returncode != 0, 'undetected negative control: '+label+'/'+mutant)
                negative.append({'suite':label,'mutant':mutant,'optimized':bool(opt),
                                 'detected':True,'last_error':result.stderr.splitlines()[-1] if result.stderr else ''})
        print('Verified '+label,flush=True)
    write_json(E/'NEGATIVE_CONTROLS.json',negative)

    # Preserve the old program graph and the exact historical qualification files.
    H = P/'history/v23'
    H.mkdir(parents=True,exist_ok=True)
    for name in ['HISTORY_AUDIT.md','PIPELINE_STATUS.json','PROOF_STATUS.json',
                 'LITERATURE_CROSSWALK.md','RESOURCE_LEDGER.md','INHERITANCE.json',
                 'RESPONSE_TO_REFEREE.md','HISTORICAL_PIPELINE_V20.json']:
        shutil.copyfile(OLD/name,H/name)
    (P/'HISTORY_AUDIT.md').write_text('''# Revision 24 historical and first-principles audit

The controlling review is e34f5eb4fe1b1f03018c6baec2e594ab22766dfb, against
v23 package e926b783b643b3e7f275a18105528927b76cc97b. This revision descends
from that review; it does not restart from an older A1 manuscript.

The actual v23 compatible-occupations, binary-noisy-frontiers,
three-report-frontier, acquisition-and-resource-order and
 theta-frontier-consumers modules supply the accepted r6 repairs.
The continuation, decision-continuations, weighted-residuals,
joint-residuals and streaming-complexity modules fix the causal quotient,
shift compatibility and previously established majority widths.
The physical-complexity, physical-full-profile, physical-frontier,
microscopic-composition and Gaussian transport modules fix the original
row-event task, positive-noise family, actual mark, resource cuts and
transport hypotheses. Adaptive-testing and nonlinear-testing contain the
older revealed-law and polynomial-certification results; these are not
rebranded as the present sampled-preparation dual.

The General Theta Foundations v0.1 blueprint fixes positive experimental
kernels, actual preparation, executable tests, causality and charged
simulation before derived geometry. The new proof uses that order:
actual likelihoods -> posterior continuation -> validation-test quotient
-> architecture-free prior certificate and residual-state implementation.

All 35 inherited mathematical-module digests are checked. Every v23
source file is hashed in evidence/PREDECESSOR_SOURCE_HASHES.json. The
unchanged historical graph and previous audit files are copied to
history/v23, so their complete derivation references remain available.
The whole 96-page predecessor article and 649-page predecessor development
are preserved in the paired full volumes, page by page.

The old odd-horizon majority-width theorem, ideal marked separation value
and three-response decision invariant are not new v24 claims. The new
physical result is a matched minimum-preparation segment, not a proof of
the least peak width, the entire margin curve or eleven-paper closure.
A2 remains an independent geometric chain. The original B4 aggregate and
broad C2 form/rigidity/optional-projection obligations are retained, not
replaced by a finite-state or Gaussian stability assertion.
''')
    (P/'RESOURCE_LEDGER.md').write_text('''# Resource ledger for the new physical audit

| Resource | Charged value |
|---|---:|
| Candidate training preparations | 2 |
| Fresh candidate validation preparations | 1 |
| Fresh target validation preparations | 1 |
| Total preparations | 4 |
| Report/mark updates | 12 |
| Decision labels | 5 |
| Peak clocked persistent labels | 12 |
| Separate calibration samples or counters | 0 |
| Random bits or stochastic selector | 0 |
| Explicit autonomous phase-tagged states | at most 75 |

Full profile: (1,2,3,3,4,5,5,10,12,10,10,7,3).
Training marks are read and discarded. Validation marks are used.
The event and row are selected before either validation. Candidate and
target validations are independent of training. No first-bit buffer or
candidate-event accumulator lies outside the profile.

The theorem proves N_c(W)=2 for W>=12 on the stated threshold interval.
It does not prove that twelve is the smallest feasible peak. The earlier
minimum decision alphabet of three remains valid with longer training;
the shortest new audit uses five decision labels. Old resource points
are therefore retained rather than deleted under a different resource
order.

For R confidence repetitions, total preparations are 4R and a clocked
implementation uses at most 12(2R+1) labels. This is an upper construction,
not a confidence lower frontier. Atomic autonomous stochastic updates in
the separate binary example are not equated with their fair-bit-expanded
implementation; time, precision and state costs are stated separately.
''')
    write_json(P/'PROOF_STATUS.json',{
        'schema':'gtf24.proof-status/1','analytic_proofs_in_main':True,
        'independent_referee_or_formal_verification':False,
        'new_claims':{
          'posterior_predictive_dual':'proved; compact parameter, finite alphabet, unrestricted memory',
          'outer_dominating_row_converse':'proved; declared reset/validation interface',
          'physical_minimum_training':'proved: N=2 at every W>=12 and stated interval',
          'two_preparation_selector_minimum':'proved exactly for the specified selector, not global score optimality',
          'full_profile':'explicit deterministic implementation, peak12; not peak optimality',
          'subdivision_certificate':'proved HS/m gap; block degrees d_r; not global SOS degree',
          'stationary_autonomous_formula':'classical Hellman-Cover specialization, proved and attributed',
          'autonomous_finite_time_upper':'proved conservative dyadic implementation bound',
          'raw_physical_confidence':'proved upper construction only'},
        'not_proved':['W=3..11 physical preparation boundary','least peak width at N=2',
          'optimal score for all N=2 controllers','uniform global Putinar degree',
          'generic controlled K-state minimax recursion','optimal joint time-precision-memory frontier',
          'B4/C2 aggregate closure','eleven-paper closure'],
        'norberg_original_proof_comparison':'incomplete; original proof not obtained',
        'finite_checks_are_analytic_proofs':False,
    })
    write_json(P/'PIPELINE_STATUS.json',{
        'schema':'gtf24.pipeline-status/1',
        'inherited_v23_status':json.loads((OLD/'PIPELINE_STATUS.json').read_text()),
        'v24_root_connection':'actual preparation -> predictive continuation dual -> compatible finite-state implementation -> sharp physical minimum-preparation segment',
        'A2':'independent geometric chain, not claimed as a derived corollary',
        'B4':'historical aggregate obligations retained; not closed here',
        'C2':'bounded physical/transport consumers do not close the historical broad target',
        'all_eleven_papers_closed':False,
    })
    (P/'LITERATURE_CROSSWALK.md').write_text('''# Literature crosswalk, 24 September 2026

## Finite-state testing

Hellman--Cover (1970), Learning with Finite Memory, Annals of Mathematical
Statistics 41:765-782, is the source of the stationary autonomous optimum,
not a result claimed as new here. Their 1971 On Memory Saved by
Randomization, 42:1075-1078, prevents blanket deterministic purification
claims. R. A. Flower--Hellman (1972), IEEE IT18:429-431, and
Cover--Freedman--Hellman (1976), Information and Control 30:49-85, belong
to the finite-time/finite-sample comparison. Metadata were checked at the
author-maintained source:
https://ee.stanford.edu/~hellman/publications.html
The complete original-proof literature comparison is not represented as
finished merely by obtaining this bibliography.

Managoli--Prabhakaran, Memory Constrained Adversarial Hypothesis Testing,
arXiv:2605.12063v1, 12 May 2026, treats time-invariant randomized FSMs and
adaptive choices of report distributions under binary hypotheses. Its
asymptotic minimax error bounds have matching state exponents and match
exactly for a class of problems. The finite reset signed-score task in
this revision has fixed private parameters and different resource cuts.
https://arxiv.org/abs/2605.12063
https://arxiv.org/html/2605.12063v1

## Comparison and algebra

Blackwell comparison, Sion minimax, and positive polynomial bases are
classical ingredients, not claimed as new general principles. The
posterior-predictive formula is proved with its exact reset quantifiers.
Muller--Montufar, arXiv:2110.07409, studies polynomial constraints on
feasible POMDP frequencies; generic polynomial feasibility alone is not
our novelty claim. Putinar (1993) is credited for the strict-positivity
background. The new HS/m certificate uses subdivision and is not a
claimed global SOS-degree bound.

Norberg (2002), Comparison of Statistical Experiments with Filtered
Probability Spaces, Statistics & Risk Modeling 20:1-28,
doi:10.1524/strm.2002.20.14.1, was verified through its publisher record.
The original proof was not obtained through the accessible publisher and
Norwegian library records. No absence-of-overlap or exhaustive priority
claim is made from those records.
https://www.degruyterbrill.com/document/doi/10.1524/strm.2002.20.14.1/html
https://www.nb.no/maken/item/URN%3ANBN%3Ano-nb_digibok_2010022204100

The previous detailed crosswalk is preserved at
history/v23/LITERATURE_CROSSWALK.md.
''')

    env = os.environ.copy()
    env.update(SOURCE_DATE_EPOCH='1790208000',FORCE_SOURCE_DATE='1')
    for i in range(3):
        with (E/f'LATEX_PASS_{i+1}.txt').open('w') as stream:
            run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],
                stdout=stream,stderr=subprocess.STDOUT,env=env)
    log = (P/'main.log').read_text(errors='replace')
    defects = [s for s in ['Overfull \\hbox','Overfull \\vbox','There were undefined references',
                          'multiply defined','LaTeX Warning: Reference','LaTeX Warning: Citation'] if s in log]
    write_json(E/'TYPESETTING_CHECKS.json',{'defects':defects,'passes':3})
    require(not defects,'typesetting defects: '+repr(defects))
    shutil.copyfile(P/'main.pdf',P/'paper.pdf')
    article = fitz.open(P/'paper.pdf')
    labels = {x.group(1):{'number':x.group(2),'page':int(x.group(3))}
              for x in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',(P/'main.aux').read_text())}
    write_json(E/'THEOREM_LOCATIONS.json',labels)
    preservation,volumes = [],{}
    for oldname,newname,expected_pages,title in [
        ('paper.pdf','complete-manuscript.pdf',96,'Complete Mathematical Manuscript'),
        ('complete-development.pdf','complete-development.pdf',649,'Complete Development')]:
        old = fitz.open(OLD/oldname)
        require(len(old)==expected_pages,'predecessor page count')
        merged = fitz.open()
        merged.insert_pdf(article)
        divider = merged.new_page(width=612,height=792)
        divider.insert_text((72,130),'General Theta Foundations I',fontsize=20)
        divider.insert_text((72,168),title,fontsize=17)
        divider.insert_textbox(fitz.Rect(72,220,540,620),
            'Part II: preserved revision 23\n\nThe following '+str(len(old))+
            ' pages reproduce the predecessor volume without alteration.\n\n'
            'Part I contains the new revision 24 proof chain. Earlier theorem '
            'numbers in Part II retain their original meaning. The source '
            'modules, proof qualifications and historical references remain '
            'available in the accompanying repository and source archive.',fontsize=12)
        offset = len(merged)
        merged.insert_pdf(old)
        merged.set_metadata({'title':'General Theta Foundations I v24: '+title,'author':'Qian Qi'})
        merged.set_toc([[1,'Part I: revision 24',1],[1,'Part II: preserved revision 23',offset]])
        output = P/newname
        if output.exists():
            output.unlink()
        merged.save(output,garbage=4,deflate=True)
        merged.close()
        merged = fitz.open(output)
        for i in range(len(old)):
            before,after = old[i],merged[offset+i]
            text_equal = before.get_text() == after.get_text()
            raster_equal = before.get_pixmap(alpha=False).samples == after.get_pixmap(alpha=False).samples
            require(text_equal and raster_equal,'changed predecessor page: '+oldname+'/'+str(i+1))
            preservation.append({'volume':newname,'predecessor_page':i+1,'new_page':offset+i+1,
                                 'text_equal':True,'raster_equal':True})
        volumes[newname] = {'pages':len(merged),'predecessor_pages':len(old),
                            'divider_pages':1,'sha256':sha(output)}
        old.close()
        merged.close()
        print('Preserved '+oldname,flush=True)
    write_json(E/'PRESERVED_PAGES.json',preservation)
    require(all(sha(OLD/name)==digest for name,digest in old_sources.items()),'predecessor changed during build')

    source_files = [f for f in sorted(P.rglob('*')) if f.is_file()
                    and 'evidence' not in f.relative_to(P).parts and '__pycache__' not in f.parts
                    and f.suffix in {'.tex','.py','.md','.json'}]
    source_hashes = {f.relative_to(P).as_posix():sha(f) for f in source_files}
    write_json(E/'SOURCE_HASHES.json',source_hashes)
    receipt = {
       'schema':'gtf24.build-receipt/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-snapshot'),
       'review_commit':REVIEW,'predecessor_commit':PREDECESSOR,
       'workflow_run':os.environ.get('GITHUB_RUN_ID'),
       'article_pages':len(article),'article_sha256':sha(P/'paper.pdf'),
       'complete_volumes':volumes,'preserved_page_comparisons':len(preservation),
       'all_predecessor_pages_text_and_raster_equal':True,
       'unchanged_inherited_math_modules':len(inheritance['unchanged_math_modules']),
       'unchanged_predecessor_source_files':len(old_sources),
       'new_finite_checks':results['v24']['checks'],
       'inherited_finite_checks':sum(v['checks'] for k,v in results.items() if k!='v24'),
       'finite_checks':sum(v['checks'] for v in results.values()),
       'normal_optimized_equal':True,'negative_control_executions':len(negative),
       'typesetting_defects':defects,
       'physical_boundary':'N_c(W,Q)=2 for W>=12 and u1+beta<=c<m2-beta',
       'peak_width_optimality_proved':False,'global_SOS_degree_bound_proved':False,
       'analytic_proofs_independently_verified':False,'all_eleven_papers_closed':False,
       'norberg_original_proof_comparison':'incomplete',
       'old_paths_modified':[],'old_paths_deleted':[],'font_files_distributed':False,
    }
    write_json(E/'BUILD_RECEIPT.json',receipt)
    with zipfile.ZipFile(E/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for f in source_files:
            archive.write(f,P.name+'/'+f.relative_to(P).as_posix())
        for name in sorted(old_sources):
            archive.write(OLD/name,OLD.name+'/'+name)
        for name in ('paper.pdf','complete-development.pdf'):
            archive.write(OLD/name,OLD.name+'/'+name)
    renders = E/'renders'
    renders.mkdir(exist_ok=True)
    selected = {0,len(article)-1}
    for key in ['thm:dual','thm:outer','thm:physical','eq:certificate','eq:poly',
                'lem:profile','thm:quantitative','thm:autonomous','cor:confidence']:
        require(key in labels,'missing theorem location: '+key)
        selected.add(labels[key]['page']-1)
    for i in sorted(selected):
        article[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(renders/f'page-{i+1:03d}.png')
    article.close()
    print(json.dumps(receipt,indent=2,sort_keys=True),flush=True)
    for suffix in ['aux','log','out','toc','pdf']:
        temporary = P/('main.'+suffix)
        if temporary.exists():
            temporary.unlink()

if __name__ == '__main__':
    main()
