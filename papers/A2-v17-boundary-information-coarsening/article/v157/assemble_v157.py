#!/usr/bin/env python3
"""Build three complete v157 review objects from the pinned v155 manuscript."""
from __future__ import annotations
import argparse,collections,hashlib,importlib.util,json,os,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'v155'/'geometry.tex'
PREV_HASH='7169ee083430fab37e6ed353a18a499e38dc6c79cee164d89cb5c50936a98af7'
BASE='54b3a37bb8349fbba089dd0b7cdaa2ba0aa74414'
REVIEW='52ebb8183433ad398f61958219b2af809f721824'
from frontmatter_v157 import BIB,DISCLOSURE,II_TITLE,II_ABSTRACT,II_INTRO,MASTER_ABSTRACT,MASTER_INTRO
# Only reuse the inspected v155 frontmatter, not any v156 encoded source.
spec=importlib.util.spec_from_file_location('predecessor_frontmatter',HERE.parent/'v155'/'assemble_v155.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
I_ABSTRACT=previous.I_ABSTRACT
I_INTRO=previous.I_INTRO+r'''
The companion paper identifies the simultaneous graph of reciprocal
power maps with complete quadrics as a scheme over the native quadratic
coefficient space (Theorem~\ref{thm:power-graph-v157}). Its contact
divisors recover regular-pencil spectral exponents, and its resolved
pencil family carries the finite algebra used here with its multiplication
unchanged (Proposition~\ref{prop:pencil-compactification-v157}). This
boundary interpretation uses the congruence action on the recovered
source, rather than the larger full cotangent-coordinate action.
'''

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def once(t,a,b):
    if t.count(a)!=1:raise ValueError('Nonunique anchor: '+a)
    return t.replace(a,b,1)
def labels(t):return re.findall(r'\\label\{([^}]+)\}',t)
def refs(t):return set(re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',t))
BLOCK=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|definition|example|remark|proof)\}.*?\\end\{\1\}',re.S)
def blocks(t):return collections.Counter(m.group(0) for m in BLOCK.finditer(t))
def compile_one(name,passes=2):
    for i in range(passes):
        with (HERE/f'{name}-build-pass-{i+1}.txt').open('w') as f:
            subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',name+'.tex'],cwd=HERE,stdout=f,stderr=subprocess.STDOUT,check=True)
def aux_labels(name):
    return {m.group(1):(m.group(2),m.group(3)) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}',(HERE/(name+'.aux')).read_text())}
def aliases(needed,other,prefix):
    out=['% Embedded companion-paper references; no external aux file is required.','\\makeatletter']
    for key in sorted(needed):
        if key not in other:raise ValueError('Absent companion reference '+key)
        number,page=other[key]
        out.append(r'\@namedef{r@'+key+'}{{'+prefix+number+'}{'+prefix+page+'}{}{}{}}')
    return '\n'.join(out+['\\makeatother\n'])
def source(preamble,title,abstract,intro,body,tail,cross=''):
    return preamble+cross+'\n\\begin{document}\n\\title{'+title+'}\n\\author{Qian Qi}\n\\date{September 25, 2026}\n\\subjclass[2020]{14M12, 14B05, 14D20, 13C40}\n\\hypersetup{pdftitle={'+title+', revision 157},pdfauthor={Qian Qi}}\n\\begin{abstract}\n'+abstract+'\n\\end{abstract}\n\\maketitle\n'+intro+'\n'+body+'\n'+tail

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
    if sha(PREV)!=PREV_HASH:raise RuntimeError('Locked complete v155 source hash mismatch')
    old=PREV.read_text();start=old.index('\\begin{abstract}');end=old.index('% BEGIN PRESERVED PART')
    (HERE/'PREVIOUS_FRONTMATTER_V155.tex').write_text(old[start:end])
    body=old[end:]
    core=(HERE/'universal-power-ideals-v157.tex').read_text()
    bridge='The preceding relative caution concerns the valuation-ring proof. The following polynomial identity establishes the equality over arbitrary complex base algebras.\n\n'
    body=once(body,'\\section{Descent and complete-local details}',bridge+core+'\n\\section{Descent and complete-local details}')
    body=once(body,'\\end{thebibliography}',BIB+'\n\\end{thebibliography}')
    body=once(body,'\\begin{thebibliography}{99}',DISCLOSURE+'\\begin{thebibliography}{99}')
    master=old[:start].replace('revision 155','revision 157')+'\\begin{abstract}\n'+MASTER_ABSTRACT+'\n\\end{abstract}\n\\maketitle\n'+MASTER_INTRO+'\n'+body
    missing=set(labels(old))-set(labels(master));dups=[k for k,v in collections.Counter(labels(master)).items() if v>1]
    lost=blocks(old)-blocks(master);badrefs=refs(master)-set(labels(master))
    cites={x.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',master) for x in group.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',master))
    if missing or dups or lost or badrefs or cites-bib:
        raise RuntimeError(str({'missing_labels':sorted(missing),'duplicates':dups,'lost_blocks':len(lost),'undefined_refs':sorted(badrefs),'undefined_citations':sorted(cites-bib)}))
    (HERE/'geometry.tex').write_text(master)
    cut=body.index('% BEGIN PRESERVED PART 17-assistance.tex');mathematical=body[:cut];tail=body[cut:]
    mathematical=re.sub(r'\\part\*\{[^}]*\}\s*','',mathematical).replace('\\appendix','')
    starts=list(re.finditer(r'\\section\{([^}]+)\}',mathematical))
    paper_i=[];paper_ii=[];mapping=[];appendix=False
    i_main={'First relations, ungraded isomorphisms, and inverse systems','Intrinsic tensor rulings','Actual factor descent and moving coefficient spaces','An intrinsic coefficient principle','Quadratic relation spaces and intrinsic reconstruction of pencils','The exact infinitesimal order of pencil reconstruction','Coefficient-support orientation and a local algebraic inverse','The intrinsic polarization and a projective moduli completion'}
    for j,m in enumerate(starts):
        title=m.group(1);block=mathematical[m.start():starts[j+1].start() if j+1<len(starts) else len(mathematical)]
        if title=='Detailed reconstruction statements and comparisons':appendix=True
        dest='I' if title in i_main or appendix else 'II'
        if title=='Detailed reconstruction statements and comparisons':paper_i.append('\\appendix\n')
        if dest=='I':paper_i.append(block)
        else:paper_ii.append((title,block))
        mapping.append({'section':title,'paper':dest,'labels':labels(block)})
    # Put the complete reciprocal section and the new global boundary argument first.
    lead=['Quadratic sections of reciprocal normalization fibres','Universal power ideals','The reciprocal power graph and complete quadrics','Boundary contacts and spectral schemes','A projective incidence compactification for pencils','Singularities of the universal power-zero schemes']
    lookup=dict(paper_ii)
    if any(t not in lookup for t in lead):raise RuntimeError('Missing principal section')
    ordered_ii=[lookup[t] for t in lead]+[b for t,b in paper_ii if t not in lead]
    i_body='\n'.join(paper_i);ii_body='\n'.join(ordered_ii)
    if blocks(mathematical)!=blocks(i_body)+blocks(ii_body):raise RuntimeError('Proof partition lost or duplicated a mathematical block')
    preamble=old[:old.index('\\begin{document}')]
    make_i=lambda cross='':source(preamble,'Finite failure schemes and the reconstruction of quadratic pencils',I_ABSTRACT,I_INTRO,i_body,tail,cross)
    make_ii=lambda cross='':source(preamble,II_TITLE,II_ABSTRACT,II_INTRO,ii_body,tail,cross)
    i0,ii0=make_i(),make_ii();external_i=refs(i0)-set(labels(i0));external_ii=refs(ii0)-set(labels(ii0))
    if external_i-set(labels(ii0)) or external_ii-set(labels(i0)):raise RuntimeError('Cross-paper reference not assigned')
    (HERE/'reconstruction.tex').write_text(i0);(HERE/'divisor-geometry.tex').write_text(ii0)
    (HERE/'PAPER_MAP_V157.json').write_text(json.dumps({'papers':{'I':'reconstruction','II':'divisor-geometry'},'section_allocation':mapping,'paper_II_principal_reading_order':lead,'I_external_labels':sorted(external_i),'II_external_labels':sorted(external_ii),'all_body_math_blocks_partitioned_exactly_once':True},indent=2)+'\n')
    preservation={'revision':157,'base_complete_revision_commit':BASE,'controlling_review_commit':REVIEW,'predecessor_sha256':PREV_HASH,'predecessor_labels':len(labels(old)),'current_labels':len(labels(master)),'missing_predecessor_labels':sorted(missing),'duplicate_labels':dups,'predecessor_math_blocks':sum(blocks(old).values()),'current_math_blocks':sum(blocks(master).values()),'all_predecessor_math_blocks_retained_byte_for_byte':not lost,'all_body_math_blocks_partitioned_exactly_once_in_companions':True,'predecessor_source_modified':False,'previous_frontmatter_archived':True}
    (HERE/'NONDELETION_V157.json').write_text(json.dumps(preservation,indent=2)+'\n')
    receipt=dict(preservation,source_commit=os.environ.get('GITHUB_SHA','local-build'),compiled=False,historical_28_checks_rerun=False,Ballico_1993_full_text_comparison_completed=False,general_proofs_certified_by_computation=False,journal_acceptance_asserted=False,v156_undecodable_source_used_as_mathematical_input=False)
    if args.build:
        compile_one('geometry',3);compile_one('reconstruction',2);compile_one('divisor-geometry',2)
        oldmaps=None
        for attempt in range(4):
            imap=aux_labels('reconstruction');iimap=aux_labels('divisor-geometry')
            maps=(aliases(external_i,iimap,'II.'),aliases(external_ii,imap,'I.'))
            (HERE/'reconstruction.tex').write_text(make_i(maps[0]));(HERE/'divisor-geometry.tex').write_text(make_ii(maps[1]))
            compile_one('reconstruction',2);compile_one('divisor-geometry',2)
            if maps==oldmaps:break
            oldmaps=maps
        else:raise RuntimeError('Companion maps did not stabilize')
        outputs={}
        for name in ('geometry','reconstruction','divisor-geometry'):
            log=(HERE/(name+'.log')).read_text(errors='replace')
            bad=[s for s in ('undefined references','There were undefined','multiply defined','Citation `') if s in log]
            overfull=re.findall(r'Overfull \\hbox \(([^)]+)\)',log)
            if bad or overfull:raise RuntimeError(str({'file':name,'bad':bad,'overfull':overfull}))
            subprocess.run(['pdftotext','-layout',name+'.pdf',name+'.txt'],cwd=HERE,check=True)
            info=subprocess.run(['pdfinfo',name+'.pdf'],cwd=HERE,check=True,text=True,capture_output=True).stdout
            outputs[name]={'pages':int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1)),'source_sha256':sha(HERE/(name+'.tex')),'pdf_sha256':sha(HERE/(name+'.pdf')),'pdf_bytes':(HERE/(name+'.pdf')).stat().st_size,'clean_references_and_no_overfull_hboxes':True}
        receipt.update(compiled=True,outputs=outputs,companion_reference_maps_embedded_and_stable=True)
    receipt['input_sha256']={p.name:sha(p) for p in sorted(HERE.glob('*')) if p.name in ('frontmatter_v157.py','universal-power-ideals-v157.tex','assemble_v157.py','check_v157.py')}
    for name in ('EXACT_CHECKS_V157.json','INHERITED_V155_CHECKS_RERUN.json'):
        if (HERE/name).exists():receipt[name+'_sha256']=sha(HERE/name)
    (HERE/'BUILD_RECEIPT_V157.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
