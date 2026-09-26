#!/usr/bin/env python3
"""Materialize complete A2 v167 papers from hash-locked v166, then compile."""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
from frontmatter_v167 import II_ABSTRACT, II_INTRO, I_ADD, BIB
HERE=Path(__file__).resolve().parent
BRANCH='revision/a2-v167-determinantal-hilbert-states-2026-09-26'
REVIEW='d5dd2e67b56c96f0a003e38e720918eba05239ca'
REPORT_BLOB='881415d5ad9e719376a8b3eb14323f0fcb077e94'
REL='papers/A2-v17-boundary-information-coarsening/article/v167'
PINS={
 'geometry':'9d3d15facba0a3e8a8fc3ddd9d84be1530abc23eded2c7051073e5657c12b602',
 'reconstruction':'0521ef82e4f48e3923ea2e5132d95cab3e55a6006bbd7d83db0f20db614b2303',
 'divisor-geometry':'ff1c3465643d14ec914fd01b078ad3eccaeb47d367ff7afc6498a287267c29bd'}
MATH=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|remark|example|definition|proof)\}.*?\\end\{\1\}',re.S)
LABEL=re.compile(r'\\label\{([^}]+)\}')
REF=re.compile(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}')
AUX=re.compile(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}')
SEC=re.compile(r'\\section\{([^}]+)\}')

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok:bool,msg:str)->None:
 if not ok:raise RuntimeError(msg)
def once(s:str,a:str,b:str)->str:
 require(s.count(a)==1,'Missing or nonunique anchor: '+a)
 return s.replace(a,b,1)
def counts(s:str):return collections.Counter(hashlib.sha256(m.group().encode()).hexdigest() for m in MATH.finditer(s))
def strip_embedded(s:str)->str:
 s=re.sub(r'% Embedded companion-paper references;[^\n]*\n\\makeatletter\n.*?\\makeatother\n', '',s,flags=re.S)
 return re.sub(r'% BEGIN V166 COMPANION REFERENCES\n.*?% END V166 COMPANION REFERENCES\n','',s,flags=re.S)
def section_span(s:str,title:str):
 matches=list(SEC.finditer(s))
 for i,m in enumerate(matches):
  if m.group(1)==title:return m.start(),matches[i+1].start() if i+1<len(matches) else s.index('\\begin{thebibliography}')
 raise RuntimeError('Missing section '+title)
def abstract(s:str,text:str)->str:
 pattern=r'(\\begin\{abstract\}\n).*?(\n\\end\{abstract\})'
 out,n=re.subn(pattern,lambda m:m.group(1)+text.strip()+m.group(2),s,count=1,flags=re.S)
 require(n==1,'Abstract missing');return out


def assemble(prev:Path):
 old={}
 for name,pin in PINS.items():
  p=prev/(name+'.tex');require(p.exists() and sha(p)==pin,'Locked predecessor mismatch: '+str(p))
  old[name]=p.read_text()
  matches=list(SEC.finditer(old[name]));end=matches[1].start() if name!='geometry' else matches[0].start()
  (HERE/('PREVIOUS_'+name.upper().replace('-','_')+'_FRONTMATTER_V166.tex')).write_text(old[name][:end])
 templates={n:strip_embedded(s).replace('revision 166}', 'revision 167}',1) for n,s in old.items()}
 mainparts='\n'.join((HERE/n).read_text() for n in ['determinantal-states-v167.tex','two-wall-slice-v167.tex','horizontal-comparison-v167.tex'])
 local=(HERE/'local-algebra-clarifications-v167.tex').read_text()
 effective=(HERE/'effective-states-v167.tex').read_text()
 s=templates['reconstruction']
 s=once(s,'\\label{sec:paper-i-v166}','\\label{sec:paper-i-v166}\\label{sec:paper-i-v167}')
 anchor='\\section{First relations, ungraded isomorphisms, and inverse systems}'
 s=once(s,anchor,I_ADD+'\n'+anchor)
 s=once(s,'\\begin{thebibliography}',effective+'\n\\begin{thebibliography}')
 templates['reconstruction']=s
 s=templates['divisor-geometry'];s=abstract(s,II_ABSTRACT)
 a,b=section_span(s,'Introduction');s=s[:a]+II_INTRO+'\n'+s[b:]
 s=s.replace('Power ideals and the Hilbert boundary of quadratic pencils','Determinantal models and Hilbert limits of quadratic pencils')
 moved=[]
 for title in ['Power coefficients and their twists','Universal power ideals','The reciprocal power graph and complete quadrics']:
  a,b=section_span(s,title);moved.append(s[a:b]);s=s[:a]+s[b:]
 anchor='\\section{Universal horizontal models of the Hilbert boundary}'
 s=once(s,anchor,mainparts+'\n'+anchor)
 app='\\appendix\n\\renewcommand{\\thesection}{\\AlphAlph{\\value{section}}}\n'
 s=once(s,app,app+local+'\n'+'\n'.join(moved)+'\n')
 templates['divisor-geometry']=s
 s=templates['geometry']
 s=once(s,'\\appendix',mainparts+'\n'+effective+'\n\\appendix\n'+local+'\n')
 s=once(s,'\\end{abstract}',
  'The determinantal model for every polynomial contact order, its finite\njet and decorated chamber theorems, and the complete nonsymmetric\ntwo-wall slice are included without removing predecessor proofs.\n\\end{abstract}')
 templates['geometry']=s
 for name,s in templates.items():
  templates[name]=once(s,'\\end{thebibliography}',BIB+'\n\\end{thebibliography}')
 original=counts(old['geometry']);current=counts(templates['geometry'])
 pair=counts(templates['reconstruction'])+counts(templates['divisor-geometry'])
 require(not(original-current),'A predecessor mathematical block changed or disappeared')
 require(current==pair,'Complete paper bodies must partition master exactly once')
 labels=LABEL.findall(templates['geometry']);oldlabels=LABEL.findall(old['geometry'])
 missing=sorted(set(oldlabels)-set(labels));dups=sorted(k for k,v in collections.Counter(labels).items() if v>1)
 require(not missing and not dups,'Master labels missing or duplicated')
 available=set().union(*(set(LABEL.findall(s)) for s in templates.values()))
 for name,s in templates.items():
  require(not(set(REF.findall(s))-available),'Unknown references in '+name+': '+str(set(REF.findall(s))-available))
  own=LABEL.findall(s);require(len(own)==len(set(own)),'Duplicate labels: '+name)
  require(not(counts(old[name])-counts(s)),'Nondeletion failure: '+name)
  (HERE/(name+'.tex')).write_text(s)
 receipt={'revision':167,'controlling_review_commit':REVIEW,'predecessor_sha256':PINS,
 'predecessor_math_blocks':sum(original.values()),'current_math_blocks':sum(current.values()),
 'predecessor_labels':len(oldlabels),'current_labels':len(labels),'missing_labels':missing,'duplicate_labels':dups,
 'all_predecessor_math_blocks_retained_byte_for_byte':True,'body_partitioned_exactly_once':True,
 'all_three_predecessor_frontmatters_archived':True,'historical_manuscript_sources_modified':False,
 'moved_intact_to_appendix':['Power coefficients and their twists','Universal power ideals','The reciprocal power graph and complete quadrics'],
 'external_independent_paper_I_audit_obtained':False}
 (HERE/'NONDELETION_V167.json').write_text(json.dumps(receipt,indent=2)+'\n')
 return templates,receipt
def compile_one(name:str,passes:int=2):
 for k in range(passes):
  run=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',name+'.tex'],cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (HERE/(name+'.build-output.txt')).write_text(run.stdout)
  require(run.returncode==0,'LaTeX failed: '+name+'; see build-output and log')
def read_aux(name:str):return {k:(n,p) for k,n,p in AUX.findall((HERE/(name+'.aux')).read_text())}
def embed(s:str,other:dict,prefix:str):
 own=set(LABEL.findall(s));needed=sorted(set(REF.findall(s))-own)
 require(all(k in other for k in needed),'Missing companion labels: '+str([k for k in needed if k not in other]))
 lines=['% BEGIN V167 COMPANION REFERENCES','\\makeatletter']
 for k in needed:
  n,p=other[k];lines.append('\\@namedef{r@'+k+'}{{'+prefix+'.'+n+'}{'+prefix+'.'+p+'}{}{}{}}')
 lines+=['\\makeatother','% END V167 COMPANION REFERENCES']
 return once(s,'\\begin{document}','\n'.join(lines)+'\n\\begin{document}')

def build(templates):
 for name in ('reconstruction','divisor-geometry'):compile_one(name)
 stable=False
 for iteration in range(6):
  before={n:read_aux(n) for n in ('reconstruction','divisor-geometry')}
  for name,other,prefix in [('reconstruction','divisor-geometry','II'),('divisor-geometry','reconstruction','I')]:
   (HERE/(name+'.tex')).write_text(embed(templates[name],before[other],prefix))
  for name in before:compile_one(name)
  after={n:read_aux(n) for n in before}
  if before==after:stable=True;break
 require(stable,'Companion reference pagination did not stabilize')
 compile_one('geometry',3)
 outputs={};index={}
 for name in templates:
  log=(HERE/(name+'.log')).read_text(errors='replace')
  bad=[x for x in ['There were undefined references','There were multiply-defined labels','Overfull \\hbox','LaTeX Warning: Reference','LaTeX Warning: Citation'] if x in log]
  require(not bad,'Final layout/reference failure in '+name+': '+str(bad))
  info=subprocess.check_output(['pdfinfo',str(HERE/(name+'.pdf'))],text=True)
  pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
  outputs[name]={'pages':pages,'pdf_sha256':sha(HERE/(name+'.pdf')),'tex_sha256':sha(HERE/(name+'.tex')),'clean_references_and_no_overfull_hboxes':True}
  subprocess.run(['pdftotext','-layout',str(HERE/(name+'.pdf')),str(HERE/(name+'.txt'))],check=True)
  aux=read_aux(name)
  for key in LABEL.findall(templates[name]):
   if key not in aux:continue
   num,page=aux[key]
   if name!='geometry':index[key]={'paper':name,'number':num,'page':page}
   elif key in index:index[key]['master_number']=num;index[key]['master_page']=page
 # Add master locations in a separate pass regardless of dictionary order.
 master=read_aux('geometry')
 for key,record in index.items():
  if key in master:record.update(master_number=master[key][0],master_page=master[key][1])
 (HERE/'THEOREM_INDEX_V167.json').write_text(json.dumps(index,indent=2)+'\n')
 render=HERE/'render-audit';render.mkdir(exist_ok=True)
 selected={'reconstruction':{1},'divisor-geometry':{1},'geometry':{1}}
 for key,rec in index.items():
  if key.endswith('v167') and key.startswith(('thm:','prop:')):
   name=rec['paper'];p=int(rec['page']);selected[name].update(range(p,min(p+2,outputs[name]['pages'])+1))
 for name,pages in selected.items():
  for page in sorted(pages):subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1400','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
 return outputs,{n:sorted(p) for n,p in selected.items()}


def publish(root:Path,receipt:dict):
 text='# A2 revision 167 — complete review entry\n\n'
 text+=f'Branch: `{BRANCH}`.\n\nControlling review commit: `{REVIEW}`.\n\nAuthored build commit: `{receipt["source_commit"]}`.\n\n'
 titles={'reconstruction':'Paper I — Finite failure schemes and the reconstruction of quadratic pencils','divisor-geometry':'Paper II — Determinantal models and Hilbert limits of quadratic pencils','geometry':'Complete preservation master (not a third submission)'}
 for n,title in titles.items():
  text+=f'## {title}\n\n{receipt["outputs"][n]["pages"]} pages. [Complete PDF]({REL}/{n}.pdf) · [Complete standalone LaTeX]({REL}/{n}.tex).\n\n'
 text+='''## Mathematical changes

An explicit maximal-minor Rees model for every polynomial contact order;
primitive Hilbert-state specialization and a pointwise finite coefficient-jet bound;
finite decorated chambers for exact monomial coefficient arcs, retaining residue cancellation;
a complete nonsymmetric two-wall model with determinant ideal
`b^10(b,c)^4(b,c^2)^6`, all five embedded limit types, and exceptional geometry;
strict horizontal base change, coherent common refinements, a nonflat counterexample,
and normalization comparison; explicit extension multiplication and ramified class groups.

All 390 predecessor mathematical blocks are retained byte-for-byte. The three
power/reciprocal sections moved to appendices are not deleted. The original
front matters are archived. The master and the two paper bodies partition exactly.

'''
 for n,title in [('RESPONSE_TO_V166_REPORT.md','All 62 referee responses'),('THEOREM_INDEX_V167.json','Compiled theorem and page index'),('THEOREM_DEPENDENCIES_V167.md','Proof dependencies'),('BUILD_RECEIPT_V167.json','Build receipt'),('NONDELETION_V167.json','Proof and label retention'),('EXACT_CHECKS_V167.json','Finite exact checks'),('LITERATURE_AUDIT_V167.md','Source comparison and documentary limits')]:
  text+=f'[{title}]({REL}/{n})\n\n'
 text+='''## Scope that is not represented as completed

The exact monomial family classification is not a component/normalization
classification of every higher-contact parameter fibre. Different generic-polynomial
strata are not glued into an unproved global moduli stack. Higher-corank and
singular-pencil Hilbert boundaries remain separate questions. The effective
failure-family application still uses reconstruction first. No independent external
full audit of Paper I or complete Ballico 1993 comparison was obtained.
Finite checks and compilation do not certify general proofs, originality, or
acceptance at any journal.
'''
 entry=root/'CURRENT_REVIEW_ENTRY.md'
 if entry.exists() and not (HERE/'PREVIOUS_CURRENT_REVIEW_ENTRY_V166.md').exists():
  shutil.copyfile(entry,HERE/'PREVIOUS_CURRENT_REVIEW_ENTRY_V166.md')
 entry.write_text(text)
 (root/'A2_REVISION_V167_INDEX.md').write_text(text)
 readme=root/'README.md'
 if readme.exists() and not (HERE/'PREVIOUS_ROOT_README_V166.md').exists():shutil.copyfile(readme,HERE/'PREVIOUS_ROOT_README_V166.md')
 readme.write_text('# Theta-Theory — A2 revision 167\n\nThis isolated revision branch contains the complete v167 manuscripts prepared against the locked v166 referee report.\n\n[Current review entry](CURRENT_REVIEW_ENTRY.md) gives both complete papers, their PDFs, the preservation master, all 62 responses, and verification receipts.\n\nThe previous README is retained in '+REL+'/PREVIOUS_ROOT_README_V166.md. Historical manuscript and review sources are unchanged.\n')

 (HERE/'CURRENT_REVIEW_ENTRY.md').write_text(text.replace(REL+'/', ''))

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--build',action='store_true')
 ap.add_argument('--baseline',type=Path,default=HERE.parent/'v166')
 ap.add_argument('--root',type=Path,default=(HERE.parents[3] if len(HERE.parents)>3 else HERE.parent/'local-audit-root'))
 ap.add_argument('--local-audit',action='store_true',help='Allow absence of the report bytes only for local prepublication compilation.')
 args=ap.parse_args();args.root.mkdir(parents=True,exist_ok=True)
 report=args.root/'reviews/a2-v166-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md'
 validated=False
 if report.exists():
  data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  require(blob==REPORT_BLOB,'Wrong controlling report')
  (HERE/'CONTROLLING_REFEREE_REPORT_V166.md').write_bytes(data);validated=True
 else:require(args.local_audit and not os.environ.get('GITHUB_ACTIONS'),'Controlling report bytes required for remote publication')
 response=(HERE/'RESPONSE_TO_V166_REPORT.md').read_text()
 require(list(map(int,re.findall(r'^### (\d+)\.',response,re.M)))==list(range(1,63)),'All 62 response items required')
 templates,receipt=assemble(args.baseline)
 receipt.update(source_commit=os.environ.get('GITHUB_SHA','local-prepublication-audit'),controlling_report_blob=REPORT_BLOB,controlling_report_bytes_validated=validated,compiled=False)
 if args.build:
  outputs,rendered=build(templates)
  receipt.update(compiled=True,outputs=outputs,rendered_pages=rendered,companion_references_stabilized=True)
  checks=json.loads((HERE/'EXACT_CHECKS_V167.json').read_text());require(checks['all_checks_pass'],'Exact checks required')
  receipt['inherited_v166_full_chain_rerun']=checks['inherited_v166_full_chain_rerun']
  publish(args.root,receipt)
 manifest={p.name:sha(p) for p in HERE.iterdir() if p.suffix in ('.py','.tex','.md') and not p.name.startswith(('PREVIOUS_','geometry','reconstruction','divisor-geometry','CURRENT_REVIEW_ENTRY'))}
 (HERE/'SOURCE_MANIFEST_V167.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (HERE/'BUILD_RECEIPT_V167.json').write_text(json.dumps(receipt,indent=2)+'\n')
 for name,pin in PINS.items():require(sha(args.baseline/(name+'.tex'))==pin,'Historical source changed')
 print(json.dumps({'compiled':receipt['compiled'],'retained_blocks':receipt['predecessor_math_blocks'],'outputs':receipt.get('outputs',{})},indent=2))
if __name__=='__main__':main()
