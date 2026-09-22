#!/usr/bin/env python3
"""Reorder unchanged proof blocks, validate preservation, optionally compile.

No mathematical text is inferred or fetched. All input files are committed.
Generated files in build/ relocate complete lemmas and statements, and the
resource model; no proof is abridged. Use --prepare-only without TeX.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parent
EXPECTED={
 '02_experiments.tex':'1bd4f6273d62c860f8a348dcc4f72734dbc388db',
 '03_transversality.tex':'6395724ba2c4bed3ead19178a1cfe8206f9a3824',
 '04_observation_algebra.tex':'c3c127d2370371d45334b9d3ff61f2e9e5e98718',
 '05_confluence.tex':'73eeae176876f515676f4148961cfb09146c9547',
 '06_streaming.tex':'e662f435a3a485542606b759b7a3129f298cd865',
 '06a_attainable_filtration.tex':'fedb4c3421227a6c8060d32d2091a5d65ff9a9a6',
 '06b_collision_geometry.tex':'e0b9ba68173fc2b50f9e9fc30038959484f2ce96',
 '07_uniform_resolution.tex':'03ad17ec736f673c0ad274733fde4092d28333bc',
 '08_sequential_value.tex':'cd811b4398e55953def241cf43383816225f700c',
 '09_common_risk.tex':'3f41b497d5602afc7f9f5bf6aa089a6fe7bf355d',
}

def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def proof_blocks(text):
    return re.findall(r'\\begin\{proof\}.*?\\end\{proof\}',text,re.S)


def take_lemma(text, label):
    for m in re.finditer(r'\\begin\{lemma\}.*?\\end\{lemma\}\s*\\begin\{proof\}.*?\\end\{proof\}',text,re.S):
        if '\\label{'+label+'}' in m.group():
            replacement='The proof of Lemma~\\ref{'+label+'} appears in the principal analytic inputs.'
            return m.group(),text[:m.start()]+replacement+text[m.end():]
    raise ValueError('missing complete lemma '+label)


def expand(path):
    text=path.read_text()
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(ROOT/(m.group(1)+'.tex')),text)


def prepare():
    sources={}
    for name,sha in EXPECTED.items():
        data=(ROOT/'core'/name).read_bytes()
        if blob(data)!=sha: raise ValueError('pinned v9 source mismatch: '+name)
        sources[name]=data.decode()
    out=ROOT/'build';out.mkdir(exist_ok=True)
    confluent,rest5=take_lemma(sources['05_confluence.tex'],'lem:confluent-positive')
    cover,rest6a=take_lemma(sources['06a_attainable_filtration.tex'],'lem:tame-rectangle')
    start=rest6a.index('A bounded semialgebraic format means')
    end=rest6a.index('The proof of Lemma~\\ref{lem:tame-rectangle}')
    format_definition=rest6a[start:end]
    (out/'analytic_inputs.tex').write_text(confluent+'\n\n'+format_definition+cover+'\n')
    (out/'05_confluence.tex').write_text(rest5)
    (out/'06a_attainable_filtration.tex').write_text(rest6a)
    text=sources['06_streaming.tex']
    start=text.index('\\begin{definition}[Finite-state filter]')
    end=text.index('\\begin{lemma}[Uniform finite-horizon transition bounds]')
    (out/'operational_model.tex').write_text('\\subsection{Persistent state and prediction loss}\n'+text[start:end])
    (out/'06_streaming.tex').write_text(text[:start]+'The resource model and loss are defined in Section~\\ref{sec:experiment}.\n\n'+text[end:])
    def take_theorem(text,label):
        for match in re.finditer(r'\\begin\{theorem\}.*?\\end\{theorem\}',text,re.S):
            if '\\label{'+label+'}' in match.group():
                return match.group()
        raise ValueError('missing complete theorem '+label)
    exact=(ROOT/'sections/exact_statements.tex').read_text()
    (out/'main_classification.tex').write_text(take_theorem(exact,'thm:resolution-main')+'\n')
    (out/'exact_information.tex').write_text(
        '\\subsection{Exact information and continuous state dimension}\n'+
        take_theorem(exact,'thm:main')+'\n')
    old_intro=(ROOT/'history/V13_introduction.tex').read_text()
    (out/'effective_overview.tex').write_text(
        '\\subsection{Complete numerical realization statement}\n'+
        'The following collects the intrinsic and effective conclusions. '
        'Its construction and resource bounds are proved in the surrounding '
        'appendices; no stronger numerical converse is implicit.\n'+
        take_theorem(old_intro,'thm:effective-main')+'\n')
    expanded=expand(ROOT/'main.tex')
    inherited=Counter(hashlib.sha256(x.encode()).hexdigest() for text in sources.values() for x in proof_blocks(text))
    current=Counter(hashlib.sha256(x.encode()).hexdigest() for x in proof_blocks(expanded))
    manifest=json.loads((ROOT/'V10_PRESERVATION_MANIFEST.json').read_text())
    v10=Counter(manifest['proof_sha256'])
    if v10-current: raise ValueError('a complete v10 proof is absent or changed')
    if inherited-current: raise ValueError('an inherited complete proof block is absent')
    labels=re.findall(r'\\label\{([^}]+)\}',expanded)
    if len(labels)!=len(set(labels)):raise ValueError('duplicate labels')
    if set(manifest['named_results'])-set(labels):raise ValueError('a v10 named result is absent')
    v11_manifest=json.loads((ROOT/'V11_PRESERVATION_MANIFEST.json').read_text())
    v11=Counter(v11_manifest['proof_sha256'])
    corrections=json.loads((ROOT/'PROOF_CORRECTIONS.json').read_text())['corrections']
    retained=v11.copy()
    for correction in corrections:
        prior=correction['old_proof_sha256']; revised=correction['new_proof_sha256']
        if retained[prior]!=1 or current[revised]!=1:
            raise ValueError('documented proof correction does not match compiled text')
        retained[prior]-=1
    if retained-current:raise ValueError('unapproved change to a v11 proof')
    if set(v11_manifest['named_results'])-set(labels):
        raise ValueError('a v11 named result is absent')

    v12_manifest=json.loads((ROOT/'V12_PRESERVATION_MANIFEST.json').read_text())
    v12=Counter(v12_manifest['proof_sha256'])
    if v12-current:raise ValueError('a complete v12 proof was changed or removed')
    if set(v12_manifest['named_results'])-set(labels):
        raise ValueError('a v12 named result is absent')
    v13_manifest=json.loads((ROOT/'V13_PRESERVATION_MANIFEST.json').read_text())
    v13=Counter(v13_manifest['proof_sha256'])
    if v13-current:raise ValueError('a complete v13 proof was changed or removed')
    if set(v13_manifest['named_results'])-set(labels):
        raise ValueError('a v13 named result is absent')
    statement_pattern=r'\\begin\{(theorem|lemma|proposition|corollary)\}.*?\\end\{\1\}'
    statements=Counter(hashlib.sha256(m.group().encode()).hexdigest()
                       for m in re.finditer(statement_pattern,expanded,re.S))
    v13_statements=Counter(v13_manifest['statement_sha256'])
    if v13_statements-statements:raise ValueError('a complete v13 statement was changed or removed')
    v14_manifest=json.loads((ROOT/'V14_PRESERVATION_MANIFEST.json').read_text())
    v14=Counter(v14_manifest['proof_sha256'])
    v14_statements=Counter(v14_manifest['statement_sha256'])
    if v14-current:raise ValueError('a complete v14 proof was changed or removed')
    if v14_statements-statements:raise ValueError('a complete v14 statement was changed or removed')
    if set(v14_manifest['named_results'])-set(labels):
        raise ValueError('a v14 named result is absent')
    refs=set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}',expanded))
    missing=refs-set(labels)
    if missing:raise ValueError('undefined source references '+str(sorted(missing)))
    old_labels=set(re.findall(r'\\label\{((?:thm|lem|cor|prop):[^}]+)\}', '\n'.join(sources.values())))|{'thm:main','thm:resolution-main'}
    if old_labels-set(labels):raise ValueError('missing predecessor named result')
    report={'retained_v10_proofs':sum(v10.values()),'retained_v10_named_results':len(manifest['named_results']),'pinned_v9_body_files':len(EXPECTED),'retained_named_results':len(old_labels),
            'retained_complete_proof_blocks':sum(inherited.values()),
            'compiled_proof_blocks':sum(current.values()),'all_references_resolved_in_source':True,
            'statement':'Source preservation, not mathematical proof verification.'}
    report.update(retained_v11_proofs_byte_identical=sum(retained.values()),
                  v11_documented_proof_corrections=len(corrections),
                  retained_v11_named_results=len(v11_manifest['named_results']),
                  current_named_results=len(re.findall(r'\\label\{((?:thm|lem|cor|prop):[^}]+)\}',expanded)),
                  no_unapproved_proof_deletions=True,
                  retained_v12_proofs_byte_identical=sum(v12.values()),
                  retained_v12_named_results=len(v12_manifest['named_results']))
    report.update(retained_v13_statements_byte_identical=sum(v13_statements.values()),
                  retained_v13_proofs_byte_identical=sum(v13.values()),
                  retained_v13_named_results=len(v13_manifest['named_results']))
    report.update(retained_v14_statements_byte_identical=sum(v14_statements.values()),
                  retained_v14_proofs_byte_identical=sum(v14.values()),
                  retained_v14_named_results=len(v14_manifest['named_results']))
    (ROOT/'PRESERVATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'expanded.tex').write_text(expanded)
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args();report=prepare()
    if not args.prepare_only:
        for _ in range(3):
            run=subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode',
                                '-halt-on-error','main.tex'],cwd=ROOT,capture_output=True,text=True)
            (ROOT/'build/last-tex-output.txt').write_text(run.stdout+run.stderr)
            if run.returncode:raise RuntimeError('TeX failed; inspect build/last-tex-output.txt')
        log=(ROOT/'main.log').read_text()
        bad=[line for line in log.splitlines() if 'undefined' in line.lower() or 'Overfull' in line]
        if bad:raise RuntimeError('TeX warnings: '+str(bad))
        report['pdflatex_passes']=3;report['undefined_or_overfull_warnings']=0
        (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
