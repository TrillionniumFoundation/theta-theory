#!/usr/bin/env python3
"""Assemble and compile a full, hash-locked, source-preserving A2 v169 revision."""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
from frontmatter_v169 import TITLE, II_ABSTRACT, II_INTRO, I_ADD, BIB
HERE=Path(__file__).resolve().parent
BRANCH='revision/a2-v169-content-free-higher-contact-2026-09-26'
REVIEW='f50f6a7b194adbb42813988d3e68a43d71ccc520'
REPORT_BLOB='f84656b9a3b0a6be81b844b21b73efafe08c6d8a'
FIRST_REVIEW='be1987dd1a37064c0bea291d7ad38ccd12cc5951'
FIRST_BLOB='b0523d8e6b294379de5a2679c116528063efc014'
REL='papers/A2-v17-boundary-information-coarsening/article/v169'
PINS={
 'geometry':'4bff129ce5ab084d70b1415c6ee3875077c1fb5c850e495a302171392573ddf7',
 'reconstruction':'789dff907fe15b9005be77766a77c126ea62fdb341e83aa3c54b66a6f9e821df',
 'divisor-geometry':'0f02b5d1bebc60e24e09cb1e901d3576e8ce247352dd4e71a60d68d17a668434'}
PARTS=['primitive-content-v169.tex','all-order-contact-model-v169.tex','embedded-contact-limits-v169.tex','equivariant-comparison-v169.tex']
MATH=re.compile(r'\\begin\{(theorem|lemma|proposition|corollary|remark|example|definition|proof)\}.*?\\end\{\1\}',re.S)
LABEL=re.compile(r'\\label\{([^}]+)\}')
REF=re.compile(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}')
AUX=re.compile(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}')
SEC=re.compile(r'\\section\{([^}]+)\}')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def once(s,a,b):
 require(s.count(a)==1,'Missing or nonunique anchor: '+a)
 return s.replace(a,b,1)
def counts(s):return collections.Counter(hashlib.sha256(m.group().encode()).hexdigest() for m in MATH.finditer(s))
def strip_embedded(s):
 return re.sub(r'% BEGIN V\d+ COMPANION REFERENCES\n.*?% END V\d+ COMPANION REFERENCES\n','',s,flags=re.S)
def abstract(s,text):
 out,n=re.subn(r'(\\begin\{abstract\}\n).*?(\n\\end\{abstract\})',lambda m:m.group(1)+text.strip()+m.group(2),s,count=1,flags=re.S)
 require(n==1,'Abstract missing');return out

def assemble(prev):
 old={};templates={}
 for name,pin in PINS.items():
  source=prev/(name+'.tex');require(source.exists() and sha(source)==pin,'Wrong complete predecessor: '+name)
  old[name]=source.read_text()
  sections=list(SEC.finditer(old[name]));end=sections[1].start() if name!='geometry' else sections[0].start()
  (HERE/('PREVIOUS_'+name.upper().replace('-','_')+'_FRONTMATTER_V167.tex')).write_text(old[name][:end])
  templates[name]=strip_embedded(old[name]).replace('revision 167}', 'revision 169}',1)
 newparts='\n'.join((HERE/n).read_text() for n in PARTS)
 s=templates['reconstruction']
 s=once(s,'\\section{First relations, ungraded isomorphisms, and inverse systems}',I_ADD+'\n\\section{First relations, ungraded isomorphisms, and inverse systems}')
 templates['reconstruction']=s
 s=templates['divisor-geometry']
 s=abstract(s,II_ABSTRACT)
 sections=list(SEC.finditer(s));require(sections[0].group(1)=='Introduction','Introduction anchor')
 s=s[:sections[0].start()]+II_INTRO+'\n'+s[sections[1].start():]
 s=s.replace('Determinantal models and Hilbert limits of quadratic pencils',TITLE)
 app='\\appendix\n\\renewcommand{\\thesection}{\\AlphAlph{\\value{section}}}\n'
 s=once(s,app,'')
 s=once(s,'\\section{A determinantal model for every contact order}',newparts+'\n'+app+'\n\\section{A determinantal model for every contact order}')
 templates['divisor-geometry']=s
 s=templates['geometry']
 s=once(s,'\\appendix',newparts+'\n\\appendix')
 s=once(s,'\\end{abstract}','The all-order marked-contact chain, its normal Rees algebra,\npunctual genus-correction rings, and fixed-degree equivariant gluing\nare also included in full.\n\\end{abstract}')
 templates['geometry']=s
 disclosure=r"""
\paragraph{Revision 169.}
AI assistance was used in deriving and drafting the all-order row
factorization, monic chart equations, associated-point and genus-correction
calculations, equivariant chart gluing, Quot comparison, and finite exact
checks. The written arguments are offered for independent mathematical
scrutiny. No external independent audit of the sharp inverse, formal
proof-assistant certification, or journal endorsement is represented as
completed by this revision.
"""
 for name,s in templates.items():
  s=once(s,'\\begin{thebibliography}',disclosure+'\n\\begin{thebibliography}')
  templates[name]=once(s,'\\end{thebibliography}',BIB+'\n\\end{thebibliography}')
 original=counts(old['geometry']);current=counts(templates['geometry'])
 pair=counts(templates['reconstruction'])+counts(templates['divisor-geometry'])
 require(not(original-current),'A predecessor mathematical block changed or disappeared')
 require(current==pair,'Paper bodies do not partition the master exactly')
 labels=LABEL.findall(templates['geometry']);oldlabels=LABEL.findall(old['geometry'])
 missing=sorted(set(oldlabels)-set(labels));dups=sorted(k for k,v in collections.Counter(labels).items() if v>1)
 require(not missing and not dups,'Missing/duplicate master labels')
 available=set().union(*(set(LABEL.findall(s)) for s in templates.values()))
 for name,s in templates.items():
  require(not(set(REF.findall(s))-available),'Unknown references: '+str(set(REF.findall(s))-available))
  own=LABEL.findall(s);require(len(own)==len(set(own)),'Duplicate labels '+name)
  require(not(counts(old[name])-counts(s)),'Per-paper nondeletion failure '+name)
  (HERE/(name+'.tex')).write_text(s)
 receipt={'revision':169,'controlling_review_commit':REVIEW,'earlier_review_commit':FIRST_REVIEW,
 'predecessor_sha256':PINS,'predecessor_math_blocks':sum(original.values()),'current_math_blocks':sum(current.values()),
 'predecessor_labels':len(oldlabels),'current_labels':len(labels),'missing_labels':missing,'duplicate_labels':dups,
 'all_predecessor_math_blocks_retained_byte_for_byte':True,'body_partitioned_exactly_once':True,
 'all_three_predecessor_frontmatters_archived':True,'historical_manuscript_sources_modified':False,
 'former_paper_II_main_sections_moved_intact_to_appendices':True,'external_independent_paper_I_audit_obtained':False}
 require(receipt['predecessor_math_blocks']==423 and receipt['predecessor_labels']==625,'Wrong predecessor counts')
 (HERE/'NONDELETION_V169.json').write_text(json.dumps(receipt,indent=2)+'\n')
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
 lines=['% BEGIN V169 COMPANION REFERENCES','\\makeatletter']
 for k in needed:
  n,p=other[k];lines.append('\\@namedef{r@'+k+'}{{'+prefix+'.'+n+'}{'+prefix+'.'+p+'}{}{}{}}')
 lines+=['\\makeatother','% END V169 COMPANION REFERENCES']
 return once(s,'\\begin{document}','\n'.join(lines)+'\n\\begin{document}')

def build(templates):
 for name in templates:
  for suffix in ('.aux','.out','.toc'):
   (HERE/(name+suffix)).unlink(missing_ok=True)
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
 (HERE/'THEOREM_INDEX_V169.json').write_text(json.dumps(index,indent=2)+'\n')
 render=HERE/'render-audit';render.mkdir(exist_ok=True)
 selected={'reconstruction':{1},'divisor-geometry':{1},'geometry':{1}}
 for key,rec in index.items():
  if key.endswith('v169') and key.startswith(('thm:','prop:')):
   name=rec['paper'];p=int(rec['page']);selected[name].update(range(p,min(p+2,outputs[name]['pages'])+1))
 for name,pages in selected.items():
  for page in sorted(pages):subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1400','-png',str(HERE/(name+'.pdf')),str(render/(name+'-'+str(page)))],check=True)
 return outputs,{n:sorted(p) for n,p in selected.items()}


def publish(root,receipt):
 text='# A2 revision 169 — complete referee entry\n\n'
 text+=f'Branch: `{BRANCH}`.\n\nControlling second v167 review: `{REVIEW}`.\n\nEarlier v167 review: `{FIRST_REVIEW}`.\n\nAuthored build commit: `{receipt["source_commit"]}`.\n\n'
 titles={'reconstruction':'Paper I — Finite failure schemes and the reconstruction of quadratic pencils','divisor-geometry':'Paper II — '+TITLE,'geometry':'Complete preservation master — not a third submission'}
 for n,title in titles.items():
  text+=f'## {title}\n\n{receipt["outputs"][n]["pages"]} pages. [Complete PDF]({REL}/{n}.pdf) · [Complete standalone LaTeX]({REL}/{n}.tex).\n\n'
 text+='''## Central mathematical changes

The marked family `[t^a : b s^a : c s t^(a-1)]` is treated for every `a >= 2`.
Its raw degree-m evaluation ideal factors as `b^C prod_j (b,c^j)^E_j`;
the primitive Rees algebra is normal and its graph is a chain of a point blow-ups.
Uniform monic equations give every embedded wall and chamber limit, including
all punctual modules and the cuspidal genus correction of length
`(a-1)(a-2)/2` and nilpotence order `a-1`. A sharp family jet bound is `ord(b)+1`.
The three-contact instance has seven explicit curve families, not just a
matrix encoding. The full fixed-degree polynomial graphs glue equivariantly
under actual source/target changes. A concrete map to the fixed-source Quot
scheme contracts the exceptional chain while the Hilbert graph separates it.

'''
 text+=f'All {receipt["predecessor_math_blocks"]} predecessor mathematical blocks and all {receipt["predecessor_labels"]} predecessor master labels are retained. Earlier main sections of Paper II are moved intact into appendices; historical manuscript sources are not modified. Both paper bodies partition the master exactly.\n\n'
 links=[('RESPONSE_TO_SECOND_V167_REPORT.md','Replies to all 66 requests in the controlling report'),('RESPONSE_TO_FIRST_V167_REPORT.md','Replies to all 66 requests in the first report'),('REFEREE_CROSSWALK_V169.md','Compiled theorem/page locators'),('THEOREM_DEPENDENCIES_V169.md','Proof dependencies'),('THEOREM_INDEX_V169.json','Complete theorem/page index'),('BUILD_RECEIPT_V169.json','Build receipt'),('NONDELETION_V169.json','Proof and label retention'),('EXACT_CHECKS_V169.json','Auxiliary exact checks'),('LITERATURE_AUDIT_V169.md','Primary-source comparison and documentary limits')]
 for n,title in links:text+=f'[{title}]({REL}/{n})\n\n'
 text+='''## Precise scope

The complete all-order fibre and curve classification is for the marked surface
family and its stated equivariant extensions, not the full fibre over B_3 or B_a.
The projective gluing is for one fixed-degree rational-map problem. It is not
an unproved all-Kronecker-strata compactification of quadratic pencils.
Higher-corank and singular-pencil Hilbert fibre classification, a full-B_a
integral-closure formula, and unequal interacting-contact classification are
not claimed as completed. The finite-algebra application still reconstructs
the specified effective family first. No external independent full proof audit
of Paper I or full Ballico 1993 comparison was obtained. Compilation and finite
checks certify reproducibility only, not mathematical proof, priority, or journal merit.

The partial v168 branch, both review branches, and all earlier revision branches
are untouched. This complete v169 package starts from the reviewed complete v167 sources.
'''
 for name in ('CURRENT_REVIEW_ENTRY.md','README.md'):
  src=root/name;dst=HERE/('PREVIOUS_ROOT_'+name.replace('.md','')+'_V167.md')
  if src.exists() and not dst.exists():shutil.copyfile(src,dst)
 (root/'CURRENT_REVIEW_ENTRY.md').write_text(text)
 (root/'A2_REVISION_V169_INDEX.md').write_text(text)
 (root/'README.md').write_text('# Theta-Theory — A2 revision 169\n\n[Current review entry](CURRENT_REVIEW_ENTRY.md) links the complete manuscripts, PDFs, both referee responses, theorem locations, and preservation/build receipts.\n\nThis isolated branch is based on the complete reviewed v167 package. Historical manuscript sources, review branches, and the partial v168 branch are unchanged.\n')
 (HERE/'CURRENT_REVIEW_ENTRY.md').write_text(text.replace(REL+'/',''))


def response_crosswalk():
 index=json.loads((HERE/'THEOREM_INDEX_V169.json').read_text());text='# A2 v169 — compiled referee locators\n\n'
 for source in ('RESPONSE_TO_SECOND_V167_REPORT.md','RESPONSE_TO_FIRST_V167_REPORT.md'):
  text+='## '+source+'\n\n'
  for item in re.split(r'(?=^### \d+\.)',(HERE/source).read_text(),flags=re.M)[1:]:
   heading=item.splitlines()[0][4:];keys=sorted(set(re.findall(r'(?:thm|prop|cor|lem|eq|sec|ex):[a-zA-Z0-9-]+',item)))
   entries=[]
   for key in keys:
    if key not in index:continue
    r=index[key];entries.append(f'`{key}`: {r["paper"]}, {r["number"]}, p. {r["page"]} (master p. {r.get("master_page","n/a")})')
   text+='### '+heading+'\n\n'+('; '.join(entries) if entries else 'See the response text and its stated scope/documentary status.')+'\n\n'
 (HERE/'REFEREE_CROSSWALK_V169.md').write_text(text)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',action='store_true')
 ap.add_argument('--baseline',type=Path,default=HERE.parent/'v167')
 ap.add_argument('--root',type=Path,default=HERE.parents[3])
 ap.add_argument('--local-audit',action='store_true')
 args=ap.parse_args();args.root.mkdir(parents=True,exist_ok=True)
 validated={}
 reports=[('second','reviews/a2-v167-second-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md','CONTROLLING_SECOND_V167_REPORT.md',REPORT_BLOB),('first','reviews/a2-v167-independent-harsh-top4-2026-09-26/REFEREE_REPORT.md','EARLIER_FIRST_V167_REPORT.md',FIRST_BLOB)]
 for key,path,out,expected in reports:
  report=args.root/path
  if report.exists():
   data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   require(blob==expected,'Wrong report bytes: '+key)
   (HERE/out).write_bytes(data);validated[key]=True
  else:
   require(args.local_audit and not os.environ.get('GITHUB_ACTIONS'),'Both report byte locks required for publication')
   validated[key]=False
 for n in ('RESPONSE_TO_SECOND_V167_REPORT.md','RESPONSE_TO_FIRST_V167_REPORT.md'):
  require(list(map(int,re.findall(r'^### (\d+)\.',(HERE/n).read_text(),re.M)))==list(range(1,67)),'All 66 response items required: '+n)
 templates,receipt=assemble(args.baseline)
 receipt.update(source_commit=os.environ.get('GITHUB_SHA','local-prepublication-audit'),report_blob_locks={'second':REPORT_BLOB,'first':FIRST_BLOB},report_bytes_validated=validated,compiled=False)
 if args.build:
  outputs,rendered=build(templates)
  receipt.update(compiled=True,outputs=outputs,rendered_pages=rendered,companion_references_stabilized=True)
  checks=json.loads((HERE/'EXACT_CHECKS_V169.json').read_text());require(checks['all_checks_pass'],'Exact checks required')
  receipt['inherited_v167_full_chain_rerun']=checks['inherited_v167_full_chain_rerun']
  response_crosswalk();publish(args.root,receipt)
 manifest={p.name:sha(p) for p in HERE.iterdir() if p.suffix in ('.py','.tex','.md') and not p.name.startswith(('PREVIOUS_','geometry','reconstruction','divisor-geometry','CURRENT_REVIEW_ENTRY'))}
 (HERE/'SOURCE_MANIFEST_V169.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (HERE/'BUILD_RECEIPT_V169.json').write_text(json.dumps(receipt,indent=2)+'\n')
 for name,pin in PINS.items():require(sha(args.baseline/(name+'.tex'))==pin,'Historical source changed')
 print(json.dumps({'compiled':receipt['compiled'],'retained_blocks':receipt['predecessor_math_blocks'],'current_blocks':receipt['current_math_blocks'],'outputs':receipt.get('outputs',{})},indent=2))
if __name__=='__main__':main()
