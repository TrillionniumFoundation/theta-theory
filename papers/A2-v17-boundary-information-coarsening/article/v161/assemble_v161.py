#!/usr/bin/env python3
"""Assemble complete v161 manuscripts; preserve every v160 mathematical block.

The v158 helper functions supply compilation and embedded reference maps.
The mathematical input is the complete, byte-locked v160 master, not a
regenerated or encoded intermediate manuscript. No predecessor is modified.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
helper=HERE.parent/'v158'/'assemble_v158.py'
code=helper.read_text().split('def main():',1)[0]
code=code.replace('from frontmatter_v158 import','from frontmatter_v161 import')
code=code.replace('revision 158},pdfauthor','revision 161},pdfauthor')
exec(compile(code,str(helper),'exec'))
PREV=HERE.parent/'v160'/'geometry.tex'
PREV_HASH='ebe53861e6313880a01b8bda8e80930f209c1b20c7c9ed1e6b78b52cffa27d73'
REVIEW='596df442f9155c79b6b33378c0a208259385b2ae'
BASE='58c33453bf01d1f73083cb744d0479ecdc3dcf2f'
INPUTS=('multiple-incidence-v161.tex','higher-contact-v161.tex','effective-boundary-v161.tex')
I_CORE=['First relations, ungraded isomorphisms, and inverse systems','Intrinsic tensor rulings','Actual factor descent and moving coefficient spaces','An intrinsic coefficient principle','Quadratic relation spaces and intrinsic reconstruction of pencils','The exact infinitesimal order of pencil reconstruction','Coefficient-support orientation and a local algebraic inverse']
I_APPS=['The intrinsic polarization and a projective moduli completion','The intrinsic source and its apolar envelope','Universal property of the intrinsic envelope','The incidence centre from failure multiplication','Effective boundary groupoids and relative lifting obstructions']
II_CORE=['Power coefficients and their twists','Quadratic sections of reciprocal normalization fibres','Universal power ideals','The reciprocal power graph and complete quadrics','Multiple reduced incidence and its complete Hilbert boundary','Higher contact, thick tails, and singular multiplication graphs']
II_APPS=['Power graphs of every rank','Contacts and minimal indices of arbitrary pencils','Boundary contacts and spectral schemes','A projective incidence compactification for pencils','The simple corank-two incidence modification','A computed boundary of the pencil incidence space','Ordinary collision strata and their Hilbert fibres','Singularities of the universal power-zero schemes']
def write_json(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true');args=ap.parse_args()
    if sha(PREV)!=PREV_HASH:raise RuntimeError('Complete v160 source hash mismatch')
    old=PREV.read_text();start=old.index('\\begin{abstract}');end=old.index('% BEGIN PRESERVED PART')
    (HERE/'PREVIOUS_MASTER_FRONTMATTER_V160.tex').write_text(old[start:end])
    for name in ('reconstruction','divisor-geometry'):
        t=(PREV.parent/(name+'.tex')).read_text();a=t.index('\\begin{abstract}')
        b=t.index('\\section{'+('First relations' if name=='reconstruction' else 'Power coefficients'))
        (HERE/('PREVIOUS_'+name.upper().replace('-','_')+'_FRONTMATTER_V160.tex')).write_text(t[a:b])
    body=old[end:];core='\n'.join((HERE/n).read_text() for n in INPUTS)
    body=once(body,'\\section{Descent and complete-local details}',core+'\n\\section{Descent and complete-local details}')
    body=once(body,'\\end{thebibliography}',BIB+'\n\\end{thebibliography}')
    master=old[:start].replace('revision 160','revision 161')+'\\begin{abstract}\n'+MASTER_ABSTRACT+'\n\\end{abstract}\n\\maketitle\n'+MASTER_INTRO+'\n'+body
    missing=set(labels(old))-set(labels(master));dups=[k for k,v in collections.Counter(labels(master)).items() if v>1]
    lost=blocks(old)-blocks(master);badrefs=refs(master)-set(labels(master))
    cites={x.strip() for g in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',master) for x in g.split(',')}
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',master))
    if missing or dups or lost or badrefs or cites-bib:
        raise RuntimeError(str(dict(missing=sorted(missing),duplicates=dups,lost_blocks=len(lost),undefined_refs=sorted(badrefs),undefined_citations=sorted(cites-bib))))
    (HERE/'geometry.tex').write_text(master)
    cut=body.index('% BEGIN PRESERVED PART 17-assistance.tex');mathematical=body[:cut];tail=body[cut:]
    mathematical=re.sub(r'\\part\*\{[^}]*\}\s*','',mathematical).replace('\\appendix','')
    starts=list(re.finditer(r'\\section\{([^}]+)\}',mathematical));parts={};ordered=[];old_i_appendices=[];is_i_appendix=False
    for j,m in enumerate(starts):
        title=m.group(1)
        if title in parts:raise RuntimeError('Duplicate section title '+title)
        parts[title]=mathematical[m.start():starts[j+1].start() if j+1<len(starts) else len(mathematical)]
        ordered.append(title)
        if title=='Detailed reconstruction statements and comparisons':is_i_appendix=True
        if is_i_appendix:old_i_appendices.append(title)
    i_names=I_CORE+I_APPS+old_i_appendices
    ii_names=II_CORE+II_APPS+[t for t in ordered if t not in i_names and t not in II_CORE+II_APPS]
    if set(i_names)&set(ii_names) or set(i_names+ii_names)!=set(parts):raise RuntimeError('Invalid manuscript partition')
    i_body='\n'.join(parts[t] for t in I_CORE)+'\n\\appendix\n'+'\n'.join(parts[t] for t in I_APPS+old_i_appendices)
    ii_body='\n'.join(parts[t] for t in II_CORE)+'\n\\appendix\n'+'\n'.join(parts[t] for t in ii_names[len(II_CORE):])
    if blocks(mathematical)!=blocks(i_body)+blocks(ii_body):raise RuntimeError('Math block partition failure')
    preamble=old[:old.index('\\begin{document}')]
    make_i=lambda cross='':source(preamble,'Finite failure schemes and the reconstruction of quadratic pencils',I_ABSTRACT,I_INTRO,i_body,tail,cross)
    make_ii=lambda cross='':source(preamble,II_TITLE,II_ABSTRACT,II_INTRO,ii_body,tail,cross)
    i0,ii0=make_i(),make_ii();external_i=refs(i0)-set(labels(i0));external_ii=refs(ii0)-set(labels(ii0))
    if external_i-set(labels(ii0)) or external_ii-set(labels(i0)):raise RuntimeError('Unassigned cross-paper reference')
    (HERE/'reconstruction.tex').write_text(i0);(HERE/'divisor-geometry.tex').write_text(ii0)
    write_json('PAPER_MAP_V161.json',dict(I_main=I_CORE,I_appendices=I_APPS+old_i_appendices,II_main=II_CORE,II_appendices=ii_names[len(II_CORE):],all_body_blocks_partitioned_exactly_once=True,section_labels={t:labels(parts[t]) for t in ordered}))
    preservation=dict(revision=161,controlling_review_commit=REVIEW,complete_predecessor_commit=BASE,predecessor_sha256=PREV_HASH,predecessor_labels=len(labels(old)),current_labels=len(labels(master)),predecessor_math_blocks=sum(blocks(old).values()),current_math_blocks=sum(blocks(master).values()),missing_labels=sorted(missing),duplicate_labels=dups,all_predecessor_math_blocks_retained_byte_for_byte=not lost,body_partitioned_exactly_once=True,predecessor_source_modified=False,all_three_previous_frontmatters_archived=True)
    write_json('NONDELETION_V161.json',preservation)
    receipt=dict(preservation,source_commit=os.environ.get('GITHUB_SHA','local-build'),compiled=False,general_proofs_certified_by_computation=False,Ballico_1993_full_text_comparison_completed=False,journal_acceptance_asserted=False)
    if args.build:
        compile_one('geometry',3);compile_one('reconstruction',2);compile_one('divisor-geometry',2)
        oldmaps=None
        for attempt in range(5):
            maps=(aliases(external_i,aux_labels('divisor-geometry'),'II.'),aliases(external_ii,aux_labels('reconstruction'),'I.'))
            (HERE/'reconstruction.tex').write_text(make_i(maps[0]));(HERE/'divisor-geometry.tex').write_text(make_ii(maps[1]))
            compile_one('reconstruction',2);compile_one('divisor-geometry',2)
            if maps==oldmaps:break
            oldmaps=maps
        else:raise RuntimeError('Companion references did not stabilize')
        outputs={};index={}
        for name in ('geometry','reconstruction','divisor-geometry'):
            log=(HERE/(name+'.log')).read_text(errors='replace')
            bad=[s for s in ('undefined references','There were undefined','multiply defined','Citation `') if s in log]
            overfull=re.findall(r'Overfull \\hbox \(([^)]+)\)',log)
            if bad or overfull:raise RuntimeError(str(dict(file=name,bad=bad,overfull=overfull)))
            subprocess.run(['pdftotext','-layout',name+'.pdf',name+'.txt'],cwd=HERE,check=True)
            info=subprocess.check_output(['pdfinfo',name+'.pdf'],cwd=HERE,text=True)
            outputs[name]=dict(pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1)),source_sha256=sha(HERE/(name+'.tex')),pdf_sha256=sha(HERE/(name+'.pdf')),pdf_bytes=(HERE/(name+'.pdf')).stat().st_size,clean_references_and_no_overfull_hboxes=True)
            if name!='geometry':
                for label,(num,page) in aux_labels(name).items():
                    if label.endswith('v161') and not num.startswith(('I.','II.')):
                        index[label]=dict(paper=name,number=num,page=page)
        receipt.update(compiled=True,outputs=outputs,companion_reference_maps_embedded_and_stable=True)
        write_json('THEOREM_INDEX_V161.json',index)
    receipt['input_sha256']={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.name in INPUTS+('frontmatter_v161.py','assemble_v161.py','check_v161.py')}
    receipt['helper_sha256']=sha(helper)
    for n in ('EXACT_CHECKS_V161.json','INHERITED_V160_CHECKS_RERUN.json'):
        if (HERE/n).exists():receipt[n+'_sha256']=sha(HERE/n)
    write_json('BUILD_RECEIPT_V161.json',receipt)
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
