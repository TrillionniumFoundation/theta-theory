#!/usr/bin/env python3
"""Build the v24 main article and complete companions; audit preservation.

Checks below establish source identity, routing and successful compilation.
They are not formal verification of the mathematical arguments.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'build'
FORMAL=('theorem','lemma','proposition','corollary')
REVIEW='78e948fe03a3969fde4c96411ae1fee5915cb908'
BASE='e7c1111d0ab8fb39e4b213902186db2cdf6d0dea'
MANIFEST='c740764bb7ef5e55ce3308cfc57456cf30d95d81'
REPORT_BLOB='70ff9f7fbf7b3845e0b45d8d6ff55c9ac21521e5'

def sha(data: bytes)->str: return hashlib.sha256(data).hexdigest()
def git_blob(data: bytes)->str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def expand(path:Path,stack:tuple[Path,...]=())->str:
    path=path.resolve()
    if not path.is_relative_to(ROOT) or path in stack:
        raise ValueError('Escaping or cyclic TeX input: '+str(path))
    return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(ROOT/(m[1]+'.tex'),stack+(path,)),path.read_text())
def blocks(text:str,envs:tuple[str,...])->Counter:
    pat=r'\\begin\{('+ '|'.join(envs) +r')\}.*?\\end\{\1\}'
    return Counter(sha(m[0].encode()) for m in re.finditer(pat,text,re.S))
def labels(text:str)->list[str]:return re.findall(r'\\label\{([^}]+)\}',text)
def refs(text:str)->set[str]:return set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}',text))
def cites(text:str)->set[str]:
    return {x.strip() for m in re.finditer(r'\\cite(?:\[[^]]*\])*\{([^}]+)\}',text) for x in m[1].split(',')}
def verify_history()->dict:
    H=ROOT/'history/v23-source'
    old_bytes=(ROOT/'history/v22-source-manifest.json').read_bytes()
    if git_blob(old_bytes)!='a2fea657ca31b1e824cff9393f02c4aa78c2ad54':
        raise ValueError('Pinned v22 manifest mismatch')
    files=json.loads(old_bytes)['files']
    data=(H/'SOURCE_MANIFEST.json').read_bytes()
    if git_blob(data)!=MANIFEST:raise ValueError('Pinned v23 manifest mismatch')
    delta=json.loads(data)
    if delta['removed']:raise ValueError('Unexpected v23 source removals')
    files.update(delta['files'])
    for name,digest in files.items():
        if sha((H/name).read_bytes())!=digest:raise ValueError('Historical source mismatch: '+name)
    if git_blob((ROOT/'review-basis/REFEREE_REPORT.md').read_bytes())!=REPORT_BLOB:
        raise ValueError('Controlling report mismatch')
    if sha((ROOT/'history/v23-expanded.tex').read_bytes())!='dd1c2a35fcdcd132d31eef01dfe5c326d0ffaf9bae05b229f25f37114aadba12':
        raise ValueError('Expanded baseline mismatch')
    return {'submission_commit':BASE,'review_commit':REVIEW,
            'v23_manifest_git_blob':MANIFEST,'review_report_git_blob':REPORT_BLOB,
            'verified_manifest_covered_v23_source_files':len(files)}
def write_bibliographies()->None:
    # Flatten only known bibliography wrappers. Original source remains in history.
    text=expand(ROOT/'references-v23.tex')
    keep=[]
    for line in text.splitlines():
        s=line.strip()
        if not s or s.startswith('%'):continue
        if s.startswith(('\\begingroup','\\endgroup','\\let','\\renewcommand{\\endthebibliography}',
                         '\\begin{thebibliography}','\\end{thebibliography}','\\enlargethispage')):continue
        if re.fullmatch(r'\\[A-Za-z]+EndBibliography\}',s):continue
        keep.append(line)
    text='\n'.join(keep)+'\n'
    starts=list(re.finditer(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    entries={}
    for i,m in enumerate(starts):
        if m[1] in entries:raise ValueError('Duplicate bibliography key '+m[1])
        entries[m[1]]=text[m.start():starts[i+1].start() if i+1<len(starts) else len(text)].strip()
    for doc in ('main','companions'):
        # Bootstrap the bibliography file for recursive expansion on a clean tree.
        dest=ROOT/f'references-{doc}.tex'
        dest.touch(exist_ok=True)
        needed=cites(expand(ROOT/f'{doc}.tex'))
        if needed-entries.keys():raise ValueError('Missing bibliography: '+str(needed-entries.keys()))
        selected=entries.keys() if doc=='companions' else needed
        ordered=sorted(selected,key=lambda k:re.sub(r'\\[A-Za-z]+|[{}\\\s]','',entries[k].split('\n',1)[1]).lower())
        dest.write_text('\\begin{thebibliography}{99}\n'+ '\n\n'.join(entries[k] for k in ordered)+'\n\\end{thebibliography}\n')
def prepare()->dict:
    OUT.mkdir(exist_ok=True)
    hist=verify_history()
    write_bibliographies()
    text={doc:expand(ROOT/f'{doc}.tex') for doc in ('main','companions')}
    old=(ROOT/'history/v23-expanded.tex').read_text()
    union='\n'.join(text.values())
    bp=blocks(old,('proof',));bs=blocks(old,FORMAL)
    if (sum(bs.values()),sum(bp.values()))!=(130,129):raise ValueError('Baseline formal blocks changed')
    ns=blocks(union,FORMAL);np=blocks(union,('proof',))
    # One recorded navigation sentence changed after moving the Leja proof.
    edits=json.loads((ROOT/'EDITORIAL_PROOF_EDITS.json').read_text())
    normalized=union
    for edit in edits:
        new_blocks=[m[0] for m in re.finditer(r'\\begin\{proof\}.*?\\end\{proof\}',normalized,re.S)
                    if sha(m[0].encode())==edit['new_proof_sha256']]
        if len(new_blocks)!=1:raise ValueError('Editorial proof edit not unique')
        before=new_blocks[0].replace(edit['new_phrase'],edit['old_phrase'])
        if sha(before.encode())!=edit['old_proof_sha256']:raise ValueError('Unrecorded proof edit')
        normalized=normalized.replace(new_blocks[0],before,1)
    normalized_proofs=blocks(normalized,('proof',))
    if bs-ns or bp-normalized_proofs:raise ValueError('Inherited statement or proof missing/changed')
    oldothers=blocks(old,('definition','remark'))
    if oldothers-blocks(union,('definition','remark')):raise ValueError('Inherited definition/remark missing')
    oldlabels=set(labels(old));all_labels=labels(union)
    dup={k:v for k,v in Counter(all_labels).items() if v>1}
    missing=refs(union)-set(all_labels)
    dropped=oldlabels-set(all_labels)
    if dup or missing or dropped:raise ValueError(f'Label audit: duplicate={dup}, missing={sorted(missing)}, dropped={sorted(dropped)}')
    for doc,t in text.items():
        bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',t))
        if cites(t)-bib:raise ValueError('Unresolved citations '+doc)
        (OUT/f'{doc}-expanded.tex').write_text(t)
    cross={doc:sorted(refs(t)-set(labels(t))) for doc,t in text.items()}
    # Record cross-volume references occurring inside main proofs for human review.
    proof_cross=[]
    for m in re.finditer(r'\\begin\{proof\}.*?\\end\{proof\}',text['main'],re.S):
        ext=refs(m[0])-set(labels(text['main']))
        if ext:proof_cross.append({'proof_sha256':sha(m[0].encode()),'external_labels':sorted(ext)})
    allowed={'sec:common-risk'} # Explicit non-premise about a separate mechanical realization.
    if {x for p in proof_cross for x in p['external_labels']}-allowed:
        raise ValueError('Unexpected external proof dependence in main article')
    report={'version':24,'source_identity':hist,
        'v23_formal_statements_preserved_byte_identical':sum(bs.values()),
        'v23_proof_blocks_preserved_complete':sum(bp.values()),
        'v23_proof_blocks_preserved_byte_identical':sum((bp & np).values()),
        'navigation_only_proof_edits':edits,
        'v23_definitions_and_remarks_preserved_byte_identical':sum(oldothers.values()),
        'v23_labels_preserved':len(oldlabels),
        'compiled_statement_blocks':sum(ns.values()),'compiled_proof_blocks':sum(np.values()),
        'new_statement_blocks':sum((ns-bs).values()),'new_proof_blocks':sum((normalized_proofs-bp).values()),
        'formal_block_multiplicities_preserved':all(ns[k]==v for k,v in bs.items()) and all(normalized_proofs[k]==v for k,v in bp.items()),
        'volumes':{doc:{'statement_blocks':sum(blocks(t,FORMAL).values()),'proof_blocks':sum(blocks(t,('proof',)).values()),
                       'labels':len(labels(t)),'cross_volume_references':cross[doc]} for doc,t in text.items()},
        'main_proof_external_references':proof_cross,
        'main_external_proof_reference_assessment':'Only sec:common-risk: explicit separate mechanical non-claim in the realization proof; not a premise of the collision classification.',
        'unresolved_source_labels_or_citations':0,
        'preservation_scope':'Every inherited formal statement, complete proof, definition and remark remains active in exactly one of the two volumes. One proof has a recorded navigation-only sentence edit; all 772 manifest-covered historical source files are separately preserved. Source checks do not certify theorem correctness.'}
    if not report['formal_block_multiplicities_preserved']:raise ValueError('Inherited formal blocks duplicated')
    (ROOT/'PRESERVATION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def external_aux(doc:str)->None:
    """Export labels only. Prefix displayed main numbers with M, not keys."""
    source=ROOT/f'{doc}.aux'
    if not source.exists():return
    result=[]
    allowed=set(labels(expand(ROOT/f'{doc}.tex')))
    for line in source.read_text().splitlines():
        found=re.match(r'\\newlabel\{([^}]+)\}',line)
        if not found or found[1] not in allowed:continue
        if doc=='main':
            line=re.sub(r'^(\\newlabel\{[^}]+\}\{\{)([^}]+)(\})',lambda m:m[1]+'M.'+m[2]+m[3],line)
        result.append(line)
    (ROOT/f'{doc}-external.aux').write_text('\n'.join(result)+'\n')

def build()->dict:
    report=prepare()
    for doc in ('main','companions'):
        for suffix in ('.pdf','.aux','.out','-external.aux'):
            (ROOT/(doc+suffix)).unlink(missing_ok=True)
    # Five alternating passes: external labels, anchors and page numbers settle.
    for n in range(1,6):
        for doc in ('main','companions'):
            proc=subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',doc+'.tex'],
                cwd=ROOT,capture_output=True,text=True,timeout=180)
            (OUT/f'{doc}-pass-{n}.txt').write_text(proc.stdout+proc.stderr)
            if proc.returncode:raise RuntimeError(f'pdflatex failed: {doc}, pass {n}; see build log')
            external_aux(doc)
    for doc in ('main','companions'):
        log=(ROOT/f'{doc}.log').read_text(errors='replace')
        bad=[x for x in log.splitlines() if any(y in x.lower() for y in ('undefined','multiply defined','overfull','rerun to get','label(s) may have changed'))]
        if bad:raise RuntimeError(doc+' compilation warnings: '+repr(bad))
        result=subprocess.run(['pdfinfo',str(ROOT/f'{doc}.pdf')],capture_output=True,text=True,check=True)
        pages=int(next(x.split(':',1)[1] for x in result.stdout.splitlines() if x.startswith('Pages:')))
        report['volumes'][doc].update(pages=pages,pdf_sha256=sha((ROOT/f'{doc}.pdf').read_bytes()),
                                     tex_passes=5,undefined_duplicate_overfull_or_unsettled_warnings=0)
    report['build_executed']=True
    report['scope']='Executed source/LaTeX checks and builds, not independent peer review or a formal proof certificate.'
    (ROOT/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args()
    print(json.dumps(prepare() if args.prepare_only else build(),indent=2))
if __name__=='__main__':main()
